# BOOTSTRAP-NEW-PROJECT.md — Bootstrap específico del formato horror-choice

> ⚠️ Para el **bootstrap genérico** (cualquier formato de video con IA) ver `../ai-video-production/BOOTSTRAP.md` — pasos 1-10 con dir, venv, .env, smoke tests.
>
> Este doc cubre solo lo **específico del formato horror-choice** que se hace ENCIMA del bootstrap genérico: qué templates específicos copiar, qué inputs FASE 0 recolectar.

**Pre-requisitos:** bootstrap genérico completado (proyecto inicializado con scripts/, .venv/, .env, hyperframes.json).

---

## 0. DÓNDE VIVE QUÉ

```
<repo>/                                             ← raíz del repo
├── PAUTA.md, NARRATION-RULES.md, docs/FEEDBACK-LOOP.md  ← entry docs generales
├── .agents/skills/                                  ← skills hyperframes / gsap (compartidos)
├── .claude/skills/
│   ├── ai-video-production/                        ← toolkit GENERAL (TTS, image, SFX, motion, etc.)
│   │   └── templates/
│   │       ├── scripts/{tts,image,sfx,captions}.py
│   │       ├── .env.example
│   │       └── templates/project/hyperframes.json
│   └── horror-choice-format/                       ← formato ESPECÍFICO horror-choice (FUENTE de este doc)
│       └── templates/
│           ├── NARRATIVE-TEMPLATE.md
│           ├── SFX-LIST-TEMPLATE.md
│           ├── sfx-spec-TEMPLATE.json
│           └── FREESOUND-QUERIES-TEMPLATE.md   ← opcional fallback
├── elige-companero/                                ← proyecto Video #1 (referencia)
├── bosque-abandonado/                              ← proyecto Video #2 (referencia)
└── <NUEVO_PROYECTO>/                               ← lo que vas a crear ahora
```

---

## 1-4. ENTORNO, PROYECTO Y TEMPLATES DEL FORMATO

Seguí el bootstrap genérico (`../ai-video-production/BOOTSTRAP.md` §1-4). Para horror-choice, el paso de
templates del formato es:

```bash
cd "projects/<NUEVO_PROYECTO>"
HORROR_DIR="../../.claude/skills/horror-choice-format/templates"
cp "$HORROR_DIR/NARRATIVE-TEMPLATE.md"   NARRATIVE.md
cp "$HORROR_DIR/SFX-LIST-TEMPLATE.md"    SFX-LIST.md
cp "$HORROR_DIR/sfx-spec-TEMPLATE.json"  sfx-spec.json
# FREESOUND-QUERIES.md es fallback opcional (solo si un SFX de ElevenLabs sale uncanny):
#   cp "$HORROR_DIR/FREESOUND-QUERIES-TEMPLATE.md" FREESOUND-QUERIES.md
```

Los gates QA (`audit-narrative`, `render-lock`, `audit-frames`, `qa-gate`, …) ya están disponibles como
`uv run ai-video <gate>`; `uv run ai-video doctor` confirma keys y dependencias.

---

## 5. CREAR `hyperframes.json`

Editar el archivo copiado en paso 2:
```bash
nano hyperframes.json
# Reemplazar "[NOMBRE_PROYECTO]" con el nombre real
```

Resultado esperado:
```json
{
  "name": "bosque-encantado",
  "output": { "width": 1080, "height": 1920, "fps": 30 }
}
```

---

## 6. CREAR `index.html` BASE

Por ahora puede ser vacío o copiar el esqueleto de `bosque-abandonado/index-v2.html` (cambiar título). El contenido real se construye siguiendo `VIDEO-PLAYBOOK.md`.

```bash
cp "bosque-abandonado/index-v2.html" index.html
# Edita el <title> y limpia el contenido por hito
```

---

## 7. VERIFICAR EL FORMATO DE LOS TEMPLATES

Validá que todo está editable y no quedaron placeholders sin reemplazar:

```bash
grep -r "<NUEVO_PROYECTO>\|<aqui-tu-key\|\[NOMBRE_PROYECTO\]" . 2>/dev/null
```

No debe devolver nada en archivos que ya editaste. Los templates en `.md` mantienen sus placeholders entre corchetes hasta que tengas los inputs de FASE 0.

---

## 8. PRIMER COMANDO DE PRUEBA (smoke test)

Probar que TTS funciona end-to-end:

```bash
uv run ai-video tts \
  -t "Prueba de voz para nuevo proyecto." \
  -o assets/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/_smoketest.mp3 && \
rm assets/_smoketest.mp3
```

Si imprime una duración (~2s) y borra el archivo, **estás listo**.

Probar SFX:
```bash
uv run ai-video sfx \
  -t "low sub-bass impact" -d 0.5 -o assets/sfx/_smoketest.mp3 && \
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/sfx/_smoketest.mp3 && \
rm assets/sfx/_smoketest.mp3
```

Probar imagen:
```bash
uv run ai-video image \
  -p "test prompt: simple black square" -o assets/_smoketest.png && \
ls -la assets/_smoketest.png && \
rm assets/_smoketest.png
```

