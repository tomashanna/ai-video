# LIBRARY.md — Biblioteca central de assets reutilizables

> Todo SFX, música o voz que se haya generado en cualquier proyecto y valga la pena reutilizar vive acá. Antes de generar un asset nuevo, **buscá en esta library primero**. Cada generación que evitamos = créditos ahorrados + tiempo de producción reducido.

**Última actualización**: 2026-05-10
**Estado**: 53 SFX + 5 música + 4 voice IDs catalogados

---

## Estructura

```
library/
├── LIBRARY.md                    ← Este doc (catálogo maestro)
├── sfx-catalog.json              ← Machine-readable de SFX
├── voices-catalog.json           ← Machine-readable de voces
├── sfx/                          ← SFX organizados por categoría
│   ├── cuts/                     ← 7 cortes NARRATIVE-LED-EDITING (universales)
│   ├── impacts/                  ← Flash, stab, shatter
│   ├── drones/                   ← Tension, build, cave
│   ├── ambients/                 ← Forest, mine, dawn (loops)
│   ├── footsteps/                ← Leaves, gravel, soil, mine
│   ├── voices-sfx/               ← Whispers, breaths, exhales, laughter
│   ├── body-impacts/             ← Falls, grips, splinters
│   ├── warm-cliffhanger/         ← Fire, strum, cup, birds, pad
│   ├── motion/                   ← Accelerate, vanish, wakeup
│   ├── horror-specific/          ← Howls, sonidos solo para horror
│   └── countdown/                ← Tick
├── voices/                       ← Voice IDs ElevenLabs (referencias)
│   └── samples/                  ← (Opcional: samples de audio por voz)
├── music/                        ← Música procesada lista para usar
└── samples/                      ← Samples genéricos (placeholder)
```

---

## Filosofía

1. **Antes de generar, buscar acá.** Cada asset es ~200 créditos ElevenLabs. Reutilizar es gratis.
2. **Nombres canónicos**, no prefijos de proyecto. `flash-sharp.mp3`, no `h2-flash-impact.mp3`.
3. **Categorías ortogonales**. Un asset vive en UNA categoría, no múltiples.
4. **Copies, no symlinks**. Independencia: si borro un proyecto, la library sigue.
5. **Solo lo reutilizable**. SFX muy específicos de un proyecto (ej: una línea de diálogo) NO van acá.

---

## Cómo usar la library en un proyecto nuevo

### Workflow recomendado

```
1. Leer este doc (LIBRARY.md) ANTES de pasar a sfx-spec.json
2. Por cada SFX que necesita tu video:
   a. Buscar en la categoría correspondiente
   b. Si existe: copiar a tu proyecto y wire al index.html
   c. Si no existe: agregarlo a sfx-spec.json para generar
3. Después de generar nuevos SFX:
   a. Si alguno es reutilizable → copiarlo de vuelta a library/
   b. Actualizar este doc + sfx-catalog.json
```

### Comando para copiar SFX a tu proyecto

```bash
# Single
cp "<repo-root>/library/sfx/cuts/cut-white-flash.mp3" \
   "<proyecto>/assets/sfx/cut-white-flash.mp3"

# Categoría completa (ej: todos los cuts)
cp "<repo-root>/library/sfx/cuts/"*.mp3 \
   "<proyecto>/assets/sfx/cuts/"
```

---

## CATÁLOGO — SFX por categoría

### 🎬 Cuts (NARRATIVE-LED-EDITING — sistema universal)

> Los 7 cortes universales del sistema de edición narrativa. Aplican a CUALQUIER formato (horror, documental, educacional, ads). Ver `ai-video-production/NARRATIVE-LED-EDITING.md`.

