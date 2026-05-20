# audio-direction.md — Dirección creativa de música + SFX + ducking + reverb

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define INTENT de audio. El ingeniero implementa con tracks específicos, BPM exactos, dB de ducking, plugins de EQ, LUFS targets. Esta es DIRECCIÓN, no especificación técnica.

---

## Las 4 capas de audio

Todo video del formato tiene estas 4 capas trabajando juntas:

| Capa | Función | Coverage |
|------|---------|----------|
| **Música** | Mood + tensión emocional | 70-90% del video |
| **Voiceover** | Narrativa + dialogue | 60-80% del video |
| **Ambient continuo** | Sense of place | 95-100% del video |
| **SFX puntuales** | Eventos específicos + impact | Eventos discretos |

**Validado:** los 13 referentes tienen sound fabric coverage ≥99% (cero dead zones). El video AUDITIVO está vivo en cada segundo.

---

## Capa 1 — MÚSICA (dirección creativa)

### Géneros musicales validados por mood

| Mood del video | Género musical sugerido |
|----------------|--------------------------|
| Uncanny puro / body horror | Dark ambient drone (bajos profundos sostenidos) |
| Cosmic horror | Orchestral drone con strings disonantes |
| Surrealismo absurdo | Industrial drone con elementos arrítmicos |
| Claustrofóbico liminal | Ambient minimalist con eco profundo |
| Synthwave / dreamcore | Synthwave 80s, hyperpop, hardstyle |
| Folclor / paranormal | Acoustic dark folk con violines |
| Journey horror (tren, coche) | Orchestral suspenso con crescendos |
| Industrial pesadilla | Drone industrial mecánico |

### BPM intent (rango, no exacto)

- **60-70 BPM lento:** drone atmosférico, máximo dread (mayoría de referentes)
- **80-95 BPM medio:** suspense build-up
- **100-130 BPM alto:** EDM/synthwave climax (ref-13 fiesta carpinchos)

El arquitecto dice "BPM lento" o "BPM alto" — ingeniero elige número exacto.

### Música evoluciona o constante?

**Música evolutiva (recomendada):**
- Empieza con drone bajo en hook
- Crescendo gradual hacia climax
- Cambio drástico en counterfactual outro

**Música constante (más simple):**
- Mismo loop todo el video con varying intensity

**Recomendación:** evolutiva. Validado en referentes top (ref-13 cambia drone→EDM, ref-03 crescendo gradual, nuestro mina-v15 cambia a folclórica en outro).

### Cambio musical en counterfactual outro

**CRÍTICO:** la música del outro DEBE contrastar con el horror.

- Horror = drone bajo dark ambient
- Outro = folk acústico cálido / piano íntimo / strings warm
- El CONTRASTE auditivo es parte de la catharsis (junto al contraste visual)

Validado en TODOS los referentes top.

### Hooks musicales (melodía reconocible)

- **Sin hook melódico** (drone puro): mayoría de referentes — la música es atmósfera
- **Con hook melódico** (motif que se repite): ref-13 EDM riff, ref-12 orchestral motif
- **Decisión creativa:** si el video es muy atmosférico, drone sin hook. Si querés viralidad de "música pegadiza", agregar hook melódico.

---

## Capa 2 — VOICEOVER (dirección creativa)

### Voz character

| Atributo | Validado en referentes | Intent en SPEC |
|----------|------------------------|----------------|
| Género | Masculino mayormente | "deep voice masculina" |
| Tono | Grave, autoritario | "registro grave intimate" |
| Pace | Medio-lento, pausado | "pace medio, no apurado" |
| Idioma | Español neutro o latino | "español neutro" |
| Procesamiento intent | Compresión + bass boost + presence | "voz 'en tu cara', clara en altavoz móvil" |

**(Ingeniero decide ElevenLabs voice ID, compresor settings, EQ específico)**

### Voiceover style — segunda persona presente histórico

El arquitecto especifica el REGISTRO. Detalle completo en `narrator-voice.md`.

Resumen:
- **Segunda persona:** "Si elegís a Bruno", "Vos te quedás", "Tu mano busca el botón"
- **Presente histórico:** "Bruno saca el medidor", "La pantalla parpadea en rojo"
- **Oraciones simples concatenadas:** sin subordinadas complejas
- **Pausas dramáticas:** entre frases clave, hay silencio (no music + no voice)

### Multi-narrator (cuando aplica)

Algunos videos usan voces diferentes para personajes:
- ref-12: narrador + Nano (agudo) + Teresa (rasposo)
- Decisión creativa, no default

Si multi-narrator:
- Cada voz tiene su processing único
- Captions deben indicar speaker (ver `captions.md`)

---

## Capa 3 — AMBIENT CONTINUO (dirección creativa)

### Por qué es la capa más importante

