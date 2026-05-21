# effects-library — transitions, overlays, audio stings

> CAPA 1 universal template. Drop-in reusable effects for ANY AI video project (horror-choice, B2B, documental, cinema, etc.). Each transition ships as a self-contained JSON spec with a copy-paste ffmpeg recipe + audio recipe + use-cases + HyperFrames alternative + canonical validation status.
>
> Companion to `avu-library/` (audiovisual units: countdown, hook transition, outro card). Where AVU = pre-rendered .mp4 components, this library = procedural effects you apply between clips at render time.

---

## Contents

```
effects-library/
├── transitions/                      # 10 procedural inter-clip effects (JSON specs)
│   ├── cross-fade-0.5s.json
│   ├── cross-fade-1.0s.json
│   ├── hard-cut-with-whoosh.json     # workhorse for short-form
│   ├── film-burn-transition.json
│   ├── static-noise-transition.json
│   ├── black-screen-0.3s.json
│   ├── fade-to-black-1.0s.json       # canonical outro
│   ├── light-flash-impact.json       # climax peak only
│   ├── projector-cue-cinema.json
│   └── glitch-transition.json
├── overlays/
│   └── caption-burn-template.css     # 3-class caption style (name/narration/warning)
├── audio-stings/
│   ├── whoosh-warm.mp3               # 0.48s — hard-cut sting
│   ├── drone-tension.mp3             # 3.0s — glitch/static layer
│   └── projector-cue.mp3             # 1.0s — cinema reel-change
└── README.md                          # this file
```

---

## Decision matrix — which transition to use

| Situation | Use | Duration | Why |
|---|---|---|---|
| Connect two beats inside the same scene | `cross-fade-0.5s` | 0.5s | Invisible blend, no rupture |
| Time jump / memory dissolve | `cross-fade-1.0s` | 1.0s | Slow, deliberate, reads as "later" |
| Scene change (default workhorse) | `hard-cut-with-whoosh` | 0.0s + 0.48s sting | Preserves cuts/min target 2-7 |
| Cinema-genre scene change | `projector-cue-cinema` | 1.0s | Diegetic + reel-change feel |
| Cinema or memory bloom | `film-burn-transition` | 0.6s | Warm orange consumes frame |
| Reality glitches (analog) | `static-noise-transition` | 0.4s | VHS-style noise burst |
| Reality glitches (digital) | `glitch-transition` | 0.3s | RGB-split + pixel shift |
| Narrative comma / breath | `black-screen-0.3s` | 0.3s | Brief black insert, lets beat land |
| Climax peak / plot twist reveal | `light-flash-impact` | 0.2s | White flash + sharp SFX (max 1-2x/reel) |
| Outro before cliffhanger card | `fade-to-black-1.0s` | 1.0s | Universal close pattern (9/10 canonicals) |

---

## Usage — ffmpeg recipes (procedural baking)

Each `transitions/<id>.json` ships an `ffmpeg_recipe` field with placeholder params (`{clip_a}`, `{clip_b}`, `{offset}`, `{output}`). Workflow:

```bash
# 1. Inspect the spec
cat .claude/skills/ai-video-production/templates/effects-library/transitions/hard-cut-with-whoosh.json | jq

# 2. Read params (ffmpeg_params field tells you how to compute placeholders)

# 3. Substitute + run
CLIP_A=assets/clips-trimmed/h3-shot1.mp4
CLIP_B=assets/clips-trimmed/h3-shot2.mp4
DUR_A=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $CLIP_A)
WHOOSH_MS=$(python3 -c "print(int(($DUR_A * 1000) - 80))")

ffmpeg -y -i $CLIP_A -i $CLIP_B \
  -i .claude/skills/ai-video-production/templates/effects-library/audio-stings/whoosh-warm.mp3 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v];[0:a][1:a]concat=n=2:v=0:a=1[base];[2:a]adelay=${WHOOSH_MS}|${WHOOSH_MS},volume=0.55[whoosh];[base][whoosh]amix=inputs=2:duration=first:normalize=0[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k \
  assets/clips-trimmed/h3-with-whoosh.mp4
```

---

## Usage — HyperFrames inline (recommended for short-form)

Most transitions ship a `hyperframes_alternative` field with the equivalent GSAP timeline. Prefer this over ffmpeg pre-baking when:

- You're inside an active HyperFrames composition (faster iteration, no re-render of upstream clips).
- The transition needs to sync with caption/SFX tracks that live in the composition timeline.
- You want to A/B variants of the transition without re-encoding clips.

Example — `hard-cut-with-whoosh` inline:

```html
<!-- HyperFrames index.html -->
<audio data-track-index="62" data-start="14.5" src="assets/sfx/cut-warm-whoosh.mp3" data-volume="0.55"></audio>
<!-- The hard cut itself = data-end of clip_a meets data-start of clip_b at 14.58s -->
```

