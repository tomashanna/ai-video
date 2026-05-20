#!/bin/bash
# master-audio.sh — 2-pass LUFS normalization to Instagram Reels standard (-14 LUFS)
#
# Generado 2026-05-13 desde análisis empírico de 7 referentes (LUFS -13.76 a -14.45).
#
# Pipeline:
#   Pass 1: medir input loudness (loudnorm print_format=json)
#   Pass 2: aplicar corrección lineal (preserva dinámica vs single-pass dinámico)
#
# Usage:
#   master-audio.sh renders/draft.mp4                  # outputs renders/draft-mastered.mp4
#   master-audio.sh renders/draft.mp4 renders/final.mp4

set -e

INPUT="$1"
OUTPUT="${2:-${INPUT%.mp4}-mastered.mp4}"

if [ -z "$INPUT" ]; then
  echo "Usage: master-audio.sh <input.mp4> [output.mp4]"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "ERROR: input not found: $INPUT"
  exit 1
fi

echo "▶ Mastering to -14 LUFS Instagram standard"
echo "  Input:  $INPUT"
echo "  Output: $OUTPUT"
echo ""

# Pass 1: measure
echo "📊 Pass 1 — measuring input loudness..."
PASS1_OUTPUT=$(ffmpeg -hide_banner -i "$INPUT" \
  -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=json" \
  -f null - 2>&1)

# Extract JSON block (loudnorm prints to stderr)
JSON=$(echo "$PASS1_OUTPUT" | sed -n '/^{/,/^}/p')

MEASURED_I=$(echo "$JSON" | grep input_i | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_TP=$(echo "$JSON" | grep input_tp | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_LRA=$(echo "$JSON" | grep input_lra | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_THRESH=$(echo "$JSON" | grep input_thresh | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')

if [ -z "$MEASURED_I" ]; then
  echo "ERROR: could not parse loudnorm output. Run ffmpeg manually to debug:"
  echo "  ffmpeg -i $INPUT -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -"
  exit 2
fi

echo "  Measured: I=$MEASURED_I LUFS  TP=$MEASURED_TP dBTP  LRA=$MEASURED_LRA LU  Thresh=$MEASURED_THRESH"
echo ""

# Check if already in target range
DELTA=$(echo "$MEASURED_I - (-14)" | bc -l)
ABS_DELTA=$(echo "$DELTA" | tr -d '-')
IN_RANGE=$(echo "$ABS_DELTA <= 0.5" | bc -l)

if [ "$IN_RANGE" = "1" ]; then
  echo "✓ Already in target (-14 ±0.5 dB). Copying without normalization."
  cp "$INPUT" "$OUTPUT"
  exit 0
fi

# Pass 2: apply linear correction
echo "🎚  Pass 2 — applying linear correction to -14 LUFS..."
ffmpeg -y -hide_banner -loglevel warning -i "$INPUT" \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$MEASURED_I:measured_TP=$MEASURED_TP:measured_LRA=$MEASURED_LRA:measured_thresh=$MEASURED_THRESH:linear=true:print_format=summary" \
  -c:v copy -c:a aac -b:a 192k \
  "$OUTPUT"

echo ""
echo "✅ Mastered: $OUTPUT"
echo ""

# Verify
echo "🔍 Verifying output..."
VERIFY=$(ffmpeg -hide_banner -i "$OUTPUT" \
  -af "loudnorm=I=-14:TP=-1:LRA=11:print_format=json" \
  -f null - 2>&1 | sed -n '/^{/,/^}/p' | grep input_i | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')

echo "  Final LUFS: $VERIFY (target -14 ±0.5)"

# Verify pass
VERIFY_DELTA=$(echo "$VERIFY - (-14)" | bc -l)
VERIFY_ABS=$(echo "$VERIFY_DELTA" | tr -d '-')
VERIFY_PASS=$(echo "$VERIFY_ABS <= 0.5" | bc -l)

if [ "$VERIFY_PASS" = "1" ]; then
  echo "  ✓ PASS — Instagram-ready"
  exit 0
else
  echo "  ⚠ WARNING — final LUFS outside ±0.5 dB. May need manual review."
  exit 0  # don't fail, just warn
fi
