"""
orchestrator_state.py — State machine helpers for Script C (orchestrator-cp-by-cp.py).

Provides:
  - State enum + valid transitions
  - Verdict parsing (PASS/NB/FAIL/ESCALATE)
  - Architectural decisions YAML append (schema-safe)
  - Adversarial multi-CP prompt detection
  - Cost/timeout tracking helpers

NO API calls, NO subprocess. Pure Python state + filesystem ops.
"""

from __future__ import annotations

import datetime
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# -----------------------------------------------------------------------------
# State enum + transitions
# -----------------------------------------------------------------------------


class OrchestratorState(str, Enum):  # noqa: UP042 - str mixin kept for JSON/equality back-compat
    PENDING = "PENDING"
    SPEC_GEN = "SPEC_GEN"
    SPEC_AUDIT = "SPEC_AUDIT"
    USER_APPROVE = "USER_APPROVE"
    CP1_ENG = "CP1_ENG"
    CP1_AUDIT = "CP1_AUDIT"
    CP2_ENG = "CP2_ENG"
    CP2_AUDIT = "CP2_AUDIT"
    CP3_ENG = "CP3_ENG"
    CP3_AUDIT = "CP3_AUDIT"
    CP4_ENG = "CP4_ENG"
    CP4_AUDIT = "CP4_AUDIT"
    CP5_ENG = "CP5_ENG"
    CP5_AUDIT = "CP5_AUDIT"
    READY = "READY"
    PUBLISHED = "PUBLISHED"
    HALTED = "HALTED"


# Ordered linear progression. Each transition requires precondition.
LINEAR_FLOW = [
    OrchestratorState.PENDING,
    OrchestratorState.SPEC_GEN,
    OrchestratorState.SPEC_AUDIT,
    OrchestratorState.USER_APPROVE,
    OrchestratorState.CP1_ENG,
    OrchestratorState.CP1_AUDIT,
    OrchestratorState.CP2_ENG,
    OrchestratorState.CP2_AUDIT,
    OrchestratorState.CP3_ENG,
    OrchestratorState.CP3_AUDIT,
    OrchestratorState.CP4_ENG,
    OrchestratorState.CP4_AUDIT,
    OrchestratorState.CP5_ENG,
    OrchestratorState.CP5_AUDIT,
    OrchestratorState.READY,
    OrchestratorState.PUBLISHED,
]


def next_state(current: OrchestratorState) -> OrchestratorState | None:
    """Return next state in linear flow, or None if terminal."""
    if current == OrchestratorState.HALTED:
        return None
    try:
        idx = LINEAR_FLOW.index(current)
    except ValueError:
        return None
    if idx + 1 >= len(LINEAR_FLOW):
        return None
    return LINEAR_FLOW[idx + 1]


def cp_id_from_state(state: OrchestratorState) -> str | None:
    """Return 'CP1'..'CP5' if state is a CP_ENG/CP_AUDIT, else None."""
    name = state.value
    m = re.match(r"^(CP[1-5])_(ENG|AUDIT)$", name)
    if not m:
        return None
    return m.group(1)


def previous_cp(cp: str) -> str | None:
    """Return prior CP id, e.g. 'CP3' -> 'CP2'. 'CP1' returns None."""
    m = re.match(r"^CP([1-5])$", cp)
    if not m:
        return None
    n = int(m.group(1))
    if n == 1:
        return None
    return f"CP{n - 1}"


# -----------------------------------------------------------------------------
# Verdict parsing
# -----------------------------------------------------------------------------


VALID_VERDICTS = {"PASS", "NB", "FAIL", "ESCALATE"}


def parse_verdict(verdict_path: Path) -> str:
    """
    Parse verdict from `<project>/CP[N]-AUDIT-verdict.md`.

    Looks for a line matching `verdict: <VAL>` or `Verdict: <VAL>` or
    `**Verdict**: <VAL>` (case-insensitive). VAL must be in VALID_VERDICTS.

    Returns 'UNKNOWN' if no verdict line found.
    """
    if not verdict_path.exists():
        return "MISSING"
    try:
        text = verdict_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "MISSING"

    # Canonical verdicts + el vocabulario emoji/GO-NO-GO que MANDA AUDITOR-PROTOCOL § 5.
    # Mapeo: GO -> PASS · NO-GO -> FAIL · ESCALAR -> ESCALATE.
    vocab = r"(PASS|NB|FAIL|ESCALATE|ESCALAR|NO-?GO|GO)"
    patterns = [
        rf"(?im)^\s*\**\s*(?:verdict|veredicto)\s*\**\s*[:=]\s*\**\s*(?:🟢|🟡|🔴|⛔)?\s*{vocab}\b",
        rf"(?im)^\s*[-*|]\s*(?:🟢|🟡|🔴|⛔)?\s*(?:verdict|veredicto)\s*[:=]\s*{vocab}\b",
        rf"(?im)^\s*(?:🟢|🟡|🔴|⛔)\s*{vocab}\b",
    ]
    norm = {"GO": "PASS", "NOGO": "FAIL", "NO-GO": "FAIL", "ESCALAR": "ESCALATE"}
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            raw = m.group(1).upper()
            return norm.get(raw, norm.get(raw.replace(" ", ""), raw))
    return "UNKNOWN"


