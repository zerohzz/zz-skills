#!/usr/bin/env python3
"""
plan_slides.py

Analyze article/markdown content and produce slide_plan.json —
a structured plan telling Claude how to distribute content across
N slides for a social media carousel.

Usage:
    python3 plan_slides.py --input article.md --slides 9 --ratio 3:4 --theme sketch --output slide_plan.json
"""

import sys
import re
import math
import argparse
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BLOCK_WEIGHTS = {
    "heading": {1: 4.0, 2: 3.0, 3: 2.0, 4: 1.5},
    "paragraph": 1.0,
    "code": 2.5,
    "list": 0.8,
    "quote": 1.5,
    "image": 3.0,
}

# Ratio-specific weight targets: taller ratios fit more content per slide
TARGET_WEIGHT_PER_RATIO = {
    "3:4":  6.0,   # baseline
    "9:16": 8.5,   # 42% more content for 57% more height
    "1:1":  4.5,   # 25% less content for 25% less height
}

RATIO_CONFIGS = {
    "3:4":  {"width": 1080, "height": 1440},
    "9:16": {"width": 1080, "height": 1920},
    "1:1":  {"width": 1080, "height": 1080},
}

# CJK Unicode ranges: CJK Unified Ideographs, CJK Extension A, CJK Extension B
CJK_RANGES = [
    (0x4E00, 0x9FFF),
    (0x3400, 0x4DBF),
    (0x20000, 0x2A6DF),
]

DEFAULT_EMOJI_GENERIC = "📖"
DEFAULT_EMOJI_TECHNICAL = "💡"
DEFAULT_EMOJI_NATURE = "🌿"
DEFAULT_EMOJI_CREATIVE = "🎨"


# ---------------------------------------------------------------------------
# HTML stripping (adapted from normalize_article.py)
# ---------------------------------------------------------------------------

def strip_html(html: str) -> str:
    """Remove HTML tags, preserve semantic structure as Markdown."""
    html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', html, flags=re.DOTALL)
    html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', html, flags=re.DOTALL)
    html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', html, flags=re.DOTALL)
    html = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', html, flags=re.DOTALL)
    html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', r'> \1', html, flags=re.DOTALL)
    html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html, flags=re.DOTALL)
    html = re.sub(r'<pre[^>]*>(.*?)</pre>', r'```\n\1\n```', html, flags=re.DOTALL)
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', html, flags=re.DOTALL)
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'<[^>]+>', '', html)
    return html


# ---------------------------------------------------------------------------
# Metadata extraction (adapted from normalize_article.py)
# ---------------------------------------------------------------------------

def extract_metadata(text: str) -> dict:
    """Extract title, author, date, subtitle from text heuristics."""
    metadata = {"title": "", "author": "", "date": "", "subtitle": ""}

    lines = text.strip().split('\n')
    for i, line in enumerate(lines[:10]):
        clean = line.strip().lstrip('#').strip()
        if not clean:
            continue
        if not metadata["title"]:
            metadata["title"] = clean
            continue
        if not metadata["subtitle"] and len(clean) < 200 and i < 5:
            if not re.match(r'^(by|author|date|published)', clean.lower()):
                metadata["subtitle"] = clean
                continue
        if re.match(r'^(by |author:?\s)', clean.lower()):
            metadata["author"] = re.sub(
                r'^(by |author:?\s+)', '', clean, flags=re.IGNORECASE
            ).strip()
        if re.search(r'\b(20\d{2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', clean.lower()):
            if len(clean) < 50:
                metadata["date"] = clean

    return metadata


# ---------------------------------------------------------------------------
# Block extraction (adapted from normalize_article.py, with extra fields)
# ---------------------------------------------------------------------------

