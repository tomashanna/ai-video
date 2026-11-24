"""Generate still images with Gemini (Nano Banana), optionally conditioned on reference images.

Usage:
    # No reference (initial character anchor, landscapes, objects)
    ai-video image -p "prompt here" -o assets/frame.png

    # One or more references (character consistency via multimodal input)
    ai-video image -p "The character from the reference walking through a dark forest." \\
        --ref assets/char-a-anchor.png -o assets/h3-walk-a.png

    # Per-format style suffix (default is empty = genre-agnostic)
    ai-video image -p "..." --style-suffix " <format style>" -o assets/...

Defaults target vertical reels: 9:16, 1K. See
``.claude/skills/ai-video-production/CHARACTER-CONSISTENCY.md`` for the anchor workflow.
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path
from typing import Any

from ai_video import budget
from ai_video.config import get_settings
from ai_video.errors import AIVideoError, ProviderError
from ai_video.log import get_logger
from ai_video.retry import retry_call

log = get_logger(__name__)

MODEL = "gemini-3.1-flash-image-preview"
SIZES = ("512", "1K", "2K", "4K")
ASPECTS = ("9:16", "16:9", "1:1", "4:5", "3:4", "4:3")
_MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}

# Layer A is genre-agnostic: no style suffix by default. Formats pass --style-suffix.
STYLE_SUFFIX = ""

# Style suffix of the HORROR format (layer B). Not applied by default.
HORROR_SUFFIX = (
    " Dark cinematic horror aesthetic, desaturated color grade with warm amber "
    "and orange highlights only, liminal space mood, eerie atmospheric lighting, "
    "Midjourney v6 photorealistic style, uncanny valley, subtle film grain, "
    "low-key lighting, dead-center composition, 35mm lens, shallow depth of field. "
    "No text, no logos, no watermarks."
)


def resolve_style_suffix(no_mono_suffix: bool, style_suffix: str | None) -> str:
    """--style-suffix wins; else STYLE_SUFFIX (''). --no-mono-suffix forces empty (back-compat)."""
    if no_mono_suffix:
        return ""
    return style_suffix if style_suffix is not None else STYLE_SUFFIX


def mime_for(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    if ext not in _MIME:
        raise ValueError(f"unsupported reference format ({ext}): {path}")
    return _MIME[ext]


def load_reference_images(ref_paths: list[Path]) -> list[tuple[str, bytes]]:
    """Validate and read reference images -> [(mime, bytes)]."""
    out = []
    for ref in ref_paths:
        if not ref.is_file():
            raise FileNotFoundError(f"reference image not found: {ref}")
        out.append((mime_for(ref), ref.read_bytes()))
    return out


def extract_image_bytes(response: Any) -> bytes:
    """First inline image in a Gemini response (handles base64 strings)."""
    candidates = getattr(response, "candidates", None) or []
    for cand in candidates:
        content = getattr(cand, "content", None)
        for part in getattr(content, "parts", None) or []:
            inline = getattr(part, "inline_data", None)
            if inline is not None and getattr(inline, "data", None):
                data = inline.data
                return base64.b64decode(data) if isinstance(data, str) else bytes(data)
    raise ProviderError("no image returned by Gemini (blocked by safety filter or empty response)")


def generate(
    prompt: str,
    output: Path,
    *,
    refs: list[Path] | None = None,
    size: str = "1K",
    aspect: str = "9:16",
    client: Any = None,
    guard: budget.BudgetGuard | None = None,
) -> int:
    if not prompt.strip():
        raise ValueError("empty prompt")
    if size not in SIZES:
        raise ValueError(f"size must be one of {SIZES}")
    if aspect not in ASPECTS:
        raise ValueError(f"aspect must be one of {ASPECTS}")
    ref_data = load_reference_images(refs or [])
    settings = get_settings()
    guard = guard or budget.default_guard()
    cost = budget.estimate("gemini_image_per_image")
    if settings.dry_run:
        guard.check(cost, what="gemini:image")
        log.info("dry-run: image (%s, %s, %d refs) ~$%.3f -> %s", size, aspect, len(ref_data), cost, output)
        return 0

    from google.genai import types

    if client is None:
        from ai_video.providers.clients import gemini_client

        client = gemini_client(settings)
    contents: list[Any] = [types.Part(inline_data=types.Blob(mime_type=m, data=b)) for m, b in ref_data]
    contents.append(prompt)
    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=aspect, image_size=size),
    )

    def _call() -> bytes:
        resp = client.models.generate_content(model=MODEL, contents=contents, config=config)
        return extract_image_bytes(resp)

    with guard.charge("gemini", "image", cost):
        data = retry_call(_call, attempts=settings.max_retries + 1, describe="gemini image")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return len(data)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Image generator with multimodal reference support (Gemini)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("-p", "--prompt", required=True, help="Base prompt")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PNG path")
    parser.add_argument("--ref", type=Path, action="append", default=[], help="Reference image (repeatable)")
    parser.add_argument("--size", default="1K", choices=SIZES, help="Resolution (default 1K; 512 for drafts)")
    parser.add_argument("--aspect", default="9:16", choices=ASPECTS, help="Aspect ratio (default 9:16)")
    parser.add_argument("--no-mono-suffix", action="store_true", help="Force no style suffix (back-compat)")
    parser.add_argument("--style-suffix", default=None, help="Format style suffix (default empty)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and estimate cost only")
    args = parser.parse_args()

    if args.dry_run:
        get_settings().dry_run = True
    suffix = resolve_style_suffix(args.no_mono_suffix, args.style_suffix)
    if not suffix and args.style_suffix is None and not args.no_mono_suffix:
        log.warning("no style suffix (agnostic default). Pass --style-suffix with the format's style.")
    try:
        n = generate(args.prompt + suffix, args.output, refs=args.ref, size=args.size, aspect=args.aspect)
    except (ValueError, FileNotFoundError, AIVideoError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if n:
        refs = f" (refs: {len(args.ref)})" if args.ref else ""
        print(f"wrote {args.output} ({n / 1024:.1f} KB, {args.size}, {args.aspect}){refs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
