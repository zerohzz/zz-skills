# Changelog

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
