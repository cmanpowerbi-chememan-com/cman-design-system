# Chememan Modern Components

Each component is **token-driven**: do not hard-code colors, radii, or shadows. Reach into `tokens/tokens.css` (CSS custom properties) or the `tailwind.preset.js` extension. The default visual language is:

- **Working primary palette = green + blue + brown.** Rotate across the three so a layout doesn't feel mono-chromatic. Forest / Blue / Amber are equal-weight primaries.
- Rounded corners: **`--cman-r-lg` (16px)** for inputs/buttons, **`--cman-r-xl` (24px)** for cards, **`--cman-r-2xl` (32px)** for hero panels.
- Layered soft shadows + a forest / blue / amber glow on emphasis surfaces (`--cman-sh-glow-forest`, `--cman-sh-glow-blue`, `--cman-sh-glow-amber`).
- **Glassmorphism = bright frosted white** (~18% white tint + bright top inset highlight + 24px blur). Text stays readable; colors behind bleed through softly. See "Glass recipe" below.
- Type uses the FC Minimal scale from `typography/TYPOGRAPHY.md`.

## Glass recipe (canonical)

Apply via the utility classes from `tokens.css`:

| Class                       | Use                                                                  |
|-----------------------------|----------------------------------------------------------------------|
| `.cman-glass`               | **Default.** Bright white frost on dark/colorful backgrounds.        |
| `.cman-glass-heavy`         | Same recipe, more opaque (28% white) — busy backgrounds, full nav.   |
| `.cman-glass-light`         | Frosted on light backgrounds. Use dark text.                         |
| `.cman-glass-tint-forest`   | Adds a 10% green wash to the white frost.                            |
| `.cman-glass-tint-blue`     | Adds a 15% blue wash. **Use blue tint at least once per layout.**    |
| `.cman-glass-tint-amber`    | Adds a 15% brown wash.                                               |

The recipe under each class is identical in structure — only the wash color and the glow shadow differ. **Never** drop below ~15% white alpha or the glass collapses into a thin grey panel.

> Snippets below are **HTML + Tailwind** (preferred), but a vanilla-CSS variant works the same — Tailwind classes map directly to the CSS variables in `tokens.css`.

---

## Button

Primary CTA fills with brand forest; secondary/ghost variants stay neutral so the forest only screams when needed (the brand book treats forest as the focal — too many forest fills numb its impact).

```html
<!-- Primary -->
<button class="inline-flex items-center gap-2 rounded-cman-lg bg-cman-forest px-6 py-3
               font-cman font-semibold text-white shadow-cman-md
               transition duration-cman-base ease-cman-spring
               hover:-translate-y-0.5 hover:shadow-cman-glow-forest
               focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
               focus-visible:outline-cman-mint">
  Get started
  <svg class="h-4 w-4" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2">
    <path d="M3 8h10M9 4l4 4-4 4"/>
  </svg>
</button>

<!-- Secondary (glass on dark hero) -->
<button class="cman-glass-dark inline-flex items-center gap-2 rounded-cman-lg px-6 py-3
               font-cman font-medium text-white/90 hover:bg-white/15">
  Learn more
</button>

<!-- Tertiary / link -->
<button class="font-cman font-semibold text-cman-forest underline-offset-4 hover:underline">
  Contact sales →
</button>
```

**Sizes**: sm `py-2 px-4 text-sm` · md `py-3 px-6` (default) · lg `py-4 px-8 text-lg`.
**Don't**: never use the secondary palette for a primary CTA. Brand CTAs are forest. Coral/amber CTAs are reserved for destructive/secondary contexts.

---

## Card

Three variants matching the user's reference deck (bento, glass, content).

### Glass card (modern, default — bright frost)
```html
<!-- Plain frost — works on any colorful/dark background -->
<div class="cman-glass rounded-cman-xl p-6">
  <p class="cman-eyebrow text-cman-sky">Capability</p>
  <h3 class="cman-h3 mt-2">Continuous AI</h3>
  <p class="mt-3 text-white/85 cman-body">
    Models that learn from your operations data — without leaving the plant network.
  </p>
</div>
```

### Brand-tinted glass cards (rotate forest / blue / amber across a layout)

```html
<!-- Forest tint — heritage, sustainability, nature -->
<div class="cman-glass-tint-forest rounded-cman-xl p-6">
  <p class="cman-eyebrow text-cman-mint">Heritage</p>
  <h3 class="cman-h3 mt-2">35 years of refined chemistry.</h3>
</div>

<!-- Blue tint — tech, digital, data -->
<div class="cman-glass-tint-blue rounded-cman-xl p-6">
  <p class="cman-eyebrow text-cman-sky">Digital</p>
  <h3 class="cman-h3 mt-2">AI-monitored kilns at every plant.</h3>
</div>

<!-- Amber tint — earth, mascot, warm editorial -->
<div class="cman-glass-tint-amber rounded-cman-xl p-6">
  <p class="cman-eyebrow" style="color:#E1B86B">Earth</p>
  <h3 class="cman-h3 mt-2">↓ 42% CO₂ since 2020.</h3>
</div>
```

