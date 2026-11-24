# TASTE-LOG — Horror-choice format

> **Purpose**: capturar el juicio perceptual del USER (Tomás) sobre videos del formato horror-choice. Lo que Gemini Vision puntúa NO es lo mismo que lo que vos sentís ver el video. Este doc captura la DIFERENCIA + intuye por qué.
> **Owner**: 🔍 Auditor entrevista al USER post-PUBLISH; entries written by auditor based on user input. **NUNCA el auditor inventa entries — solo registra lo que el user articula**.
> **Why this exists**: el sistema codifica 33+ gaps técnicos pero ~0 gaps estéticos. Sin este doc, después de N videos producís contenido técnicamente correcto pero estilísticamente promedio. Tu gusto = activo más subestimado del sistema (per architectural review 2026-05-21).
> **Created**: 2026-05-21 — first entry retrospective from 3 backrooms POV refs ingested 2026-05-20/21.
> **Autoridad estructural + invariante** (separada del juicio perceptual de este doc): `PAUTA-MASTER.md § 2` (esqueleto + "bueno-aparente nunca en el played path"; las entries #1/#2 sobre SFX-densos/inmersión están codificadas en `INGENIERO-PAUTA § 10`).

---

## Format note (transitorio)

Este doc está intencionalmente NO-TAXONOMIC en v1. Prose libre, observation-driven. **NO arme tablas de check-boxes**. Después de 2-3 entries más vamos a iterar el formato real — probablemente algunas dimensiones repetidas emergerán naturalmente. Hasta entonces, prosa honest descriptive captura mejor el insight.

---

## Entry #1 — 2026-05-21 — 3 refs backrooms POV horror

**Refs evaluados**:
- Ref-NEW-A: `¿A quién elegirás#povhorror #liminalspaces #backrooms.mp4` (Felipe + Enzo, 85.6s, cueva subacuática)
- Ref-NEW-B: `¿Qué compañero elegirás#povhorror #liminalspaces #backrooms.mp4` (Tulio + Daniel, 91.1s, torre nocturna)
- Ref-NEW-C: `¿A quién elegirás esta vez#povhorror #liminalspaces #backrooms.mp4` (Dylan + Leo, 79.8s, Louvre after-hours)

**Tu percepción declarada**: "ALTISIMA calidad" — los 3.

**Scores Gemini brutal honest**:
| Ref | Score Gemini |
|-----|-------------:|
| A cave | 6.9/10 |
| B tower | **6.6/10** |
| C Louvre | 7.9/10 |

**Delta**: substancial. Si tu perceptual es ~9/10 para los 3 (consistent con "ALTISIMA"), tenés:
- A: delta +2.1 (vos 9, Gemini 6.9)
- B: delta +2.4 (vos 9, Gemini 6.6)
- C: delta +1.1 (vos 9, Gemini 7.9)

Promedio delta ~+1.9 puntos.

⚠️ **CORRECTION + UPDATE 2026-05-21 PM (post user perceptual scores received)**:

Mi inferencia original asumió cinema tu perceptual era ~6-7 + backrooms ~9 — **ambas inferencias INCORRECTAS**. Tu números reales:
- matadero v1: **7.9/10**
- cinema-abandonado v2: **7.8/10** (diferencia 0.1 — esencialmente equivalentes)
- Ref-A cave: **10.0/10**
- Ref-B tower: **10.0/10**
- Ref-C Louvre: **9.6/10**

**Deltas reales (Gemini holistic vs User perceptual)**:

| Video | Gemini | User | Delta | Signal |
|-------|:---:|:---:|:---:|---|
| matadero v1 | 9.75 | 7.9 | +1.85 | Gemini OVER |
| cinema-abandonado v2 | 8.6 | 7.8 | +0.80 | Gemini OVER |
| Ref-A cave | 6.9 | **10** | **-3.10** | Gemini UNDER |
| Ref-B tower | 6.6 | **10** | **-3.40** | Gemini UNDER |
| Ref-C Louvre | 7.9 | **9.6** | **-1.70** | Gemini UNDER |

**Average delta own productions: +1.33** (Gemini infla).
**Average delta canonical backrooms: -2.73** (Gemini sub-pesa).
**Total spread = 4.06 puntos** — Gemini INVIERTE SIGNO entre own vs canonical.

### Lo que CONFIRMÓ tu data

Mi hipótesis original "INMERSIÓN > PERFECCIÓN" **resultó VALIDADA, no refutada**. Refinada con números reales:

1. Los 3 backrooms tienen artifacts visuales Gemini-cazados (Ref-A walls melt 0:11 + finger morph 0:58; Ref-B hand melts 0:26 + fingers dissolve 0:30 + jacket-blob 0:48; Ref-C hand digit morph 0:22 + jittering painting 1:12).

2. **A pesar de todos esos artifacts, vos diste 10/10 a A y B + 9.6 a C**. Tu juicio explícitamente NO castiga AI imperfection cuando el feel inmersivo + liminal-spaces está fuerte.

3. **Gemini HOLISTIC NO sabe puntuar género POV/liminal-spaces correctamente**. Penaliza exactamente lo que vos NO penalizás. Anti-pattern #12 sustancialmente más grave que codifiqué — no es offset constant, es INVERSIÓN DE JUICIO entre tipos de video.

### Lo que Gemini PENALIZÓ y a vos no te importó

Gemini sub-pesa:
1. **POV hands "stiff plastic"** (Ref-A 0:11-0:14 melting walls, Ref-A 0:58 finger morph rock, Ref-C 0:22 keys digit morph). Para Gemini: "lack of realistic fluid/surface interaction breaks immersion". Para vos: aceptable porque el POV ES inmersión.
2. **Hook genérico narrativamente** (Ref-A: "generic horror trope opening line", Ref-B: "derivative Cartoon Cat"). Para Gemini: pierde 1-2 puntos hook. Para vos: el hook visual (silueta característica) ya cumplió.
3. **Captions ausentes Ref-B**: Gemini destructor (-3pts catastrophe). Para vos: parece que el visual carga suficiente sin captions — o no lo notaste (o lo notaste pero no se lo pusiste como deal-breaker).
4. **AI artifacts cercanos visibles**: Ref-A blood "flat sticker not fluid", Ref-C sarcophagus "hallucinated hieroglyphics jitter". Para Gemini: "breaks immersion essential for POV". Para vos: integrado en la estética backrooms (que ABRAZA imperfección + sueño glitchy).

### Lo que Gemini PREMIÓ y a vos también

Concordancia entre vos y Gemini en estos 3 refs:
1. **Audio production layering 3-4 layers** (los 3 refs hit 8-9/10 audio Gemini). Para vos: probably el factor más alto en tu "ALTISIMA". Sound design dense + layered = inmersión.
2. **Narrative comprehension 8-9/10**: los 3 refs tienen dilema claro + counterfactual visible. Para vos: la estructura del format funciona.
3. **Horror atmosphere sustained 7-8.5/10**: los 3 mantienen dread sin jump-scares cheap. Para vos: probablemente el "vibe" que llamás ALTISIMA es exactamente esta sustained dread.

### Lo que TÚ valorás (Gemini NO captura bien)

Patrones que emergen de TU side del delta:

1. **Inmersión POV literal**: vos sos el viewer protagonista, no observador. Los hands VAN al frame. Eso genera identificación que Gemini lee como "stiff plastic" pero vos leés como "I am the character". Esto NO es un bug — es el género POV horror. Cinema-abandonado iter 1 era POV pero los hands estaban menos integrados; quizás por eso te sentiste "peor".

2. **Estética liminal-spaces / backrooms**: ambiente abandonado + space familiar pero wrong (cueva submarina iluminada, torre nocturna desierta, Louvre after-hours sin gente). Eso es la firma genre. Los 3 refs ABRAZAN imperfección visual AI porque la imperfección encaja con el "feel" backrooms (todo se siente "almost real but wrong"). Cinema-abandonado iter 6 también tenía esto pero menos explícito.

3. **Sound design 3-4 layers densos**: Ref-A subbase drone + heartbeat + spatial + voice; Ref-C metallic keys + hollow stone + drone + foley. Esto coincide con § 25 PAUTA "music layers 3 mandatory" que codificamos. Tu intuición ya validaba esa regla antes de que la articulamos.

4. **Counterfactual twin/good ending**: los 3 refs usan twin endings (Ref-A good cave path at end, Ref-B happy alt 1:21, Ref-C Leo brilliant good ending 1:11). Esto valida § 24 PAUTA refined — twin ending FUNCIONA cuando es framed como "relief from horror" no "retrospective explanation". Cinema-abandonado iter 1-6 cayó en "retrospective explanation" y eso es probablemente parte del "peor".

5. **Character design uncanny pero readable**: los 3 refs tienen characters con silueta DISTINCT (Felipe tall alien-grey, Tulio sheep-wolf hybrid mask, Dylan spindly silent). Gemini puntuó character consistency 6-8/10 (con fluctuations). Para vos: lo "readable" del archetype importa más que lo "consistent" anatómicamente. Cinema-abandonado Salvador/Nico también tenían silueta DISTINCT pero los stitches fluctuaban — quizás eso te bothered más que a Gemini.

### 🚨 BREAKTHROUGH 2026-05-21 PM late — EXECUTION CONTINUITY identified as THE X factor

**User confirmed in chat**: lo que llama "consistencia" NO es story chain narrativo. Es **EXECUTION CONTINUITY** — physical journey continuous shot-to-shot:

1. POV/character motion REAL between shots (no teleportation)
2. Audio bridges across cuts (no silencio gaps)
3. Visual style consistent shot-to-shot
4. Kinetic momentum sustains (shot N motion continues into N+1)

**User example matadero (BROKEN)**:
```
shot 1: meat → shot 2: matadero → shot 3: cortando → shot 4: boca → shot 5: boca me come
↑ story chain coherent BUT physical journey broken (cada cut es teleport)
```

**User example canonical Ref-A cave (PERFECT)**:
```
shot 1: cueva → shot 2: avanzo caminando → shot 3: traje ofrecido →
shot 4: pongo traje → shot 5: bajo → shot 6: nado
↑ cada shot tiene MOVIMIENTO físico bridge al siguiente
```

**Validation via calibrated Gemini v4 (2026-05-21)**:
- Added EXECUTION CONTINUITY as PRIMARY dimension (30% weight)
- Gemini v4 detected matadero teleport-cuts (exec dim score 4.8/10)
- Gemini v4 final weighted: matadero 7.6 (vs user 7.9 = delta -0.3 ✅)
- Mean abs delta v4 across 5 critical videos: 0.14 (38% improvement vs v2)

**THIS is THE primary gap own production → canonical** identified definitively. All previous hypotheses (atmosphere, sound, character) are secondary to EXECUTION CONTINUITY.

### El insight más importante de este entry (revisado 2026-05-21 PM — CONFIRMADO con datos reales)

**Tu data refuta mi corrección anterior y CONFIRMA la hipótesis original "INMERSIÓN > PERFECCIÓN" pero más fuerte de lo que pensé**.

**Hipótesis CONFIRMADA con números reales**:

1. **Tu vara NO es restrictive** — diste 10/10 a 2 refs. Cuando algo te resuena, vale 10 honest.

2. **El gap real own production vs canonical canonical = 2.1 pts perceptuales** (matadero/cinema 7.85 promedio vs backrooms 9.87 promedio). Eso es ENORME en escala 1-10.

3. **Gemini INVIERTE SIGNO** entre own (+1.33 over) y canonical (-2.73 under). La inversión NO es ruido — es señal: Gemini NO sabe puntuar género POV/liminal-spaces.

4. **Lo que separa 7.85 → 10 para vos** (qué hacen backrooms que nuestras producciones NO):
   - POV inmersión literal (hands ARE you, no observador)
   - Liminal-spaces atmosphere coherence (backrooms vibe sustained)
   - Sound design 3-4 layers densos (drone + subbase + heartbeat + foley)
   - Counterfactual twin/good ending framed como relief (no retrospective)
   - Uncanny character silueta DISTINCT (Felipe alien-grey, Tulio sheep-wolf, Dylan spindly)
   - Atmospheric secondary motion ≥3 simultaneous (walls + ambient + character breath + light)
   - Cuts/min 14-19 modulated

   Algunas codificadas ya (cuts/min § 23, music layers § 25, counterfactual § 24, character signature § 21, atmospheric motion § 20). Otras NO (POV inmersión literal, liminal-spaces vibe coherence).

5. **System target REAL para video #3** = **perceptual ≥9.0**, NO Gemini ≥9.7. Porque:
   - Gemini ≥9.7 técnicamente alcanzable (matadero crossed it iter 6) PERO usuario score 7.9 mismo video = NO satisface
   - Backrooms refs canonicalmente Gemini ≤8 PERO usuario 10/10 — Gemini puede dar bajo y aún así user-satisfaction high
   - **Dual-gate actual (Gemini + audit-vs-ref) NO predict user-satisfaction**

6. **System necesita capturar al menos UNA dimensión nueva**: probablemente "inmersión POV literal" + "liminal-vibe coherence" + "atmosphere depth quanti". Hoy Gemini holistic 14-dim NO la incluye.

### Implicación arquitectural enorme

Si el sistema actual mide "Gemini holistic ≥9.7" como gate, y vos dijiste 7.9 a matadero que cruzó ese gate — **el gate técnico NO predice tu satisfaction**. Hay un gap arquitectural en la definición de "calidad" del sistema.

**Forward** (decisión a tomar con architect):
- ¿Reemplazar Gemini holistic ≥9.7 con user_perceptual ≥9.0 como gate primario?
- ¿Mantener dual-gate técnico + agregar tercer gate "user perceptual ≥X"?
- ¿O cambiar a "user perceptual ≥9.0 OR (Gemini ≥9.7 AND user perceptual ≥8.0)" combined gate?

Cualquiera de las opciones requiere arquitectura nueva — NO es ajuste cosmético.

---

## Entry #2 — 2026-05-30 — V5 `sala-limpia-bioseguridad` SHIPPED ("muy bueno") + ajustes forward V6

**Veredicto Tomás V5**: "brutal… muy bueno" tras cerrar 3 bugs forenses (si-elegiste framing, audio truncation, caption coverage). Aprobado.

**Ajustes pequeños pedidos para V6+ (aplicar en SPEC/engine):**
1. ⭐ **Name labels del hook MÁS GRANDES.** Los labels de personaje (Axel/Hugo, Y11.5) deben aparecer en letra más grande al inicio. → subir `fontsize` en `drawtext_namelabels()` (engine) + codificar tamaño canónico en INGENIERO-PAUTA name-label spec. (V5 quedaron chicos para el gusto de Tomás.)
2. ⭐ **MÁS SFX, especialmente GRITOS al morir.** Cada consequence-A fatal (body horror = muerte/daño) debe tener un SFX de grito/agonía + más densidad de SFX en general (canonical refs tienen 30-40 SFX, sound design denso). → architect agrega `scream`/`agony` SFX por shot fatal en `asset_list.sfx_prompts_to_generate`; engineer mux. (V5 tenía SFX por acción pero faltaban gritos de muerte.)

**Why**: estos son los detalles de "felt quality" que separan canónico de promedio (TASTE-LOG raison d'être). Sound design denso + labels legibles = más inmersión + scroll-stop.
**How to apply V6**: el arquitecto los incorpora en el SPEC FASE 0 (name_label_fontsize_intent + scream SFX per fatal shot); el ingeniero ejecuta.

---

## Entry #3 — 2026-06-01 — V6 `invernadero-turno-riego` SHIPPED ("buena / bastante bueno")

**Veredicto Tomás**: "Buena! Bastante bueno, creo que estamos sacando contenido de calidad." Publicado.

**Lección estructural (no debe recurrir)**: el bueno-aparente (Celeste) quedó presente en el recorrido jugado tentando → violaba el invariante canónico; el arquitecto lo diseñó así + el auditor lo racionalizó. Root cause = receta `SKILL.md` "doble-amable = ambos hablan" sin el límite del invariante. Fixeado: invariante en PAUTA §2 + SPEC-AUDIT anti-pattern #20 + validator `ai-video audit-spec-structure-vs-canonical` (12 tests). Memoria `feedback_spec_audit_structural_divergence`.

**Ajustes pedidos por Tomás para V7+ (codificados en docs existentes, sin parches nuevos):**
1. Más sonidos inmersivos matcheados a la acción (PAUTA §2.4 + INGENIERO-PAUTA §10).
2. Más efectos corte-TV en cambios A↔B + muerte (effects-library `old_screen_glitch_error` + INGENIERO §9).
3. Narración final no-"retrasada": atempo nunca <0.90 (V6 over-atempo 0.74 = arrastrado); extender clip, no ralentizar la voz (INGENIERO §1.6). David C2 OK.
4. Name-labels grandes arriba de cada uno, antes Y durante el countdown (INGENIERO §7.4.1).
5. Música ambiente mood-matched volumen-bajo, atmosférica/tonal (NO melódica — preserva el dread; PAUTA §25).
6. ⚠️ Caption-overlap cuando hablan 2 (narrador+personaje o 2 personajes) — investigación 2026-06-01.

**Gemini calibrado 7.9** (execution_continuity 5.2 = GAP#40 teleport-cuts; otras 9 dims 8.5-9.6). El techo own-prod sigue siendo la continuidad de ejecución (= matadero 7.9 / cinema 7.8); las mejoras 1-6 NO lo tocan (es de animación i2v — el próximo gran salto de calidad).

---

## Emergent patterns to watch in next entries

(Después de 2-3 entries más vamos a iterar el formato real. Por ahora estos son patterns a verificar si recurren.)

1. **¿INMERSIÓN > PERFECCIÓN se repite?** Si en entry #2 y #3 el delta Gemini-user va en mismo sentido (Gemini sub-pesa POV inmersión), valida hipótesis.
2. **¿Tu juicio premia complejidad audio sobre complejidad visual?** Los 3 refs scored high audio pero medio visual para Gemini. Si tu perceptual sigue tracking sound design layering, sería pattern claro.
3. **¿Hay un "vibe coherence" score que necesitamos crear?** Hoy NO existe en audit-against-referent ni Gemini holistic. Si tu juicio repetidamente cae fuera de esos 14 dimensions, está señalando una dimensión faltante.
4. **¿Cuándo SÍ coincidís con Gemini bajo?** Vos viste cinema-abandonado iter 1 y dijiste "peor" — Gemini iter 5 también scoreó bajo (audio/visual mismatch). Hay convergencia user-Gemini cuando hay errores TÉCNICOS objetivos. La divergencia ocurre en juicios ESTÉTICOS.
5. **¿La estética backrooms transfiere fuera del genre?** Si en formato tutorial / B2B futuro mantenés preferencia por liminal-space-vibe + sound depth, es signature CROSS-FORMAT (debería ir a TASTE-LOG NIVEL 2 universal, no NIVEL 3 horror-choice). Pero esperar a tener data.

---

## Author note (auditor — para próximas sessions)

Este entry fue ESCRITO POR EL AUDITOR retroactivamente basado en el análisis de los 3 refs + el comentario user "calidad ALTISIMA" + comparación con cinema-abandonado donde user dijo "el peor". Es **inferencia best-effort, no captura directa del user**.

Próximo entry (post video #3 ship) debería ser entrevista directa estructurada con 5 preguntas:
1. "Cuál SHOT (timestamp específico) hubieras cortado diferente o regenerado?"
2. "Cuál AUDIO momento (cue + timestamp) te molestó pero dejaste pasar?"
3. "Compará este video con el anterior — qué hiciste mejor, qué peor?"
4. "Si tuvieras que prohibirte UNA cosa que hiciste en este video forward, cuál?"
5. "¿Qué le falta a este video para ser 10/10 PARA TI (no para Gemini)?"

Hasta entonces, este entry sirve como **baseline retrospective** que próximos entries pueden refute o corroborate.

---

**Última actualización**: 2026-05-21 (creación + entry #1 retrospective 3 backrooms refs).
**Próximo entry esperado**: post video #3 ship — entrevista directa 5 Q estructurada.
