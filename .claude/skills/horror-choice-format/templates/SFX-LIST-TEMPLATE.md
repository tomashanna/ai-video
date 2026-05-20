# SFX-LIST.md — [NOMBRE_PROYECTO]

Lista de efectos de sonido para la pasada de animación. Motor único: **ElevenLabs Sound Effects API** (vía `scripts/sfx.py`). Para ambient loops >22s usar `loop:true` + expansión ffmpeg `stream_loop` (ver `PRODUCTION-PIPELINE.md` § 12.5). Freesound queda como fallback opcional avanzado solo si un asset puntual sale uncanny.

**Convención de naming:** `assets/sfx/<scene>-<descriptor>.mp3`
**Volumen objetivo (mezcla):** todos los SFX a `data-volume="0.25"` excepto white-flash impacts a `0.6`. Narración siempre `1.0`. Ver `PRODUCTION-PIPELINE.md` § 12 para tabla completa.

---

## Capa de fondo (continua, todo el video) — ElevenLabs con loop expansion

| Asset | Cobertura | Prompt EL | Duración seed | Vol |
|---|---|---|---|---|
| `sfx/ambient-forest-wind.mp3` | 0.0–72.0s | "continuous abandoned forest night wind, dead trees creaking, cold atmospheric, no animals, no rain, perfectly looping" | 22s loop → expandir a 75s con ffmpeg `stream_loop 3` | 0.12 |
| `sfx/ambient-dawn-warmth.mp3` | 72.0–82.0s | "warm dawn forest ambience, soft distant morning birds, gentle wind, cozy peaceful, perfectly looping" | 12s loop directo | 0.18 |

---

## H1 — Presentación (0.0–10.0s)

| t | Asset | Fuente | Prompt | Dur |
|---|---|---|---|---|
| 0.0 | `sfx/h1-distant-howl.mp3` | ElevenLabs | "very distant low animalistic howl far away through fog, almost imperceptible, single event, no music, isolated horror atmosphere" | 3s |
| 1.0 | `sfx/h1-name-stab.mp3` | ElevenLabs | "low frequency cinematic sub-bass stab impact for title reveal, single short hit, dry no reverb tail" | 0.5s |

---

## H2 — Countdown + loading (10.0–22.5s)

| t | Asset | Fuente | Prompt | Dur |
|---|---|---|---|---|
| 11.0 | *(ya existe)* `tick.mp3` | — | — | 0.1s |
| 14.0 | `sfx/h2-loading-drone.mp3` | ElevenLabs | "low rising tension drone slow build sub-bass cinematic horror buildup, intensifies smoothly" | 2.5s |
| 19.5 | `sfx/h2-flash-impact.mp3` | ElevenLabs | "short cinematic white-flash impact, sharp crack with deep sub-bass tail" | 0.5s |
| 19.5 | `sfx/h2-glass-shatter-soft.mp3` | ElevenLabs | "soft glass tinkle shatter, subtle, single event, short decay" | 0.8s |

---

## H3 — 1er dilema (22.5–46.0s)

### Subcapa de pasos (loop)
| Asset | Cobertura | Prompt | Dur |
|---|---|---|---|
| `sfx/h3-footsteps-leaves-loop.mp3` | 19.0–35.5s (loop) | "slow heavy footsteps on dry dead crunchy leaves, single person, steady pace, dry no reverb, perfectly looping" | 4s |

### Eventos puntuales
| t | Asset | Fuente | Prompt | Dur |
|---|---|---|---|---|
| 25.7 | `sfx/h3-whisper.mp3` | ElevenLabs | "creepy hushed unintelligible whisper of an old man very close to the ear, breathy, single short phrase" | 2s |
| 28.5 | `sfx/h3-second-footsteps.mp3` | ElevenLabs | "second set of footsteps on dry leaves slightly out of sync with the first, almost imperceptible, behind listener" | 5s |
| 31.5 | `sfx/h3-breath-behind.mp3` | ElevenLabs | "single low exhaled breath very close behind ear, raspy, single event, no words, horror" | 1.5s |
| 35.7 | `sfx/h3-flash-impact.mp3` | ElevenLabs | "white flash transition impact, sharp crack plus low sub bass boom, dry" | 0.7s |
| 36.0 | `sfx/h3-cold-grip.mp3` | ElevenLabs | "sudden grip of a cold dead hand on shoulder, fabric and skin contact, quiet wet thud" | 1s |
| 36.5 | `sfx/h3-body-fall.mp3` | ElevenLabs | "human body collapsing onto dead leaves and earth, dull thud no scream, single event" | 1.5s |
| 43.0 | `sfx/h3-release-exhale.mp3` | ElevenLabs | "long slow released exhale, calm relief, ambient warm low sub" | 3s |

