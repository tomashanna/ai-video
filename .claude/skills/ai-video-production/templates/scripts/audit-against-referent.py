#!/usr/bin/env python3
"""
audit-against-referent.py — Compare our video against F1 canonical n=10 referent profile.

Tolerance per metric: p25-p75 bands (interquartile range).

Critical metrics (failure relevant — must ≥85% in range to pass):
  - pace.wpm_total            (sweet spot ~153-180 wpm)
  - audio.lufs_integrated     (-14 ±0.5 Instagram target)
  - pacing.cuts_per_min       (2-7 horror-narrativo target)
  - pace.coverage_pct         (≥70% narration coverage)

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
from pathlib import Path
from statistics import quantiles


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


def compute_bands(referent_data, section, key, tolerance="p25-p75"):
    """Compute p25-p75 (or p5-p95) band from n=10 referent values."""
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
        ).strip()
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
        )
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
        )
        cuts = sum(1 for line in result.stderr.splitlines() if "pts_time:" in line)
        out["pacing"]["cuts_per_min"] = (cuts * 60.0) / out["duration_s"]
        out["pacing"]["cuts_total_raw"] = cuts
    except Exception as e:
        print(f"WARN: scene detection failed: {e}", file=sys.stderr)

    # Whisper pace + coverage (requires whisper + audio extract)
    try:
        import whisper
        # Extract audio
        audio_tmp = "/tmp/audit-referent-audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", video_path, "-vn", "-ac", "1", "-ar", "16000",
             audio_tmp, "-loglevel", "error"],
            check=True
        )
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
        if os.path.exists("/tmp/audit-referent-audio.wav"):
            y, sr = librosa.load("/tmp/audit-referent-audio.wav", sr=None)
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
                    default="../referent-analysis/horror-choice/F1-INGENIERO-MEASUREMENTS.json",
                    help="Path to F1 measurements JSON")
    ap.add_argument("--tolerance", choices=["p25-p75", "p5-p95"], default="p25-p75",
                    help="Tolerance per metric (default p25-p75 interquartile range)")
    args = ap.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        sys.exit(2)

    # Resolve measurements path (try relative to cwd, then to script dir)
    meas_path = args.measurements
    if not os.path.exists(meas_path):
        # Try relative to script's grandparent (i.e., project root)
        script_dir = Path(__file__).resolve().parent
        candidate = script_dir.parent.parent.parent.parent / "referent-analysis" / "F1-INGENIERO-MEASUREMENTS.json"
        if candidate.exists():
            meas_path = str(candidate)
        else:
            print(f"ERROR: measurements not found: {args.measurements}", file=sys.stderr)
            print(f"  Tried: {candidate}", file=sys.stderr)
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
        crit_total += 1
        ours_val = ours.get(section, {}).get(key)
        lo, hi, n = compute_bands(per_referent, section, key, tolerance=args.tolerance)
        if ours_val is None:
            status = "N/A"
            band_str = f"[{lo:.2f}, {hi:.2f}]" if lo is not None else "?"
            print(f"{label:<28} {'?':>10} {band_str:>20} {status:>8}")
            continue
        if lo is None or hi is None:
            status = "NO-REF"
            band_str = "n<4 referents"
            print(f"{label:<28} {ours_val:>10.2f} {band_str:>20} {status:>8}")
            continue
        in_band = lo <= ours_val <= hi
        status = "PASS ✓" if in_band else "FAIL ✗"
        if in_band:
            crit_in_band += 1
        band_str = f"[{lo:.2f}, {hi:.2f}]"
        print(f"{label:<28} {ours_val:>10.2f} {band_str:>20} {status:>8}")

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
