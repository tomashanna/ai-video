# EXCALIDRAW SYSTEM OVERVIEW — Multi-capa

> **Propósito**: doc jerárquico parseable por agente Excalidraw (MCP) en chat separado → diagrama visual multi-capa del sistema completo pre-V5.
>
> **Audiencia**: compañeros técnicos. Cubre Capa A agnostic + Capa B horror-choice activa + Capa C cerro-aislado-v4 D38 + forward placeholders (Marina, Sprint B/M).
>
> **Estado**: post Sub-fase 3A CERRADA + Paso 4 sequence COMPLETE + 9 validators built + Sync.so workflow ready. V5 ship readiness: PIPELINE validado, voice A/B pending Tomás.
>
> **Fecha**: 2026-05-27.

---

## Legend — colores, nodos, edges

### Colores per layer / capa
| Color | Meaning |
|---|---|
| 🔵 **Blue** | Capa A — agnostic universal (`ai-video-production/`) |
| 🟢 **Green** | Capa B — format-specific active (`horror-choice-format/`) |
| 🟡 **Amber** | Capa C — per-video active (`cerro-aislado-v4/` D38, V5+) |
| ⚪ **Gray** | Forward / placeholders (Marina, Sprint B/M pending, Hedra V6+) |
| 🔴 **Red** | Decisor / human gates |
| 🟠 **Orange** | Auditor (Claude Code) role |
| 🟣 **Violet** | Claude conversacional (estratega, NO ejecutor) |
| 🔷 **Cyan** | Validators / gates programáticos |

### Node types
| Type | Notation | Examples |
|---|---|---|
| `ROLE` | hexagon | Tomás, Claude conv, Auditor |
| `PROC` | rounded rect | CP1 anchors, CP4 Hailuo |
| `SCRIPT` | rect | `build-video-hybrid.py`, `audit-spec-narrative-coherence.py` |
| `DOC` | parallelogram | `CLAUDE.md`, `PIPELINE.md`, `PAUTA-MASTER.md` |
| `ASSET` | cylinder | atomic clips, recipes JSON, music mp3 |
| `GATE` | diamond | D17 lip_sync_required, Pattern 7 capability check |
| `DECISION` | diamond | branch (effects vs passthrough) |
| `PLACEHOLDER` | dashed rect | Marina format slot, Hedra V6+ |
| `PRINCIPLE` | circle | Agnóstico, Automatizable, Escalable, Sólido |

### Edge types
| Edge | Notation | Meaning |
|---|---|---|
| `produces` | →  (solid) | A genera output B |
| `consumes` | →  (solid) | B usa A como input |
| `validates` | ⇢ (dashed) | A valida B (gate) |
| `depends_on` | ⤇ (dotted) | A requiere B presente/correcto |
| `governs` | ⊳ (thick) | autoridad/regla aplica a |
| `frozen_ref` | 🔒 (lock) | referencia inmutable D38 |
| `pending` | ⏳ (clock) | forward, no construido |

---

## LAYER 1 — Roles, comms, principios canonical

### Nodes — Layer 1
```
[L1.tomas]           Tomás                    (ROLE 🔴, decisor + override + listen test)
[L1.claude_conv]     Claude conversacional    (ROLE 🟣, estratega — NO ejecuta tools)
[L1.auditor]         Auditor (Claude Code)    (ROLE 🟠, architect + engineer + run scripts)

[L1.p1_agnostic]     Principio 1: Agnóstico   (PRINCIPLE 🟦)
[L1.p2_automatable]  Principio 2: Automatizable (PRINCIPLE 🟦)
[L1.p3_escalable]    Principio 3: Escalable   (PRINCIPLE 🟦)
[L1.p4_solido]       Principio 4: Sólido (filesystem = ground truth) (PRINCIPLE 🟦)

[L1.ground_truth]    Filesystem repo          (DOC 🔵, source of truth canonical)
[L1.freeze_manifest] _freeze-manifests/v4-baseline.md5 (DOC 🔵, D38 verifiability estructural)

[L1.p7_capability]   Pattern 7: Capability Matrix (PRINCIPLE 🟦, applicable/not_applicable/pass/fail)
[L1.bug9]            Bug #9: video_capabilities missing → HALT (PRINCIPLE 🟦)
[L1.hr14_rotation]   HR#14: Pattern rotation per HR + GAP #10 canonical taxonomy (PRINCIPLE 🟦)

[L1.disponibilidad_uso]  "Disponibilidad ≠ Uso" (PRINCIPLE 🟦, tiered catalogs canonical)
```

### Edges — Layer 1
```
[L1.tomas]          ⊳ [L1.claude_conv]      : "delegates strategy"
[L1.tomas]          ⊳ [L1.auditor]          : "approves cascades + override authority"
[L1.claude_conv]    → [L1.tomas]            : "proposes plans (user decides)"
[L1.claude_conv]    → [L1.auditor]          : "structures messages, NEVER spawns agents"
[L1.auditor]        → [L1.tomas]            : "reports honest + escalates ambiguity (Bug #9)"
[L1.auditor]        → [L1.ground_truth]     : "reads + writes filesystem"

[L1.p1_agnostic]    ⊳ [L1.auditor]          : "guides --format REQUIRED in all builds"
[L1.p2_automatable] ⊳ [L1.auditor]          : "scripts > docs theater"
[L1.p3_escalable]   ⊳ [L1.auditor]          : "capability-gating per Pattern 7"
[L1.p4_solido]      ⊳ [L1.ground_truth]     : "filesystem = canonical, NOT memory"
[L1.p4_solido]      ⊳ [L1.freeze_manifest]  : "D38 verifiability estructural"

[L1.p7_capability]  ⊳ [Layer 2 validators]  : "applicable/not_applicable/pass/fail per cap flag"
[L1.bug9]           ⊳ [Layer 2 validators]  : "exit 2 if video_capabilities missing"
[L1.hr14_rotation]  ⊳ [Layer 4 video-log]   : "no repeat pattern 2 videos consecutivos"
[L1.disponibilidad_uso] ⊳ [Layer 3 transitions/ global tiered] : "universal available ≠ prescribed"
```

---

## LAYER 2 — Pipeline CP-by-CP end-to-end

### Nodes — Layer 2 (PROC chain + outputs + validators)

