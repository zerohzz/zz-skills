---
name: write-prompt
description: >-
  Research-backed prompt optimizer with diagnostic analysis. Three modes:
  "optimize" diagnoses intent and complexity, selects the best structural
  pattern, and applies technique modules (CoT, examples, verification).
  "refine" makes surgical three-layer improvements. "plan" decomposes goals
  into executable prompt chains. Use this skill whenever the user mentions
  prompt optimization, prompt improvement, prompt engineering, or asks for
  help writing better prompts — even if they don't say "optimize" explicitly.
  Triggers on: "optimize prompt", "improve prompt", "improve my prompt",
  "help me write a prompt", "make this prompt better", "refine prompt",
  "优化提示词", "优化prompt", "改进提示词", "帮我写提示词", "精炼",
  "how to prompt for", "rewrite this prompt". Also use when the user pastes
  a prompt and asks for feedback, or says something like "this prompt isn't
  working well". Do NOT trigger when user says "optimize code", "optimize
  performance", "优化代码" — those are refactoring tasks, not prompt work.
version: 2.0.0
---

# Prompt Optimizer

Research-backed prompt optimization skill. Analyzes prompts using a diagnostic framework, selects the best structural pattern for the task, and applies proven techniques (Chain-of-Thought, few-shot examples, self-verification) to produce higher-quality AI outputs.

## Modes

| Mode | Trigger | What it does |
|------|---------|-------------|
| **optimize** | Default, or user says "optimize", "restructure", "优化" | Diagnose → select structural pattern → apply technique modules → output optimized prompt |
| **refine** | User says "refine", "polish", "make precise", "精炼" | Three-layer surgical improvement: clarity → completeness → technique enhancement |
| **plan** | User says "plan", "步骤化", "step by step", "break down" | Decompose goal into a sequence of linked prompts (prompt chain) |

## Critical Rules

- **Optimize ≠ Execute**: You are improving the prompt text itself, not executing it. If someone asks you to optimize a prompt about writing code, your job is to improve the prompt — not write the code. This is the most common mistake.
- **Preserve intent**: The user's core goal must not change. Optimization adds structure and precision around the goal, not a different goal.
- **Preserve variables**: Keep `{{variable}}` placeholders exactly as-is — they are intentional blanks for the user to fill.
- **Technique proportionality**: A simple request deserves a concise optimized prompt. Wrapping "write me a haiku" in a 500-word Role/Skills/Rules structure would make it worse, not better. Match the weight of the output to the complexity of the task.
- **Pattern fit**: Not every prompt needs a Role/persona. A classification task needs examples, not a character backstory. Choose the pattern that actually helps.
- **Demonstrate, don't describe**: When adding few-shot examples, generate realistic concrete examples with real-looking data — not "[example input]" placeholders. Examples teach patterns implicitly, which research shows is more effective than verbose instructions.
- **No fabrication**: Don't add requirements the user never implied. Optimization sharpens what's there; it doesn't invent new scope.
- **Direct output only**: Output the optimized prompt directly. No "Here's the optimized version:" prefix. No code fences wrapping it. The user should be able to copy-paste your output immediately.

## Workflow

1. **Detect language**: Match the user's language (Chinese → Chinese, English → English)
2. **Detect mode**: Default to `optimize`; use `refine` if the input is already well-structured; use `plan` if the user requests it or the goal clearly requires multiple phases
3. **Run diagnostic analysis** (internal — see below)
4. **Apply the selected mode**
5. **Output ONLY the optimized prompt** — no preamble, no wrapping, no explanation

---

## Internal Diagnostic Framework

Before optimizing, analyze the input prompt internally. This guides your strategy selection — do NOT show this analysis to the user.

### Step 1 — Classify Intent

| Category | Signal words |
|----------|-------------|
| Generation | write, create, draft, generate, build, design |
| Analysis | review, analyze, evaluate, compare, assess, audit |
| Transformation | convert, translate, reformat, summarize, adapt |
| Reasoning | solve, decide, calculate, debug, explain, prove |
| Conversation | role-play, tutor, coach, advise, interview |
| Extraction | find, extract, identify, classify, categorize, parse |

### Step 2 — Assess Complexity

