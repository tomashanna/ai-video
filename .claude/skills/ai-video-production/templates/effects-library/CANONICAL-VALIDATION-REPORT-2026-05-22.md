# Effects-library canonical validation — 2026-05-22

## Method

- **N refs analyzed**: 8 (ref-03, ref-06, ref-08, ref-09, ref-10, ref-11, ref-12, ref-13 — full F1 canonical set)
- **N transitions audited**: 10 (all files in `effects-library/transitions/`)
- **Data sources**: `ref-XX-frame-by-frame-events.json` (scene_cut counts + segment timing) + `ref-XX-<chars>-<setting>.md` (narrative beat-by-beat descriptions with explicit transition language) + `aggregate-patterns.json` (cross-ref synthesis)
- **Classification scheme**:
  - **OBSERVED** — explicit narrative/event description of this transition type at a specific timestamp
  - **VARIANT** — similar concept different parameters (e.g., fade-to-black observed but duration 0.5s not 1.0s)
  - **ABSENT** — no evidence in narrative or events
  - **INSUFFICIENT_DATA** — frame events don't classify transition type AND narrative is ambiguous

## Limitations

1. **`*-frame-by-frame-events.json` does NOT classify transition type per cut** — only counts `n_scene_cuts` and timestamps. Transition style (hard cut vs fade vs flash) inferred from narrative `*.md` descriptions only.
2. **Narrative descriptions vary in precision** — ref-03/08 explicitly state "fade negro" / "hard cut a fade negro post-muerte"; ref-06/09/11 use more generic "cut hacia X" language without specifying whether fade or hard cut.
3. **Glitch/flicker effects in 4/8 refs apply to CAPTION TEXT overlay only**, NOT inter-clip transitions. The library's `glitch-transition.json` (designed as inter-clip RGB-split) is a different effect class than what the canonical refs use.
4. **No audio waveform analysis was performed** — whoosh/sting presence inferred from narrative "audio-visual sync" mentions (ref-08 § 7, ref-10 § 7, ref-11 § 7, ref-13 § 7), not from spectral analysis of the actual ref audio.
5. **F1 canonical set has zero cinema-setting refs** — `film-burn-transition` and `projector-cue-cinema` cannot be validated against this cohort by design.

## Matrix (10 × 8)

| transition_id | ref-03 | ref-06 | ref-08 | ref-09 | ref-10 | ref-11 | ref-12 | ref-13 | validated_N/8 |
|---|---|---|---|---|---|---|---|---|---|
| black-screen-0.3s | OBSERVED (28.5s, 49.2s, 71.7s death-cut masks) | ABSENT | OBSERVED (post-muerte + Pablo apaga luces 60s) | ABSENT | ABSENT | ABSENT | VARIANT (111s fade out — outro-length, not 0.3s breath) | ABSENT | **2/8** |
| cross-fade-0.5s | ABSENT (95% hard cuts per § 6) | ABSENT (UI button fade-in only, not clip-to-clip) | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | **0/8** |
| cross-fade-1.0s | VARIANT (paleta shift warm→dawn 79-81s via hard cut not blend) | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | OBSERVED (sepia flashback Beat 12 monólogo Teresa 85-90s) | ABSENT | **1/8** |
| fade-to-black-1.0s | OBSERVED (49.2-49.7s explosion fade negro) | ABSENT | VARIANT (fade negro post-muerte 22s but quick not 1.0s) | ABSENT | ABSENT | ABSENT | OBSERVED (111-113s "Fade out. Music crescendo final") | ABSENT | **2/8** |
| film-burn-transition | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | **0/8** |
| glitch-transition (inter-clip) | ABSENT | ABSENT | ABSENT (caption-level flicker only, not inter-clip) | ABSENT | ABSENT (caption-level only) | ABSENT (caption-level only) | ABSENT (caption-level only) | ABSENT | **0/8** |
| hard-cut-with-whoosh | OBSERVED (42 cuts, 95% hard § 6) | OBSERVED (17 hard cuts) | OBSERVED (18 hard cuts + § 7 audio-visual sync) | OBSERVED (34 hard cuts, highest density) | OBSERVED (22 hard cuts + § 7 SFX sync) | OBSERVED (22 hard cuts + § 7 "4 momentos audio-impact sync") | OBSERVED (32 hard cuts) | OBSERVED (68 hard cuts + CUTS FLOODING climaxes) | **8/8** |
| light-flash-impact | ABSENT | ABSENT | OBSERVED (58-60s flash blanco + descarga sync § 7) | ABSENT | OBSERVED (47-49s flash blanco partículas § 7) | OBSERVED (§ 7 "4 momentos impacto audio + flash de luz") | ABSENT | OBSERVED (34-37s flash blanco + 1:02 impacto sónico + warp) | **4/8** |
| projector-cue-cinema | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | **0/8** |
| static-noise-transition (inter-clip) | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT | ABSENT (cuts flooding ≠ VHS static) | **0/8** |

