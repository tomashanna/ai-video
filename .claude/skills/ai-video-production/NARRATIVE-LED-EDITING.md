# NARRATIVE-LED-EDITING.md — El narrador dicta los cortes

> El espectador no entiende la historia por las imágenes. La entiende por el RITMO. Cada frase del narrador es una **habitación visual**, separada de las otras por **negros + audio punctuation**. Este patrón se aplica a CUALQUIER formato de video con IA — horror-choice, documental, educacional, todo.

---

## El principio

**El narrador es el director.** Cuando el narrador cambia de idea, cambia de rama, o llega a una pausa dramática, ahí va un corte. Esos cortes están punctuados por SONIDO específico, no por silencio raso. La pantalla muchas veces va a NEGRO breve (no white flash) para señalar "esto es otra realidad / otra rama / otro beat".

### Por qué importa

| Objetivo del video | Cómo lo logra este patrón |
|---|---|
| **Engagement** | Cada negro + audio crea tensión rítmica — el espectador no puede mirar para otro lado porque cada pausa dramática le grita "viene algo" |
| **Comprensión** | Cada negro = punto-y-aparte narrativo. El cerebro procesa cada rama por separado: "esto fue rama A, NEGRO, esto fue rama B, NEGRO, esto es la realidad" |
| **Retención hasta el final** | El último negro antes del cliffhanger (warm whoosh) promete una resolución distinta. Engancha hasta el final |

---

## Taxonomía de 7 cortes — cada uno con audio + duración propia

| Tipo de corte | Cuándo se usa | Audio (prompt EL típico) | Duración | Volumen |
|---|---|---|---|---|
| **1. WHITE FLASH** | Cuando se TOMA la elección (cliff/branch fork). "Ahora decide → ¡cortaste!" | "short cinematic white-flash impact, sharp crack with deep sub-bass tail, dry, single event" | ~0.15s blanco | 0.55–0.65 |
| **2. BLACK + LOW THUD** | Entrada a rama mala (game-over alternativo). "Y esto es lo que te pasó si elegiste mal" | "low heavy heart-skip thud, body weight collapse, dark sub-bass impact, single event, no music" | 0.3–0.5s negro | 0.50–0.60 |
| **3. BLACK + DRONE BAJO** | Sostener el momento muerto. "Estás muerto / atrapado / perdido" | "low continuous sub-bass drone, doom atmosphere, no melody, sustained event" | 0.4–0.8s negro | 0.35–0.45 |
| **4. BLACK + RISE DRONE** | Transición rama mala → rama buena ("y si no..."). "Pero si hubieras elegido distinto..." | "ascending sub-bass pad rising from low to mid, transition swell, tension to release" | 0.4–0.6s negro | 0.40–0.55 |
| **5. BLACK + EXHALE** | Entrada a rama buena (alivio). "Sobreviviste" | "soft human exhale of relief, ambient warm low pad tail, no music, single event" | 0.2–0.4s negro | 0.35–0.45 |
| **6. BLACK + PUNCT SILENCE** | Pausa entre nominales del narrador ("El suelo." "Oscuridad.") | (sin audio o casi: leve drone bajo) | 0.15–0.30s negro | 0.10–0.20 |
| **7. WARM WHITE** | Transición al cliffhanger (rama "buena hipotética" / cierre cálido) | "soft warm whoosh transition without horror, gentle wind change, single event" | 0.3–0.5s blanco cálido | 0.40–0.50 |

---

## Cómo aplicar — Workflow

### Paso 1: Marcar el script del narrador

Tomar el texto literal y marcar cada cambio de beat. Cada coma o punto es un candidate de corte.

**Ejemplo bosque-abandonado H3 (narr4):**

```
Texto del narrador:
"Si te giras: una mano fría en tu hombro. El suelo. Oscuridad. No hay amanecer para ti.
Si no te giras: bien. Aprendes rápido. El bosque te deja pasar."
```

Mapeado de cortes:

