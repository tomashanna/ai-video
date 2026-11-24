#!/usr/bin/env python3
"""
audit-audio.py — Audio QA del render. Versión 2 (2026-05-13 PM).

Reescrito desde cero después de validar contra videos exitosos (mina v15 9.9,
bosque v10-berni 10/10, elige V7 9.5) y video fallido (pueblo v2).

CAMBIOS vs v1 (todos los umbrales recalibrados con datos reales):
- v1 categorizaba por track-index (40-49 narración, etc.) → BUG: bosque v10 usa
  tracks 28-31 para narración. Re-categorizado por src name.
- v1 vara música ≥85% → ELIMINADA: bosque v10 tiene 100%, pueblo v2 también 100%
  (no discrimina). Música NO es métrica de éxito.
- v1 vara narración ≥40% → SUBIDA a ≥70% (los 3 exitosos tienen 70-77%, pueblo
  fallido 30.9%).
- v1 detectaba "gaps narrativos >2s" como issue → ELIMINADO: los exitosos tienen
  gaps de 2-3s entre frases. Lo que importa es la avg block duration, no gaps.
- NUEVO: avg block duration ≥4.5s (los exitosos tienen 4.7-6.1s, pueblo fallido
  2.34s — narrador tartamudea con frases cortas).
- NUEVO: sound fabric coverage ≥99% (narración + ambient + música cubren todo).

Umbrales VALIDADOS contra evidencia (4 videos):
  | Métrica              | mina v15 | bosque v10 | elige V7 | pueblo v2 |
  |----------------------|----------|------------|----------|-----------|
  | Narración coverage   | 77.0%    | 70.3%      | 72.9%    | 30.9% ❌  |
  | Avg block duration   | 6.07s    | 5.24s      | 4.73s    | 2.34s ❌  |
  | Sound fabric         | 100%     | 100%       | 99.9%    | 100%      |

Pueblo cumple sound fabric (música tapa) pero falla narración + avg block.

Usage:
  python audit-audio.py --video renders/draft.mp4 --html index.html
"""

import argparse
import json
import os
import re
import sys

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800


# UMBRALES validados contra los 3 videos exitosos (2026-05-13)
MIN_NARRATION_COVERAGE = 70.0    # %. mina 77, bosque 70.3, elige 72.9, pueblo 30.9 ❌
MIN_AVG_BLOCK_DURATION = 4.5     # s. mina 6.07, bosque 5.24, elige 4.73, pueblo 2.34 ❌
MIN_BLOCK_DURATION = 3.0         # s. para bloques NO transicionales
MIN_SOUND_FABRIC_COVERAGE = 99.0 # %. todos los exitosos: 100. dead zones >1s = fail.

# LUFS target (Instagram Reels standard, validado contra 7 referentes -13.76 a -14.45)
TARGET_LUFS = -14.0
LUFS_TOLERANCE = 0.5  # ±0.5 dB acceptable


def get_video_duration(video_path: str) -> float:
    import subprocess
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True, check=True
    , timeout=SUBPROCESS_TIMEOUT_S)
    return float(result.stdout.strip())


def measure_lufs(video_path: str) -> dict:
    """Measure integrated LUFS via ffmpeg loudnorm. Returns dict with input_i, input_tp, input_lra."""
    import subprocess
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", video_path,
         "-af", f"loudnorm=I={TARGET_LUFS}:TP=-1:LRA=11:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True
    , timeout=SUBPROCESS_TIMEOUT_S)
    # ffmpeg writes loudnorm JSON to stderr
    output = result.stderr
    # Find JSON block
    try:
        start = output.rindex("{")
        end = output.rindex("}") + 1
        data = json.loads(output[start:end])
        return {
            "input_i": float(data.get("input_i", 0)),
            "input_tp": float(data.get("input_tp", 0)),
            "input_lra": float(data.get("input_lra", 0)),
            "input_thresh": float(data.get("input_thresh", 0)),
        }
    except (ValueError, json.JSONDecodeError, KeyError):
        return {"input_i": None, "input_tp": None, "input_lra": None, "input_thresh": None}


