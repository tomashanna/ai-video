#!/usr/bin/env python3
"""audit-spec-voice-exclusivity.py — VOICE EXCLUSIVITY LAW (Capa A, agnóstica).

LEY (universal, todo formato con narración hablada):
  En cualquier instante t, como MÁXIMO UNA voz hablada (narrador O un personaje) puede sonar.
  Entre dos ventanas de voz consecutivas el buffer mínimo es 0.30s (FLOOR técnico, NO una pausa
  dramática — solo garantiza que no se pisen ni queden pegadas al milisegundo). Música / SFX /
  ambient conviven libremente con la voz; esta ley solo gobierna VOCES HABLADAS.

Disparador: V7 ultimo-tren-carga v2 — el `narrator_hook` (12 palabras @165WPM ≈ 4.36s desde 1.8s →
  termina 6.16s) y `tobias_hook_lure` (arranca 3.2s) se SOLAPABAN. Dos voces simultáneas = artefacto
  uncanny + AI-detect signal. Esta ley lo caza en el SPEC (L1) y en el TTS real (L2).

MODOS
  --mode spec  --format <f> --spec <yaml>
       Parsea §9 narration_script COMPLETO (TODOS los speakers: narrator + char_a + char_b + …).
       ventana[i] = [start, start + dur_estimada] donde
         start          = timestamp_intent_s[0]
         dur_estimada   = palabras(text_canonical) / pace_wpm(speaker) * 60
         pace_wpm       = MODEL-CAPABILITIES-MATRIX canonical_pace_wpm (fallback 165) per speaker;
                          la matriz hoy declara un único pace de TTS canónico → todos los speakers
                          lo usan salvo override per-speaker futuro en la matriz.
       FAIL (exit 1) si dos ventanas se INTERSECTAN, o si el gap entre el fin de una y el inicio de
       la siguiente es < 0.30s (buffer mínimo). JSON report con los pares en conflicto.

  --mode tts  --manifest <json>
       Ídem pero con DURACIONES REALES del manifest CP2 (cada entry: segment_id / speaker /
       duration_s / shot_id_anchor). El start REAL de cada voz NO está en el manifest (depende del
       layout de assembly), así que se reconstruye igual que en el assembly: cada voz arranca en el
       START de su shot ancla (+ lead opcional) sobre el timeline reconciliado de los atomics, si se
       pasa --atomic-dir; si no, se cae al timestamp_intent_s del SPEC (--spec) como start. La
       duración SIEMPRE es la real del manifest. Reporta los mismos pares en conflicto.

Capability-aware: has_tts_narration=false → not_applicable (exit 0).
Agnostic-by-design: --format REQUERIDO en --mode spec.

Exit: 0 = PASS / not_applicable · 1 = FAIL (solape o buffer<floor) · 2 = error de invocación/IO.

Companion test: test_audit-spec-voice-exclusivity.py (HR#26). Forward L4: audit-render-voice-overlap.py.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

CANONICAL_PACE_WPM_DEFAULT = 165.0   # MATRIX elevenlabs.canonical_pace_wpm (F1 median)
BUFFER_FLOOR_S = 0.30                # minimum dead air between two spoken-voice windows


def load_canonical_pace(matrix_path):
    """Read canonical_pace_wpm from MODEL-CAPABILITIES-MATRIX.md (line-scan, comment-stripped).
    HR#28/29: roles CONSULT the matrix, no hardcoded pace. Fallback to 165 if unreadable."""
    wpm = CANONICAL_PACE_WPM_DEFAULT
    try:
        for raw in Path(matrix_path).read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0]
            m = re.search(r"canonical_pace_wpm:\s*([0-9.]+)", line)
            if m:
                wpm = float(m.group(1))
    except Exception:
        pass
    return wpm


def speaker_pace(speaker, default_wpm, per_speaker):
    """Per-speaker pace override (forward — the matrix declares one canonical TTS pace today)."""
    return float(per_speaker.get(speaker, default_wpm))


