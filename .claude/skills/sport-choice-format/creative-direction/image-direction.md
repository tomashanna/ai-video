# image-direction.md — Descripción per-shot de imágenes sport-choice (⭐ REGLA DE AMBIENTE)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa de sport-choice** vive en `sport-choice-format/PAUTA-MASTER.md`. La **autoridad técnica de la REGLA DE AMBIENTE** vive en `sport-choice-format/INGENIERO-PAUTA-MASTER.md § 1`. Este doc IMPLEMENTA esa regla a nivel per-shot. Si hay conflicto → gana la pauta.
>
> Si llegaste acá sin leer las pautas, parar y leerlas primero.

---

> Cada shot del video tiene una IMAGEN base (generada por AI) que después se anima. El arquitecto la describe con suficiente detalle para que el ingeniero la produzca coherentemente. En sport-choice, esa descripción está GOBERNADA por la REGLA DE AMBIENTE — porque el riesgo #1 del formato es que el viewer no entienda qué pasa en el partido en cada frame.

---

## ⭐⭐ LA REGLA DE AMBIENTE — el orden visual del partido (REGLA CENTRAL)

> Autoridad: `INGENIERO-PAUTA-MASTER.md § 1`. Acá la aplicamos per-shot.

**Cada `visual_intent` se construye en este ORDEN exacto:**

```
(1) CÁMARA POV 1ª persona del jugador
(2) ZONA del campo          (círculo central / banda / borde del área / mano a mano / medio campo)
(3) GEOGRAFÍA clara         (arco + red, compañeros kit PROPIO, rivales kit OPUESTO, arquero kit DISTINTO, balón, líneas de cal)
(4) ESTADIO lleno + reflectores + césped
(5) la ACCIÓN / animación   (lo que pasa en este shot)
```

**Calidad:** premium, foto-real broadcast, 85mm, profundidad de campo. Debe entenderse **CLARÍSIMO qué pasa en el partido** en cada frame.

**Por qué el orden importa:** ubicar primero (POV → zona → geografía → estadio) ancla al viewer espacialmente; recién entonces la acción tiene contexto. La geografía DEBE preceder a la acción.

---

## El framework de descripción per-shot (sport)

Cada shot necesita estas dimensiones, en el orden de la REGLA DE AMBIENTE:

| # | Dimensión | Qué especifica | Ejemplo |
|---|-----------|----------------|---------|
| 1 | **POV** | Cámara 1ª persona del jugador | "Cámara POV en primera persona del jugador" |
| 2 | **Zona del campo** | Dónde estás en la cancha | "en el borde del área rival" |
| 3 | **Geografía** | Arco, kits propio/rival/arquero, balón, líneas | "Saka (kit rojo #7) desmarcado a la izquierda; arquero (kit verde) achicando; balón a tus pies; líneas del área" |
| 4 | **Estadio** | Lleno + reflectores + césped | "Estadio Champions lleno, reflectores sobre el césped verde" |
| 5 | **Acción** | Lo que pasa / se anima en este shot | "el viewer arma el remate y le pega de primera" |
| 6 | **LUT / mood** | warm_glory / cool_cinematic_stadium / cool_defeat | "cool_cinematic_stadium (juego en tensión)" |
| 7 | **Lip sync** | ¿Jugador hablando visible? | true (con dialogue + delivery) / false |

Si una dimensión falta, el ingeniero la rellena con intuición = geografía confusa = el viewer se pierde.

---

## Ejemplos completos por tipo de shot

### Hook (dyad)

```
Cámara POV en primera persona de un jugador, parado en el CÍRCULO CENTRAL del estadio.
Geografía: a la izquierda [PROTAGONISTA] (kit ROJO mangas blancas, dorsal 7, piel marrón,
rapado, barba corta, sonrisa amplia) pide el balón con la mano; a la derecha [FOIL] (kit AZUL
marino franja roja, dorsal 10, piel oscura, rapado, bigote, serio); líneas de cal del círculo
central bajo los pies; balón blanco oficial en el suelo. Estadio LLENO desenfocado al fondo,
reflectores sobre el césped verde brillante. Acción: micro-bob de cámara, los dos jugadores
miran al viewer esperando la elección. Foto-real broadcast, 85mm, profundidad de campo.
```

### Recorrido del FOIL (counterfactual — shot dentro del recorrido del camino no-elegido)

