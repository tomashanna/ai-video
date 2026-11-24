# ai-video measure-canonical-decision-ui-pacing — Phase 1 priority spec

> **Status**: SPEC ONLY (script to be built post-matadero ship)
> **Trigger**: Hard Rule #19 EXPANSION 2026-05-18 ("NEVER ESTIMATE, ALWAYS MEASURE") + GAP #16 countdown duration USER-VALIDATED + GAP #21 per-segment WPM intra-speaker variance + canonical_validation_status pending_video_measurement flags in PAUTA-MASTER + INGENIERO-PAUTA + SPEC schema v8.
> **Owner**: 🛠️ Engineer Phase 1 implementation. Estimate 4-6h build + 7 refs run.

---

## 1. Purpose

Empirically measure canonical decision UI pacing parameters across 8 source videos (`/videosref_elige_tu_compa/*.MP4`) to FLIP `canonical_validation_status` from `pending_video_measurement` → `validated_via_video_measurement` for:

- `countdown_digit_duration_s` (currently architect interim 1.0s per user perceptual, was 0.7s broadcast standard)
- `countdown_pause_beat_s` (currently 0.3s inferred)
- `loading_bar_fill_duration_s` (currently 3.0s inferred per architect)
- `decision_filter_overlay_intensity` (sepia 0.4 + contrast 1.2 + hue-rotate 15deg)
- `ambient_duck_db_during_countdown` (-6 dB inferred)
- `per_segment_wpm_canonical_band` (NEW per GAP #21 — intra-speaker variance bands)

Plus identify additional empirical patterns observed but not yet codified.

---

## 2. Inputs

```yaml
sources:
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 00-01-36_1.MP4  # ref-03 bruno+pablo
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 00-07-06_1.MP4  # ref-06 axel+enzo
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-05-30_1.MP4  # ref-08 hugo+pablo
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-07-19_1.MP4  # ref-09 victor+axel
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-09-44_1.MP4  # ref-10 rurik+enzo
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-13-25_1.MP4  # ref-11 mario+ivan
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-22-41_1.MP4  # ref-12 nano+teresa
  - /videosref_elige_tu_compa/ScreenRecording_05-13-2026 11-25-03_1.MP4  # ref-13 miro+bryan
```

Per-ref existing data: `data/referent-analysis/ref-XX/metadata.json` + `transcription.json` + `ui-elements.json`.

---

## 3. Methodology

### 3.1 Decision window detection

```python
# Use existing canonical-scenes/ref-XX-frame-by-frame-events.json (when Phase 1 generates them)
# OR fallback: per-ref scene_cuts.txt + transcription.json identify hook + decision moments

# Hook countdown window: typically last 1-3s of first beat (4-7s timeline)
# Decision UI windows: typically 3-5s post setup_decision narration (D1/D2 moments)
```

### 3.2 Countdown digit duration measurement

```python
# For each detected countdown window:
# 1. Extract frames at 0.1s granularity
# 2. OCR each frame: identify digit "3", "2", "1", "0"
# 3. Detect digit transitions: t when "3" → "2" → "1" → "0/disappears"
# 4. digit_duration = transition_t[n+1] - transition_t[n]
# 5. Aggregate per-ref: list of digit_durations
# 6. Cross-canonical: median + p25/p75 bands

# Output:
# {
#   "countdown_digit_duration_s": {
#     "ref-03": [0.95, 1.02, 0.98],
#     "ref-06": [0.88, 0.92, 0.91],
#     ...
#     "aggregate": {"median": 0.97, "p25": 0.92, "p75": 1.02}
#   }
# }
```

### 3.3 Pause beat measurement (narration_end → countdown_start)

```python
# 1. From transcription.json, find narrator segment end timestamp before countdown window
# 2. From OCR/frame detection, find countdown first digit "3" appear timestamp
# 3. pause_beat = countdown_start - narration_end
# 4. Aggregate per-ref + cross-canonical
```

### 3.4 Filter overlay detection (SSIM + color histogram)

```python
# 1. Sample frame BEFORE decision window (no filter applied)
# 2. Sample frame DURING decision window (filter applied)
# 3. Compute color histogram diff between pre/during frames
# 4. Detect dominant shift (sepia/grain/chromatic-aberration/scan-lines)
# 5. Quantify intensity via SSIM degradation + histogram delta
# 6. Output: filter_type + intensity per ref

# Possible filters detected:
# - sepia (warm tint shift toward yellow/brown)
# - grain (noise increase via local variance)
# - chromatic-aberration (R/G/B channel separation)
# - scan-lines (vertical/horizontal line patterns)
# - VHS (combination of above)
```

### 3.5 Freeze frame detection (SSIM consecutive frames)

```python
# 1. Sample 10 frames at 0.1s intervals during decision window
# 2. Compute SSIM between consecutive frames
# 3. If SSIM > 0.98 for >2s consecutive → freeze frame confirmed
# 4. Output: freeze_frame_applied (bool) + freeze_duration_s
```

### 3.6 Loading bar fill duration measurement

```python
# 1. Identify loading bar bounding box via OCR/template matching
# 2. Track fill percentage (visible fill width) across frames
# 3. Measure t_0% (appear) → t_100% (full)
# 4. loading_fill_duration = t_100% - t_0%
# 5. Compare vs countdown_total_duration (should match per canonical)
```

### 3.7 Ambient audio duck measurement

```python
# 1. ffmpeg extract audio + librosa loudness analysis
# 2. Compute RMS dB pre-decision_window vs during-decision_window
# 3. duck_db = RMS_during - RMS_pre
# 4. Cross-canonical aggregate
```

### 3.8 Per-segment WPM canonical bands (GAP #21 NEW)

```python
# Per ref, per narrator segment in transcription.json:
# 1. wpm_seg = words / segment_duration * 60
# 2. Categorize by segment role:
#    - hook_framing
#    - setup_establishing
#    - decision_setup
#    - consequence_narration
#    - cliffhanger
#    - climax_staccato
# 3. Aggregate per-role: median + p25/p75
# 4. Identify acceptable variance per role (e.g., climax_staccato may exceed 200 WPM)

# Output:
# {
#   "per_segment_wpm_canonical_bands": {
#     "hook_framing": {"median": 165, "p25": 152, "p75": 180},
#     "decision_setup": {"median": 170, "p25": 160, "p75": 185},
#     "climax_staccato": {"median": 220, "p25": 200, "p75": 250},
#     ...
#   }
# }
```

---

## 4. Outputs

### 4.1 Per-ref measurements JSON

```
data/referent-analysis/empirical-decision-ui-pacing/
├── ref-03-measurements.json
├── ref-06-measurements.json
├── ref-08-measurements.json
├── ref-09-measurements.json
├── ref-10-measurements.json
├── ref-11-measurements.json
├── ref-12-measurements.json
├── ref-13-measurements.json
└── aggregate-canonical-bands.json  # cross-ref empirical bands
```

### 4.2 Aggregate canonical bands schema

```json
{
  "schema_version": "v1",
  "extraction_date": "2026-05-XX",
  "source_refs": ["ref-03", "ref-06", ...],
  "params": {
    "countdown_digit_duration_s": {"median": 0.97, "p25": 0.92, "p75": 1.02, "n_samples": 24},
    "countdown_pause_beat_s": {"median": 0.32, "p25": 0.25, "p75": 0.38, "n_samples": 8},
    "loading_bar_fill_duration_s": {"median": 3.0, "p25": 2.8, "p75": 3.2, "n_samples": 8},
    "decision_filter_overlay_type": "sepia_grain_dominant",  # categorical winner
    "decision_filter_overlay_intensity": {"median": 0.45, "p25": 0.35, "p75": 0.55},
    "ambient_duck_db_during_countdown": {"median": -6.2, "p25": -7.5, "p75": -4.8, "n_samples": 8},
    "freeze_frame_applied": {"pct_refs_with_freeze": 0.875, "median_duration_s": 2.1},
    "per_segment_wpm_bands": {
      "hook_framing": {"median": 165, "p25": 152, "p75": 180},
      "setup_establishing": {"median": 170, "p25": 158, "p75": 185},
      "decision_setup": {"median": 175, "p25": 165, "p75": 188},
      "consequence_narration": {"median": 170, "p25": 158, "p75": 182},
      "cliffhanger": {"median": 160, "p25": 145, "p75": 178},
      "climax_staccato": {"median": 220, "p25": 195, "p75": 250}
    }
  }
}
```

### 4.3 Cross-codification updates post-script

When script runs successfully, auto-update OR manual review:

| Doc | Field to update | Current value | Action |
|-----|----------------|---------------|--------|
| `INGENIERO-PAUTA § 7.10` | `countdown_digit_duration_s` | 1.0 (user perceptual validated) | Replace with measured median |
| `INGENIERO-PAUTA § 7.10` | `countdown_pause_beat_s` | 0.3 inferred | Replace with measured |
| `PAUTA-MASTER § 18` | freeze_frame canonical % | "observed in 2/6 refs" (WRONG) | Replace with measured pct + samples |
| `PAUTA-MASTER § 18` | filter_overlay_type | "VHS sepia grain" inferred | Replace with measured dominant |
| `CREATIVE-SPEC-TEMPLATE v8` | All `narrative_pacing.*` fields | `canonical_validation_status: pending_video_measurement` | Flip to `validated_via_video_measurement` + add `validated_at` + reference aggregate JSON |
| `AUDITOR-PROTOCOL § 3 CP2 M7.6.5` | `per_segment_wpm_bands` | inferred 152-180 single band | Replace with per-role measured bands |

---

## 5. Dependencies

```python
# requirements.txt additions:
# librosa>=0.10  # audio analysis loudness/duck
# scikit-image>=0.21  # SSIM
# pytesseract>=0.3  # OCR digit detection (alternative: paddleocr)
# opencv-python>=4.8  # frame extraction + histogram

# Existing:
# openai-whisper  # transcription (already used)
# ffmpeg-python  # video processing (already used)
```

---

## 6. Build estimate

| Phase | Time | Owner |
|-------|------|-------|
| Initial implementation (countdown digit + pause beat + freeze detection) | 2h | Engineer |
| Filter overlay detection (color histogram + SSIM) | 1.5h | Engineer |
| Audio duck measurement (librosa) | 1h | Engineer |
| Per-segment WPM bands (GAP #21) | 1h | Engineer |
| Test on ref-13 (pilot) | 0.5h | Engineer |
| Run on all 8 refs + aggregate | 0.5h | Engineer |
| Auditor verify outputs vs my visual frame extracts | 1h | Auditor |
| Architect update codification per measurements | 1h | Architect |
| **Total** | **8h** | Multi-role |

Cost: **$0** (no API calls — all local ffmpeg + Whisper + librosa).

---

## 7. Acceptance criteria

✅ All 8 refs processed without errors
✅ Aggregate JSON generated con median + p25/p75 per param
✅ Per-segment WPM bands per role (GAP #21)
✅ Cross-codification updates applied (≥6 amendments per Section 4.3)
✅ `canonical_validation_status` flipped pending → validated_via_video_measurement on all affected fields
✅ Auditor independent verify (sample 2-3 refs frame extract vs measured values within ±5% tolerance)

---

## 8. Forward Phase 2 enhancements

After base script works:
- Add motion velocity per shot_type measurement (GAP #11 closure)
- Add ambient/SFX category-specific volume canonical bands (GAP #17 closure)
- Add character intro pose pattern detection (PAUTA § 5)
- Add cliffhanger archetype acoustic signature (music BPM + drone vs warm waltz)

---

**Última actualización**: 2026-05-19 PM late (auditor spec'd post matadero iter 7 in flight)
**Next**: Engineer Phase 1 implementation post-matadero ship
