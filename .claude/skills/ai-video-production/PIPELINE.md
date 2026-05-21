# PIPELINE.md — Pipeline técnico general de video con IA

> Comandos, voice IDs, patrones GSAP base, render, música, asset naming, HyperFrames gotchas. Independiente del formato. Para motion avanzado ver `MOTION-LAYER.md`; para SFX ver `SFX-PIPELINE.md`; para variantes de imagen ver `IMAGE-VARIETY.md`.

---

## 1. TTS — narración con ElevenLabs

### Comando base

```bash
.venv/bin/python scripts/tts.py \
  -t "Texto a narrar." \
  -v <VOICE_ID> \
  -o assets/nombre-raw.mp3
```

### Voice IDs validados

| Voz | ID | Característica |
|-----|-----|----------------|
| Horror narrador grave | `Tj9l48J9AJbry5yCP5eW` | Tono lento, susurro |
| Voz A/B test | `2gPFXx8pN3Avh27Dw5Ma` | Usado en bosque-abandonado v3 |
| Reservada | `1BfrkuYXmEwp8AWqSLWk` | Sin testear |

Cada formato puede definir su voz canónica. **Verificar `DEFAULT_VOICE_ID` en `scripts/tts.py` antes de cada video nuevo.**

### Post-procesado obligatorio — atempo 2x

Las voces lentas por naturaleza (como `Tj9l48J9AJbry5yCP5eW`) requieren acelerar a 2x:

```bash
ffmpeg -y -i assets/nombre-raw.mp3 \
  -filter:a "atempo=2.0" \
  assets/nombre-2x.mp3
```

Medir duración después:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/nombre-2x.mp3
```

**Regla:** nunca usar el raw en el render. Siempre el `-2x.mp3` o el procesado equivalente. La voz cruda suena a IA.

---

## 2. IMÁGENES — generación con Gemini Nano Banana

### Comando base

```bash
.venv/bin/python scripts/image.py \
  -p "prompt aquí" \
  -o assets/nombre.png
