# Voice Effects Presets — creepy effects library

> **Library de presets reusables para procesar voces TTS** con efectos creepy/horror. 10 presets canónicos covering matarife, cocinera, ghost, ultratumba, demon, possessed child, radio static, distant echo, vampire whisper, phone call. Reusable cross-project via `apply-voice-preset.py`.

**Status**: ✅ 2 validated (matarife + cocinera matadero CP2) + 🟡 8 pending user test 2026-05-27.

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

`samples/` contains demos generated 2026-05-27 from Oxley base (`2gPFXx8pN3Avh27Dw5Ma`, 94 WPM raw):

| File | Preset | Listen for |
|------|--------|-----------|
| `_base_oxley_dry.mp3` | DRY (baseline) | Reference unprocessed |
| `matarife_canonical_demo.mp3` | matarife_canonical | Industrial grave + flanger |
| `cocinera_warm_demo.mp3` | cocinera_warm | Intimate warm echo |
| `ghost_whisper_demo.mp3` | ghost_whisper | Airy floating layer |
| `ultratumba_cavernoso_demo.mp3` | ultratumba_cavernoso | Cripta + grave + lowpass |
| `demon_growl_demo.mp3` | demon_growl | Octave down + distortion |
| `possessed_child_demo.mp3` | possessed_child | Pitch up + chorus modulation |
| `static_radio_old_demo.mp3` | static_radio_old | Radio lo-fi + bitcrush |
| `distant_echo_demo.mp3` | distant_echo | Múltiples ecos + lowpass |
| `vampire_whisper_demo.mp3` | vampire_whisper | Bass boost + micro reverb intimate |
| `phone_call_horror_demo.mp3` | phone_call_horror | EQ telephone 400-3400Hz + phaser |

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
voice-effects/
├── README.md                 (this file)
├── presets-catalog.json      (10 presets canonical)
└── samples/
    ├── _base_oxley_dry.mp3   (15.3s reference)
    ├── matarife_canonical_demo.mp3
    ├── cocinera_warm_demo.mp3
    ├── ghost_whisper_demo.mp3
    ├── ultratumba_cavernoso_demo.mp3
    ├── demon_growl_demo.mp3
    ├── possessed_child_demo.mp3
    ├── static_radio_old_demo.mp3
    ├── distant_echo_demo.mp3
    ├── vampire_whisper_demo.mp3
    └── phone_call_horror_demo.mp3

scripts/
└── apply-voice-preset.py     (CLI wrapper + M7.7.5 verify)
```

## Cross-references

- `library/voices-catalog.json` § voices[] — per-voice atempo_strategy + effects_chain inline (matarife + cocinera entries)
- `.claude/skills/creative-director/master-flow-v2/GAPS-LOG.md` row 45 — Gap #45 audit-tts-perceptual.py Sprint B priority (extend con preset-aware intelligibility check)
- `CLAUDE.md` Hard Rule #19 — NEVER ESTIMATE, ALWAYS MEASURE (per-preset validation_status + measurement required)