def categorize_track(src: str, duration: float) -> str:
    """Categorize audio track by src name (NOT track-index — that's project-dependent).

    Heurística validada contra 4 videos:
    - narration: src contains "narr"
    - music: src contains "music"
    - tick: src contains "tick"
    - ambient_continuous: src contains "ambient" OR (forest-wind|desert-wind|cave-drone) OR duration >= 60s with vol < 0.3
    - ambient_long: duration >= 8.0s (loops largos: footsteps, fire-crackle)
    - ambient_short: duration >= 3.0s (drones cortos, builds, exhales largos)
    - event: duration < 3.0s (flashes, stabs, thuds, whispers cortos)
    """
    src_lower = src.lower()

    if "narr" in src_lower:
        return "narration"
    if "music" in src_lower:
        return "music"
    if "tick" in src_lower:
        return "tick"
    if any(kw in src_lower for kw in ["ambient", "forest-wind", "desert-wind", "cave-drone",
                                       "footsteps-loop", "fire-crackle", "fire-loop",
                                       "wind-full", "wind-loop", "loop"]):
        return "ambient_continuous"
    if duration >= 8.0:
        return "ambient_long"
    if duration >= 3.0:
        return "ambient_short"
    return "event"


def parse_html_tracks(html_path: str) -> list:
    """Parse all <audio> elements from index.html."""
    if not os.path.exists(html_path):
        return []
    with open(html_path) as f:
        content = f.read()
    pattern = re.compile(
        r'<audio[^>]+src="([^"]+)"[^>]+data-start="([\d.]+)"[^>]+data-duration="([\d.]+)"[^>]+data-track-index="(\d+)"[^>]*?(?:data-volume="([\d.]+)")?',
        re.DOTALL
    )
    tracks = []
    for m in pattern.finditer(content):
        src = m.group(1)
        start = float(m.group(2))
        duration = float(m.group(3))
        track_idx = int(m.group(4))
        vol = float(m.group(5)) if m.group(5) else 1.0
        category = categorize_track(src, duration)
        tracks.append({
            "src": src, "start": start, "duration": duration,
            "end": start + duration, "track": track_idx,
            "vol": vol, "category": category
        })
    return tracks


def coverage_pct(tracks: list, video_duration: float, resolution: float = 0.1) -> float:
    """Calculate coverage % of given track list across video duration."""
    if not tracks:
        return 0.0
    units = int(video_duration / resolution)
    covered = set()
    for t in tracks:
        for u in range(int(t["start"] / resolution), int(t["end"] / resolution)):
            if 0 <= u < units:
                covered.add(u)
    return (len(covered) / units) * 100


def find_dead_zones(tracks: list, video_duration: float,
                     min_gap_seconds: float = 1.0, resolution: float = 0.1) -> list:
    """Find segments with NO active tracks. Returns list of (start, end, duration)."""
    if not tracks:
        return [(0, video_duration, video_duration)]
    units = int(video_duration / resolution)
    covered = [False] * units
    for t in tracks:
        for u in range(int(t["start"] / resolution), int(t["end"] / resolution)):
            if 0 <= u < units:
                covered[u] = True
    zones = []
    in_zone = False
    zone_start = 0
    for u in range(units):
        if not covered[u]:
            if not in_zone:
                zone_start = u * resolution
                in_zone = True
        else:
            if in_zone:
                zone_end = u * resolution
                dur = zone_end - zone_start
                if dur >= min_gap_seconds:
                    zones.append((zone_start, zone_end, dur))
                in_zone = False
    if in_zone:
        zone_end = units * resolution
        dur = zone_end - zone_start
        if dur >= min_gap_seconds:
            zones.append((zone_start, zone_end, dur))
    return zones


