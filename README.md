# AI Video — sistema de producción de video con IA

> **Qué es esto.** Un sistema para producir videos cortos generados con IA de punta a punta
> (imagen → TTS → SFX → animación i2v → lip-sync → composición HyperFrames → master -14 LUFS → render).
> Está construido como una jerarquía de **capas agnósticas** + un equipo de **tres roles** con
> autoridad separada, de modo que agregar un formato nuevo no toca el núcleo y cada decisión
> tiene UNA sola fuente de verdad. Para **editar footage YA grabado** (testimonios, ads, entrevistas —
> no generar desde cero) hay además un rol **Editor** (`video-editor`) — ver "Los tres roles".

> **Front-door operativo.** Este README explica *qué es* el sistema y *cómo está organizado*.
> Para las reglas de trabajo vivas — hard rules, gates obligatorios, triggers de skills, paths
> canónicos, qué doc es autoritativo por tema — la fuente es **`CLAUDE.md`** (se auto-inyecta en
> cada sesión). El **estado del proyecto** (qué se hizo, qué versión va) es el **`git log`**, no este archivo.

---

## Arquitectura — capas agnósticas

El cambio se aísla por *alcance*. Modificar una capa baja sirve a todo lo de arriba; las capas
altas son desechables.

```
Capa A    — UNIVERSAL, agnóstica de género        .claude/skills/ai-video-production/
            Toolkit técnico de CUALQUIER video: TTS, imagen, SFX, motion, captions Whisper,
            mix/mastering, pipeline HYBRID per-clip, validators, QA. + creative-director (arquitecto)
            + video-director (ingeniero) + video-animation. Catálogo, no prescripción.

Capa A.5  — NÚCLEO de una FAMILIA de formatos      .claude/skills/choice-format-core/
            Mecánica común a TODOS los formatos "choice" (hook dyad + countdown + botones A/B +
            decisión→consecuencia + counterfactual + cliffhanger + POV 1ª persona + UI safe zones).
            Agnóstica al género. La heredan los formatos choice de Capa B. Apunta a Capa A para
            lo universal — no lo duplica.

Capa B    — FORMATO / GÉNERO concreto              .claude/skills/<formato>-format/
            Hereda su familia (Capa A.5 si aplica) y agrega el SABOR de género: autoridad creativa
            (PAUTA-MASTER) + autoridad técnica (INGENIERO-PAUTA-MASTER) + creative-direction +
            referencias canónicas + rotación. Un formato nuevo = una Capa B nueva; A y A.5 intactas.

Capa C    — POR-VIDEO, desechable                  <proyecto>/  +  creative-specs/<id>.yaml
            El output: el SPEC del arquitecto (creative-specs/<id>.yaml) + el directorio del
            video con sus assets y renders. El SPEC decide qué del catálogo se USA.
```

**Principio "Disponibilidad ≠ Uso".** Capa A y A.5 son *catálogos disponibles*, no obligaciones.
La Capa C (el SPEC) decide qué se usa. Un formato nuevo referencia el catálogo existente y solo
agrega lo que su género necesita.

**Regla de oro.** ¿Sirve a CUALQUIER video? → Capa A. ¿A toda una familia de formatos? → Capa A.5.
¿A un solo formato? → Capa B. ¿A un solo video? → Capa C. (Detalle: `video-director/ARCHITECTURE.md`.)

---

## Los tres roles

Tres roles que **nunca se mezclan**, cada uno en su propio terminal/contexto. Se comunican por
**filesystem** (ground truth), no por memoria conversacional.

| Rol | Skill / doc canónico | Hace | Output |
|-----|----------------------|------|--------|
| 🏛️ **Arquitecto** | `.claude/skills/creative-director/` | DISEÑA el qué: historia, personajes, script, intent visual/audio | `creative-specs/<id>.yaml` |
| 🛠️ **Ingeniero** | `.claude/skills/video-director/` + `ai-video-production/` + skills técnicos | EJECUTA el SPEC: imagen, TTS, SFX, animación, lip-sync, mix, render | `video.mp4` + handoff por checkpoint |
| 🔍 **Auditor** | `.claude/skills/creative-director/AUDITOR-PROTOCOL.md` | VERIFICA cada handoff contra la autoridad canónica, de forma independiente | tabla de findings + verdict GO / NO-GO / ESCALAR por CP |

**Por qué tres.** El auditor lee las fuentes primarias *sin* compartir contexto con arquitecto ni
ingeniero — ese tercer ojo independiente es lo que evita que pase un bug sistémico.

El handoff entre roles y los gates por checkpoint están en
`creative-director/HANDOFF-PROTOCOL.md` y `creative-director/AUDITOR-PROTOCOL.md`.

**➕ Un rol aparte: 🎬 el Editor.** El triángulo de arriba **fabrica** videos con IA (desde cero). Para
**editar footage YA grabado** (testimonios, ads, entrevistas, screen-recordings — casos German, editorial,
Palti) hay un cuarto rol independiente y paralelo, el **Editor** (`.claude/skills/video-editor/`): no genera
ni diseña, **ensambla y pule lo que existe** (cortes, velocidad, captions, música/mezcla/−14 LUFS,
transiciones, textos, color). Vive en su propia terminal como los otros y reusa el toolkit de `ai-video-production`.

