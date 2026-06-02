# CAPTIONS.md — Captions sincronizados automáticamente con Whisper

> Nunca escribir timings de captions a mano. Siempre auto-generar desde el audio con Whisper. Los timings manuales SIEMPRE se desincronizan eventualmente.

---

## ⛔ HARD RULE — Whisper-sync caption desde primer frame audible

**Scope**: 🌐 **Universal** — aplica a CUALQUIER video con voz humana o TTS, cualquier delivery format, cualquier duración, cualquier plataforma.

### La regla

**TODA narración (humana o TTS) que aparezca en el video DEBE tener su caption Whisper-sincronizado visible desde el primer frame audible de ese audio.**

Sin excepciones. Aplica a:
- Reel viral horror con narrador omnisciente
- B2B commercial con voz corporativa
- Tutorial con instructor hablando
- Documental con voiceover
- Testimonial con persona en cámara
- Ad de 15s con tagline hablado
- Series long-form de YouTube

### Por qué es universal (no solo short-form)

| Plataforma | % viewers sound-off | Razón |
|---|---|---|
| Instagram Reels / TikTok | ~60-75% | Autoplay muted por default, scrolling público |
| LinkedIn | ~80%+ | Autoplay muted, contexto oficina |
| YouTube Shorts | ~40-50% | Mejor que IG pero significativo |
| YouTube Long | ~20-30% | Segundo monitor, biblioteca, multitasking |
| TV/CTV ads | ~30%+ | Salas con gente, kids, etc. |
| Web embed | ~70%+ | Autoplay muted forzado por browsers |

**En TODAS las plataformas, ≥20% de tu audiencia ve sin audio**. Sin captions, ese 20%+ no entiende qué pasa → bounce inmediato.

### Cómo implementarlo (resumen)

```bash
# Para CADA audio de narración (no SFX) en el proyecto:
.venv/bin/python scripts/captions.py \
  -a assets/<narration-audio>.mp3 \
  -t <offset-en-timeline-segundos> \
  -e <prefijo-caption-id>
```

Output: `tl.set()` calls + HTML elements listos para pegar en `index.html`.

### Anti-pattern crítico

❌ **"Es solo el intro / es solo 5s / la gente ya tiene audio activado"** — todos son falsos. El intro es DONDE más importa (sound-off scrollers necesitan saber que hay audio antes de unmute). Los 5s son SUFICIENTES para perder a alguien. Y la gente NO tiene audio activado por default en ninguna plataforma.

❌ **Auto-captions de YouTube/IG en lugar de burned-in** — opcionales como complemento, pero NO sustitutos. Razones:
- No están sincronizados como burned-in
- Pueden estar desactivados
- En cross-posting (subir el mismo video a múltiples plataformas), no se transfieren
- Errores de transcripción son visibles al espectador

**Fix**: caption burned-in vía Whisper + GSAP innerHTML changes. El auto-caption de la plataforma es complemento opcional.

### Caso de estudio — mina-abandonada v15

El h1-narr (audio 0-4.71s) NO tenía Whisper-caption en el primer pass de v15. El usuario lo notó: *"porque no hay captions en el 'elige a tu compañero...' al inicio? es clave si un usuario no tiene audio aun y ve el video en reel, así entiendo que tiene audio y le pone el sonido"*.

Fix aplicado: Whisper sobre h1-narr-2x.mp3 → 3 frases progresivas para caption-h1-narr. Aparece desde el segundo 0.1s.

**Lección codificada acá**: incluso en proyectos donde "el narrador externo es obvio", agregar el caption es no-negociable.

---

## Por qué auto-generar (timings)

En bosque-abandonado v1 los captions se hand-timed y se desfasaron visiblemente de la narración. Whisper genera timestamps a nivel de palabra desde el audio TTS-procesado-a-2x, garantizando sincronía 100%.

---

## Comando

