#!/usr/bin/env python3
"""
audit-shot-spec-compliance.py — per-shot SPEC contract verifier (Script B).

Verifies each shot atomic clip vs SPEC across 8 dimensions:

  dim 0 — Scope creep detection (shot exists in BOTH filesystem AND SPEC)
  dim 1 — Narrator says SPEC.narration_in_this_shot (Whisper transcript vs SPEC)
  dim 2 — Caption shows SPEC.narration_in_this_shot (Gemini OCR vs SPEC)
  dim 3 — Caption matches narrator (sync check, includes offset_s estimate)
  dim 4+5 — Visual matches SPEC.visual_intent (Gemini Vision describe)
  dim 6 — Characters expected vs visible (anchor identity check)
  dim 7 — Action matches SPEC.scene_context.who_does_what (3-keyframe sequence)

Thresholds (per CONTRACT-A-B-INTERFACE.md):
  - text dims (1,2,3): jaccard ≥ 0.7
  - visual dims (4+5, 6, 7): similarity ≥ 0.6
  - sync offset (dim 3): |offset_s| ≤ 1.5s

Usage (single shot):
    python audit-shot-spec-compliance.py \\
        --spec creative-specs/<id>.yaml \\
        --shot-id shot_05 \\
        --atomic-clip-path assets/clips-atomic/shot_05_atomic.mp4 \\
        --anchors-dir assets/anchors/ \\
        --output assets/clips-atomic/shot_05_audit.json

Usage (batch all shots):
    python audit-shot-spec-compliance.py \\
        --spec creative-specs/<id>.yaml \\
        --atomic-dir assets/clips-atomic/ \\
        --anchors-dir assets/anchors/ \\
        --batch

Exit codes:
  0 — all audited shots PASS overall
  1 — at least one shot FAIL or hard error
  2 — transient (Gemini Vision API fail after retries)
  3 — warnings only (e.g., missing optional fields)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    import google.genai as genai  # noqa: F401  (fail fast if the extra is missing)
except ImportError:
    print(
        "ERROR: missing deps. Run: uv sync --extra providers --extra media",
        file=sys.stderr,
    )
    sys.exit(2)

try:
    import whisper as openai_whisper
except ImportError:
    print("ERROR: openai-whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
    sys.exit(2)

from ai_video.core.similarity import estimate_text_offset_s, jaccard_similarity

# ─────────────────────────────────────────────────────────────────────────────
# Config (per CONTRACT v1.0)
# ─────────────────────────────────────────────────────────────────────────────
GEMINI_MODEL = "gemini-3-flash-preview"
WHISPER_MODEL = "base"
WHISPER_LANG = "es"
TEXT_THRESHOLD = 0.7
VISUAL_THRESHOLD = 0.6
OFFSET_THRESHOLD_S = 1.5

_WHISPER_MODEL_CACHE = None


def get_whisper_model():
    global _WHISPER_MODEL_CACHE
    if _WHISPER_MODEL_CACHE is None:
        print(f"  Loading Whisper model={WHISPER_MODEL}...", file=sys.stderr)
        _WHISPER_MODEL_CACHE = openai_whisper.load_model(WHISPER_MODEL)
    return _WHISPER_MODEL_CACHE


# ─────────────────────────────────────────────────────────────────────────────
# Utilities — ffmpeg / Whisper / Gemini
# ─────────────────────────────────────────────────────────────────────────────


def ffprobe_duration(video_path: str) -> float:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                video_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def extract_audio(video_path: str, out_wav: str) -> bool:
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                video_path,
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-c:a",
                "pcm_s16le",
                out_wav,
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        return os.path.exists(out_wav)
    except Exception as e:
        print(f"  ERROR extracting audio: {e}", file=sys.stderr)
        return False


def extract_frame(video_path: str, t: float, out_png: str) -> bool:
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                str(t),
                "-i",
                video_path,
                "-frames:v",
                "1",
                "-q:v",
                "2",
                out_png,
            ],
            check=False,
            capture_output=True,
            timeout=30,
        )
        return os.path.exists(out_png) and os.path.getsize(out_png) > 1000
    except Exception:
        return False


def whisper_transcribe(audio_wav: str) -> dict:
    """Return {'text': str, 'segments': [...]} (or empty if silent/no speech)."""
    if not os.path.exists(audio_wav) or os.path.getsize(audio_wav) < 1024:
        return {"text": "", "segments": []}
    try:
        model = get_whisper_model()
        result = model.transcribe(
            audio_wav,
            language=WHISPER_LANG,
            word_timestamps=True,
            verbose=False,
            fp16=False,
        )
        return {
            "text": result.get("text", "").strip(),
            "segments": result.get("segments", []),
        }
    except Exception as e:
        print(f"  ERROR whisper transcribe: {e}", file=sys.stderr)
        return {"text": "", "segments": []}


def gemini_call(client, prompt: str, image_paths: list, retries: int = 3) -> str:
    """Call Gemini Vision with text prompt + images. Retry on transient errors."""
    parts = [{"text": prompt}]
    for p in image_paths:
        try:
            with open(p, "rb") as f:
                parts.append(
                    {
                        "inline_data": {"mime_type": "image/png", "data": f.read()},
                    }
                )
        except Exception as e:
            print(f"  WARN failed to load image {p}: {e}", file=sys.stderr)

    last_err = None
    for attempt in range(retries):
        try:
            r = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[{"role": "user", "parts": parts}],
            )
            return (r.text or "").strip()
        except Exception as e:
            last_err = e
            wait = 2**attempt
            print(
                f"  Gemini call attempt {attempt + 1}/{retries} failed: {e}; retry in {wait}s",
                file=sys.stderr,
            )
            time.sleep(wait)
    raise RuntimeError(f"Gemini call failed after {retries} attempts: {last_err}")


# ─────────────────────────────────────────────────────────────────────────────
# Gemini prompts (small + focused per dim)
# ─────────────────────────────────────────────────────────────────────────────

PROMPT_OCR_CAPTION = """You are an OCR extractor for a vertical video frame.

