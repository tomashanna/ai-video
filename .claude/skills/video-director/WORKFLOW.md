# WORKFLOW.md — Disciplina secuencial

> La diferencia entre 8.5 y 9.5 NO es habilidad — es disciplina. Saltarse pasos siempre cuesta más al final.

---

## El loop maestro

```
┌───────────────────────────────────────────────────────────────┐
│                                                                │
│  1. LEER DOCS  →  2. PLANEAR  →  3. EJECUTAR  →  4. QA GEMINI │
│       ↑                                              │         │
│       │                                              ↓         │
│       └─────────── 5. ITERAR (si score <9.7) ───────┘         │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

No es opcional. Cada vez.

---

## Paso 1 — LEER DOCS (antes de cualquier código)

### Pregunta antes de tocar HTML/GSAP/audio:

| Si la tarea es… | Leé… |
|---|---|
| Bootstrap proyecto nuevo | `ai-video-production/BOOTSTRAP.md` |
| Generar TTS | `ai-video-production/PIPELINE.md` § 1 |
| Generar imágenes | `ai-video-production/PIPELINE.md` § 2 + `IMAGE-VARIETY.md` |
| Aplicar motion | `ai-video-production/MOTION-LAYER.md` |
| Captions / subtítulos | `ai-video-production/CAPTIONS.md` |
| SFX / sound design | `ai-video-production/SFX-PIPELINE.md` |
| Render | `ai-video-production/PIPELINE.md` § 5 |
| Música | `ai-video-production/PIPELINE.md` § 6 |
| QA / validación final | `ai-video-production/QA.md` |
| Formato horror-choice | `horror-choice-format/PAUTA.md` (entry point) |
| HyperFrames CLI | `hyperframes-cli` skill |
| GSAP API | `gsap` skill |

Si la doc no existe, escribila vos mientras ejecutás. Memoria viva.

### Excepción: tareas triviales

Si ya leíste la doc en esta sesión Y la tarea es 1 cambio aislado (ej: subir un volumen), podés saltearte. Pero si han pasado >50 mensajes o cambió el contexto, releé.

---

## Paso 2 — PLANEAR

Antes de tocar archivos, escribí mentalmente o en TaskCreate:

1. **Output esperado**: ¿cómo se mide éxito? (Gemini score, ffprobe specs, listening pass)
2. **Pasos secuenciales**: lista numerada. Si >5 pasos, usá TaskCreate.
3. **Riesgos**: ¿qué puede romperse? ¿qué es destructivo?
4. **Punto de no retorno**: ¿hay un momento donde si esto falla, perdimos tiempo / créditos?

### Cuándo usar TaskCreate

| Tarea | TaskCreate? |
|---|---|
| 1-2 ediciones triviales | No |
| Cambio + render + QA | Sí (3 tasks mínimo) |
| Proyecto nuevo bootstrap | Sí (>5 tasks) |
| Refactor multi-archivo | Sí |
| QA + iteración hasta 9.7 | Sí (1 task por iteración) |

---

## Paso 3 — EJECUTAR

### Reglas durante ejecución

1. **Una herramienta por vez salvo paralelo evidente.** Lecturas paralelas sí; renders en paralelo NO (SIGTERM).
2. **Verificá cada output antes del siguiente paso.** Si un audio salió de 4.2s, no asumas que es 4s.
3. **No re-leas archivos que acabás de editar** (la harness ya sabe el state).
4. **Updates breves al usuario** en momentos clave: "Encontré X." "Cambio de approach: Y." NO narres cada bash.

### Sub-loop para producción de assets — ORDEN CRÍTICO

```
0. ⭐ SHOT LIST FIRST — target 12-15 imágenes totales (NO 18-23)
   ↓
1. ANCHORS DE PERSONAJES PRIMERO (sin --ref)
   ↓
2. TTS por bloque de narración (atempo 2x después)
   ↓
3. ESCENAS CON PERSONAJES (usando anchors como --ref)
   ↓
4. ESCENAS SIN PERSONAJES (paisajes, objetos)
   ↓
5. SFX (buscar en library/ primero, generar solo lo faltante)
   ↓
