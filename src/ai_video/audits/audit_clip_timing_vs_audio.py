#!/usr/bin/env python3
"""audit-clip-timing-vs-audio.py — L4 output-side of the V5 truncation trilogy.

L1 (audit-spec-narration-fits-duration) = SPEC physics: canonical narration ≤ min(intent, i2v cap).
L2 (audit-tts-vs-spec-duration)         = TTS mp3 actual duration vs SPEC intent.
L4 (THIS)                               = the VISUAL CLIP / RENDER duration vs its AUDIO.

The V5 truncation bug had three escape hatches. L1/L2 cover the SPEC + TTS sides. L4 closes the
OUTPUT side: even if SPEC fit and TTS length are fine, the engineer can still trim the visual clip
shorter than the muxed narration (narration over a frozen/black frame), or the render amix
`duration=longest` can leave a video/audio stream tail mismatch. L4 measures the produced media.

Two modes:
  --mode clip   (per atomic clip, CP4): given a clip mp4 with a muxed narration audio stream,
                check visual_dur >= narration_dur AND visual_dur >= duration_intent_s - 0.1.
                (narration_dur measured from the audio stream of the clip, OR --narration-dur / a
                separate --narration-file.)
  --mode render (per final render, CP5): check |video_stream_dur - audio_stream_dur| <= av-tol
                (0.3s). Catches the amix duration=longest tail.

Rules (HR#28/#29 i2v cap read from MODEL-CAPABILITIES-MATRIX):
  - visual_dur >= narration_dur                       (else narration on frozen/black frame → FAIL)
  - visual_dur >= duration_intent_s - 0.1             (clip too short for its allocated beat → FAIL)
  - |video_stream_dur - audio_stream_dur| <= 0.3      (render amix tail → FAIL)
  - advisory FLAG: visual_dur > i2v_clip_cap + tol while produced from a single i2v tier clip
    (means a freeze-extend/tpad or longer tier was needed — verify it actually happened).

Capability-gate (Pattern 7): --format REQUIRED. If has_ai_generated_clips (clip mode) or
has_tts_narration (render mode A/V check is still meaningful, but the narration-vs-visual rule is
TTS-gated) is false → exit 0 verdict 'not_applicable' (NO fail).

Exit codes: 0 = PASS / not_applicable · 1 = FAIL (a rule above is violated) · 2 = can't-measure /
wrong-architecture (ffprobe failed, no audio stream where narration expected, SPEC missing caps).

⛔ DESIGN: ALL logic lives in PURE functions (evaluate_clip_timing / evaluate_av_sync) that receive
already-extracted durations. The runtime wrapper (ffprobe_stream_duration) is thin and is what tests
mock — no real media needed.

Authority: HR#25 (HYBRID per-clip atomic) + HR#28/#29 (MODEL-CAPABILITIES-MATRIX) + GAP V5 truncation
trilogy (L1/L2/L4). TDD + Hard Rule #26 companion test (test_audit-clip-timing-vs-audio.py).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from ai_video.paths import model_capabilities_matrix

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

try:
    import yaml
except ImportError:
    yaml = None  # SPEC is optional in clip mode (intent can be passed via --intent-dur)

# MODEL-CAPABILITIES-MATRIX fallbacks (HR#29 — real source of truth is the MATRIX file).
I2V_CLIP_MAX_S_DEFAULT = 5.9          # MATRIX hailuo_std.clip_duration_max_s
DEFAULT_INTENT_FLOOR_TOL_S = 0.1      # visual_dur >= intent - 0.1
DEFAULT_AV_TOL_S = 0.3                # |video - audio| <= 0.3 (amix duration=longest tail)


# ─────────────────────────────────── MATRIX read (HR#29) ───────────────────────────────────
def load_i2v_caps(matrix_path):
    """Read per-model clip_duration_max_s from MODEL-CAPABILITIES-MATRIX.md via line-scan (no
    yaml-in-md fragility); fall back to defaults. Roles consult the matrix, NO hardcoded model
    assumptions (anti-pattern #18 / HR#29). Returns {model_name: clip_max_s}."""
    import re
    caps = {"hailuo_std": I2V_CLIP_MAX_S_DEFAULT, "hailuo_pro": 10.0}  # fallback
    try:
        cur = None
        for raw in Path(matrix_path).read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].rstrip()  # drop trailing comments (keys carry "# forward ...")
            # top-level model key inside a yaml fence: non-indented `name:` with no inline value.
            mk = re.match(r"^([a-z0-9_]+):\s*$", line)
            if mk:
                cur = mk.group(1)
            mc = re.search(r"clip_duration_max_s:\s*([0-9.]+)", line)
            if mc and cur:
                caps[cur] = float(mc.group(1))
    except Exception:
        pass
    return caps