#### CP0 — SPEC creation (architect)
```
[L2.cp0_brief]       Tomás brief V5             (PROC, decisor input — historia/setting/etc)
[L2.cp0_pauta]       PAUTA-MASTER consult       (DOC 🟢, P1/P2/P3/P6/P9 canonical empíricos)
[L2.cp0_videolog]    video-log consult          (DOC 🟢, rotation HR#14 + cross-video uniqueness)
[L2.cp0_taste_log]   TASTE-LOG horror-choice    (DOC 🟢, anti-cliché + Tomás gusto)
[L2.cp0_spec_emit]   creative-specs/v5.yaml     (DOC 🟡, output SPEC v11.1)
[L2.cp0_d14_d22]     Architect D14-D22 self-audit (GATE 🔷, POV count + Si elegiste + visual match + scene_context)
[L2.cp0_spec_audit]  SPEC-AUDIT charter (Gate 5) (GATE 🔷, ≥5/8 refs canonical + MODEL-BEHAVIOR-LOG)
[L2.cp0_narrative]   audit-spec-narrative-coherence.py (GATE 🔷, BUILD 4 — structure + cross-video + anti-cliché)
[L2.cp0_l1_wpm]      audit-spec-narration-fits-duration.py (GATE 🔷, BUILD 5 Sprint M L1)
[L2.cp0_lip_marks]   audit-spec-lip-sync-marks.py (GATE 🔷, BUILD 8 — coverage + consistency)
```

#### CP1 — Reference Anchors
```
[L2.cp1_anchors]     Gemini Nano Banana STRICT  (PROC, image generation; 6-finger + signature features)
[L2.cp1_anchor_assets] anchors/<char>_v1.png + locus anchors (ASSET 🟡)
[L2.cp1_audit]       Auditor: visual + cross-anchor consistency + premium prompt 5-block + cost (GATE 🔷)
[L2.cp1_mbl_check]   MODEL-BEHAVIOR-LOG verify (GATE 🔷, face/stability/pose-coupling Gemini constraints)
```

#### CP2 — TTS narration
```
[L2.cp2_tts]         ElevenLabs v3 (TTS)        (PROC, voice = Eleguar/José pending A/B Tomás)
[L2.cp2_tts_assets]  assets/tts/<shot>_narrator.mp3 (ASSET 🟡)
[L2.cp2_m7]          M7 acoustic verify (Whisper re-transcribe + per-segment WPM + intelligibility ≥0.90) (GATE 🔷)
[L2.cp2_l2_duration] audit-tts-vs-spec-duration.py (GATE 🔷, BUILD 6 Sprint M L2)
[L2.cp2_listen]      Tomás listen test          (GATE 🔴, Rule D PRECEDENCE)
```

#### CP3 — Shot images
```
[L2.cp3_shots]       Gemini --ref shot generation (PROC, anchor + scene_context)
[L2.cp3_shot_assets] shots/<shot>.png            (ASSET 🟡)
[L2.cp3_audit]       Auditor: character consistency + variantes + paleta + setup timing + atmospheric motions (GATE 🔷, D28)
```

#### CP4 — Hailuo Std animation
```
[L2.cp4_hailuo]      MiniMax Hailuo Std i2v     (PROC, image-to-video motion AI)
[L2.cp4_clip_assets] clips/<shot>.mp4 (raw)     (ASSET 🟡)
[L2.cp4_dry_run]     Dry-run gate (1 shot sample audit pre-cascade) (GATE 🔷)
[L2.cp4_manifest]    A4 manifest schema (cost + tier + timestamp + prediction_id) (GATE 🔷)

[L2.cp45_sync_so]    CP4.5 Sync.so post-process (PROC, NEW — only shots lip_sync_required:true)
[L2.cp45_lipsync_assets] clips/<shot>_lipsync.mp4 (ASSET 🟡)

[L2.cp46_atomic_mux] CP4.6 build_clip_atomic.py (PROC, visual + audio + captions baked per Hard Rule #23)
[L2.cp46_atomic_assets] clips-atomic/<shot>_atomic.mp4 (ASSET 🟡)
[L2.cp46_quality_gate] quality_gate_per_clip.py (GATE 🔷, per-clip ≥9.0 PASS / 7.0-8.9 iterate / <7.0 escalate)
[L2.cp46_midexec]    gemini_midexec_vision.py hooks (GATE 🔷, hailuo_post/tts_post/atomic_post/transition_post)
```

#### CP5 — Hybrid assembly + final master
```
[L2.cp5_4_2_concat]  4.2 concat-clips-with-audio.py (PROC 🔵, Layer 1 concat → clips_concat_only.mp4)
[L2.cp5_4_4_effects] 4.4 apply-effects-between-clips.py (PROC 🔵, Layer 2 xfade + stings → clips_with_effects.mp4)
[L2.cp5_4_3_music]   4.3 apply-cross-clip-music.py (PROC 🔵, Layer 3 music + sidechain duck + final master -14 LUFS)
[L2.cp5_4_1_orch]    4.1 build-video-hybrid.py (PROC 🔵, orchestrator — Layer 4 UI overlay + fps norm + 8 gates)
[L2.cp5_draft]       renders/draft-vN.mp4 + _gates.json + _manifest.json (ASSET 🟡)
[L2.cp5_8_gates]     8 pre-render gates (duration / LUFS / dBTP / resolution / fps / caption / layers / frames) (GATE 🔷)
[L2.cp5_hf_ui]       HyperFrames UI overlay (countdown / decision UI / outro / watermark) (PROC, project-specific)
```

#### Final
```
[L2.human_checklist] Tomás HUMAN-CHECKLIST 7 Q gestalt (GATE 🔴, perceptual)
[L2.publish]         Publish @elige_tucompanero (PROC, manual anti-ban)
```

