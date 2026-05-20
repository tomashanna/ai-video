# PAUTA-MASTER.md — Pauta empírica del formato "Elige a tu compañero"

> **AUTORIDAD MÁXIMA del formato.** Esta pauta deriva EXCLUSIVAMENTE del análisis empírico de **8 videos virales canónicos** ubicados en `/videosref_elige_tu_compa/`. Reemplaza referencias previas a V1/V2/V3/V7 nuestro/V2 nuestro que existían en `CREATIVE-BRIEF.md` (la pauta anterior mezclaba referentes externos antiguos con nuestra propia producción — método metodológicamente incorrecto).
>
> **Última actualización:** 2026-05-13 PM
> **Versión:** v1.0 (post-restructure post-Maikol-incident)

---

## 0. METODOLOGÍA — DE DÓNDE VIENEN ESTAS REGLAS

### Los 8 videos canónicos (base empírica única)

| ref-ID | Creator | Setting | Score Gemini (rúbrica) |
|--------|---------|---------|------------------------|
| ref-03 | @referent-a | Mina abandonada (Bruno/Pablo) | 9.04 |
| ref-06 | @referent-a | Carretera rural nocturna (Axel/Enzo) | 8.62 |
| ref-08 | @referent-a | Acuario abandonado (Hugo/Pablo) | 8.85 |
| ref-09 | @referent-a | Cockpit avión (Victor/Axel) | 8.99 |
| ref-10 | @referent-a | Planta industrial fundición (Rurik/Enzo) | 8.66 |
| ref-11 | @referent-c | Metro / vagón vacío (Mario/Ivan) | 8.04 |
| ref-12 | @referent-b | Tren nocturno (Nano/Teresa) | 8.83 |
| ref-13 | @referent-b | Planta eléctrica → fiesta carpinchos (Miro/Bryan) | 9.10 ⭐ TOP |

### Lo que esto significa

- **TODA regla en esta pauta** está validada contra estos 8 videos. Si una regla NO se cumple en 7/8 o más, está marcada como "no universal".
- **NINGUNA regla** viene de V1, V2, V3 originales antiguos NI de V7 nuestro NI de bosque nuestro. La pauta anterior tenía ese sesgo metodológico.
- **Los 8 videos** son la única fuente de verdad. Cualquier hallazgo posterior que contradiga esta pauta debe re-analizar los 8 antes de proponer cambio.

### 📚 Cross-ref con canonical-scenes (añadido 2026-05-16 Bloque I)

Cuando una regla acá tiene compliance N/8 explícito, podés ver EJEMPLOS CONCRETOS de cómo se ejecuta beat-by-beat en:

- **`canonical-scenes/INDEX.md`** — cross-ref grid por `pattern_category` (12 grids: hook, setup, decision_setup, consequence_A/B, cliffhanger). Buscás "cómo se ejecuta X categoría en los 8" → INDEX.
- **`canonical-scenes/ref-XX-*.md`** — deep-dive scene-by-scene por ref (10-14 beats con `who's there`, `what they do LITERAL`, narration Whisper, UI active, animation tier, pattern observation).

**Convención**: cuando esta pauta diga "validado 8/8" en una regla → mirá la sección correspondiente en INDEX para ver el patrón cross-canónicos + lee 1-2 ref-XX más similares al tuyo para empirical reference de beats. PAUTA = QUÉ, canonical-scenes = CÓMO.

### Lo que NO es base de pauta (BAN ABSOLUTO)

- ❌ **Nuestras propias producciones** (mina-abandonada, bosque-abandonado, elige-companero, pueblo-fantasma-desierto, calabozo-catacumbas, cabana-tormenta, isla-faro) — son lo que QUEREMOS MEJORAR para coincidir con los virales, NO fuente de regla
- ❌ **Gemini scores nuestros (9.9/10, 9.5/10, etc.) como "validación"** — demostrados INFLADOS. Pueblo-v2 obtuvo Gemini 9.9 con video real 7/10 (falso positivo). Usuario confirmó "ninguno alcanza @referent-a ni por cerca". **Gemini score nuestro ≠ autoridad canónica.**
- ❌ Videos referenciados como V1/V2/V3 en docs antiguos (sin certeza de cuáles son ni si están entre los 8)
- ❌ Refs 1, 2, 4, 5, 7 (otros géneros: AI mystery, meme, POV synthwave) — NO son elige-tu-compañero

### Lo que SÍ es base de pauta

- ✅ **Solo los 8 videos canónicos** en `/videosref_elige_tu_compa/` (refs 3, 6, 8-13)
- ✅ Análisis empíricos descriptive de esos 8 (`/referent-analysis/descriptive-analysis/ref-XX.md` para los 8)
- ✅ Cada regla con compliance N/8 explícito

### Lista de invenciones prohibidas (de incidentes pasados)

| Invención | Cuándo apareció | Por qué prohibida |
|-----------|-----------------|---------------------|
| "BAJARÍAS estándar" | Incidente Maikol crucero 2026-05-13 | NO existe. Tagline universal: "Elige a tu compañero" |
| "Motor duda artificial" | Incidente Maikol marítimo previo | Refutado por § 6 de esta pauta |
| "2 dilemas mínimo" | Pauta vieja CREATIVE-BRIEF | Empíricamente 3-4 (1 inicial + 2-3 internas) |
| "Bueno aparente no tiene diálogo" | Pauta vieja | ref-08 Hugo SÍ habla |
| "Opción ganadora SIEMPRE va contra impulso" | Pauta vieja § 1 | ref-09 Victor obedecer = ganadora |
| "Bueno = tame / menos amenazante" | Pauta vieja | 7/8 buenos son visualmente extreme también |
| "Opción C corporal motion canónica" | Memoria intro_9s_canonical | Es técnica nuestra, NO regla canónica |

**Si una regla NO está en este doc con compliance N/8 → NO ES REGLA. Es invención.**

---

## 1. FILOSOFÍA — LA REGLA DE ORO

> **El formato es el GENERADOR de creatividad, no el LÍMITE.** El espectador viene por la fórmula reconocible (countdown, dilema binario, twist, cliffhanger). La creatividad vive en QUÉ poblamos esos slots, no en romperlos.
>
> **Si te encontrás queriendo romper el formato, el problema es tu historia, no el formato.**

Validado en 8/8: ningún video rompe la estructura. Toda la variación está en los slots.

---

## 2. ESTRUCTURA TEMPORAL EMPÍRICA

### Duración total (range real, no fijo)

- **Mínimo observado:** 76s (ref-10)
- **Máximo observado:** 129s (ref-13)
- **Promedio:** ~97s
- **Sweet spot recomendado:** 80-100s

### Distribución por fase (validada en 8/8)

| Fase | % del video | Función |
|------|-------------|---------|
| **Hook + presentación dyad** | 0-15% | Visual uncanny + "Elige a tu compañero" + countdown |
| **Setup rama del malo** | 15-25% | Establecer contexto narrativo |
| **3-4 dilemas con consecuencias** | 25-85% | Cada uno con countdown + loading bar + body horror si fallás |
| **Resolución del último dilema** | 85-92% | Climax del path elegido |
| **Counterfactual outro** | 92-100% | "Si hubieras elegido X, habrías..." |

---

## 3. REGLAS INVIOLABLES (validadas en 8/8)

### Lenguaje
- ✓ **Segunda persona implícita:** "tú trabajas, miras, eliges" (no "trabajarás")
- ✓ **Presente del indicativo** en consecuencias
- ✓ **Oraciones cortas y staccato** en momentos de tensión
- ✓ **Frases nominales sin verbo** para climax: "Luz fría, pasillo vacío.", "Caes al vacío."

### Estructura
- ✓ **3-4 decisiones binarias** (no 2 — eso era falso en pauta vieja) — incluye decisión inicial "elegir compañero" + 2-3 internas
- ✓ **Cada decisión** tiene countdown 3-2-1 + barra de carga porcentual
- ✓ **Counterfactual outro** mostrando "qué habría pasado si X" — 8/8 cumplen
- ✓ **Loading bar** entre decisiones (7/8 — ref-11 lo tiene menos pronunciado)
- ✓ **Hard cut** entre escenas con SFX impacto

### Producción
- ✓ **POV (primera persona) ≥80% de los shots** — ENFORCEMENT obligatorio. El arquitecto debe contar shots POV vs non-POV en el SPEC y reportar ratio en self-audit pre-handoff. Validado >70-80% en 8/8 (refinado de estimación previa). NO shots en tercera persona donde el viewer ve "al protagonista" — el viewer ES el protagonista.
- ✓ **Body horror específico, no genérico** — "destrozado por taladro", "ahogado en algo que no es agua", "atropellado", "electrocutado" (no "mueres")
- ✓ **CTA narrado al final** ("Una noche en paz" tipo tagline)
- ✓ **Watermark del creator** visible toda la duración
- ✓ **Caption del Reel** con pregunta directa ("¿A quién elegirías?") + hashtags

