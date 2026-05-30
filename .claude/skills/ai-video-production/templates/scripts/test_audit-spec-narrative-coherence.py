"""test_audit-spec-narrative-coherence.py — adversarial tests for BUILD 4 (PRE-4.J post-shakedown).

Per Hard Rule #26: companion test sidecar. TDD: written FIRST (RED).

17 tests covering (consequence-framing re-grounded in PRIMARY SOURCE 2026-05-29 — pattern_class 2/5):
- CLI/agnostic/capability (3): --format required, arbitrary format → not_applicable, Bug #9 caps missing
- Structure validation (9): clean PASS, invalid cliffhanger pattern, consequence without marker
  FLAG (not fail — branch may be caption-marked), synthetic "Si elegiste A" bare-label FAIL,
  choice-reference variant ("Si decides/escogiste") PASS, hook countdown not last, dilema placement
  out of band, counterfactual retrospective, WPM out of band
- Cross-video uniqueness (4): location exact-match FAIL, signature semantic ≥block FAIL,
  signature in [flag, block) FLAG, pattern rotation repeat last video FAIL
- Anti-cliché (1): forbidden phrase in SPEC → FAIL

Library: sentence-transformers + paraphrase-multilingual-MiniLM-L12-v2 (lazy-loaded in script;
CLI/structure/anti-cliché tests don't load the model). Semantic tests trigger model load (~3-5s
cached, ~30-60s first download).

NO heavy py deps in tests (no numpy/whisper). Synthetic SPEC + synthetic video-log MD parsed by script.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-narrative-coherence.py"

CLEAN_SHOT_LIST_YAML = """shot_list:
  - shot_id: shot_01
    beat_role: hook
    duration_intent_s: 2.7
    narration_in_this_shot:
      narrator_text: "Aterrizaje nocturno con dos dilemas en cuatro horas"
  - shot_id: shot_02
    beat_role: setup
    duration_intent_s: 3.0
    narration_in_this_shot:
      narrator_text: "Hay dos figuras esperándote en la torre del control"
  - shot_id: shot_03
    beat_role: decision_question
    duration_intent_s: 2.5
    narration_in_this_shot:
      narrator_text: "Cuál eliges para abrir la puerta principal del lugar"
  - shot_id: shot_04
    beat_role: consequence_A
    duration_intent_s: 4.0
    narration_in_this_shot:
      narrator_text: "Si enciendes la linterna, Bruno te arrastra al pozo y caes"
  - shot_id: shot_05
    beat_role: consequence_B
    duration_intent_s: 4.0
    narration_in_this_shot:
      narrator_text: "Si esperas, Bruno saca el medidor y la pantalla parpadea en rojo"
  - shot_id: shot_06
    beat_role: cliffhanger
    duration_intent_s: 3.0
    narration_in_this_shot:
      narrator_text: "Una noche en paz antes del primer dilema verdadero"