### Edges — Layer 2 chain
```
[L2.cp0_brief]      → [L2.cp0_pauta]         : "consults"
[L2.cp0_brief]      → [L2.cp0_videolog]      : "consults"
[L2.cp0_brief]      → [L2.cp0_taste_log]     : "consults"
[L2.cp0_pauta]      → [L2.cp0_spec_emit]     : "informs"
[L2.cp0_videolog]   → [L2.cp0_spec_emit]     : "informs (rotation HR#14)"
[L2.cp0_taste_log]  → [L2.cp0_spec_emit]     : "informs (anti-cliché)"
[L2.cp0_spec_emit]  ⇢ [L2.cp0_d14_d22]       : "validated by"
[L2.cp0_spec_emit]  ⇢ [L2.cp0_spec_audit]    : "validated by (≥5/8 refs)"
[L2.cp0_spec_emit]  ⇢ [L2.cp0_narrative]     : "validated by (BUILD 4)"
[L2.cp0_spec_emit]  ⇢ [L2.cp0_l1_wpm]        : "validated by (Sprint M L1)"
[L2.cp0_spec_emit]  ⇢ [L2.cp0_lip_marks]     : "validated by (BUILD 8)"
[L2.cp0_spec_emit]  → [L2.cp1_anchors]       : "feeds anchor prompts"

[L2.cp1_anchors]    → [L2.cp1_anchor_assets] : "produces"
[L2.cp1_anchor_assets] ⇢ [L2.cp1_audit]      : "validated by"
[L2.cp1_anchor_assets] ⇢ [L2.cp1_mbl_check]  : "validated by (face/stability/pose)"
[L2.cp1_anchor_assets] → [L2.cp3_shots]      : "--ref source"

[L2.cp0_spec_emit]  → [L2.cp2_tts]           : "feeds narrator_text per shot"
[L2.cp2_tts]        → [L2.cp2_tts_assets]    : "produces mp3"
[L2.cp2_tts_assets] ⇢ [L2.cp2_m7]            : "validated by"
[L2.cp2_tts_assets] ⇢ [L2.cp2_l2_duration]   : "validated by (BUILD 6 Sprint M L2)"
[L2.cp2_tts_assets] ⇢ [L2.cp2_listen]        : "validated by (Rule D)"

[L2.cp1_anchor_assets] → [L2.cp3_shots]      : "consumes (anchor --ref)"
[L2.cp3_shots]      → [L2.cp3_shot_assets]   : "produces"
[L2.cp3_shot_assets] ⇢ [L2.cp3_audit]        : "validated by"
[L2.cp3_shot_assets] → [L2.cp4_hailuo]       : "feeds Hailuo i2v"

[L2.cp4_hailuo]     → [L2.cp4_clip_assets]   : "produces"
[L2.cp4_clip_assets] ⇢ [L2.cp4_dry_run]      : "validated by (pre-cascade)"
[L2.cp4_clip_assets] ⇢ [L2.cp4_manifest]     : "schema verified"
[L2.cp4_clip_assets] → [L2.cp45_sync_so]     : "if lip_sync_required=true"
[L2.cp45_sync_so]   → [L2.cp45_lipsync_assets] : "produces"
[L2.cp45_lipsync_assets] → [L2.cp46_atomic_mux] : "consumed"
[L2.cp4_clip_assets] → [L2.cp46_atomic_mux]  : "consumed (when lip_sync false)"
[L2.cp2_tts_assets] → [L2.cp46_atomic_mux]   : "consumed (per-clip audio)"
[L2.cp46_atomic_mux] → [L2.cp46_atomic_assets] : "produces"
[L2.cp46_atomic_assets] ⇢ [L2.cp46_quality_gate] : "validated by"
[L2.cp46_atomic_assets] ⇢ [L2.cp46_midexec]  : "validated by (4 hooks)"

[L2.cp46_atomic_assets] → [L2.cp5_4_2_concat] : "Layer 1 input"
[L2.cp5_4_2_concat] → [L2.cp5_4_4_effects]  : "concat_only.mp4"
[L2.cp5_4_4_effects] → [L2.cp5_4_3_music]   : "clips_with_effects.mp4"
[L2.cp5_4_3_music]  → [L2.cp5_4_1_orch]     : "master_final.mp4"
[L2.cp5_4_1_orch]   → [L2.cp5_draft]        : "produces draft-vN.mp4"
[L2.cp5_draft]      ⇢ [L2.cp5_8_gates]      : "validated by"
[L2.cp5_hf_ui]      → [L2.cp5_4_1_orch]     : "Layer 4 overlay (optional)"

[L2.cp5_draft]      ⇢ [L2.human_checklist]  : "perceptual gate"
[L2.human_checklist] → [L2.publish]          : "if all PASS"
```

---

## LAYER 3 — Code organization Capa A / B / C

### Capa A — agnostic universal (Blue 🔵)

#### Subgroup: 4 Paso 4 builds (orchestrator + chain)
```
[L3.A.script_4_1]    build-video-hybrid.py        (SCRIPT 🔵, Paso 4.1 orchestrator final)
[L3.A.script_4_2]    concat-clips-with-audio.py   (SCRIPT 🔵, Paso 4.2 Layer 1)
[L3.A.script_4_3]    apply-cross-clip-music.py    (SCRIPT 🔵, Paso 4.3 Layer 3 + master)
[L3.A.script_4_4]    apply-effects-between-clips.py (SCRIPT 🔵, Paso 4.4 Layer 2)
```

#### Subgroup: Validators (Sprint M + narrative coherence)
```
[L3.A.script_narrative] audit-spec-narrative-coherence.py (SCRIPT 🔵, BUILD 4 — sentence-transformers)
[L3.A.script_l1_wpm]    audit-spec-narration-fits-duration.py (SCRIPT 🔵, BUILD 5)
[L3.A.script_l2_dur]    audit-tts-vs-spec-duration.py (SCRIPT 🔵, BUILD 6)
[L3.A.script_lip_marks] audit-spec-lip-sync-marks.py (SCRIPT 🔵, BUILD 8)
[L3.A.script_recipes]   test_effects_library_recipes_schema.py (SCRIPT 🔵, schema validator)
```

#### Subgroup: Pre-V4 enforcement (Sprint A — Scripts A/B/C)
```
[L3.A.script_build_atomic] build_clip_atomic.py (SCRIPT 🔵, Script A — per-clip atomic + caption burn)
[L3.A.script_audit_b]      audit-shot-spec-compliance.py (SCRIPT 🔵, Script B — per-shot 8-dim)
[L3.A.script_orchestrator] orchestrator-cp-by-cp.py (SCRIPT 🔵, Script C — CP gates state machine)
[L3.A.script_quality_gate] quality_gate_per_clip.py (SCRIPT 🔵)
[L3.A.script_midexec]      gemini_midexec_vision.py (SCRIPT 🔵, 4 hooks)
```

#### Subgroup: lib helpers
```
[L3.A.lib_adapter]   spec_transitions_adapter.py (SCRIPT 🔵, V4 legacy → per-shot canonical normalizer)
[L3.A.lib_similarity] similarity.py             (SCRIPT 🔵, Script A helper)
[L3.A.lib_state]      orchestrator_state.py     (SCRIPT 🔵, Script C helper)
[L3.A.lib_hard_rules] hard_rules_parser.py      (SCRIPT 🔵)
```

