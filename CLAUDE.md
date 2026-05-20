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
| horror, hito, choice, dilema, twist, cliffhanger, "elige a tu compañero", malo/bueno aparente | **+ `horror-choice-format`** |
| animar, Kling, Replicate, image-to-video, "darle vida" | **+ `video-animation`** |
| hyperframes lint/render/init/preview | **+ `hyperframes` + `hyperframes-cli`** |

**Regla:** tarea de DISEÑO = solo arquitecto. Tarea de EJECUCIÓN = ingeniero (3+ skills). NUNCA mezclar roles.

### 0.2 Si es video NUEVO: identificar GENRE + DELIVERY FORMAT

Todo proyecto se define por DOS ejes ortogonales:
- **GENRE** (qué cuenta): horror-choice, tutorial, testimonial, brand-story, etc.
- **DELIVERY FORMAT** (cómo se entrega): reel, youtube-short, youtube-long, b2b-commercial, instagram-story, libre.

Si el usuario solo dijo uno, **preguntá el otro**. Default si no aclara: `format = reel`.

### 0.3 Lectura obligatoria antes de planear (para horror-choice × reel)

> **Si tu rol es 🔍 AUDITOR**: tu lectura obligatoria es la de `creative-director/AUDITOR-PROTOCOL.md` § 1 — NO la lista de abajo. El auditor lee fuentes primarias directas + handoff del ingeniero, **sin** contexto del arquitecto. NO compartas terminal con arq/ing.

```
1. INDEX.md (front door)
2. CLAUDE.md (este archivo) — completo
3. ai-video-production/DELIVERY-FORMATS.md § Matriz GENRE × FORMAT (validar combo)
4. ai-video-production/formats/reel.md (specs + safe zones)
5. ai-video-production/RETENTION-RULES.md (short-form)
6. horror-choice-format/SKILL.md + PAUTA.md (entry del formato)
7. ⭐ horror-choice-format/**PAUTA-MASTER.md** (AUTORIDAD CREATIVA EMPÍRICA del ARQUITECTO — derivada de 8 videos canónicos virales). Reemplaza CREATIVE-BRIEF.md que está DEPRECATED
7.5. ⭐ horror-choice-format/**INGENIERO-PAUTA-MASTER.md** (AUTORIDAD TÉCNICA EMPÍRICA del INGENIERO — pace WPM, LUFS, mix, cuts/min, motion, color, BPM, UI timing — derivada de 10 referentes F1). El ingeniero consulta este doc para CUALQUIER métrica técnica. NUNCA usa nuestras producciones como referencia técnica.
8. horror-choice-format/PATTERNS.md (reglas técnicas — validar contra PAUTA-MASTER + INGENIERO-PAUTA-MASTER en conflicto, ganan los dos masters)
9. ⭐ horror-choice-format/video-log.md — AUTORITATIVO para rotación pattern
10. horror-choice-format/INTRO-FORMULA-V15.md (receta canónica)
11. horror-choice-format/BOOTSTRAP-NEW-PROJECT.md § 9.a + 9.b (template inputs FASE 0)
12. video-director/SKILL.md + WORKFLOW.md + ANTI-PATTERNS.md
13. ai-video-production/SKILL.md + BOOTSTRAP.md + PIPELINE.md + CAPTIONS.md + MOTION-LAYER.md + IMAGE-VARIETY.md + SFX-PIPELINE.md + QA.md
14. video-animation/SKILL.md + ANIMATION-LAYER.md § 1 PRE-GATE
15. library/LIBRARY.md + voices-catalog.json + sfx-catalog.json
16. elements.json (countdown/loader/lower-third disponibles)
17. NARRATION-RULES.md + FEEDBACK-LOOP.md
```

### 0.4 Plan-First Rule

Antes de modificar archivos, llamar APIs externas (ElevenLabs, Gemini, Replicate), o renderizar: presentar plan + esperar confirmación explícita del usuario.

---

## 🏛️ Arquitectura — 2 roles × 3 capas

### 2 roles (axis: QUÉ se hace)

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

### 3 capas (axis: alcance del cambio)

