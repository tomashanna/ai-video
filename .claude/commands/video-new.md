---
description: Crear un video desde cero con todos los gates obligatorios. Usage: /video-new <genre> <delivery> <slug> "<setting>" [--duration 90s] [--slot-h0]
argument-hint: <genre> <delivery> <slug> "<setting description>"
---

# /video-new — Crear video desde cero

Arrancá una sesión de producción de video horror-choice (o cualquier genre) con todo el contexto obligatorio cargado y los gates pre-render activos.

## Tarea

Argumentos recibidos: $ARGUMENTS

Vas a crear un video nuevo. Antes de hacer NADA, leé en orden los siguientes docs y aplicá las reglas (NO improvises ni saltes ningún paso).

---

## ⛔ PASO 1 — Lectura obligatoria (antes de planear)

```
1. docs/OPERATING-MANUAL.md (manual operativo canónico)
2. README.md (estructura del sistema + capas)
3. .claude/skills/ai-video-production/DELIVERY-FORMATS.md § Matriz GENRE × FORMAT
4. .claude/skills/ai-video-production/formats/<delivery>.md  (donde <delivery> = reel, youtube-short, etc.)
5. .claude/skills/ai-video-production/RETENTION-RULES.md  (si short-form)
6. .claude/skills/<genre>-format/SKILL.md
7. .claude/skills/<genre>-format/PAUTA.md
8. .claude/skills/<genre>-format/PATTERNS.md § 6 + § 6.5
9. .claude/skills/<genre>-format/PAUTA-MASTER.md (autoridad empírica derivada de 8 videos canónicos)
10. ⭐ .claude/skills/<genre>-format/video-log.md (AUTORITATIVO para rotación pattern)
11. .claude/skills/<genre>-format/INTRO-FORMULA.md (si genre=horror-choice + delivery=reel)
12. .claude/skills/<genre>-format/BOOTSTRAP-NEW-PROJECT.md § 9.a + 9.b
13. .claude/skills/video-director/SKILL.md + WORKFLOW.md + ANTI-PATTERNS.md
14. .claude/skills/ai-video-production/SKILL.md + BOOTSTRAP.md + PIPELINE.md + CAPTIONS.md + IMAGE-VARIETY.md + MOTION-LAYER.md + SFX-PIPELINE.md + QA.md
15. .claude/skills/video-animation/SKILL.md + ANIMATION-LAYER.md § 1 PRE-GATE
16. assets/library/LIBRARY.md + voices-catalog.json + sfx-catalog.json
17. templates/hyperframes/elements.json
18. NARRATION-RULES.md + docs/FEEDBACK-LOOP.md
```

Memorias críticas (consultar inicio):
- `quality_standards.md` (vara 9.7 + pre-animation gate)
- `animation_30s_rule.md` (regla 30s universal model-agnóstica) + `video-director/MODEL-BENCHMARK.md` (selección modelo táctico)
- `intro_9s_canonical.md` (pattern v15)
- `archetype_system.md` (matriz expandida 10 patterns)
- `feedback_qa_gates_and_audits.md` (Show 70/30 + Slot H0 + CTAs)

---

## ⛔ PASO 2 — Bootstrap del proyecto NUEVO

Preparar entorno + directorio del proyecto (los gates son comandos del paquete, no se copian):

```bash
# 0. Una vez por clon: entorno + CLI (los gates NO se copian: son comandos versionados y testeados)
uv sync --all-extras                 # o: uv sync --extra providers --extra media
cp .env.example .env                 # completar GEMINI_API_KEY / ELEVENLABS_API_KEY / REPLICATE_API_TOKEN
uv run ai-video doctor               # ffmpeg, extras y keys (nunca imprime valores)

# 1. Proyecto nuevo — vive en projects/<slug>/ (git-ignored); el SPEC en creative-specs/<id>.yaml
mkdir -p "projects/<slug>"/{assets/sfx,renders}
cp templates/project/hyperframes.json "projects/<slug>/hyperframes.json"
cd "projects/<slug>"

# 2. Templates propios del formato (Capa B), ej. horror-choice-format:
FORMAT_DIR="../../.claude/skills/<genre>-format/templates"
cp "$FORMAT_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$FORMAT_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$FORMAT_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json

# 3. Verificación (NO continuar si falla): SPEC válido + todos los gates disponibles
uv run ai-video validate-spec ../../creative-specs/<id>.yaml
uv run ai-video list                 # gates, builders y providers disponibles
```

---

## ⛔ PASO 3 — Elegir pattern de matriz expandida

**Consultar `<genre>-format/video-log.md`** (no NARRATIVE.md de proyectos viejos). Identificar qué patterns están sobre-usados (>2 veces consecutivas) y descartarlos.

Si el genre tiene matriz expandida (horror-choice), elegir entre los 10 patterns + meta-cliffhanger uno que NO se haya usado en los últimos 3 videos. Razonar la elección al usuario.

---

## ⛔ PASO 4 — Inputs FASE 0

Usar la tabla del `<genre>-format/BOOTSTRAP-NEW-PROJECT.md` § 9.a + 9.b. NO improvisar preguntas — usar el template estandarizado.

