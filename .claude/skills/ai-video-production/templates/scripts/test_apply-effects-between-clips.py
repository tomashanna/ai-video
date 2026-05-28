"""
test_apply-effects-between-clips.py — adversarial tests for Paso 4.4 apply-effects-between-clips.py.

Per CLAUDE.md Hard Rule #26: every new script ships with test_*.py companion.
TDD: written FIRST (RED), script implemented after (GREEN).

9 tests (4 capability-aware/agnostic + 5 properties PRE-4.B #9-#14):
1. --format required (no silent assumption)
2. --format horror-choice succeeds on existing concat (dry-run)
3. --format arbitrary proves agnostic (dry-run)
4. has_layer_2_effects=false → passthrough concat (real copy)
5. effects applied at correct boundaries per SPEC shot_list (property #9)
6. xfade duration matches recipe duration_s (property #10)
7. variety ≥3 unique transition types used (property #11, F1 PARTIAL)
8. audio sting volume within recipe band ±3dB (property #14, F1 PARTIAL)
9. pre/post visual continuity — xfade boundary blends, no hard jump (property #13, F1 PARTIAL)

Fixtures: synthetic ffmpeg-lavfi clips + synthetic recipe JSONs + synthetic sting mp3s.
NO heavy py deps (no numpy/whisper). NO golden V4 reference (V4 read-only input data only,
NOT quality reference — Tomás canonical principle).

Architecture: PRE-4.E (PIPELINE §13.9.1 LAYER 2) — xfade at clip boundaries from atomic
clips (V4 empirical cp5-layer2-concat.py reads N atomic clips, chains xfade w/ cumulative
offsets). clips_concat_only.mp4 (4.2 output) used for passthrough branch. Stings overlaid
per recipe (NO pre-rendered effect mp4s).

Authority: Paso 4.4 build + PRE-4.B coverage + PRE-4.E xfade-post-concat + Pattern 7 capability matrix.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parent / "apply-effects-between-clips.py"

FIXTURE_FPS = 30
FIXTURE_SR = 48000
FIXTURE_DUR = 1.0


def _run(args, env_overrides=None):
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
    return subprocess.run([sys.executable, str(SCRIPT)] + args,
                          capture_output=True, text=True, env=env)


def _make_clip(path, duration=FIXTURE_DUR, fps=FIXTURE_FPS, color="red"):
    """Synthetic atomic clip: solid color video + sine audio, 1080x1920 (project target)."""
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={color}:s=1080x1920:d={duration}:r={fps}",
        "-f", "lavfi", "-i", f"sine=frequency=440:duration={duration}:sample_rate={FIXTURE_SR}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", str(FIXTURE_SR),
        "-t", str(duration),
        str(path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _make_sting(path, duration=0.4):
    """Synthetic audio sting (short sine burst)."""
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"sine=frequency=880:duration={duration}:sample_rate={FIXTURE_SR}",
        "-c:a", "libmp3lame", "-t", str(duration), str(path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def _avg_rgb_at(path, t):
    """Extract frame at time t, scale to 1x1, return (R,G,B) average pixel via rawvideo."""
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(path),
         "-vframes", "1", "-vf", "scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True,
    )
    data = r.stdout
    if len(data) < 3:
        return None
    return (data[0], data[1], data[2])


def _make_recipe(effects_dir, rid, duration_s, xfade_transition,
                 sting_path=None, sting_volume=None, xfade_fidelity=None):
    """Write a synthetic recipe JSON mirroring effects-library schema (+ explicit xfade_transition)."""
    recipe = {
        "id": rid,
        "type": "transition",
        "duration_s": duration_s,
        "xfade_transition": xfade_transition,
        "audio_sting_path": str(sting_path) if sting_path else None,
        "audio_sting_volume": sting_volume,
    }
    if xfade_fidelity is not None:
        recipe["xfade_fidelity"] = xfade_fidelity
    (Path(effects_dir) / f"{rid}.json").write_text(json.dumps(recipe), encoding="utf-8")


def _write_spec(path, shots_with_trans, has_layer_2=True, has_captions=True,
                fmt="interactive_choice", omit_capabilities=False):
    """Write minimal SPEC yaml. shots_with_trans = list of (shot_id, transition_out_or_None)."""
    shot_lines = []
    for sid, tout in shots_with_trans:
        shot_lines.append(f"  - shot_id: {sid}")
        if tout:
            shot_lines.append(f"    transition_out: {tout}")
    shots_block = "\n".join(shot_lines)
    caps_block = "" if omit_capabilities else f"""video_capabilities:
  source_clips_origin: "ai_generated"
  has_ai_generated_clips: true
  has_tts_narration: true
  has_sfx_layer: true
  has_captions_baked: {str(has_captions).lower()}
  has_layer_2_effects: {str(has_layer_2).lower()}
  has_layer_3_music: true
  has_layer_4_ui: true
  format_type: "{fmt}"
