"""test_audit-spec-lip-sync-marks.py — BUILD 8 helper validator (PRE-4.J).

Validates SPEC per-shot lip_sync_required declarations (D17 architect compliance + consistency).
5 tests: CLI + Bug #9 + clean PASS + shot missing field FAIL + inconsistency (character speech but
lip_sync_required false) FAIL.
"""
import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-lip-sync-marks.py"


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _write_spec(path, *, shot_yaml=None, omit_caps=False):
    caps = "" if omit_caps else (
        "video_capabilities:\n"
        '  has_tts_narration: true\n'
        '  has_layer_2_effects: true\n'
        '  format_type: "interactive_choice"\n'
    )
    body = shot_yaml or """shot_list:
  - shot_id: shot_01
    lip_sync_required: false
    narration_in_this_shot:
      speaker: narrator_off_screen
      narrator_text: "Voiceover off-screen sin cara visible"
  - shot_id: shot_02
    lip_sync_required: true
    narration_in_this_shot:
      speaker: character_a
      dialog_text: "Te estaba esperando"
"""
    Path(path).write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")


class TestLipSyncMarks(unittest.TestCase):
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

    def test_clean_all_shots_marked_passes(self):
        _write_spec(self.spec)  # both shots have lip_sync_required + consistent
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("\"pass\"", r.stdout)

    def test_shot_missing_lip_sync_mark_fails(self):
        bad = """shot_list:
  - shot_id: shot_missing
    narration_in_this_shot:
      narrator_text: "shot sin lip_sync_required declarado"
"""
        _write_spec(self.spec, shot_yaml=bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("shot_missing", r.stdout)
        self.assertIn("missing", r.stdout.lower())

    def test_inconsistency_character_speech_but_lip_sync_false_fails(self):
        bad = """shot_list:
  - shot_id: shot_dialog_no_marker
    lip_sync_required: false
    narration_in_this_shot:
      speaker: character_a
      dialog_text: "Te estaba esperando aquí"
"""
        _write_spec(self.spec, shot_yaml=bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("inconsistency", r.stdout.lower())
        self.assertIn("shot_dialog_no_marker", r.stdout)

    def test_voice_off_exception_passes(self):
        # Faceless character (Axel visor) speaks via VOICE-OFF: dialog + lip_sync false + voice_off
        # → CANONICAL exception (AUDITOR-PROTOCOL CP4, calca ref-10 Rurik). Must PASS, not FAIL.
        ok = """shot_list:
  - shot_id: shot_axel_voiceoff
    has_lip_sync_required: false
    voice_off: true
    narration_in_this_shot: "Axel se acerca a la campana de flujo."
    dialog_text: "Sostenlo a la luz."
"""
        _write_spec(self.spec, shot_yaml=ok)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"voice_off exception must pass.\nstdout {r.stdout}")
        self.assertIn("\"pass\"", r.stdout)

    def test_faceless_character_exception_passes(self):
        ok = """shot_list:
  - shot_id: shot_faceless
    has_lip_sync_required: false
    faceless_character: true
    narration_in_this_shot:
      speaker: character_a
      dialog_text: "Métete y respira hondo"
"""
        _write_spec(self.spec, shot_yaml=ok)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"faceless_character exception must pass.\nstdout {r.stdout}")


_V11_STRING_SCHEMA = """schema_version: "v11.1"
video_capabilities:
  format_type: "interactive_choice"
  has_tts_narration: true
  has_layer_2_effects: true
shot_list:
  - shot_id: shot_01
    section_id: hook
    duration_intent_s: 3.0
    narration_in_this_shot: "Elige a tu compañero para esta noche."
    has_lip_sync_required: false
    dialog_text: null
"""


class TestV11RealSchemaRegression(unittest.TestCase):
    """pattern_class 4/5: parse REAL v11 schema — sibling has_lip_sync_required + sibling dialog_text
    (NOT dict narration_in_this_shot.speaker/.dialog_text + lip_sync_required). Regression for the
    AttributeError crash on the first real v11 SPEC."""
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
        # shot_01 declares has_lip_sync_required (sibling) + no dialog → consistent → PASS
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
