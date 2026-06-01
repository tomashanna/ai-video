# PAUTA-MASTER.md — Pauta del formato "Sport-Choice" (drama deportivo interactivo)

> **AUTORIDAD CREATIVA del formato sport-choice** (rol 🏛️ ARQUITECTO). Define la HISTORIA/LÓGICA del formato.
>
> ⚠️ **ESTADO METODOLÓGICO (leer primero, § 0).** A diferencia de `horror-choice-format/PAUTA-MASTER.md` (derivada EMPÍRICAMENTE de 8 videos virales canónicos), sport-choice **AÚN NO tiene referentes virales propios medidos**. Esta pauta es:
> - **MECÁNICA heredada** de horror-choice (validada en 8 virales) → se reusa tal cual.
> - **LÓGICA deportiva = diseño net-new** del arquitecto + las indicaciones de Tomás (fuente) + el SPEC validado `creative-specs/champions-sport-choice.yaml`. Esta capa se VALIDARÁ empíricamente con nuestros primeros videos (igual que horror-choice se validó con sus 8). Cada hallazgo se loguea en `video-log.md` y se promueve acá cuando hay patrón observado.
>
> **Última actualización:** 2026-05-31 (creación)
> **Versión:** v0.1 (pre-empírico — fase de validación)

---

## 0. METODOLOGÍA — DE DÓNDE VIENEN ESTAS REGLAS

### Las dos fuentes de esta pauta

| Capa | Fuente | Estado de validación |
|------|--------|----------------------|
| **MECÁNICA del formato choice** (estructura temporal, hook dyad, countdown, decisiones binarias, framing acción-condicional, counterfactual, cliffhanger, POV >80%, lenguaje 2ª persona presente) | `horror-choice-format/PAUTA-MASTER.md` — derivada de **8 videos virales canónicos** | ✅ VALIDADO empíricamente (8/8). Se HEREDA. |
| **LÓGICA deportiva** (elección=equipo, ramas asimétricas, decisiones=jugadas, consecuencias=gol/burla, paleta SFX fútbol) | Diseño del arquitecto + indicaciones de Tomás + SPEC `champions-sport-choice.yaml` | 🟡 DISEÑO (pre-empírico). Se valida con nuestros primeros videos. |

### Lo que esto significa

- **TODA regla de MECÁNICA** está validada contra los 8 virales de horror-choice. Para esas reglas, la autoridad última es `horror-choice-format/PAUTA-MASTER.md` (leé las secciones de estructura allí — no las re-litigamos acá).
- **TODA regla de LÓGICA deportiva** es diseño inicial. Si un video demuestra que una de estas reglas falla, se revisa acá y se loguea en `video-log.md`. No están "talladas en piedra empírica" todavía — están en su primera iteración.
- **No inventar autoridad empírica que no existe.** Cuando esta pauta diga "diseño" o "fase de validación", es honesto: no hay 8 videos detrás de la lógica deportiva todavía.

### Cross-ref con la mecánica heredada

Cuando esta pauta diga "se hereda § X de horror-choice", andá a `horror-choice-format/PAUTA-MASTER.md` § X para el detalle empírico (con compliance N/8). PAUTA sport = QUÉ cambia en la lógica deportiva; horror-choice PAUTA = la mecánica del formato choice que NO cambia.

### Lo que NO es base de pauta (BAN)

- ❌ Tratar la lógica deportiva como "empíricamente validada" antes de tener videos shipped — es diseño en validación.
- ❌ Inventar reglas mid-conversación que contradigan ESTA pauta o la mecánica heredada — si un caso justifica desvío, escalar a Tomás PRIMERO.
- ❌ Cualquier elemento de horror (muerte, body horror, monstruos, drones de terror, gritos) — sport-choice es drama deportivo, no terror disfrazado de fútbol.

---

## 1. FILOSOFÍA — LA REGLA DE ORO + LA ELECCIÓN = EQUIPO

> **El formato es el GENERADOR de creatividad, no el LÍMITE** (se hereda de horror-choice § 1). El espectador viene por la fórmula reconocible (countdown, dilema binario, consecuencia, cliffhanger). La creatividad vive en QUÉ poblamos esos slots con contenido deportivo, no en romper la mecánica.

