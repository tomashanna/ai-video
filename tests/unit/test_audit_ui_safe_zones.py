#!/usr/bin/env python3
"""test_audit-ui-safe-zones.py — HR#26 companion test de audit-ui-safe-zones.py.

Modela el CASO DISPARADOR HISTÓRICO (drift Y48/Y52 + F1 ignorado, 2026-06-04):
  - El bug real (loading bar pegada al countdown <6pp / caption fuera de la banda
    F1 / name label fuera de banda) DEBE FALLAR el gate.
  - El layout canónico (caption Y62, loading Y52 con ≥6pp del countdown Y46) PASA.
  - Edge cases: capability-gate not_applicable, Bug #9, report-only (watermark +
    choice_buttons), elemento ausente = skipped, parseo px/% + translateY.

Correr: python3 test_audit-ui-safe-zones.py
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location("audit_ui_safe_zones", Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_ui_safe_zones.py")
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


# Bandas sintéticas estables (NO dependen de F1) para aislar la lógica pura.
SYNTH_BANDS = {
    "captions_narration": (53.5, 64.2, "F1-synth"),
    "character_name_labels": (22.0, 32.8, "F1-synth"),
    "warning_text": (31.7, 64.0, "F1-synth"),
    "loading_bar": (44.0, 52.0, "INGENIERO-CHOICE-CORE §2"),
    "countdown": (46.0, 46.0, "INGENIERO-CHOICE-CORE §2"),
}


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — style_to_y_pct
# ════════════════════════════════════════════════════════════════════════════
class TestStyleToYPct(unittest.TestCase):
    def test_top_pct_centered_translateY(self):
        # loading bar canónica: top:52% + translate(-50%,-50%) → centro 52%
        y = m.style_to_y_pct("position:absolute;top:52%;left:50%;transform:translate(-50%,-50%);height:16px;")
        self.assertAlmostEqual(y, 52.0, places=1)

    def test_bottom_px_with_height_anchor_bottom(self):
        # caption-wrap: bottom:540px;height:280px sobre 1920 → centro 64.6%
        y = m.style_to_y_pct("position:absolute;bottom:540px;height:280px;width:100%;")
        self.assertAlmostEqual(y, 64.6, places=1)

    def test_top_px_no_height(self):
        # name label class: top:220px sobre 1920 → 11.46%
        y = m.style_to_y_pct("position:absolute;top:220px;")
        self.assertAlmostEqual(y, 11.46, places=1)

    def test_translateX_only_not_centered_vertically(self):
        # watermark top:4% + translateX(-50%) → ancla superior 4% (NO centrado en Y)
        y = m.style_to_y_pct("position:absolute;top:4%;left:50%;transform:translateX(-50%);")
        self.assertAlmostEqual(y, 4.0, places=1)

    def test_no_vertical_anchor_returns_none(self):
        self.assertIsNone(m.style_to_y_pct("position:absolute;left:50%;width:100%;height:100%;"))

    def test_empty_style_none(self):
        self.assertIsNone(m.style_to_y_pct(""))


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — classify_element
# ════════════════════════════════════════════════════════════════════════════
class TestClassify(unittest.TestCase):
    def test_caption(self):
        self.assertEqual(m.classify_element("", "caption-wrap"), "captions_narration")

    def test_loading_bar(self):
        self.assertEqual(m.classify_element("loading_bar_decision", "loading_bar"), "loading_bar")

    def test_countdown(self):
        self.assertEqual(m.classify_element("countdown_3_2_1_hook", "countdown"), "countdown")

    def test_choice_button_not_name_label(self):
        # CASO REGRESIÓN: el botón A/B NO debe clasificar como name label (banda top).
        self.assertEqual(m.classify_element("choice_button_ivan", "choice_button"), "choice_buttons")

    def test_real_name_label(self):
        self.assertEqual(m.classify_element("name-mateo", "name-label name-label-left"),
                         "character_name_labels")

    def test_watermark(self):
        self.assertEqual(m.classify_element("watermark_handle", ""), "watermark")

    def test_unknown_returns_none(self):
        self.assertIsNone(m.classify_element("random_div", "some-class"))


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — evaluate_safe_zones
# ════════════════════════════════════════════════════════════════════════════
class TestEvaluate(unittest.TestCase):
    def test_canonical_layout_passes(self):
        """Layout sano: caption Y62, loading Y52, countdown Y46 (sep 6pp) → PASS."""
        els = [
            {"element_type": "captions_narration", "y_pct": 62.0, "raw": "caption"},
            {"element_type": "loading_bar", "y_pct": 52.0, "raw": "loading"},
            {"element_type": "countdown", "y_pct": 46.0, "raw": "cd"},
        ]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertTrue(ok, [r["detail"] for r in reasons if r["status"] == "fail"])

    def test_drift_caption_out_of_band_fails(self):
        """CASO DISPARADOR: caption hardcodeado fuera de la banda F1 → FAIL."""
        els = [{"element_type": "captions_narration", "y_pct": 40.0, "raw": "caption-wrap"}]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertFalse(ok)
        self.assertTrue(any(r["status"] == "fail" and r["element_type"] == "captions_narration"
                            for r in reasons))

    def test_loading_overlaps_countdown_fails(self):
        """CASO DISPARADOR núcleo (drift Y48/Y52): loading bar pegada al countdown.

        Loading Y48 + countdown Y46 → sep 2pp < 6pp → FAIL. Es EXACTAMENTE el
        overlap que motivó revisar Y48→Y52 en INGENIERO-CHOICE-CORE §2.6.
        """
        els = [
            {"element_type": "loading_bar", "y_pct": 48.0, "raw": "loading"},
            {"element_type": "countdown", "y_pct": 46.0, "raw": "cd"},
        ]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertFalse(ok)
        sep_fail = [r for r in reasons if r["element_type"] == "loading_bar↔countdown"]
        self.assertEqual(len(sep_fail), 1)
        self.assertEqual(sep_fail[0]["status"], "fail")

    def test_loading_y52_separated_passes(self):
        """El FIX canónico: loading Y52 + countdown Y46 → sep 6pp ≥ 6pp → PASS."""
        els = [
            {"element_type": "loading_bar", "y_pct": 52.0, "raw": "loading"},
            {"element_type": "countdown", "y_pct": 46.0, "raw": "cd"},
        ]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertTrue(ok, [r["detail"] for r in reasons if r["status"] == "fail"])
        sep = [r for r in reasons if r["element_type"] == "loading_bar↔countdown"]
        self.assertEqual(sep[0]["status"], "ok")

    def test_name_label_out_of_band_fails(self):
        els = [{"element_type": "character_name_labels", "y_pct": 60.0, "raw": "name-x"}]
        ok, _ = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertFalse(ok)

    def test_tolerance_edge_inside(self):
        # caption band hi=64.2, +2pp = 66.2 → 66.0 dentro
        els = [{"element_type": "captions_narration", "y_pct": 66.0, "raw": "c"}]
        ok, _ = m.evaluate_safe_zones(els, SYNTH_BANDS, tolerance_pp=2.0)
        self.assertTrue(ok)

    def test_tolerance_edge_outside(self):
        # 66.3 > 64.2+2.0 → fuera
        els = [{"element_type": "captions_narration", "y_pct": 66.3, "raw": "c"}]
        ok, _ = m.evaluate_safe_zones(els, SYNTH_BANDS, tolerance_pp=2.0)
        self.assertFalse(ok)

    def test_watermark_report_only_never_fails(self):
        """Watermark Y4 (canónico top) NO debe fallar aunque la banda F1 sea Y77-84."""
        els = [{"element_type": "watermark", "y_pct": 4.0, "raw": "wm"}]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertTrue(ok)
        self.assertEqual(reasons[0]["status"], "skipped")

    def test_choice_buttons_report_only_never_fails(self):
        """Botón A/B Y75 (bottom-anchored) NO debe fallar contra banda name-label top."""
        els = [{"element_type": "choice_buttons", "y_pct": 75.0, "raw": "btn"}]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertTrue(ok)
        self.assertEqual(reasons[0]["status"], "skipped")

    def test_element_absent_is_not_a_fail(self):
        """Sin overlays = PASS (path HYBRID sin divs estructurales)."""
        ok, reasons = m.evaluate_safe_zones([], SYNTH_BANDS)
        self.assertTrue(ok)
        self.assertEqual(reasons, [])

    def test_unparseable_y_is_skipped(self):
        els = [{"element_type": "countdown", "y_pct": None, "raw": "cd-fullframe"}]
        ok, reasons = m.evaluate_safe_zones(els, SYNTH_BANDS)
        self.assertTrue(ok)
        self.assertEqual(reasons[0]["status"], "skipped")


# ════════════════════════════════════════════════════════════════════════════
# WRAPPER RUNTIME — parse_html_overlays + main (capability gate / Bug #9)
# ════════════════════════════════════════════════════════════════════════════
def _write(tmp, name, text):
    p = Path(tmp) / name
    p.write_text(text, encoding="utf-8")
    return str(p)


CAPS_OK = """
video_capabilities:
  has_captions_baked: true
  format_type: "interactive_choice"
  output_resolution: "1080x1920"
