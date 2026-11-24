# PAUTA-MASTER.md — Pauta del formato "Sport-Choice" (drama deportivo interactivo)

> **AUTORIDAD CREATIVA del formato sport-choice** (rol 🏛️ ARQUITECTO). Define la HISTORIA/LÓGICA del formato.
>
> **Versión:** **v0.2** (operativa) — el DISEÑO sigue siendo el de v0 (dos recorridos completos + asimetría por favorito + compuertas 2-3 + catálogo de fracaso + fallo-de-jugador + narración-no-juzga + política A/B); v0.2 le AGREGA la capa operativa (§10.A guion beat-a-beat, §10.B catálogo de jugadas-compuerta por posición, §10.C plantilla de cadena causal) sin re-litigar nada del diseño. Sigue siendo **pre-empírico** (0 videos shipped). Consolida el diseño derivado de:
> - la sesión de diseño con Tomás (2026-05-31 / 06-01) + el upgrade "PAUTA potente" aprobado tras el fail del topical champions,
> - `BRIEF-TEMPLATE-DEPORTES-v0` (input de ideas de Tomás),
> - `creative-director/master-flow-v2/SYSTEM-LEARNINGS-V3-V4-COMPILATION.md` (learnings del sistema).
>
> ⚠️ La estructura DEPRECADA "rama corta del foil = counterfactual opening fijo que spoileaba" (la vieja v0.1) NO es el diseño: el orden de los dos recorridos es 🟩 VARIABILIDAD (§4 + §10.A), no un opening fijo.
>
> ⚠️ **Pre-empírico**: sport-choice NO tiene referentes virales propios todavía. La MECÁNICA choice se hereda de **`../choice-format-core/`** (agnóstica, derivada de los 8 virales horror — sport y horror son HERMANOS que heredan del core, ya NO hermano-de-hermano); la LÓGICA deportiva es **diseño en validación** — se valida con nuestros primeros videos y se loguea en `video-log.md`.

---

## §0 — METODOLOGÍA + ESTADO

### De dónde vienen estas reglas

| Capa | Fuente | Validación |
|------|--------|------------|
| **MECÁNICA choice** (estructura temporal, countdown, loading, botones A/B, framing acción-condicional, POV >80%, 2ª persona presente) | `../choice-format-core/CHOICE-MECHANIC.md` (agnóstico, derivado de los 8 virales) | ✅ VALIDADO — se HEREDA |
| **LÓGICA deportiva** (elección=compañero, dos recorridos, asimetría por favorito, decisiones=jugadas, catálogo de fracaso, fallo-de-jugador, narración-no-juzga, identidad real-topical) | diseño Tomás+arquitecto + brief deportes + SYSTEM-LEARNINGS | 🟡 DISEÑO (pre-empírico) — se valida con nuestros videos |

### Marco de lectura (Pattern 8 — anti reglas binarias)

Toda elección creativa se expresa como **🟦 PRINCIPIO (mandatorio) / 🟩 VARIABILIDAD (libre) / 🟥 ANTI-PATTERN (evitar)**, NUNCA como regla binaria. Si algo acá suena a "regla rígida" sobre una elección creativa, es un bug de framing.

### BAN (no hacer)
- ❌ Tratar la lógica deportiva como "empíricamente validada" antes de tener videos shipped.
- ❌ Cualquier elemento de horror (muerte, body horror, monstruos, drones de terror, gritos de horror) — sport-choice es drama deportivo, no terror.
- ❌ Inventar reglas mid-conversación que contradigan esta pauta o la mecánica heredada — si un caso lo justifica, escalar a Tomás.

---

## §1 — NORTE DE PRODUCCIÓN: la máquina partido → reel

> **Meta del formato: 1 reel viral por partido (topical — Mundial como primera ola).**

El formato es una **máquina topical data-driven**:

```
INPUT = un partido real  →  los 2 cracks marquee (uno por equipo) + el favorito (cuotas/forma)
                          ↓
PROCESO = dyad de los 2 cracks + asimetría según el favorito + jugadas del catálogo + narración play-by-play
                          ↓
OUTPUT = 1 reel (~86-100s)
```

- **Automatable + escalable = obligatorio** (no se artesanan 64 partidos). La **FASE 0 es mayormente DATA-PULLED** (equipos, cracks, kits, favorito) más que diseño a mano.
- **Cadencia alta** durante el Mundial → el pipeline tiene que estar aceitado.

### 🟦 Default vs override (regla operativa)
- Cuando Tomás dice genéricamente **"haz un video de sport-choice"** → se aplican los **defaults data-driven** de esta pauta (dyad = los 2 cracks del partido, asimetría = el favorito, etc.).
- Cuando Tomás da **inputs específicos** para un video (otro cruce, otra jugada-clave, otra política A/B, etc.) → **esos inputs OVERRIDEAN** los defaults. La pauta es el piso, no la jaula.

