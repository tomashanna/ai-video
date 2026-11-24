#!/usr/bin/env python3
"""
concat-clips-with-audio.py — Paso 4.2: pure sequential concat of atomic clips.

Bottom-up Paso 4 sequence step 1 (4.2 → 4.4 → 4.3 → 4.1 per PRE-4.D verdict).
Concatenates assets/clips-atomic/*.mp4 in SPEC shot_list order, audio properly muxed.
NO transitions/xfade — that is 4.4 apply-effects-between-clips.py, applied POST-concat
per PRE-4.E canonical (xfade filter post-concat, NOT pre-rendered effect mp4s).

Capability-aware (Pattern 7, PIPELINE §13.10): reads spec.video_capabilities + branches
per source_clips_origin. NO silent horror-choice paradigm assumption.

Agnostic-by-design: --format REQUIRED (no silent assumption). Pattern mirrors
measure-canonical-decision-ui-pacing.py post-TIER-2.1 refactor.

Usage:
    python concat-clips-with-audio.py --format <format> --spec <path> [--clips-dir <p>] [--output-dir <p>]
    python concat-clips-with-audio.py --format horror-choice --spec <path> --dry-run

Implementation: ffmpeg concat demuxer + stream copy (lossless — preserves codec/fps/
captions/sample-rate). Falls back to concat-filter re-encode if stream-copy fails
(heterogeneous inputs). pre_existing paradigm defaults to re-encode (heterogeneous-safe).

Output: <output-dir>/clips_concat_only.mp4

Build Paso 4.2 (2026-05-26) — TDD + Hard Rule #26 (test_concat-clips-with-audio.py companion).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def resolve_paths(format_name, clips_override=None, output_override=None):
    """Resolve clips-dir + output-dir. Project-relative defaults (NOT format-specific —
    atomic clips always live in <project>/assets/clips-atomic regardless of paradigm).
    --format drives capability awareness + appears in dry-run output for agnostic proof.
    """
    clips_dir = Path(clips_override) if clips_override else Path("assets/clips-atomic")
    output_dir = Path(output_override) if output_override else Path("assets/concat")
    return {"clips_dir": clips_dir, "output_dir": output_dir}


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def determine_branch(caps):
    """Capability-aware branch per Pattern 7. Returns 'ai_generated' | 'pre_existing' | 'mixed'.

    Raises ValueError if video_capabilities missing (Bug #9 escalation — Pattern 7 mandates
    explicit capability declaration, no silent paradigm assumption).
    """
    if caps is None:
        raise ValueError(
            "SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). "
            "Cannot infer paradigm — escalate to architect (Bug #9)."
        )
    origin = caps.get("source_clips_origin", "ai_generated")
    if origin == "mixed":
        raise NotImplementedError(
            "source_clips_origin: mixed paradigm requires dedicated sprint (not yet built)."
        )
    if origin == "pre_existing" or not caps.get("has_ai_generated_clips", True):
        return "pre_existing"
    return "ai_generated"


def build_concat_list(shot_list, clips_dir):
    """Map SPEC shot_list[] order → <clips-dir>/<shot_id>_atomic.mp4 paths (in order)."""
    clips = []
    missing = []
    for shot in shot_list:
        shot_id = shot["shot_id"] if isinstance(shot, dict) else str(shot)
        clip = clips_dir / f"{shot_id}_atomic.mp4"
        if clip.exists():
            clips.append(clip.resolve())
        else:
            missing.append(str(clip))
    return clips, missing


def _run_concat(clip_paths, output_path, stream_copy):
    """ffmpeg concat demuxer. stream_copy=True → -c copy (lossless). False → re-encode."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as lf:
        for c in clip_paths:
            # escape single quotes per ffmpeg concat list syntax
            safe = str(c).replace("'", "'\\''")
            lf.write(f"file '{safe}'\n")
        list_path = lf.name

    base = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list_path]
    if stream_copy:
        cmd = base + ["-c", "copy", str(output_path)]
    else:
        cmd = base + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(output_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    Path(list_path).unlink(missing_ok=True)
    return r


def concat_clips(clip_paths, output_path, branch):
    """Concat with capability-aware strategy + auto-fallback.

    ai_generated → stream copy (uniform atomic clips, lossless).
    pre_existing → re-encode (heterogeneous-safe).
    Fallback: if stream-copy fails → re-encode.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stream_copy = (branch == "ai_generated")
    r = _run_concat(clip_paths, output_path, stream_copy=stream_copy)
    if r.returncode != 0 and stream_copy:
        # Fallback: stream-copy failed (likely heterogeneous timebase) → re-encode
        print(f"⚠️ stream-copy concat failed, falling back to re-encode: {r.stderr[:200]}",
              file=sys.stderr)
        r = _run_concat(clip_paths, output_path, stream_copy=False)
    return r


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="Format name (e.g., horror-choice). REQUIRED — no silent assumption.")
    parser.add_argument("--spec", required=True, help="Path to SPEC.yaml (video_capabilities mandatory)")
    parser.add_argument("--clips-dir", default=None, help="Atomic clips dir (default: assets/clips-atomic)")
    parser.add_argument("--output-dir", default=None, help="Output dir (default: assets/concat)")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved paths + branch, exit 0")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    paths = resolve_paths(args.format, args.clips_dir, args.output_dir)
    clips_dir = paths["clips_dir"]
    output_dir = paths["output_dir"]

    spec = load_spec(spec_path)
    caps = spec.get("video_capabilities")
    shot_list = spec.get("shot_list", []) or []

    try:
        branch = determine_branch(caps)
    except (ValueError, NotImplementedError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"clips_dir: {clips_dir}")
        print(f"output_dir: {output_dir}")
        print(f"capability_branch: {branch}")
        print(f"source_clips_origin: {caps.get('source_clips_origin', 'ai_generated')}")
        print(f"shot_count: {len(shot_list)}")
        return 0

    clip_paths, missing = build_concat_list(shot_list, clips_dir)
    if missing:
        print(f"ERROR: {len(missing)} atomic clip(s) missing: {missing[:3]}", file=sys.stderr)
        return 1
    if not clip_paths:
        print("ERROR: no clips resolved from SPEC shot_list", file=sys.stderr)
        return 1

    output_path = output_dir / "clips_concat_only.mp4"
    r = concat_clips(clip_paths, output_path, branch)
    if r.returncode != 0:
        print(f"ERROR: ffmpeg concat failed: {r.stderr[:300]}", file=sys.stderr)
        return 1

    print(f"✅ Concat complete ({branch}): {len(clip_paths)} clips → {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
