# Template — elige-tu-companero

> ⛔ **ARQUITECTURA ACTUALIZADA 2026-05-23 Sub-Fase 3A.** La PAUTA canónica de este formato vive en **`horror-choice-format/PAUTA-MASTER.md`** (8 videos virales canónicos empíricos) + `PATTERNS.md` + `SCRIPT-WRITING-GUIDE.md` + `PAUTA.md`. Los docs en ESTE folder son **operacionales secundarios** — NO autoridad creativa.
>
> ⚠️ **`CREATIVE-BRIEF.md` fue DEPRECATED 2026-05-13 PM** (mal-grounded en V1/V2/V3 antiguos + V7 nuestro). Movido a `_archive-deprecated-docs/` durante Sub-Fase 3A. NO USAR como autoridad — solo histórico.

---

## ⛔ LEER PRIMERO (orden estricto)

Antes de tocar nada de este folder, leer EN ORDEN:

1. **`../../horror-choice-format/PAUTA-MASTER.md`** — PAUTA CANÓNICA ACTUAL (autoridad empírica de 8 videos virales)
   - § 0 Metodología (los 8 videos = única fuente)
   - § 1 Filosofía ("el formato es generador, no límite")
   - § 2 Estructura temporal empírica (range duración real 76-129s)
   - § 3 Reglas inviolables con compliance N/8
   - § 4 Hallazgo: personajes recurrentes cross-video (Pablo, Axel, Enzo rotan rol)
   - § 5 Hallazgo: bueno aparente puede ser visualmente extreme
   - § 6 Hallazgo: "opción ganadora contra impulso" NO es universal
   - § 7 Slot A — 8 escenarios empíricos
   - § 8 Slot B — visual malo aparente (6 plantillas validadas)
   - § 9 Slot C — visual bueno aparente
   - § 10 Slot D — dinámica de control del malo
   - § 11 Slot E — dilemas
   - § 12 Slot F — body horror específico
   - § 13 Slot G — cliffhanger archetype (Paz perdida domina 7/8)
   - § 14 Slot H — ambient creatures
   - § 15 Patterns narrativos observados (P1, P2, P3, P6, P9)
   - § 16 Checklist de calidad
   - § 17 Reglas de rotación

