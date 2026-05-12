# Web adapter — Next.js / React / Tailwind

How to wire the Chememan design system into a Next.js app with Tailwind CSS.

## 1. Install fonts + tokens

Copy (or symlink) the design system into your Next.js project:

```
your-app/
  app/
  public/
    chememan/                ← copy ../../assets here
      logo/chememan-full-logo.png
      characters/chememan-character.png
      fonts/*.{otf,ttf}
  styles/
    globals.css              ← imports tokens
  tailwind.config.js         ← uses preset
```

## 2. `globals.css`

```css
/* Import the FC Minimal @font-face declarations.
   Adjust paths if you copied the system somewhere other than /public/chememan/. */
@font-face { font-family: 'FC Minimal'; font-weight: 400; font-style: normal;
  src: url('/chememan/fonts/FC Minimal Regular ver 1.10.otf') format('opentype'); font-display: swap; }
@font-face { font-family: 'FC Minimal'; font-weight: 600; font-style: normal;
  src: url('/chememan/fonts/FC Minimal SemiBold ver 1.10.otf') format('opentype'); font-display: swap; }
@font-face { font-family: 'FC Minimal'; font-weight: 700; font-style: normal;
  src: url('/chememan/fonts/FC Minimal Bold ver 1.10.otf') format('opentype'); font-display: swap; }
@font-face { font-family: 'FC Minimal'; font-weight: 800; font-style: normal;
  src: url('/chememan/fonts/FC Minimal ExtraBold ver 1.10.otf') format('opentype'); font-display: swap; }
@font-face { font-family: 'FC Minimal'; font-weight: 900; font-style: normal;
  src: url('/chememan/fonts/FC Minimal Black ver 1.10.otf') format('opentype'); font-display: swap; }
/* (add the other weights as needed — full list in design-system/chememan/typography/fonts.css) */

/* Import the design tokens (CSS custom properties + glass utilities) */
@import "../../design-system/chememan/tokens/tokens.css";
@import "tailwindcss";

/* Project-level base */
html, body { font-family: 'FC Minimal', system-ui, sans-serif; background: var(--cman-bg); color: var(--cman-fg); }
```

## 3. `tailwind.config.js`

```js
import cman from "../design-system/chememan/tokens/tailwind.preset";

/** @type {import('tailwindcss').Config} */
export default {
  presets: [cman],
  content: ["./app/**/*.{ts,tsx,jsx,js}", "./components/**/*.{ts,tsx,jsx,js}"],
};
```

## 4. Logo component (use the brand asset, never re-trace it)

```tsx
// components/ChememanLogo.tsx
import Image from "next/image";

export function ChememanLogo({ className = "h-9 w-auto", variant = "full" }) {
  const src = variant === "character"
    ? "/chememan/characters/chememan-character.png"
    : "/chememan/logo/chememan-full-logo.png";
  return (
    <Image src={src} alt="Chememan — Human Chemical for a Better Future"
           width={400} height={200} className={className} priority />
  );
}
```

## 5. Hero example (drop-in)

See `design-system/chememan/examples/hero.html` for a copy-pasteable pattern.

## 6. Animation (use the `motion` skill)

Tokens already expose easings/durations. With Motion (formerly Framer Motion):

```tsx
import { motion } from "motion/react";

<motion.div
  initial={{ y: 20, opacity: 0 }}
  whileInView={{ y: 0, opacity: 1 }}
  viewport={{ once: true, margin: "-10%" }}
  transition={{
    duration: 0.4,                                    // matches --cman-d-slow
    ease: [0.2, 0, 0, 1]                              // matches --cman-e-standard
  }}
  className="cman-glass-dark rounded-cman-xl p-6"
>
  …
</motion.div>
```

## 7. Quick decision tree

| Want to build…                 | Pattern + skill                                                |
|--------------------------------|----------------------------------------------------------------|
| Marketing / landing page       | `patterns/PATTERNS.md` §1, §3, §4 + `ui-ux-pro-max` for review |
| Dashboard / admin              | `taste-skill` for layout brief + components from §Card/§Form    |
| Investor / corporate film      | §6 dark-mode stack — **no mascot, no warm light**              |
| Internal employee tool (CMAN AI)| §5 mascot hero is allowed                                       |
