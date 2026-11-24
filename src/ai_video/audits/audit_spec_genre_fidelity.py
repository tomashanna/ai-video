#!/usr/bin/env python3
"""audit-spec-genre-fidelity.py — Firewall de GÉNERO sport-choice (no-horror guard, BONUS).

Scans a sport-choice SPEC and flags HORROR-LEAK: the horror sabor sneaking into a
fútbol-real video. sport-choice and horror-choice are SIBLINGS that inherit the same
agnostic choice MECHANIC (choice-format-core) — they share so much that the horror
flavor (death/body-horror/monsters, terror drones/screams/whispers SFX, the grave
omniscient horror narrator voice_id, cool_horror LUT) trivially leaks in.

This is the SPEC-level accelerator for the checklist doc:
  sport-choice-format/NO-HORROR-GUARD.md  (the MUST — human/visual items G1/G7/G8 live there).

What this scanner covers (checklist items G2-G6, the ones that live in the SPEC):
  G2  SFX palette          — terror SFX (drone/scream/whisper/sub-bass/death-scream) in asset_list SFX prompts
  G3  narrator voice        — horror grave narrator voice_id (Tj9l48J9AJbry5yCP5eW) in narrator_voice / narration_script
  G4  music                 — dark ambient / horror drone in music layer ElevenLabs prompts
  G5  body-horror/death     — death / monster / body-horror / uncanny terms in narration + visual_intent + description
  G6  LUTs                  — cool_horror / horror_* LUT names in visual_style_lut (section + shot level)

What it does NOT cover (stays human/visual in NO-HORROR-GUARD.md):
  G1 preset CSS (lives in index.html / BRAND, not the SPEC),
  G7 estadio geography (needs frame inspection — Gate 4 Gemini Vision),
  G8 layer inheritance (needs reading the engineer handoff/process).

Authority:
  sport-choice-format/PAUTA-MASTER.md §0 BAN + §6 (failure = deportivo, NO daño físico)
  sport-choice-format/INGENIERO-PAUTA-MASTER.md §2 (SFX palette absolute rule) + §4 (LUTs / música)
  horror-choice-format/VISUAL-STYLE.md (lúgubre preset = OPPOSITE)

Capability-aware: has_ai_generated_clips required for a meaningful scan; video_capabilities
missing → Bug #9 (exit 2). Agnostic-by-design: --format REQUIRED. The scan only runs for
sport-family formats (sport-choice); other formats → not_applicable (exit 0) so the gate is a
no-op for horror (NON-DESTRUCTIVE — horror's own validators are untouched).

Build 2026-06-01 — TDD + Hard Rule #26 companion test (test_audit-spec-genre-fidelity.py).
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

# ---------------------------------------------------------------------------
# Horror-leak lexicon. Each entry is a checklist item + a regex (word-bounded,
# accent/case-insensitive). Built from NO-HORROR-GUARD.md "Catálogo de términos".
# Deliberately CONSERVATIVE: only terms that are unambiguous horror, so legit
# sport tension words (tensión, rugido, abucheos, drone subharmónico de tensión
# DEPORTIVA, cool_defeat, derrota, presión, clímax, gol rival) do NOT false-fail.
# ---------------------------------------------------------------------------

# Horror voice_id (horror-choice grave/whisper narrator — deprecated 2026-05-18).
HORROR_VOICE_IDS = {"Tj9l48J9AJbry5yCP5eW"}

# Term groups: (item_code, human_label, [regex patterns]). Patterns are matched
# case-insensitively; \b word boundaries keep them from matching inside other words.
LEXICON = [
    # G5 — death / physical harm to the protagonist (consequence of error must be
    # sporting humiliation, NOT physical damage — PAUTA §0 BAN + §6).
    (
        "G5",
        "death / physical harm",
        [
            r"\bmuerte\b",
            r"\bmueres\b",
            r"\bmorir\b",
            r"\bmuere\b",
            r"\bcad[áa]ver\b",
            r"\bsangre\b",
            r"\bsangr\w*",
            r"\bmutila\w*",
            r"\bdescuartiz\w*",
            r"\bagoniz\w*",
            r"\bdeath\b",
            r"\bblood\b",
            r"\bcorpse\b",
            r"\bgore\b",
        ],
    ),
    # G5 — monsters / supernatural.
    (
        "G5",
        "monster / supernatural",
        [
            r"\bmonstruo\w*",
            r"\bcriatura\w*",
            r"\bdemonio\w*",
            r"\bente\b",
            r"\bfantasma\w*",
            r"\bespectro\w*",
            r"\bposesi[óo]n\b",
            r"\bpos[ée]\w*",
            r"\bsacrificio\b",
            r"\britual\b",
            r"\bmonster\b",
            r"\bcreature\b",
            r"\bdemon\b",
            r"\bghost\b",
        ],
    ),
    # G5 — body-horror / uncanny.
    (
        "G5",
        "body-horror / uncanny",
        [
            r"\bbody[\s-]?horror\b",
            r"\bdeforme\w*",
            r"\bgrotesc\w*",
            r"\bperturbador\w*",
            r"\buncanny\b",
            r"\bantinatural\w*",
        ],
    ),
    # G5 — terror atmosphere (NOTE: "terror"/"horror"/"jumpscare" but NOT "tensión").
    (
        "G5",
        "terror atmosphere",
        [
            r"\bterror\b",
            r"\bhorror\b",
            r"\bpesadilla\w*",
            r"\bpavor\b",
            r"\bjumpscare\b",
            r"\bnightmare\b",
            r"\bdread\b",
        ],
    ),
    # G4 — horror audio in MUSIC layer prompts (dark ambient / horror drone).
    # "drone" alone is NOT leak (sport uses "drone subharmónico de tensión deportiva");
    # the leak is the HORROR qualifier next to it, or dark-ambient/eerie.
    (
        "G4",
        "horror music (dark ambient / horror drone / eerie pad)",
        [
            r"\bdark\s+ambient\b",
            r"\bhorror\s+drone\b",
            r"\bdrone\s+(?:of\s+)?(?:terror|horror)\b",
            r"\beerie\b",
            r"\bdread\s+ambience\b",
            r"\bdrone\s+uncanny\b",
            r"\buncanny\s+drone\b",
        ],
    ),
    # G2 — horror SFX palette (screams / whispers / jumpscare sub-bass / death-scream).
    (
        "G2",
        "horror SFX (scream / whisper / jumpscare sub-bass)",
        [
            r"\bscream\w*",
            r"\bdeath[\s-]?scream\b",
            r"\bwhisper\w*",
            r"\bsusurro\w*",
            r"\bsusurr\w*",
            r"\bgrito\s+de\s+(?:terror|horror|pavor)\b",
            r"\bjumpscare\b",
            r"\bsub[\s-]?bass\s+(?:jumpscare|horror|dread)\b",
            r"\bheartbeat\s+(?:dread|horror|pavor)\b",
        ],
    ),
]


def _norm(text: str) -> str:
    """Lowercase + strip accents so 'muérete' and 'muerete' both match. Keeps word chars."""
    if not text:
        return ""
    t = text.lower()
    repl = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n"}
    return "".join(repl.get(c, c) for c in t)


# Negation guard: the CANONICAL sport music/SFX ElevenLabs prompts deliberately END with a
# NEGATIVE instruction to the model ("...no horror", "sin horror", "without horror") so the
# generator does NOT produce a terror bed. That is the OPPOSITE of a leak — it must NOT flag.
# We detect a negation immediately preceding the matched term and skip the hit.
_NEGATORS = (re.compile(_norm(r"(?:\bno\b|\bsin\b|\bwithout\b|\bavoid\b|\bnot\b)\s*$"), re.IGNORECASE),)


def _is_negated(norm_text: str, match_start: int) -> bool:
    """True if the term at `match_start` is immediately preceded by a negator (no/sin/without)."""
    preceding = norm_text[max(0, match_start - 15) : match_start]
    return any(neg.search(preceding) for neg in _NEGATORS)


# Pre-normalize the lexicon patterns too (accents stripped) and compile once.
def _compile():
    compiled = []
    for code, label, pats in LEXICON:
        cps = [re.compile(_norm(p), re.IGNORECASE) for p in pats]
        compiled.append((code, label, cps))
    return compiled


COMPILED = _compile()


def _scan_text(text, *, field, shot_id=None):
    """Return a list of leak hits found in `text`."""
    hits = []
    if not text or not isinstance(text, str):
        return hits
    norm = _norm(text)
    for code, label, cps in COMPILED:
        flagged = False
        for cp in cps:
            for m in cp.finditer(norm):
                # Skip negated mentions ("no horror" / "sin drones" — a deliberate NEGATIVE
                # prompt instruction, the opposite of a leak).
                if _is_negated(norm, m.start()):
                    continue
                # locate the matched substring in the ORIGINAL for a readable snippet
                snippet = text[max(0, m.start() - 25) : m.end() + 25].replace("\n", " ").strip()
                hits.append(
                    {
                        "item": code,
                        "category": label,
                        "field": field,
                        "shot_id": shot_id,
                        "term": m.group(0),
                        "snippet": snippet,
                    }
                )
                flagged = True
                break  # one hit per group/field is enough to flag
            if flagged:
                break
    return hits


def _iter_narration(spec):
    """Yield (field_label, text, shot_id) for every narration string in the SPEC."""
    for seg in spec.get("narration_script") or []:
        if isinstance(seg, dict):
            yield (
                "narration_script.text_canonical",
                seg.get("text_canonical") or seg.get("text") or "",
                seg.get("shot_id_anchor"),
            )
    for s in spec.get("shot_list") or []:
        if not isinstance(s, dict):
            continue
        sid = s.get("shot_id")
        nis = s.get("narration_in_this_shot")
        if isinstance(nis, str):
            yield ("shot.narration_in_this_shot", nis, sid)
        elif isinstance(nis, dict):
            yield ("shot.narration_in_this_shot", nis.get("narrator_text") or "", sid)
        # dialog spoken by characters on-screen
        dt = s.get("dialog_text")
        if isinstance(dt, str):
            yield ("shot.dialog_text", dt, sid)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--format", required=True, help="format id (sport-choice → scan; others → not_applicable)"
    )
    parser.add_argument("--spec", required=True)
    parser.add_argument(
        "--max-hits",
        type=int,
        default=0,
        help="if >0, truncate the reported hit list (the verdict is unaffected)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    is_sport = "sport" in args.format.lower()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f) or {}

    caps = spec.get("video_capabilities")
    if caps is None:
        print(
            "ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\n"
            f"is_sport_family: {is_sport}\n"
            f"branch: {'genre_fidelity_scan' if is_sport else 'not_applicable'}"
        )
        return 0

    # Agnostic-by-design + NON-DESTRUCTIVE: only sport-family formats are scanned.
    # horror-choice (and anything else) → no-op so this gate never touches horror.
    if not is_sport:
        report = {
            "format": args.format,
            "overall_status": "not_applicable",
            "detail": "genre-fidelity (no-horror) scan applies to sport-family formats only; "
            "other formats are a no-op (NON-DESTRUCTIVE — horror validators untouched)",
        }
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    hits = []

    # --- G5: narration + dialog text ---
    for field, text, sid in _iter_narration(spec):
        hits.extend(_scan_text(text, field=field, shot_id=sid))

    # --- G5: visual_intent + description per shot ---
    for s in spec.get("shot_list") or []:
        if not isinstance(s, dict):
            continue
        sid = s.get("shot_id")
        hits.extend(_scan_text(s.get("visual_intent"), field="shot.visual_intent", shot_id=sid))
        hits.extend(_scan_text(s.get("description"), field="shot.description", shot_id=sid))

    # --- G6: LUT names (section level + shot level) ---
    def _check_lut(lut, *, field, sid=None):
        if isinstance(lut, str) and "horror" in lut.lower():
            hits.append(
                {
                    "item": "G6",
                    "category": "horror LUT",
                    "field": field,
                    "shot_id": sid,
                    "term": lut,
                    "snippet": lut,
                }
            )

    for sec in spec.get("narrative_sections") or []:
        if isinstance(sec, dict):
            _check_lut(
                sec.get("visual_style_lut"),
                field=f"narrative_sections[{sec.get('section_id')}].visual_style_lut",
            )
    for s in spec.get("shot_list") or []:
        if isinstance(s, dict):
            _check_lut(s.get("visual_style_lut"), field="shot.visual_style_lut", sid=s.get("shot_id"))

    # --- G4: music layer ElevenLabs prompts ---
    for layer in spec.get("music_continuous_layers") or []:
        if isinstance(layer, dict):
            hits.extend(
                _scan_text(
                    layer.get("eleven_labs_prompt") or layer.get("elevenlabs_prompt"),
                    field=f"music_continuous_layers[{layer.get('layer_id')}].eleven_labs_prompt",
                )
            )

    # --- G2: SFX prompts (asset_list.sfx_prompts_to_generate) ---
    al = spec.get("asset_list") or {}
    if isinstance(al, dict):
        for sfx in al.get("sfx_prompts_to_generate") or []:
            if isinstance(sfx, dict):
                hits.extend(
                    _scan_text(sfx.get("prompt"), field=f"asset_list.sfx[{sfx.get('sfx_id')}].prompt")
                )

    # --- G3: horror narrator voice_id ---
    voice_hits = []
    nv = spec.get("narrator_voice")
    if isinstance(nv, str) and nv in HORROR_VOICE_IDS:
        voice_hits.append(
            {
                "item": "G3",
                "category": "horror narrator voice_id",
                "field": "narrator_voice",
                "shot_id": None,
                "term": nv,
                "snippet": "horror grave/whisper narrator (deprecated 2026-05-18)",
            }
        )
    for seg in spec.get("narration_script") or []:
        if isinstance(seg, dict) and seg.get("voice_id") in HORROR_VOICE_IDS:
            voice_hits.append(
                {
                    "item": "G3",
                    "category": "horror narrator voice_id",
                    "field": f"narration_script[{seg.get('segment_id')}].voice_id",
                    "shot_id": seg.get("shot_id_anchor"),
                    "term": seg.get("voice_id"),
                    "snippet": "horror grave narrator voice_id",
                }
            )
    hits.extend(voice_hits)

    # de-dup identical (item, field, term) tuples
    seen = set()
    deduped = []
    for h in hits:
        key = (h["item"], h["field"], h["term"], h["shot_id"])
        if key not in seen:
            seen.add(key)
            deduped.append(h)
    hits = deduped

    items_flagged = sorted({h["item"] for h in hits})
    overall = "fail" if hits else "pass"
    shown = hits if args.max_hits <= 0 else hits[: args.max_hits]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "overall_status": overall,
        "overall_pass": not hits,
        "checklist_items_scanned": ["G2", "G3", "G4", "G5", "G6"],
        "checklist_items_not_scanned_human_visual": [
            "G1 (CSS preset)",
            "G7 (estadio geography)",
            "G8 (layer inheritance)",
        ],
        "items_flagged": items_flagged,
        "leak_count": len(hits),
        "leaks": shown,
        "note": "human/visual verification of G1/G7/G8 still required — see NO-HORROR-GUARD.md",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not hits else 1


if __name__ == "__main__":
    sys.exit(main())
