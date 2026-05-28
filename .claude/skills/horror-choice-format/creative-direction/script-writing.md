# script-writing.md — Craft del script unificado (la columna vertebral temporal)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> **PRINCIPIO FUNDAMENTAL:** la narración define la línea temporal del video. Todo lo demás (imágenes, animaciones, captions, SFX) se ancla a ella.
>
> Story = "Bruno saca el medidor" (qué pasa)
> Narración = "Bruno saca el medidor de gases y lo pone frente a tu cara. La pantalla parpadea en rojo, dice: 'Hay una grieta en el túnel 4. Vamos.'" (qué se dice EXACTAMENTE)
>
> **Estas son cosas distintas.** Una buena historia con script genérico = mediocre. Una historia simple con script crafted = viral.

---

## La función del script unificado

El script unificado tiene 3 funciones simultáneas:

1. **TEMPORAL backbone** — Define la línea de tiempo del video. Cada segmento tiene timestamp + duration. Imágenes, animaciones, captions, SFX se enchufan acá.

2. **CRAFT linguístico** — Cada palabra está elegida. "Susurra" ≠ "dice". "Te arrastra" ≠ "te lleva". "Caes" ≠ "vas hacia abajo". La elección de palabras carga peso emocional.

3. **DELIVERY blueprint** — Cada segmento incluye notas de delivery (pace, tone, pausa después, susurro vs voz normal) para que el ingeniero pueda producir TTS con la inflexión correcta.

---

## Estructura del script unificado

### ⚠️ IMPORTANTE — Timestamps NO son absolutos

El script NO contiene `timestamp_start` ni `timestamp_end` absolutos. Por dos razones:

1. **TTS no genera duración exacta.** Si decís "este segment dura 1.5s" pero ElevenLabs genera 2.1s, no se puede comprimir → cascade de timeline rota.
2. **El timeline real lo computa el ingeniero** después de generar TTS: orden + duración real + pausas estrictas → línea temporal final.

El arquitecto provee:
- `target_duration`: aproximación de cuánto debería durar (guía, NO regla)
- `pause_after_strict_seconds`: ESTRICTO — decisión creativa de cuánto silencio dejar
- `order`: secuencia (1, 2, 3, ...)

El ingeniero computa:
- Real timeline post-TTS
- Sync de visuales, captions, SFX, animaciones con timestamps reales
- Ajustes si total > o < target duration

### Formato canónico v2

```yaml
narration_script:
  meta:
    target_total_duration: 90s  # aproximación target
    target_pace_wpm: 95  # validado H-choice
    estimated_word_count: 142
    speakers: [narrator]  # o [narrator, bruno, pablo] si multi
    register: tuteo_presente_historico  # o voseo_presente_historico

  segments:
    - id: <unique-id>
      order: 1  # secuencia explícita
      speaker: narrator | <character-name>
      text: "<exact-text>"
      target_duration: ~1.5s  # APROXIMACIÓN, no estricto
      delivery:
        pace: <fast | medium | slow>
        tone: <intimate | alarming | descriptive | climactic | cozy | etc.>
        volume: <whisper | normal | emphasis>
        emotion: <neutral | dread | urgency | catharsis | etc.>
      pause_after_strict_seconds: <float>  # ESTRICTO — decisión creativa
      voice_processing_intent: <standard | custom_per_character>
      lip_sync_intent: <none | required | optional>
      countdown_ui_after: <seconds, opcional para decision points>
      keyword_highlights_in_caption: [{word: X, color: Y}]
```

**El ingeniero NO necesita timestamps absolutos del arquitecto. Los computa de:**
- `order` → secuencia
- `target_duration` → guía (real depende de TTS)
- `pause_after_strict_seconds` → SI es respetado al pie
- `countdown_ui_after` → tiempo de UI sin voiceover

### Ejemplo de script completo (basado en ref-03 Bruno/Pablo)

