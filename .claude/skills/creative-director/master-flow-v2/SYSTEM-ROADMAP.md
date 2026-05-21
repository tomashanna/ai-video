# SYSTEM ROADMAP — end-to-end flow + agents + Gemini integration + layer architecture

> **Audience**: tu equipo (creator team) — onboarding rápido al sistema multi-agent video production.
> **Purpose**: enable visualization of how the system actually works → identify improvements + redundancies pre-investment.
> **Output**: this doc (structured markdown) + Excalidraw-ready diagram spec § 11.
> **Last validated**: 2026-05-21 post Phase 2 architectural refactor COMPLETE (per-clip atomic + Quality Gate Agent + effects library).
> **Previous milestone**: 2026-05-19 matadero v1 FINAL ship (8-iter campaign, 22 gaps codified) + 2026-05-20 cinema-abandonado v2 (6-iter, 11 NEW gaps).

---

## 1. Executive summary (1-min read)

```
SISTEMA = 3 LLM agents + 1 automated agent + 1 user + 5 niveles de docs
GOAL    = Producir videos horror-choice ≥9.7 Gemini + ≥85% empirical audit automatizado
TOOLS   = ElevenLabs (audio) + Replicate Hailuo (video) + Gemini Vision (audit + image)
          + HyperFrames (compose) + Whisper (transcribe) + ffmpeg (everything)

3 LLM AGENTS:
  🏛️ ARCHITECT (terminal 2)  — DESIGNS what + story + characters + script + intent
  🛠️ ENGINEER (terminal 1)   — EXECUTES the SPEC: assets gen + audio + compose + render
  🔍 AUDITOR (terminal 3)    — VERIFIES handoffs independently against canonical authority

⭐ 1 AUTOMATED AGENT (Phase 2 NEW 2026-05-20):
  🤖 QUALITY GATE AGENT      — Per-clip automated QA (Gemini Vision + sentinels + verdict)
                              Runs PER ATOMIC CLIP before assembly. Catches bugs at granular
                              level vs current "auditor reviews POST-render"

1 USER (👤): perceptual ground truth (Rule D PRECEDENCE) + final PUBLISH approval

5 LAYERS:
  NIVEL 0 — Universal AI principles (Hard Rules CLAUDE.md, now 23 rules)
  NIVEL 1 — Multi-agent protocols (TEAM + AUDITOR + HANDOFF)
  NIVEL 2 — Video production universal (ai-video-production/* + Phase 2 scripts + effects-library)
  NIVEL 3 — Format-specific (horror-choice-format/* PAUTA + INGENIERO-PAUTA)
  NIVEL 4 — Per-video SPEC (creative-specs/<id>.yaml)

ITER PATTERN:
  Architect SPEC → Engineer execute PER CLIP → Quality Gate per-clip verdict →
  Auditor cross-verify → User perceptual → PUBLISH
  (loop ≥9.7 Gemini + audit-against-ref + user approval)
```

**Milestones**:
- **2026-05-19 matadero v1** — first video shipped (8 iter, 22 gaps codified)
- **2026-05-20 cinema-abandonado v2** — 2nd video (6 iter = -25%, $14.29 vs $15.56)
- **2026-05-20 Phase 2 refactor COMPLETE** — per-clip atomic assembly + Quality Gate Agent + mid-exec Gemini Vision + 10-transition effects library. Eliminates 7/8 recurring bug classes structurally. MANDATORY video #3+ per Hard Rule #23.
- **Forward video #3 estimate**: 1-3 iter, ~$15-16 budget, lip-sync precision = only remaining bug class (Phase 3 Hedra deferred).

---

## 2. Architecture overview

### 2.1 Three-agent separation of concerns

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   👤 USER (creator)                                                 │
│   • Concept / story / pattern preference                            │
│   • Perceptual ground truth (Rule D PRECEDENCE)                     │
│   • Final PUBLISH approval                                          │
│                                                                     │
└──────────────────────┬──────────────────────────────────────────────┘
                       │ Requirements
                       │ Feedback (perceptual)
                       │ PUBLISH vote
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   🏛️ ARCHITECT (terminal 2)        CREATIVE intent owner            │
│   ──────────────────────────────────────────────────                │
│   • User interview → SPEC.yaml                                      │
│   • Pattern selection (P1-P10 horror-choice)                        │
│   • Story + characters + script + visual intent                     │
│   • Canonical compliance verdicts                                   │
│   • Track parallel codifications (PAUTA + INGENIERO-PAUTA + SPEC)  │
│   • In-SPEC annotations forward-tracking                            │
│                                                                     │
│   Output: creative-specs/<id>.yaml                                  │
│           + amendments to canonical authority docs                  │
│                                                                     │
└──────────────────────┬──────────────────────────────────────────────┘
                       │ SPEC handoff
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   🛠️ ENGINEER (terminal 1)         EXECUTION owner                  │
│   ──────────────────────────────────────────────────                │
│   • CP1 Anchor generation (Gemini API image)                        │
│   • CP2 TTS (ElevenLabs) + Whisper captions                         │
│   • CP3 Shot images (Gemini API)                                    │
│   • CP4 Animation (Hailuo / Kling / Seedance via Replicate)        │
│   • CP5 Composition + render (HyperFrames + ffmpeg)                │
│   • Self-audits before each handoff                                 │
│                                                                     │
│   Output: assets/ + index.html + renders/draft.mp4                  │
│           + CP[N]-handoff.md per checkpoint                         │
│                                                                     │
└──────────────────────┬──────────────────────────────────────────────┘
                       │ Handoff via filesystem
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   🔍 AUDITOR (terminal 3)          VERIFICATION owner               │
│   ──────────────────────────────────────────────────                │
│   • Read fuentes primarias DIRECT (NO trust intermediate docs)     │
│   • Verify engineer claims via independent measurement              │
│   • Cross-validate architect verdicts against canonical refs        │
│   • Run audit scripts (6 gates + S1-S6 sentinels)                  │
│   • Issue verdict (🟢/🟡/🔴/⛔) per CP                              │
│   • Codify gaps detected → GAPS-LOG anti-recurrencia                │
│                                                                     │
│   Output: tabla findings + verdict per CP                           │
│           + GAPS-LOG.md updates                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Why 3 LLM agents (+ 1 automated) — evolution timeline

**Before 2026-05-17**: 2-role system (architect + engineer). Risk: engineer self-audit + Gemini holistic scores inflated (matadero CP5 v1 = 9.0 holistic con 0/10 SFX wired = critical gap missed).