```bash
.venv/bin/python scripts/captions.py \
  -a assets/h3-narr1-2x.mp3 \
  -t 22.7 \
  -e h3-cap-narr1
```

- `-a` — archivo de audio (después de atempo 2x, no el raw)
- `-t` — offset del audio en la timeline del video (data-start)
- `-e` — prefijo para los IDs de los elementos GSAP

### Output

Imprime una serie de llamadas `tl.set()` listas para pegar en el `<script>` de `index.html`:

```js
tl.set("#h3-cap-narr1-0", { opacity: 1 }, 22.7);
tl.set("#h3-cap-narr1-0", { opacity: 0 }, 23.4);
tl.set("#h3-cap-narr1-1", { opacity: 1 }, 23.4);
tl.set("#h3-cap-narr1-1", { opacity: 0 }, 24.1);
...
```

Y el HTML correspondiente:

```html
<div id="h3-cap-narr1-0" class="caption caption-abs" style="opacity:0;">SI ELEGISTE A BERNI</div>
<div id="h3-cap-narr1-1" class="caption caption-abs" style="opacity:0;">LLEVA AÑOS</div>
...
```

---

## Batch mode

Para procesar todos los audios de un video en una sola corrida:

```bash
.venv/bin/python scripts/captions.py --spec captions-spec.json
```

Formato de `captions-spec.json`:

```json
[
  {"audio": "assets/h1-narr-2x.mp3", "start": 1.0, "prefix": "h1-cap"},
  {"audio": "assets/h3-narr1-2x.mp3", "start": 22.7, "prefix": "h3-cap-narr1"},
  {"audio": "assets/h3-narr2-2x.mp3", "start": 25.5, "prefix": "h3-cap-narr2"},
  ...
]
```

---

## Dependencia

```bash
.venv/bin/pip install openai-whisper
```

Primera ejecución descarga el modelo Whisper (~150MB). Subsecuentes son instantáneas.

---

## CSS obligatorio para captions

```css
.caption {
  font-size: 80px;
  font-family: "Anton", "Bebas Neue", "Impact", sans-serif;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: #ffffff;
  text-shadow:
    -2px -2px 0 rgba(0,0,0,0.85), 2px -2px 0 rgba(0,0,0,0.85),
    -2px  2px 0 rgba(0,0,0,0.85), 2px  2px 0 rgba(0,0,0,0.85),
    0 4px 10px rgba(0,0,0,1);
  -webkit-text-stroke: 1.5px rgba(0,0,0,0.7);  /* obligatorio */
  white-space: normal;                          /* obligatorio — sin esto se cortan */
  width: 960px;
  text-align: center;
  line-height: 1.15;
  opacity: 0;
  will-change: opacity;
}

.caption-abs { position: absolute; }
.caption-sm  { font-size: 68px; }  /* para frases largas */
```

Para frases >8 palabras, agregar `caption-sm` o inline `style="font-size:68px"`.

---

## Posicionamiento (Instagram safe zones)

Los captions deben estar dentro de la zona segura para evitar que Instagram los tape con su UI:

```css
.caption-wrap {
  position: absolute;
  bottom: 540px;       /* deja espacio para la UI inferior */
  left: 0; right: 0;
  height: 280px;
  display: flex; align-items: center; justify-content: center;
  z-index: 70; pointer-events: none;
}
```

Zonas reservadas en Instagram (no poner texto):
- Top: y = 0–270
- Bottom: y = 1380–1920
- Right: x = 840–1080

Zona segura: x 60–840, y 270–1380.

---

## Workflow recomendado

1. **Generar todos los audios TTS** y aplicar atempo 2x (ver `PIPELINE.md` §1)
2. **Medir duraciones** con ffprobe
3. **Calcular `data-start`** real de cada bloque de narración en el video
4. **Crear `captions-spec.json`** con audio + start + prefix por bloque
5. **Ejecutar batch** `scripts/captions.py --spec captions-spec.json`
6. **Copiar el output** (HTML + GSAP) al `index.html`
7. **Verificar visualmente** los captions tras el primer render (Whisper acierta ~95%, ocasionalmente hay que corregir un timing)