| Tiempo | Texto narrado | Corte tipo | Imagen |
|---|---|---|---|
| T+0 (just after countdown) | (silencio antes de la frase) | **1. WHITE FLASH** | – |
| T+0.15 | "Si te giras:" | (cap) | Mano monstruo POV |
| T+1.5 | "una mano fría en tu hombro." | (cap) | Mano monstruo POV continúa |
| T+2.8 | (punto) | **2. BLACK + LOW THUD** | Negro |
| T+3.2 | "El suelo." | (cap) | POV ground close-up |
| T+4.0 | (punto) | **6. BLACK + PUNCT SILENCE** | Negro |
| T+4.2 | "Oscuridad." | (cap, sostener negro) | Negro continuado |
| T+4.8 | (punto, peso) | **3. BLACK + DRONE BAJO** | Negro + drone |
| T+5.5 | "No hay amanecer para ti." | (cap) | (sigue negro o sutil) |
| T+7.0 | (silencio dramático) | **4. BLACK + RISE DRONE** | Negro + ascending |
| T+7.5 | "Si no te giras:" | (cap) | Imagen del forest pass-zone |
| T+8.5 | "bien." | (cap) | **5. BLACK + EXHALE** breve antes |
| T+9.0 | "Aprendes rápido." | (cap) | Continúa caminando |
| T+10.0 | "El bosque te deja pasar." | (cap, resolución) | Forest fade |

### Paso 2: Implementar en HTML/GSAP

#### Patrón GSAP para BLACK + AUDIO

CSS necesario (agregar al stylesheet):

```css
#black-overlay {
  position: absolute; inset: 0;
  background: #000000;
  z-index: 94;  /* above flash-white (93) */
  pointer-events: none;
  opacity: 0;
  will-change: opacity;
}
```

HTML:

```html
<div id="black-overlay"></div>
```

GSAP — entrada a rama mala (CORTE TIPO 2):

```js
// T = momento de transición (después del white flash de la elección)
const T = 38.8;  // ejemplo

// 1. Levanto el negro
tl.set("#black-overlay", { opacity: 1 }, T);

// 2. Anclo la imagen siguiente con opacity:0 (no se ve por debajo del negro todavía)
tl.set("#scene-bad-outcome", { opacity: 1 }, T);  // ya está visible PERO oculta por negro

// 3. Bajo el negro suavemente después del thud
tl.to("#black-overlay", { opacity: 0, duration: 0.35, ease: "power2.out" }, T + 0.15);

// 4. Hard-kill para seek correcto
tl.set("#black-overlay", { opacity: 0 }, T + 0.6);

// 5. Audio del cut
// <audio> con data-start=T data-duration=0.5 data-volume=0.55 src="assets/sfx/cut-bad-thud.mp3"
```

GSAP — transición rama mala → buena (CORTE TIPO 4):

```js
// T_mid = momento entre outcome A y outcome B
const T_mid = 43.0;

// 1. Negro entra
tl.to("#black-overlay", { opacity: 1, duration: 0.15, ease: "power2.in" }, T_mid);

// 2. Sostiene negro mientras suena el rise drone
tl.set("#black-overlay", { opacity: 1 }, T_mid + 0.15);

// 3. Imagen mala se va al 0 mientras negro está arriba
tl.set("#scene-bad-outcome", { opacity: 0 }, T_mid + 0.15);

// 4. Imagen buena se prepara
tl.set("#scene-good-outcome", { opacity: 1 }, T_mid + 0.45);

// 5. Negro baja revelando buena
tl.to("#black-overlay", { opacity: 0, duration: 0.25, ease: "power2.out" }, T_mid + 0.45);
tl.set("#black-overlay", { opacity: 0 }, T_mid + 0.75);

// 6. Audio rise drone
// <audio> data-start=T_mid data-duration=0.5 data-volume=0.45 src="assets/sfx/cut-rise-drone.mp3"
```

### Paso 3: Generar los 7 SFX con `ai-video sfx`

Los 7 sonidos van a `assets/sfx/cuts/` para mantenerlos separados de los SFX por escena:

