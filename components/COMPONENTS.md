# Chememan Components — Live App Truth

Every snippet below is copied or reconstructed from the LIVE Chememan Supply Chain
app (https://sc-qas.chememan.com — QAS/staging), extracted 2026-08-15. This is
**Bootstrap 5.3.2 + Font Awesome 6.5.0** markup — plain HTML/CSS classes, not
Tailwind. Raw evidence: `../reference/sc-qas-extracted/`.

Do not hand-roll colors/sizes/radii — reach into `tokens/tokens.css`
(`--cman-*` custom properties) or the Bootstrap classes shown here, which the
reference stylesheet `reference/sc-qas-extracted/site.css` already styles via
those same tokens.

Setup once per page (see `adapters/web/WEB.md` for the full drop-in order):

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
<link rel="stylesheet" href="tokens/tokens.css">
<link rel="stylesheet" href="reference/sc-qas-extracted/site.css">
```

---

## Navbar

Fixed top bar, 44px tall, brand left, user + logout right. Note the brand uses
a compact `<img>` + two-tone text (`CHEMEMAN` full-opacity, `| Supply Chain`
at 70% opacity) — swap the module name per app.

```html
<nav class="navbar navbar-dark" style="background-color: var(--cman-green); height:44px; min-height:44px;">
  <div class="container-fluid" style="padding-top:0; padding-bottom:0;">
    <a class="navbar-brand fw-bold mb-0 d-flex align-items-center gap-2 text-decoration-none text-white"
       href="/" style="padding-top:0; padding-bottom:0; cursor:pointer;">
      <img src="/Content/logo-icon.png" alt="Chememan Logo" style="height:28px; width:auto;">
      <span style="font-size: var(--cman-fs-xl2); line-height:1;">
        CHEMEMAN <span style="opacity:.7; font-weight:400;">| Supply Chain</span>
      </span>
    </a>
    <div class="d-flex align-items-center text-white gap-3">
      <span class="d-none d-sm-flex align-items-center gap-2">
        <i class="fas fa-user-circle"></i>
        <span style="font-size: var(--cman-fs-xl);">Demo User</span>
      </span>
      <a href="/Account/Logout" class="btn btn-outline-light btn-sm">
        <i class="fas fa-sign-out-alt me-1"></i>Logout
      </a>
    </div>
  </div>
</nav>
```

**Rules**: height is fixed at 44px (`--cman-navbar-height`), never grows with content.
Logo is 28px tall. Only two actions live here — user identity and logout; put
everything else in the sidebar.

---

## Sidebar (expanded + collapsed)

240px expanded, 64px collapsed (`--sidebar-width` / `--sidebar-collapsed-width`),
state persisted in `localStorage['sidebarCollapsed']`. White background,
grouped nav with section labels + dividers, active item = light-green fill +
3px left border.

```html
<div id="wrapper">
  <nav id="sidebar">
    <div class="sidebar-header">
      <span class="sidebar-brand">Navigation</span>
      <button id="sidebarToggle" title="Toggle menu">
        <i class="fas fa-chevron-left" id="toggleIcon"></i>
      </button>
    </div>

    <ul class="nav flex-column">
      <li class="nav-item">
        <a class="nav-link active" href="/" data-bs-toggle="tooltip" data-bs-placement="right" title="Dashboard">
          <i class="fas fa-tachometer-alt nav-icon"></i>
          <span class="nav-label">Dashboard</span>
        </a>
      </li>

      <li><div class="sidebar-divider"></div></li>
      <li><div class="sidebar-section-label">Shipment</div></li>
      <li class="nav-item">
        <a class="nav-link" href="/Shipment" data-bs-toggle="tooltip" data-bs-placement="right" title="Shipment List">
          <i class="fas fa-list nav-icon"></i>
          <span class="nav-label">Shipment List</span>
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Shipment/Create" data-bs-toggle="tooltip" data-bs-placement="right" title="Create Shipment">
          <i class="fas fa-plus-circle nav-icon"></i>
          <span class="nav-label">Create Shipment</span>
        </a>
      </li>
    </ul>
  </nav>

  <main id="mainContent">
    <!-- page content -->
  </main>
</div>
```

**Toggle script** (vanilla JS, persists to `localStorage`):

```html
<script>
(function () {
  var STORAGE_KEY = 'sidebarCollapsed';
  var body = document.body;
  var toggleBtn = document.getElementById('sidebarToggle');
  var toggleIcon = document.getElementById('toggleIcon');

  function setCollapsed(collapsed) {
    body.classList.toggle('sidebar-collapsed', collapsed);
    toggleIcon.className = collapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left';
    localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0');
  }

  setCollapsed(localStorage.getItem(STORAGE_KEY) === '1'); // restore on load
  toggleBtn.addEventListener('click', function () {
    setCollapsed(!body.classList.contains('sidebar-collapsed'));
  });
})();
</script>
```

**Rules**:
- Section labels (`.sidebar-section-label`) are `.65rem`, bold, `.1em` tracking,
  uppercase, muted gray — one per nav group, never per item.
- Active item gets `var(--sidebar-active)` background + `var(--sidebar-active-border)`
  3px left border + weight 600. Hover (non-active) gets `var(--cman-surface-50)`.
  bg with no border shift.
- Collapsed mode (`body.sidebar-collapsed`): sidebar shrinks to 64px, labels and
  section headers hide (opacity 0), nav-icons center at `1.1rem`, active item
  keeps its identity via an **inset** left border instead of a real border (since
  there's no room to shift layout: `inset 3px 0 0 var(--sidebar-active-border)`).
  Add `data-bs-toggle="tooltip"` to every nav-link so collapsed icons still show
  their label on hover.
- The whole app shell is `#wrapper { display:flex; height: calc(100vh - 44px) }`
  under a `body { overflow:hidden; height:100vh }` — the sidebar and main content
  each scroll independently, the page itself never scrolls. See
  `patterns/PATTERNS.md` for the full shell pattern.

---

## Card + card-header

```html
<div class="card">
  <div class="card-header">
    <i class="fas fa-file-invoice me-2"></i>PO Header
  </div>
  <div class="card-body">
    <!-- content -->
  </div>
</div>
```

**Rules**: `border-radius: 8px` (top corners on the header too), `1px solid rgba(0,0,0,.08)`
border, soft shadow `0 1px 6px rgba(0,0,0,.07)`. Header is filled solid `var(--cman-green)`
with white text, weight 600, `.9rem` — this is the ONE place forest green appears as a
large fill; body stays white/neutral. The `min-height: 52px` bump on `.card-header` is
**dashboard-page-only** (`Home_Index.html` + `theme_dump/root.html` — the
authenticated dashboard, NOT the anonymous login page below) — it comes from a
page-specific override in `table-overrides.css`, not the shared card rule, so don't
assume every card-header is 52px tall on list/form pages.

A card can drop `card-body` padding for a full-bleed table:
```html
<div class="card">
  <div class="card-body p-0">
    <div class="table-responsive"><table class="table table-hover mb-0 align-middle">…</table></div>
  </div>
  <div class="card-footer d-flex align-items-center justify-content-between">
    <small class="text-muted">Showing 1 - 20 of 120</small>
    <!-- pagination, see below -->
  </div>
</div>
```

---

## Buttons

```html
<!-- Primary brand action -->
<button class="btn btn-cman btn-sm"><i class="fas fa-plus me-1"></i>New Shipment</button>

<!-- On a dark surface (navbar) -->
<a href="/Account/Logout" class="btn btn-outline-light btn-sm">
  <i class="fas fa-sign-out-alt me-1"></i>Logout
</a>

<!-- Secondary row action (table edit icon) -->
<a href="/Po/Edit/1" class="btn btn-sm btn-outline-primary" title="Edit"><i class="fas fa-edit"></i></a>

<!-- Neutral / reset -->
<a href="/Po?reset=True" class="btn btn-outline-secondary btn-sm"><i class="fas fa-times"></i></a>

<!-- Bootstrap semantic (integration action) -->
<a href="/Po/SapSync" class="btn btn-success btn-sm"><i class="fab fa-sap me-1"></i>Reload SAP</a>
```

`.btn-cman` (from `site.css`, styled with tokens):
```css
.btn-cman { background-color: var(--cman-green); color: #fff; border: none; }
.btn-cman:hover, .btn-cman:focus {
  background-color: var(--cman-teal);
  color: #fff;
  box-shadow: var(--cman-sh-btn-cman-hover);
}
```

**Rules**: `.btn-cman` is the only branded button class; everything else is stock
Bootstrap (`btn-outline-primary`, `btn-outline-secondary`, `btn-success`,
`btn-outline-light` on dark surfaces). Size is almost always `btn-sm` in this
dense admin UI — full-size `btn` is rare.

---

## Status badges

`.badge` base: `.75rem`, weight 600, `.65em/.3em` padding, `.02em` tracking.
The app has **10 shipment-status badges**, each reusing a Bootstrap 5 named
contextual color verbatim. Generalised tokens live in `tokens/tokens.css`
(`--cman-status-*`); this table is the literal Supply-Chain mapping.

| SC status class | Label | Generic color token | Hex (bg / fg) |
|---|---|---|---|
| `.badge-PROPOSED` | Proposed | `--cman-status-primary` | `#0d6efd` / `#fff` |
| `.badge-BOOKINGNOTPRO` | Booking-Not Proposed | `--cman-status-orange` | `#fd7e14` / `#fff` |
| `.badge-BOOKINGPRO` | Booking-Proposed | `--cman-status-teal-alt` | `#20c997` / `#fff` |
| `.badge-BOOKEDNOTPRO` | Booked-Not Proposed | `--cman-status-warning` | `#ffc107` / `#000` |
| `.badge-BOOKEDPRO` | Booked-Proposed | `--cman-status-success` | `#198754` / `#fff` |
| `.badge-LOADED` | Loaded | `--cman-status-cyan` | `#0dcaf0` / `#000` |
| `.badge-SHIPPED` | Shipped | `--cman-status-indigo` | `#6610f2` / `#fff` |
| `.badge-ARRIVED` | Arrived | `--cman-status-purple` | `#6f42c1` / `#fff` |
| `.badge-CLOSED` | Closed | `--cman-status-dark` | `#212529` / `#fff` |
| `.badge-CANCELLED` | Cancelled | `--cman-status-danger` | `#dc3545` / `#fff` |

```html
<span class="badge badge-PROPOSED px-2">Proposed</span>
<span class="badge badge-BOOKEDPRO px-2">Booked-Proposed</span>
<span class="badge badge-CLOSED px-2">Closed</span>
```

**Accessibility debt (copied faithfully from the live app — do not "fix" the
colors)**: three of these status pairs fail WCAG AA text contrast (4.5:1
minimum for normal text) when measured as rendered:

| Pair | Foreground / background | Measured contrast |
|---|---|---|
| `.badge-BOOKINGPRO` (`status.teal-alt`) | `#fff` on `#20c997` | **2.13:1** |
| `.badge-BOOKINGNOTPRO` (`status.orange`) | `#fff` on `#fd7e14` | **2.57:1** |
| form placeholder text | `#adb5bd` on white | **2.07:1** |

These are the live app's actual shipped colors, so this doc preserves them
as-is. If you reuse the generalized `status.orange` / `status.teal-alt`
foreground pairs for **new** UI outside this exact badge context, pick a
darker foreground first — don't copy them as an accessible pattern.

Other list pages (e.g. PO status) reuse **plain Bootstrap badges** instead of
the custom `badge-*` classes when there are only 2 states:
```html
<span class="badge bg-success">ACTIVE</span>
<span class="badge bg-secondary">CLOSED</span>
```

**Rule**: define a `badge-<STATUS>` class only when a domain has >2–3 states worth
color-coding at a glance (shipment lifecycle). For a simple binary/tri-state field,
plain `bg-success` / `bg-secondary` / `bg-danger` is enough — don't invent a custom
class for two states.

---

## Tables

```html
<div class="table-responsive">
  <table class="table table-hover mb-0 align-middle">
    <thead class="table-light">
      <tr>
        <th class="ps-3 sort-col"><a href="?sortBy=poNo&sortDir=asc">PO No. <i class="fas fa-sort text-muted opacity-50 small"></i></a></th>
        <th class="text-end sort-col"><a href="?sortBy=totalPo&sortDir=asc">Total PO <i class="fas fa-sort text-muted opacity-50 small"></i></a></th>
        <th class="pe-3 text-center">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr style="cursor:pointer;" onclick="window.location.href='/Po/View/1'">
        <td class="ps-3 fw-semibold"><a href="/Po/View/1" class="text-decoration-none"><small>4200000000</small></a></td>
        <td class="text-end"><small>100.00</small></td>
        <td class="pe-3 text-center" onclick="event.stopPropagation()">
          <a href="/Po/Edit/1" class="btn btn-sm btn-outline-primary" title="Edit"><i class="fas fa-edit"></i></a>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.table thead th {
  font-size: var(--cman-fs-base-sm); font-weight: var(--cman-fw-bold);
  text-transform: uppercase; letter-spacing: var(--cman-ls-tablehead);
  color: var(--cman-surface-700);
}
.table td { font-size: var(--cman-fs-lg); }
.table tbody tr:nth-child(odd)  { background-color: var(--cman-surface-0)  !important; }
.table tbody tr:nth-child(even) { background-color: var(--cman-surface-25) !important; }
```

**Rules**:
- Header: uppercase, bold, `.04em` tracking, muted gray — never colored.
- Sortable columns wrap the label in an `<a>` with a `fa-sort` icon at 50% opacity;
  the active sort column shows `fa-sort-down`/`fa-sort-up` at full `text-success`.
- Zebra striping is intentionally subtle (`#fff` / `#fafffa`, barely distinguishable) —
  don't darken it for "better readability", that's a deliberate design decision.
- Whole rows are clickable (`cursor:pointer` + `onclick` to the detail view) with
  the Actions cell calling `event.stopPropagation()` so the edit icon doesn't
  double-navigate.
- **Dense grid variant** (`Po_Create.html` line-items table — used when a table IS
  the primary input surface, not a read-only list):
  ```css
  .items-table th, .items-table td { white-space: nowrap; padding: 4px 6px; font-size: var(--cman-fs-md); }
  .items-table thead th { background: var(--cman-surface-75); font-size: var(--cman-fs-sm2); }
  .items-table .form-control, .items-table .form-select { font-size: var(--cman-fs-md); padding: 2px 6px; height: 28px; }
  ```

---

## Form controls, labels, readonly/disabled

```html
<div class="col-md-3">
  <label class="form-label small mb-1">Customer</label>
  <select name="customerCode" class="form-select form-select-sm">
    <option value="">All Customers</option>
    <option value="1000001">1000001: EXAMPLE TRADING CO., LTD</option>
  </select>
</div>
<div class="col-md-2">
  <label class="form-label small mb-1">PO No.</label>
  <input type="text" name="poNo" class="form-control form-control-sm" placeholder="Search PO..." />
</div>
```

```css
.form-label { font-size: var(--cman-fs-md); font-weight: var(--cman-fw-semibold); color: var(--cman-surface-700); margin-bottom: .25rem; }
.form-control, .form-select { font-size: var(--cman-fs-lg); }
.form-control:focus, .form-select:focus {
  border-color: var(--cman-focus-border);
  box-shadow: var(--cman-focus-ring);
}
::placeholder { color: var(--cman-surface-500) !important; opacity: 1; }

/* Readonly / disabled — one rule for every input type */
.form-control[readonly], .form-control:disabled, .form-select:disabled, .flatpickr-input[readonly] {
  background-color: var(--cman-surface-100) !important;
  opacity: 1 !important;
  cursor: default;
}

/* Date/datetime inputs: gray placeholder-style text when empty, dark once filled.
   Toggle the `.has-value` class in JS when the field gets a value. */
input[type="date"], input[type="datetime-local"] { color: var(--cman-surface-500); }
input[type="date"].has-value, input[type="datetime-local"].has-value { color: var(--cman-surface-800) !important; }
```

**Rules**: labels are always `.82rem` semibold gray, never the brand color. Inputs
are `.875rem` — one size smaller than the label, which is unusual but consistent
across the whole app; don't "fix" it to match. Every readonly/disabled state uses
the exact same light-gray fill, regardless of input type — this uniformity is
deliberate (site.css comment: "Uniform readonly / disabled field styling").

---

## Nav-tabs

```html
<ul class="nav nav-tabs">
  <li class="nav-item"><a class="nav-link active" href="#">Header</a></li>
  <li class="nav-item"><a class="nav-link" href="#">Items</a></li>
  <li class="nav-item"><a class="nav-link" href="#">Documents</a></li>
</ul>
```

```css
.nav-tabs { border-bottom: var(--cman-border-navtabs); }
.nav-tabs .nav-link { color: var(--cman-surface-600); font-size: var(--cman-fs-md2); padding: .4rem .8rem; border: none; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.nav-tabs .nav-link:hover { color: var(--cman-green); border-bottom-color: var(--cman-teal); }
.nav-tabs .nav-link.active { color: var(--cman-green) !important; border-bottom: 2px solid var(--cman-green) !important; font-weight: var(--cman-fw-semibold); background: none; }
```

---

## Pagination

```html
<nav>
  <ul class="pagination pagination-sm mb-0">
    <li class="page-item active"><a class="page-link" href="?page=1">1</a></li>
    <li class="page-item"><a class="page-link" href="?page=2">2</a></li>
    <li class="page-item"><a class="page-link" href="?page=2">&raquo;</a></li>
  </ul>
</nav>
```

```css
.page-link { color: var(--cman-green); }
.page-item.active .page-link { background-color: var(--cman-green); border-color: var(--cman-green); }
```

Always paired with a row-count caption in the card footer:
`<small class="text-muted">Showing 1 - 20 of 120</small>`. Use `pagination-sm`
— the app never uses full-size pagination.

---

## select2 (searchable dropdown)

Loaded via CDN (`select2@4.1.0-rc.0`), sized to match `.form-select` even though
its dropdown is appended to `<body>` and doesn't inherit page font-size by default.

```html
<select name="customerCode" class="form-select form-select-sm select2-search">
  <option value="">All Customers</option>
  <option value="1000001">1000001: EXAMPLE TRADING CO., LTD</option>
</select>
<script>
  $('.select2-search').select2({ width: '100%' });
</script>
```

```css
.select2-container { width: 100% !important; }
.select2-container--default .select2-selection--single { height: calc(1.5em + .75rem + 2px); border: 1px solid var(--cman-surface-400); }
.select2-container, .select2-container .select2-selection__rendered, .select2-dropdown,
.select2-results__option, .select2-search--dropdown .select2-search__field { font-size: var(--cman-fs-md); }
.select2-results__option { padding: 4px 8px; }
```

Full CSS: `../reference/sc-qas-extracted/select2-flatpickr.css`.

---

## flatpickr (date picker)

Loaded via CDN (`flatpickr@4.6.13`), compacted from its library default (238px
day-grid, 34px day cells, `.78rem`) to match the app's dense forms.

```html
<input type="text" class="form-control form-control-sm" id="poDate" placeholder="Select date">
<script>flatpickr("#poDate", { dateFormat: "d/m/Y" });</script>
```

```css
.flatpickr-calendar { font-size: var(--cman-fs-md) !important; width: auto !important; }
.dayContainer, .flatpickr-days { width: 238px !important; }
.flatpickr-day { max-width: 34px !important; height: 34px !important; line-height: 34px !important; font-size: var(--cman-fs-sm2) !important; }
```

Full CSS: `../reference/sc-qas-extracted/select2-flatpickr.css`.

---

## Login card

**This WAS dumped** — `root.html` (anonymous login), the page an
unauthenticated visitor to `/` actually sees, captured before any
sign-in redirect. NOT the same file as `theme_dump/root.html` used
elsewhere in this doc (the authenticated dashboard) — see
`reference/sc-qas-extracted/README.md` for the provenance of both. An
earlier version of this doc claimed the login page wasn't dumped and
reconstructed a guess; the markup below is copied structurally from the
real dump.

```html
<body class="d-flex align-items-center justify-content-center" style="background: var(--cman-grad-login-bg); min-height:100vh;">
  <div class="w-100" style="max-width: 420px; padding: 1rem;">

    <div class="card shadow-lg border-0" style="border-radius: var(--cman-r-lg); overflow:hidden;">
      <div class="card-header text-center py-4" style="background-color: var(--cman-green);">
        <img src="/Content/logo-full.png" alt="Chememan Logo"
             style="height:52px; width:auto; margin-bottom:8px; display:block; margin-left:auto; margin-right:auto;">
        <div class="text-white fw-bold" style="font-size: var(--cman-fs-2xl); letter-spacing: var(--cman-ls-loginbrand);">CHEMEMAN</div>
        <small class="text-white opacity-75" style="font-size: var(--cman-fs-xs); letter-spacing: var(--cman-ls-loginsub);">SUPPLY CHAIN</small>
      </div>
      <div class="card-body p-4">
        <h5 class="mb-4 text-center text-muted">Sign In</h5>
        <form method="post"><!-- point action at your own login endpoint; if your
             backend needs an antiforgery/CSRF hidden input, add your framework's
             own here — don't copy one from another app's dump. -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Username</label>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-user text-muted"></i></span>
              <input type="text" class="form-control" placeholder="Enter username" autocomplete="username" />
            </div>
          </div>
          <div class="mb-4">
            <label class="form-label fw-semibold">Password</label>
            <div class="input-group">
              <span class="input-group-text"><i class="fas fa-lock text-muted"></i></span>
              <input type="password" class="form-control" placeholder="Enter password" autocomplete="current-password" />
            </div>
          </div>
          <button type="submit" class="btn btn-cman w-100 py-2 fw-semibold">
            <i class="fas fa-sign-in-alt me-2"></i>Sign In
          </button>
        </form>
      </div>
      <div class="card-footer text-center py-3 bg-light">
        <small class="text-muted">&copy; 2026 Chememan Public Company Limited</small>
      </div>
    </div>

  </div>
</body>
```

**Rules**:
- Page background is the gradient (`--cman-grad-login-bg`) on `<body>` itself,
  centered with plain Bootstrap flex utilities (`d-flex align-items-center
  justify-content-center`) — not a wrapping flex style attribute.
- Wrapper is capped at **420px**, not 380px.
- Card header is a **flat** fill (`var(--cman-green)`, `#1a472a`) — **not** a
  gradient. The logo (`logo-full.png`, 52px tall) sits above the two-line
  brand text.
- The "Sign In" heading is a plain `<h5>` with no size override — it renders
  at the Bootstrap default (now tokenized as `--cman-fs-h5`, see
  `typography/TYPOGRAPHY.md`).
- Username/Password each use an `input-group` with a Font Awesome icon
  (`fa-user` / `fa-lock`), not a bare `form-control`.
- **`.login-card-header` in `site.css` is dead CSS — it matches zero elements
  on any dumped page.** The real card header uses a plain `card-header` class
  with an inline flat `background-color`, never `.login-card-header`. Don't
  wire new markup to that class; it's kept in the reference stylesheet only
  because it's what the app itself still ships, unused.
- Don't invent a form `action` or copy the `__RequestVerificationToken` value
  seen in the raw dump — that token is a live, per-request security value,
  not a reusable design-system asset.

---

## Component checklist (quality gate)

- [ ] No hardcoded hex/px — reach into `tokens/tokens.css`.
- [ ] Brand green (`--cman-green`) appears as a **solid fill** only in the navbar
      and `card-header` — never as a full-page background outside the login screen.
- [ ] Status badges use the literal `badge-<STATUS>` classes for the shipment
      lifecycle; plain `bg-success`/`bg-secondary`/`bg-danger` for simple 2–3 state fields.
- [ ] Every readonly/disabled input uses the single uniform gray fill
      (`var(--cman-surface-100)`) — don't invent a per-field readonly style.
- [ ] Table header stays uppercase/bold/muted-gray — never colored, never lowercase.
- [ ] No custom webfont — this is the Bootstrap 5.3.2 system stack (see
      `typography/TYPOGRAPHY.md`). If a request explicitly wants FC Minimal +
      the CI-book palette instead, use `tokens/brand-ci-legacy.css` and say so.
