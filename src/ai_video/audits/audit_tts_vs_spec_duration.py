#!/usr/bin/env python3
"""audit-tts-vs-spec-duration.py — BUILD 6 Sprint M L2 (PRE-4.J).

Post-CP2 gate: validate actual TTS mp3 duration (per shot in --tts-dir) matches
SPEC declared duration_intent_s within tolerance. Catches TTS overshoots BEFORE
they propagate to clip atomic mux + concat (where they cause sync drift).

For each shot with narrator_text:
  - Look for <tts-dir>/<shot_id>_narrator.mp3 (canonical naming forward).
  - ffprobe actual duration.
  - |actual - intent| > tolerance → FAIL.
  - File missing while narration expected → FAIL.

Shots without narrator_text → skipped (visual-only, no TTS expected).

Capability-aware: has_tts_narration false → not_applicable.
video_capabilities missing → Bug #9.

Build PRE-4.J BUILD 6 (2026-05-27) — TDD + Hard Rule #26 companion test.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

DEFAULT_TOLERANCE_S = 0.5
DEFAULT_NAMING = "{shot_id}_narrator.mp3"


def ffprobe_duration(path):
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT_S,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--tts-dir", default="assets/tts", help="Dir with per-shot TTS mp3s")
    parser.add_argument(
        "--naming-pattern", default=DEFAULT_NAMING, help='Filename pattern (default "{shot_id}_narrator.mp3")'
    )
    parser.add_argument("--tolerance-s", type=float, default=DEFAULT_TOLERANCE_S)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    caps = spec.get("video_capabilities")
    if caps is None:
        print(
            "ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
            file=sys.stderr,
        )
        return 2

    has_tts = bool(caps.get("has_tts_narration", False))
    tts_dir = Path(args.tts_dir)

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\ntts_dir: {tts_dir}\n"
            f"naming: {args.naming_pattern}\ntolerance: ±{args.tolerance_s}s\n"
            f"has_tts_narration: {has_tts}\n"
            f"branch: {'L2_tts_duration_check' if has_tts else 'not_applicable'}"
        )
        return 0

    if not has_tts:
        report = {
            "format": args.format,
            "overall_status": "not_applicable",
            "detail": "has_tts_narration=false → TTS duration check skipped",
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    shots = spec.get("shot_list") or []
    fails, ok = [], []
    for s in shots:
        text = ((s.get("narration_in_this_shot") or {}).get("narrator_text") or "").strip()
        if not text:
            continue  # no TTS expected
        shot_id = s.get("shot_id", "?")
        intent = s.get("duration_intent_s")
        try:
            intent = float(intent) if intent is not None else None
        except (TypeError, ValueError):
            intent = None
        mp3 = tts_dir / args.naming_pattern.format(shot_id=shot_id)
        if not mp3.exists():
            fails.append(
                {
                    "shot_id": shot_id,
                    "reason": "TTS file missing (narration expected)",
                    "expected_path": str(mp3),
                }
            )
            continue
        actual = ffprobe_duration(mp3)
        if actual is None:
            fails.append({"shot_id": shot_id, "reason": "ffprobe failed", "path": str(mp3)})
            continue
        entry = {
            "shot_id": shot_id,
            "actual_s": round(actual, 3),
            "intent_s": intent,
            "delta_s": round(actual - intent, 3) if intent else None,
            "tolerance_s": args.tolerance_s,
        }
        if intent is None:
            entry["reason"] = "duration_intent_s missing — cannot validate"
            fails.append(entry)
        elif abs(actual - intent) > args.tolerance_s:
            entry["reason"] = (
                f"TTS {actual:.2f}s vs intent {intent:.2f}s "
                f"|Δ|={abs(actual - intent):.2f}s > tolerance {args.tolerance_s}s"
            )
            fails.append(entry)
        else:
            ok.append(entry)

    overall = "fail" if fails else "pass"
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "tts_dir": str(tts_dir),
        "tolerance_s": args.tolerance_s,
        "overall_status": overall,
        "overall_pass": not fails,
        "fail_shots": fails,
        "ok_shots": ok,
        "total_checked": len(fails) + len(ok),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
