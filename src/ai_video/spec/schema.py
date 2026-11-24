"""Pydantic schema for creative specs (schema v11.x).

The spec is the contract between the *architect* (who designs the video) and the
*engineer* (who renders it). This schema validates the structural core every tool relies
on — project identity, capability flags, shot list and narration script — while allowing
the many optional, format-specific blocks (``extra="allow"``) so it never blocks creative
iteration.

Validation layers:

* **Types / ranges** — durations > 0, fps in a known set, ``WxH`` resolutions, ordered
  ``[start, end]`` timestamps, ``[lo, hi]`` bands with ``lo <= hi``.
* **Cross-references** — unique shot ids; every narration segment anchors to an existing shot.
* **Soft checks** (warnings, not errors) — shot durations vs. declared duration, narration
  past the end of the video, overlapping voices.
"""

from __future__ import annotations

import re
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOLUTION = re.compile(r"^(\d{3,4})x(\d{3,4})$")
SCHEMA_VERSION = re.compile(r"^v11(\.\d+)*$")
ALLOWED_FPS = (24, 25, 30, 50, 60)

PositiveSeconds = Annotated[float, Field(gt=0, le=3600)]


class _Open(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class Project(_Open):
    project_id: str
    format: str = Field(min_length=1)
    delivery: str = Field(min_length=1)
    total_duration_s_intent: PositiveSeconds | None = None
    language: str | None = None

    @field_validator("project_id")
    @classmethod
    def _kebab(cls, v: str) -> str:
        if not KEBAB.match(v) and not v.startswith("<"):
            raise ValueError(f"project_id must be kebab-case, got {v!r}")
        return v


class VideoCapabilities(_Open):
    source_clips_origin: Literal["ai_generated", "pre_existing", "mixed"]
    has_ai_generated_clips: bool
    has_tts_narration: bool
    has_human_voiceover: bool = False
    has_sfx_layer: bool = False
    has_captions_baked: bool = False
    has_layer_2_effects: bool = False
    has_layer_3_music: bool = False
    has_layer_4_ui: bool = False
    audio_mix_target: str | None = None
    format_type: str = Field(min_length=1)
    duration_intent_s: PositiveSeconds
    target_fps: int = 30
    output_resolution: str = "1080x1920"

    @field_validator("target_fps")
    @classmethod
    def _fps(cls, v: int) -> int:
        if v not in ALLOWED_FPS:
            raise ValueError(f"target_fps must be one of {ALLOWED_FPS}, got {v}")
        return v

    @field_validator("output_resolution")
    @classmethod
    def _res(cls, v: str) -> str:
        if not RESOLUTION.match(v):
            raise ValueError(f"output_resolution must look like 1080x1920, got {v!r}")
        return v

    @model_validator(mode="after")
    def _origin_consistency(self) -> VideoCapabilities:
        if self.source_clips_origin == "pre_existing" and self.has_ai_generated_clips:
            raise ValueError("source_clips_origin=pre_existing contradicts has_ai_generated_clips=true")
        return self

    @property
    def size(self) -> tuple[int, int]:
        m = RESOLUTION.match(self.output_resolution)
        assert m is not None
        return int(m.group(1)), int(m.group(2))


class Band(BaseModel):
    """A ``[lo, hi]`` numeric band."""

    lo: float
    hi: float

    @model_validator(mode="before")
    @classmethod
    def _from_list(cls, v: Any) -> Any:
        if isinstance(v, (list, tuple)):
            if len(v) != 2:
                raise ValueError("band must be [lo, hi]")
            return {"lo": v[0], "hi": v[1]}
        return v

    @model_validator(mode="after")
    def _ordered(self) -> Band:
        if self.lo > self.hi:
            raise ValueError(f"band lower bound {self.lo} > upper bound {self.hi}")
        return self


class EditingTargets(_Open):
    target_cuts_per_min: Band | None = None
    target_total_cuts: Band | None = None
    transition_variety_min: int | None = Field(default=None, ge=0)


class Shot(_Open):
    shot_id: str = Field(min_length=1)
    section_id: str | None = None
    description: str | None = None
    duration_intent_s: PositiveSeconds
    ui_active: list[Any] | dict[str, Any] | None = None


class NarrationSegment(_Open):
    segment_id: str = Field(min_length=1)
    speaker: str = Field(min_length=1)
    voice_id: str | None = None
    text_canonical: str = Field(min_length=1)
    timestamp_intent_s: tuple[float, float]
    shot_id_anchor: str | None = None
    lip_sync_required: bool = False

    @field_validator("timestamp_intent_s")
    @classmethod
    def _ordered(cls, v: tuple[float, float]) -> tuple[float, float]:
        start, end = v
        if start < 0 or end <= start:
            raise ValueError(f"timestamp_intent_s must be [start, end] with 0 <= start < end, got {list(v)}")
        return v

    @property
    def duration_s(self) -> float:
        return self.timestamp_intent_s[1] - self.timestamp_intent_s[0]


class CreativeSpec(_Open):
    schema_version: str
    project: Project
    video_capabilities: VideoCapabilities
    shot_list: list[Shot] = Field(min_length=1)
    narration_script: list[NarrationSegment] = Field(default_factory=list)
    editing_targets: EditingTargets | None = None
    narrator_voice: str | None = None

    @field_validator("schema_version")
    @classmethod
    def _version(cls, v: str) -> str:
        if not SCHEMA_VERSION.match(str(v)):
            raise ValueError(f"unsupported schema_version {v!r} (expected v11.x)")
        return v

    @model_validator(mode="after")
    def _cross_refs(self) -> CreativeSpec:
        ids = [s.shot_id for s in self.shot_list]
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        if dupes:
            raise ValueError(f"duplicate shot_id(s): {dupes}")
        known = set(ids)
        orphans = [n.segment_id for n in self.narration_script if n.shot_id_anchor and n.shot_id_anchor not in known]
        if orphans:
            raise ValueError(f"narration segments anchored to unknown shots: {orphans}")
        seg_ids = [n.segment_id for n in self.narration_script]
        seg_dupes = sorted({i for i in seg_ids if seg_ids.count(i) > 1})
        if seg_dupes:
            raise ValueError(f"duplicate narration segment_id(s): {seg_dupes}")
        return self

    # ------------------------------------------------------------- soft checks
    def warnings(self, *, duration_tolerance: float = 0.30, voice_buffer_s: float = 0.0) -> list[str]:
        out: list[str] = []
        intent = self.video_capabilities.duration_intent_s
        total = sum(s.duration_intent_s for s in self.shot_list)
        if abs(total - intent) / intent > duration_tolerance:
            out.append(
                f"shot durations sum to {total:.1f}s vs duration_intent_s {intent:.0f}s "
                f"(>{duration_tolerance:.0%} off)"
            )
        horizon = max(intent, total)
        late = [n.segment_id for n in self.narration_script if n.timestamp_intent_s[1] > horizon + 0.5]
        if late:
            out.append(f"narration ends after the video ({horizon:.1f}s): {late}")
        segs = sorted(self.narration_script, key=lambda n: n.timestamp_intent_s[0])
        for a, b in zip(segs, segs[1:]):
            if a.speaker != b.speaker and b.timestamp_intent_s[0] < a.timestamp_intent_s[1] + voice_buffer_s:
                out.append(
                    f"voices overlap: {a.segment_id} ({a.speaker}) and {b.segment_id} ({b.speaker}) "
                    f"at {b.timestamp_intent_s[0]:.2f}s"
                )
        return out
