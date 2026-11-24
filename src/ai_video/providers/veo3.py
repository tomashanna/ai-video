"""Generate short clips with native audio via Google Veo 3.1 (Gemini API).

Usage:
    ai-video veo3 --prompt "POV walking corridor" --output assets/clips/shot_01.mp4
    ai-video veo3 --prompt "..." --aspect 9:16 --duration 6 --tier fast --output ...
    ai-video veo3 --prompt "character speaking" --image-ref assets/anchors/char.png --output ...

Tiers: preview (default, highest quality) | fast | lite. Typical latency 60-90s per 6s clip.
Requires GEMINI_API_KEY with Veo access. Spend is estimated per second of video and
checked against AIVIDEO_BUDGET_USD (set AIVIDEO_PRICE_VEO_PER_S=0 if your plan includes Veo).
"""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ai_video import budget
from ai_video.config import get_settings
from ai_video.errors import AIVideoError, ProviderError
from ai_video.log import get_logger
from ai_video.retry import poll_until, retry_call

log = get_logger(__name__)

TIER_MODELS = {
    "preview": "veo-3.1-generate-preview",
    "fast": "veo-3.1-fast-generate-preview",
    "lite": "veo-3.1-lite-generate-preview",
}
ASPECTS = ("9:16", "16:9")
DURATIONS = (4, 6, 8)
_MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}


def filter_rejection_reasons(response: Any) -> list[str]:
    """Safety-filter reasons from an operation response (empty list if none)."""
    if response is None:
        return []
    count = getattr(response, "rai_media_filtered_count", 0) or 0
    if not count:
        return []
    return [str(r) for r in (getattr(response, "rai_media_filtered_reasons", None) or ["unspecified"])]


def generate_video(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "9:16",
    duration_s: int = 6,
    tier: str = "preview",
    image_ref_path: Path | None = None,
    *,
    client: Any = None,
    guard: budget.BudgetGuard | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Generate via Veo + download. Returns metadata dict (empty paths in dry-run)."""
    if not prompt.strip():
        raise ValueError("empty prompt")
    if tier not in TIER_MODELS:
        raise ValueError(f"tier must be one of {tuple(TIER_MODELS)}")
    if aspect_ratio not in ASPECTS:
        raise ValueError(f"aspect must be one of {ASPECTS}")
    if duration_s not in DURATIONS:
        raise ValueError(f"duration must be one of {DURATIONS}")
    if image_ref_path is not None and not image_ref_path.is_file():
        raise FileNotFoundError(f"reference image not found: {image_ref_path}")

    settings = get_settings()
    guard = guard or budget.default_guard()
    model_id = TIER_MODELS[tier]
    cost = budget.estimate("veo_per_s", duration_s)
    if settings.dry_run:
        guard.check(cost, what="gemini:veo")
        log.info("dry-run: veo %s %ss %s ~$%.2f -> %s", model_id, duration_s, aspect_ratio, cost, output_path)
        return {"model": model_id, "dry_run": True, "estimated_usd": cost}

    from google.genai import types

    if client is None:
        from ai_video.providers.clients import gemini_client

        client = gemini_client(settings)

    image = None
    if image_ref_path is not None:
        ext = image_ref_path.suffix.lower().lstrip(".")
        if ext not in _MIME:
            raise ValueError(f"unsupported reference format ({ext})")
        image = types.Image(image_bytes=image_ref_path.read_bytes(), mime_type=_MIME[ext])

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio, duration_seconds=duration_s, number_of_videos=1
    )
    start = time.monotonic()
    with guard.charge("gemini", f"veo-{tier}-{duration_s}s", cost):
        operation = retry_call(
            lambda: client.models.generate_videos(model=model_id, prompt=prompt, image=image, config=config),
            attempts=settings.max_retries + 1,
            describe="veo generate_videos",
        )
        log.info("veo operation %s started (%s)", operation.name, model_id)

        def _done() -> Any:
            nonlocal operation
            operation = client.operations.get(operation)
            return operation if operation.done else None

        if not operation.done:
            operation = poll_until(
                _done,
                timeout_s=settings.poll_timeout_s,
                interval_s=15,
                sleep=sleep,
                describe="Veo generation",
            )
    gen_s = time.monotonic() - start

    response = operation.response
    reasons = filter_rejection_reasons(response)
    if reasons:
        raise ProviderError(f"Veo safety filter rejected the prompt: {'; '.join(reasons)}")
    videos = getattr(response, "generated_videos", None) if response is not None else None
    if not videos:
        raise ProviderError("Veo returned no video")

    video = videos[0].video
    data = retry_call(
        lambda: client.files.download(file=video), attempts=settings.max_retries + 1, describe="veo download"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    size_mb = output_path.stat().st_size / 1e6
    log.info("saved %s (%.1f MB) in %.0fs", output_path, size_mb, time.monotonic() - start)
    return {
        "model": model_id,
        "aspect_ratio": aspect_ratio,
        "duration_s": duration_s,
        "output_path": str(output_path),
        "size_mb": size_mb,
        "generation_latency_s": gen_s,
        "estimated_usd": cost,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Veo 3.1 video generation (Gemini API)")
    parser.add_argument("--prompt", required=True, help="Generation prompt")
    parser.add_argument("--output", type=Path, required=True, help="Output MP4 path")
    parser.add_argument("--aspect", default="9:16", choices=ASPECTS)
    parser.add_argument("--duration", type=int, default=6, choices=DURATIONS, help="Seconds (default 6)")
    parser.add_argument("--tier", default="preview", choices=list(TIER_MODELS))
    parser.add_argument("--image-ref", type=Path, help="Reference image (character anchor)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and estimate cost only")
    args = parser.parse_args()

    if args.dry_run:
        get_settings().dry_run = True
    try:
        result = generate_video(
            args.prompt, args.output, args.aspect, args.duration, args.tier, args.image_ref
        )
    except (ValueError, FileNotFoundError, AIVideoError, TimeoutError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not result.get("dry_run"):
        print(
            f"generated {result['output_path']} ({result['size_mb']:.1f} MB, ~${result['estimated_usd']:.2f})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
