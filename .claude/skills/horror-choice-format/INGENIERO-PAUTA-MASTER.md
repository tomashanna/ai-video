# INGENIERO-PAUTA-MASTER.md — Autoridad TÉCNICA del INGENIERO para horror-choice × reel

> **Doc gemelo de `PAUTA-MASTER.md`** (autoridad creativa del arquitecto). Este doc es **autoridad técnica empírica del INGENIERO** derivada de **10 referentes F1 canónicos**.
>
> **Versión 2** — 2026-05-15. **n=10 referentes** (ref-03, ref-04, ref-05, ref-06, ref-08, ref-09, ref-10, ref-11, ref-12, ref-13). Todas las transcripciones completas via Whisper-small.
>
> ⛔ **NUNCA usar nuestras producciones (mina, bosque, elige, pueblo) como referencia técnica.** Están en `/referent-analysis/our-production-archive/` con prefijo NO AUTORIDAD. Medido empíricamente: nuestras producciones tienen pace ~20-30% más lento que la mediana referente.

---

## 0. Metodología

- **n=10 referentes F1** (horror-choice de `@referent-a` y similares)
- Fuente raw: `/referent-analysis/F1-INGENIERO-MEASUREMENTS.json`
- Source MP4s: `/videosref_elige_tu_compa/ScreenRecording_05-13-2026_*.MP4`
- Tools usados:
  - **Whisper small** (CLI, fp16=False, language=es) para transcripción
  - **ffmpeg ebur128** para LUFS integrated + por sección
  - **librosa 0.11** (beat_track, rms) para BPM + RMS dB
  - **Pillow + numpy** para HSV / brightness / vignette / grain de frames
- Section split: hook=0-15% / dilemmas=15-80% / outro=80-100% del duration

### Caveats importantes
- ref-03..ref-06 transcriptions pre-existentes con Whisper model desconocido. ref-08..ref-13 transcritos con Whisper-small CPU. WPM bimodal posible (precision varía 2-5% entre modelos).
- Music BPM medido sobre mezcla narración+música → librosa sesgado cuando narración domina. Para BPM puro: separar stems con Demucs (TODO).
- Cuts/min "de-clustered" = excluye flash bursts (cuts <0.5s entre sí). Raw scene-detector counts inflado 2-4x. **Usar `cuts_per_min` (de-clustered), NO `cuts_per_min_raw`.**

---

## 1. NARRACIÓN — la métrica más crítica

### 1.1 Speaking rate WPM (palabras ÷ tiempo HABLANDO, excluye pausas)

**Esta es la rate que controla el TTS engine (ElevenLabs `--speed`).**

| Métrica | Min | Max | Avg | Median | p25 | p75 | std |
|---------|-----|-----|-----|--------|-----|-----|-----|
| **Speaking WPM total** | **115** | **195** | **162** | **165** | **153** | **180** | 25 |
| Speaking WPM hook (0-15%) | 105 | 212 | 155 | 154 | 141 | 177 | 34 |
| Speaking WPM dilemmas (15-80%) | 111 | 202 | 162 | 167 | 158 | 176 | 26 |
| Speaking WPM outro (80-100%) | 134 | 203 | 165 | 167 | 140 | 183 | 26 |

**Target operacional**: **153-180 WPM speaking rate** (p25-p75 sweet spot).

**Median = 165 WPM ≈ 2.75 w/s** ← target ideal si no hay constraint específico.

**En w/s (palabras/segundo speaking)**:
- Range válido: 1.9-3.25 w/s
- **Sweet spot p25-p75**: **2.55-3.0 w/s**
- **Target ideal (median)**: **2.75 w/s**

#### Cómo elegir dentro del range según tono del video

| Tono narrativo | Speaking WPM | w/s |
|----------------|--------------|-----|
| Contemplativo / lento (slow horror) | 153-165 (p25-median) | 2.55-2.75 |
| **Neutro** (estándar horror-choice) | **165-175 (median-medium)** | **2.75-2.9** |
| Punchy / urgent (thriller energy) | 175-185 (medium-p75) | 2.9-3.1 |
| Excepcional / specific reason | 185-195 (p75-max) | 3.1-3.25 |

> Caso real: maikol-crucero (Thriller dance subject, 2026-05-15). Ingeniero propuso 3.0 w/s = 180 WPM. Cae en "Punchy / urgent" categoría → válido para el subject matter. No es óptimo (overshoot vs median 165), pero está dentro del p25-p75.

### 1.2 Coverage WPM (palabras ÷ duración total video)

Si user pregunta "qué denso narrativamente debe ser" usá coverage. Si pregunta "qué velocidad TTS" usá speaking (1.1).

| Min | Max | Avg | Median |
|-----|-----|-----|--------|
| ~115 | ~170 | ~145 | ~144 |

Coverage = speaking × coverage_pct. Para target median: 165 WPM speaking × 88% coverage = 145 coverage WPM.

### 1.3 Narration coverage %

% del video con narración activa (NO pausas, NO silencios).

| Min | Max | Avg | Median | p25 | p75 |
|-----|-----|-----|--------|-----|-----|
| 77.8% | **96.3%** | **88.2%** | 88.6% | 84.7% | 92.5% |

**Target operacional**: **≥85% coverage** (p25 ≈ 85%).

Implicancia: solo 12-15% del video puede ser silencio/pausa. Si tu video tiene >25% silencios → tartamudea narrativamente (caso pueblo-fantasma-desierto v2: 30.9% coverage = falla).

### 1.4 Avg block duration (duración promedio de cada frase del narrador)

| Min | Max | Avg | Median | p25 | p75 |
|-----|-----|-----|--------|-----|-----|
| 2.1s | 6.8s | **3.6s** | 3.3s | 2.8s | 3.5s |

**Target operacional**: **2.8-3.5s avg** (sweet spot p25-p75).

Implicancia: frases de tamaño medio (5-8 palabras a 165 WPM). NO frases largas (>6s) que se sienten lentas, NO frases cortas (<2s) que tartamudean. ⚠️ Hubo un over-shoot en mi n=5 ("≥4.5s") — con n=10 el target real es 2.8-3.5s.

### 1.5 Pausas

| Métrica | Range | Avg |
|---------|-------|-----|
| Pause count | 1-21 | 9.8 |
| Pause avg duration | 0.41-1.5s | 0.76s |
| Pause max duration | 0.48-2.3s | 1.48s |
| Total pause time | 0.5-14s | 6.8s |

**Pattern**: hay pausas, pero son CORTAS (0.4-0.8s avg). Pausa larga (>2s) reservada para 1 momento dramático específico (decision pop, twist beat).

### 1.6 Cómo aplicar en TTS

#### ElevenLabs (`text_to_speech.convert`)
- **Voice ID canónico nuestro (Tj9l48J9AJbry5yCP5eW)** es LENTO por default → necesita post-procesado con `ffmpeg atempo 2.0x` para llegar a ~170-185 speaking WPM
- **Voice IDs alternativos** (ej. `I0RpMYnjlWe6hUgHLXrb`): usar `--speed 0.95-1.0` ElevenLabs nativo (NO 0.7 — produce 120 WPM = -25% del target)
- Validar con: `python -c "import json; d=json.load(open('output.json')); segs=d['segments']; words=sum(len(s['text'].split()) for s in segs); speak=sum(s['end']-s['start'] for s in segs); print(f'{words/speak*60:.0f} WPM speaking')"`

#### Validación pre-render
```bash
# Si pace WPM < 156 → re-generar TTS con speed +10-15%
# Si pace WPM > 195 → re-generar TTS con speed -5-10%
# Si coverage < 80% → narración hay que extender (más palabras o menos pausas)
```

### 1.7 ⛔ Anti-pattern de nuestras producciones (caso de estudio)

Medido empíricamente: nuestras producciones (mina v15, bosque v10, elige V7) y maikol-crucero hasta 2026-05-15:
- Speaking WPM real ≈ 120 (vs median canónico 165, p25 153)
- Diferencia: **~-20% a -30% del p25 del referente canónico**
- Voice ID `Tj9l48J9AJbry5yCP5eW` + `atempo 2.0x` produce ese pace
- Voice ID `I0RpMYnjlWe6hUgHLXrb` con `--speed 0.7` produce el mismo pace

**Fix por defecto** (apuntar a la median):
- Atempo **2.3x** sobre voice canónico lento → ~165 WPM speaking
- O voice alternativo con **`--speed 0.95`** → ~165 WPM

**Fix por tono** (si el video específico justifica):
- Slow horror contemplativo → atempo 2.1x = 153 WPM (p25)
- Punchy/thriller energy → atempo 2.5x = 180 WPM (p75)

Caso disparador documentado: **maikol-crucero 2026-05-15**. Ingeniero propuso A=2.5 (150 WPM) / B=3.0 (180 WPM) / C=3.4 (204 WPM). Análisis honesto con n=10:
- **Opción A (150 WPM)**: marginalmente debajo del p25 (153) — aceptable para slow horror
- **Opción B (180 WPM)**: en p75 — aceptable para "Thriller dance" subject matter (justificación del ingeniero válida)
- Opción C (204 WPM): sobre max (195) — overshoot

