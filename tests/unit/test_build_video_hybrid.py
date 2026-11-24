"""
test_build-video-hybrid.py — adversarial tests for Paso 4.1 build-video-hybrid.py (orchestrator final).

Per Hard Rule #26: companion test sidecar. TDD: written FIRST (RED).

Chains 4.2 → 4.4 → 4.3 → Layer 4 UI overlay + fps normalization → emit + 8 pre-render gates.
11 tests (CLI/agnostic + capability branches + fps + Layer 4 + gates + Bug #9):
1. --format required
2. horror-choice end-to-end succeeds (real chain, setUpClass)
3. arbitrary format proves agnostic (dry-run)
4. all 8 pre-render gates pass → exit 0 (from setUpClass)
5. output fps == target_fps 30 (from setUpClass)
6. target_fps 24 normalizes output to 24
7. Layer 4 disabled skips UI overlay (manifest layer_4_applied false)
8. pre-render gate failure (bad duration_intent) → nonzero + report
9. video_capabilities missing → Bug #9 exit 2
10. target_fps missing → defaults 30 + WARNING (dry-run)
11. final master LUFS within -14 ±0.5 (gate 2 canonical-anchored, from setUpClass)

Synthetic fixtures via ffmpeg lavfi. Uses REAL Capa A effects-library (hard-cut-with-whoosh recipe
+ whoosh sting). NO numpy/whisper. NO golden V4.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pytest

pytestmark = pytest.mark.ffmpeg  # synthesises fixtures with ffmpeg lavfi

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/build/build_video_hybrid.py"
SR = 48000


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _make_clip(path, duration=1.0, fps=30, color="red"):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=480x854:d={duration}:r={fps}",
        "-f", "lavfi", "-i", f"sine=frequency=300:duration={duration}:sample_rate={SR}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", str(SR),
        "-t", str(duration), str(path),
    ], check=True, capture_output=True)


def _make_audio(path, duration=3.0, freq=110):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={duration}:sample_rate={SR}",
        "-c:a", "libmp3lame", "-t", str(duration), str(path),
    ], check=True, capture_output=True)


def _probe(path, stream, entry):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream,
                        "-show_entries", f"stream={entry}", "-of",
                        "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True)
    return r.stdout.strip()


def _duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def _build_project(root, has_l4=True, target_fps=30, duration_intent=3.0,
                   mix_target="lufs_-14", omit_caps=False, omit_target_fps=False,
                   fmt="interactive_choice", clip_fps=30):
    """Create synthetic project dir: assets/clips-atomic + music + narration + SPEC."""
    root = Path(root)
    clips = root / "assets/clips-atomic"
    music = root / "assets/music"
    narr_dir = root / "assets/narration"
    for d in (clips, music, narr_dir):
        d.mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(["red", "green", "blue"], start=1):
        _make_clip(clips / f"shot_0{i}_atomic.mp4", duration=1.0, fps=clip_fps, color=c)
    _make_audio(music / "drone_base.mp3", duration=3.0, freq=80)
    _make_audio(music / "ambient_room.mp3", duration=3.0, freq=140)
    _make_audio(narr_dir / "narrator_master.mp3", duration=3.0, freq=220)

    caps = ""
    if not omit_caps:
        tfps = "" if omit_target_fps else f"  target_fps: {target_fps}\n"
        caps = (
            "video_capabilities:\n"
            '  source_clips_origin: "ai_generated"\n'
            "  has_ai_generated_clips: true\n"
            "  has_tts_narration: true\n"
            f'  audio_mix_target: "{mix_target}"\n'
            "  has_captions_baked: false\n"
            "  has_layer_2_effects: true\n"
            "  has_layer_3_music: true\n"
            f"  has_layer_4_ui: {str(has_l4).lower()}\n"
            f'  format_type: "{fmt}"\n'
            f"  duration_intent_s: {duration_intent}\n"
            f"{tfps}"
            '  output_resolution: "1080x1920"\n'
        )
    spec = root / "spec.yaml"
    spec.write_text(
        f'schema_version: "v11.1"\n{caps}'
        "shot_list:\n"
        "  - shot_id: shot_01\n    transition_out: hard-cut-with-whoosh\n"
        "  - shot_id: shot_02\n    transition_out: hard-cut-with-whoosh\n"
        "  - shot_id: shot_03\n"
        "music_continuous_layers:\n"
        "  - layer_id: drone_base\n"
        "  - layer_id: ambient_room\n",
        encoding="utf-8")
    return spec


class TestOrchestratorCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = _build_project(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero(self):
        r = _run(["--spec", str(self.spec), "--project-dir", self.tmp, "--dry-run"])
        self.assertNotEqual(r.returncode, 0, f"stderr: {r.stderr}")
        self.assertIn("format", r.stderr.lower())

    def test_invocation_with_arbitrary_format_proves_agnostic(self):
        r = _run(["--format", "tutorial-stub", "--spec", str(self.spec),
                  "--project-dir", self.tmp, "--dry-run"])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("tutorial-stub", r.stdout, "Arbitrary format in output (agnostic proof)")

    def test_video_capabilities_missing_bug9(self):
        spec = _build_project(self.tmp, omit_caps=True)
        r = _run(["--format", "horror-choice", "--spec", str(spec),
                  "--project-dir", self.tmp, "--dry-run"])
        self.assertEqual(r.returncode, 2, f"Bug #9 expected exit 2. stderr: {r.stderr}")

    def test_target_fps_missing_defaults_30_with_warning(self):
        spec = _build_project(self.tmp, omit_target_fps=True)
        r = _run(["--format", "horror-choice", "--spec", str(spec),
                  "--project-dir", self.tmp, "--dry-run"])
        self.assertEqual(r.returncode, 0, f"stderr {r.stderr}")
        self.assertIn("30", r.stdout, "Default target_fps 30 reported")
        self.assertIn("warning", (r.stdout + r.stderr).lower(), "WARNING when target_fps absent")


class TestOrchestratorE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.spec = _build_project(cls.tmp, has_l4=True, target_fps=30, duration_intent=3.0)
        cls.out_dir = Path(cls.tmp) / "renders"
        cls.result = _run(["--format", "horror-choice", "--spec", str(cls.spec),
                           "--project-dir", cls.tmp, "--output-dir", str(cls.out_dir)])
        cls.draft = cls.out_dir / "draft-v1.mp4"
        cls.gates_path = cls.out_dir / "draft-v1_gates.json"
        cls.manifest_path = cls.out_dir / "draft-v1_manifest.json"
        cls.gates = json.loads(cls.gates_path.read_text()) if cls.gates_path.exists() else None
        cls.manifest = json.loads(cls.manifest_path.read_text()) if cls.manifest_path.exists() else None

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_invocation_with_horror_choice_succeeds_end_to_end(self):
        self.assertEqual(self.result.returncode, 0,
                         f"stdout {self.result.stdout}\nstderr {self.result.stderr}")
        self.assertTrue(self.draft.exists(), "Final draft mp4 must be produced")
        self.assertIsNotNone(self.gates)
        self.assertIsNotNone(self.manifest)

    def test_pre_render_gates_all_pass_returns_zero(self):
        self.assertEqual(self.result.returncode, 0)
        self.assertIsNotNone(self.gates)
        fails = [g for g in self.gates["gates"] if g["status"] == "fail"]
        self.assertEqual(fails, [], f"No gate may fail: {fails}")
        self.assertEqual(len(self.gates["gates"]), 8, "Exactly 8 pre-render gates")

    def test_output_fps_matches_target_30(self):
        self.assertTrue(self.draft.exists())
        self.assertEqual(_probe(self.draft, "v:0", "r_frame_rate"), "30/1")

    def test_final_master_lufs_within_band(self):
        self.assertTrue(self.draft.exists())
        r = subprocess.run(["ffmpeg", "-i", str(self.draft), "-af", "ebur128", "-f", "null", "-"],
                           capture_output=True, text=True)
        m = re.findall(r"I:\s*(-?\d+\.?\d*)\s*LUFS", r.stderr)
        self.assertTrue(m, "ebur128 must report loudness")
        self.assertAlmostEqual(float(m[-1]), -14.0, delta=0.5,
                               msg=f"Final LUFS {m[-1]} outside -14 ±0.5")


class TestOrchestratorBranches(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.out_dir = Path(self.tmp) / "renders"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_target_fps_24_normalizes_output_to_24(self):
        spec = _build_project(self.tmp, target_fps=24, duration_intent=3.0)
        r = _run(["--format", "horror-choice", "--spec", str(spec),
                  "--project-dir", self.tmp, "--output-dir", str(self.out_dir)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        draft = self.out_dir / "draft-v1.mp4"
        self.assertEqual(_probe(draft, "v:0", "r_frame_rate"), "24/1",
                         "Orchestrator must normalize output to target_fps=24")

    def test_layer_4_disabled_skips_ui_overlay(self):
        spec = _build_project(self.tmp, has_l4=False, duration_intent=3.0)
        r = _run(["--format", "horror-choice", "--spec", str(spec),
                  "--project-dir", self.tmp, "--output-dir", str(self.out_dir)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        manifest = json.loads((self.out_dir / "draft-v1_manifest.json").read_text())
        self.assertFalse(manifest["layer_4_applied"],
                         "has_layer_4_ui=false must skip UI overlay")

    def test_pre_render_gate_failure_returns_nonzero_with_report(self):
        spec = _build_project(self.tmp, duration_intent=99.0)  # wrong → gate 1 fails
        r = _run(["--format", "horror-choice", "--spec", str(spec),
                  "--project-dir", self.tmp, "--output-dir", str(self.out_dir)])
        self.assertNotEqual(r.returncode, 0, "Gate failure must return nonzero")
        gates = json.loads((self.out_dir / "draft-v1_gates.json").read_text())
        fails = [g for g in gates["gates"] if g["status"] == "fail"]
        self.assertTrue(any("duration" in g["name"].lower() for g in fails),
                        f"Duration gate must fail: {fails}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
