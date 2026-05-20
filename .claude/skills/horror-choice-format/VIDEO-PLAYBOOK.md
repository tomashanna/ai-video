# VIDEO-PLAYBOOK.md — Guía completa para producir un video desde cero

> Este documento es un playbook secuencial. Seguilo en orden y tendrás un video completo. Cada sección dice qué generar, cómo generarlo, y cómo validarlo antes de seguir. Diseñado para que otra instancia de Claude lo siga sin preguntas.

**Referencia técnica:** `PRODUCTION-PIPELINE.md` (comandos exactos)
**Reglas del formato:** `PATTERNS.md` (nunca romper)
**Reglas de guion:** `SCRIPT-WRITING-GUIDE.md` (seguir checklist)
**Setup del proyecto:** `BOOTSTRAP-NEW-PROJECT.md` (si todavía no hay proyecto)

---

## ORDEN DE FASES (actualizado V8)

```
0. INPUTS         → 5 datos del usuario
1. SCRIPT         → NARRATIVE.md completo
2. ASSET PLAN     → planos distintos V8-1 + SFX list V8-2 + motion plan V8-3 + plan de música
2.5. IMAGES       → generar imágenes (PLANOS DISTINTOS por escena, ver IMAGE-VARIETY.md)
3. TTS            → narración + atempo 2x + medir duraciones
3.5. CAPTIONS ⚠️  → Whisper auto-gen HARD GATE — jamás hand-time
4. MÚSICA ⚠️      → 2-3 segmentos: horror (H1-H5) + cliffhanger cálido (H6)
4.5. SFX          → ElevenLabs Sound Effects batch (INCLUYE tick.mp3 para countdown)
5. COMPOSITION    → index.html con reglas V7 + V7-7 safe zones
5.5. MOTION PASS  → aplicar V8-3 (Ken Burns + parallax + flicker + glitch + etc.)
6. RENDER + QA    → Gemini Video Analyzer (9 dim) + REVISIÓN HUMANA (Gemini no detecta todo)
7. FINAL          → render high quality + publicación
```

**⚠️ FASES CRÍTICAS QUE NO SE PUEDEN SALTAR (aprendizaje mina-abandonada v1, 2026-05-10):**

- **3.5 captions Whisper** — no hand-timing. CADA frase del narrador debe tener caption sincronizado. En v1 escribí 23 captions a mano cuando el narrador decía ~45 frases. El espectador sin audio (75% de Instagram) pierde la historia.
- **4 música** — el video sin música real (solo ambient SFX) se siente "narrador con efectos", no cine. La música hace heavy-lift atmosférico.
- **Tick.mp3** — sin sonido de countdown 3-2-1 los countdowns se sienten silenciosos. tick.mp3 ahora está en `sfx-spec-TEMPLATE.json`.
- **Gemini QA es necesario pero NO suficiente** — Gemini no detecta variantes-too-similar (planos del mismo tipo) ni captions incompletos. Validar también con criterio humano.

---

## FASE 0 — INPUTS DEL USUARIO (10 min)

Antes de generar nada, recolectá estos 5 datos. Sin todos, no arrancás.

| Input | Ejemplo Video #1 | Descripción |
|-------|-----------------|-------------|
| Nombre personaje malo aparente | CRISTÓBAL | Monstruoso visualmente, tiene diálogo |
| Nombre personaje bueno aparente | GERALD / Yerald (TTS) | Extraño pero pacífico, sin diálogo |
| Escenario | Casa rural de noche | Dónde transcurre la historia |
| Dilema 1 | Curiosidad vs obediencia (mirar/no mirar) | Categoría de PATTERNS.md sección 6 |
| Dilema 2 | Sumisión a instinto vs resistencia (comer/no comer) | Segunda elección interna |

Una vez confirmados, generá el guion con `SCRIPT-WRITING-GUIDE.md`. Validá con el checklist de ese documento antes de continuar.

**Test de calidad del dilema antes de seguir:**
- ¿La tentación mala es genuinamente deseable para el espectador? Si no, rediseñá el dilema.
- ¿La opción ganadora va contra el impulso primario? Si no, invertí las opciones.

---

## FASE 0.5 — ASSET PLAN V8 (15 min) ⭐ NUEVA

> Aprendida del post-mortem de bosque-abandonado v2. Sin este plan, los assets salen incompletos y el video pasa V7 pero no V8.

Antes de generar nada, escribir 3 listas en `NARRATIVE.md` (ver `templates/NARRATIVE-TEMPLATE.md`):

### 2.1 Lista de variantes de imagen (V8-1)

Para cada escena del video, calcular su duración total y determinar variantes:

| Duración total | Variantes mínimas |
|---|---|
| ≤ 4s | 1 |
| 4–8s | 2 (`-a`, `-b`) |
| > 8s | 3 (`-a`, `-b`, `-c`) |

Ejemplo:
```
- h3-wide: duración total 9.5s → 3 variantes (-a/-b/-c)
- h3-char: duración total 2.3s → 1 (no requiere variantes)
- h4-tension: duración total 6.0s → 2 variantes (-a/-b)
```

### 2.2 Lista de SFX por escena (V8-2)

Listar TODO sonido por hito, cada uno con timestamp + descripción + duración + influence + loop si aplica. Mínimo orientativo:

| Hito | SFX típicos |
|---|---|
| H1 | distant howl, name reveal stab |
| H2 | loading drone, flash impact, glass shatter soft |
| H3 | footsteps loop, whisper, second footsteps behind, breath behind, flash impact, cold grip / body fall, release exhale |
| H4 | similar a H3 |
| H5 | gravel footsteps, presence disappear |
| H6 | warm whoosh, fire crackle loop, cup toast, warm pad |

**Capa continua (ambient):** forest wind 0–72s + dawn warmth 72–82s. Estos son Freesound (loops largos no los hace ElevenLabs).

Total típico: **25-30 SFX dedicados** + 6 Freesound auxiliares. Usar `templates/SFX-LIST-TEMPLATE.md` como base.

### 2.3 Plan de motion por escena (V8-3)

Para cada plano, definir qué motion lleva más allá del Ken Burns base. Tabla en `NARRATIVE.md`:

| Plano | Duración | Ken Burns | Parallax | Flicker | Shake | Vignette pulse | Glitch | Glow | Niebla |
|---|---|---|---|---|---|---|---|---|---|
| h1-characters | 7s | ✅ | – | – | – | – | – | – | – |
| h3-wide (a/b/c) | 9.5s | ✅ | ✅ | – | – | – | – | – | ✅ |
| h3-char | 2.3s | ✅ | – | ✅ | ✅ | – | – | – | – |
| h3-twist-bad | 3.3s | – | – | – | – | – | ✅ | – | – |
| h6-fire | 3s | ✅ | – | ✅ | – | – | – | – | partículas |

