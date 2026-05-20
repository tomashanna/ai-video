# image-direction.md — Descripción per-shot de imágenes (que se enchufan al script)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> Cada shot del video tiene una IMAGEN base (generada por AI). El arquitecto describe esa imagen con suficiente detalle para que el ingeniero pueda producirla coherentemente. Estas imágenes después se animan (ver `animation-direction.md`) y todas se sincronizan al script (`script-writing.md`).

---

## El framework de descripción per-shot

Cada shot crítico necesita 7 dimensiones especificadas. Si una dimensión falta, el ingeniero la rellena con intuición (= drift creativo).

### Las 8 dimensiones obligatorias por shot

| # | Dimensión | Qué especifica | Ejemplo |
|---|-----------|----------------|---------|
| 1 | **Scene description** | Qué se ve en el frame | "Bruno en primer plano, casco minero con lámpara apagada" |
| 2 | **Lighting** | Fuente + dirección + intensidad de luz EN ESE shot | "Top-down dramatic desde lámpara superior, sombras duras bajo cuencas oculares" |
| 3 | **Pose & expression** | Posición corporal + cara del personaje | "Cuerpo estático, hombros relajados; ojo único fijo en cámara, sin parpadear, expresión inexpresiva" |
| 4 | **Atmosphere** | Qué hay físicamente en el aire | "Polvo en suspensión visible, ligera niebla baja, vapor por respiración fría" |
| 5 | **Composition** | Encuadre + ángulo + rule applied | "Slight low angle for menace, sujeto centrado simétrico, regla de tercios rota intencionalmente" |
| 6 | **Color emphasis** | Qué color domina + qué color destaca | "Marrones tierra + grises dominantes, accent rojo en lámpara de pecho (medidor de gas)" |
| 7 | **Mood** | Sensación emocional target | "Ominous + intimate threat + claustrofóbico" |
| 8 | **Lip sync requirement** | ¿Hay character hablando visible en cámara? | true (con dialogue + delivery intent) / false |

---

## Lip sync direction — cuando el personaje habla en cámara

**Decisión validada del proyecto:** intentar lip sync siempre que el personaje hable visible en cámara. El ingeniero itera tools hasta lograr mejor resultado.

### Cuándo lip_sync_required = TRUE

- Personaje habla dialogue visible en cámara (boca movible visible)
- Close-up / medium shot del personaje hablando
- POV mostrando otro personaje hablando

### Cuándo lip_sync_required = FALSE

- POV donde el personaje habla off-camera (audio sin boca visible)
- Wide shot donde la boca no es legible en frame
- Personaje no habla en el shot (solo narrador omnisciente sobre la imagen)
- Shots de detail/objeto sin personaje visible hablando

### Engineer tool iteration

El ingeniero itera entre tools según calidad esperada:

| Iteration | Tool | Costo | Quality | Cuándo |
|-----------|------|-------|---------|--------|
| Primary | **Hedra Character-3** | $0.05/s | 9.5/10 lipsync specialist | Default para todo lip sync |
| Fallback 1 | **Sync.so post-process** | varies | Reemplaza región boca en clip ya generado | Cuando Hedra falla character match |
| Fallback 2 | **Veo 3.1 native audio** | $0.40/s | Audio + lip sync nativo integrado | Shot crítico premium |
| Fallback 3 | **Kling 3.0 Omni** | similar tier | Multilingual lipsync nativo | Si español necesita más naturalidad |

**El arquitecto NO elige el tool — solo dice `lip_sync_required: true` + `dialogue_text: "..."` + `delivery_intent`.** El ingeniero itera hasta resultado satisfactorio.

### Cómo el arquitecto especifica

```yaml
shot:
  id: shot_setup_bruno_dialogue
  ...
  lip_sync:
    required: true
    character_speaking: bruno
    dialogue_text: "Los ojos se adaptan solos."
    delivery_intent: susurro_intimate
    engineer_tool_suggestion: "Primary: Hedra. Iterar hasta lip movement matchea articulación natural del español."
```

### Anti-patterns en lip sync

❌ **Lip sync sin dialogue_text specified** → engineer no sabe qué sincronizar
❌ **Lip sync en wide shot con boca invisible** → desperdicio, no se nota
❌ **Multiple character lip sync en mismo shot** → confusión, usar shots separados
❌ **Forzar tool específico al ingeniero** → arquitecto da intent, ingeniero elige

---

## Plantilla completa per shot

