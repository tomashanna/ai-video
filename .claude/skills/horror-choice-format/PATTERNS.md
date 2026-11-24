# PATTERNS.md — Reglas del formato "Elige a tu compañero"

> ⚠️ **AUDIT 2026-05-13 PM — REGLAS NARRATIVAS PARCIALMENTE DESACTUALIZADAS.** Este doc se basaba en 3 videos antiguos (V1, V2, V3 con 6M/4M/2.4M views). La **autoridad creativa actual** es `PAUTA-MASTER.md` (8 videos virales canónicos en `/videosref_elige_tu_compa/`).
>
> **Reglas TÉCNICAS de este doc siguen válidas:**
> - § 1 V15 timing (intro 9s, loading bar 2.5s, countdown 0.5s/número, white flash 0.25s)
> - § 2 audio (LUFS, ducking, SFX layering)
> - § 3 visual (POV %, transitions)
> - § 8 mecánica de elección
> - § 10 HTML/CSS implementación
>
> **Reglas NARRATIVAS de este doc están desactualizadas — usar PAUTA-MASTER:**
> - § 4 "bueno aparente no tiene diálogo" → **falso**: ref-08 Hugo SÍ habla "No me elijas". NO es regla estricta.
> - § 4 "bueno aparente solo en cliffhanger" → **falso**: 8/8 lo muestran en H1 presentación dyad.
> - § 4 "bueno = menos amenazante visualmente" → **falso**: 7/8 son visualmente extreme también (Miro hexagonal, Teresa dientes afilados).
> - § 6 "opción ganadora SIEMPRE contra impulso primario" → **falso**: ref-09 Victor obedecer = ganadora (procedural-aligned).
>
> **Para ejemplos empíricos auténticos de los 8 canónicos, ver `PAUTA-MASTER.md` §§ 7-13.** Los ejemplos en este doc usando HUGO/SANTI/Cristóbal/Gerald/Kevin/Rurik/Samuel son de **nuestras producciones, NO de los 8 canónicos**.

> Síntesis accionable del análisis de los 3 videos virales de @referent-a (V1: 6M views, V2: 4M, V3: 2.4M). ⚠️ Estos 3 videos NO son los 8 canónicos actuales — son referentes antiguos del mismo creator. Para autoridad empírica, usar PAUTA-MASTER.

> ⤴ **MECÁNICA AGNÓSTICA DEL FORMATO CHOICE AHORA EN `choice-format-core/`.** La mecánica genérica (estructura temporal/INTRO timing, lógica del dilema + plot-twist coherente 3-condiciones, mecánica de elección interactiva: loading bar / white flash / separador de rama) se extrajo a `../choice-format-core/CHOICE-MECHANIC.md` (creativa) + `../choice-format-core/INGENIERO-CHOICE-CORE.md` (técnica choice-UI). **Este doc queda como las reglas TÉCNICAS APLICADAS a horror + todo el contenido horror** (audio/visual de terror, arquetipos, lenguaje, cliffhanger sensorial, HTML/CSS, Kling-horror, prohibiciones). Las secciones con puntero `⤴` cross-linkean a core; **ningún cuerpo de sección se borró** (este doc está muy cross-referenciado).

---

## 1. ESTRUCTURA TEMPORAL

> ⤴ **El esqueleto temporal agnóstico + el timing del hook viven en `../choice-format-core/CHOICE-MECHANIC.md § 2` + `../choice-format-core/INGENIERO-CHOICE-CORE.md § 5` (0 cuts en hook).** Acá quedan los detalles de timing V15 horror (intro 9s, loading bar 2.5s, countdown, white flash) como receta APLICADA.

### ⭐ V15 (moderna — post mina-abandonada 9.9/10) — DEFAULT

Estructura optimizada para retención agresiva tras aplicar `ai-video-production/RETENTION-RULES.md`. Aplica a Reels / TikTok / IG Reels modernos.

| Hito | % video | Acción | Doc detallado |
|------|---------|--------|---|
| Frame 0 | 0% | Teaser visual (empty location + ominous element) + caption Whisper-sync inicia | `INTRO-FORMULA.md` |
| Hook visual completo | 0-3% | Personajes materializan vía Kling end_image (NO cut) | `INTRO-FORMULA.md` § Assets |
| Labels personajes | 3-6% | HUGO/SANTI visibles 2.5s con drop shadow uniforme | `INTRO-FORMULA.md` |
| Question caption | 5-7% | "¿CON QUIÉN BAJARÍAS?" (1s) | `INTRO-FORMULA.md` |
| Countdown | 6-8% | 3-2-1 (0.5s c/u) + 3 ticks | `INTRO-FORMULA.md` |
| Flash + bridge | 8% | White flash 0.25s. NO cap-chose (Whisper cap-h3-n1 carry el bridge) | `INTRO-FORMULA.md` |
| Setup escenario | 10-25% | Story arranca — narrador h3-narr1 + Whisper captions sync | – |
| Primera elección | 25-30% | Loading bar 2.5s con "AHORA DECIDE" | § 8 abajo |
| Primer twist | 30-50% | Hard cut + white flash + SFX al frame 0 | § 8 abajo |
| Segunda elección | 50-60% | Loading bar 2.5s | § 8 abajo |
| Segundo twist | 60-65% | Hard cut + white flash | § 8 abajo |
| Resolución horror | 65-85% | Si elegiste bien: salida con vida. Si mal: muerte detallada | – |
| Bridge cliffhanger | 85-87% | "Y si hubieras elegido a [BUENO]..." (caption amarillo cálido) | – |
| Cliffhanger | 87-95% | Bueno aparente en paz cotidiana, warm tint activo, música dawn | § 7 abajo |
| CTA final | 95-100% | "¿Sobreviviste? Comenta A o B" + CTA voz | § 7 abajo |

**Constantes duras V15:**
- Intro completo en **9s** (10% de un 90s, 12% de un 75s, 6% de un 60s)
- Loading bar siempre **2.5 segundos absolutos**, no proporcional
- White flash en cada twist: **0.25s fade-out** (anteriormente 2-3 frames, ahora más cinematic)
- SFX impacto sincronizado al **frame 0** de la nueva escena, sin delay
- Countdown **0.5s por número** (NO 0.3s — validado en v13 que se siente atropellado)
- Labels visibles **mínimo 2.5s** (NO 1.5s — viewer no alcanza a leerlos)
- **NO cap-chose post-countdown** — Whisper cap-h3-n1 carry el "SI ELEGISTE A [MALO]" bridge

### Estructura V1 legacy (para referencia histórica)

V1 original (@referent-a 2024-2025) tenía hold de presentación 15-17s (17%). Era el estándar pre-retención agresiva.

**Por qué cambió a 9s en v15**:
- Reels/TikTok scroll speed acelerado en 2026
- Hold >10% del video aumenta bounce a los 3-5s
- Hook visual + caption en frame 0 reemplaza la necesidad de "construir tensión lenta"

**Si usas V1 legacy**: solo si el delivery es YouTube Long (16:9, >3min) y querés tono "documental". Ver `formats/youtube-long.md`.

