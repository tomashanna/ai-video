#!/usr/bin/env python3
"""test_audit-first30s-animation.py — HR#26 companion adversarial test.

Fixtures sintéticas que MODELAN EL CASO DISPARADOR HISTÓRICO:
  - cabana-tormenta: el HOOK (start 0) shipeado como <img> estático/Ken Burns →
    el gate DEBE fallar HR#6.
  - versión sana con el hook como <video> clip animado AI → PASA.
  - un estático/Ken Burns de 5.0s → FALLA HR#7 (max 2-3s).
  - share de estáticos >20% → FALLA HR#7.
Más capability gates (Bug #9, not_applicable) + ambos modos (manifest + HTML) +
edge cases (ventana boundary, share boundary).
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Import del script-under-test (nombre con guiones → importlib).
_HERE = Path(__file__).resolve().parent
_SUT_PATH = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_first30s_animation.py"
_spec = importlib.util.spec_from_file_location("audit_first30s_animation", _SUT_PATH)
sut = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sut)


# ═══════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — HR#6 first-30s animation
# ═══════════════════════════════════════════════════════════════════════════

class TestEvaluateFirst30sHR6(unittest.TestCase):

    def test_hook_static_at_start_0_fails(self):
        """CASO DISPARADOR cabana-tormenta: hook estático en start 0 → FAIL HR#6."""
        shots = [
            {"shot_id": "hook", "start_s": 0.0, "is_animated": False},      # <img> estático
            {"shot_id": "s2", "start_s": 3.0, "is_animated": True},
        ]
        ok, reasons = sut.evaluate_first30s_hr6(shots)
        self.assertFalse(ok)
        fails = [r for r in reasons if r["status"] == "fail"]
        self.assertEqual(len(fails), 1)
        self.assertEqual(fails[0]["shot_id"], "hook")

    def test_hook_animated_passes(self):
        """Versión sana: hook = clip animado AI → PASS."""
        shots = [
            {"shot_id": "hook", "start_s": 0.0, "is_animated": True},       # <video>
            {"shot_id": "s2", "start_s": 5.0, "is_animated": True},
        ]
        ok, reasons = sut.evaluate_first30s_hr6(shots)
        self.assertTrue(ok)

    def test_some_clip_present_but_hook_static_still_fails(self):
        """Refuta el check INGENUO ('hay AL MENOS un clip animado'): aunque haya
        clips animados después, el hook estático <30s sigue siendo FAIL."""
        shots = [
            {"shot_id": "hook", "start_s": 0.0, "is_animated": False},      # estático
            {"shot_id": "s2", "start_s": 4.0, "is_animated": True},
            {"shot_id": "s3", "start_s": 8.0, "is_animated": True},
        ]
        ok, _ = sut.evaluate_first30s_hr6(shots)
        self.assertFalse(ok)

    def test_static_after_30s_does_not_fail_hr6(self):
        """Shot estático que arranca DESPUÉS de la ventana no lo gatea HR#6."""
        shots = [
            {"shot_id": "hook", "start_s": 0.0, "is_animated": True},
            {"shot_id": "late_static", "start_s": 35.0, "is_animated": False},
        ]
        ok, reasons = sut.evaluate_first30s_hr6(shots)
        self.assertTrue(ok)
        late = [r for r in reasons if r["shot_id"] == "late_static"][0]
        self.assertFalse(late["rule_applies"])

    def test_window_boundary_exclusive(self):
        """start_s == window_s NO entra en la ventana (>=window queda fuera)."""
        shots = [{"shot_id": "edge", "start_s": 30.0, "is_animated": False}]
        ok, reasons = sut.evaluate_first30s_hr6(shots, window_s=30.0)
        self.assertTrue(ok)
        self.assertFalse(reasons[0]["rule_applies"])


# ═══════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — HR#7 Ken Burns fallback
# ═══════════════════════════════════════════════════════════════════════════

