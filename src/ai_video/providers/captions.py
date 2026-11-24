"""
Auto-generate GSAP caption timing from narration audio.

Uses Whisper to transcribe audio with word-level timestamps, then
groups words into caption segments and outputs ready-to-paste GSAP set() calls.

Usage:
    # Single file
    .venv/bin/python scripts/captions.py -a assets/h3-narr1-raw.mp3 -t 22.7

    # Batch from a JSON spec
    .venv/bin/python scripts/captions.py --spec captions-spec.json

Output:
    GSAP tl.set() / tl.to() calls printed to stdout, ready to paste into index.html.

Dependencies:
    pip install openai-whisper
    (ffmpeg must be on PATH)
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import whisper
except ImportError:
    sys.exit(
        "error: openai-whisper not installed.\n"
        "Run: .venv/bin/pip install openai-whisper"
    )


MAX_WORDS_PER_CAPTION = 6   # max words before splitting a new caption
MIN_GAP_S = 0.08            # minimum silence gap to force a split
FADE_DURATION = 0.0         # instant set (no fade) — keep captions sharp


def transcribe(audio_path: Path) -> list[dict]:
    """Return list of {word, start, end} dicts via Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(
        str(audio_path),
        language="es",
        word_timestamps=True,
        verbose=False,
    )
    words = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            words.append({"word": w["word"].strip(), "start": w["start"], "end": w["end"]})
    return words


def group_into_captions(words: list[dict]) -> list[dict]:
    """
    Group words into caption segments respecting MAX_WORDS_PER_CAPTION
    and splitting on punctuation boundaries (., ?, !, :).
    Returns list of {text, start, end}.
    """
    if not words:
        return []

    captions = []
    current_words = []
    current_start = words[0]["start"]

    for i, w in enumerate(words):
        current_words.append(w["word"])
        is_boundary = bool(re.search(r"[.!?:]$", w["word"]))
        is_gap = (
            i + 1 < len(words)
            and (words[i + 1]["start"] - w["end"]) >= MIN_GAP_S
        )
        at_max = len(current_words) >= MAX_WORDS_PER_CAPTION

        if is_boundary or is_gap or at_max or i == len(words) - 1:
            captions.append({
                "text": " ".join(current_words).upper().strip(),
                "start": round(current_start, 3),
                "end": round(w["end"], 3),
            })
            if i + 1 < len(words):
                current_start = words[i + 1]["start"]
            current_words = []

    return captions


def emit_gsap(captions: list[dict], element_id: str, audio_offset: float) -> str:
    """
    Emit GSAP set() calls for a list of captions.
    audio_offset = the data-start value of the audio clip in the composition.
    """
    lines = [f"      /* captions for #{element_id} (offset={audio_offset}s) */"]
    for cap in captions:
        t_on  = round(audio_offset + cap["start"], 3)
        t_off = round(audio_offset + cap["end"] + 0.05, 3)  # tiny hold after end
        lines.append(f'      tl.set("#{element_id}", {{ opacity: 1, innerHTML: "{cap["text"]}" }}, {t_on});')
        lines.append(f'      tl.set("#{element_id}", {{ opacity: 0 }}, {t_off});')
    return "\n".join(lines)


def process_single(audio_path: Path, offset: float, element_id: str) -> None:
    print(f"\n[captions.py] transcribing {audio_path.name}...", file=sys.stderr)
    words = transcribe(audio_path)
    captions = group_into_captions(words)

    print(f"[captions.py] {len(captions)} caption segments:", file=sys.stderr)
    for c in captions:
        print(f"  [{c['start']:.2f}–{c['end']:.2f}] {c['text']}", file=sys.stderr)

    print("\n" + emit_gsap(captions, element_id, offset))


def process_spec(spec_path: Path) -> None:
    """
    spec JSON format:
    [
      {"audio": "assets/h3-narr1-raw.mp3", "offset": 22.7, "element": "h3-cap-narr1"},
      ...
    ]
    """
    spec = json.loads(spec_path.read_text())
    for entry in spec:
        audio_path = spec_path.parent / entry["audio"]
        process_single(audio_path, entry["offset"], entry["element"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Auto-generate GSAP captions from narration audio")
    parser.add_argument("-a", "--audio", type=Path, help="Single audio file")
    parser.add_argument("-t", "--offset", type=float, default=0.0,
                        help="data-start offset of this audio clip in the composition")
    parser.add_argument("-e", "--element", default="cap-narr",
                        help="CSS id of the caption <div> element")
    parser.add_argument("--spec", type=Path, help="JSON batch spec file")
    args = parser.parse_args()

    if args.spec:
        process_spec(args.spec)
    elif args.audio:
        process_single(args.audio, args.offset, args.element)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
