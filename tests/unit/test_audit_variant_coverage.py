#!/usr/bin/env python3
"""test_audit-variant-coverage.py — HR#26 companion test for audit-variant-coverage.py (HR#5).

ANTI-THEATER: prueba que el validator CAZA el bug REAL (bosque-v2 PowerPoint-narrado:
1 PNG reusado en escena ~11s) y NO molesta en el caso bueno (11s con 3 variantes) ni
en shots cortos (3s con 1 variante → regla no aplica).

Cobertura:
  PURE evaluate_variant_coverage:
    (a) bosque-v2: 1 shot 11s / 1 variante → FAIL nombrando el shot.
    (b) bueno: 11s / 3 variantes → PASS.
    (c) corto: 3s / 1 variante → PASS (regla no aplica).
    (d) límite: 4.0s exacto / 1 variante → PASS (umbral es ESTRICTO >4.0).
  Runtime helpers: timestamp_intent_s vs duration_intent_s; conteo de variantes desde disco (-a/-b/-c).
  CLI por subprocess con fixtures tempfile:
    --format requerido; Bug#9 video_capabilities ausente; not_applicable; FAIL real; PASS con files -b/-c.

Runnable: python3 test_audit-variant-coverage.py  → imprime "OK: ..." o sys.exit(1).
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_variant_coverage.py"


def _load():
    spec = importlib.util.spec_from_file_location("variant_cov", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


M = _load()
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  ok: {msg}")


# ───────────────────────── PURE FUNCTION (the heart of the bug) ─────────────────────────
print("[pure] evaluate_variant_coverage")

# (a) bosque-v2: 1 shot 11s con 1 variante → FAIL, nombrando el shot.
ok, reasons = M.evaluate_variant_coverage([
    {"shot_id": "shot_bosque_long", "onscreen_s": 11.0, "n_variants": 1},
])
check(ok is False, "(a) bosque-v2 11s/1var → FAIL (PowerPoint-narrado cazado)")
fail_ids = [r["shot_id"] for r in reasons if r["status"] == "fail"]
check("shot_bosque_long" in fail_ids, "(a) FAIL nombra el shot ofensor (shot_bosque_long)")
check(any("PowerPoint" in r["detail"] for r in reasons if r["status"] == "fail"),
      "(a) razón cita riesgo PowerPoint-narrado")

# (b) bueno: 11s con 3 variantes → PASS.
ok, reasons = M.evaluate_variant_coverage([
    {"shot_id": "shot_ok_long", "onscreen_s": 11.0, "n_variants": 3},
])
check(ok is True, "(b) 11s/3var → PASS (no molesta el caso bueno)")
check(all(r["status"] == "ok" for r in reasons), "(b) sin fails en caso bueno")

# (c) shot corto 3s con 1 variante → PASS (regla no aplica).
ok, reasons = M.evaluate_variant_coverage([
    {"shot_id": "shot_short", "onscreen_s": 3.0, "n_variants": 1},
])
check(ok is True, "(c) 3s/1var → PASS (regla no aplica a ≤4s)")
check(reasons[0]["rule_applies"] is False, "(c) rule_applies=False en shot corto")

# (d) límite exacto 4.0s / 1 variante → PASS (umbral ESTRICTO >4.0).
ok, _ = M.evaluate_variant_coverage([{"shot_id": "shot_edge", "onscreen_s": 4.0, "n_variants": 1}])
check(ok is True, "(d) 4.0s exacto/1var → PASS (umbral es estricto >4.0)")
# y 4.01s con 1 variante → FAIL
ok, _ = M.evaluate_variant_coverage([{"shot_id": "shot_over", "onscreen_s": 4.01, "n_variants": 1}])
check(ok is False, "(d) 4.01s/1var → FAIL (apenas pasa el umbral)")

# Mixto: el bueno no enmascara al malo en el mismo SPEC.
ok, reasons = M.evaluate_variant_coverage([
    {"shot_id": "shot_good", "onscreen_s": 9.0, "n_variants": 3},
    {"shot_id": "shot_bad", "onscreen_s": 9.0, "n_variants": 1},
])
check(ok is False and [r["shot_id"] for r in reasons if r["status"] == "fail"] == ["shot_bad"],
      "(mix) un shot bueno no enmascara al malo")


# ───────────────────────── RUNTIME HELPERS ─────────────────────────
print("[runtime] shot_onscreen_seconds + count_variants")

check(M.shot_onscreen_seconds({"timestamp_intent_s": [16.0, 24.0]}) == 8.0,
      "onscreen desde timestamp_intent_s (end-start)")
check(M.shot_onscreen_seconds({"duration_intent_s": 6.0}) == 6.0,
      "onscreen fallback a duration_intent_s")
check(M.shot_onscreen_seconds({"timestamp_intent_s": [2.0, 5.0], "duration_intent_s": 99}) == 3.0,
      "timestamp_intent_s tiene prioridad sobre duration_intent_s")

# count_variants desde disco: base shot_07.png + shot_07-b.png = 2 variantes (caso sala-limpia real).
_tmp = tempfile.mkdtemp()
try:
    adir = Path(_tmp) / "clips"
    adir.mkdir()
    (adir / "shot_07.png").write_bytes(b"x")
    (adir / "shot_07-b.png").write_bytes(b"x")
    (adir / "shot_09.png").write_bytes(b"x")  # solo base → 1 variante
    check(M.count_variants({"shot_id": "shot_07"}, str(adir)) == 2,
          "count_variants: base + -b = 2 (desde disco)")
    check(M.count_variants({"shot_id": "shot_09"}, str(adir)) == 1,
          "count_variants: solo base = 1 (PowerPoint risk)")
    check(M.count_variants({"shot_id": "shot_07"}, None) == 0,
          "count_variants: sin assets_dir y sin declaración = 0")
    check(M.count_variants({"shot_id": "shot_09", "image_variants": ["wide", "close", "detail"]}, str(adir)) == 3,
          "count_variants: max(declarado SPEC=3, disco=1) = 3")
finally:
    shutil.rmtree(_tmp, ignore_errors=True)


# ───────────────────────── CLI (subprocess + fixtures) ─────────────────────────
print("[cli] subprocess paths")
tmp = tempfile.mkdtemp()
try:
    spec = Path(tmp) / "spec.yaml"

    def write_spec(body, *, has_clips=True, omit_caps=False):
        caps = "" if omit_caps else (
            "video_capabilities:\n"
            f"  has_ai_generated_clips: {str(has_clips).lower()}\n"
            '  format_type: "interactive_choice"\n'
        )
        spec.write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")

    # --format requerido.
    write_spec("shot_list: []\n")
    r = _run(["--spec", str(spec), "--dry-run"])
    check(r.returncode != 0 and "format" in r.stderr.lower(), "CLI: --format requerido (exit≠0)")

    # Bug #9: video_capabilities ausente → exit 2.
    write_spec("shot_list: []\n", omit_caps=True)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2, "CLI: video_capabilities ausente → Bug#9 exit 2")

    # not_applicable: has_ai_generated_clips=false → exit 0.
    write_spec("shot_list:\n  - shot_id: shot_01\n    duration_intent_s: 11.0\n", has_clips=False)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 0 and "not_applicable" in r.stdout.lower(),
          "CLI: has_ai_generated_clips=false → not_applicable exit 0")

    # FAIL real (bosque-v2): shot 11s, 1 variante declarada (image_variants=1), sin assets_dir.
    write_spec(
        "shot_list:\n"
        "  - shot_id: shot_03\n"
        "    duration_intent_s: 11.0\n"
        "    image_variants: 1\n"
    )
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 1, "CLI: 11s/1var → exit 1 (FAIL)")
    check("shot_03" in r.stdout and '"fail"' in r.stdout, "CLI: FAIL nombra shot_03")

    # PASS con archivos -b/-c en assets/clips: shot_03.png + -b + -c = 3 variantes.
    adir = Path(tmp) / "clips"
    adir.mkdir(exist_ok=True)
    for nm in ("shot_03.png", "shot_03-b.png", "shot_03-c.png"):
        (adir / nm).write_bytes(b"x")
    r = _run(["--format", "horror-choice", "--spec", str(spec), "--assets-dir", str(adir)])
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["overall_pass"] is True,
          "CLI: 11s con 3 archivos (-b/-c) en disco → PASS exit 0")

    # PASS: shot corto 3s con 1 variante (regla no aplica).
    write_spec("shot_list:\n  - shot_id: shot_short\n    duration_intent_s: 3.0\n    image_variants: 1\n")
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 0, "CLI: shot 3s/1var → PASS (regla no aplica)")
finally:
    shutil.rmtree(tmp, ignore_errors=True)


# ───────────────────────── INTEGRATION: real SPEC must parse without crash ─────────────────────────
print("[integration] real example SPEC parses")
real = Path(__file__).resolve().parents[2] / "examples/specs/sala-limpia-bioseguridad.yaml"
if real.exists():
    r = _run(["--format", "horror-choice", "--spec", str(real)])
    check("Traceback" not in r.stderr, "real SPEC: no crash")
    check(r.returncode in (0, 1), f"real SPEC: exit 0/1 (got {r.returncode})")
else:
    print("  (skip: real SPEC not present)")


# ───────────────────────── verdict ─────────────────────────
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("\nOK: audit-variant-coverage.py catches bosque-v2 PowerPoint-narrado bug; clean cases pass.")
