# V4 LAUNCH CHECKLIST — Pre-launch verification gates

> **Purpose**: structural gate before any V4 video production starts. ALL items checked = V4 ready. Any unchecked = V4 BLOCKED.
>
> **Status**: pre-V4 lock. Updated 2026-05-21 PM late post V3 archived + enforcement scripts built.
>
> **Critical principle**: V4 launch ONLY via `scripts/orchestrator-cp-by-cp.py` (Script C). NO manual agent spawning bypass.

---

## ⛔ Pre-launch hard gates (ALL must PASS)

### Gate 1 — Enforcement scripts present + tested

```
□ scripts/build_clip_atomic.py (Script A) — caption-burn extension
   ✓ Built? [yes/no]
   ✓ 10/10 functional tests PASS? [yes/no]
   ✓ Adversarial ADV-A PASS? [yes/no]
   ✓ Test report: /tmp/script_a_test_report.md

□ scripts/audit-shot-spec-compliance.py (Script B) — per-shot SPEC compliance 8 dim
   ✓ Built? [yes/no]
   ✓ Adversarial V3 archive detects KNOWN bugs?
     - Caption drift 0-34s on shots 01-05 (dim 3 FAIL)? [yes/no]
     - Hook caption ABSENT (dim 2 FAIL shot_01)? [yes/no]
     - Bryan visual inconsistency cross-shots (dim 6)? [yes/no]
   ✓ Test report: /tmp/script_b_adversarial_test.md

□ scripts/orchestrator-cp-by-cp.py (Script C) — CP-by-CP gate state machine
   ✓ Built? [yes/no]
   ✓ Adversarial tests PASS:
     - C9 multi-CP prompt → REFUSE? [yes/no]
     - C2 skip CP handoff → HALT? [yes/no]
     - C4 FAIL verdict propagation → HALT? [yes/no]
     - C7 override without reason → REJECT? [yes/no]
     - C6 valid override → ALLOW + log to ARCHITECTURAL-DECISIONS.md? [yes/no]
   ✓ Test report: /tmp/script_c_adversarial_tests.md

□ ARCHITECTURAL-DECISIONS.md present + schema valid
   ✓ File exists at master-flow-v2/? [yes/no]
   ✓ YAML schema documented + validated? [yes/no]
```

### Gate 2 — Documentation aligned

```
□ CLAUDE.md Hard Rule #24 active (CP-by-CP gates mandatory)
□ CLAUDE.md Hard Rule #25 active (HYBRID architecture canonical)
□ PIPELINE.md § 13.9 HYBRID architecture explicit recipe
□ PIPELINE.md § 13.9 references 3 scripts as BLOCKER (not "no-blocker")
□ AUDITOR-PROTOCOL.md § 6 anti-pattern #15 (engineer multi-CP FORBIDDEN)
□ AUDITOR-PROTOCOL.md § 6 anti-pattern #16 (caption-audio sync verification)
□ BOOTSTRAP.md amended — 3 enforcement scripts in copy list
□ CONTRACT-A-B-INTERFACE.md exists (binding contract)
```

### Gate 3 — SPEC v11 architect template ready

```
□ creative-director/templates/CREATIVE-SPEC-TEMPLATE-v11.yaml exists
□ Schema includes mandatory hybrid fields:
   ✓ assembly_strategy: per_clip_atomic_hybrid (forward V4+)
   ✓ per-shot motion_bridge_intent (from_previous + to_next)
   ✓ per-shot pov_traversal enum
   ✓ per-shot audio_layer_continuity list
   ✓ per-shot visual_style_lut reference
   ✓ per-shot narration_in_this_shot (for Script B dim 1+2)
   ✓ per-shot visual_intent (for Script B dim 4+5)
   ✓ per-shot scene_context.who_is_there (for Script B dim 6)
   ✓ per-shot scene_context.who_does_what (for Script B dim 7)
   ✓ counterfactual_placement enum (NEVER after_both_paths_retrospective)
   ✓ music_continuous_layers (Layer 3 cross-clip)
   ✓ characters[] with real invented names (NEVER job descriptions)
```

### Gate 4 — System state ready

```
□ V3 archived cleanly at _archive-phase3-v3-learning/
□ Active session state memory updated (V3 closure + V4 readiness)
□ No in-flight V3 iter (clean slate)
□ Cinema + matadero remain reference baselines
□ Cost ceiling configured ($5/video default Script C halt)
□ Timeout ceiling configured (50 min/CP default Script C halt)
```

### Gate 5 — Auditor commitment (amended 2026-05-22 — explicit SPEC-AUDIT canonical charter)

```
□ Auditor (Claude session) commits to enforcement via Script C ONLY
□ NO manual agent spawning bypass during V4 production
□ Engineer agent invocations = ONE per CP maximum
□ Auditor gate spawn between every CP (anti-pattern #15)
□ Caption-audio sync verification mandatory per shot during CP4 (anti-pattern #16)
□ ⭐ NEW SPEC-AUDIT charter (pre-CP1, addresses canonical quality gap 2026-05-22):
```

#### SPEC-AUDIT charter — explicit auditor responsibilities (pre-CP1)

