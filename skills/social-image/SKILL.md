---
name: social-image
description: >
  Transform blog posts, essays, and articles into beautiful multi-slide social
  media image carousels for Xiaohongshu (小红书 / XHS). Use when the user says
  "make social images", "create carousel", "turn this into XHS slides", "make
  XHS cards", "make social cards", "xiaohongshu cards", "social media poster",
  "图片轮播", "小红书图片", "小红书卡片", "生成小红书", "做成海报", or provides
  content and asks for shareable social media images or Instagram-style carousels.
  Produces cover + content slides as individual PNG files, supports 3:4 / 9:16 / 1:1
  aspect ratios and 8 visual themes.
---

# Article → Social Image Carousel

You transform written content into image carousels for social media platforms. This is not a design exercise — it is content adaptation: finding the article's core insights, restructuring them for slide format with the selected tone, distributing them across slides that flow naturally when swiped, and rendering them as pixel-perfect PNG files ready to publish.

---

## Step 0: Gather Requirements

Accept content from the user in any form:

| Source | Action |
|---|---|
| URL | `web_fetch` to retrieve article body |
| File path | Read the markdown file from disk |
| Pasted text / markdown | Use directly |

If a URL is given but retrieval fails, ask the user to paste the content. **Never hallucinate article content.**

After receiving content, determine parameters. Use defaults unless the user specifies otherwise:

| Parameter | Flag | Default | Options |
|---|---|---|---|
| Slide count (max) | `--slides N` | 9 | 1–18 (actual count may be lower if content is sparse) |
| Aspect ratio | `--ratio` | `3:4` | `3:4`, `9:16`, `1:1` |
| Theme | `--theme` | `sketch` | sketch, editorial, terminal, botanical, clean-modern, warm-paper, neo-brutalism, claude-like |
| Language mode | `--lang` | `auto` | `zh`, `en`, `auto` |
| Tone | `--tone` | `default` | `xhs`, `default`, `origin` — controls how aggressively content is rewritten (see Step 1) |
| Author tag | `--author` | (none) | Any string, e.g. `@username` — shown bottom-left of each content slide |

If the user has not specified these, proceed with defaults silently. Only ask if something is ambiguous.

---

## Step 1: Adapt Content for Slides

Before planning slides, Claude adapts the source article into slide-ready format based on the `--tone` setting. Save the result to `xhs_content.md`.

### Language detection (applies to all tones)

- If the content is primarily English and `--lang` is `auto` or `zh`: translate and adapt to Mandarin Chinese
- If the content is primarily Chinese: keep as Chinese
- If `--lang zh` is set: always output in Chinese
- If `--lang en` is set: keep English

---

### Tone: `xhs` — Full XHS-native rewrite

Rewrite the source article into authentic Xiaohongshu voice. Read `references/xhs-style-guide.md` for detailed guidelines.

- **Title**: under 20 Chinese characters (or ~40 English characters), catchy — use a question, bold statement, or number-led hook
- **Short paragraphs**: 2–3 sentences maximum per paragraph; hard line breaks between paragraphs
- **Emoji**: sprinkle naturally, 1–2 per paragraph where they add warmth or emphasis — never forced
- **Structure**: organize content into clear topic groups; each group will become one slide
- **Hashtags**: extract 3–5 relevant hashtags in `#话题#` format; place at end of content
- **Tone**: conversational, first-person where appropriate, experience-sharing, authentic — not corporate

---

### Tone: `default` — Auto-selected style (smart compression)

Claude analyzes the content and auto-selects the best style. Do NOT read `xhs-style-guide.md`.

**Content analysis — decide formality based on content type:**
- Personal blog / essay / story → casual, warm, first-person OK
- Tutorial / how-to → neutral, clear, instructional
- Technical / research / analysis → formal, precise, third-person
- Listicle / roundup → concise, scannable, direct

