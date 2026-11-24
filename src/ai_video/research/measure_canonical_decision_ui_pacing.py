#!/usr/bin/env python3
"""
measure-canonical-decision-ui-pacing.py — Phase 1 priority script.

Empirically measure canonical decision UI pacing across 8 source videos.
Flips canonical_validation_status pending_video_measurement → validated.

Inputs:
- referent-analysis/ref-XX/transcription.json (Whisper segments with timestamps)
- referent-analysis/ref-XX/scene_cuts.txt
- videosref_elige_tu_compa/*.MP4 (source videos)

Outputs:
- referent-analysis/empirical-decision-ui-pacing/ref-XX-measurements.json (per ref)
- referent-analysis/empirical-decision-ui-pacing/aggregate-canonical-bands.json (cross-ref)

Methodology:
1. Per-segment WPM categorization by role (GAP #21)
2. Decision window detection (transcription text patterns)
3. Countdown digit OCR + transition timing (EasyOCR on 0.1s frames)
4. Pause beat (narration_end → countdown_start)
5. SSIM freeze detection
6. Librosa ambient duck (RMS pre/during)
7. Aggregate cross-canonical bands median + p25/p75
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from statistics import median

try:
    import numpy as np
except ImportError:
    # numpy is required for actual measurement runs but NOT for --dry-run / argparse.
    # Test environment without numpy can still validate CLI flag handling.
    np = None

from ai_video.paths import referent_analysis_dir, repo_root

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

PROJECT_ROOT = repo_root()
REF_DIR = referent_analysis_dir()

# Module-level paths populated by main() per --format flag.
# Sub-Fase 3A.2 TIER 2.1 (2026-05-25): hardcoded → CLI configurable (Capa A agnostic).
SOURCES_DIR = None
OUT_DIR = None


def resolve_format_paths(format_name, sources_override=None, out_override=None, ref_dir_override=None):
    """Resolve format-aware default paths or honor explicit overrides.

    horror-choice: namespaced post-TIER 2.3 (2026-05-25) — F1 + ref-XX moved to referent-analysis/horror-choice/
    arbitrary X:   <X>-refs/ + referent-analysis/<X>/empirical-decision-ui-pacing/
    """
    if format_name == "horror-choice":
        defaults = {
            "sources_dir": PROJECT_ROOT / "videosref_elige_tu_compa",
            "out_dir": REF_DIR / "horror-choice" / "empirical-decision-ui-pacing",
            "ref_dir": REF_DIR / "horror-choice",
        }
    else:
        defaults = {
            "sources_dir": PROJECT_ROOT / f"{format_name}-refs",
            "out_dir": REF_DIR / format_name / "empirical-decision-ui-pacing",
            "ref_dir": REF_DIR / format_name,
        }
    return {
        "sources_dir": Path(sources_override) if sources_override else defaults["sources_dir"],
        "out_dir": Path(out_override) if out_override else defaults["out_dir"],
        "ref_dir": Path(ref_dir_override) if ref_dir_override else defaults["ref_dir"],
    }

# Map ref-XX → source MP4 basename (from spec)
REF_TO_SOURCE = {
    "ref-03": "ScreenRecording_05-13-2026 00-01-36_1.MP4",
    "ref-06": "ScreenRecording_05-13-2026 00-07-06_1.MP4",
    "ref-08": "ScreenRecording_05-13-2026 11-05-30_1.MP4",
    "ref-09": "ScreenRecording_05-13-2026 11-07-19_1.MP4",
    "ref-10": "ScreenRecording_05-13-2026 11-09-44_1.MP4",
    "ref-11": "ScreenRecording_05-13-2026 11-13-25_1.MP4",
    "ref-12": "ScreenRecording_05-13-2026 11-22-41_1.MP4",
    "ref-13": "ScreenRecording_05-13-2026 11-25-03_1.MP4",
}

# Decision window detection patterns
DECISION_PATTERNS = [
    r"\bahora decides?\b",
    r"\bdecid[íi]s?\b",
    r"\b(?:te (?:incomoda|gusta|asusta|quieres|conviene)|prefieres)\b",
    r"\bo (?:puedes|prefier|sabe[ns]?|te|ya)\b",
    r"\bsi escogiste\b",
    r"\bsi (?:eliges|miras|seguís|salís|esper)",
]

# Per-segment role classifier (heuristic patterns)
ROLE_PATTERNS = {
    "hook_framing": [r"\b(?:escoge|elige|decid[íi]).*\bcompañer", r"\b(matarife|cocinera|ó o)\b"],
    "setup_establishing": [r"\bplanta el", r"\b(turno|cámara|gancho|despiese)", r"\bsi (?:elegiste|escogiste)\b"],
    "decision_setup": [r"\b(empieza a|empieza|aparece|se voltea|se acerca|empezás)\b"],
    "decision_question": [r"\bdecid[íi]s?\b", r"\bahora decides?\b", r"\b(?:miras|mirás|salís|seguís|te incomoda|prefieres)\b\?"],
    "consequence_narration": [r"\bsi (?:miras|mirás|seguís|salís|esper|te quieres|sabes|te incomoda)", r"\b(?:envía|enoja|sonríe|deja de|empieza a|abre la)\b"],
    "cliffhanger": [r"\b(?:nunca|sirena|seis|saliste|vive tu|aprendiste|loop|eterno|para siempre|baila)\b"],
    "climax_staccato": [r"^\s*(?:la (?:olla|sirena)|cena|nunca|fin|ya)\b"],
}


def classify_segment(text):
    """Heuristic role classifier per segment text."""
    text_lower = text.lower().strip()
    for role, patterns in ROLE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, text_lower):
                return role
    return "unclassified"


def find_decision_windows(segments):
    """Find decision narration windows from transcription segments.
    Returns list of {narration_end_s, expected_countdown_start_s, segment_idx}.
    """
    windows = []
    for i, seg in enumerate(segments):
        text_lower = seg["text"].lower().strip()
        for pat in DECISION_PATTERNS:
            if re.search(pat, text_lower):
                windows.append({
                    "segment_idx": i,
                    "segment_text": seg["text"].strip(),
                    "narration_start_s": seg["start"],
                    "narration_end_s": seg["end"],
                    "expected_window_start_s": seg["end"],
                    "expected_window_end_s": min(seg["end"] + 5.0, segments[-1]["end"]),
                })
                break
    return windows


def measure_per_segment_wpm(segments):
    """GAP #21 — per-segment WPM categorized by role."""
    per_role = {}
    for seg in segments:
        text = seg["text"].strip()
        dur = seg["end"] - seg["start"]
        if dur < 0.3:  # skip ultra-short
            continue
        words = len(text.split())
        if words == 0:
            continue
        wpm = words / dur * 60.0
        role = classify_segment(text)
        per_role.setdefault(role, []).append({
            "text": text[:60],
            "duration_s": round(dur, 2),
            "words": words,
            "wpm": round(wpm, 1),
        })
    # Aggregate per role
    agg = {}
    for role, items in per_role.items():
        wpms = [x["wpm"] for x in items]
        agg[role] = {
            "n_samples": len(items),
            "median_wpm": round(median(wpms), 1),
            "p25_wpm": round(float(np.percentile(wpms, 25)), 1),
            "p75_wpm": round(float(np.percentile(wpms, 75)), 1),
            "min_wpm": round(min(wpms), 1),
            "max_wpm": round(max(wpms), 1),
            "samples": items[:3],  # first 3 examples
        }
    return agg


