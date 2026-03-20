# Design Principles

## Core philosophy

The interface must **clarify the article's structure**, not merely restyle its words.
Every visual and interactive decision should answer: *does this help the reader understand faster or explore deeper?*

---

## Four aesthetic directions

These are the only four directions this skill uses. Choose based on article tone.
Each maps to a concrete design system in `build_page_plan.py`.

### `dark-technical`
For developer content, system architecture, technical analysis, frameworks.

Character: precision, monospace clarity, analytical depth.
Font: IBM Plex Sans + IBM Plex Mono. Palette: dark slate + electric blue/cyan accent.
Avoids: warm tones, decorative flourishes, rounded softness.

### `editorial-ink`
For opinion pieces, essays, cultural commentary, long-form arguments.

Character: typographic authority, ink-on-paper weight, magazine density.
Font: Playfair Display + Crimson Pro. Palette: aged paper + editorial red.
Avoids: startup aesthetic, pill buttons, gradient surfaces.

### `clean-analytical`
For data-driven posts, research, comparisons, tool reviews.

Character: tabular precision, high contrast, chart-friendly, nothing decorative.
Font: Plus Jakarta Sans + Fira Code. Palette: deep slate + cyan or amber.
Avoids: rounded cards, soft shadows, anything that reduces data legibility.

### `editorial-warm`
For tutorials, case studies, personal narratives, instructional content.

Character: forward momentum, approachable warmth, milestone satisfaction.
Font: Newsreader + Nunito. Palette: warm cream + burnt orange.
Avoids: cold analytical tones, complex visual noise, multi-column density.

### `claude-like`
For conversational AI content, reflective essays, thought leadership, or anything that benefits from warm intellectual clarity and a reading-first experience.

Character: quiet confidence, warm restraint, generous whitespace, content-forward. No decoration, no noise. The design recedes completely — the reader only notices the content.
Font: Instrument Serif (display headings, italic accents) + DM Sans (body, UI). Palette: warm off-white + terracotta coral.
Accent use: sparse and deliberate — the coral accent appears only on genuinely interactive or highlighted elements, never decoratively.
Avoids: dark themes, cold grays, dense multi-column layouts, heavy shadows, flashy transitions, anything that competes with the text.

---

## What to prefer

- Strong section contrast — adjacent sections should feel visually distinct
- Decisive spacing — generous OR tight, not default middle
- Typography-led hierarchy — fonts carry more weight than boxes and borders
- Restrained motion — one well-orchestrated reveal beats ten micro-animations
- Content-first layout — the design recedes, the content advances

## What to avoid

- Generic startup landing-page aesthetic (hero → feature cards → CTA)
- Purple gradient on white background as default
- Excessive centered layouts with equal-width card grids
- Shadow-heavy surfaces that look like a Tailwind UI template
- Decorative animations with no explanatory role
- Overuse of pill buttons and badge clusters
- Shallow visual patterns that obscure rather than reveal meaning

---

## Layout composition rules

**Asymmetry is more interesting than symmetry.**
Use offset cards, diagonal breaks, varying column widths. Symmetry implies interchangeability; asymmetry implies hierarchy.

**Empty space is a design element.**
Generous padding around key statements signals importance. Do not fill every pixel.

**Color encodes meaning, not decoration.**
Use accent color only for genuinely actionable or highlighted elements. A page with three uses of the accent color is stronger than one with thirty.

**Typography contrast creates structure.**
Display font at 700–900 weight + body font at 300–400 weight creates hierarchy without boxes. A 4× size jump is more powerful than a 1.5× size jump.

---

## Motion rules

**Page load:** One staggered sequence. Elements enter from below (translateY 12–16px) with opacity 0 → 1. Delay 80–100ms between elements. Total sequence under 800ms.

**Scroll reveal:** Intersection Observer, threshold 0.1. Elements above the fold load on entry. Fire once, then unobserve — no re-animation on scroll-back.

**Interactive transitions:** 200–300ms. Use `cubic-bezier(0.34, 1.56, 0.64, 1)` for reveals (spring-like). Use `ease-out` for dismissals.

**Respect motion preferences:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Quality bar

Each section should feel designed for **this article**, not copied from a generic starter.

Ask before finalizing:
- Would a reader recognize this as belonging to this specific article?
- Does the visual hierarchy match the argument hierarchy?
- Is every interactive element earning its presence?
- Would a senior designer approve this for publication?