#### Subgroup: Generation scripts
```
[L3.A.script_tts]    tts.py    (SCRIPT 🔵, ElevenLabs wrapper)
[L3.A.script_image]  image.py  (SCRIPT 🔵, Gemini Nano Banana wrapper)
[L3.A.script_sfx]    sfx.py    (SCRIPT 🔵, ElevenLabs SFX wrapper)
[L3.A.script_video]  video.py  (SCRIPT 🔵, Replicate Hailuo/Veo wrapper)
[L3.A.script_captions] captions.py (SCRIPT 🔵, Whisper)
[L3.A.script_veo3]   veo3.py    (SCRIPT 🔵, Veo 3.1 wrapper)
```

#### Subgroup: Audit scripts (older)
```
[L3.A.audit_against_ref]   audit-against-referent.py (SCRIPT 🔵, F1 bands)
[L3.A.audit_audio]         audit-audio.py (SCRIPT 🔵)
[L3.A.audit_frames]        audit-frames.py (SCRIPT 🔵, Gemini Vision)
[L3.A.audit_frames_g]      audit-frames-granular.py (SCRIPT 🔵, sentinels S1-S10)
[L3.A.audit_narrative]     audit-narrative.py (SCRIPT 🔵)
[L3.A.audit_spec_complete] audit-spec-completeness.py (SCRIPT 🔵, Gate 0)
[L3.A.audit_calibrated]    audit-gemini-calibrated.py (SCRIPT 🔵, calibrated v4)
[L3.A.qa_gate]             qa-gate.py (SCRIPT 🔵)
[L3.A.render_lock]         render-lock.py (SCRIPT 🔵)
[L3.A.continuity_check]    continuity-check.py (SCRIPT 🔵)
[L3.A.sync_check]          sync-check.py (SCRIPT 🔵)
```

#### Subgroup: Templates + assets agnostic
```
[L3.A.spec_template]   CREATIVE-SPEC-TEMPLATE-v11.yaml (DOC 🔵, SPEC v11.1 schema canonical)
[L3.A.effects_universal] transitions/universal/transitions/ (11 primitives, global root) (ASSET 🔵)
[L3.A.audio_stings_A]    transitions/universal/audio-stings/ (whoosh + drone + flash-sharp) (ASSET 🔵)
[L3.A.caption_styles]    caption-styles/caption-burn-template.css (DOC 🔵, 3 classes universal mechanism)
[L3.A.calibrated_prompt] calibrated-gemini-prompt-v4.txt (DOC 🔵)
[L3.A.bootstrap]         BOOTSTRAP.md (DOC 🔵, §1.1 asset layout convention NEW)
[L3.A.pipeline]          PIPELINE.md (DOC 🔵, §13.9 HYBRID arch + §13.9.1.1 LAYER 2 I/O Finding #1)
[L3.A.model_benchmark]   MODEL-BENCHMARK.md (DOC 🔵, 35+ AI models + MODEL-BEHAVIOR-LOG)
[L3.A.model_behavior]    MODEL-BEHAVIOR-LOG.md (DOC 🔵, Gemini --ref constraints)
[L3.A.delivery_formats]  DELIVERY-FORMATS.md (DOC 🔵, matriz GENRE × FORMAT)
```

### Capa B — horror-choice format-specific (Green 🟢)

```
[L3.B.pauta_master]      PAUTA-MASTER.md (DOC 🟢, autoridad creativa empírica 8 refs)
[L3.B.ingeniero_pauta]   INGENIERO-PAUTA-MASTER.md (DOC 🟢, autoridad técnica empírica)
[L3.B.script_writing]    SCRIPT-WRITING-GUIDE.md (DOC 🟢, formato horror)
[L3.B.canonical_scenes]  canonical-scenes/ (8 refs frame-by-frame + INDEX) (ASSET 🟢)
[L3.B.video_log]         video-log.md (DOC 🟢, rotation + cross-video uniqueness schema NEW BUILD 3)
[L3.B.taste_log]         TASTE-LOG.md (DOC 🟢, Tomás gusto codificado)
[L3.B.creative_direction] creative-direction/ (aesthetic/animation/audio/camera/captions/etc) (DOC 🟢)
[L3.B.lip_sync_workflow] lip-sync-workflow.md (DOC 🟢, BUILD 8 — Hailuo Std + Sync.so workflow)
[L3.B.effects_subgenre]  transitions/horror-choice/transitions/ (4 sub-genre: film-burn/projector/static-noise/old_screen_glitch) (ASSET 🟢)
[L3.B.audio_stings_B]    transitions/horror-choice/audio-stings/ (projector-cue + drone-tension copy) (ASSET 🟢)
[L3.B.intro_formula]     INTRO-FORMULA.md (DOC 🟢, receta 9s canonical)
[L3.B.patterns]          PATTERNS.md (DOC 🟢, reglas técnicas)
[L3.B.character_names]   CHARACTER-NAMES-CATALOG.md (DOC 🟢)
[L3.B.bootstrap_horror]  BOOTSTRAP-NEW-PROJECT.md (DOC 🟢, FASE 0 inputs horror-choice)
```

### Capa C — per-video active (Amber 🟡)

```
[L3.C.cerro_v4]      cerro-aislado-v4/ D38 frozen (ASSET 🟡 🔒, V4 baseline reference)
[L3.C.cerro_spec]    creative-specs/cerro-aislado-v4.yaml (DOC 🟡 🔒, V4 SPEC frozen)
[L3.C.v5_placeholder] V5 (creative-specs/<v5-id>.yaml + <v5-project>/) (PLACEHOLDER ⚪ ⏳)
```

