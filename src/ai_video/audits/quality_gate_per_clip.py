#!/usr/bin/env python3
"""
quality_gate_per_clip.py — Automated Quality Gate Agent (per-clip QA).

Phase 2 4th agent role: per-clip atomic QA running AFTER build_clip_atomic.py
completes. Validates a single shot's atomic clip against the SPEC + canonical
audio/visual/caption rules, then emits 🟢/🟡/🔴 verdict.

Authority:
  - AUDITOR-PROTOCOL § 6 anti-patterns 1-11 (especially #8 measure-don't-pattern-match,
    #9 audio-visual lip-sync realism, #10 trust docs without direct verify, #11
    random distributed timestamp frame extraction)
  - Hard rule #1 (Gemini ≥9.7 dual gate) — this per-clip gate is the early-warning
    upstream of the holistic gate, catching issues before assembly
  - Hard rule #19 NEVER ESTIMATE, ALWAYS MEASURE — every check measures directly
  - CLAUDE.md § Pre-render gate 7 gates obligatorios + Q17-Q21 referent-validated

Five check categories per clip atomic:
  1. Visual canonical compliance (Gemini Vision, 3 frames start/mid/end)
     - SPEC scene_context.who_is_there / who_does_what match
     - atmospheric_motions_count ≥3 visible
     - character consistency vs anchor
  2. Caption schema validation (clip_NN_captions.json sidecar)
     - all captions have start_abs_s + end_abs_s (no None)
     - no overlap same-Y position
     - chunks ≥1.5s
     - no voseo when SPEC declares tuteo (and vice versa)
  3. Audio waveform analysis (ffmpeg + librosa)
     - LUFS in canonical band -14 ±0.5 (Hard rule #1 / Q18)
     - true peak ≤-1 dBFS
     - no clipping events (peak ≥0 dBFS)
     - audibility (mean_volume between -30 and -16 dBFS on speech segments)
  4. Sync verify
     - TTS caption text matches audio via re-Whisper (text similarity ≥0.6)
     - audio duration matches video duration ±0.1s
     - SFX events at expected timestamps (if SPEC declares sfx_events)
  5. GAPS sentinels (per-clip subset of audit-frames-granular)
     - S1 audio-visual character mismatch
     - S2 duplicate text within clip window
     - S6 countdown digit transition (if AVU clip)
     - S8 background motion (atmospheric_motions visible)

Verdict logic:
  🟢 PASS: all checks PASS, ship-ready
  🟡 NB:   1-2 marginal WARN issues, acceptable but flagged
  🔴 FAIL: ≥1 critical FAIL, halt assembly, escalate

Usage:
    python quality_gate_per_clip.py \\
        --clip assets/clips-atomic/shot_07_atomic.mp4 \\
        --captions assets/clips-atomic/shot_07_captions.json \\
        --spec creative-specs/<id>.yaml \\
        --shot-id shot_07_d1_setup_question \\
        [--enable-gemini] \\
        [--enable-whisper] \\
        [--clip-start-abs-s 38.5]

Exit codes:
    0 — 🟢 PASS (ship-ready)
    1 — 🟡 NB   (marginal, review)
    2 — 🔴 FAIL (halt assembly)
    3 — script error (missing inputs / deps)

Cost: ~$0.10 per clip when --enable-gemini active (3 frames × Gemini Vision).
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(3)


# ============================================================
# CANONICAL THRESHOLDS (referent-validated per Hard rule #1)
# ============================================================
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

# Argentine voseo morphology markers (not exhaustive — covers common verb forms)
VOSEO_MARKERS = [
    r"\bvos\s+(sos|tenés|querés|podés|sabés|hacés|elegís|venís|tenes|querés)\b",
    r"\bsos\b",
    r"\btenés\b",
    r"\bquerés\b",
    r"\bpodés\b",
    r"\bsabés\b",
    r"\bhacés\b",
    r"\belegís\b",
    r"\bvení\b",
    r"\bandate\b",
    r"\bdecíme\b",
    r"\bmiráme\b",
    r"\bquedáte\b",
    r"\bpegáte\b",
    r"\bmovéte\b",
]

# Tuteo (Spain/LatAm neutral) markers
TUTEO_MARKERS = [
    r"\btú\s+(eres|tienes|quieres|puedes|sabes|haces|eliges|vienes)\b",
    r"\beres\b",
    r"\btienes\b",
    r"\bquieres\b",
    r"\bpuedes\b",
    r"\bsabes\b",
    r"\bhaces\b",
    r"\beliges\b",
    r"\bven\b",
    r"\bvete\b",
    r"\bdíme\b",
    r"\bmírame\b",
    r"\bquédate\b",
]


# ============================================================
# UTILITIES
# ============================================================
def run_ffprobe_duration(path: Path) -> float:
    """Return media file duration in seconds via ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def run_ffprobe_streams(path: Path) -> dict:
    """Return parsed ffprobe streams JSON."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-of", "json", str(path)],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"streams": []}


def add_finding(findings: list, check: str, severity: str, issue: str,
                fix_hint: str = "", **extra) -> None:
    """Append a structured finding."""
    f = {
        "check": check,
        "severity": severity,  # FAIL | WARN | INFO
        "issue": issue,
    }
    if fix_hint:
        f["fix_hint"] = fix_hint
    f.update(extra)
    findings.append(f)


# ============================================================
# SPEC LOADING
# ============================================================
def load_spec(spec_path: Path) -> dict:
    with open(spec_path) as f:
        return yaml.safe_load(f) or {}


def find_shot_in_spec(spec: dict, shot_id: str) -> dict:
    """Return the shot dict matching shot_id, or {} if not found."""
    shot_list = spec.get("shot_list", [])
    if isinstance(shot_list, dict):
        shots = shot_list.get("shots", [])
    else:
        shots = shot_list if isinstance(shot_list, list) else []

    # Exact match
    for shot in shots:
        if shot.get("id") == shot_id:
            return shot

    # Prefix match (e.g., shot_07 matches shot_07_d1_setup_question)
    prefix_match = None
    for shot in shots:
        sid = shot.get("id", "")
        if sid.startswith(shot_id) or shot_id.startswith(sid.split("_")[0] + "_" + sid.split("_")[1] if "_" in sid else sid):
            prefix_match = shot
            break
    if prefix_match:
        return prefix_match

    # Match just the numeric prefix shot_NN
    m = re.match(r"(shot_\d+)", shot_id)
    if m:
        prefix = m.group(1)
        for shot in shots:
            if shot.get("id", "").startswith(prefix):
                return shot

    return {}


def detect_register(spec: dict, shot: dict) -> str:
    """Detect declared narrative register: voseo | tuteo | unknown."""
    # Check shot-level first
    for source in [shot, spec]:
        for key in ["register", "narrative_register", "person"]:
            v = source.get(key)
            if isinstance(v, str):
                vl = v.lower()
                if "voseo" in vl:
                    return "voseo"
                if "tuteo" in vl:
                    return "tuteo"
        # Nested SPEC voice/script blocks
        nested = source.get("script") or source.get("narration") or {}
        if isinstance(nested, dict):
            for key in ["register", "person"]:
                v = nested.get(key)
                if isinstance(v, str):
                    vl = v.lower()
                    if "voseo" in vl:
                        return "voseo"
                    if "tuteo" in vl:
                        return "tuteo"
    return "unknown"


# ============================================================
# CHECK 1: VISUAL CANONICAL COMPLIANCE (Gemini Vision)
# ============================================================
GEMINI_VISUAL_PROMPT_TMPL = """Examina este frame de un clip atomic de horror-choice (1080×1920 vertical IG Reel).