"""


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _build_spec(path, *, location="torre control aeropuerto abandonado nocturno",
                signature_staging="controlador encapuchado en torre de control con radares parpadeantes",
                cliffhanger="P3", hook_beats=("name_label", "setting", "narrator_framing", "push_in", "countdown"),
                dilema_pct=18, counterfactual="twin_end", shot_list_yaml=CLEAN_SHOT_LIST_YAML,
                format_type="interactive_choice", omit_caps=False,
                extra_narration_for_anticliche=None):
    """Write a synthetic SPEC with controllable fields."""
    caps = "" if omit_caps else (
        "video_capabilities:\n"
        f'  format_type: "{format_type}"\n'
        "  has_layer_2_effects: true\n"
        "  has_layer_3_music: true\n"
        "  has_layer_4_ui: true\n"
        '  audio_mix_target: "lufs_-14"\n'
    )
    hook_yaml = "\n".join(f"    - {b}" for b in hook_beats)
    extra = f"extra_text: \"{extra_narration_for_anticliche}\"\n" if extra_narration_for_anticliche else ""
    content = f"""schema_version: "v11.1"
{caps}location: "{location}"
signature_staging: "{signature_staging}"
narrative_structure:
  cliffhanger_archetype: "{cliffhanger}"
  hook_sub_beats:
{hook_yaml}
  dilema_placement_pct: {dilema_pct}
  counterfactual_placement: "{counterfactual}"
{extra}{shot_list_yaml}
"""
    Path(path).write_text(content, encoding="utf-8")


def _build_videolog(path, rows):
    """Write a synthetic video-log with the cross-video uniqueness table.
    rows: list of dicts with num, project, location, signature_staging, confidence."""
    header = "# video-log (synthetic test fixture)\n\n## Cross-video uniqueness fields\n\n"
    table = "| # | Proyecto | location | signature_staging | Confidence |\n"
    table += "|---|---|---|---|---|\n"
    for r in rows:
        table += (f"| {r['num']} | {r['project']} | {r['location']} | "
                  f"{r['signature_staging']} | {r.get('confidence', 'HIGH')} |\n")
    # Tabla maestra with cliffhanger pattern column (for rotation check)
    table += "\n## Tabla maestra (for rotation)\n\n"
    table += "| # | Proyecto | Pattern |\n|---|---|---|\n"
    for r in rows:
        table += f"| {r['num']} | {r['project']} | {r.get('pattern', 'P?')} |\n"
    Path(path).write_text(header + table, encoding="utf-8")


def _build_anticliche(path, phrases):
    Path(path).write_text("\n".join(phrases) + "\n", encoding="utf-8")


PRIOR_ROWS = [
    {"num": 7, "project": "matadero-banquete v1", "pattern": "P6",
     "location": "matadero refrigerado -30°C turno noche 2-6 AM",
     "signature_staging": "matarife casco-cuchillo en patio matadero con cocinera entre carcasas hanging"},
    {"num": 6, "project": "isla-faro v1", "pattern": "P6",
     "location": "isla con faro abandonado",
     "signature_staging": "aislamiento en isla con faro como punto de elección entre dos figuras"},
]


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.vlog = Path(self.tmp) / "vlog.md"
        _build_spec(self.spec)
        _build_videolog(self.vlog, PRIOR_ROWS)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invocation_without_format_exits_nonzero(self):
        r = _run(["--spec", str(self.spec), "--video-log", str(self.vlog), "--dry-run"])
        self.assertNotEqual(r.returncode, 0, f"stderr: {r.stderr}")
        self.assertIn("format", r.stderr.lower())

    def test_arbitrary_format_not_applicable(self):
        _build_spec(self.spec, format_type="tutorial")
        r = _run(["--format", "tutorial-stub", "--spec", str(self.spec),
                  "--video-log", str(self.vlog)])
        self.assertEqual(r.returncode, 0, f"stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("not_applicable", r.stdout.lower(),
                      "Non-interactive-choice format must report not_applicable")

    def test_bug9_video_capabilities_missing(self):
        _build_spec(self.spec, omit_caps=True)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog)])
        self.assertEqual(r.returncode, 2, f"Expected Bug #9 exit 2. stderr: {r.stderr}")


class TestStructure(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.vlog = Path(self.tmp) / "vlog.md"
        _build_videolog(self.vlog, PRIOR_ROWS)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _run_clean(self, **overrides):
        _build_spec(self.spec, **overrides)
        return _run(["--format", "horror-choice", "--spec", str(self.spec),
                     "--video-log", str(self.vlog), "--skip-semantic"])

    def test_clean_spec_passes_structure(self):
        r = self._run_clean()
        self.assertEqual(r.returncode, 0, f"Clean SPEC must pass.\nstdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("overall_pass", r.stdout)

    def test_invalid_cliffhanger_pattern_fails(self):
        r = self._run_clean(cliffhanger="P4")  # P4 deprecated per GAP #10
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("cliffhanger", r.stdout.lower() + r.stderr.lower())

    def test_consequence_without_conditional_framing_flags(self):
        # No "Si [acción]" marker → FLAG (exit 0), NOT fail: branch may be marked via bridge caption.
        # Principle enforced (branch must be marked) but specific phrasing NOT forced (pattern_class 3/5).
        bad_shot_list = CLEAN_SHOT_LIST_YAML.replace(
            'narrator_text: "Si enciendes la linterna, Bruno te arrastra al pozo y caes"',
            'narrator_text: "La luz se apaga y la torre tiembla"'  # no detectable marker
        )
        r = self._run_clean(shot_list_yaml=bad_shot_list)
        self.assertEqual(r.returncode, 0, f"missing marker must FLAG (exit 0) not FAIL.\nstdout {r.stdout}")
        self.assertIn("flag", r.stdout.lower())
        self.assertIn("framing", r.stdout.lower())

    def test_synthetic_si_elegiste_label_fails(self):
        # Bare synthetic label "Si elegiste A" (0/8 primary source) → FAIL post-fix.
        # This is the exact form the deprecated "Si elegiste X" rule wrongly REQUIRED.
        bad_shot_list = CLEAN_SHOT_LIST_YAML.replace(
            'narrator_text: "Si enciendes la linterna, Bruno te arrastra al pozo y caes"',
            'narrator_text: "Si elegiste A, la luz se apaga y la torre tiembla"'
        )
        r = self._run_clean(shot_list_yaml=bad_shot_list)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("framing", r.stdout.lower() + r.stderr.lower())

    def test_choice_reference_variant_passes(self):
        # @referent-b variant "Si decides..." / "Si escogiste..." (2/8 primary source) → PASS
        variant = CLEAN_SHOT_LIST_YAML.replace(
            'narrator_text: "Si enciendes la linterna, Bruno te arrastra al pozo y caes"',
            'narrator_text: "Si decides comer la fruta, la mesa entera se desploma sobre ti"'
        ).replace(
            'narrator_text: "Si esperas, Bruno saca el medidor y la pantalla parpadea en rojo"',
            'narrator_text: "Si escogiste no tocarla, Teresa guarda el plato y se aleja"'
        )
        r = self._run_clean(shot_list_yaml=variant)
        self.assertEqual(r.returncode, 0, f"choice-reference variant must pass.\nstdout {r.stdout}")

    def test_hook_countdown_not_last_fails(self):
        r = self._run_clean(hook_beats=("countdown", "name_label", "setting", "narrator_framing", "push_in"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("hook", r.stdout.lower() + r.stderr.lower())

    def test_dilema_placement_out_of_band_fails(self):
        r = self._run_clean(dilema_pct=4)  # too early
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("dilema", r.stdout.lower() + r.stderr.lower())

    def test_counterfactual_retrospective_fails(self):
        r = self._run_clean(counterfactual="retrospective")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("counterfactual", r.stdout.lower() + r.stderr.lower())

    def test_wpm_out_of_band_fails(self):
        # Insert a shot with extremely high WPM: 20 words / 1.0s = 1200 WPM
        bad_shot_list = CLEAN_SHOT_LIST_YAML + """  - shot_id: shot_99
    beat_role: setup
    duration_intent_s: 1.0
    narration_in_this_shot:
      narrator_text: "uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete dieciocho diecinueve veinte"
