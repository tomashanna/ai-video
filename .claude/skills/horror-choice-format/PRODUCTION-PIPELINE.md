# PRODUCTION-PIPELINE.md — Pipeline técnico de producción

> Comandos exactos, voice IDs, patrones GSAP y reglas de implementación aprendidas en producción del Video #1. Este documento es la diferencia entre tardar 2 horas en un hito y tardar 20 minutos.

---

## 1. TTS — GENERACIÓN DE NARRACIÓN

### Comando base
```bash
cd "/ruta/al/proyecto"
.venv/bin/python scripts/tts.py \
  -t "Texto a narrar." \
  -v 2gPFXx8pN3Avh27Dw5Ma \
  -o assets/nombre-raw.mp3
```

### Voice IDs validados
> ⛔ **El voice ID `Tj9l48J9AJbry5yCP5eW` (Video #1) está DEPRECATED.** No usarlo como default. El default canónico y el narrador V5 viven en `library/voices-catalog.json` (source of truth — Hard rule #19, `canonical_validation_status` mandatorio).

| Voz | ID | Uso |
|-----|-----|-----|
| Default proyecto | `2gPFXx8pN3Avh27Dw5Ma` | Default canónico (ver `voices-catalog.json`) |
| Narrador V5 | `K3TeN3ZVK8WnOeJ0NYqZ` | Narrador horror V5 (ver `voices-catalog.json`) |
| Horror narrador Video #1 | `Tj9l48J9AJbry5yCP5eW` | ⛔ DEPRECATED — histórico, no usar |

### Post-procesado de narración

> ⛔ **`atempo=2.0` está DEPRECATED.** No acelerar la voz al doble. El pipeline real (ver `../ai-video-production/PIPELINE.md` + `INGENIERO-PAUTA-MASTER.md § 1.6`) ajusta el pace con un **cap ≥0.90** sobre el TTS lento — NO un slow-down/speed-up fijo de la voz. Generar la narración al pace WPM canónico (INGENIERO-PAUTA) y aplicar el atempo de corrección solo si el TTS quedó por debajo del piso, nunca un factor 2.0.

Medir duración del resultado:
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/nombre.mp3
```

**Regla:** medir siempre el pace real con ffprobe contra la banda WPM canónica antes de aceptar el clip. La voz sin procesar suena a IA, pero el fix es pace correcto en generación, no `atempo=2.0`.

### Volumen de producción por hito
- 4 bloques de narración por hito (narr1–narr4)
- narr1: setup del escenario (~5–8s al pace WPM canónico)
- narr2: tensión + pregunta del personaje (~1.5–2.5s)
- narr3: "Ahora decide." (~1s)
- narr4: twist dual (malo + bueno) (~7–9s)

---

## 2. IMÁGENES — GENERACIÓN CON GEMINI

### Comando base
```bash
cd "/ruta/al/proyecto"
.venv/bin/python scripts/image.py \
  -p "prompt aquí" \
  -o assets/nombre.png
```

⚠️ El template de `image.py` es **AGNÓSTICO** (no aplica suffix por default). Para horror, aplicá el HORROR_SUFFIX de una de dos formas: pasá `--style-suffix "<horror suffix>"` en cada call, **o** seteá `STYLE_SUFFIX = HORROR_SUFFIX` en tu copia de `scripts/image.py` (la constante `HORROR_SUFFIX` ya está definida ahí). El estilo horror es:
> "Dark cinematic horror aesthetic, desaturated color grade with warm amber and orange highlights only, liminal space mood, eerie atmospheric lighting, Midjourney v6 photorealistic style, uncanny valley, subtle film grain, low-key lighting, dead-center composition, 35mm lens, shallow depth of field. No text, no logos, no watermarks."

No repitas el suffix en tu prompt si lo aplicás vía `--style-suffix`/`STYLE_SUFFIX`. Solo describí la escena.

### Estructura de prompt que funciona
```
[PUNTO DE VISTA] + [SUJETO PRINCIPAL] + [ACCIÓN/ESTADO] + [AMBIENTE] + [ÁNGULO DE CÁMARA]
```

Ejemplo funcional:
> "First-person POV seated at a long wooden table in a dark farmhouse dining room. A plate of roasted meat placed directly in front of you. Four figures with large insect heads sit around the table eating silently. To your left, a beetle-headed figure in a white shirt leans toward you, one finger pointing at your plate. Candles on the table, cold shadows, stone walls. Wide shot, slightly low angle."

### Lo que Gemini rechaza (aprendido en producción)
| ❌ Bloqueado | ✅ Alternativa segura |
|-------------|----------------------|
| "blood", "sangre" | "dark fluid", "dark stain" |
| "slashing motion toward camera" | "arm raised in static position" |
| "razor-sharp serrated edge" | "sharp chitinous foreleg" |
| "throat opening from inside" | "skin splitting to reveal exoskeleton" |
| Gore explícito con descripción de herida | Body horror descriptivo sin fluidos |

**Regla general:** describir el resultado visual, no la acción violenta. "Una pierna con exoesqueleto quitinoso visible" pasa. "Una pierna siendo cortada con sangre" no pasa.

### Imágenes por hito (patrón Video #1)
| Posición | Qué muestra | Timing |
|----------|-------------|--------|
| img-1 | Wide shot del escenario, POV entrando | Setup narr1 |
| img-2 | Close-up del personaje que da la advertencia | narr2 |
| img-3 | Close-up del elemento de tensión (monstruo, objeto) | narr3 + countdown |
| img-4a | Twist malo — consecuencia visual | narr4 primera mitad |
| img-4b | Twist bueno — salida/reconocimiento | narr4 segunda mitad |

---

## 2.5 VARIANTES DE IMAGEN — REGLA V8-1 (OBLIGATORIA)

> Aprendida del post-mortem de bosque-abandonado v2: reusar el mismo PNG para varias captions de la misma escena produce slideshow feel. El parallax y Ken Burns delatan la repetición todavía más.

### Cuándo generar variantes

| Duración total de la escena en el video | Variantes mínimas |
|---|---|
| ≤ 4s | 1 (no requiere variantes) |
| 4–8s | 2 (`-a`, `-b`) |
| > 8s | 3 (`-a`, `-b`, `-c`) |

Contar la duración total que la escena ocupa en el video, no la duración de cada caption individual. Ejemplo: si `h3-forest-walk` aparece en 4 captions de 2-3s cada una sumando 10s totales, son 3 variantes.

### Cómo diseñar las variantes

Cambia **ángulo / distancia / pose / framing** — NO cambies el escenario, los personajes, ni la paleta de color. La variante debe parecer otro frame del mismo plano, no otra escena.

Ejemplos del proyecto bosque-abandonado:
- `h3-forest-walk-a` — Berni 3 pasos adelante, POV centrado
- `h3-forest-walk-b` — Berni 5 pasos adelante (más pequeño en frame), más niebla
- `h3-forest-walk-c` — POV bajo (cerca del suelo), solo se ven las piernas de Berni mid-stride

Mismo escenario. Distinto framing.

### Comando

```bash
.venv/bin/python scripts/image.py -p "<prompt variante>" -o assets/<name>-b.png
```

Lanzar las generaciones en paralelo en background (Gemini Nano Banana tolera 3-5 RPM concurrente):

```bash
for variant in b c; do
  python scripts/image.py -p "..." -o assets/h3-forest-walk-$variant.png &
done
wait
```

Budget: +5-8 imágenes por video, ~$0.20-0.40 en Gemini Nano Banana paid tier.

### Naming + symlinks (importante si la composición ya rendereó)

Si renombrás `h3-forest-walk.png → h3-forest-walk-a.png` para empezar a usar variantes, dejá un symlink para no romper composiciones previas:

```bash
cd assets/
mv h3-forest-walk.png h3-forest-walk-a.png
ln -sf h3-forest-walk-a.png h3-forest-walk.png
```

Documentado como error 5.13 en PAUTA.md.

### Wiring en index.html

Alternar variantes cada 2-3s dentro de la misma escena:

```html
<img id="h3-walk-1" src="assets/h3-forest-walk-a.png" class="scene-image clip"
     style="opacity:0;" data-start="19.0" data-duration="3.0" data-track-index="20" />
<img id="h3-walk-2" src="assets/h3-forest-walk-b.png" class="scene-image clip"
     style="opacity:0;" data-start="22.0" data-duration="3.0" data-track-index="21" />
<img id="h3-walk-3" src="assets/h3-forest-walk-c.png" class="scene-image clip"
     style="opacity:0;" data-start="25.0" data-duration="2.7" data-track-index="22" />
```

Aplicar el Ken Burns + parallax (sección 3.5) a cada variante por separado.

---

## 3. GSAP — PATRONES DE IMPLEMENTACIÓN

### Regla crítica: ancla en t=0 para evitar pre-render flash
Todo elemento que empiece invisible DEBE tener esta ancla, o HyperFrames lo mostrará brevemente al inicio del video:

```js
// ✅ CORRECTO
tl.set("#mi-imagen", { opacity: 0, scale: 1.0 }, 0);  // ancla t=0
tl.set("#mi-imagen", { opacity: 1 }, 36.6);             // reveal
tl.to( "#mi-imagen", { scale: 1.04, duration: 8, ease: "sine.inOut" }, 36.6); // KB
tl.set("#mi-imagen", { opacity: 0 }, 44.3);             // hide

// ❌ INCORRECTO — produce flash al inicio
tl.set("#mi-imagen", { opacity: 1 }, 36.6);
```

### Patrón de white flash en twists
```js
tl.set("#flash-white", { opacity: 0.9 }, T);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, T + 0.001);
```
Nunca usar `fromTo` para el flash — mismo bug que el ancla.

### Patrón de loading bar (siempre 3s en este proyecto)
```js
tl.set("#h4-loading-wrap", { opacity: 1 }, T);
tl.to( "#h4-loading-fill", { width: "100%", duration: 3.0, ease: "none" }, T);
tl.set("#h4-loading-wrap", { opacity: 0 }, T + 3.1);
```
Nota: PATTERNS.md dice 2.5s. En implementación HTML usamos 3.0s (countdown de 3 dígitos × 1s cada uno). Ambos validados.

### Patrón de countdown (reusar los mismos elementos #cnt-3/2/1)
```js
tl.set("#cnt-3", { opacity: 1 }, T);     tl.set("#cnt-3", { opacity: 0 }, T + 1.0);
tl.set("#cnt-2", { opacity: 1 }, T+1.0); tl.set("#cnt-2", { opacity: 0 }, T + 2.0);
tl.set("#cnt-1", { opacity: 1 }, T+2.0); tl.set("#cnt-1", { opacity: 0 }, T + 3.0);
```
Los elementos `#cnt-3/2/1` se comparten entre todos los hitos. No duplicar HTML.