### La regla fundacional de sport-choice: la elección del hook = EQUIPO / identidad

> **Se presentan DOS jugadores, uno de cada equipo. Elegir a un jugador = jugás PARA ese equipo.**

- Si eliges a Saka → juegas para el Arsenal.
- Si eliges a Dembélé → juegas para el PSG.

**SIEMPRE dar contexto explícito al viewer** sobre qué significa cada elección. El narrador / los captions deben decir literalmente "Si eliges a X, juegas para el equipo A… / Si eliges a Y, para el equipo B…". Sin este contexto, el viewer no entiende si el otro jugador es su rival o su compañero.

**Por qué esto importa tanto:** resuelve de raíz la **incoherencia rival/compañero**. En horror-choice "elegir compañero" es literal (con quién pasás la noche). En fútbol, dos jugadores de equipos distintos NO pueden ser ambos tus compañeros. La solución: la elección define tu equipo. El elegido es tu compañero; el otro (y su kit) es el rival. Esto debe quedar CLARÍSIMO desde el hook.

### El emparejamiento dyad

- Los dos jugadores se presentan **simultáneamente** en el hook (se hereda de horror § 3 personajes).
- **Name labels GRANDES** (monospaced, Y11.5) sobre cada uno (se hereda).
- **Contraste visual obligatorio**: kits de colores opuestos (rojo vs azul), posturas distintas. El kit ES el contraste visual — no necesitamos uncanny, necesitamos identidad de equipo legible.

---

## 2. ESTRUCTURA — RAMAS ASIMÉTRICAS EN UN VIDEO

> Se hereda la **estructura temporal** de horror-choice § 2 (duración 80-100s, distribución por fase). Lo sport-específico es **CÓMO se reparten las dos ramas de la elección del hook**.

### Las dos ramas (la innovación estructural de sport-choice)

Un video sport-choice resuelve la elección del hook con **dos ramas asimétricas**:

| Rama | Qué es | Duración relativa | Función |
|------|--------|-------------------|---------|
| **RAMA CORTA** (el foil) | "Si eliges al OTRO jugador, juegas para el equipo B → la jugada sale redonda → gol → campeón, gloria rápida" | ~3 shots, glimpse veloz (ocupa el slot del **counterfactual de APERTURA**) | El camino-no-tomado glorioso. Sube los stakes y crea contraste emocional ANTES de entrar a la rama jugable. **NO spoilea el resultado de la rama profunda.** |
| **RAMA PROFUNDA** (el viaje interactivo) | "Pero elegiste a X, juegas para el equipo A" → las 3 decisiones de juego → desenlace | Núcleo del video (las 3 decisiones + consecuencias) | El viaje real. Acertar las 3 → gol → campeón. Errar cualquiera → la jugada se cae → el rival gana → eres la burla. |

### Por qué la rama corta va PRIMERO (counterfactual opening)

Se hereda de horror-choice § 24 / ref-09 (10/10 en comprensión narrativa): el **counterfactual ANTES de que resuelva la rama jugable** sube los stakes. En sport-choice esto se calca: mostramos primero la gloria veloz del foil ("si elegías al otro, ganabas fácil"), creando el contraste emocional que hace que la rama profunda pese más ("pero elegiste a este, y ahora todo depende de vos").

**Anti-spoiler:** la rama corta NO revela cómo termina la rama profunda. Muestra el desenlace del CAMINO-NO-TOMADO (el otro equipo), no del elegido.

### Distribución por fase (heredada + reskineada)

| Fase | % del video | Función sport-choice |
|------|-------------|----------------------|
| **Hook + dyad** | 0-15% | Dos jugadores + name labels + "Elige tu compañero" + contexto equipo + countdown |
| **Rama corta (counterfactual opening)** | 15-25% | Glimpse del foil: eliges al otro → gol → campeón (gloria rápida) → pivote |
| **Setup + 3 decisiones de juego** | 25-85% | Cada decisión = jugada real con countdown + loading bar + consecuencia (avanza o se cae) |
| **Resolución del clímax (D3)** | 85-92% | Definir mano a mano: gol & campeón O error & burla |
| **Cliffhanger + CTA** | 92-100% | Vuelta olímpica / outro + "Elige bien a tu compañero. Vuelve mañana." |

---

