# Chememan Modern Design System — agent brief

**Read this file before producing any Chememan-branded deliverable** — website, scrollable HTML deck, PPTX, dashboard, motion graphic, or printed asset. The design system below is the single source of truth; it merges:

1. The official **Chememan Corporate Identity Standard Manual** (logo grid, clear-space, primary colors, secondary palette, typography).
2. The user's **modern aesthetic direction** (glassmorphism, bento grid, dark hero with vibrant gradient mesh, rounded corners, layered soft shadows + glow).
3. Project-specific rules from the parent `CLAUDE.md` (e.g. clean-minimal corporate aesthetic for stakeholder work, character mascot reserved for internal/employee surfaces).

If a request conflicts with this system, **flag the conflict** before deviating. Don't silently invent off-brand variants.

---

## Folder map

```
design-system/chememan/
├── CLAUDE.md                  ← this file (auto-loaded entry point)
├── README.md                  ← human-facing usage doc (start here for tutorials)
├── tokens/
│   ├── tokens.json            ← canonical machine-readable tokens (W3C-ish format)
│   ├── tokens.css             ← CSS custom properties + glass utility classes
│   ├── tokens.pptx.json       ← PptxGenJS-friendly mirror (HEX without #, fontFace strings, pt sizes)
│   └── tailwind.preset.js     ← Tailwind preset (drop-in for new projects)
├── typography/
│   ├── fonts.css              ← @font-face for FC Minimal × 18 styles
│   └── TYPOGRAPHY.md          ← scale, pairing rules, Thai/EN notes
├── components/
│   └── COMPONENTS.md          ← button, card, navbar, hero, modal, footer, form
├── patterns/
│   └── PATTERNS.md            ← bento grid, scroll-snap deck, stat row, split feature, mascot hero, dark stack
├── adapters/
│   ├── web/WEB.md             ← Next.js + Tailwind setup
│   ├── html-slides/HTML_SLIDES.md  ← scrollable / kiosk decks
│   └── pptx/PPTX.md           ← PptxGenJS master + slide-type cookbook
├── examples/
│   └── hero.html              ← working demo: nav + hero + bento + footer
└── assets/
    ├── logo/chememan-full-logo.png
    ├── characters/chememan-character.png
    └── fonts/FC Minimal *.{otf,ttf}      ← 36 files (18 styles × 2 formats)
```

## Brand non-negotiables (from the CI book)

- **Working primary palette = Green + Blue + Brown** (user direction, 2026-05-10):
  - **Forest** `#00522C` — Primary 1, brand green. Heritage / nature / heavy industry.
  - **Blue** `#3C60A5` — Primary 2, brand blue (with `sky #5ECDF6` for highlights, `navy #223562` for deep surfaces). Tech / digital / data.
  - **Amber** `#745021` — Primary 3, brand brown. Earth / mascot / warm editorial.
  - White + Black round out the primary system.
  - **Note**: The official CI book p.12 only labels Forest/Amber/White/Black as primary. Blue is officially a secondary swatch. We promote it to primary-tier here because the modern aesthetic the user wants leans on the green/blue/brown triad. Both are valid — be explicit about which you're following when stakes are high (printed brand collateral defaults to the official 4; digital surfaces default to the working 5).
- **Secondary palette**: 12 remaining swatches (`tokens.json → color.secondary`) for accents, illustrations, and stat color-coding. Never as primary CTA.
- **Logo**: use the PNG in `assets/logo/`. Do not redraw, restroke, recolor, distort, or rotate. Clear-space ≥ X-height (the "N" of CHEMEMAN). Min size 1.5 cm full / 1 cm character.
- **Logo on color**: green logo only on tints ≤ 60% of secondary swatches. Above that — invert to white knockout. The CI book p.13/p.15 shows the exact fades.
- **Don'ts** (CI book p.8 "Incorrect Treatments"): no color swap, no stroke, no shadow, no proportion change, no busy photo background, no text squish.
- **Typography**: FC Minimal only, EN + TH. Don't pair with another typeface.

## Modern aesthetic — the user's direction

The brand book gives the **what**. The user's reference set (`input/Chememan Brand Kits/Design Style Reference/`) defines the **how**:

