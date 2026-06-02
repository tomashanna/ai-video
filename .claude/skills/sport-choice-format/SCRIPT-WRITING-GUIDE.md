# SCRIPT-WRITING-GUIDE.md — Cómo generar guiones del formato "Sport-Choice"

> Este documento se le pasa a Claude como contexto cuando se le pide generar un guion sport-choice. La AUTORIDAD creativa es `PAUTA-MASTER.md`; este doc es la guía de ESCRITURA del guion deportivo.

> ⚠️ **CÓMO LEER ESTE DOC (lente principio/variabilidad/anti-pattern — mismo framing que horror-choice).** El formato choice NO tiene reglas rígidas en sus elecciones creativas: tiene **flexibilidad dentro de un marco**. Tres niveles:
> - 🟦 **PRINCIPIO (mandatorio)** — el mecanismo que hace funcionar el formato. NO negociable. Ej: "la elección = equipo, con contexto explícito"; "la consecuencia sigue causalmente de la jugada".
> - 🟩 **VARIABILIDAD (libre)** — cómo ejecutás el principio. Múltiples formas válidas. Ej: el fraseo del framing condicional ("Si encaras…" / "Si decides encarar…" / "Si vas al uno contra uno…"); qué jugada-clave usás en el clímax.
> - 🟥 **ANTI-PATTERN (evitar)** — formas que rompen la credibilidad futbolística. Ej: pasarle el balón a un rival; "devuelves seguro y pierdes el balón" (no causal).
>
> Si algo acá suena a "regla binaria obligatoria" sobre una **elección creativa**, es un bug de framing — reportalo. La MECÁNICA (countdown, decisiones binarias, counterfactual, POV) sí es regla dura, **heredada de `../choice-format-core/CHOICE-MECHANIC.md`** (agnóstica, común a horror y sport).

---

## CÓMO USAR ESTE DOCUMENTO

Para generar un guion nuevo, pegale a Claude:
1. Este documento + `PAUTA-MASTER.md` (sport) + la MECÁNICA agnóstica de `../choice-format-core/CHOICE-MECHANIC.md`
2. Los inputs del usuario (partido/equipos/jugadores, topical o ficticio, tipo de jugada-clave deseada)
3. La instrucción: "Generá un guion sport-choice siguiendo la plantilla y respetando la lógica deportiva (cadena que cierra + 7 anti-patterns) + la mecánica heredada".

Claude responde con: el guion completo en español NEUTRAL, con timings calculados para ~90s, framing acción-condicional, y la cadena de lógica deportiva cerrada.

---

## INPUTS REQUERIDOS DEL USUARIO

Antes de generar, pedile al usuario estos datos. Si faltan, pedilos primero:

1. **Los dos jugadores del dyad + sus equipos** (p.ej. Saka/Arsenal y Dembélé/PSG). ¿Reales (topical) o ficticios?
2. **El partido / contexto** (final de Champions, derbi, clásico, último minuto, etc.)
3. **El equipo de la rama PROFUNDA** (el jugable — qué jugador es el "compañero protagonista") y el de la rama CORTA (el foil)
4. **La posición del POV** (extremo / delantero centro / mediapunta / lateral / arquero) — define las jugadas
5. **El tipo de jugada-clave del clímax** (mano a mano / penal / tiro libre / cabezazo) — rotar vs video anterior (ver `video-log.md`)
6. **Duración objetivo** (default: 90s)

---

## LA ESTRUCTURA DEL GUION SPORT-CHOICE

> 🟦 PRINCIPIO: la estructura es la del formato choice (heredada de `../choice-format-core/CHOICE-MECHANIC.md § 2` — esqueleto + invariante). Lo que cambia es el CONTENIDO de cada bloque (deportivo).

