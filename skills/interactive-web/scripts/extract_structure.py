#!/usr/bin/env python3
"""
extract_structure.py

Analyse a normalized article and produce structure.json:
- article type classification
- thesis extraction
- section map
- key concepts
- interaction model recommendation
- design direction hint

Usage:
    python3 scripts/extract_structure.py --input normalized.md
    python3 scripts/extract_structure.py --input blocks.json
"""

import sys
import re
import json
import argparse
from pathlib import Path


# ─── Article type signals ───────────────────────────────────────────────────

ARTICLE_TYPE_SIGNALS = {
    "tutorial": [
        r'\bstep\b', r'\bhow to\b', r'\bguide\b', r'\bwalkthrough\b',
        r'\binstall\b', r'\bsetup\b', r'\bbegin\b', r'\bfirst.*then\b',
        r'^\d+\.\s', r'\bprerequisite\b', r'\bin this tutorial\b'
    ],
    "technical-analysis": [
        r'\barchitecture\b', r'\bsystem\b', r'\bcomponent\b', r'\bflow\b',
        r'\bintegration\b', r'\bapi\b', r'\bperformance\b', r'\bscalability\b',
        r'\blatency\b', r'\bdependency\b', r'\binfrastructure\b'
    ],
    "opinion": [
        r'\bi believe\b', r'\bi think\b', r'\bin my view\b', r'\bcontroversial\b',
        r'\bargue\b', r'\bmy take\b', r'\bopinion\b', r'\bthesis\b',
        r'\bwhy i\b', r'\bwhy we\b', r'\bwhy.*matters\b'
    ],
    "tool-review": [
        r'\bvs\b', r'\bversus\b', r'\bcompare\b', r'\bcomparison\b',
        r'\bpros and cons\b', r'\btradeoff\b', r'\balternative\b',
        r'\bwhich.*should\b', r'\bbetter than\b', r'\bbenchmark\b'
    ],
    "case-study": [
        r'\bcase study\b', r'\bresult\b', r'\boutcome\b', r'\bwe built\b',
        r'\bwe shipped\b', r'\bchallenge\b', r'\bsolution\b', r'\bimpact\b',
        r'\bmetric\b', r'\bimproved\b', r'\blearning\b', r'\blesson\b'
    ],
    "timeline": [
        r'\bhistory\b', r'\bevolution\b', r'\borigin\b', r'\bthen\b.*\bnow\b',
        r'\b20\d\d\b.*\b20\d\d\b', r'\bera\b', r'\bphase\b', r'\bgeneration\b',
        r'\bfirst.*second.*third\b', r'\bearly\b.*\blater\b'
    ],
    "framework": [
        r'\bframework\b', r'\bprinciple\b', r'\bpillar\b', r'\bmodel\b',
        r'\blayer\b', r'\bdimension\b', r'\baxis\b', r'\bmaturity\b',
        r'\bspectrum\b', r'\bconcept\b', r'\bmental model\b'
    ],
    "data-driven": [
        r'\b\d+%\b', r'\bstatistic\b', r'\bdata\b', r'\bstudy\b',
        r'\bresearch\b', r'\bsurvey\b', r'\bfound that\b', r'\baccording to\b',
        r'\bgrowth\b.*\b\d+\b', r'\bmetric\b', r'\bmeasur'
    ]
}


INTERACTION_MODELS = {
    "tutorial": {
        "model": "step-sequencer",
        "label": "Step Sequencer",
        "reason": "Tutorial content has a natural forward sequence; revealing steps one-at-a-time reduces overwhelm and creates progress momentum."
    },
    "technical-analysis": {
        "model": "architecture-explainer",
        "label": "Architecture Explainer",
        "reason": "Technical systems have components and flows that benefit from visual representation and selective depth."
    },
    "opinion": {
        "model": "scroll-journey",
        "label": "Scroll Journey",
        "reason": "Argumentative essays have a narrative arc; scroll-based reveal preserves logical flow while adding pacing."
    },
    "tool-review": {
        "model": "comparison-matrix",
        "label": "Comparison Matrix",
        "reason": "Comparison content is most useful when readers can evaluate options side-by-side interactively."
    },
    "case-study": {
        "model": "scroll-journey",
        "label": "Scroll Journey with Metric Highlights",
        "reason": "Case studies have a story arc (challenge → solution → results); metrics deserve visual emphasis."
    },
    "timeline": {
        "model": "timeline-experience",
        "label": "Timeline Experience",
        "reason": "Chronological content becomes navigable and memorable when mapped to a visual time axis."
    },
    "framework": {
        "model": "concept-explorer",
        "label": "Concept Explorer",
        "reason": "Framework content has interrelated concepts; layered exploration lets readers navigate depth at their own pace."
    },
    "data-driven": {
        "model": "data-dashboard",
        "label": "Data Dashboard",
        "reason": "Data-rich content is most impactful when statistics are animated, contextualized, and visually prominent."
    }
}

