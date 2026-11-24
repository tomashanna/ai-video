#!/usr/bin/env python3
"""
extract-canonical-max-detail.py — Phase 1 GAP #20 closure.

Extract dense frames per canonical referent + compile frame-by-frame events JSON.

Methodology (per GAP #20 docs MAX DETAIL):
- Frame extraction:
  - Every 0.5s for first 30s (hook + setup density)
  - Every 1s for rest of timeline (consequence + cliffhanger)
- Events compilation per ref:
  - Hook sub-beats (from transcription pattern matching)
  - Decision UI windows (from "Decidís"/"Ahora decides" patterns)
  - Scene cuts (from scene_cuts.txt)
  - Caption timestamps (from transcription segments)
  - Per-role narration segments

Outputs:
- canonical-scenes/ref-XX/frames-max-detail/ (folder with all dense frames)
- canonical-scenes/ref-XX-frame-by-frame-events.json
- canonical-scenes/aggregate-patterns.json (cross-ref hook sub-beat frequencies)

Usage:
    python extract-canonical-max-detail.py --format <format-name> [--refs ref-XX ref-YY] [--skip-frames]
    python extract-canonical-max-detail.py --format horror-choice [--sources-dir <path>] [--canonical-scenes-dir <path>]
    python extract-canonical-max-detail.py --format horror-choice --dry-run    # prints resolved paths + exit 0

Format-aware defaults:
- horror-choice: sources-dir = videosref_elige_tu_compa/, canonical-scenes = .claude/skills/horror-choice-format/canonical-scenes/
- arbitrary <X>: sources-dir = <X>-refs/, canonical-scenes = .claude/skills/<X>-format/canonical-scenes/
- --format is REQUIRED (no silent assumption)

Refactored Sub-Fase 3A.2 TIER 2.1 (2026-05-25): hardcoded paths → CLI flags per Capa A agnostic principle.
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from ai_video.paths import referent_analysis_dir, repo_root

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

PROJECT_ROOT = repo_root()
REF_DIR = referent_analysis_dir()

# Module-level paths populated by main() per --format flag.
# Sub-Fase 3A.2 TIER 2.1 (2026-05-25): hardcoded → CLI configurable (Capa A agnostic).
SOURCES_DIR = None
CANONICAL_SCENES_DIR = None


def resolve_format_paths(format_name, sources_override=None, canonical_scenes_override=None, ref_dir_override=None):
    """Resolve format-aware default paths or honor explicit overrides.

    horror-choice: namespaced post-TIER 2.3 (2026-05-25) — ref-XX moved to referent-analysis/horror-choice/
    arbitrary X:   <X>-refs/ + .claude/skills/<X>-format/canonical-scenes/ + referent-analysis/<X>/
    """
    if format_name == "horror-choice":
        defaults = {
            "sources_dir": PROJECT_ROOT / "videosref_elige_tu_compa",
            "canonical_scenes_dir": PROJECT_ROOT / ".claude/skills/horror-choice-format/canonical-scenes",
            "ref_dir": REF_DIR / "horror-choice",
        }
    else:
        defaults = {
            "sources_dir": PROJECT_ROOT / f"{format_name}-refs",
            "canonical_scenes_dir": PROJECT_ROOT / f".claude/skills/{format_name}-format/canonical-scenes",
            "ref_dir": REF_DIR / format_name,
        }
    return {
        "sources_dir": Path(sources_override) if sources_override else defaults["sources_dir"],
        "canonical_scenes_dir": Path(canonical_scenes_override) if canonical_scenes_override else defaults["canonical_scenes_dir"],
        "ref_dir": Path(ref_dir_override) if ref_dir_override else defaults["ref_dir"],
    }

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

HOOK_SUB_BEAT_PATTERNS = {
    "framing_question": [r"\b(?:escoge|elige|escogiste|decid[íi]).*(?:compañer|noche|salir)", r"\bpara salir\b"],
    "character_intro": [r"\b(?:o|y)\s+(?:\w+\s*)?(?:[A-Z][a-z]+|el matarife|la cocinera)\b"],
    "setup_threat": [r"\b(?:nunca|para siempre|loop|eterno|sin terminar|cena|infinito|silencio)\b"],
    "character_threat": [r"\b(?:no me|no te|prepárate|cuidado)\b"],
    "countdown_trigger": [r"\b(?:tres|3|tic|toc|ahora|ya)\b"],
}

DECISION_PATTERNS = [
    r"\b(?:ahora )?decid[íi]s?\b",
    r"\bahora decides?\b",
    r"\b(?:te|tu) (?:incomoda|gusta|asusta|quier|conv|prefier)\b",
    r"\bsi (?:escogiste|eliges|miras|seguís|salís|esper|te|sabes|te incomoda)\b",
    r"\bo (?:puedes|prefier|sabe[ns]?|ya)\b",
]

CLIFFHANGER_PATTERNS = [
    r"\b(?:saliste con vida|saliste sin|vive tu|aprendiste|baila|llegaste|nunca saldr[áa]s|nunca encontr[áa]s)\b",
    r"\b(?:la sirena|la fiesta|el infinito|el silencio|el vacío)\b",
]


def get_video_duration(mp4_path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4_path)],
        capture_output=True, text=True, check=True,
     timeout=SUBPROCESS_TIMEOUT_S)
    return float(r.stdout.strip())


def extract_dense_frames(mp4_path, out_dir, dense_until_s=30.0):
    """Extract every 0.5s for first 30s + every 1s for rest.

    Uses ffmpeg fps filter with split between two passes for efficiency.
    """
    out_dir.mkdir(exist_ok=True, parents=True)
    duration = get_video_duration(mp4_path)

    # Pass 1: dense (every 0.5s) first 30s
    pass1 = out_dir / "_pass1.txt"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(mp4_path),
        "-t", str(min(dense_until_s, duration)),
        "-vf", "fps=2,scale=540:960",  # 2 fps = every 0.5s
        "-q:v", "3",
        "-pix_fmt", "yuvj420p",
        str(out_dir / "frame_dense_%04d.jpg"),
    ], check=True, timeout=SUBPROCESS_TIMEOUT_S)
    n_dense = len(list(out_dir.glob("frame_dense_*.jpg")))

    # Pass 2: sparse (every 1s) from 30s onwards
    if duration > dense_until_s:
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", str(dense_until_s),
            "-i", str(mp4_path),
            "-vf", "fps=1,scale=540:960",  # 1 fps = every 1s
            "-q:v", "3",
            "-pix_fmt", "yuvj420p",
            str(out_dir / "frame_sparse_%04d.jpg"),
        ], check=True, timeout=SUBPROCESS_TIMEOUT_S)
    n_sparse = len(list(out_dir.glob("frame_sparse_*.jpg")))

    return {
        "dense_frames": n_dense,
        "sparse_frames": n_sparse,
        "total_frames": n_dense + n_sparse,
        "dense_interval_s": 0.5,
        "sparse_interval_s": 1.0,
        "dense_until_s": dense_until_s,
        "video_duration_s": duration,
    }


def classify_segment_role(text, idx, total_segments):
    """Heuristic role classifier per segment in narrative arc position."""
    text_lower = text.lower().strip()
    pos = idx / max(total_segments - 1, 1)  # 0.0 = start, 1.0 = end

    # Position-aware: first 15% = hook, last 15% = cliffhanger
    if pos < 0.15:
        for pat in HOOK_SUB_BEAT_PATTERNS["framing_question"]:
            if re.search(pat, text_lower):
                return "hook_framing_question"
        for pat in HOOK_SUB_BEAT_PATTERNS["character_intro"]:
            if re.search(pat, text_lower):
                return "hook_character_intro"
        for pat in HOOK_SUB_BEAT_PATTERNS["character_threat"]:
            if re.search(pat, text_lower):
                return "hook_character_threat"
        return "hook_other"

    if pos > 0.85:
        for pat in CLIFFHANGER_PATTERNS:
            if re.search(pat, text_lower):
                return "cliffhanger"
        return "cliffhanger_outro"

    # Middle 70% = setup, decision, consequence
    for pat in DECISION_PATTERNS:
        if re.search(pat, text_lower):
            return "decision_question"
    if re.search(r"^si (?:eliges|escogiste|miras|seguís|salís|esper|te quieres|sabes)", text_lower):
        return "consequence_setup"
    if re.search(r"\b(?:envía|enoja|sonríe|deja de|abre la|aprende a)\b", text_lower):
        return "consequence_narration"
    if re.search(r"\b(?:empieza a|empieza|aparece|se voltea|se acerca|empezás|de repente)\b", text_lower):
        return "decision_setup"

    return "setup_unclassified"


def find_decision_windows(segments):
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
                    "estimated_decision_window_end_s": min(seg["end"] + 5.0, segments[-1]["end"]),
                })
                break
    return windows


def find_hook_sub_beats(segments, hook_end_s=15.0):
    """Identify hook sub-beats from transcription segments."""
    sub_beats = []
    for i, seg in enumerate(segments):
        if seg["start"] > hook_end_s:
            break
        text_lower = seg["text"].lower().strip()
        for beat_name, patterns in HOOK_SUB_BEAT_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, text_lower):
                    sub_beats.append({
                        "segment_idx": i,
                        "start_s": seg["start"],
                        "end_s": seg["end"],
                        "beat_type": beat_name,
                        "text": seg["text"].strip(),
                    })
                    break
    return sub_beats


def find_cliffhanger_segments(segments, cliffhanger_start_pct=0.85):
    cliff = []
    for i, seg in enumerate(segments):
        pos = i / max(len(segments) - 1, 1)
        if pos < cliffhanger_start_pct:
            continue
        text_lower = seg["text"].lower().strip()
        for pat in CLIFFHANGER_PATTERNS:
            if re.search(pat, text_lower):
                cliff.append({
                    "segment_idx": i,
                    "start_s": seg["start"],
                    "end_s": seg["end"],
                    "text": seg["text"].strip(),
                })
                break
    return cliff


def compile_events(ref_id, transcription_path, scene_cuts_path):
    transcription = json.loads(transcription_path.read_text())
    segments = transcription["segments"]

    # Scene cuts
    scene_cuts = []
    if scene_cuts_path.exists():
        for line in scene_cuts_path.read_text().splitlines():
            line = line.strip()
            if line:
                try:
                    scene_cuts.append(float(line))
                except ValueError:
                    pass

    # Per-segment role
    role_assigned = []
    role_counter = Counter()
    for i, seg in enumerate(segments):
        role = classify_segment_role(seg["text"], i, len(segments))
        role_assigned.append({
            "segment_idx": i,
            "start_s": seg["start"],
            "end_s": seg["end"],
            "duration_s": seg["end"] - seg["start"],
            "text": seg["text"].strip(),
            "role": role,
            "words": len(seg["text"].split()),
            "wpm": round(len(seg["text"].split()) / max(seg["end"] - seg["start"], 0.1) * 60.0, 1),
        })
        role_counter[role] += 1

    return {
        "ref_id": ref_id,
        "n_segments": len(segments),
        "total_duration_s": segments[-1]["end"] if segments else 0,
        "n_scene_cuts": len(scene_cuts),
        "scene_cut_density_per_min": round(len(scene_cuts) / max(segments[-1]["end"], 1) * 60, 2) if segments else 0,
        "hook_sub_beats": find_hook_sub_beats(segments),
        "decision_windows": find_decision_windows(segments),
        "cliffhanger_segments": find_cliffhanger_segments(segments),
        "role_distribution": dict(role_counter),
        "segments_annotated": role_assigned,
        "scene_cuts_timestamps": scene_cuts,
    }


def aggregate_patterns(per_ref_events):
    """Cross-ref aggregation: hook sub-beat order frequency + cliffhanger structure."""
    hook_beat_order = []
    decision_windows_per_ref = []
    cliffhanger_count = Counter()
    scene_cut_densities = []
    role_distributions = Counter()

    for ref_events in per_ref_events:
        if not ref_events:
            continue
        # Hook sub-beat sequence
        beats = [b["beat_type"] for b in ref_events["hook_sub_beats"]]
        hook_beat_order.append({
            "ref_id": ref_events["ref_id"],
            "beat_order": beats,
        })
        decision_windows_per_ref.append({
            "ref_id": ref_events["ref_id"],
            "n_decisions": len(ref_events["decision_windows"]),
        })
        for cs in ref_events["cliffhanger_segments"]:
            cliffhanger_count["has_cliffhanger"] += 1
            break
        scene_cut_densities.append(ref_events["scene_cut_density_per_min"])
        for role, n in ref_events["role_distribution"].items():
            role_distributions[role] += n

    # Hook beat-type frequency across refs
    beat_freq = Counter()
    for ref in hook_beat_order:
        for beat in ref["beat_order"]:
            beat_freq[beat] += 1

    return {
        "schema_version": "v1",
        "extraction_date": "2026-05-20",
        "n_refs": len(per_ref_events),
        "hook_sub_beat_frequency": dict(beat_freq),
        "hook_sub_beat_order_per_ref": hook_beat_order,
        "decision_windows_per_ref": decision_windows_per_ref,
        "n_refs_with_cliffhanger": cliffhanger_count["has_cliffhanger"],
        "scene_cut_density_per_min": {
            "median": round(sorted(scene_cut_densities)[len(scene_cut_densities)//2], 2) if scene_cut_densities else 0,
            "min": round(min(scene_cut_densities), 2) if scene_cut_densities else 0,
            "max": round(max(scene_cut_densities), 2) if scene_cut_densities else 0,
        },
        "role_distribution_cumulative": dict(role_distributions),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="Format name (e.g., horror-choice). REQUIRED — no silent assumption.")
    parser.add_argument("--sources-dir", default=None,
                        help="Override sources MP4 dir (default: format-aware)")
    parser.add_argument("--canonical-scenes-dir", default=None,
                        help="Override canonical-scenes output dir (default: format-aware)")
    parser.add_argument("--refs", nargs="+", help="Specific refs (default: all 8)")
    parser.add_argument("--skip-frames", action="store_true", help="Skip dense frame extraction (use existing)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print resolved paths + exit 0 (testability)")
    args = parser.parse_args()

    global SOURCES_DIR, CANONICAL_SCENES_DIR, REF_DIR
    paths = resolve_format_paths(args.format, args.sources_dir, args.canonical_scenes_dir)
    SOURCES_DIR = paths["sources_dir"]
    CANONICAL_SCENES_DIR = paths["canonical_scenes_dir"]
    REF_DIR = paths["ref_dir"]  # namespace per format post-TIER 2.3 completion (2026-05-25)

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"sources_dir: {SOURCES_DIR}")
        print(f"canonical_scenes_dir: {CANONICAL_SCENES_DIR}")
        print(f"ref_dir: {REF_DIR}")
        return 0

    CANONICAL_SCENES_DIR.mkdir(exist_ok=True, parents=True)

    refs_to_process = args.refs or list(REF_TO_SOURCE.keys())

    per_ref_events = []
    for ref_id in refs_to_process:
        print(f"\n=== {ref_id} ===")
        source_mp4 = SOURCES_DIR / REF_TO_SOURCE[ref_id]
        if not source_mp4.exists():
            print(f"  ❌ Source MP4 not found: {source_mp4.name}")
            continue

        transcription_path = REF_DIR / ref_id / "transcription.json"
        scene_cuts_path = REF_DIR / ref_id / "scene_cuts.txt"
        if not transcription_path.exists():
            print(f"  ❌ Transcription missing: {transcription_path}")
            continue

        # Frame extraction
        frames_dir = CANONICAL_SCENES_DIR / ref_id / "frames-max-detail"
        if not args.skip_frames:
            print(f"  Extracting dense frames → {frames_dir}")
            try:
                frame_info = extract_dense_frames(source_mp4, frames_dir)
                print(f"    ✓ {frame_info['total_frames']} frames ({frame_info['dense_frames']} dense @ 0.5s + {frame_info['sparse_frames']} sparse @ 1s)")
            except subprocess.CalledProcessError as e:
                print(f"    ❌ ffmpeg failed: {e}")
                frame_info = {"error": "extraction_failed"}
        else:
            n_existing = len(list(frames_dir.glob("frame_*.jpg"))) if frames_dir.exists() else 0
            frame_info = {"total_frames": n_existing, "skip_frames": True}
            print(f"  Skipped frame extraction (existing: {n_existing} frames)")

        # Compile events
        print("  Compiling events from transcription + scene_cuts...")
        events = compile_events(ref_id, transcription_path, scene_cuts_path)
        events["frame_extraction_info"] = frame_info
        events["source_mp4"] = REF_TO_SOURCE[ref_id]

        # Save per-ref events JSON
        events_path = CANONICAL_SCENES_DIR / f"{ref_id}-frame-by-frame-events.json"
        events_path.write_text(json.dumps(events, indent=2, ensure_ascii=False))
        print(f"    ✓ events saved: {events_path}")
        print(f"    hook sub-beats: {len(events['hook_sub_beats'])} | decisions: {len(events['decision_windows'])} | cliffhanger segs: {len(events['cliffhanger_segments'])}")
        print(f"    role distribution: {events['role_distribution']}")
        per_ref_events.append(events)

    # Aggregate
    if len(per_ref_events) >= 2:
        agg = aggregate_patterns(per_ref_events)
        agg_path = CANONICAL_SCENES_DIR / "aggregate-patterns.json"
        agg_path.write_text(json.dumps(agg, indent=2, ensure_ascii=False))
        print(f"\n✓ Aggregate saved: {agg_path}")
        print(f"  Hook sub-beat frequency: {agg['hook_sub_beat_frequency']}")
        print(f"  Refs with cliffhanger: {agg['n_refs_with_cliffhanger']}/{agg['n_refs']}")
        print(f"  Scene cut density (per min): median={agg['scene_cut_density_per_min']['median']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
