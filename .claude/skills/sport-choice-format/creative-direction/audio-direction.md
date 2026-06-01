# audio-direction.md — Dirección de audio sport-choice (paleta SFX fútbol)

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad técnica de la paleta SFX fútbol + música deportiva** vive en `sport-choice-format/INGENIERO-PAUTA-MASTER.md §§ 2, 4`. La **mecánica de audio** (4 capas, ducking, sound fabric 99%, mastering) se HEREDA de `horror-choice-format/creative-direction/audio-direction.md` + `ai-video-production/SFX-PIPELINE.md` + `AUDIO-MASTERING.md`. Si hay conflicto → gana la pauta.
>
> Si llegaste acá sin leer las pautas, parar y leerlas primero.

---

> El arquitecto define INTENT de audio; el ingeniero implementa con tracks, BPM, dB de ducking, LUFS. En sport-choice, la MECÁNICA de las 4 capas se hereda — lo que cambia es el CONTENIDO: paleta SFX de fútbol en vez de horror.

---

## Las 4 capas de audio (heredadas, reskineadas al estadio)

| Capa | Función | Coverage | Contenido sport-choice |
|------|---------|----------|------------------------|
| **Música** | Mood + tensión | 70-90% | Drone de tensión deportiva → celebración cálida (contraste) |
| **Voiceover** | Narrativa + dialogue | 60-80% | Narrador grave deportivo, español neutral (David C2) |
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
| Rama corta gloriosa / resolución / outro (acierto) | Celebración triunfal cálida | "triumphant stadium celebration ambience, distant euphoric crowd cheering warm, confetti rustle, victory tone, uplifting, no horror" |
| Clímax D3 (mano a mano) | Tensión rising | "rising dark cinematic strings tension, pounding low pulse building, climax buildup, no resolution" |
| Outro sostenido | Hum bajo + swell triunfal (loop cue) | "sustained low hum gradual fade blended with faint triumphant swell, cliffhanger atmospheric, loop cue" |

**Contraste musical clave:** drone de tensión (juego) → celebración cálida (gol/gloria). El error/burla va con paleta fría + abucheos (la música baja y dejan paso a la humillación social). BPM: lento/medio en tensión, alto en celebración.

---

## Capa 2 — VOICEOVER (intent)

- **Voz:** narrador grave deportivo, autoritario pero claro (mismo registro que horror, mismo voice_id David C2).
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
- **Pings de redes positivos** (opcional, si se muestra el furor a favor)

#### D) ⭐ BURLA (error — el equivalente sport del "impacto de horror")
- **Abucheos / "uy" decepcionado** de la hinchada — cada error
- **Pings de redes / notificaciones** (meme alert) — "eres la burla"
- **Silbidos** de la hinchada — humillación sostenida

#### E) SFX UI (heredado)
- Tick del countdown 3-2-1 (film leader academy AVU)
- Beep tick del loading bar (Y52)
- Pop sutil al aparecer botones A/B

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
    gloria: [explosion_celebracion, confeti_rustle, pings_redes_positivos]
    burla: [abucheos_uy_decepcion, pings_redes_meme, silbidos_hinchada]   # ⭐ el equivalente sport del impacto
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
