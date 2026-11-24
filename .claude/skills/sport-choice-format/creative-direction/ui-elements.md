# ui-elements.md — Name labels de equipos + countdown + botones de jugadas + watermark (sport-choice)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> Los **specs técnicos de UI** (safe zones, posiciones Y, monospaced, decision-UI editorial pacing, no-overlap) se HEREDAN de `../../choice-format-core/INGENIERO-CHOICE-CORE.md § 2` (UI safe zones + no-overlap matrix) + `§ 1` (decision-UI editorial pacing) + docs/OPERATING-MANUAL.md HR#4. Este doc reskinea el CONTENIDO de la UI a deporte. Si hay conflicto → gana la técnica heredada.
>
> Si llegaste acá sin leer las pautas, parar y leerlas primero.

---

> El arquitecto define INTENT visual de los elementos UI; el ingeniero implementa con HTML/CSS/GSAP. En sport-choice, los elementos signature del formato choice (countdown, loading bar, botones A/B, name labels, watermark) se HEREDAN — lo que cambia es el CONTENIDO: equipos en vez de criaturas, jugadas en vez de dilemas de horror.

---

## Los elementos UI signature (heredados del formato choice)

| Elemento | Función | Specs (heredados) | Contenido sport-choice |
|----------|---------|-------------------|------------------------|
| **Name labels** | Identificar el dyad | Monospaced, Y11.5, GRANDES | Nombre del jugador (GIMÉNEZ / TAU) |
| **Caption de contexto** | Decir qué equipo es cada uno | drop-shadow, **Y55** (⛔ NO Y62 — exclusivo de los captions del narrador; jamás solapados) | "GIMÉNEZ = MÉXICO · TAU = SUDÁFRICA" |
| **Countdown del HOOK** | Urgencia en la elección de compañero | Film leader academy AVU, completo 3-2-1 | Igual (heredado) |
| ⭐ **Countdown de COMPUERTA** | Urgencia en decisiones de jugada | **OVERRIDE SPORT (creator 2026-06-04)**: dígitos 3→2→1 ARRIBA (Y≈28-32, monospaced grandes) + **barra que se AGOTA** (llena→vacía, clara/brillante, Y≈36-38). ⛔ SIN film-leader/crosshair al centro (desconcentra sobre la jugada congelada). SIEMPRE 3-2-1 completo | Ver `../INGENIERO-PAUTA-MASTER.md § 1.5` (autoridad) |
| **Botones A/B** | Las 2 opciones de jugada | Paired, Y75/Y82, safe zones IG. ⛔ **SIEMPRE con prefijo rotulado "A. " / "B. "** (creator 2026-06-04) | "A. DESCARGAS CON GIMÉNEZ" / "B. GIRAS SOBRE EL CENTRAL" |
| **Watermark** | Brand | bottom, 60-80% opacity, persistente | `@elige_tucompanero` |

> Specs exactos heredados (monospaced, no-overlap matrix, pacing) = `../../choice-format-core/INGENIERO-CHOICE-CORE.md § 1-§ 2`, CON los overrides sport de `../INGENIERO-PAUTA-MASTER.md § 1.5` (countdown de compuerta + rotulado A/B + zonas exclusivas hook), que MANDAN en este formato.

---

## Name labels de EQUIPOS (lo sport-específico)

> El name label es el primer punto de contexto de equipo. Es CRÍTICO para resolver la incoherencia rival/compañero.

- **Texto:** nombre del jugador (SAKA, DEMBÉLÉ), monospaced GRANDE, Y11.5 (heredado).
- **El caption de contexto** (Y62) hace el mapeo jugador→equipo EXPLÍCITO: "SAKA = ARSENAL · DEMBÉLÉ = PSG".
- **(Opcional) tinte por equipo:** el name label puede llevar un tinte del color del kit (rojo Arsenal / azul PSG) para reforzar visualmente la identidad de equipo. Decisión creativa.
- **(Opcional) escudo/badge:** si la likeness/branding lo permite, un mini-badge del equipo junto al nombre. Cuidado con derechos de marca — evaluar.

🟦 PRINCIPIO: al terminar el hook, el viewer DEBE saber, sin ambigüedad, qué jugador pertenece a qué equipo. Name label + caption de contexto lo garantizan.

---

## Countdown + loading bar (heredados)

- **Countdown:** film leader academy AVU (clip heredado `countdown-3-2-1-film-leader-with-ticks.mp4`), Y46, digit 1.0s, SFX tick por dígito. Aparece en el hook (atención) + en cada una de las 3 decisiones.
- **Loading bar:** horizontal Y52 (≥6% separación del countdown Y46 — heredado, evita overlap), beep tick acumulativo, termina con flash/cut a la consecuencia. Aparece tras cada decisión.
- **Decision-UI editorial pacing** (heredado de `../../choice-format-core/CHOICE-MECHANIC.md § 9` creative intent + `INGENIERO-CHOICE-CORE.md § 1` técnica): freeze frame + filter OPCIONAL (no obligatorio), pause beat 0.9s median, countdown sync al fin de la narración de la pregunta, loading Y52.

(No re-litigar estos specs — son los heredados.)

---

## Botones A/B de JUGADAS (lo sport-específico)

> Visualizan las dos opciones de la jugada. 🟦 El orden hablado = orden de botones (A = primera opción mencionada por el narrador).

