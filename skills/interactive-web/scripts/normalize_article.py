#!/usr/bin/env python3
"""
normalize_article.py

Normalize raw article input (Markdown, HTML, plain text, .docx)
into clean structured Markdown with consistent block types.

Outputs: normalized.md
"""

import sys
import re
import argparse
import json
from pathlib import Path


def strip_html(html: str) -> str:
    """Remove HTML tags, preserve semantic structure."""
    # Convert semantic blocks to Markdown equivalents
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
    html = re.sub(r'<[^>]+>', '', html)  # strip remaining tags
    return html


def extract_metadata(text: str) -> dict:
    """Extract title, author, date from text heuristics."""
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
            # Likely a subtitle if short and early
            if not re.match(r'^(by|author|date|published)', clean.lower()):
                metadata["subtitle"] = clean
                continue
        # Author patterns
        if re.match(r'^(by |author:?\s)', clean.lower()):
            metadata["author"] = re.sub(r'^(by |author:?\s+)', '', clean, flags=re.IGNORECASE).strip()
        # Date patterns
        if re.search(r'\b(20\d{2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b', clean.lower()):
            if len(clean) < 50:
                metadata["date"] = clean

    return metadata


def extract_blocks(text: str) -> list:
    """Parse text into typed content blocks."""
    blocks = []
    current_para = []

    lines = text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith('```'):
            if current_para:
                blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})
                current_para = []
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append({"type": "code", "lang": lang, "content": '\n'.join(code_lines)})
            i += 1
            continue

        # Heading
        m = re.match(r'^(#{1,4})\s+(.+)', line)
        if m:
            if current_para:
                blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})
                current_para = []
            level = len(m.group(1))
            blocks.append({"type": "heading", "level": level, "content": m.group(2).strip()})
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('>'):
            if current_para:
                blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})
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
                blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})
                current_para = []
            list_items = []
            list_type = "ordered" if re.match(r'^\d+\.', line.strip()) else "unordered"
            while i < len(lines) and (re.match(r'^[-*•]\s+', lines[i].strip()) or re.match(r'^\d+\.\s+', lines[i].strip())):
                item = re.sub(r'^[-*•]\s+', '', lines[i].strip())
                item = re.sub(r'^\d+\.\s+', '', item)
                list_items.append(item)
                i += 1
            blocks.append({"type": "list", "list_type": list_type, "items": list_items})
            continue

        # Empty line — flush paragraph
        if not line.strip():
            if current_para:
                blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})
                current_para = []
            i += 1
            continue

        # Regular text
        current_para.append(line.strip())
        i += 1

    if current_para:
        blocks.append({"type": "paragraph", "content": ' '.join(current_para).strip()})

    # Remove empty blocks
    blocks = [b for b in blocks if b.get("content") or b.get("items")]
    return blocks


def blocks_to_markdown(metadata: dict, blocks: list) -> str:
    """Reconstruct clean Markdown from extracted blocks."""
    lines = []

    if metadata.get("title"):
        lines.append(f"# {metadata['title']}\n")
    if metadata.get("subtitle"):
        lines.append(f"_{metadata['subtitle']}_\n")
    if metadata.get("author"):
        lines.append(f"**Author:** {metadata['author']}")
    if metadata.get("date"):
        lines.append(f"**Date:** {metadata['date']}\n")
    if any([metadata.get("author"), metadata.get("date")]):
        lines.append("")

    lines.append("---\n")

    for block in blocks:
        btype = block.get("type")
        if btype == "heading":
            prefix = "#" * block["level"]
            lines.append(f"{prefix} {block['content']}\n")
        elif btype == "paragraph":
            lines.append(f"{block['content']}\n")
        elif btype == "quote":
            lines.append(f"> {block['content']}\n")
        elif btype == "code":
            lang = block.get("lang", "")
            lines.append(f"```{lang}\n{block['content']}\n```\n")
        elif btype == "list":
            for item in block.get("items", []):
                if block.get("list_type") == "ordered":
                    lines.append(f"1. {item}")
                else:
                    lines.append(f"- {item}")
            lines.append("")

    return '\n'.join(lines)


def normalize(source: str) -> tuple[dict, list, str]:
    """Main normalization pipeline."""
    # Detect and convert HTML
    if '<html' in source.lower() or '</p>' in source or '</div>' in source:
        source = strip_html(source)

    # Clean whitespace
    source = re.sub(r'\r\n', '\n', source)
    source = re.sub(r'\n{4,}', '\n\n\n', source)
    source = source.strip()

    metadata = extract_metadata(source)
    blocks = extract_blocks(source)
    markdown = blocks_to_markdown(metadata, blocks)

    return metadata, blocks, markdown


def main():
    parser = argparse.ArgumentParser(description='Normalize article for interactive-web skill')
    parser.add_argument('--input', '-i', required=True, help='Input file path or - for stdin')
    parser.add_argument('--output', '-o', default='normalized.md', help='Output markdown file')
    parser.add_argument('--blocks', '-b', default='blocks.json', help='Output blocks JSON file')
    args = parser.parse_args()

    if args.input == '-':
        source = sys.stdin.read()
    else:
        source = Path(args.input).read_text(encoding='utf-8')

    metadata, blocks, markdown = normalize(source)

    Path(args.output).write_text(markdown, encoding='utf-8')
    Path(args.blocks).write_text(json.dumps({"metadata": metadata, "blocks": blocks}, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"✓ Normalized → {args.output}")
    print(f"✓ Blocks JSON → {args.blocks}")
    print(f"  Title: {metadata.get('title', '(none)')}")
    print(f"  Blocks: {len(blocks)} extracted")
    block_types = {}
    for b in blocks:
        block_types[b['type']] = block_types.get(b['type'], 0) + 1
    for btype, count in sorted(block_types.items()):
        print(f"    {btype}: {count}")


if __name__ == '__main__':
    main()
