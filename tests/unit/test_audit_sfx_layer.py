#!/usr/bin/env python3
"""test_audit-sfx-layer.py — HR#26 companion test for audit-sfx-layer.py (HR#8).

ANTI-THEATER: prueba que el validator CAZA el bug REAL (matadero CP5 gap #13: SFX en
disco pero 0 wired → render sin capa SFX) y NO molesta en el caso bueno (≥1 SFX wired).

Cobertura:
  is_sfx_role: class sfx/flash → True; music/narration/ambient → False; nombre.
  PURE evaluate_sfx_layer:
    (a) matadero: 0 wired + 10 en disco → FAIL citando "existencia-en-disco ≠ wired".
    (b) 0 wired + 0 en disco → FAIL (no se generó nada).
    (c) bueno: ≥1 wired → PASS.
  Extractores runtime:
    manifest HYBRID (class sfx wired) + HTML LEGACY (track-index 60-110, excluye música) + disco.
  CLI por subprocess con fixtures tempfile:
    --format requerido; Bug#9; not_applicable; FAIL matadero (disco sin wiring);
    PASS (manifest con SFX); HTML legacy PASS/FAIL.

Runnable: python3 test_audit-sfx-layer.py  → imprime "OK: ..." o sys.exit(1).
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_sfx_layer.py"


def _load():
    spec = importlib.util.spec_from_file_location("sfx_layer", SCRIPT)
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


# ───────────────────────── is_sfx_role ─────────────────────────
print("[pure] is_sfx_role")
check(M.is_sfx_role(declared_class="sfx", name="footsteps") is True, "class=sfx → True")
check(M.is_sfx_role(declared_class="flash", name="flash_impact") is True, "class=flash → True")
check(M.is_sfx_role(declared_class="music", name="drone") is False, "class=music → False")
check(M.is_sfx_role(declared_class="narration", name="narr") is False, "class=narration → False")
check(M.is_sfx_role(declared_class="ambient", name="ambient_tunnel") is False,
      "class=ambient → False (no es capa SFX de eventos puntuales)")
# class declarado explícito GANA: si el ingeniero declaró class=sfx, es wiring intent.
# La heurística de nombre solo decide cuando NO hay class declarado.
check(M.is_sfx_role(declared_class="sfx", name="ambient_tunnel") is True,
      "class=sfx explícito GANA al nombre (declarado=wiring intent autoritativo)")
check(M.is_sfx_role(declared_class=None, name="ambient_tunnel") is False,
      "sin class declarado + nombre ambient → False (heurística decide)")


# ───────────────────────── PURE evaluate_sfx_layer (the heart of the bug) ─────────────────────────
print("[pure] evaluate_sfx_layer")

# (a) matadero gap #13: 0 wired pero 10 en disco → FAIL citando el gap.
ondisk = [f"sfx_{i}.mp3" for i in range(10)]
ok, reasons = M.evaluate_sfx_layer([], ondisk)
check(ok is False, "(a) matadero: 0 wired + 10 en disco → FAIL")
check(any("matadero" in r["detail"] or "disco" in r["detail"] for r in reasons),
      "(a) razón cita el gap disco-vs-wired (matadero)")
check(reasons[0]["ondisk_sfx_count"] == 10 and reasons[0]["wired_sfx_count"] == 0,
      "(a) report cuenta 10 en disco / 0 wired (evidencia del gap exacto)")

# (b) 0 wired + 0 en disco → FAIL (ni siquiera se generó).
ok, reasons = M.evaluate_sfx_layer([], [])
check(ok is False, "(b) 0 wired + 0 en disco → FAIL (nada generado ni wired)")

# (c) bueno: ≥1 wired → PASS (aunque haya más en disco huérfanos).
ok, reasons = M.evaluate_sfx_layer(["footsteps", "body_thud"], ondisk)
check(ok is True, "(c) 2 wired → PASS")
check(reasons[0]["status"] == "ok", "(c) status=ok")

# (c2) exactamente 1 wired (el mínimo) → PASS.
check(M.evaluate_sfx_layer(["only_one"], [])[0] is True, "(c2) exactamente 1 wired → PASS (min=1)")

# min_sfx override: exigir 3, con 2 wired → FAIL.
check(M.evaluate_sfx_layer(["a", "b"], [], min_sfx=3)[0] is False,
      "min_sfx=3 con 2 wired → FAIL")


# ───────────────────────── extractores runtime ─────────────────────────
print("[runtime] extract_wired_sfx_from_manifest + _from_html + list_ondisk_sfx")

# manifest HYBRID estilo ultimo-tren-carga: 33 sfx + 5 music + 2 ambient.
manifest = {"assets": (
    [{"id": f"sfx_{i}", "class": "sfx"} for i in range(33)]
    + [{"id": f"mus_{i}", "class": "music"} for i in range(5)]
    + [{"id": f"amb_{i}", "class": "ambient"} for i in range(2)]
)}
wired = M.extract_wired_sfx_from_manifest(manifest)
check(len(wired) == 33, f"manifest: 33 SFX wired (music+ambient excluidos), got {len(wired)}")

# manifest con flash (class sfx + name flash) cuenta como SFX wired.
wired = M.extract_wired_sfx_from_manifest({"assets": [{"id": "flash_electric_impact", "class": "sfx"}]})
check(len(wired) == 1, "manifest: flash (class sfx) cuenta como SFX wired")

# manifest SOLO con música → 0 SFX wired (caso matadero potencial).
wired = M.extract_wired_sfx_from_manifest({"assets": [{"id": "drone", "class": "music"}]})
check(len(wired) == 0, "manifest solo música → 0 SFX wired")

# HTML LEGACY: track-index 60-110 sí, fuera no, música excluida.
html = """
<audio id="narr" src="assets/tts/narr.mp3" data-track-index="10"></audio>
<audio id="music" src="assets/music/drone.mp3" data-track-index="40"></audio>
<audio id="fx1" src="assets/sfx/footsteps.mp3" data-track-index="72"></audio>
<audio id="fx2" src="assets/sfx/body_thud.mp3" data-track-index="80"></audio>
"""
hwired = M.extract_wired_sfx_from_html(html)
check(len(hwired) == 2, f"HTML: 2 SFX en banda 60-110 (narr@10 y music@40 excluidos), got {len(hwired)}")
check(any("footsteps" in w for w in hwired), "HTML: footsteps@72 wired")

# HTML con música EN la banda SFX (track 70) → excluida por nombre.
html_music_in_band = '<audio src="assets/music/score.mp3" data-track-index="70"></audio>'
check(len(M.extract_wired_sfx_from_html(html_music_in_band)) == 0,
      "HTML: música en banda 60-110 → excluida (no es SFX por nombre)")

# list_ondisk_sfx desde un dir tempfile.
_tmp = tempfile.mkdtemp()
try:
    sdir = Path(_tmp) / "sfx"
    sdir.mkdir()
    for nm in ("a.mp3", "b.wav", "c.png", "d.txt"):
        (sdir / nm).write_bytes(b"x")
    disk = M.list_ondisk_sfx(str(sdir))
    check(set(disk) == {"a.mp3", "b.wav"}, "list_ondisk_sfx: solo audio (mp3/wav), no png/txt")
    check(M.list_ondisk_sfx(None) == [], "list_ondisk_sfx(None) → []")
finally:
    shutil.rmtree(_tmp, ignore_errors=True)


# ───────────────────────── CLI (subprocess + fixtures) ─────────────────────────
print("[cli] subprocess paths")
tmp = tempfile.mkdtemp()
try:
    proj = Path(tmp) / "proj"
    (proj / "assets" / "sfx").mkdir(parents=True)
    specs_dir = Path(tmp) / "creative-specs"
    specs_dir.mkdir()
    spec = specs_dir / "proj.yaml"

    def write_spec(*, has_sfx=True, omit_caps=False):
        caps = "" if omit_caps else (
            "video_capabilities:\n"
            f"  has_sfx_layer: {str(has_sfx).lower()}\n"
            '  format_type: "interactive_choice"\n'
        )
        spec.write_text(f'schema_version: "v11.1"\n{caps}', encoding="utf-8")

    def write_manifest(items):
        (proj / "assets" / "audio-manifest.json").write_text(
            json.dumps({"assets": items}), encoding="utf-8")

    def put_disk_sfx(names):
        sdir = proj / "assets" / "sfx"
        for f in sdir.iterdir():
            f.unlink()
        for nm in names:
            (sdir / nm).write_bytes(b"x")

    # --format requerido.
    write_spec()
    r = _run(["--spec", str(spec), "--dry-run"])
    check(r.returncode != 0 and "format" in r.stderr.lower(), "CLI: --format requerido")

    # Bug #9: video_capabilities ausente → exit 2.
    write_spec(omit_caps=True)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2, "CLI: video_capabilities ausente → Bug#9 exit 2")

    # not_applicable: has_sfx_layer=false → exit 0.
    write_spec(has_sfx=False)
    write_manifest([{"id": "drone", "class": "music"}])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 0 and "not_applicable" in r.stdout.lower(),
          "CLI: has_sfx_layer=false → not_applicable exit 0")

    # FAIL MATADERO: 10 SFX en disco, manifest SIN ninguna clase sfx → 0 wired.
    write_spec()
    write_manifest([{"id": "drone", "class": "music"}, {"id": "amb", "class": "ambient"}])
    put_disk_sfx([f"sfx_{i}.mp3" for i in range(10)])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 1, "CLI MATADERO: 10 en disco / 0 wired → exit 1 (FAIL)")
    payload = json.loads(r.stdout)
    check(payload["wired_sfx_count"] == 0 and payload["ondisk_sfx_count"] == 10,
          "CLI MATADERO: report 0 wired / 10 en disco (gap exacto)")
    check(any("disco" in rr["detail"] for rr in payload["reasons"]),
          "CLI MATADERO: razón cita el gap disco-vs-wired")

    # PASS: manifest CON SFX wired (aunque queden huérfanos en disco también).
    write_manifest([
        {"id": "footsteps_wet_concrete", "class": "sfx"},
        {"id": "body_thrown_back_thud", "class": "sfx"},
        {"id": "drone", "class": "music"},
    ])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["overall_pass"] is True and payload["wired_sfx_count"] == 2,
          "CLI: 2 SFX wired en manifest → PASS exit 0")

    # PASS via HTML LEGACY: borrar manifest, crear index.html con SFX en banda 60-110.
    (proj / "assets" / "audio-manifest.json").unlink()
    (proj / "index.html").write_text(
        '<audio src="assets/sfx/footsteps.mp3" data-track-index="72"></audio>'
        '<audio src="assets/music/drone.mp3" data-track-index="40"></audio>',
        encoding="utf-8")
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["wired_sfx_count"] == 1,
          "CLI LEGACY: 1 SFX en banda 60-110 en HTML → PASS")

    # FAIL via HTML LEGACY: index.html SIN ningún track en banda 60-110 + 5 en disco.
    (proj / "index.html").write_text(
        '<audio src="assets/music/drone.mp3" data-track-index="40"></audio>',
        encoding="utf-8")
    put_disk_sfx([f"orphan_{i}.mp3" for i in range(5)])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 1, "CLI LEGACY MATADERO: 0 SFX wired en HTML + 5 en disco → exit 1")

    # cant_measure: ni manifest ni html → exit 2.
    (proj / "index.html").unlink()
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2 and "cant_measure" in r.stdout,
          "CLI: sin manifest ni html → exit 2 cant_measure")
finally:
    shutil.rmtree(tmp, ignore_errors=True)


# ───────────────────────── INTEGRATION: real ultimo-tren-carga ─────────────────────────
print("[integration] real ultimo-tren-carga SPEC + manifest parse")
real = Path(__file__).resolve().parents[2] / "examples/specs/ultimo-tren-carga.yaml"
if real.exists():
    r = _run(["--format", "horror-choice", "--spec", str(real)])
    check("Traceback" not in r.stderr, "real SPEC: no crash")
    check(r.returncode in (0, 1, 2), f"real SPEC: exit válido (got {r.returncode})")
else:
    print("  (skip: real SPEC not present)")


# ───────────────────────── verdict ─────────────────────────
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("\nOK: audit-sfx-layer.py catches matadero gap #13 (SFX en disco / 0 wired); ≥1 wired passes.")