- **Dark hero panels** (forest-900 / midnight gradients) with bright editorial typography and **mint glow** as the focal accent.
- **Glassmorphism — bright frosted white** (revised 2026-05-10). The canonical recipe is `rgba(255,255,255,0.18)` background + `1px solid rgba(255,255,255,0.35)` border + `blur(24px) saturate(180%)` + `inset 0 1px 0 rgba(255,255,255,0.45)` top-edge highlight. The point: text stays readable on the frost while colors behind still bleed through softly. Earlier dark variants (`rgba(255,255,255,0.06)`) made cards feel like flat grey panels — don't use those. For brand-tinted glass, use `cman-glass-tint-forest`, `cman-glass-tint-blue`, `cman-glass-tint-amber` — all keep ~20% white tint and only hint the brand color (10–15% alpha) so it feels like white frost picking up the surface behind, not a solid color card.
- **Bento layouts** with mixed tile sizes (2:2 hero tile + 1:1 stats + horizontal quote) — see `patterns/PATTERNS.md` §1.
- **Rounded corners** ladder: 16 → 24 → 32 px depending on surface scale.
- **Layered shadow + glow** — soft drop shadow + faint forest/amber glow on emphasis surfaces (`--cman-sh-glow-forest`).
- **Type contrast** — eyebrow (12px tracking 0.16em uppercase) → display (8rem extrabold) → lead (1.25rem regular). Wide vertical leap is the signature.
- **Section rhythm** — never stack two same-tone sections in a row. Alternate dark-mesh ↔ bright-glass ↔ off-white-editorial. Any text-heavy section over a colored background **must** be wrapped in a `cman-glass-heavy` "story panel" for readability (see `patterns/PATTERNS.md` §0a). At least one **clean off-white editorial section** (Levels/Yucca aesthetic — `#F7F5F0` background, oversized FC Minimal headline, hairlines, small color-square eyebrows) belongs in any landing page over 4 sections (see §0b). Don't run an all-dark or all-glass page.

## Audience-aware variants

| Context | Aesthetic | Mascot? | Background |
|---|---|---|---|
| **Investor / corporate** (`proj_chememan` style) | Clean dark, mint glow, abstract — **NOT factory imagery** | ❌ | Forest-900 + grad-midnight |
| **Internal / employee** (`proj_cmanai` style) | Friendly, character-led | ✅ | Light or grad-hero-mesh |
| **Marketing / B2B web** | Modern bento + glass | optional | Hero-mesh gradient |
| **Print PPTX (board)** | Light deck, conservative | ❌ | White + forest accent |

When in doubt, **default to the corporate dark stack** — it's the safest brand-consistent baseline and the closest match to the user's reference deck.

## Quick recipes

**"Build a Chememan website."**
1. `npm create next-app` (or use the existing project).
2. Follow `adapters/web/WEB.md` to wire fonts + tokens + Tailwind preset.
3. Use `patterns/PATTERNS.md` §1 (bento) + §3 (stat row) + §4 (split feature) for the home page.
4. Run `ui-ux-pro-max` skill for review pass.

**"Build a Chememan scrollable HTML slide deck."**
1. Start from `examples/hero.html` — it's already loaded with the system.
2. Convert sections to `<section class="slide">` with `scroll-snap-align: start`.
3. Follow `adapters/html-slides/HTML_SLIDES.md` for the deck container + progress bar pattern.
4. Add motion via the `motion` skill — token easings/durations are predefined.

**"Build a Chememan PPTX."**
1. Use the `pptx` skill.
2. Import `tokens/tokens.pptx.json` as the color/font source — never inline HEX.
3. Use `adapters/pptx/PPTX.md` master-slide and slide-type code as the starting template.
4. Run `review-slides` skill afterwards.

## Canonical mistakes to avoid

- ❌ Using forest as a card-fill across the whole layout — overuses the focal, feels heavy. Forest = logo + 1 emphasis.
- ❌ **Forgetting blue.** The working palette is green + blue + brown. If a layout uses only forest+amber, you've left a primary out of the system. Rotate (use `cman-glass-tint-blue` for one tile, sky for an accent stripe, blue-amber gradient on a CTA, etc.).
- ❌ **Dark/opaque glass** (e.g. `rgba(255,255,255,0.06)`). Old default — replaced. Use the bright-frost recipe (~18% white) so the colors behind read through.
- ❌ Glass surface on a flat white page — looks like a thin grey card. Glass needs a colorful/imagery layer behind it.
- ❌ Brand-tinted glass that's too saturated (`rgba(0,82,44,0.20)` was the old "glass-brand" — it reads as solid forest). Tints must be 10–15% alpha, layered over a 20% white wash.
- ❌ Mixing FC Minimal with Inter/Roboto/etc. — FC Minimal handles both EN and TH; pairing weakens the system.
- ❌ Using the mascot on investor decks — it reads as informal. (Memory: `feedback_aesthetic_clean_minimal`).
- ❌ Hardcoded HEX or px values — always reach into `tokens.css` (web) or `tokens.pptx.json` (PPTX).

## Updating this system

- Token changes go to `tokens.json` first; mirror to `tokens.css` and `tokens.pptx.json` immediately. Out-of-sync token files are the #1 silent source of brand drift.
- Adding a component? Append to `components/COMPONENTS.md` with a working snippet — do **not** create a sub-file unless the component is genuinely large (>500 lines).
- New pattern? Same — append to `patterns/PATTERNS.md`.
- If you change anything in this folder, **update the parent `CLAUDE.md` only if a top-level rule changed**. Internal additions don't need a parent update.
