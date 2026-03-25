# Component Patterns

Ready-to-use CSS and JS building blocks for the five design directions.
Reference when building artifacts — adapt tokens from `blueprint.json`.

---

## Design Token Reference: `claude-like`

Paste this into `<style>` as the base token set when using the `claude-like` direction.

```css
/* claude-like design system */
:root {
  /* Fonts */
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-body: 'DM Sans', system-ui, sans-serif;
  --font-mono: 'DM Mono', 'Fira Code', monospace;

  /* Palette */
  --bg:           #faf9f7;
  --surface:      #ffffff;
  --border:       #e8e4dc;
  --text-primary: #1a1816;
  --text-muted:   #8b8580;
  --accent:       #d97757;   /* terracotta coral — use sparingly */
  --accent-deep:  #c9622a;   /* hover / pressed state */
  --accent-soft:  #f5ede8;   /* accent tint for backgrounds */
  --positive:     #4a7c59;

  /* Spacing scale */
  --space-xs: 0.375rem;
  --space-sm: 0.75rem;
  --space-md: 1.25rem;
  --space-lg: 2rem;
  --space-xl: 3.5rem;

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
}

/* Typography */
body {
  font-family: var(--font-body);
  font-size: clamp(15px, 1.4vw, 17px);
  line-height: 1.7;
  color: var(--text-primary);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3 {
  font-family: var(--font-display);
  font-weight: 400;   /* Instrument Serif reads better at regular weight */
  line-height: 1.15;
  letter-spacing: -0.01em;
}

/* Claude-like accent rule: use only for interactive/highlighted elements */
.accent { color: var(--accent); }
.accent-bg { background: var(--accent-soft); border-left: 3px solid var(--accent); }

/* Surface card — subtle lift, no heavy shadow */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-md) var(--space-lg);
}
```

---

## Hero Section

```html
<header class="hero">
  <div class="tag">Article type · Read time</div>
  <h1 class="hero-title">Article Title</h1>
  <p class="hero-sub">Thesis or subtitle — one punchy sentence.</p>
  <div class="hero-meta">
    <span>Author</span><span>Date</span>
  </div>
</header>
```
```css
.hero { padding: 3rem 0 2.5rem; border-bottom: 1px solid var(--border); margin-bottom: 3rem; }
.tag {
  display: inline-block;
  font-family: var(--font-mono, monospace); font-size: 11px; letter-spacing: .08em;
  text-transform: uppercase; color: var(--accent);
  border: 1px solid var(--accent); border-radius: 4px;
  padding: 3px 10px; margin-bottom: 1.25rem;
}
.hero-title {
  font-family: var(--font-display); font-weight: 800;
  font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.05; margin-bottom: 1rem;
}
.hero-sub { color: var(--text-muted); font-size: 1.05rem; max-width: 56ch; margin-bottom: 1.5rem; }
.hero-meta { display: flex; gap: 1.5rem; font-size: 12px; color: var(--text-muted); font-family: var(--font-mono, monospace); }
```

---

## Sticky Progress Bar

```html
<div class="progress-bar"><div class="progress-fill" id="pbar"></div></div>
```
```css
.progress-bar { position: fixed; top: 0; left: 0; width: 100%; height: 3px; background: var(--border); z-index: 100; }
.progress-fill { height: 100%; background: var(--accent); width: 0; transition: width .15s ease; }
```
```javascript
window.addEventListener('scroll', () => {
  const pct = window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100;
  document.getElementById('pbar').style.width = Math.min(pct, 100) + '%';
}, { passive: true });
```

---

## Scroll Reveal (base)

Add `.reveal` class to any element. JS handles the rest.

```css
.reveal { opacity: 0; transform: translateY(14px); transition: opacity .5s ease, transform .5s ease; }
.reveal.visible { opacity: 1; transform: none; }
```
```javascript
// Staggered page-load
document.querySelectorAll('.reveal').forEach((el, i) => {
  setTimeout(() => el.classList.add('visible'), 100 + i * 80);
});

// Scroll reveal for deeper content
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }});
}, { threshold: 0.1 });
document.querySelectorAll('.scroll-reveal').forEach(el => obs.observe(el));
```

