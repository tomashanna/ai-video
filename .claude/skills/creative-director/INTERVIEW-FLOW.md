# INTERVIEW-FLOW.md — Cómo el arquitecto entrevista al user

> Flujo general que el arquitecto sigue cada vez que el user inicia un proyecto. Las preguntas se adaptan al template detectado.

---

## Filosofía de la entrevista

**El arquitecto NO IMPROVISA.** Hace preguntas estructuradas, propone opciones del catalog, deja que el user elija. Esto:
- Activa ownership del user
- Asegura cobertura de todos los slots del SPEC
- Evita "saltar" reglas críticas del formato

---

## Las 4 fases de la entrevista

### Fase 1 — Identificación de template + fundamentals
### Fase 2 — Worldbuilding (setting, mood, dyad)
### Fase 3 — Narrative design (story, decisiones, twist, outro)
### Fase 4 — Polish (captions, audio, brand, validación)

---

## Fase 1 — Identificación de template + fundamentals

### Preguntas iniciales

**1.1 Identificar template**
> "¿Qué tipo de video quieres hacer?"
> "¿Es del formato elige-tu-compañero / dilema binario? ¿O algo distinto?"

→ Si user dice "elige a tu compañero / dilema / horror choice" → activá template `elige-tu-companero`
→ Si user describe otro tipo → identificá template (frutas-30s, brand-story, etc.) o pedí más info

**1.2 Confirmar delivery format**
> "¿Reel vertical 9:16? ¿Otro formato (YouTube short, Story, B2B)?"
> Default: Reel vertical 9:16

**1.3 Confirmar duración target**
> "¿Duración? Default es 90s (sweet spot validado). Range posible 60-130s."

**1.4 Identificar serie continuity**
> "¿Este video es standalone o parte de una serie del creator? Si serie, ¿qué número/contexto?"

### Fase 1 — Outputs
```yaml
project_id: <slug-elegido>
template: elige-tu-companero
delivery_format: reel_9_16
duration_target: 90s
is_part_of_series: true/false
series_episode: <numero>
```

---

## Fase 2 — Worldbuilding (setting, mood, dyad)

### Preguntas en orden

**2.1 Setting** (cargar `environments.md` antes)
> "¿Setting? Tengo varios validados:
> - Mina abandonada (subterráneo claustrofóbico)
> - Hotel infinito (liminal horror)
> - Bosque nocturno (folclor)
> - Carretera rural (noir)
> - Cockpit de avión (tecnológico falible)
> - Acuario abandonado (marítimo)
> - Metro nocturno (urbano)
> - Planta industrial (brutalist)
> - Vagón de tren (journey)
> - O algo nuevo: ¿qué tenés en mente?"

→ User elige. Si nuevo → validá que tenga peligro inherente.

**2.2 Mood**
> "¿Qué tono querés? Te propongo:
> - **Uncanny puro / body horror** (Cronenberg-style)
> - **Surrealismo absurdo** (Kafka + AI)
> - **Cosmic horror megalofobia** (Lovecraft)
> - **Claustrofóbico liminal** (backrooms)
> - **Folklor / paranormal** (gnomo, duende)
> - **Industrial brutalist** (peligro mecánico)
>
> O combinación."

→ Mood define color grade + audio + character categories.

**2.3 Archetype dyad** (cargar `characters.md` + `character-pairs.md`)
> "Para tu setting + mood, te tiro 3 pares validados del catálogo:
>
> Opción A: [BRUNO B1 cíclope cuello largo] + [PABLO E1 tubérculo ovoide]
> Opción B: [KRAVEN B3 piel correosa rojiza] + [MATEO C humano normal cozy]
> Opción C: [Nuevo: cabeza-pulpo en buzo vintage] + [Niño-fresa]
>
> ¿Cuál te llama? ¿O querés que tire variaciones?"

→ User elige. Validá:
- Al menos 1 uncanny extremo
- Categorías opuestas
- Nombres con contraste fonético

**2.4 Stakes** (cargar `stakes-catalog.md`)
> "Default stakes = muerte/supervivencia. ¿Mantenemos?
> Si querés otro:
> - Pérdida memoria gradual
> - Trauma psicológico
> - Pérdida identidad
>
> Pero usar otro stake es decisión riesgosa — vital genera más engagement."

→ Validar que stakes elegidos son **visualizables concretamente**.

### Fase 2 — Outputs
```yaml
environment: { setting_type, time_of_day, weather, ambient_creature_optional }
mood: { tone, color_grade_direction, audio_direction }
archetype_dyad: { dangerous + safe with categories, names, descriptions }
stakes_level: { vital_muerte / vital_perdida / etc }
```

---

## Fase 3 — Narrative design (story, decisiones, twist, outro)

### Preguntas