Esto se implementa en Fase 5.5, pero **se diseña ahora** para que el guion vaya alineado con el motion.

### Gate antes de Fase 1

Antes de generar imágenes, validar que NARRATIVE.md tiene:
- [ ] Lista de variantes de imagen por escena con cantidades correctas según duración
- [ ] Lista de SFX por hito (~25-30 + 6 Freesound) — guardado también en `SFX-LIST.md` o como `sfx-spec.json`
- [ ] Plan de motion por escena

Sin esto, NO arrancar generación de assets — se vuelve un caos a corregir.

---

## FASE 1 — IMAGEN DE PRESENTACIÓN + AUDIO HITO 1 (20 min)

### 1.1 Imagen de los dos personajes (`assets/h1-characters.png`)

> Hito 1 dura ~10s — según tabla V8-1 requiere ≥ 2 variantes si vas a aplicarle Ken Burns serio. Para H1 una sola es aceptable si vas a hacer un push-in lento sin cortes.
> En H3/H4/H5/H6 las variantes son obligatorias siempre.

Prompt template:
```
Split composition, side by side, dead center, full body portrait.
LEFT: [DESCRIPCIÓN_MALO] — [COLOR_ROPA], [POSTURA], [DETALLE_MONSTRUOSO].
RIGHT: [DESCRIPCIÓN_BUENO] — [COLOR_ROPA], [POSTURA], [DETALLE_UNCANNY].
Both standing, facing camera. Dark road or [ESCENARIO] background, night.
Symmetrical composition, cold blue-green lighting from above.
```

Ejemplo Video #1:
```
Split composition, side by side, dead center, full body portrait.
LEFT: Cristóbal — large beetle head with compound eyes and mandibles, white dress shirt, grey trousers, standing upright, arms at sides.
RIGHT: Gerald — elderly man with an unnaturally wide smile showing too many teeth, beige cardigan, plaid shirt, hands clasped in front, slightly tilted head.
Both standing facing camera. Dark rural road at night background.
Symmetrical composition, cold blue-green overhead lighting.
```

### 1.2 Narración Hito 1

Texto: `"Elige a tu compañero. Para esta noche, [NOMBRE_MALO]... o [NOMBRE_BUENO]."`

```bash
.venv/bin/python scripts/tts.py -t "Elige a tu compañero. Para esta noche, [NOMBRE_MALO]... o [NOMBRE_BUENO]." -v Tj9l48J9AJbry5yCP5eW -o assets/narration-raw.mp3
ffmpeg -y -i assets/narration-raw.mp3 -filter:a "atempo=2.0" assets/narration.mp3
ffprobe -v error -show_entries format=duration -of csv=p=0 assets/narration.mp3
# Guardar duración como DUR_H1_NARR
```

### 1.3 HTML Hito 1 (template)

```html
<!-- HITO 1 — Presentación (0–[T_H1_END]s) -->
<img id="scene" src="assets/characters.png" class="scene-image" style="opacity:1;" />

<div class="name-label" id="label-cristobal" style="opacity:0;">[NOMBRE_MALO_UPPER]</div>
<div class="name-label" id="label-gerald"    style="opacity:0; right:60px; left:auto;">[NOMBRE_BUENO_UPPER]</div>

<div class="caption-wrap">
  <div id="cap-1" class="caption caption-abs" style="opacity:0;">ELIGE A TU COMPAÑERO</div>
  <div id="cap-2" class="caption caption-abs" style="opacity:0;">PARA ESTA NOCHE,</div>
  <div id="cap-3" class="caption caption-abs" style="opacity:0;">[NOMBRE_MALO_UPPER] O [NOMBRE_BUENO_UPPER].</div>
</div>

<audio id="narr-h1" class="clip" src="assets/narration.mp3" data-start="1.0" data-duration="[DUR_H1_NARR]" data-track-index="1" data-volume="1.0"></audio>
```

**T_H1_END = 1.0 + DUR_H1_NARR + 1.0** (1s de inicio + narración + 1s final)

---

## FASE 2 — HITO 2: COUNTDOWN INICIAL (no genera assets nuevos)

El Hito 2 reutiliza `assets/tick.mp3` (ya existe). Solo HTML y GSAP.

**Duración:** 6s (T_H1_END → T_H1_END + 6)
**T_H2_START = T_H1_END**
**T_H2_END = T_H2_START + 6**

```html
<!-- HITO 2 — Countdown (T_H2_START–T_H2_END) -->
<div id="loading-wrap" class="loading-bar-wrap" style="opacity:0; bottom:420px;">
  <div class="choice-label">A. [NOMBRE_MALO_UPPER]</div>
  <div class="choice-label">B. [NOMBRE_BUENO_UPPER]</div>
  <div class="loading-bar-track" style="margin-top:14px;">
    <div id="loading-fill" class="loading-bar-fill"></div>
  </div>
</div>
<audio id="tick-h2-3" class="clip" src="assets/tick.mp3" data-start="[T_H2_START]"     data-duration="0.1" data-track-index="5"  data-volume="0.8"></audio>
<audio id="tick-h2-2" class="clip" src="assets/tick.mp3" data-start="[T_H2_START+1.0]" data-duration="0.1" data-track-index="6"  data-volume="0.8"></audio>
<audio id="tick-h2-1" class="clip" src="assets/tick.mp3" data-start="[T_H2_START+2.0]" data-duration="0.1" data-track-index="7"  data-volume="0.8"></audio>
```

---

## FASE 3 — HITO TIPO "HISTORIA CON ELECCIÓN" (Hitos 3 y 4)

Este es el hito de mayor producción. Seguir este orden exacto.

### 3.1 Generar narración (4 bloques)

| Bloque | Contenido | Duración esperada (2x) |
|--------|-----------|------------------------|
| narr1 | Setup del escenario + lo que ves | 5–8s |
| narr2 | Personaje da advertencia o instrucción | 1.5–2.5s |
| narr3 | "Ahora decide." | ~1s |
| narr4 | Twist dual: "Si [malo]... Si [bueno]..." | 6–9s |

