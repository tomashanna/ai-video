# Voice Effects Presets — creepy effects library

> **Library de presets reusables para procesar voces TTS** con efectos creepy/horror. 10 presets documentados: 4 user-validated en listen test 2026-05-27 (ghost/ultratumba/demon/possessed) + 2 matadero-validated en contexto original (matarife/cocinera) + 4 recipe-archived (static_radio/distant_echo/vampire_whisper/phone_call). Reusable cross-project via `apply-voice-preset.py`.

**Status post listen-test 2026-05-27**:
- ✅ **4 user-validated** (Oxley dry base): `ghost_whisper`, `ultratumba_cavernoso`, `demon_growl`, `possessed_child`
- 🟡 **2 contextually-validated** (matadero CP2 original): `matarife_canonical`, `cocinera_warm` — failed Oxley-dry standalone test (context mismatch, NOT recipe fault). Re-test con voz correcta antes de revival.
- 📁 **4 recipe-archived** (rejected user test 2026-05-27): `static_radio_old`, `distant_echo`, `vampire_whisper`, `phone_call_horror` — recipes kept como forensic record para futuras producciones que requieran intent específico.

---

## Quick start

```bash
# 1. Listar presets disponibles
python3 .claude/skills/ai-video-production/templates/scripts/apply-voice-preset.py --list

# 2. Aplicar preset a un archivo TTS ya procesado
python3 .claude/skills/ai-video-production/templates/scripts/apply-voice-preset.py \
  --preset ultratumba_cavernoso \
  --input <project>/assets/narr-processed.mp3 \
  --output <project>/assets/narr-final.mp3

# 3. Validar intelligibility (M7.7.5 enforcement)
python3 .claude/skills/ai-video-production/templates/scripts/apply-voice-preset.py \
  --preset demon_growl \
  --input raw.mp3 \
  --output processed.mp3 \
  --verify --text "Texto esperado exacto del SPEC"
# Exit 0 = PASS / Exit 2 = FAIL bajo threshold 0.85
```

## Listening samples

Los demos de audio NO se versionan (se regeneran localmente con `apply-voice-preset` sobre cualquier TTS seco). Presets validados en listen-test 2026-05-27:

| File | Preset | Status | Listen for |
|------|--------|--------|-----------|
| `_base_oxley_dry.mp3` | DRY baseline | reference | Voz Oxley raw 15.3s sin procesamiento (94 WPM) |
| `ghost_whisper_demo.mp3` | ghost_whisper | ✅ validated 2026-05-27 | Airy floating layer ethereal |
| `ultratumba_cavernoso_demo.mp3` | ultratumba_cavernoso | ✅ validated 2026-05-27 | Cripta + grave + lowpass |
| `demon_growl_demo.mp3` | demon_growl | ✅ validated 2026-05-27 | Octave down + distortion |
| `possessed_child_demo.mp3` | possessed_child | ✅ validated 2026-05-27 | Pitch up + chorus modulation |

## Revival demos 2026-05-29 (matarife + cocinera fair-context)

Re-generados en contexto correcto post-feedback Tomás:

| File | Voice | Atempo | Text | Status |
|------|-------|--------|------|--------|
| `matarife_canonical_revival_2026_05_29.mp3` | Oxley | 1.6× | "Hoy la carne está fresca..." | 🟡 revival_pending_user_test_2026_05_29 |
| `cocinera_warm_revival_2026_05_29.mp3` | Kate BFP | 1.23× | "Pasa querido, la cena..." | 🟡 revival_pending_user_test_2026_05_29 |

**Si Tomás listen test confirma estos** → flip catalog `revival_validated_2026_05_29` + reusable en SPECs V5+. Si fail también en fair context → recipe-archived definitivo.

## Recipe-archived presets (rejected user test 2026-05-27)

Recipes kept en catalog como forensic record. Sample binaries deleted post listen test. Re-validable en contexto correcto si futuras producciones requieren el intent:

| Preset | Why archived | Context for potential revival |
|--------|--------------|-------------------------------|
| `matarife_canonical` | Test base Oxley DRY ≠ matadero original context (atempo 1.6× + matarife text) | Re-test con Oxley + matarife-specific text + atempo. Matadero CP2 M7.7.5 PASS sigue como authority en su contexto original. |
| `cocinera_warm` | Aplicado a Oxley masculino — preset diseñado para Kate femenina warm | Re-test con Kate (`qWWAqFomnJ99VwQLREfT`) + cocinera text + atempo 1.23×. |
| `static_radio_old` | Recipe ffmpeg correcto pero outcome no calzaba percepción "radio rota" | Si SPEC futuro pide walkie-talkie/transmisión rota → re-genera demo + re-evaluate |
| `distant_echo` | Echos sonaron retro/cheesy en lugar de "llamado lejano" canonical | Si SPEC futuro pide bosque/cueva calling pattern → re-evaluate con texto+intent diferente |
| `vampire_whisper` | Oxley base ya es character-creepy → preset adicional redundant | Re-test con voz base neutral (Eleguar/Ignacio) — el "grave-cercano" puede emerger sobre voz limpia |
| `phone_call_horror` | EQ telephone funciona pero texto genérico no genera cue "llamada" contextual | Re-test con texto que SUENE a llamada (pregunta urgente directa) + voz neutral |

## Integración SPEC schema (arquitecto V5+)

