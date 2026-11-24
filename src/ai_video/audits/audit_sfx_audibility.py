#!/usr/bin/env python3
"""
audit-sfx-audibility.py — the gate the relative-volume mix was missing (SFX existence ≠ audible).

A clip-scoped SFX can be "wired" and still be INAUDIBLE in the master if its source is quiet and the
bed (narration -14 LUFS + music) sits on top. Existence/wiring checks pass; the viewer hears nothing.
This auditor measures, PER SFX EVENT, the master RMS energy inside the event window vs the surrounding
local bed (sibling-aware, cleanest sample) and FAILS the event if the delta is below a per-class floor:

  delta_dB = rms(master, event_window) - rms(master, surrounding_clean_bed)

Pass floors (an event must lift the master at least this much over its local bed):
  event / scream / transition / diegetic / ui / flash : >= +2.0 dB
  texture (drips / footsteps / buzz)                   : >= +1.0 dB

PRIMARY vs REINFORCEMENT: the FIRST occurrence of each (shot, sfx_id) is audibility-critical and must
clear its class floor against a clean bed. A REPEAT of the same texture/ui sfx_id inside the same dense
window only reinforces (its bed is already full of the sibling) → only required to stay PRESENT (Δ>=0).
event/scream/diegetic/transition/flash are ALWAYS primary.

Event timeline sources (first found wins, or pass --events-json explicitly):
  1. --events-json <file>  : a flat JSON list of
        [{"t0_s": <abs s>, "sfx_id": "...", "class": "event", "src_dur_s": 0.6}, ...]
     (absolute timeline onsets — no reconciliation needed).
  2. autodetect <project-dir>/assets/clips-atomic/_phase1_progress.json (per-shot `sfx_events` with
     in-clip onsets) → re-anchored to each shot's start on the reconciled timeline (sum of atomic
     clip durations). Shot order from --spec if given, else the manifest order.

Usage:
  audit-sfx-audibility.py --video renders/draft.mp4 [--project-dir .] [--events-json events.json]
                          [--spec ../creative-specs/x.yaml] [--json out.json] [--bed-pad 2.0]
Exit 0 = all primary events PASS; exit 1 = one or more FAIL; exit 2 = no event source found.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800

BED_PAD = 2.0
FLOOR_DB = {
    "event": 2.0,
    "scream": 2.0,
    "transition": 2.0,
    "diegetic": 2.0,
    "ui": 2.0,
    "flash": 2.0,
    "texture": 1.0,
}
REINFORCE_CLS = {"texture", "ui"}
EFFECTIVE_DUR_CAP = 1.2  # measure at most the first 1.2s of an event (the transient is what's heard)


def run(cmd):
    return subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT_S)


def probe_dur(p):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def rms_dbfs(video, t0, t1):
    """Mean RMS (dBFS) of the master audio in [t0, t1]."""
    t0 = max(0.0, t0)
    if t1 <= t0:
        return None
    r = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-ss",
            f"{t0:.3f}",
            "-t",
            f"{(t1 - t0):.3f}",
            "-i",
            str(video),
            "-af",
            "astats=metadata=1:reset=0",
            "-f",
            "null",
            "-",
        ]
    )
    vals = []
    for line in r.stderr.splitlines():
        if "RMS level dB:" in line:
            try:
                vals.append(float(line.split("RMS level dB:")[1].strip().split()[0]))
            except (ValueError, IndexError):
                pass
    if not vals:
        return None
    lin = [10 ** (v / 20.0) for v in vals if not math.isinf(v)]
    if not lin:
        return -120.0
    return 20 * math.log10(sum(lin) / len(lin))


def shot_starts(proj, shots):
    atomic = proj / "assets" / "clips-atomic"
    starts, cum = {}, 0.0
    for sid in shots:
        # support both <shot>_atomic.mp4 (canonical) and <shot>.mp4
        f = atomic / f"{sid}_atomic.mp4"
        starts[sid] = cum
        if f.exists():
            cum += probe_dur(f)
    return starts


def load_events_from_json(path, vdur):
    raw = json.loads(Path(path).read_text())
    events = []
    for e in raw:
        t0 = float(e.get("t0_s", e.get("t0", 0.0)))
        cls = e.get("class", e.get("cls", "texture"))
        dur = min(EFFECTIVE_DUR_CAP, max(0.25, float(e.get("src_dur_s", e.get("src_dur", 0.6)))))
        events.append(
            {
                "shot": e.get("shot", "-"),
                "sfx_id": e.get("sfx_id", "sfx"),
                "cls": cls,
                "t0": round(t0, 3),
                "t1": round(min(vdur, t0 + dur), 3),
            }
        )
    return events


def load_events_from_phase1(proj, spec_path, vdur):
    prog = proj / "assets" / "clips-atomic" / "_phase1_progress.json"
    if not prog.exists():
        return None
    results = json.loads(prog.read_text())
    shots = [r["shot_id"] for r in results]
    if spec_path:
        import yaml

        spec = yaml.safe_load(Path(spec_path).read_text())
        shots = [s.get("shot_id") or s.get("id") for s in spec["shot_list"]]
    starts = shot_starts(proj, shots)
    events, seen = [], set()
    for r in results:
        sid = r["shot_id"]
        base = starts.get(sid)
        if base is None:
            continue
        for ev in r.get("sfx_events", []):
            t0 = base + ev["onset_s"]
            dur = min(EFFECTIVE_DUR_CAP, max(0.25, ev.get("src_dur", 0.6)))
            events.append(
                {
                    "shot": sid,
                    "sfx_id": ev["sfx_id"],
                    "cls": ev.get("cls", "texture"),
                    "t0": round(t0, 3),
                    "t1": round(min(vdur, t0 + dur), 3),
                }
            )
    return events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--events-json", default=None, help="Explicit flat event list (abs timeline onsets)")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--bed-pad", type=float, default=BED_PAD)
    args = ap.parse_args()

    proj = Path(args.project_dir).resolve()
    video = Path(args.video)
    if not video.exists():
        print(f"FAIL: video not found: {video}", file=sys.stderr)
        sys.exit(2)
    vdur = probe_dur(video)

    if args.events_json:
        events = load_events_from_json(args.events_json, vdur)
    else:
        events = load_events_from_phase1(proj, args.spec, vdur)
    if events is None:
        print(
            "FAIL: no event source — pass --events-json or run a phase1 that writes "
            "assets/clips-atomic/_phase1_progress.json with sfx_events.",
            file=sys.stderr,
        )
        sys.exit(2)
    if not events:
        print("AUDIBILITY GATE: PASS (no SFX events to audit)")
        sys.exit(0)

    # mark primary vs reinforcement
    seen = set()
    for e in sorted(events, key=lambda x: x["t0"]):
        key = (e["shot"], e["sfx_id"])
        e["primary"] = key not in seen or e["cls"] not in REINFORCE_CLS
        seen.add(key)

    spans = [(e["t0"], e["t1"]) for e in events]

    def clean_bed(e):
        """Cleanest local bed: several 0.4s windows just before/after the event, DROP any overlapping a
        sibling event, take the QUIETEST surviving sample (the true 'without this sound' floor)."""
        win = 0.4
        cand_ts = []
        for k in range(1, 6):
            cand_ts.append((e["t0"] - k * win - 0.05, e["t0"] - (k - 1) * win - 0.05))
            cand_ts.append((e["t1"] + (k - 1) * win + 0.05, e["t1"] + k * win + 0.05))
        clean = []
        for a, b in cand_ts:
            if a < 0 or b > vdur:
                continue
            contaminated = any(
                not (b <= s or a >= t)
                for (s, t) in spans
                if not (abs(s - e["t0"]) < 1e-6 and abs(t - e["t1"]) < 1e-6)
            )
            if contaminated:
                continue
            v = rms_dbfs(video, a, b)
            if v is not None:
                clean.append(v)
        if clean:
            return min(clean)
        pre = rms_dbfs(video, e["t0"] - args.bed_pad, e["t0"] - 0.05)
        post = rms_dbfs(video, e["t1"] + 0.05, e["t1"] + args.bed_pad)
        beds = [b for b in (pre, post) if b is not None]
        return (20 * math.log10(sum(10 ** (b / 20.0) for b in beds) / len(beds))) if beds else None

    rows, fails = [], []
    for e in events:
        ev_rms = rms_dbfs(video, e["t0"], e["t1"])
        bed_rms = clean_bed(e)
        delta = (ev_rms - bed_rms) if (ev_rms is not None and bed_rms is not None) else None
        floor = FLOOR_DB.get(e["cls"], 2.0) if e["primary"] else 0.0
        ok = delta is not None and delta >= floor - 1e-6
        rows.append(
            {
                **e,
                "ev_rms": round(ev_rms, 2) if ev_rms is not None else None,
                "bed_rms": round(bed_rms, 2) if bed_rms is not None else None,
                "delta_db": round(delta, 2) if delta is not None else None,
                "floor": floor,
                "pass": ok,
            }
        )
        if not ok:
            fails.append(rows[-1])

    print(f"\nSFX AUDIBILITY AUDIT — {video.name}  ({len(events)} events, video {vdur:.1f}s)")
    print(
        f"{'shot':9s} {'sfx_id':26s} {'cls':10s} {'P':1s} {'t0':>7s} {'ev_dB':>7s} {'bed_dB':>7s} {'Δ':>6s} {'flr':>4s}  res"
    )
    for r in sorted(rows, key=lambda x: x["t0"]):
        print(
            f"{r['shot']!s:9s} {str(r['sfx_id'])[:26]:26s} {r['cls']:10s} {'P' if r['primary'] else 'r'} "
            f"{r['t0']:7.2f} {r['ev_rms']!s:>7s} {r['bed_rms']!s:>7s} {r['delta_db']!s:>6s} "
            f"{r['floor']:4.1f}  {'PASS' if r['pass'] else 'FAIL'}"
        )
    nprim = sum(1 for r in rows if r["primary"])
    nprim_pass = sum(1 for r in rows if r["primary"] and r["pass"])
    print(f"\nprimary events: {nprim_pass}/{nprim} clear class floor.")
    npass = sum(1 for r in rows if r["pass"])
    print(f"{npass}/{len(rows)} events audible (Δ >= floor). {len(fails)} FAIL.")
    if args.json:
        Path(args.json).write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    if fails:
        print("FAILING events:", ", ".join(f"{f['shot']}/{f['sfx_id']}(Δ{f['delta_db']})" for f in fails))
        sys.exit(1)
    print("AUDIBILITY GATE: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