| Archivo | Duración | Uso | Volume rec. |
|---|---|---|---|
| `cuts/cut-white-flash.mp3` | 0.5s | Tipo 1: cliff/branch fork. Cuando se TOMA la elección. | 0.55-0.65 |
| `cuts/cut-bad-thud.mp3` | 0.7s | Tipo 2: entrada a rama mala. Game-over alternativo. | 0.50-0.60 |
| `cuts/cut-drone-low.mp3` | 1.0s | Tipo 3: sostener momento muerto. "Estás muerto/atrapado". | 0.35-0.45 |
| `cuts/cut-rise-drone.mp3` | 0.6s | Tipo 4: transición rama mala → buena. "Y si no..." | 0.40-0.55 |
| `cuts/cut-exhale.mp3` | 0.5s | Tipo 5: entrada a rama buena. Alivio. "Sobreviviste". | 0.35-0.45 |
| `cuts/cut-silence-drone.mp3` | 0.3s | Tipo 6: pausa entre nominales narrador. "El suelo." | 0.10-0.20 |
| `cuts/cut-warm-whoosh.mp3` | 0.5s | Tipo 7: transición al cliffhanger cálido. | 0.40-0.50 |

**Aprendizaje**: la diferencia entre 8.5 y 9.5 en Gemini es usar los 7 cortes diferenciados, NO solo white flash para todo.

---

### 💥 Impacts (universales)

| Archivo | Duración | Uso |
|---|---|---|
| `impacts/stab-subbass.mp3` | 0.5s | Hit corto sub-bass — reveal de nombre, dramático |
| `impacts/flash-sharp.mp3` | 0.7s | White flash con crack agudo + sub-bass tail |
| `impacts/flash-soft.mp3` | 0.5s | Variante suave del flash (sin crack agudo) |
| `impacts/flash-warm.mp3` | 0.7s | Flash para transición cálida (sin horror) |
| `impacts/glass-shatter-soft.mp3` | 0.8s | Cristal rompiéndose, sutil |

---

### 🌫️ Drones (tension/build)

| Archivo | Duración | Uso |
|---|---|---|
| `drones/loading-drone-buildup.mp3` | 2.5s | Drone que sube durante loading bar — 2.5s exacto |
| `drones/tension-rise-3s.mp3` | 3s | Build de tensión, termina en cliff |
| `drones/cave-drone-deep.mp3` | varia | Drone deep para escenarios subterráneos/cueva |

---

### 🌬️ Ambients (loops largos — capa de fondo)

> Para coberturas >22s, usar `ffmpeg -stream_loop -1` para expandir. Mix volume típico: 0.10-0.18.

| Archivo | Duración source | Uso |
|---|---|---|
| `ambients/forest-wind-loop-22s.mp3` | 22s | Bosque nocturno, viento, árboles. Loopable. |
| `ambients/dawn-warmth-loop-12s.mp3` | 12s | Amanecer cálido, pájaros lejanos. Loopable. |
| `ambients/mine-industrial-loop.mp3` | varia | Mina/industrial subterráneo. Loopable. |

---

### 👣 Footsteps

| Archivo | Duración | Uso |
|---|---|---|
| `footsteps/leaves-loop-4s.mp3` | 4s | Caminando sobre hojas secas. Loopable. |
| `footsteps/leaves-2nd-set-creepy.mp3` | 5s | Segundo set de pasos detrás — horror |
| `footsteps/gravel-6s.mp3` | 6s | Transición leaves → grava. Salida del bosque. |
| `footsteps/mine-loop-4s.mp3` | 4s | Pasos en suelo de mina. Loopable. |
| `footsteps/soil.mp3` | varia | Pasos en tierra suelta |

---

### 🗣️ Voices-SFX (whispers, breaths, exhales)

> Sonidos vocales NO narración. Atmósfera + tensión + alivio.

| Archivo | Duración | Uso |
|---|---|---|
| `voices-sfx/whisper-creepy-old-man.mp3` | 2s | Susurro horror de viejo, ininteligible |
| `voices-sfx/whisper-warn-male.mp3` | varia | Susurro masculino de advertencia |
| `voices-sfx/breath-behind-raspy.mp3` | 1.5s | Respiración detrás del oído, raspy |
| `voices-sfx/exhale-release-warm.mp3` | 3s | Exhalación larga de alivio + warm pad |
| `voices-sfx/exhale-relief.mp3` | varia | Exhalación corta de alivio |
| `voices-sfx/gasp-collapse.mp3` | varia | Gasp de colapso/asfixia |
| `voices-sfx/laughter-distant-faint.mp3` | 2s | Risas lejanas, casi subliminal |
| `voices-sfx/laughter-warm-group.mp3` | 3s | Risas cálidas grupo cliffhanger |

