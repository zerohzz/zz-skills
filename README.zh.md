# zz-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md)

由 [zerohzz](https://alex-huang.dev) 分享的 Claude Code 技能集 —— 用于构建互动内容、录制演示、生成社交媒体图片和优化提示词。

## 安装

### 快速安装（推荐）

```bash
npx skills add zerohzz/zz-skills
```

### 注册为插件市场

```bash
/plugin marketplace add zerohzz/zz-skills
```

### 安装单个技能

```bash
/plugin install interactive-web@zz-skills
/plugin install gif-recorder@zz-skills
/plugin install social-image@zz-skills
/plugin install write-prompt@zz-skills
```

或者直接告诉 Claude Code：

> 请从 github.com/zerohzz/zz-skills 安装技能

## 更新

1. 在 Claude Code 中运行 `/plugin`
2. 切换到 **Marketplaces** 标签
3. 选择 **zz-skills** → **Update marketplace**

开启 **auto-update** 即可自动获取最新版本。

## 技能一览

| 技能 | 描述 |
|------|------|
| [interactive-web](#interactive-web) | 将文章转化为互动网页体验 |
| [gif-recorder](#gif-recorder) | 将任意网站录制为精美的 GIF 动图 |
| [social-image](#social-image) | 将内容转化为多页小红书/Instagram 图文轮播 |
| [write-prompt](#write-prompt) | 优化和精炼 AI 提示词 |

---

### interactive-web

将博客文章、随笔和技术文章转化为精美的互动网页体验。自动运行结构化分析流水线，选择合适的交互模型，匹配美学方向，构建生产级的单文件 HTML。

**使用方法：**

```bash
/interactive-web posts/my-article.md
/interactive-web https://example.com/article
/interactive-web posts/my-article.md --model step-sequencer --design claude-like
```

**触发短语：** `"Make this interactive"` · `"把这篇文章做成网页"` · `"Visualize this article"` · `"Make this explorable"`

<details>
<summary>处理流水线</summary>

| 阶段 | 脚本 | 输入 | 输出 |
|------|------|------|------|
| 标准化 | `normalize_article.py` | 原始文本 / URL / 文件 | `normalized.md` |
| 提取结构 | `extract_structure.py` | `normalized.md` | `structure.json` |
| 生成蓝图 | `build_page_plan.py` | `structure.json` | `blueprint.json` |
| 构建页面 | Claude (SKILL.md) | `blueprint.json` + 文章 | 单文件 HTML |

</details>

<details>
<summary>交互模型</summary>

| 模式 | 适用场景 |
|------|----------|
| `scroll-journey` | 叙事文、观点文章、长篇论述 |
| `step-sequencer` | 教程、操作指南、实现演示 |
| `concept-explorer` | 框架介绍、分层概念、能力模型 |
| `comparison-matrix` | 工具评测、权衡分析、横向对比 |
| `architecture-explainer` | 技术架构、流程、组件、集成方案 |
| `decision-tree` | 策略指南、诊断内容、选择类文章 |
| `timeline` | 历史回顾、时间线、前后对比 |
| `data-dashboard` | 数据密集型、研究驱动、指标丰富的内容 |
| `filterable-gallery` | 模式库、精选案例、参考合集 |
| `faq-explorer` | 问答帖、FAQ、问题驱动的内容 |

</details>

<details>
<summary>设计方向</summary>

| 方向 | 风格特征 | 字体 |
|------|----------|------|
| `dark-technical` | 精确、等宽字体清晰、分析感 | IBM Plex Sans + IBM Plex Mono |
| `editorial-ink` | 排版权威感、墨水纸张质感 | Playfair Display + Crimson Pro |
| `clean-analytical` | 表格精度、高对比度、图表友好 | Plus Jakarta Sans + Fira Code |
| `editorial-warm` | 前进感、亲和温暖 | Newsreader + Nunito |
| `claude-like` | 内敛自信、温暖克制、内容优先 | Instrument Serif + DM Sans |

| 方向 | 预览 |
|------|------|
| `dark-technical` | ![dark-technical](screenshots/dark-technical.gif) |
| `editorial-ink` | ![editorial-ink](screenshots/editorial-ink.gif) |
| `clean-analytical` | ![clean-analytical](screenshots/clean-analytical.gif) |
| `editorial-warm` | ![editorial-warm](screenshots/editorial-warm.gif) |
| `claude-like` | ![claude-like](screenshots/claude-like.gif) |

</details>

<details>
<summary>捆绑样式</summary>

捆绑样式同时锁定视觉风格和交互模型。

| 样式 | 适用场景 | 交互模型 | 字体 |
|------|----------|----------|------|
| `story-scrollytelling` | 叙事散文、长篇论述 | scroll-journey | Cormorant Garamond + Lato |
| `bento-analytical` | 对比评测、数据分析 | comparison-matrix | Plus Jakarta Sans + Fira Code |
| `technical-glow` | 工程架构、系统设计 | architecture-explainer | IBM Plex Sans + IBM Plex Mono |
| `warm-cards` | 教程、操作指南 | step-sequencer | Nunito + Fira Code |
| `glass-layered` | 概念框架、心智模型 | concept-explorer | Space Grotesk + Space Mono |

</details>

**演示：** [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web)

---

### gif-recorder

将任意网站录制为精美的 GIF 动图 —— 适用于 README 演示、社交媒体或演示文稿。完全在 Claude Code 内运行：抓取页面、重建为自包含 HTML、在本地服务、通过 Playwright 录制。

**使用方法：**

```bash
/gif-recorder https://example.com
```

**触发短语：** `"把网站录制成 GIF"` · `"做一个演示 GIF"` · `"录制这个网址"`

<details>
<summary>选项</summary>

**光标模式：**

| 模式 | 效果 | 适用场景 |
|------|------|----------|
| `default` | 白色箭头 | 快速录制、内部演示 |
| `highlight` | 黄色光晕 + 点击涟漪 *（默认）* | 教程、产品演示 |
| `minimal` | 淡白光晕 | 网站演示、设计产品 |
| `animated` | 蓝色多环光晕 + 运动轨迹 | 营销视频、落地页 |

**输出控制：**

```bash
--width 720 --height 1280        # Playwright 视口
--out-width 540 --out-height 960 # GIF 输出分辨率
--max-size 5                     # 限制 5 MB
```

</details>

---

### social-image

将博客文章和长文内容转化为多页小红书/Instagram 图文轮播。分析内容权重，智能分配到各张幻灯片，以原生小红书风格重写文案，通过 Playwright 将每张幻灯片渲染为高质量 PNG。

**使用方法：**

```bash
/social-image posts/my-article.md
/social-image https://example.com/article
/social-image posts/my-article.md --theme sketch --slides 9 --ratio 3:4
```

**触发短语：** `"把这篇文章做成小红书"` · `"做一个轮播图"` · `"生成社交媒体图片"`

<details>
<summary>选项</summary>

| 参数 | 默认值 | 可选值 |
|------|--------|--------|
| `--slides` | 9 | 1–18 |
| `--ratio` | `3:4` | `3:4`（小红书）、`9:16`（Stories）、`1:1`（Feed） |
| `--theme` | 自动 | 见下方 |
| `--lang` | 自动检测 | `zh`、`en` |

**主题：**

| 主题 | 风格特征 |
|------|----------|
| `sketch` | 手绘墨水感，松散而富有表现力 |
| `editorial` | 干净的编辑排版，字体权威感 |
| `terminal` | 暗色等宽字体，代码终端风格 |
| `botanical` | 有机绿色，自然灵感的柔和感 |
| `clean-modern` | 极简留白，现代清晰感 |
| `warm-paper` | 米白纸张色调，亲切温暖 |
| `neo-brutalism` | 粗边框、高对比度、张扬个性 |
| `claude-like` | 内敛自信、温暖克制 |

</details>

---

### write-prompt

AI 提示词优化工具，支持三种模式：**optimize**（重构原始提示词）、**refine**（精炼现有提示词）、**plan**（将模糊需求转化为分步指令）。

**使用方法：**

```bash
/write-prompt optimize "你的原始提示词"
/write-prompt refine "你的现有提示词"
/write-prompt plan "你的模糊需求"
```

**触发短语：** `"优化提示词"` · `"优化 prompt"` · `"Optimize this prompt"` · `"Improve my prompt"`

---

## 环境要求

- 已安装并运行 Claude Code
- Python 3.10+（`interactive-web` 和 `social-image` 的流水线脚本需要）

## 许可证

[MIT](LICENSE)

## Star 趋势

[![Star History Chart](https://api.star-history.com/svg?repos=zerohzz/zz-skills&type=Date)](https://www.star-history.com/#zerohzz/zz-skills&Date)
