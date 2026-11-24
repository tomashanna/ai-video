#!/bin/bash
# Quema captions legibles (blanco, contorno + sombra, lower-third) sobre footage.
# Genera un .ass con PlayRes = dimensiones reales (fontsize/margen en px reales)
# y quema con libass. Portable: crea su propia config de fontconfig si falta
# (en macOS no siempre hay fonts.conf -> libass no resuelve la fuente por nombre).
#
# Uso:
#   scripts/burn-captions.sh <input.mp4> <sub.srt> <W> <H> <fontsize> <marginV> <output.mp4> [bold] [FontName]
#
#   <W> <H>     dimensiones de DISPLAY del video (las que ves; ojo con rotación)
#   bold        0 (regular, default) | -1 (bold)
#   FontName    familia (default "Georgia"); debe existir en el sistema
#
# Ej. testimonio vertical 576x1024, Georgia serif:
#   scripts/burn-captions.sh in.mp4 sub.srt 576 1024 38 130 out.mp4 0 Georgia
set -euo pipefail
if [ "$#" -lt 7 ]; then
  sed -n '2,14p' "$0" >&2
  exit 2
fi
IN="$1"; SRT="$2"; W="$3"; H="$4"; FS="$5"; MV="$6"; OUT="$7"; BOLD="${8:-0}"; FONT="${9:-Georgia}"
command -v ffmpeg >/dev/null || { echo "error: ffmpeg not found on PATH" >&2; exit 2; }
[ -f "$IN" ] || { echo "error: input not found: $IN" >&2; exit 2; }
[ -f "$SRT" ] || { echo "error: srt not found: $SRT" >&2; exit 2; }

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

# mktemp in a private dir (the old `mktemp ...`.ass form leaked the mktemp file and
# produced a path ffmpeg's filter parser could mis-split). Clean up on any exit.
TMPD="$(mktemp -d)"
trap 'rm -rf "$TMPD"' EXIT
ASS="$TMPD/captions.ass"
if command -v ai-video >/dev/null; then
  ai-video make-ass "$SRT" "$ASS" "$W" "$H" "$FS" "$MV" "$BOLD" "$FONT"
else
  uv run --quiet ai-video make-ass "$SRT" "$ASS" "$W" "$H" "$FS" "$MV" "$BOLD" "$FONT"
fi

ffmpeg -y -hide_banner -loglevel error -i "$IN" \
  -vf "ass='${ASS}':fontsdir='${FONTSDIR}'" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k \
  "$OUT"

echo "OK -> $OUT"
