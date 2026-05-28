# ui-elements.md — Countdown + loading bars + choice buttons + watermark

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define INTENT visual de los elementos UI. El ingeniero implementa con HTML/CSS/GSAP. Estos son elementos signature del formato que el viewer asocia con "es elige a tu compañero".

---

## Los 4 elementos UI signature

| Elemento | Función | Validado en |
|----------|---------|-------------|
| Countdown circular 3-2-1 | Crear urgencia en decision points | 13/13 referentes |
| Loading bars con porcentaje | Comunicar "tu decisión carga" | 12/13 referentes |
| Choice buttons A/B | Visualizar opciones binarias | 13/13 referentes |
| Watermark del creator | Brand identity | 13/13 referentes |

**Estos NO son opcionales** — son parte del DNA del formato. Sin ellos, no se reconoce como "elige tu compañero".

---

## Countdown circular 3-2-1

### Función narrativa
- Generar urgencia: "tenés que decidir AHORA"
- Marcar el momento exacto de decisión
- Generar engagement: viewer ESTÁ decidiendo (mental engagement)

### Apariciones en el video
- **H1 Hook (0-3s):** countdown inicial, NO es decisión real — es "atención inmediata"
- **H3 Decision 1 (alrededor 17-20s):** countdown de decisión
- **H4 Decision 2 (alrededor 40-43s):** countdown de decisión
- **H5 Decision 3 (alrededor 65-68s):** countdown de decisión

### Visual intent

- **Forma:** círculo grande centrado
- **Números:** GRANDE, sans-serif bold, blanco
- **Animación intent:** 3 → 2 → 1 con scale pop en cada número
- **Color del círculo:** negro sólido con stroke sutil O transparente con stroke
- **Background tint:** sutil oscurecimiento del frame mientras está activo
- **Duración:** ~3 segundos total (1s por número)

### Position
- Centro absoluto del frame (X 50%, Y 50%)
- O ligeramente arriba (Y 40%) para no tapar captions narrativos abajo

### SFX intent
- Tick-tick audible por cada número (tic 3, tic 2, tic 1)
- Crescendo de tensión

---

## Loading bars con porcentaje

### Función narrativa
- Comunicar "tu decisión está siendo procesada"
- Crear espera dramática
- Generar moment of commitment

### Cuándo aparece
- Después de la decisión binaria (post H3, H4, H5)
- Aparece como overlay sobre la imagen
- Dura 2-4 segundos máximo

### Visual intent

- **Forma:** barra horizontal con texto "LOADING" y porcentaje 0% → 100%
- **Posición:** centro del frame (Y 50%) o adjacent a las choice buttons
- **Color:** monocromática (blanco/gris) o con accent del archetype elegido
- **Animación intent:** porcentaje sube de 0 a 100, barra se llena de izquierda a derecha
- **Duration:** 2-4s
- **Termina con:** flash/transición al consequence shot

### SFX intent
- Beep tick acumulativo a medida que sube el porcentaje
- Click sutil al llegar a 100%
- Pre-impact sound antes de la consecuencia

### Variaciones (decisión creativa)
- "LOADING..." (genérico)
- "PROCESSING DECISION..."
- "CALCULATING OUTCOME..."
- "100%" sin label (solo porcentaje)
- "DESTINY LOADING..." (más dramático)

---

## Choice buttons A/B

### Función narrativa
- Visualizar las 2 opciones de la decisión
- Asociar visualmente "A es izquierda, B es derecha"
- Mostrar lo que el viewer está "eligiendo"

### Cuándo aparece
- Durante el countdown (3-2-1) en decision points
- Side by side dentro del frame
- Persisten hasta que el countdown termina

### Visual intent

- **Layout:** dos paneles horizontales paired left/right
- **Cada button contiene:**
  - Letra grande (A o B)
  - Texto de la opción ("Enciendes la linterna" / "Esperas")
  - Optional: porcentaje de "votos" (creates community feel)