### Ken Burns (zoom sutil en imágenes estáticas)
```js
tl.to("#mi-imagen", { scale: 1.04, duration: DURACIÓN, ease: "sine.inOut" }, T_INICIO);
```
- Scale máximo: 1.04 (más hace que se vea barato)
- Ease: `sine.inOut` siempre
- Para imágenes que se muestran 2 veces (ejemplo h4-table), usar duration = span total del hito para suavidad

---

## 3.5 MOTION LAYER COMPLETO — REGLA V8-3 (OBLIGATORIA)

> Ken Burns es el **piso**, no el techo. Toda escena estática >2s requiere algún tipo de motion adicional según el género y momento narrativo. Aprendido del post-mortem de bosque-abandonado v2 (Gemini: "PowerPoint narrado, no cine").

### Cuándo aplicar cada técnica

| Técnica | Cuándo aplicarla |
|---|---|
| Ken Burns (scale 1.04) | **Siempre**, en todo plano estático. Es el piso. |
| Parallax 3 capas | Planos con profundidad (forest path, road, hallway) |
| Flicker de exposición | Rostros tensos, luces inestables, momentos de "respiración" |
| Handheld shake | Close-ups de horror sostenidos >2s |
| Vignette pulsante | Momentos de tensión sostenida (build-up al twist) |
| Glitch frame | Antes/durante white flash twist |
| Glow pulsante | Fuentes de luz cálida en plano (fogata, luz misteriosa) |
| Niebla/partículas/chispas | Exteriores (bosque), interiores con humo, fogatas |

### Parallax 3 capas

Estructura HTML — wrappear la imagen con capas:
```html
<div class="parallax-wrap clip" data-start="19" data-duration="6.7" data-track-index="20">
  <img id="px-back"  class="px-layer" src="assets/h3-forest-walk-a.png" data-depth="0.3" />
  <img id="px-mid"   class="px-layer" src="assets/h3-forest-walk-a.png" data-depth="0.6" />
  <img id="px-front" class="px-layer" src="assets/h3-forest-walk-a.png" data-depth="1.0" />
</div>
```

```css
.parallax-wrap { position: absolute; inset: 0; }
.px-layer      { position: absolute; inset: 0; object-fit: cover; }
```

