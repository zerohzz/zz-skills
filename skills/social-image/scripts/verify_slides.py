#!/usr/bin/env python3
"""
verify_slides.py

Open each HTML slide via Playwright, measure actual rendered content height
vs available viewport height, and report which slides need fill components.

Usage:
    python3 verify_slides.py --input-dir slides/ --width 1080 --height 1920 \
        --output verify_report.json
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print(
        "playwright not found. Install with: pip install playwright && playwright install chromium"
    )
    sys.exit(1)


# Thresholds for fill ratio classification
PASS_THRESHOLD = 0.75
WARN_THRESHOLD = 0.60


async def _measure_slide(page, is_cover: bool) -> dict:
    """Measure content height vs available height for a single slide."""
    return await page.evaluate("""(isCover) => {
        const inner = document.querySelector('.card-inner');
        if (!inner) return { content_height_px: 0, available_height_px: 0, error: 'no .card-inner' };

        const innerRect = inner.getBoundingClientRect();
        const innerStyle = getComputedStyle(inner);
        const padTop = parseFloat(innerStyle.paddingTop);
        const padBottom = parseFloat(innerStyle.paddingBottom);
        const availableHeight = innerRect.height - padTop - padBottom;

        if (isCover) {
            // Cover uses .cover-inner layout — measure all children
            const children = inner.children;
            let totalHeight = 0;
            for (const child of children) {
                totalHeight += child.getBoundingClientRect().height;
            }
            // Account for gap between flex children
            const gap = parseFloat(getComputedStyle(inner).gap) || 0;
            totalHeight += Math.max(0, children.length - 1) * gap;
            return {
                content_height_px: Math.round(totalHeight),
                available_height_px: Math.round(availableHeight),
            };
        }

        // Content slides — measure actual children height inside .card-content
        // Note: .card-content has flex:1 so scrollHeight = stretched height, not content height.
        // We measure children's bounding rects instead.
        const content = document.querySelector('.card-content');
        if (!content) return { content_height_px: 0, available_height_px: Math.round(availableHeight), error: 'no .card-content' };

        // Sum actual children heights (including margins)
        const children = content.children;
        let contentHeight = 0;
        if (children.length > 0) {
            const firstRect = children[0].getBoundingClientRect();
            const lastChild = children[children.length - 1];
            const lastRect = lastChild.getBoundingClientRect();
            // Distance from top of first child to bottom of last child
            contentHeight = lastRect.bottom - firstRect.top;
        }

        // Also account for swipe-hint/cta-hint space (these are siblings of .card-content)
        const swipe = document.querySelector('.swipe-hint') || document.querySelector('.cta-hint');
        let reservedBottom = 0;
        if (swipe) reservedBottom += swipe.getBoundingClientRect().height + 16;

        return {
            content_height_px: Math.round(contentHeight),
            available_height_px: Math.round(availableHeight - reservedBottom),
        };
    }""", is_cover)


def _classify(fill_ratio: float) -> str:
    if fill_ratio >= PASS_THRESHOLD:
        return "pass"
    if fill_ratio >= WARN_THRESHOLD:
        return "warn"
    return "sparse"


async def verify_all(input_dir: str, width: int, height: int) -> dict:
    input_path = Path(input_dir).resolve()
    html_files = sorted(input_path.glob("*.html"))
    if not html_files:
        print(f"No HTML files found in {input_dir}")
        return {}

    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1.0,  # measure at 1x for accurate CSS pixel values
        )

        for html_file in html_files:
            name = html_file.stem
            is_cover = "cover" in name.lower()
            page = await ctx.new_page()
            url = "file://" + str(html_file.resolve())

            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception:
                pass

            # Wait for fonts to settle (affects line heights)
            try:
                await page.evaluate("() => document.fonts.ready")
                await page.wait_for_timeout(100)
            except Exception:
                pass

            measurements = await _measure_slide(page, is_cover)
            await page.close()

            content_h = measurements.get("content_height_px", 0)
            available_h = measurements.get("available_height_px", 1)
            error = measurements.get("error")

            if error:
                results[name] = {"error": error, "status": "error"}
                print(f"  ✗ {name}: {error}")
                continue

            fill_ratio = round(content_h / max(available_h, 1), 2)
            gap_px = max(0, available_h - content_h)
            status = _classify(fill_ratio)

            results[name] = {
                "content_height_px": content_h,
                "available_height_px": available_h,
                "fill_ratio": fill_ratio,
                "gap_px": gap_px,
                "status": status,
            }

            icon = {"pass": "✓", "warn": "△", "sparse": "✗"}[status]
            print(f"  {icon} {name}: {fill_ratio:.0%} filled ({content_h}/{available_h}px) gap={gap_px}px → {status}")

        await browser.close()

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Verify slide whitespace by measuring actual rendered content height."
    )
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing HTML slide files")
    parser.add_argument("--width", "-W", type=int, default=1080, help="Viewport width (default: 1080)")
    parser.add_argument("--height", "-H", type=int, default=1920, help="Viewport height (default: 1920)")
    parser.add_argument("--output", "-o", default=None, help="Output JSON report path (optional)")
    args = parser.parse_args()

    print(f"Verifying slides in {args.input_dir} at {args.width}x{args.height}...")
    results = asyncio.run(verify_all(args.input_dir, args.width, args.height))

    # Summary
    statuses = [r.get("status") for r in results.values()]
    pass_count = statuses.count("pass")
    warn_count = statuses.count("warn")
    sparse_count = statuses.count("sparse")
    total = len(statuses)
    print(f"\n{'✓' if sparse_count == 0 else '⚠'} {pass_count}/{total} pass, {warn_count} warn, {sparse_count} sparse")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"Report written to {args.output}")

    # Exit code: 1 if any sparse slides
    sys.exit(1 if sparse_count > 0 else 0)


if __name__ == "__main__":
    main()