"""

CAPS_NOT_APPLICABLE = """
video_capabilities:
  has_captions_baked: false
  format_type: "youtube_long"
  output_resolution: "1920x1080"
"""

CAPS_MISSING = """
title: "no capabilities block"
shot_list: []
"""

# index.html que reproduce el BUG: loading bar Y48 pegada al countdown Y46.
HTML_BUG = """<!DOCTYPE html><html><body>
<div id="root">
<div class="caption-wrap" style="position:absolute;bottom:540px;height:280px;width:100%;"></div>
<div id="loading_bar_decision" class="loading_bar" style="position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);width:900px;height:16px;"></div>
<div id="countdown_pt" class="countdown" style="position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);width:200px;height:200px;"></div>
</div></body></html>
"""

# index.html canónico: loading Y52, countdown Y46 (sep 6pp), caption Y62.
HTML_OK = """<!DOCTYPE html><html><body>
<div id="root">
<div class="caption-wrap" style="position:absolute;bottom:540px;height:280px;width:100%;"></div>
<div id="loading_bar_decision" class="loading_bar" style="position:absolute;top:52%;left:50%;transform:translate(-50%,-50%);width:900px;height:16px;"></div>
<div id="countdown_pt" class="countdown" style="position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);width:200px;height:200px;"></div>
<div id="watermark_handle" style="position:absolute;top:4%;left:50%;transform:translateX(-50%);">@elige_tucompanero</div>
</div></body></html>
"""


class TestParseHtml(unittest.TestCase):
    def test_extracts_and_classifies(self):
        els = m.parse_html_overlays(HTML_OK)
        types = {e["element_type"] for e in els}
        self.assertIn("captions_narration", types)
        self.assertIn("loading_bar", types)
        self.assertIn("countdown", types)
        self.assertIn("watermark", types)

    def test_loading_and_countdown_centered_y(self):
        els = {e["element_type"]: e["y_pct"] for e in m.parse_html_overlays(HTML_OK)}
        self.assertAlmostEqual(els["loading_bar"], 52.0, places=1)
        self.assertAlmostEqual(els["countdown"], 46.0, places=1)


class TestMainRuntime(unittest.TestCase):
    def _run(self, caps_text, html_text, extra=None):
        with tempfile.TemporaryDirectory() as tmp:
            spec = _write(tmp, "spec.yaml", caps_text)
            html = _write(tmp, "index.html", html_text)
            argv = ["prog", "--format", "horror-choice", "--spec", spec, "--html", html]
            if extra:
                argv += extra
            import sys
            old = sys.argv
            sys.argv = argv
            try:
                # silenciar el JSON del gate (main() imprime su reporte a stdout)
                with contextlib.redirect_stdout(io.StringIO()), \
                        contextlib.redirect_stderr(io.StringIO()):
                    return m.main()
            finally:
                sys.argv = old

    def test_bug_html_fails_exit_1(self):
        """CASO DISPARADOR end-to-end: HTML con loading Y48 pegada al countdown → exit 1."""
        self.assertEqual(self._run(CAPS_OK, HTML_BUG), 1)

    def test_canonical_html_passes_exit_0(self):
        self.assertEqual(self._run(CAPS_OK, HTML_OK), 0)

    def test_not_applicable_exit_0(self):
        """format_type youtube_long + horizontal → HR#4 no aplica → exit 0."""
        self.assertEqual(self._run(CAPS_NOT_APPLICABLE, HTML_BUG), 0)

    def test_missing_capabilities_bug9_exit_2(self):
        self.assertEqual(self._run(CAPS_MISSING, HTML_OK), 2)

    def test_loading_band_override(self):
        """Override --loading-band 44,48 hace que loading Y52 caiga FUERA → exit 1
        (demuestra que la constante es overridable, autoridad CLI)."""
        rc = self._run(CAPS_OK, HTML_OK, extra=["--loading-band", "44,48"])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
