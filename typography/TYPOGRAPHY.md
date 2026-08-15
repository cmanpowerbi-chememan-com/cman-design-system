# Chememan Typography — Live App Truth

**Verified finding (2026-08-15, extracted from https://sc-qas.chememan.com — QAS/staging):
the app declares NO `font-family` anywhere.** Zero occurrences across every dumped page
and the one custom stylesheet (`site.css`). Five files were dumped while
authenticated (`Home_Index.html`, `Po.html`, `Po_Create.html`, `Po_Index.html`,
`theme_dump/root.html` — the AUTHENTICATED root, i.e. the dashboard you land
on when `/` is requested with a logged-in session), but only **3 of those 5
are actually unique** — `Home_Index.html` is byte-identical to
`theme_dump/root.html`, and `Po.html` is byte-identical to `Po_Index.html`.
Separately, the anonymous login page — the page an unauthenticated visitor to
`/` actually sees — was also captured (`root.html` at the top of the evidence
folder, a different, 3,671-byte file; see
`reference/sc-qas-extracted/README.md` for the full provenance table). Adding
that in, this evidence set documents **4 unique pages total**: login,
dashboard, PO list, PO create. This is not an oversight to "fix" — it is the
current, shipped state, and this document treats it as the default for
anything meant to look like the Supply Chain app.

Raw evidence: `../reference/sc-qas-extracted/` + `theme_report.txt` ("FONT-FAMILY (0 distinct)").

## What actually renders

Because no font-family is declared, the browser falls back to **Bootstrap 5.3.2's own
default system-font stack**, which Bootstrap sets on `<body>`:

```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue",
  "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji",
  "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
```

Token: `--cman-font` in `tokens/tokens.css`.

- **Root size**: `1rem` = 16px, **line-height**: `1.5` — both Bootstrap defaults, never
  overridden anywhere in the app.
- **Thai glyphs** fall through to whatever the OS supplies for Thai in that stack —
  on Windows that's typically **Leelawadee UI**, since none of the declared families
  (Segoe UI, Roboto, Helvetica Neue, Noto Sans, Arial) carry native Thai glyphs.
  This is worth knowing if a design review flags "the Thai looks different from the
  English" — that's expected, not a bug, given the app never opted into a Thai-aware
  webfont.
- To render pixel-identical to the live app, **do not add `@font-face` at all** —
  just load Bootstrap 5.3.2 and let its default stack apply.

## Type scale — every size actually used

All values are `rem`, listed smallest to largest, with the exact spot in the app
that uses each one. Sizes come from the shared layout `<style>` blocks + `site.css`
+ the `Po_Create.html` page-specific block — see `theme_report.txt` for the full
frequency count.

| Token | Size | Used for |
|---|---|---|
| `--cman-fs-2xs` | `.65rem` | `.sidebar-section-label` |
| `--cman-fs-xs` | `.72rem` | login sub-brand text |
| `--cman-fs-sm` | `.75rem` | `.badge`, flatpickr weekday header |
| `--cman-fs-sm2` | `.78rem` | `.sidebar-brand`, flatpickr day cell |
| `--cman-fs-base-sm` | `.8rem` | `.table thead th` |
| `--cman-fs-md` | `.82rem` | `.form-label`, select2 (all parts), flatpickr calendar, items-table cells |
| `--cman-fs-md2` | `.85rem` | `.nav-tabs .nav-link`, `.section-title` (Po_Create) |
| `--cman-fs-lg` | `.875rem` | `.form-control` / `.form-select`, `.table td` |
| `--cman-fs-lg2` | `.88rem` | flatpickr current-month label (real). Also declared on `.sidebar .nav-link` in site.css, but that selector matches no element in the app (no bare `class="sidebar"` exists — the real sidebar is `<nav id="sidebar">`) — see `--cman-light` in `tokens/tokens.css` for the same dead-selector finding. |
| `--cman-fs-xl` | `.9rem` | `.card-header`, `.nav-icon` / `.nav-label`, navbar username |
| `--cman-fs-xl2` | `.95rem` | navbar brand ("CHEMEMAN \| Supply Chain") |
| `--cman-fs-2xl` | `1rem` | login brand |
| `--cman-fs-3xl` | `1.1rem` | collapsed-sidebar nav icon |
| `--cman-fs-h5` | `1.25rem` | unstyled `<h5>` — e.g. the "Sign In" login heading, modal titles (7 occurrences, no size override) |
| `--cman-fs-h4` | `1.5rem` | unstyled `<h4>` — e.g. list-page headers like "PO List" (5 occurrences, no size override) |

There is no display/hero scale — this is a dense admin app, not a marketing page.
**Correction (2026-08-15): an earlier version of this doc claimed the largest text
on any authenticated screen was `1.1rem` — that was false.** The dumps contain 5
`<h4>` and 7 `<h5>` tags with no size override, so they render at Bootstrap
5.3.2's own default heading sizes — `1.5rem` and `1.25rem` respectively — both
bigger than `1.1rem`. `patterns/PATTERNS.md` §2 and §3 already use exactly these
tags for page/section headings; `--cman-fs-h4`/`--cman-fs-h5` above just give
those inherited sizes a name.

## Weights

Only **3 weights** are used anywhere in the app:

| Weight | Token | Used for |
|---|---|---|
| 400 (regular) | `--cman-fw-regular` | body text, table cell values |
| 600 (semibold) | `--cman-fw-semibold` | active sidebar nav-link, card-header, form-label, buttons, badges, active nav-tabs |
| 700 (bold) | `--cman-fw-bold` | table `thead th`, sidebar brand, sidebar-section-label |

Never use 300/500/800/900 — they don't exist anywhere in the reference app.

## Letter-spacing

| Token | Value | Used for |
|---|---|---|
| `--cman-ls-badge` | `.02em` | `.badge` |
| `--cman-ls-tablehead` | `.04em` | `.table thead th` |
| `--cman-ls-sidebarbrand` | `.04em` | `.sidebar-brand` |
| `--cman-ls-sectiontitle` | `.06em` | `.section-title` (Po_Create) |
| `--cman-ls-loginbrand` | `.08em` | login page brand text |
| `--cman-ls-sidebarsection` | `.1em` | `.sidebar-section-label` |
| `--cman-ls-loginsub` | `.12em` | login page sub-brand |

## If you want FC Minimal instead

The **prior** design-system iteration (CI-book palette + glassmorphism aesthetic,
now archived) specified **FC Minimal** as the single brand typeface across 18
styles. That font is still shipped in `../assets/fonts/` and its `@font-face`
declarations still live in `typography/fonts.css` — it is now **opt-in**, not the
default, because the live Supply Chain app does not load it.

Use FC Minimal when building marketing / investor / brand-forward surfaces that
intentionally follow the CI book instead of the Bootstrap admin-app look — pair
it with `tokens/brand-ci-legacy.css` (the matching color system), not
`tokens/tokens.css`.

```html
<link rel="stylesheet" href="design-system/chememan/typography/fonts.css" />
<link rel="stylesheet" href="design-system/chememan/tokens/brand-ci-legacy.css" />
```

See `fonts.css`'s header comment for the full weight list and the `.cman-display`
/ `.cman-h1`…`.cman-eyebrow` utility classes that ship with it.
