"""Pure output checks used by the eval harness, plus a smoke run of the offline suites."""

from __future__ import annotations

from pathlib import Path

import pytest
from evals import checks
from evals import run as R


def test_av_checks_boundaries():
    assert checks.check_duration(30.2, 30.0, tol_s=0.25).passed
    assert not checks.check_duration(30.3, 30.0, tol_s=0.25).passed
    assert checks.check_resolution(1080, 1920).passed and not checks.check_resolution(1920, 1080).passed
    assert checks.check_fps(29.97, 30.0, tol=0.05).passed and not checks.check_fps(24, 30).passed
    assert checks.check_loudness(-14.9).passed and not checks.check_loudness(-15.2).passed
    assert checks.check_true_peak(-1.0).passed and not checks.check_true_peak(-0.2).passed


def test_in_band_and_unavailable_band():
    assert checks.check_in_band("x", 5, (4, 6, 10)).passed
    assert not checks.check_in_band("x", 7, (4, 6, 10)).passed
    assert checks.check_in_band("x", 7, (4, 6, 10), slack=1).passed
    skipped = checks.check_in_band("x", 7, (None, None, 2))
    assert skipped.passed and skipped.meta["skipped"]


def test_caption_y_pct():
    assert checks.caption_y_pct(0, 0, 1000) == 100.0
    assert checks.caption_y_pct(700, 64, 1920) == pytest.approx(61.88, abs=0.01)


def _cue(text, s, e):
    return {"text": text, "start": s, "end": e}


def test_caption_timing_detects_each_defect():
    speech = [(0.0, 1.0), (1.2, 2.0)]
    good = [_cue("HOLA", 0.0, 1.0), _cue("MUNDO", 1.2, 2.0)]
    assert all(r.passed for r in checks.check_caption_timing(good, speech, video_duration_s=2.0))

    def failed(cues, **kw):
        return {
            r.name
            for r in checks.check_caption_timing(cues, speech, video_duration_s=2.0, **kw)
            if not r.passed
        }

    assert "captions_no_overlap" in failed([_cue("A", 0, 1.5), _cue("B", 1.0, 2.0)])
    assert "captions_monotonic" in failed([_cue("B", 1.2, 2.0), _cue("A", 0.0, 1.0)])
    assert "captions_min_duration" in failed([_cue("A", 0, 0.1), _cue("B", 1.2, 2.0)])
    assert "captions_readability" in failed([_cue("X" * 50, 0, 1.0), _cue("B", 1.2, 2.0)])
    assert "captions_within_video" in failed([_cue("A", 0, 1.0), _cue("B", 1.2, 2.5)])
    assert "captions_temporal_coverage" in failed([_cue("HOLA", 0.0, 1.0)])  # HR#30-C: 2nd phrase uncaptioned


def test_patch_helpers():
    spec = {"a": {"b": [1, {"c": 2}]}, "lst": []}
    out = R.apply_patch(spec, {"set": {"a.b.1.c": 3}, "append": {"lst": "x"}})
    assert out["a"]["b"][1]["c"] == 3 and out["lst"] == ["x"]
    assert spec["a"]["b"][1]["c"] == 2  # original untouched
    assert R.summarize_output(
        'noise {"overall_status": "fail", "checks": {"voseo": {"status": "fail"}}}'
    ) == ("status=fail failing=['voseo']")


@pytest.mark.parametrize("suite", ["captions", "safe_zone", "rubric"])
def test_offline_suites_match_expectations(suite: str, tmp_path: Path):
    results = R.SUITES[suite](tmp_path)
    assert results and all(r.ok for r in results), [r for r in results if not r.ok]
