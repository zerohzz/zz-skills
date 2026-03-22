# Content Extraction Guide

When analyzing an article, extract these elements systematically.
Used in Step 1 (Analysis) before selecting interaction model.

---

## Always extract

| Element | Description |
|---|---|
| **Title** | Exact article title |
| **Subtitle** | If present |
| **Author** | If present |
| **Date** | Publication date |
| **Target audience** | Who is this written for? |
| **Thesis** | One sentence: what is this article *actually* claiming? |
| **Section headings** | All H2 and H3 headings, in order |
| **Key concepts** | Named ideas, tools, frameworks, entities — 3 to 7 |
| **Explicit examples** | Concrete cases used to illustrate points |
| **Comparisons** | Any side-by-side evaluations in the text |
| **Stages or phases** | Sequential steps, phases, or chronological markers |
| **Data points** | Any numbers, percentages, metrics, statistics |
| **Code snippets** | Technical samples or commands |
| **Pull-quote candidates** | The most memorable or impactful sentence |
| **Strongest takeaway** | What should the reader remember most? |
| **Open questions** | Unresolved points or future directions mentioned |

---

## Infer from structure

After extracting above, infer:

| Inference | Question to answer |
|---|---|
| **Dominant structure** | Is this linear / layered / hub-and-spoke / comparison / branching? |
| **Best interaction model** | What interaction genuinely reduces cognitive load for this content? |
| **Sections → components** | Which sections become interactive, which remain static? |
| **Upgrade or degrade?** | Is there enough structure to warrant interaction, or is static better? |
| **Tone match** | Which aesthetic direction matches the article's voice? |

---

## Content transformation rules

When building the artifact, transform source content — do not copy-paste.

| Source element | How to transform |
|---|---|
| Body paragraphs | Extract key claims; compress; don't reproduce verbatim |
| Step-by-step lists | Render as step sequencer, not a static list |
| Comparison text | Render as matrix or toggle, not prose |
| Data / statistics | Animate as stat cards, not inline numbers |
| Code blocks | Render with syntax styling and copy button |
| Pull quotes | Extract and render with typographic weight |
| Definitions | Surface as glossary popovers or concept cards |
| Conclusions | Place at end with visual emphasis; do not bury |

---

## What to NEVER do

- Invent article sections not present in source material
- Add fake metrics, fake citations, or fabricated claims
- Force interactivity where static is clearer
- Reproduce long paragraphs verbatim — compress and transform
- Summarize a sophisticated argument into marketing copy

---
---

# Quality Checklist

Run through this before presenting the final artifact.

## Content fidelity
- [ ] The article's main argument or thesis is preserved
- [ ] No claims have been invented or added
- [ ] No metrics, statistics, or citations are fabricated
- [ ] Technical content has not been oversimplified
- [ ] Nuance from the original has not been flattened

## Interaction quality
- [ ] At least one interaction materially reduces cognitive load
- [ ] Every interactive element has a clear purpose
- [ ] No interactions are purely decorative
- [ ] The page is still coherent without clicking/expanding everything
- [ ] Interactive affordances are obvious — users know what they can do

## Visual quality
- [ ] Font is NOT Inter, Roboto, Arial, or System UI
- [ ] Color palette has a clear dominant + accent logic
- [ ] Page feels designed for this content, not templated
- [ ] Adjacent sections are visually distinct
- [ ] Visual hierarchy reflects argument hierarchy

## Technical quality
- [ ] Page-load animation sequence is smooth and intentional
- [ ] All interactive elements have keyboard accessibility
- [ ] `prefers-reduced-motion` is respected
- [ ] Mobile layout is functional (min 375px width)
- [ ] No broken states or uncaught interactions

## Output completeness
- [ ] Artifact rationale is included (3 sentences max)
- [ ] Reuse notes are included (what to swap for another article)
- [ ] Artifact is self-contained (no external dependencies that might break)
