# MOTION-LAYER.md — Motion patterns para cualquier video con IA

> Ken Burns es el piso, no el techo. Ningún plano estático >2s sin algún motion. Esto convierte un slideshow en cine. Aplica a CUALQUIER formato.

---

## Stack de motion (qué aplicar y cuándo)

| Técnica | Cuándo aplicarla |
|---|---|
| **Ken Burns** (scale 1.0 → 1.04) | **SIEMPRE** en todo plano estático >2s. Piso obligatorio. |
| **Parallax 3 capas** | Planos con profundidad (caminos, pasillos, calles) |
| **Flicker exposición** | Rostros tensos, luces inestables, momentos de "respiración" |
| **Handheld shake** | Close-ups sostenidos >2s, momentos de tensión |
| **Vignette pulsante** | Build-up al climax o twist |
| **Glitch frame** | Justo antes/durante white flash o cortes intensos |
| **Glow pulsante** | Fuentes de luz cálida (fogata, lámpara, sol) |
| **Niebla / partículas / chispas** | Exteriores con atmósfera, fuegos, ambientes |

---

## Ken Burns base

```js
tl.to("#mi-imagen", { scale: 1.04, duration: DURATION, ease: "sine.inOut" }, T_START);
```

- Scale máximo: **1.04** (más se ve barato)
- Ease: `sine.inOut` siempre
- Direccional opcional: agregar `x` o `y` para "push to corner" en lugar de zoom puro

---

## Parallax 3 capas

### HTML — wrappear la imagen con capas

```html
<div class="parallax-wrap clip" data-start="19" data-duration="6.7" data-track-index="20">
  <img id="px-back"  class="px-layer" src="assets/scene-a.png" data-depth="0.3" />
  <img id="px-mid"   class="px-layer" src="assets/scene-a.png" data-depth="0.6" />
  <img id="px-front" class="px-layer" src="assets/scene-a.png" data-depth="1.0" />
</div>
```

```css
.parallax-wrap { position: absolute; inset: 0; }
.px-layer      { position: absolute; inset: 0; object-fit: cover; }
```

### GSAP

```js
// Las 3 capas viajan a la misma dirección a velocidades distintas
tl.fromTo("#px-back",  { x: 0 }, { x: -12, duration: DUR, ease: "none" }, T);
tl.fromTo("#px-mid",   { x: 0 }, { x: -24, duration: DUR, ease: "none" }, T);
tl.fromTo("#px-front", { x: 0 }, { x: -40, duration: DUR, ease: "none" }, T);
```

Para POV caminando (vertical) sustituir `x` por `y`.

**Tip**: las 3 capas pueden ser variantes -a/-b/-c distintas para crear efecto de profundidad con cambio sutil.

---

## Flicker de exposición

3 pulsos sutiles de brillo durante el plano:

```js
tl.to("#mi-imagen", { filter: "brightness(1.08)", duration: 0.12, ease: "power2.out" }, T + 1.0);
tl.to("#mi-imagen", { filter: "brightness(1.00)", duration: 0.18, ease: "power2.in"  }, T + 1.12);
tl.to("#mi-imagen", { filter: "brightness(0.94)", duration: 0.10, ease: "power2.out" }, T + 2.5);
tl.to("#mi-imagen", { filter: "brightness(1.00)", duration: 0.15, ease: "power2.in"  }, T + 2.6);
```

**Importante**: si la imagen tiene un `filter` base (contrast/saturate/brightness por estilo), el flicker debe respetarlo. Usar CSS variables:

```css
.scene-image {
  --base-filter: contrast(1.18) saturate(0.45) brightness(0.82);
  filter: var(--base-filter);
}
```

Y animar `--base-filter` con GSAP en lugar de `filter` directo.

---

## Handheld shake sutil

```js
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

microShake("#close-up-rostro", 25.7, 2.3);
```

Si querés más intensidad: subir el rango a ±4px o ±6px en momentos extremos.

---

## Vignette pulsante

### CSS

```css
.vignette-pulse {
  position: absolute; inset: 0; pointer-events: none; z-index: 45;
  background: radial-gradient(ellipse 900px 1700px at 50% 50%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.85) 100%);
}
```

### GSAP — pulso 2-3s antes del twist/climax

