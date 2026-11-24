# assets/transitions/ — Carpeta GLOBAL de transiciones (autoridad única)

> **Single source of truth de transiciones del sistema.** Carpeta root global (movida desde `ai-video-production/templates/effects-library/` + `<format>-format/effects-library/` el 2026-06-05 por directiva del creator). Cada transición es un JSON self-contained con `ffmpeg_recipe` + `audio_recipe` + `xfade_transition` + `xfade_fidelity` + use-cases + HyperFrames alternative + `canonical_validation_status`.
>
> **`catalog.json` = el índice consultable**: mapea cada transición → formatos donde sirve (`formats`) + capa + cuándo usarla. El sistema (scripts + agentes) lee el catálogo primero; el recipe después.

---

## Estructura

```
assets/transitions/                              # GLOBAL root
├── catalog.json                          # ⭐ índice transición → formato (consultar PRIMERO)
├── README.md                             # este archivo (autoridad)
├── CANONICAL-VALIDATION-REPORT-2026-05-22.md   # validation record F1 de las recipes
├── universal/                            # disponible para CUALQUIER formato
│   ├── transitions/*.json                # 11 primitivas (7 originales + 4 user-directed 2026-06-05: camera-shake / pan-left whip-blur / brightness-flash / zoom-in)
│   └── audio-stings/*.mp3                # whoosh-warm / drone-tension / flash-sharp
├── horror-choice/                        # SOLO formato horror-choice
│   ├── transitions/*.json                # film-burn / old_screen_glitch / projector-cue / static-noise
│   └── audio-stings/*.mp3                # projector-cue / drone-tension
└── sport-choice/                         # SOLO formato sport-choice (bootstrapped vacío 2026-06-05)
    ├── assets/transitions/                      # candidatos futuros: replay-wipe, stadium-flash, scoreboard-cut
    └── audio-stings/
```

Compat: los paths viejos (`ai-video-production/templates/effects-library/{transitions,audio-stings}` + `<format>-format/effects-library/{transitions,audio-stings}`) son **symlinks** hacia acá — los scripts ya copiados en proyectos bootstrapeados siguen resolviendo.

---

## ⭐ Principio canónico: "Disponibilidad ≠ Uso"

| Capa | Path | Disponible para |
|------|------|-----------------|
| **universal** | `assets/transitions/universal/transitions/` | CUALQUIER formato/video |
| **per-format** | `transitions/<format>/transitions/` | Solo cuando `--format <ese-formato>` |
| **SPEC (Capa C)** | `creative-specs/<id>.yaml` → `shot_list[].transition_in/out` | Este video — ES quien decide |

- El catálogo es **disponibilidad**, NO prescripción. Ningún formato/video está obligado a usar una transición por existir.
- Resolución per formato: ver `catalog.json § format_resolution` (per-format tiene precedencia sobre universal si un id existe en ambas).
- Formatos nuevos: (1) referencian universal directamente, (2) agregan las suyas en `transitions/<format>/`, (3) NO duplican primitivas.

---

## Decision matrix — qué transición usar

| Situación | Use | Duración | Por qué |
|---|---|---|---|
| Cambio de escena (default workhorse) | `hard-cut-with-whoosh` | 0.0s + sting 0.48s | Preserva cuts/min 2-7 (validated 8/8) |
| Conectar dos beats dentro de la misma escena | `cross-fade-0.5s` | 0.5s | Blend invisible |
| Salto temporal / memory dissolve | `cross-fade-1.0s` | 1.0s | Lee como "después" (solo con intent) |
| Coma narrativa / respiro | `black-screen-0.3s` | 0.3s | Inserto negro breve |
| Climax peak / plot twist reveal | `light-flash-impact` | 0.2s | White flash + SFX (máx 1-2x/reel) |
| Outro antes del cliffhanger card | `fade-to-black-1.0s` | 1.0s | Cierre universal |
| Glitch de realidad (digital) | `glitch-transition` | 0.3s | xfade=hlslice |
| ⭐ Impacto físico (golpe/caída/tackle/jump-scare) | `camera-shake` | 0.25s | Shake decayente ACOPLADO al sting (movimiento = duración del sonido; máx 2-3x/reel) |
| ⭐ Continuidad espacial (personaje/lugar adyacente) | `pan-left-0.2s` | 0.2s | Whip pan + motion blur direccional — dyad A→B, pase→receptor |
| ⭐ Revelación / despertar / cambio de realidad | `brightness-flash` | 0.3–0.5s | Bloom sin sting (counterfactual, gloria) |
| ⭐ Punch de atención (wide→detalle/decisión) | `zoom-in-0.3s` | 0.3s | Forward energy hacia lo que importa |

