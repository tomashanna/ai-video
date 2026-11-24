# MODEL-CAPABILITIES-MATRIX.md — capacidades declarativas de los modelos del pipeline

> **NIVEL CAPA A (agnóstico — cualquier formato/proyecto lo consulta).** Creado 2026-05-30 tras V5 bug raíz: narración over-written escapó validación porque ningún rol del triángulo tenía visibilidad codificada de los límites del modelo i2v (Hailuo Std clip ~5.9s). Pattern_class 6/5 `model_constraints_not_propagated_across_triangle_roles` → Hard Rule #29.
>
> **Quién lo consulta (OBLIGATORIO)**:
> - 🏛️ **Arquitecto (CP0)**: antes de fijar `duration_intent_s` + escribir narración. Calcula `narración_dur_canonical = palabras/canonical_pace_wpm*60` y verifica `≤ min(duration_intent_s, model.clip_duration_max_s)`.
> - 🔍 **Validator L1** (`ai-video audit-spec-narration-fits-duration`): lee este archivo, chequea canonical-pace-fit vs límite del modelo.
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

kling_25_turbo_pro:
  provider: replicate
  model_id: "kwaivgi/kling-v2.5-turbo-pro"
  type: i2v
  clip_duration_tiers_s: [5, 10]      # genera 5s o 10s (param duration)
  cost_per_second_usd: 0.07           # MODEL-BENCHMARK § 1.1 → ~$0.35/clip 5s (~25% más que hailuo_std)
  leaderboard: "Elo 1283 i2v (supera a Kling 3.0 — MODEL-BENCHMARK § 1.2.2, leaderboard-validated)"
  audio_output: false
  strengths:
    - "instruction-following superior a hailuo_std → mejor para POV-lock + slow-motion holds + composición dictada"
    - "default del proyecto para hook viral primeros 30s (MODEL-BENCHMARK § 1.1)"
  resolution_observed: "1072x1928"    # MEDIDO mexico-sudafrica 2026-06-04 (start_image 768x1376, AR ~9:16; NO es 1080x1920 exacto → el atomic build escala+crop a 1080x1920)
  fps_observed: 24                     # MEDIDO: 24fps (igual que hailuo); duration=5 → 5.04s reales (121 frames)
  clip_real_s_observed: 5.04           # duration=5 → 5.041667s reales → más corto que hailuo (5.875s); afecta trim vs freeze-extend en CP5
  first_use: "mexico-sudafrica regen R1/R2/R3 shots 05/07/13/15 (2026-06-04) — observed completado post-batch"
  ⚠️_implicación_clave: |
    Mismo principio que hailuo: narración@165WPM debe caber en el tier elegido (5s tier → ≤13-14 palabras).
    Clips a 5s son MÁS CORTOS que los 5.875s de hailuo → si el shot lo necesita, tier 10s + trim CP5.

hailuo_pro:        # 1080p tier de minimax/hailuo-02 — usado V7 ultimo-tren-carga (mayoría de shots)
  provider: replicate
  model_id: "minimax/hailuo-02"        # MISMO modelo que hailuo_std; el tier lo fija el param resolution
  type: i2v
  resolution_param: "1080p"            # std=768p, pro=1080p (API enum resolution: [512p, 768p, 1080p])
  clip_duration_enum_s: [6, 10]        # API: duration ∈ {6,10}; "6s" sale ~5.9s reales (igual que std)
  clip_duration_max_s: 5.9             # observado V5 en tier 6s; 10s disponible pero NO usado en V7
  clip_duration_min_s: 1.0
  fps_observed: 24
  audio_output: false                  # NO genera audio (igual que std) — muxear aparte (atomic)
  cost_per_clip_usd: 0.49              # ⚠️ verify_at_first_call — 1080p-6s. Público minimax/hailuo-02 ≈ $0.48-0.49/clip
                                       #    (std 768p-6s = $0.28 observado V5). NO observado programáticamente
                                       #    (Replicate no expone pricing en API/openapi); usar este rango y CONFIRMAR
                                       #    con el 1er clip real (predict cost en el dashboard) antes de proyectar el batch completo.
  motion_constraints:
    - "mismas que hailuo_std (face frontal/15-30°, AVOID head turns bruscos)"
    - "1080p mejora detalle/sharpness vs 768p; NO cambia los límites de motion ni el audio"
  prompt_anti_patterns: ["talking","speaking","lips moving (esperar sync preciso)"]

