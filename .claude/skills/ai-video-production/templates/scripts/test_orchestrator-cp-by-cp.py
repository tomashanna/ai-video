#!/usr/bin/env python3
"""Companion test (HR#26) para orchestrator-cp-by-cp.py — el script más safety-critical (HR#24)
cuyo docstring afirmaba "17 tests" que NO existían. Testea el gate de prompt-scope adversarial
(--validate-engineer-prompt) end-to-end vía subprocess, incluyendo el bypass ES (fix Wave 1).
Corre: python3 test_orchestrator-cp-by-cp.py"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "orchestrator-cp-by-cp.py"


def _validate(prompt):
    r = subprocess.run([sys.executable, str(SCRIPT), "--validate-engineer-prompt", prompt],
                       capture_output=True, text=True)
    return r.returncode


def test_forbidden_en_halts():
    assert _validate("execute CP1-CP5 todo de una") != 0, "prompt EN forbidden no HALTea"


def test_forbidden_es_halts():
    # bypass ES que ANTES pasaba limpio (fix Wave 1: FORBIDDEN_PHRASES + ES)
    assert _validate("ejecuta todos los checkpoints de corrido sin parar") != 0, \
        "bypass ES 'de corrido / sin parar' no HALTea"
    assert _validate("hazlo autónomo de punta a punta") != 0, \
        "bypass ES 'autónomo / de punta a punta' no HALTea"


def test_clean_prompt_ok():
    assert _validate("Genera el anchor del personaje para CP1, un plano frontal close-up.") == 0, \
        "prompt single-CP legítimo HALTea (falso positivo)"


def main():
    test_forbidden_en_halts()
    test_forbidden_es_halts()
    test_clean_prompt_ok()
    print("OK: test_orchestrator-cp-by-cp.py (prompt-scope gate HR#24, EN+ES — 3 checks)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