---

### 💀 Body-impacts (horror)

| Archivo | Duración | Uso |
|---|---|---|
| `body-impacts/body-fall-leaves.mp3` | 1.5s | Cuerpo cayendo sobre hojas/tierra |
| `body-impacts/cold-grip.mp3` | 1s | Mano fría agarrando hombro |
| `body-impacts/fall-pit.mp3` | varia | Caída a pozo/mina |
| `body-impacts/wood-splinter.mp3` | varia | Madera astillándose (estructura colapsando) |

---

### 🔥 Warm-cliffhanger (sonidos de cierre cálido)

> Para H6 / cliffhanger / ramas "lo que hubieras tenido". Música mayor + sonidos cotidianos cálidos.

| Archivo | Duración | Uso |
|---|---|---|
| `warm-cliffhanger/fire-distant-warm.mp3` | 6s | Fuego lejano filtrado, cálido |
| `warm-cliffhanger/fire-crackle-loop-8s.mp3` | 8s | Crepitar de fogata íntimo. Loopable. |
| `warm-cliffhanger/acoustic-strum-warm.mp3` | 2s | Strum único de guitarra acústica cálida |
| `warm-cliffhanger/cup-toast-clink.mp3` | 0.5s | Brindis de tazas metálicas |
| `warm-cliffhanger/cup-set-soft.mp3` | varia | Taza apoyándose suavemente |
| `warm-cliffhanger/dawn-birds-chorus.mp3` | 4s | Coro de pájaros amanecer |
| `warm-cliffhanger/first-bird-single.mp3` | 1.5s | Primer pájaro del amanecer, una nota |
| `warm-cliffhanger/bird-distant-dawn.mp3` | varia | Pájaro lejano alternativa |
| `warm-cliffhanger/warm-pad-resolution.mp3` | 2s | Acorde mayor resolutivo, hopeful |
| `warm-cliffhanger/paper-rustle.mp3` | varia | Papel/libro |

---

### 🏃 Motion (movimiento, transiciones)

| Archivo | Duración | Uso |
|---|---|---|
| `motion/footsteps-accelerate.mp3` | 3s | Pasos acelerando de lento a urgente |
| `motion/footstep-return.mp3` | 1s | Pisada de vuelta al camino |
| `motion/footstep-relief.mp3` | varia | Pisada después de salvarse |
| `motion/whoosh-presence-vanish.mp3` | 2s | Whoosh de presencia que desaparece |
| `motion/wakeup-disorient-tinnitus.mp3` | 2s | Despertar disoriented + tinnitus |
| `motion/knock-pillar.mp3` | varia | Golpe rítmico en pilar (4 veces) |
| `motion/pickaxe-distant.mp3` | varia | Pico lejano cavando |

---

### 👻 Horror-specific

| Archivo | Duración | Uso |
|---|---|---|
| `horror-specific/howl-distant-low.mp3` | 3s | Aullido lejano horror, ambient |

---

### ⏱️ Countdown

| Archivo | Duración | Uso |
|---|---|---|
| `countdown/tick.mp3` | 0.1s | Tick de countdown 3-2-1. Reutilizable triple. |

---

## CATÁLOGO — Música

Mix volume recomendado: 0.05-0.18 para horror ambient, 0.13-0.18 para dawn cálida.

| Archivo | Duración | Uso |
|---|---|---|
| `music/horror-tension.mp3` | ~63s | Música de tensión horror, ambient. Sin melodía clara. |
| `music/horror-tension-loop-83s.mp3` | 83s | Loop pre-expandido de horror-tension. |
| `music/dawn-cliffhanger.mp3` | ~6s | Música cálida cliffhanger. Sin narración encima puede subir vol. |
| `music/dawn-cliffhanger-loop-23s.mp3` | 23s | Loop pre-expandido de dawn. |
| `music/party-warm.mp3` | varia | Música de fiesta cálida (rama "buena hipotética" alegre) |

