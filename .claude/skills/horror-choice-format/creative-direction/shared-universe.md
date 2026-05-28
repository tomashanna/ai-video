# shared-universe.md — Personajes recurrentes + personalidades relatable + arcos morales cross-video

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El usuario lo señaló como insight crítico:
> "Se repiten personajes entre medio de las historias (se hace ver que es todo un mundo), algunos personajes eran chistosos/de fiesta/tristes/chamberos que hacen reflejar que son similares a uno, personajes que se repiten y que antes eran buenos vs luego son malos y viceversa."
>
> Este doc captura esa dimensión.

---

## Por qué shared universe importa

**Sin shared universe:**
- Cada video es standalone, no acumula
- Follower no tiene razón de quedarse a largo plazo
- No hay "lo conocía a Bruno desde antes"

**Con shared universe:**
- Universo vivo donde los personajes coexisten
- Re-watches por discovery (¿en cuál video apareció Bruno por primera vez?)
- Shares con context "este es Bruno, sale en varios videos"
- Comments enriquecidos: "¡es Bruno otra vez!"
- Brand identity exponencial

**Validado:** @referent-b usa personalidades reconocibles (Bryan-fiestero, Miro-zen). @referent-a reusa Axel entre ref-06 y ref-09. Es estrategia comprobada del nicho.

---

## Las 3 dimensiones del shared universe

### Dimensión 1 — **Recurrencia de personajes** (físico)
### Dimensión 2 — **Personalidades reconocibles** (psicológico)
### Dimensión 3 — **Arcos morales** (narrativo cross-video)

---

## Dimensión 1 — Recurrencia de personajes (físico)

### Cómo se manifiesta

- El mismo character visual aparece en múltiples videos
- Mismo diseño, mismo nombre, misma identidad visual
- Roles pueden cambiar (protagonista, ambient, antagonista, mencionado solo)

### Validado

**Axel** aparece en:
- ref-06 (carretera, peligroso protagonista)
- ref-09 (cockpit, peligroso protagonista)

**Cuándo recurrir un personaje**

1. **Personaje icónico** del primer video genera follower interés
2. **Universo expansion** — diferentes settings, mismo personaje
3. **Easter eggs** — personaje aparece en background sin protagonismo

### Reglas para recurrencia

- **Mantener nombre exacto** entre videos
- **Mantener diseño visual** entre videos (ref image debe estar consistente)
- **Variar ROL pero NO PERSONALIDAD** entre videos
- **Documentar en canonical_characters.yaml** cuándo aparecen y en qué rol

### Ejemplos hipotéticos para nuestro creator

```
KRAVEN aparece en:
- Video 1 (mina): protagonista peligroso
- Video 3 (hotel): background, lo ves en pasillo
- Video 5 (bosque): protagonista ambiguo (twist — siempre era guía)

HUGO aparece en:
- Video 2 (mina alternativa): protagonista peligroso
- Video 6 (acuario): protagonista ambiguo, dice "no me elijas"

SANTI aparece en:
- Video 2 (counterfactual): seguro hace mate
- Video 7 (cabaña): protagonista seguro, hace café
- Video 10 (carretera): SE INVIRTIÓ — protagonista peligroso (twist universo)
```

---

## Dimensión 2 — Personalidades reconocibles (psicológico)

**Insight del user:** "personajes chistosos/de fiesta/tristes/chamberos que hacen reflejar que son similares a uno."

Los personajes top tienen **personalidad distintiva** que los hace memorables. No solo visual — psicológico.

### Las 8 personalidades archetype del formato

#### 1. **EL FIESTERO** (Bryan-style — ref-13)
- Comportamiento: invita al party, hedonismo, "vamos a divertirnos"
- Vibe: enthusiastic, animal magnetism
- Aparente: amigable, buen plan
- Verdad típica: te lleva a hedonismo eterno = pierdes identidad/objetivo
- Catchphrase típica: "Vení, conmigo va a ser fiesta toda la noche"
- Relatable porque: todos tenemos amigo fiestero

#### 2. **EL ZEN / MÍSTICO** (Miro-style — ref-13)
- Comportamiento: calmo, meditativo, "todo está bien"
- Vibe: spiritual, slightly detached
- Aparente: sabio, guía
- Verdad típica: amistad real pero requiere disciplina o sacrificios
- Catchphrase típica: "La paciencia es el camino"
- Relatable porque: idealizamos al maestro espiritual