```

### STYLE_SUFFIX por formato

Cada formato puede definir su suffix de estilo. Por ejemplo, en horror-choice-format el script tiene `HORROR_SUFFIX` hardcoded:

```python
HORROR_SUFFIX = (
    " Dark cinematic horror aesthetic, desaturated color grade with warm amber "
    "and orange highlights only, liminal space mood, eerie atmospheric lighting, "
    "Midjourney v6 photorealistic style, uncanny valley, subtle film grain, "
    "low-key lighting, dead-center composition, 35mm lens, shallow depth of field. "
    "No text, no logos, no watermarks."
)
```

**Para un formato nuevo:** copiar `image.py` del template y reemplazar `HORROR_SUFFIX` por tu propio `STYLE_SUFFIX`.

Flag `--no-mono-suffix` desactiva el suffix (útil para escenas en colores naturales).

### ⭐ Meta-regla universal: cada formato define su preset CSS filter canónico

**Scope**: 🌐 **Universal** — aplica a CUALQUIER genre/delivery combination.

Además del `STYLE_SUFFIX` (que afecta la generación de imágenes), todo genre o delivery format DEBE definir su **preset CSS filter canónico** en su `BRAND.md` (o equivalente). Este filter se aplica a TODOS los `.scene-image` del video para garantizar consistencia visual entre proyectos del mismo genre/marca.

```css
.scene-image {
  filter: contrast(X) saturate(Y) brightness(Z);
}
```

Presets canónicos:

| Genre / Format | Preset CSS filter | Look |
|---|---|---|
| **horror-choice** (validado v15) | `contrast(1.28) saturate(0.35) brightness(0.74)` | Lúgubre desaturado, integra IA-images claros (Santi) al ambiente oscuro |
| **B2B / corporate** (planeado) | `contrast(1.05) saturate(0.95) brightness(1.0)` | Naturalista limpio |
| **documental** (planeado) | `contrast(1.10) saturate(0.90) brightness(0.98)` | Naturalista cinematográfico sutil |
| **comedy / vibrant** (planeado) | `contrast(1.15) saturate(1.20) brightness(1.05)` | Saturado, alegre, alto contraste |
| **horror-deep** (alt) | `contrast(1.35) saturate(0.25) brightness(0.65)` | Sub-genre claustrofóbico |

**Por qué importa**: sin preset canónico, cada video del mismo genre se ve "ligeramente diferente" → audiencia recurrente no reconoce identidad visual. Cliente B2B detecta inconsistencias entre videos de la misma campaña.

**Workflow en proyecto nuevo**:
1. Confirmar `genre` + `delivery_format` en bootstrap
2. Buscar preset canónico en `<genre>-format/BRAND.md`
3. Si NO existe → definir preset y documentarlo en `BRAND.md` del nuevo genre
4. Aplicar en CSS `.scene-image` del `index.html`
5. Validar con 3 frames de escenas distintas — ¿se ve consistente?

**Override por escena**: aceptable cuando la narrativa lo justifica (ej: horror-choice H6 cliffhanger usa `filter: none` para activar warm tint cálido vs lúgubre).

**Anti-patterns**:
- ❌ Filter ad-hoc por proyecto sin documentar → próximo video diverge
- ❌ Filter excesivamente fuerte (contrast >1.5, saturate <0.2) → imágenes "muertas"
- ❌ Sin filter → IA-images crudas se ven "fake" / "AI-generated"

### Estructura de prompt que funciona

```
[PUNTO DE VISTA] + [SUJETO PRINCIPAL] + [ACCIÓN/ESTADO] + [AMBIENTE] + [ÁNGULO DE CÁMARA]
```

Ejemplo:
> "First-person POV seated at a long wooden table in a dark farmhouse dining room. A plate of roasted meat in front. Four figures with insect heads sit eating silently. Candles on the table, cold shadows, stone walls. Wide shot, slightly low angle."

### Lo que Gemini rechaza (aprendido en producción horror)

| ❌ Bloqueado | ✅ Alternativa segura |
|-------------|----------------------|
| "blood", "sangre" | "dark fluid", "dark stain" |
| "slashing motion toward camera" | "arm raised in static position" |
| "razor-sharp serrated edge" | "sharp chitinous foreleg" |
| Gore explícito con descripción de herida | Body horror descriptivo sin fluidos |

**Regla general:** describir el resultado visual, no la acción violenta. Cualquier formato que toque temas sensibles debe seguir este pattern.

### Variantes de imagen

Para escenas >4s necesitás variantes -a/-b/-c. Ver `IMAGE-VARIETY.md` para reglas y comandos paralelos.

---

## 3. GSAP — patrones base (motion avanzado en `MOTION-LAYER.md`)

### Regla crítica: ancla en t=0 para evitar pre-render flash

Todo elemento que empiece invisible DEBE tener esta ancla:

```js
// ✅ CORRECTO
tl.set("#mi-imagen", { opacity: 0, scale: 1.0 }, 0);  // ancla t=0
tl.set("#mi-imagen", { opacity: 1 }, 36.6);             // reveal
tl.to( "#mi-imagen", { scale: 1.04, duration: 8, ease: "sine.inOut" }, 36.6); // Ken Burns
tl.set("#mi-imagen", { opacity: 0 }, 44.3);             // hide

// ❌ INCORRECTO — produce flash al inicio
tl.set("#mi-imagen", { opacity: 1 }, 36.6);
```

### White flash en cortes secos

```js
tl.set("#flash-white", { opacity: 0.9 }, T);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, T + 0.001);
```

Nunca usar `fromTo` para el flash — mismo bug que el ancla.

Para evitar que el flash reaparezca al hacer seek en el video, agregar hard-kill después:
```js
tl.set("#flash-white", { opacity: 0 }, T + 0.2);  // hard-kill obligatorio
```

### Ken Burns base (zoom sutil — el piso de motion)

```js
tl.to("#mi-imagen", { scale: 1.04, duration: DURATION, ease: "sine.inOut" }, T_START);
```

- Scale máximo: **1.04** (más hace que se vea barato)
- Ease: `sine.inOut` siempre
- Aplicar en TODO plano estático >2s

Para motion avanzado (parallax, flicker, vignette pulsante, glitch, glow, niebla) ver `MOTION-LAYER.md`.

---

## 4. CAPTIONS — CSS obligatorio

El default `white-space: nowrap` rompe captions largos. Siempre:

```css
.caption {
  font-size: 80px;
  white-space: normal;
  width: 960px;
  text-align: center;
  line-height: 1.15;
  -webkit-text-stroke: 1.5px rgba(0,0,0,0.7);  /* obligatorio: stroke negro */
}
```

Para frases >8 palabras, reducir font-size a 68px inline:
```html
<div class="caption caption-abs" style="font-size:68px; line-height:1.1;">FRASE LARGA EN MAYÚSCULAS.</div>
```

Generación automática de timings con Whisper: ver `CAPTIONS.md`.

---

## 5. RENDER — HyperFrames

### Pre-render gates obligatorios (sesión 2026-05-10)

**Antes de cada render, correr 3 gates:**

```bash
# 1. Lint (schema/syntax)
npx hyperframes lint