| Level | Criteria |
|-------|---------|
| SIMPLE | Single clear task, one-shot capable, minimal ambiguity |
| MODERATE | Multiple requirements, benefits from structure and constraints |
| COMPLEX | Multi-step, needs decomposition, reasoning chain, or multiple examples |

### Step 3 — Identify Weaknesses

Check for these common gaps:
- Missing persona or role definition (when a persona would help)
- Missing context or background
- Vague qualifiers ("good", "detailed", "comprehensive") without specifics
- No output format specified
- No constraints or scope boundaries
- No examples for pattern-based tasks
- No reasoning guidance for analytical tasks
- No success criteria

### Step 4 — Select Strategy

Use intent + complexity + weaknesses to choose:

| Complexity | Recommended Pattern | Techniques to Consider |
|-----------|-------------------|----------------------|
| SIMPLE | Task-Directive | Output format, constraints |
| MODERATE | Role-System or Task-Directive | + CoT if reasoning, + examples if pattern-based |
| COMPLEX | Decomposed or Reasoning-Chain | + Self-verification, + examples, + edge cases |

For Extraction/Classification tasks at any complexity, prefer Few-Shot pattern.
For Conversation tasks, prefer Role-System pattern.

---

## Mode: optimize

Transform a raw prompt into a structured, technique-enhanced prompt. Run the diagnostic framework, select the best-fit pattern, apply relevant technique modules, then output the result.

### Structural Patterns

Select ONE pattern based on your diagnosis.

#### Pattern A: Role-System

Best for persona-driven tasks (writing, tutoring, reviewing, advising).

```
# Role: [Specific expert role with domain qualifiers]

## Context
[What the user is working on, why they need this, relevant background]

## Instructions
1. [Specific, actionable directive]
2. [Specific, actionable directive]
3. [Specific, actionable directive]

## Constraints
- [What NOT to do]
- [Boundaries: tone, audience, length, scope]

## Output Format
[Exact format specification — structure, sections, length]
```

#### Pattern B: Task-Directive

Best for action-oriented tasks (generate X, analyze Y, build Z).

```
## Task
[Single clear sentence stating the objective]

## Context
[Background information needed to complete the task]

## Requirements
1. [Specific requirement with measurable criteria]
2. [Specific requirement with measurable criteria]
3. [Specific requirement with measurable criteria]

## Constraints
- [Scope boundaries and exclusions]
- [Format, tone, length limits]

## Output Format
[Exact format specification]
```

#### Pattern C: Reasoning-Chain

Best for analytical and reasoning tasks (solve, decide, debug, explain).

```
## Task
[Clear problem statement]

## Approach
Think through this step by step:
1. First, [specific reasoning step relevant to the task]
2. Then, [specific reasoning step]
3. Finally, [specific reasoning step]

## Verification
Before giving your final answer, check that:
- [Specific verification criterion]
- [Specific verification criterion]

## Output Format
[Format specification — show reasoning and conclusion separately]
```

#### Pattern D: Few-Shot

Best for pattern-matching tasks (classification, formatting, extraction, translation).

```
## Task
[What to do with each input]

## Examples

Input: [realistic example 1]
Output: [correct output 1]

Input: [realistic example 2]
Output: [correct output 2]

Input: [realistic example 3 — edge case]
Output: [correct output 3]

## Rules
[Any rules not fully captured by the examples]

Now process the following:
Input: {{user_input}}
```

#### Pattern E: Decomposed

Best for complex multi-step tasks that benefit from explicit sub-task structure.

```
## Objective
[High-level goal in one sentence]

## Step 1: [Sub-task name]
[Specific instructions for this sub-task]

## Step 2: [Sub-task name]
[Specific instructions — may reference output of Step 1]

## Step 3: [Sub-task name]
[Specific instructions]

## Final Output
[How to combine and present the results]
```

### Technique Modules

After selecting a pattern, append any of these modules when the diagnosis warrants it. Weave them naturally into the chosen pattern — do not add them as disconnected appendices.