class TestEvaluateKenburnsHR7(unittest.TestCase):

    def test_kenburns_5s_fails_duration(self):
        """CASO DISPARADOR: Ken Burns de 5.0s → FAIL HR#7 (max 2-3s)."""
        shots = [
            {"shot_id": "kb", "is_static_kenburns": True, "duration_s": 5.0},
            {"shot_id": "a", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "b", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "c", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "d", "is_static_kenburns": False, "duration_s": 4.0},
        ]
        ok, summary, per_shot = sut.evaluate_kenburns_hr7(shots)
        self.assertFalse(ok)
        self.assertIn("kb", summary["over_duration_shots"])
        # share 1/5 = 20% → share OK; falla SOLO por duración.
        self.assertTrue(summary["share_ok"])
        self.assertFalse(summary["duration_ok"])

    def test_kenburns_share_over_20pct_fails(self):
        """Share de estáticos > 20% → FAIL HR#7 (PowerPoint-narrado cabana-tormenta:
        23/23 = 100% estáticos)."""
        shots = [
            {"shot_id": "kb1", "is_static_kenburns": True, "duration_s": 2.5},
            {"shot_id": "kb2", "is_static_kenburns": True, "duration_s": 2.5},
            {"shot_id": "a", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "b", "is_static_kenburns": False, "duration_s": 4.0},
        ]
        ok, summary, _ = sut.evaluate_kenburns_hr7(shots)  # 2/4 = 50%
        self.assertFalse(ok)
        self.assertFalse(summary["share_ok"])

    def test_kenburns_within_budget_passes(self):
        """1/5 = 20% estáticos, cada uno ≤3s → PASS (fallback acotado válido)."""
        shots = [
            {"shot_id": "kb", "is_static_kenburns": True, "duration_s": 2.5},
            {"shot_id": "a", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "b", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "c", "is_static_kenburns": False, "duration_s": 4.0},
            {"shot_id": "d", "is_static_kenburns": False, "duration_s": 4.0},
        ]
        ok, summary, _ = sut.evaluate_kenburns_hr7(shots)
        self.assertTrue(ok)

    def test_no_static_passes(self):
        """0 estáticos → PASS trivial."""
        shots = [{"shot_id": "a", "is_static_kenburns": False, "duration_s": 4.0}]
        ok, summary, _ = sut.evaluate_kenburns_hr7(shots)
        self.assertTrue(ok)
        self.assertEqual(summary["static_kenburns_shots"], 0)


# ═══════════════════════════════════════════════════════════════════════════
# WRAPPERS DE EXTRACCIÓN
# ═══════════════════════════════════════════════════════════════════════════

class TestParseManifestShots(unittest.TestCase):

    def test_cumulative_start_and_procedural_flagged(self):
        manifest = {"shots": [
            {"shot_id": "shot_01", "model": "kling_v2.5_pro", "procedural": False},
            {"shot_id": "shot_02", "model": "hailuo_std", "procedural": False},
            {"shot_id": "shot_08", "model": "procedural", "procedural": True},
        ]}
        spec = {"shot_list": [
            {"shot_id": "shot_01", "duration_intent_s": 5.0},
            {"shot_id": "shot_02", "duration_intent_s": 4.0},
            {"shot_id": "shot_08", "duration_intent_s": 2.2},
        ]}
        shots = sut.parse_manifest_shots(manifest, spec)
        self.assertEqual(shots[0]["start_s"], 0.0)
        self.assertEqual(shots[1]["start_s"], 5.0)
        self.assertEqual(shots[2]["start_s"], 9.0)
        self.assertTrue(shots[0]["is_animated"])
        self.assertTrue(shots[2]["is_static_kenburns"])   # procedural bridge

    def test_procedural_bridge_under_30s_fails_hr6(self):
        """Un bridge procedural que cae <30s viola HR#6 (no-AI en la ventana)."""
        manifest = {"shots": [
            {"shot_id": "shot_01", "model": "kling_v2.5_pro", "procedural": False},
            {"shot_id": "shot_08", "model": "procedural", "procedural": True},
        ]}
        spec = {"shot_list": [
            {"shot_id": "shot_01", "duration_intent_s": 5.0},
            {"shot_id": "shot_08", "duration_intent_s": 2.2},   # start 5.0s (<30)
        ]}
        shots = sut.parse_manifest_shots(manifest, spec)
        ok, reasons = sut.evaluate_first30s_hr6(shots)
        self.assertFalse(ok)
        self.assertEqual([r["shot_id"] for r in reasons if r["status"] == "fail"], ["shot_08"])


class TestParseHtmlShots(unittest.TestCase):

    def test_video_animated_img_static(self):
        html = (
            '<video id="v-hook" src="assets/hook.mp4" class="clip" data-start="0" data-duration="3.31"></video>\n'
            '<img id="kb1" src="assets/s2.png" class="clip" data-start="3.31" data-duration="3"/>\n'
            '<div id="countdown" data-start="5.5" data-duration="3.0"></div>\n'  # overlay, no <video>/<img>
        )
        shots = sut.parse_html_shots(html)
        self.assertEqual(len(shots), 2)   # div ignorado
        v = [s for s in shots if s["shot_id"] == "v-hook"][0]
        i = [s for s in shots if s["shot_id"] == "kb1"][0]
        self.assertTrue(v["is_animated"])
        self.assertFalse(i["is_animated"])
        self.assertTrue(i["is_static_kenburns"])


# ═══════════════════════════════════════════════════════════════════════════
# RUNTIME (end-to-end vía subprocess) — capability gates + casos disparadores
# ═══════════════════════════════════════════════════════════════════════════

def _run(args):
    res = subprocess.run(
        [sys.executable, str(_SUT_PATH)] + args,
        capture_output=True, text=True)
    return res


