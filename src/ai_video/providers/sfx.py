"""Generate sound effects with the ElevenLabs text-to-sound-effects API.

Usage:
    ai-video sfx -t "low impactful horror whoosh sub-bass" -d 1.5 -o assets/sfx/whoosh.mp3
    ai-video sfx -t "..." -d 4 -i 0.6 --loop -o assets/sfx/loop.mp3
    ai-video sfx --spec sfx-spec.json            # batch mode
    ai-video sfx --spec sfx-spec.json --dry-run  # validate + estimate cost only

Batch spec (JSON list, paths relative to the spec file's directory):
    [{"out": "assets/sfx/h1-howl.mp3", "text": "distant howl...", "duration": 3.0,
      "influence": 0.3, "loop": false}, ...]
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_video import budget
from ai_video.config import get_settings
from ai_video.errors import AIVideoError, BudgetExceededError
from ai_video.log import get_logger
from ai_video.providers.tts import write_chunks
from ai_video.retry import retry_call

log = get_logger(__name__)

DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"
MIN_DURATION_S, MAX_DURATION_S = 0.5, 22.0


@dataclass(frozen=True)
class SFXJob:
    text: str
    out: Path
    duration: float | None = None
    influence: float | None = None
    loop: bool = False

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError(f"{self.out}: empty prompt text")
        if self.duration is not None and not MIN_DURATION_S <= self.duration <= MAX_DURATION_S:
            raise ValueError(f"{self.out}: duration must be within [{MIN_DURATION_S}, {MAX_DURATION_S}]s")
        if self.influence is not None and not 0.0 <= self.influence <= 1.0:
            raise ValueError(f"{self.out}: influence must be within [0, 1]")


def load_jobs(spec_path: Path) -> list[SFXJob]:
    """Parse and validate a batch spec. Relative ``out`` paths resolve against the spec's dir."""
    try:
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{spec_path}: invalid JSON ({exc})") from exc
    if not isinstance(raw, list):
        raise ValueError(f"{spec_path}: expected a JSON list of jobs")
    jobs = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict) or "out" not in item or "text" not in item:
            raise ValueError(f"{spec_path}: job #{i} needs 'out' and 'text'")
        out = Path(item["out"])
        if not out.is_absolute():
            out = spec_path.parent / out
        job = SFXJob(
            text=str(item["text"]),
            out=out,
            duration=item.get("duration"),
            influence=item.get("influence"),
            loop=bool(item.get("loop", False)),
        )
        job.validate()
        jobs.append(job)
    return jobs


def generate_one(client: Any, job: SFXJob, *, model_id: str | None = None) -> int:
    kwargs: dict[str, Any] = {"text": job.text, "output_format": DEFAULT_OUTPUT_FORMAT}
    if job.duration is not None:
        kwargs["duration_seconds"] = job.duration
    if job.influence is not None:
        kwargs["prompt_influence"] = job.influence
    if job.loop:
        kwargs["loop"] = True
    if model_id:
        kwargs["model_id"] = model_id
    return write_chunks(client.text_to_sound_effects.convert(**kwargs), job.out)


def run_jobs(
    jobs: list[SFXJob],
    *,
    client: Any = None,
    guard: budget.BudgetGuard | None = None,
    model_id: str | None = None,
) -> tuple[int, int]:
    """Run jobs sequentially. Returns (ok, failed). Stops early if the budget is exhausted."""
    settings = get_settings()
    guard = guard or budget.default_guard()
    cost = budget.estimate("elevenlabs_sfx_per_call")
    guard.check(cost * len(jobs), what=f"elevenlabs:sfx x{len(jobs)}")
    if settings.dry_run:
        log.info("dry-run: %d SFX jobs (~$%.2f)", len(jobs), cost * len(jobs))
        return 0, 0
    if client is None:
        from ai_video.providers.clients import elevenlabs_client

        client = elevenlabs_client(settings)
    ok = failed = 0
    for job in jobs:
        try:

            def _call(job: SFXJob = job) -> int:
                return generate_one(client, job, model_id=model_id)

            with guard.charge("elevenlabs", "sfx", cost):
                size = retry_call(
                    _call,
                    attempts=settings.max_retries + 1,
                    describe=f"sfx {job.out.name}",
                )
            log.info("wrote %s (%.1f KB)", job.out, size / 1024)
            ok += 1
        except BudgetExceededError:
            raise
        except Exception as exc:  # one bad job must not kill the batch
            log.error("FAILED %s: %s", job.out, exc)
            failed += 1
    return ok, failed


def main() -> int:
    parser = argparse.ArgumentParser(description="ElevenLabs Sound Effects generator")
    parser.add_argument("-t", "--text", help="Prompt for the SFX")
    parser.add_argument("-d", "--duration", type=float, help="Duration in seconds (0.5-22)")
    parser.add_argument("-i", "--influence", type=float, help="prompt_influence 0-1 (default ~0.3)")
    parser.add_argument("--loop", action="store_true", help="Generate as a perfect loop")
    parser.add_argument("--model", help="model_id override (default eleven_text_to_sound_v2)")
    parser.add_argument("-o", "--output", type=Path, help="Output mp3 path")
    parser.add_argument("--spec", type=Path, help="Batch mode: JSON list of jobs")
    parser.add_argument("--dry-run", action="store_true", help="Validate and estimate cost only")
    args = parser.parse_args()

    if args.dry_run:
        get_settings().dry_run = True
    try:
        if args.spec:
            jobs = load_jobs(args.spec)
        else:
            if not args.text or not args.output:
                print("error: -t and -o are required (or use --spec)", file=sys.stderr)
                return 2
            job = SFXJob(args.text, args.output, args.duration, args.influence, args.loop)
            job.validate()
            jobs = [job]
        ok, failed = run_jobs(jobs, model_id=args.model)
    except (ValueError, FileNotFoundError, AIVideoError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if not get_settings().dry_run:
        print(f"{ok}/{len(jobs)} generated")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