```bash
# Generar los 4 raw
.venv/bin/python scripts/tts.py -t "[NARR1_TEXT]" -v Tj9l48J9AJbry5yCP5eW -o assets/hN-narr1-raw.mp3
.venv/bin/python scripts/tts.py -t "[NARR2_TEXT]" -v Tj9l48J9AJbry5yCP5eW -o assets/hN-narr2-raw.mp3
.venv/bin/python scripts/tts.py -t "Ahora decide." -v Tj9l48J9AJbry5yCP5eW -o assets/hN-narr3-raw.mp3
.venv/bin/python scripts/tts.py -t "[NARR4_TEXT]" -v Tj9l48J9AJbry5yCP5eW -o assets/hN-narr4-raw.mp3

# Procesar todos a 2x
for f in hN-narr1 hN-narr2 hN-narr3 hN-narr4; do
  ffmpeg -y -i assets/${f}-raw.mp3 -filter:a "atempo=2.0" assets/${f}-2x.mp3
  echo "$f: $(ffprobe -v error -show_entries format=duration -of csv=p=0 assets/${f}-2x.mp3)s"
done
```

Guardar: DUR_N1, DUR_N2, DUR_N3, DUR_N4

### 3.2 Calcular timestamps

```
T_START     = T_fin_hito_anterior
T_NARR2     = T_START + DUR_N1
T_NARR3     = T_NARR2 + DUR_N2
T_COUNTDOWN = T_NARR3 + DUR_N3 + 0.2   (pequeño gap)
T_TWIST     = T_COUNTDOWN + 3.0         (countdown 3s)
T_MIDTWIST  = T_TWIST + (DUR_N4 × 0.55) (split narr4: ~55% malo / 45% bueno)
T_END       = T_TWIST + DUR_N4

# Para captions de narr1 (dividir en 2 partes iguales si hay 2 frases):
T_CAP1A_END = T_START + (DUR_N1 × 0.5)
```

### 3.3 Generar 4–5 imágenes (con variantes V8-1)

| ID | Descripción | Cuándo aparece | Variantes según duración |
|----|-------------|----------------|--------------------------|
| `hN-wide-a/b/c` | POV entrando/sentado en el escenario, wide shot | T_START → T_NARR2 | 2-3 variantes (suele durar >4s) |
| `hN-char` | Close-up del personaje malo dando la advertencia | T_NARR2 → T_COUNTDOWN | 1 (suele durar <4s) |
| `hN-tension-a/b` | Close-up del elemento de tensión (objeto/monstruo) | T_COUNTDOWN → T_TWIST | 2 (suele durar 4-7s) |
| `hN-twist-bad` | Consecuencia visual si el espectador elige mal | T_TWIST → T_MIDTWIST | 1 |
| `hN-twist-good` | Salida/reconocimiento si elige bien | T_MIDTWIST → T_END | 1 |

**Comando para variantes en paralelo:**
```bash
# Generar A primero (la principal)
.venv/bin/python scripts/image.py -p "[PROMPT_A]" -o assets/hN-wide-a.png &

# Variantes B y C en paralelo
.venv/bin/python scripts/image.py -p "[PROMPT_B_distinta_distancia]" -o assets/hN-wide-b.png &
.venv/bin/python scripts/image.py -p "[PROMPT_C_distinto_ángulo]" -o assets/hN-wide-c.png &
wait
```

Diseño de variantes: cambiar **ángulo / distancia / pose / framing** — NUNCA escenario o personajes. Ver PRODUCTION-PIPELINE § 2.5.

**Symlink de backward-compat** (si el HTML ya referenciaba el nombre sin sufijo):
```bash
cd assets/ && ln -sf hN-wide-a.png hN-wide.png
```

Prompt template por tipo:

**Wide shot (hN-wide):**
```
First-person POV [acción: entering/seated at/walking toward] [ESCENARIO].
[DESCRIPCIÓN_AMBIENTE_3_DETALLES]. [PERSONAJES_SI_APLICA].
Wide shot, slightly low angle from [posición del POV].
```

**Close-up personaje (hN-char):**
```
Extreme close-up of [DESCRIPCIÓN_PERSONAJE] leaning toward camera,
[ACCIÓN_CRÍPTICA: whispering / pointing / tilting head].
[DETALLE_FÍSICO_UNO]. [LUZ_AMBIENTE]. No background visible.
```

**Elemento tensión (hN-tension):**
```
Extreme close-up of [OBJETO_O_CRIATURA] [ESTADO].
[DETALLE_1]. [DETALLE_2]. Cold overhead light. Dead-center composition.
```

**Twist malo (hN-twist-bad):**
```
First-person POV looking at/down at [CONSECUENCIA_VISUAL].
[DESCRIPCIÓN_HORROR_SIN_SANGRE_NI_CORTES]. Cold blue light. Horror body transformation / extreme close-up.
```

**Twist bueno (hN-twist-good):**
```
First-person POV [ACCIÓN_DE_SALIDA: walking toward door / being gestured out / returning to calm].
[DETALLE_1]. [PERSONAJE_ACTUANDO_BIEN]. Night exterior visible. Cold-to-warm light transition.
```

### 3.4 HTML template Hito historia (copiar/pegar y rellenar slots)

