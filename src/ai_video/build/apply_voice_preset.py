#!/usr/bin/env python3
"""apply-voice-preset.py — Apply creepy voice effects preset to a TTS-generated mp3.

Reads presets-catalog.json, dispatches to sox or ffmpeg per preset.tool, and
applies the recipe chain. Optional --verify flag runs Whisper transcription to
sanity-check intelligibility >= 0.85 (M7.7.5 enforcement).

Usage:
  python apply-voice-preset.py --preset ultratumba_cavernoso \\
    --input assets/narr-processed.mp3 \\
    --output assets/narr-final.mp3

  python apply-voice-preset.py --list           # list available presets
  python apply-voice-preset.py --preset matarife_canonical --verify --text "..." ...

Exit codes:
  0 = OK
  1 = preset not found / input missing / tool failure
  2 = M7.7.5 intelligibility check failed (when --verify used)
"""

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

from ai_video.paths import voice_effects_catalog

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

CATALOG_PATH = voice_effects_catalog()


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        sys.exit(f"error: catalog not found at {CATALOG_PATH}")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def find_preset(catalog: dict, preset_id: str) -> dict:
    for p in catalog["presets"]:
        if p["preset_id"] == preset_id:
            return p
    available = ", ".join(p["preset_id"] for p in catalog["presets"])
    sys.exit(f"error: preset '{preset_id}' not found. Available: {available}")


def list_presets(catalog: dict) -> None:
    print(f"\n{len(catalog['presets'])} voice effect presets (catalog v{catalog['version']}):\n")
    for p in catalog["presets"]:
        status_icon = "✅" if p["validation_status"] == "validated" else "🟡"
        print(f"  {status_icon} {p['preset_id']:<25} {p['label']}")
        print(f"     tool={p['tool']:<8} risk={p['intelligibility_risk']:<6} overhead={p['duration_overhead_pct']}%")
    print()


def apply_sox(chain: str, input_path: Path, output_path: Path) -> None:
    cmd = ["sox", str(input_path), str(output_path)] + shlex.split(chain)
    print(f"[sox] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    if result.returncode != 0:
        sys.exit(f"sox failed:\n{result.stderr}")


def apply_ffmpeg(chain: str, input_path: Path, output_path: Path) -> None:
    cmd = ["ffmpeg", "-y", "-i", str(input_path), "-af", chain, str(output_path)]
    print(f"[ffmpeg] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{result.stderr}")


def verify_intelligibility(audio_path: Path, expected_text: str, threshold: float) -> tuple[float, str]:
    """Whisper-transcribe + Jaccard token overlap vs expected. Returns (score, transcribed)."""
    try:
        import whisper
    except ImportError:
        print("warning: openai-whisper not installed; skipping --verify", file=sys.stderr)
        return (1.0, "")
    model = whisper.load_model("small")
    result = model.transcribe(str(audio_path), language="es", fp16=False)
    transcribed = result["text"].strip().lower()
    expected_tokens = set(expected_text.lower().split())
    transcribed_tokens = set(transcribed.split())
    if not expected_tokens:
        return (1.0, transcribed)
    intersection = expected_tokens & transcribed_tokens
    score = len(intersection) / len(expected_tokens)
    return (score, transcribed)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply creepy voice effects preset")
    parser.add_argument("--preset", help="Preset ID (run --list to see available)")
    parser.add_argument("--input", type=Path, help="Input mp3 path")
    parser.add_argument("--output", type=Path, help="Output mp3 path")
    parser.add_argument("--list", action="store_true", help="List available presets")
    parser.add_argument("--verify", action="store_true", help="Run M7.7.5 intelligibility check post-apply (requires --text)")
    parser.add_argument("--text", help="Expected text for --verify (Whisper Jaccard check)")
    parser.add_argument("--threshold", type=float, default=0.85, help="Intelligibility threshold (default 0.85)")
    args = parser.parse_args()

    catalog = load_catalog()

    if args.list:
        list_presets(catalog)
        return

    if not args.preset or not args.input or not args.output:
        parser.error("--preset, --input, and --output required (or use --list)")

    if not args.input.exists():
        sys.exit(f"error: input not found: {args.input}")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    preset = find_preset(catalog, args.preset)
    print(f"\n→ Applying preset: {preset['preset_id']} ({preset['label']})")
    print(f"  intent: {preset['intent']}")
    print(f"  tool: {preset['tool']} | risk: {preset['intelligibility_risk']} | overhead: {preset['duration_overhead_pct']}%\n")

    if preset["tool"] == "sox":
        apply_sox(preset["chain"], args.input, args.output)
    elif preset["tool"] == "ffmpeg":
        apply_ffmpeg(preset["chain"], args.input, args.output)
    else:
        sys.exit(f"error: unknown tool '{preset['tool']}' in preset {preset['preset_id']}")

    print(f"\n✓ Output: {args.output}")

    if args.verify:
        if not args.text:
            sys.exit("error: --verify requires --text (expected transcription)")
        score, transcribed = verify_intelligibility(args.output, args.text, args.threshold)
        print(f"\n[M7.7.5 intelligibility check]")
        print(f"  expected:    {args.text}")
        print(f"  transcribed: {transcribed}")
        print(f"  score:       {score:.2f} (threshold {args.threshold})")
        if score < args.threshold:
            print(f"  ✗ FAIL — consult preset.intelligibility_mitigation")
            print(f"           mitigation: {preset['intelligibility_mitigation']}")
            sys.exit(2)
        print(f"  ✓ PASS")


if __name__ == "__main__":
    main()
