# CP3 — Shot Images Flow (DRAFT — basado en matadero-banquete IN FLIGHT)

> **Status**: v2 draft 2026-05-18. CP3 base matadero-banquete CERRADO (22/22 base shots accepted, Path B-extension applied). Variants phase pending pre-CP4.
> **Authority**: auditor-led documentation. Architect+engineer validan + amend.

---

## 0. Overview

**Scope**: generar N shot images base usando anchors CP1 como reference + 5-block premium prompts per shot. Output: imágenes estáticas listas para CP4 animation layer.

| Métrica | Valor matadero-banquete (in flight) |
|---------|---------------------------------------|
| Shots target | 22 (19 HERO + 3 STANDARD) |
| Variants -a/-b/-c per hard rule #5 | Spirit-not-literal: 4-6 shots seleccionados (min 4) — **PENDING Q7 variants phase pre-CP4** |
| Entry criteria | CP1 + CP2 cerrados + SPEC `shot_list` 22 entries + `image_direction` |
| Exit criteria | N/M shots PASS visual audit + cross-shot consistency + contact-sheet + as_built CP3 annotation |
| Cost estimate | $3.97 base + $1.61 variants = ~$5.58 / range $2.65-6.61 |
| **Cost real CP3 (base only)** | **$3.05** (shot_07 + shot_12 v1 + Batch 3a 12 + regens + 3b + 3c + shot_20 iter 2 + 2 gates) |
| Cost acumulado proyecto post-CP3 base | **$4.66 / $12 = 38.8%** |
| Time típico | ~30-45 min (parallel batches by setting cluster) |
| Budget % | ~25% del total proyecto (base only; +$1.61 if variants ejecutan) |

---

## 1. Pre-handoff structure (engineer)

**File**: `<proyecto>/CP3-PRE-handoff.md`

**Required sections**:
1. Lectura obligatoria (SPEC shot_list completo + reference_anchors + aesthetic_strategy + as_built blocks + memorias prompt_quality + first_person_pov + visual_matches_narration)
2. SPEC slots involucrados
3. Anchors usage matrix per shot (N-tabla: shot_id × tier × quality × refs_count × anchor_bundle)
4. Special handling per shot (HIGH RISK shots flagged — body horror climax, complex multi-character, deferral gates)
5. Engineer-domain decisions (model strategy, prompt construction approach, iteration budget, tooling reuse)
6. Self-audit criteria per shot + cross-shot
7. Plan ejecución (batch clusters by setting + cost + time)
8. Pre-requisitos (CP3 blockers + items not blocking CP3 but blocking CP4)
9. Preguntas explícitas Q1-QN (architect) + A1-AN (auditor)

**Authority cited (must)**:
- SPEC shot_list line numbers per shot (scene_context + camera + visual_action_match + lip_sync_required)
- SPEC aesthetic_strategy (LUTs + paleta dual + vignette)
- SPEC as_built blocks (path_b_deferrals_active, etc.)
- Memorias: prompt_quality_no_vague, first_person_pov, visual_matches_narration, quality_standards
- INGENIERO-PAUTA § 5 (vignette/saturation/brightness)
- Hard rules #5 variantes + #19 + #20

---

## 2. Pre-gate auditor checklist

Per `AUDITOR-PROTOCOL.md` § 3 CP3:

| # | Item | Verifico |
|---|------|----------|
| A1 | Multi-anchor concurrent refs capability | MODEL-BENCHMARK L1232 (Pro tier 5 personajes / 14 imagenes ref) |
| A2 | Cost estimate vs Pro 2K pricing | $0.134/img × N + iter buffer |
| A3 | Tooling reuse (image.py + validate-cocinera + build-contact-sheet) | Validado CP1 |
| A4 | SPEC trigger gates consistent threshold | Validation scripts thresholds match SPEC line citations |
| A5 | NO UI/captions in CP3 base images | CP3 base / CP4 animation / CP5 composition separation |
| A6 | Contact-sheet review format | 4×N grid suficiente for visual cross-shot review |
| A7 | AI failure modes documented per HIGH-RISK shot | Body horror climax + uncanny features patterns |

**Plus structural CP3 audit**:
- Variantes -a/-b/-c per hard rule #5 (spirit-not-literal OK con per-shot marking)
- Character consistency cross-shot planeada (anchors as refs per shot)
- Paleta dual ejecutada per shot tag (cool industrial vs warm cozy vs body horror flesh)
- POV ratio 100% (per SPEC D14)
- lip_sync_required marker per shot (per SPEC D17)
- Hard rule #21 SPEC storyboard-level drives prompts