# -----------------------------------------------------------------------------
# Adversarial prompt detection
# -----------------------------------------------------------------------------


FORBIDDEN_PHRASES = [
    "execute cp1-cp5",
    "execute cp1 cp5",
    "cp1 through cp5",
    "cp1-cp5",
    "all cps",
    "autonomous all",
    "skip audit",
    "skip cp",
    "force pass",
    "force-pass",
    "bypass gate",
    "bypass-gate",
    "todo de una",
    "end-to-end",
    "end to end",
    "multi-cp",
    "multi cp",
    # ── ES — el sistema es spanish-neutral; estos eran el bypass confirmado ──
    "de corrido",
    "sin parar",
    "de un tiron",
    "de un tirón",
    "de un saque",
    "punta a punta",
    "de punta a punta",
    "todos los checkpoints",
    "todos los cp",
    "todos los cps",
    "autónomo",
    "autonomo",
    "corré todo",
    "corre todo",
    "hazlo solo",
    "sin auditar",
    "salta el audit",
    "saltea el audit",
]


def detect_multi_cp_prompt(engineer_prompt: str) -> str | None:
    """
    Check engineer prompt for forbidden multi-CP / skip-audit / force-pass phrases.

    Returns the matched phrase (string) if found, else None.
    Case-insensitive substring match.
    """
    if not engineer_prompt:
        return None
    lower = engineer_prompt.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower:
            return phrase
    return None


def assert_engineer_scope_single_cp(handoff_text: str, expected_cp: str) -> str | None:
    """
    Verify engineer handoff scope is single CP only.

    Look for `scope: CP[N] only` (case-insensitive) OR `scope: CP[N]`.
    If mentions multiple CPs in scope line (e.g. "scope: CP1-CP5"), return error.

    Returns None on success, error string on failure.
    """
    if not handoff_text:
        return "Handoff text empty"

    # Look for a scope declaration line
    scope_match = re.search(
        r"(?im)^\s*[-*#]*\s*(?:engineer\s+)?scope\s*[:=]\s*(.+)$", handoff_text
    )
    if not scope_match:
        # No explicit scope declaration. Accept but warn (legacy handoffs).
        return None

    scope_value = scope_match.group(1).strip()
    scope_lower = scope_value.lower()

    # If contains forbidden multi-CP phrases in scope line, fail
    multi_cp_in_scope = re.search(r"cp\s*[1-5]\s*[-–to ]+\s*cp\s*[1-5]", scope_lower)
    if multi_cp_in_scope:
        return f"Engineer scope contains multi-CP range: '{scope_value}'"

    # Count distinct CP mentions in scope line
    cps_mentioned = set(re.findall(r"cp\s*([1-5])", scope_lower))
    if len(cps_mentioned) > 1:
        return f"Engineer scope mentions multiple CPs: {sorted(cps_mentioned)}"

    # If single CP mentioned, verify it matches expected
    if cps_mentioned:
        only_cp = f"CP{next(iter(cps_mentioned))}"
        if only_cp.upper() != expected_cp.upper():
            return f"Engineer scope CP mismatch: declared {only_cp}, expected {expected_cp}"

    return None


# -----------------------------------------------------------------------------
# ARCHITECTURAL-DECISIONS.md append (YAML schema)
# -----------------------------------------------------------------------------


VALID_AGENTS = {"user", "auditor", "engineer", "architect", "orchestrator"}
VALID_CP_AFFECTED = {"CP1", "CP2", "CP3", "CP4", "CP5", "GLOBAL"}