### Stat card (bento)
```html
<div class="cman-glass rounded-cman-xl p-8">
  <p class="cman-display text-cman-sky" style="font-size:clamp(3rem,6vw,5rem)">320M+</p>
  <p class="cman-caption mt-2 text-white/75 uppercase tracking-widest">tonnes processed</p>
</div>
```

### Solid content card (light page)
```html
<article class="rounded-cman-xl bg-white p-6 shadow-cman-md transition hover:shadow-cman-lg">
  <img src="..." alt="" class="rounded-cman-md aspect-video object-cover w-full"/>
  <p class="cman-eyebrow mt-4 text-cman-forest">Sustainability</p>
  <h3 class="cman-h3 mt-2 text-cman-forest-900">Carbon-negative lime by 2030</h3>
  <p class="cman-body mt-3 text-cman-charcoal">Our roadmap to net-negative cement-grade lime.</p>
</article>
```

---

## Navbar

Sticky glass nav over a hero gradient — matches the `Innovate Without Limits` reference. Logo lockup left, nav center, primary CTA right.

```html
<header class="sticky top-0 z-30 backdrop-blur-cman-lg">
  <nav class="cman-glass mx-auto mt-4 flex max-w-7xl items-center justify-between
              rounded-cman-2xl px-6 py-3">
    <a href="/" class="flex items-center gap-3">
      <img src="/design-system/chememan/assets/logo/chememan-full-logo.png"
           alt="Chememan — Human Chemical" class="h-9 w-auto"/>
    </a>
    <ul class="hidden md:flex items-center gap-8 cman-caption text-white/80">
      <li><a href="#" class="hover:text-white">Products</a></li>
      <li><a href="#" class="hover:text-white">Sustainability</a></li>
      <li><a href="#" class="hover:text-white">Investors</a></li>
      <li><a href="#" class="hover:text-white">Careers</a></li>
    </ul>
    <a href="#contact" class="rounded-cman-lg bg-cman-mint px-5 py-2.5 font-cman font-semibold
                              text-cman-forest-900 shadow-cman-glow-forest transition hover:bg-white">
      Contact us
    </a>
  </nav>
</header>
```

**Logo clear-space**: per CI book, the X-height (the "N" of CHEMEMAN) of the logo is the minimum padding around it. The `px-6 py-3` on the nav already satisfies this for an `h-9` (~36px) lockup.

---

## Hero

Full-bleed gradient mesh, eyebrow → display headline → lead → dual CTA → stat row.

```html
<section class="relative overflow-hidden bg-cman-grad-hero-mesh text-white">
  <div class="mx-auto max-w-7xl px-6 pt-32 pb-24 md:pt-40">
    <p class="cman-eyebrow text-cman-mint">Human Chemical for a Better Future</p>
    <h1 class="cman-display mt-6 max-w-4xl bg-gradient-to-br from-white via-cman-mint to-cman-emerald
               bg-clip-text text-transparent">
      Industrial chemistry,<br/>built for what's next.
    </h1>
    <p class="cman-lead mt-8 max-w-2xl text-white/75">
      Chememan is Thailand's leading lime producer — quietly powering steel, sugar, water, and
      semiconductor industries across Asia.
    </p>
    <div class="mt-10 flex flex-wrap items-center gap-4">
      <a href="#" class="rounded-cman-lg bg-cman-mint px-7 py-3.5 font-cman font-semibold
                         text-cman-forest-900 shadow-cman-glow-forest transition hover:scale-[1.02]">
        Explore products
      </a>
      <a href="#" class="cman-glass-dark rounded-cman-lg px-7 py-3.5 font-cman font-medium">
        Investor relations
      </a>
    </div>

    <!-- Stat row — rotates green / blue / brown / blue glow across stats -->
    <dl class="mt-20 grid grid-cols-2 gap-4 md:grid-cols-4">
      <div class="cman-glass rounded-cman-xl p-6">
        <dt class="cman-caption text-white/75">Years operating</dt>
        <dd class="cman-h2 mt-2 text-cman-mint">35+</dd>
      </div>
      <div class="cman-glass rounded-cman-xl p-6">
        <dt class="cman-caption text-white/75">Plants</dt>
        <dd class="cman-h2 mt-2 text-cman-sky">5</dd>
      </div>
      <div class="cman-glass rounded-cman-xl p-6">
        <dt class="cman-caption text-white/75">Tonnes / year</dt>
        <dd class="cman-h2 mt-2" style="color:#E1B86B">1.2M</dd>
      </div>
      <div class="cman-glass rounded-cman-xl p-6">
        <dt class="cman-caption text-white/75">Countries shipped</dt>
        <dd class="cman-h2 mt-2 text-cman-sky">12</dd>
      </div>
    </dl>
  </div>

  <!-- Optional: character mascot floating on top-right -->
  <img src="/design-system/chememan/assets/characters/chememan-character.png"
       alt="" aria-hidden="true"
       class="pointer-events-none absolute -right-8 top-12 hidden w-72 opacity-90 md:block"/>
</section>
```

