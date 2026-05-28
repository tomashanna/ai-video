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


if __name__ == "__main__":
    unittest.main(verbosity=2)
