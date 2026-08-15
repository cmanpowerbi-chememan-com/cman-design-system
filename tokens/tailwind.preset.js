/**
 * Chememan Design System — Tailwind preset
 * Mirrors tokens.json / tokens.css. Drop into tailwind.config.js:
 *   const cman = require("./design-system/chememan/tokens/tailwind.preset");
 *   module.exports = { presets: [cman], content: [...] };
 *
 * This file itself is CommonJS (module.exports) so it drop-in requires from
 * either a CJS or ESM tailwind.config.js (Node/Tailwind both accept `require()`
 * of a CJS module from either). Keep the require() example above in sync with
 * this file's own module.exports — don't reintroduce an import/export-default
 * example while this file stays CJS.
 *
 * PROVENANCE (2026-08-15): extracted from the LIVE Chememan Supply Chain
 * app (https://sc-qas.chememan.com — QAS/staging), a Bootstrap 5.3.2
 * admin app — NOT the CI-book glassmorphism system (see
 * tokens/brand-ci-legacy.css for that palette instead).
 *
 * The app itself ships no Tailwind — if you're building a Tailwind project
 * that needs to LOOK like the Supply Chain app, this preset gets you the
 * same colors/scale as utility classes (`bg-cman-green`) instead of the
 * Bootstrap classes the live app actually uses. For a byte-for-byte
 * Bootstrap drop-in, use adapters/web/WEB.md instead.
 */

const green = {
  DEFAULT: '#1a472a',
  50: '#f8fdf9', 100: '#f0f7f4', 200: '#afc8bd', 300: '#6e9986',
  400: '#2d6a4f', 500: '#1a472a', 600: '#153a23', 700: '#112e1d',
  800: '#0c2317', 900: '#081711',
};

// Renamed from "neutral" (2026-08-15) -- this scale is NOT a strict light->dark
// gray ramp: 25 and 200 are green-tinted (200 == layout sidebar-active) and 200
// is lighter than 150. See tokens.css for the full explanation. `neutral` below
// is kept as a compatibility alias pointing at the same object.
const surface = {
  0: '#ffffff', 25: '#fafffa', 50: '#f8f9fa', 75: '#f1f3f5',
  100: '#f0f0f0', 150: '#e9ecef', 200: '#e8f5e9', 300: '#dee2e6',
  400: '#ced4da', 500: '#adb5bd', 600: '#6c757d', 700: '#495057',
  800: '#212529', 900: '#000000',
};
const neutral = surface; // compatibility alias -- reach for `surface` in new code

// Bootstrap 5's own named contextual colors — reused verbatim by the app's
// 10 shipment-status badges. See components/COMPONENTS.md for the literal
// SC status name -> color mapping.
const status = {
  primary: '#0d6efd', orange: '#fd7e14', 'teal-alt': '#20c997',
  warning: '#ffc107', success: '#198754', cyan: '#0dcaf0',
  indigo: '#6610f2', purple: '#6f42c1', dark: '#212529', danger: '#dc3545',
};

