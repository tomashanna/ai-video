#!/usr/bin/env python3
"""test_audit-style-markup.py — adversarial tests para audit-style-markup.py (HR#26 companion).

Modela el caso disparador histórico (grep manual del pre-render-gate Q19/Q20 que
deja pasar render sin vignette + name labels en fuente proporcional). El bug REAL
debe FALLAR el gate; el caso sano PASA; edge cases cubren la implicación condicional
de Q20 (sin name labels → not_applicable) + capability gate + Bug #9.

Run: python3 test_audit-style-markup.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_style_markup.py"

# import por path (nombre con guión no es importable como módulo normal)
_spec = importlib.util.spec_from_file_location("audit_style_markup", _SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


# ─────────── fixtures HTML (modelan markup real del template choice) ───────────

# Caso SANO: vignette por radial-gradient + name labels en Menlo (monospaced).
HTML_HEALTHY = """<!DOCTYPE html><html><head>
<style>
#root { position:absolute; }
.vignette-overlay { position:absolute; width:100%; height:100%;
  background: radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.7) 100%); }
.name-label { font-family: Menlo, monospace; font-size:80px; color:white; }
</style></head><body>
<div id="root" data-composition-id="x">
  <div class="vignette-overlay"></div>
  <div class="name-label" id="choice_button_a">DARIO</div>
  <div class="name-label" id="choice_button_b">TOBIAS</div>
</div></body></html>"""

# BUG #1 (vignette ausente): name labels mono OK pero CERO markup de vignette.
HTML_NO_VIGNETTE = """<!DOCTYPE html><html><head>
<style>
.name-label { font-family: 'Space Mono', monospace; font-size:80px; }
</style></head><body>
<div id="root">
  <div class="name-label" id="choice_button_a">DARIO</div>
  <div class="name-label" id="choice_button_b">TOBIAS</div>
</div></body></html>"""

# BUG #2 (names sin mono): vignette OK pero name labels en Arial (proportional).
HTML_NAMES_NO_MONO = """<!DOCTYPE html><html><head>
<style>
.vignette { box-shadow: inset 0 0 200px 80px rgba(0,0,0,0.8); }
.name-label { font-family: 'Arial Bold', sans-serif; font-size:80px; }
</style></head><body>
<div id="root">
  <div class="vignette"></div>
  <div class="name-label" id="choice_button_a">DARIO</div>
  <div class="name-label" id="choice_button_b">TOBIAS</div>
</div></body></html>"""

# EDGE (Q20 not_applicable): vignette OK + NINGÚN name label (ni selector ni nombres).
HTML_NO_NAMES = """<!DOCTYPE html><html><head>
<style>.vig { background: radial-gradient(circle, transparent, black); }</style>
</head><body>
<div id="root"><div class="vig"></div>
  <div class="caption-wrap">algo de narración sin nombres de personaje</div>
</div></body></html>"""

# TRAMPA: 'monospace' SOLO en comentario + name mencionado SOLO en comentario.
# Q20 debe seguir FAIL (names detectados por selector choice_button, mono solo en
# comentario NO cuenta como fuente declarada... pero nuestro check busca mono en
# todo el HTML incluyendo comentarios — esta fixture documenta que la señal
# load-bearing es el selector de label, y verifica el detector de nombres-en-texto
# ignora comentarios).
HTML_NAME_IN_COMMENT_ONLY = """<!DOCTYPE html><html><head>
<style>.vignette{box-shadow:inset 0 0 100px black;} .name-label{font-family:Georgia,serif;}</style>
</head><body>
<div id="root">
  <div class="vignette"></div>
  <!-- DARIO y TOBIAS son los personajes; deberían ir en monospace -->
  <div class="caption-wrap">solo narración aquí</div>
