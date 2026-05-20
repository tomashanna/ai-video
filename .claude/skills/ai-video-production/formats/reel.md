# formats/reel.md — Instagram Reels / TikTok / IG Reels

> Delivery format vertical short-form. El más exigente en retención y el más viral si se ejecuta bien.

---

## Specs técnicos (no negociables)

| Atributo | Valor |
|---|---|
| Aspect ratio | 9:16 |
| Resolución | 1080 × 1920 |
| FPS | 30 (o 60 si el contenido es action-heavy) |
| Codec video | H.264 High profile L4.0, yuv420p |
| Codec audio | AAC-LC stereo, 48000Hz |
| Bitrate video | 3-5 Mbps (target ~4 Mbps con CRF 18) |
| Bitrate audio | 128-256 kbps (target 192k) |
| Duración | 30-90s (sweet spot 60-90s) |
| Tamaño máx | <100 MB (idealmente 40-60 MB) |
| Container | MP4 |

Verificación:
```bash
ffprobe -v error -show_entries stream=codec_name,profile,r_frame_rate,sample_rate,width,height -of default=nw=1 render.mp4
```

---

## Reglas heredadas

### 🌐 Universal (todas aplican)
- `CAPTIONS.md` § Whisper-sync hard rule — caption visible desde primer frame audible
- `ELEMENTS-LIBRARY.md` § Drop shadow text legibility — 4 strokes + glow para texto sobre IA images
- `PIPELINE.md` § Preset filter principle — el genre define el preset CSS canónico
- `CHARACTER-CONSISTENCY.md` § Bootstrap gate — anchor por personaje antes de generar escenas
- `video-animation/ANIMATION-LAYER.md` § Duration matching tier 5s/10s

### 📱 Vertical short-form (todas aplican)
- `RETENTION-RULES.md` (completa) — hook 2-3s, intro ≤10%, cero estáticas first 30s, UI safe zones
- `ANIMATION-LAYER.md` § PRE-GATE — `data-start < 30s` requiere Kling, no Ken Burns

### 🎬 Format-specific
Ver sección "Específico Reel" abajo.

---

## Específico Reel

### Hook en primeros 2-3s
**Scope**: 📱 Reel/TikTok/IG Reel

El swipe-away decisivo ocurre entre el segundo 1 y 3. Antes del segundo 3 el viewer debe:
1. Ver una imagen atmosférica que NO sea "explicación textual" (hook visual)
2. Leer un caption que confirme "hay audio + hay narrativa interactiva"
3. Sentir que algo va a pasar (movimiento de cámara, sonido in)

**Patrones validados**:
- Teaser empty location + ominous element + Kling end_image materialize (validado horror-choice v15)
- Cold open con accion in-progress (sin intro)
- Pregunta directa a cámara con sonido in inmediato

### Intro ≤10% del total
**Scope**: 📱

| Duración total | Intro máx |
|---|---|
| 30s | 3s |
| 60s | 6s |
| 90s | 9s |
| 120s | 12s |

Hold de presentación de personajes (si aplica) no debe exceder el 10%.

### UI Safe Zones — Instagram

**Scope**: 📱 IG Reels específicamente (TikTok tiene zonas distintas pero estos valores son seguros para ambos).

```css
/* Zonas seguras para texto/UI sobre el frame 1080×1920 */
.caption-wrap {
  bottom: 540px;    /* arriba de descripción/comentarios IG */
  height: 280px;
  z-index: 70;
}
.loading-bar-wrap {
  bottom: 700px;    /* arriba de description */
}
.name-label {
  top: 220px;       /* debajo de header IG */
}
#end-cta {
  bottom: 540px;    /* mismo nivel que captions */
}
```

**Zonas a EVITAR**:
- `bottom: 0-540px` → tapado por description + comments + music sticker + like button
- `top: 0-200px` → tapado por header del usuario + audio name
- `right: 0-200px` → tapado por columna de actions (like, comment, share, save)

### Caption sizing

**Scope**: 📱

| Tipo | Font-size | Por qué |
|---|---|---|
| Caption narrador | 80px Anton | Legible en mobile a brazo extendido |
| Caption secundaria (dialogue, italic) | 64px | Diferencia visual del narrador |
| Caption emphasis (CTA, key moment) | 90-110px | Llama el ojo |
| Label personajes | 60-72px | Sub-elemento, no compite con captions |
| Countdown digit | 400px Anton | Llena el viewport vertical |

### Música y SFX

**Scope**: 📱

Volume canónico (heredado de PIPELINE.md):
- Narrador: 1.0
- Música: 0.05-0.18 (depende del momento — alta en climax, baja durante narrador)
- SFX puntuales (flash impact, thud, exhale): 0.40-0.65
- Ambient continuo: 0.10-0.18

**Regla**: Reel está diseñado para autoplay con AUDIO. Pero hay que asegurar que la narrativa se entienda **sin audio** vía captions. Si quitar la voz rompe la comprensión, los captions están mal hechos.

---

## Anti-patterns específicos Reel

### ❌ Intro de >10s sin hook visual

**Por qué falla**: scroll-away garantizado. Reels tiene la barra más impaciente de scroll.

**Fix**: hook visual + caption < 3s. Si necesitas más tiempo, comprime.

### ❌ Caption-wrap en `bottom: 0` o `bottom: <540px`

**Por qué falla**: tapado por UI de IG. Caption invisible para usuario.

**Fix**: `bottom: 540px` mínimo. Verificar en mockup IG real.

### ❌ Render en 16:9 con padding letterbox para "convertir a 9:16"

**Por qué falla**: el algoritmo de IG penaliza videos con bandas negras. Pixel real = 1080×1920 sin letterbox.

**Fix**: render nativo 9:16 desde el inicio. Si la fuente es 16:9, recortar o regenerar.

### ❌ Imágenes estáticas >2s en primeros 30s

**Por qué falla**: PRE-GATE de retención. Cualquier "diapositiva" en esta ventana baja retention rate del 70% al 40%.

**Fix**: animar con Kling (heredado de `ANIMATION-LAYER.md`).

---

## QA específico Reel

Además del `QA.md` universal, agregar al prompt Gemini:

```
Dimensiones específicas Reel:
- ¿El hook en primeros 3s es suficientemente fuerte para detener el scroll?
- ¿La narrativa se entiende sin audio? (sound-off scrollers son ~60%)
- ¿Hay elementos visuales tapados por UI de IG (bottom: 0-540px, right: 0-200px)?
- ¿La duración total está en sweet spot 60-90s o muy corto/largo?
- ¿El último frame (cliffhanger / CTA) invita a comentar/compartir?
```

---

## Casos producidos

| Proyecto | Combo | Score Gemini | Path |
|---|---|---|---|
| mina-abandonada v15-final ⭐ | horror-choice × reel | 9.9/10 | `renders/v15-final.mp4` |

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- `RETENTION-RULES.md` — reglas de retención short-form
- `formats/instagram-story.md` — formato hermano (más corto, más interactivo)
- `formats/youtube-short.md` — formato hermano (sin UI de IG, algoritmo distinto)
