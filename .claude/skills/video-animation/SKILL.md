---
name: video-animation
description: ANIMACIÓN AI image-to-video (multi-model — Kling/Seedance/Hailuo según MODEL-BENCHMARK) — última capa del pipeline. Activar SIEMPRE que la tarea mencione: animar, animación, Kling, Replicate, image-to-video, "darle vida al video", "convertir imágenes en clips". Cubre decision tree, duration matching tier 5s/10s, prompt engineering, integración HTML, sync narrador, costo + retries. NUNCA activar sola — siempre en combo con `video-director` (workflow + quality bar) + `ai-video-production` (motion CSS + QA) + skill del formato si aplica. Fase MÁS CARA del pipeline ($5-9/video).
---

# Video Animation — Replicate Kling pipeline

## ⛔ LECTURA OBLIGATORIA al activar esta skill

Si activaste esta skill, leé estos archivos ANTES de planear o ejecutar:

1. **`docs/OPERATING-MANUAL.md`** — context global + hard rules
2. Este archivo (`SKILL.md`) entero — identidad + hard rules de animación
3. **`.claude/skills/video-animation/ANIMATION-LAYER.md`** — doc maestro 12 secciones (decision tree, duration matching, loop strategy, prompt engineering, asset prep, integración HTML, sync narrador, costo+retries, audio, workflow, checklist, anti-patterns)
4. **`<proyecto>/index.html`** — state actual del HTML donde se integrarán los clips
5. **`<proyecto>/NARRATIVE.md`** — timing + asset list (necesario para duration matching)

**ACTIVÁ EN PARALELO obligatoriamente:**
- **`video-director`** — workflow + quality bar + Gemini QA gate previo (no animar hasta ≥9.0)
- **`ai-video-production`** — motion CSS complementario (Ken Burns + parallax) + QA post-animación + character consistency
- Si el video es del formato horror-choice: **`horror-choice-format`** — override H1 con Kling tier 5s loopable atmospheric

**PRE-CONDICIÓN no-negociable:** el render base debe pasar Gemini QA ≥ 9.0 con estáticas + Ken Burns ANTES de animar. Animar amplifica errores narrativos. Si el shape del video no está validado, primero validar.

**NO planees ni ejecutes hasta haber leído ANIMATION-LAYER.md entero + el index.html + NARRATIVE.md del proyecto.**

**Plan-First Rule estricta:** cada clip Kling cuesta $0.35-0.70. Antes de generar batch, presentar plan en tabla `| imagen | scene_dur | tier | prompt | loopable | costo |` con total estimado, y esperar aprobación.

---


> Sos el especialista en animar imágenes estáticas. Pasamos de "Ken Burns sobre fotos" a **escenas vivas**. Es la diferencia entre presentación y cine.

---

## Cuándo se activa este skill

- "Animar video X" / "Animar mina-abandonada"
- "Convertir imágenes en clips"
- "Usar Kling" / "Replicate" / "video-AI"
- "Darle vida al video"
- Cualquier tarea de generar MP4s desde PNGs

**No se activa solo para**:
- Motion CSS (Ken Burns / parallax / flicker) — eso es `ai-video-production/MOTION-LAYER.md`
- Edición de video existente sin agregar Kling

---

## Quality bar de animación

| Métrica | Target |
|---|---|
| **Animación con Kling** | 8-10 imágenes de las 12-15 del video (no animar todo) |
| **Duration matching** | scene_duration + 0.5s buffer ≤ kling_duration |
| **Tier Kling** | 5s o 10s (fijos — no continuo) |
| **Costo realista** | $5-9 por video (incluyendo 1.5x retries) |
| **Quality variance** | Aceptable 3 retries por clip antes de abandonar |
| **Pre-render check** | Cada clip revisado individualmente ANTES de integrar |

---

## Hard rules (no negociable)

1. **NO animar antes de Gemini QA ≥ 9.0 con estáticas + Ken Burns.** Animá sobre un "shape" del video ya validado. Si la narrativa o el timing está mal, animar lo amplifica.
2. **Duration matching obligatorio.** scene_duration + 0.5s buffer → next tier. Sino frame congelado o loop visible.
3. **NO animar todo.** Wide establishing shots + detail shots → Ken Burns suficiente. 8-10 de 15 imágenes es óptimo. **Excepción crítica:** regla #9 abajo (los primeros 30s).
4. **Imagen para Kling = PNG raw sin CSS filter.** El filter se aplica en HTML después.
5. **Pre-render check por clip ANTES de wire al HTML.** Detectar fallos Kling antes del render del video completo.
6. **Sync motion clave con narrador.** Si el clip tiene acción narrativa, debe ocurrir cuando el narrador lo dice.
7. **Loop solo en contenido estructuralmente loopable.** Niebla, fuego, polvo. NUNCA personajes con gestos.
8. **3 retries máximo por clip.** Después, aceptar el mejor o dejar estático.
9. **⛔ Primeros 30s = 100% Kling.** Toda escena con `data-start < 30s` debe ser un clip Kling, sin excepción de tipo de plano. Ni Ken Burns ni estática aceptables. **Razón:** retención crítica en los primeros 30s del Reel. Detalle: `ANIMATION-LAYER.md` § 1 PRE-GATE.

---

## Documentos en este skill

| Doc | Cuándo leerlo |
|---|---|
| **`SKILL.md`** | Punto de entrada (este). Identidad + hard rules. |
| **`ANIMATION-LAYER.md`** ⭐ | Doc maestro completo. 12 secciones cubren: decision tree, duration matching, loop strategy, prompt engineering, asset prep, integración HTML, sync narrador, costo+retries, audio, workflow, checklist, anti-patterns. |

