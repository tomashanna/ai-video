#!/usr/bin/env python3
"""SRT -> ASS con PlayRes = dimensiones reales del video.

Por qué: al quemar un SRT con el filtro `subtitles` de ffmpeg, libass usa una
resolución de script por defecto (~384x288); el Fontsize se interpreta en ese
espacio y luego se escala al alto real del video -> queda GIGANTE y mal ubicado.
Generando un .ass con PlayResX/Y = dimensiones reales, el fontsize y el margen
quedan en PIXELES REALES y la posición es exacta. (Gotcha validado en Palti.)

Estilo: blanco, contorno + sombra suave, lower-third (Alignment 2). Pensado para
captions legibles sobre footage real sin tapar caras.

Uso:
  make_ass.py <in.srt> <out.ass> <W> <H> <fontsize> <marginV> [bold] [FontName]

  bold     : 0 (regular, default) | -1 (bold)
  FontName : familia de fuente (default "Georgia"). Debe existir en el sistema.
"""
import sys, re

srt, out = sys.argv[1], sys.argv[2]
W, H, fs, mv = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
bold = sys.argv[7] if len(sys.argv) > 7 else "0"
font = sys.argv[8] if len(sys.argv) > 8 else "Georgia"


def to_ass_time(t):
    # "00:00:03,040" -> "0:00:03.04"
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    cs = int(round(int(ms) / 10.0))
    if cs == 100:
        cs = 99
    return f"{int(h)}:{int(m):02d}:{int(s):02d}.{cs:02d}"


blocks = re.split(r"\n\s*\n", open(srt, encoding="utf-8").read().strip())
dialogues = []
for b in blocks:
    lines = [l for l in b.splitlines() if l.strip() != ""]
    if len(lines) < 2:
        continue
    tl_idx = next((i for i, l in enumerate(lines) if "-->" in l), None)
    if tl_idx is None:
        continue
    start, end = [x.strip() for x in lines[tl_idx].split("-->")]
    text = "\\N".join(lines[tl_idx + 1:])
    dialogues.append((to_ass_time(start), to_ass_time(end), text))

header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{fs},&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,{bold},0,0,0,100,100,0,0,1,3,2,2,40,40,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

with open(out, "w", encoding="utf-8") as f:
    f.write(header)
    for start, end, text in dialogues:
        f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")

print(f"OK -> {out}  ({len(dialogues)} cues, PlayRes {W}x{H}, font={font}, fs={fs}, mv={mv})")
