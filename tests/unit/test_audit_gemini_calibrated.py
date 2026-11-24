"""Calibrated v4 rubric parsing/scoring (regression: weighted score was never computed)."""

from __future__ import annotations

import pytest

from ai_video.audits import audit_gemini_calibrated as A

LABELS = [
    "EXECUTION CONTINUITY",
    "INMERSIÓN POV",
    "SOUND DEPTH",
    "ATMOSPHERE",
    "CHARACTER SIGNATURE",
    "STORY LOGIC",
    "EDITING MODULATION",
    "HOOK RETENTION",
    "CAPTIONS",
    "NARRATIVE COMPREHENSION",
]


def _response(scores: list[float], extra: str = "") -> str:
    lines = [
        f"{i}. {label} (weight x): {s}" for i, (label, s) in enumerate(zip(LABELS, scores, strict=True), 1)
    ]
    return "\n".join(lines) + "\nWEIGHTED SCORE: 9.9\nCONFIDENCE: High\nVERDICT: PUBLISH\n" + extra


def test_weights_sum_to_one_and_match_patterns():
    assert sum(A.WEIGHTS.values()) == pytest.approx(1.0)
    assert [n for n, _ in A.DIM_PATTERNS] == list(A.WEIGHTS)


def test_parse_complete_v4_response_computes_weighted_score():
    scores = [8.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0]
    parsed = A.parse_response(_response(scores))
    assert parsed["dimensions_complete"] is True
    assert parsed["weighted_score_computed"] == pytest.approx(9.0 - 0.30)  # only execution is 1 pt lower
    assert parsed["weighted_score_reported"] == 9.9  # Gemini's own arithmetic is kept only for cross-check
    assert parsed["confidence"] == "high" and parsed["verdict"] == "PUBLISH"


def test_parse_incomplete_response_does_not_score():
    parsed = A.parse_response("1. EXECUTION CONTINUITY: 9\n3. SOUND DEPTH: 8")
    assert parsed["dimensions_complete"] is False and parsed["weighted_score_computed"] is None


def test_weighted_score_validates_input():
    with pytest.raises(ValueError, match="missing"):
        A.weighted_score({"captions": 9})
    with pytest.raises(ValueError, match="outside"):
        A.weighted_score({k: 11 for k in A.WEIGHTS})
    assert A.weighted_score({k: 10 for k in A.WEIGHTS}) == pytest.approx(10.0)