---

## Anti-patterns

- ❌ **Hand-timing captions** — eventualmente se desfasan, especialmente tras regenerar audio
- ❌ **Usar Whisper sobre el raw TTS** — los timestamps van a estar en velocidad 1x, no 2x
- ❌ **Saltarse el offset `-t`** — los timestamps salen relativos al audio, no al video
- ❌ **Captions con `white-space: nowrap`** — frases largas se cortan fuera de pantalla
- ❌ **Dejar los `opacity: 0` intermedios entre segmentos de Whisper** — produce gaps visibles donde la pantalla queda sin caption durante 0.3-0.6s entre cada frase. Aprendizaje mina-abandonada v3→v4 (2026-05-10).

## Post-procesar el output de Whisper — IMPORTANTE

El script `captions.py` produce un patrón:
```js
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 1" }, 1.0);
tl.set("#cap-X", { opacity: 0 }, 2.0);   // <-- ANTI-PATRÓN
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 2" }, 2.5);
tl.set("#cap-X", { opacity: 0 }, 3.5);   // <-- ANTI-PATRÓN
```

Los `opacity: 0` intermedios crean GAPS (0.3-0.6s entre cada frase donde no hay caption). El espectador percibe que "los captions fallan" o "el video se queda sin texto".

**Fix obligatorio**: eliminar los `opacity: 0` intermedios, dejar solo el ÚLTIMO `opacity: 0` por cada elemento (cierre de la narración antes de pasar al siguiente audio).

## Anti-patrón crítico — OVERLAP entre captions Whisper y separadores V7-3 / puente V7-4

**Aprendizaje mina-abandonada v4→v5 (2026-05-10):** una vez que las captions Whisper se mantienen visibles toda la narración (sin gaps), pueden **overlapear con los elementos separadores del formato horror-choice**:

- **V7-3 separadores** (`cap-h3-branch`, `cap-h4-branch` con texto "SI [opción B]:" en azul `#c8d8ff`) — están en la misma `.caption-wrap` que las Whisper captions y aparecen ENCIMA del caption activo.
- **V7-4 puente** (`h5-bridge` con "Y SI HUBIERAS ELEGIDO A [BUENO]..." en dorado `#f5d9a0`) — mismo problema.

**Verificado visualmente en frames extraídos**:
- v4 a 43s mostraba "EL SUELO. OSCURIDAD. NO HAY MAÑANA." + "SI NO RESPIRAS:" superpuestos
- v4 a 70.5s mostraba "CAES AL POZO." + "SI IGNORAS:" superpuestos
- v4 a 84s mostraba "LOGRASTE SALIR." + "Y SI HUBIERAS ELEGIDO A SANTI..." superpuestos

### Fix obligatorio — uno de los dos:

**Opción A (preferida en formato horror-choice): eliminar los separadores V7-3 de texto**

Las captions Whisper ya incluyen "SI [opción B]:" como prefijo natural del audio (ej: "SI NO RESPIRAS: PASAS LA ZONA."). El separador V7-3 textual es redundante.

Mantener SOLO el **pulso visual `#fade-out`** (el oscurecimiento sutil) sin el caption de texto azul:

```js
/* Separador V7-3 — solo pulso #fade-out, sin texto */
tl.to("#fade-out", { opacity: 0.5, duration: 0.25, ease: "power2.inOut" }, T);
tl.to("#fade-out", { opacity: 0,    duration: 0.25, ease: "power2.out"   }, T + 0.25);
/* NO incluir tl.set("#cap-h3-branch", { opacity: 1 }) */
```

Y remover los `<div id="cap-X-branch">` del HTML (o dejarlos con `display:none`).

