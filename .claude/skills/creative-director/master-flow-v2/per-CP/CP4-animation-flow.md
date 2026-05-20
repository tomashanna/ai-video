# CP4 — Animation Flow (DRAFT in-flight — matadero-banquete CP4 active)

> **Status**: v1 draft 2026-05-18. CP4 matadero in flight (batch 4a pending architect commit + engineer execute). Doc captures learnings durante CP4 execution.
> **Authority**: auditor-led documentation. Architect+engineer validan + amend.
> **Próxima validation**: post-CP4 matadero closure + 2do video horror-choice.

---

## 0. Overview

**Scope**: animar N shot clips base + variants efectivos via AI model (Hailuo / Kling / Seedance / etc.) per architect SPEC. Output: video clips ready para CP5 composition assembly.

| Métrica | Valor matadero-banquete (in flight) |
|---------|---------------------------------------|
| Clips target | 22 base + 7 effective variants (shot_07-a dropped post-CP3 audit) = 29 clips |
| Tier strategy | Hailuo 02 Std 768p all-shots (user strategy 2026-05-18, Pro reserved Video 2 Phase 5 pilot) |
| Entry criteria | CP3 base + variants closed + library voice IDs validated + architect cp4_animation_model_decision + cp4_hailuo_6s_clip_workaround committed |
| Exit criteria | N/N clips delivered + cost guardrail PASS + per-clip canonical compliance audit + manifest JSON complete + POST-CHECKPOINT 4 SELF-AUDIT |
| Cost estimate | **$8.56** (29 clips × $0.27 + baseline test $0.73) o **$8.83** si shot_02 regenerado (dry-run reuse decision) |
| Cumulative projected | ~$14.6 / $17 revised budget = 86% |
| Time típico | ~60-90 min (incluyendo baseline + dry-run + audits + batches 4a/4b/4c) |

---

## 1. Pre-handoff structure (engineer)

**File**: `<proyecto>/CP4-PRE-handoff.md`

**Required sections** (per HANDOFF-PROTOCOL L91-138):
1. Lectura obligatoria (SPEC shot_list animation_intensity + cp4_animation_model_decision + MODEL-BENCHMARK + INGENIERO-PAUTA § 5.6 motion table + memorias animation_30s_rule + prompt_quality_no_vague)
2. SPEC slots involucrados (shot_list per-shot camera + motion_intensity_intent + lip_sync_required + variants picks)
3. Per-shot animation plan tabla (model tier, lip sync strategy, body horror critical flag, mini-cuts internal, premium prompt 5-block compliance)
4. Body horror climax shots escalation criteria + iter budgets
5. Cost budget tabla (Pro vs Std tier comparison + per-batch projection + per-clip tracking guardrail)
6. Self-audit criteria 8 categories (motion compliance + lip sync coherence + visual-narration match + clip duplication + camera spec + mini-cuts implementation + body horror Hailuo quality gate + D28 canonical_validation_status)
7. Plan ejecución batches por setting cluster (Mirror CP3 pattern)
8. Pre-requisitos blockers (CP2 carryover + voice library + architect amendments + Q1-Q5 + A1-A5)
9. Preguntas explícitas Q1-Q5 (architect) + A1-A5 (auditor)
10. Bloqueo explícito (no API calls hasta GO verdicts)
11. Voice library update plan (post Track A confirmation)

---

## 2. Pre-gate auditor checklist (M7/M7.7/M7.7.5 + CP4 NEW checks 5-7)

Per `AUDITOR-PROTOCOL.md` § 3 CP4:

| # | Item | Verifico |
|---|------|----------|
| C1 | Primeros 30s = animation AI obligatoria | hard rule #6 + memoria `animation_30s_rule` |
| C2 | Ken Burns fallback only ≤2-3s post 3 regen failures | hard rule #7 + cp4_animation_model_decision fallback_rules |
| C3 | Modelo per shot decision tree | MODEL-BENCHMARK § 1.2 |
| C4 | Premium prompt 5-block compliance per shot | hard rule #20 + INGENIERO-PAUTA § 5.7 |
| **C5** | **CP5 trim mandate post tool tier constraint** (added 2026-05-18) | Si Hailuo Std 6s tier > SPEC duration_intent_s → engineer commits CP5 ffmpeg trim. Architect annotation `cp[N]_<model>_<dur>s_clip_workaround_<date>` |
| **C6** | **A4 manifest schema verify** (added 2026-05-18) | JSON manifest required fields + cost guardrail halt threshold |
| **C7** | **Dry-run gate pre-cascade** (added 2026-05-18) | 1 non-critical shot test + auditor visual canonical compliance ≥10/10 PASS → batch GO |
| D28 | Cross-validate canonical_validation_status modelo | hard rule #19 expansion |

---

## 3. Pre-gate architect checklist

**TODO architect**. Auditor stub:
- Model tier choice cumple `cp4_animation_model_decision` user-approved
- Body horror climax escalation criteria defined per shot
- Variants picks animation strategy (animate each separately o subset)
- Cost overrun authorization explícita si Pro tier required + body horror upgrade