def analyze(video_path: str, html_path: str, measure_loudness: bool = True) -> dict:
    """Main analysis."""
    duration = get_video_duration(video_path)
    tracks = parse_html_tracks(html_path)
    lufs_data = measure_lufs(video_path) if measure_loudness else {"input_i": None}

    by_cat = {}
    for t in tracks:
        by_cat.setdefault(t["category"], []).append(t)

    narration = by_cat.get("narration", [])
    music = by_cat.get("music", [])
    ambient_c = by_cat.get("ambient_continuous", [])
    ambient_l = by_cat.get("ambient_long", [])
    ambient_s = by_cat.get("ambient_short", [])
    events = by_cat.get("event", [])
    ticks = by_cat.get("tick", [])

    all_ambient = ambient_c + ambient_l + ambient_s
    sound_fabric = narration + music + all_ambient

    avg_narr = sum(t["duration"] for t in narration) / len(narration) if narration else 0
    min_narr = min((t["duration"] for t in narration), default=0)
    max_narr = max((t["duration"] for t in narration), default=0)
    short_blocks = [t for t in narration if t["duration"] < MIN_BLOCK_DURATION]

    report = {
        "video_duration": round(duration, 2),
        "mastering": {
            "lufs_integrated": round(lufs_data["input_i"], 2) if lufs_data["input_i"] is not None else None,
            "true_peak": round(lufs_data["input_tp"], 2) if lufs_data.get("input_tp") is not None else None,
            "lra": round(lufs_data["input_lra"], 2) if lufs_data.get("input_lra") is not None else None,
            "target_lufs": TARGET_LUFS,
            "tolerance": LUFS_TOLERANCE,
        },
        "counts": {
            "narration": len(narration),
            "music": len(music),
            "ambient_continuous": len(ambient_c),
            "ambient_long": len(ambient_l),
            "ambient_short": len(ambient_s),
            "event": len(events),
            "tick": len(ticks),
        },
        "coverage": {
            "narration_pct": round(coverage_pct(narration, duration), 1),
            "music_pct": round(coverage_pct(music, duration), 1),
            "ambient_pct": round(coverage_pct(all_ambient, duration), 1),
            "sound_fabric_pct": round(coverage_pct(sound_fabric, duration), 1),
        },
        "narration_quality": {
            "avg_block": round(avg_narr, 2),
            "min_block": round(min_narr, 2),
            "max_block": round(max_narr, 2),
            "short_blocks_count": len(short_blocks),
            "short_blocks": [{"src": t["src"], "duration": round(t["duration"], 2)} for t in short_blocks],
        },
        "dead_zones": find_dead_zones(sound_fabric, duration, min_gap_seconds=1.0),
        "issues": [],
    }

    # Validation against thresholds
    nc = report["coverage"]["narration_pct"]
    avg = report["narration_quality"]["avg_block"]
    sf = report["coverage"]["sound_fabric_pct"]
    dz = report["dead_zones"]

    if nc < MIN_NARRATION_COVERAGE:
        report["issues"].append(
            f"LOW_NARRATION_COVERAGE: {nc}% (vara ≥{MIN_NARRATION_COVERAGE}%). "
            f"Los 3 videos exitosos tienen 70-77%."
        )
    if avg < MIN_AVG_BLOCK_DURATION:
        report["issues"].append(
            f"SHORT_NARRATION_BLOCKS: avg {avg}s (vara ≥{MIN_AVG_BLOCK_DURATION}s). "
            f"Narrador 'tartamudea' con frases cortas. Los exitosos tienen 4.73-6.07s."
        )
    # Short blocks tolerable hasta 7 (validado: mina 1, bosque 4, elige 5, pueblo 10)
    # No es regla independiente — el avg ya discrimina. Solo flag si extremo.
    if len(short_blocks) > 7:
        report["issues"].append(
            f"TOO_MANY_SHORT_BLOCKS: {len(short_blocks)} bloques <{MIN_BLOCK_DURATION}s "
            f"(pueblo fallido tenía 10). Reescribir guion con frases más largas."
        )
    if sf < MIN_SOUND_FABRIC_COVERAGE:
        report["issues"].append(
            f"DEAD_ZONES: sound fabric solo {sf}% (vara ≥{MIN_SOUND_FABRIC_COVERAGE}%). "
            f"Hay momentos sin narración + sin música + sin ambient."
        )
    for zone in dz:
        if zone[2] >= 2.0:
            report["issues"].append(
                f"DEAD_ZONE_LONG: {zone[2]:.2f}s sin sonido entre {zone[0]:.2f}s y {zone[1]:.2f}s"
            )

    # LUFS check (post 2026-05-13 — referent-validated)
    lufs = report["mastering"]["lufs_integrated"]
    if lufs is not None:
        if abs(lufs - TARGET_LUFS) > LUFS_TOLERANCE:
            report["issues"].append(
                f"LUFS_OFF_TARGET: integrated {lufs} dB (target {TARGET_LUFS} ±{LUFS_TOLERANCE}). "
                f"7/7 referentes Instagram entre -13.76 y -14.45. "
                f"Aplicar scripts/master-audio.sh para normalizar."
            )

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Audit audio v2 — basado en métricas validadas de los 3 videos exitosos."
    )
    parser.add_argument("--video", required=True, help="Path to MP4 render")
    parser.add_argument("--html", required=True, help="Path to index.html (REQUIRED)")
    parser.add_argument("--max-issues", type=int, default=0,
                        help="Fail if more than N issues (default 0 — vara estricta)")
    parser.add_argument("--output", help="Save JSON report")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video not found: {args.video}")
        return 2
    if not os.path.exists(args.html):
        print(f"ERROR: html not found: {args.html}")
        return 2

    print(f"🎵 Auditing audio (v2, vara basada en mina v15 / bosque v10 / elige V7)")
    print(f"   Video: {args.video}")
    print()

    report = analyze(args.video, args.html)

    print(f"Duration:                 {report['video_duration']}s")
    print(f"Tracks count:             narr={report['counts']['narration']} "
          f"music={report['counts']['music']} "
          f"ambient_cont={report['counts']['ambient_continuous']} "
          f"ambient_long={report['counts']['ambient_long']} "
          f"ambient_short={report['counts']['ambient_short']} "
          f"events={report['counts']['event']} "
          f"ticks={report['counts']['tick']}")
    print()
    print(f"Narration coverage:       {report['coverage']['narration_pct']}%  (vara ≥{MIN_NARRATION_COVERAGE}%)")
    print(f"Avg narration block:      {report['narration_quality']['avg_block']}s  (vara ≥{MIN_AVG_BLOCK_DURATION}s)")
    print(f"Short blocks (<{MIN_BLOCK_DURATION}s):     {report['narration_quality']['short_blocks_count']}")
    print(f"Sound fabric:             {report['coverage']['sound_fabric_pct']}%  (vara ≥{MIN_SOUND_FABRIC_COVERAGE}%)")
    print(f"Dead zones (≥1s):         {len(report['dead_zones'])}")
    if report['mastering']['lufs_integrated'] is not None:
        print(f"LUFS integrated:          {report['mastering']['lufs_integrated']} dB  (target {TARGET_LUFS} ±{LUFS_TOLERANCE})")
        print(f"True peak:                {report['mastering']['true_peak']} dBTP")
        print(f"LRA:                      {report['mastering']['lra']} LU")
    print()

    if report["issues"]:
        print(f"❌ Issues ({len(report['issues'])}):")
        for issue in report["issues"]:
            print(f"   • {issue}")
        if report['narration_quality']['short_blocks']:
            print()
            print(f"   Short blocks detail:")
            for b in report['narration_quality']['short_blocks']:
                print(f"     - {b['src']}: {b['duration']}s")
        print()

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved: {args.output}")

    if len(report["issues"]) > args.max_issues:
        print(f"❌ AUDIO AUDIT FAILED — {len(report['issues'])} issues (max {args.max_issues})")
        print(f"   Vara basada en mina v15 / bosque v10 / elige V7. NO ajustar al alza para 'pasar'.")
        return 1

    print(f"✅ AUDIO AUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
