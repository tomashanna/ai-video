# AI Video 1 — Manual operativo canónico

> **Este archivo se inyecta automáticamente al system prompt en cada sesión.** Es la **única source of truth garantizada** que ves siempre. Las skills/sub-docs requieren decisión activa de lectura — este NO.
>
> Si algo está acá, es **regla operativa imperativa**. Si está en sub-docs, es referencia detallada para implementación.

---

## ⛔ Step 0 — antes de CUALQUIER acción en este directorio

### 0.0 🏛️ Arquitectura three-agent (post 2026-05-17 — codificado AUDITOR como rol formal)

El sistema tiene **TRES roles** que NUNCA se mezclan, cada uno en su propio terminal:

| Rol | Skill / Doc canónico | Función | Output |
|-----|----------------------|---------|--------|
| 🏛️ **ARQUITECTO** | `creative-director` skill | DISEÑA qué + historia + characters + script + intent visual/audio | `creative-specs/<id>.yaml` |
| 🛠️ **INGENIERO** | `video-director` + `ai-video-production` + skills técnicos | EJECUTA el spec: image gen, TTS, SFX, animation, render, mastering | `video.mp4` + `CP[N]-handoff.md` per checkpoint |
| 🔍 **AUDITOR** | `creative-director/AUDITOR-PROTOCOL.md` | VERIFICA handoffs del ingeniero **independientemente** contra autoridad canónica directa (PAUTA-MASTER + INGENIERO-PAUTA + ref-XX + SPEC) — NO delega al self-audit del arq/ing | Tabla findings + verdict GO/NO-GO/ESCALAR per CP |

**Metáfora:** arquitecto dibuja los planos del edificio. Ingeniero lo construye. Auditor es el inspector municipal con copia propia del código de construcción — no le pregunta al arquitecto si cumple. Cada uno es rey en su dominio.

**Por qué 3 roles** (no 2): sin auditor independiente, el self-audit del ingeniero + Gemini holístico inflado (caso pueblo-v2 9.9 vs 7/10 real) deja pasar bugs sistemáticos. Tercer ojo lee fuentes primarias sin contexto compartido = independencia de juicio estructural.

### Trigger por rol

| User dice... | Activá... |
|--------------|-----------|
| "Diseñá una historia", "necesito un concepto", "qué hacemos para el próximo reel", "iteremos con el creativo" | 🏛️ **creative-director** |
| "Producí spec X", "renderizá", "armá las imágenes", "haz el video", "componé en HyperFrames", "ejecutá el spec" | 🛠️ **video-director** + technical stack |
| "Auditá CP[N]", "verificá el handoff del ingeniero", "audit independiente del SPEC", "revisá el render contra autoridad", "actuá como auditor" | 🔍 **AUDITOR** — leer `creative-director/AUDITOR-PROTOCOL.md` + autoridad canónica DIRECTA |

**Si user dice "hagamos un video nuevo"** → empezar con creative-director (diseño). Una vez SPEC aprobado → handoff a engineer. Cada handoff CP[N] del ingeniero pasa por auditor independiente antes de ejecutar el siguiente CP.

### El handoff entre roles

```
USER → ARQUITECTO (entrevista + diseña) → SPEC.yaml
              ↓
       🔍 AUDITOR audit SPEC vs PAUTA-MASTER + D14-D22 (independiente)
              ↓
       USER aprueba SPEC
              ↓
            HANDOFF
              ↓
INGENIERO (CP1 anchors) → CP1-handoff.md
              ↓
       🏛️ ARQUITECTO approval gate creativo + 🔍 AUDITOR audit técnico-creativo independiente
              ↓
INGENIERO (CP2 script) → CP2-handoff.md → arq+audit gates
              ↓
INGENIERO (CP3 shot images) → CP3-handoff.md → arq+audit gates
              ↓
INGENIERO (CP4 animation) → CP4-handoff.md → arq+audit gates
              ↓
INGENIERO (CP5 render) → renders/draft.mp4
              ↓
        Pre-render-gate (20 Q técnicas)
              ↓
       🔍 AUDITOR final: Gemini ≥9.7 + audit-against-referent ≥85%
              ↓
        Architect-final-review (12 Q creativas)
              ↓
        User HUMAN-CHECKLIST (7 Q gestalt)
              ↓
              ✅ PUBLICAR
```

Detalle del workflow arq↔ing: `creative-director/HANDOFF-PROTOCOL.md`.
Detalle del rol auditor: `creative-director/AUDITOR-PROTOCOL.md`.

### 0.1 Identificar tarea + activar skills (legacy mapping — sigue válido)

Identificá la tarea y activá las skills correspondientes (sin esto, fallás):

