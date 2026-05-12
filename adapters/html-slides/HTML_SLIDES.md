# HTML Slides adapter — scrollable / scroll-snap deck

A "scrollable HTML deck" is a single HTML page where each section is a full-viewport pane and scrolling = advancing slides. It behaves like a deck but is shareable as a URL, animatable with web tech, and indexable by search.

## Two modes

| Mode               | When to use                                       |
|--------------------|---------------------------------------------------|
| **Scroll-snap**    | Default. User-controlled pacing. Good for narrative landing pages. |
| **Auto-advance**   | Kiosk / lobby screens. Slides advance on a timer. |

Both share the same slide markup; only the container behavior differs.

## Skeleton (scroll-snap)

```html
<!doctype html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <title>Chememan — Investor Story</title>
  <link rel="stylesheet" href="../../typography/fonts.css"/>
  <link rel="stylesheet" href="../../tokens/tokens.css"/>
  <style>
    html, body { margin:0; height:100%; font-family:'FC Minimal', sans-serif; background: var(--cman-forest-900); color:#fff; }
    .deck { height:100vh; overflow-y:scroll; scroll-snap-type: y mandatory; scroll-behavior: smooth; }
    .slide { height:100vh; scroll-snap-align: start; display:grid; place-items:center; padding:5vh 8vw; position:relative; }
    .slide-num { position:absolute; top:5vh; left:8vw; font-size:.75rem; letter-spacing:.16em; text-transform:uppercase; color:rgba(255,255,255,.5); }
  </style>
</head>
<body>
  <main class="deck">
    <!-- Slide 1: cover -->
    <section class="slide" style="background: var(--cman-grad-hero-mesh);">
      <span class="slide-num">01 / 06</span>
      <div style="text-align:center; max-width:90vw;">
        <p class="cman-eyebrow" style="color: var(--cman-mint);">SET : CMAN</p>
        <h1 class="cman-display" style="background: linear-gradient(135deg,#fff,#20BB8D);
                                        -webkit-background-clip:text; background-clip:text; color:transparent;">
          Industrial chemistry,<br/>built for what's next.
        </h1>
        <p class="cman-lead" style="margin-top:2rem; color:rgba(255,255,255,.75); max-width:42rem; margin-inline:auto;">
          A 35-year company report — distilled.
        </p>
      </div>
    </section>

    <!-- Slide 2: stat -->
    <section class="slide" style="background: var(--cman-forest-900);">
      <span class="slide-num">02 / 06</span>
      <div class="cman-glass-dark" style="padding:4rem 5rem; border-radius: var(--cman-r-2xl);">
        <p class="cman-eyebrow" style="color: var(--cman-mint);">Tonnes / year</p>
        <p class="cman-display" style="font-size:clamp(4rem,12vw,12rem); color: var(--cman-mint); margin-top:1rem;">
          1.2M
        </p>
        <p class="cman-caption" style="color:rgba(255,255,255,.7); margin-top:1rem;">
          Highest-purity quicklime in Southeast Asia.
        </p>
      </div>
    </section>

    <!-- Slide 3: chart / bento … etc. -->

  </main>

  <!-- Optional: progress bar -->
  <div id="progress"
       style="position:fixed; left:0; top:0; height:3px; width:0; background: var(--cman-mint); z-index:9; transition: width .2s;"></div>
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

## Slide types (mix and match)

1. **Cover** — `--cman-grad-hero-mesh` background, eyebrow + display headline + lead.
2. **Big stat** — single number in `cman-display` size, glass card frame.
3. **Quote** — italicized lead with `cman-glass-brand`, attribution caption beneath.
4. **Bento grid** — see `patterns/PATTERNS.md` §1 — but capped at 4 tiles per slide for legibility.
5. **Two-column compare** — split panel, left forest fill, right amber fill, mint divider.
6. **Closing CTA** — large headline, single primary button.

## Auto-advance variant

Add this script if it's a kiosk:

```js
const slides = document.querySelectorAll('.slide');
let i = 0;
setInterval(() => {
  i = (i + 1) % slides.length;
  slides[i].scrollIntoView({ behavior: 'smooth' });
}, 8000);  // 8s per slide
```

## Animation per slide (entrance)

Use `IntersectionObserver` + Motion (skill: `motion`) so each slide animates only when entering view. Sample:

```js
const reveal = (el) => el.animate(
  [{ opacity: 0, transform: 'translateY(24px)' }, { opacity: 1, transform: 'none' }],
  { duration: 600, easing: 'cubic-bezier(0.2,0,0,1)', fill: 'forwards' }
);
new IntersectionObserver((entries) => entries.forEach(e => e.isIntersecting && reveal(e.target)), {
  threshold: 0.4
}).observe(...document.querySelectorAll('.slide > *'));
```

## Aspect-ratio reminders

- **Web slides default to 16:9 viewport behavior** — the snap-y model is browser-window-relative, not slide-canvas-relative. If the user wants strict 1920×1080 frames, wrap each slide in `<div class="slide-frame">` with `aspect-ratio: 16/9; max-width: 100vw; max-height: 100vh; margin: auto;` and put content inside.
- **Vertical / 9:16** — set `aspect-ratio: 9/16`. Reserve for mobile-first kiosks or social-style decks.

## When to convert to PPTX instead

If the user needs the deck **emailable, presenter-noted, or playable inside Microsoft Teams / Google Meet's slide-share UI**, build it as PPTX (see `../pptx/PPTX.md`). Scrollable HTML is best when it lives at a URL and benefits from web-only features (live charts, video embeds, hover states, scroll-linked motion).
