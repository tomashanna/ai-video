# SPEC-VS-CANONICAL-AUDIT — cerro-aislado-v4

**Audited**: 2026-05-22
**SPEC**: `creative-specs/cerro-aislado-v4.yaml` v11.1 (40K tokens, 20 shots)
**Auditor**: 🔍 Auditor (independent terminal — read PAUTA-MASTER + canonical refs directly per AUDITOR-PROTOCOL § 1, NO delegating to architect)
**Charter**: V4-LAUNCH-CHECKLIST Gate 5 SPEC-AUDIT (codified 2026-05-22)

---

## 1. Coverage tally

| Metric | Required | Actual | Status |
|--------|----------|--------|--------|
| `references_canonical[]` entries | ≥5/8 | **5/8** | ✅ PASS |
| Each entry has `informs[]` non-empty | true | 5/5 (3-5 fields each) | ✅ PASS |
| Each entry has `why_relevant` ≥10 chars | true | 5/5 (238-373 chars) | ✅ PASS |
| Substantive (NOT boilerplate) | true | 5/5 substantive | ✅ PASS |

**Coverage floor PASS** — does NOT trigger HALT escalate.

---

## 2. Per-ref linkage table

| ref_id | Cited | informs[] field paths | Linkage substantive? | Auditor notes |
|--------|-------|----------------------|----------------------|---------------|
| ref-03 (Bruno mina P2) | YES | narrative_structure.pattern_id, slot_d_malo_dialogue_pattern, cliffhanger_archetype, consequence_b_twist_reveal, shot_18.bruno_relevo_blueprint | ✅ **YES** | Direct blueprint — "Iván meteorólogo serio = Bruno minero serio" + "Si esperás, llega cambio de turno" canonical pattern. SPEC implements in path B (shot_14-18 + outro). |
| ref-10 (Rurik fundicion) | YES | slot_g.sensory_elements, cliffhanger_outro.visual_style_lut, outro.dawn_palette_shift, consequence_path_b.dawn_transition | ✅ **YES** | "Outro café+cartas+pizza paleta industrial→dawn = nuestro cocinita+mate+cartas paleta snow-blue→amber-dawn". SPEC narrative_sections.consequence_path_b uses `warm_dawn_amber_v1` LUT. |
| ref-06 (Enzo carretera) | YES | confined_space_ratio, slot_a_atrapamiento_isolation, target_cuts_per_min, hook_setting_warning_premise | ✅ **YES** | "90% en coche = 90% en caseta" — SPEC has 17/20 shots dentro caseta (85%). Hook 4s confined-space tension reflected in hook duration. |
| ref-08 (Hugo acuario) | YES | cliffhanger_archetype_variant, outro.cozy_laboral_pattern, bueno_aparente_dialogue_in_hook | ✅ **YES** | Outro acuario laboral cozy = cognado outro montaña. "Hugo 'No me elijas' = licencia para Renato susurrando 'Esperá adentro'" — VERIFIED: Renato dialogue at t=21-23s (Slot B setup, NOT hook 0-8s) — canon majoritario preserved (Renato silent in hook). |
| ref-11 (Iván metro) | YES | char_a.recurring_role_inversion, target_cuts_per_min, audio_direction.pacing_contemplativo, silence_intentional_threat | ✅ **YES** | Iván role-flip (ritual moneda → P2 trabajador) third meta-flip post Pablo/Axel/Rurik per PAUTA § 4. Cuts/min atypical low matches pacing montaña contemplativo. User approved 2026-05-22. |
| ref-09 | NO | — | — | NOT used. Acceptable — ref-09 is P9 twist reveal, not relevant to P2 + dawn outro pattern. |
| ref-12 | NO | — | — | NOT used. Acceptable — ref-12 emotional monologue outro (Teresa) is Propuesta B territory, not P2 montaña. |
| ref-13 | NO | — | — | NOT used. Acceptable — ref-13 mini-cuts signature applies to flooding consequence; SPEC uses moderate cuts/min canonical 14-22 band per ref-11 pacing contemplativo. |

---

## 3. PAUTA-MASTER section compliance

