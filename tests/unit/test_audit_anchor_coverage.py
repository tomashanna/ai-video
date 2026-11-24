"""test_audit-anchor-coverage.py — CP1 anchor-coverage gate (Hard Rule #26 companion).

ANTI-THEATER: each test exercises the REAL bug this gate closes — an anchor needed by
>1 shot (or declared) but missing on disk → FileNotFoundError mid-batch in CP4 ($ spent).
The adversarial core (TestAdversarialCore) proves: bad case (missing prop in 2 shots) FAILs
naming the prop, AND clean cases (all present / single-shot-undeclared) PASS without noise.

Unit tests hit the PURE function evaluate_anchor_coverage + derive_needed_anchors directly;
CLI tests run the script by subprocess with tempfile SPEC fixtures + touched anchor files.
"""
import importlib.util, json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_anchor_coverage.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("anchor_coverage", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _project_with_anchors(tmp, anchor_files):
    """Create <tmp>/assets/anchors and touch each given <id>.png. Returns project dir path."""
    proj = Path(tmp)
    adir = proj / "assets" / "anchors"
    adir.mkdir(parents=True, exist_ok=True)
    for aid in anchor_files:
        (adir / f"{aid}.png").write_bytes(b"\x89PNG\r\n\x1a\n")  # minimal PNG-ish stub
    return proj


def _write_spec(path, body, *, has_ai_clips=True, omit_caps=False):
    caps = "" if omit_caps else (
        "video_capabilities:\n"
        f"  has_ai_generated_clips: {str(has_ai_clips).lower()}\n"
        '  format_type: "interactive_choice"\n'
    )
    Path(path).write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")


# A SPEC whose prop `olla_caldo_anchor` appears in TWO shots (matadero dialect).
_SPEC_PROP_IN_2_SHOTS = """reference_anchors:
  props:
    - id: olla_caldo_anchor
      severity: STRICT
      appears_in_shots: [shot_01, shot_21]
shot_list:
  - shot_id: shot_01
    anchor_id_required: {}
  - shot_id: shot_21
    anchor_id_required: {}
"""

# A SPEC where the same anchor_id is required in TWO shots (sala-limpia dialect).
_SPEC_CHAR_IN_2_SHOTS = """shot_list:
  - shot_id: shot_01
    anchor_id_required: {char_a: char_a_v1, char_b: char_b_v1}
  - shot_id: shot_06
    anchor_id_required: {char_a: char_a_v1}
"""

# A prop that appears in ONE shot only and is NOT declared in reference_anchors → not required.
_SPEC_PROP_IN_1_SHOT_UNDECLARED = """shot_list:
  - shot_id: shot_01
    anchor_id_required: {char_a: char_a_v1, prop_cameo: cameo_prop_v1}
  - shot_id: shot_02
    anchor_id_required: {char_a: char_a_v1}
"""


class TestAdversarialCore(unittest.TestCase):
    """The three task-mandated adversarial cases — the reason this gate exists."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_a_prop_in_2_shots_missing_anchor_FAILS_naming_it(self):
        # BAD case: olla_caldo_anchor needed (declared + 2 shots) but NO file → FAIL naming it.
        _write_spec(self.spec, _SPEC_PROP_IN_2_SHOTS)
        proj = _project_with_anchors(self.tmp, [])  # anchors dir exists but EMPTY
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 1, f"missing required anchor must FAIL.\nstdout {r.stdout}")
        self.assertIn("olla_caldo_anchor", r.stdout)
        rep = json.loads(r.stdout)
        self.assertEqual(rep["overall_status"], "fail")
        self.assertIn("olla_caldo_anchor", [m["anchor_id"] for m in rep["missing"]])

    def test_b_all_anchors_present_PASSES(self):
        # GOOD case: char_a_v1 + char_b_v1 both needed (≥2 shots) and both present → PASS.
        _write_spec(self.spec, _SPEC_CHAR_IN_2_SHOTS)
        proj = _project_with_anchors(self.tmp, ["char_a_v1", "char_b_v1"])
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 0, f"all anchors present must PASS.\nstdout {r.stdout}")
        rep = json.loads(r.stdout)
        self.assertEqual(rep["overall_status"], "pass")
        self.assertEqual(rep["missing"], [])

    def test_c_prop_in_1_shot_undeclared_NOT_required(self):
        # cameo_prop_v1 appears in exactly 1 shot and is NOT in reference_anchors → not needed.
        # char_a_v1 (2 shots) IS needed and IS present → overall PASS, no false alarm on cameo.
        _write_spec(self.spec, _SPEC_PROP_IN_1_SHOT_UNDECLARED)
        proj = _project_with_anchors(self.tmp, ["char_a_v1"])  # cameo NOT generated
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 0, f"single-shot undeclared prop must NOT be required.\nstdout {r.stdout}")
        rep = json.loads(r.stdout)
        self.assertEqual(rep["overall_status"], "pass")
        self.assertNotIn("cameo_prop_v1", rep["needed"])
        self.assertNotIn("cameo_prop_v1", [m["anchor_id"] for m in rep["missing"]])


class TestPureFunction(unittest.TestCase):
    """evaluate_anchor_coverage — the decision, isolated from filesystem/SPEC."""

    def setUp(self):
        self.mod = _load_module()

    def test_missing_is_named(self):
        ok, missing = self.mod.evaluate_anchor_coverage(
            needed=["olla_caldo_anchor", "char_a_v1"], present=["char_a_v1"])
        self.assertFalse(ok)
        self.assertEqual(missing, ["olla_caldo_anchor"])

    def test_all_present_ok(self):
        ok, missing = self.mod.evaluate_anchor_coverage(
            needed=["char_a_v1", "char_b_v1"], present=["char_a_v1", "char_b_v1", "extra_v1"])
        self.assertTrue(ok)
        self.assertEqual(missing, [])

    def test_empty_needed_trivially_ok(self):
        ok, missing = self.mod.evaluate_anchor_coverage(needed=[], present=[])
        self.assertTrue(ok)
        self.assertEqual(missing, [])

    def test_multiple_missing_sorted(self):
        ok, missing = self.mod.evaluate_anchor_coverage(
            needed=["zeta_v1", "alpha_v1", "mid_v1"], present=["mid_v1"])
        self.assertFalse(ok)
        self.assertEqual(missing, ["alpha_v1", "zeta_v1"])  # sorted, deterministic


class TestDeriveNeeded(unittest.TestCase):
    """derive_needed_anchors — the >1-shot / declared rule across both SPEC dialects."""

    def setUp(self):
        self.mod = _load_module()

    def test_declared_prop_is_needed_even_if_appears_once_field_absent(self):
        spec = {"reference_anchors": {"props": [{"id": "olla_caldo_anchor"}]}, "shot_list": []}
        needed, reasons = self.mod.derive_needed_anchors(spec)
        self.assertIn("olla_caldo_anchor", needed)
        self.assertIn("reference_anchors", reasons["olla_caldo_anchor"])

    def test_anchor_in_2_shots_needed_single_shot_not(self):
        spec = {"shot_list": [
            {"shot_id": "s1", "anchor_id_required": {"char_a": "char_a_v1", "p": "cameo_v1"}},
            {"shot_id": "s2", "anchor_id_required": {"char_a": "char_a_v1"}},
        ]}
        needed, _ = self.mod.derive_needed_anchors(spec)
        self.assertIn("char_a_v1", needed)        # 2 shots → needed
        self.assertNotIn("cameo_v1", needed)      # 1 shot, undeclared → not needed

    def test_declared_setting_with_appears_in_shots_count_in_reason(self):
        spec = {"reference_anchors": {"settings": [
            {"id": "matadero_interior_anchor", "appears_in_shots": ["s2", "s3", "s4"]}]}}
        needed, reasons = self.mod.derive_needed_anchors(spec)
        self.assertIn("matadero_interior_anchor", needed)
        self.assertIn("3 shots", reasons["matadero_interior_anchor"])


class TestCLIGates(unittest.TestCase):
    """Capability gating + Bug #9 + arg validation — mirror reference-validator conventions."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_format_required(self):
        _write_spec(self.spec, _SPEC_CHAR_IN_2_SHOTS)
        proj = _project_with_anchors(self.tmp, ["char_a_v1", "char_b_v1"])
        r = _run(["--spec", str(self.spec), "--project-dir", str(proj), "--dry-run"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("format", r.stderr.lower())

    def test_bug9_video_capabilities_missing(self):
        _write_spec(self.spec, _SPEC_CHAR_IN_2_SHOTS, omit_caps=True)
        proj = _project_with_anchors(self.tmp, ["char_a_v1", "char_b_v1"])
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 2)

    def test_has_ai_generated_clips_false_not_applicable(self):
        _write_spec(self.spec, _SPEC_PROP_IN_2_SHOTS, has_ai_clips=False)
        proj = _project_with_anchors(self.tmp, [])  # missing, but gate is off → still PASS
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout.lower())

    def test_anchors_dir_absent_is_measured_as_missing_not_crash(self):
        # project-dir with NO assets/anchors at all → can still measure (all needed missing) → FAIL, no crash.
        _write_spec(self.spec, _SPEC_CHAR_IN_2_SHOTS)
        proj = Path(self.tmp) / "emptyproj"
        proj.mkdir()
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--project-dir", str(proj)])
        self.assertEqual(r.returncode, 1, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertNotIn("Traceback", r.stderr)
        rep = json.loads(r.stdout)
        self.assertFalse(rep["anchors_dir_exists"])
        self.assertIn("char_a_v1", [m["anchor_id"] for m in rep["missing"]])

    def test_spec_not_found_cant_measure(self):
        r = _run(["--format", "horror-choice", "--spec", str(Path(self.tmp) / "nope.yaml"),
                  "--project-dir", self.tmp])
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    if not result.wasSuccessful():
        print("FAILED")
        sys.exit(1)
    print("OK: audit-anchor-coverage — adversarial bug caught (missing required anchor → FAIL), "
          "clean cases PASS (all present + single-shot-undeclared), pure fn + dialects + CLI gates verified")
