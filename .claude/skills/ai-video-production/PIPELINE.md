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

### Voice IDs canonical (post 2026-05-18 — siempre consultar `library/voices-catalog.json` como autoridad)

| Voz | ID | Estado | Característica |
|-----|-----|--------|----------------|
| **Oxley Evil Character** | `2gPFXx8pN3Avh27Dw5Ma` | ✅ default canonical | LatAm baseline ~96 WPM. Narrator + matarife (con SoX effects chain). Validated matadero CP2 M7.7.5 PASS. |
| **Kate BFP** | `qWWAqFomnJ99VwQLREfT` | ✅ cocinera canonical | Warm female Spanish. User override matadero CP2 2026-05-19. |
| **Valeria** | `9oPKasc15pfAbMr7N6Gs` | 🟡 alternative cocinera | Warm female ~143 WPM. Valid alternative for non-matadero projects. |
| **David C2 — Deep horror narrator** | `K3TeN3ZVK8WnOeJ0NYqZ` | ✅ canonical V5+ narrator (2026-05-29) | Deep mysterious LatAm horror. WPM 157.2 raw (canonical band). Tomás A/B pick over Eleguar/Ignacio/José. |
| Ignacio Uruguayan (A/B alternate) | `AvFwmpNEfWWu5mtNDqhH` | 🟡 reserva TikTok-energetic | WPM 179.4 raw. Reserva si SPEC futuro pide format viral stories. |
| Eleguar (A/B alternate) | `T7QGPtToiqH4S8VlIkMJ` | 🟡 reserva entertainment | WPM 166.0 raw. Reserva si SPEC futuro pide entertainment-TV energetic. |
| ~~José Latam Neutral Warm~~ | ~~`HdHf5loDYrvGJRrbzbUX`~~ | ❌ rejected horror (2026-05-29) | WPM 143.3 debajo canonical p25. Pattern repeat de Vicente rejection. |
| ~~Matthew Schmitz Nosferatu~~ | ~~`Tj9l48J9AJbry5yCP5eW`~~ | ❌ DEPRECATED 2026-05-18 | Susurro grave lento. Matadero CP2 user listen test refuted canonical compliance ('muy lento'). |
| Reservada | `1BfrkuYXmEwp8AWqSLWk` | 🟡 untested | Sin testear. |

**Verificar `DEFAULT_VOICE_ID` en `scripts/tts.py` antes de cada video nuevo (debe ser `2gPFXx8pN3Avh27Dw5Ma` Oxley).** Cada formato puede definir su voz canónica via `<format>-format/INGENIERO-PAUTA-MASTER.md`.

### Post-procesado obligatorio — atempo per-segment (post 2026-05-18)

**DEPRECATED**: atempo 2.0 uniform (era para Tj9l48J9 deprecated voice). NUNCA uses esto en producción nueva.

**CANONICAL** workflow per `voices-catalog.json` § atempo_rule:

1. Per-segment atempo computed via `raw_dur/target_dur` clamped `[0.7, 2.5]`
2. Per-speaker multiplier on top (SPEC pace_correction_path_E_2026_05_18):
   - narrator ×1.15
   - matarife ×1.28 (ceiling)
   - cocinera ×1.23
3. Verify post-TTS measure_F1.py vs canonical p25-p75 bands `[152.71, 179.84]`

```bash
# Per-segment example:
ffmpeg -y -i assets/nombre-raw.mp3 \
  -filter:a "atempo=<raw_dur/target_dur clamped 0.7-2.5>" \
  assets/nombre-atempo.mp3

# Per-segment medir duración:
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/nombre-atempo.mp3
```

**Regla:** nunca usar el raw en el render. Siempre el `-atempo.mp3` con per-segment ratios. La voz cruda suena a IA + lenta de canonical band.

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

El default `white-space: nowrap` rompe captions largos: siempre `white-space: normal` + `width: 960px` + `text-align: center`.