**3.1 Plot pattern** (cargar `plot-patterns.md`)
> "Tenés 10 patterns validados según apariencia × verdad. Para tu mood, te recomiendo:
>
> - **Pattern 1** (clásico bueno=bueno / malo=malo) — straightforward, sin twist
> - **Pattern 3** (seguro era trampa retroactiva) — twist clásico
> - **Pattern 6** (hedonismo eterno) — comentario filosófico
> - **Pattern 4** (peligroso advierte 'no me elijas') — empatía con monster
>
> ¿Cuál te llama? Recordá: chequeo video-log para no repetir."

→ Validá rotación + condiciones del twist si aplica.

**3.2 Hook 0-3s** (cargar `hooks.md`)
> "Hook 0-3s. Te propongo 3 fórmulas:
>
> - **A**: confronta al monstruo en primer plano frame 0
> - **B**: dyad simultáneo en frame 0
> - **C**: setting impossible primero, criaturas después
> - **D**: dialogue del peligroso ('No me elijas...')
>
> ¿Cuál?"

→ Validá que tiene visual uncanny + warning + countdown.

**3.3 3 decisiones** (cargar `story-arc.md`)
> "Diseñemos las 3 decisiones. Vamos uno por uno.
>
> **Decisión 1 (H3, ~18s):** stakes medio.
> 'Ahora debes de decidir: [VERB A] o [VERB B]'
> ¿Qué opciones? Match con setting + archetype."

→ Iterá uno a uno con user. Para cada decisión validá:
- Wording binario action-verb
- Consequence visualizable
- Stakes ascendentes (medio → alto → máximo)

**3.4 Twist / payoff** (cargar `plot-patterns.md` + `shared-universe.md` si aplica)
> "Para el twist final, ¿cómo se cierra? Opciones según pattern elegido:
> ..."

**3.5 Counterfactual outro** (cargar `counterfactual-outros.md`)
> "El outro mostrando qué pasaba con el [SAFE]. Te tiro 3 punchlines:
>
> - **Mundano absurdo**: 'Si hubieras elegido a PABLO, habrían jugado cartas toda la noche, comido pan con queso y subido al amanecer riendo'
> - **Ternura naive**: 'Si hubieras elegido a PABLO, estarías junto a una chimenea con café y un perro echado a tus pies'
> - **Doble filo**: 'Si hubieras elegido a PABLO, habrían visto novelas turcas... y a la mañana descubrirías que él lleva 30 años en esa cabaña sin envejecer'
>
> ¿Cuál te llama?"

### Fase 3 — Outputs
```yaml
plot_pattern: { id, name, twist_conditions if applicable }
hook: { formula, visual_description, voiceover_text, warning_text, countdown_intent }
story_arc:
  setup: ...
  decision_1: { trigger, options, consequence }
  decision_2: { ... }
  decision_3: { ... }
  climax: ...
counterfactual_outro:
  category: <mundano-absurdo / cinismo / ternura / surreal / hedonista / doble-filo>
  text: "..."
  visual: "..."
```

---

## Fase 4 — Polish (captions, audio, brand, validación)

### Preguntas

**4.1 Keyword highlights** (cargar `captions.md` + `keyword-highlights.md` patterns)
> "Identifiquemos keywords para highlight inline. Te propongo:
>
> - Nombres (BRUNO, PABLO) → amarillo
> - Settings críticos (MINA, TÚNEL) → cyan
> - Peligros (LINTERNA, DINAMITA, ALARMA) → rojo
> - Verbos críticos (MUERES, CAES, ESCAPAS) → rojo
>
> ¿Va? ¿Querés cambiar colors? ¿Agregás keywords?"

**4.2 Brand identity** (cargar `brand-and-cliffhanger.md`)
> "Brand:
>
> - Handle del creator: [tu handle]
> - Reel caption: pregunta + hashtags
> - Tagline signature: '[reusable]'
> - Cliffhanger pattern: A (cierre suave) / B (loop CTA explicit) / C (teaser visual)
>
> ¿Confirmás handle y tagline? ¿Cliffhanger pattern?"

**4.3 Shared universe / personajes recurrentes** (cargar `shared-universe.md`)
> "¿Aprovechamos shared universe?
>
> - ¿Algún personaje recurrente del catálogo aparece aquí? (Bruno otra vez? Kraven?)
> - ¿Easter eggs cross-video? (foto en pared, sound cue signature)
> - ¿Personalidad psicológica del archetype más allá del visual? (fiestero, zen, chambero, triste, etc.)"

**4.4 Validación final cross-cutting** (cargar `anti-patterns.md`)
> "Vamos a validar checklist final antes de codificar SPEC:
>
> - ✅ Archetype con uncanny extremo? D2 OK
> - ✅ Keyword highlights identificados? D9 OK
> - ✅ Counterfactual con punchline específica? D13 OK
> - ✅ Hook con visual uncanny + dilema + countdown? D11 OK
> - ✅ Stakes vitales escalantes?
> - ✅ Pattern rotado (no repite último)?
> - ✅ Setting con peligro inherente?
> - ✅ Voiceover en segunda persona + presente histórico?
>
> ¿Todo OK?"

