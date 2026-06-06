---
name: sport-choice-format
description: GENRE skill — sport-choice (drama deportivo interactivo). Misma MECÁNICA que horror-choice (POV 1ª persona, hook dyad, 3 decisiones con countdown + botones A/B, framing acción-condicional, counterfactual, cliffhanger/CTA, ~90s, name labels grandes) pero SIN horror/sobrenatural: la elección = EQUIPO, las decisiones = jugadas reales de fútbol, las consecuencias = gol & gloria O error & burla. Football es la primera aplicación. Activar cuando la tarea mencione: sport-choice, fútbol/football, "elige tu compañero" deportivo, "elige tu equipo", jugada, penal, gol, partido, Champions, dyad de jugadores, "juegas para el equipo X". Por default delivery = reel (vertical 9:16, 80-100s). DEPENDE de `ai-video-production` (toolkit técnico) + `video-director` (workflow). NUNCA activar sola.
---

# Sport-Choice Format — GENRE skill

> Este es un GENRE skill (qué cuenta el video), NO un delivery format skill (cómo se entrega). El delivery por default es `reel` (vertical 9:16, 80-100s).
>
> **Sport-choice y horror-choice son HERMANOS que heredan la mecánica de `choice-format-core`**: comparten 100% la MECÁNICA AGNÓSTICA del formato choice (hook dyad → countdown → decisiones binarias → consecuencias → counterfactual → cliffhanger), que vive en `choice-format-core/` (Capa A.5) — NO una hereda de la otra (hermano heredando de hermano sería un anti-pattern de capas). Lo único que cambia entre ambos es la HISTORIA/LÓGICA de género: drama deportivo en vez de horror. Por eso este formato **hereda el pipeline universal de `ai-video-production` (Capa A) + la mecánica choice de `choice-format-core` (Capa A.5)**, y solo documenta lo que es sport-específico (Capa B).

## ⛔ LECTURA OBLIGATORIA al activar esta skill

> **🏗️ ESTADO DEL FORMATO (2026-05-31):** sport-choice es un **template NUEVO Capa 2** recién creado. Football es la primera aplicación. A diferencia de horror-choice (derivado empíricamente de 8 videos virales canónicos), sport-choice **AÚN NO tiene referentes virales propios** — su autoridad empírica se derivará de nuestros primeros videos (igual que horror-choice se derivó de sus 8 virales). Hasta entonces, la estructura/mecánica se HEREDA de `choice-format-core` (la mecánica agnóstica que SÍ está validada — derivada de los 8 virales vía horror) y solo la lógica deportiva es net-new. Ver § "Estado del formato" abajo.

Si activaste esta skill, leé estos archivos ANTES de planear o ejecutar:

