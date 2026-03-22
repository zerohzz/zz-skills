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