| Trigger | Skills obligatorias |
|---|---|
| video, render, captions, SFX, narración, TTS, imagen, motion, animar, Kling, Gemini, Whisper | `video-director` (ingeniero) + `ai-video-production` |
| diseñar historia, concepto, idear, "qué hacemos", "iteremos con creativo" | 🏛️ `creative-director` (arquitecto) — STANDALONE para diseño |
| choice / dilema / "elige a tu compañero" / countdown / botones A/B / counterfactual (familia choice) | **+ `choice-format-core` + el skill del GÉNERO** |
| horror, hito, twist, cliffhanger, malo/bueno aparente, body-horror | **+ `horror-choice-format`** |
| fútbol / deporte / jugada / penal / gol / Champions / "elige tu equipo" | **+ `sport-choice-format`** |
| animar, Kling, Replicate, image-to-video, "darle vida" | **+ `video-animation`** |
| hyperframes lint/render/init/preview | **+ `hyperframes` + `hyperframes-cli`** |

**Regla:** tarea de DISEÑO = solo arquitecto. Tarea de EJECUCIÓN = ingeniero (3+ skills). NUNCA mezclar roles.

### 0.2 Si es video NUEVO: identificar GENRE + DELIVERY FORMAT

Todo proyecto se define por DOS ejes ortogonales:
- **GENRE** (qué cuenta): horror-choice, tutorial, testimonial, brand-story, etc.
- **DELIVERY FORMAT** (cómo se entrega): reel, youtube-short, youtube-long, b2b-commercial, instagram-story, libre.

Si el usuario solo dijo uno, **preguntá el otro**. Default si no aclara: `format = reel`.

### 0.3 Lectura obligatoria antes de planear (agnóstica — ruteá al formato activo)

> **Si tu rol es 🔍 AUDITOR**: tu lectura obligatoria es la de `creative-director/AUDITOR-PROTOCOL.md` § 1 — NO la lista de abajo. El auditor lee fuentes primarias directas + handoff del ingeniero, **sin** contexto del arquitecto. NO compartas terminal con arq/ing.

```
1. README.md (front door — qué es el sistema + arquitectura de capas)
2. CLAUDE.md (este archivo) — completo
3. ai-video-production/DELIVERY-FORMATS.md § Matriz GENRE × FORMAT (validar combo)
4. ai-video-production/formats/<delivery>.md (reel / youtube-short / etc. — specs + safe zones)
5. ai-video-production/RETENTION-RULES.md (si short-form)
6. choice-format-core/ (SI el formato pertenece a la familia choice — mecánica AGNÓSTICA: dyad + countdown + A/B + counterfactual + cliffhanger + invariante)
7. ⭐ <format>-format/SKILL.md — el skill del FORMATO ACTIVO, que lista SU lectura obligatoria de género:
     PAUTA-MASTER (autoridad CREATIVA empírica) + INGENIERO-PAUTA-MASTER (autoridad TÉCNICA empírica:
     WPM/LUFS/mix/cuts/motion/color/UI) + PATTERNS + video-log (rotación) + refs canónicas + BOOTSTRAP § 9.
     (Para horror: `horror-choice-format/SKILL.md`. NUNCA usar nuestras producciones como referencia técnica.)
8. video-director/SKILL.md + WORKFLOW.md + ANTI-PATTERNS.md (workflow del ingeniero)
9. ai-video-production/SKILL.md + BOOTSTRAP.md + PIPELINE.md + CAPTIONS.md + MOTION-LAYER.md + IMAGE-VARIETY.md + SFX-PIPELINE.md + QA.md (toolkit técnico universal)
10. video-animation/SKILL.md + ANIMATION-LAYER.md § 1 PRE-GATE
11. library/LIBRARY.md + voices-catalog.json + sfx-catalog.json
12. elements.json (countdown/loader/lower-third disponibles)
13. FEEDBACK-LOOP.md
```

### 0.4 Plan-First Rule

Antes de modificar archivos, llamar APIs externas (ElevenLabs, Gemini, Replicate), o renderizar: presentar plan + esperar confirmación explícita del usuario.

---

## 🏛️ Arquitectura — 3 roles × 4 capas (A / A.5 / B / C)

### Roles (axis: QUÉ se hace) — arquitecto + ingeniero (+ auditor independiente, ver § 0.0)

```
🏛️ ARQUITECTO (creative-director)        🛠️ INGENIERO (video-director + stack)
   ↓                                          ↓
   DISEÑA:                                    EJECUTA:
   - Historia + characters uncanny            - Image generation (Midjourney/Flux/Nano Banana)
   - Script unificado (narración exacta)      - TTS (ElevenLabs voice processing)
   - Anchor prompts + consistency severity    - SFX + music + ambient (ElevenLabs SFX)
   - Shot direction (7 dims per shot)         - Animation (Kling 2.5 / Seedance / etc.)
   - Lip sync intent                          - Lip sync iteration (Hedra/Sync.so/Veo)
   - Color grading intent (paleta dual)       - CSS filters + LUTs implementation
   - Audio direction (genre + ducking)        - Audio mix + ducking + mastering -14 LUFS
   - Counterfactual punchline                 - HyperFrames composition + render
   - Cliffhanger pattern                      - Pre-render-gate 20 Q
   - User interview + iteration               - Asset list production
                                              - Architect feedback loop
   Output: CREATIVE-SPEC.yaml                 Output: video.mp4 ready
```