Patrón GSAP (T = inicio del plano, DUR = duración):
```js
// Las 3 capas viajan a la misma dirección a distintas velocidades
tl.fromTo("#px-back",  { x: 0 }, { x: -12, duration: DUR, ease: "none" }, T);
tl.fromTo("#px-mid",   { x: 0 }, { x: -24, duration: DUR, ease: "none" }, T);
tl.fromTo("#px-front", { x: 0 }, { x: -40, duration: DUR, ease: "none" }, T);
```

Para parallax vertical (POV caminando) sustituir `x` por `y`.

### Flicker de exposición

```js
// 3 pulsos sutiles de brillo durante la duración del plano
tl.to("#mi-imagen", { filter: "brightness(1.08)", duration: 0.12, ease: "power2.out" }, T + 1.0);
tl.to("#mi-imagen", { filter: "brightness(1.00)", duration: 0.18, ease: "power2.in"  }, T + 1.12);
tl.to("#mi-imagen", { filter: "brightness(0.94)", duration: 0.10, ease: "power2.out" }, T + 2.5);
tl.to("#mi-imagen", { filter: "brightness(1.00)", duration: 0.15, ease: "power2.in"  }, T + 2.6);
```

Importante: si la imagen ya tiene un `filter` base (contrast/saturate/brightness para horror grade), el flicker debe respetarlo. Usar variables CSS:
```css
.scene-image { --base-filter: contrast(1.18) saturate(0.45) brightness(0.82); filter: var(--base-filter); }
```

### Handheld shake sutil

```js
// Loop manual de micro-shake durante la duración del plano
function microShake(targetSel, startT, durationT) {
  const steps = Math.floor(durationT * 6); // ~6Hz
  for (let i = 0; i < steps; i++) {
    const t = startT + i / 6;
    const dx = (Math.random() - 0.5) * 4; // ±2px
    const dy = (Math.random() - 0.5) * 4;
    tl.set(targetSel, { x: dx, y: dy }, t);
  }
  tl.set(targetSel, { x: 0, y: 0 }, startT + durationT);
}
microShake("#h3-berni-whisper", 25.7, 2.3);
```

### Vignette pulsante

CSS:
```css
.vignette-pulse {
  position: absolute; inset: 0; pointer-events: none; z-index: 45;
  background: radial-gradient(ellipse 900px 1700px at 50% 50%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.85) 100%);
}
```

GSAP — pulso lento 2-3s antes del twist:
```js
tl.fromTo("#vignette-pulse", { opacity: 0.4 }, { opacity: 0.75, duration: 1.5, ease: "sine.inOut" }, T_BUILDUP);
tl.to(   "#vignette-pulse", { opacity: 0.4, duration: 1.5, ease: "sine.inOut" }, T_BUILDUP + 1.5);
```

### Glitch frame (antes/durante white flash twist)

```js
// 2 frames de displacement justo antes del flash
tl.set("#mi-imagen", { x: 8, filter: "hue-rotate(15deg)" }, T_FLASH - 0.066);
tl.set("#mi-imagen", { x: -6, filter: "hue-rotate(-10deg)" }, T_FLASH - 0.033);
tl.set("#mi-imagen", { x: 0, filter: "" }, T_FLASH);
// luego el patrón normal de #flash-white
```

### Glow pulsante

Para luces cálidas en frame (fogata, luz misteriosa, linterna):
```js
tl.to("#h4-light-source", {
  filter: "brightness(1.15) drop-shadow(0 0 40px rgba(255,180,80,0.7))",
  duration: 0.6, ease: "sine.inOut", repeat: -1, yoyo: true
}, T);
```

### Niebla / partículas overlay

Capa HTML encima del scene-image:
```html
<div class="fog-layer" style="background-image: url('assets/fog-loop.png');"></div>
```

```css
.fog-layer {
  position: absolute; inset: 0; pointer-events: none; z-index: 32;
  background-size: cover; opacity: 0.45; mix-blend-mode: screen;
  will-change: transform;
}
```

GSAP — deriva lenta:
```js
tl.fromTo(".fog-layer",
  { x: 0, y: 0 },
  { x: -120, y: -40, duration: 30, ease: "none", repeat: -1 },
  0);
```

Para chispas en fogata, usar Canvas 2D o un sprite sheet animado con `background-position`.

### Cómo combinar — capas típicas por género de escena

| Tipo de escena | Stack recomendado |
|---|---|
| POV caminando en bosque | Ken Burns + parallax 3 capas + niebla overlay |
| Close-up rostro tenso | Ken Burns + flicker + handheld shake + vignette pulse |
| Aparición monstruo / mano | Glitch frame + vignette cierre |
| Luz cálida / fogata | Ken Burns + glow pulsante + partículas |
| Carretera al amanecer | Ken Burns (push-in) + niebla disipándose |
| Buildup pre-twist | Vignette pulse + flicker creciente |

### Performance — qué evitar

- ❌ `filter: blur()` animado (mata GPU)
- ❌ Más de 6 elementos animando simultáneamente en la misma capa
- ❌ Animar `width`/`height` — siempre `transform: scale/translate`
- ❌ Setear `will-change` en >10 elementos al mismo tiempo

---

## 4. CAPTIONS — CSS OBLIGATORIO

> ⛔ **CSS/clases de captions → `../ai-video-production/CAPTIONS.md`** (home canónico). Ahí vive el CSS completo (`white-space: normal` obligatorio, font-size 80px / 68px para frases largas, text-stroke, width safe-zone) **+ el sistema de 3 clases** (`caption-name` / `caption-narration` / `caption-warning`) que este subset NO tenía. No dupliques las reglas acá.

---

## 5. HYPERFRAMES — RENDER

### Comando de render
```bash
cd "/ruta/al/proyecto"
"/ruta/al/hyperframes" render . \
  --output renders/nombre-draft.mp4 \
  --fps 30 \
  --quality draft
```

Ruta de HyperFrames en este proyecto:
```
~/.npm/_npx/702923228c2ce1e6/node_modules/.bin/hyperframes
```

### Opciones de calidad
| Flag | Uso | Tiempo estimado (56s video) |
|------|-----|---------------------------|
| `--quality draft` | Revisión rápida | ~8–15 min |
| `--quality high` | Entrega final | ~30–45 min |