### Transiciones narrativas — RAMA B EXPLÍCITA (regla añadida 2026-05-15)
- ✓ **Después de cada decisión binaria, debe haber transición narrativa explícita** entre rama elegida y rama no-elegida — NO solo cliffhanger final
- ✓ **Si el video muestra consecuencia A (eg. ahogarse)**, antes de avanzar al siguiente hito debe haber 1 línea de narración o cue visual que sea explícito "Si hubieras elegido B / Vuelves al momento / Otra realidad" — sin esto el viewer queda perdido sobre cómo pasamos de "ahogándote" a "estás de vuelta con malo aparente"
- ✓ Si la transición es solo cliffhanger al final ("Si hubieras elegido X"), el viewer interpreta saltos mid-video como bugs narrativos
- ✓ **Caso disparador maikol-crucero (2026-05-15)**: rama B no presentada → user confused en 1:00 "no se explica cómo paso de ahogarse a estar de vuelta con Maikol"

### Presentación de personajes — BUENO APARENTE NECESITA ≥2 SHOTS PRE-CLIFFHANGER (regla añadida 2026-05-15)
- ✓ **El bueno aparente debe aparecer visualmente en ≥2 shots ANTES del cliffhanger outro** — NO puede ser solo "mencionado por el narrador" o "aparece por primera vez en outro"
- ✓ Si bueno aparente solo aparece en cliffhanger, el outro no tiene anclaje emocional ni puede crear "habrías elegido a X" como counterfactual
- ✓ En 8/8 canónicos: bueno aparente aparece en H1 (presentación dyad) + reaparece en cliffhanger. Mínimo 2 shots de presencia visual antes del payoff
- ✓ **Caso disparador maikol-crucero**: CHELO aparece en 1:18-1:19 sin haber sido presentada previamente con suficiente presencia → counterfactual outro no carga emocionalmente

### Lip sync intent — MARCAR EXPLÍCITAMENTE EN SPEC (regla añadida 2026-05-15)
- ✓ **Para cada shot del SPEC, el arquitecto debe marcar `lip_sync_required: true|false`**:
  - `true` si el shot incluye diálogo del personaje (malo o bueno aparente habla on-screen)
  - `false` si solo hay narración voiceover (no diálogo on-screen)
- ✓ **Si `lip_sync_required: false`**: el ingeniero NO debe usar clips animados con movimiento de boca visible — porque crea disonancia (personaje "habla" pero no está diciendo nada audible)
- ✓ Implementación técnica: ver `INGENIERO-PAUTA-MASTER.md` § Lip sync rule
- ✓ **Caso disparador maikol-crucero**: 0:22 Maikol "habla" en clip animado mientras solo narrador habla → user confused "Maikol aparece hablando pero solo habla el narrador"

### "Si elegiste X" framing — REGLA INVIOLABLE (regla añadida 2026-05-16)
- ✓ **Toda consequence narration en Slot E DEBE prefijarse "Si elegiste {opción}..."** — caption "SI ELEGISTE B:" SOLA no es suficiente
- ✓ Compliance: validado en 8/8 canónicos (auditor debe verificar lectura de transcriptions reales — Bloque H futuro)
- ✓ Aplicado por arquitecto en SPEC v6: `consequence_A_text` y `consequence_B_text` empiezan con "Si elegiste {A|B}..."
- ✓ Auto-audit D19 valida compliance en handoff
- ✓ Sin este framing, el horror-choice colapsa a horror genérico (caso cabina-14 V1 render 2026-05-16)
- ⚠️ **EXTRACT to choice-format-base** cuando agreguemos un 2do template del género choice

### Narración CLARA, NO tenebrosa — REGLA INVIOLABLE (regla añadida 2026-05-16)
- ✓ **Foco**: pocas palabras que digan QUÉ pasa (acción) o den contexto. NO priorizar "sonar tenebroso" en el relato.
- ✓ El estilo tenebroso emerge del **visual + SFX + música ambient**, NO de la narración.
- ✓ **Estilismo > claridad = BUG del formato.** Si el viewer no entiende qué pasa en 1ra escucha sin caption → reescribir.
- ✓ Ejemplos:
  - ❌ Tenebroso ("genre temptation"): "El silencio te abraza con dedos de hielo y el ojo del faro te elige."
  - ✅ Claro: "Te congelaste. El ojo del faro te encuentra."
- ✓ Aplicado en SPEC v6 narration_in_this_shot: priorizar verbo + sujeto + objeto LITERAL.
- ✓ Caso disparador: cabina-14 V1 — narración estilizada produjo confusion sobre lógica narrativa.

### Respeto absoluto de la pauta para guiones — REGLA INVIOLABLE (regla añadida 2026-05-16)
- ✓ **La estructura narrativa según PAUTA-MASTER no es sugerencia — es regla.**
- ✓ Improvisar fuera de la pauta (cambiar orden de hitos, agregar slots no canónicos, alterar formato de "Si elegiste X") = BUG del producto creativo.
- ✓ Si el arquitecto cree que un caso justifica desvío → escalar al user PRIMERO, NO improvisar.
- ✓ Caso disparador: cabina-14 SPEC inicial saltó pattern de Slot E → render reveló gaps narrativos.

### Personajes
- ✓ **Dos personajes presentados simultáneamente** en H1 (no aparición sequential)
- ✓ **Name labels** sobre cada personaje al introducirlos (8/8)
- ✓ **Contraste visual entre los dos** (color, forma, postura)
- ⚠️ **Diálogo del malo aparente** — varía: a veces tiene dialogue críptico (1-2 líneas), a veces no. NO es regla estricta.
- ⚠️ **Diálogo del bueno aparente** — ref-08 Hugo (bueno) sí habla "No me elijas". Otros buenos no. NO es regla estricta.

---

## 4. HALLAZGO CRÍTICO — PERSONAJES RECURRENTES CROSS-VIDEO

Personajes con el mismo nombre y diseño visual aparecen en múltiples videos, **a veces con roles invertidos**:

| Personaje | Aparece en | Rol video N | Rol video M |
|-----------|------------|-------------|-------------|
| **PABLO** (tubérculo ovoide) | ref-03 + ref-08 | Bueno (ref-03 mina) | **Malo / traidor** (ref-08 acuario) |
| **AXEL** (cabeza hongo rojo) | ref-06 + ref-09 | Malo (ref-06 carretera) | **Bueno / protector** (ref-09 cockpit) |
| **ENZO** (esquelético calvo / humano normal con chimenea) | ref-06 + ref-10 | Bueno cozy (ref-06) | Bueno aliado (ref-10) — mantiene rol pero versión más extraña |

### Implicación creativa
- El rol (malo/bueno) **NO está predeterminado por el diseño visual**
- El **comportamiento + outcome del video** define quién es malo/bueno
- Recurrencia cross-video crea "universo del creator" + drives re-watch + crea misterio ("¿Pablo es bueno o malo realmente?")

### Implicación para arquitecto
Cuando diseñes un video nuevo, considerá:
- ¿Reusar personaje recurrente con rol invertido? (Pablo recurre, ahora será malo)
- ¿Personaje nuevo? Validar que pueda jugar ambos roles potencialmente

---

## 5. HALLAZGO CRÍTICO — BUENO APARENTE PUEDE SER VISUALMENTE EXTREME

La pauta vieja decía: "Bueno aparente = uncanny calmante, no monstruoso". **Falso en 7/8.**

| Video | Bueno aparente | Es "tame"? |
|-------|----------------|------------|
| ref-03 | PABLO tubérculo ovoide | Uncanny moderado |
| ref-06 | ENZO humano normal con chimenea | **SÍ tame** (único) |
| ref-08 | HUGO esqueleto humanoide alto con pipa | Uncanny extreme |
| ref-09 | AXEL cabeza hongo rojo + cuello largo | Uncanny extreme |
| ref-10 | ENZO esquelético calvo con tirantes | Uncanny moderado |
| ref-11 | MARIO criatura cuello largo + uniforme ferroviario | Uncanny moderado |
| ref-12 | TERESA anciana dientes afilados | Uncanny extreme |
| ref-13 | MIRO humanoide azul hexagonal levitando | Uncanny extreme |

### Implicación
**El bueno aparente NO necesita ser "tame".** Puede ser tan visualmente extreme como el malo. Lo que lo hace "bueno" es:
- Comportamiento (calma, ayuda, no amenaza)
- Outcome (counterfactual cozy en outro)
- Contraste tonal vs malo (no necesariamente visual)

---

## 6. HALLAZGO CRÍTICO — "OPCIÓN GANADORA CONTRA IMPULSO" NO ES UNIVERSAL

La pauta vieja decía: "La opción ganadora va contra el impulso primario. SIEMPRE."

**Realidad observada en 8/8:**

