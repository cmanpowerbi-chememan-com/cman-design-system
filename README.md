# Chememan Design System

A token-driven design system carrying **jakkaritw's approved 2026-08-15
theme** for the Chememan Budget Management web app (Next.js + React,
`c:\04.budget_management_web`), so other internal apps can drop it in and
look consistent. Rebuilt 2026-08-15.

This repo carries **exactly ONE style** — there used to be two ("live
Supply Chain app" system and, before that, a CI-book/glassmorphism system);
both are retired. If you're looking for either of those, they only exist in
this repo's git history before this rebuild — nothing current here traces
back to them.

**Honest provenance**: every value below traces back to
`c:\04.budget_management_web\frontend\src\styles\tokens.css` /
`global.css` and the decision record in
`design/mockups/theme-shell-green-handoff-prompt.md` (both read-only
sources in that repo, mirrored here) — **not** to
`sc-qas.chememan.com`. An earlier version of this repo's README claimed
every value traced to `reference/sc-qas-extracted/`; that folder and the
system it backed are gone.

## TL;DR (humans)

```bash
# View the demo — no build step, just open it:
open examples/app-shell.html

# Check the token files are still in lockstep before committing a change:
python tools/check-tokens.py
```

## What's inside

- **Tokens** (`tokens/`) — colors, type scale, weights,
  letter-spacing, radius, spacing. `tokens.json` is authoritative;
  `tokens.css` mirrors it as CSS custom properties; `tailwind.preset.js`
  forwards `var(--cman-*)` references into Tailwind (no duplicated
  literals — see its header comment); `tokens.pptx.json` mirrors the
  colors for PptxGenJS decks.
- **Typography** (`typography/`) — the app's actual font stack (Bootstrap's
  system-font default — the app loads no custom webfont).
- **Components** (`components/`) — copy-paste HTML+CSS for the nav shell,
  buttons, cards, status pills, the budget data grid, GL-group chips, the
  ฝ่าย (department) picker, forms, and loading/empty/error states — all
  built from `tokens/tokens.css` custom properties, matching the real
  class names in the source app's `global.css`.
- **Patterns** (`patterns/`) — the page shapes the source app actually
  uses: app shell, the budget grid page, and a modal/subform pattern.
- **Adapters** (`adapters/`) — drop-in guides: `web/` (plain HTML/CSS +
  Tailwind, no framework required), `html-slides/`, `pptx/`.
- **Examples** (`examples/app-shell.html`) — a self-contained page
  (tokens.css only, no build step, no CDN) showing the shell, a card, the
  budget grid, buttons, and status pills.
- **Assets** (`assets/`) — `logo/chememan-full-logo.png` and
  `characters/chememan-character.png`. That is the whole folder now —
  the FC Minimal webfont (36 files) shipped here before this rebuild is
  gone; the system ships no custom font.

## The theme, at a glance

| Role | Token | Value |
|---|---|---|
| Page shell / nav background | `--cman-shell` | `#2e8b57` |
| Brand accent (button fill, links) | `--cman-green` | `#2e8b57` |
| Hover / lighter step | `--cman-teal` | `#3fa06e` |
| Card surface | `--cman-surface` | `#fbf9f3` |
| Card surface, inset | `--cman-surface-inset` | `#eae4d7` |
| Ink (primary text on a card) | `--cman-ink` | `#1c1a16` |
| Accent text on a card | `--cman-accent-text` | `#b24222` |
| Status — SAP | `--cman-status-sap` | `#5e7a50` |
| Status — Approved | `--cman-status-approved` | `#4a5e80` |
| Special row | `--cman-special-bg` / `--cman-special-edge` | `#f0e7d3` / `#c9a24b` |

Full table with roles + every token → `tokens/tokens.json`.

## The contrast rule — read this before using on-shell tokens

`#2e8b57` (the light-theme shell) is light enough that **no** ink color
reaches WCAG AA (4.5:1 for small text) painted directly on it. Pure white
tops out at **4.25:1** — jakkaritw's accepted trade-off (2026-08-15): keep
the picked green exactly as-is and accept 4.25 as the ceiling, rather than
darken the brand color to chase AA. Practical rules that follow from this:

- `--cman-ink-on-shell` / `--cman-ink-on-shell-2` / `--cman-accent-on-shell`
  are all white in light theme (the muted tier and the old gold accent
  both failed outright — `#c6c0b2` measured 2.34:1, `#d4ac52` measured
  1.99:1 — and are retired for this role).
