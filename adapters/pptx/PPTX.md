# PPTX adapter — PptxGenJS

How to render a Chememan-branded `.pptx` deck using jakkaritw's approved
2026-08-15 theme — a light card + green shell deck, not the retired dark
hero/glass CI-book look. Pair this guide with the `pptx` skill.

## Token import

PPTX color values must be 6-char HEX without `#`. Use `tokens/tokens.pptx.json`
as the source of truth (it already strips the `#`). Keep all literal colors
out of slide code — pull from the JSON.

```js
import pptxgen from "pptxgenjs";
import t from "../../tokens/tokens.pptx.json" assert { type: "json" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 × 7.5 in (16:9)
```

## Master slide (brand-locked frame)

Light card background — the deck equivalent of the app's own card surface,
with a green shell header bar instead of a full-page dark background.

```js
pres.defineSlideMaster({
  title: "CMAN_MASTER",
  background: { color: t.color.SURFACE },
  objects: [
    // Shell-green header bar
    { rect: { x: 0, y: 0, w: 13.333, h: 0.55, fill: { color: t.color.SHELL } } },
    { image: { path: t.logo_paths.full, x: 11.6, y: 0.1, w: 1.5, h: 0.35 } },
    { text: {
        text: "Chememan Budget Management", options: {
          x: 0.6, y: 0.1, w: 8, h: 0.35, color: "FFFFFF",
          fontFace: t.font.primary, fontSize: t.size_pt.caption, bold: true
    }}},
    // Footer hairline + page number
    { line: { x: 0.6, y: 7.05, w: 12.13, h: 0,
              line: { color: t.color.SURFACE_INSET, width: 0.75 } } },
  ],
  slideNumber: { x: 12.6, y: 7.12, w: 0.5, h: 0.3, color: t.color.INK_3,
                 fontFace: t.font.primary, fontSize: t.size_pt.footnote, align: "right" }
});
```

## Slide types

### Cover

```js
const s = pres.addSlide({ masterName: "CMAN_MASTER" });
s.addText("FY2026 Budget", {
  x: 0.6, y: 2.0, w: 12.1, h: 0.5, color: t.color.INK_3,
  fontFace: t.font.primary, fontSize: t.size_pt.caption, charSpacing: 100
});
s.addText("Where the budget stands.", {
  x: 0.6, y: 2.5, w: 12.1, h: 1.6, color: t.color.SHELL,
  fontFace: t.font.primary, fontSize: t.size_pt.display, bold: false
});
```

### Big stat card

```js
const s2 = pres.addSlide({ masterName: "CMAN_MASTER" });
s2.addShape(pres.ShapeType.roundRect, {
  x: 1.5, y: 1.5, w: 10.3, h: 4.0, rectRadius: t.card_style.rectRadius,
  fill: t.card_style.fill, line: t.card_style.line, shadow: t.card_style.shadow
});
s2.addText("APPROVED TO DATE", {
  x: 1.5, y: 1.9, w: 10.3, h: 0.5, color: t.color.INK_3,
  fontFace: t.font.primary, fontSize: t.size_pt.caption, charSpacing: 100, align: "center"
});
s2.addText("฿48.2M", {
  x: 1.5, y: 2.4, w: 10.3, h: 2.2, color: t.color.STATUS_APPROVED,
  fontFace: t.font.primary, fontSize: 96, bold: true, align: "center"
});
```

### Two-up status compare

Mirrors the app's own SAP (reference actuals) vs. Approved (board_budget)
reference-layer coloring — reuse those two colors whenever a deck compares
the same two layers.

```js
const s3 = pres.addSlide({ masterName: "CMAN_MASTER" });
[
  { x: 0.6,  label: "SAP ACTUALS", color: t.color.STATUS_SAP, value: "312.4M" },
  { x: 6.87, label: "APPROVED",    color: t.color.STATUS_APPROVED, value: "345.1M" },
].forEach(col => {
  s3.addShape(pres.ShapeType.roundRect, {
    x: col.x, y: 1.6, w: 5.87, h: 3.2, rectRadius: t.card_style.rectRadius,
    fill: t.card_style.fill, line: t.card_style.line, shadow: t.card_style.shadow
  });
  s3.addText(col.label, { x: col.x + 0.3, y: 1.9, w: 5.3, h: 0.4,
    color: t.color.INK_3, fontFace: t.font.primary, fontSize: t.size_pt.caption, charSpacing: 100 });
  s3.addText(col.value, { x: col.x + 0.3, y: 2.4, w: 5.3, h: 1.4,
    color: col.color, fontFace: t.font.primary, fontSize: 44, bold: true });
});
```

## Only one theme

The design system ships a single light Sea Green theme — there's nothing
to branch on for a deck. If a board printout genuinely needs different
ink/paper values, that's a new, explicit decision — don't repurpose
`tokens.pptx.json` values for that without one.

## Render

```bash
node build-deck.js   # writes ./out/chememan-budget-deck.pptx
```

## Rules to enforce in the code review

- [ ] Every `color:` literal pulls from `tokens.pptx.json` (no inline HEX).
- [ ] Master slide is applied to every slide (`masterName: "CMAN_MASTER"`)
      — guarantees the shell header bar + footer + page number.
- [ ] Logo uses the official PNG from `assets/logo/`. Never re-create the
      lockup with PptxGenJS shapes.
- [ ] SAP/Approved comparisons reuse `STATUS_SAP` / `STATUS_APPROVED` —
      don't invent a new color pair for the same two reference layers.
- [ ] Cards use `t.card_style` as-is (radius, fill, line, shadow) rather
      than hand-tuned per-slide values.
