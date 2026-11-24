"""
test_measure-canonical-decision-ui-pacing.py — adversarial tests for Sub-Fase 3A.2 TIER 2.1 refactor.

Per CLAUDE.md Hard Rule #26: every refactor ships with test_*.py companion.

Tests validate Capa A agnostic refactor:
1. --format required (no silent assumption)
2. --format horror-choice resolves legacy hardcoded paths (backward compat)
3. --format arbitrary resolves <format>-refs / referent-analysis/<format>/... pattern (agnostic proven)

Authority: Sub-Fase 3A.2 PRE-CLEANUP-A TIER 2.1 (2026-05-25).
"""
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/research/measure_canonical_decision_ui_pacing.py"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _run(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True,
    )


class TestMeasureCanonicalDecisionUIPacingRefactor(unittest.TestCase):

    def test_invocation_without_format_exits_nonzero_with_clear_error(self):
        """--format is REQUIRED. Missing → argparse error + non-zero exit."""
        result = _run(["--dry-run"])
        self.assertNotEqual(result.returncode, 0,
                            f"Expected non-zero exit when --format missing. Got {result.returncode}\nstderr: {result.stderr}")
        self.assertIn("format", result.stderr.lower(),
                      f"Error message must mention 'format'. stderr: {result.stderr}")

    def test_invocation_with_horror_choice_succeeds_on_existing_paths(self):
        """--format horror-choice resolves to legacy hardcoded paths (backward compat)."""
        result = _run(["--format", "horror-choice", "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 with --format horror-choice. Got {result.returncode}\nstderr: {result.stderr}")
        self.assertIn("videosref_elige_tu_compa", result.stdout,
                      "horror-choice default sources_dir must resolve to videosref_elige_tu_compa")
        self.assertIn("empirical-decision-ui-pacing", result.stdout,
                      "horror-choice default out_dir must include empirical-decision-ui-pacing")

    def test_invocation_with_arbitrary_format_name_succeeds_proves_agnostic(self):
        """--format <arbitrary> resolves to <arbitrary>-refs/ and referent-analysis/<arbitrary>/... pattern.

        Proves the script is AGNOSTIC: no longer hardcoded to horror-choice."""
        result = _run(["--format", "tutorial-test-stub", "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 with arbitrary --format. Got {result.returncode}\nstderr: {result.stderr}")
        self.assertIn("tutorial-test-stub-refs", result.stdout,
                      "Arbitrary format default sources_dir must follow <format>-refs/ pattern")
        self.assertIn("tutorial-test-stub/empirical-decision-ui-pacing", result.stdout,
                      "Arbitrary format default out_dir must follow referent-analysis/<format>/empirical-decision-ui-pacing/ pattern")
        self.assertNotIn("videosref_elige_tu_compa", result.stdout,
                         "Arbitrary format MUST NOT default to horror-choice paths (agnostic proof)")

    def test_explicit_override_flags_honored(self):
        """--sources-dir + --out-dir override format defaults."""
        result = _run([
            "--format", "horror-choice",
            "--sources-dir", "/custom/sources",
            "--out-dir", "/custom/out",
            "--dry-run"
        ])
        self.assertEqual(result.returncode, 0)
        self.assertIn("/custom/sources", result.stdout)
        self.assertIn("/custom/out", result.stdout)
        self.assertNotIn("videosref_elige_tu_compa", result.stdout,
                         "Override must NOT use horror-choice default when --sources-dir specified")


if __name__ == "__main__":
    unittest.main(verbosity=2)
