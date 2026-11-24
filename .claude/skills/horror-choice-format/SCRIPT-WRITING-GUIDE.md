# SCRIPT-WRITING-GUIDE.md — Cómo generar guiones estilo "Elige a tu compañero"

> Este documento se le pasa a Claude como contexto cuando se le pide generar un nuevo guion del formato. Está optimizado para Claude — ver `PATTERNS.md` para reglas técnicas de producción.

> ⚠️ **CÓMO LEER ESTE DOC (framing — refactor 2026-05-29, pattern_class 3/5).** Los videos canónicos NO tienen reglas rígidas: tienen **flexibilidad creativa dentro de un marco**. Este doc distingue 3 niveles y el arquitecto debe saber cuál es cuál:
> - 🟦 **PRINCIPIO (underlying, mandatorio)** — el mecanismo que hace funcionar el formato. NO negociable. Ej: "la consecuencia marca a qué rama pertenece".
> - 🟩 **VARIABILIDAD (exploración creativa, libre)** — cómo ejecutás el principio. Múltiples formas válidas, todas vistas en los 8 virales. Ej: "Si la enciendes" / "Si decides" / "Si elegiste a Víctor". Elegí la que mejor suene; NO hay una "correcta".
> - 🟥 **ANTI-PATTERN (conocido, evitar)** — formas que empíricamente fallan. Ej: bare label robótico "Si elegiste A".
>
> Si algo acá suena a "regla binaria obligatoria" sobre una **elección creativa**, es un bug de framing — reportalo. Autoridad última = fuente primaria: `data/referent-analysis/horror-choice/ref-XX/transcription.json`.

> 🟦 **Autoridad ESTRUCTURAL + invariante (PRINCIPIO, no negociable)**: el esqueleto canónico y el invariante "el bueno-aparente NUNCA está en el recorrido jugado tomando decisiones con el viewer" viven en **`PAUTA-MASTER.md § 2`** (validador pre-emit: `ai-video audit-spec-structure-vs-canonical`). Escribí el guion contra ese esqueleto.

---

## CÓMO USAR ESTE DOCUMENTO

Para generar un guion nuevo, pegale a Claude:
1. Este documento completo
2. Los inputs del usuario (nombres, escenario, tipo de dilema deseado)
3. La instrucción: "Generá un guion siguiendo la plantilla y respetando todas las reglas de calidad"

Claude debe responder con: el guion completo siguiendo la plantilla literal, en español, con todos los timings calculados para una duración objetivo de 90 segundos.

---

## INPUTS REQUERIDOS DEL USUARIO

Antes de generar, pedile al usuario estos 5 datos. Si faltan, pedilos antes de empezar:

1. **Nombre del personaje "malo aparente"** (el monstruo amenazante; suele tener diálogo críptico, pero 🟩 varía por video)
2. **Nombre del personaje "bueno aparente"** (el extraño pacífico; con o sin diálogo — 🟩 variabilidad, NO regla: ref-08 Hugo SÍ habla "No me elijas")
3. **Escenario** (central nuclear, hospital, submarino, bosque, faro, etc.)
4. **Categoría de dilema central** — elegir UNA:
   - Honestidad vs mentira propia
   - Acción impulsiva vs paciencia
   - Curiosidad vs obediencia
   - Violencia vs confianza
   - Sumisión a instinto vs resistencia estoica
5. **Duración objetivo** (default: 90 segundos)

Si el usuario no especifica duración, asumir 90s. Si no especifica número de elecciones, asumir 3 (formato V1, el más viral).

---

## OUTPUT REQUERIDO — EL GUION INCLUYE PLAN DE ASSETS

A partir de V8 (post-mortem bosque-abandonado v2), el guion entregado al usuario **NO es solo texto narrado**. Incluye 3 tablas adicionales que después usa la Fase 0.5 del VIDEO-PLAYBOOK:

### Tabla A — Variantes de imagen (V8-1)

Para cada escena del guion, calcular su duración total en el video y especificar variantes:

| Escena | Duración total | Variantes |
|---|---|---|
| h3-wide (POV bosque) | 9.5s | 3 variantes (`-a`/`-b`/`-c`) |
| h3-char (whisper) | 2.3s | 1 |
| h4-tension (luz cálida) | 6.0s | 2 (`-a`/`-b`) |
| ... | ... | ... |

### Tabla B — SFX por hito (V8-2)