### Problemas conocidos y soluciones
| Problema | Causa | Solución |
|---------|-------|----------|
| `Target closed` (exit code 1) | Chrome crash por memoria | Reintentar — es transient |
| Imágenes con 404 en render | Path mal en `src=` | Verificar que el archivo existe en `assets/` |
| Audio silencioso | `<audio>` sin atributo `id` | Agregar `id` único a todo `<audio>` |
| Elemento visible desde t=0 | Falta ancla GSAP | Agregar `tl.set(el, {opacity:0}, 0)` |
| Flash visible al inicio | `fromTo` usado para estado inicial | Reemplazar con `set + to` |

### Timing del render en producción
- Draft de 56s tarda ~8–12 min en MacBook
- Chrome puede reducir workers a 1 cuando hay muchos audios (normal, continúa igual)
- No interrumpir — el proceso continúa aunque parezca lento

---

## 6. FÓRMULA DE TIMING POR HITO

Para calcular los timestamps de un hito nuevo a partir de las duraciones de audio:

```
T_inicio = T_fin_hito_anterior

T_narr1_fin = T_inicio + dur_narr1
T_narr2_fin = T_narr1_fin + dur_narr2
T_narr3_fin = T_narr2_fin + dur_narr3

T_countdown = T_narr3_fin + 0.2  (gap mínimo)
T_twist_flash = T_countdown + 3.0  (3s de countdown)
T_narr4_fin = T_twist_flash + dur_narr4

T_fin_hito = T_narr4_fin

T_img1_hide = T_narr2_fin  (aprox — ver cuándo cambia la escena)
T_img2_hide = T_countdown
T_img3_hide = T_twist_flash
T_twist_malo_hide = T_twist_flash + (dur_narr4 * 0.55)  (aprox primera mitad)
T_twist_bueno_hide = T_fin_hito
```

Siempre medir duraciones reales con ffprobe antes de calcular — nunca asumir.

---

## 7. NOMENCLATURA DE ASSETS

Patrón establecido:
```
assets/
  h{N}-scene.png             → wide shot del escenario (default = variante -a)
  h{N}-scene-{a,b,c}.png     → variantes de la misma escena (V8-1 — regla obligatoria)
  h{N}-{personaje}.png       → close-up de personaje
  h{N}-{elemento}.png        → objeto/elemento de tensión
  h{N}-{twist-malo}.png      → consecuencia negativa
  h{N}-{twist-bueno}.png     → salida / reconocimiento
  h{N}-narr{1-4}-raw.mp3     → TTS sin procesar (descartar después)
  h{N}-narr{1-4}-2x.mp3      → TTS procesado (usar en render)
  music-{nombre}-raw.mp3     → música descargada sin procesar
  music-{nombre}.mp3         → música procesada (trim + fades) lista para render
  sfx/
    h{N}-{descriptor}.mp3    → SFX por escena (V8-2 — regla obligatoria)
    ambient-{nombre}.mp3     → capas ambient continuas (forest-wind, dawn-warmth)
```

Los raw se pueden borrar una vez validado el hito. Los 2x son los definitivos.

### Reserva de `data-track-index`

| Rango | Uso |
|---|---|
| 0–19 | Imágenes (scene-image y capas parallax) |
| 20–39 | Captions y elementos de texto |
| 40–59 | Narración + música + ticks |
| **60–110** | **SFX dedicados (V8-2) — reservado** |
| 111+ | Misceláneos (overlays, flashes, fade) |

Asignar `data-track-index` único por clip para que HyperFrames no haga conflictos en render.

---

## 8. MÚSICA DE FONDO — REGLAS DE PRODUCCIÓN

### Estructura de segmentos (Video #1)

| Segmento | Archivo | t_start | t_end | Volume | Descripción |
|----------|---------|---------|-------|--------|-------------|
| Horror | `music-horror.mp3` | 0 | 63.1s | 0.18 | Thriller suspense, looped, fade in 0.5s / out 1s |
| Fiesta | `music-party.mp3` | 63.1s | 68.3s | 0.22 | EDM trance desde segundo 17 del original, 5.2s |
| Amanecer | `music-dawn.mp3` | 68.3s | 74.4s | 0.40 | Serena, 6.1s, fade in 0.3s / out 0.5s |

### Volúmenes validados
- Narración siempre a `data-volume="1.0"`
- Música horror: `0.18` — audible pero no tapa la voz
- Música fiesta: `0.22` — ligeramente más alto que horror para el contraste, sin tapar narración
- Música amanecer: `0.40` — sin narración encima, puede ser más presente

### Fuentes (royalty-free, sin atribución):
- Horror: `nastelbom-horror-thriller-376319` — Pixabay
- Fiesta: `diogodasilvasimoes-forever-edm-trance-vibes-489439` — Pixabay (usar desde segundo 17)
- Amanecer: `ashot_danielyan-serene-peace-110617` — Pixabay

### Procesado de música — REGLA CRÍTICA

**❌ NUNCA hacer esto (produce archivo silencioso):**
```bash
ffmpeg -y -ss 17 -i music-raw.mp3 -t 5.2 -af "afade=t=in:st=0:d=0.2" music.mp3
# -ss antes de -i + -af produce silencio total
```

**✅ Siempre en DOS pasos:**
```bash
# Paso 1: extraer el clip
ffmpeg -y -i music-raw.mp3 -ss 17 -t 5.2 music-clip.mp3

# Paso 2: aplicar fades por separado
ffmpeg -y -i music-clip.mp3 \
  -af "afade=t=in:st=0:d=0.2,afade=t=out:st=5.0:d=0.2" \
  music-final.mp3
```

**Para loops (cuando el track es más corto que la duración necesaria):**
```bash
ffmpeg -y -stream_loop 1 -i music-raw.mp3 -t 63.1 \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=62.1:d=1.0" \
  music-horror.mp3
# -stream_loop 1 antes de -i hace que el archivo se reproduzca 2 veces
# No usar -ss con -stream_loop
```

**Verificar que el archivo tiene audio (nunca asumir):**
```bash
ffmpeg -i music.mp3 -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"
# Si dice "-inf LUFS" → archivo silencioso, reprocesor
# Si dice "-7 LUFS" o similar → OK
```

---

## 9. KLING (VIDEO.PY) — PROMPTS QUE FUNCIONAN

> Esta sección es referencia rápida con los 9 prompts validados en elige-companero. Para el playbook completo de animación (duration matching, tier 5s vs 10s, loop strategy, integración HTML, costo + retries, anti-patterns) ver **`../ai-video-production/ANIMATION-LAYER.md`** ⭐
>
> Override del formato horror-choice (H1 siempre tier 5s loopable atmospheric): ver `PATTERNS.md` § 10.5.

