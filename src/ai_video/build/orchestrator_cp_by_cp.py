#!/usr/bin/env python3
"""
orchestrator-cp-by-cp.py — Script C: CP-by-CP state machine orchestrator.

Enforces structural gates between checkpoints (CP1..CP5) so V4+ launches can
NOT bypass the per-CP audit handoffs. The state machine progresses linearly
PENDING → ... → CP[N]_ENG → CP[N]_AUDIT → ... → READY → PUBLISHED.

Per CP, advancing to next state requires:
  1. Required precondition handoff file exists on disk
  2. Previous CP audit verdict is PASS (or NB with warning, FAIL halts)
  3. Per-CP timeout not exceeded
  4. Cost cap not exceeded
  5. Engineer prompt does NOT contain forbidden multi-CP/skip-audit phrases
  6. Engineer handoff scope claims single CP only

Overrides are explicit via --override-cpN-<flag> --reason "<≥10 chars>" and
are appended to master-flow-v2/ARCHITECTURAL-DECISIONS.md per YAML schema.

Dry-run mode (--dry-run) validates gate logic against the project filesystem
WITHOUT spawning any engineer agents. This is what the 17 tests use.

Exit codes:
  0  — orchestrator advanced to READY or completed dry-run gate check OK
  1  — HALT (gate failed, file missing, FAIL verdict, scope violation)
  2  — INVALID INPUT (bad CLI args, malformed override)
  3  — COST CAP exceeded
  4  — TIMEOUT exceeded

CLI examples:

    # Normal launch (would spawn engineer for each CP — implemented as stub)
    python orchestrator-cp-by-cp.py \\
        --project-id parque-acuatico-v4 \\
        --project-dir parque-acuatico-v4 \\
        --spec creative-specs/parque-acuatico-v4.yaml

    # With override (skip CP3 audit because iter 4 only regenerates CP4)
    python orchestrator-cp-by-cp.py \\
        --project-id parque-acuatico-v4 \\
        --project-dir parque-acuatico-v4 \\
        --spec creative-specs/parque-acuatico-v4.yaml \\
        --override-cp3-skip --reason "V4 iter 4 — only regenerating CP4 animation"

    # Dry-run mode (gate validation only, no spawn)
    python orchestrator-cp-by-cp.py \\
        --project-id parque-acuatico-v4 \\
        --project-dir parque-acuatico-v4 \\
        --spec creative-specs/parque-acuatico-v4.yaml \\
        --dry-run

    # Validate single engineer prompt (adversarial mode)
    python orchestrator-cp-by-cp.py \\
        --validate-engineer-prompt "execute CP1-CP5 todo de una"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


from ai_video.core.orchestrator_state import (  # noqa: E402
    OrchestratorState,
    LINEAR_FLOW,
    next_state,
    cp_id_from_state,
    previous_cp,
    parse_verdict,
    detect_multi_cp_prompt,
    assert_engineer_scope_single_cp,
    OverrideEntry,
    now_iso_utc,
    append_architectural_decision,
    parse_cost_from_file,
    HaltReason,
    GateHalt,
    VALID_AGENTS,
    VALID_CP_AFFECTED,
)


# -----------------------------------------------------------------------------
# Defaults
# -----------------------------------------------------------------------------

DEFAULT_TIMEOUT_PER_CP_MIN = 50
MAX_TIMEOUT_PER_CP_MIN = 120
# Cost cap default raised 2026-05-22 per V4 user authorization. Default in code
# (not CLI flag) = structural enforcement that survives V5/V6/future videos.
# Override at invocation via --cost-cap-usd if user authorizes mid-run.
# Recommended ALERT trigger at $6 (75% of cap) for early warning.
DEFAULT_COST_CAP_USD = 8.0


# Default ARCHITECTURAL-DECISIONS.md path (relative to repo root if available)
def default_decisions_path() -> Path:
    # Repo skills dir first, then walk up from cwd (legacy layouts).
    from ai_video.errors import ConfigError
    from ai_video.paths import skills_dir

    try:
        canonical = skills_dir() / "creative-director" / "master-flow-v2" / "ARCHITECTURAL-DECISIONS.md"
        if canonical.exists():
            return canonical
    except ConfigError:
        pass
    here = Path.cwd()
    for parent in [here] + list(here.parents):
        candidate = (
            parent
            / ".claude"
            / "skills"
            / "creative-director"
            / "master-flow-v2"
            / "ARCHITECTURAL-DECISIONS.md"
        )
        if candidate.exists():
            return candidate
        candidate2 = (
            parent
            / "creative-director"
            / "master-flow-v2"
            / "ARCHITECTURAL-DECISIONS.md"
        )
        if candidate2.exists():
            return candidate2
    # Fallback: relative to cwd
    return Path("master-flow-v2/ARCHITECTURAL-DECISIONS.md")


# -----------------------------------------------------------------------------
# Override flag parsing
# -----------------------------------------------------------------------------

# Known override flag names → (cp_affected, override_flag_label, verdict_bypassed)
KNOWN_OVERRIDE_FLAGS = {
    "override-cp1-skip": ("CP1", "skip-cp1-audit", None),
    "override-cp2-skip": ("CP2", "skip-cp2-audit", None),
    "override-cp3-skip": ("CP3", "skip-cp3-audit", None),
    "override-cp4-skip": ("CP4", "skip-cp4-audit", None),
    "override-cp5-skip": ("CP5", "skip-cp5-audit", None),
    "override-cp1-force-pass": ("CP1", "force-pass-cp1-fail", "FAIL"),
    "override-cp2-force-pass": ("CP2", "force-pass-cp2-fail", "FAIL"),
    "override-cp3-force-pass": ("CP3", "force-pass-cp3-fail", "FAIL"),
    "override-cp4-force-pass": ("CP4", "force-pass-cp4-fail", "FAIL"),
    "override-cp5-force-pass": ("CP5", "force-pass-cp5-fail", "FAIL"),
    "override-cost-cap-bypass": ("GLOBAL", "cost-cap-bypass", None),
    "override-timeout-bypass": ("GLOBAL", "timeout-bypass", None),
    # NEW 2026-05-22 — canonical floor enforcement at CP5 (audit-against-referent.py)
    "override-cp5-canonical-floor": ("CP5", "canonical-floor-bypass", None),
}


@dataclass
class ParsedOverride:
    flag_name: str  # e.g. "override-cp3-skip"
    cp_affected: str  # e.g. "CP3"
    override_flag_label: str  # e.g. "skip-cp3-audit"
    reason: str
    verdict_bypassed: Optional[str] = None


def parse_overrides_from_args(argv: list[str]) -> tuple[list[ParsedOverride], list[str], Optional[str]]:
    """
    Extract --override-XXX flags + --reason from argv. Returns:
      (overrides_list, remaining_argv, error_message_or_None)

    Each override is of form `--override-<name>` and must be followed (in some
    order) by `--reason "<≥10 chars>"`. We support EITHER:
      --override-cp3-skip --reason "explanation"
    or repeated pairs via `--override-name=value` style.

    For multiple overrides in one invocation, each requires its OWN --reason
    paired by position. Simpler: one override per invocation in MVP.
    """
    overrides: list[ParsedOverride] = []
    remaining: list[str] = []
    i = 0
    pending_override: Optional[str] = None

    while i < len(argv):
        token = argv[i]
        if token.startswith("--override-"):
            # Strip the leading --
            name = token[2:]
            # Allow --override-name=reason form
            if "=" in name:
                # not supported with implicit reason; treat as flag with embedded value
                k, v = name.split("=", 1)
                if k not in KNOWN_OVERRIDE_FLAGS:
                    return [], [], f"Unknown override flag: --{k}"
                cp_aff, label, verdict_bypassed = KNOWN_OVERRIDE_FLAGS[k]
                overrides.append(
                    ParsedOverride(
                        flag_name=k,
                        cp_affected=cp_aff,
                        override_flag_label=label,
                        reason=v,
                        verdict_bypassed=verdict_bypassed,
                    )
                )
                i += 1
                continue

            if name not in KNOWN_OVERRIDE_FLAGS:
                return [], [], f"Unknown override flag: --{name}"
            if pending_override is not None:
                return (
                    [],
                    [],
                    f"Override --{pending_override} requires --reason before next --override",
                )
            pending_override = name
            i += 1
            continue

        if token == "--reason":
            if pending_override is None:
                # --reason without a pending override
                return [], [], "--reason given without preceding --override-* flag"
            if i + 1 >= len(argv):
                return [], [], "--reason requires a value"
            reason_value = argv[i + 1]
            cp_aff, label, verdict_bypassed = KNOWN_OVERRIDE_FLAGS[pending_override]
            overrides.append(
                ParsedOverride(
                    flag_name=pending_override,
                    cp_affected=cp_aff,
                    override_flag_label=label,
                    reason=reason_value,
                    verdict_bypassed=verdict_bypassed,
                )
            )
            pending_override = None
            i += 2
            continue

        remaining.append(token)
        i += 1

    if pending_override is not None:
        return (
            [],
            [],
            f"Override --{pending_override} requires --reason \"<≥10 chars>\"",
        )

    return overrides, remaining, None


# -----------------------------------------------------------------------------
# Gate checks
# -----------------------------------------------------------------------------


@dataclass
class GateContext:
    project_id: str
    project_dir: Path
    spec_path: Path
    decisions_path: Path
    timeout_per_cp_min: int
    cost_cap_usd: float
    cost_log_path: Optional[Path]
    overrides: list[ParsedOverride]
    dry_run: bool = False
    cp_start_time: Optional[float] = None
    halts: list[HaltReason] = None
    warnings: list[str] = None
    architectural_log: list[OverrideEntry] = None
    consumed_overrides: set = None  # tracks id(ParsedOverride) already logged in this orchestrator run

    def __post_init__(self):
        if self.halts is None:
            self.halts = []
        if self.warnings is None:
            self.warnings = []
        if self.architectural_log is None:
            self.architectural_log = []
        if self.consumed_overrides is None:
            self.consumed_overrides = set()

    def find_override(self, cp_affected: str, flag_substr: str) -> Optional[ParsedOverride]:
        """Find an override matching cp + flag substring (e.g. 'skip', 'force-pass')."""
        for o in self.overrides:
            if o.cp_affected != cp_affected:
                continue
            if flag_substr.lower() in o.override_flag_label.lower():
                return o
            if flag_substr.lower() in o.flag_name.lower():
                return o
        return None

    def find_global_override(self, flag_substr: str) -> Optional[ParsedOverride]:
        for o in self.overrides:
            if o.cp_affected != "GLOBAL":
                continue
            if flag_substr.lower() in o.override_flag_label.lower():
                return o
            if flag_substr.lower() in o.flag_name.lower():
                return o
        return None


def gate_check_handoff_exists(ctx: GateContext, cp_id: str) -> None:
    """Precondition 1: previous CP handoff exists."""
    prev = previous_cp(cp_id)
    if prev is None:
        # CP1 has no predecessor handoff
        return

    handoff_path = ctx.project_dir / f"{prev}-handoff.md"
    if handoff_path.exists():
        return

    # Also accept POST-AUDIT-handoff name variant
    alt_path = ctx.project_dir / f"{prev}-POST-AUDIT-handoff.md"
    if alt_path.exists():
        return

    # Check for skip override
    o = ctx.find_override(prev, "skip")
    if o is not None:
        entry = _override_to_entry(o, ctx)
        if entry is not None:
            ctx.architectural_log.append(entry)
        ctx.warnings.append(
            f"OVERRIDE: --{o.flag_name} bypassed handoff requirement for {prev}"
        )
        return

    raise GateHalt(
        HaltReason(
            "MISSING_HANDOFF",
            f"REQUIRED FILE MISSING: {handoff_path} (no {alt_path.name} either). "
            f"Cannot advance to {cp_id} without {prev} handoff.",
        )
    )


def gate_check_verdict(ctx: GateContext, cp_id: str) -> None:
    """Precondition 2: previous CP audit verdict PASS (NB warning, FAIL halt)."""
    prev = previous_cp(cp_id)
    if prev is None:
        return

    verdict_path = ctx.project_dir / f"{prev}-AUDIT-verdict.md"
    if not verdict_path.exists():
        # Check skip override
        o = ctx.find_override(prev, "skip")
        if o is not None:
            entry = _override_to_entry(o, ctx)
            if entry is not None:
                ctx.architectural_log.append(entry)
            ctx.warnings.append(
                f"OVERRIDE: --{o.flag_name} bypassed audit verdict requirement for {prev}"
            )
            return
        raise GateHalt(
            HaltReason(
                "MISSING_VERDICT",
                f"REQUIRED FILE MISSING: {verdict_path}. "
                f"Cannot advance to {cp_id} without {prev} audit verdict.",
            )
        )

    verdict = parse_verdict(verdict_path)
    if verdict == "PASS":
        return
    if verdict == "NB":
        ctx.warnings.append(
            f"PREVIOUS CP VERDICT NB — {prev} passed conditionally, continuing with warning"
        )
        return
    if verdict in ("FAIL", "ESCALATE"):
        # Check force-pass override
        o = ctx.find_override(prev, "force-pass")
        if o is not None:
            o.verdict_bypassed = verdict
            entry = _override_to_entry(o, ctx)
            if entry is not None:
                ctx.architectural_log.append(entry)
            ctx.warnings.append(
                f"OVERRIDE: --{o.flag_name} bypassed {verdict} verdict for {prev}"
            )
            return
        raise GateHalt(
            HaltReason(
                "VERDICT_FAIL",
                f"PREVIOUS CP VERDICT {verdict}: {verdict_path}. "
                f"Cannot advance to {cp_id}. To bypass: "
                f"--override-{prev.lower()}-force-pass --reason \"<≥10 chars>\"",
            )
        )

    # UNKNOWN / MISSING after exists — treat as halt
    raise GateHalt(
        HaltReason(
            "VERDICT_UNPARSEABLE",
            f"Could not parse verdict from {verdict_path} (found '{verdict}'). "
            f"Expected one of PASS/NB/FAIL/ESCALATE.",
        )
    )


def gate_check_timeout(ctx: GateContext) -> None:
    """Precondition 3: per-CP timeout not exceeded."""
    if ctx.cp_start_time is None:
        return
    elapsed_sec = time.time() - ctx.cp_start_time
    elapsed_min = elapsed_sec / 60.0
    if elapsed_min > ctx.timeout_per_cp_min:
        o = ctx.find_global_override("timeout")
        if o is not None:
            entry = _override_to_entry(o, ctx)
            if entry is not None:
                ctx.architectural_log.append(entry)
            ctx.warnings.append(
                f"OVERRIDE: --{o.flag_name} bypassed timeout cap ({elapsed_min:.1f} min)"
            )
            return
        raise GateHalt(
            HaltReason(
                "TIMEOUT_EXCEEDED",
                f"TIMEOUT EXCEEDED: {elapsed_min:.1f} min > {ctx.timeout_per_cp_min} min. "
                f"To bypass: --override-timeout-bypass --reason \"<≥10 chars>\"",
            )
        )


def gate_check_cost(ctx: GateContext) -> None:
    """Precondition 4: cost cap not exceeded."""
    if ctx.cost_log_path is None:
        return
    cost = parse_cost_from_file(ctx.cost_log_path)
    if cost > ctx.cost_cap_usd:
        o = ctx.find_global_override("cost")
        if o is not None:
            entry = _override_to_entry(o, ctx)
            if entry is not None:
                ctx.architectural_log.append(entry)
            ctx.warnings.append(
                f"OVERRIDE: --{o.flag_name} bypassed cost cap (${cost:.2f})"
            )
            return
        raise GateHalt(
            HaltReason(
                "COST_CAP_EXCEEDED",
                f"COST CAP EXCEEDED: ${cost:.2f} > ${ctx.cost_cap_usd:.2f}. "
                f"To bypass: --override-cost-cap-bypass --reason \"<≥10 chars>\"",
            )
        )


def gate_check_engineer_prompt(prompt: str) -> None:
    """Precondition 5: engineer prompt is single-CP scoped (no forbidden phrases)."""
    matched = detect_multi_cp_prompt(prompt)
    if matched is not None:
        raise GateHalt(
            HaltReason(
                "ADVERSARIAL_PROMPT",
                f"Forbidden phrase detected in engineer prompt: '{matched}'. "
                f"Engineer scope MUST be single CP only. Refusing spawn.",
            )
        )


def gate_check_engineer_scope_metadata(handoff_text: str, expected_cp: str) -> None:
    """Precondition 6: engineer handoff scope is single CP only."""
    err = assert_engineer_scope_single_cp(handoff_text, expected_cp)
    if err is not None:
        raise GateHalt(
            HaltReason(
                "SCOPE_VIOLATION",
                f"Engineer scope check FAILED for {expected_cp}: {err}",
            )
        )


def gate_check_canonical_floor_cp5(ctx: GateContext) -> None:
    """
    Precondition 7 (CP5-only, NEW 2026-05-22): canonical technical floor enforced.

    Runs audit-against-referent.py on renders/draft.mp4. Promotes the script from
    "sanity check" (Hard Rule #1 prior wording) to gate-blocking enforcement at CP5
    final. Exit 1 from the script = HALT. Override path:
        --override-cp5-canonical-floor --reason "<≥10 chars>"

    Caso disparador: 2026-05-22 Tomás canonical-quality-gap question — V4 system
    enforced "SPEC compliance" via Script B but had NO script-callable canonical
    floor enforcement (audit-against-referent existed but wasn't wired). This
    closes that gap structurally for CP5.

    What the underlying script measures (per audit-against-referent.py docstring):
      - pace.wpm_total (sweet spot ~153-180)
      - audio.lufs_integrated (-14 ±0.5)
      - pacing.cuts_per_min (canonical band)
      - pace.coverage_pct (≥70%)
    PASS = ≥85% critical metrics in p25-p75 bands vs F1 canonical referent profile.
    """
    if ctx.dry_run:
        # Skip in dry-run — script requires real video file at renders/draft.mp4
        return

    render_path = ctx.project_dir / "renders" / "draft.mp4"
    if not render_path.exists():
        raise GateHalt(
            HaltReason(
                "MISSING_RENDER",
                f"REQUIRED FILE MISSING: {render_path}. "
                f"CP5 canonical floor needs final render before audit.",
            )
        )

    # Run the packaged audit with the *current* interpreter (the old code shelled out to
    # whatever `python3` was first on PATH, which may lack the project's dependencies).
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "ai_video.audits.audit_against_referent", "--video", str(render_path)],
        capture_output=True, text=True, cwd=str(ctx.project_dir), timeout=1800,
    )

    # Exit code semantics from audit-against-referent.py:
    #   0 = ≥85% critical metrics in band (PASS)
    #   1 = <85% (FAIL — gate-blocking)
    #   2 = missing data / can't measure (BLOCKED)
    if result.returncode == 0:
        return  # canonical floor PASS, proceed

    # FAIL or BLOCKED — check for override
    o = ctx.find_override("CP5", "canonical-floor")
    if o is not None:
        entry = _override_to_entry(o, ctx)
        if entry is not None:
            ctx.architectural_log.append(entry)
        ctx.warnings.append(
            f"OVERRIDE: --{o.flag_name} bypassed canonical floor "
            f"(audit-against-referent exit {result.returncode})"
        )
        return

    raise GateHalt(
        HaltReason(
            "CANONICAL_FLOOR_FAIL",
            f"audit-against-referent.py exit {result.returncode} (FAIL or BLOCKED). "
            f"CP5 cannot advance — render does NOT meet canonical technical floor. "
            f"To bypass: --override-cp5-canonical-floor --reason \"<≥10 chars>\". "
            f"Output:\n{result.stdout}\n{result.stderr}",
        )
    )


def _override_to_entry(o: ParsedOverride, ctx: GateContext) -> Optional[OverrideEntry]:
    # Dedup guard: if this ParsedOverride was already logged in this orchestrator
    # run, return None so caller skips re-append.
    if id(o) in ctx.consumed_overrides:
        return None
    ctx.consumed_overrides.add(id(o))
    return OverrideEntry(
        timestamp=now_iso_utc(),
        override_flag=o.override_flag_label,
        cp_affected=o.cp_affected,
        reason=o.reason,
        agent="user",  # CLI invocation = user-authorized
        verdict_bypassed=o.verdict_bypassed,
        related_files=[],
        notes=f"Orchestrator --{o.flag_name} for project {ctx.project_id}",
    )


# -----------------------------------------------------------------------------
# Engineer spawn (stub — actually orchestrator does not spawn agents in MVP)
# -----------------------------------------------------------------------------


def spawn_engineer(ctx: GateContext, cp_id: str) -> dict:
    """
    Spawn engineer agent for given CP.

    In MVP this is a STUB that:
      - Builds the engineer prompt
      - Validates the prompt for forbidden phrases (raise GateHalt if any)
      - In dry-run mode: returns a dict with the prompt for inspection
      - In normal mode: would invoke Task agent via Claude SDK (NOT in MVP)

    Returns dict with status + prompt + cp_id.
    """
    prompt = (
        f"Engineer scope: {cp_id} ONLY. Do NOT chain CPs across {cp_id}. "
        f"Read SPEC at {ctx.spec_path}. "
        f"Emit {cp_id}-handoff.md in project dir {ctx.project_dir}. "
        f"Stop after handoff written. Single-CP execution only. "
        f"Audit gate must run after. No verdict bypass."
    )

    # Defensive check: ensure the prompt we generated does not accidentally
    # match a forbidden phrase. (It shouldn't but be safe.)
    gate_check_engineer_prompt(prompt)

    if ctx.dry_run:
        return {
            "status": "dry-run",
            "cp_id": cp_id,
            "prompt": prompt,
            "spawned": False,
        }

    # In production this would invoke Task SDK with the prompt above
    # We do NOT actually spawn here — Script C orchestrates via filesystem,
    # actual agent spawning happens in the wrapping shell/Claude session.
    return {
        "status": "ready-to-spawn",
        "cp_id": cp_id,
        "prompt": prompt,
        "spawned": False,
    }


# -----------------------------------------------------------------------------
# Main state machine driver
# -----------------------------------------------------------------------------


def run_orchestrator(ctx: GateContext, start_state: OrchestratorState) -> tuple[OrchestratorState, int]:
    """
    Run state machine from start_state. Returns (final_state, exit_code).

    In dry-run mode, runs gate checks for each transition WITHOUT spawning
    engineers and WITHOUT requiring engineer handoffs that haven't been
    created yet — but still requires precondition files for past CPs.
    """
    state = start_state
    iter_count = 0
    max_iter = 50  # safety bound

    while iter_count < max_iter:
        iter_count += 1
        nxt = next_state(state)
        if nxt is None:
            break

        # Reset per-CP timer when entering an ENG state
        if state.value.endswith("_ENG"):
            ctx.cp_start_time = time.time()

        # Try to advance
        try:
            if nxt.value.endswith("_ENG"):
                cp = cp_id_from_state(nxt)
                if cp is not None:
                    gate_check_handoff_exists(ctx, cp)
                    gate_check_verdict(ctx, cp)
                    gate_check_timeout(ctx)
                    gate_check_cost(ctx)
                    spawn_engineer(ctx, cp)
            elif nxt.value.endswith("_AUDIT"):
                # Audit step requires engineer handoff produced
                cp = cp_id_from_state(nxt)
                if cp is not None:
                    handoff_path = ctx.project_dir / f"{cp}-handoff.md"
                    alt_path = ctx.project_dir / f"{cp}-POST-AUDIT-handoff.md"
                    if not handoff_path.exists() and not alt_path.exists():
                        if not ctx.dry_run:
                            raise GateHalt(
                                HaltReason(
                                    "MISSING_ENG_HANDOFF",
                                    f"Engineer did NOT emit {handoff_path}. "
                                    f"Cannot transition to {nxt.value}.",
                                )
                            )
                        # In dry-run mode, missing future handoffs is expected;
                        # we stop here and report state reached.
                        return state, 0

                    # Validate scope metadata
                    if handoff_path.exists():
                        text = handoff_path.read_text(encoding="utf-8", errors="replace")
                        gate_check_engineer_scope_metadata(text, cp)

                    # CP5 final audit step: enforce canonical technical floor
                    # via audit-against-referent.py (gate-blocking, exit 1 = HALT)
                    # Wired 2026-05-22 to close canonical-quality-gap.
                    if cp == "CP5":
                        gate_check_canonical_floor_cp5(ctx)
        except GateHalt as h:
            ctx.halts.append(h.reason)
            return OrchestratorState.HALTED, 1

        state = nxt

        if state == OrchestratorState.PUBLISHED or state == OrchestratorState.READY:
            return state, 0

    return state, 0


def flush_architectural_log(ctx: GateContext) -> None:
    """Append all logged overrides to ARCHITECTURAL-DECISIONS.md."""
    for entry in ctx.architectural_log:
        append_architectural_decision(ctx.decisions_path, entry)
        print(
            f"⚠️  ARCHITECTURAL OVERRIDE applied: {entry.override_flag} | "
            f"CP: {entry.cp_affected} | Reason: {entry.reason}"
        )
        print(f"   Logged to {ctx.decisions_path}")


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Script C — CP-by-CP orchestrator state machine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--project-id", help="Project identifier (e.g. parque-acuatico-v4)")
    p.add_argument(
        "--project-dir",
        help="Project directory containing CP[N]-handoff.md + CP[N]-AUDIT-verdict.md",
    )
    p.add_argument("--spec", help="Path to creative SPEC YAML file")
    p.add_argument(
        "--start-state",
        default="USER_APPROVE",
        choices=[s.value for s in LINEAR_FLOW],
        help="State to start from (default: USER_APPROVE, i.e. just before CP1).",
    )
    p.add_argument(
        "--timeout-per-cp-min",
        type=int,
        default=DEFAULT_TIMEOUT_PER_CP_MIN,
        help=f"Max minutes per CP (default {DEFAULT_TIMEOUT_PER_CP_MIN}, max {MAX_TIMEOUT_PER_CP_MIN}).",
    )
    p.add_argument(
        "--cost-cap-usd",
        type=float,
        default=DEFAULT_COST_CAP_USD,
        help=f"Max USD cost per video (default ${DEFAULT_COST_CAP_USD}).",
    )
    p.add_argument(
        "--cost-log",
        help="Path to running cost log (one float USD per line, or 'total_usd: X').",
    )
    p.add_argument(
        "--decisions-path",
        help="Path to ARCHITECTURAL-DECISIONS.md (default: auto-detect under .claude/skills/creative-director/master-flow-v2/).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate gates without spawning engineers.",
    )
    p.add_argument(
        "--validate-engineer-prompt",
        help="Adversarial mode: pass a candidate engineer prompt to validate. "
        "Exits 0 if clean, 1 if forbidden phrase detected.",
    )
    p.add_argument(
        "--validate-handoff-scope",
        help="Adversarial mode: pass path to handoff file to validate scope metadata.",
    )
    p.add_argument(
        "--validate-handoff-cp",
        help="Expected CP for handoff scope validation (e.g. CP2).",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # First extract overrides (custom --override-* flags not in argparse)
    overrides, remaining, override_err = parse_overrides_from_args(argv)
    if override_err is not None:
        print(f"❌ INVALID OVERRIDE: {override_err}", file=sys.stderr)
        return 2

    # Validate override reasons (≥10 chars)
    for o in overrides:
        if not o.reason or len(o.reason.strip()) < 10:
            print(
                f"❌ INVALID OVERRIDE: --{o.flag_name} requires --reason \"<≥10 chars>\". "
                f"Got: '{o.reason}' (length {len(o.reason.strip())})",
                file=sys.stderr,
            )
            return 2

    parser = build_parser()
    args = parser.parse_args(remaining)

    # Adversarial validation modes (single-shot, no project required)
    if args.validate_engineer_prompt is not None:
        matched = detect_multi_cp_prompt(args.validate_engineer_prompt)
        if matched is not None:
            print(
                f"❌ REFUSE: Forbidden phrase '{matched}' in engineer prompt.",
                file=sys.stderr,
            )
            return 1
        print("✅ Engineer prompt clean (no forbidden phrases).")
        return 0

    if args.validate_handoff_scope is not None:
        if not args.validate_handoff_cp:
            print(
                "❌ --validate-handoff-scope requires --validate-handoff-cp <CP>.",
                file=sys.stderr,
            )
            return 2
        handoff_file = Path(args.validate_handoff_scope)
        if not handoff_file.exists():
            print(f"❌ Handoff file missing: {handoff_file}", file=sys.stderr)
            return 1
        text = handoff_file.read_text(encoding="utf-8", errors="replace")
        err = assert_engineer_scope_single_cp(text, args.validate_handoff_cp)
        if err is not None:
            print(f"❌ SCOPE VIOLATION: {err}", file=sys.stderr)
            return 1
        print(f"✅ Handoff scope matches {args.validate_handoff_cp}.")
        return 0

    # Normal orchestrator mode requires project + spec
    if not args.project_id or not args.project_dir or not args.spec:
        parser.error("--project-id, --project-dir, and --spec are required (unless using --validate-* modes)")

    # Validate timeout
    if args.timeout_per_cp_min <= 0 or args.timeout_per_cp_min > MAX_TIMEOUT_PER_CP_MIN:
        print(
            f"❌ INVALID --timeout-per-cp-min: {args.timeout_per_cp_min} "
            f"(must be 1-{MAX_TIMEOUT_PER_CP_MIN})",
            file=sys.stderr,
        )
        return 2

    if args.cost_cap_usd < 0:
        print(f"❌ INVALID --cost-cap-usd: {args.cost_cap_usd}", file=sys.stderr)
        return 2

    project_dir = Path(args.project_dir)
    spec_path = Path(args.spec)
    decisions_path = (
        Path(args.decisions_path) if args.decisions_path else default_decisions_path()
    )
    cost_log_path = Path(args.cost_log) if args.cost_log else None

    if not args.dry_run and not project_dir.exists():
        print(f"❌ Project directory missing: {project_dir}", file=sys.stderr)
        return 1

    ctx = GateContext(
        project_id=args.project_id,
        project_dir=project_dir,
        spec_path=spec_path,
        decisions_path=decisions_path,
        timeout_per_cp_min=args.timeout_per_cp_min,
        cost_cap_usd=args.cost_cap_usd,
        cost_log_path=cost_log_path,
        overrides=overrides,
        dry_run=args.dry_run,
    )

    start_state = OrchestratorState(args.start_state)

    print(f"🚀 Orchestrator starting: project={args.project_id} from state={start_state.value}")
    print(f"   spec={spec_path}")
    print(f"   project_dir={project_dir}")
    print(f"   dry_run={args.dry_run}")
    if overrides:
        print(f"   overrides={len(overrides)}:")
        for o in overrides:
            print(f"     --{o.flag_name} (cp={o.cp_affected}) reason=\"{o.reason}\"")
    print()

    final_state, exit_code = run_orchestrator(ctx, start_state)

    # Flush architectural log AFTER state machine completes (even on halt,
    # we still write the log entries for overrides that WERE consumed).
    try:
        flush_architectural_log(ctx)
    except Exception as e:
        print(f"⚠️  Failed to write architectural decisions log: {e}", file=sys.stderr)

    print()
    print(f"📊 Orchestrator final state: {final_state.value} (exit={exit_code})")
    if ctx.warnings:
        print(f"   Warnings: {len(ctx.warnings)}")
        for w in ctx.warnings:
            print(f"     ⚠️  {w}")
    if ctx.halts:
        print(f"   Halts: {len(ctx.halts)}")
        for h in ctx.halts:
            print(f"     ⛔ {h}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