---

## Pull Quote

```html
<blockquote class="pull-quote">
  <p>The most memorable sentence from the article goes here.</p>
  <cite>— Context or attribution</cite>
</blockquote>
```
```css
.pull-quote {
  position: relative; border-left: 4px solid var(--accent);
  padding: 1.25rem 1.75rem; margin: 2.5rem 0;
  font-family: var(--font-display); font-size: clamp(1.1rem, 2.5vw, 1.4rem);
  font-style: italic; line-height: 1.5;
}
.pull-quote::before {
  content: '"'; position: absolute; top: -.5rem; left: 1rem;
  font-size: 5rem; line-height: 1; color: var(--accent); opacity: .2;
}
.pull-quote cite { display: block; margin-top: .75rem; font-size: .85rem; font-style: normal; color: var(--text-muted); }
```

---

## Stat Card (with count-up)

```html
<div class="stat-card">
  <div class="stat-number" data-target="847" data-suffix="%">0%</div>
  <div class="stat-label">Key metric label</div>
  <div class="stat-context">Additional context in smaller text</div>
</div>
```
```css
.stat-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; text-align: center; }
.stat-number { font-family: var(--font-display); font-size: 3.5rem; font-weight: 800; line-height: 1; color: var(--accent); font-variant-numeric: tabular-nums; }
.stat-label { font-size: 12px; color: var(--text-muted); margin-top: .5rem; font-family: var(--font-mono, monospace); letter-spacing: .04em; text-transform: uppercase; }
.stat-context { font-size: 13px; color: var(--text-muted); margin-top: .25rem; }
```
```javascript
function countUp(el, target, suffix='', duration=1500) {
  const start = performance.now();
  const tick = now => {
    const p = Math.min((now - start) / duration, 1);
    const e = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(e * target).toLocaleString() + suffix;
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
// Trigger on scroll entry
const statObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      countUp(e.target, +e.target.dataset.target, e.target.dataset.suffix || '');
      statObs.unobserve(e.target);
    }
  });
});
document.querySelectorAll('.stat-number').forEach(el => statObs.observe(el));
```

---

## Concept Accordion

```html
<div class="concept-list">
  <div class="concept" id="c-1">
    <button class="concept-head" onclick="toggleConcept('c-1')" aria-expanded="false">
      <span class="concept-dot" style="background: var(--accent)"></span>
      <span class="concept-title">Concept Name</span>
      <span class="concept-tag">Category</span>
      <span class="concept-chevron" aria-hidden="true">↓</span>
    </button>
    <div class="concept-body">
      <div class="concept-inner">Expanded explanation goes here.</div>
    </div>
  </div>
</div>
```
```css
.concept { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; margin-bottom: .5rem; }
.concept.open { border-color: var(--accent); }
.concept-head { width: 100%; display: flex; align-items: center; gap: .75rem; padding: 1rem 1.25rem; background: none; border: none; cursor: pointer; text-align: left; color: var(--text-primary); transition: background .15s; }
.concept-head:hover { background: rgba(255,255,255,.04); }
.concept-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.concept-title { flex: 1; font-weight: 500; font-size: 14px; }
.concept-tag { font-family: var(--font-mono, monospace); font-size: 10px; padding: 2px 8px; border-radius: 20px; border: 1px solid var(--border); color: var(--text-muted); }
.concept-chevron { font-size: 11px; color: var(--text-muted); transition: transform .25s ease; }
.concept.open .concept-chevron { transform: rotate(180deg); }
.concept-body { max-height: 0; overflow: hidden; transition: max-height .35s ease; }
.concept.open .concept-body { max-height: 300px; }
.concept-inner { padding: .25rem 1.25rem .9rem 2.75rem; font-size: 13.5px; color: var(--text-muted); line-height: 1.65; }
```
```javascript
function toggleConcept(id) {
  const el = document.getElementById(id);
  const isOpen = el.classList.contains('open');
  document.querySelectorAll('.concept').forEach(c => {
    c.classList.remove('open');
    c.querySelector('.concept-head').setAttribute('aria-expanded', 'false');
  });
  if (!isOpen) {
    el.classList.add('open');
    el.querySelector('.concept-head').setAttribute('aria-expanded', 'true');
  }
}
```