TASK: extract ONLY the burned-in caption text (large text overlay typically at lower-middle of frame, ~60% from top, white or red, bold, with drop shadow). IGNORE: small UI labels, character name labels at top, watermarks, mascot/sign text in the scene itself.

If NO caption text is visible (frame has no caption overlay) → respond exactly: ABSENT
If caption visible → respond EXACTLY the caption text on a single line, no quotes, no extras.

Examples:
  → ELIGE TU COMPAÑERO
  → El parque está cerrado por una razón.
  → ABSENT
"""

PROMPT_OCR_CAPTION_BBOX = """You are an OCR extractor for a vertical video frame.

TASK: extract ONLY the burned-in caption text overlay (typically large bold text, white or red, with drop shadow, located in the lower-middle band of the frame). Ignore any other text (character name labels at top, watermarks, mascot signage in the scene itself, UI elements, loading bars).

Respond on FIRST LINE with EXACTLY one of:
  CAPTION: <text>     — if a caption text overlay is visible
  ABSENT              — if no caption overlay is visible

Optional SECOND LINE (only if CAPTION):
  Y_RATIO: <0.0-1.0>  — approximate vertical position of caption (0.0=top, 1.0=bottom)
"""

PROMPT_DESCRIBE_VISUAL = """You are a visual scene describer for video QA.

TASK: in 2-3 SHORT factual sentences, describe what is VISUALLY in this frame:
  - subjects (characters, objects, props)
  - setting (location, time of day, lighting)
  - composition (POV, shot type, framing)

Be concrete. NO speculation, NO interpretation, NO emotional adjectives.
NO mention of captions/UI overlays — only the underlying scene.

Output: 2-3 sentences plain text only.
"""

PROMPT_COMPARE_VISUAL = """You are a visual semantics evaluator.

You will receive TWO descriptions:
  A: SPEC visual intent (what the shot SHOULD look like)
  B: Observed visual description (what is ACTUALLY in the frame)

TASK: rate how well B matches A semantically, on a 0.0–1.0 scale.
  1.0 = matches every key element (subjects, setting, action, composition)
  0.7 = matches main subjects + setting, minor differences in details
  0.5 = matches some elements but key items missing
  0.3 = wrong subjects or wrong setting
  0.0 = completely unrelated

Respond ONLY with a single line:
  SCORE: <0.0-1.0>
  REASON: <one short sentence>
"""

PROMPT_IDENTIFY_CHARACTERS = """You are a character detector.

TASK: identify which characters are visible in this video frame.
Output a list of character labels using these EXACT codes if matching:
  - char_a_mateo : purple frog mascot suit, friendly/familiar look
  - char_a       : same as above (synonym)
  - char_b_bryan : human lifeguard, sun-weathered, tank top, holding flashlight
  - char_b       : same as above (synonym)
  - viewer_pov   : ONLY use if first-person POV hands or body parts of the viewer are visible
  - other        : any other person/character not matching above

Respond with ONE line:
  CHARS: <comma-separated list>
  (or CHARS: none if no characters visible)

Examples:
  CHARS: char_a_mateo, char_b_bryan
  CHARS: char_b_bryan
  CHARS: none
"""

PROMPT_COMPARE_ANCHOR = """You are an identity-match evaluator.

You will receive TWO images:
  IMAGE 1: anchor reference (canonical look of a character)
  IMAGE 2: a frame from a video clip

TASK: rate how well the character in IMAGE 2 visually matches the anchor in IMAGE 1 on a 0.0–1.0 scale.
Focus on: clothing/costume, build, color palette, distinguishing props (flashlight, frog suit, etc.).
Allow normal pose / angle differences — only penalize true identity divergence.

  1.0 = same character, very high confidence
  0.7 = same character, with normal pose/lighting variance
  0.5 = ambiguous — could be same or different
  0.3 = likely different character
  0.0 = clearly different character or character not visible

Respond ONLY with:
  SCORE: <0.0-1.0>
  REASON: <one short sentence>
"""

PROMPT_DESCRIBE_ACTION_SEQUENCE = """You are an action sequence describer for a video shot.

You will receive THREE keyframes from the SAME shot in order: START, MIDDLE, END.

TASK: in 2-3 short factual sentences, describe the ACTION/MOTION that happens across these frames (what characters do, how POV moves, what changes between frames). Focus on motion + change, NOT static descriptions.

