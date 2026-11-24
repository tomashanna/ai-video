"""test_audit-tts-vs-spec-duration.py — BUILD 6 Sprint M L2.

Post-CP2 gate: TTS actual duration (mp3 in tts-dir) vs SPEC duration_intent_s per shot.
Catches TTS overshoots that would cause sync drift or shot overlap downstream.

7 tests: CLI/capability/Bug9 + clean match + overshoot FAIL + TTS missing FAIL + no-narration skip.
Synthetic mp3s via ffmpeg lavfi (sine tones at controlled durations).
"""
import json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

import pytest

pytestmark = pytest.mark.ffmpeg  # synthesises fixtures with ffmpeg lavfi

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_tts_vs_spec_duration.py"
SR = 48000


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _make_mp3(path, duration_s, freq=220):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={duration_s}:sample_rate={SR}",
        "-c:a", "libmp3lame", "-t", str(duration_s), str(path),
    ], check=True, capture_output=True)


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
      narrator_text: "Tres segundos de narración"
  - shot_id: shot_02
    duration_intent_s: 2.0
    narration_in_this_shot:
      narrator_text: "Dos segundos"
"""
    Path(path).write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")


class TestL2(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.tts = Path(self.tmp) / "tts"
        self.tts.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero(self):
        _write_spec(self.spec)
        r = _run(["--spec", str(self.spec), "--tts-dir", str(self.tts), "--dry-run"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("format", r.stderr.lower())

    def test_bug9_video_capabilities_missing(self):
        _write_spec(self.spec, omit_caps=True)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--tts-dir", str(self.tts)])
        self.assertEqual(r.returncode, 2)

    def test_has_tts_narration_false_not_applicable(self):
        _write_spec(self.spec, has_tts=False)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--tts-dir", str(self.tts)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout.lower())

    def test_clean_match_passes(self):
        # mp3 durations match SPEC ±0.1s tolerance
        _write_spec(self.spec)
        _make_mp3(self.tts / "shot_01_narrator.mp3", 3.0)
        _make_mp3(self.tts / "shot_02_narrator.mp3", 2.0)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--tts-dir", str(self.tts)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("\"pass\"", r.stdout)

    def test_tts_overshoot_fails(self):
        # mp3 way longer than SPEC intent → FAIL
        _write_spec(self.spec)
        _make_mp3(self.tts / "shot_01_narrator.mp3", 6.0)  # 6s vs intent 3s → overshoot 3s
        _make_mp3(self.tts / "shot_02_narrator.mp3", 2.0)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--tts-dir", str(self.tts), "--tolerance-s", "0.5"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("shot_01", r.stdout)

    def test_tts_missing_when_narration_expected_fails(self):
        _write_spec(self.spec)
        _make_mp3(self.tts / "shot_01_narrator.mp3", 3.0)
        # shot_02 narrator missing → FAIL
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--tts-dir", str(self.tts)])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("shot_02", r.stdout)
        self.assertIn("missing", r.stdout.lower())

    def test_no_narration_shot_skipped(self):
        shot = """shot_list:
  - shot_id: shot_visual_only
    duration_intent_s: 3.0
  - shot_id: shot_narrator
    duration_intent_s: 2.0
    narration_in_this_shot:
      narrator_text: "Dos segundos"
"""
        _write_spec(self.spec, shot_yaml=shot)
        _make_mp3(self.tts / "shot_narrator_narrator.mp3", 2.0)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--tts-dir", str(self.tts)])
        self.assertEqual(r.returncode, 0,
                         f"shot_visual_only must be skipped (no narration expected)\nstdout {r.stdout}")
        self.assertIn("\"pass\"", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