```js
tl.fromTo("#vignette-pulse",
  { opacity: 0.4 },
  { opacity: 0.75, duration: 1.5, ease: "sine.inOut" },
  T_BUILDUP
);
tl.to("#vignette-pulse",
  { opacity: 0.4, duration: 1.5, ease: "sine.inOut" },
  T_BUILDUP + 1.5
);
```

Para tensión sostenida: hacer loop con `yoyo: true, repeat: -1`.

---

## Glitch frame (antes/durante twist)

2 frames de displacement justo antes del flash:

```js
tl.set("#mi-imagen", { x: 8,  filter: "hue-rotate(15deg)"  }, T_FLASH - 0.066);
tl.set("#mi-imagen", { x: -6, filter: "hue-rotate(-10deg)" }, T_FLASH - 0.033);
tl.set("#mi-imagen", { x: 0,  filter: ""                   }, T_FLASH);
// luego el patrón normal de white flash
```

---

## Glow pulsante

Para luces cálidas en frame (fogata, linterna, sol):

```js
tl.to("#fuente-de-luz", {
  filter: "brightness(1.15) drop-shadow(0 0 40px rgba(255,180,80,0.7))",
  duration: 0.6,
  ease: "sine.inOut",
  repeat: -1,
  yoyo: true
}, T_START);
```

---

## Niebla / partículas overlay

### HTML

```html
<div class="fog-layer" style="background-image: url('assets/fog-loop.png');"></div>
```

### CSS

```css
.fog-layer {
  position: absolute; inset: 0; pointer-events: none; z-index: 32;
  background-size: cover; opacity: 0.45; mix-blend-mode: screen;
  will-change: transform;
}
```

### GSAP — deriva lenta continua

```js
tl.fromTo(".fog-layer",
  { x: 0, y: 0 },
  { x: -120, y: -40, duration: 30, ease: "none", repeat: -1 },
  0
);
```

Para chispas en fogata: usar Canvas 2D o un sprite sheet animado con `background-position`.

---

## Cortes narrativos — patrón obligatorio cross-domain

> Los CORTES (cambios de imagen/escena) NO son solo motion — son **edición narrativa audio-led**. Cuando el narrador cambia de idea, rama, o llega a una pausa dramática, ahí va un negro + audio específico, no solo un cambio de imagen.
>
> Ver el documento completo **`NARRATIVE-LED-EDITING.md`** con la taxonomía de 7 tipos de corte (WHITE FLASH, BLACK + LOW THUD, BLACK + DRONE BAJO, BLACK + RISE DRONE, BLACK + EXHALE, BLACK + PUNCT SILENCE, WARM WHITE).
>
> **Aprendizaje 2026-05-10**: este patrón es la diferencia entre un video que se siente "PowerPoint con narración" y un video que se siente cine. Bosque-abandonado lo aplica orgánicamente; mina-abandonada no, y por eso se siente lineal pese a tener buen motion.

---

## Stack típico por género de plano

| Tipo de escena | Motion recomendado |
|---|---|
| POV caminando exterior | Ken Burns + parallax 3 capas + niebla overlay |
| Close-up rostro tenso | Ken Burns + flicker + handheld shake + vignette pulse |
| Aparición monstruo / amenaza | Glitch frame + vignette cierre |
| Luz cálida / fogata | Ken Burns + glow pulsante + partículas |
| Carretera / road shot | Ken Burns (push-in) + niebla disipándose |
| Buildup pre-twist / pre-climax | Vignette pulse + flicker creciente |
| Plano genérico estático | Ken Burns (default) |

---

## Anti-patterns de performance

NO hacer:

- ❌ `filter: blur()` animado (mata GPU)
- ❌ Más de 6 elementos animando simultáneamente en la misma capa
- ❌ Animar `width` / `height` — siempre `transform: scale/translate`
- ❌ Setear `will-change` en >10 elementos al mismo tiempo
- ❌ Crear más de 3 capas de parallax (4+ no mejora visualmente y duplica costo render)

Si el render se cuelga o sale lento, primero reducir capas.

---

## Workflow recomendado para aplicar motion a un video

1. **Render base** primero (solo Ken Burns + lo básico)
2. **Ver el render** y notar qué planos se sienten "muertos" o "diapositivas"
3. **Listar el motion plan** por escena en una tabla del NARRATIVE.md o doc equivalente
4. **Implementar por capas**: primero parallax donde aplica, luego flicker, luego vignette/glow, luego niebla
5. **Re-render** y comparar
6. **QA con Gemini Video Analyzer** — preguntar específicamente "¿hay momentos donde la imagen permanece estática >2s sin motion?"

