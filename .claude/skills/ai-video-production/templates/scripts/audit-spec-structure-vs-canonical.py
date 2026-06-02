#!/usr/bin/env python3
"""audit-spec-structure-vs-canonical.py — horror-choice structure/invariant gate (PAUTA-MASTER § 2).

Enforces .claude/skills/horror-choice-format/PAUTA-MASTER.md § 2 (the structural authority
derived empirically from 5 canonical refs, 2026-06-01) programmatically, pre-emit. This is the
"SPEC-AUDIT structure axis" referenced in PAUTA-MASTER § 2.4: the architect runs it against
his OWN spec (HR#27 self-validation) and the auditor re-runs it (anti-pattern #17).

Why it exists: the format skeleton + the "bueno aparente never decides with the viewer" invariant
were implicit in PAUTA-MASTER but NEVER codified as an auditable invariant → in V6 (invernadero)
the bueno-aparente (Celeste) ended up present in the PLAYED PATH tempting the viewer at shots
05/06/07/10/11, violating the canon, and neither architect nor auditor flagged it in time (they
rationalized it). This validator turns the structure into something the SPEC-AUDIT checks explicitly.

Checks (each gate: pass | fail | flag | not_applicable):
  § 2 INVARIANT (the key check — 🔴 FAIL):
    The character with role: bueno_aparente must NOT appear in scene_context.who_is_there (nor
    anchor_id_required) of ANY decision/consequence shot of the PLAYED PATH. The played path =
    shots whose section_id ∈ {setup_pre_decision, decision_*, consequence_*}. The bueno_aparente
    may ONLY appear in hook / counterfactual_* / cliffhanger_*.
  § 1 STRUCTURE (🟡 flag if a block is missing):
    hook + countdown, played-path with 2-3 decisions (each decision_N having a consequence_A
    shot AND a consequence_B shot), counterfactual (opening or final), cliffhanger.
  § 3 SEQUENTIAL PATHS (🔴 fail if interleaved):
    the counterfactual is not interleaved inside the played path (it sits at the very start,
    before the first played-path section, or at the very end, after the last one).

Capability-gate (Pattern 7): format != horror-choice → not_applicable. video_capabilities
missing → Bug #9 (exit 2). Agnostic-by-design: --format REQUIRED.

Exit codes: 0 = pass | flag | not_applicable (no hard structural violation).
            1 = fail (🔴 invariant or sequential-paths violation).
            2 = usage / missing SPEC / missing video_capabilities (Bug #9).

Build 2026-06-01 — TDD + Hard Rule #26 companion test (test_audit-spec-structure-vs-canonical.py).
Authority: horror-choice-format/PAUTA-MASTER.md § 2 (§§ 2.1/2.2/2.3/2.4).
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

# PAUTA-MASTER § 2.1/2.2 — section taxonomy.
# PLAYED PATH = the recorrido jugado (the chosen/scary companion's path). The bueno_aparente
# is FORBIDDEN here.
PLAYED_PATH_PREFIXES = ("setup_pre_decision", "decision", "consequence", "resolution")
# Sections where the bueno_aparente is ALLOWED to appear (hook dyad + counterfactual cozy +
# cliffhanger). PAUTA-MASTER § 2.2.
ALLOWED_FOR_BUENO_PREFIXES = ("hook", "counterfactual", "cliffhanger")

# The subset of the played path that constitutes "taking decisions WITH the viewer" — the exact
# scope of the § 2 invariant (decision setups + the consequence branches). setup_pre_decision is
# included because that is where the dyad establishes the temptation (V6 shot_05 = setup_pre_decision
# was a violation locus). resolution_* is excluded from the invariant scope (the chosen companion
# legitimately resolves the night there) but is still part of the played path for § 3 sequencing.
INVARIANT_SCOPE_PREFIXES = ("setup_pre_decision", "decision", "consequence")


def gate(name, status, detail):
    return {"name": name, "status": status, "detail": detail}


def _section_id(shot):
    """v11 canonical SPECs key beats via `section_id`; synthetic fixtures may use `beat_role`."""
    return str(shot.get("section_id") or shot.get("beat_role") or "").strip()


def _has_prefix(section_id, prefixes):
    sid = section_id.lower()
    return any(sid == p or sid.startswith(p) for p in prefixes)


def _decision_index(section_id):
    """Extract N from decision_N / decision_N_climax / consequence_dN / consequence_N. None if absent."""
    m = re.search(r"(?:decision|consequence)[_a-z]*?_?d?(\d+)", section_id.lower())
    return int(m.group(1)) if m else None


def _consequence_branch(shot):
    """Return 'A' | 'B' | None for a consequence shot.

    Branch detection (in priority order, robust to creative variation):
      1. explicit shot field `consequence_branch: A|B`.
      2. section_id suffix (consequence_d1_a / consequence_a1 / ..._b).
      3. fatal-vs-survive heuristic: a consequence-A in this format is the FATAL branch (death),
         consequence-B is the survive-continue branch. We infer from the bridge/branch caption
         text + narration "Si [acción]" framing only as a last resort, so we DON'T over-claim;
         when ambiguous we group by (decision_index, narration-conditional) pairing in the caller.
    """
    explicit = str(shot.get("consequence_branch") or "").strip().upper()
    if explicit in ("A", "B"):
        return explicit
    sid = _section_id(shot).lower()
    m = re.search(r"_([ab])\d*$", sid) or re.search(r"_([ab])$", sid) or re.search(r"_d?\d+_([ab])\b", sid)
    if m:
        return m.group(1).upper()
    return None


def load_spec(spec_path):
    with open(spec_path) as f:
        return yaml.safe_load(f)


def _bueno_aparente_id(spec):
    """Find the character_id whose role is bueno_aparente. Returns (cid, name) or (None, None)."""
    for c in spec.get("characters", []) or []:
        if str(c.get("role") or "").strip().lower() == "bueno_aparente":
            return c.get("character_id"), c.get("name")
    return None, None


def _shot_references_char(shot, char_id):
    """True if the bueno_aparente char_id is present in this shot's who_is_there OR anchor_id_required."""
    sc = shot.get("scene_context") or {}
    who = sc.get("who_is_there") or []
    if isinstance(who, str):
        who = [who]
    if char_id in who:
        return True
    anchors = shot.get("anchor_id_required") or {}
    if isinstance(anchors, dict) and char_id in anchors:
        return True
    return False