**Rewriting rules:**
- **Title**: clear and engaging, preserve the original title's intent — don't clickbait or over-simplify
- **Compression**: moderate — shorten paragraphs for slide readability, but keep the author's voice and key details
- **Emoji**: only if the content naturally lends itself to them (casual/personal content); never force emojis into technical or formal content
- **Structure**: organize into clear topic groups for slides; merge thin sections, split dense ones
- **Tone**: match the original author's voice — do not force first-person if the original uses third-person
- **Hashtags**: include only if the content is social-media oriented; otherwise omit the hashtag line entirely

---

### Tone: `origin` — Preserve original voice (minimal compression)

Preserve the original article's wording, structure, and tone as faithfully as possible. Do NOT read `xhs-style-guide.md`.

- **Title**: use the original article title as-is (trim to character limit only if absolutely necessary)
- **Subtitle**: use the article's own subtitle or first sentence
- **Emoji**: pick one neutral, topic-appropriate emoji for the cover only
- **Structure**: map the original article's sections directly to `## Section` headings; only split a section if it exceeds ~150 words
- **Content**: preserve original wording and sentence structure **verbatim** — do not paraphrase, do not add conversational interjections, do not shift to first-person
- **Emoji in body**: do not add any emojis to body text
- **Hashtags**: do not generate hashtags — omit the hashtag line entirely
- **Trimming**: only cut content if it physically cannot fit the requested number of slides. When trimming is necessary, remove footnotes, image references, and redundant examples — never rewrite what remains.

---

### Output format for xhs_content.md

The output structure is the same **regardless of tone**. What changes per tone is the *content* within this structure, not the structure itself.

```markdown
# [Title]

[Cover subtitle — one line]

[Cover emoji — single emoji]

---

## [Section topic 1]

[Content for slide 1]

## [Section topic 2]

[Content for slide 2]

...

[Optional: hashtag line — only for xhs tone or when default tone deems it appropriate]
```

If no hashtags are generated (`origin` or `default` mode), omit the hashtag line entirely.

---

## Step 2: Plan Slides

Run the planning script with the rewritten content:

```bash
python3 {SKILL_DIR}/scripts/plan_slides.py \
  --input xhs_content.md \
  --slides {SLIDES} \
  --ratio {RATIO} \
  --theme {THEME} \
  --output slide_plan.json
```

If the script outputs `⚠ Auto-fit suggested`, inform the user that the content would work better with fewer slides, and ask if they want to use the suggested count or keep their original number.

**Read `slide_plan.json` carefully before proceeding.** It is your implementation contract for Step 3. The JSON structure will look like:

```json
{
  "config": {
    "theme": "sketch",
    "ratio": "3:4",
    "width": 1080,
    "height": 1440,
    "total_slides": 9
  },
  "cover": {
    "emoji": "✨",
    "title": "标题文字",
    "subtitle": "副标题一句话"
  },
  "slides": [
    {
      "slide_number": 2,
      "type": "content",
      "heading": "主题标题",
      "design_hint": "section-opener",
      "blocks": [
        { "type": "heading", "level": 2, "content": "小标题" },
        { "type": "paragraph", "content": "内容段落..." },
        { "type": "list", "list_type": "unordered", "items": ["要点1", "要点2"] }
      ]
    }
  ]
}
```

---

## Step 3: Build Slide HTML

For each slide defined in `slide_plan.json`, generate a self-contained HTML file and save it to `{SKILL_DIR}/slides/` (inside the skill directory, as a sibling of `assets/`). This ensures the `../assets/` relative CSS paths in the templates resolve correctly.

**Ratio class:** Add a class to `<body>` based on the aspect ratio for ratio-adaptive styling:
- `3:4` → `<body class="ratio-3-4">`
- `9:16` → `<body class="ratio-9-16">`
- `1:1` → `<body class="ratio-1-1">`

**Naming convention:**
- Cover: `{SKILL_DIR}/slides/cover.html`
- Content slides: `{SKILL_DIR}/slides/slide_01.html`, `{SKILL_DIR}/slides/slide_02.html`, etc. (zero-padded)

