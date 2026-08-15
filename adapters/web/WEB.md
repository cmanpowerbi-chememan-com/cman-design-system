# Web adapter — plain HTML/CSS drop-in

How to make a new project look like the Chememan Budget Management web app
(jakkaritw's approved 2026-08-15 theme). The source app is React + Next.js
with its own hand-written CSS — **no Bootstrap, no jQuery, no icon-font
CDN** — so this adapter needs neither. If your project is Tailwind-based
instead, see "Tailwind projects" below.

## 1. The one link tag you need

```html
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="design-system/chememan/tokens/tokens.css" />
</head>
```

That's it — no CDN, no build step. `tokens.css` carries every color
(light + dark via `[data-theme='dark']`), the type scale, radius, and
spacing as CSS custom properties. Write your own component CSS against
those custom properties, using the class names and snippets in
`components/COMPONENTS.md` as the starting point (they're copy-paste
compatible with the real app).

## 2. Dark mode

The theme switches via a `data-theme` attribute, not a class or media
query:

```html
<html data-theme="dark">
```

Toggle it in JS (`document.documentElement.setAttribute('data-theme',
'dark')`) and every `--cman-*` color custom property repoints
automatically — no separate dark stylesheet to maintain.

## 3. Wire up the app shell

Copy `.nav` / `.wrap` / `.page-head` from `components/COMPONENTS.md` §
Nav and `patterns/PATTERNS.md` § 1. That's the whole shell — no framework
component library needed.

## 4. Quick decision tree

| Want to build… | Start from |
|---|---|
| A new page matching the Budget app | `patterns/PATTERNS.md` §1 (shell) + §2/§3 depending on grid vs. modal |
| A one-off status/state indicator | `components/COMPONENTS.md` § Status legend + status cell |
| Something that should look like the app's example page | `examples/app-shell.html` — open it directly, no build step |

## Tailwind projects (React / Next.js)

If your project is Tailwind-based and wants the SAME palette/scale as
utility classes:

```js
// tailwind.config.js
const cman = require("./design-system/chememan/tokens/tailwind.preset");
module.exports = { presets: [cman], content: [...] };
```

This gets you `bg-cman-shell`, `text-cman-ink`, `bg-cman-green`, etc. —
each one is a thin `var(--cman-*)` forward into `tokens.css` (see the
preset's own header comment), so **you must still link `tokens/tokens.css`**
for these utility classes to resolve to anything. The upside: dark-mode
switching via `data-theme` works through Tailwind classes automatically,
with nothing to keep in sync between the preset and the CSS file.

For a pixel-identical drop-in, prefer plain CSS + `components/COMPONENTS.md`
over reimplementing components as Tailwind utility soup — the source app
itself is hand-written CSS, not Tailwind.