| Hito V1 legacy | % video | Acción |
|------|---------|--------|
| Frame 0 | 0% | Imagen estática presentación + ELIGE A TU COMPAÑERO + nombres |
| Hold presentación | 0-17% | 15-17s SIN movimiento — para que viewer escanee personajes |
| Cuenta regresiva | 17-21% | 3-2-1 con sonido proyector |
| Setup escenario | 21-37% | Establecimiento + primera advertencia |
| Primera elección | 37-39% | Loading bar 2.5s |
| Primer twist | 39-55% | Hard cut + flash |
| Segunda elección | 55-58% | Loading 2.5s |
| Segundo twist | 61% | Hard cut + flash |
| Tercera elección | 70-78% | Opcional |
| Resolución | 78-95% | Outcome del path elegido |
| Cliffhanger | 95-100% | "Si hubieras elegido a [BUENO]..." |

**Constantes duras V1 legacy:**
- Loading bar 2.5 segundos absolutos
- White flash 2-3 frames @ 30fps (66-100ms)
- SFX al frame 0 sin delay

---

## 2. AUDIO — REGLAS NO NEGOCIABLES

**Voz del narrador:**
- Hombre, 30-40 años, susurro grave
- Grabada a **2-5cm del micrófono** (efecto "voz en tu cabeza")
- EQ: bass boost 80-150Hz, recorte de agudos sobre 12kHz
- Compresión: ratio 4:1 a 6:1 con makeup gain alto
- Reverb: dark room, decay <0.6s, pre-delay mínimo
- Velocidad: pausada, con pausas de 1-2 segundos antes de cada revelación

**Música:**
- Drone ambiental sin BPM definido
- Layers de 30-45s en loop sin crossfade perceptible
- Frecuencias dominantes en sub-bass (50-120Hz)
- Ducking de **-5 a -7dB** cuando entra la voz

**SFX obligatorios (mínimo):**
- Click de proyector de cine en cada countdown
- Riser que empieza al final de cada pregunta y termina exactamente cuando la loading bar llega al 100%
- Risers terminan SIEMPRE en impacto seco o silencio súbito (nunca fade out)
- Glitch digital antes de cada twist (10 frames antes del corte)
- Sub-bass hit en cada hard cut de twist

**Cortes narrativos audio-led (regla nueva 2026-05-10):**

El narrador dicta cuándo cortar. Cada frase/idea del narrador es una "habitación visual" separada de las otras por **negro + audio específico** (no flash blanco para TODO). Hay 7 tipos de corte con audio + duración propia:

| Tipo | Cuándo se usa | Duración negro |
|---|---|---|
| WHITE FLASH | Elección tomada (cliff fork) | ~0.15s blanco |
| BLACK + LOW THUD | Entrada rama mala | 0.3–0.5s |
| BLACK + DRONE BAJO | Sostener muerto/atrapado | 0.4–0.8s |
| BLACK + RISE DRONE | Transición rama mala → buena | 0.4–0.6s |
| BLACK + EXHALE | Entrada rama buena (alivio) | 0.2–0.4s |
| BLACK + PUNCT SILENCE | Pausa entre nominales | 0.15–0.30s |
| WARM WHITE | Transición al cliffhanger | 0.3–0.5s |

**Por qué importa**: el espectador entiende la historia por el RITMO, no por las imágenes. Cada negro = punto-y-aparte narrativo que le dice "esto fue rama A, esto fue rama B, esto es la realidad". Sin negros + audio variado, el video se siente lineal/atropellado.

**Validado** en bosque-abandonado v2-final (lo aplica orgánicamente — Gemini lo identificó como su mayor fortaleza). NO aplicado en mina-abandonada v6 — todos los cortes son white flash + corte directo, por eso se siente lineal.

Implementación completa: `../ai-video-production/NARRATIVE-LED-EDITING.md`.

**Capa SFX por escena (regla V8-2 — perenne):**

Música + narración + ticks de countdown **no es sound design**. Es "narrador con música". Para que el video se sienta cine, cada escena necesita SFX granulares:

| Tipo de plano | SFX requeridos |
|---|---|
| POV caminando | footsteps en el material correcto (leaves/gravel/wood); pasos secundarios fuera de sync en momentos de "perseguido" |
| Close-up rostro tenso | breath/exhale puntual, micro-rustle de ropa, ambient room tone |
| Build-up al twist | drone ascendente sub-bass, tension rise |
| White flash twist | flash impact = sharp crack + sub-bass boom (volume 0.55-0.65) |
| Consecuencia malo | impacto físico de la consecuencia (body fall, grip, glass shatter) |
| Consecuencia bueno | release exhale, ambient warm pad bajo |
| Cliffhanger fogata | fire crackle loop, group laughter distant, single acoustic chord, dawn birds |

**Capa ambient continua (regla V8-2 — perenne):**

Por debajo de toda la sección horror: forest wind o industrial drone en `volume 0.10-0.18`. Por debajo del cliffhanger cálido: dawn warmth ambient en `volume 0.12-0.18`. No reemplaza la música — coexiste por debajo como sub-suelo sónico.

**Generación:** ElevenLabs Sound Effects con `loop:true` a 22s, expandido a duración objetivo con ffmpeg `stream_loop`. Ver `PRODUCTION-PIPELINE.md` § 12.5. **No requiere Freesound** — EL maneja todos los casos del workflow estándar.

**Master:**
- LUFS objetivo: **-9.5 a -10.0** (mezclado para feed de Instagram, sonido denso)
- Brickwall limiting en la voz para que no se pierda contra sub-bass

---

## 3. VISUAL — REGLAS NO NEGOCIABLES

**Composición:**
- Presentación: simétrica, dead-center, dos personajes flanqueando el eje vertical
- Resto del video: POV (primera persona) en >80% de los planos
- Plano medio largo en presentación; primer plano en momentos de amenaza directa

**Variedad visual obligatoria (regla V8-1 — perenne):**

Cualquier escena que ocupe >4s totales en el video DEBE tener **2-3 variantes** de imagen con sufijos `-a`, `-b`, `-c`. Cambiar ángulo / distancia / pose / framing — NO escenario.

| Duración total de la escena | Variantes mínimas |
|---|---|
| ≤ 4s | 1 |
| 4–8s | 2 PLANOS DISTINTOS (no variantes — ej: wide + close-up detalle) |
| > 8s | 3 PLANOS DISTINTOS (wide + close-up rostro + close-up detalle) |
| > 15s | 4-5 PLANOS DISTINTOS (agregar lateral/picado/ambiental) |

**Aprendizaje crítico (mina-abandonada v1, 2026-05-10)**: una versión vieja de esta regla decía "cambiar ángulo/distancia/framing". Produce slideshow disimulado — Gemini Video Analyzer no lo detecta, pero el espectador humano sí ("varias imágenes diferentes pero iguales"). La regla correcta es **cambiar el TIPO DE PLANO** (wide / close-up rostro / close-up detalle / lateral / picado / contra-picado / POV manos / ambiental), no el framing del mismo plano.

