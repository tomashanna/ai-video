# Template — elige-tu-companero

> ⛔ **ARQUITECTURA CORREGIDA 2026-05-13 PM.** La PAUTA canónica de este formato vive en `horror-choice-format/CREATIVE-BRIEF.md` (940 líneas) + `PATTERNS.md` + `SCRIPT-WRITING-GUIDE.md` + `PAUTA.md`. Los docs en ESTE folder son **operacionales secundarios** — NO autoridad creativa.

---

## ⛔ LEER PRIMERO (orden estricto)

Antes de tocar nada de este folder, leer EN ORDEN:

1. **`../../horror-choice-format/CREATIVE-BRIEF.md`** — PAUTA canónica completa
   - § 0 Filosofía: "el formato es generador, no límite"
   - § 1 DNA + Reglas inviolables (2 dilemas mínimo, opción ganadora va contra impulso, etc.)
   - § 2 Slots A-H (cada uno con plantillas validadas)
   - § 3 4 arquetipos cliffhanger
   - § 3.5 10 patterns matriz expandida
   - § 3.6 H0 reglas por pattern
   - § 4 8 story seeds pre-validados
   - § 5 CREATIVE-PROMPT-TEMPLATE
   - § 6 Checklist pre-producción
   - § 9 FAQ del agente

2. **`../../horror-choice-format/PATTERNS.md`**
3. **`../../horror-choice-format/SCRIPT-WRITING-GUIDE.md`**
4. **`../../horror-choice-format/PAUTA.md`**
5. **`../../horror-choice-format/INTRO-FORMULA-V15.md`**
6. **`../../horror-choice-format/CHARACTER-NAMES-CATALOG.md`**
7. **`../../horror-choice-format/video-log.md`** (rotación pattern obligatoria)

---

## Docs operacionales en este folder

Estos docs **NO contienen reglas creativas** — solo cómo IMPLEMENTAR técnicamente lo que la PAUTA dicta. Si encontrás conflicto entre estos docs y la pauta canónica, **gana la pauta canónica siempre**.

| Doc | Función operacional | Pauta relacionada |
|-----|---------------------|-------------------|
| `aesthetic.md` | Dirección CSS color (warm/cool LUTs) | CREATIVE-BRIEF § 2 Slot A iluminación |
| `audio-direction.md` | Dirección audio (música/SFX/ducking intent) | PATTERNS § 2 AUDIO + Slot F SFX |
| `captions.md` | Sistema 3 clases captions (name/narration/warning) | PATTERNS § 3 visual + V7-1 stroke |
| `camera-and-shots.md` | Tipos de planos + motion direction | PATTERNS § 3 VISUAL + V8-3 motion |
| `image-direction.md` | Per-shot framework + anchor prompts | Slot B + Slot C plantillas |
| `animation-direction.md` | Animation tier strategy (HERO/STANDARD/DRAFT) + cost optimization | PATTERNS § 10.5 Kling + MODEL-BENCHMARK |
| `script-writing.md` | Formato unified script YAML (target_duration + pause_strict) | SCRIPT-WRITING-GUIDE plantilla maestra |
| `ui-elements.md` | UI specifics (countdown, loading bars, choice buttons) | V7-2 choice labels + V7-3 separador |
| `shared-universe.md` | Cross-video continuity (recurring characters, easter eggs) | Slot H ambient creatures (extensión) |

---

## Lo que ELIMINADO (eran duplicados de la pauta)

Estos docs que existían antes ahora están eliminados porque duplicaban contenido canónico:

- ❌ `characters.md` → ver Slot B + Slot C en CREATIVE-BRIEF
- ❌ `plot-patterns.md` → ver § 3.5 matriz expandida
- ❌ `story-arc.md` → ver § 1 DNA + § 3.6 H0 + PATTERNS § 1 estructura
- ❌ `hooks.md` → ver INTRO-FORMULA-V15
- ❌ `environments.md` → ver Slot A (15 escenarios)
- ❌ `counterfactual-outros.md` → ver § 3 archetypes + § 4 seeds
- ❌ `stakes-catalog.md` → ver Slot F body horror
- ❌ `narrator-voice.md` → ver § 1 reglas lenguaje + SCRIPT-WRITING-GUIDE
- ❌ `anti-patterns.md` → ver § 9 FAQ + PAUTA § 5 errores
- ❌ `brand-and-cliffhanger.md` → ver § 3 cliffhanger + BRAND.md
- 📂 `referent-analysis.md` → movido a `/referent-analysis/REFERENT-ANALYSIS-13-VIDEOS-SYNTHESIS.md`

---

## Workflow del arquitecto (versión corregida)

```
1. Leer pauta canónica COMPLETA (orden estricto arriba)
2. Consultar video-log.md → rotación pattern
3. ENTREVISTAR user (INTERVIEW-FLOW.md root level)
4. Llenar Slot A-H del CREATIVE-PROMPT-TEMPLATE (§ 5 CREATIVE-BRIEF)
   - Slot A: Escenario (de los 15 + variantes)
   - Slot B: Visual malo aparente (de las 7 plantillas)
   - Slot C: Visual bueno aparente (de las 7 plantillas)
   - Slot D: Regla del malo aparente (LA LÍNEA MÁS IMPORTANTE)
   - Slot E: 2 dilemas internos (de las 5 categorías, NO repetir categoría)
   - Slot F: Body horror específico (visualizable, no "mueres")
   - Slot G: Cliffhanger archetype (rotado vs video anterior)
   - Slot H: Ambient creatures (del catálogo por setting)
   - H0 opcional: SOLO si pattern lo permite (§ 3.6)
5. Considerar reskinear de los 8 seeds (§ 4) antes de inventar desde 0
6. Aplicar checklist § 6 pre-producción
7. Codificar en CREATIVE-SPEC.yaml usando Slot A-H como estructura primaria
8. Operacionales (image-direction, animation-direction, etc.) llenan el "cómo"
9. HANDOFF al ingeniero
```

---

## Reglas inviolables que TODO arquitecto debe respetar (de la pauta)

De `CREATIVE-BRIEF.md` § 1:

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