- Never paint `--cman-teal` or `--cman-status-approved` directly on
  `--cman-shell` — untested for AA there, and the source app never does it.
- If text needs to be small AND contrast-critical, put it on a card
  (`--cman-surface`), not directly on the shell.

Full WCAG math (every fg/bg ratio) → run
`python tools/check-tokens.py` for token-file consistency and see the
provenance chain in `tokens/tokens.css`'s header comment for where the
numbers come from.

## DS token ↔ app token mapping

The design system's public API (`--cman-*`) maps onto the budget app's own
token names as follows — use this table when porting a component:

| DS token (`tokens/tokens.css`) | Budget app token (`frontend/src/styles/tokens.css`) |
|---|---|
| `--cman-shell` | `--paper` |
| `--cman-green` | `--accent` (light theme: also `--paper`, `--c-forest`) |
| `--cman-teal` | `--accent-2` (also `--c-mint`, `--c-blue`) |
| `--cman-surface` | `--surface` |
| `--cman-surface-inset` | `--paper-2` |
| `--cman-ink` / `--cman-ink-2` / `--cman-ink-3` | `--ink` / `--ink-2` / `--ink-3` |
| `--cman-line` / `--cman-line-2` | `--line` / `--line-2` |
| `--cman-ink-on-shell` / `--cman-ink-on-shell-2` | `--ink-on-shell` / `--ink-on-shell-2` |
| `--cman-accent-on-shell` | `--accent-on-shell` |
| `--cman-accent-text` | `--accent-text` |
| `--cman-line-on-shell` | `--line-on-shell` |
| `--cman-status-sap` / `-approved` / `-pending` | `--status-sap` / `--status-approved` / `--status-pending` |
| `--cman-special-bg` / `-edge` | `--special-bg` / `--special-edge` |
| `--cman-focus-ring` | `--focus-ring` |
| `--cman-font-sans` / `-serif` / `-mono` | `--sans` / `--serif` / `--mono` |
| `--cman-r-base` | `--r` |

The budget app can adopt this design system by linking `tokens/tokens.css`
and mapping its own `--paper`/`--accent`/etc. call sites to the `--cman-*`
names above (or vice versa) — no value guesswork needed.

## File structure

```
tokens/
  tokens.json               ← authoritative machine-readable tokens
  tokens.css                ← CSS custom properties, mirrors tokens.json
  tokens.pptx.json           ← PptxGenJS mirror (regenerated for this theme)
  tailwind.preset.js         ← Tailwind preset — var(--cman-*) passthrough, no duplicated literals
typography/
  TYPOGRAPHY.md              ← font stack, type scale, weights, tracking
components/
  COMPONENTS.md              ← nav, buttons, cards, status pills, budget grid, GL chips, ฝ่าย picker, forms
patterns/
  PATTERNS.md                ← app shell, budget grid page, modal/subform
adapters/
  web/WEB.md                 ← plain HTML/CSS + optional Tailwind drop-in
  html-slides/HTML_SLIDES.md ← scrollable / kiosk decks using this theme
  pptx/PPTX.md                ← PptxGenJS master + slide-type cookbook
examples/
  app-shell.html              ← working demo, self-contained (tokens.css only)
assets/
  logo/chememan-full-logo.png
  characters/chememan-character.png
```

## Updating this system

- **`tokens/tokens.json` is authoritative** — edit it first, then mirror to
  `tokens/tokens.css` by hand. `tokens/tailwind.preset.js` never needs a
  matching edit for a value change — it only forwards `var(--cman-*)`
  names, so it only needs touching when you add or rename a token. After
  editing tokens, run the drift guard:

  ```bash
  python tools/check-tokens.py
  ```

  It resolves every token in the `:root` context — chasing `var()` alias
  chains the same way a browser would — and fails with a readable diff on
  any mismatch between `tokens.css` and `tokens.json`, or on any
  `var(--cman-*)` reference in the docs/`tailwind.preset.js` that doesn't
  resolve to a real `tokens.css` definition. Run it before committing any
  token change.
- Adding a component or pattern? Append to the relevant `.md` with a
  working snippet — don't create a sub-file unless it's genuinely large
  (>500 lines).
- If the app's own theme changes again (a new jakkaritw-approved color,
  a new component), re-read `frontend/src/styles/tokens.css` +
  `global.css` first, then propagate: tokens → components → patterns →
  adapters, in that order.