### Comando base
```bash
cd "/ruta/al/proyecto"
.venv/bin/python scripts/video.py \
  -i assets/imagen.png \
  -p "motion prompt aquí" \
  -o assets/nombre.mp4 \
  --duration 5
```
Modelo: `kwaivgi/kling-v2.0` | Parámetro de imagen: `start_image` (NO `image`) | cfg_scale: 0.5

### Fórmula de prompt que funciona
```
[SUJETO] + [VERBO DE MOVIMIENTO ESPECÍFICO] + [DIRECCIÓN/RESULTADO] + [CONTEXTO ATMOSFÉRICO]
```

Kling responde bien a movimientos **lentos, deliberados y de un solo sujeto**. Cuantos más elementos en movimiento simultáneo, peor el resultado.

### Prompts validados en Video #1

| Clip | Prompt | Resultado |
|------|--------|-----------|
| h3-scene | `First person camera slowly moves forward toward a dark farmhouse doorway, four insect-headed figures seated at a table inside, dim candlelight, atmospheric fog, eerie slow approach` | ✅ Perfecto |
| h1-yerald-close | `elderly man leans forward toward camera with a welcoming smile, slowly raises one hand palm out gesturing to viewer, warm inviting expression` | ✅ Perfecto |
| h3-cristobal-whisper | `Beetle-headed figure tilts head slightly forward as if whispering, slow subtle movement, dim candlelight flickering, eerie atmospheric` | ✅ Perfecto |
| h3-mantis | `Praying mantis-headed figure moves closer toward camera with slow intimidating approach, head tilts, unblinking stare, unsettling presence` | ✅ Perfecto |
| h4-table | `Insect-headed figures seated around table eating slowly, heads bob in unnatural rhythmic motion, dim candlelight, eerie stillness` | ✅ Perfecto |
| h4-exit | `Heavy wooden door swings open slowly, insect figure steps aside to let through, dark night visible outside door` | ✅ Perfecto |
| h5-dawn | `Figure sprints urgently down empty rural road at dawn, fast running motion, desperate escape, golden morning light` | ✅ Perfecto |
| h6-door | `Warm smiling man nods welcomingly, people laughing and moving behind him, warm indoor party light` | ✅ Perfecto |
| h6-dance | `People in festive colorful attire dancing with raised arms, joyful movement, warm party lights, lively celebration` | ✅ Perfecto |

### Lo que NO funciona

| ❌ Patrón problemático | Qué pasa | ✅ Alternativa |
|----------------------|----------|---------------|
| `[acción] toward camera` con violencia | Kling aplica la acción sobre el propio sujeto, no hacia el espectador | Describir la experiencia del espectador: "foreleg descends into frame", "screen darkens from impact" |
| Múltiples eventos simultáneos (`swings, fluid spatters, camera shakes, goes dark`) | Kling ignora la mayoría o los mezcla mal | Un solo movimiento principal por prompt |
| `camera shakes` como efecto | Kling no lo interpreta como efecto de cámara | Omitir — editar en post si es necesario |

### Prompt para h3-cut (regenerar)
El prompt original falló porque Kling interpretó el ataque sobre la mantis misma. Prompt corregido:
```
Extreme close-up of praying mantis serrated foreleg swinging down into frame, fills the screen, everything cuts to black, first-person perspective
```

---

## 10. REGLAS V7 — PULIDO POST-ANÁLISIS GEMINI

> Las 6 reglas que llevaron el video de 7/10 (V6) a 9.5/10 (V7) según Gemini. Aplicar siempre desde el primer render. Cada regla resuelve un problema concreto que Gemini detectó en producción.

### V7-1. Text stroke obligatorio en todos los captions

**Problema en V6:** captions blancas se perdían cuando el fondo tenía zonas claras (niebla, amanecer).

**CSS — agregar al selector `.caption`:**
```css
.caption {
  /* ...resto de propiedades existentes */
  -webkit-text-stroke: 1.5px rgba(0,0,0,0.7);
}
```

### V7-2. Choice labels A/B en 64px con stroke

**Problema en V6:** las opciones "A. DEVUELVES LA MIRADA / B. BAJAS LOS OJOS" en 48px no se leían en móvil cuando el pulgar tapaba pantalla.

**CSS — reemplazar `.choice-label`:**
```css
.choice-label {
  font-family: "Anton", "Bebas Neue", sans-serif;
  font-size: 64px;          /* era 48px en V6 */
  color: #fff;
  text-shadow: 0 3px 8px rgba(0,0,0,0.9);
  -webkit-text-stroke: 2px rgba(0,0,0,0.8);
  letter-spacing: 0.06em;
  display: block;
  margin-bottom: 6px;
}
```

### V7-3. Separador de rama A→B en cada elección interna

**Problema en V6:** las ramas A (miras → caes) y B (bajás → sobrevivís) se percibían como secuenciales, no como alternativas.

**HTML — agregar antes del caption B:**
```html
<div id="h3-cap-branch-b" class="caption caption-abs"
  style="opacity:0; color:#c8d8ff;">SI BAJAS LOS OJOS:</div>
```

Texto: imperativo corto que nombra **la elección**, no la consecuencia. Color `#c8d8ff` (azul claro tenue) diferente del blanco para señalizar que es metadata, no narración.

**JS — patrón completo (T = tiempo de inicio del outcome B):**
```js
/* Pulso oscuro suave en fade-out */
tl.to("#fade-out", { opacity: 0.55, duration: 0.25, ease: "power2.inOut" }, T);
tl.to("#fade-out", { opacity: 0,    duration: 0.25, ease: "power2.out"   }, T + 0.25);
/* Label de rama B */
tl.set("#h3-cap-branch-b", { opacity: 1 }, T);
tl.set("#h3-cap-branch-b", { opacity: 0 }, T + 1.2);
/* Caption del outcome B empieza 1.2s después del separador */
tl.set("#h3-cap-7", { opacity: 1 }, T + 1.2);
```

Aplicar el mismo patrón en cada elección interna del video (Hito 3, Hito 4, etc.).

### V7-4. Puente narrativo Cristóbal → Yerald

**Problema en V6:** la transición de la rama Cristóbal (horror) al cliffhanger Yerald (paz) era abrupta — solo un white flash, sin contexto.

**HTML — agregar en el área de captions del Hito 5:**
```html
<div id="h5-bridge-cap" class="caption caption-abs"
  style="opacity:0; font-size:68px; color:#f5d9a0;">Y SI HUBIERAS ELEGIDO A YERALD...</div>
```

Color `#f5d9a0` (dorado pálido) — anticipa la calidez del cliffhanger.