Listar TODO sonido por hito con timestamp, descripción del prompt para ElevenLabs, duración, e influence si aplica. Mínimo: ~25-30 SFX dedicados + 6 Freesound auxiliares.

Ver `templates/SFX-LIST-TEMPLATE.md` para formato canónico.

### Tabla C — Motion plan por escena (V8-3)

Para cada plano, definir qué stack de motion lleva:

| Plano | Duración | Ken Burns | Parallax | Flicker | Shake | Vignette pulse | Glitch | Glow | Niebla |
|---|---|---|---|---|---|---|---|---|---|
| h3-wide | 9.5s | ✅ | ✅ 3 capas | – | – | – | – | – | ✅ |
| h3-char | 2.3s | ✅ | – | ✅ ojos | ✅ sutil | – | – | – | – |
| ... | | | | | | | | | |

**Sin estas 3 tablas, el guion no está completo.** Estas tablas son insumo directo para Fase 2 (generación de assets), Fase 6.5 (SFX) y Fase 6.6 (Motion pass).

---

## PLANTILLA MAESTRA

Copiá esta plantilla y reemplazá los slots `[EN_CORCHETES]`. Todos los timings asumen 90s totales.

```
[ESCENA 1 — PRESENTACIÓN — 0:00 a 0:15 (17%)]
Texto en pantalla: [NOMBRE_MALO], [NOMBRE_BUENO], ELIGE A TU COMPAÑERO
Narración: "Elige a tu compañero para esta noche, [NOMBRE_MALO] o [NOMBRE_BUENO]."

[ESCENA 2 — CUENTA REGRESIVA — 0:15 a 0:18 (17-21%)]
Texto en pantalla: 3, 2, 1
Narración: (silencio, sonido de proyector de cine)

[ESCENA 3 — ADVERTENCIA DEL MALO — 0:18 a 0:25 (21-28%)]
Texto en pantalla: [ADVERTENCIA_DE_5_A_8_PALABRAS_EN_MAYÚSCULA], NO ME ELIJAS, NO SOY INOCENTE.
Narración: "[ADVERTENCIA_DE_5_A_8_PALABRAS]. No me elijas. No soy inocente."

[ESCENA 4 — SETUP DEL ESCENARIO — 0:25 a 0:33 (28-37%)]
Texto en pantalla: SI ELIGES A [NOMBRE_MALO], [DESCRIPCIÓN_ESCENARIO_10_PALABRAS]. [DETALLE_TÉCNICO_AMBIENTE]. [NOMBRE_MALO] [ACCIÓN_AMBIGUA].
Narración: "Si eliges a [NOMBRE_MALO], [descripción del escenario]. [Detalle técnico]. [Nombre malo] [acción]."

[ESCENA 5 — PRIMERA PREGUNTA — 0:33 a 0:35.5 (37-40%)]
Texto en pantalla: [PREGUNTA_DEL_PERSONAJE_5_PALABRAS]. AHORA DECIDE.
Narración: "[Pregunta directa del personaje]. Ahora decide."

[ESCENA 6 — LOADING BAR — 0:35.5 a 0:38 (40-42%)]
Texto en pantalla: A. [OPCIÓN_IMPULSIVA_2_3_PALABRAS]   B. [OPCIÓN_ESTOICA_2_3_PALABRAS]
Narración: silencio + riser ascendente
Duración EXACTA: 2.5 segundos

[ESCENA 7 — PRIMER TWIST (CONSECUENCIA NEGATIVA) — 0:38 a 0:50 (42-55%)]
Texto en pantalla: SI [OPCIÓN_IMPULSIVA], [NOMBRE_MALO] [ACCIÓN_VIOLENTA]. [EFECTO_CORPORAL_GRÁFICO]. [SENSACIÓN_FÍSICA_NEGATIVA].
Narración: "Si [opción impulsiva], [nombre malo] [acción]. [Efecto]. [Sensación]."

[ESCENA 8 — SEGUNDA RAMA (CONSECUENCIA "BUENA") — 0:50 a 0:55 (55-61%)]
Texto en pantalla: SI [OPCIÓN_ESTOICA], ÉL [ACCIÓN_RECONOCIMIENTO]. [PALABRA_RECONOCIMIENTO_1_2_PALABRAS]. [INSTRUCCIÓN].
Narración: "Si [opción estoica], él [acción]. '[Palabra reconocimiento]'. [Instrucción]."

[ESCENA 9 — SEGUNDA PREGUNTA — 0:55 a 0:58 (61-65%)]
Texto en pantalla: [NUEVA_SITUACIÓN_DE_TENSIÓN]. [PREGUNTA_BINARIA]. AHORA DECIDE.
Narración: "[Nueva situación]. [Pregunta]. Ahora decide."

[ESCENA 10 — LOADING BAR 2 — 0:58 a 1:00.5 (65-67%)]
Texto en pantalla: A. [OPCIÓN_C]   B. [OPCIÓN_D]
Duración EXACTA: 2.5 segundos

[ESCENA 11 — SEGUNDO TWIST (CLÍMAX DE HORROR) — 1:00.5 a 1:10 (67-78%)]
Si la opción C es la "mala":
Texto en pantalla: SI [OPCIÓN_C], [CONSECUENCIA_FATAL]. [DETALLE_CORPORAL]. [FRASE_FINAL_CRÍPTICA].
Narración: "Si [opción C], [consecuencia]. [Detalle]. [Frase final]."

[ESCENA 12 — SUPERVIVENCIA / RESOLUCIÓN — 1:10 a 1:23 (78-92%)]
Texto en pantalla: SI [OPCIÓN_D], [ACCIÓN_DEL_MALO_QUE_SALVA]. [DESCRIPCIÓN_ESCAPE]. [PAISAJE_FINAL_AMBIVALENTE].
Narración: "Si [opción D], [acción salvadora]. [Escape]. [Paisaje]."

[ESCENA 13 — CLIFFHANGER — 1:23 a 1:30 (92-100%)]
Texto en pantalla: SI HUBIERAS ELEGIDO A [NOMBRE_BUENO], HABRÍAN [ACCIÓN_COTIDIANA_PAZ_8_PALABRAS] JUNTOS, EN SILENCIO, MIRANDO [ELEMENTO_NATURAL] AL [TIEMPO_DEL_DÍA].
Narración: "Si hubieras elegido a [nombre bueno], habrían [acción cotidiana] juntos, en silencio, mirando [elemento natural] al [tiempo del día]."
```

