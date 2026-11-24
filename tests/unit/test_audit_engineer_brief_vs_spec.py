"""test_audit-engineer-brief-vs-spec.py — Gap #47 anti-recurrence validator companion.

Hard Rule #26 companion test for audit-engineer-brief-vs-spec.py.

Cases:
  (a) brief with the visual_intent VERBATIM → PASS
  (b) brief paraphrased/compressed (V7 shot_03b reconstruction: SPEC "POV mira atrás:
      reja se cierra sellando salida" vs brief "Dario baja al andén parte 2") → FAIL
  (c) brief that contradicts (same shot, different action) → FAIL
  (d) shot_id not in SPEC → exit 2
  (e) real SPEC v11 shot from creative-specs/ultimo-tren-carga.yaml → PASS verbatim / FAIL paraphrase
  (f) --all-shots --briefs-json batch mode
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_engineer_brief_vs_spec.py"
REAL_SPEC = Path(__file__).resolve().parents[2] / "examples/specs/ultimo-tren-carga.yaml"


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


# Reconstruction of V7 shot_03b canonical visual_intent (per the real SPEC).
SHOT_03B_VI = (
    "POV girando brevemente hacia atrás: una reja de seguridad metálica baja y se cierra "
    "con un chasquido pesado, sellando los escalones de salida. La luz de emergencia ámbar "
    "parpadea sobre los barrotes mojados. La mirada vuelve al frente del andén de servicio."
)


def _write_spec(path, shots_yaml):
    Path(path).write_text(f'schema_version: "v11.1"\n{shots_yaml}', encoding="utf-8")


class TestBriefVsSpec(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        _write_spec(self.spec, f"""shot_list:
  - shot_id: shot_03b
    visual_intent: |
      {SHOT_03B_VI}
  - shot_id: shot_01
    visual_intent: |
      POV plano medio del dyad bajo luz ámbar parpadeante, Tobias extiende el termo humeante.
""")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # (a) verbatim → PASS
    def test_verbatim_brief_passes(self):
        brief = f"Engineer brief shot_03b — ejecutá esto literal:\n{SHOT_03B_VI}\nFin."
        r = _run(["--spec", str(self.spec), "--shot-id", "shot_03b", "--brief", brief])
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        rep = json.loads(r.stdout)
        self.assertTrue(rep["overall_pass"])
        self.assertTrue(rep["verbatim_present"])

    # (b) V7 shot_03b paraphrase/compression → FAIL
    def test_v7_shot03b_paraphrase_fails(self):
        brief = "shot_03b: Dario baja al andén parte 2. Continúa el recorrido."
        r = _run(["--spec", str(self.spec), "--shot-id", "shot_03b", "--brief", brief])
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        rep = json.loads(r.stdout)
        self.assertFalse(rep["overall_pass"])
        self.assertFalse(rep["verbatim_present"])
        self.assertTrue(any("Gap #47" in f for f in rep["failures"]))

    # (c) contradiction (same shot, different action) → FAIL
    def test_contradiction_fails(self):
        # Mentions the shot but describes a different action than "reja se cierra".
        brief = ("POV girando hacia atrás: la reja de seguridad metálica SE ABRE de par en par "
                 "y el viewer sube corriendo los escalones hacia la salida iluminada.")
        r = _run(["--spec", str(self.spec), "--shot-id", "shot_03b", "--brief", brief])
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        rep = json.loads(r.stdout)
        self.assertFalse(rep["overall_pass"])

    # (d) shot_id not in SPEC → exit 2
    def test_unknown_shot_id_exits_2(self):
        r = _run(["--spec", str(self.spec), "--shot-id", "shot_zzz", "--brief", "whatever"])
        self.assertEqual(r.returncode, 2, r.stderr + r.stdout)
        self.assertIn("not found", r.stderr)

    # (d2) missing spec → exit 2
    def test_missing_spec_exits_2(self):
        r = _run(["--spec", str(Path(self.tmp) / "nope.yaml"),
                  "--shot-id", "shot_03b", "--brief", "x"])
        self.assertEqual(r.returncode, 2)

    # brief via @file
    def test_brief_from_file(self):
        bf = Path(self.tmp) / "brief.txt"
        bf.write_text(SHOT_03B_VI, encoding="utf-8")
        r = _run(["--spec", str(self.spec), "--shot-id", "shot_03b", "--brief", f"@{bf}"])
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertTrue(json.loads(r.stdout)["overall_pass"])

    # (f) --all-shots batch
    def test_all_shots_mode(self):
        briefs = {
            "shot_03b": SHOT_03B_VI,                       # verbatim → ok
            "shot_01": "shot_01: arrancá la escena del túnel.",  # paraphrase → fail
        }
        bj = Path(self.tmp) / "briefs.json"
        bj.write_text(json.dumps(briefs, ensure_ascii=False), encoding="utf-8")
        r = _run(["--spec", str(self.spec), "--all-shots", "--briefs-json", str(bj)])
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        rep = json.loads(r.stdout)
        self.assertEqual(rep["total_checked"], 2)
        self.assertEqual(rep["fail_count"], 1)

    def test_all_shots_unknown_shot_exits_2(self):
        bj = Path(self.tmp) / "briefs.json"
        bj.write_text(json.dumps({"shot_nope": "x"}), encoding="utf-8")
        r = _run(["--spec", str(self.spec), "--all-shots", "--briefs-json", str(bj)])
        self.assertEqual(r.returncode, 2)


@unittest.skipUnless(REAL_SPEC.exists(), "real V7 SPEC not present")
class TestRealSpecV11(unittest.TestCase):
    """(e) Real SPEC v11 — read a real shot from ultimo-tren-carga.yaml."""

    def test_real_shot03b_verbatim_passes(self):
        # Pull the canonical visual_intent straight from the real SPEC, pass it verbatim.
        import yaml
        spec = yaml.safe_load(REAL_SPEC.read_text(encoding="utf-8"))
        shot = next(s for s in spec["shot_list"] if s["shot_id"] == "shot_03b")
        vi = shot["visual_intent"]
        r = _run(["--spec", str(REAL_SPEC), "--shot-id", "shot_03b", "--brief", vi])
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        self.assertTrue(json.loads(r.stdout)["overall_pass"])

    def test_real_shot03b_paraphrase_fails(self):
        r = _run(["--spec", str(REAL_SPEC), "--shot-id", "shot_03b",
                  "--brief", "shot_03b: Dario baja al andén parte 2."])
        self.assertEqual(r.returncode, 1, r.stderr + r.stdout)
        rep = json.loads(r.stdout)
        self.assertFalse(rep["overall_pass"])
        self.assertTrue(any("Gap #47" in f for f in rep["failures"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