---

## Code Block with Copy Button

```html
<div class="code-block">
  <div class="code-header">
    <span class="code-lang">javascript</span>
    <button class="copy-btn" onclick="copyCode(this)">Copy</button>
  </div>
  <pre><code>// Your code here</code></pre>
</div>
```
```css
.code-block { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin: 1.5rem 0; }
.code-header { display: flex; justify-content: space-between; align-items: center; padding: .5rem 1rem; border-bottom: 1px solid var(--border); }
.code-lang { font-family: var(--font-mono, monospace); font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: .06em; }
.copy-btn { font-family: var(--font-mono, monospace); font-size: 11px; color: var(--text-muted); background: none; border: none; cursor: pointer; padding: 2px 8px; border-radius: 4px; transition: background .15s, color .15s; }
.copy-btn:hover { background: var(--border); color: var(--text-primary); }
pre { margin: 0; padding: 1rem; overflow-x: auto; }
code { font-family: var(--font-mono, monospace); font-size: 13px; line-height: 1.6; color: var(--text-primary); }
```
```javascript
function copyCode(btn) {
  const code = btn.closest('.code-block').querySelector('code').textContent;
  navigator.clipboard.writeText(code).then(() => {
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}
```

---

## Takeaway Grid

```html
<div class="takeaway-grid">
  <div class="takeaway">
    <div class="tk-icon">→ KEY INSIGHT</div>
    <p>The most important thing to remember from this section.</p>
  </div>
  <!-- repeat -->
</div>
```
```css
.takeaway-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: .75rem; margin-top: 1.5rem; }
.takeaway { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1.1rem 1.25rem; font-size: 13.5px; line-height: 1.6; }
.tk-icon { font-family: var(--font-mono, monospace); font-size: 10px; color: var(--accent); margin-bottom: .4rem; letter-spacing: .06em; }
```

---

## Responsive Base

```css
/* Container */
.container { max-width: 820px; margin: 0 auto; padding: 0 clamp(1rem, 5vw, 3rem); }

/* Fluid type */
html { font-size: clamp(15px, 1.5vw, 17px); }

/* Mobile overrides */
@media (max-width: 600px) {
  .hero-title { font-size: 2rem; }
  .stat-number { font-size: 2.5rem; }
  .takeaway-grid { grid-template-columns: 1fr; }
  .hero-meta { flex-direction: column; gap: .4rem; }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

---

# Bundled Style Design Tokens and Components

The five sections below define CSS tokens and key component patterns for each bundled rendering style. Use the tokens as `:root` custom properties. Components listed are those that differ meaningfully from the base `claude-like` patterns above.

---

## Design Token Reference: `story-scrollytelling`

```css
:root {
  /* Fonts */
  --font-display: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'Lato', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;

  /* Palette */
  --bg:           #f9f6f0;
  --surface:      #ffffff;
  --border:       #ddd7c8;
  --text-primary: #1c1814;
  --text-muted:   #7a7060;
  --accent:       #8b4513;
  --accent-warm:  #c8702a;
  --accent-soft:  #f5ede3;
  --positive:     #3a6b44;
  --chapter-rule: #c8b89a;
  --dropcap-bg:   #f0ead8;

  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.75rem;
  --space-lg: 3.5rem;
  --space-xl: 5rem;
  --space-chapter: 8rem;

  /* Radius — intentionally tight for editorial feel */
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-lg: 8px;
}
```

### Drop Cap

```css
.chapter-body > p:first-of-type::first-letter {
  float: left;
  font-family: var(--font-display);
  font-size: 4.5rem;
  line-height: 0.8;
  margin: 0.1rem 0.15rem 0 0;
  padding: 0.25rem 0.3rem 0.15rem;
  background: var(--dropcap-bg);
  color: var(--accent);
  font-weight: 700;
  border-radius: var(--radius-sm);
}
```

### Chapter Rule

```html
<div class="chapter-divider" role="separator" aria-hidden="true"></div>
```
```css
.chapter-divider {
  width: 60px;
  height: 2px;
  background: var(--chapter-rule);
  margin: var(--space-lg) 0 var(--space-md);
}
```

### Editorial Pull Quote

```html
<blockquote class="pull-quote">
  <p>The insight stated in its most essential form.</p>
  <cite>— Context or chapter name</cite>
