/**
 * Chememan Modern Design System — Tailwind preset
 * Drop into tailwind.config.js:
 *   import cman from "./design-system/chememan/tokens/tailwind.preset";
 *   export default { presets: [cman], content: [...] };
 *
 * Color names match tokens.css custom-property suffixes (cman-forest, cman-mint, etc.)
 * so devs can reach for either utility classes (`bg-cman-forest`) or vars (`var(--cman-forest)`).
 */

// Primary tier (working palette per user direction, 2026-05-10):
// Green + Blue + Brown. Blue elevated from secondary to primary for the
// Chememan modern aesthetic. Official CI book p.12 lists only Forest/Amber/
// White/Black as primary — Blue is officially secondary.
const brand = {
  forest:   { DEFAULT: '#00522C', 100: '#E5EDE9', 200: '#BFD3C8', 300: '#7FA897',
              400: '#3F7E66', 500: '#00522C', 600: '#00421F', 700: '#003118',
              800: '#00210F', 900: '#001008' },
  blue:     { DEFAULT: '#3C60A5', 100: '#E1E8F4', 200: '#B8C7E4', 300: '#8AA1CF',
              400: '#5C7BBA', 500: '#3C60A5', 600: '#2F4D87', 700: '#223562',
              800: '#161F3C', 900: '#0A0F1F' },
  amber:    { DEFAULT: '#745021', 100: '#F1ECE3', 200: '#D6C7A6', 300: '#A8916A',
              400: '#8F6A3D', 500: '#745021', 600: '#5C3F19' },
  navy:     '#223562', sky: '#5ECDF6',  jade: '#388062',
  emerald:  '#00AC69', mint: '#20BB8D', olive: '#6F5229', copper: '#AD6637',
  gold:     '#CD9D3F', yellow:'#FFD100', peach: '#F6CEB7', coral: '#E8676A',
  mist:     '#EFEFEF', grey: '#7F7F7F', charcoal: '#333333',
};

module.exports = {
  theme: {
    extend: {
      colors: {
        'cman-forest':   brand.forest,
        'cman-blue':     brand.blue,
        'cman-amber':    brand.amber,
        'cman-navy':     brand.navy,
        'cman-sky':      brand.sky,
        'cman-jade':     brand.jade,
        'cman-emerald':  brand.emerald,
        'cman-mint':     brand.mint,
        'cman-olive':    brand.olive,
        'cman-copper':   brand.copper,
        'cman-gold':     brand.gold,
        'cman-yellow':   brand.yellow,
        'cman-peach':    brand.peach,
        'cman-coral':    brand.coral,
        'cman-mist':     brand.mist,
        'cman-grey':     brand.grey,
        'cman-charcoal': brand.charcoal,
      },
      fontFamily: {
        cman:    ['"FC Minimal"', 'Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'cman-th':['"FC Minimal"', '"IBM Plex Sans Thai"', '"Noto Sans Thai"', 'sans-serif'],
      },
      borderRadius: {
        'cman-xs':  '4px',
        'cman-sm':  '8px',
        'cman-md':  '12px',
        'cman-lg':  '16px',
        'cman-xl':  '24px',
        'cman-2xl': '32px',
        'cman-3xl': '48px',
      },
      boxShadow: {
        'cman-xs':   '0 1px 2px rgba(0,16,8,0.06)',
        'cman-sm':   '0 2px 4px rgba(0,16,8,0.08), 0 1px 2px rgba(0,16,8,0.04)',
        'cman-md':   '0 8px 16px -4px rgba(0,16,8,0.10), 0 2px 4px rgba(0,16,8,0.06)',
        'cman-lg':   '0 20px 40px -12px rgba(0,16,8,0.16), 0 8px 16px -8px rgba(0,16,8,0.08)',
        'cman-xl':   '0 32px 64px -16px rgba(0,16,8,0.20), 0 12px 24px -12px rgba(0,16,8,0.10)',
        'cman-2xl':  '0 48px 96px -24px rgba(0,16,8,0.28)',
        'cman-glow-forest': '0 0 32px rgba(0,82,44,0.45), 0 0 4px rgba(32,187,141,0.30)',
        'cman-glow-blue':   '0 0 32px rgba(60,96,165,0.50), 0 0 4px rgba(94,205,246,0.40)',
        'cman-glow-amber':  '0 0 32px rgba(116,80,33,0.40), 0 0 4px rgba(205,157,63,0.30)',
      },
      backgroundImage: {
        'cman-grad-forest-glow':  'radial-gradient(ellipse at top, #1F8B5A 0%, #00522C 35%, #001008 100%)',
        'cman-grad-blue-glow':    'radial-gradient(ellipse at top, #5ECDF6 0%, #3C60A5 35%, #0A0F1F 100%)',
        'cman-grad-amber-glow':   'radial-gradient(ellipse at top, #C6913E 0%, #745021 40%, #1A0F05 100%)',
        'cman-grad-forest-amber': 'linear-gradient(135deg, #00522C 0%, #745021 100%)',
        'cman-grad-forest-blue':  'linear-gradient(135deg, #00522C 0%, #3C60A5 100%)',
        'cman-grad-blue-amber':   'linear-gradient(135deg, #3C60A5 0%, #745021 100%)',
        'cman-grad-tricolor':     'linear-gradient(135deg, #00522C 0%, #3C60A5 50%, #745021 100%)',
        'cman-grad-midnight':     'linear-gradient(180deg, #0A0F1F 0%, #161F3C 50%, #001008 100%)',
        'cman-grad-sunrise-jade': 'linear-gradient(135deg, #00522C 0%, #20BB8D 50%, #5ECDF6 100%)',
        'cman-grad-headline':     'linear-gradient(135deg, #FFFFFF 0%, #5ECDF6 60%, #20BB8D 100%)',
        'cman-grad-hero-mesh':
          'radial-gradient(at 20% 10%, #00522C 0%, transparent 45%),' +
          'radial-gradient(at 80% 0%,  #3C60A5 0%, transparent 50%),' +
          'radial-gradient(at 50% 90%, #745021 0%, transparent 50%),' +
          'radial-gradient(at 90% 80%, #20BB8D 0%, transparent 40%), #050E1A',
      },
      backdropBlur: {
        'cman-sm':  '8px',  'cman-md':  '16px', 'cman-lg':  '24px',
        'cman-xl':  '40px', 'cman-2xl': '64px',
      },
      transitionTimingFunction: {
        'cman-standard':   'cubic-bezier(0.2, 0, 0, 1)',
        'cman-decelerate': 'cubic-bezier(0, 0, 0.2, 1)',
        'cman-accelerate': 'cubic-bezier(0.4, 0, 1, 1)',
        'cman-spring':     'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      transitionDuration: {
        'cman-instant':   '100ms',
        'cman-fast':      '180ms',
        'cman-base':      '240ms',
        'cman-slow':      '400ms',
        'cman-slower':    '640ms',
        'cman-cinematic': '1200ms',
      },
    },
  },
};