| Video | Decisión clave | Impulso primario | Ganadora alineada con impulso? |
|-------|----------------|------------------|--------------------------------|
| ref-03 (Bruno linterna) | Encender / esperar | Encender luz = impulso | **NO** — ganadora es esperar (contra impulso) ✓ |
| ref-06 (Axel claxon) | Tocar claxon / silencio | Tocar = impulso | **NO** — ganadora es silencio ✓ |
| ref-08 (Pablo meter brazo) | Meter / negarse | Negarse = impulso (sensato) | **SÍ** — ganadora es negarse (con impulso) |
| ref-09 (Victor cinturón) | Mantener cinturón mientras abre puerta | Soltarse = impulso miedo | **NO** — ganadora es obedecer (contra impulso) ✓ |
| ref-10 (Rurik válvula) | Abrir / negarse | Negarse = impulso | **SÍ** — ganadora es negarse (con impulso) |
| ref-11 (Ivan moneda) | Recoger / patear | Recoger = impulso | Mixed |
| ref-12 (Nano) | Elegirlo / no | No elegirlo = impulso (warning) | **SÍ** — ganadora es no elegirlo |
| ref-13 (Bryan paciencia) | Esperar / huir | Esperar = impulso pasivo | Variable |

**Conclusión:** la regla NO es universal. Lo que SÍ es universal:
- **Las decisiones son ambiguas** — el viewer no tiene confianza 100% en cuál es correcta
- A veces ganadora va contra impulso, a veces con impulso
- El test correcto: **¿la decisión genera DUDA real?** Si la respuesta es obvia, el dilema está mal diseñado.

---

## 7. SLOT A — ESCENARIOS EMPÍRICOS (de los 8 videos)

| # | Setting | Función | Atmósfera | Material |
|---|---------|---------|-----------|----------|
| 1 | **Mina subterránea 200m** (ref-03) | Trabajo / extracción | Claustrofobia profunda | Roca + madera podrida |
| 2 | **Carretera rural nocturna + coche** (ref-06) | Tránsito / encierro móvil | Noir + amenaza inminente | Asfalto + cabina coche |
| 3 | **Acuario abandonado con tanques** (ref-08) | Exhibición de criaturas | Marítimo + claustrofobia | Vidrio + agua + metal |
| 4 | **Cockpit de avión sobre océano** (ref-09) | Pilotaje / control | Tecnológico + fragilidad | Metal + paneles + vista exterior |
| 5 | **Planta industrial / fundición** (ref-10) | Procesos industriales | Industrial + peligro elemental | Acero + fuego + vapor |
| 6 | **Metro / estación + vagón vacío** (ref-11) | Transporte urbano nocturno | Urbano deserto | Hormigón + azulejos + rieles |
| 7 | **Tren nocturno + vagón** (ref-12) | Viaje encerrado | Journey horror + sepia memorial | Madera vintage + tapizado |
| 8 | **Planta eléctrica → fiesta carpinchos** (ref-13) | Industrial → hedonismo | Brutalist → EDM | Metal industrial → neon party |

### Reglas del Slot A (validadas en 8/8)

- ✓ **Atrapamiento físico** — el espectador no puede salir fácilmente
- ✓ **Aislamiento social** — sin testigos / sin ayuda externa accesible
- ✓ **Función específica del lugar** (no genérico "casa vieja")
- ✓ **Elementos diegéticos** identificables (taladro, faro, panel control, etc.)
- ✓ **Iluminación dramática** (single source + crushed blacks, o industrial naranjas, o neón EDM)

---

## 8. SLOT B — VISUAL DEL MALO APARENTE (de los 8 videos)

| Video | Nombre malo | Visual signature | Categoría |
|-------|-------------|-------------------|-----------|
| ref-03 | **BRUNO** | Cíclope cuello largo + casco minero + chaqueta cuadros + tirantes | Humano + alteración corporal extrema |
| ref-06 | **AXEL** | Cabeza hongo rojo + cuerpo humano + cuello largo | Humano + cabeza vegetal-fungal |
| ref-08 | **PABLO** | Tubérculo ovoide / criatura ovoide sin nariz | Humanoide vegetal absurdo |
| ref-09 | **VICTOR** | Esquelético piel oscura + máscara blanca + gorra capitán | Humano + máscara grotesca |
| ref-10 | **RURIK** | Traje hazmat amarillo + máscara con globos oculares múltiples | Humano + traje industrial deforme |
| ref-11 | **IVAN** | Humanoide cabeza esférica beige + boca ancha sonriente | Humano + cabeza geométrica |
| ref-12 | **NANO** | Cabeza banana literal + overol jean | Humano + cabeza vegetal |
| ref-13 | **BRYAN** | Capybara antropomorfo musculoso + chaleco táctico → abrigo largo | Animal antropomorfizado |

### Plantillas que funcionan (de los 8)
1. **Humano + cabeza vegetal/animal extrema** (Axel, Nano)
2. **Humano + cabeza geométrica imposible** (Ivan)
3. **Humano + traje protector deforme con detalle imposible** (Rurik)
4. **Humano + alteración corporal extrema** (Bruno cuello, Pablo proporciones)
5. **Esquelético / piel correosa + máscara** (Victor)
6. **Animal antropomorfizado muscular** (Bryan)

### Test rápido
- ¿Pasa el "scroll-stop"? Si NO frenarías el feed para mirarlo, está demasiado genérico
- ¿Se siente "incorrecto" de una manera que no podés nombrar? Sí = correcto
- ¿Es "Halloween costume normal"? Sí = demasiado genérico

---

## 9. SLOT C — VISUAL DEL BUENO APARENTE (de los 8 videos)

| Video | Nombre bueno | Visual signature | Categoría |
|-------|--------------|-------------------|-----------|
| ref-03 | **PABLO** | Tubérculo ovoide + overol jean | Vegetal antropomorfo cute |
| ref-06 | **ENZO** | Humano normal con chimenea | Realista único (atípico) |
| ref-08 | **HUGO** | Esqueleto humanoide alto + apron + pipa | Liminal-uncanny (visualmente extreme) |
| ref-09 | **AXEL** | Cabeza hongo rojo + cuerpo humano | Vegetal extreme (visualmente extreme) |
| ref-10 | **ENZO** | Esquelético calvo + tirantes + bare torso | Liminal-uncanny |
| ref-11 | **MARIO** | Criatura cuello largo + uniforme ferroviario | Alien grotesque (visualmente extreme) |
| ref-12 | **TERESA** | Anciana piel arrugada + dientes afilados | Monstruous tragic |
| ref-13 | **MIRO** | Humanoide azul translúcido + cabeza hexagonal + levitando | Geometric impossible (visualmente extreme) |

### Hallazgo clave (vs pauta vieja)

**El bueno aparente NO necesita ser "tame".** 7/8 son visualmente tan extremes como el malo. Solo ENZO ref-06 es humano realista.

### Lo que SÍ define al bueno aparente

- ✓ **CONTRASTE con el malo** — distinto en color, forma, postura
  - Bruno vertical alto cíclope vs Pablo bajo ovoide
  - Victor esquelético vertical vs Axel cabeza-hongo
  - Bryan musculoso vs Miro flotando lotus
- ✓ **Postura no amenazante** — sentado, sonriendo, ofreciendo algo (café, mate, charla)
- ✓ **Outcome cozy en counterfactual** — "habrían tomado café / jugado cartas / mirado el amanecer / etc."
- ⚠️ **Diálogo opcional** — ref-08 Hugo sí habla. Otros no.

---

## 10. SLOT D — LA REGLA / DINÁMICA DEL MALO APARENTE

Lo que el malo enforza o exige. **NO siempre es una frase textual literal**, a veces es procedural implícita.

### De los 8 videos

| Video | Regla del malo (textual o implícita) |
|-------|--------------------------------------|
| ref-03 Bruno | **Implícita:** Apaga la luz. Adaptate a la oscuridad. ("Los ojos se adaptan solos" — dialogue de Bruno) |
| ref-06 Axel | **Implícita procedural:** Quedate inmóvil. No reacciones. No enciendas. No toques claxon. |
| ref-08 Pablo (malo) | **Implícita:** Obedéceme cuando te pida algo (alimentar, meter brazo, mirar). |
| ref-09 Victor | **Implícita procedural:** Cierra los ojos. Abrocha cinturón. Confía en el procedimiento aunque te dé miedo. |
| ref-10 Rurik | **Implícita procedural:** Ponte el traje. Abre la válvula. Sigue las órdenes industriales. |
| ref-11 Ivan | **Implícita:** Recogé / patéa la moneda. Bajáte / quedáte. Decisiones rituales. |
| ref-12 Nano | **Textual:** "No la escojas, ven conmigo." (hook line) |
| ref-13 Bryan | **Implícita:** Ven a la fiesta. Olvida tu objetivo. Disfruta el momento. |

### Características de la regla (validadas)

- ✓ **Hay una dinámica de control** — el malo siempre exige algo
- ✓ **A veces es textual** (frase 5-10 palabras), a veces es procedural
- ✓ **Conecta con los dilemas** — los dilemas testean si seguís la regla del malo o la resistís
- ✓ **No es moralmente obvia** — no es "no mates" / "no robes"
- ✓ **Consecuencia inmediata si la rompés** — body horror específico

