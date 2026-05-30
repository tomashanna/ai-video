# MODEL-CAPABILITIES-MATRIX.md — capacidades declarativas de los modelos del pipeline

> **NIVEL CAPA A (agnóstico — cualquier formato/proyecto lo consulta).** Creado 2026-05-30 tras V5 bug raíz: narración over-written escapó validación porque ningún rol del triángulo tenía visibilidad codificada de los límites del modelo i2v (Hailuo Std clip ~5.9s). Pattern_class 6/5 `model_constraints_not_propagated_across_triangle_roles` → Hard Rule #29.
>
> **Quién lo consulta (OBLIGATORIO)**:
> - 🏛️ **Arquitecto (CP0)**: antes de fijar `duration_intent_s` + escribir narración. Calcula `narración_dur_canonical = palabras/canonical_pace_wpm*60` y verifica `≤ min(duration_intent_s, model.clip_duration_max_s)`.
> - 🔍 **Validator L1** (`audit-spec-narration-fits-duration.py`): lee este archivo, chequea canonical-pace-fit vs límite del modelo.
> - 🔍 **Auditor**: anti-pattern #12 — ningún validator asume capacidades hardcoded; consulta esta matriz.
> - 🛠️ **Ingeniero**: usa los settings canónicos + respeta los límites al generar.
>
> **Append-only forward**: nuevos modelos (marina/tutorial/B2B) agregan entradas. NO borrar (registro forense).

---

## i2v — image-to-video (animación)

```yaml
hailuo_std:
  provider: replicate
  model_id: "minimax/hailuo-02"
  type: i2v
  clip_duration_max_s: 5.9          # observado V5: 5.875s reales (NO genera clips más largos en este tier)
  clip_duration_min_s: 1.0
  resolution_observed: "768x1376"   # tier 768p (param resolution=768p)
  fps_observed: 24
  audio_output: false               # ⚠️ NO genera audio — narración/SFX se muxean aparte (atomic)
  cost_per_clip_usd: 0.28           # V5 observado (768p 6s)
  motion_constraints:
    - "face frontal o 15-30° tilt; AVOID head turns bruscos (uncanny)"
    - "lip-sync NO fonémicamente preciso (i2v base) → Phase 3 Hedra/Sync.so si se requiere"
  prompt_anti_patterns: ["talking","speaking","lips moving (esperar sync preciso)"]
  ⚠️_implicación_clave: |
    Si la narración canónica de un shot (palabras/165*60) > 5.9s, NO cabe en un clip Hailuo.
    Opciones: (a) trim narración a ≤5.9s@165WPM (~16 palabras), (b) freeze-extend último frame
    (tpad) para cubrir narración más larga, (c) split shot en 2 clips, (d) usar hailuo_pro/veo.
    NUNCA trimear el clip a duration_intent_s dejando la narración muxeada truncada (V5 bug).

hailuo_pro:        # forward — NO usado aún
  provider: replicate
  type: i2v
  clip_duration_max_s: 10
  status: unverified_forward

veo_3_1:           # forward — NO usado (billing surprise V3, ver SYSTEM-LEARNINGS)
  type: i2v
  clip_duration_max_s: 8
  status: avoid_until_billing_confirmed
```

## tts — text-to-speech

```yaml
elevenlabs:
  provider: elevenlabs (API + MCP)
  type: tts
  models: ["eleven_v3", "eleven_multilingual_v2"]
  canonical_narrator_v5: "David C2"
  voice_id: "K3TeN3ZVK8WnOeJ0NYqZ"     # validated_canonical_narrator_v5_2026_05_29
  canonical_pace_wpm: 165               # F1 median; David C2 mide 157 → atempo ×1.05 → 165
  physical_ceiling_wpm: 280             # límite inteligibilidad TTS (NO usar como "fit", ver abajo)
  ⚠️_fit_rule: |
    El check de "cabe en el shot" NO es WPM≤280 (eso es "comprimible si hablás rápido").
    Es: narración_dur_a_pace_CANÓNICO (palabras/165*60) ≤ duration_intent_s. El TTS se genera
    a pace canónico (165), NO comprimido a 280. V5 bug: L1 chequeó ≤280 (PASS) pero el TTS a 165
    salió más largo que duration_intent_s.
  character_voices_v5:
    axel_malo: "Oxley Evil 2gPFXx8pN3Avh27Dw5Ma (validated; filtro visor: highpass180+lowpass3500+reverb)"
    hugo_bueno: "Kate BFP qWWAqFomnJ99VwQLREfT (validated_canonical, sin filtro)"
  caption_floor_s: 0.5                  # text_to_sound_effects floor (no genera <0.5s)
```

## t2i — text-to-image (anchors + shots)

```yaml
gemini_flash_image:
  provider: gemini (google-genai)
  model_id: "gemini-3.1-flash-image-preview"   # "Nano Banana"
  type: t2i
  resolution: "1080x1920 (vertical reel)"
  cost_per_image_usd: ~0.04
  ⚠️_HORROR_SUFFIX_gotcha: |
    scripts/image.py inyecta HORROR_SUFFIX (paleta warm amber). Para paletas cool/clínicas
    usar --no-mono-suffix + bloque de estilo propio (V5 CP3).
  constraints_canonical (ver MODEL-BEHAVIOR-LOG entry 1 para detalle empírico):
    - "face-coupling: identidad propaga vía cara; rasgo raro sin cara → regresa a normal"
    - "stability-budget: ≤3 props/elementos beyond el anchor char (anatomía rara)"
    - "pose-coupling: shot hand pose debe MATCH anchor pose exacto (no abstracto)"
    - "hand-configuration: bare/gloved + holding/empty deben coincidir con anchor"
    - "locus-anchors para rasgos raros aislados de la cara"
    - "prompts en frases descriptivas, NUNCA label-prefix (POV:/ANGLE:) → texto burned-in"
  pro_tier: "image.py NO soporta tier Pro actualmente (hardcoded flash) — forward gap"
```

## Cómo se usa (resumen enforcement)

1. **Arquitecto** lee esta matriz en CP0 → per shot: `palabras/165*60 ≤ min(duration_intent_s, modelo_i2v.clip_duration_max_s)`. Si falla → trim/split/extend/cambiar modelo. Documenta `model_constraints_acknowledged: true` en el SPEC.
2. **Validator L1** lee esta matriz → chequea canonical-pace-fit (NO ceiling 280).
3. **Auditor** (anti-pattern #12) → ningún validator/build asume capacidades hardcoded; todos consultan esta matriz.
4. **Ingeniero** → settings canónicos + respeta `clip_duration_max_s` (NO trimear clip dejando audio muxeado truncado).

**Forward**: cuando se adopte un modelo nuevo, agregar su entrada ACÁ antes de usarlo en producción (HR#29).
