"""
test_audit-spec-completeness.py — adversarial tests for the dict-form ui_active backport.

Per CLAUDE.md Hard Rule #26 + Sub-Fase 3A 2026-05-23: every patched script ships
with test_*.py companion validating FAIL→PASS TDD transition.

Sprint 3.3 backport context (per cerro-aislado-v4/CP5-handoff.md L33+L83):
  - V4 SPEC v11.5 uses dict-form `ui_active: [{element_id, timestamp_visible_s, ...}]`
  - Original template script crashes: `AttributeError: 'dict' object has no attribute 'lower'`
    at line 79 (`elem_lower = elem.lower()` assumed string)
  - V4 engineer patched in-place; this backport propagates fix to template forward.

Test cases (mandatory per Paso 3.3 handoff):
1. V4 SPEC v11.5 case → template (post-backport) must NOT crash + match in-place output
2. Mock complete string-form SPEC → exit 0 PASS (no false positive regression)
3. Mock dict-form SPEC (V4-style) → exit 0 PASS (the backport scenario)
4. Mock missing assets → exit 1 FAIL (real defect detection preserved)
5. Mock malformed/missing SPEC path → exit 2 (script error handling)
6. Regression equivalence: in-place vs template post-backport → identical stdout/exit

Authority: CLAUDE.md Hard Rule #19 + #26. Bug class: SCHEMA EVOLUTION crash.
V4 ground truth: cerro-aislado-v4/CP5-handoff.md L33 (script was patched in-place;
backport pending). NO modificar V4 archive (D38).
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_SCRIPT = REPO_ROOT / "src" / "ai_video" / "audits" / "audit_spec_completeness.py"
INPLACE_SCRIPT = REPO_ROOT / "cerro-aislado-v4" / "scripts" / "audit-spec-completeness.py"
V4_SPEC = REPO_ROOT / "creative-specs" / "cerro-aislado-v4.yaml"
V4_PROJECT_DIR = REPO_ROOT / "cerro-aislado-v4"


def _run(script: Path, args: list) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script)] + args,
        capture_output=True,
        text=True,
    )


class TestAuditSpecCompletenessBackport(unittest.TestCase):
    """Backport dict-form ui_active support from V4 in-place to template."""

    # ---------- V4 ground truth tests ----------

    @unittest.skipUnless(V4_SPEC.exists() and V4_PROJECT_DIR.exists(), "local-only V4 project not present")
    def test_v4_spec_v11_5_no_crash_post_backport(self):
        """Template (post-backport) must NOT crash on V4 SPEC v11.5 dict-form ui_active.
        Pre-backport reproduces: AttributeError at L79. Post-backport: completes."""
        result = _run(TEMPLATE_SCRIPT, [
            "--spec", str(V4_SPEC),
            "--project-dir", str(V4_PROJECT_DIR),
            "--cp", "5",
            "--html", "index.html",
        ])
        self.assertNotIn(
            "AttributeError", result.stderr,
            f"Pre-backport bug: AttributeError on dict-form. stderr: {result.stderr}"
        )
        self.assertIn(
            "VERDICT:", result.stdout,
            f"Script must complete + emit VERDICT line. stdout: {result.stdout}"
        )
        # V4 SHIPPED — all assets present → must PASS inventory
        self.assertEqual(
            result.returncode, 0,
            f"V4 SHIPPED all assets present → expected exit 0. Got {result.returncode}.\n"
            f"stdout: {result.stdout}"
        )
        self.assertIn("INVENTORY COMPLETE", result.stdout)

    @unittest.skipUnless(V4_SPEC.exists() and V4_PROJECT_DIR.exists(), "local-only V4 project not present")
    def test_regression_equivalence_inplace_vs_template_post_backport(self):
        """Post-backport: in-place vs template MUST produce identical output on V4 input.
        This is the canonical regression check — patch equivalence verification."""
        inplace_result = _run(INPLACE_SCRIPT, [
            "--spec", str(V4_SPEC), "--project-dir", str(V4_PROJECT_DIR),
            "--cp", "5", "--html", "index.html",
        ])
        template_result = _run(TEMPLATE_SCRIPT, [
            "--spec", str(V4_SPEC), "--project-dir", str(V4_PROJECT_DIR),
            "--cp", "5", "--html", "index.html",
        ])
        self.assertEqual(
            inplace_result.returncode, template_result.returncode,
            f"Exit codes drift: in-place={inplace_result.returncode} "
            f"vs template={template_result.returncode}"
        )
        self.assertEqual(
            inplace_result.stdout, template_result.stdout,
            "stdout drift — regression detected post-backport"
        )

    # ---------- Mock tests (synthetic SPECs) ----------

    def test_mock_string_form_complete_passes(self):
        """Mock SPEC with string-form ui_active + assets present → exit 0 PASS."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            spec_content = """
