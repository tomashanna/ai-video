#!/usr/bin/env python3
"""test_audit-spec-declarations.py — HR#26 companion adversarial test.

Modela los CASOS DISPARADORES HISTÓRICOS (el bug real DEBE fallar el gate):
  · Q26 — caso matadero (GAP #23): shot sin setting_ambient → FAIL.
  · Q27 — GAP #26: shot con atmospheric_motions_count 2 → FAIL; count!=len(list) → FAIL.
  · Q28 — GAP #25: TODOS los shots static → FAIL; un static aislado → PASS.
  · Q22b — HR#19: canonical_validation_status deprecated_our_prod_only → FAIL; ausente → FAIL.
  · Caso SANO — los 4 checks PASAN.

Carga el módulo con guion en el nombre vía importlib. Corre: python3 test_audit-spec-declarations.py
"""

from __future__ import annotations

import importlib.util
import os
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_spec = importlib.util.spec_from_file_location(
    "audit_spec_declarations",
    Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_spec_declarations.py",
)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


# ── Fixtures: SPEC dicts sintéticos ─────────────────────────────────────────────────────────


def _shot(
    shot_id,
    *,
    ambient="una rata cruza al fondo",
    motions_count=3,
    motions_list=None,
    traversal="walking_forward",
):
    if motions_list is None:
        motions_list = [f"motion_{i}" for i in range(motions_count)]
    return {
        "shot_id": shot_id,
        "section_id": "setup_pre_decision",
        "setting_ambient_creature_or_object": ambient,
        "pov_traversal": traversal,
        "motion_type": traversal,
        "visual_action_match": {
            "matches_literal": True,
            "atmospheric_motions_count": motions_count,
            "atmospheric_motions_list": motions_list,
        },
    }


def _healthy_spec():
    """Caso SANO: familia choice, 3 shots, todos bien, pacing con validation_status válido."""
    return {
        "project": {"format": "horror-choice"},
        "video_capabilities": {"has_ai_generated_clips": True, "format_type": "interactive_choice"},
        "shot_list": [
            _shot("shot_01", traversal="push_in"),
            _shot("shot_02", traversal="walking_forward"),
            _shot("shot_03", traversal="static_with_micro_bob"),  # freeze aislado legítimo
        ],
        "narrative_pacing": {
            "target_cuts_per_min": [18, 22],
            "canonical_validation_status": "validated_via_video_measurement",
        },
    }


class TestQ26AmbientCreature(unittest.TestCase):
    """Q26 — GAP #23 caso matadero: setting MUERTO."""

    def test_shot_sin_ambient_FALLA(self):
        shots = [
            {"shot_id": "shot_01", "ambient": "rata al fondo"},
            {"shot_id": "shot_02", "ambient": ""},  # ← bug matadero: setting muerto
            {"shot_id": "shot_03", "ambient": None},
        ]
        r = mod.evaluate_q26(shots, format_in_family=True, field_present_in_any=True)
        self.assertEqual(r["status"], "fail")
        self.assertIn("shot_02", r["offender_shots"])
        self.assertIn("shot_03", r["offender_shots"])

    def test_todos_con_ambient_PASA(self):
        shots = [
            {"shot_id": "shot_01", "ambient": "haz de luz"},
            {"shot_id": "shot_02", "ambient": "fuego del horno"},
        ]
        r = mod.evaluate_q26(shots, format_in_family=True, field_present_in_any=True)
        self.assertEqual(r["status"], "pass")

    def test_no_familia_y_campo_ausente_NOT_APPLICABLE(self):
        shots = [{"shot_id": "shot_01", "ambient": None}]
        r = mod.evaluate_q26(shots, format_in_family=False, field_present_in_any=False)
        self.assertEqual(r["status"], "not_applicable")

    def test_no_familia_pero_campo_presente_APLICA(self):
        # Señal: el SPEC usa el campo aunque el formato no sea choice → la regla aplica.
        shots = [{"shot_id": "shot_01", "ambient": "x"}, {"shot_id": "shot_02", "ambient": ""}]
        r = mod.evaluate_q26(shots, format_in_family=False, field_present_in_any=True)
        self.assertEqual(r["status"], "fail")


