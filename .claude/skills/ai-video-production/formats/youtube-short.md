# formats/youtube-short.md — YouTube Shorts

> Delivery format vertical short-form de YouTube. Hermano del Reel pero con métricas y UI distintas.

---

## Specs técnicos

| Atributo | Valor |
|---|---|
| Aspect ratio | 9:16 |
| Resolución | 1080 × 1920 (mínimo) o 2160 × 3840 (4K para más reach algo) |
| FPS | 30 o 60 |
| Codec video | H.264 High profile, yuv420p (o H.265 HEVC para 4K) |
| Codec audio | AAC-LC stereo, 48000Hz |
| Bitrate video | 4-8 Mbps (YT recompresa fuerte, dar margen) |
| Duración | ≤ 60s (hard cap de YT) |
| Tamaño máx | 256 GB técnicamente, target <100 MB |
| Container | MP4 |

---

## Reglas heredadas

### 🌐 Universal
- Idénticas a `reel.md`

### 📱 Vertical short-form
- Idénticas a `reel.md`

### 🎬 Format-specific
Ver sección "Específico YouTube Shorts" abajo.

---

## Diferencias clave vs Reel

| Aspecto | Reel | YouTube Short |
|---|---|---|
| Duración máx | 90s recomendado, 180s teórico | **60s hard cap** |
| Audio nativo | Música del catálogo IG OK | Música licensed OK pero menos catálogo |
| UI safe zones | Bottom 540px + right 200px IG | Bottom ~300px (subscribe button) + right ~200px (likes) |
| Algoritmo | Hook agresivo 1-2s | Hook puede ser menos agresivo (público está EN YT) |
| Re-watch loop | Importante (loop visible) | **Crítico** (loops = views) |
| Cliffhanger CTA | "Comenta A o B" | "Mira el video completo" (link al long-form) |
| Captions burned-in | Necesario | Opcional (YT tiene auto-captions buenas, pero burned-in da más control) |

---

## Específico YouTube Shorts

### Hook timing
**Scope**: 📱

YT Shorts viewer está más "investing" que IG/TikTok viewer (vino a YT explícitamente). Hook puede ser 3-5s, no necesariamente 1-2s.

Pero el **bounce a los 3-5s** es alto. Hook debe terminar antes del 5s o tener clear forward motion.

### Duración: 30-50s sweet spot (no 60s)
**Scope**: 📱 YT Shorts

Aunque el cap es 60s, los Shorts que **mejor retention rate** tienen son 30-50s. Razón: completion rate >80% es señal de calidad para el algoritmo. Un Short de 50s con 90% completion bate a uno de 60s con 70%.

**Recomendación**: target 40-50s para nuevos Shorts a menos que la narrativa REQUIERA más.

### Loop final (re-watch trigger)
**Scope**: 📱 YT Shorts específicamente

YT Shorts auto-loopea. Diseñar el último frame para que conecte con el primero:
- Visualmente similar (mismo encuadre o composición)
- Audio termina en silence o fade-out (no en climax)
- Caption final invita a re-mirar (ej: "¿Lo viste?" → encadena con primer frame)

Esto es **menos crítico en Reel** porque IG auto-loopea pero el espectador suele scrollear.

### UI Safe Zones — YouTube Shorts

```css
.caption-wrap {
  bottom: 380px;    /* arriba de "Suscribe" button + columna right actions */
  height: 280px;
  z-index: 70;
}
.loading-bar-wrap {
  bottom: 600px;
}
.name-label {
  top: 180px;       /* debajo de canal name + ... menu */
}
```

**Zonas a EVITAR**:
- `bottom: 0-380px` → tapado por título + descripción + comentarios + subscribe button
- `right: 0-180px` → like / dislike / comments / share / remix
- `top: 0-150px` → header con canal + menú overflow

---

## Anti-patterns específicos YT Shorts

### ❌ Duración exactamente 60s

**Por qué falla**: completion rate cae al borde del cap. Mejor 50-55s.

### ❌ Música del catálogo IG (no licensed para YT)

**Por qué falla**: YT bloquea / desmonetiza por copyright.

**Fix**: usar YouTube Audio Library o música original/licensed para YT.

### ❌ CTA "comenta A o B" sin contexto

**Por qué falla**: en YT el viewer suele venir de search/feed, no de algoritmo interactivo. "Comenta" funciona menos.

**Fix**: CTA tipo "¿Quieres más? Mira el video completo en mi canal" o link al long-form en pinned comment.

---

## QA específico YT Shorts

Agregar al prompt Gemini:

```
Dimensiones específicas YouTube Short:
- ¿Loop final está bien diseñado (último frame encadena visualmente con primero)?
- ¿Duración en sweet spot 30-50s o cerca del cap 60s (penalizado)?
- ¿Hay elementos tapados por UI de YT (bottom 380px, right 180px)?
- ¿CTA es apropiado para audiencia de YouTube (no "comenta A/B" sin contexto)?
```

---

## Casos producidos

(ninguno aún)

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- `RETENTION-RULES.md` — reglas universales short-form
- `formats/reel.md` — formato hermano (más viral, menos completion-rate-focus)