### Edges — Layer 3 cross-layer
```
[L3.A.spec_template] → [L3.C.cerro_spec]      : "schema parent"
[L3.A.spec_template] → [L3.C.v5_placeholder]  : "V5 SPEC uses v11.1 schema"
[L3.A.script_4_1]    ⤇ [L3.A.script_4_2]      : "depends on (subprocess chain)"
[L3.A.script_4_1]    ⤇ [L3.A.script_4_4]      : "depends on"
[L3.A.script_4_1]    ⤇ [L3.A.script_4_3]      : "depends on"
[L3.A.script_4_4]    ⤇ [L3.A.lib_adapter]     : "imports normalize_transitions"
[L3.A.script_4_4]    consumes [L3.A.effects_universal] : "Capa A primitives"
[L3.A.script_4_4]    consumes [L3.B.effects_subgenre]  : "Capa B sub-genre"
[L3.A.script_narrative] consumes [L3.B.video_log] : "cross-video uniqueness parse"
[L3.A.script_narrative] consumes [L3.B.pauta_master] : "P1-P9 canonical"
[L3.A.script_narrative] consumes [L3.B.taste_log] : "anti-cliché phrases (override)"
[L3.A.bootstrap]     ⊳ [Capa C V5 project setup] : "asset layout canonical"
[L3.A.pipeline]      ⊳ [L3.A.script_4_*]         : "governs HYBRID arch"

[L1.freeze_manifest] ⊳ [L3.C.cerro_v4]        : "verifies D38 unchanged"
[L1.freeze_manifest] 🔒 [L3.C.cerro_spec]      : "frozen ref"
```

---

## LAYER 4 — Detalle fino (effects tiered + Hard Rules + SPEC schema + Pattern 7)

### Effects-library TIERED (Cross-Capa, post-PRE-4.K)
```
[L4.tier_capa_A]     Capa A universal primitives (7) (ASSET 🔵)
                     - cross-fade-0.5s.json     (xfade=fade, literal)
                     - cross-fade-1.0s.json     (xfade=fade, literal)
                     - hard-cut-with-whoosh.json (hardcut, literal — workhorse 8/8 canonical)
                     - black-screen-0.3s.json   (fadeblack, approximate — concat-insert)
                     - fade-to-black-1.0s.json  (fadeblack, approximate — terminal fade)
                     - light-flash-impact.json  (fadewhite, approximate — climax)
                     - glitch-transition.json   (hlslice, literal — Decision 1.5 universal)

[L4.tier_capa_B]     Capa B horror sub-genre (3) (ASSET 🟢)
                     - film-burn-transition.json    (fadewhite, approximate — amber bloom)
                     - projector-cue-cinema.json    (fade, literal core — bloom dropped)
                     - static-noise-transition.json (dissolve, approximate — noise insert)

[L4.option_d_fields] xfade_transition + xfade_fidelity + native_mechanism_note (per recipe)
                     5 literal + 5 approximate (WARNING fires on approximate use in real run)

[L4.option_b_trigger] ⏳ Option B hybrid dispatch (transition_method enum) — TRIGGERS when SPEC uses approximate in production AND lossy reduction perceptually unacceptable
```

### Hard Rules canonical (15 capability-gated)
```
[L4.hr1]   Quality gate primario (Gemini ≥9.7 + audit-against-referent ≥85%) — gated has_ai_generated_clips
[L4.hr2]   Stop point pre-animation ≥9.7 — gated has_ai_generated_clips
[L4.hr3]   Captions Whisper, NUNCA hand-timed — gated has_captions_baked
[L4.hr4]   UI safe zones IG Reel (caption Y62 / loading Y52 / name Y11.5) — gated format_type reel/interactive_choice
[L4.hr5]   Variantes -a/-b/-c en shots >4s — gated has_ai_generated_clips
[L4.hr6]   ⛔ Primeros 30s = animation AI obligatoria — gated has_ai_generated_clips AND interactive_choice/reel
[L4.hr7]   Animation AI preferred (Ken Burns fallback ≤20%) — gated has_ai_generated_clips
[L4.hr8]   Capa SFX dedicada — gated has_sfx_layer
[L4.hr9]   Mix volumes canonical (narrador 1.0 / música 0.05-0.18 / SFX 0.20-0.35) — gated audio_mix_target lufs_-14
[L4.hr10]  Atempo 2x sobre TTS — gated has_tts_narration
[L4.hr11]  Render lock entre agentes (FFmpeg SIGTERM mitigation) — universal
[L4.hr12]  Plot twist coherente — gated interactive_choice format
[L4.hr13]  Audio coverage ≥70% + sound fabric ≥99% — gated has_tts_narration AND has_layer_3_music
[L4.hr14]  Rotación pattern HR#14 (NO repeat 2 consecutivos) — horror-choice format
[L4.hr15]  HyperFrames timeline namespace — universal
[L4.hr16]  data-duration > clip real → negro total — universal
[L4.hr17]  Plan-First Rule — universal
[L4.hr18]  Template ships 2 pautas paired — universal
[L4.hr19]  Nuestras producciones NO autoridad técnica — universal (measure-not-estimate)
[L4.hr20]  Modelo barato = prompt premium quality — gated has_ai_generated_clips
[L4.hr21]  SPEC storyboard-level obligatorio — universal
[L4.hr23]  Per-clip atomic assembly canonical V3+ — gated has_ai_generated_clips
[L4.hr24]  Auditor enforce CP-by-CP gates MANDATORY — universal
[L4.hr25]  HYBRID architecture canonical V4+ — gated has_captions_baked
[L4.hr26]  Tests adversariales obligatorios forward — universal
```

### SPEC schema v11.1 — video_capabilities §1.6
```
[L4.cap_source_origin]     source_clips_origin: ai_generated | pre_existing | mixed
[L4.cap_ai_gen]            has_ai_generated_clips: bool
[L4.cap_tts]               has_tts_narration: bool
[L4.cap_voiceover]         has_human_voiceover: bool
[L4.cap_audio_target]      audio_mix_target: lufs_-14 | spec_declared | preserve_source | none
[L4.cap_sfx]               has_sfx_layer: bool
[L4.cap_captions]          has_captions_baked: bool
[L4.cap_layer2]            has_layer_2_effects: bool (Pattern 7 gate Layer 2)
[L4.cap_layer3]            has_layer_3_music: bool (Pattern 7 gate Layer 3)
[L4.cap_layer4]            has_layer_4_ui: bool (Pattern 7 gate Layer 4)
[L4.cap_format_type]       format_type: interactive_choice | tutorial | b2b_commercial | compilation | other
[L4.cap_duration]          duration_intent_s: float
[L4.cap_target_fps]        target_fps: int (default 30, PRE-4.1 NEW)
[L4.cap_resolution]        output_resolution: WxH (default 1080x1920)
```

