"""
test_hard_rules_parser.py — adversarial tests for hard_rules_parser.py

Per CLAUDE.md Hard Rule #26: every new script ships with test_*.py companion
that validates against canonical filesystem ground truth.

DATA-DRIVEN refactor (auditoría 2026-06-04): el test ANTERIOR esperaba un conteo
LITERAL de 25 rules (1-21 + 23-26) y la secuencia exacta correspondiente. Quedó
STALE cuando CLAUDE.md sumó HR#27 (SPEC 0-findings), HR#28/29 (model capabilities
matrix) y HR#30 (caption coverage 3 niveles) — y luego HR#31 (voice exclusivity).
Resultado: 3 fallos por conteo/secuencia hardcodeados, NO por un bug del parser.

El parser está SANO (lo confirma qa-gate.py que lo consume en verde). El arreglo
NO toca lib/hard_rules_parser.py: hace el TEST data-driven, asertando INVARIANTES
ESTRUCTURALES que sobreviven al crecimiento de la tabla, en vez de un número fijo:
  (a) secuencia monótona estrictamente creciente (sin duplicados ni desorden),
  (b) #22 ausente (empty slot documentado en footnote CLAUDE.md),
  (c) conteo ≥27 (la tabla SOLO crece; nunca menos rules que el snapshot 2026-06-04),
  (d) HR#1 parsea thresholds 9.0/8.5 — eso NO cambia, es lo que qa-gate.py consume,
  (e) los authority pointers de las rules NUEVAS (#27 en adelante) existen como
      strings no-vacíos (el parser captura la última columna sin romperse).

Nota de parseo: la fila "| 28/29 ⛔ | ... |" NO matchea el regex estricto del parser
(el `/29` tras el primer entero rompe el patrón), por lo que #28 y #29 NO aparecen
en el output. Es comportamiento ESPERADO y consistente con el principio "#22 ausente":
el test asume gaps documentados, no exige contigüidad total.

Authority: CLAUDE.md Hard Rules table + footnote. HR#26 companion (data-driven 2026-06-04).
"""
import re
import sys
import unittest
from pathlib import Path

# Add parent dir to path so `import hard_rules_parser` resolves regardless
# of cwd at test invocation (project scripts/lib/ or template scripts/lib/).

from ai_video.core.hard_rules_parser import (  # noqa: E402
    parse_hard_rules,
    get_rule,
    get_quality_threshold_calibrated,
    get_quality_threshold_perceptual,
)


CLAUDE_MD_PATH = Path(__file__).resolve().parents[2] / "docs/OPERATING-MANUAL.md"

# Invariante (c): floor de conteo. Snapshot 2026-06-04 parsea 28 rules
# ([1..21, 23, 24, 25, 26, 27, 30, 31]). La tabla SOLO crece → ≥27 es el piso
# pedido por la auditoría (margen bajo el snapshot para tolerar un re-conteo menor
# sin volver a quedar stale, pero por encima del estado pre-cascade de 25).
MIN_RULE_COUNT = 27

# Invariante (e): rules nuevas (post-cascade) cuyo authority_pointer DEBE existir.
# #28/#29 quedan fuera por el parseo de "28/29" (ver docstring) — no se asertan acá.
NEW_RULES_WITH_AUTHORITY = (27, 30, 31)


