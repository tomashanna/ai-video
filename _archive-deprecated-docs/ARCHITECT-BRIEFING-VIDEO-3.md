# ARCHITECT BRIEFING — Video #3 launch (2026-05-21 PM)

> **For**: 🏛️ Arquitecto en terminal 2 (creative-director skill)
> **From**: 🔍 Auditor (this session, 3-terminal separation per memory `feedback_3_terminal_separation`)
> **Status**: SISTEMA ENTERAMENTE LISTO for video #3 forward. Architect can launch interview con user any time.

---

## 🎯 Lo que cambió desde matadero/cinema

Sprint sistémico 2026-05-21 producido (en este orden):

### Nuevas authority docs
1. **PAUTA-MASTER § 23-25 + § 24.8 refined**: cuts/min canonical 14-22 + counterfactual placement refined (twin-ending acceptable) + music layers 3 mandatory
2. **INGENIERO-PAUTA § 8.11-8.17 NEW** (7 new sections):
   - § 8.11 per-section music layers (3 layer ffmpeg recipe)
   - § 8.12 pacing markers per shot
   - § 8.13 effects library usage table
   - § 8.14 anchor STRICT mode ALL shots (cost RESET to $0 enterprise)
   - § 8.15 Hailuo Pro 1080p escalation policy
   - § 8.16 ⭐ EXECUTION CONTINUITY implementation (motion bridges + audio bridges + LUT consistency)
   - § 8.17 lip-sync integration (Hedra default OR Veo 3.1 if enterprise)
3. **AUDITOR-PROTOCOL § 3 CP5 step 11 NEW** + § 6 anti-patterns #11-#14 NEW
4. **GAPS-LOG**: 35 gaps total. **GAP #40 ⭐⭐ EXECUTION CONTINUITY** = THE primary X factor (post-2026-05-21 PM)

### Cost model RESET (CRITICAL) — UPDATED 2026-05-21 PM late

User confirmed 2026-05-21 PM late: **Gemini Enterprise (Business Edition) includes Veo 3.1 as capacity** — replaces Veo 3.0, NOT add-on. PLUS Gemini + ElevenLabs enterprise = $0.

⭐⭐ **MASSIVE IMPLICATION**: Veo 3.1 ($0.40/s retail) now FREE via Gemini API direct. Native audio + lip-sync + 4K + 9:16 + cinematic 9/10 quality.

### ⚠️ Veo USE CASE clarification (user 2026-05-21 PM late)

**Veo is a GENERATOR (scene-from-scratch), NOT a DUBBER (post-process)**:
- **Veo 3.1**: GENERATES whole character-speaking shot (visual + audio + lip-sync) from prompts + character anchor image → use when generating scenes from scratch
- **Sync Labs / HeyGen**: DUBS existing real-life video to new audio → NOT our use case
- **Hedra Character-3**: still → talking head, narrowed use case — Veo replaces at $0

**API route critical**: Use Veo via **Gemini API direct** (free enterprise), NEVER via Replicate (paid separate).

```
ANTES (matadero/cinema):  $14-16/video
DESPUÉS new model:        $0-9/video (depends on Veo NSFW filter)

3 SCENARIOS forward:

SCENARIO A — Veo 3.1 unlimited + accepts horror content:
  All animation via Veo = $0
  Native audio + lip-sync via Veo = $0
  Total Replicate: $0
  Total video #3: ~$0 (operational only)
  
SCENARIO B (REALISTIC) — Veo for safe + Hailuo for gore:
  ~70% shots Veo-safe = $0
  ~30% shots gore via Hailuo Pro = $3.60-4.20
  Lip-sync Veo native = $0
  Total Replicate: ~$4
  Total video #3: ~$4
  
SCENARIO C (CONSERVATIVE) — Veo selective hero + Hailuo rest:
  Hero shots (3) + lip-sync (3) via Veo = $0
  Rest (16) via Hailuo Std + Pro = ~$8
  Total video #3: ~$8

SCENARIO D (FALLBACK) — Veo NSFW rejects most:
  All animation via Hailuo Std/Pro = $5-8
  Lip-sync Hedra fallback = $1.50
  Total video #3: ~$7-10
```