```
[BLOQUE 1 — HOOK / DYAD — 0:00 a ~0:09 (0-15%)]
  Visual: POV frente a los DOS jugadores en el círculo central, name labels GRANDES,
          kits contrastantes. Countdown 3-2-1 al final del hook.
  Narración: "Final de la Champions. Elige tu compañero. [JUGADOR_A], [EQUIPO_A]. [JUGADOR_B], [EQUIPO_B]."
  Caption clave: "[JUGADOR_A] = [EQUIPO_A]   ·   [JUGADOR_B] = [EQUIPO_B]"   ← 🟦 contexto de equipo EXPLÍCITO

[BLOQUE 2 — RAMA CORTA (foil, counterfactual opening) — ~0:09 a ~0:23 (15-25%)]
  Visual: glimpse veloz del foil → el favorito te deja el balón → le pegas → GOL → su equipo campeón → gloria rápida.
  Narración: "Si eliges a [FOIL], juegas para [EQUIPO_B]. Te la deja, le pegas, y la clavas.
              Gol. [EQUIPO_B] es campeón y levantas la copa."
  🟦 NO spoilea el resultado de la rama profunda. Es el camino-no-tomado glorioso.

[BLOQUE 3 — PIVOTE — ~0:20 a ~0:24]
  Visual: corte de la hipótesis del foil a la realidad jugable (tus mangas son del otro equipo).
  Narración: "Pero elegiste a [PROTAGONISTA]. Juegas para [EQUIPO_A]."

[BLOQUE 4 — SETUP + DECISIÓN 1 (banda/medio campo) — ~0:24 a ~0:44 (25-50%)]
  Setup: "Avanzas por la banda. El lateral de [EQUIPO_B] te cierra."
  Pregunta: "Ahora decides. [OPCIÓN_A] o [OPCIÓN_B]."   ← 🟦 orden hablado = orden de botones (A=primera, B=segunda)
  Countdown 3-2-1 + loading bar + botones A/B.
  Consecuencia errada: la jugada se cae → el rival sale → abucheos.   ← 🟦 causal + humillación
  Consecuencia acierto: dejas atrás al rival → avanzas a la siguiente zona.

[BLOQUE 5 — DECISIÓN 2 (borde del área) — ~0:44 a ~0:65 (50-72%)]
  Setup: "Llegas al borde del área."
  Pregunta: "Ahora decides. [OPCIÓN_A] o [OPCIÓN_B]."   (TIPO de jugada distinto al D1 — ej: pase/visión)
  Countdown + loading + botones.
  Consecuencia errada: el arquero la saca / el rival contraataca → abucheos.
  Consecuencia acierto: quedas en posición de definir.

[BLOQUE 6 — DECISIÓN 3 / CLÍMAX (mano a mano u otra jugada-clave) — ~0:65 a ~0:83 (72-92%)]
  (Opcional) El protagonista habla: "Confía en ti. La metes."   ← lip-sync
  Pregunta: "[CONTEXTO clímax]. Ahora decides. [OPCIÓN_A] o [OPCIÓN_B]."   (TIPO: definición)
  Countdown + loading + botones.
  Consecuencia errada: el arquero la atrapa / la mandas afuera → "[EQUIPO_B] gana y eres la burla."
  Consecuencia acierto: "Gol. [EQUIPO_A] es campeón."

[BLOQUE 7 — RESOLUCIÓN + CLIFFHANGER / CTA — ~0:83 a 0:90 (92-100%)]
  Visual: vuelta olímpica, levantar la copa, confeti, el compañero te abraza.
  (Opcional) Protagonista: "Te lo dije, hermano."   ← lip-sync
  CTA: "Elige bien a tu compañero. Y vuelve mañana."   ← tagline reconocible cross-video
```

---

## REGLAS DE ESCRITURA

> Esta sección lista SOLO el DELTA deportivo. La mecánica de escritura AGNÓSTICA (lenguaje 2ª persona presente + español neutral + oraciones cortas/claras + narración no-estilizada; framing acción-condicional como PRINCIPIO 🟦 / variabilidad 🟩 / anti-pattern bare-label 🟥; estructura de cada decisión; "orden hablado = orden de botones") **se HEREDA de `../choice-format-core/CHOICE-MECHANIC.md § 3`** y NO se redefine acá. Leer ese doc primero. Abajo, solo el sabor sport sobre esas reglas + la lógica deportiva net-new.

### Lenguaje + framing — el sabor sport sobre la mecánica heredada
- ⤴ Reglas base (2ª persona, español neutral, oraciones cortas, narración clara no-estilizada, framing acción-condicional sin bare label) → `../choice-format-core/CHOICE-MECHANIC.md § 3`.
- 🟩 **Fraseo condicional reskineado a la jugada (variabilidad libre):** "Si encaras…" / "Si devuelves…" / "Si la cruzas…" / "Si picas…" / "Si asistes a tu compañero…". Elegí el fraseo que mejor suene con la jugada.
- 🟦 **La narración dice QUÉ pasa EN LA JUGADA, no "suena épico":** la épica emerge del visual + rugido de hinchada + música, no de la narración.

