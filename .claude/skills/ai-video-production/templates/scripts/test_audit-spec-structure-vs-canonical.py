"""test_audit-spec-structure-vs-canonical.py — adversarial tests for the structure/invariant gate (PAUTA-MASTER § 2).

Per Hard Rule #26: companion test sidecar (TDD). CRITICAL — this is a REAL adversarial test, NOT
circular: the centerpiece is a REGRESSION test against the REAL V6 SPEC
(creative-specs/invernadero-turno-riego.yaml) which MUST yield 🔴 FAIL on the § 2 invariant
(Celeste = bueno_aparente is in who_is_there of shots 05/06/07/10/11 = played-path
decision/consequence shots). If the validator does NOT catch that, it is mis-built and the test
fails loudly. The synthetic fixtures (a correct SPEC with bueno_aparente only in hook/counterfactual
→ PASS; one with bueno_aparente in a decision → FAIL) pin the behavior in isolation.

NO heavy py deps (no numpy/whisper). Synthetic SPEC built inline + parsed by the script. The V6
regression test is skipped (not failed) only if the real SPEC file is absent from the repo.

Authority under test: horror-choice-format/PAUTA-MASTER.md § 2 (§§ 2.1/2.2/2.3).
Build 2026-06-01.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-structure-vs-canonical.py"

# The real V6 SPEC. Path is resolved relative to repo root (this test lives in
# .claude/skills/ai-video-production/templates/scripts/ → 5 parents up = repo root).
REPO_ROOT = Path(__file__).resolve().parents[5]
V6_SPEC = REPO_ROOT / "creative-specs" / "invernadero-turno-riego.yaml"


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _caps_block(format_type="interactive_choice", omit=False):
    if omit:
        return ""
    return (
        "video_capabilities:\n"
        f'  format_type: "{format_type}"\n'
        "  has_ai_generated_clips: true\n"
        "  has_tts_narration: true\n"
        "  has_captions_baked: true\n"
        '  audio_mix_target: "lufs_-14"\n'
    )


# A canonical-compliant skeleton: bueno_aparente (char_b) ONLY in hook + counterfactual_opening +
# cliffhanger. char_a (the chosen/scary companion) lives the played path. 2 decisions, each with a
# consequence_A (fatal) and consequence_B (survive). Counterfactual at the opening (ref-09 variant).
CLEAN_SPEC = """schema_version: "v11.1"
{caps}characters:
  - character_id: char_a
    name: Bruno
    role: malo_aparente
  - character_id: char_b
    name: Celeste
    role: bueno_aparente
shot_list:
  - shot_id: shot_01
    section_id: hook
    duration_intent_s: 6.0
    avu_overlay_clip: "countdown-3-2-1-film-leader-with-ticks.mp4"
    scene_context:
      who_is_there: [char_a, char_b, viewer_pov]
    narration_in_this_shot: "Elige a tu compañero. Bruno o Celeste."
  - shot_id: shot_02
    section_id: counterfactual_opening
    duration_intent_s: 8.0
    scene_context:
      who_is_there: [char_b, viewer_pov]
    narration_in_this_shot: "Si hubieras elegido a Celeste, habrías regado al amanecer."
  - shot_id: shot_03
    section_id: setup_pre_decision
    duration_intent_s: 5.0
    scene_context:
      who_is_there: [char_a, viewer_pov]
    narration_in_this_shot: "Si eliges a Bruno, quedas encerrado hasta el amanecer."
  - shot_id: shot_04
    section_id: decision_1
    duration_intent_s: 4.0
    scene_context:
      who_is_there: [viewer_pov]
    narration_in_this_shot: "Ahora decides. La comes o la devuelves."
  - shot_id: shot_05
    section_id: consequence_d1
    consequence_branch: A
    duration_intent_s: 6.0
    scene_context:
      who_is_there: [viewer_pov]
    narration_in_this_shot: "Si comes la fruta, te ahogas en el suelo."
  - shot_id: shot_06
    section_id: consequence_d1
    consequence_branch: B
    duration_intent_s: 5.0
    scene_context:
      who_is_there: [char_a, viewer_pov]
    narration_in_this_shot: "Si la devuelves, Bruno asiente. Sigues limpio."
  - shot_id: shot_07
    section_id: decision_2
    duration_intent_s: 4.0
    scene_context:
      who_is_there: [viewer_pov]
    narration_in_this_shot: "Ahora decides. La alimentas o no te acercas."
  - shot_id: shot_08
    section_id: consequence_d2
    consequence_branch: A
    duration_intent_s: 6.0
    scene_context:
      who_is_there: [viewer_pov]
    narration_in_this_shot: "Si la alimentas, te traga el brazo."
  - shot_id: shot_09
    section_id: consequence_d2
    consequence_branch: B
    duration_intent_s: 5.0
    scene_context:
      who_is_there: [char_a, viewer_pov]
    narration_in_this_shot: "Si no te acercas, Bruno cierra la jaula."
  - shot_id: shot_10
    section_id: resolution_b
    duration_intent_s: 5.0
    scene_context:
      who_is_there: [char_a, viewer_pov]
    narration_in_this_shot: "Amanece verde. Sales con vida."
  - shot_id: shot_11
    section_id: cliffhanger_outro
    duration_intent_s: 4.0
    scene_context:
      who_is_there: [char_b, viewer_pov]
    narration_in_this_shot: "En el delantal de Celeste ya hay semillas."
