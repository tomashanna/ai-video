#!/usr/bin/env python3
"""test_audit-render-audio-coverage.py — companion test (HR#26 TDD).

Validates audit-render-audio-coverage.py: narration coverage on the rendered MP4 in the HYBRID
per-clip-atomic path. The validator exists to catch the under-narration class (pueblo-v2) that
audit-audio.py renders INVISIBLE because it parses <audio> tags from index.html (which don't exist
in per-clip-atomic) — and to refuse the false-PASS of reading a legacy HTML for an atomic render.

Cases:
  - PURE good: coverage 85%, no gap >2s → PASS (ok=True).
  - PURE bad: coverage 30% → FAIL (the pueblo-v2 under-narration bug).
  - PURE bad: 3s narrative dead-zone inside the narrated span → FAIL.
  - GUARD: per_clip_atomic + --html → exit 2 'wrong_architecture' (no false PASS off HTML).
  - GATE: has_tts_narration=false → exit 0 'not_applicable'.
  - CLI: missing --format → nonzero; missing --video (with tts) → exit 2.
  - Runtime path (CLI exit 0/1) with whisper + silencedetect + ffprobe MOCKED (no media, no deps).
  - silencedetect parser + segment union edge cases.

MOCKS: ffprobe_duration, whisper_transcribe_mp4, ffmpeg_silence_zones (monkeypatched in-process so
the test never touches real media, ffmpeg, or whisper). Strategy/SPEC reads use real temp files.

Runnable: python3 test_audit-render-audio-coverage.py  (prints "OK: ..." / sys.exit(1) on failure).
"""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

pytestmark = pytest.mark.ffmpeg  # synthesises fixtures with ffmpeg lavfi

