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

El guion sport-choice tiene el mismo backbone que el formato choice — la diferencia es el contenido de cada nodo:

```
ELECCIÓN = EQUIPO  →  RAMA CORTA (foil glorioso, counterfactual opening)  →  PIVOTE
   →  RAMA PROFUNDA: D1 (banda) → D2 (área) → D3 (clímax)  →  RESOLUCIÓN (gol/copa)  →  CLIFFHANGER/CTA
```

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

## Nodo 2 — Ramas asimétricas

> 🟦 PRINCIPIO: una rama corta (foil glorioso) ocupa el counterfactual de apertura; una rama profunda (interactiva) es el núcleo.

### Rama CORTA (el foil) — counterfactual opening

- ~3 shots, glimpse veloz: "Si eliges al OTRO jugador, juegas para su equipo → te deja el balón → le pegas → GOL → su equipo campeón → gloria rápida".
- Va PRIMERO (counterfactual ANTES de que resuelva la rama jugable — heredado de ref-09, sube stakes).
- Tono = warm glory (celebración cálida).
- 🟦 **NO spoilea la rama profunda** — muestra el desenlace del camino-NO-tomado (el otro equipo).

### PIVOTE

- 1 shot corto: corte de la hipótesis del foil a la realidad. "Pero elegiste a [PROTAGONISTA]. Juegas para [EQUIPO]."
- Visual: el viewer ve sus propias mangas del equipo elegido + el compañero a su lado pidiendo arrancar la jugada.

### Rama PROFUNDA — el viaje interactivo

- El núcleo: las 3 decisiones de juego + consecuencias.
- Acertar las 3 → gol → campeón. Errar cualquiera → la jugada se cae → el rival gana → eres la burla.

---

## Nodo 3 — Las 3 decisiones (jugadas reales)

> 🟦 PRINCIPIO: mecánica del dilema heredada (setup → pregunta → countdown → loading → consecuencia A + B); contenido = jugadas reales de tipos distintos con escalada de presión.

### Estructura de cada decisión (heredada de `../../choice-format-core/CHOICE-MECHANIC.md § 5`)

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

🟥 ANTI-PATTERNS (PAUTA-MASTER § 6): "B" siempre correcta; decisión sin duda real; las 3 del mismo tipo; consecuencia no causal.

---

## Nodo 4 — Las consecuencias (gol/gloria O error/burla)

> 🟦 PRINCIPIO: las consecuencias son 100% el partido. NO muerte, NO horror.

### Consecuencia de ERROR = humillación deportiva (el equivalente sport del body horror)

- **Visualizable + causal:** la jugada que se cae (pérdida → contraataque, tiro atajado, definición fallada) + la reacción social (abucheos, manos en la cabeza, el rival celebrando).
- **La humillación es SOCIAL y DEPORTIVA:** "El PSG gana y eres la burla" — memes, redes, abucheos de 67.000 personas. NUNCA física letal.
- 🟦 Causalmente justificada (§ 6 anti-pattern #3): un pase seguro no "pierde el balón"; una atajada implica tiro AL arco; gol implica balón DENTRO.

### Consecuencia de ACIERTO

- Avanzas (D1/D2) o definís (D3). Acertar las 3 → "Gol. [EQUIPO] es campeón."

### Resolución + Cliffhanger/CTA

- Vuelta olímpica, levantar la copa, confeti, el compañero te abraza ("Te lo dije, hermano" — lip-sync).
- El counterfactual ya se mostró al inicio (rama corta), NO se repite un cozy hogareño.
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

Cada eslabón explícito y coherente. Correr los 7 anti-patterns (PAUTA-MASTER § 6) sobre cada decisión/consecuencia ANTES de emitir el SPEC.

---

## Anti-patterns en la escritura del guion sport

❌ **Hook sin contexto de equipo** → confusión rival/compañero.
❌ **Ramas simétricas o rama corta que spoilea la profunda.**
❌ **Decisiones que no son jugadas reales** (genéricas, sin zona/geografía).
❌ **Consecuencia de error que cae en horror** (muerte, sangre) en vez de humillación deportiva.
❌ **Consecuencia no causal** (pase seguro pierde el balón) o contradicción física (atajada vs tiro afuera).
❌ **Orden hablado ≠ orden de botones.**
❌ **"B" siempre correcta** / decisión sin duda real.
❌ **Narración estilizada** que prioriza "sonar épico" sobre claridad de la jugada.