**JS — 1.5s antes del flash que abre Hito 6:**
```js
/* T_flash_h6 = tiempo del white flash que abre el cliffhanger */
tl.set("#h5-bridge-cap", { opacity: 1 }, T_flash_h6 - 1.5);
tl.set("#h5-bridge-cap", { opacity: 0 }, T_flash_h6);
```

Acortar el caption anterior del Hito 5 1.5s para hacer espacio. En V7: `h5-cap-4` termina en 64.6 (era 66.1), `h5-bridge-cap` ocupa 64.6–66.1.

### V7-5. CTA de engagement al final — TEXTO + VOZ DEL NARRADOR

**Problema en V6/V7:** el video terminaba en "UNA NOCHE EN PAZ." sin invitar a interactuar. En V7 se agregó solo caption visual — incompleto, porque "comentar A" o "comentar B" son comentarios de 1 carácter, débiles algorítmicamente.

**Solución final (V7.1 / V8):** combinar visual + voz. La voz pide "y por qué" → comentarios largos → engagement de calidad para el algoritmo de Instagram.

#### Paso 1 — generar la narración del CTA

```bash
.venv/bin/python scripts/tts.py \
  -t "Y tú... ¿qué habrías elegido? Comenta A o B abajo, y dinos por qué." \
  -v K3TeN3ZVK8WnOeJ0NYqZ \
  -o assets/cta-narration-raw.mp3

# ⛔ NO usar atempo=2.0 (DEPRECATED). Generar al pace WPM canónico; aplicar cap ≥0.90 solo si el TTS quedó lento (ver INGENIERO-PAUTA-MASTER § 1.6).
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/cta-narration-raw.mp3
# Esperado: ~2.0-2.4s al pace canónico
```

Voice ID **el mismo narrador horror del video** (narrador V5 = `K3TeN3ZVK8WnOeJ0NYqZ`, ver `voices-catalog.json`) — mantiene la inmersión. El cambio es de tono (rompe la 4ª pared y habla directo), no de voz. ⛔ El antiguo `Tj9l48J9AJbry5yCP5eW` está DEPRECATED.

#### Paso 2 — HTML del caption visual

```html
<div id="h6-cap-5" class="caption caption-abs"
  style="opacity:0; font-size:60px;">¿SOBREVIVISTE? 💬 COMENTA A o B</div>

<audio id="cta-narration" class="clip"
  src="assets/cta-narration-2x.mp3"
  data-start="[T_FIN - 2.4]"
  data-duration="2.4"
  data-track-index="52"
  data-volume="1.0"></audio>
```

Font-size 60px (más chico que las captions normales de 80px porque incluye emoji).

#### Paso 3 — JS del timing

```js
/* T_fin = duración total del video */
tl.set("#h6-cap-5", { opacity: 1 }, T_fin - 2.4);
tl.set("#h6-cap-5", { opacity: 0 }, T_fin);
```

Acortar el caption anterior ("UNA NOCHE EN PAZ.") 2.4s para hacer espacio. El audio del CTA arranca automáticamente por `data-start`, no requiere tl.call.

#### Variaciones permitidas del texto

Si el video usa un cliffhanger con otro arco (ver `PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated]` § 3), adaptar el CTA:

| Archetype del cliffhanger | CTA narrado sugerido |
|---|---|
| Paz perdida (clásico) | "Y tú... ¿qué habrías elegido? Comenta A o B abajo, y dinos por qué." |
| Trampa simétrica | "Las dos te mataban. ¿Cuál te dolió más? Comenta A o B y por qué." |
| Inversión total | "El monstruo te salvó. ¿Lo viste venir? Comenta A o B y cómo lo descubriste." |
| Meta-cliffhanger | "¿Y si no había buena opción? Comenta A, B o 'NINGUNA' y por qué." |

### V7-6. Gemini QA gate antes de aprobar el render

**Problema en V6:** el render se aprobaba "a ojo" sin método objetivo. Bugs como "Gerald/Yerald inconsistente" o "transiciones confusas" pasaban a producción.

**Workflow obligatorio después de cada render:**

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/nombre.mp4 \
  --prompt "Analiza en detalle: (1) ¿Se entiende cuándo es outcome A vs B en cada elección? (2) ¿La transición a [BUENO_APARENTE] es clara? (3) ¿El texto es legible en todos los fondos? (4) ¿El tamaño del texto A/B es suficiente para móvil? (5) ¿Hay CTA al final? Dame un score 1-10."
```

**Umbral de aprobación — VARA DUAL (canónica, ver `../ai-video-production/QA.md`):**
- ⛔ El umbral ≥9.0 de V7 es **OBSOLETO**. La vara fija desde 2026-05-15 es **DUAL** y requiere AMBAS condiciones:
  - (a) Gemini calibrado (`audit-gemini-calibrated.py`, calibrated_v4) **≥9.7**, **Y**
  - (b) `audit-against-referent` **≥85%** de métricas críticas en bandas p25–p75 (F1, n=10).
- AMBAS deben pasar para APROBAR. Si Gemini ≥9.7 pero referent <85% → NO aprobado (iterar). Si referent ≥85% pero Gemini <9.7 → NO aprobado (iterar A→B→C pre-animation).
- Cap de iteración: 3 rounds pre-animation. Tras 3 sub-9.7 → ESCALAR al usuario (no parar pre-animation esperando que la animación AI rescate el score).

**Qué hacer con el feedback:**
- Cada problema que Gemini menciona → comparar contra reglas V7-1 a V7-7 — la mayoría son cubiertos por estas reglas
- Problemas que NO están cubiertos → documentar como nueva regla V8

### V7-7. Instagram safe zones (CSS posicional)

**Problema en V7 draft:** name-labels en `top:180px` quedaban bajo el botón X de Instagram; captions y CTA en `bottom:0 height:400px` quedaban tapados por el caption del post + profile pic + audio + follow.

**Zonas reservadas en el frame 1080×1920:**
- **Top:** y = 0–270 (14% superior) — botón X, audio info, sound mute
- **Bottom:** y = 1380–1920 (28% inferior) — caption del post, profile pic + handle, audio attribution, botón seguir
- **Right:** x = 840–1080 (22% derecha) — like, comment, share, save, "..."

**Zona segura para texto crítico:** X 60–840, Y 270–1380.

**CSS — reglas posicionales obligatorias:**

```css
/* Labels superiores (nombres de personajes, headers) */
.name-label {
  top: 300px;          /* mínimo 270, recomendado 300 */
  /* ...resto de propiedades */
}

