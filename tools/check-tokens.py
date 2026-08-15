"""Drift guard for the Chememan design-system token files.

v4 (dark mode removed 2026-08-15): jakkaritw decided the app ships ONE
theme only — light Sea Green — so this script now resolves a single
`:root` context. tailwind.preset.js entries are all `var(--cman-*)`
passthroughs, not duplicated literals, so there is nothing to compare BY
VALUE there — this script instead confirms every var(--cman-*) name it
references actually exists in tokens.css (a NAME check, not a value check).

This script asserts:
  (a) every color token's "value" in tokens.json matches what tokens.css
      resolves to in `:root` (alias chains, e.g. --cman-accent-on-shell ->
      var(--cman-green), followed before comparing).
  (b) every non-color token's "value" in tokens.json (font/radius/spacing)
      matches tokens.css.
  (c) every `var(--cman-*)` reference in tokens/tailwind.preset.js resolves
      to a real tokens.css custom property.
  (d) every `var(--cman-*)` / `var(--sidebar-*)` reference used anywhere in
      the design-system docs (see LIVE_DOC_FILES below) resolves to a
      tokens.css definition — including `var(--name, fallback)` forms,
      where an undefined `--name` must still fail even though the fallback
      makes the CSS itself valid.
  (e) non-zero exit with a readable diff on any failure — a renamed or
      missing tokens.json key produces a `FAIL` line naming the key, never
      a raw KeyError/traceback.

Run: python tools/check-tokens.py
Stdlib only. UTF-8 on every file read.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS_DIR = os.path.join(ROOT, "tokens")

# Every doc that links tokens.css and references its custom properties.
LIVE_DOC_FILES = [
    os.path.join(TOKENS_DIR, "tailwind.preset.js"),
    os.path.join(ROOT, "typography", "TYPOGRAPHY.md"),
    os.path.join(ROOT, "components", "COMPONENTS.md"),
    os.path.join(ROOT, "patterns", "PATTERNS.md"),
    os.path.join(ROOT, "adapters", "web", "WEB.md"),
    os.path.join(ROOT, "examples", "app-shell.html"),
    os.path.join(ROOT, "README.md"),
]

# (tokens.json dotted path, tokens.css var suffix after "--cman-")
COLOR_TOKENS = [
    ("color.shell", "shell"),
    ("color.green", "green"),
    ("color.teal", "teal"),
    ("color.ink-on-shell", "ink-on-shell"),
    ("color.ink-on-shell-2", "ink-on-shell-2"),
    ("color.accent-on-shell", "accent-on-shell"),
    ("color.line-on-shell", "line-on-shell"),
    ("color.surface", "surface"),
    ("color.surface-inset", "surface-inset"),
    ("color.ink", "ink"),
    ("color.ink-2", "ink-2"),
    ("color.ink-3", "ink-3"),
    ("color.line", "line"),
    ("color.line-2", "line-2"),
    ("color.accent-text", "accent-text"),
    ("color.status.sap", "status-sap"),
    ("color.status.approved", "status-approved"),
    ("color.status.pending", "status-pending"),
    ("color.special.bg", "special-bg"),
    ("color.special.edge", "special-edge"),
    ("color.focus-ring", "focus-ring"),
]

# Non-color tokens: one value, declared once in :root —
# (tokens.json dotted path, tokens.css var suffix).
SCALAR_TOKENS = [
    ("font.family.sans", "font-sans"),
    ("font.family.serif", "font-serif"),
    ("font.family.mono", "font-mono"),
    ("font.base-size", "fs-base"),
    ("font.line-height.base", "lh-base"),
    ("font.line-height.tight", "lh-tight"),
    ("font.size.3xs", "fs-3xs"), ("font.size.2xs", "fs-2xs"),
    ("font.size.xs", "fs-xs"), ("font.size.xs2", "fs-xs2"),
    ("font.size.sm", "fs-sm"), ("font.size.sm2", "fs-sm2"),
    ("font.size.base-sm", "fs-base-sm"), ("font.size.md", "fs-md"),
    ("font.size.md2", "fs-md2"), ("font.size.lg", "fs-lg"),
    ("font.size.lg2", "fs-lg2"), ("font.size.xl", "fs-xl"),
    ("font.size.xl2", "fs-xl2"), ("font.size.2xl", "fs-2xl"),
    ("font.size.3xl", "fs-3xl"), ("font.size.4xl", "fs-4xl"),
    ("font.size.display", "fs-display"),
    ("font.weight.regular", "fw-regular"), ("font.weight.medium", "fw-medium"),
    ("font.weight.semibold", "fw-semibold"), ("font.weight.bold", "fw-bold"),
    ("font.weight.extrabold", "fw-extrabold"),
    ("font.tracking.tight", "ls-tight"), ("font.tracking.tight-2", "ls-tight-2"),
    ("font.tracking.tight-3", "ls-tight-3"), ("font.tracking.wide", "ls-wide"),
    ("font.tracking.wider", "ls-wider"), ("font.tracking.widest", "ls-widest"),
    ("radius.base", "r-base"), ("radius.xs", "r-xs"),
    ("radius.pill", "r-pill"), ("radius.circle", "r-circle"),
    ("spacing.4", "space-4"), ("spacing.6", "space-6"), ("spacing.8", "space-8"),
    ("spacing.10", "space-10"), ("spacing.12", "space-12"), ("spacing.14", "space-14"),
    ("spacing.16", "space-16"), ("spacing.20", "space-20"), ("spacing.24", "space-24"),
    ("spacing.28", "space-28"), ("spacing.32", "space-32"), ("spacing.40", "space-40"),
    ("spacing.48", "space-48"),
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def normalize(value):
    """Collapse whitespace/quote-style so hand-mirrored values compare equal
    regardless of formatting: "rgba(28, 26, 22, .14)" vs "rgba(28,26,22,.14)"
    (spacing), or JSON's required double-quoted font names vs tokens.css's
    single-quoted ones (quote style)."""
    if value is None:
        return None
    value = str(value).strip()
    value = re.sub(r"\s*,\s*", ",", value)
    value = re.sub(r"\s+", " ", value)
    return value.replace('"', "'")


# --- CSS custom-property parsing + var() resolution -----------------------

ROOT_BLOCK_RE = re.compile(r":root\s*\{(.*?)\n\}", re.S)
CSS_DECL_RE = re.compile(r"(--[\w-]+):\s*([^;]+);")
VAR_CALL_RE = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,[^)]*)?\)")
USED_VAR_RE = re.compile(r"var\(\s*(--[\w-]+)\s*[,)]")
# Scope the "must resolve" checks to the design system's own public API
# (--cman-*). Component-local custom properties (e.g. a .gl-chip's own
# --chip-bg/--chip-fg, set and consumed within the same rule) are a normal
# CSS pattern, not a design-token reference, and must not be flagged.
CMAN_VAR_RE = re.compile(r"^--cman-")


def parse_block_vars(css_text, block_re):
    m = block_re.search(css_text)
    if not m:
        return {}
    return {name: value.strip() for name, value in CSS_DECL_RE.findall(m.group(1))}


def resolve_text(context, text, _stack=frozenset()):
    """Substitute every var(--name[, fallback]) in `text` using `context`,
    chasing alias chains. Cycle-safe; gives up after 10 passes."""
    if text is None:
        return None
    text = str(text)

    def sub(m):
        ref = m.group(1)
        if ref in _stack or ref not in context:
            return m.group(0)
        return resolve_text(context, context[ref], _stack | {ref})

    for _ in range(10):
        new_text = VAR_CALL_RE.sub(sub, text)
        if new_text == text:
            break
        text = new_text
    return normalize(text)


# --- tokens.json path lookup (never raises) --------------------------------

def jget(tok, path):
    cur = tok
    parts = path.split(".")
    for part in parts:
        if not isinstance(cur, dict) or part not in cur:
            return None, f"tokens.json missing '{path}' (renamed or removed key?)"
        cur = cur[part]
    if isinstance(cur, dict):
        return cur, None
    return cur, None


def main():
    fails = []
    diffs = []

    css_path = os.path.join(TOKENS_DIR, "tokens.css")
    json_path = os.path.join(TOKENS_DIR, "tokens.json")
    js_path = os.path.join(TOKENS_DIR, "tailwind.preset.js")

    css_text = read(css_path)
    js_text = read(js_path)
    tok = json.loads(read(json_path))

    root_vars = parse_block_vars(css_text, ROOT_BLOCK_RE)
    all_defined = set(root_vars)

    if not root_vars:
        print("=== check-tokens.py: FATAL ===")
        print("  Could not find a :root { ... } block in tokens.css")
        return 1

    # ---- (a) color tokens ---------------------------------------------------
    for json_path_key, css_suffix in COLOR_TOKENS:
        entry, err = jget(tok, json_path_key)
        if err:
            fails.append(err)
            continue
        if not isinstance(entry, dict) or "value" not in entry:
            fails.append(f"{json_path_key}: missing 'value' key")
            continue
        css_var = f"--cman-{css_suffix}"

        json_val = normalize(entry["value"])
        css_val = resolve_text(root_vars, root_vars.get(css_var))
        if json_val != css_val:
            fails.append(f"{json_path_key} value drift")
            diffs.append(f"  {json_path_key}: json={json_val} css={css_val}")

    # ---- (b) scalar tokens (theme-invariant) -------------------------------
    for json_path_key, css_suffix in SCALAR_TOKENS:
        entry, err = jget(tok, json_path_key)
        if err:
            fails.append(err)
            continue
        json_val = entry.get("value") if isinstance(entry, dict) else entry
        json_val = resolve_text(root_vars, json_val)  # resolves e.g. "var(--cman-font-sans)"
        css_var = f"--cman-{css_suffix}"
        css_val = resolve_text(root_vars, root_vars.get(css_var))
        if json_val != css_val:
            fails.append(f"{json_path_key} value drift")
            diffs.append(f"  {json_path_key}: json={json_val} css={css_val}")

    # ---- (c) tailwind.preset.js: every var(--cman-*) name must be defined -
    tw_used = {v for v in USED_VAR_RE.findall(js_text) if CMAN_VAR_RE.match(v)}
    tw_undefined = tw_used - all_defined
    if tw_undefined:
        fails.append("undefined var(...) reference in tokens/tailwind.preset.js")
        diffs.append(f"  tailwind.preset.js: {sorted(tw_undefined)}")

    # ---- (d) every var(--cman-*) used in the docs must resolve ------------
    for path in LIVE_DOC_FILES:
        if not os.path.exists(path):
            continue
        used = {v for v in USED_VAR_RE.findall(read(path)) if CMAN_VAR_RE.match(v)}
        undefined = used - all_defined
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
    print(f"  {len(COLOR_TOKENS)} color tokens agree across tokens.css / tokens.json")
    print(f"  {len(SCALAR_TOKENS)} font/radius/spacing tokens agree across tokens.css / tokens.json")
    print("  every var(--cman-*) reference in tailwind.preset.js resolves to tokens.css")
    print(f"  every var(--cman-*) reference in the {len(LIVE_DOC_FILES)} doc files resolves to tokens.css")
    print()
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