Mantener constantes entre planos: escenario, personajes, paleta. Cambiar: qué muestra el plano (sujeto, encuadre, lente, perspectiva).

Reutilizar el mismo PNG produce slideshow. Detectado en bosque-abandonado v2 ("PowerPoint narrado") + mina-abandonada v1 ("imágenes diferentes pero iguales"). Implementación completa: `../ai-video-production/IMAGE-VARIETY.md`.

**Color grading:**
- Bleach bypass con alto contraste
- Negros aplastados (crushed blacks)
- Desaturación general
- Tinte frío predominante (teal/azul/verde institucional según escenario)
- Paleta cálida (ámbar, dorado) **únicamente** en cliffhanger final

**Iluminación:**
- Diegética siempre (luces del entorno: fluorescentes, fuego, paneles)
- Niebla volumétrica densa en escenarios industriales
- Sombras profundas, dirección cenital o lateral dura

**Post-procesado constante:**
- Grain de medio tamaño en TODO el video
- Vignette sutil
- Chromatic aberration visible en bordes
- Motion blur en escenas de acción
- Distorsión de barril ligera (simula lente real)

**Tipografía:**
- Familia: pixelada 8-bit estilo "VCR OSD Mono" o "Press Start 2P"
- Color: blanco #FFFFFF con drop shadow negro
- Transformación: TODO MAYÚSCULAS
- Tracking ligeramente aumentado
- Posición: nombres en tercio superior cerca de cabezas; narración en tercio inferior centrado
- Animación: **HARD CUT siempre, nunca fade ni slide**

---

## 4. PERSONAJES — ARQUETIPOS FIJOS

El formato siempre tiene exactamente 2 personajes con roles invertidos:

**EL "MALO APARENTE" (Mentor Cruel):**
- Visualmente monstruoso, alto, deforme
- Es el peligroso pero también el que premia decisiones correctas
- Tiene línea de diálogo propia (críptica, autoritaria)
- Función narrativa: **somete al espectador a pruebas con reglas estrictas**
- NO es villano gratuito — es un sistema con lógica interna

**EL "BUENO APARENTE" (Distractor):**
- Visualmente extraño (puede ser tan extreme como el malo — ver `PAUTA-MASTER.md` § 5)
- Diálogo según apariencia (variabilidad, NO regla: ref-08 Hugo SÍ habla "No me elijas")
- **INVARIANTE (5/5 refs): NUNCA en el recorrido jugado tomando decisiones — solo en hook (H1 dyad) + counterfactual + cliffhanger.** Ver `PAUTA-MASTER.md` § 2
- Función narrativa: **representa la paz que el espectador rechazó por prejuicio visual**

**Contraste obligatorio:**
- Forma orgánica vs forma geométrica
- Color oscuro vs color claro (o viceversa)
- Vertical vs horizontal en proporciones
- Movimiento vs quietud

---

## 5. LENGUAJE — PATRONES SINTÁCTICOS

**Largo de oración:**
- Promedio: 5.4 palabras
- 45% son oraciones de 1-3 palabras
- 40% son de 4-7 palabras
- 15% son de 8+ palabras (solo descripciones de ambiente o cliffhanger)

**Tipos de oración requeridos:**
- **Imperativas:** "Elige a tu compañero", "Ahora decide", "Demuéstralo"
- **Nominales (sin verbo):** "Luz fría, pasillo vacío", "Reactor 1, Nivel -3"
- **Condicionales:** "Si X, [consecuencia en presente]"

**Tiempo verbal:**
- Presente de indicativo SIEMPRE en consecuencias ("trabajas", "quema", "mueres")
- NUNCA futuro ("trabajarás") — pierde inmediatez

**Persona:**
- Segunda persona implícita 90% ("trabajas", "eliges", "miras")
- Segunda persona explícita 10% solo en diálogos de personajes

---

## 6. LÓGICA DEL DILEMA MORAL — LA REGLA MÁS IMPORTANTE

> ⤴ **La dilemma-mechanics agnóstica vive en `../choice-format-core/CHOICE-MECHANIC.md § 5`** (lo universal es la DUDA real, no "ganadora contra impulso" — ⚠️ ese encabezado de abajo está REFUTADO por PAUTA-MASTER § 6 como no-universal; queda por valor histórico). Acá quedan los ejemplos horror.

> **El sistema premia obediencia, no virtud. La opción ganadora siempre va contra el impulso primario.**

| Impulso primario (PERDÉS) | Opción ganadora (GANÁS) |
|---------------------------|-------------------------|
| Mentir para salvarse | Decir la verdad incómoda |
| Saltar al rescate | Activar la alarma (acción mediada) |
| Pedir irse | Quedarse sentado |
| Resistirse físicamente | Esperar |
| Encender la bengala (curiosidad) | Quedarse a oscuras (obediencia) |
| Quitar máscara por la fuerza | Esperar a que él decida |

**Por qué importa:** sin esta regla, una IA generaría dilemas obvios tipo "¿matás al malo o no?" que son binarios morales triviales y no producen el "twist psicológico" del formato. El espectador debe **descubrir tarde que su instinto era el equivocado**.

**Categorías válidas de dilema:**
- Honestidad vs mentira propia
- Acción vs pasividad
- Curiosidad vs obediencia
- Violencia vs confianza
- Sumisión a instinto vs resistencia estoica

**Test de calidad del dilema — LA TENTACIÓN DEBE SER GENUINAMENTE DESEABLE:**

> Preguntate: ¿el espectador promedio realmente querría hacer la opción "mala"? Si la respuesta es "no obvio", el dilema es débil.

| ❌ Tentación débil | ✅ Tentación real |
|-------------------|------------------|
| Carne cruda (nadie la quiere) | Carne asada (huele bien, da hambre) |
| Atacar a un monstruo (miedo anula el impulso) | Devolver la mirada a algo que te mira fijo (instinto de dominancia) |
| Saltar a agua helada | Encender una luz en la oscuridad (alivio del miedo) |

La tensión no viene de la regla — viene de que el espectador *realmente quería hacer lo incorrecto* y se lo negaron. Si la opción "mala" ya repulsa antes de la consecuencia, el twist no tiene impacto.

### ⚠️ Excepción de la matriz expandida (2026-05-13)

La regla "opción ganadora va contra impulso primario" **asume apariencia asimétrica + verdad invertida** (el monstruoso es realmente bueno, el amable es realmente malo). Esto cubre Patterns 4, 6, 10 (oficiales 3.1, 3.2, 3.3).

En los **patterns nuevos sin twist** (1, 2, 3, 5, 7, 9), la regla NO aplica de la misma forma. El motor narrativo cambia:

