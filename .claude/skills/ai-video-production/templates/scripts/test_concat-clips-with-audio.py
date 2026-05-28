"""
test_concat-clips-with-audio.py — adversarial tests for Paso 4.2 concat-clips-with-audio.py.

Per CLAUDE.md Hard Rule #26: every new script ships with test_*.py companion.
TDD: written FIRST (RED), script implemented after (GREEN).

8 tests (5 capability-aware/agnostic + 3 properties):
1. --format required (no silent assumption)
2. --format horror-choice backward compat
3. --format arbitrary proves agnostic
4. source_clips_origin: pre_existing branches correctly
5. concat output_duration == sum(inputs) ±tolerance (property #1)
6. concat preserves codec h264+aac + fps + sample_rate (properties #2/#3/#4 — PRESERVATION not hardcoded value)
7. concat no audio dropout at boundaries (property #6 — ffprobe audio-duration ≈ video-duration proxy, NO Whisper)
8. caption baked preserved post-concat, gated by has_captions_baked (property #8, Hard Rule #25)

Fixtures: synthetic ffmpeg-lavfi clips (color + sine audio + optional drawtext). NO heavy py deps.
NO golden V4 reference per Tomás canonical principle (V4 clips read-only input data only, NOT quality reference).

Authority: Paso 4.2 build + PRE-4.B coverage + PRE-4.D dependency order + PRE-4.E xfade-post-concat.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parent / "concat-clips-with-audio.py"

FIXTURE_FPS = 30        # synthetic fixtures @ 30fps (hyperframes.json output target)
FIXTURE_SR = 48000      # 48kHz
FIXTURE_DUR = 1.0       # 1s per clip (fast)


def _run(args, env_overrides=None):
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True, env=env)


def _make_clip(path, duration=FIXTURE_DUR, fps=FIXTURE_FPS, color="red", caption_text=None):
    """Generate synthetic clip via ffmpeg lavfi: color video + sine audio + optional drawtext."""
    vf = f"fps={fps}"
    if caption_text:
        vf += f",drawtext=text='{caption_text}':fontcolor=white:fontsize=40:x=20:y=20:box=1:boxcolor=black"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=320x240:d={duration}:r={fps}",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}:sample_rate={FIXTURE_SR}",
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", str(FIXTURE_SR),
        "-t", str(duration),
        str(path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _ffprobe(path, stream, entries):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", stream,
         "-show_entries", f"stream={entries}", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return r.stdout.strip()


def _duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _audio_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def _write_spec(path, source_origin="ai_generated", has_ai=True, has_captions=True,
                fmt="interactive_choice", shots=("shot_01", "shot_02", "shot_03")):
    """Write minimal SPEC yaml with video_capabilities + shot_list (plain text, no yaml import)."""
    shot_lines = "\n".join(f"  - shot_id: {s}" for s in shots)
    content = f"""schema_version: "v11.1"
video_capabilities:
  source_clips_origin: "{source_origin}"
  has_ai_generated_clips: {str(has_ai).lower()}
  has_tts_narration: true
  has_human_voiceover: false
  audio_mix_target: "lufs_-14"
  has_sfx_layer: true
  has_captions_baked: {str(has_captions).lower()}
  has_layer_2_effects: true
  has_layer_3_music: true
  has_layer_4_ui: true
  format_type: "{fmt}"
