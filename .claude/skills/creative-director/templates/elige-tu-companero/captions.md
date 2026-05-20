# captions.md — Caption style + posicionamiento + animación + keyword highlights

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define INTENT de captions. El ingeniero implementa font choice, CSS, GSAP. Esta es DIRECCIÓN de cómo se ve y comporta el texto.

---

## El sistema de 3 tipos de captions

Cada tipo tiene rol narrativo distinto. El arquitecto decide cuándo se usa cuál.

### Tipo 1 — **Name labels** (etiquetas de personajes)
- **Cuándo:** introducción de archetypes en H2 setup (3-15s)
- **Contenido:** EL NOMBRE en mayúsculas ("BRUNO", "PABLO", "AXEL", "ENZO")
- **Persistence:** 1-2s, después fade
- **Position intent:** sobre la cabeza del personaje (no over face)
- **Style intent:** retro/expediente/typewriter — comunica "este es un archivo, no es ficción"
- **Color intent:** blanco puro

### Tipo 2 — **Narration captions** (subtítulos del voiceover)
- **Cuándo:** durante TODO el voiceover (sync palabra por palabra)
- **Contenido:** transcripción exacta del voiceover
- **Persistence:** cambia con cada frase
- **Position intent:** Y 65% (tercio inferior, fuera de safe zones IG)
- **Style intent:** sans-serif bold display, legible a glance
- **Color intent:** blanco con drop shadow para legibilidad

### Tipo 3 — **Warning text** (texto de alerta on-screen)
- **Cuándo:** Hook H1 + climax moments + setup retroactivo de twist
- **Contenido:** frase corta 3-5 palabras MAYÚSCULAS ("NO CONFÍES EN ÉL", "ÚLTIMA OPORTUNIDAD", "ESTO NO ES UN JUEGO")
- **Persistence:** 1.5-2s con animación entrada/salida
- **Position intent:** Y 50% (centro) o adjacent al sujeto referido
- **Style intent:** sans bold con presencia dramática
- **Color intent:** rojo (peligro) o amarillo (advertencia) — destaca del resto

---

## Inline keyword highlighting (gap D9 — el #3 más crítico)

**Validado en 12/13 referentes virales.** Dentro de la narration caption blanca, algunas palabras cambian a otro color INLINE.

### Las palabras que se destacan

| Categoría | Ejemplos | Color sugerido |
|-----------|----------|----------------|
| Nombres de personajes | BRUNO, PABLO, AXEL, ENZO, KRAVEN, MATEO | Amarillo o naranja |
| Settings críticos | MINA, TÚNEL 4, PISO 14, COCKPIT, VAGÓN | Cyan o amarillo |
| Objetos de decisión | LINTERNA, DINAMITA, ALARMA, MEDIDOR DE GAS | Rojo |
| Verbos críticos | MUERES, CAES, ESCAPAS, RESPIRAS | Rojo |
| Advertencias inline | NO CONFÍES, ÚLTIMA, NUNCA | Rojo |
| Decisiones binarias | OPCIÓN A / OPCIÓN B / SUBIR / QUEDARTE | Cyan / Amarillo |
| Stakes | MUERTE, SUPERVIVENCIA, TRAMPA | Rojo |
| Tiempo crítico | 3 SEGUNDOS, AHORA, ÚLTIMA OPORTUNIDAD | Rojo |

### Reglas de highlighting

#### Regla 1 — No abusar
- **5-10 keywords destacados** en todo el video (no más)
- Cada keyword destacado = momento crítico
- Si todo está destacado, nada está destacado

#### Regla 2 — Color por categoría
- **Rojo:** peligro, muerte, advertencia, urgencia
- **Amarillo:** atención, nombres de personajes, opciones
- **Naranja:** transición rojo↔amarillo, alerta moderada
- **Cyan:** opciones alternativas, settings, decisiones seguras
- **Verde** (raro): naturaleza, "vida", contraste con rojo

#### Regla 3 — Consistency
- Usar **máximo 2-3 colores distintos** de highlight en TODO el video
- Si BRUNO está amarillo, debe estar amarillo SIEMPRE que aparezca
- Si LINTERNA está rojo, dinamita también rojo (categoría peligro)

#### Regla 4 — Match al pattern
- Pattern 1 (clásico bueno=bueno) → highlights rojos en peligros, amarillos en seguros
- Pattern 3 (seguro era trampa) → en outro, retroactivamente palabras del "seguro" pasan a rojo
- Pattern 6 (hedonismo) → cambio de palette de highlights cuando entra mundo seguro

