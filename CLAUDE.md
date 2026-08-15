# Chememan Design System — agent brief

**Read this file before producing any Chememan-branded deliverable** that
should match the Budget Management web app's look — website, internal
admin page, scrollable HTML deck, or PPTX. The design system below is the
single source of truth. There is exactly **ONE** style in this repo as of
2026-08-15 — do not reintroduce a second one (this repo used to carry two:
a "live Supply Chain app" extraction and, before that, a CI-book/
glassmorphism system; both are retired and only exist in git history now).

If a request asks for something this system doesn't cover (e.g. a genuinely
different brand direction for an investor deck), **flag the conflict**
before inventing an off-system variant — don't silently extend this repo
with a second palette.

---

## Folder map

```
CLAUDE.md                    ← this file (auto-loaded entry point)
README.md                    ← human-facing usage doc (start here for tutorials)
tokens/
  tokens.json                ← canonical machine-readable tokens (authoritative, light + dark)
  tokens.css                 ← CSS custom properties, mirrors tokens.json
  tokens.pptx.json           ← PptxGenJS-friendly mirror
  tailwind.preset.js         ← Tailwind preset — var(--cman-*) passthrough, no duplicated literals
typography/
  TYPOGRAPHY.md               ← font stack + type scale + weights + tracking
components/
  COMPONENTS.md               ← nav, buttons, cards, status pills, budget grid, GL chips, ฝ่าย picker, forms
patterns/
  PATTERNS.md                 ← app shell, budget grid page, modal/subform
adapters/
  web/WEB.md                  ← plain HTML/CSS + optional Tailwind drop-in
  html-slides/HTML_SLIDES.md  ← scrollable / kiosk decks
  pptx/PPTX.md                 ← PptxGenJS master + slide-type cookbook
examples/
  app-shell.html               ← working demo: nav + card + budget grid + buttons + status pills
assets/
  logo/chememan-full-logo.png
  characters/chememan-character.png
```

## Provenance — read this before trusting a value

Every token traces to **jakkaritw's approved 2026-08-15 theme** for the
Budget Management web app:

```
c:\04.budget_management_web\frontend\src\styles\tokens.css   (token defs)
c:\04.budget_management_web\frontend\src\styles\global.css   (real call sites)
c:\04.budget_management_web\design\mockups\theme-shell-green-handoff-prompt.md  (decision record)
c:\04.budget_management_web\design\mockups\theme-shell-green-contrast.py       (WCAG math)
```

Those are **read-only sources** for this repo — never edit them from here.
If the app's theme changes again, re-read them, then propagate: tokens →
components → patterns → adapters, in that order (see README.md
"Updating this system").

## Brand non-negotiables

- **Shell color** = Sea Green `#2e8b57` (light theme). jakkaritw picked
  this over a deeper `#1a4e31` that would have kept the old gold accent —
  do not "fix" the lighter shade back to the deep one; that was a rejected
  alternative, not a draft.
- **On-shell text is white**, not cream/gold. The muted on-shell tier and
  the old gold accent both fail WCAG AA on this shell and are retired for
  that role — see the contrast rule below.
- **Cards stay light** (`--cman-surface` / `--cman-surface-inset`) in both
  themes except where the dark-theme override says otherwise — most of the
  app renders on cards floating on the shell, not directly on it.
- **No custom webfont.** The system font stack (Bootstrap 5.3.2's default)
  is the only typeface. FC Minimal and its 36 font files are retired —
  do not re-add `@font-face` to this system without a new, explicit
  decision from jakkaritw (this is not a revival of the old default).
- **Logo**: use the PNG in `assets/logo/`. Do not redraw, recolor, distort,
  or rotate it.

## The contrast rule (first-class, not a footnote)

`#2e8b57` is light enough that **no** ink color reaches WCAG AA (4.5:1)
painted directly on it — pure white tops out at 4.25:1, which is the
accepted ceiling for on-shell text (jakkaritw's 2026-08-15 trade-off).
Practical consequences:

- Never paint `--cman-teal`, `--cman-status-approved`, or any muted/gold
  ink directly on `--cman-shell` — they either fail outright or are
  untested there.
- Small, contrast-critical text belongs on a card
  (`--cman-surface`/`--cman-surface-inset`), not directly on the shell.
- Don't propose darkening the shell to "fix" the 4.25:1 ceiling — that is
  the accepted, signed-off trade-off, not an open bug.

## Quick recipes

**"Build an internal admin page that should look like the Budget app."**
1. Link `tokens/tokens.css` (no CDN or build step required — the system
   ships no custom font and no framework dependency).
2. Use the markup + CSS in `components/COMPONENTS.md` and the page shape
   in `patterns/PATTERNS.md` §1 (app shell).
3. If the project is Tailwind-based, layer in `tokens/tailwind.preset.js`
   instead of copy-pasting component CSS — see `adapters/web/WEB.md`.

**"Build a Chememan scrollable HTML slide deck."**
1. Follow `adapters/html-slides/HTML_SLIDES.md` — light shell/card
   aesthetic, not the old dark-glass CI-book look.
2. Link `tokens/tokens.css` only; no webfont to load.

**"Build a Chememan PPTX."**
1. Use the `pptx` skill.
2. Import `tokens/tokens.pptx.json` as the color/font source — never
   inline HEX.
3. Use `adapters/pptx/PPTX.md`'s master-slide template — light card deck,
   not the old dark hero/glass template.

## Canonical mistakes to avoid

- ❌ Reviving the CI-book Forest/Blue/Amber palette or the dark-glass/bento
  aesthetic — both are retired; if a request explicitly wants that look,
  say so and treat it as a new decision, not something to resurrect here.
- ❌ Adding `@font-face` / FC Minimal back — the system ships no custom
  webfont.
- ❌ Painting muted or gold ink directly on the shell — see the contrast
  rule above.
- ❌ Treating `--cman-shell` and `--cman-green` as always-identical — they
  hold the same value in light theme but diverge in dark theme (near-black
  shell + a separate lighter-green accent). Always use the token for the
  ROLE you mean (page background vs. button/link fill), not whichever
  happens to match visually in light theme.
- ❌ Hardcoded HEX or px values in new components — always reach into
  `tokens.css` (web) or `tokens.pptx.json` (PPTX).
- ❌ Inventing a font-size, radius, or spacing value the source app
  (`global.css`) doesn't actually use — the scale in `tokens/tokens.json`
  is curated from real call sites, not a generic design-token ladder.

## Updating this system

- Token changes go to `tokens/tokens.json` first (both `light` and `dark`
  values for colors); mirror to `tokens/tokens.css` immediately.
  `tokens/tailwind.preset.js` only needs an edit when you add/rename a
  token (it forwards `var(--cman-*)` names, never literal values). Run
  `python tools/check-tokens.py` before committing.
- Adding a component? Append to `components/COMPONENTS.md` with a working
  snippet — do **not** create a sub-file unless the component is genuinely
  large (>500 lines).
- New pattern? Same — append to `patterns/PATTERNS.md`.
- If you change anything in this folder, update `README.md`'s "at a
  glance" table too when a color/role changes — it's the first thing a
  human reads.
