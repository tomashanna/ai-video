"""Synthetic media fixtures + probing with ffmpeg (optional dependency).

Everything is generated on the fly with ``lavfi`` sources — no binary fixtures in git.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from ai_video.proc import run


def have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def make_clip(
    out: Path,
    *,
    seconds: float = 3.0,
    size: str = "1080x1920",
    fps: int = 30,
    tone_lufs: float | None = -14.0,
    freq: int = 440,
) -> Path:
    """Test-pattern video + sine tone, loudness-normalised to ``tone_lufs`` (None = raw -30 dBFS)."""
    out.parent.mkdir(parents=True, exist_ok=True)
    af = f"loudnorm=I={tone_lufs}:TP=-1.5:LRA=7" if tone_lufs is not None else "volume=-30dB"
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size={size}:rate={fps}:duration={seconds}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency={freq}:sample_rate=48000:duration={seconds}",
            "-af",
            af,
            "-ar",
            "48000",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-preset",
            "ultrafast",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-shortest",
            str(out),
        ],
        timeout=300,
    )
    return out


@dataclass(frozen=True)
class Probe:
    duration_s: float
    width: int
    height: int
    fps: float


def probe(path: Path) -> Probe:
    res = run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        timeout=60,
    )
    data = json.loads(res.stdout)
    v = next(s for s in data["streams"] if s["codec_type"] == "video")
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    return Probe(float(data["format"]["duration"]), int(v["width"]), int(v["height"]), num / den)


def loudness(path: Path) -> tuple[float, float]:
    """(integrated LUFS, true peak dBTP) via the ebur128 filter."""
    res = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-filter_complex",
            "ebur128=peak=true",
            "-f",
            "null",
            "-",
        ],
        timeout=300,
        check=True,
    )
    summary = res.stderr[res.stderr.rfind("Summary:") :]
    i = re.search(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", summary)
    tp = re.search(r"Peak:\s+(-?\d+(?:\.\d+)?) dBFS", summary)
    if not i:
        raise ValueError("could not parse integrated loudness")
    return float(i.group(1)), float(tp.group(1)) if tp else float("nan")
