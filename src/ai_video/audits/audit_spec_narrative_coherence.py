#!/usr/bin/env python3
"""
audit-spec-narrative-coherence.py — BUILD 4 PRE-4.J narrative-coherence validator.

Closes the V4 "no 100%" gap: V5 SPEC narrative quality is verified programmatically pre-emit,
separating STRUCTURE (template adherence, validated vs canonical) from CONTENT (cross-video
novelty, validated vs prior video-log + anti-cliché). Subjective taste residual = human.

Capability-aware (Pattern 7): only horror-choice format_type interactive_choice triggers
narrative checks; other format_types → not_applicable. video_capabilities missing → Bug #9.

Checks (per-gate pass | fail | flag | not_applicable):
  STRUCTURE
    1. cliffhanger_archetype ∈ {P1, P2, P3, P6, P9} canonical (post GAP #10)
    2. hook_sub_beats ends with "countdown" (canonical last beat)
    3. dilema_placement_pct ∈ [10, 30] canonical band
    4. counterfactual_placement != retrospective (PAUTA § 24 anti-pattern)
    5. "Si [acción condicional]" framing in every consequence shot (D19 corrected to PRIMARY
       SOURCE: action-conditional dominant 6/8 @referent-a ["Si la enciendes",
       "Si te niegas"] + choice-reference variant 2/8 @referent-b ["Si decides",
       "Si escogiste X"]; bare label "Si elegiste A/B" = 0/8 synthetic anti-pattern)
    6. WPM per beat_role within canonical band (per-role lookup, fallback default [110, 220])
  CROSS-VIDEO UNIQUENESS (parses video-log markdown)
    7. location exact-match vs prior rows → FAIL
    8. signature_staging semantic similarity (paraphrase-multilingual-MiniLM-L12-v2):
       ≥ block_threshold (0.85 default) → FAIL · [flag_threshold, block) → FLAG · else PASS
    9. pattern rotation HR#14: V5 cliffhanger_archetype != last video's pattern
  ANTI-CLICHÉ
    10. Forbidden phrases (default list per feedback_anti_cliche_horror, override --anti-cliche-file)

Cross-video skips: verbs (catálogo válido del formato) + characters (repetibles).

Library: sentence-transformers + paraphrase-multilingual-MiniLM-L12-v2 (~470 MB, local $0).
Lazy-loaded: model only loaded when signature_staging check actually runs (CLI / structure /
anti-cliche tests don't trigger the load). --skip-semantic skips the model entirely.

Build PRE-4.J BUILD 4 (2026-05-27) — TDD + Hard Rule #26 companion test.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

CANONICAL_PATTERNS = {"P1", "P2", "P3", "P6", "P9"}  # PAUTA-MASTER post GAP #10
WPM_BANDS = {
    "hook": (150, 220),
    "hook_framing": (150, 220),
    "setup": (100, 200),
    "setup_establishing": (100, 200),
    "decision_setup": (140, 220),
    "decision_question": (130, 220),
    "consequence": (110, 220),
    "consequence_A": (110, 220),
    "consequence_B": (110, 220),
    "consequence_narration": (110, 220),
    "cliffhanger": (70, 180),
}
WPM_DEFAULT_BAND = (110, 220)
DILEMA_PLACEMENT_BAND_PCT = (10, 30)

DEFAULT_ANTI_CLICHE = [
    "te conviertes en cena",
    "cena que nunca acaba",
    "bucle eterno",
    "nunca encuentras la salida",
]

# Consequence framing — re-extracted from PRIMARY SOURCE (Whisper transcripts of the 8 canonical
# virals: referent-analysis/horror-choice/ref-{03,06,08,09,10,11,12,13}/transcription.json).
# DOMINANT (6/8 @referent-a): "Si [acción condicional]" = "Si" + optional clitics +
#   a 2nd-person present/preterite verb describing the action taken
#   ("Si la enciendes", "Si esperas", "Si te niegas", "Si los sigues", "Si la abres").
# VARIANT (2/8 @referent-b): choice-reference ("Si decides...", "Si escogiste/escoges X",
#   "Si tomaste...") — also a 2nd-person verb, accepted by the same regex.
# ANTI-PATTERN (0/8 — pure synthesis, NEVER in primary source): bare label "Si elegiste A" /
#   "Si elegiste opción B". This is what the deprecated "Si elegiste X" rule (D19 synthesis)
#   wrongly required; enforcing it produces robotic guiones and FAILs the canonical action form.
# NOTE: "Si elegiste a Víctor" (preposition "a" + name, ref-09 branch setup) is NOT the anti-pattern
#   — the synthetic regex is case-sensitive on the [ABC] label so a lowercase "a" never matches.
ACTION_CONDITIONAL_RE = re.compile(
    r"\bsi\s+(?:(?:no|ya)\s+)?(?:(?:te|lo|la|le|los|las|me|se|nos)\s+)*"
    r"[a-záéíóúñ]+(?:as|es|ás|és|aste|iste)\b",
    re.IGNORECASE,
)
SYNTHETIC_LABEL_RE = re.compile(
    r"(?i:\bsi\s+(?:elegiste|escogiste|eliges|escoges)\s+(?:la\s+)?(?:opci[oó]n\s+)?)[ABC]\b"
)


def _narr_text(shot):
    """narration_in_this_shot is a STRING in v11 canonical SPECs (cerro-aislado-v4, V5+) with a
    sibling `dialog_text`; legacy/synthetic fixtures use a dict {narrator_text, ...}. Accept both.
    (pattern_class 4/5: validators must parse the real artifact schema, not only synthetic fixtures.)"""
    n = shot.get("narration_in_this_shot")
    if isinstance(n, dict):
        return n.get("narrator_text") or ""
    if isinstance(n, str):
        return n
    return ""


def _beat_role(shot):
    """v11 canonical SPECs key beats via `section_id` (hook / setup_* / decision_* / consequence_* /
    cliffhanger_* / resolution_*); synthetic fixtures use `beat_role`. Accept both."""
    return str(shot.get("beat_role") or shot.get("section_id") or "")


def _wpm_band_for(role):
    r = role.lower()
    for prefix, key in (("hook", "hook"), ("setup", "setup"), ("decision", "decision_setup"),
                        ("consequence", "consequence"), ("cliffhanger", "cliffhanger")):
        if r.startswith(prefix):
            return WPM_BANDS[key]
    return WPM_BANDS.get(role, WPM_DEFAULT_BAND)


def gate(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def parse_videolog(path):
    """Parse Cross-video uniqueness table: rows with `| N | proj | loc | sig | conf |`."""
    text = Path(path).read_text(encoding="utf-8")
    rows = []
    seen = set()
    pat = re.compile(
        r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$",
        re.MULTILINE,
    )
    for m in pat.finditer(text):
        num = int(m.group(1))
        if num in seen:
            continue
        seen.add(num)
        rows.append({
            "num": num, "project": m.group(2).strip(), "location": m.group(3).strip(),
            "signature_staging": m.group(4).strip(), "confidence": m.group(5).strip(),
        })
    return rows


def parse_patterns_from_videolog(path):
    """Find pattern P<N> per row number (any table row starting with | N | + containing P\\d)."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|", line)
        if not m:
            continue
        num = int(m.group(1))
        if num in out:
            continue
        pmatch = re.search(r"\bP(\d+)\b", line)
        if pmatch:
            out[num] = f"P{pmatch.group(1)}"
    return out


