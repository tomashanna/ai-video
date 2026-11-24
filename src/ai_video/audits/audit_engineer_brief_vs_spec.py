#!/usr/bin/env python3
"""audit-engineer-brief-vs-spec.py — Gap #47 anti-recurrence validator.

PURPOSE: the contract handed to the engineer is the SPEC, NOT the brief. When the
orchestrator/auditor spawns the engineer for a shot/CP, it sometimes writes a prose
"brief" that PARAPHRASES or COMPRESSES the SPEC's canonical `visual_intent` instead of
passing the literal text → the engineer executes a DRIFTED version of the SPEC.

Triggering history (Gap #47, 2 recurrences):
  - V7 shot_03b: the brief confused the shot ("Dario baja al andén parte 2" instead of
    the SPEC's "POV mira atrás: reja se cierra sellando la salida").
  - V4 shot_16: same class of brief-vs-SPEC compression drift.

This validator receives the brief text that is about to be passed to the engineer + the
SPEC + the shot_id, and verifies that the brief does NOT contradict/compress the canonical
field of the SPEC for that shot.

Checks (per shot):
  1. PRESENCE  — the canonical field text appears VERBATIM in the brief (substring match,
     whitespace+case normalized). Missing → FAIL (paraphrase/compression detected, Gap #47).
  2. NO-CONTRADICTION — key tokens of the canonical text (words ≥4 chars, minus ES stopwords)
     are present in the brief ≥ coverage threshold (default 0.8). Below → FAIL + missing tokens.
  3. SCOPE — if --shot-id is not in the SPEC → exit 2 (usage error).

Capability-aware: NOT applicable here. This is a STRUCTURAL cross-format process guard
(brief→engineer handoff fidelity) — it runs ALWAYS, independent of video_capabilities.

Exit 0 PASS / 1 FAIL (drift) / 2 usage error. JSON report on stdout.

Hard Rule #26 companion test: test_audit-engineer-brief-vs-spec.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

# Spanish stopwords (≥4 chars or short connectors) — pruned so they don't count as
# "key tokens" for the no-contradiction coverage heuristic.
ES_STOPWORDS = {
    "para",
    "pero",
    "porque",
    "como",
    "cuando",
    "donde",
    "hacia",
    "hasta",
    "desde",
    "sobre",
    "entre",
    "este",
    "esta",
    "esto",
    "esos",
    "esas",
    "eso",
    "esa",
    "ese",
    "unos",
    "unas",
    "una",
    "uno",
    "los",
    "las",
    "del",
    "con",
    "por",
    "que",
    "sus",
    "sin",
    "más",
    "muy",
    "ya",
    "le",
    "lo",
    "la",
    "el",
    "un",
    "su",
    "se",
    "y",
    "o",
    "a",
    "de",
    "en",
    "es",
    "al",
    "mientras",
    "luego",
    "tras",
    "cada",
}

DEFAULT_COVERAGE_THRESHOLD = 0.8


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def normalize(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace — for substring presence match."""
    text = _strip_accents(text.lower())
    return re.sub(r"\s+", " ", text).strip()


def key_tokens(text: str) -> list[str]:
    """Content words: ≥4 chars (accent-stripped, lowercased), not ES stopwords."""
    norm = normalize(text)
    words = re.findall(r"[a-z0-9]+", norm)
    out = []
    for w in words:
        if len(w) >= 4 and w not in ES_STOPWORDS:
            out.append(w)
    return out


def load_shot(spec: dict, shot_id: str):
    """Return the shot dict for shot_id, or None if not found.

    shot_list is the v11 canonical container; falls back to 'shots' for synthetic fixtures.
    """
    shots = spec.get("shot_list")
    if shots is None:
        shots = spec.get("shots") or []
    for s in shots:
        if isinstance(s, dict) and s.get("shot_id") == shot_id:
            return s
    return None


def all_shot_ids(spec: dict) -> list[str]:
    shots = spec.get("shot_list") or spec.get("shots") or []
    return [s.get("shot_id") for s in shots if isinstance(s, dict) and s.get("shot_id")]