def extract_blocks(text: str) -> list:
    """Parse text into typed content blocks with word_count / line_count fields."""
    blocks = []
    current_para = []

    lines = text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Image: ![alt](src)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            blocks.append({
                "type": "image",
                "alt": img_match.group(1),
                "src": img_match.group(2),
            })
            i += 1
            continue

        # Code block
        if line.strip().startswith('```'):
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append({
                "type": "code",
                "lang": lang,
                "content": '\n'.join(code_lines),
                "line_count": len(code_lines),
            })
            i += 1
            continue

        # Heading
        m = re.match(r'^(#{1,4})\s+(.+)', line)
        if m:
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            level = len(m.group(1))
            blocks.append({
                "type": "heading",
                "level": level,
                "content": m.group(2).strip(),
            })
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].lstrip('>').strip())
                i += 1
            blocks.append({"type": "quote", "content": ' '.join(quote_lines)})
            continue

        # List
        if re.match(r'^[-*•]\s+', line.strip()) or re.match(r'^\d+\.\s+', line.strip()):
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            list_items = []
            list_type = "ordered" if re.match(r'^\d+\.', line.strip()) else "unordered"
            while i < len(lines) and (
                re.match(r'^[-*•]\s+', lines[i].strip())
                or re.match(r'^\d+\.\s+', lines[i].strip())
            ):
                item = re.sub(r'^[-*•]\s+', '', lines[i].strip())
                item = re.sub(r'^\d+\.\s+', '', item)
                list_items.append(item)
                i += 1
            blocks.append({"type": "list", "list_type": list_type, "items": list_items})
            continue

        # Empty line — flush paragraph
        if not line.strip():
            if current_para:
                content = ' '.join(current_para).strip()
                blocks.append({
                    "type": "paragraph",
                    "content": content,
                    "word_count": len(content.split()),
                })
                current_para = []
            i += 1
            continue

        # Regular text
        current_para.append(line.strip())
        i += 1

    if current_para:
        content = ' '.join(current_para).strip()
        blocks.append({
            "type": "paragraph",
            "content": content,
            "word_count": len(content.split()),
        })

    # Remove empty/degenerate blocks
    blocks = [b for b in blocks if b.get("content") or b.get("items") or b.get("src")]
    return blocks


# ---------------------------------------------------------------------------
# normalize_content: main entry for this script
# ---------------------------------------------------------------------------

def normalize_content(input_path: str) -> tuple:
    """Parse markdown/HTML file into (metadata dict, blocks list)."""
    source = Path(input_path).read_text(encoding='utf-8')

    # Detect and convert HTML
    if '<html' in source.lower() or '</p>' in source or '</div>' in source:
        source = strip_html(source)

    # Clean whitespace
    source = re.sub(r'\r\n', '\n', source)
    source = re.sub(r'\n{4,}', '\n\n\n', source)
    source = source.strip()

    metadata = extract_metadata(source)
    blocks = extract_blocks(source)

    return metadata, blocks


# ---------------------------------------------------------------------------
# Language detection
# ---------------------------------------------------------------------------

def _is_cjk(ch: str) -> bool:
    cp = ord(ch)
    for lo, hi in CJK_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def detect_language(blocks: list) -> str:
    """Return 'zh' if >30% of all text chars are CJK, else 'en'."""
    all_text = []
    for block in blocks:
        btype = block.get("type")
        if btype in ("heading", "paragraph", "quote"):
            all_text.append(block.get("content", ""))
        elif btype == "list":
            all_text.extend(block.get("items", []))
        elif btype == "code":
            all_text.append(block.get("content", ""))

    combined = ''.join(all_text)
    if not combined:
        return "en"

    cjk_count = sum(1 for ch in combined if _is_cjk(ch))
    ratio = cjk_count / len(combined)
    return "zh" if ratio > 0.30 else "en"


# ---------------------------------------------------------------------------
# Weight assignment
# ---------------------------------------------------------------------------

def assign_weights(blocks: list, ratio: str = "3:4") -> list:
    """Return a new list of blocks each with an added 'weight' field.

    Block weights are ratio-independent — ratio adaptation is handled by
    TARGET_WEIGHT_PER_RATIO at the slide-distribution level. The ratio param
    is accepted for API compatibility but unused.
    """
    weighted = []
    for block in blocks:
        b = dict(block)
        btype = b["type"]

        if btype == "heading":
            level = b.get("level", 2)
            b["weight"] = BLOCK_WEIGHTS["heading"].get(level, 1.5)

        elif btype == "paragraph":
            word_count = b.get("word_count", len(b.get("content", "").split()))
            b["weight"] = max(1.0, word_count / 50)

        elif btype == "code":
            line_count = b.get("line_count", len(b.get("content", "").split('\n')))
            b["weight"] = max(2.5, line_count / 8 * 2.5)

        elif btype == "list":
            item_count = len(b.get("items", []))
            b["weight"] = item_count * 0.8

        elif btype == "quote":
            b["weight"] = BLOCK_WEIGHTS["quote"]

        elif btype == "image":
            b["weight"] = BLOCK_WEIGHTS["image"]

        else:
            b["weight"] = 1.0

        weighted.append(b)

    return weighted