</blockquote>
```
```css
.pull-quote {
  margin: var(--space-lg) 0;
  padding: var(--space-sm) 0 var(--space-sm) var(--space-md);
  border-left: 3px solid var(--accent);
  font-family: var(--font-display);
  font-style: italic;
  font-size: clamp(1.2rem, 2.2vw, 1.5rem);
  line-height: 1.5;
  color: var(--text-primary);
}
.pull-quote cite {
  display: block;
  margin-top: 0.5rem;
  font-family: var(--font-body);
  font-style: normal;
  font-size: 0.8rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-muted);
}
```

### Chapter Section (scroll-reveal, opacity only)

```css
.chapter {
  margin-bottom: var(--space-chapter);
  opacity: 0;
  transition: opacity 600ms ease;
}
.chapter.visible { opacity: 1; }
.chapter h2 {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 3vw, 2.4rem);
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: var(--space-sm);
}
```
```javascript
const chapters = document.querySelectorAll('.chapter');
const observer = new IntersectionObserver(
  (entries) => entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } }),
  { threshold: 0.08 }
);
chapters.forEach(c => observer.observe(c));
```

### Container (story mode — narrower than base)

```css
.story-container { max-width: 700px; margin: 0 auto; padding: 0 clamp(1.25rem, 5vw, 3rem); }
@media (max-width: 600px) {
  .story-container { padding: 0 1.25rem; }
  .chapter h2 { font-size: 1.6rem; }
  .pull-quote { font-size: 1.1rem; }
  .chapter-body > p:first-of-type::first-letter { font-size: 3rem; }
}
```

---

## Design Token Reference: `bento-analytical`

```css
:root {
  /* Fonts */
  --font-display: 'Plus Jakarta Sans', system-ui, sans-serif;
  --font-body:    'Plus Jakarta Sans', system-ui, sans-serif;
  --font-mono:    'Fira Code', monospace;

  /* Palette */
  --bg:           #f4f6f9;
  --surface:      #ffffff;
  --surface-alt:  #f8f9fb;
  --border:       #dde2ec;
  --border-strong:#b8bfcc;
  --text-primary: #111827;
  --text-muted:   #6b7280;
  --accent:       #2563eb;
  --accent-warm:  #f59e0b;
  --accent-soft:  #eff6ff;
  --positive:     #16a34a;
  --negative:     #dc2626;

  /* Spacing */
  --space-xs:   0.25rem;
  --space-sm:   0.5rem;
  --space-md:   1rem;
  --space-lg:   1.5rem;
  --space-xl:   2.5rem;
  --bento-gap:  1rem;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Shadows */
  --shadow-tile:       0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-tile-hover: 0 4px 12px rgba(0,0,0,0.10);
  --shadow-accent:     0 0 0 2px var(--accent), 0 4px 12px rgba(37,99,235,0.12);
}
```

### Bento Grid Layout

```html
<div class="bento-grid">
  <div class="bento-tile tile-wide"><!-- spans full row --></div>
  <div class="bento-tile"><!-- spans half --></div>
  <div class="bento-tile"><!-- spans half --></div>
  <div class="bento-tile tile-stat"><!-- small stat tile --></div>
  <div class="bento-tile tile-stat"><!-- small stat tile --></div>
  <div class="bento-tile tile-stat"><!-- small stat tile --></div>