---

## TEMPLATE CANÓNICO DE EVENTO (añadido 2026-05-16)

Cada decisión binaria sigue esta ESTRUCTURA (🟦 principio). El fraseo exacto es 🟩 variabilidad.

```
SETUP:        {personaje habla / 1 frase narrator} (1 línea, NO 3 segments fragmentados)
PREGUNTA:     "Ahora decide. A. {opción}. B. {opción}."   ← "Ahora decide(s)" = gatillo canónico (8/8)
CONSEQUENCE A: "Si {acción que tomaste}, {qué pasa LITERAL que matchea visual}."
BRIDGE:       caption "SI ELEGISTE B:" (opcional — marca de rama)
CONSEQUENCE B: "Si {acción que tomaste}, {qué pasa LITERAL que matchea visual}."
```

🟦 **PRINCIPIO**: cada consecuencia marca a qué rama pertenece (sin esto el viewer se pierde — regla "rama B explícita", PAUTA).
🟩 **VARIABILIDAD del marcador** (todas canónicas, primary source — elegí la que mejor suene):
- acción condicional — *"Si la enciendes"*, *"Si esperas"*, *"Si te niegas"*, *"Si la abres"* (6/8 @referent-a — DOMINANTE)
- choice-reference — *"Si decides…"*, *"Si escogiste…"* (2/8 @referent-b)
- branch por nombre — *"Si elegiste a Víctor…"* (ref-09, marca el path por personaje)
🟥 **ANTI-PATTERN**: bare label robótico *"Si elegiste A"* / *"Si elegiste B"* (0/8 — nunca en primary source; suena a formulario, no a horror).

**Regla "Narración CLARA, NO tenebrosa"** (PAUTA-MASTER § 3 regla añadida 2026-05-16):

- ❌ Tenebroso (genre temptation): *"El silencio te abraza con dedos de hielo"*
- ✅ Claro: *"Te congelaste."*

- ❌ Tenebroso: *"La oscuridad consume tu última esperanza, devorando tu alma"*
- ✅ Claro: *"La luz se apaga. No respiras."*

El tono tenebroso emerge del **visual + SFX + música ambient**, NO de la narración. La narración prioriza CLARIDAD de acción/contexto.

**Test**: ¿el viewer entiende qué pasa en 1ra escucha sin caption? Si NO → reescribir.

