/**
 * Chememan Design System — Tailwind preset
 * Mirrors tokens.css. Drop into tailwind.config.js:
 *   const cman = require("./design-system/chememan/tokens/tailwind.preset");
 *   module.exports = { presets: [cman], content: [...] };
 *
 * This file itself is CommonJS (module.exports) so it drop-in requires from
 * either a CJS or ESM tailwind.config.js (Node/Tailwind both accept `require()`
 * of a CJS module from either).
 *
 * PROVENANCE (rebuilt 2026-08-15): jakkaritw's approved 2026-08-15 theme for
 * the Chememan Budget Management web app — see tokens.css's header comment
 * for the full provenance chain. NOT an extraction from sc-qas.chememan.com.
 *
 * DESIGN NOTE — this preset does NOT duplicate literal hex/px values. Every
 * entry below is a `var(--cman-*)` reference straight into tokens.css, which
 * you must also link (`<link rel="stylesheet" href=".../tokens.css">`) for
 * these classes to resolve. This keeps tailwind.preset.js from becoming a
 * SECOND place a literal value could drift from tokens.css/tokens.json —
 * tools/check-tokens.py only needs to confirm each `var(--cman-*)` name
 * below actually exists in tokens.css, not that some duplicated hex still
 * matches.
 */

module.exports = {
  theme: {
    extend: {
      colors: {
        'cman-shell':            'var(--cman-shell)',
        'cman-green':            'var(--cman-green)',
        'cman-teal':             'var(--cman-teal)',
        'cman-ink-on-shell':     'var(--cman-ink-on-shell)',
        'cman-ink-on-shell-2':   'var(--cman-ink-on-shell-2)',
        'cman-accent-on-shell':  'var(--cman-accent-on-shell)',
        'cman-line-on-shell':    'var(--cman-line-on-shell)',
        'cman-surface':          'var(--cman-surface)',
        'cman-surface-inset':    'var(--cman-surface-inset)',
        'cman-ink':              'var(--cman-ink)',
        'cman-ink-2':            'var(--cman-ink-2)',
        'cman-ink-3':            'var(--cman-ink-3)',
        'cman-line':             'var(--cman-line)',
        'cman-line-2':           'var(--cman-line-2)',
        'cman-accent-text':      'var(--cman-accent-text)',
        'cman-status-sap':       'var(--cman-status-sap)',
        'cman-status-approved':  'var(--cman-status-approved)',
        'cman-status-pending':   'var(--cman-status-pending)',
        'cman-special-bg':       'var(--cman-special-bg)',
        'cman-special-edge':     'var(--cman-special-edge)',
        'cman-focus-ring':       'var(--cman-focus-ring)',
      },
      fontFamily: {
        cman:        ['var(--cman-font-sans)'],
        'cman-serif':['var(--cman-font-serif)'],
        'cman-mono': ['var(--cman-font-mono)'],
      },
      fontSize: {
        'cman-3xs':     'var(--cman-fs-3xs)',
        'cman-2xs':     'var(--cman-fs-2xs)',
        'cman-xs':      'var(--cman-fs-xs)',
        'cman-xs2':     'var(--cman-fs-xs2)',
        'cman-sm':      'var(--cman-fs-sm)',
        'cman-sm2':     'var(--cman-fs-sm2)',
        'cman-base-sm': 'var(--cman-fs-base-sm)',
        'cman-md':      'var(--cman-fs-md)',
        'cman-md2':     'var(--cman-fs-md2)',
        'cman-lg':      'var(--cman-fs-lg)',
        'cman-lg2':     'var(--cman-fs-lg2)',
        'cman-xl':      'var(--cman-fs-xl)',
        'cman-xl2':     'var(--cman-fs-xl2)',
        'cman-2xl':     'var(--cman-fs-2xl)',
        'cman-3xl':     'var(--cman-fs-3xl)',
        'cman-4xl':     'var(--cman-fs-4xl)',
        'cman-display': 'var(--cman-fs-display)',
        'cman-base':    'var(--cman-fs-base)',
      },
      fontWeight: {
        'cman-regular':   'var(--cman-fw-regular)',
        'cman-medium':    'var(--cman-fw-medium)',
        'cman-semibold':  'var(--cman-fw-semibold)',
        'cman-bold':      'var(--cman-fw-bold)',
        'cman-extrabold': 'var(--cman-fw-extrabold)',
      },
      letterSpacing: {
        'cman-tight':   'var(--cman-ls-tight)',
        'cman-tight-2': 'var(--cman-ls-tight-2)',
        'cman-tight-3': 'var(--cman-ls-tight-3)',
        'cman-wide':    'var(--cman-ls-wide)',
        'cman-wider':   'var(--cman-ls-wider)',
        'cman-widest':  'var(--cman-ls-widest)',
      },
      borderRadius: {
        'cman-base':   'var(--cman-r-base)',
        'cman-xs':     'var(--cman-r-xs)',
        'cman-pill':   'var(--cman-r-pill)',
        'cman-circle': 'var(--cman-r-circle)',
      },
      spacing: {
        'cman-4':  'var(--cman-space-4)',
        'cman-6':  'var(--cman-space-6)',
        'cman-8':  'var(--cman-space-8)',
        'cman-10': 'var(--cman-space-10)',
        'cman-12': 'var(--cman-space-12)',
        'cman-14': 'var(--cman-space-14)',
        'cman-16': 'var(--cman-space-16)',
        'cman-20': 'var(--cman-space-20)',
        'cman-24': 'var(--cman-space-24)',
        'cman-28': 'var(--cman-space-28)',
        'cman-32': 'var(--cman-space-32)',
        'cman-40': 'var(--cman-space-40)',
        'cman-48': 'var(--cman-space-48)',
      },
      ringColor: {
        'cman-focus': 'var(--cman-focus-ring)',
      },
    },
  },
};
