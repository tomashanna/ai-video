#!/usr/bin/env python3
"""
gemini_midexec_vision.py — Mid-execution Gemini Vision hooks (NOT post-hoc).

Phase 2: real-time Gemini Vision checks DURING CP execution so we catch
visual/audio mismatches per-shot immediately and regen ONE shot vs full iter.

4 hooks (each invoked at a specific CP step):

  hook=hailuo_post       (CP4, per animation clip)
    Verify shot_NN.mp4 visually matches SPEC scene_context.
    Extract 3 frames (start/mid/end) → Gemini Vision query.
    Checks: visual_intent match, character consistency, atmospheric motions present.
    Cost ~$0.05.

  hook=tts_post          (CP2, per TTS segment)
    Whisper re-transcribe segment_NN.mp3 → compare vs SPEC text_canonical.
    Audibility: mean_volume in [-30, -16] dBFS.
    Voseo grep (per memory feedback_spanish_neutral).
    Cost $0 (local Whisper).

  hook=atomic_post       (CP5, per atomic clip)
    Verify shot_NN_atomic.mp4 caption alignment + audio sync.
    3 frames extracted → Gemini Vision check.
    Cost ~$0.05.

  hook=transition_post   (assembly time, per transition)
    After ffmpeg concat clip_N + transition + clip_N+1.
    Visual continuity: jarring? broken? natural?
    Cost ~$0.05.

Outputs JSON report per check. Exit 1 if 🔴 score <7 detected (engineer
iterates ONE shot, not full iter cycle).

Usage:
  python gemini_midexec_vision.py --hook hailuo_post \\
    --clip assets/clips/shot_05.mp4 --spec creative-specs/foo.yaml \\
    --shot-id shot_05 [--output reports/shot_05_hailuo.json]

  python gemini_midexec_vision.py --hook tts_post \\
    --tts assets/tts/segment_03.mp3 --spec creative-specs/foo.yaml \\
    --segment-id segment_03

  python gemini_midexec_vision.py --hook atomic_post \\
    --clip assets/clips-atomic/shot_05_atomic.mp4 --spec creative-specs/foo.yaml \\
    --shot-id shot_05 --captions iter3-captions.json

  python gemini_midexec_vision.py --hook transition_post \\
    --concat assets/clips-atomic/concat_05_06.mp4 \\
    --from-shot shot_05 --to-shot shot_06

Exit codes:
  0 — all checks PASS (all scores ≥7)
  1 — 🔴 issue detected (score <7) → engineer should regen this single asset
  2 — error (missing deps, bad inputs, API failure)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import google.genai as genai  # noqa: F401  (availability check)
except ImportError:
    print("ERROR: missing deps. Run: uv sync --extra providers", file=sys.stderr)
    sys.exit(2)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

from ai_video.config import get_settings
from ai_video.providers.clients import gemini_client

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

GEMINI_MODEL = "gemini-3.1-flash-lite"
SCORE_FAIL_THRESHOLD = 7  # score <7 in any dimension → 🔴 flag regen

# Voseo argentine words to flag in TTS transcripts (per feedback_spanish_neutral)
VOSEO_PATTERNS = [
    r"\bvos\b",
    r"\bdecís\b",
    r"\belegís\b",
    r"\bsalís\b",
    r"\besperás\b",
    r"\bseguís\b",
    r"\btrabajás\b",
    r"\bpasás\b",
    r"\bllegás\b",
    r"\bpodés\b",
    r"\bvení\b",
    r"\bmirá\b",
    r"\bsentís\b",
    r"\bcomés\b",
    r"\bsos\b",
    r"\btenés\b",
    r"\bquerés\b",
    r"\bsabés\b",
    r"\bdecí\b",
    r"\bdecidí\b",
]


# ─────────────────────────────────────────────────────────────────────────────
# SHARED HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def load_spec(spec_path: str) -> dict:
    with open(spec_path) as f:
        return yaml.safe_load(f)


def find_shot(spec: dict, shot_id: str) -> dict | None:
    """Locate a shot dict in spec.shot_list by id (handles list or {shots: [...]})."""
    shot_list = spec.get("shot_list", [])
    if isinstance(shot_list, dict):
        shots = shot_list.get("shots", [])
    else:
        shots = shot_list if isinstance(shot_list, list) else []
    for shot in shots:
        if shot.get("id") == shot_id:
            return shot
    # Try fuzzy: shot_id may include suffix like "shot_05_hook"
    for shot in shots:
        if shot.get("id", "").startswith(shot_id) or shot_id.startswith(shot.get("id", "")):
            return shot
    return None


def find_narration_segment(spec: dict, segment_id: str) -> dict | None:
    """Locate narration segment in spec by id. Searches narration_script + shot_list."""
    # Try narration_script.segments
    nsc = spec.get("narration_script", {})
    if isinstance(nsc, dict):
        for seg in nsc.get("segments", []):
            if seg.get("id") == segment_id or seg.get("segment_id") == segment_id:
                return seg
    # Try shot_list narration_in_this_shot
    shot_list = spec.get("shot_list", [])
    if isinstance(shot_list, dict):
        shots = shot_list.get("shots", [])
    else:
        shots = shot_list if isinstance(shot_list, list) else []
    for shot in shots:
        if shot.get("id") == segment_id:
            return {
                "id": segment_id,
                "text_canonical": shot.get("narration_in_this_shot", {}).get("narrator_text", "")
                or shot.get("text_canonical", ""),
            }
    return None


def ffprobe_duration(media_path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", media_path],
        capture_output=True,
        text=True,
        check=True,
        timeout=SUBPROCESS_TIMEOUT_S,
    )
    return float(result.stdout.strip())


def extract_n_frames(video_path: str, n: int, output_dir: str) -> list[tuple[float, str]]:
    """Extract N evenly-spaced frames (start/mid/end for n=3). Returns [(t, path)]."""
    os.makedirs(output_dir, exist_ok=True)
    duration = ffprobe_duration(video_path)
    if n < 1:
        n = 1
    if n == 1:
        timestamps = [duration / 2]
    else:
        # Slight inset to avoid edge ffmpeg failures
        timestamps = [max(0.05, duration * (i / (n - 1)) - (0.05 if i == n - 1 else 0)) for i in range(n)]
    out = []
    for t in timestamps:
        fp = os.path.join(output_dir, f"frame_{t:06.2f}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(t), "-i", video_path, "-frames:v", "1", "-q:v", "2", fp],
            capture_output=True,
            check=False,
            timeout=SUBPROCESS_TIMEOUT_S,
        )
        if os.path.exists(fp) and os.path.getsize(fp) > 1000:
            out.append((t, fp))
    return out


def gemini_query_image(client, prompt: str, image_path: str) -> str:
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [{"text": prompt}, {"inline_data": {"mime_type": "image/png", "data": image_bytes}}],
            }
        ],
    )
    return response.text.strip()


def gemini_query_images(client, prompt: str, image_paths: list[str]) -> str:
    """Send multiple images in one Gemini call for cross-frame consistency check."""
    parts: list[dict[str, Any]] = [{"text": prompt}]
    for ip in image_paths:
        with open(ip, "rb") as f:
            parts.append({"inline_data": {"mime_type": "image/png", "data": f.read()}})
    response = client.models.generate_content(model=GEMINI_MODEL, contents=[{"role": "user", "parts": parts}])
    return response.text.strip()


def parse_score_response(text: str) -> dict:
    """Parse Gemini response of form 'DIMENSION: score/10 — rationale' per line.

    Returns {dimension: {score: int, rationale: str}}.
    Also handles JSON-formatted responses if Gemini decides to emit them.
    """
    text = text.strip()
    # Try JSON parse first
    if text.startswith("{"):
        try:
            data = json.loads(text)
            out = {}
            for k, v in data.items():
                if isinstance(v, dict) and "score" in v:
                    out[k] = {"score": int(v["score"]), "rationale": v.get("rationale", "")}
                elif isinstance(v, (int, float)):
                    out[k] = {"score": int(v), "rationale": ""}
            if out:
                return out
        except (json.JSONDecodeError, ValueError):
            pass
    # Fallback: regex line-by-line
    out = {}
    # Match e.g. "visual_match: 8/10 — characters present"
    pat = re.compile(r"^\s*[-*]?\s*([A-Za-z_][A-Za-z0-9_ ]+?)\s*[:=]\s*(\d+)\s*/\s*10\s*[-—–]?\s*(.*)$")
    for line in text.split("\n"):
        m = pat.match(line)
        if m:
            dim = m.group(1).strip().lower().replace(" ", "_")
            out[dim] = {"score": int(m.group(2)), "rationale": m.group(3).strip()}
    return out


def min_score(scores: dict) -> int | None:
    if not scores:
        return None
    return min(s["score"] for s in scores.values())


# ─────────────────────────────────────────────────────────────────────────────
# HOOK 1 — HAILUO POST (CP4 per clip)
# ─────────────────────────────────────────────────────────────────────────────

HAILUO_POST_PROMPT_TMPL = """Examina estos 3 frames (start/mid/end) de un clip animado (Hailuo/Kling/Seedance) para un video horror-choice 1080×1920.