"""


def _write(path, body):
    Path(path).write_text(body, encoding="utf-8")


class TestV6RealRegression(unittest.TestCase):
    """⭐ THE non-circular adversarial test: the real V6 SPEC MUST FAIL the invariant."""

    @unittest.skipUnless(V6_SPEC.exists(), f"real V6 SPEC not found at {V6_SPEC}")
    def test_v6_invernadero_passes_post_f2(self):
        # V6 amended (F2): Celeste (bueno_aparente) removed from the played path → the corrected
        # REAL artifact MUST now PASS the § 2 invariant. (Pre-F2 it FAILED; the FAIL path is now
        # covered by the mutation regression below + the synthetic fixtures.)
        r = _run(["--format", "horror-choice", "--spec", str(V6_SPEC)])
        self.assertEqual(r.returncode, 0,
                         f"V6 (post-F2) MUST pass.\nstdout {r.stdout}\nstderr {r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["overall_status"], "pass")
        inv = next(g for g in data["gates"]
                   if g["name"] == "invariant_bueno_aparente_absent_from_played_path")
        self.assertEqual(inv["status"], "pass", f"invariant gate must PASS on fixed V6, got {inv}")

    @unittest.skipUnless(V6_SPEC.exists(), f"real V6 SPEC not found at {V6_SPEC}")
    def test_v6_real_artifact_mutated_into_violation_fails(self):
        # Non-circular real-artifact FAIL regression (HR#26 / instance 4/5): inject the
        # bueno_aparente (char_b) into a played-path decision shot of the REAL V6 SPEC → the
        # validator MUST catch it (exit 1). Uses the real v11 schema, not a synthetic dict.
        import yaml, tempfile
        spec = yaml.safe_load(V6_SPEC.read_text())
        for sh in spec.get("shot_list", []):
            if sh.get("shot_id") == "shot_06":
                sh.setdefault("scene_context", {}).setdefault("who_is_there", []).append("char_b")
        td = tempfile.mkdtemp()
        try:
            mp = Path(td) / "v6_mutated.yaml"
            mp.write_text(yaml.safe_dump(spec, allow_unicode=True))
            r = _run(["--format", "horror-choice", "--spec", str(mp)])
            self.assertEqual(r.returncode, 1,
                             f"Mutated V6 (char_b injected into played-path shot_06) MUST fail.\n{r.stdout}")
        finally:
            shutil.rmtree(td, ignore_errors=True)

    @unittest.skipUnless(V6_SPEC.exists(), f"real V6 SPEC not found at {V6_SPEC}")
    def test_v6_celeste_correctly_allowed_in_hook_counterfactual(self):
        # Sanity: the validator must NOT flag Celeste's LEGITIMATE appearances (hook shot_01,
        # counterfactual_opening shot_02, cliffhanger shot_22). The "present in allowed" gate passes.
        r = _run(["--format", "horror-choice", "--spec", str(V6_SPEC)])
        data = json.loads(r.stdout)
        allowed = next(g for g in data["gates"]
                       if g["name"] == "invariant_bueno_aparente_present_in_allowed")
        self.assertEqual(allowed["status"], "pass", f"Celeste should be allowed in hook/cf/cliff: {allowed}")


class TestSyntheticFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_clean_spec_passes(self):
        # bueno_aparente only in hook/counterfactual/cliffhanger → PASS (exit 0).
        _write(self.spec, CLEAN_SPEC.format(caps=_caps_block()))
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"Clean SPEC must pass.\nstdout {r.stdout}\nstderr {r.stderr}")
        data = json.loads(r.stdout)
        self.assertEqual(data["overall_status"], "pass", data)

    def test_bueno_aparente_in_decision_fails(self):
        # Inject char_b (bueno_aparente) into a DECISION shot's who_is_there → MUST FAIL § 2.
        bad = CLEAN_SPEC.format(caps=_caps_block()).replace(
            "  - shot_id: shot_04\n    section_id: decision_1\n    duration_intent_s: 4.0\n"
            "    scene_context:\n      who_is_there: [viewer_pov]",
            "  - shot_id: shot_04\n    section_id: decision_1\n    duration_intent_s: 4.0\n"
            "    scene_context:\n      who_is_there: [char_b, viewer_pov]")
        _write(self.spec, bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"bueno_aparente in decision must FAIL.\nstdout {r.stdout}")
        data = json.loads(r.stdout)
        inv = next(g for g in data["gates"]
                   if g["name"] == "invariant_bueno_aparente_absent_from_played_path")
        self.assertEqual(inv["status"], "fail")
        self.assertIn("shot_04", inv["detail"])

    def test_bueno_aparente_in_consequence_via_anchor_fails(self):
        # § 2 also checks anchor_id_required (not only who_is_there). Inject char_b anchor into a
        # consequence shot whose who_is_there does NOT list char_b → MUST still FAIL.
        bad = CLEAN_SPEC.format(caps=_caps_block()).replace(
            "  - shot_id: shot_08\n    section_id: consequence_d2\n    consequence_branch: A\n"
            "    duration_intent_s: 6.0\n    scene_context:\n      who_is_there: [viewer_pov]",
            "  - shot_id: shot_08\n    section_id: consequence_d2\n    consequence_branch: A\n"
            "    duration_intent_s: 6.0\n    anchor_id_required: {char_b: char_b_v1}\n"
            "    scene_context:\n      who_is_there: [viewer_pov]")
        _write(self.spec, bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"bueno_aparente anchor in consequence must FAIL.\nstdout {r.stdout}")
        data = json.loads(r.stdout)
        inv = next(g for g in data["gates"]
                   if g["name"] == "invariant_bueno_aparente_absent_from_played_path")
        self.assertEqual(inv["status"], "fail")
        self.assertIn("shot_08", inv["detail"])

    def test_interleaved_counterfactual_fails_sequential(self):
        # Move the counterfactual to sit BETWEEN played-path sections (after decision_1) → § 3 FAIL.
        bad = CLEAN_SPEC.format(caps=_caps_block()).replace(
            "  - shot_id: shot_02\n    section_id: counterfactual_opening",
            "  - shot_id: shot_02\n    section_id: setup_pre_decision").replace(
            "  - shot_id: shot_06\n    section_id: consequence_d1\n    consequence_branch: B",
            "  - shot_id: shot_06\n    section_id: counterfactual_mid\n    consequence_branch: B")
        _write(self.spec, bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        data = json.loads(r.stdout)
        seq = next(g for g in data["gates"] if g["name"] == "sequential_paths")
        self.assertEqual(seq["status"], "fail",
                         f"interleaved counterfactual must FAIL § 3.\nstdout {r.stdout}")
        self.assertEqual(r.returncode, 1)

    def test_missing_decisions_flags_structure(self):
        # A SPEC with only ONE decision → structure skeleton FLAG (not fail), exit 0.
        bad = CLEAN_SPEC.format(caps=_caps_block()).replace(
            "  - shot_id: shot_07\n    section_id: decision_2\n    duration_intent_s: 4.0\n"
            "    scene_context:\n      who_is_there: [viewer_pov]\n"
            '    narration_in_this_shot: "Ahora decides. La alimentas o no te acercas."\n', "").replace(
            "    section_id: consequence_d2\n", "    section_id: consequence_d1_extra\n")
        _write(self.spec, bad)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"missing decision must FLAG (exit 0) not FAIL.\nstdout {r.stdout}")
        data = json.loads(r.stdout)
        skel = next(g for g in data["gates"] if g["name"] == "structure_skeleton")
        self.assertEqual(skel["status"], "flag", f"expected structure FLAG, got {skel}")


class TestCapabilityGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_non_horror_choice_not_applicable(self):
        _write(self.spec, CLEAN_SPEC.format(caps=_caps_block()))
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"non-horror-choice must be not_applicable.\nstdout {r.stdout}")
        self.assertIn("not_applicable", r.stdout.lower())

    def test_format_flag_required(self):
        _write(self.spec, CLEAN_SPEC.format(caps=_caps_block()))
        r = _run(["--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(r.returncode, 0, f"missing --format must error. stderr: {r.stderr}")
        self.assertIn("format", r.stderr.lower())

    def test_bug9_video_capabilities_missing(self):
        _write(self.spec, CLEAN_SPEC.format(caps=_caps_block(omit=True)))
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 2, f"Bug #9 (missing video_capabilities) must exit 2. stderr: {r.stderr}")

    def test_missing_spec_exits_2(self):
        r = _run(["--format", "horror-choice", "--spec", str(Path(self.tmp) / "nope.yaml")])
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
