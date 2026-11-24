"""Deterministic, reusable output checks for short vertical videos.

Every function is pure (data in, :class:`CheckResult` out) so the same checks can run on
synthetic fixtures in CI and on real renders locally. Thresholds default to the delivery
spec (9:16 reel, -14 LUFS) and the empirical referent bands in ``data/referent-analysis``.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from itertools import pairwise
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str
    value: Any = None
    meta: dict[str, Any] = field(default_factory=dict)


def check_duration(actual_s: float, expected_s: float, tol_s: float = 0.25) -> CheckResult:
    delta = actual_s - expected_s
    return CheckResult(
        "duration",
        abs(delta) <= tol_s,
        f"{actual_s:.2f}s vs expected {expected_s:.2f}s (±{tol_s}s, Δ{delta:+.2f})",
        actual_s,
    )


def check_resolution(width: int, height: int, expected: tuple[int, int] = (1080, 1920)) -> CheckResult:
    ok = (width, height) == expected
    return CheckResult("resolution", ok, f"{width}x{height} vs {expected[0]}x{expected[1]}", (width, height))


def check_fps(fps: float, expected: float = 30.0, tol: float = 0.01) -> CheckResult:
    return CheckResult("fps", abs(fps - expected) <= tol, f"{fps:.3f} fps vs {expected}", fps)


def check_loudness(integrated_lufs: float, target: float = -14.0, tol: float = 1.0) -> CheckResult:
    """Integrated loudness (EBU R128) within ``target ± tol`` LU."""
    ok = abs(integrated_lufs - target) <= tol
    return CheckResult("loudness", ok, f"{integrated_lufs:.1f} LUFS vs {target} ±{tol}", integrated_lufs)


def check_true_peak(true_peak_dbtp: float, ceiling: float = -1.0) -> CheckResult:
    return CheckResult(
        "true_peak",
        true_peak_dbtp <= ceiling,
        f"{true_peak_dbtp:.1f} dBTP vs ceiling {ceiling}",
        true_peak_dbtp,
    )


def check_in_band(
    name: str, value: float, band: tuple[float | None, float | None, int], *, slack: float = 0.0
) -> CheckResult:
    """Value inside an empirical ``(lo, hi, n)`` band (with optional absolute slack)."""
    lo, hi, n = band
    if lo is None or hi is None:
        return CheckResult(name, True, f"band unavailable (n={n}) — not evaluated", value, {"skipped": True})
    ok = (lo - slack) <= value <= (hi + slack)
    return CheckResult(name, ok, f"{value:.2f} vs band [{lo:.2f}, {hi:.2f}] (n={n}, slack {slack})", value)


def caption_y_pct(margin_v_px: int, font_size_px: int, height_px: int) -> float:
    """Vertical centre (% from top) of a bottom-anchored ASS caption line."""
    centre_from_bottom = margin_v_px + font_size_px / 2
    return round(100 * (1 - centre_from_bottom / height_px), 2)


def check_caption_timing(
    cues: Sequence[dict[str, Any]],
    speech: Sequence[tuple[float, float]],
    *,
    video_duration_s: float,
    min_cue_s: float = 0.3,
    max_cps: float = 20.0,
    min_coverage: float = 0.95,
) -> list[CheckResult]:
    """Caption cues vs spoken spans: ordering, overlap, readability and temporal coverage (HR#30-C)."""
    out: list[CheckResult] = []
    ordered = all(b["start"] >= a["start"] for a, b in pairwise(cues))
    out.append(
        CheckResult(
            "captions_monotonic", ordered, "cue starts are non-decreasing" if ordered else "out of order"
        )
    )
    overlaps = [i for i, (a, b) in enumerate(pairwise(cues)) if b["start"] < a["end"] - 1e-6]
    out.append(
        CheckResult(
            "captions_no_overlap",
            not overlaps,
            f"overlapping cue pairs at {overlaps}" if overlaps else "no overlapping cues",
        )
    )
    short = [c["text"] for c in cues if c["end"] - c["start"] < min_cue_s]
    out.append(
        CheckResult(
            "captions_min_duration",
            not short,
            f"cues shorter than {min_cue_s}s: {short}" if short else f"all cues ≥ {min_cue_s}s",
        )
    )
    fast = [c["text"] for c in cues if len(c["text"]) / max(c["end"] - c["start"], 1e-6) > max_cps]
    out.append(
        CheckResult(
            "captions_readability",
            not fast,
            f"cues above {max_cps} chars/s: {fast}" if fast else f"all cues ≤ {max_cps} chars/s",
        )
    )
    inside = all(0 <= c["start"] < c["end"] <= video_duration_s + 1e-6 for c in cues)
    out.append(
        CheckResult(
            "captions_within_video",
            inside,
            "all cues inside the video" if inside else "a cue starts/ends outside the video",
        )
    )
    spoken = sum(e - s for s, e in speech)
    covered = 0.0
    for s, e in speech:
        for c in cues:
            covered += max(0.0, min(e, c["end"]) - max(s, c["start"]))
    ratio = covered / spoken if spoken else 1.0
    out.append(
        CheckResult(
            "captions_temporal_coverage",
            ratio >= min_coverage,
            f"{ratio:.0%} of speech has a caption on screen (min {min_coverage:.0%})",
            ratio,
        )
    )
    return out