| Module | When to apply | What to add |
|--------|--------------|-------------|
| **Chain-of-Thought** | Task requires reasoning or multi-step analysis | Add explicit reasoning steps: "Think through X before concluding" or a structured approach section |
| **Few-Shot Examples** | Task is pattern-based and benefits from demonstrations | Generate 2-3 realistic input/output pairs showing the desired behavior |
| **Self-Verification** | Accuracy is critical; output has verifiable criteria | Add "Before finalizing, verify that:" section with task-specific checks |
| **Audience & Tone** | No audience or tone defined; output quality depends on voice | Add explicit audience definition, tone directive, and register |
| **Edge Case Handling** | Task has obvious corner cases or failure modes | Add "Handle these edge cases:" section or weave into constraints |

---

## Mode: refine

For prompts that already have usable structure. Apply surgical improvements across three layers. Preserve the original structure and voice.

### Layer 1 — Clarity (always apply)

- Replace every vague qualifier with a specific one ("detailed" → "covering X, Y, Z in 2-3 sentences each")
- Replace implicit assumptions with explicit statements
- Add scope boundaries (what is in/out of scope)
- Define ambiguous terms
- Remove redundancy

### Layer 2 — Completeness (apply based on gaps)

- Add output format if missing
- Add constraints or boundaries if missing
- Add context/background if the task depends on unstated assumptions
- Add success criteria if "done" is undefined
- Add edge case handling if the task has obvious corner cases

### Layer 3 — Technique Enhancement (apply when it would meaningfully improve results)

- Add reasoning directive if the task involves analysis or decision-making
- Add few-shot examples if the task is pattern-based and has none
- Add self-verification step if accuracy is critical
- Add decomposition if the prompt tries to do too much in one shot

### Refine Rules

- Make surgical improvements, not wholesale rewrites
- If the prompt is already strong, make minimal changes
- Never change the prompt's structural pattern unless it is clearly wrong
- When in doubt, improve less rather than more

---

## Mode: plan

Convert a goal into an executable **prompt chain** — a sequence of prompts where each builds on the previous one's output.

### Process

1. Analyze the goal to identify required phases
2. For each phase, generate a standalone optimized prompt (using the optimize logic above)
3. Link prompts by specifying what output feeds into the next
4. Add a coordination header

### Output Format

```
# Prompt Chain: [Goal]

## Overview
[1-2 sentences describing the approach]
Total prompts: N

---

## Prompt 1 of N: [Phase name]

[Full optimized prompt for this phase]

**Feed forward →** [What output from this prompt to pass to the next]

---

## Prompt 2 of N: [Phase name]

[Full optimized prompt — references {{output from Prompt 1}} where needed]

**Feed forward →** [What to pass forward]

---

## Prompt N of N: [Final phase name]

[Full optimized prompt for final assembly/delivery]
```

### Plan Rules

- Each prompt in the chain must be self-contained and independently executable (given the feed-forward input)
- If the goal is simple enough for a single prompt, produce one optimized prompt instead and note: "This goal is achievable in a single prompt."
- Keep chains short: 2-4 prompts for most goals, 5+ only for genuinely complex projects

---

## Examples

### Example 1: optimize — simple generation task

**Input**: "Help me write marketing copy"

**Output**:

## Task
Write compelling marketing copy for {{product/service}}.