/* Captions principales + CTA final */
.caption-wrap {
  bottom: 540px;       /* aleja el wrap de la UI inferior */
  height: 280px;       /* captions centradas en y≈1240 */
  /* ...resto de propiedades */
}

/* Loading bars con opciones A/B durante la elección */
.loading-bar-wrap {
  bottom: 700px;       /* la barra queda en y≈1220, choice labels arriba */
  /* ...resto de propiedades */
}
```

Si usás `style="bottom:XXXpx"` inline para overridear el default del `.loading-bar-wrap` (por ejemplo para alinear con choice labels en `#h3-loading-wrap`), nunca menor a `bottom: 680px`.

**Verificación visual obligatoria post-render:**
```bash
# Extraer frames con texto crítico
ffmpeg -ss 2  -i renders/v.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/check-top.png    # name labels
ffmpeg -ss 25 -i renders/v.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/check-cap.png    # captions
ffmpeg -ss [t_cta] -i renders/v.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/check-cta.png  # CTA final
```

Después leer las imágenes con el Read tool y confirmar que ningún texto vive en el 14% superior ni en el 28% inferior del frame.

---

## 11. SYMLINK assets/ — GOTCHA DE PRODUCCIÓN

El HTML referencia `assets/...` pero los archivos viven en `assets v1/`. Crear el symlink antes del primer render:

```bash
cd "/ruta/al/proyecto"
ln -sf "assets v1" assets
```

Verificar:
```bash
ls -la | grep assets
# Debería mostrar: assets -> assets v1
```

Sin este symlink, el render produce errores `media_missing_src` para todos los videos/audios y el resultado sale silencioso o sin imágenes. El lint también falla con `audio_src_not_found`.

### Symlinks de variantes (gotcha de V8-1)

Cuando agregás variantes a una composición que ya rendereó antes, el HTML original referencia `assets/nombre.png` pero el archivo está ahora en `assets/nombre-a.png`. Dejar symlinks por compatibilidad:

```bash
cd assets/
mv h3-forest-walk.png h3-forest-walk-a.png
ln -sf h3-forest-walk-a.png h3-forest-walk.png  # backward-compat
```

Distinto del symlink global de § 11 (`assets → assets v1`, folder completo). Este es por archivo individual.

---

## 12. SFX — ELEVENLABS SOUND EFFECTS (REGLA V8-2)

> Motor principal de sound design. Generativo desde texto, duración controlable 0.5-22s, mismo workflow que TTS.

### Requisitos previos

- `ELEVENLABS_API_KEY` en `.env` (la misma que TTS)
- Paquete `elevenlabs >= 2.40.0` en el venv del proyecto (incluye `client.text_to_sound_effects.convert`)
- Carpeta `assets/sfx/` creada

### Script — `scripts/sfx.py`

Patrón implementado en bosque-abandonado. Análogo a `scripts/tts.py`. Modo single y batch.

```bash
# Single
python scripts/sfx.py -t "<prompt>" -d <segundos> -i <influence 0-1> -o assets/sfx/<name>.mp3

# Loop perfecto
python scripts/sfx.py -t "campfire crackling cozy" -d 8 --loop -o assets/sfx/fire-loop.mp3

# Batch desde spec JSON
python scripts/sfx.py --spec sfx-spec.json
```

### Formato `sfx-spec.json`

```json
[
  {
    "out": "assets/sfx/h3-whisper.mp3",
    "text": "creepy hushed whisper of an old man very close to the ear, breathy, no music",
    "duration": 2.0,
    "influence": 0.6
  },
  {
    "out": "assets/sfx/h3-footsteps-loop.mp3",
    "text": "slow heavy footsteps on dry dead leaves, single person, steady pace, dry no reverb",
    "duration": 4.0,
    "influence": 0.5,
    "loop": true
  }
]
```

### Parámetros del endpoint

| Parámetro | Rango | Cuándo cambiarlo |
|---|---|---|
| `text` | string | Prompt — describir el sonido, no la causa. "low impactful sub-bass stab" mejor que "monster attack sound" |
| `duration_seconds` | 0.5 – 22 | Lo que necesitás. Para loops largos >22s usar Freesound |
| `prompt_influence` | 0 – 1 | `0.3` default. Subir a `0.6-0.7` para impacts y drones donde querés que respete tu prompt al pie |
| `loop` | bool | `true` para ambient loops perfectos (fire, wind, footsteps loop) |
| `output_format` | `mp3_44100_128` | Coincide con TTS — facilita mezcla |

### Estructura de prompt que funciona

```
[TIPO DE SONIDO] + [CARACTERÍSTICA SONORA ESPECÍFICA] + [CONTEXTO] + [NEGATIVOS]
```

Negativos típicos: `no music`, `no melody`, `dry no reverb`, `single event`, `no echo`.

Ejemplos validados (bosque-abandonado v3):

| Categoría | Prompt | Duración | Influence |
|---|---|---|---|
| Sub-bass impact | `low frequency cinematic sub-bass stab impact for title reveal, single short hit, dry no reverb tail, no music` | 0.5 | 0.5 |
| White flash | `short cinematic white-flash impact, sharp crack with deep sub-bass tail, like a camera flash crossed with thunder, dry, single event` | 0.7 | 0.5 |
| Footsteps loop | `slow heavy human footsteps walking on dry dead crunchy leaves, single person, steady pace, dry no reverb, no music` | 4.0 | 0.5 |
| Whisper horror | `creepy hushed unintelligible whisper of an old man very close to the ear, breathy, single short phrase, no music, no melody` | 2.0 | 0.6 |
| Tension drone | `low rising tension drone slow build sub-bass cinematic horror buildup, no melody, no rhythm, intensifies smoothly` | 2.5 | 0.7 |
| Body fall | `human body collapsing onto dead leaves and earth, dull thud no scream, single event, no music` | 1.5 | 0.6 |
| Campfire loop | `warm intimate campfire crackling close-up, dry wood embers popping, cozy continuous ambient` | 8.0 | 0.5 (`loop:true`) |

### Mix volumes

> ⛔ **Mix volumes → `../ai-video-production/SFX-PIPELINE.md § Mix volumes`** (tabla canónica de `data-volume`: narración 1.0 / música 0.05–0.18 / SFX 0.20–0.35 / flash 0.55–0.65 / ambient continuo 0.10–0.18 / clinks 0.25–0.35). No dupliques la tabla acá.

### Cuántos SFX por video — orden de magnitud

Un Reel de 80-90s en este formato típicamente necesita **25-30 SFX** discretos. Costo aproximado en ElevenLabs paid tier: ~$5-8 totales (~200 créditos/seg de SFX generado).