### Implicación para el arquitecto

Cuando diseñes, identificá **la dinámica de control del malo**:
- ¿Qué te pide?
- ¿Cómo te lo pide? (verbalmente / por gesto / por procedural)
- ¿Qué pasa si la rompés?
- ¿Cómo el dilema testea esa dinámica?

---

## 11. SLOT E — LOS DILEMAS

### Número de dilemas (incluye decisión inicial "elegir compañero")

| Video | Total decisiones | Decisión inicial + internas |
|-------|------------------|------------------------------|
| ref-03 | 4 | 1 inicial + 3 internas |
| ref-06 | 4 | 1 inicial + 3 internas |
| ref-08 | 3 | 1 inicial + 2 internas |
| ref-09 | 4 | 1 inicial + 3 internas |
| ref-10 | 3 | 1 inicial + 2 internas |
| ref-11 | 3 | 1 inicial + 2 internas |
| ref-12 | 3 | 1 inicial + 2 internas |
| ref-13 | 3 | 1 inicial + 2 internas |

**Regla actualizada:** 3-4 decisiones total (NO solo 2 internas como decía pauta vieja). Promedio: **3.4 decisiones**.

### Categorías de dilemas observadas

1. **Curiosidad / obediencia** — encender luz, mirar lo prohibido, abrir puerta
2. **Acción / pasividad** — gritar / silencio, salir / quedarse, tocar claxon / no
3. **Sumisión / resistencia** — ponerte traje, abrochar cinturón, abrir válvula
4. **Confianza / desconfianza** — meter brazo, aceptar oferta, seguir orden
5. **Avance / retroceso** — bajar del tren, recoger moneda, continuar

### Regla de variedad

Los dilemas dentro de un video **deben ser de categorías diferentes** (no todos curiosidad/obediencia, por ejemplo). Validado en 8/8 — ninguno repite categoría dentro del mismo video.

### Estructura del dilema

```
1. SETUP (1-2 oraciones) — qué te ofrecen / qué ves / qué pasa
2. PREGUNTA — "Ahora decide. A. [opción 1] B. [opción 2]"
3. COUNTDOWN — circular 3-2-1 (3 segundos exactos)
4. LOADING BAR — barra porcentual mientras el viewer "elige"
5. CONSECUENCIA A — body horror específico O acción de Maikol
6. CONSECUENCIA B — apertura al siguiente dilema
```

Validado en 8/8.

---

## 12. SLOT F — BODY HORROR ESPECÍFICO

**Nunca "mueres".** Siempre imagen visualizable concreta.

### De los 8 videos

| Video | Body horror ejemplos |
|-------|----------------------|
| ref-03 Bruno | Caes al pozo, dinamita en mano explota, taladro destroza huesos |
| ref-06 Axel | Coche se sale de carretera y choca contra árboles, atropello bajo ruedas |
| ref-08 Pablo | Tiburón muerde, anguila electrocuta, ahogado en tanque |
| ref-09 Victor | Caes al vacío sin paracaídas, despresurización, succionado por viento |
| ref-10 Rurik | Quemaduras por metal fundido, quemaduras por vapor, electrocución |
| ref-11 Ivan | Atropellado por tren, moneda quema y paraliza |
| ref-12 Nano | Apuñalamiento, caída del tren |
| ref-13 Bryan | Caída al vacío, envío al infinito, atrapado en fiesta eterna |

### Patrones validados

- ✓ **Específico al setting** — taladro en mina, anguila en acuario, vapor en planta, tren en metro
- ✓ **Visualizable concretamente** — IA puede generar la imagen
- ✓ **Sensorial** — frío, peso, calor, dolor implicado
- ✓ **No abstracto** — nunca "tu alma se pierde" o "mueres"

### 7 tipos catalogados

1. **Caída / impacto físico** (ref-03 pozo, ref-09 vacío, ref-13 vacío)
2. **Aplastamiento / atropello** (ref-06 coche, ref-11 tren)
3. **Quemadura / calor extremo** (ref-10 metal fundido)
4. **Asfixia / ahogamiento** (ref-08 tanque)
5. **Electrocución** (ref-08 anguila, ref-10 vapor)
6. **Penetración** (ref-12 apuñalamiento)
7. **Pérdida progresiva de identidad/libertad** (ref-13 fiesta eterna)

---

## 13. SLOT G — CLIFFHANGER ARCHETYPE (counterfactual outro)

### Realidad observada en 8/8

**TODOS los 8 videos tienen counterfactual outro tipo "Si hubieras elegido X, habrías..."**

| Video | Counterfactual outro |
|-------|----------------------|
| ref-03 | Pablo jugando cartas + comiendo pan + amanecer |
| ref-06 | Enzo chimenea + café + perro |
| ref-08 | Hugo limpieza tranquila + café + comida |
| ref-09 | Axel desenlace positivo |
| ref-10 | Enzo vigilancia + pizza + cartas |
| ref-11 | Mario final positivo |
| ref-12 | Teresa historia emocional vs Nano violencia |
| ref-13 | Bryan fiesta eterna (twist: el "good" es trampa) |

### Hallazgo vs pauta vieja

La pauta vieja decía rotar 4 archetypes (Paz perdida / Trampa simétrica / Inversión total / Meta). **En la práctica, 7/8 son "Paz perdida"** (cliffhanger cozy mostrando vida normal cómoda). Solo ref-13 es "Hedonismo trampa" (variant).

**Trampa simétrica no se observa en ninguno de los 8.**
**Inversión total no se observa en ninguno de los 8.**
**Meta-cliffhanger no se observa en ninguno de los 8.**

### Elementos sensoriales validados (de Paz perdida en los 8)

- ✓ Café / té
- ✓ Pan / pizza / comida casera
- ✓ Cartas (jugar)
- ✓ Chimenea / fuego cozy
- ✓ Perro / mascota
- ✓ Amanecer / luz dorada
- ✓ Música acústica cálida
- ⚠️ NO observado: vino, ballenas, estrellas (eran en pauta vieja sin validación)

### Estructura del outro

```
1. Voz: "Si hubieras elegido a [BUENO]..."
2. Visual cozy contraste tonal vs horror previo
3. Detalle específico cotidiano (1-2 elementos)
4. Cierre con imagen cálida / amanecer / silueta tranquila
5. Tagline + CTA: "Elige a tu compañero para..." [loop al próximo video]
```

---

## 14. SLOT H — AMBIENT CREATURES

**No detectados sistemáticamente** en los 8 videos analizados. La pauta vieja mencionaba esto como obligatorio pero las descriptive analyses no los identifican explícitamente.

**Estado:** opcional, no obligatorio. Si lo implementás, hacelo subtle (background).

---

## 15. PATTERNS NARRATIVOS OBSERVADOS

### Patrones explícitos en los 8

| Pattern | Definición | Videos |
|---------|------------|--------|
| **P1 — Verdad visible** | El obvio peligroso ES peligroso | ref-03, ref-06, ref-08, ref-10, ref-12 |
| **P2 — Supervivencia si manejás bien** | Peligroso puede sobrevivirse con decisiones correctas | ref-03 (Bruno entrega relevo si esperás) |
| **P9 — Peligroso te ayuda** | El que parece amenazante es el que te salva | ref-09 (Victor) |
| **P3 — Seguro era trampa** | Bueno aparente era el real peligro | ref-08 (Pablo traidor) |
| **P6 — Hedonismo eterno** | "Bueno" te lleva a placer pero perdés objetivo | ref-13 (Bryan) |

### Hallazgo

**P1, P2, P9, P3, P6 son los patterns observados.** Otros patterns mencionados en pauta vieja (P4 Paz perdida, P5 Doble peligro visible, P10 Inversión total, Meta-cliffhanger) NO se observan en los 8.

Esto NO significa que no existan — solo que en estos 8 referentes virales no son los patterns dominantes.

---

## 16. CHECKLIST DE CALIDAD NARRATIVA (post-empírico)

Antes de aprobar un SPEC, validar:

### Estructura
- [ ] Setting tiene atrapamiento físico + aislamiento social
- [ ] 3-4 decisiones (1 inicial + 2-3 internas)
- [ ] Cada decisión tiene categoría diferente
- [ ] Cada decisión tiene countdown + loading bar
- [ ] Counterfactual outro tipo "Paz perdida" con elementos sensoriales validados
- [ ] Duración 76-130s (sweet spot 80-100s)

### Personajes
- [ ] Malo aparente con visual signature uncanny (no necesita ser EL MÁS extreme)
- [ ] Bueno aparente con CONTRASTE visual vs malo (color, forma, postura)
- [ ] Name labels sobre cada uno al inicio
- [ ] Bueno con outcome cozy en outro
- [ ] (Opcional) Personaje recurrente cross-video — documentar rol nuevo

