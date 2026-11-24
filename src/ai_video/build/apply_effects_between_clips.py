#!/usr/bin/env python3
"""
apply-effects-between-clips.py — Paso 4.4: effects library applier (Layer 2 HYBRID).

Bottom-up Paso 4 sequence step 2 (4.2 → 4.4 → 4.3 → 4.1 per PRE-4.D verdict).
Applies inter-clip transitions (xfade + audio stings) per SPEC shot_list[].transition_out
and effects-library/transitions/*.json recipes.

Architecture — PRE-4.E (PIPELINE §13.9.1 LAYER 2): xfade filter at clip boundaries, NO
pre-rendered effect mp4s. xfade physically requires 2 separate inputs, so the effects branch
reads the ATOMIC CLIPS (V4 empirical cp5-layer2-concat.py reads N atomic clips + chains xfade
with cumulative offsets). The 4.2 output (clips_concat_only.mp4) is used for the PASSTHROUGH
branch (has_layer_2_effects: false → copy concat'd stream as final 4.4 output).

Tiered global transitions/ root (2026-06-05, "Disponibilidad ≠ Uso"): universal primitives
(<repo>/transitions/universal/transitions/) + per-format sub-genre
(<repo>/transitions/<format>/transitions/). Index: <repo>/transitions/catalog.json.
Legacy effects-library paths remain as compat symlinks. --effects-dir accepts ONE OR MORE
catalog dirs (searched in order). It is REQUIRED in the effects branch — no silent format default
(agnostic-by-design). Per-shot transition schema is canonical (PRE-4.J); legacy top-level
transitions[] arrays are normalized via lib/spec_transitions_adapter.normalize_transitions.

Option D (PRE-4.J): each recipe declares xfade_transition + xfade_fidelity (literal|approximate)
+ native_mechanism_note. When an `approximate`-fidelity recipe is used in a REAL run, a WARNING
is emitted (chained-xfade reduction is lossy; full fidelity = Option B hybrid dispatch, GAPS-LOG).

Capability-aware (Pattern 7, PIPELINE §13.10): reads spec.video_capabilities.has_layer_2_effects.
False → passthrough. Missing video_capabilities block → Bug #9 escalation (exit 2).

Usage:
    python apply-effects-between-clips.py --format <fmt> --spec <path> \\
        --effects-dir <capaA_transitions> [<capaB_transitions> ...] \\
        [--clips-dir <p>] [--input <concat.mp4>] [--output <p>]
    python apply-effects-between-clips.py --format horror-choice --spec <path> --dry-run

Output: <output> (default assets/concat/clips_with_effects.mp4) + sidecar manifest JSON.

Build Paso 4.4 (2026-05-26). PRE-4.J/PRE-4.K integration (2026-05-27): multi-catalog --effects-dir,
Option D fidelity warnings, spec_transitions_adapter. Hard Rule #26 companion test.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

from ai_video.core.spec_transitions_adapter import normalize_transitions

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800


# Fallback for recipe ids that lack an explicit `xfade_transition` field (post Option D all
# canonical recipes declare it; this remains for forward/legacy robustness).
REAL_RECIPE_XFADE_MAP = {
    "black-screen-0.3s": "fadeblack",
    "cross-fade-0.5s": "fade",
    "cross-fade-1.0s": "fade",
    "fade-to-black-1.0s": "fadeblack",
    "film-burn-transition": "fadewhite",
    "glitch-transition": "hlslice",
    "hard-cut-with-whoosh": "hardcut",
    "light-flash-impact": "fadewhite",
    "projector-cue-cinema": "fade",
    "static-noise-transition": "dissolve",
}

HARD_CUT_NAMES = {"hardcut", "hard_cut", "concat", "no_cut", "none"}


def resolve_paths(input_override, clips_override, output_override):
    return {
        "input": Path(input_override) if input_override else Path("assets/concat/clips_concat_only.mp4"),
        "clips_dir": Path(clips_override) if clips_override else Path("assets/clips-atomic"),
        "output": Path(output_override) if output_override else Path("assets/concat/clips_with_effects.mp4"),
    }


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def determine_branch(caps):
    """Capability-aware branch (Pattern 7). Returns 'effects' | 'passthrough'.
    Raises ValueError if video_capabilities missing (Bug #9 — no silent paradigm assumption)."""
    if caps is None:
        raise ValueError(
            "SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). "
            "Cannot infer paradigm — escalate to architect (Bug #9)."
        )
    return "effects" if caps.get("has_layer_2_effects", True) else "passthrough"


def ffprobe_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
     timeout=SUBPROCESS_TIMEOUT_S)
    return float(r.stdout.strip())


