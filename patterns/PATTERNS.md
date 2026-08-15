# Chememan Patterns — Live App Truth

Higher-order page layouts assembled from `components/COMPONENTS.md` primitives,
extracted from the LIVE Chememan Supply Chain app (https://sc-qas.chememan.com —
QAS/staging, 2026-08-15). These are the four page shapes every screen in the app
falls into — start here, don't redesign the wheel per screen.

---

## 1. App-shell (flagship pattern — every authenticated page uses this)

Fixed 44px navbar + full-height flex row (collapsible sidebar + independently
scrolling main content). The page itself never scrolls; the sidebar and main
content each scroll on their own.

```
┌──────────────────────────────────────────────────────────┐
│ navbar (44px, fixed, brand-green)                         │
├───────────────┬──────────────────────────────────────────┤
│ sidebar        │ #mainContent (flex:1, scrolls, #f8f9fa)  │
│ 240px / 64px   │                                           │
│ collapsible    │  page content here                       │
│ (own scroll)   │                                           │
└───────────────┴──────────────────────────────────────────┘
```

```html
<body>
  <!-- navbar — components/COMPONENTS.md § Navbar -->
  <nav class="navbar navbar-dark" style="background-color: var(--cman-green); height:44px; min-height:44px;">
    …
  </nav>

  <div id="wrapper">
    <!-- sidebar — components/COMPONENTS.md § Sidebar -->
    <nav id="sidebar">…</nav>

    <main id="mainContent">
      <!-- one of §2/§3/§4 below -->
    </main>
  </div>
</body>
```

```css
body { overflow: hidden; height: 100vh; }
html { height: 100%; }
#wrapper { display: flex; height: calc(100vh - var(--cman-navbar-height)); }
#mainContent { flex: 1; min-width: 0; padding: 1.5rem; background: var(--cman-surface-50); overflow-y: auto; overflow-x: hidden; }
```

**When to break the mold**: never, for an authenticated page. Every list, create,
edit, and dashboard screen in the reference app uses this exact shell — the only
variation is what goes inside `#mainContent`.

See `examples/app-shell.html` for a full working copy.

---

## 2. List page (index / table view)

Header row → filter card → data-table card with footer pagination. This is the
shape of `/Po`, `/Shipment`, and every other index screen.

```html
<div class="d-flex align-items-center mb-4">
  <div>
    <h4 class="mb-0 fw-bold text-dark"><i class="fas fa-file-invoice me-2 text-success"></i>PO List</h4>
    <small class="text-muted">Purchase orders synced from SAP</small>
  </div>
  <div class="ms-auto d-flex gap-2">
    <a href="/Po/SapSync" class="btn btn-success btn-sm"><i class="fab fa-sap me-1"></i>Reload SAP</a>
    <a href="/Po/Create" class="btn btn-cman btn-sm"><i class="fas fa-plus me-1"></i>Create PO</a>
  </div>
</div>

<!-- Filter card -->
<div class="card mb-3">
  <div class="card-body py-3">
    <form class="row g-2 align-items-end" method="get">
      <div class="col-md-3">
        <label class="form-label small mb-1">Customer</label>
        <select class="form-select form-select-sm select2-search">…</select>
      </div>
      <div class="col-md-2">
        <label class="form-label small mb-1">Status</label>
        <select class="form-select form-select-sm">
          <option value="">All Status</option>
          <option value="ACTIVE">Active</option>
          <option value="CLOSED">Closed</option>
        </select>
      </div>
      <div class="col-auto d-flex gap-1">
        <button type="submit" class="btn btn-cman btn-sm"><i class="fas fa-search me-1"></i>Search</button>
        <a href="?reset=True" class="btn btn-outline-secondary btn-sm"><i class="fas fa-times"></i></a>
      </div>
    </form>
  </div>
</div>

<!-- Data table card — components/COMPONENTS.md § Tables + § Pagination -->
<div class="card">
  <div class="card-body p-0">
    <div class="table-responsive"><table class="table table-hover mb-0 align-middle">…</table></div>
  </div>
  <div class="card-footer d-flex align-items-center justify-content-between">
    <small class="text-muted">Showing 1 - 20 of 120</small>
    <nav><ul class="pagination pagination-sm mb-0">…</ul></nav>
  </div>
</div>
```

**Rules**:
- Header row: page title (icon + `h4 fw-bold`) + one-line muted subtitle on the
  left, primary actions on the right (`.ms-auto`). Never more than 2 header actions.
- Filter card always sits directly above the table card, `mb-3` gap, same width.
  Filter fields are `form-select-sm` / `form-control-sm` in a `row g-2
  align-items-end` grid — Search (`.btn-cman`) + Reset (`.btn-outline-secondary`)
  as the last `col-auto`.
- Sortable column headers link back to the same URL with `sortBy`/`sortDir` query
  params — server-rendered sort, no client JS table library.
- Row click navigates to the detail view; the Actions cell stops propagation
  (see Tables in COMPONENTS.md).

---

## 3. Create / edit form page

Sticky section header inside the scroll area + one `.card` per logical section +
a dense `.items-table` for line items. This is the shape of `/Po/Create`.