> Esto es UN shot del recorrido COMPLETO del foil (no una "rama corta" — el foil tiene su propio recorrido entero con setup + compuertas + desenlace). El recorrido del foil puede ir al inicio O al final del video (🟩 orden variable). ⤴ `PAUTA-MASTER.md § 4` + § 10.A.

```
Cámara POV en primera persona al BORDE DEL ÁREA rival. Geografía: [FOIL] (kit azul franja roja
#10), tu compañero en esta hipótesis, te deja el balón de tacón sobre las líneas de cal;
portería con red y arquero (kit verde) al fondo; defensores azules cerca; balón blanco llegando
a tus botas. Estadio LLENO, reflectores y luz dorada cálida de la hipótesis gloriosa. Acción:
el viewer arma el pie y le pega de primera. Foto-real broadcast, 85mm, profundidad de campo.
```

### Setup / decisión (banda — D1)

```
Cámara POV en primera persona del jugador, AVANZANDO POR LA BANDA derecha. Geografía: el lateral
rival (kit azul) te cierra el paso de frente; la línea de cal de banda a tu derecha; tu compañero
(kit rojo) corre por el centro pidiendo; el arco rival al fondo a la izquierda; balón controlado
a tus pies. Estadio LLENO rugiendo, reflectores y luz fría de tensión sobre el césped. Acción: el
viewer encara al lateral con el balón dominado, decidiendo encarar o devolver. Foto-real broadcast,
85mm, profundidad de campo.
```

### Clímax (mano a mano — D3)

```
Cámara POV en primera persona del jugador, en el MANO A MANO dentro del área rival. Geografía: el
arquero rival (kit verde fosforescente, distinto a ambos equipos) adelantado achicando el ángulo a
pocos metros; la portería con red detrás; líneas de cal del área grande y el punto de penal a un
lado; tu compañero (kit rojo #7) desmarcado al borde izquierdo; balón blanco a tus pies. Estadio
LLENO rugiendo, reflectores y luz fría de tensión. Acción: el viewer encara al arquero, decidiendo
el remate; el arquero se agranda. Foto-real broadcast, 85mm, profundidad de campo shallow sobre el
balón y el arquero.
```

### Consecuencia de error (humillación — burla)

```
Cámara POV en primera persona del jugador, dentro del área rival tras el remate fallado. Geografía:
el arquero rival (kit verde) abraza el balón en el suelo; tus manos visibles yendo a tu cabeza; los
defensores rivales (kit azul) empiezan a celebrar; el arco detrás; líneas de cal. Estadio LLENO con
la hinchada local en silencio o abucheando, paleta FRÍA desaturada gris-azul (el frío del fracaso —
NO horror rojo), reflectores planos. Acción: el viewer se lleva las manos a la cabeza mientras el
rival celebra. Foto-real broadcast, 85mm, profundidad de campo.
```

### Resolución / gloria (gol — campeón)

```
Cámara POV en primera persona del jugador frente a la PORTERÍA rival. Geografía: la red del arco se
infla con el balón blanco dentro; el arquero (kit verde) vencido en el suelo; líneas de cal del área;
tu compañero (kit rojo #7) corre hacia el viewer con los brazos abiertos. Estadio LLENO estallando en
celebración bajo luz DORADA cálida (warm_glory), confeti empezando a caer. Acción: el compañero corre
a abrazar al viewer celebrando el título. Foto-real broadcast, 85mm, profundidad de campo.
```

---

## ⭐ BIBLIOTECA DE PROMPTS — imagen + animación pareada (parametrizable)