def load_recipe(effects_dirs, recipe_id):
    """Search catalog dirs in order for <recipe_id>.json. Returns dict (incl _found_dir +
    xfade_fidelity), or None if not found in any catalog."""
    for d in effects_dirs:
        rp = d / f"{recipe_id}.json"
        if rp.exists():
            data = json.loads(rp.read_text(encoding="utf-8"))
            xname = data.get("xfade_transition") or REAL_RECIPE_XFADE_MAP.get(recipe_id) or "fade"
            return {
                "id": recipe_id,
                "xfade_transition": xname,
                "xfade_fidelity": data.get("xfade_fidelity"),
                "native_mechanism_note": data.get("native_mechanism_note"),
                "duration_s": float(data.get("duration_s", 0.5)),
                "audio_sting_path": data.get("audio_sting_path"),
                "audio_sting_volume": data.get("audio_sting_volume"),
                "_found_dir": d,
            }
    return None


def resolve_boundary_recipe_id(shots, i):
    """Boundary between clip i-1 and i: prefer shot[i-1].transition_out, else shot[i].transition_in."""
    prev_shot, cur_shot = shots[i - 1], shots[i]
    if isinstance(prev_shot, dict) and prev_shot.get("transition_out"):
        return prev_shot["transition_out"]
    if isinstance(cur_shot, dict) and cur_shot.get("transition_in"):
        return cur_shot["transition_in"]
    return None


def resolve_sting(recipe_dir, sting_path):
    """Resolve sting: absolute → use; relative → recipe's own catalog dir parent. None if missing."""
    if not sting_path:
        return None
    p = Path(sting_path)
    if not p.is_absolute():
        p = recipe_dir.parent / sting_path
    return p if p.exists() else None


def build_filtergraph(clips, durs, boundary_recipes,
                      target_w=1080, target_h=1920, target_fps=30):
    """xfade/concat chain filtergraph (V4 empirical cp5-layer2-concat pattern).

    target_w/target_h/target_fps default to horror-choice canonical (1080x1920 / 30) so
    SPECs that omit output_resolution/target_fps render byte-identical to pre-C1 behavior
    (retrocompat MANDATORY, D-editorial-20). Editorial paradigm passes 1920x1080 from
    video_capabilities.output_resolution. Capability-aware (Pattern 7)."""
    fc = []
    for idx in range(len(clips)):
        fc.append(f"[{idx}:v]fps={target_fps},scale={target_w}:{target_h},setsar=1,format=yuv420p,"
                  f"settb=AVTB,setpts=PTS-STARTPTS[v{idx}n]")
        fc.append(f"[{idx}:a]aresample=async=1:first_pts=0,asettb=AVTB,asetpts=PTS-STARTPTS[a{idx}n]")

    last_v, last_a = "v0n", "a0n"
    cum = durs[0]
    boundaries = []

    for i in range(1, len(clips)):
        recipe = boundary_recipes[i - 1]
        vlab, alab = f"v{i}", f"a{i}"
        xname = recipe["xfade_transition"] if recipe else "hardcut"
        d = recipe["duration_s"] if recipe else 0.0

        if xname in HARD_CUT_NAMES or d <= 0.0:
            cut_time = cum
            fc.append(f"[{last_v}][{last_a}][v{i}n][a{i}n]concat=n=2:v=1:a=1[{vlab}][{alab}]")
            cum += durs[i]
            applied, d = "hardcut", 0.0
        else:
            d = max(0.1, d)
            offset = cum - d
            cut_time = cum - d / 2.0
            fc.append(f"[{last_v}][v{i}n]xfade=transition={xname}:duration={d}:offset={offset:.3f}[{vlab}]")
            fc.append(f"[{last_a}][a{i}n]acrossfade=d={d}[{alab}]")
            cum += durs[i] - d
            applied = xname

        boundaries.append({
            "cut_time": round(max(0.0, cut_time), 3),
            "applied": applied,
            "duration_s": round(d, 3),
            "recipe": recipe,
        })
        last_v, last_a = vlab, alab

    return fc, last_v, last_a, boundaries, cum


def run_chain(clips, fc, last_v, last_a, tmp_out, target_fps=30):
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
    for c in clips:
        cmd += ["-i", str(c)]
    cmd += [
        "-filter_complex", ";".join(fc),
        "-map", f"[{last_v}]", "-map", f"[{last_a}]",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-r", str(target_fps),
        str(tmp_out),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)