---

## 4. Execution sub-patterns observados (matadero-banquete CP4 in flight)

### 4.1 Baseline test pre-cascade (Pro vs Std comparison)

Pattern: cuando tier strategy ambigua (Pro vs Std vs other), test 1 non-critical establishing shot con 2 tiers side-by-side ($0.75 single side-by-side cost).

**Caso matadero shot_02 baseline 2026-05-18**:
- 1 Hailuo Pro 1080p clip + 1 Hailuo Std 768p clip = $0.75 total
- User visual review side-by-side
- Decision: Std 768p acceptable canonical compliance → tier strategy Std all-shots

**Lesson**: baseline test informs tier decision empirically vs estimation. Cheap insurance ($0.75 vs $4 cascade waste si tier wrong).

### 4.2 Tool tier constraint → CP5 trim workaround

Pattern: cuando AI model tier tiene clip duration mínimo > SPEC `duration_intent_s` per shot.

**Caso matadero Hailuo 02 Std**:
- Hailuo 02 Std 768p technical minimum 6s/clip per MODEL-BENCHMARK § 3.2
- SPEC duration_intent_s ranges 2-7s (most shots 3-4s)
- Workaround: 1 Hailuo 6s clip + CP5 ffmpeg trim per-clip → SPEC duration

**Architect SPEC commit**: `cp4_hailuo_6s_clip_workaround_2026_05_18` documents tool constraint acknowledgment + creative_intent_preserved + no_creative_tradeoff: true.

**Cost acceptance**: over-provisioning ~$2.29 unavoidable tool constraint, NOT engineer waste.

### 4.3 Dry-run gate pre-cascade (A4 manifest schema verification)

Pattern: ANTES de full batch execute, 1 single clip dry-run validates pipeline + JSON manifest schema + cost guardrail.

**Caso matadero shot_02 dry-run 2026-05-18**:
- 1 Hailuo Std 768p single clip = $0.264
- Engineer JSON manifest produced with required fields + traceability extras
- Auditor independent visual audit 10/10 canonical compliance PASS

**Lesson**: dry-run cheap insurance + reusable as final shot_02 (save $0.27 regen).

### 4.4 Motion velocity workaround setpts ±20% (gap #11)

Pattern: cuando motion velocity within clip percibido off (slow/fast feel) pero canonical compliance otherwise OK → CP5 ffmpeg setpts adjustment ±20% MAX.

**Caso matadero shot_02 dry-run**:
- User listen: canonical compliance + motion feel PERFECTO
- Pending verification batch 4a clips per-clip motion velocity perceptual review CP5
- Workaround codified hasta Phase 1 priority script `measure-canonical-motion-velocity.py`

**Engineering**:
```bash
# Per-clip CP5 setpts adjustment if needed:
ffmpeg -i clip.mp4 -vf "setpts=0.85*PTS" -an clip_faster.mp4   # +18% speed
ffmpeg -i clip.mp4 -vf "setpts=1.15*PTS" -an clip_slower.mp4   # -13% speed

# Cap ±20% MAX — beyond visible artifacting per frame rate degradation
```

### 4.5 Lip sync workaround per character type

Pattern: lip sync strategy varies per character architecture (humano normal vs cleaver-head vs otro).

**Caso matadero**:
- Cocinera (humano normal boca): Hedra/Sync.so standard lip sync — shots 01/20
- Matarife (cleaver-head, no human mouth): vibración mango + caption-as-mouth + voice flanger metálico — shots 03/11/17
- Narrator (off-screen): no lip sync needed

**Lesson**: SPEC per shot `lip_sync_required: true|false` + `lip_sync_strategy` field if non-standard.

---

## 5. Post-handoff structure (engineer)

**File**: `<proyecto>/CP4-POST-AUDIT-handoff.md` (TODO mid-CP4 matadero — pendiente)

**Required deliverables**:
- N clip mp4 files in `assets/clips/`
- Mini-cuts split files (shot_16/21/22) via ffmpeg post-Hailuo
- Manifest JSON con per-clip cost + tier + spec_duration_intent_s + cp5_trim_target_s
- POST-CHECKPOINT 4 SELF-AUDIT per HANDOFF-PROTOCOL L142-214
- Path B escalation reports si body horror tier upgrade needed

**Required measurements**:
- Per-clip duration (Hailuo output 6s tier) + CP5 trim target_s per shot
- Cost cumulative_usd per batch (4a / 4b / 4c)
- Body horror canonical compliance per shot (mandíbula apertura visceral, elongation, etc.)
- Motion velocity perceptual review per-clip (setpts adjustment if needed)

---

## 6. Post-gate auditor checklist

