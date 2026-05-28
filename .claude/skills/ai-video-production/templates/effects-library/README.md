# effects-library (Capa A — universal primitives)

> **CAPA 1 / agnóstica.** Primitivas de transición **universales**, disponibles para CUALQUIER formato (horror-choice, B2B, documental, tutorial, cinema, etc.). Cada transición es un JSON self-contained con `ffmpeg_recipe` + `audio_recipe` + `xfade_transition` + `xfade_fidelity` + use-cases + HyperFrames alternative + canonical validation status.
>
> Companion a `avu-library/` (unidades audiovisuales pre-renderizadas) + a `caption-styles/` (mecanismo de caption-burn universal, relocado fuera de aquí en PRE-4.K).

---

## ⭐ Principio canónico: "Disponibilidad ≠ Uso" (codificado PRE-4.K 2026-05-27)

El sistema de effects-library es **TIERED** (dos capas), y la disponibilidad de un catálogo NO obliga a usarlo:

| Capa | Path | Contenido | Disponible para |
|------|------|-----------|-----------------|
| **A — universal** (este dir) | `ai-video-production/templates/effects-library/transitions/` | 7 primitivas universales | CUALQUIER formato/video |
| **B — format sub-genre** | `<format>-format/effects-library/transitions/` | efectos específicos del paradigma | Solo cuando `--format <ese-formato>` |
| **C — SPEC del video** | `creative-specs/<id>.yaml` `shot_list[].transition_in/out` | declaración explícita de qué se aplica | Este video |

- **Capa A = CATÁLOGO disponible, NO prescripción.** Ningún formato/video está obligado a usar estas primitivas.
- **Capa B = catálogo del paradigma**, disponible bajo su `--format`. NO obligatorio dentro del formato.
- **Capa C (SPEC) decide.** El agente lee el SPEC y busca cada transition en los catálogos disponibles (Capa A primitivas + Capa B del format).
- **Forward:** otros formatos (tutorial, B2B) (1) referencian primitivas Capa A directamente, (2) agregan sus propias sub-genre en su `<format>-format/effects-library/`, (3) NO duplican primitivas.

Esto resuelve el gap conceptual "agnóstico" (disponibilidad) vs "universal use" (prescripción). Capa A es agnóstica porque está disponible para todos, no porque todos deban usarla.

---

## Contents (Capa A — 7 universal primitives)

```
effects-library/                          # CAPA A universal
├── transitions/                          # 7 primitivas universales (JSON specs)
│   ├── cross-fade-0.5s.json
│   ├── cross-fade-1.0s.json
│   ├── hard-cut-with-whoosh.json         # workhorse short-form (8/8 canonical)
│   ├── black-screen-0.3s.json            # narrative comma
│   ├── fade-to-black-1.0s.json           # canonical outro
│   ├── light-flash-impact.json           # climax peak only (4/8 canonical)
│   └── glitch-transition.json            # xfade=hlslice (primitive; horror VHS variant → Capa B)
├── audio-stings/
│   ├── whoosh-warm.mp3                    # 0.48s — hard-cut sting
│   ├── drone-tension.mp3                  # 3.0s — glitch layer
│   └── flash-sharp.mp3                    # ~0.15s — light-flash impact (copied PRE-4.K, fixes broken path)
├── CANONICAL-VALIDATION-REPORT-2026-05-22.md   # master validation record (all 10 recipes, both layers)
└── README.md                             # this file
```

**Relocados en PRE-4.K (2026-05-27):**
- `overlays/caption-burn-template.css` → `ai-video-production/templates/caption-styles/` (mecanismo de caption universal, NO una transición).
- 3 sub-genre horror → `horror-choice-format/effects-library/transitions/`: `film-burn-transition`, `projector-cue-cinema`, `static-noise-transition` (+ stings `projector-cue.mp3` + copia de `drone-tension.mp3`).

**Decision 1.5 (PRE-4.K):** `glitch-transition` queda en Capa A — `xfade=transition=hlslice` es primitiva universal. Un formato que quiera variante VHS-styled crea un recipe propio en su Capa B que use esta primitiva como base.

---

## Decision matrix — primitivas universales (Capa A)