def _spec_yaml(has_clips=True, format_type="interactive_choice", shot_list=None,
               with_caps=True):
    d = {}
    if with_caps:
        d["video_capabilities"] = {
            "has_ai_generated_clips": has_clips,
            "format_type": format_type,
        }
    d["shot_list"] = shot_list or []
    return d


class TestRuntimeCLI(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, name, obj):
        p = self.dir / name
        if name.endswith((".yaml", ".yml")):
            import yaml
            p.write_text(yaml.safe_dump(obj), encoding="utf-8")
        else:
            p.write_text(obj, encoding="utf-8")
        return p

    # — Capability gates —

    def test_missing_video_capabilities_exit_2(self):
        spec = self._write("spec.yaml", _spec_yaml(with_caps=False))
        man = self._write("m.yaml", {"shots": [{"shot_id": "shot_01", "model": "kling"}]})
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--manifest", str(man)])
        self.assertEqual(res.returncode, 2, res.stderr)
        self.assertIn("Bug #9", res.stderr)

    def test_has_no_clips_not_applicable_exit_0(self):
        spec = self._write("spec.yaml", _spec_yaml(has_clips=False))
        man = self._write("m.yaml", {"shots": [{"shot_id": "shot_01", "model": "kling"}]})
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--manifest", str(man)])
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("not_applicable", res.stdout)

    def test_format_type_out_of_set_not_applicable(self):
        spec = self._write("spec.yaml", _spec_yaml(format_type="testimonial"))
        man = self._write("m.yaml", {"shots": [{"shot_id": "shot_01", "model": "kling"}]})
        res = _run(["--format", "editorial", "--spec", str(spec), "--manifest", str(man)])
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("not_applicable", res.stdout)

    # — Caso disparador HTML (cabana-tormenta hook estático) —

    def test_html_hook_static_fails(self):
        spec = self._write("spec.yaml", _spec_yaml())
        html = self._write("index.html",
            '<img id="hook" src="assets/hook.png" data-start="0" data-duration="3"/>\n'
            '<video id="s2" src="assets/s2.mp4" data-start="3" data-duration="3"></video>\n')
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--html", str(html)])
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        report = json.loads(res.stdout)
        self.assertFalse(report["hr6_first30s_animation"]["pass"])

    def test_html_all_video_passes(self):
        spec = self._write("spec.yaml", _spec_yaml())
        html = self._write("index.html",
            '<video id="hook" src="assets/hook.mp4" data-start="0" data-duration="3"></video>\n'
            '<video id="s2" src="assets/s2.mp4" data-start="3" data-duration="3"></video>\n')
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--html", str(html)])
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_html_5s_kenburns_fails_hr7(self):
        """Ken Burns de 5s (<img> 5s) → FAIL HR#7 incluso si está fuera de los 30s
        (la regla HR#7 es global). Lo ponemos en start 40 para aislar HR#7 de HR#6."""
        spec = self._write("spec.yaml", _spec_yaml())
        html = self._write("index.html",
            '<video id="a" src="a.mp4" data-start="0" data-duration="6"></video>\n'
            '<video id="b" src="b.mp4" data-start="6" data-duration="6"></video>\n'
            '<video id="c" src="c.mp4" data-start="12" data-duration="6"></video>\n'
            '<video id="d" src="d.mp4" data-start="18" data-duration="6"></video>\n'
            '<img id="kb5" src="kb.png" data-start="40" data-duration="5"/>\n')  # 1/5=20% but 5s>3s
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--html", str(html)])
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        report = json.loads(res.stdout)
        self.assertTrue(report["hr6_first30s_animation"]["pass"])     # 30s window clean
        self.assertFalse(report["hr7_kenburns_fallback"]["pass"])     # but 5s static
        self.assertIn("kb5", report["hr7_kenburns_fallback"]["summary"]["over_duration_shots"])

    # — Manifest mode end-to-end —

    def test_manifest_hook_static_model_fails(self):
        spec = self._write("spec.yaml", _spec_yaml(shot_list=[
            {"shot_id": "shot_01", "duration_intent_s": 5.0},
            {"shot_id": "shot_02", "duration_intent_s": 4.0},
        ]))
        man = self._write("m.yaml", {"shots": [
            {"shot_id": "shot_01", "model": "ken-burns", "procedural": True},  # hook no-AI
            {"shot_id": "shot_02", "model": "hailuo_std", "procedural": False},
        ]})
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--manifest", str(man)])
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)

    def test_empty_input_exit_2(self):
        spec = self._write("spec.yaml", _spec_yaml())
        man = self._write("m.yaml", {"shots": []})
        res = _run(["--format", "horror-choice", "--spec", str(spec), "--manifest", str(man)])
        self.assertEqual(res.returncode, 2, res.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