Tres pruebas pasadas → setup OK.

---

## 9. RECOLECTAR INPUTS FASE 0

Antes de que el agente arranque a producir, tener los datos. Divididos en dos bloques:

### 9.a — Inputs del DELIVERY FORMAT (eje técnico)

> Estos definen el "cómo se entrega". Default razonable: reel.

| Input | Ejemplo | Default | Si dudás |
|---|---|---|---|
| **Delivery format** | reel / youtube-short / instagram-story | **reel** (validado v15) | Si el video va a IG con duración 60-90s → reel |
| **Plataforma primaria** | IG / TikTok / ambas / YT Shorts | **IG Reels** | Afecta safe zones — ver `../ai-video-production/formats/<delivery>.md` § UI Safe Zones |
| **Duración target (segundos)** | 60 / 75 / 90 / 120 | **90s** (sweet spot validado en v15) | <60s = más viral pero menos narrativa; >90s = riesgo de retention drop |
| **Idioma captions** | es / en / pt | **es** (formato @referent-a) | Si target audience LATAM → es |

### 9.b — Inputs del GENRE horror-choice (eje narrativo)

> Cada slot tiene autoridad creativa en `PAUTA-MASTER.md` (8 videos canónicos virales). NO improvisar — consultar PAUTA-MASTER + `video-log.md` antes de elegir.

| Input | Notas / opciones | Autoridad |
|---|---|---|
| **Nombre malo aparente** | Cristóbal, Berni, Martín, Hugo, Maikol | `PAUTA-MASTER.md` § 8 catalog Slot B |
| **Nombre bueno aparente** | Gerald, Yonaiker, Tobías, Santi, Chelo | `PAUTA-MASTER.md` § 9 catalog Slot C |
| **Escenario / setting** | farmhouse, bosque, faro, mina, crucero, cabaña, calabozo | Propuesta libre dentro del archetype |
| **Verbo H1** | BAJARÍAS / ENTRARÍAS / SUBIRÍAS / CRUZARÍAS / PASARÍAS LA NOCHE | `INTRO-FORMULA.md` |
| **Pattern de matriz expandida** | NO improvisar — elegir de los 10 patterns + meta-cliffhanger | `PAUTA-MASTER.md` § 15 + `video-log.md` (rotación) |
| **Dilema H3 concreto** | primera elección binaria (mirar/no mirar, comer/no comer, entrar/quedarse) | `PAUTA-MASTER.md` § 9 |
| **Dilema H4 concreto** | segunda elección, sube apuesta | `PAUTA-MASTER.md` § 9 |
| **Twist H4→H5** | solo si pattern lo requiere (patterns 3, 8, 9, 10 + meta) | `PAUTA-MASTER.md` § 15 |
| **Cliffhanger setting H6** | "Una noche en paz" — dónde termina el cierre (cabaña, café, fogón — safe place warm contrast) | `PAUTA-MASTER.md` § 16 |
| **Slot H0 personal stakes** | OPCIONAL — NO observado en 8/8 canónicos, usar con precaución | `PAUTA-MASTER.md` (guidelines empíricas) |

**Regla de rotación pattern**: consultar `video-log.md` antes de elegir. NO repetir mismo pattern 2 videos seguidos.

Pegárselos al agente al iniciar.

---

## 9.5. ⭐ DOBLE GATE ANTES DE GENERAR ASSETS (proyectos NUEVOS, 2026-05-11)

Después de los inputs FASE 0 y antes de generar TTS/imágenes/SFX, ejecutar dos validaciones rápidas:

### 9.5.a — Character anchors

El formato horror-choice tiene 2 personajes recurrentes (malo aparente + bueno aparente). El bueno aparente **aparece en 2 contextos visualmente distintos**: H1 presentación y H6 cliffhanger (cabaña / safe place).

**Decisión obligatoria pre-render**:

| Escenario | Decisión |
|---|---|
| Bueno aparente lleva mismo outfit en H1 y H6 (zona de confort consistente) | 1 anchor — `<bueno>-anchor.png` |
| Bueno aparente justificadamente cambia (tiempo pasó, escapó al cliffhanger) | 2 anchors — `<bueno>-h1-anchor.png` + `<bueno>-h6-anchor.png` con MISMA cara y physicality |

**Anti-pattern (mina-abandonada original)**: Santi H1 ≠ Santi H6 visualmente (casco LED vs beanie, ropa azul vs marrón). Sin anchor compartido, las dos generaciones convergieron en "Santis distintos". El cliffhanger perdió fuerza.

Ver `ai-video-production/CHARACTER-CONSISTENCY.md` § BOOTSTRAP GATE para el procedimiento completo.

### 9.5.b — Continuidad captions ↔ narrador

El formato horror-choice tiene captions hardcoded típicos:
- `cap-q`: "¿CON QUIÉN BAJARÍAS?" / "¿CON QUIÉN ENTRARÍAS?" — pregunta retórica
- `cap-chose`: "SI ELEGISTE A [BUENO]..." — bridge al H3 narrador

