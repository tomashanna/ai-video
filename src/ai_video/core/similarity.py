"""
similarity.py — shared text similarity utilities for Script A + Script B.

Per CONTRACT-A-B-INTERFACE.md § 3: Jaccard word-level, case-insensitive,
punctuation-stripped. Both Script A (build_clip_atomic caption-burn) and
Script B (audit-shot-spec-compliance) use this same implementation to avoid
silent divergence.

Authority: CONTRACT-A-B-INTERFACE.md v1.0 (2026-05-21 auditor pre-build).
"""

import re
import string

_PUNCT_TABLE = str.maketrans({c: " " for c in string.punctuation + "¿¡«»“”‘’"})


def _normalize(text: str) -> set:
    """Lowercase, strip punctuation, collapse whitespace, return word set."""
    if not text:
        return set()
    t = text.lower().translate(_PUNCT_TABLE)
    t = re.sub(r"\s+", " ", t).strip()
    # filter empty + drop pure-numeric tokens? no — keep tokens since narration
    # may include numbers we want to verify ("hace años" vs "hace 5 años")
    return set(w for w in t.split() if w)


def jaccard_similarity(text_a: str, text_b: str) -> float:
    """Word-level Jaccard similarity, case-insensitive, ignoring punctuation.

    Per CONTRACT-A-B-INTERFACE.md § 3:
        words_a = set(text_a.lower().split())  # normalize: strip punctuation first
        words_b = set(text_b.lower().split())
        if not words_a and not words_b:
            return 1.0
        if not words_a or not words_b:
            return 0.0
        return len(words_a & words_b) / len(words_a | words_b)
    """
    words_a = _normalize(text_a)
    words_b = _normalize(text_b)
    if not words_a and not words_b:
        return 1.0
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def estimate_text_offset_s(
    whisper_segments: list,
    target_text: str,
    caption_appears_at_s: float | None = None,
) -> float | None:
    """Estimate timing offset between when narrator says target_text and when
    caption shows it. Returns offset_s = caption_time - narrator_first_token_time.

    Positive value → caption is LATE.
    Negative value → caption is EARLY.

    whisper_segments: list of {start, end, text} dicts from whisper.transcribe()
    target_text: SPEC text we expect captioned (also what we expect narrator to say)
    caption_appears_at_s: when (in clip-local time) the burned caption first appears
                         per Gemini Vision frame scan. If None → return None.

    Heuristic: find earliest whisper segment whose text shares ≥0.3 jaccard with
    first 3 words of target. That segment's .start is "narrator says it" time.
    """
    if caption_appears_at_s is None or not whisper_segments or not target_text:
        return None

    target_first3 = " ".join(target_text.split()[:3])
    best_start = None
    best_jac = 0.0
    for seg in whisper_segments:
        seg_text = seg.get("text", "")
        jac = jaccard_similarity(target_first3, seg_text)
        if jac > best_jac and jac >= 0.3:
            best_jac = jac
            best_start = seg.get("start", 0.0)
    if best_start is None:
        # fall back: first whisper segment with any speech
        if whisper_segments:
            best_start = whisper_segments[0].get("start", 0.0)
        else:
            return None

    return float(caption_appears_at_s) - float(best_start)