---

## Position direction

### Y-position por tipo

| Caption type | Y position intent | Reason |
|--------------|-------------------|--------|
| Name labels | Y 25-30% (top, sobre personaje) | Asocia visualmente |
| Narration | Y 65% (centro-inferior, fuera safe zones IG) | Legibilidad sin overlap UI |
| Warning text | Y 50% (centro absoluto) | Máxima atención |
| Choice options (A/B) | Y 50% + paired left/right | Decisión visual binaria |
| Loading bar / countdown | Y 40% (centro-alto) | Visible sin tapar caras |

### Safe zones IG (NO codificar exactos — eso es ingeniero)
- Arriba: evitar barra de estado IG
- Abajo: evitar caption del Reel + barra navegación
- Derecha: evitar botones like/comment/share

El arquitecto dice "respetá safe zones IG" — ingeniero calcula píxeles.

---

## Animation intent

### Animaciones validadas

#### **Scale pop** (signature)
- Caption aparece con leve scale-up (0.85 → 1.0) en ~0.15s
- Crea "punch" visual sin distraer
- Usado en TODAS las narration captions de los referentes top

#### **Fade in/out**
- Aparición y salida suave
- Usado en name labels (subtle, no distraen)
- Usado en warning text salida

#### **Typewriter effect** (raro)
- Letra por letra revealing
- Solo en momentos especiales (texto sobre máquina escribiendo, glitch reveal)
- NO usar en narration caption regular (sería slow)

#### **Marker sweep** (raro)
- Línea de color barre el texto
- Solo en warning text para highlight DRAMÁTICO

#### **Word-by-word sync** (default narration)
- Cada palabra aparece exactamente cuando se pronuncia
- Implementación: Whisper-sync (responsabilidad del ingeniero)
- Arquitecto solo dice: "narration captions sync palabra-por-palabra"

#### **InnerHTML swap** (cambio de texto sin animación)
- Caption se queda visible, solo cambia el texto
- Usado cuando hay narración continua y no hay break entre frases
- Decisión técnica del ingeniero — arquitecto solo dice "el texto cambia continuo, no hay gaps"

### Anti-patterns en animation

❌ **Typewriter effect en narration regular** — lento, irrita
❌ **Marker sweep en cada caption** — gimmick, pierde fuerza
❌ **Scale pop demasiado pronunciado** (scale 0.5 → 1.5) — distrae del visual
❌ **Sin animación de aparición** — captions "aparecen muerto" sin punch
❌ **Animation diferente por caption** — inconsistencia
❌ **Caption fade-out lento (>0.5s)** — overlap con siguiente caption

---

## Caption density

### Cuántas captions debe haber

- **Hook H1 (0-3s):** 1-2 captions cortos + warning text opcional
- **Setup H2 (3-15s):** name labels + 2-3 narration captions
- **Decision points (H3-H5):** option A vs option B + countdown + narration de "ahora decide"
- **Consequence sections:** narration captions casi continuas (1 cada 2-3s)
- **Outro H6:** narration cozy + counterfactual

### Caption coverage de la narración

- **>90% del voiceover debe tener caption visible** (validado en referentes top)
- Gap >2s sin caption = viewer SOUND-OFF pierde la historia
- Excepción: silencios narrativos a propósito (clímax visual sin palabras)

---

## Multi-narrator captions (cuando aplica)

Si el video tiene múltiples voces (narrador + dialogue de personajes — ver `narrator-voice.md`):

### Diferenciación visual entre speakers
- **Narrator:** caption blanco estándar
- **Personaje A dialogue:** caption con prefix "BRUNO:" o color shift sutil
- **Personaje B dialogue:** caption con prefix "PABLO:" o italics

Validado en ref-12 (Nano Banano + Teresa + narrator distintos).

---

## Lenguaje y registro de las captions

El texto en captions DEBE matchear el registro del voiceover (ver `narrator-voice.md`).

### Reglas
- Segunda persona ("vos", "tú")
- Presente histórico ("Bruno saca el medidor")
- Oraciones simples concatenadas
- Sin punctuación complicada (puntos, comas, exclamaciones — usar moderado)
- Sin negritas/cursivas dentro del texto (la negrita VIENE del style universal)
- Sin emojis (no es ese tono)

### Ejemplos validados (de ref-03 Bruno/Pablo)

```
"Si elegís a Bruno"
"estás en una mina a 200 metros bajo tierra"
"turno nocturno, sin señal"
"Bruno apaga los cascos de luz"
"y susurra"
"Los ojos se adaptan solos"
```