### 4 capas (axis: alcance del cambio)

```
CAPA A UNIVERSAL (ingeniero)  → .claude/skills/video-director/ + .claude/skills/ai-video-production/
                              → .claude/skills/creative-director/ (arquitecto) + INTERVIEW-FLOW + HANDOFF-PROTOCOL
                              → library/, elements.json, root docs

CAPA A.5 FAMILIA CHOICE       → .claude/skills/choice-format-core/ (mecánica AGNÓSTICA del formato choice:
   (agnóstica al género)        hook dyad + countdown + botones A/B + decisión→consecuencia + counterfactual +
                                cliffhanger + POV + framing condicional + UI safe zones + decision-UI pacing).
                                La HEREDAN horror-choice-format Y sport-choice-format. Apunta a ai-video-production
                                para lo UNIVERSAL (NO lo duplica). Creada 2026-06-01 (refactor "agnóstico fuera del template").

CAPA B FORMATO/TEMPLATE       → horror-choice-format/ (género horror) + sport-choice-format/ (género deportes)
                              → cada formato HEREDA la mecánica de choice-format-core (Capa A.5) + agrega su SABOR de
                                género (arquitecto = "qué decir" en creative-direction/; ingeniero = "cómo ejecutar")

CAPA C POR-VIDEO              → creative-specs/<id>.yaml (output del arquitecto)
                              → <proyecto>/ (output del ingeniero: assets + render)
```

**Regla de oro**: modificar CAPA A sirve a TODOS los videos futuros. CAPA A.5 a toda la familia choice. CAPA B a TODOS los del formato. CAPA C es desechable. Si dudás dónde poner algo: `video-director/ARCHITECTURE.md`.

---

## 🔒 Hard rules globales (NO negociables)

> ⛔ **Detalle completo** (GATING per rule + razón estructural + casos disparadores + doc canónico extendido) → **`HARD-RULES.md`** (root). Esta tabla = **resumen autoritativo + capability gates + pointer doc**. Para edge case GATING / ambigüedad / contexto histórico → consultar HARD-RULES.md.