---

## Transiciones avanzadas (post 2026-05-13 — referent-validated)

> Análisis de 7 referentes Instagram reveló que los cortes profesionales usan transiciones **audio-led** (J-cuts, L-cuts) y **transiciones visuales** (whip pan, light leak) — NO simples cuts duros.

### J-cut — el audio del próximo shot entra ANTES del cut visual

**Cuándo:** transición a una escena donde quieres preparar al viewer auditivamente.

**Ejemplo:** narración del Hito 3 empieza a 22.5s. Pero el ambient nuevo (cave-drone) entra a 22.0s. El viewer escucha el cambio antes de verlo → sensación de "anticipación" cinematográfica.

```html
<!-- Visual cut at 22.5s -->
<img class="clip" src="assets/h3-scene.png"
     data-start="22.5" data-duration="6" data-track-index="20">

<!-- Audio entrance at 22.0s (0.5s before visual cut) -->
<audio class="clip" src="assets/sfx/cave-drone.mp3"
       data-start="22.0" data-duration="6.5" data-volume="0.15"
       data-track-index="62">
```

**Regla:** el audio J-cut entra 0.3-0.8s antes del visual cut. Más de 1s = el viewer percibe descoordinación.

### L-cut — el audio del shot actual continúa DESPUÉS del cut visual

**Cuándo:** transición donde quieres que la voz/ambient del shot anterior sostenga la conexión emocional.

**Ejemplo:** narrador termina frase a 12.0s. Visual corta a 12.0s. Pero el ambient anterior (forest-wind) continúa hasta 12.5s, overlapping con el nuevo shot.

```html
<!-- Visual cuts at 12.0s -->
<img class="clip" src="assets/h2-scene.png"
     data-start="6" data-duration="6" data-track-index="20">
<img class="clip" src="assets/h3-scene.png"
     data-start="12.0" data-duration="8" data-track-index="20">

<!-- Audio overlaps -->
<audio class="clip" src="assets/sfx/forest-wind.mp3"
       data-start="6" data-duration="6.5" data-volume="0.12"
       data-track-index="62">
       <!-- Continues 0.5s past visual cut -->
```

### Whip pan — transición motion-blur entre shots

**Cuándo:** transición de alta energía (decision point → consequence). Más usado en TikTok/Reels que en cine.

```javascript
// Frame final del shot A
tl.to('#shot-a', {
  x: -200,
  filter: 'blur(8px) brightness(1.2)',
  duration: 0.15,
  ease: 'power2.in'
}, T - 0.15);

// Frame inicial del shot B (entrada motion-blur)
tl.fromTo('#shot-b',
  { x: 200, filter: 'blur(8px) brightness(1.2)' },
  { x: 0,   filter: 'blur(0px) brightness(1.0)', duration: 0.15, ease: 'power2.out' },
  T);
```

Total whip duration: 0.3s (0.15 out + 0.15 in). Cualquier cosa más larga rompe el ritmo.

### Light leak — overlay de luz orgánica entre cuts

**Cuándo:** transición "respiración" entre actos. Usado por video editors pros (Casey Neistat style).

```html
<div id="light-leak" class="clip"
     data-start="30" data-duration="0.6" data-track-index="92"></div>

<style>
#light-leak {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(
    ellipse at 30% 50%,
    rgba(255, 200, 100, 0.8) 0%,
    rgba(255, 200, 100, 0.3) 40%,
    transparent 70%
  );
  mix-blend-mode: screen;
  opacity: 0;
}
</style>

<script>
// Light leak swipe
tl.fromTo('#light-leak',
  { opacity: 0, x: -200 },
  { opacity: 0.8, duration: 0.2, ease: 'power2.out' },
  T);
tl.to('#light-leak',
  { opacity: 0, x: 200, duration: 0.4, ease: 'power2.in' },
  T + 0.2);
</script>
```

### Cuándo usar cada transición

| Beat narrativo | Transición recomendada |
|----------------|------------------------|
| Hito → Hito (decision point reveal) | **J-cut** (ambient nuevo anticipa cambio) |
| Consecuencia → Counterfactual | **L-cut** (sostener emoción anterior) |
| Hard energy shift (climax) | **Whip pan** + flash white |
| Suave transición ambiental | **Light leak** + crossfade |
| Cliffhanger → outro | **Crossfade** lento + BLACK + warm-whoosh |