HERE = Path(__file__).parent
SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_render_audio_coverage.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("arac", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MOD = _load_module()


def _segs(*pairs):
    """[(start,end), ...] → whisper-style segments with text."""
    return [{"start": a, "end": b, "text": "narra"} for a, b in pairs]


def _run_cli(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# PURE LOGIC
# ---------------------------------------------------------------------------
def test_pure_good_passes():
    # 84% coverage over 100s with only a clean 1.0s gap (≤ 2.0s) inside the span.
    segs = _segs((0, 42.5), (43.5, 85.0))  # 42.5 + 41.5 = 84.0s coverage
    ok, reasons = MOD.evaluate_audio_coverage(segs, total_dur=100.0,
                                              silence_zones=[(42.5, 43.5)],  # 1.0s gap ≤ 2.0
                                              min_coverage=40.0)
    if not ok:
        _fail(f"good case should PASS, got reasons={reasons}")
    print("OK: pure good case (84% coverage, 1.0s gap) PASSES")


def test_pure_low_coverage_fails():
    # 30% coverage — the pueblo-v2 under-narration class.
    segs = _segs((0, 15.0), (50.0, 65.0))  # 30s / 100s = 30%
    ok, reasons = MOD.evaluate_audio_coverage(segs, total_dur=100.0,
                                              silence_zones=[], min_coverage=40.0)
    if ok:
        _fail("30% coverage must FAIL")
    if not any("LOW_NARRATION_COVERAGE" in r for r in reasons):
        _fail(f"expected LOW_NARRATION_COVERAGE reason, got {reasons}")
    print("OK: pure low-coverage (30%) FAILS with LOW_NARRATION_COVERAGE")


def test_pure_dead_zone_fails():
    # Good coverage but a 3s silence INSIDE the narrated span → narrator vanished mid-video.
    segs = _segs((0, 40.0), (43.0, 90.0))  # 40 + 47 = 87s / 100 = 87% coverage (high)
    # silence 40.0..43.0 = 3.0s, inside span [0, 90] → narrative dead-zone.
    ok, reasons = MOD.evaluate_audio_coverage(segs, total_dur=100.0,
                                              silence_zones=[(40.0, 43.0)], min_coverage=40.0)
    if ok:
        _fail("3s narrative dead-zone must FAIL despite high coverage")
    if not any("NARRATIVE_DEAD_ZONE" in r for r in reasons):
        _fail(f"expected NARRATIVE_DEAD_ZONE reason, got {reasons}")
    print("OK: pure 3s dead-zone inside span FAILS with NARRATIVE_DEAD_ZONE")


def test_pure_trailing_silence_not_a_gap():
    # Silence AFTER the last word (cliffhanger tail) is NOT a narrative gap.
    segs = _segs((0, 50.0))  # 50% coverage
    ok, reasons = MOD.evaluate_audio_coverage(segs, total_dur=100.0,
                                              silence_zones=[(50.0, 100.0)],  # 50s tail, outside span
                                              min_coverage=40.0)
    if not ok:
        _fail(f"trailing silence after last word must NOT count as a gap; reasons={reasons}")
    print("OK: trailing silence after last narrated word is NOT a narrative gap")


def test_pure_invalid_duration():
    ok, reasons = MOD.evaluate_audio_coverage(_segs((0, 5)), total_dur=0.0,
                                              silence_zones=[], min_coverage=40.0)
    if ok or not any("INVALID_DURATION" in r for r in reasons):
        _fail(f"total_dur=0 must FAIL with INVALID_DURATION; reasons={reasons}")
    print("OK: total_dur=0 → INVALID_DURATION FAIL")


def test_segments_union_overlap():
    # Overlapping segments must not double-count.
    secs = MOD.segments_coverage_seconds(_segs((0, 10), (5, 15)))  # union = 15s
    if abs(secs - 15.0) > 1e-6:
        _fail(f"overlap union should be 15.0s, got {secs}")
    print("OK: overlapping segments union = 15.0s (no double count)")


def test_silencedetect_parser():
    stderr = (
        "[silencedetect @ 0x1] silence_start: 12.5\n"
        "[silencedetect @ 0x1] silence_end: 15.0 | silence_duration: 2.5\n"
        "[silencedetect @ 0x1] silence_start: 40.0\n"
        "[silencedetect @ 0x1] silence_end: 41.0 | silence_duration: 1.0\n"
    )
    zones = MOD.parse_silencedetect(stderr)
    if zones != [(12.5, 15.0), (40.0, 41.0)]:
        _fail(f"silencedetect parse wrong: {zones}")
    print("OK: silencedetect stderr parsed to 2 zones")


# ---------------------------------------------------------------------------
# RUNTIME PATH (in-process main() with MOCKED media wrappers)
# ---------------------------------------------------------------------------
def _patch_runtime(duration, segments, silence_zones):
    MOD.ffprobe_duration = lambda v: duration
    MOD.whisper_transcribe_mp4 = lambda v, language="es", model_name="base": segments
    MOD.ffmpeg_silence_zones = lambda v, noise_db=-35.0, min_silence_s=0.5: silence_zones


def test_cli_runtime_good_pass(tmp):
    fake_mp4 = tmp / "render.mp4"
    fake_mp4.write_bytes(b"\x00")  # exists; never decoded (mocked)
    _patch_runtime(100.0, _segs((0, 42.5), (43.5, 85.0)), [(42.5, 43.5)])
    rc = MOD.main_with_argv(["--format", "horror-choice", "--video", str(fake_mp4)])
    if rc != 0:
        _fail(f"mocked good render should exit 0, got {rc}")
    print("OK: CLI runtime good render (mocked) → exit 0 PASS")


def test_cli_runtime_low_coverage_fail(tmp):
    fake_mp4 = tmp / "render2.mp4"
    fake_mp4.write_bytes(b"\x00")
    _patch_runtime(100.0, _segs((0, 15.0), (50.0, 65.0)), [])  # 30%
    rc = MOD.main_with_argv(["--format", "horror-choice", "--video", str(fake_mp4)])
    if rc != 1:
        _fail(f"mocked 30% render should exit 1 (FAIL), got {rc}")
    print("OK: CLI runtime low-coverage render (mocked, 30%) → exit 1 FAIL")


# ---------------------------------------------------------------------------
# GUARDS / GATES (CLI via subprocess — no media touched on these paths)
# ---------------------------------------------------------------------------
def test_guard_atomic_plus_html_exit2(tmp):
    manifest = tmp / "_batch_manifest.json"
    manifest.write_text(json.dumps({
        "assembly_strategy": "per_clip_atomic",
        "shots": [{"shot_id": "s1", "format_version": "atomic_v1", "audit_status": "PASS"}],
    }), encoding="utf-8")
    html = tmp / "index.html"
    html.write_text("<audio src='legacy.mp3' data-start='0' data-duration='90' data-track-index='1'>",
                    encoding="utf-8")
    fake_mp4 = tmp / "r.mp4"; fake_mp4.write_bytes(b"\x00")
    r = _run_cli(["--format", "horror-choice", "--video", str(fake_mp4),
                  "--html", str(html), "--manifest", str(manifest)])
    if r.returncode != 2:
        _fail(f"per_clip_atomic + --html must exit 2, got {r.returncode}\n{r.stdout}\n{r.stderr}")
    if "wrong_architecture" not in r.stdout:
        _fail(f"expected wrong_architecture verdict; stdout={r.stdout}")
    print("OK: GUARD per_clip_atomic + --html → exit 2 wrong_architecture (no false PASS off HTML)")


def test_guard_atomic_inferred_from_manifest(tmp):
    # No explicit assembly_strategy key, but all shots atomic_v1 → inferred per_clip_atomic.
    manifest = tmp / "_batch_manifest.json"
    manifest.write_text(json.dumps({
        "shots": [{"shot_id": "s1", "format_version": "atomic_v1", "audit_status": "PASS"}],
    }), encoding="utf-8")
    html = tmp / "index.html"; html.write_text("<audio src='x'>", encoding="utf-8")
    fake_mp4 = tmp / "r.mp4"; fake_mp4.write_bytes(b"\x00")
    r = _run_cli(["--format", "horror-choice", "--video", str(fake_mp4),
                  "--html", str(html), "--manifest", str(manifest)])
    if r.returncode != 2:
        _fail(f"atomic inferred from atomic_v1 shots must exit 2, got {r.returncode}\n{r.stdout}")
    print("OK: GUARD atomic inferred from atomic_v1 manifest shots → exit 2")


def test_gate_no_tts_not_applicable(tmp):
    spec = tmp / "spec.yaml"
    spec.write_text('schema_version: "v11.1"\n'
                    'video_capabilities:\n  has_tts_narration: false\n', encoding="utf-8")
    fake_mp4 = tmp / "r.mp4"; fake_mp4.write_bytes(b"\x00")
    r = _run_cli(["--format", "tutorial", "--video", str(fake_mp4), "--spec", str(spec)])
    if r.returncode != 0:
        _fail(f"has_tts_narration=false must exit 0, got {r.returncode}\n{r.stdout}")
    if "not_applicable" not in r.stdout:
        _fail(f"expected not_applicable; stdout={r.stdout}")
    print("OK: GATE has_tts_narration=false → exit 0 not_applicable")


def test_cli_missing_format_nonzero():
    r = _run_cli(["--video", "x.mp4"])
    if r.returncode == 0:
        _fail("missing --format must exit nonzero (Pattern 7 agnostic-by-design)")
    print("OK: CLI missing --format → nonzero exit")


def test_cli_missing_video_exit2(tmp):
    # has_tts unknown (no spec) → defaults to audit branch; no --video → exit 2 can't-measure.
    r = _run_cli(["--format", "horror-choice"])
    if r.returncode != 2:
        _fail(f"missing --video (audit branch) must exit 2, got {r.returncode}\n{r.stderr}")
    print("OK: CLI missing --video on audit branch → exit 2 can't-measure")


if __name__ == "__main__":
    # Pure-function tests (no temp dir).
    test_pure_good_passes()
    test_pure_low_coverage_fails()
    test_pure_dead_zone_fails()
    test_pure_trailing_silence_not_a_gap()
    test_pure_invalid_duration()
    test_segments_union_overlap()
    test_silencedetect_parser()

    # In-process runtime tests (mocked media).
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        test_cli_runtime_good_pass(tmp)
        test_cli_runtime_low_coverage_fail(tmp)

    # GUARD / GATE / CLI subprocess tests.
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        test_guard_atomic_plus_html_exit2(tmp)
        test_guard_atomic_inferred_from_manifest(tmp)
        test_gate_no_tts_not_applicable(tmp)
        test_cli_missing_video_exit2(tmp)
    test_cli_missing_format_nonzero()

    print("\nOK: all audit-render-audio-coverage tests passed")
