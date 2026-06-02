#!/usr/bin/env python3
"""audit-render-audio-coverage.py — narration coverage on the RENDERED mp4 (HYBRID-aware).

REPLACES audit-audio.py for the per-clip-atomic HYBRID path (HR#23 + HR#25). audit-audio.py
parses <audio> tags out of index.html; in the HYBRID per-clip-atomic path the narration audio is
MUXED inside each clip + overlaid by ffmpeg POST-concat → there are NO <audio> tags to parse →
audit-audio reports 0% (false FAIL) or, worse, reads a stale legacy index.html (false PASS). Either
way the under-narration class (pueblo-v2: 30.9% narration coverage, narrator "stammers") becomes
INVISIBLE. This validator opens the MP4 itself and measures what is actually audible.

WHAT IT VALIDATES (operates on the rendered MP4, never on HTML):
  - coverage_pct = (seconds of audible narration / total duration) >= min_coverage (default 40%).
  - no narrative dead-zone > 2.0s INSIDE the span where narration should exist (first narrated
    second .. last narrated second) — i.e. the narrator does not vanish mid-video.

GUARD (HYBRID architecture, HR#23/#25): if assembly_strategy == per_clip_atomic (from the batch
manifest or the SPEC) AND an --html is passed → exit 2 'wrong-architecture'. We refuse to read a
legacy index.html for an atomic render (that is exactly the false-PASS audit-audio.py falls into).

Capability-gate (Pattern 7): --format REQUIRED. If has_tts_narration is false → exit 0
'not_applicable' (no narration to cover — not a failure).

Exit codes: 0 = PASS / not_applicable · 1 = FAIL (gate violated) · 2 = can't-measure /
wrong-architecture (missing media, whisper/ffmpeg unavailable, or HTML passed for an atomic render).

Authority: HR#13 (audio coverage técnicos) + HR#23/#25 (HYBRID per-clip-atomic) + HR#30
(coverage = temporal, 1-frame existence insufficient). GAP: audit-audio.py wrong-artefact in HYBRID.
Companion test: test_audit-render-audio-coverage.py (HR#26 — TDD, mocks whisper + silencedetect).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pyyaml only needed when reading a SPEC for capabilities/strategy
    yaml = None

MIN_COVERAGE_DEFAULT = 40.0     # %. pueblo-v2 failed at 30.9%; the 3 success videos sit 70-77%.
MAX_NARRATIVE_GAP_S = 2.0       # s. dead-zone inside the narrated span longer than this → FAIL.


# ---------------------------------------------------------------------------
# PURE LOGIC (no media, no deps) — this is what the test exercises directly.
# ---------------------------------------------------------------------------
def segments_coverage_seconds(transcript_segments: list[dict]) -> float:
    """Union of [start,end) of narrated segments, in seconds (overlap-safe)."""
    spans = []
    for s in transcript_segments or []:
        try:
            a = float(s["start"])
            b = float(s["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if b > a:
            spans.append((a, b))
    if not spans:
        return 0.0
    spans.sort()
    total = 0.0
    cur_a, cur_b = spans[0]
    for a, b in spans[1:]:
        if a <= cur_b:  # overlap / contiguous → extend
            cur_b = max(cur_b, b)
        else:
            total += cur_b - cur_a
            cur_a, cur_b = a, b
    total += cur_b - cur_a
    return total


def narrated_span(transcript_segments: list[dict]) -> tuple[float, float] | None:
    """(first narrated second, last narrated second) across all segments, or None if empty."""
    starts, ends = [], []
    for s in transcript_segments or []:
        try:
            a = float(s["start"]); b = float(s["end"])
        except (KeyError, TypeError, ValueError):
            continue
        if b > a:
            starts.append(a); ends.append(b)
    if not starts:
        return None
    return (min(starts), max(ends))


def narrative_gaps_in_span(silence_zones: list[tuple[float, float]],
                           span: tuple[float, float],
                           max_gap_s: float) -> list[dict]:
    """Silence zones that overlap the narrated span and whose IN-SPAN portion exceeds max_gap_s.

    silence_zones: list of (start, end) seconds from ffmpeg silencedetect.
    span: (span_start, span_end) — only gaps WITHIN this window count as "narrator vanished
    mid-video". Lead-in silence before the first word and trailing silence after the last word are
    NOT narrative gaps (cliffhanger tails, intro stings, etc.)."""
    span_start, span_end = span
    out = []
    for z in silence_zones or []:
        try:
            zs = float(z[0]); ze = float(z[1])
        except (TypeError, ValueError, IndexError):
            continue
        # clip the silence zone to the narrated span
        a = max(zs, span_start)
        b = min(ze, span_end)
        dur = b - a
        if dur > max_gap_s:
            out.append({"start": round(a, 2), "end": round(b, 2), "duration_s": round(dur, 2)})
    return out


def evaluate_audio_coverage(transcript_segments: list[dict],
                            total_dur: float,
                            silence_zones: list[tuple[float, float]],
                            min_coverage: float) -> tuple[bool, list[str]]:
    """PURE decision. Returns (ok, reasons).

    ok = coverage_pct >= min_coverage AND no narrative dead-zone > MAX_NARRATIVE_GAP_S inside the
    narrated span. reasons is a list of human-readable failure strings (empty when ok)."""
    reasons: list[str] = []
    if not total_dur or total_dur <= 0:
        return False, ["INVALID_DURATION: total_dur must be > 0 (could not measure the render)"]

    narrated_s = segments_coverage_seconds(transcript_segments)
    coverage_pct = narrated_s / total_dur * 100.0

    if coverage_pct < min_coverage:
        reasons.append(
            f"LOW_NARRATION_COVERAGE: {coverage_pct:.1f}% audible narration "
            f"(min {min_coverage:.0f}%). pueblo-v2 failed at 30.9%; success videos 70-77%. "
            f"This is the under-narration class audit-audio misses in the HYBRID path."
        )

    span = narrated_span(transcript_segments)
    if span is not None:
        for g in narrative_gaps_in_span(silence_zones, span, MAX_NARRATIVE_GAP_S):
            reasons.append(
                f"NARRATIVE_DEAD_ZONE: {g['duration_s']}s silence between {g['start']}s and "
                f"{g['end']}s — inside narrated span, narrator vanished (max {MAX_NARRATIVE_GAP_S}s)."
            )
    return (len(reasons) == 0), reasons


def resolve_min_coverage_pct(narrated_seconds: float, total_dur: float) -> float:
    """Helper for reporting (kept pure)."""
    if not total_dur or total_dur <= 0:
        return 0.0
    return round(narrated_seconds / total_dur * 100.0, 1)


# ---------------------------------------------------------------------------
# THIN RUNTIME WRAPPERS (media + heavy deps live here; the test mocks these).
# ---------------------------------------------------------------------------
def ffprobe_duration(video_path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def whisper_transcribe_mp4(video_path: str, language: str = "es",
                           model_name: str = "base") -> list[dict]:
    """Transcribe the rendered MP4's audio track. Returns whisper-style segments
    [{'start','end','text'}]. Lazy import so the test never needs whisper installed."""
    import whisper  # lazy
    model = whisper.load_model(model_name)
    result = model.transcribe(
        video_path, language=language, verbose=False, fp16=False,
        condition_on_previous_text=False,
    )
    segs = []
    for s in result.get("segments", []) or []:
        if (s.get("text") or "").strip():
            segs.append({"start": float(s.get("start", 0)),
                         "end": float(s.get("end", 0)),
                         "text": (s.get("text") or "").strip()})
    return segs


def ffmpeg_silence_zones(video_path: str, noise_db: float = -35.0,
                         min_silence_s: float = 0.5) -> list[tuple[float, float]]:
    """Run ffmpeg silencedetect on the MP4. Returns [(start, end)] silence intervals.
    Parses silence_start / silence_end pairs from stderr."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video_path,
         "-af", f"silencedetect=noise={noise_db}dB:d={min_silence_s}",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return parse_silencedetect(out.stderr)


