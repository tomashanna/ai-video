#!/usr/bin/env python3
"""test_audit-caption-temporal-coverage.py — HR#30 companion test (Hard Rule #26).

Validates audit-caption-temporal-coverage.py both at the PURE layer (no IO) and the
RUNTIME layer (whisper/ffprobe/sidecar mocked — NO real media, NO heavy deps).

Run: python3 test_audit-caption-temporal-coverage.py
Prints "OK: ..." per assertion group; sys.exit(1) on any failure.

Cases (per spec):
  GOOD  → cues cover 95% of spoken span, each <3.5s, ≤2 lines           → PASS
  BAD   → 1 cue spans 6s (collapsed static block = the V5/V6 burn bug)  → FAIL
  BAD   → cues cover only ~50% of the spoken span                        → FAIL
  + edge: zero cues / silent clip / >2-line cue / interval merge / runtime e2e PASS+FAIL.
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_caption_temporal_coverage.py"


def _load_module():
    """Import the hyphenated script as a module so we can call its pure functions."""
    spec = importlib.util.spec_from_file_location("acc_mod", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load_module()


def check(cond, msg):
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)


# ===========================================================================
# 1. PURE LAYER — evaluate_caption_temporal
# ===========================================================================
def test_good_full_coverage_passes():
    # spoken span 0.5 .. 10.5  (10.0s). Cues are progressive, each <3.5s, 1-2 lines,
    # covering 0.5..10.0 = 9.5s = 95% → PASS.
    cues = [
        {"start_s": 0.5, "end_s": 3.0, "text": "Aterrizas de noche", "id": "n1"},
        {"start_s": 3.0, "end_s": 6.0, "text": "y la torre\nte espera", "id": "n2"},
        {"start_s": 6.0, "end_s": 8.5, "text": "Dos figuras", "id": "n3"},
        {"start_s": 8.5, "end_s": 10.0, "text": "Elige", "id": "n4"},
    ]
    ok, reasons = M.evaluate_caption_temporal(cues, (0.5, 10.5), total_dur=11.0)
    check(ok, f"GOOD case should PASS but failed: {reasons}")
    check(any("coverage=0.9" in r or "coverage=1.0" in r for r in reasons),
          f"coverage ratio not reported as ≥0.90: {reasons}")
    print("OK: GOOD full-coverage cues (95%, <3.5s each, ≤2 lines) → PASS")


def test_collapsed_block_6s_cue_fails():
    # THE V5/V6 BUG: one static cue carrying the whole narration. spoken span 10s,
    # a single cue 0..6 (covers 60%) AND it spans 6s > 3.5s → must FAIL (collapsed block).
    cues = [{"start_s": 0.0, "end_s": 6.0,
             "text": "Aterrizas de noche y la torre te espera con dos figuras", "id": "blob"}]
    ok, reasons = M.evaluate_caption_temporal(cues, (0.0, 10.0), total_dur=11.0)
    check(not ok, f"collapsed-block 6s cue MUST FAIL but passed: {reasons}")
    check(any("collapsed static block" in r for r in reasons),
          f"collapsed-block reason not present: {reasons}")
    print("OK: BAD collapsed 6s static cue (V5/V6 burn bug) → FAIL")


def test_half_coverage_fails():
    # Cues cover only ~50% of a 10s spoken span (5.0..10.0 uncaptioned).
    cues = [
        {"start_s": 0.0, "end_s": 2.5, "text": "Aterrizas", "id": "n1"},
        {"start_s": 2.5, "end_s": 5.0, "text": "de noche", "id": "n2"},
    ]
    ok, reasons = M.evaluate_caption_temporal(cues, (0.0, 10.0), total_dur=11.0)
    check(not ok, f"50% coverage MUST FAIL but passed: {reasons}")
    check(any(r.startswith("coverage=0.5") for r in reasons),
          f"coverage ~0.50 not reported: {reasons}")
    check(any("do NOT span" in r for r in reasons),
          f"coverage-fail reason not present: {reasons}")
    print("OK: BAD 50% temporal coverage → FAIL")


def test_zero_cues_over_speech_fails():
    ok, reasons = M.evaluate_caption_temporal([], (0.0, 8.0), total_dur=9.0)
    check(not ok, "no cues over spoken audio MUST FAIL")
    check(any("NO caption cues" in r for r in reasons), f"existence-fail reason missing: {reasons}")
    print("OK: EDGE zero cues over an 8s spoken span (existence) → FAIL")


def test_silent_clip_not_applicable():
    # No spoken span (music-only) → not this validator's job to fail.
    ok, reasons = M.evaluate_caption_temporal([], None, total_dur=9.0)
    check(ok, f"silent clip should NOT fail (N/A) but failed: {reasons}")
    ok2, _ = M.evaluate_caption_temporal([], (4.0, 4.0), total_dur=9.0)  # zero-length span
    check(ok2, "zero-length spoken span should be N/A (ok=True)")
    print("OK: EDGE silent / zero-length spoken span → N/A (PASS, not a false FAIL)")


def test_three_line_cue_fails():
    # Good coverage + short cues, but one cue has 3 lines → FAIL (reel safe zone).
    cues = [
        {"start_s": 0.0, "end_s": 3.0, "text": "linea uno\nlinea dos\nlinea tres", "id": "n1"},
        {"start_s": 3.0, "end_s": 6.0, "text": "ok", "id": "n2"},
        {"start_s": 6.0, "end_s": 9.5, "text": "fin", "id": "n3"},
    ]
    ok, reasons = M.evaluate_caption_temporal(cues, (0.0, 10.0), total_dur=11.0)
    check(not ok, f"3-line cue MUST FAIL but passed: {reasons}")
    check(any("lines >" in r for r in reasons), f"line-count reason missing: {reasons}")
    print("OK: EDGE cue with 3 lines → FAIL (reel safe zone)")


def test_merge_intervals_and_clipping():
    # Overlapping cues must not double-count; caption time outside the spoken span is clipped.
    merged = M.merge_intervals([(0, 2), (1, 3), (5, 6)])
    check(merged == [(0.0, 3.0), (5.0, 6.0)], f"merge_intervals wrong: {merged}")
    # cue extends beyond the spoken span — only the overlap counts
    covered = M.covered_within_span(
        [{"start_s": 0.0, "end_s": 20.0, "text": "x"}], span_start=2.0, span_end=10.0)
    check(abs(covered - 8.0) < 1e-6, f"clipping to spoken span wrong: {covered}")
    print("OK: EDGE interval merge (no double-count) + clip caption to spoken span")


def test_threshold_boundary_exactly_90_passes():
    # Exactly 90% coverage of a 10s span, all cues short → PASS (boundary not a false FAIL).
    cues = [
        {"start_s": 0.0, "end_s": 3.0, "text": "a", "id": "n1"},
        {"start_s": 3.0, "end_s": 6.0, "text": "b", "id": "n2"},
        {"start_s": 6.0, "end_s": 9.0, "text": "c", "id": "n3"},
    ]
    ok, reasons = M.evaluate_caption_temporal(cues, (0.0, 10.0), total_dur=11.0)
    check(ok, f"exactly 90% coverage should PASS but failed: {reasons}")
    print("OK: EDGE coverage exactly at 90% threshold → PASS")


# ===========================================================================
# 2. RUNTIME LAYER — end-to-end with whisper/ffprobe/sidecar MOCKED (no media)
# ===========================================================================
def _mock_runtime(span, total_dur):
    """Monkeypatch the module's IO functions so main() runs with no real media/deps."""
    M.whisper_spoken_span = lambda *a, **k: span
    M.ffprobe_duration = lambda *a, **k: total_dur


