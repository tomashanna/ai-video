#!/usr/bin/env python3
"""
build-canonical-scenes.py — Generate per-referent scene-by-scene canonical markdown.

Pipeline:
  1. Load: transcription.json + scene_cuts.txt + ui-elements.json + descriptive-analysis/ref-XX.md
  2. De-cluster scene_cuts (timestamps within 200ms = same boundary)
  3. Cluster boundaries into scenes (consolidate consecutive close cuts)
  4. Per scene: extract narration + UI active + visual (from gemini-frames-analysis OR call Gemini)
  5. Output markdown per CANONICAL-SCENE-SCHEMA.md

Usage:
  python build-canonical-scenes.py --input <ref_folder> --output <output_dir> \\
      [--filename <custom_name.md>] [--pattern <P1-P10>] [--score <X.XX>] \\
      [--source-video <MP4_path>] [--use-gemini]

Honesty rule: if raw data insufficient for a field → write [NEEDS VALIDATION], NOT invent.

Cost: ~$0.20 per ref if Gemini calls needed (6 frames × $0.002 typical).
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


# ─── Constants ──────────────────────────────────────────────────────────────

DECLUSTER_WINDOW_S = 0.5  # cuts within 0.5s = same scene boundary
MIN_SCENE_DURATION_S = 1.0  # don't create scenes shorter than this
PATTERN_CATEGORIES_RANGES = [
    # (category, start_pct, end_pct) — heuristic mapping
    ("hook", 0.0, 0.15),
    ("setup_post_hook", 0.15, 0.25),
    ("decision_setup", 0.25, 0.32),
    ("decision_countdown", 0.32, 0.35),
    ("consequence_A", 0.35, 0.45),
    ("rama_B_transition", 0.45, 0.50),
    ("consequence_B", 0.50, 0.60),
    ("decision_setup", 0.60, 0.66),
    ("decision_countdown", 0.66, 0.69),
    ("consequence_A", 0.69, 0.80),
    ("rama_B_transition", 0.80, 0.85),
    ("cliffhanger", 0.85, 1.00),
]


# ─── Helpers ────────────────────────────────────────────────────────────────


def load_json(path: Path) -> Any:
    """Tolerant loader — fixes common non-strict JSON (leading-dot floats like .11)."""
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Fix leading-dot floats: ": .11" → ": 0.11"
        raw = path.read_text()
        fixed = re.sub(r":\s*\.(\d)", r": 0.\1", raw)
        try:
            return json.loads(fixed)
        except json.JSONDecodeError as e:
            print(f"WARN: {path.name} unparseable even after leading-dot fix: {e}", file=sys.stderr)
            return None


def parse_scene_cuts(path: Path) -> list[float]:
    """Read scene_cuts.txt → sorted list of timestamps (float)."""
    if not path.exists():
        return []
    cuts = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            cuts.append(float(line))
        except ValueError:
            continue
    return sorted(cuts)


def decluster_cuts(cuts: list[float], window: float = DECLUSTER_WINDOW_S) -> list[float]:
    """Merge cuts within `window` seconds into single boundary (take first)."""
    if not cuts:
        return []
    result = [cuts[0]]
    for c in cuts[1:]:
        if c - result[-1] > window:
            result.append(c)
    return result


def cluster_into_scenes(
    boundaries: list[float], video_duration: float, min_duration: float = MIN_SCENE_DURATION_S
) -> list[tuple[float, float]]:
    """Build [start, end] scene ranges from boundary list. Drop scenes <min_duration."""
    if not boundaries:
        return [(0.0, video_duration)]
    starts = [0.0] + boundaries
    ends = boundaries + [video_duration]
    scenes = []
    for s, e in zip(starts, ends):
        if e - s >= min_duration:
            scenes.append((s, e))
    return scenes


def overlapping_segments(
    segments: list[dict], t_start: float, t_end: float
) -> list[dict]:
    """Whisper segments that overlap [t_start, t_end]."""
    return [
        s for s in segments
        if s["end"] >= t_start and s["start"] <= t_end
    ]


def ui_keyframes_in_range(
    ui_data: dict, t_start: float, t_end: float
) -> dict:
    """ui-elements.json keys are 'frame_XX.X' (timestamp). Return dict of matching frames."""
    if not ui_data:
        return {}
    result = {}
    for key, value in ui_data.items():
        m = re.match(r"frame_([\d.]+)", key)
        if not m:
            continue
        ts = float(m.group(1))
        if t_start <= ts <= t_end:
            result[key] = value
    return result


def map_pattern_category(t_start: float, t_end: float, duration: float) -> str:
    """Heuristic mapping (start_pct → category). NOT a definitive assignment."""
    pct_start = t_start / duration if duration > 0 else 0
    for cat, lo, hi in PATTERN_CATEGORIES_RANGES:
        if lo <= pct_start < hi:
            return cat
    return "cliffhanger"


def format_timestamp(seconds: float) -> str:
    """seconds → MM:SS"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