> **Cómo se usa:** copiá el bloque del tipo de shot, reemplazá los `[PLACEHOLDERS]` (`[EQUIPO_A]`, `[KIT_A]` = color/patrón del kit propio, `[KIT_B]` = kit rival, `[KIT_GK]` = kit arquero distinto a ambos, `[DORSAL_A]`, `[CRACK_A_RASGOS]` = descriptor foto-real del crack, `[ESTADIO]`, `[ZONA]`…), y verificá la checklist REGLA DE AMBIENTE + la checklist de animación de abajo. Nivel de detalle = el de los 2 ejemplos canónicos de `INGENIERO-PAUTA-MASTER.md § 1`.
>
> Cada tipo trae **dos prompts pareados**:
> - **IMAGEN** (Gemini t2i): REGLA DE AMBIENTE (POV→zona→geografía→estadio→acción) + calidad 5-block premium (subject + camera 85mm/profundidad + lighting reflectores + atmospheric + style foto-real broadcast). Mood SIEMPRE vía físico observable (césped brillante bajo reflectores, vapor de la hinchada, confeti suspendido, banderas flameando), NUNCA "cinematic atmosphere" vago (memoria `prompt_quality_no_vague`).
> - **MOTION** (Hailuo i2v, ≤5.9s): qué se mueve y cómo, respetando los constraints empíricos de modelo.
>
> ### ⛔ Constraints de modelo que TODO prompt de esta biblioteca respeta
> - **IMAGEN** (`MODEL-BEHAVIOR-LOG.md` entry 1+2 + `MODEL-CAPABILITIES-MATRIX.md`): frases descriptivas con sujeto+verbo, **NUNCA label-prefix** ("POV:", "ANGLE:", "ACTION:") → Gemini lo quema como texto en el frame. **≤3 props/elementos** más allá del/los jugador(es) ancla (stability budget — pasarse degrada la imagen). Likeness **descriptor-based**, nunca el nombre real de la celebridad. Para shots que aíslan un rasgo/objeto sin cara → anchor locus-específico.
> - **MOTION** (`MODEL-CAPABILITIES-MATRIX.md` hailuo_std + `MODEL-BEHAVIOR-LOG.md`): la acción CABE en **≤5.9s** (Hailuo Std clip_max). Cara frontal o 15-30° de tilt; **AVOID head-turns bruscos** (uncanny). `prompt_anti_patterns`: **NUNCA "talking" / "speaking" / "lips moving"** salvo `lip_sync_required: true` (el lip-sync preciso es Phase 3, no i2v base). Hailuo NO genera audio → narración/SFX se muxean aparte.

---

### 1) HOOK — dyad (los dos cracks, elección)