#### 3. **EL CHAMBERO / TRABAJADOR** (Bruno-style — ref-03)
- Comportamiento: estoico, focused on trabajo, no smalltalk
- Vibe: working-class hero, callado
- Aparente: peligroso por su rudeza
- Verdad típica: realmente seguro, solo es estoico
- Catchphrase típica: "Vamos, hay trabajo que hacer"
- Relatable porque: todos conocemos trabajador serio que parece intimidante

#### 4. **EL TRISTE / DEPRESSED** (hipotético)
- Comportamiento: lento, conversación short, mirada lejana
- Vibe: weight of the world, melancolía
- Aparente: ambiguo (¿peligroso o solo triste?)
- Verdad típica: víctima también del mundo del horror
- Catchphrase típica: "No hay esperanza, pero podemos intentar"
- Relatable porque: todos tenemos momentos así

#### 5. **EL CHISTOSO** (hipotético — Pablo cozy)
- Comportamiento: bromea constantemente, hace chistes malos
- Vibe: tension-breaker
- Aparente: incomoda en horror context, parece raro
- Verdad típica: REAL safe — su humor es coping mechanism
- Catchphrase típica: "Y vos qué cara tenés, parece que viste un fantasma 😂"
- Relatable porque: amigo que rompe la tensión con humor

#### 6. **EL CALMADO / MATEMÁTICO** (Santi-style)
- Comportamiento: analítico, pone problemas en perspectiva, observa antes de actuar
- Vibe: tranquilo, intelectual
- Aparente: seguro (de hecho lo es)
- Verdad típica: seguro confirmado, su calma desactiva peligro
- Catchphrase típica: "Pensemos esto un momento..."
- Relatable porque: el amigo "voice of reason"

#### 7. **EL HISTÉRICO / PARANOICO**
- Comportamiento: alarmista, ve peligro en todo, "salgamos de acá YA"
- Vibe: ansiedad, hypervigilance
- Aparente: ambiguo (¿está loco o ve algo real?)
- Verdad típica: SU paranoia tenía razón — había peligro real
- Catchphrase típica: "Algo no está bien acá, vámonos"
- Relatable porque: la voz de alerta del grupo

#### 8. **EL HEREDERO / CHARMING**
- Comportamiento: smooth, encantador, todo está bajo control
- Vibe: confident, world-traveled, gentlemanly
- Aparente: parece confiable, líder natural
- Verdad típica: trampa retroactiva — su charm oculta peligro real
- Catchphrase típica: "Confía en mí, sé lo que hago"
- Relatable porque: el amigo "demasiado bueno para ser verdad"

### Combinar personalidad con archetype visual

El visual extreme (cíclope, hongo, capybara) + personalidad psicológica = personaje COMPLETO.

| Visual archetype | Personalidad típica que matchea |
|------------------|----------------------------------|
| B1 Cíclope cuello largo | EL CHAMBERO / TRABAJADOR (silent, work-focused) |
| A4 Cabeza-hongo | EL ZEN / MÍSTICO (con su otherness orgánica) |
| C1 Dientes-afilados | EL TRISTE (sad smile que termina mostrando dientes) |
| A1 Capybara antropomorfo | EL FIESTERO (mammal social) |
| D1 Geometric impossible | EL ZEN (otherworldly calm) |
| E1 Vegetal antropomorfo | EL CHISTOSO (absurdez visual matches humor) |
| F1 Industrial hazard | EL HISTÉRICO (paranoia del operario expuesto) |
| C2 Esquelético calvo | EL CHARMING o EL TRISTE (depending on look) |

---

## Dimensión 3 — Arcos morales cross-video

**Insight del user:** "personajes que se repiten y que antes eran buenos vs luego son malos y viceversa."

Esto es WORLDBUILDING NARRATIVO. Cada personaje recurrente puede TRANSFORMARSE a través de los videos.

### Las 4 patrones de arco moral

#### Patrón A — **Always good** (consistencia confirmada)
- Aparece como seguro/safe en TODOS los videos donde sale
- Builds trust del viewer
- Cuando lo ves → "ok, este es de fiar"
- Ejemplo: Mateo siempre cozy seguro

#### Patrón B — **Always bad** (consistencia maléfica)
- Aparece como peligroso en TODOS los videos
- Builds dread del viewer
- Cuando lo ves → "ay no, este otra vez"
- Ejemplo: Kraven siempre amenazante

