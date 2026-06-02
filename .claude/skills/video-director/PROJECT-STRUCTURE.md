# PROJECT-STRUCTURE.md — Esqueleto canónico de cada video

> Cada video vive en una carpeta propia. Este doc define qué archivos debe tener, de dónde vienen, y cómo se generan. Sin esto, cada proyecto reinventa su estructura.

---

## Estructura mínima de un proyecto

```
<proyecto>/
├── CLAUDE.md                    ← Governance (Plan-First, Phase rules)
├── DESIGN.md                    ← Colores, tipografía, safe zones
├── NARRATIVE.md                 ← Script + asset list
├── creative-brief-v1.md         ← Brief llenado (slot-based)
├── V6-VS-V7.md                  ← Historial de iteraciones (renombrar por proyecto)
├── AGENTS.md                    ← Convenciones del proyecto
├── hyperframes.json             ← Config HyperFrames
├── meta.json                    ← Metadata HyperFrames
├── index.html                   ← Composición principal
├── .env                         ← API keys (NO commitear)
├── .venv/                       ← Python virtual env
├── assets/                      ← TTS + imágenes + SFX generados
│   ├── *.png                    ← Imágenes (con variantes -a/-b/-c)
│   ├── *-raw.mp3                ← TTS raw (descartar)
│   ├── *-2x.mp3                 ← TTS procesado (usar)
│   ├── music-*.mp3              ← Música procesada
│   └── sfx/                     ← SFX por escena
│       └── cuts/                ← SFX de cortes NARRATIVE-LED (copy de library/)
├── scripts/                     ← Copy de <formato>/templates/scripts/
│   ├── tts.py
│   ├── image.py
│   ├── sfx.py
│   └── captions.py
├── renders/                     ← Output MP4
│   ├── draft.mp4
│   ├── v1-final.mp4
│   ├── v2-final.mp4
│   └── final.mp4
├── performance/                 ← Capturas T+48h por video
│   └── YYYY-MM-DD-<slug>.md     ← Copy de video-director/templates/video-performance-template.md
├── captions-spec.json           ← Spec batch Whisper
├── sfx-spec.json                ← Spec batch SFX (referenciar library/ donde aplique)
└── compositions/                ← Sub-composiciones opcionales
    ├── captions.html
    └── overlays.html
```

---

## Tabla detallada — qué archivo, de dónde, cuándo se genera

### Archivos de governance

| Archivo | Origen | Generación | Frequency |
|---|---|---|---|
| `CLAUDE.md` | Copy de proyecto previo del mismo formato | Editar Phase actual + ajustes mínimos | Por proyecto |
| `DESIGN.md` | Copy de proyecto previo | Editar colores específicos si varían | Por proyecto |
| `AGENTS.md` | Copy de proyecto previo | Replica | Por proyecto |
| `V<n>-VS-V<m>.md` | Vacío | Se llena cada iteración del render | Por proyecto |

### Archivos de contenido

| Archivo | Origen | Generación |
|---|---|---|
| `NARRATIVE.md` | `<formato>/templates/NARRATIVE-TEMPLATE.md` | Llenar con script único + asset list |
| `creative-brief-v1.md` | Plantilla en `<formato>/PAUTA-MASTER.md` (Slots A-H) | Llenar TODOS los slots ANTES de generar assets |

### Archivos de config HyperFrames

| Archivo | Origen | Generación |
|---|---|---|
| `hyperframes.json` | `<formato>/templates/hyperframes.json-TEMPLATE` | Ajustar duraciones / IDs si varían |
| `meta.json` | `npx hyperframes init` | Auto-generado |
| `index.html` | `<formato>/VIDEO-PLAYBOOK.md` templates por hito | Construir hito por hito |

### Carpetas de assets

| Carpeta | Contenido | Generación |
|---|---|---|
| `assets/*.png` | Imágenes del video | `scripts/image.py` + variantes -a/-b/-c |
| `assets/*-2x.mp3` | Narraciones TTS procesadas | `scripts/tts.py` + atempo cap ≥0.90 con ffmpeg (NO slow-down de voz — ver INGENIERO §1.6) |
| `assets/music-*.mp3` | Música procesada | Copy de `library/music/` o procesar de raw |
| `assets/sfx/*.mp3` | SFX específicos del video | Copy de `library/sfx/` o `scripts/sfx.py` |
| `assets/sfx/cuts/*.mp3` | 7 cortes universales NARRATIVE-LED | **Siempre copy de `library/sfx/cuts/`** |