```html
<!-- HITO [N] — Historia con elección (T_START–T_END) -->

<!-- Imágenes -->
<img id="h[N]-wide"       src="assets/h[N]-wide.png"       class="scene-image clip" style="opacity:0;" data-start="[T_START]"    data-duration="[DUR_N1+DUR_N2]" data-track-index="[IDX]"   />
<img id="h[N]-char"       src="assets/h[N]-char.png"       class="scene-image clip" style="opacity:0;" data-start="[T_NARR2]"    data-duration="[DUR_N2+DUR_N3+3.5]" data-track-index="[IDX+1]" />
<img id="h[N]-twist-bad"  src="assets/h[N]-twist-bad.png"  class="scene-image clip" style="opacity:0;" data-start="[T_TWIST]"    data-duration="[DUR_N4*0.55]"   data-track-index="[IDX+2]" />
<img id="h[N]-twist-good" src="assets/h[N]-twist-good.png" class="scene-image clip" style="opacity:0;" data-start="[T_MIDTWIST]" data-duration="[DUR_N4*0.45]"   data-track-index="[IDX+3]" />

<!-- Captions -->
<div class="caption-wrap">
  <div id="h[N]-cap-1a" class="caption caption-abs" style="opacity:0;">[CAPTION_NARR1_PRIMERA_FRASE]</div>
  <div id="h[N]-cap-1b" class="caption caption-abs" style="opacity:0;">[CAPTION_NARR1_SEGUNDA_FRASE]</div>
  <div id="h[N]-cap-2"  class="caption caption-abs" style="opacity:0;">[CAPTION_NARR2]</div>
  <div id="h[N]-cap-3"  class="caption caption-abs" style="opacity:0;">AHORA DECIDE.</div>
  <div id="h[N]-cap-bad"  class="caption caption-abs" style="opacity:0; white-space:normal; text-align:center; width:920px; font-size:68px; line-height:1.1;">[CAPTION_TWIST_BAD — todo en mayúsculas]</div>
  <div id="h[N]-cap-good" class="caption caption-abs" style="opacity:0;">[CAPTION_TWIST_GOOD — todo en mayúsculas]</div>
</div>

<!-- Loading bar -->
<div id="h[N]-loading-wrap" class="loading-bar-wrap" style="opacity:0; bottom:420px;">
  <div class="choice-label">A. [OPCION_MALA_2_PALABRAS]</div>
  <div class="choice-label">B. [OPCION_BUENA_2_PALABRAS]</div>
  <div class="loading-bar-track" style="margin-top:14px;">
    <div id="h[N]-loading-fill" class="loading-bar-fill"></div>
  </div>
</div>

<!-- Ticks (reutilizan assets/tick.mp3) -->
<audio id="h[N]-tick-3" class="clip" src="assets/tick.mp3" data-start="[T_COUNTDOWN]"     data-duration="0.1" data-track-index="[IDX+4]" data-volume="0.8"></audio>
<audio id="h[N]-tick-2" class="clip" src="assets/tick.mp3" data-start="[T_COUNTDOWN+1.0]" data-duration="0.1" data-track-index="[IDX+5]" data-volume="0.8"></audio>
<audio id="h[N]-tick-1" class="clip" src="assets/tick.mp3" data-start="[T_COUNTDOWN+2.0]" data-duration="0.1" data-track-index="[IDX+6]" data-volume="0.8"></audio>

<!-- Narración -->
<audio id="h[N]-narr1" class="clip" src="assets/h[N]-narr1-2x.mp3" data-start="[T_START]"    data-duration="[DUR_N1]" data-track-index="[IDX+7]"  data-volume="1.0"></audio>
<audio id="h[N]-narr2" class="clip" src="assets/h[N]-narr2-2x.mp3" data-start="[T_NARR2]"    data-duration="[DUR_N2]" data-track-index="[IDX+8]"  data-volume="1.0"></audio>
<audio id="h[N]-narr3" class="clip" src="assets/h[N]-narr3-2x.mp3" data-start="[T_NARR3]"    data-duration="[DUR_N3]" data-track-index="[IDX+9]"  data-volume="1.0"></audio>
<audio id="h[N]-narr4" class="clip" src="assets/h[N]-narr4-2x.mp3" data-start="[T_TWIST]"    data-duration="[DUR_N4]" data-track-index="[IDX+10]" data-volume="1.0"></audio>
```

### 3.5 GSAP template Hito historia (copiar/pegar y sustituir T_ y DUR_)

```js
/* ===== HITO [N] (t=[T_START]–[T_END]s) ===== */

/* White flash entrada */
tl.set("#flash-white", { opacity: 0.9 }, [T_START]);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_START] + 0.001);

/* h[N]-wide: wide shot escenario */
tl.set("#h[N]-wide", { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-wide", { opacity: 1 }, [T_START]);
tl.to( "#h[N]-wide", { scale: 1.04, duration: [DUR_N1+DUR_N2], ease: "sine.inOut" }, [T_START]);
tl.set("#h[N]-wide", { opacity: 0 }, [T_NARR2]);

/* h[N]-char: personaje dando advertencia */
tl.set("#h[N]-char", { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-char", { opacity: 1 }, [T_NARR2]);
tl.to( "#h[N]-char", { scale: 1.03, duration: [DUR_N2+DUR_N3+3.5], ease: "sine.inOut" }, [T_NARR2]);
tl.set("#h[N]-char", { opacity: 0 }, [T_TWIST]);

/* h[N]-twist-bad: consecuencia mala */
tl.set("#h[N]-twist-bad", { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-twist-bad", { opacity: 1 }, [T_TWIST]);
tl.to( "#h[N]-twist-bad", { scale: 1.04, duration: [DUR_N4*0.55], ease: "sine.inOut" }, [T_TWIST]);
tl.set("#h[N]-twist-bad", { opacity: 0 }, [T_MIDTWIST]);

/* h[N]-twist-good: salida buena */
tl.set("#h[N]-twist-good", { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-twist-good", { opacity: 1 }, [T_MIDTWIST]);
tl.to( "#h[N]-twist-good", { scale: 1.03, duration: [DUR_N4*0.45], ease: "sine.inOut" }, [T_MIDTWIST]);
tl.set("#h[N]-twist-good", { opacity: 0 }, [T_END]);

/* Captions setup → tensión */
tl.set("#h[N]-cap-1a", { opacity: 1 }, [T_START]);      tl.set("#h[N]-cap-1a", { opacity: 0 }, [T_CAP1A_END]);
tl.set("#h[N]-cap-1b", { opacity: 1 }, [T_CAP1A_END]);  tl.set("#h[N]-cap-1b", { opacity: 0 }, [T_NARR2]);
tl.set("#h[N]-cap-2",  { opacity: 1 }, [T_NARR2]);      tl.set("#h[N]-cap-2",  { opacity: 0 }, [T_NARR3]);
tl.set("#h[N]-cap-3",  { opacity: 1 }, [T_NARR3]);      tl.set("#h[N]-cap-3",  { opacity: 0 }, [T_COUNTDOWN]);

/* Countdown 3→2→1 */
tl.set("#cnt-3", { opacity: 1 }, [T_COUNTDOWN]);       tl.set("#cnt-3", { opacity: 0 }, [T_COUNTDOWN]+1.0);
tl.set("#cnt-2", { opacity: 1 }, [T_COUNTDOWN]+1.0);   tl.set("#cnt-2", { opacity: 0 }, [T_COUNTDOWN]+2.0);
tl.set("#cnt-1", { opacity: 1 }, [T_COUNTDOWN]+2.0);   tl.set("#cnt-1", { opacity: 0 }, [T_TWIST]);

tl.set("#flash-white", { opacity: 0.9 }, [T_COUNTDOWN]);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_COUNTDOWN]+0.001);
tl.set("#flash-white", { opacity: 0.9 }, [T_COUNTDOWN]+1.0);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_COUNTDOWN]+1.001);
tl.set("#flash-white", { opacity: 0.9 }, [T_COUNTDOWN]+2.0);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_COUNTDOWN]+2.001);

/* Loading bar */
tl.set("#h[N]-loading-wrap", { opacity: 1 }, [T_COUNTDOWN]);
tl.to( "#h[N]-loading-fill", { width: "100%", duration: 3.0, ease: "none" }, [T_COUNTDOWN]);
tl.set("#h[N]-loading-wrap", { opacity: 0 }, [T_TWIST]+0.1);

/* White flash twist */
tl.set("#flash-white", { opacity: 0.9 }, [T_TWIST]);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_TWIST]+0.001);

/* Twist captions */
tl.set("#h[N]-cap-bad",  { opacity: 1 }, [T_TWIST]);     tl.set("#h[N]-cap-bad",  { opacity: 0 }, [T_MIDTWIST]);
tl.set("#h[N]-cap-good", { opacity: 1 }, [T_MIDTWIST]);  tl.set("#h[N]-cap-good", { opacity: 0 }, [T_END]);

tl.set({}, {}, [T_END]);
```