```yaml
narration_script:
  meta:
    target_total_duration: 92s
    target_pace_wpm: 92
    estimated_word_count: 145
    speakers: [narrator, bruno]
    register: tuteo_presente_historico

  segments:

    # ========== HOOK ==========
    - id: hook_warning
      order: 1
      speaker: narrator
      text: "No confíes en él."
      target_duration: 1.5s  # aproximación
      delivery:
        pace: slow
        tone: alarming
        volume: whisper
        emotion: dread
      pause_after_strict_seconds: 0.5  # estricto
      keyword_highlights_in_caption: []  # toda la frase es warning, no inline highlight

    - id: hook_dilema
      order: 2
      speaker: narrator
      text: "Elige a tu compañero para esta noche, Bruno o Pablo."
      target_duration: 2.5s
      delivery:
        pace: medium
        tone: alarming
        volume: normal
        emotion: urgency
      pause_after_strict_seconds: 0.8
      keyword_highlights_in_caption:
        - { word: BRUNO, color: yellow }
        - { word: PABLO, color: yellow }

    # ========== SETUP ==========
    - id: setup_bruno_intro
      order: 3
      speaker: narrator
      text: "Si elegís a Bruno, estás en una mina a 200 metros bajo tierra, turno nocturno, sin señal."
      target_duration: 5s
      delivery:
        pace: medium
        tone: descriptive
        volume: normal
        emotion: neutral
      pause_after_strict_seconds: 0.3
      keyword_highlights_in_caption:
        - { word: BRUNO, color: yellow }
        - { word: MINA, color: cyan }

    - id: setup_bruno_action
      order: 4
      speaker: narrator
      text: "Bruno apaga los cascos de luz y susurra:"
      target_duration: 2.5s
      delivery:
        pace: medium
        tone: descriptive
        volume: normal
        emotion: dread_buildup
      pause_after_strict_seconds: 0.3

    - id: setup_bruno_dialogue
      order: 5
      speaker: bruno  # personaje, NO narrator
      text: "Los ojos se adaptan solos."
      target_duration: 2s
      delivery:
        pace: slow
        tone: intimate
        volume: whisper
        emotion: neutral_creepy
      pause_after_strict_seconds: 0.5
      voice_processing_intent: "voz Bruno distinta del narrator — pitch slightly lower + reverb cave + heavy dampening"
      lip_sync_intent: required  # Bruno habla visible en cámara

    # ========== DECISION 1 ==========
    - id: decision_1_trigger
      order: 6
      speaker: narrator
      text: "Ahora debes de decidir, enciendes tu linterna o esperas."
      target_duration: 3s
      delivery:
        pace: medium
        tone: urgency
        volume: normal
        emotion: urgency
      pause_after_strict_seconds: 0  # immediately countdown UI plays
      countdown_ui_after: 3s  # UI corre 3s sin voiceover
      keyword_highlights_in_caption:
        - { word: LINTERNA, color: red }
        - { word: ESPERAS, color: cyan }

    # ========== CONSEQUENCE 1 ==========
    - id: consequence_1_setup
      order: 7
      speaker: narrator
      text: "Si la enciendes,"
      target_duration: 1.5s
      delivery:
        pace: medium
        tone: descriptive
        volume: normal
        emotion: dread
      pause_after_strict_seconds: 0.2
      keyword_highlights_in_caption:
        - { word: ENCIENDES, color: red }

    - id: consequence_1_action_1
      order: 8
      speaker: narrator
      text: "Bruno te agarra del brazo,"
      target_duration: 2s
      delivery:
        pace: medium
        tone: descriptive_dread
        volume: normal
        emotion: dread
      pause_after_strict_seconds: 0.2

    - id: consequence_1_action_2
      order: 9
      speaker: narrator
      text: "te arrastra al borde del pozo,"
      target_duration: 2s
      delivery:
        pace: medium
        tone: descriptive_dread
        volume: normal
        emotion: dread
      pause_after_strict_seconds: 0.2

    - id: consequence_1_action_3
      order: 10
      speaker: narrator
      text: "y te suelta."
      target_duration: 1s
      delivery:
        pace: slow
        tone: climactic
        volume: emphasis
        emotion: dread
      pause_after_strict_seconds: 1.5  # PAUSA DRAMÁTICA — silencio carga el peso

    - id: consequence_1_climax
      order: 11
      speaker: narrator
      text: "Caes al vacío."
      target_duration: 1.5s
      delivery:
        pace: slow
        tone: climactic
        volume: emphasis
        emotion: dread_climax
      pause_after_strict_seconds: 2.0  # PAUSA DRAMÁTICA + SFX sub-bass thud
      keyword_highlights_in_caption:
        - { word: CAES, color: red }

    # (continúa con DECISION 2, CONSEQUENCE 2, DECISION 3, CLIMAX)
    # ...

    # ========== COUNTERFACTUAL OUTRO ==========
    - id: outro_intro
      order: 25
      speaker: narrator
      text: "Si hubieras elegido a Pablo,"
      target_duration: 2.5s
      delivery:
        pace: slow
        tone: contemplative
        volume: normal
        emotion: catharsis_intro
      pause_after_strict_seconds: 0.5
      keyword_highlights_in_caption:
        - { word: PABLO, color: yellow }

    - id: outro_punchline
      order: 26
      speaker: narrator
      text: "habrían jugado cartas toda la noche, comido pan con queso y subido a la superficie riendo al amanecer."
      target_duration: 6s
      delivery:
        pace: medium_warm
        tone: cozy_warm
        volume: normal
        emotion: catharsis_relief
      pause_after_strict_seconds: 1.5
      keyword_highlights_in_caption: []  # outro sin highlights — todo el texto cálido cohesivo

    # ========== LOOP CTA (opcional) ==========
    - id: loop_cta
      order: 27
      speaker: narrator
      text: "Elige a tu compañero para..."
      target_duration: 2.5s
      delivery:
        pace: slow
        tone: cliffhanger
        volume: whisper
        emotion: anticipation
      pause_after_strict_seconds: 0  # video termina
      keyword_highlights_in_caption: []
```