**Opción B: hide explícito de la Whisper caption durante el separador/puente**

Si querés mantener el texto del separador V7-3 (para formatos no-horror-choice), agregar hide explícito:

```js
/* Antes del separador */
tl.set("#cap-h3-n4", { opacity: 0 }, 42.8);  // hide Whisper caption
tl.set("#cap-h3-branch", { opacity: 1 }, 42.8);  // show separator
tl.set("#cap-h3-branch", { opacity: 0 }, 44.0);
/* La próxima innerHTML de cap-h3-n4 a 44.32 restaurará opacity:1 automáticamente */
```

**Para el V7-4 puente (h5-bridge)**: SIEMPRE aplicar hide explícito al Whisper caption del Hito 5, porque el puente es esencial al formato y debe ser visible solo (sin overlap).

### Validación frame-by-frame post-fix

Después de cada cambio de captions, extraer frames del render en los momentos críticos:

```bash
for t in 42.5 43 43.5 44 69 70 70.5 71 71.5 83 83.5 84 84.5; do
  ffmpeg -y -ss $t -i renders/draft.mp4 -frames:v 1 -q:v 2 renders/debug/frame-${t}s.jpg
done
```

Leer cada frame y confirmar que SOLO un caption está visible. Gemini Video Analyzer NO detecta este tipo de overlap de manera consistente — la verificación humana (o con frames) es necesaria.

```js
// CORRECTO — caption queda visible toda la narración, solo cambia innerHTML
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 1" }, 1.0);
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 2" }, 2.5);  // innerHTML cambia, opacity sigue 1
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 3" }, 4.0);
tl.set("#cap-X", { opacity: 0 }, 5.5);  // SOLO el último opacity 0 — cierre del audio
```

Script Python para procesar el output de `captions.py`:

```python
import re
from pathlib import Path

text = Path("index.html").read_text()
caption_block_re = re.compile(
    r'(/\* captions for #(cap-[\w-]+) \(offset=[\d.]+s\) \*/\s*\n'
    r'(?:\s*tl\.set\("#\2"[^\n]*\n)+)',
    re.MULTILINE
)

def process_block(match):
    block = match.group(0)
    lines = block.split('\n')
    header = lines[0]
    body_lines = [l for l in lines[1:] if l.strip()]
    inner_lines = []
    last_opacity_0 = None
    for line in body_lines:
        if 'innerHTML' in line:
            inner_lines.append(line)
        else:
            last_opacity_0 = line  # always overwrite — keep only the last
    out_lines = [header] + inner_lines
    if last_opacity_0:
        out_lines.append(last_opacity_0)
    return '\n'.join(out_lines) + '\n'

Path("index.html").write_text(caption_block_re.sub(process_block, text))
```

Validación post-fix: extraer frames a 1s de intervalo del render. Cada frame en el rango de una narración DEBE tener un caption visible. Si algún frame queda en blanco entre dos narraciones consecutivas, todavía hay un gap.

---

## Sistema de 3 clases — validado contra 7 referentes (2026-05-13)

> **🎯 SCOPE:** Las 3 clases son específicas de **F1 (Horror choice narrativo)**. Solo el "drop shadow > thick stroke" universal aplica a todos los formatos. Ver `FORMAT-DETECTION.md` antes de aplicar.

**Hallazgo empírico:** análisis de Gemini Vision sobre 35 keyframes + Gemini full-video sobre 7 referentes (4 de @referent-a) revela que el sistema de UNA clase de caption (Anton/Bebas + thick stroke) NO coincide con la práctica profesional. Los referentes F1 usan **3 clases distintas** según rol narrativo, y **drop shadow en lugar de stroke** (este último es 🌐 universal).

### NUEVO 2026-05-13 PM (post Gemini full-video) — Inline keyword highlighting

