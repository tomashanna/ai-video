#!/usr/bin/env python3
"""audit-caption-temporal-coverage.py — HR#30 caption temporal-coverage net (post V5/V6).

Final-render safety net for the V5/V6 caption bug: the caption was burned as ONE
static cue that ffmpeg's wrap truncated to the first line, so only the 1st sentence
showed while the rest of the narration was spoken with no caption. build_clip_atomic
now chunks captions word-timed PER CLIP, but THIS validator is the net at the
final render — it re-derives the spoken span from the render and checks that the
caption cues actually SPAN it temporally (not just exist).

HR#30 = caption coverage in 3 levels:
  (A) existence  — a caption exists (1 frame proves this; INSUFFICIENT alone).
  (B) semantic   — caption text matches the narration (out of scope here; see
                   audit-frames / continuity-check).
  (C) TEMPORAL   — caption cues cover the WHOLE spoken span, chunked, ≤2 lines each.
                   ← THIS validator owns (C).

FAIL (exit 1) if ANY of:
  - covered span < COVERAGE_MIN (default 0.90) of the spoken span, OR
  - a single cue spans > MAX_CUE_SPAN_S (default 3.5s)  → collapsed-block detector
    (this is literally the V5/V6 bug: one 6s cue carrying the whole narration), OR
  - a cue has > MAX_CUE_LINES (default 2) lines.

Runtime sources:
  - spoken span: Whisper word-timestamps over the render audio (first word start →
    last word end). THIN wrapper; pure logic gets the number.
  - caption cues: the per-clip caption sidecar(s) (build_clip_atomic
    build_caption_sidecar) and/or the build_manifest dir, OR OCR-sampling the render
    when no sidecar exists (--ocr). Pure logic gets [{start_s,end_s,text}].

DESIGN (testable): all decision logic lives in pure functions that receive
ALREADY-EXTRACTED data (cues, spoken_span_s, total_dur). The runtime wrapper does
ffprobe/whisper/sidecar-read/OCR and hands the numbers to the pure layer, so the
companion test needs NO real media and NO heavy deps.

Capability-gate (Pattern 7): --format REQUIRED; has_captions_baked false →
exit 0 verdict 'not_applicable'.

Exit codes: 0 = PASS / not_applicable · 1 = FAIL (coverage gate violated)
            · 2 = can't-measure / wrong-architecture (no audio, no cues, no whisper).

Authority: HR#30 + AUDITOR-PROTOCOL §6 (instance 6 user_perceptual_detects_what_
validators_miss) + build_clip_atomic build_caption_sidecar/build_manifest.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Tunable thresholds (HR#30 defaults)
# ---------------------------------------------------------------------------
COVERAGE_MIN_DEFAULT = 0.90    # captioned span must cover ≥90% of spoken span
MAX_CUE_SPAN_S_DEFAULT = 3.5   # any cue longer than this = collapsed-block (V5/V6 bug)
MAX_CUE_LINES_DEFAULT = 2      # ≤2 lines per cue (reel safe zone)
# small float epsilon so "exactly at threshold" doesn't false-fail on rounding
_EPS = 1e-6


# ===========================================================================
# PURE LOGIC (no IO — fully unit-testable with synthetic data)
# ===========================================================================
def _cue_line_count(text: str) -> int:
    """Lines in a cue = explicit newlines (\\n or literal '\\n') count. A cue with no
    newline = 1 line. Empty/whitespace = 0 lines (still 'exists' for span purposes)."""
    if text is None:
        return 0
    norm = text.replace("\\n", "\n")
    stripped = norm.strip()
    if not stripped:
        return 0
    # number of non-empty visual lines
    return sum(1 for ln in stripped.split("\n") if ln.strip()) or 1


def merge_intervals(intervals: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Merge overlapping/touching [start,end] intervals. Pure helper for coverage."""
    clean = []
    for a, b in intervals:
        try:
            a = float(a); b = float(b)
        except (TypeError, ValueError):
            continue
        if b < a:
            a, b = b, a
        if b - a <= 0:
            continue
        clean.append((a, b))
    if not clean:
        return []
    clean.sort()
    merged = [clean[0]]
    for a, b in clean[1:]:
        la, lb = merged[-1]
        if a <= lb + _EPS:               # overlap or touch → extend
            merged[-1] = (la, max(lb, b))
        else:
            merged.append((a, b))
    return merged