def check_one(canonical_text: str, brief_text: str, field: str, shot_id: str, threshold: float) -> dict:
    """Run presence + no-contradiction checks for a single shot brief."""
    canonical_text = (canonical_text or "").strip()
    brief_norm = normalize(brief_text)
    canon_norm = normalize(canonical_text)

    # Check 1 — PRESENCE (verbatim substring, normalized).
    verbatim_present = bool(canon_norm) and canon_norm in brief_norm

    # Check 2 — NO-CONTRADICTION (key token coverage).
    canon_tokens = key_tokens(canonical_text)
    brief_token_set = set(key_tokens(brief_text))
    if canon_tokens:
        present = [t for t in canon_tokens if t in brief_token_set]
        missing = [t for t in canon_tokens if t not in brief_token_set]
        coverage = len(present) / len(canon_tokens)
    else:
        present, missing, coverage = [], [], 1.0

    coverage_ok = coverage >= threshold

    failures = []
    if not verbatim_present:
        failures.append(f"brief no contiene el {field} literal (paráfrasis/compresión detectada — Gap #47)")
    if not coverage_ok:
        failures.append(
            f"token coverage {coverage:.2f} < umbral {threshold:.2f} — el brief omite/altera "
            f"contenido canónico (posible contradicción/drift). missing: {sorted(set(missing))}"
        )

    return {
        "shot_id": shot_id,
        "field": field,
        "status": "pass" if not failures else "fail",
        "verbatim_present": verbatim_present,
        "token_coverage": round(coverage, 4),
        "coverage_threshold": threshold,
        "canonical_token_count": len(canon_tokens),
        "missing_tokens": sorted(set(missing)),
        "canonical_field_text": canonical_text,
        "failures": failures,
    }


def resolve_brief(brief_arg: str) -> str:
    """A brief value of '@path' loads file contents; otherwise it's literal text."""
    if brief_arg.startswith("@"):
        p = Path(brief_arg[1:])
        if not p.exists():
            raise FileNotFoundError(f"brief file not found: {p}")
        return p.read_text(encoding="utf-8")
    return brief_arg


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--spec", required=True, help="SPEC yaml path")
    parser.add_argument("--shot-id", help="single shot to validate")
    parser.add_argument("--brief", help="brief text, or @file to load from disk (single-shot mode)")
    parser.add_argument(
        "--field",
        default="visual_intent",
        help="canonical SPEC field to validate against (default visual_intent)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_COVERAGE_THRESHOLD,
        help=f"min key-token coverage (default {DEFAULT_COVERAGE_THRESHOLD})",
    )
    parser.add_argument(
        "--all-shots",
        action="store_true",
        help="validate a set of briefs from --briefs-json (map shot_id→brief)",
    )
    parser.add_argument("--briefs-json", help="JSON file: {shot_id: brief_text, ...} for --all-shots")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    field = args.field

    # ---- ALL-SHOTS mode -----------------------------------------------------
    if args.all_shots:
        if not args.briefs_json:
            print("ERROR: --all-shots requires --briefs-json", file=sys.stderr)
            return 2
        bj_path = Path(args.briefs_json)
        if not bj_path.exists():
            print(f"ERROR: briefs-json not found: {bj_path}", file=sys.stderr)
            return 2
        briefs = json.loads(bj_path.read_text(encoding="utf-8"))
        if not isinstance(briefs, dict):
            print("ERROR: briefs-json must be a JSON object {shot_id: brief}", file=sys.stderr)
            return 2

        results = []
        unknown = []
        for sid, brief_text in briefs.items():
            shot = load_shot(spec, sid)
            if shot is None:
                unknown.append(sid)
                continue
            results.append(check_one(shot.get(field), str(brief_text), field, sid, args.threshold))
        if unknown:
            print(f"ERROR: shot_id(s) not in SPEC: {unknown}", file=sys.stderr)
            return 2

        fails = [r for r in results if r["status"] == "fail"]
        report = {
            "spec": str(spec_path),
            "field": field,
            "mode": "all_shots",
            "overall_status": "fail" if fails else "pass",
            "overall_pass": not fails,
            "total_checked": len(results),
            "fail_count": len(fails),
            "results": results,
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1 if fails else 0

    # ---- SINGLE-SHOT mode ---------------------------------------------------
    if not args.shot_id or args.brief is None:
        print(
            "ERROR: single-shot mode requires --shot-id and --brief (or use --all-shots --briefs-json)",
            file=sys.stderr,
        )
        return 2

    shot = load_shot(spec, args.shot_id)
    if shot is None:
        print(
            f"ERROR: shot_id '{args.shot_id}' not found in SPEC. available: {all_shot_ids(spec)}",
            file=sys.stderr,
        )
        return 2

    try:
        brief_text = resolve_brief(args.brief)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    result = check_one(shot.get(field), brief_text, field, args.shot_id, args.threshold)
    report = {
        "spec": str(spec_path),
        "field": field,
        "mode": "single_shot",
        "overall_status": result["status"],
        "overall_pass": result["status"] == "pass",
        **result,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