## 3. LAS DECISIONES = JUGADAS REALES + CONSECUENCIAS = EL PARTIDO

> Se hereda la **mecánica del dilema** de horror-choice § 11 (setup → pregunta → countdown → loading bar → consecuencia A → consecuencia B). Lo sport-específico es QUÉ pueblan esos slots: jugadas reales de fútbol con consecuencias 100% futbolísticas.

### Las decisiones son jugadas reales

Cada decisión binaria es una **disyuntiva de juego** que un futbolista realmente enfrenta en una jugada decisiva:

| # | Zona del campo | Disyuntiva (ejemplos) |
|---|----------------|------------------------|
| D1 | Banda / medio campo | Encarar al lateral **o** devolver seguro |
| D2 | Borde del área | Buscar el ángulo desde lejos **o** asistir a tu compañero |
| D3 (clímax) | Mano a mano con el arquero | Definir cruzado al palo lejano **o** picarla |

**Regla de variedad** (heredada de horror § 11): las 3 decisiones deben ser de TIPOS distintos de jugada (no las 3 "definir al arco"). Una de regate/encare, una de pase/visión, una de definición. Mantiene la jugada creíble y la escalada de presión.

**Escalada de presión** (heredada de horror § escalada): la presión sube zona por zona — banda → borde del área → mano a mano. El clímax (D3) es el momento de máxima tensión, mano a mano con el arquero.

### Las consecuencias son 100% el partido

> **El enfoque es ESTAR decidiendo dentro del partido. Cada resultado es consecuencia futbolística directa.** NO body horror, NO muerte — el "castigo" del error es la HUMILLACIÓN DEPORTIVA.

| Resultado de la decisión | Consecuencia |
|--------------------------|--------------|
| **Opción ARRIESGADA-pero-CORRECTA** (la que paga) | La jugada de gol avanza. Dejas atrás al rival, llegas a la siguiente zona, te quedas mano a mano, la clavas. |
| **Opción ERRADA** | Error → la jugada se cae → el rival capitaliza (sale jugando, contraataca, el arquero la saca) → **PIERDES** y eres **LA BURLA** (memes, redes sociales, abucheos de la hinchada, "el hazmerreír"). |
| **Acertar las 3** | **GOL → CAMPEÓN.** Levantas la copa (la orejona), GLORIA, vuelta olímpica, el estadio estalla. |

### El catálogo de "consecuencias de error" (el equivalente sport del body horror)

Donde horror-choice tiene body horror específico (§ 12), sport-choice tiene **fracaso deportivo específico + humillación social**. Nunca "fallas" genérico — siempre una imagen concreta de la jugada que se cae + la reacción social:

1. **Pérdida de balón → contraataque rival** (devolviste y el rival salió jugando)
2. **Tiro desviado / atajado → el rival respira** (buscaste el ángulo imposible, el arquero la saca)
3. **Definición fallada mano a mano → el arquero la atrapa / la mandas afuera**
4. **La humillación social** (siempre acompaña al error): abucheos de la hinchada, memes en redes, "eres la burla", el rival celebrando en tu cara, manos a la cabeza.

**Regla:** el error debe ser **visualizable concretamente** (la IA puede generar la jugada que se cae) + **causalmente justificado** (ver § 6: un pase seguro no "pierde el balón"; una atajada implica un tiro AL arco). La humillación es social y deportiva — NO física letal.

---

## 4. SIN HORROR — LA DIFERENCIA CENTRAL

> **sport-choice es drama deportivo, NO horror disfrazado de fútbol.**

- ❌ **NO muerte.** El "castigo" del error es perder el partido + ser la burla, no morir.
- ❌ **NO sobrenatural.** No criaturas, no monstruos, no uncanny. Jugadores reales (o futbolistas ficticios realistas) en un estadio real.
- ❌ **NO body horror.** Nada de sangre, mutilación, ahogo. La peor imagen es un jugador con las manos en la cabeza mientras el rival celebra.
- ❌ **NO drones de terror ni gritos de horror** en el audio (ver § paleta SFX en INGENIERO-PAUTA + `creative-direction/audio-direction.md`).

**El "horror" de sport-choice es la HUMILLACIÓN:** fallar en el momento decisivo, perder la final, convertirte en meme, escuchar el abucheo de 67.000 personas. Es un miedo social y deportivo, intenso pero NO sobrenatural.