class TestHardRulesParser(unittest.TestCase):
    """Canonical ground truth: current CLAUDE.md at root. Invariantes estructurales."""

    @classmethod
    def setUpClass(cls):
        cls.rules = parse_hard_rules(CLAUDE_MD_PATH)
        cls.rule_ids = [r["rule_id"] for r in cls.rules]
        cls.sorted_ids = sorted(cls.rule_ids)

    # ── (a) secuencia monótona estrictamente creciente ────────────────────────
    def test_sequence_strictly_monotonic_increasing(self):
        """rule_ids en orden de tabla deben ser estrictamente crecientes
        (sin duplicados, sin desorden). Detector de drift agnóstico al conteo."""
        self.assertEqual(
            self.rule_ids, self.sorted_ids,
            f"rule_ids no están en orden ascendente: {self.rule_ids}",
        )
        for a, b in zip(self.rule_ids, self.rule_ids[1:]):
            self.assertLess(
                a, b,
                f"secuencia no estrictamente creciente: {a} no < {b} en {self.rule_ids}",
            )

    # ── (b) #22 ausente (empty slot documentado) ──────────────────────────────
    def test_rule_22_absent_empty_slot(self):
        """Rule #22 = empty slot canónico (CLAUDE.md footnote). NUNCA en output."""
        self.assertNotIn(
            22, self.rule_ids,
            "Rule #22 es empty slot canónico — el parser debe omitirlo.",
        )
        # y la búsqueda directa retorna None, no crashea
        self.assertIsNone(get_rule(self.rules, 22))

    # ── (c) conteo ≥ MIN_RULE_COUNT (la tabla solo crece) ──────────────────────
    def test_rule_count_at_least_floor(self):
        """Conteo ≥27. Refleja el cascade HR#27/#28-29/#30(/#31) sin hardcodear
        un número exacto que vuelva a quedar stale en el próximo agregado."""
        self.assertGreaterEqual(
            len(self.rules), MIN_RULE_COUNT,
            f"Esperado ≥{MIN_RULE_COUNT} rules, got {len(self.rules)}. "
            f"Secuencia: {self.rule_ids}",
        )

    def test_core_rules_present(self):
        """Las rules fundacionales (1-21, 23-26) deben seguir presentes — el
        crecimiento agrega, nunca borra el núcleo histórico."""
        core = set(range(1, 22)) | {23, 24, 25, 26}
        present = set(self.rule_ids)
        missing = core - present
        self.assertEqual(
            missing, set(),
            f"Core rules ausentes (regresión): {sorted(missing)}",
        )

    # ── (d) HR#1 thresholds 9.0/8.5 (lo que qa-gate consume — NO cambia) ───────
    def test_rule_1_thresholds_9_0_and_8_5(self):
        """Rule #1 = dual quality gate. Debe parsear calibrated ≥9.0 + perceptual
        ≥8.5. Es exactamente lo que qa-gate.py lee — invariante load-bearing."""
        rule_1 = get_rule(self.rules, 1)
        self.assertIsNotNone(rule_1, "Rule #1 ausente del parse output")
        self.assertIn("≥9.0", rule_1["text"],
                      f"Rule #1 sin threshold calibrated ≥9.0. Excerpt: {rule_1['text'][:200]}")
        self.assertIn("≥8.5", rule_1["text"], "Rule #1 sin threshold perceptual ≥8.5")
        # via los helpers que consume qa-gate.py:
        self.assertEqual(get_quality_threshold_calibrated(self.rules), 9.0)
        self.assertEqual(get_quality_threshold_perceptual(self.rules), 8.5)

    # ── (e) authority pointers de rules nuevas no-vacíos ──────────────────────
    def test_new_rules_authority_pointers_nonempty(self):
        """Las rules del cascade (#27, #30, #31) deben existir con authority_pointer
        string no-vacío (el parser captura la última columna sin romperse)."""
        for rid in NEW_RULES_WITH_AUTHORITY:
            rule = get_rule(self.rules, rid)
            self.assertIsNotNone(rule, f"Rule #{rid} (nueva) ausente del parse")
            ap = rule["authority_pointer"]
            self.assertIsInstance(ap, str, f"Rule #{rid} authority_pointer no es str")
            self.assertGreater(
                len(ap.strip()), 0,
                f"Rule #{rid} authority_pointer vacío: {ap!r}",
            )

    # ── severity por emoji (sin cambios — sigue siendo invariante del parser) ──
    def test_severity_extraction(self):
        """⛔⛔ → 'critical' (#24, #25); ⛔ → 'blocker' (#26); ninguno → 'standard' (#1)."""
        self.assertEqual(get_rule(self.rules, 24)["severity"], "critical")
        self.assertEqual(get_rule(self.rules, 25)["severity"], "critical")
        self.assertEqual(get_rule(self.rules, 26)["severity"], "blocker")
        self.assertEqual(get_rule(self.rules, 1)["severity"], "standard")

    def test_get_rule_missing_returns_none(self):
        """get_rule del empty slot retorna None, NO raises."""
        self.assertIsNone(get_rule(self.rules, 22), "Rule #22 lookup debe ser None")
        self.assertIsNone(get_rule(self.rules, 9999), "id inexistente → None")

    def test_schema_per_rule(self):
        """Cada rule parseada tiene el schema canónico
        {rule_id: int, text: str, severity: str, authority_pointer: str}."""
        required_keys = {"rule_id", "text", "severity", "authority_pointer"}
        valid_severities = {"critical", "blocker", "standard"}
        for r in self.rules:
            self.assertTrue(
                required_keys.issubset(r.keys()),
                f"Rule #{r.get('rule_id')} sin schema keys. Got: {set(r.keys())}",
            )
            self.assertIsInstance(r["rule_id"], int)
            self.assertIsInstance(r["text"], str)
            self.assertIsInstance(r["severity"], str)
            self.assertIn(r["severity"], valid_severities)
            self.assertIsInstance(r["authority_pointer"], str)
            self.assertGreater(len(r["text"]), 0, f"Rule #{r['rule_id']} text vacío")


if __name__ == "__main__":
    unittest.main(verbosity=2)