---

## 3. Pre-gate architect checklist

**TODO architect**. Auditor stub:
- Anchor bundle matrix per shot adequate (extra anchors needed?)
- Cinematic reference per HIGH-RISK shot (Cronenberg / Tetsuo / etc.)
- Special handling shots ratios (climax / multi-character / deferral)
- Iteration budget cap per tier (HERO 1.5 avg / 3 max, STANDARD 1 avg / 2 max)
- Batch ordering (cluster vs chronological vs risk-first)

---

## 4. Execution sub-patterns observados (matadero-banquete CP3 in flight)

### 4.1 Test-first strategy (HIGH-RISK shot single antes de cascade)

Pattern: cuando hay shot con highest risk (body horror climax shot_07), engineer test ONE primero ($0.13) → validate Pro generation pipeline → cascade Batch 3a full o escalate.

**Caso matadero shot_07**: 
- "carcasa abre la boca grande" — risk: Pro renders literal surgical incision o normal carcass o safety block
- Engineer plan: test shot_07 alone → if PASS, cascade Batch 3a; if FAIL, escalate to Midjourney v7 manual
- Cost gate: $0.13 vs $4 cascade

**Authority**: architect Q5 + Q7 verdicts. Auditor concurrence.

**Lesson**: test-first es PATRÓN canónico para shots con AI failure modes documentables. Aplicar siempre en CP3 cuando ≥1 shot tiene "Pro might fail" risk.

### 4.2 Spirit-not-literal variants (hard rule #5)

Pattern: hard rule #5 "variantes -a/-b/-c en escenas >4s" se interpreta **spirit-not-literal**: variants donde realmente aportan retention, no automáticamente en TODO shot >4s.

**Caso matadero**: 12 shots candidatos >4s. Architect+auditor concur: marking categories per-shot: `VARIANTS_CP3` / `MOTION_VARIETY_CP4` / `SHORT_OK`. Min 4 shots con variants base CP3.

**Authority caveat auditor**: per-shot explicit marking OBLIGATORIA. Documentar in-SPEC `cp3_variants_strategy_<date>` annotation.

**Lesson**: hard rules "literal compliance" pueden cargarse de costo excesivo. Spirit-not-literal interpretation defendible CON explicit marking + min-count enforcement (no skip-all).

### 4.3 SPEC trigger gate violation (procedural NB flag)

Pattern: SPEC declara trigger gate (e.g. `path_b_deferral.escalation_trigger`) que bloquea downstream shots. Engineer puede inadvertidamente parallel-process antes de gate check.

**Caso matadero shot_20**: 
- SPEC L574: "if shot_20 generated <28 teeth, ESCALATE before proceeding"
- Engineer parallel-generated shot_21 + shot_22 ANTES de gate check shot_20
- $0.24 sunk (irreversible)

**Verdict auditor**: NB flag procedural (lesson learned, no rollback feasible).

**Lesson**: SPEC explicit triggers DEBEN block downstream shots, NO parallel-generate. Engineer plan debe respetar order del trigger. Forward: agregar trigger compliance check a engineer self-audit pre-execute.

### 4.4 Path A/B/C cuando shot trigger gate falla — y nueva distinction Path B vs Path B-extension

Pattern: cuando gate trigger dispara (e.g. teeth count <28), engineer presents 3 paths.

**Caso matadero shot_20 (iter 1 = 16 teeth, iter 2 EXTREME = also <28)**:
- Path A: iter 2 con prompt EXTREMO ($0.13) — auditor GO, **FAILED Pro ceiling sistemático**
- Path B: engineer attempts to bypass — accept current (VIOLA SPEC L574 trigger — auditor REJECTED ✓ correct call)
- Path C: escalate Midjourney v7 manual — auditor recommended fallback
- **Path B-extension**: architect amends SPEC threshold post-escalation con canonical rationale — **NEW PATTERN descubierto CP3 cierre**

