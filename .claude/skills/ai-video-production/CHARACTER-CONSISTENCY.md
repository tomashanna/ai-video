# CHARACTER-CONSISTENCY.md — Personajes idénticos entre tomas

> El problema #1 de los videos generados con IA: el personaje cambia de cara entre tomas. El espectador percibe que es **otra persona** y la narrativa se rompe. Este doc resuelve eso con el sistema de **anchor + reference**.

---

## El problema

Cada llamada a Gemini Nano Banana (o cualquier modelo de generación) es independiente. Si pedís 3 imágenes de "un hombre con barba canosa caminando en el bosque", obtenés 3 hombres distintos que se parecen vagamente.

**Síntomas que el espectador detecta**:
- "¿Es el mismo personaje?"
- Cara cambia de forma sutil pero perceptible
- Ropa varía entre tomas
- Edad aparente fluctúa
- Postura / build corporal cambia

**Impacto**: rompe la inmersión narrativa. El video pierde coherencia. La audiencia siente que "está mal hecho" aunque no sepa por qué.

---

## La solución: Anchor + Reference

```
1. ANCHOR (primera imagen del personaje)
   - Generar UNA imagen "fuente de verdad" del personaje
   - Idealmente close-up frontal claro
   - Guardar como assets/<personaje>-anchor.png
   - Esta imagen NUNCA se modifica después

2. REFERENCE-BASED GENERATION (todas las siguientes)
   - Cada nueva imagen del personaje:
     INPUT: assets/<personaje>-anchor.png + texto de prompt
     OUTPUT: la nueva escena con el MISMO personaje
   - Gemini usa el anchor para mantener identidad visual
```

El modelo recibe la imagen del anchor como contexto multi-modal y genera variaciones que conservan: cara, build, edad, rasgos distintivos.

---

## Workflow paso a paso

### Paso 1 — Diseñar el anchor del personaje

Pensar el anchor antes de generarlo. Preguntas críticas:

1. **¿Qué rasgo es no-negociable?** (cara, build, ropa, edad)
2. **¿Cuál es la pose más informativa?** (close-up frontal de pecho hacia arriba suele ser óptimo)
3. **¿Qué iluminación es neutra?** (no demasiado contrastada — sino restringe variaciones)
4. **¿Qué incluir en el anchor?** (cabeza + hombros, o full body, o desde la cintura)

**Recomendación**: medium close-up (cabeza + pecho), iluminación frontal suave, fondo neutro o desenfocado, mirada al frente.

### Paso 2 — Generar el anchor

```bash
uv run ai-video image \
  -p "Medium close-up portrait of [DESCRIPTION]. Subject facing camera, neutral expression, soft frontal lighting, blurred background. Photorealistic 35mm." \
  -o assets/<personaje>-anchor.png
```

**Verificar visualmente**:
- ✅ ¿La cara está clara y bien definida?
- ✅ ¿Los rasgos clave son visibles?
- ✅ ¿La iluminación es suficiente para que se vea el rostro?

Si NO está bien → regenerar. **El anchor es la fuente de verdad — si está mal, todas las escenas heredarán el problema.**

### Paso 3 — Generar escenas usando el anchor como referencia

Para cada escena del video con ese personaje:

```bash
uv run ai-video image \
  -p "[SAME CHARACTER] walking through a dark forest at night, POV slightly behind subject, mist around them. Same lighting style as reference." \
  --ref assets/<personaje>-anchor.png \
  -o assets/h3-walk-a.png
```

El script (extendido — ver `ai-video image`) toma el anchor como input multimodal y genera una nueva escena con el mismo personaje.

### Paso 4 — Multi-character scenes

Para escenas con 2+ personajes:

```bash
uv run ai-video image \
  -p "[CHARACTER 1] and [CHARACTER 2] sitting at a table, facing each other, dim candlelight." \
  --ref assets/character1-anchor.png \
  --ref assets/character2-anchor.png \
  -o assets/h4-meeting.png
```

Pasar múltiples `--ref` para que Gemini tenga ambos personajes como contexto.

---

## Reglas críticas

### Regla 1 — Anchor PRIMERO, escenas DESPUÉS (orden no negociable)

