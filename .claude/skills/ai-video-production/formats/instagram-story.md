# formats/instagram-story.md — Instagram / Facebook Stories

> Delivery format vertical short-short. 15s/segmento, descartable, interactividad nativa.

---

## Specs técnicos

| Atributo | Valor |
|---|---|
| Aspect ratio | 9:16 |
| Resolución | 1080 × 1920 |
| FPS | 30 |
| Codec video | H.264 High profile, yuv420p |
| Codec audio | AAC-LC stereo, 48000Hz |
| Bitrate video | 3-5 Mbps |
| Duración | ≤ 15s por segmento (IG corta automáticamente). Series de varios segmentos OK. |
| Tamaño máx | <100 MB |
| Container | MP4 |

---

## Reglas heredadas

### 🌐 Universal
- `CAPTIONS.md` § Whisper-sync — sound-off scrollers existen
- `ELEMENTS-LIBRARY.md` § Drop shadow
- `PIPELINE.md` § Preset filter

### 📱 Vertical short-form (modificadas — duración menor)
- ✅ Hook EXTREMO en primeros 1-2s (más agresivo que Reel)
- ❌ "Intro ≤10%" — irrelevante a 15s, todo es intro
- ✅ "Cero estáticas" — aplica a todos los 15s (no solo first 30s)
- ✅ UI safe zones IG (similar a Reel pero más restrictivas)

### 🎬 Format-specific
Ver sección abajo.

---

## Específico Instagram Story

### Duración: 15s hard cap por segmento
**Scope**: 📱 Story

Stories de >15s se cortan automáticamente. Hay 2 estrategias:

| Estrategia | Cuándo usarla |
|---|---|
| **Single 15s** | Mensaje único, ad simple, teaser |
| **Multi-segment** | Narrativa más larga, 2-5 stories en secuencia (cada una 15s) |

### Story sticker interactivos (la innovación del formato)
**Scope**: 📱 Story específicamente

Stories permite agregar stickers interactivos POR ENCIMA del video después del upload:
- **Poll**: A vs B (2 opciones)
- **Quiz**: 4 opciones, una correcta
- **Slider**: scale 0-100 (emoji slider)
- **Question**: text input
- **Countdown**: para un drop / launch
- **Link**: para CTA externo

**Anti-pattern**: simular stickers HARDCODED en el video. NO funciona, deja al usuario CON los stickers nativos.

**Pattern correcto**: dejar espacio vacío donde irán los stickers (típicamente bottom 1/3 o center).

```css
/* Reservar zona para stickers post-upload */
.sticker-zone {
  position: absolute;
  bottom: 600px;    /* zona donde típicamente van stickers */
  height: 600px;
  width: 100%;
  /* NO poner contenido aquí */
}
```

### Hook 1-2s, no 3s
**Scope**: 📱 Story

Stories tienen tap-to-skip-forward. El thumb está ENCIMA del screen, listo para skip. Hook debe ser inmediato:
- Primer frame: imagen impactante (no fade-in)
- Audio in inmediato (no silencio inicial)
- Caption visible en frame 0

### Tap forward / tap back
**Scope**: 📱 Story

Tap-derecha-superior = skip al siguiente segmento. Tap-izquierda-superior = back.
- **No info crítica en bordes top** (~250px) — área de tap
- **Skip rate alto**: si tu segmento aburre en los primeros 2s, swipe out

### Captions en Stories

**Scope**: 📱 Story

Posición preferida: **centro vertical** o **arriba** (no bottom):
- Bottom típicamente reserved para stickers / responses
- Center = máxima visibilidad
- Tamaño: 70-90px (más grande que Reel porque viewing time es menor)

```css
.story-caption {
  position: absolute;
  top: 700px;     /* centro vertical aprox (1920/2 + margen) */
  font-size: 80px;
  /* ... drop shadow + stroke ... */
}
```

### Music: limited catalog
**Scope**: 📱 Story

IG Stories tiene catálogo de música más limitado que Reels (subset). Verificar antes de seleccionar.

---

## UI Safe Zones — Instagram Stories

```css
/* Zonas safe para texto/UI sobre 1080×1920 Story */
.story-safe-top    { top: 240px; }      /* debajo de header username + close X */
.story-safe-bottom { bottom: 250px; }   /* arriba de reply text input + reactions */
.story-safe-zones {
  /* No text en bordes top 240px ni bottom 250px */
  /* Center vertical = safest */
}
```

**Zonas a EVITAR**:
- `top: 0-240px` → tapa con header (username, close button, ad indicator si sponsored)
- `bottom: 0-250px` → reply box + reactions row
- Lados izquierdo/derecho top → swipe-up/down indicators (en algunas versiones)

---

## Multi-segment stories

Para narrativa más larga que 15s, planear segmentos como mini-cliffhangers:

```
Story 1 (15s)   HOOK + setup
                Último frame: TBC → siguiente
Story 2 (15s)   Develop + reveal parcial
                Último frame: cliffhanger → siguiente
Story 3 (15s)   Climax / payoff
                CTA + link sticker
```

**Regla**: cada segmento debe ser **autocontenido** lo suficiente para que el viewer que se une en story #2 no se sienta perdido, pero debe **incentivar** ir a la siguiente.

---

## Anti-patterns específicos Story

### ❌ Story de >15s (esperando que IG lo trim)

**Por qué falla**: IG corta a los 15s exactos sin warning, perdés el final.

**Fix**: editar a 14.5s exactos, leave breathing room.

### ❌ Contenido crítico en `bottom: 0-250px`

**Por qué falla**: tapado por reply box / reactions. Invisible.

**Fix**: contenido crítico en center vertical o arriba (después del header zone).

### ❌ Stickers HARDCODED simulados en el video

**Por qué falla**: viewer cree que son interactivos. No lo son. Mal UX.

**Fix**: dejar zona vacía, agregar stickers nativos post-upload.

### ❌ Hook lento (fade-in de 1s+)

**Por qué falla**: viewer skip-forward antes de que cargue el hook.

**Fix**: primer frame ya con visual impactante. Sin fade-in.

---

## QA específico Story

```
Dimensiones específicas Instagram Story:
- ¿Duración exacta ≤14.5s (no cortado por IG)?
- ¿Hook visual en frame 0 (sin fade-in lento)?
- ¿Hay zona vacía planeada para stickers post-upload?
- ¿Captions en center o arriba (no bottom)?
- ¿Contenido crítico fuera de top: 0-240px y bottom: 0-250px?
- ¿Si es multi-segment, cada uno termina en cliffhanger / incentive al siguiente?
```

---

## Casos producidos

(ninguno aún)

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- `formats/reel.md` — formato hermano (más largo, menos interactivo nativo)
