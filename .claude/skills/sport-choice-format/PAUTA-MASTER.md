# PAUTA-MASTER.md — Pauta del formato "Sport-Choice" (drama deportivo interactivo)

> **AUTORIDAD CREATIVA del formato sport-choice** (rol 🏛️ ARQUITECTO). Define la HISTORIA/LÓGICA del formato.
>
> **Versión:** **v0** — 2026-06-01. **Reemplaza la v0.1** (que tenía la estructura "rama corta foil" + counterfactual opening que spoileaba). Esta versión consolida el diseño derivado de:
> - la sesión de diseño con Tomás (2026-05-31 / 06-01),
> - `BRIEF-TEMPLATE-DEPORTES-v0` (input de ideas de Tomás),
> - `creative-director/master-flow-v2/SYSTEM-LEARNINGS-V3-V4-COMPILATION.md` (learnings del sistema).
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
| **No-favorito → su recorrido** | **MÁS compuertas** (~3-4) → más difícil, más chances de fallar |
| **El gap escala con las cuotas** | favoritazo → 2 vs 4 · partido parejo → 2 vs 3 |
| 🟦 **Invisible como editorial** | NO se dice "este es el fácil" — se **deriva de la realidad** → hace sentido + automatable |
| 🟩 **Knob de batacazo** | se puede invertir (underdog más fácil) para narrativa de upset (raro) |

---

## §5 — LAS DECISIONES = JUGADAS (compuertas)

- 🟩 **Compuertas por recorrido:** 2 (favorito) a 3-4 (no-favorito), según §4.
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

## §11 — OUTRO / CTA

- El **contraste entre los dos recorridos** ES el counterfactual (ves las dos elecciones).
- 🟦 **CTA loop** tipo tagline reconocible cross-video: *"Elige bien a tu compañero. Y vuelve mañana."* + watermark `@elige_tucompanero` persistente.

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
| **Pipeline CP0 → CP5** + gates obligatorios por CP | `master-flow-v2` + CLAUDE.md |
| **8 gates pre-render** + dual quality bar + **Gemini QA** (audit-frames, audit-gemini-calibrated, audit-audio, continuity) | CLAUDE.md § Pre-render gate |
| **Ensamblado HYBRID per-clip atomic** + captions Whisper word-timed (HR#3/#25/#30) | `PIPELINE.md §13` |
| **MODEL-CAPABILITIES** (clip_max, pace WPM, constraints Gemini) HR#28/#29 | `ai-video-production/MODEL-CAPABILITIES-MATRIX.md` |
| **Cost cap 25%** sobre último video exitoso · **TDD** (HR#26) · medir-no-estimar | SYSTEM-LEARNINGS-V3-V4 |
| **Mecánica choice** (countdown 1s/dígito, loading bar, botones A/B, framing acción-condicional, POV >80%) | `choice-format-core/CHOICE-MECHANIC.md` (creativa) + `choice-format-core/INGENIERO-CHOICE-CORE.md` (técnica choice-UI) — agnóstico, derivado de los 8 virales vía horror |

---

## §14 — PENDIENTES + RELACIÓN CON DOCS + ESTADO

### Deliverables Capa B/C que siguen a esta pauta
- `BRAND.md` deportes (look cálido/saturado/brillante + preset CSS — OPUESTO al lúgubre `saturate .35/brightness .74` de horror).
- SPEC template deportes v1 (hereda schema v11; campos sport: `risk_policy`, `favorite`, `recorridos[]`, `compuertas`).
- `SCRIPT-WRITING-GUIDE.md` update (alinear a dos-recorridos + favorito + narración-no-juzga; ya está en 🟦/🟩/🟥).
- Failure-catalog como doc Capa C operacional + `TASTE-LOG.md` deportes.
- `INGENIERO-PAUTA-MASTER` ya tiene REGLA DE AMBIENTE + paleta SFX fútbol (ajustes menores).

### Estado
- **Versión:** v0 (pre-empírico, fase de validación).
- **Pre-rebuild attempts:** `champions-sport-choice` / `champions-arsenal-wins` / `champions-psg-wins` (2026-05-30) — fallaron por (a) concepto rival/compañero roto y (b) teleport-continuity. Esta v0 resuelve ambos (elegir-compañero + dos-recorridos + EXECUTION CONTINUITY). NO usar como autoridad.
- **Para promover a v1.0 empírico:** shippear ≥3 videos + derivar canonical-scenes propios + loguear hallazgos en `video-log.md`.