# ---------------------------------------------------------------------------
# Cover info extraction
# ---------------------------------------------------------------------------

# Emoji detection: match emoji characters, explicitly excluding CJK ranges
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002600-\U000027BF"  # misc symbols (arrows, weather, etc.)
    "\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
    "\U0001FA00-\U0001FA6F"  # chess symbols, etc.
    "\U0001FA70-\U0001FAFF"  # symbols & pictographs extended-A
    "\U00002702-\U000027B0"  # dingbats subset
    "]+",
    flags=re.UNICODE,
)

_TECHNICAL_KEYWORDS = re.compile(
    r'\b(code|api|function|algorithm|data|python|javascript|software|system|tech|'
    r'server|database|network|machine learning|AI|GPU|CPU|cloud|deploy)\b',
    re.IGNORECASE,
)
_NATURE_KEYWORDS = re.compile(
    r'\b(nature|plant|tree|forest|ocean|environment|garden|animal|wildlife|earth|'
    r'ecology|sustainability|green|climate)\b',
    re.IGNORECASE,
)
_CREATIVE_KEYWORDS = re.compile(
    r'\b(design|art|creative|photography|film|music|draw|paint|craft|color|'
    r'illustration|typography|aesthetic)\b',
    re.IGNORECASE,
)


def _pick_default_emoji(blocks: list, metadata: dict) -> str:
    """Pick a topic-appropriate default emoji based on content keywords."""
    all_text = metadata.get("title", "") + " " + metadata.get("subtitle", "")
    for block in blocks:
        if block.get("type") in ("heading", "paragraph"):
            all_text += " " + block.get("content", "")

    if _TECHNICAL_KEYWORDS.search(all_text):
        return DEFAULT_EMOJI_TECHNICAL
    if _NATURE_KEYWORDS.search(all_text):
        return DEFAULT_EMOJI_NATURE
    if _CREATIVE_KEYWORDS.search(all_text):
        return DEFAULT_EMOJI_CREATIVE
    return DEFAULT_EMOJI_GENERIC


def extract_cover_info(blocks: list, metadata: dict, language: str) -> dict:
    """Return {'emoji': str, 'title': str, 'subtitle': str}."""
    # Find first emoji in any block content
    emoji = None
    for block in blocks:
        btype = block.get("type")
        texts = []
        if btype in ("heading", "paragraph", "quote"):
            texts = [block.get("content", "")]
        elif btype == "list":
            texts = block.get("items", [])
        for text in texts:
            m = _EMOJI_RE.search(text)
            if m:
                emoji = m.group(0)[0]  # take just the first emoji character
                break
        if emoji:
            break

    if not emoji:
        emoji = _pick_default_emoji(blocks, metadata)

    # Title
    title_limit = 20 if language == "zh" else 60
    if metadata.get("title"):
        title = metadata["title"][:title_limit]
    else:
        # First H1
        h1 = next((b for b in blocks if b.get("type") == "heading" and b.get("level") == 1), None)
        if h1:
            title = h1["content"][:title_limit]
        else:
            # First paragraph truncated
            para = next((b for b in blocks if b.get("type") == "paragraph"), None)
            title = (para["content"][:title_limit] if para else "")

    # Subtitle
    subtitle = ""
    if metadata.get("subtitle"):
        subtitle = metadata["subtitle"][:80]
    else:
        # Second substantive paragraph (>30 chars)
        para_count = 0
        for block in blocks:
            if block.get("type") == "paragraph":
                content = block.get("content", "")
                if len(content) > 30:
                    para_count += 1
                    if para_count == 2:
                        subtitle = content[:80]
                        break

    return {"emoji": emoji, "title": title, "subtitle": subtitle}


# ---------------------------------------------------------------------------
# Slide distribution planning
# ---------------------------------------------------------------------------

