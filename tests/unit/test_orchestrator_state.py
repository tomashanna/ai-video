#!/usr/bin/env python3
"""Companion test (HR#26) para lib/orchestrator_state.py —
parse_verdict (vocab emoji GO/NO-GO de AUDITOR-PROTOCOL §5) + detect_multi_cp_prompt (bypass ES).
Corre: python3 lib/test_orchestrator_state.py"""

import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
from ai_video.core import orchestrator_state as O


def _verdict(text):
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(text)
        p = f.name
    return O.parse_verdict(Path(p))


def test_emoji_verdicts():
    assert _verdict("# Audit\n\n🔴 NO-GO\n") == "FAIL", "emoji 🔴 NO-GO no mapea a FAIL"
    assert _verdict("🟢 GO incondicional") == "PASS", "🟢 GO no mapea a PASS"
    assert _verdict("⛔ ESCALAR") == "ESCALATE", "⛔ ESCALAR no mapea a ESCALATE"
    assert _verdict("Verdict: 🔴 NO-GO") == "FAIL", "verdict-line con emoji NO-GO falla"
    # formas legacy siguen andando
    assert _verdict("**Verdict**: PASS") == "PASS", "forma legacy PASS rota"
    assert _verdict("verdict: FAIL") == "FAIL", "forma legacy FAIL rota"
    assert _verdict("sin nada") == "UNKNOWN", "texto sin verdict debería ser UNKNOWN"


def test_prompt_scope_es_bypass():
    assert O.detect_multi_cp_prompt("ejecuta todos los checkpoints de corrido sin parar"), (
        "bypass ES 'de corrido / sin parar' no detectado"
    )
    assert O.detect_multi_cp_prompt("hazlo autónomo de punta a punta"), (
        "bypass ES 'autónomo / de punta a punta' no detectado"
    )
    assert O.detect_multi_cp_prompt("corré todo sin auditar"), (
        "bypass ES 'corré todo / sin auditar' no detectado"
    )
    assert O.detect_multi_cp_prompt("execute cp1-cp5"), "EN literal dejó de detectar (regresión)"
    assert O.detect_multi_cp_prompt("generá el anchor del CP1 nomás") is None, (
        "falso positivo en prompt single-CP legítimo"
    )


def main():
    test_emoji_verdicts()
    test_prompt_scope_es_bypass()
    print("OK: lib/test_orchestrator_state.py (parse_verdict emoji §5 + bypass ES — 2 grupos)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
