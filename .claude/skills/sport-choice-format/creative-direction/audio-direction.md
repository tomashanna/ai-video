# audio-direction.md — Dirección de audio sport-choice (paleta SFX fútbol)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad técnica de la paleta SFX fútbol + música deportiva** vive en `sport-choice-format/INGENIERO-PAUTA-MASTER.md §§ 2, 4`. La **mecánica de audio** (4 capas, ducking, sound fabric 99%, mastering) se HEREDA de `ai-video-production/SFX-PIPELINE.md` + `ai-video-production/AUDIO-MASTERING.md` (técnica universal) + la mecánica de audio choice de `../../choice-format-core/INGENIERO-CHOICE-CORE.md`. ⛔ **NO se hereda de `horror-choice-format/`** (firewall de capas — `NO-HORROR-GUARD.md`): ahí viven la paleta de terror, el voice_id grave de horror y las LUTs `cool_horror`. Si hay conflicto → gana la pauta.
>
> Si llegaste acá sin leer las pautas, parar y leerlas primero.

---

> El arquitecto define INTENT de audio; el ingeniero implementa con tracks, BPM, dB de ducking, LUFS. En sport-choice, la MECÁNICA de las 4 capas se hereda — lo que cambia es el CONTENIDO: paleta SFX de fútbol en vez de horror.

---

## Las 4 capas de audio (heredadas, reskineadas al estadio)

| Capa | Función | Coverage | Contenido sport-choice |
|------|---------|----------|------------------------|
| **Música** | Mood + tensión | 70-90% | Drone de tensión deportiva → celebración cálida (contraste) |
| **Voiceover** | Narrativa + dialogue | 60-80% | Relator play-by-play deportivo, español neutral (El Faraón `QpDQJR3frbDwOhTIo8nW`) |
| **Ambient continuo** | Sense of place | 95-100% | **Rugido de estadio lleno** + cánticos + eco (cero dead zones — la final NO calla) |
| **SFX puntuales** | Eventos + impact | Eventos discretos | Silbato, redes, atajada, abucheos, confeti, boot-strike |

> Heredado: sound fabric coverage ≥99% (cero dead zones). El estadio está SONORAMENTE vivo en cada segundo.

---

## ⛔ REGLA ABSOLUTA DE LA PALETA

> **NUNCA gritos de horror, drones de terror, sub-bass de jumpscare, ni susurros uncanny.** El audio de sport-choice es 100% diegético-deportivo + música de tensión deportiva. Si un SFX evoca terror, está fuera de formato.

---

## Capa 1 — MÚSICA (intent deportivo)

> Detalle de mood + prompts ElevenLabs en `INGENIERO-PAUTA-MASTER.md § 4`.

| Sección | Mood | Prompt ejemplo |
|---------|------|----------------|
| Hook + juego en tensión | Drone subharmónico de tensión deportiva (sports-thriller bed) | "low subharmonic drone, sustained deep bass tension, dark cinematic sports-thriller bed, faint orchestral swell undertone" |
| Desenlace glorioso (gol/campeón) / resolución / outro (acierto) | Celebración triunfal cálida | "triumphant stadium celebration ambience, distant euphoric crowd cheering warm, confetti rustle, victory tone, uplifting, no horror" |
| Clímax D3 (mano a mano) | Tensión rising | "rising dark cinematic strings tension, pounding low pulse building, climax buildup, no resolution" |
| Outro sostenido | Hum bajo + swell triunfal (loop cue) | "sustained low hum gradual fade blended with faint triumphant swell, cliffhanger atmospheric, loop cue" |

**Contraste musical clave:** drone de tensión (juego) → celebración cálida (gol/gloria). El error/burla va con paleta fría + abucheos (la música baja y dejan paso a la humillación social). BPM: lento/medio en tensión, alto en celebración.

---

## Capa 2 — VOICEOVER (intent)

