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
3. **El equipo del recorrido JUGADO** (el del jugador que elegís = protagonista) y el del recorrido del FOIL (el contraste, el camino no-elegido). Cada uno es un recorrido COMPLETO; el orden entre ellos es libre (ver estructura)
4. **La posición del POV** (extremo / delantero centro / mediapunta / lateral / arquero) — define las jugadas
5. **El tipo de jugada-clave del clímax** (mano a mano / penal / tiro libre / cabezazo) — rotar vs video anterior (ver `video-log.md`)
6. **Duración objetivo** (default: 90s)

---

## LA ESTRUCTURA DEL GUION SPORT-CHOICE

> 🟦 PRINCIPIO: la estructura es la del formato choice (heredada de `../choice-format-core/CHOICE-MECHANIC.md § 2` — esqueleto + invariante). Lo que cambia es el CONTENIDO de cada bloque (deportivo). El timeline de diseño beat-a-beat (con bandas %) vive en `PAUTA-MASTER.md § 10.A`.
>
> ⚠️ **DOS RECORRIDOS COMPLETOS, no una "rama corta + rama profunda".** Un video sport-choice muestra los DOS recorridos enteros, uno y luego el otro (cada uno con su setup, sus compuertas y su desenlace). El contraste entre los dos desenlaces ES el counterfactual. El recorrido del FOIL puede ir al INICIO o al FINAL (🟩 variabilidad — NO un "counterfactual opening fijo"). Lo que NUNCA varía 🟦: son SECUENCIALES (jamás interleaved) + el foil NUNCA aparece en el played path (los rivales del played path son `rival_npc` genérico, NO el anchor de la estrella foil — ver `PAUTA-MASTER.md § 4` tagging).

```
[BLOQUE 1 — HOOK / DYAD — 0-15%]
  Visual: POV frente a los DOS cracks en el círculo central, name labels GRANDES,
          kits contrastantes. Countdown 3-2-1 al final del hook. 🟦 0 cuts en el hook.
  Narración: "Final de la Champions. Elige tu compañero. [JUGADOR_A], [EQUIPO_A]. [JUGADOR_B], [EQUIPO_B]."
  Caption clave: "[JUGADOR_A] = [EQUIPO_A]   ·   [JUGADOR_B] = [EQUIPO_B]"   ← 🟦 contexto de equipo EXPLÍCITO

[RECORRIDO JUGADO — completo (setup + compuertas 2-3 + desenlace)]
  El viaje POV continuo del compañero ELEGIDO. La cancha = la línea de tiempo (mediocampo → banda
  → borde del área → mano a mano). 🟦 anti-teleporte: continuidad física shot-a-shot.

  · SETUP: "Avanzas por la banda. El lateral de [EQUIPO_RIVAL] te cierra."
  · COMPUERTA (×2-3 según favorito — favorito ~2 / no-favorito ~3, PAUTA § 4/§ 5):
       Pregunta: "Ahora decides. [OPCIÓN_A] o [OPCIÓN_B]."   ← 🟦 orden hablado = orden de botones (A=primera)
       Countdown 3-2-1 + loading bar + botones A/B.
       Consecuencia ✗ (errada): la jugada se cae → el rival capitaliza → abucheos.   ← 🟦 causal + humillación (catálogo § 6)
       Consecuencia ✓ (acierto): avanzas a la siguiente zona / quedas en posición de definir.
       (Las compuertas escalan de zona: creación → área → definición. TIPOS distintos — § 5.)
  · DESENLACE del recorrido jugado: acertar la cadena → "Gol. [EQUIPO] es campeón" (vuelta olímpica,
       copa, confeti); errar una compuerta → la jugada se cae rotando el catálogo § 6 → "eres la burla".
  · (Opcional) el protagonista habla con lip-sync ("Confía en ti. La metes." / "Te lo dije, hermano.")

[PIVOTE — el ÚNICO corte no-continuo permitido]
  Marca el pasaje de un recorrido al otro (NO es teleporte: es un cambio de hipótesis explícito).
  🟦 Marcarlo con un cue de bisagra (caption-puente "SI HUBIERAS ELEGIDO A [el otro]…" / línea
  "Pero del otro lado…" / reset al círculo central con las mangas del otro kit) para que el viewer
  NUNCA se pierda sobre en qué recorrido está. Ver PAUTA § 10.A.

[RECORRIDO DEL FOIL — completo (counterfactual, tagueado counterfactual_*)]
  El otro compañero/equipo: su setup → sus compuertas → su desenlace. Mismo tratamiento continuo.
  Muestra el camino-NO-tomado entero (no un glimpse). 🟩 Puede ir ANTES del recorrido jugado
  (counterfactual de apertura, emotional_framing stakes_lift) O DESPUÉS (relief_contrast).
  🟦 NO spoilea el otro recorrido — son dos elecciones distintas, ambas con su desenlace propio.

[OUTRO / CTA — 92-100%]
  Resolución de ambos recorridos ya mostrada. CTA: "Elige bien a tu compañero. Y vuelve mañana."
  ← tagline reconocible cross-video + watermark @elige_tucompanero persistente.
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
- 🟥 **ANTI-PATTERNS** (correr sobre cada decisión — ver PAUTA-MASTER § 10 + plantilla § 10.C): balón al rival, orden desalineado, consecuencia no causal, contradicción física (atajada vs tiro afuera), "B" siempre correcta, decisión sin duda real.

### Duración / pace (heredado — mecánica + universal)
- 🟦 ~90s total (banda 80-100s). ⤴ Duración total = `../choice-format-core/CHOICE-MECHANIC.md § 2`.
- 🟦 Word budget por shot ≈ `duration_intent_s × 2.75` (~165 WPM). ⤴ Pace WPM + narración-fits-duration (HR#28/#29 — narración ≤ min(duración del shot, clip_max del modelo)) = técnica universal `ai-video-production/MODEL-CAPABILITIES-MATRIX.md`.

---

## CHECKLIST DEL GUION (antes de pasar al SPEC)

- [ ] Hook con contexto de equipo EXPLÍCITO ("X = equipo A · Y = equipo B")
- [ ] DOS recorridos completos (cada uno setup + compuertas + desenlace) — NO "rama corta + profunda"
- [ ] Recorridos SECUENCIALES (jamás interleaved) + el foil tagueado `counterfactual_*` puede ir al inicio O al final
- [ ] El foil NUNCA aparece en el played path (rivales del played path = `rival_npc` genérico, NO el anchor del foil)
- [ ] PIVOTE marcado con cue de bisagra (el único corte no-continuo) — el viewer nunca se pierde de recorrido
- [ ] Compuertas por recorrido = 2-3 (favorito ~2 / no-favorito ~3) = jugadas de tipos distintos, escalada de zona
- [ ] Cada compuerta: setup + pregunta (orden = botones) + consecuencia errada (causal + humillación) + consecuencia acierto
- [ ] Consecuencia de error = humillación deportiva (abucheos/memes/burla), NUNCA muerte/horror
- [ ] Acertar la cadena → gol → campeón → vuelta olímpica + CTA
- [ ] Cadena de lógica cierra en AMBOS recorridos (elección → equipo → jugadas → resultado) — plantilla § 10.C
- [ ] Anti-patterns corridos sobre cada compuerta (§ PAUTA-MASTER 10)
- [ ] "B" no siempre correcta; cada decisión genera duda real
- [ ] Español neutral, 2ª persona presente, oraciones cortas claras
- [ ] Framing acción-condicional (no bare label), ~90s, watermark `@elige_tucompanero`

---

## EJEMPLO DE GUION (ilustrativo — NO de una producción nuestra)

> ⚠️ Ejemplo de enseñanza con jugadores/equipos genéricos. NO es el guion de ningún video shipped (sport-choice tiene 0 videos shipped — HR#19: nuestras producciones NO son autoridad). Muestra la estructura DOS RECORRIDOS con el recorrido del foil al FINAL (orden 🟩 variable — también válido al inicio).

```
[HOOK] "Final. Elige tu compañero. [CRACK_A], [EQUIPO_A]. [CRACK_B], [EQUIPO_B]."
       Caption: [CRACK_A] = [EQUIPO_A]   ·   [CRACK_B] = [EQUIPO_B]

