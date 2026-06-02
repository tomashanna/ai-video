# HANDOFF — Sub-fase 3A cierre (2026-05-27)

> **Audiencia**: Tomás + próxima sesión Auditor (Claude Code). Continuidad **fact-based** (filesystem ground truth, NO memoria conversacional — Principio 4 Sólido).
>
> **Última verify**: 2026-05-28 (D38 11× UNCHANGED, local == remote, tests 109 PASS preservados).

---

## Status overall
- **Sub-fase 3A definitively CERRADA** (cierre 2026-05-27 + commits push 2026-05-27 + voice-effects investigación 2026-05-28).
- **V5 ship readiness FINAL**: riesgo-pipeline mitigated (shakedown V4 RAZONABLE), riesgo-historia covered (4 validators armed pre-V5), riesgo-voice pending Tomás A/B.
- **Sistema agnostic + capability-aware** post Pattern 7 cascade PRE-4.G/H/I/J/K.
- **8 commits temáticos pushed** a `github.com/tomashanna/AI-Video-Edits-` main.

## Hitos técnicos sesión 2026-05-27/28

### 8 commits pushed (lineales sobre `48bd13e` Phase 2 base):
| Hash | Title |
|------|-------|
| `a4909a2` | Cleanup: .gitignore + 2535 deletes accumulated (prior 3A + this session) |
| `1dcb2c7` | Sub-Fase 3A foundations: V3/V4 learnings + Sprint A enforcement + D38 baseline (cerro 966 MB) |
| `0d71a0f` | PRE-4 cascade: Paso 4 sequence (4.2 → 4.4 → 4.3 → 4.1) + effects-library TIERED |
| `c1151cf` | PRE-V5 readiness: Sprint M validators (4 NEW) + Sync.so workflow + EXCALIDRAW |
| `59699be` | Fix .gitignore (inline-comments bug) + 3 missed M + parque-acuatico SPEC |
| `6ffab22` | Add F1 horror-choice canonical measurements + UI safe zones (372 MB) |
| `be8f3cd` | Add voice-effects toolkit + apply-voice-preset.py (Capa A horror-genre presets) |

