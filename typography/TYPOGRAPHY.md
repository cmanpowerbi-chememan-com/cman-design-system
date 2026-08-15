# Chememan Typography

Source: jakkaritw's approved 2026-08-15 theme for the Budget Management web
app (`c:\04.budget_management_web\frontend\src\styles\global.css`). This
system ships **no custom webfont** — FC Minimal and its 36 font files were
retired with the 2026-08-15 rebuild of this repo. If a future request
genuinely needs a brand-forward typeface, that is a new decision to make
with jakkaritw, not something to revive from this repo's git history.

## What actually renders

```css
font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue",
  "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji",
  "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
```

Token: `--cman-font-sans` in `tokens/tokens.css`. `--cman-font-serif`
collapses to the same stack (the source app has no serif face — it's used
for the page-title/heading role, not a different typeface). Monospace role
(`--cman-font-mono`) is `SFMono-Regular, Menlo, Monaco, Consolas,
"Liberation Mono", "Courier New", monospace` — used for numeric/tabular
text (IDs, amounts, meta labels).

- **Root size**: `1rem` = 16px (browser default).
- **Body size**: `.875rem` = 14px — the app's actual body font-size
  (`--cman-fs-base`), one step down from the browser default.
- **Line-height**: `1.5` base (`--cman-lh-base`); `.98` for the display
  heading only (`--cman-lh-tight`, tighter leading at large sizes).
- **Thai glyphs** fall through to whatever the OS supplies for Thai in this
  stack — on Windows that's typically Leelawadee UI, since none of the
  declared families carry native Thai glyphs. Expected, not a bug.

## Type scale — every size actually used

All values come from `frontend/src/styles/global.css`, smallest to
largest. Do not add a size the app doesn't use.

| Token | Size | Used for |
|---|---|---|
| `--cman-fs-3xs` | `9px` | meta-tag, role-badge label |
| `--cman-fs-2xs` | `9.5px` | v3-count pill, group-head-row label |
| `--cman-fs-xs` | `10px` | col-filter label, action-btn caption |
| `--cman-fs-xs2` | `10.5px` | table thead th, admin-zone-note |
| `--cman-fs-sm` | `11px` | v3-email, dept-picker-cc-count |
| `--cman-fs-sm2` | `11.5px` | gl-chip, action-col label |
| `--cman-fs-base-sm` | `12px` | filter-chip, grid-error, grid-empty-row |
| `--cman-fs-md` | `12.5px` | data-table base size, status-cell |
| `--cman-fs-md2` | `13px` | `.btn`, dept-picker-trigger, add-txn select |
| `--cman-fs-lg` | `13.5px` | v3-name |
| `--cman-fs-lg2` | `14px` | month-col th-label — same size as body text |
| `--cman-fs-xl` | `14.5px` | nav-logo-text `.name`, admin-zone-title |
| `--cman-fs-xl2` | `15px` | icon-btn, user-avatar |
| `--cman-fs-2xl` | `16px` | legend, month-group-label |
| `--cman-fs-3xl` | `20px` | v3-division, side-heading |
| `--cman-fs-4xl` | `24px` | modal-title |
| `--cman-fs-display` | `clamp(34px, 4.9vw, 60px)` | `.page-title` hero — the ONE fluid/responsive size in the system |

There is no marketing/hero deck scale beyond `--cman-fs-display` — this is
a dense data-entry app, not a brochure site. The display size is reserved
for the page title only.

## Weights

Five weights are used across the app — do not use one outside this list.

| Weight | Token | Used for |
|---|---|---|
| 400 (regular) | `--cman-fw-regular` | `.page-title`, `.gl-combo-empty`, body copy |
| 500 (medium) | `--cman-fw-medium` | nav-logo `.sub`, side-heading, legend labels |
| 600 (semibold) | `--cman-fw-semibold` | `.btn`, `.v3-name`, active states |
| 700 (bold) | `--cman-fw-bold` | table headers, `.gl-chip`, admin-zone-title |
| 800 (extrabold) | `--cman-fw-extrabold` | `.v3-count`, `.v3-cc-pill .n`, count pills |

## Letter-spacing

A curated sample of the real letter-spacing values in `global.css`, not an
exhaustive list of every literal decimal used (the app has ~12 distinct
values; these 6 cover the meaningfully different tiers).

| Token | Value | Used for |
|---|---|---|
| `--cman-ls-tight` | `-.025em` | `.page-title` (display heading) |
| `--cman-ls-tight-2` | `-.01em` | `.v3-division`, `.v3-name` |
| `--cman-ls-tight-3` | `-.005em` | `.btn`, nav-logo-text `.name` |
| `--cman-ls-wide` | `.02em` | `.col-filter`, current-month th-label |
| `--cman-ls-wider` | `.04em` | `.meta-tag`, dept-picker-group-head |
| `--cman-ls-widest` | `.08em` | `.admin-zone-title` uppercase labels |

## Usage

```html
<link rel="stylesheet" href="tokens/tokens.css" />
<style>
  body { font-family: var(--cman-font-sans); font-size: var(--cman-fs-base); line-height: var(--cman-lh-base); }
  .page-title { font-family: var(--cman-font-serif); font-size: var(--cman-fs-display); line-height: var(--cman-lh-tight); letter-spacing: var(--cman-ls-tight); font-weight: var(--cman-fw-regular); }
</style>
```

No `@font-face` needed anywhere — the browser's own system-font stack
applies as soon as `--cman-font-sans` is referenced.
