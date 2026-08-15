# Web adapter — Bootstrap 5.3.2 drop-in

How to make a new project **look identical to the live Chememan Supply Chain app**
(https://sc-qas.chememan.com — QAS/staging). The reference app is plain
server-rendered HTML + Bootstrap + jQuery, not React/Next — this adapter targets
that same stack. If your project is React/Next/Tailwind, see the "Tailwind
projects" section at the bottom instead.

> For the CI-book / glassmorphism system instead of the live-app look, use
> `tokens/brand-ci-legacy.css` + `typography/fonts.css` and skip everything below.

## 1. CDN links — exact order

This is the order the live app itself loads them in (`<head>`). Items 1–3 and
5–6 are linked `<link rel="stylesheet">` tags, verified directly against the
dumped `<head>` markup. **Items 7 and 8 are NOT separate linked stylesheets in
the real app** — they are inline `<style>` blocks embedded in the app's own
shared layout, split out into standalone files here (`layout-shell.css`,
`table-overrides.css`) purely for readability. The order below is this doc's
own reconstruction of "shell rules before table rules", not something the app
literally does via `<link>` order.

```html
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- 1. Bootstrap 5.3.2 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- 2. Font Awesome 6.5.0 — assumed by every component's icon markup -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">

  <!-- 3. This design system's tokens (custom properties) -->
  <link rel="stylesheet" href="design-system/chememan/tokens/tokens.css" />

  <!-- 4. The reference stylesheet — component classes (.btn-cman, .badge-*, .card-header fill, etc.)
          that consume the tokens above. Copy this file into your project; it is the
          app's actual custom CSS, 1:1. -->
  <link rel="stylesheet" href="design-system/chememan/reference/sc-qas-extracted/site.css" />

  <!-- 5. Only if the page uses a date picker -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.13/flatpickr.min.css" />
  <!-- + design-system/chememan/reference/sc-qas-extracted/select2-flatpickr.css -->

  <!-- 6. Only if the page uses a searchable dropdown -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0-rc.0/css/select2.min.css" />

  <!-- 7. App-shell layout rules (sidebar, navbar height, main-content scroll) -->
  <link rel="stylesheet" href="design-system/chememan/reference/sc-qas-extracted/layout-shell.css" />

  <!-- 8. Table zebra + card-header height overrides -->
  <link rel="stylesheet" href="design-system/chememan/reference/sc-qas-extracted/table-overrides.css" />
</head>
```

**Do not add a custom `font-family`** — the app declares none anywhere; it
renders in Bootstrap's own default system-font stack. See
`typography/TYPOGRAPHY.md`.

## 2. Scripts — exact order

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<!-- your app's own JS here -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/flatpickr/4.6.13/flatpickr.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.1.0-rc.0/js/select2.min.js"></script>
```

jQuery loads before Bootstrap's JS bundle; select2 needs jQuery, so it always
loads last.

## 3. Wire up the app shell

Copy the sidebar-toggle script from `components/COMPONENTS.md § Sidebar` and the
`#wrapper` / `#mainContent` structure from `patterns/PATTERNS.md § 1`. That's
the whole shell — no framework component library needed.

## 4. Assumptions your markup can rely on

- **Font Awesome 6.5.0** free icon set — every component snippet in
  `components/COMPONENTS.md` uses `fas`/`fab` classes from it directly.
- **Bootstrap 5.3.2** utility classes (`d-flex`, `gap-2`, `text-end`, `me-1`, …)
  are used throughout instead of custom utility CSS — don't reinvent them.
- **jQuery 3.7.1** is present (required by select2; Bootstrap 5's own JS does
  not need it).

## 5. Quick decision tree

| Want to build… | Start from |
|---|---|
| A new authenticated screen matching the SC app | `patterns/PATTERNS.md` §1 (shell) + §2/§3 depending on list vs. form |
| A login screen | `patterns/PATTERNS.md` §4 |
| A one-off status/state indicator | `components/COMPONENTS.md` § Status badges |
| Something that should look like the app's example page | `examples/app-shell.html` — open it directly, no build step |

## Tailwind projects (React / Next.js)

If your project is Tailwind-based and you want the SAME palette/scale as
utility classes instead of Bootstrap classes:

```js
// tailwind.config.js
const cman = require("./design-system/chememan/tokens/tailwind.preset");
module.exports = { presets: [cman], content: [...] };
```

This gets you `bg-cman-green`, `text-cman-surface-700`, etc. — but note the
live app itself ships **no Tailwind**; component markup in `components/COMPONENTS.md`
is Bootstrap-class HTML. For a pixel-identical drop-in, prefer the CDN + `site.css`
route above over reimplementing components in Tailwind.