```yaml
shot:
  id: shot_hook_close_up_bruno_ojo
  synced_to_script_segment: hook_warning  # link al script-writing.md
  timestamp_start: 0.0
  duration: 3.5s
  type: close_up  # de camera-and-shots.md

  visual_description:
    scene: |
      Close-up frontal del rostro de BRUNO. Cabeza llena el frame (head fills frame).
      Casco minero apagado, ligero óxido en el borde. Cuello largo apenas visible
      saliendo del cuello del chaleco minero raído. Penumbra de túnel mina al fondo
      (out of focus).

    lighting: |
      Top-down dramatic — única fuente es lámpara superior del túnel (no de su casco).
      Crea shadow profunda bajo cuencas oculares, bajo barbilla, bajo nariz.
      Ojo único central iluminado tenuemente, glistens reflectante.
      Resto de la cara en penumbra parcial.

    pose_expression: |
      Cuerpo estático (de pecho hacia arriba visible). Hombros caídos relajados,
      pero la postura comunica espera. Ojo único fijo en cámara, NO parpadea durante
      todo el shot. Boca ligeramente apretada, sin sonrisa. Sin gesto de manos visible.

    atmosphere: |
      Polvo fino en suspensión, visible como motas iluminadas en el haz de luz.
      Ligera condensación visible en su exhalación (frío subterráneo).
      Out of focus background sugiere texturas de roca y vigas de madera.

    composition: |
      Slight low angle (5-10 grados desde abajo) que amplifica menace.
      Sujeto centrado simétricamente.
      Rule of thirds NO respetada — composición central deliberada para creep.
      Profundidad de campo shallow — solo cara enfocada, fondo blur 30%.

    color_emphasis: |
      Paleta dominante: marrones tierra + grises piedra + crushed blacks.
      Accent color: NINGUNO en este shot — el rojo se reserva para shots de objetos peligrosos.
      Skin tones: grisáceos enfermizos, no warm.

    mood: |
      Ominous + intimate threat + uncanny puro. El viewer siente que Bruno LO ESTÁ MIRANDO.
      Una pausa de tensión, no acción.

  reference_anchor_image:
    needed: true
    description: "Bruno character anchor — se debe crear UNA reference image al inicio del proyecto y reusar en TODOS los shots con Bruno. Cross-shot character consistency es CRÍTICO."

  film_grain_intent: visible_8_to_10_percent
  vignette_intent: pronunciada
```

---

## Reglas de coherencia visual cross-shot

### Regla 1 — **Character consistency obligatoria**

Si Bruno aparece en 10 shots distintos, debe ser EL MISMO Bruno en los 10.
- Mismo diseño visual (cara, cuerpo, ropa, props)
- Misma lámpara con mismo parche de tape rojo (visual signature)
- Mismas proporciones (cuello largo siempre 3x normal)

**Arquitecto especifica:**
- `reference_anchor_image: needed: true` para personajes principales
- El ingeniero crea UNA reference image al inicio y la reusa con IP-Adapter / Reference Mode

### Regla 2 — **Lighting coherente con el setting + cambia con narrativa**

El setting tiene lighting general (de `environments.md`). Pero CADA shot puede tener variación:
- Shot establishing wide → lighting general del setting
- Close-up del peligroso → top-down dramatic (sombras duras)
- POV manos → lighting de objeto en mano (linterna ilumina manos)
- Counterfactual outro → lighting OPUESTO (warm soft)

### Regla 3 — **Composition por mood del segment narrativo**

```
HOOK (creep + uncanny) → composition centrada simétrica, low angle slight
SETUP (descriptive)    → composition tercios respetada, eye-level
DECISION points        → POV con UI elements, regla composición rota para urgency
CONSEQUENCE peligrosa  → composition asimétrica desbalanceada (chaos)
CLIMAX                 → composition extrema (extreme close-up + high angle threat)
OUTRO cozy             → composition tercios respetada, eye-level cálido
```

### Regla 4 — **Color emphasis por shot, accent isolation por video**

El video TIENE un accent color (e.g., rojo para mina-Bruno). Pero NO todos los shots tienen accent isolation.
- Shots de objetos peligrosos (medidor, alarma, dinamita) → accent rojo
- Shots de personajes → sin accent forzado (la paleta dual carga el peso)
- Shots de setting general → paleta dominante sin accent
- Outro → SIN accent (todo cálido uniforme)

