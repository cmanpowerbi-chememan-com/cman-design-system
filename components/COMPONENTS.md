# Chememan Components

Every snippet below is reconstructed from the LIVE Chememan Budget
Management web app (`c:\04.budget_management_web\frontend\src\styles\global.css`),
jakkaritw's approved 2026-08-15 theme. Class names match the app's own
CSS 1:1 so a snippet here can be copy-pasted straight into that codebase
or ported into a new project unchanged.

Do not hand-roll colors/sizes/radii — reach into `tokens/tokens.css`
(`--cman-*` custom properties). Setup once per page:

```html
<link rel="stylesheet" href="tokens/tokens.css" />
```

No framework CDN is required — the source app is plain React + CSS, not
Bootstrap. See `adapters/web/WEB.md` if your project also wants Tailwind
utility classes over these same tokens.

---

## Nav (shell)

Sticky top bar painted directly on the shell color — the ONE place in the
whole app where on-shell text tokens are load-bearing (no card ancestor).

```html
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-logo-text">
      <span class="name">Chememan</span>
      <span class="sub">Budget Management</span>
    </div>
    <button class="icon-btn" aria-label="Toggle theme">🌙</button>
  </div>
</nav>
```

```css
.nav {
  position: sticky; top: 0; z-index: 100;
  background: var(--cman-shell);
  border-bottom: 1px solid var(--cman-line-on-shell); /* on-shell hairline — plain --cman-line vanishes on the shell */
}
.nav-inner { display: flex; align-items: center; gap: 18px; height: 64px; padding: 0 28px; }
.nav-logo-text .name { font-weight: var(--cman-fw-semibold); font-size: 14.5px; color: var(--cman-ink-on-shell); }
.nav-logo-text .sub { font-size: 10.5px; color: var(--cman-ink-on-shell-2); font-weight: var(--cman-fw-medium); text-transform: uppercase; letter-spacing: var(--cman-ls-wider); }
.icon-btn {
  margin-left: auto; width: 36px; height: 36px; border-radius: var(--cman-r-base);
  border: 1px solid var(--cman-line); background: var(--cman-surface); cursor: pointer;
}
```

**Rule**: anything painted directly on `.nav`'s own `--cman-shell`
background (no card ancestor) must use the `-on-shell` token variants —
see the contrast rule in `CLAUDE.md`. `.icon-btn` itself is a light card
sitting ON the shell, so it uses the plain (non-shell) tokens internally.

---

## Buttons

```html
<button class="btn">Cancel</button>
<button class="btn btn-export">Export</button>
<button class="btn btn-sm btn-ghost">Reset columns</button>
```

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 10px 16px; border-radius: var(--cman-r-base);
  font-size: var(--cman-fs-md2); font-weight: var(--cman-fw-semibold); letter-spacing: var(--cman-ls-tight-3);
  border: 1px solid var(--cman-line); background: var(--cman-surface); color: var(--cman-ink); cursor: pointer;
}
.btn:hover { border-color: var(--cman-ink); background: var(--cman-surface-inset); }
.btn:disabled { opacity: .55; cursor: not-allowed; }
.btn-sm { padding: 7px 12px; font-size: var(--cman-fs-base-sm); }