When the Architect emits `creative-specs/<id>.yaml v11.1`, the Auditor MUST produce a formal output `SPEC-VS-CANONICAL-AUDIT.md` BEFORE user approval gate. This output enforces canonical quality at SPEC stage where it is cheapest to fix.

**Charter responsibilities (binding for V4+)**:

1. **Read canonical authority directly** (NOT delegated):
   - `horror-choice-format/PAUTA-MASTER.md` (creative authority — 8 viral refs synthesized)
   - `horror-choice-format/canonical-scenes/INDEX.md` (cross-ref grid)
   - All 8 canonical refs: `canonical-scenes/ref-03/06/08/09/10/11/12/13.md` (or whichever 8 are present)

2. **N/8 canonical refs coverage verification**:
   - Count `references_canonical[]` entries declared in SPEC v11.1
   - Each entry MUST cite a real `ref_id` matching `canonical-scenes/ref-XX*.md`
   - Each entry MUST have `informs: [<SPEC field paths>]` array (≥1 field referenced)
   - Each entry MUST have `why_relevant: "<≥10 chars rationale>"` non-empty
   - Verify the linkage is SUBSTANTIVE (not boilerplate like "general inspiration")

3. **Coverage floor — minimum 5/8 refs cited with substantive linkage**:
   - IF `len(references_canonical) < 5` → HALT + escalate to Tomás before CP1 advances
   - IF entries exist but linkage is shallow (no informs array OR generic why_relevant) → HALT + escalate
   - Rationale: <5/8 means architect leaned on personal taste or single-ref pattern matching, not empirical synthesis