### Regla 5 — **Atmosphere realista pero exagerada**

El polvo, niebla, vapor, chispas DEBEN ser visualmente PROMINENTES (no sutil real).
- Polvo en suspensión = motas visibles en haz de luz
- Niebla baja = visible a nivel piso
- Vapor respiración = visible en cold settings
- Chispas = visible flashes blancos rápidos

Si arquitecto describe "polvo en suspensión" → ingeniero debe hacerlo VISIBLE en la imagen, no sutil background.

---

## Image description by shot type

### Establishing wide (H2 setup)
**Foco:** mostrar escala + setting + establish dyad

```yaml
visual_description:
  scene: "Wide shot del túnel principal de la mina. Bruno y Pablo al fondo (small in frame), conectados por escalera de madera. Tres niveles de túneles visibles, profundidad infinita."
  lighting: "Multi-source ambient — lámparas de cascos + lámparas colgantes intermitentes a lo largo del túnel"
  pose_expression: "Bruno camina lento hacia cámara. Pablo detrás, levemente desfazado, brazos a los costados"
  atmosphere: "Polvo en suspensión espeso, niebla baja, vapor de respiración. Frío subterráneo evidente"
  composition: "Wide angle, rule of thirds respetada. Subjects en el tercio inferior. Profundidad de campo deep — todo enfocado para mostrar escala"
  color_emphasis: "Marrones tierra dominantes + grises piedra. Lámparas amarillas como puntos cálidos"
  mood: "Establish + claustrofobia + escala oprimente"
```

### Medium shot character (presentation)
**Foco:** introducir personaje con identity clara

```yaml
visual_description:
  scene: "Medium shot frontal de PABLO solo, hasta cintura visible. Detrás se ve el setting blurry (mina)"
  lighting: "Side light suave desde la derecha. Crea contour cálido en el lado derecho de la cara. Lado izquierdo en sombra parcial"
  pose_expression: "Pablo de pie estático. Sonrisa permanente leve. Ojos pequeños negros mirando hacia cámara pero ligeramente ajeno. Manos cruzadas sobre el overol jean"
  atmosphere: "Algo de polvo pero menos que en wide. Sin niebla aquí"
  composition: "Subject centrado en frame. Slight upward angle (eye level a su altura). Profundidad media — Pablo en focus, fondo soft blur"
  color_emphasis: "Marrón overol jean dominante + skin tones beige tubérculo. Accent: ninguno (Pablo es safe — sin red)"
  mood: "Cozy uncanny — pareces ingenuamente seguro pero algo no está bien"
```

### Close-up high tension (decision moment)
**Foco:** comunicar tensión + character agency

```yaml
visual_description:
  scene: "Close-up frontal del rostro de BRUNO. Ojo único FIJO en cámara. Cabeza ocupa 60% del frame"
  lighting: "Top-down dramatic ÚNICA fuente. Crea sombras duras bajo cuencas oculares, casi todo el rostro en sombra excepto eye + parte superior frente"
  pose_expression: "Estático. Ojo único no parpadea. Boca ligeramente apretada. Es lo más amenazante posible sin hacer nada"
  atmosphere: "Polvo + condensación de respiración (frío). Quietud cargada"
  composition: "Centered, low angle slight 5 grados. Profundidad shallow extreme — solo eye en focus crítico"
  color_emphasis: "Crushed blacks dominantes. Skin tones grisáceos. NO accent — pero el eye glistens sutilmente warm (cálido sobre el cool)"
  mood: "Uncanny extreme + intimate threat"
```

### POV (decision point con UI)
**Foco:** inmersión + agency del viewer

```yaml
visual_description:
  scene: "POV first-person. Tus manos visible saliendo desde bottom del frame, sosteniendo linterna. Bruno frente a vos, slightly out of focus. Túnel mina como fondo"
  lighting: "Lámpara del casco de Bruno apunta hacia vos creando rim light en sus contornos. Tus manos iluminadas por la luz del túnel"
  pose_expression: "Tus manos: dedo a milímetros del botón de la linterna, tensión visible en knuckles. Bruno: estático, mirando a tu dirección, lámpara apagada"
  atmosphere: "Polvo, niebla, frío. Sensación de aliento contenido"
  composition: "POV centrado, manos en el tercio inferior. Bruno en el tercio medio. Tunnel converging lines hacia centro deep"
  color_emphasis: "Paleta cool desaturada. Accent: NINGUNO en el shot mismo, pero UI countdown LOADING amarilla/blanca sobreimpresa"
  mood: "Tu decisión. Urgencia. Punto de no retorno"
```