| # | Regla (resumen) | Gate (Pattern 7) | Doc canónico |
|---|---|---|---|
| 1 | Quality gate primario: `calibrated_v4 ≥9.0` OR `user_perceptual ≥8.5` (OR logic) | `format_type ∈ {interactive_choice, reel}` AND `has_ai_generated_clips` | `audit-gemini-calibrated.py` + `quality_standards.md` |
| 2 | Stop point pre-animation ≥9.7 (iter A→B→C antes de animar) | `has_ai_generated_clips` | `quality_standards.md` |
| 3 | Captions vía Whisper, NUNCA hand-timed | `has_captions_baked` | `CAPTIONS.md` |
| 4 | UI safe zones IG Reel (caption Y62 / loading Y48 / name Y11.5) | `format_type ∈ {interactive_choice, reel}` OR vertical 1080×1920 | `formats/reel.md` + `choice-format-core/INGENIERO-CHOICE-CORE § 2` + `<format>-format/INGENIERO-PAUTA-MASTER § 7` |
| 5 | Variantes -a/-b/-c en shots >4s (TIPOS de plano distintos) | `has_ai_generated_clips` | `IMAGE-VARIETY.md` |
| 6 | ⛔ Primeros 30s = animation AI obligatoria (no Ken Burns) | `has_ai_generated_clips` AND `format_type ∈ {interactive_choice, reel}` | `animation_30s_rule.md` |
| 7 | Animation AI preferred (Ken Burns fallback ≤20%, max 2-3s) | `has_ai_generated_clips` | `MOTION-LAYER.md` + `<format>-format/INGENIERO-PAUTA-MASTER § 5.6` |
| 8 | Capa SFX dedicada obligatoria (track-index 60-110) | `has_sfx_layer` | `SFX-PIPELINE.md` |
| 9 | Mix volumes canónicos (narración 1.0 / música 0.05-0.18 / SFX 0.20-0.35 / flash 0.55-0.65) | `audio_mix_target: lufs_-14` | `SFX-PIPELINE.md` |
| 10 | Atempo 2x sobre TTS lento | `has_tts_narration` | `PIPELINE.md § 1` |
| 11 | Render lock entre agentes (`render-lock.py acquire`) | universal | `PIPELINE.md § 11` |
| 12 | Plot twist coherente (3 condiciones: lógica + imágenes + narración) | `format_type: interactive_choice` | `archetype_system.md` |
| 13 | Audio coverage técnicos (narración ≥70% + block ≥4.5s + fabric ≥99%) | `has_tts_narration` AND `has_layer_3_music` | `audit-audio.py` |
| 14 | Rotación pattern (NO repetir mismo pattern 2 consecutivos) | familia choice (horror/sport/…) | `<format>-format/video-log.md` + `choice-format-core/ROTATION-RULES.md` |
| 15 | HyperFrames namespace `window.__timelines.main = tl` único | universal | `quality_standards.md` |
| 16 | `data-duration > clip real` → negro total (fix `ffmpeg tpad`) | universal | `HYPERFRAMES-GOTCHAS.md` |
| 17 | Plan-First Rule (APIs externas + modificación assets requieren plan + confirm) | universal | (este doc § Step 0.4) |
| 18 | Cada template ships 2 pautas paired (PAUTA-MASTER creative + INGENIERO-PAUTA technical) | universal | `PAUTA-MASTER` + `INGENIERO-PAUTA-MASTER` |
| 19 | Nuestras producciones **NO** autoridad técnica — "NEVER ESTIMATE, ALWAYS MEASURE" (`canonical_validation_status` mandatorio) | universal | `video-director/SKILL.md` + `voices-catalog.json` |
| 20 | Modelo barato = prompt premium quality (5-block: subject+camera+lighting+action+atmosphere) | `has_ai_generated_clips` | `<format>-format/INGENIERO-PAUTA-MASTER § 5.7` + `MODEL-BENCHMARK` |
| 21 | SPEC storyboard-level obligatorio (D19-D22 architect audit) | universal | `CREATIVE-SPEC-TEMPLATE-v11.yaml` + `creative-director/SKILL.md` |
| 23 | Per-clip atomic assembly canonical V3+ (HYBRID Layer 1) | `has_ai_generated_clips` AND `source_clips_origin ∈ {ai_generated, mixed}` | `PIPELINE.md § 13` + `build_clip_atomic.py` |
| 24 ⛔⛔ | Auditor enforce CP-by-CP gates MANDATORY (engineer multi-CP autonomous FORBIDDEN) | universal | `AUDITOR-PROTOCOL § 6 anti-pattern #15` |
| 25 ⛔⛔ | HYBRID architecture canonical V4+ (captions BURNED per clip + narrator continuous Layer 3) | `has_captions_baked` | `PIPELINE.md § 13.9` |
| 26 ⛔ | Tests adversariales obligatorios (`test_*.py` companion per new script) | universal | `BOOTSTRAP.md § script copy list` + Sprint M |
| 27 ⛔ | Arquitecto entrega SPEC con **0 findings 🔴 known** (self-validation pre-emit: corre los validators contra su PROPIO SPEC + itera hasta 🟢; NO entrega con gaps 🔴 declarados). Auditor que recibe SPEC con 🔴 → **RETORNA al arquitecto**, NO escala a Tomás salvo ambigüedad arquitectural real | universal | `creative-director/SKILL.md` § self-validation + `CP2-script-flow.md` + `AUDITOR-PROTOCOL §6 #17` |
| 28/29 ⛔ | **Pipeline models DECLARAN capabilities en `MODEL-CAPABILITIES-MATRIX.md`; los 3 roles del triángulo CONSULTAN antes de producir/validar.** Arquitecto: per shot `narración@165WPM ≤ min(duration_intent_s, i2v.clip_max_s)` pre-SPEC. Validator/Auditor: NO asumir capacidades hardcoded — leer la MATRIX. Modelo nuevo → agregar entrada ANTES de usarlo. (pattern_class 6/5 `model_constraints_not_propagated_across_triangle_roles`; V5 bug: narración truncada 18.8s) | universal | `ai-video-production/MODEL-CAPABILITIES-MATRIX.md` + `audit-spec-narration-fits-duration.py` |
| 30 ⛔ | **Caption coverage = 3 niveles: (A) existence + (B) semantic-match texto + (C) TEMPORAL span.** El caption burn DEBE chunkear TODA la narración del clip en cues word-timed progresivos (≤2 líneas c/u), NO un bloque estático (que se trunca a la 1ª frase). Auditor: verificar 1 frame = existence only (insuficiente) — chequear coverage temporal (caption presente durante TODA la narración hablada). (V5 caption bug: solo la 1ª frase se mostraba; instance 6 `user_perceptual_detects_what_validators_miss`) | `has_captions_baked` | `AUDITOR-PROTOCOL §6` + forward `audit-caption-temporal-coverage.py` |