❌ NO empezar generando escenas y "el personaje aparece como sea".
✅ Generar TODOS los anchors al inicio. Después las escenas.

### Regla 2 — UN anchor por personaje, mantener durante TODO el video

❌ NO regenerar el anchor a mitad de producción (el personaje cambia).
✅ Si el anchor "no convence" → regenerarlo ANTES de generar escenas. Una vez que generaste 3+ escenas con él, está locked.

### Regla 3 — Anchor reutilizable entre videos del mismo universo

Si tenés una serie con personajes recurrentes (ej: Berni aparece en 5 videos), el MISMO anchor sirve para los 5.

```
assets/library/characters/
  berni-anchor.png        # Mismo personaje en todos los videos donde aparece
  yonaiker-anchor.png
  hugo-anchor.png
```

Considerar agregar una carpeta `assets/library/characters/` para anchors de personajes recurrentes.

### Regla 4 — Variaciones permitidas / prohibidas

| Permitido (Gemini puede variar) | Prohibido (debe permanecer igual) |
|---|---|
| Pose, ángulo de cámara | Cara, rasgos distintivos |
| Iluminación (brillante / oscura) | Build corporal |
| Expresión facial sutil (neutra → asustada) | Edad aparente |
| Distancia de cámara (wide / medium / close-up) | Ropa principal (en video que ocurre en pocas horas) |
| Acción (caminar, sentarse, correr) | Color de piel / cabello / ojos |

### Regla 5 — Excepción narrativa: transformación

Si el personaje SE TRANSFORMA en el video (body horror, edad, posesión):
- El anchor ORIGINAL se mantiene para escenas pre-transformación
- Crear un anchor SECUNDARIO para escenas post-transformación
- Documentar la transformación como evento narrativo

```
assets/
  berni-anchor.png              # Pre-transformación
  berni-transformed-anchor.png  # Post-transformación
```

### Regla 6 — NO mezclar identidades

❌ NO usar el anchor de Berni para generar "alguien parecido a Berni pero distinto".
- Si necesitás un personaje similar pero distinto, generá su PROPIO anchor primero.

---

## Convención de naming

```
assets/
  <personaje>-anchor.png          # Anchor canónico (close-up frontal claro)
  <personaje>-sheet.png           # OPCIONAL: character sheet con múltiples ángulos
  <personaje>-h1.png              # Personaje en H1
  <personaje>-h3-a.png            # Personaje en H3 toma A
  <personaje>-h3-b.png            # Personaje en H3 toma B
  scene-<lugar>-<personaje>.png   # Escenas con personaje específico
```

---

## Implementación técnica: ai-video image extendido

El script soporta `--ref <path>` (uno o múltiples):

```bash
# Sin ref (anchor o ambiente sin personajes)
uv run ai-video image -p "..." -o assets/forest.png

# Con 1 ref (escena con 1 personaje)
uv run ai-video image -p "..." --ref assets/berni-anchor.png -o assets/h3.png

# Con 2+ refs (escena con varios personajes)
uv run ai-video image -p "..." \
  --ref assets/berni-anchor.png \
  --ref assets/yonaiker-anchor.png \
  -o assets/h1-both.png
```

Internamente Gemini recibe `contents=[image1, image2, prompt_text]` (multimodal).

---

## Prompt engineering con reference

Cuando pasás `--ref`, el prompt cambia:

### Sin referencia (anchor inicial)
```
"Medium close-up portrait of a 60-year-old gaunt man with grey hair, deep eyes,
worn dark jacket, neutral expression, soft frontal lighting, blurred dark forest background.
Photorealistic 35mm, monochrome editorial."
```

### Con referencia (escena nueva)
```
"The man from the reference image walking through a dark misty forest at night.
POV slightly behind subject. Mist swirls around him. Same character — same face,
same age, same jacket. New angle and lighting."
```

**Patrones de prompt clave con referencia**:
- "The [character] from the reference"
- "Same character — same face, same age, same [ropa]"
- "Maintain reference identity"
- "Keep facial features identical to reference"

---

## Casos de uso por formato

### Horror-choice (2 personajes + POV usuario)