def _write_sidecar(dirpath: Path, captions: list[dict]) -> Path:
    """Write a build_clip_atomic-style sidecar (build_caption_sidecar schema)."""
    p = dirpath / "shot_01_captions.json"
    p.write_text(json.dumps({
        "shot_id": "shot_01", "duration_s": 11.0, "global_window_s": [0.0, 11.0],
        "captions": captions, "format_version": "atomic_v1",
    }), encoding="utf-8")
    return p


def _run_main(argv):
    """Call main() with patched sys.argv; capture exit code + stdout."""
    import contextlib
    import io
    old_argv = sys.argv
    sys.argv = ["audit-caption-temporal-coverage.py"] + argv
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = M.main()
    finally:
        sys.argv = old_argv
    return code, buf.getvalue()


def test_runtime_e2e_good_passes():
    tmp = Path(tempfile.mkdtemp())
    video = tmp / "draft.mp4"; video.write_bytes(b"fake")  # existence only; IO is mocked
    _write_sidecar(tmp, [
        {"id": "n1", "text": "Aterrizas de noche", "global_start_s": 0.5, "global_end_s": 3.0},
        {"id": "n2", "text": "y la torre te espera", "global_start_s": 3.0, "global_end_s": 6.0},
        {"id": "n3", "text": "Dos figuras", "global_start_s": 6.0, "global_end_s": 8.5},
        {"id": "n4", "text": "Elige", "global_start_s": 8.5, "global_end_s": 10.0},
    ])
    _mock_runtime(span=(0.5, 10.5), total_dur=11.0)
    code, out = _run_main(["--format", "horror-choice", "--video", str(video),
                           "--project-dir", str(tmp)])
    rep = json.loads(out)
    check(code == 0, f"runtime GOOD should exit 0, got {code}\n{out}")
    check(rep["overall_status"] == "pass", f"expected pass, got {rep['overall_status']}")
    check(rep["cue_count"] == 4 and rep["cue_source"].startswith("sidecar"),
          f"sidecar cues not loaded: {rep}")
    print("OK: RUNTIME e2e GOOD (mocked whisper+ffprobe+sidecar) → exit 0 PASS")