</div>
```
```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--bento-gap);
  max-width: 1100px;
  margin: 0 auto;
}
.bento-tile {
  grid-column: span 6;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-tile);
  transition: box-shadow 180ms ease-out, transform 180ms ease-out;
}
.bento-tile:hover { box-shadow: var(--shadow-tile-hover); transform: translateY(-2px); }
.tile-wide  { grid-column: span 12; }
.tile-stat  { grid-column: span 4; }
.tile-accent { border-left: 4px solid var(--accent); background: var(--accent-soft); }
@media (max-width: 700px) {
  .bento-tile, .tile-wide, .tile-stat { grid-column: span 12; }
}
```

### Filter Chip Bar

```html
<div class="chip-bar" role="group" aria-label="Filter by category">
  <button class="chip active" onclick="filterBento(this, 'all')">All</button>
  <button class="chip" onclick="filterBento(this, 'pros')">Pros</button>
  <button class="chip" onclick="filterBento(this, 'cons')">Cons</button>
</div>
```
```css
.chip-bar { display: flex; flex-wrap: wrap; gap: .5rem; margin-bottom: var(--space-md); }
.chip {
  font-family: var(--font-body); font-size: 12px; font-weight: 600;
  padding: .3rem .85rem; border-radius: 999px;
  border: 1.5px solid var(--border); background: var(--surface);
  color: var(--text-muted); cursor: pointer;
  transition: background 150ms, color 150ms, border-color 150ms;
}
.chip.active, .chip:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
```

### Bento Tile Enter Animation (staggered by position)

```javascript
const tiles = document.querySelectorAll('.bento-tile');
tiles.forEach((tile, i) => {
  tile.style.cssText = 'opacity:0;transform:translateY(10px)';
  setTimeout(() => {
    tile.style.transition = 'opacity 350ms ease-out, transform 350ms ease-out';
    tile.style.opacity = '1';
    tile.style.transform = 'translateY(0)';
  }, i * 60);
});
```

---

## Design Token Reference: `technical-glow`

```css
:root {
  /* Fonts */
  --font-display: 'IBM Plex Sans', system-ui, sans-serif;
  --font-body:    'IBM Plex Sans', system-ui, sans-serif;
  --font-mono:    'IBM Plex Mono', monospace;

  /* Palette */
  --bg:             #0a0e17;
  --surface:        #111827;
  --surface-raised: #161f30;
  --border:         #1e2d45;
  --border-glow:    #2a4a7a;
  --text-primary:   #e2eaf8;
  --text-muted:     #6b82a8;
  --accent:         #38bdf8;
  --accent-warm:    #fb923c;
  --positive:       #4ade80;
  --negative:       #f87171;
  --code-bg:        #0d1420;
  --glow-color:     rgba(56,189,248,0.18);
  --glow-strong:    rgba(56,189,248,0.35);

  /* Spacing */
  --space-xs:    0.375rem;
  --space-sm:    0.75rem;
  --space-md:    1.25rem;
  --space-lg:    2rem;
  --space-xl:    3.5rem;
  --panel-pad:   1.5rem;

  /* Radius — precise, not soft */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Shadows / glow */
  --shadow-panel:      0 0 0 1px var(--border), 0 4px 24px rgba(0,0,0,0.4);
  --shadow-glow:       0 0 0 1px var(--border), 0 0 20px var(--glow-color);
  --shadow-glow-accent:0 0 0 1px var(--accent), 0 0 32px var(--glow-strong);
}
```

### Glow Panel

```html
<section class="glow-panel">
  <h2 class="panel-heading">// Section Name</h2>
  <div class="panel-body"><!-- content --></div>
</section>
```
```css
.glow-panel {
  background: var(--surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-panel);
  padding: var(--panel-pad);
  margin-bottom: var(--space-lg);
  transition: box-shadow 250ms ease;
}
.glow-panel:hover { box-shadow: var(--shadow-glow); }
.panel-heading {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent);
  letter-spacing: 0.04em;
  margin-bottom: var(--space-sm);
}
```

### Flow Step Indicator with Glow Pulse

```html
<div class="flow-steps">
  <div class="flow-step active" data-step="1">
    <div class="step-dot"></div>
    <span>Step label</span>
  </div>
  <!-- repeat -->
