# script-writing.md — La lógica narrativa del formato sport-choice

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa de sport-choice** vive en `sport-choice-format/PAUTA-MASTER.md`. La **mecánica del formato choice** se hereda de `../../choice-format-core/CHOICE-MECHANIC.md` (agnóstica, derivada de los 8 virales vía horror). Este doc te ayuda a IMPLEMENTAR la lógica narrativa deportiva. Si hay conflicto → gana la pauta.
>
> Si llegaste acá sin leer las pautas, parar y leerlas primero.

---

> Este doc detalla CÓMO se arma narrativamente un guion sport-choice, slot a slot, traduciendo la mecánica del formato choice a contenido deportivo. Para la plantilla de escritura concreta ver `../SCRIPT-WRITING-GUIDE.md`; para la lógica de alto nivel ver `../PAUTA-MASTER.md`.

---

## El backbone narrativo (heredado, reskineado)

El guion sport-choice tiene el mismo backbone que el formato choice — la diferencia es el contenido de cada nodo. La estructura es **DOS RECORRIDOS COMPLETOS** (no "rama corta + rama profunda"):

```
ELECCIÓN = EQUIPO  →  RECORRIDO 1 (completo: setup → compuertas 2-3 → desenlace)  →  PIVOTE
   →  RECORRIDO 2 (completo: setup → compuertas → desenlace)  →  OUTRO / CTA
```

- El recorrido del FOIL (tagueado `counterfactual_*`) puede ir **al inicio O al final** (🟩 variabilidad — NO un opening fijo). El contraste entre los dos desenlaces ES el counterfactual.
- Los recorridos son SECUENCIALES (jamás interleaved) + el foil NUNCA aparece en el played path (§ tagging `PAUTA-MASTER.md § 4`).
- Timeline beat-a-beat con bandas % → `PAUTA-MASTER.md § 10.A`.

Todo se sincroniza al script timeline (igual que en el pipeline universal): `narration_script[]` con timestamps + `shot_list[]` con `narration_in_this_shot` por shot. La estructura no se inventa — se hereda.

---

## Nodo 1 — La elección = equipo (el corazón de sport-choice)

> 🟦 PRINCIPIO: presentar dos jugadores simultáneamente; elegir uno = jugar PARA su equipo; dar contexto EXPLÍCITO.

- **Dyad simultánea** en el hook (heredado de `../../choice-format-core/CHOICE-MECHANIC.md § 2.1` + name labels § 2.5): los dos jugadores en frame al mismo tiempo, name labels GRANDES (monospaced Y11.5), kits contrastantes.
- **El contexto de equipo es OBLIGATORIO y EXPLÍCITO:**
  - Narración: "Saka, Arsenal. Dembélé, PSG."
  - Caption: "SAKA = ARSENAL · DEMBÉLÉ = PSG"
- **Por qué:** dos jugadores de equipos distintos no pueden ser ambos tu compañero. La elección define tu equipo: el elegido es tu compañero, el otro (+ su kit) es el rival. Sin contexto explícito → el viewer no sabe si el otro es rival o aliado (la incoherencia que el formato resuelve).

🟥 ANTI-PATTERN: presentar el dyad sin decir qué equipo es cada uno → confusión rival/compañero.

---

## Nodo 2 — Dos recorridos completos + asimetría por favorito

> 🟦 PRINCIPIO: el video muestra los DOS recorridos completos (cada uno con setup + compuertas + desenlace), uno y luego el otro. La asimetría (cuántas compuertas tiene cada recorrido) sale del FAVORITO del partido (§ `PAUTA-MASTER.md § 4`). El contraste entre los dos desenlaces ES el counterfactual.

### Recorrido JUGADO (el del jugador elegido = protagonista)

