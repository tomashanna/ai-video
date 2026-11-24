#!/usr/bin/env python3
"""test_audit-decision-ui-pacing.py — HR#26 companion adversarial test de Q22a.

Modela el CASO DISPARADOR (un parámetro de decision-UI fuera de la banda canónica DEBE fallar el
gate) + casos sanos + report-only:
  · FIXTURE DISPARADOR — countdown digit duration FUERA de banda (banda FUERTE simulada n=8) → FAIL.
  · countdown digit duration DENTRO de banda (n fuerte) → PASS.
  · banda DÉBIL (n=1, como el aggregate JSON canónico real de countdown_digit_duration) → report-only,
    NUNCA falla aunque el valor esté lejos de la mediana.
  · pause beat (banda fuerte n=14) fuera de [p25,p75] → FAIL.
  · WPM decision_question fuera de banda fuerte → FAIL; dentro → PASS.
  · params del render (ambient_duck / freeze SSIM / loading fill) → siempre forward, nunca medidos.
  · capability-gate: format_type sin UI + has_layer_4_ui false → not_applicable.
  · video_capabilities ausente → Bug #9 (exit 2).

Carga el módulo con guion en el nombre vía importlib. Corre: python3 test_audit-decision-ui-pacing.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "audit_decision_ui_pacing", Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_decision_ui_pacing.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


# ── Bandas sintéticas ───────────────────────────────────────────────────────────────────────

def _bands(*, cd_n=8, cd_p25=0.85, cd_p75=1.05, pb_n=14, pb_p25=0.33, pb_p75=2.1,
           dq_n=23, dq_p25=140.0, dq_p75=160.0):
    """aggregate dict sintético. cd_n controla si countdown_digit es banda fuerte (≥4) o débil."""
    return {
        "schema_version": "v1",
        "source_refs": ["ref-03", "ref-06"],
        "params": {
            "countdown_digit_duration_s": {"median": 0.95, "p25": cd_p25, "p75": cd_p75, "n_samples": cd_n},
            "countdown_pause_beat_s": {"median": 0.9, "p25": pb_p25, "p75": pb_p75, "n_samples": pb_n},
            "freeze_frame": {"pct_windows_with_freeze": 0.14, "n_windows_total": 22},
            "per_segment_wpm_bands": {
                "decision_question": {"median": 150.0, "p25": dq_p25, "p75": dq_p75, "n_samples": dq_n},
                "decision_setup": {"median": 165.0, "p25": 152.5, "p75": 205.9, "n_samples": 10},
            },
        },
    }


def _decision_shot(shot_id="shot_06", *, cd_dur=1.0, pause_beat=0.9, clock_consistent=True,
                   wpm_role="decision_question", wpm=150.0, freeze=True, loading_s=3.5):
    """Estructura pura tal como la arma extract_decision_shots()."""
    return {
        "shot_id": shot_id,
        "countdown_digit_duration_s": cd_dur,
        "countdown_pause_beat_s": pause_beat,
        "pause_beat_clock_consistent": clock_consistent,
        "wpm_checks": ([{"role": wpm_role, "wpm": wpm}] if wpm_role else []),
        "freeze_declared": freeze,
        "loading_visible_s": loading_s,
    }


def _statuses(results, param):
    out = []
    for shot in results:
        for c in shot["checks"]:
            if c["param"].split("[")[0] == param:
                out.append(c["status"])
    return out


class TestCountdownDigitDuration(unittest.TestCase):
    """CASO DISPARADOR: countdown digit duration fuera de banda FUERTE → FAIL."""

    def test_countdown_fuera_de_banda_fuerte_FALLA(self):
        shots = [_decision_shot(cd_dur=0.4)]  # 0.4 < p25 0.85 → fuera
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(cd_n=8))
        self.assertFalse(ok, "countdown 0.4s fuera de banda fuerte [0.85,1.05] DEBE fallar")
        self.assertIn("fail", _statuses(results, "countdown_digit_duration_s"))

    def test_countdown_dentro_de_banda_fuerte_PASA(self):
        shots = [_decision_shot(cd_dur=0.95)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(cd_n=8))
        self.assertTrue(ok)
        self.assertIn("pass", _statuses(results, "countdown_digit_duration_s"))

    def test_banda_DEBIL_n1_es_report_only_nunca_falla(self):
        # n=1 como el aggregate JSON canónico real → aunque 0.4 esté lejos, NO falla.
        shots = [_decision_shot(cd_dur=0.4, pause_beat=0.9, wpm=150.0)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(cd_n=1))
        self.assertIn("report_only", _statuses(results, "countdown_digit_duration_s"))
        self.assertNotIn("fail", _statuses(results, "countdown_digit_duration_s"))


class TestPauseBeat(unittest.TestCase):
    def test_pause_beat_fuera_de_banda_FALLA(self):
        shots = [_decision_shot(pause_beat=5.0)]  # 5.0 > p75 2.1 → fuera
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(pb_n=14))
        self.assertFalse(ok)
        self.assertIn("fail", _statuses(results, "countdown_pause_beat_s"))

    def test_pause_beat_dentro_PASA(self):
        shots = [_decision_shot(pause_beat=0.9)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(pb_n=14))
        self.assertTrue(ok)

    def test_pause_beat_None_es_report_only(self):
        shots = [_decision_shot(pause_beat=None)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(pb_n=14))
        self.assertIn("report_only", _statuses(results, "countdown_pause_beat_s"))

    def test_pause_beat_cross_clock_NO_falla_es_report_only(self):
        # clock inconsistente (dos relojes del SPEC divergen) → aunque 8.9 esté fuera de banda,
        # NO falla: cross-clock no es measurement-grade (anti-artefacto).
        shots = [_decision_shot(pause_beat=8.9, clock_consistent=False)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands(pb_n=14))
        self.assertTrue(ok, "cross-clock pause-beat NO debe fallar el gate (es report-only)")
        self.assertIn("report_only", _statuses(results, "countdown_pause_beat_s"))


class TestWPMPerSegment(unittest.TestCase):
    def test_decision_question_fuera_de_banda_FALLA(self):
        shots = [_decision_shot(wpm_role="decision_question", wpm=260.0)]  # > p75 160
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands())
        self.assertFalse(ok)
        self.assertIn("fail", _statuses(results, "per_segment_wpm"))

    def test_decision_question_dentro_PASA(self):
        shots = [_decision_shot(wpm_role="decision_question", wpm=150.0)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands())
        self.assertTrue(ok)

    def test_rol_no_gating_no_falla(self):
        # un rol fuera de GATING_WPM_ROLES se reporta pero no gatea aunque "raro"
        shots = [_decision_shot(wpm_role="cliffhanger", wpm=999.0)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands())
        self.assertTrue(ok)
        self.assertIn("report_only", _statuses(results, "per_segment_wpm"))


class TestFreezeAndLoadingReportOnly(unittest.TestCase):
    def test_freeze_y_loading_son_report_only(self):
        shots = [_decision_shot(freeze=True, loading_s=3.5)]
        ok, results = mod.evaluate_decision_ui_pacing(shots, _bands())
        self.assertIn("report_only", _statuses(results, "freeze_declared_context"))
        self.assertIn("report_only", _statuses(results, "loading_bar_visible_span_s"))


# ── Extracción desde SPEC dict ────────────────────────────────────────────────────────────────

def _spec_dict(*, countdown_span=(1.0, 4.0), countdown_text="3-2-1", dur=4.8,
               narration="El riel se ve firme. Ahora decides: pisas el riel o el cemento.",
               narration_end_abs=30.3):
    """SPEC mínimo con 1 decision shot (shot_06) + su narración en narration_script."""
    return {
        "video_capabilities": {"format_type": "interactive_choice", "has_layer_4_ui": True},
        "shot_list": [
            {"shot_id": "shot_06", "section_id": "decision_1", "duration_intent_s": dur,
             "pov_traversal": "static_with_micro_bob",
             "visual_style_lut": "amber_emergency_tunnel_v1_freeze_filter",
             "avu_overlay_clip": "decision-freeze-with-tick-3-2-1.mp4",
             "narration_in_this_shot": narration,
             "ui_active": [
                 {"element_id": "countdown_d1",
                  "timestamp_visible_s": list(countdown_span), "text": countdown_text,
                  "font": "film_leader_academy"},
                 {"element_id": "loading_bar_d1",
                  "timestamp_visible_s": [1.0, 4.5], "font": "loading_canonical"},
             ]},
        ],
        "narration_script": [
            {"segment_id": "narrator_d1_question", "speaker": "narrator",
             "shot_id_anchor": "shot_06",
             "timestamp_intent_s": [25.5, narration_end_abs]},
        ],
    }


class TestExtraction(unittest.TestCase):
    def test_countdown_digit_duration_derivado(self):
        shots = mod.extract_decision_shots(_spec_dict(countdown_span=(1.0, 4.0), countdown_text="3-2-1"))
        self.assertEqual(len(shots), 1)
        self.assertAlmostEqual(shots[0]["countdown_digit_duration_s"], 1.0, places=2)

    def test_detecta_decision_shot_por_ui_y_section(self):
        shots = mod.extract_decision_shots(_spec_dict())
        self.assertEqual(shots[0]["shot_id"], "shot_06")

    def test_wpm_clasifica_decision_question(self):
        shots = mod.extract_decision_shots(_spec_dict())
        roles = [w["role"] for w in shots[0]["wpm_checks"]]
        self.assertIn("decision_question", roles)

    def test_loading_visible_span(self):
        shots = mod.extract_decision_shots(_spec_dict())
        self.assertAlmostEqual(shots[0]["loading_visible_s"], 3.5, places=2)

    def test_freeze_declarado_detectado(self):
        shots = mod.extract_decision_shots(_spec_dict())
        self.assertTrue(shots[0]["freeze_declared"])


class TestCLI(unittest.TestCase):
    """Wrapper runtime: capability-gate, Bug #9, exit codes."""

    def _run(self, spec_obj, bands_obj=None, extra=None):
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d) / "spec.yaml"
            sp.write_text(_yaml_dump(spec_obj))
            args = [sys.executable, str(Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_decision_ui_pacing.py"),
                    "--format", "horror-choice", "--spec", str(sp)]
            if bands_obj is not None:
                bp = Path(d) / "bands.json"
                bp.write_text(json.dumps(bands_obj))
                args += ["--bands-json", str(bp)]
            if extra:
                args += extra
            return subprocess.run(args, capture_output=True, text=True)

    def test_bug9_video_capabilities_ausente_exit2(self):
        r = self._run({"shot_list": []}, bands_obj=_bands())
        self.assertEqual(r.returncode, 2)
        self.assertIn("Bug #9", r.stderr)

    def test_not_applicable_sin_ui(self):
        spec = {"video_capabilities": {"format_type": "tutorial", "has_layer_4_ui": False},
                "shot_list": []}
        r = self._run(spec, bands_obj=_bands())
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout)

    def test_smoke_disparador_fuera_de_banda_exit1(self):
        # countdown 0.4s/digit con banda fuerte n=8 → exit 1
        spec = _spec_dict(countdown_span=(1.0, 2.2), countdown_text="3-2-1")  # 1.2/3=0.4
        r = self._run(spec, bands_obj=_bands(cd_n=8))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn('"overall_status": "fail"', r.stdout)

    def test_smoke_dentro_de_banda_exit0(self):
        spec = _spec_dict(countdown_span=(1.0, 4.0), countdown_text="3-2-1")  # 1.0/digit
        # pause beat: countdown_start_abs = shot_start_abs(shot_06=0, único shot) + 1.0 = 1.0;
        # narration_end_abs = 30.3 → pause = 1.0-30.3 negativo → fuera de banda. Para aislar el
        # caso countdown, usamos override de bands con pause débil + wpm amplio.
        bands = _bands(cd_n=8, pb_n=1, dq_p25=80.0, dq_p75=260.0)
        r = self._run(spec, bands_obj=bands)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_bands_json_ausente_exit2(self):
        # sin --bands-json y sin path canónico alcanzable desde el tmpdir → exit 2
        with tempfile.TemporaryDirectory() as d:
            sp = Path(d) / "spec.yaml"
            sp.write_text(_yaml_dump(_spec_dict()))
            r = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_decision_ui_pacing.py"),
                 "--format", "horror-choice", "--spec", str(sp),
                 "--bands-json", str(Path(d) / "nope.json")],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)


def _yaml_dump(obj):
    try:
        import yaml
        return yaml.safe_dump(obj)
    except ImportError:  # pragma: no cover
        return json.dumps(obj)  # yaml.safe_load lee JSON


if __name__ == "__main__":
    unittest.main(verbosity=2)