**Auto-audit D19 (corregido 2026-05-29 — primary source)** valida el 🟦 principio (la consecuencia marca su rama vía cláusula condicional `Si …`) y flaggea el 🟥 anti-pattern (bare label "Si elegiste A/B"). **NO fuerza un fraseo específico**: "Si la enciendes" y "Si decides" pasan igual. Caption "SI ELEGISTE B:" es marcador-puente válido (no el único compliance). El validator `ai-video audit-spec-narrative-coherence` enforza esto.

---

## CALIDAD AL ESCRIBIR — principios + anti-patterns (no reglas rígidas)

Lo de abajo son 🟦 principios de estilo (staccato, presente, 2ª persona) y 🟥 anti-patterns (vocab IA genérico). El estilo es bastante consistente en los 8 (más "regla" que el contenido narrativo), pero seguí distinguiendo principio underlying de elección creativa libre.

### Sintaxis

- **Promedio 5.4 palabras por oración.** Si una oración pasa de 8 palabras, partila en dos.
- **45% de las oraciones deben ser de 1-3 palabras.** Ejemplos válidos: "Honesto.", "Ahora decide.", "Caminas, muerdes.", "El líquido quema."
- **Nunca usar futuro.** "Te quemará" → "Te quema". "Morirás" → "Mueres".
- **Segunda persona implícita siempre.** "Tú miras" → "Miras". "Tú decides" → "Decides".
- **Permitidas oraciones nominales (sin verbo).** "Luz fría, pasillo vacío." es correcto.

### Vocabulario

**Usar estos sustantivos del campo semántico:** pasillo, agua, cuerpo, ojos, brazo, oscuridad, silencio, aire, luz, fin, garganta, huesos, órganos, venas, pulmones, sangre.

**Usar estos verbos detonantes en momentos de horror:** quemar, derretir, destruir, aplastar, morder, cerrar (puertas/ojos), caer, oscurecer, debilitar, abrir (cuerpo).

**Usar estas palabras de "calma engañosa" SOLO en cliffhanger:** calma, sonrisa, juntos, paz, estrellas, amanecer, raciones calientes, café, silencio.

**Evitar palabras de IA genérica:** "siniestro", "macabro", "espeluznante", "tenebroso". Estas son adjetivos vagos que no describen nada físico. Reemplazar siempre con descripción corporal concreta.

### Diálogo de los personajes

🟩 **VARIABILIDAD (NO regla binaria):** que el malo hable y el bueno calle es UNA configuración frecuente, NO ley. El bueno PUEDE hablar (ref-08 Hugo: "No me elijas, algo me controla"); el malo puede ser procedural sin diálogo. 🟦 Principio: caracterización funcional coherente (el malo controla/exige; el bueno calma/ofrece) — con o sin diálogo.

Cuando el malo habla, dice frases cortas, crípticas y autoritarias. Máximo 5 palabras. Ejemplos del formato:
- "Honesto. Baja conmigo."
- "Inteligente. Elegiste bien."
- "Demuéstralo."
- "Ya no necesitas respirar."
- "Las cosas de aquí abajo odian la luz."

Patrón: una palabra de juicio + una orden o frase declarativa corta.

### El dilema

🟦 **PRINCIPIO (mandatorio, PAUTA §6):** el dilema debe generar **DUDA real** — el viewer NO tiene 100% de confianza en cuál es correcta. Si la respuesta es obvia, el dilema está mal diseñado.

🟩 **VARIABILIDAD:** "la ganadora va contra el impulso" es UNA forma frecuente de generar duda, NO una ley. Empíricamente NO es universal (PAUTA §6 lo refuta): en ref-09 la ganadora es OBEDECER (con el impulso de confiar en el procedimiento); en ref-08/ref-10 la ganadora es negarse (con el impulso sensato). A veces va contra el impulso, a veces con él. Lo único constante: **ambigüedad**.

Ejemplos que generan duda real (variabilidad):
- Encender la bengala (curiosidad) vs Quedarse a oscuras (obediencia)
- Soltar el cinturón por miedo vs Mantenerlo abrochado mientras se abre la puerta (ref-09, ganadora = obedecer)
- Saltar al rescate (acción) vs Activar alarma (mediación)

🟥 **ANTI-PATTERN (decisión sin duda):**
- "¿Confías o no confías?" — abstracto, no accionable
- "¿Lo matas o lo dejas vivir?" — binario moral obvio
- "¿Vas a la izquierda o a la derecha?" — sin carga psicológica ni pista de consecuencia

### El cliffhanger (counterfactual outro)