---

## Cómo navegar — dónde vive la autoridad de cada tema

Para cada tema hay **un solo** doc autoritativo. La fuente maestra de este mapa es
`CLAUDE.md` § "Docs autoritativos" y § "Paths canónicos" — abajo el resumen para arrancar.

| Buscás… | Está en |
|---------|---------|
| Reglas de trabajo vivas (hard rules, gates, **triggers → skill**, paths) | **`CLAUDE.md`** (auto-load) + detalle en `HARD-RULES.md` |
| Toolkit técnico universal (TTS, imagen, SFX, motion, captions, QA) | `.claude/skills/ai-video-production/` (`SKILL.md`, `PIPELINE.md`, `CAPTIONS.md`, …) |
| Editar footage YA grabado (captions, música, velocidad, transiciones, color) | `.claude/skills/video-editor/` (`SKILL.md` + `TOOLBOX.md`) |
| Arquitectura de pipeline (HYBRID per-clip, Layers 1-4) | `.claude/skills/ai-video-production/PIPELINE.md` |
| Mecánica agnóstica de los formatos choice | `.claude/skills/choice-format-core/` |
| Autoridad CREATIVA de un formato | `.claude/skills/<formato>-format/PAUTA-MASTER.md` |
| Autoridad TÉCNICA de un formato (WPM, LUFS, mix, pacing) | `.claude/skills/<formato>-format/INGENIERO-PAUTA-MASTER.md` |
| Referencias canónicas de un formato (videos virales medidos) | `.claude/skills/<formato>-format/canonical-scenes/` |
| Esquema canónico del SPEC | `.claude/skills/creative-director/templates/CREATIVE-SPEC-TEMPLATE-v11.yaml` |
| Protocolo de handoff arquitecto↔ingeniero | `.claude/skills/creative-director/HANDOFF-PROTOCOL.md` |
| Protocolo del auditor (metodología de verificación) | `.claude/skills/creative-director/AUDITOR-PROTOCOL.md` |
| Selección de modelo IA (imagen + animación, benchmark) | `.claude/skills/video-director/MODEL-BENCHMARK.md` |
| Capacidades declaradas por modelo del pipeline | `.claude/skills/ai-video-production/MODEL-CAPABILITIES-MATRIX.md` |
| Voice IDs validados | `library/voices-catalog.json` |
| SFX reusables | `library/sfx-catalog.json` + `library/LIBRARY.md` |
| Componentes UI (countdown / loader / lower-third) | `elements.json` |
| Templates copy-paste para proyecto nuevo | `.claude/skills/ai-video-production/templates/` |
| Qué está congelado / es baseline | `_freeze-manifests/` (cada manifest se auto-documenta) |
| Mediciones empíricas de referentes (autoridad técnica) | `referent-analysis/` |
| Estado del proyecto / qué se hizo / qué versión va | **`git log`** |

---

## Getting started

```bash
# 1. Clonar
git clone https://github.com/tomashanna/AI-Video-Edits-.git
cd AI-Video-Edits-

# 2. Leer el front-door operativo (NO opcional)
#    CLAUDE.md se auto-inyecta en sesiones de Claude Code; si trabajás a mano, leelo primero.

# 3. Entorno + dependencias base
python3 -m venv .venv
source .venv/bin/activate
pip install pyyaml sentence-transformers
# Por script, además: elevenlabs, google-genai, openai-whisper, replicate

# 4. Verificar que los tests pasan
cd .claude/skills/ai-video-production/templates/scripts
for f in test_*.py lib/test_*.py; do python3 "$f" 2>&1 | tail -1; done   # cada uno → "OK"
```

**Para arrancar un video nuevo**, no improvisar: seguir el bootstrap canónico de
`ai-video-production/BOOTSTRAP.md` (genérico) + el del formato (`<formato>-format/BOOTSTRAP-NEW-PROJECT.md`),
que copian los scripts de QA y los gates obligatorios antes de generar nada. El flujo completo
arquitecto → ingeniero → auditor (con los gates por checkpoint) está en `CLAUDE.md` § Step 0.

---

## Principios canónicos del proyecto

| # | Principio | Qué significa |
|---|-----------|---------------|
| 1 | **Agnóstico** | `--format` requerido en los scripts; lo específico de un formato vive en su Capa B, nunca en A |
| 2 | **Automatizable** | Scripts > documentación. Una regla sin script de enforcement es decoración |
| 3 | **Escalable** | Capability matrix por validator. Formato nuevo = Capa B nueva, Capa A intacta |
| 4 | **Sólido** | El filesystem es la ground truth (no la memoria). Lo congelado se verifica vía freeze-manifest, no por confianza |

---

## Contribuir / colaborar

- **Maintainer**: Tomás Hanna (tomashanna)
- **Colaboradores**: IanCid + afluence (técnico)
- **Comunicación**: filesystem como ground truth (no memoria conversacional — Principio 4)
- **Commit / branch**: nunca `--amend` ni `push --force` sobre commits ya pusheados. Los detalles
  operativos vivos están en `CLAUDE.md`.

**Repo**: `github.com/tomashanna/AI-Video-Edits-`
