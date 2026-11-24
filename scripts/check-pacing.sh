#!/bin/bash
# scripts/check-pacing.sh — verifica cuts/min target empírico (2-7 para horror narrativo)
#
# Generado 2026-05-13 desde análisis de 7 referentes.
# Cuts detectados con ffmpeg scene threshold 0.3 (hard cuts).
# Long shots con internal motion (Ken Burns, parallax) NO se cuentan como cuts.
#
# Usage:
#   scripts/check-pacing.sh renders/draft.mp4
#
# Exit codes:
#   0 = pass (2-7 cuts/min)
#   2 = warning (fuera de rango pero no bloquea)

set -e

VIDEO="${1:-renders/draft.mp4}"

if [ ! -f "$VIDEO" ]; then
  echo "ERROR: video not found: $VIDEO"
  exit 1
fi

DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
CUTS=$(ffmpeg -hide_banner -i "$VIDEO" \
  -filter:v "select='gt(scene,0.3)',showinfo" \
  -f null - 2>&1 | grep -c "pts_time")

CUTS_PER_MIN=$(echo "scale=2; $CUTS * 60 / $DURATION" | bc)

echo "▶ Pacing check: $VIDEO"
echo "  Duration:  ${DURATION}s"
echo "  Hard cuts: $CUTS"
echo "  Cuts/min:  $CUTS_PER_MIN"
echo ""

# Validate range (2-7 cuts/min)
LOW=$(echo "$CUTS_PER_MIN < 2" | bc -l)
HIGH=$(echo "$CUTS_PER_MIN > 7" | bc -l)

if [ "$LOW" = "1" ]; then
  echo "⚠️  TOO STATIC — <2 cuts/min."
  echo "   Riesgo: viewer percibe 'video quieto'."
  echo "   Fix: agregar cuts en decision points narrativos O verify internal motion (Ken Burns + parallax) en cada shot."
  echo "   Ver: ai-video-production/PACING-MARKERS.md"
  exit 2
fi

if [ "$HIGH" = "1" ]; then
  echo "⚠️  TOO OVERCUT — >7 cuts/min."
  echo "   Riesgo: viewer no procesa, rompe inmersión narrativa."
  echo "   Fix: consolidar shots, usar long shots con caption innerHTML swap."
  echo "   Ver: ai-video-production/PACING-MARKERS.md"
  exit 2
fi

echo "✅ PASS — pacing en sweet spot (2-7 cuts/min)"
echo "   Promedio @referent-a (4 referentes): 4.2 cuts/min"
exit 0
