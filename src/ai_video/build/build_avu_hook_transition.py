#!/usr/bin/env python3
"""
build_avu_hook_transition.py — Build hook-transition-warm-whoosh.mp4 AVU

Spec:
- 0.5s, 1080×1920, 30 fps
- Visual: warm light flash (orange-yellow gradient fade-in + fade-out)
- Audio: cut-warm-whoosh.mp3 from library (-10 dB ducked)
- Purpose: shot-to-shot warm transition signal (matadero→cliffhanger cut at ~67s)
"""
import subprocess
import tempfile
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from ai_video.paths import avu_dir, library_dir, repo_root

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

PROJECT_ROOT = repo_root()
AVU_DIR = avu_dir()
# Unique, private work dir (was a fixed /tmp path shared across runs/users).
TMP = Path(tempfile.mkdtemp(prefix="ai-video-avu_hook_transition-"))

W, H = 1080, 1920
FPS = 30
DUR_S = 0.5
N_FRAMES = int(FPS * DUR_S)  # 15 frames

OUT_VIDEO = AVU_DIR / "hook-transition-warm-whoosh.mp4"
WHOOSH_PATH = library_dir() / "sfx/cuts/cut-warm-whoosh.mp3"


def draw_frame(i):
    """Frame i (0..14): warm flash bell curve."""
    t = i / (N_FRAMES - 1)
    bell = 4.0 * t * (1.0 - t)
    intensity = bell * 0.85
    img = Image.new("RGB", (W, H), (0, 0, 0))
    if intensity > 0.01:
        overlay = Image.new("RGB", (W, H), (255, 140, 50))
        mask = Image.new("L", (W, H), int(intensity * 255))
        img = Image.composite(overlay, img, mask)
        # Radial gradient bright center
        draw = ImageDraw.Draw(img)
        cx, cy = W // 2, H // 2
        for r in range(0, 600, 50):
            alpha = max(0, int(intensity * (255 - r // 3)))
            color = (255, 240 - r // 6, 200 - r // 4)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
        img = img.filter(ImageFilter.GaussianBlur(radius=30))
    return img


def main():
    AVU_DIR.mkdir(exist_ok=True, parents=True)
    for i in range(N_FRAMES):
        draw_frame(i).save(TMP / f"frame_{i:04d}.png")

    silent = TMP / "silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS),
        "-i", str(TMP / "frame_%04d.png"),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p", "-vf", "format=yuv420p",
        "-color_range", "tv",
        "-r", str(FPS),
        str(silent),
    ], check=True, timeout=SUBPROCESS_TIMEOUT_S)

    # Audio: cut-warm-whoosh trimmed to 0.5s + -10 dB
    audio = TMP / "audio.mp3"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(WHOOSH_PATH),
        "-t", str(DUR_S),
        "-af", "volume=-10dB",
        "-c:a", "libmp3lame", "-b:a", "192k",
        str(audio),
    ], check=True, timeout=SUBPROCESS_TIMEOUT_S)

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(silent), "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
        "-shortest",
        str(OUT_VIDEO),
    ], check=True, timeout=SUBPROCESS_TIMEOUT_S)

    print(f"✓ AVU built: {OUT_VIDEO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