### Cover slide (slide_number: 1, type: "cover")

Use `{SKILL_DIR}/assets/cover.html` as your starting template. Replace these placeholders:

| Placeholder | Value |
|---|---|
| `{{THEME}}` | theme name from config |
| `{{FONT_URL}}` | Google Fonts URL for the theme (see table below) |
| `{{RATIO_CLASS}}` | `ratio-3-4`, `ratio-9-16`, or `ratio-1-1` based on config.ratio |
| `{{TONE}}` | `config.content_tone` from slide_plan.json (empty string if `default`) |
| `{{REF}}` | Category breadcrumb — infer from content: e.g. `REF — 思维 / 第一性原理`. Format: `REF — domain / topic`. If no clear category, leave empty. |
| `{{SOURCE}}` | Source title in uppercase: e.g. `THE BOOK OF ELON · 1/3`. Use article source if known, or the article title abbreviated + slide count. |
| `{{TITLE}}` | `cover.title` from slide_plan.json |
| `{{SUBTITLE}}` | `cover.subtitle` from slide_plan.json |
| `{{AUTHOR}}` | `config.author` from slide_plan.json (empty if not set) |

**Cover layout:** The cover is now left-aligned (not centered), with a REF breadcrumb at top, source line, large title (84px), subtitle, and optional author footer at bottom. This follows the ljg-card reading card pattern for a more authoritative, magazine-like feel.

### Content slides (type: "content")

Use `{SKILL_DIR}/assets/card.html` as your starting template. Replace these placeholders:

| Placeholder | Value |
|---|---|
| `{{THEME}}` | theme name from config |
| `{{FONT_URL}}` | Google Fonts URL for the theme |
| `{{RATIO_CLASS}}` | `ratio-3-4`, `ratio-9-16`, or `ratio-1-1` based on config.ratio |
| `{{TONE}}` | `config.content_tone` from slide_plan.json (empty string if `default`) |
| `{{CONTENT}}` | HTML rendered from the slide's `blocks` array (including semantic blocks) |
| `{{PAGE}}` | `slide_number - 1` (content slide index, 1-based) |
| `{{TOTAL}}` | `total_slides - 1` (total content slides) |

### Block rendering rules

**Standard blocks:**

| Block type | HTML output |
|---|---|
| `heading` level 2 | `<h2>text</h2>` |
| `heading` level 3 | `<h3>text</h3>` |
| `paragraph` | `<p>text</p>` |
| `list` unordered | `<ul><li>item</li>...</ul>` |
| `list` ordered | `<ol><li>item</li>...</ol>` |
| `code` | `<pre><code class="lang-{lang}">text</code></pre>` |
| `quote` | `<blockquote><p>text</p></blockquote>` |

**Semantic blocks** (detected by `plan_slides.py` from content patterns):

| Block type | HTML output |
|---|---|
| `comparison` | `<div class="comparison"><div class="comparison-card"><div class="comparison-label">left_label</div><div class="comparison-title">short title</div><div class="comparison-body">left_content</div></div><div class="comparison-card"><div class="comparison-label">right_label</div><div class="comparison-title">short title</div><div class="comparison-body">right_content</div></div></div>` |
| `data-callout` | `<div class="data-callout"><div class="data-item dark"><div class="data-label">label</div><div class="data-value">$13,000</div><div class="data-desc">description</div></div><div class="data-divider">÷</div><div class="data-item"><div class="data-label">label</div><div class="data-value">$200</div><div class="data-desc">description</div></div></div>` — use `.dark` class on one item for contrast |
| `labeled-item` | `<div class="labeled-item"><div class="item-label">label</div><div class="item-content">content</div></div>` |
| `gold-sentence` | `<div class="gold-sentence">content</div>` — for short, insight-dense sentences |

