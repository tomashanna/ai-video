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

### Rama corta (foil — counterfactual opening)

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
| Rama corta gloriosa + resolución + outro (acierto) | `warm_glory` | Cálido dorado, celebración |
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