- El viaje POV continuo del compañero elegido: setup → compuertas (2-3 según favorito) → desenlace.
- 🟦 Continuidad física shot-a-shot (anti-teleporte, EXECUTION CONTINUITY § 2). La cancha = la línea de tiempo.
- Tagging: `setup_pre_decision` → `decision_N` → `consequence_*` (es el played path; sus compuertas las cuenta el guard).
- 🟥 El foil NUNCA aparece acá: los rivales del played path son `rival_npc` genérico, NO el anchor de la estrella foil (ese reuso es el bug del topical champions — § `PAUTA-MASTER.md § 4`).

### Recorrido del FOIL (el contraste — counterfactual)

- El viaje POV completo del OTRO jugador para su equipo: su setup → sus compuertas → su desenlace propio. Es un recorrido ENTERO (no un glimpse de 3 shots).
- Tagueado `counterfactual_*`. La estrella foil aparece SOLO acá + en `hook` + `cliffhanger`.
- 🟩 **Orden libre:** puede ir al INICIO (counterfactual de apertura, emotional_framing `stakes_lift`) O al FINAL (`relief_contrast`). NO es un opening fijo. ⤴ `../../choice-format-core/CHOICE-MECHANIC.md § 6`.
- 🟦 **NO spoilea el otro recorrido** — son dos elecciones distintas, cada una con su desenlace.

### PIVOTE (el único corte no-continuo)

- Marca el pasaje de un recorrido al otro. NO es teleporte (que rompe inmersión DENTRO de un recorrido) — es un cambio de hipótesis explícito.
- 🟦 Marcarlo con un cue de bisagra ("SI HUBIERAS ELEGIDO A [el otro]…" / "Pero del otro lado…" / reset visual al círculo central con las mangas del otro kit) para que el viewer nunca se pierda de recorrido. ⤴ `PAUTA-MASTER.md § 10.A`.

### Asimetría por favorito (cuántas compuertas cada recorrido)

- Favorito → MENOS compuertas (~2, la gloria más cerca). No-favorito → MÁS compuertas (~3, más difícil). Banda 2-3; el guard flagea >3 (§ `PAUTA-MASTER.md § 4`/§ 5).
- 🟦 Invisible como editorial: se deriva del favorito real (cuotas/forma), NO se dice "este es el fácil".

---

## Nodo 3 — Las compuertas (2-3 por recorrido — jugadas reales)

> 🟦 PRINCIPIO: cada recorrido tiene 2-3 compuertas (favorito ~2 / no-favorito ~3, asimetría § Nodo 2); mecánica del dilema heredada (setup → pregunta → countdown → loading → consecuencia A + B); contenido = jugadas reales de tipos distintos con escalada de presión. Catálogo de jugadas-compuerta por posición POV → `../PAUTA-MASTER.md § 10.B`.

### Estructura de cada compuerta (heredada de `../../choice-format-core/CHOICE-MECHANIC.md § 5`)

```
1. SETUP (1-2 frases) — dónde estás en el campo, qué pasa ("Avanzas por la banda. El lateral te cierra.")
2. PREGUNTA — "Ahora decides. [OPCIÓN_A] o [OPCIÓN_B]."   🟦 orden hablado = orden de botones
3. COUNTDOWN 3-2-1 (film leader academy AVU, digit 1.0s) + botones A/B
4. LOADING BAR (Y52)
5. CONSECUENCIA ERRADA — la jugada se cae → rival capitaliza → abucheos   🟦 causal + humillación
6. CONSECUENCIA ACIERTO — avanzas a la siguiente zona / definís
```

### Variedad de jugadas (🟦 tipos distintos + escalada)

| Decisión | Zona | Tipo de jugada | Ejemplo |
|----------|------|----------------|---------|
| D1 | Banda / medio campo | Regate / encare | Encarar al lateral vs devolver seguro |
| D2 | Borde del área | Pase / visión | Buscar el ángulo vs asistir al compañero |
| D3 (clímax) | Mano a mano / definición | Definición | Cruzar al palo lejano vs picar |