---

## FASE 4 — HITO TIPO "RESOLUCIÓN" (Hito 5: escape)

Estructura más simple — sin elección, sin countdown. Solo narración + 2–3 imágenes.

### 4.1 Narración (2–3 bloques)

| Bloque | Contenido | Duración (2x) |
|--------|-----------|---------------|
| narr1 | Salida del lugar | 2.5–4s |
| narr2 | Tránsito (coche, camino) | 1.5–2.5s |
| narr3 | Llegada + estado final | 3–5s |

### 4.2 Calcular timestamps

```
T_START  = T_fin_hito_anterior
T_NARR2  = T_START + DUR_N1
T_NARR3  = T_NARR2 + DUR_N2
T_END    = T_NARR3 + DUR_N3
```

### 4.3 HTML template Hito resolución

```html
<!-- HITO [N] — Resolución (T_START–T_END) -->
<img id="h[N]-exit"    src="assets/h[N]-exit.png"    class="scene-image clip" style="opacity:0;" data-start="[T_START]"  data-duration="[DUR_N1]"         data-track-index="[IDX]"   />
<img id="h[N]-transit" src="assets/h[N]-transit.png" class="scene-image clip" style="opacity:0;" data-start="[T_NARR2]"  data-duration="[DUR_N2]"         data-track-index="[IDX+1]" />
<img id="h[N]-arrive"  src="assets/h[N]-arrive.png"  class="scene-image clip" style="opacity:0;" data-start="[T_NARR3]"  data-duration="[DUR_N3]"         data-track-index="[IDX+2]" />

<div class="caption-wrap">
  <div id="h[N]-cap-1" class="caption caption-abs" style="opacity:0;">[CAPTION_NARR1]</div>
  <div id="h[N]-cap-2" class="caption caption-abs" style="opacity:0;">[CAPTION_NARR2]</div>
  <div id="h[N]-cap-3" class="caption caption-abs" style="opacity:0;">[CAPTION_NARR3]</div>
</div>

<audio id="h[N]-narr1" class="clip" src="assets/h[N]-narr1-2x.mp3" data-start="[T_START]" data-duration="[DUR_N1]" data-track-index="[IDX+3]" data-volume="1.0"></audio>
<audio id="h[N]-narr2" class="clip" src="assets/h[N]-narr2-2x.mp3" data-start="[T_NARR2]" data-duration="[DUR_N2]" data-track-index="[IDX+4]" data-volume="1.0"></audio>
<audio id="h[N]-narr3" class="clip" src="assets/h[N]-narr3-2x.mp3" data-start="[T_NARR3]" data-duration="[DUR_N3]" data-track-index="[IDX+5]" data-volume="1.0"></audio>
```

### 4.4 GSAP template Hito resolución

```js
/* ===== HITO [N] — Resolución (t=[T_START]–[T_END]s) ===== */

tl.set("#flash-white", { opacity: 0.9 }, [T_START]);
tl.to( "#flash-white", { opacity: 0, duration: 0.1, ease: "power2.out" }, [T_START]+0.001);

tl.set("#h[N]-exit",    { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-exit",    { opacity: 1 }, [T_START]);
tl.to( "#h[N]-exit",    { scale: 1.03, duration: [DUR_N1], ease: "sine.inOut" }, [T_START]);
tl.set("#h[N]-exit",    { opacity: 0 }, [T_NARR2]);

tl.set("#h[N]-transit", { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-transit", { opacity: 1 }, [T_NARR2]);
tl.to( "#h[N]-transit", { scale: 1.03, duration: [DUR_N2], ease: "sine.inOut" }, [T_NARR2]);
tl.set("#h[N]-transit", { opacity: 0 }, [T_NARR3]);

tl.set("#h[N]-arrive",  { opacity: 0, scale: 1.0 }, 0);
tl.set("#h[N]-arrive",  { opacity: 1 }, [T_NARR3]);
tl.to( "#h[N]-arrive",  { scale: 1.03, duration: [DUR_N3], ease: "sine.inOut" }, [T_NARR3]);
tl.set("#h[N]-arrive",  { opacity: 0 }, [T_END]);

tl.set("#h[N]-cap-1", { opacity: 1 }, [T_START]);  tl.set("#h[N]-cap-1", { opacity: 0 }, [T_NARR2]);
tl.set("#h[N]-cap-2", { opacity: 1 }, [T_NARR2]);  tl.set("#h[N]-cap-2", { opacity: 0 }, [T_NARR3]);
tl.set("#h[N]-cap-3", { opacity: 1 }, [T_NARR3]);  tl.set("#h[N]-cap-3", { opacity: 0 }, [T_END]);

tl.set({}, {}, [T_END]);
```

---

## FASE 5 — HITO TIPO "CLIFFHANGER" (Hito 6 — siempre el último)

**Único hito con color cálido (ámbar/dorado).** CSS class `.warm-tint` debe activarse.

### 5.1 Narración (1 bloque pausado, ~16s a 2x)

Texto exacto usando la plantilla:
> "Si hubieras elegido a [NOMBRE_BUENO], habrían [ACCIÓN_PAZ]. Una noche en paz."

Parámetro especial: velocidad más lenta — si el atempo 2x suena apresurado, probar `atempo=1.8`.

### 5.2 Imagen

1 imagen única, plano POV:
```
First-person POV looking at [ESCENA_CÁLIDA_DESEABLE].
[NOMBRE_BUENO] appears [DESCRIPCIÓN_CÁLIDA_NO_UNCANNY — cara normal, sonrisa genuina, copa de vino o similar].
[NOMBRE_BUENO] is NOT the center of the frame — seated to the side, observing warmly.
Warm amber and golden lighting throughout. No cold tones anywhere.
[DETALLE_SENSORIAL_1]. [DETALLE_SENSORIAL_2].
```

**CRÍTICO:** la imagen del bueno aparente en el cliffhanger debe ser DIFERENTE a la del Hito 1. Cara genuinamente normal y cálida, sin uncanny valley.