1. **`<repo-root>/CLAUDE.md`** — context global + arquitectura 3 capas + 3 roles
2. **⭐ `<repo-root>/.claude/skills/sport-choice-format/PAUTA-MASTER.md`** — **AUTORIDAD CREATIVA del ARQUITECTO** para sport-choice. La historia/lógica: elección=equipo, decisiones=jugadas, consecuencias=gol/burla, ramas asimétricas, cadena de lógica que debe cerrar, anti-patterns.
2.5. **⭐ `<repo-root>/.claude/skills/sport-choice-format/INGENIERO-PAUTA-MASTER.md`** — **AUTORIDAD TÉCNICA del INGENIERO** para sport-choice. HEREDA la técnica choice-UI de `choice-format-core/INGENIERO-CHOICE-CORE.md` (decision-UI pacing, UI safe zones, caption chunking, lip sync, 0 cuts en hook) + la técnica universal de `ai-video-production/` (pace WPM, LUFS, mix, captions, ensamblado HYBRID, MODEL-CAPABILITIES, 8 gates) + lo sport-específico: la ⭐⭐ **REGLA DE AMBIENTE** (orden visual del partido), paleta SFX fútbol, consistencia de kits.
3. **⭐ `<repo-root>/.claude/skills/choice-format-core/CHOICE-MECHANIC.md`** — **se HEREDA la MECÁNICA estructural AGNÓSTICA** (estructura temporal, hook dyad, invariante, decisión→consecuencia, framing acción-condicional, lenguaje 2ª persona presente, POV >80%, counterfactual placement, cliffhanger/CTA loop, patterns abstractos). Esta es la autoridad de la mecánica choice — derivada de los 8 virales (vía horror) pero ya género-neutro. (Los 8 canonical-scenes de horror se consultan SOLO por su valor ESTRUCTURAL hasta tener canonical-scenes propios de sport.)
3.5. **⭐ `<repo-root>/.claude/skills/choice-format-core/INGENIERO-CHOICE-CORE.md`** — **se HEREDA la técnica choice-UI específica**: decision-UI editorial pacing, UI safe zones (caption Y62 / loading Y52 / countdown Y46 / name labels Y11.5 monospaced + no-overlap matrix), caption chunking word-timed, lip sync rule, 0 cuts en hook. El ingeniero de sport-choice consulta ESTE doc para la técnica de la mecánica choice. ⤴ Para la técnica UNIVERSAL (pace WPM, LUFS -14, mix de volúmenes, cuts/min, music BPM, coverage, HYBRID per-clip atomic, MODEL-CAPABILITIES, 8 gates) la autoridad es **`ai-video-production/`** (Capa A) — `INGENIERO-CHOICE-CORE.md` apunta ahí, no la duplica.
4. **`<repo-root>/.claude/skills/sport-choice-format/SCRIPT-WRITING-GUIDE.md`** — cómo escribir un guion sport-choice (lente principio/variabilidad/anti-pattern, igual que horror).
5. **⭐ `<repo-root>/.claude/skills/sport-choice-format/video-log.md` (AUTORITATIVO PARA ROTACIÓN)** — registro de videos producidos. OBLIGATORIO consultar antes de elegir pattern/setting/dyad.
6. **El sub-doc específico de tu tarea** en `creative-direction/`:
   - Diseñar concepto + slots → `PAUTA-MASTER.md` (todo) + video-log para rotación
   - Escribir guion → `SCRIPT-WRITING-GUIDE.md` + `creative-direction/script-writing.md`
   - Prompts de imagen/animación → **`creative-direction/image-direction.md` (REGLA DE AMBIENTE)** + INGENIERO-PAUTA § REGLA DE AMBIENTE
   - Dirección de audio → `creative-direction/audio-direction.md` (paleta SFX fútbol)
   - UI (name labels equipos, countdown, botones) → `creative-direction/ui-elements.md`
7. Este archivo (`SKILL.md`) entero — hard rules del formato

**ACTIVÁ EN PARALELO obligatoriamente:**
- **`video-director`** — workflow + quality bar + decisiones estratégicas (INGENIERO)
- **`ai-video-production`** — toolkit técnico (PIPELINE, MOTION, CAPTIONS, SFX, QA, etc.)

Si la tarea es animar, **también `video-animation`**.

**NO planees ni ejecutes hasta haber leído**: CLAUDE.md + **sport-choice PAUTA-MASTER.md (COMPLETO)** + sport-choice INGENIERO-PAUTA-MASTER.md + la MECÁNICA agnóstica de `choice-format-core/CHOICE-MECHANIC.md` (+ `INGENIERO-CHOICE-CORE.md` si la tarea es técnica) + video-log.md + este SKILL.md + el sub-doc de tu tarea.

---

## Qué es este skill

Este skill encodea las **reglas, patterns y dirección creativa del formato sport-choice** — la versión deportiva del formato choice. El espectador vive una jugada decisiva de fútbol en POV: elige un jugador (= elige equipo), y luego recorre las compuertas (2-3 decisiones de juego reales por recorrido) cuyo desenlace es la gloria (gol, levantar la copa) o la humillación (fallar, perder, ser la burla en redes). El video muestra los DOS recorridos completos (el elegido + el del foil), uno y luego el otro.

Es **un GENRE skill (Capa B)**. El toolkit técnico general (TTS, image gen, SFX gen, motion, captions, render, QA, ensamblado HYBRID per-clip atomic) vive en `ai-video-production/` (Capa A). La mecánica estructural AGNÓSTICA del formato choice (hook dyad, countdown, decisiones, counterfactual, cliffhanger) vive en `choice-format-core/` (Capa A.5) — derivada de los 8 virales (vía horror) pero género-neutro — y se HEREDA. horror-choice y sport-choice son HERMANOS que heredan de ese núcleo común. Este skill construye encima de ambas capas y aporta SOLO el sabor sport.

## En qué difiere de horror-choice (la diferencia central)