---

## Las 8 reglas del craft del script

### Regla 1 — **Cada palabra tiene peso**

Las palabras NO se eligen por sinónimo cercano. Cada elección comunica algo específico.

| Genérico ❌ | Crafted ✅ | Por qué |
|------------|-----------|---------|
| "dice" | "susurra" | Comunica intimacy + sound dampened + intimate threat |
| "te lleva" | "te arrastra" | Comunica resistance + violence |
| "vas hacia abajo" | "caes" | Comunica loss of control + immediacy |
| "es peligroso" | "no confíes en él" | Comunica direct warning + intimate |
| "hay un problema" | "algo no está bien" | Comunica ambiguity + dread |
| "muere" | "tu cuerpo se rinde" | Comunica gradual + visceral |

### Regla 2 — **Frases cortas concatenadas con comas**

```
✅ "Bruno te agarra del brazo, te arrastra al borde del pozo, y te suelta. Caes al vacío."

❌ "Bruno te agarra del brazo mientras te arrastra hacia el borde del pozo hasta que finalmente decide soltarte y caer al vacío."
```

**Por qué:** las frases cortas concatenadas crean **ritmo de acción**. Las oraciones largas pierden el viewer.

### Regla 3 — **Pausas dramáticas marcadas EXPLÍCITAMENTE**

Las pausas son craft, no técnica. El silencio CARGA peso emocional cuando bien colocado:

- **Pre-climax:** 1.5-2.0s antes de la frase impactante
- **Post-action verb:** 0.5s después de verbos críticos ("te suelta", "se acerca")
- **Entre setups y consecuencias:** 0.3-0.5s para que el viewer procese
- **Antes del counterfactual:** 1.0s para shift tonal