### Detail shot (objeto crítico)
**Foco:** subrayar el peligro

```yaml
visual_description:
  scene: "Detail shot del MEDIDOR DE GAS en la mano de Bruno. Pantalla LCD vintage con números parpadeantes en rojo. Caja amarilla industrial con stickers de warning visible"
  lighting: "La pantalla LCD emite su propia luz roja, iluminando la mano que sostiene y la cara cercana de Bruno. Rim light desde lámpara superior"
  pose_expression: "Mano de Bruno sostiene firme. Dedos largos, pálidos, ligeramente deformados. Sin movimiento"
  atmosphere: "El red emite glow leve en aire que se mezcla con polvo en suspensión"
  composition: "Extreme close-up. Pantalla LCD ocupa 70% del frame. Macro lens feel"
  color_emphasis: "RED INTENSO domina (#FF0000 emisivo). Resto en negros/marrones. Accent isolation máxima"
  mood: "Algo está mal. El peligro es ahora medible"
```

### Climax shot (post H5)
**Foco:** el momento más impactante visual del video

```yaml
visual_description:
  scene: "Extreme close-up del TALADRO en acción, chispas saltando del metal sobre roca. Visible: cilindro del taladro + chispas en arc"
  lighting: "Las chispas son la fuente de luz. Resto del frame casi black. Flashes blancos cortos creando rim light momentáneo sobre el taladro"
  pose_expression: "Movimiento implícito — el taladro está activo (animation lo confirma). Sin pose humana visible en este shot"
  atmosphere: "Chispas como flashes blancos rápidos. Humo fino. Olor a metal quemado implícito"
  composition: "Extreme close-up centered. Profundidad mínima. Macro shot"
  color_emphasis: "RED del taladro hot + WHITE flashes chispas + crushed blacks. Máxima contrast"
  mood: "Punch visceral final. Climax horror"
```

### Counterfactual outro shot (H6)
**Foco:** catharsis + contraste tonal

```yaml
visual_description:
  scene: "Medium shot warm cozy. Pablo y vos sentados en una mesa de madera de cantina minera. Pablo sirve pan con queso. Vos del otro lado, sosteniendo cartas"
  lighting: "Multi-source warm — lámpara ámbar tungsten colgante encima, ventana al fondo con luz dorada del amanecer entrando, vela en la mesa"
  pose_expression: "Pablo sonríe natural mostrando dientes pequeños, mano serving. Tus manos visibles del otro lado de la mesa con cartas, posición relajada"
  atmosphere: "Aire cálido visible, sin polvo, vapor sutil del pan caliente"
  composition: "Eye level, rule of thirds respetada. Profundidad media — ambos enfocados"
  color_emphasis: "WARM cálidos: dorados + ámbar + marrones cálidos. Sin accent — todo cohesivo cálido. CONTRASTE TOTAL con el horror previo"
  mood: "Catharsis + relief + cozy nostalgia. El viewer SUSPIRA"
```

---

## Reference anchor images — para character consistency

### Cuándo es obligatorio

- Personajes que aparecen en >2 shots → reference anchor obligatorio
- Settings que recurren → reference anchor opcional
- Personajes que aparecen en 1 shot → opcional

### Qué specifica el arquitecto en el SPEC

```yaml
reference_anchor_requirements:
  - character: BRUNO
    needed: true
    detail_intent: |
      Generar UNA imagen de Bruno standalone, neutral pose, lighting básico.
      Esta imagen es la "biblia" — todos los shots con Bruno deben matchear:
      - Misma proporción de cuello (3x normal)
      - Mismo ojo único en mismo position
      - Misma ropa minera (chaleco + tirantes + delantal)
      - Mismo casco con tape rojo en el borde
    purpose: "Cross-shot character consistency. Bruno NUNCA varía físicamente entre shots."

  - character: PABLO
    needed: true
    detail_intent: |
      Pablo standalone neutral pose. Detalles:
      - Cuerpo ovoide tubérculo (no más alto que tu cintura)
      - Sin nariz visible
      - Overol jean con tirantes
      - Pelo rubio escaso visible
    purpose: "Cross-shot character consistency."
```

**El ingeniero usa estas anchor images como reference (IP-Adapter, Seedream 4.5 Sequence Mode, Nano Banana Pro multi-image, etc.).**