> CSS canónico de captions → `CAPTIONS.md` (3 clases + drop-shadow, NO thick stroke).

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

### Volúmenes recomendados

> Mix volumes canónicos → `SFX-PIPELINE.md § Mix volumes`.

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

Between-clip transitions live en la carpeta **GLOBAL root `transitions/`** (migrada 2026-06-05; principio "Disponibilidad ≠ Uso" intacto): **universal** `transitions/universal/transitions/` (11: cross-fade ×2, hard-cut-with-whoosh, black-screen, fade-to-black, light-flash, glitch, camera-shake, pan-left, brightness-flash, zoom-in) + **per-format** `transitions/<format>/transitions/` (horror-choice: film-burn, projector-cue-cinema, static-noise, old_screen_glitch_error). **Índice transición→formato = `transitions/catalog.json`** (consultar PRIMERO); autoridad = `transitions/README.md`. Los paths viejos effects-library quedan como symlinks de compat. Caption burn styles → `templates/caption-styles/caption-burn-template.css`. (La tabla de abajo es un sketch Phase 2 histórico):

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
│ Applied as: xfade filter post-concat at clip boundaries.            │
│   (Canonical pattern PRE-4.E 2026-05-25 — see §13.9.1 LAYER 2.)     │
│   NOT separate files / NOT pre-rendered intermediate mp4s.          │
│ Contents:                                                           │
│   • Editorial impulsive SFX: whoosh, stinger, flash impact,        │
│     projector-cue (cambio de carrete), glitch-static               │
│   • Drone-tail crescendo across boundary                           │
│   • Audio sting bundled per effect recipe                          │
│     (transitions/<layer>/transitions/<name>.json `audio_sting_volume`) │
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
       target_lufs_pre_mix: -27 ±2 dBFS   # PRE-4.C tolerance (2026-05-25): SPEC-declared band (plumbing). F1 NOT measure per-layer pre-mix (only final mix); SPEC-anchored is canonical for this parameter.
     - layer_id: "accent_drama"
       sections: [{from: 50s, to: 88s, intent: "rising tension"}]
       eleven_labs_prompt: "dark cinematic strings rising"
       compose_strategy: "single_38s"
       target_lufs_pre_mix: -25 ±2 dBFS   # PRE-4.C tolerance (2026-05-25): SPEC-declared band
     - layer_id: "ambient_room"
       sections: [{from: 0s, to: 88s, intent: "scene ambience continuous"}]
       eleven_labs_prompt: "abandoned cinema room tone, distant hum"
       compose_strategy: "loop_8s_stretched"
       target_lufs_pre_mix: -30 ±2 dBFS   # PRE-4.C tolerance (2026-05-25): SPEC-declared band

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
   + sidechain ducking layer 1+2 UNDER TTS speech (-8 ±1 dB during VO segments)   # PRE-4.C tolerance (2026-05-25): SPEC-declared band (plumbing). Outcome verifiable via final dynamic_range_db (F1 canonical 14.49-22.34, typical ducking 10-25 dB).
   + final master loudnorm -14 ±0.5 LUFS / -1 ±0.3 dBTP   # PRE-4.C tolerance (2026-05-25): LUFS CANONICAL-ANCHORED to F1 (avg -14.06 ±0.41, p25 -14.03, p75 -13.86 per F1-INGENIERO-MEASUREMENTS.json). dBTP headroom SPEC-anchored (F1 NOT measure).
