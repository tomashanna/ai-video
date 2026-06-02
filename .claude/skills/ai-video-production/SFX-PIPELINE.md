# SFX-PIPELINE.md — Generación de SFX con ElevenLabs

> Motor único de sound design para cualquier video con IA. ElevenLabs Sound Effects API cubre impactos, ambients, loops (vía `loop:true` + ffmpeg expansion), instrumentos y voces. Freesound queda solo como fallback opcional avanzado.

---

## Cuándo usar este pipeline

Cualquier video con IA que necesite SFX más allá de música + narración. Específicamente:
- Footsteps, breaths, whispers
- Impactos (white flash, body fall, glass shatter)
- Drones de tensión
- Ambient continuo (wind, fire, dawn)
- Instrumentos cortos (acoustic strum, cup toast)
- Voces ambient (group laughter)

Para horror-choice-format hay un template específico en `horror-choice-format/templates/SFX-LIST-TEMPLATE.md`.

---

## Requisitos previos

- `ELEVENLABS_API_KEY` en `.env`
- `elevenlabs >= 2.40.0` en el venv (`pip install elevenlabs`)
- Carpeta `assets/sfx/` creada
- Script `scripts/sfx.py` copiado del template (ver `templates/scripts/sfx.py`)

---

## Comando base

```bash
# Single
.venv/bin/python scripts/sfx.py -t "<prompt>" -d <segundos> -i <influence> -o assets/sfx/<name>.mp3

# Loop perfecto (para ambients y footsteps)
.venv/bin/python scripts/sfx.py -t "<prompt>" -d <segundos> --loop -o assets/sfx/<name>.mp3

# Batch desde spec JSON
.venv/bin/python scripts/sfx.py --spec sfx-spec.json
```

---

## Formato `sfx-spec.json`

```json
[
  {
    "out": "assets/sfx/h3-whisper.mp3",
    "text": "creepy hushed whisper of an old man very close to the ear, breathy, no music",
    "duration": 2.0,
    "influence": 0.6
  },
  {
    "out": "assets/sfx/ambient-wind-loop.mp3",
    "text": "continuous forest night wind, dead trees creaking, perfectly looping, no music",
    "duration": 22.0,
    "influence": 0.5,
    "loop": true
  }
]
```

---

## Parámetros del endpoint

| Parámetro | Rango | Cuándo cambiarlo |
|---|---|---|
| `text` | string | Describir el SONIDO, no la causa. "low impactful sub-bass stab" mejor que "monster attack sound" |
| `duration_seconds` | 0.5 – 22 | Lo que necesitás. Para >22s ver loop expansion abajo |
| `prompt_influence` | 0 – 1 | Default `0.3`. Subir a `0.6-0.7` para impacts y drones donde el prompt debe respetarse al pie |
| `loop` | bool | `true` para ambients perfectos (fire, wind, footsteps) |
| `output_format` | `mp3_44100_128` | Coincide con TTS — facilita mezcla |

---

## Estructura de prompt que funciona

```
[TIPO DE SONIDO] + [CARACTERÍSTICA SONORA ESPECÍFICA] + [CONTEXTO] + [NEGATIVOS]
```

**Negativos típicos**: `no music`, `no melody`, `dry no reverb`, `single event`, `no echo`.

### Ejemplos validados

| Categoría | Prompt | Dur | Influence |
|---|---|---|---|
| Sub-bass impact | `low frequency cinematic sub-bass stab impact, single short hit, dry no reverb tail, no music` | 0.5 | 0.5 |
| White flash | `short cinematic white-flash impact, sharp crack with deep sub-bass tail, like a camera flash crossed with thunder, dry` | 0.7 | 0.5 |
| Footsteps loop | `slow heavy human footsteps walking on dry dead crunchy leaves, single person, steady pace, dry no reverb, no music` | 4.0 | 0.5 (loop) |
| Whisper horror | `creepy hushed unintelligible whisper of an old man very close to the ear, breathy, single short phrase, no music` | 2.0 | 0.6 |
| Tension drone | `low rising tension drone slow build sub-bass cinematic, no melody, intensifies smoothly` | 2.5 | 0.7 |
| Body fall | `human body collapsing onto dead leaves and earth, dull thud no scream, single event, no music` | 1.5 | 0.6 |
| Campfire loop | `warm intimate campfire crackling close-up, dry wood embers popping, cozy continuous ambient` | 8.0 | 0.5 (loop) |
| Acoustic guitar | `single warm acoustic guitar chord strum, open major chord, nylon strings, intimate close-up, single event no progression, no other instruments` | 2.0 | 0.6 |
| Bird call | `single distant blackbird call, one clear note, dawn morning forest, lone bird far away, no other animals, no music` | 1.5 | 0.6 |