---

## §2 — FILOSOFÍA + LA REGLA #1

- **Adjetivos rectores (todo video):** dinámico · divertido · polémico · que haga sentido.
- **Pilares (carry-forward del sistema):** agnóstico · automatizable · escalable · sólido.
- El formato es **generador, no límite**: la mecánica choice es fija; la creatividad vive en QUÉ la puebla.

### 🟦 LA REGLA #1 — EXECUTION CONTINUITY

El factor X del TASTE-LOG (Tomás da 10/10 a los backrooms y 7.9 a lo nuestro): la diferencia NO es atmósfera ni sonido — es **continuidad física shot-a-shot (no teleporte)**. El fútbol es continuo-motriz → **cada recorrido se vive como UN plano continuo** (POV avanzando por la cancha). El corte entre recorrido 1 y 2 es un **pivote limpio a propósito**; jamás teleporte dentro de un recorrido. Esta regla manda sobre todo lo demás.

---

## §3 — LA ELECCIÓN = TU COMPAÑERO (= tu equipo)

- 🟦 **POV = sos un jugador anónimo del equipo** (cara nunca visible — manos / botas / mangas). El elegido (la estrella real) es tu **compañero**: le pasás y él define (gol) o falla.
- 🟦 **Dyad = dos estrellas REALES, una por equipo** (rivales). Elegís una → es tu compañero + jugás para su equipo; la otra (y su kit) = rival.
- 🟦 **Contexto explícito ANTES del countdown** (el viewer sabe qué elige antes de que corra el reloj — hereda horror GAP#15/#16).
- 🟦 **Likeness real = descriptor-based aproximada** (los modelos t2i no clonan nombrados; kit/dorsal/posición/build son la firma legible).
- 🟦 **POV ficticio = seguridad gratis**: como vos (POV) no sos una persona real, los **fallos pueden caer en VOS** sin riesgo legal. El único riesgo es mostrar a la estrella real fallando (→ política A/B, §9).

---

## §4 — ESTRUCTURA: DOS RECORRIDOS + ASIMETRÍA POR FAVORITO

### Dos recorridos completos (la innovación estructural)

Un video muestra **los DOS recorridos completos, uno y luego el otro** (= el counterfactual; ves las dos elecciones). Cada recorrido = el viaje POV continuo de un compañero/equipo, con sus compuertas y su desenlace.

- 🟩 **El orden varía por video** (corto→largo o largo→corto).
- 🟦 **El resultado siempre se muestra** (por ahora; sin cliffhanger que oculte el desenlace).
- 🟦 **La cancha es la línea de tiempo**: mediocampo → banda → borde del área → mano a mano (travel continuo, anti-teleporte §2).

### 🟦 Asimetría = el FAVORITO del partido (data-driven)

| | |
|---|---|
| **Input** | el partido real + quién es **favorito** (cuotas/forma, scrapeado de internet) |
| **Favorito → su recorrido** | **MENOS compuertas** (~2) → la gloria está más cerca, mayor prob. de ganar |
| **No-favorito → su recorrido** | **MÁS compuertas** (~3) → más difícil, más chances de fallar |
| **El gap escala con las cuotas** | partido parejo → 2 vs 3 · favoritazo → la asimetría grande se expresa en el counterfactual + intensidad de shots (el played path se mantiene 2-3) |
| 🟦 **Invisible como editorial** | NO se dice "este es el fácil" — se **deriva de la realidad** → hace sentido + automatable |
| 🟩 **Knob de batacazo** | se puede invertir (underdog más fácil) para narrativa de upset (raro) |

### 🟦 Tagging canónico — cómo mapea al guard estructural

> Para que el guard `ai-video audit-spec-structure-vs-canonical` enforce el invariante (foil fuera del played path), cada video taguea sus `section_id` así:

- **Recorrido JUGADO** (el del jugador que elegís = protagonista) → `setup_pre_decision` → `decision_N` → `consequence_*` (= el played path; sus compuertas son las que cuenta el guard).
- **Recorrido del FOIL** (el contraste, el camino no-elegido) → `counterfactual_*` (opening o final). La **estrella foil** aparece SOLO acá + en `hook` + `cliffhanger`. **NUNCA en el played path.**
- 🟥 **En el played path, el rival es KIT / NPC genérico** (anchor de rival genérico), **NO el anchor de la estrella foil.** Reusar el anchor del foil para los rivales del played path es exactamente lo que **FALLA** el SPEC champions (shots 05/06/07/12/17/19) → usar un anchor `rival_npc` aparte para los obstáculos.
- **Compuertas del recorrido jugado = 2-3** (banda canónica; favorito 2 / no-favorito 3). El guard **FLAGea** >3.

---

## §5 — LAS DECISIONES = JUGADAS (compuertas)

- 🟩 **Compuertas del recorrido jugado (played path):** 2 (favorito) a 3 (no-favorito) — banda canónica; el guard `ai-video audit-spec-structure-vs-canonical` flagea >3. El recorrido del foil = `counterfactual_*` (ver §4 tagging).
- 🟦 **✓ = avanza** (sigue el plano hacia el arco) · **✗ = perdés la jugada Y el partido** (inserto corto dead-end; luego el video sigue por el camino correcto).
- 🟩 **Tipos distintos** por compuerta (regate/encare, pase/visión, definición), presión escalando zona por zona.
- 🟥 **"B" no siempre correcta** — rotar qué opción paga.
- 🟦 **Duda real:** ambas opciones defendibles (si una es obvia, no hay dilema).
- 🟩 **Ratio debatible:** ~1 de cada 3-4 decisiones deliberadamente debatible (fuel de comentarios).

---

## §6 — CONSECUENCIAS: CATÁLOGO ROTADO (Capa C)

> 🟥 El fracaso NO es siempre "contra → gol rival" (repetitivo + implausible a esa frecuencia). Rotar del catálogo:

| Modo de fracaso | Registro | Regla |
|---|---|---|
| Robo / pérdida directa | neutro | — |
| Bloqueo / despeje | neutro | — |
| Atajada sin gol | tenso | — |
| Offside / gol anulado | polémico | — |
| Papelón / blooper propio | divertido/meme | 🟦 **≥1 por video** (lo más compartible) |
| Falta / amarilla | neutro | — |
| **Fallo-de-jugador** (§7) | injusto/polémico | calibrado — no cada pase |
| Contra → gol rival | alto stakes | 🟦 **reservado al clímax**, no cada error |

🟦 **Rotación:** no repetir el mismo modo 2 veces seguidas · contra→gol solo clímax · ≥1 papelón por video.

---

## §7 — FALLO-DE-JUGADOR (el motor de polémica)

- Elegís la jugada **correcta** (le das al desmarcado) pero el resultado depende de **a quién**: el receptor define… o **la pierde**. Cuenta como derrota **aunque la decisión fue correcta** = injusto-frustrante **deliberado**.
- 🟩 **Señalización (knob):** algunos señalizados (el receptor viene frío → confirma la bronca), otros blindside (rage puro). Mezcla, lean señalizado temprano.
- 🟦 **Calibración:** modo **raro**, NO default — si pasa seguido, el viewer aprende "nunca pases" y muere la mecánica de pase.
- ⚠️ **Quién falla lo define la política A/B (§9):** por default el receptor que falla es VOS o un compañero genérico (A). La estrella nombrada solo falla en modo B.

---

## §8 — NARRACIÓN: narra la consecuencia, NUNCA juzga (Capa C)

- 🟦 **Relator play-by-play vivo, neutral de juicio.** Mete al viewer en la jugada; **el juicio lo pone el comentario del usuario** (polémica orgánica).
- 🟦 **EL GOL SE GRITA** (directiva creator 2026-06-04): en el momento del gol, el relator GRITA el "¡Gooool!" (la firma del relator latinoamericano) y el ESTADIO explota con él (SFX explosión de celebración en banda alta 0.55-0.65 — ver INGENIERO-PAUTA § 2/audio-direction). Neutral-de-juicio aplica al JUICIO sobre el jugador, NO a la emoción del gol: la épica del gol ES del relator. El estiramiento del grito se modera para que el TTS no glitchee ("¡Gooool!" con 3-4 oes, no "GOOOOOOOL" en caps interminable — caso audición 2026-06-03).
- ✅ *"Uy… se la diste al lateral, enganchó y la perdió. Salen de contra. Gol."*
- 🟥 *"Ese jugador es malo, perdiste el partido."* (editorializa = prohibido)
- 🟦 **Español neutral** (tú/eliges/decides), 2ª persona presente, oraciones cortas y claras. NUNCA voseo. La épica emerge del visual + rugido + música, no de la narración.

---

## §9 — IDENTIDAD REAL-TOPICAL + POLÍTICA DE RIESGO A/B

- **Real topical**: estrellas reales, partido real, Mundial. Likeness descriptor-based aproximada (no deepfake).
- 🟦 **DEFAULT A:** la estrella nombrada queda en la **GLORIA**; el fallo cae en **VOS (POV)** o en un **compañero genérico** (*"le diste al lateral y la perdió"*). Real + topical + seguro + escalable. (POV ficticio lo hace gratis, §3.)
- 🟧 **B SELECTIVO (solo primeros videos, dosificado):** la estrella nombrada **puede fallar** para boost de viralidad temprana (montarse en la ola Mundial). Es la **línea roja** del brief §4 (derechos de imagen + portrayal negativo + synthetic-media policy IG/TikTok) → **riesgo asumido conscientemente, declarado por video en el SPEC (`risk_policy: A|B`) + logueado en `video-log.md`.** No es default; se apaga al escalar.

---

## §10 — CADENA DE LÓGICA + ANTI-PATTERNS (la sección más importante)

**Cadena que debe cerrar:** elegís compañero → jugás para su equipo → 2-4 jugadas coherentes con la zona → resultado (acertás → gol/campeón; errás → la jugada se cae, rotando el catálogo §6).

| 🟥 Anti-pattern | Regla |
|---|---|
| Pasarle al rival | tu kit recibe; el kit opuesto es obstáculo. SIEMPRE |
| Orden hablado ≠ botones | A = primera opción nombrada |
| Consecuencia no causal | un pase seguro NO "pierde el balón" — la opción conservadora castiga perdiendo la CHANCE, no con un error imposible |
| Contradicción física | atajada ⇒ tiro al arco · gol ⇒ balón adentro |
| Geografía confusa | **REGLA DE AMBIENTE** (POV→zona→geografía→estadio→acción) por shot — ver INGENIERO-PAUTA |
| Mismo fracaso repetido | rotar catálogo §6 |
| Fallo-de-jugador en cada pase | calibrar raro §7 |
| Decisión sin duda real | ambas opciones defendibles §5 |

**Implicación para el arquitecto:** validá la cadena eslabón por eslabón + corré los anti-patterns sobre cada decisión y consecuencia ANTES de emitir el SPEC.

---

## §10.A — GUION BEAT-A-BEAT: el timeline de diseño 0→~90s (dos recorridos)

> ⚠️ **Esto es la CAPA OPERATIVA de la estructura §4, no una re-litigación.** La estructura (dos recorridos completos + asimetría por favorito) ya está fijada en §4. Acá se baja a una **línea de tiempo de diseño pre-empírica** que el arquitecto usa como plantilla. La **mecánica temporal agnóstica** (hook dyad + countdown + loading bar + decisión→consecuencia + counterfactual placement + cliffhanger/CTA) NO se duplica — vive en `../choice-format-core/CHOICE-MECHANIC.md §2` + su técnica de UI en `../choice-format-core/INGENIERO-CHOICE-CORE.md`. Acá solo el SABOR sport sobre ese esqueleto.

### El timeline de diseño (🟩 bandas % pre-empíricas — NO números rígidos canónicos)

> 🟩 **Las bandas % de abajo son un PUNTO DE PARTIDA de diseño, NO mediciones.** sport-choice tiene 0 videos shipped → ningún % acá está validado empíricamente. Tratalos como guía de proporción, no como ley. Se ajustan con cada video logueado en `video-log.md`. La duración total (~86-100s) sí está acotada por la mecánica heredada (`../choice-format-core/CHOICE-MECHANIC.md §2`).

```
0%──────── HOOK / DYAD ────────15%
  POV en el círculo central frente a los DOS cracks (uno por equipo), name labels GRANDES,
  kits contrastantes, contexto de equipo EXPLÍCITO (caption "[A]=[EQUIPO_A] · [B]=[EQUIPO_B]"),
  countdown 3-2-1 al cierre del hook. 🟦 0 cuts en el hook (un plano continuo — core).

15%──── RECORRIDO 1 (completo) ────~50%
  El viaje POV continuo de un compañero/equipo: setup → compuerta(s) (2-3 según favorito §4)
  → desenlace de ESE recorrido (gol&gloria O fracaso del catálogo §6). La cancha = la línea de
  tiempo (mediocampo → banda → borde del área → mano a mano). 🟦 anti-teleporte: continuidad
  física shot-a-shot dentro del recorrido (REGLA #1 §2).

~50%───────── PIVOTE ─────────~55%
  El ÚNICO corte no-continuo permitido (ver abajo). Marca el pasaje del recorrido 1 al 2.

~55%──── RECORRIDO 2 (completo) ────~92%
  El otro compañero/equipo: su setup → sus compuertas → su desenlace. Mismo tratamiento
  continuo intra-recorrido. El contraste entre los dos desenlaces ES el counterfactual (§11).

92%──────── OUTRO / CTA ────────100%
  Resolución visible de ambos recorridos ya mostrada; cierre con tagline loop + watermark (§11).
```

### 🟦 Dónde caen las compuertas en la línea de tiempo

- Cada **compuerta** = un micro-evento editorial (setup de la jugada → pregunta → countdown 3-2-1 + botones A/B + loading bar → consecuencia ✗ dead-end / ✓ avanza). El pacing técnico de ese micro-evento es agnóstico → `../choice-format-core/INGENIERO-CHOICE-CORE.md §1`.
- Las compuertas se distribuyen **a lo largo del recorrido**, escalando con la zona del campo (la cancha es la línea de tiempo §4): compuerta temprana en zona de creación (mediocampo/banda), compuerta tardía en zona de definición (borde del área / mano a mano). 🟩 La posición exacta de cada compuerta dentro del recorrido es variabilidad de diseño.
- **Cuántas:** 2 (favorito) a 3 (no-favorito) **por recorrido jugado** — banda §4/§5; el guard `ai-video audit-spec-structure-vs-canonical` flagea >3.

### 🟦 El PIVOTE — el único corte no-continuo permitido

- Dentro de cada recorrido manda **EXECUTION CONTINUITY** (§2): el recorrido se vive como UN plano continuo, jamás teleporte shot-a-shot.
- El **pivote entre recorrido 1 y recorrido 2 es la excepción a propósito**: un corte limpio y marcado que dice "ahora ves la OTRA elección". No es un teleporte (que rompe inmersión dentro de un recorrido) — es un cambio de hipótesis explícito.
- 🟦 **Cómo se marca el pivote** (que el viewer entienda que cambió de recorrido, no que "se teletransportó"): un cue explícito de transición de rama (heredado — `../choice-format-core/CHOICE-MECHANIC.md §4` "transición narrativa explícita entre ramas"). 🟦 **La narración de apertura del recorrido del foil SIEMPRE abre con "Si eliges a [estrella foil]…"** (regla del creator 2026-06-04 — framing condicional de elección, simétrico al "Eliges a [estrella]" de la rama jugada). Acompañado 🟩 de reset visual claro (círculo central con las mangas del otro kit) y/o caption-puente. Lo que importa (🟦 PRINCIPIO): el viewer NUNCA queda confundido sobre en qué recorrido está.
- 🟥 **ANTI-PATTERN:** cortar entre shots DENTRO de un recorrido como si fuera un pivote (eso es el teleporte que mató la inmersión — ver §14 learnings) · o pasar de recorrido 1 a 2 SIN marcar el pivote (el viewer cree que es la misma jugada y se pierde).

### 🟩 Orden de los recorridos (variabilidad — NO un opening fijo)

- 🟩 El recorrido del FOIL (tagueado `counterfactual_*`, §4) puede ir **al inicio O al final** del video — los dos órdenes son válidos (corto→largo o largo→corto). NO es un "counterfactual opening fijo".
- 🟦 Lo que NO varía: los dos recorridos son **SECUENCIALES, jamás interleaved** (no cortar de uno a otro beat-a-beat — eso colapsa la inmersión continua de cada uno). El foil NUNCA aparece en el played path (§4 tagging).
- ⤴ El **emotional framing** del counterfactual (stakes_lift si va antes / relief_contrast si va después) es mecánica agnóstica → `../choice-format-core/CHOICE-MECHANIC.md §6`.

---

## §10.B — CATÁLOGO DE JUGADAS-COMPUERTA POR POSICIÓN POV

> Las compuertas (§5) son jugadas reales. **Qué jugadas tienen sentido depende de la posición del POV** (extremo / 9 / mediapunta / lateral / arquero). Este catálogo da, por posición, jugadas-compuerta con sus opciones A/B y la zona del campo a la que pertenecen — para que el arquitecto arme recorridos coherentes con la posición y para que la rotación del `video-log.md` (jugada-clave + posición POV) tenga de dónde elegir.
>
> 🟩 **Todo este catálogo es VARIABILIDAD de diseño pre-empírica.** No es una lista cerrada ni "canónica" — es un menú de arranque. El arquitecto puede inventar otras jugadas-compuerta que respeten la cadena causal (§10.C) + la duda real (§5). 🟦 Lo único mandatorio: **ambas opciones A/B defendibles** (duda real §5) + **consecuencia causal** (§10) + la jugada CABE en la zona declarada.

### Extremo (banda → recorte → borde del área)

| Jugada-compuerta | Zona | Opción A | Opción B | Por qué hay duda real |
|------------------|------|----------|----------|------------------------|
| Encarar al lateral | Banda | Encarar (1v1) | Devolver y reciclar | encarar arriesga perder el balón; devolver enfría la chance |
| Salida de banda | Banda / línea de fondo | Tirar el centro raso atrás | Buscar el palo corto tú mismo | centro = depende del rematador; palo corto = ángulo muy cerrado |
| Recorte hacia adentro | Borde del área | Recortar y sacar el zurdazo | Tocar al que llega de frente | el zurdazo lo bloquea el defensor; el toque depende del timing del compañero |
| Diagonal interior | Entrelíneas | Pisarla y esperar el desborde | Pase de primera al hueco | esperar te cierra el espacio; primera es alto riesgo de imprecisión |

### Delantero centro (9) — espaldas al arco / área

| Jugada-compuerta | Zona | Opción A | Opción B | Por qué hay duda real |
|------------------|------|----------|----------|------------------------|
| Pivot de espaldas | Borde del área | Aguantar y descargar al que llega | Girar sobre el central | descargar cede la definición; girar arriesga perder la marca |
| Desmarque | Línea de último defensor | Romper al primer palo | Quedarte en el punto de penal | primer palo = anticipas pero ángulo cerrado; punto penal = más tiempo pero te puede ganar el central |
| Definición mano a mano | Mano a mano | Cruzarla al palo lejano | Picarla / definir por abajo | cruzada = el arquero llega con la mano; picada = riesgo de que la lea |
| Cabezazo en el centro | Área, salto | Cabecear al primer palo | Peinarla al segundo | primer palo = reflejo del arquero; segundo = depende de que llegue alguien |

### Mediapunta (10) — creación entre líneas

| Jugada-compuerta | Zona | Opción A | Opción B | Por qué hay duda real |
|------------------|------|----------|----------|------------------------|
| Última pausa | Entrelíneas, frente al área | Filtrar el pase entre centrales | Abrir a la banda para el desborde | filtrado = altísimo riesgo/recompensa; abrir = más seguro pero ralentiza |
| Llegada desde atrás | Borde del área | Rematar de primera el rebote | Pararla y acomodártela | primera = puede salir desviada; pararla = te llega la marca |
| Tiro libre frontal | Frontal del área | Pegarle directo al ángulo | Tocarla en corto y combinar | directo = la barrera y el ángulo; corto = pierde el factor sorpresa |
| Enganche en tres cuartos | Tres cuartos | Enganchar hacia el centro | Soltarla rápido al pivote | enganchar te expone al doblaje; soltar baja la temperatura |

### Lateral que sube (carrilero)

| Jugada-compuerta | Zona | Opción A | Opción B | Por qué hay duda real |
|------------------|------|----------|----------|------------------------|
| Superposición | Banda, sobrepaso | Pedirla por fuera y desbordar | Quedarte de apoyo y recargar | desbordar = expone la espalda a la contra; apoyo = renuncia a la chance |
| Centro desde el fondo | Línea de fondo | Centro al área pasado | Centro raso al primer palo | pasado = depende del cabeceador; raso = lo corta el primer defensor |
| Cierre vs proyección | Medio campo | Subir al ataque | Quedarte por si hay contra | subir = riesgo de quedar mal parado; quedarte = un atacante menos |

### Arquero (POV del que ataja — para climaxes defensivos)

| Jugada-compuerta | Zona | Opción A | Opción B | Por qué hay duda real |
|------------------|------|----------|----------|------------------------|
| Penal decisivo | Punto de penal | Tirarte a tu palo fuerte | Quedarte en el medio / esperar | adivinar el palo = riesgo puro; esperar = solo te salva si la pican al centro |
| Uno contra uno (achique) | Borde del área chica | Salir a achicar el ángulo | Esperar parado el remate | salir = te la pueden picar; esperar = le das todo el arco |
| Córner / centro | Área chica | Salir a descolgar el centro | Quedarte en la línea | salir = riesgo de no llegar; quedarte = dejas el cabezazo libre |

> 🟦 **Cada recorrido usa jugadas de TIPOS distintos** (§5): no tres encares seguidos. Combiná creación + pase + definición escalando la zona. La **posición POV se rota entre videos** (§12 + `video-log.md`) para variar el tipo de jugadas y evitar feed predecible.

---

## §10.C — PLANTILLA DE CADENA CAUSAL (checklist pre-SPEC)

> ⛔ **El arquitecto corre esta plantilla por video ANTES de emitir el SPEC** (es la bajada operativa de la cadena de §10 + la self-validation de HR#27). Cada eslabón debe cerrar; si uno no cierra, el SPEC NO sale. Complementa (no reemplaza) los validators estructurales que el arquitecto corre pre-emit (`ai-video audit-spec-structure-vs-canonical` + `ai-video audit-spec-narrative-coherence`) + el `NO-HORROR-GUARD.md`.

**Eslabón por eslabón (marcá cada uno por recorrido):**

1. **[ ] ELECCIÓN → EQUIPO.** El hook presenta el dyad con contexto EXPLÍCITO de equipo (caption + narración). Elegir un crack = jugar para su equipo (§3). Sin esto, colapsa el concepto rival/compañero.
2. **[ ] EQUIPO → KIT (firma de identidad).** Tu kit recibe; el kit opuesto obstaculiza; el arquero rival viste un kit DISTINTO a ambos (§10 anti-pattern "pasarle al rival" + INGENIERO-PAUTA §3). Verificá que cada compuerta respete esto: el receptor de tu pase es de TU kit, el obstáculo es del kit rival.
3. **[ ] COMPUERTA 1..N coherentes con la ZONA.** Cada compuerta es una jugada que tiene sentido en la zona del campo donde cae (§10.B + la cancha = línea de tiempo §4). Una definición no va en mediocampo; un encare de banda no va en el área chica.
4. **[ ] Cada compuerta = duda real.** Ambas opciones A/B defendibles (§5). Si una es obvia, no hay dilema → rediseñar.
5. **[ ] Tipos de compuerta distintos + escalada de zona.** No repetir el mismo tipo de jugada (§5). La presión escala mediocampo → área → definición.
6. **[ ] Orden hablado = orden de botones.** A = primera opción nombrada en la narración (§10 anti-pattern + core §3).
7. **[ ] Cada CONSECUENCIA causalmente justificada (§10).** Una opción conservadora castiga perdiendo la CHANCE (la jugada se enfría, baja la presión), NO con un error físicamente imposible (un pase seguro no "pierde el balón"). Sin contradicción física (atajada ⇒ tiro al arco; gol ⇒ balón adentro).
8. **[ ] Modo de fracaso del catálogo §6, rotado.** No el mismo modo 2 veces seguidas; contra→gol solo en el clímax; ≥1 papelón por video.
9. **[ ] Fallo-de-jugador calibrado (§7).** Si se usa, es raro (no en cada pase) + respeta la política A/B (§9) sobre quién falla.
10. **[ ] DESENLACE coherente con el recorrido.** Acertar la cadena → gol/campeón; errar → la jugada se cae rotando el catálogo. El recorrido del foil (`counterfactual_*`) cierra su propio desenlace; el foil NUNCA aparece en el played path (§4 tagging).
11. **[ ] Narración narra-no-juzga (§8)** + español neutral + 2ª persona presente.
12. **[ ] Cadena entera cerrada por AMBOS recorridos.** Correr 1-11 sobre el recorrido jugado Y el del foil.

> 🟦 Si cualquier eslabón no cierra → **iterar el diseño ANTES del SPEC** (no emitir con un eslabón roto). Esto es la self-validation pre-emit de HR#27 aplicada a la lógica deportiva.

---

## §10.D — REGLAS DEL MOMENTO DE DECISIÓN: lógica espacial + posesión (directivas del creator 2026-06-04, post primer draft)

> El sentido del formato vive en que el viewer SIENTA que decide. Tres reglas 🟦 NO negociables que gobiernan compuertas y consecuencias:

### 🟦 R1 — LÓGICA ESPACIAL (continuidad de punto de vista)
El POV está UBICADO en un punto concreto del campo cuando se le hace la pregunta. **Las consecuencias salen DESDE ese mismo punto** (o en continuidad física evidente con él). Si decidiste en la banda, el desenlace se ve desde la banda — jamás "apareces fuera de la cancha" viendo el desenlace desde otro lado. Cada `visual_intent` de consecuencia DEBE heredar el encuadre/posición del shot de decisión que la causó. (Caso disparador: shot_07 del draft #2 — el viewer se veía fuera de la cancha tras decidir dentro del área.)

### 🟦 R2 — EL BALÓN ESPERA LA DECISIÓN (posesión en compuerta)
En el clip de una compuerta, **el balón está EN POSESIÓN del POV** (al pie, enfrente, o viniendo hacia él en el aire) y **NINGUNA acción del balón se resuelve hasta que el usuario decide**. El clip de compuerta = **cámara lenta / tensión sostenida**: los demás jugadores PUEDEN moverse (el entorno respira: rivales presionando, compañeros desmarcándose, multitud), pero el balón no inicia su acción. "Que haga sentido que aún podemos decidir porque TENEMOS el balón." (Casos disparadores: shots 05/13/15 del draft #2 — el balón avanzaba al arco o la acción se resolvía antes de la decisión.)

### 🟦 R3 — LA CÁMARA SIGUE LO DECIDIDO (consecuencia direccional)
La consecuencia CONTINÚA desde el encuadre congelado de la decisión y **la cámara/acción se mueve EN LA DIRECCIÓN de lo que se decidió** (elegiste descargar a la derecha → la jugada sale hacia la derecha desde tu punto). El viewer percibe: "yo decidí y el mundo se movió hacia donde decidí".

**Implicación arquitecto (pre-SPEC):** por cada compuerta, declarar la POSICIÓN espacial exacta del POV + verificar que sus 2 consecuencias arrancan desde esa posición y se mueven en la dirección de la opción (sumar al checklist §10.C eslabones 3 y 7). **Implicación ingeniero:** traducción a prompts de imagen/motion en `INGENIERO-PAUTA-MASTER § 1.5`.

---

## §11 — OUTRO / CTA

- El **contraste entre los dos recorridos** ES el counterfactual (ves las dos elecciones).
- 🟦 **CTA de PARTIDO (default para topicales pre-match — regla del creator 2026-06-04):** el outro pregunta la PREDICCIÓN del partido real: *"Viste los dos finales. ¿Quién gana? ¿[Equipo A] o [Equipo B]? Deja tu resultado en los comentarios."* + botones A/B con los EQUIPOS (Y75/Y82) + pregunta on-screen Y62. El comentario-predicción es el fuel de engagement (tribalismo + re-watch post-partido para ver quién acertó). La identidad de marca queda en el watermark.
- 🟩 **CTA loop de marca** (*"Elige bien a tu compañero. Y vuelve mañana."*) — variante para videos NO atados a un partido con resultado pendiente.
- 🟦 Watermark `@elige_tucompanero` persistente en todos los casos.

---

## §12 — ROTACIÓN ENTRE VIDEOS

Consultar `video-log.md` ANTES de diseñar. Rotar: **liga/equipos** (no repetir cruce ni liga consecutiva) · **jugada-clave del clímax** (no siempre mano a mano) · **posición del POV** · **modo de fracaso destacado** (§6) · **política A/B** (§9). Hasta ≥3 videos, rotación a mano.

---

## §13 — LO QUE SE HEREDA (todo lo NO sport-específico)

> ⛔ **REGLA EXPLÍCITA (Tomás 2026-06-01):** todo lo que NO es lógica deportiva sport-específica **se construye EXACTAMENTE como un video de horror-choice**. NO se reinventa.

| Tema | De dónde se hereda |
|------|--------------------|
| **Códigos / scripts de edición** (build_clip_atomic, cp*.py, effects, captions, etc.) | `ai-video-production/templates/` (Capa A) |
| **Comunicación entre agentes** (arquitecto / ingeniero / auditor, handoffs `CP[N]-handoff.md`) | `creative-director/master-flow-v2/` + `AUDITOR-PROTOCOL.md` + `HANDOFF-PROTOCOL.md` |
| **Pipeline CP0 → CP5** + gates obligatorios por CP | `master-flow-v2` + docs/OPERATING-MANUAL.md |
| **8 gates pre-render** + dual quality bar + **Gemini QA** (audit-frames, audit-gemini-calibrated, audit-audio, continuity) | docs/OPERATING-MANUAL.md § Pre-render gate |
| **Ensamblado HYBRID per-clip atomic** + captions Whisper word-timed (HR#3/#25/#30) | `PIPELINE.md §13` |
| **MODEL-CAPABILITIES** (clip_max, pace WPM, constraints Gemini) HR#28/#29 | `ai-video-production/MODEL-CAPABILITIES-MATRIX.md` |
| **Cost cap 25%** sobre último video exitoso · **TDD** (HR#26) · medir-no-estimar | SYSTEM-LEARNINGS-V3-V4 |
| **Mecánica choice** (countdown 1s/dígito, loading bar, botones A/B, framing acción-condicional, POV >80%) | `choice-format-core/CHOICE-MECHANIC.md` (creativa) + `choice-format-core/INGENIERO-CHOICE-CORE.md` (técnica choice-UI) — agnóstico, derivado de los 8 virales vía horror |

---

## §14 — PENDIENTES + RELACIÓN CON DOCS + ESTADO

### Deliverables Capa B/C que siguen a esta pauta
- `VISUAL-STYLE.md` deportes (look cálido/saturado/brillante + preset CSS — OPUESTO al lúgubre `saturate .35/brightness .74` de horror).
- SPEC template deportes v1 (hereda schema v11; campos sport: `risk_policy`, `favorite`, `recorridos[]`, `compuertas`).
- `SCRIPT-WRITING-GUIDE.md` update (alinear a dos-recorridos + favorito + narración-no-juzga; ya está en 🟦/🟩/🟥).
- Failure-catalog como doc Capa C operacional + `TASTE-LOG.md` deportes.
- `INGENIERO-PAUTA-MASTER` ya tiene REGLA DE AMBIENTE + paleta SFX fútbol (ajustes menores).

### Estado
- **Versión:** v0.2 operativa (pre-empírico, fase de validación) — diseño v0 + capa operativa §10.A/B/C.
- **Pre-rebuild attempts (NO usar como autoridad — HR#19):** `champions-sport-choice` / `champions-arsenal-wins` / `champions-psg-wins` — NOT SHIPPED. Fallaron por (a) concepto rival/compañero roto (la estrella foil aparecía como rival en el played path) y (b) teleport-continuity entre shots. El diseño v0 resuelve ambos (elegir-compañero + dos-recorridos + EXECUTION CONTINUITY §2 + foil fuera del played path §4); v0.2 baja la estructura a una capa operativa para que esté lista ANTES de producir el próximo. Learnings en `video-log.md` #1.
- **Para promover a v1.0 empírico:** shippear ≥3 videos + derivar canonical-scenes propios + loguear hallazgos en `video-log.md`.