🟩 VARIABILIDAD: qué jugada exacta, qué opción paga (rotar — no siempre la arriesgada ni siempre la conservadora), el fraseo condicional ("Si encaras…" / "Si vas al uno contra uno…").

🟥 ANTI-PATTERNS (PAUTA-MASTER § 10): "B" siempre correcta; decisión sin duda real; todas las compuertas del mismo tipo; consecuencia no causal.

---

## Nodo 4 — Las consecuencias (gol/gloria O error/burla)

> 🟦 PRINCIPIO: las consecuencias son 100% el partido. NO muerte, NO horror.

### Consecuencia de ERROR = humillación deportiva (el equivalente sport del body horror)

- **Visualizable + causal:** la jugada que se cae (pérdida → contraataque, tiro atajado, definición fallada) + la reacción social (abucheos, manos en la cabeza, el rival celebrando).
- **La humillación es SOCIAL y DEPORTIVA:** "El PSG gana y eres la burla" — memes, redes, abucheos de 67.000 personas. NUNCA física letal.
- 🟦 Causalmente justificada (§ 10 anti-pattern causal + § 10.C eslabón 7): un pase seguro no "pierde el balón"; una atajada implica tiro AL arco; gol implica balón DENTRO.

### Consecuencia de ACIERTO

- Avanzas (compuerta de creación) o definís (compuerta de definición). Acertar la cadena del recorrido → "Gol. [EQUIPO] es campeón."

### Resolución + Cliffhanger/CTA

- Vuelta olímpica, levantar la copa, confeti, el compañero te abraza ("Te lo dije, hermano" — lip-sync).
- El counterfactual ES el contraste entre los dos recorridos (ambos se muestran completos); NO se repite un cozy hogareño de horror.
- CTA verbal tagline: "Elige bien a tu compañero. Y vuelve mañana." (loop cross-video).

---

## Lenguaje (heredado de `../../choice-format-core/CHOICE-MECHANIC.md § 3`)

- 🟦 Segunda persona presente ("Avanzas", "Te la deja, le pegas").
- 🟦 Español NEUTRAL (tú/eliges) — NUNCA voseo.
- 🟦 Oraciones cortas, claras — la narración dice QUÉ pasa, no "suena épico". La épica viene del visual + rugido + música.
- 🟦 Word budget ≈ duración × 2.75 (165 WPM); narración ≤ min(duración shot, clip_max modelo) (HR#28/#29).

---

## La cadena de lógica que debe cerrar (recordatorio)

```
ELECCIÓN → EQUIPO → JUGADAS (coherentes con la posición/zona) → RESULTADO (gol&campeón / error&burla)
```

Cada eslabón explícito y coherente. Correr la plantilla de cadena causal (PAUTA-MASTER § 10.C) + los anti-patterns (§ 10) sobre cada decisión/consecuencia ANTES de emitir el SPEC.

---

## Anti-patterns en la escritura del guion sport

❌ **Hook sin contexto de equipo** → confusión rival/compañero.
❌ **Recorridos interleaved** (cortar de uno a otro beat-a-beat) o un recorrido que spoilea el otro → deben ser secuenciales, cada uno con su desenlace.
❌ **El foil aparece en el played path** (los rivales deben ser `rival_npc` genérico, NO el anchor del foil) → el bug del topical champions.
❌ **PIVOTE sin marcar** (el viewer cree que sigue la misma jugada) o teleporte DENTRO de un recorrido.
❌ **Decisiones que no son jugadas reales** (genéricas, sin zona/geografía).
❌ **Consecuencia de error que cae en horror** (muerte, sangre) en vez de humillación deportiva.
❌ **Consecuencia no causal** (pase seguro pierde el balón) o contradicción física (atajada vs tiro afuera).
❌ **Orden hablado ≠ orden de botones.**
❌ **"B" siempre correcta** / decisión sin duda real.
❌ **Narración estilizada** que prioriza "sonar épico" sobre claridad de la jugada.