# ─────────────────────────────────── PURE LOGIC (testable) ───────────────────────────────────
def evaluate_clip_timing(visual_dur, narration_dur, intent_dur, av_len_diff_s,
                         *, i2v_clip_cap=None, intent_floor_tol=DEFAULT_INTENT_FLOOR_TOL_S,
                         av_tol=DEFAULT_AV_TOL_S):
    """PURE: decide whether a produced atomic clip's timing is sound.

    Args (all already extracted — NO media access here):
      visual_dur      : video-stream duration of the clip (s) or None.
      narration_dur   : muxed/expected narration duration (s) or None (no narration → rule skipped).
      intent_dur      : SPEC duration_intent_s (s) or None (no intent → rule skipped).
      av_len_diff_s   : |video_stream - audio_stream| of the clip (s) or None (skip av rule).
      i2v_clip_cap    : single-i2v-clip ceiling for this tier (s) → advisory FLAG only.

    Returns (ok: bool, reasons: list[str]). reasons carry "FAIL:"/"FLAG:" prefixes.
    ok is False only on a FAIL; a FLAG alone leaves ok True (advisory).
    """
    fails, flags = [], []

    if visual_dur is None:
        return False, ["FAIL: visual (video-stream) duration could not be measured"]

    # Rule 1 — visual must cover the narration (else narration on frozen/black frame).
    if narration_dur is not None:
        if visual_dur + 1e-6 < narration_dur:
            fails.append(
                f"FAIL: visual {visual_dur:.2f}s < narration {narration_dur:.2f}s "
                f"→ narration plays over a frozen/black frame (Δ {narration_dur - visual_dur:.2f}s)")

    # Rule 2 — visual must reach (almost) its allocated beat duration.
    if intent_dur is not None:
        if visual_dur + 1e-6 < intent_dur - intent_floor_tol:
            fails.append(
                f"FAIL: visual {visual_dur:.2f}s < duration_intent_s {intent_dur:.2f}s - "
                f"{intent_floor_tol:.2f}s tol (clip too short for its beat)")

    # Rule 3 — internal A/V streams of the clip must line up.
    if av_len_diff_s is not None:
        if av_len_diff_s > av_tol + 1e-6:
            fails.append(
                f"FAIL: |video - audio| = {av_len_diff_s:.2f}s > {av_tol:.2f}s tol "
                f"(stream tail mismatch — amix duration=longest)")

    # Advisory — visual longer than ONE i2v clip of this tier ⇒ a freeze-extend/longer tier was used.
    if i2v_clip_cap is not None and visual_dur > i2v_clip_cap + 0.25:
        flags.append(
            f"FLAG: visual {visual_dur:.2f}s > i2v single-clip cap {i2v_clip_cap:.2f}s "
            f"→ verify a freeze-extend/longer-tier produced this (not a duplicated/looped artifact)")

    return (len(fails) == 0), (fails + flags)


def evaluate_av_sync(video_dur, audio_dur, *, av_tol=DEFAULT_AV_TOL_S):
    """PURE: final-render video-stream vs audio-stream duration mismatch (amix tail).
    Returns (ok, reasons)."""
    if video_dur is None or audio_dur is None:
        return False, ["FAIL: could not measure both video and audio stream durations"]
    diff = abs(video_dur - audio_dur)
    if diff > av_tol + 1e-6:
        return False, [
            f"FAIL: |video {video_dur:.2f}s - audio {audio_dur:.2f}s| = {diff:.2f}s > "
            f"{av_tol:.2f}s tol (amix duration=longest left a tail)"]
    return True, [f"video {video_dur:.2f}s / audio {audio_dur:.2f}s within {av_tol:.2f}s tol"]


