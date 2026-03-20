---
name: interactive-web
description: Transform blog posts, essays, technical articles, and long-form written content into polished interactive web experiences. Use this skill whenever a user wants an article, essay, or transcript turned into an interactive webpage, scrollytelling experience, visual concept explorer, timeline, comparison page, architecture explainer, or educational mini-app. Trigger when the user says "make this interactive", "turn my blog into a webpage", "visualize this article", "build an explainer for this", or hands you any substantial written content (article, transcript, framework post, case study) and implies they want something publishable or shareable. This skill is agentic: it runs a structured analysis pipeline, produces an intermediate blueprint, then generates a complete artifact — without requiring step-by-step user guidance. Also trigger for: "convert my post to a visual", "make this explorable", "build an interactive summary", "turn this into a mini-site".
---

# Blog → Interactive Web Experience

You transform written content into professional interactive web experiences. This is not decoration — it is content intelligence: finding the article's hidden structure, choosing an interaction model that genuinely aids comprehension, and building a production-quality artifact.

---

## Step 0: Ingest

Accept input in any form:

| Source | Action |
|---|---|
| Pasted text | Use directly |
| URL | `web_fetch` to retrieve article body |
| Uploaded file | Read from `/mnt/user-data/uploads/` |
| Markdown / HTML | Parse structure from headings and blocks |

If a URL is given but retrieval fails, ask for pasted text. **Never hallucinate article content.**

---

## Step 1: Run the Analysis Pipeline

Before writing any code, use scripts to build a grounded content model.

```bash
# Step 1a: Normalize raw input
python3 scripts/normalize_article.py --input <source>

# Step 1b: Extract structure (produces structure.json)
python3 scripts/extract_structure.py --input normalized.md

# Step 1c: Generate page blueprint (produces blueprint.json)
python3 scripts/build_page_plan.py --input structure.json
```

The scripts are available in `scripts/`. They produce intermediate JSON files. Read `blueprint.json` before building anything — it is your implementation contract.

If the environment cannot run scripts, perform the same analysis mentally and document your reasoning in a compact internal brief:

```
ANALYSIS BRIEF (internal — do not show user):
Article type:     [ Tutorial | Opinion | Data-driven | Narrative | Explainer |
                    Case Study | Technical Reference | Tool Review | Timeline ]
Thesis:           [One sentence — what is this actually about?]
Target reader:    [Technical | General | Domain specialist | Students]
Key concepts:     [3–7 extractable ideas, entities, stages, or comparisons]
Dominant structure: [ Linear | Hub-and-spoke | Comparison | Timeline |
                      Layered | Q&A | Process | Decision-tree ]
Best interaction: [See Step 2 — choose one primary model]
Degrade to static? [Yes / No — see degradation logic below]
```

---

## Step 2: Decide the Interaction Model

### Degradation Logic — decide FIRST

Ask: does this content genuinely benefit from interactivity?

**Upgrade to interactive when:**
- Content has explicit phases, stages, comparisons, or hierarchies
- Readers need to navigate depth at their own pace
- Multiple entities or concepts have meaningful relationships
- Data, metrics, or tradeoffs are central

**Degrade to static editorial when:**
- Content is a short opinion or single argument with no structure
- No interaction would reduce cognitive load or reveal structure
- Content is a brief note, announcement, or unstructured reflection

> A high-quality static editorial page is a better output than hollow interactivity.

### Interaction model selection

| Pattern | Best for |
|---|---|
| **Scroll Journey** | Narratives, opinion essays, long-form arguments |
| **Step Sequencer** | Tutorials, how-tos, implementation walkthroughs |
| **Concept Explorer** | Frameworks, layered ideas, capability models |
| **Comparison Matrix** | Tool reviews, tradeoff analysis, side-by-side choices |
| **Architecture Explainer** | Technical systems, flows, components, integrations |
| **Decision Tree** | Strategic guides, diagnostic content, "which one" posts |
| **Timeline Experience** | Historical, chronological, before/after evolution |
| **Data Dashboard** | Statistics-heavy, research-driven, metric-rich content |
| **Filterable Gallery** | Pattern libraries, curated examples, reference roundups |
| **FAQ Explorer** | Q&A posts, FAQs, question-driven content |