---

## H4 — 2do dilema (46.0–64.0s)

[Patrón análogo a H3 — adaptar según escena específica. Ver bosque-abandonado/SFX-LIST.md como referencia.]

---

## H5 — Salida (64.0–72.0s)

| t | Asset | Fuente | Prompt | Dur |
|---|---|---|---|---|
| 64.0 | `sfx/h5-footsteps-gravel.mp3` | ElevenLabs | "footsteps transitioning from leaves to gravel/dirt road, quiet morning, single person, 6 seconds" | 6s |
| 65.5 | `sfx/h5-disappear.mp3` | ElevenLabs | "soft whoosh of leaves rustling and a presence vanishing, no impact, ambient release" | 2s |
| 68.5 | `sfx/h5-first-bird.mp3` | ElevenLabs | "single distant blackbird call, one clear note, dawn morning forest, lone bird, no other animals, no music" | 1.5s |

---

## H6 — Cliffhanger (72.0–82.0s)

| t | Asset | Fuente | Prompt | Dur |
|---|---|---|---|---|
| 72.0 | `sfx/h6-flash-warm.mp3` | ElevenLabs | "soft warm whoosh transition without any horror, gentle wind change" | 0.7s |
| 72.0 | `sfx/h6-fire-crackle-loop.mp3` | ElevenLabs | "warm intimate campfire crackling close-up, dry wood embers popping, cozy ambient" | 8s `loop:true` |
| 73.5 | `sfx/h6-laughter.mp3` | ElevenLabs | "small group of three or four people laughing softly around campfire, warm intimate genuine, slight distance, no music, no words" | 3s |
| 75.0 | `sfx/h6-acoustic-strum.mp3` | ElevenLabs | "single warm acoustic guitar chord strum, open major chord, nylon strings, intimate close-up, single event no progression, no other instruments" | 2s |
| 76.5 | `sfx/h6-cup-toast.mp3` | ElevenLabs | "two metal tin cups clinking together once, friendly toast sound, dry" | 0.5s |
| 78.0 | `sfx/h6-dawn-birds.mp3` | ElevenLabs | "warm dawn morning birds chorus, multiple species singing, countryside spring atmosphere, no traffic, peaceful" | 4s |
| 80.5 | `sfx/h6-warm-pad.mp3` | ElevenLabs | "warm major chord low pad resolution feel-good, no rhythm, hopeful" | 2s |

---

## Resumen de generación

| Fuente | Cantidad | Costo aprox |
|---|---|---|
| ElevenLabs SFX | ~30-35 archivos (incluyendo ambient loops + voces + instrumentos) | ~$5-10 (~15-20k créditos) |
| Freesound | 0 (fallback opcional si EL falla puntualmente) | – |

---

## Workflow

1. Editar este archivo con los timestamps reales del proyecto (no estimados).
2. Convertir a `sfx-spec.json` (formato batch — ver `templates/sfx-spec-TEMPLATE.json`).
3. Ejecutar: `python scripts/sfx.py --spec sfx-spec.json`
4. Verificar duraciones con ffprobe.
5. Para ambient loops >22s: expandir con ffmpeg `stream_loop` (ver PIPELINE § 12.5).
6. Wire en `index.html` con `data-track-index` 60-110 reservado para SFX.
7. **Fallback opcional**: si un SFX EL específico salió notoriamente uncanny, regenerar con prompt distinto o copiar `templates/FREESOUND-QUERIES-TEMPLATE.md` y descargar ese asset puntual.

---

## Reglas de mezcla (de PRODUCTION-PIPELINE § 12)

1. **Narración = 1.0** siempre. Nada compite con la voz.
2. **Música ambient = 0.05–0.18** (background).
3. **SFX eventos puntuales = 0.20–0.35**.
4. **Flash impacts = 0.55–0.65**. Tienen que pegar.
5. **Ambient continuo (wind/fire loop) = 0.10–0.18**.
6. **Si dos SFX se solapan**: bajar el menos importante 0.05–0.10.