DESIGN_DIRECTIONS = {
    "tutorial": "editorial-warm",
    "technical-analysis": "dark-technical",
    "opinion": "editorial-ink",
    "tool-review": "clean-analytical",
    "case-study": "editorial-warm",
    "timeline": "editorial-ink",
    "framework": "dark-technical",
    "data-driven": "clean-analytical"
}

# Bundled style directions — map article type to a rendering mode that
# pre-selects both visual identity and interaction model together.
# Used when --style auto is passed or when the caller requests style-mode output.
STYLE_DIRECTIONS = {
    "tutorial":           "warm-cards",
    "technical-analysis": "technical-glow",
    "opinion":            "story-scrollytelling",
    "tool-review":        "bento-analytical",
    "case-study":         "story-scrollytelling",
    "timeline":           "story-scrollytelling",
    "framework":          "glass-layered",
    "data-driven":        "bento-analytical"
}

STYLE_INTERACTION_OVERRIDES = {
    "story-scrollytelling": "scroll-journey",
    "bento-analytical":     "comparison-matrix",
    "technical-glow":       "architecture-explainer",
    "warm-cards":           "step-sequencer",
    "glass-layered":        "concept-explorer"
}

VALID_STYLES = set(STYLE_INTERACTION_OVERRIDES.keys())


def classify_article(text: str) -> tuple[str, dict]:
    """Score each article type against signal patterns."""
    text_lower = text.lower()
    scores = {}

    for article_type, patterns in ARTICLE_TYPE_SIGNALS.items():
        score = sum(1 for p in patterns if re.search(p, text_lower))
        scores[article_type] = score

    best_type = max(scores, key=scores.get)
    if scores[best_type] == 0:
        best_type = "opinion"  # safe fallback

    return best_type, scores


def extract_thesis(blocks: list) -> str:
    """Find the most likely thesis sentence — first substantive paragraph."""
    for block in blocks:
        if block.get("type") == "paragraph":
            content = block["content"]
            if len(content) > 60 and not content.startswith("(") and not content.startswith("["):
                # Truncate to first 2 sentences
                sentences = re.split(r'(?<=[.!?])\s+', content)
                return ' '.join(sentences[:2])
    return ""


def extract_concepts(blocks: list, max_concepts: int = 7) -> list:
    """Extract key named concepts from headings and emphasized text."""
    concepts = []

    for block in blocks:
        if block.get("type") == "heading" and block.get("level", 1) >= 2:
            concepts.append({
                "label": block["content"],
                "source": "heading",
                "level": block.get("level", 2)
            })

        if block.get("type") == "paragraph":
            # Extract bolded terms
            bold_terms = re.findall(r'\*\*(.+?)\*\*', block["content"])
            for term in bold_terms:
                if len(term) < 60 and term not in [c["label"] for c in concepts]:
                    concepts.append({"label": term, "source": "bold", "level": 3})

    return concepts[:max_concepts]


def extract_sections(blocks: list) -> list:
    """Build section map from heading hierarchy."""
    sections = []
    current_section = None

    for block in blocks:
        if block.get("type") == "heading":
            if block.get("level", 2) == 1:
                continue  # Skip title

            if current_section:
                sections.append(current_section)

            current_section = {
                "id": re.sub(r'[^a-z0-9]+', '-', block["content"].lower()).strip('-'),
                "label": block["content"],
                "level": block.get("level", 2),
                "blocks": [],
                "has_code": False,
                "has_list": False,
                "has_quote": False,
                "block_count": 0
            }
        elif current_section:
            current_section["blocks"].append(block.get("type", "paragraph"))
            current_section["block_count"] += 1
            if block.get("type") == "code":
                current_section["has_code"] = True
            if block.get("type") == "list":
                current_section["has_list"] = True
            if block.get("type") == "quote":
                current_section["has_quote"] = True

    if current_section:
        sections.append(current_section)

    # Assign interaction roles
    for section in sections:
        section["role"] = infer_section_role(section)

    return sections


def infer_section_role(section: dict) -> str:
    """Determine how a section should be rendered."""
    label_lower = section["label"].lower()

    if any(w in label_lower for w in ["intro", "overview", "background", "context", "about"]):
        return "static-editorial"
    if any(w in label_lower for w in ["step", "how", "install", "setup", "implement"]):
        return "step-reveal"
    if any(w in label_lower for w in ["compare", "vs", "versus", "tradeoff", "difference"]):
        return "comparison"
    if any(w in label_lower for w in ["result", "outcome", "metric", "impact", "number"]):
        return "stat-highlight"
    if any(w in label_lower for w in ["conclusion", "summary", "takeaway", "next", "final"]):
        return "static-editorial"
    if section.get("has_code"):
        return "code-explainer"
    if section.get("has_list") and section.get("block_count", 0) <= 3:
        return "card-reveal"
    return "static-editorial"