### Regla 4 — **Verbos en presente histórico SIEMPRE**

```
✅ "Bruno saca el medidor"
✅ "La pantalla parpadea en rojo"
✅ "Te agarra del brazo"

❌ "Bruno sacó el medidor" (pasado)
❌ "Bruno va a sacar el medidor" (futuro)
❌ "Bruno está sacando el medidor" (continuo)
```

**Por qué:** presente histórico = acción AHORA. Pasado = "te cuento una historia ajena". Es la diferencia entre inmersivo vs documental.

### Regla 5 — **Segunda persona — ELEGIR voseo o tuteo + mantener**

```
✅ Tuteo: "tú eliges", "tú te quedas", "tu mano busca"
✅ Voseo: "vos elegís", "vos te quedás", "tu mano busca"

❌ Mix: "vos eliges" (mezclado)
❌ Tercera persona: "el espectador decide"
```

Decisión por video. Una vez decidido — CONSISTENTE.

### Regla 6 — **Phrases signature que se repiten entre videos**

Estas phrases son brand del formato. Aparecen en TODOS los videos:

| Phrase | Cuándo aparece | Función |
|--------|----------------|---------|
| "Elige a tu compañero para esta noche" | Hook (siempre) | Tagline universal |
| "Si elegís a [X]" | Setup + cada consequence | Conditional framing |
| "Ahora debes de decidir" | Trigger de cada decisión | Decision marker |
| "[ACCIÓN A] o [ACCIÓN B]" | Después de "ahora debes de decidir" | Binary options |
| "Si la enciendes, ..." / "Si esperas, ..." | Consequence framing | Outcome reveal |
| "Si hubieras elegido a [SAFE]..." | Counterfactual outro | Catharsis signal |
| "habrían [VERBO BANAL]..." | Outro punchline | Mundano absurdo |

**Reusarlas crea brand recognition. NO inventarlas frescas cada video.**

### Regla 7 — **Word count target por sección**

Validado contra referentes:

| Sección | Duration target | Word count target |
|---------|-----------------|-------------------|
| Hook | 3s | 8-12 palabras |
| Setup | 10-12s | 25-35 palabras |
| Decision 1 + trigger | 3s | 8-12 palabras |
| Consequence 1 | 10-15s | 15-25 palabras |
| Decision 2 + trigger | 3s | 8-12 palabras |
| Consequence 2 | 10-15s | 15-25 palabras |
| Decision 3 + trigger | 3s | 8-12 palabras |
| Climax | 8-12s | 12-20 palabras |
| Counterfactual outro | 10-12s | 25-35 palabras |
| Loop CTA | 0-5s | 5-8 palabras |
| **TOTAL** | **90s** | **130-160 palabras** |

**Validación:** ref-03 tiene ~145 palabras en 92s = 95 wpm. Está en el sweet spot.

### Regla 8 — **Test "decílo en voz alta"**

Antes de aprobar el script, leelo en voz alta. Si suena:
- **Como audiolibro formal** → demasiado literario, reescribir
- **Como Hollywood trailer** → demasiado teatral
- **Como newsletter copy** → demasiado neutral
- **Como "te cuento un secreto entre vos y yo"** → ✅ correcto

---

## Word choice catalog — verbos validados

### Verbos de acción peligrosa (categoría peligro físico)
- "te agarra" (no "te toma")
- "te arrastra" (no "te lleva")
- "te empuja" (no "te mueve")
- "te suelta" (no "te deja caer")
- "te destroza" (no "te lastima")
- "te aplasta" (no "te apreta")

### Verbos de movimiento físico
- "caes" (no "vas hacia abajo")
- "te hundes" (no "vas bajo el agua")
- "tropezás" (no "te caés un poco")
- "huís" (no "te escapás")