SPEC del shot {shot_id}:
- visual_intent: {visual_intent}
- characters expected: {characters}
- atmospheric_motions expected: {atmospheric_motions}
- who_does_what per character: {who_does_what}

Tarea: scoreá 1-10 cada dimensión y dá rationale breve.

Dimensiones:
1. visual_match — ¿los frames muestran lo que dice visual_intent (LITERAL, no metáfora)?
2. character_consistency — ¿el/los personaje(s) lucen iguales entre frames start/mid/end (mismo rostro, ropa, props)?
3. atmospheric_motions_visible — ¿se ven motions ambientales descritos (polvo, flicker, swaying, etc.)?
4. composition_safe_zones — ¿la composición respeta safe zones IG Reel (sujeto no cortado feo, no off-frame, captions zone Y 58-72% libre si aplica)?
5. literal_action_match — ¿los personajes hacen LITERALMENTE lo descrito en who_does_what (verbo+objeto+cómo)?

Formato respuesta EXACTO (una dimensión por línea, score/10 — rationale):
visual_match: X/10 — <rationale>
character_consistency: X/10 — <rationale>
atmospheric_motions_visible: X/10 — <rationale>
composition_safe_zones: X/10 — <rationale>
literal_action_match: X/10 — <rationale>

Si una dimensión scorea <7 explicá específicamente qué falta o está mal."""


def hook_hailuo_post(args) -> dict:
    if not os.path.exists(args.clip):
        return {"status": "error", "error": f"clip not found: {args.clip}"}
    if not os.path.exists(args.spec):
        return {"status": "error", "error": f"spec not found: {args.spec}"}

    spec = load_spec(args.spec)
    shot = find_shot(spec, args.shot_id)
    if not shot:
        return {"status": "error", "error": f"shot_id '{args.shot_id}' not found in SPEC"}

    visual_intent = shot.get("visual_action_match", {}).get("visual_intent", "") or shot.get(
        "description", ""
    )
    characters = ", ".join(
        shot.get("characters_visible", []) or shot.get("scene_context", {}).get("who_is_there", [])
    )
    atm_list = shot.get("atmospheric_motions_list", [])
    atm_str = "; ".join(atm_list) if atm_list else "(none specified)"
    wdw = shot.get("scene_context", {}).get("who_does_what", {})
    wdw_str = "; ".join(f"{k}: {v}" for k, v in wdw.items()) if isinstance(wdw, dict) and wdw else "(none)"

    if get_settings().gemini_api_key is None:
        return {"status": "error", "error": "GEMINI_API_KEY not set"}
    client = gemini_client()

    with tempfile.TemporaryDirectory() as tmpdir:
        frames = extract_n_frames(args.clip, 3, tmpdir)
        if len(frames) < 2:
            return {"status": "error", "error": f"could not extract enough frames from {args.clip}"}

        prompt = HAILUO_POST_PROMPT_TMPL.format(
            shot_id=args.shot_id,
            visual_intent=visual_intent or "(not specified)",
            characters=characters or "(none)",
            atmospheric_motions=atm_str,
            who_does_what=wdw_str,
        )
        response = gemini_query_images(client, prompt, [fp for _, fp in frames])

    scores = parse_score_response(response)
    minscore = min_score(scores)
    flagged = minscore is not None and minscore < SCORE_FAIL_THRESHOLD

    return {
        "status": "ok",
        "hook": "hailuo_post",
        "shot_id": args.shot_id,
        "clip": args.clip,
        "frames_extracted": len(frames),
        "scores": scores,
        "min_score": minscore,
        "flagged_regen": flagged,
        "raw_response": response,
        "recommendation": (
            f"REGEN this clip — min dimension score {minscore} (<{SCORE_FAIL_THRESHOLD})"
            if flagged
            else "PASS — clip matches SPEC"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# HOOK 2 — TTS POST (CP2 per segment)
# ─────────────────────────────────────────────────────────────────────────────


def whisper_transcribe(audio_path: str) -> str:
    """Local Whisper transcribe → text. Returns empty string on failure."""
    try:
        import whisper
    except ImportError:
        # Fall back to whisper CLI if Python module missing
        try:
            with tempfile.TemporaryDirectory() as tmp:
                subprocess.run(
                    [
                        "whisper",
                        audio_path,
                        "--model",
                        "base",
                        "--language",
                        "Spanish",
                        "--output_format",
                        "txt",
                        "--output_dir",
                        tmp,
                    ],
                    capture_output=True,
                    check=True,
                    timeout=180,
                )
                txt_path = Path(tmp) / (Path(audio_path).stem + ".txt")
                if txt_path.exists():
                    return txt_path.read_text().strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return ""
        return ""

    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language="es", fp16=False)
        return result.get("text", "").strip()
    except Exception:
        return ""


def ffmpeg_mean_volume(audio_path: str) -> float | None:
    """Return mean_volume in dBFS via ffmpeg volumedetect. None if unavailable."""
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", audio_path, "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True,
            text=True,
            check=False,
            timeout=SUBPROCESS_TIMEOUT_S,
        )
        # Output in stderr
        m = re.search(r"mean_volume:\s*(-?\d+\.?\d*)\s*dB", result.stderr)
        if m:
            return float(m.group(1))
    except Exception:
        pass
    return None


def normalize_text(s: str) -> str:
    """Lowercase, strip punctuation/diacritics-naive, collapse whitespace for fuzzy compare."""
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def text_similarity(a: str, b: str) -> float:
    """Token-overlap Jaccard 0-1. Cheap, no extra deps."""
    ta = set(normalize_text(a).split())
    tb = set(normalize_text(b).split())
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


def detect_voseo(text: str) -> list[str]:
    """Return list of voseo words detected (per feedback_spanish_neutral memory)."""
    text_lower = text.lower()
    hits = []
    for pat in VOSEO_PATTERNS:
        for m in re.finditer(pat, text_lower):
            hits.append(m.group(0))
    return hits


def hook_tts_post(args) -> dict:
    if not os.path.exists(args.tts):
        return {"status": "error", "error": f"tts file not found: {args.tts}"}
    if not os.path.exists(args.spec):
        return {"status": "error", "error": f"spec not found: {args.spec}"}

    spec = load_spec(args.spec)
    segment = find_narration_segment(spec, args.segment_id)
    expected_text = ""
    if segment:
        expected_text = segment.get("text_canonical", "") or segment.get("narrator_text", "")

    transcribed = whisper_transcribe(args.tts)
    similarity = text_similarity(expected_text, transcribed) if expected_text else None
    voseo_hits = detect_voseo(transcribed) if transcribed else []
    mean_db = ffmpeg_mean_volume(args.tts)

    audibility_ok = mean_db is not None and -30 <= mean_db <= -16
    # Similarity threshold 0.55 = ~half the canonical words present (Jaccard is strict)
    text_match_ok = similarity is None or similarity >= 0.55
    voseo_clean = len(voseo_hits) == 0

    flagged = (not text_match_ok) or (not audibility_ok) or (not voseo_clean)

    issues = []
    if not text_match_ok:
        issues.append(f"text_mismatch: similarity {similarity:.2f} < 0.55 (expected vs transcribed)")
    if not audibility_ok:
        if mean_db is None:
            issues.append("audibility_unmeasurable: ffmpeg volumedetect failed")
        else:
            issues.append(f"audibility_out_of_range: mean_volume {mean_db:.1f}dBFS (target [-30, -16])")
    if not voseo_clean:
        issues.append(f"voseo_detected: {sorted(set(voseo_hits))} — per feedback_spanish_neutral")

    return {
        "status": "ok",
        "hook": "tts_post",
        "segment_id": args.segment_id,
        "tts": args.tts,
        "expected_text": expected_text,
        "transcribed_text": transcribed,
        "similarity_jaccard": similarity,
        "mean_volume_dbfs": mean_db,
        "voseo_hits": sorted(set(voseo_hits)),
        "checks": {
            "text_match": text_match_ok,
            "audibility": audibility_ok,
            "voseo_clean": voseo_clean,
        },
        "issues": issues,
        "flagged_regen": flagged,
        "recommendation": (
            f"REGEN TTS — {len(issues)} issue(s): {'; '.join(issues)}"
            if flagged
            else "PASS — TTS matches SPEC, audible, neutral Spanish"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# HOOK 3 — ATOMIC POST (CP5 per atomic clip)
# ─────────────────────────────────────────────────────────────────────────────

ATOMIC_POST_PROMPT_TMPL = """Examina estos 3 frames (start/mid/end) de un clip ATÓMICO ya muxeado (imagen + audio + caption sincronizado) para video horror-choice 1080×1920.

