#!/usr/bin/env python3
"""
audit-gemini-calibrated.py — Tomás-calibrated Gemini Vision scoring

Runs Gemini Vision against a video with a TOMÁS-CALIBRATED prompt template
(genre-aware POV/liminal-spaces horror-choice rubric with 11-datapoint
few-shot calibration). Outputs both dimensional scores + weighted total.

WHY: generic Gemini holistic INVERTS sign by genre — over-scores own
productions (~+1.33) and under-scores canonical refs (~-2.73). Calibrated
prompt narrows the gap by encoding Tomás's taste empirically.

OUTPUT: parallel to existing audit-frames.py / analyze_video.py — generates
gemini_calibrated_score + gemini_calibrated_dimensions + delta_vs_generic.

USAGE:
    python audit-gemini-calibrated.py <video.mp4> [--output <out.json>]

OUTPUTS:
    stdout: human-readable score breakdown
    --output: JSON with 8 dimensions + weighted_score + raw_response

ENV:
    GEMINI_API_KEY — required.

PROMPT TEMPLATE LOCATION:
    Looked up in this priority:
    1. $GEMINI_CALIBRATED_PROMPT_PATH env var
    2. .claude/skills/ai-video-production/templates/calibrated-gemini-prompt-v2.txt
    3. /tmp/calibrated_prompt_v2.txt (test path fallback)

WEIGHTED SCORE FORMULA (v4 — EXECUTION CONTINUITY as primary dimension):
    0.30 × execution_continuity (⭐⭐ NEW primary, was missing in v2)
    + 0.15 × inmersion_pov
    + 0.15 × sound_depth
    + 0.10 × atmosphere_coherence
    + 0.10 × character_signature
    + 0.05 × story_logic_continuity
    + 0.05 × editing_modulation
    + 0.05 × hook_retention
    + 0.03 × captions
    + 0.02 × narrative_comprehension

DIMENSIONS DEFINED IN CALIBRATED PROMPT — single source of truth there.

COST: ~$0.10-0.15 per video (Gemini Vision Files API).

VALIDATION:
- v2 mean abs delta 0.227 across 11-datapoint calibration set 2026-05-21
- v4 with EXECUTION CONTINUITY dimension: mean abs delta 0.14 across 5 critical
  test videos (matadero+cinema+Ref-A+Ref-1+Ref-3) — 38% improvement over v2.
- v4 successfully detects teleport-cut pattern in matadero (4.8/10 exec dim)
  vs v2 missed entirely (scored 9.9 inflated).

NEVER hardcoded canonical data here — always read from the prompt template
that gets versioned + iterated externally.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from google import genai  # noqa: F401  (availability check)
    from google.genai import types  # noqa: F401  (availability check)
except ImportError:
    print("ERROR: pip install google-genai", file=sys.stderr)
    sys.exit(1)


# Tomás-calibrated weights v4 (must match prompt template v4)
WEIGHTS = {
    "execution_continuity": 0.30,  # ⭐⭐ NEW primary
    "inmersion_pov": 0.15,
    "sound_depth": 0.15,
    "atmosphere_coherence": 0.10,
    "character_signature": 0.10,
    "story_logic_continuity": 0.05,
    "editing_modulation": 0.05,
    "hook_retention": 0.05,
    "captions": 0.03,
    "narrative_comprehension": 0.02,
}

# Dimensional regex v4 (matches v4 prompt output format)
DIM_PATTERNS = [
    ("execution_continuity", r"1\.\s+EXECUTION CONTINUITY[^:]*:\s*(\d+\.?\d*)"),
    ("inmersion_pov", r"2\.\s+(?:INMERSIÓN POV|INMERSION POV)[^:]*:\s*(\d+\.?\d*)"),
    ("sound_depth", r"3\.\s+SOUND DEPTH[^:]*:\s*(\d+\.?\d*)"),
    ("atmosphere_coherence", r"4\.\s+ATMOSPHERE[^:]*:\s*(\d+\.?\d*)"),
    ("character_signature", r"5\.\s+CHARACTER[^:]*:\s*(\d+\.?\d*)"),
    ("story_logic_continuity", r"6\.\s+STORY LOGIC[^:]*:\s*(\d+\.?\d*)"),
    ("editing_modulation", r"7\.\s+EDITING[^:]*:\s*(\d+\.?\d*)"),
    ("hook_retention", r"8\.\s+HOOK[^:]*:\s*(\d+\.?\d*)"),
    ("captions", r"9\.\s+CAPTIONS[^:]*:\s*(\d+\.?\d*)"),
    ("narrative_comprehension", r"10\.\s+NARRATIVE[^:]*:\s*(\d+\.?\d*)"),
]


def find_prompt_template() -> Path:
    """Look for calibrated prompt in priority order (v4 latest, v2 symlinks to v4)."""
    override = os.environ.get("GEMINI_CALIBRATED_PROMPT_PATH")
    if override:
        p = Path(override)
        if not p.is_file():
            raise FileNotFoundError(f"GEMINI_CALIBRATED_PROMPT_PATH={override} does not exist")
        return p
    from ai_video.paths import prompt_path

    return prompt_path("calibrated-gemini-prompt-v4.txt")


def parse_response(text: str) -> dict:
    """Extract 8 dimensional scores + weighted score + verdict from Gemini response."""
    dims = {}
    for name, pattern in DIM_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            dims[name] = float(m.group(1))

    # Compute weighted score from dimensions (don't trust Gemini's own arithmetic)
    if len(dims) == 8:
        weighted_computed = sum(dims[k] * WEIGHTS[k] for k in WEIGHTS)
    else:
        weighted_computed = None

    # Also extract Gemini's reported WEIGHTED SCORE (cross-check)
    m_weighted = re.search(r"WEIGHTED SCORE[:\s]+(\d+\.?\d*)", text)
    weighted_reported = float(m_weighted.group(1)) if m_weighted else None

    # Confidence
    m_conf = re.search(r"CONFIDENCE[:\s]+(high|medium|low)", text, re.IGNORECASE)
    confidence = m_conf.group(1).lower() if m_conf else "unknown"

    # Verdict line
    m_verdict = re.search(r"VERDICT[:\s]+(.+?)(?:\n|$)", text)
    verdict = m_verdict.group(1).strip() if m_verdict else None

    return {
        "dimensions": dims,
        "weighted_score_computed": weighted_computed,
        "weighted_score_reported": weighted_reported,
        "confidence": confidence,
        "verdict": verdict,
        "dimensions_complete": len(dims) == 8,
    }


def analyze(video_path: Path, prompt: str) -> str:
    """Run Gemini Vision via Files API + return raw text response."""
    from ai_video.providers.clients import gemini_client

    client = gemini_client()

    size_mb = video_path.stat().st_size / 1e6
    print(f"[info] Uploading {video_path.name} ({size_mb:.1f} MB)...", file=sys.stderr)
    uploaded = client.files.upload(file=str(video_path))

    # Wait for processing
    from ai_video.config import get_settings
    from ai_video.retry import poll_until

    def _ready():
        nonlocal uploaded
        uploaded = client.files.get(name=uploaded.name)
        return None if uploaded.state.name == "PROCESSING" else uploaded

    if uploaded.state.name == "PROCESSING":
        uploaded = poll_until(
            _ready, timeout_s=get_settings().poll_timeout_s, interval_s=3, describe="Gemini file processing"
        )

    if uploaded.state.name == "FAILED":
        raise RuntimeError(f"File processing failed: {uploaded.state}")

    print("[info] Running calibrated analysis...", file=sys.stderr)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[uploaded, prompt],
    )
    return response.text


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("video", type=Path, help="Path to video MP4")
    parser.add_argument("--output", type=Path, help="Write JSON output here")
    parser.add_argument("--prompt-path", type=Path, help="Override calibrated prompt path")
    args = parser.parse_args()

    from ai_video.config import get_settings

    get_settings().require("gemini_api_key")  # fail fast before uploading anything

    prompt_path = args.prompt_path or find_prompt_template()
    prompt = prompt_path.read_text()
    print(f"[info] Using prompt: {prompt_path}", file=sys.stderr)

    raw_response = analyze(args.video, prompt)
    parsed = parse_response(raw_response)

    # Human-readable stdout
    print(f"\n═══ Tomás-calibrated Gemini score: {args.video.name} ═══\n")
    if parsed["dimensions_complete"]:
        for name, score in parsed["dimensions"].items():
            weight = WEIGHTS[name]
            print(f"  {name:30s} {score:>5.1f} / 10  (weight {weight:.2f})")
        print(f"\n  WEIGHTED SCORE (computed)  {parsed['weighted_score_computed']:>5.2f} / 10")
        if parsed['weighted_score_reported']:
            print(f"  WEIGHTED SCORE (Gemini said): {parsed['weighted_score_reported']:>5.2f}")
        print(f"  CONFIDENCE: {parsed['confidence']}")
        if parsed['verdict']:
            print(f"  VERDICT: {parsed['verdict']}")
    else:
        print(f"  ⚠️  Could not parse all 8 dimensions ({len(parsed['dimensions'])}/8)")
        print("  Raw response saved for inspection.")

    if args.output:
        output_data = {
            "video": str(args.video),
            "prompt_path": str(prompt_path),
            **parsed,
            "raw_response": raw_response,
        }
        args.output.write_text(json.dumps(output_data, indent=2))
        print(f"\n  → Full output: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
