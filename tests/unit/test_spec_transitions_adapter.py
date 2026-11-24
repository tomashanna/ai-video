"""Adversarial tests for spec_transitions_adapter.normalize_transitions (PRE-4.J Decision 3).

Per Hard Rule #26: companion test sidecar. 3 tests:
1. canonical per-shot passthrough (no conversion)
2. legacy top-level transitions[] array converted correctly + non-destructive
3. no transitions declared → spec unchanged
"""

import unittest

from ai_video.core.spec_transitions_adapter import normalize_transitions


class TestSpecTransitionsAdapter(unittest.TestCase):
    def test_canonical_per_shot_passthrough(self):
        spec = {
            "shot_list": [
                {"shot_id": "shot_01", "transition_out": "cross-fade-0.5s"},
                {"shot_id": "shot_02"},
            ]
        }
        out = normalize_transitions(spec)
        self.assertIs(out, spec, "Canonical spec must be returned as-is (no copy)")
        self.assertEqual(out["shot_list"][0]["transition_out"], "cross-fade-0.5s")

    def test_legacy_top_level_array_converted_correctly(self):
        spec = {
            "shot_list": [
                {"shot_id": "shot_01"},
                {"shot_id": "shot_02"},
                {"shot_id": "shot_03"},
            ],
            "transitions": [
                {"from_shot_id": "shot_01", "to_shot_id": "shot_02", "transition_type": "hard_cut"},
                {"from_shot_id": "shot_02", "to_shot_id": "shot_03", "transition_type": "white_flash"},
                {
                    "from_shot_id": "shot_03",
                    "to_shot_id": "shot_04",
                    "transition_type": "hard_cut_with_whoosh",
                },
            ],
            "shot_list_extra": None,
        }
        # extend shot_list to cover the third transition target
        spec["shot_list"].append({"shot_id": "shot_04"})
        out = normalize_transitions(spec)
        by = {s["shot_id"]: s for s in out["shot_list"]}
        self.assertEqual(
            by["shot_01"]["transition_out"],
            "hard-cut-with-whoosh",
            "hard_cut must map to canonical recipe id",
        )
        self.assertEqual(
            by["shot_02"]["transition_out"],
            "light-flash-impact",
            "white_flash must map to canonical recipe id",
        )
        self.assertEqual(
            by["shot_03"]["transition_out"],
            "hard-cut-with-whoosh",
            "hard_cut_with_whoosh (BUILD 1 fix) must map to canonical recipe id",
        )
        self.assertNotIn("transition_out", by["shot_04"], "Last shot has no outgoing transition")
        # Non-destructive: original spec untouched
        self.assertNotIn(
            "transition_out",
            spec["shot_list"][0],
            "Original spec must NOT be mutated (deep-copy on conversion)",
        )

    def test_no_transitions_returns_spec_unchanged(self):
        spec = {"shot_list": [{"shot_id": "shot_01"}, {"shot_id": "shot_02"}]}
        out = normalize_transitions(spec)
        self.assertIs(out, spec, "Spec without transitions must be returned as-is")
        self.assertNotIn("transition_out", out["shot_list"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