def overlay_stings(tmp_in, output, sting_jobs):
    """Pass 2: amix stings onto chained audio at boundary cut times. Empty → move tmp_in → output."""
    if not sting_jobs:
        Path(tmp_in).replace(output)
        return subprocess.CompletedProcess([], 0, "", "")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(tmp_in)]
    for path, _vol, _t in sting_jobs:
        cmd += ["-i", str(path)]
    fc = ["[0:a]volume=1.0[base]"]
    mix_labels = ["[base]"]
    for k, (_path, vol, t) in enumerate(sting_jobs, start=1):
        delay_ms = int(max(0.0, t - 0.05) * 1000)
        fc.append(f"[{k}:a]adelay={delay_ms}|{delay_ms},volume={vol}[s{k}]")
        mix_labels.append(f"[s{k}]")
    fc.append(f"{''.join(mix_labels)}amix=inputs={len(mix_labels)}:duration=first:normalize=0[aout]")
    cmd += [
        "-filter_complex", ";".join(fc),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(output),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    Path(tmp_in).unlink(missing_ok=True)
    return r


def write_manifest(output, branch, fmt, clips, shots, boundaries, expected_dur, actual_dur):
    transitions = []
    for i, b in enumerate(boundaries, start=1):
        rec = b["recipe"]
        prev_id = shots[i - 1]["shot_id"] if isinstance(shots[i - 1], dict) else str(shots[i - 1])
        cur_id = shots[i]["shot_id"] if isinstance(shots[i], dict) else str(shots[i])
        transitions.append({
            "from_shot": prev_id,
            "to_shot": cur_id,
            "transition_id": rec["id"] if rec else None,
            "xfade_transition": b["applied"],
            "xfade_fidelity": (rec.get("xfade_fidelity") if rec else None),
            "duration_s": b["duration_s"],
            "cut_time_s": b["cut_time"],
            "sting_path": (rec.get("audio_sting_path") if rec else None),
            "sting_volume": (rec.get("audio_sting_volume") if rec else None),
        })
    unique = sorted({t["transition_id"] for t in transitions if t["transition_id"]})
    manifest = {
        "stage": "layer2_effects",
        "branch": branch,
        "format": fmt,
        "clips_count": len(clips),
        "boundaries_count": len(boundaries),
        "unique_transition_types": unique,
        "approximate_fidelity_used": sorted({
            t["transition_id"] for t in transitions if t.get("xfade_fidelity") == "approximate"
        }),
        "expected_duration_s": round(expected_dur, 3) if expected_dur is not None else None,
        "actual_duration_s": round(actual_dur, 3) if actual_dur is not None else None,
        "output": str(output),
        "transitions": transitions,
    }
    mpath = output.parent / f"{output.stem}_manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="Format name (e.g., horror-choice). REQUIRED — no silent assumption.")
    parser.add_argument("--spec", required=True, help="Path to SPEC.yaml (video_capabilities mandatory)")
    parser.add_argument("--input", default=None,
                        help="4.2 concat output for passthrough (default: assets/concat/clips_concat_only.mp4)")
    parser.add_argument("--clips-dir", default=None, help="Atomic clips dir (default: assets/clips-atomic)")
    parser.add_argument("--output", default=None,
                        help="Output mp4 (default: assets/concat/clips_with_effects.mp4)")
    parser.add_argument("--effects-dir", nargs="+", default=None,
                        help="One or more transition catalog dirs (Capa A primitives + format Capa B). "
                             "Searched in order. REQUIRED in effects branch (no silent format default).")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved paths + branch, exit 0")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    paths = resolve_paths(args.input, args.clips_dir, args.output)
    spec = normalize_transitions(load_spec(spec_path))   # PRE-4.J adapter: legacy transitions[] → per-shot
    caps = spec.get("video_capabilities")
    shots = spec.get("shot_list", []) or []

    try:
        branch = determine_branch(caps)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    effects_dirs = [Path(x) for x in args.effects_dir] if args.effects_dir else None
    boundary_recipe_ids = [resolve_boundary_recipe_id(shots, i) for i in range(1, len(shots))]

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"input(passthrough_src): {paths['input']}")
        print(f"clips_dir: {paths['clips_dir']}")
        print(f"output: {paths['output']}")
        print(f"effects_dirs: {[str(d) for d in effects_dirs] if effects_dirs else None}")
        print(f"capability_branch: {branch}")
        print(f"has_layer_2_effects: {caps.get('has_layer_2_effects', True)}")
        print(f"shot_count: {len(shots)}")
        print(f"boundary_transition_ids: {boundary_recipe_ids}")
        return 0

    output = paths["output"]
    output.parent.mkdir(parents=True, exist_ok=True)

    # ── PASSTHROUGH branch ────────────────────────────────────────────────
    if branch == "passthrough":
        inp = paths["input"]
        if not inp.exists():
            print(f"ERROR: passthrough input not found: {inp}", file=sys.stderr)
            return 1
        r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                            "-i", str(inp), "-c", "copy", str(output)], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
        if r.returncode != 0:
            print(f"ERROR: passthrough copy failed: {r.stderr[:300]}", file=sys.stderr)
            return 1
        write_manifest(output, "passthrough", args.format, [inp], shots, [], None,
                       ffprobe_duration(output))
        print(f"✅ passthrough (has_layer_2_effects=false): {inp} → {output}")
        return 0

    # ── EFFECTS branch ────────────────────────────────────────────────────
    if effects_dirs is None:
        print("ERROR: --effects-dir REQUIRED in effects branch (one or more catalog dirs: "
              "Capa A primitives + format Capa B). No silent format default (agnostic-by-design).",
              file=sys.stderr)
        return 2

    clips, missing = [], []
    for shot in shots:
        sid = shot["shot_id"] if isinstance(shot, dict) else str(shot)
        c = paths["clips_dir"] / f"{sid}_atomic.mp4"
        (clips if c.exists() else missing).append(c if c.exists() else str(c))
    if missing:
        print(f"ERROR: {len(missing)} atomic clip(s) missing: {missing[:3]}", file=sys.stderr)
        return 1
    if len(clips) < 2:
        print("ERROR: effects branch needs ≥2 atomic clips", file=sys.stderr)
        return 1

    boundary_recipes = []
    for rid in boundary_recipe_ids:
        rec = load_recipe(effects_dirs, rid) if rid else None
        if rid and rec is None:
            print(f"⚠️ recipe '{rid}' not found in {[str(d) for d in effects_dirs]} — hard-cut fallback",
                  file=sys.stderr)
        if rec and rec.get("xfade_fidelity") == "approximate":
            note = (rec.get("native_mechanism_note") or "")[:90]
            print(f"⚠️ WARNING: recipe '{rec['id']}' xfade_fidelity=approximate — chained-xfade is LOSSY "
                  f"({note}). Production use flagged; full fidelity = Option B hybrid dispatch (GAPS-LOG).",
                  file=sys.stderr)
        boundary_recipes.append(rec)

    durs = [ffprobe_duration(c) for c in clips]
    # C1 (D-editorial-20): output dims/fps from capabilities. Defaults = horror-choice
    # canonical (1080x1920 / 30) → byte-identical when flags absent (retrocompat).
    res = str((caps or {}).get("output_resolution", "1080x1920")).lower()
    try:
        target_w, target_h = (int(x) for x in res.split("x"))
    except ValueError:
        print(f"WARNING: output_resolution '{res}' unparseable — defaulting 1080x1920.", file=sys.stderr)
        target_w, target_h = 1080, 1920
    target_fps = int((caps or {}).get("target_fps", 30))
    fc, last_v, last_a, boundaries, expected_dur = build_filtergraph(
        clips, durs, boundary_recipes, target_w, target_h, target_fps)

    tmp_out = output.parent / f"{output.stem}.nosting.mp4"
    r = run_chain(clips, fc, last_v, last_a, tmp_out, target_fps)
    if r.returncode != 0:
        print(f"ERROR: xfade chain failed: {r.stderr[-500:]}", file=sys.stderr)
        return 1

    sting_jobs = []
    for b in boundaries:
        rec = b["recipe"]
        if rec and rec.get("audio_sting_path") and rec.get("audio_sting_volume") is not None:
            spath = resolve_sting(rec["_found_dir"], rec["audio_sting_path"])
            if spath:
                sting_jobs.append((spath, rec["audio_sting_volume"], b["cut_time"]))
            else:
                print(f"⚠️ sting not found for {rec['id']}: {rec['audio_sting_path']} "
                      f"(recorded in manifest, not overlaid)", file=sys.stderr)
    r2 = overlay_stings(tmp_out, output, sting_jobs)
    if r2.returncode != 0:
        print(f"ERROR: sting overlay failed: {r2.stderr[-500:]}", file=sys.stderr)
        return 1

    actual_dur = ffprobe_duration(output)
    manifest = write_manifest(output, "effects", args.format, clips, shots, boundaries,
                              expected_dur, actual_dur)
    print(f"✅ effects applied: {len(clips)} clips, {manifest['boundaries_count']} boundaries, "
          f"{len(manifest['unique_transition_types'])} unique types → {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
