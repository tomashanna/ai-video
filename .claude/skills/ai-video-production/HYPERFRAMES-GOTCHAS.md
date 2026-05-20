# HYPERFRAMES-GOTCHAS.md — Bugs sutiles que cuestan horas si no los conocés

> Patrones de falla silenciosa de HyperFrames descubiertos en producción. Ninguno tira error explícito; el render "funciona" pero faltan elementos o aparece negro.

---

## 1. Timeline registration namespace

### El bug

GSAP timeline construido con `paused: true` pero registrado mal:

```html
<!-- MAL — namespace inventado, HyperFrames lo ignora -->
<script>
  const tl = gsap.timeline({ paused: true });
  tl.set("#cnt-3", { opacity: 1 }, 5.7);
  tl.set("#cnt-3", { opacity: 0 }, 6.2);
  // ... 30 líneas más de tl.set/tl.to ...
  window.__hyperframes_timeline__ = tl;  /* ← MAL */
  tl.play(0);                            /* ← MAL (redundante e inútil) */
</script>
```

### Síntoma

El render se ejecuta sin errores. Pero **NINGÚN elemento controlado por GSAP aparece**: countdown numbers, labels, captions hardcoded, cap-chose, todos quedan en su `style="opacity:0"` inline. Música, narración y videos sí funcionan (esos son controlados por el sistema de HyperFrames vía `data-start`/`data-duration`, no por GSAP).

Gemini Video Analyzer puede no detectarlo y reportar elementos visibles que no están (ver `QA.md` § "Gemini ALUCINA").

### El fix exacto

```html
<script>
  const tl = gsap.timeline({ paused: true });
  // ... tl.set/tl.to ...

  window.__timelines = window.__timelines || {};
  window.__timelines.main = tl;
</script>
```

HyperFrames busca específicamente `window.__timelines.main` (o `.<composition-id>` si registraste más de una). Cualquier otro nombre se ignora silenciosamente. **NO necesitás llamar `tl.play(0)`** — HyperFrames hace seek por frame al timestamp correspondiente.

### Cómo detectarlo en una micro-composición

Extraer frame al timestamp donde DEBERÍA aparecer un elemento GSAP-controlado (countdown 3 a t=5.95s, cap-chose a t=8.0s, etc) y verificar visualmente. Si no aparece → revisar namespace antes de iterar timings.

**Aprendido en**: mina-abandonada intro v2→v4 (2026-05-11). 3 renders perdidos.

---

## 2. Video element con `data-duration` > duración real del .mp4 → fondo NEGRO

### El bug

```html
<!-- Clip Kling es 5s, pero composición lo extiende a 9s -->
<video src="assets/h1-approach.mp4"
       data-start="0" data-duration="9"></video>
```

### Síntoma

Frames 0-5s: video se reproduce normalmente.
Frames 5-9s: **NEGRO TOTAL** (no hold del último frame).

### Por qué pasa

HyperFrames no extiende el video element con last-frame hold. Cuando el `<video>` HTML5 termina su contenido nativo, el frame compositor recibe transparencia y se ve el background del root (negro `#000000`).

### Fix #1 (recomendado): extender el .mp4 con ffmpeg

```bash
ffmpeg -y -i assets/clip.mp4 \
  -vf "tpad=stop_mode=clone:stop_duration=4" \
  -an assets/clip-9s.mp4
```

`tpad stop_mode=clone` clona el último frame por la duración pedida. `-an` elimina audio (no aplica a clips Kling silentes pero costumbre).

### Fix #2: usar tier Kling más alto

Si scene_duration es ~9s pedir tier 10s a Kling. Cuesta el doble pero mantiene un único asset.

### Fix #3: añadir un `<img>` con el last-frame extraído

```bash
ffmpeg -y -sseof -0.1 -i assets/clip.mp4 -frames:v 1 assets/clip-lastframe.png
```

Luego en HTML: `<img src="...-lastframe.png" data-start="5" data-duration="4">` superpuesto en el mismo track-index.

### Cómo detectarlo

Frame extraction a `(clip_duration + 1s)`. Si negro → fix.

**Aprendido en**: mina-abandonada intro v2→v3 (2026-05-11). Gemini lo detectó como "fundido a negro elegante" — confirmar siempre con frame propio.

---

## 3. Lint warnings que NO bloquean pero deben revisarse

Después de `npx hyperframes lint`, además de errores (que SÍ bloquean), hay warnings que el render ignora pero pueden afectar calidad:

| Warning | Significa | Cuándo importa |
|---|---|---|
| `gsap_exit_missing_hard_kill` | Un fade-to-opacity-0 sin `tl.set` duro después | Solo importa si HyperFrames hace non-linear seeking. En render lineal estándar suele ser inocuo. |
| `composition_self_attribute_selector` | CSS selector usa el id del propio root | Solo importa si el root se embebe en otra composición. Para projects standalone es OK. |
| `composition_file_too_large` | HTML >400 líneas | Importa para legibilidad y diff. No para render. |

**Regla**: leer todos los warnings antes del primer render del proyecto. Después, si no cambiaron las estructuras relevantes, se pueden ignorar.

---

## 4. Lint flag `--strict` y `--strict-all`

- `--strict`: convierte ERRORS en bloqueo (default ya bloquea errores, este flag es redundante)
- `--strict-all`: convierte WARNINGS en bloqueo también

**Cuándo usar `--strict-all`**: render final antes de publicar. Si pasa con `--strict-all`, sabés que el HTML está limpio. Para iteraciones intermedias **NO usar** — bloquea por warnings inocuos.

---

## 5. `data-duration` en elementos `<div>` SIN `class="clip"`

```html
<!-- MAL — sin class="clip" -->
<div id="cap-chose" data-start="7" data-duration="2">SI ELEGISTE A HUGO</div>
```

HyperFrames no aplica `data-start`/`data-duration` a divs sin `class="clip"`. El elemento queda siempre visible (o controlado solo por GSAP).

```html
<!-- BIEN — con class="clip" -->
<div id="cap-chose" class="caption caption-abs clip" data-start="7" data-duration="2">SI ELEGISTE A HUGO</div>
```

**Caso especial captions**: a veces se prefiere dejar **sin** `class="clip"` y controlar visibilidad solo por GSAP (`tl.set opacity 1/0`). Eso funciona, pero exige que el GSAP timeline esté correctamente registrado (ver § 1).

---

## 6. Render de composición distinta a `index.html`

```bash
# CORRECTO: flag corto -c o --composition
npx hyperframes render -c intro-preview.html -o renders/intro.mp4

# INCORRECTO: --entry o --file no existen
npx hyperframes render --entry intro-preview.html  # ERROR: "Not a directory: ..."
```

Si la composición vive en `compositions/intro.html` y referencia componentes vía `<template data-composition-src>`, ver doc oficial sobre sub-compositions.

---

## Última actualización

2026-05-11. Inicial. Tras intro mina-abandonada v1-v6.