| Dimensión | horror-choice | **sport-choice** |
|-----------|---------------|------------------|
| **Qué es la elección del hook** | Elegir compañero/criatura (con quién pasás la noche) | **Elegir un jugador = elegir EQUIPO. Elegir = jugás PARA ese equipo.** |
| **Qué son las decisiones** | Curiosidad / obediencia / sumisión (encender luz, meter brazo) | **Jugadas reales de fútbol** (encarar/devolver, buscar ángulo/asistir, definir cruzado/picar) |
| **Qué es la consecuencia mala** | Body horror específico (taladro, ahogo, electrocución) | **Error futbolístico → la jugada se cae → el rival capitaliza → PIERDES y eres LA BURLA** (memes, redes, abucheos). NO muerte, NO horror. |
| **Qué es la consecuencia buena** | Sobrevivir + counterfactual cozy (café, cartas, amanecer) | **GOL → CAMPEÓN, levantar la copa, GLORIA, vuelta olímpica** |
| **Tono** | Uncanny, dread, sobrenatural | **Drama deportivo, tensión de final, humillación social** (sin nada sobrenatural) |
| **Personajes** | Criaturas uncanny inventadas (nombres reales inventados) | **Jugadores reales** (likeness foto-real descriptor-based) o jugadores ficticios |
| **Paleta SFX** | Drones, susurros, gritos de horror | **Rugido de hinchada, silbato, redes, cánticos, abucheos, atajada, confeti** (NUNCA gritos de horror) |
| **Counterfactual** | "Si hubieras elegido a X (bueno), habrías tomado café" | **El contraste entre los DOS recorridos completos** (ves las dos elecciones): el recorrido del foil es un viaje entero con su propio desenlace, no un cozy hogareño. ⤴ `PAUTA-MASTER.md § 4` + § 10.A |

**Lo que NO cambia (se HEREDA tal cual de `choice-format-core` — la mecánica agnóstica común a horror y sport):** POV 1ª persona >80%, hook con dyad simultánea + name labels GRANDES, decisiones binarias (2-3 internas por recorrido) con countdown 3-2-1 + loading bar + botones A/B, framing acción-condicional ("Si encaras / Si devuelves"), counterfactual placement, cliffhanger + CTA verbal, duración 80-100s, español neutral, captions Whisper word-timed, decision-UI editorial pacing, UI safe zones, lip-sync rule. (El narrador grave, watermark `@elige_tucompanero`, ensamblado HYBRID per-clip atomic y los 8 gates pre-render se heredan del pipeline universal `ai-video-production` + preferencias del creator.)

## Validado en

