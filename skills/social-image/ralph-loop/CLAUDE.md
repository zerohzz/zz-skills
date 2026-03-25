# Ralph Loop — Social Image Quality

Zero memory per iteration. State lives in `progress.txt`, `scores.json`, and git.

## 0. Orient

```
Read: progress.txt → scores.json → git log --oneline -15 → SKILL.md
```

Infer iteration number from `scores.json.iterations.length + 1`.

## 1. Generate

Run social-image skill (Steps 0–3):
- Source: `{{TEST_ARTICLE}}`
- Params: `--ratio 9:16 --theme {{THEME}} --slides {{SLIDES}} --tone {{TONE}}`
- Output: `skills/social-image/slides/*.html`

## 2. Fill Gate

Each non-cover slide must pass before proceeding:

| Element | Est. height |
|---------|-------------|
| h2 | 80px |
| h3 | 60px |
| p (per line, ~18 chars) | 50px |
| li | 60px |
| code (per line) | 40px |
| blockquote | 80px |

Available = **1652px** (1920 − 268). Pass = gap ≤ 80px from last element to page-number. If fail: add source content, add visual components, scale typography. Max 3 retries per slide.

## 3. Render

```python
from playwright.sync_api import sync_playwright
import glob, os
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1080,"height":1920})
    os.makedirs("output",exist_ok=True)
    for f in sorted(glob.glob("skills/social-image/slides/*.html")):
        pg.goto("file://"+os.path.abspath(f)); pg.wait_for_timeout(1000)
        pg.screenshot(path=f"output/{os.path.splitext(os.path.basename(f))[0]}.png",full_page=False)
    b.close()
```

## 4. Blind Score

Spawn **one Agent per content slide** (skip cover). Sub-agent prompt — copy exactly:

```
Blind visual reviewer. No project context.

Score this social media slide (1–5 per dimension, 5=flawless):

1. {{DIM_1}}: {{DESC_1}}
2. {{DIM_2}}: {{DESC_2}}
3. {{DIM_3}}: {{DESC_3}}
4. {{DIM_4}}: {{DESC_4}}
5. {{DIM_5}}: {{DESC_5}}
6. {{DIM_6}}: {{DESC_6}}

5=zero issues. <5=state exact problem.

JSON only:
{"d1":N,"d2":N,"d3":N,"d4":N,"d5":N,"d6":N,"total":N,"pass":BOOL,"feedback":["..."]}
pass=true iff total==30.
```

## 5. Branch

- ALL slides 30/30 → **Step 6**
- ANY slide <30 → **Step 7**

## 6. Done

Update scores.json, append `## Iter N — PASS` to progress.txt, commit, then:

`<promise>COMPLETE</promise>`

## 7. Root-Cause Fix

**Do NOT patch HTML. Fix SKILL.md.**

Think step by step:
1. List every feedback item. Group into: Fill | Typography | Layout | Density | Aesthetics | Consistency
2. For each group, identify the SKILL.md section that should have prevented the issue
3. Determine: is the rule missing, too weak, or wrong?
4. Edit `SKILL.md` (and `assets/*.css` if structural). One edit per identified cause.

Record in progress.txt:
```
## Iter N — FAIL (YYYY-MM-DD) Score: X/30
[category]: [feedback] → [file:section]: [edit made] — [why]
Next iter: [what to watch for]
```

Update scores.json. Commit. Do NOT output `<promise>COMPLETE</promise>`.

## Rules

- Sub-agents: fresh per slide, zero shared context
- Never self-score. Never skip blind review.
- `<promise>COMPLETE</promise>` only at 30/30 on every slide
- Always edit SKILL.md — that is the point
- Always write progress.txt — it is the next iteration's memory
- Never invent content — source article only
