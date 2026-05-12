# Chememan Typography Standard

**Single typeface system: `FC Minimal`** — covers both English and Thai across 9 weights × italic = 18 styles. This was specified in the Chememan Corporate Identity Standard Manual ("Primary English Typeface" and "Primary Thai Typeface" pages 1C–2C). Do not introduce a second typeface unless the user explicitly asks for one — pairing decreases brand consistency.

## Loading

```html
<link rel="stylesheet" href="design-system/chememan/typography/fonts.css" />
```

The `@font-face` rules in `fonts.css` use **relative paths** to `../assets/fonts/`. If you copy the design system into a different location, the assets folder must move with it (or rewrite the URLs).

## Web fallback

`FC Minimal` is the primary, but you must declare a fallback so the page renders before the OTF/TTF arrive:

```css
font-family: 'FC Minimal', 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
```

For Thai-heavy content add `'IBM Plex Sans Thai'` or `'Noto Sans Thai'` to the fallback chain.

## Type scale

The scale is **purposefully wide** — Display 8rem down to caption 0.875rem — to give designers headroom for large editorial heroes (matching the user's reference set: Asteru, AI Tech Business, Reviews bento layouts).

| Token        | Class              | Weight | Size (clamp)             | Line | Tracking |
|--------------|--------------------|--------|--------------------------|------|----------|
| Display      | `.cman-display`    | 900    | 3.5–8rem (responsive)    | 1.05 | −0.04em  |
| H1           | `.cman-h1`         | 800    | 2.5–4.5rem               | 1.05 | −0.03em  |
| H2           | `.cman-h2`         | 700    | 2–3rem                   | 1.1  | −0.02em  |
| H3           | `.cman-h3`         | 600    | 1.5–2rem                 | 1.2  | −0.01em  |
| H4           | `.cman-h4`         | 600    | 1.25rem                  | 1.3  | 0        |
| Lead         | `.cman-lead`       | 400    | 1.125–1.5rem             | 1.5  | 0        |
| Body         | `.cman-body`       | 400    | 1rem                     | 1.6  | 0        |
| Caption      | `.cman-caption`    | 500    | 0.875rem                 | 1.4  | +0.02em  |
| Eyebrow      | `.cman-eyebrow`    | 600    | 0.75rem (uppercase)      | 1    | +0.16em  |

## Pairing rules

- **One weight per "voice"**: don't mix Bold + ExtraBold in the same heading group. Pick one.
- **Display only once per view** — hero headline only. If a section has its own headline, that's H1, not Display.
- **Eyebrow → Headline → Lead** is the canonical hero stack. Always uppercase the eyebrow with full tracking (0.16em).
- **Italic is editorial**, not decorative. Reserve for quotes, callouts, or the rare emphasis word — never run paragraphs in italic.
- **Tracking gets tighter as size grows**. Display = −0.04em; body = 0. The defaults already encode this; don't override.

## Thai-specific notes

FC Minimal handles Thai vowels and tone-mark stacking correctly — but the **CLAUDE.md project rule about Thai text in video** still applies for any deliverable that goes through ffmpeg. For PPTX and HTML, native rendering is fine.

## PPTX equivalents

`pptxgenjs` accepts `fontFace: 'FC Minimal'` directly if the .otf is installed on the system rendering the deck. If you can't guarantee that, fall back to `'Inter'` — keep the visual hierarchy by sticking to the size_pt scale defined in `tokens/tokens.pptx.json`.
