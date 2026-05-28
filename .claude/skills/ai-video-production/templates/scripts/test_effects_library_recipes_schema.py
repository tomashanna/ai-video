"""Schema tests for effects-library recipes (PRE-4.J Option D + PRE-4.K tiered).

Per Hard Rule #26: refactor (Option D fields added to 10 recipes) ships tests.
Validates the ACTUAL tiered library (Capa A universal primitives + Capa B horror sub-genre):
1. Every recipe in both catalogs parses as JSON + has xfade_transition / xfade_fidelity /
   native_mechanism_note fields.
2. xfade_transition values are in the legal ffmpeg xfade set ∪ {hardcut}; xfade_fidelity in
   {literal, approximate}.

Read-only against real recipe files (validates the library, not synthetic fixtures).
"""
import json
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
CAPA_A = SCRIPTS_DIR.parent / "effects-library" / "transitions"               # templates/effects-library/transitions
CAPA_B = SCRIPTS_DIR.parents[2] / "horror-choice-format" / "effects-library" / "transitions"

LEGAL_XFADE = {"fade", "fadeblack", "fadewhite", "dissolve", "hlslice", "hardcut"}
LEGAL_FIDELITY = {"literal", "approximate"}


def _all_recipes():
    files = []
    for d in (CAPA_A, CAPA_B):
        if d.exists():
            files.extend(sorted(d.glob("*.json")))
    return files


class TestRecipesSchema(unittest.TestCase):

    def test_all_recipes_parse_and_have_option_d_fields(self):
        files = _all_recipes()
        self.assertGreaterEqual(len(files), 10, f"Expected ≥10 recipes across catalogs, got {len(files)}")
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