### 5.3 Activar warm tint en CSS

En el `<style>`, agregar:
```css
.warm-tint {
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 1200px 1800px at 50% 50%,
    rgba(180, 100, 20, 0.15) 0%,
    rgba(120, 60, 0, 0.08) 60%,
    rgba(0,0,0,0) 100%);
  pointer-events: none;
  z-index: 36;
}
```

Y en HTML del Hito 6: `<div id="warm-tint" class="warm-tint" style="opacity:0;"></div>`

### 5.4 GSAP — activar warm tint

```js
tl.set("#warm-tint", { opacity: 0 }, 0);
tl.set("#warm-tint", { opacity: 1 }, [T_H6_START]);
```

---

## FASE 6 — ENSAMBLADO FINAL

### 6.1 Actualizar data-duration de la composición

```html
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
  data-duration="[T_H6_END]">
```

### 6.2 Contador de data-track-index

Llevar conteo incremental. Video #1 usó hasta track-index 35. Empezar el próximo desde 1 y asignar secuencialmente.

### 6.3 Render BASE (sin V8 motion ni SFX dedicado)

Este render es la **versión V7** del video — solo Ken Burns, captions, narración, música, ticks. Sirve como punto de partida para las Fases 6.5 (SFX) y 6.6 (Motion).

```bash
cd "/ruta/al/proyecto"
hyperframes render . --output renders/video-v7-base-draft.mp4 --fps 30 --quality draft
```

Si falla con `Target closed`: reintentar. Es crash de Chrome, no error de código.

---

## FASE 6.3 — CAPTIONS WHISPER AUTO (10 min) ⭐ HARD GATE

> **JAMÁS hand-time captions.** Los timings manuales se desincronizan visiblemente. Cada frase del narrador debe tener su caption sincronizado a nivel de palabra. Aprendizaje de mina-abandonada v1 (2026-05-10): 23 captions a mano cuando había ~45 frases — el espectador silente pierde el 50% de la historia.

### 6.3.1 Crear `captions-spec.json`

Lista todos los audios narración con su `offset` (data-start real en el video) y `element` (CSS id del `<div>` de caption):

```json
[
  {"audio": "assets/h1-narr-2x.mp3",  "offset": 1.0,   "element": "cap-h1-1"},
  {"audio": "assets/h3-narr1-2x.mp3", "offset": 19.2,  "element": "cap-h3-n1"},
  {"audio": "assets/h3-narr2-2x.mp3", "offset": 26.78, "element": "cap-h3-n2"},
  {"audio": "assets/h3-narr3-2x.mp3", "offset": 32.59, "element": "cap-h3-n3"},
  {"audio": "assets/h3-narr4-2x.mp3", "offset": 38.5,  "element": "cap-h3-n4"},
  {"audio": "assets/h4-narr1-2x.mp3", "offset": 48.5,  "element": "cap-h4-n1"},
  {"audio": "assets/h4-narr2-2x.mp3", "offset": 57.16, "element": "cap-h4-n2"},
  {"audio": "assets/h4-narr3-2x.mp3", "offset": 60.87, "element": "cap-h4-n3"},
  {"audio": "assets/h4-narr4-2x.mp3", "offset": 65.0,  "element": "cap-h4-n4"},
  {"audio": "assets/h5-narr1-2x.mp3", "offset": 75.5,  "element": "cap-h5-n1"},
  {"audio": "assets/h5-narr2-2x.mp3", "offset": 81.28, "element": "cap-h5-n2"},
  {"audio": "assets/h6-narr1-2x.mp3", "offset": 85.3,  "element": "cap-h6-n1"}
]
```

**Keys exactos del script:** `audio` (string path), `offset` (float, segundos), `element` (string, CSS id del div sin `#`).

**Patrón de output:** un solo `<div>` por narración cuyo `innerHTML` cambia con cada palabra/frase. Es decir, el div `#cap-h3-n2` se reutiliza para todas las captions de h3-narr2 — el script genera `tl.set(..., { opacity: 1, innerHTML: "..." }, t)` para cada segmento. Por eso solo necesitás 12 `<div>` (uno por audio), no 45.

### 6.3.2 Ejecutar Whisper

```bash
.venv/bin/python scripts/captions.py --spec captions-spec.json
```

Output: bloques `<div>` HTML + GSAP `tl.set()` calls listos para pegar en `index.html`.

### 6.3.3 Wire en `index.html`

Reemplazar los captions hand-timed por los bloques que generó Whisper. Confirmar que **cada frase del narrador tiene su caption** (mucho más captions que en la versión sin Whisper — esperar 3-5x más).

### Gate antes de Fase 6.4

- [ ] Cada audio narración tiene captions auto-generadas
- [ ] No quedan captions hand-timed en `index.html`
- [ ] Re-render rápido + revisión visual: cada palabra del narrador debe aparecer en pantalla cuando se dice

---

## FASE 6.4 — MÚSICA (15-30 min) ⭐ HARD GATE

> El video sin música real (solo ambient SFX) se siente "narrador con efectos", no cine. La música hace heavy-lift atmosférico. **No saltarse esta fase.**

### 6.4.1 Diseñar segmentos de música

Mínimo 2 segmentos, idealmente 3:

| Segmento | Cobertura | Mood | Volumen sugerido |
|---|---|---|---|
| Horror | H1–H5 (0 → ~70s) | drone ambient oscuro, sub-bass, sin BPM definido | 0.05–0.18 |
| Cliffhanger | H6 (70s → fin) | warm pad mayor, acústico, esperanzado | 0.13–0.18 |
| Transición (opcional) | breve, en el puente al cliffhanger | shimmer ascendente | 0.10 |

### 6.4.2 Fuentes recomendadas

**Opción A — ElevenLabs Sound Effects con prompts musicales** (rápido, integrado al pipeline):
```bash
# Música horror — drone largo
.venv/bin/python scripts/sfx.py \
  -t "dark ambient horror drone music, low sub-bass evolving slowly, no melody no rhythm, cinematic tension, perfectly looping" \
  -d 22 --loop -i 0.5 \
  -o assets/music-horror-loop.mp3

# Expandir a 70s con stream_loop
ffmpeg -y -stream_loop 2 -i assets/music-horror-loop.mp3 -t 70 \
  -af "afade=t=in:st=0:d=2,afade=t=out:st=68:d=2" \
  assets/music-horror.mp3

# Música cliffhanger — pad cálido
.venv/bin/python scripts/sfx.py \
  -t "warm cinematic resolution music, soft acoustic pad with subtle major chord progression, hopeful peaceful, no drums, perfectly looping" \
  -d 15 --loop -i 0.5 \
  -o assets/music-dawn-loop.mp3

ffmpeg -y -i assets/music-dawn-loop.mp3 \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=13:d=1.5" \
  assets/music-dawn.mp3
```

