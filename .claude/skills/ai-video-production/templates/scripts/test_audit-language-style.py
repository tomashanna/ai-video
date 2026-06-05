#!/usr/bin/env python3
"""test_audit-language-style.py — HR#26 companion test de audit-language-style.py.

Modela los 4 CASOS DISPARADORES HISTÓRICOS (bugs shipped reales): cada uno DEBE FALLAR
el gate. Más: caso sano que PASA + edge cases (vosotros NO es voseo; 'sos un' SÍ; oficio en
descripción válido; handle reference en comentario válido; --checks selectivo).

Corre: python3 test_audit-language-style.py
"""
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

# import por path (nombre con guiones → no importable normal)
_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("audit_language_style", _HERE / "audit-language-style.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


# ─────────────────────────────────────────────────────────────────────────────
# Lógica pura — VOSEO (caso disparador: matadero shipped con voseo)
# ─────────────────────────────────────────────────────────────────────────────
class TestVoseoPure(unittest.TestCase):
    def test_disparador_matadero_eligis_te_convertis(self):
        # CASO HISTÓRICO: matadero post-ship 2026-05-20 shipeó con voseo.
        texts = [{"source": "narration[0]", "text": "Si elegís a Bruno, te convertís en algo más."}]
        ok, findings = mod.evaluate_voseo(texts)
        self.assertFalse(ok, "el voseo del matadero DEBE fallar el gate")
        self.assertIn("elegís", findings[0]["hits"])

    def test_sano_neutral_pasa(self):
        texts = [{"source": "n", "text": "Si eliges a Dario, bajas al túnel. Ahora decides."}]
        ok, findings = mod.evaluate_voseo(texts)
        self.assertTrue(ok)
        self.assertEqual(findings, [])

    def test_edge_vosotros_no_es_voseo(self):
        # falso-positivo a evitar: 'vosotros' NO debe matchear 'vos'
        texts = [{"source": "n", "text": "Vosotros no entendéis nada de esto."}]
        ok, _ = mod.evaluate_voseo(texts)
        self.assertTrue(ok, "'vosotros' NO es voseo (word-boundary)")

    def test_edge_sos_un_es_voseo(self):
        # 'sos un' SÍ es voseo standalone (regla explícita de la tarea)
        texts = [{"source": "n", "text": "Vos sos un cobarde."}]
        ok, findings = mod.evaluate_voseo(texts)
        self.assertFalse(ok)
        self.assertIn("sos", findings[0]["hits"])
        self.assertIn("vos", findings[0]["hits"])

    def test_edge_acento_word_boundary(self):
        # 'podés/tenés' con acento dentro de oración real
        texts = [{"source": "n", "text": "No tenés escapatoria, no podés correr."}]
        ok, findings = mod.evaluate_voseo(texts)
        self.assertFalse(ok)
        self.assertIn("tenés", findings[0]["hits"])
        self.assertIn("podés", findings[0]["hits"])


# ─────────────────────────────────────────────────────────────────────────────
# Lógica pura — CLICHÉ (caso disparador: matadero frases overused)
# ─────────────────────────────────────────────────────────────────────────────
class TestClichePure(unittest.TestCase):
    def test_disparador_cena_que_nunca_acaba(self):
        texts = [{"source": "n", "text": "Bienvenido a la cena que nunca acaba."}]
        ok, findings = mod.evaluate_cliche(texts)
        self.assertFalse(ok, "cliché 'cena que nunca acaba' DEBE fallar")
        self.assertIn("cena que nunca acaba", findings[0]["hits"])

    def test_case_insensitive(self):
        texts = [{"source": "n", "text": "Es un BUCLE ETERNO sin salida."}]
        ok, findings = mod.evaluate_cliche(texts)
        self.assertFalse(ok)
        self.assertIn("bucle eterno", findings[0]["hits"])

    def test_sano_original_pasa(self):
        texts = [{"source": "n", "text": "La descarga te lanza hacia atrás contra el riel."}]
        ok, _ = mod.evaluate_cliche(texts)
        self.assertTrue(ok)

    def test_extra_cliche_extensible(self):
        texts = [{"source": "n", "text": "frase prohibida custom"}]
        ok, findings = mod.evaluate_cliche(texts, phrases=mod.CLICHE_PHRASES + ("frase prohibida custom",))
        self.assertFalse(ok)


# ─────────────────────────────────────────────────────────────────────────────
# Lógica pura — NAMES (caso disparador: cinema-abandonado 'Proyector'/'Acomodador')
# ─────────────────────────────────────────────────────────────────────────────
class TestNamesPure(unittest.TestCase):
    def test_disparador_cinema_proyector(self):
        names = [{"source": "characters[char_a].name", "name": "Proyector"}]
        ok, findings = mod.evaluate_names(names)
        self.assertFalse(ok, "name 'Proyector' (oficio) DEBE fallar")
        self.assertEqual(findings[0]["hit"], "Proyector")

    def test_disparador_matarife_name(self):
        names = [{"source": "characters[char_a].name", "name": "Matarife"}]
        ok, _ = mod.evaluate_names(names)
        self.assertFalse(ok, "name 'Matarife' (oficio) DEBE fallar")

    def test_bruno_con_descripcion_oficio_pasa(self):
        # CLAVE: 'Bruno' con description 'matarife del pueblo' PASA — la descripción
        # NO se alimenta a evaluate_names (solo el name field). Modelamos eso: el name es Bruno.
        names = [{"source": "characters[char_a].name", "name": "Bruno"}]
        ok, _ = mod.evaluate_names(names)
        self.assertTrue(ok, "'Bruno' es nombre real válido aunque su oficio sea matarife")

    def test_real_names_pasan(self):
        names = [
            {"source": "characters[char_a].name", "name": "Dario"},
            {"source": "characters[char_b].name", "name": "Tobias"},
        ]
        ok, _ = mod.evaluate_names(names)
        self.assertTrue(ok)


# ─────────────────────────────────────────────────────────────────────────────
# Lógica pura — HANDLE (caso disparador: handle propio @referent-a)
# ─────────────────────────────────────────────────────────────────────────────
class TestHandlePure(unittest.TestCase):
    def test_disparador_conspiracion_como_handle_propio(self):
        handles = [{"source": "channel_signature.watermark_handle", "handle": "@referent-a"}]
        ok, findings = mod.evaluate_handle(handles)
        self.assertFalse(ok, "@referent-a como handle propio DEBE fallar")
        self.assertIn("reference-only", findings[0]["detail"])

    def test_canonical_pasa(self):
        handles = [{"source": "meta.watermark", "handle": "@elige_tucompanero"}]
        ok, _ = mod.evaluate_handle(handles)
        self.assertTrue(ok)

    def test_otro_handle_no_canonico_falla(self):
        handles = [{"source": "meta.watermark", "handle": "@random_channel"}]
        ok, _ = mod.evaluate_handle(handles)
        self.assertFalse(ok)


# ─────────────────────────────────────────────────────────────────────────────
# Extracción + wrapper (end-to-end con SPEC sintético en tempfile)
# ─────────────────────────────────────────────────────────────────────────────
_SYNTH_BUGGY = """
video_capabilities:
  has_ai_generated_clips: true
  format_type: interactive_choice
project:
  channel: "@referent-a"
characters:
  - character_id: char_a
    name: "Matarife"
    visual_signature: "el matarife del pueblo, delantal ensangrentado"
narration_script:
  - segment_id: seg_1
    text_canonical: "Si elegís a Matarife, vivís la cena que nunca acaba."
shot_list:
  - shot_id: shot_01
    dialog_text: "Matarife: vení, no tengas miedo."
    ui_overlay_elements:
      - {element_id: warning_caption_setting, text: "EL TÚNEL SE CIERRA"}
      - {element_id: name_label_char_a, text: "MATARIFE"}
"""

_SYNTH_CLEAN = """
video_capabilities:
  has_ai_generated_clips: true
  format_type: interactive_choice
project:
  channel: "@elige_tucompanero"
characters:
  - character_id: char_a
    name: "Bruno"
    visual_signature: "el matarife del pueblo, delantal ensangrentado"
  - character_id: char_b
    name: "Dario"
narration_script:
  - segment_id: seg_1
    text_canonical: "Si eliges a Bruno, bajas al túnel. Ahora decides."
shot_list:
  - shot_id: shot_01
    dialog_text: "Bruno: ven conmigo, no tengas miedo."
    narration_in_this_shot: "El último tren ya pasó."
    ui_overlay_elements:
      - {element_id: warning_caption_setting, text: "EL TUNEL SE CIERRA HASTA EL AMANECER"}
      - {element_id: name_label_char_a, text: "BRUNO"}
"""

# SPEC con @referent-a SOLO como reference en un comentario yaml → NO debe fallar handle
_SYNTH_REFERENCE_ONLY = """
video_capabilities:
  has_ai_generated_clips: true
project:
  channel: "@elige_tucompanero"
# - ref-11 (@referent-a canon — REFERENCE only, excluido)
references_canonical:
  - ref_id: ref-03
    why_relevant: "calco de @referent-a estilo viral"
characters:
  - character_id: char_a
    name: "Dario"
narration_script:
  - segment_id: seg_1
    text_canonical: "Si eliges a Dario, bajas al túnel."
"""


class TestWrapperEndToEnd(unittest.TestCase):
    def _write(self, text):
        f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
        f.write(text)
        f.close()
        self.addCleanup(os.unlink, f.name)
        import yaml
        with open(f.name) as fh:
            return yaml.safe_load(fh)

    def test_buggy_spec_fails_all_four(self):
        spec = self._write(_SYNTH_BUGGY)
        ok, report = mod.run_checks(spec, None, list(mod.ALL_CHECKS))
        self.assertFalse(ok, "el SPEC con los 4 bugs DEBE fallar")
        self.assertEqual(report["voseo"]["status"], "fail")
        self.assertEqual(report["cliche"]["status"], "fail")
        self.assertEqual(report["names"]["status"], "fail")
        self.assertEqual(report["handle"]["status"], "fail")

    def test_clean_spec_passes_all_four(self):
        spec = self._write(_SYNTH_CLEAN)
        ok, report = mod.run_checks(spec, None, list(mod.ALL_CHECKS))
        self.assertTrue(ok, f"el SPEC sano DEBE pasar; report={report}")

    def test_reference_only_handle_passes(self):
        # @referent-a en comentario/why_relevant NO es handle propio → handle PASS
        spec = self._write(_SYNTH_REFERENCE_ONLY)
        ok, report = mod.run_checks(spec, None, ["handle"])
        self.assertTrue(ok, "mención reference de @referent-a NO debe fallar handle")

    def test_selective_checks(self):
        # SPEC buggy pero solo corremos 'names' → falla names, no evalúa el resto
        spec = self._write(_SYNTH_BUGGY)
        ok, report = mod.run_checks(spec, None, ["names"])
        self.assertFalse(ok)
        self.assertIn("names", report)
        self.assertNotIn("voseo", report)

    def test_caption_text_checked_not_name_label(self):
        # captions (warning) SÍ se chequean; name_label NO (es UI cromo, no narrativa).
        spec = self._write("""
video_capabilities: {has_ai_generated_clips: true}
shot_list:
  - shot_id: shot_01
    ui_overlay_elements:
      - {element_id: warning_caption_x, text: "no tenés salida"}
      - {element_id: name_label_char_a, text: "no tenés salida"}
""")
        texts = mod.collect_texts(spec)
        srcs = [t["source"] for t in texts]
        self.assertTrue(any("warning_caption_x" in s for s in srcs))
        self.assertFalse(any("name_label" in s for s in srcs),
                         "name_label NO debe entrar a los textos chequeados por estilo")

    def test_html_watermark_extraction(self):
        spec = self._write("video_capabilities: {has_ai_generated_clips: true}\n")
        html = '<div class="watermark-handle">@referent-a</div>'
        handles = mod.collect_handles(spec, html)
        self.assertTrue(any(h["handle"] == "@referent-a" for h in handles))
        ok, _ = mod.evaluate_handle(handles)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main(verbosity=2)