---

## Usage — overlays/caption-burn-template.css

Three canonical classes — drop into any project's stylesheet:

```html
<link rel="stylesheet" href=".claude/skills/ai-video-production/templates/effects-library/overlays/caption-burn-template.css">

<div class="caption-wrap">
  <span class="caption-narration">El sótano <span class="keyword">olía</span> a humedad.</span>
</div>

<div class="caption-name">EMI <span class="archetype">MALO APARENTE</span></div>

<div class="caption-warning">
  <span class="lead-in">Si elegiste a</span>
  EMI
</div>
```

GSAP integration:
```js
tl.from('.caption-narration', { opacity: 0, y: 8, duration: 0.18 }, 'tBeat');
```

Canonical positions (hard rule #4):
- `.caption-wrap`: `bottom: 540px; height: 280px` (Y 62%)
- `.caption-name`: `top: 220px` (Y 11.5%)

---

## Audio stings — provenance + canonical status

| Sting | Duration | Source | Canonical status |
|---|---|---|---|
| `whoosh-warm.mp3` | 0.48s | `library/sfx/cuts/cut-warm-whoosh.mp3` | validated (8/10 F1 referents use warm whoosh for hard cuts) |
| `drone-tension.mp3` | 3.0s | `library/sfx/drones/tension-rise-3s.mp3` | validated (used as glitch/static underlayer) |
| `projector-cue.mp3` | 1.0s | `cinema-abandonado/assets/sfx/projection_film_transition.mp3` | pending (cinema sub-genre not in F1 set — manual QA per video) |

Volumes follow hard rule #9 mix canonical bands:
- Whoosh / hard-cut sting: **0.55** (within flash impacts band 0.55-0.65)
- Drone tension layer: **0.35** (within SFX events band 0.20-0.35)
- Projector cue: **0.45** (within SFX events band, top of range)
- Light-flash impact SFX: **0.65** (top of flash impacts band — meant to peak)

---

## Hard rules cross-reference

Every spec in this library aligns with CLAUDE.md hard rules:

- **#4** UI safe zones — caption CSS positions (540px / 220px) are canonical.
- **#9** Mix volumes — every `audio_sting_volume` field stays within canonical bands.
- **#12** Plot twist coherence — `light-flash-impact` reserved for plot-twist reveal cuts (3 conditions).
- **#19** "NEVER ESTIMATE, ALWAYS MEASURE" — each spec ships `canonical_validation_status` explicit (`validated` / `pending`) + `validated_against_canonical_refs` list. `pending` specs require manual QA per video until F2 referent set established.
- **Pacing markers** (CLAUDE.md table) — see `ai-video-production/PACING-MARKERS.md` for cuts/min 2-7 rule when chaining transitions.

---

## Anti-patterns

1. **Using `light-flash-impact` >2x per reel** → loses impact, viewer fatigue, photosensitive risk.
2. **Using `cross-fade-1.0s` as default scene change** → kills short-form pacing (cuts/min drops below 2).
3. **Using `film-burn-transition` or `projector-cue-cinema` in non-cinema genres** → breaks aesthetic coherence.
4. **Skipping audio sting on `hard-cut-with-whoosh`** → naked cut feels amateur; sting is non-optional.
5. **Hand-timed captions overlay** → hard rule #3 violation. Always Whisper-timed via `scripts/captions.py`.
6. **More than 2x `static-noise-transition` or `glitch-transition` per reel** → "reality glitch" loses meaning through repetition.
7. **Burning captions via this CSS in HyperFrames AND scheduling separate caption track** → double captions on render. Pick one path per project.

---

## Adding a new transition

1. Create `transitions/<new-id>.json` with the full schema (see any existing spec as reference).
2. Required fields: `id`, `type`, `category`, `duration_s`, `description`, `ffmpeg_recipe`, `ffmpeg_params`, `audio_recipe`, `use_cases`, `avoid_for`, `hyperframes_alternative`, `canonical_validation_status`, `validated_against_canonical_refs`, `validated_notes`.
3. If using a new audio sting, copy the source `.mp3` into `audio-stings/` and document provenance in this README's audio stings table.
4. Validate JSON: `python3 -c "import json; json.load(open('transitions/<new-id>.json'))"`.
5. Update the decision matrix above with the new option.
6. Set `canonical_validation_status: pending` unless you've explicitly measured against ≥3 F1/F2 canonical referents per hard rule #19.

---

## Versioning + provenance

- Created: 2026-05-20 (Engineer Sub-Agent B build phase).
- Audio stings: copied from `library/sfx/` + `cinema-abandonado/assets/sfx/` (paths in audio stings table).
- All ffmpeg recipes target H.264 + AAC for IG Reel compatibility (1080×1920, 30fps).
- All recipes use `-crf 18` (visually lossless) and `-preset medium` (balance of speed/size). Override per-project if needed.
