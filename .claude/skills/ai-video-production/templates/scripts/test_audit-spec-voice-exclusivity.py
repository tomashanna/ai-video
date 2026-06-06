"""test_audit-spec-voice-exclusivity.py — VOICE EXCLUSIVITY LAW (Capa A) companion test (HR#26).

Adversarial + synthetic coverage of audit-spec-voice-exclusivity.py AND the L3 assembly assertion
in cp5b_run_all.py.

Core adversarial cases (per the V7 brief):
  - MUST FAIL on the reconstructed v2 cue timings: a narrator window and a character (Dario) window
    OVERLAPPING in time (two voices at once) — the bug the law exists to catch.
  - MUST PASS on the v3 layout: the same voices separated so no two voices ever sound at once and
    every narrator↔character handoff keeps the 0.30s floor.
Plus minimal synthetic fixtures: CLI/capability/buffer-floor/same-speaker-abut/dry-run, and direct
unit tests of the L3 assert_voice_exclusivity() shift-or-abort logic.
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-voice-exclusivity.py"
DRIVER = Path(__file__).parent / "cp5b_run_all.py"
PY = sys.executable


def _run(args):
    return subprocess.run([PY, str(SCRIPT)] + args, capture_output=True, text=True)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── synthetic SPEC builders ───────────────────────────────────────────────────

_CAPS = ('video_capabilities:\n'
         '  has_tts_narration: true\n'
         '  format_type: "interactive_choice"\n')


def _spec_yaml(narration, has_tts=True, omit_caps=False):
    caps = "" if omit_caps else (_CAPS if has_tts else
                                 'video_capabilities:\n  has_tts_narration: false\n')
    lines = ['schema_version: "v11.1"', caps.rstrip("\n"), "narration_script:"]
    for seg, spk, ts0, text in narration:
        lines += [f"  - segment_id: {seg}", f"    speaker: {spk}",
                  f"    timestamp_intent_s: [{ts0}, {ts0 + 1}]",
                  f'    text_canonical: "{text}"']
    return "\n".join(lines) + "\n"


def _manifest(entries):
    """entries: (segment_id, speaker, duration_s, shot_id_anchor)."""
    return json.dumps([{"segment_id": s, "speaker": sp, "duration_s": d, "shot_id_anchor": sh,
                        "voice_id": "x", "file": f"assets/tts/{s}.mp3"} for s, sp, d, sh in entries])


def _spec_with_shots(narration, shot_starts):
    """SPEC whose narration_script gives per-segment timestamp_intent_s = the shot start (tts-mode
    start source when no --atomic-dir)."""
    lines = ['schema_version: "v11.1"', _CAPS.rstrip("\n"), "shot_list:"]
    for sh in shot_starts:
        lines.append(f"  - shot_id: {sh}")
    lines.append("narration_script:")
    for seg, spk, ts0, sh in narration:
        lines += [f"  - segment_id: {seg}", f"    speaker: {spk}",
                  f"    timestamp_intent_s: [{ts0}, {ts0 + 1}]",
                  f"    shot_id_anchor: {sh}", f'    text_canonical: "x x x"']
    return "\n".join(lines) + "\n"


class TestSpecMode(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.spec = self.tmp / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_requires_format(self):
        self.spec.write_text(_spec_yaml([("narrator_hook", "narrator", 1.0, "uno dos tres")]))
        r = _run(["--mode", "spec", "--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("format", r.stderr.lower())

    def test_bug9_missing_caps(self):
        self.spec.write_text(_spec_yaml([("a", "narrator", 1.0, "uno")], omit_caps=True))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 2)

    def test_not_applicable_no_tts(self):
        self.spec.write_text(_spec_yaml([("a", "narrator", 1.0, "uno")], has_tts=False))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout.lower())

    def test_v2_hook_narrator_plus_character_overlap_FAILS(self):
        # Reconstructed v2 bug: narrator (12w @165WPM ≈ 4.36s from 1.8 → ends ~6.16s) and a CHARACTER
        # window starting at 3.2s OVERLAP → two voices at once. MUST FAIL.
        narr = [
            ("narrator_hook", "narrator", 1.8,
             "El ultimo tren ya paso Elige a tu companero Dario o Tobias"),  # 12 words
            ("char_lure", "char_b", 3.2, "Ven conmigo abajo hace frio"),    # starts inside narrator
        ]
        self.spec.write_text(_spec_yaml(narr))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"v2 overlap must FAIL.\n{r.stdout}")
        d = json.loads(r.stdout)
        self.assertEqual(d["overall_status"], "fail")
        kinds = {c["kind"] for c in d["conflicts"]}
        self.assertIn("overlap", kinds)

    def test_v3_layout_no_overlap_PASSES(self):
        # v3: narrator finishes, THEN the character speaks with a >=0.3s handoff gap. No overlap.
        narr = [
            ("narrator_hook", "narrator", 1.8, "uno dos tres"),       # ~1.09s → ends ~2.89s
            ("char_dario", "char_a", 4.0, "cuatro cinco seis"),       # starts 4.0 > 2.89 + 0.3
        ]
        self.spec.write_text(_spec_yaml(narr))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"separated layout must PASS.\n{r.stdout}")
        self.assertIn('"pass"', r.stdout)

    def test_same_speaker_abut_is_not_a_buffer_violation(self):
        # Two consecutive NARRATOR segments abutting (gap 0.1s) = continuous narration, ONE voice.
        # The 0.3s floor applies only to DIFFERENT-speaker handoffs → this must PASS.
        narr = [("n1", "narrator", 0.0, "uno"), ("n2", "narrator", 0.42, "dos")]  # ~0.36s each, gap ~0.06
        self.spec.write_text(_spec_yaml(narr))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"same-speaker abut must PASS.\n{r.stdout}")

    def test_diff_speaker_under_floor_FAILS(self):
        narr = [("n1", "narrator", 0.0, "uno"), ("c1", "char_a", 0.45, "dos")]  # gap ~0.09 < 0.30
        self.spec.write_text(_spec_yaml(narr))
        r = _run(["--mode", "spec", "--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"diff-speaker under-floor must FAIL.\n{r.stdout}")
        self.assertIn("buffer_under_floor", r.stdout)


class TestTtsMode(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_tts_v2_overlap_FAILS(self):
        # REAL durations: narrator 5.2s from shot_01 (start 0 → 0.1..5.3), Dario 2.7s from shot_01
        #   at the SAME shot start (0 → 0.45..3.15) → overlaps the narrator. MUST FAIL.
        mf = self.tmp / "manifest.json"
        mf.write_text(_manifest([("narrator_hook", "narrator", 5.2, "shot_01"),
                                 ("dario_lure", "char_a", 2.7, "shot_01")]))
        spec = self.tmp / "spec.yaml"
        spec.write_text(_spec_with_shots(
            [("narrator_hook", "narrator", 0.0, "shot_01"), ("dario_lure", "char_a", 0.0, "shot_01")],
            ["shot_01"]))
        r = _run(["--mode", "tts", "--manifest", str(mf), "--spec", str(spec)])
        self.assertEqual(r.returncode, 1, f"tts v2 overlap must FAIL.\n{r.stdout}")
        self.assertIn("overlap", r.stdout)

    def test_tts_v3_separated_PASSES(self):
        # v3: narrator on shot_01 (start 0), Dario on a LATER shot start (10) → no overlap.
        mf = self.tmp / "manifest.json"
        mf.write_text(_manifest([("narrator_hook", "narrator", 5.2, "shot_01"),
                                 ("dario_rule", "char_a", 2.7, "shot_05")]))
        spec = self.tmp / "spec.yaml"
        spec.write_text(_spec_with_shots(
            [("narrator_hook", "narrator", 0.0, "shot_01"), ("dario_rule", "char_a", 10.0, "shot_05")],
            ["shot_01", "shot_05"]))
        r = _run(["--mode", "tts", "--manifest", str(mf), "--spec", str(spec)])
        self.assertEqual(r.returncode, 0, f"tts v3 separated must PASS.\n{r.stdout}")
        self.assertIn('"pass"', r.stdout)

    def test_tts_exclude_segment_removes_overlap(self):
        # The v2-overlapping char window, but EXCLUDED (a fix-pack muted it in the cut) → PASS.
        mf = self.tmp / "manifest.json"
        mf.write_text(_manifest([("narrator_hook", "narrator", 5.2, "shot_01"),
                                 ("tobias_lure", "char_b", 2.7, "shot_01")]))
        spec = self.tmp / "spec.yaml"
        spec.write_text(_spec_with_shots(
            [("narrator_hook", "narrator", 0.0, "shot_01"), ("tobias_lure", "char_b", 0.0, "shot_01")],
            ["shot_01"]))
        r = _run(["--mode", "tts", "--manifest", str(mf), "--spec", str(spec),
                  "--exclude-segments", "tobias_lure"])
        self.assertEqual(r.returncode, 0, f"excluding the muted voice must PASS.\n{r.stdout}")


class TestL3Assertion(unittest.TestCase):
    """Direct unit tests de cp5b_run_all.assert_voice_exclusivity (L3 guard del DRIVER global).

    El driver cp5b_run_all.py es PER-PROYECTO (V7 lo hardcodea — no se porta a Capa A;
    el port canónico al template es la variante per-clip `assert_voice_exclusivity_in_clip`
    en build_clip_atomic.py, cubierta por test_build_clip_atomic.py). Esta clase corre
    SOLO cuando el test vive copiado en un proyecto que tiene su driver; en el template
    se skippea limpio en vez de FAILear por archivo ausente.
    """

    @classmethod
    def setUpClass(cls):
        if not DRIVER.exists():
            raise unittest.SkipTest(
                "cp5b_run_all.py ausente (template) — L3 per-clip cubierto por "
                "test_build_clip_atomic.py; este test corre en proyectos con driver propio"
            )
        cls.mod = _load(DRIVER, "cp5b_driver")

    def test_passes_when_separated(self):
        voices = [
            {"seg": "n1", "speaker": "narrator", "t0": 0.1, "dur": 5.0, "shot": "shot_01", "priority": 0},
            {"seg": "d1", "speaker": "char_a", "t0": 10.45, "dur": 2.0, "shot": "shot_05", "priority": 2},
        ]
        bounds = {"shot_01": (0.0, 6.0), "shot_05": (10.0, 14.0)}
        out = self.mod.assert_voice_exclusivity(voices, bounds)
        self.assertEqual({v["seg"]: v["t0"] for v in out}, {"n1": 0.1, "d1": 10.45})

    def test_shifts_dialog_off_narrator_within_shot(self):
        # Dario at 10.45 overlaps a SHORT adjacent narrator (10.1..10.7). Dario (prio 2) cedes and
        #   shifts LATER to narrator_end+floor = 11.0 — a +0.55s shift (≤1s) inside shot_05.
        voices = [
            {"seg": "n_adj", "speaker": "narrator", "t0": 10.1, "dur": 0.6, "shot": "shot_05", "priority": 1},
            {"seg": "d1", "speaker": "char_a", "t0": 10.45, "dur": 2.0, "shot": "shot_05", "priority": 2},
        ]
        bounds = {"shot_05": (10.0, 14.5)}
        out = self.mod.assert_voice_exclusivity(voices, bounds)
        d1 = next(v for v in out if v["seg"] == "d1")
        # narrator ends 10.7 → dialog moved to 10.7 + 0.30 = 11.0 (a 0.55s shift, inside shot)
        self.assertAlmostEqual(d1["t0"], 11.0, places=2)
        self.assertGreaterEqual(d1["t0"] - (10.1 + 0.6), self.mod.VOICE_BUFFER_FLOOR_S - 1e-6)
        self.assertLessEqual(abs(d1["t0"] - 10.45), self.mod.VOICE_SHIFT_MAX_S + 1e-6)

    def test_hook_narrator_keeps_priority(self):
        # In the hook, narrator goes FIRST (priority 0). The character cedes. Narrator is SHORT (2.0s)
        #   so the lure can shift to narrator_end+floor = 2.4 — a +0.6s shift (≤1s) inside the shot.
        voices = [
            {"seg": "n_hook", "speaker": "narrator", "t0": 0.1, "dur": 2.0, "shot": "shot_01", "priority": 0},
            {"seg": "lure", "speaker": "char_b", "t0": 1.8, "dur": 1.5, "shot": "shot_01", "priority": 2},
        ]
        bounds = {"shot_01": (0.0, 8.0)}
        out = self.mod.assert_voice_exclusivity(voices, bounds)
        n = next(v for v in out if v["seg"] == "n_hook")
        lure = next(v for v in out if v["seg"] == "lure")
        self.assertEqual(n["t0"], 0.1, "narrator must NOT move in the hook (priority 0)")
        self.assertGreaterEqual(lure["t0"], n["t0"] + n["dur"] + self.mod.VOICE_BUFFER_FLOOR_S - 1e-6)
        self.assertLessEqual(abs(lure["t0"] - 1.8), self.mod.VOICE_SHIFT_MAX_S + 1e-6)

    def test_aborts_when_cannot_fit_within_1s(self):
        # Dialog overlaps narrator and the ONLY non-colliding slot needs a >1s shift → ABORT (SystemExit).
        voices = [
            {"seg": "n", "speaker": "narrator", "t0": 0.1, "dur": 5.0, "shot": "shot_x", "priority": 1},
            {"seg": "d", "speaker": "char_a", "t0": 0.5, "dur": 2.0, "shot": "shot_x", "priority": 2},
        ]
        bounds = {"shot_x": (0.0, 7.0)}   # to clear the narrator (ends 5.1) dialog needs t0>=5.4 = +4.9s
        with self.assertRaises(SystemExit):
            self.mod.assert_voice_exclusivity(voices, bounds)

    def test_aborts_on_same_speaker_overlap(self):
        voices = [
            {"seg": "n1", "speaker": "narrator", "t0": 0.0, "dur": 5.0, "shot": "shot_a", "priority": 1},
            {"seg": "n2", "speaker": "narrator", "t0": 2.0, "dur": 2.0, "shot": "shot_b", "priority": 1},
        ]
        bounds = {"shot_a": (0.0, 6.0), "shot_b": (2.0, 5.0)}
        with self.assertRaises(SystemExit):
            self.mod.assert_voice_exclusivity(voices, bounds)


if __name__ == "__main__":
    unittest.main(verbosity=2)