def should_degrade(blocks: list, sections: list) -> tuple[bool, str]:
    """Determine if static page is better than interactive."""
    total_words = sum(
        len(b.get("content", "").split())
        for b in blocks if b.get("type") == "paragraph"
    )
    heading_count = len(sections)

    if total_words < 150:
        return True, "Content is too short to benefit from interactivity (< 300 words)"
    if heading_count < 2:
        return True, "Content has no meaningful section structure (< 2 headings)"
    if heading_count == 0 and total_words < 500:
        return True, "Short unstructured content — static editorial is more appropriate"

    return False, ""


def main():
    parser = argparse.ArgumentParser(description='Extract structure from normalized article')
    parser.add_argument('--input', '-i', required=True, help='Normalized markdown or blocks.json')
    parser.add_argument('--output', '-o', default='structure.json', help='Output structure JSON')
    parser.add_argument(
        '--style', default=None,
        help='Visual style override: story-scrollytelling | bento-analytical | '
             'technical-glow | warm-cards | glass-layered | auto'
    )
    args = parser.parse_args()

    input_path = Path(args.input)

    if args.input.endswith('.json'):
        data = json.loads(input_path.read_text(encoding='utf-8'))
        blocks = data.get("blocks", [])
        metadata = data.get("metadata", {})
        full_text = ' '.join(
            b.get("content", " ".join(b.get("items", [])))
            for b in blocks
        )
    else:
        full_text = input_path.read_text(encoding='utf-8')
        # Re-extract blocks for analysis
        from normalize_article import extract_blocks, extract_metadata
        metadata = extract_metadata(full_text)
        blocks = extract_blocks(full_text)

    article_type, type_scores = classify_article(full_text)
    interaction_info = INTERACTION_MODELS[article_type]
    design_direction = DESIGN_DIRECTIONS[article_type]

    # Resolve bundled style (--style flag overrides auto-classification)
    if args.style and args.style != 'auto' and args.style in VALID_STYLES:
        selected_style = args.style
    elif args.style == 'auto' or args.style is None:
        selected_style = STYLE_DIRECTIONS.get(article_type)
    else:
        selected_style = None

    # When a bundled style is active, override interaction model
    if selected_style and selected_style in STYLE_INTERACTION_OVERRIDES:
        override_model = STYLE_INTERACTION_OVERRIDES[selected_style]
        interaction_info = {
            "model": override_model,
            "label": override_model.replace('-', ' ').title(),
            "reason": f"Style '{selected_style}' bundles this interaction model as its default."
        }

    thesis = extract_thesis(blocks)
    concepts = extract_concepts(blocks)
    sections = extract_sections(blocks)
    degrade, degrade_reason = should_degrade(blocks, sections)

    structure = {
        "metadata": metadata,
        "analysis": {
            "article_type": article_type,
            "type_scores": type_scores,
            "thesis": thesis,
            "word_count": sum(len(b.get("content","").split()) for b in blocks if b.get("type") == "paragraph"),
            "section_count": len(sections),
            "has_code": any(b.get("type") == "code" for b in blocks),
            "has_data": bool(re.search(r'\b\d+%\b|\b\$\d+|\b\d+x\b', full_text)),
            "has_comparison": bool(re.search(r'\bvs\b|\bversus\b|\bcompare\b', full_text.lower()))
        },
        "recommendation": {
            "interaction_model": interaction_info["model"],
            "interaction_label": interaction_info["label"],
            "reason": interaction_info["reason"],
            "design_direction": design_direction,
            "selected_style": selected_style,
            "degrade_to_static": degrade,
            "degrade_reason": degrade_reason
        },
        "concepts": concepts,
        "sections": sections
    }

    Path(args.output).write_text(json.dumps(structure, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"✓ Structure extracted → {args.output}")
    print(f"  Article type: {article_type} (score: {type_scores[article_type]})")
    print(f"  Interaction model: {interaction_info['label']}")
    print(f"  Design direction: {design_direction}")
    if selected_style:
        print(f"  Selected style: {selected_style}")
    print(f"  Degrade to static: {degrade}")
    if degrade:
        print(f"  Reason: {degrade_reason}")
    print(f"  Concepts: {len(concepts)}")
    print(f"  Sections: {len(sections)}")


if __name__ == '__main__':
    main()