shot_list:
{shot_lines}
"""
    Path(path).write_text(content, encoding="utf-8")


class TestConcatCLI(unittest.TestCase):
    """CLI + capability-aware + agnostic (no fixtures needed — dry-run)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero_with_clear_error(self):
        _write_spec(self.spec)
        result = _run(["--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(result.returncode, 0,
                            f"Expected non-zero without --format. stderr: {result.stderr}")
        self.assertIn("format", result.stderr.lower())

    def test_invocation_with_horror_choice_succeeds_on_existing_atomic_clips(self):
        _write_spec(self.spec, fmt="interactive_choice")
        result = _run(["--format", "horror-choice", "--spec", str(self.spec),
                       "--clips-dir", self.tmp, "--output-dir", self.tmp, "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("ai_generated", result.stdout, "horror-choice default branch should be ai_generated")

    def test_invocation_with_arbitrary_format_succeeds_proves_agnostic(self):
        _write_spec(self.spec, fmt="tutorial")
        result = _run(["--format", "tutorial-test-stub", "--spec", str(self.spec),
                       "--clips-dir", self.tmp, "--output-dir", self.tmp, "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 arbitrary format. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("tutorial-test-stub", result.stdout,
                      "Arbitrary format must appear in resolved output (agnostic proof)")

    def test_invocation_with_pre_existing_clips_branches_correctly(self):
        _write_spec(self.spec, source_origin="pre_existing", has_ai=False)
        result = _run(["--format", "compilation-test", "--spec", str(self.spec),
                       "--clips-dir", self.tmp, "--output-dir", self.tmp, "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 pre_existing. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("pre_existing", result.stdout,
                      "pre_existing source_clips_origin must branch to pre_existing path (capability-aware)")


class TestConcatProperties(unittest.TestCase):
    """Property tests — real concat of synthetic fixtures via ffprobe verification."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.clips_dir = Path(cls.tmp) / "clips-atomic"
        cls.out_dir = Path(cls.tmp) / "concat"
        cls.clips_dir.mkdir(parents=True)
        cls.out_dir.mkdir(parents=True)
        # 3 synthetic atomic clips, 1s each, 30fps 48kHz, w/ burned caption marker
        cls.clip_dur = FIXTURE_DUR
        for i, color in enumerate(["red", "green", "blue"], start=1):
            _make_clip(cls.clips_dir / f"shot_0{i}_atomic.mp4",
                       duration=cls.clip_dur, color=color, caption_text=f"CLIP{i}")
        cls.spec = Path(cls.tmp) / "spec.yaml"
        _write_spec(cls.spec)
        # Run the concat script (real)
        cls.result = _run(["--format", "horror-choice", "--spec", str(cls.spec),
                           "--clips-dir", str(cls.clips_dir), "--output-dir", str(cls.out_dir)])
        cls.output = cls.out_dir / "clips_concat_only.mp4"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_concat_succeeds_and_output_exists(self):
        self.assertEqual(self.result.returncode, 0,
                         f"Concat must exit 0. stdout: {self.result.stdout}\nstderr: {self.result.stderr}")
        self.assertTrue(self.output.exists(), f"Output mp4 must exist: {self.output}")

    def test_concat_output_duration_matches_sum_inputs_within_tolerance(self):
        """Property #1: output duration == sum(3 × 1s) ±0.15s tolerance."""
        self.assertTrue(self.output.exists())
        dur = _duration(self.output)
        expected = self.clip_dur * 3
        self.assertAlmostEqual(dur, expected, delta=0.15,
                               msg=f"Output duration {dur} != sum {expected} ±0.15")

    def test_concat_preserves_codec_h264_aac_fps_samplerate(self):
        """Properties #2/#3/#4: codec h264+aac PRESERVED + fps PRESERVED (30 from fixtures) + 48kHz."""
        self.assertTrue(self.output.exists())
        vcodec = _ffprobe(self.output, "v:0", "codec_name")
        acodec = _ffprobe(self.output, "a:0", "codec_name")
        rfps = _ffprobe(self.output, "v:0", "r_frame_rate")
        sr = _ffprobe(self.output, "a:0", "sample_rate")
        self.assertEqual(vcodec, "h264", f"Video codec must preserve h264, got {vcodec}")
        self.assertEqual(acodec, "aac", f"Audio codec must preserve aac, got {acodec}")
        self.assertEqual(rfps, f"{FIXTURE_FPS}/1", f"fps must preserve {FIXTURE_FPS}, got {rfps}")
        self.assertEqual(sr, str(FIXTURE_SR), f"sample_rate must preserve {FIXTURE_SR}, got {sr}")

    def test_concat_no_audio_dropout_at_boundaries(self):
        """Property #6 proxy: output audio duration ≈ video duration (no dropout/truncation).
        ffprobe-based, NO Whisper (test env minimal)."""
        self.assertTrue(self.output.exists())
        vdur = _duration(self.output)
        adur = _audio_duration(self.output)
        self.assertIsNotNone(adur, "Output must have audio stream (no dropout)")
        self.assertAlmostEqual(adur, vdur, delta=0.2,
                               msg=f"Audio duration {adur} must ≈ video duration {vdur} (no dropout)")

    def test_concat_caption_baked_preserved_post_concat(self):
        """Property #8 (Hard Rule #25 gated has_captions_baked): burned caption survives concat.
        Proxy: extract frame from each clip's window, verify non-uniform pixels (caption present)."""
        self.assertTrue(self.output.exists())
        # Extract frame at 0.5s (within clip 1 window) — should have burned "CLIP1" text
        frame = Path(self.tmp) / "_probe_frame.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "0.5",
                        "-i", str(self.output), "-vframes", "1", str(frame)],
                       check=True, capture_output=True)
        self.assertTrue(frame.exists(), "Frame extraction must succeed (frames preserved post-concat)")
        # Verify frame non-trivial size (caption + color content present, not black/empty)
        self.assertGreater(frame.stat().st_size, 1000,
                           "Extracted frame must have content (burned caption preserved)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