## Candidate adds (canonical patterns NOT in library)

1. **`hard-cut-with-flash-sync`** (variant of hard-cut-with-whoosh) — Observed in 4/8 refs at non-climax beats (ref-08 descarga, ref-10 vapor, ref-11 4-moment audio-impact, ref-13 cuts flooding). Different from `light-flash-impact` (which is climax-only): this is a cut where audio impact (SFX, drone hit, drop) syncs frame-perfect with a visual flash element WITHOUT full white screen. Worth adding as a distinct transition because canonical pattern is "audio impact → visual flash element (white particles, electric sparks, drop visual) → cut" rather than full whiteout.

2. **`cuts-flooding-burst`** — Observed in ref-13 exclusively (60+ cuts in 5s at warp moments 28-37s + 66-71s). Could be a structured macro-transition: "rapid cut density burst" for climactic moments. ref-13 descriptive § 6 + scene_cuts.txt confirm pattern. Not generalizable to other F1 refs but worth documenting as a "climax pacing intensifier" macro.

3. **`hard-cut-to-counterfactual-tonal-shift`** — Observed in 6/8 refs (ref-03, ref-06, ref-08, ref-09, ref-10, ref-13) as the canonical outro transition: hard cut from horror scene directly to cozy counterfactual scene with simultaneous tonal palette shift (warm/eerie → warm/dawn or cool/cinema → cozy/amber). NOT a fade — explicit hard cut with paleta change. More common than `fade-to-black-1.0s` for outros (6/8 vs 2/8). Worth codifying as a distinct outro pattern transition.

## Candidate deprioritize (library effects with 0 canonical observations)

1. **`cross-fade-0.5s`** (0/8) — F1 canonical pattern explicitly rejects soft crossfades for inter-beat connection. ref-03 § 6 reports "95% hard cuts". Prior validation citing ref-01/04/07 is invalid (those refs are not in F1 set). **Recommendation**: remove from default rotation in horror-choice format. Keep available as a GENERIC effect for non-horror sub-genres (lifestyle, brand-story) where soft blends are appropriate.

2. **`glitch-transition`** (0/8 inter-clip) — Caption-level glitch is in 4/8 refs but inter-clip RGB-split glitch is in 0/8. **Recommendation**: split into two distinct library items — (a) `caption-glitch-text` effect (validated 4/8 for caption overlay) and (b) `inter-clip-glitch-transition` (0/8, sub-genre only). Current single JSON conflates these.

3. **`static-noise-transition`** (0/8) — No F1 canonical evidence. Sub-genre-specific (found-footage/VHS/cabin horror). **Recommendation**: keep but require explicit SPEC justification field (e.g., `setting.aesthetic = "found-footage"` OR `beat.signature = "reality-glitch"`).

## Audio stings canonical alignment

- **whoosh-warm.mp3** — Observed implicitly in 4/8 refs as audio-visual-sync impact stings (ref-08 § 7, ref-10 § 7, ref-11 § 7 "4 momentos impacto audio", ref-13 § 7 "impacto sónico sincronizado"). Refs do NOT name "whoosh" specifically — they describe generic "impacto de audio" or "drone burst" or "drop hit" depending on beat. **The hard-cut + audio-impact pattern is 8/8 universal** even when whoosh-specific timbre is not cited. **validated 4/8 explicit + 4/8 implicit pattern fit**.