### Archivos de spec (machine-readable)

| Archivo | Contenido |
|---|---|
| `captions-spec.json` | Lista de audios + offsets + element IDs para Whisper batch |
| `sfx-spec.json` | Lista de SFX a generar (solo los que NO existan en library) |

### Carpetas operativas

| Carpeta | Contenido |
|---|---|
| `scripts/` | Copy de `<formato>/templates/scripts/` (incluye STYLE_SUFFIX hardcoded) |
| `renders/` | MP4s de draft + iteraciones + final |
| `performance/` | Capturas T+48h |
| `compositions/` | Sub-composiciones opcionales (data-composition-src) |

---

## Orden de creación de un proyecto nuevo

> Si seguís este orden, no te trabás. Saltearse pasos siempre cuesta más al final.

### Paso 1 — Pre-requisitos (5 min)

- Carpeta del proyecto: `mkdir <proyecto> && cd <proyecto>`
- `.venv` + `pip install elevenlabs python-dotenv openai-whisper`
- Copy `.env` del proyecto previo (mismas API keys: ELEVENLABS_API_KEY, GEMINI_API_KEY, REPLICATE_API_TOKEN)

### Paso 2 — Governance + design (10 min)

```bash
# Copy de proyecto previo del mismo formato
cp ../<proyecto-previo>/CLAUDE.md .
cp ../<proyecto-previo>/DESIGN.md .
cp ../<proyecto-previo>/AGENTS.md .
```

Editar `CLAUDE.md`: ajustar Phase actual si cambió. Mantener Plan-First rule + Source-of-Truth rule.

### Paso 3 — Scripts del formato (1 min)

```bash
cp -r ../.claude/skills/<formato>-format/templates/scripts ./scripts
```

Verificar que `scripts/tts.py` tiene el voice ID correcto en `DEFAULT_VOICE_ID`.

### Paso 4 — Creative brief (20 min)

```bash
# Tomar la plantilla de PAUTA-MASTER.md (Slots A-H)
# Crear creative-brief-v1.md llenando TODOS los slots
```

**Antes de cualquier API call**: pasar checklist de calidad de `<formato>/PAUTA-MASTER.md` § 16.

### Paso 5 — Script narrativo (30 min)

```bash
cp ../.claude/skills/<formato>-format/templates/NARRATIVE-TEMPLATE.md ./NARRATIVE.md
# Llenar con el script único + asset plan (variantes -a/-b/-c)
```

### Paso 6 — Asset generation (1.5-2h) — ORDEN OBLIGATORIO

#### 6.A — Anchors de personajes PRIMERO (sin --ref)

> Para cada personaje del video, generar un anchor canónico ANTES de cualquier escena. Sin anchor = inconsistencia visual garantizada. Ver `ai-video-production/CHARACTER-CONSISTENCY.md`.

```bash
# Para cada personaje (malo aparente, bueno aparente, narrador POV si aplica):
.venv/bin/python scripts/image.py \
  -p "Medium close-up portrait of [PERSONAJE]. Facing camera, neutral expression, soft frontal lighting, blurred background. Photorealistic 35mm." \
  -o assets/<personaje>-anchor.png
```

Verificar visualmente cada anchor. Si no convence → regenerar AHORA, antes de continuar con escenas.

#### 6.B — TTS por bloque de narración

```bash
.venv/bin/python scripts/tts.py -t "<texto>" -v <voice-id> -o assets/narr-N-raw.mp3
# Pipeline real: cap atempo ≥0.90 (NUNCA slow-down de voz). atempo=2.0 está DEPRECATED — ver INGENIERO-PAUTA-MASTER §1.6
ffmpeg -y -i assets/narr-N-raw.mp3 -filter:a "atempo=0.95" assets/narr-N-2x.mp3
```

#### 6.C — Escenas CON personajes (usando anchors como --ref)

