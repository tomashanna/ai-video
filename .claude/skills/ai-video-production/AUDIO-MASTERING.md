# AUDIO-MASTERING.md — Mastering -14 LUFS (Instagram Reels standard)

> Generado 2026-05-13 desde análisis empírico de 7 referentes (LUFS medido -13.76 a -14.45, sin excepción).

---

## ⛔ HARD RULE — LUFS integrado en -14 ±0.5 dB

**Scope:** 🌐 Universal — aplica a TODOS los videos publicados en Instagram Reels, Reels Mix, Stories, Feed video.

**Why:** Instagram normaliza loudness a -14 LUFS. Subir un video más alto (-10, -12) → Instagram lo baja agresivamente → suena "apagado" comparado con otros videos. Subir más bajo (-16, -20) → audio percibe "débil" → bounce. **-14 es el sweet spot exacto.**

**Evidence:**
- 7/7 referentes analizados están entre -13.76 y -14.45 LUFS integrado
- Promedio: -13.96 LUFS (n=7)
- Confianza estadística: muy alta — sin un solo outlier

---

## Pipeline obligatorio post-mix

### Paso 1 — Medir LUFS actual

```bash
ffmpeg -i renders/draft.mp4 \
  -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json \
  -f null - 2>&1 | grep -A 12 '"input_i"'
```

Output esperado:
```json
{
  "input_i": "-12.34",            // LUFS integrado actual
  "input_tp": "-0.45",            // True peak actual
  "input_lra": "9.20",            // Loudness range actual
  "input_thresh": "-22.84",
  "output_i": "-14.00",           // Target (siempre -14)
  "output_tp": "-1.00",
  "output_lra": "9.20",
  "output_thresh": "-24.50",
  "normalization_type": "dynamic"
}
```

### Paso 2 — Decidir si normalizar

| Condición | Acción |
|-----------|--------|
| `input_i` entre -13.5 y -14.5 | ✅ Pass — NO normalizar, ya está en target |
| `input_i` entre -12 y -13.5 OR -14.5 y -16 | ⚠️ Normalizar (loudnorm 2-pass) |
| `input_i` < -16 OR > -12 | ❌ Re-revisar mix (algo está mal en el balance) |

### Paso 3 — Normalización 2-pass (gold standard)

**Primera pasada (medición):**
```bash
ffmpeg -i renders/draft.mp4 \
  -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json \
  -f null - 2>&1 | tee /tmp/loudnorm-pass1.log
```

Extraer valores: `measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`.

**Segunda pasada (aplicar):**
```bash
ffmpeg -i renders/draft.mp4 \
  -af loudnorm=I=-14:TP=-1:LRA=11:\
measured_I=<measured_I>:\
measured_TP=<measured_TP>:\
measured_LRA=<measured_LRA>:\
measured_thresh=<measured_thresh>:\
linear=true:print_format=summary \
  -c:v copy -c:a aac -b:a 192k \
  renders/draft-mastered.mp4
```

**Por qué 2-pass:** la primera pasada mide con precisión, la segunda aplica una corrección lineal (no dinámica) que preserva el "feel" del mix. Single-pass dinámico puede sonar comprimido.

### Paso 4 — Verificar resultado

```bash
ffmpeg -i renders/draft-mastered.mp4 \
  -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json \
  -f null - 2>&1 | grep '"input_i"'
```

Debe mostrar `"input_i": "-14.0X"` (±0.1 dB acceptable).

---

## Script automatizado

```bash
#!/bin/bash
# scripts/master-audio.sh — 2-pass LUFS normalization to -14
INPUT="$1"
OUTPUT="${2:-${INPUT%.mp4}-mastered.mp4}"

if [ -z "$INPUT" ]; then
  echo "Usage: master-audio.sh <input.mp4> [output.mp4]"
  exit 1
fi

# Pass 1: measure
JSON=$(ffmpeg -i "$INPUT" \
  -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json \
  -f null - 2>&1 | grep -A 12 '"input_i"' | head -12)

MEASURED_I=$(echo "$JSON" | grep input_i | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_TP=$(echo "$JSON" | grep input_tp | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_LRA=$(echo "$JSON" | grep input_lra | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
MEASURED_THRESH=$(echo "$JSON" | grep input_thresh | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')

echo "Medido: I=$MEASURED_I TP=$MEASURED_TP LRA=$MEASURED_LRA Thresh=$MEASURED_THRESH"

# Pass 2: apply
ffmpeg -y -i "$INPUT" \
  -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=$MEASURED_I:measured_TP=$MEASURED_TP:measured_LRA=$MEASURED_LRA:measured_thresh=$MEASURED_THRESH:linear=true:print_format=summary" \
  -c:v copy -c:a aac -b:a 192k \
  "$OUTPUT"

echo "✓ Mastered: $OUTPUT"
```

