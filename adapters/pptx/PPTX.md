# PPTX adapter — PptxGenJS

How to render a Chememan-branded `.pptx` deck while staying inside the design system. Pair this guide with the `pptx` skill.

## Token import

PPTX color values must be 6-char HEX without `#`. Use `tokens/tokens.pptx.json` as the source of truth (it already strips the `#`). Keep all literal colors out of slide code — pull from the JSON.

```js
import pptxgen from "pptxgenjs";
import t from "../../tokens/tokens.pptx.json" assert { type: "json" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 in (16:9)
pres.defineLayout({ name: "CMAN_16x9", width: 13.333, height: 7.5 });
```

## Master slide (brand-locked frame)

```js
pres.defineSlideMaster({
  title: "CMAN_MASTER",
  background: { color: t.color.BG_DARK },     // obsidian forest
  objects: [
    // Top-right brand mark
    { image: { path: t.logo_paths.full, x: 11.0, y: 0.35, w: 1.9, h: 0.55 } },
    // Bottom hairline divider
    { line: { x: 0.6, y: 7.05, w: 12.13, h: 0,
              line: { color: t.color.MINT, width: 0.5, transparency: 70 } } },
    // Footer
    { text: {
        text: "Chememan PCL · SET : CMAN", options: {
          x: 0.6, y: 7.12, w: 6, h: 0.3, color: t.color.MINT,
          fontFace: t.font.primary, fontSize: t.size_pt.footnote,
          charSpacing: 60
    }}},
    { text: {
        text: "Human Chemical for a Better Future", options: {
          x: 7, y: 7.12, w: 5.7, h: 0.3, color: "BFD3C8",
          fontFace: t.font.primary, fontSize: t.size_pt.footnote, align: "right"
    }}}
  ],
  slideNumber: { x: 12.6, y: 7.12, w: 0.5, h: 0.3, color: "BFD3C8",
                 fontFace: t.font.primary, fontSize: t.size_pt.footnote, align: "right" }
});
```

## Slide types

### Cover

```js
const s = pres.addSlide({ masterName: "CMAN_MASTER" });
s.background = { color: t.color.BG_DARK };
// Tinted glow shape
s.addShape(pres.ShapeType.ellipse, {
  x: -2, y: -2, w: 9, h: 9,
  fill: { color: t.color.FOREST, transparency: 70 },
  line: { type: "none" }
});
s.addText("Human Chemical · Annual Story 2026", {
  x: 0.6, y: 1.2, w: 12.1, h: 0.5, color: t.color.MINT,
  fontFace: t.font.primary, fontSize: t.size_pt.caption, charSpacing: 200
});
s.addText("Industrial chemistry,\nbuilt for what's next.", {
  x: 0.6, y: 2.0, w: 12.1, h: 3.5, color: "FFFFFF",
  fontFace: t.font.primary, fontSize: t.size_pt.display, bold: true,
  paraSpaceAfter: 12
});
s.addText("A 35-year company report — distilled.", {
  x: 0.6, y: 5.9, w: 12.1, h: 0.6, color: "BFD3C8",
  fontFace: t.font.primary, fontSize: t.size_pt.lead
});
```

### Big stat

```js
const s2 = pres.addSlide({ masterName: "CMAN_MASTER" });
// Glass-style rounded panel
s2.addShape(pres.ShapeType.roundRect, {
  x: 1.5, y: 1.5, w: 10.3, h: 4.5, rectRadius: 0.18,
  fill: { color: t.color.BG_DARK_ELEVATED, transparency: 30 },
  line: { color: t.color.MINT, width: 0.75, transparency: 70 },
  shadow: { type: "outer", blur: 24, offset: 6, angle: 90, color: "000000", opacity: 0.45 }
});
s2.addText("TONNES / YEAR", {
  x: 1.5, y: 1.9, w: 10.3, h: 0.5, color: t.color.MINT,
  fontFace: t.font.primary, fontSize: 14, charSpacing: 200, align: "center"
});
s2.addText("1.2M", {
  x: 1.5, y: 2.4, w: 10.3, h: 2.6, color: t.color.MINT,
  fontFace: t.font.primary, fontSize: 220, bold: true, align: "center"
});
s2.addText("Highest-purity quicklime in Southeast Asia.", {
  x: 1.5, y: 5.2, w: 10.3, h: 0.5, color: "FFFFFF",
  fontFace: t.font.primary, fontSize: t.size_pt.lead, align: "center", transparency: 25
});
```

