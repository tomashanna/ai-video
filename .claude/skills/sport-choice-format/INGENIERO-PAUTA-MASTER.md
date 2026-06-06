# INGENIERO-PAUTA-MASTER.md — Autoridad TÉCNICA del INGENIERO para sport-choice × reel

> **AUTORIDAD TÉCNICA del formato sport-choice** (rol 🛠️ INGENIERO). Define CÓMO ejecutar técnicamente lo que la PAUTA-MASTER creativa dicta.
>
> ⚠️ **ESTE DOC HEREDA, NO DUPLICA.** sport-choice comparte 100% el pipeline técnico universal + la técnica choice-UI agnóstica. La autoridad de lo heredado vive en DOS capas:
> - **`../choice-format-core/INGENIERO-CHOICE-CORE.md`** (Capa A.5 — técnica choice-UI agnóstica: decision-UI editorial pacing, UI safe zones caption Y62/loading Y52/countdown Y46/name labels Y11.5, caption chunking word-timed, lip sync rule, 0 cuts en hook — derivada de mediciones F1 de 10 referentes vía horror) +
> - **`ai-video-production/`** (Capa A — técnica UNIVERSAL: pace WPM, LUFS, mix de volúmenes, cuts/min, music BPM, coverage, HYBRID per-clip atomic, MODEL-CAPABILITIES, motion, mastering, 8 gates — PIPELINE, CAPTIONS, SFX-PIPELINE, MOTION-LAYER, AUDIO-MASTERING, MODEL-CAPABILITIES-MATRIX, etc.). `INGENIERO-CHOICE-CORE.md` apunta a esta capa para lo universal; no la duplica.
>
> Este doc documenta SOLO lo sport-específico: la ⭐⭐ **REGLA DE AMBIENTE**, la paleta SFX fútbol, y la consistencia de kits/likeness. Todo lo demás se hereda.
>
> **Última actualización:** 2026-05-31 (creación)
> **Versión:** v0.1 (pre-empírico — fase de validación)

---

## 0. METODOLOGÍA — DE DÓNDE VIENEN ESTAS REGLAS

### Lo que se HEREDA — DOS capas (técnica choice-UI de Capa A.5 + técnica universal de Capa A, NO re-medido)

> Las filas marcadas **[A.5 choice-core]** son técnica de la mecánica choice → autoridad `../choice-format-core/INGENIERO-CHOICE-CORE.md`. Las marcadas **[A universal]** son pipeline universal → autoridad `ai-video-production/`. Ninguna se re-mide acá. (El lineaje empírico de ambas son las mediciones F1 de 10 referentes vía horror — esa historia sigue siendo cierta, ahora vive en core.)