🟦 **PRINCIPIO (mandatorio):** counterfactual "Si hubieras elegido a [BUENO], habrían…" cerrando con un cozy **ESPECÍFICO al setting**, en contraste tonal con el horror previo. (6/8 conspiracion; @referent-b usa variantes sin "Si hubieras".)

🟩 **VARIABILIDAD (primary source — cada uno DISTINTO, NO copy-paste):**
- ref-03 (mina): *"habrían jugado cartas toda la noche, comido pan con queso y subido a la superficie riendo al amanecer"*
- ref-06 (carretera): *"estaría junto a una chimenea encendida, con café y un perro, así de simple"*
- ref-10 (fundición): *"pasado la noche en la sala de control, tomado café mientras juegan cartas y comen pizza"*
- ref-09 (cockpit): *"hablado toda la noche, mostrado las estrellas desde la cabina, aterrizado el avión suavemente al amanecer"*
- → El detalle cozy SALE del setting concreto (mina→pan con queso; cockpit→estrellas; fundición→sala de control). Paleta sensorial: café/té, comida casera, cartas, chimenea, perro, amanecer.

🟥 **ANTI-PATTERN:**
- Template rígido copy-paste *"…juntos, en silencio, mirando [elemento] al [tiempo]"* → **0/8 primary source**. Suena a fórmula, mata el contraste.
- Cozy genérico no-anclado al setting (intercambiable entre videos).

⚠️ **"Una noche en paz"** = **0/8 en los virales canónicos** (esos son otros creators con SU firma). Es **NUESTRA firma de marca** (@elige_tucompanero, loop CTA) — legítima como identidad, pero NO es "regla canónica del formato". Usala como cierre de marca opcional, no como ley.

---

## EJEMPLO COMPLETO DE GUION GENERADO

Para que veas qué calidad esperar, acá un ejemplo generado siguiendo todas las reglas:

**Inputs del usuario:**
- Malo aparente: MARTÍN (entidad antropomorfa con cara cubierta de musgo)
- Bueno aparente: TOBÍAS (humanoide pequeño con piel translúcida)
- Escenario: faro abandonado en la costa
- Dilema central: curiosidad vs obediencia
- Duración: 90s

**Guion generado:**

```
[0:00] MARTÍN, TOBÍAS, ELIGE A TU COMPAÑERO
"Elige a tu compañero para esta noche, Martín o Tobías."

[0:15] 3, 2, 1
(sonido de proyector)

[0:18] EL FARO LLEVA AÑOS APAGADO. NO LO ENCIENDAS, NO ME ELIJAS.
"El faro lleva años apagado. No lo enciendas. No me elijas."

[0:25] SI ELIGES A MARTÍN, ESTÁS EN EL FARO DE PUNTA NEGRA. NIVEL 4, BOMBILLA APAGADA. MARTÍN MIRA AL MAR.
"Si eliges a Martín, estás en el faro de Punta Negra. Nivel 4, bombilla apagada. Martín mira al mar."

[0:33] ¿QUIERES VERLO? AHORA DECIDE.
"¿Quieres verlo? Ahora decide."

[0:35.5] A. ENCIENDES LA LUZ   B. TE QUEDAS A OSCURAS
(loading bar 2.5s + riser)

[0:38] SI ENCIENDES LA LUZ, EL HAZ ATRAVIESA LA NIEBLA. ALGO ENORME LEVANTA LA CABEZA DEL AGUA. MARTÍN SONRÍE. EL CRISTAL TIEMBLA. EL FARO CAE. TE APLASTA.
"Si enciendes la luz, el haz atraviesa la niebla. Algo enorme levanta la cabeza del agua. Martín sonríe. El cristal tiembla. El faro cae. Te aplasta."

[0:50] SI TE QUEDAS A OSCURAS, MARTÍN ASIENTE. INTELIGENTE. AHORA ESCUCHA.
"Si te quedas a oscuras, Martín asiente. 'Inteligente. Ahora escucha.'"

[0:55] ALGO RASGUÑA LA PUERTA. ¿LE ABRES O ESPERAS A QUE SE VAYA? AHORA DECIDE.
"Algo rasguña la puerta. ¿Le abres o esperas a que se vaya? Ahora decide."

[0:58] A. ABRES LA PUERTA   B. ESPERAS
(loading bar 2.5s)

[1:00.5] SI ABRES LA PUERTA, ALGO LARGO Y BLANCO TE ABRAZA. TE LLEVA AL AGUA. NO PUEDES GRITAR. EL FRÍO TE ENTRA POR LOS OJOS.
"Si abres la puerta, algo largo y blanco te abraza. Te lleva al agua. No puedes gritar. El frío te entra por los ojos."

[1:10] SI ESPERAS, EL RASGUÑO PARA. MARTÍN APAGA SU LINTERNA. AMANECE. SALES DEL FARO. EL MAR ESTÁ VACÍO.
"Si esperas, el rasguño para. Martín apaga su linterna. Amanece. Sales del faro. El mar está vacío."

[1:23] SI HUBIERAS ELEGIDO A TOBÍAS, HABRÍAN TOMADO TÉ CALIENTE JUNTOS, EN SILENCIO, MIRANDO LAS ESTRELLAS AL AMANECER. UNA NOCHE EN PAZ.
"Si hubieras elegido a Tobías, habrían tomado té caliente juntos, en silencio, mirando las estrellas al amanecer. Una noche en paz."
```