- **Color intent:**
  - Una opción con tinte rojo/peligro (la peligrosa)
  - Otra opción con tinte azul/cyan/neutral (la segura)
  - O ambas neutrales blancas
- **Border:** sutil stroke para legibilidad
- **Animación:** entrada con fade-in o slide-in sutil

### Position
- Mitad inferior del frame, side by side
- O centradas verticalmente con countdown arriba
- Respetan safe zones de IG (no derecha extrema donde están likes IG)

### Variantes (decisión creativa)

#### Variante 1 — Texto puro
```
[ A ]               [ B ]
ENCIENDES           ESPERAS
LA LINTERNA
```

#### Variante 2 — Con porcentaje community
```
[ A — 67% ]         [ B — 33% ]
ENCIENDES           ESPERAS
```

#### Variante 3 — Solo letras + voiceover dice opciones
```
        [ A ]    [ B ]
```
(El voiceover dice "A: enciendes la linterna. B: esperas.")

### SFX intent
- Pop sutil al aparecer
- Click subtle al final del countdown (decisión "consagrada")

---

## Watermark del creator

### Función
- Brand identity
- Atribución (que no roben el video sin crédito)
- Reconocimiento serie

### Visual intent

- **Texto:** handle del creator (e.g., "@referent-c", "referent-a", "referent-b")
- **Posición:** bottom-left o bottom-center, fuera de UI Instagram
- **Opacidad:** 60-80% (sutil, no compite)
- **Font:** sans-serif simple, weight regular
- **Color:** blanco con drop shadow sutil
- **Persistence:** TODO el video (no parpadea, no aparece/desaparece)

### Anti-patterns watermark

❌ **Watermark grande/dominante** — distrae del contenido
❌ **Watermark con border o fondo** — look amateur
❌ **Watermark cambia de posición** — confunde
❌ **Watermark con animación** — innecesario
❌ **Sin watermark** — pierde brand identity + atribución

### Para tu identidad de creator

- Decidí UN handle único (e.g., "@horror.choice.argentina", "@elige.tu.compañero", "@conspiracionobscura")
- Mantenelo CONSTANTE entre videos (serie continuity)
- Posición y opacidad CONSISTENTES (parte del brand visual)

---

## UI elements menos críticos (opcionales)

### Title cards
- Algunos referentes usan title cards (texto sobre fondo negro)
- @referent-b los usa para introducir personajes con personalidad
- "BRYAN — EL FIESTERO" + visual de capybara
- Decisión creativa, no necesario

### Progress timeline
- Algunos referentes muestran progress timeline (similar a YouTube progress)
- "Hito 1 / 3" indicator
- Decisión creativa

### Stat overlays
- Mostrar "stats" del personaje (humor, danger, trust)
- Muy raro en este formato
- Más típico de gamification extrema

### Glitch overlays
- Visual glitch effects en transiciones (ref-13 cambio de estado de Miro)
- Decisión creativa, no default

---

## Coordinación con captions

Los UI elements coexisten con narration captions. Coordinación crítica:

| Cuando hay... | Narration caption está... |
|---------------|----------------------------|
| Countdown 3-2-1 activo | OFF o MUY tenue (el countdown lleva atención) |
| Loading bar 0-100% | Narration en pause (voiceover dice "decides...") |
| Choice buttons A/B mostrados | Caption con narration ALTAS arriba/abajo |
| Solo narration | UI elements ausentes |

**Regla:** UN elemento UI dominante por vez. Si hay countdown, caption baja. Si hay loading bar, countdown se fue. No overlap visual.

---

## Output al SPEC

