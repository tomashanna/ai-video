# SYSTEM-LEARNINGS-V3-V4-COMPILATION.md

**Document type:** System learnings compilation
**Source project:** horror-choice / @elige_tucompanero
**Target:** Reusable across multi-format AI video projects (Marina Sole AI Influencer, tutorial, B2B, etc.)
**Compiled:** 2026-05-22
**Purpose:** Input mandatorio del Auditor nuevo para que arranque con el aprendizaje completo de V3+V4, sin redescubrir empíricamente lo que ya pagamos.

---

## SECTION 0 — Cómo usar este documento

Este doc compila el aprendizaje del sistema horror-choice durante V3 (failure cycle costoso) y V4 (Phase 2.5 hybrid first execution). Contiene:

- 20 decisiones humanas tomadas con razón estructural documentada
- 7 bugs identificados con root cause + prevention proposal
- Patterns emergentes detectados durante la sesión
- 4 constraints empíricos descubiertos sobre Gemini Image API
- Mapeo agnóstico vs específico (qué se reusa, qué se replica adaptando)
- Antipatterns documentados que el Auditor nuevo debe NO repetir

El Auditor nuevo debe leer este doc completo antes de spawn cualquier agente. Es input al mismo nivel que PAUTA-MASTER o canonical-scenes.

---

## SECTION 1 — Contexto sistémico

### 1.1 Estado del sistema horror-choice al cerrar V4

El sistema completó la transición de V3 (cinema legacy stack con global captions causando drift) a V4 (Phase 2.5 hybrid architecture con per-clip atomic + Layer 3 cross-clip + HyperFrames UI overlay).

V4 fue el primer video que ejecutó la arquitectura hybrid completa con:
- Script A (build_clip_atomic + bake captions per clip)
- Script B (audit-shot-spec-compliance per shot, 8 dimensions)
- Script C (orchestrator-cp-by-cp con CP gates obligatorios)
- ARCHITECTURAL-DECISIONS.md con schema YAML
- V4-LAUNCH-CHECKLIST.md con 5 gates binarios
- MODEL-BEHAVIOR-LOG.md (nuevo, NIVEL 1.5)
- SPEC v11.1 con references_canonical[] mandatorio

### 1.2 Costo total del aprendizaje

