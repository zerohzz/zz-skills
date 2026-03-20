# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

**Private development repo** for Claude Code skills published to [`zerohzz/zz-skills`](https://github.com/zerohzz/zz-skills) (public). All work happens here first; the public repo is a clean copy for end users.

## Publishing to Public Repo

```bash
GITHUB_PAT=ghp_xxx ./sync-public.sh
```

`sync-public.sh` clones `zz-skills`, rsyncs all files (excluding `.git`, `sync-public.sh`, and `scripts/`), commits as `feat: sync from dev YYYY-MM-DD`, then pushes.

**Before syncing:** ensure no private data, WIP notes, test files, or personal paths exist in the output.

## Repo Structure

```
zz-skills-dev/
├── interactive-web/         # The interactive-web skill
│   ├── skill/
│   │   ├── SKILL.md         # Main skill definition (Claude reads this when invoked)
│   │   ├── scripts/         # Python analysis pipeline (normalize → extract → blueprint)
│   │   ├── references/      # Design principles, visualization patterns, content extraction guide
│   │   └── assets/          # Reusable CSS/JS component patterns
│   ├── README.md
│   └── CHANGELOG.md
├── sync-public.sh           # Dev → public sync script (excluded from public repo)
└── README.md
```

## Skill Architecture: interactive-web

The skill runs a **4-stage analysis pipeline** before generating any HTML:

1. `normalize_article.py` — cleans raw input → `normalized.md`
2. `extract_structure.py` — identifies structure → `structure.json`
3. `build_page_plan.py` — selects interaction model and design → `blueprint.json`
4. Claude builds from `blueprint.json` per `SKILL.md`

**Key design constraint:** Skills must be self-contained and usable by any Claude Code user who installs from the public repo. No paths, tokens, or dev-only assumptions.

## Design Directions (interactive-web)

Five aesthetic directions are available via `--design`. Each has matching fonts, palette, and character:

| Direction | Character | Key fonts |
|-----------|-----------|-----------|
| `dark-technical` | Precision, monospace clarity | IBM Plex Sans + IBM Plex Mono |
| `editorial-ink` | Typographic authority, ink-on-paper | Playfair Display + Crimson Pro |
| `clean-analytical` | Tabular precision, chart-friendly | Plus Jakarta Sans + Fira Code |
| `editorial-warm` | Approachable warmth, forward momentum | Newsreader + Nunito |
| `claude-like` | Quiet confidence, content-forward, warm restraint | Instrument Serif + DM Sans |

`claude-like` was added 2026-03-20. Full token reference in `assets/component-patterns.md`, palette config in `build_page_plan.py`, character spec in `references/design-principles.md`.

## Live Demo

Skill Lab page: [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web)

Example command and its output:
```bash
/interactive-web https://alex-huang.dev/posts/ai-website-one-day/ --design claude-like
```
→ [alex-huang.dev/skill-lab/interactive-web-demo.html](https://alex-huang.dev/skill-lab/interactive-web-demo.html)

The demo page is inlined directly into the Skill Lab page (no iframe) — source HTML also at `interactive-web-ai-workflow.html` in the dev repo root.

---

## Adding a New Skill

New skills go in their own top-level directory (e.g., `my-skill/`). Each skill needs:
- `skill/SKILL.md` — the skill definition with YAML frontmatter (`name`, `description`)
- Any supporting scripts or reference files the skill reads at runtime
- A `README.md` and `CHANGELOG.md`

The `SKILL.md` frontmatter `description` field is what Claude uses to decide when to trigger the skill — write it precisely.