- **NINGÚN video shipped todavía** (HR#19: nuestras producciones NO son autoridad). El intento topical `champions-sport-choice` (+ `champions-arsenal-wins` / `champions-psg-wins`) **NO se shippeó** — falló por concepto rival/compañero roto + teleport-continuity (ver `video-log.md` #1 learnings). El diseño v0 + la capa operativa v0.2 existen para que la estructura esté lista ANTES de producir el próximo.

(Hasta tener ≥1 video shipped con buena retención + el OK de Tomás, sport-choice está en **fase de validación**: la mecánica heredada está probada, pero la lógica deportiva concreta se está validando empíricamente. Los hallazgos se loguean en `video-log.md` y se promoverán a PAUTA-MASTER cuando haya patrón observado.)

## Cuándo activar este skill

Activar cuando el usuario:

- Pide generar un guion/concepto del formato sport-choice (`SCRIPT-WRITING-GUIDE.md` + PAUTA-MASTER)
- Menciona fútbol/football + "elige tu compañero" / "elige tu equipo" / jugada / gol / penal / partido / Champions
- Pide prompts de imagen para jugadores o jugadas (`creative-direction/image-direction.md` — REGLA DE AMBIENTE)
- Quiere configurar timing, countdowns, botones de decisión deportiva (`creative-direction/ui-elements.md`)
- Presenta opciones A/B de jugadas y pide decidir (resolver contra PAUTA-MASTER, no preferencia personal)
- Valida un render contra el formato sport-choice

**Para cualquier tarea técnica concreta** (generar audio, imágenes, SFX, motion, captions, render, QA), activar también `ai-video-production`.

## Documentos en este skill

| Doc | Cuándo leerlo |
|---|---|
| **`SKILL.md`** (este) | Punto de entrada. Qué es sport-choice, diferencia con horror, hard rules del formato, qué se hereda. |
| **⭐ `PAUTA-MASTER.md`** | **Autoridad CREATIVA.** La historia/lógica: elección=equipo, ramas asimétricas, decisiones=jugadas, consecuencias=gol/burla, cadena de lógica, anti-patterns. |
| **⭐ `INGENIERO-PAUTA-MASTER.md`** | **Autoridad TÉCNICA.** Hereda lo universal + REGLA DE AMBIENTE + paleta SFX fútbol + consistencia de kits. |
| `SCRIPT-WRITING-GUIDE.md` | Cómo escribir un guion sport-choice (lente principio/variabilidad/anti-pattern). |
| `video-log.md` | Registro de videos producidos. Rotación obligatoria (pattern / setting / liga-equipos / tipo de jugada-clave). |
| `creative-direction/README.md` | Índice de docs operacionales + workflow del arquitecto sport-choice. |
| `creative-direction/script-writing.md` | La lógica narrativa sport (cómo se estructura el guion deportivo). |
| `creative-direction/image-direction.md` | ⭐ La **REGLA DE AMBIENTE** (orden visual del partido) + per-shot framework. |
| `creative-direction/audio-direction.md` | Paleta SFX fútbol + ambient de estadio + ducking. |
| `creative-direction/ui-elements.md` | Name labels de equipos, countdown, botones A/B de jugadas, watermark. |

## Qué se HEREDA (NO duplicar) vs qué es sport-específico

**SE HEREDA de `choice-format-core` (Capa A.5) + `ai-video-production` (Capa A) (NO duplicado en este skill):**
- **MECÁNICA estructural agnóstica** (estructura temporal, hook dyad sub-beats, invariante, decisión→consecuencia, framing acción-condicional, counterfactual placement, cliffhanger/CTA loop, POV >80%, patterns abstractos) → `choice-format-core/CHOICE-MECHANIC.md`.
- **Técnica choice-UI** (decision-UI editorial pacing, UI safe zones, caption chunking word-timed, lip sync rule, 0 cuts en hook) → `choice-format-core/INGENIERO-CHOICE-CORE.md`.
- **Rotación entre videos** (no repetir pattern/dyad consecutivo) → `choice-format-core/ROTATION-RULES.md`.
- **Técnica universal** (pace WPM, LUFS, mix, captions Whisper, HYBRID per-clip atomic, MODEL-CAPABILITIES-MATRIX, motion, mastering, 8 gates) → `ai-video-production/` (la apunta `INGENIERO-CHOICE-CORE.md`, no la duplica).
- `templates/scripts/` (tts.py, image.py, sfx.py, captions.py, video.py, los 8 gates, build_clip_atomic.py, etc.) → se heredan de `ai-video-production/templates/`.
- `effects-library/` → se hereda de `ai-video-production/templates/effects-library/` (transiciones, voice-effects). Los presets de voz de horror NO se usan; se usa narrador deportivo limpio.
- `canonical-scenes/` → ⚠️ sport-choice aún no tiene canonical-scenes propios. Hasta entonces se consultan los de `horror-choice-format/canonical-scenes/` **solo por su valor ESTRUCTURAL** (placement del counterfactual, framing acción-condicional, dyad, escalada de 3 decisiones, outro) — son refs virales HORROR-específicos, no de sport. Se derivarán los propios empíricamente de nuestros primeros videos.
- CREATIVE-SPEC schema (v11.1) → se hereda de `creative-director/templates/`.

**Es SPORT-ESPECÍFICO (vive en este skill):**
- La LÓGICA narrativa: elección=equipo, ramas asimétricas (corta gloriosa del foil + profunda interactiva), decisiones=jugadas reales, consecuencias=gol/gloria O error/burla, contexto explícito de equipo.
- La **REGLA DE AMBIENTE** (orden visual del partido en cada prompt de imagen/animación).
- La paleta SFX de fútbol (rugido, silbato, redes, cánticos, abucheos, atajada, confeti).
- La consistencia de identidad (kit propio vs rival siempre legible).
- Los anti-patterns deportivos cazados (no pasarle el balón al rival, orden hablado = orden de botones, consecuencia causalmente justificada, no contradicciones físicas, B no siempre correcta).

## Hard rules del formato (nunca romper)

> Para hard rules del toolkit general (variantes -a/-b/-c, capa SFX dedicada, motion AI, ensamblado HYBRID), ver `ai-video-production/SKILL.md` + CLAUDE.md. Para la MECÁNICA del formato choice (countdown, loading bar, framing condicional, counterfactual, POV), se HEREDA de `choice-format-core/CHOICE-MECHANIC.md` + `choice-format-core/INGENIERO-CHOICE-CORE.md` (Capa A.5 agnóstica, común a horror y sport). Estas son **específicas de sport-choice**:

1. **La elección del hook = EQUIPO.** Se presentan dos jugadores, uno de cada equipo. Elegir uno = jugás PARA ese equipo. **SIEMPRE dar contexto explícito** al viewer ("Si eliges a X, juegas para el equipo A; si eliges a Y, para el equipo B"). Esto resuelve de raíz la incoherencia rival/compañero. Ver PAUTA-MASTER § 1.
2. **DOS recorridos completos en UN video** (asimétricos por favorito): el recorrido JUGADO (el elegido) + el recorrido del FOIL (el contraste, tagueado `counterfactual_*`), cada uno con setup + compuertas (2-3 según favorito) + desenlace. Son SECUENCIALES (jamás interleaved); el orden entre ellos es 🟩 libre (el foil al inicio O al final — NO un "counterfactual opening fijo"); el foil NUNCA aparece en el played path. Ver PAUTA-MASTER § 4 + § 10.A.
3. **Decisiones = jugadas reales de fútbol** (compuertas — catálogo por posición POV en PAUTA-MASTER § 10.B). Consecuencias = 100% del partido: acertar → la jugada de gol avanza; errar → la jugada se cae → el rival capitaliza → PIERDES y eres LA BURLA. Ver PAUTA-MASTER § 5.
4. **SIN horror/sobrenatural.** Drama deportivo y humillación social, NO muerte, NO monstruos, NO body horror. Esta es la diferencia central vs horror-choice. Ver PAUTA-MASTER § 0 BAN + `NO-HORROR-GUARD.md`.
5. **NO pasarle el balón a un rival** (incoherencia futbolística). El compañero elegido + los de su kit son tu equipo; los del kit opuesto son obstáculos. Ver PAUTA-MASTER § 10 anti-patterns + § 10.C eslabón 2.
6. **Orden hablado = orden de botones** (si el narrador dice "encaras o devuelves", el botón A = encaras, B = devuelves). Ver PAUTA-MASTER § 10.
7. **Consecuencia causalmente justificada** (un pase seguro NO "pierde el balón"; una atajada implica un tiro AL arco, no afuera). Sin contradicciones físicas. Ver PAUTA-MASTER § 10 + § 10.C eslabón 7.
8. **Evitar que "B" sea siempre la correcta** (predecible). Rotar qué opción es la acertada entre decisiones y entre videos. Ver PAUTA-MASTER § 5.
9. **REGLA DE AMBIENTE** (técnica, pero load-bearing creativa): cada prompt UBICA la escena ANTES de la acción en orden — POV → zona del campo → geografía (arco, kits, balón, líneas) → estadio lleno → acción. Ver INGENIERO-PAUTA-MASTER § REGLA DE AMBIENTE + `creative-direction/image-direction.md`.
10. **Likeness de jugadores reales = descriptor-based**, NUNCA el nombre de celebridad literal en el prompt (los modelos t2i no reproducen personas reales nombradas; riesgo CP1). Ver PAUTA-MASTER § 5 + INGENIERO-PAUTA § consistencia.
11. **Heredadas inviolables del formato choice (de `choice-format-core` — comunes a horror y sport):** POV 1ª persona >80%, hook dyad simultánea con name labels GRANDES, decisiones binarias (2-3 internas por recorrido) con countdown + loading bar + botones, framing acción-condicional (NO bare label "Si elegiste A"), counterfactual placement, cliffhanger + CTA, duración 80-100s, español neutral, watermark `@elige_tucompanero`. Ver `choice-format-core/CHOICE-MECHANIC.md` (creativa) + `choice-format-core/INGENIERO-CHOICE-CORE.md` (técnica).

## Estado del formato

- **Fase:** validación (mecánica heredada probada en horror-choice; lógica deportiva PRE-EMPÍRICA — 0 videos shipped)
- **PAUTA-MASTER:** v0.2 operativa (diseño v0 + capa operativa § 10.A guion beat-a-beat / § 10.B catálogo de jugadas-compuerta por posición / § 10.C plantilla de cadena causal).
- **Videos shipped:** NINGUNO. El intento topical champions NO se shippeó (ver `video-log.md` #1). NO usar como autoridad (HR#19).
- **Referentes virales propios:** NINGUNO todavía. Se derivarán empíricamente de nuestros primeros videos (igual que horror-choice se derivó de 8 virales). Hasta entonces, la autoridad estructural se hereda de `choice-format-core` (la mecánica agnóstica validada — derivada de los 8 virales vía horror) + la lógica deportiva se documenta en PAUTA-MASTER como diseño + se ajusta con cada video logueado en `video-log.md`.
- **Pending:** shippear video #1 + recolectar ≥3 videos para derivar canonical-scenes propios de sport-choice + escribir patterns deportivos empíricos.