**Outcome real CP3 matadero**:
- Path A iter 2 EXTREMO también falló Pro ceiling
- 4 iterations total tested (cocinera anchor v1 + v2 + shot_20 iter 1 + iter 2) — Pro ceiling sistemático CONFIRMED
- Path C (Midjourney) considerada pero deferred — not cost-effective for non-load-bearing dimension
- Architect emitió **Path B-extension** verdict: re-categorize teeth count como "uncanny enrichment NOT load-bearing for P6 trap pattern". Load-bearing dimensions (warm welcoming expression + glow eyes #FF6B1F + uniform dense smile qualitative + stained chef coat + micro-burns + warm palette) ALL delivered. Trap reveal operates via narration + cozy seduction, no via dental count.
- Gate threshold lowered: "visible uniform dense teeth" (qualitative) vs original numerical 28-32

**Auditor concurrence retroactive**: ✅ CONCUR Path B-extension. Per PAUTA-MASTER § 9 hallazgo "signatures buenos categóricas NO numerical" + ref-13 analysis "load-bearing dimensions per archetype". Architect re-categorization defendible.

**Distinction CRÍTICA**:

| Pattern | Quién inicia | Auditor verdict default |
|---------|--------------|--------------------------|
| **Path B** (engineer accept current bypass) | Engineer | ❌ REJECT — viola SPEC trigger |
| **Path B-extension** (architect SPEC amendment post-escalation) | Architect (post-escalate trigger fire) | ✅ Concur if rationale canonical |

**Lesson learned crítico**: el SPEC trigger gate "ESCALATE before proceeding" es **el punto donde architect debe re-evaluate threshold con canonical authority**, no engineer bypass. Trigger fire correctly escalates → architect decides amend o stick. Engineer NUNCA bypassea solo.

**Authority**: AUDITOR-PROTOCOL § 5 + ahora extended: "Path B-extension" requiere architect canonical rationale documented in-SPEC, NO engineer-domain decision.

### 4.5 Pro ceiling pattern (training data defaults) — confirmed sistemático

Pattern: Gemini Pro tiene "ceiling" en features fine-detail (teeth count, specific count instructions). Triple negative reinforcement rompe ~50% de defaults; pero algunos features hit hard ceiling no breakable by prompt.

**Casos matadero (confirmed sistemático tras CP3 cierre)**:
- Cocinera anchor v1: 28-32 target → Pro delivered ~14
- Cocinera anchor v2: 28-32 target + extreme prompt → Pro delivered ~20-22
- shot_20 close-up iter 1: 28-32 target + close-up prompt → Pro delivered 16
- shot_20 close-up iter 2 EXTREME ("30 teeth count enforcement, 60% mouth crop") → Pro delivered <28 again
- Matarife gloves: SPEC "up to elbows" → Pro defaulted mid-forearm → triple negative fixed v2 ✓ (breakable)
- Matadero clock "EXIT" → Pro corrected to "5:40 AM" via explicit instruction ✓ (breakable)

**Pattern observado**: features breakable (qualitative position/object) vs features non-breakable (specific numerical counts especially anatomical).

**Lesson confirmed**: Pro ceiling para **numerical anatomical counts** = candidate para architect Path B-extension (re-categorize as enrichment) OR Path C (escalate alternative tool) si load-bearing. NO insist iter 3+ con Pro si pattern repetido.

**Forward implication**: spec design should AVOID numerical anatomical counts when possible — prefer qualitative descriptions ("uniform dense smile" vs "28-32 teeth"). Documentar in PAUTA-MASTER / INGENIERO-PAUTA forward.

### 4.6 Batch clustering by setting

Pattern: minimize ref-image switching cost generando shots por setting cluster en paralelo.

**Caso matadero**:
- Batch 3a: 14 shots matadero_interior cluster (matarife + cocinera + matadero + cuchillo + olla refs)
- Batch 3b: 3 shots pasillo_carne body horror cluster (pasillo ref)
- Batch 3c: 5 shots cliffhanger cluster (cocinera + exterior + comedor + olla refs)

**Authority architect Q6**: GO con modified cluster (specific modification engineer-dominated).

**Lesson**: cluster ordering canonical pattern. Modifications architect-domain (Q6 verdict).

---

## 5. Post-handoff structure (engineer)

**File**: `<proyecto>/CP3-POST-AUDIT-handoff.md` (TODO mid-CP3 matadero — pendiente)

**Required deliverables**:
- N shot PNG files in `assets/shots/`
- Variants -a/-b/-c per shot marcado VARIANTS_CP3
- Contact-sheet final 22-shot grid (e.g. 4×6 or 5×5)
- Per-shot self-audit table
- Path B/C resolution if any trigger fired

**Required measurements**:
- Per-shot character consistency cross-shot (matarife/cocinera signature features)
- Cross-shot setting coherence (matadero hooks layout, comedor pendant lights)
- Paleta dual visible (cool 14 shots + warm 6 shots + body horror 3 shots)
- SPEC trigger gates resolution (shot_20 teeth gate PASS/FAIL outcome)
- POV consistency 22/22 + lip_sync_required marker preserved

---

## 6. Post-gate auditor checklist

| # | Item | Method |
|---|------|--------|
| V1 | Character consistency cross-shots | Visual review matarife in shots 01/03/10/11/12/17 + cocinera in 01/12/13/20/21/22 |
| V2 | Setting consistency cross-shots | Visual review matadero hooks layout + comedor pendant lights |
| V3 | Visual matches narration LITERAL (D20) | Per shot: visual element matches narration text |
| V4 | Cross-anchor signatures preserved in shots | Clock 5:40 AM in matadero + comedor shots, blue gloves cross-PPE |
| V5 | Paleta dual ejecutada | Cool 14 + warm 6 + flesh tones 3 visible |
| V6 | Variants -a/-b/-c en min 4 shots VARIANTS_CP3 marked | Count + types of plano distinct |
| V7 | SPEC trigger gates resolved | shot_20 teeth count PASS or escalated |
| V8 | NO UI/captions/text in base images | Spot-check |
| V9 | Aspect 9:16 enforced | Sample check |

**Gemini Vision audit programmatic**:
- shot_20 teeth count (validate-cocinera.py threshold [28, 32])
- Other quantifiable features

---

## 7. Post-gate architect checklist

**TODO architect**. Auditor stub:
- shot_07 body horror coherence (creative review — Cronenberg aesthetic intent)
- shot_12 dual visibility (Matarife sharp + Cocinera ghost-blurred works)
- Variants TIPOS DE PLANO distinct (wide / close-up / lateral / picado)
- Overall narrative arc visible from contact-sheet

---

## 8. CP closure

**as_built annotation schema** (proposed for matadero):

```yaml
cp3_closure_<date>:
  cp3_closure_date: <YYYY-MM-DD>
  total_shots: N
  shots_first_pass: <count>
  shots_required_iter: <count>
  shots_escalated_path_c: <count>
  variants_strategy:
    decision: "spirit-not-literal hard rule #5"
    shots_with_variants_cp3: [list]
    shots_motion_variety_cp4: [list]
    shots_short_ok: [list]
    min_variants_cp3_count: 4
  spec_trigger_gates_resolutions:
    - shot_id: <shot_20>
      gate: path_b_deferral teeth count
      outcome: <PASS|ESCALATED_PATH_C>
      final_count: <N>
  cost_total_cp3_usd: <X.XX>
  procedural_violations: [list NB flags]
  architect_concurrence: true
  auditor_concurrence: true
```

---

## 9. Sub-patterns matadero-banquete CP3 (concrete examples)

### Casos Path A/B/C

| Path | Caso | Outcome (in flight) |
|------|------|---------------------|
| A | shot_20 teeth iter 2 con prompt extremo | PENDING — engineer execute |
| B | shot_20 accept 16 teeth | ❌ REJECTED auditor (viola SPEC L574 trigger) |
| C | shot_20 → Midjourney v7 manual (if Path A iter 2 fails) | PENDING — contingent |

### Test-first

| Shot | Risk | Outcome |
|------|------|---------|
| shot_07 climax body horror | Pro literal interpretation / safety filter / normal carcass | PENDING — test pre-cascade |

### Procedural violations

| Violation | Daño | Lesson |
|-----------|------|--------|
| shot_21 + shot_22 parallel-generated antes de shot_20 gate check | $0.24 sunk irreversible | Forward: SPEC trigger compliance check en engineer self-audit pre-execute |

### Re-handoff cycles

| Handoff | Razón |
|---------|-------|
| PRE → execute | Architect Q1-Q7 + auditor A1-A7 verdicts + spirit-not-literal concurrence + shot_07 test-first approved |
| Mid-execute trigger fires | shot_20 teeth gate <28 → Path A/B/C decision |

---

## 10. Open issues forward

| # | Issue | Forward CP |
|---|-------|-----------|
| 1 | shot_20 teeth gate Path A iter 2 outcome | CP3 cierre |
| 2 | Variants execution post Q7 marking list | CP3 cierre |
| 3 | shot_07 body horror Pro generation outcome | CP3 cierre or escalate Midjourney |
| 4 | Matarife per-segment audio listen test pre-CP4 | CP4 lip sync |
| 5 | CP4 model decision Hailuo 02 Pro all-shots + user budget $6 | CP4 entry |

---

## 11. Métricas observadas matadero-banquete CP3 (cierre base — 2026-05-18)

| Métrica | Valor |
|---------|-------|
| Shots target | 22 base + variants pending Q7 phase |
| Shots base generated | **22/22** |
| Shots first-pass PASS | 18/22 |
| Shots required regen | 4/22 (~18%) — incluye 2 anchors CP1 cross + shot_01 + shot_12 |
| shot_20 teeth iterations | 2 (iter 1 + iter 2 EXTREMO, ambos FAIL Pro ceiling) |
| **Cost CP3 base only** | **$3.05** |
| Cost acumulado proyecto post-CP3 base | $4.66 / $12 = 38.8% |
| Cost variants pending (estimated) | $1.07-1.61 (4-6 shots) |
| SPEC triggers fired | 1 (shot_20 teeth gate — RESOLVED via Path B-extension architect amendment) |
| Path A applied | 1 (shot_20 iter 2 — FAILED Pro ceiling) |
| Path B (engineer bypass) rejected by auditor | 1 (correct call — escalation triggered properly) |
| **Path B-extension applied (architect amend post-escalate)** | 1 (shot_20 → architect re-categorize teeth count as non-load-bearing per PAUTA-MASTER § 9 + ref-13 load-bearing analysis) |
| Path C deferred | 1 (Midjourney v7 manual — deferred, not cost-effective for non-load-bearing) |
| Procedural violations (NB flag) | 1 (parallel shot_21+22 pre shot_20 gate — irreversible, lesson learned forward) |
| Test-first executed | 1 (shot_07 climax — PASS, cascade unlocked) |
| Pro ceiling sistemático CONFIRMED | Yes (4 iterations all hit ceiling on teeth count) |

---

## 12. Lessons learned codified (post-CP3 closure)

1. **Test-first PATRÓN canónico** para shots con AI failure modes documentables. shot_07 climax PASS confirmed pattern viable.
2. **Spirit-not-literal variants** defendible CON explicit per-shot marking + min-count enforcement.
3. **SPEC explicit triggers DEBEN bloquear downstream**, NO parallel-process. Forward: check en engineer self-audit pre-execute.
4. **Path B vs Path B-extension distinction CRÍTICA**:
   - Path B (engineer bypass attempt) — ❌ default reject
   - Path B-extension (architect SPEC amendment post-escalation con canonical rationale) — ✅ concur if defendible
   - El trigger gate "ESCALATE before proceeding" es el punto donde architect re-evaluates threshold, NO engineer bypassea solo
5. **Pro ceiling sistemático para numerical anatomical counts** (4 iterations confirmed). Features breakable: qualitative position/object. Features non-breakable: specific numerical counts especially anatomical. **Forward SPEC design**: AVOID numerical anatomical counts — prefer qualitative ("uniform dense smile" vs "28-32 teeth"). Documentar in PAUTA-MASTER / INGENIERO-PAUTA-MASTER.
6. **Batch cluster by setting** canonical pattern para parallel execution + minimize ref switching.
7. **Path B deferral chain works**: anchor → CP3 close-up → architect amendment. Validates the deferral pattern (gate fires properly, architect decides amend).
8. **Load-bearing vs enrichment dimension distinction** (NEW lesson from architect Path B-ext rationale): per archetype, identify which visual dimensions are load-bearing for the pattern reveal (e.g. P6 trap: cozy seduction + glow eyes + counterfactual reveal = load-bearing; teeth count = enrichment). When Pro ceiling hits enrichment dimension → Path B-extension viable. When Pro ceiling hits load-bearing → Path C escalate.
9. **Cost discipline**: CP3 ended $3.05 base (vs estimate $3.97). Test-first + Path B-extension (instead of $0.36 iter 3 + Midjourney time) saved budget. Validates careful gate-driven decision making.
10. ⭐ **Variants composition validation NOT just intra-shot, ALSO vs adjacent base shots** (caso disparador shot_07-a vs shot_08 absorption_pov 2026-05-18). Architect Q7 picked shot_07-a "close-up engulfed mouth-dominant POV" pero shot_08 base ya cubría exact composition (front-view mouth-dominant POV + viewer hands + knife falling). Result: shot_07-a redundant editorial — cost sunk $0.134, CP4 engineer puede ignore o swap. Lesson codified AUDITOR-PROTOCOL § 3 CP3 punto 2.1+2.2 + ARCHITECT-MASTER-FLOW § 5.1 amendment forward. Auditor fault: concur picks list sin cross-validation adjacent base composition diversity.

---

**Última actualización**: 2026-05-18 (post-CP3 base closure, Path B-extension applied)
**Próximo update**: post-Q7 variants phase execution + CP4 animation entry