⚠️ **CRITICAL TEST NEEDED BEFORE VIDEO #3 COMMITS**: Veo 3.1 NSFW filter historically rejects horror gore. Need test bench (3 sample shots safe/borderline/horror) to determine which Scenario applies. Per INGENIERO-PAUTA § 8.18.5.

### FREE (Enterprise confirmed)
- ✅ Veo 3.1 video generation (NEW)
- ✅ Gemini Vision audits (calibrated v4)
- ✅ Gemini Nano Banana image gen
- ✅ ElevenLabs TTS + SFX + music + voice cloning
- ✅ Whisper local

### PAID (Replicate only)
- Hailuo Std/Pro (if used for gore/NSFW shots Veo rejects)
- Hedra Character-3 (fallback if Veo lip-sync insufficient)
- Kling/Seedance (alternative tiers if needed)

### Calibrated Gemini v4 deployed
- Mean abs Δ 0.14 across 5 test videos
- EXECUTION CONTINUITY dimension primary (30% weight)
- Run via `audit-gemini-calibrated.py` post-render
- New gate primario proposed: `gemini_calibrated_v4 ≥9.0` OR `user_perceptual ≥8.5`

---

## 🚨 GAP #40 EXECUTION CONTINUITY — primary directive for SPEC design

**User articulated 2026-05-21 PM**: el gap own → canonical es **execution continuity**, NO story chain.

Specifically 4 sub-criteria per cut transition (codified INGENIERO-PAUTA § 8.16.2):

1. **POV motion bridge** — POV/character physically moves between shots (no teleportation)
2. **Audio bridge** — sound layer continuous across cuts (no silence)
3. **Visual style consistent** — LUT same shot-to-shot within section
4. **Kinetic momentum** — motion of shot N continues into shot N+1

**Matadero pattern (BROKEN)**:
```
shot 1: meat (static POV)
→ HARD CUT (no motion bridge)
shot 2: matadero exterior (teleport, new framing)
→ HARD CUT  
shot 3: cutting (teleport again)
→ HARD CUT
shot 4: mouth attack (teleport)
```

**Ref-A cave pattern (CORRECT)**:
```
shot 1: cueva (POV stationary)
→ POV WALKS FORWARD (motion bridges cut)
shot 2: cueva deeper (visible continuation)
→ DIVING SUIT OFFERED (organic transition)
shot 3: putting on suit (continuation)
→ DESCENDING (motion bridges cut)
shot 4: underwater (continuation visible)
```

**Architect SPEC v10 needs NEW fields per shot**:

```yaml
shot_list:
  - shot_id: <id>
    motion_bridge_intent:
      from_previous: "continuing walk forward from shot_02 same speed"
      to_next: "POV approaches doorway visible in next shot"
    pov_traversal: walking_forward | descending | ascending | approaching | turning | static_with_micro_bob
    audio_layer_continuity: [drone_base, ambient_corridor]  # layers MUST sustain across cut
    visual_style_lut: warm_industrial_v2  # same LUT shot N + N+1 within section
    motion_type: hand_close_up | full_body_action | walking | etc  # for Hailuo Pro tier auto-select
    hero: true|false  # for tier escalation

narrative_sections:
  - section_id: pre_decision
    shot_ids: [shot_01..shot_06]
    audio_layer_continuity_within_section: [drone_base, ambient_corridor]
    visual_style_lut: warm_industrial
```

---

## 📋 User interview prompts forward (for architect to use)

Architect, when launching FASE 0 interview with user for video #3, recommended questions:

