# social-image

Transform articles into XHS social media carousels — multi-slide image sets ready to post on Little Red Book (XHS), Instagram, or any image carousel platform.

The skill analyzes your content, distributes it across slides based on weight and structure, adapts copy with a configurable tone (XHS-native, auto-selected, or original voice), and renders each slide to a high-quality PNG using Playwright. No manual layout work required.

---

## Installation

### Quick Install

```bash
npx skills add zerohzz/zz-skills
```

### Install This Skill Only

```bash
/plugin install social-image@zz-skills
```

### Via Plugin Marketplace

```bash
/plugin marketplace add zerohzz/zz-skills
```

Then install `social-image` from the marketplace UI.

---

## Usage

**From a file:**

```bash
/social-image posts/my-article.md
```

**From a URL:**

```bash
/social-image https://example.com/article
```

**With a theme:**

```bash
/social-image posts/my-article.md --theme sketch
/social-image posts/my-article.md --theme editorial --ratio 9:16
```

**With tone control:**

```bash
/social-image posts/my-article.md --tone origin          # preserve original voice
/social-image posts/my-article.md --tone xhs --lang zh   # full XHS adaptation
/social-image posts/my-article.md                        # auto-selects tone (default)
```

**Full options:**

```bash
/social-image posts/my-article.md --slides 12 --ratio 3:4 --theme warm-paper --tone xhs --lang zh
```

---

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--slides` | `9` | Number of slides to generate (1–18) |
| `--ratio` | `3:4` | Aspect ratio: `3:4` (XHS default), `9:16` (Stories), `1:1` (Feed) |
| `--theme` | auto | Visual theme (see Themes below) |
| `--tone` | `default` | Content adaptation: `xhs` (full XHS rewrite), `default` (auto-select), `origin` (preserve original voice) |
| `--lang` | auto-detect | Output language: `zh` (Chinese), `en` (English) |

When `--slides` is omitted and the content is short, the skill enters **auto-fit mode** and uses as few slides as needed rather than padding to 9.

---

## Themes

| Theme | Character |
|-------|-----------|
| `sketch` | Hand-drawn ink aesthetic, loose and expressive — great for personal essays and creative content |
| `editorial` | Clean editorial layout with typographic authority — suits thought leadership and analysis |
| `terminal` | Dark monospace, code-terminal energy — ideal for developer content and technical posts |
| `botanical` | Organic greens and nature-inspired softness — works well for lifestyle and wellness topics |
| `clean-modern` | Minimal white space, contemporary clarity — versatile default for most content types |
| `warm-paper` | Off-white paper tones, approachable warmth — perfect for storytelling and personal narratives |
| `neo-brutalism` | Bold borders, high contrast, loud personality — attention-grabbing for bold opinions |
| `claude-like` | Quiet confidence, warm restraint, content-forward — clean and readable across all topics |

If no `--theme` is specified, the skill selects the best match based on content tone and topic.

---

## Requirements

- **Python 3.10+**
- **Playwright** (installed automatically on first run via `playwright install chromium`)

The skill installs Playwright's Chromium browser on first use if not already present.

---

## Pipeline

| Stage | Script | Output |
|-------|--------|--------|
| Plan | `plan_slides.py` | `slide_plan.json` — content analysis, weight scoring, slide structure, extractable content |
| Build | Claude generates HTML | `slides/*.html` — one themed HTML file per slide |
| Verify | `verify_slides.py` | `verify_report.json` — measures actual rendered content height vs available space |
| Render | `render_slides.py` | `slide_01.png` … `slide_N.png` — one PNG per slide |

### Whitespace Verification Loop

After HTML generation, `verify_slides.py` opens each slide in headless Chromium and measures the actual content fill ratio. Slides below 75% filled are flagged for fill component insertion. This closes the feedback gap between HTML generation and rendering — sparse slides are caught and fixed before screenshots are taken.

```bash
python3 verify_slides.py --input-dir slides/ --width 1080 --height 1920 --output verify_report.json
```

---

## Output

Each run produces a numbered set of PNG files in the current directory:

```
slide_01.png   (cover)
slide_02.png
…
slide_09.png   (closing / CTA)
```

Upload directly to XHS, Instagram, or any carousel-capable platform.

---

## Style Guide

The XHS copywriting and design conventions used by this skill are documented in:

`social-image/skill/references/xhs-style-guide.md`