# ─────────────────────────────────── THIN RUNTIME (mocked in tests) ───────────────────────────
def ffprobe_stream_duration(path, stream):
    """Thin runtime: ffprobe a single stream's duration. stream ∈ {'v','a'}. Returns float|None.
    Falls back to format=duration if the stream lacks a per-stream duration tag."""
    sel = "v:0" if stream == "v" else "a:0"
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", sel,
         "-show_entries", "stream=duration", "-of",
         "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    val = (r.stdout or "").strip().splitlines()
    for line in val:
        try:
            d = float(line)
            if d > 0:
                return d
        except ValueError:
            continue
    # fallback: container duration
    r2 = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    try:
        d = float((r2.stdout or "").strip())
        return d if d > 0 else None
    except ValueError:
        return None


def _load_intent_from_spec(spec_path, shot_id):
    """Best-effort: read duration_intent_s for shot_id from the SPEC. Returns float|None.
    Also returns the per-shot i2v tier if declared (model_tier_override)."""
    if yaml is None or not spec_path:
        return None, None, None
    p = Path(spec_path)
    if not p.exists():
        return None, None, "missing"
    try:
        spec = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return None, None, "unparseable"
    caps = (spec or {}).get("video_capabilities")
    for s in (spec or {}).get("shot_list") or []:
        if str(s.get("shot_id")) == str(shot_id):
            try:
                intent = float(s.get("duration_intent_s"))
            except (TypeError, ValueError):
                intent = None
            return intent, s.get("model_tier_override"), caps
    return None, None, caps


