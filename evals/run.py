"""Eval harness for the AI-video pipeline.

    uv run python -m evals.run                 # all suites (render suite auto-skips without ffmpeg)
    uv run python -m evals.run --suite spec    # one suite: spec | captions | safe_zone | rubric | render
    uv run python -m evals.run --json evals/out/report.json

Suites
------
spec       Each case injects one defect into a synthetic spec and asserts the real gate
           (validate-spec, language style, voice exclusivity, narration fit) catches it —
           and that the clean baseline passes (no false positives).
captions   Whisper-like word timings -> real caption grouping -> timing/readability/coverage checks.
safe_zone  Caption placement vs the empirical caption band measured on referents.
rubric     Calibrated-v4 weighted scoring + HR#1 verdict logic over recorded judge outputs
           (swap FixtureJudge for GeminiJudge to score real renders).
render     Synthetic 9:16 clips generated with ffmpeg: duration/resolution/fps/loudness checks,
           including deliberately broken variants that must be rejected.

Exit code 0 when every case matches its expectation, 1 otherwise.
"""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from ai_video.core import empirical_bands as eb
from ai_video.providers.captions import group_into_captions
from evals import checks, media
from evals.rubric import FixtureJudge, Thresholds, verdict

HERE = Path(__file__).resolve().parent
CASES = yaml.safe_load((HERE / "cases.yaml").read_text(encoding="utf-8"))
BASE_SPEC = yaml.safe_load((HERE / "fixtures" / "base_spec.yaml").read_text(encoding="utf-8"))


@dataclass
class CaseResult:
    suite: str
    case: str
    expected: str
    actual: str
    ok: bool
    detail: str = ""
    seconds: float = 0.0


# ----------------------------------------------------------------- spec helpers


def _walk(obj: Any, dotted: str) -> tuple[Any, Any]:
    parts = dotted.split(".")
    for p in parts[:-1]:
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    last = parts[-1]
    return obj, int(last) if isinstance(obj, list) else last