---

## Loop expansion — ambients largos >22s

ElevenLabs limita a 22s por call. Para ambient layers de 30-90s, generar 22s con `loop:true` y expandir:

```bash
# 1. Generar el seed loopable
.venv/bin/python scripts/sfx.py \
  -t "continuous forest night wind, dead trees creaking, perfectly looping" \
  -d 22 --loop -i 0.5 \
  -o assets/sfx/ambient-wind-loop.mp3

# 2. Expandir a duración objetivo con fade-out
ffmpeg -y -stream_loop 3 -i assets/sfx/ambient-wind-loop.mp3 -t 75 \
  -af "afade=t=out:st=74:d=1" \
  assets/sfx/ambient-wind.mp3
```

`-stream_loop N` = el archivo se reproduce `N+1` veces. Calcular: `N = ceil(target / 22) - 1`.

| Target | Source 22s | -stream_loop |
|---|---|---|
| 30s | 22s | 1 (2 vueltas) |
| 45s | 22s | 2 (3 vueltas) |
| 75s | 22s | 3 (4 vueltas) |
| 90s | 22s | 4 (5 vueltas) |

Verificar con ffprobe:
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 assets/sfx/ambient-wind.mp3
```

---

## Mix volumes — tabla canónica

Aplicar a `data-volume` en cada `<audio class="clip">`:

| Capa | data-volume | Notas |
|---|---|---|
| Narración | **1.0** | Siempre. Nada compite con la voz. |
| Música ambient (horror, oscura) | 0.05–0.18 | Apenas perceptible |
| Música ambient (dawn, cálida) | 0.13–0.18 | Sin narración encima puede subir |
| SFX eventos puntuales | 0.20–0.35 | Footsteps, whispers, breaths, body falls |
| Flash impacts | 0.55–0.65 | Tienen que pegar (white flash + sub-bass) |
| Ambient continuo (wind/fire loop) | 0.10–0.18 | Capa profunda, no compite con SFX puntuales |
| Glass / cup clinks / SFX agudos | 0.25–0.35 | Audibles pero no dominantes |

**Si dos SFX se solapan**: bajar el menos importante 0.05–0.10.

---

## Costo orientativo

Un video de 80-90s con sound design completo (~25-35 SFX + 2-3 ambient loops): **~$5-10 en ElevenLabs paid tier** (~15-20k créditos).

---

## 7 SFX de CORTE — set canónico reusable cross-video

> Aparte de los SFX por escena, todo video con narrador + cambios narrativos debería tener los 7 sonidos del set de cortes. Se generan **una sola vez** y se reutilizan entre videos del workspace. Ver `NARRATIVE-LED-EDITING.md` para taxonomía completa y cuándo usar cada uno.

Ubicación recomendada: `assets/sfx/cuts/` (separado de los SFX por escena).

| Asset | Función narrativa | Prompt EL |
|---|---|---|
| `cuts/cut-white-flash.mp3` | Elección tomada (cliff fork) | "short cinematic white-flash impact, sharp crack with deep sub-bass tail, dry, single event" |
| `cuts/cut-bad-thud.mp3` | Entrada rama mala (game-over) | "low heavy heart-skip thud, body weight collapse, dark sub-bass impact, single event" |
| `cuts/cut-drone-low.mp3` | Sostener muerto / atrapado | "low continuous sub-bass drone, doom atmosphere, no melody, sustained 1 second" |
| `cuts/cut-rise-drone.mp3` | Transición rama mala → buena | "ascending sub-bass pad rising from low to mid, transition swell, tension to release" |
| `cuts/cut-exhale.mp3` | Entrada rama buena (alivio) | "soft human exhale of relief, ambient warm low pad tail, no music, single event" |
| `cuts/cut-silence-drone.mp3` | Pausa entre nominales | "very low subtle drone for dramatic silence, almost imperceptible, atmospheric, 0.3s" |
| `cuts/cut-warm-whoosh.mp3` | Transición al cliffhanger | "soft warm whoosh transition without horror, gentle wind change, single event" |

Costo del set completo: ~$0.50 (~2k créditos EL). Generado una vez, reutilizable en todos los proyectos.

Para generarlo, usar el batch JSON ejemplo en `NARRATIVE-LED-EDITING.md` § "Paso 3".

---

## Workflow recomendado

> ⛔ **Paso 0 obligatorio — REUSE FIRST, CREATE SECOND** (regla canónica 2026-05-16):
> ANTES de invocar `scripts/sfx.py` para cualquier evento sonoro:
> 1. `cat library/sfx-catalog.json | grep -i "<evento>"` (ej: "thud", "wind", "footsteps", "flash")
> 2. Revisar también `library/sfx/cuts/` (set canónico de 7 cortes reusables — ver § "7 SFX de CORTE" abajo) y `library/sfx/ambients/` (ambients ya generados).
> 3. **Si EXISTE** → reusar path indicado en catalog. NO generar.
> 4. **Si NO existe** → generar con `scripts/sfx.py`. Después agregar a `library/sfx-catalog.json` para próximos videos.
>
> **Why**: cada SFX nuevo cuesta créditos EL ($0.05-0.20) + 3-8s de wait. Library tiene 7+ cortes canónicos + ambients reusables — empezá por ahí. Caso disparador: bosque-v3 regeneró white-flash que ya estaba en `library/sfx/cuts/cut-white-flash.mp3`.

1. **Drafttear lista de SFX por escena** con timestamps reales del index.html (no estimados). En `horror-choice-format/` esto es la sección "Lista de SFX por hito (V8-2)" del `NARRATIVE.md`.
2. **Cruzar lista vs `library/sfx-catalog.json`** — marcar cuáles ya existen (reuse) y cuáles requieren generación (new). Solo los NEW pasan al sfx-spec.json.
3. **Convertir lista de NEW a `sfx-spec.json`** (formato batch).
4. **Ejecutar batch**: `.venv/bin/python scripts/sfx.py --spec sfx-spec.json` (corre en background, ~3-8s por SFX).
5. **Para ambients >22s**: ejecutar la expansión ffmpeg después del batch.
6. **Verificar duraciones** con `ffprobe` (EL entrega con ±1-2% de error, aceptable).
7. **Agregar los SFX nuevos a `library/sfx-catalog.json`** con path + descripción + prompt usado (alimenta future reuse).
8. **Conectar en `index.html`** con `data-track-index` reservado 60-110.
9. **Listening pass** con auriculares — ajustar volúmenes si algo tapa la narración.

---

## Fallback opcional: Freesound

Solo si un asset específico EL salió notoriamente uncanny y no se arregla iterando el prompt. Casos típicos:
- Voces humanas grupales muy adelante en la mezcla (uncanny valley)
- Instrumentos acústicos prominentes en foreground

Workflow: copiar `horror-choice-format/templates/FREESOUND-QUERIES-TEMPLATE.md`, hacer queries, descargar manualmente, anotar CC-BY en `CREDITS.md`.

**Para producción estándar, NO usar Freesound** — agrega 15-20 min manuales por video sin diferencia perceptible en mezcla.

---

## ElevenLabs MCP (opcional — uso ad-hoc)

El MCP oficial está instalado a scope user (`uvx elevenlabs-mcp`). Útil para generar 1 SFX en conversación sin entrar a CLI.

**Para producción batch siempre usar `scripts/sfx.py`** — es reproducible, versionable, y no depende de la disponibilidad del MCP.

---

## Ducking, EQ y density rules — validado contra referentes (2026-05-13)

> El mix de @referent-a se siente "limpio" porque tiene ducking automático + EQ separation + 100% sound fabric. Estas son las 3 reglas obligatorias.

### Ducking — atenuar capas cuando narración activa

La música y el ambient deben **bajar de volumen** cuando hay narración, y **recuperar** cuando termina. Esto es ducking.

**Reglas:**
| Capa | Volumen normal | Duck cuando hay narración | Restore time |
|------|----------------|---------------------------|---------------|
| Música atmosférica | 0.18 | **0.06** (duck -12 dB equiv) | 200ms ramp |
| Ambient continuo (wind/fire) | 0.15 | **0.08** (duck -6 dB equiv) | 200ms ramp |
| SFX impacto (one-shot) | 0.55-0.65 | **NO duck** — el impacto compite a propósito | n/a |
| Tick countdown | 0.20 | **NO duck** — ya es bajo | n/a |

**GSAP implementation:**

```javascript
// Función helper de ducking
function duckOnNarration(narrAudioEl, musicAudioEl, ambientAudioEl, narrStart, narrEnd) {
  const NARR_FADE = 0.2; // 200ms ramp

  // Music duck
  tl.to(musicAudioEl, { volume: 0.06, duration: NARR_FADE }, narrStart);
  tl.to(musicAudioEl, { volume: 0.18, duration: NARR_FADE }, narrEnd);

  // Ambient duck
  tl.to(ambientAudioEl, { volume: 0.08, duration: NARR_FADE }, narrStart);
  tl.to(ambientAudioEl, { volume: 0.15, duration: NARR_FADE }, narrEnd);
}

