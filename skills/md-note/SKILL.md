---
name: md-note
description: "Reformat messy, unstructured notes into clean Obsidian-flavored markdown with YAML frontmatter, heading hierarchy, normalized tags, and descriptive links. Use this skill whenever the user asks to clean up notes, format notes for Obsidian, convert raw text into structured markdown, organize messy notes, add frontmatter to a note, or mentions 'Obsidian', 'note formatting', 'markdown cleanup', 'YAML frontmatter', or 'reformat my notes'. Also trigger when the user pastes a block of unstructured text and asks to make it readable, organized, or well-formatted as a note."
---

# Obsidian Markdown Formatter

Transform messy, unstructured notes into clean, well-organized Obsidian-flavored markdown following community best practices. Supports English, Chinese, and mixed-language notes with automatic language detection.

## Core Principles

- **Zero information loss** — preserve every piece of original content. Never delete, paraphrase away, or merge information into ambiguity.
- **No fabrication** — do not infer missing facts, add opinions, or invent content not present in the source.
- **Language mirroring** — auto-detect the input language (English, Chinese, or mixed) and output in the same language. Only override when the user explicitly requests a different language.

## Workflow

Follow these steps in order for every note:

### Step 1: Detect language

Determine whether the input is English, Chinese, or mixed. This governs the language of all generated content (summary, section headings, tag labels) except YAML field names, which are always English.

### Step 2: Identify structural elements

Scan the full note and extract:
- A candidate **title** (the most prominent topic or first heading)
- Logical **sections** and their hierarchy
- Any **tags**, hashtags, or category keywords
- Any **URLs** (raw or partially formatted)
- **Key terms**, definitions, and important concepts
- **Date** signals (explicit dates, "today", timestamps)
- **Status** signals ("draft", "WIP", "done", "complete", etc.)

### Step 3: Generate YAML frontmatter

Place a valid YAML block at the very top of the output with exactly these four fields:

```yaml
---
title: "<note title>"
date: YYYY-MM-DD
tags:
  - tag-one
  - tag-two
status: draft
---
```

Rules for each field:
- `title` — derived from the note's main topic or heading.
- `date` — use the note's own date if one is found; otherwise use today's date. Always `YYYY-MM-DD`.
- `tags` — lowercase, hyphen-separated for multi-word tags. Gathered from inline `#tags`, category words, and topic keywords in the note.
- `status` — infer from content cues (`draft`, `in-progress`, `complete`). Default to `draft` when unclear.

### Step 4: Write the H1 title and summary

- Exactly **one** `# Title` per note, matching the YAML `title`.
- Immediately below, write a **1-2 sentence summary** distilling the note's core content (in the detected language).

### Step 5: Organize body content

Restructure the content into a logical hierarchy:
- `##` (H2) for major sections
- `###` (H3) for subsections within an H2

Use your judgment to group related information. Preserve the original ordering where it already makes sense; reorganize only when the original is genuinely disordered.

### Step 6: Normalize formatting

Apply these formatting rules throughout the body:

| Element | Rule |
|---------|------|
| Unordered lists | Always use `-` (hyphen + space). Never `*` or `+`. |
| Ordered lists | Use `1.` numbering. |
| Bold emphasis | **Bold** key terms, definitions, and important concepts. |
| Raw URLs | Convert to `[descriptive text](URL)` markdown links. |
| Mixed list styles | Unify into a single consistent style. |
| Spacing | Single blank line between sections. Consistent indentation. |

### Step 7: Collect tags

At the bottom of the note, add a dedicated section:

```markdown
## Tags

#tag-one #tag-two #tag-three
```

This section mirrors the tags in the YAML frontmatter. All inline tags found in the note body should be gathered here as well.

### Step 8: Review

Before returning the output, verify:
- Every piece of original information is present (zero loss)
- Heading hierarchy is clean (`#` -> `##` -> `###`, no skipped levels)
- YAML frontmatter is valid
- All URLs are converted to descriptive links
- All tags appear both in YAML and the bottom Tags section
- Language is consistent with the detected input language

## Output Format

Return **only** the reformatted markdown. No explanations, commentary, or surrounding text — just the clean `.md` content.

Structure order:
1. YAML frontmatter
2. `#` Title
3. Summary (1-2 sentences)
4. `##` / `###` body sections
5. `## Tags` section

## Example

**Input (messy note):**

```
kubernetes notes oct 2024

pods are the smallest deployable unit. each pod = one or more containers.
services expose pods to network traffic (ClusterIP, NodePort, LoadBalancer)

https://kubernetes.io/docs/concepts/workloads/pods/

important: namespaces isolate resources within a cluster

#devops #k8s #containers

TODO: read about StatefulSets vs Deployments
```

**Output:**

```markdown
---
title: "Kubernetes Core Concepts"
date: 2024-10-01
tags:
  - devops
  - k8s
  - containers
  - kubernetes
status: draft
---

# Kubernetes Core Concepts

An overview of foundational Kubernetes concepts including pods, services, namespaces, and areas for further study.

## Pods

- **Pods** are the smallest deployable unit in Kubernetes.
- Each pod consists of one or more containers.

## Services

- **Services** expose pods to network traffic.
- Service types include **ClusterIP**, **NodePort**, and **LoadBalancer**.

## Namespaces

- **Namespaces** isolate resources within a cluster.

## Resources

- [Kubernetes Pods Documentation](https://kubernetes.io/docs/concepts/workloads/pods/)

## To Do

- Read about **StatefulSets** vs **Deployments**

## Tags

#devops #k8s #containers #kubernetes
```

## Handling Edge Cases

- **No clear title**: Synthesize a short descriptive title from the note's dominant topic.
- **No date found**: Use today's date.
- **Very short notes** (< 3 lines): Still apply the full structure (frontmatter, H1, summary, tags) — even minimal notes benefit from consistent formatting.
- **Already partially formatted notes**: Preserve existing valid structure; fix only what's inconsistent or missing.
- **Code blocks in the note**: Preserve them as-is inside fenced code blocks. Do not reformat code content.