def check_invariant(spec, shots):
    """§ 2 INVARIANT — bueno_aparente NEVER in the played-path decision/consequence shots."""
    cid, cname = _bueno_aparente_id(spec)
    if not cid:
        return gate("invariant_bueno_aparente_absent_from_played_path", "not_applicable",
                    "no character with role: bueno_aparente declared — cannot evaluate § 2 invariant "
                    "(declare one per PAUTA-MASTER § 2.1, or this is not a horror-choice dyad SPEC)")
    violations = []
    for s in shots:
        sid = _section_id(s)
        if not _has_prefix(sid, INVARIANT_SCOPE_PREFIXES):
            continue
        if _shot_references_char(s, cid):
            violations.append(f"{s.get('shot_id', '?')}(section={sid})")
    if violations:
        return gate(
            "invariant_bueno_aparente_absent_from_played_path", "fail",
            f"bueno-aparente '{cname}' ({cid}) presente en el played path "
            f"(who_is_there/anchor) de shots de decisión/consecuencia: {violations}. "
            f"Viola invariante PAUTA-MASTER § 2.2 (el bueno-aparente SOLO puede estar en "
            f"hook / counterfactual / cliffhanger — NUNCA decidiendo con el viewer en el recorrido "
            f"jugado). 🔴 RETORNA al arquitecto (HR#27).")
    return gate("invariant_bueno_aparente_absent_from_played_path", "pass",
                f"bueno-aparente '{cname}' ({cid}) ausente del played path — solo en "
                f"hook/counterfactual/cliffhanger ✓ (PAUTA-MASTER § 2.2)")


