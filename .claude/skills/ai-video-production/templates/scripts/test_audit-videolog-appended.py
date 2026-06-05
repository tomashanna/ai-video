#!/usr/bin/env python3
"""test_audit-videolog-appended.py — HR#26 companion adversarial test.

Modela los CASOS DISPARADORES (el video-log incompleto DEBE fallar el gate):
  · FIXTURE A — video-log SIN entry del proyecto → FAIL (Q15 learnings nunca appended).
  · FIXTURE B — entry SIN bullets (o <2) → FAIL.
  · FIXTURE C — entry completa (pattern + ≥2 bullets [+ score]) → PASS.
  · FIXTURE D — dos entries consecutivas mismo pattern + --check-rotation → FAIL (HR#14).
Más: pure functions (project_matches/extract_pattern/count_bullets/mentions_score/
rotation), parsing del .md (split_log_entries/parse_master_table_patterns) y exit codes.

Carga el módulo con guion en el nombre vía importlib. Corre: python3 test_audit-videolog-appended.py
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

_HERE = Path(__file__).parent
_SCRIPT = _HERE / "audit-videolog-appended.py"
_spec = importlib.util.spec_from_file_location("audit_videolog_appended", _SCRIPT)
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


# ── Fixtures: video-log.md sintéticos ────────────────────────────────────────────────────────

def _log_entry_complete(num=2, project="lago-helado", pattern="P9", prev_pattern="P1"):
    """Tabla maestra con 2 filas (rotación VÁLIDA por default: prev_pattern ≠ pattern) +
    sección ### de learnings completa para `project`."""
    return textwrap.dedent(f"""\
        # video-log.md — formato test

        ## Tabla maestra

        | # | Fecha | Proyecto | Pattern | Score | Status |
        |---|---|---|---|---|---|
        | 1 | 2026-05-01 | `previo-proyecto` | **{prev_pattern} — algo** | 9.8/10 | SHIPPED |
        | {num} | 2026-06-01 | `{project}` | **{pattern} — peligroso te ayuda** | 9.9/10 | ✅ SHIPPED |

        ## Learnings

        ### #{num} — {project} ({pattern})
        - Pattern {pattern} funcionó: el amenazante terminó salvando al viewer.
        - SFX densos matcheados subieron el sound design.
        - Atempo cap evitó la narración robótica.
        """)


def _log_no_entry():
    """FIXTURE A: el proyecto buscado NO está en ningún lado."""
    return textwrap.dedent("""\
        # video-log.md — formato test
        ## Tabla maestra
        | # | Fecha | Proyecto | Pattern | Score | Status |
        |---|---|---|---|---|---|
        | 1 | 2026-05-01 | `otro-proyecto` | **P1 — verdad visible** | 9.5/10 | SHIPPED |
        """)


def _log_entry_no_bullets(project="lago-helado", pattern="P9"):
    """FIXTURE B: entry existe + menciona pattern + score, pero SIN bullets de learnings."""
    return textwrap.dedent(f"""\
        # video-log.md — formato test
        ## Tabla maestra
        | # | Fecha | Proyecto | Pattern | Score | Status |
        |---|---|---|---|---|---|
        | 1 | 2026-05-01 | `previo` | **P1 — x** | 9.5/10 | SHIPPED |
        | 2 | 2026-06-01 | `{project}` | **{pattern} — y** | 9.9/10 | SHIPPED |

        ## Learnings
        ### #2 — {project} ({pattern})
        El video salió bien pero nadie escribió los aprendizajes en bullets.
        """)


def _log_two_consecutive_same_pattern(project="lago-helado"):
    """FIXTURE D: las dos últimas filas comparten pattern → rotación HR#14 viola."""
    return textwrap.dedent(f"""\
        # video-log.md — formato test
        ## Tabla maestra
        | # | Fecha | Proyecto | Pattern | Score | Status |
        |---|---|---|---|---|---|
        | 1 | 2026-05-01 | `previo` | **P6 — hedonismo** | 9.5/10 | SHIPPED |
        | 2 | 2026-06-01 | `{project}` | **P6 — hedonismo otra vez** | 9.9/10 | SHIPPED |

        ## Learnings
        ### #2 — {project} (P6)
        - Bullet uno de learnings.
        - Bullet dos de learnings.
        """)


def _write(text):
    fd, path = tempfile.mkstemp(suffix=".md")
    os.close(fd)
    Path(path).write_text(text, encoding="utf-8")
    return path


