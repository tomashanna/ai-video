#!/usr/bin/env python3
"""audit-spec-narration-fits-duration.py — BUILD 5 Sprint M L1 (PRE-4.J).

Pre-emit SPEC gate: validate that each shot's narrator_text "FITS" in declared
duration_intent_s — i.e., implied WPM is physically achievable for TTS.

Different from BUILD 4 check_wpm (style — per-role canonical band):
  L1 = "physics fit": implied WPM ∈ [MIN, MAX] where MAX = TTS upper intelligibility
  (default 280) and MIN = pause-heavy lower (default 60). Per-shot.

Reports per-shot:
  - WPM > max_wpm → FAIL (narration too long for shot; TTS can't deliver intelligibly).
  - WPM < min_wpm → FLAG (suspiciously slow; verify intent).
  - else → PASS.

Plus advisory: for each shot, achievable_duration_at_target = words / target_wpm * 60.
Architect can adjust duration_intent_s or trim narration_text.

Capability-aware: has_tts_narration false → not_applicable. video_capabilities missing → Bug #9.
Agnostic-by-design: --format REQUIRED.

Build PRE-4.J BUILD 5 (2026-05-27) — TDD + Hard Rule #26 companion test.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

MAX_WPM_DEFAULT = 280.0   # TTS upper intelligibility ceiling
MIN_WPM_DEFAULT = 60.0    # pause-heavy lower
TARGET_WPM_DEFAULT = 165.0  # canonical narrator pace (F1 measured)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--max-wpm", type=float, default=MAX_WPM_DEFAULT)
    parser.add_argument("--min-wpm", type=float, default=MIN_WPM_DEFAULT)
    parser.add_argument("--target-wpm", type=float, default=TARGET_WPM_DEFAULT,
                        help="Target WPM for advisory achievable_duration (default canonical 165)")
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
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
              file=sys.stderr)
        return 2

    has_tts = bool(caps.get("has_tts_narration", False))
    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nhas_tts_narration: {has_tts}\n"
              f"branch: {'L1_wpm_fit_check' if has_tts else 'not_applicable'}\n"
              f"thresholds: min={args.min_wpm}, max={args.max_wpm}, target={args.target_wpm}")
        return 0

    if not has_tts:
        report = {
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_tts_narration=false → narration-fit check skipped (no TTS to fit)"
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    shots = spec.get("shot_list") or []
    fail_shots, flag_shots, ok_shots = [], [], []
    for s in shots:
        text = ((s.get("narration_in_this_shot") or {}).get("narrator_text") or "").strip()
        dur = s.get("duration_intent_s")
        if not text or not dur:
            continue
        try:
            dur = float(dur)
        except (TypeError, ValueError):
            continue
        if dur <= 0:
            continue
        words = len(text.split())
        wpm = words / dur * 60
        target_dur = round(words / args.target_wpm * 60, 2) if args.target_wpm > 0 else None
        entry = {
            "shot_id": s.get("shot_id", "?"), "words": words, "duration_s": dur,
            "wpm": round(wpm, 1), "achievable_duration_at_target": target_dur,
        }
        if wpm > args.max_wpm:
            entry["reason"] = f"WPM {wpm:.0f} > max {args.max_wpm} (narration too long for shot)"
            fail_shots.append(entry)
        elif wpm < args.min_wpm:
            entry["reason"] = f"WPM {wpm:.0f} < min {args.min_wpm} (suspiciously slow)"
            flag_shots.append(entry)
        else:
            ok_shots.append(entry)

    overall = "fail" if fail_shots else ("flag" if flag_shots else "pass")
    report = {
        "format": args.format, "spec": str(spec_path),
        "overall_status": overall, "overall_pass": overall == "pass",
        "max_wpm": args.max_wpm, "min_wpm": args.min_wpm, "target_wpm": args.target_wpm,
        "fail_shots": fail_shots, "flag_shots": flag_shots,
        "ok_count": len(ok_shots), "total_checked": len(fail_shots) + len(flag_shots) + len(ok_shots),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fail_shots else 1


if __name__ == "__main__":
    sys.exit(main())
