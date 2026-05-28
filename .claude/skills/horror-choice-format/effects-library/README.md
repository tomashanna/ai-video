# effects-library (Capa B — horror-choice sub-genre)

> **CAPA 2 / format-specific.** Transiciones específicas del paradigma **horror-choice**, disponibles solo bajo `--format horror-choice`. Relocadas desde Capa A en PRE-4.K (2026-05-27) por ser sub-genre (cinema / found-footage / VHS), NO primitivas universales.
>
> Para primitivas universales (cross-fade, hard-cut, fade-to-black, black-screen, light-flash, glitch) → `ai-video-production/templates/effects-library/` (Capa A).

---

## ⭐ Principio "Disponibilidad ≠ Uso"

- Estas transiciones son **CATÁLOGO del paradigma horror-choice**, disponibles cuando `--format horror-choice`.
- Estar disponibles NO obliga a usarlas. El **SPEC del video (Capa C)** declara explícitamente qué transitions se aplican en `shot_list[].transition_in/out`.
- El agente lee el SPEC y busca cada transition en los catálogos disponibles: **Capa A primitivas** (universales) + **Capa B** (este — horror sub-genre).
- Un horror-choice video típicamente usa primitivas Capa A (hard-cut, cross-fade, light-flash) + ocasionalmente una sub-genre de aquí cuando el setting lo amerita (cinema/found-footage).

---

## Contents

```
horror-choice-format/effects-library/        # CAPA B horror-choice
├── transitions/                              # 3 sub-genre recipes (JSON specs)
│   ├── film-burn-transition.json             # cinema warm-amber bloom (0/8 F1 — cinema-setting only)
│   ├── projector-cue-cinema.json             # cinema reel-change cue (0/8 F1 — cinema-setting only)
│   └── static-noise-transition.json          # VHS analog noise burst (0/8 F1 — found-footage only)
├── audio-stings/
│   ├── projector-cue.mp3                      # 1.0s — cinema reel-change (film-burn + projector recipes)
│   └── drone-tension.mp3                      # 3.0s — static-noise underlayer (shared primitive, copia de Capa A)
└── README.md                                 # this file
```

**Nota sting `drone-tension.mp3`:** es una primitiva de audio compartida (también en Capa A, usada por `glitch-transition`). Copiada aquí para que `static-noise-transition` (Capa B) sea self-contained — sin paths relativos cross-layer frágiles. Cada catálogo es self-contained.

---

## Decision matrix — sub-genre horror-choice (Capa B)

| Situation | Use | Duration | Constraint |
|---|---|---|---|
| Cinema-genre scene change | `projector-cue-cinema` | 1.0s | Solo si setting = cinema/theater/drive-in |
| Cinema flashback / memory bloom | `film-burn-transition` | 0.6s | Warm orange bloom; solo cinema aesthetic |
| Reality glitch (analog VHS) | `static-noise-transition` | 0.4s | Found-footage / security-cam / reality-break beat; max 2x/reel |

**Canonical status:** las 3 son **0/8 F1** (el set canónico horror-choice no tiene refs cinema/found-footage). Requieren justificación explícita en el SPEC (`setting = cinema` / `found-footage` / `reality-glitch beat`). Validación técnica pendiente de un F2 referent set del sub-genre.

---

## `xfade_transition` + `xfade_fidelity` (Option D, PRE-4.J)

Cada recipe declara `xfade_transition` + `xfade_fidelity` + `native_mechanism_note`. Las 3 de aquí son `approximate` (sus mecanismos reales — concat-insert de ruido, overlay bloom ámbar — NO son xfades puros; el chained-xfade los aproxima). `apply-effects-between-clips.py` emite WARNING al usarlas en producción real. Trigger Option B (dispatch híbrido por `transition_method` para fidelidad completa) documentado en GAPS-LOG.

| Recipe | `xfade_transition` | `xfade_fidelity` | Native mechanism |
|--------|--------------------|------------------|------------------|
| film-burn-transition | `fadewhite` | approximate | alpha-fade + overlay bloom ámbar (no equivalente xfade) |
| projector-cue-cinema | `fade` | approximate (literal core) | `xfade=fade` core + white-bloom fades + projector sting |
| static-noise-transition | `dissolve` | approximate | concat + inserto 0.4s ruido analógico (geq random) |

---

## Adding a horror-choice sub-genre transition

1. Crear `transitions/<id>.json` con schema completo + `xfade_transition`/`xfade_fidelity`/`native_mechanism_note`.
2. Si la transición es **universal** (no horror-specific) → va en Capa A, NO aquí.
3. Si necesita un sting nuevo, copialo a `audio-stings/` (self-contained).
4. Set `canonical_validation_status` honesto (0/N si no medido contra refs del sub-genre).

---

## Versioning
- Created 2026-05-27 (PRE-4.K tiered relocation desde Capa A).
- Master validation record (las 10 recipes ambas capas): `ai-video-production/templates/effects-library/CANONICAL-VALIDATION-REPORT-2026-05-22.md`.