**When rendering semantic blocks:**
- `comparison`: The `comparison-title` should be a 2-4 word summary extracted from the content. The `comparison-body` is the full text.
- `data-callout`: Use `data-divider` between items when showing a relationship (÷, ×, =, →). Apply `.dark` to the first item for visual contrast.
- `gold-sentence`: These are standalone — do not nest inside `<p>` tags. Use `<span class="accent-text">key phrase</span>` inside gold sentences to highlight the core insight.
- `labeled-item`: These replace `**Label**: content` patterns. The label appears in accent color above the body text.

### Content tone colors

`slide_plan.json` includes `config.content_tone` (one of: `philosophical`, `technical`, `literary`, `scientific`, `default`) and `config.tone_colors` with `bg` and `accent` values. These are set automatically based on content keyword analysis.

**How to apply:** Set `data-tone="{{TONE}}"` on the `<body>` tag (the template already includes this). The base CSS maps each tone to `--tone-bg` and `--tone-accent` CSS variables. Themes can use these to override their defaults for a content-appropriate feel.

If `content_tone` is `default`, set `data-tone=""` (empty) so no override kicks in and the theme's natural colors show through.

---

### Anti-AI design guidelines

These rules prevent the output from looking like typical AI-generated content. Follow them when building slide HTML:

1. **No three-equal-column layouts** — if you have 3 items, use 2+1 or asymmetric grid, not equal thirds
2. **No centered hero headlines on content slides** — titles are left-aligned; only the cover may center text
3. **Accent color in max 2 places per slide** — labels + one highlight; don't spray accent everywhere
4. **10:1 size ratio** — the largest element (data value, title) should be ~10× the smallest (label, caption). Example: 72px data vs 22px label
5. **Off-black only** — use `#1a1a1a` or `#2c2c2c`, never pure `#000000`
6. **No generic class names** — use `.comparison-card`, `.data-value`, `.gold-sentence` — never `.section`, `.panel`, `.box`
7. **Whitespace is intentional** — large gaps between sections signal hierarchy, not emptiness
8. **One visual anchor per slide** — each slide should have exactly one element that immediately grabs the eye (a large number, a bold title, a comparison block)

---

### Design hint application

Apply the slide's `design_hint` value to add visual variety:

| Hint | Treatment |
|---|---|
| `section-opener` | Heading already has accent bar from theme CSS — no extra treatment needed |
| `code-heavy` | Reduce code block font size to 0.75rem for readability |
| `list-heavy` | Increase `li` font size slightly and add more padding between items |
| `quote-featured` | Style the blockquote as a pull quote with larger text and centered alignment |
| `text-dense` | Add class `text-dense` to `.card-content` (CSS adds extra paragraph margin). **Do not add `<hr>` elements.** |

### Whitespace control: semantic visual fill

After assembling the content blocks for each **non-cover slide**, estimate whether the content will fill the viewport. If not, generate a visual component to fill the gap.

**Estimation rules:**
- h2 heading ≈ 80px, h3 ≈ 60px, paragraph ≈ 50px per line (~18 Chinese chars per line at 32px), list item ≈ 60px, code block ≈ 40px per line, blockquote ≈ 80px
- comparison block ≈ 280px (two side-by-side cards), data-callout ≈ 200px (row of data items), labeled-item ≈ 100px, gold-sentence ≈ 120px
- Card inner padding: ~128px vertical (top 52px + bottom 76px including safe zone)
- Available content height = viewport height − container padding (80px) − card padding (128px) − page number area (60px) = **viewport height − 268px**
- For 3:4 (1440px): available ≈ 1172px. For 9:16 (1920px): available ≈ 1652px. For 1:1 (1080px): available ≈ 812px.

**If estimated content height < 75% of available height**, the slide has excess whitespace. You **must** generate a static front-end visual component to fill the gap. Do not leave slides with large empty areas.

**Component selection — match the slide's content meaning:**