#### Patrón C — **Good → Bad** (corrupción/decline)
- En video 1, fue seguro/safe
- En video 5, se reveló peligroso
- Narrativa: algo lo cambió (corrupción, trauma, posesión)
- Generates: "wait, NO ERA bueno realmente?"

#### Patrón D — **Bad → Good** (redemption arc)
- En video 1, fue peligroso
- En video 7, se reveló seguro (siempre estuvo manipulado o malentendido)
- Narrativa: redención, malinterpretación, vínculo nuevo
- Generates: "ahora entiendo a Bruno"

### Cómo manejar arcos morales

#### Documentar en canonical_characters.yaml

```yaml
KRAVEN:
  base_archetype: B1
  base_personality: chambero_trabajador
  appearances:
    - video: 1
      role: protagonist_dangerous
      moral_status: malo
      revelation: "Real danger, mata si lo elegís"
    - video: 5
      role: protagonist_ambiguous
      moral_status: bueno (twist)
      revelation: "Era trabajador, su rudeza era preocupación. Su trabajo era PROTEGERTE"
  arc_pattern: B → C (always bad → revealed good)
  arc_explanation: |
    En video 1, Kraven aparece como peligroso clásico.
    En video 5, retroactivamente revelamos: la mina necesitaba revisión, Kraven era el inspector.
    Sus "amenazas" eran advertencias sobre el real peligro (grieta, gas).
    Pablo en video 1 era la trampa real (vibrante pero engañoso).
  generates: "Recapped horror — Kraven REDIMIDO"

SANTI:
  base_archetype: C (humano cozy)
  base_personality: el_calmado_matematico
  appearances:
    - video: 2
      role: protagonist_safe
      moral_status: bueno
      revelation: "Cozy puro, hace mate"
    - video: 10
      role: protagonist_dangerous (twist)
      moral_status: malo
      revelation: "Su calma era manipulation. Te lleva a cabaña aislada donde lleva 30 años atrapando víctimas."
  arc_pattern: A → D (always good → revealed bad)
  arc_explanation: |
    El twist más doloroso: SANTI siempre confió.
    Video 10 revela que su "cozy" era trampa.
    Lleva 30 años en cabaña sin envejecer (categoría C1 doble filo del catálogo).
  generates: "Trust broken — ¿en quién confiar ya?"
```

#### Reglas para arcos

- **NO transformar a un personaje sin justificación narrativa** — el viewer debe poder explicar el arc
- **Documentar arc completo desde el inicio** — sabés qué video va a transformar el personaje
- **Setup visual subtle en videos previos** — un detalle que retroactivamente justifica (e.g., en video 1, foto vieja en pared)
- **NO transformar más de 1 personaje por video** — sobreloads cognitivamente
- **Cooldown entre arcs** — mínimo 3 videos entre transformaciones del mismo personaje

---

## Reflejo en el viewer ("similares a uno")

**Insight del user:** "personajes ... que hacen reflejar que son similares a uno."

Personalidades relatable + arcos morales = viewer se IDENTIFICA con algunos personajes.

### Pares relatable que funcionan

| Personalidad | Por qué resuena |
|--------------|------------------|
| EL FIESTERO | Todos tuvimos amigo así o lo hemos sido |
| EL CHISTOSO | Coping con humor es universal |
| EL TRISTE | Estados depresivos relatable post-pandemia |
| EL CHAMBERO | Working-class hero — viewer trabajador conecta |
| EL CALMADO | Wisdom figure — aspiracional |
| EL HISTÉRICO | Anxiety era — relatable a generación ansiosa |

### Cómo se manifiesta en el video

- **Catchphrase del personaje** que el viewer puede repetir
- **Detalle visual signature** (e.g., Bryan siempre con chaleco, Mateo siempre con su libreta)
- **Behavior coherente** entre videos (Bryan siempre invita a fiesta, Mateo siempre piensa antes de actuar)
- **Hint of viewer in character** — "yo también soy un poco así"

---

## Recurrencia narrativa de SETTINGS

(Heredado de brand-and-cliffhanger.md, expandido acá)

Settings también pueden recurrir:

- **Mismo edificio, diferentes pisos** — hotel piso 14 (video 5), hotel piso 7 (video 8)
- **Mismo bosque, diferentes claros** — bosque del gnomo (video 6), bosque del coyote (video 9)
- **Mismo creator, diferentes refugios** — cabaña del invierno, mina del verano

Genera worldbuilding.

---

## Easter eggs y discovery

**Recompensa al re-watcher.**