def check_cliffhanger(cliff):
    if cliff in CANONICAL_PATTERNS:
        return gate("structure_cliffhanger", "pass", f"{cliff} ∈ canonical {{P1,P2,P3,P6,P9}}")
    return gate("structure_cliffhanger", "fail",
                f"cliffhanger_archetype='{cliff}' NOT ∈ canonical (P4/P5/P10/Meta deprecated per GAP #10)")


def check_hook_order(hook_beats):
    if not hook_beats:
        return gate("structure_hook_order", "fail", "hook_sub_beats empty")
    # v11 canonical: hook_sub_beats is a list of dicts {beat_id, ...}; synthetic fixtures use strings.
    last = hook_beats[-1]
    last_label = (last.get("beat_id") or last.get("content") or "") if isinstance(last, dict) else str(last)
    if "countdown" not in last_label.lower():
        return gate("structure_hook_order", "fail",
                    f"hook last beat='{last_label}' (must contain 'countdown' per canonical)")
    return gate("structure_hook_order", "pass", f"countdown is last hook beat ('{last_label}') ✓")


def check_dilema_placement(pct):
    lo, hi = DILEMA_PLACEMENT_BAND_PCT
    if pct is None:
        # v11 canonical SPECs derive dilema placement from section_id timeline, not a declared %.
        # Absent → not_applicable (NOT fail) — placement verified via shot_list sections / CP5 render.
        return gate("structure_dilema_placement", "not_applicable",
                    "dilema_placement_pct not declared (v11 derives from section_id timeline)")
    if lo <= float(pct) <= hi:
        return gate("structure_dilema_placement", "pass", f"{pct}% ∈ [{lo}, {hi}]")
    return gate("structure_dilema_placement", "fail",
                f"dilema placement {pct}% NOT in canonical band [{lo}, {hi}]")