Notá:
- Frases cortas (4-8 palabras)
- Sin punctuación al final de cada caption
- Whisper-sync hace que cada frase aparezca cuando se dice
- El TEXTO ESCRITO es prácticamente igual al voiceover (no se "edita" para captions)

---

## Caption del Reel (Instagram description)

(Esto NO es caption on-screen — es el texto EN INSTAGRAM debajo del video. Es parte del brand-and-cliffhanger.md pero relevante mencionar acá.)

Algunos referentes ponen:
- "Qué compañero elegirás?" (ref-10)
- "¿Elegirías a Bruno o Pablo?"

Es CTA para comentarios. (Detalle en `brand-and-cliffhanger.md`.)

---

## Output al SPEC

```yaml
captions:
  general_style_intent:
    typography: sans-serif bold display (engineer choose Anton/Bebas/Montserrat)
    name_labels_style: monospaced retro typewriter feel (engineer choose VT323 / Space Mono / IBM Plex Mono)
    color_base: white
    effect: drop shadow blur (NOT thick stroke unless display extreme font)

  caption_types_usage:
    name_labels:
      timestamps: ["3-5s for Bruno", "5-7s for Pablo"]
      position_intent: top above each character (Y ~25%)
      animation_intent: scale pop entrada + fade out
      content_examples: ["BRUNO", "PABLO"]

    narration_captions:
      coverage: ">90% of voiceover"
      position_intent: Y 65% (center-bottom, respeta safe zones IG)
      animation_intent: scale pop word-by-word, sync con Whisper
      examples_at_timestamps:
        - { ts: "5s", text: "Si elegís a BRUNO", highlights: { "BRUNO": "yellow" } }
        - { ts: "7s", text: "estás en una MINA a 200 metros bajo tierra", highlights: { "MINA": "cyan" } }
        - { ts: "22s", text: "Ahora debes de decidir", highlights: {} }
        - { ts: "23s", text: "enciendes tu LINTERNA o esperas", highlights: { "LINTERNA": "red" } }

    warning_text_overlays:
      - { ts: "0.5-2s", text: "NO CONFÍES EN ÉL", color_intent: "red glow", position_intent: "Y 50% center", animation: "scale pop + glow pulse" }
      - { ts: "1:15-1:17", text: "ÚLTIMA OPORTUNIDAD", color_intent: "red", position_intent: "Y 50%" }

  keyword_highlight_strategy:
    color_assignments:
      yellow: "nombres de personajes (BRUNO, PABLO)"
      cyan: "settings/decisiones seguras (MINA, ESPERAS, TÚNEL 4)"
      red: "peligros + verbos críticos + warnings (LINTERNA, DINAMITA, MUERES, NO CONFÍES, ALARMA)"
    estimated_total_highlights: 8

  language_register:
    person: "segunda persona vos / tú"
    tense: "presente histórico"
    sentence_length: "4-8 palabras por frase típico"
    punctuation: "minimal — Whisper sync sin punctuation final"

  multi_speaker: false  # no character dialogue, solo narrator único
```

---

## Anti-patterns en captions (consolidados)

❌ **Captions con thick stroke 12px en font sans regular** — look amateur capcut 2010
❌ **Sin keyword highlights** — gap D9 automático (-1.5 puntos)
❌ **Todos los caption en mismo color sin variación** — visual monotonía
❌ **Highlights en >4 colores distintos** — confunde
❌ **Captions en safe zones de IG** — viewer no las ve (tapadas por UI)
❌ **Caption persistente > 3s sin cambio** — viewer ya lo leyó, pasa a fondo visual
❌ **Captions sin sync con voz** — viewer percibe desorden
❌ **Captions con emojis** — rompe tone serio del horror
❌ **Captions con punctuation finales** (puntos, comas) — innecesario, Whisper sync funciona mejor sin
❌ **Captions en third person ("Bruno hace X")** — rompe segunda persona del voiceover

---

## Validación final de captions

- [ ] ¿Name labels definidos para H2 setup?
- [ ] ¿Narration captions cubren >90% del voiceover?
- [ ] ¿Warning text definidos para hook + clímax?
- [ ] ¿Keyword highlights identificados (5-10 keywords) con colores asignados?
- [ ] ¿Position intent claro (Y % por tipo)?
- [ ] ¿Animation intent definido (scale pop, fade, sync word-by-word)?
- [ ] ¿Lenguaje en segunda persona + presente histórico?
- [ ] ¿Si hay dialogue character → multi-speaker definido?

Si ❌ en cualquiera → ajustar antes de SPEC.
