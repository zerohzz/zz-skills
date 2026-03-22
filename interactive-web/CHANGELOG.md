# Changelog

All notable changes to `interactive-web` will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

---

## [1.2.0] — 2026-03-21

### Added

- **5 bundled visual styles** via `--style` flag — each pre-selects a visual identity, layout philosophy, and interaction model as a single rendering mode:
  - `story-scrollytelling` — Cormorant Garamond + Lato, single-column chapter rhythm, drop caps, opacity-only scroll reveal, editorial pull-quotes. For narrative essays and long-form arguments.
  - `bento-analytical` — Plus Jakarta Sans + Fira Code, 12-column bento tile grid, filter chip bar, tile hover effects. For comparisons, tool reviews, and data-rich content.
  - `technical-glow` — IBM Plex Sans + IBM Plex Mono, dark glow panels, flow step indicators with glow pulse, terminal-style section headers. For architecture and engineering articles.
  - `warm-cards` — Nunito + Fira Code, step card sequencer with animated progress tracker, spring-eased completion states. For tutorials and how-to guides.
  - `glass-layered` — Space Grotesk + Space Mono, glass panels over gradient backdrop (`backdrop-filter` + `@supports` fallback), overview-to-detail crossfade navigation. For framework and mental model content.
- **`--style` CLI argument** in `extract_structure.py` — accepts any of the 5 style names or `auto`; writes `selected_style` to `structure.json`
- **`STYLE_DIRECTIONS` dict** in `extract_structure.py` — auto-maps article types to bundled styles (`tutorial → warm-cards`, `technical-analysis → technical-glow`, `opinion → story-scrollytelling`, `tool-review → bento-analytical`, `case-study → story-scrollytelling`, `timeline → story-scrollytelling`, `framework → glass-layered`, `data-driven → bento-analytical`)
- **`STYLE_INTERACTION_OVERRIDES` dict** in both pipeline scripts — maps each style to its default interaction model
- **`DESIGN_SYSTEMS` entries** for all 5 new styles in `build_page_plan.py` — full font + palette token sets including style-specific tokens (glow colors, glass opacity, chapter rules, step-done colors)
- **`selected_style` key** in `blueprint.json` `design` block and `implementation_notes`
- **Bundled style specs** in `references/design-principles.md` — full design spec per style: character, fonts, palette summary, layout, interaction model, mobile behavior, avoids
- **CSS token blocks and component patterns** for all 5 styles in `assets/component-patterns.md` — drop cap, chapter rule, bento grid, filter chips, glow panels, flow step indicators, step cards, progress tracker, glass panels with browser fallback, overview concept cards, detail panel crossfade

### Changed

- `SKILL.md` Step 3 updated: `--style` flag documentation added above aesthetic matching table; new bundled styles reference table; new non-negotiable for complex styles with shallow content
- `references/design-principles.md` heading updated from "Four aesthetic directions" to "Aesthetic directions and styles"; added "Bundled styles" subsection with full specs for all 5 styles
- `build_page_plan.py` `build_blueprint()` updated to read `selected_style` from structure input and prefer it as the `design_direction` when present; `implementation_notes` includes style mode note when active
- `extract_structure.py` `main()` updated to resolve `selected_style` from `--style` flag and write it to structure output; interaction model overridden when bundled style is active

---

## [1.1.0] — 2026-03-20

### Added

- **`claude-like` design direction** — 5th aesthetic direction: warm off-white + terracotta coral, Instrument Serif + DM Sans, content-forward with generous whitespace and restrained accent use. Optimised for conversational AI content, reflective essays, and thought leadership.
- **Live demo** — [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web) — inline demo showing `claude-like` output for the "Build your site in one afternoon" article

---

## [1.0.0] — 2026-03-20

### Added

- **SKILL.md** — Main Claude skill definition with 5-step pipeline (Ingest → Normalize → Analyze → Blueprint → Build)
- **10 interaction models** — Scroll Journey, Step Sequencer, Concept Explorer, Comparison Matrix, Architecture Explainer, Decision Tree, Timeline Experience, Data Dashboard, Filterable Gallery, FAQ Explorer
- **4 aesthetic directions** — `dark-technical`, `editorial-ink`, `clean-analytical`, `editorial-warm` with matching font pairings and palettes
- **Degradation logic** — skill explicitly decides when static editorial output is better than hollow interactivity
- **`normalize_article.py`** — Stage 1 pipeline script: normalizes input from text, URL, or file to clean Markdown
- **`extract_structure.py`** — Stage 2 pipeline script: classifies article type and extracts structure → `structure.json`
- **`build_page_plan.py`** — Stage 3 pipeline script: selects interaction model and design direction → `blueprint.json`
- **`references/design-principles.md`** — Detailed aesthetic direction system with motion rules and quality bar
- **`references/visualization-patterns.md`** — Per-model implementation guidance for all 10 interaction patterns
- **`references/content-extraction-guide.md`** — Structured guidance on what to extract from each article type
- **`assets/component-patterns.md`** — Ready-to-use CSS/JS component patterns (step sequencers, timelines, matrices, etc.)
- **Demo site** (`demo/index.html`) — Self-contained product page with live article analyzer, pipeline diagram, and interaction model matrix
- **Example output** (`examples/alex-huang-ai-website.html`) — Full step-sequencer demo: "Building AI-Assisted Websites"
- **GitHub Actions workflow** — `deploy.yml` for automated GitHub Pages deployment of the demo site
