"""spec_transitions_adapter.py — normalize SPEC transitions to canonical per-shot form.

Canonical (PRE-4.J Decision 3): shot_list[].transition_in / transition_out (per-shot embedded).
Legacy (V4 cp5-layer2-concat): top-level transitions[] array with
from_shot_id / to_shot_id / transition_type.

normalize_transitions(spec) returns a spec whose shot_list[] carries per-shot transition_out
regardless of input form. Non-destructive when conversion is needed (deep-copies); returns the
same object when already canonical or when no transitions are declared.

Reusable helper for apply-effects-between-clips.py (Paso 4.4) + future consumers (4.3/4.1).
Build PRE-4.J (2026-05-27) + companion test_spec_transitions_adapter.py (Hard Rule #26).
"""

from __future__ import annotations

import copy

# Legacy V4 transition_type → canonical recipe id (catalog filename stem).
# Covers the transition_type vocabulary observed in V4 cp5-layer2-concat.py.
LEGACY_TYPE_TO_RECIPE = {
    "cross_fade": "cross-fade-0.5s",
    "cross_fade_0.4s": "cross-fade-0.5s",
    "cross_fade_0.5s": "cross-fade-0.5s",
    "cross_fade_0.6s": "cross-fade-0.5s",
    "cross_fade_1.0s": "cross-fade-1.0s",
    "fade_in_warm": "cross-fade-0.5s",
    "hard_cut": "hard-cut-with-whoosh",
    "hard_cut_with_whoosh": "hard-cut-with-whoosh",
    "no_cut": "hard-cut-with-whoosh",
    "continuous_push_in_no_cut": "hard-cut-with-whoosh",
    "match_cut_motion": "hard-cut-with-whoosh",
    "white_flash": "light-flash-impact",
    "white_flash_to_black": "fade-to-black-1.0s",
    "fade_to_black": "fade-to-black-1.0s",
    "black_screen": "black-screen-0.3s",
    "freeze_vhs_filter": "static-noise-transition",
    "glitch": "glitch-transition",
    "film_burn": "film-burn-transition",
    "projector_cue": "projector-cue-cinema",
}


def _has_per_shot_transitions(shot_list):
    return any(
        isinstance(s, dict) and bool(s.get("transition_in") or s.get("transition_out")) for s in shot_list
    )


def normalize_transitions(spec):
    """Return spec with transitions in canonical per-shot form.

    - Already canonical (any shot has transition_in/out) → return spec as-is.
    - Legacy top-level transitions[] present → deep-copy + map each entry onto
      shot_list[from_shot_id].transition_out (transition_type → canonical recipe id).
    - Neither → return spec as-is (valid when has_layer_2_effects: false).
    """
    if not isinstance(spec, dict):
        return spec
    shot_list = spec.get("shot_list") or []
    if _has_per_shot_transitions(shot_list):
        return spec
    legacy = spec.get("transitions")
    if not legacy:
        return spec
    out = copy.deepcopy(spec)
    by_id = {s["shot_id"]: s for s in (out.get("shot_list") or []) if isinstance(s, dict) and "shot_id" in s}
    for entry in legacy:
        frm = entry.get("from_shot_id")
        ttype = entry.get("transition_type") or entry.get("transition_id")
        if frm in by_id and ttype:
            by_id[frm]["transition_out"] = LEGACY_TYPE_TO_RECIPE.get(ttype, ttype)
    return out
