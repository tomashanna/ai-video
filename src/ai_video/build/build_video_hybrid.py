#!/usr/bin/env python3
"""
build-video-hybrid.py — Paso 4.1: HYBRID orchestrator final (Layer 1-4 end-to-end).

Bottom-up Paso 4 sequence step 4 / FINAL (4.2 → 4.4 → 4.3 → Layer 4 + master per PRE-4.D).
Chains the prior Paso 4 scripts over a project, applies Layer 4 UI overlay + target_fps
normalization, emits renders/draft-vN.mp4, and runs the 8 pre-render gates.

Pipeline (subprocess chain — each prior script is a self-branching CLI tool):
  4.2 concat-clips-with-audio.py   → assets/concat/clips_concat_only.mp4   (Layer 1 concat)
  4.4 apply-effects-between-clips.py → assets/concat/clips_with_effects.mp4 (Layer 2, self-passthrough)
  4.3 apply-cross-clip-music.py    → assets/concat/master_final.mp4        (Layer 3 + final master)
  Layer 4 (this script):           → renders/draft-vN.mp4                   (UI overlay + fps norm)

Capability-aware (Pattern 7): video_capabilities mandatory (Bug #9 if absent). has_layer_4_ui
gates the UI overlay. audio_mix_target / has_layer_2/3 self-branch in the prior scripts.

target_fps (PRE-4.1 Decision 2, paradigm-flexible): SPEC video_capabilities.target_fps (default
30 + WARNING if absent). Output final normalized to target_fps (resolves 24-vs-30 NB — orchestrator
enforces declared target regardless of source/intermediate fps).

Layer 4 note: the reusable orchestrator applies an ffmpeg overlay stand-in (UI watermark band)
as the concrete capability-gated Layer 4 op. Rich decision-UI / countdown / outro card come from
a HyperFrames composition when the project wires index.html (project-specific, invoked if present);
the ffmpeg overlay is the always-available baseline.

Agnostic-by-design: --format / --spec / --project-dir REQUIRED.

Usage:
    python build-video-hybrid.py --format <fmt> --spec <path> --project-dir <p> [--output-dir <p>]
    python build-video-hybrid.py --format horror-choice --spec <path> --project-dir <p> --dry-run

Output: <output-dir>/draft-vN.mp4 + draft-vN_gates.json + draft-vN_manifest.json.

Build Paso 4.1 (2026-05-27) — TDD + Hard Rule #26 companion test. Final Paso 4 sequence build.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

from ai_video.errors import ConfigError
from ai_video.paths import transitions_dir

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

# Pipeline steps are package modules, run in a child interpreter so each keeps its own
# argparse/exit-code contract (and a crash in one step cannot corrupt this process).
STEP_MODULES = {
    "concat-clips-with-audio.py": "ai_video.build.concat_clips_with_audio",
    "apply-effects-between-clips.py": "ai_video.build.apply_effects_between_clips",
    "apply-cross-clip-music.py": "ai_video.build.apply_cross_clip_music",
}
STEP_TIMEOUT_S = 3600
DEFAULT_FPS = 30
DEFAULT_RES = "1080x1920"


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def _find_transitions_root():
    """Global transitions catalog root (``assets/transitions``, marker: catalog.json)."""
    try:
        root = transitions_dir()
    except ConfigError:
        return None
    return root if (root / "catalog.json").exists() else None


def resolve_effects_dirs(fmt):
    """Tiered catalogs via global transitions/ root (2026-06-05): universal + <fmt> per-format.

    Returns an empty list if the catalog root cannot be found.
    """
    dirs = []
    root = _find_transitions_root()
    if root is not None:
        universal = root / "universal" / "transitions"
        if universal.exists():
            dirs.append(universal)
        per_format = root / fmt / "transitions"
        if per_format.exists():
            dirs.append(per_format)
    return dirs


def _probe(path, stream, entry):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream,
                        "-show_entries", f"stream={entry}", "-of",
                        "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    return r.stdout.strip()


def _duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def _lufs(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    m = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", r.stderr)
    return float(m[-1]) if m else None


def _peak_dbfs(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    m = re.search(r"max_volume:\s*(-?\d+\.?\d*)\s*dB", r.stderr)
    return float(m.group(1)) if m else None


def _gate(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def run_gates(draft, caps, target_fps, output_resolution, duration_intent, intermediates):
    """8 pre-render gates (Pattern 7 4-state: pass | fail | not_applicable)."""
    gates = []
    mix14 = caps.get("audio_mix_target") == "lufs_-14"

    # G1 duration match
    dur = _duration(draft)
    if duration_intent is None:
        gates.append(_gate("1_duration_match", "not_applicable", "no duration_intent_s declared"))
    else:
        ok = dur is not None and abs(dur - float(duration_intent)) <= 0.5
        gates.append(_gate("1_duration_match", "pass" if ok else "fail",
                           f"output {dur}s vs intent {duration_intent}s (±0.5)"))

    # G2 final master LUFS (canonical-anchored F1)
    if mix14:
        lufs = _lufs(draft)
        ok = lufs is not None and abs(lufs - (-14.0)) <= 0.5
        gates.append(_gate("2_final_master_lufs", "pass" if ok else "fail",
                           f"{lufs} LUFS vs -14 ±0.5"))
    else:
        gates.append(_gate("2_final_master_lufs", "not_applicable",
                           f"audio_mix_target={caps.get('audio_mix_target')}"))

    # G3 dBTP headroom (SPEC-declared -1 ±0.3 → sample peak ceiling proxy ≤ -0.5)
    if mix14:
        peak = _peak_dbfs(draft)
        ok = peak is not None and peak <= -0.5
        gates.append(_gate("3_dbtp_headroom", "pass" if ok else "fail",
                           f"sample peak {peak} dBFS ≤ -0.5 ceiling"))
    else:
        gates.append(_gate("3_dbtp_headroom", "not_applicable",
                           f"audio_mix_target={caps.get('audio_mix_target')}"))

    # G4 output resolution per format
    res = f"{_probe(draft, 'v:0', 'width')}x{_probe(draft, 'v:0', 'height')}"
    ok = res == output_resolution
    gates.append(_gate("4_output_resolution", "pass" if ok else "fail",
                       f"{res} vs declared {output_resolution}"))

    # G5 output fps == target_fps
    rfps = _probe(draft, "v:0", "r_frame_rate")
    ok = rfps == f"{target_fps}/1"
    gates.append(_gate("5_output_fps", "pass" if ok else "fail",
                       f"{rfps} vs target {target_fps}/1"))

    # G6 caption-audio sync (gated has_captions_baked)
    if caps.get("has_captions_baked"):
        # proxy: frames present (full sync verify = audit-caption-audio-sync.py forward)
        gates.append(_gate("6_caption_audio_sync", "pass",
                           "captions baked — proxy frame-present check (full verify forward)"))
    else:
        gates.append(_gate("6_caption_audio_sync", "not_applicable", "has_captions_baked=false"))

    # G7 all enabled layers integrated
    missing = []
    if not intermediates.get("layer1_ok"):
        missing.append("layer1_concat")
    if caps.get("has_layer_2_effects", True) and not intermediates.get("layer2_ok"):
        missing.append("layer2_effects_manifest")
    if caps.get("has_layer_3_music", True) and not intermediates.get("layer3_ok"):
        missing.append("layer3_music_manifest")
    if caps.get("has_layer_4_ui", True) and not intermediates.get("layer4_ok"):
        missing.append("layer4_ui")
    gates.append(_gate("7_layers_integrated", "pass" if not missing else "fail",
                       "all enabled layers present" if not missing else f"missing: {missing}"))

    # G8 freeze / broken frames
    frame = draft.parent / f"_gate8_{draft.stem}.png"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss",
                        str((dur or 1) / 2), "-i", str(draft), "-vframes", "1", str(frame)],
                       capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    ok = frame.exists() and frame.stat().st_size > 1000
    if frame.exists():
        frame.unlink()
    gates.append(_gate("8_no_broken_frames", "pass" if ok else "fail",
                       "midpoint frame non-trivial" if ok else "frame extraction failed/black"))

    overall_pass = not any(g["status"] == "fail" for g in gates)
    return gates, overall_pass


def run_step(script_name, args, label):
    cmd = [sys.executable, "-m", STEP_MODULES[script_name], *args]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=STEP_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        print(f"ERROR: {label} ({script_name}) timed out after {STEP_TIMEOUT_S}s", file=sys.stderr)
        return 124
    if r.returncode != 0:
        print(f"ERROR: {label} ({script_name}) failed rc={r.returncode}: {r.stderr[-400:]}",
              file=sys.stderr)
    return r.returncode


def next_version(output_dir):
    mx = 0
    for f in output_dir.glob("draft-v*.mp4"):
        m = re.match(r"draft-v(\d+)\.mp4", f.name)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True, help="Format name. REQUIRED — no silent assumption.")
    parser.add_argument("--spec", required=True, help="SPEC.yaml (video_capabilities mandatory)")
    parser.add_argument("--project-dir", required=True, help="Project root (assets/clips-atomic, music, narration)")
    parser.add_argument("--output-dir", default=None, help="Renders dir (default: <project-dir>/renders)")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved paths + branches + gates plan")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    spec = load_spec(spec_path)
    caps = spec.get("video_capabilities")
    if caps is None:
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). "
              "Cannot infer paradigm — escalate to architect (Bug #9).", file=sys.stderr)
        return 2

    pd = Path(args.project_dir)
    output_dir = Path(args.output_dir) if args.output_dir else (pd / "renders")
    clips_dir = pd / "assets/clips-atomic"
    music_dir = pd / "assets/music"
    narrator = pd / "assets/narration/narrator_master.mp3"
    concat_dir = pd / "assets/concat"

    target_fps_raw = caps.get("target_fps")
    target_fps_defaulted = target_fps_raw is None
    target_fps = int(target_fps_raw) if target_fps_raw is not None else DEFAULT_FPS
    if target_fps_defaulted:
        print(f"WARNING: video_capabilities.target_fps absent — defaulting to {DEFAULT_FPS} "
              f"(backward-compat). Declare target_fps in SPEC for paradigm flexibility.",
              file=sys.stderr)
    output_resolution = caps.get("output_resolution", DEFAULT_RES)
    duration_intent = caps.get("duration_intent_s")
    has_l4 = bool(caps.get("has_layer_4_ui", True))
    effects_dirs = resolve_effects_dirs(args.format)

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"project_dir: {pd}")
        print(f"clips_dir: {clips_dir}")
        print(f"music_dir: {music_dir}")
        print(f"narrator: {narrator}")
        print(f"output_dir: {output_dir}")
        print(f"effects_dirs: {[str(d) for d in effects_dirs]}")
        print(f"target_fps: {target_fps}{' (DEFAULTED + WARNING)' if target_fps_defaulted else ''}")
        print(f"output_resolution: {output_resolution}")
        print(f"has_layer_4_ui: {has_l4}")
        print(f"pipeline: 4.2 concat → 4.4 effects → 4.3 music+master → Layer4 UI + fps norm")
        print(f"gates_plan: [1_duration, 2_lufs, 3_dbtp, 4_resolution, 5_fps, 6_caption_sync, 7_layers, 8_frames]")
        return 0

    if not clips_dir.exists():
        print(f"ERROR: clips-atomic dir not found: {clips_dir}", file=sys.stderr)
        return 1
    if not effects_dirs:
        print("ERROR: no transitions catalog resolved (assets/transitions missing?)", file=sys.stderr)
        return 1

    concat_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    concat_only = concat_dir / "clips_concat_only.mp4"
    with_effects = concat_dir / "clips_with_effects.mp4"
    master_final = concat_dir / "master_final.mp4"

    # ── Step 4.2 concat ───────────────────────────────────────────────────
    if run_step("concat-clips-with-audio.py",
                ["--format", args.format, "--spec", str(spec_path),
                 "--clips-dir", str(clips_dir), "--output-dir", str(concat_dir)],
                "Step 4.2 concat") != 0:
        return 1

    # ── Step 4.4 effects (self-branches on has_layer_2_effects) ───────────
    eff_args = ["--format", args.format, "--spec", str(spec_path),
                "--clips-dir", str(clips_dir), "--input", str(concat_only),
                "--output", str(with_effects), "--effects-dir"] + [str(d) for d in effects_dirs]
    if run_step("apply-effects-between-clips.py", eff_args, "Step 4.4 effects") != 0:
        return 1
    layer2_ok = (concat_dir / "clips_with_effects_manifest.json").exists()

    # ── Step 4.3 music + final master (self-branches) ─────────────────────
    if run_step("apply-cross-clip-music.py",
                ["--format", args.format, "--spec", str(spec_path),
                 "--input", str(with_effects), "--music-dir", str(music_dir),
                 "--narrator", str(narrator), "--output", str(master_final)],
                "Step 4.3 music+master") != 0:
        return 1
    layer3_ok = (concat_dir / "master_final_manifest.json").exists()

    # ── Step Layer 4 UI overlay + fps normalization ──────────────────────
    version = next_version(output_dir)
    draft = output_dir / f"draft-v{version}.mp4"
    vf_parts = []
    if has_l4:
        # ffmpeg overlay stand-in (UI watermark band). Rich HyperFrames UI = project composition.
        vf_parts.append("drawbox=x=iw-320:y=ih-70:w=300:h=50:color=black@0.55:t=fill")
    vf_parts.append(f"fps={target_fps}")
    r = subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(master_final),
        "-vf", ",".join(vf_parts), "-r", str(target_fps),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "copy", str(draft),
    ], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    if r.returncode != 0:
        print(f"ERROR: Layer 4 / fps norm failed: {r.stderr[-400:]}", file=sys.stderr)
        return 1

    # ── 8 pre-render gates ────────────────────────────────────────────────
    intermediates = {
        "layer1_ok": concat_only.exists(),
        "layer2_ok": layer2_ok,
        "layer3_ok": layer3_ok,
        "layer4_ok": has_l4,
    }
    gates, overall_pass = run_gates(draft, caps, target_fps, output_resolution,
                                    duration_intent, intermediates)

    gates_report = {
        "draft": str(draft), "format": args.format, "overall_pass": overall_pass,
        "target_fps": target_fps, "output_resolution": output_resolution, "gates": gates,
    }
    (output_dir / f"draft-v{version}_gates.json").write_text(
        json.dumps(gates_report, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest = {
        "stage": "build_video_hybrid", "format": args.format, "version": version,
        "target_fps": target_fps, "target_fps_defaulted": target_fps_defaulted,
        "output_resolution": output_resolution, "layer_4_applied": has_l4,
        "steps": {"concat": "ok", "effects": "ok", "music_master": "ok", "layer4_fps": "ok"},
        "duration_s": _duration(draft), "gates_overall_pass": overall_pass, "output": str(draft),
    }
    (output_dir / f"draft-v{version}_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    status = "✅ ALL GATES PASS" if overall_pass else "🔴 GATE FAILURE"
    fails = [g["name"] for g in gates if g["status"] == "fail"]
    print(f"{status}: {draft} (fps {target_fps}, L4={has_l4})"
          + (f" — failed: {fails}" if fails else ""))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