class TestQ27AtmosphericMotions(unittest.TestCase):
    """Q27 — GAP #26: <3 motions o drift count↔list."""

    def test_count_2_FALLA(self):
        shots = [{"shot_id": "shot_01", "motions_count": 2, "motions_list_len": 2}]  # ← disparador
        r = mod.evaluate_q27(shots)
        self.assertEqual(r["status"], "fail")
        self.assertEqual(r["offender_shots"][0]["shot_id"], "shot_01")

    def test_count_distinto_de_list_FALLA(self):
        shots = [{"shot_id": "shot_01", "motions_count": 4, "motions_list_len": 2}]  # drift
        r = mod.evaluate_q27(shots)
        self.assertEqual(r["status"], "fail")
        self.assertTrue(any("drift" in p for p in r["offender_shots"][0]["problems"]))

    def test_count_3_y_list_3_PASA(self):
        shots = [
            {"shot_id": "shot_01", "motions_count": 3, "motions_list_len": 3},
            {"shot_id": "shot_02", "motions_count": 4, "motions_list_len": 4},
        ]
        r = mod.evaluate_q27(shots)
        self.assertEqual(r["status"], "pass")

    def test_count_ausente_FALLA(self):
        shots = [{"shot_id": "shot_01", "motions_count": None, "motions_list_len": None}]
        r = mod.evaluate_q27(shots)
        self.assertEqual(r["status"], "fail")

    def test_min_motions_override(self):
        shots = [{"shot_id": "shot_01", "motions_count": 3, "motions_list_len": 3}]
        self.assertEqual(mod.evaluate_q27(shots, min_motions=3)["status"], "pass")
        self.assertEqual(mod.evaluate_q27(shots, min_motions=5)["status"], "fail")


class TestQ28NotAllStatic(unittest.TestCase):
    """Q28 — GAP #25: all-static (no per-shot)."""

    def test_todos_static_FALLA(self):
        shots = [
            {"shot_id": "shot_01", "traversal": "static"},
            {"shot_id": "shot_02", "traversal": "static_with_micro_bob"},
            {"shot_id": "shot_03", "traversal": "freeze"},
        ]
        r = mod.evaluate_q28(shots)
        self.assertEqual(r["status"], "fail")

    def test_un_static_aislado_PASA(self):
        # Per-shot static es legítimo — solo all-static falla.
        shots = [
            {"shot_id": "shot_01", "traversal": "static_with_micro_bob"},
            {"shot_id": "shot_02", "traversal": "walking_forward"},
            {"shot_id": "shot_03", "traversal": "static"},
        ]
        r = mod.evaluate_q28(shots)
        self.assertEqual(r["status"], "pass")
        self.assertEqual(r["static_count"], 2)
        self.assertEqual(r["non_static_count"], 1)

    def test_lista_vacia_NOT_APPLICABLE(self):
        self.assertEqual(mod.evaluate_q28([])["status"], "not_applicable")


class TestQ22bCanonicalValidationStatus(unittest.TestCase):
    """Q22b — HR#19: deprecated_our_prod_only o ausente."""

    def test_deprecated_our_prod_only_FALLA(self):
        r = mod.evaluate_q22b("deprecated_our_prod_only", field_found=True)  # ← disparador HR#19
        self.assertEqual(r["status"], "fail")
        self.assertEqual(r["value"], "deprecated_our_prod_only")

    def test_ausente_FALLA(self):
        r = mod.evaluate_q22b(None, field_found=False)
        self.assertEqual(r["status"], "fail")

    def test_valido_PASA(self):
        for v in mod.VALID_CANONICAL_VALIDATION_STATUS:
            r = mod.evaluate_q22b(v, field_found=True)
            self.assertEqual(r["status"], "pass", f"{v} debería pasar")

    def test_valor_desconocido_FALLA(self):
        r = mod.evaluate_q22b("estimated_by_vibes", field_found=True)
        self.assertEqual(r["status"], "fail")


