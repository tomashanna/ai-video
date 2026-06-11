#!/bin/bash
# Quema captions legibles (blanco, contorno + sombra, lower-third) sobre footage.
# Genera un .ass con PlayRes = dimensiones reales (fontsize/margen en px reales)
# y quema con libass. Portable: crea su propia config de fontconfig si falta
# (en macOS no siempre hay fonts.conf -> libass no resuelve la fuente por nombre).
#
# Uso:
#   burn-captions.sh <input.mp4> <sub.srt> <W> <H> <fontsize> <marginV> <output.mp4> [bold] [FontName]
#
#   <W> <H>     dimensiones de DISPLAY del video (las que ves; ojo con rotación)
#   bold        0 (regular, default) | -1 (bold)
#   FontName    familia (default "Georgia"); debe existir en el sistema
#
# Ej. testimonio vertical 576x1024, Georgia serif:
#   burn-captions.sh in.mp4 sub.srt 576 1024 38 130 out.mp4 0 Georgia
set -euo pipefail
IN="$1"; SRT="$2"; W="$3"; H="$4"; FS="$5"; MV="$6"; OUT="$7"; BOLD="${8:-0}"; FONT="${9:-Georgia}"

DIR="$(cd "$(dirname "$0")" && pwd)"

# --- fontconfig portable (macOS): crear config mínima si no hay una utilizable ---
FCFILE="${FONTCONFIG_FILE:-/tmp/video-editor-fonts.conf}"
if [ ! -f "$FCFILE" ]; then
  mkdir -p /tmp/video-editor-fc-cache
  cat > "$FCFILE" <<'EOF'
<?xml version="1.0"?>
<fontconfig>
  <dir>/System/Library/Fonts</dir>
  <dir>/System/Library/Fonts/Supplemental</dir>
  <dir>/Library/Fonts</dir>
  <dir>~/Library/Fonts</dir>
  <cachedir>/tmp/video-editor-fc-cache</cachedir>
</fontconfig>
EOF
fi
export FONTCONFIG_FILE="$FCFILE"
FONTSDIR="/System/Library/Fonts/Supplemental"

ASS="$(mktemp -t veditcap).ass"
python3 "$DIR/make_ass.py" "$SRT" "$ASS" "$W" "$H" "$FS" "$MV" "$BOLD" "$FONT"

ffmpeg -y -hide_banner -loglevel error -i "$IN" \
  -vf "ass=${ASS}:fontsdir=${FONTSDIR}" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"

rm -f "$ASS"
echo "OK -> $OUT"