> ⚠️ **#22 = empty slot** (accidental skip 2026-05-21, blast radius 54 refs externos > beneficio cosmético). Detalle Numbering note → `HARD-RULES.md`.

---

## 📍 Paths canónicos (cierre hidden gap path-clarification 2026-05-23)

| Recurso | Path canonical | Notes |
|---------|----------------|-------|
| `elements.json` | `<repo-root>/elements.json` (root, NOT inside library/ ni skills/) | Components UI catalog (countdown/loader/lower-third). Codificado post inventory 2026-05-23 (Hidden gap 3). |
| `library/voices-catalog.json` | `<repo-root>/library/voices-catalog.json` | ElevenLabs voice IDs validados |
| `library/sfx-catalog.json` | `<repo-root>/library/sfx-catalog.json` | SFX reusables |
| ⭐ `choice-format-core/` | `<repo-root>/.claude/skills/choice-format-core/` | **Capa A.5** — mecánica AGNÓSTICA de la familia choice (CHOICE-MECHANIC + INGENIERO-CHOICE-CORE + ROTATION-RULES). La heredan horror-choice + sport-choice; apunta a ai-video-production para lo universal. Creada 2026-06-01. |
| `videosref_elige_tu_compa/` | `<repo-root>/videosref_elige_tu_compa/` (root) | 8 reference videos canónicos **del formato horror-choice** (refs de género, NO global; cada formato trae las suyas) |
| `referent-analysis/` | `<repo-root>/referent-analysis/` (root) | Empirical analysis outputs F1 measurements |
| `creative-specs/<id>.yaml` | `<repo-root>/creative-specs/<id>.yaml` | Per-video SPEC outputs from architect |
| `_archive-deprecated-docs/` | `<repo-root>/_archive-deprecated-docs/` | DEPRECATED docs preserved as historical reference (CREATIVE-BRIEF + POST-MORTEM-TEMPLATE + ARCHITECT-BRIEFING-VIDEO-3 + plain/v10 SPEC templates) |
| `_archive-legacy-projects/` | `<repo-root>/_archive-legacy-projects/` | Pre-V1 dev projects archived (cabina-14 + bosque-abandonado + mina-abandonada + pueblo-fantasma + maikol-crucero + cabana-tormenta + calabozo-catacumbas + isla-faro + elige-companero) |
| `_archive-phase3-v3-learning/` | `<repo-root>/_archive-phase3-v3-learning/` | V3 parque-acuatico learning archive |

---

## 🚀 Bootstrap canónico — proyecto NUEVO

Si es un proyecto nuevo desde cero, los scripts QA NO existen todavía. **Copiarlos del template ANTES de hacer cualquier cosa**:

```bash
cd "<repo-root>"
mkdir -p "<PROYECTO>"/{assets,scripts,renders}
mkdir -p "<PROYECTO>/assets/sfx"
cd "<PROYECTO>"

# 1. Scripts genéricos (production + 8 gates obligatorios):
SKILL_DIR="<repo-root>/.claude/skills/ai-video-production/templates"
cp "$SKILL_DIR/scripts/"*.py scripts/
#   → tts.py, image.py, sfx.py, captions.py, video.py
#   → audit-narrative.py, render-lock.py, audit-frames.py, audit-audio.py, continuity-check.py, qa-gate.py
#   ⭐ audit-audio.py + continuity-check.py agregados 2026-05-13 (post pueblo-fantasma-desierto v2)
#   ⭐ audit-spec-completeness.py agregado 2026-05-19 (post matadero CP5 gap #13 — SPEC asset_list + ui_active inventory diff)

# 2. Templates de configuración:
cp "$SKILL_DIR/.env-TEMPLATE"            .env
cp "$SKILL_DIR/hyperframes.json-TEMPLATE" hyperframes.json

# 3. Si el formato tiene templates propios (Capa B), copialos de <format>-format/templates/:
FORMAT_DIR="<repo-root>/.claude/skills/<format>-format/templates"   # ej: horror-choice-format
cp "$FORMAT_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$FORMAT_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$FORMAT_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json

# 4. Verificación obligatoria (NO continuar si falla):
for f in tts.py image.py sfx.py captions.py video.py audit-narrative.py render-lock.py audit-frames.py audit-frames-granular.py audit-audio.py continuity-check.py audit-against-referent.py audit-spec-completeness.py qa-gate.py; do
  [ -f scripts/$f ] && echo "✓ scripts/$f" || echo "✗ MISSING scripts/$f"
done

# 5. venv + deps:
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install elevenlabs google-genai python-dotenv openai-whisper replicate
```

Sin esos scripts en `scripts/`, los gates del flow fallan con `FileNotFoundError`.

Detalle completo: `ai-video-production/BOOTSTRAP.md` + `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md`.

---

## 🚧 Pre-render gate — 8 gates OBLIGATORIOS + 4 referent-validated antes de stop point pre-animation

