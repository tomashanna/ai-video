"""test_audit-spec-genre-fidelity.py — Firewall de GÉNERO sport-choice (no-horror guard).

Validates that audit-spec-genre-fidelity.py:
  - is agnostic-by-design (--format required; non-sport → not_applicable no-op),
  - Bug #9 (missing video_capabilities → exit 2),
  - a CLEAN sport-choice SPEC passes (exit 0),
  - each horror-leak class FAILS (exit 1): G2 SFX, G3 voice, G4 music, G5 narration+visual, G6 LUT,
  - the critical FALSE-POSITIVE guards do NOT fail (cool_defeat, sport tension drone,
    rugido/abucheos/derrota/tensión deportiva — legit sport terms must pass).

Run: python3 test_audit-spec-genre-fidelity.py   (unittest; no pytest needed).
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent / "audit-spec-genre-fidelity.py"

_CAPS = (
    "video_capabilities:\n"
    "  has_ai_generated_clips: true\n"
    "  has_tts_narration: true\n"
    '  format_type: "interactive_choice"\n'
)


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def _write(path, body, *, caps=_CAPS):
    Path(path).write_text(f'schema_version: "v11.1"\n{caps}{body}', encoding="utf-8")


# A clean sport-choice SPEC: deportivo SFX, sport LUTs (incl. cool_defeat), sport-thriller
# music, sport narrator voice, play-by-play narration with NO horror.
_CLEAN_SPORT = """narrator_voice: K3TeN3ZVK8WnOeJ0NYqZ
narrative_sections:
  - section_id: hook
    visual_style_lut: cool_cinematic_stadium_v1
  - section_id: consequence_d1
    visual_style_lut: cool_defeat_v1
  - section_id: resolution
    visual_style_lut: warm_glory_v1
music_continuous_layers:
  - layer_id: drone_base
    eleven_labs_prompt: "low subharmonic drone, sustained deep bass tension, dark cinematic sports-thriller bed, no horror"
  - layer_id: celebration
    eleven_labs_prompt: "triumphant stadium celebration ambience, euphoric crowd cheering warm, no horror"
asset_list:
  sfx_prompts_to_generate:
    - sfx_id: stadium_roar
      prompt: "massive packed football stadium crowd roar swelling, ultras chanting"
    - sfx_id: boos
      prompt: "disappointed stadium crowd booing, jeers and whistles"
    - sfx_id: net_ripple
      prompt: "football hitting the back of the net, net ripple, then crowd explosion"
narration_script:
  - segment_id: narrator_hook
    voice_id: K3TeN3ZVK8WnOeJ0NYqZ
    text_canonical: "Final de la Champions. Elige tu compañero. Saka, Arsenal. Dembele, PSG."
    shot_id_anchor: shot_01
shot_list:
  - shot_id: shot_01
    visual_style_lut: cool_cinematic_stadium_v1
    description: "POV en el circulo central frente al dyad Saka y Dembele."
    visual_intent: "Camara POV en el circulo central. Geografia: arco con red, kit rojo propio, kit azul rival, arquero, balon blanco, lineas de cal. Estadio lleno, reflectores, cesped. Accion: micro-bob."
    narration_in_this_shot: "Te la deja, le pegas, y la clavas. Gol. Eres campeon."
  - shot_id: shot_07
    visual_style_lut: cool_defeat_v1
    description: "El lateral roba el balon y sale de contra."
    visual_intent: "POV en la banda. Geografia: arco lejano, kit propio, lateral rival, balon. Estadio lleno. Accion: el rival roba y la perdes; abucheos de la hinchada, derrota deportiva."
    narration_in_this_shot: "Uy, se la diste al lateral, la perdio. Salen de contra. La burla es total."
