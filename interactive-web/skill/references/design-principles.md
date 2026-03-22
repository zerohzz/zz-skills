# Design Principles

## Core philosophy

The interface must **clarify the article's structure**, not merely restyle its words.
Every visual and interactive decision should answer: *does this help the reader understand faster or explore deeper?*

---

## Aesthetic directions and styles

The skill has two layers of visual configuration:

1. **Aesthetic directions** — visual tokens only (palette + typography). Choose when you want precise control.
2. **Bundled styles** — rendering modes that pre-select both visual identity *and* interaction model together. Use via `--style` flag for opinionated, coherent output.

Both layers map to concrete design systems in `build_page_plan.py`.

---

### Aesthetic directions

Choose based on article tone when using legacy mode (no `--style` flag).

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

### Bundled styles (`--style` flag)

Each bundled style is a complete rendering mode: it specifies layout, typography, palette, interaction model, motion philosophy, and component behavior as a unified whole. Pass via `--style <name>` to `extract_structure.py`.

Available values: `story-scrollytelling`, `bento-analytical`, `technical-glow`, `warm-cards`, `glass-layered`

---

### `story-scrollytelling`

For narrative essays, long-form arguments, case studies with a story arc, personal histories, chronological reflections.

**Character:** Chapter rhythm, editorial gravity, prose-first. The design recedes completely to serve uninterrupted reading. No cards, no step UI — pure vertical flow with deliberate pacing.
**Font:** Cormorant Garamond (display, italic accents) + Lato (body). Palette: aged warm cream (`#f9f6f0`) + saddle brown ink (`#8b4513`).
**Layout:** Single column, 700px max-width, 6rem chapter gaps. Drop cap on first paragraph after each chapter heading.
**Preferred interaction model:** `scroll-journey` (scroll-reveal chapters, floating ToC, reading progress bar).
**Key components:** Chapter rules (decorative HR), editorial pull-quotes (border-left, no background), drop caps via CSS `::first-letter`.
**Mobile:** Body 16px, hero title clamps to 2rem, floating ToC hidden, reading progress bar stays.
**Avoids:** Cards, grids, step navigation, any modular UI that fragments the narrative. Never use for tutorials or data-heavy comparison content.

---

### `bento-analytical`

For comparison articles, tool reviews, framework breakdowns, data-rich research, "X patterns" posts.

**Character:** Modular precision, scannable tile composition, data-forward. Like a well-designed dashboard for ideas. Information lives in purposeful tiles, not flowing prose.
**Font:** Plus Jakarta Sans (display + body, geometric clarity) + Fira Code (mono). Palette: cool light gray (`#f4f6f9`) + electric blue (`#2563eb`).
**Layout:** 12-column CSS Grid, 1100px max-width, 1rem bento gap. Tiles span 6 (default), 12 (full-width), or 4 (narrow) columns.
**Preferred interaction model:** `comparison-matrix` (filter chips, expandable tiles, data rows).
**Key components:** Bento tiles (standard/wide/stat/code variants), filter chip bar, recommendation card, data rows with tabular numbers.
**Mobile:** All tiles collapse to full-width stack. Comparison shows one option at a time.
**Avoids:** Flowing prose layout, centered single column, warm serif fonts, decorative softness. Never use for personal essays or narrative content.

---

### `technical-glow`

For engineering posts, system design explainers, AI workflow articles, architecture breakdowns, code-centric content.

**Character:** Dark precision with luminous depth. Code is a first-class citizen. Panels, not pages. Low-intensity glow as emphasis, never decoration.
**Font:** IBM Plex Sans + IBM Plex Mono (same family — maximum consistency for technical scanning). Palette: deep navy-black (`#0a0e17`) + sky blue glow (`#38bdf8`).
**Layout:** Single column + optional two-panel for architecture sections (40/60 split). 960px max-width.
**Preferred interaction model:** `architecture-explainer` (panel tabs, flow walkthrough, animated step indicators).
**Key components:** Glow panels with box-shadow luminance, terminal-style section headers (`// name`), flow step indicators with glow pulse on active state, glow callout blocks.
**Motion:** Panel glow transitions (not parallax). Active step pulse animation (stops on completion). Reduced-motion: static glow values remain, all animation stops.
**Mobile:** Two-panel collapses to single column. Code blocks get horizontal scroll.
**Avoids:** Light backgrounds, serif fonts, warm palettes, rounded softness. Never use `degrade_to_static: true` content — this style requires sufficient article structure.

---

### `warm-cards`

For tutorials, how-to guides, step-by-step walkthroughs, beginner explainers, instructional content.

**Character:** Milestone satisfaction, friendly progress, mobile-first clarity. Each step is a small win. The interaction reinforces forward momentum.
**Font:** Nunito (display + body, rounded geometric sans) + Fira Code (mono). Palette: warm cream (`#fef9f4`) + warm orange (`#e96d2c`).
**Layout:** Single column, centered cards, 680px max-width. Cards are full container width with generous radius (16px).
**Preferred interaction model:** `step-sequencer` (one card at a time, animated progress tracker, completion state).
**Key components:** Step cards (active/done states), segmented progress bar, completion card with positive color, numbered pill badges, warm callout cards.
**Motion:** Card transition with spring easing. Completed card collapse to strip (56px) via `cubic-bezier(0.34,1.56,0.64,1)`. Checkmark scales in with delay. Progress segments fill on step complete.
**Mobile:** Navigation buttons become full-width. Progress shows "Step X / Y" text instead of circles.
**Avoids:** Dense multi-column layouts, dark themes, cold analytical palettes, anything that feels intimidating or enterprise-like.

---

### `glass-layered`

For concept frameworks, mental models, layered explainers, AI system overviews, overview-to-detail educational pieces.

**Character:** Spatial depth, premium clarity, layer-aware. Overview and detail coexist in the same visual space. Depth communicates hierarchy — more important content floats forward.
**Font:** Space Grotesk (display + body, geometric modern) + Space Mono (mono). Palette: deep space navy (`#060d1f`) with gradient backdrop + indigo-lavender (`#818cf8`) glass.
**Layout:** CSS Grid with named areas: overview row (`repeat(auto-fit, minmax(240px,1fr))`) + detail panel (full-width below). 1000px max-width.
**Preferred interaction model:** `concept-explorer` (click concept → detail panel crossfade, glass tab bar, depth-layer navigation).
**Key components:** Glass panels (`backdrop-filter: blur(16px)` + RGBA surface + `@supports` fallback to `surface_solid`), overview concept cards, detail panel with crossfade, glass tab bar.
**Browser fallback:** `@supports (backdrop-filter: blur(1px)) { ... }` wrapping all glass surfaces. Use `surface_solid` (`#0f1e3d`) as fallback when backdrop-filter is unavailable.
**Motion:** Overview cards enter with scale(0.96)+fade, 400ms spring easing, 80ms stagger. Detail panel crossfade: opacity + translateY(4px)→0 + blur(0→16px), 350ms. Selected card glow pulse 3s infinite (stops on deselect).
**Mobile:** Overview cards stack vertically. Sidebar disappears. Detail panel full-screen with scroll.
**Avoids:** Full-page glassmorphism overload, excessive blur, low contrast. Never use `degrade_to_static: true` content — the layered hierarchy requires sufficient article structure.

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