def _design_hint(slide_blocks: list) -> str:
    """Classify a slide's design hint based on its block composition."""
    if not slide_blocks:
        return "text-dense"

    total_weight = sum(b.get("weight", 0) for b in slide_blocks)
    code_weight = sum(b.get("weight", 0) for b in slide_blocks if b.get("type") == "code")
    list_weight = sum(b.get("weight", 0) for b in slide_blocks if b.get("type") == "list")

    if slide_blocks[0].get("type") == "heading":
        return "section-opener"
    if total_weight > 0 and code_weight / total_weight > 0.40:
        return "code-heavy"
    if total_weight > 0 and list_weight / total_weight > 0.40:
        return "list-heavy"
    if any(b.get("type") == "quote" for b in slide_blocks):
        return "quote-featured"
    return "text-dense"


def calc_optimal_slides(weighted_blocks: list, ratio: str = "3:4") -> int:
    """
    Calculate the natural slide count for good content density.
    Uses ratio-specific target weight per slide.
    Returns total slides (including cover).
    """
    target = TARGET_WEIGHT_PER_RATIO.get(ratio, 6.0)
    total = sum(b["weight"] for b in weighted_blocks)
    content_slides = math.ceil(total / target)
    return max(1, content_slides) + 1  # +1 for cover


def plan_distribution(weighted_blocks: list, num_slides: int, ratio: str) -> tuple:
    """
    Distribute weighted_blocks across slides.

    num_slides is treated as a CEILING (maximum), not a target.
    The actual slide count is the smaller of the optimal count (based on content
    density) and num_slides.

    Returns (slides_list, auto_fit_suggested, auto_fit_message, total_weight, target_per_slide).
    slides_list contains dicts with keys: slide_number, type, blocks, weight, design_hint, sparse.
    Slide 1 is always the cover (no content blocks).
    """
    total_weight = sum(b["weight"] for b in weighted_blocks)

    # Ceiling semantics: use the smaller of optimal count and requested max
    optimal = calc_optimal_slides(weighted_blocks, ratio)
    actual_slides = min(optimal, num_slides)
    auto_fit_suggested = actual_slides < num_slides
    auto_fit_message = None
    if auto_fit_suggested:
        auto_fit_message = (
            f"Content fits naturally in {actual_slides} slides at good density "
            f"(optimal: {optimal}, requested max: {num_slides}). "
            f"Using {actual_slides} slides."
        )

    # Reserve slide 1 for cover
    content_slides_needed = max(1, actual_slides - 1)
    target_per_slide = total_weight / content_slides_needed if content_slides_needed > 0 else total_weight

    # Greedy bin-packing
    slide_groups = []   # list of lists of blocks
    current_group = []
    current_weight = 0.0

    i = 0
    while i < len(weighted_blocks):
        block = weighted_blocks[i]
        bweight = block["weight"]

        # Heading: keep it tied to the next block
        if block.get("type") == "heading" and i + 1 < len(weighted_blocks):
            next_block = weighted_blocks[i + 1]
            combined_weight = bweight + next_block["weight"]

            # If adding this heading+next pair would overflow, start a new slide
            # (but only if current_group is non-empty)
            if current_group and current_weight + combined_weight > target_per_slide * 1.2:
                slide_groups.append(current_group)
                current_group = []
                current_weight = 0.0

            current_group.append(block)
            current_weight += bweight
            # Don't advance i for next_block; let the loop handle it naturally
            i += 1
            continue

        # Single block larger than the target: give it its own slide
        if not current_group and bweight > target_per_slide * 1.2:
            slide_groups.append([block])
            i += 1
            continue

        # Would overflow? Start a new slide.
        if current_group and current_weight + bweight > target_per_slide * 1.2:
            slide_groups.append(current_group)
            current_group = [block]
            current_weight = bweight
        else:
            current_group.append(block)
            current_weight += bweight

        i += 1

    if current_group:
        slide_groups.append(current_group)

    # Build slides list
    slides = [{"slide_number": 1, "type": "cover"}]
    for idx, group in enumerate(slide_groups):
        slide_weight = sum(b["weight"] for b in group)
        slides.append({
            "slide_number": idx + 2,
            "type": "content",
            "weight": round(slide_weight, 2),
            "blocks": group,
            "design_hint": _design_hint(group),
            "sparse": len(group) < 3,
            "extractable_content": _extract_quotable_content(group),
        })

    # Enforce visual variety — no 3+ consecutive same-hint slides
    _enforce_variety(slides)

    return slides, auto_fit_suggested, auto_fit_message, total_weight, target_per_slide