| Content semantic | Recommended components |
|---|---|
| Steps / tools / workflow | Timeline, flowchart, funnel, pipeline diagram, Gantt chart |
| Comparison / choice | VS card, decision tree, comparison table, pros-cons color blocks |
| Numbers / data / conclusions | Data highlight blocks, progress bars, ring chart, bubble chart |
| Definitions / concepts | Concept map, formula box, definition panels, Callout tip boxes |
| Multiple factors / relationships | Venn diagram, 2×2 matrix, cycle diagram, fishbone diagram |
| Key points / summary | Icon tag cloud, numbered card grid, Checklist, label badge strip |
| Quotes / insights | Quote block, speech bubble, highlight banner, persona card |

**Use `extractable_content` from slide_plan.json** — each slide includes `quotes`, `data_points`, `tools_mentioned`, and `code_blocks` extracted from the source article. Use these as real content for fill components instead of inventing abstract visualizations.

**Component styling rules:**
- Use only theme colors: `var(--accent)` for highlights, card background color for fills
- **No borders or outlines** — do NOT wrap components in border boxes. Use background tints, spacing, and typography to create visual structure instead
- Font: inherit from theme (heading font for labels, body font for descriptions)
- Border-radius: 12–14px where background fills are used
- Background: use `rgba()` tints of the accent color at 4–8% opacity, or transparent
- Separation between elements: use spacing (gap, margin, padding) and subtle background tints, not lines or borders
- All component CSS must be in an inline `<style>` block within the slide HTML
- Components must NOT introduce new information not present in the source article — they **visualize or restructure existing content** in a more space-filling layout

**Component placement:**
- Insert after the last content block, before swipe-hint / cta-hint
- The component should fill the remaining vertical space naturally — do not hardcode pixel heights

**Examples of good fill components:**
- A slide about 4 tools → 2×2 tool comparison grid below the text
- A slide with 3 key takeaways → data badges summarizing numbers from the article
- A slide listing pitfalls → checklist grid summarizing each pitfall as a visual check item
- A slide about a workflow → horizontal pipeline/funnel showing the stages

### Theme font URLs

| Theme | Google Fonts URL |
|---|---|
| sketch | `https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap` |
| editorial | `https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Crimson+Pro:wght@400;600&display=swap` |
| terminal | `https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap` |
| botanical | `https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Nunito:wght@400;600;700&display=swap` |
| clean-modern | `https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap` |
| warm-paper | `https://fonts.googleapis.com/css2?family=Newsreader:wght@400;600&family=Nunito:wght@400;600;700&display=swap` |
| neo-brutalism | `https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&family=Space+Mono:wght@400;700&display=swap` |
| claude-like | `https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Lora:ital,wght@0,400;0,600;0,700;1,400&display=swap` |

### Author tag and swipe hints

For each **content slide** (not the cover):

- If `config.author` is non-empty: add `<div class="author-tag">{{AUTHOR}}</div>` inside `.card-inner`, just before `.page-number`
- If this is **not the last content slide**: add `<div class="swipe-hint">→ 继续滑动</div>` just before `.page-number`
- If this is the **last content slide**: instead add `<div class="cta-hint">💬 [one line that invites engagement, adapted to the article topic]</div>` just before `.page-number`

---

## Step 3.5: Verify Whitespace (mandatory)

After generating all slide HTML files, run the whitespace verification script **before rendering to PNG**. This measures actual rendered content height in each slide and reports which slides need fill components.

```bash
python3 {SKILL_DIR}/scripts/verify_slides.py \
  --input-dir {SKILL_DIR}/slides/ \
  --width {WIDTH} --height {HEIGHT} \
  --output verify_report.json
```

The script outputs a JSON report with each slide's fill ratio and status:
- `"pass"` (≥75% filled) — no action needed
- `"warn"` (60–75% filled) — fill component recommended
- `"sparse"` (<60% filled) — fill component **required**

**For each `"sparse"` or `"warn"` slide:**

1. Read the slide's HTML file
2. Check `extractable_content` in `slide_plan.json` for quotable sentences, data points, and tools to visualize
3. Pick a fill component from the taxonomy that matches the slide's content semantic
4. Add the component inside `.card-content`, after the last content block (use inline `<style>` for component CSS)
5. The component should target the `gap_px` value from the report — design it to fill roughly that many pixels

