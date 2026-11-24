"""test_audit-spec-narration-fits-duration.py — BUILD 5 Sprint M L1.

Validates that SPEC narration_text per shot FITS in declared duration_intent_s
(implied WPM physically achievable for TTS). Pre-emit gate — runs before TTS generation.

7 tests: CLI/capability/Bug9 + clean PASS + WPM too high FAIL + WPM too low FLAG + missing-input skip.
"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_spec_narration_fits_duration.py"


def _load_module():
    """Import the hyphen-named script as a module to unit-test its matrix reader directly."""
    spec = importlib.util.spec_from_file_location("l1_narration_fit", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _write_spec(path, *, has_tts=True, shot_yaml=None, omit_caps=False):
    caps = (
        ""
        if omit_caps
        else (
            "video_capabilities:\n"
            f'  has_tts_narration: {str(has_tts).lower()}\n'
            '  format_type: "interactive_choice"\n'
        )
    )
    body = (
        shot_yaml
        or """shot_list:
  - shot_id: shot_01
    duration_intent_s: 4.0
    narration_in_this_shot:
      narrator_text: "Aterrizaje nocturno con dos dilemas en cuatro horas vivirás"
  - shot_id: shot_02
    duration_intent_s: 3.0
    narration_in_this_shot:
      narrator_text: "Hay dos figuras esperándote en la torre"
"""
    )
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
        self.assertNotIn(
            "shot_visual_only", r.stdout.split("fail_shots")[0] if "fail_shots" in r.stdout else r.stdout
        )


_V11_STRING_SCHEMA = """schema_version: "v11.1"
video_capabilities:
  format_type: "interactive_choice"
  has_tts_narration: true
shot_list:
  - shot_id: shot_01
    section_id: hook
    duration_intent_s: 4.0
    narration_in_this_shot: "Elige a tu compañero para esta noche. Axel o Hugo."
    has_lip_sync_required: false
    dialog_text: null
"""

# V5 bug class: narration at canonical pace LONGER than min(duration_intent_s, i2v clip max) → truncated.
_V5_BUG_TRUNCATION = """schema_version: "v11.1"
video_capabilities:
  format_type: "interactive_choice"
  has_tts_narration: true
shot_list:
  - shot_id: shot_20
    section_id: resolution_b
    duration_intent_s: 5.0
    narration_in_this_shot: "Si aguantas afuera, la ducha se purga sola. Axel asiente y se aparta. La esclusa se abre al amanecer. Sales con vida."
    has_lip_sync_required: false
    dialog_text: null
"""


class TestV11RealSchemaRegression(unittest.TestCase):
    """pattern_class 4/5: parse REAL v11 schema (string narration_in_this_shot), not only dict fixtures."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.spec.write_text(_V11_STRING_SCHEMA, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_v11_string_schema_no_crash(self):
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertNotIn("Traceback", r.stderr, f"crashed on v11 string schema:\n{r.stderr}")
        self.assertNotIn("AttributeError", r.stderr)
        # shot_01 = 10 words / 4.0s → canonical 3.64s ≤ min(4.0, 5.9) → fits, exit 0
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}")

    def test_v5_bug_narration_exceeds_canonical_fit_fails(self):
        # 22 words / 165 WPM = 8.0s canonical > min(duration_intent_s 5.0, i2v 5.9) → MUST FAIL (V5 bug class).
        # Old check (WPM=22/5*60=264 ≤ 280) would have PASSED → that was the V5 gap.
        self.spec.write_text(_V5_BUG_TRUNCATION, encoding="utf-8")
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertNotEqual(
            r.returncode, 0, f"narration exceeding canonical fit must FAIL.\nstdout {r.stdout}"
        )
        self.assertIn("truncated", r.stdout.lower())


# Reproduces the MATRIX structure where a COMMENTED top-level key (veo_3_1: # forward ...) follows
# hailuo_std. The pre-fix reader matched `^name:$` against the raw line, so the commented key never
# reset `cur` → veo_3_1's clip_duration_max_s (8) got attributed to hailuo_std, reading 8.0 not 5.9.
_MATRIX_WITH_COMMENTED_KEY = """## i2v
```yaml
hailuo_std:
  type: i2v
  clip_duration_max_s: 5.9          # observado V5: 5.875s reales

hailuo_pro:        # forward — NO usado aún
  type: i2v
  clip_duration_max_s: 10
  status: unverified_forward

veo_3_1:           # forward — NO usado (billing surprise V3)
  type: i2v
  clip_duration_max_s: 8
  status: avoid_until_billing_confirmed
```

## tts
```yaml
elevenlabs:
  canonical_pace_wpm: 165
```
"""


class TestMatrixReaderInlineCommentRegression(unittest.TestCase):
    """REGRESSION: a commented top-level key (e.g. `veo_3_1: # forward ...`) must not bleed its
    clip_duration_max_s onto the previous key. hailuo_std must read 5.9, NOT 8.0."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.matrix = Path(self.tmp) / "MATRIX.md"
        self.matrix.write_text(_MATRIX_WITH_COMMENTED_KEY, encoding="utf-8")
        self.mod = _load_module()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_hailuo_std_reads_59_not_80_with_commented_veo_key(self):
        wpm, caps = self.mod.load_matrix_values(self.matrix)
        self.assertEqual(
            caps.get("hailuo_std"), 5.9, f"commented veo_3_1 key bled its cap onto hailuo_std: {caps}"
        )
        self.assertNotEqual(caps.get("hailuo_std"), 8.0)
        # the commented keys must be parsed as their OWN entries (comment stripped, then matched)
        self.assertEqual(caps.get("hailuo_pro"), 10.0, caps)
        self.assertEqual(caps.get("veo_3_1"), 8.0, caps)
        self.assertEqual(wpm, 165.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