# ─────────────────────────────────── CLI ───────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--mode", choices=["clip", "render"], required=True)
    parser.add_argument("--video", required=True, help="clip mp4 (clip mode) or final render (render mode)")
    parser.add_argument("--spec", default=None, help="SPEC yaml (clip mode: pulls duration_intent_s)")
    parser.add_argument("--shot-id", default=None, help="clip mode: shot_id to look up in SPEC")
    parser.add_argument("--intent-dur", type=float, default=None,
                        help="clip mode: override duration_intent_s (else from SPEC via --shot-id)")
    parser.add_argument("--narration-dur", type=float, default=None,
                        help="clip mode: narration duration override (else measured from clip audio stream)")
    parser.add_argument("--i2v-tier", default="hailuo_std", help="clip mode: i2v tier for the advisory cap")
    parser.add_argument("--av-tol", type=float, default=DEFAULT_AV_TOL_S)
    parser.add_argument("--intent-floor-tol", type=float, default=DEFAULT_INTENT_FLOOR_TOL_S)
    parser.add_argument("--matrix", default=None, help="path to MODEL-CAPABILITIES-MATRIX.md")
    # capability overrides (so render-mode A/V check works even without a SPEC on disk)
    parser.add_argument("--has-ai-generated-clips", choices=["true", "false"], default=None)
    parser.add_argument("--has-tts-narration", choices=["true", "false"], default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    matrix_path = args.matrix or (
        model_capabilities_matrix())
    i2v_caps = load_i2v_caps(matrix_path)
    clip_cap = i2v_caps.get(args.i2v_tier, I2V_CLIP_MAX_S_DEFAULT)

    # Resolve capabilities: explicit flags > SPEC video_capabilities block.
    spec_caps = None
    intent = args.intent_dur
    if args.spec and (args.shot_id or args.mode == "clip"):
        intent_from_spec, tier_from_spec, spec_caps = _load_intent_from_spec(args.spec, args.shot_id)
        if intent is None:
            intent = intent_from_spec
        if args.i2v_tier == "hailuo_std" and tier_from_spec:
            clip_cap = i2v_caps.get(tier_from_spec, clip_cap)

    def cap(name, flag):
        if flag is not None:
            return flag == "true"
        if isinstance(spec_caps, dict):
            return bool(spec_caps.get(name, False))
        return None  # unknown

    has_ai = cap("has_ai_generated_clips", args.has_ai_generated_clips)
    has_tts = cap("has_tts_narration", args.has_tts_narration)

    if args.dry_run:
        print(f"format: {args.format}\nmode: {args.mode}\nvideo: {args.video}\n"
              f"i2v_tier: {args.i2v_tier} clip_cap: {clip_cap}\nmatrix: {matrix_path}\n"
              f"has_ai_generated_clips: {has_ai}\nhas_tts_narration: {has_tts}\n"
              f"intent_dur: {intent}\nav_tol: {args.av_tol}")
        return 0

    # ── Capability gate (Pattern 7) ──
    # clip mode is the per-clip atomic check → gated on has_ai_generated_clips (default-apply if unknown
    # but a SPEC said nothing → treat unknown as applicable to avoid silent skips).
    if args.mode == "clip" and has_ai is False:
        print(json.dumps({"format": args.format, "mode": args.mode,
                          "overall_status": "not_applicable",
                          "detail": "has_ai_generated_clips=false → no atomic clip timing to check"},
                         indent=2, ensure_ascii=False))
        return 0

    vpath = Path(args.video)
    if not vpath.exists():
        print(f"ERROR: video not found: {vpath}", file=sys.stderr)
        return 2

    video_dur = ffprobe_stream_duration(vpath, "v")
    audio_dur = ffprobe_stream_duration(vpath, "a")

    if args.mode == "render":
        # render A/V sync. If no audio stream at all → can't measure (wrong architecture).
        if audio_dur is None:
            print(json.dumps({"format": args.format, "mode": args.mode,
                              "overall_status": "cannot_measure",
                              "detail": "render has no measurable audio stream"},
                             indent=2, ensure_ascii=False), )
            return 2
        ok, reasons = evaluate_av_sync(video_dur, audio_dur, av_tol=args.av_tol)
        report = {
            "format": args.format, "mode": args.mode, "video": str(vpath),
            "video_stream_dur_s": round(video_dur, 3) if video_dur is not None else None,
            "audio_stream_dur_s": round(audio_dur, 3) if audio_dur is not None else None,
            "av_tol_s": args.av_tol,
            "overall_status": "pass" if ok else "fail", "overall_pass": ok,
            "reasons": reasons,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if ok else 1

    # ── clip mode ──
    # narration duration: override > measured from the clip's audio stream.
    narration_dur = args.narration_dur if args.narration_dur is not None else audio_dur
    # The narration-vs-visual rule only bites when there's actually a narration to cover.
    if has_tts is False:
        narration_dur = None
    if narration_dur is None and has_tts is not False:
        # Audio expected (has_tts true/unknown) but no audio stream measurable → cannot validate rule 1.
        # Still run intent + (no) av rule, but flag the measurement gap as cannot_measure if intent also
        # absent (nothing left to check meaningfully).
        if intent is None:
            print(json.dumps({"format": args.format, "mode": args.mode,
                              "overall_status": "cannot_measure",
                              "detail": "no narration audio stream AND no duration_intent_s — nothing to check"},
                             indent=2, ensure_ascii=False))
            return 2

    av_len_diff = (abs(video_dur - audio_dur)
                   if (video_dur is not None and audio_dur is not None) else None)

    ok, reasons = evaluate_clip_timing(
        video_dur, narration_dur, intent, av_len_diff,
        i2v_clip_cap=clip_cap, intent_floor_tol=args.intent_floor_tol, av_tol=args.av_tol)

    report = {
        "format": args.format, "mode": args.mode, "video": str(vpath),
        "shot_id": args.shot_id,
        "visual_dur_s": round(video_dur, 3) if video_dur is not None else None,
        "narration_dur_s": round(narration_dur, 3) if narration_dur is not None else None,
        "duration_intent_s": intent,
        "av_len_diff_s": round(av_len_diff, 3) if av_len_diff is not None else None,
        "i2v_tier": args.i2v_tier, "i2v_clip_cap_s": clip_cap, "matrix": str(matrix_path),
        "overall_status": "pass" if ok else "fail", "overall_pass": ok,
        "reasons": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