**Per-format (horror-choice)**: `static-noise-transition` (VHS analog) · `projector-cue-cinema` (reel-change) · `film-burn-transition` (cinema bloom) · `old_screen_glitch_error` (CRT error).

---

## `xfade_transition` + `xfade_fidelity` fields

Cada recipe declara explícitamente (no inferencia):
- `xfade_transition`: el valor `xfade=transition=<name>` ffmpeg legal, o `hardcut` (concat puro).
- `xfade_fidelity`: `literal` (el recipe ES un xfade de ese tipo) o `approximate` (otro mecanismo — concat-insert/overlay/jitter-crop — que el chained-xfade aproxima).
- `native_mechanism_note`: descripción del mecanismo real cuando `approximate`.

`ai-video apply-effects-between-clips` lee estos fields; recipe `approximate` en producción real emite WARNING.

---

## Usage

- Assembly post-concat: `ai-video apply-effects-between-clips --effects-dir <dirs>` (chained-xfade desde clips atómicos). `ai-video build-video-hybrid` resuelve los dirs automáticamente vía `assets/transitions/catalog.json` (walk-up desde el script).
- Cada recipe ships `ffmpeg_recipe` (placeholders `{clip_a}`/`{clip_b}`/`{output}`) + `hyperframes_alternative` (GSAP equivalente).
- Previews locales: `assets/transitions/_previews/` (gitignored, regenerables).

## Audio stings (universal)

| Sting | Duración | Used by (BUNDLED — el sting es parte de la transición) |
|---|---|---|
| `whoosh-warm.mp3` | 0.48s | hard-cut-with-whoosh |
| `drone-tension.mp3` | 3.0s | glitch-transition |
| `flash-sharp.mp3` | ~0.15s | light-flash-impact |
| ⭐ `whoosh-badminton-shake.mp3` | 0.63s | camera-shake (peak @ 120ms → alineado al corte, vol 0.55) |
| ⭐ `whoosh-badminton-pan.mp3` | 0.70s | pan-left-0.2s (peak @ 168ms → centro del whip, vol 0.35) |
| ⭐ `swoosh-quick-stereo.mp3` | 0.32s | brightness-flash (peak @ 192ms → pico blanco, vol 0.35) |
| ⭐ `whoosh-blade-swipe-double.mp3` | 0.56s | zoom-in-0.3s (1er swipe @ 144ms → mitad del zoom, vol 0.35) |

Los 4 ⭐ = user-uploaded 2026-06-05 (SoundBits ×2 / InspectorJ / Cyberwave Orchestra), procesados a 48kHz estéreo peak ~-1dBFS. Volumes per hard rule #9 bands.

---

## Hard rules + anti-patterns

- **#9** mix volumes → cada `audio_sting_volume` en banda. **#12** plot twist → `light-flash-impact`. **#19** measure-not-estimate → cada recipe ships `canonical_validation_status` (`pending` hasta ≥3 referentes medidos).
- ⭐ **Ley de ACOPLE movimiento↔sonido** (directiva Tomás 2026-06-05, caso camera-shake v1 rechazado): en transiciones con sting bundled, **la duración del movimiento se DERIVA del envelope audible del sting** (medir RMS por ventanas: snap → decay → umbral inaudible), no se elige independiente. Movimiento y sonido mueren JUNTOS. Si se cambia el sting de un recipe → remedir envelope y re-derivar `duration_s`.
- Anti-patterns: `light-flash-impact` >2x/reel · `cross-fade-1.0s` como default · sting salteado en `hard-cut-with-whoosh` · `camera-shake`+`light-flash-impact` en el mismo seam · >3 `zoom-in`/`pan-left` por reel (patrón mecánico detectable).

---

## Agregar una transición nueva

1. Crear `<layer>/transitions/<id>.json` con schema completo (+ `xfade_transition` + `xfade_fidelity` + `native_mechanism_note`).
2. **Agregar su entry a `catalog.json`** con `formats` explícito — sin entry en el catálogo, el sistema no la "ve".
3. Universal solo si sirve a cualquier formato; si es sabor de género → `transitions/<format>/`.
4. `canonical_validation_status: pending` salvo ≥3 referentes medidos (HR#19).
5. Correr `tests/unit/test_effects_library_recipes_schema.py` (valida schema + sync catálogo↔disco).

ffmpeg recipes target H.264 + AAC, 1080×1920 30fps, `-crf 18 -preset medium`.