def check_bueno_only_in_allowed(spec, shots):
    """Companion to § 2: confirm the bueno_aparente DOES appear somewhere allowed (hook /
    counterfactual / cliffhanger). If declared but never present anywhere → FLAG (dyad incomplete)."""
    cid, cname = _bueno_aparente_id(spec)
    if not cid:
        return gate("invariant_bueno_aparente_present_in_allowed", "not_applicable",
                    "no bueno_aparente declared")
    allowed_hits = [
        s.get("shot_id", "?") for s in shots
        if _has_prefix(_section_id(s), ALLOWED_FOR_BUENO_PREFIXES) and _shot_references_char(s, cid)
    ]
    if allowed_hits:
        return gate("invariant_bueno_aparente_present_in_allowed", "pass",
                    f"bueno-aparente '{cname}' presente en hook/counterfactual/cliffhanger: {allowed_hits} ✓")
    return gate("invariant_bueno_aparente_present_in_allowed", "flag",
                f"bueno-aparente '{cname}' ({cid}) declarado pero NO aparece en ningún shot de "
                f"hook/counterfactual/cliffhanger. El dyad necesita presentarlo (hook) + su recorrido "
                f"cozy (counterfactual). Verificá la presentación (PAUTA-MASTER § 2.1/2.2).")


def check_structure(shots):
    """§ 1 STRUCTURE — hook+countdown, played path with 2-3 decisions (each w/ consequence A & B),
    counterfactual (opening or final), cliffhanger. Missing block → FLAG (🟡)."""
    missing = []
    section_ids = [_section_id(s) for s in shots]

    has_hook = any(_has_prefix(sid, ("hook",)) for sid in section_ids)
    if not has_hook:
        missing.append("hook")

    # countdown — declared via avu_overlay_clip containing 'countdown' in a hook shot, OR a hook
    # sub-beat named countdown (checked elsewhere); here we scan the hook shots' avu clips + ui.
    has_countdown = False
    for s in shots:
        if not _has_prefix(_section_id(s), ("hook",)):
            continue
        avu = str(s.get("avu_overlay_clip") or "").lower()
        if "countdown" in avu:
            has_countdown = True
            break
        for ui in (s.get("ui_active") or []):
            if isinstance(ui, dict) and "countdown" in str(ui.get("element_id") or "").lower():
                has_countdown = True
                break
        if has_countdown:
            break
    if has_hook and not has_countdown:
        missing.append("hook_countdown (no avu_overlay_clip/ui countdown in hook shot)")

    has_counterfactual = any(_has_prefix(sid, ("counterfactual",)) for sid in section_ids)
    if not has_counterfactual:
        missing.append("counterfactual (opening or final)")

    has_cliffhanger = any(_has_prefix(sid, ("cliffhanger",)) for sid in section_ids)
    if not has_cliffhanger:
        missing.append("cliffhanger")

    # Decisions: 2-3, each with a consequence_A shot AND a consequence_B shot.
    decision_idx = sorted({_decision_index(sid) for sid in section_ids
                           if _has_prefix(sid, ("decision",)) and _decision_index(sid) is not None})
    n_decisions = len(decision_idx)
    if n_decisions < 2:
        missing.append(f"played-path decisions (found {n_decisions}, canonical 2-3)")
    elif n_decisions > 3:
        missing.append(f"played-path decisions out of band (found {n_decisions}, canonical 2-3)")

    # Per decision: at least one consequence shot with branch A AND one with branch B.
    # Group consequence shots by decision index; detect A/B per group.
    branch_gaps = []
    for di in decision_idx:
        cons = [s for s in shots
                if _has_prefix(_section_id(s), ("consequence",)) and _decision_index(_section_id(s)) == di]
        branches = {_consequence_branch(s) for s in cons}
        narr_conditionals = [s for s in cons if re.search(r"\bsi\b", str(s.get("narration_in_this_shot") or ""),
                                                           re.IGNORECASE)]
        # Robust 2-branch detection: explicit/sid branches A&B present, OR ≥2 distinct
        # "Si [acción]" consequence narrations under this decision (one per branch).
        has_ab = ("A" in branches and "B" in branches) or (len(narr_conditionals) >= 2)
        if not has_ab:
            branch_gaps.append(f"D{di} (consequence shots={[s.get('shot_id','?') for s in cons]}, "
                               f"branches detected={sorted(b for b in branches if b)})")
    if branch_gaps:
        missing.append(f"each decision needs a consequence_A AND consequence_B: gaps in {branch_gaps}")

    if missing:
        return gate("structure_skeleton", "flag",
                    f"PAUTA-MASTER § 2.1 skeleton incomplete: {missing}. "
                    f"Canonical = hook+countdown → played path (2-3 decisions, each A muerte / B sobrevive) "
                    f"→ counterfactual → cliffhanger.")
    return gate("structure_skeleton", "pass",
                f"skeleton complete: hook+countdown + {n_decisions} decisions (each A & B) + "
                f"counterfactual + cliffhanger ✓ (PAUTA-MASTER § 2.1)")