**Opción B — Pixabay royalty-free** (más natural, más manual):
- Horror: buscar "dark ambient drone horror", "cinematic tension underscore"
- Cliffhanger: buscar "warm acoustic guitar pad", "serene peace music"
- Procesar en 2 pasos con ffmpeg (NUNCA `-ss` antes de `-i` con `-af` — produce silencio)

### 6.4.3 Wire en `index.html`

```html
<audio id="music-horror" class="clip" src="assets/music-horror.mp3"
       data-start="0" data-duration="70" data-track-index="50" data-volume="0.12"></audio>
<audio id="music-dawn" class="clip" src="assets/music-dawn.mp3"
       data-start="70" data-duration="15" data-track-index="51" data-volume="0.16"></audio>
```

Reservar `data-track-index` 50–59 para música (separado de SFX 60–110).

### Gate antes de Fase 6.5

- [ ] Música horror cubre toda la sección H1–H5
- [ ] Música cliffhanger entra en H6 con fade-in suave (~1.5s)
- [ ] Mix volumes correctos (música no compite con narración)
- [ ] Render rápido para verificar que NO satura

---

## FASE 6.5 — GENERACIÓN DE SFX V8-2 (15 min) ⭐ NUEVA

> Una vez que tenés timestamps reales del index.html (no estimados), generás todos los SFX dedicados. Esta fase ejecuta el plan que escribiste en Fase 0.5.

### 6.5.1 Convertir SFX-LIST.md → sfx-spec.json

Tomar la lista de Fase 0.5 y volcar a JSON. Template en `templates/sfx-spec-TEMPLATE.json`.

Cada entrada:
```json
{
  "out": "assets/sfx/<scene>-<descriptor>.mp3",
  "text": "<prompt para ElevenLabs Sound Effects API>",
  "duration": <segundos 0.5-22>,
  "influence": <0-1, default 0.3>,
  "loop": <true/false, default false>
}
```

### 6.5.2 Generar todos los SFX en batch

```bash
.venv/bin/python scripts/sfx.py --spec sfx-spec.json
```

Tiempo: ~3-8s por SFX. Total ~3-5 min para 25-30 SFX.

### 6.5.3 Verificar duraciones

```bash
for f in assets/sfx/*.mp3; do
  echo "$(basename $f): $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s"
done
```

ElevenLabs entrega duraciones con ±1-2% de error. Aceptable.

### 6.5.4 Expandir ambient loops largos

Para los SFX continuos que generaste con `loop:true` a 22s (ambient-forest-wind, ambient-dawn-warmth si necesita >12s, ambient-industrial-drone), expandir a la duración objetivo del hito con ffmpeg:

```bash
# Patrón estándar — ver PRODUCTION-PIPELINE.md § 12.5
ffmpeg -y -stream_loop 3 -i assets/sfx/ambient-forest-wind-loop.mp3 -t 75 \
  -af "afade=t=out:st=74:d=1" \
  assets/sfx/ambient-forest-wind.mp3
```

Calcular `-stream_loop` según `ceil(target / 22) - 1`. Verificar con ffprobe:
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 assets/sfx/ambient-forest-wind.mp3
```

**Si algún SFX EL salió notoriamente uncanny y no se arregla iterando el prompt:** fallback opcional a Freesound (§ 13 de PIPELINE). NO es parte del workflow estándar — solo excepción puntual.

### 6.5.5 Wire SFX en index.html

Cada SFX entra como `<audio class="clip">` con `data-track-index` 60-110 (rango reservado).

Ejemplo:
```html
<!-- Capa ambient continua -->
<audio id="ambient-wind" class="clip" src="assets/sfx/ambient-forest-wind.mp3"
       data-start="0" data-duration="72" data-track-index="60" data-volume="0.12"></audio>

<!-- SFX H3 ejemplo -->
<audio id="h3-whisper" class="clip" src="assets/sfx/h3-whisper.mp3"
       data-start="25.7" data-duration="2.0" data-track-index="71" data-volume="0.30"></audio>
<audio id="h3-flash-impact" class="clip" src="assets/sfx/h3-flash-impact.mp3"
       data-start="35.7" data-duration="0.7" data-track-index="72" data-volume="0.60"></audio>
```

Mix volumes canónicos: ver PRODUCTION-PIPELINE § 12.

### 6.5.6 Render con SFX

```bash
hyperframes render . --output renders/video-v8-sfx-draft.mp4 --fps 30 --quality draft
```

Verificar que ningún SFX tapa la narración escuchando con auriculares. Si algo sobresale, ajustar `data-volume`.

---

## FASE 6.6 — MOTION PASS V8-3 (45-90 min) ⭐ NUEVA

> Una vez que el video con SFX se ve y suena correcto, aplicar la capa de motion completa. Esto es lo que lleva el score de 8/10 a 9.5+/10.

### 6.6.1 Refactor del HTML para parallax (si aplica)

Para escenas con profundidad (POV caminando, pasillos), reemplazar `<img class="scene-image">` por capas:

```html
<div id="h3-wide-wrap" class="parallax-wrap clip"
     data-start="22.5" data-duration="9.5" data-track-index="20">
  <img id="h3-wide-back"  class="px-layer" src="assets/h3-wide-a.png" data-depth="0.3" />
  <img id="h3-wide-mid"   class="px-layer" src="assets/h3-wide-b.png" data-depth="0.6" />
  <img id="h3-wide-front" class="px-layer" src="assets/h3-wide-c.png" data-depth="1.0" />
</div>
```

Las 3 capas pueden usar la misma variante o las 3 distintas — depende del efecto deseado. CSS y patrón GSAP completo en `PRODUCTION-PIPELINE.md` § 3.5.

### 6.6.2 Agregar capas de overlay

CSS adicional para vignette pulse, niebla, fuego, etc.:

```css
.vignette-pulse {
  position: absolute; inset: 0; pointer-events: none; z-index: 45;
  background: radial-gradient(ellipse 900px 1700px at 50% 50%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.85) 100%);
}
.fog-layer {
  position: absolute; inset: 0; pointer-events: none; z-index: 32;
  background-image: url('assets/fog-loop.png');
  background-size: cover; opacity: 0.45; mix-blend-mode: screen;
}
```

HTML correspondiente en cada hito:
```html
<div id="h3-vignette" class="vignette-pulse" style="opacity:0;"></div>
<div id="h3-fog"      class="fog-layer"       style="opacity:0;"></div>
```

### 6.6.3 Aplicar motion según plan de Fase 0.5

Por cada plano del NARRATIVE.md table, agregar los `tl.to(...)` GSAP correspondientes. Patrones completos en `PRODUCTION-PIPELINE.md` § 3.5:

- Ken Burns (`scale 1.0 → 1.04`)
- Parallax (3 capas con `x` o `y` distintos)
- Flicker exposición (`filter: brightness`)
- Handheld shake (`translate ±2px @ 6Hz`)
- Vignette pulsante (radial-gradient opacity)
- Glitch frame (1-2 frames de displacement)
- Glow pulsante (filter brightness + box-shadow)
- Niebla deriva (translate continuo de fog-layer)

Snippet ejemplo (escena h3 con parallax + niebla):
```js
const T = 22.5; const DUR = 9.5;