> **Actualizado 2026-05-13** tras pueblo-fantasma-desierto v2 (Gemini 9.9 con video 7/10 real). Agregados gates 5 y 6 que detectan exactamente lo que Gemini holístico no ve: gaps de narración + cobertura baja + caminos rotos.
>
> **Actualizado 2026-05-13 (PM)** tras análisis de 7 referentes Instagram (incluye 4 @referent-a). Pre-render-gate ahora tiene 20 preguntas Y/N: 16 base + Q17-Q20 referent-validated (cuts/min 2-7, LUFS -14 ±0.5, vignette aplicado, monospaced fonts para character names). Ver `pre-render-gate/SKILL.md` § 17-20.
>
> **Actualizado 2026-05-19** tras matadero CP5 STOP point gap #13 — Gate 0 NUEVO (`audit-spec-completeness.py`) que mide SPEC asset_list + ui_active INVENTORY vs actual filesystem + index.html wired. BLOQUEANTE pre-todo-otro-gate porque audits 1-7 miden CALIDAD de lo que existe, NO INVENTARIO contra SPEC (caso disparador: engineer declared CP5 done con 0/10 SFX + 0/3 music + 0/2 ambient + 0/3 countdown wired pero audits 4-6 no lo detectaron).

Después del render draft, ANTES de declarar stop point al usuario, correr en orden:

```bash
# ⛔ Gate 0 NUEVO (BLOQUEANTE PRIORIDAD ABSOLUTA) — SPEC asset_list + ui_active completeness
.venv/bin/python scripts/audit-spec-completeness.py \
  --spec ../creative-specs/<id>.yaml --project-dir . --cp 5 --html index.html
# Exit 0 → CONTINUE a gates 1-7
# Exit 1 → STOP point INVÁLIDO, engineer continue execute (CP4-audio / CP5-UI / etc.) hasta ALL inventory PASS
# Razón: previene declarar STOP con sub-paquetes ungenerated (SFX/music/ambient/UI countdown/buttons/loading)
# Authority: AUDITOR-PROTOCOL § 3 CP5 step 9 + TEAM-PROTOCOL § 10 + GAPS-LOG.md gap #13

# Gate 1 — Lint (sintaxis HTML)
npx hyperframes lint
# Falla → fix root cause, NO --no-verify

# Gate 2 — Audit narrativo (visibilidad <1s, z-index, asset orphans)
.venv/bin/python scripts/audit-narrative.py
# Falla → revisar visibility, z-index 68 black-overlay, orphans

# Gate 3 — Render lock (coordinación entre agentes)
.venv/bin/python scripts/render-lock.py acquire <proyecto>
# Falla con lock tomado → wait, NO romper el lock

# Render draft
npx hyperframes render --output renders/draft.mp4

# Gate 4 — Audit frames (Gemini Vision frame-by-frame)
.venv/bin/python scripts/audit-frames.py --video renders/draft.mp4 --interval 1.0 --max-issues 2
# Falla → fix issues localizados (UI overlap, frames negros, texto sobre rostros)

# ⭐ Gate 5 NUEVO — Audit audio (narración coverage + música + gaps)
.venv/bin/python scripts/audit-audio.py --video renders/draft.mp4 --html index.html --max-issues 2
# Falla → fix gaps narrativos >2s, cobertura narración <40%, música ausente
# CRÍTICO: detecta lo que Gemini holístico NO ve (ambient/SFX tapan silencios narrativos)

# ⭐ Gate 6 NUEVO — Continuity check (NARRATIVE.md vs index.html)
.venv/bin/python scripts/continuity-check.py --narrative NARRATIVE.md --html index.html --video-duration <X>
# Falla → fix caminos narrativos rotos, hitos under-narrated, balance temporal

# Gemini QA holístico (con prompt UNIVERSAL 14 dimensiones, ver QA.md)
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py renders/draft.mp4 --prompt "$PROMPT"
# NUEVO 2026-05-13: prompt fuerza inventario obligatorio narración/música/closure
# Si dimensión (12), (13) o (14) falla → score TOPE 8.0 (no compensar con atmósfera)

# Gate 7 — QA gate (bloquea sub-9.7)
.venv/bin/python scripts/qa-gate.py --score <X.X> --stage pre-kling --iteration <N>
# Exit 0 → OK para Kling
# Exit 1 → BLOCKED, iterar A→B→C con fixes NO-KLING
# Exit 2 → ESCALAR (3 iter sin llegar a 9.7)

# Si los 8 gates pasan: append learnings (2-3 bullets) a <format>-format/video-log.md y reportar al usuario.
.venv/bin/python scripts/render-lock.py release <proyecto>
```

**NO declarar stop point al usuario hasta que los 8 gates retornen exit 0.**