def _enforce_variety(slides: list) -> None:
    """Ensure no more than 2 consecutive content slides share the same design_hint.

    Mutates slides in place. Only reclassifies 'text-dense' runs to add visual breaks.
    """
    content = [s for s in slides if s.get("type") == "content"]
    for i in range(2, len(content)):
        if (content[i]["design_hint"] == content[i-1]["design_hint"] == content[i-2]["design_hint"]
                and content[i]["design_hint"] == "text-dense"):
            content[i-1]["design_hint"] = "section-opener"
            content[i-1]["sparse"] = True


# ---------------------------------------------------------------------------
# Extractable content — preserve quotable material for fill components
# ---------------------------------------------------------------------------

_DATA_POINT_RE = re.compile(
    r'(?:'
    r'\$\d[\d,.]*'                      # dollar amounts: $12, $1,500
    r'|\d+[\d.]*\s*%'                   # percentages: 80%, 3.5%
    r'|\d+[\d.]*\s*(?:小时|分钟|h|hr|min|天|秒|ms|s)\b'  # durations
    r'|\d+[\d.]*\s*(?:px|rem|em|KB|MB|GB|TB)\b'  # technical units
    r'|\d+[\d,.]*\s*(?:个|条|篇|次|行|步|项|张|页)\b'  # Chinese counters
    r'|\d{2,}[\d,.]*'                   # standalone numbers 2+ digits
    r')',
    re.IGNORECASE,
)

_QUOTABLE_KEYWORDS_ZH = re.compile(
    r'(?:最重要|关键|核心|本质|真正|其实|一句话|说白了|瓶颈|永远|'
    r'不是.*而是|与其.*不如)',
)
_QUOTABLE_KEYWORDS_EN = re.compile(
    r'\b(?:the key|crucial|essential|never|always|the real|in short|'
    r'bottom line|the truth is|not about.*but about)\b',
    re.IGNORECASE,
)

_PROPER_NOUN_RE = re.compile(
    r'\b(?:'
    r'ChatGPT|GPT-\d|Claude|Gemini|Copilot|'
    r'GitHub|Git|Docker|Kubernetes|AWS|GCP|Azure|Vercel|Netlify|'
    r'React|Vue|Angular|Next\.?js|Nuxt|Astro|Svelte|'
    r'Tailwind|Bootstrap|CSS|HTML|JavaScript|TypeScript|Python|Rust|Go|'
    r'Node\.?js|Deno|Bun|npm|pnpm|yarn|pip|cargo|'
    r'PostgreSQL|MySQL|MongoDB|Redis|Supabase|Firebase|'
    r'Playwright|Puppeteer|Selenium|Jest|Vitest|pytest'
    r')\b'
)


def _extract_quotable_content(slide_blocks: list) -> dict:
    """Extract quotable sentences, data points, tools, and code blocks from slide blocks."""
    quotes = []
    data_points = []
    tools_mentioned = set()
    code_blocks = []

    for block in slide_blocks:
        btype = block.get("type")
        content = block.get("content", "")

        if btype == "code":
            code_blocks.append(content[:200])  # truncate long code
            continue

        # Gather all text from this block
        texts = []
        if btype in ("heading", "paragraph", "quote"):
            texts = [content]
        elif btype == "list":
            texts = block.get("items", [])

        for text in texts:
            # Extract data points
            for m in _DATA_POINT_RE.finditer(text):
                dp = m.group(0).strip()
                if dp and dp not in data_points:
                    data_points.append(dp)

            # Extract proper nouns / tools
            for m in _PROPER_NOUN_RE.finditer(text):
                tools_mentioned.add(m.group(0))

            # Extract quotable sentences (split on Chinese/English sentence boundaries)
            sentences = re.split(r'[。！？.!?]', text)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 10:
                    continue
                if _QUOTABLE_KEYWORDS_ZH.search(sentence) or _QUOTABLE_KEYWORDS_EN.search(sentence):
                    quotes.append(sentence)
                # Also capture short, punchy sentences (opinion-like)
                elif len(sentence) < 40 and any(c in sentence for c in ('—', '——', '：', ':')):
                    quotes.append(sentence)

    return {
        "quotes": quotes[:5],  # cap at 5 per slide
        "data_points": data_points[:10],
        "tools_mentioned": sorted(tools_mentioned),
        "code_blocks": code_blocks[:2],
    }