| Pattern | Motor de tensión (NO es "contra impulso") |
|---|---|
| 1 — Verdad visible | Setup que genera **duda artificial** antes de revelación obvia (el video te hace dudar de tu instinto correcto) |
| 2 — Paz neutral | Lección de calma — no hay tensión por dilema, hay tensión por **expectativa rota** (el viewer espera horror que no llega) |
| 3 — Apariencias engañan dobles | Tensión por **prejuicio del viewer** — ambos se ven peligrosos, pero el video revela que el prejuicio era erróneo |
| 5 — Doble peligro visible | Tensión por **fatalismo** — no había opción correcta, ambos matan |
| 7 — Trampa cordial doble | Tensión por **falta de señal visual** — el viewer no tiene prejuicio que lo guíe |
| 9 — Distinción entre horrors | Tensión por **detalle sutil** — ¿qué diferencia al monstruo bueno del malo? |

Para esos patterns, validá la calidad del video con: (1) **¿el motor de tensión correspondiente está bien construido?** (2) **¿el cierre cierra el motor?** (3) **¿el viewer puede explicar el video en una frase?**.

---

## 6.5. ⛔ PLOT TWIST — uno de los pilares del formato

> ⤴ **Las 3 condiciones de coherencia del plot twist (lógica + imágenes + narración) son agnósticas y viven en `../choice-format-core/CHOICE-MECHANIC.md` (dilemma-mechanics + twist coherence).** Acá quedan los ejemplos horror del twist + su aplicación al formato de terror.

> Aplicación específica del principio universal de `video-director/SKILL.md` § Filosofía #8 al formato horror-choice.

### Regla 1 — Rotación de combinaciones obligatoria (plot twist es opcional)

> **Cambio 2026-05-13**: el plot twist dejó de ser obligatorio. La regla anterior decía "plot twist obligatorio en casi todos los videos" — diluía la variabilidad porque forzaba siempre el mismo arco emocional (sorpresa por engaño). Ahora el director rota entre **10 patterns apariencia × verdad** (ver `PAUTA-MASTER.md` § 15 patterns observados). Algunos patterns incluyen plot twist, otros no — la variedad importa más que el twist.

**Regla operativa actual:**

1. **Rotación obligatoria**: nunca repetir la misma combinación apariencia × verdad dos videos seguidos. Consultar `<formato>/video-log.md` al inicio del bootstrap para verificar.

2. **Plot twist es un recurso, no requisito**. Está disponible para los patterns 3, 8, 9, 10 + cualquier meta-cliffhanger (`PAUTA-MASTER.md` § 13 (cliffhanger archetype)). En patterns 1, 2, 4, 5, 6, 7 el motor narrativo es la calidad del dilema interno (§ 6), no la sorpresa.

3. **Si el director elige un pattern CON plot twist** — aplican las Reglas 2 y 3 abajo (timing setup + 3 condiciones coherencia).

4. **Si el director elige un pattern SIN plot twist** — Reglas 2 y 3 NO aplican. Pero la calidad del dilema moral (§ 6) sí, y los anti-patterns del formato (verbos en presente, no fade entre captions, etc.) también.

**Tipos de plot twist validados** (cuando aplica):
- **Revelación de rol invertido** (Pattern 10): el "monstruoso" era guardián, el "amable" era trampa.
- **Revelación de apariencias engañan ambas** (Pattern 3): ambos visualmente monstruosos resultan genuinos.
- **Revelación retrospectiva** (Pattern 8 o 9): un detalle desde H1 cobra significado nuevo en H6.
- **Revelación de identidad** (Meta-cliffhanger § 3.4): el viewer descubre algo sobre sí mismo.
- **Revelación temporal** (Meta-cliffhanger variante): lo que parecía "ahora" era "hace años".

### Regla 2 — Timing de elementos del plot twist (NO confundir con detail shots)

Los elementos visuales que sirven al plot twist tienen **reglas de timing distintas** a los detail shots normales. Esta categoría es invisible en AUDIT.md por defecto — el agente puede pasar el lint y aún así romper el twist por timing insuficiente.

| Tipo de elemento | Rol narrativo | data-duration | Caption acompañante |
|---|---|---|---|
| **Setup element** | Planta semilla del twist (ej: foto vieja en H3 que se cobra en H6) | **2.5-3.5s mínimo** (idealmente 3.0-3.5s) | Caption sutil sincronizado ("Algo familiar.") que confirma el feeling sin explicar |
| **Payoff element** | Cobra el twist (ej: close-up termo con iniciales en H6) | 2.0-3.0s | Caption explícito que cierra el gap lógico |
| **Transición revelación** | Cut entre setup y payoff dentro del twist (ej: foto detail → Marco rostro) | 1.5-2.0s | Sin caption (la imagen habla) |
| **Detail shot normal** | Refuerzo visual no-narrativo | 1.5-2.5s | Opcional |

**Por qué los setup elements necesitan más tiempo**:

El viewer necesita 2.5s+ para procesar inconscientemente un elemento que va a tener payoff retroactivo. Bajo 2.5s la imagen es **vista** pero NO **procesada**. Cuando llega el payoff, no hay memoria que recuperar → el twist falla aunque el setup esté ahí técnicamente.

Fases mentales del setup (suman 2.5-3.5s):
1. Notar (0.4-0.6s) — el ojo encuentra el elemento en el frame
2. Reconocer (0.8-1.2s) — "es viejo, alguien con un termo"
3. Leer caption (0.5-0.7s) — "Algo familiar" confirma verbalmente
4. Incomodidad sin entender (0.5-1.0s) — "¿esto debería significar algo?"

**Anti-pattern detectado en cabana-tormenta v4 (2026-05-13)**:

La foto del padre en H3 estaba <1s porque el agente productor confundió "show don't tell" (no narrar explícitamente) con "mostrar rápido". Son cosas distintas: *show don't tell* = sin narración explicativa. *Setup element timing* = tiempo en pantalla suficiente para procesar. Las dos reglas son ortogonales.

Resultado: el twist H6 falló retroactivamente porque el viewer nunca registró la foto en H3. Fix en v5: extender la foto a 3.0-3.5s.

**Cómo aplicarlo al draftear NARRATIVE.md**:

Antes de wire un elemento al HTML, preguntate:
- ¿Este elemento se cobra después en el video? → Setup element, 2.5-3.5s
- ¿Este elemento ES la revelación? → Payoff element, 2.0-3.0s
- ¿Es solo refuerzo visual? → Detail shot normal, 1.5-2.5s

NO uses la regla genérica "imágenes >2s, detail shots 1.5-2.5s" para setup elements. Esa regla aplica a planos sin función narrativa retroactiva.

### Regla 3 — Las 3 condiciones de coherencia (sino el twist falla)

Todo plot twist DEBE cumplir 3 condiciones simultáneamente:

### Las 3 condiciones del plot twist coherente

1. **Lógica clara** — el viewer puede explicar el twist en una frase tras ver el video. Si queda con "¿pero por qué eso era una trampa?" → el twist falla.

2. **Imágenes acompañan** — visual evidence del twist en el frame, no solo narrado. El elemento que revela el twist debe ser **visualmente identificable** y conectado al evento anterior. Ejemplo correcto: si el twist es "el termo era de tu padre", el termo debe mostrarse con iniciales / detalle distintivo que lo conecte — no basta con narrar "reconoces el olor".