```
CAPA 1 UNIVERSAL (ingeniero)  → .claude/skills/video-director/ + .claude/skills/ai-video-production/
                              → .claude/skills/creative-director/ (arquitecto) + INTERVIEW-FLOW + HANDOFF-PROTOCOL
                              → library/, elements.json, root docs

CAPA 2 FORMATO/TEMPLATE       → INGENIERO:  .claude/skills/horror-choice-format/
                              → ARQUITECTO: .claude/skills/creative-director/templates/elige-tu-companero/
                              (mismo formato, 2 perspectivas — arquitecto = "qué decir", ingeniero = "cómo ejecutar")

CAPA 3 POR-VIDEO              → creative-specs/<id>.yaml (output del arquitecto)
                              → <proyecto>/ (output del ingeniero: assets + render)
```

**Regla de oro**: modificar CAPA 1 sirve a TODOS los videos futuros. CAPA 2 a TODOS los del formato. CAPA 3 es desechable. Si dudás dónde poner algo: `video-director/ARCHITECTURE.md`.

---

## 🔒 Hard rules globales (NO negociables)

| # | Regla | Doc canónico |
|---|---|---|
| 1 | **Quality bar dual FIJA — AMBAS requeridas**: (a) Gemini holístico ≥9.7 + (b) `audit-against-referent.py` ≥85% métricas críticas en rango canónico (F1 n=10 referentes: pace WPM, LUFS, cuts/min, narration coverage). Gemini solo NO basta — scores históricamente inflados (caso pueblo v2: 9.9 holístico vs 7/10 real). Falla de cualquiera de los 2 gates → NO publicar. Tras 3 iter sin pasar ambas → ESCALAR. Histórico: 9.5 (2026-05-12) → 9.7 holístico (2026-05-13) → **dual gate (2026-05-15)**. | memoria `quality_standards.md` + `referent-analysis/F1-INGENIERO-MEASUREMENTS.json` |
| 2 | **Stop point pre-animation requiere ≥9.7.** La animación AI (Kling/Hailuo/Seedance/etc.) NO rescata score — solo agrega +0.1-0.2 sobre baseline. Iterar A→B→C (guion/captions → assets → wiring/mix) hasta ≥9.7 antes de animar. | memoria `quality_standards.md` |
| 3 | **Captions vía Whisper, NUNCA hand-timed.** Post-procesar para eliminar opacity:0 intermedios (gaps 0.3-0.6s). | `ai-video-production/CAPTIONS.md` |
| 4 | **UI safe zones IG Reel** (medido n=10 canónicos): `caption-wrap { bottom: 540px; height: 280px }` (Y 62% canónico ✓). Loading bars: `bottom: 1000px` (Y 48% canónico — banda 44-51%, frame 1920px). Name labels: `top: 220px` (Y 11.5%, banda canónica 12-40%). | `ai-video-production/formats/reel.md` + `horror-choice-format/INGENIERO-PAUTA-MASTER.md` § 7 |
| 5 | **Variantes -a/-b/-c en escenas >4s**, con TIPOS DE PLANO distintos (wide / close-up rostro / close-up detalle / lateral / picado). NO variantes de la misma toma. | `ai-video-production/IMAGE-VARIETY.md` |
| 6 | **⛔ Primeros 30s del Reel = animation AI obligatoria** (universal short-form, model-agnostic). Toda escena con `data-start < 30s` debe ser clip animado vía image-to-video AI (Kling/Hailuo/Seedance/etc.), NO Ken Burns ni estático. Razón: retención algoritmo IG. Modelo según `video-director/MODEL-BENCHMARK.md` § 1.1 / § 2.0. | memoria `animation_30s_rule.md` |
| 7 | **Animation AI preferred SIEMPRE** (reform 2026-05-16). Ken Burns degrada a fallback (último recurso): SOLO cuando regen animation falla 3 veces consecutivas Y el shot es narrativamente esencial. **Max 2-3s duration** cuando usado. Si tu plan default es Ken Burns en plano >2s → estás violando la regla = re-spec o escalar al arquitecto. Ver `INGENIERO-PAUTA-MASTER § 5.6` motion table. | `ai-video-production/MOTION-LAYER.md` + `horror-choice-format/INGENIERO-PAUTA-MASTER.md § 5.6` |
| 8 | **Capa SFX dedicada obligatoria.** Track-index 60-110 reservado. Música + narración + ticks NO es sound design. | `ai-video-production/SFX-PIPELINE.md` |
| 9 | **Mix volumes canónicos**: narración 1.0, música 0.05-0.18 (horror 0.13, dawn 0.17), SFX eventos 0.20-0.35, flash impacts 0.55-0.65, ambient continuo 0.10-0.18. | `ai-video-production/SFX-PIPELINE.md` |
| 10 | **Atempo 2x sobre TTS lento** (nunca raw). Voice ID canónico: `Tj9l48J9AJbry5yCP5eW`. | `ai-video-production/PIPELINE.md` § 1 |
| 11 | **Render lock entre agentes** (`scripts/render-lock.py acquire`). Sin esto: FFmpeg SIGTERM por CPU contention. | `ai-video-production/PIPELINE.md` § 11 |
| 12 | **Plot twist coherente (cuando aplica)**: 3 condiciones simultáneas — lógica clara + imágenes acompañan + narración explica link. Setup elements del twist: timing 2.5-3.5s (no detail shots). | memoria `archetype_system.md` |
| 13 | **Audio coverage thresholds técnicos** (medidos en nuestras producciones — NO autoridad creativa): narración coverage **≥70%** + avg block duration **≥4.5s** + sound fabric **≥99%**. ⚠️ Los Gemini scores 9.9/10/9.5 de nuestra producción son INFLADOS — autoridad creativa del formato vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos). Estos thresholds son SOLO para verificar audio del render. | `audit-audio.py` + memoria `feedback_qa_gates_and_audits.md` |
| 14 | **Rotación obligatoria de pattern** (formato horror-choice): consultar `video-log.md` antes de elegir. NO repetir mismo pattern 2 videos seguidos. | memoria `archetype_system.md` + `video-log.md` |
| 15 | **HyperFrames timeline namespace**: `window.__timelines.main = tl;` único namespace válido. Otros ignorados silenciosamente. | memoria `quality_standards.md` |
| 16 | **data-duration > clip real → NEGRO total.** Fix: `ffmpeg tpad` antes de wire. | `ai-video-production/HYPERFRAMES-GOTCHAS.md` |
| 17 | **Plan-First Rule**: APIs externas + modificación assets requieren plan + confirmación usuario. | (este doc § Step 0.4) |
| 18 | **Cada template ships con DOS pautas paired (creative + engineering)**, ambas derivadas de canonical referents. `PAUTA-MASTER.md` = autoridad arquitecto. `INGENIERO-PAUTA-MASTER.md` = autoridad ingeniero. Sin el segundo, el ingeniero cae back a nuestras producciones (NO autoridad técnica). Cuando creemos un template nuevo (tutorial, B2B, documental), **ambas pautas son required** antes de ejecutar el primer video del formato. | `horror-choice-format/PAUTA-MASTER.md` + `horror-choice-format/INGENIERO-PAUTA-MASTER.md` (en construcción 2026-05-15) |
| 19 | **Nuestras producciones NO son autoridad técnica.** Para CUALQUIER métrica técnica (pace, LUFS, mix, cuts, motion, UI timing, color grade, BPM, voice ID, atempo, modelo, SFX, music style), consultar `<format>-format/INGENIERO-PAUTA-MASTER.md`. **NUNCA** comparar contra `mina-abandonada/`, `bosque-abandonado/`, `elige-companero/`, ni los `ours-*.md` (movidos a `referent-analysis/our-production-archive/` con "NO AUTORIDAD"). Si la métrica no está documentada, **medirla** de los referentes ANTES de decidir. **⭐ NEW expansion 2026-05-18 (caso voice ID matadero)**: cada default técnico en `library/*` + `scripts/*` defaults + `elements.json` DEBE declarar campo `canonical_validation_status: {validated|pending|deprecated_our_prod_only}` + `validated_against_canonical_refs: [<ref-XX list o "N/A measure pending">]` + `validated_at: <date>`. Sin este flag explícito → assume `pending` y audit obligatorio ANTES de usar en producción canonical. **⭐ NEW principle 2026-05-18 (post user listen voice refute): "NEVER ESTIMATE, ALWAYS MEASURE"**. Workflow obligatorio para cualquier technical parameter default: (1) **MEASURE** canonical refs per parameter (diarization per-speaker WPM, per-frame LUT analysis, music BPM extract, etc.), (2) **MATCH** candidate defaults vs measured bands cuantitativamente, (3) **VALIDATE** ambos programmatic + perceptual, (4) **USE** con `canonical_validation_status: validated` + measured fields. Aplica a voice IDs, atempo, models, LUTs, SFX, music BPM, UI elements. Caso disparador 2026-05-15: maikol-crucero, ingeniero recomendó pace 3.0 w/s comparando contra nuestras producciones; referentes reales 2.43-2.75 w/s; correcto era 2.5 w/s. Caso disparador 2026-05-18: voice ID `Tj9l48J9AJbry5yCP5eW` etiquetado "default_canonical" pero `validated_in` solo nuestras producciones (V7 + bosque v1) — user listen test matadero refutó perception "muy lento" porque voice character (susurro grave) NO validated contra canonical viral narrators (LatAm energetic conversational). Plus: per-speaker canonical WPM bands NO existían (F1 measured only total) → engineer atempo aplicado uniform sin canonical per-speaker reference. Fix: Phase 1 priority script `measure-canonical-per-speaker.py` (diarization-based) ANTES de 2do video. | `video-director/SKILL.md` § FUENTE DE AUTORIDAD TÉCNICA + `library/voices-catalog.json` canonical_validation_status fields + Phase 1 cleanup measure-canonical-per-speaker.py |
| 20 | **Modelo barato = prompt premium quality** (regla añadida 2026-05-16). Si el motion del shot permite usar Hailuo / Seedance Lite / Wan-AI (cheap tier), el prompt **DEBE compensar** con: multi-clause + camera direction (lens/movement/angle) + lighting (source/temp/intensity) + exact action (verbo+objeto+cómo) + atmosphere VIA physical expressions (no abstract) + style reference. SPEC schema v6 `scene_context.who_does_what` es input crítico — si falta info → ESCALAR al arquitecto, NO improvisar para llenar gaps. | `horror-choice-format/INGENIERO-PAUTA-MASTER.md § 5.7` + `video-director/MODEL-BENCHMARK.md` |
| 21 | **SPEC storyboard-level obligatorio** (regla añadida 2026-05-16). El SPEC debe describir cada shot a nivel storyboard de cine: `who_is_there`, `who_does_what` (LITERAL per character), `why_this_shot_exists`, `narration_in_this_shot`, `visual_action_match` con `matches_literal: true` certificado. Sin esto el ingeniero improvisa = bugs garantizados (caso cabina-14 2026-05-15: 17 issues narrativos). Auto-audits D19-D22 validan compliance. | `creative-director/templates/CREATIVE-SPEC-TEMPLATE.yaml v6` + `creative-director/SKILL.md` D19-D22 |

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