**Sound fabric 99-100% requirement** = ambient continuo es la "base" que NUNCA falta. Si la música baja, si el voiceover hace pausa, si los SFX terminan, el ambient sostiene la inmersión.

### Ambient por setting (catálogo)

| Setting | Ambient continuo intent |
|---------|--------------------------|
| Mina | Drone metálico bajo + goteos cada 4-5s + viento de pozos lejano + crujidos de madera |
| Hotel | Hum de fluorescentes + zumbido AC + viento de pasillos + ocasional puerta lejana |
| Bosque | Viento entre árboles + grillos + lechuza ocasional + crujido de hojas |
| Carretera | Motor del coche idling + viento contra ventana + crujido del cuero del asiento |
| Cockpit | Hum constante de motor + viento alto + radio static ocasional |
| Acuario | Burbujas en tanques + agua circulando + eco metálico de pasillos |
| Metro | Viento de túneles + electricidad zumbando + goteos + tren lejano |
| Planta industrial | Maquinaria mecánica + generadores + vapor escapando + clanks ocasionales |
| Tren | Rodamiento rítmico de ruedas en vías + crujido vagón + viento en ventana |

### Reglas del ambient

- **2 capas mínimo simultáneas** (drone base + textura intermitente)
- **Volumen bajo y constante** (NO sube ni baja con voiceover — siempre presente)
- **Eco/reverb apropiado al espacio** (cueva diferente que exterior — decisión por setting)
- **Cero gaps** (si hay momento sin música ni voz, ambient sostiene)

---

## Capa 4 — SFX PUNTUALES (dirección creativa)

### Las 4 sub-categorías de SFX

#### A) **Foley específico** (sonido de acción visible)
- Pasos sobre superficie específica (gravilla, hojas, metal)
- Encender linterna (click + zumbido eléctrico)
- Manipular objetos (papel, llave, herramienta)
- Crujidos de madera bajo peso
- Splashes de agua
- Crash de objetos

**Regla:** CADA acción visible debe tener foley. Cero acciones mudas. Validado en referentes top.

#### B) **Impactos puntuales** (eventos dramáticos)
- White flash impact (decisión tomada, cliff fork)
- Body fall thud (death moment)
- Sub-bass stab (jumpscare visual)
- Glass shatter (vidrio rompiéndose)
- Scream cut (grito interrumpido)
- Heart skip beat (transición rama mala)

**Catálogo de los 7 SFX de corte canónicos** (heredado de SFX-PIPELINE.md):
- White flash → decisión tomada
- Bad thud → entrada rama mala
- Low drone → sostener muerto/atrapado
- Rise drone → transición rama mala → buena
- Exhale → entrada rama buena (alivio)
- Silence drone → pausa entre nominales
- Warm whoosh → transición al cliffhanger

#### C) **SFX UI** (countdown + loaders + buttons)
- Tick-tick del countdown 3-2-1
- Beep del aparición de countdown
- Beep tick de carga de barra LOADING
- Pop sutil al aparecer botones A/B
- Click sutil al "presionar" botón (decisión visible)

#### D) **Music stings** (acentos musicales con visual)
- Sub-bass impact en sync con cut
- Crescendo cortado en clímax
- Drone descenso al outro

---

## Ducking (intent, no dB)

**Ducking = bajar volumen de una capa cuando otra activa.**

### Reglas de ducking

| Cuando hay... | Baja... |
|---------------|---------|
| Voiceover activo | Música baja sutilmente |
| Voiceover activo | Ambient baja levemente |
| Voiceover activo | SFX puntuales NO bajan (compiten a propósito) |
| SFX impact (white flash, thud) | Música baja brevemente |
| Climax con sub-bass | Voiceover puede pausar para dejar el impact |

El arquitecto dice "ducking activo" — ingeniero implementa con compresores y automation.

---

## Reverb por entorno (intent)

Cada entorno tiene su "espacial" único. El reverb del voiceover y SFX debe MATCHEAR el setting.

| Setting | Reverb intent |
|---------|---------------|
| Mina/Cueva | Reverb amplio, decay 2-3s, frecuencias bajas dominan |
| Hotel pasillo | Reverb medium, decay 1.5s, agudos presentes (azulejos) |
| Bosque | Reverb corto, decay 0.5s (al aire libre absorbe rápido) |
| Cockpit | Reverb mínimo (espacio cerrado pequeño) |
| Acuario | Reverb medium con flutter (echo metálico) |
| Túnel metro | Reverb amplio + agudos absorbed (hormigón) |
| Tren | Reverb corto + rolling stock ambient permanece |
| Exterior carretera | Reverb mínimo (al aire libre) |

**Ingeniero decide algoritmo de reverb. Arquitecto solo dice "amplio cueva" o "corto exterior".**

---

## Sound design coherencia checklist

### Cada acción visual tiene reforzador sonoro?