**Veredicto**: ambas A y B son válidas según tono. Para maikol-crucero con su "Thriller energy" justificada, **B es OK**. Para video standard horror-choice, target sería **median 165 WPM** (entre A y B).

---

## 2. AUDIO MIX

### 2.1 LUFS integrated (target Instagram)

| Min | Max | Avg | Median | p25 | p75 | Std |
|-----|-----|-----|--------|-----|-----|-----|
| **-15.20** | **-13.76** | **-14.06** | -13.96 | -14.03 | -13.86 | 0.41 |

**Target operacional**: **-14 ±0.5 LUFS integrated** (9/10 dentro de ±0.5).

Tightness (std 0.41) → todos los referentes masterizan a target Instagram. 1 outlier en -15.2 (ref-XX más quiet del set).

### 2.2 LUFS por sección

| Sección | Min | Max | Avg | Notas |
|---------|-----|-----|-----|-------|
| Hook (0-15%) | -15.3 | -13.2 | -14.0 | similar al integrated |
| Dilemmas (15-80%) | -14.1 | -13.6 | **-13.9** | pico de energía |
| Outro (80-100%) | -14.1 | -13.3 | -13.7 | sutil pico al cliffhanger |

### 2.3 RMS dB por sección (energía relativa)

| Sección | Avg | Notas |
|---------|-----|-------|
| Hook | -21.0 | energía base |
| Dilemmas | **-19.9** | pico (decision tension) |
| **Outro** | **-31.6** | ⚠️ **caída fuerte (-12 dB vs dilemmas)** |

**Pattern crítico descubierto**: el outro tiene RMS dB MUY bajo (-25 a -37 dB en n=5). Esto es **deliberado** — punchline zone con narración íntima/baja energía como contraste al cliffhanger.

**No leer como "audio bug"** — es creative pattern. Si vas a "fix" un outro que se siente "bajo", probablemente estás rompiendo el patrón.

### 2.4 Dynamic range

| Min | Max | Avg |
|-----|-----|-----|
| 18.6 | 22.3 | **20.2 dB** |

Range 18-22 dB → buen pico-valle, no over-compressed. Si tu master tiene range <15 dB = sobre-comprimido. Si >25 dB = audio se va a sentir "ondulado".

### 2.5 Cómo aplicar en mastering

```bash
# Master to -14 LUFS integrated:
ffmpeg -i input.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=summary" output.wav

# Verificar:
ffmpeg -i output.wav -af ebur128 -f null - 2>&1 | grep "I:"
# Debe estar entre -14.3 y -13.6
```

---

## 3. PACING / CUTS

### 3.1 Cuts/min (de-clustered, excluye flash bursts)

| Min | Max | Avg | Median | p25 | p75 |
|-----|-----|-----|--------|-----|-----|
| 1.06 | 8.86 | **4.19** | 4.14 | 2.75 | 4.98 |

**Range válido F1 (n=10)**: **1-9 cuts/min de-clustered**. Sweet spot p25-p75 = **2.75-5.0**.

⚠️ **CRÍTICO — distinción raw vs de-clustered**:
- `ffprobe` / scene-detector raw count infla 2-4x por flash bursts (cuts <0.5s entre sí cuentan como múltiples cuts)
- Ejemplo extremo: ref-13 raw=31.7/min vs de-clustered=8.9/min
- **Usar SIEMPRE de-clustered** (`cuts_per_min`), NO `cuts_per_min_raw`
- Para de-cluster: agrupar cuts dentro de ventana de 0.5s como UN solo cut perceptual

### 3.2 Distribución de cuts por sección — **PATTERN FUERTE PERO NO ABSOLUTO**

| Sección | Median cuts | Avg | Notas |
|---------|-------------|-----|-------|
| **Hook (0-15%)** | **0** | **0.4** | **8/10 referentes tienen 0 cuts** (2 tienen 1-3) |
| Dilemmas (15-80%) | ~3-5 | ~4 | la mayoría de cuts viven acá |
| Outro (80-100%) | ~2 | ~2 | 1-3 cuts para cliffhanger reveal |

**Regla derivada (n=10)**: HOOK típicamente sin cuts (8/10) — es un plano largo continuo con motion interno (Kling, push-in, parallax) durante los primeros 13-14 segundos. **No es 100% universal**, pero el outlier (2/10 con cuts en hook) es excepción no regla.

Implicancia operacional: si tu hook tiene >2 cuts, estás rompiendo el pattern típico. El hook se sostiene por **motion + narrative tension**, NO por cortes.

### 3.3 Tiempo entre cuts

| Métrica | Min | Max | Avg |
|---------|-----|-----|-----|
| Time between cuts avg | 9.8s | 22.7s | 15.1s |
| Long shots >8s count | 1 | 5 | 2.8 |

**Pattern**: cada video tiene **2-3 long shots** (>8s) que sostienen energía sin cortes.

---

## 4. MÚSICA

### 4.1 BPM (beat_track librosa, sobre mezcla completa)

| Min | Max | Avg | Median |
|-----|-----|-----|--------|
| 99 | 161 | **126** | 129 |

**Distribución bimodal**:
- **~100 BPM** (ref-03, ref-08) → drone lento, eerie ambient
- **~135-160 BPM** (ref-04, ref-05, ref-06) → tension build pulsing

**Target operacional**: elegí según archetype del video:
- Setting "abandonado / silencio" → 95-110 BPM
- Setting "noche + persecución / cazas / decisión" → 130-160 BPM

Nota: librosa beat_track sobre mezcla narración+música puede sesgar — para BPM puro de la pista musical idealmente correr sobre stems separados (Demucs). TODO.

---

## 5. VISUAL / COLOR GRADING

### 5.1 Brightness

| Métrica | Avg | Range |
|---------|-----|-------|
| Brightness mean | 69.7 | 53-89 (de 255) |
| Brightness std | 27.0 | variabilidad alta |

Frames están en **27% brightness mean** → look oscurísimo (crushed blacks confirmed). Std alto = high contrast entre lit subjects + dark backgrounds.

### 5.2 Vignette ratio

(brightness center 60% / brightness edges 20%)

| Min | Max | Avg | Median |
|-----|-----|-----|--------|
| 1.28 | 1.56 | **1.43** | 1.42 |

**Target operacional**: **vignette ratio 1.35-1.50** (centro 35-50% más brillante que edges).

Implicancia CSS: `box-shadow: inset 0 0 200px 100px rgba(0,0,0,0.7)` o LUT con vignette ~40% intensity.

### 5.3 Grain variance (proxy de film grain)

| Min | Max | Avg |
|-----|-----|-----|
| 84 | 270 | 172 |

Variabilidad alta. Target operacional: **150-200** = grain visible pero no dominante. Translation a CSS: `noise overlay opacity 0.06-0.10`.

### 5.4 Saturación + dominant hue

| Saturation % avg | Distribution hue dominante (n=10) |
|------------------|------------------------------------|
| 32.0% (range 19-45%) | **4 red / 1 orange / 4 cyan / 1 blue-cyan** |

**Pattern n=10 (CORREGIDO vs n=5)**: el formato F1 es **BIMODAL warm vs cool**, NO todo warm como sugería n=5.
- Warm dominant (5/10): red/orange — settings mining, desierto, bosque rojo, decay
- **Cool dominant (5/10)**: cyan/blue-cyan — settings agua, noche-luna, criptas-acuáticas

Implicancia: la decisión warm vs cool depende del **setting**, no de "formato siempre warm". Si tu setting es agua/noche/luna → cool palette es canónica.

Saturación moderada (~32%) → NO oversaturated. NO desaturated tampoco (>20%).

### 5.5 Frame-to-frame diff (variedad visual)

Avg frame diff: 36.6 (en escala 0-255).
Max: 116.

**Implicancia**: hay variedad visual significativa cada 5s. Si tu render tiene avg diff <20 → demasiada similitud, slideshow feel.

### 5.6 Motion intensity per shot type — REGLA OPERACIONAL (reform 2026-05-16: Ken Burns = FALLBACK only)

Caso disparador: maikol-crucero (issues 8, 9, 11, 14) — múltiples shots estáticos consecutivos crearon feel "aburrido / lento / no cinemático". **Reform 2026-05-16**: Ken Burns degrada de DEFAULT a FALLBACK (último recurso). Animation AI = preferred SIEMPRE.

CLAUDE.md hard rule #6 + #7 + #20 + #21 operacionalizan esta tabla:

