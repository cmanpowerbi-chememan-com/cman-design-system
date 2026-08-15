# Chememan Patterns

Higher-order page layouts assembled from `components/COMPONENTS.md`
primitives. Source: jakkaritw's approved 2026-08-15 theme for the Budget
Management web app. These are the page shapes that app actually uses —
start here, don't redesign the wheel per screen.

---

## 1. App shell (flagship pattern — every page uses this)

Sticky nav painted on the shell + a centered content column. The nav is
the ONE place on-shell text tokens are load-bearing; everything below it
renders on cards.

```
┌──────────────────────────────────────────────────────────┐
│ .nav (sticky, shell-green background, white text)         │
├──────────────────────────────────────────────────────────┤
│ .wrap (max-width 1980px, centered)                         │
│   .page-head (title + user bar)                            │
│   page content — cards, tables, forms                      │
└──────────────────────────────────────────────────────────┘
```

```html
<body>
  <nav class="nav"><!-- components/COMPONENTS.md § Nav --></nav>
  <div class="wrap">
    <div class="page-head">
      <h1 class="page-title glassy">OPEX <em>Management.</em></h1>
      <div class="user-bar v3"><!-- identity + ฝ่าย picker + CC/GL counts --></div>
    </div>
    <!-- one of §2/§3 below -->
  </div>
</body>
```

```css
.wrap { max-width: 1980px; margin: 0 auto; padding: 0 28px; }
.page-head { padding: 32px 0 22px; display: flex; flex-direction: column; gap: 16px; }
.page-title {
  font-family: var(--cman-font-serif); font-size: var(--cman-fs-display); line-height: var(--cman-lh-tight);
  letter-spacing: var(--cman-ls-tight); font-weight: var(--cman-fw-regular);
}
```

**When to break the mold**: never. Every screen in the source app uses
this exact shell — the only variation is what fills `.wrap` below the
page head.

**On-shell exception**: `.page-title` sits directly in `.page-head`, which
sits directly in `.wrap` — no card ancestor, straight on the body
background. In the real app the body background is also the shell color
(`--cman-shell`), so `.page-title` uses `--cman-accent-on-shell` (white),
not the card-context `--cman-accent-text`. See `components/COMPONENTS.md`
§ Nav for the same on-shell reasoning.

See `examples/app-shell.html` for a full working copy.

---

## 2. Budget grid page (the primary workflow)

Toolbar (year selector + ฝ่าย picker + add-transaction) → status legend →
admin-only reference strip → two side-by-side data tables (COST / SGA).
This is the shape of the main budget screen.

```html
<div class="budget-grid">
  <div class="grid-toolbar">
    <select class="year-select"><option>2026</option></select>
    <div class="dept-picker"><!-- components/COMPONENTS.md § ฝ่าย picker --></div>
    <div class="add-txn-trigger"><button class="btn btn-export">+ เพิ่ม Transaction</button></div>
  </div>

  <div class="legend"><!-- components/COMPONENTS.md § Status legend --></div>

  <div class="admin-zone"><!-- admin-only: read-only Approved-layer note --></div>

  <div class="side-section">
    <div class="side-heading-row">
      <h2 class="side-heading">Cost</h2>
      <button class="btn btn-sm btn-ghost">Reset columns</button>
    </div>
    <div class="table-panel"><!-- components/COMPONENTS.md § Card + card panel --></div>
  </div>

  <div class="side-section">
    <div class="side-heading-row">
      <h2 class="side-heading">SG&amp;A</h2>
      <button class="btn btn-sm btn-ghost">Reset columns</button>
    </div>
    <div class="table-panel">…</div>
  </div>
</div>
```

```css
.budget-grid { margin: 20px 0 60px; display: flex; flex-direction: column; gap: 16px; }
.grid-toolbar { display: flex; align-items: flex-start; gap: 12px; flex-wrap: wrap; padding: 14px 16px; background: var(--cman-surface); border: 1px solid var(--cman-line); border-radius: var(--cman-r-base); }
.side-section { margin-bottom: 28px; }
.side-heading-row { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 8px; }
.side-heading { font-family: var(--cman-font-serif); font-size: var(--cman-fs-3xl); font-weight: var(--cman-fw-medium); margin: 0; }
```

**Rules**:
- Toolbar always sits above the legend, which sits above the tables — in
  that order.
- `.side-heading-row` has NO card ancestor (only `.table-panel` below it
  is a card) — it renders directly on the page background, so
  `.side-heading` uses `--cman-ink-on-shell` if the page background is the
  shell color, or the plain `--cman-ink` if the page has been given a
  neutral (non-shell) background. Check what actually sits behind it
  before picking the token.
- COST and SGA are always shown side by side (or stacked on narrow
  viewports) — never merged into one table.

---

## 3. Modal / subform

Used for anything that needs focused input outside the main grid flow
(add/edit a detail row, a special-GL subform).

```html
<div class="modal-backdrop">
  <div class="modal">
    <h2 class="modal-title">Edit detail</h2>
    <!-- form fields -->
    <div class="add-txn-actions">
      <button class="btn">Cancel</button>
      <button class="btn btn-export">Save</button>
    </div>
  </div>
</div>
```

```css
.modal-backdrop { position: fixed; inset: 0; z-index: 500; display: flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, .35); }
.modal { background: var(--cman-surface); border-radius: var(--cman-r-base); padding: 20px 24px; max-width: 640px; width: 100%; }
.modal-title { font-family: var(--cman-font-serif); font-size: var(--cman-fs-4xl); font-weight: var(--cman-fw-regular); color: var(--cman-ink); }
```

**Rule**: `.modal-backdrop` sits ABOVE the sticky `.nav` (`z-index: 500` >
nav's `z-index: 100`) so it always covers the page, including a
fullscreen grid overlay.

---

## Pattern checklist

- [ ] Every page uses the §1 app shell — no page-specific nav variant.
- [ ] The budget grid always orders toolbar → legend → admin note →
      tables, never reshuffled.
- [ ] Anything with no card ancestor uses the on-shell token variant that
      matches what's actually behind it (check, don't assume).
- [ ] Modals sit above the sticky nav and any fullscreen overlay.
