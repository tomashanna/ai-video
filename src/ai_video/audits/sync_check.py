#!/usr/bin/env python3
"""
sync-check.py — Frame-perfect sync verification (audio impact ↔ visual response).

Generado 2026-05-13. Detecta SFX impact events en index.html, extrae frames
del render alrededor de cada impact timestamp, y mide cambio visual via brightness
delta. Si hay impact audio sin visual response significativa → flag.

Por qué importa:
- Audio-reactive motion sin testing = sync drift invisible
- Un white-flash a 30.0s con scale pop a 30.15s = viewer percibe "lag"
- audit-frames.py mide quality general; audit-audio.py mide audio quality;
  sync-check.py es el bridge entre ambos.

Usage:
  python sync-check.py --video renders/draft.mp4 --html index.html [--threshold 0.05]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# SFX impact keywords (detect impact events from src name)
IMPACT_KEYWORDS = [
    "white-flash", "flash", "thud", "body-fall", "body-thud",
    "sub-bass", "stab", "impact", "punch", "slam", "crack",
    "glass-shatter", "scream", "scream-cut",
]

# Default visual change threshold (brightness delta)
DEFAULT_THRESHOLD = 0.05  # 5% brightness change minimum

# Time offsets around impact to capture (seconds)
PRE_OFFSET = 0.1   # frame BEFORE impact
POST_OFFSET = 0.15 # frame AFTER impact (small lag tolerated)


def parse_impact_events(html_path: str) -> list:
    """Extract SFX impact events from index.html."""
    if not os.path.exists(html_path):
        return []
    with open(html_path) as f:
        content = f.read()
    pattern = re.compile(
        r'<audio[^>]+src="([^"]+)"[^>]+data-start="([\d.]+)"',
        re.DOTALL
    )
    events = []
    for m in pattern.finditer(content):
        src = m.group(1)
        start = float(m.group(2))
        src_lower = src.lower()
        if any(kw in src_lower for kw in IMPACT_KEYWORDS):
            events.append({"src": src, "time": start})
    return events


def extract_frame(video: str, t: float, out: str) -> bool:
    """Extract a single frame at time t."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-ss", str(t), "-i", video, "-frames:v", "1",
             "-q:v", "3", out],
            capture_output=True, text=True, timeout=10
        )
        return os.path.exists(out)
    except Exception as e:
        print(f"  ERROR extracting frame at {t}s: {e}")
        return False


def measure_brightness(image_path: str) -> float:
    """Measure average brightness of an image (0-255 → 0.0-1.0)."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error",
             "-i", image_path,
             "-vf", "format=gray,signalstats",
             "-f", "null", "-"],
            capture_output=True, text=True, timeout=10
        )
        # signalstats writes YAVG=<value> to stderr
        m = re.search(r"YAVG:(\d+\.?\d*)", result.stderr)
        if m:
            return float(m.group(1)) / 255.0
    except Exception:
        pass
    return 0.5  # default mid-gray on error


def analyze_impact(video: str, event: dict, threshold: float, debug_dir: str) -> dict:
    """Analyze a single impact event."""
    t = event["time"]
    pre_path = os.path.join(debug_dir, f"impact-{t:.2f}-pre.jpg")
    post_path = os.path.join(debug_dir, f"impact-{t:.2f}-post.jpg")

    extract_frame(video, t - PRE_OFFSET, pre_path)
    extract_frame(video, t + POST_OFFSET, post_path)

    if not (os.path.exists(pre_path) and os.path.exists(post_path)):
        return {"event": event, "status": "ERROR", "delta": 0.0}

    pre_b = measure_brightness(pre_path)
    post_b = measure_brightness(post_path)
    delta = abs(post_b - pre_b)

    status = "PASS" if delta >= threshold else "FAIL"
    return {
        "event": event,
        "pre_frame": pre_path,
        "post_frame": post_path,
        "pre_brightness": round(pre_b, 3),
        "post_brightness": round(post_b, 3),
        "delta": round(delta, 3),
        "threshold": threshold,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Verify audio impacts have visual response (frame-perfect sync)."
    )
    parser.add_argument("--video", required=True, help="Path to MP4 render")
    parser.add_argument("--html", required=True, help="Path to index.html")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Min brightness delta to count as visual response (default {DEFAULT_THRESHOLD})")
    parser.add_argument("--debug-dir", default="renders/debug-sync",
                        help="Where to save extracted frames")
    parser.add_argument("--output", help="Save JSON report")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video not found: {args.video}")
        return 2
    if not os.path.exists(args.html):
        print(f"ERROR: html not found: {args.html}")
        return 2

    Path(args.debug_dir).mkdir(parents=True, exist_ok=True)

    print("🎬 Frame-perfect sync check")
    print(f"   Video: {args.video}")
    print(f"   HTML: {args.html}")
    print()

    events = parse_impact_events(args.html)
    if not events:
        print("ℹ️  No impact events detected (no SFX matching keywords: " + ", ".join(IMPACT_KEYWORDS[:5]) + "...)")
        print("   This is OK if the video has no scripted impacts. Otherwise check sfx naming.")
        return 0

    print(f"Detected {len(events)} impact events:")
    for e in events:
        print(f"  - {e['time']:.2f}s: {e['src']}")
    print()

    results = []
    fails = []
    for event in events:
        r = analyze_impact(args.video, event, args.threshold, args.debug_dir)
        results.append(r)
        symbol = "✓" if r["status"] == "PASS" else "✗" if r["status"] == "FAIL" else "?"
        print(f"  {symbol} {event['time']:.2f}s {event['src']}: "
              f"brightness {r.get('pre_brightness', '?')} → {r.get('post_brightness', '?')}, "
              f"delta {r['delta']} (threshold {args.threshold})")
        if r["status"] == "FAIL":
            fails.append(r)

    print()
    print(f"Results: {len(results) - len(fails)}/{len(results)} impacts have visual response")

    if args.output:
        with open(args.output, "w") as f:
            json.dump({"events": events, "results": results}, f, indent=2)
        print(f"Report saved: {args.output}")

    if fails:
        print()
        print(f"❌ SYNC CHECK FAILED — {len(fails)} impact(s) have no visual response (delta < {args.threshold})")
        print("   Posibles causas:")
        print("   - SFX impact sin animation reactiva (whip pan, scale pop, brightness flash)")
        print("   - Animation existe pero está fuera del rango ±0.15s del audio")
        print("   - Animation muy sutil (delta < threshold)")
        print()
        print(f"   Ver frames extraídos en: {args.debug_dir}/")
        print("   Ver: ai-video-production/MOTION-LAYER.md § 'Audio-reactive motion'")
        return 1

    print("✅ SYNC CHECK PASSED — all impacts have visual response")
    return 0


if __name__ == "__main__":
    sys.exit(main())