# ─── Gemini Vision (optional) ───────────────────────────────────────────────


def call_gemini_on_frame(frame_path: Path) -> str:
    """Call Gemini Vision on 1 frame, return short description. Returns [NEEDS VALIDATION] on error."""
    try:
        import google.genai as genai
        from dotenv import load_dotenv

        # Try common env locations
        for env_path in [
            "<repo-root>/mina-abandonada/.env",
            "<repo-root>/elige-companero/.env",
            "<repo-root>/cabina-14/.env",
        ]:
            if os.path.exists(env_path):
                load_dotenv(env_path)
                break

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "[NEEDS VALIDATION] (no GEMINI_API_KEY)"

        client = genai.Client(api_key=api_key)
        with open(frame_path, "rb") as f:
            img_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": img_bytes}},
                        {
                            "text": (
                                "Describí este frame en 2-3 oraciones LITERALES (NO interpretativas). "
                                "Mencioná: 1) characters/objects visibles y qué hacen, 2) camera shot type (wide/medium/close-up/POV), "
                                "3) UI elements on-screen si hay (countdown, choice buttons, captions). "
                                "Sin adjetivos abstractos ('uncanny', 'tenebroso'). Solo qué se ve."
                            )
                        },
                    ]
                }
            ],
        )
        return response.text.strip()[:500]
    except Exception as e:
        return f"[NEEDS VALIDATION] (Gemini call failed: {type(e).__name__})"