def parse_silencedetect(stderr: str) -> list[tuple[float, float]]:
    """PURE parser for ffmpeg silencedetect stderr → [(start, end)]."""
    starts = [float(m.group(1)) for m in re.finditer(r"silence_start:\s*([0-9.]+)", stderr)]
    ends = [float(m.group(1)) for m in re.finditer(r"silence_end:\s*([0-9.]+)", stderr)]
    zones = []
    for i, s in enumerate(starts):
        e = ends[i] if i < len(ends) else None
        if e is not None and e > s:
            zones.append((s, e))
    return zones


# ---------------------------------------------------------------------------
# Strategy / capability resolution
# ---------------------------------------------------------------------------
def read_assembly_strategy(manifest_path: str | None, spec_path: str | None) -> str | None:
    """Resolve assembly_strategy from batch manifest first, then SPEC. None if undeclared."""
    # 1) batch manifest (engineer-emitted) — may carry the strategy explicitly.
    if manifest_path and Path(manifest_path).exists():
        try:
            data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
            strat = data.get("assembly_strategy")
            if strat:
                return strat
            # atomic_v1 manifests imply per_clip_atomic even if not labelled.
            shots = data.get("shots") or []
            if shots and all(s.get("format_version") == "atomic_v1" for s in shots if isinstance(s, dict)):
                return "per_clip_atomic"
        except (ValueError, OSError):
            pass
    # 2) SPEC (architect-declared, PIPELINE.md §794).
    if spec_path and yaml is not None and Path(spec_path).exists():
        try:
            spec = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8")) or {}
            return spec.get("assembly_strategy")
        except Exception:
            pass
    return None