// Parallax 3 capas
tl.fromTo("#h3-wide-back",  { x: 0 }, { x: -12, duration: DUR, ease: "none" }, T);
tl.fromTo("#h3-wide-mid",   { x: 0 }, { x: -24, duration: DUR, ease: "none" }, T);
tl.fromTo("#h3-wide-front", { x: 0 }, { x: -40, duration: DUR, ease: "none" }, T);

// Niebla overlay
tl.set("#h3-fog", { opacity: 0.45 }, T);
tl.fromTo("#h3-fog", { x: 0, y: 0 }, { x: -120, y: -40, duration: DUR, ease: "none" }, T);
tl.set("#h3-fog", { opacity: 0 }, T + DUR);
```

### 6.6.4 Render con motion

```bash
hyperframes render . --output renders/video-v8-motion-draft.mp4 --fps 30 --quality draft
```

Mirá el video en mute primero para enfocarte en el motion. ¿Hay algún plano que sigue sintiéndose estático? Ajustá.

### 6.6.5 Anti-patrones de performance

NO hacer:
- `filter: blur()` animado (mata GPU)
- Más de 6 elementos animando simultáneamente en la misma capa
- Animar `width`/`height` (siempre `transform: scale/translate`)
- Setear `will-change` en >10 elementos al mismo tiempo

Si el render se cuelga o sale lento, reducir capas.

---

## FASE 7 — GEMINI QA + RENDER FINAL (10 min)

### 7.1 Gemini Video Analyzer (gate de aprobación)

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/video-v8-motion-draft.mp4 \
  --prompt "Analiza en detalle:
  (1) ¿Se entiende cuándo es outcome A vs B en cada elección?
  (2) ¿La transición a [BUENO_APARENTE] es clara?
  (3) ¿El texto es legible en todos los fondos?
  (4) ¿El tamaño del texto A/B es suficiente para móvil?
  (5) ¿Hay CTA al final?
  (6) ¿Hay variedad visual o se reusa la misma imagen?
  (7) ¿El video se siente vivo (motion en cada plano) o slideshow?
  (8) ¿El diseño sonoro va más allá de narración + música? (footsteps, breaths, impactos, ambient)
  (9) ¿Hay momentos donde la imagen permanece estática >2s sin ningún motion?
  Dame un score 1-10 considerando estas 9 dimensiones."
```

### 7.2 Acción por score

| Score | Acción |
|---|---|
| ≥ 9.0 | **APROBADO** → Fase 7.3 |
| 7.0–8.9 | Iterar: revisar qué dimensión bajó el score. Si fue (7)/(9) volver a Fase 6.6. Si fue (8) volver a Fase 6.5. Si fue (6) volver a Fase 1/3 y agregar variantes. |
| < 7.0 | Algo estructural está roto. Revisar PAUTA § 5 errores y `V6-VS-V7.md`. |

### 7.3 Render final high-quality

```bash
hyperframes render . --output renders/video-final.mp4 --fps 30 --quality high
```

Tiempo: ~30-45 min para video de 80-90s. Verificar specs después:

```bash
ffprobe -v quiet -print_format json -show_streams renders/video-final.mp4 | \
  python3 -c "import json,sys; [print(s['codec_name'], s.get('r_frame_rate',''), s.get('sample_rate','')) for s in json.load(sys.stdin)['streams']]"
```

Debe imprimir: `h264 30/1` y `aac 48000`.

### 7.4 Update de docs

- Actualizar `V6-VS-V7.md` con la versión nueva y el score
- Documentar cualquier hallazgo nuevo (regla V9?) en PAUTA + PATTERNS + PIPELINE
- Si se usaron Freesound CC-BY, actualizar `CREDITS.md`

---

## CHECKLIST DE APROBACIÓN POR HITO

Antes de marcar un hito como aprobado:

**V7 (formato base):**
- [ ] Audio sincronizado con captions (leer captions mientras escuchás el audio)
- [ ] Captions no se cortan en pantalla (texto con wrap si es largo)
- [ ] Imágenes correctas en cada momento (no se superponen, no aparecen antes de tiempo)
- [ ] Countdown visible y audible (ticks suenan, digits aparecen)
- [ ] Loading bar llena en ~3s exactos
- [ ] White flash en cada twist (no fade, hard cut)
- [ ] Dilema: opción mala es genuinamente tentadora ✓
- [ ] Texto narrado = texto en pantalla (nunca difieren)
- [ ] Text stroke en todos los captions (V7-1)
- [ ] Choice labels A/B en 64px con stroke (V7-2)
- [ ] Separador de rama A→B (V7-3)

**V8 (calidad cinematográfica):**
- [ ] Cada escena >4s tiene ≥2 variantes de imagen (V8-1)
- [ ] SFX por escena conectado (footsteps, breaths, impacts) — track-index 60-110 (V8-2)
- [ ] Ambient continuo (wind/dawn) bajo la sección correspondiente (V8-2)
- [ ] Ken Burns en todo plano estático (V8-3 piso)
- [ ] Motion adicional según plan en NARRATIVE.md (parallax/flicker/vignette/glitch/glow donde aplique)
- [ ] Ningún plano estático >2s sin algún motion

---

## TRACK INDEX REFERENCE — Video #1

Para el próximo video, los primeros índices libres son 36+.

| Rango | Qué es |
|-------|--------|
| 1–4 | H1: narración + scene |
| 5–7 | H2: ticks |
| 8–13 | H2: loading, countdown |
| 14–19 | H3: imágenes |
| 16–19 | H3: narrations |
| 20–24 | H3: ticks, loading, extras |
| 25–27 | H4: imágenes principales |
| 28–31 | H4: narrations |
| 32–34 | H4: ticks |
| 35 | H4: exit image |
| 36+ | H5, H6 — libres |
