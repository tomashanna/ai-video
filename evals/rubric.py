"""Rubric-based scoring hook for subjective quality.

The production judge is Gemini with the calibrated v4 prompt
(``ai_video.audits.audit_gemini_calibrated``). Evals must stay offline and deterministic,
so a :class:`Judge` is any callable that maps a render to per-dimension scores. Offline we
use :class:`FixtureJudge` (recorded scores); plug :class:`GeminiJudge` in locally to score
real renders with the same aggregation and the same thresholds as ``qa-gate`` (HR#1).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from ai_video.audits.audit_gemini_calibrated import WEIGHTS, weighted_score
from ai_video.core.hard_rules_parser import (
    get_quality_threshold_calibrated,
    get_quality_threshold_perceptual,
    parse_hard_rules,
)
from ai_video.paths import hard_rules_doc


class Judge(Protocol):
    def __call__(self, render_id: str) -> dict[str, float]: ...


@dataclass(frozen=True)
class Thresholds:
    calibrated: float
    perceptual: float

    @classmethod
    def from_hard_rules(cls) -> Thresholds:
        rules = parse_hard_rules(hard_rules_doc())
        cal, perc = get_quality_threshold_calibrated(rules), get_quality_threshold_perceptual(rules)
        if cal is None or perc is None:
            raise ValueError("Hard Rule #1 thresholds not found")
        return cls(cal, perc)


@dataclass(frozen=True)
class Verdict:
    render_id: str
    score: float
    status: str  # PASS | AWAITING_PERCEPTUAL | FAIL
    weakest: str


def verdict(
    render_id: str, dims: dict[str, float], th: Thresholds, perceptual: float | None = None
) -> Verdict:
    """Same OR-logic as qa-gate: calibrated ≥ threshold, or human perceptual ≥ threshold."""
    score = weighted_score(dims)
    weakest = min(WEIGHTS, key=lambda k: dims[k])
    if score >= th.calibrated:
        status = "PASS"
    elif perceptual is None:
        status = "AWAITING_PERCEPTUAL"
    else:
        status = "PASS" if perceptual >= th.perceptual else "FAIL"
    return Verdict(render_id, score, status, weakest)


class FixtureJudge:
    """Replays recorded judge outputs: ``{render_id: {"dims": {...}, "perceptual": x}}``."""

    def __init__(self, path: Path) -> None:
        self.data = json.loads(path.read_text(encoding="utf-8"))

    def __call__(self, render_id: str) -> dict[str, float]:
        return {k: float(v) for k, v in self.data[render_id]["dims"].items()}


class GeminiJudge:  # pragma: no cover - needs network + GEMINI_API_KEY
    """Live judge: uploads the render and parses the calibrated v4 response."""

    def __init__(self, renders_dir: Path) -> None:
        self.renders_dir = renders_dir

    def __call__(self, render_id: str) -> dict[str, float]:
        from ai_video.audits import audit_gemini_calibrated as A

        prompt = A.find_prompt_template().read_text(encoding="utf-8")
        parsed = A.parse_response(A.analyze(self.renders_dir / f"{render_id}.mp4", prompt))
        if not parsed["dimensions_complete"]:
            raise ValueError(f"judge response for {render_id} incomplete")
        return dict(parsed["dimensions"])