</div>
```
```css
.flow-steps { display: flex; flex-direction: column; gap: 0.75rem; }
.flow-step { display: flex; align-items: center; gap: 0.75rem; color: var(--text-muted); font-size: 0.875rem; }
.step-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--border); flex-shrink: 0;
  transition: background 300ms;
}
.flow-step.active .step-dot {
  background: var(--accent);
  animation: glow-pulse 2s ease-in-out infinite;
}
.flow-step.done .step-dot { background: var(--positive); animation: none; }
.flow-step.active { color: var(--text-primary); }
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--glow-color); }
  50%       { box-shadow: 0 0 0 6px var(--glow-color); }
}
@media (prefers-reduced-motion: reduce) {
  .flow-step.active .step-dot { animation: none; }
}
```

### Technical Code Block (dark, glow-aware)

```css
.code-block { background: var(--code-bg); border: 1px solid var(--border); border-radius: var(--radius-md); }
.code-header { border-bottom: 1px solid var(--border); }
.code-lang { color: var(--accent); }
code { color: var(--text-primary); font-size: 13px; }
```

### Glow Callout

```html
<div class="glow-callout" data-type="note">
  <span class="callout-label">→ NOTE</span>
  <p>Callout content here.</p>
</div>
```
```css
.glow-callout {
  background: var(--surface-raised);
  border-left: 3px solid var(--accent);
  border-radius: var(--radius-sm);
  padding: var(--space-sm) var(--space-md);
  margin: var(--space-md) 0;
  box-shadow: 0 0 16px var(--glow-color);
}
.glow-callout[data-type="warning"] { border-color: var(--accent-warm); box-shadow: 0 0 16px rgba(251,146,60,0.15); }
.callout-label {
  font-family: var(--font-mono); font-size: 10px;
  color: var(--accent); text-transform: uppercase;
  letter-spacing: 0.08em; display: block; margin-bottom: 0.3rem;
}
```

### Panel Enter Animation

```javascript
const panels = document.querySelectorAll('.glow-panel');
panels.forEach((panel, i) => {
  panel.style.cssText = 'opacity:0;transform:translateX(-8px)';
  setTimeout(() => {
    panel.style.transition = 'opacity 400ms cubic-bezier(0.22,1,0.36,1), transform 400ms cubic-bezier(0.22,1,0.36,1), box-shadow 250ms ease';
    panel.style.opacity = '1';
    panel.style.transform = 'translateX(0)';
  }, i * 100);
});
```

---

## Design Token Reference: `warm-cards`

```css
:root {
  /* Fonts */
  --font-display: 'Nunito', system-ui, sans-serif;
  --font-body:    'Nunito', system-ui, sans-serif;
  --font-mono:    'Fira Code', monospace;

  /* Palette */
  --bg:               #fef9f4;
  --surface:          #ffffff;
  --surface-soft:     #fdf3ea;
  --border:           #ead5c4;
  --border-active:    #e8a87c;
  --text-primary:     #2d1a0e;
  --text-muted:       #8c6652;
  --accent:           #e96d2c;
  --accent-deep:      #ea580c;
  --accent-warm:      #f4a62b;
  --accent-soft:      #fff7ed;
  --positive:         #3d7a51;
  --step-done:        #d4edda;
  --step-done-border: #a3cfb4;

  /* Spacing */
  --space-xs:  0.375rem;
  --space-sm:  0.75rem;
  --space-md:  1.25rem;
  --space-lg:  2rem;
  --space-xl:  3rem;
  --card-pad:  1.5rem 1.75rem;
  --card-gap:  1rem;

  /* Radius — friendly and generous */
  --radius-sm:   8px;
  --radius-md:   14px;
  --radius-lg:   20px;
  --radius-pill: 999px;

  /* Shadows */
  --shadow-card:        0 2px 8px rgba(233,109,44,0.08), 0 1px 3px rgba(0,0,0,0.06);
  --shadow-card-hover:  0 6px 20px rgba(233,109,44,0.14);
  --shadow-card-active: 0 0 0 3px rgba(233,109,44,0.22), 0 4px 16px rgba(0,0,0,0.08);
  --shadow-card-done:   0 1px 4px rgba(0,0,0,0.04);
}
```

### Step Card (active / done states)

```html
<div class="step-card" data-step="1" data-state="active">
  <div class="step-header">
    <span class="step-badge">1</span>
    <h3 class="step-title">Step Title</h3>
  </div>
  <div class="step-body">
    <p>Step content here.</p>
  </div>
  <div class="step-nav">
    <button class="btn-prev" onclick="prevStep()">← Back</button>
    <button class="btn-next" onclick="nextStep()">Continue →</button>
  </div>