**Test rápido:** si una escena podría aparecer en una transmisión de la Champions o en un video de "fails de fútbol", está en tono. Si parece de una película de terror, está fuera de formato.

---

## 5. PERSONAJES — JUGADORES (likeness foto-real o ficticios)

> Se hereda de horror § 3 personajes (dyad simultánea, name labels, contraste). Lo sport-específico: los personajes son JUGADORES, no criaturas.

### Dos modos de personaje

| Modo | Qué es | Cuándo usar |
|------|--------|-------------|
| **Jugadores REALES** (likeness foto-real) | Saka, Dembélé, etc. — descriptor-based | Videos topicales (final real, fichaje, derbi del fin de semana). Máxima viralidad por relevancia. |
| **Jugadores FICTICIOS** (realistas) | Un "10" inventado, un crack de barrio | Videos no atados a un partido real. Más libertad, menos riesgo de likeness. |

### Likeness de jugadores reales = descriptor-based (REGLA CRÍTICA — riesgo CP1)

- **NUNCA poner el nombre de la celebridad literal en el prompt de imagen** (los modelos t2i no reproducen personas reales nombradas de forma confiable; intentarlo produce caras genéricas o falla).
- En su lugar, describir por **RASGOS FOTO-REALES reconocibles**: posición (extremo del Arsenal), tono de piel, corte de pelo (rapado), vello facial (barba corta / bigote), gesto característico (sonrisa amplia), y el **kit** (camiseta roja mangas blancas, dorsal 7).
- Iterar en CP1 hasta likeness aceptable. Es el riesgo de producción #1 del formato (ver INGENIERO-PAUTA § consistencia).
- **Excepción topical**: el `name_validation.is_real_invented_name` del SPEC va en `false` con `topical_real_person_exception: true`. NO aplica la regla horror de "nombres reales inventados" — acá los nombres son de personas reales públicas.

### Rol de cada jugador en el dyad

| Rol | Quién | Función |
|-----|-------|---------|
| **companero_protagonista** | El jugador del equipo de la rama PROFUNDA (el jugable) | Tu compañero. Confiar en él + acertar las jugadas paga gol + copa. PUEDE hablar on-screen (lip-sync), p.ej. pidiendo el balón / "Confía en ti, la metes" (se hereda de ref-08 Hugo que habla). |
| **foil** | El jugador del otro equipo (rama CORTA) | El "favorito obvio/fácil". Su rama es la apuesta veloz que también gana, pero NO es la jugable. Sin él, la elección del protagonista no tiene contraste. Puede tener 1-2 líneas. |

**Importante:** el foil **NO es "el malo"**. En sport-choice no hay malo aparente. El foil es simplemente el otro equipo / el camino-no-tomado. La tensión no es "uno es peligroso" sino "uno te lleva a la gloria fácil (foil) y el otro a la gloria difícil pero tuya (protagonista)".

### Consistencia de identidad (kit propio vs rival)

- El **kit del jugador elegido = tu equipo** (tu kit). Los compañeros visten tu kit; los rivales (lateral, arquero, defensores) visten el kit opuesto.
- El kit debe ser **siempre legible** en cada frame (color, mangas, dorsal). Es la señal visual que le dice al viewer quién es aliado y quién obstáculo.
- El arquero rival viste un kit distinto a ambos (regla de fútbol). Detalle técnico en INGENIERO-PAUTA § consistencia.

---

## 6. CADENA DE LÓGICA + ANTI-PATTERNS (la sección más importante)

> La lógica deportiva debe CERRAR sin huecos. Estos son los anti-patterns que YA cazamos diseñando el primer video. Violar cualquiera rompe la credibilidad futbolística → el viewer detecta el error y el formato colapsa.

### La cadena de lógica que debe cerrar

```
ELECCIÓN (jugador X)  →  EQUIPO (jugás para el equipo de X)  →  JUGADAS (3 decisiones de juego
   coherentes con esa posición/zona)  →  RESULTADO (acertar las 3 = gol & campeón; errar = la jugada
   se cae & el rival gana & sos la burla)
```

Cada eslabón debe ser explícito y coherente con el anterior. Si el viewer no puede trazar "elegí a este → soy de este equipo → estoy haciendo esta jugada → por esto gané/perdí", la lógica tiene un hueco.

