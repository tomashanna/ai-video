# SPEC-VS-CANONICAL-AUDIT — sala-limpia-bioseguridad (V5)

**Audited**: 2026-05-29
**SPEC**: `creative-specs/sala-limpia-bioseguridad.yaml` v11.1 (22 shots, 5 refs, 14 caps keys, 1628 lines)
**Auditor**: terminal independiente — leí PAUTA-MASTER (corregida 2026-05-29) + primary-source transcripts ref-03/09/10 + MODEL-BEHAVIOR-LOG + v11 template + cerro-aislado-v4 (precedente) DIRECTO. NO delegué al self-audit del arquitecto.

---

## Coverage tally
- `references_canonical[]` declared: **5/8**
- Coverage floor (≥5/8): ✅ **PASS**

## Per-ref linkage table

| ref_id | informs[] | Linkage substantive? | Verificación independiente |
|--------|-----------|----------------------|----------------------------|
| ref-10 | char_a.visual_signature · cliffhanger_archetype · shot_06 · drone_base | ✅ SÍ | Rurik hazmat sin-boca + P1 procedural + body horror industrial = match directo a Axel visor/protocolo. Confirmado vs ref-10 transcript ("Si lo dejas… / Si te lo pones… / Si la abres…" acción-condicional). |
| ref-03 | hook_sub_beats · shot_07 · pacing_modulation | ✅ SÍ | D1 curiosidad/obediencia calca "Si la enciendes, Bruno te agarra". SPEC shot_07 "Si lo levantas, el vial revienta" = misma estructura. |
| ref-09 | counterfactual_placement · emotional_framing · shot_02 | ✅ SÍ | ref-09 counterfactual al inicio (10/10 narrativa). SPEC shot_02 = "Si hubieras elegido a Hugo…" en posición temprana + `before_choice_resolves` + `stakes_lift`. Match exacto. |
| ref-08 | char_b · narrator_cozy_counterfactual · shot_09.has_lip_sync_required | ✅ SÍ | ref-08 Hugo (bueno) habla → licencia para Hugo hablar (cliffhanger). Outro cozy laboral análogo. |
| ref-06 | shot_18 · canonical_constraints.si_elegiste_framing | ✅ SÍ | P1 puro (peligro ofrece, no persigue). |

ref-11/12/13 excluidos con razón declarada (aceptable, floor cumplido).

## PAUTA-MASTER section compliance (verificado directo)
- § 3 consequence framing (corregido): ✅ **acción-condicional** — "Si lo levantas / Si lo dejas / Si te inyectas / Si te niegas / Si entras y respiras / Si aguantas afuera". **0 bare-label "Si elegiste A"**. Match 6/8 primary source.
- § 15 pattern: ✅ P1 (obedecer al peligroso obvio mata en 3/3 ramas A; resistir salva).
- § 24 counterfactual: ✅ `before_choice_resolves` + `stakes_lift` (canónico preferido, 10/10 ref-09).
- § 13 cliffhanger: ✅ cozy ESPECÍFICO al setting (café sala descanso + cartas + esclusa amanecer). NO template rígido. "Una noche en paz" NO usado como ley.
- Hook sub-beats: ✅ termina en countdown (Film Leader Academy AVU, digit 1.0s).
- Bueno ≥2 shots pre-cliffhanger: ✅ Hugo en shot_01 + shot_02 (+ shot_22 cliffhanger).
- § 23 cuts/min: 🟡 base 14.7 (22 shots/90s), ~18.7 percibidos con 4 reaction-inserts — **borde inferior** banda 14-22. CP5 medir directo.
- § 25 música 3 capas: 🟡 declarado (drone+ambient+accent / 6 capas) — CP4 verificar espectro.
- POV ≥80%: ✅ 100%. Español neutral: ✅ 0 voseo ("estás" = forma tú correcta). Nombres reales: ✅ Axel/Hugo.

## MODEL-BEHAVIOR-LOG constraints
- ✅ Axel (signature en visor/respiradores = objeto) + Hugo (piel translúcida = superficie) → **NO anatomía rara aislable de la cara**. `locus_anchor_required: false` para ambos (correcto). Sin riesgo face/pose-coupling. ≤3 props/shot declarado. camera_intent en frases descriptivas (no label-prefix). ✅ COMPLIANT.

## ⛔ Enforcement validators (BUILD 4/5/8) — NO RUNNABLE (structural schema mismatch)

Corrí los 3 validators de enforcement contra el SPEC real:
- `audit-spec-narrative-coherence.py` → **CRASH** `AttributeError: 'str' object has no attribute 'get'` (check_wpm/check_consequence_framing leen `narration_in_this_shot.narrator_text`, pero el campo es **string**).
- `audit-spec-narration-fits-duration.py` + `audit-spec-lip-sync-marks.py` → mismo crash (leen `.narrator_text`/`.speaker`/`.dialog_text`).

**Root cause (verificado, NO es culpa del arquitecto):**
| Campo | v11 template + cerro-aislado-v4 (precedente shipped) + este SPEC | Validators BUILD 4/5/8 esperan |
|---|---|---|
| `narration_in_this_shot` | **string** + sibling `dialog_text`/`has_lip_sync_required` | **dict** `{speaker, narrator_text, dialog_text}` |
| `hook_sub_beats` | list de **dicts** `{beat_id, timestamp, content}` | list de **strings** terminando en `"countdown"` |
| `dilema_placement_pct` | **ausente** (cerro tampoco lo tiene) | requerido ∈ [10,30] |