**Plus humano post-stop-point**: el usuario abre el render y ejecuta `video-director/HUMAN-CHECKLIST.md` (7 preguntas, ~2 min). El agente NO declara "listo" por su cuenta — declara "esperando human-checklist".

---

## 🗺️ Docs autoritativos (UN solo lugar por tema)

Para cada tema crítico, hay UN doc autoritativo. **NO buscar en otros docs ni en NARRATIVE.md de proyectos viejos:**

| Tema | Doc autoritativo |
|---|---|
| **Autoridad CREATIVA del formato activo** (arquitecto) | ⭐ `<format>-format/PAUTA-MASTER.md` (ej. horror-choice, sport-choice) |
| **Autoridad TÉCNICA del formato activo** (ingeniero) | ⭐ `<format>-format/INGENIERO-PAUTA-MASTER.md` |
| **Mecánica AGNÓSTICA de la familia choice** | ⭐ `choice-format-core/CHOICE-MECHANIC.md` (creativa) + `INGENIERO-CHOICE-CORE.md` (técnica) |
| **NUNCA AUTORIDAD** (post-mortem propio) | `referent-analysis/our-production-archive/` con README "NO AUTORIDAD" |
| Vara de calidad + pre-animation gate + QA protocol | memoria `quality_standards.md` |
| Selección de modelo AI (animation + imagen) — benchmark + decision tree + cost matrix | `video-director/MODEL-BENCHMARK.md` |
| Regla 30s universal short-form (model-agnostic) | memoria `animation_30s_rule.md` |
| Intro 9s pattern (horror-choice) | memoria `intro_9s_canonical.md` + `horror-choice-format/INTRO-FORMULA.md` |
| Patterns (forma abstracta apariencia×verdad) + plot twist | `choice-format-core/CHOICE-MECHANIC.md § 7` (agnóstico) + catálogo de género `<format>-format/PAUTA-MASTER.md` |
| **Rotación pattern entre videos** | ⭐ `<format>-format/video-log.md` + `choice-format-core/ROTATION-RULES.md` (NO confiar en NARRATIVE.md viejos) |
| 7 gates obligatorios pre-render | (este doc § Pre-render gate) + `video-director/WORKFLOW.md` |
| Bootstrap proyecto nuevo | `ai-video-production/BOOTSTRAP.md` (genérico) + `<format>-format/BOOTSTRAP-NEW-PROJECT.md` (específico del formato) |
| Specs técnicos delivery format | `ai-video-production/formats/<delivery>.md` |
| Retention rules short-form | `ai-video-production/RETENTION-RULES.md` |
| Character consistency | `ai-video-production/CHARACTER-CONSISTENCY.md` |
| HyperFrames bugs sutiles | `ai-video-production/HYPERFRAMES-GOTCHAS.md` |
| Anti-patterns universales | `video-director/ANTI-PATTERNS.md` |
| Voice IDs ElevenLabs validados | `library/voices-catalog.json` |
| SFX disponibles para reuse | `library/sfx-catalog.json` + `library/LIBRARY.md` |
| Components UI (countdown/loader/lower-third) | `elements.json` |
| Templates copy-paste | `.claude/skills/ai-video-production/templates/` |
| **Audio mastering -14 LUFS** (post 2026-05-13) | `ai-video-production/AUDIO-MASTERING.md` + `scripts/master-audio.sh` |
| **Color grading 2 LUTs** (post 2026-05-13) | `ai-video-production/COLOR-GRADING.md` (NARRATIVE warm/eerie vs CHOICE cool/cinematic) |
| **Pacing cuts/min 2-7** (post 2026-05-13) | `ai-video-production/PACING-MARKERS.md` + `scripts/check-pacing.sh` |
| **Captions 3 clases** (post 2026-05-13) | `ai-video-production/CAPTIONS.md` § "Sistema de 3 clases" (name/narration/warning) |
| **Character names archetype** (post 2026-05-13) | `horror-choice-format/CHARACTER-NAMES-CATALOG.md` |
| **Síntesis referent analysis** (post 2026-05-13) | `referent-analysis/REFERENT-PATTERNS.md` (35 frames Gemini Vision + 7 videos LUFS) |

---

## 📋 Inputs FASE 0 — recolectar antes de producir

Todo video nuevo necesita inputs FASE 0 confirmados antes de generar assets. Se dividen en dos ejes ortogonales:

- **Eje DELIVERY (técnico)** — format, plataforma, duración, idioma. Aplica a TODOS los templates. Ver `ai-video-production/DELIVERY-FORMATS.md` + `ai-video-production/formats/<delivery>.md`.
- **Eje GENRE (narrativo)** — depende del template. Cada `<format>-format/BOOTSTRAP-NEW-PROJECT.md § 9` define los slots específicos del template.

