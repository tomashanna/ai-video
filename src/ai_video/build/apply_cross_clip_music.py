#!/usr/bin/env python3
"""
apply-cross-clip-music.py — Paso 4.3: Layer 3 cross-clip music + sidechain duck + final master.

Bottom-up Paso 4 sequence step 3 (4.2 → 4.4 → 4.3 → 4.1 per PRE-4.D verdict).
Consumes the 4.4 output (clips_with_effects.mp4 — clip audio + effect stings) and overlays
the continuous Layer 3 audio (narrator master + music layers + ambient), ducks layers 1+2
under narrator VO, and applies the final master loudnorm.

Architecture — PIPELINE §13.7.5 / §13.9.1 LAYER 3 (post-concat continuous overlay):
  music_continuous_layers[] (SPEC) → <music-dir>/<layer_id>.mp3 → amix music_bed
  narrator master (Layer 3 VO) → sidechain key (layers 1+2 duck UNDER it)
  final master loudnorm -14 ±0.5 LUFS / -1 ±0.3 dBTP (two-pass for accuracy)

PRE-4.C tolerance bands: final master LUFS CANONICAL-ANCHORED to F1 (-14.06 ±0.41); sidechain
duck dB + dBTP headroom SPEC-DECLARED (plumbing).

Capability-aware (Pattern 7, PIPELINE §13.10):
  video_capabilities missing               → Bug #9 (exit 2)
  audio_mix_target: none                    → passthrough (copy, no master)
  has_layer_3_music: false                  → master_only (final master input, no music)
  else                                      → full (music mix + duck + master)
  has_tts_narration: false OR no narrator   → full branch without sidechain duck

Agnostic-by-design: --format REQUIRED (no silent assumption).

Usage:
    python apply-cross-clip-music.py --format <fmt> --spec <path> [--input <4.4.mp4>] \\
        [--music-dir <p>] [--narrator <mp3>] [--output <p>]
    python apply-cross-clip-music.py --format horror-choice --spec <path> --dry-run

Output: <output> (default assets/final/master_final.mp4) + sidecar manifest JSON.

Build Paso 4.3 (2026-05-27) — TDD + Hard Rule #26 companion test.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

TARGET_LUFS = -14.0          # canonical-anchored F1 (-14.06 ±0.41)
TARGET_TP = -1.0             # SPEC-declared headroom
TARGET_LRA = 11.0
DEFAULT_DUCK_DB = -8.0       # PRE-4.C sidechain duck (SPEC-declared plumbing)


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def determine_branch(caps):
    """Pattern 7 branch. Raises ValueError if video_capabilities missing (Bug #9)."""
    if caps is None:
        raise ValueError(
            "SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). "
            "Cannot infer paradigm — escalate to architect (Bug #9)."
        )
    if caps.get("audio_mix_target") == "none":
        return "passthrough"
    if not caps.get("has_layer_3_music", True):
        return "master_only"
    return "full"


def ffprobe_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def resolve_music_files(music_dir, layers):
    found, missing = [], []
    for layer in layers:
        lid = layer.get("layer_id") if isinstance(layer, dict) else str(layer)
        f = music_dir / f"{lid}.mp3"
        (found if f.exists() else missing).append(f if f.exists() else lid)
    return found, missing


def build_mix(input_video, music_files, narrator, out_wav):
    """Build Layer 3 mix (clip audio + music + narrator, music/clip ducked under narrator).
    Returns (returncode, stderr, duck_applied).

    The final mix is padded with apad=whole_dur to the FULL video duration before output: amix ends
    at the longest INPUT, so if narrator/music end before the video the audio cola se corta (the V7
    audio-tail fix — and per HR#16 data-duration > clip → negro). apad guarantees coverage [0,dur]."""
    vdur = ffprobe_duration(input_video)
    inputs = ["-i", str(input_video)]
    fc = []
    narr_idx = None
    music_start = 1
    if narrator:
        inputs += ["-i", str(narrator)]
        narr_idx = 1
        music_start = 2
    music_labels = []
    for k, mf in enumerate(music_files):
        inputs += ["-i", str(mf)]
        music_labels.append(f"[{music_start + k}:a]")

    # music_bed
    if len(music_labels) == 0:
        music_bed = None
    elif len(music_labels) == 1:
        fc.append(f"{music_labels[0]}anull[music]")
        music_bed = "[music]"
    else:
        fc.append(f"{''.join(music_labels)}amix=inputs={len(music_labels)}:duration=longest:normalize=0[music]")
        music_bed = "[music]"

    duck_applied = False
    if narr_idx is not None:
        # bed = clip audio + music, ducked under narrator; narrator on top
        if music_bed:
            fc.append(f"[0:a]{music_bed}amix=inputs=2:duration=longest:normalize=0[bed]")
        else:
            fc.append("[0:a]anull[bed]")
        fc.append(f"[{narr_idx}:a]asplit=2[nkey][nmix]")
        fc.append("[bed][nkey]sidechaincompress=threshold=0.05:ratio=8:attack=20:release=300[bedduck]")
        fc.append("[nmix][bedduck]amix=inputs=2:duration=longest:normalize=0[mixraw]")
        duck_applied = True
    else:
        if music_bed:
            fc.append(f"[0:a]{music_bed}amix=inputs=2:duration=longest:normalize=0[mixraw]")
        else:
            fc.append("[0:a]anull[mixraw]")

    # pad the final bus to the full video duration so the audio tail is never truncated (V7 fix).
    if vdur:
        fc.append(f"[mixraw]apad=whole_dur={vdur:.3f},atrim=0:{vdur:.3f},asetpts=N/SR/TB[mixout]")
    else:
        fc.append("[mixraw]apad=pad_dur=0.05,asetpts=N/SR/TB[mixout]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs + [
        "-filter_complex", ";".join(fc), "-map", "[mixout]",
        "-c:a", "pcm_s16le", "-ar", "48000", str(out_wav),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    return r.returncode, r.stderr, duck_applied


def loudnorm_measure(audio_src):
    r = subprocess.run([
        "ffmpeg", "-i", str(audio_src),
        "-af", f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json",
        "-f", "null", "-",
    ], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    err = r.stderr
    start = err.rfind("{")
    end = err.rfind("}")
    if start == -1 or end == -1 or end < start:
        return None
    try:
        return json.loads(err[start:end + 1])
    except json.JSONDecodeError:
        return None


def loudnorm_apply(audio_src, m, out_wav):
    af = (f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}"
          f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true:print_format=summary")
    r = subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(audio_src),
        "-af", af, "-ar", "48000", "-c:a", "pcm_s16le", str(out_wav),
    ], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    return r.returncode, r.stderr


def mux(input_video, mastered_audio, output):
    r = subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(input_video), "-i", str(mastered_audio),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000", str(output),
    ], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    return r.returncode, r.stderr


def master_audio_source(audio_src, output_video, mux_video, tmpdir):
    """Two-pass loudnorm of audio_src; mux onto mux_video → output_video. Returns (rc, stderr)."""
    m = loudnorm_measure(audio_src)
    if m is None:
        return 1, "loudnorm measure failed (no JSON)"
    master_wav = Path(tmpdir) / "_master.wav"
    rc, err = loudnorm_apply(audio_src, m, master_wav)
    if rc != 0:
        return rc, f"loudnorm apply failed: {err[-300:]}"
    return mux(mux_video, master_wav, output_video)


def write_manifest(output, branch, fmt, music_count, duck_db, narrator_used,
                   input_dur, output_dur):
    manifest = {
        "stage": "layer3_master",
        "branch": branch,
        "format": fmt,
        "music_layers_count": music_count,
        "narrator_used": narrator_used,
        "sidechain_duck_db": duck_db,
        "target_lufs": TARGET_LUFS,
        "target_tp": TARGET_TP,
        "input_duration_s": round(input_dur, 3) if input_dur else None,
        "output_duration_s": round(output_dur, 3) if output_dur else None,
        "output": str(output),
    }
    mpath = output.parent / f"{output.stem}_manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="Format name. REQUIRED — no silent assumption.")
    parser.add_argument("--spec", required=True, help="SPEC.yaml (video_capabilities + music_continuous_layers)")
    parser.add_argument("--input", default=None,
                        help="4.4 output (default: assets/concat/clips_with_effects.mp4)")
    parser.add_argument("--music-dir", default=None, help="Music layer mp3 dir (default: assets/music)")
    parser.add_argument("--narrator", default=None,
                        help="Narrator master mp3 (default: assets/narration/narrator_master.mp3)")
    parser.add_argument("--output", default=None, help="Output (default: assets/final/master_final.mp4)")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved paths + branch, exit 0")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    input_path = Path(args.input) if args.input else Path("assets/concat/clips_with_effects.mp4")
    music_dir = Path(args.music_dir) if args.music_dir else Path("assets/music")
    narrator = Path(args.narrator) if args.narrator else Path("assets/narration/narrator_master.mp3")
    output = Path(args.output) if args.output else Path("assets/final/master_final.mp4")

    spec = load_spec(spec_path)
    caps = spec.get("video_capabilities")
    layers = spec.get("music_continuous_layers", []) or []

    try:
        branch = determine_branch(caps)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    has_tts = bool(caps.get("has_tts_narration", True)) if caps else False
    narrator_available = has_tts and narrator.exists()

    if args.dry_run:
        print(f"format: {args.format}")
        print(f"input: {input_path}")
        print(f"music_dir: {music_dir}")
        print(f"narrator: {narrator} (available={narrator_available})")
        print(f"output: {output}")
        print(f"capability_branch: {branch}")
        print(f"has_layer_3_music: {caps.get('has_layer_3_music', True)}")
        print(f"music_layers_declared: {[l.get('layer_id') if isinstance(l, dict) else l for l in layers]}")
        return 0

    if not input_path.exists():
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    in_dur = ffprobe_duration(input_path)

    # ── PASSTHROUGH ───────────────────────────────────────────────────────
    if branch == "passthrough":
        r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                            "-i", str(input_path), "-c", "copy", str(output)],
                           capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
        if r.returncode != 0:
            print(f"ERROR: passthrough copy failed: {r.stderr[:300]}", file=sys.stderr)
            return 1
        write_manifest(output, "passthrough", args.format, 0, None, False,
                       in_dur, ffprobe_duration(output))
        print(f"✅ passthrough (audio_mix_target=none): {input_path} → {output}")
        return 0

    with tempfile.TemporaryDirectory() as td:
        # ── MASTER_ONLY ───────────────────────────────────────────────────
        if branch == "master_only":
            rc, err = master_audio_source(input_path, output, input_path, td)
            if rc != 0:
                print(f"ERROR: master_only failed: {err[-300:]}", file=sys.stderr)
                return 1
            write_manifest(output, "master_only", args.format, 0, None, False,
                           in_dur, ffprobe_duration(output))
            print(f"✅ master_only (has_layer_3_music=false): mastered → {output}")
            return 0

        # ── FULL ──────────────────────────────────────────────────────────
        music_files, missing = resolve_music_files(music_dir, layers)
        if missing:
            print(f"⚠️ music layer(s) missing in {music_dir}: {missing}", file=sys.stderr)
        if not music_files:
            print("⚠️ no music layer files found — degrading to master_only", file=sys.stderr)
            rc, err = master_audio_source(input_path, output, input_path, td)
            if rc != 0:
                print(f"ERROR: master degrade failed: {err[-300:]}", file=sys.stderr)
                return 1
            write_manifest(output, "master_only", args.format, 0, None, narrator_available,
                           in_dur, ffprobe_duration(output))
            print(f"✅ master_only (no music files): mastered → {output}")
            return 0

        narr = narrator if narrator_available else None
        mix_wav = Path(td) / "_mix.wav"
        rc, err, duck_applied = build_mix(input_path, music_files, narr, mix_wav)
        if rc != 0:
            print(f"ERROR: Layer 3 mix failed: {err[-400:]}", file=sys.stderr)
            return 1
        rc, err = master_audio_source(mix_wav, output, input_path, td)
        if rc != 0:
            print(f"ERROR: full master failed: {err[-300:]}", file=sys.stderr)
            return 1

        out_dur = ffprobe_duration(output)
        duck_db = DEFAULT_DUCK_DB if duck_applied else None
        manifest = write_manifest(output, "full", args.format, len(music_files), duck_db,
                                  narrator_available, in_dur, out_dur)
        print(f"✅ full Layer 3: {len(music_files)} music layers, narrator={narrator_available}, "
              f"duck={duck_db}dB, master -14 LUFS → {output}")
        return 0


if __name__ == "__main__":
    sys.exit(main())