### Fase 4 — Outputs
```yaml
captions: { keyword_highlights, position, animation }
brand_identity: { handle, reel_caption, tagline, cliffhanger_pattern }
shared_universe: { canonical_chars_referenced, easter_eggs, signatures }
validation_checklist: all_passed
```

---

## Después de las 4 fases: HANDOFF

Cuando los 4 fases están completos:

**5.1 Codificar SPEC**
> El arquitecto genera el archivo `creative-specs/<project-id>.yaml` con todos los outputs de las 4 fases consolidados.

**5.2 Last review con user**
> "Te muestro el SPEC completo. ¿Confirmás? ¿Cambiamos algo?"
> Si user cambia → iterar.

**5.3 Aprobación final + handoff message**
> "Spec aprobado. Pasamos al ingeniero.
>
> El ingeniero leerá `creative-specs/<project-id>.yaml` y producirá el video.
> Vos vas a participar de nuevo en:
> - Review del primer draft del video
> - Decisiones técnicas que requieran tu input creativo (ej: 'el modelo AI no puede reproducir tu cíclope cuello largo, te propongo variante')
>
> Pero la ejecución técnica (TTS, render, captions sync, color grade CSS) la maneja el ingeniero sin pedirte input."

---

## Patrones de entrevista por tipo de user

### Si el user es **nuevo** (primera vez con el formato)
- Más explicaciones por pregunta
- Mostrar 3+ opciones de cada slot
- Validar concepts simples antes de avanzar

### Si el user es **experimentado** (ya conoce el formato)
- Preguntas más rápidas, menos explicaciones
- "Default OK?" para slots típicos
- Foco en decisiones creativas únicas

### Si el user es **decisivo** ("ya tengo el concepto en la cabeza")
- Dejá que cuente la idea full primero
- Después validá vos cumplimiento de reglas
- Mostrá gaps con propuestas

### Si el user es **explorativo** ("no sé qué quiero")
- Empezá por mood + setting
- Proponé 3 paths distintos
- Iterá rápido hasta que se entusiasme con UNO

---

## Anti-patterns en entrevista

❌ **Hacer todas las preguntas en una sola sesión gigante** → user se agota
❌ **Proponer 1 sola opción** → no activás ownership
❌ **Aprobar pattern repetido sin chequear video-log** → ennui audience
❌ **Saltarte fase 4 validation** → spec con gaps
❌ **Avanzar sin que user confirme cada fase** → spec termina con cosas que user no aprobó
❌ **Tocar territorio del ingeniero en preguntas** ("¿qué LUFS querés?") → user confunde scope
❌ **Improvisar archetype sin consultar catalog** → pierdes consistencia con sistema validado

---

## Ejemplo de entrevista completa (transcript hipotético)

```
ARQUITECTO: "Hola. ¿Qué tipo de video querés hacer?"

USER: "Algo tipo elige a tu compañero, en un faro nocturno."

ARQUITECTO: "Perfecto. Template = elige-tu-compañero. Setting = faro nocturno.
Es genial — me cuadra con mood claustrofóbico marítimo. ¿Pensaste en
mood específico? Te propongo:
- Cosmic horror (lovecraftiano, escala marina aterradora)
- Surrealismo absurdo (criaturas weird en faro)
- Folklor (sirenas, mitos del mar)
- Claustrofobico técnico (faro mecánico que falla)
¿Cuál te llama?"

USER: "Cosmic horror suena bien."

ARQUITECTO: "Top. Para faro + cosmic horror + dyad uncanny, te tiro 3 pares:
A: KAEL [B3 piel correosa rojiza con bata de farero raído] +
   LEO [C humano normal cozy con uniforme de marinero relajado]
B: KRAKAN [Nuevo: cabeza-pulpo en cuerpo humano con chaleco vintage] +
   MIKA [A2 cabeza-medusa con pelo translúcido translucent]
C: OSO [B2 esqueleto humanoide alto, capucha negra] +
   TIO [C humano abuelo amable, pipa]
¿Cuál te llama?"

USER: "B me parece genial — Krakan-pulpo es perfecto."

ARQUITECTO: "Excelente. Sigamos:
- Stakes: vital (caer al mar / devorado por algo abajo)?
- Plot pattern: te recomiendo Pattern 3 (Mika era trampa) o
  Pattern 6 (Mika te lleva al fondo, hedonismo submarino eterno) o
  Pattern 1 (clásico bueno=bueno / malo=malo)?"

USER: "Pattern 6 me parece interesante."

ARQUITECTO: "Buenísimo, eso da mucho juego."
[... continúa con fase 3 ...]
```

---

## Output protocol

Cuando la entrevista termine, el arquitecto:

1. Codifica spec completo en YAML
2. Guarda en `creative-specs/<project-id>.yaml`
3. Avisa al user: "Spec listo. Pasamos al ingeniero."
4. Si user pide tweaks → iterar
5. NO arranca producción técnica desde el arquitecto (el ingeniero lo hace)