**Re-run `verify_slides.py` after edits.** Repeat until all slides show `"pass"` or `"warn"`. Maximum 2 iterations — if a slide still fails after 2 rounds, accept it and proceed.

**Cover slides** will always show as sparse (they're intentionally minimal). Ignore the cover's status.

---

## Step 4: Render to PNG

Once all HTML files are written to `slides/` and verification passes, run the renderer:

```bash
python3 {SKILL_DIR}/scripts/render_slides.py \
  --input-dir {SKILL_DIR}/slides/ \
  --output-dir output/ \
  --width {WIDTH} \
  --height {HEIGHT} \
  --dpr 2
```

`{WIDTH}` and `{HEIGHT}` come from `config.width` and `config.height` in `slide_plan.json`.
Output PNGs are written to `output/` in the current working directory.

The `--dpr 2` flag renders at 2× pixel density for crisp display on high-DPI screens.

### If overflow warnings appear

If the renderer outputs `⚠ overflow: {SKILL_DIR}/slides/slide_NN.html`, inspect that slide's HTML and fix the overflow by:

1. Shortening paragraph text (trim to key points)
2. Reducing font size via an inline `<style>` tag in the slide file
3. Removing the least important block from that slide

Re-run the renderer for the affected slide only after fixing.

### If Playwright is not installed

Print this message to the user and stop:

```
Playwright is required to render slides. Install it with:

  pip install playwright && playwright install chromium

Then re-run this skill.
```

---

## Step 4.5: Visual Hierarchy Review

After rendering, invoke these skills to evaluate slide quality:

1. **`/impeccable:critique`** — assess visual hierarchy, information architecture, emotional resonance. Output severity-rated issue list (critical / moderate / minor).
2. **`/impeccable:polish`** — check spacing consistency, alignment, vertical fill. Flag any slide where content visually fills < 70% of card height.
3. **`/frontend-design:frontend-design`** — verify the design has intentional aesthetic direction; flag generic defaults in typography or color use.

For each issue: output the affected slide filename, the issue category, and a one-line fix recommendation. Auto-apply safe fixes (font-size, line-height, margin, padding) via an inline `<style>` block in the slide HTML. Flag content-editing issues for human review. Re-render affected slides after auto-fixes.

This step is **optional but recommended** — skip it only if the user explicitly says to skip visual review.

---

## Step 5: Deliver

After all PNGs are generated:

1. List all output files: `output/cover.png`, `output/slide_01.png`, etc.
2. Show total slide count and pixel dimensions (e.g., `9 slides at 1080×1440 @2× = 2160×2880px`)
3. Offer follow-up options:

> Want to adjust anything?
> - Change tone (`--tone xhs`, `--tone default`, `--tone origin`)
> - Change theme (`--theme`)
> - Adjust slide count (`--slides`)
> - Regenerate a specific slide
> - Edit a slide's content and re-render
> - Change aspect ratio (`--ratio`)

---

## Reference Files

| File | When to read |
|---|---|
| `references/xhs-style-guide.md` | During Step 1 **only when `--tone xhs`** — XHS tone, title guidelines, hashtag strategy, before/after examples |

---

## Non-Negotiables

- Always read `slide_plan.json` before building any HTML — it is the implementation contract
- Never skip Step 1 — even in `origin` mode, content must be restructured into the `xhs_content.md` format for the slide planning pipeline
- Always use the templates in `assets/` as starting points for slide HTML
- `{SKILL_DIR}` is the directory containing this SKILL.md file; all script and asset paths are relative to it
- Never invent article content — all slide content must come from the source material
- Keep slide HTML self-contained; CSS must be inline or loadable via relative paths that work from the `slides/` subdirectory
- If `python3` is not available, try `python`
- Never produce fewer than 2 slides (cover + at least 1 content slide)