NO speculation, NO mention of captions/UI. Plain text only.
"""

PROMPT_COMPARE_ACTION = """You are a visual semantics evaluator.

You will receive TWO descriptions:
  A: SPEC scene_context.who_does_what (what SHOULD happen)
  B: Observed action sequence (what ACTUALLY happens)

TASK: rate how well B matches A on a 0.0–1.0 scale. Focus on:
  - WHO acts (correct character)
  - WHAT they do (correct verb/action)
  - HOW (correct direction, manner)

  1.0 = matches every key action
  0.7 = main action matches, minor differences
  0.5 = some action matches, key items missing
  0.3 = wrong action or wrong character
  0.0 = unrelated

Respond ONLY with:
  SCORE: <0.0-1.0>
  REASON: <one short sentence>
"""


def parse_score(response_text: str) -> tuple[float, str]:
    """Parse 'SCORE: X.XX / REASON: ...' format. Returns (score, reason)."""
    score = 0.0
    reason = ""
    for line in response_text.splitlines():
        line = line.strip()
        m = re.match(r"^SCORE:\s*([0-9.]+)", line, re.IGNORECASE)
        if m:
            try:
                score = float(m.group(1))
                score = max(0.0, min(1.0, score))
            except ValueError:
                pass
        m = re.match(r"^REASON:\s*(.*)", line, re.IGNORECASE)
        if m:
            reason = m.group(1).strip()
    return score, reason


def parse_chars(response_text: str) -> list:
    """Parse 'CHARS: a, b, c' format → list of normalized char codes."""
    for line in response_text.splitlines():
        line = line.strip()
        m = re.match(r"^CHARS:\s*(.*)", line, re.IGNORECASE)
        if m:
            payload = m.group(1).strip()
            if payload.lower() in ("none", "", "ninguno"):
                return []
            items = [c.strip().lower() for c in payload.split(",") if c.strip()]
            return _normalize_char_codes(items)
    return []


def _normalize_char_codes(items: list) -> list:
    """Map gemini outputs to canonical char_a/char_b/viewer_pov/other set."""
    out = []
    for it in items:
        it = it.strip().lower()
        if it in ("char_a", "char_a_mateo", "mateo"):
            out.append("char_a")
        elif it in ("char_b", "char_b_bryan", "bryan"):
            out.append("char_b")
        elif it in ("viewer_pov", "pov", "viewer"):
            out.append("viewer_pov")
        elif it:
            out.append("other")
    # dedupe preserving order
    seen = set()
    uniq = []
    for c in out:
        if c not in seen:
            uniq.append(c)
            seen.add(c)
    return uniq


def parse_caption_ocr(response_text: str) -> tuple[str | None, float | None]:
    """Parse OCR response. Returns (text or None for ABSENT, optional Y ratio)."""
    text = None
    y_ratio = None
    body = response_text.strip()
    if not body:
        return None, None
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    if not lines:
        return None, None
    first = lines[0]
    if first.upper().startswith("ABSENT") or first.upper() == "ABSENT":
        text = None
    elif first.upper().startswith("CAPTION:"):
        text = first[len("CAPTION:") :].strip() or None
    else:
        # fallback: treat first non-empty line as caption (legacy prompt path)
        if first.upper() == "NONE":
            text = None
        else:
            text = first
    for line in lines[1:]:
        m = re.match(r"^Y_RATIO:\s*([0-9.]+)", line, re.IGNORECASE)
        if m:
            try:
                y_ratio = float(m.group(1))
            except ValueError:
                pass
    return text, y_ratio


# ─────────────────────────────────────────────────────────────────────────────
# SPEC loader
# ─────────────────────────────────────────────────────────────────────────────


def load_spec(spec_path: str) -> dict:
    with open(spec_path) as f:
        return yaml.safe_load(f)


def get_shot_list(spec: dict) -> list:
    sl = spec.get("shot_list", [])
    if isinstance(sl, dict):
        return sl.get("shots", []) or []
    return sl if isinstance(sl, list) else []


def find_shot_in_spec(spec: dict, shot_id: str) -> dict | None:
    for s in get_shot_list(spec):
        if s.get("shot_id") == shot_id:
            return s
    return None


def find_canonical_text_for_shot(spec: dict, shot_id: str) -> str | None:
    """SPEC.shot_list[N].narration_in_this_shot may say '(silent — character speaks)';
    in that case the actual on-screen text comes from narration_script / asset_list
    where text_canonical is paired with shot_id_anchor=<shot_id>.

    Returns the most specific narration text expected for the shot."""
    # 1. shot's own field
    shot = find_shot_in_spec(spec, shot_id)
    if shot:
        direct = shot.get("narration_in_this_shot")
        if direct and not _is_silent_marker(direct):
            return direct.strip()

    # 2. asset_list narration items with shot_id_anchor == shot_id
    asset_list = spec.get("asset_list", {}) or {}
    if isinstance(asset_list, dict):
        candidates = []
        for key in ("narration", "narrations", "tts", "captions"):
            items = asset_list.get(key, []) or []
            if isinstance(items, list):
                candidates.extend(items)
        # also a flat list?
        for v in asset_list.values():
            if isinstance(v, list):
                for it in v:
                    if isinstance(it, dict) and it.get("shot_id_anchor") == shot_id:
                        tc = it.get("text_canonical")
                        if tc:
                            return tc.strip()

    # search all top-level lists too (some SPECs nest differently)
    def _walk(node):
        if isinstance(node, dict):
            if node.get("shot_id_anchor") == shot_id and node.get("text_canonical"):
                return node["text_canonical"].strip()
            for v in node.values():
                r = _walk(v)
                if r:
                    return r
        elif isinstance(node, list):
            for v in node:
                r = _walk(v)
                if r:
                    return r
        return None

    walked = _walk(spec)
    if walked:
        return walked

    # 3. fallback: return whatever was in narration_in_this_shot (possibly silent marker)
    if shot:
        return (shot.get("narration_in_this_shot") or "").strip() or None
    return None


def _is_silent_marker(text: str) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return (
        t.startswith("(silent")
        or t.startswith("(no narration")
        or t == "silent"
        or "silent — character speaks" in t
        or "no narration" in t
    )


# ─────────────────────────────────────────────────────────────────────────────
# Dimension verifiers
# ─────────────────────────────────────────────────────────────────────────────


def verify_dim0_scope_creep(shot_id: str, shot_in_spec: bool, clip_exists: bool) -> dict:
    """Shot exists in BOTH filesystem and SPEC?"""
    if shot_in_spec and clip_exists:
        return {
            "shot_in_spec": True,
            "clip_exists": True,
            "pass": True,
            "reason": "Shot exists in SPEC and filesystem",
        }
    if not shot_in_spec and clip_exists:
        return {
            "shot_in_spec": False,
            "clip_exists": True,
            "pass": False,
            "reason": "SCOPE CREEP: clip exists in filesystem but NOT in SPEC",
        }
    if shot_in_spec and not clip_exists:
        return {
            "shot_in_spec": True,
            "clip_exists": False,
            "pass": False,
            "reason": "Clip missing in filesystem (SPEC declares it)",
        }
    return {
        "shot_in_spec": False,
        "clip_exists": False,
        "pass": False,
        "reason": "Shot in neither SPEC nor filesystem",
    }


def verify_dim1_narrator(whisper_text: str, spec_text: str) -> dict:
    if _is_silent_marker(spec_text):
        # Shot is intentionally silent (on-screen character dialog only) — narration source is dialog audio.
        # Whisper will still capture some speech. We treat as N/A (skip pass/fail).
        return {
            "whisper_text": whisper_text,
            "spec_text": spec_text,
            "jaccard_similarity": None,
            "threshold": TEXT_THRESHOLD,
            "pass": True,
            "skipped": True,
            "reason": "SPEC marks this shot as silent (on-screen character dialog); narrator content check N/A",
        }
    sim = jaccard_similarity(whisper_text, spec_text)
    return {
        "whisper_text": whisper_text,
        "spec_text": spec_text,
        "jaccard_similarity": round(sim, 3),
        "threshold": TEXT_THRESHOLD,
        "pass": sim >= TEXT_THRESHOLD,
    }


def verify_dim2_caption(caption_ocr_text: str | None, spec_text: str) -> dict:
    if _is_silent_marker(spec_text):
        # On-screen-dialog shots may have caption from character speech; we expect SOMETHING but not the silent marker.
        return {
            "caption_ocr_text": caption_ocr_text,
            "spec_text": spec_text,
            "jaccard_similarity": None,
            "threshold": TEXT_THRESHOLD,
            "pass": True,
            "skipped": True,
            "reason": "SPEC marks shot silent; caption content check N/A",
        }
    if caption_ocr_text is None:
        return {
            "caption_ocr_text": None,
            "spec_text": spec_text,
            "jaccard_similarity": 0.0,
            "threshold": TEXT_THRESHOLD,
            "pass": False,
            "reason": "Caption ABSENT during this shot (expected SPEC text not visible)",
        }
    sim = jaccard_similarity(caption_ocr_text, spec_text)
    return {
        "caption_ocr_text": caption_ocr_text,
        "spec_text": spec_text,
        "jaccard_similarity": round(sim, 3),
        "threshold": TEXT_THRESHOLD,
        "pass": sim >= TEXT_THRESHOLD,
    }


def verify_dim3_caption_vs_narrator(
    caption_text: str | None,
    narrator_text: str,
    caption_appears_at_s: float | None,
    whisper_segments: list,
) -> dict:
    if caption_text is None and not narrator_text:
        return {
            "caption_text": None,
            "narrator_text": "",
            "jaccard_similarity": 1.0,
            "offset_s_estimated": None,
            "threshold": TEXT_THRESHOLD,
            "pass": True,
            "skipped": True,
            "reason": "Both caption and narrator empty (silent shot)",
        }
    if caption_text is None:
        return {
            "caption_text": None,
            "narrator_text": narrator_text,
            "jaccard_similarity": 0.0,
            "offset_s_estimated": None,
            "threshold": TEXT_THRESHOLD,
            "pass": False,
            "reason": "Caption ABSENT but narrator speaks — sync broken (caption missing)",
        }
    sim = jaccard_similarity(caption_text, narrator_text)
    offset_s = estimate_text_offset_s(whisper_segments, caption_text, caption_appears_at_s)
    sync_ok = bool(sim >= TEXT_THRESHOLD and (offset_s is None or abs(offset_s) <= OFFSET_THRESHOLD_S))
    return {
        "caption_text": caption_text,
        "narrator_text": narrator_text,
        "jaccard_similarity": round(float(sim), 3),
        "offset_s_estimated": round(float(offset_s), 2) if offset_s is not None else None,
        "threshold": TEXT_THRESHOLD,
        "offset_threshold_s": OFFSET_THRESHOLD_S,
        "pass": sync_ok,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main audit per shot
# ─────────────────────────────────────────────────────────────────────────────


def audit_shot(
    client,
    shot_id: str,
    atomic_clip_path: str,
    spec: dict,
    anchors_dir: str | None,
    workdir: str,
    shot_in_spec: bool = True,
) -> dict:
    """Run all 8 dimensions on one shot. Returns audit JSON dict."""
    print(f"\n━━━ {shot_id} ━━━", file=sys.stderr)

    result = {
        "shot_id": shot_id,
        "atomic_clip_path": str(atomic_clip_path),
        "gemini_model": GEMINI_MODEL,
        "whisper_model": WHISPER_MODEL,
    }
    warnings = []

    clip_exists = os.path.exists(atomic_clip_path) and os.path.getsize(atomic_clip_path) > 1024

    # ── dim 0 ── scope creep
    result["dim0_scope_creep"] = verify_dim0_scope_creep(shot_id, shot_in_spec, clip_exists)
    print(
        f"  dim0 scope_creep: {'PASS' if result['dim0_scope_creep']['pass'] else 'FAIL'} — {result['dim0_scope_creep']['reason']}",
        file=sys.stderr,
    )

    if not clip_exists:
        # cannot run other dims, return early
        result["overall_pass"] = False
        result["fail_dimensions"] = ["dim0"]
        result["warnings"] = ["clip missing — only dim0 evaluated"]
        return result

    # Determine SPEC expected fields
    shot = find_shot_in_spec(spec, shot_id) or {}
    spec_narration = find_canonical_text_for_shot(spec, shot_id) or ""
    spec_visual = (shot.get("visual_intent") or "").strip()
    scene_context = shot.get("scene_context", {}) or {}
    spec_who_is_there = scene_context.get("who_is_there", []) or []
    spec_who_does_what = (scene_context.get("who_does_what") or "").strip()

    # Normalize expected chars (drop viewer_pov from comparison since first-person POV is invisible)
    expected_chars_raw = _normalize_char_codes(spec_who_is_there)
    expected_chars_visible = [c for c in expected_chars_raw if c != "viewer_pov"]

    # ── Whisper transcribe full clip audio ──
    audio_wav = os.path.join(workdir, f"{shot_id}_audio.wav")
    print("  Extracting audio → Whisper...", file=sys.stderr)
    have_audio = extract_audio(atomic_clip_path, audio_wav)
    whisper_out = whisper_transcribe(audio_wav) if have_audio else {"text": "", "segments": []}
    whisper_text = whisper_out["text"]
    whisper_segments = whisper_out["segments"]
    print(f"    Whisper text: {whisper_text[:80]}", file=sys.stderr)

    duration_s = ffprobe_duration(atomic_clip_path)
    if duration_s <= 0:
        warnings.append("Could not probe clip duration; defaulting frame extraction to t=1.0s")
        duration_s = 2.5

    # ── Extract keyframes ──
    t_start = max(0.1, duration_s * 0.15)
    t_mid = max(0.5, duration_s * 0.5)
    t_end = max(1.0, duration_s * 0.85)
    frame_start = os.path.join(workdir, f"{shot_id}_start.png")
    frame_mid = os.path.join(workdir, f"{shot_id}_mid.png")
    frame_end = os.path.join(workdir, f"{shot_id}_end.png")
    extract_frame(atomic_clip_path, t_start, frame_start)
    extract_frame(atomic_clip_path, t_mid, frame_mid)
    extract_frame(atomic_clip_path, t_end, frame_end)

    # ── Scan multiple frames for caption (dim 2): if narrator says X but caption first appears late, capture appearance time ──
    caption_text_by_t = {}
    scan_times = [t_start, t_mid, t_end]
    for tt, fp in zip(scan_times, [frame_start, frame_mid, frame_end]):
        if not os.path.exists(fp):
            continue
        try:
            resp = gemini_call(client, PROMPT_OCR_CAPTION_BBOX, [fp])
            ctext, _ = parse_caption_ocr(resp)
            caption_text_by_t[tt] = ctext
        except Exception as e:
            warnings.append(f"OCR failed at t={tt:.2f}: {e}")
            caption_text_by_t[tt] = None

    # primary caption text = best non-empty from mid → end → start
    caption_priority = [
        caption_text_by_t.get(t_mid),
        caption_text_by_t.get(t_end),
        caption_text_by_t.get(t_start),
    ]
    primary_caption = next((c for c in caption_priority if c), None)

    # estimate caption appears_at_s = earliest scan time where caption text non-empty
    caption_appears_at_s = None
    for tt in scan_times:
        if caption_text_by_t.get(tt):
            caption_appears_at_s = tt
            break

    # ── dim 1 ── narrator says SPEC
    result["dim1_narrator_says_spec"] = verify_dim1_narrator(whisper_text, spec_narration)
    print(f"  dim1 narrator: {_fmt_pass(result['dim1_narrator_says_spec'])}", file=sys.stderr)

    # ── dim 2 ── caption shows SPEC
    result["dim2_caption_shows_spec"] = verify_dim2_caption(primary_caption, spec_narration)
    result["dim2_caption_shows_spec"]["caption_scan_per_frame"] = {
        f"{tt:.2f}s": c for tt, c in caption_text_by_t.items()
    }
    print(f"  dim2 caption_vs_spec: {_fmt_pass(result['dim2_caption_shows_spec'])}", file=sys.stderr)

    # ── dim 3 ── caption matches narrator + offset
    result["dim3_caption_matches_narrator"] = verify_dim3_caption_vs_narrator(
        primary_caption,
        whisper_text,
        caption_appears_at_s,
        whisper_segments,
    )
    print(
        f"  dim3 caption_vs_narrator: {_fmt_pass(result['dim3_caption_matches_narrator'])}", file=sys.stderr
    )

    # ── dim 4+5 ── visual matches SPEC.visual_intent
    result["dim4_5_visual_matches_intent"] = verify_dim45_visual(
        client,
        frame_mid,
        spec_visual,
        warnings,
    )
    print(f"  dim4_5 visual_vs_intent: {_fmt_pass(result['dim4_5_visual_matches_intent'])}", file=sys.stderr)

    # ── dim 6 ── characters
    result["dim6_characters_correct"] = verify_dim6_characters(
        client,
        frame_mid,
        expected_chars_visible,
        expected_chars_raw,
        anchors_dir,
        workdir,
        warnings,
    )
    print(f"  dim6 characters: {_fmt_pass(result['dim6_characters_correct'])}", file=sys.stderr)

    # ── dim 7 ── action sequence
    result["dim7_action_matches_narration"] = verify_dim7_action(
        client,
        [frame_start, frame_mid, frame_end],
        spec_who_does_what,
        warnings,
    )
    print(f"  dim7 action: {_fmt_pass(result['dim7_action_matches_narration'])}", file=sys.stderr)

    # ── overall ──
    fail_dims = []
    for dim_key in (
        "dim0_scope_creep",
        "dim1_narrator_says_spec",
        "dim2_caption_shows_spec",
        "dim3_caption_matches_narrator",
        "dim4_5_visual_matches_intent",
        "dim6_characters_correct",
        "dim7_action_matches_narration",
    ):
        d = result.get(dim_key, {})
        if not d.get("pass", False):
            fail_dims.append(dim_key.split("_")[0])  # dim0 / dim1 / dim2...

    # Promote dim4_5 / dim6 / dim7 short keys
    fail_dims = []
    name_map = {
        "dim0_scope_creep": "dim0",
        "dim1_narrator_says_spec": "dim1",
        "dim2_caption_shows_spec": "dim2",
        "dim3_caption_matches_narrator": "dim3",
        "dim4_5_visual_matches_intent": "dim4_5",
        "dim6_characters_correct": "dim6",
        "dim7_action_matches_narration": "dim7",
    }
    for full_key, short_key in name_map.items():
        d = result.get(full_key, {})
        if not d.get("pass", False):
            fail_dims.append(short_key)

    result["overall_pass"] = len(fail_dims) == 0
    result["fail_dimensions"] = fail_dims
    result["warnings"] = warnings
    print(
        f"  ━ overall: {'PASS' if result['overall_pass'] else 'FAIL'} (failures: {fail_dims})",
        file=sys.stderr,
    )
    return result


def _fmt_pass(d: dict) -> str:
    if d.get("skipped"):
        return f"SKIPPED ({d.get('reason', '')})"
    if d.get("pass"):
        score = d.get("jaccard_similarity") or d.get("similarity_score") or d.get("anchor_similarity") or ""
        return f"PASS ({score})"
    score = d.get("jaccard_similarity") or d.get("similarity_score") or ""
    reason = d.get("reason", "")
    return f"FAIL ({score}) — {reason}"


def verify_dim45_visual(client, frame_path: str, spec_visual: str, warnings: list) -> dict:
    if not os.path.exists(frame_path):
        return {
            "visual_description": "",
            "spec_visual_intent": spec_visual,
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": "Mid-frame not extractable",
        }
    if not spec_visual:
        warnings.append("dim4_5: SPEC.visual_intent empty — skipping")
        return {
            "visual_description": "",
            "spec_visual_intent": "",
            "similarity_score": None,
            "threshold": VISUAL_THRESHOLD,
            "pass": True,
            "skipped": True,
            "reason": "No SPEC.visual_intent provided",
        }
    # 1. describe what is visually in frame
    try:
        desc = gemini_call(client, PROMPT_DESCRIBE_VISUAL, [frame_path])
    except Exception as e:
        warnings.append(f"dim4_5 describe failed: {e}")
        return {
            "visual_description": "",
            "spec_visual_intent": spec_visual,
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": f"Gemini describe failed: {e}",
        }
    # 2. compare to spec
    compare_prompt = (
        PROMPT_COMPARE_VISUAL + f"\n\nA (SPEC visual intent):\n{spec_visual}\n\nB (Observed):\n{desc}\n"
    )
    try:
        cmp = gemini_call(client, compare_prompt, [])
        score, reason = parse_score(cmp)
    except Exception as e:
        warnings.append(f"dim4_5 compare failed: {e}")
        return {
            "visual_description": desc,
            "spec_visual_intent": spec_visual,
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": f"Gemini compare failed: {e}",
        }
    return {
        "visual_description": desc,
        "spec_visual_intent": spec_visual,
        "similarity_score": round(score, 3),
        "threshold": VISUAL_THRESHOLD,
        "pass": score >= VISUAL_THRESHOLD,
        "reason": reason,
    }


def verify_dim6_characters(
    client,
    frame_path: str,
    expected_visible: list,
    expected_raw: list,
    anchors_dir: str | None,
    workdir: str,
    warnings: list,
) -> dict:
    if not os.path.exists(frame_path):
        return {
            "expected_chars": expected_raw,
            "visible_chars": [],
            "anchor_similarity": {},
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": "Frame not extractable",
        }

    # 1. identify chars visible in frame
    try:
        resp = gemini_call(client, PROMPT_IDENTIFY_CHARACTERS, [frame_path])
        visible = parse_chars(resp)
    except Exception as e:
        warnings.append(f"dim6 identify failed: {e}")
        return {
            "expected_chars": expected_raw,
            "visible_chars": [],
            "anchor_similarity": {},
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": f"Gemini identify failed: {e}",
        }
    # remove viewer_pov from comparison (first-person POV is invisible by nature)
    visible_no_pov = [c for c in visible if c != "viewer_pov"]

    # 2. for each expected char actually present in frame, check anchor similarity
    anchor_sim = {}
    anchor_files = {
        "char_a": "char_a_mateo.png",
        "char_b": "char_b_bryan.png",
    }
    if anchors_dir:
        for c in expected_visible:
            anchor_path = os.path.join(anchors_dir, anchor_files.get(c, ""))
            if not os.path.exists(anchor_path):
                anchor_sim[c] = None
                continue
            # only meaningful if char actually visible
            if c not in visible_no_pov:
                anchor_sim[c] = 0.0
                continue
            try:
                cmp = gemini_call(client, PROMPT_COMPARE_ANCHOR, [anchor_path, frame_path])
                score, reason = parse_score(cmp)
                anchor_sim[c] = round(score, 3)
            except Exception as e:
                warnings.append(f"dim6 anchor compare {c} failed: {e}")
                anchor_sim[c] = None

    # 3. pass condition: set(expected_visible) == set(visible_no_pov) AND every anchor_sim ≥ threshold
    expected_set = set(expected_visible)
    visible_set = set(c for c in visible_no_pov if c in ("char_a", "char_b"))
    set_match = expected_set == visible_set

    anchor_pass = True
    reason_parts = []
    for c, s in anchor_sim.items():
        if s is None:
            reason_parts.append(f"{c} anchor unavailable")
            anchor_pass = False
        elif s < VISUAL_THRESHOLD:
            reason_parts.append(f"{c} anchor {s:.2f} < {VISUAL_THRESHOLD}")
            anchor_pass = False

    if not set_match:
        missing = expected_set - visible_set
        extra = visible_set - expected_set
        if missing:
            reason_parts.append(f"missing: {sorted(missing)}")
        if extra:
            reason_parts.append(f"unexpected: {sorted(extra)}")

    return {
        "expected_chars": sorted(expected_set),
        "visible_chars": sorted(visible_set),
        "viewer_pov_in_spec": "viewer_pov" in expected_raw,
        "anchor_similarity": anchor_sim,
        "threshold": VISUAL_THRESHOLD,
        "pass": set_match and anchor_pass,
        "reason": "; ".join(reason_parts) if reason_parts else "match",
    }


def verify_dim7_action(client, keyframes: list, spec_action: str, warnings: list) -> dict:
    if not spec_action:
        return {
            "spec_action": "",
            "action_observed": "",
            "similarity_score": None,
            "threshold": VISUAL_THRESHOLD,
            "pass": True,
            "skipped": True,
            "reason": "SPEC.scene_context.who_does_what empty",
        }
    existing = [k for k in keyframes if os.path.exists(k)]
    if not existing:
        return {
            "spec_action": spec_action,
            "action_observed": "",
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": "No keyframes extractable",
        }
    try:
        action_obs = gemini_call(client, PROMPT_DESCRIBE_ACTION_SEQUENCE, existing)
    except Exception as e:
        warnings.append(f"dim7 describe failed: {e}")
        return {
            "spec_action": spec_action,
            "action_observed": "",
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": f"Gemini describe failed: {e}",
        }
    compare_prompt = (
        PROMPT_COMPARE_ACTION
        + f"\n\nA (SPEC who_does_what):\n{spec_action}\n\nB (Observed action sequence):\n{action_obs}\n"
    )
    try:
        cmp = gemini_call(client, compare_prompt, [])
        score, reason = parse_score(cmp)
    except Exception as e:
        warnings.append(f"dim7 compare failed: {e}")
        return {
            "spec_action": spec_action,
            "action_observed": action_obs,
            "similarity_score": 0.0,
            "threshold": VISUAL_THRESHOLD,
            "pass": False,
            "reason": f"Gemini compare failed: {e}",
        }
    return {
        "spec_action": spec_action,
        "action_observed": action_obs,
        "similarity_score": round(score, 3),
        "threshold": VISUAL_THRESHOLD,
        "pass": score >= VISUAL_THRESHOLD,
        "reason": reason,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Batch driver
# ─────────────────────────────────────────────────────────────────────────────


def discover_atomic_clips(atomic_dir: str) -> list:
    """List atomic clips: shot_NN_*_atomic.mp4 — fall back to shot_NN_atomic.mp4 or shot_NN.mp4."""
    p = Path(atomic_dir)
    if not p.exists():
        return []
    out = []
    for f in sorted(p.iterdir()):
        if not f.is_file() or f.suffix != ".mp4":
            continue
        name = f.stem
        m = re.match(r"^(shot_\d{2})(?:_.+)?(?:_atomic)?$", name)
        if m:
            shot_id = m.group(1)
            out.append((shot_id, str(f)))
    # de-dupe: prefer *_atomic.mp4 if both exist
    by_shot = {}
    for sid, path in out:
        if sid in by_shot:
            # prefer atomic variant
            if "_atomic" in path and "_atomic" not in by_shot[sid]:
                by_shot[sid] = path
        else:
            by_shot[sid] = path
    return sorted(by_shot.items())


def main():
    parser = argparse.ArgumentParser(description="Per-shot SPEC compliance verifier (Script B)")
    parser.add_argument("--spec", required=True, help="Path to SPEC YAML")
    parser.add_argument("--shot-id", help="Single shot ID (e.g., shot_05)")
    parser.add_argument("--atomic-clip-path", help="Path to single atomic clip mp4")
    parser.add_argument("--atomic-dir", help="Dir of atomic clips for batch mode")
    parser.add_argument("--anchors-dir", help="Dir of CP1 anchor images")
    parser.add_argument("--batch", action="store_true", help="Batch audit all clips in --atomic-dir")
    parser.add_argument("--output", help="Output JSON path (single shot mode)")
    parser.add_argument("--env", help="Path to .env file with GEMINI_API_KEY")
    args = parser.parse_args()

    # env / Gemini (settings: env vars > --env file > ./.env)
    from ai_video.errors import ConfigError
    from ai_video.providers.clients import gemini_client, settings_with_env_file

    try:
        client = gemini_client(settings_with_env_file(args.env))
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    spec = load_spec(args.spec)

    # build spec shot set for scope-creep check
    spec_shot_ids = set(s.get("shot_id") for s in get_shot_list(spec) if s.get("shot_id"))

    results = []
    with tempfile.TemporaryDirectory() as workdir:
        if args.batch:
            if not args.atomic_dir:
                print("ERROR: --batch requires --atomic-dir", file=sys.stderr)
                return 1
            discovered = discover_atomic_clips(args.atomic_dir)
            # also include any spec_shot_ids NOT present in filesystem (clip_exists=False) so dim0 catches gaps
            disc_ids = set(sid for sid, _ in discovered)
            for sid in spec_shot_ids - disc_ids:
                discovered.append((sid, ""))
            discovered.sort(key=lambda x: x[0])

            print(f"📋 Batch audit: {len(discovered)} shots", file=sys.stderr)
            for shot_id, clip_path in discovered:
                try:
                    in_spec = shot_id in spec_shot_ids
                    res = audit_shot(client, shot_id, clip_path, spec, args.anchors_dir, workdir, in_spec)
                except Exception as e:
                    traceback.print_exc()
                    res = {
                        "shot_id": shot_id,
                        "atomic_clip_path": clip_path,
                        "error": str(e),
                        "overall_pass": False,
                        "fail_dimensions": ["script_error"],
                        "warnings": [traceback.format_exc()],
                    }
                results.append(res)
                # write per-shot json
                if clip_path:
                    out_json = clip_path.replace(".mp4", "_audit.json")
                    try:
                        with open(out_json, "w") as f:
                            json.dump(res, f, indent=2, ensure_ascii=False, default=str)
                    except Exception as e:
                        print(f"  WARN failed to write {out_json}: {e}", file=sys.stderr)

            # write batch summary
            summary = {
                "spec": str(args.spec),
                "total_shots": len(results),
                "passed": sum(1 for r in results if r.get("overall_pass")),
                "failed": sum(1 for r in results if not r.get("overall_pass")),
                "shots": results,
            }
            print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
        else:
            if not args.shot_id or not args.atomic_clip_path:
                print("ERROR: single-shot mode requires --shot-id and --atomic-clip-path", file=sys.stderr)
                return 1
            in_spec = args.shot_id in spec_shot_ids
            res = audit_shot(
                client,
                args.shot_id,
                args.atomic_clip_path,
                spec,
                args.anchors_dir,
                workdir,
                in_spec,
            )
            results.append(res)
            out_path = args.output or args.atomic_clip_path.replace(".mp4", "_audit.json")
            with open(out_path, "w") as f:
                json.dump(res, f, indent=2, ensure_ascii=False, default=str)
            print(json.dumps(res, indent=2, ensure_ascii=False, default=str))

    # exit code: 0 if all pass, 1 if any fail
    any_fail = any(not r.get("overall_pass") for r in results)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
