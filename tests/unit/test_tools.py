"""Render lock, SRT->ASS conversion, caption grouping/emission and the ai-video CLI dispatcher."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from ai_video import cli
from ai_video.build import render_lock as RL
from ai_video.editor import make_ass as MA
from ai_video.providers import captions as CAP

# ------------------------------------------------------------------ render lock


def test_lock_acquire_is_exclusive_and_release_by_project(tmp_path: Path):
    lock = tmp_path / "r.lock"
    assert RL.acquire("video-a", 10, pid=os.getpid(), path=lock) == RL.EXIT_OK
    assert RL.acquire("video-b", 10, pid=os.getpid(), path=lock) == RL.EXIT_HELD
    assert RL.release("video-b", path=lock) == RL.EXIT_HELD  # not ours, still live
    assert RL.release("video-a", path=lock) == RL.EXIT_OK
    assert not lock.exists()


def test_lock_with_dead_pid_stays_live_within_ttl(tmp_path: Path):
    """Regression: the old lock stored the CLI's own pid and was stale immediately."""
    lock = tmp_path / "r.lock"
    dead_pid = 999_999
    assert RL.acquire("video-a", 15, pid=dead_pid, path=lock) == RL.EXIT_OK
    assert RL.acquire("video-b", 15, pid=dead_pid, path=lock) == RL.EXIT_HELD


def test_lock_expired_ttl_is_recovered(tmp_path: Path):
    lock = tmp_path / "r.lock"
    old = (datetime.now(UTC) - timedelta(hours=3)).isoformat()
    lock.write_text(
        json.dumps({"pid": 999_999, "project": "old", "started_at": old, "expected_duration_min": 10})
    )
    assert RL.acquire("new", 10, pid=999_999, path=lock) == RL.EXIT_STALE_RECOVERED
    assert RL.read_lock(lock)["project"] == "new"


def test_lock_corrupt_file_is_recovered_and_force_release(tmp_path: Path):
    lock = tmp_path / "r.lock"
    lock.write_text("{not json")
    assert RL.acquire("p", pid=os.getpid(), path=lock) == RL.EXIT_STALE_RECOVERED
    assert RL.release(None, force=True, path=lock) == RL.EXIT_OK


def test_is_live_rules():
    now = datetime(2026, 1, 1, 12, tzinfo=UTC)
    base = {"pid": 999_999, "expected_duration_min": 10}
    assert RL.is_live({**base, "started_at": (now - timedelta(minutes=14)).isoformat()}, now=now)
    assert not RL.is_live({**base, "started_at": (now - timedelta(minutes=16)).isoformat()}, now=now)
    assert RL.is_live({"pid": os.getpid()})
    assert not RL.is_live({"pid": 0, "started_at": "garbage"})


def test_render_lock_cli_roundtrip(tmp_path: Path):
    env = {**os.environ, "AIVIDEO_RENDER_LOCK": str(tmp_path / "cli.lock")}

    def run(*a: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "ai_video.build.render_lock", *a],
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )

    assert run("acquire", "proj", "--duration", "5").returncode == 0
    assert run("acquire", "other").returncode == 1
    assert "LIVE" in run("status").stdout
    assert run("release", "proj").returncode == 0
    assert "free" in run("status").stdout


# ---------------------------------------------------------------------- make-ass


@pytest.mark.parametrize(
    ("srt", "ass"),
    [
        ("00:00:03,040", "0:00:03.04"),
        ("00:00:59,995", "0:01:00.00"),  # carry instead of clamping to .99
        ("01:02:03,4", "1:02:03.40"),
        ("00:00:00.120", "0:00:00.12"),
    ],
)
def test_to_ass_time(srt: str, ass: str):
    assert MA.to_ass_time(srt) == ass


def test_to_ass_time_rejects_garbage():
    with pytest.raises(ValueError):
        MA.to_ass_time("3 seconds")