---

## Coherencia entre shots consecutivos

### Continuity rules

Si shot N termina con Bruno mirando a la derecha, shot N+1 (su POV) debe mostrar lo que está a la derecha (no a la izquierda).

Ejemplos:
- Shot 1 Bruno close-up mirando hacia abajo → Shot 2 POV de Bruno mirando al pozo (consistente)
- Shot 1 Bruno mirando a vos → Shot 2 POV tus manos visible (consistente)
- Shot 1 Bruno con lámpara apagada → Shot 2 mismo Bruno con lámpara encendida sin explicación (INCONSISTENT — necesita transición)

### Shot-to-shot transitions

(Detalle de transiciones específicas en `animation-direction.md`. Acá solo intent visual.)

- Hard cut → no overlap entre shots, instantáneo
- Fade to black → transición tonal o de hito
- Light leak → suave entre actos
- Whip → motion-blur entre shots high-energy

---

## Special visual moments

### VFX transformations

Cuando hay transformación visual del personaje (Miro cambia color, Bruno parpadea ojo único):

```yaml
vfx_moment:
  shot_id: shot_hook_bruno_blink
  description: "Bruno parpadea su ojo único — único acto físico no-humano visible"
  timing: "0.5s a 1.5s del shot"
  what_animates: |
    Solo el ojo único de Bruno cierra lentamente (0.4s) y abre (0.4s).
    El resto del cuerpo de Bruno permanece estático.
    Animation type intent: needs_motion (not Ken Burns, real motion).
  intent_for_animation: "Premium tier — debe verse natural"
```

### Composite shots

Cuando un shot requiere COMPOSITE de elementos (e.g., POV + UI overlay):

```yaml
composite_shot:
  shot_id: shot_dp1_pov_with_ui
  base_image: "POV con manos + Bruno + túnel"
  overlay_elements:
    - { type: ui_countdown, position: "Y 40% center", description: "círculo countdown 3-2-1" }
    - { type: ui_buttons, position: "Y 65% paired left/right", description: "ENCIENDES vs ESPERAS" }
    - { type: caption_narration, position: "Y 75% center", description: 'Sync con script segment decision_1_trigger' }
  intent_to_engineer: "El base image se genera sin UI. UI elements se compositan en HyperFrames después."
```

---

## Anti-patterns en image direction

❌ **Scene description vague** ("Bruno close-up") sin lighting/pose/atmosphere details → engineer rellena con drift
❌ **Falta reference anchor** para personajes recurrentes → character drift cross-shots
❌ **Lighting genérico** que no encaja con setting → look incoherente
❌ **Composition sin intent** ("plano medio" sin specify ángulo / DOF / rule) → engineer adivina
❌ **Color emphasis ausente** → ingeniero usa paleta default
❌ **Mood ausente** → ingeniero no sabe el tono emocional
❌ **Atmosphere ausente** → imagen se siente "limpia y AI" en lugar de "lugar vivo"
❌ **Inconsistencia continuity** entre shots consecutivos → viewer detecta error
❌ **Especificar prompts técnicos** ("usar Midjourney v6 cfg_scale 7") → es del ingeniero

---

## Validación final per shot

Antes de aprobar shot description en SPEC:

- [ ] ¿Las 7 dimensiones especificadas (scene, lighting, pose, atmosphere, composition, color, mood)?
- [ ] ¿Synced_to_script_segment definido?
- [ ] ¿Reference anchor flag (true/false) definido si character recurrente?
- [ ] ¿Continuity con shot anterior verificada?
- [ ] ¿Film grain + vignette intent matching aesthetic.md?
- [ ] ¿Composite shots (con UI overlay) marcados explícitamente?
- [ ] ¿VFX moments (transformations) descritos si aplican?

---

## Cómo se enchufa con todo lo demás

```
SCRIPT (timeline backbone)
   ↓
   segments con timestamp + synced_to_visual: shot_id
   ↓
SHOT IMAGES (image-direction.md)
   ↓
   con 7 dimensiones por shot
   ↓
ANIMATIONS (animation-direction.md)
   ↓
   tier por shot (premium / standard / draft) + qué animar
   ↓
CAPTIONS (captions.md)
   ↓
   synced_to_script_segment, position, keyword highlights
   ↓
AUDIO (audio-direction.md)
   ↓
   music + SFX + ambient anclados al script timeline
```

**Todo encaja porque todo está sincronizado al script.**
