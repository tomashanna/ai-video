# Autonomous Video Factory — Roadmap

> **Goal**: scale from ~1 video/semana (manual) → 3 videos/día autonomous factory.
> **Decision principle**: NEVER auto-publish to IG (ban risk). Keep last-mile manual.
> **Validation gate**: video #3 manual ship with Phase 2 + calibrated v4 + GAP #40 EXECUTION CONTINUITY focus. IF achieves perceptual ≥9.0 → THEN build factory. IF NOT → re-iterate amendments first.

---

## 1. Why this exists

```
CURRENT (manual):
  USER triggers each phase → 30-90 min user time/video → ~1 video/semana max

GOAL (autonomous factory):
  Theme queue → autonomous CP1-CP5 con AUDITOR GATES per CP → human checkpoints → MANUAL publish
  → 3 videos/día sustainable → 90+/mes scale
  → User time: ~10 min/video × 3 = ~30 min/día
```

**Critical constraint**: auto-publishing to Instagram = ban risk. Last mile stays manual. User reviews finished render + clicks publish.

## 1.5 ⛔⛔ CRITICAL — Per-CP auditor gates MANDATORY (post 2026-05-21 V3 failure lesson)

V3 iter 1 producía 15 bugs at once porque engineer spawned as single agent CP1→CP5 autonomous sin auditor gates entre. User found at end + costoso iter 2 reassembly needed.

**HARD architectural rule**: orchestrator MUST spawn engineer as ONE agent per CP, con auditor gate spawn between each:

```
orchestrator.py per video:
  spawn architect_agent(theme) → SPEC.yaml
  spawn auditor_agent(audit SPEC vs PAUTA) → PASS/NB/FAIL verdict ⭐ GATE
  user_approval_gate(SPEC) ← CHECKPOINT 1
  
  spawn engineer_agent(CP1 anchors) → CP1-handoff.md
  spawn auditor_agent(audit CP1) → verdict ⭐ GATE
  if FAIL → re-spawn engineer CP1 (iter), max 3 attempts
  
  spawn engineer_agent(CP2 TTS) → CP2-handoff.md
  spawn auditor_agent(audit CP2) → verdict ⭐ GATE
  
  spawn engineer_agent(CP3 shots) → CP3-handoff.md
  spawn auditor_agent(audit CP3) → verdict ⭐ GATE
  
  spawn engineer_agent(CP4 animation) → CP4-handoff.md
  spawn auditor_agent(audit CP4) → verdict ⭐ GATE
  
  spawn engineer_agent(CP5 render) → renders/draft.mp4
  spawn auditor_agent(final audit) → verdict ⭐ GATE (calibrated v4 + sentinels + audit-spec)
  
  user_checklist_gate(render) ← CHECKPOINT 2
  user_publish_manual() ← CHECKPOINT 3 (anti-ban)
```

**Why this matters**: bug detection cost scales linearly per CP vs exponentially at end-of-pipeline. Catching missing decision UI at CP2 = 5 min fix vs catching at CP5 = full reassembly hour.

**Forward implementation**: `scripts/orchestrator-cp-by-cp.py` enforces this pattern. No "execute end-to-end" allowed.

---

## 2. Pre-condition before building factory

**Video #3 must validate the Phase 2 + calibrated v4 + GAP #40 stack**.

Required outcomes for GO decision:
- ✅ Video #3 perceptual score ≥9.0 (vs current baseline 7.85)
- ✅ Gemini calibrated v4 ≥9.0
- ✅ EXECUTION CONTINUITY dimension ≥8.5 per cut audit
- ✅ Iter count ≤3 (vs matadero 8, cinema 6)
- ✅ Cost ≤$9 per video

If video #3 hits all 5 → factory greenlit.
If video #3 misses → iterate amendments first, retest video #4 manual.

---

## 3. Sequential phases (no timeframes — gated by quality)