### Patterns validados

- **Personaje recurrente en background** sin protagonismo
- **Objeto signature** que aparece en múltiples videos (e.g., una llave dorada specific)
- **Sound cue característica** (e.g., melodía signature cada vez que aparece KRAVEN)
- **Visual marker** (e.g., un cuadro de un faro en pared = adelanto del próximo video del faro)

### Reglas

- 1-2 easter eggs por video (no más, se vuelven cliché)
- NO ser obvios — el viewer descubre en re-watch
- Documentarlos para coherencia cross-video

---

## Output al SPEC

```yaml
shared_universe:
  is_part_of_series: true
  series_name: "Una noche en peligro"
  episode_number: 1  # primer video estableciendo universe

  canonical_characters_in_this_video:
    - name: KRAVEN
      base_archetype: B1_ciclope_cuello_largo
      base_personality: chambero_trabajador
      role_this_video: protagonist_dangerous
      moral_status_this_video: malo_aparente
      arc_pattern_planned: B (always bad — for now, possibly revealed good in future video)
      ref_image_to_create: /assets/anchors/kraven.png
      future_appearances_hint: "Aparecerá en background en video 3 (hotel pasillo) — easter egg"

    - name: PABLO
      base_archetype: E1_tuberculo_ovoide
      base_personality: el_chistoso
      role_this_video: protagonist_safe
      moral_status_this_video: seguro_aparente
      arc_pattern_planned: A (always good — confirmed)
      ref_image_to_create: /assets/anchors/pablo.png
      future_appearances_hint: "Aparecerá en video 4 outro counterfactual (también cozy)"

  characters_referenced_in_background_this_video:
    - name: HUGO
      where: "Foto en pared del living, video 5s — easter egg de personaje que aparecerá en video 6"
      ref_image_to_create: /assets/anchors/hugo.png

  setting_recurrence:
    this_video_setting: mina_abandonada_pozo_central
    setting_will_recur: false  # mina específica para este video, otras minas posibles
    visual_marker_for_universe: "El cuadro del faro en oficina del minero (visible 0:11) reaparecerá en video del faro"

  moral_arcs_active:
    - character: KRAVEN
      this_video_arc: malo (establishing arc B)
      future_planned: "Posible reveal redemption en video 5 — TBD"

  catchphrases_signature:
    - character: KRAVEN
      catchphrase: "Vamos, hay trabajo que hacer"
      timestamp_in_video: "0:15"

  visual_signatures:
    - character: KRAVEN
      detail: "Su lámpara de casco SIEMPRE tiene un parche de tape rojo distintivo"
      purpose: "viewer reconoce a Kraven en future cameos"

  easter_eggs_this_video:
    - description: "Foto de HUGO joven en pared del living a 5s"
      purpose: "Setup para video 6 — Hugo regresa como protagonista"
    - description: "Sonido melódico signature de Kraven (3 notas low brass) cada vez que aparece"
      purpose: "audio recognition cross-video"
```

---

## Anti-patterns en shared universe

❌ **Recurrir personaje SIN documentar** — pierdes la track entre videos
❌ **Cambiar diseño visual de personaje recurrente** — viewer no lo reconoce
❌ **Transformar arc moral sin setup retroactivo** — twist parece arbitrario
❌ **3+ personajes recurrentes en mismo video** — confunde, sobrecarga
❌ **Easter eggs demasiado obvios** — pierden el "discover" factor
❌ **Personalidad inconsistente entre videos** (Bryan fiestero en v1, Bryan triste en v3 sin razón) — incoherente
❌ **Mismo setting EXACTO en videos consecutivos** (mina otra vez en v2) — pierde variedad
❌ **Sin track de canonical_characters.yaml** — eventualmente perdés el universo

---

## Validación final de shared universe

- [ ] ¿Es video standalone o parte de serie? Si serie → documentar canonical chars
- [ ] ¿Personaje peligroso y seguro tienen personalidad PSICOLÓGICA además de visual?
- [ ] ¿Si recurre personaje del universo → diseño visual + nombre EXACTOS consistentes?
- [ ] ¿Arco moral del personaje recurrente documentado?
- [ ] ¿1-2 easter eggs incluidos?
- [ ] ¿Visual signatures definidos para reconocimiento cross-video?
- [ ] ¿Catchphrase signature decidida si aplica?
- [ ] ¿canonical_characters.yaml actualizado?

Si ❌ en cualquiera → ajustar antes de SPEC.