### Pattern 7 Capability Matrix methodology
```
[L4.p7_states]       4 states: applicable | not_applicable | pass | fail
[L4.p7_gating]       Hard Rules gated per capability flags (skip if false, not fail)
[L4.p7_bug9]         video_capabilities missing → Bug #9 exit 2 (NO silent paradigm assumption)
[L4.p7_audit_match]  Validators emit not_applicable for inactive capabilities — auditor checks correctness
```

### Cross-video uniqueness (BUILD 3 + BUILD 4)
```
[L4.cv_location]     SPEC `location` field — exact-match against prior video-log rows → FAIL on match
[L4.cv_staging]      SPEC `signature_staging` field — semantic similarity ≥0.85 → FAIL, [0.75,0.85) → FLAG
[L4.cv_verbs_skip]   Verbs (mata/apuñala/ahoga) — NO check (catálogo válido del formato)
[L4.cv_chars_skip]   Characters — NO check (repetibles cross-video)
[L4.cv_model]        sentence-transformers paraphrase-multilingual-MiniLM-L12-v2 (Spanish-aware, 384-dim, $0 offline)
[L4.cv_threshold]    block 0.85 / flag 0.75 (tuneable empíricamente post 5-10 videos)
```

### Audio tolerance bands (PRE-4.C dual source)
```
[L4.audio_canonical] Final master LUFS -14 ±0.5 (CANONICAL-ANCHORED F1: -14.06 ±0.41)
                     Dynamic range 14.49-22.34 dB (F1 measured)
                     Cuts/min 2-7 / 14-22 (per band)
[L4.audio_spec_decl] Per-layer pre-mix LUFS (SPEC-DECLARED, plumbing not F1):
                     drone_base -27 ±2, accent -25 ±2, ambient -30 ±2
                     Sidechain duck -8 ±1 dB (SPEC-declared)
                     dBTP headroom -1 ±0.3 (SPEC-declared)
```

### Edges — Layer 4
```
[L4.tier_capa_A]     ⊳ [L2.cp5_4_4_effects]   : "consumed (universal default)"
[L4.tier_capa_B]     ⊳ [L2.cp5_4_4_effects]   : "consumed (when --format horror-choice)"
[L4.option_d_fields] ⊳ [L2.cp5_4_4_effects]   : "WARNING on approximate use"
[L4.cv_model]        ⊳ [L3.A.script_narrative] : "sentence-transformers lazy-load"
[L4.cv_location]     ⊳ [L3.B.video_log]       : "parser regex extraction"
[L4.cv_staging]      ⊳ [L3.B.video_log]       : "parser + embedding compare"
[L4.audio_canonical] ⊳ [L2.cp5_4_3_music]     : "two-pass loudnorm target"
[L4.audio_canonical] ⊳ [L2.cp5_8_gates]       : "Gate 2 LUFS check"
[L4.hr14]            ⊳ [L3.B.video_log]       : "rotation check"
[L4.hr23]            ⊳ [L2.cp46_atomic_mux]   : "per-clip atomic mandatory"
[L4.hr25]            ⊳ [L2.cp5_*]             : "HYBRID architecture canonical"
[L4.cap_layer2]      ⊳ [L2.cp5_4_4_effects]   : "Pattern 7 branch (effects | passthrough)"
[L4.cap_layer3]      ⊳ [L2.cp5_4_3_music]     : "Pattern 7 branch (full | master_only | passthrough)"
[L4.cap_layer4]      ⊳ [L2.cp5_4_1_orch]      : "Pattern 7 branch (UI overlay | skip)"
[L4.cap_target_fps]  ⊳ [L2.cp5_4_1_orch]      : "fps normalization target"
```

---

## LAYER 5 — Forward roadmap (placeholders ⚪ ⏳)

### Format slots (Capa B forward)
```
[L5.marina_slot]     Marina AI Influencer format (PLACEHOLDER ⚪)
                     Forward: marina-format/ con PAUTA + INGENIERO-PAUTA propias
                     Reuses: Capa A (95%) + Pattern 7 + Hard Rules universal + lib helpers
                     Replaces: PAUTA-MASTER (single-character + cross-video coherence)
                     New: lip-sync mandatorio (Hedra Character-3 viable here)

[L5.tutorial_slot]   Tutorial format (PLACEHOLDER ⚪)
[L5.b2b_slot]        B2B commercial format (PLACEHOLDER ⚪)
[L5.documental_slot] Documentary format (PLACEHOLDER ⚪)
```

### Sprint B — 8 validators codified, NOT built
```
[L5.sb_anchor_sig]   audit-anchor-vs-spec-signature.py (PLACEHOLDER ⚪ Gap #44) — anchor signature compliance
[L5.sb_tts_perc]     audit-tts-perceptual.py           (PLACEHOLDER ⚪ Gap #45) — 70% TTS automation
[L5.sb_deliverable]  audit-deliverable-vs-spec-manifest.py (PLACEHOLDER ⚪ Gap #46) — 1:1 manifest
[L5.sb_brief]        audit-engineer-brief-vs-spec.py   (PLACEHOLDER ⚪ Gap #47) — brief literal verify
[L5.sb_stability]    audit-spec-stability-budget.py    (PLACEHOLDER ⚪ Gap #48) — ≤3 props
[L5.sb_pose]         audit-spec-pose-coupling.py       (PLACEHOLDER ⚪ Gap #49) — anchor pose match
[L5.sb_prompt_syn]   audit-engineer-prompt-syntax.py   (PLACEHOLDER ⚪ Gap #50) — label-prefix detect
[L5.sb_burned_text]  audit-shot-burned-text-ocr.py     (PLACEHOLDER ⚪ Gap #51) — overlay text detection
```

### Sprint M — defense-in-depth CRÍTICA (1 built esta sesión)
```
[L5.sm_l1_wpm]       ✅ audit-spec-narration-fits-duration.py (BUILT BUILD 5 — Bug#12 L1)
[L5.sm_l2_dur]       ✅ audit-tts-vs-spec-duration.py         (BUILT BUILD 6 — Bug#12 L2)
[L5.sm_l4_clip]      audit-clip-timing-vs-audio.py   (PLACEHOLDER ⚪ — Bug#12 L4 per-clip+render total)
[L5.sm_auditor_scope] audit-auditor-decision-scope.py (PLACEHOLDER ⚪ Gap #52 — escalation enforcement)
[L5.sm_tier_strat]   audit-spec-tier-strategy.py     (PLACEHOLDER ⚪ Gap #53)
[L5.sm_cost_tracker] cost-tracker-unified.py         (PLACEHOLDER ⚪ Bug#4 — Claude API spend visibility)
```

