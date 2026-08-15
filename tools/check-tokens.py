"""Drift guard for the Chememan design-system token files.

tokens/tokens.css, tokens/tokens.json, and tokens/tailwind.preset.js are
hand-mirrored (see README.md "Updating this system") -- out-of-sync token
files are the documented #1 source of silent brand drift in this repo.

v2 (2026-08-15): rewritten to compare BY NORMALIZED KEY, not by value set.
The v1 checker compared "the set of hex colors in file A" against "the set
of hex colors in file B" -- so a name<->value swap (e.g. green and teal
trading hex values) left the set unchanged and passed clean. This version
looks up the SAME logical token (e.g. "color.brand.green") in all three
files and requires the value to agree; a swap now changes what one file
says for that specific key, which the other two still disagree with.

This script asserts:
  (a) every logical token in one of the categories below (colors, layout,
      font size/weight/tracking, radius, shadow, border, focus) resolves to
      the SAME value in every file that defines it. A file that simply does
      not carry a given token (e.g. tailwind.preset.js has no "focus.ring"
      equivalent) is not required to -- only files that DO define a key must
      agree on its value.
  (b) `var(--x)` references (including ones with a fallback, `var(--x, #fff)`)
      are resolved against tokens.css before comparison, so a value written
      as `var(--cman-neutral-300)` in one file and the literal hex in
      another are recognised as equal.
  (c) every `var(--cman-*)` / `var(--sidebar-*)` / `var(--transition)`
      reference used anywhere in the live-app-system docs resolves to a
      definition in tokens/tokens.css -- including `var(--name, fallback)`
      forms, where an undefined `--name` must still fail even though the
      fallback makes the CSS itself valid.
  (d) non-zero exit with a readable diff on any failure -- a renamed or
      missing tokens.json key produces a `FAIL` line naming the key, never
      a raw KeyError/traceback.

Scope for (c): only the files that consume the LIVE-APP token system are
scanned (see LIVE_APP_FILES below). The CI-book legacy system
(tokens/brand-ci-legacy.css, typography/fonts.css, examples/hero.html,
adapters/html-slides/, adapters/pptx/) defines and uses its own, different
`--cman-*` variables (e.g. --cman-forest) and is intentionally out of scope.

Run: python tools/check-tokens.py
Stdlib only. UTF-8 on every file read.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_DIR = os.path.join(ROOT, "tokens")

# Files that consume tokens/tokens.css in the live-app (default) system --
# deliberately excludes the CI-book legacy system (brand-ci-legacy.css,
# fonts.css, hero.html, html-slides/, pptx/), which has its own token set.
LIVE_APP_FILES = [
    os.path.join(TOKENS_DIR, "tokens.css"),
    os.path.join(ROOT, "typography", "TYPOGRAPHY.md"),
    os.path.join(ROOT, "components", "COMPONENTS.md"),
    os.path.join(ROOT, "patterns", "PATTERNS.md"),
    os.path.join(ROOT, "adapters", "web", "WEB.md"),
    os.path.join(ROOT, "examples", "app-shell.html"),
    os.path.join(ROOT, "README.md"),
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def normalize(value):
    """Collapse whitespace + stringify so hand-mirrored values compare equal
    regardless of spacing style or JSON number-vs-string ("rgba(26, 71, 42,
    .35)" vs "rgba(26,71,42,.35)"; 600 vs "600")."""
    if value is None:
        return None
    value = str(value).strip()
    value = re.sub(r"\s*,\s*", ",", value)
    return re.sub(r"\s+", " ", value)


# --- CSS custom-property parsing + var() resolution -----------------------

CSS_DECL_RE = re.compile(r"(--[\w-]+):\s*([^;]+);")
# Consumes the WHOLE var() call (name + optional fallback) so it can be
# substituted in place -- deliberately separate from USED_VAR_RE below,
# which only needs to capture the name for the "is it defined" check.
VAR_CALL_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")
# Widened per the (c) check requirement: matches both `var(--name)` and
# `var(--name, fallback)` -- a defined fallback must NOT hide an undefined
# variable name from this check.
USED_VAR_RE = re.compile(r"var\(\s*(--[\w-]+)\s*[,)]")


