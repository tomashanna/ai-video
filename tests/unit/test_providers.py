"""SFX, image, Kling and Veo providers with fully mocked SDK clients (no network)."""

from __future__ import annotations

import base64
import json
import sys
import types
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from ai_video.budget import BudgetGuard
from ai_video.config import get_settings
from ai_video.errors import BudgetExceededError, ProviderError
from ai_video.providers import image, sfx, veo3, video


@pytest.fixture
def guard(tmp_path: Path) -> BudgetGuard:
    return BudgetGuard(tmp_path / "ledger.jsonl", limit_usd=50)


@pytest.fixture
def png(tmp_path: Path) -> Path:
    p = tmp_path / "frame.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\nfake")
    return p


# -------------------------------------------------------------------------- SFX


def test_sfx_load_jobs_resolves_relative_to_spec(tmp_path: Path):
    spec = tmp_path / "proj" / "sfx-spec.json"
    spec.parent.mkdir()
    spec.write_text(
        json.dumps([{"out": "assets/sfx/a.mp3", "text": "howl", "duration": 3}]), encoding="utf-8"
    )
    jobs = sfx.load_jobs(spec)
    assert jobs[0].out == spec.parent / "assets/sfx/a.mp3"


@pytest.mark.parametrize(
    ("payload", "msg"),
    [
        ("{}", "JSON list"),
        ("[{}]", "needs 'out' and 'text'"),
        ('[{"out": "a.mp3", "text": "x", "duration": 30}]', "duration"),
        ('[{"out": "a.mp3", "text": "x", "influence": 2}]', "influence"),
        ("[nope", "invalid JSON"),
    ],
)
def test_sfx_load_jobs_rejects_bad_specs(tmp_path: Path, payload: str, msg: str):
    spec = tmp_path / "s.json"
    spec.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError, match=msg):
        sfx.load_jobs(spec)


def test_sfx_batch_continues_after_one_failure(
    tmp_path: Path, guard: BudgetGuard, monkeypatch: pytest.MonkeyPatch
):
    get_settings().max_retries = 0
    client = MagicMock()
    client.text_to_sound_effects.convert.side_effect = [RuntimeError("boom"), iter([b"mp3"])]
    jobs = [sfx.SFXJob("a", tmp_path / "a.mp3"), sfx.SFXJob("b", tmp_path / "b.mp3", duration=2, loop=True)]
    ok, failed = sfx.run_jobs(jobs, client=client, guard=guard)
    assert (ok, failed) == (1, 1)
    assert (tmp_path / "b.mp3").read_bytes() == b"mp3"
    kwargs = client.text_to_sound_effects.convert.call_args.kwargs
    assert kwargs["duration_seconds"] == 2 and kwargs["loop"] is True
    assert guard.spent() == pytest.approx(0.10)  # only the successful job is charged


def test_sfx_batch_refuses_when_budget_too_small(tmp_path: Path):
    tiny = BudgetGuard(tmp_path / "l.jsonl", limit_usd=0.15)
    client = MagicMock()
    jobs = [sfx.SFXJob(str(i), tmp_path / f"{i}.mp3") for i in range(3)]
    with pytest.raises(BudgetExceededError):
        sfx.run_jobs(jobs, client=client, guard=tiny)
    client.text_to_sound_effects.convert.assert_not_called()


# ------------------------------------------------------------------------ image


def _fake_genai_types(monkeypatch: pytest.MonkeyPatch) -> None:
    """Install a tiny stand-in for google.genai.types so tests never need the SDK."""
    t = types.ModuleType("google.genai.types")
    for name in ("Part", "Blob", "GenerateContentConfig", "ImageConfig", "Image", "GenerateVideosConfig"):
        setattr(t, name, lambda name=name, **kw: SimpleNamespace(kind=name, **kw))
    genai = types.ModuleType("google.genai")
    genai.types = t  # type: ignore[attr-defined]
    google = types.ModuleType("google")
    google.genai = genai  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "google", google)
    monkeypatch.setitem(sys.modules, "google.genai", genai)
    monkeypatch.setitem(sys.modules, "google.genai.types", t)


def _image_response(data):
    part = SimpleNamespace(inline_data=SimpleNamespace(data=data))
    return SimpleNamespace(
        candidates=[SimpleNamespace(content=SimpleNamespace(parts=[SimpleNamespace(inline_data=None), part]))]
    )