def covered_within_span(
    cues: list[dict], span_start: float, span_end: float
) -> float:
    """Total seconds of [span_start, span_end] covered by cue intervals (clipped to
    the spoken span — caption time before/after spoken audio doesn't count)."""
    span_start = float(span_start); span_end = float(span_end)
    if span_end - span_start <= 0:
        return 0.0
    clipped = []
    for c in cues:
        try:
            s = max(float(c["start_s"]), span_start)
            e = min(float(c["end_s"]), span_end)
        except (TypeError, ValueError, KeyError):
            continue
        if e - s > 0:
            clipped.append((s, e))
    return sum(b - a for a, b in merge_intervals(clipped))


def evaluate_caption_temporal(
    caption_cues: list[dict],
    spoken_span_s: tuple[float, float] | list | None,
    total_dur: float,
    coverage_min: float = COVERAGE_MIN_DEFAULT,
    max_cue_span_s: float = MAX_CUE_SPAN_S_DEFAULT,
    max_cue_lines: int = MAX_CUE_LINES_DEFAULT,
) -> tuple[bool, list[str]]:
    """PURE decision core for HR#30 temporal coverage.

    Args:
      caption_cues:  [{start_s, end_s, text}] (text optional; used for line count).
      spoken_span_s: (first_word_start_s, last_word_end_s) of narration in the render.
                     None / empty / zero-length → no speech → not this validator's
                     job to fail (returns ok=True with an info reason).
      total_dur:     render duration (seconds) — used to clamp the spoken span.

    Returns (ok, reasons). reasons always lists every issue found (multi-fail
    visibility) PLUS the computed coverage ratio as the first entry.
    """
    reasons: list[str] = []

    # --- normalize spoken span ---
    if not spoken_span_s or len(spoken_span_s) < 2:
        return True, ["no spoken span detected (silent / music-only clip) → coverage check N/A"]
    sp_start, sp_end = float(spoken_span_s[0]), float(spoken_span_s[1])
    if total_dur and total_dur > 0:
        sp_end = min(sp_end, float(total_dur))
        sp_start = max(0.0, sp_start)
    spoken_len = sp_end - sp_start
    if spoken_len <= 0:
        return True, ["spoken span is zero-length after clamping → coverage check N/A"]

    cues = caption_cues or []
    if not cues:
        reasons.append(
            f"coverage=0.00 — NO caption cues at all over a {spoken_len:.1f}s spoken span "
            f"(existence FAIL, the strongest form of the V5/V6 bug)")
        return False, reasons

    # --- (C1) temporal coverage ratio over the spoken span ---
    covered = covered_within_span(cues, sp_start, sp_end)
    ratio = covered / spoken_len if spoken_len > 0 else 0.0
    reasons.append(f"coverage={ratio:.2f} ({covered:.2f}s / {spoken_len:.2f}s spoken)")

    ok = True
    if ratio < coverage_min - _EPS:
        ok = False
        reasons.append(
            f"FAIL coverage {ratio:.2f} < min {coverage_min:.2f} — captions do NOT span "
            f"the whole narration (V5/V6: only the 1st sentence shows)")

    # --- (C2) collapsed-block detector: any single cue spanning too long ---
    for c in cues:
        try:
            dur = float(c["end_s"]) - float(c["start_s"])
        except (TypeError, ValueError, KeyError):
            continue
        if dur > max_cue_span_s + _EPS:
            ok = False
            cid = c.get("id", c.get("text", "?"))
            reasons.append(
                f"FAIL cue '{_short(cid)}' spans {dur:.1f}s > {max_cue_span_s:.1f}s — "
                f"collapsed static block (the exact V5/V6 burn bug: one cue carries "
                f"the whole narration and wrap truncates it to line 1)")

    # --- (C3) line count per cue (reel safe zone) ---
    for c in cues:
        lines = _cue_line_count(c.get("text", ""))
        if lines > max_cue_lines:
            ok = False
            cid = c.get("id", c.get("text", "?"))
            reasons.append(
                f"FAIL cue '{_short(cid)}' has {lines} lines > {max_cue_lines} "
                f"(overflows the reel caption safe zone)")

    return ok, reasons


def _short(v) -> str:
    s = str(v)
    return s if len(s) <= 32 else s[:29] + "..."