# 2. Audit narrativo (visibilidad <1s, z-index conflicts, data-duration mismatch)
.venv/bin/python scripts/audit-narrative.py

# 3. Render lock (coordinación entre agentes — evita FFmpeg SIGTERM por CPU contention)
.venv/bin/python scripts/render-lock.py acquire <project-name>
# si falla, esperá:
.venv/bin/python scripts/render-lock.py wait <project-name> --timeout 1800
```

Detalle: `AUDIT.md` y sección 11 (multi-agent coordination) abajo. Los scripts viven en `templates/scripts/` — copiar a `scripts/` del proyecto.

### Comando base

```bash
npx hyperframes render . \
  --output renders/draft.mp4 \
  --fps 30 \
  --quality draft
# liberar el lock al terminar:
.venv/bin/python scripts/render-lock.py release
```

`hyperframes render .` (directorio) — NO `hyperframes render index.html` (falla).

### Calidad

| Flag | Uso | Tiempo (~80s video) |
|---|---|---|
| `--quality draft` | Revisión rápida | ~8-15 min |
| `--quality high` | Entrega final | ~30-45 min |

### Problemas conocidos

| Problema | Causa | Solución |
|---|---|---|
| `Target closed` (exit 1) | Chrome crash por memoria | Reintentar — transient |
| 404 en imágenes | Path mal en `src=` | Verificar archivo existe |
| Audio silencioso | `<audio>` sin `id` | Agregar `id` único |
| Elemento visible desde t=0 | Falta ancla GSAP | `tl.set(el, {opacity:0}, 0)` |
| Flash visible al inicio | `fromTo` para estado inicial | Reemplazar con `set + to` |
| Flash reaparece al seek | Falta hard-kill después del flash | Añadir `tl.set(flash, {opacity:0}, T+0.2)` |

### Specs de salida

Confirmar con ffprobe:
```bash
ffprobe -v quiet -print_format json -show_streams renders/final.mp4 | \
  python3 -c "import json,sys; [print(s['codec_name'], s.get('r_frame_rate',''), s.get('sample_rate','')) for s in json.load(sys.stdin)['streams']]"
```

Debe mostrar: `h264 30/1` y `aac 48000`. Tamaño < 650 MB para Instagram Reels.

---

## 6. MÚSICA — procesar en 2 pasos (regla crítica)

### ❌ NUNCA hacer esto (produce silencio)

```bash
ffmpeg -y -ss 17 -i music-raw.mp3 -t 5.2 -af "afade=t=in:st=0:d=0.2" music.mp3
# -ss antes de -i + -af = silencio total
```

### ✅ Siempre en DOS pasos

```bash
# Paso 1: extraer el clip
ffmpeg -y -i music-raw.mp3 -ss 17 -t 5.2 music-clip.mp3

# Paso 2: aplicar fades por separado
ffmpeg -y -i music-clip.mp3 \
  -af "afade=t=in:st=0:d=0.2,afade=t=out:st=5.0:d=0.2" \
  music-final.mp3
```

### Loops largos

```bash
ffmpeg -y -stream_loop 1 -i music-raw.mp3 -t 63.1 \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=62.1:d=1.0" \
  music-horror.mp3
# -stream_loop 1 = reproduce 2 veces
# NO usar -ss con -stream_loop
```

### Verificar que tiene audio

```bash
ffmpeg -i music.mp3 -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"
# Si dice "-inf LUFS" → archivo silencioso, reprocesar
# Si dice "-7 LUFS" o similar → OK
```

### Volúmenes recomendados (de mix table)

- Música ambient horror: `data-volume="0.05-0.18"` (apenas perceptible)
- Música cliffhanger / dawn: `data-volume="0.13-0.18"` (sin narración encima)

---

## 7. NOMENCLATURA + TRACK-INDEX

### Patrón de archivos

```
assets/
  scene.png                    → imagen principal
  scene-{a,b,c}.png            → variantes para escenas >4s (V8-1)
  narr{N}-raw.mp3              → TTS sin procesar (descartar)
  narr{N}-2x.mp3               → TTS procesado (usar en render)
  music-{name}-raw.mp3         → música descargada
  music-{name}.mp3             → música procesada (trim + fades)
  sfx/
    <scene>-<descriptor>.mp3   → SFX por escena
    ambient-{name}.mp3         → capas ambient continuas