| § | PAUTA section | SPEC compliance | Status |
|---|---------------|-----------------|--------|
| § 8 | P2 pattern (Supervivencia si manejás) | `pattern: P2` + twist relevo post-decision via Iván "Fin del turno. Bajemos." | ✅ PASS |
| § 18 | Hook 4-beat ordering canonical | name_labels → caption_setting → push_in → countdown LAST | ✅ PASS (GAP #18 fixed) |
| § 24 | Counterfactual placement enum | `good_path_at_end` (P2 canonical, NOT retrospective) | ✅ PASS |
| § 23 | Cuts/min canonical band 14-22 | `target_cuts_per_min: [14, 22]` declared | ✅ PASS |
| Hard Rule #25 | HYBRID architecture | `assembly_strategy: per_clip_atomic_hybrid` + 4 hybrid_layers explicit | ✅ PASS |
| Hard Rule #4 | Loading bar Y position | Y_pct: 52 (post-matadero GAP #14 codification, vs original Hard Rule #4 quotes Y48) | 🟡 NB (doc inconsistency — see § 5) |
| feedback_si_elegiste_framing | "SI ELEGISTE {char}" prefix | Verified shot_09 caption: "SI ELEGISTE A IVÁN..." | ✅ PASS |
| feedback_first_person_pov | POV locked all shots | All 20 shots have `pov_traversal` filled | ✅ PASS |
| feedback_spanish_neutral | Spanish neutral, NO voseo | 3 imperative phrases use voseo: "Esperá", "Inclinate", "Recalibralo" | 🟡 NB (see § 5) |
| feedback_character_real_names | Real names, no job descriptors | Iván + Renato (real names) | ✅ PASS |
| feedback_watermark_handle | `@elige_tucompanero` | `watermark_handle: "@elige_tucompanero"` | ✅ PASS |
| feedback_per_clip_atomic | Per-clip atomic forward | `per_clip_atomic_hybrid` + Layer 3 cross-clip declared | ✅ PASS |
| GAP #14 | Decision UI editorial pacing (freeze + VHS filter + countdown sync) | `decision_freeze_d1` AVU + filter LUT freeze + loading Y52 | ✅ PASS |
| GAP #40 | EXECUTION CONTINUITY | All shots have `motion_bridge_intent.from_previous + to_next` + `pov_traversal` enum + `audio_layer_continuity` | ✅ PASS |
| Hard Rule #19 | Hailuo legacy stack (NOT Veo) | 18 Hailuo shots, 0 Veo shots | ✅ PASS |

---

## 4. v11.1 schema mandatory per-shot fields

Sampled 3 random shots (shot_01, shot_04, shot_09) — **11/11 mandatory fields present in each**:
- ✅ scene_context (who_is_there + who_does_what + why_this_shot_exists + camera_intent)
- ✅ motion_bridge_intent (from_previous + to_next)
- ✅ pov_traversal enum
- ✅ audio_layer_continuity[]
- ✅ visual_style_lut
- ✅ anchor_id_required
- ✅ caption_burn_strategy (whisper_from_clip_audio)
- ✅ script_b_compliance_targets (8-dim thresholds)
- ✅ narration_in_this_shot
- ✅ visual_intent (multi-line detail)
- ✅ visual_action_match.matches_literal: true

---

## 5. NB flags (proceed but engineer/user attention required)

### NB #1 — Spanish neutral 3 imperative phrases use voseo argentino 🟡

Architect emitted text_canonical with voseo imperatives in 3 places:
- `char_b [21.0-23.0]: "Esperá adentro. Algo no anda bien."` → fix to **"Espera adentro. Algo no anda bien."**
- `char_a [41.6-43.5]: "Recalibralo. Inclinate al borde."` → fix to **"Recalíbralo. Inclínate al borde."**
- Other imperatives "Subamos" / "Bajemos" / "Sales" use nosotros + tú correctly (no fix needed)

**Action**: Engineer at CP2 TTS stage MUST patch text_canonical to neutral imperatives BEFORE TTS generation. Or architect can amend SPEC pre-CP1. User decides which.

### NB #2 — Loading bar Y52 vs Hard Rule #4 Y48 wording doc inconsistency 🟡

SPEC uses `decision_freeze_d1.overlay_loading_bar.y_pct: 52`. This reflects GAP #14 codification (matadero post-fix engineer best practice: "loading bar Y52 default not Y48"). Hard Rule #4 in CLAUDE.md still quotes original measurement "bottom: 1000px = Y 48% canonical ✓".

**Action**: NOT a SPEC blocker. Doc inconsistency for cleanup — Hard Rule #4 should be amended post-V4 to reflect GAP #14 lesson (band 44-52% acceptable, Y52 canonical safe). Add to GAPS-LOG forward.

### NB #3 — Architect's 6 production flags (for engineer attention CP1-CP4)

Architect explicitly flagged these in handoff:
1. **Iván 6-finger glove uncanny detail** — Hailuo consistency risk across 7 shots. → CP1 anchor MUST lock 6-finger detail visibly; Script B dim 6 anchor_similarity audit critical.
2. **Anemómetro 3-cup instrument** — specific terminology. → CP4 Hailuo prompt must include "3-cup spinning anemometer roof-mounted" to avoid weather-vane drift.
3. **Camioneta naranja shot_18** — exterior vehicle in snow. → Plan 3 regens + Ken Burns fallback per Hard Rule #7 if Hailuo fails.
4. **Dawn LUT cross-clip transition shot_13→14** — Layer 3 LUT continuity. → CP5 mastering must verify or generate LUT shift.
5. **Mate gourd shot_19** — Argentine cultural element. → CP4 prompt engineering required (specific reference photo or detailed prompt).
6. **`anchor_consistency_strict: false` set for 4 shots (04/12/13/15)** — all POV-only/transition shots with no character visible (`who_is_there: [viewer_pov]` only). Auditor confirms exception ACCEPTABLE per v11.1 spirit (anchor doesn't apply when no character in frame).

**Action**: Engineer reads these as CP1-CP4 attention items. Auditor reviews each per CP audit handoff.

### NB #4 — Shot count 20 at lower bound; duration sum 85s vs 90s intent

20 shots is at lower bound of 20-25 target. Duration sum 85s leaves 5s headroom for transitions + outro card. Architect documented intentional.

**Action**: NOT a blocker. Engineer at CP3-CP4 may add variants/mini-cuts if needed to hit cuts/min canonical band.

---

## 6. Verdict

```
🟢 PASS — proceed to user approval for CP1
```

**Justification**:
- 5/5 references_canonical substantively linked (above floor 5/8)
- All 9 hard constraints PASS
- All 11 v11.1 per-shot mandatory fields present in sampled shots
- All PAUTA sections checked PASS or NB (no FAIL or HALT)
- 4 NB items (3 production, 1 minor i18n) are addressable at CP1-CP2 engineer stage — no architect rework required
- Iván role-flip user-approved 2026-05-22 (cross-canon meta-storytelling PAUTA § 4 precedent)
- HYBRID architecture canonical V4+ explicit declared
- Hailuo legacy stack (no Veo billing surprise)

**No HALT triggered. No ESCALATE triggered.**

---

## 7. User decision required

Tomás: please review the SPEC + this audit + decide:

1. **🟢 APPROVE — proceed to CP1**: SPEC ready, engineer can spawn CP1 anchors generation via Script C orchestrator. NB items deferred to engineer (Spanish neutral fix at CP2 TTS, production flags at CP1-CP4).
2. **🟡 APPROVE WITH PRE-CP1 FIXES**: ask architect to patch the 3 Spanish neutral imperatives in `text_canonical` BEFORE engineer spawns CP1. ~5 min architect amend, no cost.
3. **🔴 REJECT / REWORK**: if you disagree with any of the design choices (references chosen, Iván role-flip, 20-shot count, dawn outro, etc.) — flag specifically and architect reworks.

Auditor recommendation (per Gate 5 charter — independent opinion): **Option 2 — APPROVE WITH PRE-CP1 FIXES**. The Spanish neutral patches are 3 words total, cheap fix at architect stage where they're tracked in the SPEC itself; doing them at CP2 TTS means engineer is patching text not from SPEC source-of-truth.

---

**Audit complete. Awaiting user verdict.**
