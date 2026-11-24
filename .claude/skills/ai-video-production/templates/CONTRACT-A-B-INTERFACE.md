# Contract Script A ↔ Script B — interface definition

> **Purpose**: prevent silent divergence between Script A (caption-burn per clip) and Script B (per-shot SPEC compliance audit). Define output of A + input of B + shared conventions BEFORE parallel build.
>
> **Author**: 🔍 Auditor (terminal 3) — pre-build contract.
> **Date**: 2026-05-21 PM late, pre-V4 enforcement scripts.
> **Status**: BINDING contract. Engineer A + Engineer B must respect this verbatim.

---

## 1. Script A output spec (exact)

### File format

```
Container:    MP4
Codec video:  h264 (yuv420p, fps preserved from input)
Codec audio:  AAC stereo 48kHz (preserved from input, -c:a copy)
Bit depth:    8-bit
Color space:  bt709
```

### Resolution

```
PRESERVE input clip resolution (NO upscale, NO downscale):
  - Hailuo Std input 768×1376 → output 768×1376
  - Hailuo Pro input 1080×1934 → output 1080×1934
  - Veo input 1080×1920 → output 1080×1920

Aspect ratio: 9:16 vertical (input preserved)
```

### Captions burned in frame data

**Caption presence**:
- IF Whisper detects speech in clip audio → captions BURNED into frame data (via ffmpeg drawtext)
- IF Whisper detects no speech (empty transcript) → NO captions burned, clip pass-through unchanged