**IMAGEN** (`cool_cinematic_stadium`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador parado en el CÍRCULO CENTRAL del [ESTADIO]. Geografía: a la
izquierda [CRACK_A_RASGOS] con [KIT_A] y dorsal [DORSAL_A], pide el balón con la mano abierta; a la
derecha [CRACK_B_RASGOS] con [KIT_B] y dorsal [DORSAL_B], serio mirando al frente; líneas de cal
blancas del círculo central bajo los pies; balón blanco oficial quieto en el césped. Estadio LLENO
desenfocado al fondo con banderas de ambas hinchadas flameando, reflectores cayendo sobre el césped
verde brillante con rocío. Composición simétrica de los dos jugadores encarando a cámara, ambos a
media distancia, esperando la elección. Foto-real broadcast, lente 85mm, profundidad de campo media
con fondo suavemente desenfocado.
```
**MOTION** (≤5.9s): `subtle first-person camera micro-bob and slow breathing sway; the two players stand still facing camera, chest rising and falling, one slowly opens his hand asking for the ball; flags wave in the background, floodlights flicker faintly on the wet grass; faces frontal, calm neutral expressions, mouths closed, no head turns, no talking; slow cinematic hold.`

---

### 2) COMPUERTA / DECISIÓN en zona X (el dilema de la jugada)

**IMAGEN** (`cool_cinematic_stadium`, `lip_sync_required: false`) — ejemplo zona = banda:
```
Cámara en primera persona de un jugador AVANZANDO POR LA BANDA derecha del [ESTADIO]. Geografía: un
defensor rival con [KIT_B] cierra el paso de frente a pocos metros; la línea de cal de banda corre a
la derecha; un compañero con [KIT_A] dorsal [DORSAL_A] corre por el centro pidiendo el pase; el arco
rival con red al fondo a la izquierda; balón blanco controlado al ras del césped a los pies. Estadio
LLENO rugiendo con bengalas de humo tenue en la tribuna, reflectores y luz fría de tensión sobre el
césped. El viewer encara al defensor con el balón dominado, peso adelantado, a punto de decidir.
Foto-real broadcast, lente 85mm, profundidad de campo shallow sobre el balón y el defensor.
```
**MOTION** (≤5.9s): `first-person view dribbling forward, the ball rolls and bounces slightly at the feet, the opposing defender shifts weight side to side blocking the path, the teammate jogs across the background calling for it, smoke haze drifts in the stands, floodlights steady; camera low and tense holding on the duel; defender facing forward, no abrupt turns, no talking; freezes naturally as the decision approaches.`

> 🟩 Para otras zonas, intercambiá el bloque (2) de geografía: *borde del área* (arquero achicando + compañero desmarcado + punto de penal), *mediocampo* (líneas de centro + dos rivales acercándose), *mano a mano* (ver tipo 0 clímax en "Ejemplos completos" arriba). La acción de motion sigue el mismo molde: balón + 1 rival moviéndose + ≤3 elementos.

---

### 3) GOL — la red inflándose (acierto / desenlace glorioso)

**IMAGEN** (`warm_glory`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador frente a la PORTERÍA rival del [ESTADIO], justo después del
remate. Geografía: la red blanca del arco se infla hacia atrás con el balón blanco dentro tocando el
fondo de la malla; el arquero con [KIT_GK] vencido tendido en el césped junto al palo; líneas de cal
del área grande en primer plano. Estadio LLENO estallando, miles de brazos arriba y banderas
flameando, luz DORADA cálida de reflectores, primeras chispas de confeti suspendidas en el aire. El
viewer mira la pelota en la red en el instante del gol. Foto-real broadcast, lente 85mm, profundidad
de campo media, leve motion del momento.
```
**MOTION** (≤5.9s): `the net ripples and billows backward as the ball settles into the mesh, the goalkeeper slumps on the grass, the first-person camera jolts up and surges forward toward the goal in celebration, confetti and ticker-tape drift down, the crowd erupts with arms raised and flags waving under golden floodlights; fast euphoric energy; no faces close-up, no talking.`

---

### 4) PAPELÓN / BLOOPER PROPIO (error divertido — el más compartible, ≥1 por video §6)

**IMAGEN** (`cool_defeat`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador dentro del área rival del [ESTADIO] tras un remate ridículo
fallado. Geografía: el balón blanco se va MUY por encima del travesaño hacia la tribuna; el arco con
red intacto y el arquero con [KIT_GK] mirando la pelota irse con las manos en la cintura; líneas de
cal del área. Las propias manos del viewer (mangas [KIT_A]) suben hacia la cabeza en gesto de
"no puede ser"; un compañero con [KIT_A] al costado se agarra la cara. Estadio LLENO con la hinchada
en reacción de incredulidad, paleta FRÍA desaturada gris-azul (el frío del papelón deportivo, NO
horror), reflectores planos. Foto-real broadcast, lente 85mm, profundidad de campo media.
```
**MOTION** (≤5.9s): `the ball flies way over the crossbar into the stands, the first-person hands (own sleeves) rise to the head in disbelief, the nearby teammate covers his face, the goalkeeper watches with hands on hips, the crowd recoils in a collective groan; muted desaturated tone; awkward comedic beat; faces frontal in dismay, no abrupt head turns, no talking.`

---

### 5) CELEBRACIÓN con copa / vuelta olímpica (gloria sostenida)

**IMAGEN** (`warm_glory`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador en el centro del césped del [ESTADIO] en la vuelta olímpica.
Geografía: el compañero con [KIT_A] dorsal [DORSAL_A] levanta el trofeo plateado en alto justo
adelante; las propias manos del viewer (mangas [KIT_A]) aplauden hacia arriba; líneas de cal y el
arco al fondo. Estadio LLENO en éxtasis, confeti dorado y plateado lloviendo denso, banderas y
bengalas de la hinchada, luz DORADA cálida saturada de reflectores sobre el césped brillante. Foto-real
broadcast, lente 85mm, profundidad de campo media con confeti en foco cercano.
```
**MOTION** (≤5.9s): `dense gold and silver confetti rains down, the teammate hoists the trophy and it glints under the floodlights, the first-person hands clap upward, flags wave and smoke flares glow in the packed stands, the camera sways with the celebration; warm saturated euphoric tone; teammate facing forward smiling, no abrupt turns, no talking.`

---

### 6) DERROTA / ABUCHEO (humillación sostenida — `cool_defeat`)

**IMAGEN** (`cool_defeat`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador parado en el césped del [ESTADIO] tras perder. Geografía: los
rivales con [KIT_B] celebran en grupo a media distancia abrazándose; las propias manos del viewer
(mangas [KIT_A]) cuelgan a los costados, cabeza baja implícita por el ángulo; un compañero con [KIT_A]
de rodillas en el césped a un lado; líneas de cal. Estadio LLENO con la hinchada local abucheando y
silbando, paleta FRÍA desaturada gris-azul (el frío del fracaso deportivo, NO horror rojo),
reflectores fríos y planos. Foto-real broadcast, lente 85mm, profundidad de campo media.
```
**MOTION** (≤5.9s): `the rival players celebrate hugging in the mid-distance, the teammate kneels on the grass, the first-person hands hang limp at the sides, the camera dips slightly as if the head drops, a few scattered seats empty in the stands; cold desaturated grey-blue tone, flat lighting; heavy defeated beat; figures frontal, no abrupt head turns, no talking.`

---

### 7) COUNTERFACTUAL del FOIL (un shot del recorrido completo del camino no-elegido)

> El recorrido del foil es un recorrido ENTERO (setup + compuertas + desenlace); este es UN shot de definición de ESE recorrido. El foil (estrella rival) es tu compañero EN ESTA hipótesis → su kit pasa a ser el propio de la hipótesis. ⤴ `PAUTA-MASTER.md § 4` + § 10.A.

**IMAGEN** (`warm_glory` si es el desenlace glorioso del foil, `lip_sync_required: false`):
```
Cámara en primera persona al BORDE DEL ÁREA rival del [ESTADIO], en la hipótesis del otro equipo.
Geografía: [CRACK_B_RASGOS] con [KIT_B] dorsal [DORSAL_B] —tu compañero en ESTA hipótesis— te deja
el balón de tacón sobre las líneas de cal; la portería con red y el arquero con [KIT_GK] al fondo; un
defensor con [KIT_A] (ahora el rival de la hipótesis) llega tarde; balón blanco llegando a las botas.
Estadio LLENO, reflectores y luz DORADA cálida de la hipótesis gloriosa, vapor de la hinchada en el
aire frío. El viewer arma el pie para pegarle de primera. Foto-real broadcast, lente 85mm, profundidad
de campo shallow sobre el balón.
```
**MOTION** (≤5.9s): `the foil teammate back-heels the ball, it rolls into the first-person path, the viewer plants and swings the boot to strike it first-time, the late defender lunges in too slow, warm golden light and crowd breath-haze in the air; smooth confident tempo; teammate frontal, no abrupt head turns, no talking.`

---

### 8) PIVOTE entre recorridos (el único corte no-continuo — cambio de hipótesis)

> El pivote NO es teleporte: es el corte marcado que pasa de un recorrido al otro. Visualmente, un reset claro al círculo central con las mangas del OTRO kit comunica "ahora ves la otra elección". El cue verbal/caption lo refuerza (ui-elements + § 10.A).

**IMAGEN** (`cool_cinematic_stadium`, `lip_sync_required: false`):
```
Cámara en primera persona de un jugador de vuelta en el CÍRCULO CENTRAL del [ESTADIO], reseteado al
arranque de la otra hipótesis. Geografía: ahora las propias mangas visibles son [KIT_B] (el otro kit);
[CRACK_B_RASGOS] con [KIT_B] dorsal [DORSAL_B] está al lado como nuevo compañero, mirando al frente;
líneas de cal del círculo central; balón blanco quieto en el centro. Estadio LLENO al fondo
desenfocado, reflectores sobre el césped verde, leve neblina del recinto. Composición de reinicio,
limpia y centrada. Foto-real broadcast, lente 85mm, profundidad de campo media.
```
**MOTION** (≤5.9s): `a clean reset beat — gentle first-person camera settle as the scene re-establishes at the center circle, the new teammate stands beside facing forward, the ball sits still at center, faint arena haze drifts, floodlights steady; calm transitional hold that reads as a new branch, not a continuation; faces frontal, no abrupt turns, no talking.`

> ⚠️ El pivote es el ÚNICO corte no-continuo permitido (EXECUTION CONTINUITY § 2). DENTRO de cada recorrido, los shots se encadenan con continuidad física (la animación de cada shot fluye al siguiente, sin teleporte).

### Checklist de animación por shot (validar ANTES de generar el clip)
- [ ] ¿La acción CABE en ≤5.9s (Hailuo Std clip_max)? Si la narración del shot a 165 WPM > 5.9s → trim/split/freeze-extend (`MODEL-CAPABILITIES-MATRIX.md`).
- [ ] ¿Caras frontales o 15-30°? ¿CERO head-turns bruscos?
- [ ] ¿CERO "talking"/"speaking"/"lips moving" salvo `lip_sync_required: true`?
- [ ] ¿La acción describe QUÉ se mueve (balón, manos, red, confeti, 1 rival) — no "movimiento cinematográfico" vago?
- [ ] ¿≤3 elementos en movimiento (no caos)?
- [ ] ¿El mood emerge de físico observable (confeti, vapor, banderas, reflectores), no de adjetivos abstractos?
- [ ] ⛔ **Si las botas/piernas propias del POV son visibles en el frame → DEBEN tener movimiento declarado** (peso cambiando, paso, trote, ajuste de apoyo sobre el césped). Piernas/zapatillas POV congeladas = uncanny inmediato. (Regla del creator 2026-06-04 — caso disparador: shots POV del champions con zapatillas estáticas "se veía raro".)

---

## Anchors de kit + likeness (consistencia cross-shot)

> Autoridad: `INGENIERO-PAUTA-MASTER.md § 3`.

### Reference anchor por jugador (obligatorio)

Generar UNA imagen anchor por jugador con su kit exacto (color, mangas, dorsal) + rasgos foto-reales, y reusarla en todos sus shots (IP-Adapter / reference mode). El dorsal + patrón del kit = visual signature, NUNCA varían cross-shot.

```yaml
reference_anchor_requirements:
  - character: PROTAGONISTA
    needed: true
    detail_intent: |
      [Jugador] standalone. RASGOS FOTO-REALES (descriptor-based, NO nombre literal):
      extremo del [equipo], piel marrón, rapado, barba corta, sonrisa amplia.
      KIT: camiseta ROJA mangas blancas, pantalón blanco, dorsal 7 grande (espalda + frente).
    purpose: "Consistencia cross-shot del jugador + kit. Riesgo CP1 — iterar hasta likeness aceptable."
  - character: FOIL
    needed: true
    detail_intent: |
      [Jugador] standalone. RASGOS FOTO-REALES: extremo del [equipo rival], piel oscura,
      rapado, bigote, serio. KIT: camiseta AZUL marino franja roja central, dorsal 10.
    purpose: "Consistencia + contraste de kit vs protagonista."
```

### Likeness de jugadores reales = descriptor-based (REGLA CRÍTICA — riesgo CP1)

- ⛔ NUNCA el nombre de la celebridad literal en el prompt → describir por rasgos foto-reales + kit + dorsal.
- Iterar en CP1 hasta likeness aceptable. Es el riesgo de producción #1 del formato.

### Los 3 kits siempre legibles

- Kit PROPIO (tu equipo: tus mangas en el POV + compañeros) / kit RIVAL (defensores, lateral) / kit del ARQUERO (distinto a ambos). En cada shot, los 3 inequívocos. El kit dice quién es aliado y quién obstáculo.

---

## LUTs / mood por sección (intent — ejecuta el ingeniero)

| Sección | LUT | Mood |
|---------|-----|------|
| Juego en tensión (hook, setup, decisiones) | `cool_cinematic_stadium` | Frío cinematográfico de broadcast |
| Desenlace glorioso (gol/campeón) + resolución + outro (acierto) | `warm_glory` | Cálido dorado, celebración |
| Error / burla | `cool_defeat` | Frío desaturado gris-azul (fracaso deportivo, NO horror rojo) |

(Sin `cool_horror` ni LUTs de terror.)

---

## Anti-patterns en image direction (sport)

❌ **Saltar la REGLA DE AMBIENTE** (acción primero, sin geografía) → frame confuso, no se entiende la jugada.
❌ **Geografía incompleta** (falta arco, balón, o no se sabe quién es compañero/rival).
❌ **Kits ambiguos o no especificados** → el viewer no distingue aliado de obstáculo.
❌ **POV no establecido** → el modelo genera tercera persona (rompe HR POV 1ª persona).
❌ **Nombre de celebridad literal en el prompt** → caras genéricas/falla; usar descriptor + kit.
❌ **Falta reference anchor** para los jugadores → drift de kit/cara cross-shot.
❌ **Estadio genérico** sin lleno/reflectores/césped → se ve vacío y falso.
❌ **LUT de horror** en cualquier shot → fuera de formato.

---

## Validación final per shot

- [ ] ¿El prompt sigue el orden REGLA DE AMBIENTE (POV → zona → geografía → estadio → acción)?
- [ ] ¿Geografía completa (arco, kit propio, kit rival, arquero si aplica, balón, líneas)?
- [ ] ¿Los 3 kits inequívocos?
- [ ] ¿POV 1ª persona establecido?
- [ ] ¿Reference anchor flag para los jugadores recurrentes?
- [ ] ¿LUT correcta (warm_glory / cool_cinematic_stadium / cool_defeat — ninguna de horror)?
- [ ] ¿Lip sync flag definido si el jugador habla?
- [ ] ¿Cierra con "foto-real broadcast, 85mm, profundidad de campo"?
- [ ] ¿Queda CLARÍSIMO qué pasa en el partido con solo leer el prompt?