// Aplicar por cada bloque de narración
duckOnNarration(narrEl, musicEl, ambientEl, 5.0, 12.0);
duckOnNarration(narrEl, musicEl, ambientEl, 17.0, 25.0);
// ...
```

**Excepción:** SFX impacto puede romper ducking (es intencional el "punch"). Ejemplo: white-flash a 30s mantiene volumen 0.6 aunque haya narración. La narración natural se atenúa por debajo del impacto.

### EQ separation — frecuencias por capa

Para evitar mud (frecuencias compitiendo), filtrar cada capa antes del mix:

**Narración:**
- High-pass 80 Hz (remove rumble bajo)
- Presence boost +2 dB @ 3-5 kHz (claridad voz)
- Optional de-ess @ 6-8 kHz si TTS suena sibilante

```bash
# Aplicar a un asset de narración:
ffmpeg -i assets/h1-narr.mp3 \
  -af "highpass=f=80,equalizer=f=4000:width_type=h:width=2000:g=2" \
  assets/h1-narr-eq.mp3
```

**Música atmosférica:**
- Low-pass 8 kHz cuando coincide con narración (deja espacio en agudos para la voz)
- Mid scoop -3 dB @ 1-3 kHz (no compite con voz)

```bash
ffmpeg -i assets/music.mp3 \
  -af "lowpass=f=8000,equalizer=f=2000:width_type=h:width=1500:g=-3" \
  assets/music-eq.mp3