def apply_patch(spec: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(spec)
    for path, value in (case.get("set") or {}).items():
        parent, key = _walk(out, path)
        parent[key] = value
    for path, item in (case.get("append") or {}).items():
        parent, key = _walk(out, path)
        parent[key].append(item)
    return out


def run_gate(gate: str, spec_path: Path, extra: list[str]) -> tuple[int, str]:
    if gate == "validate-spec":
        cmd = [sys.executable, "-m", "ai_video.cli", gate, str(spec_path)]
    else:
        cmd = [
            sys.executable,
            "-m",
            "ai_video.cli",
            gate,
            *extra,
            "--format",
            "horror-choice",
            "--spec",
            str(spec_path),
        ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return r.returncode, summarize_output(r.stdout + r.stderr)


def summarize_output(text: str) -> str:
    """Short human summary of a gate's output (JSON report or plain text)."""
    try:
        start = text.index("{")
        report, _ = json.JSONDecoder().raw_decode(text[start:])
    except ValueError:
        lines = text.strip().splitlines()
        return lines[-1][:160] if lines else ""
    failing: list[str] = []

    def walk(o: Any, key: str | None = None) -> None:
        if isinstance(o, dict):
            label = o.get("check") or o.get("gate") or o.get("name") or key
            if (o.get("status") == "fail" and "source" not in o and label) or o.get("kind") == "overlap":
                failing.append(str(label or o.get("kind")))
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, None)

    walk(report)
    status = report.get("overall_status", "?") if isinstance(report, dict) else "?"
    return f"status={status} failing={sorted(set(failing)) or '-'}"


def suite_spec(tmp: Path) -> list[CaseResult]:
    results = []
    for case in CASES["spec_cases"]:
        t0 = time.monotonic()
        spec = apply_patch(BASE_SPEC, case)
        path = tmp / f"{case['id']}.yaml"
        path.write_text(yaml.safe_dump(spec, allow_unicode=True, sort_keys=False), encoding="utf-8")
        rc, tail = run_gate(case["gate"], path, list(case.get("args", [])))
        actual = {0: "pass", 1: "fail"}.get(rc, f"error({rc})")
        results.append(
            CaseResult(
                "spec",
                f"{case['gate']}:{case['id']}",
                case["expect"],
                actual,
                actual == case["expect"],
                tail,
                time.monotonic() - t0,
            )
        )
    return results


# ------------------------------------------------------------- other suites


def suite_captions(_: Path) -> list[CaseResult]:
    results = []
    for case in CASES["caption_cases"]:
        words = [{"word": w, "start": s, "end": e} for w, s, e in case["words"]]
        cues = group_into_captions(words)
        res = checks.check_caption_timing(
            cues, [(w["start"], w["end"]) for w in words], video_duration_s=case["video_duration_s"]
        )
        failed = [r.name for r in res if not r.passed]
        actual = "fail" if failed else "pass"
        results.append(
            CaseResult(
                "captions",
                case["id"],
                case["expect"],
                actual,
                actual == case["expect"],
                f"{len(cues)} cues; failed: {failed or '-'}",
            )
        )
    return results


def suite_safe_zone(_: Path) -> list[CaseResult]:
    band = eb.ui_band("horror-choice", "captions_narration")
    results = []
    for case in CASES["safe_zone_cases"]:
        y = checks.caption_y_pct(case["margin_v_px"], case["font_size_px"], case["height_px"])
        r = checks.check_in_band("caption_y_pct", y, band, slack=2.0)
        actual = "pass" if r.passed else "fail"
        results.append(
            CaseResult("safe_zone", case["id"], case["expect"], actual, actual == case["expect"], r.detail)
        )
    return results


def suite_rubric(_: Path) -> list[CaseResult]:
    path = HERE / "fixtures" / "judge_scores.json"
    judge, data = FixtureJudge(path), json.loads(path.read_text(encoding="utf-8"))
    th = Thresholds.from_hard_rules()
    results = []
    for rid, rec in data.items():
        if rid.startswith("_"):
            continue
        v = verdict(rid, judge(rid), th, rec.get("perceptual"))
        ok = v.status == rec["expect"] and v.weakest == rec.get("expect_weakest", v.weakest)
        results.append(
            CaseResult(
                "rubric",
                rid,
                rec["expect"],
                v.status,
                ok,
                f"score {v.score:.2f} (threshold {th.calibrated}), weakest={v.weakest}",
            )
        )
    return results


def suite_render(tmp: Path) -> list[CaseResult]:
    if not media.have_ffmpeg():
        return [CaseResult("render", "*", "pass", "skipped", True, "ffmpeg/ffprobe not on PATH")]
    variants: list[tuple[str, dict[str, Any], str]] = [
        ("reel-ok", {"seconds": 3.0}, "pass"),
        ("wrong-aspect", {"seconds": 3.0, "size": "1920x1080"}, "fail"),
        ("too-quiet", {"seconds": 3.0, "tone_lufs": None}, "fail"),
        ("wrong-fps", {"seconds": 3.0, "fps": 24}, "fail"),
    ]
    results = []
    for name, kw, expect in variants:
        t0 = time.monotonic()
        clip = media.make_clip(tmp / f"{name}.mp4", **kw)
        p = media.probe(clip)
        lufs, tp = media.loudness(clip)
        rs = [
            checks.check_duration(p.duration_s, 3.0, tol_s=0.1),
            checks.check_resolution(p.width, p.height),
            checks.check_fps(p.fps),
            checks.check_loudness(lufs),
            checks.check_true_peak(tp),
        ]
        failed = [r.name for r in rs if not r.passed]
        actual = "fail" if failed else "pass"
        results.append(
            CaseResult(
                "render",
                name,
                expect,
                actual,
                actual == expect,
                f"{p.width}x{p.height}@{p.fps:.0f} {p.duration_s:.2f}s {lufs:.1f}LUFS; "
                f"failed: {failed or '-'}",
                time.monotonic() - t0,
            )
        )
    return results


SUITES: dict[str, Callable[[Path], list[CaseResult]]] = {
    "spec": suite_spec,
    "captions": suite_captions,
    "safe_zone": suite_safe_zone,
    "rubric": suite_rubric,
    "render": suite_render,
}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Run ai-video evals")
    ap.add_argument("--suite", choices=[*SUITES, "all"], default="all")
    ap.add_argument("--json", type=Path, help="write a JSON report here")
    a = ap.parse_args(argv)

    names = list(SUITES) if a.suite == "all" else [a.suite]
    results: list[CaseResult] = []
    with tempfile.TemporaryDirectory(prefix="ai-video-evals-") as tmp:
        for n in names:
            results += SUITES[n](Path(tmp))

    width = max(len(r.case) for r in results)
    for r in results:
        mark = "ok  " if r.ok else "MISS"
        print(f"{mark} {r.suite:<9} {r.case:<{width}}  expect={r.expected:<20} got={r.actual:<20} {r.detail}")
    passed = sum(r.ok for r in results)
    print(f"\n{passed}/{len(results)} eval cases matched expectations")
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(
            json.dumps([asdict(r) for r in results], indent=2, ensure_ascii=False), encoding="utf-8"
        )
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