def read_has_tts(spec_path: str | None) -> bool | None:
    """Read video_capabilities.has_tts_narration from SPEC. None if SPEC/caps absent."""
    if not spec_path or yaml is None or not Path(spec_path).exists():
        return None
    try:
        spec = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    caps = spec.get("video_capabilities")
    if caps is None:
        return None
    return bool(caps.get("has_tts_narration", False))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True, help="delivery/genre format (Pattern 7 gate)")
    parser.add_argument("--video", help="path to the rendered MP4 (the artefact we audit)")
    parser.add_argument("--html", help="legacy index.html — DISALLOWED for per_clip_atomic (guard)")
    parser.add_argument("--spec", help="SPEC yaml (capabilities + assembly_strategy)")
    parser.add_argument("--manifest", help="batch manifest json (_batch_manifest.json)")
    parser.add_argument("--min-coverage", type=float, default=MIN_COVERAGE_DEFAULT,
                        help=f"min audible-narration coverage %% (default {MIN_COVERAGE_DEFAULT})")
    parser.add_argument("--language", default="es", help="whisper language (default es)")
    parser.add_argument("--whisper-model", default="base")
    parser.add_argument("--noise-db", type=float, default=-35.0)
    parser.add_argument("--min-silence-s", type=float, default=0.5)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    strategy = read_assembly_strategy(args.manifest, args.spec)
    has_tts = read_has_tts(args.spec)

    if args.dry_run:
        print(json.dumps({
            "format": args.format, "assembly_strategy": strategy,
            "has_tts_narration": has_tts, "min_coverage": args.min_coverage,
            "branch": "audit" if (has_tts is not False) else "not_applicable",
        }, indent=2, ensure_ascii=False))
        return 0

    # GUARD (HR#23/#25): atomic render + HTML passed → wrong-architecture. Refuse to read legacy HTML.
    if strategy == "per_clip_atomic" and args.html:
        print(json.dumps({
            "format": args.format, "overall_status": "wrong_architecture",
            "assembly_strategy": strategy,
            "detail": ("assembly_strategy=per_clip_atomic but --html was passed. Narration is muxed "
                       "per-clip; there are no <audio> tags. Audit the rendered MP4 (--video), NOT "
                       "the HTML — reading legacy index.html here yields a false PASS (the audit-audio "
                       "bug this validator replaces)."),
        }, indent=2, ensure_ascii=False))
        return 2

    # Capability gate (Pattern 7): explicit has_tts=false → not_applicable.
    if has_tts is False:
        print(json.dumps({
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_tts_narration=false → no narration to cover.",
        }, indent=2, ensure_ascii=False))
        return 0

    if not args.video:
        print("ERROR: --video is required (this validator audits the rendered MP4, not HTML).",
              file=sys.stderr)
        return 2
    if not Path(args.video).exists():
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        return 2

    # Runtime measurement (mocked in tests).
    try:
        total_dur = ffprobe_duration(args.video)
        segments = whisper_transcribe_mp4(args.video, language=args.language,
                                          model_name=args.whisper_model)
        silence_zones = ffmpeg_silence_zones(args.video, noise_db=args.noise_db,
                                             min_silence_s=args.min_silence_s)
    except FileNotFoundError as e:
        print(f"ERROR: required tool not found ({e}). Need ffprobe/ffmpeg + whisper.", file=sys.stderr)
        return 2
    except Exception as e:  # whisper load / decode failure → can't-measure, not a FAIL.
        print(f"ERROR: could not measure render audio: {e}", file=sys.stderr)
        return 2

    ok, reasons = evaluate_audio_coverage(segments, total_dur, silence_zones, args.min_coverage)

    narrated_s = segments_coverage_seconds(segments)
    report = {
        "format": args.format, "video": args.video,
        "assembly_strategy": strategy,
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "total_duration_s": round(total_dur, 2),
        "narrated_seconds": round(narrated_s, 2),
        "coverage_pct": resolve_min_coverage_pct(narrated_s, total_dur),
        "min_coverage": args.min_coverage,
        "max_narrative_gap_s": MAX_NARRATIVE_GAP_S,
        "segments_count": len(segments),
        "silence_zones_count": len(silence_zones),
        "reasons": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


# Alias for in-process testing (mock the runtime wrappers, then call with an explicit argv list).
main_with_argv = main


if __name__ == "__main__":
    sys.exit(main())
