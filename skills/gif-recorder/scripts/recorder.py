#!/usr/bin/env python3
"""
GIF Recorder Engine
Serves a pre-built local HTML file on localhost, records Playwright interaction, exports GIF.

Usage:
  python recorder.py \
    --site-dir /path/to/site \
    --steps-json /path/to/steps.json \
    --output /path/to/output.gif \
    [--width 720] [--height 1280] [--fps 12] \
    [--cursor default|highlight|minimal|animated]

Cursor modes:
  default   — plain arrow, no effects (quick recordings, internal demos)
  highlight — yellow glow + click ripple (tutorials, technical walkthroughs)
  minimal   — faint halo, minimal effects (website demos, design-oriented products)
  animated  — blue multi-ring glow + trail + click burst (marketing, landing pages)

steps.json format:
  [
    {"type": "wait",   "seconds": 2},
    {"type": "scroll", "amount": 300},
    {"type": "click",  "selector": "button:has-text('Next →')"},
    {"type": "move",   "selector": "h1"},
    {"type": "snap",   "frames": 12}
  ]
"""

import asyncio
import http.server
import json
import sys
import threading
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
import imageio.v3 as iio
from playwright.async_api import async_playwright


# ── Cursor rendering ──────────────────────────────────────────────────────────

def draw_cursor(
    img: Image.Image,
    x: float,
    y: float,
    mode: str = "highlight",
    trail: list[tuple[float, float]] | None = None,
) -> Image.Image:
    """Render cursor on top of a frame according to the chosen mode."""
    base = img.convert("RGBA")

    if mode == "default":
        # Plain white arrow with dark outline — no glow, no circle
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.polygon([(x, y), (x + 16, y + 6), (x + 6, y + 16)], fill=(255, 255, 255, 235))
        d.polygon([(x + 1, y + 1), (x + 14, y + 7), (x + 7, y + 14)], fill=(30, 30, 30, 215))
        base = Image.alpha_composite(base, ov)

    elif mode == "highlight":
        # Yellow glow halo + white dot + arrow
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(255, 220, 60, 155))
        blurred = ov.filter(ImageFilter.GaussianBlur(radius=9))
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(sh)
        d2.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 245))
        d2.polygon([(x, y), (x + 15, y + 6), (x + 6, y + 15)], fill=(15, 15, 15, 225))
        base = Image.alpha_composite(base, blurred)
        base = Image.alpha_composite(base, sh)

    elif mode == "minimal":
        # Very faint white halo + small dot + arrow — almost no effect
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 255, 255, 35))
        blurred = ov.filter(ImageFilter.GaussianBlur(radius=4))
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(sh)
        d2.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 255, 255, 220))
        d2.polygon([(x, y), (x + 13, y + 5), (x + 5, y + 13)], fill=(20, 20, 20, 210))
        base = Image.alpha_composite(base, blurred)
        base = Image.alpha_composite(base, sh)

    elif mode == "animated":
        # Trail dots (fading blue circles at recent cursor positions)
        if trail:
            for i, (tx, ty) in enumerate(trail):
                alpha = int(70 * (i + 1) / len(trail))
                r = int(3 + 4 * (i + 1) / len(trail))
                ov_t = Image.new("RGBA", img.size, (0, 0, 0, 0))
                d_t = ImageDraw.Draw(ov_t)
                d_t.ellipse((tx - r, ty - r, tx + r, ty + r), fill=(100, 200, 255, alpha))
                base = Image.alpha_composite(base, ov_t)
        # Outer soft glow ring
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.ellipse((x - 36, y - 36, x + 36, y + 36), fill=(80, 160, 255, 55))
        blurred_out = ov.filter(ImageFilter.GaussianBlur(radius=14))
        # Inner tighter glow ring
        ov2 = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d2 = ImageDraw.Draw(ov2)
        d2.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(160, 210, 255, 120))
        blurred_in = ov2.filter(ImageFilter.GaussianBlur(radius=5))
        # White dot + arrow
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        d3 = ImageDraw.Draw(sh)
        d3.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 255))
        d3.polygon([(x, y), (x + 14, y + 5), (x + 5, y + 14)], fill=(10, 10, 10, 230))
        base = Image.alpha_composite(base, blurred_out)
        base = Image.alpha_composite(base, blurred_in)
        base = Image.alpha_composite(base, sh)

    return base.convert("RGB")


# ── Frame capture ──────────────────────────────────────────────────────────────