```
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 0 — Video #3 MANUAL validation                                 │
│  ───────────────────────────────────                                 │
│  • Architect manual interview + SPEC v10                             │
│  • Engineer manual CP1-CP5 with Phase 2 stack                        │
│  • Auditor manual gates incl. calibrated v4                          │
│  • User HUMAN-CHECKLIST                                              │
│  • GATE: perceptual ≥9.0? IF YES → Step 1. IF NO → iterate            │
└──────────────────────────┬───────────────────────────────────────────┘
                           │ video #3 validated
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 1 — Orchestrator scaffold (Phase A)                            │
│  ────────────────────────────────────────                            │
│  • Anthropic Agent SDK setup                                         │
│  • Define 3 agent classes (Architect / Engineer / Auditor)           │
│  • Task queue (SQLite local DB)                                      │
│  • State machine: PENDING → SPEC_GEN → ... → AUDITED                 │
│  • Manual test: 1 video to SPEC stage autonomous                     │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 2 — Engineer + quality gates autonomous (Phase B)              │
│  ─────────────────────────────────────────────────────               │
│  • Engineer autonomous CP1-CP5                                       │
│  • Per-clip atomic pipeline runs end-to-end                          │
│  • Auditor autonomous (calibrated v4 + sentinels + audit-spec)       │
│  • Quality Gate Agent per clip operates autonomously                 │
│  • Manual test: 1 video end-to-end render stage                      │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 3 — Monitoring + cost tracking (Phase C)                       │
│  ──────────────────────────────────────────                          │
│  • Dashboard CLI / web UI                                            │
│  • Cost tracker per video (Replicate + Anthropic Claude API)         │
│  • Alert thresholds (cost overrun, error rates)                      │
│  • DO NOT add auto-publish — keep manual                             │
│  • Manual test: 3 videos in queue, all autonomous to ready-state     │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│  STEP 4 — Production hardening (Phase D)                             │
│  ────────────────────────────────                                    │
│  • Failure recovery patterns (NSFW reject → Hailuo fallback)         │
│  • Network retry exponential backoff                                 │
│  • Quality gate iter cap (3 attempts → escalate human)               │
│  • Schedule automation (daily queue check)                           │
│  • Human override mechanisms (cancel, force-pass, skip CP)           │
│  • First week production observation                                 │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
                           ▼
                  ┌─────────────────────┐
                  │  PRODUCTION READY   │
                  │  3 videos/día        │
                  │  Manual publish      │
                  └─────────────────────┘
```

---

## 4. Architecture diagram (Excalidraw spec § 11.8)

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER DASHBOARD (CLI / web)                    │
│  • Input theme/pattern queue                                     │
│  • Monitor in-flight videos + costs                              │
│  • SPEC approval gate (HUMAN CHECKPOINT 1)                       │
│  • Final HUMAN-CHECKLIST gate (HUMAN CHECKPOINT 2)               │
│  • MANUAL PUBLISH to IG (HUMAN CHECKPOINT 3 — anti-ban)          │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR.py                             │
│                                                                  │
│  Cron / Schedule: trigger 3x/día                                 │
│  ────────────────────────────────────                            │
│  for video in queue:                                             │
│    state = init_state(video)                                     │
│    spawn_architect(state) → SPEC.yaml                            │
│    user_approval_gate(SPEC)  ← HUMAN CHECKPOINT 1                │
│    spawn_engineer(SPEC, state) → CP1-CP5 (autonomous)            │
│    spawn_auditor(state) → calibrated_v4_gate                     │
│    if gemini_calibrated_v4 ≥9.0:                                 │
│      mark_ready_for_review(render)                               │
│      user_checklist_gate(render)  ← HUMAN CHECKPOINT 2           │
│      if approved:                                                │
│        export_render + caption_draft for MANUAL publish          │
│        user_publish_manual()  ← HUMAN CHECKPOINT 3 (anti-ban)    │
│    else: iter or escalate human                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │ ARCHITECT  │  │  ENGINEER  │  │  AUDITOR   │
        │  agent     │  │   agent    │  │   agent    │
        │            │  │            │  │            │
        │ Claude API │  │ Claude API │  │ Claude API │
        │ + PAUTA    │  │ + Phase 2  │  │ + calib v4 │
        │ docs       │  │ pipeline   │  │ + gates    │
        └────────────┘  └────────────┘  └────────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐  ┌────────────┐  ┌────────────┐
        │ Veo 3.1    │  │ Hailuo     │  │ Quality    │
        │ Gemini API │  │ Replicate  │  │ Gate Agent │
        │ FREE       │  │ ($0.27-    │  │ per clip   │
        │            │  │  $0.60/    │  │ autonomous │
        │            │  │   clip)    │  │            │
        └────────────┘  └────────────┘  └────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │  Filesystem output queue     │
                │  /renders/ready/<video>.mp4  │
                │  + caption_draft.txt         │
                │  + hashtags.txt              │
                │  + first_frame_thumbnail.jpg │
                └──────┬───────────────────────┘
                       │
                       ▼ user manually publishes when ready
                ┌──────────────────────────────┐
                │   USER → IG @elige_tucompanero│
                │   (manual click, anti-ban)    │
                └──────────────────────────────┘