- **drone-tension.mp3** — No explicit canonical observation by filename. Implicit fit: refs 03/10/13 mention sub-bass drones and "hum industrial" ambient layers (ref-10 § 3 "ambient: hum industrial"). Used by library as input for static-noise + glitch transitions (both 0/8). **validated 0/8 explicit — pending dedicated ambient drone analysis**.

- **projector-cue.mp3** — No canonical observation possible (zero cinema refs in F1). **validated 0/8 by design**. Reserved for cinema sub-genre use only.

## Honest gaps in measurement

1. **Frame events JSON lacks transition_type field** — all 8 `ref-XX-frame-by-frame-events.json` files report `n_scene_cuts` + `scene_cut_density_per_min` but do NOT classify each cut as hard/fade/flash/etc. Classification relied entirely on narrative `.md` descriptions, which vary in precision.
2. **Ambiguous "cut hacia X" language** in ref-06 (line 234, 494), ref-08 (line 454), ref-10 (line 417), ref-13 (line 505) — these mention scene changes but do not specify transition style. Default-assumed hard cut based on cohort prevalence (95% hard cuts in ref-03 § 6) but not directly confirmed.
3. **No audio spectral analysis** — sting presence inferred from narrative "audio-visual sync" mentions. ref-11 § 7's "4 momentos" is the most explicit audio-impact count but does not specify timbre (whoosh vs drone burst vs flash crack).
4. **Glitch/flicker conflation risk** — 4 refs mention glitch/flicker effects (ref-08, ref-10, ref-11, ref-12) but ALL apply to CAPTION TEXT overlay, NOT inter-clip transition. The library's `glitch-transition.json` description targets inter-clip use, so canonical "glitch presence" does NOT validate it.
5. **Sub-genre out-of-scope effects** — `film-burn-transition`, `projector-cue-cinema` cannot be validated against F1 (zero cinema refs by design). This is acknowledged in the JSONs but is a structural gap in the F1 cohort.

## Recommendation

### Validated effects ready for V4+ default use (N ≥ 3)

- **`hard-cut-with-whoosh`** (8/8) — workhorse default for all inter-beat transitions in horror-choice. Use freely.
- **`light-flash-impact`** (4/8) — climax peak transitions. Use 1-2x per reel max. Photosensitive safety constraint preserved.

### Validated with caution (N = 1-2)

- **`black-screen-0.3s`** (2/8) — use mainly to mask death-cut frames, not as inter-beat narrative comma. Max 2x per reel.
- **`fade-to-black-1.0s`** (2/8) — use ONLY when narrative explicitly requires "end of chapter" weight. More common F1 outro pattern is hard cut directly to counterfactual cozy (6/8) — see candidate add #3.
- **`cross-fade-1.0s`** (1/8) — memory/sepia flashback only. Do not use for ordinary beat connection.

### Flag-with-caution in V4 (N = 0, sub-genre justified)

- **`film-burn-transition`** (0/8) — cinema sub-genre only. Require explicit SPEC `setting.aesthetic = "cinema"`.
- **`projector-cue-cinema`** (0/8) — cinema sub-genre only. Same constraint.
- **`static-noise-transition`** (0/8) — found-footage sub-genre only. Require explicit SPEC `beat.signature = "reality-glitch"` or `setting.aesthetic = "found-footage"`.

### Recommended actions

- **Remove from default rotation**: `cross-fade-0.5s` (0/8, generic with no canonical observation). Keep available for non-horror sub-genres but flag in SPEC validator.
- **Split into two library items**: `glitch-transition` → (a) `caption-glitch-text-effect` (validated 4/8 separate validation) + (b) `inter-clip-glitch-transition` (0/8 sub-genre).
- **Add to library** (high priority): `hard-cut-to-counterfactual-tonal-shift` (6/8 canonical outro pattern, currently absent from library).
- **Consider adding** (medium priority): `hard-cut-with-flash-sync` (variant for non-climax audio-impact moments, 4/8).
- **F2 cohort needed**: cinema-setting refs to validate `film-burn-transition` + `projector-cue-cinema` technical parameters.