@dataclass
class OverrideEntry:
    timestamp: str
    override_flag: str
    cp_affected: str
    reason: str
    agent: str
    verdict_bypassed: str | None = None
    related_files: list = field(default_factory=list)
    notes: str | None = None

    def validate(self) -> str | None:
        # ISO8601 simple sanity
        if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$", self.timestamp):
            return f"Invalid timestamp ISO8601: {self.timestamp}"
        if not self.override_flag or not isinstance(self.override_flag, str):
            return "override_flag missing"
        if self.cp_affected not in VALID_CP_AFFECTED:
            return f"cp_affected must be one of {VALID_CP_AFFECTED}, got {self.cp_affected}"
        if not self.reason or len(self.reason.strip()) < 10:
            return f"reason must be ≥10 chars non-whitespace (got {len(self.reason.strip())})"
        if self.agent not in VALID_AGENTS:
            return f"agent must be one of {VALID_AGENTS}, got {self.agent}"
        return None

    def to_yaml_block(self) -> str:
        lines = [f"- timestamp: {self.timestamp}"]
        lines.append(f"  override_flag: {_yaml_str(self.override_flag)}")
        lines.append(f"  cp_affected: {self.cp_affected}")
        lines.append(f"  reason: {_yaml_str(self.reason)}")
        lines.append(f"  agent: {self.agent}")
        if self.verdict_bypassed is None:
            lines.append("  verdict_bypassed: null")
        else:
            lines.append(f"  verdict_bypassed: {_yaml_str(self.verdict_bypassed)}")
        if self.related_files:
            lines.append("  related_files:")
            for rf in self.related_files:
                if isinstance(rf, dict):
                    lines.append(f"    - path: {_yaml_str(rf.get('path', ''))}")
                    lines.append(f"      action: {_yaml_str(rf.get('action', ''))}")
                else:
                    lines.append(f"    - {_yaml_str(str(rf))}")
        else:
            lines.append("  related_files: []")
        if self.notes is None:
            lines.append("  notes: null")
        else:
            lines.append(f"  notes: {_yaml_str(self.notes)}")
        return "\n".join(lines)


def _yaml_str(s: str) -> str:
    """Quote string for YAML if it contains special chars."""
    if s is None:
        return "null"
    s = str(s)
    if re.search(r'[:#\[\]{}&*!|>%@`,\n"\'\\]', s) or s.strip() != s or not s:
        # Use double quotes with escape
        escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    return s


def now_iso_utc() -> str:
    return (
        datetime.datetime.now(datetime.UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def append_architectural_decision(
    decisions_path: Path, entry: OverrideEntry
) -> None:
    """
    Append YAML entry to ARCHITECTURAL-DECISIONS.md.

    Strategy: file is markdown with a `entries: []` line. We append entries
    AFTER the `entries: []` marker in the YAML block. If `entries: []` not
    present, append a new section at the end.

    Idempotent: never truncates existing content. ALWAYS appends.
    """
    err = entry.validate()
    if err:
        raise ValueError(f"Invalid override entry: {err}")

    if not decisions_path.exists():
        # Create with skeleton
        decisions_path.parent.mkdir(parents=True, exist_ok=True)
        decisions_path.write_text(
            "# ARCHITECTURAL-DECISIONS.md — Override + Decision Log\n\n"
            "```yaml\nentries: []\n```\n\n"
            "## Appended entries\n\n",
            encoding="utf-8",
        )

    block = entry.to_yaml_block()

    # Append as a fenced YAML block at the end
    appendix = (
        f"\n```yaml\n# Appended {entry.timestamp} by orchestrator (agent={entry.agent})\n"
        f"{block}\n```\n"
    )
    # Always write at the end — append-only
    with decisions_path.open("a", encoding="utf-8") as f:
        f.write(appendix)


# -----------------------------------------------------------------------------
# Gate halt reasons
# -----------------------------------------------------------------------------


@dataclass
class HaltReason:
    code: str
    message: str

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"


class GateHalt(Exception):
    def __init__(self, reason: HaltReason):
        super().__init__(str(reason))
        self.reason = reason


# -----------------------------------------------------------------------------
# Cost / timeout tracking
# -----------------------------------------------------------------------------


def parse_cost_from_file(cost_log_path: Path) -> float:
    """
    Parse cumulative cost USD from `cost_log_path`.
    Expected format: one float per line (USD), or `total_usd: <float>` line.
    Returns 0.0 if file missing.
    """
    if not cost_log_path.exists():
        return 0.0
    try:
        text = cost_log_path.read_text(encoding="utf-8")
    except OSError:
        return 0.0
    # Try `total_usd:` first
    m = re.search(r"(?im)^\s*total_usd\s*[:=]\s*([0-9]+\.?[0-9]*)\s*$", text)
    if m:
        return float(m.group(1))
    # Sum lines that parse as float
    total = 0.0
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            total += float(line)
        except ValueError:
            continue
    return total
