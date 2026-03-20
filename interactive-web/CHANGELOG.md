# Changelog

All notable changes to `interactive-web` will be documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

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