| Shot context | Motion target | Fallback (último recurso) |
|---|---|---|
| **Hook 0-15% (primeros ~13-14s)** | **100% Kling** (HOOK VIRAL OVERRIDE per MODEL-BENCHMARK § 2.0) | NO fallback — re-spec si necesario |
| **Decision point + consequences A/B** | **Animation full** (Kling/Seedance/Hailuo según movimiento) | NO fallback — narrative beat crítico |
| **Body horror / muerte / ahogamiento** | **Animation full** + opcionalmente blood/SFX overlay | NO fallback — critical narrative beat |
| **Cliffhanger outro counterfactual** | **Animation full** (warm/cozy motion) | NO fallback — emotional anchor |
| **Establishing setting (>2s)** | **Animation full preferred** (cheap model OK con premium prompt per § 5.7) | Ken Burns SOLO si regen falla 3 veces consecutivas Y shot es esencial |
| **Detail shot (<2s)** | Animation OR Ken Burns aceptable | Ken Burns OK acá |

**🚨 Regla operacional crítica (reform 2026-05-16)**: Ken Burns es **SEÑAL DE GAP** narrativo. Si tu plan tiene Ken Burns en un shot >2s, **pausá y preguntate**:

1. ¿Este shot puede animarse con cheap model (Hailuo) + premium prompt (§ 5.7)?
2. Si NO → ¿este shot es realmente necesario o es relleno?
3. Si es necesario pero no se puede animar → **ESCALAR al arquitecto** antes de fallback a Ken Burns.

**Threshold duración Ken Burns** (cuando es fallback inevitable): MAX 2-3 segundos. Más que eso = re-plan o re-spec con animation. Ver CLAUDE.md hard rule #7.

#### Self-audit del ingeniero (POST-CHECKPOINT 4)

```
□ Hook 0-15% = 100% animation AI clips? [SI/NO]
□ Cada decision consequence tiene animation AI clip? [SI/NO]
□ Cada body horror beat tiene animation AI clip? [SI/NO]
□ Cliffhanger outro tiene animation AI clip? [SI/NO]
□ Establishing shots >2s con animation AI (cheap model OK + premium prompt)? [SI/NO]
□ ≥3 shots consecutivos con Ken Burns (fuera del hook) = VIOLACIÓN [SI = re-spec]
□ Total animation AI vs Ken Burns ratio: [X% / Y%]
□ Cualquier Ken Burns >3s? [SI = re-plan]
```

Target ratio aproximado: **≥80% animation AI shots** en videos de 80-100s (post-reform 2026-05-16). El 20% restante son detail shots <2s donde Ken Burns es aceptable.

---

### 5.7 Premium prompt quality rule (añadida 2026-05-16)

Cuando uses modelo más barato (Hailuo / Seedance Lite / Wan-AI cheap tier), el prompt **DEBE** ser premium quality para cerrar el gap de calidad. Hard rule #20 CLAUDE.md.

**Estructura mínima del premium prompt** (5 bloques, no negociable):

1. **Subject + body** — verbo + objeto + cómo (LITERAL, no abstracto). Ej: *"Maikol gira 90° hacia cámara, sonrisa contenida sin abrir boca"* (NO *"Maikol uncanny y siniestro"*).
2. **Camera direction** — lens (24mm wide / 50mm normal / 85mm portrait), movement (static / push-in slow / dolly left / handheld), angle (eye-level / low / Dutch).
3. **Lighting** — source (window left / overhead flicker / sconce warm), temperature (5000K cool / 3200K warm / sodium 2700K), intensity (key+fill / silhouette / chiaroscuro).
4. **Atmosphere** — mood VIA physical expressions, NO conceptos abstractos. Ej: *"breath visible in cold air, slight shiver in shoulders"* (NO *"sense of dread"*).
5. **Style reference** — cinematic / photoreal / painterly / archive footage / VHS degraded. Pick ONE.

**Anti-pattern**: prompt de 1 línea "Maikol uncanny en faro horror atmosphere" → cheap model produce slop. Mismo prompt expandido 5-clause + camera + lighting + literal physical mood → cheap model competitivo con tier HERO.

**Dependencia crítica del SPEC**: si SPEC v6 tiene gap en `scene_context.who_does_what` para algún shot → **ESCALAR al arquitecto antes de generar prompt**. Premium prompt necesita scene description completa. NO improvisar para llenar gaps — eso reintroduce los bugs que v6 schema previene.

**Validado 2026-05-16** (caso cabina-14): cuando engineer tuvo SPEC con scene_context vacío, improvisó prompts → 17 issues narrativos. Con SPEC v6 + scene_context lleno + premium prompt structure → cheap model (Hailuo) cierra gap a Kling Turbo Pro a 1/3 del costo.

---

## 6. SILENCIOS

| Métrica | Range | Avg |
|---------|-------|-----|
| Silence count | 1-2 | 1.4 |
| Silence total | 0.95-3.0s | 1.81s |
| Silence % | 1.05-3.4% | **2.25%** |

**Target operacional**: silencios totales **<5%** del video. Más que eso = dead air. Los referentes tienen silencios mínimos — el sound fabric (narr + music + SFX + ambient) cubre casi todo.

---

## 7. UI ELEMENTS — SAFE ZONES + POSITION (medido 2026-05-15 vía Gemini Vision sobre 50 frames de 10 referentes)

Fuente raw: `/referent-analysis/F1-UI-SAFE-ZONES.json` (n=100 detecciones de UI elements via Gemini-3.1-flash-lite).

> ⚠️ **REGLA OPERACIONAL MÁS IMPORTANTE DE ESTA SECCIÓN**: UN UI element por banda Y a la vez. Si countdown está activo en Y 35-56%, NO pongas captions en esa banda. Si captions en Y 60-65% activos, NO pongas otro UI en Y 58-72%. Bands son temporalmente exclusivas.

### 7.1 Position safe zones (n=10 referentes)

| UI element | Y % center (avg) | Y band (range) | X % center | Width % | Color | Font | n |
|-----------|------------------|----------------|------------|---------|-------|------|---|
| **Caption narración** | **62%** | **58-72%** | 50% | 47% | white (red para warning) | sans-serif | 42 |
| **Caption warning** (texto rojo) | 53% | 21-66% | 50% | 47% | **red** dominant | sans-serif bold | 4 |
| **Countdown 3-2-1** | **46%** | **35-56%** | **50%** (center) | 44% (size) | white | sans-serif large | 1 (sparse) |
| **Loading bar** | **48%** | **44-51%** | 50% | 17% | varía | — | 3 |
| **Character name labels** | **33%** | **12-40%** (top third) | 52% (over character) | 14% | **white** 25/25 | **monospaced 13/25** (canónico) o sans-serif | 25 |
| **Choice buttons A/B** | **stacked top** | **7-20%** (poll style ref-06) | left-aligned X 1-25% | full row | white | monospaced | 5 |
| Watermark | 79% | 75-85% | 30% (bottom-left) | varía | white | sans-serif | 20 |

### 7.2 No-overlap matrix — REGLA CRÍTICA

**Cuando un UI element está visible en estas bandas, NO pongas otro UI element en la misma banda:**

| Banda Y | Owner cuando activa | Prohibido en esa banda |
|---------|----------------------|-------------------------|
| **Y 7-20%** | Choice buttons A/B (poll style) | character labels, captions |
| **Y 12-40%** | Character name labels | choice buttons, captions, subject focus |
| **Y 35-56%** | **Countdown** (cuando activo) | captions, choice buttons, narration text |
| **Y 44-51%** | **Loading bar** (cuando activo) | captions, countdown (mutuamente exclusivo) |
| **Y 58-72%** | **Captions narración** (zona canónica) | countdown, loading bar, choice buttons, subject text |
| **Y 75-85%** | Watermark (always-on) | otros UI overlays |

Implicación: **el video se compone temporalmente en zonas**. Cuando hay decision point activo (Y 35-56% countdown), captions estática debe MOVERSE fuera de esa banda o desaparecer. Cuando captions narración en Y 60-65%, countdown no debe estar visible en Y 35-56%.

### 7.3 Captions canónicas — Y 60-65% (regla universal)

@referent-a (7/10 refs) usa Y 60-65% consistentemente. **Default para horror-choice × reel: caption-wrap bottom: 540px (~Y 62%)**.

Variantes observadas (n=10):
- @referent-a: Y 60-65% (7/10) — **canónico**
- @referent-c: Y 76% bottom-low (1/10) — variante
- ref-13 creator: Y 47% center (1/10) — variante atípica
- Otros: Y 46-56% (2/10) — bandas centrales menos comunes

**Reglas adicionales medidas**:
- 71% de captions tienen drop shadow
- 69% tienen stroke
- 100% son white text (red SOLO para warning específico)
- Width ~47% (caption box centered, X 27-73%)
- Height ~3% per line (multi-line wraps)

### 7.4 Character name labels — MONOSPACED canónico

13/25 observaciones son monospaced (52%) — **es el font canónico** para character names en horror-choice. Refuerza pattern previo en `referent_validated_patterns.md`.

- Y position: **12-40%** (top third) — encima de cada personaje en H1 dyad presentation
- Color: **white** (25/25 = 100%)
- Width avg: 14% (nombres cortos como BRUNO, AXEL, MAIKOL, CHELO)
- Stroke: 60% / Shadow: 60%