def check_counterfactual(placement):
    if placement == "retrospective":
        return gate("structure_counterfactual", "fail",
                    "counterfactual_placement=retrospective is anti-pattern (PAUTA § 24)")
    if placement is None:
        return gate("structure_counterfactual", "fail", "counterfactual_placement missing")
    return gate("structure_counterfactual", "pass", f"placement={placement} ✓")


def check_consequence_framing(consequence_shots):
    """Primary-source enforcement (replaces synthetic 'Si elegiste X' substring check).

    Canonical consequence framing = "Si [acción condicional]" (6/8 @referent-a) or the
    choice-reference variant "Si decides/escogiste/tomaste ..." (2/8 @referent-b). The bare
    synthetic label "Si elegiste A/B" (0/8 — never in primary source) is the anti-pattern.
    """
    if not consequence_shots:
        return gate("structure_consequence_framing", "not_applicable",
                    "no consequence shots in shot_list")
    synthetic, missing = [], []
    for s in consequence_shots:
        txt = _narr_text(s)
        sid = s.get("shot_id", "?")
        if SYNTHETIC_LABEL_RE.search(txt):
            synthetic.append(sid)
        elif not ACTION_CONDITIONAL_RE.search(txt):
            missing.append(sid)
    if synthetic:
        return gate("structure_consequence_framing", "fail",
                    f"consequence shots use synthetic bare-label framing 'Si elegiste A/B' "
                    f"(0/8 primary source — anti-pattern): {synthetic}. Use action-conditional "
                    f"'Si [la enciendes / te niegas / esperas]' per ref-03/06/08/09/10/11.")
    if missing:
        # Principle = consequence marks its branch; the SPECIFIC marker is creative variability.
        # A consequence may be branch-marked via a bridge caption ("SI ELEGISTE B:") that this
        # validator (narrator_text only) cannot see → FLAG, do NOT hard-FAIL. Only the bare-label
        # anti-pattern above is a FAIL. (pattern_class 3/5: enforce principle, not creative choice.)
        return gate("structure_consequence_framing", "flag",
                    f"consequence shots without a detectable 'Si [acción]' marker in narrator_text: "
                    f"{missing}. Principle = branch must be marked; OK if done via bridge caption "
                    f"'SI ELEGISTE B' (not visible here). Verify branch-marking manually.")
    return gate("structure_consequence_framing", "pass",
                f"all {len(consequence_shots)} consequence shots use canonical "
                f"'Si [acción condicional]' framing ✓")


def check_wpm(shot_list):
    outliers = []
    for s in shot_list:
        # Shots carrying a countdown AVU overlay include NON-speaking time in duration_intent_s →
        # WPM from full duration is misleading (e.g. hook with 3s countdown). Skip.
        if "countdown" in str(s.get("avu_overlay_clip") or "").lower():
            continue
        role = _beat_role(s) or "default"
        txt = _narr_text(s)
        dur = s.get("duration_intent_s")
        if not txt or not dur or float(dur) <= 0:
            continue
        words = len(txt.split())
        wpm = words / float(dur) * 60
        lo, hi = _wpm_band_for(role)
        if not (lo <= wpm <= hi):
            outliers.append(f"{s.get('shot_id', '?')}(role={role}): {wpm:.0f}WPM ∉ [{lo},{hi}]")
    if outliers:
        # STYLE band (per-role canonical pace), ADVISORY only → FLAG. The blocking PHYSICS gate is
        # audit-spec-narration-fits-duration.py (WPM > 280 = TTS can't deliver = FAIL). A stylistic
        # deviation (dialog-heavy shot, marginal pace) should not hard-block. (pattern_class lens.)
        return gate("structure_wpm", "flag",
                    f"WPM stylistic-band advisory (blocking physics gate = narration-fits-duration): {outliers[:5]}")
    return gate("structure_wpm", "pass", "all shots WPM within per-role canonical stylistic bands")