```
assets/
  <malo-aparente>-anchor.png        # Generar PRIMERO
  <bueno-aparente>-anchor.png       # Generar PRIMERO
  h1-characters.png                  # Usar AMBOS anchors como --ref
  h3-cristobal-whisper.png           # Solo malo-aparente como --ref
  h6-yonaiker-people.png             # Solo bueno-aparente como --ref
```

### Documental con narrador (1 personaje)

```
assets/
  narrator-anchor.png               # Generar PRIMERO
  scene-1-narrator.png              # Con --ref del narrador
  scene-2-narrator.png              # Con --ref del narrador
  ...
```

### Educational con varios "talking heads"

```
assets/
  expert-A-anchor.png
  expert-B-anchor.png
  expert-A-explaining.png           # --ref expert-A
  expert-B-explaining.png           # --ref expert-B
  both-discussing.png               # --ref expert-A + --ref expert-B
```

---

## Cuándo NO usar reference

- **Imágenes ambientales sin personaje** (paisajes, objetos, detalles).
- **Plano de "consecuencia" abstracta** (negro, simbólico, sin sujeto humano).
- **Generación del anchor mismo** (no podés tener referencia antes del primero).
- **Personaje genuinamente nuevo en el video** que no aparece en ninguna otra escena.

---

## Anti-patterns

### ❌ Generar cada escena del personaje sin referencia
"3 imágenes de Berni" → 3 Bernis distintos. Slideshow de gemelos.

### ❌ Re-generar el anchor a mitad del video
"No me convenció, lo hago de nuevo." Después de generar 4 escenas con el anchor viejo, regenerar el anchor obliga a regenerar TODAS las escenas. Decidí bien el anchor antes de continuar.

### ❌ Cambiar la descripción del personaje entre prompts
- Anchor: "60 años, barba canosa, mandíbula angular"
- Escena con --ref: "viejo, barba blanca"
La descripción debe coincidir con el anchor para que Gemini priorice los rasgos correctos.

### ❌ Anchor con cara semi-oculta
Si el anchor es contra-luz, perfil, sombra fuerte → Gemini no puede inferir bien la cara. Resultado: las escenas con referencia tienen baja consistencia.

### ❌ Mismo anchor para personajes "similares" para ahorrar trabajo
Cada personaje único tiene anchor único. NO existe "anchor genérico de viejo".

---

## Validación: ¿el personaje quedó consistente?

Tras generar todas las escenas del personaje:

1. Abrir las imágenes en grid (Finder column view o similar)
2. Comparar caras visualmente: ¿es la MISMA persona en todas?
3. Si una imagen rompe la consistencia → regenerarla con `--ref` reforzando el prompt
4. Gemini QA del video final: si en el feedback aparece "el personaje cambia" → falla de consistencia, iterar

---

## ⭐ BOOTSTRAP GATE — Shot list validation (proyectos NUEVOS, 2026-05-11)

> **Scope explícito**: este gate aplica al **bootstrap de proyectos NUEVOS**. NO se usa para "fixear" personajes en proyectos ya en producción (mina-abandonada, bosque-abandonado, etc.) donde un personaje arrastra inconsistencias preexistentes — eso es trabajo de remediación caso por caso, no de gate.

### Por qué este gate existe

Sin este gate puede pasar lo siguiente — silenciosamente, hasta el cliffhanger del render final:

**Caso real (mina-abandonada, descubierto 2026-05-11)**:
- H1 Santi: casco LED blanco, ropa azul de trabajo, libreta + termo
- H6 Santi: beanie azul oscuro, chaqueta marrón, taza de café

Es el mismo personaje narrativamente pero el viewer no hace la conexión visual. El cliffhanger pierde el peso emocional ("ah, Santi estaba a salvo en la cabaña") porque parece otro tipo.

Ningún Gemini QA flageó esto porque cada imagen, vista aislada, es válida. La inconsistencia solo se ve recorriendo el video entero comparando frames de inicio y final.

### Procedimiento del gate

**Cuándo aplicar**: una vez que tengás el NARRATIVE.md completo del proyecto nuevo Y antes de empezar a generar imágenes (después de `BOOTSTRAP.md` paso 5, antes del paso 7).

