#!/usr/bin/env python3
"""Companion test (HR#26) para tts.py — caza el regreso de la voz DEPRECATED como default.
NO importa tts.py (evita requerir elevenlabs): parsea el source. Corre: python3 test_tts.py"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPRECATED = "Tj9l48J9AJbry5yCP5eW"


def _find_catalog():
    for p in [HERE, *HERE.parents]:
        c = p / "library" / "voices-catalog.json"
        if c.exists():
            return c
    return None


def test_default_voice_not_deprecated():
    src = (HERE / "tts.py").read_text(encoding="utf-8")
    m = re.search(r'^DEFAULT_VOICE_ID\s*=\s*["\']([^"\']+)["\']', src, re.M)
    assert m, "no se encontró DEFAULT_VOICE_ID en tts.py"
    vid = m.group(1)
    assert vid != DEPRECATED, f"DEFAULT_VOICE_ID es la voz DEPRECATED {DEPRECATED} (bug live)"
    return vid


def test_default_matches_catalog(vid):
    cat = _find_catalog()
    if not cat:
        print("  (voices-catalog.json no encontrado — skip match check)")
        return
    d = json.loads(cat.read_text(encoding="utf-8"))
    if "default_voice" in d:
        assert vid == d["default_voice"], f"DEFAULT_VOICE_ID {vid} != catalog default_voice {d['default_voice']}"
    dep = d.get("default_voice_DEPRECATED_2026_05_18")
    if dep:
        assert vid != dep, f"DEFAULT_VOICE_ID == catalog deprecated {dep}"


def main():
    vid = test_default_voice_not_deprecated()
    test_default_matches_catalog(vid)
    print(f"OK: test_tts.py (DEFAULT_VOICE_ID={vid} — no deprecada, matchea catalog)")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"FAIL: {e}")
        sys.exit(1)