### 7.5 Choice buttons A/B — 2 estilos observados

**Estilo 1 — Poll stacked top (ref-06)**:
- A en Y ~8%, B en Y ~14-16%
- Left-aligned X ~1%
- Monospaced
- Formato: "A. OPTION 1" / "B. OPTION 2"
- Cuando este estilo activo: percentage indicator Y ~40% center + loading bar Y ~46-48%

**Estilo 2 — Inline caption prompts (otros 9/10 refs)**:
- NO usan botones A/B explícitos como graphics
- En vez: caption-style prompts inline tipo "¿BAJAS? O ESPERAS"
- En posición caption canónica Y 60-65%
- Más simple, mismo efecto narrativo

**Engineer decision**: para horror-choice estándar, usar Estilo 2 (más simple + 9/10 lo usa). Estilo 1 (poll) solo para variant específica.

### 7.6 Anti-patterns detectados en maikol-crucero (causa de los issues 5, 10, 17)

| Issue maikol | Violación |
|--------------|-----------|
| 0:25 countdown tapa texto en imagen | Countdown en Y 35-56% sobre subject text → viola no-overlap |
| 0:49-0:52 countdown tapa choice + captions sobre A/B | Múltiples UI elements en bandas overlapping simultáneamente |
| 1:28-1:30 CTA "sobreviviste" sobre captions | CTA en banda Y 58-72% (caption canónica) → conflict |

**Fix path para los 3 issues**: aplicar 7.2 no-overlap matrix. Mover countdown más alto (Y 35-40% top de su band) si captions activas debajo. CTA outro debe usar banda diferente (probablemente Y 50-58% si captions ausentes en ese momento).

### 7.7 ⚠️ DISCREPANCIA DESCUBIERTA con CLAUDE.md hard rule #4

CLAUDE.md hard rule #4 dice:
> `caption-wrap { bottom: 540px; height: 280px }`. Loading bars: `bottom: 700px`. Name labels: `top: 220px`.

Conversión a Y % (frame 1920px tall):
- Caption: top 1100px = Y 57.3% / bottom 1380px = Y 71.9% → centra ~Y 64% — **alineado con canónico Y 62%** ✓
- Loading bars: 700px desde abajo = Y 63.5% — **CONFLICTO con canónico Y 48%** ❌
- Name labels: 220px desde arriba = Y 11.5% — un poquito sobre canónico floor 12-40% ⚠️ aceptable

**Loading bars en hard rule está MAL** vs canónicos. Canónicos lo ponen en Y 48% (banda 44-51%), no en Y 63.5%.

**Decisión operacional**: cuando regenerés maikol-crucero o cualquier video futuro, **usá Y 48% (≈ frame top 920px / bottom 1000px) para loading bars**, NO el `bottom: 700px` de CLAUDE.md.

✅ RESUELTO 2026-05-15: CLAUDE.md hard rule #4 actualizada con loading bar `bottom: 1000px` (Y 48% canónico). Ver `CLAUDE.md` § Hard rules globales #4.

### 7.8 UI timing exact (medido 2026-05-15 vía Gemini-Vision sobre frames a 5fps en ventanas UI)

Fuente raw: `/referent-analysis/F1-UI-TIMING.json` (n=10 referentes, ~50 UI events medidos).

#### Hook countdown 3-2-1 (UNIVERSAL — 10/10)

| Métrica | Min | Max | Avg | Median |
|---------|-----|-----|-----|--------|
| **Duración total** | **2.2s** | **3.0s** | **2.42s** | **2.2s** |
| Digit "3" duración | 0.6 | 1.0 | 0.78 | 0.8 |
| Digit "2" duración | 0.6 | 1.0 | 0.84 | 0.8 |
| Digit "1" duración | 0.4 | 1.0 | 0.80 | 0.8 |

**Target operacional**: **countdown 3-2-1 = 2.2-2.5s total, cada dígito ~0.8s on-screen**.

Ubicación temporal: siempre en primeros 12s del video (durante hook).

#### Decision-time countdown (variable — algunos refs lo omiten)

10/10 tienen hook countdown. **Per-decision countdown variable**: aparece en algunos (ref-03 tiene 3 decisions con countdown), ausente en otros (ref-04, ref-05, ref-12 NO usan countdown en decisiones, solo en hook).

Si decidís usar countdown en decisiones, mismo timing que hook (~0.8s/dígito = 2.2-2.5s total).

#### Loading bar (n=17 eventos)

| Métrica | Min | Max | Avg | Median |
|---------|-----|-----|-----|--------|
| **Duración** | **0.8s** | **4.4s** | **2.25s** | **2.0s** |

**Target operacional**: **loading bar = 2.0-2.5s** (sub-stylo @referent-a). Variant @referent-c: 4.2s (más dramático, con % counter explícito).

Característica: loading bar inicia EXACTAMENTE cuando A/B buttons aparecen + termina justo antes del consequence cut. Sync ~1:1 con choice buttons.

#### Choice buttons A/B window (n=16 eventos)

| Métrica | Min | Max | Avg | Median |
|---------|-----|-----|-----|--------|
| **Duración** | **1.0s** | **4.4s** | **2.44s** | **2.2s** |

**Target operacional**: choice buttons visible **2.0-2.5s** simultáneo con loading bar (mismo tiempo, mismo ciclo).

#### CTA outro (n=7 — algunos refs no tienen CTA explícito visual)

| Métrica | Min | Max | Avg | Median |
|---------|-----|-----|-----|--------|
| **Duración** | **0.2s** | **2.2s** | **1.06s** | **0.8s** |

**Target operacional**: CTA outro **~1s** (corto, no tapa el cliffhanger final).

#### 2 estilos de UI decision (engineer decision)

| Estilo | Refs | Loading | A/B | Característica |
|--------|------|---------|-----|-----------------|
| **@referent-a** (CANÓNICO mayoritario) | ref-03, 06, 08, 09, 10, 13 | 2.0-2.5s | 2.0-2.2s | Compacto, ritmo rápido |
| @referent-c (variant) | ref-11 | 4.2s | 4.2-4.4s | Más dramático, con % counter |
| Sin UI decision (variant) | ref-04, 05, 12 | — | — | Solo hook countdown, decisions con narración + cut |

**Default para horror-choice estándar**: estilo @referent-a (compacto 2.0-2.5s). Para video más dramático: variant upsidia_ (4.2s). Para video minimalista narrativo: skip per-decision UI.

### 7.9 Issues maikol-crucero — fix path con datos exactos

| Issue maikol | Fix con n=10 data |
|--------------|---------------------|
| 1 — countdown intro muy rápido (0:06) | Target: 2.2-2.5s total, cada dígito ~0.8s. Si maikol tiene <2s → extender. |
| 10 — countdown decisión rápido (0:49-0:52) | Target: 2.0-2.5s (estilo canónico) o 4.2s (variant dramático). |
| 17 — CTA "comenta A o B" sobrepuesto a caption | Mover CTA a banda Y ≠ caption (caption Y 60-65%, CTA puede ir a Y 50-58% o Y 75-78% si watermark off). Duración CTA ~1s. |

### 7.10 Decision UI implementation — NEW (post-matadero GAP #14 codification 2026-05-19)

> **Authority**: `horror-choice-format/PAUTA-MASTER.md § 18 decision-UI-pacing` (creative intent) + canonical-scenes/INDEX.md decision setup grid 3.3 (empirical 8/8 refs).
> **Trigger**: user iter 2 matadero "Countdowns NO van ligados a narración + countdown se sobrepone con loading bar + falta efecto cámara vieja".

#### 7.10.1 Freeze frame technique

**Approach A — GSAP timeline pause** (recommended, runtime control):
```javascript
// HyperFrames composition pattern:
tl.set("#shot-06-clip video", {
  attr: { paused: "true" },
  // OR: animationPlayState: "paused"
}, "narration_end_marker_shot_06");
```

**Approach B — ffmpeg extract last frame** (alternative, static asset):
```bash
ffmpeg -sseof -0.5 -i shot_06.mp4 -update 1 -q:v 1 shot_06_lastframe.jpg
# Then display .jpg statically during countdown window via CSS
```

Default canonical: **Approach A** (GSAP pause). Engineer prefer runtime control.

#### 7.10.2 CSS filter overlay during decision

```css
.shot-decision-ui-active {
  filter: sepia(0.4) contrast(1.2) hue-rotate(15deg) brightness(0.95);
  position: relative;
}

.shot-decision-ui-active::after {
  /* Grain canvas overlay 8% opacity */
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('library/textures/grain-8pct.png');
  /* OR: SVG noise filter for procedural grain */
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Optional chromatic aberration (canonical optional) */
.shot-decision-ui-active video {
  filter: drop-shadow(2px 0 0 rgba(255,0,0,0.3)) drop-shadow(-2px 0 0 rgba(0,255,255,0.3));
}
```