**Steps**:

1. **Extraer del NARRATIVE.md la shot list completa** — todas las imágenes/planos planeados, separados por personaje protagónico.

2. **Para cada personaje recurrente**, listar TODOS los planos donde aparece y anotar para cada uno:
   - Setting (mismo escenario que H1 o distinto)
   - Outfit / vestuario esperado
   - Iluminación / paleta
   - Pose / acción
   - Distancia (close-up / wide / detail)

3. **Validar coherencia de outfit/identidad entre planos**:
   - ¿El personaje cambia de ropa entre escenas? → ¿Hay justificación narrativa (paso del tiempo, cambio de location)?
   - Si NO hay justificación → unificar ANTES de generar.
   - Si SÍ hay justificación → planear los puntos de transición (cambio de outfit visible o cut narrativo)

4. **Decidir anchors**:
   - 1 anchor por outfit/aparición canónica del personaje
   - Si Santi tiene "outfit mina" + "outfit cabaña cliffhanger" → 2 anchors (santi-mine-anchor.png, santi-cabin-anchor.png)
   - Documentar en NARRATIVE.md cuál anchor usa cada plano

5. **Generar anchors + spot-check antes de generar escenas**:
   - Generar los 2-N anchors
   - Confirmar visualmente que son el mismo personaje (misma cara, mismo build, mismo physicality)
   - SOLO entonces empezar a generar escenas con `--ref`

### Template — Shot list con character anchors

Agregar al final de NARRATIVE.md (proyecto nuevo):

```markdown
## CHARACTER ANCHORS

| Personaje | Anchor file | Aparece en | Outfit | Justificación si cambia |
|---|---|---|---|---|
| Hugo | hugo-anchor.png | H1, H3, H4, H5 | minero de carbón gaunt, lámpara de carbide, pickaxe | (no cambia) |
| Santi | santi-mine-anchor.png | H1 | casco LED blanco, ropa azul trabajo, libreta + termo | (aparición inicial) |
| Santi | santi-cabin-anchor.png | H6 | beanie + chaqueta marrón, taza de café | Paso del tiempo, ya escapó, está descansando |

## SHOT LIST POR PERSONAJE

### Hugo (hugo-anchor.png)
- H1 wide presentación (junto a Santi)
- H3 walk POV trasero
- H3 hugo-warn close-up cara
- H4 keep-walking medium shot
- H5 mine-exit silhouette

### Santi (santi-mine-anchor.png)
- H1 wide presentación (junto a Hugo)

### Santi (santi-cabin-anchor.png)
- H6 cabin establishing (con coffee, geology notebook)
- H6 santi-face close-up
- H6 coffee detail
```

### Anti-pattern al bootstrap-time

❌ **Generar imágenes ad-hoc por escena sin planear los anchors primero**

Cada generación independiente diverge un poco. Después de 12 imágenes el personaje del cliffhanger ya no parece el mismo del intro.

❌ **Asumir "el modelo lo va a reconocer porque el nombre es el mismo"**

Gemini Nano Banana / Imagen no tiene memoria entre llamadas. Si no le pasás el anchor con `--ref`, cada generación es un personaje nuevo similar pero no idéntico.

### Cómo este gate se conecta con BOOTSTRAP.md

Ver `BOOTSTRAP.md` paso 5.5 (recién agregado): "Validación de shot list con character anchors antes de generar imágenes".

---

## Próximos niveles (futuro)

Cuando el proyecto crezca:

1. **Character LoRA training** (Civitai / Replicate) — entrenar modelo específico del personaje. Más caro pero da consistencia 99%.
2. **Character sheet pipeline** — generar primero un sheet con 4-6 ángulos canónicos, después escenas referencian al sheet.
3. **Library de personajes recurrentes** (`assets/library/characters/`) — anchors compartidos entre videos.

---

## Cross-references

- `IMAGE-VARIETY.md` — variantes -a/-b/-c (combinar con character consistency: variantes mismas, mismo personaje)
- `PIPELINE.md` § 2 — generación de imágenes general
- `BOOTSTRAP.md` — ahora incluye "anchor first" como paso explícito
- `ai-video image` — soporta `--ref`