**Post 2026-05-17**: AUDITOR added as 3rd independent role. Verifies engineer claims via DIRECT measurement (not pattern-match labels — anti-pattern #8). User-flagged structural gaps that 2-role system missed get codified into AUDITOR-PROTOCOL forward.

**Validated by matadero**: 8 iter campaign, 22 gaps codified. Without auditor independent verification, ~12 of those gaps would have shipped undetected.

**Post 2026-05-20 Phase 2**: ⭐ **QUALITY GATE AGENT** added as 4th role (automated, not LLM). Spawned PER CLIP atomic post-build. Runs Gemini Vision + sentinels + caption schema + audio waveform analysis. Returns 🟢/🟡/🔴 verdict per clip BEFORE assembly. If 🔴 → halt + regen ONE clip (NOT full iter cycle).

**Why 4th role exists**:
- Auditor (LLM) reviews POST-render = retroactive (expensive if bug found after full assembly).
- Quality Gate Agent (automated) reviews PER ATOMIC CLIP = preventive (cheap regen one clip).
- Matadero + cinema-abandonado both shipped with bugs auditor only caught POST-render. Phase 2 = catch at clip-build time.

**Cost-benefit Phase 2**: ~$0.10 per clip × 22 clips = $2.20/video Quality Gate cost. Saves $5-15/iter avoided = 100-700% ROI per bug caught early.

### 2.3 Layer architecture (4 niveles)

```
┌─────────────────────────────────────────────────────────────────────┐
│ NIVEL 0 — Universal AI principles                                   │
│   CLAUDE.md (project root)                                          │
│   • Hard Rule #1-#22 (canonical compliance + quality bar + dual gate)│
│   • Bootstrap canonical procedure                                   │
│   • Pre-render gate 7 gates                                         │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ NIVEL 1 — Multi-agent universal protocols                           │
│   .claude/skills/creative-director/                                 │
│   • TEAM-PROTOCOL.md (3-agent coordination)                         │
│   • AUDITOR-PROTOCOL.md (verification independent)                  │
│   • HANDOFF-PROTOCOL.md (CP handoff schema)                         │
│   • master-flow-v2/ (architect + auditor + gaps + this roadmap)    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ NIVEL 2 — Video production universal (format-agnostic)              │
│   .claude/skills/ai-video-production/                               │
│   • BOOTSTRAP.md (new project setup)                                │
│   • PIPELINE.md (CP1-CP5 flow + § 13 NEW per-clip atomic Phase 2)   │
│   • SFX-PIPELINE.md / CAPTIONS.md / AUDIO-MASTERING.md / etc.       │
│   • templates/scripts/* (13 scripts: 10 audit + 3 Phase 2 NEW)      │
│     ⭐ Phase 2 NEW 2026-05-20:                                       │
│       - build_clip_atomic.py (per-clip mux pipeline)                │
│       - quality_gate_per_clip.py (4th role automated)               │
│       - gemini_midexec_vision.py (4 mid-exec hooks)                 │
│   • templates/avu-library/ (4 AVU pre-rendered clips)               │
│   • templates/effects-library/ ⭐ NEW Phase 2                        │
│     - 10 transitions JSON specs (cross-fade/film-burn/glitch/etc)   │
│     - caption-burn-template.css (3 canonical classes)               │
│     - 3 audio stings (whoosh + drone + projector-cue)               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ NIVEL 3 — Format-specific (per-genre)                               │
│   .claude/skills/horror-choice-format/                              │
│   • PAUTA-MASTER.md (creative authority — 8 canonical refs)         │
│   • INGENIERO-PAUTA-MASTER.md (technical authority — empirical)     │
│   • canonical-scenes/ref-XX.md (8 documented refs)                  │
│   • video-log.md (cross-video tracking + rotation)                  │
│   • templates/ (NARRATIVE + SFX-LIST per format)                    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│ NIVEL 4 — Per-video SPEC (this specific production)                │
│   creative-specs/<id>.yaml                                          │
│   • shot_list (22+ shots)                                           │
│   • narration_script (segments + speakers + timings)                │
│   • asset_list (SFX/music/ambient/clips/UI elements)                │
│   • hook_sub_beats / decision_sub_beats schema v8                   │
│   • In-SPEC annotations per-iter                                    │
└─────────────────────────────────────────────────────────────────────┘
```

**Reglas oro**:
- Modificar NIVEL 0/1 sirve a TODOS los videos forever
- Modificar NIVEL 2 sirve a TODOS los videos forever
- Modificar NIVEL 3 sirve a TODOS los videos del formato
- Modificar NIVEL 4 sirve solo a este video (desechable)

**Si dudás dónde codificar algo**: empezá NIVEL 4 (project local), promote a NIVEL 3 cuando segundo video del formato lo necesita, promote a NIVEL 2 cuando cross-format need observed.

---

## 3. End-to-end flow per video (CP1 → CP5 → PUBLISH)

### 3.1 Flow visual

```
START
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 0 — Pre-production (user + architect)                     │
│ ──────────────────────────────────────────                      │
│ 1. User concept input (pattern P1-P10 + setting + dyad)        │
│ 2. Architect interview FASE 0 inputs                           │
│ 3. Architect SPEC.yaml v8 schema                               │
│ 4. Auditor SPEC audit vs PAUTA + INGENIERO-PAUTA               │
│ 5. User approves SPEC                                          │
└─────────────────────────────────────────────────────────────────┘
  │ SPEC handoff
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CP1 — Reference Anchors (engineer)                              │
│ ──────────────────────────────────────────                      │
│ • Generate 8 anchor images (Gemini Pro 3.1 typically)          │
│ • Character anchors (dyad: malo + bueno aparente)              │
│ • Setting anchors (4)                                          │
│ • Prop anchors (2)                                             │
│ • Engineer self-audit + emit CP1-handoff.md                    │
│                                                                 │
│ Audits:                                                         │
│ • 🏛️ Architect approval gate creativo (consistency)            │
│ • 🔍 Auditor § 3 CP1 audit (D1-D8 SPEC compliance)              │
│                                                                 │
│ 🤖 Gemini: Image gen API (Gemini 3.1 Pro)                       │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CP2 — Script + TTS + Captions (engineer)                        │
│ ──────────────────────────────────────────                      │
│ • Generate 19+ TTS segments (ElevenLabs canonical voice)       │
│ • Whisper transcribe → captions.json                           │
│ • 3-class system (name_labels / narration / warning_red)       │
│ • Apply atempo 2.0x canonical (NEVER per-segment over-tempo)   │
│ • Engineer self-audit + emit CP2-handoff.md                    │
│                                                                 │
│ Audits:                                                         │
│ • 🔍 Auditor § 3 CP2 M7 acoustic verify (BLOQUEANTE):           │
│   - M7.1-M7.6 pace WPM canonical band [152-180]                │
│   - M7.6.5 NEW per-segment WPM check (GAP #21)                 │
│   - M7.7 audibility + intelligibility (Whisper re-transcribe)  │
│   - M7.7.5 semantic equivalence rules                          │
│                                                                 │
│ 🤖 Gemini: NOT used (Whisper + librosa only)                    │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CP3 — Shot Images (engineer)                                    │
│ ──────────────────────────────────────────                      │
│ • Generate 22 shot images (Gemini Pro)                         │
│ • Variants -a/-b/-c shots >4s                                  │
│ • Architect Q-picks composition vs SPEC visual_intent          │
│                                                                 │
│ Audits:                                                         │
│ • 🏛️ Architect approval gate (visual intent compliance)        │
│ • 🔍 Auditor § 3 CP3 audit:                                     │
│   - Character consistency cross-shots                          │
│   - Variantes diversity                                        │
│   - 2.1+2.2 cross-validate variants vs adjacent base shots     │
│   - D29 editorial pacing (decision UI moments)                 │
│                                                                 │
│ 🤖 Gemini: Image gen Pro + Vision audit                         │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CP4 — Animation (engineer)                                      │
│ ──────────────────────────────────────────                      │
│ • Animate 22+ clips via Hailuo / Kling / Seedance              │
│ • Premium prompts 5-block structure (Hard Rule #20)            │
│ • Architect A4 manifest schema obligatorio                     │
│ • Dry-run gate (1 shot test pre-batch)                         │
│                                                                 │
│ Audits:                                                         │
│ • 🔍 Auditor § 3 CP4 audit:                                     │
│   - 30s rule (animation AI obligatoria)                        │
│   - Premium prompt 5-block                                     │
│   - C-INVENTORY video assets (Gate 0 pre-CP5)                  │
│   - Dry-run gate visual canonical compliance                   │
│                                                                 │
│ 🤖 Gemini: Vision audit single shot pre-batch (dry-run gate)    │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CP5 — Render + Final QA (engineer + auditor + architect)        │
│ ──────────────────────────────────────────                      │
│ • Audio assets gen (SFX + music + ambient via ElevenLabs)      │
│ • UI elements wire (countdown AVU + buttons + loading)         │
│ • HyperFrames composition + ffmpeg render                      │
│ • 8 gates pre-render obligatorios                              │
│                                                                 │
│ 8 Gates pre-render:                                             │
│ • Gate 0: audit-spec-completeness.py (inventory diff)          │
│ • Gate 1: hyperframes lint                                     │
│ • Gate 2: audit-narrative.py (z-index/orphans)                 │
│ • Gate 3: render-lock.py (coordination)                        │
│ • Gate 4: audit-frames.py (Gemini Vision frame-by-frame)       │
│ • Gate 5: audit-frames-granular.py (S1-S6 sentinels NEW)       │
│ • Gate 6: audit-audio.py (coverage + LUFS + gaps)              │
│ • Gate 7: qa-gate.py (dual gate score check)                   │
│                                                                 │
│ Plus auditor § 3 CP5 step 9 C-INVENTORY-WIRED (BLOQUEANTE)     │
│ Plus auditor § 3 CP5 step 10 D29 editorial pacing audit         │
│                                                                 │
│ Dual quality gate (Hard Rule #1):                              │
│ (a) Gemini holistic 14-dim ≥9.7                                │
│ (b) audit-against-referent.py ≥85% metrics canonical band     │
│                                                                 │
│ 🤖 Gemini: Vision frame-by-frame + holistic 14-dim scoring     │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ POST-RENDER USER GATE                                           │
│ ──────────────────────────────────────────                      │
│ • User HUMAN-CHECKLIST 7 Q gestalt review                      │
│ • Perceptual sanity check (Rule D PRECEDENCE)                  │
│ • Vote PUBLISH / ITER N+1 / REJECT                             │
└─────────────────────────────────────────────────────────────────┘
  │
  ├─ PUBLISH → 🎉 Instagram upload @elige_tucompanero
  │
  └─ ITER → loop back to relevant CP (engineer fixes)
```

### 3.2 Iteration loop pattern

```
Per iter:
  Engineer execute fix → Engineer self-audit → Emit handoff
                                                    │
                                                    ▼
  Auditor independent verify → Issue verdict
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
          🟢 GO                🟡 NB                 🔴 NO-GO
          incondicional        condicional           bloqueante
              │                     │                     │
              │                     ▼                     ▼
              │              Engineer fix          ESCALATE
              │              + re-emit             user / architect
              │                                          │
              │                                          ▼
              │                                   New iter OR re-spec
              │
              ▼
          User HUMAN-CHECKLIST
              │
              ▼
          PUBLISH ✅
```

**Iter cap protocol**: engineer iter cap=2 default per overnight authorization. User explicit waiver per iter required for iter ≥3. Matadero used 8 iter via user authorizations.

---

## 4. Gemini integration map (PER phase + verdict)

### 4.1 Gemini touch points complete inventory

| Phase | Tool | Owner | Purpose | Verdict semantics |
|-------|------|-------|---------|-------------------|
| **CP1 anchors** | Gemini Pro image API | Engineer | Generate 8 reference anchors | Visual quality assessment via direct image gen |
| **CP1 audit** | Gemini Vision | Auditor (manual) | Verify anchors match SPEC.visual_anchor_prompt | ✅ matches OR 🔴 prompt drift |
| **CP3 shots** | Gemini Pro image API | Engineer | Generate 22 shot images | Direct gen quality |
| **CP3 audit** | Gemini Vision | Auditor (manual) | Verify shots match SPEC.visual_intent + character consistency | ✅/🔴 per shot |
| **CP4 dry-run** | Gemini Vision | Engineer | Single shot test pre-batch (canonical compliance ≥10/10 items) | 🟢 batch GO / 🔴 escalate |
| **CP5 audit-frames** | Gemini Vision | Engineer + Auditor | Frame-by-frame interval 1.0s (89 frames per 89s video) | Issues per timestamp |
| **CP5 audit-frames-granular Tier 2** | Gemini Vision (FORWARD) | Engineer + Auditor | Per 0.5s frame text dedup + character visibility (S1+S6 enhanced) | Sentinel patterns automated |
| **CP5 holistic 14-dim** | Gemini Pro descriptive | Engineer + Auditor | Final qualitative scoring 14 dimensions | ≥9.7 gate (a) PASS dual gate |
| **CP5 auditor cross-validate** | Gemini Vision (independent query) | Auditor | Cross-check engineer's claims (anti-pattern #8 verification) | Concur OR flag false-positive |

**Plus Gemini API for content generation**:
- Image generation: anchors + shots (Gemini Pro 3.1)
- Vision audit: frame analysis (Gemini Pro descriptive)
- NOT Gemini: TTS (ElevenLabs), animation (Hailuo via Replicate), transcription (Whisper local)

### 4.2 Critical Gemini decision points

```
Decision tree per CP audit:

1. Engineer self-audit (Gemini Vision OR holistic)
   ↓
2. Engineer report metrics/claims
   ↓
3. 🚨 ANTI-PATTERN #8: Auditor MUST NOT trust engineer label
   ↓
4. Auditor INDEPENDENT Gemini query (cross-validate)
   ↓
5. Compare engineer claim vs auditor independent finding
   ↓
6. If divergence → 🔴 FAIL bloqueante, escalate
   If convergence → ✅ PASS (with NB if marginal)
```

**Matadero example**: engineer iter 5 reported "AVU validated 10/10 Dim 12". Auditor independent Gemini query confirmed (no divergence). ✓ PASS.

**Counter-example**: engineer iter 7 reported "narrator pace canonical 178 WPM avg". Auditor PER-SEGMENT check via GAP #21 codification revealed caption[2] = 236 WPM outlier. Engineer overall avg PASSED but per-segment FAILED. Auditor caught what engineer missed.

### 4.3 Gemini limitations + workarounds

| Limitation | Workaround | Status |
|------------|------------|--------|
| LLM cannot watch mp4 directly | Extract frames via ffmpeg → Gemini Vision per frame | ✅ Current |
| Holistic 14-dim subjective drift | Dual gate: Gemini + audit-against-referent metrics | ✅ Hard Rule #1 |
| Per-frame analysis interval 1.0s misses 0.5s events | audit-frames-granular Gate 5 (0.5s first 30s) | ✅ Phase 0 done |
| Gemini doesn't measure timing precisely | ffmpeg + Whisper + librosa local measurement | ✅ Phase 1 forward |
| Gemini false-positive bias (Dim 12 captions Y58 vs canonical Y62) | Hard Rule #4 empirical canonical wins + architect reject | ✅ Matadero F15 |
| Gemini inflated scores when atmosphere strong | dual gate audit-against-referent prevents | ✅ Hard Rule #1 |

---

## 5. Ownership matrix (who does what per stage)

### 5.1 Decision authority matrix

| Decision | 👤 User | 🏛️ Arch | 🛠️ Eng | 🔍 Aud | Notes |
|----------|---------|---------|---------|---------|-------|
| Pattern P1-P10 choice | ✅ FINAL | Recommend | — | Verify rotation | video-log.md tracking |
| Setting + dyad concept | ✅ FINAL | Refine via interview | — | — | — |
| Script text / narrator lines | — | ✅ AUTHOR | Generate TTS | Verify pace canonical | — |
| Visual style (filter / color grade) | — | ✅ INTENT | Implement | Verify vs canonical | — |
| Specific timestamps / timing | — | Intent | ✅ OPERATIONAL | Verify cascade integrity | GAP #22 lesson |
| Model selection (Hailuo / Kling) | — | Recommend | ✅ TIER decision | Verify quality | MODEL-BENCHMARK.md |
| SPEC schema amendments | — | ✅ OWNER | — | Verify consistency | Track parallel |
| PAUTA-MASTER amendments | — | ✅ OWNER | — | Verify empirical evidence | — |
| INGENIERO-PAUTA amendments | — | ✅ OWNER | Propose technical | Verify implementation feasibility | — |
| Audit verdicts per CP | — | Creative-domain verdicts | Self-audit | ✅ INDEPENDENT verdict | — |
| Iter scope per fix | Authorize iter ≥3 | — | ✅ Propose engineer-fixable | Recommend path | — |
| Architect-domain residuals (cuts/coverage/Gemini false-positive) | Optional vote | ✅ FINAL | — | Verify rationale empirical | F13/F14/F15 |
| Quality gate (a) Gemini ≥9.7 | — | — | Self-report | ✅ Cross-validate independent | — |
| Quality gate (b) audit-against-ref ≥85% | — | — | Auto script | ✅ Verify metrics canonical | — |
| **PUBLISH approval** | ✅ **FINAL** | — | — | Recommend ship-ready | Rule D PRECEDENCE |
| Forward Phase 1 priorities | Approve | Recommend | Build | Recommend | — |
| New format template (tutorial/B2B) | ✅ FINAL | Create new PAUTA pair | Build templates | Verify cross-template | — |

### 5.2 Communication channels

```
USER ↔ ARCHITECT      : Direct chat in terminal 2 (concept + interview + feedback)
USER ↔ ENGINEER        : Direct chat in terminal 1 (status + iter approvals)
USER ↔ AUDITOR         : Direct chat in terminal 3 (audit results + verdicts)

ARCHITECT ↔ ENGINEER   : Filesystem (creative-specs/<id>.yaml)
                         + USER bridge (paste-paste prompts)

ENGINEER ↔ AUDITOR     : Filesystem (CP[N]-handoff.md)
                         + USER bridge

ARCHITECT ↔ AUDITOR    : Filesystem (Track commits + amendments)
                         + USER bridge

ALL agents ↔ SHARED   : 
  • GAPS-LOG.md (cross-agent gap tracking)
  • active_session_state.md (memory snapshot)
  • PAUTA-MASTER + INGENIERO-PAUTA (canonical authority)
```

**No agent-to-agent direct communication** — all via filesystem OR user paste-bridge. This is structural (each agent in own terminal = fresh context = independence of judgment preserved).

---

## 6. Anti-pattern detection points

### 6.1 Anti-patterns codified AUDITOR-PROTOCOL § 6 (10 total)

| # | Anti-pattern | Detection point | Sentinel |
|---|--------------|-----------------|----------|
| 1 | Delegar verificación al self-audit | All audits | Manual check direct |
| 2 | Confiar citaciones del handoff sin leer fuente | All audits | Direct read |
| 3 | Audit superficial cuando cambios mayores | CP3/CP5 | Full SPEC re-read |
| 4 | Maquillar findings para acelerar GO | All audits | Honest table |
| 5 | Compartir contexto arq/ing | All terminals | Fresh context per role |
| 6 | Inventar findings sin authority quote | All audits | Mandatory line cite |
| 7 | Cerrar audit sin responder Q1-QN explícitas | All audits | Q&A protocol |
| **8** | **Pattern-match label engineer sin medir directo** | CP4-CP5 | Direct ffmpeg/ls verify (matadero GAP #13) |
| **9** | **Audio-visual lip-sync realism violations** | CP5 character speech | Frame extract at character-silent moments (matadero GAP #9) |
| **10** | **Trust docs canonical-scenes sin direct frame verification** | All canonical pattern verification | Extract source video frames directly (matadero GAP #20) |

### 6.2 Sentinel patterns automated (audit-frames-granular.py)

```
Gate 5 — audit-frames-granular.py sentinels:

S1. Audio-visual character mismatch
    "if speaker=character + character.face_visible == false → 🚨 FLAG"
    Status: WARN (needs character_visible_config OR Gemini Vision Tier 2)

S2. Duplicate text within window (10s)
    "if same text in 2+ HTML elements within 10s → 🚨 FLAG"
    Status: FAIL detection (cross-type captions vs outro_cards + stale HTML elements)

S3. AVU sync drift (FORWARD)
    "if AVU bundled audio peaks != expected timing → 🚨 FLAG"
    Status: ⏸ pending Phase 1

S4. Caption Y position canonical
    "if caption Y outside [55-70%] band → 🚨 FLAG"
    Status: WARN

S5. Watermark IG safe zone
    "if watermark Y > 1700px → 🚨 FLAG (close to IG UI)"
    Status: WARN

S6. Countdown digit transition timing
    "if GSAP tl.call() timestamps not staggered ≥0.5s → 🚨 FAIL"
    Status: FAIL detection (matadero GAP #22 — added 2026-05-19)

S7. Watermark text canonical (FORWARD)
    "if watermark text != @elige_tucompanero → 🚨 FAIL"
    Status: ⏸ pending implementation (matadero ship caught manually)
```

---

## 7. Decision matrix + verdict semantics

### 7.1 Verdict states (universal)

```
🟢 GO incondicional        — ship-ready, no blockers
🟡 GO conditional          — minor fixes engineer-iterable, ship after iter
🔴 NO-GO                   — bloqueante, must fix before next iter
⛔ ESCALATE                — escalate to user (over iter cap OR architect-domain)
```

### 7.2 Dual quality gate (Hard Rule #1)

```
Gate (a): Gemini holistic 14-dim ≥9.7
   PASS → continue
   FAIL → iter A→B→C engineer fixes
   3x FAIL → ESCALATE user

Gate (b): audit-against-referent.py ≥85% metrics canonical band
   PASS → continue
   FAIL → architect verdict residuals (accept signature OR amend)
   Both gates FAIL → STOP + escalate

Plus user perceptual ground truth (Rule D PRECEDENCE):
   Override any gate when user-perception conflicts
```

### 7.3 Path matrix (engineer fixes)

```
Path A: iter retry (engineer-domain fixes)
   - Most fixes (caption text, mix levels, GSAP timing, etc.)
   - Iter cap=2 default per overnight auth
   
Path B: engineer bypass (accept current as-is)
   - REJECT default — bypass erases architect intent
   - User explicit waiver required

Path B-extension: architect SPEC amendment post-escalate
   - Architect amends SPEC with canonical rationale
   - Engineer execute under new SPEC
   
Path C: alternative tool / approach
   - When current approach hits ceiling (Hailuo Std weakness, etc.)
   - Engineer + architect collaborate
   
Path D: full sprint (Phase A→E)
   - When multiple structural gaps detected
   - User authorization required
   
Path E: re-spec / re-render with corrected values
   - Post Phase 1 measurement scripts
   - Flip pending → validated
```

---

## 8. Iteration trajectory + convergence

### 8.1 Matadero v1 trajectory (validated)

```
Iter 1: 40% sistema / 60% user-in-loop  (initial autonomous)
Iter 2: 50% / 50%                       (Path D Phase A→E)
Iter 3: 65% / 35%                       (engineer-domain fixes)
Iter 4: 75% / 25%                       (editorial pacing tripartita)
Iter 5: 85% / 15%                       (AVU pilot)
Iter 6: 95% / 5%                        (Gemini 10/10 first time)
Iter 7: 95% / 5%                        (per-segment WPM fix)
Iter 8: 98% / 2%                        (GAP #22 staggered fix + S6 sentinel)
```

### 8.2 Forward convergence estimate

```
Video #2 horror-choice  (heredando 22 gaps):     92-95% start / 1-2 iter
Video #3                (heredando 25+ gaps):    95-97% start / 1 iter
Video #5+               (heredando 30+ gaps):    97-98% asymptotic / 1 iter
Video #1 nuevo formato  (NIVEL 1+2 only):       80% start / 2-3 iter (partial reset)
```

### 8.3 Driver of convergence

Cada feedback humano = gap codificado = system protection forward. Each video produced = system gets structurally smarter, NOT just better at this specific video.

---

## 9. Forward improvements + redundancies (opportunities)

### 9.1 Redundancies identified

| Redundancy | Current state | Optimization opportunity |
|------------|---------------|--------------------------|
| Engineer self-audit + Auditor independent audit | Both run Gemini holistic | Consolidate Tier 2 audit-frames-granular handle both |
| canonical-scenes/ref-XX.md sampled every 5s + manual frame review | Two parallel sources | Phase 1 `extract-canonical-max-detail.py` regenerate at 0.5s granularity (single source) |
| HTML+GSAP countdown D1/D2 + AVU library | Two patterns for same element | Migrate D1/D2 to AVU (1 pattern universal) |
| audit-frames.py (interval 1s) + audit-frames-granular.py (0.5s) | Two scripts | audit-frames-granular Tier 2 subsumes audit-frames |
| Multiple architect-domain residuals (cuts/coverage/Gemini false-positive) | Manual verdicts per video | Codify standard "ref-13 signature accepted" templates |

### 9.2 Improvements priorities (next sprint candidates)

| Priority | Improvement | Effort | Impact |
|----------|-------------|--------|--------|
| ⭐ HIGH | Build remaining 3 AVUs (decision-freeze + hook-transition + outro-card) | ~$1.00 + 4-6h | Eliminate GAP #22 class entirely + universal cross-template |
| ⭐ HIGH | audit-frames-granular Tier 2 (Gemini Vision per-frame text dedup) | 4-6h + $0.30/run | Auto-catch D1/D2-style render-time visual issues |
| ⭐ HIGH | measure-canonical-decision-ui-pacing.py | 8h | Flip pending → validated canonical_validation_status × 6 amendments |
| MEDIUM | extract-canonical-max-detail.py | 6h | Regenerate canonical-scenes MAX DETAIL anti-recurrencia GAP #20 |
| MEDIUM | measure-canonical-audio-cue-levels.py | 4h | Empirical SFX mix bands canonical (GAP #17) |
| MEDIUM | character_visible_config schema + Gemini Vision S1 sentinel | 6h | Auto-catch anti-pattern #9 hidden form |
| LOW | Phase 5 orchestrator (auto-coordinate 3 agents) | TBD | Reduce user-in-loop to perceptual review only |

### 9.3 Team adoption recommendations

**For creator (user)**:
- Use this roadmap as onboarding doc para team
- Each video produced reinforces system maturity
- Pattern rotation tracking via video-log.md OBLIGATORIO

**For engineering team**:
- Bootstrap canonical procedure (CLAUDE.md L196-229) for new projects
- Audit-spec-completeness Gate 0 BLOQUEANTE pre-everything
- audit-frames-granular Gate 5 auto-detect bug classes

**For creative team**:
- PAUTA-MASTER + INGENIERO-PAUTA = empirical authority (NOT our productions)
- canonical-scenes ref-XX docs = pattern reference
- video-log.md rotation tracking before pattern selection

---

## 10. Glossary (key terms)

| Term | Meaning |
|------|---------|
| **AVU** | Audio-Visual Atomic Unit — pre-rendered .mp4 with audio bundled (eliminates compose-time sync bugs) |
| **CP1-CP5** | Checkpoints in production flow (Anchors / Script / Shots / Animation / Render) |
| **D29** | Decision UI editorial pacing audit step (freeze + filter + countdown sync narration + UI spacing) |
| **Dual gate** | (a) Gemini holistic ≥9.7 + (b) audit-against-referent ≥85% — BOTH required |
| **Gate 0-7** | Pre-render bloqueante gates (audit-spec-completeness + lint + audit-narrative + render-lock + audit-frames + audit-frames-granular + audit-audio + qa-gate) |
| **GAP #N** | Tracked gap in GAPS-LOG.md (22 codified post-matadero) |
| **Hard Rule #N** | Canonical compliance rule in CLAUDE.md (22 rules total) |
| **Iter cap** | Default engineer iter limit = 2 per overnight authorization |
| **NIVEL 0-4** | Layer architecture (universal → format → SPEC) |
| **P1-P10** | Pattern matrix horror-choice archetypes (per PAUTA-MASTER § 15) |
| **Path A/B/C/D/E** | Fix path types (iter retry / bypass / alternative / full sprint / re-render) |
| **Rule D PRECEDENCE** | User perceptual ground truth wins over automated metrics |
| **Sentinel S1-S7** | audit-frames-granular auto-detect patterns |

---

## 11. Excalidraw diagram spec (visual elements para tu equipo)

### 11.1 Core diagram — 3 agents + flow

```
Visual elements to draw in Excalidraw:

[3 large rectangles aligned horizontally]:
  🏛️ ARCHITECT (terminal 2)  |  🛠️ ENGINEER (terminal 1)  |  🔍 AUDITOR (terminal 3)
  
  Color coding:
  - Architect: PURPLE (#6B46C1)
  - Engineer:  GREEN  (#10B981)
  - Auditor:   ORANGE (#F59E0B)

[Above all 3]: 👤 USER (rectangle blue #3B82F6)
[Below all 3]: 📁 SHARED FILESYSTEM (rectangle gray #6B7280)

Arrows (bidirectional with labels):
  USER → ARCHITECT: "concept + interview + feedback"
  USER ↔ ENGINEER: "status + iter approvals"
  USER ↔ AUDITOR: "audit results + verdicts"
  
  ARCHITECT → FILESYSTEM: "creative-specs/<id>.yaml"
  ENGINEER → FILESYSTEM: "CP[N]-handoff.md + renders/"
  AUDITOR → FILESYSTEM: "GAPS-LOG.md + verdicts"
  
  Annotation: "No agent-to-agent direct communication"
```

### 11.2 4-layer architecture diagram

```
[4 stacked rectangles vertical]:

┌─────────────────────────────────┐
│ NIVEL 0 — CLAUDE.md             │  RED  (#EF4444)
│ Hard Rules + Bootstrap          │
└─────────────────────────────────┘
         ↓ inherits
┌─────────────────────────────────┐
│ NIVEL 1 — Multi-agent protocols │  ORANGE (#F59E0B)
│ TEAM + AUDITOR + HANDOFF        │
└─────────────────────────────────┘
         ↓ inherits
┌─────────────────────────────────┐
│ NIVEL 2 — Video production      │  YELLOW (#EAB308)
│ ai-video-production scripts     │
└─────────────────────────────────┘
         ↓ inherits
┌─────────────────────────────────┐
│ NIVEL 3 — Format-specific       │  GREEN  (#10B981)
│ horror-choice-format/* (PAUTA)  │
└─────────────────────────────────┘
         ↓ inherits
┌─────────────────────────────────┐
│ NIVEL 4 — Per-video SPEC        │  BLUE  (#3B82F6)
│ creative-specs/<id>.yaml        │
└─────────────────────────────────┘

Annotation right side:
  "Promote bottom-up:
   NIVEL 4 → 3 when 2nd video needs
   NIVEL 3 → 2 when cross-format need
   NIVEL 2 → 1 when multi-agent need
   NIVEL 1 → 0 when universal"
```

### 11.3 End-to-end flow diagram

```
[Horizontal flow with iteration loop]:

START → PHASE 0 → CP1 → CP2 → CP3 → CP4 → CP5 → PUBLISH GATE → 🎉

Below each phase: which agent owns + key outputs

Loop arrow back from each CP audit:
  "If 🔴 NO-GO → loop back to engineer fix"
  "If 🟡 NB → engineer iter + re-audit"
  "If 🟢 GO → continue next CP"

8 Gates labeled in CP5 column:
  Gate 0: audit-spec-completeness
  Gate 1: lint
  ...
  Gate 7: qa-gate

Gemini integration markers (yellow stars ⭐):
  - CP1 (image gen + audit)
  - CP3 (image gen + audit)
  - CP4 dry-run audit
  - CP5 audit-frames + holistic + cross-validate

User perceptual marker (blue 👤):
  - Post-CP5 HUMAN-CHECKLIST
  - PUBLISH approval
```

### 11.4 Gemini integration map diagram

```
[Donut/circular diagram OR flowchart]:

Central node: "GEMINI"

Spokes outward to:
1. "Image gen" → CP1 anchors + CP3 shots
2. "Vision audit (engineer)" → CP4 dry-run + CP5 self-audit
3. "Vision audit (auditor)" → CP1/CP3 manual + CP5 cross-validate
4. "Holistic 14-dim" → CP5 final scoring (gate a)
5. "Granular per-frame Tier 2" → Forward (S1+S6 enhanced)

Each spoke labeled with:
  - Who calls
  - When
  - Verdict semantics
  - Cost estimate
```

### 11.5 Decision matrix flowchart

```
[Decision tree starting from "Audit finding"]:

Audit finding
  ↓
Severity?
  ├─ FAIL bloqueante → 🔴 NO-GO → Engineer fix path
  ├─ NB marginal → 🟡 GO conditional → iter
  └─ PASS → 🟢 GO incondicional → next CP

Engineer fix path:
  ├─ engineer-domain → Path A iter retry
  ├─ architect-domain → ESCALATE to architect
  ├─ tool-ceiling → Path C alternative
  └─ multi-structural → Path D full sprint
```

### 11.6 Suggested Excalidraw export format

For your team — export diagrams as:
- **SVG**: for documentation embeds + scalable
- **PNG 1200×800**: for slides/wiki
- **Excalidraw .excalidraw JSON**: editable forward

Tools to use:
- excalidraw.com (free + open source)
- excalidraw VS Code extension
- Plus annotations + groupings for sub-sections

---

### 11.7 ⭐ Per-clip atomic assembly diagram (Phase 2 — 2026-05-20)

**Purpose**: visualize how Phase 2 architecture eliminates 7/8 recurring edit bug classes structurally. This diagram is the **key value-add** for video #3+ ship quality vs matadero/cinema legacy.

```
═══════════════════════════════════════════════════════════════════════════
LEGACY PIPELINE (matadero + cinema-abandonado) — BUG-PRONE
═══════════════════════════════════════════════════════════════════════════

[Horizontal flow, RED arrows showing where bugs accumulate]

  Clip_01.mp4 ─┐
  Clip_02.mp4 ─┤
  Clip_03.mp4 ─┤───► ffmpeg concat ────► [global master.mp3 90s+] ──┐
  ...          ─┤                              ↑                     │
  Clip_22.mp4 ─┘                              [TTS + SFX + music]    │
                                               [mixed cumulatively]   ▼
                                                              ┌──────────────┐
                                                              │ Final render │
                                                              └──────┬───────┘
                                                                     │
                                                                     ▼
                                                          🔴 BUG-PRONE OUTPUT:
                                                            ├ End-of-timeline drift
                                                            ├ Caption fragments
                                                            ├ Same-Y overlap
                                                            ├ Audio/clip mismatch
                                                            ├ SFX context-blind
                                                            ├ AVU GSAP offsets
                                                            └ Cumulative timeline error

  Bug detection: ONLY post-render Gemini audit (retroactive).
  Cost to fix: $5-15/iter cycle (full re-render).


═══════════════════════════════════════════════════════════════════════════
PHASE 2 PIPELINE (mandatory video #3+) — STRUCTURALLY EXEMPT
═══════════════════════════════════════════════════════════════════════════

[Vertical flow, GREEN per-clip atomic units]

  FOR EACH SHOT_NN:
  ┌─────────────────────────────────────────────────────────────────┐
  │  1. Hailuo animate → shot_NN.mp4 (visual only)                  │
  │                                                                 │
  │  2. ⚡ GEMINI VISION hook (mid-execution)                       │
  │     • Verify visual matches SPEC scene_context                  │
  │     • Score: visual_match, character_consistency,               │
  │       atmospheric_motions, composition, literal_action_match    │
  │     • If <7 → flag regen ONE shot ($0.27 vs full iter)          │
  │                                                                 │
  │  3. build_clip_atomic.py:                                       │
  │     ├ TTS narration for THIS window                             │
  │     ├ SFX events for this shot                                  │
  │     ├ Local ambient slice                                       │
  │     ├ Optional AVU overlay (countdown/decision-freeze/outro)    │
  │     ├ ffmpeg mux audio + video → shot_NN_atomic.mp4             │
  │     └ Caption sidecar JSON (scope-limited)                      │
  │                                                                 │
  │  4. ⭐ QUALITY GATE AGENT (4th role automated):                 │
  │     ├ Gemini Vision per-clip (3 frames)                         │
  │     ├ Caption schema validation (no None, no overlap, ≥1.5s)    │
  │     ├ Audio waveform (LUFS ±0.5, no clipping)                   │
  │     ├ Sync verify (Whisper similarity ≥0.6)                     │
  │     ├ Sentinels (S1 ghost-speaker, S2 dup text, S6 AVU)         │
  │     └ Verdict: 🟢 PASS / 🟡 NB / 🔴 FAIL                         │
  │                                                                 │
  │     If 🔴 → halt assembly, regen ONE clip (NOT full iter)       │
  └─────────────────────────────────────────────────────────────────┘
                                  ↓
  ┌─────────────────────────────────────────────────────────────────┐
  │  ASSEMBLY:                                                      │
  │                                                                 │
  │  ffmpeg concat:                                                 │
  │   shot_01_atomic + effect_01 + shot_02_atomic + effect_02 +     │
  │   ... + outro_atomic                                            │
  │                                                                 │
  │  Effects library (10 transitions):                              │
  │   cross-fade-0.5s, hard-cut-whoosh, film-burn, static-noise,    │
  │   black-screen, fade-to-black, light-flash, projector-cue,      │
  │   glitch-transition, cross-fade-1.0s                            │
  │                                                                 │
  │  + cross-clip music continuous layer (separate track)           │
  │  + cross-clip ambient continuous layer (separate track)         │
  │  + color grading LUTs cross-section                             │
  │                                                                 │
  │  ⚡ GEMINI VISION transition_post hook (verify continuity)      │
  └─────────────────────────────────────────────────────────────────┘
                                  ↓
                          ┌──────────────┐
                          │ Final render │
                          └──────┬───────┘
                                 │
                                 ▼
                  🟢 STRUCTURALLY BUG-EXEMPT OUTPUT:
                    ├ Per-clip sync verified independent
                    ├ Captions scope-limited per clip (no fragmentation)
                    ├ Audio mux atomic (no drift)
                    ├ SFX explicit per shot (no context blindness)
                    ├ AVU bundled atomic (no GSAP cross-clip offset)
                    ├ Quality Gate Agent verdict per-clip pre-assembly
                    └ Mid-exec Gemini catches regen-able bugs early

  Bug detection: PER-CLIP atomic + transition_post + post-render.
  Cost: $2.20/video Gemini Vision integration; regen ONE clip = $0.27 vs $5-15/iter.
```

#### Why per-clip atomic ELIMINATES 7/8 bug classes (structural reasoning)

| Bug class current legacy | Why it happens | Why per-clip eliminates |
|--------------------------|----------------|-------------------------|
| End-of-timeline sync drift | Global master.mp3 = TTS+SFX+music mixed cumulatively across 90s. Each offset compounds. | Per-clip mux = audio scope ends WITH clip. No compounding across timeline. |
| Caption fragmentation (Whisper over-segment) | Whisper applied to 90s global = 60-70 chunks default. | Per-clip Whisper applied to 4-6s = 2-4 chunks max. Schema validation per clip. |
| Same-Y caption overlap (cross-class) | All captions overlay same Y plane on global timeline. | Per-clip caption sidecar = scope-limited. Validation per clip catches Y overlap immediately. |
| Audio/clip mismatch boundaries | Master.mp3 has TTS at 14.5s. Clip boundary at 14.0s. Mismatch hidden until full render. | Audio bundled WITH visual mux. Boundary IS clip end. Cannot mismatch by construction. |
| SFX context-blind reuse | SFX library global pool, engineer picks without scene context. | Per-clip explicit SFX selection per shot's `who_does_what` context. Reuse DENY list cross-setting. |
| AVU GSAP timing offsets | AVU HTML+GSAP relies on `data-start` timestamps on global timeline. | AVU MP4 bundled atomic in clip mux. No cross-clip GSAP timing dependency. |
| Cumulative timeline error | 90s+ timeline with 22+ shots, 30+ audio events, 20+ captions. Compounding. | Each clip 4-6s scope. No compounding by definition. |

**Only remaining bug class** (1/8): **Lip-sync precision**. Phase 2 cannot fix because Hailuo first-frame conditioning is the source. **Phase 3 forward** (Hedra/Sync.so ~$3/video, user deferred 2026-05-20).

#### Excalidraw diagram spec § 11.7

Visual elements:
- **2 large vertical columns side-by-side**: "LEGACY (red border)" vs "PHASE 2 (green border)"
- **Per clip atomic** depicted as **stacked rounded rectangles** color-coded (visual=blue, audio=orange, captions=yellow, AVU=purple, Quality Gate=green-tick)
- **Effects between clips** depicted as **diamond shapes** between clips (cross-fade icon, whoosh icon, light-flash icon)
- **Cross-clip music layer** depicted as **continuous wavy line** running ACROSS all clips at bottom
- **Gemini Vision hooks** depicted as **yellow stars ⭐** at hailuo_post, tts_post, atomic_post, transition_post positions
- **Quality Gate Agent** depicted as **green checkmark box** AFTER each clip atomic build
- **Bug detection markers**: red ✗ on left column (post-hoc only), green ✓ on right column (per-clip + post-hoc)
- **Cost annotations**: "$5-15/iter" on legacy bugs, "$0.27 regen 1 clip" on Phase 2

Suggested layout:
```
[Title banner top]: "PER-CLIP ATOMIC ASSEMBLY — Phase 2 (2026-05-20)"
[Left column]: LEGACY pipeline (red)
[Right column]: PHASE 2 pipeline (green)
[Bottom annotation table]: 7 bug classes + structural reasoning
```

#### 🆕 Excalidraw § 11.7.b — 3 AUDIO LAYERS diagram (added 2026-05-21 post user Q&A)

> **Gap fill**: Original § 11.7 NO mostraba claramente las 3 capas de audio + cross-clip music workflow + transition_post audio audit. User exposed 3 gaps Q1+Q2+Q3 → esta sub-spec cierra ambigüedad.

Visual elements (separate diagram):

```
[Horizontal flow with 3 stacked audio swimlanes]:

═══════════════════════════════════════════════════════════════════════
TITLE: "AUDIO ARCHITECTURE — 3 layers per scope"
═══════════════════════════════════════════════════════════════════════

[Top row: VISUAL flow]
   clip_01.mp4  ──[effect_01]── clip_02.mp4  ──[effect_02]── clip_03.mp4  ──...
   
[Middle row 1: LAYER 1 AUDIO PER-CLIP (orange, bundled in clip mp4)]
   ┌─────────────┐           ┌─────────────┐           ┌─────────────┐
   │TTS+SFX+AVU  │           │TTS+SFX+AVU  │           │TTS+SFX+AVU  │
   │diegetic     │           │diegetic     │           │diegetic     │
   └─────────────┘           └─────────────┘           └─────────────┘
   [Audit per clip: Quality Gate Agent ✓]

[Middle row 2: LAYER 2 AUDIO EFFECT TRANSITIONS (purple diamond between clips)]
                  ◆whoosh◆                  ◆flash◆
                  in effect mp4              in effect mp4
                  non-diegetic              non-diegetic
   [Audit Q22 NEW: audit-effects-audio.py post-concat ✓]

[Bottom row: LAYER 3 CROSS-CLIP CONTINUOUS (wavy lines running across)]
   ≈≈≈ drone_base 0-88s ≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
        ≈≈≈ accent_drama 50-88s ≈≈≈≈≈≈≈≈
   ~~~ ambient_room 0-88s ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
   [Audit Q23 NEW: audit-music-layers.py post-concat ✓]

[Bottom annotation box]:
   "Scope decision rule:
    • Diegetic (in scene)       → LAYER 1
    • Editorial transition cue  → LAYER 2
    • Global music+ambient      → LAYER 3"

[Side panel — Color coding]:
   • Orange = clip-atomic audio (Layer 1)
   • Purple = effect transition audio (Layer 2)
   • Cyan wave = cross-clip music (Layer 3)
   • Green tick = Quality Gate verdict per-clip
   • Yellow stars ⭐ = Gemini Vision audit hooks

[Side panel — transition_post hook NEW audio dimensions]:
   visual_continuity (existing)
   + audio_continuity (NEW Whisper sliding window)
   + music_layer_continuity (NEW librosa RMS verify)
   + effect_audio_volume_match (NEW ±3dB tolerance)
   + sfx_no_bleed (NEW Layer 1 length matches clip mp4)

[Cost annotation]:
   "+$0.05 per transition × 10 = +$0.50 per video for full audio cross-clip audit"
```

**Suggested layout**: place § 11.7.b diagram BELOW main § 11.7 column comparison. Connects the dots visually for team — they see the per-clip column AND understand how audio layers interact across clips.

#### 🆕 Excalidraw § 11.8 — AUTONOMOUS FACTORY architecture (added 2026-05-21 PM late)

> **Source**: full plan in `<repo-root>/AUTONOMOUS-FACTORY-ROADMAP.md`
> **Status**: AWAITING video #3 validation gate. Build only IF video #3 perceptual ≥9.0.

Visual elements for team Excalidraw:

```
═══════════════════════════════════════════════════════════════════════
TITLE: "AUTONOMOUS VIDEO FACTORY — 3 videos/día con manual publish anti-ban"
═══════════════════════════════════════════════════════════════════════

[Top row: USER DASHBOARD — blue rectangle]
   • Input queue (theme + pattern + setting)
   • Monitor in-flight + costs + scores
   • 3 HUMAN CHECKPOINTS marked with ⭐ stars
   
[Center: ORCHESTRATOR.py — large blue box]
   • Scheduled trigger 3x/día
   • State machine PENDING → SPEC_GEN → CP1-5 → AUDITED → READY
   • Failure recovery patterns
   
[Below orchestrator — 3 agent boxes side-by-side]:
   🏛️ ARCHITECT (purple)     🛠️ ENGINEER (green)     🔍 AUDITOR (orange)
   Claude API + PAUTA         Claude API + Phase 2    Claude API + calib v4
   
[Below agents — 4th automated agent]:
   ⭐ Quality Gate Agent (teal) — per-clip operates autonomously
   
[Below QG agent — model tier]:
   Veo 3.1 (yellow, FREE Gemini API) | Hailuo Replicate (red, $0.27-0.60)
   
[Bottom of pipeline — output queue gray]:
   Filesystem /renders/ready/<video>.mp4
   + caption_draft.txt + hashtags.txt + first_frame.jpg
   
[FINAL stage — USER MANUAL PUBLISH (blue with anti-ban warning)]:
   ⚠️ USER → manually opens IG → posts at organic time
   NEVER programmatic publish — IG ban risk

[Side annotations]:
   • Human checkpoints star markers: SPEC approval, HUMAN-CHECKLIST, publish
   • Cost annotation: $4 per video × 90/mo = $360/mo Replicate
   • Time annotation: 10-15 min user time per video (manual publish included)
   
[Decision gate marker top-right]:
   "Build factory ONLY IF video #3 perceptual ≥9.0
    (validation gate per Phase 4 evolution roadmap)"
```

**Color coding** (consistent with prior diagrams):
- Orchestrator: BLUE (#3B82F6)
- Architect agent: PURPLE (#6B46C1)
- Engineer agent: GREEN (#10B981)
- Auditor agent: ORANGE (#F59E0B)
- Quality Gate Agent: TEAL (#14B8A6) — 4th role
- Veo 3.1: YELLOW (#EAB308) — enterprise FREE
- Hailuo Replicate: RED (#EF4444) — paid
- Filesystem state: GRAY (#6B7280)
- HUMAN CHECKPOINTS: ⭐ STARS with big yellow color
- ANTI-BAN warning on manual publish: RED with caution icon

---

## 12. Quick reference cards

### 12.1 For new agent onboarding

**Architect**:
```
1. Read NIVEL 1 protocols (TEAM + HANDOFF + AUDITOR for context)
2. Read NIVEL 3 PAUTA-MASTER + INGENIERO-PAUTA del formato
3. Read GAPS-LOG (avoid known patterns)
4. Use CREATIVE-SPEC-TEMPLATE v8 schema
5. Cite empirical refs (NOT our productions)
6. Track parallel commits per ChannelTrack
```

**Engineer**:
```
1. Read NIVEL 0 CLAUDE.md Hard Rules (especially #19 #20)
2. Read NIVEL 2 BOOTSTRAP + PIPELINE
3. Read SPEC.yaml + handoff packages
4. Run 8 Gates obligatorios pre-render
5. Emit handoff with engineering-only metrics (NO architect domain)
6. Honest self-report failures (do not maquillar)
```

**Auditor**:
```
1. Read NIVEL 0/1 + NIVEL 3 PAUTA + INGENIERO-PAUTA
2. Read SPEC + engineer handoff
3. Anti-pattern #8: MEDIR directo (NO trust labels)
4. Anti-pattern #10: VERIFY direct frames (NO trust docs)
5. Independent Gemini Vision queries
6. Tabla findings con line citations
7. Verdict per CP + GAPS-LOG update si new gap detected
```

### 12.2 For user

```
Inputs needed per video:
1. Pattern preference (P1-P10) — check video-log.md rotation first
2. Setting concept
3. Character dyad (malo aparente + bueno aparente)
4. Cliffhanger archetype preference
5. Delivery format (default reel 9:16)

Approvals at:
1. SPEC final (Phase 0 closure)
2. Each CP if architect approval gate triggered
3. HUMAN-CHECKLIST post-render
4. PUBLISH (final)
```

---

## 13. Forward evolution roadmap

```
Phase 0 (DONE 2026-05-19): Matadero v1 FINAL ship — 3-agent system validated
Phase 1 (DONE 2026-05-20): Priority scripts + AVU library + Track B canonical bands
Phase 2 (DONE 2026-05-20): ⭐ Per-clip atomic assembly + Quality Gate Agent (4th role) +
                            10-transition effects library + mid-exec Gemini Vision hooks.
                            Eliminates 7/8 recurring bug classes. MANDATORY video #3+.
Phase 3 (DONE 2026-05-21): Calibrated Gemini v4 (mean abs Δ 0.14) + EXECUTION CONTINUITY
                            dimension primary 30% weight + GAP #40 codified + cost model
                            reset Gemini+EL enterprise FREE + Veo 3.1 enterprise validated
                            (4 test bench PASS incl. character speech native lip-sync).
                            Production ready: veo3.py + audit-gemini-calibrated.py.
Phase 4 (NEXT — video #3): First video on full Phase 2 + Phase 3 stack. VALIDATION GATE
                            for autonomous factory greenlight. Required outcomes:
                              - Perceptual ≥9.0
                              - Gemini calibrated v4 ≥9.0
                              - EXECUTION CONTINUITY dim ≥8.5
                              - Iter count ≤3
                              - Cost ≤$9
                            If validated → Phase 5 autonomous factory.
                            If NOT → iterate amendments + retest video #4 manual.
Phase 5 (CONDITIONAL — autonomous factory): Build orchestrator + 3-agent autonomous
                            pipeline + monitoring + manual-publish queue. Goal: 3 videos/día.
                            See AUTONOMOUS-FACTORY-ROADMAP.md for full plan + Excalidraw spec.
                            KEY CONSTRAINT: NEVER auto-publish (IG ban risk). User stays
                            in loop for SPEC approval + HUMAN-CHECKLIST + manual publish.
Phase 6:        Tutorial/B2B/Documentary formats (cross-format validation).
Phase 7:        JSON schemas + machine-readable canonical authority.
Phase 8:        Engagement-loop integration (auto-respond DMs, comment monitoring).
```

---

---

## 14. Premium prompt 5-block structure (Hard Rule #20 expansion)

> **Authority**: `horror-choice-format/INGENIERO-PAUTA-MASTER.md § 5.7` (validated 2026-05-16 caso cabina-14).
> **Owner**: 🛠️ Engineer redacta. 🔍 Auditor audits via SPEC compliance check + visual frame extract verification.
> **Trigger**: cuando engineer usa cheap model (Hailuo Std/Pro, Seedance Lite, Wan-AI) en lugar de hero tier (Kling 2.5 Turbo Pro, Veo 3.1).

### 14.1 Los 5 bloques canonical (orden + propósito)

| # | Bloque | Propósito | Anti-pattern |
|---|--------|-----------|--------------|
| 1 | **Subject + body** | Verbo + objeto + cómo (LITERAL, no abstracto). Lo QUE el personaje hace físicamente | ❌ "Maikol uncanny y siniestro" → ✅ "Maikol gira 90° hacia cámara, sonrisa contenida sin abrir boca" |
| 2 | **Camera direction** | Lens (24mm wide / 50mm normal / 85mm portrait) + Movement (static / push-in slow / dolly left / handheld) + Angle (eye-level / low / Dutch) | ❌ "cinematic shot" → ✅ "50mm portrait lens, slow push-in, eye-level angle" |
| 3 | **Lighting** | Source (window left / overhead flicker / sconce warm) + Temperature (5000K cool / 3200K warm / sodium 2700K) + Intensity (key+fill / silhouette / chiaroscuro) | ❌ "dramatic lighting" → ✅ "single sodium 2700K bulb overhead flickering, chiaroscuro shadows on right cheek" |
| 4 | **Atmosphere VIA physical** | Mood expresado en EXPRESIONES FÍSICAS observables, NO conceptos abstractos | ❌ "sense of dread" → ✅ "breath visible in cold air, slight shiver shoulders, eyes slow-blink wider" |
| 5 | **Style reference** | UNO solo: cinematic / photoreal / painterly / archive footage / VHS degraded | ❌ "horror cinematic dramatic painterly" (multiple) → ✅ "cinematic photoreal" (one + qualifier OK) |

### 14.2 Ejemplo real — matadero v1 shot_01 hook (Hailuo Std + premium prompt)

```
[Block 1 — Subject+body]
Matarife stands frontal facing viewer, motionless arms by sides, slight chest 
breath rise every 2 seconds. Cocinera 2m to his right inclines body slightly 
forward toward viewer, head tilts 5° while breathing normally, eye glow 
intensity pulses subtle warm tungsten.

[Block 2 — Camera direction]
Wide-medium portrait lens 35mm, static framing eye-level, no movement except 
imperceptible parallax background dust particles.

[Block 3 — Lighting]
Cinema matadero overhead fluorescent tubes 5000K cool, flickering once at 
4-second mark. Side fluorescent on left wall casts slight green-cyan tint. 
Cocinera underlit by warm 2700K tungsten from below table (visible heat from 
caldron).

[Block 4 — Atmosphere VIA physical]
Cold breath visible from cocinera mouth subtle, cold air condensation faint on 
matarife cleaver-head surface. Steam rising lazy from caldron toward cocinera 
chin. Hanging meat carcasses sway nearly imperceptible 2cm side-to-side every 
3 seconds.

[Block 5 — Style reference]
Cinematic photoreal, 8K resolution, slight film grain.
```

Cost validation matadero: Hailuo Std @ $0.045/s × 6s = $0.27/clip with premium prompt achieved Gemini Dim 9 audio quality 10/10 — competitivo con Kling Turbo Pro @ $0.07/s × 6s = $0.42/clip (-36% cost).

### 14.3 Ownership matrix per role

| Role | Premium prompt responsibility |
|------|------------------------------|
| 🏛️ **Architect** | Provides SPEC `scene_context.who_does_what` per shot — CRITICAL input. Engineer cannot improvise blocks 1+4 without this. |
| 🛠️ **Engineer** | Authors final premium prompt 5-block. Combines SPEC content + technical params (lens/lighting/style). |
| 🔍 **Auditor** | Verifies engineer prompt contains 5 blocks via grep/structural check. Cross-validates output via frame extract vs SPEC `visual_intent`. |
| 👤 **User** | Approves SPEC pre-CP1 (ensures scene_context complete). Rule D PRECEDENCE override post-render if quality fails. |

### 14.4 Verdict per missing/malformed block

| Block status | Verdict | Action |
|--------------|---------|--------|
| All 5 blocks present + canonical | ✅ PASS | CP3/CP4 proceed |
| 4/5 blocks present (1 missing) | 🟡 NB engineer-fixable | Engineer adds missing + re-gen single shot |
| 3/5 or less blocks | 🔴 NO-GO | Engineer rewrite all prompts + escalate scene_context check |
| Block 1 absent ("subject+body abstract") | 🔴 SHIP-BLOCKING | Cheap model will produce slop. Must rewrite OR upgrade to hero tier model |
| Block 4 abstract instead physical | 🔴 NO-GO | Hard rule #20 violation, root cause cabina-14 case |
| SPEC `scene_context.who_does_what` empty | ⛔ ESCALATE to architect — NO improvise to fill gaps |

---

## 15. MODEL-BENCHMARK key content summary

> **Full doc**: `.claude/skills/video-director/MODEL-BENCHMARK.md` (35 models tracked).
> **Owner**: 🛠️ Engineer consults BEFORE choosing model per shot. Updates when new model emerges OR pricing changes.
> **Recommended refresh**: every 60 days — industry moves weekly.

### 15.1 Defaults recommended per use-case (cheat sheet)

| Use-case | Default model | Cost | Fallback | Razón |
|----------|--------------|------|----------|-------|
| **Hook viral (first 30s Reel)** | Kling 2.5 Turbo Pro | $0.07/s | Seedance 2.0 | Hard rule #6 + leaderboard-validated; narrative control |
| **B-roll / non-hero shots >30s** | Kling 2.5 Turbo Pro | $0.07/s | LTX-2.3 self-host | Coste/calidad sweet spot |
| **Cinematic high-prod long-form** | Veo 3.1 Standard | $0.40/s | Kling 3.0 | Audio nativo + multi-image refs |
| **Multi-shot narrativo character** | Seedance 2.0 + Nano Banana | $0.247/s + $0.04/img | Kling 3.0 Omni | Multi-shot nativo + consistency |
| **Talking head / lip-sync** | Hedra Character-3 | $0.05/s | Sync.so post-process | Especialista 9.5/10 lip-sync |
| **Motion narrativo (walking/grabbing/turning)** | **Hailuo 02** ★ | Std $0.045/s, Pro $0.08/s | Kling Turbo Pro | Validated 2026-05-16 cabina-14 |
| **Cinematic estática c/ character preservation** | Seedance 1 Pro 1080p | $0.12/s | Kling 2.5 | Mejor composition + aesthetic estático |
| **Storyboard/anchor image c/ character** | Gemini Nano Banana | $0.039/img | Seedream / Flux Kontext + PuLID | Multi-image conversation |
| **Title cards con texto legible** | Ideogram 3.0 | $0.075/img | Nano Banana | Tipografía in-image #1 |
| **Horror gore explícito** | Wan 2.7 self-host | GPU cost | Hunyuan 1.5 cozy | Único 100% permisivo |
| **Pose-driven character recurrente** | Wan 2.2 Animate | self-host | — | Skeleton-driven identity lock |

### 15.2 Decision tree per shot (validated N=2 A/B test)

```
⛔ PREREQUISITE INCONDICIONAL:
   Prompt MUST be polished 5-block premium (per § 14). Without it,
   ANY model subperforms. Model decision is SECONDARY to prompt.

Q1: ¿Shot requires MOTION NARRATIVO?
    (walking, running, grabbing, turning, looking, escaping)
    ├─ SÍ → Hailuo 02 ★
    │       budget tight → Standard 768p ($0.045/s)
    │       hero shot   → Pro 1080p ($0.08/s)
    └─ NO → Q2

   ⚠️ HOOK VIRAL OVERRIDE: shot data-start <30s → Kling 2.5 Turbo Pro 
   DEFAULT regardless of motion (hard rule #6).

Q2: ¿Cinematic ESTÁTICA + character preservation?
    (plano fijo con micro-gestos, parallax sutil, no acción)
    ├─ SÍ → Seedance 1 Pro 1080p ($0.12/s) — mejor composition estático
    └─ NO → Q3

Q3: ¿Talking head / lip-sync required?
    ├─ SÍ → Hedra Character-3 ($0.05/s) OR Sync.so post-process
    └─ NO → Q4

Q4: ¿Long-form cinematic (>15s shots) + audio nativo + 9:16?
    ├─ SÍ → Veo 3.1 Standard ($0.40/s)
    └─ NO → Kling 2.5 Turbo Pro fallback (universal default)
```

### 15.3 Caso real matadero v1 — model selection validation

**Matadero used Hailuo 02 Std 768p universal tier para 22 shots** ($0.045/s × 6s minimum = $0.27/clip × 29 clips = $8.39 total).

| Shot type | Why Hailuo Std worked | Where Hailuo Std failed |
|-----------|----------------------|-------------------------|
| Body horror (carcasa mouth opening shot_07 climax) | ✅ Hailuo handles deformation horror efectivo (premium prompt 5-block) | — |
| Decision UI shots (shot_06, shot_13) | ✅ Static dyad + UI overlay, no character motion needed | — |
| Character intro (shot_01 hook) | ✅ Subtle breath motion | ⚠️ Walking gait baseline = "se arrastran" (user catch — GAP #12) |
| Eternal trap multiplication (shot_22) | — | ❌ Hailuo Std doesn't handle "eternal multiplication" motion intent. Static base failed = used variants -a + -c rescue. |

**Conclusion**: Hailuo Std saved $5.62 vs Pro all-shots projection ($14.01 - $8.39 = $5.62). Pro tier reserved for shots Hailuo Std weakness identified (cf GAP #12). Engineer Track B forward: `measure-canonical-motion-velocity.py` to systematize this decision.

### 15.4 Maintenance protocol — cuándo actualizar

```
Trigger update events:
1. New model leaderboard ranking shifts (artificialanalysis.ai monthly check)
2. Pricing change >20% on any default model
3. New model emerges with claimed quality at lower cost (run A/B test before adopting)
4. Existing model shutdown announced (Sora 2 Sep 2026, Imagen 4 Jun 2026)
5. Empirical validation refutes claim (caso Hailuo for horror — was "weakened", validated 2026-05-16)

Update process:
- Update § 3 spec sheet of affected model
- Update § 4 Claim Validation Log (VALIDATED / WEAK / REFUTED status)
- Update § 1.1 cheat sheet if default changes
- Bump "Última actualización" date
- Notify auditor + architect via update log

Update cadence cap: every 60 days minimum review even if no triggers (industry moves weekly).
```

---

## 16. Stack técnico por agente (implementation details)

> Para entender CÓMO está implementado cada agente, no solo qué hace.

### 16.1 🏛️ Architect (terminal 2)

```
LLM client: Claude Code CLI (terminal interactive session)
Model: Claude Opus 4.x (creative reasoning + long context)
Context fresh: NEW terminal session = independent context

Bootstrap files leídos al arrancar (en orden):
1. CLAUDE.md (project root, ALWAYS auto-loaded)
2. .claude/skills/creative-director/SKILL.md
3. .claude/skills/horror-choice-format/PAUTA-MASTER.md
4. .claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md
5. .claude/skills/creative-director/master-flow-v2/ (todos: TEAM-PROTOCOL + ARCHITECT-MASTER-FLOW + AUDITOR-MASTER-FLOW + GAPS-LOG + SYSTEM-ROADMAP)
6. video-log.md (rotation tracking)
7. canonical-scenes/ref-XX.md (cuando comparison needed)
8. Memorias active_session_state.md (sprint context)

Scripts invocados: NONE directly — architect is doc author + decision maker only.

Outputs writes:
- creative-specs/<id>.yaml (per video)
- PAUTA-MASTER amendments + INGENIERO-PAUTA amendments
- CREATIVE-SPEC-TEMPLATE.yaml (schema evolution)
- video-log.md entries

Comando típico user invoca:
> Pasame el creative-director skill, necesito armar SPEC video #2
   → Architect reads bootstrap + user interview FASE 0 + generates SPEC.yaml
```

### 16.2 🛠️ Engineer (terminal 1)

```
LLM client: Claude Code CLI (terminal interactive session)
Model: Claude Sonnet 4.x or Opus 4.x (long-running execute + parallel tools)
Context fresh: NEW terminal session

Bootstrap files leídos al arrancar:
1. CLAUDE.md (auto-loaded)
2. .claude/skills/video-director/SKILL.md
3. .claude/skills/ai-video-production/SKILL.md + BOOTSTRAP.md + PIPELINE.md
4. .claude/skills/ai-video-production/HYPERFRAMES-GOTCHAS.md + CAPTIONS.md + SFX-PIPELINE.md
5. .claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md
6. .claude/skills/video-animation/SKILL.md + ANIMATION-LAYER.md
7. .claude/skills/video-director/MODEL-BENCHMARK.md (model selection)
8. creative-specs/<id>.yaml (THIS video SPEC)
9. <project>/scripts/* (cuando ejecuta gates)

Scripts Python invocados (en order durante CP1-CP5):
CP1: scripts/image.py (Gemini Pro 3.1 anchor generation)
CP2: scripts/tts.py (ElevenLabs) + scripts/captions.py (Whisper)
CP3: scripts/image.py (shot generation)
CP4: scripts/video.py (Replicate Hailuo/Kling)
CP5 audio: scripts/sfx.py (ElevenLabs SFX) + scripts/master-audio.sh (ffmpeg loudnorm)
CP5 composition: npx hyperframes lint + scripts/render-lock.py
CP5 gates:
  - scripts/audit-spec-completeness.py (Gate 0)
  - scripts/audit-narrative.py (Gate 2)
  - scripts/audit-frames.py (Gate 4 — Gemini Vision interval 1s)
  - scripts/audit-frames-granular.py (Gate 5 — sentinels S1-S10)
  - scripts/audit-audio.py (Gate 6)
  - scripts/audit-against-referent.py (canonical bands check)
  - scripts/qa-gate.py (Gate 7 — dual gate score)
CP5 render: npx hyperframes render --output renders/draft.mp4
Forward Phase 1: scripts/measure-canonical-* + scripts/extract-canonical-max-detail.py

Outputs writes:
- <project>/assets/* (anchors + clips + tts + sfx + ambient + music)
- <project>/index.html (HyperFrames composition)
- <project>/renders/draft.mp4
- <project>/CP[N]-handoff.md per checkpoint
- <project>/captions/captions.json

Comando típico user invoca:
> Engineer, arrancá CP1 con SPEC matadero-banquete.yaml
   → Engineer reads SPEC + executes CP1 anchors + emits handoff
```

### 16.3 🔍 Auditor (terminal 3)

```
LLM client: Claude Code CLI (terminal interactive session)
Model: Claude Sonnet 4.x or Opus 4.x (independent verification)
Context fresh: NEW terminal session — NEVER share context with arch/eng

Bootstrap files leídos al arrancar (PRE-AUDIT obligatorio per AUDITOR-PROTOCOL § 1):
1. CLAUDE.md
2. .claude/skills/creative-director/AUDITOR-PROTOCOL.md (10 anti-patterns)
3. .claude/skills/creative-director/master-flow-v2/GAPS-LOG.md
4. creative-specs/<id>.yaml (THIS video SPEC completo)
5. .claude/skills/horror-choice-format/PAUTA-MASTER.md (creative authority empirical)
6. .claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md (technical authority)
7. ref-XX canonical primary (cited en SPEC.references)
8. video-log.md (rotation pattern)
9. <project>/CP[N]-handoff.md (engineer's report)
10. <project>/renders/draft.mp4 (when render done — for frame extraction)

Scripts Python invocados (auditor side):
- scripts/audit-spec-completeness.py (re-run independent)
- scripts/audit-frames-granular.py (sentinels S1-S10)
- scripts/audit-against-referent.py (canonical bands re-check)
- ffmpeg -ss <t> -i renders/draft.mp4 -vframes 1 (frame extract for visual verify)
- ffmpeg loudnorm (LUFS + TP verify)

Direct Gemini Vision queries (manual, NOT scripted yet):
- "Verify shot_NN visual matches SPEC visual_intent"
- "Detect character lip-sync compliance"
- "Cross-validate engineer claim X vs canonical ref"

Outputs writes:
- Tabla findings en chat (per AUDITOR-PROTOCOL § 4)
- Verdict 🟢/🟡/🔴/⛔ per CP
- GAPS-LOG.md updates (cuando nuevo gap detectado)

NEVER writes:
- creative-specs/* (architect domain)
- <project>/assets/* or renders/* (engineer domain)
- handoff.md (only emits chat findings)

Comando típico user invoca:
> Auditor, verifica CP1 handoff matadero
   → Auditor reads bootstrap + handoff + runs audits + emits verdict
```

### 16.4 Context isolation — how it's guaranteed

**Structural** (not optional):

1. **3 separate terminals** — each Claude Code instance has own context window
2. **No agent-to-agent direct messages** — all communication via filesystem (handoff.md files) OR user paste-bridge
3. **Each terminal reads ONLY its own protocol docs** — auditor reads AUDITOR-PROTOCOL, engineer reads INGENIERO-PAUTA, architect reads PAUTA-MASTER
4. **Fresh context per session** — when user closes/opens terminal, NEW Claude session = NEW context. Bootstrap files re-read.
5. **Anti-pattern #5** (codified): "Compartir contexto arq/ing" — auditor NEVER reads HANDOFF-PROTOCOL because that's arch/eng-side context. Independence preserved.

**Communication channels validated**:

```
User ↔ Architect    : direct chat terminal 2
User ↔ Engineer     : direct chat terminal 1
User ↔ Auditor      : direct chat terminal 3
User bridges agent communication via copy-paste prompts

Architect → Engineer  : creative-specs/<id>.yaml (filesystem)
Engineer → Auditor    : <project>/CP[N]-handoff.md (filesystem)
Auditor → Architect   : GAPS-LOG.md updates (filesystem) + escalation chat user

All agents → User     : direct chat
```

---

## 17. Ejemplos de prompts reales que arman los agentes

### 17.1 🏛️ Architect FASE 0 user interview (concept gathering)

```
FASE 0 — Architect prompt al usuario para gather inputs:

"Para producir tu video horror-choice, necesito 5 inputs FASE 0:

1. PATTERN ROTATION (revisar video-log.md rotation tracking)
   Última pattern usada: P6 Hedonismo Eterno (matadero v1)
   Disponibles forward: P1/P3/P5/P9 (avoid P6 again)
   ¿Cuál preferís? O describí el archetype de twist que querés.

2. SETTING + ATMOSPHERE
   Examples canonical: planta eléctrica, mina abandonada, acuario, carretera, 
   fundición, metro, tren, cockpit, matadero.
   ¿Qué setting? + paleta tonal preferred (warm/cool/sepia/cinematic).

3. DYAD CHARACTERS
   Necesito 2 characters uncanny + visualmente extreme:
   - Malo aparente (el que parece dangerous but...)
   - Bueno aparente (el que parece safe but...)
   Describilos físicamente OR pickeá del PAUTA § 5 catalog.

4. CLIFFHANGER ARCHETYPE
   Tipos: muerte / bucle eterno TRAP / pérdida identidad / prisión emocional / 
          salida amanecer
   ¿Cuál twist final querés?

5. DELIVERY FORMAT (default: reel 9:16, 88s)
   ¿Diferente? Especificá.

Cuando me confirmes los 5, genero SPEC v9 completo con shot_list 22 shots + 
narration_script + asset_list + GAPS #23-#28 fields populated."
```

### 17.2 🏛️ SPEC.yaml visual_intent example (matadero shot_07 climax)

```yaml
- id: shot_07_consequence_A1_climax
  timestamp_intent: [23, 27]
  duration_intent_s: 4
  scene_context:
    who_is_there: "Viewer POV (manos+cuchillo holding) + carcasa hanging from hook"
    who_does_what: |
      Carcasa colgante de un gancho se contorsiona violentamente, su parte 
      central (donde estaría el estómago) ABRE COMO UNA BOCA MASIVA con dientes 
      humanos uniformes perfectos visibles en el interior rosado-rojo. La boca 
      grita silencio. Carne se estira en hilos translúcidos entre dientes.
    why_this_shot_exists: |
      Climax body horror P6 consequence_A — viewer eligió "mirar" → carcasa 
      revela ser organismo vivo + lo va a tragar. Setup para shot_08 absorption.
    narration_in_this_shot: |
      [23.5-25.5s]: "Si mirás, la carcasa abre la boca grande, te traga entero."
  visual_intent: |
    POV viewer: manos+cuchillo visible bottom edge frame (frozen mid-action).
    Center frame: carcasa hanging from chain swinging slow. Mid-carcasa interior 
    expands wide reveals mouth aperture 60cm wide x 80cm tall. Inside: rows of 
    uniform human teeth (28-32 visible). Pink-red soft tissue glistens wet. 
    Lateral chain creaks visible side-to-side motion 5cm. Cinematic body horror.
  visual_action_match:
    spec_text_narration: "carcasa abre la boca grande te traga entero"
    visual_event_required: "carcasa apertura central + dientes humanos uniformes visible + viewer POV manos still"
    matches_literal: true
  pov: true
  lip_sync_required: false
  setting_ambient_creature_or_object: "rata gris escapando entre carcasas en fondo (lateral 5% frame width)"
  atmospheric_motions_count: 4
  atmospheric_motions_list:
    - "vapor pesado del piso ascending lateral"
    - "polvo flotando atmospheric (illuminated by overhead fluorescent flicker)"
    - "chain hooking slight oscillation 5cm side-to-side"
    - "carcass interior tissue glisten (wet shine pulses)"
  pov_traversal_intent: static
  character_active_gesture_per_shot: null  # no human characters this shot (carcasa = creature)
  ui_active: [caption_scale_pop_CENA_SIN_TERMINAR_Y62, watermark]
```

### 17.3 🛠️ Engineer Gemini Pro anchor generation prompt (CP1)

```python
# scripts/image.py invokes Gemini Pro 3.1 with this prompt structure:

anchor_prompt = """
You are generating a CHARACTER REFERENCE ANCHOR for video production.
This anchor will be reused across multiple shots to maintain character consistency.

CHARACTER: matarife_anchor

PROMPT (8K photorealistic):
Photorealistic 8k portrait, full body neutral standing pose, plain gray 
background, soft front light. Subject: tall thin male humanoid figure, 
height 1.85m. CRITICAL: his head is literally replaced by a large vertical 
butcher cleaver knife (60cm tall stainless steel blade pointing up, sharp 
edge visible at top, black molded grip where mouth would be at bottom — no 
human face, no eyes). Body wears thick brown leather butcher apron stained 
with dried blood and rust patches covering chest and thighs. Industrial 
blue plastic gloves up to elbows. Black rubber boots knee-high. Arms hang 
neutral at sides. No human facial expression possible (no face). The 
cleaver-head reflects ambient light subtly (steel sheen). Cinematic horror 
aesthetic but composed and frontal. No text, no logos.

OUTPUT REQUIREMENTS:
- 1080×1920 portrait orientation (Reel 9:16)
- 8K detail level
- Neutral background gray
- Plain front lighting (anchor reuse — lighting added per shot)
"""

# API call:
import google.genai as genai
client = genai.Client()
response = client.models.generate_images(
    model="imagen-3.0",  # OR "gemini-pro-image" depending on availability
    prompt=anchor_prompt,
    config={"number_of_images": 1, "aspect_ratio": "9:16"}
)
# Save to assets/anchors/matarife_anchor.png
```

### 17.4 🔍 Auditor Gemini Vision cross-validate prompt

```python
# Auditor runs independent Gemini Vision query to verify engineer claim
# (anti-pattern #8: pattern-match label sin medir directo)

auditor_query = """
You are an INDEPENDENT VIDEO AUDIT EXPERT.

CONTEXT: This is frame extracted at t=22s from matadero-banquete iter 8 render.
Engineer's claim: "D1 decision UI countdown shows digit '3' at start of window 
(t=22.64s) with proper film leader Academy style + freeze + filter overlay."

YOUR TASK: Verify the engineer's claim INDEPENDENTLY. Do NOT trust the label.

Examine the attached frame and report:

1. Is countdown digit "3" visible center frame? (Y/N + position)
2. What style is the countdown? (film_leader_academy = crosshair circle + big 
   central digit OR css_minimalist_ring = small ring + small digit OR other)
3. Is background scene frozen (no motion blur, sharp edges)? Or animated?
4. Is filter overlay applied (sepia/grain/VHS visible)? Or raw clip?
5. Are choice buttons "A) MIRAR" / "B) SEGUIR" visible at top?
6. Is loading bar visible? At what Y% position?
7. Is cocinera lips static (NOT mid-articulation)? Per anti-pattern #9, 
   character lips MUST be static when no character audio playing.

Output: structured JSON with each verification + concur/refute engineer claim.

CANONICAL REFERENCE: Reels P6 Hedonismo Eterno (ref-08 acuario + ref-13 
electrica per PAUTA-MASTER § 18 decision-UI-pacing).
"""

# Run query:
import google.genai as genai
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        {"role": "user", "parts": [
            {"text": auditor_query},
            {"inline_data": {"mime_type": "image/jpeg", "data": frame_b64}}
        ]}
    ]
)
# Parse JSON response → audit findings table
```

### 17.5 Common pattern — copy-paste user bridge prompts

User actúa como bridge entre agents (no direct comm). Typical bridge prompts:

```
USER → ARCHITECT (start sprint):
"Architect, necesito SPEC video #2. Inputs FASE 0: pattern P3, setting cinema 
abandonado, dyad proyeccionista (bueno aparente) + acomodador (malo aparente 
que salva twist), cliffhanger prisión emocional eterna."

USER → ENGINEER (start CP):
"Engineer, arrancá CP4 animation. SPEC: creative-specs/cinema-abandonado.yaml. 
Usá MODEL-BENCHMARK.md decision tree. Premium prompt 5-block obligatorio."

USER → AUDITOR (audit post-handoff):
"Auditor, verifica CP5-POST-AUDIT-handoff.md cinema-abandonado iter 1. 
Run Gate 0 + audit-frames-granular S1-S10 + dual gate check."

USER → AUDITOR (forward learning):
"Auditor, vi que [X] no funciona bien en este video. Codify forward como GAP 
si es sistémico."

User feedback chains (Rule D PRECEDENCE):
"User perceptual: [observation X]" → Auditor codifies → Architect adapts SPEC 
forward → Engineer implements forward.
```

---

**Última actualización**: 2026-05-20 PM (Sprint A roadmap + Phase 1 Track B Engineer completed + GAPS #23-#28 codified + § 14-17 NEW expansion for Excalidraw diagramming).
**Owner**: Auditor terminal 3 (este doc) + cross-validated por architect Track parallel
**Next revision**: post Phase 1 priority queue completion + video #2 first iter

---

## Apéndice — Matadero v1 reference card

```
Format: horror-choice × reel 9:16
Duration: 90.521s
Pattern: P6 Hedonismo Eterno (Cocinera path TRAP eterno)
Iterations: 8 (overnight → iter 8 GAP #22 fix)
Cost: $15.56 / $17 = 91.5%
Quality: Gemini 10/10 iter 6 + user 9.5/10 iter 8
Gaps codified during production: 12 NEW (#11-#22)
AVU library: 1/4 templates (countdown-3-2-1-film-leader)
Status: PUBLISHED 2026-05-19 PM Instagram @elige_tucompanero
```
