#!/usr/bin/env python3
"""
render_slides.py

Render HTML slide files to PNG images using Playwright.
Each HTML file in --input-dir is screenshotted to --output-dir.

Usage:
    python3 render_slides.py --input-dir slides/ --output-dir output/ \
        --width 1080 --height 1440 --dpr 2
"""

import argparse
import asyncio
import sys
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print(
        "playwright not found. Install with: pip install playwright && playwright install chromium"
    )
    sys.exit(1)


MAX_RETRIES = 3


async def _wait_for_fonts(page, timeout_ms: int = 5000) -> bool:
    """Wait for document.fonts.ready and verify at least one custom font loaded."""
    try:
        await page.evaluate("() => document.fonts.ready")
        await page.wait_for_timeout(100)  # minimal layout settle time
        font_count = await page.evaluate("() => document.fonts.size")
        return font_count > 0
    except Exception:
        return False


async def _verify_slide(page, name: str, width: int, height: int) -> list:
    """Run visual verification checks. Returns list of warning strings."""
    warnings = []

    # 1. Font verification — check if any custom fonts loaded
    font_count = await page.evaluate("() => document.fonts.size")
    if font_count == 0:
        warnings.append(f"no custom fonts loaded")

    # 2. Content overflow check
    actual_height = await page.evaluate(
        "() => document.querySelector('.card-container')?.scrollHeight || document.body.scrollHeight"
    )
    if actual_height > height * 1.02:
        warnings.append(f"content overflow ({actual_height}px > {height}px)")

    # 3. Blank slide detection — sample center pixels for variance
    is_blank = await page.evaluate("""() => {
        const el = document.querySelector('.card-content');
        if (!el) return true;
        const rect = el.getBoundingClientRect();
        return rect.height < 10;
    }""")
    if is_blank:
        warnings.append("blank or empty slide (card-content height < 10px)")

    return warnings


async def _render_single(ctx, html_file, output_path, width, height, dpr) -> tuple:
    """Render a single HTML slide with retry logic. Returns (name, success, warnings)."""
    name = html_file.stem
    out_file = output_path / f"{name}.png"

    for attempt in range(1, MAX_RETRIES + 1):
        page = await ctx.new_page()
        await page.set_viewport_size({"width": width, "height": height})

        url = "file://" + str(html_file.resolve())
        try:
            await page.goto(url, wait_until="networkidle", timeout=15000)
        except Exception:
            pass  # proceed — fonts may still load

        # Wait for fonts properly instead of arbitrary sleep
        fonts_ok = await _wait_for_fonts(page)
        if not fonts_ok and attempt < MAX_RETRIES:
            await page.close()
            print(f"  ↻ {name}: fonts not ready, retry {attempt}/{MAX_RETRIES}")
            await asyncio.sleep(1)
            continue

        # Verify slide quality
        warnings = await _verify_slide(page, name, width, height)

        # Retry on critical issues (blank slide) if attempts remain
        has_critical = any("blank" in w for w in warnings)
        if has_critical and attempt < MAX_RETRIES:
            await page.close()
            print(f"  ↻ {name}: {warnings[0]}, retry {attempt}/{MAX_RETRIES}")
            await asyncio.sleep(0.5)
            continue

        # Capture screenshot
        await page.screenshot(
            path=str(out_file),
            clip={"x": 0, "y": 0, "width": width, "height": height},
        )
        await page.close()

        # Report
        status = "✓" if not warnings else "⚠"
        print(f"{status} {name}.png ({width * dpr:.0f}x{height * dpr:.0f}px @ {dpr}x)")
        for w in warnings:
            print(f"  ⚠ {name}: {w}")

        return name, True, warnings

    return name, False, [f"failed after {MAX_RETRIES} retries"]


async def render_all(input_dir: str, output_dir: str, width: int, height: int, dpr: float):
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    html_files = sorted(input_path.glob("*.html"))
    if not html_files:
        print(f"No HTML files found in {input_dir}")
        return 0

    count = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=dpr,
        )

        for html_file in html_files:
            name, success, warnings = await _render_single(
                ctx, html_file, output_path, width, height, dpr
            )
            if success:
                count += 1

        await browser.close()

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Render HTML slide files to PNG images using Playwright."
    )
    parser.add_argument(
        "--input-dir", "-i",
        required=True,
        help="Directory containing HTML files",
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help="Directory to write PNG files",
    )
    parser.add_argument(
        "--width", "-W",
        type=int,
        default=1080,
        help="Viewport width in CSS pixels (default: 1080)",
    )
    parser.add_argument(
        "--height", "-H",
        type=int,
        default=1440,
        help="Viewport height in CSS pixels (default: 1440)",
    )
    parser.add_argument(
        "--dpr", "-d",
        type=float,
        default=2.0,
        help="Device pixel ratio / scale factor for Retina output (default: 2)",
    )
    args = parser.parse_args()

    count = asyncio.run(
        render_all(args.input_dir, args.output_dir, args.width, args.height, args.dpr)
    )
    print(f"✓ Rendered {count} slides to {args.output_dir}/")


if __name__ == "__main__":
    main()