```

**Ambient continuo (wind, fire):**
- High-pass 60 Hz (remove sub-rumble si lo hay)
- Notch -4 dB @ 2 kHz si compite con voz

**SFX impacto:**
- NO EQ (queremos toda la frecuencia para el "punch")

### Density rules — sound fabric 100%

7/7 referentes tienen sound fabric ≥99% (sin dead zones de silencio mid-video).

**Reglas:**
1. **Ambient continuo siempre presente** — desde 0s hasta el outro fade. Es la base layer.
2. **Música atmosférica** — al menos durante 70-85% del video. Puede entrar en setup (5-10s) y salir en outro.
3. **SFX impacto cada 10-20s** — mantiene atención. Sin SFX = "el video se queda quieto auditivamente".
4. **Narración cobertura ≥70%** — validado contra exitosos (mina 77%, bosque 70.3%, elige 72.9%).
5. **Avg block duration ≥4.5s** — narración fluida, no entrecortada. Validado (mina 6.07s, bosque 5.24s, elige 4.73s, pueblo fallido 2.34s ❌).
6. **Cero dead zones >1s** — siempre hay algo sonando (ambient mínimo).
7. **Silencio único permitido:** los últimos ~1s antes del end (fade out outro).

### Implementación HTML/GSAP

```html
<!-- Layer base — ambient continuo desde 0s hasta end-1s -->
<audio class="clip" src="assets/sfx/ambient-wind.mp3"
       data-track-index="60" data-start="0" data-volume="0.15"></audio>

<!-- Layer media — música atmosférica desde 5s hasta 85s -->
<audio class="clip" src="assets/sfx/music-tense.mp3"
       data-track-index="55" data-start="5" data-volume="0.18"></audio>

<!-- Narración — cuando aplica -->
<audio class="clip" src="assets/h1-narr-eq.mp3"
       data-track-index="40" data-start="1" data-volume="1.0"></audio>

<!-- SFX impactos puntuales cada 10-20s -->
<audio class="clip" src="assets/sfx/whisper.mp3"
       data-track-index="70" data-start="12" data-volume="0.30"></audio>
<audio class="clip" src="assets/sfx/white-flash.mp3"
       data-track-index="71" data-start="28" data-volume="0.60"></audio>
<!-- ... -->
```

### Anti-patterns

❌ **Música a volumen plano sin ducking:** la narración compite con la música → viewer percibe "no se entiende qué dice". Universal en horror narrativo: la música DEBE duckear.

❌ **Ambient continuo cortado mid-video:** el silencio repentino interrumpe inmersión. Mantener layer base activa todo el video (excepto últimos 1s).

❌ **SFX impacto al volumen de la narración:** se pierden. Subir a 0.55-0.65 (audibles sobre todo lo demás).

❌ **EQ de narración con muddy lows:** sin high-pass 80 Hz, los TTS tienen rumble bajo que compite con sub-bass de música/SFX → mix turbio.

❌ **Density gaps con dead zones >1s:** validado contra pueblo-fantasma-desierto v2 — tenía 40s de outro mudo, audit-audio lo detectó, viewer percibió "video se cortó".

---

## Validación con audit-audio.py

El script `scripts/audit-audio.py` valida automáticamente:
- Narration coverage ≥70% ✓
- Avg block duration ≥4.5s ✓
- Sound fabric coverage ≥99% ✓
- LUFS integrated -14 ±0.5 dB ✓

Si falla cualquier check → ajustar mix → re-render → re-audit.