| Situation | Use | Duration | Why |
|---|---|---|---|
| Connect two beats inside the same scene | `cross-fade-0.5s` | 0.5s | Invisible blend |
| Time jump / memory dissolve | `cross-fade-1.0s` | 1.0s | Slow, reads as "later" |
| Scene change (default workhorse) | `hard-cut-with-whoosh` | 0.0s + 0.48s sting | Preserves cuts/min 2-7 |
| Narrative comma / breath | `black-screen-0.3s` | 0.3s | Brief black insert |
| Climax peak / plot twist reveal | `light-flash-impact` | 0.2s | White flash + SFX (max 1-2x/reel) |
| Outro before cliffhanger card | `fade-to-black-1.0s` | 1.0s | Universal close |
| Reality glitches (digital) | `glitch-transition` | 0.3s | xfade=hlslice RGB-shift feel |

**Sub-genre (Capa B horror-choice)** — para `--format horror-choice`, ver `horror-choice-format/effects-library/README.md`: `static-noise-transition` (VHS analog), `projector-cue-cinema` (cinema reel-change), `film-burn-transition` (cinema bloom).

---

## `xfade_transition` + `xfade_fidelity` fields (Option D, PRE-4.J 2026-05-27)

Cada recipe declara explícitamente (no inferencia):
- `xfade_transition`: el valor `xfade=transition=<name>` ffmpeg legal, o `hardcut` (concat puro).
- `xfade_fidelity`: `literal` (el recipe ES un xfade de ese tipo) o `approximate` (el recipe usa otro mecanismo — concat-insert/overlay/terminal-fade — y el chained-xfade lo aproxima).
- `native_mechanism_note`: descripción del mecanismo real cuando `approximate`.

`apply-effects-between-clips.py` lee estos fields. Cuando un recipe `approximate` se usa en producción real (no dry-run) emite WARNING. Trigger Option B (dispatch híbrido por `transition_method`) documentado en GAPS-LOG.

---

## Usage — ffmpeg recipes / HyperFrames inline

Cada `transitions/<id>.json` ships `ffmpeg_recipe` (placeholders `{clip_a}`/`{clip_b}`/`{output}`) + `hyperframes_alternative` (GSAP equivalente). Para assembly post-concat usar `scripts/apply-effects-between-clips.py` (chained-xfade desde clips atómicos, canonical PRE-4.E).

Caption burn-in: ahora en `caption-styles/caption-burn-template.css` (3 clases name/narration/warning, override defaults per BRAND.md).

---

## Audio stings — provenance (Capa A)

| Sting | Duration | Used by | Canonical status |
|---|---|---|---|
| `whoosh-warm.mp3` | 0.48s | hard-cut-with-whoosh | validated (8/8 F1 hard cuts) |
| `drone-tension.mp3` | 3.0s | glitch-transition | validated (glitch layer) |
| `flash-sharp.mp3` | ~0.15s | light-flash-impact | validated (4/8 F1 climax flash). Copiado PRE-4.K desde `library/sfx/impacts/` para self-contained (fixea path `../../../../` roto) |

Volumes per hard rule #9 bands. (`projector-cue.mp3` movido a Capa B horror-choice junto a film-burn/projector recipes.)

---

## Hard rules + anti-patterns

- **#4** caption safe zones → ahora en `caption-styles/`. **#9** mix volumes → cada `audio_sting_volume` en banda. **#12** plot twist → `light-flash-impact`. **#19** measure-not-estimate → cada recipe ships `canonical_validation_status` + `xfade_fidelity`.
- Anti-patterns: `light-flash-impact` >2x/reel; `cross-fade-1.0s` como default; saltear sting en `hard-cut-with-whoosh`; captions hand-timed (#3 violation).

---

## Adding a new transition

1. Crear `transitions/<id>.json` con schema completo + `xfade_transition` + `xfade_fidelity` + `native_mechanism_note`.
2. Si es format sub-genre (no universal) → va en `<format>-format/effects-library/transitions/`, NO aquí.
3. Validar JSON. Set `canonical_validation_status: pending` salvo ≥3 referentes medidos (#19).

---

## Versioning
- Created 2026-05-20. **PRE-4.K tiered split + PRE-4.J Option D fields: 2026-05-27.**
- ffmpeg recipes target H.264 + AAC, 1080×1920 30fps, `-crf 18 -preset medium`.
