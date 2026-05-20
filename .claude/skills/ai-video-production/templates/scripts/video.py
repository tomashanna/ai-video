#!/usr/bin/env python3
"""
video.py — Genera clips de video animados desde imágenes estáticas usando Kling via Replicate.

Uso:
  python scripts/video.py -i assets/h3-scene.png -p "camera moves forward into doorway" -o assets/h3-scene.mp4
  python scripts/video.py -i assets/h3-scene.png -p "..." -o assets/out.mp4 --duration 5

Implementación: polling manual de predictions/{id} cada 5s en lugar de client.run() (que
hace long-poll y choca con timeout server-side de 60s cuando Replicate está saturado).
"""

import argparse
import base64
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import httpx
import re
import replicate
import replicate.exceptions

MODEL_DEFAULT = "kwaivgi/kling-v2.5-turbo-pro"
MAX_ATTEMPTS = 3
POLL_INTERVAL = 5
POLL_TIMEOUT = 600

def image_to_data_uri(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else "image/png"
    return f"data:{mime};base64,{data}"

def build_input(model, image_uri, prompt, duration, end_image_uri=None):
    base = {
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


def create_with_429_retry(client, model, image_uri, prompt, duration, end_image_uri=None, max_429=10, max_402=8):
    """Crea prediction reintentando en caso de rate limit 429 o insufficient credit 402."""
    n_429 = 0
    n_402 = 0
    while True:
        try:
            return client.predictions.create(
                model=model,
                input=build_input(model, image_uri, prompt, duration, end_image_uri),
            )
        except replicate.exceptions.ReplicateError as e:
            msg = str(e)
            if "429" in msg or "throttled" in msg.lower():
                n_429 += 1
                if n_429 > max_429:
                    raise RuntimeError(f"still rate limited after {max_429} retries")
                m = re.search(r"resets in ~?(\d+)s", msg)
                wait_s = int(m.group(1)) + 2 if m else 12
                print(f"  rate limited (429), waiting {wait_s}s...", file=sys.stderr)
                time.sleep(wait_s)
            elif "402" in msg or "Insufficient credit" in msg:
                n_402 += 1
                if n_402 > max_402:
                    raise RuntimeError(f"still insufficient credit after {max_402} retries (~{max_402*60}s)")
                wait_s = 60
                print(f"  insufficient credit (402) #{n_402}/{max_402}, waiting {wait_s}s for billing propagation...", file=sys.stderr)
                time.sleep(wait_s)
            else:
                raise

def run_one_attempt(client, model, image_uri, prompt, duration, output_path, end_image_uri=None):
    """Crea prediction, polea hasta succeeded/failed, descarga MP4."""
    prediction = create_with_429_retry(client, model, image_uri, prompt, duration, end_image_uri)
    pid = prediction.id
    print(f"  prediction id: {pid}")

    deadline = time.time() + POLL_TIMEOUT
    while True:
        prediction.reload()
        status = prediction.status
        if status == "succeeded":
            break
        if status in ("failed", "canceled"):
            raise RuntimeError(f"prediction {pid} {status}: {prediction.error}")
        if time.time() > deadline:
            try:
                prediction.cancel()
            except Exception:
                pass
            raise TimeoutError(f"prediction {pid} stuck at {status} after {POLL_TIMEOUT}s")
        time.sleep(POLL_INTERVAL)

    output = prediction.output
    if hasattr(output, "read"):
        video_bytes = output.read()
    else:
        import urllib.request
        with urllib.request.urlopen(str(output), timeout=120) as r:
            video_bytes = r.read()

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(video_bytes)

    return len(video_bytes)

def run(image_path: str, prompt: str, output_path: str, duration: int = 5, model: str = MODEL_DEFAULT, end_image_path: str = None):
    if not os.path.exists(image_path):
        print(f"error: image not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    if end_image_path and not os.path.exists(end_image_path):
        print(f"error: end_image not found: {end_image_path}", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("error: REPLICATE_API_TOKEN not set in .env", file=sys.stderr)
        sys.exit(1)

    print(f"animating {image_path} → {output_path} ({duration}s) model={model}{' [+end_image]' if end_image_path else ''}")
    print(f"prompt: {prompt}")

    image_uri = image_to_data_uri(image_path)
    end_image_uri = image_to_data_uri(end_image_path) if end_image_path else None

    client = replicate.Client(
        api_token=token,
        timeout=httpx.Timeout(60.0, connect=30.0),
    )

    last_exc = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        start = time.time()
        try:
            print(f"[attempt {attempt}/{MAX_ATTEMPTS}] calling Kling...")
            size_bytes = run_one_attempt(client, model, image_uri, prompt, duration, output_path, end_image_uri)
            elapsed = time.time() - start
            size_kb = size_bytes // 1024
            print(f"wrote {output_path} ({size_kb} KB, {elapsed:.0f}s)")
            return
        except (httpx.ReadTimeout, httpx.ConnectTimeout, httpx.RemoteProtocolError, TimeoutError, RuntimeError) as e:
            last_exc = e
            elapsed = time.time() - start
            print(f"[attempt {attempt}] {type(e).__name__} after {elapsed:.0f}s: {e}", file=sys.stderr)
            if attempt < MAX_ATTEMPTS:
                backoff = 15 * attempt
                print(f"retrying in {backoff}s...", file=sys.stderr)
                time.sleep(backoff)

    print(f"FAILED after {MAX_ATTEMPTS} attempts. Last error: {last_exc}", file=sys.stderr)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image",    required=True, help="input image path (start frame)")
    parser.add_argument("-e", "--end-image", default=None, help="optional end frame image path (interpolation target)")
    parser.add_argument("-p", "--prompt",   required=True, help="motion description")
    parser.add_argument("-o", "--output",   required=True, help="output .mp4 path")
    parser.add_argument("--duration",       type=int, default=5, choices=[5, 10], help="clip duration in seconds (default: 5)")
    parser.add_argument("--model",          default=MODEL_DEFAULT, help=f"Replicate model identifier (default: {MODEL_DEFAULT})")
    args = parser.parse_args()
    run(args.image, args.prompt, args.output, args.duration, args.model, args.end_image)

if __name__ == "__main__":
    main()