[RECORRIDO JUGADO — elegiste a [CRACK_A], juegas para [EQUIPO_A]]
  [SETUP+C1] "Avanzas por la banda. El lateral de [EQUIPO_B] te cierra.
              Ahora decides. Encaras al lateral o devuelves seguro."
     (errada) "Si devuelves, la jugada se enfría: [EQUIPO_B] se reordena y la chance se apaga. La hinchada se queja."
     (acierto) "Si encaras, dejas atrás al lateral y avanzas al borde del área."

  [C2] "Llegas al borde del área. Ahora decides. Buscas el ángulo o asistes a [CRACK_A]."
     (errada) "Si buscas el ángulo desde lejos, el arquero la saca. [EQUIPO_B] contraataca."
     (acierto) "Si asistes a [CRACK_A], te la devuelve y quedas solo ante el arquero."

  [C3 clímax] [CRACK_A]: "Confía en ti. La metes."
              "Mano a mano. Ahora decides. La cruzas o picas."
     (errada) "Si la picas, el arquero la atrapa. [EQUIPO_B] gana y eres la burla."
     (acierto) "Si la cruzas al palo lejano, gol. [EQUIPO_A] es campeón."
  [desenlace jugado] [CRACK_A]: "Te lo dije, hermano." — vuelta olímpica, copa, confeti.

[PIVOTE] "Pero del otro lado, con [CRACK_B]…"   ← cue de bisagra (el único corte no-continuo)

[RECORRIDO DEL FOIL — completo (counterfactual_*)]
  El viaje POV de [CRACK_B] para [EQUIPO_B]: su setup → sus compuertas → su desenlace propio.
  Muestra el camino-NO-tomado entero (no un glimpse). NO spoilea el recorrido jugado.

[OUTRO] "Elige bien a tu compañero. Y vuelve mañana."
```

> ⚠️ **Nota de enseñanza sobre la C1 (anti-pattern causal, PAUTA-MASTER § 10 + § 10.C eslabón 7):** la consecuencia conservadora se "castiga" perdiendo la **CHANCE** de gol (la jugada se enfría / la presión baja), NO con un error físicamente improbable. Un pase seguro normalmente NO "pierde el balón" — devolver mantiene posesión. Por eso el ejemplo dice "la jugada se enfría / la chance se apaga", no "pierdes el balón". Este es exactamente el chequeo que el arquitecto corre (§ 10.C eslabón 7) antes de emitir el SPEC.
