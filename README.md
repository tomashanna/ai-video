# AI Video Edits — horror-choice format production system

> **What is this**: production system for AI-generated horror-choice videos (binary-decision format published @elige_tucompanero on Instagram). Multi-layer agnostic architecture supporting horror-choice format active + forward placeholders (Marina AI Influencer, tutorial, B2B).

---

## Current state (last update 2026-05-28)

**Sub-fase 3A CERRADA** — pipeline validated against V4 baseline, 4 validators armed pre-V5, 8 commits temáticos pushed.

| Dimension | State |
|-----------|-------|
| Pipeline Paso 4 sequence (4.2 → 4.4 → 4.3 → 4.1) | ✅ Built + tested + shakedown-validated vs V4 |
| 4 critical validators pre-V5 | ✅ Armed (narrative-coherence + L1 narration-fits + L2 TTS-duration + lip-sync-marks) |
| Pattern 7 capability matrix | ✅ Cascadeado sistema-wide (15 Hard Rules gated + SPEC v11.1 §1.6) |
| Effects-library TIERED (Capa A universal + Capa B horror) | ✅ Relocated + Option D fields |
| D38 baseline frozen + verifiable | ✅ `_freeze-manifests/v4-baseline.md5` (11× verified UNCHANGED last session) |
| Voice strategy V5 | ⏳ Settings codified; A/B test pending Tomás (Eleguar vs candidate alts) |
| 109 tests aggregate | ✅ PASS |

---

## Triángulo operativo (3 roles)

- 🔴 **Tomás** — decisor creativo, override authority, listen test ground truth (Rule D PRECEDENCE).
- 🟣 **Claude conversacional** — estratega en chats del Project. NO ejecuta scripts ni spawn agents. Estructura mensajes al Auditor.
- 🟠 **Auditor (Claude Code)** — engineer + architect role, ejecuta scripts via subprocess, escribe filesystem, audita compliance, emite verdicts honestos.

Roles NUNCA se mezclan. Comunicación vía filesystem (ground truth) + chats separados.

---

## Architecture — 3 layers (Capa A / B / C)

```
Capa A — agnostic universal             (.claude/skills/ai-video-production/)
├── templates/scripts/                  ← engines: 4 Paso 4 builds + validators + lib helpers
├── templates/effects-library/          ← 7 universal transition primitives + audio stings
├── templates/voice-effects/            ← 10 creepy voice presets + apply-voice-preset.py
├── templates/caption-styles/           ← caption-burn 3 canonical classes
└── templates/CREATIVE-SPEC-TEMPLATE-v11.yaml ← canonical SPEC schema

Capa B — format-specific active         (.claude/skills/horror-choice-format/)
├── PAUTA-MASTER.md                     ← creative authority (8 viral refs synthesized)
├── INGENIERO-PAUTA-MASTER.md           ← technical authority (F1 measurements)
├── canonical-scenes/                   ← 8 reference videos frame-by-frame
├── effects-library/                    ← 3 horror sub-genre transitions (film-burn/projector/static-noise)
├── creative-direction/                 ← per-dimension creative guides
├── lip-sync-workflow.md                ← Sync.so canonical workflow
└── video-log.md                        ← per-video rotation log + cross-video uniqueness

Capa C — per-video                      (cerro-aislado-v4/ + V5+ projects)
└── cerro-aislado-v4/                   ← D38 frozen baseline reference (READ-ONLY)
```

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/tomashanna/aI-Video-Edits-.git
cd "AI Video Edits"  # or similar workspace name

# 2. Setup deps
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml sentence-transformers  # core deps for validators
# Plus per script: elevenlabs, google-genai, openai-whisper, replicate

# 3. Verify tests pass (~3 min, 109 tests)
cd .claude/skills/ai-video-production/templates/scripts
for f in test_*.py lib/test_*.py; do python3 "$f" 2>&1 | tail -1; done
# Expect: each "OK"

# 4. Verify D38 baseline UNCHANGED
cd "/path/to/AI Video Edits"
md5 -r cerro-aislado-v4/renders/draft-v2.mp4 \
       cerro-aislado-v4/scripts/audit-spec-completeness.py \
       cerro-aislado-v4/scripts/lib/similarity.py \
       cerro-aislado-v4/scripts/lib/orchestrator_state.py \
       creative-specs/cerro-aislado-v4.yaml
