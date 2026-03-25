#!/usr/bin/env python3
"""
build_page_plan.py

Generate blueprint.json — the implementation contract Claude reads
before building the interactive artifact.

Inputs:  structure.json (from extract_structure.py)
Outputs: blueprint.json

The blueprint defines:
  - page sections and their component types
  - interaction mapping per section
  - design system tokens to use
  - content slots (what goes where)
  - state requirements
  - accessibility notes
"""

import json
import re
import argparse
from pathlib import Path


# ─── Design system tokens per direction ──────────────────────────────────────

DESIGN_SYSTEMS = {
    "dark-technical": {
        "font_display": "IBM Plex Sans",
        "font_body": "IBM Plex Sans",
        "font_mono": "IBM Plex Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap",
        "palette": {
            "bg": "#0d1117",
            "surface": "#161b22",
            "border": "#30363d",
            "text_primary": "#e6edf3",
            "text_muted": "#7d8590",
            "accent": "#58a6ff",
            "accent_warm": "#f78166",
            "positive": "#3fb950"
        },
        "theme": "dark"
    },
    "editorial-ink": {
        "font_display": "Playfair Display",
        "font_body": "Crimson Pro",
        "font_mono": "IBM Plex Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Crimson+Pro:wght@300;400;600&family=IBM+Plex+Mono:wght@400&display=swap",
        "palette": {
            "bg": "#faf8f2",
            "surface": "#ffffff",
            "border": "#e8e4d9",
            "text_primary": "#1a1612",
            "text_muted": "#8a8070",
            "accent": "#c41e3a",
            "accent_warm": "#d4a853",
            "positive": "#3d6b3d"
        },
        "theme": "light"
    },
    "clean-analytical": {
        "font_display": "Plus Jakarta Sans",
        "font_body": "Plus Jakarta Sans",
        "font_mono": "Fira Code",
        "font_import": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&family=Fira+Code:wght@400;500&display=swap",
        "palette": {
            "bg": "#0f172a",
            "surface": "#1e293b",
            "border": "#334155",
            "text_primary": "#f1f5f9",
            "text_muted": "#94a3b8",
            "accent": "#22d3ee",
            "accent_warm": "#f59e0b",
            "positive": "#4ade80"
        },
        "theme": "dark"
    },
    "editorial-warm": {
        "font_display": "Newsreader",
        "font_body": "Nunito",
        "font_mono": "IBM Plex Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,600;0,700;1,400&family=Nunito:wght@300;400;600&family=IBM+Plex+Mono:wght@400&display=swap",
        "palette": {
            "bg": "#fdf6ee",
            "surface": "#fff9f2",
            "border": "#e8ddd0",
            "text_primary": "#2c1810",
            "text_muted": "#9a8070",
            "accent": "#e85d04",
            "accent_warm": "#606c38",
            "positive": "#3d6b3d"
        },
        "theme": "light"
    },
    "claude-like": {
        "font_display": "Instrument Serif",
        "font_body": "DM Sans",
        "font_mono": "DM Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&family=DM+Mono:wght@400;500&display=swap",
        "palette": {
            "bg": "#faf9f7",
            "surface": "#ffffff",
            "border": "#e8e4dc",
            "text_primary": "#1a1816",
            "text_muted": "#8b8580",
            "accent": "#d97757",
            "accent_warm": "#c9622a",
            "positive": "#4a7c59"
        },
        "theme": "light"
    },

    # ─── Bundled styles (layout + visual identity + interaction model) ─────────
    "story-scrollytelling": {
        "font_display": "Cormorant Garamond",
        "font_body": "Lato",
        "font_mono": "Fira Code",
        "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Lato:wght@300;400;700&family=Fira+Code:wght@400&display=swap",
        "palette": {
            "bg": "#f9f6f0",
            "surface": "#ffffff",
            "border": "#ddd7c8",
            "text_primary": "#1c1814",
            "text_muted": "#7a7060",
            "accent": "#8b4513",
            "accent_warm": "#c8702a",
            "positive": "#3a6b44",
            "chapter_rule": "#c8b89a",
            "dropcap_bg": "#f0ead8"
        },
        "theme": "light"
    },
    "bento-analytical": {
        "font_display": "Plus Jakarta Sans",
        "font_body": "Plus Jakarta Sans",
        "font_mono": "Fira Code",
        "font_import": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap",
        "palette": {
            "bg": "#f4f6f9",
            "surface": "#ffffff",
            "border": "#dde2ec",
            "text_primary": "#111827",
            "text_muted": "#6b7280",
            "accent": "#2563eb",
            "accent_warm": "#f59e0b",
            "positive": "#16a34a",
            "surface_alt": "#f8f9fb",
            "accent_soft": "#eff6ff"
        },
        "theme": "light"
    },
    "technical-glow": {
        "font_display": "IBM Plex Sans",
        "font_body": "IBM Plex Sans",
        "font_mono": "IBM Plex Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:ital,wght@0,400;0,500;1,400&display=swap",
        "palette": {
            "bg": "#0a0e17",
            "surface": "#111827",
            "border": "#1e2d45",
            "text_primary": "#e2eaf8",
            "text_muted": "#6b82a8",
            "accent": "#38bdf8",
            "accent_warm": "#fb923c",
            "positive": "#4ade80",
            "glow_color": "rgba(56,189,248,0.18)",
            "glow_strong": "rgba(56,189,248,0.35)",
            "surface_raised": "#161f30",
            "code_bg": "#0d1420"
        },
        "theme": "dark"
    },
    "warm-cards": {
        "font_display": "Nunito",
        "font_body": "Nunito",
        "font_mono": "Fira Code",
        "font_import": "https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Fira+Code:wght@400&display=swap",
        "palette": {
            "bg": "#fef9f4",
            "surface": "#ffffff",
            "border": "#ead5c4",
            "text_primary": "#2d1a0e",
            "text_muted": "#8c6652",
            "accent": "#e96d2c",
            "accent_warm": "#f4a62b",
            "positive": "#3d7a51",
            "surface_soft": "#fdf3ea",
            "step_done": "#d4edda",
            "step_done_border": "#a3cfb4"
        },
        "theme": "light"
    },
    "glass-layered": {
        "font_display": "Space Grotesk",
        "font_body": "Space Grotesk",
        "font_mono": "Space Mono",
        "font_import": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap",
        "palette": {
            "bg": "#060d1f",
            "surface": "rgba(255,255,255,0.06)",
            "surface_strong": "rgba(255,255,255,0.10)",
            "surface_solid": "#0f1e3d",
            "border": "rgba(255,255,255,0.12)",
            "border_strong": "rgba(255,255,255,0.22)",
            "text_primary": "#eef2ff",
            "text_muted": "#8896b8",
            "accent": "#818cf8",
            "accent_warm": "#f472b6",
            "positive": "#34d399",
            "glass_tint": "rgba(129,140,248,0.08)"
        },
        "theme": "dark"
    }
}