| Métrica técnica | Valor heredado | Autoridad |
|-----------------|----------------|-----------|
| **Speaking rate** | 156-195 WPM (target ~165 WPM; narrador sport = El Faraón `QpDQJR3frbDwOhTIo8nW` — raw WPM a MEDIR en CP2 del video #2 antes de fijar atempo, HR#19) | **[A universal]** `ai-video-production/` (NARRATION) + `MODEL-CAPABILITIES-MATRIX.md` + `library/voices-catalog.json` |
| **Narration coverage** | ≥80% | **[A universal]** `ai-video-production/` (audit-audio / coverage) |
| **LUFS integrated** | -14 ±0.5 (Instagram) | **[A universal]** `ai-video-production/AUDIO-MASTERING.md` + CLAUDE.md HR#1/#9 |
| **Mix de volúmenes** | narración 1.0 / música 0.05-0.18 / SFX 0.20-0.35 / flash 0.55-0.65 | **[A universal]** CLAUDE.md HR#9 + `SFX-PIPELINE.md` |
| **Ducking / sidechain** | -6 dB target sobre música+ambient cuando narrador habla | **[A universal]** `SFX-PIPELINE.md` + SPEC `layer_3.sidechain_target_db` |
| **Cuts/min** | banda 14-22 (modulado por sección — ver editing_targets del SPEC) | **[A universal]** `ai-video-production/PACING-MARKERS.md` |
| **Music BPM** | según mood (ver § música sport abajo) | **[A universal]** `SFX-PIPELINE.md` (MUSIC layers) |
| **0 cuts en hook** | universal (hook = single shot O push-in continuo) | **[A.5 choice-core]** `../choice-format-core/INGENIERO-CHOICE-CORE.md § 5` |
| **Captions** | Whisper word-timed progresivos, ≤2 líneas, chunk_caption_cues (NUNCA bloque estático que se trunca) | **[A.5 choice-core]** `../choice-format-core/INGENIERO-CHOICE-CORE.md § 3` + CLAUDE.md HR#3/#30 + `CAPTIONS.md` |
| **UI safe zones** | caption Y62 / loading Y52 / countdown Y46 / name labels Y11.5 monospaced + no-overlap matrix | **[A.5 choice-core]** `../choice-format-core/INGENIERO-CHOICE-CORE.md § 2` + CLAUDE.md HR#4 |
| **Decision-UI editorial pacing** | countdown digit 1.0s, pause beat 0.9s median, loading Y52 ≥6% sep de countdown, NO ambient duck obligatorio, freeze/filter OPCIONAL | **[A.5 choice-core]** `../choice-format-core/INGENIERO-CHOICE-CORE.md § 1` |
| **Lip sync rule** | si `lip_sync_required: false` → NO clip con boca visible moviéndose | **[A.5 choice-core]** `../choice-format-core/INGENIERO-CHOICE-CORE.md § 4` |
| **Ensamblado** | HYBRID per-clip atomic (captions burned per clip + Layer 3 continuo) | **[A universal]** CLAUDE.md HR#23 + HR#25 + `PIPELINE.md § 13` + `build_clip_atomic.py` |
| **MODEL-CAPABILITIES** | Hailuo clip_max 5.9s, etc. — leer la MATRIX antes de producir | **[A universal]** CLAUDE.md HR#28/#29 + `MODEL-CAPABILITIES-MATRIX.md` |
| **8 gates pre-render** | Gate 0 spec-completeness + lint + narrative + render-lock + frames + audio + continuity + qa-gate | **[A universal]** CLAUDE.md § Pre-render gate |

> **Regla #1 del ingeniero (heredada):** NUNCA usar nuestras propias producciones como autoridad técnica. La autoridad de la mecánica son los referentes F1 (vía `choice-format-core/INGENIERO-CHOICE-CORE.md` para la técnica choice-UI + `ai-video-production/` para lo universal). Para la capa sport (REGLA DE AMBIENTE, SFX fútbol), la autoridad es ESTE doc + se valida con cada video.

### Lo que es SPORT-ESPECÍFICO (este doc)

1. ⭐⭐ **REGLA DE AMBIENTE** (§ 1) — el orden visual del partido en cada prompt de imagen/animación. **La regla técnica central del formato.**
2. **Paleta SFX fútbol** (§ 2) — qué sonidos pueblan la capa SFX.
3. **Consistencia de identidad** (§ 3) — kits propio vs rival, likeness descriptor-based.
4. **Música deportiva** (§ 4) — el mood musical reskineado.

---

## 1. ⭐⭐ REGLA DE AMBIENTE — el orden visual del partido (LA REGLA TÉCNICA CENTRAL)

> **Como TODO pasa en la cancha, el riesgo #1 del formato es que el viewer no entienda QUÉ está pasando en el partido en cada frame** (dónde está el arco, quién es compañero, quién rival, dónde está el balón). La REGLA DE AMBIENTE elimina ese riesgo: cada prompt de imagen/animación UBICA la escena ANTES de la acción, en un orden fijo.

### La regla (NO negociable)

**Cada `visual_intent` de cada shot DEBE construirse en este ORDEN exacto:**

```
(1) CÁMARA POV 1ª persona del jugador
     ↓
(2) ZONA del campo  (círculo central / banda / borde del área / mano a mano / medio campo)
     ↓
(3) GEOGRAFÍA clara:
       - arco + red (¿dónde está la portería?)
       - compañeros (kit PROPIO)
       - rivales (kit OPUESTO)
       - arquero (kit DISTINTO a ambos)
       - balón (¿dónde está?)
       - líneas de cal (referencia espacial)
     ↓
(4) ESTADIO lleno + reflectores + césped
     ↓
(5) la ACCIÓN / animación  (lo que pasa en este shot)
```

**Calidad de imagen:** premium, foto-real broadcast, lente 85mm, profundidad de campo. Debe entenderse **CLARÍSIMO qué pasa en el partido** en cada frame.

**Por qué este orden:** ubicar primero (POV → zona → geografía → estadio) ancla al viewer espacialmente; recién entonces la acción tiene contexto. Si la acción va primero (o sin geografía), el viewer ve "alguien patea algo en algún lado" — confuso. La geografía DEBE preceder a la acción.

### Ejemplo completo #1 — shot del HOOK (dyad)

```
Cámara POV en primera persona de un jugador, parado en el CÍRCULO CENTRAL del
estadio [Puskás Aréna]. Geografía: a la izquierda Saka (kit ROJO mangas blancas,
dorsal 7, piel marrón, rapado, barba corta, sonrisa amplia) pide el balón con la
mano abierta; a la derecha Dembélé (kit AZUL marino franja roja central, dorsal 10,
piel oscura, rapado, bigote, serio); líneas de cal del círculo central bajo los pies;
balón blanco oficial en el suelo. Estadio Champions LLENO desenfocado al fondo,
reflectores cayendo sobre el césped verde brillante. Acción: micro-bob de cámara,
los dos jugadores miran al viewer esperando la elección. Foto-real broadcast, 85mm,
profundidad de campo.
```

(Orden verificable: POV ✓ → zona [círculo central] ✓ → geografía [Saka kit rojo izq / Dembélé kit azul der / líneas / balón] ✓ → estadio [lleno + reflectores + césped] ✓ → acción [micro-bob, miran al viewer] ✓.)

### Ejemplo completo #2 — shot de DECISIÓN (D3 clímax mano a mano)

```
Cámara POV en primera persona del jugador, en el MANO A MANO dentro del área rival.
Geografía: el arquero del rival (kit verde fosforescente distinto a ambos equipos)
adelantado achicando el ángulo a pocos metros; la portería con red detrás de él;
líneas de cal del área grande y el punto de penal a un lado; tu compañero Saka
(kit rojo mangas blancas #7) desmarcado al borde del área izquierdo; balón blanco
controlado a tus pies. Estadio LLENO rugiendo, reflectores y luz fría de tensión
sobre el césped. Acción: el viewer encara al arquero con el balón dominado, decidiendo
el remate; el arquero se agranda. Foto-real broadcast, 85mm, profundidad de campo
shallow sobre el balón y el arquero.
```

(Orden: POV ✓ → zona [mano a mano en el área] ✓ → geografía [arquero kit verde + portería + líneas + Saka kit rojo + balón] ✓ → estadio [lleno + reflectores] ✓ → acción [encara, el arquero se agranda] ✓.)

### Checklist por shot (el ingeniero valida ANTES de generar)

- [ ] ¿El prompt empieza con la cámara POV 1ª persona?
- [ ] ¿Está nombrada la ZONA del campo explícitamente?
- [ ] ¿Está la GEOGRAFÍA completa: arco, kit propio, kit rival, arquero (si aplica), balón, líneas?
- [ ] ¿Está el ESTADIO (lleno + reflectores + césped)?
- [ ] ¿La ACCIÓN va AL FINAL, no al principio?
- [ ] ¿Los kits son inequívocos (color propio vs opuesto vs arquero)?
- [ ] ¿Queda CLARÍSIMO qué pasa en el partido con solo leer el prompt?
- [ ] ¿Cierra con "foto-real broadcast, 85mm, profundidad de campo"?

Si ❌ en cualquiera → reescribir el prompt antes de generar (no dejar que el modelo improvise la geografía).

### Anti-patterns de la REGLA DE AMBIENTE

❌ **Acción primero, geografía después** ("le pega al balón… en un estadio") → el modelo no sabe dónde está el arco.
❌ **Geografía incompleta** (falta el arco, o no se sabe quién es compañero/rival) → frame ambiguo.
❌ **Kits no especificados o ambiguos** → el viewer no distingue aliado de obstáculo.
❌ **"Estadio" genérico sin lleno/reflectores/césped** → se ve vacío y falso, no broadcast.
❌ **POV no establecido** → el modelo genera tercera persona (rompe HR de POV 1ª persona).
❌ **Falta el balón** → jugada sin balón = sin sentido futbolístico.
❌ **Botas/piernas propias del POV visibles y ESTÁTICAS** → si las zapatillas/piernas del viewer aparecen en el frame, el motion prompt DEBE darles movimiento (peso cambiando, paso, ajuste de apoyo). Piernas POV congeladas = uncanny inmediato (regla del creator 2026-06-04, caso champions).

---

## 1.5 ⭐⭐ MOMENTO DE DECISIÓN — clips + UI (traducción técnica de PAUTA § 10.D, directivas del creator 2026-06-04)

### Clips de COMPUERTA (los shots de decisión) — el balón espera

🟦 El motion prompt de toda compuerta sigue esta plantilla (R2 de PAUTA § 10.D):
```
slow-motion tense hold: the ball stays in the POV's possession ([at the own boots / floating
mid-air toward the POV]) and NEVER resolves its action; surrounding players keep moving
([rival pressing, teammate making a run]), crowd alive in the background; camera locked at
first-person eye level; the moment stretches as if time slowed for the decision; no talking.
```
- 🟦 **Cámara lenta explícita** ("slow-motion", "the moment stretches") — el clip ES la decisión sostenida.
- 🟦 **El balón NO inicia acción** — sin pases saliendo, sin remates, sin el balón viajando al arco.
- 🟩 El entorno SÍ vive: rivales que presionan, compañeros desmarcándose, multitud, banderas.
- 🟥 ANTI-PATTERN: balón avanzando al arco / arquero reaccionando / jugada resolviéndose ANTES del pick del viewer (casos shots 05/13/15 draft #2 mexico-sudafrica).
- ⛔⛔ **HANDBALL GENERADO — manos y balón JAMÁS en la misma cláusula del prompt** (caso shot_05 Kling 2026-06-05: el motion pedía "balón en posesión" + "mangas propias en el frame" → el modelo resolvió la posesión AGARRANDO el balón con las manos del POV — handball flagrante; los i2v no conocen las reglas del fútbol). Regla: (a) la posesión del balón se describe SIEMPRE con pies/botas ("at the own boots", "glued to the feet", "the ball stays on the grass"); (b) si las mangas/manos POV aparecen en el prompt, van en cláusula SEPARADA y LEJOS del balón ("hands stay down at the sides, out of frame"); (c) **negative OBLIGATORIO en todo motion de jugada de campo**: "no hands touching the ball, the ball is played with feet only". Únicas excepciones: arquero (guantes) y saque de banda explícito.

### Clips de CONSECUENCIA — desde el punto de decisión, en la dirección decidida

🟦 El prompt de imagen Y el motion de toda consecuencia heredan la POSICIÓN del shot de decisión (R1+R3):
- El primer frame de la consecuencia ≈ el encuadre del freeze de la decisión (misma zona, misma orientación al arco).
- La acción/cámara se mueve **EN LA DIRECCIÓN de la opción elegida** ("the play breaks out toward [the right where the teammate was / the near post]").
- 🟥 ANTI-PATTERN: el desenlace visto desde FUERA de la cancha o desde otra zona del campo (caso shot_07 draft #2 — "decidí dentro del área y me veo afuera").

### Decision-UI SPORT (override del estilo heredado — el film-leader queda solo para el HOOK)

| Elemento | Regla sport (creator 2026-06-04, refinada post draft v4) |
|----------|----------------------------------|
| **Countdown de compuerta** | **ESTILO UNIFICADO con el hook** (creator post-v5): dígito **3 → 2 → 1 ARRIBA** (Y≈28-32), **~240px** monospaced + stroke/glow, **CON CÍRCULO/RING alrededor** (~400px Ø, trazo blanco grueso, estilo academy-leader) para que se note más — ⛔ pero SIN el crosshair/líneas internas (eso desconcentra sobre la jugada). 🟩 Variante válida: barra que se RELLENA al 100% ARRIBA de los números (sincronizada al countdown). SIEMPRE completo 3-2-1. ⛔ SIN barra "draining" debajo (v4, bug). |
| ⭐ **Barra de progreso del VIDEO** | Barra **GLOBAL persistente** que muestra el avance del video completo ("cuánto le queda al video" — retention device pedido por el creator): fina (~5-7px), borde inferior (Y≈98.5-99, fuera de las safe zones de contenido), blanca semitransparente (~70%), se LLENA de izquierda a derecha con el progreso real, visible TODO el video. |
| **Botones A/B** | ⛔ SIEMPRE rotulados con prefijo **"A. "** y **"B. "** (p.ej. "A. DESCARGAS CON GIMÉNEZ"). Y75/Y82 como siempre. |
| **Hook countdown** | **MISMO sistema que las compuertas** (creator post-v6: el film-leader centrado TAPA los captions del dyad): dígito 240px + ring ARRIBA, completo 3-2-1. ⛔ El AVU film-leader centrado queda FUERA del formato sport (los ticks de audio se mantienen). UN solo estilo de countdown en todo el video. |
| ⭐ **Caption muere con la voz** | ⛔ El caption del narrador DESAPARECE cuando el narrador termina de hablar (la última cue termina en el `end` real de la última palabra del words.json — JAMÁS sostenida hasta el final del clip). Bug class conocida del chunker (`chunk_caption_cues` champions outro + hook mexico-sudafrica v6): en shots con cola sin narración (hook 9s, outro), el caption fantasma queda colgado. Regla universal del formato (portar al template Capa A). |
| **Contexto de equipo del hook** | El contexto explícito jugador=equipo (PAUTA §3) vive EN el caption estilizado clase-name del narrador ("Giménez, México." verde / "Tau, Sudáfrica." amarillo) + los name labels + los kits. ⛔ SIN banner duplicado Y55 (el "GIMÉNEZ = MÉXICO · TAU = SUDÁFRICA" del diseño v1 quedó redundante — creator post-v6: "no eliminaste los captions anteriores"). |
| **Captions del narrador vs UI textual (TODO shot)** | ⛔ ZONAS EXCLUSIVAS universales: la narración es DUEÑA de Y62 en todo el video; cualquier UI textual concurrente (caption de contexto del hook, pregunta del outro "¿QUIÉN GANA EL PARTIDO?", warnings) va a **Y55**. JAMÁS dos textos en la misma Y en la misma ventana (bugs draft #2 hook + draft v4 outro). |
| ⭐ **Caption del HOOK = clase "name" EMOCIONANTE** | (creator post-v5: "están muy planos… hacelos más estéticos al inicio"). En el caption de la presentación del dyad ("…Giménez, México. Tau, Sudáfrica."), los NOMBRES + EQUIPOS van **coloreados con el color del kit** (p.ej. GIMÉNEZ/MÉXICO en verde kit, TAU/SUDÁFRICA en amarillo Bafana) + **más grandes que la narración normal** (~1.3-1.5×) + stroke. La emoción del momento de elección se ve en el caption — texto plano blanco SOLO para narración corriente. (Hereda el espíritu del sistema de 3 clases de `ai-video-production/CAPTIONS.md` — clase name.) |

---

## 2. PALETA SFX FÚTBOL

> Reemplaza la paleta de horror (drones, susurros, gritos). Heredá la MECÁNICA de SFX (`SFX-PIPELINE.md`: capa dedicada track-index 60-110, foley por acción visible, ducking) pero con SONIDOS DEPORTIVOS. Los presets de voz de horror en `effects-library/voice-effects/` NO se usan.

### Catálogo SFX sport-choice

| Categoría | SFX | Cuándo |
|-----------|-----|--------|
| **Ambiente base (continuo)** | **Rugido de hinchada** (packed stadium crowd roar) | Cross-clip continuo casi todo el video — la final NO calla nunca |
| **Ambiente base** | **Cánticos lejanos de ultras** + eco de estadio cerrado | Capa continua bajo el rugido |
| **Eventos de juego** | **Silbato** del árbitro | Inicio/falta/penal |
| **Eventos de juego** | **Golpe al balón** (boot-strike) | Cada vez que se patea/pasa |
| **Eventos de juego** | **Red inflándose** (net ripple) | GOL |
| **Eventos de juego** | **Atajada / manotazo** (goalkeeper save) | El arquero saca/ataja |
| **GLORIA (acierto)** | **Explosión de celebración** de la hinchada | Gol propio / campeón |
| **GLORIA** | **Confeti** (rustle) + cánticos eufóricos | Vuelta olímpica / levantar la copa |
| **BURLA (error)** | ⭐ **Abucheos / "uy" decepcionado** de la hinchada | Cada error → la jugada se cae |
| **BURLA** | **Silbidos** de la hinchada | Humillación sostenida |
| **UI** | Tick del countdown 3-2-1 (film leader academy) + beep tick del loading bar | Cada decisión (el AVU countdown es UNIVERSAL — vive en `ai-video-production/templates/avu-library/`, NO en horror) |

### Regla absoluta de la paleta

> ⛔ **NUNCA gritos de horror, drones de terror, sub-bass de jumpscare, ni susurros uncanny.** El audio de sport-choice es 100% diegético-deportivo + música de tensión deportiva. Si un SFX evoca terror, está fuera de formato.

### Capas de audio (heredadas, reskineadas al estadio)

| Capa | horror | sport-choice |
|------|--------|--------------|
| Música (Layer 3 drone) | dark ambient drone | drone subharmónico de tensión deportiva sostenida (sports-thriller bed) |
| Voiceover | narrador grave | relator play-by-play deportivo, español neutral (El Faraón `QpDQJR3frbDwOhTIo8nW` — voices-catalog) |
| Ambient continuo (Layer 2) | hum/viento del setting | **rugido de estadio lleno** + cánticos + eco (cobertura 99-100%, cero dead zones) |
| SFX puntuales (Layer 1 clip-scoped) | foley horror + impactos | foley deportivo (boot-strike, red, atajada) + abucheos/confeti |
| Accent (clímax) | string stabs | rising strings + low pulse en D3 (mano a mano) + remate |

(Detalle creativo de las 4 capas → `creative-direction/audio-direction.md`. Detalle técnico de la mecánica SFX → `ai-video-production/SFX-PIPELINE.md`.)

---

## 3. CONSISTENCIA DE IDENTIDAD — RÉGIMEN ESTRICTO (kits + 5 anchors + likeness) — RIESGO #1 CP1

> Lo equivalente a "character consistency" de horror, pero centrado en KITS DE EQUIPO + likeness de jugadores reales. **Es el riesgo de producción #1 del formato** — por eso es un régimen ESTRICTO codificado, no un "ojalá salga parecido".

### 3.0 ⭐ LOS 5 ANCHORS OBLIGATORIOS POR VIDEO

> Cada video sport-choice genera estos 5 anchors en CP1 (UNA reference image por anchor, reusada en todos sus shots vía `--ref` / reference mode). El dorsal + el patrón del kit son la **visual signature** — NUNCA varían cross-shot.

| Anchor | Qué es | Kit / firma | Por qué es obligatorio |
|--------|--------|-------------|------------------------|
| `jugador_A` | La estrella del equipo A (compañero del recorrido jugado si A es el elegido) | [KIT_A] + dorsal_A, rasgos foto-reales descriptor-based | El compañero recurrente del recorrido jugado |
| `jugador_B` | La estrella del equipo B (el foil) | [KIT_B] + dorsal_B, rasgos foto-reales descriptor-based | Aparece SOLO en hook + su propio recorrido `counterfactual_*` + cliffhanger (PAUTA § 4) |
| `arquero_rival` | El arquero | **[KIT_GK] DISTINTO a ambos equipos** (regla real del fútbol: guante + color diferenciado) | Evita confusión en el mano a mano; aparece en todas las definiciones |
| `rival_npc` | Defensor/lateral genérico de campo | kit del equipo OPUESTO al recorrido en curso, **cara genérica** (NO una estrella nombrada) | ⛔⛔ **Los obstáculos del played path usan ESTE anchor, NUNCA el de `jugador_B`.** Reusar el anchor de la estrella foil para los rivales del played path es el **bug EXACTO del topical champions** (shots 05/06/07/12/17/19) → confunde quién es el compañero. Anchor `rival_npc` aparte = fix. |
| `viewer_hands` | Las manos/botas del POV | mangas + (si visibles) botas con el **kit ELEGIDO** del recorrido en curso | El viewer ES el protagonista (POV >80%); sus mangas marcan de qué equipo juega en cada recorrido |

> ⚠️ **`viewer_hands` cambia de kit entre recorridos:** en el recorrido jugado las mangas son [KIT_A]; en el recorrido del foil (la otra hipótesis) son [KIT_B]. Generar la variante de manos por kit (o un anchor de manos por kit). El PIVOTE (PAUTA § 10.A) es justamente donde el viewer ve que sus mangas cambiaron de kit.
> ⛔ **El anchor `viewer_hands` NO se pasa como reference image a los shots de campo** (lección empírica mexico-sudafrica CP3 2026-06-04): el modelo IMPORTA LA POSE del anchor (piernas sentadas/despatarradas → tercera persona del propio cuerpo = POV roto). El color de mangas se controla TEXTUALMENTE ("mangas VERDES/AMARILLAS propias" en el visual_intent) + directiva first-person explícita. El anchor de manos sirve como REFERENCIA DE ESTILO para el humano/auditor, no como ref del modelo.
> 🟩 Si un video tiene jugadores que hablan on-screen en shots donde se aísla una zona sin cara (raro en sport), considerar anchors locus-específicos (`MODEL-BEHAVIOR-LOG.md` entry 1) — pero en sport el riesgo locus es bajo (la firma es el kit+dorsal, no anatomía rara).

### 3.1 SPEC REQUIREMENTS (el arquitecto los declara; el schema v11 ya los soporta)

- 🟦 `anchor_consistency_strict: true` por shot con personas (Bryan-style strict — schema v11).
- 🟦 `anchor_id_required` por shot: qué anchor de CP1 DEBE matchear cada persona visible (p.ej. `{ jugador_A: "jugador_A_v1", arquero_rival: "arquero_rival_v1" }`). Los obstáculos del played path → `rival_npc`, NUNCA `jugador_B`.
- 🟦 **Kit + dorsal INVARIANTES cross-shot** (la visual signature). El color, el patrón de mangas y el número NO cambian entre shots del mismo anchor.
- 🟦 `anchor_similarity_threshold: 0.6` (Script B dim 6 — el floor enforced del schema v11).

### 3.2 ⛔ GATE CP1 — regen MANDATORY si la consistencia falla (Risk C ya codificado)

> Esto NO se reinventa — es el **Risk C** ya codificado en el sistema. Citarlo, no recrearlo:

- 🟦 Si la consistencia del anchor **falla el audit** (Script B **dim 6 anchor_similarity < 0.6**) → **regen MANDATORY del anchor ANTES de CP3.** No es decisión humana opcional: es auto-regen estructural (el principio canónico "si el SPEC declara X y el output produce Y, se regenera para match — no se patchea downstream").
- 🟦 **Por qué es barato hacerlo bien en CP1:** el costo de regenerar un anchor es trivial (~$0.04-0.36) vs la propagación a CP4 Hailuo si la inconsistencia llega a la capa cara (regenerar clips animados = $3-5). Atrapar la inconsistencia en CP1 es el punto de máximo apalancamiento. (Authority: schema v11 `dim6_anchor_similarity_min: 0.6` + GAPS-LOG #44 "engineer regen anchor antes de CP3" + el costo trivial vs propagación.)
- 🛠️ El ingeniero registra el resultado del audit de consistencia (por anchor, por shot) en el `CP1-handoff.md`.

### Kit propio vs rival — siempre legible

- **El kit del jugador elegido = TU equipo (tu kit).** Aparece en el POV (tus mangas), en tu compañero, y define "los míos".
- **Los rivales visten el kit OPUESTO** (color contrastante). Son obstáculos (lateral, defensores).
- **El arquero rival viste un kit DISTINTO a ambos** (regla real del fútbol — guante + color diferenciado). Esto evita confusión en el mano a mano.
- En cada shot, el ingeniero verifica que los 3 kits (propio / rival de campo / arquero) sean visualmente inequívocos. El kit es la señal que le dice al viewer quién es aliado y quién obstáculo.

**Anchors de kit:** generados por los 5 anchors obligatorios de § 3.0 (UNA reference image por anchor, reusada vía `--ref` / reference mode). El dorsal y el patrón del kit = la "visual signature", NUNCA varían cross-shot. ⛔ Recordatorio del bug champions: el obstáculo de campo es `rival_npc` (cara genérica), NO el anchor de la estrella foil `jugador_B`.

### Likeness de jugadores reales = descriptor-based (REGLA CRÍTICA — el riesgo #1 CP1)

> ⭐ **Este es EL riesgo de producción #1 del formato.** La likeness descriptor-based de jugadores reales es lo más probable que requiera iteración en CP1 → **presupuestar iteración de CP1 (anchor generation) para `jugador_A` y `jugador_B`** explícitamente en el plan de costo del video.

- ⛔ **NUNCA poner el nombre de la celebridad literal en el prompt de imagen.** Los modelos t2i no reproducen personas reales nombradas de forma confiable (producen caras genéricas o fallan).
- ✅ Describir por **RASGOS FOTO-REALES reconocibles**: posición + tono de piel + corte de pelo + vello facial + gesto característico + **kit con dorsal**. Ejemplo: "extremo del [equipo], piel marrón, rapado, barba corta, sonrisa amplia, kit rojo mangas blancas dorsal 7".
- **Iterar en CP1** hasta likeness aceptable (gate § 3.2: dim 6 ≥ 0.6, regen mandatory bajo el umbral).
- Si la likeness no converge a un nivel aceptable tras iteración razonable, **escalar al arquitecto** (puede decidir jugador ficticio o ajustar el descriptor) — no forzar un anchor pobre downstream.

### Lip sync (heredado, aplicado al protagonista)

- El **jugador protagonista PUEDE hablar on-screen** (p.ej. pidiendo el balón / "Confía en ti, la metes" / "Te lo dije, hermano"). En esos shots `lip_sync_required: true`.
- Aplica la **lip sync rule heredada** (`../choice-format-core/INGENIERO-CHOICE-CORE.md § 4`): si `lip_sync_required: false`, NO usar clips con boca visible moviéndose (crea disonancia). El ingeniero itera tools (Hedra primary, ver MODEL-BENCHMARK) hasta resultado aceptable.

---

## 4. MÚSICA DEPORTIVA (mood reskineado)

> Hereda la mecánica de música universal de `ai-video-production/SFX-PIPELINE.md` (3 capas mandatorias, BPM por mood, evolución, ducking — ver tabla heredada-universal de `../choice-format-core/INGENIERO-CHOICE-CORE.md § 0`). Reskin del MOOD:

| Sección | Mood musical sport-choice | Ejemplo de prompt ElevenLabs |
|---------|---------------------------|------------------------------|
| Hook + juego en tensión | Drone subharmónico de **tensión deportiva sostenida** (sports-thriller bed) | "low subharmonic drone, sustained deep bass tension, no melody, dark cinematic sports-thriller bed, faint orchestral swell undertone" |
| Desenlace glorioso (gol/campeón) + resolución + outro (acierto) | **Celebración triunfal cálida** | "triumphant stadium celebration ambience, distant euphoric crowd cheering warm, confetti rustle, victory tone, uplifting, no horror" |
| Clímax D3 (mano a mano) | **Tensión rising** | "rising dark cinematic strings tension, pounding low pulse building, climax buildup, no resolution" |
| Outro sostenido | Hum bajo + swell triunfal (loop cue) | "sustained low hum gradual fade blended with faint triumphant swell, cliffhanger atmospheric, loop cue" |

**Contraste musical clave:** el drone de tensión (juego) → celebración cálida (gol/gloria). Igual que horror contrasta drone → folk cozy, sport-choice contrasta tensión → triunfo. El error/burla va con paleta fría desaturada (gris-azul del fracaso, NO rojo de horror) + abucheos.

**LUTs (intent de color, ejecuta el ingeniero):**
- `warm_glory` = celebración / gol / copa (cálido dorado)
- `cool_cinematic_stadium` = juego en tensión (frío cinematográfico de broadcast)
- `cool_defeat` = error / burla (frío desaturado gris-azul — el frío del fracaso deportivo, NO horror rojo)

(Sin `cool_horror` ni ninguna LUT de terror.)

---

## 5. GATES + VALIDACIÓN (heredados)

Se heredan los **8 gates pre-render** (CLAUDE.md § Pre-render gate) + el dual quality bar (Gemini ≥9.7 + audit-against-referent ≥85%). Notas sport-específicas para los gates:

- **Gate 4 (audit-frames Gemini Vision):** verificar adicionalmente que en cada frame se entienda la geografía del partido (arco visible, kits distinguibles, balón ubicable) — la REGLA DE AMBIENTE se valida acá visualmente.
- **Gate 5 (audit-audio):** verificar que el rugido de estadio cubra ≥99% (cero dead zones) y que los abucheos/celebración estén presentes en los beats de error/gloria.
- **Gate 6 (continuity-check):** verificar que la cadena de lógica deportiva cierre (elección → equipo → jugadas → resultado) sin saltos, y que el orden hablado = orden de botones.
- **audit-against-referent:** ⚠️ sport-choice aún NO tiene referentes virales propios para el ≥85% de métricas críticas. Hasta tenerlos, este audit se corre contra las **bandas técnicas heredadas de F1** (las de la mecánica: LUFS, cuts/min, UI safe zones, pace) — que SÍ aplican. Las métricas de CONTENIDO deportivo (qué % son shots de jugada, etc.) se derivarán empíricamente con nuestros primeros videos. Documentar honestamente en el handoff que la referencia es la mecánica F1, no referentes sport.

---

## 6. RELACIÓN CON OTROS DOCUMENTOS

### Hereda (autoridad técnica, NO re-litiga)

- ✓ `../choice-format-core/INGENIERO-CHOICE-CORE.md` (Capa A.5) — la técnica choice-UI de la mecánica: decision-UI editorial pacing, UI safe zones (caption Y62/loading Y52/countdown Y46/name labels Y11.5 + no-overlap matrix), caption chunking word-timed, lip sync rule, 0 cuts en hook.
- ✓ `ai-video-production/` (Capa A) — la técnica UNIVERSAL: PIPELINE, SFX-PIPELINE, CAPTIONS, MOTION-LAYER, AUDIO-MASTERING, COLOR-GRADING, PACING-MARKERS, MODEL-CAPABILITIES-MATRIX, build_clip_atomic.py, pace WPM, LUFS, mix, cuts, BPM, los 8 gates. (`INGENIERO-CHOICE-CORE.md` apunta acá para lo universal; no lo duplica.)
- ✓ `video-director/MODEL-BENCHMARK.md` — selección de modelo (imagen + animation + lip sync).

### Aporta (lo sport-específico)

- ✓ REGLA DE AMBIENTE (§ 1) — el orden visual del partido.
- ✓ Paleta SFX fútbol (§ 2).
- ✓ Consistencia de kits + likeness descriptor-based (§ 3).
- ✓ Música/LUTs deportivos (§ 4).

### No toca

- Decisiones creativas (qué jugadas, qué equipos, la lógica narrativa) — son del arquitecto (PAUTA-MASTER).

---

## 7. ESTADO + PRÓXIMOS PASOS

- **Versión:** v0.1 (pre-empírico, fase de validación)
- **Para promover a v1.0 empírico:** medir nuestros primeros videos sport-choice (F1-style: cuts/min, LUFS, coverage, % shots de jugada, claridad de geografía) + escribir bandas técnicas deportivas propias. Hasta entonces, la técnica de la mecánica se hereda de F1 (válida) + la capa sport (AMBIENTE, SFX, kits) se ajusta con cada video logueado en `video-log.md`.