2. **`../../horror-choice-format/canonical-scenes/INDEX.md` + ref-XX.md** (shot-by-shot empírico per pattern)
3. **`../../horror-choice-format/PATTERNS.md`**
4. **`../../horror-choice-format/SCRIPT-WRITING-GUIDE.md`**
5. **`../../horror-choice-format/PAUTA.md`**
6. **`../../horror-choice-format/INTRO-FORMULA.md`** (renamed from INTRO-FORMULA-V15.md 2026-05-23 Hard Rule #19)
7. **`../../horror-choice-format/CHARACTER-NAMES-CATALOG.md`**
8. **`../../horror-choice-format/video-log.md`** (rotación pattern obligatoria)
9. **`../../creative-director/templates/CREATIVE-SPEC-TEMPLATE-v11.yaml`** (schema template para SPEC output)
10. **`../../video-director/MODEL-BEHAVIOR-LOG.md`** (model constraints architect MUST design within, added 2026-05-22)

---

## Docs operacionales en este folder

Estos docs **NO contienen reglas creativas** — solo cómo IMPLEMENTAR técnicamente lo que la PAUTA dicta. Si encontrás conflicto entre estos docs y la pauta canónica, **gana la pauta canónica siempre**.

| Doc | Función operacional | Pauta relacionada |
|-----|---------------------|-------------------|
| `aesthetic.md` | Dirección CSS color (warm/cool LUTs) | PAUTA-MASTER § 7 Slot A iluminación |
| `audio-direction.md` | Dirección audio (música/SFX/ducking intent) | PATTERNS § 2 AUDIO + Slot F SFX |
| `captions.md` | Sistema 3 clases captions (name/narration/warning) | PATTERNS § 3 visual + V7-1 stroke |
| `camera-and-shots.md` | Tipos de planos + motion direction | PATTERNS § 3 VISUAL + V8-3 motion |
| `image-direction.md` | Per-shot framework + anchor prompts | PAUTA-MASTER § 8 Slot B + § 9 Slot C plantillas |
| `animation-direction.md` | Animation tier strategy (HERO/STANDARD/DRAFT) + cost optimization | PATTERNS § 10.5 + MODEL-BENCHMARK + creative-director/SKILL.md § TIER ASSIGNMENT PER SHOT |
| `script-writing.md` | Formato unified script YAML (target_duration + pause_strict) | SCRIPT-WRITING-GUIDE plantilla maestra |
| `ui-elements.md` | UI specifics (countdown, loading bars, choice buttons) | V7-2 choice labels + V7-3 separador |
| `shared-universe.md` | Cross-video continuity (recurring characters, easter eggs) | PAUTA-MASTER § 4 personajes recurrentes + § 14 Slot H ambient creatures |

---

## Lo que ELIMINADO (eran duplicados de la pauta)

Estos docs que existían antes ahora están eliminados porque duplicaban contenido canónico:

- ❌ `characters.md` → ver Slot B + Slot C en PAUTA-MASTER §§ 8-9
- ❌ `plot-patterns.md` → ver PAUTA-MASTER § 15 patterns observados
- ❌ `story-arc.md` → ver PAUTA-MASTER § 1 DNA + PATTERNS § 1 estructura
- ❌ `hooks.md` → ver INTRO-FORMULA.md
- ❌ `environments.md` → ver PAUTA-MASTER § 7 Slot A (8 escenarios empíricos)
- ❌ `counterfactual-outros.md` → ver PAUTA-MASTER § 13 cliffhanger archetypes
- ❌ `stakes-catalog.md` → ver PAUTA-MASTER § 12 Slot F body horror
- ❌ `narrator-voice.md` → ver PAUTA-MASTER § 3 reglas + SCRIPT-WRITING-GUIDE
- ❌ `anti-patterns.md` → ver PAUTA-MASTER § 16 checklist + AUDITOR-PROTOCOL § 6
- ❌ `brand-and-cliffhanger.md` → ver PAUTA-MASTER § 13 cliffhanger + VISUAL-STYLE.md
- 📂 `referent-analysis.md` → movido a `/referent-analysis/REFERENT-ANALYSIS-13-VIDEOS-SYNTHESIS.md`

---

## Workflow del arquitecto (versión actualizada Sub-Fase 3A)

```
1. Leer pauta canónica COMPLETA (orden estricto arriba — PAUTA-MASTER.md PRIMERO)
2. Consultar video-log.md → rotación pattern
3. ENTREVISTAR user (INTERVIEW-FLOW.md root level)
4. Llenar Slot A-H per PAUTA-MASTER:
   - Slot A: Escenario (de los 8 empíricos en § 7)
   - Slot B: Visual malo aparente (de las 6 plantillas validadas § 8)
   - Slot C: Visual bueno aparente (§ 9, puede ser extreme uncanny)
   - Slot D: Regla del malo aparente § 10 (LA LÍNEA MÁS IMPORTANTE)
   - Slot E: Dilemas internos § 11 (categorías validadas, NO repetir)
   - Slot F: Body horror específico § 12 (visualizable, no "mueres")
   - Slot G: Cliffhanger archetype § 13 (rotado vs video anterior — Paz perdida domina 7/8)
   - Slot H: Ambient creatures § 14 (del catálogo por setting)
5. Considerar reskinear de seeds canónicos antes de inventar desde 0
6. Aplicar checklist § 16 pre-producción
7. Codificar en CREATIVE-SPEC v11.yaml usando Slot A-H estructura + references_canonical[]
   (mínimo ≥5/8 refs cited per Gate 5 SPEC-AUDIT charter V4-LAUNCH-CHECKLIST)
8. Validar contra MODEL-BEHAVIOR-LOG constraints (face-coupling + stability budget + pose-coupling)
9. Operacionales (image-direction, animation-direction, etc.) llenan el "cómo"
10. HANDOFF al ingeniero
```

---

## Reglas inviolables que TODO arquitecto debe respetar (de la pauta)

De `PAUTA-MASTER.md` § 3 (autoridad empírica actual):

- **Estructura temporal:** Presentación 0-17% + Rama malo 17-78% + Resolución 78-88% + Cliffhanger 88-100%
- **2 dilemas internos** (no 3 — eso era inventado por mi previous docs)
- **La opción ganadora va contra el impulso primario. SIEMPRE.**
- **POV (primera persona) en >80% de los planos** (user confirmó esta regla en chat 2026-05-13)
- **Body horror específico, no genérico** ("tus venas se oscurecen" no "mueres")
- **Bueno aparente NO tiene diálogo** (excepto invitación inicial opcional)
- **Contraste visual obligatorio** entre los dos personajes
- **Tentación GENUINAMENTE deseable** — si repulsa antes de la consecuencia, twist falla

---

## Anti-patterns del arquitecto (del incidente Maikol-2026-05-13)

❌ **Construir historia AL REVÉS** — desde imagen visual hacia slots forzados. La PAUTA es el GENERADOR, no el LÍMITE.

❌ **Saltarse el CREATIVE-PROMPT-TEMPLATE (§ 5)** — improvisar desde el input del user sin pasar por slot template.

❌ **Ignorar story seeds (§ 4)** — reskinear MAGNUS → MAIKOL es mejor que inventar desde 0.

❌ **Inventar H0 contra reglas del pattern (§ 3.6)** — P1 = ❌ generalmente no.

❌ **Olvidar Slot D regla del malo** — "la línea más importante de todo el script".

❌ **No catalogar dilemas en las 5 categorías validadas (Slot E)** — y peor, repetir categoría.

❌ **Body horror genérico** ("pantalla negra → splash" = "mueres" disfrazado).

❌ **Inventar elementos sensoriales en counterfactual** que no están en § 3.1 PAZ PERDIDA validados.

❌ **No consultar Slot H ambient creatures** — son obligatorios post-2026-05-11.

❌ **Inventar reglas que contradicen la pauta** (ej: "duda artificial" cuando § 1 dice "opción ganadora va contra impulso primario, SIEMPRE").