6. MEDIR cada asset con ffprobe → Verificar → Wire en HTML
```

**⭐ Paso 0 — Shot list cap (regla 2026-05-11, mina-abandonada v8)**:

Antes de generar imágenes, escribí la lista completa de planos en `NARRATIVE.md` y **cap a 12-15 imágenes para un Reel ~90-100s**. Detalle en `ai-video-production/ANIMATION-LAYER.md` § Cantidad óptima de imágenes.

Razón: con >18 imágenes, la mitad termina <3s o detail puro = no-animable con Kling = filler Ken Burns inconsistente. Con 12-15, cada una aguanta tier Kling y el motion es consistente en TODO el video.

Distribución target (cualquier formato):
- 2-3 establishing wide
- 3-4 close-ups con expresión clave
- 3-4 POV con motion narrativo
- 2-3 detail con narrativa puntual

Si una imagen no pasa el decision tree de `ANIMATION-LAYER.md` § 1, **no la generes** — es filler.

**Por qué este orden**:
- Anchors PRIMERO → consistencia de personajes en todo el video (ver `ai-video-production/CHARACTER-CONSISTENCY.md`)
- TTS antes que captions → captions necesitan los audios para Whisper
- Escenas con personajes después de anchors → cada generación referencia al anchor
- SFX al final → ya sabés timings reales, podés buscar en library

Asset que no se midió = asset que va a salir mal en el render.

### Sub-loop para HTML/GSAP

```
Edit → Lint → AUDIT → render-lock acquire → Render draft → release → ffprobe specs
```

**5 gates OBLIGATORIOS — 3 antes del render + 2 después** (regla 2026-05-13 — actualizado para incluir qa-gate y audit-frames):

**ANTES de `npx hyperframes render`:**

**1. Lint** — `npx hyperframes lint`. Errores reales bloquean. Cubre schema/syntax.

**2. AUDIT narrativo** — `.venv/bin/python scripts/audit-narrative.py`. Cubre lo que lint NO:
- Imágenes con visibilidad efectiva <1s (anti-pattern)
- data-duration < GSAP opacity:0 timestamp (imagen cortada antes de tiempo)
- z-index conflicts (black-overlay tapando caption-wrap)
- Asset orphans

Setup en proyecto nuevo: `cp .claude/skills/ai-video-production/templates/scripts/audit-narrative.py scripts/`. Doc: `ai-video-production/AUDIT.md`.

**3. render-lock** — `.venv/bin/python scripts/render-lock.py acquire <project>`. Si otro agente está renderizando, este comando falla → hacer `wait` antes de continuar. Sin esto, FFmpeg muere con SIGTERM por CPU contention (aprendizaje amargo: 3 EPIPE consecutivos = 45 min perdidos).

**DESPUÉS del render draft, ANTES del stop point pre-animation:**

**4. AUDIT FRAMES** — `.venv/bin/python scripts/audit-frames.py --video renders/draft.mp4`. Detecta issues que Gemini holístico NO ve:
- UI overlap (countdown tapa imagen — caso isla-faro v1)
- Frames negros sin razón narrativa
- Character drift entre frames consecutivos
- Texto cortado o fuera de safe zone
- Captions overlap entre sí

Setup: `cp .claude/skills/ai-video-production/templates/scripts/audit-frames.py scripts/`. Costo: $0.10-0.20 con Gemini Vision Flash. Falla si >2 frames con issues.

**5. QA GATE pre-animation** — `.venv/bin/python scripts/qa-gate.py --score <X.X> --stage pre-kling --iteration <N>` (flag `--stage pre-kling` se preserva por compat con script). **BLOQUEA el stop point si score <9.7.** Forzá iteración con fixes NO-ANIMATION-AI (A→B→C — guion/captions/imágenes/wiring/mix, todo menos animar) hasta llegar a 9.7. Sin este gate, el agente productor puede reportar score bajo asumiendo "animation AI lo arregla" (anti-pattern documentado en isla-faro v1).

Setup: `cp .claude/skills/ai-video-production/templates/scripts/qa-gate.py scripts/`. Exit codes:
- `0`: passed, OK proceed to animation AI (modelo según MODEL-BENCHMARK)
- `1`: blocked, iterate with no-animation-AI fixes
- `2`: escalation required (3+ iter sin llegar a 9.7)

Comando completo del render con los 3 gates:

```bash
npx hyperframes lint && \
  .venv/bin/python scripts/audit-narrative.py && \
  .venv/bin/python scripts/render-lock.py acquire <project> || \
  .venv/bin/python scripts/render-lock.py wait <project> && \
  npx hyperframes render --output renders/vN.mp4 && \
  .venv/bin/python scripts/render-lock.py release
