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

> ⛔ **Herencia (Capa A.5).** La MECÁNICA UI agnóstica de la familia choice — posiciones/safe-zones, timing del countdown (1.0s/dígito), pause beat (~0.9s), loading bar Y52, countdown Y46, film-leader-academy, no-overlap matrix, SFX tick — vive en **`../../choice-format-core/INGENIERO-CHOICE-CORE.md §1-2`** (técnica) + **`CHOICE-MECHANIC.md`** (intent). Este doc NO la re-define: solo agrega el **sabor horror** (estructura de hitos, variaciones de label dramáticas, color rojo=peligro/cyan=seguro, decisiones creativas de género).

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

### Visual intent + position + SFX (técnica agnóstica → home canónico)

> ⛔ **Countdown técnico → `../../choice-format-core/INGENIERO-CHOICE-CORE.md §1` (pacing) + §2.2 (safe zone Y46).** Ahí viven: estilo `film_leader_academy` (crosshair + dígito central ~40-50% frame, serif/condensed bold), `countdown_digit_duration_s = 1.0`, `pause_beat ~0.9s`, posición Y46 (X50% center), tick audible por dígito **sobre el bed** (no ducked). No dupliques esos valores acá.

**Sabor horror (decisión de género, NO en el home):**
- **Background tint:** sutil oscurecimiento del frame mientras el countdown está activo (refuerza la tensión horror).

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

### Visual intent + SFX (técnica agnóstica → home canónico)

> ⛔ **Loading bar técnica → `../../choice-format-core/INGENIERO-CHOICE-CORE.md §1.2-1.4` + §2.2 (safe zone Y52).** Ahí viven: posición **Y52** (≥6% sep del countdown Y46), fill L→R, duración **2.0-2.5s** (variante dramática ~4.2s con % counter), termina con flash/cut al consequence shot, beep tick acumulativo. No dupliques esos valores acá.

### Variaciones de label (sabor horror — decisión creativa)
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

### Layout + position (técnica agnóstica → home canónico)

> ⛔ **Choice buttons técnica → `../../choice-format-core/INGENIERO-CHOICE-CORE.md §2.2` (safe zones) + §2.3 (no-overlap)** + **`CHOICE-MECHANIC.md §3`** (orden hablado = orden de botones). Ahí viven: layout paired, banda/posición + safe zones IG, font monospaced, timing (~2.0-2.5s simultáneo con loading bar). No dupliques esos valores acá.

**Color intent (sabor horror — decisión de género):**
- Una opción con tinte **rojo/peligro** (la peligrosa), otra con **cyan/neutral** (la segura) — o ambas neutrales blancas. Horror puede mapear color a peligro de forma CONSISTENTE entre videos (a diferencia de sport, que rota el color para no spoilear).

### Variantes de layout (decisión creativa)

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

### Visual intent (técnica agnóstica → home canónico)

> ⛔ **Watermark técnica → `../../choice-format-core/INGENIERO-CHOICE-CORE.md §2.2`** (posición Y79% / banda 75-85% / X30% bottom-left / sans-serif / always-on / opacidad sutil 60-80% con drop-shadow). No dupliques esos valores acá.
>
> **Handle canónico del creator = `@elige_tucompanero`** (memoria `feedback_watermark_handle` — NUNCA `@referent-a`, que es referencia canónica, no nuestro handle). Constante entre videos.

### Anti-patterns watermark

❌ **Watermark grande/dominante** — distrae del contenido
❌ **Watermark con border o fondo** — look amateur
❌ **Watermark cambia de posición** — confunde
❌ **Watermark con animación** — innecesario
❌ **Sin watermark** — pierde brand identity + atribución

### Para tu identidad de creator

Handle canónico ya fijado: **`@elige_tucompanero`** (ver pointer arriba + memoria `feedback_watermark_handle`). Posición y opacidad CONSISTENTES entre videos (parte del brand visual).

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

> ⛔ **Regla agnóstica → `../../choice-format-core/INGENIERO-CHOICE-CORE.md §2.1` (un UI element por banda Y a la vez) + §2.3 (no-overlap matrix completa: qué banda es dueña cuándo + qué queda prohibido).** Resumen: countdown activo → caption baja/OFF; loading bar activa → countdown ya se fue; UN elemento UI dominante por vez. No dupliques la matriz acá.

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