- [ ] Bruno enciende lámpara → sonido encendido lámpara
- [ ] Linterna entra a oscuridad → click + zumbido eléctrico
- [ ] Pasos en mina → foley pasos gravilla
- [ ] Manipula medidor → foley plastic + beep
- [ ] Mira a cámara → silencio cargado (no SFX, sound design)
- [ ] Sonríe → silencio dramático O sutil breath
- [ ] Activa taladro → motor + chispas + impact
- [ ] Counterfactual: come pan → foley masticación + cuchillo sobre madera

### Cada caption swap tiene SFX UI?

- [ ] Aparición de scale pop caption → sutil "pop" SFX
- [ ] Countdown tick → tick-tick audible
- [ ] Decision moment → impact sub-bass

### Cada cut tiene transición auditiva?

- [ ] Hard cut a nueva escena → ambient cambia inmediatamente
- [ ] Cut a clímax → impact sound
- [ ] Cut a outro → music shift radical (drone → folk)

---

## Output al SPEC

```yaml
audio_direction:
  music:
    genre_intent: dark_ambient_drone
    bpm_range: lento_60_70
    evolution_intent: |
      Crescendo gradual desde 0:00 (drone bajo) hasta clímax (sub-bass + impactos).
      Cambio radical en outro: drone → folk acústico cálido con guitarra y armónica.
    melodic_hook: false  # drone atmosférico sin riff
    outro_music_shift_intent: "drone → folk acoustic cozy con guitarra acústica + armónica suave"

  voiceover:
    voice_character: deep_voice_masculino_intimate
    registro: segunda_persona_presente_historico
    pace: medio_pausado
    processing_intent: "compresión + bass boost + presence — voz 'en tu cara', clara en altavoz móvil"
    multi_narrator: false

  ambient_continuous:
    setting: mina
    layers_intent:
      - drone_metalico_subterraneo_bajo_constante
      - gotas_de_agua_cada_4_5_segundos
      - viento_de_pozos_lejano
      - crujidos_madera_intermitentes
    coverage_requirement: "100% del video — cero gaps"

  sfx_strategy:
    foley_specific:
      - { action: "encender linterna", timestamp: "0:18", intent: "click + zumbido eléctrico" }
      - { action: "pasos en gravilla", timestamp: "0:24-0:28", intent: "foley pasos minería" }
      - { action: "Bruno manipula medidor", timestamp: "0:35", intent: "plastic click + beep electrónico" }
      - { action: "activación taladro", timestamp: "1:15", intent: "motor industrial + chispas" }
    impactos:
      - { event: "decisión tomada", timestamp: "0:20", intent: "white flash impact + sub-bass" }
      - { event: "explosión dinamita", timestamp: "1:10", intent: "boom orgánico + reverb largo" }
      - { event: "destrozado por taladro", timestamp: "1:15", intent: "sub-bass + grito cortado" }
    ui_sfx:
      - { element: "countdown 3-2-1", intent: "tick audible" }
      - { element: "loading bar", intent: "beep tick acumulativo" }
      - { element: "appearance de captions", intent: "pop sutil cada nueva frase" }

  ducking_intent: "activo — música baja cuando narrador habla, ambient baja levemente, SFX puntuales mantienen volumen"

  reverb_intent:
    mina_setting: "amplio cave reverb decay 2-3s, frecuencias bajas dominan"
    outro_cozy_setting: "reverb mínimo interior pequeño hogareño"

  total_sfx_events_estimated: 30  # validado de referentes top
```

---

## Anti-patterns en audio direction

❌ **Música sin evolución** — flat, aburre, score audio cae
❌ **Sin ambient continuo** — dead zones, viewer percibe "video se corta"
❌ **SFX density baja (<10 events)** — sound design pobre, gap
❌ **Sin ducking** — voiceover compite con música, viewer no entiende
❌ **Music outro = music horror** — falta catharsis auditiva
❌ **Reverb mismo en todo el video** — incoherente con setting changes
❌ **Voiceover sin compresión** — pierde en altavoz móvil
❌ **Multi-narrator sin diferenciación clara** — viewer confunde quién habla
❌ **SFX UI demasiado fuertes (overpower)** — distrae de narrativa
❌ **Música genérica AI sin curaduría** — sounds amateur, score cae

---

## Validación final de audio direction

- [ ] ¿Music genre + BPM range + evolution definidos?
- [ ] ¿Voiceover character + registro especificados?
- [ ] ¿Ambient layers definidos por setting?
- [ ] ¿SFX estimados ≥20 events (foley + impacts + UI)?
- [ ] ¿Ducking intent activo?
- [ ] ¿Reverb intent por entorno?
- [ ] ¿Outro music shift definido (contrast con horror)?
- [ ] ¿Cada caption swap tiene SFX UI intent?
- [ ] ¿Cada acción visual tiene foley intent?

Si ❌ en cualquiera → ajustar antes de SPEC.