V3 cycle: ~$6-30 cumulative (Replicate Hailuo + Veo cost surprise + multiple iter).
V4 cycle hasta CP3 close: ~$2.01-2.21 (dentro de $8 cap).
Plus Claude API spend no trackeado en cap (gap identificado, ver bug #4).

V3 fue lección cara con valor estructural enorme. V4 está siendo lección barata con conocimiento empírico crítico para forward.

### 1.3 Principio operativo central derivado de la sesión

> **El sistema no debe depender de juicio humano para cosas verificables estructuralmente, ni de docs como enforcement.**
>
> Cada vez que algo escala a humano, preguntar:
> 1. ¿Es decisión creativa irreemplazable? → mantener como decisión humana
> 2. ¿Es regla con criterio binario? → codificar como script o assertion estructural
> 3. ¿Es constraint del modelo externo? → documentar en MODEL-BEHAVIOR-LOG como input mandatorio del Architect
>
> Forward, cada video debería traer 3-5 decisiones humanas máximo, todas creativas o perceptuales. El resto se autoresuelve.

---

## SECTION 2 — Decisiones trackeadas (20 con razón estructural)

```yaml
decision_id: 1
date: 2026-05-22T06:00:00Z
context: "Auditor propuso cost cap V4 $9 con alert $7"
options_presented:
  - id: 1
    description: "Cap $9, alert $7 (Auditor recomendación)"
  - id: 2
    description: "Cap $8, alert $6 (más conservador)"
user_choice: 2
structural_reason: "V3 cinema legacy fue $6.28 y salió con bugs. Si V4 con arquitectura nueva supera $8, problema estructural, no retry budget. Halt fuerza escalation antes de blow-up."
forward_codification:
  proposed: "Default cost cap en código (no flag CLI) escala 25% sobre costo último video exitoso. Si V4 sale en $5, V5 default = $6.25."
  status: "partially_codified — default $8 hardcoded en Script C, regla de escalado dinámico pendiente Sprint B"
category: structural
pattern_class: "cost_discipline_conservative"
automation_potential:
  code_able: true
  proposed_script: null
  proposed_protocol_amendment: "Sprint B: cost-cap-auto-scale.py que ajuste DEFAULT_COST_CAP_USD según último video exitoso"
```

```yaml
decision_id: 2
context: "Auditor propuso 'I audit each script post-build' para los 3 enforcement scripts"
user_choice: "tests adversariales + V3 archive como verdadero adversarial, no auto-audit"
structural_reason: "Auditor construyendo enforcement del Auditor = loop circular (anti-pattern #5). Tests del enforcement van a sistema independiente o usuario."
forward_codification:
  proposed: "AUDITOR-PROTOCOL charter explicit: no autoauditar mecanismos de enforcement propio. Tests del enforcement van a sistema independiente o validación con artifacts existentes (V3 archive como caso real)."
  status: "codified en AUDITOR-PROTOCOL activation protocol nuevo"
category: structural
pattern_class: "no_circular_self_audit"
automation_potential:
  code_able: partial
  proposed_protocol_amendment: "AUDITOR-PROTOCOL section: 'Auditor never audits scripts that codify Auditor's own enforcement'"
```

```yaml
decision_id: 3
context: "Auditor propuso scripts pending no-blocker V4"
user_choice: "Build scripts BEFORE V4 launch, no after-the-fact"
structural_reason: "Hard Rules son texto = decoration. Scripts ARE the enforcement. Sin scripts, las Hard Rules son lo mismo que en V3."
forward_codification:
  proposed: "Regla codificada NIVEL 1: 'Si Hard Rule depende de enforcement no estructural (sin script), Hard Rule no es válida hasta que enforcement estructural exista. No launches new format video sin scripts equivalentes.'"
  status: "applied V4, debe ser regla explícita NIVEL 1 forward"
category: structural
pattern_class: "enforcement_must_precede_rules"
automation_potential:
  code_able: partial
  proposed_protocol_amendment: "V4-LAUNCH-CHECKLIST Gate 1 template + format-specific equivalente debe existir antes de launch"
```

```yaml
decision_id: 4
context: "Gate 3 RED detectado pre-V4: SPEC v11 template no existía. Opciones: build, bypass con override, postpone"
user_choice: "Option A — Build v11 template antes de V4"
structural_reason: "Bypass de Hard Rule #25 = documentation theater. Si validamos bypass una vez, el principio se debilita forward."
forward_codification:
  proposed: "Sprint B: cuando Gate RED bloquea launch, opción 'bypass con override' no debe ser default ofrecida por Auditor. Solo 'build' o 'postpone' son opciones legítimas."
  status: "codified en Gate 5 charter amend"
category: structural
pattern_class: "no_bypass_default_for_gate_red"
automation_potential:
  code_able: true
  proposed_script: "audit-launch-gate-options.py — valida que opciones presentadas al usuario cuando Gate RED no incluyen bypass como default"
```

```yaml
decision_id: 5
context: "Tomás inicialmente dijo 'que el Architect invente todo' (FASE 0 inputs). Claude conversacional frenó."
user_choice: "Architect propone N opciones FASE 0, Tomás elige entre opciones"
structural_reason: "Juicio creativo es activo irreemplazable. Delegarlo al Architect produce horror-choice promedio estadístico. Pero generar 5 inputs de cero es overhead innecesario. Comparativa entre opciones aprovecha creatividad del Architect + preserva juicio humano."
forward_codification:
  proposed: "Architect default mode forward para FASE 0: generar 3 propuestas distintas (diversity criteria mínimo 2 axes) + Tomás elige. NO Architect invent todo, NO Tomás genera de cero."
  status: "validated en V4 (3 opciones A/B/C funcionaron), debe ser default del Architect en CP0 forward"
category: operativa + creativa
pattern_class: "architect_proposes_user_chooses"
automation_potential:
  code_able: partial
  proposed_protocol_amendment: "Architect bootstrap CP0: 'default mode = 3 propuestas comparativas. No solicitar inputs directos del usuario en CP0.'"
```

```yaml
decision_id: 6
context: "3 propuestas FASE 0 V4 (A submarino, B geriátrico, C meteorológico). Criterio Tomás: 'el que dé mejor insights del sistema'"
user_choice: "C — Estación meteorológica Cerro Aislado"
structural_reason: "V4 es test de hybrid architecture completa. Setting más controlado minimiza variables fuera del sistema = señal más limpia. P2 canon-rooted recomendado por PAUTA específicamente para video #4."
forward_codification:
  proposed: "Cuando V es validation experiment vs producción libre, criterio default = 'minimize variables fuera del sistema bajo test'. Architect debe rankear propuestas según este criterio cuando context indica 'validation'."
  status: "criterio aplicado V4 exitosamente, debe ser opcional declarable en CP0 trigger"
category: estructural + creativa
pattern_class: "validation_video_minimizes_variables"
automation_potential:
  code_able: partial
  proposed_protocol_amendment: "Architect CP0 ack: si user_context indica 'validation video' → propuesta ranking includes 'controlled variables' como criterio explícito"
```

```yaml
decision_id: 7
context: "3 imperativos voseo argentino en SPEC v11. Auditor ofreció proceed/amend/reject."
user_choice: "Option 2 — Architect amend voseo en SPEC ahora (pre-CP1)"
structural_reason: "SPEC es contrato vinculante. Si CP2 patchea voseo a neutral en TTS pero SPEC dice 'esperá', contrato fue letra muerta. Source-of-truth debe ser limpio."
forward_codification:
  proposed: "Sprint B: validators automáticos en SPEC-AUDIT stage detectan violaciones antes de juicio humano. Hard Rule violation en SPEC → solo opciones legítimas son amend o reject. 'Proceed con NB' se elimina como categoría cuando hay Hard Rule violada."
  status: "Sprint B en construcción paralela V4 (audit-spec-language-neutral.py + audit-spec-character-names-real.py + audit-spec-pattern-rotation.py)"
category: structural
pattern_class: "no_downstream_patch_of_source"
automation_potential:
  code_able: true
  proposed_script: "audit-spec-language-neutral.py (+ 2 más en Sprint B)"
```

```yaml
decision_id: 8
context: "Sprint B (auto-validation suite) paralelo a V4 o post-V4"
user_choice: "Sprint B paralelo a V4 con safety constraints (engineer separado, no contamines foco V4)"
structural_reason: "Ventana de tiempo coincide (V4 = 2-3h, Sprint B = 2-3h). Sin pasos perdidos. V5 nace con auto-validation activa."
forward_codification:
  proposed: "Cuando dos tracks de trabajo son temporalmente compatibles + técnicamente independientes + sin dependencia bidireccional → paralelizar es default. Constraint clave: separar atenciones (spawn engineer separado), no contaminar agente principal."
  status: "validated en V4, debe ser regla operativa default"
category: operativa
pattern_class: "parallelize_when_temporally_compatible_and_independent"
automation_potential:
  code_able: false
```

```yaml
decision_id: 9
context: "Architect amend voseo aplicado a SPEC pre-CP1 (segunda confirmación de #7)"
user_choice: "Aplicado"
structural_reason: "Validación de #7 después de Architect generar amend"
category: structural
pattern_class: "no_downstream_patch_of_source"
```

```yaml
decision_id: 10
context: "Iván 6-finger glove canónico declarado en SPEC. Anchor podría tener 5 vs 6 fingers. Script B dim 6 no detecta esto."
user_choice: "Codificar gap structural: Script B verifica consistency intra-video (shot vs anchor), NO compliance anchor vs SPEC.visual_signature"
structural_reason: "Anchor con 5 fingers ya está violando SPEC en CP1. Script B en CP3 aceptará shots con 5 fingers como 'consistent with anchor' aunque SPEC declare 6-finger. Mismo gap arquitectural detectado proactivamente."
forward_codification:
  proposed: "Sprint B add: audit-anchor-vs-spec-signature.py. Input: anchor PNG + SPEC.characters[].visual_signature[]. Process: Gemini Vision describe features del anchor → compare contra signature[] declarado. Exit 1 si gap. Engineer regen anchor antes de CP3."
  status: "Sprint B priority CRÍTICA (validated en V4 CP3 con polydactyly regression)"
category: structural
pattern_class: "spec_signature_features_not_structurally_verified"
automation_potential:
  code_able: true
  proposed_script: "audit-anchor-vs-spec-signature.py"
```

```yaml
decision_id: 11
context: "Iván fingers en contact-sheet-cp1.png (visual check pendiente)"
user_choice: "Confiar engineer iter discipline + Script B catch CP3"
structural_reason: "Decisión #10 validó forward que Script B catch issues estructurales. Iter cost trivial pero adds wallclock sin valor claro."
category: structural (delegación a enforcement estructural)
```

```yaml
decision_id: 12
context: "CP2 audio NB: Vicente voice override Renato + atempo 2.0× anemometro. Auditor no puede reproducir audio."
user_choice: "GO Option 1 — listen + approve"
structural_reason: "Tu juicio perceptual audio es input irremplazable. NO escalation innecesaria, ES el rol creativo legítimo."
forward_codification:
  proposed: "Gemini Audio + audit-tts-perceptual.py puede automatizar 70% (distorsión técnica, pronunciación inteligible, prosody bands). El 30% restante (character match cultural + emoción específica) sigue siendo del usuario."
  status: "Sprint B priority media (post V4)"
category: creativa (irreemplazable) + cosmética parcial
pattern_class: "audio_verification_partial_automation"
automation_potential:
  code_able: partial
  proposed_script: "audit-tts-perceptual.py (cubre 70% técnico)"
  irreplaceable_human_reason: "character match cultural + emoción específica"
```

```yaml
decision_id: 13
context: "CP3 engineer crash mid-handoff. 20 PNGs en disk pero CP3-handoff.md NO escrito. 3 opciones recovery."
user_choice: "Option A — Auditor audit directo de artifacts (con check 1:1 filesystem vs SPEC.shot_list)"
structural_reason: "Engineer's deliverables están on disk + verificables directamente. Filesystem evidence es stronger ground truth que handoff text claim (anti-pattern #11). Crash recovery debería ser canonical."
forward_codification:
  proposed: "AUDITOR-PROTOCOL: crash recovery canonical method = read filesystem directly + cross-check 1:1 vs SPEC manifest + emit verdict skipping missing handoff. No re-spawn engineer para reconstruct handoff."
  status: "codified en AUDITOR-PROTOCOL activation protocol"
category: operativa + structural
pattern_class: "crash_recovery_from_filesystem"
automation_potential:
  code_able: true
  proposed_script: "audit-deliverable-vs-spec-manifest.py"
```

```yaml
decision_id: 14
context: "Verificación 1:1 filesystem ↔ SPEC.shot_list — debe ser responsabilidad estructural, no del Auditor manual"
user_choice: "Codificar estructural — el Auditor o Architect debe hacerlo siosi"
structural_reason: "Correspondencia entre artefactos es código (matemática set comparison), no juicio. No debe depender de memoria del Auditor."
forward_codification:
  proposed: "Sprint B add: audit-deliverable-vs-spec-manifest.py. Corre automático en cada CP-audit ANTES del análisis cualitativo. Exit 0/1/2 binary. Si exit 1 → CP halt con per-file diff."
  status: "Sprint B priority alta, codificado como Gap #46"
category: structural
pattern_class: "structural_correspondence_never_manual_audit"
automation_potential:
  code_able: true
  proposed_script: "audit-deliverable-vs-spec-manifest.py"
```

```yaml
decision_id: 15
context: "Iván polydactyly regression 3/3 hand-visible shots (5 fingers vs SPEC 6). Voseo precedent aplica."
user_choice: "Option A — Regen 3 shots con polydactyly reinforcement explicit"
structural_reason: "SPEC contrato vinculante. Cost $0.36 trivial vs propagation a CP4 Hailuo ($3-5 si hay que regen capa cara después). Mismo principio que voseo."
forward_codification:
  proposed: "Sprint B priority CRÍTICA: audit-anchor-vs-spec-signature.py debe estar listo antes de V5. Este patrón se va a repetir cada vez que personaje horror tenga signature features anatómicas no-standard."
  status: "Sprint B priority alta, codificado como Gap #44"
category: structural (repite pattern voseo)
pattern_class: "no_downstream_patch_of_source"
```

```yaml
decision_id: 16
context: "shot_11 hand-only regression después de regen con anchor full. Auditor proposed Option α: locus-specific hand anchor"
user_choice: "Option α híbrida — dedicated hand anchor + regen shot_11 con locus only + shot_16 con full anchor"
structural_reason: "Única opción que resuelve problema técnico + valida methodology nueva + sienta precedent para V5+. Otras opciones (drop polydactyly, inpaint, accept regression) no producen knowledge forward."
forward_codification:
  proposed: "Methodology 'locus-specific anchors for character signature features' se vuelve patrón. Cuando shot composition aísla signature feature de face → generar locus anchor pre-CP3."
  status: "MODEL-BEHAVIOR-LOG entry 1 codificado, audit-anchor-vs-spec-signature.py debe extender a per-locus methodology"
category: estructural + creativa
pattern_class: "locus_specific_anchors_for_signature_features"
automation_potential:
  code_able: partial
  proposed_protocol_amendment: "Architect CP0: flag shots con composition que isolate signature features → trigger locus-specific anchor pre-CP1"
```

```yaml
decision_id: 17
context: "shot_16 regen produjo composition distinta a SPEC (static confrontation vs reveal beat). Auditor admitió mea culpa: no cruzó brief vs SPEC literal"
user_choice: "Option 1 — Regen matching SPEC literal"
structural_reason: "Consistencia con precedente voseo + polydactyly. SPEC contrato vinculante. Auditor self-bug es valioso documentar pero no justifica amend retrospectivo del SPEC."
forward_codification:
  proposed: "Sprint B add: audit-engineer-brief-vs-spec.py. Recibe brief proposed + SPEC + valida que brief contains literal visual_intent text. Exit 1 si Auditor brief omits OR reformulates. Plus AUDITOR-PROTOCOL amend: pre-spawn engineer narrow, paste LITERAL visual_intent verbatim, NO compress."
  status: "Sprint B priority media, codificado como Gap #47"
category: structural
pattern_class: "no_informal_spec_reformulation_during_production"
automation_potential:
  code_able: true
  proposed_script: "audit-engineer-brief-vs-spec.py"
```

```yaml
decision_id: 18
context: "shot_16 SPEC literal inejecutable estructuralmente por Gemini stability budget (~3 props max para preservar rare anatomy). Auditor proposed Option 3 SPEC simplification."
user_choice: "Option 3 — SPEC simplification por stability budget"
structural_reason: "Architect amend SPEC desde source authority con razón documentada (MODEL-BEHAVIOR-LOG empirical finding) ≠ silent reformulation. Preserva reveal beat narrativo con composición static post-action."
forward_codification:
  proposed: "Sprint B add: audit-spec-stability-budget.py. Parse SPEC.shot_list[] → identifica shots con characters con visual_signature anatómica rara → cuenta props + actions. Exit 1 si >3 elementos beyond anchor character. CP0 Architect briefing: stability budget rule (max 3 elements per shot for rare anatomy). Plus BOOTSTRAP.md amend: Architect bootstrap incluye lectura mandatoria de MODEL-BEHAVIOR-LOG en CP0."
  status: "Sprint B priority media-alta, codificado en MODEL-BEHAVIOR-LOG entry 1"
category: estructural + creativa
pattern_class: "spec_amend_with_source_authority_when_model_constrained"
automation_potential:
  code_able: true
  proposed_script: "audit-spec-stability-budget.py"
  proposed_protocol_amendment: "BOOTSTRAP.md: MODEL-BEHAVIOR-LOG es input mandatorio Architect CP0"
```

```yaml
decision_id: 19
context: "shot_16 v11.2 falló con palm-down resting (full anchor palm-forward). Auditor descubrió pose-coupling."
user_choice: "Option A — Architect amend SPEC v11.3 pose-match (palm-forward holding clipboard)"
structural_reason: "Forward-engineering (aplicar pose-coupling finding nuevo para diseñar SPEC compatible con modelo) ≠ reverse-engineering (tomar output existente y reescribir SPEC). Architect amend con source authority + documented reason."
forward_codification:
  proposed: "Sprint B add: audit-spec-pose-coupling.py. Parse SPEC.shot_list[] → identifica shots con character anatomical signature → check hand poses match anchor poses declared en SPEC.characters[]. Architect CP0 protocol: declare anchor_pose field en SPEC.characters[] + hand_pose field en each shot_list[]."
  status: "Sprint B priority media-alta, codificado en MODEL-BEHAVIOR-LOG entry 1 update 2"
category: estructural
pattern_class: "spec_amend_with_source_authority_when_model_constrained"
automation_potential:
  code_able: true
  proposed_script: "audit-spec-pose-coupling.py"
```

```yaml
decision_id: 20
context: "shot_16 v11.3 falló con palm-forward HOLDING clipboard. 5 iter fallidos cumulativos. Auditor descubrió 4th constraint: bare/gloved + holding/empty exact match."
user_choice: "Path A — Architect amend SPEC v11.4 a v2 stop-gesture composition (matches preserved render)"
structural_reason: "Después de 5 iter empíricos + 4 capas refinement, SPEC original inejecutable estructuralmente. Architect amend con source authority + razón documentada empírica de 5 iter + descubrimiento de 4 constraints reales del modelo. NO reverse engineering. Es conscious source amendment con MODEL-BEHAVIOR-LOG entry como justificación."
forward_codification:
  proposed: "Sprint B CRÍTICA: audit-spec-model-constraints.py meta-validator que parse SPEC.shot_list[] y check 4 constraints (face co-located, ≤3 elementos, pose exact match, hand configuration match). Architect CP0 MUST run pre-emission."
  status: "Sprint B priority CRÍTICA, codificado en MODEL-BEHAVIOR-LOG entry 1 final con 4 constraints empíricos"
category: estructural
pattern_class: "spec_amend_with_source_authority_when_model_constrained"
automation_potential:
  code_able: true
  proposed_script: "audit-spec-model-constraints.py (meta-validator de los 4 constraints)"
```

---

## SECTION 3 — Bugs identificados (7 con root cause + prevention)

```yaml
bug_id: 1
date_detected: 2026-05-22 nightly session
detected_by: "engineer crash 3rd occurrence"
description: "Engineer agent API stream idle timeout mid-step cuando wallclock >15 min"
category: "does_not_execute_what_should"
root_cause: "Engineer agent context inflation OR API server idle timeout policy. Sequential API calls con wallclock alto disparan timeout antes de step final (typically handoff doc write)."
evidence:
  - "Script C tests overnight pre-fix"
  - "V3 iter 2 surgical fix mid-execution"
  - "V4 CP3 shot gen mid-handoff"
frequency: 3 occurrences in single session
current_workaround: "Auditor recovery from filesystem (codified Decision #13)"
prevention_proposal:
  - "Engineer prompts split heavy work into checkpoints with intermediate writes"
  - "For image gen >10 shots: batch 5 with intermediate partial-handoff flushes"
  - "For CP4 Hailuo (20 calls): explicit 'write partial handoff every 3 clips'"
codification_status: "queue Sprint B priority alta (3+ occurrences threshold met)"
sprint_b_action: "INGENIERO-PAUTA amend: section 'intermediate handoff protocol' mandatorio para CP3+CP4"
```

```yaml
bug_id: 2
date_detected: 2026-05-22 CP1 audit
description: "Anchor signature features no propagan a downstream shots vía Gemini --ref"
category: "executes_incorrectly"
root_cause: "Gemini --ref preserves identity primarily through face recognition. When face absent OR pose mismatch OR composition complex, model defaults to most-likely interpretation (normal human anatomy) regardless of --ref + explicit prompt reinforcement."
evidence:
  - "V4 CP1 anchor Iván 6-finger achieved iter 3"
  - "V4 CP3 shot_11 (hand-only) regressed to 5 fingers across 3 iter"
  - "V4 CP3 shot_16 v11.2 palm-down (pose mismatch) regressed to 5 fingers 2 iter"
  - "V4 CP3 shot_16 v11.3 palm-forward holding (bare/gloved mismatch) regressed to 5/6 mixed"
empirical_constraints_discovered:
  - "Face co-located con signature feature (no hand-only/feature-only)"
  - "≤3 prop/character elements beyond anchor (stability budget)"
  - "Hand pose exact match anchor pose (not abstract category)"
  - "Hand configuration match (bare/gloved + holding/empty status)"
current_workaround: "Locus-specific anchors + SPEC design within 4 constraints + amend SPEC v11.4 a composition that matches all 4"
prevention_proposal:
  - "Sprint B CRÍTICA: audit-spec-model-constraints.py meta-validator que check los 4 constraints pre-emit SPEC"
  - "Sprint B alta: audit-anchor-vs-spec-signature.py per-locus methodology"
  - "BOOTSTRAP.md amend: MODEL-BEHAVIOR-LOG es input mandatorio Architect CP0"
  - "SPEC v11.x schema: declare anchor_pose + hand_pose per shot mandatorio"
codification_status: "MODEL-BEHAVIOR-LOG entry 1 codified, Sprint B scripts in queue"
sprint_b_action: "audit-spec-model-constraints.py CRÍTICA antes V5"
```

```yaml
bug_id: 3
date_detected: 2026-05-22 CP3 regen shot_16
description: "Auditor engineer brief no cross-checked contra SPEC literal — compress visual_intent al escribir engineer brief"
category: "does_not_execute_what_should"
root_cause: "Auditor compress o reformula visual_intent al spawn Engineer narrow scope, en vez de paste literal del SPEC.shot_list[N].visual_intent. Anti-pattern detected via self mea culpa del Auditor."
evidence:
  - "V4 CP3 shot_16 regen primera vez con 'palm-forward stop gesture' (compressed) vs SPEC literal 'ladder descent + clipboard + glove removal'"
current_workaround: "AUDITOR-PROTOCOL amend section: 'pre-spawn Engineer narrow, paste LITERAL visual_intent verbatim, NO compress, NO reformulation'"
prevention_proposal:
  - "Sprint B add: audit-engineer-brief-vs-spec.py. Recibe brief proposed + SPEC. Valida brief contains literal visual_intent text exact match. Exit 1 si omits OR reformulates."
codification_status: "queue Sprint B priority media. AUDITOR-PROTOCOL amend already in place."
sprint_b_action: "audit-engineer-brief-vs-spec.py"
```

```yaml
bug_id: 4
date_detected: 2026-05-22 CP3 close
description: "Cost ledger incompleto — Claude API spend invisible al cost cap"
category: "executes_incorrectly"
root_cause: "Script C cost cap monitorea Replicate + Gemini Image + ElevenLabs pero NO Claude API agent spawns. False sense of compliance con cap."
evidence:
  - "V4 $1.55-1.91 reportado en CP3, ~50 tool calls del Engineer en CP3 alone"
  - "Plus Architect + Auditor multiple invocations no contabilizados"
  - "Mismo class de bug que V3 Veo cost surprise"
current_workaround: "Pending — Auditor reportará estimación cuando consulte"
prevention_proposal:
  - "Sprint B CRÍTICA: cost-tracker-unified.py que sume 4 fuentes:"
  - "  - Replicate API responses con cost field"
  - "  - Gemini Image: count × $0.039"
  - "  - ElevenLabs: per-call si aplica"
  - "  - Claude API: token usage × rate per agent invocation"
  - "Output: dashboard tiempo real total spend. Script C consulta antes de cada CP spawn."
codification_status: "queue Sprint B priority CRÍTICA"
sprint_b_action: "cost-tracker-unified.py antes de V5 mandatory"
```

```yaml
bug_id: 5
date_detected: 2026-05-22 cross-session pattern
description: "Pattern sistémico: SPEC contract weakening durante producción"
category: "executes_incorrectly"
root_cause: "Durante producción aparecen micro-oportunidades de que el SPEC se debilite silenciosamente. Compress descriptions, reformular para clarity, accept output que funciona aunque diferente. No por mala fe, por shortcuts naturales bajo context pressure."
evidence:
  - "V4 voseo (TTS engineer reformulation tentativa)"
  - "V4 polydactyly anchor signature loss downstream"
  - "V4 shot_16 brief auditor reformulation"
frequency: 3 instancias V4 (mismo root pattern)
current_workaround: "Decisiones humanas explicit aplicando 'SPEC contrato vinculante' principle"
prevention_proposal:
  - "Cluster de Sprint B validators que protegen SPEC integrity:"
  - "  - audit-spec-language-neutral.py"
  - "  - audit-engineer-brief-vs-spec.py"
  - "  - audit-anchor-vs-spec-signature.py"
  - "  - audit-spec-model-constraints.py"
  - "  - audit-deliverable-vs-spec-manifest.py"
  - "Charter Auditor amend: 'Cuando hay Hard Rule violation en SPEC, solo opciones legítimas son amend source o reject. No proceed-with-NB como tercera opción.'"
codification_status: "queue completo en Sprint B + V4-LAUNCH-CHECKLIST Gate 5 amend codified"
```

```yaml
bug_id: 6
date_detected: 2026-05-22 cross-session pattern
description: "Auditor + Architect dependencia textual: MODEL-BEHAVIOR-LOG no era input mandatorio del Architect en CP0"
category: "does_not_execute_what_should"
root_cause: "MODEL-BEHAVIOR-LOG existe pero no estaba codificado en BOOTSTRAP.md como mandatory read del Architect. Resultado: Architect diseña SPECs fuera de constraints conocidos del modelo, descubrimos en producción."
evidence:
  - "V4 shot_16 original SPEC v11.1 violaba 4 constraints empíricos de Gemini. 5 iter para descubrir empíricamente."
prevention_proposal:
  - "BOOTSTRAP.md amend: 'Architect bootstrap CP0 — lectura obligatoria de MODEL-BEHAVIOR-LOG.md antes de emit SPEC. Architect debe diseñar dentro de constraints documentados.'"
  - "SPEC-AUDIT charter amend (V4-LAUNCH-CHECKLIST Gate 5): Auditor verifica que SPEC respeta constraints documentados en MODEL-BEHAVIOR-LOG."
codification_status: "queue Sprint B alta. AUDITOR-PROTOCOL activation protocol ya incluye lectura."
```

```yaml
bug_id: 7
date_detected: 2026-05-22 across multiple decisions
description: "Decisiones cosméticas escalan a humano innecesariamente"
category: "executes_what_should_not"
root_cause: "Auditor offers 'proceed con NB' como opción legítima cuando hay Hard Rule violada. Eso fuerza decisión humana en cosas que deberían bloquear estructuralmente."
evidence:
  - "Voseo SPEC = decisión humana cuando debería ser auto-amend del Architect"
  - "Polydactyly anchor consistency = decisión humana cuando debería ser auto-regen estructural"
frequency: 2+ instancias V4
prevention_proposal:
  - "Sprint B: Auto-validation suite SPEC corre en SPEC-AUDIT stage ANTES de juicio humano"
  - "Self-amend protocol del Architect: si validator falla, SPEC vuelve al Architect con feedback automático. Architect amend en hasta N intentos antes de escalar."
  - "Charter Auditor amend: eliminar 'proceed con NB' como tercera opción cuando Hard Rule violada"
codification_status: "Sprint B en construcción paralela V4"
```

---

## SECTION 4 — 4 constraints empíricos de Gemini --ref (descubiertos en V4)

Esto es información empírica nueva que NO existía documentada antes de V4. Crítico para CUALQUIER proyecto que use Gemini Image API (incluido AI influencer Marina Sole).

### Constraint 1 — Face-coupling de identidad

**Behavior:** Gemini --ref propaga identidad primariamente via face recognition. Cuando face está co-located en frame con signature feature, identity preserve. Cuando signature feature aparece en hand-only o feature-only composition (sin face en frame), regresa a interpretación normal.

**Evidence V4:** shot_10 face+hand → 6 fingers ✓. shot_11 hand-only → 5 fingers ✗ across 3 iter.

**Workaround:** locus-specific anchors per signature region (hand-only anchor, eye-only anchor) cuando shot composition isolates feature from face.

### Constraint 2 — Stability budget ~3 elementos

**Behavior:** Face+hand co-location es necesario pero NO suficiente. Cuando composition incluye 4+ props + multi-beat action, Gemini consume "stability budget" y regresa a anatomía normal + introduce hallucinations (severed glove, detached fingers).

**Evidence V4:** shot_16 v3 iter 1 (multi-prop + glove removal) → 3 fingers + hallucinations. shot_16 v2 (palm-forward + 0 props) → 6 fingers ✓.

**Threshold empírico:** ≤3 distinct prop/character elements beyond anchor character itself.

**Workaround:** SPEC composition design ≤3 elementos. Decompose multi-action en multi-shot si necesario.

### Constraint 3 — Pose-coupling EXACT match

**Behavior:** Cuando face+full anchor están en frame, Gemini balances face identity vs hand identity. Pose mismatch (hand pose en shot ≠ hand pose en anchor) crea "inconsistency penalty" → fallback a anatomía normal.

**Evidence V4:** anchor char_a_v1.png pose = palm-forward raised. shot_10/16v2 palm-forward → 6 fingers ✓. shot_16 v11.2 palm-down resting → 5 fingers ✗ across 2 iter.

**Subtlety:** locus anchor (sin face) es pose-tolerant porque no hay face identity conflict.

**Workaround:** Match shot hand pose con anchor hand pose OR generate locus anchor con pose matching shot.

### Constraint 4 — Hand configuration match (bare/gloved + holding/empty)

**Behavior:** Pose match abstract NO es suficiente. Match debe ser EXACT incluyendo:
- Hand configuration: both bare matching anchor bare, OR both gloved matching anchor gloved
- Object holding state: anchor empty hand → shot debe ser empty hand
- Full pose context, no just "palm forward" abstract category

**Evidence V4:** shot_16 v11.3 palm-forward HOLDING clipboard (anchor empty) → 5/6 fingers mixed. Mismo pose abstract pero holding state mismatch.

**Workaround:** Match all aspects (pose + bare/gloved + holding state) OR generate locus anchor con exact composition.

---

## SECTION 5 — Patterns emergentes detectados

### Pattern 1 — "No downstream patch of source"

**Definición:** Si SPEC declara X y output produce Y, la corrección debe ser en SPEC (amend con razón documentada) o en output (regen para match SPEC). Nunca "aceptamos Y y patcheamos downstream para que funcione".

**Instancias V4:** 3 (voseo, polydactyly anchor signature, shot_16 brief)

**Codificación forward:** Sprint B validators + Charter Auditor elimina "proceed con NB" cuando Hard Rule violada.

**Threshold trigger:** 5+ instancias del mismo pattern → regla codificada estructural automática.

### Pattern 2 — "Architect proposes, user chooses"

**Definición:** Para FASE 0, default mode del Architect = generar 3 propuestas distintas (diversity criteria mínimo 2 axes). User elige. NO Architect invent todo, NO user genera de cero.

**Instancia V4:** 1 (FASE 0 V4 con A/B/C funcionó perfecto)

**Codificación forward:** Architect bootstrap CP0 amend.

### Pattern 3 — "SPEC amend with source authority when model constrained"

**Definición:** Cuando descubrimos límite del modelo empíricamente, Architect amend SPEC con razón documentada (MODEL-BEHAVIOR-LOG entry) es legítimo. ≠ silent reformulation o reverse engineering.

**Instancias V4:** 3 (stability budget, pose-coupling, pose-coupling refinement bare/gloved)

**Codificación forward:** Si patrón aparece 2-3 instancias más → trigger: "Architect en CP0 MUST run audit-spec-model-constraints.py pre-emission. No SPEC emits sin pasar este validator."

### Pattern 4 — "Structural correspondence never manual audit"

**Definición:** Verificación de correspondencia entre artefactos (filesystem vs SPEC manifest, anchor vs SPEC signature, brief vs SPEC literal) es código, no juicio humano.

**Instancias V4:** 3 (filesystem 1:1, anchor signature, brief literal)

**Codificación forward:** Cluster de validators Sprint B que cubre todos los puntos de correspondence.

### Pattern 5 — "Cost discipline conservative"

**Definición:** Cost cap default escala 25% sobre último video exitoso. No 50%, no 100%. Forzar disciplina sin recortar buffer útil.

**Instancia V4:** 1 (cost cap $8 = ~25% over V3 $6.28)

**Codificación forward:** Sprint B cost-cap-auto-scale.py.

### Pattern 6 — "No circular self-audit"

**Definición:** Auditor never audits scripts that codify Auditor's own enforcement. Loop circular = anti-pattern #5.

**Instancia V4:** 1 (test scripts ABC con V3 archive como adversarial)

**Codificación forward:** AUDITOR-PROTOCOL charter explícito.

### Pattern 7 — "Parallelize when temporally compatible AND independent"

**Definición:** Dos tracks de trabajo paralelos si: temporalmente compatibles + técnicamente independientes + sin dependencia bidireccional. Constraint: separar atenciones (engineer separado), no contaminar agente principal.

**Instancia V4:** 1 (Sprint B paralelo a V4 con safety constraints)

**Codificación forward:** Regla operativa default del Auditor.

### Pattern 8 — "Synthesis converts flexible principles to binary rules"

**pattern_class:** `synthesis_converts_flexible_principles_to_binary_rules` (refinamiento 2026-05-29 de `validation_against_synthesis_violates_primary_source_principle` — Tomás precisó el framing: el problema no es "regla equivocada → regla correcta" sino que **la síntesis convierte PRINCIPIOS FLEXIBLES en REGLAS BINARIAS**. El fix correcto = expresar **principio (mandatorio) + variabilidad (libre) + anti-pattern (evitar)**, NO cambiar una regla rígida por otra.)

**Definición:** Una regla/validator que se valida contra un doc de SÍNTESIS (PAUTA-MASTER, canonical-scenes, memorias-paráfrasis) en vez de contra la FUENTE PRIMARIA (transcripts Whisper de los 8 virales en `referent-analysis/horror-choice/ref-XX/`) hereda la paráfrasis del sintetizador, no el dato real. Si V_n respeta el canónico correcto, el validator FAIL; si respeta la paráfrasis, PASS pero el output sale robótico. Familia directa del anti-pattern #10 (trust docs/intermediate sin direct verification).

**Instancias detectadas (threshold canonical promotion = 5):**
- **1/5** — matadero canonical-scenes countdown (auditor concluyó "2/6 refs tienen countdown" desde docs sampleados cada 5s; direct frame extraction reveló 4/4 FILM LEADER ACADEMY universal). Origen del anti-pattern #10. 2026-05-19.
- **2/5** — ⭐ regla `feedback_si_elegiste_framing` / D19 "Si elegiste X" (síntesis) vs primary source "Si [acción condicional]" (6/8 @referent-a) + "Si decides/escogiste" (2/8 @referent-b). El validator `audit-spec-narrative-coherence.py` enforzaba el substring `si elegiste` → FAIL sobre el 6/8 canónico real. Detectado por Tomás (user_perceptual_catch). Fix: primary-source enforcement + 17 tests. 2026-05-29. **Co-findings TAREA 2** (misma clase, NO fixeados — Tomás decide): `"Una noche en paz"` mandado como "canónico" pero 0/8 (es nuestra firma de marca); template cliffhanger rígido `"juntos, en silencio, mirando…"` 0/8; SCRIPT-WRITING-GUIDE "bueno sin diálogo" + "ganadora contra impulso" contradicen PAUTA §0/§6.

- **3/5** — ⭐ cluster `SCRIPT-WRITING-GUIDE.md` convertía principios flexibles en reglas binarias: (a) "ganadora contra impulso" como ley (PAUTA §6 lo refuta → principio real = DUDA real); (b) "bueno NO tiene diálogo" binario (ref-08 Hugo habla → variabilidad); (c) cliffhanger template rígido "…juntos, en silencio, mirando…" (0/8 → principio = cozy ESPECÍFICO al setting); (d) "Una noche en paz" como regla canónica (0/8 → es firma de marca @elige_tucompanero). **Fix 2026-05-29** (Tomás override authority): SCRIPT-WRITING-GUIDE refactoreado a 🟦principio/🟩variabilidad/🟥anti-pattern + validator `check_consequence_framing` refinado (missing marker → FLAG no FAIL; solo bare-label = FAIL). **2da pasada forense** (INGENIERO-PAUTA + canonical-scenes + TASTE-LOG + validators L1/lip-sync): **superficie de ENFORCEMENT limpia** — métricas técnicas ya son bandas (principio), TASTE-LOG ya es prosa no-taxonómica, validators L1/lip-sync gatean física/realismo, NO elecciones creativas. Único residual 🟡 cosmético: canonical-scenes ref-09/ref-13 usan label "Si elegiste X framing" pero los ejemplos capturados son correctos (action/choice) → relabel forward. **Propagación Categoría C limpiada 2026-05-29 (scope Opción 1 — 5 docs teaching: PAUTA-MASTER §3, creative-director SKILL D19, ARCHITECT-MASTER-FLOW, CP2-script-flow, AUDITOR-PROTOCOL L201 → 🟦/🟩/🟥). Categoría B (canonical-scenes ~68 hits, cosmético) + D (bridge-caption válido) deferred forward. ⭐ LESSON: una paráfrasis sintética introducida en 1 doc PROPAGA cross-docs (113 raw hits / solo ~10 genuine-template) — forward, todo doc creative nuevo debe pasar audit "principio vs variabilidad vs anti-pattern" ANTES de commit canonical.**

- **4/5** — ⭐ `tests_with_synthetic_fixtures_dont_substitute_real_artifact_testing` (sub-nombre de la MISMA familia: un stand-in sintético sustituyendo el ground-truth). Los validators BUILD 4/5/8 (narrative-coherence + narration-fits-duration + lip-sync-marks) se escribieron + testearon con fixtures **dict-form SINTÉTICAS** y **nunca corrieron contra un SPEC v11 real**. El schema v11 canónico (cerro-aislado-v4 + V5: `narration_in_this_shot` **string** + sibling `dialog_text`/`has_lip_sync_required` + `section_id` + hook_sub_beats **dicts**) NO coincide con el dict-form de las fixtures → los 3 validators **CRASHEAN** (`AttributeError`) en el primer SPEC v11 real (sala-limpia-bioseguridad SPEC-AUDIT 2026-05-29). Detectado por el AUDITOR al **correr** los validators (el arquitecto reportó "all PASS" sin correrlos — exactamente el rol del 3er ojo independiente). **Fix Opción A 2026-05-29** (Tomás): helpers both-forms (`_narr_text`/`_beat_role`/`_wpm_band_for` + section_id + has_lip_sync_required sibling + dilema_placement opcional + hook dict beats) → parsean el schema v11 real Y mantienen fixtures legacy; + **real-artifact regression tests** (v11-string-schema) en los 3 test files → 34/34 PASS. NO se tocó SPEC V5 ni cerro (D38) ni template. ⭐ **LESSON: tests adversariales (HR#26) DEBEN incluir un regression test contra el SCHEMA del artefacto REAL, no solo fixtures sintéticas — sino el validator pasa sus propios tests pero crashea en producción ("green tests, red reality").**

**Codificación forward:** si llega 5/5 → promote a Hard Rule / structural validator (`audit-rule-vs-primary-source.py`: toda regla con claim "canónico N/M" debe citar el transcript/frame primario, no la síntesis; + toda regla sobre una elección creativa debe declararse como principio+variabilidad+anti-pattern, NO regla binaria). Hasta entonces: el Auditor, al validar CUALQUIER regla, distingue principio underlying (enforce) de variabilidad creativa (NO enforce) de anti-pattern (flag), y lee la fuente primaria directa (transcript/frame), NO la síntesis. Refuerza anti-pattern #10 en AUDITOR-PROTOCOL §6.

---

## SECTION 6 — Mapa agnóstico vs específico (para adaptación a formato nuevo)

### Capa A — AGNÓSTICO 100% (reusa sin cambios)

Estos componentes funcionan para cualquier formato (horror-choice, AI influencer, tutorial, B2B, documental):

**Arquitectura:**
- CP-by-CP pipeline (CP0 → CP1 → CP2 → CP3 → CP4 → CP5)
- Per-clip atomic mux
- 3 audio layers (per-clip diegetic / effect non-diegetic / cross-clip global)
- HyperFrames UI overlay (Layer 4)
- Quality Gate per artifact + Auditor independent + User perceptual (3-level review)

**Scripts enforcement:**
- Script A — build_clip_atomic.py (bake captions per clip)
- Script B — audit-shot-spec-compliance.py (8 dimensions per shot)
- Script C — orchestrator-cp-by-cp.py (CP gates state machine)
- All Sprint B validators (cuando se buildeen)

**Docs estructurales:**
- AUDITOR-PROTOCOL.md activation protocol
- BOOTSTRAP.md
- V4-LAUNCH-CHECKLIST.md template (con format-specific equivalent)
- ARCHITECTURAL-DECISIONS.md schema YAML
- MODEL-BEHAVIOR-LOG.md (4 constraints Gemini empíricos aplicables a cualquier proyecto que use Gemini Image)
- SYSTEM-ROADMAP.md
- PIPELINE.md §13.9 hybrid architecture

**Patterns operativos:**
- Architect propose N options, user chooses
- No downstream patch of source
- Structural correspondence never manual audit
- Cost discipline conservative
- Parallel when temporally compatible

**Constraints Gemini:** los 4 constraints empíricos aplican a CUALQUIER proyecto que use Gemini Image API. AI influencer también.

### Capa B — ESPECÍFICO HORROR-CHOICE (replicar con adaptación al formato nuevo)

Estos componentes son específicos del formato horror pero la **estructura** es replicable. Hay que crear el equivalente para el nuevo formato:

- PAUTA-MASTER horror-choice → PAUTA-MASTER nuevo formato (autoridad creativa del formato)
- canonical-scenes/ref-XX.md (8 refs horror) → refs canónicos nuevo formato
- CREATIVE-SPEC-TEMPLATE-v11.1.yaml → SPEC template adaptado al formato
- TASTE-LOG horror-choice → TASTE-LOG nuevo formato (gusto codificado del usuario)
- INGENIERO-PAUTA → puede reusarse mayormente, ajustes específicos al formato

### Capa C — NUEVO (crear desde cero para el formato nuevo)

Depende del formato. Posibles ejemplos:
- Métricas específicas (e.g., "belief threshold" para AI influencer en vez de "EXECUTION CONTINUITY" para horror)
- Constraints específicos (e.g., lip sync mandatorio para AI influencer)
- Cliffhanger archetypes (NO aplica para AI influencer, sí para horror)
- Dyad characters (NO aplica para single character como Marina, sí para horror)
- Cross-video character consistency (CRÍTICO para Marina, no crítico para horror que cambia cast)

---

## SECTION 7 — Antipatterns documentados (que el Auditor nuevo NO debe repetir)

### Anti-pattern V4 #1 — Documentation theater

**Definición:** Codificar Hard Rules en docs sin enforcement estructural (script). "Hard Rules son texto que el agente lee y decide aplicar" = no es enforcement.

**Manifestación V3:** Caption-audio sync rule en PAUTA, sin script que bloquee si offset >0.1s. Resultado: drift 0-34s no detectado.

**Mitigación:** Script A + Script B + Script C. No new Hard Rules sin enforcement structural correspondiente.

### Anti-pattern V4 #2 — Engineer multi-CP autonomous

**Definición:** Engineer spawn con instrucción para ejecutar múltiples CPs end-to-end sin gates intermedios.

**Manifestación V3:** One-shot autonomous test → 15 bugs surface.

**Mitigación:** Script C orchestrator refuses prompts multi-CP. Engineer narrow scope = single CP only.

### Anti-pattern V4 #3 — Auditor unilateral architectural rollback

**Definición:** Auditor decide cambio arquitectural sin escalation a usuario.

**Manifestación V3:** Auditor decidió rollback Phase 2 → cinema legacy unilateral.

**Mitigación:** ARCHITECTURAL-DECISIONS.md mandatorio para decisiones que afectan forward. Cambios arquitecturales requieren user PRECEDENCE explícito.

### Anti-pattern V4 #4 — Circular self-audit

**Definición:** Auditor audita scripts que codifican el enforcement del Auditor mismo.

**Mitigación:** Tests adversariales + V3 archive como caso real + user verifica outputs estructurados.

### Anti-pattern V4 #5 — Silent SPEC reformulation

**Definición:** Compress, reformular o reverse-engineer SPEC durante producción para que match output existente.

**Manifestación V4:** Auditor brief al engineer compressed visual_intent. Engineer regen produjo output diferente. Reverse engineering tentación rejected.

**Mitigación:** AUDITOR-PROTOCOL: pre-spawn engineer narrow, paste LITERAL visual_intent verbatim. Sprint B: audit-engineer-brief-vs-spec.py.

### Anti-pattern V4 #6 — Cost surprise hidden

**Definición:** Asumir que servicio X es FREE sin verificar. Costo aparece retroactivo en factura.

**Manifestación V3:** Veo enterprise assumed FREE. Cost surprise.

**Mitigación:** Sprint B: cost-tracker-unified.py que captura todas las fuentes. Plus regla: no assume FREE, verify before launch.

---

## SECTION 8 — Sprint B priorities consolidadas (para Project nuevo)

Lista priorizada de scripts/amendments pendientes que deberían existir antes de launch de cualquier formato nuevo:

**CRÍTICAS:**
1. `cost-tracker-unified.py` — sum all sources, real-time dashboard
2. `audit-spec-model-constraints.py` — meta-validator 4 constraints Gemini
3. `audit-deliverable-vs-spec-manifest.py` — filesystem 1:1 SPEC

**ALTAS:**
4. `audit-anchor-vs-spec-signature.py` per-locus methodology
5. `audit-spec-language-neutral.py` — voseo + regionalismos
6. INGENIERO-PAUTA amend: intermediate handoff protocol mandatorio CP3+CP4

**MEDIAS:**
7. `audit-engineer-brief-vs-spec.py` — brief literal verify
8. `audit-spec-pose-coupling.py` — hand pose match anchor
9. `audit-spec-stability-budget.py` — ≤3 elementos rare anatomy
10. `audit-tts-perceptual.py` — distorsión + pronunciación (70% audio automation)
11. `audit-spec-character-names-real.py` — no descriptors (format-specific applicability)
12. `audit-spec-pattern-rotation.py` — pattern reuse check (horror-specific, adapt para formato)

**OPCIONALES post-V4 evaluation:**
13. DECISIONS-LOG.md + BUGS-LOG.md con schemas YAML + pattern detection automation
14. `cost-cap-auto-scale.py` — default escala 25% sobre último video exitoso

---

## SECTION 9 — Activation pattern del Auditor nuevo

Cuando arranque Auditor en proyecto nuevo, invocación user:

```
Sos el AUDITOR del proyecto [NOMBRE PROYECTO].
Tu prioridad: [TASK ESPECÍFICA].
Antes de empezar, ejecutá AUDITOR ACTIVATION PROTOCOL.
```

Auditor self-bootstrap reads automáticamente:
- AUDITOR-PROTOCOL.md (activation section)
- BOOTSTRAP.md
- CLAUDE.md Hard Rules
- SYSTEM-ROADMAP.md
- PIPELINE.md
- **SYSTEM-LEARNINGS-V3-V4-COMPILATION.md (este documento)**
- MODEL-BEHAVIOR-LOG.md
- ARCHITECTURAL-DECISIONS.md
- + format-specific docs cuando estén creados (PAUTA-MASTER del formato, refs, SPEC template)

Después de bootstrap, Auditor confirma activation complete con 8 self-check items y procede con task.

---

## SECTION 10 — Reglas del triángulo operativo

El sistema funciona como triángulo de 3 vértices con roles específicos:

**Usuario (Tomás):**
- Decisiones creativas irreemplazables (FASE 0 elección entre opciones)
- Juicio perceptual (audio listen, visual gestalt)
- Aprobaciones de PRECEDENCE para cambios arquitecturales
- Override authority cuando justificado con razón

**Claude conversacional (Project chat):**
- Ayudante entre Usuario y código
- Estructura mensajes al Auditor
- Tracking de decisiones + bugs + patterns
- Detección meta-patrones que escapen al Auditor
- NO ejecutor — no spawn agents, no run scripts

**Auditor + Engineer + Architect (Claude Code):**
- Ejecución estructural via orchestrator
- Gates obligatorios per CP
- Spawning sub-agents con narrow scope
- Reports forenses honestos al usuario

Los 3 vértices se necesitan. Eliminar cualquiera rompe el sistema.

---

## SECTION 11 — Cierre

Este documento debe leerse completo por:
- Auditor del proyecto nuevo en activation protocol
- Claude conversacional invocado en Project antes de primer brainstorm

V4 está pagando empíricamente el conocimiento que este documento captura. Cualquier formato forward debería aprovecharlo desde CP0, no redescubrirlo.

Si aparecen findings nuevos durante producción de cualquier formato que no están en este doc, actualizarlo con append-only. Es living document.

---

**END OF DOC**