### Verbos sensoriales
- "sentís el frío del metal" (no "el metal está frío")
- "tu corazón late" (no "estás nervioso")
- "tus pulmones queman" (no "te falta aire")
- "tus huesos crujen" (no "te lastimás")

### Verbos de habla (specific)
- "susurra" (intimate creepy)
- "murmura" (low menacing)
- "grita" (panic / urgency)
- "dice" (neutral — usar con moderación)
- "advierte" (warning con peso)
- "balbucea" (debilidad / miedo)

### Sustantivos de peligro
- "el vacío" (no "el agujero")
- "la oscuridad" (no "lo oscuro")
- "el pozo" (specific concrete)
- "el filo" (peligro implícito)
- "el peso" (físico crushing)

---

## Pausas dramáticas — catálogo

### Patrón 1 — Pausa después de verbo de acción crítico

```
"Bruno te agarra del brazo,
te arrastra al borde del pozo,
y te suelta."
[PAUSA 1.5s]  ← peso del momento
"Caes al vacío."
[PAUSA 2.0s]  ← silencio que carga
```

### Patrón 2 — Pausa pre-decisión (antes de "Ahora debes de decidir")

```
[silencio 1s antes del trigger]
"Ahora debes de decidir,
enciendes tu linterna o esperas."
[silencio 3s mientras countdown corre]
```

### Patrón 3 — Pausa pre-climax (la frase culminante)

```
"Se acerca al espacio."
[PAUSA 2s]
"Escuchás cómo tus huesos se destrozan."
[PAUSA 3s + sub-bass impact]
```

### Patrón 4 — Pausa tonal en counterfactual

```
[end of climax horror]
[PAUSA 1.5s + music shift]
"Si hubieras elegido a Pablo,"
[PAUSA 0.5s]
"habrían jugado cartas..."
```

---

## Multi-narrator script (cuando aplica)

Si el video tiene múltiples speakers (ref-12 Nano + Teresa + narrator):

### Formato con speaker tags

```yaml
- id: dialogue_pablo
  order: 20
  speaker: pablo  # personaje, no narrator
  text: "Si querés, hago café."
  target_duration: 2s
  delivery:
    pace: slow_calm
    tone: cozy
    volume: normal
    emotion: caring
  pause_after_strict_seconds: 0.5
  voice_processing_intent: "voz Pablo distinta del narrator — pitch shift up + warmer EQ"
  lip_sync_intent: required  # Pablo habla visible

- id: narrator_continuation
  order: 21
  speaker: narrator
  text: "Y eso es lo que habrías escuchado, si hubieras elegido a Pablo."
  target_duration: 3s
  delivery: ...
  pause_after_strict_seconds: 0.5
```

### Reglas multi-narrator

- Máximo 3 voces distintas en un video (narrator + 2 personajes)
- Cada speaker tiene voice processing único (decisión creativa de intent, ingeniero lo implementa)
- Captions deben indicar speaker (`captions.md` para detalle)
- NO usar dialogue genérico ("hola, ¿cómo estás?") — cada línea de personaje carga peso narrativo

---

## Cómo el script se sincroniza con TODO lo demás

El script es el **timeline backbone**. Otros artefactos se anclan a él:

```
SCRIPT (timeline backbone)
    ↓
    ├── synced_to_visual → shot list en story-arc.md / image-direction.md
    ├── synced_to_caption → caption list en captions.md
    ├── synced_to_animation → animation tier en animation-direction.md
    ├── synced_to_sfx → SFX events en audio-direction.md
    ├── synced_to_music → music timeline en audio-direction.md
    └── synced_to_ui → UI elements (countdown, loader) en ui-elements.md
```

