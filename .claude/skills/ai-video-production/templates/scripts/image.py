"""
Generate images via Gemini Nano Banana for video compositions.

Supports reference images (character consistency via multimodal input).

Usage:
    # Sin referencia (anchor inicial, paisajes, objetos sin personaje)
    .venv/bin/python scripts/image.py -p "prompt here" -o assets/frame.png

    # Con 1 referencia (escena con un personaje conocido)
    .venv/bin/python scripts/image.py \\
      -p "The character from the reference walking through a dark forest." \\
      --ref assets/berni-anchor.png \\
      -o assets/h3-walk-a.png

    # Con múltiples referencias (escena con varios personajes)
    .venv/bin/python scripts/image.py \\
      -p "Both characters sitting at a table, facing each other." \\
      --ref assets/berni-anchor.png \\
      --ref assets/yonaiker-anchor.png \\
      -o assets/h1-both.png

    # Override del style suffix
    .venv/bin/python scripts/image.py -p "..." --no-mono-suffix -o assets/...

Defaults are tuned for vertical Reels: 9:16, 1K resolution, monochrome-enforced prompt suffix.

CHARACTER CONSISTENCY:
    Para mantener un personaje visualmente idéntico entre tomas:
    1. Generar primero el anchor del personaje (sin --ref) — close-up frontal claro.
    2. Para CADA escena con ese personaje, pasar --ref <anchor>.
    Ver ai-video-production/CHARACTER-CONSISTENCY.md para reglas completas.
"""

import argparse
import base64
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parent.parent

HORROR_SUFFIX = (
    " Dark cinematic horror aesthetic, desaturated color grade with warm amber "
    "and orange highlights only, liminal space mood, eerie atmospheric lighting, "
    "Midjourney v6 photorealistic style, uncanny valley, subtle film grain, "
    "low-key lighting, dead-center composition, 35mm lens, shallow depth of field. "
    "No text, no logos, no watermarks."
)


def load_reference_images(ref_paths):
    """
    Load reference images and convert them to types.Part for multimodal input.

    Args:
        ref_paths: list of Path objects pointing to PNG/JPG files.

    Returns:
        list of types.Part with inline_data (image bytes).
    """
    parts = []
    for ref_path in ref_paths:
        if not ref_path.exists():
            sys.exit(f"error: reference image not found: {ref_path}")
        ext = ref_path.suffix.lower().lstrip(".")
        if ext not in {"png", "jpg", "jpeg", "webp"}:
            sys.exit(f"error: unsupported reference format ({ext}): {ref_path}")
        mime = "image/png" if ext == "png" else "image/jpeg" if ext in {"jpg", "jpeg"} else "image/webp"
        with open(ref_path, "rb") as f:
            image_bytes = f.read()
        parts.append(
            types.Part(
                inline_data=types.Blob(
                    mime_type=mime,
                    data=image_bytes,
                )
            )
        )
    return parts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Image generator with multimodal reference support (Gemini Nano Banana)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("-p", "--prompt", required=True, help="Base prompt")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PNG path")
    parser.add_argument(
        "--ref",
        type=Path,
        action="append",
        default=[],
        help="Reference image path (for character consistency). Can be repeated for multiple references.",
    )
    parser.add_argument(
        "--size",
        default="1K",
        choices=["512", "1K", "2K", "4K"],
        help="Resolution (default 1K; 512 for drafts)",
    )
    parser.add_argument("--aspect", default="9:16", help="Aspect ratio (default 9:16)")
    parser.add_argument("--no-mono-suffix", action="store_true", help="Skip style suffix enforcement")
    args = parser.parse_args()

    load_dotenv(PROJECT_ROOT / ".env")
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        sys.exit("error: GEMINI_API_KEY not found in .env")

    prompt_text = args.prompt if args.no_mono_suffix else args.prompt + HORROR_SUFFIX

    # Build multimodal contents: [ref_image_1, ref_image_2, ..., prompt_text]
    contents = []
    if args.ref:
        contents.extend(load_reference_images(args.ref))
        ref_names = ", ".join(r.name for r in args.ref)
        print(f"[image.py] using {len(args.ref)} reference(s): {ref_names}", file=sys.stderr)
    contents.append(prompt_text)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=args.aspect,
                image_size=args.size,
            ),
        ),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    image_saved = False
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None):
            data = part.inline_data.data
            if isinstance(data, str):
                data = base64.b64decode(data)
            args.output.write_bytes(data)
            image_saved = True
            break

    if not image_saved:
        sys.exit("error: no image returned from Gemini")

    size_kb = args.output.stat().st_size / 1024
    ref_info = f" (refs: {len(args.ref)})" if args.ref else ""
    print(f"wrote {args.output} ({size_kb:.1f} KB, {args.size}, {args.aspect}){ref_info}")


if __name__ == "__main__":
    main()
