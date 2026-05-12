# Chememan Design Patterns

Higher-order layouts assembled from the `components/` primitives. Use these as starting points — don't redesign the wheel for each landing page or slide.

## Section-rhythm rule

A landing page or deck shouldn't be all dark glass or all white editorial. Alternate to give the eye breaks and signal tonal shifts:

```
HERO (dark mesh + glass)
  ↓
STORY PANEL (large bright-frost glass over a tri-color bg)   ← §0a
  ↓
BENTO BAND (tri-color tinted glass tiles)                     ← §1
  ↓
CLEAN EDITORIAL (off-white, oversized FC Minimal, hairlines)  ← §0b
  ↓
FOOTER (deep navy + sky stripe)
```

Two new "tone-break" patterns are at the top because they get used between every other pattern.

## §0a — Story panel (large glass over color)

**Use when**: a section has prose / multi-paragraph text and you want it to read cleanly above a colored or mesh background. The big bright-frost glass panel is a readability container. Avoids the "wall of white text on a mesh gradient" problem.

```html
<section style="
    padding: 120px 24px;
    background:
      radial-gradient(at 30% 20%, rgba(0,82,44,.50) 0%, transparent 55%),
      radial-gradient(at 75% 80%, rgba(60,96,165,.55) 0%, transparent 55%),
      radial-gradient(at 50% 50%, rgba(116,80,33,.30) 0%, transparent 60%),
      #050E1A;">
  <article class="cman-glass-heavy" style="
      max-width: 1080px; margin: 0 auto;
      padding: clamp(40px, 6vw, 80px);
      border-radius: var(--cman-r-3xl);">
    <p class="cman-eyebrow" style="color: var(--cman-sky);">The Chememan story</p>
    <h2 class="cman-h1" style="margin-top:1rem;">From a single kiln to Southeast Asia's lime backbone.</h2>

    <div style="display:grid; gap:48px; margin-top:40px;
                grid-template-columns: 1fr 1.4fr;">
      <p class="cman-lead" style="border-left: 2px solid rgba(94,205,246,.5); padding-left: 24px;">
        We didn't set out to be the biggest. We set out to be the cleanest, the most reliable…
      </p>
      <div class="cman-body" style="line-height: 1.7;">
        <p>Founded in 1989…</p>
        <p style="margin-top:1.25em;">Our roadmap to 2030…</p>
      </div>
    </div>
  </article>
</section>
```

**Notes**
- Use `cman-glass-heavy` (not `cman-glass`) for prose-heavy panels. The extra opacity (28% white vs 18%) keeps small body text legible against busy backgrounds without losing the see-through quality.
- Border-radius: `--cman-r-3xl` (48px) for hero-scale panels. Smaller panels can use `--cman-r-2xl`.
- Two-column layout (`1fr 1.4fr`) — short editorial lead on the left, longer prose on the right. The lead carries a sky-blue left rule as a tonal accent.

## §0b — Clean editorial section (Levels / Yucca aesthetic)