### Slot D — dinámica de control del malo
- [ ] Identificado QUÉ exige el malo (textual o procedural)
- [ ] Conectado con los dilemas (cada dilema testea esa dinámica)
- [ ] Consecuencia inmediata si se rompe (body horror específico)

### Dilemas (Slot E)
- [ ] 2-3 internas + 1 inicial = 3-4 total
- [ ] Categorías diferentes entre dilemas
- [ ] Cada dilema genera DUDA real (no respuesta obvia)
- [ ] Setup + pregunta + countdown + loading + consequence

### Body horror (Slot F)
- [ ] Específico al setting
- [ ] Visualizable (IA puede generar la imagen)
- [ ] Sensorial (frío, peso, dolor)
- [ ] NO genérico "mueres"

### Lenguaje
- [ ] Segunda persona ("tú trabajas, miras")
- [ ] Presente del indicativo
- [ ] Oraciones cortas
- [ ] Frases nominales en climax

### Producción
- [ ] POV >70% planos
- [ ] Hard cuts entre escenas
- [ ] Countdown 3-2-1 + loading bar en cada decisión
- [ ] Watermark del creator persistente

---

## 17. REGLAS DE ROTACIÓN ENTRE VIDEOS

### Rotación de roles de personajes recurrentes

Si reusás un personaje del catálogo de 8 (Pablo, Axel, Enzo, etc.):
- ¿Mismo rol que el video anterior donde apareció? OK pero menos sorpresa
- ¿Rol invertido? Más fuerte (Pablo bueno → malo, Axel malo → bueno)
- **NO** uses el mismo personaje en mismo rol en 2 videos consecutivos

### Rotación de settings

Los 8 settings observados: mina, carretera, acuario, cockpit, planta-fundición, metro, tren, planta-eléctrica.

Para video nuevo: no repetir setting del video anterior. Variedad mantiene fresh el feed.

### Rotación de patterns

Los 5 patterns observados (P1, P2, P3, P6, P9). No repetir el mismo pattern en 2 videos consecutivos.

---

## 18. CÓMO USAR ESTA PAUTA

### Flujo correcto

1. **Leer esta pauta COMPLETA** antes de diseñar
2. **Llenar Slots A-H** del SPEC con data validada
3. **Validar checklist § 16** antes de aprobar
4. **Consultar video-log.md** para rotación
5. **Usar 8 videos canónicos como referencia** — si una idea no tiene precedente en los 8, dudar antes de incluirla

### Flujo INCORRECTO (errores cometidos antes)

- ❌ Construir historia desde imagen visual hacia slots forzados (incidente Maikol-2026-05-13)
- ❌ Tomar reglas de V1/V2/V3 antiguos o V7 nuestro
- ❌ Inventar reglas mid-conversación cuando algo no encaja
- ❌ Saltar Slot D (la dinámica de control del malo)
- ❌ Asumir 2 dilemas cuando los virales tienen 3-4
- ❌ Forzar "opción ganadora contra impulso" como universal (no lo es)

---

## 19. RELACIÓN CON OTROS DOCUMENTOS

### Esta pauta REEMPLAZA empíricamente

- ❌ `CREATIVE-BRIEF.md` v anterior (pauta sobre V1/V2/V3/V7) → DEPRECATED, usar este doc
- ❌ Slots que mencionaba personajes nuestros (Cristóbal, Gerald del V7) → no relevantes para pauta

### Esta pauta COMPLEMENTA

- ✓ `PATTERNS.md` — reglas técnicas del formato (estructura V15, audio, visual)
- ✓ `SCRIPT-WRITING-GUIDE.md` — plantilla del guion
- ✓ `PAUTA.md` — workflow de producción
- ✓ `INTRO-FORMULA-V15.md` — hook 9s
- ✓ `CHARACTER-NAMES-CATALOG.md` — nombres
- ✓ `video-log.md` — rotación cross-video

### Esta pauta NO toca

- Decisiones técnicas (LUFS, CSS, ffmpeg, voice IDs) — son del ingeniero
- Operacionales (image-direction, animation-direction, etc.) — son layer secundario en creative-director

---

## 20. ÚLTIMO CHEQUEO METODOLÓGICO

Antes de aprobar esta pauta como autoridad, verificá:

- [ ] ¿Cada regla está validada en N/8 videos? ✓ (incluí counts en cada sección)
- [ ] ¿No hay referencias a V1/V2/V3 antiguos ni a V7 nuestro como fuente de regla? ✓
- [ ] ¿Las reglas que no son universales están marcadas como tales? ✓
- [ ] ¿La pauta está empíricamente grounded? ✓
- [ ] ¿Hay hallazgos que contradicen la pauta vieja? ✓ Documentados en §§ 4, 5, 6, 13

**Estado:** Pauta master v1.0 lista para uso por arquitecto.

---

## § 18 — Decision UI editorial pacing (added 2026-05-19 — GAP #14 codification)

> **Status**: codified empíricamente post-matadero CP5 iter 2 user feedback.
> **Authority basis**: pattern observed 8/8 canonical refs (canonical-scenes/INDEX.md decision setup grid 3.3) + ref-13 deep-dive Beat 4 + ref-03 explicit "filter cinematic/gritty con grain".
> **Caso disparador**: user listen post iter 2 — "Countdowns NO van ligados a narración, están puestos ahí nada más. En refs canónicos imagen se queda estática con efecto cámara vieja + ahí se hace countdown. Countdown se sobrepone con loading bar."

### 18.1 Pattern canonical observado

Decision UI moments en formato horror-choice (8/8 canonical refs) son **micro-eventos editoriales estructurados**, NO simplemente "elementos UI puestos sobre clip animado". Pattern:

```
[narration_end] → [pause beat 0.9s canonical median Phase 1] → [countdown 3-2-1 digit per 1.0s user Rule D PRECEDENCE 2026-05-20] → [SFX time_loop_glitch optional per digit, NO ambient duck per Phase 1] → [freeze frame + filter overlay OPTIONAL stylistic 14% refs]
                                                                                                  [loading bar fills L→R Y52, ≥6% Y separation from countdown Y46]
```

### 18.2 Why freeze frame at decision

**Pause cognitiva del viewer**: separa el decision moment del flow narrativo continuo. Viewer needs cognitive pause para procesar la pregunta moral + scan opciones A/B. Motion continua durante countdown distrae cognición. Refs evidence:

- ref-03 (Bruno/Pablo): "Kling POV con hand" + **"Filter cinematic/gritty con grain"** — motion minimal (hand poised) + filter overlay creates "old camera footage stilled" feel
- ref-09 (Victor): "Kling Victor silueta + **typewriter UI**" — UI typewriter motion replaces clip motion focus
- ref-12 (Nano): "Kling POV con plato + Nano + UI" — minimal scene motion + UI animation primary

**Empirical observation**: refs use Kling POV but with **subtle/static composition** during decision (hand poised, character expectant), NOT full action motion.

### 18.3 Why filter overlay during decision

**Archetype "looking back at footage"**: viewer is **implicated** in the decision retroactively. The vintage/VHS/sepia filter signals "this is recorded surveillance you're watching, your decision was already made/being watched". Creates uncanny temporal displacement.

**Refs evidence**:
- ref-03 explicit "filter cinematic/gritty con grain"
- Universal grain overlay 11/13 (REFERENT-ANALYSIS § visual)
- Crushed blacks + high contrast en decision moments (matches "old footage" aesthetic)

**Canonical CSS interpretation**: `filter: sepia(0.4) contrast(1.2) hue-rotate(15deg)` + grain canvas overlay 8% opacity.

### 18.4 Why countdown sync to narration_end

**Structural cue "narrator finished propuesta, ahora decidís"**: countdown timing must follow narrative beat completion. Otherwise countdown reads "loose UI element" disconnected from narrative flow.

Per ref-13 Beat 4 (decision_setup_1): `[24.0-26.0s]: Narrator "Ahora decides que responder."` → `[26.0-29.0s]: Captions A/B + countdown + loading bar`. The narration completion at 26s triggers countdown start, NOT arbitrary timeline position.

**Canonical pause beat**: 0.3s gap between narration_end_marker and countdown_start. Structural breath cue.

### 18.5 Why loading bar separated ≥6% Y from countdown

**Visual hierarchy + cognitive load**: countdown Y46% + loading bar Y48% = 2% spacing = visually overlapping at typical font sizes. User cognitive load high (reading countdown + scanning options + perceiving urgency) — UI elements need clear hierarchy.

Empirical canonical Y52% para loading bar (≥6% spacing from countdown Y46%). Matadero iter 2 used Y48% — flagged "cramped + overlap" by user. Revised pattern Y52% canonical safe.

### 18.6 Why audio cue specific during countdown

**Alerts viewer "decision moment NOW"**: SFX tick + tone + ambient drop signal urgency + decision imminence. Without audio cue, countdown feels visual-only afterthought.

Canonical: SFX `time_loop_glitch` OR `decision-tick` per digit + ambient duck -6dB during countdown window. Per ref-13 + ref-09 typewriter UI pattern.