---

## Workflow rápido — referencia

> Detalle completo en `ANIMATION-LAYER.md` § 10 (workflow recomendado).

```
PRE: video ya pasó Gemini QA ≥ 9.0 con estáticas + Ken Burns
     (NO animar hasta que el "shape" esté validado)

1. Listar imágenes para Kling (8-10 de las 12-15)
   → Para cada una: tipo de plano + duración + complejidad acción

2. Decision tree (ANIMATION-LAYER § 1)
   ✅ Close-up rostro, twist, cliffhanger, partículas, personaje con gesto
   ❌ Wide establishing, detail shot estático, POV fallen

3. Calcular tier por imagen (ANIMATION-LAYER § 2)
   scene_duration + 0.5s → next tier (5s o 10s)

4. Diseñar prompt Kling (ANIMATION-LAYER § 4)
   → Sujeto + verbo específico + dirección + atmósfera
   → Una acción por prompt

5. Verificar setup técnico
   - REPLICATE_API_TOKEN en .env
   - ai-video video disponible (copiar de templates si no existe)

6. Generar clips en batch (paralelo si la API lo permite)
   uv run ai-video video \
     -i assets/scene-source.png \
     -p "prompt aquí" \
     -o assets/scene.mp4 \
     --duration 5  # o 10

7. Pre-render check de cada clip ANTES de wire HTML
   - Abrir cada .mp4 generado
   - Verificar quality (no derretimiento, no manos raras, motion coherente)
   - Reintentar fallidos (max 3 intentos)

8. Reemplazar <img> por <video> en index.html
   - autoplay muted playsinline
   - SIN loop excepto atmospheric loopables
   - mismo data-start / data-duration / data-track-index

9. Render draft del video animado completo

10. Gemini QA + diagnosis checklist
    → Si algún clip se siente truncado/looped visible → flag y reintentar

11. Render final --quality high
```

---

## Setup en proyecto

### Verificar antes de empezar

```bash
# 1. REPLICATE_API_TOKEN configurado
grep -q REPLICATE_API_TOKEN .env || echo "❌ Falta REPLICATE_API_TOKEN en .env"

# 2. ai-video video existe
uv run ai-video video --help >/dev/null  # tool del paquete, nada que copiar

# 3. replicate package instalado
.venv/bin/pip list 2>/dev/null | grep -q replicate || .venv/bin/pip install replicate
```

### Si falta ai-video video

Copiar de referencia:
```bash
cp ~/AI\ video\ 1/elige-companero/scripts/video.py \
   <tu-proyecto>/scripts/video.py
```

El script:
- Modelo: `kwaivgi/kling-v2.0`
- Parámetro de imagen: `start_image` (NO `image`)
- cfg_scale: 0.5
- Soporta `--duration 5` o `--duration 10`

---

## Anti-patterns (resumen — detalle en ANIMATION-LAYER.md § 12)

- ❌ **Animation duration < image-on-screen duration** → frame congelado
- ❌ **Loop con personaje haciendo gesto** → snap-back visible
- ❌ **Múltiples acciones en un prompt Kling** → falla previsible
- ❌ **Aplicar filter CSS antes de Kling** → Kling necesita PNG limpio
- ❌ **Descubrir fallas en render final** → 15 min perdidos
- ❌ **Animar TODO** → caro, innecesario, wide shots no ganan nada
- ❌ **Animar antes de validar shape con Gemini** → amplificás errores narrativos

---

## Costo orientativo

| Concepto | Costo |
|---|---|
| Clip Kling tier 5s | ~$0.35 |
| Clip Kling tier 10s | ~$0.70 |
| Video típico (8-10 animados × tier mixto) | $4-7 base |
| **+ Retries 1.5x** | **$6-10 budget realista** |

Plan-First Rule (`docs/OPERATING-MANUAL.md` de cada proyecto): proponer plan antes de generar clips. Cuesta créditos.

---

## Aplicación por formato

| Formato | Override animación |
|---|---|
| **horror-choice** | H1 (presentación) **siempre Kling tier 5s loopable atmospheric** — niebla/velas, sin character motion |
| **documental** (futuro) | Decision tree estándar |
| **educacional** (futuro) | Solo close-ups de diagramas / objetos clave |

---

## Cross-references

- `ai-video-production/PIPELINE.md` § 9 — comando base + voice rules
- `ai-video-production/MOTION-LAYER.md` — motion CSS (NO Kling). Complementario.
- `ai-video-production/IMAGE-VARIETY.md` — variantes -a/-b/-c (cada variante animada con Kling preserva consistency)
- `ai-video-production/CHARACTER-CONSISTENCY.md` — anchors siguen aplicando antes de Kling
- `ai-video-production/QA.md` — Gemini QA post-animación
- `video-director/STARTER-PROMPTS.md` § #11 — prompt copy-paste para animación

---

## Validado en

- **elige-companero v1** — 9 prompts Kling exitosos. Aprendizaje: duration mismatch (5s anim para 7s scene) → corregido en v2 con esta doc.
- **mina-abandonada v7d** — pendiente animación con Kling sobre el render base 10/10.
- **bosque-abandonado v2** — sin Kling todavía. Candidato a animación selectiva post-publicación primer batch.

---

## Última actualización

2026-05-11. Inicial. Skill independiente creada después de aprender que `ANIMATION-LAYER.md` dentro de `ai-video-production/` no se auto-activaba con triggers de animación. Ahora vive como skill propia con description auto-trigger.