**Cómo elegir música**:
- Horror puro → `horror-tension.mp3`
- Cliffhanger cálido al final → `dawn-cliffhanger.mp3`
- Cliffhanger con celebración (gente, fogata, fiesta) → `party-warm.mp3`

---

## CATÁLOGO — Voice IDs ElevenLabs

> Voces TEXT-TO-SPEECH (no SFX). Cada voice ID se referencia por string en `tts.py -v <ID>`. Después del TTS aplicar atempo 2x si la voz es lenta.

### Voz primaria (default para nuevos proyectos)

| Voice ID | Nombre / etiqueta | Características | Status |
|---|---|---|---|
| `Tj9l48J9AJbry5yCP5eW` | **Narrador horror primario** | Tono grave, susurro, lento por naturaleza | ✅ Default canónico |

**Reglas obligatorias para esta voz**:
- Aplicar `atempo=2.0` con ffmpeg después de generar
- "2x es muy rápido" NO aplica acá — esta voz es lenta y 2x suena natural
- Sample: `library/voices/samples/Tj9l48J9AJbry5yCP5eW-sample.mp3` (pendiente generar)

---

### Voces secundarias (A/B testing o casos específicos)

| Voice ID | Etiqueta | Tested in | Notas |
|---|---|---|---|
| `2gPFXx8pN3Avh27Dw5Ma` | **Voz V2 (locked para bosque)** | bosque-abandonado v2-final | Project-specific override. NO usar como default. |
| `1BfrkuYXmEwp8AWqSLWk` | Voz reserva sin testear | — | Guardada para futuras pruebas |

---

### Voces a evitar

| Voice ID | Por qué no usar |
|---|---|
| `0Wj6ADitNyDvXgT6W65p` | Era el default INCORRECTO en tts.py. Voz más rápida, no horror. |

---

### Workflow para usar voces

```bash
# 1. Generar TTS raw
.venv/bin/python scripts/tts.py \
  -t "Texto a narrar" \
  -v Tj9l48J9AJbry5yCP5eW \
  -o assets/narr-raw.mp3

# 2. Aplicar atempo 2x
ffmpeg -y -i assets/narr-raw.mp3 -filter:a "atempo=2.0" assets/narr-2x.mp3

# 3. Medir duración
ffprobe -v quiet -show_entries format=duration -of csv=p=0 assets/narr-2x.mp3
```

---

## Reglas de uso de la library

1. **Buscar antes de generar.** Siempre. Aunque pienses que vas a generar algo nuevo, chequeá esta lista primero.
2. **No mover, copiar.** `cp` de la library a tu proyecto. La library queda intacta.
3. **Si generás algo reutilizable, agregalo de vuelta.** Después de un proyecto, evaluar:
   - ¿Este SFX podría servir en otro formato?
   - Si sí → copiar a library/ + actualizar este doc + actualizar sfx-catalog.json
4. **No agregar todo.** Diálogos específicos (`h1-yerald-dialog`), narraciones, voces de personajes → NO van.
5. **Categorías son ortogonales.** Un SFX vive en UNA. Si dudás entre dos, elegí la más específica.

---

## Cuándo NO usar la library

- **Voces de personajes específicos** (Yerald, Hugo, etc.) — son del proyecto.
- **Narraciones (TTS output)** — son del proyecto.
- **SFX muy específicos** que no aplicarían a otro formato (ej: "h1-yerald-asks-pick-me").
- **Variantes -full, -loop expandidos** de loops generados con stream_loop — se regeneran fácil con el comando.

---

## Próximas acciones sugeridas

1. **Generar voice samples** — un MP3 corto por cada voice ID con la misma frase de ejemplo para comparar rápido sin abrir EL UI.
2. **Migrar SFX nuevos** después de cada proyecto que se publique.
3. **Crear sub-categoría `educational/` o `documental/`** cuando aparezca un template nuevo no-horror que requiera SFX distintos.

---

## Última actualización

2026-05-10. Inicial. 53 SFX deduplicados de bosque/elige/mina + 5 música + 4 voice IDs catalogados.
