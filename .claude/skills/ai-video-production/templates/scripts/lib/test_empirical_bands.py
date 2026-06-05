#!/usr/bin/env python3
"""test_empirical_bands.py — HR#26 companion de lib/empirical_bands.py.

Cubre: banda pura (p25-p75 / p5-p95 / n<4), routing per-formato sin fallback
silencioso (sport pre-empírico → None), fallback EXPLÍCITO, lectura real de los
F1 JSON del repo (smoke contra horror-choice), y el caso disparador Y52:
la banda de captions_narration.y_pct medida debe contener ~62-64, NO 48.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import empirical_bands as eb  # noqa: E402


def _mk_fixture_tree(tmp: Path, fmt: str = "horror-choice"):
    """Arma un referent-analysis/<fmt>/ sintético con 5 referentes."""
    d = tmp / "referent-analysis" / fmt
    d.mkdir(parents=True)
    per_ref = {}
    # valores conocidos: cuts 2,3,4,5,6 → p25/p75 computables; lufs constantes
    for i, cuts in enumerate([2, 3, 4, 5, 6]):
        per_ref[f"ref-{i:02d}"] = {
            "pace": {"wpm_total": 160 + i},
            "audio": {"lufs_integrated": -14.0},
            "pacing": {"cuts_per_min": cuts, "cuts_per_min_raw": cuts * 2},
        }
    (d / "F1-INGENIERO-MEASUREMENTS.json").write_text(
        json.dumps({"metadata": {}, "per_referent": per_ref}))
    ui = {}
    for i, y in enumerate([62.0, 63.0, 64.0, 62.5, 63.5]):
        ui[f"ref-{i:02d}"] = {
            "captions_narration": {"x_pct": 50.0, "y_pct": y},
            "character_name_labels": {"y_pct_avg": 20.0 + i},
        }
    (d / "F1-UI-SAFE-ZONES.json").write_text(
        json.dumps({"metadata": {}, "per_referent": ui}))
    return tmp / "referent-analysis"


class TestComputeBand(unittest.TestCase):
    def test_p25_p75(self):
        lo, hi, n = eb.compute_band([2, 3, 4, 5, 6])
        self.assertEqual(n, 5)
        self.assertLess(lo, hi)
        self.assertGreaterEqual(lo, 2)
        self.assertLessEqual(hi, 6)

    def test_too_few_values_returns_none(self):
        lo, hi, n = eb.compute_band([1, 2, 3])
        self.assertIsNone(lo)
        self.assertIsNone(hi)
        self.assertEqual(n, 3)

    def test_p5_p95_wider_than_p25_p75(self):
        vals = list(range(1, 21))
        lo_iq, hi_iq, _ = eb.compute_band(vals, "p25-p75")
        lo_w, hi_w, _ = eb.compute_band(vals, "p5-p95")
        self.assertLess(lo_w, lo_iq)
        self.assertGreater(hi_w, hi_iq)

    def test_ignores_none_values(self):
        lo, hi, n = eb.compute_band([2, None, 3, 4, None, 5, 6])
        self.assertEqual(n, 5)


class TestPerFormatRouting(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = _mk_fixture_tree(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_band_from_fixture(self):
        lo, hi, n = eb.band("horror-choice", "pacing", "cuts_per_min", base=self.base)
        self.assertEqual(n, 5)
        self.assertIsNotNone(lo)

    def test_raw_vs_curated_are_distinct_keys(self):
        lo_c, hi_c, _ = eb.band("horror-choice", "pacing", "cuts_per_min", base=self.base)
        lo_r, hi_r, _ = eb.band("horror-choice", "pacing", "cuts_per_min_raw", base=self.base)
        self.assertGreater(lo_r, lo_c)  # raw ~2x curated en el fixture
        self.assertGreater(hi_r, hi_c)

    def test_unknown_format_no_silent_fallback(self):
        """sport pre-empírico: sin F1 propio → (None, None, 0), JAMÁS hereda solo."""
        lo, hi, n = eb.band("sport-choice", "pacing", "cuts_per_min", base=self.base)
        self.assertIsNone(lo)
        self.assertEqual(n, 0)

    def test_explicit_fallback_inherits(self):
        lo, hi, n = eb.band("sport-choice", "pacing", "cuts_per_min",
                            base=self.base, fallback_format="horror-choice")
        self.assertEqual(n, 5)

    def test_ui_band_handles_avg_variant(self):
        lo, hi, n = eb.ui_band("horror-choice", "character_name_labels", "y_pct",
                               base=self.base)
        self.assertEqual(n, 5)  # lee y_pct_avg cuando y_pct no existe


class TestAgainstRealRepoData(unittest.TestCase):
    """Smoke contra los F1 reales del repo (skip si no se encuentran — proyecto copiado)."""

    def setUp(self):
        self.root = eb.find_referent_analysis_root()
        if self.root is None or not (self.root / "horror-choice").is_dir():
            self.skipTest("referent-analysis/horror-choice no encontrado")

    def test_caso_disparador_y52_loading_drift(self):
        """La banda MEDIDA de captions y_pct contiene ~62-64 — el hardcode Y48
        de CLAUDE.md HR#4 para loading vs Y52 del CORE es exactamente el drift
        que este lib elimina: el gate lee la banda, no la prosa."""
        lo, hi, n = eb.ui_band("horror-choice", "captions_narration", "y_pct")
        self.assertGreaterEqual(n, 4)
        self.assertGreater(hi, 55.0)  # las captions canónicas viven ~60s, no ~48
        self.assertLess(lo, 70.0)

    def test_cuts_per_min_bands_exist_and_methods_differ(self):
        lo_c, hi_c, n_c = eb.band("horror-choice", "pacing", "cuts_per_min")
        lo_r, hi_r, n_r = eb.band("horror-choice", "pacing", "cuts_per_min_raw")
        self.assertGreaterEqual(n_c, 4)
        self.assertGreaterEqual(n_r, 4)
        # documenta la discrepancia 2-7 vs 14-22: son counting methods distintos
        self.assertNotEqual((lo_c, hi_c), (lo_r, hi_r))

    def test_lufs_band_near_minus_14(self):
        lo, hi, n = eb.band("horror-choice", "audio", "lufs_integrated")
        self.assertGreaterEqual(n, 4)
        self.assertLess(lo, -10.0)
        self.assertGreater(hi, -20.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