def extract_frames_dense(mp4_path, start_s, end_s, interval_s=0.1, out_dir=None):
    """Extract frames at interval_s granularity in [start, end] window."""
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True, parents=True)
    duration = end_s - start_s
    # ffmpeg fps filter for dense extraction
    fps = 1.0 / interval_s
    pattern = str(out_dir / "frame_%04d.jpg")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", str(start_s),
        "-i", str(mp4_path),
        "-t", str(duration),
        "-vf", f"fps={fps},scale=540:960",  # downscale for OCR speed
        "-q:v", "3",
        "-pix_fmt", "yuvj420p",
        pattern,
    ], check=True, timeout=SUBPROCESS_TIMEOUT_S)
    return sorted(out_dir.glob("frame_*.jpg"))


def detect_countdown_digits(frame_paths, easyocr_reader, start_s, interval_s):
    """OCR each frame for digit '3','2','1','0' detection in center region.
    Returns transitions: list of {t, digit}.
    """
    transitions = []
    last_digit = None
    for i, fp in enumerate(frame_paths):
        t = start_s + i * interval_s
        import cv2
        img = cv2.imread(str(fp))
        if img is None:
            continue
        # Crop center region (where countdown typically is)
        h, w = img.shape[:2]
        cy_lo, cy_hi = int(h * 0.35), int(h * 0.65)
        cx_lo, cx_hi = int(w * 0.30), int(w * 0.70)
        center = img[cy_lo:cy_hi, cx_lo:cx_hi]
        # EasyOCR
        try:
            results = easyocr_reader.readtext(center, allowlist="0123456789")
        except Exception:
            results = []
        digit = None
        for res in results:
            bbox, text, conf = res
            text = text.strip()
            if conf > 0.4 and text in {"3", "2", "1", "0"}:
                digit = text
                break
        if digit and digit != last_digit:
            transitions.append({"t": round(t, 2), "digit": digit})
            last_digit = digit
    return transitions