```

Si cualquier gate falla, el render NO arranca. **Cada gate cuesta <2s, ahorra hasta 12 min de re-render basura.**

### Sub-loop OBLIGATORIO: pick + COMPATIBILITY CHECK components (antes de tocar index.html)

> Para evitar feed predecible Y para evitar identidad visual incoherente DENTRO de un video.

```
1. Leer <formato>/video-log.md últimas 3 filas (qué componentes usaron videos previos)
2. Leer <repo-root>/elements.json (catálogo)
3. Excluir lo que el video anterior usó
4. Pick uno por categoría:
   - 1 countdown (pulse / glitch / slam) — el MISMO se usa en TODOS los countdowns del video
   - 1 loader (bar / radial / segments) — el MISMO se usa en TODOS los loaders del video
   - 1 lower-third (5 opciones) — solo si lo necesitás
5. ⭐ COMPATIBILITY CHECK (obligatorio antes de wire):
   a. Timing: countdown 3-3.5s → flash → loader 3-3.5s (SECUENCIALES, no overlap)
   b. Posición: countdown center / loader bottom 700px (no chocan)
   c. Estética: verificar contra matriz de ai-video-production/ELEMENTS-LIBRARY.md § Regla 2.3
      - Combos top: pulse+bar, glitch+segments, slam+segments
      - Combos a EVITAR: pulse+segments, glitch+bar, slam+radial
6. Wire al index.html via data-composition-src (NO hardcodear)
7. Anotar la selección en <formato>/video-log.md después del render
```

**Anti-pattern A**: hardcodear countdown/loader/lower-third sin chequear elements.json. Los 3 primeros videos lo hicieron mal.

**Anti-pattern B**: cambiar el countdown/loader entre dilemas del mismo video (ej: countdown-glitch en H2 y countdown-slam en H3). Rompe la identidad visual del video.

**Anti-pattern C**: ignorar el compatibility check estético. Combos chocantes confunden la identidad del feed.

Doc completo: `ai-video-production/ELEMENTS-LIBRARY.md`.

---

## Paso 4 — QA GEMINI + DIAGNOSIS CHECKLIST

> **El paso 4 NO es solo Gemini score.** Gemini detecta algunas cosas pero no todas (aprendizaje 2026-05-10: no detecta variedad visual real ni cortes narrativos). Por eso este paso combina **Gemini QA + diagnosis checklist de 8 categorías**.

### Obligatorio antes de declarar "terminado"

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/draft.mp4 \
  --prompt "$(cat /tmp/qa-prompt.txt)"
```

### Prompt base — 9 dimensiones universales

(ver `ai-video-production/QA.md` § Prompt UNIVERSAL)

Para formatos específicos: agregar dimensiones del formato. Horror-choice: agregar 4 dimensiones de `horror-choice-format/PAUTA.md` § 2 (claridad A/B, transición cliffhanger, choice labels, CTA).

### DIAGNOSIS CHECKLIST de 8 categorías — corre DESPUÉS de Gemini

Detalle completo de cómo chequear cada una: **`ai-video-production/QA.md` § AUTONOMOUS ITERATION LOOP**.

