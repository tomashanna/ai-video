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

## 8.10 PER-CLIP ATOMIC ASSEMBLY IMPLEMENTATION (NEW 2026-05-20 — Phase 2 forward, Hard Rule #23)

> **Engineering implementation** del refactor architecture descripto en `ai-video-production/PIPELINE.md § 13`. Esta sección es la guía operacional del INGENIERO. Aplica a horror-choice × reel forward (video #3+).

### 8.10.1 Architectural rationale (por qué refactor)

User architectural insight 2026-05-20 (memory `feedback_per_clip_atomic_assembly`): **"en vez de hacer todo el audio de una vez, se hace el audio por clip y luego que todos los clips estan listos con el audio y todo se juntan"**.

Eliminates **7/8 bug classes recurrentes** que el ingeniero combatía iter tras iter:

| Bug class | Caso disparador horror-choice | Causa raíz (global master) |
|-----------|-------------------------------|-----------------------------|
| Sync drift end-of-timeline | matadero iter 1 "QUE DAS CENA" | Master.mp3 acumula +0.5s drift por timeline largo |
| Caption fragmentation | cinema iter 1 "ELICHE" | Whisper sobre master fragmenta tokens en boundaries |
| Same-Y caption overlap | matadero iter 5 D1+D2 | Captions sobre timeline global no ven contexto per-clip |
| Audio/clip boundary mismatch | matadero iter 7 GSAP offsets | Master boundaries no align con clip cuts |
| SFX context-blind | recurring 8 videos | SFX sobre timeline global ignora qué pasa en cada clip |
| AVU GSAP compose-time fragility | matadero iter 3-4 countdown | AVU armado en HTML/GSAP (compose-time) vs pre-rendered atomic |
| Cumulative timeline error | universal >60s videos | Drift compounds linealmente con duración |

Single bug class NO eliminada: cross-clip music ducking (sigue siendo layer post-concat — gestionada en step 10 del pipeline).

### 8.10.2 Per-clip workflow steps (operacional para INGENIERO)

```bash
# Per shot (repeat N veces, paralelizable):

# Step 1: Animate (CP4 existente — sin cambios)
.venv/bin/python scripts/video.py -i assets/anchors/shot_NN.png -p "<motion prompt>" \
  -o assets/clips/shot_NN.mp4 --duration <Ws>

# Steps 2-5: Atomic builder (combo TTS + SFX + ambient + mix + mux + caption sidecar)
.venv/bin/python scripts/build_clip_atomic.py \
  --shot-id shot_NN \
  --spec creative-specs/<id>.yaml \
  --clip-video assets/clips/shot_NN.mp4 \
  --voice-id <VOICE_ID> \
  --output-dir assets/atomic/
# Outputs:
#   assets/atomic/shot_NN_with_audio.mp4
#   assets/atomic/shot_NN_captions.json
#   assets/atomic/shot_NN_audio_breakdown.json (TTS + SFX + ambient mix log)

# Step 6: Quality Gate Agent (per-clip verdict)
.venv/bin/python scripts/quality_gate_per_clip.py \
  --clip assets/atomic/shot_NN_with_audio.mp4 \
  --captions assets/atomic/shot_NN_captions.json \
  --spec creative-specs/<id>.yaml \
  --shot-id shot_NN \
  --output handoffs/CP5-clip-NN-gate-verdict.md
# Exit 0 = ≥9.0 PASS (proceed step 7)
# Exit 1 = 7.0-8.9 ITERATE (engineer re-builds clip, max 3 iter)
# Exit 2 = <7.0 ESCALATE (architect re-spec required)

# Step 7: Mid-execution Gemini Vision hook (catches bugs ANTES de concat)
.venv/bin/python scripts/gemini_midexec_vision.py \
  --clip assets/atomic/shot_NN_with_audio.mp4 \
  --captions assets/atomic/shot_NN_captions.json \
  --spec creative-specs/<id>.yaml \
  --shot-id shot_NN \
  --output audits/shot_NN_gemini.json

# After ALL clips PASS steps 6+7, assemble cross-clip layers:

# Step 8: Concat
bash scripts/concat-clips-with-audio.sh assets/atomic/ assembled.mp4

# Step 9: Effects library between clips
.venv/bin/python scripts/apply-effects-between-clips.py \
  --input assembled.mp4 \
  --spec creative-specs/<id>.yaml \
  --output assembled_with_transitions.mp4

# Steps 10-12: Cross-clip music + ambient + LUTs
.venv/bin/python scripts/apply-cross-clip-music.py \
  --input assembled_with_transitions.mp4 \
  --spec creative-specs/<id>.yaml \
  --output assembled_final.mp4

# Step 13: Final render + global audit
# (existing 7 pre-render gates + Gemini holístico ≥9.7 + audit-against-referent ≥85%)
```

### 8.10.3 Audio mix per-clip (NOT global)

El INGENIERO realiza el mix **dentro del clip atomic**, NO sobre timeline global. Esto:

- Elimina cumulative drift (mix matemática per ventana corta = sin compounding error)
- Permite SFX context-aware (el script ve qué pasa en ESTE shot, no infiere desde timeline global)
- Caption sidecar JSON generated per clip = Whisper local sobre ventana de pocos segundos = más preciso

#### Mix volumes per-clip (canónicos, IGUAL que global pero aplicados localmente)

| Track | Volume per clip | Notas |
|-------|-----------------|-------|
| Narración | 1.0 | LUFS target -16 LUFS per clip (cross-clip mastering -14 LUFS lo achieva post-concat) |
| Ambient local | 0.10-0.18 | Slice de cross-clip ambient para boundaries smooth |
| SFX eventos | 0.20-0.35 | Context-aware al shot |
| Flash impacts | 0.55-0.65 | Solo si SPEC declara flash en este shot |
| Música | **NO en clip atomic** | Música = cross-clip layer (step 10 post-concat) para ducking automático contínuo |

**Regla**: música NUNCA va dentro del clip atomic. Va como cross-clip layer post-concat. Razón: necesita seguir secciones (hook/dilemmas/outro) y ducking automático cross-clip.

### 8.10.4 Caption sidecar JSON per-clip schema

`build_clip_atomic.py` genera `shot_NN_captions.json`:

```json
{
  "shot_id": "shot_03",
  "clip_duration_s": 4.2,
  "tts_source_text": "Si elegiste a Hugo... cuidado con sus pasos.",
  "whisper_segments": [
    {
      "start_s": 0.12,
      "end_s": 1.85,
      "text": "Si elegiste a Hugo",
      "class": "narration",
      "y_position_canonical": 540
    },
    {
      "start_s": 1.95,
      "end_s": 4.10,
      "text": "cuidado con sus pasos",
      "class": "narration",
      "y_position_canonical": 540
    }
  ],
  "canonical_validation": {
    "y_position_in_band": true,
    "stroke_drop_shadow_applied": true,
    "monospaced_for_names": "N/A (no name in this clip)"
  }
}
```

**Ventajas**:
- Sidecar = data-driven, no compile-time GSAP hardcoding
- Quality Gate Agent lee sidecar para audit caption Y position canonical (banda 540-820px)
- Mid-execution Gemini Vision verifica match captions vs audio per shot

### 8.10.5 AVU overlay integration per clip

AVUs (Audio-Visual Units pre-rendered, ver § 7.11) integran **dentro del clip atomic** cuando aplica:

```bash
# Step 4 alternativo cuando shot incluye AVU (countdown 3-2-1, decision freeze, hook transition, outro card):

.venv/bin/python scripts/build_clip_atomic.py \
  --shot-id shot_01 \
  --clip-video assets/clips/shot_01.mp4 \
  --avu-overlay ai-video-production/templates/avu-library/countdown-3-2-1-film-leader-with-ticks.mp4 \
  --avu-start-s 5.0 \
  --avu-end-s 8.0 \
  --voice-id <VOICE_ID> \
  --output-dir assets/atomic/
```

**Key**: AVU mp4 (audio + visual bundled) overlay ON the clip atomic mp4 = single self-contained mp4 con audio + AVU + base visual. NO GSAP compose-time hack. **Elimina bug class #6** (AVU GSAP timing fragility — caso matadero iter 3-4).

### 8.10.6 Effects library between clips — usage examples

Entre clips (post-concat, step 9), el INGENIERO aplica transitions per SPEC `transitions[]` array:

```yaml
# SPEC schema v10 declares per clip-boundary transition:
transitions:
  - between: [shot_01, shot_02]
    effect: white-flash-0.1s
    reason: "pre-twist impact (hook → dilemma 1)"
  - between: [shot_02, shot_03]
    effect: hard-cut
    reason: "default pacing, cuts/min target 4.2"
  - between: [shot_06, shot_07]
    effect: glitch-0.2s
    reason: "plot twist reveal at H4"
  - between: [shot_N-1, shot_N]
    effect: dip-to-black-0.4s
    reason: "outro card entrance"
```

```bash
.venv/bin/python scripts/apply-effects-between-clips.py \
  --input assembled.mp4 \
  --spec creative-specs/<id>.yaml \
  --output assembled_with_transitions.mp4
```

**Anti-pattern eliminado**: GSAP white-flash hardcoded sobre timeline global con `tl.set(...) → tl.to(...)` (caso bug "flash reaparece al seek"). Ahora flash AVU bundled en transition mp4 entre clips = atomic, no GSAP fragility.

### 8.10.7 Mid-execution Gemini Vision hooks invocation

Invocados **per clip** después de Quality Gate PASS, ANTES de concat:

| Cuándo | Trigger | Output |
|--------|---------|--------|
| Per clip atomic PASS (step 6) | Quality Gate exit 0 | `audits/shot_NN_gemini.json` |
| Pre-concat checkpoint | All clips PASS individually | `audits/pre-concat-summary.md` |
| Post-concat pre-effects | After step 8 concat | `audits/post-concat-fullvideo.json` |
| Post-final (existing) | Step 13 final render | Existing 7 gates (sin cambios) |

**Por qué mid-execution**: caso matadero iter 7 — caption fragmentation D1+D2 detectada en final render = re-build TODOS los clips. Con mid-execution hook = detectado per clip = solo re-build shot_NN (10x más barato).

```bash
# Per clip:
.venv/bin/python scripts/gemini_midexec_vision.py \
  --clip assets/atomic/shot_NN_with_audio.mp4 \
  --captions assets/atomic/shot_NN_captions.json \
  --spec creative-specs/<id>.yaml \
  --shot-id shot_NN \
  --output audits/shot_NN_gemini.json
```

**5 dimensions auditadas per clip**:
1. UI overlap (caption Y vs canonical band 540-820px)
2. Frames negros (visibility <1s per HyperFrames gotchas)
3. AVU detect (si SPEC declara AVU en clip, verificar presencia)
4. Character consistency vs anchor (compare frame medio del clip vs `assets/anchors/<character>.png`)
5. Caption text match TTS source (verifica Whisper no fragmentó tokens)

Exit 0 = OK proceed concat. Exit 1 = issue → fix antes de concat.

### 8.10.8 Quality Gate Agent verdict thresholds

| Score | Verdict | Acción ingeniero |
|-------|---------|-------------------|
| **≥9.0** | 🟢 PASS | Proceed to step 7 Gemini Vision mid-exec |
| **8.0-8.9** | 🟡 ITERATE (minor) | Re-build clip con fixes localizados (max 3 iter per clip) |
| **7.0-7.9** | 🟠 ITERATE (mayor) | Re-build clip con re-spec menor — consultar SPEC |
| **<7.0** | 🔴 ESCALATE | STOP. Architect re-spec del shot (no fix engineering puede salvar) |
| **Tras 3 iter sub-9.0** | ⛔ ESCALATE forzado | NO opcional. Handoff `escalate-clip-NN.md` al arquitecto. |

**Cap global**: si >30% de clips llegan a ESCALATE → STOP video, request architect full re-spec. No engineering hack puede compensar SPEC defectuoso a esa escala.

### 8.10.9 Reusable shot-with-audio assets

Ventaja secundaria: clips atomic (shot_NN_with_audio.mp4) son **reusables across videos**:

- Outro card AVU + audio bundled → reusable en TODOS los videos del formato
- Hook countdown 3-2-1 (film leader academy) → reusable
- Decision freeze UI + ticks → reusable
- "Una noche en paz" cliffhanger card → reusable

Estos viven en `ai-video-production/templates/avu-library/` con manifest declaring duration, resolution, audio_bundled status, canonical_validation_status.

### 8.10.10 Compliance verification (pre-render-gate Q26 NEW)

Pre-render-gate gana Q26 NEW 2026-05-20:

**Q26**: Video assembly used per-clip atomic strategy (NOT global master.mp3 legacy)?
- Verify: `assets/atomic/shot_NN_with_audio.mp4` files exist per shot
- Verify: NO `assets/master.mp3` ni `assets/master-90s.mp3` in project
- Verify: SPEC `assembly_strategy: per_clip_atomic` declared
- **Y → PASS, N → 🔴 FAIL ship-blocking** (video #3+ MUST use per-clip atomic per Hard Rule #23)

Exception: matadero + cinema-abandonado legacy projects exempted (in-flight grandfather clause).

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

## 11.5 ACCEPTANCE CRITERIA — Script merge requirements (NEW 2026-05-23 post Hard Rule #26)

> **Codificado Sub-Fase 3A 2026-05-23 post Bug #12 user perceptual catch + Gap #52 auditor silent decision pattern threshold reached.**

Engineer NO declara un script complete (ready for merge) sin cumplir:

1. **`test_<script>.py` companion sidecar** existente en mismo directorio
2. **Tests passing run** completo sin errores
3. **V4 archive validation** (`cerro-aislado-v4/`) cuando aplicable — usar V4 case real como ground truth
4. **Honest test results**: si test FALLA, engineer reporta FAIL explícito, NO maquilla
5. **Cost discipline**: tests deben ejecutar local + FREE Gemini Vision (cost cap $0 enforced)

Auditor NO acepta merge si:
- Falta test sidecar (Hard Rule #26 violation)
- Tests existen pero NO pasan
- Engineer no documentó cómo el script fue validated against V4 archive

Pattern_class enforced: `tests_adversariales_obligatorios_forward`. Sub-Fase 3A Sprint M defense in depth requirement.

**Workflow forward**:
```
Engineer builds script_new.py
  ↓
Engineer builds test_script_new.py (V4 archive case + mock cases + edge cases)
  ↓
Engineer runs test_script_new.py → all PASS
  ↓
Engineer emits handoff with test results table
  ↓
Auditor verifies tests independent + filesystem state
  ↓
Merge OR escalate
```

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


---

## § 8.11 — PER-SECTION MUSIC LAYERS RULE (NEW 2026-05-21 — comparative analysis cinema vs canonical refs)

> **Authority**: `PAUTA-MASTER § 25` (Music layers 3 mandatory creative authority) + Gemini Vision comparative analysis 2026-05-21 (cinema 1 layer "minimal" vs canonical 3 layers).
> **Trigger**: cinema-abandonado iter 1-6 shipped with 1-layer music — Gemini said "audio does 60% of the work" (warning, not compliment). Forward: 3 layers mandatory.

### 8.11.1 The 3 mandatory layers

| Layer | Continuity | Volume (canonical horror) | Frequency band | Source |
|---|---|---|---|---|
| **1. Drone** | Continuous 80-100% | 0.05-0.13 (peak 0.13 in horror sections) | 40-200 Hz dominant | ElevenLabs SFX "subharmonic horror tonal pad" or curated library file |
| **2. Ambient** | Per-section (changes with setting beat) | 0.10-0.18 | 200-2000 Hz | ElevenLabs SFX setting-specific (e.g. "projector reel mechanism + dust hum", "mine drip echo + wind") |
| **3. Accent** | Event-driven (countdown ticks, dilemma locks, climax peaks) | 0.20-0.35 (impacts 0.55-0.65) | Wide-spectrum | ElevenLabs SFX or `effects-library/audio-stings/*.mp3` |

### 8.11.2 ffmpeg recipe for layer mixing

```bash
# Inputs:
#   $DRONE = path to layer 1 (looped to video duration)
#   $AMBIENT_HOOK, $AMBIENT_DIL1, $AMBIENT_DIL2, $AMBIENT_OUTRO = layer 2 per section
#   $NARR = narration .wav (master)
#   $ACCENTS = composite of accent SFX already timeline-placed
#   $VIDEO = render base mp4 (visual only)
#   $DURATION = total video duration in seconds

# Step 1: Loop drone to full video duration
ffmpeg -y -stream_loop -1 -i "$DRONE" -t "$DURATION" -c:a aac -b:a 192k drone_full.aac

# Step 2: Concatenate ambient per-section with crossfades
ffmpeg -y \
  -i "$AMBIENT_HOOK" -i "$AMBIENT_DIL1" -i "$AMBIENT_DIL2" -i "$AMBIENT_OUTRO" \
  -filter_complex "[0:a][1:a]acrossfade=d=0.5[a01];[a01][2:a]acrossfade=d=0.5[a012];[a012][3:a]acrossfade=d=0.5[aout]" \
  -map "[aout]" -c:a aac -b:a 192k ambient_full.aac

# Step 3: Three-layer mix with ducking under narrator
ffmpeg -y \
  -i drone_full.aac \
  -i ambient_full.aac \
  -i "$ACCENTS" \
  -i "$NARR" \
  -filter_complex "
    [0:a]volume=0.13[drone];
    [1:a]volume=0.15[ambient];
    [2:a]volume=0.30[accent];
    [3:a]volume=1.0[narr];
    [drone][narr]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=400[drone_ducked];
    [ambient][narr]sidechaincompress=threshold=0.05:ratio=3:attack=30:release=500[amb_ducked];
    [drone_ducked][amb_ducked][accent][narr]amix=inputs=4:duration=longest:normalize=0[mix];
    [mix]loudnorm=I=-14:LRA=11:TP=-1.5[out]
  " \
  -map "[out]" -c:a aac -b:a 256k audio_3layer.aac

# Step 4: Mux with video
ffmpeg -y -i "$VIDEO" -i audio_3layer.aac -c:v copy -c:a copy -shortest renders/draft_3layer.mp4
```

**Key points**:
- `sidechaincompress` ducks drone + ambient by ~3-6 dB when narrator speaking (mix priority per PAUTA § 25.3).
- Accents stay on (intentional cut-through during narration).
- Final `loudnorm` to -14 LUFS (Hard Rule #4 + INGENIERO § 2.1).

### 8.11.3 Mix volumes table per layer type

| Layer | Hook (0-9s) | Dilemma (15-80%) | Climax beat | Decision UI (countdown) | Outro/cliffhanger |
|---|---|---|---|---|---|
| Drone | 0.10 | 0.13 | 0.13 | 0.13 | 0.08 |
| Ambient | 0.12 | 0.15-0.18 | 0.10 (give space) | 0.10 | 0.12 |
| Accent | n/a (or 1 cue) | 0.20-0.30 per dilemma lock | 0.55-0.65 (flash impact) | 0.30-0.40 per tick | 0.20 fade-out |

**Default fallback** if architect SPEC doesn't specify section-by-section: drone=0.13, ambient=0.15, accent=0.30 with `loudnorm` post-mix.

### 8.11.4 Validation post-mix

```bash
# Verify 3-layer presence via spectrogram analysis
ffmpeg -i renders/draft_3layer.mp4 -lavfi showspectrumpic=s=1920x1080:mode=combined spectrogram.png
# Visual check: 3 distinct horizontal bands (40-200 / 200-2000 / 2000+ Hz) present 60%+ of timeline width
# OR use audit-audio.py extension (Phase 2 forward)
```

### 8.11.5 Canonical validation status

```yaml
canonical_validation_status: "validated_4_videos_2026_05_21"
validated_against_canonical_refs:
  - "Ref-2 cockpit 3-layer → 10/10 audio (canonical gold standard per Gemini Vision)"
  - "Ref-1 mina 3-layer → 9/10 audio"
  - "cinema-abandonado iter 6 1-layer minimal → 9/10 (narrator-carried, risky)"
validation_methodology: "Gemini Vision audio dimension comparative + 3-layer presence inspection"
validated_at: 2026-05-21
phase_2_forward:
  - "Build audit-audio.py extension: spectrogram-based 3-layer detection threshold"
  - "Add ElevenLabs SFX prompts library/sfx-catalog.json: drone-horror-subharmonic + ambient-cinema-projector + accent-canonical pack"
```

---

## § 8.12 — PACING MARKERS PER SHOT (NEW 2026-05-21 — comparative analysis cinema cuts/min vs canonical band)

> **Authority**: `PAUTA-MASTER § 23` (Cuts/min canonical band 18-22 creative authority) + Gemini Vision comparative analysis 2026-05-21.
> **Trigger**: cinema-abandonado iter 1-6 shipped at 12 cuts/min — below canonical Gemini-perceived band 18-22. Forward: engineer builds per-shot durations to support architect's pace target.

### 8.12.1 Per-shot duration target math

For target **Gemini-perceived cuts/min = 18-22** (architect's PAUTA § 23 band):

```
total_perceived_cuts = (cuts_per_min_target) × (duration_min)

Example: 90s reel @ 20 cuts/min → 30 perceived cuts total
Example: 75s reel @ 18 cuts/min → 22 perceived cuts total
Example: 95s reel @ 22 cuts/min → 34 perceived cuts total
```

**Perceived cuts include**:
- Primary shot changes (1 per shot entry in SPEC `shot_list[]`)
- Variant inserts within shots >4s (-a, -b, -c per Hard Rule #5)
- Reaction shot inserts (hand-close-up, eye-close-up, setting detail)
- Effects library transitions counted as cuts: `hard-cut-with-whoosh`, `light-flash-impact`, `glitch-transition`
- NOT counted: `cross-fade-0.5s`, `cross-fade-1.0s`, `fade-to-black-1.0s` (perceived as continuous)

### 8.12.2 Per-shot duration build process

**Step 1 — Compute target cuts**:
```python
# After receiving SPEC from architect
total_duration_s = spec['video']['total_duration_s']
target_cuts_per_min_low = 18
target_cuts_per_min_high = 22
target_cuts_low = int(target_cuts_per_min_low * total_duration_s / 60)
target_cuts_high = int(target_cuts_per_min_high * total_duration_s / 60)
print(f"Target perceived cuts: {target_cuts_low}-{target_cuts_high}")
```

**Step 2 — Count SPEC declared cuts**:
```python
declared_shots = len(spec['shot_list'])
declared_variants = sum(len(s.get('variants', [])) for s in spec['shot_list'])
declared_reaction_inserts = sum(len(s.get('reaction_inserts', [])) for s in spec['shot_list'])
declared_cuts = declared_shots + declared_variants + declared_reaction_inserts
print(f"SPEC declares: {declared_cuts} perceived cuts")
```

**Step 3 — Gap check + escalation**:
```python
if declared_cuts < target_cuts_low:
    print(f"⚠️ SPEC short by {target_cuts_low - declared_cuts} cuts. Escalate to architect:")
    print(f"   Request mini-cuts via variants OR reaction inserts OR counterfactual quick-flashes")
    # DO NOT improvise mini-cuts as engineer (violates "engineer doesn't decide creative")
elif declared_cuts > target_cuts_high + 5:
    print(f"⚠️ SPEC over by {declared_cuts - target_cuts_high} cuts. Check pace doesn't fragment narrative.")
else:
    print(f"✅ SPEC within band. Proceed to per-clip duration build.")
```

**Step 4 — Per-clip duration assignment**:
```python
# Allocate duration per shot to total
remaining_duration = total_duration_s
remaining_shots = declared_shots

for shot in spec['shot_list']:
    if shot.get('fixed_duration_s'):  # architect locked in (countdown, cliffhanger, etc.)
        duration = shot['fixed_duration_s']
    else:
        # Default = remaining / remaining_shots, clamped per shot type
        default = remaining_duration / remaining_shots
        # Clamp by shot type:
        if shot['type'] == 'hook_intro':
            duration = min(default, 9.0)  # canonical hook ≤9s
        elif shot['type'] == 'dilemma_reaction':
            duration = min(default, 4.0)  # canonical dilemma beats ≤4s
        elif shot['type'] == 'climax_peak':
            duration = min(default, 6.0)
        else:
            duration = default
    shot['computed_duration_s'] = duration
    remaining_duration -= duration
    remaining_shots -= 1
```

### 8.12.3 Mini-cuts catalog (engineer's quick toolkit when architect approves)

When architect adds mini-cuts to SPEC, engineer implements:

| Mini-cut type | Duration | Implementation | When used |
|---|---|---|---|
| Variant insert -a/-b/-c | 1.5-2.5s | Different camera angle of same beat (wide → close-up → detail) | Shots >4s primary |
| Reaction shot | 1.0-2.0s | Character POV / hand close-up / object detail | Between dialogue beats |
| Counterfactual quick-flash | 0.5-1.0s | Brief insert of alternate path during main path | Hints stakes (post PAUTA § 24) |
| Setting micro-detail | 0.8-1.5s | Architectural close-up (clock, projector, doorknob) | Establishes time/place |
| POV hand insert | 0.5-1.2s | First-person hand reaching/touching | First-person POV per memory `first_person_pov` |

### 8.12.4 Effects library transitions counted as cuts (per § 8.13 NEW)

When using `effects-library/transitions/`:
- `hard-cut-with-whoosh` = +1 cut
- `light-flash-impact` = +1 cut (use max 1-2 per reel per existing library README)
- `glitch-transition` = +1 cut
- `static-noise-transition` = +1 cut
- `projector-cue-cinema` = +1 cut
- `cross-fade-0.5s` = 0 cuts (perceived continuous)
- `cross-fade-1.0s` = 0 cuts (perceived continuous)
- `fade-to-black-1.0s` = 0 cuts (outro continuous)
- `black-screen-0.3s` = +0.5 cut (perceived as breath, ambiguous)
- `film-burn-transition` = +1 cut

### 8.12.5 Canonical validation status

```yaml
canonical_validation_status: "pending_full_canonical_gemini_pass"
validated_against_canonical_refs:
  - "Ref-1 mina 21 cuts/min (Gemini Vision 2026-05-21)"
  - "Ref-2 cockpit 13 cuts/min modulated (Gemini Vision 2026-05-21)"
  - "Ref-3 metro 28 cuts/min (Gemini Vision 2026-05-21)"
  - "cinema-abandonado 12 cuts/min BELOW band (Gemini Vision 2026-05-21)"
validation_methodology: "Gemini Vision direct cuts/min report — 4 videos"
validated_at: 2026-05-21
caveat: "Gemini-perceived band 18-22 NOT same as INGENIERO § 3.1 de-clustered band 2.75-5. Reconciliation in PAUTA § 23.3."
phase_2_forward:
  - "Gemini Vision pass on remaining 7 F1 refs to confirm band"
  - "Triangulate Gemini-perceived vs de-clustered metric ratio"
```

---

## § 8.13 — EFFECTS LIBRARY USAGE TABLE (NEW 2026-05-21 — Phase 2 forward usage rules)

> **Authority**: `ai-video-production/templates/effects-library/README.md` + comparative analysis cinema (hard cuts + zooms only) vs canonical refs (transition variety).
> **Trigger**: cinema-abandonado iter 1-6 used only hard cuts + zoom transitions — Gemini editing dimension 8/10 (predictable). Canonical refs use varied transitions per beat type.

> ⭐ **TIERED catalogs (PRE-4.K 2026-05-27, "Disponibilidad ≠ Uso")**: las transitions de la tabla viven en DOS capas. **Capa A** (`ai-video-production/templates/effects-library/transitions/`) = primitivas universales: `cross-fade-0.5s`, `cross-fade-1.0s`, `hard-cut-with-whoosh`, `black-screen-0.3s`, `fade-to-black-1.0s`, `light-flash-impact`, `glitch-transition`. **Capa B** (`horror-choice-format/effects-library/transitions/`) = sub-genre horror: `film-burn-transition`, `projector-cue-cinema`, `static-noise-transition`. El engineer pasa `--effects-dir` con AMBOS catálogos (Capa A + Capa B) al correr `apply-effects-between-clips.py`. Disponibilidad ≠ prescripción: el SPEC `shot_list[].transition_out` elige. Cada recipe declara `xfade_transition` + `xfade_fidelity` (Option D PRE-4.J): los 5 `approximate` (light-flash/black-screen/fade-to-black/film-burn/static-noise) emiten WARNING en producción (chained-xfade lossy).

### 8.13.1 When to use which transition (by beat type)

| Beat type | Recommended transition | Effects lib file | Why |
|---|---|---|---|
| **Within-scene beat connection** (same character, same setting, time-continuous) | `cross-fade-0.5s` | `cross-fade-0.5s.json` | Invisible blend, preserves continuity |
| **Within-scene time jump** (later same day, memory dissolve) | `cross-fade-1.0s` | `cross-fade-1.0s.json` | Slow deliberate, reads as "later" |
| **Scene change default workhorse** | `hard-cut-with-whoosh` | `hard-cut-with-whoosh.json` | Preserves cuts/min target, audio sting | 
| **Hook countdown impact** | `hard-cut-with-whoosh` (or AVU bundled per § 7.11.5) | `hard-cut-with-whoosh.json` | High-energy entry to body |
| **Decision UI / choice freeze** | `black-screen-0.3s` + freeze frame | `black-screen-0.3s.json` | Lets choice land |
| **Decision lock-in (countdown ends, path commits)** | `light-flash-impact` | `light-flash-impact.json` | White flash + sharp SFX (high impact, USE SPARINGLY) |
| **Climax peak / plot twist reveal** | `light-flash-impact` | `light-flash-impact.json` | MAX 1-2× per reel per library README |
| **Counterfactual quick-flash insert** (per PAUTA § 24) | `glitch-transition` or `static-noise-transition` | `glitch-transition.json` / `static-noise-transition.json` | Signals "what if" alternate reality |
| **Cinema-genre scene change** | `projector-cue-cinema` | `projector-cue-cinema.json` | Diegetic, reel-change feel (use when setting = cinema/theater) |
| **Cinema flashback / memory bloom** | `film-burn-transition` | `film-burn-transition.json` | Warm orange consumes frame |
| **Outro before cliffhanger card** | `fade-to-black-1.0s` | `fade-to-black-1.0s.json` | Universal close pattern (9/10 canonicals per library README) |
| **Narrative comma / pause / breath** | `black-screen-0.3s` | `black-screen-0.3s.json` | Brief black insert, lets beat land |

### 8.13.2 Transition variety rule per reel

**Minimum variety target** (avoid cinema iter 1-6 anti-pattern of hard-cut + zoom only):

| Reel section | Min different transition types | Note |
|---|---|---|
| Hook | 1 (default = `hard-cut-with-whoosh` to body) | Hook = continuous shot per INGENIERO § 3.2 |
| Body (dilemmas) | **3 different types** | E.g. `hard-cut-with-whoosh` + `cross-fade-0.5s` + `light-flash-impact` (sparingly) |
| Climax | 1-2 (e.g. `light-flash-impact` + `cross-fade-1.0s` post-climax) | High impact, then breathe |
| Outro | 1 (`fade-to-black-1.0s`) | Canonical close |

**Total target**: ≥4 distinct transition types per ~90s reel. Cinema iter 1-6 used 2 (hard cuts + zooms) → fell short.

### 8.13.3 Implementation per SPEC field

Architect SPEC v10 forward will include:
```yaml
shot_list:
  - shot_id: shot_02
    type: dilemma_lock_in
    transition_out:
      effect: "light_flash_impact"
      effects_library_ref: "effects-library/transitions/light-flash-impact.json"
      duration_s: 0.2
      sting_audio: "effects-library/audio-stings/whoosh-warm.mp3"
```

Until v10 lands, engineer reads SPEC `shot_list[].transition_out.effect` field if present, else defaults to `hard-cut-with-whoosh` for scene changes + `cross-fade-0.5s` for within-scene beats.

### 8.13.4 Cost analysis

Effects library transitions are **procedural ffmpeg recipes** (Hairloss for free):
- Audio stings are already in `audio-stings/` (no ElevenLabs spend).
- ffmpeg render = ~2-5% added render time per transition.
- **Total cost: $0 per video** (purely engineering effort).

### 8.13.5 Canonical validation status

```yaml
canonical_validation_status: "validated_partial_via_library_README_canonical_refs"
validated_against_canonical_refs:
  - "fade-to-black-1.0s: 9/10 canonical refs use for outro (per library README)"
  - "hard-cut-with-whoosh: matches canonical refs Ref-1 + Ref-3 hard-cut dominant style (Gemini Vision 2026-05-21)"
  - "light-flash-impact: canonical refs use for plot twist reveals (per existing library doc)"
  - "cinema-abandonado iter 1-6: USED ONLY hard cuts + zooms (anti-pattern variety <2)"
validation_methodology: "Effects library README canonical claims + 4-video comparative Gemini analysis"
validated_at: 2026-05-21
phase_2_forward:
  - "Build transition_out SPEC schema field v10 mandatory per shot"
  - "Gemini Vision transition variety count on F1 refs to confirm ≥4 distinct/reel canonical"
```

---

## § 8.14 — ANCHOR STRICT MODE ALL SHOTS POLICY (NEW 2026-05-21 — comparative analysis character consistency)

> **Authority**: comparative analysis cinema-abandonado character consistency 7/10 vs canonical Ref-2 9/10 — Ref-2 won character dimension via strict anchor consistency across all shots, cinema used STRICT only on hero shots.
> **Trigger**: cinema iter 1-6 — character Salvador "morphing of facial features between scenes" per Gemini direct quote. Loss attributable to non-strict anchors on non-hero shots.

### 8.14.1 Rule

**ALL anchors in shot_list[] generate with STRICT mode** (Nano Banana / Midjourney --cref + sref, or equivalent character-lock mode per model). NOT just hero shots (hook + climax + cliffhanger). Forward: every shot's character anchor goes through STRICT validation pass.

### 8.14.2 Why

Empirical comparison character consistency dimension:

| Video | Character consistency score | Mechanism | Gemini quote |
|-------|---|---|---|
| **Ref-2 cockpit (Victor/Axel)** | **9/10** ⭐ | STRICT anchors all shots | *"Victor's skeletal texture, hat, and facial structure remain identical across cockpit, tarmac, and exterior shots"* |
| Ref-1 mina (Bruno/Pablo) | 6/10 | Likely STRICT hero only | *"Bruno's facial structure shifts significantly... by 0:50, his skin becomes heavily wrinkled"* |
| Ref-3 metro (Nano/Teresa) | 6/10 | Likely STRICT hero only | *"Nano Banano's overalls and head shape shift slightly between shots (AI hallucination)"* |
| **cinema-abandonado (ours)** | **7/10** ⚠ | STRICT hero only | *"Salvador's face shifts slightly between the lobby and the projection room (stitches change density)"* |

**Mechanism**: Ref-2's 9/10 character consistency directly contributed to its 9.0/10 overall score (the highest of the 4 comparison). Cinema's 7/10 character consistency directly contributed to its 8.6/10 (second-highest, gap = 0.4 points). STRICT mode on non-hero shots was the marginal cost that bought the gap.

### 8.14.3 Implementation per shot

```python
# Per shot in SPEC shot_list[]:
for shot in spec['shot_list']:
    # Previously: STRICT only on hero shots
    # OLD: if shot['hero']: strict = True
    
    # NEW POLICY: STRICT on ALL shots
    strict = True
    
    # Generate anchor with STRICT mode
    if model == 'nano-banana':
        flags = ['--cref', shot['character_anchor_url'], '--sref', shot['style_anchor_url'], '--cw', '100']
    elif model == 'midjourney':
        flags = ['--cref', shot['character_anchor_url'], '--cw', '100', '--sref', shot['style_anchor_url']]
    elif model == 'flux-character':
        flags = ['--character-lock-mode', 'strict']
    # Submit + audit per shot
```

### 8.14.4 Cost impact (forward) — UPDATED 2026-05-21 PM post enterprise free clarification

⚠️ **COST RESET 2026-05-21 PM**: User confirmed Gemini + ElevenLabs API keys = enterprise = $0 cost. Previous cost projections OBSOLETE for Gemini-based work.

| Item | Old projection (paid) | NEW reality (enterprise) | Delta |
|---|---|---|---|
| Nano Banana image generation per video (anchors + shots all STRICT) | ~$2.90-3.80 | **$0** | -$2.90-3.80 |
| Gemini Vision validation per shot | ~$1.00-1.20 | **$0** | -$1.00-1.20 |
| **Total added cost per video** | — | **$0** (was ~$1.10-1.70) | — |

**NEW trade**: $0 added cost for STRICT all shots policy → there is NO reason NOT to use STRICT on every shot. This becomes default canonical.

**ONE caveat**: enterprise rate limits might constrain volume. If Gemini API quotas hit, fall back to selective STRICT. But assume unlimited for now.

### 8.14.5 Validation per shot

```bash
# Per shot anchor:
.venv/bin/python scripts/validate-anchor-strict.py \
  --anchor-target assets/anchors/character_<name>_strict.png \
  --shot-render assets/shots/<shot_id>.png \
  --threshold 0.85
# Returns face-similarity score via Gemini Vision. <0.85 → regen with stricter prompt + sref reinforcement.
```

### 8.14.6 When to relax (escape hatch)

STRICT all-shots is policy default. Engineer can request architect approval to relax IF:
- Character is **occluded** (back-of-head, silhouette, hidden by setting)
- Character is **distant background** (small in frame, body language only matters)
- Character is in **deliberate transformation beat** (architectural design choice — e.g. "Salvador's stitches loosen" climax)

In those cases SPEC `shot_list[].anchor_strict: false` declared explicitly + architect approval gate.

### 8.14.7 Canonical validation status

```yaml
canonical_validation_status: "validated_4_videos_2026_05_21_qualitative"
validated_against_canonical_refs:
  - "Ref-2 cockpit STRICT all shots → 9/10 character consistency (canonical gold)"
  - "cinema-abandonado STRICT hero only → 7/10 character consistency (anti-pattern)"
  - "Ref-1 mina + Ref-3 metro likely STRICT hero only → 6/10 character consistency"
validation_methodology: "Gemini Vision character dimension comparative + reverse-engineering from consistency scores"
validated_at: 2026-05-21
caveat: "Canonical refs anchor-mode policy not directly observable from output, inferred from consistency outcomes"
phase_2_forward:
  - "Build validate-anchor-strict.py script + integrate per CP3 (shot images checkpoint)"
  - "Measure cost delta in real production: target ~+$1.10-1.70/video"
  - "Track character consistency Gemini dimension score improvement target ≥8/10 per Hard Rule #23 outcome"
```

---

## § 8.15 — HAILUO PRO 1080P ESCALATION POLICY (NEW 2026-05-21 — comparative analysis AI artifacts hero shots)

> **Authority**: comparative analysis cinema visual artifact score 7/10 vs canonical Ref-2 8/10 — cinema's lower score driven by visible rubbery hands (0:31, 1:05) + floaty walk (0:49). Hailuo Std produced these artifacts; Pro 1080p would have produced better fidelity on those specific shot types.
> **Trigger**: cinema iter 1-6 — Gemini "Significant AI 'melting' on the hands... Salvador's walk at 0:49 is a bit 'floaty,' lacking weight or foot-planting."

### 8.15.1 Escalation rule per shot type

| Shot type | Std vs Pro default | Rationale |
|---|---|---|
| **HERO shots** — hook + climax peak + cliffhanger reveal | **DEFAULT Hailuo Pro 1080p** | Highest viewer attention, frame-by-frame inspection likely |
| **Walking / full-body action shots** | **DEFAULT Hailuo Pro 1080p** | Std model floaty-walk failure mode (cinema 0:49 case) |
| **Hand-close-up shots** | **DEFAULT Hailuo Pro 1080p** | Std model "melting fingers" failure mode (cinema 0:31, 1:05 cases) |
| **Lip-sync close-up dialogue shots** | **DEFAULT Hailuo Pro 1080p** | Lip-sync precision matters more at close range |
| **Animal / creature with anatomy** | **DEFAULT Hailuo Pro 1080p** | Std model anatomical drift |
| Reaction inserts (hand-close, eye-close, setting detail) | Std (cheaper, fast, brief) | <2s duration, viewer doesn't inspect |
| Background ambient shots | Std (cheaper) | Low attention area |
| Setting establishing shots (no characters) | Std (cheaper) | Architectural / environmental, lower bar |
| Variant -a/-b/-c micro-inserts | Std (cheaper) | Brief, supports primary shot |

### 8.15.2 Cost impact (forward) — UPDATED 2026-05-21 PM new cost model

⚠️ **COST RESET 2026-05-21**: Replicate is now the ONLY paid vendor for video #3+. Gemini + ElevenLabs API = enterprise FREE.

**Per-tier Replicate pricing (CURRENT)**:

| Tier | Cost per 6s clip | Use case |
|---|---|---|
| Hailuo Std 768p | ~$0.27 ($0.045/s) | Default for non-hero shots |
| Hailuo Pro 1080p | ~$0.60 ($0.10/s) | DEFAULT hero + walking + hand-close-up |
| Kling 2.5 Pro | ~$0.45 ($0.075/s) | Alternative if Hailuo Pro fails |
| Veo 3.1 Standard | ~$2.40 ($0.40/s) retail | Premium — **POTENTIALLY FREE if enterprise covers Veo** (verify) |

**Per video typical shot count requiring Pro escalation**:
- Hero shots: 3 (hook + climax + cliffhanger)
- Walking shots: ~1-2
- Hand-close-ups: ~1-2 (per dilemma)
- Lip-sync close-ups: ~1-2 (per character speaking on-screen)
- **Total escalation: ~5-7 shots × Pro $0.60 = ~$3-4.20/video** (Replicate)

**Full video #3 Replicate cost estimate**:
- 5-6 shots Pro: $3-3.60
- 16-17 shots Std: $4.32
- Hedra lip-sync: $1.50 (optional but recommended)
- **Total Replicate per video: ~$8-9** (vs old $14-16 model)

**ENTERPRISE FREE (no cost)**:
- Gemini Nano Banana image gen
- Gemini Vision audits (calibrated v4 + audit-frames-granular)
- ElevenLabs TTS + SFX + music + voice cloning
- Whisper (always local)

### 8.15.3 Implementation per shot

```python
# In SPEC shot_list[] for each shot:
def select_model_tier(shot):
    hero_types = {'hook', 'climax_peak', 'cliffhanger_reveal'}
    pro_motion_types = {'walking', 'full_body_action', 'hand_close_up', 'lip_sync_close_up', 'creature_with_anatomy'}
    
    if shot['type'] in hero_types or shot.get('hero', False):
        return 'hailuo_pro_1080p'
    if shot['motion_type'] in pro_motion_types:
        return 'hailuo_pro_1080p'
    if shot.get('force_pro', False):  # architect override
        return 'hailuo_pro_1080p'
    return 'hailuo_std'

# Submit to Replicate:
model_id = 'minimax/hailuo-02-pro' if tier == 'hailuo_pro_1080p' else 'minimax/hailuo-02-standard'
# (model IDs per video-director/MODEL-BENCHMARK.md — verify current at runtime)
```

### 8.15.4 SPEC v10 schema field

Architect SPEC v10 forward will include:
```yaml
shot_list:
  - shot_id: shot_03_hands_close_ticket
    motion_type: "hand_close_up"
    model_tier_override: null  # null = auto-select per § 8.15.1 table
    # OR explicit:
    # model_tier_override: "hailuo_pro_1080p"  # force Pro
```

Until v10 lands, engineer applies decision table from § 8.15.1 deterministically per shot.

### 8.15.5 Validation post-render

Per shot rendered via Hailuo Pro:
```bash
# Visual artifact check via Gemini Vision per shot
.venv/bin/python scripts/audit-frames-granular.py \
  --video assets/clips/shot_03_hands_close.mp4 \
  --check rubbery_hands,floaty_walk,anatomical_drift \
  --threshold strict
# If still artifacts despite Pro → escalate to architect (consider hero treatment, different model, regen)
```

### 8.15.6 Cross-ref MODEL-BENCHMARK.md

Verify current Hailuo Pro 1080p availability + pricing + reliability:
- `video-director/MODEL-BENCHMARK.md § 1.1 Image-to-video tier` (refresh every 60 days per memory `reference_model_benchmark`)

### 8.15.7 Canonical validation status

```yaml
canonical_validation_status: "validated_via_failure_mode_analysis_2026_05_21"
validated_against_canonical_refs:
  - "cinema-abandonado Hailuo Std hands 0:31 + 1:05 + walk 0:49 → visual 7/10 (anti-pattern)"
  - "Ref-2 cockpit visual 8/10 likely Pro tier or equivalent (Luma/Runway Gen-2 per Gemini guess)"
  - "Ref-1 mina + Ref-3 metro visual 5/10 likely Std tier (consistent with hands artifacts present)"
validation_methodology: "Gemini Vision artifact identification + model tier reverse-engineering from quality outcomes"
validated_at: 2026-05-21
caveat: "Canonical refs exact model tier not observable from output, inferred from visual fidelity outcomes"
phase_2_forward:
  - "Build SPEC v10 schema model_tier_override field"
  - "Measure visual dimension delta in real production: target ≥8/10 visual per Hard Rule #23 outcome"
  - "Track cost delta target: ~+$3-4.20/video Pro escalation"
  - "Refresh MODEL-BENCHMARK.md if Hailuo Pro pricing/availability changes"
```


---

## § 8.16 — EXECUTION CONTINUITY IMPLEMENTATION (NEW 2026-05-21 PM late — GAP #40 codification)

> **Authority**: GAP #40 EXECUTION CONTINUITY identified as PRIMARY gap own production → canonical via user articulation 2026-05-21 PM + calibrated Gemini v4 validation (matadero exec dim 4.8/10 vs Ref-A 10/10).
> **The single biggest factor separating 7.85 → 9.9+ perceptual**.

### 8.16.1 Rule

Every shot's animation prompt MUST encode motion bridging to next shot. Specifically per shot in shot_list[]:

```yaml
shot_list:
  - shot_id: shot_03_walking_corridor
    motion_bridge_intent:  # NEW field
      from_previous: "continuing walk forward from shot_02 same speed"
      to_next: "POV approaches doorway visible in frame"
    pov_traversal: "walking_forward"  # enum
    audio_layer_continuity: ["drone_base", "footsteps_continuous", "ambient_corridor"]
    visual_style_lut: "warm_industrial_cool_v2"  # same LUT as previous + next
```

### 8.16.2 Four sub-criteria per cut transition

| Sub-criterion | Implementation | Penalty if missing |
|---|---|---|
| **1. POV motion bridge** | Hailuo prompt: "POV walking forward at constant 0.5m/s pace OR descending at gravity OR rotating head left" | Cut feels teleport |
| **2. Audio bridge** | At least 1 sound layer (drone OR ambient OR foley) continues without cutoff at edit point | Silence at cut = jarring |
| **3. Visual style consistent** | Same color LUT + grading + lighting style applied shot N and N+1 | Style jump = uncanny |
| **4. Kinetic momentum** | Shot N+1 first frame velocity ≈ shot N last frame velocity (smooth motion continuity) | Sudden stop = jarring |

### 8.16.3 Implementation Hailuo prompt template (for motion bridge shots)

```python
def build_motion_bridge_prompt(shot):
    """Generate Hailuo prompt encoding motion bridge intent."""
    base = shot['description']
    bridge_from = shot.get('motion_bridge_intent', {}).get('from_previous', '')
    bridge_to = shot.get('motion_bridge_intent', {}).get('to_next', '')
    pov_motion = shot.get('pov_traversal', 'static')
    
    motion_clause_map = {
        'walking_forward': 'POV camera moving forward at steady walking pace (0.5 m/s), camera at human eye level, slight bob from footsteps',
        'descending': 'POV camera descending smoothly (0.3 m/s downward), gravity-influenced motion',
        'ascending': 'POV camera rising upward (0.3 m/s), counter-gravity motion',
        'approaching_character': 'POV moving toward character in frame, getting closer each second',
        'turning_left': 'POV camera rotating left 30 degrees over 2 seconds, smooth rotation',
        'turning_right': 'POV camera rotating right 30 degrees over 2 seconds, smooth rotation',
        'static_with_micro_bob': 'POV camera stationary with subtle natural breathing micro-bob',
    }
    motion_clause = motion_clause_map.get(pov_motion, '')
    
    prompt = f"""{base}

CAMERA / POV: {motion_clause}

CONTINUITY:
- From previous shot: {bridge_from}
- Leading to next shot: {bridge_to}
- Camera speed/motion should be CONSISTENT with adjacent shots, no abrupt stops or jumps.
"""
    return prompt
```

### 8.16.4 Audio bridge implementation

Per cross-clip music layer (PIPELINE.md § 13.7.5 Layer 3 — cross-clip continuous):
- `drone_base` layer plays 0-duration_s continuously → bridges all cuts
- `ambient_room_continuous` layer plays per-section continuously → bridges within section
- Specific event SFX (Layer 1 per-clip diegetic) may end at clip boundary but background layers MUST sustain

### 8.16.5 Visual style consistency

```python
# Same LUT applied across multi-shot section:
# Section "narrative_pre_decision" shots 1-6: LUT "warm_industrial"
# Section "decision_moment" shots 7-9: LUT transition "warm_industrial → cool_decision"
# Section "consequence_pathA" shots 10-15: LUT "cool_horror"

# At cut between shots: LUT MUST be SAME within section.
# At section boundary (rare): transition LUT explicit + audible cue marker.
```

### 8.16.6 Validation per cut transition

```bash
# Per cut, run continuity verification
.venv/bin/python scripts/audit-execution-continuity.py \
  --clip-prev assets/clips/shot_03.mp4 \
  --clip-next assets/clips/shot_04.mp4 \
  --check pov_motion_continuity,audio_layer_continuity,lut_consistency,kinetic_momentum
# Exit 0 = continuity ✓ / Exit 1 = teleport detected = FAIL
```

(Script to build Phase 3 priority — currently use manual frame extraction + visual review)

### 8.16.7 SPEC v10 schema fields needed (architect to codify)

```yaml
shot_list:
  - shot_id: <id>
    motion_bridge_intent:
      from_previous: <string description>
      to_next: <string description>
    pov_traversal: <enum: walking_forward | descending | ascending | approaching_character | turning_left | turning_right | static_with_micro_bob>
    audio_layer_continuity: [<list of layer_ids that must NOT cut at boundary>]
    visual_style_lut: <lut_id reference>
    
# Plus per-section:
narrative_sections:
  - section_id: pre_decision
    shot_ids: [shot_01..shot_06]
    audio_layer_continuity_within_section: [drone_base, ambient_corridor]
    visual_style_lut: warm_industrial
```

### 8.16.8 Cost impact

- Hailuo prompts more verbose (~100-200 chars added per shot): $0 (no per-token charge on Replicate Hailuo)
- Cross-clip music layer (Layer 3 PIPELINE § 13.7.5): no additional cost, just additional ElevenLabs compose_music call which is enterprise FREE
- Validation script: $0 (local ffmpeg + librosa)
- Estimated cost impact: **$0**

This is a PROCESS amendment, not a cost addition.

### 8.16.9 Canonical validation status

```yaml
canonical_validation_status: "validated_via_calibrated_gemini_v4_2026_05_21"
validated_against_canonical_refs:
  - "Ref-A cave (Felipe+Enzo) Gemini v4 exec dim 10/10 → user 10/10"
  - "Ref-1 mina (Bruno+Pablo) Gemini v4 exec dim 10/10 → user 9.9/10"
  - "matadero v1 Gemini v4 exec dim 4.8/10 → user 7.9 (anti-pattern teleport-cuts)"
  - "cinema-abandonado v2 Gemini v4 exec dim 5.5/10 → user 7.8 (anti-pattern)"
validation_methodology: "Calibrated Gemini v4 EXECUTION CONTINUITY dimension 30% weight + manual cut-by-cut analysis"
validated_at: 2026-05-21
phase_3_forward:
  - "Build audit-execution-continuity.py automated check script"
  - "Validate motion_bridge_intent + pov_traversal + audio_layer_continuity fields work in SPEC v10"
  - "Test on video #3 first ship with calibrated Gemini v4 — confirm exec dim ≥9 achievable"
```

---

## § 8.17 — LIP-SYNC INTEGRATION (Veo 3.1 DEFAULT — enterprise free) — Phase 3 forward 2026-05-21

> **Authority**: Phase 3 priority post Phase 2 architectural refactor + cost model reset 2026-05-21. Lip-sync precision was the 1/8 remaining bug class not eliminated by Phase 2.
> **🎯 CRITICAL UPDATE 2026-05-21 PM late**: User confirmed Gemini Enterprise (Business Edition) includes Veo 3.1 as capacity (replaces Veo 3.0). Lip-sync via Veo 3.1 = **$0 cost**. Hedra demoted to fallback.

### 8.17.1 When to use lip-sync

Lip-sync model required when:
- Character speaks on-screen (face visible + audio character speech)
- Without lip-sync: uncanny mismatch between lip motion + audio → realismo broken
- Anti-pattern #9 AUDITOR-PROTOCOL: "Audio-visual lip-sync realism violations"

Per video, typical shots requiring lip-sync:
- Hook character intro (if dyad speaks): ~2 shots × ~3s each = 6s
- Decision moment narrator/character dialogue: ~3 shots × ~4s = 12s
- Climax confrontation character speech: ~2 shots × ~4s = 8s
- **Total typical: ~25-30s of lip-sync per video**

### 8.17.2 Vendor options

**Option A — Hedra Character-3 (Replicate, $0.05/s)**:
- **Best in class** specialist 9.5/10 lipsync quality (per MODEL-BENCHMARK.md.bak.sprint-combinado-8)
- Audio-driven: input audio + character photo → lip-synced video output
- Drop-in: insert into Hailuo animation pipeline as character-talking shots
- Cost: $0.05/s × 30s = **$1.50/video**
- Validated by Hedra Studio + Replicate
- API: api.hedra.com (feb 2026 launch) OR atlabs.ai third-party OR Replicate hosted

**Option B — Veo 3.1 (Gemini, ENTERPRISE FREE confirmed 2026-05-21 PM)** ⭐⭐ DEFAULT:
- Native audio + lip-sync in single generation (no separate step)
- Generates ENTIRE scene visual + audio + lip-sync end-to-end
- Quality: 9/10 video-driven
- Cost: **$0** (Gemini Enterprise Business Edition includes Veo 3.1 as capacity, NOT add-on)
- ✅ Verified user 2026-05-21: "Veo 3.1 reemplazó a Veo 3.0 dentro del plan Gemini Enterprise (Business Edition) como capacidad incluida"
- 4K + native 9:16 vertical (perfect for IG Reel)
- API endpoint: Gemini API (same auth as Vision, separate model id for veo3)
- ⚠️ Caveats forward to verify:
  - Enterprise quotas / rate limits per month — unknown
  - NSFW filter — Veo 3.1 historically rejects horror gore content; may need to soften prompts OR fallback to Hedra
  - Generation time slower than Hailuo (~minutes per clip vs seconds)
- API: Gemini API via gemini-3-flash-preview or veo3 endpoint

**Option C — Sync.so (Replicate, $0.10-0.30/s)**:
- Post-process — needs existing video + audio → outputs lip-synced version
- Quality: 7/10
- ⛔ Skip — Hedra strictly better quality at lower cost

**Option D — ElevenLabs**:
- No video lip-sync product. Only audio generation.
- Can pair with Hedra/Veo as audio source.
- Not a standalone lip-sync option.

### 8.17.3 Recommendation for video #3 — UPDATED 2026-05-21 PM late (user clarification Veo = generator)

**NEW DEFAULT: Veo 3.1 via Gemini Enterprise API** ⭐⭐:
- $0 cost (enterprise confirmed — Veo is GENERATOR, generates whole character-speaking shot end-to-end)
- Native audio + lip-sync + visual in single generation call
- Quality 9/10 video-driven
- 4K + native 9:16 vertical
- **Reframes lip-sync workflow**: NO separate "animate then lip-sync" pipeline. Veo generates the speaking shot WHOLE.
- Replaces Hailuo + Hedra for character-speaking shots specifically
- ⚠️ Test on 1 sample shot BEFORE committing entire video #3 to Veo (NSFW filter + quotas + quality validation)

**FALLBACK 1: Hailuo Pro + character anchor (no lip-sync)**:
- If Veo rejects shot content (NSFW gore filter), use Hailuo Pro to generate the visual
- Then either:
  - Accept slightly stiff lip-sync (Hailuo doesn't sync to audio explicitly)
  - OR add Hedra post-process for lip-sync on the still-character composition

**FALLBACK 2: Hedra Character-3 via Replicate**:
- $1.50/video cost (only when Veo rejects content AND we need precise lip-sync)
- 9.5/10 specialist quality
- Drop-in compatible with per-clip atomic pipeline
- Use case narrowed: character-speaking shots Veo rejected for NSFW reasons

### 8.17.4 Integration workflow (per-clip atomic compatible)

Per character-talking shot:

```bash
# Step 1: Generate character anchor with mouth-closed pose (Gemini Nano Banana STRICT) — FREE
.venv/bin/python scripts/image.py \
  --prompt "character_<name> talking head, mouth closed neutral, looking at camera, [setting]" \
  --strict \
  --output assets/anchors/character_<name>_talking_anchor.png

# Step 2: Generate character TTS audio for this shot (ElevenLabs) — FREE
.venv/bin/python scripts/tts.py \
  --voice <voice_id> --text "<dialog>" \
  --output assets/tts/shot_<id>_dialog.mp3

# Step 3: Hedra lip-sync animation (Replicate $0.05/s × shot_duration)
.venv/bin/python scripts/lip-sync-hedra.py \
  --image assets/anchors/character_<name>_talking_anchor.png \
  --audio assets/tts/shot_<id>_dialog.mp3 \
  --output assets/clips/shot_<id>_lipsynced.mp4 \
  --duration <shot_duration_s>
# Replicate model: hedra/character-3 (verify current endpoint)

# Step 4: Build atomic clip (per-clip atomic pipeline)
.venv/bin/python scripts/build_clip_atomic.py \
  --visual assets/clips/shot_<id>_lipsynced.mp4 \
  --audio-overrides "tts:assets/tts/shot_<id>_dialog.mp3" \
  --shot-id shot_<id>
```

### 8.17.5 Validation

```bash
# Per lip-sync shot:
.venv/bin/python scripts/gemini_midexec_vision.py \
  --hook atomic_post \
  --clip assets/clips-atomic/shot_<id>_atomic.mp4 \
  --captions assets/clips-atomic/shot_<id>_captions.json \
  --spec ../creative-specs/<id>.yaml \
  --shot-id shot_<id>
# Gemini Vision checks lip-sync alignment + caption sync + audio quality
```

### 8.17.6 Cost summary

| Item | Hedra default | Veo 3.1 enterprise free | Veo 3.1 retail |
|---|---|---|---|
| Lip-sync cost per video | $1.50 | $0 | $12 |
| Quality | 9.5/10 | 9/10 | 9/10 |
| Integration effort | Drop-in compatible | Native | Native |
| **Default recommendation** | ✅ DEFAULT | Use IF enterprise confirmed | Skip — too expensive |

### 8.17.7 Build script TODO

`scripts/lip-sync-hedra.py` — to build forward Phase 3 first video that uses lip-sync. Currently Hedra integration via Replicate is straightforward (similar to Hailuo call pattern).

### 8.17.8 Canonical validation status

```yaml
canonical_validation_status: "pending_video_3_first_use"
validated_against_canonical_refs:
  - "MODEL-BENCHMARK.md.bak.sprint-combinado-8 historical Hedra Character-3 9.5/10 specialist score"
  - "Refs canónicos lip-sync no validated empirically per-video — pending video #3 first use Hedra"
validation_methodology: "Industry benchmark + pending production validation"
validated_at: 2026-05-21
phase_3_forward:
  - "Build lip-sync-hedra.py script Replicate integration"
  - "Test on video #3 character-talking shots"
  - "Compare Hedra output quality vs Veo 3.1 if enterprise covers"
  - "Measure user perceptual delta with vs without lip-sync"
```


---

## § 8.18 — VEO 3.1 PRIMARY MODEL STRATEGY (enterprise free) — NEW 2026-05-21 PM late

> **Authority**: User confirmed 2026-05-21 PM "Veo 3.1 reemplazó a Veo 3.0 dentro del plan Gemini Enterprise (Business Edition) como capacidad incluida — no es un add-on aparte".
> **Implication**: Veo 3.1 = $0 cost via existing Gemini API key. Potentially replaces large portions of Replicate Hailuo spend.

### 8.18.0 ⚠️ API ROUTE CLARIFICATION (2026-05-21 PM late — user clarification)

**Veo 3.1 is a Google DeepMind model. Access route MATTERS for cost**:

| Route | Cost | Use |
|-------|------|-----|
| **Gemini API direct** (model `veo-3.1`) | **$0 ENTERPRISE** ✅ | DEFAULT — use this route |
| Replicate hosted Veo | Charged separately (NOT enterprise) | ❌ DO NOT use Veo via Replicate |
| Google AI Studio direct | Same enterprise key | Acceptable alternate |

**Implementation**: same `google-genai` Python library we use for Vision audits, just with `veo-3.1` model id. Same `GEMINI_API_KEY` env var.

**NEVER call Veo via Replicate** — that's a paid separate vendor host (no enterprise benefit). Always Gemini API endpoint.

### 8.18.0.1 Veo USE CASE — GENERATOR not DUBBER (user clarification 2026-05-21)

**Veo 3.1 is for GENERATING scenes from scratch, NOT post-process visual dubbing on existing video.**

User's distinction (from Google docs):
> "Elige Veo 3.1 si tu objetivo es crear contenido desde cero — short film, ad clip, cinematic scene donde personaje inventado dice diálogo unos segundos hiperrealistamente."
> "Sync Labs o HeyGen si ya tienes video grabado y solo necesitas traducir/cambiar audio sin volver a grabar."

**Tool taxonomy CLARIFIED**:

| Tool | Use case | Our pipeline forward |
|------|----------|---------------------|
| **Veo 3.1** (Gemini API enterprise) | GENERATE scene (visual + audio + lip-sync) from prompts + character anchor image | ✅ PRIMARY for character-speaking shots — generate whole shot end-to-end |
| Hailuo Std/Pro (Replicate) | GENERATE scene (visual only, no audio) from prompts + character anchor | ✅ For non-character shots OR Veo-rejected NSFW shots |
| Hedra Character-3 (Replicate) | Still photo → talking-head animation with audio sync | ⚠️ DEMOTED — Veo replaces this use case at $0 |
| Sync Labs / HeyGen | DUB existing real-life video to new audio (visual dub) | ❌ NOT our use case — we generate from scratch always |

**Translated to architectural decision per shot type**:

| Shot type | Primary tool | Fallback |
|---|---|---|
| Character speaking on-screen | **Veo 3.1** (generates whole shot incl. lip-sync) | Hailuo + Hedra if Veo NSFW reject |
| Character moving without speaking | Veo 3.1 OR Hailuo Pro (both fine) | n/a |
| POV traversal (no character on-screen) | Veo 3.1 OR Hailuo Std | n/a |
| Atmospheric / setting establishing | Veo 3.1 OR Hailuo Std | n/a |
| Gore / explicit horror content | **Hailuo Std/Pro** (Veo will reject NSFW) | n/a (Hailuo is the path) |

### 8.18.1 Veo 3.1 capabilities summary

| Feature | Veo 3.1 enterprise |
|---|---|
| Cost | **$0** (enterprise included) |
| Quality | 9/10 cinematic (premium tier — above Hailuo Pro) |
| Native audio in clip | ✅ YES (no separate TTS for character shots) |
| Native lip-sync | ✅ YES (no Hedra needed) |
| Resolution | 4K |
| Aspect ratio | Native 9:16 (perfect IG Reel) |
| Multi-image refs / ingredients-to-video | ✅ YES |
| Generation time | ~minutes per clip (slower than Hailuo seconds) |
| NSFW handling | ⚠️ Historically rejects horror gore (per MODEL-BENCHMARK) |
| API endpoint | Gemini API (model id veo3 / veo-3-1) |

### 8.18.2 Decision tree per shot — Veo 3.1 vs Hailuo

```
Per shot in shot_list[]:
  ┌─────────────────────────────────────────────────────┐
  │ 1. Is this shot's content acceptable to Veo filter? │
  │    (NO explicit gore, NO extreme body horror)       │
  └───────────┬───────────────────────┬─────────────────┘
              │ YES                    │ NO (gore/horror)
              ▼                        ▼
  ┌──────────────────────┐  ┌──────────────────────────┐
  │ 2. Has Veo enterprise │  │ Use Hailuo Std/Pro       │
  │    quota remaining?   │  │ (NSFW-friendly)          │
  └──────┬──────┬─────────┘  └──────────────────────────┘
         │ YES   │ NO
         ▼       ▼
  ┌──────────┐  ┌────────────────────────┐
  │ DEFAULT  │  │ Fallback Hailuo Pro    │
  │ Veo 3.1  │  │ (quota exhausted)      │
  └──────────┘  └────────────────────────┘

When uncertain → test on 1 sample shot first.
```

### 8.18.3 Cost model with Veo 3.1 primary

**Scenario A — Veo unlimited enterprise, all shots Veo**:
- All 22 shots × $0 (Veo) = **$0** Replicate spend
- Plus all Gemini + ElevenLabs FREE
- **Total video #3 cost: ~$0** (operational only)

**Scenario B — Veo for safe shots + Hailuo for gore shots** (REALISTIC):
- ~70% shots Veo-safe (15-16 shots × $0) = $0
- ~30% shots gore/horror → Hailuo Pro (6-7 shots × $0.60) = $3.60-4.20
- Lip-sync FREE via Veo for character shots
- **Total video #3 cost: ~$4** (Replicate Hailuo for gore shots only)

**Scenario C — Veo quota limited, hero shots only** (CONSERVATIVE):
- Hero shots (3) + lip-sync shots (3) via Veo = 6 × $0 = $0
- Rest (16) via Hailuo Std + 6 Pro escalation = $4.32 + $3.60 = $7.92
- **Total video #3 cost: ~$8** (was $9 with Hedra)

**Scenario D — Veo fails NSFW + content very horror-heavy**:
- All animation via Hailuo Std/Pro = $5-8
- Lip-sync via Hedra = $1.50
- **Total video #3 cost: ~$7-10**

### 8.18.4 NSFW filter risk mitigation

Per MODEL-BENCHMARK.md.bak.sprint-combinado-8: **"Veo 3.1, Sora 2, Midjourney, Ideogram, Runway, Imagen rechazan NSFW/horror gore."**

Strategy: prompt softening + content abstraction:
- "Cleaver-headed butcher with severed meat" → "tall industrial figure with helmet, abstract industrial setting"
- "Mouth devouring viewer" → "approaching shadow with abstract organic forms"
- "Blood and viscera" → "dark substance and atmospheric elements"
- "Gore explicit" → "horror-suggestive, atmospheric"

**Test methodology before video #3 commits**:
1. Pick 3 sample SPEC shot prompts (1 safe, 1 borderline, 1 horror)
2. Submit to Veo 3.1 + Hailuo Pro parallel
3. Compare outputs + check Veo accepts/rejects
4. If Veo rejects → soften prompt OR use Hailuo fallback
5. Document which shot types Veo accepts → architect can design SPEC v10 around constraints

### 8.18.5 Test bench (recommended before video #3 commits to Veo)

```bash
# Sample 1: SAFE shot (cinematic POV walking)
.venv/bin/python scripts/veo3.py \
  --prompt "POV first-person walking through abandoned cinema corridor, dim warm lights, peeling wallpaper, dust particles in air, cinematic style" \
  --duration 6 \
  --aspect 9:16 \
  --output assets/test/veo_safe.mp4

# Sample 2: BORDERLINE shot (uncanny character)
.venv/bin/python scripts/veo3.py \
  --prompt "tall thin uncanny figure standing in dark hallway, slight tilt of head toward camera, ambient horror atmosphere, no explicit content" \
  --duration 6 \
  --aspect 9:16 \
  --output assets/test/veo_borderline.mp4

# Sample 3: HORROR shot (gore-adjacent)
.venv/bin/python scripts/veo3.py \
  --prompt "matarife character with industrial helmet, abstract industrial setting, dim ambient lights" \
  --duration 6 \
  --aspect 9:16 \
  --output assets/test/veo_horror.mp4

# Plus Hailuo parallel for comparison:
# (similar prompts via existing scripts/video.py)
```

**Decision matrix from test**:
- Both Veo + Hailuo accept all 3 → architect can use Veo as primary for ALL shots
- Veo accepts 1-2, Hailuo accepts all 3 → use Veo selectively, Hailuo fallback
- Veo rejects most → demote to lip-sync-only, Hailuo primary

### 8.18.6 Architectural changes if Veo 3.1 becomes primary

**Pipeline simplification**:
- Skip separate TTS for character-speaking shots (Veo bundles audio)
- Skip Hedra lip-sync calls (Veo handles natively)
- Skip part of audio mix complexity (Veo audio bundled in clip)

**Workflow per Veo-character-shot**:
```bash
# Single call generates visual + audio + lip-sync
.venv/bin/python scripts/veo3.py \
  --prompt "character_<name>_anchor.png + dialog text + setting + motion" \
  --dialog "<exact spoken text>" \
  --duration <shot_duration_s> \
  --aspect 9:16 \
  --output assets/clips/shot_<id>_veo.mp4

# Then drop into per-clip atomic builder (Veo audio already bundled):
.venv/bin/python scripts/build_clip_atomic.py \
  --visual assets/clips/shot_<id>_veo.mp4 \
  --audio-source bundled \
  --shot-id shot_<id>
```

**For non-character shots (POV traversal, atmospheric)**:
- Veo OR Hailuo per § 8.18.2 decision tree
- Veo audio bundled (foley, ambient) OR Hailuo + separate ElevenLabs audio

### 8.18.7 Quotas / rate limits to monitor

Gemini Enterprise Veo 3.1 quotas unknown until production use. Monitor:
- Daily / monthly generation cap
- Concurrent generation limit
- Generation time per clip (latency)
- Re-tries on filter rejection

If quota hit → fallback Hailuo + Hedra (still $5-9/video Replicate).

### 8.18.8 Canonical validation status — UPDATED 2026-05-21 PM late post test bench

```yaml
canonical_validation_status: "validated_test_bench_2026_05_21"
validated_against:
  - "Veo 3.1 SAFE shot (POV library corridor) → PASS 78s gen, 720x1280, AAC native audio"
  - "Veo 3.1 BORDERLINE shot (uncanny figure hallway) → PASS 64s gen, native audio"
  - "Veo 3.1 HORROR shot (industrial figure helmet abandoned) → PASS 80s gen, native audio"
  - "Veo 3.1 CHARACTER SPEAKING shot (dialog) → PASS 64s gen + Whisper verified 'Elige bien, no hay vuelta atrás' matches prompt"
  - "All 4 test outputs: h264+AAC, 6.0s duration, 9:16 native 720x1280, audio bundled"
validation_methodology: "Test bench 4 prompts spanning safe/borderline/horror/dialog + ffprobe stream verification + Whisper dialog match"
validated_at: 2026-05-21
test_outputs:
  - "/tmp/veo_test_safe.mp4"
  - "/tmp/veo_bench_borderline.mp4"
  - "/tmp/veo_bench_horror.mp4"
  - "/tmp/veo_bench_speaking.mp4"
build_outputs:
  - "scripts/veo3.py production-ready (3-tier preview/fast/lite + httpx download + auth follow-redirects)"
scenarios_resolved:
  - "Scenario A — Veo accepts ALL horror content tested. Default forward."
  - "Cost video #3 forward: ~$0 if Veo for all shots OR ~$4 mixed Hailuo for gore-specific"
quotas_observed:
  - "No quota errors during 4 sequential calls"
  - "Production sequential 22 shots × ~70s = ~25 min wall-clock"
  - "Possibly parallelizable (concurrent operations not yet tested)"
findings_critical:
  - "Veo 3.1 generates VISUAL + AUDIO + LIP-SYNC native end-to-end in single call"
  - "Whisper-verified dialog match: prompt 'Elige bien, no hay vuelta atras' → Veo output speech 'El lige bien, no hay vuelta atrás'"
  - "Native AAC audio bundled in mp4 output"
  - "4K available, current test 720x1280 baseline"
phase_3_forward:
  - "Test Veo 3.1 with character_anchor image_ref (image-to-video with character)"
  - "Test concurrent parallel generations (Files API rate limit unknown)"
  - "Compare quality side-by-side Veo vs Hailuo Pro for same prompt"
  - "Test motion_bridge_intent in Veo prompts (POV walking forward continuous between shots)"
  - "Architect SPEC v10 needs `model_tier_override: veo_3_1` field per shot"
```