- **Voz:** relator deportivo play-by-play vivo, español neutral — **El Faraón** (`QpDQJR3frbDwOhTIo8nW`, ver `assets/library/voices-catalog.json § sport_choice_narrator_strategy`). ⛔ NO el registro grave-omnisciente de horror (`NO-HORROR-GUARD.md` G3) — el relator mete al viewer en la jugada, no susurra desde la cripta.
- 🟦 **PICO DE GOL** (directiva creator 2026-06-04): en el gol el relator **GRITA** ("¡Gooool!" moderado 3-4 oes — TTS-safe) y el estadio explota: `crowd-goal-explosion` en banda ALTA **0.55-0.65** (banda flash/impacto HR#9, NO la banda SFX normal) + `goal-net-ripple` + celebración musical entrando. El gol es el único momento donde el audio COMPITE con el narrador a propósito.
- **Registro:** segunda persona presente ("Avanzas por la banda", "Te la deja, le pegas").
- **Idioma:** español NEUTRAL (tú/eliges) — NUNCA voseo.
- **Procesamiento:** compresión + presence (voz "en tu cara", clara en altavoz móvil) — heredado.
- **Multi-speaker:** el jugador protagonista puede tener 1-2 líneas con lip-sync ("Confía en ti. La metes." / "Te lo dije, hermano."). El foil puede tener 1 línea. Cada voz con su processing; captions indican speaker.

---

## Capa 3 — AMBIENT CONTINUO (la capa más importante)

> Sound fabric 99-100% (heredado). En sport-choice el ambient base ES el estadio.

| Capa ambient | Intent |
|--------------|--------|
| **Rugido de hinchada** (base continua) | Packed stadium crowd roar continuo — casi todo el video |
| **Cánticos lejanos de ultras** | Capa intermitente bajo el rugido |
| **Eco de estadio cerrado** | Reverb del recinto (techo cerrado del Puskás, etc.) |

Prompt ejemplo: "packed football stadium crowd roar continuous, distant chanting ultras, echoing closed-roof arena ambience, tension murmur, no music".

**Regla:** 2 capas mínimo simultáneas (rugido base + cánticos/eco), volumen bajo y constante, cero gaps. El rugido SOSTIENE la inmersión cuando la narración pausa.

---

## Capa 4 — SFX PUNTUALES (paleta fútbol)

> Catálogo completo en `INGENIERO-PAUTA-MASTER.md § 2`. Heredá la mecánica de SFX (capa dedicada track-index 60-110, foley por acción visible, ducking) de `ai-video-production/SFX-PIPELINE.md`.

#### A) Foley de juego (sonido de acción visible)
- **Golpe al balón** (boot-strike) — cada pase/remate
- **Botines sobre césped** — carrera/giro
- **Roce/forcejeo** — duelo con el rival

**Regla (heredada):** cada acción visible tiene foley. Cero jugadas mudas.

#### B) Eventos de partido (impactos dramáticos)
- **Silbato** del árbitro (inicio / falta / penal)
- **Red inflándose** (net ripple) — GOL
- **Atajada / manotazo** (goalkeeper save) — el arquero saca

#### C) GLORIA (acierto)
- **Explosión de celebración** de la hinchada (gol propio / campeón)
- **Confeti** (rustle) + cánticos eufóricos (vuelta olímpica)

#### D) ⭐ BURLA (error — el equivalente sport del "impacto de horror")
- **Abucheos / "uy" decepcionado** de la hinchada — cada error
- **Silbidos** de la hinchada — humillación sostenida

#### E) SFX UI (heredado)
- Tick del countdown 3-2-1 (film leader academy AVU)
- Beep tick del loading bar (Y52)
- Pop sutil al aparecer botones A/B

---

## ⭐ PROMPTS ElevenLabs SFX EXACTOS (paquete generación-ready)

> El arquitecto deja acá el prompt EXACTO en inglés (texto generación-ready) de cada SFX del catálogo (`INGENIERO-PAUTA-MASTER.md § 2`) + `duration_seconds` sugerida + capa destino + volumen target. El ingeniero los genera 1:1 después con `text_to_sound_effects` (NO los genera el arquitecto).
>
> **Volúmenes target** = la tabla de mix heredada (`../../choice-format-core/INGENIERO-CHOICE-CORE.md § 0` + docs/OPERATING-MANUAL.md HR#9): narración 1.0 · música 0.05-0.18 · SFX 0.20-0.35 · flash/impacto 0.55-0.65. El ambient continuo de estadio va bajo y constante (extremo bajo de la banda). Los SFX de evento NO se duckean bajo el narrador (compiten a propósito — § Ducking).
>
> **Floor técnico:** `text_to_sound_effects` no genera clips <0.5s (`caption_floor_s`, `MODEL-CAPABILITIES-MATRIX.md`). Para ticks ultra-cortos usar el AVU bundled (ya trae los ticks muxeados).

### Ambiente base (Layer 2 — continuo, cobertura 99-100%)

| SFX | Prompt ElevenLabs (EN, generación-ready) | duration_s | Capa destino | Volumen target |
|-----|------------------------------------------|-----------|--------------|----------------|
| **Rugido de hinchada** (base) | `packed football stadium crowd roar, continuous dense ambience, thousands of fans murmuring and surging, no music, no whistle, loopable bed` | 22 | Ambient continuo (Layer 2) | 0.20-0.26 (constante) |
| **Cánticos lejanos de ultras** | `distant football ultras chanting in unison, muffled rhythmic terrace chant under a crowd roar, stadium reverb, no music, loopable` | 18 | Ambient continuo (Layer 2, bajo el rugido) | 0.12-0.18 |
| **Eco de estadio cerrado** | `closed-roof arena reverb tail, large enclosed stadium room tone, faint crowd wash echoing, no music` | 12 | Ambient continuo (Layer 2, refuerzo de recinto) | 0.10-0.14 |

### Eventos de juego (Layer 1 — clip-scoped, foley por acción visible)

| SFX | Prompt ElevenLabs (EN, generación-ready) | duration_s | Capa destino | Volumen target |
|-----|------------------------------------------|-----------|--------------|----------------|
| **Silbato del árbitro** | `sharp single referee whistle blow, clean and loud, football match, no crowd` | 1.0 | Evento Layer 1 | 0.28-0.34 |
| **Golpe al balón** (boot-strike) | `solid football boot striking a ball, sharp clean kick thud, single hit, no crowd` | 0.6 | Evento Layer 1 (cada pase/remate) | 0.26-0.32 |
| **Red inflándose** (net ripple) | `football hitting the back of the net, rope mesh ripple and snap, goal net shake, single event, no crowd` | 1.2 | Evento Layer 1 (GOL) | 0.30-0.35 |
| **Atajada / manotazo** | `goalkeeper glove punch save deflecting a football, leather glove smack and ball deflection, single event, no crowd` | 0.9 | Evento Layer 1 | 0.28-0.34 |

### GLORIA (acierto — Layer 1 + accent)

| SFX | Prompt ElevenLabs (EN, generación-ready) | duration_s | Capa destino | Volumen target |
|-----|------------------------------------------|-----------|--------------|----------------|
| **Explosión de celebración** | `football stadium crowd explodes into a massive roar of celebration, sudden euphoric eruption of cheering, no music` | 4.0 | Evento Layer 1 (gol propio / campeón) | 0.45-0.60 (pico de gloria) |
| **Confeti** (rustle) | `confetti and ticker-tape rustling and fluttering down, light paper shower, celebration ambience, no music` | 5.0 | Accent (vuelta olímpica) | 0.20-0.28 |

### BURLA (error — Layer 1 + accent; el equivalente sport del impacto de horror)

| SFX | Prompt ElevenLabs (EN, generación-ready) | duration_s | Capa destino | Volumen target |
|-----|------------------------------------------|-----------|--------------|----------------|
| ⭐ **Abucheos / "uy" decepcionado** | `large football crowd groans in disappointment then boos, collective deflated 'ohh' turning to jeering, no music` | 3.5 | Evento Layer 1 (cada error) | 0.30-0.40 |
| **Silbidos de la hinchada** | `football crowd whistling in derision, sustained disapproving stadium whistles, no music` | 3.0 | Accent (humillación sostenida) | 0.24-0.32 |

### Accent de clímax (tensión)

| SFX | Prompt ElevenLabs (EN, generación-ready) | duration_s | Capa destino | Volumen target |
|-----|------------------------------------------|-----------|--------------|----------------|
| **Tensión rising clímax** | `rising dark cinematic strings tension swell, pounding low pulse building toward a climax, sports-thriller, no resolution, no horror` | 4.5 | Accent (D-clímax / mano a mano) | 0.18-0.28 (bajo el narrador) |

> ⛔ **Regla absoluta (firewall, `NO-HORROR-GUARD.md` G2):** todo prompt cierra implícita o explícitamente sin terror — `no music` donde corresponde, y JAMÁS "scream / horror / drone of dread / whisper / sub-bass jumpscare". El "rising strings tension" del clímax es **deportivo** (sports-thriller), por eso lleva "no horror" explícito. Si un prompt evoca terror → está fuera de formato.

---

## Ducking + reverb (heredado)

- **Ducking** (sidechain -6 dB): música + ambient bajan cuando el narrador habla; los SFX de evento (silbato, red, abucheo) mantienen volumen (compiten a propósito). Heredado.
- **Reverb:** matchea el recinto (estadio cerrado = reverb amplio con eco; estadio abierto = reverb medio). Heredado, ajustado al estadio.

---

## Output al SPEC (ejemplo)

```yaml
audio_direction:
  music:
    genre_intent: sports_thriller_drone
    evolution_intent: "drone de tensión deportiva en el juego → celebración triunfal cálida en gol/gloria → paleta fría + abucheos en error"
    outro_music_shift_intent: "drone tensión → triunfal cálido (loop cue)"
  voiceover:
    voice_character: narrador_grave_deportivo
    registro: segunda_persona_presente
    idioma: espanol_neutral
    processing_intent: "compresión + presence — clara en altavoz móvil"
    multi_speaker: true  # protagonista habla 1-2 líneas lip-sync
  ambient_continuous:
    setting: estadio_lleno
    layers_intent: [rugido_hinchada_continuo, canticos_ultras_lejanos, eco_estadio_cerrado]
    coverage_requirement: "99-100% — la final no calla nunca"
  sfx_strategy:
    foley_juego: [boot_strike_cada_pase, botines_cesped, forcejeo_duelo]
    eventos_partido: [silbato_arbitro, red_inflandose_gol, atajada_manotazo]
    gloria: [explosion_celebracion, confeti_rustle]
    burla: [abucheos_uy_decepcion, silbidos_hinchada]   # ⭐ el equivalente sport del impacto
    ui_sfx: [countdown_tick_film_leader, loading_beep_tick, botones_pop]
  ducking_intent: "activo (sidechain) — música+ambient bajan en narración; eventos de partido mantienen volumen"
  prohibition: "NUNCA gritos de horror, drones de terror, sub-bass jumpscare, susurros uncanny"
```

---

## Anti-patterns en audio direction (sport)

❌ **Cualquier SFX de horror** (grito, drone de terror, jumpscare) → fuera de formato.
❌ **Sin rugido de estadio continuo** → dead zones, el partido se siente vacío.
❌ **Error sin abucheos/burla** → la humillación deportiva no aterriza.
❌ **Gol sin explosión de celebración** → la gloria no aterriza.
❌ **Música del outro = música de tensión** → falta el contraste triunfal.
❌ **Sin ducking** → la narración compite con el rugido, el viewer no entiende la jugada.
❌ **Voseo** en el voiceover → audiencia international, usar español neutral.

---

## Validación final de audio direction

- [ ] ¿Música = tensión deportiva → celebración cálida (contraste)?
- [ ] ¿Rugido de estadio continuo (99-100%, cero gaps)?
- [ ] ¿SFX de evento (silbato, red, atajada) por cada acción?
- [ ] ¿Abucheos/burla en cada error + celebración/confeti en gloria?
- [ ] ¿Ducking activo?
- [ ] ¿Voiceover español neutral, grave, comprimido?
- [ ] ¿CERO SFX de horror?
- [ ] ¿Cada acción visible tiene foley?
- [ ] ¿Cada caption swap / UI tiene SFX UI?