## Context
- Product/service: {{brief description}}
- Target audience: {{who you're trying to reach}}
- Goal: {{awareness / conversion / retention}}

## Requirements
1. Open with a hook that addresses the audience's core pain point
2. Highlight 3 key benefits (not features) with concrete outcomes
3. Include one proof point (statistic, testimonial, or case study)
4. End with a clear, single call-to-action

## Constraints
- Length: 150 words maximum
- Tone: conversational and confident, not salesy or hyperbolic
- No jargon, no clichés ("revolutionize", "game-changing", "synergy")
- No false urgency ("Act now!", "Limited time!")

## Output Format
Deliver as:
- **Headline** (under 10 words)
- **Body** (2-3 short paragraphs)
- **CTA** (one sentence)

---

### Example 2: optimize — reasoning task

**Input**: "Review my code"

**Output**:

# Role: Senior Code Reviewer

## Context
Review the provided code for production readiness. The review should be thorough enough to catch bugs before they reach users, but practical — focus on issues that matter.

## Instructions
For each file, work through this process:
1. Read the code and understand the intent before looking for problems
2. Check correctness: logic errors, off-by-one errors, null/undefined edge cases, race conditions
3. Check security: injection vulnerabilities, auth bypasses, data exposure, unsafe deserialization
4. Check performance: unnecessary allocations, O(n²) where O(n) is possible, missing pagination
5. Check readability: unclear naming, functions over 40 lines, deep nesting, missing error handling

## Verification
Before finalizing your review, verify that:
- Every issue references a specific location (file + line or code snippet)
- Every issue includes a concrete fix suggestion, not just "this is bad"
- You have not flagged stylistic preferences as bugs

## Constraints
- Prioritize: bugs and security issues first, performance second, style last
- If the code is solid, say so briefly — don't manufacture issues
- Do not rewrite the code; suggest targeted fixes

## Output Format
| Location | Severity | Issue | Suggested Fix |
|----------|----------|-------|---------------|
| file:line | critical/warning/suggestion | Description | Fix |

Summary: 1-2 sentences on overall code quality.

---

### Example 3: refine

**Input**: "You are a helpful travel assistant. Help me plan a trip to Japan. Consider my budget and preferences."

**Output**:

You are a travel planning specialist with deep knowledge of Japan — transportation systems (JR Pass, IC cards, domestic flights), accommodation types (ryokan, business hotels, hostels), regional cuisine, and seasonal events.

Plan a {{duration}}-day itinerary for Japan.

Traveler profile:
- Budget: {{total budget}} USD (excluding international flights)
- Interests: {{pick from: temples/shrines, food/cooking, nature/hiking, pop culture/anime, nightlife, shopping, history, onsen}}
- Travel style: {{fast-paced sightseeing / relaxed with downtime / mix}}
- Dates: {{travel dates — affects weather, cherry blossom, festivals}}

For each day, provide:
1. Location and transit instructions (how to get there, which train/bus, cost)
2. Morning, afternoon, and evening activities with estimated time
3. Meal recommendations (specific restaurant names or food streets, with price range)
4. Estimated daily spend breakdown (transport / food / activities / accommodation)

Constraints:
- Stay within the total budget — show a running total
- Minimize backtracking (logical geographic flow)
- Include at least one off-the-beaten-path recommendation per city

Output as a day-by-day markdown itinerary with a budget summary table at the end.

---

### Example 4: plan — prompt chain

**Input**: "I want to build a Chrome extension"

**Output**:

# Prompt Chain: Build a Chrome Extension

## Overview
Specify → Implement → Review. Each prompt produces a deliverable that feeds into the next.
Total prompts: 3

---

## Prompt 1 of 3: Specification

## Task
Define the specification for a Chrome extension that {{describe what it does}}.

## Requirements
1. Research Chrome Extension Manifest V3 capabilities relevant to this use case
2. Identify minimum permissions needed (prefer narrow permissions)
3. List core features (MVP only — no nice-to-haves)
4. Define the user interaction flow: what the user clicks, sees, and gets

## Output Format
- **Purpose**: One sentence
- **Permissions**: List with justification for each
- **Features**: Numbered MVP list
- **User Flow**: Step-by-step interaction
- **File Structure**: Expected files and their roles

**Feed forward →** Pass the full specification to Prompt 2.

---

## Prompt 2 of 3: Implementation

## Task
Implement the Chrome extension defined in this specification: {{spec from Prompt 1}}

## Requirements
1. Use Manifest V3, minimal permissions, proper content security policy
2. Handle errors gracefully — user-friendly messages, never fail silently
3. Clean, readable code with comments for non-obvious logic
4. Include a `README.md` with install and usage instructions

## Output Format
All files with full content, organized by the file structure from the spec.

**Feed forward →** Pass all implementation files to Prompt 3.

---

## Prompt 3 of 3: Review & Polish

# Role: Senior Chrome Extension Reviewer

## Context
Review this Chrome extension for production readiness: {{files from Prompt 2}}

## Instructions
1. Check Manifest V3 compliance and permission minimality
2. Check security: XSS in content scripts, unsafe message passing, overly broad host permissions
3. Check error handling and edge cases (no active tab, permission denied, network failure)
4. Suggest UX improvements (icons, popup layout, keyboard shortcuts)

## Output Format
1. **Issues**: table with severity, location, fix
2. **Corrected files**: re-deliver changed files with fixes applied
3. **Store listing draft**: name, short description, detailed description