# ════════════════════════════════════════════════════════════════════════════════════════════
# PURE — funciones de decisión
# ════════════════════════════════════════════════════════════════════════════════════════════

class TestPureHelpers(unittest.TestCase):
    def test_project_matches_tolerante(self):
        self.assertTrue(mod.project_matches("| 7 | `matadero-banquete` v1 SHIP |", "matadero-banquete"))
        self.assertTrue(mod.project_matches("### #8 — sala_limpia_bioseguridad (V5)", "sala-limpia-bioseguridad"))
        self.assertFalse(mod.project_matches("| 1 | `otro-proyecto` |", "lago-helado"))

    def test_extract_pattern_tokens(self):
        self.assertEqual(mod.extract_pattern_tokens("**P9 — peligroso** y P9 de nuevo"), ["P9"])
        self.assertEqual(mod.extract_pattern_tokens("P10 — inversión, luego P6"), ["P10", "P6"])
        self.assertEqual(mod.extract_pattern_tokens("sin patterns acá"), [])

    def test_count_bullets_excluye_hr(self):
        text = "- uno\n* dos\n• tres\n---\ntexto normal\n  - indentado"
        self.assertEqual(mod.count_bullets(text), 4)
        self.assertEqual(mod.count_bullets("---\n----"), 0)

    def test_mentions_score(self):
        self.assertTrue(mod.mentions_score("Score 9.9/10 final"))
        self.assertTrue(mod.mentions_score("10.0/10"))
        self.assertTrue(mod.mentions_score("Gemini 9.7"))
        self.assertFalse(mod.mentions_score("sin score acá"))


class TestEvaluateEntry(unittest.TestCase):
    """evaluate_videolog_entry — los 4 sub-checks (a)-(d)."""

    def test_FIXTURE_A_no_entry_FALLA(self):
        r = mod.evaluate_videolog_entry("", "lago-helado", entry_found=False)
        self.assertFalse(r["overall_pass"])
        by = {c["check"]: c["status"] for c in r["checks"]}
        self.assertEqual(by["a_entry_exists"], "fail")

    def test_FIXTURE_B_sin_bullets_FALLA(self):
        text = "### #2 — lago-helado (P9)\nEl video salió bien pero sin bullets."
        r = mod.evaluate_videolog_entry(text, "lago-helado", entry_found=True)
        self.assertFalse(r["overall_pass"])
        by = {c["check"]: c["status"] for c in r["checks"]}
        self.assertEqual(by["a_entry_exists"], "pass")
        self.assertEqual(by["b_mentions_pattern"], "pass")     # menciona P9
        self.assertEqual(by["c_min_bullets"], "fail")          # 0 bullets

    def test_un_solo_bullet_FALLA(self):
        text = "### lago-helado P9\n- único bullet"
        r = mod.evaluate_videolog_entry(text, "lago-helado", entry_found=True)
        self.assertFalse(r["overall_pass"])
        self.assertEqual(r["bullet_count"], 1)

    def test_FIXTURE_C_completa_PASA(self):
        text = "### #2 — lago-helado (P9)\n- bullet uno\n- bullet dos\nscore 9.9/10"
        r = mod.evaluate_videolog_entry(text, "lago-helado", entry_found=True)
        self.assertTrue(r["overall_pass"], [(c["check"], c["status"]) for c in r["checks"]])

    def test_sin_pattern_FALLA(self):
        text = "### lago-helado\n- bullet uno\n- bullet dos"
        r = mod.evaluate_videolog_entry(text, "lago-helado", entry_found=True)
        self.assertFalse(r["overall_pass"])
        by = {c["check"]: c["status"] for c in r["checks"]}
        self.assertEqual(by["b_mentions_pattern"], "fail")

    def test_require_scores_sin_score_FALLA(self):
        text = "### lago-helado P9\n- bullet uno\n- bullet dos"
        r = mod.evaluate_videolog_entry(text, "lago-helado", require_scores=True, entry_found=True)
        self.assertFalse(r["overall_pass"])
        by = {c["check"]: c["status"] for c in r["checks"]}
        self.assertEqual(by["d_mentions_score"], "fail")

    def test_min_bullets_override(self):
        text = "### lago-helado P9\n- uno\n- dos"
        self.assertTrue(mod.evaluate_videolog_entry(text, "lago-helado", min_bullets=2,
                                                    entry_found=True)["overall_pass"])
        self.assertFalse(mod.evaluate_videolog_entry(text, "lago-helado", min_bullets=3,
                                                     entry_found=True)["overall_pass"])