Add new field `creepy_effect_preset` per character:

```yaml
characters:
  - id: char_proyector
    voice_id: K3TeN3ZVK8WnOeJ0NYqZ      # David C2
    creepy_effect_preset: ultratumba_cavernoso
    atempo_strategy: "per-segment + 1.15 narrator multiplier"
    canonical_pair: "deep_narrator + cripta_intent"

  - id: char_cocinera
    voice_id: qWWAqFomnJ99VwQLREfT       # Kate
    creepy_effect_preset: cocinera_warm
    atempo_strategy: "per-segment + 1.23 cocinera multiplier"

  - id: char_matarife
    voice_id: 2gPFXx8pN3Avh27Dw5Ma       # Oxley
    creepy_effect_preset: matarife_canonical
    atempo_strategy: "per-segment + 1.28 matarife ceiling"
```

## Workflow ingeniero CP4 audio

```bash
# Per character con creepy_effect_preset declared en SPEC:

# 1. TTS raw (no atempo yet)
.venv/bin/python scripts/tts.py \
  -t "<character line>" \
  -v "<voice_id>" \
  -o assets/tts/${char}-raw.mp3

# 2. Per-segment atempo (voices-catalog workflow)
ffmpeg -y -i assets/tts/${char}-raw.mp3 \
  -filter:a "atempo=<raw_dur/target_dur clamped [0.7, 2.5]>" \
  assets/tts/${char}-atempo.mp3

# 3. Apply creepy preset
python3 .claude/skills/ai-video-production/templates/scripts/apply-voice-preset.py \
  --preset <preset_id> \
  --input assets/tts/${char}-atempo.mp3 \
  --output assets/tts/${char}-final.mp3

# 4. M7.7.5 audit (Rule D = user perceptual precedence)
python3 .claude/skills/ai-video-production/templates/scripts/apply-voice-preset.py \
  --preset <preset_id> \
  --input assets/tts/${char}-atempo.mp3 \
  --output /tmp/${char}-verify.mp3 \
  --verify --text "<character line exact>"
# Exit 2 → reduce preset intensity per mitigation
```

## Preset risk tiers + mitigations

| Risk | Presets | Mitigation pattern |
|------|---------|-------------------|
| **low** (intel ≥0.90) | matarife, cocinera, possessed_child, vampire_whisper, phone_call | Direct apply OK |
| **medium** (intel 0.80-0.90) | ghost_whisper, ultratumba, static_radio, distant_echo | Verify M7.7.5 + reduce wet/intensity si <0.85 |
| **high** (intel 0.60-0.80) | demon_growl | Captions MANDATORY + acepta floor 0.60 por intent dramatic |

## Rules canónicas

1. **NUNCA** aplicar 2 presets seguidos sin medir intelligibility intermedio.
2. **Per-segment atempo SIEMPRE antes** del preset (workflow voices-catalog).
3. **Si preset baja intel <0.85** → consultar `intelligibility_mitigation` en catalog OR escalar al arquitecto.
4. **Auditor M7.7.5 check obligatorio** post-preset application (excepto demon_growl que tiene floor 0.60).
5. **Cuando preset cambia duración** (echos +30%) → recalcular timeline timing CP4 → re-medir vs SPEC duration.
6. **Validation status `pending_user_test`** requiere listen test ANTES de marcar `validated` en catalog.

## Adding new presets

1. Edit `presets-catalog.json` añadiendo entry al array `presets[]` con todos los fields requeridos.
2. Generate demo sample: `python3 apply-voice-preset.py --preset <new_id> --input samples/_base_oxley_dry.mp3 --output samples/<new_id>_demo.mp3`
3. User listen test → si OK, flip `validation_status: validated` + agregar `validated_in: [<project>]`.
4. Commit catalog + sample to repo.

## Future backlog (post user test 2026-05-27)

- `underwater_voice` — equalizer cut high + delay + chorus (voz bajo el agua)
- `split_personality` — dos pistas con pitch shifts opuestos overlapping
- `growing_dread` — automation reverb que crece linealmente (start 20 end 90) sobre 10s
- `reverse_whisper` — sox reverse + reverb + reverse (trick clásico horror)
- `lullaby_corrupted` — pitch shifts micro periódicos + slight detune

## Files

```
.claude/skills/ai-video-production/templates/
├── effects-library/voice-effects/
│   ├── README.md             (this file — workflow + docs)
│   └── presets-catalog.json  (10 presets canonical — recipes + metadata)
└── scripts/
    └── apply-voice-preset.py (CLI wrapper + M7.7.5 verify)

```

**Por qué split**: catalog + script viven en `.claude/skills/` como template universal (CAPA 1, copiado/leído por todos los proyectos). Samples binarios viven en `library/` (junto a `voices/`, `sfx/`, `music/` — patrón canonical para artefactos reusables). Mantiene skill template liviano.

## Cross-references

- `library/voices-catalog.json` § voices[] — per-voice atempo_strategy + effects_chain inline (matarife + cocinera entries)
- `.claude/skills/creative-director/master-flow-v2/GAPS-LOG.md` row 45 — Gap #45 audit-tts-perceptual.py Sprint B priority (extend con preset-aware intelligibility check)
- `CLAUDE.md` Hard Rule #19 — NEVER ESTIMATE, ALWAYS MEASURE (per-preset validation_status + measurement required)
