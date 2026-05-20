# creative-director — sistema de templates

> El arquitecto trabaja con **plantillas por tipo de video**. Cada plantilla = una carpeta dentro de `templates/` con todo lo que el arquitecto necesita saber para diseñar UN tipo específico de video (personajes, historia, tomas, ambientes, desenlaces, etc.).

---

## Estructura del sistema

```
creative-director/
├── SKILL.md                       ← Manifesto del arquitecto (cómo trabaja en general)
├── README.md                      ← Este archivo (explica el sistema)
├── INTERVIEW-FLOW.md              ← Flow general de entrevista al user (independiente del template)
├── CREATIVE-SPEC-TEMPLATE.yaml    ← Formato del output (mismo para todos los templates)
│
└── templates/
    │
    ├── elige-tu-companero/        ← TEMPLATE #1 (validado con 13 referentes virales)
    │   ├── README.md              ← Overview, cuándo usar, qué incluye
    │   ├── referent-analysis.md   ← Síntesis de los videos virales analizados
    │   ├── characters.md          ← Tipos de personajes (30+ uncanny archetypes)
    │   ├── character-pairs.md     ← Pares canónicos validados
    │   ├── story-arc.md           ← H1-H6 structure, 3 decision points
    │   ├── camera-and-shots.md    ← POV, medium, close-up uso por escena
    │   ├── environments.md        ← Catálogo de settings validados (mina, hotel, etc.)
    │   ├── plot-patterns.md       ← 10 patterns matrix apariencia × verdad
    │   ├── hooks.md               ← Hook 0-3s formulas
    │   ├── counterfactual-outros.md ← Punchlines de outro
    │   ├── keyword-highlights.md  ← Qué palabras destacar y en qué color
    │   ├── aesthetic.md           ← Paleta dual + vignette + film grain
    │   ├── audio-direction.md     ← Music genre + SFX layering + ducking direction
    │   └── example-specs/         ← Ejemplos de CREATIVE-SPEC.yaml producidos
    │
    └── (futuros templates a agregar)
        ├── frutas-30s/            ← Cuando lo agreguemos
        ├── brand-story/           ← Cuando lo agreguemos
        ├── tutorial-edu/          ← Cuando lo agreguemos
        └── ...
```

---

## Cómo el arquitecto usa este sistema

### Step 1 — Identifica el template
User dice: "quiero hacer un video tipo elige tu compañero" o "necesito un reel de frutas de 30 segundos".

Arquitecto identifica: `template = elige-tu-companero` (o `frutas-30s`).

### Step 2 — Carga el template folder
Lee TODOS los archivos dentro de `templates/<template-name>/`. Esto le da:
- Inspiración (referent-analysis del template)
- Catálogos (personajes, environments, plot patterns)
- Reglas específicas (camera, color, audio direction)
- Templates de output (example-specs)

### Step 3 — Entrevista al user (sigue INTERVIEW-FLOW.md)
Preguntas estructuradas que se adaptan al template detectado:
- Para `elige-tu-companero`: setting, archetype dyad hint, tono, stakes
- Para `frutas-30s`: producto, mood, target audience, llamada a acción
- Para `tutorial-edu`: tema, audience level, longitud, estructura

### Step 4 — Diseña proponiendo opciones del template
- "Te tiro 3 archetypes del catálogo: BRUNO+PABLO (cíclope + tubérculo), AXEL+ENZO (hongo + esquelético), o nuevos..."
- "Te tiro 2 environments: mina abandonada o acuario nocturno"
- "Para el counterfactual outro, mundano-absurdo o ternura-naive?"

### Step 5 — Produce el CREATIVE-SPEC.yaml
Format unificado independiente del template (estructura común con campos específicos según template).

---

## Cómo agregamos un nuevo template

Cuando queremos agregar (ej.) `frutas-30s`:

1. **Recolectar referentes virales:** 3-5 videos del tipo, idealmente ≥500k views, de creators distintos
2. **Análisis técnico + Gemini descriptivo** (mismo pipeline que usamos para H-choice)
3. **Aplicar la SCORING-RUBRIC.md** adaptada (algunas dimensiones pueden cambiar de peso para el formato)
4. **Crear `templates/frutas-30s/` con esta estructura mínima:**
   ```
   README.md
   referent-analysis.md
   characters.md (o products.md si aplica)
   story-arc.md (o ad-structure.md)
   camera-and-shots.md
   environments.md
   plot-patterns.md (o ad-patterns.md)
   hooks.md
   outros.md (o cta.md si es ad)
   keyword-highlights.md
   aesthetic.md
   audio-direction.md
   example-specs/
   ```
5. **Documentar las dimensiones críticas** del nuevo formato (qué gaps son más caros, qué reglas son universales vs format-specific)

---

## Filosofía del sistema

**Templates son CATALOGS de inspiración, no algoritmos rígidos.**

- El arquitecto NO copia/pega del template.
- LEE el template para entender qué es lo que "funciona" en ese tipo de video.
- LUEGO entrevista al user y CO-CREA una historia nueva que respeta la estructura del template pero con identidad propia.

**El template = el espíritu del formato. El SPEC = la historia única.**

---

## Templates actualmente disponibles

| Template | Status | Confianza | Source |
|----------|--------|-----------|--------|
| `elige-tu-companero` | ✅ Validado | Alta (13 referentes, 3 creators) | @referent-a + @referent-c + @referent-b |
| `frutas-30s` | 🔜 Por crear | n/a | Pendiente referentes |
| `brand-story` | 🔜 Por crear | n/a | Pendiente referentes |
| `tutorial-edu` | 🔜 Por crear | n/a | Pendiente referentes |

---

## Reglas universales (cross-template)

Algunas reglas aplican a TODOS los templates, no se duplican en cada carpeta. Viven en archivos al nivel root del creative-director:

- **`INTERVIEW-FLOW.md`** — estructura de entrevista (adaptable por template)
- **`CREATIVE-SPEC-TEMPLATE.yaml`** — formato del output (campos comunes + campos específicos)
- (No incluir reglas técnicas como LUFS, color CSS — eso es del ingeniero)

---

## Validación cuando se usa un template

Antes de declarar SPEC listo, el arquitecto debe haber leído:

- [ ] El `README.md` del template
- [ ] El `referent-analysis.md` del template (inspiración)
- [ ] El doc relevante a cada slot del SPEC (characters → characters.md, outro → counterfactual-outros.md, etc.)
- [ ] Cualquier `example-spec.yaml` del template

Si saltea cualquiera → puede proponer cosas no validadas → pérdida de calidad reproducible.
