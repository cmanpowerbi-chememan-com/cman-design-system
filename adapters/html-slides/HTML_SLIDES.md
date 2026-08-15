# HTML Slides adapter — scrollable / scroll-snap deck

A "scrollable HTML deck" is a single HTML page where each section is a
full-viewport pane and scrolling = advancing slides. It behaves like a
deck but is shareable as a URL and indexable by search.

This adapter uses the SAME light shell + card theme as the web app — no
dark-glass/bento aesthetic (that CI-book system is retired). A deck built
this way looks like an extension of the app, not a separate brand
surface.

## Two modes

| Mode | When to use |
|---|---|
| **Scroll-snap** | Default. User-controlled pacing. |
| **Auto-advance** | Kiosk / lobby screens. Slides advance on a timer. |

Both share the same slide markup; only the container behavior differs.

## Skeleton (scroll-snap)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Chememan — Budget Story</title>
  <link rel="stylesheet" href="../../tokens/tokens.css"/>
  <style>
    html, body { margin:0; height:100%; font-family: var(--cman-font-sans); background: var(--cman-shell); color: var(--cman-ink-on-shell); }
    .deck { height:100vh; overflow-y:scroll; scroll-snap-type: y mandatory; scroll-behavior: smooth; }
    .slide { min-height:100vh; scroll-snap-align: start; display:grid; place-items:center; padding:5vh 8vw; position:relative; }
    .slide-num { position:absolute; top:5vh; left:8vw; font-family: var(--cman-font-mono); font-size: var(--cman-fs-xs); letter-spacing: var(--cman-ls-widest); text-transform: uppercase; color: var(--cman-ink-on-shell-2); }
    .slide-card { background: var(--cman-surface); border-radius: var(--cman-r-base); padding: 3rem 3.5rem; max-width: 60rem; color: var(--cman-ink); }
  </style>
</head>
<body>
  <main class="deck">
    <!-- Slide 1: cover — text straight on the shell, on-shell tokens -->
    <section class="slide">
      <span class="slide-num">01 / 04</span>
      <div style="text-align:center; max-width:48rem;">
        <p style="font-family: var(--cman-font-mono); font-size: var(--cman-fs-sm); letter-spacing: var(--cman-ls-widest); text-transform: uppercase; color: var(--cman-ink-on-shell-2);">FY2026 Budget</p>
        <h1 style="font-family: var(--cman-font-serif); font-size: var(--cman-fs-display); line-height: var(--cman-lh-tight); letter-spacing: var(--cman-ls-tight); font-weight: var(--cman-fw-regular); color: var(--cman-accent-on-shell);">
          Where the budget stands.
        </h1>
      </div>
    </section>

    <!-- Slide 2: a card holding a stat — content sits on a card, plain (non-shell) tokens -->
    <section class="slide">
      <span class="slide-num">02 / 04</span>
      <div class="slide-card">
        <p style="font-family: var(--cman-font-mono); font-size: var(--cman-fs-sm); letter-spacing: var(--cman-ls-widest); text-transform: uppercase; color: var(--cman-ink-3);">Approved to date</p>
        <p style="font-family: var(--cman-font-serif); font-size: clamp(3rem, 8vw, 6rem); font-weight: var(--cman-fw-bold); color: var(--cman-status-approved); margin-top: .5rem;">฿48.2M</p>
      </div>
    </section>

    <!-- Slide 3/4: repeat the pattern — cover slides on the bare shell, content slides inside a .slide-card -->
  </main>

  <div id="progress" style="position:fixed; left:0; top:0; height:3px; width:0; background: var(--cman-ink-on-shell); z-index:9; transition: width .2s;"></div>
  <script>
    const deck = document.querySelector('.deck');
    const bar  = document.getElementById('progress');
    deck.addEventListener('scroll', () => {
      const pct = (deck.scrollTop / (deck.scrollHeight - deck.clientHeight)) * 100;
      bar.style.width = pct + '%';
    });
  </script>
</body>
</html>
```

## Slide types

1. **Cover** — bare shell background, on-shell tokens, eyebrow + display
   headline (`components/COMPONENTS.md` § Nav has the same on-shell
   reasoning).
2. **Card stat** — a single `.slide-card` on the shell holding one number
   + label, same visual language as the app's own status/legend cards.
3. **Two-up compare** — two `.slide-card` panels side by side, each using
   `--cman-status-sap` / `--cman-status-approved` for its number, matching
   the app's own SAP/Approved reference-layer coloring.
4. **Closing CTA** — bare shell, headline + one primary action styled like
   `.btn-export` (`components/COMPONENTS.md` § Buttons).

## Auto-advance variant

```js
const slides = document.querySelectorAll('.slide');
let i = 0;
setInterval(() => {
  i = (i + 1) % slides.length;
  slides[i].scrollIntoView({ behavior: 'smooth' });
}, 8000);  // 8s per slide
```

## Aspect-ratio reminders

- **Web slides default to viewport-relative sizing** — the snap-y model is
  browser-window-relative, not slide-canvas-relative. For strict 1920×1080
  frames, wrap each slide in a `.slide-frame` with
  `aspect-ratio: 16/9; max-width: 100vw; max-height: 100vh; margin: auto;`.
- **Vertical / 9:16** — set `aspect-ratio: 9/16`. Reserve for mobile-first
  kiosks.

## When to convert to PPTX instead

If the deck needs to be emailable, presenter-noted, or played inside
Teams/Meet's slide-share UI, build it as PPTX instead — see
`../pptx/PPTX.md`. Scrollable HTML is best when it lives at a URL.