def test_extract_image_bytes_variants():
    assert image.extract_image_bytes(_image_response(b"raw")) == b"raw"
    assert image.extract_image_bytes(_image_response(base64.b64encode(b"b64").decode())) == b"b64"
    with pytest.raises(ProviderError, match="no image"):
        image.extract_image_bytes(SimpleNamespace(candidates=[]))


def test_image_generate_with_refs(
    tmp_path: Path, png: Path, guard: BudgetGuard, monkeypatch: pytest.MonkeyPatch
):
    _fake_genai_types(monkeypatch)
    client = MagicMock()
    client.models.generate_content.return_value = _image_response(b"IMG")
    out = tmp_path / "o" / "shot.png"
    n = image.generate("a corridor", out, refs=[png], client=client, guard=guard)
    assert n == 3 and out.read_bytes() == b"IMG"
    contents = client.models.generate_content.call_args.kwargs["contents"]
    assert contents[-1] == "a corridor" and contents[0].inline_data.mime_type == "image/png"
    assert guard.spent() > 0


@pytest.mark.parametrize(
    ("kwargs", "exc"),
    [
        ({"size": "8K"}, ValueError),
        ({"aspect": "2:1"}, ValueError),
        ({"refs": [Path("missing.png")]}, FileNotFoundError),
    ],
)
def test_image_validation(tmp_path: Path, kwargs, exc):
    with pytest.raises(exc):
        image.generate("x", tmp_path / "o.png", **kwargs)


def test_image_rejects_unsupported_reference(tmp_path: Path):
    gif = tmp_path / "a.gif"
    gif.write_bytes(b"GIF")
    with pytest.raises(ValueError, match="unsupported"):
        image.load_reference_images([gif])


# -------------------------------------------------------------- Kling/Replicate


def test_video_helpers(png: Path):
    assert video.image_to_data_uri(png).startswith("data:image/png;base64,")
    payload = video.build_input("kwaivgi/kling-v2.0", "uri", "move", 5, "end")
    assert payload["cfg_scale"] == 0.5 and payload["end_image"] == "end"
    assert video.rate_limit_wait_s("Request was throttled. resets in ~7s") == 9
    assert video.rate_limit_wait_s("throttled") == 12


@pytest.fixture
def fake_replicate(monkeypatch: pytest.MonkeyPatch):
    class ReplicateError(Exception):
        pass

    exc_mod = types.ModuleType("replicate.exceptions")
    exc_mod.ReplicateError = ReplicateError  # type: ignore[attr-defined]
    rep = types.ModuleType("replicate")
    rep.exceptions = exc_mod  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "replicate", rep)
    monkeypatch.setitem(sys.modules, "replicate.exceptions", exc_mod)
    return ReplicateError


def test_create_prediction_waits_on_429_then_succeeds(fake_replicate):
    client = MagicMock()
    client.predictions.create.side_effect = [fake_replicate("429 throttled, resets in ~3s"), "pred"]
    sleeps: list[float] = []
    assert video.create_prediction(client, {}, "m", sleep=sleeps.append) == "pred"
    assert sleeps == [5]


def test_create_prediction_gives_up_and_propagates_other_errors(fake_replicate):
    client = MagicMock()
    client.predictions.create.side_effect = fake_replicate("429")
    with pytest.raises(ProviderError, match="rate limited"):
        video.create_prediction(client, {}, "m", max_429=2, sleep=lambda _s: None)
    client.predictions.create.side_effect = fake_replicate("422 invalid input")
    with pytest.raises(fake_replicate):
        video.create_prediction(client, {}, "m", sleep=lambda _s: None)


def _prediction(statuses, output=None):
    pred = MagicMock()
    pred.id = "p1"
    seq = iter(statuses)

    def reload():
        pred.status = next(seq)

    pred.reload.side_effect = reload
    pred.output = output
    pred.error = "nsfw"
    return pred


def test_wait_for_prediction_success_failure_and_timeout():
    ok = _prediction(["starting", "processing", "succeeded"])
    assert video.wait_for_prediction(ok, timeout_s=60, sleep=lambda _s: None) is ok
    with pytest.raises(ProviderError, match="failed: nsfw"):
        video.wait_for_prediction(_prediction(["failed"]), timeout_s=60, sleep=lambda _s: None)
    stuck = _prediction(["processing"] * 1000)
    with pytest.raises(TimeoutError):
        video.wait_for_prediction(stuck, timeout_s=0, sleep=lambda _s: None)
    stuck.cancel.assert_called_once()


def test_download_output_requires_https():
    assert video.download_output(SimpleNamespace(read=lambda: b"mp4"), 5) == b"mp4"
    with pytest.raises(ProviderError, match="non-https"):
        video.download_output("http://insecure.example/x.mp4", 5)


