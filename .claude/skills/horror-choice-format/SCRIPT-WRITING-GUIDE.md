# SCRIPT-WRITING-GUIDE.md — Cómo generar guiones estilo "Elige a tu compañero"

> Este documento se le pasa a Claude como contexto cuando se le pide generar un nuevo guion del formato. Está optimizado para Claude — ver `PATTERNS.md` para reglas técnicas de producción.

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

1. **Nombre del personaje "malo aparente"** (el monstruo amenazante con diálogo)
2. **Nombre del personaje "bueno aparente"** (el extraño pero pacífico, sin diálogo)
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

Cada decisión binaria del horror-choice sigue este template **literal**. No improvisar fuera del formato.

```
SETUP:        {personaje habla / 1 frase narrator} (1 línea, NO 3 segments fragmentados)
PREGUNTA:     "Decide. A. {opción}. B. {opción}."
CONSEQUENCE A: "Si elegiste A, {qué pasa LITERAL que matchea visual}."
BRIDGE:       caption "SI ELEGISTE B:"
CONSEQUENCE B: "Si elegiste B, {qué pasa LITERAL que matchea visual}."
```

**Regla "Narración CLARA, NO tenebrosa"** (PAUTA-MASTER § 3 regla añadida 2026-05-16):

- ❌ Tenebroso (genre temptation): *"El silencio te abraza con dedos de hielo"*
- ✅ Claro: *"Te congelaste."*

- ❌ Tenebroso: *"La oscuridad consume tu última esperanza, devorando tu alma"*
- ✅ Claro: *"La luz se apaga. No respiras."*

El tono tenebroso emerge del **visual + SFX + música ambient**, NO de la narración. La narración prioriza CLARIDAD de acción/contexto.

**Test**: ¿el viewer entiende qué pasa en 1ra escucha sin caption? Si NO → reescribir.

**Auto-audit D19** valida que `consequence_A_text` y `consequence_B_text` empiezan con "Si elegiste {A|B}..." — caption "SI ELEGISTE B:" SOLA no cuenta como compliance.

---

## REGLAS DE CALIDAD AL ESCRIBIR

Mientras Claude llena los slots, debe respetar estas reglas o el guion no va a sonar al formato.

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

### Diálogo del personaje "malo"

El malo dice frases cortas, crípticas y autoritarias. Máximo 5 palabras. Ejemplos del formato:
- "Honesto. Baja conmigo."
- "Inteligente. Elegiste bien."
- "Demuéstralo."
- "Ya no necesitas respirar."
- "Las cosas de aquí abajo odian la luz."

Patrón: una palabra de juicio + una orden o frase declarativa corta.

### El dilema

**El dilema debe seguir la regla de oro:** la opción ganadora va contra el impulso primario.

Ejemplos correctos del formato:
- Pedir irse (impulso) ❌ vs Quedarse sentado (estoico) ✅
- Encender la bengala (curiosidad) ❌ vs Quedarse a oscuras (obediencia) ✅
- Saltar al rescate (acción) ❌ vs Activar alarma (mediación) ✅

Ejemplos incorrectos (no usar):
- "¿Confías o no confías?" — demasiado abstracto
- "¿Lo matás o lo dejás vivir?" — binario moral obvio, no de obediencia
- "¿Vas a la izquierda o a la derecha?" — no hay carga psicológica

### El cliffhanger

Estructura literal: `Si hubieras elegido a [BUENO], habrían [ACCIÓN_DE_2_PERSONAS_EN_PAZ] juntos, en silencio, mirando [ELEMENTO_NATURAL] al [TIEMPO_DEL_DÍA].`

Acciones válidas: vigilado las pantallas, pasado la noche mirando el radar, comido raciones, tomado café, leído en voz alta, escuchado música, esperado el amanecer.

Elementos naturales válidos: el océano, las estrellas, el bosque, las montañas, el cielo, el río, el horizonte.

Tiempos del día válidos: amanecer, atardecer, primera luz, último silencio.

**Siempre cerrar con:** "Una noche en paz." (frase exacta, sin variaciones)

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
- [ ] ¿La opción ganadora va contra el impulso primario?
- [ ] ¿El cliffhanger usa la frase "Una noche en paz." al final?
- [ ] ¿El malo tiene 1-2 líneas de diálogo crípticas?
- [ ] ¿El bueno NO tiene diálogo?
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
4. **Reservá los nombres aprobados.** Una vez que un par de nombres funciona en producción, anotalos en `CLAUDE.md` como "FROZEN — usado en video #N".