/* Primary/brand action — solid accent fill, white label */
.btn-export { background: var(--cman-green); color: #fff; border-color: var(--cman-green); }
.btn-export:hover { background: color-mix(in oklab, var(--cman-green) 78%, black); border-color: color-mix(in oklab, var(--cman-green) 78%, black); }

/* Quiet variant for a container with NO card ancestor (e.g. sitting
   directly on the shell alongside a heading) — uses on-shell tokens. */
.btn-ghost { background: transparent; border-color: transparent; color: var(--cman-ink-on-shell-2); }
.btn-ghost:hover { color: var(--cman-ink-on-shell); background: transparent; }
```

**Rule**: `.btn` is the default (neutral card-colored) button. `.btn-export`
is the ONLY solid-fill brand button — reserve it for the primary action per
screen. `.btn-ghost` is for shell-hosted secondary actions only (it uses
on-shell tokens — do not use it inside a card).

---

## Card + card panel

```html
<div class="table-panel">
  <div class="table-wrap">
    <table class="data-table">…</table>
  </div>
</div>
```

```css
.table-panel {
  background: var(--cman-surface);
  border: 1px solid var(--cman-line);
  border-radius: var(--cman-r-base);
  overflow: hidden; /* keeps border-radius from clipping the sticky header separately */
}
```

A generic content card follows the same recipe — `background: var(--cman-surface)`,
`border: 1px solid var(--cman-line)`, `border-radius: var(--cman-r-base)`.
Nested/inset panels (search inputs, dashed add-row forms, subtotal rows)
use `--cman-surface-inset` instead of `--cman-surface` for their own
background, so they read as one step "sunken" from the card around them.

---

## Status legend + status cell

Three reference layers — SAP/Approved (read-only prior-year actuals) and
Pending (the current, editable year). Swatch + text together, never color
alone.

```html
<div class="legend">
  <span class="legend-item"><span class="legend-dot sap"></span>SAP</span>
  <span class="legend-item"><span class="legend-dot approved"></span>Approved</span>
  <span class="legend-item"><span class="legend-dot pending"></span>Pending</span>
</div>
```

```css
.legend { display: flex; align-items: center; gap: 20px; font-size: var(--cman-fs-2xl); color: var(--cman-ink-3); font-family: var(--cman-font-mono); letter-spacing: var(--cman-ls-wide); }
.legend-dot { width: 11px; height: 11px; border-radius: var(--cman-r-circle); }
.legend-dot.sap { background: var(--cman-status-sap); }
.legend-dot.approved { background: var(--cman-status-approved); }
.legend-dot.pending { background: var(--cman-status-pending); }

.status-cell { font-family: var(--cman-font-mono); font-size: var(--cman-fs-xs2); font-weight: var(--cman-fw-semibold); letter-spacing: var(--cman-ls-wider); text-transform: uppercase; color: var(--cman-ink-3); }
.status-cell.sap { color: var(--cman-status-sap); }
.status-cell.approved { color: var(--cman-status-approved); }
.status-cell.pending { color: var(--cman-status-pending); }
```

**Rule**: never rely on the color alone — pair every status swatch/cell
with its text label (accessibility: color-blind users, print/grayscale).

---

## GL-group chip

Solid-color pill for the handful of "special" GL groups that need to stand
out in an otherwise neutral table.

```html
<span class="gl-chip special-gl-group">Travel</span>
```

```css
.gl-chip {
  --chip-bg: #888; --chip-fg: #fff;
  background: var(--chip-bg); color: var(--chip-fg);
  padding: 5px 11px; border-radius: var(--cman-r-xs);
  border: 1px solid rgba(255, 255, 255, .25);
  font-weight: var(--cman-fw-bold); font-size: var(--cman-fs-sm2);
  display: inline-block; letter-spacing: var(--cman-ls-tight-3);
}
```

**Rule**: this is the one place saturated, non-token color is allowed in
this otherwise neutral system — reserve it for the handful of GL groups
that genuinely need a distinct hue; don't extend it to general-purpose UI.

---

## Badges / count pills

```html
<span class="role-badge admin">Admin</span>
<span class="v3-count">12</span>
```

```css
.role-badge { font-family: var(--cman-font-mono); font-size: var(--cman-fs-3xs); font-weight: var(--cman-fw-bold); letter-spacing: var(--cman-ls-wider); padding: 2px 7px; border-radius: var(--cman-r-pill); }
.role-badge.admin { background: color-mix(in oklab, var(--cman-accent-text) 16%, transparent); color: var(--cman-accent-text); border: 1px solid color-mix(in oklab, var(--cman-accent-text) 42%, var(--cman-line)); }
.role-badge.user  { background: color-mix(in oklab, var(--cman-teal) 16%, transparent);        color: var(--cman-teal);        border: 1px solid color-mix(in oklab, var(--cman-teal) 42%, var(--cman-line)); }

.v3-count {
  font-family: var(--cman-font-mono); font-size: var(--cman-fs-2xs); font-weight: var(--cman-fw-extrabold);
  color: var(--cman-teal); background: color-mix(in oklab, var(--cman-teal) 15%, transparent);
  border: 1px solid color-mix(in oklab, var(--cman-teal) 42%, var(--cman-line)); border-radius: var(--cman-r-pill);
  min-width: 17px; height: 17px; padding: 0 5px; display: inline-flex; align-items: center; justify-content: center;
}
```

**Rule**: a tint (`color-mix` background/border) and its own text always
mix from the SAME base token — never pair a tint mixed from one token
with text colored from a different one.

---

## ฝ่าย (department) picker

```html
<div class="dept-picker">
  <button class="dept-picker-trigger">สายงาน A › ฝ่ายบัญชี</button>
  <div class="dept-picker-panel">
    <input class="dept-picker-search" placeholder="ค้นหา…" />
    <div class="dept-picker-list">
      <div class="dept-picker-group-head">สายงาน A <span class="dept-picker-badge">3</span></div>
      <button class="dept-picker-row selected">ฝ่ายบัญชี</button>
    </div>
  </div>
</div>
```

```css
.dept-picker-trigger { min-width: 220px; text-align: left; padding: 9px 14px; background: var(--cman-surface); border: 1px solid var(--cman-line); border-radius: var(--cman-r-base); font-size: var(--cman-fs-md2); font-weight: var(--cman-fw-semibold); cursor: pointer; }
.dept-picker-panel { position: absolute; z-index: 50; min-width: 320px; max-height: 360px; background: var(--cman-surface); border: 1px solid var(--cman-line); border-radius: var(--cman-r-base); box-shadow: 0 16px 32px -10px rgba(11, 26, 18, .18); }
.dept-picker-search { margin: 10px; padding: 8px 10px; border: 1px solid var(--cman-line); border-radius: var(--cman-r-base); background: var(--cman-surface-inset); color: var(--cman-ink); font-size: var(--cman-fs-md2); }
.dept-picker-row { width: 100%; padding: 8px 10px; border: none; border-radius: var(--cman-r-base); background: transparent; color: var(--cman-ink); font-size: var(--cman-fs-md2); text-align: left; cursor: pointer; }
.dept-picker-row:hover, .dept-picker-row.selected { background: var(--cman-surface-inset); }
```

---

## Loading / empty / error states

```html
<div class="grid-loading">Loading…</div>
<div class="grid-empty">No rows to show.</div>
<div class="grid-error">Something went wrong. <button class="btn btn-sm">Retry</button></div>
```

```css
.grid-loading, .grid-empty {
  padding: 48px; text-align: center; font-family: var(--cman-font-mono);
  font-size: var(--cman-fs-md2); color: var(--cman-ink-3);
  background: var(--cman-surface); border: 1px dashed var(--cman-line); border-radius: var(--cman-r-base);
}
.grid-error {
  display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 14px 16px;
  background: color-mix(in oklab, var(--cman-accent-text) 8%, var(--cman-surface));
  border: 1px solid color-mix(in oklab, var(--cman-accent-text) 35%, var(--cman-line));
  border-radius: var(--cman-r-base); color: var(--cman-accent-text); font-size: var(--cman-fs-lg);
}
```

**Rule**: every empty/error state is an opaque card of its own — never
rely on the shell peeking through, and always pair the error tint's
background/border/text from the SAME `--cman-accent-text` token (see the
GL-chip/badge tinting rule above).

---

## Component checklist (quality gate)

- [ ] No hardcoded hex/px — reach into `tokens/tokens.css`.
- [ ] Anything with NO card ancestor (nav, a shell-hosted heading/button)
      uses the `-on-shell` token variants, never the plain ink/accent ones.
- [ ] A tint (`color-mix` bg/border) and its paired text always mix from
      the SAME base token.
- [ ] Status is never color-alone — always swatch + text label together.
- [ ] `.btn-export` (solid brand fill) is reserved for ONE primary action
      per screen — everything else is the neutral `.btn`.
- [ ] No custom webfont — see `typography/TYPOGRAPHY.md`.