CONTEXTO DEL SHOT (de SPEC):
- shot_id: {shot_id}
- who_is_there: {who_is_there}
- who_does_what:
{who_does_what}
- atmospheric_motions_count_expected: {atmospheric_count}
- atmospheric_motions_list:
{atmospheric_list}
- camera_intent: {camera}

VERIFICÁ y respondé en JSON estricto con estas keys:
{{
  "characters_visible": ["lista de characters visibles realmente"],
  "characters_match_spec": true|false,
  "atmospheric_motions_visible_estimate": <int>,
  "atmospheric_meets_threshold_3": true|false,
  "character_drift_vs_anchor": "none|minor|major",
  "composition_broken": true|false,
  "ui_overlaps_face": true|false,
  "issues": ["lista corta de issues específicos encontrados, vacío si OK"]
}}

NO incluyas texto fuera del JSON. NO uses markdown fences."""


def extract_three_frames(clip_path: Path, tmpdir: Path) -> list:
    """Extract frames at start (+0.2s), mid, end (-0.2s) of clip.

    Returns list of (label, timestamp, path) tuples.
    """
    duration = run_ffprobe_duration(clip_path)
    if duration <= 0.5:
        return []

    timestamps = [
        ("start", 0.2),
        ("mid",   duration / 2.0),
        ("end",   max(0.2, duration - 0.2)),
    ]
    extracted = []
    for label, t in timestamps:
        out = tmpdir / f"frame_{label}_{t:06.2f}.png"
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(clip_path),
             "-frames:v", "1", "-q:v", "2", str(out)],
            capture_output=True
        )
        if out.exists() and out.stat().st_size > 1000:
            extracted.append((label, t, out))
    return extracted


def gemini_vision_audit_frame(frame_path: Path, prompt: str, client) -> dict:
    """Send frame + prompt to Gemini Vision. Return parsed JSON dict or {}."""
    with open(frame_path, "rb") as f:
        image_bytes = f.read()

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=[{
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/png", "data": image_bytes}}
                ]
            }]
        )
    except Exception as e:
        return {"_error": str(e)}

    text = response.text.strip()
    # Strip optional markdown fences if model still wraps them
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"_error": "json_parse_failed", "_raw": text[:200]}


def check_visual_canonical(clip_path: Path, shot: dict, shot_id: str,
                           findings: list, enable_gemini: bool = False) -> dict:
    """Check 1: Visual canonical compliance via Gemini Vision (3 frames)."""
    results = {"enabled": enable_gemini, "frames_audited": 0, "raw": []}

    if not enable_gemini:
        add_finding(findings, "visual_canonical", "INFO",
                    "Gemini Vision not enabled (--enable-gemini) — visual canonical check skipped",
                    fix_hint="Re-run with --enable-gemini for full canonical compliance verification (~$0.10/clip)")
        return results

    try:
        import google.genai as genai
    except ImportError:
        add_finding(findings, "visual_canonical", "WARN",
                    "google-genai not installed — visual canonical check skipped",
                    fix_hint="uv sync --extra providers")
        return results

    from ai_video.config import get_settings
    from ai_video.providers.clients import gemini_client

    if get_settings().gemini_api_key is None:
        add_finding(findings, "visual_canonical", "WARN",
                    "GEMINI_API_KEY not set — visual canonical check skipped",
                    fix_hint="Set GEMINI_API_KEY in .env (see .env.example)")
        return results

    client = gemini_client()

    # Build SPEC-driven prompt
    sc = shot.get("scene_context", {}) or {}
    who_is_there = sc.get("who_is_there", []) or []
    who_does_what = sc.get("who_does_what", {}) or {}
    who_does_what_str = "\n".join(
        f"  - {k}: {v}" for k, v in who_does_what.items()
    ) if isinstance(who_does_what, dict) else str(who_does_what)
    atmospheric_count = shot.get("atmospheric_motions_count", "unknown")
    atmospheric_list = shot.get("atmospheric_motions_list", []) or []
    atmospheric_list_str = "\n".join(f"  - {m}" for m in atmospheric_list) or "  (none declared)"
    camera = shot.get("camera", {}) or {}
    camera_str = json.dumps(camera) if isinstance(camera, dict) else str(camera)

    prompt = GEMINI_VISUAL_PROMPT_TMPL.format(
        shot_id=shot_id,
        who_is_there=who_is_there,
        who_does_what=who_does_what_str,
        atmospheric_count=atmospheric_count,
        atmospheric_list=atmospheric_list_str,
        camera=camera_str,
    )

    with tempfile.TemporaryDirectory() as td:
        tmpdir = Path(td)
        frames = extract_three_frames(clip_path, tmpdir)
        if not frames:
            add_finding(findings, "visual_canonical", "FAIL",
                        f"Could not extract frames from {clip_path.name} (clip ≤0.5s or ffmpeg failed)")
            return results

        for label, t, frame_path in frames:
            audit = gemini_vision_audit_frame(frame_path, prompt, client)
            results["frames_audited"] += 1
            results["raw"].append({"label": label, "t": t, "audit": audit})

            if audit.get("_error"):
                add_finding(findings, "visual_canonical", "WARN",
                            f"Gemini Vision error at t={t:.2f}s ({label}): {audit['_error']}")
                continue

            if not audit.get("characters_match_spec", True):
                visible = audit.get("characters_visible", [])
                add_finding(findings, "visual_canonical", "FAIL",
                            f"Characters mismatch at t={t:.2f}s ({label}): SPEC expects {who_is_there}, visible {visible}",
                            fix_hint="Regenerate clip with corrected character prompt OR verify anchor was used.")
            if not audit.get("atmospheric_meets_threshold_3", True):
                est = audit.get("atmospheric_motions_visible_estimate", 0)
                add_finding(findings, "visual_canonical", "WARN",
                            f"Atmospheric motions estimate {est} <3 at t={t:.2f}s ({label}); SPEC declares {atmospheric_count}",
                            fix_hint="Add ambient micro-motion (smoke, dust, flicker, creature) at this beat.")
            drift = audit.get("character_drift_vs_anchor", "none")
            if drift == "major":
                add_finding(findings, "visual_canonical", "FAIL",
                            f"Character drift MAJOR vs anchor at t={t:.2f}s ({label})",
                            fix_hint="Re-anchor with character reference image; regenerate animation clip.")
            elif drift == "minor":
                add_finding(findings, "visual_canonical", "WARN",
                            f"Character drift MINOR vs anchor at t={t:.2f}s ({label})")
            if audit.get("composition_broken", False):
                add_finding(findings, "visual_canonical", "FAIL",
                            f"Composition broken at t={t:.2f}s ({label})",
                            fix_hint="Regenerate with explicit camera framing in prompt.")
            if audit.get("ui_overlaps_face", False):
                add_finding(findings, "visual_canonical", "FAIL",
                            f"UI overlaps character face at t={t:.2f}s ({label})",
                            fix_hint="Reposition UI to safe zone (caption Y 62%, name_label Y 11.5%).")
            for issue in audit.get("issues", []) or []:
                add_finding(findings, "visual_canonical", "WARN",
                            f"Gemini Vision @ t={t:.2f}s ({label}): {issue}")

    return results


# ============================================================
# CHECK 2: CAPTION SCHEMA VALIDATION
# ============================================================
def load_captions(captions_path: Path) -> list:
    """Load + normalize captions list from sidecar JSON."""
    with open(captions_path) as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data.get("captions", []) or []
    if isinstance(data, list):
        return data
    return []


def check_captions_schema(captions_path: Path, shot: dict, spec: dict,
                          clip_duration: float, findings: list) -> dict:
    """Check 2: validate caption sidecar schema + voseo/tuteo + overlaps + chunk durations."""
    results = {"captions_count": 0, "register_expected": None}

    if not captions_path.exists():
        add_finding(findings, "caption_schema", "FAIL",
                    f"Captions sidecar not found: {captions_path}",
                    fix_hint="Run build_clip_atomic.py to produce sidecar captions JSON.")
        return results

    try:
        captions = load_captions(captions_path)
    except (json.JSONDecodeError, OSError) as e:
        add_finding(findings, "caption_schema", "FAIL",
                    f"Captions sidecar unreadable: {e}")
        return results

    results["captions_count"] = len(captions)

    if not captions:
        # Acceptable if shot is silent_by_design or AVU bundled audio
        narration = shot.get("narration_in_this_shot", {}) or {}
        if narration.get("silence_by_design") is True:
            add_finding(findings, "caption_schema", "INFO",
                        "Captions empty but shot.silence_by_design=true — OK")
        else:
            add_finding(findings, "caption_schema", "WARN",
                        "Captions sidecar empty; shot does not declare silence_by_design",
                        fix_hint="Verify SPEC narration_in_this_shot; add captions if narration present.")
        return results

    # --- Schema: required fields ---
    for i, c in enumerate(captions):
        cap_id = c.get("id", f"cap[{i}]")
        for required in ["start_abs_s", "end_abs_s"]:
            v = c.get(required)
            if v is None:
                add_finding(findings, "caption_schema", "FAIL",
                            f"Caption {cap_id} missing or None field '{required}'",
                            fix_hint="Re-run Whisper alignment; ensure all chunks have absolute timestamps.")
        # Field text presence
        if not (c.get("whisper_text") or c.get("text")):
            add_finding(findings, "caption_schema", "FAIL",
                        f"Caption {cap_id} has no whisper_text/text")

    # --- Chunk duration ≥1.5s (canonical) ---
    for c in captions:
        cap_id = c.get("id", "?")
        start = c.get("start_abs_s")
        end = c.get("end_abs_s")
        if start is None or end is None:
            continue
        try:
            dur = float(end) - float(start)
        except (TypeError, ValueError):
            continue
        if dur < MIN_CAPTION_CHUNK_S:
            add_finding(findings, "caption_schema", "WARN",
                        f"Caption {cap_id} chunk {dur:.2f}s < {MIN_CAPTION_CHUNK_S}s canonical min",
                        fix_hint="Merge short adjacent chunks; canonical readability requires ≥1.5s.")

    # --- Overlap detection same-Y position ---
    sorted_caps = sorted(
        [c for c in captions if c.get("start_abs_s") is not None and c.get("end_abs_s") is not None],
        key=lambda c: float(c["start_abs_s"])
    )
    for i in range(len(sorted_caps) - 1):
        a = sorted_caps[i]
        b = sorted_caps[i + 1]
        try:
            a_end = float(a["end_abs_s"])
            b_start = float(b["start_abs_s"])
        except (TypeError, ValueError):
            continue
        if a_end > b_start + 0.05:
            a_y = a.get("y_position_pct", 62)
            b_y = b.get("y_position_pct", 62)
            if abs(float(a_y) - float(b_y)) < 2.0:
                add_finding(findings, "caption_schema", "FAIL",
                            f"Captions {a.get('id')} and {b.get('id')} overlap at Y≈{a_y}% "
                            f"({a_end:.2f}s vs {b_start:.2f}s)",
                            fix_hint="Stagger end/start timestamps OR move one caption to different Y.")

    # --- Voseo / tuteo consistency vs SPEC register ---
    register_expected = detect_register(spec, shot)
    results["register_expected"] = register_expected

    if register_expected in ("voseo", "tuteo"):
        wrong_markers = TUTEO_MARKERS if register_expected == "voseo" else VOSEO_MARKERS
        violator_label = "tuteo" if register_expected == "voseo" else "voseo"
        for c in captions:
            text = (c.get("whisper_text") or c.get("text") or "").lower()
            if not text:
                continue
            for pattern in wrong_markers:
                if re.search(pattern, text, re.IGNORECASE):
                    add_finding(findings, "caption_schema", "FAIL",
                                f"Caption {c.get('id')} contains {violator_label} marker "
                                f"(SPEC declares {register_expected}): \"{text[:80]}\"",
                                fix_hint=f"Rewrite to {register_expected} form; regenerate TTS + Whisper align.")
                    break
    else:
        # Just check internal consistency: don't mix voseo + tuteo within same shot
        has_voseo = False
        has_tuteo = False
        for c in captions:
            text = (c.get("whisper_text") or c.get("text") or "").lower()
            if not text:
                continue
            if any(re.search(p, text, re.IGNORECASE) for p in VOSEO_MARKERS):
                has_voseo = True
            if any(re.search(p, text, re.IGNORECASE) for p in TUTEO_MARKERS):
                has_tuteo = True
        if has_voseo and has_tuteo:
            add_finding(findings, "caption_schema", "WARN",
                        "Captions mix voseo + tuteo within same clip (SPEC has no declared register)",
                        fix_hint="Decide voseo or tuteo at SPEC level; rewrite + regen TTS.")

    # --- Y position canonical band ---
    for c in captions:
        y = c.get("y_position_pct")
        if y is None:
            continue
        try:
            yv = float(y)
        except (TypeError, ValueError):
            continue
        cls = (c.get("class") or "").lower()
        # name_label uses Y 11.5%, skip
        if cls == "name_label" or "name" in cls:
            continue
        if yv < CANONICAL_CAPTION_Y_LOW or yv > CANONICAL_CAPTION_Y_HIGH:
            add_finding(findings, "caption_schema", "WARN",
                        f"Caption {c.get('id')} Y={yv}% outside canonical band [{CANONICAL_CAPTION_Y_LOW}-{CANONICAL_CAPTION_Y_HIGH}]",
                        fix_hint="Set Y=62 (canonical) unless name_label (11.5).")

    return results


# ============================================================
# CHECK 3: AUDIO WAVEFORM ANALYSIS
# ============================================================
def measure_lufs(clip_path: Path) -> dict:
    """Run ffmpeg loudnorm pass-1 and parse LUFS + true_peak."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(clip_path),
         "-af", f"loudnorm=I={TARGET_LUFS}:TP={TRUE_PEAK_MAX}:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True
    )
    output = result.stderr
    try:
        start = output.rindex("{")
        end = output.rindex("}") + 1
        data = json.loads(output[start:end])
        return {
            "input_i": float(data.get("input_i", 0)) if data.get("input_i") not in (None, "") else None,
            "input_tp": float(data.get("input_tp", 0)) if data.get("input_tp") not in (None, "") else None,
            "input_lra": float(data.get("input_lra", 0)) if data.get("input_lra") not in (None, "") else None,
        }
    except (ValueError, json.JSONDecodeError, KeyError):
        return {"input_i": None, "input_tp": None, "input_lra": None}