> Cada escena con un personaje pasa el anchor como `--ref`. Variantes -a/-b/-c se generan también con --ref (mantienen consistencia visual a través de los tipos de plano).

```bash
# Escena de un personaje
.venv/bin/python scripts/image.py \
  -p "The character from the reference walking through dark forest. Wide shot. Same face." \
  --ref assets/berni-anchor.png \
  -o assets/h3-walk-a.png

# Escena con dos personajes (pasar ambos anchors)
.venv/bin/python scripts/image.py \
  -p "Both characters facing camera, dim candlelight." \
  --ref assets/berni-anchor.png \
  --ref assets/yonaiker-anchor.png \
  -o assets/h1-both.png
```

Generación en paralelo si las escenas son independientes:
```bash
.venv/bin/python scripts/image.py -p "..." --ref assets/<a>-anchor.png -o assets/h3-a.png &
.venv/bin/python scripts/image.py -p "..." --ref assets/<a>-anchor.png -o assets/h3-b.png &
wait
```

#### 6.D — Escenas SIN personajes (paisajes, objetos)

```bash
# Sin --ref porque no hay personaje a mantener consistente
.venv/bin/python scripts/image.py -p "Empty dark forest path at midnight, mist." -o assets/h5-road.png
```

#### 6.E — SFX

```bash
# Primero buscar en library/
cp ~/AI\ video\ 1/library/sfx/cuts/*.mp3 ./assets/sfx/cuts/
cp ~/AI\ video\ 1/library/sfx/impacts/flash-sharp.mp3 ./assets/sfx/

# Solo generar lo que falte:
.venv/bin/python scripts/sfx.py --spec sfx-spec.json
```

### Paso 7 — Composición HTML (45-90 min)

#### 7.A — PICK COMPONENTS (antes de tocar index.html)

```bash
# 1. Ver qué usó el video anterior (para excluir)
cat ~/AI\ video\ 1/.claude/skills/<formato>-format/video-log.md | head -25

# 2. Ver catálogo completo
cat ~/AI\ video\ 1/elements.json
```

#### 7.B — COMPATIBILITY CHECK (3 chequeos obligatorios)

##### Check 1: Consistencia INTRA-video
- El countdown elegido se usa en TODOS los countdowns del video (H2, H3, H4 todos iguales).
- El loader elegido se usa en TODOS los loaders del video.
- NUNCA mezclar countdown-glitch en H2 con countdown-slam en H3.

##### Check 2: Timing (no overlap)
```
countdown (3-3.5s) → flash → loader (3-3.5s) → flash → resultado
```
Son SECUENCIALES. Verificar que el `data-start` del loader = `data-start` del countdown + duración del countdown.

##### Check 3: Estética (matriz de compatibilidad)

| Countdown × Loader | bar | radial | segments |
|---|---|---|---|
| **pulse** | ✅ Perfecto | ✅ Bueno | ⚠️ Choca |
| **glitch** | ⚠️ Choca | ✅ Bueno | ✅ Perfecto |
| **slam** | ✅ Bueno | ⚠️ Choca | ✅ Perfecto |

**Combos top-tier**: pulse+bar, glitch+segments, slam+segments.
**Combos a evitar**: pulse+segments, glitch+bar, slam+radial.

#### 7.C — Wire en index.html

Editar `index.html` siguiendo `<formato>/VIDEO-PLAYBOOK.md`. Aplicar:
- 10 hard rules de `video-director/SKILL.md`
- Motion layer de `ai-video-production/MOTION-LAYER.md`
- 7 cortes de `ai-video-production/NARRATIVE-LED-EDITING.md`
- Safe zone IG: `caption-wrap bottom:540`, `loading-bar-wrap bottom:700`
- Element library: wire los componentes elegidos via `data-composition-src` (NO hardcodear)
- **Mismo countdown y mismo loader en TODOS los dilemas del video** (intra-video consistency)

Doc completo del sistema: `ai-video-production/ELEMENTS-LIBRARY.md`.

### Paso 8 — Captions Whisper (5 min)