| # | Categoría | Fix doc |
|---|---|---|
| 1 | Variedad visual (shot types distintos, no variantes de la misma toma) | `IMAGE-VARIETY.md` |
| 2 | Capa SFX completa (flash + loading + tick + ambient + impacts) | `SFX-PIPELINE.md` |
| 3 | Cortes narrativos (taxonomía 7 tipos NARRATIVE-LED-EDITING) | `NARRATIVE-LED-EDITING.md` |
| 4 | Captions (overlaps, gaps, sync, legibilidad) | `CAPTIONS.md` |
| 5 | Motion (Ken Burns + extras) | `MOTION-LAYER.md` |
| 6 | POV continuity en wrong-choice cuts | `NARRATIVE-LED-EDITING.md` + `IMAGE-VARIETY.md` |
| 7 | Mix volumes canónicos | `SFX-PIPELINE.md` |
| 8 | Specs IG (h264, aac, 30fps, 1080×1920, ≤650MB) | `PIPELINE.md` § 5 |

### Cómo interpretar el score (con stop conditions del loop autónomo)

| Score | Acción |
|---|---|
| ≥9.7 + 8 categorías green | → HUMAN-CHECKLIST gate (siguiente) |
| <9.7 después de 3 iteraciones | 🚨 ESCALAR al usuario (vara 9.7 desde 2026-05-13 — antes era 9.5, antes era ship-pragmatic 9.2-9.5) |
| 9.0–9.4 antes de 3 iteraciones | Iterar 1 vez más, atacar la categoría más baja |
| 7.5–8.9 | Iterar agresivo. Hay 2-3 fixes claros. Refactor menor |
| <7.5 | Algo estructural roto. Revisar desde la raíz del NARRATIVE.md |
| <7.0 en cualquier iteración | 🚨 ESCALAR inmediato — estructural roto |

Detalle completo en `ai-video-production/QA.md` § STOP CONDITIONS.

### Paso 4.5 — HUMAN CHECKLIST (gate humano post-Gemini)

> **Gemini ≥9.7 es necesario pero NO suficiente.** Captura el 5-10% de issues que Gemini no flagea pero el ojo humano sí.

**Evidencia:** mina-abandonada v7c sacó Gemini 9.5 con un flash de imagen <1s claramente visible. El usuario lo detectó, Gemini no.

7 preguntas, ~2 min con auriculares. Detalle: **`HUMAN-CHECKLIST.md`**. Resumen operativo:

| # | Check |
|---|-------|
| 1 | ¿Alguna imagen <1s? |
| 2 | ¿Caption habla de algo que la imagen contradice? |
| 3 | ¿Espera >3s sin caption ni audio nuevo? |
| 4 | ¿Bridge narrativo antes del cliffhanger? |
| 5 | ¿Cambio real de mundo en la música del cliffhanger? |
| 6 | ¿CTA narrado con voz (no solo texto)? |
| 7 | ¿Final genera curiosidad / want-to-rewatch? |

Si hay ≥1 ✗ → iterar. Si todos ✓ → publicar.

---

## Paso 5 — ITERAR

### Después de QA, mapeá feedback → fix

Tabla de mapeo (extiende `QA.md`):

| Problema Gemini | Causa probable | Doc para fix |
|---|---|---|
| "Foto estática con zoom" | Falta variantes -a/-b/-c | `IMAGE-VARIETY.md` |
| "Diapositivas" | Falta motion | `MOTION-LAYER.md` |
| "Sonido pobre" | Falta capa SFX | `SFX-PIPELINE.md` |
| "Captions desincronizadas" | Hand-timing | `CAPTIONS.md` (Whisper) |
| "Texto ilegible en X" | Falta stroke | `CAPTIONS.md` (text-stroke 1.5px) |
| "Transición abrupta" | Falta whip cut con motion blur | `MOTION-LAYER.md` § glitch frame |
| "Saturación de la voz" | Volúmenes mal | `SFX-PIPELINE.md` mix table |
| "Plano largo aburre" | Duración >8s con 1 sola img | `IMAGE-VARIETY.md` 3 variantes |

### Reglas de iteración

1. **Cambio de mayor impacto primero.** No empieces por el detalle estético.
2. **Una iteración = un render.** No acumules 10 fixes antes de medir. Probá 2-3 y re-mide.
3. **Si la misma dimensión baja 2 iteraciones seguidas**, retrocedé al draft anterior. Estás empeorando algo.
4. **Documentar el camino.** Cada iteración deja una línea en el NARRATIVE.md o equivalente: "iter N: cambio X → score Y/10".

