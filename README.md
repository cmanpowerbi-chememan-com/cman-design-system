# Chememan Design System

A token-driven design system extracted from the **live** Chememan Supply Chain
web app (https://sc-qas.chememan.com — QAS/staging), so other internal apps can
drop it in and look identical. Extracted 2026-08-15.

## TL;DR (humans)

```bash
# View the demo — no build step, just open it:
open examples/app-shell.html

# Use in a new Bootstrap project:
#    Follow adapters/web/WEB.md for the exact CDN + file drop-in order.
```

## What's inside

- **Tokens** (`tokens/`) — colors, type scale, radius, shadow, sidebar/layout
  metrics. `tokens.json`, `tokens.css`, and `tailwind.preset.js` stay in lockstep.
- **Typography** (`typography/`) — the live app's actual font stack (Bootstrap's
  system-font default — the app loads no custom webfont) plus the optional
  FC Minimal path for CI-book work.
- **Components** (`components/`) — copy-paste Bootstrap-class HTML for navbar,
  sidebar, card, buttons, status badges, tables, forms, nav-tabs, pagination,
  select2, flatpickr, login card.
- **Patterns** (`patterns/`) — the four page shapes: app-shell, list page,
  create/edit form, login page.
- **Adapters** (`adapters/`) — drop-in guides: `web/` (Bootstrap CDN order —
  the one to use for "make it look like the Supply Chain app"), `html-slides/`,
  `pptx/` (untouched by this extraction — see note below).
- **Reference** (`reference/sc-qas-extracted/`) — the raw evidence (site.css +
  layout/select2/flatpickr/table CSS) every token and component claim traces
  back to. If you doubt a value, check here first.
- **Examples** (`examples/app-shell.html`) — a self-contained page (tokens.css
  + CDN only, no build step) showing the navbar + sidebar + a status-badge table.
- **Assets** (`assets/`) — logos + FC Minimal font files (opt-in, CI-book path only).

## Two systems live in this repo — pick the right one

| | **Live app system (default)** | **CI-book legacy system** |
|---|---|---|
| Use when | Building anything meant to look like the Supply Chain app, or any internal Bootstrap admin tool | Marketing / investor / brand-forward surfaces that intentionally follow the official CI book + glassmorphism aesthetic |
| Tokens | `tokens/tokens.css` + `tokens/tokens.json` | `tokens/brand-ci-legacy.css` |
| Typography | Bootstrap's system-font stack (no webfont) | `typography/fonts.css` (FC Minimal) |
| Components | `components/COMPONENTS.md` | archived — see git history / `brand-ci-legacy.css` comments |
| Colors | `--cman-green` #1a472a, `--cman-teal` #2d6a4f | `--cman-forest` #00522C, `--cman-blue` #3C60A5, `--cman-amber` #745021 |

Don't mix the two token files on the same page — their `--cman-*` variable
names overlap but mean different things (e.g. `--cman-green` only exists in
the live-app system).

## Brand colors (live-app system — quick ref)

| Role | Token | HEX |
|---|---|---|
| Primary brand | `--cman-green` | `#1a472a` |
| Hover / focus | `--cman-teal` | `#2d6a4f` |
| Declared but NOT rendered (dead `.sidebar` selector) | `--cman-light` | `#f0f7f4` |
| Declared, unused anywhere | `--cman-lighter` | `#f8fdf9` |
| Real sidebar hover wash | `--cman-surface-50` (alias `--cman-neutral-50`) | `#f8f9fa` |
| Status badges (10 states) | `--cman-status-*` | see `components/COMPONENTS.md` § Status badges |

`--cman-light` / `--cman-lighter` are copied verbatim from the app's own
`:root` block, but the only CSS rule that consumes `--cman-light`
(`.sidebar .nav-link`) matches zero elements — no page carries a bare
`class="sidebar"` (the real sidebar is `<nav id="sidebar">`). See
`tokens/tokens.css` for the full explanation.

## File structure

