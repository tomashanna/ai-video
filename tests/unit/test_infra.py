"""Robustness layer: settings, budget guard, retry/backoff, log redaction, paths, safe subprocess."""

from __future__ import annotations

import json
import logging
import random
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ai_video import budget, paths, proc
from ai_video.config import Settings, get_settings, reset_settings_cache
from ai_video.errors import BudgetExceededError, ConfigError, MissingDependencyError
from ai_video.log import REDACTED, JsonFormatter, RedactingFilter, redact
from ai_video.retry import backoff_delays, poll_until, retry_call

# --------------------------------------------------------------------- settings


def test_settings_read_env_and_hide_secrets(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AI" + "za" + "SyTESTTESTTESTTESTTESTTESTTESTTEST0")
    monkeypatch.setenv("AIVIDEO_BUDGET_USD", "2.5")
    reset_settings_cache()
    s = get_settings()
    assert s.budget_usd == 2.5
    assert s.require("gemini_api_key").startswith("AIza")
    assert "AIza" not in repr(s)  # SecretStr never leaks via repr


def test_require_missing_key_has_actionable_message():
    with pytest.raises(ConfigError, match=r"REPLICATE_API_TOKEN is not set.*\.env\.example"):
        get_settings().require("replicate_api_token")


def test_blank_key_counts_as_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "   ")
    reset_settings_cache()
    with pytest.raises(ConfigError):
        get_settings().require("elevenlabs_api_key")


