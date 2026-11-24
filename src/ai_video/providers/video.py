"""Animate a still image into a short clip with Kling (image-to-video) via Replicate.

Usage:
    ai-video video -i assets/h3-scene.png -p "camera moves forward into doorway" -o assets/h3-scene.mp4
    ai-video video -i start.png -e end.png -p "..." -o out.mp4 --duration 10
    ai-video video -i start.png -p "..." -o out.mp4 --dry-run

Implementation notes:
* Predictions are created then polled manually (``client.run`` long-polls and hits a
  60s server-side timeout when Replicate is saturated).
* 429 (rate limit) honours the server's reset hint; 402 (credit propagation) waits;
  transient network errors back off exponentially. Every wait is bounded.
* Each attempt is charged against the spend budget *before* the prediction is created.
"""

from __future__ import annotations

import argparse
import base64
import re
import sys
import time
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

from ai_video import budget
from ai_video.config import get_settings
from ai_video.errors import AIVideoError, ProviderError
from ai_video.log import get_logger
from ai_video.retry import backoff_delays, poll_until

log = get_logger(__name__)

MODEL_DEFAULT = "kwaivgi/kling-v2.5-turbo-pro"
POLL_INTERVAL_S = 5.0
DURATIONS = (5, 10)
_MIME = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}