Notar cómo el ejemplo:
- Cumple los porcentajes de timing
- Usa oraciones cortas (mayoría 3-7 palabras)
- Tiempo presente siempre
- Dilema sigue regla de oro (curiosidad vs obediencia)
- Cliffhanger usa la plantilla literal
- Vocabulario específico y corporal, no genérico

---

## CHECKLIST FINAL ANTES DE ENTREGAR EL GUION

Antes de devolver el guion al usuario, Claude debe verificar:

**Contenido narrativo:**
- [ ] ¿Total de palabras está entre 180-220 para 90s? (target: ~2 palabras/segundo de narración)
- [ ] ¿Promedio de oración es ~5 palabras?
- [ ] ¿Hay al menos 3 oraciones nominales sin verbo?
- [ ] ¿Hay al menos 2 oraciones de 1-3 palabras tipo "Ahora decide" / "Honesto"?
- [ ] ¿Todos los verbos están en presente, ninguno en futuro?
- [ ] 🟦 ¿La decisión genera DUDA real (ambigua, no obvia)? (NO exigir "contra el impulso" — varía, PAUTA §6)
- [ ] 🟦 ¿El cliffhanger es counterfactual cozy ESPECÍFICO al setting (no genérico)? ("Una noche en paz" = firma de marca opcional, NO requisito)
- [ ] 🟩 ¿El diálogo de los personajes es coherente con su caracterización? (malo críptico si habla; bueno con o sin diálogo — NO forzar silencio del bueno)
- [ ] ¿Hay 2-3 elementos sensoriales concretos en el cliffhanger?
- [ ] ¿Las loading bars duran exactamente 2.5s cada una?

**Plan de assets V8 (asset plan adjunto al guion):**
- [ ] ¿Para cada escena del guion, calculaste su duración total en el video y especificaste el número de variantes? (V8-1: ≤4s → 1; 4-8s → 2; >8s → 3)
- [ ] ¿Listaste los SFX por hito en una tabla aparte del NARRATIVE.md? (V8-2: typicamente ~25-30 SFX dedicados + 6 Freesound auxiliares)
- [ ] ¿Definiste qué motion lleva cada plano más allá del Ken Burns base? (V8-3: parallax/flicker/vignette/glitch/glow/niebla — ver tabla en NARRATIVE-TEMPLATE.md)

Si algún checkbox falla, corregir antes de entregar.

**El guion NO está completo sin el plan de assets V8.** No es un "extra opcional" — sin variantes la imagen se siente slideshow, sin SFX el video se siente "narrador con música", sin motion los planos parecen diapositivas. Las 3 reglas V8 vienen del post-mortem de bosque-abandonado v2 y son la diferencia entre 7/10 y 9.5+/10.

---

## NOTAS PARA EL USUARIO HUMANO

Cuando recibas el guion generado, antes de pasarlo a producción:

1. **Leelo en voz alta cronometrado.** Si pasa de 90 segundos, recortá. Si dura menos de 80s, agregá una pausa dramática.
2. **Probá la pronunciación.** Nombres con J/G/H pueden complicar al TTS. Si elegiste "Gerald" pero tu TTS español lo dice raro, escribí "Yerald" en el script y ajustá la grafía on-screen aparte.
3. **Verificá el dilema central.** ¿La opción "ganadora" va contra el impulso? Si dudás, pedile a Claude que regenere solo esa parte.
4. **Reservá los nombres aprobados.** Una vez que un par de nombres funciona en producción, anotalos en `docs/OPERATING-MANUAL.md` como "FROZEN — usado en video #N".