**Bloque 9.a — DELIVERY** (técnico): format / plataforma / duración / idioma.
**Bloque 9.b — GENRE** (narrativo): malo aparente / bueno aparente / setting / verbo H1 / dilemas H3+H4 / twist H4-H5 / cliffhanger H6 / slot H0 sí/no.

Si el usuario no quiere decidir creativos, vos proponés 2-3 opciones de PAUTA-MASTER.md (catalog de Slots A-H empíricos, no inventes).

---

## ⛔ PASO 5 — Ejecutar en autopilot hasta stop point pre-animation

Ejecutar todas las fases sin frenar:
1. TTS (atempo 2x) — eliminar "..." antes de proper nouns (causa mispronunciación)
2. Character anchors (Gemini)
3. Imágenes de escenas (con `--ref` a anchors)
4. SFX (chequear `assets/library/` primero, generar solo lo faltante)
5. Whisper captions (post-procesar para eliminar opacity:0 intermedios)
6. index.html con HTML + GSAP + INTRO-FORMULA
7. **Los 5 gates obligatorios**:
   - `npx hyperframes lint`
   - `uv run ai-video audit-narrative`
   - `uv run ai-video render-lock acquire <slug>`
   - Render draft
   - `uv run ai-video audit-frames --video renders/draft.mp4 --interval 1.0 --max-issues 2`
   - Gemini QA → score X.X
   - `uv run ai-video qa-gate --score <X.X> --stage pre-kling --iteration <N>`

**Si qa-gate retorna exit 1 (BLOCKED)**: iterar A→B→C (guion/captions → assets → wiring/mix) hasta llegar a ≥9.7. Re-correr todos los gates.

**Si qa-gate retorna exit 2 (ESCALATION)**: 3 iteraciones sin llegar a 9.7 → escalar al usuario con análisis dimensión-por-dimensión + opciones de fix.

---

## ⛔ PASO 6 — Append learnings a `<genre>-format/video-log.md`

Antes del stop point al usuario, append 2-3 bullets al final del `<genre>-format/video-log.md` con:
- ✓ Pattern usado (matriz § 3.5) + score Gemini final + audit-against-referent match % (cuando esté disponible, Bloque C)
- ✓ 1 bullet "qué funcionó" (decisión creativa o técnica replicable)
- ✓ 1 bullet "qué no funcionó" (anti-pattern descubierto, si aplica)
- ✓ Costo total proyecto

**Razón**: el `video-log.md` SE CONSULTA antes de cada video nuevo (rotación pattern + cross-video lessons). POST-MORTEM standalone era write-only — sus learnings nunca propagaban a otros docs. Ahora los learnings viven en el doc que SÍ se lee. (POST-MORTEM-TEMPLATE.md deprecated 2026-05-15.)

---

## ⛔ STOP POINT — Reporte al usuario

Solo después de qa-gate exit 0 + audit-frames pass + learnings appended to video-log.md, reportar:

```
═══════════════════════════════════════════════════════════════════
STOP POINT pre-animation — <slug>

✓ Score Gemini final: <X.X>/10 (vara 9.7)
✓ Pattern: <#X — nombre> (justificación rotación: ...)
✓ Library reuse: SFX <N%> | Voces <N%> | Música <N%>
✓ Costo total pre-animation: $<X.XX> / cap $5
✓ Los 5 gates pasaron: lint ✓ audit-narrative ✓ render-lock ✓ audit-frames ✓ qa-gate ✓

Decisiones creativas:
<1 párrafo>

Path render: renders/draft.mp4
Learnings: appended to <genre>-format/video-log.md (2-3 bullets)

Plan animación AI propuesto:
- N clips animados para data-start < 30s (regla animation AI obligatoria primeros 30s)
- M clips animados adicionales para escenas críticas post-30s (justificación: ...)
- Costo estimado: $X.XX (modelo según MODEL-BENCHMARK — Kling 2.5 Turbo Pro default per HOOK VIRAL OVERRIDE)

¿Autorizo animation AI con este plan?
═══════════════════════════════════════════════════════════════════
```

NO renderizar animation AI hasta confirmación explícita del usuario ("sí" / "adelante" / "ok" / "procede" sin condicionales).

---

## Recordatorios críticos

- **Vara fija 9.7** — sub-9.7 NO se publica.
- **Stop point pre-animation requiere ≥9.7** — animation AI NO rescata score.
- **Primeros 30s = animation AI obligatoria** — toda escena `data-start < 30s` requiere clip AI image-to-video (modelo según MODEL-BENCHMARK).
- **Plot twist (si aplica)** = 3 condiciones (lógica + imágenes + narración).
- **Setup elements del twist** = timing 2.5-3.5s.
- **Show 70/30** — narración 0.7-0.9 palabras/seg.
- **NO repetir pattern** del último video (consultar video-log.md).
- **NO "..." antes de proper nouns** en TTS (mispronunciación).
- **Plan-First Rule** — confirmación explícita antes de gastar animation AI/Replicate.