def check_location_exact(spec_loc, prior_rows):
    norm = spec_loc.strip().lower()
    matches = [r for r in prior_rows if r["location"].strip().lower() == norm]
    if matches:
        return gate("uniqueness_location", "fail",
                    f"location '{spec_loc}' exact-matches prior #{[r['num'] for r in matches]}")
    return gate("uniqueness_location", "pass", "location unique cross-video")


def lexical_similarity(a, b):
    """Deterministic fallback similarity in [0, 1]: max(token Jaccard, char SequenceMatcher)."""
    import difflib

    na = " ".join(re.findall(r"\w+", str(a).lower()))
    nb = " ".join(re.findall(r"\w+", str(b).lower()))
    if not na or not nb:
        return 0.0
    ta, tb = set(na.split()), set(nb.split())
    jac = len(ta & tb) / len(ta | tb)
    return max(jac, difflib.SequenceMatcher(None, na, nb).ratio())


def check_signature_semantic(spec_sig, prior_rows, model, block_thr, flag_thr, *, lexical_fallback=False):
    if model is None and not lexical_fallback:
        return gate("uniqueness_signature_staging", "not_applicable",
                    "semantic check skipped (--skip-semantic)")
    sigs = [r["signature_staging"] for r in prior_rows]
    if not sigs:
        return gate("uniqueness_signature_staging", "not_applicable",
                    "no prior signature_staging in video-log")
    if model is None:
        # Fail-closed: without the embedding model, still catch near-verbatim reuse lexically
        # (the old code silently returned not_applicable, letting duplicates through).
        sims = [lexical_similarity(spec_sig, s) for s in sigs]
    else:
        embs = model.encode([spec_sig] + sigs, normalize_embeddings=True)
        # cosine via dot product (embeddings normalized)
        sims = (embs[0] @ embs[1:].T).tolist()
    if isinstance(sims, float):
        sims = [sims]
    max_sim = max(sims)
    max_idx = sims.index(max_sim)
    nearest = prior_rows[max_idx]
    if max_sim >= block_thr:
        return gate("uniqueness_signature_staging", "fail",
                    f"signature similarity {max_sim:.3f} ≥ block {block_thr} vs prior #{nearest['num']}")
    if max_sim >= flag_thr:
        return gate("uniqueness_signature_staging", "flag",
                    f"signature similarity {max_sim:.3f} ∈ [{flag_thr},{block_thr}) FLAG vs prior #{nearest['num']}")
    return gate("uniqueness_signature_staging", "pass",
                f"signature distinct (max similarity {max_sim:.3f} < flag {flag_thr})")


def check_pattern_rotation(spec_cliff, patterns_map):
    if not patterns_map:
        return gate("uniqueness_pattern_rotation", "not_applicable", "no prior patterns in video-log")
    last_num = max(patterns_map.keys())
    last_pat = patterns_map[last_num]
    if spec_cliff == last_pat:
        return gate("uniqueness_pattern_rotation", "fail",
                    f"V5 pattern '{spec_cliff}' = last video #{last_num} pattern (HR#14 rotation violation)")
    return gate("uniqueness_pattern_rotation", "pass",
                f"V5 pattern '{spec_cliff}' ≠ last video #{last_num} ({last_pat}) ✓")


def collect_all_text(spec):
    pieces = []
    for s in spec.get("shot_list", []) or []:
        nt = _narr_text(s)
        if nt:
            pieces.append(nt)
        n = s.get("narration_in_this_shot")
        # dialog_text: dict form (n.dialog_text) OR v11 sibling (shot.dialog_text)
        dlg = (n.get("dialog_text") if isinstance(n, dict) else None) or s.get("dialog_text")
        if dlg:
            pieces.append(str(dlg))
    extra = spec.get("extra_text")
    if extra:
        pieces.append(str(extra))
    return " ".join(pieces).lower()