"""
        r = self._run_clean(shot_list_yaml=bad_shot_list)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("wpm", r.stdout.lower() + r.stderr.lower())


class TestCrossVideoUniqueness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.vlog = Path(self.tmp) / "vlog.md"
        _build_videolog(self.vlog, PRIOR_ROWS)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_location_exact_match_fails(self):
        _build_spec(self.spec, location="matadero refrigerado -30°C turno noche 2-6 AM")  # exact match #7
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog), "--skip-semantic"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("location", r.stdout.lower() + r.stderr.lower())

    def test_signature_staging_semantic_block(self):
        # V5 signature = EXACT same as prior #7 → similarity ~1.0 ≥ block threshold
        _build_spec(self.spec,
                    location="laboratorio aislado submarino nocturno",  # unique location
                    signature_staging="matarife casco-cuchillo en patio matadero con cocinera entre carcasas hanging")
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog), "--block-threshold", "0.85",
                  "--flag-threshold", "0.75"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("signature", r.stdout.lower() + r.stderr.lower())

    def test_signature_staging_semantic_flag(self):
        # Configure thresholds so that a moderately-similar text lands in [flag, block) band
        # → emits warning but exit 0 (FLAG, not FAIL)
        _build_spec(self.spec,
                    location="laboratorio aislado submarino nocturno",
                    signature_staging="cocinera oculta entre las carcasas colgantes del matadero refrigerado")
        # use very loose flag (0.30) and very high block (0.999) → similar-but-not-identical lands FLAG
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog), "--block-threshold", "0.999",
                  "--flag-threshold", "0.30"])
        # FLAG = exit 0 with warning in stdout
        self.assertEqual(r.returncode, 0,
                         f"FLAG band should exit 0 with warning. stdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn("flag", r.stdout.lower(),
                      "FLAG verdict must appear in stdout")

    def test_pattern_rotation_repeat_last_fails(self):
        # Most recent prior is #7 P6 → V5 with P6 should fail rotation
        _build_spec(self.spec, cliffhanger="P6",
                    location="catedral inundada amanecer brumoso",  # unique
                    signature_staging="dos sacerdotes esperando en catedral inundada con velas flotando")
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog), "--skip-semantic"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("rotation", r.stdout.lower() + r.stderr.lower())


class TestAntiCliche(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"
        self.vlog = Path(self.tmp) / "vlog.md"
        self.anticliche = Path(self.tmp) / "anticliche.txt"
        _build_videolog(self.vlog, PRIOR_ROWS)
        _build_anticliche(self.anticliche, [
            "te conviertes en cena",
            "cena que nunca acaba",
            "bucle eterno",
            "nunca encuentras la salida",
        ])

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_anti_cliche_forbidden_phrase_fails(self):
        # Inject forbidden phrase into a shot narration
        bad_shot_list = CLEAN_SHOT_LIST_YAML.replace(
            'narrator_text: "Si enciendes la linterna, Bruno te arrastra al pozo y caes"',
            'narrator_text: "Si enciendes la linterna, te conviertes en cena de la torre"'
        )
        _build_spec(self.spec, shot_list_yaml=bad_shot_list)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec),
                  "--video-log", str(self.vlog), "--anti-cliche-file", str(self.anticliche),
                  "--skip-semantic"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("cliché", r.stdout.lower() + r.stderr.lower() + "cliche")


if __name__ == "__main__":
    unittest.main(verbosity=2)