def test_settings_reject_invalid_values(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("AIVIDEO_BUDGET_USD", "-1")
    with pytest.raises(ValueError):
        Settings()


def test_settings_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    env = tmp_path / "custom.env"
    env.write_text("ELEVENLABS_API_KEY=from-file-123456\n", encoding="utf-8")
    s = Settings(_env_file=str(env))  # type: ignore[call-arg]
    assert s.require("elevenlabs_api_key") == "from-file-123456"
    assert s.secret_values() == ["from-file-123456"]


# ----------------------------------------------------------------------- budget


def test_estimates_and_price_override(monkeypatch: pytest.MonkeyPatch):
    assert budget.estimate("kling_per_s", 10) == pytest.approx(budget.DEFAULT_PRICES["kling_per_s"] * 10)
    monkeypatch.setenv("AIVIDEO_PRICE_VEO_PER_S", "0")
    assert budget.estimate("veo_per_s", 8) == 0
    monkeypatch.setenv("AIVIDEO_PRICE_VEO_PER_S", "abc")
    with pytest.raises(ValueError, match="must be a number"):
        budget.price("veo_per_s")
    with pytest.raises(ValueError):
        budget.estimate("kling_per_s", -1)


def test_guard_records_and_blocks(tmp_path: Path):
    g = budget.BudgetGuard(
        tmp_path / "led.jsonl", limit_usd=1.0, now=lambda: datetime(2026, 1, 1, tzinfo=UTC)
    )
    with g.charge("replicate", "kling", 0.6):
        pass
    assert g.spent() == pytest.approx(0.6)
    assert g.remaining() == pytest.approx(0.4)
    with pytest.raises(BudgetExceededError, match="would exceed budget"):
        g.check(0.5)
    line = json.loads((tmp_path / "led.jsonl").read_text().splitlines()[0])
    assert line == {
        "provider": "replicate",
        "operation": "kling",
        "usd": 0.6,
        "ts": "2026-01-01T00:00:00+00:00",
    }


def test_guard_does_not_record_failed_calls(tmp_path: Path):
    g = budget.BudgetGuard(tmp_path / "led.jsonl", limit_usd=5)
    with pytest.raises(RuntimeError), g.charge("gemini", "image", 1.0):
        raise RuntimeError("api down")
    assert g.spent() == 0


def test_guard_tolerates_malformed_ledger_lines(tmp_path: Path):
    led = tmp_path / "led.jsonl"
    led.write_text('{"usd": 1.5}\nnot json\n{"nope": 1}\n\n{"usd": "0.5"}\n', encoding="utf-8")
    assert budget.BudgetGuard(led, 10).spent() == pytest.approx(2.0)


# ------------------------------------------------------------------------ retry


def test_backoff_is_exponential_and_capped():
    assert backoff_delays(5, base_s=1, max_s=5, jitter=0) == [1, 2, 4, 5]
    jittered = backoff_delays(4, base_s=10, jitter=0.2, rng=random.Random(0))
    assert all(8 <= d <= 48 for d in jittered)
    assert backoff_delays(1) == []


def test_retry_call_retries_then_succeeds():
    calls, sleeps = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise TimeoutError("slow")
        return "ok"

    assert retry_call(flaky, attempts=3, base_s=1, sleep=sleeps.append) == "ok"
    assert len(calls) == 3 and len(sleeps) == 2


def test_retry_call_reraises_and_respects_veto():
    sleeps: list[float] = []
    with pytest.raises(ValueError):
        retry_call(
            lambda: (_ for _ in ()).throw(ValueError("bad input")),
            attempts=5,
            should_retry=lambda e: not isinstance(e, ValueError),
            sleep=sleeps.append,
        )
    assert sleeps == []
    with pytest.raises(ValueError):
        retry_call(lambda: 1, attempts=0)


def test_retry_call_does_not_catch_unlisted_exceptions():
    with pytest.raises(KeyError):
        retry_call(lambda: {}["x"], attempts=3, retry_on=(TimeoutError,), sleep=lambda _s: None)


def test_poll_until_returns_and_times_out():
    seq = iter([None, None, "done"])
    assert poll_until(lambda: next(seq), timeout_s=10, interval_s=1, sleep=lambda _s: None) == "done"
    t = [0.0]

    def clock():
        t[0] += 4
        return t[0]

    with pytest.raises(TimeoutError, match="did not finish within 10s"):
        poll_until(lambda: None, timeout_s=10, sleep=lambda _s: None, clock=clock, describe="veo")


# ---------------------------------------------------------------------- logging


# Fake key *shapes*, assembled at runtime so secret scanners never see a key literal.
FAKE_KEYS = [
    "AI" + "za" + "SyA1234567890abcdefghijklmnopqrstuv",
    "r8" + "_abcdefghijklmnopqrstuvwxyz123456",
    "sk" + "_live_abcdefghijklmnopqrstuvwxyz",
]


@pytest.mark.parametrize("secret", FAKE_KEYS)
def test_redact_known_key_shapes(secret: str):
    out = redact(f"request failed with key={secret} trailing")
    assert secret not in out and REDACTED in out


def test_redact_headers_and_explicit_values():
    out = redact('headers {"x-goog-api-key": "plainvalue123"} custom=mysecretvalue', ["mysecretvalue"])
    assert "plainvalue123" not in out and "mysecretvalue" not in out


def test_redacting_filter_and_json_formatter():
    rec = logging.LogRecord(
        "ai_video.t", logging.INFO, __file__, 1, "token %s used", ("supersecret123",), None
    )
    assert RedactingFilter(["supersecret123"]).filter(rec)
    payload = json.loads(JsonFormatter().format(rec))
    assert payload["msg"] == f"token {REDACTED} used" and payload["level"] == "INFO"


# ------------------------------------------------------------------------ paths


def test_repo_root_and_derived_paths_exist():
    root = paths.repo_root()
    assert (root / "pyproject.toml").is_file()
    for p in (
        paths.library_dir(),
        paths.transitions_dir(),
        paths.avu_dir(),
        paths.voice_effects_catalog(),
        paths.model_capabilities_matrix(),
        paths.hard_rules_doc(),
        paths.human_checklist_doc(),
        paths.referent_analysis_dir(),
        paths.example_specs_dir(),
    ):
        assert p.exists(), p
    assert paths.prompt_path("calibrated-gemini-prompt-v4.txt").is_file()
    with pytest.raises(ConfigError):
        paths.prompt_path("nope.txt")


def test_resolve_asset_maps_legacy_prefixes(tmp_path: Path):
    assert (
        paths.resolve_asset("library/sfx/cuts/x.mp3", base=tmp_path)
        == tmp_path / "assets/library/sfx/cuts/x.mp3"
    )
    assert (
        paths.resolve_asset("transitions/catalog.json", base=tmp_path)
        == tmp_path / "assets/transitions/catalog.json"
    )
    assert paths.resolve_asset("assets/avu/a.mp4", base=tmp_path) == tmp_path / "assets/avu/a.mp4"
    assert paths.resolve_asset("/abs/file.mp3") == Path("/abs/file.mp3")


def test_repo_root_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    paths.repo_root.cache_clear()
    monkeypatch.setenv("AIVIDEO_REPO_ROOT", str(tmp_path))
    try:
        assert paths.repo_root() == tmp_path.resolve()
        monkeypatch.setenv("AIVIDEO_REPO_ROOT", str(tmp_path / "missing"))
        paths.repo_root.cache_clear()
        with pytest.raises(ConfigError):
            paths.repo_root()
    finally:
        monkeypatch.delenv("AIVIDEO_REPO_ROOT")
        paths.repo_root.cache_clear()


# ------------------------------------------------------------------------- proc


def test_run_rejects_shell_strings_and_missing_binaries():
    with pytest.raises(TypeError):
        proc.run("ls -la")  # type: ignore[arg-type]
    with pytest.raises(MissingDependencyError, match="not found on PATH"):
        proc.run(["definitely-not-a-binary-xyz"])


def test_run_executes_argument_lists(tmp_path: Path):
    weird = tmp_path / "a; rm -rf x.txt"  # would be dangerous under shell=True
    weird.write_text("hi", encoding="utf-8")
    res = proc.run(["cat", str(weird)], timeout=10)
    assert res.stdout == "hi"