def _est_dur(text, wpm):
    words = len((text or "").split())
    if words == 0 or wpm <= 0:
        return 0.0
    return words / wpm * 60.0


def windows_from_spec(spec, default_wpm, per_speaker):
    """Build spoken-voice windows from §9 narration_script (ALL speakers).
    window = {seg, speaker, start, end (start+est_dur), words, source='estimated'}."""
    out = []
    for n in spec.get("narration_script", []) or []:
        ts = n.get("timestamp_intent_s")
        if not ts or not isinstance(ts, (list, tuple)) or len(ts) < 1:
            continue
        text = n.get("text_canonical") or n.get("narrator_text") or n.get("text") or ""
        speaker = n.get("speaker", "narrator")
        wpm = speaker_pace(speaker, default_wpm, per_speaker)
        start = float(ts[0])
        dur = _est_dur(text, wpm)
        out.append({
            "segment_id": n.get("segment_id", "?"), "speaker": speaker,
            "start": round(start, 3), "end": round(start + dur, 3),
            "words": len((text or "").split()), "wpm": wpm, "source": "estimated_at_canonical_pace",
        })
    return out


# assembly placement leads (mirror cp5b_run_all.py): narrator lands at shot_start + 0.10,
# character dialog at shot_start + DIALOG_LEADIN so the viewer registers the scene first.
NARRATOR_LEAD_S = 0.10
DIALOG_LEAD_S = 0.45


def windows_from_tts(manifest, starts, spec_starts, exclude_segments=None):
    """Build windows from CP2 manifest REAL durations.
    start  = reconciled atomic start (starts[shot]) + per-speaker assembly lead, if --atomic-dir
             given; else SPEC timestamp_intent_s[0]. end = start + real duration_s.
    exclude_segments: segment_ids NOT actually placed in the render (e.g. a manifest entry that a
             fix-pack removed from assembly — voice present as DATA but muted in the cut)."""
    exclude = set(exclude_segments or [])
    out = []
    for seg in manifest:
        sid = seg.get("shot_id_anchor")
        seg_id = seg.get("segment_id", "?")
        if seg_id in exclude:
            continue
        dur = float(seg.get("duration_s", 0.0) or 0.0)
        if dur <= 0:
            continue
        speaker = seg.get("speaker", "narrator")
        lead = NARRATOR_LEAD_S if speaker == "narrator" else DIALOG_LEAD_S
        if starts and sid in starts:
            start = float(starts[sid]) + lead
        elif seg_id in spec_starts:
            start = float(spec_starts[seg_id])
        elif sid in spec_starts:        # shot-level fallback
            start = float(spec_starts[sid])
        else:
            continue
        out.append({
            "segment_id": seg_id, "speaker": speaker,
            "shot_id_anchor": sid, "start": round(start, 3), "end": round(start + dur, 3),
            "duration_s": round(dur, 3), "source": "manifest_real_duration",
        })
    return out