module.exports = {
  theme: {
    extend: {
      colors: {
        'cman-green':   green,
        'cman-teal':    '#2d6a4f',
        // 'cman-light' / 'cman-lighter': declared in the app's own :root but NOT
        // rendered anywhere (see tokens.css for the full explanation) -- kept
        // here only for hex-value parity with tokens.css/tokens.json.
        'cman-light':   '#f0f7f4',
        'cman-lighter': '#f8fdf9',
        'cman-surface': surface,
        'cman-neutral': neutral, // compatibility alias, same object as cman-surface
        'cman-status':  status,
      },
      fontFamily: {
        // The app declares no custom font-family — this IS the Bootstrap
        // 5.3.2 default system stack, not a placeholder fallback.
        cman: [
          'system-ui', '-apple-system', '"Segoe UI"', 'Roboto',
          '"Helvetica Neue"', '"Noto Sans"', '"Liberation Sans"', 'Arial',
          'sans-serif', '"Apple Color Emoji"', '"Segoe UI Emoji"',
          '"Segoe UI Symbol"', '"Noto Color Emoji"',
        ],
      },
      fontSize: {
        'cman-2xs': '.65rem',    // sidebar-section-label
        'cman-xs':  '.72rem',    // login sub-brand
        'cman-sm':  '.75rem',    // badge, flatpickr weekday
        'cman-sm2': '.78rem',    // sidebar-brand, flatpickr day
        'cman-base-sm': '.8rem', // table thead th
        'cman-md':  '.82rem',    // form-label, select2, flatpickr calendar
        'cman-md2': '.85rem',    // nav-tabs link, section-title
        'cman-lg':  '.875rem',   // form-control/select, table td
        'cman-lg2': '.88rem',    // sidebar nav-link, flatpickr current-month
        'cman-xl':  '.9rem',     // card-header, sidebar nav-icon/label, navbar username
        'cman-xl2': '.95rem',    // navbar brand
        'cman-2xl': '1rem',      // login brand
        'cman-3xl': '1.1rem',    // collapsed sidebar nav-icon
        // Bootstrap 5.3.2 heading defaults -- inherited, not declared anywhere
        // in the app's own CSS. Observed via unstyled <h4>/<h5> tags.
        'cman-h5': '1.25rem',    // <h5> -- e.g. "Sign In" login heading, modal titles
        'cman-h4': '1.5rem',     // <h4> -- e.g. list-page headers like "PO List"
      },
      fontWeight: {
        'cman-regular':  '400',
        'cman-semibold': '600',
        'cman-bold':     '700',
      },
      letterSpacing: {
        'cman-badge':          '.02em',
        'cman-table-head':     '.04em',
        'cman-sidebar-brand':  '.04em',
        'cman-section-title':  '.06em',
        'cman-login-brand':    '.08em',
        'cman-sidebar-section':'.1em',
        'cman-login-sub':      '.12em',
      },
      borderRadius: {
        'cman-xs': '4px',   // badge-adjacent chips, section-title
        'cman-sm': '6px',   // #sidebarToggle
        'cman-md': '8px',   // card, card-header top corners
        'cman-lg': '16px',  // login card
      },
      // Tailwind has no single border-shorthand utility (width/style/color are
      // separate utilities) -- these widths pair with a `border` style utility
      // and a `border-cman-surface-300` color utility (#dee2e6) to reproduce
      // tokens.css's `--cman-border-navtabs` / `--cman-border-hairline`.
      borderWidth: {
        'cman-navtabs':  '2px',
        'cman-hairline': '1px',
      },
      boxShadow: {
        'cman-card':           '0 1px 6px rgba(0,0,0,.07)',
        'cman-sidebar':        '2px 0 8px rgba(0,0,0,.05)',
        'cman-btn-hover':      '0 2px 6px rgba(26,71,42,.35)',
        'cman-sticky-header':  '0 2px 6px rgba(0,0,0,.06)',
        'cman-collapsed-active-inset': 'inset 3px 0 0 var(--sidebar-active-border)',
      },
      backgroundImage: {
        'cman-grad-login-bg':     'linear-gradient(135deg, #1a472a 0%, #2d6a4f 50%, #1a472a 100%)',
        // NOT used by the real login header (flat green fill) -- only backs
        // the dead `.login-card-header` rule in site.css. Kept for hex parity.
        'cman-grad-login-header': 'linear-gradient(135deg, #1a472a, #2d6a4f)',
      },
      transitionDuration: {
        'cman': '250ms', // 0.25s ease — the app's one and only transition
      },
      transitionTimingFunction: {
        'cman': 'ease',
      },
      spacing: {
        'cman-sidebar':           '240px',
        'cman-sidebar-collapsed': '64px',
        'cman-navbar':            '44px',
      },
      ringColor: {
        'cman-focus': '#2d6a4f',
      },
    },
  },
};