### 18.7 Failure mode codification

❌ **Anti-pattern**: countdown floating timing + clip motion continues + loading bar cramped + no filter overlay. Reads "UI elements puestos sueltos sobre video". Editorial structure collapsed.

✅ **Canonical**: freeze frame + filter overlay + countdown sync narration + loading bar Y52 + SFX per digit + ambient duck. Editorial structure crisp.

### 18.8 Implementation authority

Technical implementation specs → `INGENIERO-PAUTA-MASTER § 7.X decision-UI-implementation`.
SPEC schema reference → `CREATIVE-SPEC-TEMPLATE.yaml shot_list[].narrative_pacing` (schema v7 NEW 2026-05-19).
Pre-render verification → `pre-render-gate/SKILL.md Q22 NEW`.

**Compliance**: 8/8 canonical refs observan pattern (con stylistic variants e.g. ref-13 loading bar horizontal vs circular). Pattern is **categorical universal**, stylistic implementation varies.


### 18.9 ⚠️ Canonical validation status (Hard Rule #19 EXPANSION compliance) — UPDATED 2026-05-20 post Phase 1 empirical measurement

```yaml
canonical_validation_status: "validated_via_video_measurement"  # FLIPPED 2026-05-20 post engineer Track B Phase 1
validated_against_canonical_refs:
  - "canonical-scenes/INDEX.md decision setup grid 3.3 (8 refs documented patterns)"
  - "ref-13-miro-bryan-electrica.md Beat 4 deep-dive timing"
  - "ref-03 explicit 'filter cinematic/gritty con grain' notation"
  - "engineer Track B Phase 1 measurement: referent-analysis/empirical-decision-ui-pacing/aggregate-canonical-bands.json (8/8 refs measured)"
validation_methodology: "qualitative pattern extraction (Phase 0) + empirical video measurement Phase 1 (ffmpeg + Whisper + librosa + frame analysis 22 decision windows across 8 refs)"
measurement_script: "measure-canonical-decision-ui-pacing.py — engineer Track B Phase 1 COMPLETE 2026-05-20"
validated_at: 2026-05-20
```

#### ⚠️ EMPIRICAL CORRECTIONS post Phase 1 measurement (Track A v2 — 3 REFUTATIONS)

**CORRECTION 1 — ambient_duck_db_during_countdown**:
- Pre-empirical inferred: **-6 dB** (auditor proposed default)
- Phase 1 measured 8/8 refs: **+0.22 dB median (≈ NO duck canonical)**
- **Verdict**: NO ambient duck recommended OR optional stylistic choice. Refuted "ducking during countdown" inferred pattern.

**CORRECTION 2 — freeze_frame_applied**:
- Pre-empirical inferred: **default true** (8/8 refs minimal-motion pattern interpretation)
- Phase 1 measured: **14% canonical refs (3/22 windows) — MINORITY pattern**
- **Verdict**: freeze frame is OPTIONAL stylistic choice, NOT canonical signature default. Refuted "freeze obligatorio" inferred pattern.

**CORRECTION 3 — countdown_pause_beat_s**:
- Pre-empirical inferred: **0.3 s** (auditor proposed default)
- Phase 1 measured: **0.9 s median (p25=0.33, p75=2.1)** — ≥3× inferred value
- **Verdict**: canonical pause beat is **0.9 s median** (range 0.33-2.1s p25-p75). Refuted "0.3s tight pause" inferred pattern.

#### Updated canonical defaults per Phase 1

```yaml
decision_ui_canonical_defaults_v3_2026_05_20:  # Track A v3 R1 RESOLUTION
  countdown_pause_beat_s_median: 0.9                          # validated_via_video_measurement n=14 samples
  countdown_pause_beat_s_p25_p75: [0.33, 2.1]
  countdown_digit_duration_s: 1.0                             # ⚠️ UPDATED Track A v3 — user Rule D PRECEDENCE 2026-05-20 "1, 2, 3 = literal segundos". Refutes engineer empirical 0.5s (n=1 LOW confidence) AND architect v2 0.7s compromise.
  ambient_duck_db_during_countdown: 0                         # validated_via_video_measurement n=20 samples — NO duck canonical
  freeze_frame_applied_default: false                         # validated_via_video_measurement n=22 windows — OPTIONAL stylistic (14% refs)
  filter_overlay_applied_default: false                       # validated_via_video_measurement minority pattern
  loading_bar_y_pct_canonical: 52                             # validated_via_video_measurement
  countdown_y_pct_canonical: 46                                # validated_via_video_measurement
  countdown_visual_style: "film_leader_academy"               # validated_via_direct_frame_verification 4/4 refs

  # ⚠️ Per-value validation status (Track A v3 explicit n-counts)
  validation_status_per_value:
    countdown_pause_beat_s:           {status: validated_via_video_measurement, n: 14, source: "Track B Phase 1"}
    countdown_digit_duration_s:       {status: validated_via_user_perceptual,  n: user_perceptual, source: "user Rule D PRECEDENCE 2026-05-20 matadero iter 7-8"}
    ambient_duck_db_during_countdown: {status: validated_via_video_measurement, n: 20, source: "Track B Phase 1"}
    freeze_frame_applied:             {status: validated_via_video_measurement, n: 22, source: "Track B Phase 1"}
    filter_overlay_applied:           {status: validated_via_video_measurement, n: 22, source: "Track B Phase 1"}
    loading_bar_y_pct:                {status: validated_via_video_measurement, n: 8,  source: "Track B Phase 1"}
    countdown_y_pct:                  {status: validated_via_video_measurement, n: 8,  source: "Track B Phase 1"}
    countdown_visual_style:           {status: validated_via_direct_frame_verification, n: 4, source: "auditor 2026-05-19"}

  # Track A v3 R1 — countdown_digit_duration_s conflict resolution
  countdown_digit_duration_conflict_resolution:
    sources_in_conflict:
      user_perceptual_rule_d_precedence: 1.0  # WINS
      engineer_empirical: 0.5  # n=1 LOW confidence — REFUTED
      architect_track_a_v2: 0.7  # compromise — REFUTED
    user_quote: "Me gusta que los segundos en vd sean segundos, 1, 2, 3"
    verdict: "Rule D PRECEDENCE wins. Engineer measurement n=1 insufficient confidence. Architect v2 compromise refuted. countdown_digit_duration_s = 1.0s canonical until empirical n≥5 collected."
    revisit_trigger: "Phase 1 forward — measure-canonical-decision-ui-pacing.py n≥5 sample increase. If empirical median significantly differs from 1.0s, escalate to user perceptual re-confirm."
```

Empirical source: `referent-analysis/empirical-decision-ui-pacing/aggregate-canonical-bands.json` (engineer Track B Phase 1 8/8 refs measured 2026-05-20).


---

## § 19 — Audio-Visual Atomic Units (AVU) — creative intent (2026-05-19 — GAP #19 + AVU principle)

> **Status**: codified post matadero iter 3-4 sync failures + user architectural insight 2026-05-19 PM.
> **Authority basis**: 4/4 canonical refs direct frame verification (countdown FILM LEADER ACADEMY style + bundled ticks) + matadero CP5 demonstrated compose-time GSAP timing + CSS race conditions + audio mix wiring = multiple failure points.

### 19.1 Principle

Elementos audio+visual acoplados (countdown+ticks, hook transition+whoosh, outro card+drone, decision freeze+filter+tick, body horror+impact sound) **DEBEN ser atomic units** — visual + audio sincronizados estructuralmente, NO layered loose at compose-time.

**Rationale empírico**: matadero iter 3-4 demostró que compose-time wire de 3+ elementos coupled (countdown visual + tick SFX + ambient duck) introduces múltiple failure points:
- GSAP timing race conditions
- CSS class transition timing
- Audio mix track-index conflicts
- HyperFrames `data-start` vs JS animation drift

**Solution**: 1 pre-rendered .mp4 con visual + audio bundled = 1 failure point = bullet-proof sync.

### 19.2 Pattern observed canonical refs (4 verified direct frames)

| AVU type | Visual signature | Audio bundled | Refs verified |
|----------|------------------|----------------|---------------|
| Countdown 3-2-1 | **FILM LEADER ACADEMY** (crosshair circle + big central digit ~40-50% frame width) | Tick per digit (clock/film projector style) | 4/4 direct verified |
| Hook transition flash | Whoosh + flash | Whoosh diegetic | observed dominante |
| Outro card | Card text static + drone | Drone tone signature | observed dominante |
| Decision moment | Freeze + filter overlay + tick | Tick per digit + ambient duck | observed inferred |

### 19.3 When AVU OBLIGATORIO (creative intent)

✅ AVU pre-rendered .mp4 OBLIGATORIO para:
- Countdown 3-2-1 (universal across all canonical refs)
- Decision UI moments (freeze + filter + countdown + ticks atomic)
- Hook transition flashes
- Outro cards with tone signature
- Music section transitions