```

**Color coding for Excalidraw**:
- Orchestrator: BLUE (#3B82F6)
- Architect agent: PURPLE (#6B46C1)
- Engineer agent: GREEN (#10B981)
- Auditor agent: ORANGE (#F59E0B)
- Quality Gate Agent: TEAL (#14B8A6)
- Veo 3.1: YELLOW (#EAB308) — FREE enterprise
- Hailuo Replicate: RED (#EF4444) — paid
- Human checkpoints: BIG STARS ⭐ at 3 specific points
- Filesystem state: GRAY (#6B7280)
- Publishing: BLUE (#3B82F6) — USER ONLY, NOT AUTOMATED

---

## 5. Cost model autonomous factory

```
Per video forward:
  Replicate Hailuo fallback (~30% shots gore/NSFW):  ~$3
  Veo 3.1 70% shots (Gemini enterprise):             $0
  Gemini Vision audits (enterprise):                  $0
  ElevenLabs TTS+SFX+music (enterprise):              $0
  Anthropic Claude API orchestrator (3 agents):      ~$0.25
  IG Graph API (NOT used — manual publish):           $0
  ────────────────────────────────────────────
  Per video:                                          ~$3-5

3 videos/día × $4 average = $12/día
× 30 días = $360/mes
× 12 meses = $4,320/año Replicate + Claude API

Plus infrastructure:
  - Local Mac running orchestrator: $0 (existing hardware)
  - SQLite DB: $0
  - Filesystem state: $0
  - Optional: cloud orchestrator alternative ~$20/mes
  
GRAND TOTAL ANNUAL: ~$4,320-4,560/año
```

**Comparison vs current manual at scale**:
- Manual 3/día × current $14-15/video × 90/mo = ~$1,260/mes = $15,120/año
- Autonomous factory: $4,320/año Replicate + Claude
- **Savings: ~$10,800/año + most of your time**

---

## 6. Anti-ban posting strategy

### Why auto-publishing risky

```
IG anti-bot detection signals (cause bans):
  ✗ Exact same posting time daily
  ✗ Identical caption patterns
  ✗ Rapid bulk uploads
  ✗ Same device + IP + API key signature
  ✗ Zero engagement (no replies, likes given, story views)
  ✗ Pure outbound (no inbound activity)

PUBLIC: even official IG Business API has rate limits + ban risk if patterns automated.
```

### Mitigation (manual publish strategy)

```
Factory output: filesystem queue with READY videos + caption drafts
USER:
  - Opens IG mobile app or web manual
  - Picks 1-3 ready videos
  - Posts at varied times (morning / evening / late night)
  - Personalized caption tweaks per video
  - Engages with comments + DMs naturally
  - Mixes manual posts + factory-prepared
  - Stories + non-Reel content varies pattern

