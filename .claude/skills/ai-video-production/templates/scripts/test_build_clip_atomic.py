#!/usr/bin/env python3
"""Companion test (HR#26) para build_clip_atomic.py — caza el regreso del bug V5/V6
(caption colapsado a 1 cue estático). Corre con un venv que tenga las deps del módulo."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_clip_atomic as B  # noqa: E402


def _fake_whisper(n_words, total_s):
    step = total_s / n_words
    words = [
        {"word": f"w{i}", "start": round(i * step, 3), "end": round((i + 1) * step, 3)}
        for i in range(n_words)
    ]
    return {"words": words,
            "segments": [{"start": 0.0, "end": total_s,
                          "text": " ".join(w["word"] for w in words), "words": words}]}


def test_spec_override_chunks_not_single():
    spec = " ".join(f"palabra{i}" for i in range(28))   # 28 palabras / ~9s
    cues = B._build_caption_cues_from_whisper(_fake_whisper(30, 9.0), spec, "NARRATOR")
    assert len(cues) >= 4, f"colapso V5/V6: {len(cues)} cue(s) para 28 palabras (esperado >=4)"
    assert " ".join(c["text"] for c in cues).split() == spec.split(), "texto perdido/duplicado al chunkear"
    for a, b in zip(cues, cues[1:]):
        assert b["start_s"] >= a["start_s"], "timestamps no monotónicos"
    assert cues[0]["start_s"] >= 0 and cues[-1]["end_s"] <= 9.5, "fuera del span"
    assert all((c["end_s"] - c["start_s"]) <= 4.0 for c in cues), "cue >4s (riesgo bloque estático)"


def test_span_fallback_chunks():
    spec = " ".join(f"x{i}" for i in range(20))
    cues = B._chunk_text_over_span(spec, 0.0, 6.0, None)
    assert len(cues) >= 3, f"span fallback colapsó a {len(cues)} cue(s)"
    assert " ".join(c["text"] for c in cues).split() == spec.split()


def test_short_text_single_cue_ok():
    cues = B._build_caption_cues_from_whisper(_fake_whisper(3, 1.5), "tres palabras solas", None)
    assert len(cues) == 1 and cues[0]["text"] == "tres palabras solas", "texto corto no debería fragmentarse"


def main():
    test_spec_override_chunks_not_single()
    test_span_fallback_chunks()
    test_short_text_single_cue_ok()
    print("OK: test_build_clip_atomic.py (caption chunking HR#30 — 3 checks)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