**El cap-chose DEBE ser prefijo o continuación natural** de h3-narr1, no su versión en tiempo presente. Caso real: `cap-chose = "ELIGES A HUGO"` + `h3-narr1 = "Si elegiste a Hugo... lleva treinta años..."` produce conflicto verbal (presente vs pretérito) + redundancia.

**Fix template** (aplicar a NARRATIVE.md desde el primer borrador):

```markdown
## Captions hardcoded (intro)
- cap-q (5.7s): ¿CON QUIÉN ENTRARÍAS?
- cap-chose (7.3s): SI ELEGISTE A [BUENO_APARENTE]...

## Narrador h3-narr1 (arranca 9.2s en composición 100s, justo después de cap-chose)
"Si elegiste a [BUENO]... lleva [N] años en esta [SETTING]. Conoce las reglas..."
```

El "..." al final de cap-chose y el "Si elegiste a..." inicial del narrador encadenan visual + audio sin duplicación.

Ver `ai-video-production/QA.md` dimensión #10 (continuidad narrativa).

---

## 10. EL AGENTE TOMA EL VOLANTE

Decirle al agente:
> "Combo: horror-choice × `<delivery_format>`. Proyecto bootstrapeado en `<RUTA>`. Leí: PAUTA.md, VIDEO-PLAYBOOK.md, PATTERNS.md, INTRO-FORMULA.md, PRODUCTION-PIPELINE.md, BOOTSTRAP-NEW-PROJECT.md, `../ai-video-production/formats/<delivery>.md`, `../ai-video-production/RETENTION-RULES.md`. Inputs FASE 0: [pegar bloques 9.a + 9.b]. Empezá desde Fase 0 del VIDEO-PLAYBOOK."

El agente debe:
1. Confirmar lectura de los docs (incluyendo el doc del delivery format específico)
2. Validar inputs con test de calidad del dilema (`PATTERNS.md` § 6)
3. Validar combo en `../ai-video-production/DELIVERY-FORMATS.md` § "Matriz GENRE × FORMAT" — horror-choice × reel = ⭐ v15 validado
4. Aplicar la receta del intro de `INTRO-FORMULA.md` (slots `[SLOT]` → valores de FASE 0) para los primeros 9s del video
5. Generar NARRATIVE.md completo siguiendo SCRIPT-WRITING-GUIDE.md
6. Pedir tu aprobación del guion antes de generar assets

---

## CHECKLIST DEL BOOTSTRAP

Antes de pasar a producción confirmar:

- [ ] `<NUEVO_PROYECTO>/` creado con subfolders `assets/`, `assets/sfx/`, `scripts/`, `renders/`
- [ ] `ai-video tts`, `ai-video image`, `ai-video sfx`, `ai-video captions` copiados
- [ ] `.env` con API keys reales (Gemini + ElevenLabs mínimo)
- [ ] `.venv/` creado con deps instaladas
- [ ] `hyperframes.json` con nombre del proyecto
- [ ] `NARRATIVE.md`, `SFX-LIST.md`, `sfx-spec.json`, `FREESOUND-QUERIES.md` copiados como plantillas
- [ ] Smoke tests pasados (TTS, SFX, image)
- [ ] Inputs FASE 0 recolectados
- [ ] Agente confirmó lectura de los 5 docs core

---

## ERRORES COMUNES EN BOOTSTRAP

### Error: `ModuleNotFoundError: No module named 'elevenlabs'`
El venv no se activó o las deps no se instalaron. Re-run el paso 4.

### Error: `ELEVENLABS_API_KEY environment variable is not set`
El script no encuentra `.env`. Verificar que `python-dotenv` esté instalado y que `.env` esté en la raíz del proyecto (no en `scripts/`).

### Error: `Gemini API key not found` en ai-video image
Mismo problema. La configuración se lee de variables de entorno o de `.env` en el directorio actual / raíz del repo. Verificar con `uv run ai-video doctor`.

### Error: hyperframes no reconoce el directorio
Falta `hyperframes.json` o `index.html` en la raíz. Crear ambos antes de cualquier `hyperframes render`.

### Error: SFX salen silenciosos
Probablemente el venv tiene `elevenlabs < 2.40` y no tiene `text_to_sound_effects`. Actualizar:
```bash
uv lock --upgrade-package elevenlabs && uv sync --extra providers
```

---

## DESPUÉS DEL BOOTSTRAP

El proyecto está listo. El agente siguiente debería leer (en orden):

1. `BOOTSTRAP-NEW-PROJECT.md` (este, ya leído)
2. `PAUTA.md` (entry doc del formato)
3. `PATTERNS.md` (reglas perennes)
4. `SCRIPT-WRITING-GUIDE.md` (cómo redactar el guion)
5. `VIDEO-PLAYBOOK.md` (orden secuencial de fases)
6. `PRODUCTION-PIPELINE.md` (comandos exactos, técnico)

Y empezar Fase 0 del VIDEO-PLAYBOOK con los inputs ya recolectados.
