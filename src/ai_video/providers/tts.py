"""Generate narration audio with ElevenLabs text-to-speech.

Usage:
    ai-video tts                                  # reads ./script.txt, writes ./narration.mp3
    ai-video tts -i script.txt -o out.mp3
    ai-video tts -t "Frase corta a narrar"
    ai-video tts --model eleven_v3                # expressive delivery
    ai-video tts -t "..." --dry-run               # validate + estimate cost, no API call

The default voice is the catalogued ``default_voice`` in ``assets/library/voices-catalog.json``.
Every call is checked against the spend budget (``AIVIDEO_BUDGET_USD``) and retried with
exponential backoff on transient errors.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_video import budget
from ai_video.config import get_settings
from ai_video.errors import AIVideoError
from ai_video.log import get_logger
from ai_video.retry import retry_call

log = get_logger(__name__)

FALLBACK_VOICE_ID = "2gPFXx8pN3Avh27Dw5Ma"
MODELS = ("eleven_multilingual_v2", "eleven_v3", "eleven_flash_v2_5")
DEFAULT_MODEL = "eleven_multilingual_v2"
DEFAULT_LANG = "es"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
MAX_CHARS = 10_000  # ElevenLabs per-request limit for multilingual_v2


def default_voice_id() -> str:
    """Voice id from the catalog (single source of truth), with a safe fallback."""
    try:
        from ai_video.paths import library_dir

        data = json.loads((library_dir() / "voices-catalog.json").read_text(encoding="utf-8"))
        voice = data.get("default_voice")
        if isinstance(voice, str) and voice:
            return voice
    except (OSError, ValueError, AIVideoError):
        pass
    return FALLBACK_VOICE_ID


@dataclass(frozen=True)
class TTSRequest:
    text: str
    voice_id: str
    model: str = DEFAULT_MODEL
    lang: str = DEFAULT_LANG
    stability: float = 0.5
    similarity: float = 0.75
    style: float = 0.0
    speed: float = 1.0

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError("empty text input")
        if len(self.text) > MAX_CHARS:
            raise ValueError(f"text is {len(self.text)} chars; split it (max {MAX_CHARS} per request)")
        if self.model not in MODELS:
            raise ValueError(f"unknown model {self.model!r}; choose one of {MODELS}")
        for name in ("stability", "similarity", "style"):
            v = getattr(self, name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{name} must be within [0, 1], got {v}")
        if not 0.7 <= self.speed <= 1.2:
            raise ValueError(f"speed must be within [0.7, 1.2], got {self.speed}")

    def estimated_cost(self) -> float:
        return budget.estimate("elevenlabs_tts_per_1k_chars", len(self.text) / 1000)


def read_text(text_arg: str | None, input_path: Path) -> str:
    if text_arg:
        return text_arg
    if not input_path.exists():
        raise FileNotFoundError(f"input file not found: {input_path}")
    return input_path.read_text(encoding="utf-8").strip()


def write_chunks(chunks: Iterable[bytes], output: Path) -> int:
    """Stream audio chunks to ``output`` atomically; returns bytes written."""
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".part")
    n = 0
    with open(tmp, "wb") as f:
        for chunk in chunks:
            f.write(chunk)
            n += len(chunk)
    if n == 0:
        tmp.unlink(missing_ok=True)
        raise AIVideoError("TTS returned no audio")
    tmp.replace(output)
    return n


def synthesize(
    req: TTSRequest, output: Path, *, client: Any = None, guard: budget.BudgetGuard | None = None
) -> int:
    """Validate, budget-check, call ElevenLabs (with retries) and write ``output``."""
    req.validate()
    settings = get_settings()
    guard = guard or budget.default_guard()
    cost = req.estimated_cost()

    if settings.dry_run:
        guard.check(cost, what="elevenlabs:tts")
        log.info("dry-run: would synthesize %d chars (~$%.3f) -> %s", len(req.text), cost, output)
        return 0

    if client is None:
        from ai_video.providers.clients import elevenlabs_client

        client = elevenlabs_client(settings)

    def _call() -> int:
        audio = client.text_to_speech.convert(
            voice_id=req.voice_id,
            text=req.text,
            model_id=req.model,
            language_code=req.lang,
            output_format=DEFAULT_OUTPUT_FORMAT,
            voice_settings={
                "stability": req.stability,
                "similarity_boost": req.similarity,
                "style": req.style,
                "use_speaker_boost": True,
                "speed": req.speed,
            },
        )
        return write_chunks(audio, output)

    with guard.charge("elevenlabs", "tts", cost):
        return retry_call(_call, attempts=settings.max_retries + 1, describe="elevenlabs tts")


def main() -> int:
    parser = argparse.ArgumentParser(description="ElevenLabs TTS")
    parser.add_argument("-t", "--text", help="Inline text (overrides --input)")
    parser.add_argument("-i", "--input", type=Path, default=Path("script.txt"), help="Input .txt file")
    parser.add_argument("-o", "--output", type=Path, default=Path("narration.mp3"), help="Output .mp3 path")
    parser.add_argument("-v", "--voice-id", default=None, help="Voice id (default: catalog default_voice)")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, choices=MODELS)
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG, help="Language code (default: es)")
    parser.add_argument("--stability", type=float, default=0.5)
    parser.add_argument("--similarity", type=float, default=0.75)
    parser.add_argument("--style", type=float, default=0.0)
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--dry-run", action="store_true", help="Validate and estimate cost only")
    args = parser.parse_args()

    if args.dry_run:
        get_settings().dry_run = True
    try:
        req = TTSRequest(
            text=read_text(args.text, args.input),
            voice_id=args.voice_id or default_voice_id(),
            model=args.model,
            lang=args.lang,
            stability=args.stability,
            similarity=args.similarity,
            style=args.style,
            speed=args.speed,
        )
        n = synthesize(req, args.output)
    except (ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if n:
        print(f"wrote {args.output} ({n / 1024:.1f} KB, model={req.model}, voice={req.voice_id})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
