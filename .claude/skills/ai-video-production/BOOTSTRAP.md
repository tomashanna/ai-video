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
   - Si genre es horror-choice + format reel: `horror-choice-format/INTRO-FORMULA-V15.md` (receta canónica del intro 9s, validada en v15 con 9.9/10)

4. Recolectar los inputs específicos del combo. Para horror-choice × reel ver `horror-choice-format/BOOTSTRAP-NEW-PROJECT.md` § 9 (tabla de inputs FASE 0).

**Solo después** de estos 4 puntos, continuar con el paso 1 (crear directorio).

**⚠️ Gates obligatorios del flow** (cubierto en `video-director/WORKFLOW.md` Sub-loop HTML/GSAP):

Todo proyecto de video pasa por **7 gates bloqueantes** antes del stop point pre-animation:
0. ⛔ `scripts/audit-spec-completeness.py` (Gate 0 BLOQUEANTE PRIORIDAD ABSOLUTA — SPEC asset_list + ui_active inventory vs actual filesystem + index.html. Falla = STOP point INVÁLIDO. Caso disparador: matadero CP5 2026-05-19 gap #13)
1. `npx hyperframes lint` (sintaxis)
2. `scripts/audit-narrative.py` (visibilidad <1s, z-index, orphans)
3. `scripts/render-lock.py acquire <project>` (coordinación)
4. `scripts/audit-frames.py` (Gemini Vision frame-by-frame — UI overlaps, frames negros, etc.)
5. `scripts/audit-frames-granular.py` (sentinel patterns NEW 2026-05-19: audio-visual character mismatch + duplicate text + AVU sync + caption Y canonical + watermark IG safe zone. Forward: Gemini Vision integration for render-time visual deduplication. Caso disparador: matadero iter 5 D1+D2 user catches)
6. `scripts/qa-gate.py --score <X.X> --stage pre-kling --iteration <N>` (bloquea sub-9.7)

Los 6 scripts (audit-spec-completeness, audit-narrative, render-lock, audit-frames, audit-frames-granular, qa-gate) se copian del `templates/scripts/` en el paso 2 abajo. Sin estos scripts copiados al proyecto, el flow NO puede llegar al stop point.

**Learnings post-render** (reemplaza POST-MORTEM standalone, deprecated 2026-05-15): al stop point pre-animation, append 2-3 bullets al `<format>-format/video-log.md` con pattern usado, score final, qué funcionó, qué no, costo total. El video-log.md SE CONSULTA antes de cada video nuevo (rotación + cross-video lessons).

---

## 0.1 ARQUITECTURA — dónde vive qué

```
AI video 1/                                       ← raíz workspace
├── PAUTA.md, NARRATION-RULES.md, FEEDBACK-LOOP.md  ← entry docs generales
├── .claude/skills/
│   ├── ai-video-production/                      ← skill TOOLKIT (general)
│   │   └── templates/scripts/{tts,image,sfx,captions}.py  ← FUENTE de scripts
│   ├── horror-choice-format/                     ← skill de formato horror
│   └── [otros formatos futuros]                  ← documental-format, etc.
├── elige-companero/                              ← proyecto Video #1
├── bosque-abandonado/                            ← proyecto Video #2
└── <TU_PROYECTO_NUEVO>/                          ← lo que vas a crear
```

---

## 1. CREAR DIRECTORIO DEL PROYECTO

```bash
cd "<repo-root>"
mkdir -p "<TU_PROYECTO>"/{assets,scripts,renders}
mkdir -p "<TU_PROYECTO>/assets/sfx"
cd "<TU_PROYECTO>"
```

**Convención de naming**: `kebab-case`, descriptivo. Ejemplos: `elige-companero`, `bosque-abandonado`, `bosque-encantado`, `faro-vacio`.

---

## 2. COPIAR TEMPLATES (genéricos del toolkit)

Desde la raíz del proyecto nuevo:

```bash
SKILL_DIR="<repo-root>/.claude/skills/ai-video-production/templates"

# Scripts de producción (general) — incluye los 6 gates obligatorios:
#   - tts.py, image.py, sfx.py, captions.py, video.py (generación)
#   - audit-spec-completeness.py (⛔ gate 0 PRIORIDAD ABSOLUTA — SPEC inventory diff, added 2026-05-19)
#   - audit-narrative.py (gate 2 — visibilidad <1s, z-index, orphans)
#   - render-lock.py    (gate 3 — coordinación entre agentes)
#   - audit-frames.py   (gate 4 — Gemini Vision frame-by-frame)
#   - qa-gate.py        (gate 5 — bloquea sub-9.7 pre-animation)
cp "$SKILL_DIR/scripts/"*.py scripts/

# Templates de proyecto genéricos
cp "$SKILL_DIR/.env-TEMPLATE"            .env
cp "$SKILL_DIR/hyperframes.json-TEMPLATE" hyperframes.json

# (Sin POST-MORTEM — deprecated 2026-05-15; learnings van a video-log.md del formato)
```

**Verificación post-copy** — confirmar que TODOS los scripts del flow están presentes:
```bash
for script in tts.py image.py sfx.py captions.py video.py audit-spec-completeness.py audit-narrative.py render-lock.py audit-frames.py audit-frames-granular.py qa-gate.py; do
  [ -f scripts/$script ] && echo "✓ scripts/$script" || echo "✗ MISSING scripts/$script"
done
```

Si falta alguno → re-correr el `cp` desde `$SKILL_DIR`. Los 5 scripts marcados ⭐ (audit-spec-completeness, audit-narrative, render-lock, audit-frames, qa-gate) son **gates bloqueantes** del workflow — sin ellos, el agente no puede llegar al stop point pre-animation.

Si vas a producir un video del formato horror-choice, copiar también los templates específicos del formato:

```bash
HORROR_DIR="<repo-root>/.claude/skills/horror-choice-format/templates"

cp "$HORROR_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$HORROR_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$HORROR_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json
```

Para un formato distinto, copiar de su skill correspondiente.

---

## 3. CONFIGURAR `.env`

Editar y poner las API keys reales:

```bash
nano .env
```

Necesarias:
- `GEMINI_API_KEY` → https://aistudio.google.com/apikey (free tier alcanza)
- `ELEVENLABS_API_KEY` → https://elevenlabs.io/app/settings/api-keys (paid ~$22/mes)
- `REPLICATE_API_TOKEN` → solo si vas a usar animation AI para animar imágenes (Kling/Seedance/Hailuo según MODEL-BENCHMARK, ~$3/video)

Verificar:
```bash
source .env
[ -n "$GEMINI_API_KEY" ] && echo "✓ Gemini" || echo "✗ Gemini missing"
[ -n "$ELEVENLABS_API_KEY" ] && echo "✓ ElevenLabs" || echo "✗ ElevenLabs missing"
```

---

## 4. CREAR VIRTUALENV PYTHON

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install elevenlabs google-genai python-dotenv openai-whisper replicate
deactivate
```

Verificación:
```bash
.venv/bin/python -c "import elevenlabs, google.genai, dotenv; print('✓ deps ok, elevenlabs', elevenlabs.__version__)"
```

Debe imprimir `✓ deps ok, elevenlabs 2.44.0` o superior.

### Alternativa rápida (reusar venv existente)

```bash
ln -sf "<repo-root>/elige-companero/.venv" .venv
```

Funciona si estás en la misma máquina; rompe si moves el proyecto.

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

## 6. PERSONALIZAR `scripts/image.py` (si tu formato tiene STYLE_SUFFIX)

El script copiado del template tiene `HORROR_SUFFIX` hardcoded. Si tu formato es distinto, editar:

```python
# scripts/image.py

# Reemplazar HORROR_SUFFIX por el style suffix de tu formato
STYLE_SUFFIX = (
    " Documentary cinematic photography, naturalistic color grade, "
    " ... [tu estilo aquí] ... "
    "No text, no logos, no watermarks."
)
```

Y en `main()` cambiar las referencias de `HORROR_SUFFIX` a `STYLE_SUFFIX`.

Si tu formato no requiere suffix (ej: ya pasás todo el estilo en el prompt), usar `--no-mono-suffix` siempre.

---

## 7. CREAR `index.html` BASE

Copiar el esqueleto de un proyecto existente del mismo formato:

```bash
cp "<repo-root>/bosque-abandonado/index-v2.html" index.html
# Editar el <title> y limpiar el contenido por hito
```

Para formato horror-choice: usar el esqueleto de bosque-abandonado o elige-companero.
Para formato nuevo: empezar con el esqueleto base (canvas vacío 1080×1920) y construir desde cero.

---

## 8. SMOKE TESTS

### TTS

```bash
.venv/bin/python scripts/tts.py \
  -t "Prueba de voz." \
  -o assets/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/_smoketest.mp3 && \
rm assets/_smoketest.mp3
```

Si imprime duración (~2s) y borra → OK.

### SFX

```bash
.venv/bin/python scripts/sfx.py \
  -t "low sub-bass impact" -d 0.5 -o assets/sfx/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/sfx/_smoketest.mp3 && \
rm assets/sfx/_smoketest.mp3
```

### Image

```bash
.venv/bin/python scripts/image.py \
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
- [ ] `image.py` personalizado con tu STYLE_SUFFIX si aplica
- [ ] Templates del formato específico copiados (si vas a usar uno)
- [ ] Smoke tests pasados (TTS + SFX + image)
- [ ] Inputs creativos recolectados del usuario (según lo que pida el formato)

---

## 10. EL AGENTE TOMA EL VOLANTE

Decirle al agente:
> "Proyecto bootstrapeado en `<ruta>`. Combo: genre = `<genre>` × format = `<delivery>`. Skills activos: `video-director` + `ai-video-production` + `<genre>-format` + (`video-animation` si aplica). Empezá según el playbook del genre y las reglas del delivery."

Para combo **horror-choice × reel** (validado en v15-final 9.9/10):
- Agente lee `horror-choice-format/PAUTA.md`, `INTRO-FORMULA-V15.md`, `PATTERNS.md`, `VIDEO-PLAYBOOK.md`
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
El venv no se activó o las deps no se instalaron. Re-run paso 4.

### `ELEVENLABS_API_KEY environment variable is not set`
El script no encuentra `.env`. Verificar que `python-dotenv` esté instalado y que `.env` esté en la raíz del proyecto (no en `scripts/`).

### `Gemini API key not found` en image.py
Mismo problema. `load_dotenv()` busca `.env` en `PROJECT_ROOT` (el padre de `scripts/`). Confirmar que `.env` está en la raíz.

### Hyperframes no reconoce el directorio
Falta `hyperframes.json` o `index.html` en la raíz. Crear ambos antes de cualquier `hyperframes render`.

### SFX salen silenciosos
Venv tiene `elevenlabs < 2.40` (sin `text_to_sound_effects`). Actualizar:
```bash
.venv/bin/pip install --upgrade elevenlabs
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
