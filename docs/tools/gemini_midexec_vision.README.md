# ai-video gemini-midexec-vision — quick reference

Mid-execution Gemini Vision hooks (Phase 2). Catch visual/audio mismatches
**per-shot during CP execution**, regen ONE asset vs full iter cycle.

Companion to `ai-video audit-frames` (post-render holistic) — this script runs
**during** CP2 / CP4 / CP5 / assembly.

## Exit codes

| code | meaning |
|------|---------|
| 0    | all checks PASS (min dimension score ≥7) |
| 1    | 🔴 score <7 detected → regen this single asset |
| 2    | error (deps missing, file missing, API failure) |

## Hooks

### Hook 1 — `hailuo_post` (CP4, per animation clip)

After Hailuo / Kling / Seedance generates `shot_NN.mp4`:

```bash
uv run ai-video gemini-midexec-vision \
  --hook hailuo_post \
  --clip assets/clips/shot_05_film_reveal.mp4 \
  --spec creative-specs/cinema-abandonado.yaml \
  --shot-id shot_05_film_reveal \
  --output reports/midexec/shot_05_hailuo.json
```

Extracts 3 frames (start/mid/end), single Gemini Vision call. Scores 5 dimensions:

- `visual_match` — LITERAL match vs `visual_action_match.visual_intent`
- `character_consistency` — same face/clothes/props across start/mid/end
- `atmospheric_motions_visible` — motions listed in `atmospheric_motions_list` actually present
- `composition_safe_zones` — sujeto not cut, IG Reel safe zones respected
- `literal_action_match` — characters do what `scene_context.who_does_what` says

Cost ~$0.05 per shot.

### Hook 2 — `tts_post` (CP2, per TTS segment)

After ElevenLabs generates `segment_NN.mp3` and `atempo` is applied:

```bash
uv run ai-video gemini-midexec-vision \
  --hook tts_post \
  --tts assets/tts/decision_1_question.mp3 \
  --spec creative-specs/cinema-abandonado.yaml \
  --segment-id decision_1_question
```

Local Whisper transcribe + check:

- **Text match** — Jaccard token similarity vs SPEC `text_canonical` (threshold 0.55)
- **Audibility** — `ffmpeg volumedetect mean_volume` in `[-30, -16]` dBFS
- **Voseo grep** — flags `vos / decís / elegís / salís / sos / tenés / ...` per
  `feedback_spanish_neutral` memory

Cost $0 (all local).

### Hook 3 — `atomic_post` (CP5, per atomic muxed clip)

After `ai-video build-clip-atomic` outputs `shot_NN_atomic.mp4` (image + audio + caption synced):

```bash
uv run ai-video gemini-midexec-vision \
  --hook atomic_post \
  --clip assets/clips-atomic/shot_05_atomic.mp4 \
  --spec creative-specs/cinema-abandonado.yaml \
  --shot-id shot_05_film_reveal \
  --captions iter3-captions.json
```

3 frames → Gemini Vision. Scores:

- `caption_alignment` — Y 58-72% band respected, not cut off
- `caption_legibility` — drop shadow visible, contrast OK
- `ui_no_overlap` — UI elements not stepping on each other
- `visual_intent_match` — frame shows visual_intent literally
- `composition_intact` — no broken composition, no black frames

Cost ~$0.05 per atomic clip.

### Hook 4 — `transition_post` (assembly time, per transition)

After ffmpeg concats `clip_N + transition_effect + clip_N+1`:

```bash
uv run ai-video gemini-midexec-vision \
  --hook transition_post \
  --concat assets/clips-atomic/concat_05_06.mp4 \
  --from-shot shot_05_film_reveal \
  --to-shot shot_06_offers_seat_boleto
```

4 frames sampled around transition midpoint (40/48/52/60%). Scores:

- `visual_continuity` — natural vs jarring
- `no_broken_frames` — no black/corrupt/glitched frames
- `ui_continuity` — captions/watermark handoff clean
- `composition_flow` — encuadre not whiplash extreme
- `atmospheric_continuity` — lighting/color grade coherent

Cost ~$0.05 per transition.

## Total cost per video

| hooks | count typical | cost |
|-------|---------------|------|
| hailuo_post | ~22 shots | $1.10 |
| tts_post | ~18 segments | $0.00 |
| atomic_post | ~22 clips | $1.10 |
| transition_post | ~6 transitions (only flagged ones) | $0.30 |
| **total** | | **~$2.50** |

In practice run hailuo_post + tts_post on EVERY asset and only run atomic_post / transition_post on uncertain ones → ~$0.10-0.30 per video, often catching 1 bad shot = saves a full iter cycle ($5-9).

## Integration pattern in engineer scripts

Wrap your existing generation calls:

```python
import subprocess

# After Hailuo finishes shot_05.mp4:
result = subprocess.run([
    "uv", "run", "ai-video", "gemini-midexec-vision",
    "--hook", "hailuo_post",
    "--clip", "assets/clips/shot_05.mp4",
    "--spec", "creative-specs/<id>.yaml",
    "--shot-id", "shot_05_film_reveal",
    "--output", f"reports/midexec/shot_05.json"
])

if result.returncode == 1:
    # 🔴 flagged — regen THIS shot only, not full iter
    regen_hailuo("shot_05")
elif result.returncode == 2:
    # error path — escalate
    raise RuntimeError("midexec vision failed, check logs")
# returncode 0 → continue pipeline
```

## Dependencies

Already part of the project venv:

- `google-genai` (Gemini Vision)
- `python-dotenv` (`.env` with `GEMINI_API_KEY`)
- `pyyaml` (load SPEC)
- `openai-whisper` (local Whisper for `tts_post`) — `pip install openai-whisper`
- system: `ffmpeg` + `ffprobe`

## Score threshold

`SCORE_FAIL_THRESHOLD = 7` — any dimension <7 flags regen. Tunable in the
script header if you want stricter (8) or looser (6) for early iterations.