# 3. Si es horror-choice, además:
HORROR_DIR="<repo-root>/.claude/skills/horror-choice-format/templates"
cp "$HORROR_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$HORROR_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$HORROR_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json

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
| **Autoridad CREATIVA del formato horror-choice** (arquitecto) | ⭐ `horror-choice-format/PAUTA-MASTER.md` |
| **Autoridad TÉCNICA del formato horror-choice** (ingeniero) | ⭐ `horror-choice-format/INGENIERO-PAUTA-MASTER.md` (en construcción 2026-05-15) |
| **NUNCA AUTORIDAD** (post-mortem propio) | `referent-analysis/our-production-archive/` con README "NO AUTORIDAD" |
| Vara de calidad + pre-animation gate + QA protocol | memoria `quality_standards.md` |
| Selección de modelo AI (animation + imagen) — benchmark + decision tree + cost matrix | `video-director/MODEL-BENCHMARK.md` |
| Regla 30s universal short-form (model-agnostic) | memoria `animation_30s_rule.md` |
| Intro 9s pattern (horror-choice) | memoria `intro_9s_canonical.md` + `horror-choice-format/INTRO-FORMULA-V15.md` |
| Archetype matriz + patterns observados + plot twist | ⭐ `horror-choice-format/PAUTA-MASTER.md` §§ 8, 9, 15 (autoridad empírica) + `PATTERNS.md` § 6.5 |
| **Rotación pattern entre videos** | ⭐ `horror-choice-format/video-log.md` (NO confiar en NARRATIVE.md viejos) |
| 7 gates obligatorios pre-render | (este doc § Pre-render gate) + `video-director/WORKFLOW.md` |
| Bootstrap proyecto nuevo | `ai-video-production/BOOTSTRAP.md` (genérico) + `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md` (específico) |
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