| # | Item | Method |
|---|------|--------|
| V1 | Per-clip canonical compliance audit | Visual review + scene_score motion verification (proxy until Phase 1 canonical bands) |
| V2 | Cross-clip character consistency | Matarife cleaver-head + Cocinera glow eyes + warm/cool palette consistency |
| V3 | Motion velocity perceptual review per-clip | User listen + per-clip "Perfecto/Slow/Fast" verdict → setpts ±20% if needed |
| V4 | Body horror climax canonical compliance | Visceral intent delivered per shot (shot_07 mandíbula + shot_14-16 organic horror) |
| V5 | Lip sync per character type | Matarife workaround + Cocinera Hedra/Sync.so + narrator off-screen |
| V6 | Mini-cuts internal correctly | shot_16/21/22 split from single Hailuo clip via ffmpeg |
| V7 | A4 manifest cumulative cost within budget | Per-batch tracking + halt threshold compliance |

---

## 7. Post-gate architect checklist

**TODO architect**. Auditor stub:
- Body horror climax visceral intent delivered
- Lip sync workaround perceptual coherence
- Motion velocity feel match narrative intent
- Cliffhanger emotional arc preserved

---

## 8. CP closure

**as_built annotation schema** (proposed for matadero):

```yaml
cp4_closure_<date>:
  cp4_closure_date: <YYYY-MM-DD>
  total_clips: N
  clips_first_pass: <count>
  clips_required_iter: <count>
  clips_body_horror_escalated: <count>
  motion_velocity_adjustments_setpts: [list of clips + adjustment factor]
  cost_total_cp4_usd: <X.XX>
  procedural_violations: [list NB flags]
  architect_concurrence: true
  auditor_concurrence: true
```

---

## 9. Sub-patterns matadero-banquete CP4 (in flight)

### Casos Path A/B/C/B-extension

| Path | Caso | Outcome (in flight) |
|------|------|---------------------|
| A | Hailuo Std iter — body horror per shot | PENDING — engineer execute batch 4b |
| B-extension | Tool tier constraint (Hailuo 6s mínimo) | ✅ Architect amendment cp4_hailuo_6s_clip_workaround committed L817 |
| C | Pro tier escalation if body horror Std fails | PENDING — escalation criteria defined |

### Procedural violations

NONE detected yet en CP4 matadero (TBD post-batch).

### Re-handoff cycles

| Handoff | Razón |
|---------|-------|
| PRE → architect Q1-Q5 + auditor A1-A5 | Engineer flagged cost tension Pro vs Std + 5 architect questions |
| Pre-batch dry-run | shot_02 + A4 schema verify pre-cascade |

---

## 10. Open issues forward

| # | Issue | Forward CP |
|---|-------|-----------|
| 1 | Motion velocity canonical bands measurement | Phase 1 priority script `measure-canonical-motion-velocity.py` |
| 2 | Body horror Hailuo Std capability verification | Batch 4b execute — escalate Pro tier if Std fails canonical |
| 3 | Lip sync matarife workaround perceptual coherence | CP4 batch 4a execute — review post-render |
| 4 | shot_02 dry-run reuse decision (save $0.27) | Engineer pending confirm reuse OR regenerate in batch 4a |

---

## 11. Métricas observadas matadero-banquete CP4 (in flight)

| Métrica | Valor (partial) |
|---------|-----------------|
| Clips target | 29 effective (22 base + 7 variants - shot_07-a drop) |
| Baseline test | 2 clips Pro+Std $0.73 |
| Dry-run shot_02 Std | 1 clip $0.264 |
| Total spent so far CP4 | $0.994 |
| Batch 4a pending | 14 clips Std × $0.27 = $3.78 (if shot_02 reused) |
| Batch 4b body horror | 5 clips Std × $0.27 = $1.35 (TBD escalation) |
| Batch 4c cliffhanger | 9 clips Std × $0.27 = $2.43 |
| **CP4 total projected** | **~$8.56** |
| Cumulative project | ~$14.6 / $17 revised = 86% |

---

## 12. Lessons learned codified (in-flight matadero CP4)

1. **Tier strategy informed by baseline test** (Pro vs Std side-by-side comparison) — empirical evidence > estimation. Cheap insurance pre-cascade ($0.75 baseline vs $4 batch waste).
2. **Tool tier constraint workaround** (Hailuo 6s mínimo) via architect SPEC annotation + CP5 ffmpeg trim. NOT engineer waste, NOT creative trade-off.
3. **Dry-run gate pre-cascade** (1 single shot test + A4 manifest verify + 10/10 visual canonical audit) → batch GO confidence o early escalation.
4. **Motion velocity workaround setpts ±20%** (gap #11) hasta Phase 1 canonical bands. Per-clip user/architect perceptual review CP5 → adjust if needed.
5. **Lip sync workaround varies per character architecture**: Hedra/Sync.so standard humano, vibración+caption+flanger non-humano (cleaver-head Matarife).
6. **Cost guardrail JSON manifest cumulative tracking** (halt threshold $5.50 mid-batch) prevents waste si quality fails mid-batch.
7. **shot_02 dry-run output reuse** vs regenerate batch 4a → save $0.27 if canonical compliance PASS.

---

**Última actualización**: 2026-05-18 (mid-CP4 matadero, batch 4a pending architect commit + execute)
**Próximo update**: post-CP4 closure matadero + variants animation outcome