Activate via JS:
```javascript
tl.set("#shot-06-clip", { className: "shot-decision-ui-active" }, "narration_end + 0.3");
```

#### 7.10.3 Countdown timing pattern

```javascript
// SPEC narrative_pacing.countdown_starts_after_narration_id resolves to timestamp:
const narrationEndMarker = narration_script.find(s => s.id === "decision_1_question").end_time_s;
const countdownStart = narrationEndMarker + 0.3;  // pause beat structural cue
const digitDuration = 0.7;

tl.to("#countdown-3", { opacity: 1, scale: 1.2 }, countdownStart);
tl.to("#countdown-3", { opacity: 0 }, countdownStart + digitDuration);
tl.to("#countdown-2", { opacity: 1, scale: 1.2 }, countdownStart + digitDuration);
tl.to("#countdown-2", { opacity: 0 }, countdownStart + (digitDuration * 2));
tl.to("#countdown-1", { opacity: 1, scale: 1.2 }, countdownStart + (digitDuration * 2));
tl.to("#countdown-1", { opacity: 0 }, countdownStart + (digitDuration * 3));
// Total countdown: 2.1s (3 digits × 0.7s)
```

#### 7.10.4 Loading bar position — REVISED canonical Y52 (not Y48)

**REVISION post 2026-05-19**: empirical Y48 from ref-03 (per § 7.1) was canonical baseline but **causes visual overlap with countdown Y46% in dense UI moments** (decision shots tienen countdown + choice buttons + loading + caption simultáneos).

**Revised canonical para decision UI shots specifically**: `bottom: 940px` (~Y 52%) en frame 1920. ≥6% Y separation from countdown Y46.

```css
.loading-bar-decision {
  position: absolute;
  bottom: 940px;  /* Y52 — revised post matadero CP5 */
  height: 6px;
  left: 5%;
  right: 5%;
  /* Y48 (bottom: 1000px) still canonical for NON-decision shots */
}
```

⚠️ **Backward-compat**: hard rule #4 CLAUDE.md says "Loading bars: bottom: 1000px". Esta § 7.10.4 es **clarification for decision UI shots specifically**, NOT global override. Decision UI shots requieren Y52 (≥6% spacing); other shots Y48 baseline OK.

#### 7.10.5 Audio cue per countdown digit

```javascript
// Per digit: SFX time_loop_glitch + ambient duck
tl.to("#audio-ambient", { volume: 0.4 }, countdownStart);  // duck -6dB
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart);
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart + digitDuration);
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart + (digitDuration * 2));
tl.to("#audio-ambient", { volume: 1.0 }, countdownStart + (digitDuration * 3));  // restore
```

**SFX options canonical**:
- `time_loop_glitch` (canonical, generated CP5 if not in library/sfx)
- `decision-tick` (alternative, more clinical/clock-tick feel)
- Avoid: full impact SFX (too aggressive for decision tension)

#### 7.10.6 Full integrated GSAP timeline snippet

```javascript
// shot_06 decision UI canonical pattern (HyperFrames composition):
const narrationEnd = parseFloat(document.querySelector("#decision_1_question").dataset.endTime);
const pauseBeat = 0.3;
const decisionStart = narrationEnd + pauseBeat;
const digitDur = 0.7;

// 1. Freeze frame
tl.set("#shot-06-video", { attr: { paused: true } }, decisionStart);

// 2. Filter overlay activate
tl.set("#shot-06", { className: "shot-decision-ui-active" }, decisionStart);

// 3. Loading bar fill L→R Y52
tl.fromTo("#loading-bar-decision",
  { width: "0%" },
  { width: "100%", duration: digitDur * 3, ease: "none" },
  decisionStart
);

// 4. Countdown digits 3-2-1 con SFX + ambient duck
tl.to("#audio-ambient", { volume: 0.4 }, decisionStart);
[3, 2, 1].forEach((digit, i) => {
  const t = decisionStart + (digitDur * i);
  tl.to(`#countdown-${digit}`, { opacity: 1, scale: 1.2, duration: 0.1 }, t);
  tl.to(`#countdown-${digit}`, { opacity: 0, duration: 0.1 }, t + digitDur - 0.1);
  tl.call(() => playSfx("time_loop_glitch"), null, t);
});
tl.to("#audio-ambient", { volume: 1.0 }, decisionStart + (digitDur * 3));

// 5. Resume motion (or transition to consequence shot)
tl.set("#shot-06-video", { attr: { paused: false } }, decisionStart + (digitDur * 3));
```

#### 7.10.7 Compliance verification

Pre-render-gate Q22 obligatorio (per `pre-render-gate/SKILL.md`). Required 4/4 checks:
- [ ] Freeze frame applied (GSAP `paused: true` at narration_end)
- [ ] Filter overlay class applied (sepia + contrast + hue-rotate + grain canvas)
- [ ] Countdown `data-start` = narration_end + 0.3s (NOT loose timing)
- [ ] Loading bar Y52 (`bottom: 940px`) ≥6% Y separation from countdown Y46

Si Q22 fails → editorial canonical signature missing → BLOQUEA render hard-rule horror-choice format.

---

## 8. CAPTIONS SPECS (PENDIENTE — TODO Gemini Vision pass)

Métricas que requieren OCR + visual analysis:
- Font family exacta
- Font weight + size
- Color por clase (name / narration / warning)
- Drop shadow specs (offset, blur, opacity)
- Sync precision (frame-by-frame)

Lo que sí sabemos por `REFERENT-PATTERNS.md`:
- Y position bottom-center ~65%
- 3-class system (name / narration / warning)
- Monospaced para character names
- Whisper-sync (NO hand-timed)
- Red glow para warning text

---

## 8.5 LIP SYNC RULE — REGLA OPERACIONAL (añadida 2026-05-15)

Caso disparador: maikol-crucero (issue 3, 4) — clip animado de Maikol con movimiento de boca visible mientras audio era solo narrador → user confused "Maikol aparece hablando pero solo habla el narrador".

### Regla técnica

| Estado del SPEC | Acción del ingeniero |
|------------------|----------------------|
| `lip_sync_required: true` (shot incluye diálogo del personaje) | Aplicar lip sync con tool (Hedra Character-3 / Sync.so / Veo / Kling Omni) ANTES de wire al timeline |
| `lip_sync_required: false` (solo narración voiceover, no diálogo) | **NUNCA usar clip animado con movimiento de boca visible**. Opciones aceptables: |
|  | 1. Usar shot NO Kling (estático con motion CSS — Ken Burns) |
|  | 2. Usar Kling clip generado con prompt explícito "mouth closed, neutral expression, NO mouth movement" |
|  | 3. Cover lower face con UI overlay (caption, lower-third) |
|  | 4. Usar frame del Kling clip ANTES de cualquier mouth movement (extract still + Ken Burns) |

### Auto-detección del bug

Si vas a usar un Kling clip donde el personaje habla naturalmente:
- Inspeccionar el clip antes de wire — ¿hay mouth movement visible >0.5s?
- Si SÍ + audio del shot es narrator (no character) → es violación de esta regla → re-generar o substituir

### Anti-pattern documentado

❌ Generar Kling clip con prompt "X says: 'frase'" → produce mouth movement
❌ Wire ese clip mientras audio es narrator (no character voice)
❌ Resultado: user percibe disonancia "está hablando pero no se le entiende"

### Self-audit (POST-CHECKPOINT 4)

```
□ Para cada Kling clip animado en el timeline:
  - ¿El audio en ese timestamp es character dialogue o narrator?
  - Si narrator + clip tiene mouth movement → violación, fix antes de render
