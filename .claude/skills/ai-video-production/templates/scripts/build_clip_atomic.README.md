# build_clip_atomic.py — Per-clip atomic assembly

Per-clip atomic AVU builder (Phase 2 architectural refactor). Each clip becomes a self-contained `<shot>_atomic.mp4` with visual + audio + captions + manifest bundled, eliminating end-of-timeline sync drift bugs that compound under the legacy global-master pipeline.

## What it does

For each shot in `creative-specs/<id>.yaml`:

1. Reads `shot_NN` metadata (window, narration segments, SFX category context).
2. Loads visual: `assets/clips/<shot_id>.mp4` (Hailuo/Kling/Seedance render).
3. Resolves narration TTS segments whose `timestamp_intent_s` overlaps the shot window — loads `assets/tts/<segment_id>.mp3` per segment.
4. Resolves SFX events whose `start_s` falls in the shot window (from `cp5-audio-master.py` `SFX_EVENTS` or a JSON file).
5. Mixes per-clip audio: each source `adelay` to its local offset + `volume` scale + `amix=normalize=0` (canonical mix levels per Hard Rule #9).
6. Muxes video + composed audio → `<output-dir>/<shot_id>_atomic.mp4`.
7. (Optional) Overlays an AVU asset (countdown / decision-freeze / outro) with bundled audio.
8. Writes captions sidecar `<shot_id>_captions.json` (relative + global timing).
9. Writes audit manifest `<shot_id>_manifest.json` (LUFS, peak, duration delta, PASS/REVIEW verdict).

## Architecture rationale

Memory: `feedback_per_clip_atomic_assembly` (2026-05-20). The legacy pipeline builds a single 90s `master.mp3` then muxes with concatenated clips → drift compounds → end-of-timeline caption sync bugs (cinema-abandonado iter 1 "ELICHE", matadero iter 1 "QUE DAS CENA"). The atomic approach lets you verify sync per shot independently and concat clips that already carry their own audio.

Cross-clip layers (continuous ambient, music shifts) are applied AFTER the concat step — NOT in this script. This script only owns per-shot atomic units.

## Usage

### Single shot

```bash
.venv/bin/python scripts/build_clip_atomic.py \
  --spec ../creative-specs/cinema-abandonado.yaml \
  --shot-id shot_01_hook \
  --output-dir assets/clips-atomic/
```

### Single shot with AVU overlay

```bash
.venv/bin/python scripts/build_clip_atomic.py \
  --spec ../creative-specs/cinema-abandonado.yaml \
  --shot-id shot_01_hook \
  --avu countdown \
  --output-dir assets/clips-atomic/
```

Valid `--avu` values: `countdown`, `decision-freeze`, `hook-transition`, `outro-card`, `outro`.

Override AVU inject offset: `--avu-inject-s 6.0` (default = end-aligned).

### Batch (all shots in SPEC)

```bash
.venv/bin/python scripts/build_clip_atomic.py \
  --spec ../creative-specs/cinema-abandonado.yaml \
  --batch \
  --output-dir assets/clips-atomic/
```

Writes `_batch_manifest.json` summarizing all shots + audit verdicts + list of failures.

### Custom SFX source

By default the script auto-loads `<project_root>/scripts/cp5-audio-master.py` if it exists (extracts module-level `SFX_EVENTS` list of `(path, start_s, volume)` tuples).

Explicit override:

```bash
# Python module style (recommended for current project pattern)
--sfx-events scripts/cp5-audio-master.py

# JSON style (forward-canonical Phase 2+)
--sfx-events sfx-events.json
```

JSON schema:
```json
[
  {"path": "assets/sfx/footsteps.mp3", "start_s": 3.5, "volume": 0.22},
  {"path": "library/sfx/warm-cliffhanger/bird-distant-dawn.mp3", "start_s": 87.5, "volume": 0.30}
]
```

## Output files per shot

| File | Purpose |
|------|---------|
| `<shot_id>_atomic.mp4` | Self-contained video+audio. Ready for ffmpeg concat. |
| `<shot_id>_captions.json` | Caption sidecar with LOCAL (per-clip relative) + GLOBAL (SPEC absolute) timing. |
| `<shot_id>_manifest.json` | Audit: duration delta, LUFS, peak dB, audio sources count, audit_status PASS/REVIEW. |

## Manifest audit fields

```json
{
  "shot_id": "shot_01_hook",
  "spec_intent_duration_s": 9.0,
  "actual_duration_s": 9.0,
  "duration_delta_s": 0.0,
  "duration_ok": true,
  "audio": {
    "sources_count": 3,
    "narration_segments": ["hook_narrator_framing", "hook_salvador_warning"],
    "sfx_events_count": 2,
    "lufs_integrated": -28.5,
    "lufs_target": -14.0,
    "lufs_in_band": false,
    "peak_db": -8.8,
    "peak_ok": true
  },
  "audit_status": "REVIEW"
}
```

**Note on LUFS at this stage:** atomic clips intentionally measure *low* LUFS (typically -22 to -30) because music + continuous ambient are NOT yet layered in. The cross-clip post-concat layer + final `master-audio.sh` brings the assembly to -14 ±0.5 LUFS. The per-clip LUFS check is a sanity gate (audio is present + peak not clipping), not the final mastering target.

## Mix levels applied (Hard Rule #9)

| Source type | Default volume | Range |
|-------------|---------------|-------|
| Narration TTS | 1.0 | fixed |
| SFX event | 0.28 (per-event override allowed) | 0.20–0.35 |
| Flash impact | 0.60 | 0.55–0.65 |
| Ambient continuous | 0.14 | 0.10–0.18 (applied at concat layer, NOT here) |

Per-event volume comes from the SFX events source (`cp5-audio-master.py` tuple slot 3 or JSON `volume` field).

## Known limitations

- **No music layer per clip** — music is intentionally a cross-clip layer (handled post-concat).
- **No continuous ambient per clip** — applied post-concat as global underbed.
- **TTS naming mismatch handling** — if a narration segment ID doesn't have a matching `assets/tts/<id>.mp3`, the script logs `TTS MISSING` and skips it (clip builds with available audio only). Verify TTS asset naming matches SPEC segment IDs before running.
- **AVU overlay re-encodes video** — single-shot AVU mode uses x264 CRF 18 (visually transparent). Without `--avu` the script uses `-c:v copy` (no re-encode).

## Integration with next pipeline step (post-Phase 2)

After all atomic clips are built and PASS audit:

```bash
# Concat all atomic clips (sequential)
ffmpeg -f concat -safe 0 -i atomic-concat.txt -c copy assembled.mp4

# Then add cross-clip music + ambient layer
# Then run master-audio.sh assembled.mp4 → mastered.mp4
```

Concat list file format (one per line):
```
file 'shot_01_hook_atomic.mp4'
file 'shot_02_proyector_intro.mp4'
...
```

## Validation test case (executed 2026-05-20)

Tested against `cinema-abandonado` project:

- `shot_01_hook` with AVU countdown overlay → 9.00s output, h264+aac, LUFS=-23.31 (AVU ticks audio bundled).
- `shot_05_film_reveal` without AVU → 5.88s output, h264+aac, LUFS=-26.83 (no TTS — file naming mismatch reported correctly).

Both produced valid mp4 + captions sidecar + manifest. Verified streams: `h264` video + `aac 48000Hz stereo` audio.

## Related

- `master-audio.sh` — replaced for per-clip pipeline; still used as final master step post-concat.
- `cp5-audio-master.py` — legacy global master script; this script reads its `SFX_EVENTS` as source of truth.
- `audit-frames-granular.py` S11 — per-clip caption sync gate (Phase 2 amendment).
- Memory `feedback_per_clip_atomic_assembly` — architectural rationale.
- Hard Rules #9 + #15 + #16 — mix levels + HyperFrames timing.
