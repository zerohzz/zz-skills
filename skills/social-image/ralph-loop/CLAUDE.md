# Ralph Loop — Social Image Visual Quality

You have ZERO memory. Read state from disk before doing anything.

## Goal

Improve `skills/social-image/SKILL.md` until every carousel slide scores **30/30** from a blind reviewer.

---

## Step 0: Load Context

Read these files in order. Do NOT skip any.

1. `skills/social-image/ralph-loop/progress.txt` — learnings from prior iterations
2. `skills/social-image/ralph-loop/scores.json` — previous scores and feedback
3. `git log --oneline -15` — what changed recently
4. `skills/social-image/SKILL.md` — the skill you are improving

Determine your **iteration number** from scores.json (count entries in `iterations` array + 1).

---

## Step 1: Generate HTML

Run the social-image skill to produce HTML slides:

- **Source**: `{{TEST_ARTICLE}}`
- **Params**: `--ratio 9:16 --theme {{THEME}} --slides {{SLIDES}} --tone {{TONE}}`
- Follow SKILL.md Steps 0–3. Output HTML to `skills/social-image/slides/`.

---

## Step 2: Fill Check (gate — do not proceed until passed)

For each non-cover slide HTML:

1. Read the file. Calculate: `content_height` = sum of all element heights (h2≈80px, h3≈60px, p≈50px/line, li≈60px, code≈40px/line, blockquote≈80px, visual components by their defined height).
2. Available height for 9:16 = **1652px** (1920 − 268px padding/chrome).
3. **Pass condition**: content fills ≥95% of available height. Gap between last element and page-number ≤ 80px.
4. If fail: add content from source article, add visual fill components, increase typography scale. Re-check.
5. Repeat until every slide passes. Max 3 inner iterations per slide.

---

## Step 3: Render to PNG

```python
# Save as /tmp/render_ralph.py and run with python3
from playwright.sync_api import sync_playwright
import glob, os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    os.makedirs("output", exist_ok=True)
    for f in sorted(glob.glob("skills/social-image/slides/*.html")):
        page.goto("file://" + os.path.abspath(f))
        page.wait_for_timeout(1000)
        page.screenshot(path=f"output/{os.path.splitext(os.path.basename(f))[0]}.png", full_page=False)
    browser.close()
```

---

## Step 4: Blind Review (sub-agent)

For **each content slide** PNG (skip cover.png), spawn a **fresh sub-agent** via the Agent tool. The sub-agent receives ONLY the image + this prompt:

```
You are a blind visual reviewer. You know nothing about this project.

Score this social media slide image on 6 dimensions (1–5 each):

1. **{{DIM_1_NAME}}**: {{DIM_1_DESC}}
2. **{{DIM_2_NAME}}**: {{DIM_2_DESC}}
3. **{{DIM_3_NAME}}**: {{DIM_3_DESC}}
4. **{{DIM_4_NAME}}**: {{DIM_4_DESC}}
5. **{{DIM_5_NAME}}**: {{DIM_5_DESC}}
6. **{{DIM_6_NAME}}**: {{DIM_6_DESC}}

Scale: 5=flawless 4=minor nitpick 3=noticeable issue 2=significant problem 1=broken
Be strict. 5 means zero issues. For any score <5, state the exact problem.

Reply with ONLY this JSON:
{"d1":N,"d2":N,"d3":N,"d4":N,"d5":N,"d6":N,"total":N,"pass":BOOL,"feedback":["issue"]}
pass=true only when total==30.
```

Pass the PNG file path so the agent can read the image.

---

## Step 5: Decide

Take the **minimum total score** across all slides.

- **30/30 on ALL slides** → Step 6
- **Any slide < 30** → Step 7

---

## Step 6: Ship It

```
1. Update scores.json: add {"iteration": N, "scores": {...}, "result": "PASS"}
2. Append to progress.txt:
   ## Iteration N — PASS ✓ (YYYY-MM-DD)
   All slides: 30/30
3. git add skills/social-image/ output/ && git commit -m "ralph: PASS 30/30"
```

Then output exactly: `<promise>COMPLETE</promise>`

---

## Step 7: Root-Cause Fix (improve the SKILL, not the output)

**Do NOT just patch the current HTML.** Fix the source of truth.

### 7a. Diagnose

Group sub-agent feedback into categories:
- **Fill**: whitespace, empty gaps, sparse content
- **Typography**: font size, line height, weight hierarchy
- **Layout**: alignment, spacing, element distribution
- **Density**: too little text, shallow content, padding filler
- **Aesthetics**: color, contrast, visual components
- **Consistency**: cross-slide style variation

### 7b. Trace to SKILL.md

For each category with issues, find the specific section in SKILL.md that:
- Gave insufficient instruction (missing rule)
- Gave wrong instruction (bad default value)
- Failed to enforce a constraint (no verification step)

### 7c. Edit

Make surgical edits to `skills/social-image/SKILL.md`. Also fix `assets/base.css` or theme CSS if the issue is structural. Each edit must have a clear rationale tied to sub-agent feedback.

### 7d. Record

Append to `progress.txt`:
```
## Iteration N — FAIL (YYYY-MM-DD)
Score: X/30 (worst slide: slide_NN)
Issues: [category]: [specific feedback]
Fix: [file]: [what changed] — because [rationale]
Next iteration should: [actionable advice]
```

Update `scores.json`:
```json
{"iteration": N, "slide_scores": {...}, "worst": X, "result": "FAIL", "changes": ["file:change"]}
```

Commit: `git add -A && git commit -m "ralph: iter N — X/30, fix [category]"`

Do NOT output `<promise>COMPLETE</promise>`.

---

## Rules

- Sub-agents MUST be fresh (Agent tool, no context reuse)
- Never skip blind review — no self-scoring
- Never output `<promise>COMPLETE</promise>` unless every slide is 30/30
- Always edit SKILL.md — that is the whole point of this loop
- Always write to progress.txt — it is the next iteration's only memory
- Never invent article content — only use source material
