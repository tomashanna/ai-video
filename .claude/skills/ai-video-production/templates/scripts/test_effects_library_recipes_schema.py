"""Schema tests for global transitions/ recipes (PRE-4.J Option D + global root 2026-06-05).

Per Hard Rule #26: refactor (root transitions/ migration + catalog.json index) ships tests.
Validates the ACTUAL global library (universal + per-format layers):
1. Every recipe in every layer parses as JSON + has xfade_transition / xfade_fidelity /
   native_mechanism_note fields.
2. xfade_transition values are in the legal ffmpeg xfade set ∪ {hardcut}; xfade_fidelity in
   {literal, approximate}.
3. catalog.json ↔ disk sync: every recipe on disk has a catalog entry and vice versa
   (no orphans in either direction); catalog `recipe` paths resolve; `formats` non-empty.

Read-only against real recipe files (validates the library, not synthetic fixtures).
"""
import json
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent


def _transitions_root():
    """Walk up to repo-root global transitions/ (marker: catalog.json) — same logic as build-video-hybrid."""
    for base in [SCRIPTS_DIR] + list(SCRIPTS_DIR.parents):
        cand = base / "transitions" / "catalog.json"
        if cand.exists():
            return cand.parent
    return None


ROOT = _transitions_root()

LEGAL_XFADE = {"fade", "fadeblack", "fadewhite", "dissolve", "hlslice", "slideleft", "zoomin", "hardcut"}
LEGAL_FIDELITY = {"literal", "approximate"}


def _layer_dirs():
    if ROOT is None:
        return []
    return sorted(p / "transitions" for p in ROOT.iterdir()
                  if p.is_dir() and (p / "transitions").is_dir())


def _all_recipes():
    files = []
    for d in _layer_dirs():
        files.extend(sorted(d.glob("*.json")))
    return files


class TestRecipesSchema(unittest.TestCase):

    def test_transitions_root_found(self):
        self.assertIsNotNone(ROOT, "global transitions/catalog.json not found walking up from scripts dir")

    def test_all_recipes_parse_and_have_option_d_fields(self):
        files = _all_recipes()
        self.assertGreaterEqual(len(files), 14, f"Expected ≥14 recipes across layers, got {len(files)}")
        for f in files:
            with self.subTest(recipe=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))  # raises if invalid JSON
                for field in ("xfade_transition", "xfade_fidelity", "native_mechanism_note"):
                    self.assertIn(field, data, f"{f.name} missing Option D field '{field}'")
                self.assertTrue(str(data["native_mechanism_note"]).strip(),
                                f"{f.name} native_mechanism_note must be non-empty")

    def test_xfade_values_legal(self):
        for f in _all_recipes():
            with self.subTest(recipe=f.name):
                data = json.loads(f.read_text(encoding="utf-8"))
                self.assertIn(data["xfade_transition"], LEGAL_XFADE,
                              f"{f.name} xfade_transition '{data['xfade_transition']}' not legal")
                self.assertIn(data["xfade_fidelity"], LEGAL_FIDELITY,
                              f"{f.name} xfade_fidelity '{data['xfade_fidelity']}' not in {LEGAL_FIDELITY}")


class TestCatalogSync(unittest.TestCase):
    """catalog.json is the system's index (transición → formato) — must mirror disk 1:1."""

    @classmethod
    def setUpClass(cls):
        if ROOT is None:
            raise unittest.SkipTest("transitions root not found")
        cls.catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
        cls.entries = {e["id"]: e for e in cls.catalog["transitions"]}
        cls.disk_ids = {f.stem: f for f in _all_recipes()}

    def test_every_disk_recipe_has_catalog_entry(self):
        missing = sorted(set(self.disk_ids) - set(self.entries))
        self.assertEqual(missing, [], f"Recipes on disk missing from catalog.json: {missing}")

    def test_every_catalog_entry_resolves_on_disk(self):
        for tid, entry in self.entries.items():
            with self.subTest(transition=tid):
                path = ROOT / entry["recipe"]
                self.assertTrue(path.is_file(), f"catalog entry '{tid}' recipe path missing: {entry['recipe']}")
                self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["id"], tid,
                                 f"catalog id '{tid}' != recipe JSON id")

    def test_entries_declare_formats_and_layer(self):
        for tid, entry in self.entries.items():
            with self.subTest(transition=tid):
                self.assertTrue(entry.get("formats"), f"'{tid}' has empty formats")
                self.assertTrue(entry.get("layer"), f"'{tid}' has empty layer")
                if entry["layer"] != "universal":
                    self.assertNotIn("*", entry["formats"],
                                     f"'{tid}' is per-format ({entry['layer']}) but declares formats ['*']")

    def test_format_resolution_layers_exist(self):
        for fmt, layers in self.catalog["format_resolution"].items():
            if fmt.startswith("_"):
                continue
            for layer in layers:
                with self.subTest(format=fmt, layer=layer):
                    self.assertTrue((ROOT / layer / "transitions").is_dir(),
                                    f"format_resolution['{fmt}'] references missing layer dir '{layer}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