### Anti-patterns transiciones

❌ **Hard cut sin audio bridge:** rompe inmersión. SIEMPRE usar J-cut o L-cut entre shots de >5s.

❌ **Whip pan en setup descriptivo:** la energía no encaja con el tono narrativo lento. Whip pan SOLO en momentos de high-energy.

❌ **Light leak excesivo:** >1 por video se vuelve gimmick. Reservar para transición señature (acto 2 → acto 3).

❌ **Crossfade prolongado (>1s):** se siente "old-school slideshow". Sweet spot 0.3-0.6s.

---

## Audio-reactive motion (post 2026-05-13)

> Motion que responde DINÁMICAMENTE al audio. Aumenta inmersión 2-3x vs motion estático pre-programado.

### Patrón 1 — Volume → Scale (heartbeat effect)

El elemento "respira" al ritmo del volumen del audio.

```javascript
// Setup: AudioContext + AnalyserNode
const audioCtx = new AudioContext();
const audioEl = document.querySelector('#narration-audio');
const source = audioCtx.createMediaElementSource(audioEl);
const analyser = audioCtx.createAnalyser();
analyser.fftSize = 256;
source.connect(analyser);
analyser.connect(audioCtx.destination);

const dataArray = new Uint8Array(analyser.frequencyBinCount);

// On each animation frame
function updateAudioReactive() {
  analyser.getByteFrequencyData(dataArray);
  const avgVolume = dataArray.reduce((a, b) => a + b) / dataArray.length / 255;

  // Scale element based on volume (1.0 to 1.05 range)
  const scale = 1.0 + avgVolume * 0.05;
  document.querySelector('#main-subject').style.transform = `scale(${scale})`;

  requestAnimationFrame(updateAudioReactive);
}

audioEl.addEventListener('play', () => {
  audioCtx.resume();
  updateAudioReactive();
});
```

**Nota HyperFrames:** este patrón funciona en preview interactivo. Para render deterministico, **pre-procesar** el audio y exportar curve de volumen → aplicar como tween con GSAP keyframes pre-calculados.

### Patrón 2 — Narration onset → Caption pop

Cada vez que el narrador empieza una nueva frase, el caption "pop in" con scale + glow.

```javascript
// Detectar onsets de narración (Whisper timestamps)
const narrationOnsets = [
  { time: 1.0, text: "ELIGE A TU COMPAÑERO" },
  { time: 4.0, text: "BRUNO O PABLO" },
  // ...
];

narrationOnsets.forEach(({ time, text }) => {
  tl.set('#narr-1', { innerHTML: text }, time);
  tl.fromTo('#narr-1',
    { opacity: 0, scale: 0.9 },
    { opacity: 1, scale: 1.0, duration: 0.15, ease: 'back.out(2)' },
    time);
});
```

**Diferencia vs innerHTML swap estático:** el "pop" es perceptible y mantiene atención.

### Patrón 3 — Beat sync (musical impact)

Si la música tiene beats marcados, el visual reacciona a cada beat con un sutil flicker.

```javascript
// Beat timestamps (pre-procesados via audio analysis tool)
const beats = [4.0, 4.5, 5.0, 5.5, 6.0, 6.5, /* ... */];

beats.forEach(beatT => {
  tl.to('#scene', {
    filter: 'brightness(1.10) contrast(1.10)',
    duration: 0.08,
    ease: 'power2.out'
  }, beatT);
  tl.to('#scene', {
    filter: 'brightness(1.00) contrast(1.00)',
    duration: 0.12,
    ease: 'power2.in'
  }, beatT + 0.08);
});
```

### Patrón 4 — SFX impact → Visual punch

Cada SFX de impacto (white-flash, body-thud, sub-bass) coincide con scale pop visual.

```javascript
// SFX impact timestamps (from sfx-spec.json)
const impacts = [
  { time: 30.0, sfx: 'white-flash', intensity: 1.0 },
  { time: 45.5, sfx: 'body-thud',   intensity: 0.8 },
];

impacts.forEach(({ time, intensity }) => {
  tl.to('#scene', {
    scale: 1.0 + intensity * 0.05,
    filter: `brightness(${1.0 + intensity * 0.2})`,
    duration: 0.1,
    ease: 'power3.out'
  }, time);
  tl.to('#scene', {
    scale: 1.0,
    filter: 'brightness(1.0)',
    duration: 0.3,
    ease: 'power2.in'
  }, time + 0.1);
});
```