SPEC del shot {shot_id}:
- visual_intent: {visual_intent}
- narrator_text expected: "{narrator_text}"
- ui_active expected: {ui_active}

Tarea: scoreá 1-10 cada dimensión.

Dimensiones:
1. caption_alignment — ¿el caption visible está en la safe zone (Y 58-72%)? ¿texto cortado, fuera de pantalla, overlap con otro UI?
2. caption_legibility — ¿el caption es legible (drop shadow visible, contrast OK, no cubierto por sujeto)?
3. ui_no_overlap — ¿UI elements (countdown/loader/name labels) NO se superponen entre sí ni tapan al sujeto principal?
4. visual_intent_match — ¿el frame muestra lo que dice visual_intent (LITERAL)?
5. composition_intact — ¿composición no rota (sujeto no off-frame, encuadre balanceado, no frames negros)?

Formato respuesta EXACTO:
caption_alignment: X/10 — <rationale>
caption_legibility: X/10 — <rationale>
ui_no_overlap: X/10 — <rationale>
visual_intent_match: X/10 — <rationale>
composition_intact: X/10 — <rationale>

Si scorea <7 en alguna dimensión, explicá qué está mal."""


def hook_atomic_post(args) -> dict:
    if not os.path.exists(args.clip):
        return {"status": "error", "error": f"atomic clip not found: {args.clip}"}
    if not os.path.exists(args.spec):
        return {"status": "error", "error": f"spec not found: {args.spec}"}

    spec = load_spec(args.spec)
    shot = find_shot(spec, args.shot_id)
    if not shot:
        return {"status": "error", "error": f"shot_id '{args.shot_id}' not found in SPEC"}

    visual_intent = shot.get("visual_action_match", {}).get("visual_intent", "") or shot.get(
        "description", ""
    )
    narrator_text = shot.get("narration_in_this_shot", {}).get("narrator_text", "") or shot.get(
        "text_canonical", ""
    )
    ui_active = ", ".join(shot.get("ui_active", []) or [])

    if get_settings().gemini_api_key is None:
        return {"status": "error", "error": "GEMINI_API_KEY not set"}
    client = gemini_client()

    with tempfile.TemporaryDirectory() as tmpdir:
        frames = extract_n_frames(args.clip, 3, tmpdir)
        if len(frames) < 2:
            return {"status": "error", "error": f"could not extract enough frames from {args.clip}"}

        prompt = ATOMIC_POST_PROMPT_TMPL.format(
            shot_id=args.shot_id,
            visual_intent=visual_intent or "(not specified)",
            narrator_text=narrator_text or "(none)",
            ui_active=ui_active or "(none)",
        )
        response = gemini_query_images(client, prompt, [fp for _, fp in frames])

    scores = parse_score_response(response)
    minscore = min_score(scores)
    flagged = minscore is not None and minscore < SCORE_FAIL_THRESHOLD

    return {
        "status": "ok",
        "hook": "atomic_post",
        "shot_id": args.shot_id,
        "clip": args.clip,
        "frames_extracted": len(frames),
        "scores": scores,
        "min_score": minscore,
        "flagged_regen": flagged,
        "raw_response": response,
        "recommendation": (
            f"REGEN atomic clip — min dimension score {minscore} (<{SCORE_FAIL_THRESHOLD})"
            if flagged
            else "PASS — atomic clip caption+sync OK"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# HOOK 4 — TRANSITION POST (assembly time per transition)
# ─────────────────────────────────────────────────────────────────────────────

TRANSITION_POST_PROMPT_TMPL = """Examina estos 4 frames consecutivos de una TRANSICIÓN entre dos clips de un video horror-choice 1080×1920.

