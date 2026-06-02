#!/usr/bin/env python3
"""
build_clip_atomic.py — Per-clip atomic assembly pipeline (Phase 2 architectural refactor).

Builds self-contained AVU per clip: visual + audio (TTS + SFX + optional AVU overlay) +
caption sidecar JSON + manifest. Eliminates end-of-timeline sync drift bug class by
making each shot an atomic unit that can be verified independently before concat.

References:
  - memory feedback_per_clip_atomic_assembly (architectural insight 2026-05-20)
  - INGENIERO-PAUTA-MASTER § 9 mix levels (volumes canónicos)
  - Hard Rule #9: narration 1.0, music 0.05-0.18, SFX events 0.20-0.35, flash 0.55-0.65

Methodology per clip:
  1. Read SPEC creative-specs/<id>.yaml + extract shot_NN metadata
  2. Load Hailuo clip (visual only): assets/clips/shot_NN.mp4
  3. Resolve TTS segments aligned to shot's timestamp window (per spec narration_script + manifest)
  4. Resolve SFX events whose timestamps fall within shot window
  5. Compose per-clip audio mix (ffmpeg amix with adelay per source)
  6. Mux video + composed audio → shot_NN_atomic.mp4
  7. Optional: overlay AVU asset (countdown / decision-freeze / outro)
  8. Generate caption sidecar JSON for this clip's window (relative timing)
  9. Generate manifest JSON with audit metadata (duration, LUFS, peaks)

Usage:
  # single shot
  python build_clip_atomic.py \\
    --spec ../creative-specs/cinema-abandonado.yaml \\
    --shot-id shot_01_hook \\
    --output-dir assets/clips-atomic/

  # batch all shots in SPEC
  python build_clip_atomic.py \\
    --spec ../creative-specs/cinema-abandonado.yaml \\
    --batch \\
    --output-dir assets/clips-atomic/

  # with AVU overlay (hook countdown LAST 3s)
  python build_clip_atomic.py \\
    --spec ../creative-specs/cinema-abandonado.yaml \\
    --shot-id shot_01_hook \\
    --avu countdown \\
    --output-dir assets/clips-atomic/

Outputs per shot:
  <output-dir>/<shot_id>_atomic.mp4      (self-contained video+audio)
  <output-dir>/<shot_id>_captions.json   (sidecar with relative timing)
  <output-dir>/<shot_id>_manifest.json   (audit metadata)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# Whisper is imported lazily inside bake_captions_per_clip() so the rest of the
# script keeps working when Whisper is not installed (e.g. legacy atomic builds).


# ----------------------------------------------------------------------------
# Canonical mix levels (Hard Rule #9 + INGENIERO-PAUTA-MASTER § 9)
# ----------------------------------------------------------------------------
MIX_NARRATION_DEFAULT = 1.0
MIX_SFX_EVENT_DEFAULT = 0.28          # within 0.20-0.35 band
MIX_FLASH_IMPACT_DEFAULT = 0.60       # within 0.55-0.65 band
MIX_AMBIENT_CONTINUOUS_DEFAULT = 0.14 # within 0.10-0.18 band

# LUFS target (Instagram Reels standard)
LUFS_TARGET = -14.0
LUFS_TOLERANCE = 1.5  # ±1.5 dB acceptable per-clip (final master tightens to ±0.5)


# ----------------------------------------------------------------------------
# Caption-burn canonical styling (Hard Rule #4 + CAPTIONS.md 3-class system)
# ----------------------------------------------------------------------------
# Y position: 62% of frame (canonical safe zone, IG Reel 9:16)
CAPTION_Y_PERCENT = 0.62
# ── CAPTION-OVERLAP fix — per-speaker/per-class Y-band + build-time de-conflict ──
# Narrator/warning captions sit at the canonical Y62 bottom-third. Character DIALOG (name class)
# sits at Y52 + NAME tag, so narrator + dialog (or 2 chars) NEVER collide at the same Y when their
# time windows overlap. De-conflict (deconflict_cue_ys) ENFORCES the A3 "no same-Y overlap" invariant
# in the burn (cross-layer narrator + dialog included) instead of only flagging it in a sidecar.
CAPTION_Y_NARRATOR = 0.62      # narration / warning
CAPTION_Y_DIALOG = 0.52        # character dialog (name class) — distinct band + NAME tag
CAPTION_Y_STEP = 0.08          # de-conflict offset step (≥6% min separation = ≥1 line height)
CAPTION_Y_MIN = 0.30           # don't push a caption above the lower-third / into the name-label band
# Font size scaling: 80px base for short captions, 68px when word count > 8
CAPTION_FONT_SIZE_SHORT = 80
CAPTION_FONT_SIZE_LONG = 68
CAPTION_LONG_WORD_THRESHOLD = 8
# Drop shadow: ~2px black offset (per referent_validated_patterns)
CAPTION_SHADOW_OFFSET_PX = 2
# Class palette (BGR-less; ffmpeg drawtext takes 0xRRGGBB or named colors)
CAPTION_COLOR_NARRATION = "white"
CAPTION_COLOR_WARNING = "red"
CAPTION_COLOR_NAME = "white"  # character-name label
CAPTION_SHADOW_COLOR = "black"

# Font file resolution — prefer monospaced for name-class, sans-serif for narration.
# macOS-friendly defaults; can be overridden via style_overrides.
DEFAULT_NARRATION_FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial Bold.ttf",
]
DEFAULT_MONO_FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/SFNSMono.ttf",
    "/System/Library/Fonts/Courier.ttc",
]


def _resolve_font(candidates: list[str]) -> str | None:
    for c in candidates:
        if Path(c).exists():
            return c
    return None


def _normalize_for_compare(text: str) -> set[str]:
    """Lowercase + strip punctuation + return word set for overlap comparison."""
    cleaned = re.sub(r"[^\w\sáéíóúñü]+", " ", text.lower(), flags=re.UNICODE)
    tokens = [t for t in cleaned.split() if len(t) >= 2]
    return set(tokens)


def _token_overlap_ratio(a: str, b: str) -> float:
    """Return |a ∩ b| / max(|a|, |b|) on token sets (case + punct insensitive)."""
    sa = _normalize_for_compare(a)
    sb = _normalize_for_compare(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / max(len(sa), len(sb))


# ----------------------------------------------------------------------------
# ffmpeg / ffprobe helpers
# ----------------------------------------------------------------------------
def run(cmd: list[str], capture: bool = False, check: bool = True) -> subprocess.CompletedProcess:
    """Run shell command, raise on error."""
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)
    return subprocess.run(cmd, check=check)


def ffprobe_duration(path: Path) -> float:
    """Return media duration in seconds."""
    if not path.exists():
        raise FileNotFoundError(f"ffprobe target missing: {path}")
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(path),
    ]
    result = run(cmd, capture=True)
    return float(result.stdout.strip())


def ffprobe_lufs(path: Path) -> float | None:
    """Measure integrated LUFS of audio in media file. Returns None if cannot measure."""
    cmd = [
        "ffmpeg", "-hide_banner", "-i", str(path),
        "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        stderr = result.stderr
        # Extract JSON block at end of stderr
        match = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", stderr, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group(0))
        return float(data.get("input_i", "0"))
    except Exception:
        return None


def ffprobe_peak_db(path: Path) -> float | None:
    """Measure peak dBFS of audio in media. Returns None if cannot measure."""
    cmd = [
        "ffmpeg", "-hide_banner", "-i", str(path),
        "-af", "volumedetect",
        "-f", "null", "-",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        match = re.search(r"max_volume:\s*(-?[\d.]+)\s*dB", result.stderr)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return None


# ----------------------------------------------------------------------------
# SPEC loaders
# ----------------------------------------------------------------------------
def load_spec(spec_path: Path) -> dict[str, Any]:
    """Load creative-specs/<id>.yaml."""
    if not spec_path.exists():
        raise FileNotFoundError(f"SPEC not found: {spec_path}")
    with open(spec_path) as f:
        return yaml.safe_load(f)


def find_shot(spec: dict, shot_id: str) -> dict | None:
    """Return shot dict matching shot_id (or first prefix match)."""
    shots = spec.get("shot_list", [])
    for shot in shots:
        if shot.get("id") == shot_id:
            return shot
    # Try prefix match (e.g. "shot_01" matches "shot_01_hook")
    for shot in shots:
        if shot.get("id", "").startswith(shot_id):
            return shot
    return None


def parse_timestamp_intent(shot: dict) -> tuple[float, float]:
    """Extract (start_s, end_s) from shot timestamp_intent like '0-9s'."""
    raw = shot.get("timestamp_intent", "")
    match = re.match(r"([\d.]+)\s*-\s*([\d.]+)", str(raw))
    if not match:
        # fallback: duration_intent_s + assume start at 0
        dur = shot.get("duration_intent_s", 0)
        return (0.0, float(dur))
    return (float(match.group(1)), float(match.group(2)))


def resolve_narration_segments(spec: dict, shot_start: float, shot_end: float) -> list[dict]:
    """Return narration segments whose timestamp_intent_s overlaps [shot_start, shot_end]."""
    segments = spec.get("narration_script", {}).get("segments", [])
    out = []
    for seg in segments:
        ts = seg.get("timestamp_intent_s")
        if not (isinstance(ts, list) and len(ts) == 2):
            continue
        seg_start, seg_end = float(ts[0]), float(ts[1])
        # overlap test
        if seg_end <= shot_start or seg_start >= shot_end:
            continue
        out.append({
            "id": seg.get("id"),
            "speaker": seg.get("speaker", "narrator"),
            "text": seg.get("text_canonical", ""),
            "global_start_s": seg_start,
            "global_end_s": seg_end,
            "local_start_s": max(0.0, seg_start - shot_start),
            "local_end_s": min(shot_end - shot_start, seg_end - shot_start),
        })
    return out


def resolve_sfx_events(sfx_events: list[dict], shot_start: float, shot_end: float) -> list[dict]:
    """Return SFX events whose start_s falls within shot window."""
    out = []
    for ev in sfx_events:
        start_s = float(ev.get("start_s", 0))
        if shot_start <= start_s < shot_end:
            new_ev = dict(ev)
            new_ev["local_start_s"] = start_s - shot_start
            out.append(new_ev)
    return out


# ----------------------------------------------------------------------------
# Asset resolvers
# ----------------------------------------------------------------------------
def find_clip_visual(project_root: Path, shot_id: str) -> Path | None:
    """Look for assets/clips/<shot_id>.mp4 — prefer variant-less, fallback to -a."""
    clips_dir = project_root / "assets" / "clips"
    candidates = [
        clips_dir / f"{shot_id}.mp4",
        clips_dir / f"{shot_id}-a.mp4",
    ]
    for c in candidates:
        if c.exists():
            return c
    # any file starting with shot_id
    if clips_dir.exists():
        matches = sorted(clips_dir.glob(f"{shot_id}*.mp4"))
        # filter out iter backups
        matches = [m for m in matches if "iter" not in m.stem and "backup" not in m.stem]
        if matches:
            return matches[0]
    return None


def find_tts_segment(project_root: Path, segment_id: str) -> Path | None:
    """Look for assets/tts/<segment_id>.mp3."""
    tts_dir = project_root / "assets" / "tts"
    candidate = tts_dir / f"{segment_id}.mp3"
    return candidate if candidate.exists() else None


def find_sfx_asset(project_root: Path, base_root: Path, sfx_path: str) -> Path | None:
    """Resolve SFX asset — supports project-relative AND base-relative (library/) paths."""
    if sfx_path.startswith("library/"):
        candidate = base_root / sfx_path
    elif "/" in sfx_path:
        # e.g. 'cinema-abandonado/assets/sfx/foo.mp3'
        candidate = base_root / sfx_path
        if not candidate.exists():
            # try as project-relative
            candidate = project_root / sfx_path
    else:
        candidate = project_root / "assets" / "sfx" / sfx_path
    return candidate if candidate.exists() else None


def find_avu_asset(base_root: Path, avu_type: str) -> Path | None:
    """Look up AVU template by type."""
    avu_dir = base_root / ".claude/skills/ai-video-production/templates/avu-library"
    mapping = {
        "countdown": "countdown-3-2-1-film-leader-with-ticks.mp4",
        "decision-freeze": "decision-freeze-with-tick-3-2-1.mp4",
        "decision_freeze": "decision-freeze-with-tick-3-2-1.mp4",
        "hook-transition": "hook-transition-warm-whoosh.mp4",
        "outro": "outro-card-template.mp4",
        "outro-card": "outro-card-template.mp4",
    }
    fname = mapping.get(avu_type)
    if not fname:
        return None
    candidate = avu_dir / fname
    return candidate if candidate.exists() else None


# ----------------------------------------------------------------------------
# Audio composition
# ----------------------------------------------------------------------------
def build_audio_mix_filter(
    inputs: list[dict],
    total_duration_s: float,
) -> tuple[list[str], str]:
    """
    Build ffmpeg -filter_complex graph for mixing N audio inputs at given offsets+volumes.

    `inputs` is a list of:
      {"path": Path, "offset_s": float, "volume": float, "label": str}

    Returns (ffmpeg_input_args, filter_complex_str, output_label).
    """
    if not inputs:
        return [], ""

    input_args = []
    filter_parts = []
    mix_labels = []

    for idx, src in enumerate(inputs):
        input_args.extend(["-i", str(src["path"])])
        offset_ms = int(round(src["offset_s"] * 1000))
        vol = src["volume"]
        in_label = f"{idx + 1}:a"  # input #(idx+1) since input 0 is video
        out_label = f"a{idx}"
        # adelay applies offset, volume scales amplitude, asetpts maintains timing
        filter_parts.append(
            f"[{in_label}]adelay={offset_ms}|{offset_ms},volume={vol}[{out_label}]"
        )
        mix_labels.append(f"[{out_label}]")

    # amix N inputs, normalize=0 keeps absolute volumes
    n = len(mix_labels)
    filter_parts.append(
        f"{''.join(mix_labels)}amix=inputs={n}:duration=longest:normalize=0[amix]"
    )
    # trim final to shot duration + light fade-out to avoid clicks
    fade_start = max(0.0, total_duration_s - 0.05)
    filter_parts.append(
        f"[amix]atrim=duration={total_duration_s},"
        f"afade=t=out:st={fade_start:.3f}:d=0.05[aout]"
    )

    return input_args, ";".join(filter_parts)


def compose_atomic_audio_video(
    visual_path: Path,
    audio_sources: list[dict],
    shot_duration_s: float,
    output_path: Path,
) -> None:
    """
    Mux visual + composed audio mix into atomic clip.
    If no audio sources: copy visual + silent track of shot_duration_s.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not audio_sources:
        # Silent track
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
            "-i", str(visual_path),
            "-f", "lavfi", "-t", f"{shot_duration_s}",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            str(output_path),
        ]
        run(cmd)
        return

    input_args, filter_complex = build_audio_mix_filter(audio_sources, shot_duration_s)

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(visual_path),
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-ar", "48000",
        str(output_path),
    ]
    run(cmd)