</div></body></html>"""

CHARACTER_NAMES = ["Dario", "Tobias"]


class TestEvaluateVignette(unittest.TestCase):
    def test_radial_gradient_passes(self):
        ok, d = mod.evaluate_vignette(HTML_HEALTHY)
        self.assertTrue(ok)
        self.assertEqual(d["status"], "ok")

    def test_box_shadow_inset_passes(self):
        ok, _ = mod.evaluate_vignette(HTML_NAMES_NO_MONO)
        self.assertTrue(ok, "box-shadow ... inset debe contar como vignette")

    def test_literal_vignette_word_passes(self):
        ok, _ = mod.evaluate_vignette('<div class="vignette-overlay"></div>')
        self.assertTrue(ok)

    def test_no_vignette_fails(self):
        ok, d = mod.evaluate_vignette(HTML_NO_VIGNETTE)
        self.assertFalse(ok, "HTML sin vignette debe FALLAR Q19 (bug histórico)")
        self.assertEqual(d["status"], "fail")

    def test_box_shadow_without_inset_not_vignette(self):
        # drop-shadow normal (offset, no inset) NO es vignette
        ok, _ = mod.evaluate_vignette('<div style="box-shadow:2px 2px 0 black;"></div>')
        self.assertFalse(ok, "box-shadow sin inset NO es vignette")


class TestEvaluateMonoNames(unittest.TestCase):
    def test_names_with_mono_passes(self):
        ok, d = mod.evaluate_mono_names(HTML_HEALTHY, CHARACTER_NAMES)
        self.assertTrue(ok)
        self.assertEqual(d["status"], "ok")
        self.assertTrue(d["applies"])

    def test_names_without_mono_fails(self):
        ok, d = mod.evaluate_mono_names(HTML_NAMES_NO_MONO, CHARACTER_NAMES)
        self.assertFalse(ok, "name labels en Arial (proportional) deben FALLAR Q20")
        self.assertEqual(d["status"], "fail")
        self.assertTrue(d["applies"])

    def test_no_name_labels_not_applicable(self):
        ok, d = mod.evaluate_mono_names(HTML_NO_NAMES, CHARACTER_NAMES)
        self.assertTrue(ok, "sin name labels → Q20 not_applicable (NO FAIL)")
        self.assertEqual(d["status"], "not_applicable")
        self.assertFalse(d["applies"])

    def test_detection_by_selector_when_text_burned(self):
        # name labels detectados por selector choice_button aunque el texto
        # del nombre no esté presente (texto horneado en el clip, HR#25)
        html = ('<style>.x{font-family:monospace}</style>'
                '<div id="choice_button_a"></div>')
        present, _ = mod.detect_name_labels(html, [])
        self.assertTrue(present, "selector choice_button debe contar como name label")

    def test_name_only_in_comment_does_not_trigger(self):
        # los nombres SOLO en comentario no deben disparar detección por-texto;
        # pero el selector choice_button está ausente acá → no aplica.
        present, ev = mod.detect_name_labels(HTML_NAME_IN_COMMENT_ONLY, CHARACTER_NAMES)
        self.assertFalse(present,
                         "nombre solo en comentario HTML + sin selector → no hay label")
        self.assertEqual(ev["name_text_hits"], [])

    def test_mono_fonts_override(self):
        html = ('<div class="name-label">DARIO</div>'
                '<style>.name-label{font-family:"Brand Mono";}</style>')
        # con default NO está → fail
        ok_default, _ = mod.evaluate_mono_names(html, CHARACTER_NAMES)
        self.assertFalse(ok_default)
        # con override que incluye Brand Mono → pass
        ok_override, _ = mod.evaluate_mono_names(
            html, CHARACTER_NAMES, mono_fonts=("Brand Mono",))
        self.assertTrue(ok_override)


class TestEvaluateCombined(unittest.TestCase):
    def test_healthy_overall_pass(self):
        ok, checks = mod.evaluate_style_markup(HTML_HEALTHY, CHARACTER_NAMES)
        self.assertTrue(ok)
        self.assertEqual(checks["Q19_vignette"]["status"], "ok")
        self.assertEqual(checks["Q20_monospaced_names"]["status"], "ok")

    def test_no_vignette_overall_fail(self):
        ok, checks = mod.evaluate_style_markup(HTML_NO_VIGNETTE, CHARACTER_NAMES)
        self.assertFalse(ok)
        self.assertEqual(checks["Q19_vignette"]["status"], "fail")

    def test_names_no_mono_overall_fail(self):
        ok, checks = mod.evaluate_style_markup(HTML_NAMES_NO_MONO, CHARACTER_NAMES)
        self.assertFalse(ok)
        self.assertEqual(checks["Q20_monospaced_names"]["status"], "fail")

    def test_no_names_q20_na_overall_pass(self):
        ok, checks = mod.evaluate_style_markup(HTML_NO_NAMES, CHARACTER_NAMES)
        self.assertTrue(ok, "Q19 ok + Q20 not_applicable → overall pass")
        self.assertEqual(checks["Q20_monospaced_names"]["status"], "not_applicable")


# ─────────── tests de integración runtime (SPEC + HTML en tempfile) ───────────

def _write(tmp, name, content):
    p = Path(tmp) / name
    p.write_text(content, encoding="utf-8")
    return p


def _spec_yaml(*, has_captions=True, with_caps=True, names=("Dario", "Tobias")):
    chars = "\n".join(
        f'  - character_id: "c{i}"\n    name: "{n}"' for i, n in enumerate(names))
    caps = ""
    if with_caps:
        caps = ("video_capabilities:\n"
                f"  has_captions_baked: {str(bool(has_captions)).lower()}\n"
                "  has_ai_generated_clips: true\n")
    return f"{caps}characters:\n{chars}\n"


def _run(spec_path, html_path=None, extra=None):
    cmd = [sys.executable, str(_SCRIPT), "--format", "horror-choice", "--spec", str(spec_path)]
    if html_path:
        cmd += ["--html", str(html_path)]
    if extra:
        cmd += extra
    return subprocess.run(cmd, capture_output=True, text=True)


class TestRuntime(unittest.TestCase):
    def test_healthy_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml())
            html = _write(tmp, "index.html", HTML_HEALTHY)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(json.loads(r.stdout)["overall_status"], "pass")

    def test_no_vignette_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml())
            html = _write(tmp, "index.html", HTML_NO_VIGNETTE)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("Q19_vignette", json.loads(r.stdout)["fail_checks"])

    def test_names_no_mono_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml())
            html = _write(tmp, "index.html", HTML_NAMES_NO_MONO)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("Q20_monospaced_names", json.loads(r.stdout)["fail_checks"])

    def test_no_names_q20_na_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            # SPEC sin characters[] + HTML sin name labels → Q20 na, Q19 ok
            spec = _write(tmp, "s.yaml", "video_capabilities:\n  has_captions_baked: true\n")
            html = _write(tmp, "index.html", HTML_NO_NAMES)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            out = json.loads(r.stdout)
            self.assertEqual(out["overall_status"], "pass")
            self.assertEqual(out["checks"]["Q20_monospaced_names"]["status"], "not_applicable")

    def test_capability_gate_not_applicable_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml(has_captions=False))
            # HTML inválido a propósito: si el gate corriera, fallaría — pero NO debe correr
            html = _write(tmp, "index.html", HTML_NO_VIGNETTE)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertEqual(json.loads(r.stdout)["overall_status"], "not_applicable")

    def test_missing_capabilities_bug9_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml(with_caps=False))
            html = _write(tmp, "index.html", HTML_HEALTHY)
            r = _run(spec, html)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
            self.assertIn("video_capabilities", r.stderr)

    def test_missing_html_bug9_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml())
            r = _run(spec, html_path=Path(tmp) / "nope.html")
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_format_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "s.yaml", _spec_yaml())
            r = subprocess.run(
                [sys.executable, str(_SCRIPT), "--spec", str(spec)],
                capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0, "--format es REQUIRED (agnostic-by-design)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
