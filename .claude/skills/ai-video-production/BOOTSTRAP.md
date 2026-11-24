# BOOTSTRAP.md — Iniciar un proyecto de video con IA desde cero

> Guía genérica para bootstrap. Independiente del genre (qué cuenta el video). Después de completarla, el proyecto está listo para que un agente siga el playbook del genre/delivery específico sin preguntas.

**Tiempo estimado:** 5-10 minutos.
**Pre-requisitos:** macOS o Linux con `python3 ≥ 3.10`, `ffmpeg`, `npm`, `git` (opcional).

---

## ⛔ 0. DECIDIR GENRE + DELIVERY FORMAT (paso obligatorio antes de cualquier otra cosa)

Todo proyecto de video se define por DOS ejes ortogonales (ver `DELIVERY-FORMATS.md` § "Matriz GENRE × FORMAT"):

| Eje | Ejemplos | Define |
|---|---|---|
| **GENRE** (qué cuenta) | horror-choice, tutorial, testimonial, brand-story, comedy | narrativa, beats, personajes, dilemas, tono |
| **DELIVERY FORMAT** (cómo se entrega) | reel, youtube-short, youtube-long, b2b-commercial, instagram-story, libre | aspect ratio, duración, FPS, UI safe zones, retention rules |

**Acción concreta antes de seguir el bootstrap**:

1. Confirmar con el usuario: `genre = X, format = Y`. Si solo dijo el genre, preguntar el format. Si solo dijo el format, preguntar el genre. **Default razonable si no aclara: format = reel.**

2. Validar el combo en la matriz de `DELIVERY-FORMATS.md`. Si el combo aparece como ✗ ("no fit"), advertir al usuario y proponer alternativa.

3. Leer en orden:
   - `DELIVERY-FORMATS.md` (catálogo padre)
   - `formats/<delivery>.md` (specs técnicas + reglas del delivery)
   - Si short-form (📱 reel / yt-short / ig-story): `RETENTION-RULES.md`
   - SKILL.md + PAUTA.md del genre (ej: `horror-choice-format/PAUTA.md`)
   - Si genre es horror-choice + format reel: `horror-choice-format/INTRO-FORMULA.md` (receta canónica del intro 9s, validada en v15 con 9.9/10)
   - ⭐⭐ **`video-director/MODEL-BEHAVIOR-LOG.md`** (added 2026-05-22 PM late post V4 shot_16 stability budget discovery): empirical model constraints architect MUST design SPEC within. Each entry has `implications_forward.architect_CP0` block with explicit design rules (e.g., Gemini Image ≤3 prop elements for shots with rare anatomy signature characters; face+hand co-located OR locus anchor for signature feature preservation). **Skipping this read = expensive CP3-CP4 regen rescue when SPEC violates model limits** (V4 shot_16 case: forced SPEC v11.1 → v11.2 amendment $0.20 + 30 min wallclock).

4. Recolectar los inputs específicos del combo. Para horror-choice × reel ver `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md` § 9 (tabla de inputs FASE 0).

**Solo después** de estos 4 puntos, continuar con el paso 1 (crear directorio).

**⚠️ Gates obligatorios del flow** (cubierto en `video-director/WORKFLOW.md` Sub-loop HTML/GSAP):