schema_version: "v11.5"
asset_list:
  sfx_prompts_to_generate: []
  music_to_generate: []
  ambient_continuous_to_generate: []
  tts_segments_to_generate: 0
  shot_list_total: 0
shot_list:
  - shot_id: "shot_01"
    ui_active:
      - "countdown"
"""
            spec_file = tmp_path / "spec.yaml"
            spec_file.write_text(spec_content, encoding="utf-8")
            (tmp_path / "index.html").write_text(
                "<audio src='narration.mp3'></audio>\n<div class='countdown'></div>",
                encoding="utf-8",
            )

            result = _run(TEMPLATE_SCRIPT, [
                "--spec", str(spec_file), "--project-dir", str(tmp_path),
                "--cp", "5", "--html", "index.html",
            ])
            self.assertEqual(
                result.returncode, 0,
                f"String-form complete should PASS. stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
            self.assertIn("INVENTORY COMPLETE", result.stdout)

    def test_mock_dict_form_complete_passes(self):
        """Mock SPEC with dict-form ui_active (V4-style) → exit 0 PASS post-backport.
        This is the canonical bug class — pre-backport crashes here too."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            spec_content = """
schema_version: "v11.5"
asset_list:
  sfx_prompts_to_generate: []
  music_to_generate: []
  ambient_continuous_to_generate: []
  tts_segments_to_generate: 0
  shot_list_total: 0
shot_list:
  - shot_id: "shot_01"
    ui_active:
      - element_id: "countdown_overlay"
        timestamp_visible_s: [0.0, 2.5]
        position: {y_pct: 46}
"""
            spec_file = tmp_path / "spec.yaml"
            spec_file.write_text(spec_content, encoding="utf-8")
            (tmp_path / "index.html").write_text(
                "<audio src='narration.mp3'></audio>\n<div class='countdown'></div>",
                encoding="utf-8",
            )

            result = _run(TEMPLATE_SCRIPT, [
                "--spec", str(spec_file), "--project-dir", str(tmp_path),
                "--cp", "5", "--html", "index.html",
            ])
            self.assertNotIn(
                "AttributeError", result.stderr,
                f"Pre-backport crash. stderr: {result.stderr}"
            )
            self.assertEqual(
                result.returncode, 0,
                f"Dict-form complete should PASS post-backport. stdout: {result.stdout}"
            )
            self.assertIn("INVENTORY COMPLETE", result.stdout)

    def test_mock_missing_assets_fails(self):
        """Mock SPEC requires 5 SFX but assets/sfx/ empty → exit 1 FAIL.
        Confirms real defect detection preserved post-backport."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            spec_content = """
schema_version: "v11.5"
asset_list:
  sfx_prompts_to_generate:
    - sfx_id: "sfx1"
    - sfx_id: "sfx2"
    - sfx_id: "sfx3"
    - sfx_id: "sfx4"
    - sfx_id: "sfx5"
  music_to_generate: []
  ambient_continuous_to_generate: []
  tts_segments_to_generate: 0
  shot_list_total: 0
shot_list: []
"""
            spec_file = tmp_path / "spec.yaml"
            spec_file.write_text(spec_content, encoding="utf-8")
            (tmp_path / "assets" / "sfx").mkdir(parents=True)
            (tmp_path / "index.html").write_text("", encoding="utf-8")

            result = _run(TEMPLATE_SCRIPT, [
                "--spec", str(spec_file), "--project-dir", str(tmp_path),
                "--cp", "5", "--html", "index.html",
            ])
            self.assertEqual(
                result.returncode, 1,
                f"Missing assets → expected exit 1 FAIL. Got {result.returncode}"
            )
            self.assertIn("INVENTORY INCOMPLETE", result.stdout)

    def test_mock_spec_path_invalid_exit_2(self):
        """Missing SPEC file → exit 2 (script error handling clear)."""
        with tempfile.TemporaryDirectory() as tmp:
            result = _run(TEMPLATE_SCRIPT, [
                "--spec", "/tmp/__nonexistent_spec_test_12345.yaml",
                "--project-dir", tmp,
                "--cp", "5", "--html", "index.html",
            ])
            self.assertEqual(
                result.returncode, 2,
                f"Invalid SPEC path → expected exit 2. Got {result.returncode}.\n"
                f"stderr: {result.stderr}"
            )
            self.assertIn("not found", result.stderr.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