# ===========================================================================
# THIN RUNTIME WRAPPER (IO: ffprobe / whisper / sidecar-read / OCR)
# ===========================================================================
def ffprobe_duration(video_path: Path) -> float | None:
    """Render duration in seconds via ffprobe. None if it can't be read."""
    import subprocess
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
            capture_output=True, text=True, timeout=60)
        v = out.stdout.strip()
        return float(v) if v else None
    except Exception:
        return None


def whisper_spoken_span(video_path: Path, language: str = "es",
                        model_name: str = "base") -> tuple[float, float] | None:
    """Return (first_word_start_s, last_word_end_s) of narration in the render via
    Whisper word-timestamps. None if no speech / whisper unavailable. THIN — the
    pure layer does all the deciding."""
    try:
        import whisper  # lazy
    except ImportError:
        return None
    try:
        model = whisper.load_model(model_name)
        res = model.transcribe(str(video_path), language=language,
                               word_timestamps=True, verbose=False, fp16=False,
                               condition_on_previous_text=False)
    except Exception:
        return None
    starts, ends = [], []
    for seg in res.get("segments", []) or []:
        for w in seg.get("words", []) or []:
            if (w.get("word") or "").strip():
                starts.append(float(w.get("start", 0)))
                ends.append(float(w.get("end", 0)))
    if not starts:
        return None
    return (min(starts), max(ends))


def load_cues_from_sidecars(sidecar_paths: list[Path]) -> list[dict]:
    """Read caption cues from one or more build_clip_atomic sidecar JSON files
    (build_caption_sidecar schema: {captions:[{global_start_s,global_end_s,text,id}]}).
    Returns global-timeline [{start_s,end_s,text,id}] sorted by start. Per-clip
    sidecars use RELATIVE local timing + a global_window_s offset for the absolute
    timeline; we read the global_* fields which are already absolute."""
    cues: list[dict] = []
    for p in sidecar_paths:
        try:
            data = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"WARN: failed to read sidecar {p}: {e}", file=sys.stderr)
            continue
        for cap in data.get("captions", []) or []:
            gs = cap.get("global_start_s", cap.get("local_start_s", cap.get("start_s")))
            ge = cap.get("global_end_s", cap.get("local_end_s", cap.get("end_s")))
            if gs is None or ge is None:
                continue
            cues.append({
                "start_s": float(gs), "end_s": float(ge),
                "text": cap.get("text", ""), "id": cap.get("id", cap.get("speaker", "?")),
            })
    cues.sort(key=lambda c: c["start_s"])
    return cues


def discover_sidecars(project_dir: Path) -> list[Path]:
    """Find per-clip caption sidecars produced by build_clip_atomic
    (<shot_id>_captions.json) anywhere under the project dir."""
    return sorted(project_dir.rglob("*_captions.json"))


