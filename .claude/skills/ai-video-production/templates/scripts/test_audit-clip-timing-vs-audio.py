"""test_audit-clip-timing-vs-audio.py — L4 output-side of the V5 truncation trilogy.

Validates the PRODUCED media: per atomic clip (visual >= narration, visual >= intent-0.1) and per
final render (|video - audio| <= 0.3s, the amix duration=longest tail).

Strategy: the validator's LOGIC is in PURE functions (evaluate_clip_timing / evaluate_av_sync) that
receive already-extracted durations → unit-tested directly with NO media. The thin runtime
(ffprobe_stream_duration) is MONKEYPATCHED with a fake duration table so the CLI paths run without
any real mp4/ffprobe. We also stub Path.exists for the --video file presence check.

Run: python3 test_audit-clip-timing-vs-audio.py  (prints "OK: ..." + sys.exit(1) on failure)
"""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

# Import the dash-named script as a module.
_SCRIPT = Path(__file__).parent / "audit-clip-timing-vs-audio.py"
_spec = importlib.util.spec_from_file_location("audit_clip_timing_vs_audio", _SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


def _run_main(argv, fake_durs):
    """Run mod.main() in-process with a fake ffprobe table + video file presence stubbed.

    fake_durs: dict {("v"|"a"): float|None} returned by the mocked ffprobe_stream_duration.
    Returns (exit_code, parsed_stdout_or_raw, raw_stdout, raw_stderr).
    """
    orig_probe = mod.ffprobe_stream_duration
    orig_exists = Path.exists

    def fake_probe(path, stream):
        return fake_durs.get(stream)

    # Make the --video path appear to exist without touching the filesystem.
    def fake_exists(self):
        if self.name.endswith(".mp4"):
            return True
        return orig_exists(self)

    mod.ffprobe_stream_duration = fake_probe
    Path.exists = fake_exists
    out, err = io.StringIO(), io.StringIO()
    old_argv = sys.argv
    try:
        sys.argv = ["audit-clip-timing-vs-audio.py"] + argv
        with redirect_stdout(out), redirect_stderr(err):
            code = mod.main()
    finally:
        sys.argv = old_argv
        mod.ffprobe_stream_duration = orig_probe
        Path.exists = orig_exists
    raw = out.getvalue()
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = raw
    return code, parsed, raw, err.getvalue()


CLIP = "/tmp/shot_07.mp4"
RENDER = "/tmp/final_render.mp4"
BASE = ["--format", "horror-choice", "--has-ai-generated-clips", "true",
        "--has-tts-narration", "true"]


class TestPureClipTiming(unittest.TestCase):
    """PURE evaluate_clip_timing — the heart of the validator, no media at all."""

    def test_good_clip_passes(self):
        # Brief's GOOD case: visual 6.2 >= audio 6.0 >= intent (6.1-0.1=6.0), av_diff 0.1.
        ok, reasons = mod.evaluate_clip_timing(
            visual_dur=6.2, narration_dur=6.0, intent_dur=6.1, av_len_diff_s=0.1,
            i2v_clip_cap=5.9)
        # visual 6.2 > cap 5.9+0.25 → advisory FLAG present, but ok stays True (no FAIL).
        self.assertTrue(ok, f"good clip should PASS, reasons={reasons}")
        self.assertFalse(any(r.startswith("FAIL:") for r in reasons), reasons)

    def test_visual_shorter_than_narration_fails(self):
        # Brief's BAD case #1: visual 5.9 < audio 6.5 → narration on frozen frame → FAIL.
        ok, reasons = mod.evaluate_clip_timing(
            visual_dur=5.9, narration_dur=6.5, intent_dur=6.0, av_len_diff_s=0.6, i2v_clip_cap=5.9)
        self.assertFalse(ok, f"visual<narration must FAIL, reasons={reasons}")
        self.assertTrue(any("frozen/black frame" in r for r in reasons), reasons)

    def test_visual_shorter_than_intent_fails(self):
        # visual 5.5 < intent 6.1 - 0.1 = 6.0 → clip too short for its beat → FAIL.
        ok, reasons = mod.evaluate_clip_timing(
            visual_dur=5.5, narration_dur=5.4, intent_dur=6.1, av_len_diff_s=0.1, i2v_clip_cap=10.0)
        self.assertFalse(ok, f"visual<intent must FAIL, reasons={reasons}")
        self.assertTrue(any("duration_intent_s" in r for r in reasons), reasons)

    def test_av_stream_mismatch_fails(self):
        # Brief's BAD case #2: av_diff 1.2 > 0.3 → amix tail → FAIL.
        ok, reasons = mod.evaluate_clip_timing(
            visual_dur=6.2, narration_dur=6.0, intent_dur=6.1, av_len_diff_s=1.2, i2v_clip_cap=10.0)
        self.assertFalse(ok, f"av_diff 1.2 must FAIL, reasons={reasons}")
        self.assertTrue(any("stream tail mismatch" in r for r in reasons), reasons)

    def test_unmeasurable_visual_fails(self):
        ok, reasons = mod.evaluate_clip_timing(None, 6.0, 6.0, 0.0)
        self.assertFalse(ok)

    def test_skips_when_no_narration_no_intent(self):
        # No narration + no intent + tiny av_diff → nothing violated → PASS.
        ok, reasons = mod.evaluate_clip_timing(6.2, None, None, 0.05, i2v_clip_cap=10.0)
        self.assertTrue(ok, reasons)

    def test_exactly_on_boundary_passes(self):
        # visual == narration, av_diff == tol, visual == intent-0.1 → all boundaries OK.
        ok, reasons = mod.evaluate_clip_timing(6.0, 6.0, 6.1, 0.3, i2v_clip_cap=10.0)
        self.assertTrue(ok, f"boundary case should PASS, reasons={reasons}")


class TestPureAvSync(unittest.TestCase):
    def test_render_av_within_tol_passes(self):
        ok, reasons = mod.evaluate_av_sync(90.10, 90.00, av_tol=0.3)
        self.assertTrue(ok, reasons)

    def test_render_av_tail_fails(self):
        # |video - audio| = 1.2 > 0.3 → amix duration=longest tail → FAIL.
        ok, reasons = mod.evaluate_av_sync(91.20, 90.00, av_tol=0.3)
        self.assertFalse(ok, reasons)
        self.assertTrue(any("amix" in r for r in reasons), reasons)


class TestCliClipMode(unittest.TestCase):
    """CLI runtime via mocked ffprobe (no media)."""

    def test_good_clip_cli_passes(self):
        code, rep, raw, err = _run_main(
            BASE + ["--mode", "clip", "--video", CLIP, "--intent-dur", "6.1", "--narration-dur", "6.0"],
            {"v": 6.2, "a": 6.0})
        self.assertEqual(code, 0, f"good clip CLI must exit 0. raw={raw} err={err}")
        self.assertEqual(rep["overall_status"], "pass")

    def test_bad_visual_shorter_than_audio_cli_fails(self):
        # visual 5.9 < audio 6.5 (measured narration) → FAIL exit 1.
        code, rep, raw, err = _run_main(
            BASE + ["--mode", "clip", "--video", CLIP, "--intent-dur", "5.0"],
            {"v": 5.9, "a": 6.5})
        self.assertEqual(code, 1, f"visual<audio must exit 1. raw={raw}")
        self.assertEqual(rep["overall_status"], "fail")
        self.assertTrue(any("frozen/black frame" in r for r in rep["reasons"]), rep["reasons"])

    def test_capability_gate_not_applicable(self):
        code, rep, raw, err = _run_main(
            ["--format", "tutorial", "--has-ai-generated-clips", "false",
             "--mode", "clip", "--video", CLIP],
            {"v": 6.2, "a": 6.0})
        self.assertEqual(code, 0)
        self.assertEqual(rep["overall_status"], "not_applicable")

    def test_no_format_arg_errors(self):
        # argparse required --format missing → SystemExit nonzero.
        with self.assertRaises(SystemExit) as cm:
            _run_main(["--mode", "clip", "--video", CLIP], {"v": 6.0, "a": 6.0})
        self.assertNotEqual(cm.exception.code, 0)


class TestMatrixRead(unittest.TestCase):
    """HR#29: clip cap read from the REAL MODEL-CAPABILITIES-MATRIX.md (no hardcoded assumption)."""

    def test_reads_hailuo_std_cap_from_matrix(self):
        matrix = (Path(__file__).resolve().parent.parent.parent.parent
                  / "ai-video-production" / "MODEL-CAPABILITIES-MATRIX.md")
        if not matrix.exists():
            self.skipTest("MATRIX not at expected path")
        caps = mod.load_i2v_caps(matrix)
        # Must NOT bleed veo_3_1's 8 into hailuo_std (trailing-comment key bug).
        self.assertAlmostEqual(caps["hailuo_std"], 5.9, places=2, msg=caps)


class TestCliRenderMode(unittest.TestCase):
    def test_render_av_diff_passes(self):
        code, rep, raw, err = _run_main(
            ["--format", "horror-choice", "--mode", "render", "--video", RENDER],
            {"v": 90.1, "a": 90.0})
        self.assertEqual(code, 0, f"raw={raw}")
        self.assertEqual(rep["overall_status"], "pass")

    def test_render_av_tail_fails(self):
        # |video - audio| = 1.2 > 0.3 → FAIL exit 1 (amix duration=longest tail).
        code, rep, raw, err = _run_main(
            ["--format", "horror-choice", "--mode", "render", "--video", RENDER],
            {"v": 91.2, "a": 90.0})
        self.assertEqual(code, 1, f"av tail must exit 1. raw={raw}")
        self.assertEqual(rep["overall_status"], "fail")

    def test_render_no_audio_cannot_measure(self):
        code, rep, raw, err = _run_main(
            ["--format", "horror-choice", "--mode", "render", "--video", RENDER],
            {"v": 90.0, "a": None})
        self.assertEqual(code, 2, f"no audio → exit 2. raw={raw}")


def _suite_runner():
    """Run unittest and print OK/exit(1) in the project's test_*.py house style."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for tc in (TestPureClipTiming, TestPureAvSync, TestMatrixRead, TestCliClipMode, TestCliRenderMode):
        suite.addTests(loader.loadTestsFromTestCase(tc))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if result.wasSuccessful():
        print("OK: audit-clip-timing-vs-audio — pure logic (good/visual<narration/visual<intent/"
              "av-tail) + CLI clip/render modes + capability gate + ffprobe MOCKED, no media used")
        sys.exit(0)
    else:
        print("FAIL: audit-clip-timing-vs-audio tests failed")
        sys.exit(1)


if __name__ == "__main__":
    _suite_runner()