### Anti-patterns deportivos (NO violar)

| # | Anti-pattern | Por qué falla | Regla |
|---|--------------|---------------|-------|
| 1 | **Pasarle el balón a un rival** | Un jugador no le pasa a alguien del kit opuesto. Rompe la lógica de equipo. | El compañero (tu kit) recibe; el rival (kit opuesto) es obstáculo. SIEMPRE. |
| 2 | **Orden hablado ≠ orden de botones** | Si el narrador dice "encaras o devuelves" pero el botón A dice "devuelves", el viewer se confunde sobre qué eligió. | El orden en que el narrador enuncia las opciones = orden de los botones (A = primera mencionada, B = segunda). |
| 3 | **Consecuencia no causalmente justificada** | "Devuelves seguro y pierdes el balón" es absurdo (un pase seguro no pierde el balón). El viewer detecta el non-sequitur. | Cada consecuencia debe seguir físicamente de la jugada. Devolver seguro = juego lento, NO pérdida; el "castigo" de la opción conservadora es perder la OPORTUNIDAD (el rival sale, la presión baja), no un error imposible. |
| 4 | **Contradicción física** | "El arquero la ataja" cuando el tiro fue afuera; "gol" cuando la mandaste al córner. | La narración + el visual + el resultado deben ser físicamente consistentes. Atajada ⇒ tiro AL arco. Gol ⇒ balón DENTRO. |
| 5 | **"B" siempre es la correcta** | Si la opción correcta es siempre la misma letra/posición, el viewer la predice y pierde la tensión. | Rotar qué opción paga: a veces la arriesgada (encarar), a veces la sensata (asistir). NO un patrón predecible A/B. La decisión debe generar DUDA real (heredado de horror § 6). |
| 6 | **Decisión sin duda real** | Si una opción es obviamente mejor, no hay dilema. | Ambas opciones deben ser defendibles ("encaro y arriesgo el gol" vs "devuelvo y mantengo posesión"). El viewer no debe tener confianza 100%. |
| 7 | **Geografía del partido confusa** | Si no se entiende dónde está el arco, quién es compañero, dónde está el balón → el viewer se pierde. | REGLA DE AMBIENTE (INGENIERO-PAUTA + image-direction): cada shot ubica POV → zona → geografía → estadio → acción. |

### Implicación para el arquitecto

Al diseñar, validá la cadena de lógica eslabón por eslabón + corré mentalmente los 7 anti-patterns sobre cada decisión y cada consecuencia. Si un eslabón no cierra o un anti-pattern aplica, reescribí ANTES de emitir el SPEC.

---

## 7. SLOTS DEL FORMATO — RESKIN DEPORTIVO

> Mapeo de los Slots A-H de horror-choice a sport-choice. Los slots de MECÁNICA (estructura, countdown, loading) se heredan. Estos son los que cambian de CONTENIDO.

| Slot horror | Slot sport-choice | Qué pueblan |
|-------------|-------------------|-------------|
| **A — Escenario** | **El estadio / el partido** | Estadio lleno (final de Champions, derbi, etc.), césped, reflectores, gradas. Atrapamiento = estás en la jugada decisiva, no podés salir. Aislamiento = la decisión es solo tuya. |
| **B — Visual del malo** | **Jugador foil** (el otro equipo) | El favorito del rival, kit opuesto. NO uncanny — identidad de equipo legible. |
| **C — Visual del bueno** | **Jugador protagonista** (tu equipo) | Tu compañero, tu kit. Contraste de color vs el foil. Puede hablar. |
| **D — Regla del malo** | **N/A → el contexto del partido** | No hay "regla del malo". El equivalente es el CONTEXTO de la jugada: estás en el minuto decisivo de la final, todo depende de cómo resuelvas. La "presión" reemplaza a la "dinámica de control del malo". |
| **E — Dilemas** | **Las 3 jugadas** | Encarar/devolver, ángulo/asistir, cruzar/picar. Tipos distintos, escalada de presión. |
| **F — Body horror** | **Fracaso deportivo + humillación social** | La jugada que se cae + abucheos/memes/burla. NO muerte. |
| **G — Cliffhanger** | **Gloria O burla + CTA** | Vuelta olímpica con la copa (acierto) / la humillación (error) + "Elige bien tu compañero. Vuelve mañana." |
| **H — Ambient creatures** | **Vida del estadio** | Banderas, bengalas, hinchas, confeti — elementos ambient vivos del estadio (opcional, subtle background). |