def visual_for_scene(
    gemini_data: dict | None,
    frames_dir: Path,
    t_start: float,
    t_end: float,
    use_gemini: bool,
) -> tuple[str, int]:
    """Return (visual_description, gemini_calls_used)."""
    if gemini_data:
        # Find frames in gemini_data within range
        frame_keys = [
            k for k, _ in gemini_data.items()
            if isinstance(k, str) and re.match(r"frame_([\d.]+)", k)
        ]
        in_range = []
        for k in frame_keys:
            m = re.match(r"frame_([\d.]+)", k)
            if not m:
                continue
            ts = float(m.group(1))
            if t_start <= ts <= t_end:
                in_range.append((ts, k))
        if in_range:
            in_range.sort()
            # Use first/last frame summary
            desc_parts = []
            for ts, k in in_range[:2]:  # max 2 frames per scene to keep concise
                v = gemini_data[k]
                if isinstance(v, dict):
                    snippet = v.get("description") or v.get("imagen") or str(v)[:200]
                else:
                    snippet = str(v)[:200]
                desc_parts.append(f"  - @{ts:.1f}s: {snippet}")
            return ("\n".join(desc_parts), 0)

    # No pre-analyzed data → optional Gemini call
    if use_gemini and frames_dir.exists():
        # Pick 1 frame from middle of scene
        mid = (t_start + t_end) / 2
        all_frames = sorted(frames_dir.glob("*.jpg"))
        if not all_frames:
            return ("[NEEDS VALIDATION] (no frames in folder)", 0)
        # Best heuristic: frames named frame_XX.X.jpg with timestamp
        closest = None
        closest_diff = float("inf")
        for fp in all_frames:
            m = re.search(r"([\d.]+)", fp.stem)
            if m:
                try:
                    ts = float(m.group(1))
                    diff = abs(ts - mid)
                    if diff < closest_diff:
                        closest_diff = diff
                        closest = fp
                except ValueError:
                    pass
        if closest is None:
            closest = all_frames[len(all_frames) // 2]
        desc = call_gemini_on_frame(closest)
        return (f"  - @{mid:.1f}s ({closest.name}): {desc}", 1)

    return ("[NEEDS VALIDATION] (no gemini-frames-analysis.json, --use-gemini OFF)", 0)


# ─── Main scene-building ────────────────────────────────────────────────────


def build_scene_block(
    scene_idx: int,
    t_start: float,
    t_end: float,
    transcription_segments: list[dict],
    ui_data: dict,
    gemini_data: dict | None,
    frames_dir: Path,
    duration_total: float,
    use_gemini: bool,
) -> tuple[str, int]:
    """Build markdown for one scene. Returns (md_block, gemini_calls_used)."""
    duration = t_end - t_start
    pattern_cat = map_pattern_category(t_start, t_end, duration_total)

    narr_segments = overlapping_segments(transcription_segments, t_start, t_end)
    if narr_segments:
        narr_lines = [
            f'- [{s["start"]:.1f}-{s["end"]:.1f}s]: "{s["text"].strip()}"'
            for s in narr_segments
        ]
        narration_text = "\n".join(narr_lines)
    else:
        narration_text = "[no narration in this range — silencio o pura música]"

    ui_in_range = ui_keyframes_in_range(ui_data, t_start, t_end)
    if ui_in_range:
        ui_summary_parts = []
        for k, v in list(ui_in_range.items())[:3]:
            if isinstance(v, dict):
                active = [el for el, present in v.items() if present and el != "frame"]
                ui_summary_parts.append(f"  - {k}: {', '.join(active) if active else 'no UI active'}")
            else:
                ui_summary_parts.append(f"  - {k}: {str(v)[:120]}")
        ui_summary = "\n".join(ui_summary_parts)
    else:
        ui_summary = "[NEEDS VALIDATION] (no UI keyframes sampled in this range)"

    visual_desc, calls_used = visual_for_scene(
        gemini_data, frames_dir, t_start, t_end, use_gemini
    )

    # Animation tier — heuristic placeholder (frame-to-frame diff would need recompute)
    animation_tier = "[NEEDS VALIDATION] (use manual observation of source video)"

    block = f"""## Scene {scene_idx} — [{format_timestamp(t_start)} - {format_timestamp(t_end)}] ({duration:.1f}s)

**Pattern category** (heuristic by % position): {pattern_cat}
<!-- ⚠️ Verificar manualmente — heurística por timestamp puede fallar en patterns con 2 decisions vs 3. -->

**Who's physically in scene**: [NEEDS VALIDATION] (from visual description below)

**Camera / shot type**: [NEEDS VALIDATION] (extract from Gemini analysis above)

**Setting**: [NEEDS VALIDATION] (from visual)

**Action LITERAL**:
- [NEEDS VALIDATION] (extract LITERAL verbs from visual analysis — NO abstract adjectives)

**Narration text** (literal from transcription.json):
{narration_text}

**Character dialogue** (if any):
- [NEEDS VALIDATION] (extract from transcription if voice differs from main narrator)

**Visual-narration coherence**:
[NEEDS VALIDATION] (compare visual_intent vs narration_describes — does the action LITERALLY match what narrator says?)

**UI elements active** (from ui-elements.json keyframes):
{ui_summary}

**Animation tier observed**:
{animation_tier}

**Pattern observation**:
- [NEEDS VALIDATION] (compare con otras refs en mismo pattern_category — qué patrones canónicos emergen)

**Visual analysis (raw, from Gemini)**:
{visual_desc}

---
"""
    return block, calls_used


def build_canonical_scenes(
    input_dir: Path,
    output_path: Path,
    pattern: str | None = None,
    score: str | None = None,
    source_video: str | None = None,
    use_gemini: bool = False,
) -> dict:
    """Main entry. Returns stats dict."""
    metadata = load_json(input_dir / "metadata.json")
    transcription = load_json(input_dir / "transcription.json")
    ui_data = load_json(input_dir / "ui-elements.json") or {}
    gemini_data = load_json(input_dir / "gemini-frames-analysis.json")
    scene_cuts_path = input_dir / "scene_cuts.txt"
    frames_dir = input_dir / "frames"

    if not transcription:
        return {"error": f"transcription.json missing in {input_dir}"}

    duration_total = None
    if metadata:
        duration_total = metadata.get("duration_s") or metadata.get("duration")
    if duration_total is None and transcription.get("segments"):
        duration_total = max(s["end"] for s in transcription["segments"]) + 2.0

    if not duration_total:
        return {"error": "could not determine video duration"}

    raw_cuts = parse_scene_cuts(scene_cuts_path)
    boundaries = decluster_cuts(raw_cuts)
    scenes = cluster_into_scenes(boundaries, duration_total)

    transcription_segments = transcription.get("segments", [])

    # Build per-scene blocks
    blocks = []
    total_gemini_calls = 0
    needs_validation_count = 0

    for i, (t_start, t_end) in enumerate(scenes, start=1):
        block, calls = build_scene_block(
            i, t_start, t_end,
            transcription_segments, ui_data, gemini_data, frames_dir,
            duration_total, use_gemini
        )
        blocks.append(block)
        total_gemini_calls += calls
        needs_validation_count += block.count("[NEEDS VALIDATION]")

    # Header
    today = "2026-05-16"
    ref_name = input_dir.name
    source_video_display = source_video or "[NEEDS VALIDATION] (source MP4 path not provided)"
    pattern_display = pattern or "[NEEDS VALIDATION] (specify via --pattern)"
    score_display = score or "[NEEDS VALIDATION] (specify via --score)"

    header = f"""# Canonical scene-by-scene — {ref_name}

**Source video**: {source_video_display}
**Pattern**: {pattern_display} (per PAUTA-MASTER § 15)
**Score Gemini empirical**: {score_display}/10 (per PAUTA-MASTER § 0 table)
**Duration total**: {duration_total:.1f}s
**Total scenes (de-clustered)**: {len(scenes)}
**Last validated**: {today} by agent draft

> ⚠️ **DISCLAIMER**: Este doc es **ejemplo empírico canónico**, NO template rígido.
> Adaptá STRUCTURE (timing, transiciones, pattern flow) con TU historia/characters.
> NO copies línea por línea — un video que clona ref-XX con nombres cambiados es plagio, no creatividad.
> El formato es el generador, no el límite.
> Ver PAUTA-MASTER.md § 1 para filosofía.

---

## Resumen estadístico (post-build)

- **Raw cuts detected**: {len(raw_cuts)}
- **De-clustered boundaries**: {len(boundaries)}
- **Scenes generated**: {len(scenes)} (min duration {MIN_SCENE_DURATION_S}s)
- **Gemini Vision calls used**: {total_gemini_calls}
- **[NEEDS VALIDATION] flags**: {needs_validation_count} (user must resolve manually)

---

"""

    full_md = header + "\n".join(blocks)
    output_path.write_text(full_md)

    return {
        "output_path": str(output_path),
        "scenes_count": len(scenes),
        "needs_validation_count": needs_validation_count,
        "gemini_calls_used": total_gemini_calls,
        "duration_total_s": duration_total,
        "raw_cuts": len(raw_cuts),
        "boundaries_declustered": len(boundaries),
    }


# ─── CLI ────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="referent-analysis/ref-XX/ folder")
    ap.add_argument("--output", required=True, help="output directory (canonical-scenes/)")
    ap.add_argument("--filename", help="output filename (default: ref-XX.md from input dir name)")
    ap.add_argument("--pattern", help="Pattern P1-P10 (per PAUTA-MASTER § 15)")
    ap.add_argument("--score", help="Score Gemini empirical (X.XX)")
    ap.add_argument("--source-video", help="Path to source MP4")
    ap.add_argument("--use-gemini", action="store_true", help="Call Gemini Vision if gemini-frames-analysis.json missing")
    args = ap.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        print(f"ERROR: input dir not found: {input_dir}", file=sys.stderr)
        return 2

    filename = args.filename or f"{input_dir.name}.md"
    output_path = output_dir / filename

    print(f"Building canonical-scenes for {input_dir.name} → {output_path}")
    print(f"  use_gemini: {args.use_gemini}")

    stats = build_canonical_scenes(
        input_dir, output_path,
        pattern=args.pattern,
        score=args.score,
        source_video=args.source_video,
        use_gemini=args.use_gemini,
    )

    if "error" in stats:
        print(f"ERROR: {stats['error']}", file=sys.stderr)
        return 1

    print(f"  ✓ {stats['scenes_count']} scenes")
    print(f"  ⚠ {stats['needs_validation_count']} [NEEDS VALIDATION] flags")
    print(f"  💰 {stats['gemini_calls_used']} Gemini calls used")
    print(f"  📁 Output: {stats['output_path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
