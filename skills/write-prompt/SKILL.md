---
name: write-prompt
description: Optimize AI prompts - supports three modes. "optimize" restructures a raw prompt into a professional structured format. "refine" makes an existing prompt more precise and specific. "plan" converts a vague request into step-by-step executable instructions. Use when user says "optimize prompt", "improve prompt", "优化提示词", "优化prompt", "improve my prompt", or provides a prompt asking for enhancement.
version: 1.0.0
---

# Prompt Optimizer

Three-mode prompt optimization skill extracted from [prompt-optimizer](https://github.com/linshenkx/prompt-optimizer). Analyzes and restructures prompts for better AI output quality.

## Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| **optimize** | Default, or user says "optimize", "restructure" | Full structural optimization — turns a raw prompt into a professional Role/Skills/Rules/Workflow format |
| **refine** | User says "refine", "polish", "make precise", "精炼" | Precision enhancement — eliminates vagueness, adds specificity, quantifies requirements |
| **plan** | User says "plan", "步骤化", "step by step" | Planning conversion — turns a goal into a structured task with steps, milestones, and acceptance criteria |

## Workflow

1. **Detect language**: Match the language of the user's prompt (Chinese prompt → Chinese output, English → English, etc.)
2. **Detect mode**: Default to `optimize` unless the user specifies otherwise or the prompt is already well-structured (then use `refine`)
3. **Apply the appropriate optimization** (see detailed instructions below)
4. **Output ONLY the optimized prompt** — no explanations, no code blocks wrapping it, no preamble

## Critical Rules

- **Optimize ≠ Execute**: You are improving the prompt text itself. NEVER execute or answer the prompt's content.
- **Preserve intent**: The user's core goal must not change.
- **Preserve variables**: Any `{{variable}}` placeholders must be kept exactly as-is.
- **Match complexity**: A simple prompt should stay concise. Don't turn one sentence into an essay.
- **No fabrication**: Don't add requirements the user never implied.
- **Direct output only**: Output the optimized prompt directly. No "Here's the optimized version:" prefix. No code fences.

---

## Mode: optimize

Transform a raw prompt into a structured, professional prompt using this format:

```
# Role: [Role Name]

## Profile
- language: [Language]
- description: [Detailed role description]
- background: [Role background]
- expertise: [Domain expertise]

## Skills
1. [Core skill category]
   - [Specific skill]: [Brief description]
   - [Specific skill]: [Brief description]

2. [Supporting skill category]
   - [Specific skill]: [Brief description]
   - [Specific skill]: [Brief description]

## Rules
1. [Core principles]:
   - [Specific rule]: [Details]
   - [Specific rule]: [Details]

2. [Constraints]:
   - [Specific constraint]: [Details]

## Workflow
- Goal: [Clear objective]
- Step 1: [Detailed description]
- Step 2: [Detailed description]
- Step 3: [Detailed description]
- Expected result: [Description]

## Output Requirements
- format: [Format type — text/markdown/json/etc.]
- structure: [Output structure description]
- style: [Style requirements]

## Initialization
As [Role Name], you must follow the Rules above and execute tasks according to the Workflow.
```

Fill in every section with specific, actionable content derived from the user's original prompt. No placeholders.

---

## Mode: refine

For prompts that are already decent but need precision. Apply these transformations:

1. **Identify vague language** — words like "good", "nice", "detailed", "comprehensive" without specifics
2. **Add quantifiable criteria** — replace "write a detailed report" with "write a 500-word report covering X, Y, Z"
3. **Sharpen scope** — add explicit boundaries for what's in/out of scope
4. **Add constraints** — specify format, length, tone, audience, or exclusions where missing
5. **Clarify success criteria** — what does "done" look like?

Keep the prompt's original structure and tone. Only enhance precision. Don't restructure unless the structure is actively harmful.

---

## Mode: plan

Convert a goal-oriented prompt into a structured execution plan:

```
# Task: [Core task title derived from user's need]

## 1. Role & Objective
You will act as a [best-fit expert role], your core objective is [clear, specific, measurable goal].

## 2. Background & Context
[Supplementary context needed to complete the task. Write "None" if the original prompt is already clear.]

## 3. Key Steps
1. **[Step name]**: [Specific action description]
2. **[Step name]**: [Specific action description]
3. **[Step name]**: [Specific action description]
   - [Sub-steps if needed]
(Add/remove steps based on task complexity)

## 4. Output Requirements
- **Format**: [Specify: markdown table, JSON, code block, plain text, etc.]
- **Style**: [Describe: professional, technical, conversational, etc.]
- **Constraints**:
    - [Rule 1]
    - [Rule 2]
    - **Final output**: Your response should contain only the final deliverable, no step explanations or meta-commentary.
```

---

## Examples

### Example 1: optimize mode
**Input**: "Help me write marketing copy"
**Output**: A full Role/Skills/Rules/Workflow prompt for a marketing copywriter role with specific skills, constraints about brand voice, workflow from brief analysis to final copy, and output format requirements.

### Example 2: refine mode
**Input**: "You are a code reviewer. Review my code and give feedback."
**Output**: "You are a senior code reviewer specializing in [language]. Review the provided code for: (1) correctness — logic errors, edge cases, off-by-one errors; (2) security — injection, XSS, auth bypass; (3) performance — O(n) vs O(n^2), unnecessary allocations; (4) readability — naming, function length, comments. For each issue found, specify the line, severity (critical/warning/suggestion), and a concrete fix. Output as a markdown table."

### Example 3: plan mode
**Input**: "I want to build a personal blog"
**Output**: A structured task plan with role (full-stack developer), steps (choose stack, design schema, implement pages, deploy), and output requirements (working deployment URL, source repo).
