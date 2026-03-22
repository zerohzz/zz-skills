---
name: gif-recorder
description: >
  Records a website's interactive user flow as a polished GIF — ready for social media,
  README demos, or presentations. Use this skill whenever the user wants to:
  - "Record my website as a GIF"
  - "Make a demo GIF of my site"
  - "Create a screen recording of this URL"
  - "Capture a user interaction flow as an animated GIF"
  - "Make a social media demo of my website"
  Always use this skill when a URL is mentioned alongside GIF, recording, demo, or screen capture.
  The skill handles the sandbox network limitation by fetching page content via web_fetch,
  reconstructing a faithful self-contained HTML, serving it on localhost, and recording
  with Playwright — so it works entirely within the Claude.ai environment.
---

# GIF Recorder

Records any website as a polished animated GIF with smooth cursor movement, click
highlights, and scroll animation. Works entirely within Claude.ai (no local setup needed).

## How it works

Because Claude.ai's sandbox can't access arbitrary external URLs via bash/Playwright,
this skill uses a **fetch → reconstruct → serve locally → record** pipeline:

1. `web_fetch` downloads the page content
2. Claude reconstructs a faithful self-contained HTML with inline CSS
3. Python HTTP server serves it on `localhost`
4. Playwright records the interaction against `localhost`
5. PIL + imageio export a polished GIF

## Workflow

### Step 1 — Gather requirements

Ask the user (if not already provided):
- **URL** to record
- **Aspect ratio / size**: default 9:16 (540×960 output), options: 16:9 (960×540), 1:1 (720×720)
- **Interaction flow**: what to click, scroll, type — in order
- **Cursor type** (see table below — default: `highlight`)
- **Style preference**: browser chrome mockup frame? (optional)

#### Cursor types

| Mode | Effect | Best for |
|------|--------|----------|
| `default` | Plain white arrow, no effects | Quick recordings, internal demos |
| `highlight` | Yellow glow halo + click ripple *(default)* | Tutorials, technical demos, product walkthroughs |
| `minimal` | Faint white halo, no click effects | Website demos, design-oriented products |
| `animated` | Blue multi-ring glow + motion trail + click burst | Marketing videos, landing page showcases |

### Step 2 — Fetch the page

Use `web_fetch` to fetch the URL. Set `html_extraction_method` to `markdown`.
Also try fetching obvious CSS paths (e.g. `/styles.css`, `/_astro/index.css`) to recover
real styles. Fetch linked CDN resources if you know their URLs.

Analyze the returned content:
- Page title and meta info
- Main sections and content blocks
- Interactive elements: buttons, tabs, accordions, nav links, forms
- Visual structure: headers, cards, sidebars

### Step 3 — Reconstruct self-contained HTML

Build a `index.html` with **all CSS inline** (no external dependencies) that:
- Faithfully reproduces the page structure and content
- Uses a dark or light theme that matches the original's aesthetic
- Includes all interactive elements with working JavaScript
- Uses system fonts to avoid font-loading issues
- Sets `cursor: none` on `body` (the recorder draws its own cursor)

Save to `/home/claude/gif_site/index.html` using `bash_tool` or `create_file`.

**Quality bar:** The reconstruction should look genuinely good — use modern CSS
(flexbox, grid, custom properties), appropriate spacing, and match the original's
visual personality. Don't produce a generic-looking page.

### Step 4 — Generate interaction steps

Based on the user's description, write a `steps.json` file:

```json
[
  {"type": "wait",   "seconds": 2},
  {"type": "move",   "selector": "h1"},
  {"type": "snap",   "frames": 12},
  {"type": "scroll", "amount": 300},
  {"type": "click",  "selector": "button:has-text('Next →')"},
  {"type": "wait",   "seconds": 1},
  {"type": "scroll", "amount": 400},
  {"type": "click",  "selector": "button:has-text('Mark complete')"},
  {"type": "wait",   "seconds": 2}
]
```

Step types:
| type | params | description |
|------|--------|-------------|
| `wait` | `seconds` | Hold on current view (good for opening / ending frames) |
| `snap` | `frames` | Capture N frames without moving |
| `scroll` | `amount` (px) | Smooth downward scroll |
| `click` | `selector` (CSS/text selector) | Animate cursor to element, click it |
| `move` | `selector` | Animate cursor to element without clicking |
| `scroll_to_bottom` | — | Scroll to page bottom |

Save to `/home/claude/gif_steps.json`.

### Step 5 — Run the recorder

```bash
cd /mnt/skills/user/gif-recorder
python scripts/recorder.py \
  --site-dir /home/claude/gif_site \
  --steps-json /home/claude/gif_steps.json \
  --output /mnt/user-data/outputs/demo.gif \
  --width 720 --height 1280 --fps 12 \
  --cursor highlight
```

Replace `--cursor highlight` with the mode chosen in Step 1.

Aspect ratio variants:
- 9:16 (social): `--width 720 --height 1280`
- 16:9 (wide):   `--width 1280 --height 720`
- 1:1 (square):  `--width 720 --height 720`

### Step 6 — Present and offer refinements

Use `present_files` to show the GIF. Then ask:
- "Does the timing feel right? I can slow down or speed up specific scenes."
- "Want to adjust which sections are shown?"
- "Should I add a browser chrome frame around it?"

If the user wants changes, edit `steps.json` or `index.html` and re-run the recorder.
**Don't start from scratch** — iterate on what's already there.

---

## Common issues and fixes

**Element not found / click misses**
→ Inspect the reconstructed HTML and fix the selector. Use `page.locator("text=Exact Button Text").first` for text-based selectors.

**GIF too large (>5 MB)**
→ Reduce FPS to 8–10, or reduce output size to 480×854.

**Page looks unstyled / wrong**
→ Improve the CSS reconstruction. Check the original page's visual style more carefully and rebuild.

**Animation cut off too early**
→ Increase `seconds` in the final `wait` step.

---

## Dependencies

Required Python packages (install once):
```bash
pip install playwright pillow imageio --break-system-packages
playwright install chromium
```

These are pre-installed in the Claude.ai sandbox.
