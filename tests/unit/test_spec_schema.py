"""Creative-spec schema: real examples validate; each structural defect is caught with a clear path."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from ai_video import paths
from ai_video.errors import SpecValidationError
from ai_video.spec import validate as V
from ai_video.spec.schema import CreativeSpec

EXAMPLES = sorted(paths.example_specs_dir().glob("*.yaml"))


def minimal() -> dict:
    return {
        "schema_version": "v11.2",
        "project": {"project_id": "demo-video", "format": "horror-choice", "delivery": "reel"},
        "video_capabilities": {
            "source_clips_origin": "ai_generated",
            "has_ai_generated_clips": True,
            "has_tts_narration": True,
            "format_type": "interactive_choice",
            "duration_intent_s": 10,
            "target_fps": 30,
            "output_resolution": "1080x1920",
        },
        "shot_list": [
            {"shot_id": "shot_01", "duration_intent_s": 5},
            {"shot_id": "shot_02", "duration_intent_s": 5},
        ],
        "narration_script": [
            {
                "segment_id": "n1",
                "speaker": "narrator",
                "text_canonical": "Elige.",
                "timestamp_intent_s": [0.5, 2.0],
                "shot_id_anchor": "shot_01",
            },
        ],
        "editing_targets": {"target_cuts_per_min": [18, 22]},
        "format_specific_block": {"anything": ["is", "allowed"]},
    }


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.stem)
def test_examples_are_valid(path: Path):
    report = V.validate_file(path)
    assert report.valid, report.errors


def test_examples_exist():
    assert len(EXAMPLES) >= 3


def test_minimal_spec_valid_and_extra_blocks_preserved():
    spec = CreativeSpec.model_validate(minimal())
    assert spec.video_capabilities.size == (1080, 1920)
    assert spec.model_extra and "format_specific_block" in spec.model_extra
    assert spec.warnings() == []


def _errors(data: dict) -> list[str]:
    with pytest.raises(SpecValidationError) as ei:
        V.parse_spec(data)
    return ei.value.errors


@pytest.mark.parametrize(
    ("mutate", "needle"),
    [
        (lambda d: d.update(schema_version="v10"), "schema_version"),
        (lambda d: d["project"].update(project_id="Bad Id"), "kebab-case"),
        (lambda d: d["video_capabilities"].update(target_fps=29), "target_fps"),
        (lambda d: d["video_capabilities"].update(output_resolution="vertical"), "output_resolution"),
        (lambda d: d["video_capabilities"].update(duration_intent_s=0), "duration_intent_s"),
        (lambda d: d["video_capabilities"].update(source_clips_origin="pre_existing"), "contradicts"),
        (lambda d: d["shot_list"].clear(), "shot_list"),
        (
            lambda d: d["shot_list"].append({"shot_id": "shot_01", "duration_intent_s": 2}),
            "duplicate shot_id",
        ),
        (lambda d: d["shot_list"][0].update(duration_intent_s=-1), "duration_intent_s"),
        (lambda d: d["narration_script"][0].update(timestamp_intent_s=[3, 1]), "timestamp_intent_s"),
        (lambda d: d["narration_script"][0].update(shot_id_anchor="shot_99"), "unknown shots"),
        (lambda d: d["narration_script"][0].update(text_canonical=""), "text_canonical"),
        (lambda d: d["editing_targets"].update(target_cuts_per_min=[22, 18]), "lower bound"),
        (lambda d: d.pop("video_capabilities"), "video_capabilities"),
    ],
)
def test_structural_defects_are_reported(mutate, needle):
    data = copy.deepcopy(minimal())
    mutate(data)
    errors = _errors(data)
    assert any(needle in e for e in errors), errors


def test_soft_warnings_duration_late_narration_and_voice_overlap():
    d = minimal()
    d["shot_list"][0]["duration_intent_s"] = 40
    d["narration_script"] += [
        {"segment_id": "c1", "speaker": "char_a", "text_canonical": "Ven.", "timestamp_intent_s": [1.5, 3.0]},
        {"segment_id": "n2", "speaker": "narrator", "text_canonical": "Fin.", "timestamp_intent_s": [60, 62]},
    ]
    w = CreativeSpec.model_validate(d).warnings()
    assert any("shot durations sum" in x for x in w)
    assert any("voices overlap" in x and "c1" in x for x in w)
    assert any("after the video" in x for x in w)


def test_load_yaml_guards(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    lst = tmp_path / "list.yaml"
    lst.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(SpecValidationError, match="mapping"):
        V.load_yaml(lst)
    bad = tmp_path / "bad.yaml"
    bad.write_text("a: [unclosed\n", encoding="utf-8")
    with pytest.raises(SpecValidationError, match="invalid YAML"):
        V.load_yaml(bad)
    evil = tmp_path / "evil.yaml"
    evil.write_text("a: !!python/object/apply:os.system ['echo pwned']\n", encoding="utf-8")
    with pytest.raises(SpecValidationError):
        V.load_yaml(evil)  # safe_load refuses arbitrary object construction
    monkeypatch.setattr(V, "MAX_SPEC_BYTES", 10)
    big = tmp_path / "big.yaml"
    big.write_text("a: " + "x" * 100, encoding="utf-8")
    with pytest.raises(SpecValidationError, match="limit"):
        V.load_yaml(big)
    with pytest.raises(SpecValidationError, match="cannot read"):
        V.load_yaml(tmp_path / "missing.yaml")


def test_cli_exit_codes_and_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
):
    good = tmp_path / "good.yaml"
    good.write_text(yaml.safe_dump(minimal()), encoding="utf-8")
    d = minimal()
    d["shot_list"][0]["duration_intent_s"] = 40
    warn = tmp_path / "warn.yaml"
    warn.write_text(yaml.safe_dump(d), encoding="utf-8")

    def run(*args: str) -> int:
        monkeypatch.setattr("sys.argv", ["validate-spec", *args])
        return V.main()

    assert run(str(good)) == 0
    assert run(str(warn)) == 0
    assert run(str(warn), "--strict") == 1
    capsys.readouterr()
    assert run(str(good), "--json") == 0
    assert '"valid": true' in capsys.readouterr().out
    assert run("--print-json-schema") == 0
    schema = capsys.readouterr().out
    assert '"shot_list"' in schema and '"video_capabilities"' in schema