```

---

## 8.6 BACKGROUND ANIMATED ELEMENT IMPLEMENTATION (NEW 2026-05-20 — GAP #23)

> **Authority**: `PAUTA-MASTER.md § 20 setting alive canonical pattern` + 8/8 refs empirical 100% have ≥1 background creature/object animated.

### 8.6.1 Hailuo motion intent prompt construction

Per shot SPEC `setting_ambient_creature_or_object` field — engineer DEBE explicitly request background animation en Hailuo prompt.

**Prompt pattern**:
```
Subject: <main shot subject per scene_context>.
Plus background animated element: <creature/object animated specific per setting>.
Motion: <main motion>. Background motion: <creature/object specific motion verb>.
```

**Examples**:

| Setting | Background creature/object prompt fragment |
|---------|---------------------------------------------|
| Mina | "rata gris corriendo entre piedras al fondo (visible ~5% frame width, motion subtle but clearly animated)" |
| Acuario | "tiburón nadando lento en tanque background visible through glass" |
| Industrial fundición | "llamas titilando furnace background + chispas saltando ocasional" |
| Metro túnel | "rata gris corriendo por las vías" + "polvo arrastrado por viento túnel" |
| Carretera nocturna | "mariposa nocturna volando cerca farol" + "polvo viento headlight beam" |
| Matadero refrigerado | "rata gris escapando entre carcasas al fondo (ambient creature Slot H)" |
| Comedor cozy | "insecto cerca lámpara warm light" + "humo vapor steam de olla central" |

### 8.6.2 Validation post-Hailuo

```bash
# Frame extraction + visual scan for background motion
ffmpeg -ss <shot_start> -t <shot_duration> -vf fps=2 -i shot.mp4 frames/%04d.png
# Visual check: each frame should have ≥1 background creature/object position changing
```

### 8.6.3 audit-frames-granular S10 sentinel detection

Post Phase 1 forward — `audit-frames-granular.py S10 background_motion_detected` per shot:
- Compute optical flow per shot
- Background region (top 25% + edges 10% lateral) MUST have motion vectors > threshold
- If static background detected → flag for re-render con prompt enforcement

---

## 8.7 POV TRAVERSAL IMPLEMENTATION (NEW 2026-05-20 — GAP #25)

> **Authority**: `PAUTA-MASTER.md § 22 POV traversal canonical pattern` + 8/8 refs empirical viewer moves through space.

### 8.7.1 Hailuo motion intent enum per SPEC pov_traversal_intent

```python
HAILUO_PROMPT_PER_POV_TRAVERSAL = {
    "static": "camera locked, viewer not moving",
    "walking_forward": "POV camera moves forward slowly, viewer walking. Subtle handheld bob. Floor visible bottom of frame moves forward.",
    "walking_backward": "POV camera retreats backward slowly. Subject grows distant.",
    "turning_left": "POV camera rotates smoothly to the left, perspective shifts revealing left side of setting.",
    "turning_right": "POV camera rotates smoothly to the right.",
    "approaching_character": "POV camera dolly forward toward character. Character grows larger in frame.",
    "ascending_stairs": "POV camera moves up, slight upward tilt, vertical motion subtle. Steps visible bottom of frame.",
    "descending_stairs": "POV camera moves down, slight downward tilt, vertical motion subtle. Steps visible bottom of frame descending.",
    "looking_around": "POV camera pans head left-right slowly, panoramic scan of setting."
}
```

### 8.7.2 ffmpeg post-process subtle camera move (fallback)

Si Hailuo no entrega traversal motion adequately:
```bash
# Add subtle dolly forward via crop + zoom interpolation
ffmpeg -i shot.mp4 -vf "zoompan=z='min(zoom+0.0015,1.05)':d=30*<duration>:s=1080x1920" shot_dollied.mp4
```

### 8.7.3 audit-frames-granular S10 sentinel detection

Post Phase 1 forward — `audit-frames-granular.py S10 viewer_traversal_detected` per shot pair:
- Compute camera ego-motion between consecutive shots
- If `pov_traversal_intent != static` declared in SPEC → optical flow MUST confirm motion direction matches enum
- If static framing throughout shot pair where SPEC says walking → flag re-render

---

## 8.8 ATMOSPHERIC MOTIONS CHECKLIST ≥3 PER SHOT (NEW 2026-05-20 — GAP #26)

> **Authority**: `PAUTA-MASTER.md § 20.1 + § 20.3 setting alive` + 8/8 refs empirical ≥3 atmospheric secondary motions per shot.

### 8.8.1 Catalog per setting

| Setting | Atmospheric motions available (pick ≥3 per shot) |
|---------|---------------------------------------------------|
| Mina | dust particles falling, lantern flicker, breath vapor, water drip from ceiling, cobwebs sway |
| Acuario | water shimmer reflection, bubbles rising, tank ripples, fluorescent flicker, fish movement in distance |
| Industrial fundición | flame flickering furnace, smoke rising, heat distortion air, sparks particles, ambient steam |
| Metro | tunnel wind dust, distant train light approach, dust particles, flickering fluorescents, steam from grilles |
| Carretera | wind dust drifting, headlight flicker, cigarette smoke trail, fog rolling, leaves rustling |
| Matadero (matadero-banquete) | breath vapor prominent, drip from carcasas, fluorescent flicker, sparks from electrical, smoke from refrigeration unit |
| Comedor cozy | pendant flicker, steam from food rising, dust in light beams, curtain sway, candle flicker |

### 8.8.2 Engineer Hailuo prompt requirement

Per shot SPEC `atmospheric_motions_count: 3` (minimum) — engineer Hailuo prompt MUST explicitly request atmospheric motions:

```
Plus atmospheric details animated: <motion 1>, <motion 2>, <motion 3>.
E.g., "breath vapor visible viewer mouth + drip slow from hanging carcasa + fluorescent yellow tube flicker subtle".
```

### 8.8.3 Validation post-Hailuo

```bash
# Optical flow analysis per shot
.venv/bin/python scripts/atmospheric-motion-count.py --shot shot.mp4 --min-count 3
# Output: detected motion regions count + types
# If < 3 → flag re-render with prompt enforcement
```

---

## 8.9 CHARACTER GESTURE PER SHOT (NEW 2026-05-20 — GAP #27)

> **Authority**: `PAUTA-MASTER.md § 21 character alive` + 8/8 refs canonical character active gesture per on-screen shot.

### 8.9.1 Gesture catalog canonical

Per character on-screen shot, MUST include ONE active gesture:

| Gesture category | Examples |
|-------------------|----------|
| Hand/arm | reaches forward, gestures while speaking, grips object tighter, points, taps surface |
| Head | turns toward viewer, tilts, looks away, nods, scans surroundings |
| Body | leans forward, weight shift, posture adjustment, breathes deeply visible |
| Facial (if face visible) | blink, mouth opens/closes, brow furrow, smile subtle change |
| Environmental interaction | touches object, leans against wall, picks up tool, examines item |

### 8.9.2 Compensation alive signals for signature-limited characters

Cuando character anchor design limits expression (matarife cleaver-head, futuro uncanny characters):

```yaml
# SPEC per shot character_active_gesture_per_shot field:
character_active_gesture_per_shot: "matarife: cleaver-head subtle vertical vibration during speech + apron sway from body weight shift + glove grip tension changes per emotional beat"

# Alive signals layered:
alive_signals:
  - "Signature subtle motion (cleaver-head vibration)"
  - "Garment motion (apron sway)"
  - "Glove tension changes"
  - "Breath vapor (cold setting)"
  - "Environmental interaction (gripping knife, touching carcasa)"
```

### 8.9.3 Hailuo prompt construction

```
Character: <character anchor reference>.
Action: <main action per scene_context.who_does_what>.
Plus active gesture this shot: <specific gesture from catalog>.
Plus alive signals: <compensation signals if signature-limited>.
```

### 8.9.4 audit-frames-granular S10 sentinel detection

Post Phase 1 forward — verify per character on-screen shot: motion vectors include character body region. If character static throughout → flag re-render.

---

## 9. CÓMO MEDIR MÉTRICAS NO DOCUMENTADAS ACÁ

### Scripts disponibles

| Tarea | Tool |
|-------|------|
| Transcripción | `<repo-root>/elige-companero/.venv/bin/whisper <audio.wav> --model small --language es --output_format json` |
| Pace WPM | `python -c "import json; d=json.load(open('transcription.json')); s=d['segments']; w=sum(len(x['text'].split()) for x in s); t=sum(x['end']-x['start'] for x in s); print(f'{w/t*60:.0f} WPM speaking')"` |
| LUFS | `ffmpeg -i input.mp4 -af ebur128 -f null - 2>&1 \| grep 'I:'` |
| LUFS por sección | recortar con `ffmpeg -ss X -t Y` + ebur128 |
| Music BPM | `python -c "import librosa; y,sr=librosa.load('audio.wav'); print(librosa.beat.beat_track(y=y, sr=sr)[0])"` |
| Cuts/min | `ffprobe -show_frames -of csv input.mp4 \| grep 'key=true'` |
| Vignette ratio | `python` con PIL: comparar mean brightness center 60% vs edges 20% |
| Grain variance | `python` con PIL: variance de blocks 16x16 en center region |

### Re-correr análisis completo

```bash
cd ~/AI\ video\ 1/referent-analysis/.venv-measurements
source bin/activate
python measure_F1.py  # re-genera F1-INGENIERO-MEASUREMENTS.json
```

### Auditar nuestro video vs canónicos (post Bloque C 2026-05-15)

`audit-against-referent.py` compara nuestro draft.mp4 contra F1 n=10 (p25-p75 bands per métrica). Gate Q21 del pre-render-gate. Hard rule #1 dual gate.

```bash
# Desde el proyecto root con .venv configurado:
.venv/bin/python scripts/audit-against-referent.py --video renders/draft.mp4 --html index.html

# Args opcionales:
#   --measurements <path>  (default: ../referent-analysis/F1-INGENIERO-MEASUREMENTS.json)
#   --tolerance p25-p75|p5-p95  (default p25-p75)