### Cleanup forward
```
[L5.cleanup_ui_dirs]  11 UI element test dirs at root → _archive-element-tests/ (TIER 1.1 pending)
[L5.cleanup_baks]     6× CLAUDE.md.bak.* + INDEX.md.bak.* → consolidate to _archive-bak-snapshots/
[L5.cleanup_shakedown] _shakedown-v4-pipeline-validation/ (86MB, removible post-review)
[L5.cleanup_snapshot] _snapshot-pre-sub-fase-3A/ (obsolete post 3A close)
[L5.cleanup_archives] _archive-legacy-projects/ (15GB) podar selectivamente post-V5
```

### Hedra deferred V6+
```
[L5.hedra_integration] Hedra Character-3 integration (PLACEHOLDER ⚪ V6+)
                       Use case: close-up talking-head puro (Hedra genera from still+audio)
                       Cost: $0.033/s Creator tier
                       Workflow: alternative to Hailuo Std + Sync.so when body motion not critical
                       Decision Tomás 2026-05-27: deferred V5 → focus Sync.so PRIMARY only
```

### Edges — Layer 5
```
[L5.marina_slot]     ⤇ [L3.A.*]               : "reuses Capa A 95%"
[L5.marina_slot]     ⤇ [L3.A.spec_template]   : "Marina SPEC uses v11.1 schema"
[L5.marina_slot]     replaces [L3.B.pauta_master] : "new format = new PAUTA"
[L5.marina_slot]     gets [L5.hedra_integration] : "Marina lip-sync mandatory"

[L5.sm_l1_wpm]       ⊳ [L2.cp0_spec_emit]     : "validates pre-emit (BUILT)"
[L5.sm_l2_dur]       ⊳ [L2.cp2_tts_assets]    : "validates post-CP2 (BUILT)"
[L5.sm_l4_clip]      ⊳ [L2.cp46_atomic_mux]   : "validates per-clip + render total (FORWARD)"
[L5.sm_cost_tracker] ⊳ [Layer 2 all CPs]      : "tracks 4 sources spend (FORWARD)"

[L5.cleanup_*]       → repo size + organization improvement (post-V5 ship)
```

---

## Visual layout suggestions for Excalidraw agent

### Top-to-bottom flow:
- **Top band**: Layer 1 (Roles + Principles + Ground Truth) — horizontal across full width
- **Mid-upper band**: Layer 2 (Pipeline CP0 → CP5) — left-to-right chain with vertical validators
- **Mid-lower band**: Layer 3 (Capa A / B / C swimlanes) — 3 horizontal lanes
- **Lower band**: Layer 4 (Detail boxes — effects tiered, Hard Rules table, SPEC schema, Pattern 7 matrix)
- **Bottom band**: Layer 5 (Forward roadmap — dashed gray boxes for placeholders)

### Grouping hints:
- Group all Capa A nodes in a blue-tinted background frame.
- Group all Capa B nodes in a green-tinted background frame.
- Group D38 frozen nodes with thick orange border + lock icon.
- Forward placeholders in dashed gray frame.

### Edges to emphasize visually:
- The CP0 → CP5 main chain (Layer 2): thick solid arrows.
- Pattern 7 capability gating: dashed cyan arrows.
- D38 freeze refs: orange dotted with lock.
- Forward placeholder edges: gray dashed.

---

## CP narrative summary — cómo se arma un video (CP0 → publish)

> Versión prosa de Layer 2 (la versión nodos+edges es la que parsea Excalidraw). Léelo top-to-bottom para entender el flow completo de un video V5+ end-to-end.