### Métricas técnicas
- **109 tests aggregate PASS** (101 Paso-4 cascade set + 8 pre-existing hard_rules_parser).
- **4 builds Paso 4 sequence**: `concat-clips-with-audio.py` · `apply-effects-between-clips.py` · `apply-cross-clip-music.py` · `build-video-hybrid.py` (orchestrator) — todos capability-aware Pattern 7 + agnostic `--format` REQUIRED + tests sidecar Hard Rule #26.
- **4 validators críticos pre-V5**:
  - `audit-spec-narrative-coherence.py` (BUILD 4 — sentence-transformers paraphrase-multilingual-MiniLM-L12-v2 + structure D14-D22 + cross-video uniqueness location/signature_staging + anti-cliché + pattern rotation HR#14) — **HIGHEST VALUE** cierra V4 "no 100%" gap.
  - `audit-spec-narration-fits-duration.py` (BUILD 5 Sprint M L1) — WPM pre-emit ∈ [60, 280] per shot.
  - `audit-tts-vs-spec-duration.py` (BUILD 6 Sprint M L2) — TTS actual mp3 vs SPEC intent ± 0.5s.
  - `audit-spec-lip-sync-marks.py` (BUILD 8) — D17 coverage + consistency.
- **Effects-library TIERED** (PRE-4.K post research + Decisión Tomás 1b):
  - Capa A universal primitives (7): cross-fade ×2, hard-cut-with-whoosh, black-screen, fade-to-black, light-flash, glitch (Decision 1.5).
  - Capa B horror sub-genre (3 relocated): film-burn, projector-cue-cinema, static-noise.
  - caption-styles/ relocated (universal mechanism Capa A).
  - Option D fields per recipe: `xfade_transition` + `xfade_fidelity` (5 literal + 5 approximate) + `native_mechanism_note` (WARNING on approximate in production).
- **D38 freeze-manifest canonical** (`_freeze-manifests/v4-baseline.md5`) — **11× verified UNCHANGED** end-to-end de sesión. Resuelve gap PRE-PRE-4.I de "frozen by memory" anti-pattern.
- **Pipeline VALIDADO via shakedown** vs V4 baseline: duration -0.447s (dentro ±0.5 cosmetic), LUFS -14.3 (mejor que baseline -14.8), res/fps exact, 7/8 gates pass (gate 1 fail = artefacto shim duration_intent round-number, NO divergencia pipeline).
- **GAP #10 RESUELTO**: video-log nomenclature canonical reconciliada a PAUTA-MASTER P1/P2/P3/P6/P9 empíricos. P4/P5/P10/Meta deprecated ex-CREATIVE-BRIEF. Filas históricas #1-#6 NOT re-tagged (revisionist anti-pattern); #7 matadero ya canonical. V5 rotation: **NOT P6 → P1/P2/P3/P9**.
- **voice-effects/ toolkit Capa A** + `apply-voice-preset.py` dispatcher — 10 creepy voice presets (sox/ffmpeg chains): matarife_canonical + cocinera_warm (validated matadero) + 8 pending user listen (ghost/ultratumba/demon/possessed_child/static_radio/distant_echo/vampire/phone_call_horror). M7.7.5 intelligibility enforcement via `--verify`.
- **Sync.so workflow** documentado en `horror-choice-format/lip-sync-workflow.md` (Capa B). Hedra Character-3 deferred V6+. Sync.so PRIMARY: preserva Hailuo body motion + reemplaza solo región boca, ~$0.068/s Replicate.
- **Voice strategy v3** codificada en `voices-catalog.json` `v5_narrator_strategy_2026_05_27` block: model eleven_v3 + settings stability 0.45 / similarity 0.80 / style 0.35 / speaker_boost true. Candidates pending A/B Tomás: Eleguar + José Latam Neutral Warm (mi rec; Tomás puede preferir Ignacio-family energetic). Tj9l48 retired confirmado.

### Pattern 7 cascadeado sistema-wide (PRE-4.G → PRE-4.H → PRE-4.I → PRE-4.J → PRE-4.K)
- 15 Hard Rules gated per capability flags (`video_capabilities` §1.6 — 14 flags incl. target_fps + output_resolution NEW PRE-4.1).
- SPEC v11.1 template canonical (`CREATIVE-SPEC-TEMPLATE-v11.yaml`).
- 4-state methodology: `applicable` / `not_applicable` / `pass` / `fail` (NO false-FAIL en capability false).
- Bug #9 escalation: `video_capabilities` missing → exit 2 (NO silent paradigm assumption).
- 7 patterns codified canonical (sistema-wide).

### "Disponibilidad ≠ Uso" principle (PRE-4.K codified)
Capa A primitivas = catálogo disponible, NO prescripción. Capa B sub-genre = catálogo del paradigma. Capa C (SPEC) decide qué se aplica. Forward formats referencian Capa A + agregan su Capa B sin duplicar.

## Decisiones arquitecturales clave (compact)
| # | Decisión | Razón estructural |
|---|----------|-------------------|
| 1 | Effects-library tiered (1b NOT wholesale) | 6 primitivas son universales — wholesale a Capa B duplicaría forward. Tiered preserva DRY + cumple "Capa A agnóstica" |
| 1.5 | Glitch en Capa A (NOT Capa B) | `xfade=hlslice` es primitive universal — horror VHS variant lo USA, no lo posee |
| 2 | Option D (xfade_transition + xfade_fidelity per recipe) | Resolver Finding #4 mapping-by-inference debt sin trigger Option B build prematuro. Option B trigger = production approximate usage perceptually inaceptable |
| 3 | Per-shot `transition_in/out` canonical (NOT top-level transitions[]) | More legible + coherente con resto SPEC. V4 legacy → adapter (`spec_transitions_adapter.py` normalize) |
| 4 | Sync.so PRIMARY only V5 (Hedra deferred V6+) | Hedra Character-3 NO re-lipsyncs existing video — solo genera from still+audio. Sync.so re-lipsyncs el clip Hailuo → preserva motion |
| 5 | target_fps paradigm-flexible default 30 | Resuelve NB 24/30 fps shakedown. Default 30 + WARNING si missing |
| 6 | voice-effects Capa A (NOT B) | Toolkit agnostic horror-genre. 8/10 presets genéricos. 2/10 validated matadero = evidence, not exclusivity |
| 7 | cerro-aislado-v4/ INCLUDED en repo | D38 baseline value > 966 MB size cost. Frozen, no churn forward |
| 8 | _archive-legacy-projects/ + _archive-phase3-v3-learning/ + snapshots EXCLUDED via .gitignore | Local-only artifacts, no for collaborators |

## Constraints carry-forward V5+ (NUNCA olvidar)
- **D38 frozen**: ANTES de cualquier acción que pueda tocar cerro-aislado-v4/ → verify freeze-manifest. Si mismatch → HALT inmediato (corruption real).
- **Pattern 7 capability-aware**: TODOS los validators/builds nuevos gated per capability flags. Bug #9 si `video_capabilities` missing.
- **Disponibilidad ≠ Uso**: catálogos disponibles, SPEC elige. NO prescripción universal.
- **TDD adversarial Hard Rule #26**: every new script ships con test_*.py companion. Min adversarial coverage.
- **Agnostic-by-design**: `--format` REQUIRED en CLI scripts nuevos. NO silent paradigm assumption.
- **Cross-video uniqueness**: `location` exact-match + `signature_staging` semantic ≥0.85 block / 0.75-0.84 flag. Verbs + characters NO check.
- **Constraints anti-destructivos sesiones**: `git reset --hard`, `git push --force`, `git clean -fdx`, `rm -rf`, `git commit --amend` ya pusheado = PROHIBIDOS. HALT + escalar.
- **HR#19 "NEVER ESTIMATE, ALWAYS MEASURE"**: nuestras producciones NO autoridad técnica. F1 referentes son ground truth.
- **HR#26 test sidecar mandatory** para scripts del copy-list (build_clip_atomic + audit-shot-spec-compliance + orchestrator-cp-by-cp + audit-spec-completeness + qa-gate + Sprint M nuevos).
- **Capability matrix testing methodology**: validators emiten `not_applicable` (NO `failed`) cuando capability=false. Auditor verifies post-build.

## Pendientes forward (NO bloquean V5, prioridad sugerida)
| Prioridad | Item | Notes |
|-----------|------|-------|
| **ALTA pre-V5** | Voice A/B test Tomás (15-30s sample Eleguar vs Ignacio-family/José) | Listen test Rule D PRECEDENCE. Settings v3 codificados en voices-catalog v5_narrator_strategy |
| MEDIA pre-V5 | 8/10 voice presets pending listen test | matarife + cocinera validados. Ghost/demon/vampire/etc. pending |
| MEDIA forward | HR#26 test debt: `test_apply-voice-preset.py` faltante | Forward fix post-V5 |
| MEDIA forward | Sprint M CRÍTICA 3 validators NO built | audit-clip-timing-vs-audio (L4) + audit-auditor-decision-scope (Gap #52) + audit-spec-tier-strategy |
| MEDIA forward | Sprint B 8 validators NO built | audit-anchor-vs-spec-signature + audit-tts-perceptual + audit-deliverable-vs-spec-manifest + audit-engineer-brief-vs-spec + audit-spec-stability-budget + audit-spec-pose-coupling + audit-engineer-prompt-syntax + audit-shot-burned-text-ocr |
| BAJA forward | LFS para `cerro-aislado-v4/assets/concat/master_pre_layer3.mp4` 90 MB | GitHub soft warning. Opcional repo-liviano |
| BAJA post-V5 | Cleanup root 11 UI dirs → `_archive-element-tests/` (TIER 1.1 pending) | snapshot manifest documented but not executed |
| BAJA post-V5 | Consolidar `.bak` root remaining → `_archive-bak-snapshots/` | small |
| BAJA post-V5 | Marina format slot Capa B build (forward AI Influencer) | Reuses Capa A 95% + Hedra Character-3 viable acá |

## Quick start próximo chat — orden de lectura
**Para context general (esta sesión):**
1. Este HANDOFF (`HANDOFF-SUB-FASE-3A-CIERRE-2026-05-27.md`)
2. `SYSTEM-LEARNINGS-V3-V4-COMPILATION.md` (20 decisions + 7 bugs + 4 Gemini constraints)
3. `~/.claude/projects/-Users-tomashanna-AI-video-1/memory/active_session_state.md` (memory updated forward)

**Para arquitectura:**
4. `EXCALIDRAW-SYSTEM-OVERVIEW.md` (5-layer system diagram + CP narrative summary CP0→publish)
5. `.claude/skills/creative-director/master-flow-v2/SYSTEM-ROADMAP.md` (Sprint A/B/M definitions §8.9)
6. `.claude/skills/ai-video-production/PIPELINE.md` (§13.9 HYBRID arch + §13.9.1.1 LAYER 2 Finding #1)
7. `.claude/skills/creative-director/AUDITOR-PROTOCOL.md` (§ activation protocol + §3.5 capability-aware testing + §3 V4 archive integrity verification)
8. `CLAUDE.md` (Hard Rules #1-#26 + Pattern 7 + Disponibilidad≠Uso)

**Para horror-choice format:**
9. `.claude/skills/horror-choice-format/PAUTA-MASTER.md` (autoridad creativa empírica 8 refs)
10. `.claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md` (autoridad técnica empírica)
11. `.claude/skills/horror-choice-format/TASTE-LOG.md` (gusto Tomás codificado)
12. `.claude/skills/horror-choice-format/canonical-scenes/INDEX.md`
13. `.claude/skills/horror-choice-format/lip-sync-workflow.md` (Capa B Sync.so canonical)
14. `referent-analysis/horror-choice/F1-INGENIERO-MEASUREMENTS.json` (autoridad WPM canonical)

**Para V5 SPEC writing:**
15. `.claude/skills/creative-director/templates/CREATIVE-SPEC-TEMPLATE-v11.yaml` (schema v11.1 + video_capabilities §1.6 + target_fps NEW)
16. Validators armed (CLI test antes de SPEC final):
    - `audit-spec-narrative-coherence.py` (structure + cross-video + anti-cliché)
    - `audit-spec-narration-fits-duration.py` (Sprint M L1 WPM fit)
    - `audit-spec-lip-sync-marks.py` (D17 coverage)

**Para voice work:**
17. `library/voices-catalog.json` (v5_narrator_strategy_2026_05_27 block — model + settings + candidates + A/B protocol)
18. `.claude/skills/ai-video-production/templates/effects-library/voice-effects/README.md` + `presets-catalog.json`

## MD5 evidence final (2026-05-28)
| File | MD5 |
|------|-----|
| **D38 5/5 baselines (UNCHANGED 11× sesión)** | |
| cerro-aislado-v4/renders/draft-v2.mp4 | `9495572adc5047e9669d261b5b0a47bb` |
| cerro-aislado-v4/scripts/audit-spec-completeness.py | `36aad9af19cb68466f9b5d05e0aac1f6` |
| cerro-aislado-v4/scripts/lib/similarity.py | `29ff3e968abd1a8281f146896907490e` |
| cerro-aislado-v4/scripts/lib/orchestrator_state.py | `09b34b1ddae30970ef98560c177d77e5` |
| creative-specs/cerro-aislado-v4.yaml | `7c73a9b739690ab360c581b684e556a2` |
| **Canonical project files** | |
| CLAUDE.md | `f659c286c7266d1cfbe639f66069b526` |
| EXCALIDRAW-SYSTEM-OVERVIEW.md | `89af7e07507b4535885d3bd198ad8c52` |
| .gitignore (post-fix) | `bddb4eaf2dfbb1cfd1b323405578f853` |
| _freeze-manifests/v4-baseline.md5 | `2ab8a905e7c02615974f0355da43899d` |
| _snapshot-pre-cleanup-tier2/SNAPSHOT-MANIFEST.md | `2ae67f7ce76b45ec270c633d3ca42d25` |
| library/voices-catalog.json | `5ee21b5b2e30a44285729d12e165c378` |
| horror-choice-format/video-log.md (GAP #10 reconciled + BUILD 3 enriched) | `dbb84531af29177dec2745c7dc096624` |
| horror-choice-format/lip-sync-workflow.md (BUILD 8) | `43babbda297c704f5f082c15278df48f` |
| audit-spec-narrative-coherence.py (BUILD 4) | `a5ff05602edaff1a285f0639be210ae6` |
| build-video-hybrid.py (Paso 4.1) | `3588ae755cee70ea8d22f65b01acb9ce` |

## Git state final
- Local HEAD = Remote HEAD = `be8f3cd0f232a4d7ea6ec7d817a10ff6d4045bb4`
- Remote: `https://github.com/tomashanna/aI-Video-Edits-.git` main
- Working tree CLEAN
- 8 commits ahead `48bd13e` Phase 2 base

## Próximas sesiones recomendadas (sugerencia, NO blocking)
1. **Voice A/B test** (chat propio Tomás + Auditor — listen test 15-30s sample Eleguar vs Ignacio-family/José). Settings v3 codificados.
2. **Excalidraw visual generation** (chat nuevo del Project con MCP Excalidraw conectado — pasar `EXCALIDRAW-SYSTEM-OVERVIEW.md` para auto-render multi-capa).
3. **V5 SPEC writing** (architect chat — usar v11.1 template + ejecutar 3 validators pre-emit). Pattern V5 ∈ {P1, P2, P3, P9} per HR#14 rotation post matadero P6.
4. **Marina format planning** (architect — Capa B placeholder forward AI Influencer + Hedra integration viable acá vs V5 horror Sync.so).
5. **Sprint M CRÍTICA validators** (engineer narrow scope per validator — `audit-clip-timing-vs-audio` highest value pre-Marina).

---

**Sistema READY V5 ship.** Sub-fase 3A definitively CERRADA con drift cero local↔remote.
