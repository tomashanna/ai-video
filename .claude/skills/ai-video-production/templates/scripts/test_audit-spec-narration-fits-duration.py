"""test_audit-spec-narration-fits-duration.py — BUILD 5 Sprint M L1.

Validates that SPEC narration_text per shot FITS in declared duration_intent_s
(implied WPM physically achievable for TTS). Pre-emit gate — runs before TTS generation.

7 tests: CLI/capability/Bug9 + clean PASS + WPM too high FAIL + WPM too low FLAG + missing-input skip.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-narration-fits-duration.py"


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _write_spec(path, *, has_tts=True, shot_yaml=None, omit_caps=False):
    caps = "" if omit_caps else (
        "video_capabilities:\n"
        f'  has_tts_narration: {str(has_tts).lower()}\n'
        '  format_type: "interactive_choice"\n'
    )
    body = shot_yaml or """shot_list:
  - shot_id: shot_01
    duration_intent_s: 3.0
    narration_in_this_shot:
      narrator_text: "Aterrizaje nocturno con dos dilemas en cuatro horas vivirás"
  - shot_id: shot_02
    duration_intent_s: 2.5
    narration_in_this_shot:
      narrator_text: "Hay dos figuras esperándote en la torre"
"""
    Path(path).write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")


class TestL1(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero(self):
        _write_spec(self.spec)
        r = _run(["--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("format", r.stderr.lower())

    def test_bug9_video_capabilities_missing(self):
        _write_spec(self.spec, omit_caps=True)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 2)

    def test_has_tts_narration_false_not_applicable(self):
        _write_spec(self.spec, has_tts=False)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout.lower())

    def test_clean_spec_passes(self):
        # 9 words / 3.0s = 180 WPM ∈ [60, 280] ✓; 7 words / 2.5s = 168 WPM ✓
        _write_spec(self.spec)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("\"pass\"", r.stdout)

    def test_wpm_exceeds_max_fails(self):
        # 30 words / 1.0s = 1800 WPM > 280 → FAIL
        shot = """shot_list:
  - shot_id: shot_overload
    duration_intent_s: 1.0
    narration_in_this_shot:
      narrator_text: "uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte veintiuno veintidos veintitres veinticuatro veinticinco veintiseis veintisiete veintiocho veintinueve treinta"
"""
        _write_spec(self.spec, shot_yaml=shot)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("shot_overload", r.stdout)

    def test_wpm_below_min_flag(self):
        # 1 word / 10.0s = 6 WPM < 60 → FLAG (exit 0, warning in stdout)
        shot = """shot_list:
  - shot_id: shot_slow
    duration_intent_s: 10.0
    narration_in_this_shot:
      narrator_text: "Solo"
"""
        _write_spec(self.spec, shot_yaml=shot)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"FLAG verdict must exit 0. stdout {r.stdout}")
        self.assertIn("flag", r.stdout.lower())

    def test_missing_narration_or_duration_skipped(self):
        # Shot without narrator_text — should be skipped, not failed
        shot = """shot_list:
  - shot_id: shot_visual_only
    duration_intent_s: 3.0
  - shot_id: shot_normal
    duration_intent_s: 3.0
    narration_in_this_shot:
      narrator_text: "Tres palabras canonical"
"""
        _write_spec(self.spec, shot_yaml=shot)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0)
        # shot_visual_only shouldn't appear in fail_shots or flag_shots
        self.assertNotIn("shot_visual_only", r.stdout.split("fail_shots")[0] if "fail_shots" in r.stdout else r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