Gemini detectó que @referent-a usa **highlighting INLINE de palabras clave** dentro de la caption blanca: una palabra crítica del enunciado cambia a rojo/amarillo. Diferencia técnica importante respecto a `caption-warning` (frase entera roja):

```html
<!-- Antes (codificado v1): caption entera roja -->
<div class="caption-warning">NO CONFÍES EN ÉL</div>

<!-- Pattern real (validado v2): inline highlight -->
<div class="caption-narration">
  Bruno saca un <span class="kw-red">medidor de gas</span> y lo pone frente a tu cara
</div>
```

```css
.kw-red {
  color: #FF3030;
  text-shadow:
    0 0 6px rgba(255,0,0,0.8),
    0 0 14px rgba(255,0,0,0.4);
}
.kw-amber {
  color: #FFCC00;
  text-shadow: 0 0 6px rgba(255,200,0,0.6);
}
```

Aplicar inline keyword highlight para:
- Sustantivos de peligro: "taladro", "dinamita", "alarma", "trampa"
- Verbos críticos: "muere", "cae", "escapa"
- Phrases de impacto: "NO CONFÍES", "ÚLTIMA OPORTUNIDAD"

### Las 3 clases

#### `.caption-name` — nombres de personajes (archetype anchors)

Para introducir personajes-archetype. Universal en @referent-a ("BRUNO", "PABLO", "ENZO", "AXEL").

```css
.caption-name {
  font-family: "VT323", "Space Mono", "IBM Plex Mono", "Courier New", monospace;
  font-weight: 700;
  font-size: 110px;
  color: #FFFFFF;
  letter-spacing: 0.05em;
  text-shadow:
    0 0 8px rgba(0,0,0,0.7),
    0 4px 8px rgba(0,0,0,0.5);
  text-transform: uppercase;
  /* NO -webkit-text-stroke — drop shadow only */
  white-space: normal;
  text-align: center;
  opacity: 0;
  will-change: opacity, transform;
}
```

**Por qué monospaced:** retro-gaming/consola aesthetic. Anchor visual del archetype. Diferencia visual fuerte entre "el nombre" y "la narración".

#### `.caption-narration` — narración/instrucciones/decisiones

Hereda mucho de `.caption` actual pero **sin thick stroke**, **con drop shadow blur**.

```css
.caption-narration {
  font-family: "Montserrat", "SF Pro Display", "Anton", sans-serif;
  font-weight: 900;
  font-size: 78px;
  color: #FFFFFF;
  text-shadow:
    0 0 12px rgba(0,0,0,0.6),
    0 6px 14px rgba(0,0,0,0.5);
  text-transform: uppercase;
  letter-spacing: 0.02em;
  /* NO -webkit-text-stroke — drop shadow only */
  white-space: normal;
  width: 960px;
  text-align: center;
  line-height: 1.15;
  opacity: 0;
  will-change: opacity;
}
```

#### `.caption-warning` — texto ominoso/advertencia rojo

Para frases como "NO CONFÍES EN ÉL", "ESTÁS SOLO", "NO HAY VUELTA ATRÁS". Universal en horror narrativo.

```css
.caption-warning {
  font-family: "Montserrat", "Anton", sans-serif;
  font-weight: 900;
  font-size: 90px;
  color: #FF0000;
  text-shadow:
    0 0 8px #FF0000,
    0 0 16px rgba(255,0,0,0.6),
    0 0 24px rgba(255,0,0,0.4),
    0 4px 8px rgba(0,0,0,0.7);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  /* glow halo via text-shadow chain */
  white-space: normal;
  text-align: center;
  opacity: 0;
  will-change: opacity, transform;
}
```

### Cuándo usar cada una

| Clase | Rol | Posición Y | Animación recomendada |
|-------|-----|------------|------------------------|
| `caption-name` | Anchor archetype (1-2 palabras) | Top-of-character (Y ~25%) o top-right | scale pop + fade in |
| `caption-narration` | Story progression, instrucciones | Y ~65% (tercio inferior) | innerHTML swap (Whisper sync) |
| `caption-warning` | Frases ominosas, twist reveal | Y central (Y ~50%) | scale pop dramatic + glow pulse |

