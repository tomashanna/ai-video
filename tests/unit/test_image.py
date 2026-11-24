#!/usr/bin/env python3
"""Companion test (HR#26) para image.py — caza el regreso del HORROR_SUFFIX como default
(Capa A debe ser AGNÓSTICA). Corre con un venv que tenga google-genai."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
from ai_video.providers import image as I


def test_default_agnostic():
    assert I.STYLE_SUFFIX == "", f"STYLE_SUFFIX default debe ser vacío (agnóstico), es {I.STYLE_SUFFIX!r}"
    assert I.resolve_style_suffix(False, None) == "", "default (sin flags) aplica suffix — debe ser agnóstico"


def test_style_suffix_override():
    assert I.resolve_style_suffix(False, " mi estilo") == " mi estilo", "--style-suffix no se aplica"


def test_no_mono_forces_empty():
    assert I.resolve_style_suffix(True, " x") == "", "--no-mono-suffix no fuerza vacío"


def test_horror_suffix_preserved():
    assert "horror" in I.HORROR_SUFFIX.lower() and len(I.HORROR_SUFFIX) > 50, "HORROR_SUFFIX se perdió"


def main():
    test_default_agnostic()
    test_style_suffix_override()
    test_no_mono_forces_empty()
    test_horror_suffix_preserved()
    print("OK: test_image.py (STYLE_SUFFIX agnóstico + HORROR preservado — 4 checks)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