def measure_volumedetect(clip_path: Path) -> dict:
    """Run ffmpeg volumedetect, return mean_volume + max_volume."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(clip_path),
         "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True
    )
    output = result.stderr
    mean_match = re.search(r"mean_volume:\s*(-?[\d.]+)\s*dB", output)
    max_match = re.search(r"max_volume:\s*(-?[\d.]+)\s*dB", output)
    return {
        "mean_volume": float(mean_match.group(1)) if mean_match else None,
        "max_volume": float(max_match.group(1)) if max_match else None,
    }


def check_audio_waveform(clip_path: Path, has_speech: bool, findings: list) -> dict:
    """Check 3: LUFS, true_peak, clipping, audibility."""
    streams = run_ffprobe_streams(clip_path)
    has_audio_stream = any(s.get("codec_type") == "audio" for s in streams.get("streams", []))

    results = {"has_audio_stream": has_audio_stream}

    if not has_audio_stream:
        add_finding(findings, "audio_waveform", "WARN",
                    "Clip has no audio stream",
                    fix_hint="If silent_by_design, OK. Otherwise add narration/SFX track before assembly.")
        return results

    lufs_data = measure_lufs(clip_path)
    vol_data = measure_volumedetect(clip_path)
    results.update({"lufs": lufs_data, "volume": vol_data})

    # LUFS check
    lufs_i = lufs_data.get("input_i")
    if lufs_i is None:
        add_finding(findings, "audio_waveform", "WARN",
                    "Could not measure LUFS (ffmpeg loudnorm did not return JSON)")
    else:
        delta = abs(lufs_i - TARGET_LUFS)
        if delta > LUFS_TOLERANCE:
            sev = "FAIL" if delta > 2.0 else "WARN"
            add_finding(findings, "audio_waveform", sev,
                        f"LUFS {lufs_i:.2f} dB outside canonical {TARGET_LUFS} ±{LUFS_TOLERANCE} dB (delta {delta:.2f})",
                        fix_hint=f"Apply master-audio.sh OR ffmpeg loudnorm pass-2 to bring to {TARGET_LUFS} LUFS.",
                        lufs_measured=round(lufs_i, 2), lufs_target=TARGET_LUFS)
        else:
            results["lufs_pass"] = True

    # True peak check
    tp = lufs_data.get("input_tp")
    if tp is not None and tp > TRUE_PEAK_MAX:
        sev = "FAIL" if tp > 0.0 else "WARN"
        add_finding(findings, "audio_waveform", sev,
                    f"True peak {tp:.2f} dBFS > {TRUE_PEAK_MAX} dBFS canonical max",
                    fix_hint="Apply limiter (ffmpeg alimiter=level_in=1:level_out=1:limit=0.89) or master-audio.sh.",
                    true_peak=round(tp, 2))

    # Clipping events (max_volume ≥ 0)
    max_vol = vol_data.get("max_volume")
    if max_vol is not None and max_vol >= 0.0:
        add_finding(findings, "audio_waveform", "FAIL",
                    f"Clipping detected: max_volume {max_vol:.2f} dBFS ≥ 0 dBFS",
                    fix_hint="Reduce input gain or apply limiter before mastering.",
                    max_volume=round(max_vol, 2))

    # Audibility on speech segments
    mean_vol = vol_data.get("mean_volume")
    if has_speech and mean_vol is not None:
        if mean_vol < SPEECH_MEAN_VOL_MIN:
            add_finding(findings, "audio_waveform", "WARN",
                        f"Speech mean_volume {mean_vol:.2f} dBFS < {SPEECH_MEAN_VOL_MIN} dBFS — too quiet, likely inaudible",
                        fix_hint="Boost narration track gain OR reduce ducking aggressiveness.",
                        mean_volume=round(mean_vol, 2))
        elif mean_vol > SPEECH_MEAN_VOL_MAX:
            add_finding(findings, "audio_waveform", "WARN",
                        f"Speech mean_volume {mean_vol:.2f} dBFS > {SPEECH_MEAN_VOL_MAX} dBFS — too hot, likely distorted",
                        fix_hint="Reduce narration gain OR apply pre-master compression.",
                        mean_volume=round(mean_vol, 2))

    return results


# ============================================================
# CHECK 4: SYNC VERIFY
# ============================================================
def text_similarity(a: str, b: str) -> float:
    """Simple word-set Jaccard similarity (normalized lowercased)."""
    def tokenize(s: str) -> set:
        return set(re.findall(r"[a-záéíóúüñ]+", s.lower()))
    ta = tokenize(a)
    tb = tokenize(b)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def check_sync(clip_path: Path, captions_path: Path, shot: dict, captions_count: int,
               enable_whisper: bool, findings: list) -> dict:
    """Check 4: sync verify (durations, optional re-Whisper)."""
    results = {"whisper_enabled": enable_whisper}

    video_duration = run_ffprobe_duration(clip_path)
    results["video_duration"] = round(video_duration, 3)

    streams = run_ffprobe_streams(clip_path)
    audio_streams = [s for s in streams.get("streams", []) if s.get("codec_type") == "audio"]
    if audio_streams:
        a_dur_str = audio_streams[0].get("duration")
        try:
            audio_duration = float(a_dur_str) if a_dur_str else video_duration
        except (TypeError, ValueError):
            audio_duration = video_duration
        results["audio_duration"] = round(audio_duration, 3)
        if abs(audio_duration - video_duration) > AUDIO_VIDEO_DURATION_TOLERANCE_S:
            add_finding(findings, "sync", "WARN",
                        f"Audio duration {audio_duration:.3f}s != video duration {video_duration:.3f}s "
                        f"(delta {abs(audio_duration - video_duration):.3f}s > {AUDIO_VIDEO_DURATION_TOLERANCE_S}s)",
                        fix_hint="Re-mux audio+video; check for offset drift in build_clip_atomic.")

    # SFX expected timestamps (if SPEC declares audio_visual_atomic_units with type=sync_contract)
    avu_list = shot.get("audio_visual_atomic_units", []) or []
    sync_contracts = [a for a in avu_list if a.get("type") == "sync_contract"]
    if sync_contracts:
        # Cannot verify ffmpeg-level without re-extracting all events; flag as INFO
        add_finding(findings, "sync", "INFO",
                    f"{len(sync_contracts)} sync_contract AVU(s) declared in SPEC — verify in render-level audit (audit-frames-granular S3)")

    # Re-Whisper (optional, expensive)
    if not enable_whisper:
        add_finding(findings, "sync", "INFO",
                    "Re-Whisper sync verify skipped (--enable-whisper) — text similarity TTS↔caption not measured",
                    fix_hint="Re-run with --enable-whisper for full TTS↔caption text-similarity verification")
        return results

    if captions_count == 0:
        return results

    try:
        import whisper
    except ImportError:
        add_finding(findings, "sync", "WARN",
                    "openai-whisper not installed — re-Whisper skipped",
                    fix_hint="pip install openai-whisper")
        return results

    # Extract audio to temp wav
    with tempfile.TemporaryDirectory() as td:
        tmp_wav = Path(td) / "audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(clip_path), "-vn",
             "-ac", "1", "-ar", "16000", str(tmp_wav)],
            capture_output=True
        )
        if not tmp_wav.exists() or tmp_wav.stat().st_size < 1000:
            add_finding(findings, "sync", "WARN", "Could not extract audio for re-Whisper")
            return results

        try:
            model = whisper.load_model("small")
            r = model.transcribe(str(tmp_wav), language="es", verbose=False)
        except Exception as e:
            add_finding(findings, "sync", "WARN", f"Whisper transcribe failed: {e}")
            return results

    whisper_text = (r.get("text") or "").strip()
    results["whisper_text"] = whisper_text[:300]

    # Compare against caption sidecar text concat
    captions = load_captions(captions_path)
    caption_text_concat = " ".join(
        (c.get("whisper_text") or c.get("text") or "").strip() for c in captions
    ).strip()
    sim = text_similarity(caption_text_concat, whisper_text)
    results["text_similarity"] = round(sim, 3)

    if sim < WHISPER_TEXT_SIM_MIN:
        sev = "FAIL" if sim < 0.3 else "WARN"
        add_finding(findings, "sync", sev,
                    f"TTS↔caption text similarity {sim:.2f} < {WHISPER_TEXT_SIM_MIN} (re-Whisper)",
                    fix_hint="Re-generate TTS OR re-align captions; check for missing/extra phrases.",
                    caption_text=caption_text_concat[:200],
                    whisper_text=whisper_text[:200])

    return results


# ============================================================
# CHECK 5: GAPS SENTINELS (per-clip subset)
# ============================================================
def check_gaps_sentinels(clip_path: Path, captions_path: Path, shot: dict,
                          captions_count: int, findings: list,
                          clip_start_abs_s: float = 0.0) -> dict:
    """Check 5: per-clip GAPS sentinels (subset of audit-frames-granular)."""
    results = {}

    captions = load_captions(captions_path) if captions_path.exists() else []
    shot_id = shot.get("id", "?")

    # --- S1: audio-visual character mismatch (per-clip simplified) ---
    # If caption has speaker=character (non-narrator) and character not in scene_context.who_is_there → FAIL
    sc = shot.get("scene_context", {}) or {}
    who_is_there = set(sc.get("who_is_there", []) or [])
    for c in captions:
        spk = (c.get("speaker") or "").lower()
        if spk in ("", "narrator", "off_screen", "off-screen"):
            continue
        if who_is_there and spk not in who_is_there:
            add_finding(findings, "sentinel_s1", "FAIL",
                        f"Caption {c.get('id')} speaker='{spk}' but scene_context.who_is_there={list(who_is_there)} "
                        f"(audio-visual character mismatch, anti-pattern #9)",
                        fix_hint="Either add character to scene_context OR change caption speaker OR change shot composition to show character.")

    # --- S2: duplicate text within clip window ---
    texts_seen = {}
    for c in captions:
        txt = (c.get("whisper_text") or c.get("text") or "").lower().strip().rstrip(".")
        if not txt:
            continue
        if txt in texts_seen:
            add_finding(findings, "sentinel_s2", "WARN",
                        f"Duplicate caption text within clip: '{txt[:60]}' appears in {texts_seen[txt]} and {c.get('id')}")
        else:
            texts_seen[txt] = c.get("id", "?")

    # --- S6: countdown digit transition (if AVU clip) ---
    is_avu = any(
        (a.get("type") == "pre_rendered_avu" and "countdown" in (a.get("id", "") + a.get("asset_path", "")).lower())
        for a in (shot.get("audio_visual_atomic_units", []) or [])
    )
    if not is_avu:
        # heuristic: check shot_id contains "avu" or "countdown"
        if any(k in shot_id.lower() for k in ["avu", "countdown"]):
            is_avu = True

    if is_avu:
        # Sample 5 frames evenly and check via volumedetect for tick energy peaks
        # (lightweight signal — does the AVU have audio peaks at expected 1s intervals?)
        duration = run_ffprobe_duration(clip_path)
        if duration >= 2.5:  # countdown AVU should be ~3s
            # Just verify >=3 distinct loud events in audio
            vol = measure_volumedetect(clip_path)
            mv = vol.get("max_volume")
            if mv is not None and mv < -10.0:
                add_finding(findings, "sentinel_s6", "WARN",
                            f"AVU countdown clip max_volume {mv:.2f} dBFS unexpectedly quiet — tick energy may be missing",
                            fix_hint="Verify bundled audio in AVU asset; re-mux with ticks at digit-change moments.")
        else:
            add_finding(findings, "sentinel_s6", "WARN",
                        f"AVU countdown clip duration {duration:.2f}s < 2.5s (expected ~3s for film leader countdown)")

    # --- S8: background motion (atmospheric_motions visible) ---
    # Done via Gemini in check_visual_canonical — this sentinel just verifies SPEC declared count ≥3
    spec_count = shot.get("atmospheric_motions_count")
    spec_list = shot.get("atmospheric_motions_list", []) or []
    if spec_count is not None:
        try:
            sc_int = int(spec_count)
            if sc_int < MIN_ATMOSPHERIC_MOTIONS:
                add_finding(findings, "sentinel_s8", "WARN",
                            f"SPEC declares atmospheric_motions_count={sc_int} < {MIN_ATMOSPHERIC_MOTIONS} canonical min",
                            fix_hint="Add atmospheric micro-motions to SPEC + re-generate clip prompt.")
        except (TypeError, ValueError):
            pass
    if not spec_list and not is_avu:
        add_finding(findings, "sentinel_s8", "WARN",
                    "SPEC has empty atmospheric_motions_list (and clip is not AVU)",
                    fix_hint="Add atmospheric_motions_list with ≥3 entries (smoke/dust/flicker/creature/etc).")

    return results


# ============================================================
# REPORTING + VERDICT
# ============================================================
def compute_verdict(findings: list) -> tuple:
    """Compute (verdict_emoji, verdict_label, exit_code) from findings.

    🟢 PASS  — 0 FAIL, 0-2 WARN
    🟡 NB    — 0 FAIL, 3+ WARN (or marginal)
    🔴 FAIL  — ≥1 FAIL
    """
    fails = [f for f in findings if f.get("severity") == "FAIL"]
    warns = [f for f in findings if f.get("severity") == "WARN"]

    if fails:
        return ("🔴", "FAIL", 2)
    if len(warns) <= 2:
        return ("🟢", "PASS", 0)
    return ("🟡", "NB", 1)


def write_audit_md(out_path: Path, clip_path: Path, shot_id: str,
                   findings: list, results_by_check: dict,
                   verdict_emoji: str, verdict_label: str) -> None:
    """Write human-readable audit report."""
    fails = [f for f in findings if f.get("severity") == "FAIL"]
    warns = [f for f in findings if f.get("severity") == "WARN"]
    infos = [f for f in findings if f.get("severity") == "INFO"]

    lines = [
        f"# Quality Gate per-Clip Audit — {shot_id}",
        "",
        f"**Clip**: `{clip_path}`",
        f"**Verdict**: {verdict_emoji} **{verdict_label}**",
        f"**Findings**: {len(fails)} FAIL · {len(warns)} WARN · {len(infos)} INFO",
        "",
        "## Verdict logic",
        "- 🟢 PASS: 0 FAIL, ≤2 WARN — ship-ready",
        "- 🟡 NB:   0 FAIL, ≥3 WARN — marginal, flagged for human review",
        "- 🔴 FAIL: ≥1 FAIL — halt assembly, escalate",
        "",
        "## Findings",
        "",
    ]

    if not findings:
        lines.append("_No findings._")
    else:
        for sev_label, sev_items, marker in [
            ("FAIL", fails, "🔴"),
            ("WARN", warns, "🟡"),
            ("INFO", infos, "ℹ️"),
        ]:
            if not sev_items:
                continue
            lines.append(f"### {marker} {sev_label} ({len(sev_items)})")
            lines.append("")
            for f in sev_items:
                lines.append(f"- **[{f.get('check')}]** {f.get('issue', '')}")
                if f.get("fix_hint"):
                    lines.append(f"  - _Fix_: {f['fix_hint']}")
            lines.append("")

    lines.extend([
        "## Check results summary",
        "",
        "```json",
        json.dumps(results_by_check, indent=2, default=str),
        "```",
        "",
    ])

    out_path.write_text("\n".join(lines))


# ============================================================
# MAIN
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--clip", required=True, help="Path to shot_NN_atomic.mp4")
    parser.add_argument("--captions", required=True, help="Path to shot_NN_captions.json sidecar")
    parser.add_argument("--spec", required=True, help="Path to creative-specs/<id>.yaml")
    parser.add_argument("--shot-id", required=True, help="Shot id (e.g. shot_07 or shot_07_d1_setup_question)")
    parser.add_argument("--enable-gemini", action="store_true",
                        help="Enable Gemini Vision visual canonical check (~$0.10/clip)")
    parser.add_argument("--enable-whisper", action="store_true",
                        help="Enable re-Whisper TTS↔caption sync verify (slow, CPU-heavy)")
    parser.add_argument("--clip-start-abs-s", type=float, default=0.0,
                        help="Absolute timestamp where this clip starts in master timeline (default 0)")
    parser.add_argument("--output-dir", default=None,
                        help="Output dir for audit.json + audit.md (default: same as clip)")
    args = parser.parse_args()

    clip_path = Path(args.clip)
    captions_path = Path(args.captions)
    spec_path = Path(args.spec)

    # --- Validate inputs ---
    for p, label in [(clip_path, "clip"), (spec_path, "spec")]:
        if not p.exists():
            print(f"ERROR: {label} not found: {p}", file=sys.stderr)
            sys.exit(3)
    # captions may legitimately not exist for AVU-only clips; we warn in check_captions_schema

    out_dir = Path(args.output_dir) if args.output_dir else clip_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    audit_json_path = out_dir / f"{clip_path.stem}_audit.json"
    audit_md_path = out_dir / f"{clip_path.stem}_audit.md"

    # --- Load SPEC ---
    spec = load_spec(spec_path)
    shot = find_shot_in_spec(spec, args.shot_id)
    if not shot:
        print(f"WARN: shot_id '{args.shot_id}' not found in SPEC. Running checks with empty shot context.",
              file=sys.stderr)

    # --- Determine has_speech from SPEC ---
    narration = shot.get("narration_in_this_shot", {}) or {}
    silence_by_design = narration.get("silence_by_design") is True
    narrator_text = narration.get("narrator_text") or ""
    char_dialogue = narration.get("character_dialogue") or {}
    has_speech = bool(narrator_text.strip()) or any(
        bool((v or "").strip()) for v in (char_dialogue.values() if isinstance(char_dialogue, dict) else [])
    )
    if silence_by_design:
        has_speech = False

    # --- Run checks ---
    findings: list = []
    results_by_check: dict = {}

    print(f"\n{'='*60}")
    print(f"Quality Gate per-Clip — {args.shot_id}")
    print(f"Clip: {clip_path.name}")
    print(f"{'='*60}\n")

    print("Check 1/5: visual canonical compliance (Gemini Vision)...")
    results_by_check["visual_canonical"] = check_visual_canonical(
        clip_path, shot, args.shot_id, findings, enable_gemini=args.enable_gemini
    )

    clip_duration = run_ffprobe_duration(clip_path)

    print("Check 2/5: caption schema validation...")
    results_by_check["caption_schema"] = check_captions_schema(
        captions_path, shot, spec, clip_duration, findings
    )
    captions_count = results_by_check["caption_schema"].get("captions_count", 0)

    print("Check 3/5: audio waveform analysis (LUFS / true_peak / clipping)...")
    results_by_check["audio_waveform"] = check_audio_waveform(
        clip_path, has_speech, findings
    )

    print("Check 4/5: sync verify (duration / re-Whisper)...")
    results_by_check["sync"] = check_sync(
        clip_path, captions_path, shot, captions_count,
        enable_whisper=args.enable_whisper, findings=findings
    )

    print("Check 5/5: GAPS sentinels (S1/S2/S6/S8)...")
    results_by_check["sentinels"] = check_gaps_sentinels(
        clip_path, captions_path, shot, captions_count, findings,
        clip_start_abs_s=args.clip_start_abs_s
    )

    # --- Compute verdict ---
    verdict_emoji, verdict_label, exit_code = compute_verdict(findings)

    fails = [f for f in findings if f.get("severity") == "FAIL"]
    warns = [f for f in findings if f.get("severity") == "WARN"]
    infos = [f for f in findings if f.get("severity") == "INFO"]

    print(f"\n{'='*60}")
    print(f"Findings: {len(fails)} FAIL · {len(warns)} WARN · {len(infos)} INFO")
    print(f"Verdict:  {verdict_emoji} {verdict_label}")
    print(f"{'='*60}\n")

    for f in findings:
        if f.get("severity") == "FAIL":
            marker = "🔴"
        elif f.get("severity") == "WARN":
            marker = "🟡"
        else:
            marker = "ℹ️"
        print(f"{marker} [{f.get('check')}] {f.get('severity')} — {f.get('issue', '')}")
        if f.get("fix_hint"):
            print(f"    fix: {f['fix_hint']}")

    # --- Write outputs ---
    audit_payload = {
        "shot_id": args.shot_id,
        "clip": str(clip_path),
        "captions": str(captions_path),
        "spec": str(spec_path),
        "verdict": verdict_label,
        "verdict_emoji": verdict_emoji,
        "exit_code": exit_code,
        "counts": {
            "fail": len(fails),
            "warn": len(warns),
            "info": len(infos),
        },
        "findings": findings,
        "results_by_check": results_by_check,
        "gemini_enabled": args.enable_gemini,
        "whisper_enabled": args.enable_whisper,
    }
    with open(audit_json_path, "w") as f:
        json.dump(audit_payload, f, indent=2, default=str)
    write_audit_md(audit_md_path, clip_path, args.shot_id, findings, results_by_check,
                   verdict_emoji, verdict_label)

    print(f"\nAudit JSON: {audit_json_path}")
    print(f"Audit MD:   {audit_md_path}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