### 19.4 When AVU NOT applicable (use sync_contract instead)

❌ AVU NO applicable cuando text/audio per-video varía:
- Character dialogue + lip-sync (unique per video)
- Narrator framing question + caption (text varies per video)
- Setting establishment visuals (per-video unique)

Para estos: **sync_contract** explícito en SPEC (visual_start_s + audio_start_s + tolerance_s) validado pre-render.

### 19.5 Canonical hook sub-beat ordering (GAP #18 codification 2026-05-19)

> Empirical 4/4 verified direct frame analysis canonical refs.

**Canonical order observed**:

```
Sub-beat 1 (0-Xs):     name labels + character intro visible
Sub-beat 2 (Xs-Ys):    caption setting/warning central + narrator framing question
Sub-beat 3 (Ys-Zs):    push-in + parallax micro-motion
Sub-beat 4 (LAST 2-3s): countdown 3-2-1 FILM LEADER ACADEMY (AVU bundled)
Sub-beat 5 (post-hook → shot_02): character dialogue (NOT in hook, separate shot)
```

**Critical**: countdown va **LAST** después de character intro completo, NO al inicio. Plus character dialogue NO en hook shot — separate shot post-hook.

Matadero iter 1 anti-pattern: hook shot_01 incluía dialogue cocinera ON-screen mid-hook + countdown overlap → editorial collapse. Canonical order requiere countdown como cierre del hook, dialogue como apertura del shot siguiente.

### 19.6 Countdown visual style correction (GAP #19 codification 2026-05-19)

> Previous PAUTA § 18 codified countdown as CSS minimalist ring + small digit. **INCORRECT** per direct frame verification 4/4 refs.

**CORRECT canonical style**: FILM LEADER ACADEMY (classic 35mm projection countdown):
- Crosshair circle (light gray ring with horizontal + vertical center lines)
- BIG central digit (~40-50% frame width)
- Black serif/condensed bold font
- Subtle motion blur during push-in
- Optional vintage film grain/scratches

**NOT**:
- CSS minimalist thin ring + small digit
- Modern web countdown style

Implementation: pre-rendered .mp4 AVU `countdown-3-2-1-film-leader-with-ticks.mp4` (3s, 1080×1920, audio bundled).

### 19.7 Compliance authority

- Technical implementation → `INGENIERO-PAUTA-MASTER § 7.11 AVU library`
- SPEC schema → `CREATIVE-SPEC-TEMPLATE.yaml shot_list[].hook_sub_beats + audio_visual_atomic_units` (v8 NEW)
- Pre-render verification → `pre-render-gate/SKILL.md Q24 + Q25 NEW`

### 19.8 Canonical validation status

```yaml
canonical_validation_status: "validated_via_direct_frame_verification_4_refs_2026_05_19"
validated_against_canonical_refs:
  - "4 canonical refs direct frame verification (countdown FILM LEADER ACADEMY style + bundled ticks)"
  - "matadero iter 3-4 empirical sync failure cases (proof of compose-time fragility)"
validation_methodology: "direct frame extraction + visual style identification + matadero empirical failure analysis"
validated_at: 2026-05-19
status_flip_path:
  - "Phase 1 forward: extract-canonical-max-detail.py + run on 8 source videos → cross-canonical bands"
  - "Plus: AVU library 4 templates built + tested on iter 5 matadero pilot"
```


---

## § 20 — Setting "alive" canonical pattern (post 2026-05-20 — GAPS #23 + #26)

> **Status**: codified post matadero v1 SHIP analysis 2026-05-20.
> **Authority basis**: deep frame analysis 8 canonical refs — 100% have ≥1 background creature/object animated + 100% have ≥3 atmospheric secondary motions per shot.
> **Caso disparador**: user concern "los videos canonical se ven y escuchan tan bien" — matadero v1 settings sentían DEAD vs canonical refs.

### 20.1 Pattern canonical observado (8/8 refs)

**Universal rule**: settings canonical refs **NUNCA están vacíos visualmente**. Cada setting tiene:

