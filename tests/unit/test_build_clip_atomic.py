#!/usr/bin/env python3
"""Companion test (HR#26) para build_clip_atomic.py — caza el regreso del bug V5/V6
(caption colapsado a 1 cue estático). Corre con un venv que tenga las deps del módulo."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
from ai_video.build import build_clip_atomic as B


def _fake_whisper(n_words, total_s):
    step = total_s / n_words
    words = [
        {"word": f"w{i}", "start": round(i * step, 3), "end": round((i + 1) * step, 3)}
        for i in range(n_words)
    ]
    return {
        "words": words,
        "segments": [
            {"start": 0.0, "end": total_s, "text": " ".join(w["word"] for w in words), "words": words}
        ],
    }


def test_spec_override_chunks_not_single():
    spec = " ".join(f"palabra{i}" for i in range(28))  # 28 palabras / ~9s
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


def test_retime_canonical_exact_count_keeps_per_word_timing():
    """Conteo igual → override POSICIONAL 1:1 con timing EXACTO (no bucketed)."""
    whisper = _fake_whisper(3, 3.0)["words"]  # starts 0.0/1.0/2.0
    retimed = B.retime_canonical("uno dos tres", whisper)
    assert [w["word"] for w in retimed] == ["uno", "dos", "tres"], "texto canónico no se aplicó"
    for r, w in zip(retimed, whisper):
        assert r["start"] == w["start"] and r["end"] == w["end"], "no preservó timing exacto Whisper 1:1"


def test_retime_canonical_overrides_mistranscription():
    """Whisper mis-transcribe ('a Dario'→'adario') pero el caption muestra el texto CANÓNICO del SPEC,
    conservando los timestamps Whisper (HR#30 nivel B spec_text_override_with_whisper_timing)."""
    whisper = [
        {"word": "elige", "start": 0.0, "end": 0.4},
        {"word": "adario", "start": 0.4, "end": 0.9},  # mis-transcripción pegada
        {"word": "otobias", "start": 0.9, "end": 1.4},
    ]
    canon = "Elige a Dario o Tobias"  # 5 tokens vs 3 Whisper
    retimed = B.retime_canonical(canon, whisper)
    assert [w["word"] for w in retimed] == canon.split(), "no usó el wording canónico del SPEC"
    assert retimed[0]["start"] == 0.0 and retimed[-1]["end"] <= 1.4 + 1e-6, "timing fuera del span Whisper"
    for a, b in zip(retimed, retimed[1:]):
        assert b["start"] >= a["start"] - 1e-9, "starts no monótonos tras el mapeo proporcional"


def test_v11_real_schema_narrator_hook_full_coverage():
    """Caso con datos REALES estilo v11 (ultimo-tren-carga narrator_hook): el burn cubre TODA la
    narración del SPEC en cues progresivos (no colapsa al 1er fragmento — bug V5/V6)."""
    # text_canonical real del SPEC v11 (creative-specs/ultimo-tren-carga.yaml narrator_hook)
    spec_text = "El último tren ya pasó. Elige a tu compañero: ¿Dario o Tobías?"
    cues = B._build_caption_cues_from_whisper(_fake_whisper(13, 3.0), spec_text, "narrator")
    joined = " ".join(c["text"] for c in cues).split()
    assert joined == spec_text.split(), f"texto del SPEC perdido/duplicado al chunkear: {joined}"
    assert len(cues) >= 2, "narración real colapsó a 1 cue estático (regresión V5/V6)"
    assert all((c["end_s"] - c["start_s"]) <= 4.0 for c in cues), "cue >4s (riesgo bloque estático)"


def test_voice_exclusivity_shifts_dialog_off_narrator():
    """Narrador y personaje colisionan en un clip → el diálogo (menor prioridad) cede ≤1s; ambos quedan
    separados por ≥VOICE_BUFFER_FLOOR_S, ninguno sale del clip."""
    srcs = [
        {"label": "narr", "offset_s": 0.0, "dur_s": 1.5, "is_voice": True, "speaker": "narrator"},
        {"label": "dario", "offset_s": 1.0, "dur_s": 1.0, "is_voice": True, "speaker": "char_a"},
        {"label": "sfx", "offset_s": 0.5, "dur_s": 0.4, "is_voice": False, "speaker": None},
    ]
    B.assert_voice_exclusivity_in_clip(srcs, clip_dur=5.0)
    narr = next(s for s in srcs if s["label"] == "narr")
    dario = next(s for s in srcs if s["label"] == "dario")
    gap = dario["offset_s"] - (narr["offset_s"] + narr["dur_s"])
    assert gap >= B.VOICE_BUFFER_FLOOR_S - 1e-6, f"voces no deconflictadas (gap {gap:.3f}s)"
    assert dario["offset_s"] + dario["dur_s"] <= 5.0 + 1e-6, "diálogo empujado fuera del clip"


def test_voice_exclusivity_aborts_when_unfittable():
    """Si no entra en ±1s dentro del clip → SystemExit (NUNCA shift silencioso >1s)."""
    srcs = [
        {"label": "narr", "offset_s": 0.0, "dur_s": 2.0, "is_voice": True, "speaker": "narrator"},
        {"label": "dario", "offset_s": 0.0, "dur_s": 2.0, "is_voice": True, "speaker": "char_a"},
    ]
    try:
        B.assert_voice_exclusivity_in_clip(srcs, clip_dur=2.1)  # no hay 0.3s de buffer disponible
    except SystemExit:
        return
    raise AssertionError("debió abortar (no se puede deconflictar dentro del clip por ≤1s)")


def test_sfx_norm_gain_quiet_source_boosted_vs_loud_attenuated(monkeypatch=None):
    """sfx_norm_gain lleva a target de CLASE en dBFS ABSOLUTO: una fuente muerta (-67 dB) se sube,
    una fuerte (-10 dB) se baja — NO un multiplicador plano sobre el raw (fix de audibilidad)."""
    saved = dict(B._SFX_MEAN_CACHE)
    try:
        B._SFX_MEAN_CACHE["/q"] = -67.0  # fuente cuasi-muda
        B._SFX_MEAN_CACHE["/l"] = -10.0  # fuente fuerte
        quiet = B.sfx_norm_gain("/q", "event")  # target -19 dBFS → debe AMPLIFICAR (>1.0)
        loud = B.sfx_norm_gain("/l", "event")  # target -19 dBFS → debe ATENUAR (<1.0)
        assert quiet > 1.0 > loud, f"per-clase no normaliza (quiet={quiet:.2f}, loud={loud:.2f})"
        # rel_scale duckea dentro de la clase
        assert B.sfx_norm_gain("/q", "event", rel_scale=0.5) < quiet, "rel_scale no duckea within-class"
    finally:
        B._SFX_MEAN_CACHE.clear()
        B._SFX_MEAN_CACHE.update(saved)


def main():
    test_spec_override_chunks_not_single()
    test_span_fallback_chunks()
    test_short_text_single_cue_ok()
    test_retime_canonical_exact_count_keeps_per_word_timing()
    test_retime_canonical_overrides_mistranscription()
    test_v11_real_schema_narrator_hook_full_coverage()
    test_voice_exclusivity_shifts_dialog_off_narrator()
    test_voice_exclusivity_aborts_when_unfittable()
    test_sfx_norm_gain_quiet_source_boosted_vs_loud_attenuated()
    print(
        "OK: test_build_clip_atomic.py (caption chunking + retime_canonical + voice-exclusivity "
        "+ sfx-audibility — 9 checks)"
    )


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
