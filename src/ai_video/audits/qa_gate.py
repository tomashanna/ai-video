#!/usr/bin/env python3
"""
qa-gate.py — Dual quality gate per CLAUDE.md Hard Rule #1 (updated 2026-05-21 PM late).

LEGACY mode (--score): single-threshold gate. Preserved for back-compat.
CANONICAL mode (--calibrated + optional --perceptual): dual-branch per Hard Rule #1:
  (a) gemini_calibrated_v4 ≥ threshold_calibrated → PASS via calibrated branch
  (b) user_perceptual_score ≥ threshold_perceptual → PASS via Rule D PRECEDENCE
  OR logic: either branch sufficient. user_perceptual is ground truth final.

Thresholds read DYNAMICALLY from CLAUDE.md Hard Rule #1 via lib/hard_rules_parser.py
per Hard Rule #19 ("NEVER ESTIMATE, ALWAYS MEASURE" — no hardcoded constants).
CLAUDE_MD_PATH env var overridable for testing.

Status enum (Sub-Fase 3A 2026-05-23):
  PASS                     → exit 0
  BLOCKED                  → exit 1
  ESCALATE                 → exit 2 (>3 iter no convergence, or invalid args)
  AWAITING_USER_PERCEPTUAL → exit 3 (NEW: calibrated FAIL + perceptual not provided)

Auto-generates project-scoped HUMAN-CHECKLIST instance when calibrated FAILS +
--project-dir + --project-id provided. Reads canonical template at
.claude/skills/video-director/HUMAN-CHECKLIST.md (READ-ONLY, never modified)
and writes <project_dir>/HUMAN-CHECKLIST-<project_id>.md with metadata header.

Usage:
  # Canonical dual-branch (Sub-Fase 3A forward):
  python qa-gate.py --calibrated 8.1 --perceptual 8.5 --stage pre-kling
    → PASS via Rule D precedence (perceptual 8.5 ≥ 8.5)

  python qa-gate.py --calibrated 8.1 --stage pre-kling \
                    --project-dir /path/to/project --project-id cerro-aislado-v4
    → AWAITING_USER_PERCEPTUAL (exit 3) + HUMAN-CHECKLIST-cerro-aislado-v4.md auto-generated

  # Legacy back-compat:
  python qa-gate.py --score 9.7 --stage pre-kling
    → PASS (single-threshold mode)

Authority: CLAUDE.md Hard Rule #1 + #19 + #26 (tests adversariales). Codified
Sub-Fase 3A 2026-05-23 post pattern_class "user_perceptual_detects_what_validators_miss".
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date
from pathlib import Path

from ai_video import paths
from ai_video.core.hard_rules_parser import (
    get_quality_threshold_calibrated,
    get_quality_threshold_perceptual,
    parse_hard_rules,
)

# Resolve canonical paths (repo-relative). Env vars allow test override; the legacy
# CLAUDE_MD_PATH / HUMAN_CHECKLIST_PATH names are still honoured.
CLAUDE_MD_PATH = Path(os.environ.get("CLAUDE_MD_PATH") or paths.hard_rules_doc())
HUMAN_CHECKLIST_CANONICAL = Path(
    os.environ.get("HUMAN_CHECKLIST_PATH") or paths.human_checklist_doc()
)

# Fallback thresholds when hard_rules_parser unavailable (defensive — should not happen
# if lib/ is properly copied per BOOTSTRAP). These mirror the canonical Hard Rule #1
# state as of 2026-05-21 PM late; if parser available, real CLAUDE.md values win.
_FALLBACK_CALIBRATED_THRESHOLD = 9.0
_FALLBACK_PERCEPTUAL_THRESHOLD = 8.5

# Legacy mode threshold (Hard Rule #1 pre-2026-05-21 historical threshold,
# preserved for back-compat with callers using --score).
_LEGACY_THRESHOLD = 9.7
_STRUCTURAL_ROT_THRESHOLD = 7.0


def _load_thresholds() -> tuple[float, float]:
    """Read canonical thresholds from CLAUDE.md via hard_rules_parser.

    Returns (calibrated_threshold, perceptual_threshold). Falls back to module
    constants if parser unavailable (defensive — emits stderr warning).
    """
    try:
        rules = parse_hard_rules(CLAUDE_MD_PATH)
        calibrated = get_quality_threshold_calibrated(rules)
        perceptual = get_quality_threshold_perceptual(rules)
        if calibrated is None or perceptual is None:
            print(
                f"⚠️ qa-gate: CLAUDE.md Rule #1 thresholds unparseable. "
                f"Falling back to constants ({_FALLBACK_CALIBRATED_THRESHOLD}, "
                f"{_FALLBACK_PERCEPTUAL_THRESHOLD}).",
                file=sys.stderr,
            )
            return _FALLBACK_CALIBRATED_THRESHOLD, _FALLBACK_PERCEPTUAL_THRESHOLD
        return calibrated, perceptual
    except Exception as e:
        print(
            f"⚠️ qa-gate: hard_rules_parser unavailable ({e}). Falling back to "
            f"constants ({_FALLBACK_CALIBRATED_THRESHOLD}, "
            f"{_FALLBACK_PERCEPTUAL_THRESHOLD}).",
            file=sys.stderr,
        )
        return _FALLBACK_CALIBRATED_THRESHOLD, _FALLBACK_PERCEPTUAL_THRESHOLD


def auto_generate_human_checklist(
    project_dir: Path,
    project_id: str,
    calibrated: float,
    perceptual: float | None,
    status: str,
    stage: str,
) -> Path:
    """Generate project-scoped HUMAN-CHECKLIST instance from canonical template.

    Reads HUMAN-CHECKLIST_CANONICAL (READ-ONLY, never modified) and writes
    <project_dir>/HUMAN-CHECKLIST-<project_id>.md with pre-filled metadata header.

    Returns the path written.
    """
    project_dir.mkdir(parents=True, exist_ok=True)
    target = project_dir / f"HUMAN-CHECKLIST-{project_id}.md"

    canonical_body = HUMAN_CHECKLIST_CANONICAL.read_text(encoding="utf-8")
    perceptual_display = f"{perceptual}" if perceptual is not None else "PENDIENTE"

    header = (
        f"# HUMAN-CHECKLIST instance — {project_id}\n\n"
        f"> Auto-generated by `qa-gate.py` (Sub-Fase 3A 2026-05-23) on "
        f"calibrated FAIL — user perceptual gate required per Hard Rule #1 Rule D PRECEDENCE.\n\n"
        f"**Project**: {project_id}\n"
        f"**Generated**: {date.today().isoformat()}\n"
        f"**Stage**: {stage}\n"
        f"**Calibrated score reported**: {calibrated}\n"
        f"**Perceptual score**: {perceptual_display}\n"
        f"**Status**: {status}\n\n"
        f"**Action required**: watch render once + fill 7-check table below "
        f"+ report findings to user. If ≥1 ✗ → not publishable, iterate. "
        f"If user_perceptual_score ≥8.5 (Rule D precedence) → can override calibrated FAIL.\n\n"
        f"---\n\n"
        f"## Canonical template (READ-ONLY reference, do not modify)\n\n"
    )
    target.write_text(header + canonical_body, encoding="utf-8")
    return target


def _legacy_gate(score: float, stage: str, iteration: int) -> int:
    """Legacy single-threshold gate (--score flag). Preserved for back-compat."""
    if score < _STRUCTURAL_ROT_THRESHOLD:
        print(f"🚨 STRUCTURAL ROT — score {score} < {_STRUCTURAL_ROT_THRESHOLD}")
        print(f"   Algo estructural está roto. NO iterar — escalar al usuario YA.")
        print(f"   Revisar diseño desde la raíz del NARRATIVE.md.")
        return 1

    if stage == "pre-kling":
        if score < _LEGACY_THRESHOLD:
            print(f"❌ PRE-KLING QA GATE BLOCKED (legacy mode)")
            print(f"   Score actual: {score} < umbral {_LEGACY_THRESHOLD}")
            print(f"   Iteración: {iteration}/3")
            print(f"   Iterar con fixes NO-KLING en orden A→B→C.")
            return 1
        print(f"✅ PRE-KLING QA GATE PASSED (legacy mode)")
        print(f"   Score: {score} ≥ {_LEGACY_THRESHOLD}")
        return 0

    elif stage == "post-kling":
        if score < _LEGACY_THRESHOLD:
            print(f"❌ POST-KLING QA GATE BLOCKED (legacy mode)")
            print(f"   Score actual: {score} < umbral {_LEGACY_THRESHOLD}")
            return 1
        print(f"✅ POST-KLING QA GATE PASSED (legacy mode)")
        print(f"   Score: {score} ≥ {_LEGACY_THRESHOLD}")
        return 0

    print(f"❌ INVALID STAGE: {stage}")
    return 1


def _dual_branch_gate(
    calibrated: float,
    perceptual: float | None,
    stage: str,
    iteration: int,
    project_dir: Path | None,
    project_id: str | None,
) -> int:
    """Canonical dual-branch gate per Hard Rule #1.

    Returns exit code: 0 = PASS, 1 = BLOCKED, 3 = AWAITING_USER_PERCEPTUAL.
    """
    if calibrated < _STRUCTURAL_ROT_THRESHOLD and (perceptual is None or perceptual < _STRUCTURAL_ROT_THRESHOLD):
        print(f"🚨 STRUCTURAL ROT — calibrated {calibrated} + perceptual "
              f"{perceptual or 'N/A'} both < {_STRUCTURAL_ROT_THRESHOLD}")
        print(f"   Algo estructural está roto. NO iterar — escalar al usuario YA.")
        return 1

    threshold_calibrated, threshold_perceptual = _load_thresholds()

    # Branch (a): calibrated PASS — sufficient, no need for perceptual.
    if calibrated >= threshold_calibrated:
        print(f"✅ {stage.upper()} QA GATE PASSED (calibrated branch)")
        print(f"   calibrated: {calibrated} ≥ threshold {threshold_calibrated}")
        if perceptual is not None:
            print(f"   perceptual: {perceptual} (informational)")
        print(f"   Source: CLAUDE.md Hard Rule #1 (threshold read dynamically)")
        return 0

    # Branch (b): perceptual ≥ threshold → PASS via Rule D PRECEDENCE.
    if perceptual is not None and perceptual >= threshold_perceptual:
        print(f"✅ {stage.upper()} QA GATE PASSED (perceptual branch — Rule D PRECEDENCE)")
        print(f"   calibrated: {calibrated} < threshold {threshold_calibrated} (would fail alone)")
        print(f"   perceptual: {perceptual} ≥ threshold {threshold_perceptual} (user ground truth overrides)")
        print(f"   Source: CLAUDE.md Hard Rule #1 dual gate OR logic")
        return 0

    # Neither branch satisfied yet.
    if perceptual is None:
        # Status AWAITING_USER_PERCEPTUAL — calibrated failed, perceptual pending user input.
        status = "AWAITING_USER_PERCEPTUAL"
        print(f"⏸️ {stage.upper()} QA GATE — status {status}")
        print(f"   calibrated: {calibrated} < threshold {threshold_calibrated} (FAIL)")
        print(f"   perceptual: NOT PROVIDED")
        print(f"   Per Hard Rule #1 Rule D PRECEDENCE: user_perceptual ≥{threshold_perceptual} "
              f"can override calibrated FAIL. User MUST watch render + report perceptual score.")
        if project_dir and project_id:
            target = auto_generate_human_checklist(
                project_dir, project_id, calibrated, perceptual, status, stage
            )
            print(f"   📋 HUMAN-CHECKLIST auto-generated: {target}")
        else:
            print(f"   (HUMAN-CHECKLIST auto-gen skipped — pass --project-dir + --project-id to enable)")
        return 3

    # Both branches FAILED (calibrated < threshold AND perceptual < threshold).
    print(f"❌ {stage.upper()} QA GATE BLOCKED")
    print(f"   calibrated: {calibrated} < threshold {threshold_calibrated}")
    print(f"   perceptual: {perceptual} < threshold {threshold_perceptual}")
    print(f"   Iteración: {iteration}/3. Iterar con fixes NO-KLING en orden A→B→C.")
    if project_dir and project_id:
        target = auto_generate_human_checklist(
            project_dir, project_id, calibrated, perceptual, "BLOCKED", stage
        )
        print(f"   📋 HUMAN-CHECKLIST auto-generated: {target}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "QA gate. CANONICAL: --calibrated [+ optional --perceptual] for dual-branch "
            "(Hard Rule #1). LEGACY: --score for single-threshold back-compat."
        )
    )
    # NOTE: --score and --calibrated are mutually exclusive at the semantic level,
    # but argparse allows either; main() validates explicitly.
    parser.add_argument(
        "--score", type=float, default=None,
        help="(LEGACY back-compat) single-threshold mode. Either --score OR --calibrated required."
    )
    parser.add_argument(
        "--calibrated", type=float, default=None,
        help="(CANONICAL forward) gemini_calibrated_v4 score (0.0-10.0)."
    )
    parser.add_argument(
        "--perceptual", type=float, default=None,
        help="(CANONICAL forward) user_perceptual_score (0.0-10.0). Optional; if missing → AWAITING_USER_PERCEPTUAL."
    )
    parser.add_argument(
        "--stage", choices=["pre-kling", "post-kling"], required=True,
        help="Pipeline stage."
    )
    parser.add_argument(
        "--iteration", type=int, default=1,
        help="Iteration number (1-3). After 3 sub-threshold iter → ESCALATE."
    )
    parser.add_argument(
        "--project-dir", type=Path, default=None,
        help="Project directory for HUMAN-CHECKLIST auto-gen target."
    )
    parser.add_argument(
        "--project-id", type=str, default=None,
        help="Project id (kebab-case) for HUMAN-CHECKLIST filename."
    )

    args = parser.parse_args()

    # XOR validation: exactly one of --score / --calibrated required.
    if args.score is None and args.calibrated is None:
        parser.error("either --score (legacy) or --calibrated (canonical) is required")
    if args.score is not None and args.calibrated is not None:
        parser.error("--score and --calibrated are mutually exclusive (use --calibrated for canonical mode)")

    if args.iteration > 3:
        print(f"🚨 ESCALATION REQUIRED — {args.iteration} iterations sin convergence")
        print(f"   Reportar al usuario con análisis dimensión-por-dimensión.")
        return 2

    # Legacy mode.
    if args.score is not None:
        if args.score < 0 or args.score > 10:
            print(f"❌ Invalid --score: {args.score}. Must be 0.0-10.0")
            return 1
        return _legacy_gate(args.score, args.stage, args.iteration)

    # Canonical dual-branch mode.
    if args.calibrated < 0 or args.calibrated > 10:
        print(f"❌ Invalid --calibrated: {args.calibrated}. Must be 0.0-10.0")
        return 1
    if args.perceptual is not None and (args.perceptual < 0 or args.perceptual > 10):
        print(f"❌ Invalid --perceptual: {args.perceptual}. Must be 0.0-10.0")
        return 1

    return _dual_branch_gate(
        args.calibrated,
        args.perceptual,
        args.stage,
        args.iteration,
        args.project_dir,
        args.project_id,
    )


if __name__ == "__main__":
    sys.exit(main())