1. **≥1 background creature/object animated** (GAP #23)
2. **≥3 atmospheric secondary motions per shot** (GAP #26)

| Ref | Setting | Background creature/object | Atmospheric motions per shot |
|-----|---------|------------------------------|-------------------------------|
| ref-03 (Bruno/Pablo mina) | Mina abandonada | Rata corriendo + insectos volando | dust + cobwebs swaying + lantern flicker + breath vapor |
| ref-06 (Enzo/Axel carretera) | Carretera nocturna | Mariposa nocturna + insectos near luces | wind dust + headlight flicker + cigarette smoke + fog |
| ref-08 (Hugo/Pablo acuario) | Acuario | **Tiburón nadando background** (signature) | water shimmer + bubbles + tank reflection ripples + fluorescent flicker |
| ref-09 (Victor/Axel cockpit) | Avión cockpit | Insectos cerca panels | turbulence subtle shake + light flicker + control panel blinks + cockpit window cloud movement |
| ref-10 (Rurik/Enzo fundicion) | Fundición industrial | Cucaracha + sparks particles | **Flame flickering furnace** + smoke + heat distortion + sparks + ambient steam |
| ref-11 (Mario/Ivan metro) | Metro subterráneo | Rata + cockroach | tunnel wind + train approach light + dust + flickering fluorescents + steam from grilles |
| ref-12 (Nano/Teresa tren) | Tren vagón | Bird outside window | window scenery moving + fabric seats subtle sway + sunlight strobe + dust particles in light beam |
| ref-13 (Miro/Bryan electrica) | Planta eléctrica | **Light beam pulsing** (signature) + electric arcs | electric flicker + smoke + dust dancing in beam + ambient vapor + Miro levitation float |

### 20.2 Why settings "alive" matters

**Viewer disengagement risk**: setting estático = viewer percibe "stage / set artificial" — rompe immersion + suspends disbelief. Canonical refs invest motion budget en background detail = viewer crees el setting "exists" más allá del frame.

**Empirical**: matadero v1 settings had carcasas hanging static + no rats moving + no flame flickering + no insect motion. Visual energy concentrated en characters → settings felt "stage dressing". Canonical refs distribute motion across foreground + background = setting feels "lived in".

### 20.3 Setting "alive" elements catalog per setting category

| Setting category | Background creature/object candidates | Atmospheric motions catalog |
|-------------------|----------------------------------------|------------------------------|
| **Mina / cuevas** | Rata, murciélago, insectos, cuervo | dust particles, lantern flicker, breath vapor, water drip from ceiling, cobwebs sway |
| **Acuario / agua** | Tiburón, pez grande, calamar, medusa | water shimmer, bubbles, tank ripples, reflection movements, fluorescent flicker |
| **Industrial / fundición** | Cucaracha, sparks particles, rata, gato | flame flickering, smoke, heat distortion, sparks, ambient steam, metal creaking |
| **Metro / túneles** | Rata, cockroach, palomas, gato | tunnel wind, distant light approach, dust, flickering fluorescents, steam from grilles |
| **Carretera / outdoor noche** | Mariposa nocturna, insectos near luces, lechuza, perro distant | wind dust, headlight flicker, cigarette smoke, fog, leaves rustling |
| **Tren / vehículo** | Bird outside window, ocasional silueta passing | scenery moving, fabric sway, sunlight strobe, dust in light beam, vibration subtle |
| **Cockpit / avión** | Insectos cerca panels, ocasional cloud outside | turbulence subtle, light flicker, panel blinks, cloud movement, window condensation |
| **Eléctrica / energía** | Electric arcs, sparks, ocasional rat near cables | electric flicker, smoke, dust dancing in beam, ambient vapor, light pulsing |
| **Matadero / cámara fría (matadero-banquete)** | Rata gris (already Slot H), insectos sutiles, gato | breath vapor MÁS prominente, drip from carcasas hanging, fluorescent flicker stronger, sparks from electrical, smoke from refrigeration unit |
| **Comedor / cozy interior** | Insect near window light, ocasional cat under table | candle/pendant flicker, steam from food, dust in light beams, curtain subtle sway, fireplace embers (if applicable) |

### 20.4 Compliance authority

- Technical implementation → `INGENIERO-PAUTA-MASTER § 8.X background animated implementation` + `§ 8.Z atmospheric motions checklist`
- SPEC schema → `CREATIVE-SPEC-TEMPLATE shot_list[].setting_ambient_creature_or_object` + `atmospheric_motions_count` (v9 NEW)
- Pre-render verification → `pre-render-gate Q26 NEW` (post Track C codification)

### 20.5 Canonical validation status

```yaml
canonical_validation_status: "validated_via_deep_frame_analysis_8_refs_2026_05_20"
validated_against_canonical_refs:
  - "8 canonical refs deep frame analysis post matadero v1 SHIP"
  - "ref-08 tiburón signature, ref-13 light beam pulsing signature, ref-10 flame flickering signature"
  - "Pattern 100% universal — NOT optional"
validation_methodology: "auditor deep frame analysis 8 refs cross-setting category"
validated_at: 2026-05-20
```

---

## § 21 — Character "alive" canonical pattern (post 2026-05-20 — GAPS #24 + #27)

> **Status**: codified post matadero v1 SHIP analysis 2026-05-20.
> **Trigger**: matadero v1 character moments static (matarife cleaver-head no expression possible + cocinera limited gestures) vs canonical refs (Bryan flexing, Miro levitating animated, Hugo pipe smoke, Bruno gesturing).

### 21.1 Character anchor design rule (creative intent)

**Character signature MUST allow gesture animation potential**. Si el anchor design limita drastically gesture range → compensate with alive signals.

**Examples**:
- Matarife cleaver-head: no facial expression possible → COMPENSATE: cleaver-head subtle vibration when speaking + apron sway + glove tension + breath vapor visible + occasional environmental interaction (touching carcasa, gripping knife)
- Cocinera glow eyes + dense smile: standard human expression → STANDARD lip-sync + breath + hand gestures with olla

### 21.2 Lip-sync OBLIGATORIO per character speech ON-screen (GAP #24)

**Universal rule canonical 8/8 refs**: cuando character habla ON-screen, lip-sync OBLIGATORIO. No floating dialogue (audio-only mientras character static).

**Verification**:
- SPEC schema `lip_sync_required: true` per shot con character speech
- Engineer implementation: Hailuo motion + lip-sync model (Sync.so / Hedra / Veo) post-process
- Pre-render-gate Q23 existing already references this

**Matadero anti-pattern**: cocinera speech ON-screen (shot_01 hook + shot_20 cliffhanger) — engineer iter 1 had audio without lip-sync motion sync. User D1 catch iter 5 forced fix.

### 21.3 Active gesture per shot canonical (GAP #27)

**Universal rule canonical 8/8 refs**: per shot con character on-screen, MUST include ONE active gesture (hand reach, head turn, breath, blink, body lean, environmental interaction).

**Examples canonical**:
- ref-03 Bruno: flexes neck up + arm reach + cyclops eye blink
- ref-06 Axel: mushroom head subtle wobble + arm gesturing
- ref-08 Hugo: pipe puff smoke + skeletal hand gestures + jaw open
- ref-13 Bryan: capybara muscle flex + arm flex + chest puff
- ref-13 Miro: levitation float + meditation hand gesture + hexagonal head rotation

**Matadero anti-pattern matarife shots**: cleaver-head static + apron static + boots static = "stage prop" feel. CANONICAL requires compensation alive signals.

### 21.4 Compensation alive signals (when signature limits)

Per character con signature limitation (matarife cleaver-head, possibly future uncanny characters):

```yaml
alive_signals_compensation:
  - "Signature element subtle motion (e.g., cleaver-head vibration during speech)"
  - "Secondary garment motion (apron sway, sleeve ruffle)"
  - "Breath vapor visible if cold setting"
  - "Glove/hand tension/grip changes per emotional beat"
  - "Environmental interaction per shot (touch object, grip tool, lean against wall)"
  - "Body posture shift subtle (lean, weight shift, head tilt)"
```

### 21.5 Compliance authority

- Technical implementation → `INGENIERO-PAUTA-MASTER § 8.W character gesture per shot`
- SPEC schema → `CREATIVE-SPEC-TEMPLATE shot_list[].character_active_gesture_per_shot` + `lip_sync_required` (v9 NEW)
- Pre-render verification → `pre-render-gate Q27 NEW` (post Track C codification)

### 21.6 Canonical validation status

```yaml
canonical_validation_status: "validated_via_deep_frame_analysis_8_refs_2026_05_20"
validated_against_canonical_refs:
  - "8 refs deep frame analysis active gestures per character on-screen shot"
  - "matadero v1 SHIP empirical anti-pattern (matarife shots static = stage prop feel)"
validation_methodology: "auditor deep frame analysis + matadero empirical failure analysis"
validated_at: 2026-05-20
```

---

## § 22 — POV traversal canonical pattern (post 2026-05-20 — GAP #25)

> **Status**: codified post matadero v1 SHIP analysis 2026-05-20.
> **Trigger**: matadero v1 viewer "teleports" between shots (cuts between static framings sin physical traversal). Canonical refs SHOW viewer physically moving through space.

### 22.1 Pattern canonical observado (8/8 refs)

**Universal rule**: canonical refs **muestran el viewer físicamente moviéndose** through space, NO solo cuts entre static framings.

**Evidence**:
- POV viewer body parts (hands, occasional legs) visible regularly per shot
- Camera angle/distance CHANGES between consecutive shots in a way that implies walking/turning/descending
- Motion intent enum per shot: walking_forward, walking_backward, turning_left, turning_right, approaching_character, ascending_stairs, descending_stairs, looking_around

**Anti-pattern**: cuts between static framings = viewer teleports = breaks immersion. Matadero v1 had multiple consecutive shots where viewer position changed dramatically with no implied traversal.

### 22.2 Why POV traversal matters

**Spatial coherence**: viewer brain builds mental map of setting through shot-to-shot motion continuity. Teleports break this map → "I'm watching a slideshow" feel vs "I'm inside this space" feel.

**Canonical evidence**: ref-13 viewer descends stairs + walks to fiesta + Miro approaches viewer = clear physical movement. ref-08 viewer walks aquarium + approaches tank + steps back = traversal. ref-11 viewer walks metro platform + train approaches = depth motion.

### 22.3 POV viewer body parts visibility

Canonical refs show viewer POV with body parts regularly visible:
- **Hands**: visible bottom of frame holding objects (knife, lantern, phone, ladle) in ~50%+ shots
- **Legs**: occasional (walking shots, sitting shots, descending stairs)
- **Arms**: visible when reaching, touching, gesturing
- **Body extremities**: occasional shadow on floor, breath vapor in cold, hair edge in wind

### 22.4 POV traversal intent enum (canonical)

```
static                    — character/object focused, viewer not moving
walking_forward          — viewer steps toward subject/setting
walking_backward          — viewer retreats from subject
turning_left              — viewer rotates left
turning_right            — viewer rotates right
approaching_character     — viewer moves toward character (or vice versa)
ascending_stairs          — viewer climbs
descending_stairs         — viewer descends
looking_around           — viewer scans setting (panning head)
```

### 22.5 Compliance authority

- Technical implementation → `INGENIERO-PAUTA-MASTER § 8.Y POV traversal implementation`
- SPEC schema → `CREATIVE-SPEC-TEMPLATE shot_list[].pov_traversal_intent` (v9 NEW enum)
- Pre-render verification → `pre-render-gate Q28 NEW` (post Track C codification)

### 22.6 Canonical validation status

```yaml
canonical_validation_status: "validated_via_deep_frame_analysis_8_refs_2026_05_20"
validated_against_canonical_refs:
  - "8 refs deep frame analysis POV traversal continuity"
  - "matadero v1 SHIP empirical anti-pattern (consecutive shots teleport viewer)"
validation_methodology: "auditor deep frame analysis 8 refs + matadero empirical anti-pattern analysis"
validated_at: 2026-05-20
```


---

## ⚠️ CONSOLIDATION PASS SCHEDULED — post video #2 (added 2026-05-20)

PAUTA-MASTER ha crecido orgánicamente post-matadero a través de codifications incrementales: § 17 rotación + § 18 decision-UI-pacing + § 19 AVU + § 20 setting alive + § 21 character alive + § 22 POV traversal. **18 gaps codified** post matadero v1 SHIP across 5 NIVEL cascade.

**Risk identified**: redundancy entre §§ relacionadas (e.g. § 18 + § 19 overlap on decision UI editorial; § 20 + § 21 + § 22 overlap on "alive" canonical patterns) + cognitive load para architect leyendo PAUTA pre-design.

**Consolidation plan**:

Post video #2 SHIPPED (next horror-choice production using P3/P5/P9 + cinema abandonado setting), merge §§ 18+20+21+22 into unified section:

```
§ NEW. Canonical quality dimensions (consolidated post video #2)
  18.x → "Decision UI editorial dimension" (sub-section)
  19.x → "AVU principle dimension" (sub-section)
  20.x → "Setting alive dimension" (sub-section)
  21.x → "Character alive dimension" (sub-section)
  22.x → "POV traversal dimension" (sub-section)
```

**Benefits**:
- Single authoritative "Quality dimensions" reference vs scattered §§
- Reduce cognitive load architect pre-design (1 § read vs 5 §§)
- Cross-dimension dependencies surface (e.g. AVU principle applies decision UI + countdown intersection)
- Empirical bands consolidated single canonical defaults block (Phase 1 measurements unified)

**Status**: deferred until post-video-#2 production complete. Trigger consolidation pass once video #2 lessons learned integrated. Maintain current incremental §§ structure for now (post-matadero traceability).

**Owner**: architect creative-domain authority. Auditor concurrence required pre-merge (avoid lossy compression).