# ─── Bundled style → preferred interaction model ─────────────────────────────

STYLE_INTERACTION_OVERRIDES = {
    "story-scrollytelling": "scroll-journey",
    "bento-analytical":     "comparison-matrix",
    "technical-glow":       "architecture-explainer",
    "warm-cards":           "step-sequencer",
    "glass-layered":        "concept-explorer"
}


# ─── Component templates per interaction model ────────────────────────────────

MODEL_PAGE_TEMPLATES = {
    "step-sequencer": {
        "sections": [
            {"id": "hero", "component": "hero-editorial", "notes": "Title, thesis, estimated read time"},
            {"id": "progress", "component": "sticky-progress-bar", "notes": "Step N of M indicator, sticky top"},
            {"id": "steps", "component": "step-sequencer", "notes": "Main content — one step at a time reveal"},
            {"id": "summary", "component": "takeaway-grid", "notes": "Key learnings or next steps"}
        ],
        "state": ["currentStep:number", "completedSteps:Set<number>"],
        "interactions": ["next-step button", "previous-step button", "step click to jump", "progress bar fills"]
    },
    "scroll-journey": {
        "sections": [
            {"id": "hero", "component": "hero-full", "notes": "Bold title, thesis as subtitle"},
            {"id": "toc", "component": "floating-toc", "notes": "Appears after first scroll, anchors to sections"},
            {"id": "content", "component": "scroll-reveal-sections", "notes": "Each major section reveals on entry"},
            {"id": "pullquotes", "component": "inline-pullquotes", "notes": "1-2 key quotes with visual weight"},
            {"id": "conclusion", "component": "conclusion-callout", "notes": "Final section with key takeaways"}
        ],
        "state": ["activeSection:string", "scrollProgress:number"],
        "interactions": ["scroll-triggered reveals", "ToC highlight on scroll", "progress bar"]
    },
    "concept-explorer": {
        "sections": [
            {"id": "hero", "component": "hero-editorial", "notes": "Title, thesis"},
            {"id": "thesis-card", "component": "thesis-card", "notes": "One-sentence thesis, visually prominent"},
            {"id": "concepts", "component": "concept-accordion", "notes": "3-7 concepts, expandable"},
            {"id": "relationships", "component": "concept-relationships", "notes": "Optional: visual connection between concepts"},
            {"id": "takeaways", "component": "takeaway-grid", "notes": "Summary of key ideas"}
        ],
        "state": ["openConcept:string|null"],
        "interactions": ["accordion open/close", "concept hover states"]
    },
    "comparison-matrix": {
        "sections": [
            {"id": "hero", "component": "hero-editorial", "notes": "What is being compared and why"},
            {"id": "criteria", "component": "criteria-selector", "notes": "Optional: filter by importance"},
            {"id": "comparison", "component": "comparison-matrix", "notes": "Options vs criteria grid with scores"},
            {"id": "recommendation", "component": "recommendation-card", "notes": "Bottom-line recommendation"},
            {"id": "details", "component": "expandable-detail-cards", "notes": "Per-option deep-dive"}
        ],
        "state": ["selectedCriteria:string[]", "highlightedOption:string|null"],
        "interactions": ["criteria filter", "option highlight", "detail expand"]
    },
    "timeline-experience": {
        "sections": [
            {"id": "hero", "component": "hero-editorial", "notes": "What period/evolution is covered"},
            {"id": "overview", "component": "timeline-overview", "notes": "All events at a glance"},
            {"id": "timeline", "component": "interactive-timeline", "notes": "Click events to expand detail"},
            {"id": "synthesis", "component": "pattern-callout", "notes": "What patterns emerge from the timeline"}
        ],
        "state": ["selectedEvent:string|null", "activePeriod:string|null"],
        "interactions": ["event click to expand", "period filter", "scrub animation"]
    },
    "architecture-explainer": {
        "sections": [
            {"id": "hero", "component": "hero-editorial", "notes": "System name and one-line summary"},
            {"id": "overview", "component": "system-overview-diagram", "notes": "High-level component map (SVG or CSS)"},
            {"id": "components", "component": "component-deep-dives", "notes": "Each component expandable"},
            {"id": "flow", "component": "flow-walkthrough", "notes": "Step-through of how data/requests flow"},
            {"id": "tradeoffs", "component": "tradeoff-callouts", "notes": "What this design optimises for, and at what cost"}
        ],
        "state": ["activeComponent:string|null", "flowStep:number"],
        "interactions": ["component click/hover", "flow step-through", "tradeoff toggle"]
    },
    "data-dashboard": {
        "sections": [
            {"id": "hero", "component": "hero-data", "notes": "Title + most striking stat as hero number"},
            {"id": "stats", "component": "stat-card-row", "notes": "3-5 KPI cards with count-up animation"},
            {"id": "chart", "component": "main-visualization", "notes": "Primary chart or comparison visual"},
            {"id": "insights", "component": "insight-cards", "notes": "Key findings from the data"},
            {"id": "methodology", "component": "collapsible-methodology", "notes": "Source and methodology, collapsed by default"}
        ],
        "state": ["hoveredDataPoint:string|null", "activeFilter:string"],
        "interactions": ["data hover tooltips", "filter controls", "count-up on entry"]
    }
}


