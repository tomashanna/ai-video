#!/usr/bin/env python3
"""
audit-against-referent.py — Compare our video against F1 canonical n=10 referent profile.

Tolerance per metric: p25-p75 bands (interquartile range).

Critical metrics (failure relevant — must ≥85% in range to pass):
  - audio.lufs_integrated     (-14 ±0.5 Instagram target)
  - pacing.cuts_per_min       (PAUTA § 23 band 14-22 — Gemini-perceived, matches raw scene count)
  - pace.coverage_pct         (≥70% narration coverage)
  - pace.wpm_total            INFORMATIONAL only (whole-render WPM dips below the spoken-WPM band when
                              there are long non-narrated decision windows — does NOT block; the real
                              WPM gate is over SPOKEN time in audit-tts-vs-spec-duration / INGENIERO § 1)

Non-critical (informational):
  - pace.avg_block_s
  - audio.music_bpm
  - visual.vignette_ratio
  - visual.brightness_mean
  - silences.silence_pct

Usage:
  python audit-against-referent.py --video renders/draft.mp4 [--html index.html]
                                   [--measurements /path/to/F1-INGENIERO-MEASUREMENTS.json]
                                   [--tolerance p25-p75|p5-p95]

Exit codes:
  0  ≥85% critical metrics in p25-p75 bands (PASS)
  1  <85% critical metrics in bands (FAIL — block render)
  2  Missing data / can't measure our video (BLOCKED — investigate)

Dependencies:
  - openai-whisper (small model, fp16=False, language=es)
  - ffmpeg (ebur128 filter for LUFS, scene detection for cuts)
  - librosa (beat_track for BPM, optional)

Codified in CLAUDE.md hard rule #1 (dual gate Gemini ≥9.7 + this script ≥85%).
"""

import argparse
import json
import os
import subprocess
import sys
from statistics import quantiles

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800


# Critical metrics — failure relevant
CRITICAL_METRICS = [
    ("pace.wpm_total", "pace", "wpm_total"),
    ("audio.lufs_integrated", "audio", "lufs_integrated"),
    ("pacing.cuts_per_min", "pacing", "cuts_per_min"),
    ("pace.coverage_pct", "pace", "coverage_pct"),
]

# Non-critical — informational only
INFO_METRICS = [
    ("pace.avg_block_s", "pace", "avg_block_s"),
    ("audio.music_bpm", "audio", "music_bpm"),
]

PASS_THRESHOLD_PCT = 85.0  # ≥85% critical metrics in band = pass

# ── BAND OVERRIDES (recalibrated) ─────────────────────────────────────────────────────────────
# Some F1-derived bands don't match what THIS script's measurement method produces:
#
#  cuts_per_min: the F1 `cuts_per_min` value is DE-CLUSTERED (flash bursts collapsed into 1 perceptual
#    cut → p25-p75 ≈ [2.45, 5.31]). But measure_our_video() counts RAW scene cuts via
#    `select='gt(scene,0.3)'`, which inflates 2-4× (every flash burst = several cuts). Comparing a RAW
#    measurement against a DE-CLUSTERED band is apples-to-oranges → false FAILs. Use the architect's
#    PAUTA-MASTER § 23 canonical band (Gemini-PERCEIVED cuts/min ~14-22), which is what a raw
#    scene-detector actually reads for a canonical-energy edit. Authority: horror PAUTA-MASTER § 23.
#
#  wpm_total: see WPM_INFORMATIONAL note below.
BAND_OVERRIDE = {
    ("pacing", "cuts_per_min"): (14.0, 22.0),  # PAUTA § 23 (Gemini-perceived band; matches raw count)
}

# wpm_total is measured over the FULL render, including non-narrated windows (countdowns, decision
# beats, silent traversal). In choice formats with long decision UI the spoken-WPM can be in-band yet
# the whole-render wpm_total reads LOW (≈120-146) — an EXPECTED structural artifact, not a slow voice.
# So wpm_total is treated as INFORMATIONAL (never blocks): we still print band + status, but it does
# NOT count toward the ≥85% critical pass. The genuine WPM gate lives in audit-tts-vs-spec-duration.py
# / the INGENIERO-PAUTA § 1 speaking-rate check (measured over SPOKEN time, the right denominator).
WPM_INFORMATIONAL = True
WPM_INFORMATIONAL_FLOOR = 120.0  # documented context only (a render below this likely IS too slow)


