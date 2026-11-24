#!/usr/bin/env python3
"""
veo3.py — Veo 3.1 video generation via Gemini API enterprise (FREE).

Generates 6s 9:16 video clips with native audio + lip-sync via Google Veo 3.1.
Costs $0 via Gemini Enterprise (Business Edition) — Veo 3.1 included as capacity.

USAGE:
    python veo3.py --prompt "POV walking corridor" --output assets/clips/shot_01.mp4
    python veo3.py --prompt "..." --aspect 9:16 --duration 6 --tier preview --output ...

PROMPT-AS-IMAGE-REF:
    python veo3.py --prompt "character speaking" --image-ref assets/anchors/char.png --output ...

TIERS:
    - preview (DEFAULT): veo-3.1-generate-preview — highest quality
    - fast: veo-3.1-fast-generate-preview — faster latency
    - lite: veo-3.1-lite-generate-preview — lighter compute

LATENCY: ~60-90s per 6s clip generation.

ENV: GEMINI_API_KEY required (Enterprise key with Veo 3.1 capacity).

OUTPUT: MP4 with h264 + AAC native audio. 9:16 native vertical for IG Reel.
"""
import argparse
import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    import httpx
except ImportError:
    print("ERROR: pip install google-genai httpx", file=sys.stderr)
    sys.exit(1)


TIER_MODELS = {
    "preview": "veo-3.1-generate-preview",
    "fast": "veo-3.1-fast-generate-preview",
    "lite": "veo-3.1-lite-generate-preview",
}


def generate_video(
    prompt: str,
    output_path: Path,
    aspect_ratio: str = "9:16",
    duration_s: int = 6,
    tier: str = "preview",
    image_ref_path: Path = None,
) -> dict:
    """Generate via Veo 3.1 + download. Returns dict with metadata."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY env var required")

    client = genai.Client(api_key=api_key)
    model_id = TIER_MODELS.get(tier, TIER_MODELS["preview"])

    print(f"[info] Generating via {model_id}", file=sys.stderr)
    print(f"[info] Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}", file=sys.stderr)
    print(f"[info] Aspect: {aspect_ratio}, Duration: {duration_s}s", file=sys.stderr)

    start = time.time()

    # Optional reference image
    image = None
    if image_ref_path and image_ref_path.exists():
        print(f"[info] Using reference image: {image_ref_path}", file=sys.stderr)
        # Upload image to Files API first then reference in generation
        uploaded = client.files.upload(file=str(image_ref_path))
        image = types.Image(image_bytes=image_ref_path.read_bytes(), mime_type="image/png")

    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
        duration_seconds=duration_s,
        number_of_videos=1,
    )

    operation = client.models.generate_videos(
        model=model_id,
        prompt=prompt,
        image=image,
        config=config,
    )
    print(f"[info] Operation: {operation.name}", file=sys.stderr)

    while not operation.done:
        elapsed = time.time() - start
        print(f"[info] Generating... {elapsed:.0f}s", file=sys.stderr, flush=True)
        time.sleep(15)
        operation = client.operations.get(operation)

    elapsed = time.time() - start
    print(f"[info] ✅ Generation done in {elapsed:.0f}s", file=sys.stderr)

    # Check for filter rejection
    if not operation.response or not operation.response.generated_videos:
        if hasattr(operation.response, 'rai_media_filtered_count') and operation.response.rai_media_filtered_count:
            print(f"[error] NSFW FILTER REJECTED — {operation.response.rai_media_filtered_count} videos blocked", file=sys.stderr)
            if operation.response.rai_media_filtered_reasons:
                for reason in operation.response.rai_media_filtered_reasons:
                    print(f"[error] Reason: {reason}", file=sys.stderr)
            raise RuntimeError("Veo NSFW filter rejection — try Hailuo fallback")
        raise RuntimeError(f"No videos generated. Response: {operation.response}")

    video = operation.response.generated_videos[0].video
    print(f"[info] URI: {video.uri}", file=sys.stderr)

    # Download with follow_redirects + auth header
    download_start = time.time()
    with httpx.Client(timeout=120.0, follow_redirects=True) as hc:
        r = hc.get(video.uri, headers={'x-goog-api-key': api_key})
        if r.status_code != 200:
            raise RuntimeError(f"Download failed HTTP {r.status_code}: {r.text[:200]}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(r.content)

    download_elapsed = time.time() - download_start
    size_mb = output_path.stat().st_size / 1e6
    total_elapsed = time.time() - start

    print(f"[info] ✅ Saved: {output_path} ({size_mb:.1f} MB)", file=sys.stderr)
    print(f"[info] Latency breakdown: generation={elapsed:.0f}s + download={download_elapsed:.1f}s = total {total_elapsed:.0f}s", file=sys.stderr)

    return {
        "model": model_id,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "duration_s": duration_s,
        "output_path": str(output_path),
        "size_mb": size_mb,
        "generation_latency_s": elapsed,
        "download_latency_s": download_elapsed,
        "total_latency_s": total_elapsed,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--prompt", required=True, help="Generation prompt")
    parser.add_argument("--output", type=Path, required=True, help="Output MP4 path")
    parser.add_argument("--aspect", default="9:16", choices=["9:16", "16:9", "1:1"])
    parser.add_argument("--duration", type=int, default=6, help="Duration seconds (default 6)")
    parser.add_argument("--tier", default="preview", choices=list(TIER_MODELS.keys()))
    parser.add_argument("--image-ref", type=Path, help="Reference image (character anchor)")
    args = parser.parse_args()

    result = generate_video(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect,
        duration_s=args.duration,
        tier=args.tier,
        image_ref_path=args.image_ref,
    )

    print(f"\n✅ Generated: {result['output_path']}")
    print(f"   Size: {result['size_mb']:.1f} MB, Latency: {result['total_latency_s']:.0f}s, Cost: $0 enterprise")


if __name__ == "__main__":
    main()
