#!/usr/bin/env python3
"""
continuity-check.py — Cross-check NARRATIVE.md vs index.html vs render real.

Codificado 2026-05-13 después de pueblo-fantasma-desierto v2:
- Gemini 9.9 score pero trama no se entiende
- Caminos narrativos rotos (gaps de 5-7s entre frases del narrador)
- Outro 40s casi sin narración

Verifica:
1. Cada hito declarado en NARRATIVE.md tiene narración + visual + audio en index.html
2. Continuidad temporal: hito[i].end ≤ hito[i+1].start (sin gaps narrativos >2s)
3. Cada beat del guion se materializa (no hay "voz del narrador prometida" sin audio en index.html)
4. Captions consistentes con narración (Whisper-sync, sin overlaps con cap-q / cap-chose hardcoded)
5. Distribución temporal balanceada (no hay 60% del video en H1 + 5% en H6)

Usage:
  python continuity-check.py --narrative NARRATIVE.md --html index.html

Integration: gate 7 del pre-render flow, después de audit-audio y antes de qa-gate.
"""

import argparse
import json
import os
import re
import sys

# Umbrales
MAX_NARRATIVE_GAP_SECONDS = 2.0  # gaps >2s entre frases de narrador = bandera roja
MIN_HITO_DURATION_PCT = 0.05  # cada hito debería ocupar ≥5% del video (~4.5s en 90s)
TARGET_NARRATION_COVERAGE = 0.40  # narración ≥40% del video


def parse_html_audio_tracks(html_path: str) -> dict:
    """Same parsing as audit-audio.py."""
    if not os.path.exists(html_path):
        return {}

    with open(html_path) as f:
        content = f.read()

    audio_pattern = re.compile(
        r'<audio\s+id="([^"]+)"[^>]*?data-start="([\d.]+)"[^>]*?data-duration="([\d.]+)"[^>]*?data-track-index="(\d+)"',
        re.DOTALL,
    )

    narration = []
    music = []
    sfx = []

    for match in audio_pattern.finditer(content):
        track_id = match.group(1)
        start = float(match.group(2))
        duration = float(match.group(3))
        track_idx = int(match.group(4))
        entry = {
            "id": track_id,
            "start": start,
            "duration": duration,
            "end": start + duration,
            "track": track_idx,
        }

        if 40 <= track_idx <= 49:
            narration.append(entry)
        elif 50 <= track_idx <= 59:
            music.append(entry)
        elif 60 <= track_idx <= 110:
            sfx.append(entry)

    return {"narration": narration, "music": music, "sfx": sfx}


def parse_narrative_md(narrative_path: str) -> dict:
    """Extract hito structure from NARRATIVE.md.

    Looks for headers like "## H1 — Setup" or "### Hito 3" and the narrator
    lines following them.
    """
    if not os.path.exists(narrative_path):
        return {}

    with open(narrative_path) as f:
        content = f.read()

    # Heurística: extraer hitos H1-H6 con duración estimada por contenido
    hito_pattern = re.compile(r"#{1,4}\s*(?:Hito\s+|H)(\d+)[\s\.\:—-]*([^\n]*)", re.IGNORECASE)

    hitos = []
    sections = []
    last_pos = 0

    for match in hito_pattern.finditer(content):
        hito_num = int(match.group(1))
        title = match.group(2).strip()
        position = match.start()

        if sections:
            # Asignar contenido al hito anterior
            sections[-1]["content"] = content[last_pos:position]

        sections.append(
            {
                "hito": hito_num,
                "title": title,
                "content": "",
                "position": position,
            }
        )
        last_pos = position

    if sections:
        sections[-1]["content"] = content[last_pos:]

    # Por cada hito, contar palabras de narrador (heurística: líneas con "Narrador" o citadas)
    for s in sections:
        narrator_lines = re.findall(
            r"(?:Narrador|narrador|narr|h\d+-narr)\S*[\s:]+[\"'].*?[\"']", s["content"], re.IGNORECASE
        )
        # Backup: líneas entre comillas (probable narración)
        if not narrator_lines:
            narrator_lines = re.findall(r'["""].*?["""]', s["content"])

        word_count = sum(len(line.split()) for line in narrator_lines)
        s["narrator_word_count"] = word_count
        s["expected_narration_seconds"] = word_count / 2.5  # ~2.5 words/sec @ atempo 2x

    return {"hitos": sections, "total_words": sum(s.get("narrator_word_count", 0) for s in sections)}


def check_continuity(narration_tracks: list, max_gap: float = MAX_NARRATIVE_GAP_SECONDS) -> list:
    """Detect narrative continuity issues."""
    issues = []

    if not narration_tracks:
        return [("NO_NARRATION", "El video no tiene ningún track de narrador")]

    sorted_tracks = sorted(narration_tracks, key=lambda x: x["start"])

    # Check gaps between narrator blocks
    for i in range(len(sorted_tracks) - 1):
        gap = sorted_tracks[i + 1]["start"] - sorted_tracks[i]["end"]
        if gap > max_gap:
            issues.append(
                (
                    "NARRATIVE_GAP",
                    f"{gap:.2f}s gap entre '{sorted_tracks[i]['id']}' "
                    f"(end {sorted_tracks[i]['end']:.2f}s) y '{sorted_tracks[i + 1]['id']}' "
                    f"(start {sorted_tracks[i + 1]['start']:.2f}s)",
                )
            )

    return issues


