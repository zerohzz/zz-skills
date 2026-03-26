# Changelog

## [1.3.0] - 2026-03-26

### Added
- Semantic block detection in `plan_slides.py` — automatically identifies comparison panels, data callouts, labeled items, and gold sentences from content patterns
- Content tone detection — analyzes content keywords to classify as philosophical, technical, literary, scientific, or default; provides matching color palette
- New CSS block types in `base.css`: `.comparison`, `.data-callout`, `.labeled-item`, `.gold-sentence`, `.accent-text`, `.equation-row`, `.data-divider`
- Content tone CSS variables (`--tone-bg`, `--tone-accent`) via `data-tone` attribute on `<body>`
- Anti-AI design guidelines in SKILL.md (no equal columns, accent max 2 places, 10:1 size ratio, off-black only)
- Theme-specific semantic block styles for sketch, claude-like, and editorial themes

### Changed
- Cover layout redesigned: left-aligned with REF breadcrumb, source line, large 84px title, and author footer (inspired by ljg-card reading card pattern)
- `cover.html` template updated with `{{REF}}`, `{{SOURCE}}`, `{{AUTHOR}}`, `{{RATIO_CLASS}}`, `{{TONE}}` placeholders
- `card.html` template updated with `{{RATIO_CLASS}}` and `{{TONE}}` placeholders
- Block rendering rules expanded with semantic block HTML patterns and rendering guidelines
- `slide_plan.json` config now includes `content_tone` and `tone_colors` fields

## [1.2.0] - 2026-03-25

### Added
- `verify_slides.py` — Playwright-based whitespace verification script that measures actual rendered content height vs available space and reports fill ratios (pass/warn/sparse)
- Step 3.5 verification loop in SKILL.md — mandatory whitespace check between HTML generation and rendering, with up to 2 fix iterations
- `extractable_content` field in slide plan JSON — preserves quotable sentences, key data points, tool names, and code blocks from source article for use in fill components
- Expanded component taxonomy in SKILL.md (decision trees, bubble charts, fishbone diagrams, Gantt charts, persona cards, etc.)

### Changed
- Pipeline is now 4-stage: Plan → Build → Verify → Render (was 3-stage)

## [1.1.0] - 2026-03-24

### Added
- `--tone` parameter with three modes:
  - `xhs` — full XHS-native rewrite (punchy titles, emojis, first-person, hashtags)
  - `default` — LLM auto-selects style based on content type, moderate compression
  - `origin` — preserve original voice, structure, and details with minimal compression
- Default tone changed from implicit XHS to `default` (auto-select) for broader platform support

### Changed
- Sketch theme fonts: Noto Serif SC + Lora (replaces Caveat + Comic Neue for proper CJK rendering)

## [1.0.0] - 2026-03-22

### Added
- Initial release of the social-image skill
- Intelligent content analysis and weight-based slide distribution
- 8 visual themes: sketch, editorial, terminal, botanical, clean-modern, warm-paper, neo-brutalism, claude-like
- XHS content rewriting with native style adaptation
- Bilingual support (auto-detect Chinese/English, adapt to XHS format)
- Auto-fit mode for short content
- Support for 3 aspect ratios: 3:4 (XHS default), 9:16 (Stories), 1:1 (Feed)
- Configurable slide count: 1-18 slides (default 9)
- plan_slides.py: content analysis and slide planning pipeline
- render_slides.py: Playwright-based HTML-to-PNG renderer