Para horror-choice × reel (template actual): ver `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md` § 9.a (DELIVERY) + § 9.b (GENRE — autoritativo per `PAUTA-MASTER.md`).

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
2. **Activar UNA skill cuando la tarea requiere 2-3.** Para horror: video-director + ai-video-production + horror-choice-format SIEMPRE.
3. **Hand-timed captions.** Whisper o nada.
4. **Render sin los 8 gates.** Gate 0 audit-spec-completeness + Lint + audit-narrative + render-lock + audit-frames + **audit-audio + continuity-check** + qa-gate.
5. **Repetir mismo pattern en videos consecutivos** (no consultar `video-log.md`).
6. **Setup elements del twist con timing <2.5s.** El viewer no procesa → twist falla retroactivamente.
7. **Plot twist sin 3 condiciones** (lógica / imágenes / narración). Confunde en vez de impactar.
8. **Sobre-narrar** (>1.1 palabras/seg). El visual debe cargar el peso emocional.
9. **Hardcodear horror-specific en CAPA 1.** Va a CAPA 2 (`horror-choice-format/`).
10. **Crear un skill por proyecto.** Los proyectos NO son skills. El formato sí.
11. **"..." antes de proper nouns en TTS.** Causa mispronunciación → cascada de regens.
12. **Modificar `index.html` completo sin micro-composition.** Usar `MICRO-COMPOSITION-WORKFLOW.md`.