# Compare vs _freeze-manifests/v4-baseline.md5 — must match 5/5
```

---

## ⛔ What NOT to touch

These are frozen / authoritative — modify only with explicit Tomás approval:

| Path | Why |
|------|-----|
| `cerro-aislado-v4/` | D38 frozen baseline V4 — ground truth for forward validation. Never modify, never delete |
| `_freeze-manifests/v4-baseline.md5` | Canonical baseline MD5 manifest. Modifying invalidates D38 verifiability |
| `_archive-*/` | Historical records preserved as historical reference |
| Any commit hash already pushed | NEVER `git commit --amend` on pushed commits. NEVER `git push --force` |

---

## Where to find things

| Looking for... | Location |
|----------------|----------|
| Pipeline engines (Paso 4 builds) | `.claude/skills/ai-video-production/templates/scripts/` |
| Validators (Sprint M + narrative coherence) | `.claude/skills/ai-video-production/templates/scripts/audit-*.py` |
| SPEC schema canonical | `.claude/skills/creative-director/templates/CREATIVE-SPEC-TEMPLATE-v11.yaml` |
| Hard Rules (canonical project rules) | `CLAUDE.md` (auto-loaded into every session) |
| Architect protocol (audit methodology) | `.claude/skills/creative-director/AUDITOR-PROTOCOL.md` |
| Pipeline architecture (HYBRID Layer 1-4) | `.claude/skills/ai-video-production/PIPELINE.md` § 13.9 |
| System roadmap (Sprint A/B/M) | `.claude/skills/creative-director/master-flow-v2/SYSTEM-ROADMAP.md` § 8.9 |
| V3/V4 learnings (20 decisions + 7 bugs + 4 Gemini constraints) | `.claude/skills/creative-director/master-flow-v2/SYSTEM-LEARNINGS-V3-V4-COMPILATION.md` |
| Horror-choice creative authority | `.claude/skills/horror-choice-format/PAUTA-MASTER.md` |
| Horror-choice technical authority | `.claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md` |
| Canonical reference videos (8 refs) | `.claude/skills/horror-choice-format/canonical-scenes/INDEX.md` |
| Voice IDs catalog + V5 narrator strategy | `library/voices-catalog.json` |
| Voice effects presets (sox/ffmpeg chains) | `.claude/skills/ai-video-production/templates/effects-library/voice-effects/` |
| Lip-sync workflow (Sync.so) | `.claude/skills/horror-choice-format/lip-sync-workflow.md` |
| F1 canonical measurements (autoridad WPM bands) | `referent-analysis/horror-choice/F1-INGENIERO-MEASUREMENTS.json` |
| System visual overview (multi-layer diagram) | `EXCALIDRAW-SYSTEM-OVERVIEW.md` |
| Latest session handoff (continuity) | `HANDOFF-SUB-FASE-3A-CIERRE-2026-05-27.md` |

---

## How the system works (high-level)

### Pipeline CP-by-CP (one video end-to-end)

```
CP0 SPEC creation → CP1 anchors → CP2 TTS → CP3 shots → CP4 Hailuo → 
CP4.5 Sync.so (lip sync) → CP4.6 atomic mux → CP5 hybrid assembly → publish
```

See `EXCALIDRAW-SYSTEM-OVERVIEW.md` § "CP narrative summary" for prose walkthrough.

### Pattern 7 — Capability Matrix

Every validator + build is **capability-gated** by `spec.video_capabilities` flags. Properties classify as `applicable / not_applicable / pass / fail` (4-state, not binary). `video_capabilities` missing → Bug #9 exit 2 (no silent paradigm assumption).

### "Disponibilidad ≠ Uso" principle

- **Capa A** = catalog disponible para CUALQUIER format (NOT prescription).
- **Capa B** = format-specific catalog (available under `--format <X>`).
- **Capa C (SPEC)** = decides what's used.

Forward formats (Marina, tutorial, B2B) reference Capa A + add their Capa B without duplicating universals.

### Subprocess chaining (Paso 4 orchestrator)

`build-video-hybrid.py` chains:
1. `concat-clips-with-audio.py` (Layer 1 atomic concat)
2. `apply-effects-between-clips.py` (Layer 2 xfade + stings, multi-catalog `--effects-dir` REQUIRED)
3. `apply-cross-clip-music.py` (Layer 3 music + sidechain duck + two-pass loudnorm -14 LUFS)
4. Layer 4 UI overlay + fps normalization
5. 8 pre-render gates

---

## Project canonical principles

| # | Principle | What it means |
|---|-----------|----------------|
| 1 | **Agnóstico** | `--format` REQUIRED on all CLI scripts. No silent paradigm assumption. Format-specific stuff lives in Capa B |
| 2 | **Automatizable** | Scripts > documentation theater. Hard Rules without enforcement scripts are decoration |
| 3 | **Escalable** | Pattern 7 capability matrix per validator. New format = new Capa B, Capa A intact |
| 4 | **Sólido** | Filesystem = ground truth (NOT memory). D38 verifiable via freeze-manifest (NOT trust) |

Plus **7 patterns codified canonical** (No downstream patch of source · Architect proposes, user chooses · SPEC amend with source authority when model constrained · Structural correspondence never manual audit · Cost discipline conservative · No circular self-audit · Parallelize when temporally compatible AND independent).

### Hard Rules (26 numbered, capability-gated)
See `CLAUDE.md` § "Hard rules globales (NO negociables)". Highlights:
- **#1** Quality gate primario (Gemini ≥9.7 + audit-against-referent ≥85%)
- **#19** "NEVER ESTIMATE, ALWAYS MEASURE" — our productions NOT technical authority; F1 referents are
- **#23** Per-clip atomic assembly canonical V3+ (HYBRID Layer 1)
- **#25** HYBRID architecture canonical V4+ (captions baked per clip, narrator continuous Layer 3)
- **#26** Tests adversariales obligatorios forward (test sidecar per new script)

---

## Documentation links

- `EXCALIDRAW-SYSTEM-OVERVIEW.md` — multi-layer visual diagram source (parseable by MCP Excalidraw agent) + CP narrative summary in prose.
- `HANDOFF-SUB-FASE-3A-CIERRE-2026-05-27.md` — latest session detail handoff (8 commits + decisions + pendings + MD5 evidence).
- `V4-LAUNCH-CHECKLIST.md` — V4 launch gates charter (5 gates GREEN reference).
- `.claude/skills/creative-director/master-flow-v2/ARCHITECTURAL-DECISIONS.md` — YAML schema for forward decisions.
- `.claude/skills/creative-director/master-flow-v2/GAPS-LOG.md` — gap tracker (52+ gaps codified).
- `.claude/skills/video-director/MODEL-BEHAVIOR-LOG.md` — empirical AI model constraints (Gemini --ref face/stability/pose-coupling + label-prefix overlay).

---

## Forward / known pending (NO blocks V5)

| Priority | Item |
|----------|------|
| **HIGH pre-V5** | Voice A/B test Tomás (Eleguar vs candidate alts) — listen test Rule D PRECEDENCE |
| MEDIUM forward | Sprint M CRÍTICA 3 validators NOT built (audit-clip-timing-vs-audio + audit-auditor-decision-scope + audit-spec-tier-strategy) |
| MEDIUM forward | Sprint B 8 validators NOT built (anchor-vs-spec-signature + tts-perceptual + deliverable-vs-spec-manifest + etc.) |
| LOW forward | HR#26 test debt: `test_apply-voice-preset.py` missing |
| LOW post-V5 | Cleanup root (11 UI dirs + .bak consolidation) |
| LOW post-V5 | Marina format slot Capa B build (forward AI Influencer + Hedra Character-3 viable) |
| Optional | LFS for `cerro-aislado-v4/assets/concat/master_pre_layer3.mp4` 90 MB |

---

## Contact / collaboration

- **Primary maintainer**: Tomás Hanna (tomashanna)
- **Collaborators**: IanCid + afluence (technical)
- **Communication**: project channel + filesystem ground truth (NOT conversational memory — Principle 4 Sólido)

---

**Repo**: `github.com/tomashanna/aI-Video-Edits-`
**Last verified state**: 2026-05-28, local HEAD == remote HEAD = `be8f3cd`, D38 11× UNCHANGED.