Los validators se escribieron con fixtures dict-form (`CLEAN_SHOT_LIST_YAML`) y **nunca corrieron contra un SPEC v11 real** (el SPEC-AUDIT de cerro predata BUILD 4/5/8). El arquitecto produjo un SPEC estructuralmente idéntico al template y al precedente cerro. **Es un bug de contrato validator↔schema, latente, surfaced ahora.**

## Verdict
- **CONTENT** (creativo/canónico): 🟢 **PASS** — P1 + framing acción-condicional + counterfactual canónico + dyad doble-monstruosa + neutral + nombres reales + refs substantivos + MODEL-BEHAVIOR-LOG compliant. Guion suena canónico (calca primary source).
- **ENFORCEMENT GATE** (runnability): 🔴 **NO-GO** — los 3 validators de enforcement no parsean el schema v11 canónico.
- **OVERALL**: ⛔ **ESCALATE** — el blocker es un bug estructural validator↔schema (NO contenido, NO arquitecto). Decisión requerida: hardening de los 3 validators al schema v11 real (string narration + sibling dialog_text + dict hook_sub_beats + manejo de dilema_placement) — contenido, ~3-5 funciones. Alternativa (cambiar template + 2 SPECs a dict-form) = más disruptiva, reabre cerro.

## NB / forward
- NB#1 cuts/min borde inferior → CP5 medir, posibles 1-2 mini-cuts (no re-emit SPEC).
- NB#2 AVU `decision-freeze-with-tick-3-2-1.mp4` no existe en library → engineer CP-pre-decisión.
- NB#3 location/signature_staging no top-level → cross-video uniqueness check no corre (verificar nesting o promover).
- NB#4 validators deben REPORTAR schema-error en vez de crashear (robustez forward).

---

## UPDATE 2026-05-29 (PM) — post validator-fix (Opción A, pattern_class 4/5)

Tomás autorizó Opción A: hardening de los 3 validators al schema v11 real (NO tocar SPEC V5 / cerro / template). Aplicado: helpers both-forms (`_narr_text`/`_beat_role`/`_wpm_band_for` + `section_id` + `has_lip_sync_required` sibling + `dilema_placement` opcional + hook dict beats) + real-artifact regression tests. **34/34 tests PASS** (20+8+6). Validators ahora **parsean el SPEC v11 real sin crash**.

### Re-audit V5 — findings reales (post-parse)

| Validator | Resultado | Triage |
|-----------|-----------|--------|
| narrative-coherence | cliffhanger ✅ · hook_order ✅ · dilema NOT_APPLICABLE · counterfactual ✅ · pattern_rotation ✅ · anti_cliche ✅ · **consequence_framing FLAG** (shot_08/13/18/19) · **WPM FAIL** (shot_01/02/03) | ver abajo |
| narration-fits-duration | **FAIL** shot_02 (320 WPM > 280 físico) | 🔴 REAL |
| lip-sync-marks | **FAIL** shot_05 + shot_15 (Axel dialog voice-off) | 🟡 validator-semantic-gap |

**Triage:**
- 🔴 **REAL — shot_02 counterfactual**: 24 palabras / 4.5s = **320 WPM** (> 280 ceiling físico TTS + > banda). Es el gap #1 que el propio arquitecto flageó ("duration tentativa, confirmar CP2"). **Requiere architect amendment**: extender `shot_02.duration_intent_s` 4.5s → ~8.5s (165 WPM) O trimear narración. **BLOQUEA CP1.**
- 🟡 **lip-sync shot_05/15 (Axel voice-off)**: Axel es **faceless** (visor sin boca) → `has_lip_sync_required:false` + diálogo voice-off es el patrón canónico documentado (AUDITOR-PROTOCOL CP4 "face-less character → lip_sync_required=false + alive signals"; calca ref-10 Rurik). El validator lip-sync NO modela la excepción faceless. **Opciones**: (a) refinar validator para aceptar `dialog_text`+lip_sync-false cuando se declara voice-off/faceless (schema field nuevo, architect+validator), o (b) aceptar como NB documentado per CP4. NO es bug de contenido.
- 🟡 NB **WPM shot_01 hook** (100 WPM): artefacto — la duración del shot (6s) incluye el countdown (3s, no-speaking); WPM efectivo ~200 in-band. Limitación del validator (divide por duración total, no speaking-time).
- 🟢 NB **consequence_framing FLAG** (shot_08/13/18/19): continuation/reaction-insert shots (0-4 palabras); la rama YA está marcada en el shot-cabeza de cada sección (shot_07 "Si lo levantas", shot_12 "Si te inyectas", shot_17 "Si entras"). FLAG correcto (no FAIL); branch marcado. Aceptable.
- 🟡 NB **WPM shot_03** (228): marginal, bajo el ceiling físico 280. Trim leve opcional.

### Verdict POST-FIX
- **ENFORCEMENT GATE runnability**: 🟢 **RESUELTO** (validators parsean v11; 34/34 tests).
- **SPEC V5 content**: 🟡 **NB → 1 fix bloqueante** — `shot_02` timing (320 WPM) requiere architect amendment antes de CP1. lip-sync faceless = decisión (refinar validator vs NB). Resto NB aceptable.
- **CP1 readiness**: 🔴 **NO todavía** — pendiente: (1) architect amend shot_02 duration; (2) decisión lip-sync faceless. Ambos contenidos/rápidos.