def check_sequential_paths(shots):
    """§ 3 — counterfactual is NOT interleaved inside the played path. It must sit before the FIRST
    played-path section (opening variant) or after the LAST one (final/default). 🔴 fail if interleaved."""
    counterfactual_positions = [i for i, s in enumerate(shots)
                                if _has_prefix(_section_id(s), ("counterfactual",))]
    if not counterfactual_positions:
        return gate("sequential_paths", "not_applicable",
                    "no counterfactual section to position-check (structure gate flags its absence)")
    played_positions = [i for i, s in enumerate(shots)
                        if _has_prefix(_section_id(s), PLAYED_PATH_PREFIXES)]
    if not played_positions:
        return gate("sequential_paths", "not_applicable", "no played-path sections to compare against")
    first_played, last_played = min(played_positions), max(played_positions)
    interleaved = [shots[i].get("shot_id", "?") for i in counterfactual_positions
                   if first_played < i < last_played]
    if interleaved:
        return gate("sequential_paths", "fail",
                    f"counterfactual shots {interleaved} están INTERCALADOS dentro del played path "
                    f"(played-path span shots index {first_played}..{last_played}). Viola "
                    f"PAUTA-MASTER § 2.3 (los dos recorridos son SECUENCIALES, jamás simultáneos: "
                    f"el counterfactual va al INICIO o al FINAL, no en el medio).")
    placement = "opening" if max(counterfactual_positions) < first_played else (
        "final" if min(counterfactual_positions) > last_played else "split")
    return gate("sequential_paths", "pass",
                f"counterfactual {placement} of the played path — secuencial, no intercalado ✓ "
                f"(PAUTA-MASTER § 2.3)")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
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

    # Capability gate: this validator is horror-choice CAPA 2 ONLY (PAUTA-MASTER § 2 is
    # horror-choice-only). We gate on the --format flag (the artifact-level genre declaration).
    fmt = str(args.format or "").strip().lower()
    if args.dry_run:
        branch = "structure_checks" if fmt == "horror-choice" else "not_applicable"
        print(f"format: {args.format}\nspec: {spec_path}\nbranch: {branch}")
        return 0

    if fmt != "horror-choice":
        report = {
            "format": args.format, "overall_status": "not_applicable",
            "detail": (f"PAUTA-MASTER § 2 is horror-choice CAPA 2 only. format='{args.format}' "
                       f"≠ horror-choice → structural canonical checks skipped.")
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("not_applicable")
        return 0

    shots = spec.get("shot_list") or []
    if not shots:
        report = {"format": args.format, "overall_status": "fail",
                  "detail": "shot_list empty/absent — cannot audit structure."}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 1

    gates = [
        check_invariant(spec, shots),            # § 2 — the key check (FAIL)
        check_bueno_only_in_allowed(spec, shots),  # § 2 companion (FLAG)
        check_structure(shots),                  # § 1 — skeleton (FLAG)
        check_sequential_paths(shots),           # § 3 — sequencing (FAIL)
    ]

    fails = [g for g in gates if g["status"] == "fail"]
    flags = [g for g in gates if g["status"] == "flag"]
    overall = "fail" if fails else ("flag" if flags else "pass")
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "authority": "horror-choice-format/PAUTA-MASTER.md § 2 (§§ 2.1/2.2/2.3)",
        "overall_status": overall,
        "overall_pass": overall == "pass",
        "fail_count": len(fails),
        "flag_count": len(flags),
        "gates": gates,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
