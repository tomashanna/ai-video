# CANONICAL-SCENES-METHOD.md — Empirical scene-by-scene reference for architects

> **Status**: CAPA 1 universal — método reusable para cualquier template (horror-choice, tutorial, B2B, etc.) con N≥5 reference videos canónicos.
>
> **Output**: per-template `canonical-scenes/` directory con 1 doc por referente + INDEX cross-ref.
>
> **Purpose**: dar al arquitecto reference empírica de NIVEL DE DETALLE correcto al diseñar SPEC v6 `scene_context.who_does_what`. Sin esto, arquitecto improvisa (caso cabina-14: EMI femenina inventada, BAJARÍAS standard sin grounding).

---

## ¿Por qué existe este método?

**Gap detectado 2026-05-16 post sprint combinado v6 schema**:

- SPEC v6 exige `scene_context` storyboard-level per shot (who_is_there, who_does_what LITERAL, why_this_shot_exists).
- PAUTA-MASTER es **síntesis macro** — describe slots y patterns abstractos, NO shot-by-shot temporal.
- `descriptive-analysis/ref-XX.md` describe MACRO narrativo (hook 0-3s, decisions con timestamps) pero NO breakdown completo per shot.
- D22 auto-audit (creative-director) exige leer ref-XX antes de diseñar visual_anchor_prompts, pero **ref-XX no tiene shot list temporal** — solo descripción macro.

**Resultado sin canonical-scenes**: arquitecto lee PAUTA-MASTER (abstracto) + ref-XX (macro), traduce a SPEC v6 (storyboard-level) sin reference granular → inventa detalles → bugs narrativos.

**Resultado con canonical-scenes**: arquitecto lee 1-2 canonical-scenes/ref-XX.md del pattern elegido → ve cómo viral real estructura shot-by-shot → SPEC v6 grounded en empirical reference.

---

## Cuándo aplicar este método

✅ **SÍ aplicar**:
- Template nuevo con N≥5 reference videos canónicos validados (viral, score real medido, no nuestros).
- Después de tener PAUTA-MASTER + INGENIERO-PAUTA del template (canonical-scenes complementa, no reemplaza).
- Antes de producir el **primer video** del template post-spec-v6.

❌ **NO aplicar**:
- Template con N<5 referentes (datos insuficientes para patterns).
- Como reemplazo de PAUTA-MASTER (la pauta sintetiza, canonical-scenes ejemplifica — son COMPLEMENTARIOS).
- Para nuestras producciones (NO autoridad técnica — hard rule #19).

---

## Workflow paso-a-paso

### Input data required per referente

Cada `referent-analysis/ref-XX/` debe tener (mínimo):

| File | Función | Cómo se genera |
|---|---|---|
| `metadata.json` | Duración + dimensiones video | ffprobe |
| `transcription.json` | Whisper segments (`start`, `end`, `text`) | openai-whisper |
| `scene_cuts.txt` | Timestamps de cuts visuales | ffmpeg scene detection threshold 0.3 |
| `ui-elements.json` | UI state per keyframe sample | Gemini Vision (existente) |
| `gemini-frames-analysis.json` (opcional) | Frame descriptions pre-analizadas | gemini-analyze.py |
| `frames/` | Frames extraídos | ffmpeg -vf select |

Si `gemini-frames-analysis.json` falta para alguna ref, el script lo genera on-demand (cost ~$0.20-$0.50 per ref).

### Processing pipeline

```
1. Load transcription.json + scene_cuts.txt + ui-elements.json + descriptive-analysis/ref-XX.md
2. De-cluster scene_cuts (timestamps within 200ms = same boundary)
3. Cluster boundaries en SCENES (group consecutive cuts where avg duration ≥1.5s)
4. Per scene boundary [t_start, t_end]:
   a. Extract narration: Whisper segments overlapping [t_start, t_end]
   b. Extract UI active: ui-elements.json keyframes in range
   c. Extract visual: gemini-frames-analysis closest frames OR call Gemini on 1-3 frames
   d. Extract animation tier: heuristic from motion (frame-to-frame diff) OR mark INFERRED
   e. Map to pattern_category: hook / setup / decision_setup / decision_countdown / consequence_A / rama_B_transition / consequence_B / cliffhanger
5. Generate markdown per CANONICAL-SCENE-SCHEMA.md
6. Flag `[NEEDS VALIDATION]` items the script couldn't determine confidently
```

### Output structure

```
<template>/canonical-scenes/
├── README.md              ← disclaimer + cómo consultar
├── INDEX.md               ← cross-ref grid (built in Step 4 of generation block)
├── ref-XX-<chars>-<setting>.md  ← 1 doc per canónico
```

Filename pattern: `ref-XX-{character_A}-{character_B}-{setting_short}.md` (e.g., `ref-03-bruno-pablo-mina.md`).

---

## Mantenimiento

### Fixed N for h-choice = 8

Los 8 canónicos h-choice están **frozen** (PAUTA-MASTER § 0 base empírica única). Agregar un 9no requiere:

1. Validar viral (≥100k views, ≥30 days post-publish)
2. Score Gemini empirical
3. Re-run canonical-scenes script sobre el nuevo ref
4. Update INDEX.md cross-ref grid
5. Re-validar PAUTA-MASTER reglas N/9 vs N/8 (compliance recount)

### Re-validation cuando cambia el método

Si modificás el script o el schema, **NO re-correr automáticamente** sobre los 8 — los outputs ya validados por humano son source-of-truth. Solo re-correr cuando agregás un canónico nuevo o detectás bug en los outputs.

---

## Cross-references — donde se cita este método

- `creative-director/SKILL.md` § knowledge base reading order — agregar canonical-scenes/INDEX + ref-XX como step ANTES de diseñar SPEC v6.
- `creative-director/SKILL.md` D22 audit — actualizar para incluir lectura de canonical-scenes/ref-XX, no solo descriptive-analysis/ref-XX.
- `<template>-format/SKILL.md` lectura obligatoria — agregar canonical-scenes/INDEX + ref-XX.
- `<template>-format/PAUTA-MASTER.md` — cross-refs en reglas con compliance N/8 ("ver canonical-scenes/ref-XX.md § Scene Y para ejemplo concreto").

---

## Anti-patterns

| ❌ Anti-pattern | Por qué falla |
|---|---|
| Usar canonical-scenes como template rígido (copiar línea por línea) | Plagio creativo. PAUTA-MASTER § 1 "el formato es el generador, no el límite". |
| Reemplazar PAUTA-MASTER con canonical-scenes | Son complementarios — pauta sintetiza reglas, canonical ejemplifica. Sin pauta, canonical es ruido. |
| Aplicar a nuestras producciones | Hard rule #19 — NO autoridad técnica. |
| Generar para template con N<5 refs | Patterns falsos por sample size. |
| Re-correr script sobre canónicos ya validados | Pierde el trabajo de validación humana. |

---

## Última actualización

2026-05-16. Creado en Bloque I post sprint combinado v6 schema. Disparador: gap entre PAUTA-MASTER macro + ref-XX descriptive vs SPEC v6 storyboard-level granularity. Aplicado primero a horror-choice (8 canónicos).