"""


class TestGenreFidelity(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.spec = Path(self.tmp) / "spec.yaml"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ---- CLI / agnostic / capability ----

    def test_invocation_without_format_exits_nonzero(self):
        _write(self.spec, _CLEAN_SPORT)
        r = _run(["--spec", str(self.spec), "--dry-run"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("format", r.stderr.lower())

    def test_bug9_video_capabilities_missing(self):
        _write(self.spec, _CLEAN_SPORT, caps="")
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 2)

    def test_non_sport_format_not_applicable_noop(self):
        # NON-DESTRUCTIVE: horror-choice must be a no-op (exit 0, not_applicable).
        _write(self.spec, _CLEAN_SPORT)
        r = _run(["--format", "horror-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("not_applicable", r.stdout.lower())

    def test_missing_spec_exits_2(self):
        r = _run(["--format", "sport-choice", "--spec", str(Path(self.tmp) / "nope.yaml")])
        self.assertEqual(r.returncode, 2)

    # ---- CLEAN sport SPEC passes (the false-positive guard) ----

    def test_clean_sport_spec_passes(self):
        _write(self.spec, _CLEAN_SPORT)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"clean sport SPEC must pass.\nstdout {r.stdout}\nstderr {r.stderr}")
        self.assertIn('"pass"', r.stdout)

    def test_legit_sport_terms_not_flagged(self):
        # cool_defeat, drone subharmonico de tension deportiva, rugido, abucheos, derrota,
        # gol rival — all legit sport, must NOT appear as leaks.
        _write(self.spec, _CLEAN_SPORT)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        rep = json.loads(r.stdout)
        self.assertEqual(rep["leak_count"], 0, f"legit sport terms false-flagged: {rep.get('leaks')}")
        # explicit: cool_defeat is sport, not the cool_horror leak
        leak_terms = " ".join(l.get("term", "") for l in rep.get("leaks", []))
        self.assertNotIn("cool_defeat", leak_terms)

    # ---- each leak class FAILS ----

    def test_g6_cool_horror_lut_fails(self):
        body = _CLEAN_SPORT.replace("visual_style_lut: cool_defeat_v1", "visual_style_lut: cool_horror_v1")
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"cool_horror LUT must fail.\nstdout {r.stdout}")
        self.assertIn("G6", r.stdout)
        self.assertIn("cool_horror", r.stdout)

    def test_g3_horror_voice_id_fails(self):
        body = _CLEAN_SPORT.replace("narrator_voice: K3TeN3ZVK8WnOeJ0NYqZ",
                                    "narrator_voice: Tj9l48J9AJbry5yCP5eW")
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"horror narrator voice_id must fail.\nstdout {r.stdout}")
        self.assertIn("G3", r.stdout)
        self.assertIn("Tj9l48J9AJbry5yCP5eW", r.stdout)

    def test_g4_dark_ambient_music_fails(self):
        body = _CLEAN_SPORT.replace(
            'eleven_labs_prompt: "low subharmonic drone, sustained deep bass tension, dark cinematic sports-thriller bed, no horror"',
            'eleven_labs_prompt: "dark ambient drone, eerie horror pad, dread ambience"')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"dark ambient horror music must fail.\nstdout {r.stdout}")
        self.assertIn("G4", r.stdout)

    def test_g2_horror_sfx_scream_fails(self):
        body = _CLEAN_SPORT.replace(
            'prompt: "massive packed football stadium crowd roar swelling, ultras chanting"',
            'prompt: "blood-curdling horror scream, uncanny whisper, jumpscare sub-bass dread"')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"horror SFX (scream/whisper) must fail.\nstdout {r.stdout}")
        self.assertIn("G2", r.stdout)

    def test_g5_death_in_narration_fails(self):
        body = _CLEAN_SPORT.replace(
            'text_canonical: "Final de la Champions. Elige tu compañero. Saka, Arsenal. Dembele, PSG."',
            'text_canonical: "Si fallas, mueres en el campo y tu cadaver queda en el cesped."')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"death in narration must fail.\nstdout {r.stdout}")
        self.assertIn("G5", r.stdout)

    def test_g5_monster_in_visual_intent_fails(self):
        body = _CLEAN_SPORT.replace(
            'visual_intent: "Camara POV en el circulo central. Geografia: arco con red, kit rojo propio, kit azul rival, arquero, balon blanco, lineas de cal. Estadio lleno, reflectores, cesped. Accion: micro-bob."',
            'visual_intent: "Camara POV. Un monstruo deforme y grotesco emerge del tunel del estadio, body-horror uncanny."')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"monster/body-horror in visual_intent must fail.\nstdout {r.stdout}")
        self.assertIn("G5", r.stdout)

    def test_negated_no_horror_in_prompt_not_flagged(self):
        # The CANONICAL sport music prompts END with "...no horror" — a NEGATIVE instruction
        # to ElevenLabs. That must NOT be flagged as a leak (it's the opposite).
        body = _CLEAN_SPORT.replace(
            'eleven_labs_prompt: "triumphant stadium celebration ambience, euphoric crowd cheering warm, no horror"',
            'eleven_labs_prompt: "triumphant stadium celebration, warm uplifting tone, sin horror, without dread"')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 0, f"'sin horror / without dread' must NOT flag.\nstdout {r.stdout}")
        rep = json.loads(r.stdout)
        self.assertEqual(rep["leak_count"], 0)

    def test_positive_horror_still_flags_after_negation_guard(self):
        # Guard must NOT over-suppress: a NON-negated horror mention elsewhere still fails.
        body = _CLEAN_SPORT.replace(
            'eleven_labs_prompt: "low subharmonic drone, sustained deep bass tension, dark cinematic sports-thriller bed, no horror"',
            'eleven_labs_prompt: "horror drone, eerie dread ambience, sustained terror bed"')
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        self.assertEqual(r.returncode, 1, f"positive horror prompt must still fail.\nstdout {r.stdout}")
        self.assertIn("G4", r.stdout)

    def test_report_lists_field_and_term(self):
        # the report must be actionable: field + term + item per leak.
        body = _CLEAN_SPORT.replace("visual_style_lut: cool_defeat_v1", "visual_style_lut: cool_horror_v1")
        _write(self.spec, body)
        r = _run(["--format", "sport-choice", "--spec", str(self.spec)])
        rep = json.loads(r.stdout)
        self.assertGreaterEqual(rep["leak_count"], 1)
        leak = rep["leaks"][0]
        for key in ("item", "category", "field", "term"):
            self.assertIn(key, leak)


if __name__ == "__main__":
    unittest.main(verbosity=2)