```bash
# Crear captions-spec.json con audios + offsets + element IDs
# Ver ai-video-production/CAPTIONS.md § Batch mode

.venv/bin/python scripts/captions.py --spec captions-spec.json > captions-output.txt
# Revisar nombres propios manualmente (Whisper falla con nombres raros)
# Copiar al script del HTML
```

### Paso 9 — Checkpoints (5 min)

```bash
npx hyperframes lint
npx hyperframes preview  # visual check rápido
```

### Paso 10 — Render draft (8-15 min)

```bash
npx hyperframes render -c index.html -o renders/v1-draft.mp4
```

### Paso 11 — Gemini QA (3 min)

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/v1-draft.mp4 \
  --prompt "$(cat /path/to/qa-prompt.txt)"
```

### Paso 12 — Iterar hasta ≥9.7 (variable)

Por cada iteración:
- Aplicar 2-3 fixes priorizados
- Re-render
- Re-QA
- Actualizar `V<n>-VS-V<m>.md`

### Paso 13 — Render final + V6-VS-V7

```bash
npx hyperframes render -c index.html -o renders/final.mp4 --quality high
# Actualizar V6-VS-V7.md con scores finales
```

### Paso 14 — Publicar

Usuario decide. NO el editor IA.

### Paso 15 — Capturar performance (T+48h)

```bash
cp ~/AI\ video\ 1/.claude/skills/video-director/templates/video-performance-template.md \
   performance/$(date +%Y-%m-%d)-<slug>.md
# Llenar métricas a T+48h
```

### Paso 16 — Update video-log del formato

Agregar fila a `<formato>-format/video-log.md` con:
- Número del video
- Fecha
- Nombre
- Archetype / tema usado
- Score Gemini
- Notas

---

## Checklist mínimo antes de declarar "proyecto listo"

Para que un proyecto se considere completo:

- [ ] `CLAUDE.md`, `DESIGN.md`, `AGENTS.md` presentes
- [ ] `NARRATIVE.md` lleno con script + asset list
- [ ] `creative-brief-v1.md` lleno con los slots (si formato lo requiere)
- [ ] `index.html` con todas las hard rules aplicadas
- [ ] Componentes `countdown` / `loader` / `lower-third` pickeados via `elements.json` (NO hardcoded). Distintos al video anterior del mismo formato.
- [ ] `assets/` con TTS, imágenes (con variantes), SFX
- [ ] Captions vía Whisper (NO hand-timed)
- [ ] Mix volumes canónicos aplicados
- [ ] Motion mínimo Ken Burns en cada plano >2s
- [ ] 7 cortes NARRATIVE-LED aplicados donde corresponda
- [ ] Lint sin errores
- [ ] Gemini QA ≥9.7
- [ ] Specs IG verificados (h264, aac, 30fps, 1080×1920, ≤650MB)
- [ ] `V<n>-VS-V<m>.md` actualizado
- [ ] Render final en quality high
- [ ] (Después de publicar) `performance/<fecha>.md` lleno a T+48h
- [ ] `<formato>/video-log.md` actualizado

---

## Anti-patterns por-proyecto

- ❌ **Cambiar la estructura.** Si necesitás algo nuevo, agregalo a `<formato>-format/` (template), no al proyecto suelto.
- ❌ **Modificar scripts/ del proyecto.** Si encontrás un bug, fix en `<formato>/templates/scripts/` y re-copy.
- ❌ **Saltearse el creative-brief.** En formatos narrativos, sin brief el video falla en calidad estructural.
- ❌ **Generar SFX que ya están en library/.** Buscar primero.
- ❌ **Captions hand-timed.** Whisper siempre, corregir nombres propios manualmente.
- ❌ **Borrar `assets/`.** Si renombrás un video, mové la carpeta entera. Los assets generados costaron créditos.

---

## Cuándo crear sub-composiciones (`compositions/`)

Crear sub-composiciones (data-composition-src) cuando:
- Un overlay se reusa en múltiples momentos del video
- Captions tienen estilo muy complejo que vale aislar
- Hay layers que se mantienen entre escenas (vignette pulsante, niebla)

Ejemplo de elige-companero: `compositions/captions.html` con border-rojo Vignelli.

NO crear si:
- El elemento aparece una sola vez
- El elemento tiene <20 líneas de HTML/CSS