3. **Narración explica el link** — 1 frase explícita que cierre el gap lógico. NO asumir contexto. Ejemplo correcto: *"Mismo termo. Mismas iniciales. Tu padre subió en 1987 y nunca bajó."* Ejemplo incorrecto: *"Reconoces el olor"* (vago, asume que el viewer conecta solo).

### Aplicación al formato horror-choice

| Hito | Tipo de twist | Condiciones a chequear |
|---|---|---|
| H3 — Primer twist (revelación tipo de personaje) | Visual + narrativo | Imágenes del "malo aparente" deben mostrar señal NUEVA que confirme su rol (cristales en boca, ojos lechosos, etc.). Narración: 1 frase que conecte la señal con la acción del viewer. |
| H4-H5 — Twist intermedio | Sensorial + decisivo | Imágenes deben mostrar consecuencia inmediata (dedo de hielo, vapor, marca). Narración: causa-efecto explícito. |
| H6 — Cliffhanger trampa-amable (más complejo) | Revelación retrospectiva | El elemento de la trampa amable debe verse claramente (termo, taza, llave) Y conectar con el pasado del viewer en 1 frase narrada. Sin ambos elementos, el viewer queda confundido. |

### Caso real validado — cabana-tormenta v2 (PROBLEMA detectado)

El cliffhanger H6 reveló que "el café era el mismo que el padre del viewer" pero:
- ❌ Las imágenes NO mostraban iniciales en el termo claras
- ❌ La narración decía "reconocerías el olor" (asume conexión emocional sin evidencia)
- ❌ El viewer queda con "¿por qué eso me atrapa?" en vez de "¡el padre también cayó en la trampa!"

Resultado: usuario reportó "el final del video confunde" tras render aprobado por Gemini. Gemini no detectó la incoherencia porque el contenido CSS+narración pasaba sus heurísticas — pero la lógica narrativa fallaba.

### Fix para próximos videos

Al draftear NARRATIVE.md del cliffhanger:

1. Escribir el twist en una frase: "El viewer descubre que [X CONECTA CON Y POR Z]."
2. Listar la evidencia visual obligatoria: imágenes que el viewer DEBE ver para conectar X con Y.
3. Listar la narración obligatoria: 1 frase explícita que cierre el gap (no metáfora, no asumir contexto).
4. Antes de generar assets, leer el twist en voz alta y preguntarte: "¿un viewer sin contexto previo podría explicarme esto en una frase?".
5. Si la respuesta es "no" → reescribir.

### Cómo lo detecta el QA Gemini extendido (post-2026-05-13)

Agregar al prompt Gemini específico del formato:
```
Dimensión Plot Twist Coherence:
- ¿El plot twist del cliffhanger se entiende sin contexto previo?
- ¿Las imágenes muestran evidencia visual del twist (no solo narrado)?
- ¿La narración explica explícitamente el link entre el setup y el twist?
- ¿Un viewer puede explicar el twist en una frase post-video?
Score 1-10 esta dimensión específicamente.
```

Si esta dimensión saca <9, **iterar guion + assets de evidencia + narración**. NO fixear con motion o Kling — es problema de información, no de animación.

---

## 7. ESTRUCTURA DEL CLIFFHANGER

**Plantilla literal:**
> "Si hubieras elegido a [BUENO_APARENTE], habrían [ACCIÓN_COTIDIANA_PAZ] juntos, en silencio, mirando [ELEMENTO_NATURAL] al [TIEMPO_DEL_DÍA]. Una noche en paz."

### Puente narrativo antes del cliffhanger (regla V7)