def parse_css_vars(css_text):
    """Every `--name: value;` custom-property declaration in tokens.css,
    raw (unresolved)."""
    return {name: value.strip() for name, value in CSS_DECL_RE.findall(css_text)}


def resolve_text(raw_vars, text, _stack=frozenset()):
    """Substitute every var(--name[, fallback]) in `text` with its resolved
    value from raw_vars, chasing alias chains (e.g. --cman-neutral-300 ->
    var(--cman-surface-300) -> #dee2e6). Works on values from ANY of the
    three files -- if tokens.json/tailwind.preset.js embed the same
    `var(--sidebar-active-border)` text tokens.css itself uses (as
    `--cman-sh-collapsed-active-inset` does), resolving all three the same
    way keeps them comparable. Cycle-safe; gives up after 10 passes."""
    if text is None:
        return None
    text = str(text)

    def sub(m):
        ref = m.group(1)
        if ref in _stack or ref not in raw_vars:
            return m.group(0)
        return resolve_text(raw_vars, raw_vars[ref], _stack | {ref})

    for _ in range(10):
        new_text = VAR_CALL_RE.sub(sub, text)
        if new_text == text:
            break
        text = new_text
    return normalize(text)


def css_val(raw_vars, name):
    if name not in raw_vars:
        return None
    return resolve_text(raw_vars, raw_vars[name])


# --- tokens.json path lookup (never raises) --------------------------------

def jget(tok, path):
    """Dotted-path getter into tokens.json. Returns (value, None) on success
    or (None, "readable reason") on a missing/renamed key -- so a renamed
    tokens.json key produces a FAIL line, never a KeyError traceback."""
    cur = tok
    parts = path.split(".")
    for i, part in enumerate(parts):
        if not isinstance(cur, dict) or part not in cur:
            return None, f"tokens.json missing '{path}' (renamed or removed key?)"
        cur = cur[part]
    if isinstance(cur, dict):
        if "value" in cur:
            cur = cur["value"]
        else:
            return None, f"tokens.json '{path}' is an object with no 'value' leaf"
    return cur, None


# --- tailwind.preset.js parsing (regex, stdlib-only) -----------------------

# Matches a bare-word/number key OR a quoted (possibly hyphenated) key,
# followed by a single-quoted string value -- covers both `50: '#fff'` and
# `'teal-alt': '#20c997'` shapes used in this file.
KV_RE = re.compile(r"(?:'([\w-]+)'|(\w+)):\s*'([^']*)'")


def parse_kv_pairs(body):
    out = {}
    for m in KV_RE.finditer(body):
        key = m.group(1) or m.group(2)
        out[key] = m.group(3)
    return out


def js_const_object(js_text, const_name):
    """`key: 'value'` pairs from a top-level `const NAME = { ... };` block."""
    m = re.search(r"const %s = \{(.*?)\n\};" % re.escape(const_name), js_text, re.S)
    return parse_kv_pairs(m.group(1)) if m else {}


def js_theme_block(js_text, key):
    """`key: 'value'` pairs from a `themeKey: { ... },` block inside
    `theme.extend`. Non-greedy, stops at the first top-level `},` -- safe
    here because none of these blocks nest braces."""
    m = re.search(r"\b%s:\s*\{(.*?)\n\s*\},\n" % re.escape(key), js_text, re.S)
    return parse_kv_pairs(m.group(1)) if m else {}


# --- generic keyed comparison ----------------------------------------------

def compare(label, values, fails, diffs):
    """values: {source_name: value}. Every source key the CALLER includes in
    this dict is EXPECTED to carry the token -- omit a source key entirely
    when that source never carries this concept by design (e.g.
    tailwind.preset.js has no brand.white/black color, no layout.sidebar-bg
    spacing entry). A value that resolves to None for an expected source is
    reported as "<MISSING>", never silently dropped -- that's what makes a
    token quietly deleted from one file (e.g. a status color removed from
    tailwind.preset.js) fail instead of passing clean. A key present in only
    0-1 sources can't drift against anything, so it's skipped."""
    if len(values) < 2:
        return
    shown = {src: (val if val is not None else "<MISSING>") for src, val in values.items()}
    if len(set(shown.values())) > 1:
        fails.append(f"{label} value drift")
        parts = " ".join(f"{src}={val}" for src, val in shown.items())
        diffs.append(f"  {label}: {parts}")


