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

Each non-cover slide: pure blank area ≤ 1% of page. Available height = **1652px** (1920 − 268).

If blank > 1%: match content semantic → add visual fill component from this table:

| 内容语义 | 推荐组件 |
|---------|---------|
| 步骤/工具/流程 | 流程图、时间轴、漏斗图、甘特图 |
| 对比/选择/优劣 | VS 对比卡、决策树、对比表格、优劣势色块 |
| 数字/结论/数据 | 数据高亮块、进度条、饼图/环形图、气泡图 |
| 定义/概念/理论 | 概念图、公式框、名词解释卡片、Callout 提示框 |
| 多要素关联 | 维恩图、四象限矩阵、循环图、鱼骨图 |
| 要点/关键词/总结 | icon 标签云、编号卡片网格、Checklist、标签徽章 |
| 观点/金句/引用 | Quote 引用块、对话气泡、高亮色块、人物卡片 |

Component must use same theme colors/fonts. Max 3 retries per slide.

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

Spawn **one Agent per content slide** (skip cover). Each sub-agent receives ONLY the slide screenshot + the rubric below. No project context. No memory.

Sub-agent prompt — copy exactly:

~~~
你是一个盲审视觉评审员。你对这个项目没有任何上下文。
请严格按照以下 6 个维度为这张社交媒体幻灯片图片打分。

## 1. 可读性（10 分）
- 字体大小不小于 28px（手机端阅读友好）
- 每页文字量控制在 80-150 字之间（信息密度适中，不压迫）
- 行间距 ≥ 1.6 倍，段间距明显区分
- 标题与正文有清晰的视觉层级（字号/粗细/颜色至少两项有区别）
- 文字与背景对比度符合 WCAG AA 标准（对比度 ≥ 4.5:1）

## 2. 视觉美学（10 分）
- 整体配色不超过 3-4 个主色，风格统一
- 排版有呼吸感：留白合理但不空洞（正文页内容占比 30%-80%）
- 元素对齐一致（左对齐或居中，不混用）
- 页与页之间风格一致（字体、配色、版式统一）
- 有适当的装饰元素（分隔线、icon、色块）但不喧宾夺主

## 3. 小红书平台适配（10 分）
- 封面页有吸引力的大标题 + 副标题/hook，能激发点击欲
- 末页有明确的 CTA（关注/收藏/评论引导）
- 文案风格口语化、有人感，避免公文/论文腔

## 4. 内容结构（10 分）
- 封面 → 痛点/hook → 核心内容 → 总结/CTA，逻辑链完整
- 每页有一个清晰的核心观点（不贪多）
- 善用编号、分点、对比等结构化表达
- 关键信息有视觉强调（加粗、高亮色块、放大字号）

## 5. 信息完整度（10 分）
- 原文核心观点无遗漏
- 转化过程中没有扭曲原意
- 适当补充了过渡语让图文版更流畅
- 信息密度均匀分布，没有某页过载、某页过空

## 6. 空白控制（10 分）
- 每页非封面页，纯空白区域不得超过页面总面积的 1%
- 当空白超标时，应根据内容语义自动生成静态前端组件填充
- 组件须与整页配色、字体保持一致，不喧宾夺主
- 语义匹配规则：
  | 内容语义 | 推荐组件 |
  |---------|---------|
  | 步骤/工具/流程 | 流程图、时间轴、漏斗图、甘特图 |
  | 对比/选择/优劣 | VS 对比卡、决策树、对比表格、优劣势色块 |
  | 数字/结论/数据 | 数据高亮块、进度条、饼图/环形图、气泡图 |
  | 定义/概念/理论 | 概念图、公式框、名词解释卡片、Callout 提示框 |
  | 多要素关联 | 维恩图、四象限矩阵、循环图、鱼骨图 |
  | 要点/关键词/总结 | icon 标签云、编号卡片网格、Checklist、标签徽章 |
  | 观点/金句/引用 | Quote 引用块、对话气泡、高亮色块、人物卡片 |

---

10 分 = 该维度零问题。<10 分 = 必须说明扣分原因。

仅输出 JSON:
{"readability":N,"aesthetics":N,"xhs_fit":N,"structure":N,"completeness":N,"whitespace":N,"total":N,"pass":BOOL,"feedback":["扣分原因1","扣分原因2"]}
pass=true 当且仅当 total==60。
~~~

## 5. Branch

- ALL slides 60/60 → **Step 6**
- ANY slide <60 → **Step 7**

## 6. Done

Update scores.json, append `## Iter N — PASS` to progress.txt, commit, then:

`<promise>COMPLETE</promise>`

## 7. Root-Cause Fix

**Do NOT patch HTML. Fix SKILL.md.**

Think step by step:
1. List every feedback item. Group into: 可读性 | 视觉美学 | 小红书适配 | 内容结构 | 信息完整度 | 空白控制
2. For each group, identify the SKILL.md section that should have prevented the issue
3. Determine: is the rule missing, too weak, or wrong?
4. Edit `SKILL.md` (and `assets/*.css` if structural). One edit per identified cause.

Record in progress.txt:
```
## Iter N — FAIL (YYYY-MM-DD) Score: X/60
[维度]: [扣分原因] → [file:section]: [修改内容] — [为什么这样改]
Next iter: [下一轮关注点]
```

Update scores.json. Commit. Do NOT output `<promise>COMPLETE</promise>`.

## Rules

- Sub-agents: fresh per slide, zero shared context
- Never self-score. Never skip blind review.
- `<promise>COMPLETE</promise>` only at 60/60 on every slide
- Always edit SKILL.md — that is the point
- Always write progress.txt — it is the next iteration's memory
- Never invent content — source article only