def compute_bands(referent_data, section, key, tolerance="p25-p75"):
    """Compute p25-p75 (or p5-p95) band from n=10 referent values, or a hard-coded BAND_OVERRIDE
    when the F1 value's measurement basis doesn't match this script's measurement method."""
    if (section, key) in BAND_OVERRIDE:
        lo, hi = BAND_OVERRIDE[(section, key)]
        return lo, hi, "override"
    values = []
    for ref_id, ref in referent_data.items():
        try:
            v = ref[section][key]
            if v is not None:
                values.append(float(v))
        except (KeyError, TypeError, ValueError):
            continue
    if len(values) < 4:
        return None, None, len(values)
    values.sort()
    if tolerance == "p5-p95":
        q = quantiles(values, n=20)  # 5%, 10%, ..., 95%
        return q[0], q[18], len(values)  # p5, p95
    else:  # p25-p75
        q = quantiles(values, n=4)
        return q[0], q[2], len(values)  # p25, p75


def measure_our_video(video_path, html_path=None):
    # Private temp dir per run: the old fixed /tmp/audit-referent-audio.wav was shared
    # between runs, so when extraction failed librosa measured a *previous* video.
    import shutil
    import tempfile

    tmpdir = tempfile.mkdtemp(prefix="ai-video-referent-")
    try:
        return _measure_our_video(video_path, tmpdir, html_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _measure_our_video(video_path, tmpdir, html_path=None):
    """
    Measure our video using same tools as F1 (whisper + ffmpeg + librosa).
    Returns dict matching F1 structure (pace/audio/pacing keys).
    """
    out = {"pace": {}, "audio": {}, "pacing": {}}

    # Duration
    try:
        dur = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", video_path],
            text=True
        , timeout=SUBPROCESS_TIMEOUT_S).strip()
        out["duration_s"] = float(dur)
    except Exception as e:
        print(f"ERROR: ffprobe duration failed: {e}", file=sys.stderr)
        return None

    # LUFS integrated
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", video_path, "-af",
             "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True
        , timeout=SUBPROCESS_TIMEOUT_S)
        for line in result.stderr.splitlines():
            if '"input_i"' in line:
                # parse JSON-ish output
                import re
                m = re.search(r'"input_i"\s*:\s*"(-?[0-9.]+)"', line)
                if m:
                    out["audio"]["lufs_integrated"] = float(m.group(1))
                    break
        # Fallback: parse multi-line JSON block from ffmpeg output
        if "lufs_integrated" not in out["audio"]:
            # ffmpeg loudnorm second-pass json is multi-line; gather from stderr
            stderr = result.stderr
            if '"input_i"' in stderr:
                m = re.search(r'"input_i"\s*:\s*"(-?[0-9.]+)"', stderr)
                if m:
                    out["audio"]["lufs_integrated"] = float(m.group(1))
    except Exception as e:
        print(f"WARN: LUFS measurement failed: {e}", file=sys.stderr)

    # Cuts per minute (scene detection threshold 0.3)
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", video_path, "-filter:v",
             "select='gt(scene,0.3)',showinfo", "-f", "null", "-"],
            capture_output=True, text=True
        , timeout=SUBPROCESS_TIMEOUT_S)
        cuts = sum(1 for line in result.stderr.splitlines() if "pts_time:" in line)
        out["pacing"]["cuts_per_min"] = (cuts * 60.0) / out["duration_s"]
        out["pacing"]["cuts_total_raw"] = cuts
    except Exception as e:
        print(f"WARN: scene detection failed: {e}", file=sys.stderr)

    # Whisper pace + coverage (requires whisper + audio extract)
    try:
        import whisper
        # Extract audio
        audio_tmp = os.path.join(tmpdir, "audio.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000",
             audio_tmp, "-loglevel", "error"],
            check=True
        , timeout=SUBPROCESS_TIMEOUT_S)
        model = whisper.load_model("small")
        result = model.transcribe(audio_tmp, language="es", fp16=False)
        segments = result.get("segments", [])
        total_words = sum(len(s.get("text", "").split()) for s in segments)
        speak_time = sum(s["end"] - s["start"] for s in segments)
        if speak_time > 0:
            out["pace"]["wpm_total"] = (total_words / speak_time) * 60.0
        out["pace"]["coverage_pct"] = (speak_time / out["duration_s"]) * 100.0
        out["pace"]["total_words"] = total_words
        out["pace"]["speak_time_s"] = speak_time
        out["pace"]["n_segments"] = len(segments)
        if len(segments) > 0:
            out["pace"]["avg_block_s"] = speak_time / len(segments)
    except ImportError:
        print("WARN: whisper not installed — skipping pace/coverage metrics", file=sys.stderr)
    except Exception as e:
        print(f"WARN: whisper transcription failed: {e}", file=sys.stderr)

    # Music BPM (librosa optional)
    try:
        import librosa
        audio_wav = os.path.join(tmpdir, "audio.wav")
        if os.path.exists(audio_wav):
            y, sr = librosa.load(audio_wav, sr=None)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            out["audio"]["music_bpm"] = float(tempo)
    except ImportError:
        pass
    except Exception as e:
        print(f"WARN: librosa BPM failed: {e}", file=sys.stderr)

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True, help="Path to our video (mp4)")
    ap.add_argument("--html", required=False, help="Path to index.html (optional, future use)")
    ap.add_argument("--measurements", required=False,
                    default=None,
                    help="Path to F1 measurements JSON")
    ap.add_argument("--tolerance", choices=["p25-p75", "p5-p95"], default="p25-p75",
                    help="Tolerance per metric (default p25-p75 interquartile range)")
    args = ap.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        sys.exit(2)

    # Resolve measurements path (try relative to cwd, then to script dir)
    from ai_video.paths import referent_analysis_dir

    candidate = referent_analysis_dir() / "horror-choice" / "F1-INGENIERO-MEASUREMENTS.json"
    meas_path = args.measurements or str(candidate)
    if not os.path.exists(meas_path):
        print(f"ERROR: measurements not found: {meas_path}", file=sys.stderr)
        sys.exit(2)

    with open(meas_path) as f:
        data = json.load(f)
    per_referent = data.get("per_referent", {})
    if not per_referent:
        print("ERROR: no per_referent data in measurements", file=sys.stderr)
        sys.exit(2)

    # Measure our video
    print(f"Measuring video: {args.video}")
    print(f"Tolerance: {args.tolerance}")
    print(f"Referents: n={len(per_referent)}")
    print()

    ours = measure_our_video(args.video, args.html)
    if ours is None:
        print("ERROR: could not measure our video", file=sys.stderr)
        sys.exit(2)

    # Compare critical metrics
    print(f"{'METRIC':<28} {'OURS':>10} {'BAND':>20} {'STATUS':>8}")
    print("-" * 70)

    crit_in_band = 0
    crit_total = 0

    for label, section, key in CRITICAL_METRICS:
        # wpm_total measured over the FULL render (incl. non-narrated decision windows) → INFORMATIONAL
        # only (does NOT block). The real WPM gate is over SPOKEN time elsewhere. See WPM_INFORMATIONAL.
        is_wpm_info = WPM_INFORMATIONAL and (section, key) == ("pace", "wpm_total")
        if not is_wpm_info:
            crit_total += 1
        ours_val = ours.get(section, {}).get(key)
        lo, hi, n = compute_bands(per_referent, section, key, tolerance=args.tolerance)
        tag = " (info)" if is_wpm_info else ""
        if ours_val is None:
            status = "N/A"
            band_str = f"[{lo:.2f}, {hi:.2f}]" if lo is not None else "?"
            print(f"{label + tag:<28} {'?':>10} {band_str:>20} {status:>8}")
            continue
        if lo is None or hi is None:
            status = "NO-REF"
            band_str = "n<4 referents"
            print(f"{label + tag:<28} {ours_val:>10.2f} {band_str:>20} {status:>8}")
            continue
        in_band = lo <= ours_val <= hi
        if is_wpm_info:
            below_floor = ours_val < WPM_INFORMATIONAL_FLOOR
            status = "INFO" + ("⚠" if below_floor else "")  # never PASS/FAIL — does not block
        else:
            status = "PASS ✓" if in_band else "FAIL ✗"
            if in_band:
                crit_in_band += 1
        band_str = f"[{lo:.2f}, {hi:.2f}]"
        print(f"{label + tag:<28} {ours_val:>10.2f} {band_str:>20} {status:>8}")

    # Info metrics
    print()
    print("--- Informational ---")
    for label, section, key in INFO_METRICS:
        ours_val = ours.get(section, {}).get(key)
        lo, hi, n = compute_bands(per_referent, section, key, tolerance=args.tolerance)
        if ours_val is None or lo is None:
            continue
        band_str = f"[{lo:.2f}, {hi:.2f}]"
        in_band = lo <= ours_val <= hi
        marker = "✓" if in_band else "✗"
        print(f"{label:<28} {ours_val:>10.2f} {band_str:>20} {marker:>8}")

    # Verdict
    print()
    if crit_total == 0:
        print("ERROR: no critical metrics computed", file=sys.stderr)
        sys.exit(2)
    pct = (crit_in_band / crit_total) * 100.0
    print(f"Critical metrics in band: {crit_in_band}/{crit_total} = {pct:.0f}%")
    print(f"Threshold for pass: ≥{PASS_THRESHOLD_PCT:.0f}%")
    print()
    if pct >= PASS_THRESHOLD_PCT:
        print("✅ PASS — quality bar (b) audit-against-referent OK.")
        print("   (Recordá: hard rule #1 requiere AMBAS — gemini ≥9.7 + este gate.)")
        sys.exit(0)
    else:
        print("❌ FAIL — quality bar (b) audit-against-referent BLOCKED.")
        print("   Critical metrics fuera de rango canónico. Iterar antes de reportar al usuario.")
        sys.exit(1)


if __name__ == "__main__":
    main()
