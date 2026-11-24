"""ElevenLabs TTS provider: voice defaults, validation, budget guard and retries (client mocked)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ai_video import paths
from ai_video.budget import BudgetGuard
from ai_video.config import get_settings
from ai_video.errors import AIVideoError, BudgetExceededError, ConfigError
from ai_video.providers import tts

DEPRECATED = "Tj9l48J9AJbry5yCP5eW"


def _client(chunks=(b"ID3", b"audio")):
    c = MagicMock()
    c.text_to_speech.convert.return_value = iter(chunks)
    return c


def test_default_voice_comes_from_catalog_and_is_not_deprecated():
    catalog = json.loads((paths.library_dir() / "voices-catalog.json").read_text(encoding="utf-8"))
    vid = tts.default_voice_id()
    assert vid == catalog["default_voice"]
    assert vid != DEPRECATED
    assert vid != catalog.get("default_voice_DEPRECATED_2026_05_18")


@pytest.mark.parametrize(
    ("kwargs", "msg"),
    [
        ({"text": "  "}, "empty"),
        ({"text": "x" * (tts.MAX_CHARS + 1)}, "split"),
        ({"model": "nope"}, "unknown model"),
        ({"stability": 1.5}, "stability"),
        ({"speed": 2.0}, "speed"),
    ],
)
def test_request_validation(kwargs, msg):
    base = {"text": "hola", "voice_id": "v"}
    base.update(kwargs)
    with pytest.raises(ValueError, match=msg):
        tts.TTSRequest(**base).validate()


def test_cost_scales_with_characters():
    short = tts.TTSRequest("a" * 1000, "v").estimated_cost()
    long = tts.TTSRequest("a" * 3000, "v").estimated_cost()
    assert long == pytest.approx(short * 3)


def test_synthesize_writes_file_and_records_spend(tmp_path: Path):
    guard = BudgetGuard(tmp_path / "ledger.jsonl", limit_usd=5)
    out = tmp_path / "out" / "narr.mp3"
    client = _client()
    n = tts.synthesize(tts.TTSRequest("Elige a tu compañero.", "voice123"), out, client=client, guard=guard)
    assert n == len(b"ID3audio")
    assert out.read_bytes() == b"ID3audio"
    kwargs = client.text_to_speech.convert.call_args.kwargs
    assert kwargs["voice_id"] == "voice123"
    assert kwargs["voice_settings"]["use_speaker_boost"] is True
    assert guard.spent() > 0
    assert not out.with_suffix(".mp3.part").exists()


def test_synthesize_retries_transient_errors(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("time.sleep", lambda _s: None)
    guard = BudgetGuard(tmp_path / "l.jsonl", limit_usd=5)
    client = MagicMock()
    client.text_to_speech.convert.side_effect = [ConnectionError("reset"), iter([b"ok"])]
    n = tts.synthesize(tts.TTSRequest("hola", "v"), tmp_path / "a.mp3", client=client, guard=guard)
    assert n == 2
    assert client.text_to_speech.convert.call_count == 2


def test_empty_audio_is_an_error_and_not_charged(tmp_path: Path):
    guard = BudgetGuard(tmp_path / "l.jsonl", limit_usd=5)
    get_settings().max_retries = 0
    with pytest.raises(AIVideoError, match="no audio"):
        tts.synthesize(tts.TTSRequest("hola", "v"), tmp_path / "a.mp3", client=_client(()), guard=guard)
    assert guard.spent() == 0


def test_budget_exceeded_blocks_call(tmp_path: Path):
    guard = BudgetGuard(tmp_path / "l.jsonl", limit_usd=0.0)
    client = _client()
    with pytest.raises(BudgetExceededError):
        tts.synthesize(tts.TTSRequest("hola " * 100, "v"), tmp_path / "a.mp3", client=client, guard=guard)
    client.text_to_speech.convert.assert_not_called()


def test_dry_run_never_calls_api(tmp_path: Path):
    get_settings().dry_run = True
    guard = BudgetGuard(tmp_path / "l.jsonl", limit_usd=5)
    assert tts.synthesize(tts.TTSRequest("hola", "v"), tmp_path / "a.mp3", guard=guard) == 0
    assert not (tmp_path / "a.mp3").exists()
    assert guard.spent() == 0


def test_missing_api_key_fails_fast(tmp_path: Path):
    guard = BudgetGuard(tmp_path / "l.jsonl", limit_usd=5)
    with pytest.raises(ConfigError, match="ELEVENLABS_API_KEY"):
        tts.synthesize(tts.TTSRequest("hola", "v"), tmp_path / "a.mp3", guard=guard)


def test_read_text_prefers_inline_and_errors_on_missing_file(tmp_path: Path):
    assert tts.read_text("inline", tmp_path / "missing.txt") == "inline"
    (tmp_path / "s.txt").write_text("  desde archivo \n", encoding="utf-8")
    assert tts.read_text(None, tmp_path / "s.txt") == "desde archivo"
    with pytest.raises(FileNotFoundError):
        tts.read_text(None, tmp_path / "missing.txt")