### Cuándo usar audio-reactive

| Caso | Patrón recomendado |
|------|---------------------|
| Narración intensa | Narration onset → caption pop |
| Música atmosférica con beats | Beat sync flicker (sutil) |
| SFX impacto (white flash, thud) | SFX impact → visual punch |
| Climax sostenido | Volume → scale (heartbeat) |

### Anti-patterns audio-reactive

❌ **Sobre-react cada milisegundo:** parece glitch técnico. Sweet spot: reacción a peaks marcados, no continuo.

❌ **Audio-reactive en setup descriptivo:** el viewer no espera reacción visual aquí. Reservar para hooks + climax.

❌ **Intensity demasiado alta (scale >1.10):** se siente "earthquake". Sweet spot 1.03-1.07.

❌ **Asumir AudioContext funciona en render:** HyperFrames preview usa AudioContext, pero render headless puede no soportar. Pre-procesar curves y aplicar como tween.

---

## Parallax 3D — técnica core (post 2026-05-13)

> Universal en 6/7 referentes. **Hacer obligatorio** en cualquier shot con sujeto + background.

### Patrón validado

```html
<div class="scene-parallax clip" data-start="10" data-duration="6">
  <img class="layer-bg"  src="assets/h2-bg-blurred.jpg">
  <img class="layer-mid" src="assets/h2-character.png">
  <div class="layer-fg caption-name">BRUNO</div>
</div>

<style>
.scene-parallax {
  position: absolute;
  inset: 0;
  overflow: hidden;
}
.layer-bg, .layer-mid {
  position: absolute;
  inset: 0;
  object-fit: cover;
  will-change: transform;
}
.layer-bg  { z-index: 1; filter: blur(8px); }
.layer-mid { z-index: 2; }
.layer-fg  { z-index: 3; position: absolute; top: 25%; left: 50%; transform: translateX(-50%); }
</style>
```

```javascript
const T = 10, DUR = 6;
window.__timelines.main
  .fromTo('.layer-bg',  { x: 0, scale: 1.0 }, { x: -40, scale: 1.18, duration: DUR, ease: 'none' }, T)
  .fromTo('.layer-mid', { x: 0, scale: 1.0 }, { x: -15, scale: 1.08, duration: DUR, ease: 'none' }, T)
  .fromTo('.layer-fg',  { x: 0 },             { x:   5, duration: DUR, ease: 'none' }, T);
```

**Velocidad de cada layer:**
- `layer-bg`: -40px translation + 1.18 scale = moves the most (deeper depth perception)
- `layer-mid`: -15px translation + 1.08 scale = medium speed
- `layer-fg`: +5px translation = small parallax in opposite direction (caption appears stationary)

### Variantes

**POV walking forward:** todas las layers se mueven HACIA el viewer (scale up), velocidades distintas:
```javascript
tl.fromTo('.layer-bg',  { scale: 1.0 }, { scale: 1.30, duration: DUR }, T);
tl.fromTo('.layer-mid', { scale: 1.0 }, { scale: 1.15, duration: DUR }, T);
tl.fromTo('.layer-fg',  { scale: 1.0 }, { scale: 1.05, duration: DUR }, T);
```

**Reveal lateral:** todas las layers se mueven en eje X, velocidades distintas:
```javascript
tl.fromTo('.layer-bg',  { x: 0 }, { x: -60, duration: DUR }, T);
tl.fromTo('.layer-mid', { x: 0 }, { x: -30, duration: DUR }, T);
tl.fromTo('.layer-fg',  { x: 0 }, { x:   0, duration: DUR }, T);
```

### Cuándo aplicar (universal)

- **Medium shots con sujeto + background**: SIEMPRE (universal en referentes)
- **POV shots**: SIEMPRE (parallax depth essential)
- **Wide shots flat**: opcional (Ken Burns puede ser suficiente)
- **Detail close-ups**: opcional (subject ocupa casi todo el frame)

### Costo de implementación

Por shot: ~3-5 min adicionales. Por video (8-12 shots): ~30-60 min total.

**ROI:** alto. Parallax es la diferencia entre "video AI generado" y "video cinematográfico".

Cada formato puede definir su propio motion plan templateado. Por ejemplo `horror-choice-format/NARRATIVE-TEMPLATE.md` ya incluye una tabla "Plan de motion por escena" como parte del workflow V8-3.