### ⛔ Per-speaker Y-band — NUNCA 2 cues concurrentes al mismo Y (cross-layer incluido)

**Narrador (Layer 3) = Y62** (banda canónica del tercio inferior). **Diálogo de personaje (Layer 1) = Y52 + tag del nombre** ("BRUNO:" / "CELESTE:"), banda distinta para que el viewer sepa quién habla.

**Regla dura**: ningún par de cues de caption que se solapen en TIEMPO puede compartir banda Y. Esto incluye **el cross-layer narrador-L3 + diálogo-L1** (no solo dos narraciones, ni solo dos personajes). El burn DEBE de-conflictar en build-time: si dos cues solapados caen en el mismo Y → offset automático del cue más tardío hacia arriba (≥6% = ≥1 alto de línea de separación). Si 2 personajes hablan concurrentes → Y distintos con ≥6% de separación (o secuenciar).

**Por qué importa**: el bug CAPTION-OVERLAP (invernadero V6) usaba `base_pct=0.62` para TODOS los speakers → narrador y diálogo concurrentes se sobreponían en Y62. El check "no same-Y overlap" existía en el audit (sidecar JSON) pero NO se enforzaba en el burn ni cubría el cross-layer narrador+diálogo. Fix codificado en `cp5b_build_atomic.py` (`deconflict_cue_ys`) + portado al template `build_clip_atomic.py`.

### Por qué drop shadow > thick stroke

**Comparativa visual:**
- Thick stroke (12px) → look "amateur", outline obvio, año-2010 capcut style
- Drop shadow blur → look "cinematic", el texto se separa SUTILMENTE del fondo, año-2025 pro

**Evidencia:** 7/7 referentes usan drop shadow. CERO usan thick stroke. @referent-a (4/7) lo usa consistentemente.

**Excepción:** si el fondo es EXTREMADAMENTE complejo (full white, multiple colors), un stroke negro de 2-3px adicional al drop shadow puede ayudar legibilidad. Pero el stroke NO es el efecto principal.

### Animaciones recomendadas

```javascript
// caption-name — scale pop entrance
tl.fromTo("#bruno-name",
  { opacity: 0, scale: 0.6 },
  { opacity: 1, scale: 1.0, duration: 0.4, ease: "back.out(2)" },
  T);

// caption-warning — scale pop + glow pulse
tl.fromTo("#warning-1",
  { opacity: 0, scale: 0.8 },
  { opacity: 1, scale: 1.0, duration: 0.3, ease: "power3.out" },
  T)
  .to("#warning-1",
    { textShadow: "0 0 16px #FF0000, 0 0 32px rgba(255,0,0,0.9)", duration: 0.3, yoyo: true, repeat: 3 },
    T + 0.4);

// caption-narration — innerHTML swap (Whisper-sync, sin animation)
tl.set("#narr-1", { opacity: 1, innerHTML: "FRASE 1" }, T);
tl.set("#narr-1", { opacity: 1, innerHTML: "FRASE 2" }, T + 1.5);
tl.set("#narr-1", { opacity: 0 }, T + duration);
```

### Backward compatibility

La clase `.caption` original sigue siendo válida (Whisper-sync narration legacy). El sistema de 3 clases es **aditivo**, no reemplaza. Para videos nuevos, preferir `caption-narration`. Para legacy, mantener `caption`.

### Coexistencia con safe zones de Instagram

Las 3 clases respetan las safe zones (top 0-270, bottom 1380-1920, right 840-1080). El `caption-name` típicamente cerca de Y=25% (top-of-character, dentro del safe), `caption-narration` Y=65% (tercio inferior, dentro del safe), `caption-warning` Y=50% (centro, seguro).
