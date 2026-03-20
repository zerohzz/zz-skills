# zz-skills-dev

> **This is the private development repo.** All work and testing happens here before publishing to [`zerohzz/zz-skills`](https://github.com/zerohzz/zz-skills) (public).
>
> 这是私有开发仓库，所有开发和测试在这里完成，确认没有问题后再同步到公开仓库。

---

## Dev → Public Workflow / 发布流程

When changes are ready to publish:

```bash
GITHUB_PAT=ghp_xxx ./sync-public.sh
```

The script will / 脚本会自动：

1. Clone `zz-skills` into a temp directory / clone 公开仓库到临时目录
2. rsync all files across (excluding `.git` and `sync-public.sh` itself) / rsync 所有文件（排除 `.git` 和脚本本身）
3. Commit: `feat: sync from dev YYYY-MM-DD`
4. Push, then clean up the temp directory and PAT / push 后自动清理临时目录和 PAT

**Rules for `zz-skills` (public) / 公开仓库规范：**
- Keep it clean — anyone should be able to install and use every skill / 保持干净，确保所有人能直接使用
- No private data, test files, WIP notes, or personal paths / 无隐私数据、测试文件、未完成的注释、个人路径
- Do all dev work and experimentation here in `-dev` first / 所有开发和实验都先在这里完成

---

Skills shared by zerohzz (alex-huang.dev) for transforming written content into interactive web experiences with Claude Code.

## Prerequisites

- Claude Code installed and running
- Python 3.10+ (for the analysis pipeline scripts)

## Installation

### Quick Install (Recommended)

```bash
npx skills add zerohzz/zz-skills
```

### Register as Plugin Marketplace

Run the following command in Claude Code:

```bash
/plugin marketplace add zerohzz/zz-skills
```

### Install Skills

**Option 1: Via Browse UI**

1. Select **Browse and install plugins**
2. Select **zz-skills**
3. Select the plugin(s) you want to install
4. Select **Install now**

**Option 2: Direct Install**

```bash
/plugin install interactive-web@zz-skills
```

**Option 3: Ask the Agent**

Simply tell Claude Code:

> Please install Skills from github.com/zerohzz/zz-skills

### Available Plugins

| Plugin | Description | Skills |
|--------|-------------|--------|
| **interactive-web** | Transform articles into interactive web experiences | [interactive-web](#interactive-web) |

## Update Skills

To update skills to the latest version:

1. Run `/plugin` in Claude Code
2. Switch to **Marketplaces** tab (use arrow keys or Tab)
3. Select **zz-skills**
4. Choose **Update marketplace**

You can also **Enable auto-update** to get the latest versions automatically.

---

## Available Skills

### interactive-web

Transform blog posts, essays, technical articles, and long-form written content into polished interactive web experiences. This skill is agentic: it runs a structured analysis pipeline, selects the right interaction model, commits to a matching aesthetic direction, and builds a production-quality single-file HTML artifact — without requiring step-by-step guidance.

**Trigger phrases:**

```
"Make this interactive"
"Turn my blog post into a webpage"
"Build an interactive explainer for this"
"Visualize this article"
"Make this explorable"
"Turn this into a mini-site"
```

**From a file:**

```bash
# Give Claude any article and ask it to make it interactive
/interactive-web posts/my-article.md
```

**From a URL:**

```bash
# Claude fetches the article automatically
/interactive-web https://example.com/article
```

**Specify interaction model:**

```bash
/interactive-web posts/my-article.md --model step-sequencer
/interactive-web posts/my-article.md --model comparison-matrix
/interactive-web posts/my-article.md --model timeline
```

**Specify design direction:**

```bash
/interactive-web posts/my-article.md --design dark-technical
/interactive-web posts/my-article.md --design editorial-ink
/interactive-web posts/my-article.md --design claude-like
```

**Combine both:**

```bash
/interactive-web posts/my-article.md --model concept-explorer --design clean-analytical
```

#### Pipeline

The skill runs a 4-stage analysis pipeline before writing any code:

| Stage | Script | Input | Output |
|-------|--------|-------|--------|
| Normalize | `normalize_article.py` | Raw text / URL / file | `normalized.md` |
| Extract | `extract_structure.py` | `normalized.md` | `structure.json` |
| Blueprint | `build_page_plan.py` | `structure.json` | `blueprint.json` |
| Build | Claude (SKILL.md) | `blueprint.json` + article | Single-file HTML |

#### Interaction Models

The skill selects one of 10 patterns based on content type and structure:

| Pattern | Best For |
|---------|----------|
| `scroll-journey` | Narratives, opinion essays, long-form arguments |
| `step-sequencer` | Tutorials, how-tos, implementation walkthroughs |
| `concept-explorer` | Frameworks, layered ideas, capability models |
| `comparison-matrix` | Tool reviews, tradeoff analysis, side-by-side choices |
| `architecture-explainer` | Technical systems, flows, components, integrations |
| `decision-tree` | Strategic guides, diagnostic content, "which one" posts |
| `timeline` | Historical, chronological, before/after evolution |
| `data-dashboard` | Statistics-heavy, research-driven, metric-rich content |
| `filterable-gallery` | Pattern libraries, curated examples, reference roundups |
| `faq-explorer` | Q&A posts, FAQs, question-driven content |

#### Design Directions

| Direction | Character | Fonts | Palette |
|-----------|-----------|-------|---------|
| `dark-technical` | Precision, monospace clarity, analytical depth | IBM Plex Sans + IBM Plex Mono | Dark slate + electric blue |
| `editorial-ink` | Typographic authority, ink-on-paper weight | Playfair Display + Crimson Pro | Aged paper + editorial red |
| `clean-analytical` | Tabular precision, high contrast, chart-friendly | Plus Jakarta Sans + Fira Code | Deep slate + cyan or amber |
| `editorial-warm` | Forward momentum, approachable warmth | Newsreader + Nunito | Warm cream + burnt orange |
| `claude-like` | Quiet confidence, warm restraint, content-forward | Instrument Serif + DM Sans | Warm off-white + terracotta coral |

#### Degradation Logic

The skill explicitly decides when **not** to add interactivity:

- **Upgrade to interactive** when content has explicit phases, comparisons, hierarchies, or data
- **Degrade to static editorial** when content is a short opinion or single argument with no navigable structure

A high-quality static editorial page is a better output than hollow interactivity.

#### Output

The skill produces three things:

1. **Artifact rationale** (3 sentences) — chosen model, design direction, and what interactivity adds
2. **The interactive webpage** — single self-contained `.html` file, open directly in any browser
3. **Reuse notes** — what to swap to adapt this to another article

#### Non-Negotiables

- Never copies paragraphs verbatim — extracts and rebuilds content into interactive treatments
- Never invents sections not in the source article
- Never uses Inter, Roboto, Arial, or System UI fonts
- All interactive elements must be keyboard accessible
- Responsive layout declared for all artifacts

---

## Demo

**Skill Lab page:** [alex-huang.dev/skill-lab/interactive-web](https://alex-huang.dev/skill-lab/interactive-web)

**Live output example** — the page below was generated by running:

```bash
/interactive-web https://alex-huang.dev/posts/ai-website-one-day/ --design claude-like
```

→ [alex-huang.dev/skill-lab/interactive-web-demo.html](https://alex-huang.dev/skill-lab/interactive-web-demo.html)

Source article: [alex-huang.dev/posts/ai-website-one-day](https://alex-huang.dev/posts/ai-website-one-day/)

---

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=zerohzz/zz-skills&type=Date)](https://www.star-history.com/#zerohzz/zz-skills&Date)