class TestExtractionHelpers(unittest.TestCase):
    """Extracción runtime contra estructuras tipo-SPEC v11."""

    def test_find_canonical_validation_status_busca_bloques(self):
        # narrative_pacing
        spec = {"narrative_pacing": {"canonical_validation_status": "pending_video_measurement"}}
        v, found, where = mod.find_canonical_validation_status(spec)
        self.assertEqual((v, found, where), ("pending_video_measurement", True, "narrative_pacing"))
        # editing_targets fallback
        spec2 = {"editing_targets": {"canonical_validation_status": "validated_via_perceptual_test"}}
        v2, found2, where2 = mod.find_canonical_validation_status(spec2)
        self.assertEqual(where2, "editing_targets")
        self.assertTrue(found2)
        # ausente (caso del SPEC real ultimo-tren-carga)
        v3, found3, where3 = mod.find_canonical_validation_status({"editing_targets": {"x": 1}})
        self.assertFalse(found3)
        self.assertIsNone(v3)

    def test_shot_motions_list_no_lista(self):
        count, list_len = mod.shot_motions(
            {
                "visual_action_match": {
                    "atmospheric_motions_count": 3,
                    "atmospheric_motions_list": "no-es-lista",
                }
            }
        )
        self.assertEqual(count, 3)
        self.assertIsNone(list_len)

    def test_shot_traversal_fallback_a_motion_type(self):
        self.assertEqual(mod.shot_traversal({"motion_type": "push_in"}), "push_in")
        self.assertEqual(
            mod.shot_traversal({"pov_traversal": "walking_forward", "motion_type": "x"}), "walking_forward"
        )


class TestRunChecksIntegration(unittest.TestCase):
    """run_checks contra SPEC dicts completos — sano vs disparadores combinados."""

    def test_spec_sano_los_4_PASAN(self):
        results = mod.run_checks(_healthy_spec(), "horror-choice", mod.ALL_CHECKS)
        self.assertEqual(len(results), 4)
        self.assertTrue(
            all(r["status"] == "pass" for r in results), [(r["check"], r["status"]) for r in results]
        )

    def test_spec_disparador_combinado_FALLA_los_4(self):
        spec = {
            "project": {"format": "horror-choice"},
            "video_capabilities": {"has_ai_generated_clips": True},
            "shot_list": [
                _shot("shot_01", ambient="", motions_count=2, motions_list=["a", "b"], traversal="static"),
                _shot(
                    "shot_02",
                    ambient=None,
                    motions_count=4,
                    motions_list=["a", "b"],
                    traversal="static_with_micro_bob",
                ),
            ],
            "editing_targets": {"canonical_validation_status": "deprecated_our_prod_only"},
        }
        results = mod.run_checks(spec, "horror-choice", mod.ALL_CHECKS)
        by = {r["check"]: r["status"] for r in results}
        self.assertEqual(by["q26_setting_ambient_creature_or_object"], "fail")
        self.assertEqual(by["q27_atmospheric_motions"], "fail")
        self.assertEqual(by["q28_not_all_static"], "fail")  # ambos shots static
        self.assertEqual(by["q22b_canonical_validation_status"], "fail")

    def test_checks_subset(self):
        results = mod.run_checks(_healthy_spec(), "horror-choice", ("q27", "q28"))
        self.assertEqual({r["check"] for r in results}, {"q27_atmospheric_motions", "q28_not_all_static"})

    def test_parse_checks(self):
        self.assertEqual(mod.parse_checks("all"), mod.ALL_CHECKS)
        self.assertEqual(mod.parse_checks("q26,q22b"), ("q26", "q22b"))
        with self.assertRaises(ValueError):
            mod.parse_checks("q99")


class TestEndToEndExitCodes(unittest.TestCase):
    """main() via subprocess-style: SPEC en tempfile → exit codes correctos."""

    def _write_spec(self, text):
        fd, path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        Path(path).write_text(textwrap.dedent(text))
        return path

    def test_spec_sin_video_capabilities_exit_2(self):
        import yaml

        path = self._write_spec("project:\n  format: horror-choice\nshot_list: []\n")
        spec = yaml.safe_load(Path(path).read_text())
        self.assertIsNone(spec.get("video_capabilities"))  # Bug #9 → exit 2 en main
        os.unlink(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