def overlay_avu(
    base_clip: Path,
    avu_path: Path,
    inject_at_local_s: float,
    output_path: Path,
) -> None:
    """
    Overlay AVU video on top of base_clip starting at inject_at_local_s.
    AVU audio is mixed in (preserves base audio).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    offset_ms = int(round(inject_at_local_s * 1000))
    # filter:
    #   - [1:v]setpts shifts AVU start
    #   - overlay enables AVU only after inject_at_local_s
    #   - [1:a] adelay shifts AVU audio
    #   - amix mixes base audio + AVU audio
    fc = (
        f"[1:v]setpts=PTS-STARTPTS+{inject_at_local_s}/TB[avuv];"
        f"[0:v][avuv]overlay=enable='gte(t,{inject_at_local_s})':eof_action=pass[vout];"
        f"[1:a]adelay={offset_ms}|{offset_ms}[avua];"
        f"[0:a][avua]amix=inputs=2:duration=first:normalize=0[aout]"
    )

    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-i", str(base_clip),
        "-i", str(avu_path),
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path),
    ]
    run(cmd)


# ----------------------------------------------------------------------------
# Captions sidecar
# ----------------------------------------------------------------------------
def build_caption_sidecar(
    shot_id: str,
    shot_start_s: float,
    shot_end_s: float,
    narration_segments: list[dict],
) -> dict:
    """
    Build captions sidecar JSON for this clip's window with RELATIVE timing.

    Output schema:
      { "shot_id": ..., "duration_s": ..., "global_window": [...],
        "captions": [ { id, text, speaker, local_start_s, local_end_s, global_start_s, global_end_s } ] }
    """
    captions = []
    for seg in narration_segments:
        captions.append({
            "id": seg["id"],
            "speaker": seg["speaker"],
            "text": seg["text"],
            "local_start_s": round(seg["local_start_s"], 3),
            "local_end_s": round(seg["local_end_s"], 3),
            "global_start_s": round(seg["global_start_s"], 3),
            "global_end_s": round(seg["global_end_s"], 3),
        })
    return {
        "shot_id": shot_id,
        "duration_s": round(shot_end_s - shot_start_s, 3),
        "global_window_s": [round(shot_start_s, 3), round(shot_end_s, 3)],
        "captions": captions,
        "format_version": "atomic_v1",
        "notes": "Local timing is relative to shot start. Global timing is the original SPEC absolute timeline.",
    }


# ----------------------------------------------------------------------------
# Manifest (audit metadata)
# ----------------------------------------------------------------------------
def build_manifest(
    shot_id: str,
    spec_intent_duration_s: float,
    actual_duration_s: float,
    audio_sources: list[dict],
    narration_segments: list[dict],
    sfx_events: list[dict],
    output_path: Path,
    avu_used: str | None,
) -> dict:
    """Build per-clip manifest with audit metadata."""
    lufs = ffprobe_lufs(output_path)
    peak_db = ffprobe_peak_db(output_path)

    duration_delta = actual_duration_s - spec_intent_duration_s
    duration_ok = abs(duration_delta) < 0.5

    lufs_ok = lufs is not None and abs(lufs - LUFS_TARGET) <= LUFS_TOLERANCE
    peak_ok = peak_db is None or peak_db <= -0.5

    return {
        "shot_id": shot_id,
        "format_version": "atomic_v1",
        "spec_intent_duration_s": round(spec_intent_duration_s, 3),
        "actual_duration_s": round(actual_duration_s, 3),
        "duration_delta_s": round(duration_delta, 3),
        "duration_ok": duration_ok,
        "audio": {
            "sources_count": len(audio_sources),
            "narration_segments": [s["id"] for s in narration_segments],
            "sfx_events_count": len(sfx_events),
            "lufs_integrated": lufs,
            "lufs_target": LUFS_TARGET,
            "lufs_in_band": lufs_ok,
            "peak_db": peak_db,
            "peak_ok": peak_ok,
        },
        "avu_overlay": avu_used,
        "audit_status": "PASS" if (duration_ok and lufs_ok and peak_ok) else "REVIEW",
    }


# ----------------------------------------------------------------------------
# Caption baking (Whisper-derived timing + ffmpeg drawtext burn-in)
# ----------------------------------------------------------------------------
def _escape_drawtext(text: str) -> str:
    """
    Escape text for ffmpeg drawtext value enclosed in single quotes.
    The drawtext arg is built as: text='...'. Inside single quotes ffmpeg only
    needs ' and \\ escaped (and we additionally guard : and % which can be
    interpreted in some ffmpeg builds when the value isn't quoted properly).
    """
    if text is None:
        return ""
    out = text
    out = out.replace("\\", "\\\\")  # literal backslash
    out = out.replace("'", r"\'")      # single quote
    out = out.replace(":", r"\:")
    out = out.replace("%", r"\%")
    # Normalize whitespace and strip
    out = " ".join(out.split())
    return out


def _whisper_transcribe(audio_path: Path, language: str = "es", model_name: str = "base") -> dict:
    """
    Transcribe audio with Whisper. Returns dict with 'text', 'segments', 'words'.
    If audio is silent or has no speech, returns {'text': '', 'segments': [], 'words': []}.
    """
    import whisper  # lazy import

    model = whisper.load_model(model_name)
    result = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=True,
        verbose=False,
        fp16=False,
        condition_on_previous_text=False,
    )
    segments = result.get("segments", []) or []
    text = (result.get("text") or "").strip()

    # Flatten word-level timestamps
    words = []
    for seg in segments:
        for w in seg.get("words", []) or []:
            tok = (w.get("word") or "").strip()
            if not tok:
                continue
            words.append({
                "word": tok,
                "start": float(w.get("start", 0)),
                "end": float(w.get("end", 0)),
            })

    return {"text": text, "segments": segments, "words": words}


def _classify_caption(speaker: str | None, text: str) -> str:
    """
    Return one of: 'narration' | 'warning' | 'name'.
    Heuristic:
      - speaker looks like a proper name (single capitalized token) -> name
      - text contains warning markers (exclamation density / shout words) -> warning
      - else narration
    """
    if speaker:
        s = speaker.strip()
        # Common narrator labels
        if s.lower() in {"narrator", "narrador", "voz", "voz en off"}:
            return "narration"
        # Single capitalized token of length 2..20 -> treat as character name label
        if re.fullmatch(r"[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{1,19}", s):
            return "name"
    # Warning detection: 2+ exclamations or shout keywords
    if text:
        if text.count("!") + text.count("¡") >= 2:
            return "warning"
        if re.search(r"\b(corre|cuidado|peligro|huye|no\b)\b", text.lower()):
            # Only flag as warning if text is short + exclamatory enough; soften default
            if "!" in text or "¡" in text:
                return "warning"
    return "narration"


# Caption chunking: máx palabras por cue progresivo (<=2 líneas al quemar). HR#30.
CAPTION_MAX_WORDS_PER_CUE = 6


def _chunk_text_over_word_timestamps(
    spec_text: str, words: list[dict], speaker: str | None,
    max_words: int = CAPTION_MAX_WORDS_PER_CUE,
) -> list[dict]:
    """Distribuye el wording del SPEC sobre los word-timestamps de Whisper como cues
    PROGRESIVOS word-timed (<= max_words c/u), para que el burn muestre TODA la narración
    en el tiempo — no un bloque estático que el wrap trunca a la 1ª línea (bug V5/V6, HR#30).
    El SPEC es autoridad del wording; Whisper aporta solo el timing (alineación POSICIONAL/
    proporcional, robusta a drift de conteo SPEC-vs-audio)."""
    spec_words = spec_text.split()
    if not spec_words or not words:
        return []
    n_spec, n_whis = len(spec_words), len(words)
    cues: list[dict] = []
    for i in range(0, n_spec, max_words):
        chunk = spec_words[i:i + max_words]
        last_idx = i + len(chunk) - 1
        ws = min(round(i * n_whis / n_spec), n_whis - 1)
        we = max(min(round(last_idx * n_whis / n_spec), n_whis - 1), ws)
        start_s = float(words[ws]["start"])
        end_s = float(words[we]["end"])
        if cues and start_s < cues[-1]["end_s"]:
            start_s = cues[-1]["end_s"]
        if end_s <= start_s:
            end_s = start_s + 0.4
        text = " ".join(chunk)
        cues.append({
            "start_s": start_s, "end_s": end_s, "text": text,
            "class": _classify_caption(speaker, text), "speaker": speaker,
        })
    return cues


def _chunk_text_over_span(
    spec_text: str, start_s: float, end_s: float, speaker: str | None,
    max_words: int = CAPTION_MAX_WORDS_PER_CUE,
) -> list[dict]:
    """Sin word-timestamps: distribuye el wording del SPEC uniformemente sobre [start_s, end_s]
    como cues progresivos (en vez de 1 bloque)."""
    spec_words = spec_text.split()
    if not spec_words:
        return []
    total = max(end_s - start_s, 0.1)
    n_chunks = (len(spec_words) + max_words - 1) // max_words
    cues: list[dict] = []
    for c in range(n_chunks):
        chunk = spec_words[c * max_words:(c + 1) * max_words]
        text = " ".join(chunk)
        cues.append({
            "start_s": start_s + total * (c / n_chunks),
            "end_s": start_s + total * ((c + 1) / n_chunks),
            "text": text, "class": _classify_caption(speaker, text), "speaker": speaker,
        })
    return cues


def _build_caption_cues_from_whisper(
    whisper_result: dict,
    spec_text_override: str | None,
    speaker: str | None,
) -> list[dict]:
    """
    Return list of {start_s, end_s, text, class} cues.

    Strategy (HR#30 — caption TEMPORAL coverage, NUNCA bloque estático):
      - spec_text_override + words: el wording del SPEC se CHUNKEA word-timed en cues
        progresivos (<=6 palabras c/u) vía _chunk_text_over_word_timestamps.
      - spec_text_override + segments sin words: se distribuye uniforme sobre el span.
      - Whisper raw (sin override): un cue por segmento; segmentos largos en grupos de ~6.
    """
    segments = whisper_result.get("segments", []) or []
    words = whisper_result.get("words", []) or []

    if not segments and not words:
        return []

    if spec_text_override and words:
        return _chunk_text_over_word_timestamps(spec_text_override, words, speaker)

    if spec_text_override and segments and not words:
        # Sin word-timestamps: distribuir el wording del SPEC sobre el span de segmentos.
        first = float(segments[0].get("start", 0))
        last = float(segments[-1].get("end", first))
        return _chunk_text_over_span(spec_text_override, first, last, speaker)

    # Whisper raw: one cue per segment, but split very long segments into ~6-word chunks
    cues = []
    for seg in segments:
        seg_text = (seg.get("text") or "").strip()
        if not seg_text:
            continue
        seg_words = seg.get("words", []) or []
        if len(seg_words) > 8:
            # Chunk into groups of ~6 words
            for i in range(0, len(seg_words), 6):
                chunk = seg_words[i:i + 6]
                if not chunk:
                    continue
                chunk_text = " ".join((w.get("word") or "").strip() for w in chunk).strip()
                if not chunk_text:
                    continue
                cues.append({
                    "start_s": float(chunk[0].get("start", 0)),
                    "end_s": float(chunk[-1].get("end", 0)),
                    "text": chunk_text,
                    "class": _classify_caption(speaker, chunk_text),
                    "speaker": speaker,
                })
        else:
            cues.append({
                "start_s": float(seg.get("start", 0)),
                "end_s": float(seg.get("end", 0)),
                "text": seg_text,
                "class": _classify_caption(speaker, seg_text),
                "speaker": speaker,
            })
    return cues


def _base_y_for_class(klass: str) -> float:
    """Canonical base Y per caption class. Dialog (name) -> Y52; narration/warning -> Y62."""
    return CAPTION_Y_DIALOG if klass == "name" else CAPTION_Y_NARRATOR


def deconflict_cue_ys(cues: list[dict]) -> list[dict]:
    """CAPTION-OVERLAP fix — assign each cue a per-class base Y, then resolve same-Y temporal
    collisions so NO two TIME-overlapping cues share a Y band (cross-layer narration+dialog AND
    char-vs-char). The later-starting cue is pushed UP by CAPTION_Y_STEP (clamped at CAPTION_Y_MIN;
    nudged down if it would breach the floor). Sets cue['y_pct'] in place. Idempotent/deterministic."""
    for c in cues:
        c.setdefault("y_pct", _base_y_for_class(c.get("class", "narration")))
    # narration/warning sort before dialog at the same start so the narrator keeps the canonical band
    ordered = sorted(cues, key=lambda c: (float(c["start_s"]),
                                          0 if c.get("class") != "name" else 1))
    for i, c in enumerate(ordered):
        moved = True
        while moved:
            moved = False
            for j in range(i):
                p = ordered[j]
                overlaps = float(c["start_s"]) < float(p["end_s"]) - 0.05 and \
                    float(c["end_s"]) > float(p["start_s"]) + 0.05
                same_band = abs(c["y_pct"] - p["y_pct"]) < (CAPTION_Y_STEP - 0.001)
                if overlaps and same_band:
                    new_y = round(c["y_pct"] - CAPTION_Y_STEP, 4)
                    if new_y < CAPTION_Y_MIN:
                        new_y = round(c["y_pct"] + CAPTION_Y_STEP, 4)
                    c["y_pct"] = new_y
                    moved = True
                    break
    return ordered


def _wrap_text_lines(text: str, max_chars_per_line: int = 22) -> list[str]:
    """Break long text into multiple lines on word boundaries."""
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current: list[str] = []
    for w in words:
        candidate = " ".join(current + [w])
        if len(candidate) <= max_chars_per_line or not current:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def _drawtext_filters_for_cue(
    cue: dict,
    video_height: int,
    video_width: int,
    font_narration: str | None,
    font_mono: str | None,
) -> list[str]:
    """
    Build drawtext= filter expressions for a single cue.
    Returns ONE expression per text line (auto-wrapped if needed).
    Lines stack vertically around Y 62%.
    """
    text = cue["text"]
    klass = cue.get("class", "narration")
    # Dialog (name class): prefix a NAME tag so the viewer knows who speaks + it reads distinct
    # from the narrator band (CAPTION-OVERLAP fix). Speaker carried on the cue when available.
    spk = (cue.get("speaker") or "").strip()
    if klass == "name" and spk and not text.upper().startswith(spk.upper() + ":"):
        text = f"{spk.upper()}: {text}"
    words_count = len(text.split())
    fontsize = CAPTION_FONT_SIZE_LONG if words_count > CAPTION_LONG_WORD_THRESHOLD else CAPTION_FONT_SIZE_SHORT

    if klass == "name":
        color = CAPTION_COLOR_NAME
        fontfile = font_mono or font_narration
    elif klass == "warning":
        color = CAPTION_COLOR_WARNING
        fontfile = font_narration
    else:
        color = CAPTION_COLOR_NARRATION
        fontfile = font_narration

    # Auto-wrap heuristic: for 1080-wide @ 80px ~22 chars/line; @ 68px ~26 chars/line.
    max_chars = 22 if fontsize == CAPTION_FONT_SIZE_SHORT else 26
    # Tighter wrap for narrower videos
    if video_width and video_width < 1000:
        max_chars = int(max_chars * video_width / 1080)

    lines = _wrap_text_lines(text, max_chars_per_line=max_chars)
    if not lines:
        return []

    # Vertical stacking: center the block of N lines around CAPTION_Y_PERCENT.
    # Each line takes ~1.2 * fontsize px vertically.
    line_height = int(round(fontsize * 1.2))
    n = len(lines)
    block_height = n * line_height
    # Top of block:
    top_offset = - block_height / 2

    # per-cue Y band (CAPTION-OVERLAP fix). Falls back to canonical Y62 if not de-conflicted.
    cue_y = cue.get("y_pct", CAPTION_Y_PERCENT)
    filters = []
    for i, line in enumerate(lines):
        escaped = _escape_drawtext(line)
        # y = h*cue_y + (i - (n-1)/2) * line_height  -> centered around the cue's band
        y_expr = f"h*{cue_y}+({i}-{(n - 1) / 2:.2f})*{line_height}"
        parts = [
            f"text='{escaped}'",
            f"fontsize={fontsize}",
            f"fontcolor={color}",
            f"x=(w-text_w)/2",
            f"y={y_expr}",
            f"shadowcolor={CAPTION_SHADOW_COLOR}",
            f"shadowx={CAPTION_SHADOW_OFFSET_PX}",
            f"shadowy={CAPTION_SHADOW_OFFSET_PX}",
            f"borderw=1",
            f"bordercolor={CAPTION_SHADOW_COLOR}",
            f"enable='between(t,{cue['start_s']:.3f},{cue['end_s']:.3f})'",
        ]
        if fontfile:
            ff_escaped = fontfile.replace(":", r"\:").replace("'", r"\'")
            parts.insert(1, f"fontfile='{ff_escaped}'")
        filters.append("drawtext=" + ":".join(parts))
    return filters


def bake_captions_per_clip(
    clip_path: Path,
    spec_shot: dict,
    output_path: Path,
    style_overrides: dict | None = None,
) -> dict:
    """
    Bake captions per clip from Whisper-derived timing + optional SPEC text override.

    Methodology:
      1. Extract audio from clip via ffmpeg (-vn -acodec libmp3lame).
      2. Whisper transcribe with word_timestamps=True, model='base', language='es'.
      3. If no speech detected -> copy clip unchanged.
      4. If spec_shot has 'text_canonical' (or 'narration_canonical') -> use SPEC text with Whisper timing.
      5. Else -> use Whisper text + Whisper timing.
      6. Apply ffmpeg drawtext to burn captions into video frames per Hard Rule #4.
      7. Preserve original audio (-c:a copy).

    Args:
      clip_path: source mp4 (must exist).
      spec_shot: dict from SPEC.shot_list[N] OR minimal dict {'id', 'text_canonical', 'speaker'}.
      output_path: destination mp4.
      style_overrides: optional dict {'font_narration', 'font_mono', 'language', 'model_name',
                                       'y_percent', 'force_class'}.

    Returns: {'success': bool, 'captions_burned': int, 'no_speech_detected': bool,
              'whisper_text': str, 'spec_text_used': bool, 'output_path': str,
              'cues': [...], 'error': str | None}
    """
    style_overrides = style_overrides or {}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "success": False,
        "captions_burned": 0,
        "no_speech_detected": False,
        "whisper_text": "",
        "spec_text_used": False,
        "sidecar_rejected": False,
        "output_path": str(output_path),
        "cues": [],
        "error": None,
    }

    if not clip_path.exists():
        result["error"] = f"clip not found: {clip_path}"
        return result

    # Detect whether clip has an audio stream
    probe_audio = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=codec_type",
            "-of", "csv=p=0",
            str(clip_path),
        ],
        capture_output=True, text=True, check=False,
    )
    has_audio_stream = bool(probe_audio.stdout.strip())

    # Extract audio for Whisper. If no audio stream, we still produce a passthrough.
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        audio_path = td_path / "clip_audio.mp3"

        if has_audio_stream:
            try:
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(clip_path),
                        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
                        str(audio_path),
                    ],
                    check=True, capture_output=True, text=True,
                )
            except subprocess.CalledProcessError as e:
                result["error"] = f"ffmpeg audio extract failed: {e.stderr}"
                return result
        else:
            # No audio stream → flag and passthrough
            result["no_speech_detected"] = True

        if has_audio_stream and audio_path.exists():
            try:
                whisper_res = _whisper_transcribe(
                    audio_path,
                    language=style_overrides.get("language", "es"),
                    model_name=style_overrides.get("model_name", "base"),
                )
            except Exception as e:
                result["error"] = f"whisper transcription failed: {e}"
                return result

            result["whisper_text"] = whisper_res["text"]
            if not whisper_res["text"].strip():
                result["no_speech_detected"] = True
        else:
            whisper_res = {"text": "", "segments": [], "words": []}

        # If no speech detected → pass-through (deterministic copy)
        if result["no_speech_detected"]:
            try:
                # Stream-copy to preserve quality + bit-exactness
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-i", str(clip_path),
                        "-c", "copy",
                        "-map", "0",
                        str(output_path),
                    ],
                    check=True, capture_output=True, text=True,
                )
                result["success"] = True
                return result
            except subprocess.CalledProcessError as e:
                # Fallback: shutil copy
                try:
                    shutil.copyfile(clip_path, output_path)
                    result["success"] = True
                    return result
                except Exception as ee:
                    result["error"] = f"passthrough failed: ffmpeg={e.stderr} shutil={ee}"
                    return result

        # SPEC text override resolution
        spec_text = (
            spec_shot.get("text_canonical")
            or spec_shot.get("narration_canonical")
            or spec_shot.get("text")
        )
        if isinstance(spec_text, dict):
            spec_text = spec_text.get("text") or None
        spec_text = (spec_text or "").strip() or None
        speaker = spec_shot.get("speaker") or spec_shot.get("character") or None

        # Sidecar-trust guard: if the SPEC text wildly diverges from Whisper text,
        # reject the override and fall back to Whisper-derived text.
        # Threshold: token-overlap ratio < 0.30 ⇒ untrusted.
        # This is the adversarial safety net per task spec A2 + ADV-A.
        sidecar_rejected = False
        if spec_text and whisper_res.get("text"):
            overlap = _token_overlap_ratio(spec_text, whisper_res["text"])
            threshold = float(style_overrides.get("sidecar_similarity_threshold", 0.30))
            if overlap < threshold:
                sidecar_rejected = True
                if not style_overrides.get("force_spec_text"):
                    spec_text = None
        result["sidecar_rejected"] = sidecar_rejected
        result["spec_text_override_input"] = (
            spec_shot.get("text_canonical")
            or spec_shot.get("narration_canonical")
            or spec_shot.get("text")
        )

        cues = _build_caption_cues_from_whisper(whisper_res, spec_text, speaker)
        result["spec_text_used"] = bool(spec_text and cues)
        result["cues"] = cues

        if not cues:
            # Edge: whisper had text but couldn't produce cues (shouldn't happen, but safe)
            result["no_speech_detected"] = True
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                     "-i", str(clip_path), "-c", "copy", "-map", "0",
                     str(output_path)],
                    check=True, capture_output=True, text=True,
                )
                result["success"] = True
                return result
            except Exception as e:
                result["error"] = f"empty-cues passthrough failed: {e}"
                return result

        # Probe video dimensions
        probe_dims = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v",
             "-show_entries", "stream=height,width", "-of", "csv=p=0", str(clip_path)],
            capture_output=True, text=True, check=False,
        )
        video_height, video_width = 1920, 1080
        try:
            tok = probe_dims.stdout.strip().splitlines()[0].split(",")
            # csv order: width,height
            video_width = int(tok[0])
            video_height = int(tok[1])
        except (ValueError, IndexError):
            pass

        # Resolve fonts
        font_narration = style_overrides.get("font_narration") or _resolve_font(DEFAULT_NARRATION_FONT_CANDIDATES)
        font_mono = style_overrides.get("font_mono") or _resolve_font(DEFAULT_MONO_FONT_CANDIDATES)

        # CAPTION-OVERLAP fix: assign per-class Y bands + de-conflict same-Y temporal collisions
        # (cross-layer narrator+dialog and char-vs-char) BEFORE burning.
        cues = deconflict_cue_ys(cues)

        # Build chained drawtext filters (multi-line per cue)
        drawtext_filters: list[str] = []
        for c in cues:
            drawtext_filters.extend(
                _drawtext_filters_for_cue(c, video_height, video_width, font_narration, font_mono)
            )
        vf = ",".join(drawtext_filters)

        # Re-encode video w/ drawtext, copy audio
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(clip_path),
            "-vf", vf,
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            "-map", "0:v:0", "-map", "0:a:0",
            str(output_path),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            result["error"] = f"ffmpeg drawtext burn failed: {e.stderr[-800:] if e.stderr else 'unknown'}"
            return result

        result["captions_burned"] = len(cues)
        result["success"] = True
        return result


# ----------------------------------------------------------------------------
# Main build per-shot
# ----------------------------------------------------------------------------
def build_clip_atomic(
    spec: dict,
    spec_path: Path,
    shot_id: str,
    project_root: Path,
    base_root: Path,
    output_dir: Path,
    sfx_events: list[dict],
    avu_type: str | None = None,
    avu_inject_s: float | None = None,
    quiet: bool = False,
) -> dict:
    """Build a single atomic clip. Returns the manifest dict."""
    shot = find_shot(spec, shot_id)
    if not shot:
        raise ValueError(f"shot_id '{shot_id}' not found in SPEC")

    shot_id = shot["id"]  # normalize to full id (prefix match resolution)
    shot_start, shot_end = parse_timestamp_intent(shot)
    shot_dur = shot_end - shot_start

    if not quiet:
        print(f"\n▶ Building atomic clip: {shot_id}")
        print(f"  Window:     [{shot_start:.2f}s, {shot_end:.2f}s] = {shot_dur:.2f}s")

    # 1. Visual
    visual = find_clip_visual(project_root, shot_id)
    if not visual:
        raise FileNotFoundError(f"Visual clip not found: assets/clips/{shot_id}.mp4")
    if not quiet:
        print(f"  Visual:     {visual.relative_to(base_root)}")

    # 2. Narration segments
    narration_segments = resolve_narration_segments(spec, shot_start, shot_end)
    audio_sources = []
    for seg in narration_segments:
        tts_path = find_tts_segment(project_root, seg["id"])
        if tts_path:
            audio_sources.append({
                "path": tts_path,
                "offset_s": seg["local_start_s"],
                "volume": MIX_NARRATION_DEFAULT,
                "label": f"tts_{seg['id']}",
            })
            if not quiet:
                print(f"  TTS:        +{seg['local_start_s']:.2f}s  {seg['id']}.mp3 @ {MIX_NARRATION_DEFAULT}")
        else:
            if not quiet:
                print(f"  TTS MISSING: {seg['id']}.mp3 — skipping")

    # 3. SFX events in window
    shot_sfx = resolve_sfx_events(sfx_events, shot_start, shot_end)
    for ev in shot_sfx:
        sfx_path_str = ev["path"]
        sfx_asset = find_sfx_asset(project_root, base_root, sfx_path_str)
        if sfx_asset:
            audio_sources.append({
                "path": sfx_asset,
                "offset_s": ev["local_start_s"],
                "volume": ev.get("volume", MIX_SFX_EVENT_DEFAULT),
                "label": f"sfx_{Path(sfx_path_str).stem}",
            })
            if not quiet:
                print(f"  SFX:        +{ev['local_start_s']:.2f}s  {Path(sfx_path_str).name} @ {ev.get('volume', MIX_SFX_EVENT_DEFAULT)}")
        else:
            if not quiet:
                print(f"  SFX MISSING: {sfx_path_str} — skipping")

    # 4. Compose atomic mp4
    atomic_path = output_dir / f"{shot_id}_atomic.mp4"
    compose_atomic_audio_video(visual, audio_sources, shot_dur, atomic_path)

    # 5. Optional AVU overlay (re-encodes with overlay+mix)
    avu_used = None
    if avu_type:
        avu_asset = find_avu_asset(base_root, avu_type)
        if not avu_asset:
            print(f"  WARN: AVU type '{avu_type}' not found in avu-library — skipping overlay", file=sys.stderr)
        else:
            inject_at = avu_inject_s if avu_inject_s is not None else max(0.0, shot_dur - ffprobe_duration(avu_asset))
            tmp_path = output_dir / f"{shot_id}_atomic_pre_avu.mp4"
            atomic_path.rename(tmp_path)
            overlay_avu(tmp_path, avu_asset, inject_at, atomic_path)
            tmp_path.unlink()
            avu_used = avu_type
            if not quiet:
                print(f"  AVU:        +{inject_at:.2f}s  {avu_asset.name}")

    actual_dur = ffprobe_duration(atomic_path)

    # 6. Captions sidecar
    captions = build_caption_sidecar(shot_id, shot_start, shot_end, narration_segments)
    captions_path = output_dir / f"{shot_id}_captions.json"
    with open(captions_path, "w") as f:
        json.dump(captions, f, indent=2, ensure_ascii=False)

    # 7. Manifest with audit
    manifest = build_manifest(
        shot_id=shot_id,
        spec_intent_duration_s=shot_dur,
        actual_duration_s=actual_dur,
        audio_sources=audio_sources,
        narration_segments=narration_segments,
        sfx_events=shot_sfx,
        output_path=atomic_path,
        avu_used=avu_used,
    )
    manifest_path = output_dir / f"{shot_id}_manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    if not quiet:
        status_glyph = "✓" if manifest["audit_status"] == "PASS" else "⚠"
        print(f"  {status_glyph} Atomic:   {atomic_path.relative_to(base_root)}  ({actual_dur:.2f}s, LUFS={manifest['audio']['lufs_integrated']})")

    return manifest


# ----------------------------------------------------------------------------
# SFX event loader — pluggable
# ----------------------------------------------------------------------------
def load_sfx_events_from_pythonfile(py_path: Path) -> list[dict]:
    """
    Load SFX_EVENTS from a Python file (e.g. project's cp5-audio-master.py).
    Expects module-level SFX_EVENTS list of (path, start_s, volume) tuples.
    """
    if not py_path.exists():
        return []
    import importlib.util
    spec = importlib.util.spec_from_file_location("sfx_events_module", py_path)
    if not spec or not spec.loader:
        return []
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"WARN: failed to load SFX events from {py_path}: {e}", file=sys.stderr)
        return []
    raw = getattr(module, "SFX_EVENTS", [])
    out = []
    for entry in raw:
        if isinstance(entry, (list, tuple)) and len(entry) >= 3:
            out.append({"path": entry[0], "start_s": float(entry[1]), "volume": float(entry[2])})
        elif isinstance(entry, dict):
            out.append({
                "path": entry.get("path") or entry.get("out") or "",
                "start_s": float(entry.get("start_s", 0)),
                "volume": float(entry.get("volume", MIX_SFX_EVENT_DEFAULT)),
            })
    return out


def load_sfx_events_from_json(json_path: Path) -> list[dict]:
    """Load SFX events from JSON: [{"path": ..., "start_s": ..., "volume": ...}, ...]"""
    if not json_path.exists():
        return []
    with open(json_path) as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        return []
    out = []
    for entry in raw:
        if isinstance(entry, dict) and "path" in entry and "start_s" in entry:
            out.append({
                "path": entry["path"],
                "start_s": float(entry["start_s"]),
                "volume": float(entry.get("volume", MIX_SFX_EVENT_DEFAULT)),
            })
    return out


# ----------------------------------------------------------------------------
# Caption-bake CLI helper
# ----------------------------------------------------------------------------
def _run_bake_captions_cli(args) -> int:
    """Implements --bake-captions invocation. Returns process exit code."""
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Resolve input clip
    spec_shot: dict[str, Any] = {}
    if args.input_clip:
        input_clip = args.input_clip.resolve()
        if not input_clip.exists():
            print(f"ERROR: --input-clip not found: {input_clip}", file=sys.stderr)
            return 2
        # Optional sidecar
        if args.sidecar and args.sidecar.exists():
            try:
                with open(args.sidecar) as f:
                    sidecar_data = json.load(f)
                # IMPORTANT (adversarial): the sidecar text is only used as a SPEC
                # text override input. The caller is responsible for trust. The
                # function below will still IGNORE this if Whisper finds different
                # actual audio — that's the whole point of the contract: timing
                # ALWAYS comes from Whisper. The text override is a hint, not a truth.
                spec_shot = sidecar_data
            except Exception as e:
                print(f"WARN: failed to read sidecar {args.sidecar}: {e}", file=sys.stderr)
        # Shot id default
        if "id" not in spec_shot:
            spec_shot["id"] = args.shot_id or input_clip.stem
    else:
        # SPEC-driven resolution
        if not args.shot_id:
            print("ERROR: --bake-captions requires --shot-id (or --input-clip).", file=sys.stderr)
            return 2
        spec = load_spec(args.spec.resolve())
        shot = find_shot(spec, args.shot_id)
        if not shot:
            print(f"ERROR: shot_id '{args.shot_id}' not found in SPEC", file=sys.stderr)
            return 2
        spec_shot = dict(shot)
        # Try to inherit narration text_canonical from narration_script if not on shot
        if "text_canonical" not in spec_shot:
            shot_start, shot_end = parse_timestamp_intent(shot)
            segs = resolve_narration_segments(spec, shot_start, shot_end)
            if segs:
                spec_shot["text_canonical"] = segs[0]["text"]
                spec_shot["speaker"] = segs[0]["speaker"]
        project_root = (args.project_root or output_dir.parent).resolve()
        clip = find_clip_visual(project_root, spec_shot["id"])
        if not clip:
            print(f"ERROR: visual clip not found for shot {spec_shot['id']}", file=sys.stderr)
            return 2
        input_clip = clip

    # Output path
    if args.output:
        output_path = args.output.resolve()
    else:
        output_path = output_dir / f"{spec_shot.get('id', 'clip')}_captions_burned.mp4"

    style_overrides = {
        "language": args.bake_language,
        "model_name": args.bake_model,
    }

    if not args.quiet:
        print(f"\n▶ Baking captions: {input_clip.name} → {output_path.name}")
        print(f"  SPEC text override: {'YES' if spec_shot.get('text_canonical') else 'no'}")
        print(f"  Whisper model: {args.bake_model}  language: {args.bake_language}")

    res = bake_captions_per_clip(
        clip_path=input_clip,
        spec_shot=spec_shot,
        output_path=output_path,
        style_overrides=style_overrides,
    )

    if not args.quiet:
        print(f"  Whisper text:       {res['whisper_text'][:100]!r}")
        print(f"  No speech detected: {res['no_speech_detected']}")
        print(f"  SPEC text used:     {res['spec_text_used']}")
        print(f"  Captions burned:    {res['captions_burned']}")
        if res.get("error"):
            print(f"  ERROR:              {res['error']}", file=sys.stderr)

    # Side-output JSON report alongside the mp4
    report_path = output_path.with_suffix(output_path.suffix + ".bake-report.json")
    with open(report_path, "w") as f:
        json.dump({
            "input_clip": str(input_clip),
            "output_path": str(output_path),
            "shot_id": spec_shot.get("id"),
            "spec_text_override": spec_shot.get("text_canonical"),
            "whisper_text": res["whisper_text"],
            "no_speech_detected": res["no_speech_detected"],
            "spec_text_used": res["spec_text_used"],
            "sidecar_rejected": res.get("sidecar_rejected", False),
            "captions_burned": res["captions_burned"],
            "cues": res["cues"],
            "error": res["error"],
            "success": res["success"],
        }, f, indent=2, ensure_ascii=False)
    if not args.quiet:
        print(f"  Report:             {report_path}")

    return 0 if res["success"] else 1


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Build per-clip atomic AVU (visual + audio + captions + manifest).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--spec", type=Path, default=None,
                        help="Path to creative-specs/<id>.yaml (required for atomic-build mode; "
                             "optional for --bake-captions when --input-clip is given).")
    parser.add_argument("--shot-id", type=str,
                        help="Single shot to build (e.g. shot_01_hook). Mutually exclusive with --batch.")
    parser.add_argument("--batch", action="store_true",
                        help="Build all shots in SPEC.")
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="Output directory for atomic clips (e.g. assets/clips-atomic/)")
    parser.add_argument("--project-root", type=Path, default=None,
                        help="Project root (defaults to parent of output-dir).")
    parser.add_argument("--base-root", type=Path, default=Path("<repo-root>"),
                        help="Base repo root (used to resolve library/ + base-relative paths).")
    parser.add_argument("--sfx-events", type=Path, default=None,
                        help="SFX events source: .py file (extract SFX_EVENTS list) OR .json file. "
                             "If omitted, will try <project_root>/scripts/cp5-audio-master.py.")
    parser.add_argument("--avu", type=str, default=None,
                        choices=["countdown", "decision-freeze", "hook-transition", "outro-card", "outro"],
                        help="Optional AVU overlay type (single-shot mode only).")
    parser.add_argument("--avu-inject-s", type=float, default=None,
                        help="Override AVU inject offset (local time). Defaults to end-aligned.")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress per-shot progress output.")
    parser.add_argument("--bake-captions", action="store_true",
                        help="Mode: bake captions per clip from Whisper-derived timing + SPEC text override. "
                             "Takes --shot-id (or --input-clip standalone) and writes burned mp4 to --output. "
                             "When set, the atomic build pipeline is bypassed.")
    parser.add_argument("--input-clip", type=Path, default=None,
                        help="Input mp4 for --bake-captions standalone mode (no SPEC lookup). "
                             "If omitted, the script resolves the clip via SPEC + --shot-id.")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output mp4 path for --bake-captions mode. Defaults to "
                             "<output-dir>/<shot_id>_captions_burned.mp4.")
    parser.add_argument("--sidecar", type=Path, default=None,
                        help="Optional sidecar JSON (used ONLY for explicit text_canonical override "
                             "in standalone --bake-captions runs). Note: per adversarial spec, sidecar "
                             "is IGNORED if SPEC also provides text_canonical for this shot.")
    parser.add_argument("--bake-language", type=str, default="es",
                        help="Whisper language code (default: es).")
    parser.add_argument("--bake-model", type=str, default="base",
                        help="Whisper model name (default: base).")
    args = parser.parse_args()

    # Caption-bake mode short-circuit
    if args.bake_captions:
        return _run_bake_captions_cli(args)

    # Bake-mode bypasses atomic-build arg validation
    if not args.bake_captions:
        if not args.spec:
            parser.error("--spec is required for atomic-build mode")
        if not args.batch and not args.shot_id:
            parser.error("Must specify either --shot-id <id> or --batch")
        if args.batch and args.shot_id:
            parser.error("--batch and --shot-id are mutually exclusive")
        if args.batch and args.avu:
            parser.error("--avu only supported in single-shot mode (batch infers AVU per shot from SPEC)")

    # Resolve roots
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    project_root = (args.project_root or output_dir.parent).resolve()
    base_root = args.base_root.resolve()

    # Load SPEC
    spec = load_spec(args.spec.resolve())

    # Load SFX events
    sfx_events = []
    if args.sfx_events:
        if args.sfx_events.suffix == ".py":
            sfx_events = load_sfx_events_from_pythonfile(args.sfx_events.resolve())
        elif args.sfx_events.suffix == ".json":
            sfx_events = load_sfx_events_from_json(args.sfx_events.resolve())
    else:
        # Try project default
        default_py = project_root / "scripts" / "cp5-audio-master.py"
        if default_py.exists():
            sfx_events = load_sfx_events_from_pythonfile(default_py)
            if not args.quiet and sfx_events:
                print(f"ℹ Loaded {len(sfx_events)} SFX events from {default_py.relative_to(base_root)}")

    # Build
    if args.shot_id:
        manifest = build_clip_atomic(
            spec=spec,
            spec_path=args.spec,
            shot_id=args.shot_id,
            project_root=project_root,
            base_root=base_root,
            output_dir=output_dir,
            sfx_events=sfx_events,
            avu_type=args.avu,
            avu_inject_s=args.avu_inject_s,
            quiet=args.quiet,
        )
        print(f"\n{'✓ PASS' if manifest['audit_status'] == 'PASS' else '⚠ REVIEW'} — {manifest['shot_id']}")
        return 0 if manifest["audit_status"] == "PASS" else 1

    # Batch
    shots = spec.get("shot_list", [])
    if not shots:
        print("ERROR: SPEC has no shot_list", file=sys.stderr)
        return 2

    summaries = []
    failed = []
    for shot in shots:
        sid = shot.get("id")
        try:
            m = build_clip_atomic(
                spec=spec,
                spec_path=args.spec,
                shot_id=sid,
                project_root=project_root,
                base_root=base_root,
                output_dir=output_dir,
                sfx_events=sfx_events,
                avu_type=None,
                avu_inject_s=None,
                quiet=args.quiet,
            )
            summaries.append(m)
            if m["audit_status"] != "PASS":
                failed.append(sid)
        except Exception as e:
            print(f"\n✗ FAILED to build {sid}: {e}", file=sys.stderr)
            failed.append(sid)

    # Batch summary manifest
    batch_path = output_dir / "_batch_manifest.json"
    with open(batch_path, "w") as f:
        json.dump({
            "spec": str(args.spec),
            "total_shots": len(shots),
            "built": len(summaries),
            "passed": sum(1 for s in summaries if s["audit_status"] == "PASS"),
            "review": sum(1 for s in summaries if s["audit_status"] != "PASS"),
            "failed": failed,
            "shots": summaries,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n══════════════════════════════════════════════════════════════")
    print(f"  Batch summary: {len(summaries)}/{len(shots)} built")
    print(f"  PASS: {sum(1 for s in summaries if s['audit_status'] == 'PASS')}")
    print(f"  REVIEW: {sum(1 for s in summaries if s['audit_status'] != 'PASS')}")
    print(f"  FAILED: {len(failed)}")
    print(f"  Manifest: {batch_path.relative_to(base_root)}")
    print(f"══════════════════════════════════════════════════════════════")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