# Exit codes:
#   0  ≥85% métricas críticas en band → PASS
#   1  <85% → FAIL (bloquea render)
#   2  data missing → BLOCKED
```

Critical metrics medidas: `pace.wpm_total`, `audio.lufs_integrated`, `pacing.cuts_per_min`, `pace.coverage_pct`.
Informational: `pace.avg_block_s`, `audio.music_bpm` (si librosa disponible).

Smoke test validado 2026-05-15 sobre bosque-abandonado v8-FINAL: 1/4 metrics en band (25%). Exit 1 FAIL correcto — confirma vendor gap (nuestras producciones técnicamente fuera de canónico aun cuando Gemini score las aprobaba).

### Antes de inventar un valor

1. ¿Está documentado acá? → usalo
2. ¿Puedo medirlo de los referentes? → medilo
3. ¿Es métrica universal (no format-specific)? → consultá `referent-analysis/REFERENT-PATTERNS.md` § REGLAS UNIVERSALES
4. ¿Ninguna de las 3? → reportá al user: "métrica X no documentada + no medible — propongo Y basado en heurística general"

**NUNCA**: hacer fallback a comparar contra `mina-abandonada/`, `bosque-abandonado/`, `elige-companero/`, o cualquier `ours-*.md`.

---

## 10. ANTI-PATTERNS — nuestras producciones como caso de estudio

Estos NO son targets — son cosas que nuestras producciones hicieron MAL y por las que NO debemos repetir.

| Anti-pattern | Nuestras producciones | Referentes F1 | Diferencia |
|--------------|----------------------|---------------|------------|
| Pace muy lento | ~120 WPM speaking | 156-195 WPM | -25-40% |
| Voice + atempo equivocado | atempo 2.0x | atempo equivalente ~2.5x | -20-30% |
| Coverage muy baja | 30-50% (pueblo v2) | 80-96% | -40% peor |
| Outro alto en RMS | -19 dB (mantiene energía) | -32 dB (drop deliberado) | falta el "punchline drop" |
| Cuts en hook | a veces 1-2 | 0 universalmente | rompe pattern |

Caso disparador: maikol-crucero 2026-05-15. Ingeniero comparó contra nuestras producciones (autoridad falsa) → recomendó pace = nuestras producciones = lento vs canónico. Fix: usar SIEMPRE esta pauta.

---

## 11. CONFIANZA + GAPS

### Confianza actual (n=10)

| Hallazgo | n | Confianza | Notas |
|----------|---|-----------|-------|
| Pace speaking p25-p75 = 153-180 WPM | 10/10 | **Alta** | Range típico claro |
| Pace median 165 WPM | 10/10 | **Alta** | Target ideal |
| LUFS -14 ±0.5 | 9/10 | **Muy alta** | 1 outlier en -15.2 |
| Coverage ≥85% | 8/10 | **Alta** | p25 = 84.7% |
| Block duration 2.8-3.5s avg | 7/10 | **Alta** | Outliers en extremos |
| Hook típicamente sin cuts | **8/10** | **Alta** | Pattern fuerte pero no absoluto |
| Outro RMS drop -9 dB | 10/10 | **Muy alta** | Pattern consistente |
| Music BPM bimodal (~100 / ~135) | 10/10 | **Alta** | Distribución clara |
| Vignette ratio 1.42 ±0.16 | 10/10 | **Alta** | Range estrecho |
| Hue bimodal warm/cool 5+5 | 10/10 | **Alta** | Depende del setting |

### Pending — gaps a cerrar

| Métrica | Estado | Próximo paso |
|---------|--------|---------------|
| Whisper ref-09 a ref-13 | running 2026-05-15 background | Auto-update a n=10 al completar |
| Caption visual specs | TODO | Gemini Vision pass sobre frames con captions |
| UI element timing exact | TODO | Frame extraction 100ms intervals en momento countdown/loading |
| Music vs narration separation | TODO | Demucs/Spleeter para stems |
| Frame-by-frame motion intensity | TODO | Optical flow OpenCV |

### Caja negra que NO podemos medir desde acá

- Voice IDs ElevenLabs usados por los referentes (privado de cada creator)
- Tools de animation (Kling vs Runway vs algo más)
- Pipeline específico de mastering

---

## 12. Última actualización

- **2026-05-15 v3** — **Fase 1 post-maikol-crucero feedback completa**:
  - § 5.6 Motion intensity per shot añadida (table por shot context: hook 100% Kling, decision consequence Kling, body horror Kling, outro Kling)
  - § 7 UI elements completamente repoblada con n=10 mediciones reales (antes era TODO):
    - § 7.1 Safe zones (caption Y 62%, countdown Y 46%, loading Y 48%, character labels Y 12-40%, choice buttons stacked top o inline)
    - § 7.2 No-overlap matrix (bandas Y temporalmente exclusivas)
    - § 7.7 Discrepancia detectada con CLAUDE.md hard rule #4 (loading bars Y 63.5% vs canónico Y 48%)
    - § 7.8 UI timing exact (hook countdown 2.2-2.5s, loading 2.0-2.5s, CTA outro ~1s)
    - § 7.9 Fix path para 3 issues maikol con datos n=10
  - § 8.5 Lip sync rule añadida (anti-pattern + 4 alternativas + auto-detección)
- **2026-05-15 v2** — n=10 referentes F1 completos (post-Whisper). Pace WPM 115-195. Cuts/min de-clustered. Hue bimodal warm/cool. Caso maikol-crucero pace re-evaluado.
- **2026-05-15 v1** — n=5. Disparado por caso maikol-crucero (engineer recomendó pace 3.0 w/s comparando contra nuestras producciones, no contra referentes).

## 13. Cambios significativos n=5 → n=10

| Métrica | n=5 dijo | n=10 dice | Implicancia |
|---------|----------|-----------|--------------|
| Pace WPM total | 156-195 (avg 176) | 115-195 (avg 162) | Range más amplio. Floor más bajo. Median 165. |
| Block duration target | ≥4.5s | 2.8-3.5s | n=5 sobre-estimó duraciones largas. Corrected. |
| Hook cuts | "0 universal 5/5" | "8/10 = 0" | Pattern fuerte, NO absoluto |
| Hue distribution | 3 red dominant | 4 red + 4 cyan bimodal | Setting-dependent, no solo warm |
| LUFS std | 0.11 (extreme tight) | 0.41 (still tight) | 1 outlier expandió std |
| Cuts/min raw vs de-clustered | n=5 usaba raw | n=10 de-clustered avg 4.19 | Raw inflado 2-4x — corrected |

**Lección operacional**: n=5 produce direcciones correctas pero rangos optimistas. n=10 da rangos más realistas. **Para futuros INGENIERO-PAUTAs minimum n=5, target n=10**.

### 7.10.8 ⚠️ Canonical validation status (Hard Rule #19 EXPANSION compliance) — UPDATED 2026-05-20 post engineer Phase 1

```yaml
canonical_validation_status: "validated_via_video_measurement"  # FLIPPED 2026-05-20
validated_against_canonical_refs:
  - "engineer Track B Phase 1 empirical measurement 8/8 refs 2026-05-20"
  - "Source: referent-analysis/empirical-decision-ui-pacing/aggregate-canonical-bands.json"
  - "Phase 0 qualitative: canonical-scenes/INDEX.md decision setup grid 3.3"