```

### `data-track-index` reservado

| Rango | Uso |
|---|---|
| 0–19 | Imágenes (scene-image y capas parallax) |
| 20–39 | Captions y elementos de texto |
| 40–59 | Narración + música + ticks |
| **60–110** | **SFX dedicados — reservado** |
| 111+ | Misceláneos (overlays, flashes, fade) |

Cada `<audio class="clip">` o `<img class="scene-image clip">` necesita un track-index único o HyperFrames falla.

---

## 8. SYMLINKS — gotchas críticos

### Pattern A: folder completo (elige-companero style)

HTML referencia `assets/...` pero archivos viven en `assets v1/`:

```bash
cd <project>/
ln -sf "assets v1" assets
```

Sin este symlink: render con `media_missing_src` para todos los videos/audios.

### Pattern B: variantes de imagen (V8-1 backward-compat)

Si renombrás `nombre.png → nombre-a.png` para soportar variantes:

```bash
cd assets/
ln -sf nombre-a.png nombre.png
```

Mantiene composiciones previas funcionando.

---

## 9. KLING — animación de imágenes estáticas (opcional)

> Esta sección es referencia rápida del comando + prompts validados. Para el playbook completo (duration matching, tier 5s vs 10s, loop strategy, integración `<video>`, sincronización con narrador, costo + retries, anti-patterns) ver **`ANIMATION-LAYER.md`** ⭐

### Comando base

```bash
.venv/bin/python scripts/video.py \
  -i assets/imagen.png \
  -p "motion prompt aquí" \
  -o assets/nombre.mp4 \
  --duration 5
```

Modelo: `kwaivgi/kling-v2.0` | Parámetro de imagen: `start_image` (NO `image`) | cfg_scale: 0.5

### Fórmula de prompt

```
[SUJETO] + [VERBO DE MOVIMIENTO ESPECÍFICO] + [DIRECCIÓN/RESULTADO] + [CONTEXTO ATMOSFÉRICO]
```

Kling responde bien a **movimientos lentos, deliberados, de un solo sujeto**. Cuantos más elementos simultáneos, peor el resultado.

### Lo que NO funciona

| ❌ Patrón | Qué pasa | ✅ Alternativa |
|---|---|---|
| `[acción] toward camera` con violencia | Kling aplica acción sobre el sujeto, no hacia espectador | Describir experiencia del espectador: "foreleg descends into frame" |
| Múltiples eventos simultáneos | Kling ignora la mayoría | Un solo movimiento principal |
| `camera shakes` | No lo interpreta como efecto de cámara | Omitir — editar en post |

---

## 10. TIMING — fórmula general

```
T_inicio = T_fin_hito_anterior

# Para cada bloque de narración encadenado:
T_blockN_fin = T_blockN-1_fin + dur_blockN

# Para countdown + loading:
T_countdown = T_narrLast_fin + 0.2  (gap mínimo)
T_loading = T_countdown
T_twist_flash = T_countdown + 3.0  (loading bar 2.5-3s estándar)
```

Siempre medir duraciones reales con `ffprobe` antes de calcular — nunca asumir.

---

## 11. MULTI-AGENT COORDINATION — render-lock

> Sesión 2026-05-10: 3 renders de mina-abandonada fallaron consecutivos con `FFmpeg signal 15` porque otro Claude estaba a 12-25% CPU simultáneamente. Diagnóstico tardó ~45 min porque el error NO sugiere "wait for the other agent". Resuelto con un lockfile global.

### El problema

Cuando dos agentes Claude lanzan `npx hyperframes render` simultáneos:
- Ambos compiten por CPU para frame capture (Chrome headless)
- Y por CPU para encoding (ffmpeg)
- El encoder se enlentece a 3-4 fps (~10x más lento que normal)
- HyperFrames mata el ffmpeg con SIGTERM por timeout interno
- Result: ambos renders fallan

### La solución — `scripts/render-lock.py`

Lockfile global en `~/.claude-render-lock.json` que cualquier agente puede leer/escribir.

```bash
# Antes del render
.venv/bin/python scripts/render-lock.py acquire <project> --duration 15

# Si falla (otro agente lo tiene), esperar
.venv/bin/python scripts/render-lock.py wait <project> --timeout 1800

# Render
npx hyperframes render . --output renders/v8.mp4