### Lógica deportiva (sport-específico — la sección crítica)
- 🟦 **La elección = equipo, con contexto explícito** (caption + narración).
- 🟦 **Las consecuencias siguen causalmente de la jugada** (un pase seguro NO pierde el balón; una atajada implica un tiro AL arco).
- 🟦 **Orden hablado = orden de botones** (A = primera opción mencionada).
- 🟦 **Las 3 decisiones son jugadas de TIPOS distintos** (regate/encare, pase/visión, definición) con escalada de presión.
- 🟩 **VARIABILIDAD:** qué jugada exacta, qué opción paga (rotar — no siempre A ni siempre B), qué tono de humillación.
- 🟥 **ANTI-PATTERNS** (correr sobre cada decisión — ver PAUTA-MASTER § 6): balón al rival, orden desalineado, consecuencia no causal, contradicción física (atajada vs tiro afuera), "B" siempre correcta, decisión sin duda real.

### Duración / pace (heredado — mecánica + universal)
- 🟦 ~90s total (banda 80-100s). ⤴ Duración total = `../choice-format-core/CHOICE-MECHANIC.md § 2`.
- 🟦 Word budget por shot ≈ `duration_intent_s × 2.75` (~165 WPM). ⤴ Pace WPM + narración-fits-duration (HR#28/#29 — narración ≤ min(duración del shot, clip_max del modelo)) = técnica universal `ai-video-production/MODEL-CAPABILITIES-MATRIX.md`.

---

## CHECKLIST DEL GUION (antes de pasar al SPEC)

- [ ] Hook con contexto de equipo EXPLÍCITO ("X = equipo A · Y = equipo B")
- [ ] Rama corta (foil glorioso) primero + pivote + rama profunda (3 decisiones)
- [ ] La rama corta NO spoilea la profunda
- [ ] 3 decisiones = jugadas de tipos distintos, escalada banda → área → clímax
- [ ] Cada decisión: setup + pregunta (orden = botones) + consecuencia errada (causal + humillación) + consecuencia acierto
- [ ] Consecuencia de error = humillación deportiva (abucheos/memes/burla), NUNCA muerte/horror
- [ ] Acierto en las 3 → gol → campeón → vuelta olímpica + CTA
- [ ] Cadena de lógica cierra (elección → equipo → jugadas → resultado)
- [ ] 7 anti-patterns corridos (§ PAUTA-MASTER 6)
- [ ] "B" no siempre correcta; cada decisión genera duda real
- [ ] Español neutral, 2ª persona presente, oraciones cortas claras
- [ ] Framing acción-condicional (no bare label), ~90s, watermark `@elige_tucompanero`

---

## EJEMPLO DE GUION (extracto — del primer video `champions-sport-choice`)

```
[HOOK] "Final de la Champions. Elige tu compañero. Saka, Arsenal. Dembélé, PSG."
       Caption: SAKA = ARSENAL   ·   DEMBÉLÉ = PSG

[RAMA CORTA] "Si eliges a Dembélé, juegas para el PSG. Te la deja, le pegas, y la clavas.
              Gol. El PSG es campeón y levantas la copa."

[PIVOTE] "Pero elegiste a Saka. Juegas para Arsenal."

[SETUP+D1] "Avanzas por la banda. El lateral del PSG te cierra.
            Ahora decides. Encaras al lateral o devuelves seguro."
   (errada) "Si devuelves, pierdes el balón y el PSG sale. La hinchada te abuchea."   ← nota: ver § anti-pattern causal abajo
   (acierto) "Si encaras, dejas atrás al lateral y avanzas al borde del área."

[D2] "Llegas al borde del área. Ahora decides. Buscas el ángulo o asistes a Saka."
   (errada) "Si buscas el ángulo desde lejos, el arquero la saca. El PSG contraataca."
   (acierto) "Si asistes a Saka, te la devuelve y quedas solo ante el arquero."

[D3 clímax] Saka: "Confía en ti. La metes."
            "Mano a mano. Ahora decides. La cruzas o picas."
   (errada) "Si la picas, el arquero la atrapa. El PSG gana y eres la burla."
   (acierto) "Si la cruzas al palo lejano, gol. El Arsenal es campeón."

[OUTRO] Saka: "Te lo dije, hermano."
        "Elige bien a tu compañero. Y vuelve mañana."
```

> ⚠️ **Nota de revisión sobre el D1 del ejemplo** (anti-pattern causal #3, PAUTA-MASTER § 6): la consecuencia errada "Si devuelves, **pierdes el balón**" del primer video roza el anti-pattern de causalidad (un pase seguro normalmente NO pierde el balón — devolver mantiene posesión). El fraseo causalmente más limpio sería que devolver **mata la oportunidad / enfría la jugada** y la presión baja (el PSG sale jugando tranquilo), no una pérdida directa. Considerar este ajuste en futuros videos o en re-iteración: la opción conservadora se "castiga" perdiendo la CHANCE de gol, no con un error físicamente improbable. Este es exactamente el tipo de chequeo que el arquitecto debe correr (§ 6 anti-pattern #3) antes de emitir el SPEC.