def find_conflicts(windows):
    """Return list of conflicting pairs. A pair (a,b) with a before b conflicts when:
      - OVERLAP: b.start < a.end — two spoken windows sound at the same instant. ALWAYS a violation
        (the core law: máx UNA voz hablada en cualquier t), regardless of who speaks.
      - BUFFER under floor: the gap (b.start - a.end) is positive but < BUFFER_FLOOR_S, AND a/b are
        DIFFERENT speakers — i.e. a real voice HANDOFF (narrator↔character). The 0.3s floor is the
        technical hand-off buffer so two distinct voices never abut to the millisecond. Consecutive
        SAME-speaker segments (continuous narration cut across shots) legitimately abut → not a
        buffer violation (it is one voice, not two competing voices).
    Sorted by start so each window is compared against the previous spoken windows."""
    ws = sorted(windows, key=lambda w: (w["start"], w["end"]))
    conflicts = []
    for i in range(len(ws)):
        a = ws[i]
        for j in range(i + 1, len(ws)):
            b = ws[j]
            # b starts at/after a.end + floor → no possible conflict with a; and since ws is
            # start-sorted every later window starts even later → stop scanning a against the rest.
            if b["start"] >= a["end"] + BUFFER_FLOOR_S:
                break
            overlap = b["start"] < a["end"] - 1e-6
            gap = b["start"] - a["end"]
            diff_speaker = a["speaker"] != b["speaker"]
            if overlap:
                conflicts.append({
                    "kind": "overlap", "a": a["segment_id"], "b": b["segment_id"],
                    "a_speaker": a["speaker"], "b_speaker": b["speaker"],
                    "a_window": [a["start"], a["end"]], "b_window": [b["start"], b["end"]],
                    "overlap_s": round(a["end"] - b["start"], 3),
                    "detail": f"{a['speaker']}:{a['segment_id']} [{a['start']}-{a['end']}] overlaps "
                              f"{b['speaker']}:{b['segment_id']} [{b['start']}-{b['end']}] by "
                              f"{round(a['end'] - b['start'], 3)}s",
                })
            elif diff_speaker and 0 <= gap < BUFFER_FLOOR_S - 1e-6:
                conflicts.append({
                    "kind": "buffer_under_floor", "a": a["segment_id"], "b": b["segment_id"],
                    "a_speaker": a["speaker"], "b_speaker": b["speaker"],
                    "a_window": [a["start"], a["end"]], "b_window": [b["start"], b["end"]],
                    "gap_s": round(gap, 3), "floor_s": BUFFER_FLOOR_S,
                    "detail": f"gap {round(gap, 3)}s between {a['segment_id']} and {b['segment_id']} "
                              f"< floor {BUFFER_FLOOR_S}s",
                })
    return conflicts