# Después (siempre, incluso si el render falla)
.venv/bin/python scripts/render-lock.py release
```

### Comandos disponibles

| Comando | Qué hace | Exit code |
|---|---|---|
| `acquire <project>` | Toma el lock si está libre; falla si otro lo tiene | 0 = ok, 1 = ocupado, 2 = recuperó lock stale |
| `wait <project>` | Bloquea hasta poder acquire, polea cada 5s | 0 = adquirido, 3 = timeout |
| `release` | Libera si somos los holders | 0 = ok |
| `status` | Muestra quién tiene el lock + si está vivo | 0 = libre, 2 = stale, 0 = alive |

Setup: `cp .claude/skills/ai-video-production/templates/scripts/render-lock.py scripts/`.

### Buenas prácticas

- **Siempre acquire antes de cualquier render >5 min**. No lo skippes "porque hoy estoy solo" — costo casi cero, ahorra 45 min cuando se rompe.
- **Release inmediato después del render**, incluso si falló. Si tu proceso muere antes del release, el lock queda stale y el próximo agente lo limpia automáticamente (pid check).
- **Para renders cortos (<3 min) podés skippear** el lock, pero documentalo en el video-log para que sepamos por qué no se usó.

---

## 12. CHECKLIST GENERAL (cualquier video con IA)

Antes de cualquier render:

- [ ] Todos los `<audio>` tienen `id` único
- [ ] Todos los elementos invisibles tienen ancla `tl.set(el, {opacity:0}, 0)`
- [ ] `data-track-index` único por clip
- [ ] Captions con `white-space: normal` + `text-stroke`
- [ ] Música procesada en 2 pasos (no -ss + -af)
- [ ] Symlinks creados si aplica
- [ ] `data-duration` de la composición = T_fin del último elemento
- [ ] Voice ID verificado en scripts/tts.py
- [ ] STYLE_SUFFIX correcto en scripts/image.py si aplica
- [ ] Variantes de imagen para escenas >4s (V8-1)
- [ ] Capa SFX dedicada (V8-2 — ver SFX-PIPELINE.md)
- [ ] Motion mínimo en planos estáticos (V8-3 — ver MOTION-LAYER.md)
- [ ] Captions auto-generadas con Whisper (no manuales)
- [ ] **`npx hyperframes lint` sin errores**
- [ ] **`scripts/audit-narrative.py` sin errores** (ver `AUDIT.md`)
- [ ] **`scripts/render-lock.py acquire` exitoso** (ver sección 11)
- [ ] **HUMAN-CHECKLIST corrido después del último Gemini QA** (ver `video-director/HUMAN-CHECKLIST.md`)

Para checklists específicos por formato, ver el SKILL del formato (ej: `horror-choice-format/PAUTA.md`).

---

## 13. PER-CLIP ATOMIC ASSEMBLY (Phase 2 forward — 2026-05-20)

> **Architectural refactor**. Codifica user architectural insight (memory `feedback_per_clip_atomic_assembly`). **Replaces** global `master.mp3` + clip merge legacy. Forward-canonical para video #3+ (matadero + cinema-abandonado quedan en legacy global).

### 13.1 Por qué refactor — bug classes eliminadas

El pipeline legacy (global audio master + clip merge al final) acumulaba 7/8 clases de bug recurrentes:

| # | Bug class | Causa raíz (global master) | Caso disparador |
|---|-----------|-----------------------------|-----------------|
| 1 | Sync drift end-of-timeline | Audio compoundea +0.5s drift por timeline largo (90s) | matadero iter 1 "QUE DAS CENA" + cinema iter 1 "ELICHE" |
| 2 | Caption fragmentation | Whisper sobre master.mp3 fragmenta en boundaries | matadero iter 7 D1/D2 |
| 3 | Same-Y caption overlap | Captions placed sobre timeline global no ven contexto per-clip | matadero iter 5 |
| 4 | Audio/clip mismatch at boundaries | Master.mp3 boundaries no align con clip cuts | matadero iter 7 GSAP timing offsets |
| 5 | SFX context-blind | SFX placed sobre timeline global ignora qué pasa en cada clip | recurring |
| 6 | AVU GSAP timing fragility | AVU compose-time (HTML/GSAP) vs pre-rendered atomic | matadero iter 3-4 |
| 7 | Cumulative timeline error | Drift compounds | universal en videos >60s |
| 8 (no eliminada) | Cross-clip music ducking | Sigue siendo cross-clip layer post-concat | manejado en step 8 abajo |

### 13.2 Pipeline DEPRECATED (legacy global master)

```
Phase 1: Animate all clips (CP4) → assets/clips/shot_NN.mp4 (no audio)
Phase 2: Generate TTS per segment → assets/tts/*.mp3 (separate timeline)
Phase 3: Generate SFX → assets/sfx/*.mp3 (separate)
Phase 4: ffmpeg compose master.mp3 (90s long audio timeline)        ⛔ DRIFT FUENTE
Phase 5: HyperFrames composition + ffmpeg merge clips + master.mp3
Phase 6: Final render with captions overlay

Problems:
- Sync errors compound across timeline
- Hard to verify per-clip independent
- Audit only after FULL render
- End-of-timeline drift hidden until final inspection
```

### 13.3 Pipeline FORWARD canonical (per-clip atomic assembly)

```
Per clip (atomic unit, repeats N times):
  Step 1: Animate Hailuo/Kling/Seedance → shot_NN.mp4 (visual only)
  Step 2: Generate audio per clip window
    - TTS narration segment (timing matched to shot)
    - SFX events for THIS shot (context-aware)
    - Local ambient slice (per shot duration)
  Step 3: Mix audio per clip → shot_NN_audio.mp3 (atomic, NO cumulative drift)
  Step 4: ffmpeg mux video + audio → shot_NN_with_audio.mp4
  Step 5: Caption sidecar JSON per clip → shot_NN_captions.json (Whisper local)
  Step 6: Quality Gate Agent per-clip verdict (≥9.0 PASS / iterate / escalate)
  Step 7 (mid-execution): Gemini Vision hook per clip → frame-by-frame audit ANTES de concat
  
Then assemble (cross-clip layers):
  Step 8: ffmpeg concat shot_01_with_audio.mp4 + shot_02_with_audio.mp4 + … → assembled.mp4
  Step 9: Effects library between clips (transitions: crossfade / hard cut / white flash / glitch / shader wipe)
  Step 10: Cross-clip music layer (sections: hook / dilemmas / outro) con ducking automático
  Step 11: Cross-clip ambient continuous (room tone bridges between clip cuts)
  Step 12: Color grading LUTs per section (NARRATIVE warm / CHOICE cool)
  Step 13: Final render + global audit (Gemini holístico ≥9.7 + audit-against-referent ≥85%)

Benefits:
- Per-clip sync verified independent (Quality Gate per clip, NOT global only)
- Debug per shot (vs full 90s scan)
- No cumulative timeline drift
- Reusable shot-with-audio assets (outro card AVU + audio bundled)
- Aligns with AVU principle (audio-visual coupled = single atomic .mp4)
- Mid-execution Gemini Vision catches bugs ANTES de finishing all clips
```

### 13.4 Scripts referenciados

| Script | Función |
|--------|---------|
| `scripts/build_clip_atomic.py` | Steps 2-5: TTS + SFX + ambient + mix + mux + caption sidecar PER clip. Self-contained atomic builder. |
| `scripts/quality_gate_per_clip.py` | Step 6: Quality Gate Agent — per-clip verdict ≥9.0 PASS / 7.0-8.9 iterate / <7.0 escalate. Inputs: clip mp4 + caption JSON + SPEC shot data. |
| `scripts/gemini_midexec_vision.py` | Step 7: Mid-execution Gemini Vision hook — Gemini Vision frame extraction per clip, AVU detect, character consistency vs anchor, caption Y position. Invoked AFTER step 6 PASS, BEFORE concat. |
| `scripts/concat-clips-with-audio.sh` | Step 8: ffmpeg concat protocol for shot_NN_with_audio.mp4 chain. |
| `scripts/apply-effects-between-clips.py` | Step 9: Effects library applier (crossfade/hard-cut/flash/glitch/wipe) per SPEC transition spec. |
| `scripts/apply-cross-clip-music.py` | Step 10-11: Music + ambient cross-clip layer with ducking + section LUFS targets. |
| `scripts/master-audio.sh` (legacy) | ⛔ DEPRECATED for video #3+. Mantener solo para regenerate de matadero/cinema-abandonado si needed. |

### 13.5 Effects library reference

Between-clip transitions live en `ai-video-production/templates/effects-library/`:

| Effect | File | Use case |
|--------|------|----------|
| `hard-cut` | (no asset — ffmpeg concat default) | Default. Pacing cuts/min 2-7. |
| `crossfade-0.3s` | `crossfade-0.3.json` (xfade duration spec) | Mood transitions (NARRATIVE between dilemmas) |
| `white-flash-0.1s` | `white-flash-0.1.mp4` (AVU 1080×1920) | Pre-twist / decision impact |
| `glitch-0.2s` | `glitch-0.2.mp4` (AVU) | Plot twist reveal |
| `shader-wipe-vertical` | `shader-wipe-vertical.mp4` (AVU) | Hook → dilemma transition |
| `dip-to-black-0.4s` | `dip-to-black-0.4.json` (xfade spec) | Outro card transition |

Cada transition declared en SPEC schema v10 `transitions[]` array. Engineer applies via `apply-effects-between-clips.py`.

### 13.6 Quality Gate Agent (NEW 4th role — operates per clip)

> **NEW agent role** added 2026-05-20 forward. Operates BETWEEN engineer per-clip build + final auditor pass. Lives in its own terminal (3-terminal-separation rule, memory `feedback_3_terminal_separation` extended).

| Field | Value |
|-------|-------|
| **Trigger** | Engineer completes shot_NN atomic build (step 5) |
| **Inputs** | shot_NN_with_audio.mp4 + shot_NN_captions.json + SPEC shot data |
| **Verdict thresholds** | ≥9.0 PASS (proceed to step 7 Gemini Vision) / 7.0-8.9 ITERATE (engineer re-builds clip) / <7.0 ESCALATE (architect re-spec) |
| **Output** | `CP[N]-clip-NN-gate-verdict.md` (filesystem handoff) |
| **Cap** | 3 iterations per clip — tras 3 sub-9.0 → ESCALATE no opcional |

### 13.7 Mid-execution Gemini Vision hooks

Invocados en step 7 per clip (post Quality Gate PASS). NO esperar final render para audit.

```bash
.venv/bin/python scripts/gemini_midexec_vision.py \
  --clip assets/clips/shot_NN_with_audio.mp4 \
  --captions assets/captions/shot_NN_captions.json \
  --spec creative-specs/<id>.yaml \
  --shot-id shot_NN \
  --output audits/shot_NN_gemini.json
```

Output: 5 dimensions per clip (UI overlap, frame negros, AVU detect, character consistency vs anchor, caption Y canonical). Exit 0 = OK proceed concat. Exit 1 = ISSUE → fix antes de concat (cheaper than re-render all clips).

### 13.7.5 ⭐ Audio architecture — 3 layers explicit (added 2026-05-21 post user Q&A)

> **Gap detected**: doc § 13 mencionó "Add cross-clip music continuous layer" vague. User Q&A 2026-05-21 exposed 3 critical gaps: (1) quién compone música continuous, (2) transition_post hook = visual only o audio?, (3) SFX impulsivos clip o effect? Esta sub-section cierra esos gaps.

**Three audio layers — scope decision matrix**:

```
┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 1 — PER-CLIP ATOMIC (scene-bound, diegetic)                  │
│ ────────────────────────────────────────────────                    │
│ Lives in: clip_NN_atomic.mp4 audio mux (via build_clip_atomic.py)   │
│ Contents:                                                           │
│   • TTS narration for this clip's window                            │
│   • Diegetic SFX (occurs IN scene: cocinera spoon tap, projector   │
│     hum, door creak DURING clip, character footsteps)               │
│   • Ambient slice (room tone scoped to this scene)                  │
│   • AVU overlay audio (countdown ticks bundled in AVU mp4)         │
│ Audit: Quality Gate Agent per-clip (step 6) ✅                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 2 — EFFECT TRANSITIONS (boundary-bound, non-diegetic)        │
│ ────────────────────────────────────────────────                    │
│ Lives in: effect_NN_to_NN+1.mp4 (separate file ENTRE clips)         │
│ Contents:                                                           │
│   • Editorial impulsive SFX: whoosh, stinger, flash impact,        │
│     projector-cue (cambio de carrete), glitch-static               │
│   • Drone-tail crescendo across boundary                           │
│   • Audio sting bundled per effect recipe                          │
│     (effects-library/transitions/<name>.json `audio_sting_volume`) │
│ Audit: NEW Q22 gate post-concat — `audit-effects-audio.py` ✅       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ LAYER 3 — CROSS-CLIP CONTINUOUS (global-bound, post-concat)        │
│ ────────────────────────────────────────────────                    │
│ Lives in: separate tracks ffmpeg amix post-concat with assembled    │
│ Contents:                                                           │
│   • drone_base (continuous 0-duration_s)                            │
│   • accent_drama (per-section, e.g. climax 50-88s)                  │
│   • ambient_room (continuous, room signature genre)                 │
│ Audit: NEW Q23 gate post-concat — `audit-music-layers.py` ✅        │
└─────────────────────────────────────────────────────────────────────┘
```

**SFX placement decision rule (Q3 resuelta)**:

```
"¿Esto pasa EN el mundo de la escena, o marca el corte editorial?"
  • EN el mundo (diegetic) → LAYER 1 (clip atomic)
  • Marca corte (non-diegetic) → LAYER 2 (effect file)
  
Examples:
  - Cocinera taps spoon @ 0:23 → diegetic (her action) → LAYER 1
  - Whoosh between clip 5→6 → non-diegetic editorial → LAYER 2 (in effect)
  - Projector hum continuous → diegetic ambient → LAYER 1
  - Cinema reel-change cue → non-diegetic transition marker → LAYER 2
  - Heartbeat sync to character action → diegetic → LAYER 1
  - Music drone background continuous → non-diegetic → LAYER 3
```

**Cross-clip music composition workflow (Q1 resuelta)**:

```
1. ARCHITECT SPEC declares (schema v10 NEW field):
   music_continuous_layers:
     - layer_id: "drone_base"
       sections: [{from: 0s, to: 88s, intent: "tension low-freq"}]
       eleven_labs_prompt: "deep industrial drone, no melody, slow swells"
       compose_strategy: "single_continuous_88s" | "stitched_sections"
       target_lufs_pre_mix: -27 dBFS
     - layer_id: "accent_drama"
       sections: [{from: 50s, to: 88s, intent: "rising tension"}]
       eleven_labs_prompt: "dark cinematic strings rising"
       compose_strategy: "single_38s"
       target_lufs_pre_mix: -25 dBFS
     - layer_id: "ambient_room"
       sections: [{from: 0s, to: 88s, intent: "scene ambience continuous"}]
       eleven_labs_prompt: "abandoned cinema room tone, distant hum"
       compose_strategy: "loop_8s_stretched"
       target_lufs_pre_mix: -30 dBFS

2. ENGINEER llama ElevenLabs compose_music PER LAYER per SPEC strategy:
   - "single_continuous_Xs" → 1 file exact length (preferred)
   - "stitched_sections" → N files crossfaded via ffmpeg acrossfade
   - "loop_Xs_stretched" → loop a base sample to target duration
   
3. PER-LAYER VERIFY pre-concat (NEW Q23 gate):
   - LUFS in band per layer type ✓
   - Length match video_duration_s ±0.5s
   - No speech bleed (Whisper voiceprint check)
   - Spectrum analysis (drone <300Hz, accent 200-2000Hz, ambient broadband)
   
4. ASSEMBLE post-concat (apply-cross-clip-music.py):
   ffmpeg amix assembled.mp4 + drone_base.mp3 + accent_drama.mp3 + ambient_room.mp3
   + sidechain ducking layer 1+2 UNDER TTS speech (-8 dB during VO segments)
   + final master loudnorm -14 LUFS / -1 dBTP
```

**transition_post hook expansion (Q2 resuelta)**:

```
gemini_midexec_vision.py hook `transition_post` EXTEND from visual-only to visual + audio:

Visual checks (existing):
  - visual_continuity (frames pre-boundary vs post-boundary)
  - no_broken_frames
  - ui_continuity
  - composition_flow
  - atmospheric_continuity

Audio checks (NEW added 2026-05-21):
  - audio_continuity (ffmpeg sliding window 2s pre / 2s post boundary,
    Whisper transcribe both sides, verify NO mid-word truncation)
  - music_layer_continuity (post-concat verify no dropout in layers 1+2+3
    at boundary timestamp via librosa RMS comparison ±3dB tolerance)
  - effect_audio_volume_match (effect sting peak vs clip audio fabric
    pre-effect RMS, target ±3dB to avoid jarring jumps)
  - sfx_no_bleed (clip 5 audio scope verify ends WITH clip 5 boundary,
    Layer 1 audio file length matches clip mp4 video length ±0.05s)

Cost impact: +$0.05/transition × ~10 transitions/video = +$0.50/video
```

**Forward script implementations** (Phase 3 priority):
- `scripts/audit-effects-audio.py` — Q22 gate post-concat (effect sting audit)
- `scripts/audit-music-layers.py` — Q23 gate post-concat (3 layers per-layer verify)
- `scripts/apply-cross-clip-music.py` — Layer 3 assemble protocol with sidechain ducking
- `gemini_midexec_vision.py transition_post` — extend with 4 audio dimensions

---

### 13.8 Migration guide para proyectos existentes

| Proyecto | Estado | Acción |
|----------|--------|--------|
| `elige-companero/`, `bosque-abandonado/`, `mina-abandonada/`, `pueblo-fantasma-desierto/` | LEGACY global master | NO migrar — quedan as-is reference para post-mortem |
| `matadero/`, `cinema-abandonado/` | LEGACY global master (in-flight) | Terminar con pipeline legacy. NO refactor mid-project. |
| Video #3+ (cualquier proyecto NUEVO 2026-05-20 forward) | **MANDATORY per-clip atomic** | Usar pipeline § 13.3. Hard Rule #23. |

**Bootstrap nuevo proyecto**: copiar los 3 nuevos scripts (`build_clip_atomic.py` + `quality_gate_per_clip.py` + `gemini_midexec_vision.py`) en step 2 del `BOOTSTRAP.md`.

**SPEC schema v10**: arquitecto declara `assembly_strategy: per_clip_atomic` (default forward) o `global_master` (legacy backcompat solo).
