#!/usr/bin/env python3
"""
audit-spec-completeness.py — SPEC asset_list + ui_active inventory diff vs actual filesystem.

Closes GAP #13 (matadero CP5 STOP point 2026-05-19): engineer can declare STOP with
sub-CPs ungenerated (SFX/music/ambient/UI elements) because existing audits measure
QUALITY of what exists, NOT INVENTORY against SPEC. This script measures inventory.

Authority:
- AUDITOR-PROTOCOL § 3 CP4 step 8 + CP5 step 9 C-INVENTORY-WIRED BLOQUEANTE
- TEAM-PROTOCOL § 10 engineer STOP point inventory table OBLIGATORIA
- GAPS-LOG.md gap #13

Usage:
    python audit-spec-completeness.py \\
        --spec creative-specs/<id>.yaml \\
        --project-dir . \\
        [--cp 4|5] \\
        [--html index.html] \\
        [--strict]

Exit codes:
    0 — ALL inventory PASS (engineer can emit STOP, auditor can continue to other gates)
    1 — ANY inventory FAIL (engineer blocked from STOP, auditor blocks CP5 gates)
    2 — script error (missing SPEC, missing project dir, etc.)
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def parse_spec(spec_path: Path) -> dict:
    """Load SPEC.yaml and extract asset_list + ui_active."""
    with open(spec_path) as f:
        return yaml.safe_load(f)


def count_in_dir(dir_path: Path, patterns: list) -> int:
    """Count files matching any pattern in directory."""
    if not dir_path.exists():
        return 0
    count = 0
    for pattern in patterns:
        count += len(list(dir_path.glob(pattern)))
    return count


def grep_count(html_path: Path, pattern: str) -> int:
    """Count regex matches in HTML file."""
    if not html_path.exists():
        return 0
    with open(html_path) as f:
        content = f.read()
    return len(re.findall(pattern, content, re.IGNORECASE))


def collect_ui_active_per_shot(spec: dict) -> dict:
    """Extract ui_active list per shot from SPEC. shot_list can be list or {shots: [...]}."""
    ui_counts = {"countdown": 0, "choice_button": 0, "loading_bar": 0,
                 "name_label": 0, "watermark": 0, "caption": 0}
    shot_list = spec.get("shot_list", [])
    if isinstance(shot_list, dict):
        shots = shot_list.get("shots", [])
    else:
        shots = shot_list if isinstance(shot_list, list) else []
    for shot in shots:
        ui_active = shot.get("ui_active", [])
        for elem in ui_active:
            # Support both string-form ("countdown") and dict-form ({"element_id": "countdown", ...}).
            # Schema v11+ uses dict-form. Backported from cerro-aislado-v4 in-place fix
            # per Sub-Fase 3A 2026-05-23 (CP5-handoff.md L83).
            if isinstance(elem, dict):
                elem_str = " ".join(str(v) for v in elem.values() if isinstance(v, str))
            else:
                elem_str = str(elem)
            elem_lower = elem_str.lower()
            if "countdown" in elem_lower:
                ui_counts["countdown"] += 1
            elif "choice" in elem_lower or "button" in elem_lower:
                ui_counts["choice_button"] += 1
            elif "loading" in elem_lower:
                ui_counts["loading_bar"] += 1
            elif "name_label" in elem_lower:
                ui_counts["name_label"] += 1
            elif "watermark" in elem_lower:
                ui_counts["watermark"] += 1
            elif "caption" in elem_lower:
                ui_counts["caption"] += 1
    return ui_counts


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--spec", required=True, help="Path to SPEC.yaml")
    p.add_argument("--project-dir", default=".", help="Project root (default: cwd)")
    p.add_argument("--cp", type=int, default=5, choices=[4, 5],
                   help="Checkpoint level (4=video only, 5=full inventory)")
    p.add_argument("--html", default="index.html", help="HTML file relative to project")
    p.add_argument("--strict", action="store_true",
                   help="Exit 1 on ANY mismatch (default: only on critical gaps)")
    args = p.parse_args()

    spec_path = Path(args.spec)
    proj_dir = Path(args.project_dir).resolve()
    html_path = proj_dir / args.html

    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        sys.exit(2)
    if not proj_dir.exists():
        print(f"ERROR: project dir not found: {proj_dir}", file=sys.stderr)
        sys.exit(2)

    spec = parse_spec(spec_path)
    asset_list = spec.get("asset_list", {})

    rows = []
    has_fail = False

    # ===== Audio assets =====
    print(f"\n=== AUDIT SPEC COMPLETENESS — CP{args.cp} ===")
    print(f"SPEC: {spec_path}")
    print(f"Project: {proj_dir}")
    print()
    print(f"{'Asset class':<28} {'SPEC':>6} {'Actual':>8} {'Status':>10}")
    print("-" * 56)

    # SFX
    sfx_spec = len(asset_list.get("sfx_prompts_to_generate", []) or [])
    sfx_actual = count_in_dir(proj_dir / "assets" / "sfx", ["*.mp3", "*.wav"])
    sfx_status = "✅ PASS" if sfx_actual >= sfx_spec else "🔴 FAIL"
    rows.append(("SFX prompts", sfx_spec, sfx_actual, sfx_status))
    if sfx_actual < sfx_spec:
        has_fail = True
    print(f"{'SFX prompts':<28} {sfx_spec:>6} {sfx_actual:>8} {sfx_status:>10}")

    # Music
    music_spec = len(asset_list.get("music_to_generate", []) or [])
    music_actual = count_in_dir(proj_dir / "assets" / "music", ["*.mp3", "*.wav"])
    music_status = "✅ PASS" if music_actual >= music_spec else "🔴 FAIL"
    rows.append(("Music tracks", music_spec, music_actual, music_status))
    if music_actual < music_spec:
        has_fail = True
    print(f"{'Music tracks':<28} {music_spec:>6} {music_actual:>8} {music_status:>10}")

    # Ambient
    amb_spec = len(asset_list.get("ambient_continuous_to_generate", []) or [])
    amb_actual = count_in_dir(proj_dir / "assets" / "ambient", ["*.mp3", "*.wav"])
    amb_status = "✅ PASS" if amb_actual >= amb_spec else "🔴 FAIL"
    rows.append(("Ambient continuous", amb_spec, amb_actual, amb_status))
    if amb_actual < amb_spec:
        has_fail = True
    print(f"{'Ambient continuous':<28} {amb_spec:>6} {amb_actual:>8} {amb_status:>10}")

    # TTS
    tts_spec = asset_list.get("tts_segments_to_generate", 0) or 0
    tts_actual = count_in_dir(proj_dir / "assets" / "tts", ["*.mp3", "*.wav"])
    tts_status = "✅ PASS" if tts_actual >= tts_spec else "🔴 FAIL"
    rows.append(("TTS segments", tts_spec, tts_actual, tts_status))
    if tts_actual < tts_spec:
        has_fail = True
    print(f"{'TTS segments':<28} {tts_spec:>6} {tts_actual:>8} {tts_status:>10}")

    # Shot clips
    shot_total = asset_list.get("shot_list_total", 0) or 0
    clip_actual = count_in_dir(proj_dir / "assets" / "clips", ["shot_*.mp4"])
    clip_status = "✅ PASS" if clip_actual >= shot_total else "🔴 FAIL"
    rows.append(("Shot clips base", shot_total, clip_actual, clip_status))
    if clip_actual < shot_total:
        has_fail = True
    print(f"{'Shot clips base':<28} {shot_total:>6} {clip_actual:>8} {clip_status:>10}")

    # CP5 additional: UI elements + audio tracks
    if args.cp >= 5:
        print()
        print(f"{'UI element / track':<28} {'SPEC':>6} {'Wired':>8} {'Status':>10}")
        print("-" * 56)

        ui_counts = collect_ui_active_per_shot(spec)

        # Countdown
        cd_spec = ui_counts["countdown"]
        cd_html = grep_count(html_path, r"countdown")
        cd_status = "✅ PASS" if cd_html > 0 or cd_spec == 0 else "🔴 FAIL"
        if cd_spec > 0 and cd_html == 0:
            has_fail = True
        rows.append(("Countdown UI", cd_spec, cd_html, cd_status))
        print(f"{'Countdown UI':<28} {cd_spec:>6} {cd_html:>8} {cd_status:>10}")

        # Choice buttons
        cb_spec = ui_counts["choice_button"]
        cb_html = grep_count(html_path, r"choice[-_]button|choice-btn")
        cb_status = "✅ PASS" if cb_html > 0 or cb_spec == 0 else "🔴 FAIL"
        if cb_spec > 0 and cb_html == 0:
            has_fail = True
        rows.append(("Choice buttons", cb_spec, cb_html, cb_status))
        print(f"{'Choice buttons':<28} {cb_spec:>6} {cb_html:>8} {cb_status:>10}")

        # Loading bar
        lb_spec = ui_counts["loading_bar"]
        lb_html = grep_count(html_path, r"loading[-_]bar|loading-bar")
        lb_status = "✅ PASS" if lb_html > 0 or lb_spec == 0 else "🔴 FAIL"
        if lb_spec > 0 and lb_html == 0:
            has_fail = True
        rows.append(("Loading bar", lb_spec, lb_html, lb_status))
        print(f"{'Loading bar':<28} {lb_spec:>6} {lb_html:>8} {lb_status:>10}")

        # Audio tracks (minimum 4 = narration + music + ambient + sfx)
        audio_tracks = grep_count(html_path, r"<audio")
        min_tracks = 1  # narration minimum
        if music_spec > 0:
            min_tracks += 1
        if amb_spec > 0:
            min_tracks += 1
        if sfx_spec > 0:
            min_tracks += 1
        at_status = "✅ PASS" if audio_tracks >= min_tracks else "🔴 FAIL"
        if audio_tracks < min_tracks:
            has_fail = True
        rows.append(("Audio tracks wired", min_tracks, audio_tracks, at_status))
        print(f"{'Audio tracks wired':<28} {min_tracks:>6} {audio_tracks:>8} {at_status:>10}")

    print()
    print("=" * 56)
    if has_fail:
        print("🔴 VERDICT: INVENTORY INCOMPLETE — engineer cannot STOP, auditor blocks CP5 gates")
        print()
        print("Failed rows:")
        for label, spec_n, actual_n, status in rows:
            if "FAIL" in status:
                print(f"  {status} {label}: SPEC={spec_n} / Actual={actual_n}")
        print()
        print("Fix: continue execute hasta ALL inventory PASS. See AUDITOR-PROTOCOL § 3 CP5 step 9.")
        sys.exit(1)
    else:
        print("✅ VERDICT: INVENTORY COMPLETE — STOP point VALID, CP5 gates can proceed")
        sys.exit(0)


if __name__ == "__main__":
    main()