def atomic_starts(atomic_dir, shot_ids):
    """Reconstruct each shot's start on the assembled timeline (cumulative atomic durations)."""
    import subprocess
    if not atomic_dir:
        return {}
    starts, cum = {}, 0.0
    for sid in shot_ids:
        p = Path(atomic_dir) / f"{sid}_atomic.mp4"
        starts[sid] = cum
        if p.exists():
            r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", str(p)], capture_output=True, text=True)
            try:
                cum += float(r.stdout.strip())
            except ValueError:
                pass
    return starts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True, choices=["spec", "tts"])
    ap.add_argument("--format", default=None, help="REQUIRED in --mode spec (agnostic-by-design)")
    ap.add_argument("--spec", default=None, help="SPEC yaml (required in spec mode; optional start-source in tts mode)")
    ap.add_argument("--manifest", default=None, help="CP2 manifest json (required in tts mode)")
    ap.add_argument("--atomic-dir", default=None, help="assets/clips-atomic dir → reconciled starts (tts mode)")
    ap.add_argument("--exclude-segments", default=None,
                    help="comma-list of segment_ids present in the manifest as DATA but NOT placed in the cut (tts mode)")
    ap.add_argument("--matrix", default=None, help="path to MODEL-CAPABILITIES-MATRIX.md")
    ap.add_argument("--buffer-floor", type=float, default=None, help="override min buffer s (default 0.30)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    global BUFFER_FLOOR_S
    if args.buffer_floor is not None:
        BUFFER_FLOOR_S = float(args.buffer_floor)

    matrix_path = args.matrix or (Path(__file__).resolve().parent.parent.parent / "MODEL-CAPABILITIES-MATRIX.md")
    default_wpm = load_canonical_pace(matrix_path)
    per_speaker = {}  # forward: matrix per-speaker pace overrides

    # ── spec mode ────────────────────────────────────────────────────────────
    if args.mode == "spec":
        if not args.format:
            print("ERROR: --format is REQUIRED in --mode spec (agnostic-by-design)", file=sys.stderr)
            return 2
        if not args.spec:
            print("ERROR: --spec is REQUIRED in --mode spec", file=sys.stderr)
            return 2
        sp = Path(args.spec)
        if not sp.exists():
            print(f"ERROR: SPEC not found: {sp}", file=sys.stderr)
            return 2
        spec = yaml.safe_load(sp.read_text())
        caps = spec.get("video_capabilities")
        if caps is None:
            print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
                  file=sys.stderr)
            return 2
        if not bool(caps.get("has_tts_narration", False)):
            print(json.dumps({"mode": "spec", "format": args.format, "overall_status": "not_applicable",
                              "detail": "has_tts_narration=false → no spoken voices to check"},
                             indent=2, ensure_ascii=False))
            return 0
        if args.dry_run:
            print(f"mode: spec\nformat: {args.format}\nspec: {sp}\ncanonical_pace_wpm: {default_wpm}\n"
                  f"buffer_floor_s: {BUFFER_FLOOR_S}")
            return 0
        windows = windows_from_spec(spec, default_wpm, per_speaker)
        conflicts = find_conflicts(windows)
        report = {
            "mode": "spec", "format": args.format, "spec": str(sp),
            "canonical_pace_wpm": default_wpm, "buffer_floor_s": BUFFER_FLOOR_S,
            "overall_status": "fail" if conflicts else "pass", "overall_pass": not conflicts,
            "windows_checked": len(windows), "conflict_count": len(conflicts),
            "conflicts": conflicts, "windows": windows,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if conflicts else 0

    # ── tts mode ─────────────────────────────────────────────────────────────
    if not args.manifest:
        print("ERROR: --manifest is REQUIRED in --mode tts", file=sys.stderr)
        return 2
    mf = Path(args.manifest)
    if not mf.exists():
        print(f"ERROR: manifest not found: {mf}", file=sys.stderr)
        return 2
    manifest = json.loads(mf.read_text())

    spec_starts, shot_ids = {}, []
    if args.spec and Path(args.spec).exists():
        spec = yaml.safe_load(Path(args.spec).read_text())
        for n in spec.get("narration_script", []) or []:
            ts = n.get("timestamp_intent_s")
            if ts and isinstance(ts, (list, tuple)):
                if n.get("segment_id"):
                    spec_starts[n["segment_id"]] = float(ts[0])
                if n.get("shot_id_anchor"):
                    spec_starts.setdefault(n["shot_id_anchor"], float(ts[0]))
        shot_ids = [s.get("shot_id") for s in spec.get("shot_list", []) or [] if s.get("shot_id")]

    starts = atomic_starts(args.atomic_dir, shot_ids) if args.atomic_dir else {}
    if args.dry_run:
        print(f"mode: tts\nmanifest: {mf}\natomic_dir: {args.atomic_dir}\n"
              f"start_source: {'reconciled_atomic' if starts else 'spec_timestamp_intent'}\n"
              f"buffer_floor_s: {BUFFER_FLOOR_S}")
        return 0
    exclude = set(args.exclude_segments.split(",")) if args.exclude_segments else None
    windows = windows_from_tts(manifest, starts, spec_starts, exclude_segments=exclude)
    if not windows:
        print(json.dumps({"mode": "tts", "overall_status": "not_applicable",
                          "detail": "no resolvable voice windows (no start source: pass --atomic-dir or --spec)"},
                         indent=2, ensure_ascii=False))
        return 0
    conflicts = find_conflicts(windows)
    report = {
        "mode": "tts", "manifest": str(mf), "atomic_dir": args.atomic_dir,
        "start_source": "reconciled_atomic" if starts else "spec_timestamp_intent",
        "excluded_segments": sorted(exclude) if exclude else [],
        "buffer_floor_s": BUFFER_FLOOR_S,
        "overall_status": "fail" if conflicts else "pass", "overall_pass": not conflicts,
        "windows_checked": len(windows), "conflict_count": len(conflicts),
        "conflicts": conflicts, "windows": windows,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