### Visual intent
- **Layout:** dos paneles paired left/right, Y60-70 (heredado, safe zones IG).
- **Cada botón contiene:** letra grande (A / B) + texto de la jugada ("ENCARAS AL LATERAL" / "DEVUELVES SEGURO").
- **Color intent (decisión creativa, NO un patrón fijo):** ⚠️ a diferencia de horror (rojo=peligrosa / cyan=segura), en sport-choice **evitar mapear siempre un color a "la correcta"** — eso entrena al viewer a predecir (PAUTA-MASTER § 5 "B no siempre correcta" + § 10 anti-patterns). Opciones: ambos neutrales blancos; o tinte por riesgo (arriesgada vs conservadora) PERO rotando cuál paga entre decisiones/videos. El color NO debe spoilear la opción correcta.
- **(Opcional) porcentaje community:** "A — 67% · B — 33%" (crea sensación de comunidad votando). Decisión creativa.

### Ejemplos de botones por decisión
```
D1:  [ A ] ENCARAS AL LATERAL     [ B ] DEVUELVES SEGURO
D2:  [ A ] BUSCAS EL ÁNGULO       [ B ] ASISTES A TU COMPAÑERO
D3:  [ A ] LA CRUZAS              [ B ] LA PICAS
```

🟦 El texto de cada botón = una jugada concreta y clara (no "opción 1"). 🟦 El orden = el orden hablado por el narrador.

### SFX intent
- Pop sutil al aparecer; click sutil al final del countdown (jugada "consagrada"). Heredado.

---

## Watermark (heredado — handle canonical)

- **Texto:** `@elige_tucompanero` (handle canonical del proyecto — NUNCA `@referent-a` que es referencia only). Heredado de la preferencia permanente del creator.
- **Posición:** bottom, fuera de UI Instagram, opacidad 60-80%, persistente, sin animación. Heredado.

---

## Coordinación con captions (heredado)

UN elemento UI dominante por vez (heredado): si hay countdown, el caption narrativo baja; si hay loading bar, el countdown ya se fue. No overlap visual. Specs de no-overlap = `../../choice-format-core/INGENIERO-CHOICE-CORE.md § 2.3` (no-overlap matrix).

---

## Output al SPEC (ejemplo)

```yaml
ui_elements:
  name_labels:
    - { text: "SAKA", font: monospaced, fontsize_intent: large, y_pct: 11.5, tint_intent: red_arsenal_optional }
    - { text: "DEMBÉLÉ", font: monospaced, fontsize_intent: large, y_pct: 11.5, tint_intent: blue_psg_optional }
  context_caption:
    text: "SAKA = ARSENAL   ·   DEMBÉLÉ = PSG"   # 🟦 contexto de equipo EXPLÍCITO
    font: drop_shadow_canonical
    y_pct: 62
  countdown_strategy:
    appearances:
      - { timestamp_intent: hook, purpose: attention, is_real_decision: false }
      - { timestamp_intent: D1, purpose: decision, is_real_decision: true }
      - { timestamp_intent: D2, purpose: decision, is_real_decision: true }
      - { timestamp_intent: D3, purpose: decision, is_real_decision: true }
    visual_intent: film_leader_academy_avu   # heredado
    y_pct: 46
  loading_bars:
    appearances: [after_D1, after_D2, after_D3]
    y_pct: 52   # heredado, ≥6% sep del countdown
    end_transition_intent: flash_cut_to_consequence
  choice_buttons:
    - { decision: D1, option_a: "ENCARAS AL LATERAL", option_b: "DEVUELVES SEGURO" }
    - { decision: D2, option_a: "BUSCAS EL ÁNGULO", option_b: "ASISTES A TU COMPAÑERO" }
    - { decision: D3, option_a: "LA CRUZAS", option_b: "LA PICAS" }
    layout_intent: "paired side-by-side, Y60-70, safe zones IG"
    color_intent: "NO mapear color fijo a la correcta (rotar qué paga) — evita predicción"   # ⚠️ § 5 "B no siempre correcta" + § 10 anti-patterns
    order_rule: "orden de botones = orden hablado por el narrador (A=primera mencionada)"   # 🟦
    show_percentages: false   # decisión creativa
  watermark:
    text: "@elige_tucompanero"   # canonical
    y_pct: bottom
    opacity_intent: "60-70%"
    persistence: "todo el video sin animación"
```

---

## Anti-patterns en UI elements (sport)

❌ **Name labels sin caption de contexto de equipo** → no se resuelve rival/compañero.
❌ **Color de botón que siempre marca la correcta** → el viewer predice (§ 5 "B no siempre correcta" + § 10).
❌ **Orden de botones ≠ orden hablado** → el viewer se confunde sobre qué eligió (§ 10 anti-pattern "orden hablado ≠ botones").
❌ **Botones A/B sin texto de jugada** (solo A/B) → no se entiende qué jugada elige.
❌ **Watermark distinto a `@elige_tucompanero`** → rompe brand canonical.
❌ **UI elements amontonados** (countdown + loading + botones + caption simultáneos) → overload (heredado).
❌ **Re-definir specs heredados** (posiciones Y, monospaced) en vez de heredarlos.

---

## Validación final UI elements

- [ ] ¿Name labels (jugador) + caption de contexto (equipo) en el hook?
- [ ] ¿Countdown en hook + cada decisión (film leader AVU, Y46)?
- [ ] ¿Loading bar tras cada decisión (Y52, ≥6% sep)?
- [ ] ¿Botones A/B con texto de JUGADA + orden = orden hablado?
- [ ] ¿Color de botones NO spoilea la correcta?
- [ ] ¿Watermark `@elige_tucompanero` persistente?
- [ ] ¿UI no overlap (specs heredados)?
- [ ] ¿Posiciones Y = las heredadas (no re-definidas)?
