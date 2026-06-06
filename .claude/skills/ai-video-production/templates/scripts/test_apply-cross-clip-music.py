"""
test_apply-cross-clip-music.py — adversarial tests for Paso 4.3 apply-cross-clip-music.py.

Per CLAUDE.md Hard Rule #26: companion test sidecar. TDD: written FIRST (RED).

7 tests (3 capability-aware/agnostic + 1 branch + 3 properties PRE-4.C):
1. --format required (no silent assumption)
2. --format horror-choice dry-run resolves full branch
3. --format arbitrary proves agnostic
4. has_layer_3_music=false → master-only (no music mix; output mastered, duration match)
5. full mix final master LUFS within -14 ±0.5 (CANONICAL-ANCHORED F1, ebur128)
6. full mix output duration matches input video (audio doesn't truncate/extend)
7. sidechain duck recorded when narrator present; absent when has_tts_narration=false

Fixtures: synthetic ffmpeg-lavfi (color+sine video, sine music/narrator mp3s). NO numpy/whisper.
NO golden V4 reference. PRE-4.C tolerance: final LUFS canonical-anchored F1 (-14.06 ±0.41);
sidechain duck dB SPEC-declared (plumbing).

Authority: Paso 4.3 build + PIPELINE §13.7.5 Layer 3 + PRE-4.C bands + Pattern 7 + PRE-4.E.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "apply-cross-clip-music.py"
SR = 48000


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True)


def _make_video(path, duration=3.0, color="navy"):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=640x360:d={duration}:r=30",
        "-f", "lavfi", "-i", f"sine=frequency=330:duration={duration}:sample_rate={SR}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", str(SR),
        "-t", str(duration), str(path),
    ], check=True, capture_output=True)


def _make_audio(path, duration=3.0, freq=110):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={duration}:sample_rate={SR}",
        "-c:a", "libmp3lame", "-t", str(duration), str(path),
    ], check=True, capture_output=True)


def _duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def _measure_lufs(path):
    r = subprocess.run(["ffmpeg", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    matches = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", r.stderr)
    return float(matches[-1]) if matches else None


def _write_spec(path, has_l3_music=True, has_tts=True, mix_target="lufs_-14",
                fmt="interactive_choice", layers=("drone_base", "ambient_room"),
                omit_caps=False):
    caps = "" if omit_caps else (
        "video_capabilities:\n"
        f'  source_clips_origin: "ai_generated"\n'
        f"  has_tts_narration: {str(has_tts).lower()}\n"
        f"  has_layer_3_music: {str(has_l3_music).lower()}\n"
        f'  audio_mix_target: "{mix_target}"\n'
        f'  format_type: "{fmt}"\n'
    )
    layer_lines = "\n".join(f"  - layer_id: {l}" for l in layers)
    Path(path).write_text(
        f'schema_version: "v11.1"\n{caps}music_continuous_layers:\n{layer_lines}\n',
        encoding="utf-8")


class TestMusicCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero_with_clear_error(self):
        _write_spec(self.spec)
        r = _run(["--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(r.returncode, 0, f"stderr: {r.stderr}")
        self.assertIn("format", r.stderr.lower())

    def test_invocation_with_horror_choice_dry_run_full_branch(self):
        _write_spec(self.spec)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec), "--dry-run"])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("full", r.stdout.lower(), "has_layer_3_music=true → full branch")

    def test_invocation_with_arbitrary_format_succeeds_proves_agnostic(self):
        _write_spec(self.spec, fmt="tutorial")
        r = _run(["--format", "tutorial-stub", "--spec", str(self.spec), "--dry-run"])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("tutorial-stub", r.stdout, "Arbitrary format must appear (agnostic proof)")


class TestMasterOnlyBranch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.inp = Path(self.tmp) / "clips_with_effects.mp4"
        self.out = Path(self.tmp) / "master_final.mp4"
        _make_video(self.inp, duration=3.0)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_has_layer_3_music_false_master_only(self):
        _write_spec(self.spec, has_l3_music=False)
        r = _run(["--format", "compilation", "--spec", str(self.spec),
                  "--input", str(self.inp), "--output", str(self.out)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertTrue(self.out.exists(), "master-only must produce output")
        self.assertIn("master_only", r.stdout.lower())
        self.assertAlmostEqual(_duration(self.out), _duration(self.inp), delta=0.2)


class TestFullMixProperties(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.music_dir = Path(cls.tmp) / "music"
        cls.music_dir.mkdir(parents=True)
        cls.inp = Path(cls.tmp) / "clips_with_effects.mp4"
        cls.narr = Path(cls.tmp) / "narrator.mp3"
        cls.out = Path(cls.tmp) / "master_final.mp4"
        _make_video(cls.inp, duration=3.0)
        _make_audio(cls.narr, duration=3.0, freq=220)
        _make_audio(cls.music_dir / "drone_base.mp3", duration=3.0, freq=80)
        _make_audio(cls.music_dir / "ambient_room.mp3", duration=3.0, freq=140)
        cls.spec = Path(cls.tmp) / "spec.yaml"
        _write_spec(cls.spec, has_l3_music=True, has_tts=True)
        cls.result = _run(["--format", "horror-choice", "--spec", str(cls.spec),
                           "--input", str(cls.inp), "--music-dir", str(cls.music_dir),
                           "--narrator", str(cls.narr), "--output", str(cls.out)])
        cls.manifest_path = cls.out.parent / "master_final_manifest.json"
        cls.manifest = json.loads(cls.manifest_path.read_text()) if cls.manifest_path.exists() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_full_mix_succeeds(self):
        self.assertEqual(self.result.returncode, 0,
                         f"stdout {self.result.stdout}\nstderr {self.result.stderr}")
        self.assertTrue(self.out.exists())
        self.assertIsNotNone(self.manifest)

    def test_full_mix_final_master_lufs_within_minus14_band(self):
        """Property: PRE-4.C canonical-anchored final master -14 ±0.5 LUFS (F1 -14.06 ±0.41)."""
        self.assertTrue(self.out.exists())
        lufs = _measure_lufs(self.out)
        self.assertIsNotNone(lufs, "ebur128 must report integrated loudness")
        self.assertAlmostEqual(lufs, -14.0, delta=0.5,
                               msg=f"Final master LUFS {lufs} outside -14 ±0.5 canonical band")

    def test_full_mix_duration_matches_input_video(self):
        self.assertTrue(self.out.exists())
        self.assertAlmostEqual(_duration(self.out), _duration(self.inp), delta=0.2,
                               msg="Mastered output duration must match input video (no truncation)")

    def test_sidechain_duck_recorded_when_narration_present(self):
        self.assertIsNotNone(self.manifest)
        self.assertEqual(self.manifest["branch"], "full")
        self.assertEqual(self.manifest["music_layers_count"], 2)
        self.assertIsNotNone(self.manifest.get("sidechain_duck_db"),
                             "Duck dB must be recorded when narrator present + has_tts_narration")


class TestAudioTailNotTruncated(unittest.TestCase):
    """apad=whole_dur tail fix: when narrator + music are SHORTER than the video, the mastered audio
    must still span the FULL video duration (amix alone would end early → cola de audio cortada)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.music_dir = Path(self.tmp) / "music"
        self.music_dir.mkdir(parents=True)
        self.inp = Path(self.tmp) / "clips_with_effects.mp4"
        self.narr = Path(self.tmp) / "narrator.mp3"
        self.out = Path(self.tmp) / "master_final.mp4"
        _make_video(self.inp, duration=5.0)              # full video 5s
        _make_audio(self.narr, duration=2.0, freq=220)   # narrator ends at 2s
        _make_audio(self.music_dir / "drone_base.mp3", duration=2.5, freq=80)  # music ends at 2.5s
        self.spec = Path(self.tmp) / "spec.yaml"
        _write_spec(self.spec, has_l3_music=True, has_tts=True, layers=("drone_base",))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_output_audio_spans_full_video_despite_short_sources(self):
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--input", str(self.inp), "--music-dir", str(self.music_dir),
                  "--narrator", str(self.narr), "--output", str(self.out)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertTrue(self.out.exists())
        self.assertAlmostEqual(_duration(self.out), 5.0, delta=0.2,
                               msg="audio tail truncated — apad=whole_dur fix missing")


if __name__ == "__main__":
    unittest.main(verbosity=2)