validation_methodology: "Phase 1 empirical: ffmpeg + Whisper + librosa + frame analysis 22 decision windows across 8 refs"
measurement_script: "measure-canonical-decision-ui-pacing.py (built + run engineer Track B Phase 1 COMPLETE)"
validated_at: 2026-05-20
```

#### ⚠️ EMPIRICAL CORRECTIONS post Phase 1 (Track A v2 — 3 REFUTATIONS)

**Updated technical specs per Phase 1 empirical:**

| Spec | Pre-empirical (Phase 0 inferred) | Phase 1 empirical (8/8 refs) | Correction status |
|------|------------------------------------|-------------------------------|-------------------|
| `countdown_pause_beat_s` | 0.3 | **0.9 s median** (p25=0.33, p75=2.1) | ⚠️ REFUTED — value ≥3× higher |
| `ambient_duck_db_during_countdown` | -6 dB | **+0.22 dB median (≈ NO duck)** | ⚠️ REFUTED — no duck canonical |
| `freeze_frame_applied_default` | true (default) | **14% refs (3/22 windows)** — MINORITY | ⚠️ REFUTED — OPTIONAL not default |
| `filter_overlay_applied_default` | true (default) | minority pattern Phase 1 | ⚠️ REFUTED — OPTIONAL stylistic |
| `countdown_digit_duration_s` | 0.7 (architect v2 compromise) | engineer empirical 0.5 (n=1) + **user Rule D 1.0** | ⚠️ Track A v3 R1: **1.0s WINS** user perceptual — engineer n=1 + architect v2 0.7 BOTH refuted |
| `loading_bar_y_pct` | 52 | 52 (CONFIRMED matched) | ✅ confirmed |
| `countdown_y_pct` | 46 | 46 (CONFIRMED matched) | ✅ confirmed |
| `countdown_visual_style` | film_leader_academy | film_leader_academy (CONFIRMED) | ✅ confirmed direct frame |

#### Updated engineer implementation per corrections

**§ 7.10.3 countdown timing pattern** — UPDATED Track A v3 R1:
```javascript
const narrationEndMarker = narration_script.find(s => s.id === "decision_1_question").end_time_s;
const pauseBeat = 0.9;  // validated_via_video_measurement n=14 samples (was 0.3 inferred, Phase 0)
const countdownStart = narrationEndMarker + pauseBeat;
const digitDuration = 1.0;  // ⚠️ Track A v3 R1 — user Rule D PRECEDENCE 2026-05-20 "segundos = segundos literal 1,2,3". Refutes engineer empirical 0.5 (n=1) + architect v2 compromise 0.7. Forward revisit if n≥5 empirical disagrees.
```

**§ 7.10.5 audio cue per countdown digit** — UPDATED ambient duck:
```javascript
// ⚠️ NO ambient duck per Phase 1 empirical (was -6dB inferred)
// Optional: tick SFX per digit, but NO ambient volume reduction
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart);
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart + digitDuration);
tl.call(() => playSfx("time_loop_glitch"), null, countdownStart + (digitDuration * 2));
// REMOVED: tl.to("#audio-ambient", { volume: 0.4 }, countdownStart);
// REMOVED: tl.to("#audio-ambient", { volume: 1.0 }, countdownStart + (digitDuration * 3));
```

**§ 7.10.1 freeze frame** — UPDATED to OPTIONAL:
```javascript
// ⚠️ Phase 1: 14% refs use freeze frame — OPTIONAL stylistic, NOT canonical default
// Apply only if SPEC explicitly declares decision_freeze_frame: true
// Default behavior: minimal-motion clip (subtle Kling POV) continues during countdown
```


### 7.11 AVU library — pre-rendered atomic units implementation (NEW 2026-05-19 — Track E Phase 2)

> **Authority**: `PAUTA-MASTER.md § 19 AVU principle creative intent` + matadero iter 3-4 empirical sync failures.
> **Trigger**: user architectural insight 2026-05-19 PM "efectos ligados a sonido/narración deben ser capa o extra que NUNCA falla" + 4/4 canonical refs direct frame verification (countdown FILM LEADER ACADEMY + bundled ticks).

#### 7.11.1 Directory structure (NIVEL 2 universal)

```
ai-video-production/templates/avu-library/
├── countdown-3-2-1-film-leader-with-ticks.mp4   # 3s, 1080×1920, audio bundled (Phase 1 priority)
├── decision-freeze-filter-loop.mp4               # 0.5s loopable, alpha channel
├── hook-transition-flash-whoosh.mp4              # 0.5s transition asset
├── outro-card-template.mp4                       # 4.6s reusable
├── README.md                                     # usage docs + specs
└── manifest.json                                 # per-AVU metadata
```

#### 7.11.2 AVU technical specs (uniform across library)

| Spec | Value | Rationale |
|------|-------|-----------|
| Resolution canonical | 1080×1920 (9:16 reel) | Reel format default |
| Resolution landscape variant | 1920×1080 | YouTube short / longform compat |
| Frame rate | 30 fps | Web standard, matches Reel |
| Codec video | H264 high profile | Universal compat |
| Audio codec | AAC stereo 256 kbps | Web standard high quality |
| Audio variant mono | AAC mono 192 kbps | If voice-only no stereo justified |
| Alpha channel (when feasible) | ProRes 4444 source → H264 transparent | For overlays |
| Countdown visual style | FILM LEADER ACADEMY (crosshair + big central digit ~40-50% frame width) | Per PAUTA § 19.6 GAP #19 correction |

#### 7.11.3 Integration HyperFrames pattern

```html
<video id="avu-countdown-hook"
       data-start="5.0"
       data-duration="3.0"
       data-track-index="100"
       src="../../.claude/skills/ai-video-production/templates/avu-library/countdown-3-2-1-film-leader-with-ticks.mp4"
       style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 60;">
</video>
```

**No GSAP timeline coupling needed** — `data-start` + `data-duration` HyperFrames-native = bullet-proof sync (single .mp4 element).

#### 7.11.4 Sync contract para elementos NOT AVU-able (per-video variable)

Para character dialogue + narrator framing question + setting captions (text varies per-video), declarar en SPEC explícito:

```yaml
audio_visual_atomic_units:  # per shot in shot_list[]
  - id: hook_countdown
    type: pre_rendered_avu
    asset_path: "ai-video-production/templates/avu-library/countdown-3-2-1-film-leader-with-ticks.mp4"
    inject_at_timestamp: 5.0
    bundled_audio: true

  - id: narrator_framing_question
    type: sync_contract  # text varies per-video
    visual_element_id: caption_central
    audio_element_id: tts_narrator_framing
    contract:
      visual_start_s: 2.0
      audio_start_s: 2.0
      tolerance_s: 0.1
    pre_render_validation: "verify visual.data-start matches audio segment start ± tolerance"
```

#### 7.11.5 Hook sub-beat ordering technical (GAP #18 codification)

Per `PAUTA-MASTER § 19.5` canonical hook order:

```javascript
// HyperFrames composition shot_01 pattern:
const hook_timeline = [
  {
    beat_id: "character_intro_name_labels",
    timestamp_s: [0, 2],
    ui_elements: ["#name_label_A", "#name_label_B", "#ambient_setting"],
    avu: null
  },
  {
    beat_id: "caption_central_setting_narrator_framing",
    timestamp_s: [2, 5],
    ui_elements: ["#caption_central_setting_name", "#caption_narrator_framing_question"],
    narration_segment_id: "narrator_framing_question",
    avu: null
  },
  {
    beat_id: "push_in_parallax_micromotion",
    timestamp_s: [Ys, Zs],
    motion_effect: "push_in + parallax_3d",
    avu: null
  },
  {
    beat_id: "countdown_avu_film_leader_LAST",  // ⚠️ LAST 2-3s del hook
    timestamp_s: [5, 7],
    avu_asset: "ai-video-production/templates/avu-library/countdown-3-2-1-film-leader-with-ticks.mp4",
    avu: true
  }
  // NOTE: character dialogue NOT in hook — separate shot_02 post-hook
];
```

**Anti-pattern matadero iter 1**: hook shot_01 with dialogue cocinera ON-screen mid-hook + countdown overlap. Result: editorial collapse, viewer cognitive overload.

**Canonical**: hook ends with countdown FILM LEADER ACADEMY. Character dialogue starts en shot_02 separate.

#### 7.11.6 Generation workflow (Phase 1 priority forward)

```bash
# Step 1: Generate FILM LEADER ACADEMY countdown 3-2-1 + ticks
# Tools: After Effects (Adobe) OR ffmpeg + animated SVG + audio mixed
# Specs per § 7.11.2

# Step 2: Validate AVU
ffprobe ai-video-production/templates/avu-library/countdown-3-2-1-film-leader-with-ticks.mp4
# Verify: 1080×1920, 30fps, 3.000s duration, audio stream present

# Step 3: Add to manifest.json
{
  "avu_library_version": "1.0",
  "templates": {
    "countdown-3-2-1-film-leader-with-ticks": {
      "asset_path": "countdown-3-2-1-film-leader-with-ticks.mp4",
      "duration_s": 3.0,
      "resolution": "1080x1920",
      "fps": 30,
      "audio_bundled": true,
      "canonical_validation_status": "validated_via_direct_frame_verification_4_refs_2026_05_19",
      "use_for": ["hook countdown", "decision UI countdown", "outro countdown"]
    }
  }
}
```

#### 7.11.7 Compliance verification (pre-render-gate)

Q24 + Q25 NEW per `pre-render-gate/SKILL.md`:
- **Q24**: Audio-visual coupled elements implemented as AVU (pre-rendered .mp4 audio bundled) OR declared explicit sync_contract validated. **Y → PASS, N → 🔴 FAIL ship-blocking** (compose-time fragility risk).
- **Q25**: Countdown visual style = FILM LEADER ACADEMY (crosshair + big central digit)? **Y → PASS, N → 🟡 NB style drift from canonical**.

#### 7.11.8 Canonical validation status

```yaml
canonical_validation_status: "validated_via_direct_frame_verification_4_refs_2026_05_19"
validated_against_canonical_refs:
  - "4 canonical refs direct frame verification (countdown FILM LEADER ACADEMY style + bundled ticks)"
  - "matadero iter 3-4 empirical sync failure cases"
validation_methodology: "direct frame extraction + visual style identification + matadero empirical failure analysis"
validated_at: 2026-05-19
phase_1_forward:
  - "Build full AVU library remaining 3 templates (decision-freeze + hook-transition + outro-card)"
  - "Run extract-canonical-max-detail.py regenerate canonical-scenes docs MAX DETAIL"
  - "Build measure-canonical-decision-ui-pacing.py + audio cue levels script"
```