# ---------------------------------------------------------------------------
# Build final slide plan JSON
# ---------------------------------------------------------------------------

def build_slide_plan(
    metadata: dict,
    weighted_blocks: list,
    slides: list,
    cover: dict,
    config: dict,
    auto_fit_suggested: bool,
    auto_fit_message,
    total_weight: float,
    target_weight_per_slide: float,
    language: str,
) -> dict:
    """Assemble the full output JSON structure."""
    ratio = config["ratio"]
    ratio_cfg = RATIO_CONFIGS[ratio]

    return {
        "config": {
            "ratio": ratio,
            "width": ratio_cfg["width"],
            "height": ratio_cfg["height"],
            "total_slides": len(slides),
            "theme": config["theme"],
            "language": language,
            "author": config.get("author", ""),
        },
        "cover": cover,
        "slides": slides,
        "metadata": {
            "total_blocks": len(weighted_blocks),
            "total_weight": round(total_weight, 2),
            "target_weight_per_slide": round(target_weight_per_slide, 2),
            "auto_fit_suggested": auto_fit_suggested,
            "auto_fit_message": auto_fit_message,
            "language_detected": language,
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Plan slide distribution for a social media carousel'
    )
    parser.add_argument('--input', '-i', required=True, help='Input markdown/HTML file')
    parser.add_argument(
        '--slides', '-s',
        type=int,
        default=9,
        metavar='N',
        help='Maximum number of slides (1–18, default 9). Actual count may be lower if content is sparse.',
    )
    parser.add_argument(
        '--ratio', '-r',
        choices=['3:4', '9:16', '1:1'],
        default='3:4',
        help='Aspect ratio (default: 3:4)',
    )
    parser.add_argument(
        '--theme', '-t',
        default='sketch',
        help='Theme name (default: sketch)',
    )
    parser.add_argument(
        '--output', '-o',
        default='slide_plan.json',
        help='Output JSON file (default: slide_plan.json)',
    )
    parser.add_argument(
        '--author',
        default='',
        metavar='TAG',
        help='Author tag shown bottom-left of each slide (e.g. @username). Optional.',
    )
    args = parser.parse_args()

    # Validate slides range
    if not (1 <= args.slides <= 18):
        parser.error(f"--slides must be between 1 and 18, got {args.slides}")

    # 1. Normalize content
    metadata, blocks = normalize_content(args.input)

    # 2. Detect language
    language = detect_language(blocks)

    # 3. Assign weights
    weighted_blocks = assign_weights(blocks, args.ratio)

    # 4. Extract cover info
    cover = extract_cover_info(weighted_blocks, metadata, language)

    # 5. Plan distribution
    slides, auto_fit_suggested, auto_fit_message, total_weight, target_per_slide = plan_distribution(
        weighted_blocks, args.slides, args.ratio
    )

    # 6. Build full plan
    config = {"ratio": args.ratio, "theme": args.theme, "author": args.author}
    plan = build_slide_plan(
        metadata=metadata,
        weighted_blocks=weighted_blocks,
        slides=slides,
        cover=cover,
        config=config,
        auto_fit_suggested=auto_fit_suggested,
        auto_fit_message=auto_fit_message,
        total_weight=total_weight,
        target_weight_per_slide=target_per_slide,
        language=language,
    )

    # 7. Write output
    output_path = Path(args.output)
    output_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding='utf-8')

    # 8. Print summary
    actual_slides = len(slides)
    total_blocks = len(weighted_blocks)
    print(f"✓ Analyzed → {total_blocks} blocks, {total_weight:.1f} total weight")
    print(f"✓ Planned  → {actual_slides} slides ({target_per_slide:.1f} weight/slide target)")
    if auto_fit_suggested and auto_fit_message:
        print(f"⚠ Auto-fit: {auto_fit_message}")
    print(f"✓ Output   → {output_path}")


if __name__ == '__main__':
    main()