def detect_freeze_via_ssim(frame_paths, start_s, interval_s, ssim_threshold=0.96):
    """SSIM consecutive frames. If >threshold for >2s consecutive → freeze."""
    from skimage.metrics import structural_similarity as ssim
    import cv2
    if len(frame_paths) < 2:
        return {"freeze_detected": False, "duration_s": 0.0}
    ssims = []
    prev_gray = None
    for fp in frame_paths:
        img = cv2.imread(str(fp), cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        if prev_gray is not None and prev_gray.shape == img.shape:
            s = ssim(prev_gray, img)
            ssims.append(s)
        prev_gray = img
    # Find longest run > threshold
    longest_run = 0
    cur_run = 0
    for s in ssims:
        if s > ssim_threshold:
            cur_run += 1
            longest_run = max(longest_run, cur_run)
        else:
            cur_run = 0
    duration_s = longest_run * interval_s
    return {
        "freeze_detected": duration_s >= 2.0,
        "duration_s": round(duration_s, 2),
        "mean_ssim": round(float(np.mean(ssims)) if ssims else 0.0, 3),
    }


def measure_ambient_duck(mp4_path, decision_window):
    """Librosa RMS pre vs during decision window."""
    import librosa
    pre_start = max(0.0, decision_window["narration_start_s"] - 2.0)
    pre_end = decision_window["narration_start_s"]
    dur_start = decision_window["expected_window_start_s"]
    dur_end = decision_window["expected_window_end_s"]
    try:
        y, sr = librosa.load(str(mp4_path), sr=22050, offset=pre_start, duration=pre_end - pre_start)
        rms_pre = float(np.mean(librosa.feature.rms(y=y)))
        y2, sr2 = librosa.load(str(mp4_path), sr=22050, offset=dur_start, duration=dur_end - dur_start)
        rms_dur = float(np.mean(librosa.feature.rms(y=y2)))
        if rms_pre <= 0:
            return {"duck_db": None, "rms_pre": rms_pre, "rms_during": rms_dur}
        duck_db = 20.0 * np.log10(rms_dur / rms_pre)
        return {
            "duck_db": round(float(duck_db), 2),
            "rms_pre": round(rms_pre, 5),
            "rms_during": round(rms_dur, 5),
        }
    except Exception as e:
        return {"duck_db": None, "error": str(e)}


def measure_ref(ref_id, easyocr_reader):
    print(f"\n=== {ref_id} ===")
    ref_path = REF_DIR / ref_id
    source_mp4 = SOURCES_DIR / REF_TO_SOURCE[ref_id]
    if not source_mp4.exists():
        print(f"  ❌ Source MP4 not found: {source_mp4}")
        return None
    trans_path = ref_path / "transcription.json"
    if not trans_path.exists():
        print(f"  ❌ Transcription not found: {trans_path}")
        return None

    transcription = json.loads(trans_path.read_text())
    segments = transcription["segments"]
    print(f"  segments: {len(segments)}")

    # 1. Per-segment WPM bands (GAP #21)
    wpm_bands = measure_per_segment_wpm(segments)
    print(f"  WPM roles: {list(wpm_bands.keys())}")

    # 2. Decision windows
    decision_windows = find_decision_windows(segments)
    print(f"  decision windows: {len(decision_windows)}")

    # 3. Per decision window: countdown digit detection + freeze + duck
    per_window_results = []
    for wi, win in enumerate(decision_windows[:3]):  # cap 3 per ref
        print(f"  window {wi+1}: '{win['segment_text'][:50]}' end={win['narration_end_s']:.2f}s")
        # Dense frames at 0.1s in narration_end → +5s window
        tmp_frames = Path(f"/tmp/canonical_pacing/{ref_id}_w{wi}")
        try:
            frame_paths = extract_frames_dense(
                source_mp4,
                win["expected_window_start_s"],
                win["expected_window_end_s"],
                interval_s=0.1,
                out_dir=tmp_frames,
            )
        except subprocess.CalledProcessError as e:
            print(f"    ⚠ frame extract failed: {e}")
            per_window_results.append({"window_idx": wi, "narration_end_s": win["narration_end_s"], "error": "frame_extract_failed"})
            continue

        # OCR digits
        try:
            transitions = detect_countdown_digits(
                frame_paths, easyocr_reader,
                start_s=win["expected_window_start_s"],
                interval_s=0.1,
            )
        except Exception as e:
            print(f"    ⚠ OCR failed: {e}")
            transitions = []
        print(f"    countdown transitions: {len(transitions)} → {[(t['t'], t['digit']) for t in transitions[:6]]}")

        # Compute digit durations
        digit_durations = []
        if len(transitions) >= 2:
            for i in range(len(transitions) - 1):
                if transitions[i]["digit"] in {"3", "2", "1"} and transitions[i+1]["digit"] in {"2", "1", "0"}:
                    dur = transitions[i+1]["t"] - transitions[i]["t"]
                    digit_durations.append(round(dur, 2))

        # Pause beat (narration_end → first countdown digit)
        pause_beat = None
        if transitions:
            pause_beat = round(transitions[0]["t"] - win["narration_end_s"], 2)

        # Freeze detection
        freeze = detect_freeze_via_ssim(
            frame_paths,
            start_s=win["expected_window_start_s"],
            interval_s=0.1,
        )

        # Audio duck
        duck = measure_ambient_duck(source_mp4, win)

        per_window_results.append({
            "window_idx": wi,
            "narration_text": win["segment_text"],
            "narration_end_s": round(win["narration_end_s"], 2),
            "expected_window_start_s": round(win["expected_window_start_s"], 2),
            "countdown_transitions": transitions[:8],
            "digit_durations_s": digit_durations,
            "pause_beat_s": pause_beat,
            "freeze": freeze,
            "ambient_duck": duck,
        })

    return {
        "ref_id": ref_id,
        "source_mp4": REF_TO_SOURCE[ref_id],
        "n_segments": len(segments),
        "n_decision_windows": len(decision_windows),
        "per_segment_wpm_bands": wpm_bands,
        "per_window_measurements": per_window_results,
    }


def aggregate_refs(per_ref_results):
    """Aggregate cross-ref canonical bands."""
    all_digit_durs = []
    all_pause_beats = []
    all_duck_db = []
    all_freeze_durations = []
    n_with_freeze = 0
    n_windows = 0

    # Per-role WPM aggregation
    per_role_wpms = {}

    for ref in per_ref_results:
        if not ref:
            continue
        for role, data in ref["per_segment_wpm_bands"].items():
            samples = [s["wpm"] for s in data.get("samples", [])]
            # Use full distribution via min/max/median markers
            per_role_wpms.setdefault(role, []).extend([data["median_wpm"]] + samples)

        for win in ref["per_window_measurements"]:
            n_windows += 1
            for d in win.get("digit_durations_s", []):
                if 0.3 < d < 2.5:  # sanity filter
                    all_digit_durs.append(d)
            pb = win.get("pause_beat_s")
            if pb is not None and -0.5 < pb < 3.0:
                all_pause_beats.append(pb)
            duck = win.get("ambient_duck", {}).get("duck_db")
            if duck is not None and -30 < duck < 5:
                all_duck_db.append(duck)
            freeze = win.get("freeze", {})
            if freeze.get("freeze_detected"):
                n_with_freeze += 1
                all_freeze_durations.append(freeze["duration_s"])

    def band(vals, name):
        if not vals:
            return {"median": None, "p25": None, "p75": None, "n_samples": 0}
        return {
            "median": round(float(median(vals)), 2),
            "p25": round(float(np.percentile(vals, 25)), 2),
            "p75": round(float(np.percentile(vals, 75)), 2),
            "n_samples": len(vals),
        }

    per_role_bands = {}
    for role, wpms in per_role_wpms.items():
        per_role_bands[role] = band(wpms, role)

    return {
        "schema_version": "v1",
        "extraction_date": "2026-05-20",
        "source_refs": [r["ref_id"] for r in per_ref_results if r],
        "params": {
            "countdown_digit_duration_s": band(all_digit_durs, "digit_dur"),
            "countdown_pause_beat_s": band(all_pause_beats, "pause"),
            "ambient_duck_db_during_countdown": band(all_duck_db, "duck"),
            "freeze_frame": {
                "pct_windows_with_freeze": round(n_with_freeze / max(n_windows, 1), 2),
                "n_windows_total": n_windows,
                "n_windows_with_freeze": n_with_freeze,
                "median_freeze_duration_s": round(float(median(all_freeze_durations)), 2) if all_freeze_durations else None,
            },
            "per_segment_wpm_bands": per_role_bands,
        },
        "notes": [
            "OCR via EasyOCR center crop. Confidence threshold 0.4.",
            "Freeze SSIM threshold 0.96 over 2s consecutive.",
            "Duck via librosa RMS pre 2s vs during decision window.",
            "Per-segment WPM categorized via heuristic regex patterns (role classifier).",
            "Filter overlay detection NOT included (Phase 2 — color histogram unreliable without canonical templates).",
            "Loading bar fill duration NOT included (Phase 2 — needs canonical UI template).",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="Format name (e.g., horror-choice). REQUIRED — no silent assumption.")
    parser.add_argument("--sources-dir", default=None,
                        help="Override sources MP4 dir (default: format-aware)")
    parser.add_argument("--out-dir", default=None,
                        help="Override output dir (default: format-aware empirical-decision-ui-pacing)")
    parser.add_argument("--refs", nargs="+", help="Specific refs (default: all 8)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print resolved paths + exit 0 (testability)")
    args = parser.parse_args()

    global SOURCES_DIR, OUT_DIR, REF_DIR
    paths = resolve_format_paths(args.format, args.sources_dir, args.out_dir)
    SOURCES_DIR = paths["sources_dir"]
    OUT_DIR = paths["out_dir"]
    REF_DIR = paths["ref_dir"]  # namespace per format post-TIER 2.3

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"sources_dir: {SOURCES_DIR}")
        print(f"out_dir: {OUT_DIR}")
        print(f"ref_dir: {REF_DIR}")
        return 0

    OUT_DIR.mkdir(exist_ok=True, parents=True)

    refs_to_process = args.refs or list(REF_TO_SOURCE.keys())

    # Init OCR once
    print("Initializing EasyOCR...")
    import easyocr
    reader = easyocr.Reader(["en"], gpu=False, verbose=False)
    print("EasyOCR ready.")

    per_ref_results = []
    for ref_id in refs_to_process:
        try:
            result = measure_ref(ref_id, reader)
            if result:
                out_path = OUT_DIR / f"{ref_id}-measurements.json"
                out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
                print(f"  ✓ saved: {out_path}")
                per_ref_results.append(result)
        except Exception as e:
            import traceback
            print(f"  ❌ {ref_id} failed: {e}")
            traceback.print_exc()

    if len(per_ref_results) >= 2:
        agg = aggregate_refs(per_ref_results)
        agg_path = OUT_DIR / "aggregate-canonical-bands.json"
        agg_path.write_text(json.dumps(agg, indent=2, ensure_ascii=False))
        print(f"\n✓ Aggregate saved: {agg_path}")
        print(f"  Bands: {json.dumps(agg['params'], indent=2)[:600]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