Result: factory does production heavy-lifting, USER does last-mile humanity-touch.
USER time: ~5 min/video to publish = 15 min/día for 3 posts.
```

### Optional automation (future, post-validation)

```
After 30+ videos shipped manual with good engagement:
  - Consider scheduled posting via Meta Business Suite (their UI scheduler)
  - Still avoid programmatic API publish
  - Mix scheduled + organic posting
  - Maintains posting variability
```

---

## 7. Risk matrix

| Risk | Likelihood | Impact | Mitigation |
|------|:---:|:---:|---|
| Veo quota hit at scale | Mid | High | Monitor + alert + fallback Hailuo, contact Google enterprise support |
| Gemini calibrated v4 drift | High | Mid | Track gemini_user_delta monthly, retrain prompt cada 10-20 videos |
| IG ban from auto-posting | High | Critical | **MANUAL PUBLISH ONLY** — factory ends at filesystem queue |
| Quality drift sin user attention | Mid | High | HUMAN-CHECKLIST 2 stays — 5 min/video user review |
| Replicate costo runs away | Low | Mid | Cost alerts + circuit breaker (>$X/día halt queue) |
| Architect generates similar SPECs | Mid | Low | Pattern rotation logic + theme seed input from user |
| Failure cascades (Veo→Hailuo→both fail) | Low | High | Escalate to human queue after 3 failed iters per CP |
| Phase 2 architecture untested at volume | High | High | **STEP 0 video #3 validates BEFORE factory build** |
| Network failures mid-production | Mid | Low | Retry exponential backoff + checkpoint state |
| Gemini hallucinations in SPEC | Mid | Mid | SPEC validation script + architect re-spec on fail |

---

## 8. Human checkpoints (3 strategic gates)

```
CHECKPOINT 1: SPEC approval (5 min/video)
  - Architect outputs SPEC v10 YAML
  - User reviews: pattern OK? characters interesting? counterfactual placement?
  - Approve → commit to engineer
  - Reject → architect re-spec OR shelve

CHECKPOINT 2: HUMAN-CHECKLIST final (5 min/video)
  - Engineer + Auditor done autonomous, render ready
  - User watches render full
  - 7 Q gestalt review
  - Perceptual score 1-10 (feeds TASTE-LOG)
  - Approve → mark ready for manual publish
  - Reject → iter or shelve

CHECKPOINT 3: Manual publish (5 min/video) — ANTI-BAN
  - User opens IG, picks video from /renders/ready/
  - Manual upload with caption tweaks + hashtags
  - Posts at organic time
  - Engages with comments naturally

Total user time per video: ~10-15 min
3 videos/día × 12 min avg = 36 min/día sustainable
```

---

## 9. Implementation phases reference

| Phase | Component | Deliverable |
|-------|-----------|-------------|
| **A** | Orchestrator scaffold | `orchestrator.py` + state machine + queue DB + Architect agent class |
| **B** | Autonomous engineer + auditor | `EngineerAgent` + `AuditorAgent` classes + calibrated v4 gate integration |
| **C** | Monitoring + cost tracking | Dashboard CLI/web + cost tracker + alert system |
| **D** | Production hardening | Failure recovery + schedule automation + override mechanisms |
| **Production** | Daily operation | 3 videos/día queue → autonomous CP1-CP5 → user publishes manually |

---

## 10. Decision tree forward

```
START
  │
  ▼
Video #3 ships manual with Phase 2 + calibrated v4 + GAP #40 focus
  │
  ▼