Todo proyecto de video pasa por **8 gates bloqueantes** antes del stop point pre-animation:
0. ⛔ `ai-video audit-spec-completeness` (Gate 0 BLOQUEANTE PRIORIDAD ABSOLUTA — SPEC asset_list + ui_active inventory vs actual filesystem + index.html. Falla = STOP point INVÁLIDO. Caso disparador: matadero CP5 2026-05-19 gap #13)
1. `npx hyperframes lint` (sintaxis)
2. `ai-video audit-narrative` (visibilidad <1s, z-index, orphans)
3. `ai-video render-lock acquire <project>` (coordinación)
4. `ai-video audit-frames` (Gemini Vision frame-by-frame — UI overlaps, frames negros, etc.)
5. `ai-video audit-audio` (narración coverage >40% + música presente + sin gaps narrativos >2s — detecta lo que Gemini holístico NO ve. Caso disparador: pueblo-fantasma-desierto v2 2026-05-13)
6. `ai-video continuity-check` (NARRATIVE.md vs index.html — caminos narrativos rotos, hitos under-narrated, balance temporal)
7. `ai-video qa-gate --score <X.X> --stage pre-kling --iteration <N>` (bloquea sub-9.7)

Los 8 scripts (audit-spec-completeness, lint, audit-narrative, render-lock, audit-frames, audit-audio, continuity-check, qa-gate) se copian del `src/ai_video/` en el paso 2 abajo. Sin estos scripts copiados al proyecto, el flow NO puede llegar al stop point.

**Learnings post-render** (reemplaza POST-MORTEM standalone, deprecated 2026-05-15): al stop point pre-animation, append 2-3 bullets al `<format>-format/video-log.md` con pattern usado, score final, qué funcionó, qué no, costo total. El video-log.md SE CONSULTA antes de cada video nuevo (rotación + cross-video lessons).

---

## 0.1 ARQUITECTURA — dónde vive qué

```
AI video 1/                                       ← raíz workspace
├── PAUTA.md, NARRATION-RULES.md, docs/FEEDBACK-LOOP.md  ← entry docs generales
├── .claude/skills/
│   ├── ai-video-production/                      ← skill TOOLKIT (general)
│   │   └── src/ai_video/{tts,image,sfx,captions}.py  ← FUENTE de scripts
│   ├── horror-choice-format/                     ← skill de formato horror
│   └── [otros formatos futuros]                  ← documental-format, etc.
├── elige-companero/                              ← proyecto Video #1
├── bosque-abandonado/                            ← proyecto Video #2
└── <TU_PROYECTO_NUEVO>/                          ← lo que vas a crear
```

---

## 0.2 GROUND TRUTH CANONICAL PRINCIPLE (D2 codificado 2026-05-24 Sub-Fase 3A.2)

**Filesystem repo es la ÚNICA fuente de verdad para docs canónicos.**

- Project Knowledge (Claude conversacional artifacts) = snapshot informativo, NOT autoritativo
- Si un doc no existe en filesystem repo → NO existe para el sistema
- Cualquier doc canónico mencionado en activation protocols, hard rules, o auditor reads DEBE estar committed en filesystem antes de poder ser referenced

**Enforcement estructural (NOT documentation theater):**
Activation protocols que listen un read no existente en filesystem deben halt y escalar via Bug #9. El Auditor de PRE-4.A demostró este enforcement empíricamente (find/grep antes de proceder, escalation activa en vez de bypass silencioso).

**Casos disparadores (PRE-4.A 2026-05-24):**
- SYSTEM-LEARNINGS-V3-V4-COMPILATION.md mentioned en activation reads, NO existía en filesystem → blocking, resuelto Commit 2
- HANDOFF Sub-Fase 3A + HANDOFF-SUB-FASE-3A presentes pero sin .md → blocking ambigüedad, resuelto Commit 1

**Forward enforcement:** cualquier sprint que introduzca docs nuevos a activation reads DEBE incluir filesystem commit step en su plan.

---

## 0.3 HANDOFF NAMING CONVENTION (codificado 2026-05-24 Sub-Fase 3A.2)

Forward, todos los handoff documents siguen este pattern:

```
HANDOFF-{PROJECT-PHASE-SUBPHASE}.md
```

**Reglas:**
- All-caps + hyphens (no spaces, no underscores)
- Extension .md mandatorio
- Sub-version separada por punto (e.g., 3A.1, 3A.2)

**Ejemplos válidos:**
- HANDOFF-SUB-FASE-3A.1.md
- HANDOFF-SUB-FASE-3A.2.md
- HANDOFF-MARINA-SPRINT-M.md
- HANDOFF-V5-CP3.md

**Ejemplos inválidos (lessons from PRE-4.A drift):**
- "HANDOFF Sub-Fase 3A" (spaces, no ext) — non-grep-able by activation
- "HANDOFF-SUB-FASE-3A" (no ext) — non-canonical

---

## 0.4 PROJECT KNOWLEDGE SYNC EXPLICIT (codificado 2026-05-24 Sub-Fase 3A.2)

**Project Knowledge es snapshot punto-en-tiempo. Forward NO se mantiene sincronizado con filesystem automáticamente.**

Implicaciones operativas:
- Claude conversacional debe asumir Project Knowledge stale a menos que el usuario provea explicit fresh content
- Cuando un doc canónico se actualiza en filesystem, Project Knowledge queda automáticamente stale
- Sincronización Project Knowledge ↔ filesystem es manual del usuario, NO automática del sistema
- Cualquier referencia de Claude conversacional a un doc DEBE ser tratada como potencialmente outdated por el Auditor — verificar filesystem si la decisión depende de la actualidad del contenido

**Razón estructural:** mantener sync automático requiere intervención usuario recurring, violando autonomía forward. Mejor: Project Knowledge es ground truth histórico, filesystem es ground truth actual, usuario bridge cuando necesario.

---

## 1. ENTORNO + DIRECTORIO DEL PROYECTO

```bash
# 0. Una vez por clon: entorno + CLI (los gates NO se copian: son comandos versionados y testeados)
uv sync --all-extras                 # o: uv sync --extra providers --extra media
cp .env.example .env                 # completar GEMINI_API_KEY / ELEVENLABS_API_KEY / REPLICATE_API_TOKEN
uv run ai-video doctor               # ffmpeg, extras y keys (nunca imprime valores)

# 1. Proyecto nuevo — vive en projects/<PROYECTO>/ (git-ignored); el SPEC en creative-specs/<id>.yaml
mkdir -p "projects/<PROYECTO>"/{assets/sfx,renders}
cp templates/project/hyperframes.json "projects/<PROYECTO>/hyperframes.json"
cd "projects/<PROYECTO>"

# 2. Templates propios del formato (Capa B), ej. horror-choice-format:
FORMAT_DIR="../../.claude/skills/<format>-format/templates"
cp "$FORMAT_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$FORMAT_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$FORMAT_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json

# 3. Verificación (NO continuar si falla): SPEC válido + todos los gates disponibles
uv run ai-video validate-spec ../../creative-specs/<id>.yaml
uv run ai-video list                 # gates, builders y providers disponibles
```

**Convención de naming**: `kebab-case`, descriptivo. Ejemplos: `elige-companero`, `bosque-abandonado`, `bosque-encantado`, `faro-vacio`.

### 1.1 ⭐ Asset layout CANONICAL (codificado PRE-4.1+ post shakedown V4 2026-05-27)

Los 4 scripts Paso 4 (`concat-clips-with-audio` / `apply-effects-between-clips` / `apply-cross-clip-music` / `build-video-hybrid`) **esperan paths exactos** bajo `<proyecto>/assets/`. Sin esto, scripts fallan ("clip(s) missing") o degradan silenciosamente (música/narrador no incluidos en el render).

| Path canonical | Contenido | Consumido por |
|----------------|-----------|---------------|
| `<proyecto>/assets/clips-atomic/shot_NN_atomic.mp4` | Per-shot atomic clips (Hard Rule #23) — visual + audio + captions baked. Naming: **EXACT** `shot_NN_atomic.mp4` (no descriptor suffix) | 4.2 concat |
| `<proyecto>/assets/concat/` | Intermedios pipeline (`clips_concat_only.mp4`, `clips_with_effects.mp4`, `master_final.mp4`) | 4.2/4.4/4.3 escriben |
| `<proyecto>/assets/music/<layer_id>.mp3` | Music layers per SPEC `music_continuous_layers[].layer_id` — **filename = layer_id EXACTO** | 4.3 cross-clip music |
| `<proyecto>/assets/narration/narrator_master.mp3` | Narrator master continuous (Layer 3 VO continuo, NO clip-scoped) | 4.3 sidechain duck key |
| `<proyecto>/assets/ambient/` | Ambient continuous layer files (opcional; algunos SPECs los unifican bajo music/) | 4.3 ambient |
| `<proyecto>/assets/sfx/` | SFX events per-clip + effect-bound stings | 4.4 effects + clip atomic mux |
| `<proyecto>/renders/draft-vN.mp4` | Output orchestrator final + `draft-vN_gates.json` + `draft-vN_manifest.json` | 4.1 build-video-hybrid |

**Anti-patterns detectados (shakedown V4 2026-05-27)** — NO seguir el layout rompe el pipeline silenciosamente:
- ❌ Narrator en `assets/tts/` (cerro V4) → 4.3 no encuentra `assets/narration/narrator_master.mp3` → mix sin narrator + sin sidechain duck (audio degrade silencioso).
- ❌ Music `layer_id` ≠ filename (e.g. SPEC `drone_base` + file `music_drone_base_cold.mp3`) → 4.3 warn "missing layer" + degrade a master_only si todos missing.
- ❌ Atomic clips con descriptor suffix (`shot_03_freeze_8s_atomic.mp4`) → 4.2 busca exact `shot_03_atomic.mp4` → error "atomic clip missing".

**Forward (nuevos formatos):** seguir layout canonical desde bootstrap. Si un formato necesita layout distinto (e.g. B2B con voz humana grabada en `voiceover/`, tutorial sin narrator), declararlo en SPEC `video_capabilities` con override fields **forward schema work** — por ahora todos los formatos siguen este layout o fallan en 4.3 graciosamente (degrade documentado).

---

## 2. TOOLKIT DISPONIBLE (no se copia nada)

Todo el toolkit vive en el paquete `ai_video` (`src/ai_video/`) y se invoca con `uv run ai-video <tool>`
desde cualquier carpeta del repo. `uv run ai-video list` muestra la lista completa; los grupos son:

| Grupo | Tools |
|---|---|
| Generación (APIs pagas, con presupuesto + retries) | `tts`, `sfx`, `image`, `video` (Kling), `veo3`, `captions` (Whisper local), `gemini-midexec-vision` |
| Gate 0 + gates canónicos | `audit-spec-completeness`, `audit-narrative`, `render-lock`, `audit-frames`, `audit-audio`, `continuity-check`, `qa-gate` |
| Per-clip atomic (HR#23/#25) | `build-clip-atomic`, `quality-gate-per-clip`, `audit-shot-spec-compliance`, `orchestrator-cp-by-cp` |
| Calidad calibrada (HR#1) | `audit-gemini-calibrated` (prompt v4 empaquetado en `src/ai_video/prompts/`) |
| Paso 4 HYBRID | `concat-clips-with-audio`, `apply-effects-between-clips`, `apply-cross-clip-music`, `build-video-hybrid` |
| Validators de SPEC | `validate-spec` (schema v11) + `audit-spec-*`, `audit-language-style`, `audit-variant-coverage`, … |

Cada tool tiene tests en `tests/unit/` (HR#26: un tool nuevo entra con su test). Para verificar el entorno:

```bash
uv run ai-video doctor && uv run pytest -q
```

### 📍 Paths canónicos referenciados (cierre hidden gap 3 — 2026-05-23)

- `templates/hyperframes/elements.json` se ubica en **root del proyecto** (`templates/hyperframes/elements.json`), NO en `assets/library/` ni en `.claude/skills/`. Esto es codificación canonical post inventory Sub-Fase 3A.

Si vas a producir un video del formato horror-choice, copiar también los templates específicos del formato:

```bash
HORROR_DIR=".claude/skills/horror-choice-format/templates"

cp "$HORROR_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$HORROR_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$HORROR_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json
```

Para un formato distinto, copiar de su skill correspondiente.

---

## 3. CONFIGURAR `.env`

`.env` vive en la raíz del repo (copiado de `.env.example`, git-ignored). Variables:

- `GEMINI_API_KEY` → https://aistudio.google.com/apikey
- `ELEVENLABS_API_KEY` → https://elevenlabs.io/app/settings/api-keys
- `REPLICATE_API_TOKEN` → solo para animación image-to-video (Kling/Seedance/Hailuo según MODEL-BENCHMARK)
- `AIVIDEO_BUDGET_USD` → tope de gasto estimado (el guard rechaza llamadas que lo superen)

Verificar (nunca imprime los valores):
```bash
uv run ai-video doctor
```

---

## 4. DEPENDENCIAS

Las gestiona `uv` desde `pyproject.toml` (lockfile `uv.lock`). No se crean venvs por proyecto:

```bash
uv sync --extra providers            # APIs (ElevenLabs, Gemini, Replicate)
uv sync --extra providers --extra media   # + Whisper / OpenCV / Pillow (captions, frame audits)
```

---

## 5. EDITAR `hyperframes.json`

```bash
nano hyperframes.json
```

Reemplazar `[NOMBRE_PROYECTO]` con el nombre real:

```json
{
  "name": "tu-proyecto",
  "output": { "width": 1080, "height": 1920, "fps": 30 }
}
```

---

## 5.5. ⭐ SHOT LIST + CHARACTER ANCHORS — gate antes de generar assets (proyectos NUEVOS, 2026-05-11)

> **Aplica solo a proyectos NUEVOS bootstrapeados desde cero.** Si estás editando un proyecto pre-existente (mina-abandonada, bosque-abandonado, etc.) saltarse este paso — los assets ya están generados.

Antes de tirar la primera línea de TTS o la primera imagen, hacer **dos validaciones de consistencia** que cuestan 10 min en bootstrap pero salvan iteraciones caras al final:

### 5.5.a — Validación de character anchors

Ver `CHARACTER-CONSISTENCY.md` § "BOOTSTRAP GATE — Shot list validation" — gate completo. Resumen:

1. Listar TODOS los planos donde aparece cada personaje recurrente
2. Para cada personaje: ¿el outfit/identidad es el mismo en todos los planos? Si cambia → justificación narrativa o unificar
3. Decidir N anchors por personaje (1 por outfit canónico)
4. Generar anchors PRIMERO, spot-check, después generar escenas con `--ref`

**Validado en bug real**: mina-abandonada Santi cambió de outfit completo entre H1 (casco LED + ropa azul) y H6 (beanie + chaqueta marrón) sin justificación narrativa. Pasó por todos los QA. El cliffhanger pierde peso emocional porque el viewer no reconoce a Santi.

### 5.5.b — Validación de continuidad caption ↔ narrador

Para cada caption hardcoded en el HTML (los que NO son auto-generados por Whisper), revisar la frase del narrador que arranca después:

| Caption | Narrador siguiente | Conflicto? |
|---|---|---|
| `"ELIGES A HUGO"` | `"Si elegiste a Hugo... lleva treinta años..."` | ❌ Tiempo verbal distinto + redundante |
| `"SI ELEGISTE A HUGO..."` | `"Si elegiste a Hugo... lleva treinta años..."` | ✅ Caption es prefijo del narrador |
| `"¿CON QUIÉN BAJARÍAS?"` | `"Elige a tu compañero..."` | ✅ Pregunta retórica + respuesta del narrador (no conflict) |

**Workflow**:
```bash
# Listar todos los captions hardcoded del HTML
grep -E 'id="cap-[^"]+".*>[A-Z]' index.html

# Para cada uno, leer el bloque NARRATIVE.md del narrador siguiente
grep -A2 "### h.*narr1" NARRATIVE.md
```

Cualquier conflicto → arreglar el TEXTO de la caption (o eliminar la caption si es redundante con el narrador) **antes** de generar TTS y rendir.

Ver `QA.md` dimensión #10 — agregado al prompt Gemini.

---

## 6. STYLE_SUFFIX por formato en `ai-video image` (AGNÓSTICO por default)

El template es **agnóstico**: `STYLE_SUFFIX = ""` (no aplica estilo por default — Capa A NO asume género). Dos formas de dar el estilo de tu formato:

**(a) Por call (recomendado, sin editar el script):**
```bash
uv run ai-video image -p "..." --style-suffix " <estilo de tu formato>" -o assets/...
```

**(b) Seteando la constante en tu copia** (si todas las imágenes llevan el mismo estilo):
```python
# ai-video image
STYLE_SUFFIX = " <estilo de tu formato>"   # horror: STYLE_SUFFIX = HORROR_SUFFIX (ya definido en el script)
```

`HORROR_SUFFIX` queda definido en el script (Capa B horror) pero **NO se aplica por default**. Si tu formato no usa suffix, dejá `STYLE_SUFFIX` vacío. (`--no-mono-suffix` sigue como opt-out explícito, hoy redundante con el default vacío.)

---

## 7. CREAR `index.html` BASE

Copiar el esqueleto de un proyecto existente del mismo formato:

```bash
cp "bosque-abandonado/index-v2.html" index.html
# Editar el <title> y limpiar el contenido por hito
```

Para formato horror-choice: usar el esqueleto de bosque-abandonado o elige-companero.
Para formato nuevo: empezar con el esqueleto base (canvas vacío 1080×1920) y construir desde cero.

---

## 8. SMOKE TESTS

### TTS

```bash
uv run ai-video tts \
  -t "Prueba de voz." \
  -o assets/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/_smoketest.mp3 && \
rm assets/_smoketest.mp3
```

Si imprime duración (~2s) y borra → OK.

### SFX

```bash
uv run ai-video sfx \
  -t "low sub-bass impact" -d 0.5 -o assets/sfx/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/sfx/_smoketest.mp3 && \
rm assets/sfx/_smoketest.mp3
```

### Image

```bash
uv run ai-video image \
  -p "test prompt: simple black square" -o assets/_smoketest.png && \
ls -la assets/_smoketest.png && \
rm assets/_smoketest.png
```

Las 3 pruebas pasadas → setup OK.

---

## 9. CHECKLIST DE BOOTSTRAP

Antes de pasar a producción del video, confirmar:

- [ ] `<TU_PROYECTO>/` creado con subfolders `assets/`, `assets/sfx/`, `scripts/`, `renders/`
- [ ] `scripts/{tts,image,sfx,captions}.py` copiados
- [ ] `.env` con API keys reales (Gemini + ElevenLabs mínimo)
- [ ] `.venv/` creado con deps instaladas
- [ ] `hyperframes.json` con nombre del proyecto
- [ ] `ai-video image` personalizado con tu STYLE_SUFFIX si aplica
- [ ] Templates del formato específico copiados (si vas a usar uno)
- [ ] Smoke tests pasados (TTS + SFX + image)
- [ ] Inputs creativos recolectados del usuario (según lo que pida el formato)

---

## 10. EL AGENTE TOMA EL VOLANTE

Decirle al agente:
> "Proyecto bootstrapeado en `<ruta>`. Combo: genre = `<genre>` × format = `<delivery>`. Skills activos: `video-director` + `ai-video-production` + `<genre>-format` + (`video-animation` si aplica). Empezá según el playbook del genre y las reglas del delivery."

Para combo **horror-choice × reel** (validado en v15-final 9.9/10):
- Agente lee `horror-choice-format/PAUTA.md`, `INTRO-FORMULA.md`, `PATTERNS.md`, `VIDEO-PLAYBOOK.md`
- Agente lee `formats/reel.md` (specs + UI safe zones + retention)
- Agente lee `RETENTION-RULES.md` (📱 short-form)
- Agente sigue VIDEO-PLAYBOOK fase 0→7

Para combo nuevo (genre o format no validado todavía):
- Agente lee `DELIVERY-FORMATS.md` § "Cuándo agregar un nuevo delivery format" + § "Cuándo crear un genre nuevo"
- Agente propone estructura siguiendo el patrón de `horror-choice-format/` (Capa 2)
- Pre-condición: confirmar con usuario que el combo va a producir ≥3 proyectos (sino usar `formats/libre.md`)

---

## ERRORES COMUNES EN BOOTSTRAP

### `ModuleNotFoundError: No module named 'elevenlabs'`
Faltan los extras de providers: `uv sync --extra providers` (paso 4).

### `ELEVENLABS_API_KEY environment variable is not set`
No hay key configurada. Copiar `.env.example` a `.env` en la raíz del repo y completar la key; verificar con `uv run ai-video doctor`.

### `Gemini API key not found` en ai-video image
Mismo problema. La configuración se lee de variables de entorno o de `.env` en el directorio actual / raíz del repo. Verificar con `uv run ai-video doctor`.

### Hyperframes no reconoce el directorio
Falta `hyperframes.json` o `index.html` en la raíz. Crear ambos antes de cualquier `hyperframes render`.

### SFX salen silenciosos
Venv tiene `elevenlabs < 2.40` (sin `text_to_sound_effects`). Actualizar:
```bash
uv lock --upgrade-package elevenlabs && uv sync --extra providers
```

---

## DESPUÉS DEL BOOTSTRAP

El proyecto está listo. El agente siguiente lee en orden:

**Si es formato horror-choice:**
1. `horror-choice-format/PAUTA.md` (entry doc del formato)
2. `horror-choice-format/PATTERNS.md` (reglas perennes)
3. `horror-choice-format/SCRIPT-WRITING-GUIDE.md`
4. `horror-choice-format/VIDEO-PLAYBOOK.md` (orden secuencial de fases)
5. `ai-video-production/PIPELINE.md`, `MOTION-LAYER.md`, `SFX-PIPELINE.md`, `CAPTIONS.md`, `IMAGE-VARIETY.md` (toolkit, on-demand)

**Si es formato nuevo (sin skill aún):**
1. Crear el skill `<formato>-format/` siguiendo la estructura de `horror-choice-format/`
2. Escribir PATTERNS, PLAYBOOK y plantillas propias del formato
3. Aprovechar todo el toolkit de `ai-video-production/` sin duplicar