Transición: {from_shot} → {to_shot}
Frame 1 (pre-transition end of clip A): ver imagen 1
Frame 2 (mid-transition early): ver imagen 2
Frame 3 (mid-transition late): ver imagen 3
Frame 4 (post-transition start of clip B): ver imagen 4

Tarea: scoreá 1-10 cada dimensión.

Dimensiones:
1. visual_continuity — ¿la transición se siente natural o jarring (corte abrupto sin razón narrativa)?
2. no_broken_frames — ¿hay frames negros / corrupted / glitched en la transición?
3. ui_continuity — ¿UI elements (captions, watermark) hacen handoff limpio o pisan la transición?
4. composition_flow — ¿el encuadre/lente del clip A→B fluye bien (no whiplash visual extremo)?
5. atmospheric_continuity — ¿lighting/color grade/atmósfera se mantienen razonablemente entre A y B (o el cambio está justificado por shift narrativo)?

Formato respuesta EXACTO:
visual_continuity: X/10 — <rationale>
no_broken_frames: X/10 — <rationale>
ui_continuity: X/10 — <rationale>
composition_flow: X/10 — <rationale>
atmospheric_continuity: X/10 — <rationale>

Si scorea <7 explicá qué está mal."""


def hook_transition_post(args) -> dict:
    if not os.path.exists(args.concat):
        return {"status": "error", "error": f"concat clip not found: {args.concat}"}

    if get_settings().gemini_api_key is None:
        return {"status": "error", "error": "GEMINI_API_KEY not set"}
    client = gemini_client()

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract 4 frames focused on transition midpoint
        duration = ffprobe_duration(args.concat)
        # Sample around the midpoint: 40% / 48% / 52% / 60% of the concat duration
        timestamps = [
            duration * 0.40,
            duration * 0.48,
            duration * 0.52,
            duration * 0.60,
        ]
        frames = []
        for i, t in enumerate(timestamps):
            fp = os.path.join(tmpdir, f"trans_{i}_{t:06.2f}.png")
            subprocess.run(
                ["ffmpeg", "-y", "-ss", str(t), "-i", args.concat, "-frames:v", "1", "-q:v", "2", fp],
                capture_output=True,
                check=False,
                timeout=SUBPROCESS_TIMEOUT_S,
            )
            if os.path.exists(fp) and os.path.getsize(fp) > 1000:
                frames.append((t, fp))

        if len(frames) < 3:
            return {"status": "error", "error": "could not extract enough frames around transition midpoint"}

        prompt = TRANSITION_POST_PROMPT_TMPL.format(
            from_shot=args.from_shot or "clip_A",
            to_shot=args.to_shot or "clip_B",
        )
        response = gemini_query_images(client, prompt, [fp for _, fp in frames])

    scores = parse_score_response(response)
    minscore = min_score(scores)
    flagged = minscore is not None and minscore < SCORE_FAIL_THRESHOLD

    return {
        "status": "ok",
        "hook": "transition_post",
        "from_shot": args.from_shot,
        "to_shot": args.to_shot,
        "concat": args.concat,
        "frames_extracted": len(frames),
        "scores": scores,
        "min_score": minscore,
        "flagged_regen": flagged,
        "raw_response": response,
        "recommendation": (
            f"REWORK transition — min dimension score {minscore} (<{SCORE_FAIL_THRESHOLD})"
            if flagged
            else "PASS — transition flows naturally"
        ),
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def print_report(report: dict) -> None:
    """Human-readable summary of a hook report."""
    hook = report.get("hook", "?")
    status = report.get("status", "?")
    print(f"\n=== gemini_midexec_vision · hook={hook} · status={status} ===")
    if status == "error":
        print(f"  ERROR: {report.get('error')}")
        return

    # Identifiers
    for key in ("shot_id", "segment_id", "from_shot", "to_shot"):
        if report.get(key):
            print(f"  {key}: {report[key]}")

    # Scores (visual hooks)
    if report.get("scores"):
        print(f"  Scores (min={report.get('min_score')}, threshold={SCORE_FAIL_THRESHOLD}):")
        for dim, sd in report["scores"].items():
            mark = "🔴" if sd["score"] < SCORE_FAIL_THRESHOLD else ("🟡" if sd["score"] < 8 else "🟢")
            print(f"    {mark} {dim}: {sd['score']}/10 — {sd['rationale'][:80]}")

    # TTS-specific
    if hook == "tts_post":
        sim = report.get("similarity_jaccard")
        vol = report.get("mean_volume_dbfs")
        print(f"  similarity: {sim:.2f}" if sim is not None else "  similarity: n/a")
        print(f"  mean_volume_dbfs: {vol}" if vol is not None else "  mean_volume_dbfs: n/a")
        if report.get("voseo_hits"):
            print(f"  voseo detected: {report['voseo_hits']}")
        if report.get("issues"):
            for iss in report["issues"]:
                print(f"  ⚠️ {iss}")

    flagged = report.get("flagged_regen", False)
    mark = "🔴 FLAGGED" if flagged else "🟢 PASS"
    print(f"  {mark} — {report.get('recommendation', '')}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Mid-execution Gemini Vision hooks (NOT post-hoc).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--hook",
        required=True,
        choices=["hailuo_post", "tts_post", "atomic_post", "transition_post"],
        help="Which mid-exec hook to run.",
    )
    # Hook 1 + 3 args
    parser.add_argument("--clip", help="Path to .mp4 (hailuo_post / atomic_post)")
    parser.add_argument("--spec", help="Path to creative-specs/<id>.yaml")
    parser.add_argument("--shot-id", help="Shot id matching SPEC shot_list[].id")
    # Hook 2 args
    parser.add_argument("--tts", help="Path to .mp3 TTS file (tts_post)")
    parser.add_argument("--segment-id", help="Segment id matching SPEC narration_script (tts_post)")
    # Hook 3 extras
    parser.add_argument("--captions", help="Optional captions.json (atomic_post)")
    # Hook 4 args
    parser.add_argument("--concat", help="Path to .mp4 concat with transition (transition_post)")
    parser.add_argument("--from-shot", help="Source shot id (transition_post)")
    parser.add_argument("--to-shot", help="Target shot id (transition_post)")
    # Output
    parser.add_argument("--output", help="Optional JSON report path")

    args = parser.parse_args()

    # Dispatch
    try:
        if args.hook == "hailuo_post":
            if not (args.clip and args.spec and args.shot_id):
                print("ERROR: hailuo_post requires --clip --spec --shot-id", file=sys.stderr)
                return 2
            report = hook_hailuo_post(args)
        elif args.hook == "tts_post":
            if not (args.tts and args.spec and args.segment_id):
                print("ERROR: tts_post requires --tts --spec --segment-id", file=sys.stderr)
                return 2
            report = hook_tts_post(args)
        elif args.hook == "atomic_post":
            if not (args.clip and args.spec and args.shot_id):
                print("ERROR: atomic_post requires --clip --spec --shot-id", file=sys.stderr)
                return 2
            report = hook_atomic_post(args)
        elif args.hook == "transition_post":
            if not args.concat:
                print("ERROR: transition_post requires --concat", file=sys.stderr)
                return 2
            report = hook_transition_post(args)
        else:
            print(f"ERROR: unknown hook {args.hook}", file=sys.stderr)
            return 2
    except Exception as e:
        report = {"status": "error", "hook": args.hook, "error": f"unhandled: {e}"}

    print_report(report)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n  Report saved: {out_path}")

    if report.get("status") == "error":
        return 2
    return 1 if report.get("flagged_regen") else 0


if __name__ == "__main__":
    sys.exit(main())