Read `references/visualization-patterns.md` for detailed implementation guidance per pattern.

---

## Step 3: Commit to a Design Direction

Before coding, commit to one aesthetic direction and execute it with precision.

Read `references/design-principles.md` for the full system.

**Core rule:** Every artifact must feel designed for this specific content. Not templated. Not generic.

**Aesthetic matching:**

| Content tone | Direction |
|---|---|
| Technical / developer | Dark, monospace accents, code-syntax palette, analytical precision |
| Opinion / essay | Editorial typography, ink-on-paper, generous whitespace, serif |
| Data / research | Clean analytical, high contrast, data visualization palette |
| Tutorial / instructional | Forward momentum, warm neutral, clear milestone hierarchy |
| Startup / product | Bold, motion-forward, sharp contrast, confident voice |
| Culture / narrative | Magazine editorial, expressive, bold typographic moments |

Read `assets/component-patterns.md` for ready-to-use CSS/JS components.

---

## Step 4: Build the Artifact

Generate a **single-file HTML artifact** (or React `.jsx` for complex state management).

### Required structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- One distinctive Google Font pair — never Inter/Roboto/Arial/System UI -->
  <!-- Full design system in CSS custom properties -->
  <!-- All styles in <style> block -->
</head>
<body>
  <!-- Content as interactive experience -->
  <!-- All JS in <script> block -->
</body>
</html>
```

### Non-negotiables

- CSS custom properties for the entire design system (`--color-*`, `--font-*`, `--space-*`)
- At least ONE interaction that materially reduces cognitive load
- Staggered page-load animation sequence
- Responsive layout (declare mobile behavior)
- All claims grounded in the source article — **never invent**
- Keyboard accessibility on all interactive elements

### Content transformation rules

Do NOT copy-paste paragraphs. Extract and rebuild:

| Source element | Interactive treatment |
|---|---|
| Stages / phases | Step sequencer or timeline |
| Data points | Animated stat cards or mini-charts |
| Comparisons | Side-by-side toggle or matrix |
| Definitions | Glossary popover or accordion |
| Key quotes | Pull-quote with typographic weight |
| Code snippets | Syntax-styled block with copy button |
| Relationships | Concept map or expandable graph |
| Conclusions | Progressive reveal, not buried in prose |

---

## Step 5: Deliver

Produce three outputs:

### 1. Artifact rationale (brief — 3 sentences)
- Chosen interaction model and why it suits this article
- Design direction taken
- What the interactive format adds over static reading

### 2. The interactive webpage artifact

### 3. Reuse notes (compact)
- What to swap to adapt this to another article
- Which parts are article-specific vs reusable pattern

---

## Reference Files

| File | When to read |
|---|---|
| `references/visualization-patterns.md` | Need detailed implementation for a specific interaction model |
| `references/design-principles.md` | Need aesthetic guidance or design decision framework |
| `references/content-extraction-guide.md` | Need structured guidance on what to extract from article |
| `references/quality-checklist.md` | Final QA before presenting to user |
| `assets/component-patterns.md` | Need CSS/JS code for specific UI components |

---

## Special Guidance: Technical Posts

- Preserve architecture and causal logic — do not flatten into marketing copy
- Render systems and flows explicitly (diagram or step reveal)
- Treat code as explanatory evidence, not decoration
- Highlight tradeoffs, constraints, failure modes — they are the content
- Distinguish clearly between "what", "why", and "how"

## Special Guidance: Opinion / Strategy Posts

- Preserve argument structure — do not summarize into bullet points
- Surface supporting pillars and counterpoints
- Surface assumptions and tradeoffs
- Use comparison, matrix, or branching view where the logic branches
- Do not present subjective claims as objective facts

---

## Non-Negotiables

- Never invent article sections not grounded in source material
- Never add fake metrics, fake citations, or fake author intent
- Never force interactivity where static presentation is better
- Never choose aesthetics that overwhelm comprehension
- Never reduce a sophisticated article into shallow visual fluff
- Never use Inter, Roboto, Arial, or System UI fonts
- Never use purple gradients on white as a default aesthetic