def check_anti_cliche(spec_text, phrases):
    hits = [p for p in phrases if p.lower() in spec_text]
    if hits:
        return gate("anti_cliche", "fail", f"forbidden cliché phrase(s) in SPEC: {hits}")
    return gate("anti_cliche", "pass", f"no forbidden cliché phrases (checked {len(phrases)})")


def lazy_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--video-log", default=None, help="Path to video-log MD")
    parser.add_argument("--anti-cliche-file", default=None,
                        help="Optional file with one forbidden phrase per line")
    parser.add_argument("--block-threshold", type=float, default=0.85)
    parser.add_argument("--flag-threshold", type=float, default=0.75)
    parser.add_argument("--skip-semantic", action="store_true",
                        help="Skip sentence-transformers semantic check (fast tests)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    spec = load_spec(spec_path)
    caps = spec.get("video_capabilities")
    if caps is None:
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
              file=sys.stderr)
        return 2
    fmt_type = caps.get("format_type")

    if args.dry_run:
        branch = "narrative_checks" if fmt_type == "interactive_choice" else "not_applicable"
        print(f"format: {args.format}\nspec: {spec_path}\nformat_type: {fmt_type}\nbranch: {branch}")
        return 0

    if fmt_type != "interactive_choice":
        report = {
            "format": args.format, "format_type": fmt_type,
            "overall_status": "not_applicable",
            "detail": (f"Narrative coherence checks only applicable to format_type=interactive_choice "
                       f"(got '{fmt_type}'). Other formats skip narrative validation.")
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("not_applicable")
        return 0

    # Anti-cliche phrases
    if args.anti_cliche_file and Path(args.anti_cliche_file).exists():
        phrases = [l.strip() for l in Path(args.anti_cliche_file).read_text(encoding="utf-8").splitlines()
                   if l.strip()]
    else:
        phrases = list(DEFAULT_ANTI_CLICHE)

    ns = spec.get("narrative_structure") or {}
    gates = []

    # Structure
    gates.append(check_cliffhanger(ns.get("cliffhanger_archetype")))
    gates.append(check_hook_order(ns.get("hook_sub_beats") or []))
    gates.append(check_dilema_placement(ns.get("dilema_placement_pct")))
    gates.append(check_counterfactual(ns.get("counterfactual_placement")))
    shot_list = spec.get("shot_list") or []
    consequence_shots = [s for s in shot_list if _beat_role(s).startswith("consequence")]
    gates.append(check_consequence_framing(consequence_shots))
    gates.append(check_wpm(shot_list))

    # Cross-video uniqueness
    prior_rows, patterns_map = [], {}
    if args.video_log and Path(args.video_log).exists():
        prior_rows = parse_videolog(args.video_log)
        patterns_map = parse_patterns_from_videolog(args.video_log)

    if prior_rows:
        if spec.get("location"):
            gates.append(check_location_exact(spec["location"], prior_rows))
        if spec.get("signature_staging"):
            model = None
            fallback = False
            if not args.skip_semantic:
                try:
                    model = lazy_model()
                except Exception as e:
                    fallback = True
                    print(f"⚠️ sentence-transformers unavailable ({type(e).__name__}) — "
                          f"using lexical similarity fallback", file=sys.stderr)
            gates.append(check_signature_semantic(spec["signature_staging"], prior_rows,
                                                  model, args.block_threshold, args.flag_threshold,
                                                  lexical_fallback=fallback))
        if patterns_map and ns.get("cliffhanger_archetype"):
            gates.append(check_pattern_rotation(ns["cliffhanger_archetype"], patterns_map))

    # Anti-cliche
    gates.append(check_anti_cliche(collect_all_text(spec), phrases))

    fails = [g for g in gates if g["status"] == "fail"]
    flags = [g for g in gates if g["status"] == "flag"]
    overall = "fail" if fails else ("flag" if flags else "pass")
    report = {
        "format": args.format, "format_type": fmt_type,
        "overall_status": overall, "overall_pass": overall == "pass",
        "fail_count": len(fails), "flag_count": len(flags), "gates": gates,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
