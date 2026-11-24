"""
test_qa-gate.py — adversarial tests for qa-gate.py dual-branch patch.

Per CLAUDE.md Hard Rule #26 + Sub-Fase 3A 2026-05-23: every patched script
ships with test_*.py companion validating FAIL→PASS TDD transition.

Test cases (per Paso 3.2 handoff):
1. V4 archive case: calibrated 8.1 + perceptual ≥8.5 → PASS via Rule D precedence
2. V4 archive case: calibrated 8.1 + perceptual MISSING → AWAITING_USER_PERCEPTUAL
3. Mock case: calibrated 9.5 + any → PASS via calibrated branch
4. Dynamic threshold: temp CLAUDE.md with modified threshold → qa-gate reads new value
5. HUMAN-CHECKLIST auto-gen: calibrated FAIL + --project-dir → file created project-scoped
6. Backward compat: legacy --score flag still works

Authority: CLAUDE.md Hard Rule #1 (dual gate calibrated 9.0 OR perceptual 8.5)
+ #19 (never estimate, always measure) + #26 (tests adversariales).

V4 archive ground truth: cerro-aislado-v4/CP5-handoff.md L40 documents
calibrated 8.1 — real score, no mock needed for V4 test cases.
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
QA_GATE_PATH = Path(__file__).resolve().parents[2] / "src/ai_video/audits/qa_gate.py"
CLAUDE_MD_CANONICAL = Path(__file__).resolve().parents[2] / "docs/OPERATING-MANUAL.md"
HUMAN_CHECKLIST_CANONICAL = (
    Path(__file__).resolve().parents[2] / ".claude/skills/video-director/HUMAN-CHECKLIST.md"
)


def _run_qa_gate(args: list, env_overrides: dict | None = None) -> subprocess.CompletedProcess:
    """Run qa-gate.py subprocess. Returns CompletedProcess with returncode + stdout."""
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run(
        [sys.executable, str(QA_GATE_PATH)] + args,
        capture_output=True,
        text=True,
        env=env,
    )


class TestQaGateDualBranch(unittest.TestCase):
    """Sub-Fase 3A Paso 3.2 dual-branch dynamic-threshold patch validation."""

    def test_v4_calibrated_below_perceptual_above_passes_rule_d(self):
        """V4 archive case: calibrated 8.1 (below 9.0) + perceptual 8.5 (≥8.5)
        → PASS via Rule D PRECEDENCE (user perceptual = ground truth final)."""
        result = _run_qa_gate(
            [
                "--calibrated",
                "8.1",
                "--perceptual",
                "8.5",
                "--stage",
                "pre-kling",
                "--iteration",
                "1",
            ]
        )
        self.assertEqual(
            result.returncode,
            0,
            f"Expected PASS (exit 0), got exit {result.returncode}. "
            f"stdout: {result.stdout}\nstderr: {result.stderr}",
        )
        self.assertIn("PASS", result.stdout, "Output must declare PASS verdict")
        # Rule D precedence: perceptual branch wins
        self.assertTrue(
            "perceptual" in result.stdout.lower() or "Rule D" in result.stdout,
            f"Output must mention perceptual branch / Rule D. Got: {result.stdout}",
        )

    def test_v4_calibrated_below_perceptual_missing_awaiting(self):
        """V4 archive case: calibrated 8.1 + perceptual NOT provided
        → status AWAITING_USER_PERCEPTUAL (exit 3, new code Sub-Fase 3A)."""
        result = _run_qa_gate(
            [
                "--calibrated",
                "8.1",
                "--stage",
                "pre-kling",
                "--iteration",
                "1",
            ]
        )
        self.assertEqual(
            result.returncode,
            3,
            f"Expected AWAITING_USER_PERCEPTUAL (exit 3), got exit {result.returncode}. "
            f"stdout: {result.stdout}",
        )
        self.assertIn("AWAITING_USER_PERCEPTUAL", result.stdout)

    def test_mock_calibrated_above_threshold_passes_calibrated_branch(self):
        """Mock case: calibrated 9.5 (≥9.0) regardless of perceptual
        → PASS via calibrated branch (Rule D precedence not needed)."""
        result = _run_qa_gate(
            [
                "--calibrated",
                "9.5",
                "--stage",
                "pre-kling",
            ]
        )
        self.assertEqual(result.returncode, 0, f"Expected PASS (exit 0). stdout: {result.stdout}")
        self.assertIn("PASS", result.stdout)
        self.assertIn("calibrated", result.stdout.lower())

    def test_dynamic_threshold_read_from_claude_md(self):
        """Dynamic threshold: temp CLAUDE.md with modified threshold.
        With threshold raised to ≥9.5, calibrated 9.0 should FAIL (no longer PASS).
        Verifies Hard Rule #19 NEVER-HARDCODE — qa-gate reads CLAUDE.md at runtime."""
        original_content = CLAUDE_MD_CANONICAL.read_text(encoding="utf-8")
        # Replace ONLY the first ≥9.0 occurrence (Rule #1 calibrated threshold)
        modified_content = original_content.replace("≥9.0", "≥9.5", 1)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tmp:
            tmp.write(modified_content)
            tmp_path = tmp.name

        try:
            # Run with calibrated=9.0. Should FAIL because temp CLAUDE.md threshold is 9.5.
            result = _run_qa_gate(
                ["--calibrated", "9.0", "--stage", "pre-kling"],
                env_overrides={"CLAUDE_MD_PATH": tmp_path},
            )
            self.assertNotEqual(
                result.returncode,
                0,
                f"qa-gate should NOT pass calibrated 9.0 against temp threshold 9.5. "
                f"This means qa-gate is hardcoded (not reading CLAUDE.md). "
                f"stdout: {result.stdout}",
            )
        finally:
            os.unlink(tmp_path)

    def test_human_checklist_auto_generated_on_calibrated_fail(self):
        """HUMAN-CHECKLIST auto-gen: calibrated 7.5 (below threshold) + --project-dir
        → file <project_dir>/HUMAN-CHECKLIST-<project_id>.md created with pre-filled fields."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            project_id = "test-proj-auto-gen"
            result = _run_qa_gate(
                [
                    "--calibrated",
                    "7.5",
                    "--stage",
                    "pre-kling",
                    "--project-dir",
                    tmp_dir,
                    "--project-id",
                    project_id,
                ]
            )
            # Exit code is AWAITING (3) because perceptual missing — checklist still must be auto-gen
            checklist_path = Path(tmp_dir) / f"HUMAN-CHECKLIST-{project_id}.md"
            self.assertTrue(
                checklist_path.exists(),
                f"HUMAN-CHECKLIST instance NOT generated. "
                f"Expected: {checklist_path}\nstdout: {result.stdout}\nstderr: {result.stderr}",
            )
            content = checklist_path.read_text(encoding="utf-8")
            # Pre-filled fields verification
            self.assertIn(project_id, content, f"Generated file missing project_id ({project_id})")
            self.assertIn("7.5", content, "Generated file missing calibrated_score reported")
            self.assertIn("PENDIENTE", content, "Generated file must declare status PENDIENTE")

    def test_human_checklist_canonical_not_modified(self):
        """Auto-gen MUST NOT modify the canonical HUMAN-CHECKLIST.md template."""
        canonical_pre = HUMAN_CHECKLIST_CANONICAL.read_bytes()
        with tempfile.TemporaryDirectory() as tmp_dir:
            _run_qa_gate(
                [
                    "--calibrated",
                    "7.5",
                    "--stage",
                    "pre-kling",
                    "--project-dir",
                    tmp_dir,
                    "--project-id",
                    "preservation-test",
                ]
            )
        canonical_post = HUMAN_CHECKLIST_CANONICAL.read_bytes()
        self.assertEqual(
            canonical_pre,
            canonical_post,
            "Canonical HUMAN-CHECKLIST.md was modified — auto-gen must use READ-ONLY copy",
        )

    def test_legacy_score_flag_back_compat(self):
        """Legacy --score invocation must still work (no breaking change for existing callers)."""
        result = _run_qa_gate(
            [
                "--score",
                "9.7",
                "--stage",
                "pre-kling",
            ]
        )
        self.assertEqual(
            result.returncode,
            0,
            f"Legacy --score 9.7 should PASS. Got exit {result.returncode}. stdout: {result.stdout}",
        )

    def test_calibrated_xor_score_required(self):
        """Invocation without --score AND without --calibrated → error (parser-level)."""
        result = _run_qa_gate(["--stage", "pre-kling"])
        self.assertNotEqual(result.returncode, 0, "Must error if neither --score nor --calibrated provided")


if __name__ == "__main__":
    unittest.main(verbosity=2)