def test_parse_srt_and_build_ass():
    srt = "1\r\n00:00:01,000 --> 00:00:02,500\r\nHola {mundo}\r\nsegunda\r\n\r\n2\n00:00:03,000 --> 00:00:04,000\n\n"
    cues = MA.parse_srt(srt)
    assert len(cues) == 1
    assert cues[0].text == "Hola \\{mundo\\}\\Nsegunda"
    out = MA.build_ass(cues, 1080, 1920, 64, 380, bold=-1, font="Inter")
    assert "PlayResX: 1080" in out and "PlayResY: 1920" in out
    assert "Style: Default,Inter,64," in out and ",380,1" in out
    assert out.strip().endswith("Hola \\{mundo\\}\\Nsegunda")
    with pytest.raises(ValueError):
        MA.build_ass(cues, 0, 1920, 64, 380)
    with pytest.raises(ValueError):
        MA.build_ass(cues, 1080, 1920, 64, 380, bold=1)


def test_make_ass_cli_legacy_positional(tmp_path: Path):
    srt = tmp_path / "a.srt"
    srt.write_text("1\n00:00:00,000 --> 00:00:01,000\nhola\n", encoding="utf-8")
    out = tmp_path / "a.ass"
    r = subprocess.run(
        [
            sys.executable,
            "-m",
            "ai_video.editor.make_ass",
            str(srt),
            str(out),
            "576",
            "1024",
            "38",
            "130",
            "-1",
            "Georgia",
        ],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert r.returncode == 0, r.stderr
    assert "Style: Default,Georgia,38," in out.read_text()


# ----------------------------------------------------------------------- captions


def _w(word: str, start: float, end: float) -> dict:
    return {"word": word, "start": start, "end": end}


def test_group_into_captions_splits_on_punctuation_gaps_and_max():
    words = [_w("Elige", 0.0, 0.3), _w("bien.", 0.3, 0.6), _w("Uno", 0.62, 0.8), _w("dos", 1.5, 1.7)]
    words += [_w(f"w{i}", 2 + i * 0.1, 2.05 + i * 0.1) for i in range(7)]
    caps = CAP.group_into_captions(words)
    assert caps[0]["text"] == "ELIGE BIEN."
    assert caps[1]["text"] == "UNO"  # gap >= MIN_GAP_S forces a split
    assert all(len(c["text"].split()) <= CAP.MAX_WORDS_PER_CAPTION for c in caps)
    assert [c["start"] for c in caps] == sorted(c["start"] for c in caps)
    assert CAP.group_into_captions([]) == []


def test_emit_gsap_escapes_text():
    js = CAP.emit_gsap([{"text": 'DIJO "HOLA" </script>', "start": 1.0, "end": 2.0}], "cap", 10.0)
    assert 'textContent: "DIJO \\"HOLA\\" </script>"' in js
    assert "innerHTML" not in js
    assert ", 11.0);" in js and "opacity: 0 }, 12.05);" in js


# ---------------------------------------------------------------------------- CLI


def test_every_registered_tool_module_exists():
    for name, module in cli.TOOLS.items():
        assert cli.module_file(module) is not None, name


def test_cli_list_and_help(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["list"]) == 0
    out = capsys.readouterr().out
    assert "audit-ui-safe-zones" in out and "validate-spec" in out
    assert cli.main(["--help"]) == 0
    assert cli.main(["nope"]) == 2


def test_cli_dispatch_propagates_exit_codes(tmp_path: Path):
    spec = tmp_path / "s.yaml"
    spec.write_text("schema_version: v9\n", encoding="utf-8")
    assert cli.main(["validate-spec", str(spec)]) == 1
    assert cli.main(["render-lock", "--help"]) == 0
    assert cli.main(["validate-spec"]) == 2  # argparse error


def test_cli_budget_and_doctor(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["budget"]) == 0
    assert "remaining" in capsys.readouterr().out
    cli.main(["doctor"])
    out = capsys.readouterr().out
    assert "GEMINI_API_KEY" in out and "AIza" not in out