4. **Cross-check declared linkage against SPEC actual content**:
   - For each `informs: [<field_path>]`, verify the cited SPEC field actually exists AND its content reflects the ref's pattern
   - Example: if `informs: ["narrative_structure.cliffhanger_archetype"]` for ref-08, the cliffhanger archetype in SPEC should align with ref-08's observed pattern
   - Catch decorative ref citations (architect cites ref but SPEC doesn't actually use it)

5. **Output format — `SPEC-VS-CANONICAL-AUDIT.md`** (mandatory, file-based handoff):

```markdown
# SPEC-VS-CANONICAL-AUDIT — <project_id>

**Audited**: <ISO date>
**SPEC**: creative-specs/<id>.yaml v11.1
**Auditor**: independent terminal, read PAUTA-MASTER + 8 refs directly

## Coverage tally
- references_canonical[] declared: N/8
- Coverage floor (≥5/8): [PASS|FAIL]

## Per-ref linkage table

| ref_id | Cited in SPEC | informs[] fields | Linkage substantive? | Notes |
|--------|---------------|------------------|----------------------|-------|
| ref-03 | YES | narrative_structure.cliffhanger_archetype, characters.char_a.visual_signature | ✅ YES — cliffhanger pattern matches P9 dyad observed | — |
| ref-06 | YES | hyperframes_ui_overlay.countdown | 🟡 PARTIAL — countdown cited but ref-06 uses different visual style | Suggest add visual_style_lut reference |
| ref-08 | NO | — | — | NOT used. Why omitted? (acceptable if rationale present in architect_annotations) |
| ref-09 | YES | narrative_structure.counterfactual_placement | ✅ YES — "good_path_at_end" pattern matches ref-09 | — |
| ref-10 | YES | characters.char_b.visual_signature | ✅ YES — uncanny smile aesthetic shared | — |
| ref-11 | NO | — | — | NOT used |
| ref-12 | YES | editing_targets.target_cuts_per_min | ✅ YES — pacing band cited | — |
| ref-13 | YES | editing_targets.transition_variety_min, ui mini-cuts | ✅ YES — mini-cuts signature codified | — |

## PAUTA-MASTER section compliance check
- § 18 hook sub-beats ordering: [PASS|FAIL] — SPEC.narrative_structure.hook_sub_beats matches canonical 4-beat order
- § 24 counterfactual_placement: [PASS|FAIL] — SPEC enum value canonical (NOT after_both_paths_retrospective)
- § 23 cuts/min: [PASS|FAIL] — SPEC.editing_targets band aligns 14-22
- (...add per critical PAUTA section)

## Verdict
- 🟢 PASS — proceed to user approval for CP1
- 🟡 NB (note bene) — proceed but flag warnings for user attention
- 🔴 HALT — SPEC needs architect rework before CP1. Specific gaps below:
  - <list specific issues>
- ⛔ ESCALATE — fundamental canonical drift, user decision required
```

6. **Block CP1 advancement if HALT/ESCALATE verdict**:
   - Auditor emits verdict file BEFORE Script C orchestrator can advance to CP1_ENG state
   - User MUST acknowledge verdict (PASS/NB unblock; HALT requires architect rework)
   - Override path: `--override-spec-audit-fail --reason "<≥10 chars>"` logs to ARCHITECTURAL-DECISIONS.md

7. ⭐⭐ **MODEL-BEHAVIOR-LOG constraints verification** (NEW 2026-05-22 PM late post V4 shot_16 stability budget discovery):
   - Auditor MUST read `.claude/skills/video-director/MODEL-BEHAVIOR-LOG.md` entries
   - For each documented model constraint, verify SPEC shots respect the constraint
   - Current entries to enforce:
     - **Entry 1 (Gemini --ref face-coupling + stability budget + POSE-coupling)**:
       - For shots with characters with `visual_signature` anatomical signature features (polydactyl / extra eyes / prosthetic / etc.) — verify ALL THREE conditions:
         (a) face+hand co-located in composition (face-coupling works), AND
         (b) ≤3 distinct prop elements beyond the anchor character itself (stability budget), AND
         (c) shot hand pose MATCHES anchor hand pose (pose-coupling — NEW 2026-05-22 PM late late finding)
       - For shots that isolate the signature locus from face (hand-only / detail-only): verify SPEC declares dedicated locus anchor in `asset_list.anchors_to_generate` (e.g., `char_X_v1_hand` for hand-only compositions). Locus anchors are pose-TOLERANT (no face = no inconsistency penalty).
       - For shots where shot hand pose ≠ anchor hand pose: verify SPEC declares locus anchor with matching shot pose in asset_list (Sprint B will auto-check via `audit-spec-pose-coupling.py` per Gap #49)
       - If SPEC violates any of (a) / (b) / (c) AND no locus anchor declared → AUDITOR HALT, escalate architect to amend BEFORE CP1
   - Future entries: as new MODEL-BEHAVIOR-LOG entries are added, this auditor verification expands per entry's `implications_forward.architect_CP0` block
   - **Sprint B priority ALTA**: `scripts/audit-spec-stability-budget.py` will automate this check (Gap #48 codified GAPS-LOG)

**Why this charter exists** (caso disparador 2026-05-22):
- Gap identified by Tomás: V4 system enforces "SPEC compliance" (Script B 8 dims) perfectly but does NOT enforce "horror-choice canonical quality" structurally
- Canonical knowledge was input-only (Architect consults refs, then SPEC fields encode decisions) but never propagated as structured queryable data
- Charter codifies the canonical floor at SPEC stage where it is cheapest to fix (vs detecting in CP5 final render)
- Phase 4 priority (Option A): Script B dim 8 vs canonical refs frame-by-frame — DEFERRED, tracked in GAPS-LOG #43

---

## 🚀 Launch procedure (when all gates PASS)

```
1. User triggers: "iniciar V4 con orchestrator-cp-by-cp.py"

2. Orchestrator (Script C) starts:
   - Spawn architect → emit creative-specs/<id>.yaml v11
   - Auditor audit SPEC vs PAUTA + canonical-scenes ref-XX
   - REQUIRE SPEC-AUDIT-verdict.md PASS before proceeding
   - User approval gate (CP0)
   
3. Per CP1-CP5 (sequential, enforced):
   - Orchestrator spawn engineer narrow CP[N] scope
   - Engineer emits CP[N]-handoff.md
   - Orchestrator spawn auditor for CP[N]
   - Auditor emits CP[N]-AUDIT-verdict.md
   - REQUIRE PASS before spawning CP[N+1]
   - IF FAIL → orchestrator HALT, escalate user
   - IF NB → orchestrator continue with warning logged
   
4. CP4 special — per-shot SPEC compliance gate:
   - Engineer emits per-shot atomic clips via Script A (captions burned)
   - Auditor runs Script B per shot (8 dim verification)
   - IF any shot FAILs Script B → engineer regen that shot
   - Max 3 iter per shot → escalate

5. CP5 final assembly:
   - Engineer HyperFrames composition + Layer 3 audio
   - Auditor 8 pre-render gates
   - REQUIRE all PASS

6. User HUMAN-CHECKLIST gate (perceptual)
7. User MANUAL publish (anti-ban)
```

---

## 🔴 Blockers list (current state — updated as gates pass)

```
[ ] Script A built + tested (10/10 + adversarial)
[ ] Script B built + V3 adversarial KNOWN bugs detected
[ ] Script C built + adversarial all PASS
[ ] ARCHITECTURAL-DECISIONS.md present
[ ] CLAUDE.md Hard Rules #24 + #25 active
[ ] AUDITOR-PROTOCOL anti-patterns #15 + #16 active
[ ] PIPELINE.md § 13.9 explicit + scripts marked BLOCKER
[ ] BOOTSTRAP.md amended
[ ] CONTRACT-A-B-INTERFACE.md present (signed)
[ ] CREATIVE-SPEC-TEMPLATE-v11.yaml exists
[ ] V3 archived cleanly
[ ] Auditor commitment confirmed
```

When ALL boxes checked → V4 READY. Until then → V4 BLOCKED.

---

## ⚠️ Bypass discipline

```
NO V4 launch via:
  ✗ Manual agent spawning bypassing orchestrator
  ✗ "Just this once" exceptions
  ✗ Skipping any pre-launch gate
  ✗ Engineer multi-CP prompts
  ✗ Auditor self-verifying engineer self-audit (anti-pattern #8)

ALL bypasses MUST be:
  - Logged to ARCHITECTURAL-DECISIONS.md
  - Justified with explicit reason ≥10 chars
  - Reviewed in next system retrospective
```
