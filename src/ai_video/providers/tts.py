"""
Generate narration MP3 via ElevenLabs for narration.

Usage:
    .venv/bin/python scripts/tts.py                              # reads script.txt, writes narration.mp3
    .venv/bin/python scripts/tts.py -i script.txt -o out.mp3
    .venv/bin/python scripts/tts.py -t "Frase corta a narrar"
    .venv/bin/python scripts/tts.py --model eleven_v3            # for expressive delivery

Defaults: catalogued default voice, Spanish, highest-quality multilingual_v2.
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import ElevenLabs

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Source of truth: library/voices-catalog.json `default_voice` (Hard rule #19).
# `Tj9l48J9AJbry5yCP5eW` quedó DEPRECATED 2026-05-18 (refutado en listen-test matadero CP2).
DEFAULT_VOICE_ID = "2gPFXx8pN3Avh27Dw5Ma"
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_LANG = "es"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_INPUT = PROJECT_ROOT / "script.txt"
DEFAULT_OUTPUT = PROJECT_ROOT / "narration.mp3"


def read_text(text_arg: str | None, input_path: Path) -> str:
    if text_arg:
        return text_arg
    if not input_path.exists():
        sys.exit(f"error: input file not found: {input_path}")
    return input_path.read_text(encoding="utf-8").strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="ElevenLabs TTS")
    parser.add_argument("-t", "--text", help="Inline text (overrides --input)")
    parser.add_argument("-i", "--input", type=Path, default=DEFAULT_INPUT, help="Input .txt file")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT, help="Output .mp3 path")
    parser.add_argument("-v", "--voice-id", default=DEFAULT_VOICE_ID)
    parser.add_argument(
        "-m",
        "--model",
        default=DEFAULT_MODEL,
        choices=["eleven_multilingual_v2", "eleven_v3", "eleven_flash_v2_5"],
        help="eleven_multilingual_v2 = default/highest quality; eleven_v3 = expressive",
    )
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG, help="Language code (default: es)")
    parser.add_argument("--stability", type=float, default=0.5)
    parser.add_argument("--similarity", type=float, default=0.75)
    parser.add_argument("--style", type=float, default=0.0)
    parser.add_argument("--speed", type=float, default=1.0)
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("error: ELEVENLABS_API_KEY not found in .env")

    text = read_text(args.text, args.input)
    if not text:
        sys.exit("error: empty text input")

    client = ElevenLabs(api_key=api_key)
    audio = client.text_to_speech.convert(
        voice_id=args.voice_id,
        text=text,
        model_id=args.model,
        language_code=args.lang,
        output_format=DEFAULT_OUTPUT_FORMAT,
        voice_settings={
            "stability": args.stability,
            "similarity_boost": args.similarity,
            "style": args.style,
            "use_speaker_boost": True,
            "speed": args.speed,
        },
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    size_kb = args.output.stat().st_size / 1024
    print(f"wrote {args.output} ({size_kb:.1f} KB, model={args.model}, voice={args.voice_id})")


if __name__ == "__main__":
    main()