### Bento (3-up)

```js
const s3 = pres.addSlide({ masterName: "CMAN_MASTER" });
const tiles = [
  { x: 0.6, w: 4.0, eyebrow: "PRODUCT", title: "Quicklime",  body: "CaO 96–98%" },
  { x: 4.7, w: 4.0, eyebrow: "PRODUCT", title: "Hydrated",   body: "Ca(OH)₂ 92%+" },
  { x: 8.8, w: 4.0, eyebrow: "PRODUCT", title: "PCC",        body: "Precipitated CaCO₃" },
];
tiles.forEach(tile => {
  s3.addShape(pres.ShapeType.roundRect, {
    x: tile.x, y: 1.6, w: tile.w, h: 4.6, rectRadius: 0.15,
    fill: { color: t.color.BG_DARK_ELEVATED, transparency: 35 },
    line: { color: t.color.MINT, width: 0.6, transparency: 75 },
    shadow: { type: "outer", blur: 16, offset: 4, angle: 90, color: "000000", opacity: 0.40 }
  });
  s3.addText(tile.eyebrow, { x: tile.x + 0.3, y: 1.9, w: tile.w - 0.6, h: 0.4,
    color: t.color.MINT, fontFace: t.font.primary, fontSize: 12, charSpacing: 200 });
  s3.addText(tile.title, { x: tile.x + 0.3, y: 2.4, w: tile.w - 0.6, h: 1.2,
    color: "FFFFFF", fontFace: t.font.primary, fontSize: t.size_pt.h1, bold: true });
  s3.addText(tile.body, { x: tile.x + 0.3, y: 5.5, w: tile.w - 0.6, h: 0.5,
    color: "BFD3C8", fontFace: t.font.primary, fontSize: t.size_pt.body });
});
```

## Color rotation (for bento variants)

When you have 4+ cards on one slide, lightly tint each with a different secondary swatch instead of running them all on the dark elevated bg — that's where the secondary palette earns its keep.

```js
const tints = [t.color.JADE, t.color.AMBER, t.color.NAVY, t.color.GOLD];
tints.forEach((color, i) => {
  s3.addShape(pres.ShapeType.roundRect, {
    x: 0.6 + i*3.1, y: 1.6, w: 3.0, h: 4.6, rectRadius: 0.15,
    fill: { color, transparency: 50 },
    line: { color: "FFFFFF", width: 0.6, transparency: 80 }
  });
});
```

## Light-mode variant

Some audiences (board printouts, traditional financials) want a **light deck**. Same master, swap:

```js
background: { color: "FFFFFF" }
// text colors:  fg primary  →  "001008" (forest-900)
//               eyebrow     →  t.color.FOREST
//               muted       →  "5C6B62"
// shape lines: subtle forest-100 instead of mint
```

## Render

```bash
node build-deck.js   # writes ./out/chememan-investor-deck.pptx
```

## Rules to enforce in the code review

- [ ] Every `color:` literal pulls from `tokens.pptx.json` (no inline HEX).
- [ ] Every `fontFace:` is `'FC Minimal'` (with `'Inter'` only as a system-fallback comment).
- [ ] Master slide is applied to every slide (`masterName: "CMAN_MASTER"`) — guarantees footer + logo on every page.
- [ ] Logo uses the official PNG from `assets/logo/`. Never re-create the lockup with PptxGenJS shapes.
- [ ] Headline weights ≥ `bold: true`. Body never bold unless it's a stat number.
- [ ] Cards use `rectRadius: 0.15–0.20` (matches the system's 12–16px web radius at slide scale).