---

## 🧠 Memorias críticas (always-on)

7 memorias consolidadas (2026-05-13). Cada una con UN propósito:

| Memoria | Tema |
|---|---|
| `quality_standards.md` | Vara dual (Gemini ≥9.7 + audit-against-referent ≥85%) + stop point pre-animation + QA protocol + HyperFrames gotchas |
| `animation_30s_rule.md` | Regla universal model-agnostic: primeros 30s = animation AI obligatoria |
| `intro_9s_canonical.md` | Pattern intro 9s horror-choice + Opción C corporal motion |
| `archetype_system.md` | Matriz 10 patterns + plot twist coherente (3 condiciones) + setup timing |
| `feedback_qa_gates_and_audits.md` | Bundle 7 fixes: qa-gate + audit-frames + Show 70/30 + Slot H0 + CTAs |
| `feedback_ambient_creatures.md` | Slot H formato (gnomo/duende/coyote según setting) |
| `feedback_no_autocreate_docs.md` | Análisis = chat, no crear .md sin pedir |

---

## 🔄 Última actualización

**2026-05-15 — arquitectura "template = 2 pautas paired"**:
- Identificado bug fundamental: el ingeniero usaba nuestras producciones como autoridad técnica → heredaba bugs (pace 25% más lento que canónicos, etc.).
- Caso disparador: maikol-crucero — ingeniero recomendó pace 3.0 w/s comparando vs mina/bosque/elige; referentes reales 2.43-2.75 w/s.
- Fix arquitectural: cada template ships con DOS pautas paired — `PAUTA-MASTER.md` (arquitecto) + `INGENIERO-PAUTA-MASTER.md` (ingeniero). Ambas derivadas de canonical referents.
- Hard rules #18-#19 agregadas.
- `ours-*.md` movidos de `referent-analysis/` a `referent-analysis/our-production-archive/` con README "NO AUTORIDAD".
- `video-director/SKILL.md` ahora tiene sección "📐 FUENTE DE AUTORIDAD TÉCNICA" como regla más importante del ingeniero.
- `horror-choice-format/INGENIERO-PAUTA-MASTER.md` en construcción (mediciones agent en background — 10 referentes F1).

**2026-05-13 — refactor mayor (Fase 1+2 de consolidación)**:
- Memorias consolidadas: 23 → 7 (eliminadas duplicadas con docs canónicos).
- CLAUDE.md re-escrito como manual operativo denso: 163 → ~280 líneas con bootstrap canónico + 5 gates pre-render + 17 hard rules + mapa docs autoritativos + inputs FASE 0 explícitos.
- Razón: el agente productor no aterrizaba en sub-docs profundos. Movemos lo crítico a always-on (CLAUDE.md + memorias).