</div>
```
```css
.step-card {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-lg);
  padding: var(--card-pad);
  box-shadow: var(--shadow-card);
  transition: box-shadow 150ms ease-out;
}
.step-card[data-state="active"] {
  border-color: var(--border-active);
  box-shadow: var(--shadow-card-active);
}
.step-card[data-state="done"] {
  background: var(--step-done);
  border-color: var(--step-done-border);
  box-shadow: var(--shadow-card-done);
  max-height: 56px;
  overflow: hidden;
  transition: max-height 350ms cubic-bezier(0.34,1.56,0.64,1);
}
.step-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: var(--radius-pill);
  background: var(--accent); color: #fff;
  font-family: var(--font-display); font-weight: 800; font-size: 13px;
}
.step-card[data-state="done"] .step-badge { background: var(--positive); }
.step-header { display: flex; align-items: center; gap: .75rem; margin-bottom: var(--space-sm); }
.step-title { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.step-nav { display: flex; justify-content: space-between; margin-top: var(--space-md); gap: .5rem; }
.btn-next, .btn-prev {
  font-family: var(--font-body); font-weight: 700; font-size: 0.875rem;
  padding: .55rem 1.25rem; border-radius: var(--radius-pill);
  border: none; cursor: pointer; transition: background 150ms, transform 100ms;
}
.btn-next { background: var(--accent); color: #fff; }
.btn-next:hover { background: var(--accent-deep); }
.btn-prev { background: var(--surface); border: 1.5px solid var(--border); color: var(--text-muted); }
@media (max-width: 600px) {
  .step-nav { flex-direction: column-reverse; }
  .btn-next, .btn-prev { width: 100%; text-align: center; }
}
```

### Segmented Progress Tracker

```html
<div class="progress-track" role="progressbar" aria-valuenow="2" aria-valuemax="5" aria-label="Step 2 of 5">
  <div class="progress-segment done"></div>
  <div class="progress-segment active"></div>
  <div class="progress-segment"></div>
  <div class="progress-segment"></div>
  <div class="progress-segment"></div>
</div>
```
```css
.progress-track {
  display: flex; gap: 4px;
  margin: var(--space-md) 0;
}
.progress-segment {
  flex: 1; height: 4px; border-radius: 2px;
  background: var(--border);
  transition: background 400ms ease;
}
.progress-segment.done   { background: var(--positive); }
.progress-segment.active { background: var(--accent); }
```

---

## Design Token Reference: `glass-layered`

```css
:root {
  /* Fonts */
  --font-display: 'Space Grotesk', system-ui, sans-serif;
  --font-body:    'Space Grotesk', system-ui, sans-serif;
  --font-mono:    'Space Mono', monospace;

  /* Palette */
  --bg:             #060d1f;
  --bg-gradient:    linear-gradient(135deg, #060d1f 0%, #0d1a38 50%, #070e22 100%);
  --surface:        rgba(255,255,255,0.06);
  --surface-strong: rgba(255,255,255,0.10);
  --surface-solid:  #0f1e3d;   /* fallback when backdrop-filter unavailable */
  --border:         rgba(255,255,255,0.12);
  --border-strong:  rgba(255,255,255,0.22);
  --text-primary:   #eef2ff;
  --text-muted:     #8896b8;
  --accent:         #818cf8;
  --accent-warm:    #f472b6;
  --positive:       #34d399;
  --glass-tint:     rgba(129,140,248,0.08);
  --glass-blur:     16px;

  /* Spacing */
  --space-xs:   0.5rem;
  --space-sm:   1rem;
  --space-md:   1.5rem;
  --space-lg:   2.5rem;
  --space-xl:   4rem;
  --layer-gap:  1.5rem;

  /* Radius */
  --radius-sm:    8px;
  --radius-md:    16px;
  --radius-lg:    24px;
  --radius-panel: 20px;

  /* Shadows */
  --shadow-glass:       0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.08);
  --shadow-glass-hover: 0 8px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.14);
  --shadow-accent-glow: 0 0 40px rgba(129,140,248,0.20);
}
```

### Glass Panel (with browser fallback)

```html
<div class="glass-panel">
  <!-- content -->
</div>
```
```css
/* Base — works everywhere */
.glass-panel {
  background: var(--surface-solid);
  border: 1px solid var(--border);
  border-radius: var(--radius-panel);
  padding: var(--space-md);
  box-shadow: var(--shadow-glass);
  transition: box-shadow 200ms ease, border-color 200ms ease;
}
/* Progressive enhancement — glass effect when supported */
@supports (backdrop-filter: blur(1px)) {
  .glass-panel {
    background: var(--surface);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
  }
}
.glass-panel:hover { box-shadow: var(--shadow-glass-hover); border-color: var(--border-strong); }
```

### Overview Concept Cards

```html
<div class="overview-grid">
  <button class="concept-card" onclick="selectConcept(this, 'concept-1')" aria-pressed="true">
    <span class="concept-index">01</span>
    <h3 class="concept-title">Concept Name</h3>
    <p class="concept-preview">Short descriptor (one sentence).</p>
  </button>
  <!-- repeat 3–6 more -->
</div>
```
```css
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--layer-gap);
  margin-bottom: var(--space-lg);
}
.concept-card {
  background: var(--surface-solid);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: var(--space-md);
  text-align: left; cursor: pointer;
  box-shadow: var(--shadow-glass);
  transition: box-shadow 200ms ease, border-color 200ms ease, transform 200ms cubic-bezier(0.34,1.56,0.64,1);
}
@supports (backdrop-filter: blur(1px)) {
  .concept-card { background: var(--surface); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
}
.concept-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-glass-hover); }
.concept-card[aria-pressed="true"] {
  border-color: var(--accent);
  box-shadow: var(--shadow-accent-glow), var(--shadow-glass);
  animation: glow-breathe 3s ease-in-out infinite;
}
.concept-index { font-family: var(--font-mono); font-size: 11px; color: var(--accent); display: block; margin-bottom: .4rem; }
.concept-title  { font-size: 1rem; font-weight: 600; color: var(--text-primary); margin-bottom: .4rem; }
.concept-preview{ font-size: 0.8rem; color: var(--text-muted); line-height: 1.5; }
@keyframes glow-breathe {
  0%, 100% { box-shadow: var(--shadow-accent-glow), var(--shadow-glass); }
  50%       { box-shadow: 0 0 60px rgba(129,140,248,0.35), var(--shadow-glass); }
}
@media (prefers-reduced-motion: reduce) {
  .concept-card[aria-pressed="true"] { animation: none; }
}
```

### Detail Panel with Crossfade

```html
<div class="detail-panel glass-panel" id="detail-panel" aria-live="polite">
  <div class="detail-content" id="detail-content">
    <!-- content swapped by JS -->
  </div>
</div>
```
```css
.detail-panel { min-height: 200px; }
.detail-content {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 350ms ease, transform 350ms ease;
}
.detail-content.exiting {
  opacity: 0;
  transform: translateY(4px);
}
```
```javascript
function selectConcept(card, conceptId) {
  // Update aria-pressed states
  document.querySelectorAll('.concept-card').forEach(c => c.setAttribute('aria-pressed', 'false'));
  card.setAttribute('aria-pressed', 'true');

  const content = document.getElementById('detail-content');
  content.classList.add('exiting');

  setTimeout(() => {
    content.innerHTML = conceptData[conceptId]; // pre-built content map
    content.classList.remove('exiting');
  }, 350);
}
```

### Page Backdrop

```css
body {
  background: var(--bg);
  background-image: var(--bg-gradient);
  min-height: 100vh;
  color: var(--text-primary);
  font-family: var(--font-body);
}
```

### Mobile Adaptation

```css
@media (max-width: 700px) {
  .overview-grid { grid-template-columns: 1fr; }
  .detail-panel { border-radius: var(--radius-md); }
  .glass-panel { padding: var(--space-sm); }
}
```
