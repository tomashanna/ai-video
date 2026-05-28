"""
test_hard_rules_parser.py — adversarial tests for hard_rules_parser.py

Per CLAUDE.md Hard Rule #26: every new script ships with test_*.py companion
that validates against V4 archive / canonical filesystem ground truth.

Coverage targets (per Sub-Fase 3A Paso 3.1 handoff):
- Current CLAUDE.md parses to 25 rules (1-21 + 23-26)
- Rule #22 = empty slot (commit 48bd13e accidental skip per CLAUDE.md footnote)
  → parser MUST skip gracefully, NOT crash, NOT emit #22
- Rule #1 quality threshold extractable (both ≥9.0 calibrated + ≥8.5 perceptual)
- Rule #26 authority_pointer references BOOTSTRAP.md + INGENIERO-PAUTA-MASTER.md
- Severity extraction matches emoji prefix (⛔⛔ critical, ⛔ blocker, none standard)

Authority: CLAUDE.md Hard Rules table + footnote (Sub-Fase 3A 2026-05-23).
"""
import sys
import unittest
from pathlib import Path

# Add parent dir to path so `import hard_rules_parser` resolves regardless
# of cwd at test invocation (project scripts/lib/ or template scripts/lib/).
sys.path.insert(0, str(Path(__file__).parent))

from hard_rules_parser import parse_hard_rules, get_rule  # noqa: E402


CLAUDE_MD_PATH = Path("<repo-root>/CLAUDE.md")


class TestHardRulesParser(unittest.TestCase):
    """Canonical ground truth: current CLAUDE.md at root."""

    @classmethod
    def setUpClass(cls):
        cls.rules = parse_hard_rules(CLAUDE_MD_PATH)
        cls.rule_ids = sorted(r["rule_id"] for r in cls.rules)

    def test_parses_25_rules_current_claude_md(self):
        """Current CLAUDE.md must yield exactly 25 rules (1-21 + 23-26)."""
        self.assertEqual(
            len(self.rules),
            25,
            f"Expected 25 rules, got {len(self.rules)}. Sequence: {self.rule_ids}",
        )

    def test_rule_22_gracefully_skipped(self):
        """Rule #22 = empty slot per CLAUDE.md footnote (commit 48bd13e
        accidental skip 2026-05-21). Parser MUST NOT crash + MUST NOT emit #22."""
        self.assertNotIn(
            22,
            self.rule_ids,
            "Rule #22 is canonical empty slot. Parser must skip gracefully.",
        )

    def test_sequence_exactly_1_to_21_plus_23_to_26(self):
        """Sequence drift detector. Expected: [1..21] + [23..26]. No other gaps."""
        expected = list(range(1, 22)) + [23, 24, 25, 26]
        self.assertEqual(
            self.rule_ids,
            expected,
            f"Sequence drift detected. Expected {expected}, got {self.rule_ids}",
        )

    def test_rule_1_quality_threshold_extractable(self):
        """Rule #1 = dual quality gate. Text must contain both calibrated ≥9.0
        and perceptual ≥8.5 thresholds (Hard Rule #1 updated 2026-05-21 PM late)."""
        rule_1 = get_rule(self.rules, 1)
        self.assertIsNotNone(rule_1, "Rule #1 missing from parse output")
        self.assertIn(
            "≥9.0",
            rule_1["text"],
            f"Rule #1 missing calibrated ≥9.0 threshold. Excerpt: {rule_1['text'][:300]}",
        )
        self.assertIn(
            "≥8.5",
            rule_1["text"],
            "Rule #1 missing perceptual ≥8.5 threshold",
        )

    def test_rule_26_authority_pointer_resolvable(self):
        """Rule #26 (Tests adversariales obligatorios forward, Paso 2 added)
        authority_pointer must reference both BOOTSTRAP.md + INGENIERO-PAUTA-MASTER.md."""
        rule_26 = get_rule(self.rules, 26)
        self.assertIsNotNone(rule_26, "Rule #26 missing (Paso 2 added it)")
        self.assertIn(
            "BOOTSTRAP.md",
            rule_26["authority_pointer"],
            f"Rule #26 authority missing BOOTSTRAP.md. Got: {rule_26['authority_pointer']}",
        )
        self.assertIn(
            "INGENIERO-PAUTA-MASTER.md",
            rule_26["authority_pointer"],
            "Rule #26 authority missing INGENIERO-PAUTA-MASTER.md",
        )

    def test_severity_extraction(self):
        """Severity per emoji prefix in rule_id column:
        ⛔⛔ → 'critical' (Rules #24, #25)
        ⛔  → 'blocker'  (Rule #26)
        none → 'standard' (most other rules e.g., #1)
        """
        rule_24 = get_rule(self.rules, 24)
        rule_25 = get_rule(self.rules, 25)
        rule_26 = get_rule(self.rules, 26)
        rule_1 = get_rule(self.rules, 1)

        self.assertEqual(rule_24["severity"], "critical",
                         f"Rule #24 severity: expected 'critical', got {rule_24['severity']}")
        self.assertEqual(rule_25["severity"], "critical",
                         f"Rule #25 severity: expected 'critical', got {rule_25['severity']}")
        self.assertEqual(rule_26["severity"], "blocker",
                         f"Rule #26 severity: expected 'blocker', got {rule_26['severity']}")
        self.assertEqual(rule_1["severity"], "standard",
                         f"Rule #1 severity: expected 'standard', got {rule_1['severity']}")

    def test_get_rule_missing_returns_none(self):
        """get_rule(rules, 22) for the empty slot returns None, NOT raises."""
        rule_22 = get_rule(self.rules, 22)
        self.assertIsNone(rule_22, "Rule #22 lookup must return None (empty slot)")

    def test_schema_per_rule(self):
        """Every parsed rule has the canonical schema:
        {rule_id: int, text: str, severity: str, authority_pointer: str}."""
        required_keys = {"rule_id", "text", "severity", "authority_pointer"}
        for r in self.rules:
            self.assertEqual(
                set(r.keys()) & required_keys,
                required_keys,
                f"Rule #{r.get('rule_id')} missing schema keys. Got: {set(r.keys())}",
            )
            self.assertIsInstance(r["rule_id"], int)
            self.assertIsInstance(r["text"], str)
            self.assertIsInstance(r["severity"], str)
            self.assertIsInstance(r["authority_pointer"], str)
            self.assertGreater(len(r["text"]), 0, f"Rule #{r['rule_id']} has empty text")


if __name__ == "__main__":
    unittest.main(verbosity=2)