**Use when**: you need a tonal break from dense colorful content. References: [levels.com](https://www.levels.com/), [yucca.co.za](https://yucca.co.za/). Big oversized type, off-white background, generous whitespace, subtle hairlines, brand color appearing only as small accents (left squares, italic words, big-stat numbers).

```html
<section style="background:#F7F5F0; color:#001008; padding: clamp(96px,14vh,200px) 24px; position:relative;">
  <div style="max-width:1280px; margin:0 auto; position:relative;">

    <!-- Tiny section number (top-right, like Yucca) -->
    <span style="position:absolute; top:-12px; right:0; font-size:.75rem; font-weight:500;
                 letter-spacing:.16em; text-transform:uppercase; color:rgba(0,16,8,.40);">
      — Section 03 / 05
    </span>

    <!-- Top hairline -->
    <div style="height:1px; width:100%; background:rgba(0,16,8,.12); margin-bottom:64px;"></div>

    <!-- Eyebrow with color square -->
    <span style="display:inline-flex; align-items:center; gap:12px;
                 font-weight:600; font-size:.75rem; letter-spacing:.16em;
                 text-transform:uppercase; color: var(--cman-forest);">
      <span style="width:10px; height:10px; background:var(--cman-forest); border-radius:2px;"></span>
      Why it matters
    </span>

    <!-- Editorial split: oversized headline + meta column -->
    <div style="display:grid; grid-template-columns: 1.2fr 1fr; gap:96px; margin-top:32px;">
      <div>
        <h2 class="cman-h1" style="font-size: clamp(2.5rem, 6vw, 5.5rem); line-height:1.02; letter-spacing:-.04em;">
          Lime is the <em style="font-style:normal; color:var(--cman-blue);">silent chemistry</em> behind everything modern industry builds.
        </h2>
        <p class="cman-lead" style="max-width:28rem; margin-top:32px; color:#2C3833;">
          Steel needs it. Water needs it. Semiconductors, sugar, paper, soil, and concrete all need it.
        </p>
      </div>

      <div>
        <!-- Meta grid (founded / listed / HQ / plants) -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:32px;
                    padding-top:24px; border-top:1px solid rgba(0,16,8,.12);">
          <div>
            <p style="font-size:.7rem; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:rgba(0,16,8,.55);">Founded</p>
            <p style="margin-top:8px; font-weight:800; font-size:2.25rem; color:var(--cman-forest); letter-spacing:-.02em;">1989</p>
          </div>
          <div>
            <p style="font-size:.7rem; font-weight:600; letter-spacing:.16em; text-transform:uppercase; color:rgba(0,16,8,.55);">Listed</p>
            <p style="margin-top:8px; font-weight:800; font-size:2.25rem; color:var(--cman-blue); letter-spacing:-.02em;">CMAN</p>
          </div>
        </div>

        <!-- Big editorial stats -->
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:48px; margin-top:48px;">
          <div>
            <p style="font-weight:900; font-size:5rem; line-height:1; letter-spacing:-.04em; color:var(--cman-forest);">99.7%</p>
            <p style="margin-top:12px; color:rgba(0,16,8,.65); line-height:1.5;">Quicklime purity, monitored by AI vision.</p>
          </div>
          <div>
            <p style="font-weight:900; font-size:5rem; line-height:1; letter-spacing:-.04em; color:var(--cman-amber);">12</p>
            <p style="margin-top:12px; color:rgba(0,16,8,.65); line-height:1.5;">Export markets, across heavy industry and food-grade.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom hairline -->
    <div style="height:1px; width:100%; background:rgba(0,16,8,.12); margin-top:96px;"></div>
  </div>
</section>
```

**Recipe ingredients (don't drop any of these)**
- Background `#F7F5F0` (warm off-white — softer than pure white).
- Section number top-right, lowercase em-dash prefix, ~40% opacity.
- Hairline above and below (`rgba(0,16,8,0.12)`, 1px).
- Eyebrow with a 10×10 brand-color square as a bullet.
- Massive headline: `font-size: clamp(2.5rem, 6vw, 5.5rem)`, `letter-spacing: -0.04em`, weight 900. **One italic phrase tinted blue** (Yucca-style emphasis).
- Editorial split: `1.2fr 1fr` headline+lead on left, meta+stats on right. Generous gap (96px desktop).
- Big-stat numbers in **forest** AND **amber** (rotation matters — never make all stats green).
- Body color `#2C3833` for warmth, not pure black.

**When NOT to use**: investor decks where the dark stack is the brand voice; product detail pages that need imagery to dominate. This pattern is best for "about / story / why-us" interludes.

## Section-rhythm checklist

- [ ] No section longer than 100vh of body copy without a glass panel or hairline break.
- [ ] At least one §0b clean editorial section in any landing page over 4 sections — gives the eye a rest.
- [ ] At least one §0a glass story panel in any deck over 5 slides — same reason.
- [ ] No two adjacent sections share the same background tone (don't stack two dark mesh sections back-to-back).

## 1. Bento grid (mixed-size cards)

The user's `Reviews` reference is the canonical bento layout: heterogeneous card sizes, each with rounded corners and either glass or color tint, packed without gutters that get visually loud.

```html
<section class="bg-cman-grad-hero-mesh py-24 text-white">
  <div class="mx-auto grid max-w-7xl gap-4 px-6 md:grid-cols-4 md:grid-rows-3 md:auto-rows-fr">
    <!-- Hero tile (2x2) -->
    <div class="cman-glass-dark md:col-span-2 md:row-span-2 rounded-cman-2xl p-8">
      <p class="cman-eyebrow text-cman-mint">Why Chememan</p>
      <h2 class="cman-h1 mt-4">35 years of industrial chemistry, refined.</h2>
    </div>
    <!-- Stat -->
    <div class="cman-glass-dark md:col-span-1 md:row-span-1 rounded-cman-xl p-6">
      <p class="cman-display text-cman-mint" style="font-size:3rem">99.7%</p>
      <p class="cman-caption mt-1 text-white/60">Purity</p>
    </div>
    <!-- Image card -->
    <div class="md:col-span-1 md:row-span-2 rounded-cman-xl bg-cman-forest-700 p-1">
      <img src="..." class="h-full w-full rounded-cman-lg object-cover"/>
    </div>
    <!-- Quote -->
    <div class="cman-glass-brand md:col-span-2 md:row-span-1 rounded-cman-xl p-6">
      <p class="cman-lead italic">"Lime is the silent ingredient in modern industry."</p>
      <p class="cman-caption mt-3 text-white/60">— CEO, Chememan</p>
    </div>
  </div>
</section>
```

## 2. Scroll-snap full-viewport sections (HTML "slide" deck)

For converting a deck-style narrative into a scrollable HTML page where each section is a full viewport pane:

```html
<main class="snap-y snap-mandatory h-screen overflow-y-auto">
  <section class="snap-start h-screen flex items-center justify-center bg-cman-grad-hero-mesh text-white">
    <div class="text-center">
      <p class="cman-eyebrow text-cman-mint">SLIDE 01</p>
      <h1 class="cman-display mt-6">The lime behind everything.</h1>
    </div>
  </section>
  <section class="snap-start h-screen flex items-center bg-white text-cman-forest-900 px-12">
    <div class="max-w-4xl">
      <h2 class="cman-h1">A 35-year story.</h2>
      <p class="cman-lead mt-6 text-cman-charcoal">Founded in 1989, Chememan grew alongside Thailand's industrial transformation…</p>
    </div>
  </section>
  <!-- repeat per slide -->
</main>
```

Pair with `motion` skill for entrance animations triggered by `IntersectionObserver` per slide.

## 3. Stat row (3 or 4 columns)

```html
<section class="border-y border-cman-border bg-cman-bg py-16">
  <dl class="mx-auto grid max-w-6xl grid-cols-2 gap-8 px-6 md:grid-cols-4">
    <div>
      <dt class="cman-caption text-cman-fg-muted">Tonnes / year</dt>
      <dd class="cman-h1 mt-2 bg-cman-grad-forest-amber bg-clip-text text-transparent">1.2M</dd>
    </div>
    <!-- ...repeat -->
  </dl>
</section>
```

## 4. Split feature row (alternating left/right)

```html
<section class="mx-auto grid max-w-7xl gap-16 px-6 py-24 md:grid-cols-2 md:items-center">
  <div>
    <p class="cman-eyebrow text-cman-forest">Sustainability</p>
    <h2 class="cman-h1 mt-4 text-cman-forest-900">Toward net-negative lime.</h2>
    <p class="cman-lead mt-6 text-cman-charcoal">Our 2030 roadmap…</p>
    <a href="#" class="mt-8 inline-flex rounded-cman-lg bg-cman-forest px-6 py-3 font-cman font-semibold text-white">Read the roadmap →</a>
  </div>
  <div class="relative">
    <img src="..." class="rounded-cman-2xl shadow-cman-xl"/>
    <div class="cman-glass-tinted absolute -bottom-6 -left-6 rounded-cman-xl p-4">
      <p class="cman-caption text-cman-forest">↓ 42% CO₂ since 2020</p>
    </div>
  </div>
</section>
```

## 5. Logo-clear hero (when the brand mascot is the focal)

The Chememan character (snowman in green cap) is high personality. Use it as a hero element on internal/employee-facing pages (e.g. `proj_cmanai`), but **avoid it on investor/B2B contexts** — it reads as informal there. The corporate film aesthetic (`proj_chememan`) explicitly excludes the mascot for that reason.

```html
<section class="grid items-center gap-12 bg-white px-6 py-24 md:grid-cols-2">
  <div>
    <p class="cman-eyebrow text-cman-amber">Internal AI</p>
    <h1 class="cman-h1 mt-4 text-cman-forest-900">Meet your new co-worker.</h1>
    <p class="cman-lead mt-6 text-cman-charcoal">CMAN AI helps every team move faster — from procurement to plant ops.</p>
  </div>
  <img src="/design-system/chememan/assets/characters/chememan-character.png" alt="" class="mx-auto w-80"/>
</section>
```

## 6. Dark-mode stack (investor / corporate film vibe)

For stakeholder-facing surfaces — uses the obsidian background, jade glow, and **no mascot, no warm lighting** (per the project memory `feedback_aesthetic_clean_minimal`):

```html
<body data-theme="dark" class="bg-cman-forest-900 text-white">
  <section class="bg-cman-grad-midnight py-32">
    <div class="mx-auto max-w-5xl px-6 text-center">
      <h1 class="cman-display bg-gradient-to-br from-white via-cman-mint to-cman-emerald bg-clip-text text-transparent">
        SET:CMAN
      </h1>
      <p class="cman-lead mt-8 text-white/70">Public, profitable, planet-aware industrial chemistry.</p>
    </div>
  </section>
</body>
```
