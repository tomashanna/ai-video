# MICRO-COMPOSITION-WORKFLOW.md — Validar cambios estructurales antes de tocar `index.html` completo

> Cuando vas a hacer un cambio que afecta el timing de toda la composición (acortar/extender una sección, agregar un nuevo plano hook, restructurar el intro), **NO toques `index.html` directamente**. Construí una micro-composición standalone, validala, e integrá después.

---

## Por qué importa

Cambios estructurales sobre `index.html` completo (típico 80-100s, 100-200 elementos) tienen problemas en cascada:

1. **Render lento**: 5-10 min por iteración. Iterar 3 veces = media hora perdida.
2. **Diagnóstico difícil**: si algo se rompe en el frame 7, ¿es el nuevo cambio o un side-effect en H4?
3. **Refactor irreversible**: shifteás 50 data-start values y descubrís que el design no convencía. Volver al estado anterior es manual.
4. **Costo Kling**: si la nueva idea requiere regenerar assets pero no convence, perdiste créditos.

La micro-composición es una HTML standalone de 5-15s que aísla la sección bajo cambio. Renderiza en ~30s, valida con Gemini + frame extraction, e iterás hasta ≥9.7 antes de tocar nada más.

---

## Cuándo usar

✅ **Sí usar micro-composición**:
- Reestructurar el intro (acortar de 19s a 9s)
- Probar un hook visual nuevo antes de comprometer assets
- Validar transición entre dos hitos
- Testear un cambio de tipografía en CTAs
- Probar pacing del countdown

❌ **NO usar micro-composición** (editar `index.html` directo es OK):
- Cambiar texto de un caption (no afecta timing)
- Subir/bajar volumen de un SFX
- Reemplazar un asset por su versión animada (mismo data-duration)
- Fixes de continuidad de captions sin shift

---

## Workflow

### 1. Crear `<seccion>-preview.html` PARTIENDO DE `index.html`

⚠️ **NO copy-pastear CSS de a piezas.** El boilerplate de HyperFrames tiene gotchas que pueden romper silenciosamente (ver `HYPERFRAMES-GOTCHAS.md` § 1).

```bash
cp index.html intro-preview.html
```

Luego stripear lo no-relevante:
- Eliminar elementos `<video>`/`<img>`/`<audio>` cuyo `data-start` esté fuera de la ventana
- Eliminar los `tl.set/tl.to` del GSAP correspondientes
- Cambiar `data-duration` del `#root` a la duración de la micro (e.g., 9s)
- Mantener intactos: estilos CSS, scripts CDN, capas overlay (vignette, grain, tint), keyframes

### 2. Asegurarse del boilerplate correcto del timeline

El `<script>` SIEMPRE cierra con:

```js
      window.__timelines = window.__timelines || {};
      window.__timelines.main = tl;
```

NO `window.__hyperframes_timeline__` ni similar. NO `tl.play(0)` manual.

### 3. Render rápido

```bash
npx hyperframes render -c <seccion>-preview.html -o renders/<seccion>-preview-vN.mp4
```

Render típico de 9s: ~30s wall-clock. Render típico de 15s: ~50s.

### 4. Gemini QA (umbral 9.7)

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/<seccion>-preview-vN.mp4 \
  --prompt "Analiza esta [duración]s de [formato + sección]. Cambios desde versión anterior: (a)... (b)...

Crítica honesta:
(1) [Pregunta específica al fix aplicado]
(2) ...
(10) Continuidad narrativa: ¿la última frase visual/audible conecta con lo que el viewer espera en los próximos 5s del video completo?
(11) Inventario de elementos UI: lista CADA texto/UI con timestamp aprox.

Dame score 1-10 honesto. Umbral 9.7 — si está abajo lista 3 problemas mayores."
```

### 5. Frame extraction (anti-alucinación obligatoria)

```bash
# Para cada elemento UI esperado en la ventana, extraer frame al timestamp medio
for t in <timestamps>; do
  ffmpeg -y -ss $t -i renders/<seccion>-preview-vN.mp4 -frames:v 1 -q:v 3 "/tmp/check-t${t}.jpg" -loglevel error
done
# Read cada JPG y confirmar presencia visual del elemento
```

### 6. Iterar hasta ≥9.7 (máximo 3 iteraciones)

Por cada iteración:
- Listar las 3 mejoras concretas que Gemini sugirió
- Aplicar (al HTML preview, no al index.html principal)
- Re-render, re-QA, re-frame-check

### 7. ⭐ Join-point QA antes de integrar (CRÍTICO)

Antes de tocar `index.html` con el cambio aprobado, renderizar un **join-test**: últimos 3s de la micro + primeros 5s de la composición principal post-integración.

```bash
# Pseudo-código del join-test
# 1. Crear join-test.html con shift -10s (o el shift que toque) aplicado solo a 0-15s del index
# 2. Render
# 3. Gemini QA específicamente sobre el segundo crítico de unión
```

Validar:
- ¿La última caption de la micro choca con la primera caption de H3? (caso real: "SI ELEGISTE A HUGO..." en intro + cap-h3-n1 "SI ELEGISTE A HUGO," — son la misma frase, debe ser una sola).
- ¿La música de la micro corta abruptamente cuando empieza el track principal?
- ¿La narración de la micro termina exactamente cuando empieza la siguiente narración?
- ¿El último frame visual de la micro hace match con el primer frame del bloque siguiente?

### 8. Solo después: integración a `index.html`

Aplicar el cambio aprobado al `index.html` completo. Shift de timings con sed/edit cuidadoso. Render completo. Gemini QA del video entero (no solo de la sección).

---

## Anti-patterns

- ❌ **Editar `index.html` con un cambio estructural y rendir 5 min para "ver qué tal"**. Caro y lento.
- ❌ **Construir el preview HTML copy-pasteando CSS** en lugar de stripear de `index.html`. Riesgo de bugs sutiles tipo namespace de timeline.
- ❌ **Declarar micro-composición lista y saltar al index.html sin join-point QA**. La micro puede ser 9.7/10 standalone pero la integración 7/10.
- ❌ **Hacer la micro-composición demasiado corta** (e.g., 3s). Pierde la chance de validar pacing real. Mínimo recomendado: **5s** para una transición; **9-12s** para un intro completo.

---

## Costo orientativo

Por iteración de micro-composición (9s):
- Render HyperFrames: ~30-50s wall-clock, despreciable
- Gemini QA: ~30s + $0.05
- Frame extraction: ~5s
- Mi atención: ~3-5 min revisando

Total ~5 min + $0.10 por iteración. Vs render completo del index (~5-10 min + $0.20 Gemini) — 2x más caro por iteración. Pero si necesitás 3 iteraciones, la micro es muchísimo más barata (5 vs 30 min).

---

## Aprendido en

**mina-abandonada intro v1-v6 (2026-05-11)**: redujimos intro de 19s a 9s + agregamos teaser hook + Kling con `end_image`. Hicimos 6 iteraciones de micro-composición (renders/intro-preview-v1 a v6) antes de tocar `index.html`. Costo total ~$1.50. Si hubiéramos tocado el index directo cada iteración: 6 × 10 min de render = 1 hora + 6× los créditos.

---

## Cross-references

- `HYPERFRAMES-GOTCHAS.md` § 1 — boilerplate correcto del timeline
- `QA.md` — protocolo Gemini + frame extraction
- `video-director/ANTI-PATTERNS.md` § Workflow — "Construir micro-composición desde cero" + "Validar sin testear join point"
