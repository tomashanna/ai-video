"""
Generate sound effects via ElevenLabs Text-to-Sound-Effects API.

Usage:
    python scripts/sfx.py -t "low impactful horror whoosh sub-bass" -d 1.5 -o assets/sfx/whoosh.mp3
    python scripts/sfx.py -t "..." -d 4 -i 0.6 --loop -o assets/sfx/loop.mp3
    python scripts/sfx.py --spec sfx-spec.json   # batch mode

Spec JSON shape (batch):
    [{"out": "assets/sfx/h1-howl.mp3", "text": "distant howl...", "duration": 3.0, "influence": 0.3, "loop": false}, ...]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def generate_one(client, *, text, duration, influence, loop, out_path, model_id=None):
    kwargs = dict(text=text, output_format=DEFAULT_OUTPUT_FORMAT)
    if duration is not None:
        kwargs["duration_seconds"] = duration
    if influence is not None:
        kwargs["prompt_influence"] = influence
    if loop:
        kwargs["loop"] = True
    if model_id:
        kwargs["model_id"] = model_id

    audio = client.text_to_sound_effects.convert(**kwargs)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return out_path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description="ElevenLabs Sound Effects generator")
    parser.add_argument("-t", "--text", help="Prompt for the SFX")
    parser.add_argument("-d", "--duration", type=float, help="Duration in seconds (0.5-22)")
    parser.add_argument("-i", "--influence", type=float, help="prompt_influence 0-1 (default ~0.3)")
    parser.add_argument("--loop", action="store_true", help="Generate as a perfect loop")
    parser.add_argument("--model", help="model_id override (default eleven_text_to_sound_v2)")
    parser.add_argument("-o", "--output", type=Path, help="Output mp3 path")
    parser.add_argument("--spec", type=Path, help="Batch mode: JSON list of jobs")
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("error: ELEVENLABS_API_KEY not found in .env")

    client = ElevenLabs(api_key=api_key)

    if args.spec:
        jobs = json.loads(args.spec.read_text())
        ok = 0
        for job in jobs:
            out = Path(job["out"])
            if not out.is_absolute():
                out = PROJECT_ROOT / out
            print(f"[gen] {out.relative_to(PROJECT_ROOT)}  ({job.get('duration', '?')}s)", flush=True)
            try:
                size = generate_one(
                    client,
                    text=job["text"],
                    duration=job.get("duration"),
                    influence=job.get("influence"),
                    loop=job.get("loop", False),
                    out_path=out,
                    model_id=args.model,
                )
                print(f"      wrote {size/1024:.1f} KB", flush=True)
                ok += 1
            except Exception as e:
                print(f"      FAILED: {e}", file=sys.stderr, flush=True)
            time.sleep(0.4)
        print(f"\n{ok}/{len(jobs)} generated")
        return

    if not args.text or not args.output:
        sys.exit("error: -t and -o are required (or use --spec)")

    out = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    size = generate_one(
        client,
        text=args.text,
        duration=args.duration,
        influence=args.influence,
        loop=args.loop,
        out_path=out,
        model_id=args.model,
    )
    print(f"wrote {out} ({size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