Para el formato activo: ver `<format>-format/BOOTSTRAP-NEW-PROJECT.md` § 9.a (DELIVERY) + § 9.b (GENRE — autoritativo per su `PAUTA-MASTER.md`). Ej. horror-choice × reel → `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md`.

---

## 🚦 Plan-First Rule (proyecto-wide)

**Aplica a:**
- Modificación de archivos (HTML, configs, scripts, docs, NARRATIVE.md)
- Llamadas a APIs externas: Gemini (image.py), ElevenLabs (tts.py / sfx.py), Replicate (video.py — Kling/Hailuo/Seedance según MODEL-BENCHMARK)
- Render (`npx hyperframes render`) cuando modifica versiones existentes

**No aplica a:**
- Comandos read-only (ls, cat, grep, find, Read, ffprobe)
- Edits triviales explícitos del usuario ("arreglá ese typo")
- mv/cp/mkdir dentro de un plan ya aprobado

**Formato del plan**: archivos a modificar / comandos a ejecutar / APIs + costo estimado / resultado esperado.

Confirmación válida: "Sí", "adelante", "ok", "procede" sin condicionales.

---

## 🧭 Workflow maestro

```
1. LEER DOCS → 2. PLANEAR → 3. EJECUTAR → 4. QA GEMINI → 5. ITERAR
   ↑                                                       │
   └───── si Gemini <9.7 (vara fija) ─────────────────────┘
```

Iteración cap: 3 rounds pre-animation. Tras 3 sub-9.7 → ESCALAR al usuario.

Detalle: `video-director/WORKFLOW.md`.

---

## ⚠️ Anti-patterns top (los que más cuestan)

1. **Parar pre-animation con sub-9.7 esperando que la animación AI lo arregle.** Animation AI (Kling/Hailuo/Seedance/etc.) NO rescata score. Iterar A→B→C primero.
2. **Activar UNA skill cuando la tarea requiere 2-3.** Para un video: video-director + ai-video-production + `<format>-format` (+ `choice-format-core` si es de la familia choice) SIEMPRE.
3. **Hand-timed captions.** Whisper o nada.
4. **Render sin los 8 gates.** Gate 0 audit-spec-completeness + Lint + audit-narrative + render-lock + audit-frames + **audit-audio + continuity-check** + qa-gate.
5. **Repetir mismo pattern en videos consecutivos** (no consultar `video-log.md`).
6. **Setup elements del twist con timing <2.5s.** El viewer no procesa → twist falla retroactivamente.
7. **Plot twist sin 3 condiciones** (lógica / imágenes / narración). Confunde en vez de impactar.
8. **Sobre-narrar** (>1.1 palabras/seg). El visual debe cargar el peso emocional.
9. **Hardcodear lo específico de un formato en CAPA A** (o lo de un género en A.5). Va a su CAPA B (`<format>-format/`).
10. **Crear un skill por proyecto.** Los proyectos NO son skills. El formato sí.
11. **"..." antes de proper nouns en TTS.** Causa mispronunciación → cascada de regens.
12. **Modificar `index.html` completo sin micro-composition.** Usar `MICRO-COMPOSITION-WORKFLOW.md`.

---

## 🧠 Memorias (always-on)

> El índice **completo + autoritativo** se auto-inyecta vía **`MEMORY.md`** (no se duplica acá; el set vigente vive ahí). Cada memoria = UN propósito.

- **Universales** (todo formato): `quality_standards` (vara dual + stop point + QA) · `animation_30s_rule` · `feedback_qa_gates_and_audits` · `feedback_no_autocreate_docs` · `doc_health_git_is_the_log` · `prompt_quality_no_vague`.
- **De género horror** (solo horror-choice): `intro_9s_canonical` · `archetype_system` (10 patterns + plot twist) · `feedback_ambient_creatures` (Slot H).

---

## 📏 Disciplina de archivos (DRY + SRP — calibrada por tipo)

- **CÓDIGO (`.py`):** SRP (un módulo = un trabajo) + DRY (lo compartido → `lib/`) + tamaño objetivo ~300-400 líneas (los de 700-1500 son targets de refactor; tests/validators cohesivos exentos) + test companion (HR#26). Excepción documentada: copias de baseline frozen.
- **DOCS (`.md`):** **un solo tema autoritativo por doc + CERO duplicación cross-doc** ("un solo lugar por tema"). **SIN tope de líneas** — un doc de autoridad largo y cohesivo está sano; dividir solo por TEMA, nunca por número. ⛔ NUNCA changelog / "Última actualización" embebido — el log es **git history** (memoria `doc_health_git_is_the_log`).
- **Secrets** (`.env`, API keys) NUNCA committeados (gitignored).

> **El estado/avances del proyecto NO viven acá** — viven en `git log`. Este doc dice qué es verdad HOY.