def test_animate_end_to_end_with_mocks(tmp_path: Path, png: Path, guard: BudgetGuard, fake_replicate):
    client = MagicMock()
    client.predictions.create.return_value = _prediction(
        ["succeeded"], output=SimpleNamespace(read=lambda: b"MP4")
    )
    out = tmp_path / "clip.mp4"
    assert (
        video.animate(png, "push in", out, duration=10, client=client, guard=guard, sleep=lambda _s: None)
        == 3
    )
    assert out.read_bytes() == b"MP4"
    assert guard.spent() == pytest.approx(0.7)


def test_animate_retries_provider_errors_then_fails(
    tmp_path: Path, png: Path, guard: BudgetGuard, fake_replicate
):
    get_settings().max_retries = 1
    client = MagicMock()
    client.predictions.create.side_effect = lambda **_: _prediction(["failed"])
    with pytest.raises(ProviderError, match="after 2 attempts"):
        video.animate(png, "x", tmp_path / "c.mp4", client=client, guard=guard, sleep=lambda _s: None)
    assert client.predictions.create.call_count == 2
    assert guard.spent() == 0  # failed attempts are not recorded as spend


@pytest.mark.parametrize("kwargs", [{"duration": 7}, {"prompt": " "}])
def test_animate_validation(tmp_path: Path, png: Path, kwargs):
    args = {"duration": 5, "prompt": "x"} | kwargs
    with pytest.raises(ValueError):
        video.animate(png, args["prompt"], tmp_path / "c.mp4", duration=args["duration"])


# --------------------------------------------------------------------------- Veo


def test_filter_rejection_reasons():
    assert veo3.filter_rejection_reasons(None) == []
    assert veo3.filter_rejection_reasons(SimpleNamespace(rai_media_filtered_count=0)) == []
    resp = SimpleNamespace(rai_media_filtered_count=1, rai_media_filtered_reasons=["violence"])
    assert veo3.filter_rejection_reasons(resp) == ["violence"]


def _veo_client(response, done_after=2):
    client = MagicMock()
    op = SimpleNamespace(name="op1", done=False, response=None)
    states = [
        SimpleNamespace(name="op1", done=i >= done_after - 1, response=response) for i in range(done_after)
    ]
    client.models.generate_videos.return_value = op
    client.operations.get.side_effect = states
    client.files.download.return_value = b"VEO"
    return client


def test_veo_generate_happy_path(tmp_path: Path, guard: BudgetGuard, monkeypatch: pytest.MonkeyPatch):
    _fake_genai_types(monkeypatch)
    resp = SimpleNamespace(generated_videos=[SimpleNamespace(video="vid")], rai_media_filtered_count=0)
    client = _veo_client(resp)
    out = tmp_path / "v.mp4"
    meta = veo3.generate_video(
        "pov corridor", out, duration_s=8, tier="fast", client=client, guard=guard, sleep=lambda _s: None
    )
    assert out.read_bytes() == b"VEO" and meta["model"] == veo3.TIER_MODELS["fast"]
    assert guard.spent() == pytest.approx(3.2)


def test_veo_safety_rejection_raises(tmp_path: Path, guard: BudgetGuard, monkeypatch: pytest.MonkeyPatch):
    _fake_genai_types(monkeypatch)
    resp = SimpleNamespace(
        generated_videos=[], rai_media_filtered_count=1, rai_media_filtered_reasons=["minor"]
    )
    with pytest.raises(ProviderError, match="safety filter"):
        veo3.generate_video(
            "x", tmp_path / "v.mp4", client=_veo_client(resp), guard=guard, sleep=lambda _s: None
        )


@pytest.mark.parametrize(
    "kwargs",
    [{"tier": "ultra"}, {"aspect_ratio": "1:1"}, {"duration_s": 5}, {"image_ref_path": Path("nope.png")}],
)
def test_veo_validation(tmp_path: Path, kwargs):
    with pytest.raises((ValueError, FileNotFoundError)):
        veo3.generate_video("x", tmp_path / "v.mp4", **kwargs)


def test_veo_dry_run_estimates_without_client(tmp_path: Path, guard: BudgetGuard):
    get_settings().dry_run = True
    meta = veo3.generate_video("x", tmp_path / "v.mp4", duration_s=6, guard=guard)
    assert meta["dry_run"] is True and meta["estimated_usd"] == pytest.approx(2.4)
    assert guard.spent() == 0