```yaml
ui_elements:
  countdown_strategy:
    appearances:
      - { timestamp: "0:00-0:03", purpose: "hook attention", duration: 3s, is_real_decision: false }
      - { timestamp: "0:17-0:20", purpose: "Decision 1 countdown", duration: 3s, is_real_decision: true }
      - { timestamp: "0:40-0:43", purpose: "Decision 2 countdown", duration: 3s, is_real_decision: true }
      - { timestamp: "1:05-1:08", purpose: "Decision 3 countdown", duration: 3s, is_real_decision: true }
    visual_intent: "círculo centrado grande, números sans-serif bold blancos, scale pop en cada número, background sutil oscurecimiento"
    sfx_intent: "tick audible por cada número"
    position_intent: "centro X 50% Y 40%"

  loading_bars:
    appearances:
      - { timestamp: "0:20-0:24", linked_to: "Decision 1 outcome" }
      - { timestamp: "0:43-0:47", linked_to: "Decision 2 outcome" }
      - { timestamp: "1:08-1:12", linked_to: "Decision 3 outcome" }
    visual_intent: "barra horizontal con texto 'LOADING' + porcentaje 0% → 100%, color monocromático blanco/gris"
    duration_each: 3s
    sfx_intent: "beep tick acumulativo subiendo"
    end_transition_intent: "flash + cut a consequence shot"

  choice_buttons:
    appearances_during_countdowns:
      - timestamp: "0:17-0:20"
        option_a: { letter: A, text: "ENCIENDES LA LINTERNA", color_intent: red_danger }
        option_b: { letter: B, text: "ESPERAS", color_intent: cyan_safe }
      - timestamp: "0:40-0:43"
        option_a: { letter: A, text: "LO SIGUES", color_intent: red_danger }
        option_b: { letter: B, text: "TE QUEDAS", color_intent: cyan_safe }
      - timestamp: "1:05-1:08"
        option_a: { letter: A, text: "ACTIVAS LA ALARMA", color_intent: red_danger }
        option_b: { letter: B, text: "ESPERAS REVISIÓN", color_intent: cyan_safe }
    layout_intent: "paired side-by-side, Y 60-70%, respetan safe zones IG"
    show_percentages: false  # decisión creativa: sin porcentaje community
    animation_intent: "fade-in sutil al inicio del countdown, fade-out al finalizar"

  watermark:
    text: "@elige.tu.compañero"  # tu handle (a definir)
    position_intent: "bottom-center, debajo del último caption"
    opacity_intent: "60-70%"
    font_intent: "sans-serif regular weight, blanco con drop shadow sutil"
    persistence: "todo el video sin animación"

  title_cards: []  # no usar en este video

  progress_timeline: false  # no usar

  glitch_overlays: []  # no usar
```

---

## Anti-patterns en UI elements

❌ **Countdown sin SFX tick** — pierde urgencia auditiva
❌ **Loading bar sin transition al final** — viewer queda colgado
❌ **Choice buttons sin texto explicativo** (solo A/B sin descripción) — viewer no entiende qué elige
❌ **Watermark grande/dominante** — distrae
❌ **UI elements amontonados** (countdown + loading + buttons + caption + glitch overlay simultáneo) — overload visual
❌ **Glitch effects en cada cut** — pierde fuerza
❌ **Progress timeline siempre visible** — distrae del contenido
❌ **Title card en cada nuevo personaje** — slow pacing
❌ **Countdown que NO está cerca del centro** — no comunica urgencia
❌ **Choice buttons sin asociación visual A=peligrosa / B=segura** — viewer adivina

---

## Validación final UI elements

- [ ] ¿Countdown definido para hook + cada decision point?
- [ ] ¿Loading bar después de cada decisión?
- [ ] ¿Choice buttons con texto + asociación visual (red/cyan)?
- [ ] ¿Watermark definido (handle + posición + opacidad)?
- [ ] ¿UI elements NO overlap visualmente?
- [ ] ¿Position de cada elemento respeta safe zones IG?
- [ ] ¿SFX intent acompañando cada UI element?

Si ❌ en cualquiera → ajustar antes de SPEC.