```json
[
  {"out": "assets/sfx/cuts/cut-white-flash.mp3", "text": "short cinematic white-flash impact, sharp crack with deep sub-bass tail, dry, single event, no music", "duration": 0.5, "influence": 0.5},
  {"out": "assets/sfx/cuts/cut-bad-thud.mp3", "text": "low heavy heart-skip thud, body weight collapse, dark sub-bass impact, single event, no music", "duration": 0.7, "influence": 0.6},
  {"out": "assets/sfx/cuts/cut-drone-low.mp3", "text": "low continuous sub-bass drone, doom atmosphere, no melody, sustained 1 second event", "duration": 1.0, "influence": 0.7},
  {"out": "assets/sfx/cuts/cut-rise-drone.mp3", "text": "ascending sub-bass pad rising from low to mid, transition swell, tension to release, single event", "duration": 0.6, "influence": 0.6},
  {"out": "assets/sfx/cuts/cut-exhale.mp3", "text": "soft human exhale of relief, ambient warm low pad tail, no music, single event", "duration": 0.5, "influence": 0.5},
  {"out": "assets/sfx/cuts/cut-silence-drone.mp3", "text": "very low subtle drone for dramatic silence, almost imperceptible, atmospheric, 0.3 seconds", "duration": 0.3, "influence": 0.5},
  {"out": "assets/sfx/cuts/cut-warm-whoosh.mp3", "text": "soft warm whoosh transition without horror, gentle wind change, single event, no music", "duration": 0.5, "influence": 0.4}
]
```

Costo aproximado: ~$0.50 (~2k créditos EL) para los 7 sonidos. Se generan UNA VEZ y se reutilizan en todos los videos.

### Paso 4: Validación

Después de aplicar, escuchar SOLO la pista de audio del render con auriculares (closed-back). Cada corte debe tener su firma sonora distinta. Si dos cortes suenan "iguales", revisar.

Visualmente: extraer frames a cada timestamp del negro y confirmar que la pantalla está efectivamente negra (no apenas oscura).

---

## Anti-patterns

- ❌ **Misma transición (white flash) para TODO** — el espectador no distingue "elección" de "rama mala terminó". Ambos sonidos son flash crack.
- ❌ **Imágenes continuas sin negro entre frases nominales del narrador** — "El suelo. Oscuridad." se siente como una idea sola en vez de dos beats dramáticos.
- ❌ **Negro sin audio** — pierde 70% del impacto. El negro silente comunica "fin" mejor cuando va con un sonido específico.
- ❌ **Audio sin negro** — un thud sin el visual de respaldo no aterriza emocionalmente.
- ❌ **Duraciones uniformes** — todos los negros de la misma duración aplana el ritmo. Debe variar 0.15–0.8s según peso emocional.

---

## Validado en

- **bosque-abandonado v2-final** (Gemini 8.75/10) — usa este patrón orgánicamente. Los cortes son lo más fuerte del video.
- **mina-abandonada v6** (Gemini 8.5/10) — NO usa este patrón. Los cortes son flash blanco + corte directo, sin variedad de negros + audio. Por eso "se siente lineal" según el usuario.
- **elige-companero V7** (Gemini 9.5/10) — usa el patrón completo, incluyendo el cliffhanger warm white.

**Aprendizaje 2026-05-10**: el usuario reportó que los cortes de bosque son superiores a mina pese a que Gemini Video Analyzer dio mejor nota a mina en "motion". Gemini no distingue entre "más efectos visuales" y "edición narrativa correcta". Validar SIEMPRE con criterio humano en este aspecto.

---

## Aplicación a otros formatos (general, no solo horror-choice)

Esta taxonomía aplica a CUALQUIER formato con narrador + branches o beats dramáticos:

| Formato | Cómo se aplica |
|---|---|
| **Documental** | Cambio de fuente/testigo = BLACK + DRONE. Revelación = BLACK + LOW THUD. Conclusión esperanzadora = WARM WHITE. |
| **Educacional** | Cambio de concepto = BLACK + PUNCT SILENCE. Pregunta a la audiencia = BLACK + RISE DRONE. "Ahora lo sabes" = BLACK + EXHALE. |
| **Storytelling personal** | Cambio de tiempo (presente → recuerdo) = BLACK + DRONE LOW. Vuelta al presente = BLACK + EXHALE. |
| **Promocional / Ad** | Problema (pain) = BLACK + LOW THUD. Solución revela = WARM WHITE. CTA = WHITE FLASH. |

El principio se mantiene: **el cambio de beat narrativo se marca con corte + audio específico, no solo con cambio de imagen**.