def image_to_data_uri(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    if ext not in _MIME:
        raise ValueError(f"unsupported image format ({ext}): {path}")
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:{_MIME[ext]};base64,{data}"


def build_input(
    model: str, image_uri: str, prompt: str, duration: int, end_image_uri: str | None = None
) -> dict[str, Any]:
    base: dict[str, Any] = {
        "start_image": image_uri,
        "prompt": prompt,
        "duration": duration,
        "negative_prompt": "static image, no movement, blur, distortion",
    }
    if end_image_uri:
        base["end_image"] = end_image_uri
    if model == "kwaivgi/kling-v2.0":
        base["cfg_scale"] = 0.5
    return base


def rate_limit_wait_s(message: str, default: float = 12.0) -> float:
    """Parse Replicate's 'resets in ~Ns' hint (plus a 2s margin)."""
    m = re.search(r"resets in ~?(\d+)s", message)
    return int(m.group(1)) + 2 if m else default


def create_prediction(
    client: Any,
    payload: dict[str, Any],
    model: str,
    *,
    max_429: int = 10,
    max_402: int = 8,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """Create a prediction, retrying on 429 (rate limit) and 402 (credit propagation)."""
    import replicate.exceptions

    n_429 = n_402 = 0
    while True:
        try:
            return client.predictions.create(model=model, input=payload)
        except replicate.exceptions.ReplicateError as e:
            msg = str(e)
            if "429" in msg or "throttled" in msg.lower():
                n_429 += 1
                if n_429 > max_429:
                    raise ProviderError(f"still rate limited after {max_429} retries") from e
                wait = rate_limit_wait_s(msg)
                log.warning("rate limited (429), waiting %.0fs", wait)
                sleep(wait)
            elif "402" in msg or "Insufficient credit" in msg:
                n_402 += 1
                if n_402 > max_402:
                    raise ProviderError(f"insufficient credit after {max_402} retries") from e
                log.warning("insufficient credit (402) %d/%d, waiting 60s", n_402, max_402)
                sleep(60)
            else:
                raise


def wait_for_prediction(
    prediction: Any, *, timeout_s: float, sleep: Callable[[float], None] = time.sleep
) -> Any:
    def _check() -> Any:
        prediction.reload()
        if prediction.status == "succeeded":
            return prediction
        if prediction.status in ("failed", "canceled"):
            raise ProviderError(f"prediction {prediction.id} {prediction.status}: {prediction.error}")
        return None

    try:
        return poll_until(
            _check,
            timeout_s=timeout_s,
            interval_s=POLL_INTERVAL_S,
            sleep=sleep,
            describe=f"prediction {prediction.id}",
        )
    except TimeoutError:
        try:
            prediction.cancel()
        except Exception as exc:  # best effort, do not mask the timeout
            log.debug("cancel failed: %s", exc)
        raise


def download_output(output: Any, timeout_s: float) -> bytes:
    if hasattr(output, "read"):
        data: bytes = output.read()
        return data
    url = str(output[0] if isinstance(output, list) else output)
    if not url.startswith("https://"):
        raise ProviderError(f"refusing to download non-https output URL: {url[:60]}")
    with urllib.request.urlopen(url, timeout=timeout_s) as r:  # noqa: S310 - https enforced above
        body: bytes = r.read()
        return body


def animate(
    image: Path,
    prompt: str,
    output: Path,
    *,
    duration: int = 5,
    model: str = MODEL_DEFAULT,
    end_image: Path | None = None,
    client: Any = None,
    guard: budget.BudgetGuard | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    if not image.is_file():
        raise FileNotFoundError(f"image not found: {image}")
    if end_image is not None and not end_image.is_file():
        raise FileNotFoundError(f"end image not found: {end_image}")
    if duration not in DURATIONS:
        raise ValueError(f"duration must be one of {DURATIONS}")
    if not prompt.strip():
        raise ValueError("empty motion prompt")

    settings = get_settings()
    guard = guard or budget.default_guard()
    cost = budget.estimate("kling_per_s", duration)
    if settings.dry_run:
        guard.check(cost, what="replicate:kling")
        log.info("dry-run: animate %s (%ds, %s) ~$%.2f -> %s", image, duration, model, cost, output)
        return 0
    if client is None:
        from ai_video.providers.clients import replicate_client

        client = replicate_client(settings)

    payload = build_input(
        model, image_to_data_uri(image), prompt, duration, image_to_data_uri(end_image) if end_image else None
    )
    attempts = settings.max_retries + 1
    delays = backoff_delays(attempts, base_s=15.0, max_s=120.0)
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            with guard.charge("replicate", f"kling-{duration}s", cost):
                pred = create_prediction(client, payload, model, sleep=sleep)
                log.info("prediction %s created (attempt %d/%d)", pred.id, attempt, attempts)
                pred = wait_for_prediction(pred, timeout_s=settings.poll_timeout_s, sleep=sleep)
                data = download_output(pred.output, settings.http_timeout_s)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            return len(data)
        except AIVideoError as exc:
            if not isinstance(exc, ProviderError):
                raise  # budget/config errors are not retryable
            last_exc = exc
        except (TimeoutError, OSError) as exc:
            last_exc = exc
        if attempt < attempts:
            log.warning("attempt %d failed (%s); retrying in %.0fs", attempt, last_exc, delays[attempt - 1])
            sleep(delays[attempt - 1])
    raise ProviderError(f"Kling failed after {attempts} attempts: {last_exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Kling image-to-video via Replicate")
    parser.add_argument("-i", "--image", type=Path, required=True, help="Input image (start frame)")
    parser.add_argument("-e", "--end-image", type=Path, default=None, help="Optional end frame")
    parser.add_argument("-p", "--prompt", required=True, help="Motion description")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output .mp4 path")
    parser.add_argument("--duration", type=int, default=5, choices=DURATIONS, help="Clip seconds (default 5)")
    parser.add_argument("--model", default=MODEL_DEFAULT, help=f"Replicate model (default {MODEL_DEFAULT})")
    parser.add_argument("--dry-run", action="store_true", help="Validate and estimate cost only")
    args = parser.parse_args()

    if args.dry_run:
        get_settings().dry_run = True
    try:
        n = animate(
            args.image,
            args.prompt,
            args.output,
            duration=args.duration,
            model=args.model,
            end_image=args.end_image,
        )
    except (ValueError, FileNotFoundError, AIVideoError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if n:
        print(f"wrote {args.output} ({n // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