def build_content_mapping(sections: list, interaction_model: str) -> list:
    """Map article sections to page components."""
    template = MODEL_PAGE_TEMPLATES.get(interaction_model, MODEL_PAGE_TEMPLATES["scroll-journey"])
    page_sections = template["sections"].copy()

    # Inject article section labels into relevant components
    content_sections = [s for s in sections if s.get("role") != "static-editorial"]

    for page_sec in page_sections:
        if page_sec.get("component") in ("step-sequencer", "concept-accordion", "scroll-reveal-sections"):
            page_sec["article_sections"] = [
                {"id": s["id"], "label": s["label"], "role": s.get("role", "static-editorial")}
                for s in sections
            ]

    return page_sections


def build_blueprint(structure: dict) -> dict:
    """Assemble the full page blueprint."""
    rec = structure["recommendation"]
    analysis = structure["analysis"]
    metadata = structure["metadata"]
    sections = structure["sections"]
    concepts = structure["concepts"]

    interaction_model = rec["interaction_model"]
    design_direction = rec["design_direction"]

    # Bundled style overrides both design direction and interaction model
    selected_style = rec.get("selected_style")
    if selected_style and selected_style in DESIGN_SYSTEMS:
        design_direction = selected_style
        interaction_model = STYLE_INTERACTION_OVERRIDES.get(selected_style, interaction_model)

    design_system = DESIGN_SYSTEMS.get(design_direction, DESIGN_SYSTEMS["dark-technical"])
    template = MODEL_PAGE_TEMPLATES.get(interaction_model, MODEL_PAGE_TEMPLATES["scroll-journey"])
    page_sections = build_content_mapping(sections, interaction_model)

    # Determine special components to include
    special_components = []
    if analysis.get("has_data"):
        special_components.append("stat-cards-with-count-up")
    if analysis.get("has_code"):
        special_components.append("code-block-with-copy")
    if analysis.get("has_comparison"):
        special_components.append("comparison-highlight")

    # Pull best quote from concepts/sections
    pull_quote_candidates = [
        s["label"] for s in sections if s.get("has_quote")
    ]

    blueprint = {
        "meta": {
            "title": metadata.get("title", ""),
            "author": metadata.get("author", ""),
            "date": metadata.get("date", ""),
            "subtitle": metadata.get("subtitle", "")
        },
        "analysis_summary": {
            "article_type": analysis["article_type"],
            "thesis": analysis.get("thesis", ""),
            "word_count": analysis.get("word_count", 0),
            "degrade_to_static": rec["degrade_to_static"],
            "degrade_reason": rec.get("degrade_reason", "")
        },
        "design": {
            "direction": design_direction,
            "selected_style": selected_style,
            "theme": design_system["theme"],
            "fonts": {
                "display": design_system["font_display"],
                "body": design_system["font_body"],
                "mono": design_system.get("font_mono", ""),
                "import_url": design_system["font_import"]
            },
            "palette": design_system["palette"]
        },
        "interaction": {
            "model": interaction_model,
            "label": rec["interaction_label"],
            "reason": rec["reason"],
            "state_variables": template.get("state", []),
            "interaction_types": template.get("interactions", [])
        },
        "page_structure": {
            "sections": page_sections,
            "special_components": special_components,
            "pull_quote_sections": pull_quote_candidates
        },
        "content_map": {
            "concepts": concepts,
            "article_sections": [
                {
                    "id": s["id"],
                    "label": s["label"],
                    "role": s.get("role", "static-editorial"),
                    "has_code": s.get("has_code", False),
                    "has_list": s.get("has_list", False),
                    "block_count": s.get("block_count", 0)
                }
                for s in sections
            ]
        },
        "accessibility": {
            "keyboard_nav": True,
            "aria_labels": "required on all interactive elements",
            "focus_visible": "required",
            "motion_reduce": "respect prefers-reduced-motion"
        },
        "implementation_notes": [
            f"Use {design_system['font_display']} for headings and display text",
            f"Use {design_system['font_body']} for body copy",
            f"Primary palette: bg={design_system['palette']['bg']}, accent={design_system['palette']['accent']}",
            f"Interaction model: {interaction_model} — {rec['reason'][:80]}",
            "All content must be grounded in source article — no invented claims",
            "Page load: staggered reveal animation on all above-fold elements",
            "Mobile: declare responsive behavior, test at 375px width",
        ] + ([f"Style mode: {selected_style} — bundled layout philosophy and visual identity"] if selected_style else [])
    }

    return blueprint


