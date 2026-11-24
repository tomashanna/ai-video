"""Convert SRT to ASS with PlayRes equal to the real video size (exact pixel font sizes).

Why: when ffmpeg's ``subtitles`` filter burns an SRT, libass uses a default script
resolution (~384x288); the font size is interpreted there and then scaled to the real
height, so captions end up huge and misplaced. Writing an ``.ass`` whose PlayResX/Y are
the real dimensions keeps font size and margins in real pixels.

Style: white, outline + soft shadow, lower third (Alignment 2) — readable captions on real
footage without covering faces.

Usage:
    ai-video make-ass in.srt out.ass --width 1080 --height 1920 --font-size 64 --margin-v 380
    ai-video make-ass in.srt out.ass 576 1024 38 130 [bold] [FontName]   # legacy positional form
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_TS = re.compile(r"^(\d+):(\d{1,2}):(\d{1,2})[,.](\d{1,3})$")


def to_ass_time(t: str) -> str:
    """SRT timestamp ``HH:MM:SS,mmm`` -> ASS ``H:MM:SS.cc`` (centiseconds, carry-correct)."""
    m = _TS.match(t.strip())
    if not m:
        raise ValueError(f"bad SRT timestamp: {t!r}")
    h, mi, s = (int(g) for g in m.groups()[:3])
    ms = int(m.group(4).ljust(3, "0"))  # "04" means 40 ms
    total_cs = round(((h * 60 + mi) * 60 + s) * 100 + ms / 10)
    h, rem = divmod(total_cs, 360000)
    mi, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{mi:02d}:{s:02d}.{cs:02d}"


def escape_ass_text(text: str) -> str:
    """Escape characters libass would treat as override blocks."""
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


@dataclass(frozen=True)
class Cue:
    start: str
    end: str
    text: str


def parse_srt(content: str) -> list[Cue]:
    cues = []
    for block in re.split(r"\n\s*\n", content.replace("\r\n", "\n").strip()):
        lines = [ln for ln in block.splitlines() if ln.strip()]
        idx = next((i for i, ln in enumerate(lines) if "-->" in ln), None)
        if idx is None or idx + 1 >= len(lines):
            continue
        start, end = (x.strip().split(" ")[0] for x in lines[idx].split("-->"))
        text = "\\N".join(escape_ass_text(ln) for ln in lines[idx + 1 :])
        cues.append(Cue(to_ass_time(start), to_ass_time(end), text))
    return cues


def build_ass(cues: list[Cue], width: int, height: int, font_size: int, margin_v: int,
              bold: int = 0, font: str = "Georgia") -> str:
    if width <= 0 or height <= 0 or font_size <= 0 or margin_v < 0:
        raise ValueError("width/height/font size must be > 0 and margin >= 0")
    if bold not in (0, -1):
        raise ValueError("bold must be 0 (regular) or -1 (bold)")
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{font_size},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,{bold},0,0,0,100,100,0,0,1,3,2,2,40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    body = "".join(f"Dialogue: 0,{c.start},{c.end},Default,,0,0,0,,{c.text}\n" for c in cues)
    return header + body


def main() -> int:
    p = argparse.ArgumentParser(description="SRT -> ASS with real PlayRes")
    p.add_argument("srt", type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("pos", nargs="*", help="legacy: W H fontsize marginV [bold] [FontName]")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--font-size", type=int)
    p.add_argument("--margin-v", type=int)
    p.add_argument("--bold", type=int, default=None, choices=(0, -1))
    p.add_argument("--font", default=None)
    a = p.parse_args()

    pos = list(a.pos)
    try:
        width = a.width if a.width is not None else int(pos[0])
        height = a.height if a.height is not None else int(pos[1])
        fs = a.font_size if a.font_size is not None else int(pos[2])
        mv = a.margin_v if a.margin_v is not None else int(pos[3])
    except (IndexError, ValueError):
        p.error("width, height, font size and margin-v are required")
    bold = a.bold if a.bold is not None else int(pos[4]) if len(pos) > 4 else 0
    font = a.font or (pos[5] if len(pos) > 5 else "Georgia")

    try:
        cues = parse_srt(a.srt.read_text(encoding="utf-8"))
        a.out.write_text(build_ass(cues, width, height, fs, mv, bold, font), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"OK -> {a.out}  ({len(cues)} cues, PlayRes {width}x{height}, font={font}, fs={fs}, mv={mv})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