---

## Modal

Glass dialog over a darkened scrim. Use for form submission, video player, image lightbox.

```html
<div class="fixed inset-0 z-40 grid place-items-center bg-cman-forest-900/70 p-4 backdrop-blur-cman-md">
  <div role="dialog" aria-modal="true"
       class="cman-glass-heavy w-full max-w-lg rounded-cman-2xl p-8 shadow-cman-2xl">
    <h2 class="cman-h2">Request a quote</h2>
    <p class="cman-body mt-3 text-white/75">Tell us your industry and tonnage.</p>
    <form class="mt-6 grid gap-4">
      <input type="email" placeholder="Work email"
             class="rounded-cman-lg border border-white/10 bg-white/5 px-4 py-3 placeholder:text-white/50
                    focus:border-cman-mint focus:outline-none focus:ring-2 focus:ring-cman-mint/40"/>
      <textarea rows="4" placeholder="Project details"
             class="rounded-cman-lg border border-white/10 bg-white/5 px-4 py-3 placeholder:text-white/50
                    focus:border-cman-mint focus:outline-none focus:ring-2 focus:ring-cman-mint/40"></textarea>
      <button class="rounded-cman-lg bg-cman-mint px-6 py-3 font-cman font-semibold
                     text-cman-forest-900 hover:bg-white">Send</button>
    </form>
  </div>
</div>
```

---

## Footer

```html
<footer class="border-t border-cman-border bg-cman-forest-900 text-white">
  <div class="mx-auto grid max-w-7xl gap-12 px-6 py-16 md:grid-cols-4">
    <div>
      <img src="/design-system/chememan/assets/logo/chememan-full-logo.png" alt="Chememan" class="h-10"/>
      <p class="cman-caption mt-4 text-white/60">Human Chemical for a Better Future</p>
    </div>
    <div>
      <p class="cman-eyebrow text-cman-mint">Products</p>
      <ul class="mt-4 space-y-2 cman-body text-white/75">
        <li><a href="#">Quick lime</a></li>
        <li><a href="#">Hydrated lime</a></li>
        <li><a href="#">Calcium carbonate</a></li>
      </ul>
    </div>
    <div>
      <p class="cman-eyebrow text-cman-mint">Company</p>
      <ul class="mt-4 space-y-2 cman-body text-white/75">
        <li><a href="#">About</a></li>
        <li><a href="#">Sustainability</a></li>
        <li><a href="#">Investors</a></li>
      </ul>
    </div>
    <div>
      <p class="cman-eyebrow text-cman-mint">Contact</p>
      <p class="mt-4 cman-body text-white/75">SET: CMAN<br/>Bangkok, Thailand</p>
    </div>
  </div>
  <div class="border-t border-white/10">
    <p class="mx-auto max-w-7xl px-6 py-6 cman-caption text-white/50">
      © Chememan Public Company Limited. All rights reserved.
    </p>
  </div>
</footer>
```

---

## Form input

```html
<label class="block">
  <span class="cman-caption text-cman-fg-muted">Email</span>
  <input type="email"
         class="mt-2 block w-full rounded-cman-lg border border-cman-border bg-white px-4 py-3
                font-cman text-cman-forest-900 transition
                focus:border-cman-forest focus:outline-none focus:ring-2 focus:ring-cman-forest/30
                aria-[invalid=true]:border-cman-coral aria-[invalid=true]:ring-cman-coral/30" />
</label>
```

---

## Component checklist (quality gate)

Before shipping any UI built from this system, verify:

- [ ] **Tri-color rotation**: green + blue + brown all appear at least once. A layout that uses only forest+amber has left blue out — add a `cman-glass-tint-blue` tile, a sky-colored stat number, or a blue-amber gradient CTA.
- [ ] Brand color **forest is used at most twice as a saturated fill per viewport** (logo + 1 emphasis surface). Anything else is glass or neutral.
- [ ] Logo retains **clear-space ≥ X-height** (don't crowd it with body copy).
- [ ] Logo never appears on **busy/photographic backgrounds** without a glass surface or solid panel underneath.
- [ ] Headlines use **FC Minimal weight 700–900**, body uses **400**. No light weights for body.
- [ ] **Glass surfaces use the bright-frost recipe** (≥ 15% white tint + bright top inset highlight + 24px blur). No `rgba(255,255,255,0.06)` "ghost" cards.
- [ ] **Glass needs something colorful behind it** — gradient, image, mesh — otherwise it collapses into grey.
- [ ] **Border-radius is tokenized** (`--cman-r-lg/xl/2xl`). No `border-radius: 13px` ad-hoc values.
- [ ] **Motion respects `prefers-reduced-motion`**. The token CSS already zeroes durations when set; don't override with hardcoded ms.
- [ ] **Contrast**: White-on-forest ≥ 7:1 (AAA). Forest-on-white = perfect AAA. Mint-on-forest passes for body but check headings. White text on bright-frost glass is fine **only** when the layer behind the glass is dark — verify before shipping.