Antes del white flash que abre el cliffhanger, mostrar una caption breve (~1.5s) sobre la última imagen de la rama Cristóbal: **"Y SI HUBIERAS ELEGIDO A [BUENO_APARENTE]..."** en color cálido (#f5d9a0 dorado pálido). Esta caption hace de **reset mental** — el espectador deja la rama horror antes de aterrizar en la rama paz. Sin el puente, la transición se percibe como "glitch" o cambio de tema. Detectado por Gemini en V6 ("transición abrupta") y resuelto en V7 ("transición excelente").

### CTA de engagement (regla V7)

Los últimos 2-2.5 segundos del cliffhanger DEBEN incluir un CTA que pregunta al espectador qué eligió. Plantilla:

> "¿SOBREVIVISTE? 💬 COMENTA A o B"

Font-size ~60px (más chico que las captions de 80px porque incluye emoji), uppercase. Fuerza interacción → mejora la distribución del algoritmo de Instagram. No es opcional: V6 no tenía esto y Gemini lo señaló como gap; V7 lo incluyó.

**Elementos sensoriales obligatorios (elegir 2-3):**
- Comida caliente / café / caramelos
- Vista al exterior (océano, estrellas, montañas)
- Tiempo del día con resonancia emocional (amanecer, atardecer)
- Sonido suave (canto de ballenas, viento, silencio)
- Acción de cuidado mutuo (vigilar juntos, comer, escuchar)

**Contraste tonal:**
- Color: cálido (ámbar/dorado) después de un video frío
- Música: resolución tonal a acorde mayor o silencio reverberante
- Velocidad: lenta después de un tercio final acelerado
- Personaje: cara normal/cálida después de versión amenazante

---

## 8. MECÁNICA DE ELECCIÓN INTERACTIVA — LA INNOVACIÓN DEL FORMATO

> ⤴ **La mecánica de elección agnóstica (loading bar, white flash, separador de rama A→B, decisión→consecuencia ✗/✓) vive en `../choice-format-core/INGENIERO-CHOICE-CORE.md` (técnica choice-UI) + `../choice-format-core/CHOICE-MECHANIC.md § 4` (dinámica).** Acá queda el sabor horror (glitch digital de terror + el impulso→muerte/castigo).

Esto es lo que diferencia "Elige a tu compañero" del horror narrativo común:

1. Aparece pregunta en pantalla con dos opciones (A y B)
2. Loading bar de 2.5s con texto "LOADING COMPLETED" o similar
3. Glitch digital 10 frames antes del corte
4. White flash 2-3 frames
5. Hard cut a la consecuencia A (impulso → muerte / castigo)
6. **SEPARADOR de rama** (regla V7 — NO OMITIR)
7. Hard cut a la consecuencia B (estoico → sobrevivís)
8. SFX impacto en frame 0 de cada nueva escena
9. La narración revela qué "eligió" el espectador (en realidad el creador eligió por él)

### Separador de rama A→B (regla V7 — crítica para comprensión)

Entre el outcome A (consecuencia mala) y el outcome B (consecuencia buena) el video DEBE incluir un separador visual breve. Sin él, el espectador percibe los dos outcomes como **secuenciales** ("primero pasa X, después Y") en lugar de **alternativos** ("si elegís X pasa esto, si elegís Y pasa lo otro"). Detectado por Gemini en V6 (score 7/10) y resuelto en V7 (score 9.5/10).

**Patrón obligatorio:**
1. Pulso oscuro suave en `#fade-out` (opacity 0 → 0.55 → 0, total 0.5s)
2. Caption corta con prefijo "SI [opción B]:" en color tenue (#c8d8ff azul claro), 1.2s
3. Recién después, el outcome B sobre su imagen

Texto del separador: imperativo corto que nombra la rama B literal — "SI BAJAS LOS OJOS:", "SI NO COMES:", "SI ESPERAS:". No la consecuencia, **la elección**.

Implementación técnica completa en `PRODUCTION-PIPELINE.md` sección 10.

**Criticidad de la sincronía:**
- Si el SFX llega 2 frames tarde, se pierde el efecto de "consecuencia inmediata"
- La loading bar debe terminar exactamente cuando termina el riser de audio
- El glitch debe preceder al corte, no coincidir con él

**Cantidad de elecciones:**
- V1 (6M views): 3 elecciones interactivas
- V2 (4M views): 2 elecciones
- V3 (2.4M views): 2 elecciones

**Correlación:** más elecciones = más views. El espectador "interactivo" se compromete más con el contenido.

---

## 9. DURACIÓN ÓPTIMA

Sweet spot observado: **90-100 segundos**.

- 80s (V3): demasiado corto para 3 elecciones, se siente apurado
- 90-100s (V1): permite 3 elecciones con setup adecuado
- 113s (V2): demasiado largo, pierde retención hacia el final

---

## 10. IMPLEMENTACIÓN HTML/CSS — REGLAS DE PRODUCCIÓN

Estas reglas son invariantes — romperlas produce bugs visuales que solo aparecen en el render final.

**Captions:**
- `white-space: normal` + `width: 960px` + `text-align: center` en `.caption` — si usás `nowrap`, las frases largas se cortan fuera de pantalla
- Frases de >8 palabras: reducir `font-size` a `68px` inline + `line-height: 1.1`
- **Stroke negro obligatorio (regla V7):** `-webkit-text-stroke: 1.5px rgba(0,0,0,0.7)` en `.caption`. Sin esto el texto blanco se pierde cuando el fondo tiene zonas claras (niebla, amanecer, fuego). Gemini detectó esta falla en V6.

**Choice labels A/B (regla V7):**
- `font-size: 64px` (NO 48px). El 48px era ilegible en móvil cuando el pulgar tapaba parte de la pantalla.
- `-webkit-text-stroke: 2px rgba(0,0,0,0.8)` obligatorio

**GSAP — ancla obligatoria:**
- Todo elemento que empiece invisible: `tl.set(el, {opacity:0, scale:1.0}, 0)` en t=0
- Sin esta ancla, HyperFrames hace pre-render del estado visible y aparece un flash al inicio
- Nunca usar `fromTo` para estados iniciales — mismo bug

**Audio:**
- Todo `<audio>` necesita atributo `id` o HyperFrames no lo reproduce
- Raw TTS nunca va al render — siempre procesar con `atempo=2.0`
- Reservar `data-track-index` 60–110 para la capa SFX (V8-2)

**Motion mínimo (regla V8-3 — perenne):**

Ningún plano queda estático >2s sin algún tipo de motion. **Ken Burns es el piso, no el techo.**

| Tipo de escena | Stack motion mínimo |
|---|---|
| Plano estático en general | Ken Burns (`scale 1.0 → 1.04`, ease sine.inOut) |
| Plano con profundidad (bosque, pasillo) | Ken Burns + parallax 3 capas |
| Close-up rostro tenso | Ken Burns + flicker exposición + handheld shake sutil |
| Build-up al twist | Vignette pulsante creciente |
| Twist + white flash | Glitch frame (1-2 frames displacement) antes del flash |
| Luz cálida (fogata, linterna) | Glow pulsante + partículas overlay |

Sin esta regla el video se siente diapositiva — Gemini lo señaló en bosque-abandonado v2 ("síndrome de PowerPoint"). Implementación completa en `PRODUCTION-PIPELINE.md` § 3.5.

**Render:**
- `hyperframes render .` (directorio) — NO `hyperframes render index.html` (falla)
- Si falla con `Target closed`: reintentar, es crash de Chrome por memoria, no error de código

Ver `PRODUCTION-PIPELINE.md` para comandos completos.

---

## 10.5. ANIMACIÓN CON KLING — overrides del formato

> Aplica la regla general de `../ai-video-production/ANIMATION-LAYER.md` con estos overrides específicos:

### H1 — Presentación de personajes: dos sub-patterns válidos

El plano de presentación de los dos compañeros (Berni vs Yonaiker, Hugo vs Santi, Cristóbal vs Gerald, Kevin vs Rurik) tiene una **estructura distinta del resto del video**. Hay 2 opciones — elegir UNA por video según el mood narrativo.

| Característica | Opción A — Atmospheric loop | Opción B — Character warning | Opción C — Character corporal ⭐ |
|---|---|---|---|
| Duración en pantalla | 7-10s | 12-18s (extiende H1) | 4-5s (h1) + 5s (h1-b) = 9s total |
| Audio adicional | – | Voz del "malo aparente" voice ID propio | – (solo narrador) |
| Kling | Tier 5s loopable | Tier 5s motion sutil hablando | 2 clips tier 5s — h1 atmospheric + h1-b corporal |
| Engagement | Medio | Alto (rompe 4ª pared) | **Alto (gestos físicos amplios)** |
| Costo | $0.35 | $0.70 (1 clip + TTS) | $0.70 (2 clips tier 5s) |
| Riesgo Kling | Bajo | Alto (boca uncanny) | Medio (manos pueden salir raras) |
| Validado en | – | elige-companero V1, V3 | **bosque-abandonado v7 (10/10 Gemini)** ⭐ |

#### Opción A — Atmospheric loop

La acción narrativa la hace SOLO el narrador diciendo los nombres. Los personajes están perfectamente quietos para que el espectador los escanee. Animación = solo entorno.

**Kling prompt template**:
```
Subtle [atmospheric element] between [character A] and [character B],
characters perfectly still no character motion,
[secondary atmospheric detail],
camera locked, atmospheric only, 5 seconds
```

Recetario por setting:

| Setting | Prompt |
|---|---|
| Bosque | `"Subtle fog drifting slowly horizontally between [A] and [B], dead leaves floating barely in the cold air, characters perfectly still, camera locked, atmospheric only, 5 seconds"` |
| Mina | `"Coal dust particles suspended in the headlamp beams between [A] and [B], faint flicker of carbide lamp, characters static motionless, camera locked, atmospheric depth, 5 seconds"` |
| Casa rural | `"Candlelight flickering subtly on [A] and [B] standing at the doorway, almost imperceptible breeze, characters perfectly still, camera locked, looping warm-cold atmosphere, 5 seconds"` |
| Hospital | `"Fluorescent light barely flickering above [A] and [B] in the corridor, dust motes in the light, characters motionless, camera locked, 5 seconds"` |

HTML:
```html
<video id="h1-characters" src="assets/h1-characters.mp4" class="scene-image clip"
       autoplay muted playsinline loop
       data-start="0" data-duration="10" data-track-index="0"
       style="opacity:1;"></video>
```

#### Opción B — Character warning (advertencia directa)

El "malo aparente" rompe la 4ª pared y le dice al espectador algo críptico que crea tensión inmediata. Validado en V1 (Kevin: "No soy la cabeza de Doritos y me llamo Kevin. No me elijas. No soy inocente.").

**Estructura temporal**:
1. **0-3s**: presentación estática + narrador "Elige a tu compañero. [A] o [B]." (igual que Opción A)
2. **3-7s**: ZOOM IN sobre el "malo" + voz propia (NO narrador) con warning críptico
3. **7-10s**: zoom-out volviendo a wide shot (transición al countdown H2)

**Audio adicional necesario**:
- Voz del "malo" con voice ID propio (NO el voice ID del narrador). Ver `.env.example` o `BOOTSTRAP-NEW-PROJECT.md` para voces validadas por personaje.
- Texto típico (4-8 palabras, en primera persona, autocondena):
  - "No me elijas. No soy inocente."
  - "Hace 30 años que cruzo este bosque. No deberías venir conmigo."
  - "Vas a ver lo que no quieres ver."
  - "Yo te lo dije."

**Kling prompts** (más cuidado — character motion):

```
Slow zoom-in toward [malo character]'s face from a wide shot,
character very slight motion only (slow eye glance toward camera, no lip sync),
[atmospheric detail],
camera move locked to subject, 5 seconds
```

Recetario:

| Setting | Prompt |
|---|---|
| Bosque (Berni) | `"Slow zoom-in toward Berni's gaunt face, his pupilless eyes turning very slightly toward camera, his thin smile holding steady, fog drifting behind him, camera move locked, 5 seconds"` |
| Mina (Hugo) | `"Slow zoom-in toward Hugo's gaunt face under his carbide helmet, his milky white eyes flickering toward camera, dust particles in the lamp beam around him, camera move locked, 5 seconds"` |
| Casa rural (Cristóbal) | `"Slow zoom-in toward Cristóbal's beetle head, mandibles barely twitching, candle light flickering on his chitinous face, eyes catching the light, camera move locked, 5 seconds"` |

**HTML pattern**:
```html
<!-- H1 wide shot (estático con Ken Burns) -->
<img id="h1-characters" src="assets/h1-characters.png" class="scene-image clip"
     data-start="0" data-duration="3" data-track-index="0" style="opacity:1;" />

<!-- H1 character warning (Kling zoom-in) -->
<video id="h1-warning" src="assets/h1-malo-warning.mp4" class="scene-image clip"
       autoplay muted playsinline
       data-start="3" data-duration="4" data-track-index="1"
       style="opacity:0;"></video>

<!-- H1 wide shot return (estático con Ken Burns reverse) -->
<img id="h1-characters-return" src="assets/h1-characters-b.png" class="scene-image clip"
     data-start="7" data-duration="3" data-track-index="2" style="opacity:0;" />

<!-- Voz del malo -->
<audio id="h1-warning-voice" src="assets/h1-malo-warning-2x.mp3"
       data-start="3.2" data-duration="3.5" data-volume="1.0" data-track-index="55"></audio>
```

**Captions del warning**: aplicar la misma regla — Whisper auto sobre el audio del malo, texto en color distinto del narrador (ej: rojo `#ff5050` para diferenciarlo).

#### Opción C — Character corporal motion ⭐ DEFAULT RECOMENDADO

Los personajes hacen GESTOS FÍSICOS AMPLIOS hacia la cámara (no atmospheric solo, no warning vocal). Es el sweet spot: motion claro que detiene el scroll, sin el riesgo de mouth-sync de B ni la sutileza aburrida de A.

**Regla de oro**: gestos hacia EL ESPECTADOR (cámara), NUNCA entre ellos. Si los personajes se miran o interactúan → spoilea el twist.

**Estructura temporal 9s** (igual mina-abandonada, validado en bosque-abandonado v7 = Gemini 10/10):

```
0-4s    h1 (Kling tier 5s, push-in atmospheric, breath vapor)
4-9s    h1-b (Kling tier 5s, motion corporal hacia cámara)
0.2-4.45s   narración "Elige a tu compañero, [A] o [B]."
0.7-4.0s    labels [A] / [B] arriba
4.5-5.4s    caption "¿CON QUIÉN CRUZARÍAS [setting]?"
5.5-8.5s    countdown 3-2-1 + ticks + loading bar (3s fill solapado)
8.5-9.0s    flash white → cut a H3
```

**Kling prompts** — gestos físicos amplios hacia cámara, NO interacción:

| Personaje | Acción corporal |
|---|---|
| "Malo aparente" (Berni/Hugo/Cristóbal) | extiende su objeto distintivo hacia la cámara (bastón, pico, mandíbulas) con sonrisa creepy expandiendo, mira fijo a cámara |
| "Bueno aparente" (Yonaiker/Santi/Gerald) | levanta su objeto cálido hacia la cámara (lámpara, foco, vela) con sonrisa warm + slight friendly head tilt hacia cámara |

**Prompt template h1-b** (corporal):
```
Two characters on [setting], both facing camera.
[MALO] (left) slowly raises/extends [creepy object] toward the camera in an inviting yet unsettling gesture, his unsettling smile widening, looking directly at camera with creepy intensity.
[BUENO] (right) lifts [warm object] up showing it warmly toward camera, gives a friendly head tilt toward viewer, warm reassuring smile widens slightly.
CRITICAL: Both gestures directed toward camera, NOT toward each other. Neither character looks at the other. No interaction between them.
[atmospheric detail]. Slow forward camera push-in. Cold blue night palette. No deformed hands, hands keep 5 fingers. 5 seconds.
```

**Prompt template h1** (atmospheric base):
```
[Atmospheric element] between two characters on [setting] at night, breath vapor exhaling subtly from both mouths, [secondary atmospheric detail], characters perfectly still with no body movement no facial expression change no eye blinks, very slow forward camera push along the path, cold blue palette, locked composition, 5 seconds.
```

**HTML 9s** (cableo exacto validado):

```html
<!-- H1 wide push-in (Kling tier 5s, scale 1.0→1.10) -->
<video id="h1-characters" src="assets/h1-characters.mp4" autoplay muted playsinline
  class="scene-image clip" data-start="0" data-duration="4" data-track-index="0"></video>
<!-- H1-b corporal motion (Kling tier 5s, scale 1.0→1.20 + camera shake) -->
<video id="h1-characters-b" src="assets/h1-characters-b.mp4" autoplay muted playsinline
  class="scene-image clip" style="opacity:0;" data-start="4" data-duration="5" data-track-index="16"></video>
```

**GSAP** (Ken Burns amplificado + camera shake durante countdown):

```js
// Ken Burns h1 + h1-b (escalas que SÍ se perciben — sin esto el motion Kling se ve aburrido)
tl.fromTo("#h1-characters", { scale: 1.0 }, { scale: 1.10, duration: 4.0, ease: "sine.inOut" }, 0);
tl.set("#h1-characters", { opacity: 0 }, 4.0);
tl.set("#h1-characters-b", { opacity: 1, scale: 1.0 }, 4.0);
tl.to("#h1-characters-b", { scale: 1.20, duration: 5.0, ease: "power1.in" }, 4.0);

// Camera shake durante countdown (5.5-8.5s) — handheld horror feel
tl.to("#h1-characters-b", { x: -4, duration: 0.08, repeat: 1, yoyo: true }, 5.5);
tl.to("#h1-characters-b", { x: 3, duration: 0.08, repeat: 1, yoyo: true }, 5.9);
tl.to("#h1-characters-b", { x: -3, duration: 0.08, repeat: 1, yoyo: true }, 6.5);
tl.to("#h1-characters-b", { x: 4, duration: 0.08, repeat: 1, yoyo: true }, 6.9);
tl.to("#h1-characters-b", { x: -5, duration: 0.08, repeat: 1, yoyo: true }, 7.5);
tl.to("#h1-characters-b", { x: 5, duration: 0.08, repeat: 1, yoyo: true }, 7.9);
tl.set("#h1-characters-b", { x: 0 }, 8.2);
```

**Hard rules para Opción C** (no negociables — validadas en v7):
1. **Duración Kling = data-duration HTML exacta** — si Kling es tier 5s, data-duration ≤ 5s. NO mostrar 7s de un clip de 10s o se pierde el motion final del clip.
2. **NUNCA gestos entre personajes** — solo hacia cámara/espectador. Pisar esta regla spoilea el twist (validado por descarte en v2 spoiler).
3. **Pre-render check de frames Kling ANTES de cablear HTML** — extraer frames a t=0.3, 2.5, 4.7 con ffmpeg y validar antes de invertir tiempo de render.
4. **NO caption "ELIGES A [A/B]"** — la loading bar fill ES la confirmación visual. Agregar caption solapa con A.BERNI/B.YONAIKER de la bar (validado en v3 → v4).
5. **Font híbrido**: Anton primary EXCEPTO `.caption` que usa Bebas Neue primary (HyperFrames descarga Anton sin latin-ext → Ñ/Í/Á fallback ugly. Bebas Neue tiene latin-ext completo).
6. **Camera shake solo durante countdown** (5.5-8.5s) — fuera de ese rango se siente excesivo.
7. **Ken Burns escalas mínimas**: h1 1.0→1.10, h1-b 1.0→1.20. Sin esto el motion Kling se ve "muerto" en pantalla (los `scale` 1.04-1.06 son imperceptibles).

### ⭐ Opción D — Teaser materialization (post-v15, RECOMENDADA por default)

Validada en mina-abandonada v15-final (9.9/10 Gemini). Usa Kling `start_image + end_image` para hacer 1 solo clip continuo donde el viewer parte de un teaser sin personajes y los ve materializar.

| Característica | Opción D — Teaser materialization ⭐ |
|---|---|
| Duración en pantalla | 5s (Kling) + 4s tpad-hold = 9s |
| Audio adicional | – (solo narrador omnisciente "Elige a tu compañero...") |
| Kling | 1 clip tier 5s con `start_image=teaser, end_image=characters` |
| Engagement | **Máximo retention 3s** (hook visual + caption + motion + payoff de materialización todo en primeros 3s) |
| Costo | $0.30 (1 clip Kling) + $0.04 (h1-teaser.png Gemini) = ~$0.35 |
| Riesgo Kling | Bajo (Kling es bueno interpolando entre 2 imágenes similares) |
| Validado en | mina-abandonada v15-final (9.9/10) |

**Cuándo usar Opción D**:
- Default para video horror-choice modern post-2026-05
- Cuando querés hook visual inmediato sin sacrificar retention 3s
- Cuando el setting tiene "umbral" simbólico (entrada de mina, puerta de casa, boca de cueva)

**Cuándo NO usar Opción D**:
- Cuando el personaje "malo aparente" tiene presencia tan icónica que romper la 4ª pared (Opción B) es más fuerte
- Cuando el video es para YouTube Long y tenés tiempo para hold de 15s (V1 legacy)

**Receta completa**: ver `INTRO-FORMULA.md` — copy-paste-ready con prompts, GSAP, audio mix.

### Cuándo usar A vs B vs C vs D

| Mood del video | Sub-pattern recomendado |
|---|---|
| **Default modern (post-2026-05) — Reels/TikTok** | **Opción D** ⭐ (mina-abandonada v15 = Gemini 9.9/10) |
| **Default pre-2026 — videos largos / YouTube** | Opción C ⭐ (bosque-abandonado v7 = Gemini 10/10) |
| Pure atmospheric / suspense lento | Opción A |
| Need hook ultra-viral con personaje icónico | Opción B (rompe 4ª pared) |
| Budget tight (videos de prueba, A/B testing) | Opción A |
| Personaje "malo" sin chiste único | Opción A o D |
| Personaje "malo" tiene presencia visual icónica | Opción B o C |
| Setting con "umbral" simbólico (entrada portal) | Opción D ⭐ |

### Resto de hitos (H3 mano, H4 luz, H5 salida, H6 cliffhanger): regla general de ANIMATION-LAYER

- Twists (mano fría, luz cálida, hand emerging): tier 5s o 10s con +1s buffer, NO loop
- Cliffhanger: tier 10s con motion sutil (humo de fogata, vapor de café), opcionalmente loop atmospheric
- Detalles (objetos, herramientas): SIN Kling — Ken Burns suficiente

### Costo orientativo formato horror-choice (15-20 imágenes típicas)

- H1: 1 clip tier 5s loopable = $0.35
- H3 twist + tensión: 2 clips tier 10s = $1.40
- H4 twist + tensión: 2 clips tier 10s = $1.40
- H5 salida: 1 clip tier 10s = $0.70
- H6 cliffhanger: 2 clips tier 10s = $1.40
- **Total base**: $5.25
- **Con retries 1.5×**: **$8 por video**

---

## 11. REGLAS PROHIBIDAS (NUNCA hacer esto)

- ❌ Fade in/out de texto on-screen (rompe el ritmo de lectura rápida)
- ❌ Música melódica con BPM definido (mata la atmósfera)
- ❌ Voz de TTS sin procesar (suena a IA, pierde intimidad)
- ❌ Color grading saturado o cálido fuera del cliffhanger
- ❌ Diálogo extendido entre personajes (rompe la inmersión POV)
- ❌ Resolución completa con explicación (el cliffhanger debe quedar abierto)
- ❌ Castigar al "bueno aparente" — siempre debe ser la opción que el espectador NO eligió
- ❌ Dilemas binarios obvios tipo "matás o no" (debe ser dilema de obediencia)
- ❌ Loading bar de duración variable (siempre 2.5s)
- ❌ Cliffhanger en color frío (debe ser cálido)
- ❌ **Reutilizar el mismo PNG en múltiples captions de la misma escena** (rompe V8-1 — produce slideshow feel, especialmente con motion)
- ❌ **Publicar sin capa SFX dedicada** más allá de narración + música + ticks (rompe V8-2 — el video se siente "narrador con música", no cine)
- ❌ **Dejar planos estáticos >2s sin motion** (rompe V8-3 — Ken Burns es el piso, no el techo)