```css
#mainContent { padding-top: 0 !important; }
#poStickyHeader {
  position: sticky; top: 0; z-index: 200;
  background: var(--cman-surface-50);
  margin: 0 -1.5rem 0; padding: .75rem 1.5rem;
  border-bottom: var(--cman-border-hairline);
  box-shadow: var(--cman-sh-sticky-header);
}
.section-title {
  font-size: var(--cman-fs-md2); font-weight: var(--cman-fw-bold);
  text-transform: uppercase; letter-spacing: var(--cman-ls-sectiontitle);
  color: var(--cman-green); padding: 6px 12px;
  background: var(--sidebar-active); border-left: 4px solid var(--cman-green);
  border-radius: var(--cman-r-xs); margin-bottom: 10px;
}
```

```html
<div id="poStickyHeader">
  <h5 class="mb-0 fw-bold">Create PO</h5>
  <div class="d-flex gap-2 ms-auto">
    <button class="btn btn-outline-secondary btn-sm">Cancel</button>
    <button class="btn btn-cman btn-sm">Save</button>
  </div>
</div>

<div class="card mb-3">
  <div class="card-body">
    <div class="section-title"><i class="fas fa-file-invoice me-2"></i>PO Header</div>
    <div class="row g-3">
      <div class="col-md-3">
        <label class="form-label">Customer</label>
        <select class="form-select select2-search">…</select>
      </div>
      <!-- more fields -->
    </div>
  </div>
</div>

<div class="card">
  <div class="card-body">
    <div class="section-title"><i class="fas fa-list me-2"></i>PO Items</div>
    <div class="items-table-wrap">
      <table class="table table-sm items-table">
        <thead><tr><th>Material</th><th class="text-end">Qty</th><th></th></tr></thead>
        <tbody>
          <tr>
            <td><input class="form-control" /></td>
            <td class="text-end"><input class="form-control text-end" /></td>
            <td><button class="btn btn-outline-secondary btn-picker"><i class="fas fa-times"></i></button></td>
          </tr>
        </tbody>
      </table>
    </div>
    <button class="btn btn-outline-secondary btn-sm mt-2"><i class="fas fa-plus me-1"></i>Add row</button>
  </div>
</div>
```

**Rules**:
- One `.section-title` bar (green-left-border, light-green fill) per logical
  group of fields — never a bare `<h5>` inside a card body.
- The action bar (Cancel/Save) sticks to the top of the scroll area
  (`position: sticky; z-index: 200`) so it's reachable on a long form without
  scrolling back up — reuse this for any form long enough to exceed one viewport.
- Line-item tables use the dense `.items-table` variant (4-6px cell padding,
  28px input height) — never the roomy list-page `.table` styling.

---

## 4. Login page

Full-viewport centered card over the brand gradient. **This WAS dumped**
— `root.html` (anonymous login), NOT the same file as `theme_dump/root.html`
used elsewhere in this system (the authenticated dashboard) — see
`reference/sc-qas-extracted/README.md` for the provenance of both. An earlier
version of this doc claimed the login page wasn't dumped and reconstructed a
guess; the markup below is copied structurally from the real dump. Full
component-level detail (rules, dead-CSS note) lives in
`components/COMPONENTS.md` § Login card — this section shows the page-level shape only.

```html
<body class="d-flex align-items-center justify-content-center" style="background: var(--cman-grad-login-bg); min-height:100vh;">
  <div class="w-100" style="max-width: 420px; padding: 1rem;">
    <div class="card shadow-lg border-0" style="border-radius: var(--cman-r-lg); overflow:hidden;">
      <div class="card-header text-center py-4" style="background-color: var(--cman-green);">
        <img src="/Content/logo-full.png" alt="Chememan Logo" style="height:52px; width:auto;">
        <div class="text-white fw-bold" style="font-size: var(--cman-fs-2xl); letter-spacing: var(--cman-ls-loginbrand);">CHEMEMAN</div>
        <small class="text-white opacity-75" style="font-size: var(--cman-fs-xs); letter-spacing: var(--cman-ls-loginsub);">SUPPLY CHAIN</small>
      </div>
      <div class="card-body p-4">
        <h5 class="mb-4 text-center text-muted">Sign In</h5>
        <form method="post"><!-- see COMPONENTS.md for the full form-field markup -->…</form>
      </div>
      <div class="card-footer text-center py-3 bg-light">
        <small class="text-muted">&copy; 2026 Chememan Public Company Limited</small>
      </div>
    </div>
  </div>
</body>
```

**Rules**: this is the **only** screen in the whole app where brand green covers
a full-viewport background (as a gradient, not a flat fill) — every other screen
keeps green confined to the navbar/card-header/badge scale. Don't reuse the
gradient background anywhere else. The card header itself is a **flat** fill,
not a gradient — see COMPONENTS.md for why `.login-card-header` (gradient) is
dead CSS.

---

## Pattern checklist

- [ ] Every authenticated page uses the §1 app-shell — no page-specific navbar/sidebar variant.
- [ ] List pages: header row -> filter card -> table card with footer pagination, in that order.
- [ ] Forms longer than one viewport get a sticky action header.
- [ ] Line-item tables use `.items-table` (dense), never the roomy list `.table`.
- [ ] Login is the only full-bleed brand-gradient screen.