```

**PRE-4.C tolerance bands — dual source pattern (codified 2026-05-25)**:

Per PRE-4.B F1 coverage audit (29 properties × dual-source classification):
- **CANONICAL-ANCHORED (F1 measured)**: final master LUFS (F1 p25-p75 -14.03 to -13.86), dynamic_range_db (F1 14.49-22.34), cuts_per_min, brightness_mean, etc.
- **SPEC-DECLARED (plumbing, F1 NOT measure)**: per-layer pre-mix LUFS, sidechain duck target dB, dBTP headroom, layer length tolerance, codec/fps/sample rate, etc.

Tests in Paso 4 (apply-cross-clip-music.py, build-video-hybrid.py) reference these tolerance bands per α + γ-1 plan: canonical-anchored where F1 measures, SPEC-anchored otherwise. NO golden reference V4 per Tomás canonical principle.

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

**Forward script implementations** (status as of 2026-05-23 Sub-Fase 3A inventory):
- `scripts/audit-effects-audio.py` — **FORWARD — not built, audit done manually via existing audio scripts**. Q22 gate post-concat audit done via combination of `audit-audio.py` + manual ffmpeg volumedetect + Gemini Vision audit-frames for visual+audio sync verification. NOT a blocker for V4+ ship.
- `scripts/audit-music-layers.py` — **FORWARD — not built, audit done manually via existing audio scripts**. Q23 gate done via `audit-audio.py` narration coverage + sound fabric thresholds (≥99% fabric required). Music layer count + duration verified manually via ffprobe per layer file pre-mix. NOT a blocker for V4+ ship.
- `scripts/apply-cross-clip-music.py` — **TO BUILD (Sub-Fase 3A Paso 4)**. Layer 3 assemble protocol with sidechain ducking. Engineer V4 used inline ffmpeg; Paso 4 consolidates as reusable script per Sprint M defense in depth.
- `scripts/concat-clips-with-audio.py` — **TO BUILD (Sub-Fase 3A Paso 4)**. Inter-clip concat with audio properly muxed.
- `scripts/apply-effects-between-clips.py` — **TO BUILD (Sub-Fase 3A Paso 4)**. Effects library application between atomic clips.
- `scripts/build-video-hybrid.py` — **TO BUILD (Sub-Fase 3A Paso 4)**. Consolidates V4 engineer inline ffmpeg as reusable script. Encapsulates full HYBRID Layer 1-4 pipeline.
- `gemini_midexec_vision.py transition_post` — extend with 4 audio dimensions (existing script, extension forward Phase 3 priority).

---

### 13.8 Migration guide para proyectos existentes

| Proyecto | Estado | Acción |
|----------|--------|--------|
| `elige-companero/`, `bosque-abandonado/`, `mina-abandonada/`, `pueblo-fantasma-desierto/` | LEGACY global master | NO migrar — quedan as-is reference para post-mortem |
| `matadero/`, `cinema-abandonado/` | LEGACY global master (in-flight) | Terminar con pipeline legacy. NO refactor mid-project. |
| Video #3+ (cualquier proyecto NUEVO 2026-05-20 forward) | **MANDATORY per-clip atomic** | Usar pipeline § 13.3. Hard Rule #23. |

**Bootstrap nuevo proyecto**: copiar los 3 nuevos scripts (`build_clip_atomic.py` + `quality_gate_per_clip.py` + `gemini_midexec_vision.py`) en step 2 del `BOOTSTRAP.md`.

**SPEC schema v10**: arquitecto declara `assembly_strategy: per_clip_atomic` (default forward) o `global_master` (legacy backcompat solo).

---

### 13.9 ⭐⭐ HYBRID ARCHITECTURE canonical (added 2026-05-21 PM late post V3 caption desync)

> **Root cause V3 desync**: cinema legacy global captions + narrator master drift architecture allows caption-audio misalignment. Phase 2 per-clip atomic eliminates that drift class BUT V3 iter 1 implementation skipped UI overlays. **Solution = HYBRID combining both**.

#### 13.9.1 Three architectural layers (canonical V4+)

```
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 1 — PER-CLIP ATOMIC (mandatory)                               │
│  Each shot mp4 = self-contained unit:                                │
│    ├── Visual (Hailuo image-to-video OR Veo if available)            │
│    ├── Clip-scoped audio:                                            │
│    │     - Character speech (if shot has character on-screen)        │
│    │     - Diegetic SFX scoped to shot                               │
│    │     - AVU overlay audio (countdown ticks if applicable)         │
│    ├── Captions BURNED per clip:                                     │
│    │     - Caption text for THIS clip's audio window                 │
│    │     - Aligned to clip's local timeline (0-Xs relative)          │
│    │     - Whisper-derived from clip audio (NOT SPEC intent)         │
│    │     - Burned via ffmpeg drawtext or video filter                │
│    └── Output: assets/clips-atomic/shot_N_atomic.mp4                 │
│                                                                      │
│  PROPERTY: caption-audio LOCKED at frame level. Cannot drift.        │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ concat atomic clips
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 2 — EFFECTS BETWEEN CLIPS (xfade filter post-concat)          │
│  ────────────────────────────────────────────                        │
│  Canonical pattern (PRE-4.E 2026-05-25): xfade filter applied to     │
│  concat'd stream AT clip boundaries. NO pre-rendered effect mp4s.    │
│                                                                      │
│  Implementation (V4 empirical via cp5-layer2-concat.py):             │
│    Step 1 — 4.2 concat-clips-with-audio.py:                          │
│      Concat atomic clips back-to-back, audio properly muxed.         │
│      Output: assets/concat/clips_concat_only.mp4                     │
│    Step 2 — 4.4 apply-effects-between-clips.py:                      │
│      xfade filter at boundaries per SPEC.shot_list[].transition_in   │
│      + sting audio overlaid per transitions/<layer>/transitions/*.json│
│      Output: assets/concat/clips_with_effects.mp4                    │
│                                                                      │
│  Transition recipes available (transitions/ global — catalog.json):  │
│    - B&W TV static interference (NEW 2026-05-21 user request)        │
│    - Cross-fade, hard-cut-whoosh, light-flash, film-burn, glitch     │
│    - Each recipe bundles audio_sting + visual filter params          │
│                                                                      │
│  RATIONALE: simpler + declarative + fewer intermediate artifacts =   │
│  fewer surface bugs (Principio 4 sistema solidez). Rejected:         │
│  pre-rendered effect_N_to_N+1.mp4 files (sequence concat pattern,    │
│  more bug surface, NOT V4 empirical).                                │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼ concat'd stream with effects applied
┌──────────────────────────────────────────────────────────────────────┐
│  LAYER 3 — CROSS-CLIP CONTINUOUS (post-concat overlay)               │
│  Continuous audio tracks overlaid post-concat:                       │
│    - Narrator master (continuous 0-duration_s, no cuts at boundaries)│
│    - Music drone_base + accents per section                          │
│    - Ambient continuous                                              │
│    - Sidechain ducking music/ambient under narrator                  │
│  Plus UI overlays via HyperFrames OR ffmpeg overlay:                 │
│    - Countdown 3-2-1 at hook end (GSAP OR AVU clip)                  │
│    - Decision UI (freeze + VHS filter + buttons + loading bar)       │
│    - AVU outro card ("TÚ DECIDES" + watermark)                       │
│    - Name labels Y11.5% monospaced                                   │
│  Final master loudnorm -14 LUFS stereo 48kHz                         │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  ┌─────────────────────────┐
                  │ Final render mp4         │
                  │ 1080×1920 9:16           │
                  │ Caption-audio LOCKED     │
                  │ Drift-free architecture  │
                  └─────────────────────────┘
```

#### 13.9.1.1 LAYER 2 — I/O clarification + tiered catalogs (PRE-4.J / PRE-4.K 2026-05-27)

- **I/O (Finding #1):** `apply-effects-between-clips.py` reads the **atomic clips** (`--clips-dir`), NOT the 4.2 `clips_concat_only.mp4`. xfade physically requires N separate inputs, so the chain is rebuilt from atomic clips (V4 empirical `cp5-layer2-concat.py`). The 4.2 concat output is consumed ONLY by the **passthrough** branch (`has_layer_2_effects: false` → copy).
- **Tiered catalogs ("Disponibilidad ≠ Uso"):** transitions live in TWO catalogs — Capa A universal primitives (7) + Capa B format sub-genre. `--effects-dir` accepts ONE OR MORE catalog dirs (searched in order), REQUIRED in the effects branch (no silent format default = agnostic-by-design). Availability ≠ prescription: the SPEC `shot_list[].transition_in/out` (Capa C) decides what is applied; a format may reference Capa A primitives + add its own Capa B without duplicating.
- **Option D fidelity:** each recipe declares `xfade_transition` + `xfade_fidelity` (literal|approximate) + `native_mechanism_note`. Chained-xfade is LOSSY for the 5 `approximate` recipes (native mechanisms = concat-insert / overlay / terminal-fade ≠ a single xfade); a WARNING fires on production use. Full fidelity = Option B hybrid dispatch (`transition_method` enum) — GAPS-LOG trigger.
- **Schema:** per-shot `transition_in/out` canonical (PRE-4.J Decision 3); legacy top-level `transitions[]` arrays normalized via `lib/spec_transitions_adapter.py`.

#### 13.9.2 Why HYBRID solves caption-audio drift permanently

```
PROBLEM (cinema legacy global captions):
  CP2 captions sidecar timestamps reference SPEC intent
  CP5 narrator master accommodates TTS overshoots via adelay padding
  CP5 HyperFrames overlay captions at SPEC-intent timestamps
  → audio plays at actual times, captions at intended times
  → cumulative drift 1-3s possible (V3 0-34s window evidenced)

PROBLEM (Phase 2 per-clip atomic V3 iter 1):
  Engineer muxed narrator per-clip → narrator cut at clip boundaries
  Engineer skipped UI overlays (no countdown / decision UI / outro)
  → broken in different way

HYBRID solves BOTH:
  Layer 1: caption baked into clip = same frame data as audio = CANNOT drift
  Layer 3: narrator continuous overlay = no boundary cuts
  Layer 3: UI overlays HyperFrames = countdown + decision + outro work
  
  Result: best of both worlds, drift class eliminated structurally.
```

#### 13.9.3 Implementation per CP

```
CP1 anchors:              Gemini Nano Banana STRICT (unchanged)
CP2 TTS:                  Per-segment generation (unchanged)
CP3 shot refs:            Gemini Nano Banana STRICT (unchanged)
CP4 animation:            Hailuo/Veo image-to-video (unchanged)

CP4.5 NEW — Per-clip atomic mux:
  build_clip_atomic.py extension:
    For each shot N:
      1. Load shot_N.mp4 (Hailuo/Veo visual)
      2. Determine clip-scoped audio:
         - If shot has character on-screen speaking: extract Veo native audio OR use Hailuo + Hedra lip-sync
         - Diegetic SFX: per SPEC sfx_events for this shot timestamp window
         - AVU overlay audio: if shot has countdown/freeze AVU
         - NO narrator (narrator is Layer 3)
      3. Generate captions for this clip's audio:
         - Whisper transcribe clip's audio (NOT SPEC narration)
         - OR if no character speech: skip captions in atomic, narrator captions in Layer 3
         - Burn into clip via ffmpeg drawtext
      4. Mux: visual + audio + captions → atomic mp4
      5. Save: assets/clips-atomic/shot_N_atomic.mp4

CP5 — HyperFrames composition + Layer 3:
  Step 1: Concat atomic clips + insert effects between
  Step 2: Overlay Layer 3 narrator master (continuous)
  Step 3: Overlay Layer 3 music + ambient (continuous)
  Step 4: Apply sidechain ducking
  Step 5: HyperFrames UI overlays (countdown + decision + outro card + name labels)
  Step 6: Final loudnorm -14 LUFS
  Step 7: 8 pre-render gates
```

#### 13.9.4 Updated build_clip_atomic.py spec

Forward modification of `scripts/build_clip_atomic.py`:

```python
def build_atomic_clip(shot_id, spec, output_path):
    """Build self-contained atomic clip with audio + captions baked."""
    # Load visual
    visual = load_hailuo_clip(shot_id)
    
    # Determine clip-scoped audio (NO narrator)
    audio_layers = []
    if shot_has_character_speech(spec, shot_id):
        char_audio = extract_character_audio(spec, shot_id)
        audio_layers.append(char_audio)
    
    sfx = generate_diegetic_sfx(spec, shot_id)
    audio_layers.extend(sfx)
    
    if shot_has_avu(spec, shot_id):
        audio_layers.append(load_avu_audio(spec, shot_id))
    
    mixed_audio = ffmpeg_amix(audio_layers)
    
    # Generate captions FROM CLIP AUDIO (Whisper)
    captions = whisper_transcribe(mixed_audio, language='es', word_timestamps=True)
    # Override caption text with SPEC text_canonical (preserve canonical wording)
    captions = align_captions_to_spec(captions, spec.text_canonical_for_shot(shot_id))
    
    # Burn captions into video
    visual_with_captions = ffmpeg_drawtext(visual, captions, style='canonical_horror_choice')
    
    # Mux
    atomic = ffmpeg_mux(visual_with_captions, mixed_audio)
    atomic.save(output_path)
```

#### 13.9.5 NEW auditor sentinel — caption-audio sync verification

`scripts/audit-caption-audio-sync.py` (forward Phase 3 priority):

```python
def audit_caption_audio_sync(video_path):
    """Verify caption text at frame T matches narrator audio at T."""
    
    # Extract frames every 3s
    frames = ffmpeg_extract_frames(video_path, interval=3)
    
    # Whisper transcribe full audio with word timestamps
    audio_timeline = whisper_full_word_timestamps(video_path)
    
    issues = []
    for t, frame in frames.items():
        # Get caption text on frame via Gemini Vision
        caption_text = gemini_vision_extract_caption(frame)
        # Get narrator audio words at this timestamp (±1s window)
        narrator_words = audio_timeline.words_in_window(t, ±1)
        
        # Verify caption text matches narrator audio
        similarity = jaccard_similarity(caption_text, narrator_words)
        if similarity < 0.5:
            issues.append({
                't': t,
                'caption': caption_text,
                'narrator': narrator_words,
                'similarity': similarity
            })
    
    return issues
```

Run this gate post-CP5 render before declaring complete.

#### 13.9.6 Migration

```
matadero + cinema-abandonado: legacy global master, grandfather, NO migrate
V3 parque-acuatico-abandonado: archived as Phase 3 learning (cinema legacy + caption drift exposed)
V4+ (next video): HYBRID architecture MANDATORY per this § 13.9 + 3 enforcement scripts BLOCKER pre-launch
```

#### 13.9.7 ⛔ Enforcement structural, no procedural

CP-by-CP gates + HYBRID architecture se enforcan vía scripts (build_clip_atomic.py caption-burn + orchestrator state machine), NO vía texto que el agente decide aplicar. Texto sin enforcement = decoración. Detalle del blocker + razón estructural → **Hard Rule #24** (CLAUDE.md) + **AUDITOR-PROTOCOL § 6 anti-pattern #15** (engineer multi-CP autonomous FORBIDDEN).

---

### 13.10 ⭐⭐ CAPABILITY MATRIX per video/format (codified 2026-05-25 PRE-4.G)

> **Caso disparador:** Tomás detectó gap arquitectural — todo lo codificado hasta PRE-4.F asume paradigma único: AI-generated viral video + TTS narration + captions baked + Layer 1-4 architecture + Gemini Image anchors + Veo3. Esto viola Principio 1 (Agnóstico) y Principio 3 (Escalable).
>
> **Pattern 7 — Capability Matrix:** El sistema sostiene paradigmas múltiples de producción de video, NO solo AI-generated horror-choice. Forward, cualquier SPEC declara explícitamente sus capabilities en bloque `video_capabilities`. Validators, builds y tests leen capabilities ANTES de aplicar properties.

#### 13.10.1 Paradigmas posibles (no exhaustive)

- **AI-generated viral video con TTS narration + Layer 1-4** (horror-choice canonical, V4 paradigm)
- **Tutorial sin TTS** (sin Layer 3 audio mix obligatorio, narration humana grabada o silencio)
- **B2B commercial con voiceover humano grabado** (Layer 1 = pre-existing voice file, no TTS)
- **Compilation de video pre-existing** (sin Veo3, sin Gemini Image anchors, source = footage existente)
- **Mixed paradigms** (AI-generated clips + pre-existing voiceover; o pre-existing clips + AI captions)

#### 13.10.2 Capability matrix declarativo (schema conceptual)

```yaml
video_capabilities:
  # Source paradigm
  source_clips_origin: ai_generated | pre_existing | mixed
  has_ai_generated_clips: true|false
  
  # Audio paradigm
  has_tts_narration: true|false
  has_human_voiceover: true|false
  audio_mix_target: lufs_-14 | spec_declared | preserve_source | none
  
  # Visual paradigm
  has_captions_baked: true|false
  has_layer_2_effects: true|false
  has_layer_3_music: true|false
  has_layer_4_ui: true|false
  
  # Format paradigm
  format_type: interactive_choice | tutorial | b2b_commercial | compilation | other
  duration_intent_s: <integer>
```

Schema evoluciona con paradigmas nuevos. NO exhaustive — agregar flags cuando paradigma nuevo lo requiera.

#### 13.10.3 Validator behavior canonical forward

Validators + builds + tests **gating per capability flag**:

```python
# Pseudocode
def test_caption_audio_lock(video, spec):
    if not spec.video_capabilities.has_captions_baked:
        return TestResult.NOT_APPLICABLE  # NOT failed, NOT pass
    # ... only run property check if capability declared ...
```

**Ejemplos de gating concretos:**

| Property | Gated by | Behavior if capability=false |
|----------|----------|------------------------------|
| Caption-audio sync (Hard Rule #25) | `has_captions_baked` | `not_applicable` |
| TTS sidechain duck -8 dB | `has_tts_narration` | `not_applicable` (no TTS to duck under) |
| Layer 3 cross-clip music continuity | `has_layer_3_music` | `not_applicable` |
| Final master LUFS -14 ±0.5 | `audio_mix_target == lufs_-14` | `not_applicable` if `preserve_source` or `none` |
| Veo3/Gemini anchor compliance | `source_clips_origin == ai_generated` | `not_applicable` for pre-existing clips |
| Decision UI overlay (Layer 4) | `format_type == interactive_choice` | `not_applicable` for tutorial/B2B |

#### 13.10.4 SPEC integration

SPEC schema v12+ incluye `video_capabilities` block **mandatorio**. SPEC sin capability matrix → SPEC-AUDIT verdict HALT (Bug #9 escalation a Tomás). Default values reflejan paradigma horror-choice canónico para retrocompatibilidad con V4-era SPECs (v11.x).

#### 13.10.5 Rationale estructural

- **Principio 1 (Agnóstico verdadero):** paradigm-agnóstico, NO solo format-agnóstico. Sistema sostiene tutoriales, B2B, compilations, AI mixed, etc. — sin refactor masivo.
- **Principio 3 (Escalable):** nuevo paradigma = agregar flag a capability matrix + bypassear properties no-aplicables. Sistema no rechaza ni fuerza.
- **Forward implementation:** Paso 4 builds (4.2/4.4/4.3/4.1) + Sprint M validators (11 backed) heredan este pattern desde inicio. Tests classifican: applicable / not_applicable / pass / fail.

#### 13.10.6 Backward compat — V4 SPEC

V4 cerro-aislado-v4.yaml (SHIPPED bajo assumptions previas) queda historical sin `video_capabilities` block. Forward V5+ SPECs lo incluyen mandatorio. Validators leyendo V4 SPEC sin capabilities → asume defaults horror-choice paradigm (backward-compat clause).

---

## 14. VOICE EXCLUSIVITY (4 capas) — Capa A, agnóstica

**LEY (universal, todo formato con voz hablada):** en cualquier instante `t`, como **máximo UNA voz hablada** puede sonar (el narrador **o** un personaje, nunca dos simultáneas). Entre dos ventanas de voz **DISTINTAS** (un handoff narrador↔personaje) el buffer mínimo es **0.30s** — un *floor técnico*, NO una pausa dramática (solo evita que dos voces se peguen al milisegundo). Dos segmentos del **mismo** speaker (narración continua cortada entre shots) **pueden** abutar: es una sola voz, no dos compitiendo. **Música / SFX / ambient conviven libremente** con la voz — la ley solo gobierna voces habladas.

**Por qué:** dos voces simultáneas = artefacto uncanny + señal AI-detect. Disparador V7 `ultimo-tren-carga` v2: `narrator_hook` (12 palabras @165WPM ≈ 4.36s desde 1.8s → fin ~6.16s) se solapaba con `tobias_hook_lure` (arranca 3.2s) por ~2.96s. Caso reconstruido en el test adversarial.

La ley se enforce en **4 capas** (defense-in-depth):

| Capa | Dónde | Qué chequea | Cuándo |
|------|-------|-------------|--------|
| **L1 SPEC** | `audit-spec-voice-exclusivity.py --mode spec --format <f> --spec <yaml>` | Parsea §9 `narration_script` (TODOS los speakers). `ventana = [timestamp_intent_s[0], start + palabras/pace_wpm*60]` con `pace_wpm` = `canonical_pace_wpm` de `MODEL-CAPABILITIES-MATRIX.md` (fallback 165). FAIL si dos ventanas se intersectan, o si el gap entre dos speakers DISTINTOS < 0.30s. | Pre-emit del SPEC (arquitecto) + SPEC-audit (auditor). |
| **L2 TTS** | `audit-spec-voice-exclusivity.py --mode tts --manifest <json> [--spec <yaml>] [--atomic-dir <dir>] [--exclude-segments <ids>]` | Ídem pero con **duraciones REALES** del manifest CP2. El `start` se reconstruye como el del assembly: `shot_start` reconciliado (de `--atomic-dir`) + lead per-speaker (narrador 0.10s / diálogo 0.45s), o `timestamp_intent_s` del SPEC si no hay atomic-dir. `--exclude-segments` para voces que un fix-pack muteó en el corte (presentes como dato en el manifest pero NO en el render). | Post-TTS, pre-assembly + pre-render-gate. |
| **L3 assembly assertion** | `assert_voice_exclusivity()` en el driver per-clip-atomic (`cp5b_run_all.py` phase3) | Sobre los cues de voz FINALES, antes del mix Layer1+Layer3. En colisión entre speakers DISTINTOS intenta **desplazar la voz de menor prioridad** (diálogo cede; en el hook el narrador va primero → prioridad 0) **±1s MÁX dentro de su shot**. Si no cabe → **ABORT** con error claro (NUNCA desplaza >1s ni a aire muerto). Same-speaker overlap → ABORT (bug de assembly). | En cada render del driver. |
| **L4 render audit** *(forward)* | `audit-render-voice-overlap.py` | Mediría sobre el MP4 final (VAD / diarización) que ningún instante tenga dos voces. Red de seguridad post-render. | Forward — aún no implementado. |

**Companion test** (HR#26): `test_audit-spec-voice-exclusivity.py` — adversarial (FAIL sobre el solape v2 narrador+personaje, PASS sobre el layout v3 separado) + fixtures sintéticas + unit tests del shift/abort de `assert_voice_exclusivity()`.

**Forward (Capa A):** portar `assert_voice_exclusivity()` al driver canónico `build-video-hybrid.py` (cualquier per-clip-atomic que mezcle voces en Layer 3) + implementar L4.