Uso: `scripts/master-audio.sh renders/draft.mp4 renders/final.mp4`

---

## Targets de mastering

| Métrica | Target | Tolerancia | Por qué |
|---------|--------|------------|---------|
| **Integrated LUFS** | -14 dB | ±0.5 dB | Instagram normalization |
| **True peak** | ≤ -1 dBTP | hard limit | Evitar inter-sample clipping en codecs lossy |
| **LRA (Loudness Range)** | 6-11 LU | preferible | Demasiado bajo (<5) = sobrecomprimido. Demasiado alto (>15) = inconsistente |
| **Short-term LUFS max** | -10 dB | hard ceiling | Picos no deben superar -10 LUFS (3 sec window) |

---

## Reglas previas (en el mix, antes de mastering)

Para llegar a -14 LUFS limpio, el mix debe estar **antes** en:

| Layer | Volumen relativo | dB típico |
|-------|------------------|-----------|
| **Narración** (foreground) | 0 dB ref | -8 a -12 LUFS short-term |
| **Música** (background) | -12 dB cuando hay narración, -4 dB cuando solo música | -22 a -18 LUFS short-term |
| **Ambient continuo** (forest, wind) | -6 dB cuando hay narración, -3 dB sin narración | -24 a -20 LUFS short-term |
| **SFX impacto** (one-shot) | 0 dB ref (igual narración) o +3 dB para peak | -8 a -10 LUFS peak |
| **Tick countdown** | -6 dB | -16 a -18 LUFS |

Si el mix entra a master en estos rangos, la pasada loudnorm solo ajusta ±0.5-2 dB. Si entra muy desbalanceado, loudnorm comprime → suena "aplastado".

---

## Anti-patterns

❌ **Aplicar loudnorm dinámico single-pass:** comprime artísticamente, mata el rango dinámico. Usar 2-pass linear=true.

❌ **Sin medir antes:** loudnorm fuerza la salida a -14 sin importar cuánto comprima. Si el input está a -8, va a aplastar -6 dB de dinámica.

❌ **Master por canal individual:** loudnorm sobre la narración sola, luego sobre música sola, luego mix. Resultado: ratio descontrolado. Master SIEMPRE sobre el mix final completo.

❌ **Re-master después de cada cambio:** el mastering es la ÚLTIMA pasada antes de publicar. Si después del master cambian assets, re-render desde el mix raw y re-master.

❌ **Skipping en "ya suena bien":** la percepción humana es no-confiable a este nivel. Medir SIEMPRE con ffmpeg loudnorm.

---

## Integración con pre-render-gate

Este pipeline va como **Q18 en pre-render-gate**:

```bash
# Q18 — LUFS check
MEASURED=$(ffmpeg -i renders/draft.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 \
  | grep '"input_i"' | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')

# Pass if within ±0.5 of -14
if (( $(echo "$MEASURED >= -14.5 && $MEASURED <= -13.5" | bc -l) )); then
  echo "✓ LUFS pass: $MEASURED"
else
  echo "✗ LUFS fail: $MEASURED (target -14 ±0.5). Run scripts/master-audio.sh"
  exit 1
fi
```

Si falla → re-master con `scripts/master-audio.sh` → re-render → re-check.

---

## Casos disparadores (por qué existe este doc)

- **pueblo-fantasma-desierto v2:** sin mastering check. LUFS desconocido. Publicación se vio "apagada" al lado de @referent-a.
- **bosque-abandonado v10, mina-abandonada v15:** funcionaron porque (afortunadamente) cayeron cerca de -14 por accidente. Sin medición fue suerte.

Codificar el target hace el éxito reproducible.
