# PACING-MARKERS.md — Target empírico de cuts/min y shot duration

> Generado 2026-05-13 desde análisis de scene detection sobre 7 referentes.
>
> **🎯 SCOPE:** El target "2-7 hard cuts/min" es específico de **F1 (Horror choice)**. F2 tiene 7+ cuts/min, F3 tiene 1-2 cuts/min, F4 tiene 3-5 cuts/min. NO universal.

## 🆕 Hallazgo crítico post Gemini full-video (2026-05-13 PM)

Mi medición previa de "2-7 cuts/min" era con ffmpeg scene detect threshold 0.3 — solo HARD CUTS visibles.

Gemini full-video reveló que la **FELT cadence experiencial** de F1 es muy distinta: **~18-30 cuts perceptibles por minuto**, contando push-ins + parallax shifts + caption innerHTML swaps + SFX impacts como "cuts perceptibles".

**Implicación:** el target real para sentirse "vivo" como @referent-a:
- Hard cuts ffmpeg-detectable: 2-7 /min
- **+ Internal motion shifts (push-in beats, parallax stops)**: cada 3-5s
- **+ Caption swaps Whisper-sync**: ~1 cada 2-3s
- **+ SFX impactos puntuales**: ~1 cada 10-15s

**Result:** UN frame NUNCA debe estar "quieto". Si no hay hard cut, hay push-in / parallax / caption swap / SFX punch. Esa es la diferencia entre "edit pro" y "slideshow con motion".

Ref-04 lo dijo explícito: "Aproximadamente 1 cut cada 1.5 a 2 segundos" (combinando hard + felt).
Ref-05: "18-20 cortes en 60 segundos."

---

## Target empírico: 2-7 cuts/min para horror narrativo

**Evidence (medido con ffmpeg scene detect threshold 0.3):**

| Video | Tipo | Duración | Hard cuts | Cuts/min |
|-------|------|----------|-----------|----------|
| ref-01 | Found footage natural | 72.9s | 9 | 7.4 |
| ref-02 | Movie clip + caption | 43.9s | 1 | 1.4 |
| **ref-03** | **Horror choice narrativo** | **93.3s** | **11** | **7.1** |
| **ref-04** | **Horror choice puertas** | **69.3s** | **3** | **2.6** |
| **ref-05** | **Horror choice puertas** | **71.3s** | **6** | **5.0** |
| **ref-06** | **Horror choice narrativo** | **90.7s** | **3** | **2.0** |
| ref-07 | Profile grid (n/a) | 49.0s | 3 | 3.7 |

**Sweet spot horror narrativo:** **2-7 cuts/min**. Promedio @referent-a (4 videos): 4.2 cuts/min.

---

## Interpretación

### < 2 cuts/min — too static

Riesgo: viewer percibe "video se quedó quieto". Sin internal motion (Ken Burns + parallax), un shot de >30s sin cut **siempre** pierde retención.

**Excepción:** si el shot tiene push-in dramático constante + captions cambiando + SFX evolutivos → puede sostener 30s+. Pero es difícil.

### 2-7 cuts/min — sweet spot

Long shots de 8-20s con internal motion (Ken Burns + parallax). Cuts en decision points narrativos. Cuts NO arbitrarios.

**Distribución típica @referent-a:**
- Setup (0-15s): 1-2 shots
- Cada bifurcación: 2-3 shots
- Climax: 2-4 shots (más rápido para acelerar)
- Counterfactual outro: 1 shot

### 7-12 cuts/min — high-energy

Estilo found footage / news-style. Funciona para hooks virales sin narrativa profunda. NO recomendado para horror narrativo (sobrecarga visual rompe inmersión).

### > 12 cuts/min — MTV/overcut

Riesgo: viewer no procesa, percibe caos. SOLO válido en compilaciones, lyrics videos, viral edits puros.

---

## Por qué 2-7 (no más)

Los referentes que funcionan en horror narrativo NO son highcut. Usan:
1. **Long shots con push-in** (Ken Burns digital constante)
2. **Parallax 3D** (subject vs background, blur bokeh)
3. **Caption innerHTML swap** (cambia el caption sin cortar el shot)
4. **SFX evolution** (drone que sube, breath que se acerca)

Esto mantiene "movimiento percibido" SIN hard cuts. Más cinematic, más inmersivo.

---

## Cuándo cortar (decisión narrativa)

Los cuts deben coincidir con **beats narrativos**, no arbitrarios.

| Beat | Cut sí/no | Por qué |
|------|-----------|---------|
| Decision point ("Ahora debes decidir...") | **SÍ** — cut a wide of objects/scene | Marca la pausa, viewer procesa la opción |
| Consequence reveal (after choice) | **SÍ** — cut a close-up del resultado | Impacto visual del resultado |
| Counterfactual outro ("Si hubieras elegido...") | **SÍ** — cut a escena alternativa | Contraste tonal |
| Mid-narration | **NO** — push-in / parallax | El audio sostiene, el shot evoluciona |
| Setup descriptive | **NO** — long shot con motion interno | Establece tono |
| Cliffhanger final | **NO** o cut suave fade-out | El silencio sostiene |