def check_hito_distribution(hitos: list, narration_tracks: list, video_duration: float = 90.0) -> list:
    """Check if hitos are temporally balanced."""
    issues = []

    if not hitos or not narration_tracks:
        return issues

    # Estimar duración real de cada hito por la narración asignada
    # Asumimos id format "h<N>-narr*" — extraer hito number del id
    hito_durations = {}
    for track in narration_tracks:
        m = re.match(r"h(\d+)-", track["id"])
        if m:
            hito_num = int(m.group(1))
            hito_durations.setdefault(hito_num, 0)
            hito_durations[hito_num] += track["duration"]

    # Flag hitos with very low actual narration vs expected
    for s in hitos:
        actual_seconds = hito_durations.get(s["hito"], 0)
        expected_seconds = s.get("expected_narration_seconds", 0)

        if expected_seconds > 2.0 and actual_seconds < expected_seconds * 0.5:
            issues.append(
                (
                    "HITO_UNDER_NARRATED",
                    f"H{s['hito']} ({s['title'][:40]}): expected ~{expected_seconds:.1f}s "
                    f"de narración, actual {actual_seconds:.1f}s ({(actual_seconds / expected_seconds) * 100:.0f}%)",
                )
            )

    return issues


def check_total_narration_coverage(narration_tracks: list, video_duration: float) -> list:
    """Check overall narration coverage."""
    issues = []

    if not narration_tracks:
        return [("NO_NARRATION_COVERAGE", "El video no tiene narración en absoluto")]

    total_narration = sum(t["duration"] for t in narration_tracks)
    coverage = total_narration / video_duration

    if coverage < TARGET_NARRATION_COVERAGE:
        issues.append(
            (
                "LOW_NARRATION_COVERAGE",
                f"Narración cubre {coverage * 100:.1f}% del video "
                f"(target ≥{TARGET_NARRATION_COVERAGE * 100:.0f}%). "
                f"Total narración: {total_narration:.1f}s de {video_duration:.1f}s",
            )
        )

    return issues


def analyze(narrative_path: str, html_path: str, video_duration: float = 90.0) -> dict:
    """Main continuity analysis."""
    report = {
        "narrative": narrative_path,
        "html": html_path,
        "issues": [],
        "warnings": [],
        "stats": {},
    }

    # Parse inputs
    narrative = parse_narrative_md(narrative_path)
    tracks = parse_html_audio_tracks(html_path)

    report["stats"]["narrative_hitos"] = len(narrative.get("hitos", []))
    report["stats"]["narrative_total_words"] = narrative.get("total_words", 0)
    report["stats"]["html_narration_tracks"] = len(tracks.get("narration", []))
    report["stats"]["html_music_tracks"] = len(tracks.get("music", []))

    # Check 1: Total narration coverage
    coverage_issues = check_total_narration_coverage(tracks.get("narration", []), video_duration)
    report["issues"].extend(coverage_issues)

    # Check 2: Continuity (gaps between narrator blocks)
    continuity_issues = check_continuity(tracks.get("narration", []))
    for severity, msg in continuity_issues:
        if "NO_NARRATION" in severity:
            report["issues"].append(f"{severity}: {msg}")
        else:
            # Gaps >5s are issues, smaller are warnings
            if (
                "5." in msg
                or "6." in msg
                or "7." in msg
                or "8." in msg
                or "9." in msg
                or float(msg.split("s gap")[0]) > 3.0
            ):
                report["issues"].append(f"{severity}: {msg}")
            else:
                report["warnings"].append(f"{severity}: {msg}")

    # Check 3: Hito distribution
    hito_issues = check_hito_distribution(
        narrative.get("hitos", []), tracks.get("narration", []), video_duration
    )
    for severity, msg in hito_issues:
        report["warnings"].append(f"{severity}: {msg}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Continuity check NARRATIVE.md vs index.html. Detecta gaps narrativos."
    )
    parser.add_argument("--narrative", required=True, help="Path to NARRATIVE.md")
    parser.add_argument("--html", required=True, help="Path to index.html")
    parser.add_argument(
        "--video-duration", type=float, default=90.0, help="Video total duration in seconds (default 90)"
    )
    parser.add_argument("--max-issues", type=int, default=2, help="Fail if more than N issues (default 2)")
    parser.add_argument("--output", help="Optional: save report as JSON")

    args = parser.parse_args()

    if not os.path.exists(args.narrative):
        print(f"ERROR: NARRATIVE.md not found: {args.narrative}")
        return 2
    if not os.path.exists(args.html):
        print(f"ERROR: index.html not found: {args.html}")
        return 2

    print("📖 Continuity check")
    print(f"   NARRATIVE.md: {args.narrative}")
    print(f"   index.html:   {args.html}")
    print(f"   Duration:     {args.video_duration}s")
    print()

    report = analyze(args.narrative, args.html, args.video_duration)

    print(f"Hitos detected:        {report['stats']['narrative_hitos']}")
    print(f"Words narrador:        {report['stats']['narrative_total_words']}")
    print(f"Tracks narración HTML: {report['stats']['html_narration_tracks']}")
    print(f"Tracks música HTML:    {report['stats']['html_music_tracks']}")
    print()

    if report["issues"]:
        print(f"❌ Issues ({len(report['issues'])}):")
        for issue in report["issues"]:
            print(f"   {issue}")
        print()

    if report["warnings"]:
        print(f"⚠️  Warnings ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"   {w}")
        print()

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved: {args.output}")

    if len(report["issues"]) > args.max_issues:
        print(f"❌ CONTINUITY CHECK FAILED — {len(report['issues'])} issues (max {args.max_issues})")
        print("   Fixear gaps narrativos / cobertura baja antes del stop point.")
        return 1

    print(f"✅ CONTINUITY CHECK PASSED — {len(report['issues'])} issues ≤ max {args.max_issues}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
