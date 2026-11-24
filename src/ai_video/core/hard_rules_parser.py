"""
hard_rules_parser.py — parse CLAUDE.md Hard Rules table into structured dicts.

Per CLAUDE.md Hard Rule #19 ("NEVER ESTIMATE, ALWAYS MEASURE") + Hard Rule #1
(dual quality gate thresholds): scripts MUST read thresholds from the canonical
Hard Rules table at runtime, NOT hardcoded constants that drift. This module is
the single-source helper for any downstream script (e.g., qa-gate.py) that needs
threshold introspection without parsing markdown itself.

Schema per rule:
    {
        "rule_id": int,                # e.g., 1, 23, 26 (NEVER 22 — empty slot)
        "text": str,                   # rule body (markdown formatting preserved)
        "severity": str,               # "critical" (⛔⛔) | "blocker" (⛔) | "standard"
        "authority_pointer": str,      # last column of table (doc refs)
    }

Hard Rule #22 = canonical empty slot per CLAUDE.md footnote (commit 48bd13e
2026-05-21 accidental skip, co-author Claude Opus 4.7). Parser skips
gracefully — Rule #22 NEVER appears in output.

Authority: CLAUDE.md Hard Rules table (lines vary, currently ~L171-L194 +
footnote at L196). Sub-Fase 3A 2026-05-23 codified this helper as Sprint M
defense in depth per Hard Rule #26 (tests adversariales obligatorios).
"""

from __future__ import annotations

import re
from pathlib import Path

# Matches a Hard Rules table row:
#   | <rule_id>( <emojis>)? | <text> | <authority_pointer> |
# Emoji column accepts ⛔ or ⛔⛔ (Unicode U+26D4). Other spaces tolerated.
_RULE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*(⛔+)?\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")

_SEVERITY_BY_EMOJI_COUNT = {
    0: "standard",
    1: "blocker",
    2: "critical",
    3: "critical",  # ⛔⛔⛔ treated as critical (no rule uses this currently)
}


def parse_hard_rules(claude_md_path: Path | str) -> list[dict]:
    """Parse CLAUDE.md Hard Rules table → list of rule dicts.

    Args:
        claude_md_path: path to the doc with the Hard Rules table
            (canonical: ``ai_video.paths.hard_rules_doc()``).

    Returns:
        list of dicts per schema in module docstring. Rule #22 is NEVER in output
        (canonical empty slot). Order matches table order.

    Raises:
        FileNotFoundError: if claude_md_path does not exist.
        ValueError: if no rules found (malformed CLAUDE.md or parser regex drift).
    """
    path = Path(claude_md_path)
    if not path.exists():
        raise FileNotFoundError(f"CLAUDE.md not found at {path}")

    rules: list[dict] = []
    in_hard_rules_section = False

    for line in path.read_text(encoding="utf-8").splitlines():
        # Section delimiter heuristic: Hard Rules table is preceded by
        # "Hard rules globales" heading. Reset on any "## " or "# " header
        # OTHER than the Hard Rules heading itself.
        if line.startswith("## ") or line.startswith("# "):
            in_hard_rules_section = "Hard rules globales" in line or "Hard Rules" in line
            continue

        if not in_hard_rules_section:
            continue

        match = _RULE_ROW_RE.match(line)
        if not match:
            continue

        rule_id_str, emoji_block, text, authority = match.groups()
        try:
            rule_id = int(rule_id_str)
        except ValueError:
            # Header row "| # | Regla | Doc canónico |" — # not numeric, skip.
            continue

        # Heuristic: skip the table separator row "| --- | --- | --- |".
        # The regex requires \d+ in column 1 so separators won't match anyway,
        # but defensive in case format drifts.
        if not text or text.startswith("---"):
            continue

        emoji_count = emoji_block.count("⛔") if emoji_block else 0
        severity = _SEVERITY_BY_EMOJI_COUNT.get(emoji_count, "critical")

        rules.append(
            {
                "rule_id": rule_id,
                "text": text.strip(),
                "severity": severity,
                "authority_pointer": authority.strip(),
            }
        )

    if not rules:
        raise ValueError(
            f"No Hard Rules parsed from {path}. Parser regex may be stale or section heading changed."
        )

    return rules


def get_rule(rules: list[dict], rule_id: int) -> dict | None:
    """Look up a rule by id. Returns None for missing (e.g., Rule #22 empty slot)."""
    for r in rules:
        if r["rule_id"] == rule_id:
            return r
    return None


def get_quality_threshold_calibrated(rules: list[dict]) -> float | None:
    """Extract calibrated quality threshold from Hard Rule #1.

    Current canonical threshold per Hard Rule #1 (updated 2026-05-21 PM late):
        gemini_calibrated_v4 ≥9.0

    Returns the numeric threshold (9.0) or None if Rule #1 missing/unparseable.
    Downstream scripts (qa-gate.py) use this for dynamic threshold lookup
    instead of hardcoded constants.
    """
    rule_1 = get_rule(rules, 1)
    if rule_1 is None:
        return None
    # Extract first decimal number after "≥" or ">=" in the text.
    match = re.search(r"(?:≥|>=)\s*(\d+(?:\.\d+)?)", rule_1["text"])
    if match:
        return float(match.group(1))
    return None


def get_quality_threshold_perceptual(rules: list[dict]) -> float | None:
    """Extract perceptual quality threshold from Hard Rule #1.

    Current canonical threshold per Hard Rule #1:
        user_perceptual_score ≥8.5

    Heuristic: second numeric threshold in Rule #1 text after the calibrated one.
    """
    rule_1 = get_rule(rules, 1)
    if rule_1 is None:
        return None
    matches = re.findall(r"(?:≥|>=)\s*(\d+(?:\.\d+)?)", rule_1["text"])
    if len(matches) >= 2:
        return float(matches[1])
    return None


if __name__ == "__main__":
    # CLI inspection: print parsed rules summary for human review.
    import json

    from ai_video.paths import hard_rules_doc

    canonical = hard_rules_doc()
    parsed = parse_hard_rules(canonical)
    summary = {
        "total_rules": len(parsed),
        "rule_ids": [r["rule_id"] for r in parsed],
        "severity_distribution": {
            s: sum(1 for r in parsed if r["severity"] == s) for s in ("critical", "blocker", "standard")
        },
        "rule_22_present": any(r["rule_id"] == 22 for r in parsed),
        "calibrated_threshold": get_quality_threshold_calibrated(parsed),
        "perceptual_threshold": get_quality_threshold_perceptual(parsed),
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