```
tokens/
  tokens.json              ← authoritative machine-readable tokens (live-app system)
  tokens.css                ← CSS custom properties, mirrors tokens.json
  tokens.pptx.json          ← PptxGenJS mirror (CI-book system — untouched)
  tailwind.preset.js        ← Tailwind preset (live-app system)
  brand-ci-legacy.css       ← outgoing CI-book palette, preserved verbatim
typography/
  TYPOGRAPHY.md             ← live-app font truth + FC Minimal opt-in path
  fonts.css                 ← FC Minimal @font-face (opt-in, CI-book system only)
components/
  COMPONENTS.md             ← navbar, sidebar, card, badges, tables, forms, etc.
patterns/
  PATTERNS.md               ← app-shell, list page, create/edit form, login page
adapters/
  web/WEB.md                ← Bootstrap 5.3.2 drop-in (start here for new apps)
  html-slides/HTML_SLIDES.md  ← untouched by this extraction (CI-book system)
  pptx/PPTX.md                ← untouched by this extraction (CI-book system)
reference/
  sc-qas-extracted/          ← raw evidence: site.css, layout/select2/flatpickr/table CSS + README
examples/
  app-shell.html             ← working demo, self-contained (tokens.css + CDN only)
  hero.html                  ← older demo of the CI-book/glassmorphism system
assets/
  logo/, characters/, fonts/ ← unchanged
```

## Known repo defect — STALE nested duplicate folders (do not read)

`tokens/tokens/`, `typography/typography/`, `components/components/`,
`patterns/patterns/`, `adapters/adapters/`, `assets/assets/`, and
`examples/examples/` (7 folders total) are leftover copies of the **outgoing
CI-book system**, from before this repo was rebuilt around the live-app
extraction. This is no longer a harmless leftover — it's a second, wrong
design system sitting at colliding paths:

- `tokens/tokens/tokens.css` still declares the **OLD** `--cman-forest:
  #00522C` palette, not the live-app `--cman-green` system.
- `adapters/adapters/web/WEB.md` is still the **old Next.js/Tailwind adapter**
  for the CI-book system, not the Bootstrap drop-in in `adapters/web/WEB.md`.
- The same pattern holds for the other 5 (typography/, components/, patterns/,
  assets/, examples/) — each nested folder is a stale pre-rebuild copy.

**Do not read from any of these 7 nested folders** — always use the top-level
folder of the same name. Every current file in this system was written to the
top-level folders only.

Cleanup (run only after explicit approval from jakkaritw — NOT run as part of
this pass):

```bash
rm -rf tokens/tokens typography/typography components/components patterns/patterns adapters/adapters assets/assets examples/examples
```

## Updating this system

- **Live-app tokens**: `tokens/tokens.json` is authoritative — edit it first,
  then mirror to `tokens/tokens.css` and `tokens/tailwind.preset.js` by hand.
  Out-of-sync token files are the #1 silent source of drift. After editing any
  of the three, run the drift guard:

  ```bash
  python tools/check-tokens.py
  ```

  It looks up each logical token (colors, layout, font size/weight/tracking,
  radius, shadow, border, focus) BY KEY in whichever of the three files
  define it, and fails if they disagree — so a name↔value swap (e.g. two
  colors trading hex values) is caught, not just a missing/extra value. It
  also checks that every `var(--cman-*)` used in the live-app docs actually
  resolves to a `tokens/tokens.css` definition, including calls that also
  supply a fallback value (e.g. `var(--cman-green, #000)`). Exits non-zero
  with a readable diff on drift (never a raw traceback, even if a
  tokens.json key is renamed) — run it before committing any token change.
- **CI-book tokens**: `tokens/brand-ci-legacy.css` is frozen/archival — don't
  add new tokens to it; if the CI-book system needs new tokens, that's a
  separate decision from this extraction.
- Adding a component or pattern? Append to the relevant `.md` with a working
  snippet — don't create a sub-file unless it's genuinely large (>500 lines).
- If you re-extract from the live app later (design refresh, new page type),
  update `reference/sc-qas-extracted/` first, then propagate to tokens →
  components → patterns, in that order — the reference folder is the
  provenance record everything else must trace back to.