**CP0 — Architect SPEC creation.** Tomás da un brief (historia, setting, character intent). El arquitecto consulta `PAUTA-MASTER.md` (patterns canonical P1/P2/P3/P6/P9 derivados empíricamente de 8 refs virales) + `video-log.md` (rotation HR#14 + cross-video uniqueness `location` + `signature_staging`) + `TASTE-LOG.md` (anti-cliché + Tomás gusto). Emite `creative-specs/<v5-id>.yaml` (SPEC v11.1 schema con `video_capabilities` §1.6 declarando 14 flags + `narrative_structure` + `shot_list[]` storyboard-level). Pasa por: architect self-audit D14-D22 + SPEC-AUDIT charter (≥5/8 refs canonical citadas con `informs`+`why_relevant`) + 3 validators nuevos esta sesión (`audit-spec-narrative-coherence.py` BUILD 4 — structure + cross-video + anti-cliché, `audit-spec-narration-fits-duration.py` BUILD 5 — WPM fit, `audit-spec-lip-sync-marks.py` BUILD 8 — D17 coverage). Tomás aprueba el SPEC.

**CP1 — Reference anchors.** Engineer corre `image.py` (Gemini Nano Banana STRICT) → genera anchors per personaje (`anchors/char_a_v1.png`) + locus anchors si hay signature features anatómicas raras (ej. polydactyly → hand-only anchor). Auditor verifica visual + cross-anchor consistency (paleta, props, wardrobe) + MODEL-BEHAVIOR-LOG constraints (face-coupling + stability budget ≤3 props + pose-coupling exact match). Cost ~$0.04 per anchor.

**CP2 — TTS narración.** Engineer corre `tts.py` (ElevenLabs v3 + voice canonical V5 pending Tomás A/B Eleguar vs José Latam Neutral Warm + settings stability 0.45 / similarity 0.80 / style 0.35 / speaker_boost true) → genera `assets/tts/<shot>_narrator.mp3` per shot. Auditor protocol M7: Whisper re-transcribe sobre TTS PROCESADO + per-segment WPM vs canonical p25-p75 [152, 180] + intelligibility ratio ≥0.90 (M7.7.5 semantic equivalence refinement Rule A/B/C/D para edge cases). Plus `audit-tts-vs-spec-duration.py` BUILD 6 Sprint M L2 (actual mp3 duration vs SPEC `duration_intent_s` ±0.5s). Tomás listen test final (Rule D PRECEDENCE — ground truth perceptual).

**CP3 — Shot images.** Engineer corre `image.py --ref <anchor.png>` per shot del SPEC → `shots/<shot>.png` con character + setting + composition declarada. Auditor cross-shots character consistency (D28) + variantes -a/-b/-c con TIPOS de plano distintos para shots >4s (Hard Rule #5) + paleta dual (narrative warm vs choice cool) + setup elements timing 2.5-3.5s + atmospheric motions ≥3 (smoke/vapor/dust/light flicker per shot) + ambient creature/object animated (rat/shark/flame).

**CP4 — Hailuo Std animation.** Engineer corre `video.py` (Replicate Hailuo Std i2v: image-to-video) per shot → `clips/<shot>.mp4` con motion. Para shots con `lip_sync_required: true` el prompt Hailuo usa template lip-sync-friendly (cara frontal/3-4, boca cerrada/neutra, NO escribir "talking"/"speaking" — Hailuo inventaría motion que pelea contra el layer Sync.so). Dry-run gate primero (1 shot sample, auditor visual canonical compliance audit) ANTES de cascade. A4 manifest schema (cost + tier + timestamp + prediction_id). Cost guardrail halt si cumulative > threshold ~$5-8.

**CP4.5 — Sync.so post-process lip sync** *(solo shots `lip_sync_required: true`)*. Engineer invoca Replicate `sync/lipsync-2-pro` con `clips/<shot>.mp4` + `assets/tts/<shot>_<character>_dialog.mp3` → `clips/<shot>_lipsync.mp4` con región boca reemplazada (preservando body motion Hailuo). Cost ~$0.068/s. Para POV first-person + face-less characters (matarife casco-cuchillo) → skip este step.

**CP4.6 — Per-clip atomic mux** *(Hard Rule #23 HYBRID Layer 1)*. Engineer corre `build_clip_atomic.py` por shot → `assets/clips-atomic/<shot>_atomic.mp4` self-contained: visual (Hailuo o lipsync) + audio per-clip (dialog character + clip-scoped SFX) + captions BURNED via Whisper-from-clip-audio (caption-audio LOCKED a frame level, drift físicamente imposible per Hard Rule #25). Quality Gate Agent verdict per clip (≥9.0 PASS / 7.0-8.9 iterate / <7.0 escalate). gemini_midexec_vision hooks: `hailuo_post` (visual quality), `tts_post` (audio quality), `atomic_post` (caption-audio sync), `transition_post` (boundary continuity).

**CP5 — Hybrid assembly + final master.** Orchestrator `build-video-hybrid.py` (Paso 4.1) encadena vía subprocess:
  - **4.2 concat-clips-with-audio.py** → `assets/concat/clips_concat_only.mp4` (Layer 1 concat de atomic clips, audio properly muxed).
  - **4.4 apply-effects-between-clips.py** → `assets/concat/clips_with_effects.mp4` (Layer 2: xfade chain entre clips per SPEC `shot_list[].transition_out` + audio stings overlaid per recipe; resolve effects-dirs tiered Capa A primitives + Capa B sub-genre).
  - **4.3 apply-cross-clip-music.py** → `assets/concat/master_final.mp4` (Layer 3: amix `music_continuous_layers[]` desde `assets/music/<layer_id>.mp3` + sidechain duck música/clip-audio bajo narrator -8±1dB + final master TWO-PASS loudnorm a -14 ±0.5 LUFS canonical-anchored F1).
  - **Layer 4 UI overlay + fps normalization** → `renders/draft-vN.mp4` (ffmpeg drawbox UI stand-in si `has_layer_4_ui: true`; opcional HyperFrames composition rich UI; fps normalizado a `target_fps` SPEC).
  - **8 pre-render gates** sobre el draft: (1) duration_match ±0.5s vs SPEC, (2) LUFS -14 ±0.5, (3) dBTP headroom ≤-0.5 dBFS, (4) output_resolution exact, (5) fps == target_fps, (6) caption-audio sync (gated `has_captions_baked`), (7) all 4 layers integrated per capability flags, (8) no broken frames (midpoint frame extraction). Emite `draft-vN_gates.json` + `draft-vN_manifest.json`.

**Final — Perceptual gate + publish.** Tomás corre HUMAN-CHECKLIST 7 Q gestalt (visual coherent? audio mix balanced? emotional arc lands? caption-audio synced perceptually? cliffhanger hits? cuts feel right? overall ship-ready?). Si PASS → publish MANUAL a @elige_tucompanero (anti-ban — no automatización del upload).

**Costo total típico V5 horror-choice 90s**: ~$5-8 (target post-V4 $14.29). Wall-clock: ~2-4 horas iter 1 (puede requerir 1-2 iter si cualquier validator surface issue).

---

## Self-contained summary for technical readers

**El sistema en 5 frases:**
1. **Capa A (agnostic)** vive en `ai-video-production/templates/` — 4 builds Paso 4 (orchestrator + chain) + ~10 validators + lib helpers + SPEC v11.1 schema + 7 universal effects primitives + caption-styles. Cualquier formato consume.
2. **Capa B (horror-choice activa)** en `horror-choice-format/` — PAUTA-MASTER (creative) + INGENIERO-PAUTA (technical) + canonical-scenes (8 refs) + video-log (rotation + cross-video uniqueness NEW) + lip-sync-workflow + 3 sub-genre effects + TASTE-LOG.
3. **Capa C (per-video)** = cerro-aislado-v4/ frozen D38 (verifiable vía `_freeze-manifests/v4-baseline.md5`) + V5+ projects forward.
4. **Pattern 7 capability-aware** + **15 Hard Rules** gated por flags `video_capabilities` (Bug #9 si missing) — Pattern 7 4-state methodology (applicable/not_applicable/pass/fail).
5. **V5 ship readiness**: pipeline VALIDADO vía shakedown V4 (RAZONABLE — dur -0.447s vs baseline, LUFS en banda). Voice canonical pending Tomás A/B test (Eleguar vs José Latam Neutral Warm). Risk-historia mitigated por validators (BUILD 4 narrative-coherence + L1 + L2 + lip-sync-marks). 109 tests PASS aggregate.

**Forward**: Marina format slot post-V5 (reuses Capa A 95% + Hedra Character-3 integration viable acá). Sprint B (8 validators) + Sprint M remaining 4 CRÍTICA (cost-tracker, L4, auditor-decision-scope, tier-strategy) build post-V5 si V5 surface needs. Cleanup root + archives post-V5 ship.

---

**Genera diagrama con MCP Excalidraw**: pasá este doc al chat con `mcp__claude_ai_Excalidraw__create_view` o `export_to_excalidraw`. El agente puede parsear las secciones `Nodes` + `Edges` per Layer y renderizar con los colores/tipos de la Legend.