"""
    content = f"""schema_version: "v11.1"
{caps_block}shot_list:
{shots_block}
"""
    Path(path).write_text(content, encoding="utf-8")


class TestEffectsCLI(unittest.TestCase):
    """CLI + capability-aware + agnostic (dry-run, no heavy fixtures)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.fx = Path(self.tmp) / "fx"
        self.fx.mkdir()
        _make_recipe(self.fx, "xfade-fade-05", 0.5, "fade")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero_with_clear_error(self):
        _write_spec(self.spec, [("shot_01", "xfade-fade-05"), ("shot_02", None)])
        result = _run(["--spec", str(self.spec), "--effects-dir", str(self.fx), "--dry-run"])
        self.assertNotEqual(result.returncode, 0,
                            f"Expected non-zero without --format. stderr: {result.stderr}")
        self.assertIn("format", result.stderr.lower())

    def test_invocation_with_horror_choice_succeeds_dry_run(self):
        _write_spec(self.spec, [("shot_01", "xfade-fade-05"), ("shot_02", None)])
        result = _run(["--format", "horror-choice", "--spec", str(self.spec),
                       "--effects-dir", str(self.fx), "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("effects", result.stdout.lower(),
                      "horror-choice w/ has_layer_2_effects=true should resolve effects branch")

    def test_invocation_with_arbitrary_format_succeeds_proves_agnostic(self):
        _write_spec(self.spec, [("shot_01", "xfade-fade-05"), ("shot_02", None)], fmt="tutorial")
        result = _run(["--format", "tutorial-test-stub", "--spec", str(self.spec),
                       "--effects-dir", str(self.fx), "--dry-run"])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 arbitrary format. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn("tutorial-test-stub", result.stdout,
                      "Arbitrary format must appear in resolved output (agnostic proof)")


class TestPassthroughBranch(unittest.TestCase):
    """has_layer_2_effects=false → passthrough copies concat input to output (Pattern 7)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.inp = Path(self.tmp) / "clips_concat_only.mp4"
        self.out = Path(self.tmp) / "clips_with_effects.mp4"
        _make_clip(self.inp, duration=2.0, color="blue")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_with_layer_2_disabled_passes_through_concat(self):
        _write_spec(self.spec, [("shot_01", None), ("shot_02", None)], has_layer_2=False)
        result = _run(["--format", "compilation-no-fx", "--spec", str(self.spec),
                       "--input", str(self.inp), "--output", str(self.out)])
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0 passthrough. stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertTrue(self.out.exists(), "Passthrough must produce output file")
        self.assertAlmostEqual(_duration(self.out), _duration(self.inp), delta=0.15,
                               msg="Passthrough output duration must equal input (copy, no effects)")
        self.assertIn("passthrough", result.stdout.lower(),
                      "Output must report passthrough branch taken")


class TestEffectsProperties(unittest.TestCase):
    """Property tests #9-#14 — real effects application of synthetic fixtures."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.clips_dir = Path(cls.tmp) / "clips-atomic"
        cls.out_dir = Path(cls.tmp) / "concat"
        cls.fx = Path(cls.tmp) / "fx"
        for d in (cls.clips_dir, cls.out_dir, cls.fx):
            d.mkdir(parents=True)
        # 5 synthetic atomic clips (4 boundaries → variety ≥3 possible)
        colors = ["red", "green", "blue", "yellow", "magenta"]
        cls.shots = [f"shot_0{i}" for i in range(1, 6)]
        for sid, color in zip(cls.shots, colors):
            _make_clip(cls.clips_dir / f"{sid}_atomic.mp4", color=color)
        # synthetic stings
        cls.whoosh = cls.fx / "whoosh.mp3"
        cls.flash_sting = cls.fx / "flash.mp3"
        cls.glitch_sting = cls.fx / "glitch.mp3"
        for s in (cls.whoosh, cls.flash_sting, cls.glitch_sting):
            _make_sting(s)
        # 4 recipes (4 unique transition ids → variety)
        _make_recipe(cls.fx, "xfade-fade-05", 0.5, "fade")
        _make_recipe(cls.fx, "flash-impact", 0.3, "fadewhite",
                     sting_path=cls.flash_sting, sting_volume=0.45)
        _make_recipe(cls.fx, "glitch", 0.3, "dissolve",
                     sting_path=cls.glitch_sting, sting_volume=0.40)
        _make_recipe(cls.fx, "hardcut-whoosh", 0.0, "hardcut",
                     sting_path=cls.whoosh, sting_volume=0.55)
        # SPEC: shot_01→fade, shot_02→flash, shot_03→glitch, shot_04→hardcut, shot_05 last
        cls.spec = Path(cls.tmp) / "spec.yaml"
        _write_spec(cls.spec, [
            ("shot_01", "xfade-fade-05"),
            ("shot_02", "flash-impact"),
            ("shot_03", "glitch"),
            ("shot_04", "hardcut-whoosh"),
            ("shot_05", None),
        ])
        cls.output = cls.out_dir / "clips_with_effects.mp4"
        cls.result = _run(["--format", "horror-choice", "--spec", str(cls.spec),
                           "--clips-dir", str(cls.clips_dir), "--output", str(cls.output),
                           "--effects-dir", str(cls.fx)])
        cls.manifest_path = cls.output.parent / "clips_with_effects_manifest.json"
        cls.manifest = None
        if cls.manifest_path.exists():
            cls.manifest = json.loads(cls.manifest_path.read_text())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_effects_run_succeeds_and_output_exists(self):
        self.assertEqual(self.result.returncode, 0,
                         f"Effects run must exit 0. stdout: {self.result.stdout}\nstderr: {self.result.stderr}")
        self.assertTrue(self.output.exists(), f"Output mp4 must exist: {self.output}")
        self.assertIsNotNone(self.manifest, "Manifest JSON must be written")

    def test_effects_applied_at_correct_boundaries_per_spec_shot_list(self):
        """Property #9: one transition per boundary, in SPEC shot_list order."""
        self.assertIsNotNone(self.manifest)
        trans = self.manifest["transitions"]
        self.assertEqual(len(trans), 4, "Must have 4 boundaries for 5 shots")
        pairs = [(t["from_shot"], t["to_shot"]) for t in trans]
        self.assertEqual(pairs, [("shot_01", "shot_02"), ("shot_02", "shot_03"),
                                 ("shot_03", "shot_04"), ("shot_04", "shot_05")],
                         "Boundaries must follow SPEC shot_list order")

    def test_xfade_duration_matches_recipe(self):
        """Property #10: each boundary duration_s == recipe duration_s."""
        self.assertIsNotNone(self.manifest)
        by_id = {t["transition_id"]: t for t in self.manifest["transitions"]}
        self.assertAlmostEqual(by_id["xfade-fade-05"]["duration_s"], 0.5, delta=0.001)
        self.assertAlmostEqual(by_id["flash-impact"]["duration_s"], 0.3, delta=0.001)
        self.assertAlmostEqual(by_id["glitch"]["duration_s"], 0.3, delta=0.001)
        self.assertAlmostEqual(by_id["hardcut-whoosh"]["duration_s"], 0.0, delta=0.001)

    def test_variety_at_least_3_unique_transition_types_used(self):
        """Property #11 (F1 PARTIAL): ≥3 unique transition types across boundaries."""
        self.assertIsNotNone(self.manifest)
        unique = {t["transition_id"] for t in self.manifest["transitions"]}
        self.assertGreaterEqual(len(unique), 3,
                                f"Need ≥3 unique transition types, got {unique}")

    def test_audio_sting_volume_within_recipe_band(self):
        """Property #14 (F1 PARTIAL): applied sting volume within recipe band ±3dB."""
        self.assertIsNotNone(self.manifest)
        recipe_vols = {"flash-impact": 0.45, "glitch": 0.40, "hardcut-whoosh": 0.55}
        stung = [t for t in self.manifest["transitions"] if t.get("sting_volume") is not None]
        self.assertGreaterEqual(len(stung), 3, "≥3 boundaries should carry a sting")
        for t in stung:
            expected = recipe_vols[t["transition_id"]]
            lo, hi = expected * (10 ** (-3 / 20)), expected * (10 ** (3 / 20))
            self.assertTrue(lo <= t["sting_volume"] <= hi,
                            f"{t['transition_id']} sting volume {t['sting_volume']} "
                            f"outside ±3dB band [{lo:.3f},{hi:.3f}] of recipe {expected}")

    def test_pre_post_visual_continuity_frame_diff_within_canonical(self):
        """Property #13 (F1 PARTIAL avg 37, p75 42): xfade boundary blends (continuity),
        NOT a hard jump. Synthetic proxy: midpoint frame of first (fade) boundary is a
        genuine red→green blend (both channels substantial), not pure either side."""
        self.assertTrue(self.output.exists())
        # First boundary (shot_01 red → shot_02 green) is a 0.5s fade.
        # shot_01 dur=1.0, xfade offset=0.5 → fade window 0.5-1.0s, midpoint 0.75s.
        rgb = _avg_rgb_at(self.output, 0.75)
        self.assertIsNotNone(rgb, "Frame extraction at boundary midpoint must succeed")
        r, g, b = rgb
        self.assertGreater(r, 25, f"Red channel should persist mid-fade (blend), got {rgb}")
        self.assertGreater(g, 25, f"Green channel should appear mid-fade (blend), got {rgb}")


class TestAdapterIntegration(unittest.TestCase):
    """PRE-4.J integration: legacy transitions[] via adapter + approximate-fidelity WARNING."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.clips_dir = Path(self.tmp) / "clips-atomic"
        self.out_dir = Path(self.tmp) / "concat"
        self.fx = Path(self.tmp) / "fx"
        for d in (self.clips_dir, self.out_dir, self.fx):
            d.mkdir(parents=True)
        for i, c in enumerate(["red", "green"], start=1):
            _make_clip(self.clips_dir / f"shot_0{i}_atomic.mp4", color=c)
        self.spec = Path(self.tmp) / "spec.yaml"
        self.output = self.out_dir / "clips_with_effects.mp4"
        self.manifest_path = self.output.parent / "clips_with_effects_manifest.json"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_legacy_transitions_array_via_adapter(self):
        """Legacy top-level transitions[] (V4 form) normalized to per-shot via adapter, then applied."""
        _make_recipe(self.fx, "cross-fade-0.5s", 0.5, "fade")
        self.spec.write_text(
            'schema_version: "v11.1"\n'
            'video_capabilities:\n'
            '  source_clips_origin: "ai_generated"\n'
            '  has_layer_2_effects: true\n'
            'shot_list:\n'
            '  - shot_id: shot_01\n'
            '  - shot_id: shot_02\n'
            'transitions:\n'
            '  - from_shot_id: shot_01\n'
            '    to_shot_id: shot_02\n'
            '    transition_type: cross_fade_0.5s\n',
            encoding="utf-8")
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--clips-dir", str(self.clips_dir), "--output", str(self.output),
                  "--effects-dir", str(self.fx)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertTrue(self.manifest_path.exists(), "Manifest must be written")
        m = json.loads(self.manifest_path.read_text())
        self.assertEqual(len(m["transitions"]), 1, "Legacy array → 1 boundary")
        self.assertEqual(m["transitions"][0]["transition_id"], "cross-fade-0.5s",
                         "Adapter must map legacy transition_type to canonical recipe id")

    def test_approximate_recipe_emits_warning(self):
        """approximate-fidelity recipe used in real run emits WARNING (Option D)."""
        _make_recipe(self.fx, "black-screen-0.3s", 0.3, "fadeblack", xfade_fidelity="approximate")
        self.spec.write_text(
            'schema_version: "v11.1"\n'
            'video_capabilities:\n'
            '  source_clips_origin: "ai_generated"\n'
            '  has_layer_2_effects: true\n'
            'shot_list:\n'
            '  - shot_id: shot_01\n'
            '    transition_out: black-screen-0.3s\n'
            '  - shot_id: shot_02\n',
            encoding="utf-8")
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--clips-dir", str(self.clips_dir), "--output", str(self.output),
                  "--effects-dir", str(self.fx)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("approximate", r.stderr.lower(),
                      "approximate-fidelity recipe must emit WARNING to stderr in real run")


if __name__ == "__main__":
    unittest.main(verbosity=2)
