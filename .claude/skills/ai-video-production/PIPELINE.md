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