def ocr_sample_cues(video_path: Path, interval_s: float = 0.5) -> list[dict] | None:
    """Fallback when there's no sidecar: OCR-sample the render to reconstruct rough
    caption cues. Heavy/optional — returns None if pytesseract/ffmpeg unavailable so
    the caller degrades to exit 2 (can't-measure) rather than a false PASS."""
    try:
        import tempfile

        import pytesseract
        from PIL import Image
    except Exception:
        return None
    # NOTE: implemented as a thin sampler; sampling logic intentionally minimal so
    # the pure evaluator remains the single source of truth. Returns [] if no text
    # frames were found (caller treats [] as a measurable empty-cue FAIL).
    dur = ffprobe_duration(video_path) or 0.0
    if dur <= 0:
        return None
    cues: list[dict] = []
    t = 0.0
    tmp = Path(tempfile.mkdtemp())
    try:
        import subprocess as sp

        import pytesseract
        from PIL import Image
        last_text, run_start = None, None
        while t < dur:
            frame = tmp / f"f_{int(t*1000)}.png"
            sp.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video_path),
                    "-frames:v", "1", "-y", str(frame)], capture_output=True, timeout=60)
            txt = ""
            if frame.exists():
                try:
                    txt = " ".join(pytesseract.image_to_string(Image.open(frame)).split())
                except Exception:
                    txt = ""
            present = bool(txt)
            if present and run_start is None:
                run_start, last_text = t, txt
            elif not present and run_start is not None:
                cues.append({"start_s": run_start, "end_s": t, "text": last_text or "", "id": "ocr"})
                run_start, last_text = None, None
            t += interval_s
        if run_start is not None:
            cues.append({"start_s": run_start, "end_s": dur, "text": last_text or "", "id": "ocr"})
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    return cues


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True, help="delivery/genre format (Pattern 7 gate)")
    parser.add_argument("--video", help="final render mp4 (spoken-span source + OCR fallback)")
    parser.add_argument("--project-dir", help="dir to auto-discover *_captions.json sidecars")
    parser.add_argument("--sidecar", action="append", default=[],
                        help="explicit caption sidecar JSON (repeatable)")
    parser.add_argument("--has-captions-baked", choices=["true", "false"], default="true",
                        help="capability flag (Pattern 7); false → not_applicable")
    parser.add_argument("--coverage-min", type=float, default=COVERAGE_MIN_DEFAULT)
    parser.add_argument("--max-cue-span-s", type=float, default=MAX_CUE_SPAN_S_DEFAULT)
    parser.add_argument("--max-cue-lines", type=int, default=MAX_CUE_LINES_DEFAULT)
    parser.add_argument("--ocr", action="store_true",
                        help="if no sidecar, OCR-sample the render to reconstruct cues")
    parser.add_argument("--lang", default="es")
    parser.add_argument("--whisper-model", default="base")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # ---- Pattern 7 capability gate ----
    if args.has_captions_baked == "false":
        report = {
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_captions_baked=false → no burned captions to span-check (HR#30 N/A)",
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    if args.dry_run:
        print(json.dumps({
            "format": args.format, "branch": "temporal_coverage_check",
            "coverage_min": args.coverage_min, "max_cue_span_s": args.max_cue_span_s,
            "max_cue_lines": args.max_cue_lines,
            "video": args.video, "project_dir": args.project_dir,
            "explicit_sidecars": args.sidecar, "ocr_fallback": args.ocr,
        }, indent=2, ensure_ascii=False))
        return 0

    if not args.video:
        print("ERROR: --video required (spoken-span source) unless --has-captions-baked false",
              file=sys.stderr)
        return 2
    video = Path(args.video)
    if not video.exists():
        print(f"ERROR: video not found: {video}", file=sys.stderr)
        return 2

    # ---- gather caption cues (sidecar → OCR fallback) ----
    sidecars = [Path(s) for s in args.sidecar]
    if not sidecars and args.project_dir:
        sidecars = discover_sidecars(Path(args.project_dir))
    cues: list[dict] | None
    cue_source: str
    if sidecars:
        cues = load_cues_from_sidecars(sidecars)
        cue_source = f"sidecar ({len(sidecars)} file(s))"
    elif args.ocr:
        cues = ocr_sample_cues(video)
        cue_source = "ocr-sampling"
        if cues is None:
            print("ERROR: --ocr requested but pytesseract/PIL/ffmpeg unavailable → can't measure cues",
                  file=sys.stderr)
            return 2
    else:
        print("ERROR: no caption sidecar found and --ocr not given → can't read cues. "
              "Pass --sidecar / --project-dir, or --ocr to reconstruct from the render.",
              file=sys.stderr)
        return 2

    # ---- spoken span (Whisper) ----
    span = whisper_spoken_span(video, language=args.lang, model_name=args.whisper_model)
    if span is None:
        print("ERROR: could not derive spoken span (whisper unavailable or no speech in render) "
              "→ can't measure temporal coverage", file=sys.stderr)
        return 2

    total_dur = ffprobe_duration(video) or (span[1] if span else 0.0)

    # ---- pure evaluation ----
    ok, reasons = evaluate_caption_temporal(
        cues, span, total_dur,
        coverage_min=args.coverage_min, max_cue_span_s=args.max_cue_span_s,
        max_cue_lines=args.max_cue_lines)

    report = {
        "format": args.format, "video": str(video),
        "overall_status": "pass" if ok else "fail", "overall_pass": ok,
        "cue_source": cue_source, "cue_count": len(cues),
        "spoken_span_s": [round(span[0], 3), round(span[1], 3)],
        "total_dur_s": round(total_dur, 3) if total_dur else None,
        "coverage_min": args.coverage_min, "max_cue_span_s": args.max_cue_span_s,
        "max_cue_lines": args.max_cue_lines,
        "reasons": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