---

## 8. CLIFFHANGER / OUTRO (counterfactual + CTA)

> Se hereda el placement del counterfactual de horror § 13 (la rama corta del foil ES el counterfactual de apertura) + el CTA verbal final.

### El outro de sport-choice

- **Si acertaste las 3:** vuelta olímpica, levantar la orejona, confeti, el estadio estalla, tu compañero te abraza ("Te lo dije, hermano"). Tono = GLORIA cálida (LUT warm_glory).
- **El counterfactual ya se mostró al inicio** (rama corta: "si elegías al otro, ganabas fácil"). El outro NO repite un counterfactual cozy hogareño (eso es horror) — cierra con la gloria de TU camino.
- **CTA verbal:** tipo tagline, reconocible cross-video. Ej: "Elige bien a tu compañero. Y vuelve mañana." Loop al próximo video.
- **Watermark:** `@elige_tucompanero` persistente (se hereda).

---

## 9. CHECKLIST DE CALIDAD NARRATIVA (sport-choice)

Antes de aprobar un SPEC sport-choice, validar:

### Lógica deportiva (lo sport-específico)
- [ ] La elección del hook = EQUIPO, con contexto EXPLÍCITO ("si eliges a X, juegas para A")
- [ ] Rama corta (foil glorioso) + rama profunda (interactiva) — asimétricas, rama corta primero
- [ ] La rama corta NO spoilea el resultado de la rama profunda
- [ ] Las 3 decisiones son jugadas reales de fútbol, de tipos distintos
- [ ] Escalada de presión zona por zona (banda → área → mano a mano)
- [ ] Consecuencias = 100% el partido (gol/gloria O error/burla), NO muerte/horror
- [ ] La cadena de lógica cierra (elección → equipo → jugadas → resultado)
- [ ] Los 7 anti-patterns corridos sobre cada decisión/consecuencia (§ 6)
- [ ] Orden hablado = orden de botones
- [ ] "B" no es siempre la correcta; cada decisión genera duda real
- [ ] NO se le pasa el balón a un rival; consecuencias causalmente justificadas; sin contradicciones físicas

### Personajes
- [ ] Dyad simultánea con name labels GRANDES + contraste de kit
- [ ] Likeness de jugadores reales = descriptor-based (NO nombre literal en prompt)
- [ ] Kit propio vs rival legible; el elegido = tu equipo
- [ ] El protagonista puede hablar (lip-sync marcado); el foil NO es "el malo"

### Mecánica heredada (validar contra horror-choice PAUTA-MASTER)
- [ ] POV 1ª persona >80% de los shots
- [ ] Cada decisión: setup + pregunta + countdown 3-2-1 + loading bar + consecuencia A + B
- [ ] Framing acción-condicional ("Si encaras / Si devuelves"), NO bare label "Si elegiste A"
- [ ] Duración 80-100s
- [ ] Counterfactual placement + cliffhanger + CTA verbal
- [ ] Español neutral (tú/eliges), watermark `@elige_tucompanero`

### Ambiente (REGLA DE AMBIENTE)
- [ ] Cada visual_intent ubica POV → zona → geografía (arco, kits, balón, líneas) → estadio → acción
- [ ] Queda CLARÍSIMO qué pasa en el partido en cada frame

---

## 10. REGLAS DE ROTACIÓN ENTRE VIDEOS

> Se hereda el principio de rotación de horror § 17 (no repetir lo mismo en videos consecutivos). Lo sport-específico: qué dimensiones rotar.

Consultar `video-log.md` ANTES de diseñar. Rotar entre videos:

- **Liga / equipos / partido:** no repetir el mismo enfrentamiento ni la misma liga consecutivamente (Champions → Premier derby → Mundial → etc.).
- **Tipo de jugada-clave del clímax:** no terminar siempre en "mano a mano con el arquero". Rotar: penal decisivo, tiro libre, cabezazo en el último córner, definición mano a mano, etc.
- **Pattern estructural** (heredado del enum canónico choice {P1, P2, P3, P6, P9}): para satisfacer el validator. P3 (rama corta del foil = "lo fácil/seguro") es el natural para sport-choice, pero rotar cuando haya patrón.
- **Posición del POV:** extremo, delantero centro, mediapunta, lateral que sube — para variar las jugadas.