def test_runtime_e2e_collapsed_block_fails():
    tmp = Path(tempfile.mkdtemp())
    video = tmp / "draft.mp4"; video.write_bytes(b"fake")
    _write_sidecar(tmp, [  # the V5/V6 bug: ONE 6s cue carrying the whole narration
        {"id": "blob", "text": "Aterrizas de noche y la torre te espera con dos figuras",
         "global_start_s": 0.0, "global_end_s": 6.0},
    ])
    _mock_runtime(span=(0.0, 10.0), total_dur=11.0)
    code, out = _run_main(["--format", "horror-choice", "--video", str(video),
                           "--project-dir", str(tmp)])
    rep = json.loads(out)
    check(code == 1, f"runtime collapsed-block should exit 1, got {code}\n{out}")
    check(rep["overall_status"] == "fail", f"expected fail, got {rep['overall_status']}")
    check(any("collapsed static block" in r for r in rep["reasons"]),
          f"collapsed-block reason missing in report: {rep['reasons']}")
    print("OK: RUNTIME e2e BAD collapsed 6s cue → exit 1 FAIL")


def test_runtime_capability_gate_not_applicable():
    code, out = _run_main(["--format", "tutorial", "--has-captions-baked", "false"])
    rep = json.loads(out)
    check(code == 0, f"not_applicable must exit 0, got {code}")
    check(rep["overall_status"] == "not_applicable", f"expected not_applicable: {rep}")
    print("OK: RUNTIME capability gate has_captions_baked=false → exit 0 not_applicable")


def test_runtime_no_cues_cant_measure_exit2():
    # No sidecar + no --ocr → can't read cues → exit 2 (NOT a false PASS).
    tmp = Path(tempfile.mkdtemp())
    video = tmp / "draft.mp4"; video.write_bytes(b"fake")
    _mock_runtime(span=(0.0, 10.0), total_dur=11.0)
    code, out = _run_main(["--format", "horror-choice", "--video", str(video),
                           "--project-dir", str(tmp)])
    check(code == 2, f"no cues + no ocr must exit 2 (can't-measure), got {code}\n{out}")
    print("OK: RUNTIME no sidecar + no --ocr → exit 2 (can't-measure, no false PASS)")


if __name__ == "__main__":
    # PURE
    test_good_full_coverage_passes()
    test_collapsed_block_6s_cue_fails()
    test_half_coverage_fails()
    test_zero_cues_over_speech_fails()
    test_silent_clip_not_applicable()
    test_three_line_cue_fails()
    test_merge_intervals_and_clipping()
    test_threshold_boundary_exactly_90_passes()
    # RUNTIME (mocked)
    test_runtime_e2e_good_passes()
    test_runtime_e2e_collapsed_block_fails()
    test_runtime_capability_gate_not_applicable()
    test_runtime_no_cues_cant_measure_exit2()
    print("OK: ALL audit-caption-temporal-coverage tests passed")