def main():
    fails = []
    diffs = []

    css_path = os.path.join(TOKENS_DIR, "tokens.css")
    json_path = os.path.join(TOKENS_DIR, "tokens.json")
    js_path = os.path.join(TOKENS_DIR, "tailwind.preset.js")

    css_text = read(css_path)
    js_text = read(js_path)
    tok = json.loads(read(json_path))

    raw_vars = parse_css_vars(css_text)

    def css(name):
        return css_val(raw_vars, name)

    def jval(path):
        v, err = jget(tok, path)
        if err:
            fails.append(f"{path}: {err}")
            return None
        return resolve_text(raw_vars, v)

    # ---- color.brand: green, teal, light, lighter, white, black ----------
    # white/black have NO tailwind mirror by design -- their "tailwind" key is
    # omitted below rather than passed as None, so that omission reads as
    # "not expected here" and not "value went missing".
    js_colors = js_theme_block(js_text, "colors")
    green_const = js_const_object(js_text, "green")
    brand_js = {
        "green": green_const.get("DEFAULT"),
        "teal": js_colors.get("cman-teal"),
        "light": js_colors.get("cman-light"),
        "lighter": js_colors.get("cman-lighter"),
    }
    for key in ("green", "teal", "light", "lighter", "white", "black"):
        values = {"css": css(f"--cman-{key}"), "json": jval(f"color.brand.{key}")}
        if key in brand_js:
            values["tailwind"] = resolve_text(raw_vars, brand_js[key])
        compare(f"color.brand.{key}", values, fails, diffs)

    # ---- color.green-ramp: 50..900 ---------------------------------------
    for step in ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900"):
        compare(
            f"color.green-ramp.{step}",
            {
                "css": css(f"--cman-green-{step}"),
                "json": jval(f"color.green-ramp.{step}"),
                "tailwind": resolve_text(raw_vars, green_const.get(step)),
            },
            fails, diffs,
        )

    # ---- color.surface (+ neutral alias must mirror it) -------------------
    surface_const = js_const_object(js_text, "surface")
    for step in ("0", "25", "50", "75", "100", "150", "200", "300", "400", "500",
                 "600", "700", "800", "900"):
        compare(
            f"color.surface.{step}",
            {
                "css": css(f"--cman-surface-{step}"),
                "json": jval(f"color.surface.{step}"),
                "tailwind": resolve_text(raw_vars, surface_const.get(step)),
            },
            fails, diffs,
        )
        # the --cman-neutral-*/color.neutral.*/neutral(JS) alias must resolve
        # to the exact same value as its surface counterpart
        compare(
            f"color.neutral.{step} (alias of surface.{step})",
            {
                "css": css(f"--cman-neutral-{step}"),
                "json": jval(f"color.neutral.{step}"),
            },
            fails, diffs,
        )

    # ---- color.status: 10 badges, bg + fg ---------------------------------
    status_const = js_const_object(js_text, "status")
    for name in ("primary", "orange", "teal-alt", "warning", "success", "cyan",
                 "indigo", "purple", "dark", "danger"):
        compare(
            f"color.status.{name}.bg",
            {
                "css": css(f"--cman-status-{name}"),
                "json": jval(f"color.status.{name}.bg"),
                "tailwind": status_const.get(name),
            },
            fails, diffs,
        )
        compare(
            f"color.status.{name}.fg",
            {
                "css": css(f"--cman-status-{name}-fg"),
                "json": jval(f"color.status.{name}.fg"),
            },
            fails, diffs,
        )

    # ---- color.gradient -----------------------------------------------------
    bgimg_js = js_theme_block(js_text, "backgroundImage")
    for key, js_key in (("login-bg", "cman-grad-login-bg"), ("login-header", "cman-grad-login-header")):
        compare(
            f"color.gradient.{key}",
            {
                "css": css(f"--cman-grad-{key}"),
                "json": jval(f"color.gradient.{key}"),
                "tailwind": resolve_text(raw_vars, bgimg_js.get(js_key)),
            },
            fails, diffs,
        )

    # ---- layout -------------------------------------------------------------
    spacing_js = js_theme_block(js_text, "spacing")
    layout_map = [
        ("sidebar-width", "--sidebar-width", "cman-sidebar"),
        ("sidebar-collapsed-width", "--sidebar-collapsed-width", "cman-sidebar-collapsed"),
        ("navbar-height", "--cman-navbar-height", "cman-navbar"),
        ("sidebar-bg", "--sidebar-bg", None),
        ("sidebar-active", "--sidebar-active", None),
        ("sidebar-active-border", "--sidebar-active-border", None),
        ("transition", "--transition", None),
    ]
    for key, css_name, js_key in layout_map:
        values = {"css": css(css_name), "json": jval(f"layout.{key}")}
        if js_key:
            values["tailwind"] = resolve_text(raw_vars, spacing_js.get(js_key))
        compare(f"layout.{key}", values, fails, diffs)

    # ---- font.size (existing coverage, now keyed) --------------------------
    fontsize_js = js_theme_block(js_text, "fontSize")
    for key in ("2xs", "xs", "sm", "sm2", "base-sm", "md", "md2", "lg", "lg2",
                "xl", "xl2", "2xl", "3xl", "h5", "h4"):
        compare(
            f"font.size.{key}",
            {
                "css": css(f"--cman-fs-{key}"),
                "json": jval(f"font.size.{key}"),
                "tailwind": fontsize_js.get(f"cman-{key}"),
            },
            fails, diffs,
        )

    # ---- font.weight (NEW coverage) ----------------------------------------
    fontweight_js = js_theme_block(js_text, "fontWeight")
    for key in ("regular", "semibold", "bold"):
        compare(
            f"font.weight.{key}",
            {
                "css": css(f"--cman-fw-{key}"),
                "json": jval(f"font.weight.{key}"),
                "tailwind": fontweight_js.get(f"cman-{key}"),
            },
            fails, diffs,
        )

    # ---- font.tracking / letter-spacing (NEW coverage) ---------------------
    # canonical key -> (css suffix, json key, js letterSpacing suffix).
    # tokens.css spells these WITHOUT hyphens (`--cman-ls-tablehead`) while
    # tokens.json/tailwind.preset.js use the hyphenated form (`table-head`)
    # -- an explicit map avoids a wrong guess at a shared naming scheme.
    tracking_map = [
        ("badge", "badge", "badge", "badge"),
        ("table-head", "tablehead", "table-head", "table-head"),
        ("sidebar-brand", "sidebarbrand", "sidebar-brand", "sidebar-brand"),
        ("section-title", "sectiontitle", "section-title", "section-title"),
        ("login-brand", "loginbrand", "login-brand", "login-brand"),
        ("sidebar-section", "sidebarsection", "sidebar-section", "sidebar-section"),
        ("login-sub", "loginsub", "login-sub", "login-sub"),
    ]
    letterspacing_js = js_theme_block(js_text, "letterSpacing")
    for canon, css_suffix, json_key, js_suffix in tracking_map:
        compare(
            f"font.tracking.{canon}",
            {
                "css": css(f"--cman-ls-{css_suffix}"),
                "json": jval(f"font.tracking.{json_key}"),
                "tailwind": letterspacing_js.get(f"cman-{js_suffix}"),
            },
            fails, diffs,
        )

    # ---- radius (existing coverage, now keyed) -----------------------------
    radius_js = js_theme_block(js_text, "borderRadius")
    for key in ("xs", "sm", "md", "lg"):
        compare(
            f"radius.{key}",
            {
                "css": css(f"--cman-r-{key}"),
                "json": jval(f"radius.{key}"),
                "tailwind": radius_js.get(f"cman-{key}"),
            },
            fails, diffs,
        )

    # ---- shadow (existing coverage, now keyed) -----------------------------
    # canonical key -> (css/json suffix, js boxShadow suffix). Only
    # "btn-hover" differs: css/json spell it "btn-cman-hover", the tailwind
    # preset drops the middle "cman" ("cman-btn-hover" -> suffix "btn-hover").
    shadow_map = [
        ("card", "card", "card"),
        ("sidebar", "sidebar", "sidebar"),
        ("btn-hover", "btn-cman-hover", "btn-hover"),
        ("sticky-header", "sticky-header", "sticky-header"),
        ("collapsed-active-inset", "collapsed-active-inset", "collapsed-active-inset"),
    ]
    boxshadow_js = js_theme_block(js_text, "boxShadow")
    for canon, suffix, js_suffix in shadow_map:
        compare(
            f"shadow.{canon}",
            {
                "css": css(f"--cman-sh-{suffix}"),
                "json": jval(f"shadow.{suffix}"),
                "tailwind": resolve_text(raw_vars, boxshadow_js.get(f"cman-{js_suffix}")),
            },
            fails, diffs,
        )

    # ---- border (NEW coverage) ----------------------------------------------
    borderwidth_js = js_theme_block(js_text, "borderWidth")
    WIDTH_RE = re.compile(r"^\s*(\d+px)")

    def width_only(value):
        if value is None:
            return None
        m = WIDTH_RE.match(value)
        return m.group(1) if m else value

    border_full_map = [
        ("card", "card", "card", None),
        ("nav-tabs", "navtabs", "nav-tabs", "cman-navtabs"),
        ("hairline", "hairline", "hairline", "cman-hairline"),
    ]
    for canon, css_suffix, json_key, js_key in border_full_map:
        css_v = css(f"--cman-border-{css_suffix}")
        json_v = jval(f"border.{json_key}")
        compare(f"border.{canon}", {"css": css_v, "json": json_v}, fails, diffs)
        if js_key:
            compare(
                f"border.{canon} (width)",
                {
                    "css": width_only(css_v),
                    "json": width_only(json_v),
                    "tailwind": borderwidth_js.get(js_key),
                },
                fails, diffs,
            )
    # sidebar active-item border widths -- css names them by px value
    # ("active-3"/"active-2"), json names them by role -- no JS mirror.
    compare(
        "border.active-left-width",
        {"css": css("--cman-border-active-3"), "json": jval("border.active-left-width")},
        fails, diffs,
    )
    compare(
        "border.active-bottom-width",
        {"css": css("--cman-border-active-2"), "json": jval("border.active-bottom-width")},
        fails, diffs,
    )

    # ---- focus (NEW coverage) ------------------------------------------------
    ringcolor_js = js_theme_block(js_text, "ringColor")
    compare(
        "focus.border",
        {
            "css": css("--cman-focus-border"),
            "json": jval("focus.border"),
            "tailwind": ringcolor_js.get("cman-focus"),
        },
        fails, diffs,
    )
    compare(
        "focus.ring",
        {"css": css("--cman-focus-ring"), "json": jval("focus.ring")},
        fails, diffs,
    )

    # ---- (c) every var(--cman-*)/--sidebar-*/--transition used in the
    #      live-app docs must resolve to a tokens.css definition -----------
    defined = set(raw_vars)
    for path in LIVE_APP_FILES:
        if not os.path.exists(path):
            continue
        used = {m for m in USED_VAR_RE.findall(read(path))}
        undefined = used - defined
        if undefined:
            rel = os.path.relpath(path, ROOT)
            fails.append(f"undefined var(...) reference in {rel}")
            diffs.append(f"  {rel}: {sorted(undefined)}")

    # ---- report -------------------------------------------------------------
    if fails:
        print("=== check-tokens.py: DRIFT DETECTED ===")
        for f in fails:
            print("  FAIL", f)
        print("--- diff ---")
        for d in diffs:
            print(d)
        print()
        print("VERDICT: FAIL")
        return 1

    print("=== check-tokens.py: OK ===")
    print("  color (brand / green-ramp / surface / neutral-alias / status / gradient) "
          "agrees across tokens.css, tokens.json, tailwind.preset.js")
    print("  layout, font (size/weight/tracking), radius, shadow, border, focus "
          "agree by key across all files that define them")
    print(f"  all var(--cman-*) references in the {len(LIVE_APP_FILES)} live-app "
          f"files resolve to tokens.css")
    print()
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
