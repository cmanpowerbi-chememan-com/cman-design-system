# Chememan Modern Design System

> A complete, token-driven design system that fuses the official Chememan corporate identity with a modern aesthetic (glassmorphism, bento, rounded, dark-mode-first). Use it for websites, scrollable HTML decks, and PPTX presentations.

## TL;DR (humans)

```bash
# 1. View the demo (the easiest way to see what this looks like):
open design-system/chememan/examples/hero.html

# 2. To use in a Next.js / Tailwind project:
#    Copy the folder, then follow adapters/web/WEB.md.
```

## What's inside

- **Tokens** — colors, type scale, spacing, radius, shadow, glass, motion. JSON, CSS, and a Tailwind preset all stay in lockstep.
- **Typography** — FC Minimal across 18 styles (TH+EN), pre-baked utility classes (`cman-display`, `cman-h1`, `cman-eyebrow`…).
- **Components** — drop-in HTML+Tailwind for button, card, navbar, hero, stat, modal, footer, form input.
- **Patterns** — bento grid, scroll-snap deck, stat row, split feature, mascot hero, dark stack.
- **Adapters** — three short guides covering Next.js web, scrollable HTML decks, and PPTX via PptxGenJS.
- **Examples** — `hero.html` is a working page using all primitives.
- **Assets** — logos + 36 FC Minimal font files, ready to ship.

## Brand colors (quick ref)

| Role | Token | HEX |
|------|-------|-----|
| Primary brand | `--cman-forest` | `#00522C` |
| Secondary brand | `--cman-amber` | `#745021` |
| Glow accent | `--cman-mint` | `#20BB8D` |
| Surface (light) | `--cman-bg` | `#FFFFFF` |
| Surface (dark) | `--cman-forest-900` | `#001008` |
| Investor headline gradient | `from white via mint to emerald` | — |

## File structure

See `CLAUDE.md` in this folder — that's the canonical map (and what future Claude agents auto-load).

## Updating

`tokens.json` is the source of truth. If you edit it, also propagate to `tokens.css` and `tokens.pptx.json` (they're hand-mirrored — keep them in sync to avoid silent brand drift). The Tailwind preset reads no JSON; update its color/radius/shadow tables in `tailwind.preset.js` when tokens change.