kling_v2.5_pro:    # Replicate kwaivgi/kling-v2.5-turbo-pro — usado V7 ultimo-tren-carga (hook + clímax: 5 shots)
  provider: replicate
  model_id: "kwaivgi/kling-v2.5-turbo-pro"   # slug VERIFICADO contra Replicate API 2026-06-04
  type: i2v                            # t2v + i2v; i2v vía start_image (first-frame). Soporta end_image (last-frame keyframe)
  clip_duration_enum_s: [5, 10]        # API enum duration: [5, 10] (VERIFICADO). El SPEC V7 usa tier 5s.
  clip_duration_max_s: 10
  clip_duration_min_s: 5               # NO genera <5s; un shot de 3.5s usa el tier 5s (subutilizado) o trim post-gen
  resolution: "1080p"                  # AR nativo 9:16 (aspect_ratio enum: [16:9, 9:16, 1:1]; IGNORADO si hay start_image)
  fps_observed: 24
  audio_output: false                  # 2.5 es silent (Kling 2.6+ agregó audio nativo) — muxear aparte (atomic)
  input_schema:
    start_image: "first frame (i2v) — reemplaza el deprecated `image`"
    end_image: "last frame opcional (keyframe conditioning)"
    prompt: "text prompt de motion"
    negative_prompt: "string (default vacío)"
    aspect_ratio: "[16:9|9:16|1:1] — IGNORADO si start_image presente"
    guidance_scale: "DEPRECATED — kept for backwards compat, no usado (NO enviar cfg_scale, removido)"
  cost_per_clip_usd:                   # $0.07/s (MODEL-BENCHMARK § Kling 2.5 + fal/Replicate); NO expuesto en API
    tier_5s: 0.35                      # ⚠️ verify_at_first_call con el 1er clip real (Replicate no da pricing programático)
    tier_10s: 0.70
  cost_per_second_usd: 0.07
  motion_constraints:
    - "safety filter AGRESIVO en horror/gore/violence (#1 production blocker) — retry ~1.3-1.6x para horror/dark"
    - "permitido: implied horror, environmental dread, monster-in-shadow. Bloqueado: gore explícito, heridas on-screen"
    - "close-up cara sólido con prompt restrictivo (ver MODEL-BENCHMARK h6-santi-face): 'NO lip movement, eyes blink, mouth still'"
    - "crowds + fast hand-object falla; prompt débil → 'Ken Burns-ish' genérico"
  prompt_adherence: "8/10"
  ⚠️_implicación_clave: |
    clip_min 5s: un shot V7 de 3.5s (07a/12a/17a) NO puede pedir un clip de 3.5s — se genera tier 5s
    y se trimea en el atomic-build a duration_intent_s (el SPEC asumió clip_max_s 5.0 → OK, dentro de tier 5s).
    Costo proyectado a tier 5s = $0.35/clip. CONFIRMAR el costo real con el 1er clip antes de quemar el batch.

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
    ai-video image inyecta HORROR_SUFFIX (paleta warm amber). Para paletas cool/clínicas
    usar --no-mono-suffix + bloque de estilo propio (V5 CP3).
  constraints_canonical (ver MODEL-BEHAVIOR-LOG entry 1 para detalle empírico):
    - "face-coupling: identidad propaga vía cara; rasgo raro sin cara → regresa a normal"
    - "stability-budget: ≤3 props/elementos beyond el anchor char (anatomía rara)"
    - "pose-coupling: shot hand pose debe MATCH anchor pose exacto (no abstracto)"
    - "hand-configuration: bare/gloved + holding/empty deben coincidir con anchor"
    - "locus-anchors para rasgos raros aislados de la cara"
    - "prompts en frases descriptivas, NUNCA label-prefix (POV:/ANGLE:) → texto burned-in"
  pro_tier: "ai-video image NO soporta tier Pro actualmente (hardcoded flash) — forward gap"
```

## Cómo se usa (resumen enforcement)

1. **Arquitecto** lee esta matriz en CP0 → per shot: `palabras/165*60 ≤ min(duration_intent_s, modelo_i2v.clip_duration_max_s)`. Si falla → trim/split/extend/cambiar modelo. Documenta `model_constraints_acknowledged: true` en el SPEC.
2. **Validator L1** lee esta matriz → chequea canonical-pace-fit (NO ceiling 280).
3. **Auditor** (anti-pattern #12) → ningún validator/build asume capacidades hardcoded; todos consultan esta matriz.
4. **Ingeniero** → settings canónicos + respeta `clip_duration_max_s` (NO trimear clip dejando audio muxeado truncado).

**Forward**: cuando se adopte un modelo nuevo, agregar su entrada ACÁ antes de usarlo en producción (HR#29).