def main():
    parser = argparse.ArgumentParser(description='Build implementation blueprint from article structure')
    parser.add_argument('--input', '-i', default='structure.json', help='Structure JSON from extract_structure.py')
    parser.add_argument('--output', '-o', default='blueprint.json', help='Output blueprint JSON')
    args = parser.parse_args()

    structure = json.loads(Path(args.input).read_text(encoding='utf-8'))
    blueprint = build_blueprint(structure)

    Path(args.output).write_text(json.dumps(blueprint, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"✓ Blueprint built → {args.output}")
    print(f"\n  {'─'*40}")
    print(f"  Interaction model : {blueprint['interaction']['label']}")
    print(f"  Design direction  : {blueprint['design']['direction']}")
    if blueprint['design'].get('selected_style'):
        print(f"  Style mode        : {blueprint['design']['selected_style']}")
    print(f"  Theme             : {blueprint['design']['theme']}")
    print(f"  Font (display)    : {blueprint['design']['fonts']['display']}")
    print(f"  Font (body)       : {blueprint['design']['fonts']['body']}")
    print(f"  Page sections     : {len(blueprint['page_structure']['sections'])}")
    print(f"  Degrade to static : {blueprint['analysis_summary']['degrade_to_static']}")
    print(f"  {'─'*40}")
    print(f"\n  Claude: read blueprint.json before writing any code.")
    print(f"  The design system tokens and page structure are your implementation contract.")


if __name__ == '__main__':
    main()