class Recorder:
    def __init__(self, w: int, h: int, fps: int, cursor_mode: str = "highlight",
                 click_settle: float = 0.6):
        self.w = w
        self.h = h
        self.fps = fps
        self.cursor_mode = cursor_mode
        self.click_settle = click_settle  # seconds to wait after click before snapping
        self.frames: list[Image.Image] = []
        self.cx = w // 2
        self.cy = h // 2
        self._trail: list[tuple[float, float]] = []  # recent positions for animated mode

    def _trail_snapshot(self) -> list[tuple[float, float]] | None:
        return self._trail[-8:] if self.cursor_mode == "animated" else None

    async def snap(self, page, n: int = 1):
        png = await page.screenshot(timeout=12000)
        img = Image.open(BytesIO(png)).convert("RGB").crop((0, 0, self.w, self.h))
        img = draw_cursor(img, self.cx, self.cy, self.cursor_mode, self._trail_snapshot())
        for _ in range(n):
            self.frames.append(img.copy())

    async def move_to(self, page, tx: float, ty: float, steps: int = 22, every: int = 4):
        sx, sy = self.cx, self.cy
        for i in range(1, steps + 1):
            t = i / steps
            t = t * t * (3 - 2 * t)  # ease-in-out
            self.cx = sx + (tx - sx) * t
            self.cy = sy + (ty - sy) * t
            if self.cursor_mode == "animated":
                self._trail.append((self.cx, self.cy))
                if len(self._trail) > 12:
                    self._trail.pop(0)
            await page.mouse.move(self.cx, self.cy)
            if i % every == 0:
                await self.snap(page)
        self.cx, self.cy = tx, ty

    async def click_element(self, page, selector: str):
        el = page.locator(selector).first
        bb = await el.bounding_box()
        if not bb:
            print(f"  ⚠ Element not found: {selector}", file=sys.stderr)
            return
        bx = int(bb["x"] + bb["width"] / 2)
        by = int(bb["y"] + bb["height"] / 2)
        await self.move_to(page, bx, by)
        await self.snap(page, 3)
        await page.mouse.click(bx, by)
        # Wait long enough for JS-triggered transitions to complete.
        # A common pattern: setTimeout(180ms) + rAF×2 + CSS transition 250ms = ~460ms.
        await asyncio.sleep(self.click_settle)
        if self.cursor_mode in ("highlight", "animated"):
            await self._ripple_frames(page, bx, by)
        else:
            await self.snap(page, 4)
        # Capture the fully-settled post-click state
        await self.snap(page, 3)

    async def _ripple_frames(self, page, x: int, y: int):
        """Animate expanding ripple / burst rings after a click."""
        png = await page.screenshot(timeout=12000)
        base_img = Image.open(BytesIO(png)).convert("RGB").crop((0, 0, self.w, self.h))
        ripple_steps = 10
        for i in range(ripple_steps):
            t = i / ripple_steps
            r = int(6 + 44 * t)
            alpha = int(230 * (1 - t))
            frame = base_img.copy().convert("RGBA")
            ov = Image.new("RGBA", frame.size, (0, 0, 0, 0))
            d = ImageDraw.Draw(ov)
            width = max(1, 3 - int(2 * t))
            if self.cursor_mode == "highlight":
                d.ellipse((x - r, y - r, x + r, y + r),
                           outline=(255, 220, 60, alpha), width=width)
            elif self.cursor_mode == "animated":
                d.ellipse((x - r, y - r, x + r, y + r),
                           outline=(100, 180, 255, alpha), width=width)
                r2 = max(4, r - 14)
                d.ellipse((x - r2, y - r2, x + r2, y + r2),
                           outline=(255, 255, 255, alpha // 2), width=1)
            frame = Image.alpha_composite(frame, ov)
            drawn = draw_cursor(frame.convert("RGB"), self.cx, self.cy,
                                self.cursor_mode, self._trail_snapshot())
            self.frames.append(drawn)

    async def scroll_by(self, page, amount: int, steps: int = 14):
        per = amount // steps
        for _ in range(steps):
            await page.mouse.wheel(0, per)
            await asyncio.sleep(0.06)
            await self.snap(page)

    async def run_steps(self, page, steps: list[dict]):
        for step in steps:
            t = step.get("type")
            if t == "wait":
                await self.snap(page, int(self.fps * step.get("seconds", 1)))
            elif t == "snap":
                await self.snap(page, step.get("frames", self.fps))
            elif t == "scroll":
                await self.scroll_by(page, step.get("amount", 300))
            elif t == "click":
                await self.click_element(page, step["selector"])
            elif t == "move":
                el = page.locator(step["selector"]).first
                bb = await el.bounding_box()
                if bb:
                    await self.move_to(page,
                                       int(bb["x"] + bb["width"] / 2),
                                       int(bb["y"] + bb["height"] / 2))
            elif t == "scroll_to_bottom":
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(0.4)
                await self.snap(page, self.fps)
            else:
                print(f"  ⚠ Unknown step type: {t}", file=sys.stderr)


# ── HTTP server ────────────────────────────────────────────────────────────────

def start_server(site_dir: str, port: int):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=site_dir, **kw)
        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


# ── GIF export ─────────────────────────────────────────────────────────────────

def export_gif(frames, out_path, fps, out_w=540, out_h=960, max_size_mb=None):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    w, h = out_w, out_h
    for attempt in range(4):
        resized = [f.resize((w, h), Image.LANCZOS) for f in frames]
        print(f"  Exporting {len(resized)} frames at {w}×{h} → {out_path}")
        iio.imwrite(str(out_path), resized, format="GIF", duration=1000 // fps, loop=0)
        size_mb = Path(out_path).stat().st_size / 1e6
        if max_size_mb is None or size_mb <= max_size_mb:
            print(f"  ✅ Done: {size_mb:.1f} MB")
            return
        # Downscale by ~30% each attempt to hit size target
        print(f"  ⚠ {size_mb:.1f} MB > {max_size_mb} MB limit — downscaling…")
        w = int(w * 0.7)
        h = int(h * 0.7)
    print(f"  ⚠ Could not reach {max_size_mb} MB after 3 downscales — saved at {size_mb:.1f} MB")


# ── Main ───────────────────────────────────────────────────────────────────────

async def main(site_dir, steps_json_path, output_gif, width, height, fps, cursor_mode,
               click_settle, out_w, out_h, max_size_mb):
    PORT = 9127

    steps = json.loads(Path(steps_json_path).read_text())
    rec = Recorder(width, height, fps, cursor_mode, click_settle)
    srv = start_server(site_dir, PORT)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        ctx = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
        )
        await ctx.add_init_script("document.documentElement.style.cursor='none'")
        page = await ctx.new_page()

        print("  Loading local page…")
        await page.goto(
            f"http://127.0.0.1:{PORT}/index.html",
            wait_until="load",   # wait for subresources (CSS, images) to finish
            timeout=15000,
        )
        # Wait for web fonts to finish loading (Google Fonts, CDN fonts, etc.)
        await page.evaluate("document.fonts.ready")
        await asyncio.sleep(0.5)  # allow JS/CSS animations to initialise

        print(f"  Running {len(steps)} steps… (cursor: {cursor_mode})")
        await rec.run_steps(page, steps)

        await browser.close()

    srv.shutdown()
    print(f"  Captured {len(rec.frames)} frames")
    export_gif(rec.frames, output_gif, fps, out_w=out_w, out_h=out_h, max_size_mb=max_size_mb)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir",    default="/home/claude/gif_site")
    parser.add_argument("--steps-json",  default="/home/claude/gif_steps.json")
    parser.add_argument("--output",      default="/mnt/user-data/outputs/demo.gif")
    parser.add_argument("--width",  type=int, default=720)
    parser.add_argument("--height", type=int, default=1280)
    parser.add_argument("--fps",    type=int, default=12)
    parser.add_argument("--cursor",
                        choices=["default", "highlight", "minimal", "animated"],
                        default="highlight",
                        help="Cursor style (default: highlight)")
    parser.add_argument("--click-settle", type=float, default=0.6,
                        help="Seconds to wait after each click for JS/CSS transitions to complete "
                             "(default: 0.6). Increase to 0.8–1.2 for heavy animated UIs.")
    parser.add_argument("--out-width",  type=int, default=540,
                        help="Output GIF width in pixels (default: 540)")
    parser.add_argument("--out-height", type=int, default=960,
                        help="Output GIF height in pixels (default: 960)")
    parser.add_argument("--max-size", default="unlimited",
                        help="Max output file size in MB, e.g. 5, 10, or 'unlimited' (default: unlimited). "
                             "If exceeded, output is automatically downscaled up to 3 times.")
    args = parser.parse_args()
    max_size_mb = None if args.max_size == "unlimited" else float(args.max_size)
    asyncio.run(main(args.site_dir, args.steps_json, args.output,
                     args.width, args.height, args.fps, args.cursor, args.click_settle,
                     args.out_width, args.out_height, max_size_mb))