**Ejemplo de sincronización (segment hook_warning):**
- Script segment: timestamp 0.5-1.8s, text "No confíes en él."
- Visual sync: shot_hook_close_up_bruno_ojo (Bruno cíclope close-up)
- Caption sync: cap_warning_red (en pantalla "NO CONFÍES EN ÉL" rojo glow)
- Animation sync: Kling clip Bruno-eye-blink-slow (5s clip premium tier)
- SFX sync: sub-bass impact a 0.5s + breath audible
- Music sync: drone bajo dark ambient (constante)
- UI sync: ninguno (UI aún no aparece, countdown empieza a 1s)

**El script es el primer artefacto que se diseña.** Después todo lo demás se ajusta.

---

## Output al SPEC — el script unificado

```yaml
# Este es UN solo artefacto en el SPEC, no fragmentado.
narration_script:
  meta:
    target_duration: 92s
    target_pace_wpm: 92
    estimated_word_count: 145
    speakers_present: [narrator, bruno]
    register: tuteo_presente_historico
    tone_overall: intimate_dread_to_catharsis

  segments:
    # ... (el script completo como mostré arriba)
```

**El ingeniero lee este script y produce:**
- TTS con cada segment respetando delivery notes
- Pausas dramáticas exactas (no las decide él, las define el script)
- Multi-narrator si aplica con voice processing distinto
- Whisper sync para captions (basado en este script exacto)

---

## Anti-patterns del script

❌ **Script fragmentado entre múltiples campos del YAML** — pierde la línea temporal coherente
❌ **Voiceover genérico repetido de catálogo sin adaptar** — falta craft
❌ **Frases largas con subordinadas** — viewer pierde foco
❌ **Pasado o futuro tense** — rompe immediacy
❌ **Tercera persona** — rompe inmersión
❌ **Verbos abstractos** ("decide ser valiente") — no visualizable
❌ **Sin pausas marcadas** — narrativa plana
❌ **Word count off-target** (e.g., 200 palabras en 60s = ametralladora) — pace roto
❌ **Phrases signature inventadas frescas cada video** — pierde brand
❌ **Dialogue largo de personajes** (>1-2 frases) — slow pacing
❌ **Script que NO se puede LEER en voz alta naturally** — sounds reading aloud, no narrativa

---

## Validación final del script

- [ ] ¿Script es UN solo artefacto unificado en SPEC?
- [ ] ¿Total word count en rango 130-160 palabras para 90s?
- [ ] ¿Pace ~90-100 WPM?
- [ ] ¿Pausas dramáticas marcadas explícitamente?
- [ ] ¿Cada segment tiene delivery notes (pace, tone, volume, emotion)?
- [ ] ¿Cada segment tiene `order` + `target_duration` + `pause_after_strict_seconds`?
- [ ] ¿NO hay `timestamp_start` ni `timestamp_end` absolutos (que el engineer compute)?
- [ ] ¿Verbos en presente histórico SIEMPRE?
- [ ] ¿Segunda persona consistente (tuteo o voseo, no mix)?
- [ ] ¿Phrases signature del formato presentes?
- [ ] ¿Word choice crafted (no genérico)?
- [ ] ¿Frases cortas concatenadas con comas?
- [ ] ¿Test "decílo en voz alta" pasado?
- [ ] ¿Multi-narrator (si aplica) con voice processing intent definido?

Si ❌ en cualquiera → reescribir esa sección del script.

---

## El script es lo MÁS importante

**Insight crítico:** una historia básica con script BRILLANTE = viral. Una historia épica con script MEDIOCRE = scroll.

@referent-a no es famoso por sus historias (las decisiones son simples). Es famoso por **cómo las cuenta**.

> "Bruno apaga los cascos de luz y susurra: 'Los ojos se adaptan solos.'"

Esa única frase carga más peso narrativo que 30 segundos de exposición genérica.

**El arquitecto invierte el tiempo aquí.** Si el script está crafted, todo lo demás (imágenes, animaciones, captions) encaja naturalmente. Si el script es vago, el ingeniero recibe instrucciones ambiguas y el resultado se siente improvisado.
