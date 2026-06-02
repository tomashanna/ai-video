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

MAX_WPM_DEFAULT = 280.0   # TTS upper intelligibility ceiling (physical, "if compressed")
MIN_WPM_DEFAULT = 60.0    # pause-heavy lower
TARGET_WPM_DEFAULT = 165.0  # canonical narrator pace (F1 measured)
# MODEL-CAPABILITIES-MATRIX defaults (HR#29 — the real source of truth is the MATRIX file;
# these are fallbacks). V5 bug: narration at canonical pace exceeded min(duration_intent_s, i2v clip
# max) → truncated. The fit check below uses CANONICAL pace + i2v clip cap, NOT the 280 ceiling.
CANONICAL_PACE_WPM_DEFAULT = 165.0   # MATRIX elevenlabs.canonical_pace_wpm
I2V_CLIP_MAX_S_DEFAULT = 5.9         # MATRIX hailuo_std.clip_duration_max_s


def load_matrix_values(matrix_path):
    """Read canonical_pace_wpm + per-model clip_duration_max_s from MODEL-CAPABILITIES-MATRIX.md via
    line-scan (no yaml-in-md fragility); fall back to defaults. HR#29 / anti-pattern #18: roles consult
    the matrix, NO hardcoded model assumptions. Returns (wpm, caps_dict {model_name: clip_max_s})."""
    import re
    wpm = CANONICAL_PACE_WPM_DEFAULT
    caps = {"hailuo_std": I2V_CLIP_MAX_S_DEFAULT, "hailuo_pro": 10.0}  # fallback
    try:
        cur = None
        for raw in Path(matrix_path).read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].rstrip()  # drop inline/trailing comments (keys carry "# forward ...")
            mw = re.search(r"canonical_pace_wpm:\s*([0-9.]+)", line)
            if mw:
                wpm = float(mw.group(1))
            mk = re.match(r"^([a-z0-9_]+):\s*$", line)  # top-level model key inside a yaml fence
            if mk:
                cur = mk.group(1)
            mc = re.search(r"clip_duration_max_s:\s*([0-9.]+)", line)
            if mc and cur:
                caps[cur] = float(mc.group(1))
    except Exception:
        pass
    return wpm, caps


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--max-wpm", type=float, default=MAX_WPM_DEFAULT)
    parser.add_argument("--min-wpm", type=float, default=MIN_WPM_DEFAULT)
    parser.add_argument("--target-wpm", type=float, default=TARGET_WPM_DEFAULT,
                        help="Target WPM for advisory achievable_duration (default canonical 165)")
    parser.add_argument("--canonical-wpm", type=float, default=None, help="override canonical pace (default: from MATRIX)")
    parser.add_argument("--i2v-clip-max-s", type=float, default=None, help="override i2v clip max seconds (default: from MATRIX)")
    parser.add_argument("--matrix", default=None, help="path to MODEL-CAPABILITIES-MATRIX.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    matrix_path = args.matrix or (Path(__file__).resolve().parent.parent.parent / "MODEL-CAPABILITIES-MATRIX.md")
    m_wpm, m_caps = load_matrix_values(matrix_path)
    canonical_wpm = args.canonical_wpm or m_wpm
    default_i2v_max = args.i2v_clip_max_s or m_caps.get("hailuo_std", I2V_CLIP_MAX_S_DEFAULT)

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
        # v11 canonical: narration_in_this_shot is a STRING; synthetic fixtures: dict {narrator_text}.
        _n = s.get("narration_in_this_shot")
        text = (_n if isinstance(_n, str) else ((_n or {}).get("narrator_text") or "")).strip()
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
        canonical_dur = words / canonical_wpm * 60          # actual TTS duration at canonical pace
        tier = s.get("model_tier_override") or "hailuo_std"  # per-shot i2v tier (MATRIX, anti-pattern #18)
        clip_cap = m_caps.get(tier, default_i2v_max)
        target_dur = round(words / args.target_wpm * 60, 2) if args.target_wpm > 0 else None
        entry = {
            "shot_id": s.get("shot_id", "?"), "words": words, "duration_s": dur,
            "wpm": round(wpm, 1), "canonical_dur_s": round(canonical_dur, 2),
            "i2v_tier": tier, "i2v_clip_cap_s": clip_cap, "achievable_duration_at_target": target_dur,
        }
        # PRIMARY truncation test (V5 bug class): narration must fit the shot's ALLOCATED duration.
        # If canonical_dur > duration_intent_s → atomic trim WILL truncate it. This is the real bug.
        if canonical_dur > dur + 0.25:
            entry["reason"] = (f"narration {canonical_dur:.1f}s @canonical {canonical_wpm:.0f}WPM > "
                               f"duration_intent_s {dur:.1f}s → would be TRUNCATED (V5 bug class)")
            fail_shots.append(entry)
        # SECONDARY (flag, not fail): narration fits duration_intent_s but exceeds ONE i2v clip of this
        # tier → engineer MUST freeze-extend (tpad) or use a longer tier. Valid if handled (e.g. shot_02).
        elif canonical_dur > clip_cap + 0.25:
            entry["reason"] = (f"narration {canonical_dur:.1f}s > i2v clip cap {clip_cap:.1f}s ({tier}) → "
                               f"requires freeze-extend/longer-tier to reach duration_intent_s {dur:.1f}s (verify engineer)")
            flag_shots.append(entry)
        elif wpm > args.max_wpm:
            entry["reason"] = f"WPM {wpm:.0f} > max {args.max_wpm} (physically undeliverable even compressed)"
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
        "canonical_wpm": canonical_wpm, "i2v_clip_max_s_default": default_i2v_max, "matrix": str(matrix_path),
        "fail_shots": fail_shots, "flag_shots": flag_shots,
        "ok_count": len(ok_shots), "total_checked": len(fail_shots) + len(flag_shots) + len(ok_shots),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fail_shots else 1


if __name__ == "__main__":
    sys.exit(main())