**Caption position** (per Hard Rule #4):
```
Y position: 62% from top of frame (canonical safe zone)
X position: center horizontal (50%)
Wrap width: 80% of frame width
Alignment: center
```

**Caption styling** (per Hard Rule #4 + CHARACTER-NAMES-CATALOG):
```
Font family:
  - Narration class: canonical narration font (drop-shadow style, e.g., "Helvetica-Bold")
  - Warning class (red): same font, color override
  - Character name labels: monospaced (e.g., "Courier-Bold")

Font size:
  - ≤8 words per caption: 80px
  - >8 words: 68px

Color:
  - Narration: white (#FFFFFF) + drop shadow black 2px offset
  - Warning (red): #FF3333 + drop shadow black 2px offset
  - Character name: white (#FFFFFF) + drop shadow black 2px offset

Readability:
  - Drop-shadow only (NO thick stroke) — drop shadow > thick stroke (referent-validated)
```

**Caption text source priority**:
```
1. IF SPEC shot has text_canonical defined → use SPEC text but Whisper TIMING
2. ELSE → use Whisper transcribed text (raw, with any pronunciation artifacts)

Timing always from Whisper (NOT SPEC intent timestamps).
```

### Filename convention

```
Input filename:  shot_NN_<descriptor>.mp4 (e.g., shot_05_bryan_dialog.mp4)
Output filename: shot_NN_<descriptor>_atomic.mp4 (e.g., shot_05_bryan_dialog_atomic.mp4)

Output location: <project>/assets/clips-atomic/shot_NN_<descriptor>_atomic.mp4
```

### Sidecar JSON output (manifest)

Script A emits sidecar manifest per clip:

```yaml
# <project>/assets/clips-atomic/shot_NN_<descriptor>_manifest.yaml
shot_id: shot_05
input_path: assets/clips/shot_05_bryan_dialog.mp4
output_path: assets/clips-atomic/shot_05_bryan_dialog_atomic.mp4
caption_processing:
  whisper_detected_speech: true                    # bool
  whisper_raw_text: "El parque está cerrado..."    # full Whisper transcript
  whisper_segments: [...]                           # word-level timestamps
  spec_text_canonical: "El parque está cerrado..." # from SPEC if present
  spec_text_used: true                              # bool — was SPEC override applied
  captions_burned_count: 4                          # number of caption events burned
  caption_class_distribution:
    narration: 3
    warning: 1
    character_name: 0
clip_metadata:
  duration_s: 5.88
  width: 768
  height: 1376
  fps: 24
  codec_video: h264
  codec_audio: aac
  channels: 2
  sample_rate: 48000
processing:
  whisper_model: base
  whisper_language: es
  drawtext_filter: "<full ffmpeg drawtext command for reproducibility>"
timestamp: 2026-05-21T22:00:00Z
script_version: ai-video build-clip-atomic v1.1 (caption-burn extension)
```

---

## 2. Script B input spec (exact)

### What Script B reads

**Per shot to audit**:

1. **Atomic clip** (Script A's output):
   ```
   Path: <project>/assets/clips-atomic/shot_NN_<descriptor>_atomic.mp4
   Format: per Script A output spec (above)
   ```

2. **Atomic clip manifest** (Script A's sidecar):
   ```
   Path: <project>/assets/clips-atomic/shot_NN_<descriptor>_manifest.yaml
   Schema: per Script A output spec (above)
   Use for: whisper_raw_text reference, captions_burned_count check
   ```

3. **SPEC YAML**:
   ```
   Path: creative-specs/<project_id>.yaml (passed via --spec arg)
   Required fields per shot:
     - shot_list[N].shot_id
     - shot_list[N].narration_in_this_shot  (dim 1+2+3)
     - shot_list[N].visual_intent           (dim 4+5)
     - shot_list[N].scene_context.who_is_there  (dim 6)
     - shot_list[N].scene_context.who_does_what (dim 7)
   ```

4. **Anchors CP1** (for dim 6 character identity verification):
   ```
   Path: <project>/assets/anchors/char_*.png
   Use: Gemini Vision compare visible characters in clip frame vs anchor refs
   ```

### Script B assumptions about the clip

```
Script B EXPECTS:
  ✓ Clip exists at expected atomic path
  ✓ Clip has captions burned in frame (per Script A contract)
    → Script B extracts caption via Gemini Vision OCR on frame
  ✓ Clip audio preserved (per Script A contract)
    → Script B re-extracts audio + Whisper transcribe for dim 1
  ✓ Manifest YAML exists with whisper_raw_text + spec_text_used flag
  ✓ Resolution per atomic clip output spec

Script B does NOT:
  ✗ Modify the atomic clip
  ✗ Generate new captions
  ✗ Assume specific resolution (handles 768×1376 + 1080×1934 + 1080×1920)
```

### Script B output

```
Path: <project>/assets/clips-atomic/shot_NN_<descriptor>_audit.json

Schema:
{
  "shot_id": "shot_05",
  "atomic_clip_path": "...",
  "dim0_scope_creep": {
    "shot_in_spec": true,             # bool
    "pass": true
  },
  "dim1_narrator_says_spec": {
    "whisper_text": "...",
    "spec_text": "...",
    "jaccard_similarity": 0.85,
    "threshold": 0.7,
    "pass": true
  },
  "dim2_caption_shows_spec": {
    "caption_ocr_text": "...",
    "spec_text": "...",
    "jaccard_similarity": 0.92,
    "threshold": 0.7,
    "pass": true
  },
  "dim3_caption_matches_narrator": {
    "caption_text": "...",
    "narrator_text": "...",
    "jaccard_similarity": 0.88,
    "threshold": 0.7,
    "offset_s_estimated": 0.0,  # ⭐ critical for drift detection
    "pass": true
  },
  "dim4_5_visual_matches_intent": {
    "visual_description": "...",      # Gemini Vision describe
    "spec_visual_intent": "...",
    "similarity_score": 0.75,
    "threshold": 0.6,
    "pass": true
  },
  "dim6_characters_correct": {
    "expected_chars": ["char_a_mateo", "char_b_bryan"],
    "visible_chars": ["char_a_mateo", "char_b_bryan"],
    "anchor_similarity": {"char_a_mateo": 0.85, "char_b_bryan": 0.78},
    "threshold": 0.6,
    "pass": true
  },
  "dim7_action_matches_narration": {
    "spec_action": "...",
    "action_observed": "...",
    "similarity_score": 0.70,
    "threshold": 0.6,
    "pass": true
  },
  "overall_pass": true,
  "fail_dimensions": [],
  "warnings": []
}
```

---

## 3. Shared conventions

### Paths

```
Project root:        <project>/
Clips raw:           assets/clips/shot_NN_*.mp4 (from CP4 Hailuo)
Atomic clips:        assets/clips-atomic/shot_NN_*_atomic.mp4 (Script A output)
Atomic manifests:    assets/clips-atomic/shot_NN_*_manifest.yaml (Script A sidecar)
Audit reports:       assets/clips-atomic/shot_NN_*_audit.json (Script B output)
Anchors:             assets/anchors/char_*.png (from CP1)
SPEC:                creative-specs/<project_id>.yaml
```

### Naming convention

```
shot_NN_<descriptor>.mp4         — original Hailuo (input to Script A)
shot_NN_<descriptor>_atomic.mp4  — atomic with captions burned (Script A output)
shot_NN_<descriptor>_manifest.yaml — sidecar metadata
shot_NN_<descriptor>_audit.json  — Script B audit report

NN = 2-digit zero-padded shot number (01, 02, ..., 13)
<descriptor> = snake_case shot name from SPEC (e.g., bryan_dialog, mateo_offer)
```

### Error handling

```
Script A errors:
  - Input clip missing/corrupt: exit 1, print specific error
  - Whisper fails: exit 1, log error
  - ffmpeg drawtext fails: exit 1, preserve input clip unchanged
  - SPEC missing for shot: warning, fall back to Whisper raw text
  - Idempotent: re-run on same input produces identical output

Script B errors:
  - Atomic clip missing: exit 1 with "Run Script A first"
  - Manifest YAML missing: exit 1
  - SPEC missing: exit 1
  - Gemini Vision API fail: retry 3x exponential backoff, then exit 2 (transient)
  - Whisper fails: exit 1
  - Dim score parse error: emit FAIL with parsing details

Both scripts:
  - Logs to stderr, JSON output to stdout (so pipeable)
  - Exit codes: 0=success/all_pass, 1=hard error, 2=transient (retry), 3=NB warnings
```

### Whisper standard configuration (shared)

```python
import whisper
model = whisper.load_model('base')  # Both A + B use 'base' model
language = 'es'                       # Spanish always
word_timestamps = True                # For caption alignment + sync verify
```

### Gemini Vision standard configuration (shared)

```python
model = "gemini-3-flash-preview"      # Both use Flash (fast + cheap)
# For dim 4+5 visual descriptions: more rigorous
# For dim 2 caption OCR: lighter prompt
```

### Jaccard similarity (shared utility)

```python
def jaccard_similarity(text_a: str, text_b: str) -> float:
    """Word-level Jaccard similarity, case-insensitive, ignoring punctuation."""
    words_a = set(text_a.lower().split())  # normalize: strip punctuation first
    words_b = set(text_b.lower().split())
    if not words_a and not words_b:
        return 1.0
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)
```

Both scripts use this same function (place in `src/ai_video/core/similarity.py` shared).

---

## 4. Forward extensions (not in v1 — document for future)

```
v1.1: Script A handles speaker diarization for multi-character clips
v1.2: Script B adds dim 8: atmospheric motion count via Gemini Vision
v1.3: Both: support 4K resolution forward (Veo output upscaled)
```

---

## 5. Versioning

```
This contract: v1.0 (2026-05-21 PM late, pre-V4 build)

Changes require:
  - Bump version
  - Update both Script A + B
  - Re-run adversarial tests
  - Log in ARCHITECTURAL-DECISIONS.md
```

---

**Author**: 🔍 Auditor terminal 3
**Approved**: pre-build, binding for Engineers A + B
**Conflict resolution**: if A and B diverge from contract, AUDITOR has final say