### Genre + delivery (existing protocol)
- Pattern preference P1-P10 (check `horror-choice-format/video-log.md` for rotation — DON'T repeat P3 cinema o P6 matadero)
- Setting concept (which setting NEW? Backrooms-style preferred per user perceptual showing 10/10 to backrooms refs)
- Character dyad (malo aparente + bueno aparente)
- Cliffhanger archetype
- Counterfactual placement: BEFORE choice OR twin/relief (NOT AFTER retrospective)

### NEW questions critical for video #3 quality push

1. **"¿Cuál es la JOURNEY física del viewer?"**
   - User must describe shot 1 → shot 2 → shot 3 ... in terms of PHYSICAL MOTION
   - Example: "Estoy en biblioteca abandonada → camino hacia el fondo → encuentro figura → me ofrece libro → tomo el libro → me transformo"
   - NOT shot list. NOT story beats. PHYSICAL JOURNEY where each shot transitions via motion.

2. **"¿Cuáles son los AUDIO layers de fondo continuos?"**
   - Per § 8.11: drone_base + ambient_section + accent_events
   - User describes: "drone_base = órgano lejano sostenido todo el video", "ambient_section_1 = corredor susurros", "ambient_section_2 = sala de lectura papeles"

3. **"¿Hay character speech on-screen?"** (lip-sync trigger)
   - Si SÍ → lip-sync needed (Hedra $1.50/video OR Veo if enterprise)
   - Si NO → narrator off-screen only, no lip-sync needed

4. **"¿Lip-sync presupuesto OK?"**
   - User confirms +$1.50/video (Hedra) acceptable OR uses Veo 3.1 enterprise free if available

5. **"¿Target perceptual?"** (calibrated Gemini v4 gate)
   - User confirms target: gemini_calibrated_v4 ≥9.0 OR user_perceptual ≥8.5
   - This becomes ship gate instead of old Gemini holístico ≥9.7

---

## 🎯 Expected video #3 outcomes (forward projections)

```
With Phase 2 architecture + v4 calibrated Gemini + GAP #40 EXECUTION CONTINUITY focus:

Target metrics:
  iter_count: 1-3 (vs matadero 8, cinema 6) ← 50-65% reduction
  cost: $8-9 (vs $14-16) ← 40-50% reduction
  user_perceptual: ≥9.0 (vs 7.85 baseline) ← +1.15 perceptual jump
  gemini_calibrated_v4: ≥9.0 (matches user perceptual)
  Δ_calibrated: ≤0.5 (within ±0.5 confidence interval)
  
Bug classes eliminated structurally:
  ✓ Sync drift (per-clip atomic)
  ✓ Caption fragmentation
  ✓ Same-Y overlap
  ✓ Audio mismatch boundaries
  ✓ SFX context-blind reuse
  ✓ AVU GSAP offsets
  ✓ Cumulative timeline error
  ✓ Editorial transition variety (effects library 10 transitions)
  
Bug classes addressed via NEW amendments (NOT yet eliminated structurally):
  ⚠ Lip-sync precision (Phase 3 Hedra/Veo integration)
  ⚠ EXECUTION CONTINUITY ← NEW PRIMARY FOCUS
  ⚠ AI artifacts hands (Hailuo Pro escalation)
  ⚠ Character morphing (anchor STRICT all shots)
```

---

## 📍 Required reads for architect (in order)

When you start video #3 SPEC design:

1. **THIS DOC** (ARCHITECT-BRIEFING-VIDEO-3.md) — overview new amendments
2. **CLAUDE.md** Hard Rule #23 (per-clip atomic mandatory) + new updates
3. **PAUTA-MASTER.md** § 18-25 (decision UI, traversal, character, atmosphere, cuts/min, counterfactual, music)
4. **INGENIERO-PAUTA-MASTER.md § 8.10-8.17** (per-clip atomic implementation + 6 amendments + GAP #40 EXECUTION CONTINUITY + lip-sync § 8.17)
5. **GAPS-LOG.md** — 35 gaps. **GAP #40 ⭐⭐ PRIMARY**
6. **TASTE-LOG.md** entry #1 (Tomás perceptual baseline 7.85, target 9+, EXECUTION CONTINUITY as X factor)
7. **health-dashboard.md** (gemini_calibrated_v4 architecture + matadero outlier resolved)
8. **video-log.md** — pattern rotation (DON'T repeat P3 cinema o P6 matadero)

---

## 🤝 Handoff protocol

This briefing is filesystem-based per memory `feedback_3_terminal_separation`. Architect picks up + reads autonomously when ready to launch video #3.

NO direct invocation. Architect works in terminal 2 independently.

User triggers architect by: "hagamos un video nuevo" or similar. Architect reads this briefing + autoridad canónica + starts FASE 0 interview.

---

## ⏭️ Status (2026-05-21 PM late)

```
✅ TAREA A: GAP #40 logged + #23/#26/#27 revised + tally updated
✅ TAREA C: lip-sync investigated + INGENIERO-PAUTA § 8.17 NEW + cost model reset
✅ TAREA B: this briefing prepared for architect terminal 2

Sistema READY for video #3 launch when user triggers.
Architect cargo this briefing + ejecuta autonomously.
```

---

**Authored by**: Auditor (terminal 3, 2026-05-21 PM late)
**For**: Architect (terminal 2)
**User decision points pending**:
1. ✅ Verify Gemini enterprise covers Veo 3.1 → CONFIRMED 2026-05-21 PM
2. ✅ Run Veo test bench → COMPLETED 2026-05-21 PM late. **ALL 4 PASS** including horror content + character speech with verified lip-sync. **Scenario A applies — video #3 ~$0 cost forward.**
3. **Trigger video #3 architect interview when ready** — sistema completamente listo.

### Test bench summary (2026-05-21 PM late)

```
Veo 3.1 capabilities VERIFIED via production test:
  ✅ Accepts horror/uncanny content (no NSFW reject for our genre)
  ✅ Generates 6s 9:16 native vertical
  ✅ Native AAC audio bundled in mp4
  ✅ Native lip-sync (Whisper verified dialog match)
  ✅ ~64-80s latency per clip
  ✅ Cost $0 enterprise
  ✅ Image-ref (character anchor) 8.5/10 identity preservation
  
Production script ready: scripts/veo3.py (3-tier + image-ref support)
```

---

## ⭐⭐ V3 PRIMARY DIRECTIVE — Longer clips + per-clip atomic anti-matadero strategy

**User creative direction codified 2026-05-21 PM late** post Phase 3 + GAP #40 codification:

> "Super relevante que no nos pase lo de matadero — cortes de un clip a otro sin relación.
> Hacer clips más largos + ocupar la estructura de clips para no caer en problemas de edición.
> Execution debe seguir las 10 reglas (dimensiones calibrated v4)."

### Strategy: fewer clips, longer duration, internal motion within each

**Shot count target V3**:

```
Total duration target: 90s
OLD strategy (matadero/cinema pattern): ~22 shots × 4s avg = 22 cuts (~14-15 cuts/min)
NEW strategy (V3 forward): ~12-16 shots × 6-8s avg = 11-15 cuts (~8-10 cuts/min)

NET: ~30-50% fewer cut points = ~30-50% fewer teleport opportunities
```

**Per-shot duration distribution proposed**:

| Section | Duration | Shot count | Avg/shot | Rationale |
|---------|---------:|:---:|---------:|-----------|
| Hook (0-9s) | 9s | **1 shot** | 9s | Entire hook in ONE clip with internal motion (POV in lobby + walk + reveal characters + countdown) |
| Setup pre-decision (9-30s) | 21s | 3 shots | 7s | POV traversal walk through space (corridor → encounter → approach) |
| Decision UI (30-35s) | 5s | 1 shot | 5s | Freeze + VHS filter + countdown 3-2-1 |
| Counterfactual relief OR Path B (35-45s) | 10s | 1-2 shots | 5-10s | "Si elegiste X" with full counterfactual journey |
| Path A consequence (45-83s) | 38s | 5-6 shots | 6-8s | Climax + reveal + cliffhanger setup with internal POV motion |
| Outro card (83-90s) | 7s | 1 shot | 7s | AVU outro card sustained |
| **TOTAL** | **90s** | **12-14 shots** | **6.4-7.5s avg** | **8-9 cuts/min** |

### Trade-off explicit (architect must accept)

**LOWER cuts/min than canonical band 14-22**:
- Canonical refs use 14-22 cuts/min — V3 strategy uses 8-10 cuts/min
- **This is intentional** — fewer cuts = fewer teleport-opportunities
- Cuts/min canonical band was to detect SLOW PACING (matadero 12 = drag)
- BUT cinematic quality matters MORE than cut frequency
- **Better 10 cuts BIEN BRIDGED than 20 cuts con 5 teleports**

### How "internal motion within shots" works

Each long shot must encode a **journey within the clip**:

```
Example shot_02 (6s walking through corridor):
  Second 0-2: POV at corridor start, dim lights, slow walk begins
  Second 2-4: POV continues forward, lights flicker, approaching figure
  Second 4-6: POV closer to figure, character visible, stop motion
  
= 1 Veo clip 6s with internal kinetic momentum
= Equivalent to 3 short clips cut together
= But ZERO teleport opportunities (no cuts within)
```

Veo 3.1 prompt template for journey-within-clip:

```
"POV first-person walking forward through dim industrial corridor.
Second 0-2: slow steady pace, peripheral details (wallpaper, dust).
Second 2-4: continue forward, dim figure visible at end of corridor.
Second 4-6: POV closer, figure raises hand defensively.
Atmospheric horror, warm tungsten flicker, dust particles in beams.
Single continuous camera motion forward, no cuts."
```

### CUTS BETWEEN SHOTS must follow motion bridge rules

Per SPEC v10 `motion_bridge_intent` field + INGENIERO-PAUTA § 8.16:

```
Cut shot_01 → shot_02:
  from_previous: "POV at countdown end, micro-pause moment"
  to_next: "POV begins walking forward from same position"
  
  At edit point: ZERO frames of inactivity. Cut from countdown final
  frame DIRECTLY to walking motion start. Audio drone continuous bridges.
```

### Per-clip atomic structure prevents editing bugs

```
Each shot = self-contained:
  ├── Veo 3.1 visual (6-8s with native audio)
  ├── Caption sidecar JSON (scope-limited)
  ├── Cross-clip music Layer 3 (drone_base continuous)
  └── No reliance on global timeline
  
Cuts between clips:
  ├── effect_NN_to_NN+1.mp4 (transition file with audio sting)
  ├── motion_bridge between shots
  └── Audio Layer 3 sustains drone across boundary
  
Per-clip Quality Gate Agent validates EACH clip before assembly.
Gemini Vision mid-exec hook validates EACH transition.
```

### Architect compliance checklist for V3 SPEC

When writing SPEC v10:

```
□ Total shots ≤16 (was 22+ in matadero/cinema)
□ Avg shot duration ≥6s (was ~4s previously)
□ Hook = 1 SHOT (not 2-3 with cuts)
□ Each shot has motion_bridge_intent.from_previous + to_next FILLED
□ Each shot has pov_traversal explicitly (not default static)
□ Audio Layer 3 (drone_base) spans 0-90s in music_continuous_layers
□ Visual_style_lut consistent within each narrative_section
□ NO shot exceeds Veo 3.1 max ~8s per generation
□ Counterfactual placement: NOT after_both_paths_retrospective
□ All 10 calibrated v4 dimensions addressed in SPEC design notes
```

### 10 calibrated v4 dimensions checklist (architect compliance)

Per AUTONOMOUS-FACTORY-ROADMAP.md § 10.5.2:

```
1. EXECUTION CONTINUITY (30%) — motion bridges, audio bridges, LUT consistency, kinetic momentum
2. INMERSIÓN POV literal (15%) — POV hands as viewer-is-character
3. SOUND DEPTH (15%) — 3-4 music layers per § 8.11
4. ATMOSPHERE coherence (10%) — ≥3 atmospheric motions per shot
5. CHARACTER signature (10%) — uncanny silueta DISTINCT + active gestures
6. STORY LOGIC CONTINUITY (5%) — narrative chain + counterfactual placement canonical
7. EDITING modulation (5%) — pacing modulates between sections (slow dialogue → fast climax)
8. HOOK 0-9s (5%) — scroll-stop visual + audio + uncanny
9. CAPTIONS (3%) — canonical style (drop-shadow + monospaced names + warning red)
10. NARRATIVE comprehension (2%) — clear dilemma + counterfactual logic
```

Every SPEC v10 shot must contribute to at least 5-6 of these 10 dimensions through deliberate design choices.