### Cuándo cortar la iteración — stop conditions del loop autónomo

Detalle completo en `ai-video-production/QA.md` § STOP CONDITIONS. Resumen:

- **Score ≥ 9.7 + 8 categorías green** → STOP, declarar terminado
- **Score < 9.7 después de 3 iteraciones** → 🚨 ESCALAR al usuario con análisis dimensión-por-dimensión:
  > "Llevamos 3 iteraciones sin llegar a 9.7. Score actual: <X>. Las categorías bajas son <Y, Z> con causa probable <W>. Las opciones son: regenerar K imágenes (10 min + $0.30) / aplicar Kling en N planos críticos ($0.70-2.50) / rediseñar M desde NARRATIVE (30 min). ¿Cuál?"
  > **NO publicar sub-9.7 bajo ninguna circunstancia.** La vara se subió de 9.5 → 9.7 el 2026-05-13 tras validar que es el piso necesario para one-shot quality reproducible.
- **Score < 7.0** en cualquier iteración → ESCALAR inmediato (estructural)
- **Mejora <0.1 entre 2 iteraciones consecutivas** → ESCALAR (diminishing returns)

---

## Flujos típicos completos

### Flujo A: Proyecto nuevo desde cero

```
0. Verificar voice ID + STYLE_SUFFIX en scripts/    [BOOTSTRAP.md]
1. Escribir NARRATIVE.md con script + asset plan     [horror-choice-format/SCRIPT-WRITING-GUIDE.md]
2. Generar imágenes (paralelo) + variantes -a/-b/-c  [IMAGE-VARIETY.md]
3. Generar TTS → atempo 2x → medir duraciones        [PIPELINE.md § 1]
4. Calcular timing real de cada hito                 [PIPELINE.md § 10]
5. Generar SFX vía sfx-spec.json                     [SFX-PIPELINE.md]
6. Procesar música (2-pass, no -ss + -af)            [PIPELINE.md § 6]
7. Whisper batch sobre todos los audios              [CAPTIONS.md]
8. Construir index.html con HTML + GSAP              [horror-choice-format/VIDEO-PLAYBOOK.md]
9. Aplicar motion layer                              [MOTION-LAYER.md]
10. Lint                                             [`npx hyperframes lint`]
11. Render draft                                     [PIPELINE.md § 5]
12. Gemini QA                                        [QA.md]
13. Iterar hasta ≥9.7                                [WORKFLOW.md § Paso 5]
14. Render final quality high
15. Verificar specs ffprobe (h264/aac/30fps/1080×1920)
```

### Flujo B: Iteración sobre video existente

```
1. Identificar qué bajó el score en Gemini QA previa
2. Mapear feedback → doc específica
3. Aplicar fix mínimo necesario
4. Lint
5. Render
6. Gemini QA
7. Si subió → siguiente fix de la lista. Si bajó → revertir
```

### Flujo C: Audit de un video "estrella" (reverse engineering)

```
1. Leer index.html completo del video estrella
2. Anotar cada decisión técnica vs lo que dicen las docs
3. Si decisión existe en docs → confirmar canónica
4. Si decisión NO existe en docs → agregarla
5. Si decisión contradice docs → entender por qué, actualizar la doc o la decisión
6. Final: las docs y el video estrella deben estar 100% en sync
```

---

## Anti-workflows (lo que NO hacés)

| ❌ Mal | ✅ Bien |
|---|---|
| "Voy a empezar a editar" sin leer docs | "Primero leo MOTION-LAYER.md, después edito" |
| Render sin lint previo | Lint → Render |
| Whisper sin medir duraciones | Medir → Calcular offsets → Whisper |
| 5 fixes en una iteración sin medir | 2-3 fixes → render → Gemini → siguientes |
| Dos renders en paralelo | Sequential. Wait until done. |
| "Mejorá esto" sin métrica de éxito | "Score Gemini de 8.8 → meta 9.7" |
| Inventar pattern cuando hay doc | Buscar pattern → si no existe, inventar Y documentar |