(Hasta tener ≥3 videos, la rotación se ajusta a mano. Con más videos, se derivarán reglas empíricas como en horror.)

---

## 11. CÓMO USAR ESTA PAUTA

### Flujo correcto

1. **Leer esta pauta COMPLETA** + las secciones de MECÁNICA de `horror-choice-format/PAUTA-MASTER.md`
2. **Consultar `video-log.md`** para rotación
3. **Entrevistar al user** (partido/equipos/jugadores objetivo, topical o ficticio)
4. **Diseñar la elección = equipo** + las dos ramas asimétricas
5. **Diseñar las 3 jugadas** (tipos distintos, escalada, duda real) + sus consecuencias (gol/burla)
6. **Validar la cadena de lógica + correr los 7 anti-patterns** (§ 6)
7. **Aplicar la REGLA DE AMBIENTE** a cada shot (ver INGENIERO-PAUTA + image-direction)
8. **Validar checklist § 9** antes de aprobar
9. **Codificar en CREATIVE-SPEC v11.yaml** (schema heredado de creative-director) + references_canonical[] (citadas por valor ESTRUCTURAL, ver SPEC champions)
10. **HANDOFF al ingeniero**

### Flujo INCORRECTO (errores a evitar)

- ❌ Olvidar el contexto explícito de equipo en el hook (→ incoherencia rival/compañero)
- ❌ Hacer las dos ramas simétricas o spoilear la profunda con la corta
- ❌ Tratar la lógica deportiva como empíricamente validada (es diseño en validación)
- ❌ Meter cualquier elemento de horror (muerte, monstruos, body horror)
- ❌ Violar un anti-pattern de § 6 (balón al rival, orden desalineado, consecuencia no causal, contradicción física, B siempre correcta)
- ❌ Prompts de imagen que no ubican la geografía del partido (REGLA DE AMBIENTE)

---

## 12. RELACIÓN CON OTROS DOCUMENTOS

### Esta pauta HEREDA (no re-litiga)

- ✓ `horror-choice-format/PAUTA-MASTER.md` — la MECÁNICA del formato choice (estructura temporal, hook dyad, decisiones, framing condicional, counterfactual, POV, lenguaje). Autoridad empírica de la mecánica.
- ✓ `ai-video-production/` — el pipeline técnico universal (TTS, image, SFX, motion, captions, render, QA, HYBRID per-clip atomic, MODEL-CAPABILITIES-MATRIX, 8 gates).
- ✓ `creative-director/` + templates — el schema CREATIVE-SPEC v11 + el workflow de handoff arq↔ing↔auditor.

### Esta pauta APORTA (lo sport-específico)

- ✓ La lógica deportiva (elección=equipo, ramas asimétricas, decisiones=jugadas, consecuencias=gol/burla)
- ✓ Los anti-patterns deportivos (§ 6)
- ✓ La paleta SFX fútbol (vía INGENIERO-PAUTA + audio-direction)
- ✓ La REGLA DE AMBIENTE (vía INGENIERO-PAUTA + image-direction)

### Esta pauta NO toca

- Decisiones técnicas (LUFS, CSS, ffmpeg, voice IDs, pace WPM exacto) — son del ingeniero (INGENIERO-PAUTA-MASTER)
- Operacionales (image-direction, audio-direction, ui-elements) — son el "cómo" en creative-direction/

---

## 13. ESTADO + PRÓXIMOS PASOS

- **Versión:** v0.1 (pre-empírico, fase de validación)
- **Primer video:** `champions-sport-choice` (Dembélé/Saka, final Champions) — SPEC validado, pending ship
- **Para promover a v1.0 empírico:** shippear ≥3 videos sport-choice + derivar canonical-scenes propios (igual que horror se derivó de 8 virales) + loguear cada hallazgo en `video-log.md`. Cuando la lógica deportiva tenga patrón observado (no solo diseño), actualizar esta pauta con compliance N/n.
