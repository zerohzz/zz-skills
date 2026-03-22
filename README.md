# zz-skills

Claude Code skills shared by zerohzz ([alex-huang.dev](https://alex-huang.dev)) — tools for building, recording, and publishing with Claude Code.

## Skills

| Skill | Description |
|-------|-------------|
| [interactive-web](#interactive-web) | Transform articles into interactive web experiences |
| [gif-recorder](#gif-recorder) | Record any website as a polished animated GIF |

## Prerequisites

- Claude Code installed and running
- Python 3.10+ (for skills that use analysis pipeline scripts)

## Installation

### Quick Install (Recommended)

```bash
npx skills add zerohzz/zz-skills
```

### Register as Plugin Marketplace

```bash
/plugin marketplace add zerohzz/zz-skills
```

### Install a Specific Skill

```bash
/plugin install interactive-web@zz-skills
/plugin install gif-recorder@zz-skills
```

Or just tell Claude Code:

> Please install Skills from github.com/zerohzz/zz-skills

## Update Skills

1. Run `/plugin` in Claude Code
2. Switch to **Marketplaces** tab
3. Select **zz-skills** → **Update marketplace**

Enable **auto-update** to always get the latest versions automatically.

---

## Available Skills

### interactive-web

Transform blog posts, essays, technical articles, and long-form written content into polished interactive web experiences. This skill is agentic: it runs a structured analysis pipeline, selects the right interaction model, commits to a matching aesthetic direction, and builds a production-quality single-file HTML artifact — without requiring step-by-step guidance.

**Trigger phrases:**

```
"Make this interactive"
"Turn my blog post into a webpage"
"Build an interactive explainer for this"
"Visualize this article"
"Make this explorable"
"Turn this into a mini-site"
```

**From a file:**

```bash
/interactive-web posts/my-article.md
```

**From a URL:**

```bash
/interactive-web https://example.com/article
```

**Specify interaction model:**

```bash
/interactive-web posts/my-article.md --model step-sequencer
/interactive-web posts/my-article.md --model comparison-matrix
/interactive-web posts/my-article.md --model timeline
```

**Specify design direction:**

```bash
/interactive-web posts/my-article.md --design dark-technical
/interactive-web posts/my-article.md --design editorial-ink
/interactive-web posts/my-article.md --design claude-like
```

**Combine both:**

```bash
/interactive-web posts/my-article.md --model concept-explorer --design clean-analytical
```

#### Pipeline

The skill runs a 4-stage analysis pipeline before writing any code:

| Stage | Script | Input | Output |
|-------|--------|-------|--------|
| Normalize | `normalize_article.py` | Raw text / URL / file | `normalized.md` |
| Extract | `extract_structure.py` | `normalized.md` | `structure.json` |
| Blueprint | `build_page_plan.py` | `structure.json` | `blueprint.json` |
| Build | Claude (SKILL.md) | `blueprint.json` + article | Single-file HTML |

#### Interaction Models

| Pattern | Best For |
|---------|----------|
| `scroll-journey` | Narratives, opinion essays, long-form arguments |
| `step-sequencer` | Tutorials, how-tos, implementation walkthroughs |
| `concept-explorer` | Frameworks, layered ideas, capability models |
| `comparison-matrix` | Tool reviews, tradeoff analysis, side-by-side choices |
| `architecture-explainer` | Technical systems, flows, components, integrations |
| `decision-tree` | Strategic guides, diagnostic content, "which one" posts |
| `timeline` | Historical, chronological, before/after evolution |
| `data-dashboard` | Statistics-heavy, research-driven, metric-rich content |
| `filterable-gallery` | Pattern libraries, curated examples, reference roundups |
| `faq-explorer` | Q&A posts, FAQs, question-driven content |

#### Design Directions

| Direction | Character | Fonts | Palette |
|-----------|-----------|-------|---------|
| `dark-technical` | Precision, monospace clarity, analytical depth | IBM Plex Sans + IBM Plex Mono | Dark slate + electric blue |
| `editorial-ink` | Typographic authority, ink-on-paper weight | Playfair Display + Crimson Pro | Aged paper + editorial red |
| `clean-analytical` | Tabular precision, high contrast, chart-friendly | Plus Jakarta Sans + Fira Code | Deep slate + cyan or amber |
| `editorial-warm` | Forward momentum, approachable warmth | Newsreader + Nunito | Warm cream + burnt orange |
| `claude-like` | Quiet confidence, warm restraint, content-forward | Instrument Serif + DM Sans | Warm off-white + terracotta coral |

#### Bundled Styles

Bundled styles lock in both a visual identity **and** an interaction model together — use `--design` to apply one. The skill picks the best match automatically if you don't specify.

```bash
/interactive-web posts/my-article.md --design story-scrollytelling
/interactive-web posts/my-article.md --design bento-analytical
/interactive-web posts/my-article.md --design technical-glow
/interactive-web posts/my-article.md --design warm-cards
/interactive-web posts/my-article.md --design glass-layered
```

| Style | Best For | Interaction | Fonts |
|-------|----------|-------------|-------|
| `story-scrollytelling` | Narrative essays, long-form arguments, case studies | scroll-journey | Cormorant Garamond + Lato |
| `bento-analytical` | Comparisons, tool reviews, data-rich breakdowns | comparison-matrix | Plus Jakarta Sans + Fira Code |
| `technical-glow` | Engineering, architecture, system design | architecture-explainer | IBM Plex Sans + IBM Plex Mono |
| `warm-cards` | Tutorials, how-tos, step-by-step walkthroughs | step-sequencer | Nunito + Fira Code |
| `glass-layered` | Concept frameworks, mental models, layered explainers | concept-explorer | Space Grotesk + Space Mono |

#### Degradation Logic

- **Upgrade to interactive** when content has explicit phases, comparisons, hierarchies, or data
- **Degrade to static editorial** when content is a short opinion or single argument with no navigable structure

A high-quality static editorial page is a better output than hollow interactivity.

#### Output

1. **Artifact rationale** (3 sentences) — chosen model, design direction, and what interactivity adds
2. **The interactive webpage** — single self-contained `.html` file, open directly in any browser
3. **Reuse notes** — what to swap to adapt this to another article

#### Non-Negotiables

- Never copies paragraphs verbatim — extracts and rebuilds content into interactive treatments
- Never invents sections not in the source article
- Never uses Inter, Roboto, Arial, or System UI fonts
- All interactive elements must be keyboard accessible
- Responsive layout declared for all artifacts

#### Demo

**Skill Lab page:** [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web)

**Live output example** — generated by running:

```bash
/interactive-web https://alex-huang.dev/posts/ai-website-one-day/ --design claude-like
```

→ [alex-huang.dev/skill-lab/interactive-web-demo.html](https://alex-huang.dev/skill-lab/interactive-web-demo.html)

Source article: [alex-huang.dev/posts/ai-website-one-day](https://alex-huang.dev/posts/ai-website-one-day/)

---

### gif-recorder

Record any website as a polished animated GIF — ready for README demos, social media, or presentations. Works entirely within Claude Code (no local setup needed): fetches the page, reconstructs it as a self-contained HTML, serves it on localhost, and records with Playwright.

**Trigger phrases:**

```
"Record my website as a GIF"
"Make a demo GIF of my site"
"Create a screen recording of this URL"
"Capture a user interaction flow as an animated GIF"
"Make a social media demo of my website"
```

**Usage:**

```bash
/gif-recorder https://example.com
```

---

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zerohzz/zz-skills&type=Date)](https://www.star-history.com/#zerohzz/zz-skills&Date)
