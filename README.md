# zz-skills

Skills shared by zerohzz （alex-huang.dev） for transforming written content into interactive web experiences with Claude Code.

## Prerequisites

- Claude Code installed and running
- Python 3.10+ (for the analysis pipeline scripts)

## Installation

**Step 1 — Register the marketplace in Claude Code:**

```
/plugin marketplace add zerohzz/zz-skills
```

**Step 2 — Install a skill:**

```
/plugin install interactive-web@zz-skills
```

### Available Skills

| Skill | Description |
|-------|-------------|
| **interactive-web** | Transform articles into interactive web experiences |

## Update Skills

```
/plugin marketplace update zerohzz/zz-skills
```

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
# Give Claude any article and ask it to make it interactive
/interactive-web posts/my-article.md
```

**From a URL:**

```bash
# Claude fetches the article automatically
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

The skill selects one of 10 patterns based on content type and structure:

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

#### Degradation Logic

The skill explicitly decides when **not** to add interactivity:

- **Upgrade to interactive** when content has explicit phases, comparisons, hierarchies, or data
- **Degrade to static editorial** when content is a short opinion or single argument with no navigable structure

A high-quality static editorial page is a better output than hollow interactivity.

#### Output

The skill produces three things:

1. **Artifact rationale** (3 sentences) — chosen model, design direction, and what interactivity adds
2. **The interactive webpage** — single self-contained `.html` file, open directly in any browser
3. **Reuse notes** — what to swap to adapt this to another article

#### Non-Negotiables

- Never copies paragraphs verbatim — extracts and rebuilds content into interactive treatments
- Never invents sections not in the source article
- Never uses Inter, Roboto, Arial, or System UI fonts
- All interactive elements must be keyboard accessible
- Responsive layout declared for all artifacts

---

## Demo

Live demo: [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web)

---

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zerohzz/zz-skills&type=Date)](https://www.star-history.com/#zerohzz/zz-skills&Date)