---

## 12.5 LOOP EXPANSION — AMBIENTS LARGOS CON ELEVENLABS

> ElevenLabs limita cada call a 22s. Para ambient layers continuos que cubren toda la sección horror (~70s) o el cliffhanger (~12s), generar a 22s con `loop:true` y expandir con ffmpeg `stream_loop`.

### Patrón estándar

```bash
# 1. Generar el seed loopable de 22s
.venv/bin/python scripts/sfx.py \
  -t "continuous abandoned forest night wind, dead trees creaking, cold atmospheric, no animals, no rain, perfectly looping" \
  -d 22 --loop -i 0.5 \
  -o assets/sfx/ambient-forest-wind-loop.mp3

# 2. Expandir a duración objetivo con fade-out
ffmpeg -y -stream_loop 3 -i assets/sfx/ambient-forest-wind-loop.mp3 -t 75 \
  -af "afade=t=out:st=74:d=1" \
  assets/sfx/ambient-forest-wind.mp3
```

`-stream_loop 3` = el archivo se reproduce 4 veces total (original + 3 loops). Ajustar según duración objetivo: `ceil(target / source) - 1`.

| Target | Source 22s | -stream_loop |
|---|---|---|
| 45s | 22s | 1 (2 vueltas) |
| 75s | 22s | 3 (4 vueltas) |
| 90s | 22s | 4 (5 vueltas) |

### Casos cubiertos

| Asset | Prompt clave | Duración final |
|---|---|---|
| `ambient-forest-wind.mp3` | "continuous forest night wind, dead trees creaking, cold atmospheric, perfectly looping" | ~75s |
| `ambient-dawn-warmth.mp3` | "warm dawn forest ambience, soft distant morning birds, cozy peaceful, perfectly looping" | 12s (direct, no expansion needed) |
| `ambient-industrial-drone.mp3` | "low industrial machine hum, distant clanks, cold institutional, perfectly looping" | ~75s |

### Por qué EL aunque corte a 22s

Validado en bosque-abandonado 2026-05-10: los 6 sonidos que originalmente iban a Freesound (wind 75s, dawn 12s, bird call, group laughter, guitar chord, dawn birds chorus) se generaron con ElevenLabs y quedaron "good enough" en el mix de horror cinematográfico. Trade-off aceptado:
- **Loops largos**: el `loop:true` de EL genera transiciones limpias; expansion con ffmpeg `stream_loop` es imperceptible cuando el sonido es estático (viento, fuego).
- **Instrumentos**: la guitarra acústica generativa es ~7/10 vs Freesound 9/10, pero como va de fondo en cliffhanger no se nota.
- **Voces humanas**: las risas grupales son las más riesgosas. Distantes y a `volume 0.20-0.25` funcionan; en foreground sonarían uncanny.

Si un asset puntual sale notoriamente uncanny, usar Freesound como fallback (§ 13).

### ElevenLabs MCP (uso ad-hoc, no para producción)

El MCP oficial está disponible vía `claude mcp add ElevenLabs --scope user -- uvx elevenlabs-mcp` con la env var `ELEVENLABS_API_KEY`. Útil para generar 1 SFX en conversación sin entrar a la CLI.

**Para producción batch, siempre usar `scripts/sfx.py` con `sfx-spec.json`** — es reproducible, versionable, y no depende de la disponibilidad del MCP.

### Workflow recomendado (orden)

1. Drafttear `SFX-LIST.md` por escena con timestamps reales medidos del index.html (cada cue tiene un `t` específico)
2. Convertir a `sfx-spec.json` (formato batch)
3. `python scripts/sfx.py --spec sfx-spec.json` — genera todo en background
4. Verificar duraciones con `ffprobe` (las generaciones pueden quedar 1-2% off del target)
5. Conectar cada SFX en `index.html` con `data-track-index` 60-110

---

## 13. FREESOUND — FALLBACK OPCIONAL (NO default)

> **Default actualizado 2026-05-10: ElevenLabs cubre todos los casos del workflow estándar.** Loops largos vía § 12.5, instrumentos y voces vía EL directo con prompts específicos. Freesound queda como **fallback avanzado** solo si un asset puntual sale notoriamente uncanny y no se arregla iterando el prompt EL.

### Cuándo recurrir a Freesound (excepción, no regla)

| Caso | Default (EL) | Freesound como fallback |
|---|---|---|
| Ambient loop forest wind 75s | ✅ EL `loop:true` 22s + ffmpeg expansion (§ 12.5) | Solo si el loop EL suena artificial |
| Single body fall thud 1.5s | ✅ EL directo | – |
| Acoustic guitar single chord | ✅ EL directo (calidad ~7/10) | Si el video pone el chord en foreground prominente |
| Group of friends laughing | ✅ EL distante a volume 0.20-0.25 | Si la mezcla requiere foreground o el resultado EL es muy uncanny |
| Dawn birds chorus 4s | ✅ EL directo | Solo si necesita máxima naturalidad |
| Whisper horror | ✅ EL directo | – |
| Sub-bass impact | ✅ EL directo | – |

### Workflow

1. Documentar las queries necesarias en `FREESOUND-QUERIES.md` (ver template en `bosque-abandonado/FREESOUND-QUERIES.md`) con: URL de búsqueda, criterios de selección, duración objetivo.
2. Usuario descarga manualmente desde [freesound.org](https://freesound.org) (requiere cuenta gratis).
3. Verificar licencia: **CC0** (sin atribución) o **CC-BY** (atribución requerida).
4. Si es WAV/largo, recortar y normalizar:
   ```bash
   ffmpeg -i source.wav -ss 30 -t 75 -ar 44100 -ac 2 assets/sfx/ambient-forest-wind.mp3 -y
   ```
5. Si es CC-BY, anotar autor + URL en `CREDITS.md` del proyecto.

### Template de query

Cada entrada en `FREESOUND-QUERIES.md` lleva:

```markdown
## `assets/sfx/<nombre>.mp3`
**Función:** [qué cubre en el video]
**URL:** https://freesound.org/search/?q=<query>&f=duration%3A%5B<min>+TO+<max>%5D
**Criterio de selección:** [lista de 3-5 filtros mentales: duración, especies, sin tráfico, etc.]
**Fallback:** [comando ffmpeg para recortar si el archivo descargado es más largo]
```

### MCP de Freesound (opcional)

Existe un servidor MCP comunitario `freesound-mcp` que automatiza búsqueda + descarga. Requiere API key gratis de Freesound. Si lo instalás, podés delegar las 6-8 descargas al agente directamente.

---
