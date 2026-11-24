#!/usr/bin/env python3
"""
build_avu_outro_card.py — Build outro-card-template.mp4 AVU

Spec:
- 4.6s, 1080×1920, 30 fps
- Visual: black background + text scale-pop fade-in (text replaceable parameter)
- Audio: drone tone signature (-15 dB)
- Purpose: video closure with cliffhanger signature line

Usage:
  python build_avu_outro_card.py --text "LA SIRENA DE LAS SEIS NUNCA SUENA PARA VOS"
  → outputs: outro-card-template.mp4 (with that text)

For project-specific use, run with --text "..." to generate per-video outro.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ai_video.paths import avu_dir, library_dir, repo_root

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

PROJECT_ROOT = repo_root()
AVU_DIR = avu_dir()
# Unique, private work dir (was a fixed /tmp path shared across runs/users).
TMP = Path(tempfile.mkdtemp(prefix="ai-video-avu_outro_card-"))

W, H = 1080, 1920
FPS = 30
DUR_S = 4.6
N_FRAMES = int(FPS * DUR_S)
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
DRONE_PATH = library_dir() / "sfx/drones/cave-drone-deep.mp3"


def draw_frame(i, text):
    img = Image.new("RGB", (W, H), (0, 0, 0))
    t = i / FPS
    if t < 0.4:
        opacity = t / 0.4
        scale = 0.92 + 0.08 * (t / 0.4)
    elif t > DUR_S - 0.4:
        remaining = DUR_S - t
        opacity = max(0, remaining / 0.4)
        scale = 1.0
    else:
        opacity = 1.0
        scale = 1.0
    if opacity <= 0.01:
        return img
    font_size = int(58 * scale)
    font = ImageFont.truetype(FONT_PATH, font_size)
    lines = wrap_text(text, font, max_width=960)
    line_h = font_size + 16
    total_h = line_h * len(lines)
    y0 = H // 2 - total_h // 2
    txt_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)
    for li, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = W // 2 - text_w // 2 - bbox[0]
        y = y0 + li * line_h
        # Shadow
        for dx, dy in [(2, 2), (-2, 2), (2, -2), (-2, -2)]:
            draw.text((x + dx, y + dy), line, font=font, fill=(0, 0, 0, int(220 * opacity)))
        draw.text((x, y), line, font=font, fill=(255, 255, 255, int(255 * opacity)))
    img = Image.alpha_composite(img.convert("RGBA"), txt_layer).convert("RGB")
    return img


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = []
    dummy = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy)
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="OUTRO CARD\nTEXT PLACEHOLDER", help="Outro text (newline OK)")
    parser.add_argument("--output", default=str(AVU_DIR / "outro-card-template.mp4"))
    args = parser.parse_args()

    text = args.text.replace("\\n", "\n").replace("\n", " ")
    AVU_DIR.mkdir(exist_ok=True, parents=True)
    for i in range(N_FRAMES):
        draw_frame(i, text).save(TMP / f"frame_{i:04d}.png")

    silent = TMP / "silent.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-framerate",
            str(FPS),
            "-i",
            str(TMP / "frame_%04d.png"),
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-vf",
            "format=yuv420p",
            "-color_range",
            "tv",
            "-r",
            str(FPS),
            str(silent),
        ],
        check=True,
        timeout=SUBPROCESS_TIMEOUT_S,
    )

    # Audio: drone -15 dB
    audio = TMP / "audio.mp3"
    if DRONE_PATH.exists():
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-stream_loop",
                "-1",
                "-i",
                str(DRONE_PATH),
                "-t",
                str(DUR_S),
                "-af",
                "volume=-15dB",
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(audio),
            ],
            check=True,
            timeout=SUBPROCESS_TIMEOUT_S,
        )
    else:
        # Fallback: silence
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=mono",
                "-t",
                str(DUR_S),
                "-c:a",
                "libmp3lame",
                "-b:a",
                "192k",
                str(audio),
            ],
            check=True,
            timeout=SUBPROCESS_TIMEOUT_S,
        )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(silent),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-ar",
            "48000",
            "-shortest",
            args.output,
        ],
        check=True,
        timeout=SUBPROCESS_TIMEOUT_S,
    )

    print(f"✓ AVU built: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
