#!/usr/bin/env python3
"""audit-spec-lip-sync-marks.py — BUILD 8 PRE-4.J helper.

Validates SPEC per-shot lip_sync_required declarations (D17 architect compliance):
1. COVERAGE: every shot declares lip_sync_required (true|false). Missing → FAIL.
2. CONSISTENCY: if shot has dialog_text OR speaker matches `character_*`, then
   lip_sync_required MUST be true. False → FAIL inconsistency (Sync.so layer needed).

Capability-aware: gates on has_tts_narration AND has_layer_2_effects (typical lip-sync
production stack). If either false → not_applicable. video_capabilities missing → Bug #9.

Build PRE-4.J BUILD 8 (2026-05-27) — TDD + Hard Rule #26 companion test.
Pairs with horror-choice-format/lip-sync-workflow.md (Capa B doc).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    caps = spec.get("video_capabilities")
    if caps is None:
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
              file=sys.stderr)
        return 2

    needs_check = bool(caps.get("has_tts_narration", False)) and bool(caps.get("has_layer_2_effects", False))

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\n"
              f"has_tts_narration: {caps.get('has_tts_narration', False)}\n"
              f"has_layer_2_effects: {caps.get('has_layer_2_effects', False)}\n"
              f"branch: {'lip_sync_check' if needs_check else 'not_applicable'}")
        return 0

    if not needs_check:
        report = {
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_tts_narration AND has_layer_2_effects must both be true for lip-sync check"
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    shots = spec.get("shot_list") or []
    fails = []
    ok = []
    for s in shots:
        sid = s.get("shot_id", "?")
        # v11 canonical: sibling `has_lip_sync_required` (bool); synthetic fixtures: `lip_sync_required`.
        lsr = s.get("lip_sync_required")
        if lsr is None:
            lsr = s.get("has_lip_sync_required")
        if lsr is None:
            fails.append({"shot_id": sid, "reason": "lip_sync_required/has_lip_sync_required missing (D17 architect audit)"})
            continue
        # consistency: dialog_text or character speaker → lip_sync flag must be true.
        # v11: dialog_text is a SIBLING of the shot; synthetic fixtures nest it under narration_in_this_shot.
        nis = s.get("narration_in_this_shot")
        nis_d = nis if isinstance(nis, dict) else {}
        speaker = str(nis_d.get("speaker", ""))
        has_dialog = bool(nis_d.get("dialog_text") or s.get("dialog_text"))
        has_char_speaker = speaker.startswith("character_") or speaker.startswith("char_")
        character_speaking = has_dialog or has_char_speaker
        # CANONICAL EXCEPTION (AUDITOR-PROTOCOL CP4): a faceless character (no mouth — e.g. visor /
        # mask) delivers dialogue via VOICE-OFF, so lip_sync_required=false is CORRECT, not an
        # inconsistency. Honored when the shot declares `voice_off: true` OR `faceless_character: true`.
        # Calca ref-10 (Rurik hazmat sin boca). Without this, V5 Axel (visor) voice-off shots false-FAIL.
        voice_off = bool(s.get("voice_off") or s.get("faceless_character"))
        if character_speaking and lsr is False and not voice_off:
            fails.append({
                "shot_id": sid, "lip_sync_required": False,
                "reason": ("inconsistency: shot has character speech (dialog_text or speaker=character_*) "
                           "but lip_sync_required=false and no voice_off/faceless_character declared "
                           "→ Sync.so layer needed but not flagged"),
                "speaker": speaker, "has_dialog_text": has_dialog,
            })
        else:
            ok.append({"shot_id": sid, "lip_sync_required": lsr,
                       "character_speaking_detected": character_speaking,
                       "voice_off_exception": voice_off})

    overall = "fail" if fails else "pass"
    report = {
        "format": args.format, "spec": str(spec_path),
        "overall_status": overall, "overall_pass": not fails,
        "fail_shots": fails, "ok_shots": ok,
        "total_checked": len(fails) + len(ok),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
