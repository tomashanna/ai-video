# quality_gate_per_clip.py — Quality Gate Agent (4th role)

Per-clip automated QA. Runs AFTER `build_clip_atomic.py` per shot, BEFORE assembly.

## Why it exists

Existing gates (`audit-frames.py`, `audit-audio.py`, `audit-frames-granular.py`) measure
the WHOLE render. By then, bugs are baked in. This script catches bugs **per atomic clip**
so failures halt assembly upstream — cheaper to fix one shot than reflow the full timeline.

Closes the upstream side of Hard Rule #1 dual gate (Gemini ≥9.7 + audit-against-referent ≥85%):
the 4th-agent per-clip gate makes those holistic gates **trivial to pass** because every clip
ships canonical-compliant.

## When to run

```
build_clip_atomic.py shot_NN  →  quality_gate_per_clip.py shot_NN  →  (🟢 PASS) assemble
                                                                  →  (🟡 NB)   review then assemble
                                                                  →  (🔴 FAIL) halt + escalate
```

## Usage

```bash
python quality_gate_per_clip.py \
    --clip assets/clips-atomic/shot_07_atomic.mp4 \
    --captions assets/clips-atomic/shot_07_captions.json \
    --spec creative-specs/<id>.yaml \
    --shot-id shot_07_d1_setup_question \
    --enable-gemini      # optional, ~$0.10/clip
    --enable-whisper     # optional, slow but verifies TTS↔caption text match
    --clip-start-abs-s 38.5  # absolute timeline offset for cross-clip context
```

Outputs:
- `assets/clips-atomic/shot_NN_atomic_audit.json` — machine-readable findings + verdict
- `assets/clips-atomic/shot_NN_atomic_audit.md`   — human report

## 5 check categories

| # | Check | Tooling |
|---|---|---|
| 1 | Visual canonical compliance — SPEC scene_context match, atmospheric_motions ≥3, character drift vs anchor, composition, UI overlap | Gemini Vision (3 frames: start, mid, end) |
| 2 | Caption schema — all `start_abs_s`/`end_abs_s` present, no overlap same-Y, chunks ≥1.5s, no voseo/tuteo mismatch vs SPEC register | Sidecar JSON parse |
| 3 | Audio waveform — LUFS -14 ±0.5, true peak ≤-1 dBFS, no clipping (max ≥0), speech audibility -30 to -16 dBFS | ffmpeg loudnorm + volumedetect |
| 4 | Sync verify — audio↔video duration ±0.1s, TTS↔caption text similarity ≥0.6 | ffprobe + (optional) Whisper re-transcribe |
| 5 | GAPS sentinels (per-clip subset) — S1 ghost-speaker, S2 duplicate text, S6 AVU countdown energy, S8 atmospheric motions count | Local heuristics |

## Verdict thresholds

| Verdict | Logic | Exit code |
|---|---|---|
| 🟢 **PASS** | 0 FAIL · ≤2 WARN | 0 |
| 🟡 **NB** (review) | 0 FAIL · ≥3 WARN | 1 |
| 🔴 **FAIL** (halt) | ≥1 FAIL | 2 |
| — | Script error (missing inputs/deps) | 3 |

A WARN per check = "marginal but not blocking". `audio_waveform` WARN escalates to FAIL when
delta thresholds exceeded (LUFS off by >2 dB, true_peak ≥0 dBFS).

## Canonical thresholds (constants at top of file)

```python
TARGET_LUFS = -14.0
LUFS_TOLERANCE = 0.5
TRUE_PEAK_MAX = -1.0
SPEECH_MEAN_VOL_MIN = -30.0
SPEECH_MEAN_VOL_MAX = -16.0
MIN_CAPTION_CHUNK_S = 1.5
CANONICAL_CAPTION_Y_LOW = 55
CANONICAL_CAPTION_Y_HIGH = 70
MIN_ATMOSPHERIC_MOTIONS = 3
AUDIO_VIDEO_DURATION_TOLERANCE_S = 0.1
WHISPER_TEXT_SIM_MIN = 0.6
```

Adjust at the top of the script if the format's canonical band evolves.

## Cost per clip

- Default (no flags): $0 (ffmpeg + local heuristics only)
- `--enable-gemini`: ~$0.10/clip (3 frames × Gemini 3.1 Flash Lite Vision)
- `--enable-whisper`: $0 but 10-30s CPU time per clip (small model)

Recommended: run default for every clip, add `--enable-gemini` for HERO tier shots
+ on iter ≥2 of any shot that failed visual on the previous iter.

## SPEC fields read

Per shot (via `--shot-id` lookup):
- `scene_context.who_is_there` / `who_does_what`
- `atmospheric_motions_count` / `atmospheric_motions_list`
- `camera`
- `narration_in_this_shot.{narrator_text, character_dialogue, silence_by_design}`
- `audio_visual_atomic_units` (for AVU detection)
- top-level `register` / `narrative_register` / `person` (voseo vs tuteo)

Falls back gracefully when fields absent (logs INFO/WARN, not FAIL).

## Dependencies

- `ffmpeg` + `ffprobe` (CLI, must be on PATH)
- `pyyaml` (always required)
- `google-genai` + `python-dotenv` + `GEMINI_API_KEY` env (only if `--enable-gemini`)
- `openai-whisper` (only if `--enable-whisper`)

## Integration with existing pipeline

Drop-in step right after atomic clip render:

```bash
# In project script that wraps build_clip_atomic:
.venv/bin/python scripts/build_clip_atomic.py --shot-id shot_07 || exit 1
.venv/bin/python scripts/quality_gate_per_clip.py \
    --clip assets/clips-atomic/shot_07_atomic.mp4 \
    --captions assets/clips-atomic/shot_07_captions.json \
    --spec creative-specs/$(basename $PWD).yaml \
    --shot-id shot_07_d1_setup_question \
    --enable-gemini
case $? in
  0) echo "🟢 shot_07 ship-ready" ;;
  1) echo "🟡 shot_07 NB — review audit.md before assembly" ;;
  2) echo "🔴 shot_07 FAIL — halt assembly"; exit 2 ;;
  3) echo "❌ script error"; exit 3 ;;
esac
```

## Sanity-tested 2026-05-20

Ran against cinema-abandonado clips:
- `assets/clips-trimmed/shot_02.mp4` (no audio stream by design) → 🟢 PASS with 1 expected WARN
- `renders/draft.mp4` cropped 38.5-45.5s (shot_07 segment with audio) → 🟢 PASS with 2 audio WARN (real LUFS -14.95 detected, speech mean_vol -15.50 detected — both genuine signals)
- Synthetic broken captions (missing `end_abs_s`, Y-overlap, ghost speaker) → 🔴 FAIL correctly detected schema FAIL + sentinel_s1 FAIL