---

## Shot duration ideal

Distribución validada (@referent-a ref-03 análisis):

```
ref-03 cuts en: 0, 20.7, 40.6, 61.8, 81.8, 87.4, 93.3 (~7 shots clave)
Shot durations: 20.7, 19.9, 21.2, 20.0, 5.6, 5.9s

Distribución:
- 4 long shots de ~20s (setup, bifurcación 1, bifurcación 2, climax setup)
- 2 short shots de ~5s al final (climax + outro)
```

**Pattern:** long shots predominan, short shots solo al climax.

**Recomendación HyperFrames:**
- Setup (0-20s): 1 shot largo
- Cada bifurcación (15-25s): 1-2 shots
- Climax (5-15s): 2-4 shots cortos (acelerar)
- Counterfactual outro (5-10s): 1 shot

---

## Internal motion (sin cut)

Para que un long shot funcione, DEBE tener movimiento percibido. Opciones:

### Ken Burns digital (universal)

```javascript
window.__timelines.main.to('.scene-img', {
  scale: 1.12,           // ~12% zoom over duration
  x: -30,                 // sutil pan
  duration: 18,           // duración del shot
  ease: 'none'
}, scene_start);
```

### Parallax 3D (recomendado para medium shots con sujetos)

```javascript
tl.to('.layer-bg',  { x: -40, scale: 1.18, duration: 18 }, T)
  .to('.layer-mid', { x: -15, scale: 1.08, duration: 18 }, T)
  .to('.layer-fg',  { x:   5, duration: 18 }, T);
```

### Caption innerHTML swap (Whisper-sync)

```javascript
tl.set("#narr-1", { opacity: 1, innerHTML: "Primera frase" }, T);
tl.set("#narr-1", { opacity: 1, innerHTML: "Segunda frase" }, T + 1.5);
tl.set("#narr-1", { opacity: 1, innerHTML: "Tercera frase" }, T + 3.0);
// Continúa cambiando el texto sin cortar el video
```

### SFX evolution

Dentro de un shot largo, los SFX evolucionan:
- 0-5s: ambient base + breath sutil
- 5-10s: drone empieza a subir
- 10-15s: drone climax + impacto sub-bass
- 15-18s: drone fade + tick countdown

Esto da movimiento auditivo sin cortar.

---

## Script de validación

```bash
#!/bin/bash
# scripts/check-pacing.sh — verifica cuts/min target

VIDEO="${1:-renders/draft.mp4}"

DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
CUTS=$(ffmpeg -i "$VIDEO" -filter:v "select='gt(scene,0.3)',showinfo" -f null - 2>&1 \
  | grep -c "pts_time")

# Calculate cuts/min
CUTS_PER_MIN=$(echo "scale=2; $CUTS * 60 / $DURATION" | bc)

echo "Duration: ${DURATION}s"
echo "Hard cuts: $CUTS"
echo "Cuts/min: $CUTS_PER_MIN"

# Validate range
if (( $(echo "$CUTS_PER_MIN < 2" | bc -l) )); then
  echo "⚠️ Demasiado static (<2 cuts/min). Considerar agregar cuts en decision points."
  exit 2
elif (( $(echo "$CUTS_PER_MIN > 7" | bc -l) )); then
  echo "⚠️ Demasiado overcut (>7 cuts/min). Considerar consolidar shots."
  exit 2
else
  echo "✓ Pacing en sweet spot (2-7 cuts/min)"
  exit 0
fi
```

---

## Integración con pre-render-gate

**Q17. ¿Cuts/min está en rango 2-7?**

```bash
bash scripts/check-pacing.sh renders/draft.mp4 || echo "Fix pacing antes de stop point"
```

Exit 0 = pass. Exit 2 = warning (no bloquea, pero requiere justificación en POST-MORTEM).

---

## Anti-patterns

❌ **Cortar cada 2-3s "para mantener engagement":** rompe inmersión narrativa. El horror narrativo necesita long shots que dejen respirar el tono.

❌ **Long shots sin internal motion:** el shot de 20s sin Ken Burns / parallax / captions cambiando → "se quedó quieto" → bounce.

❌ **Cuts arbitrarios mid-narration:** rompe el flow del audio. El cut debe coincidir con beat narrativo (decision, consequence, counterfactual).

❌ **>7 cuts/min en horror narrativo:** rompe inmersión. Si necesitás más cuts, repensar si el formato debería ser highcut viral en lugar de narrativo.

---

## Casos disparadores

- **mina-abandonada v15** (exitosa): 12 cuts en 90s = 8 cuts/min, ligeramente sobre el target. Funcionó pero con riesgo. Codificar 2-7 hace replicable más conservador.
- **pueblo-fantasma-desierto v2** (fallida): 4 cuts en 90s = 2.7 cuts/min. En target, PERO con shots estáticos sin internal motion → percibido como "quieto". El target solo es válido si los shots tienen Ken Burns + parallax + caption swap.

**Conclusión:** target de cuts/min es necesario pero no suficiente. También requiere internal motion en cada shot.