class TestRotation(unittest.TestCase):
    """evaluate_rotation — HR#14 (entry más reciente ≠ anterior)."""

    def test_FIXTURE_D_mismo_pattern_FALLA(self):
        r = mod.evaluate_rotation(["P1", "P6", "P6"])   # últimas dos = P6
        self.assertFalse(r["overall_pass"])
        self.assertEqual(r["status"], "fail")
        self.assertEqual((r["prev"], r["last"]), ("P6", "P6"))

    def test_distinto_pattern_PASA(self):
        r = mod.evaluate_rotation(["P6", "P3", "P9"])
        self.assertTrue(r["overall_pass"])
        self.assertEqual(r["status"], "pass")

    def test_una_sola_entry_NOT_APPLICABLE(self):
        r = mod.evaluate_rotation(["P9"])
        self.assertEqual(r["status"], "not_applicable")
        self.assertTrue(r["overall_pass"])

    def test_filtra_none(self):
        # filas sin pattern (None) se ignoran; quedan las dos P6 consecutivas reales.
        r = mod.evaluate_rotation(["P1", None, "P6", "P6"])
        self.assertEqual(r["status"], "fail")


class TestMarkdownParsing(unittest.TestCase):
    """split_log_entries + gather_project_text + parse_master_table_patterns."""

    def test_gather_project_text_agrega_fila_y_seccion(self):
        md = _log_entry_complete(project="lago-helado", pattern="P9", prev_pattern="P1")
        found, text = mod.gather_project_text(md, "lago-helado")
        self.assertTrue(found)
        self.assertIn("P9", text)               # de la fila de tabla
        self.assertGreaterEqual(mod.count_bullets(text), 2)  # de la sección ###

    def test_gather_no_match(self):
        found, text = mod.gather_project_text(_log_no_entry(), "lago-helado")
        self.assertFalse(found)
        self.assertEqual(text, "")

    def test_parse_master_table_orden_cronologico(self):
        md = _log_two_consecutive_same_pattern()
        rows = mod.parse_master_table_patterns(md)
        self.assertEqual([n for n, _ in rows], [1, 2])       # ordenado por #
        self.assertEqual([p for _, p in rows], ["P6", "P6"])


class TestEndToEndExitCodes(unittest.TestCase):
    """main() via subprocess — SPEC + video-log en tempfiles → exit codes correctos."""

    def _spec(self, body):
        fd, path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        Path(path).write_text(textwrap.dedent(body))
        return path

    def _run(self, *args):
        return subprocess.run([sys.executable, str(_SCRIPT), *args],
                              capture_output=True, text=True)

    SPEC_OK = "project:\n  format: horror-choice\nvideo_capabilities:\n  has_ai_generated_clips: true\n"
    SPEC_NO_CAPS = "project:\n  format: horror-choice\n"

    def test_FIXTURE_C_completa_exit_0(self):
        spec = self._spec(self.SPEC_OK)
        log = _write(_log_entry_complete(project="lago-helado"))
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log)
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_FIXTURE_A_no_entry_exit_1(self):
        spec = self._spec(self.SPEC_OK)
        log = _write(_log_no_entry())
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log)
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_FIXTURE_B_sin_bullets_exit_1(self):
        spec = self._spec(self.SPEC_OK)
        log = _write(_log_entry_no_bullets(project="lago-helado"))
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log)
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_FIXTURE_D_rotacion_repetida_exit_1(self):
        spec = self._spec(self.SPEC_OK)
        log = _write(_log_two_consecutive_same_pattern(project="lago-helado"))
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log, "--check-rotation")
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)

    def test_spec_sin_video_capabilities_exit_2(self):
        spec = self._spec(self.SPEC_NO_CAPS)
        log = _write(_log_entry_complete(project="lago-helado"))
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log)
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_fuera_familia_sin_capability_not_applicable_exit_0(self):
        spec = self._spec(self.SPEC_OK)
        log = _write(_log_no_entry())   # ni existe la entry, pero no aplica → exit 0
        r = self._run("--format", "editorial", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", log)
        os.unlink(spec); os.unlink(log)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("not_applicable", r.stdout)

    def test_log_inexistente_exit_2(self):
        spec = self._spec(self.SPEC_OK)
        r = self._run("--format", "horror-choice", "--spec", spec,
                      "--project-id", "lago-helado", "--video-log", "/nope/missing-log.md")
        os.unlink(spec)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