Perceptual score ≥9.0?
  ├─ NO → iterate amendments + try video #4 manual
  │       (don't build factory until quality validated)
  │
  └─ YES → Greenlight autonomous factory
            │
            ▼
          Phase A: Orchestrator scaffold
            │
            ▼
          Phase B: Engineer + auditor autonomous
            │
            ▼
          Phase C: Monitoring + cost
            │
            ▼
          Phase D: Production hardening
            │
            ▼
          PRODUCTION (3 videos/día)
            │
            ▼
          MANUAL PUBLISH (anti-ban)
            │
            ▼
          Engagement metrics monitor
            │
            ▼
          Iterate based on viewer perceptual + IG analytics
```

---

## 10.5 Scoring rubrics — full taxonomy (added 2026-05-21 PM late post user request)

> **Why this section**: doc previously referenced "Gemini holistic 14-dim" + "Calibrated v4 EXECUTION CONTINUITY 30%" without listing dimensions. This codifies the actual rubrics.

### 10.5.1 OLD Gemini holistic 14-dim (universal prompt, generic critic)

Source: `ai-video-production/QA.md § Prompt UNIVERSAL`. Used pre-2026-05-21 calibrated v4. Score cap rules: ANY of dimensions 12-13-14 failing → cap 8.0 maximum.

| # | Dimension | Anti-hallucination focus |
|---|-----------|--------------------------|
| 1 | Sync narración + captions (desfase audible?) | — |
| 2 | Texto legible en todos los fondos (incluyendo niebla, amanecer, fuego) | — |
| 3 | Variedad visual o reuse same image múltiples momentos | — |
| 4 | Vivo (motion en cada plano) vs slideshow (fotos estáticas) | — |
| 5 | Sound design beyond narración+música (footsteps, breaths, impactos, ambient) | — |
| 6 | Static >2s without any motion? | — |
| 7 | Transiciones intencionales vs abruptas | — |
| 8 | Audio mix hierarchy (narración dominant, música apenas, SFX en su lugar) | — |
| 9 | Cinematográfico vs "presentación con narración" | — |
| 10 | Continuidad narrativa caption vs narrator (no contradicts/duplicates en 5s) | Anti-hallucinate |
| 11 | INVENTARIO UI ELEMENTS — list each text/UI with timestamp + flag missing | Anti-hallucinate |
| 12 ⛔ | INVENTARIO NARRACIÓN timestamp-by-timestamp + gaps >2s + cobertura <40% | **Score cap 8.0 if fail** |
| 13 ⛔ | INVENTARIO MÚSICA timestamps + cobertura % + segmentos >5s sin música | **Score cap 7.0 if music absent** |
| 14 ⛔ | NARRATIVE CLOSURE — "viewer cuenta video en 1 frase" + plot twist comprensión | **Score cap 7.5/8.0 if broken** |

**Why this rubric existed**: pueblo-fantasma-desierto v2 case 2026-05-13 — Gemini gave 9.9 to video with 24% narration coverage + 40s outro silence. Dimensions 12-13-14 added as anti-hallucination forcing inventory checks.

**Why it was inflated for our use case**: 14-dim scored OUR productions HIGHLY (matadero 10/10 iter 6) but our user perceived them ~7.9. The rubric measures "cinematic + sound + narrative inventory" — captures technical quality but MISSES execution continuity (the X factor).

### 10.5.2 NEW Calibrated Gemini v4 10-dim — TOMÁS-CALIBRATED (replaces holistic for our use case)

Source: `ai-video-production/templates/calibrated-gemini-prompt-v4.txt`. Tested 2026-05-21 against 5 known scored videos. Mean abs Δ 0.14 vs user perceptual scores.

| # | Dimension | Weight | What it measures |
|---|-----------|:------:|-------------------|
| 1 ⭐⭐ | **EXECUTION CONTINUITY** | **30%** | PRIMARY — see § 10.5.3 below for full definition |
| 2 | INMERSIÓN POV / character-alive | 15% | POV hands as viewer-is-character OR strong third-person character-alive framing + traversal continuous |
| 3 | SOUND DEPTH (music layers + sound design) | 15% | Count distinct continuous sound layers (drone + ambient + accent + foley). Penalize thinness, NOT richness |
| 4 | ATMOSPHERE coherence + "alive" feel | 10% | Genre sustained throughout. Atmospheric secondary motions ≥3 simultaneous per shot |
| 5 | CHARACTER signature + "alive" gestures | 10% | Visually distinctive uncanny silhouette + active gestures (NOT mannequin-static) |
| 6 | STORY LOGIC CONTINUITY | 5% | Story chain causal makes sense + counterfactual placement (BEFORE choice OR twin/relief, NOT retrospective) |
| 7 | EDITING modulation | 5% | Cuts/min 14-22 + transition variety ≥3 types + pacing modulates |
| 8 | HOOK 0-9s retention | 5% | First 9s establishes stakes + visual scroll-stop |
| 9 | CAPTIONS | 3% | Light weight — absence in liminal-spaces is LIGHT penalty only (NOT destructor) |
| 10 | NARRATIVE comprehension (dilemma + counterfactual) | 2% | Clear dilemma + counterfactual logic understandable |

**Sum**: 30 + 15 + 15 + 10 + 10 + 5 + 5 + 5 + 3 + 2 = **100%**

### 10.5.3 EXECUTION CONTINUITY — full dimension specification (the #1 dim, 30% weight)

**The X factor** identified 2026-05-21 PM. THE primary gap own production → canonical refs.

**Definition**: viewer experiences ONE continuous physical journey — every shot transition has motion + audio + style bridging to the next. NOT just narrative chain coherent (Gemini already good at that). It's about PHYSICAL EXECUTION.

**4 sub-criteria per cut transition**:

1. **POV/character motion REAL between shots**
   - Camera/character is PHYSICALLY MOVING during transitions
   - Viewer SEES themselves walking, descending, advancing
   - NEVER teleportation between locations
   - Sub-anti-pattern: hard-cut from static composition to different framing without motion

2. **Audio bridges across cuts**
   - Sound layer (drone/ambient/foley) is CONTINUOUS across edit points
   - Music doesn't drop at cuts
   - Sound matches the physical journey
   - Sub-anti-pattern: silence at cut, abrupt audio change

3. **Visual style consistent shot-to-shot**
   - Color grading, lighting, framing language stays consistent within section
   - No jarring style jumps
   - Sub-anti-pattern: LUT changes mid-section

4. **Kinetic momentum sustains**
   - The motion of shot N continues into shot N+1
   - If POV is walking forward in shot N, shot N+1 shows continued forward motion OR organic stop
   - NOT abrupt teleport to different setup
   - Sub-anti-pattern: motion velocity shifts abruptly without narrative reason

**Scoring rule**:

| Score | Criteria |
|:-----:|----------|
| **10/10** | Every shot transition has ≥2 of {POV motion bridge / continuous audio / kinetic momentum / consistent style}. Viewer feels ONE continuous physical journey. POV traversal visibly present. |
| 8/10 | Most transitions have continuity bridges. 1-2 hard-cut teleportations but mostly bridged. |
| 6/10 | Half transitions have bridges, half are teleportations. Viewer feels "stop-and-start". |
| **4/10** | Most transitions are teleportations. Story chain present BUT physical journey absent. ⚠️ MATADERO PATTERN. |
| 2/10 | Total slideshow — every shot its own setup, no transitions, no journey. |

**HARD penalty rule**: If 3+ teleport-cuts detected → score this dimension at **4-6 maximum**, regardless of story coherence. Story chain DOES NOT compensate broken execution.

**Critical examples** (from calibrated v4 prompt):

```
❌ BROKEN (matadero v1, scored exec dim 4.8/10):
   Shot 1: meat hanging close-up (POV stationary)
     ↓ HARD CUT (no motion bridge, audio drops)
   Shot 2: matadero exterior wide (POV teleported)
     ↓ HARD CUT (no traversal)
   Shot 3: cutting POV (POV teleported)
     ↓ HARD CUT
   Shot 4: monstrous mouth appears (teleport, no spatial link)
     ↓ HARD CUT
   Shot 5: mouth attacks (teleport to consequence)
   Result: story makes sense BUT execution = teleports.

✅ ACHIEVED (Ref-A cave, scored exec dim 10/10):
   Shot 1: I'm in the cave (POV stationary, drone audio)
     ↓ POV WALKS FORWARD (kinetic motion bridges cut, audio sustained)
   Shot 2: deeper in cave (visible continuation of motion, same audio)
     ↓ Diving suit offered (POV stops, organic transition)
   Shot 3: putting on suit (motion organic, audio continues)
     ↓ I descend (POV motion downward visible, music shifts but layer continuous)
   Shot 4: underwater POV (continuation of descent, underwater audio bridges)
     ↓ Swimming forward (motion continues)
   Result: story + execution BOTH present. Viewer FEELS the journey.
```

### 10.5.4 GAP #40 — full specification

**ID**: GAP #40 (logged in GAPS-LOG.md 2026-05-21 PM)
**Title**: EXECUTION CONTINUITY — primary gap own production → canonical (THE X factor)
**Category**: `format-agnostic-creative` (per gap classification index — applies cross-format)
**Status**: ⚠️ PARTIAL — auditor codification + v4 prompt shipped + calibration validated; architect amendments PAUTA § 22 + INGENIERO-PAUTA NEW section + SPEC schema v11 in flight

**Description**: The 4 sub-criteria above (POV motion bridge / audio bridge / visual style / kinetic momentum) define what was missing in matadero + cinema-abandonado vs canonical refs. User articulated 2026-05-21 PM late:

> "Lo más importante es la consistencia. Si te fijas en los videos que le di el 9.9 o 10 tiene una consistencia clara, se entiende perfecto como avanza la historia y en qué punto estoy. Estoy en la cueva, avanzo, camino, se me ofrece traje de buceo, me lo pongo, bajo con traje, estoy buceando. Todo eso acompañado de movimiento dentro de la cueva (avanzando) luego nadando."

**Disparador**: calibrated Gemini v3 prompt FAILED to catch matadero outlier (scored 9.7 vs user 7.9). User clarified the X factor is execution-level, not narrative-level.

**Mechanism**: Gemini reading narrative chain coherent gives high score even when physical journey broken. The calibrated v4 prompt added EXECUTION CONTINUITY as dimension 1 (30% weight) + teleport-cut detection rule that forces dim score 4-6 max when ≥3 teleports.

**Codification status**:
- ✅ Calibrated Gemini v4 prompt PRIMARY dimension shipped
- ✅ INGENIERO-PAUTA § 8.16 implementation NEW (motion_bridge_intent SPEC field + audio_layer_continuity + visual_style_lut + ffmpeg recipes)
- ✅ AUDITOR-PROTOCOL § 6 anti-pattern #14 NEW: "Story chain rationalization without execution check"
- ⏳ ARCHITECT SPEC v10 schema fields per shot (pending architect commit)
- ⏳ scripts/audit-execution-continuity.py forward (Phase 3 priority automation)

### 10.5.5 v3 → v4 transformation (how mean abs Δ 0.14 was achieved)

**v3 prompt (failed)**:
- Had 9 dimensions: INMERSIÓN POV (20%) + SOUND (20%) + ATMOSPHERE (15%) + NARRATIVE+counterfactual (15%) + CHARACTER (10%) + EDITING (10%) + HOOK (5%) + CAPTIONS (5%)
- Treated narrative + execution as ONE thing under "NARRATIVE" dimension
- Gemini scored matadero 9.7 weighted (vs user 7.9) — missed teleport-cuts
- Mean abs Δ across 5 critical videos: 0.46

**Key changes v3 → v4**:

1. **SPLIT narrative dimension into TWO**:
   - NEW dimension 1: EXECUTION CONTINUITY (30% — physical journey)
   - DEMOTED dimension 6: STORY LOGIC CONTINUITY (5% — story chain)
   - Gemini was good at story chain (over-scoring 9-10) but blind to execution

2. **WEIGHT REBALANCING**:
   - Dim 1 EXECUTION CONTINUITY: NEW 30% (highest)
   - Dim 2 INMERSIÓN POV: 20% → 15% (reduced — partially captured by exec continuity)
   - Dim 3 SOUND DEPTH: 20% → 15% (slight reduction)
   - Dim 4 ATMOSPHERE: 15% → 10%
   - Dim 5 CHARACTER: 10% (kept)
   - Dim 6 STORY LOGIC: NEW 5% (was bundled in NARRATIVE)
   - Dim 7 EDITING: 10% → 5%
   - Dim 8 HOOK: 5% → 5%
   - Dim 9 CAPTIONS: 5% → 3%
   - Dim 10 NARRATIVE comprehension: NEW 2% (was bundled in NARRATIVE)

3. **EXPLICIT teleport-cut detection rule**:
   - v3: scored execution implicitly under narrative — Gemini over-scored
   - v4: explicit "if 3+ teleport cuts → cap dim 1 at 4-6 regardless of story coherence"
   - Forces Gemini to TRACE shot-by-shot transitions in output

4. **MANDATORY journey trace in output**:
   - v4 output format requires "EXECUTION CONTINUITY ANALYSIS" section with shot-by-shot trace
   - Forces Gemini to count teleports explicitly
   - Cannot rationalize away execution issues

5. **Enriched calibration examples** (11 datapoints in prompt):
   - Each example explains BOTH story logic AND execution continuity
   - matadero examples emphasize teleport pattern
   - Backrooms examples emphasize motion-bridged journey

**Results validation**:

| Video | v3 score | v4 score | User | v3 Δ | v4 Δ |
|-------|:---:|:---:|:---:|:---:|:---:|
| matadero | 9.7 | **7.6** | 7.9 | +1.80 | **-0.30** ✅ |
| cinema | 8.3 | **7.4** | 7.8 | +0.50 | **-0.40** ✅ |
| Ref-A cave | 10.0 | 10.0 | 10.0 | 0.00 | 0.00 ✅ |
| Ref-3 cockpit | 10.0 | 10.0 | 10.0 | 0.00 | 0.00 ✅ |
| Ref-1 mina | 9.9 | 9.9 | 9.9 | 0.00 | 0.00 ✅ |

**v3 mean abs Δ = 0.46**
**v4 mean abs Δ = 0.14**
**Improvement: 70% reduction** in gap vs user perceptual

**Why v4 works**: explicit dimension + hard penalty rule forces Gemini to evaluate WHAT actually distinguishes own-prod from canonical, rather than averaging high scores from features Gemini sees everywhere.

---

## 11. Status tracker (update during each phase)

```
PHASE 0 (validation):
  [ ] Video #3 manual production
  [ ] Calibrated v4 score ≥9.0
  [ ] EXECUTION CONTINUITY dim ≥8.5
  [ ] User perceptual ≥9.0
  [ ] Cost ≤$9
  [ ] User decision: build factory?

PHASE A (orchestrator scaffold):
  [ ] Anthropic Agent SDK setup
  [ ] Architect agent class
  [ ] State machine + queue
  [ ] 1 video to SPEC stage autonomous

PHASE B (autonomous engineer + auditor):
  [ ] Engineer agent class (CP1-CP5)
  [ ] Auditor agent class (gates)
  [ ] Quality Gate per clip autonomous
  [ ] 1 video end-to-end render

PHASE C (monitoring):
  [ ] Dashboard CLI/web
  [ ] Cost tracker
  [ ] Alert thresholds
  [ ] 3 videos queue test autonomous to ready

PHASE D (hardening):
  [ ] Failure recovery patterns
  [ ] Schedule automation
  [ ] Override mechanisms
  [ ] First week production

PRODUCTION:
  [ ] 3 videos/día sustained
  [ ] Manual publish working
  [ ] Engagement metrics improving
```

---

**Authored**: 2026-05-21 PM late, post Veo 3.1 enterprise validation + Phase 2 architecture complete.
**Status**: AWAITING Step 0 — video #3 manual production with new stack.
**Next**: USER triggers architect terminal 2 → architect reads `ARCHITECT-BRIEFING-VIDEO-3.md` → autonomous FASE 0 → SPEC v10 → handoff engineer.
