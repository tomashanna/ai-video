# MODEL BENCHMARK — Industria AI Video & Imagen-Gen

> **Última actualización:** 2026-05-13 (v1 research + v2 refuerzo + v3 A/B test propio N=2)
> **Próxima revisión recomendada:** cada 60 días — la industria se mueve semanalmente
> **Quién consulta este doc:** `video-director` skill ANTES de elegir modelo para un shot/proyecto
> **Quién mantiene este doc:** el agent que detecte un modelo nuevo relevante o un cambio crítico de pricing/policy

---

## 0. Cómo usar este doc

1. **Para elegir modelo en un proyecto nuevo:** ir directo a § 2 (Matriz de decisión) → cruzar use-case con quality tier → leer § 3 spec sheet del modelo elegido.
2. **Para validar si un claim es confiable:** § 4 (Claim Validation Log) marca cada premise crítico como VALIDATED / WEAK / REFUTED.
3. **Para entender el método y confianza:** § 5 (Methodology + Blindspots).
4. **Si encontrás un modelo nuevo no listado:** actualizá § 3 + § 4 con sources + bump la fecha de "Última actualización".

---

## 1. EXECUTIVE SUMMARY

### 1.1 TL;DR — Defaults recomendados por use-case (cheat sheet)

| Use-case | Default | Costo | Fallback | Razón |
|---|---|---|---|---|
| **Hook viral (primeros 30s Reel)** | Kling 2.5 Turbo Pro | $0.07/s | Seedance 2.0 | Per project hard rule; leaderboard-validated; permite control narrativo |
| **B-roll / shot no-hero >30s** | Kling 2.5 Turbo Pro | $0.07/s | LTX-2.3 self-host | Coste/calidad sweet spot; LTX cuando hace falta volumen barato |
| **Cinematic high-prod (long-form)** | Veo 3.1 Standard | $0.40/s | Kling 3.0 | Audio nativo + multi-image refs + native 9:16 |
| **Multi-shot narrativo c/ personaje** | Seedance 2.0 + Nano Banana | $0.247/s + $0.04/img | Kling 3.0 Omni | Multi-shot nativo; consistency cross-shots |
| **Talking head / lipsync** | Hedra Character-3 | $0.05/s | Sync.so (post-process) | Especialista 9.5/10 lipsync; bate a general-purpose |
| **Camera hero (dolly zoom, crash zoom)** | Higgsfield DoP + Kling backbone | $0.15-0.40/s | Kling 2.5 prompt-only | Parametric stacked camera moves únicos |
| **Horror gore explícito (sangre, herida)** | Wan 2.7 self-host | GPU cost | Hunyuan 1.5 cozy build | Único path 100% permisivo |
| **Storyboard imagen c/ personaje** | Gemini Nano Banana (2.5 Flash Image) | $0.039/img | Seedream 4.5 / Flux Kontext + PuLID | Current default validado; multi-image conversation |
| **Title cards con texto legible** | Ideogram 3.0 | $0.075/img | Nano Banana | Tipografía in-image #1 del mercado |
| **Pose-driven character recurrente** | Wan 2.2 Animate | self-host | — | Niche pero único: skeleton-driven identity lock |

### 1.2 Cambios críticos vs estado previo (lo que MOVIÓ la decisión)

1. **HappyHorse-1.0 (Alibaba ATH, abril 2026) emergió como #1 i2v** — Elo 1395 en Artificial Analysis, por encima de Seedance 2.0 (1347). Brand new, sin reviews independientes aún. **Acción:** test A/B antes de defaultear a Seedance.
2. **Kling 2.5 Turbo Pro (Elo 1283) supera a Kling 3.0 (1281/1277) en i2v leaderboard.** El default actual del proyecto **está leaderboard-validated**. NO hay razón i2v urgente para migrar a 3.0 salvo necesidad de multilingual lipsync.
3. **Sora 2 está en Elo 975 #63 i2v** — muy por debajo del marketing. Shutdown de septiembre 2026 es parcialmente quality-driven. **NO incorporar a pipeline futuro.**
4. ~~**Claim "Hailuo para horror" debilitado**~~ → **VALIDADO 2026-05-16 caso cabina-14**: Hailuo 02 competitivo vs Kling Turbo Pro para escenas de **harto movimiento** (multi-character motion + camera tracking) con **premium prompt** (per INGENIERO-PAUTA § 5.7). Costo: ~1/3 del Kling Turbo Pro a quality similar. Validez del claim **depende del prompt quality** — con prompt vago, Hailuo subperforma. Con prompt premium 5-clause (subject + camera + lighting + atmosphere + style), Hailuo cierra el gap. Ver § Premium prompt template abajo.
5. **Hunyuan 1.5 + Wan 2.7 = experimentation tier, NO production tier** para 9.7 bar. Curious Refuge ranks Wan 2.6 en 6.7/10 (debajo de todos los modelos pagos). Mantener como cost-saving experimental, no como reemplazo de Kling.
6. **Imagen 4 se apaga 30 junio 2026.** Migrar a Nano Banana (Gemini 2.5 Flash Image / Gemini 3 Pro Image / "Nano Banana Pro") — forward path, no downgrade a Imagen 3.
7. **Workflow community dominante 2026:** multi-model orchestration, NO single-model. Cita recurrente: "Seedance for action, Kling for characters, Veo for products."
8. **Pieter Levels (Photo AI)** = practitioner-evidence más fuerte para "Hailuo = Kling fallback" pero la cita es Oct 2024 — re-validar con modelos 2026.

### 1.3 Hard constraints (gates universales independientes del modelo)

- ⛔ **Sora 2:** API shutdown 2026-09-24. NO incorporar nuevos workflows.
- ⛔ **Imagen 4:** retirement 2026-06-30. Migrar antes de mayo 30.
- ⛔ **Midjourney v7:** sin API pública. NO scriptable desde `ai-video image`. Skip para automation.
- ⛔ **NSFW / horror gore:** Veo 3.1, Sora 2, Midjourney, Ideogram, Runway, Imagen rechazan. Para gore explícito: Wan 2.7 self-host o Hunyuan 1.5 cozy. Para horror "suggestive": Kling 2.5 con prompts cuidadosos / Hailuo 2.3.
- ⛔ **Watermark:** Sora 2 fuerza watermark en todos los tiers. Pika free-tier también. NUNCA usar tier con watermark para publicación final.

### 1.4 Confianza del benchmark

- **Alta confianza:** specs base, pricing, AR support, leaderboard ranks (artificialanalysis.ai), shutdown dates oficiales.
- **Media confianza:** prompt adherence scores, retry rates típicos, "fortalezas/debilidades" (community-reported pero múltiples fuentes).
- **Baja confianza:** claims marketing-only del vendor sin corroboración (ej: "95% character consistency"). Marcados explícitamente.
- **Blindspots:** Reddit threads directos (bloqueado en este pass), YouTube comments completos, Discord internals. Ver § 5.

---

## 2. MATRIZ DE DECISIÓN

> **Update 2026-05-13:** Decision tree validado con A/B test propio (`ab-testing/`) — N=2 prompts (vague + polished), source bosque-abandonado h1, Gemini Video Analyzer + observación visual frame-by-frame. **Prompt quality matters HUGELY** — los 3 modelos cambian dramáticamente entre prompt vago y prompt pulido. Ver `prompt_quality_no_vague.md` memory.

### 2.0 Decision tree — ¿qué modelo elijo? (validado N=2)

```
┌─────────────────────────────────────────────────────────────────┐
│  ⛔ PREREQUISITO INCONDICIONAL:                                  │
│  El prompt DEBE estar pulido. Validar antes de elegir modelo:    │
│  subject body details + camera lens/movement + light source/temp │
│  + atmospheric params + mood vía expresiones físicas + style ref │
│  Ver `prompt_quality_no_vague.md`. Sin prompt pulido, cualquier │
│  modelo subperforma — la decisión de modelo es secundaria.      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  Q1: ¿Escena requiere MOTION NARRATIVO?                     │
│  (caminar, correr, agarrar, voltear, mirar, escapar)        │
├─────────────────────────────────────────────────────────────┤
│   SÍ → Hailuo 02 ★                                           │
│        budget tight → Standard 768p ($0.045/s)              │
│        hero shot   → Pro 1080p ($0.08/s)                    │
│   NO → ir a Q2                                                │
└─────────────────────────────────────────────────────────────┘

> ⚠️ **HOOK VIRAL OVERRIDE**: si el shot está en primeros 30s del Reel (hard rule #6 docs/OPERATING-MANUAL.md + `animation_30s_rule.md` memoria), Kling 2.5 Turbo Pro es default INDEPENDIENTEMENTE de motion narrativo. Razón: hook viral leaderboard-validated en § 1.1 cheat sheet. Hailuo entra como default para motion narrativo SOLO en escenas data-start ≥ 30s.

┌─────────────────────────────────────────────────────────────┐
│  Q2: ¿Escena es CINEMATIC ESTÁTICA con character preservation?│
│  (plano fijo con micro-gestos, parallax sutil, no acción)   │
├─────────────────────────────────────────────────────────────┤
│   SÍ → Seedance 1 Pro 1080p ($0.12/s)                       │
│        — mejor composition + aesthetic + character framing   │
│        — vale los 71% extra vs Kling para hero estático      │
│   NO → ir a Q3                                                │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  Q3: ¿Escena ATMOSFÉRICA + giro/alejamiento de personajes?  │
│  (turn + walk away, ambient, fog, dolly + chars perfil)     │
├─────────────────────────────────────────────────────────────┤
│   SÍ → Kling 2.5 Turbo Pro ($0.07/s)                        │
│        — con prompt pulido responde bien a rotación+motion   │
│        — bate a Hailuo en cinematic quality estático         │
│        — falla con prompt vago (totalmente estático)         │
│   NO → ir a Q4                                                │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│  Q4: ¿Es DRAFT / PRUEBA INICIAL?                            │
├─────────────────────────────────────────────────────────────┤
│   SÍ → ⛔ NO USAR LTX legacy (motion 3/10, confirmado out)   │
│        Pending: validar LTX-2.3 vía fal.ai                   │
│        Workaround: Hailuo Std 768p sirve también como draft  │
│        ($0.27 / 6s) — barato Y se mueve                     │
│   NO → fallback default: Kling 2.5 Turbo Pro                 │
└─────────────────────────────────────────────────────────────┘
```

### Mapa rápido horror-choice format

| Tipo de shot | Modelo | Costo / clip |
|---|---|---|
| H1 hook — chars caminan/aparecen | Hailuo 02 Pro 1080p | $0.40 (5s) |
| H2-H6 acción — corre, mira, agarra | Hailuo 02 Std 768p | $0.27 (6s) |
| Plano cinematic estático + chars | Seedance 1 Pro | $0.60 (5s) |
| Plano atmosférico chars girando | Kling 2.5 Turbo | $0.35 (5s) |
| Atmósfera + fog (sin chars) | Kling 2.5 Turbo | $0.35 (5s) |
| Title cards / static reveals | Kling 2.5 Turbo | $0.35 (5s) |
| Drafts iteración | Hailuo 02 Std 768p (NO LTX) | $0.27 (6s) |

### 2.1 Animación (image-to-video / text-to-video) — matriz por tier

| Use-case | Tier HERO (9.7+ bar) | Tier STANDARD (9.5 bar) | Tier DRAFT (cheap) |
|---|---|---|---|
| **Reel vertical 9:16 short-form** | Kling 2.5 Turbo Pro · Seedance 2.0 · HappyHorse-1.0 (test) | Hailuo 2.3 · Kling 1.6 Pro | LTX-2.3 · Wan 2.2 self-host |
| **YouTube horizontal long-form** | Veo 3.1 Standard · Kling 3.0 | Runway Gen-4.5 · Seedance 1.5 Pro | LTX-2.3 |
| **Hook viral (primeros 30s)** | Kling 2.5 Turbo Pro (default) | Seedance 2.0 | NO usar tier draft |
| **B-roll / ambient** | Kling 2.5 Turbo Pro | Hailuo Standard 768p | LTX-2.3 · Wan 2.2 |
| **Cinematic cinema-grade** | Veo 3.1 Standard ($0.40/s) | Kling 2.1 Master ($0.28/s) | Kling 2.5 Turbo Pro |
| **Multi-shot narrative** | Seedance 2.0 (multi-shot nativo) · Kling 3.0 Omni | Runway Gen-4.5 (60s continuous) | — |
| **Talking head / lipsync** | Hedra Character-3 ($0.05/s) | Veo 3.1 (audio nativo) | Sync.so post-process |
| **Camera hero (dolly zoom, etc)** | Higgsfield DoP + Kling backbone | Kling 1.6 Pro (camera params nativos) | prompt-only Kling 2.5 |
| **Action / fast motion** | Seedance 2.0 (#1 physics) · Hailuo 2.3 | Kling 2.5 Turbo Pro | LTX-2.3 |
| **Horror suggestive (atmospheric)** | Kling 2.1 Master · Veo 3.1 (si pasa filter) | Kling 2.5 Turbo Pro · Hailuo 2.3 (test) | LTX-2.3 |
| **Horror gore explícito** | Wan 2.7 self-host · Hunyuan 1.5 cozy build | — | — |
| **Pose-driven character recurrente** | Wan 2.2 Animate · Animate-X | — | — |
| **First/last frame conditioning (cuts)** | Kling 1.6 Pro · Kling 2.5 · LTX-2.3 · Wan 2.7 | Pika 2.5 (Pikaframes) | — |
| **Audio nativo en clip** | Veo 3.1 · Kling 3.0 · Sora 2 (deprecando) | Seedance 2.0 · Vidu Q3 · Wan 2.5 | LTX-2.3 |

### 2.2 Imagen-gen (storyboard + character consistency)

| Use-case | Tier HERO | Tier STANDARD | Tier DRAFT |
|---|---|---|---|
| **Character cross-6+ escenas (horror-choice)** | Nano Banana Pro (Gemini 3) · Seedream 4.5 (14 refs) | Gemini 2.5 Flash Image · Flux Kontext + PuLID | Midjourney --oref (no API) |
| **Single-shot hero photoreal** | Imagen 4 Ultra (mientras dure) · Flux 1.1 Pro Ultra | Nano Banana · Seedream 4.5 | Flux Dev self-host |
| **Title card con texto legible** | Ideogram 3.0 Quality | Recraft V3 | Nano Banana (texto OK) |
| **Logo / brand design** | Recraft V3 (vector + style lock) | Ideogram 3.0 | — |
| **Stylized / painterly / anime** | Midjourney v7 + --sref | Flux Dev + LoRA style | Nano Banana stylized prompt |
| **NSFW / gore explícito** | Flux Dev self-host (no filter) | — | — |
| **Cross-imagen style lock** | Midjourney --sref · Seedream 4.5 | Flux Kontext | Recraft style presets |

### 2.3 Especialistas (cuándo activar UN modelo niche sobre el general-purpose)

| Trigger | Especialista | Razón explícita |
|---|---|---|
| Personaje habla on-screen (creature, narrator face) | Hedra Character-3 | Lipsync 9.5/10; bate a Veo/Kling para portrait talking |
| Kling lipsync sale mal en clip ya generado | Sync.so | Post-process: reemplaza solo región boca |
| Necesitás dolly zoom, crash zoom, FPV chase deterministic | Higgsfield DoP | Parametric stacked camera moves únicos |
| Misma motion exacta en 2 clips diferentes (pose transfer) | Wan 2.2 Animate / Animate-X | Skeleton-driven identity lock |
| Misma cara en 8 escenas con lighting drástico | Nano Banana Pro / Seedream 4.5 Sequence Mode | Multi-image conditioning cross-scene |

### 2.4 Decision update — harto movimiento + budget tight (añadido 2026-05-16)

| Use-case | Default | Razón |
|---|---|---|
| **Harto movimiento (multi-char motion + camera tracking) + budget tight** | **Hailuo 02 con premium prompt** > Kling Turbo Pro | Mismo result, ~1/3 del cost. Validado caso cabina-14 (2026-05-16). Requiere PREMIUM PROMPT obligatorio (§ 2.5). |
| **Establishing shot >2s sin budget para Kling** | **Hailuo / Seedance Lite con premium prompt** | Reemplaza Ken Burns (que ahora es fallback per hard rule #7). Premium prompt cierra gap quality. |

### 2.5 Premium prompt template — cheap tier compensation (añadida 2026-05-16)

**Conexión model-selection (lo único de este doc):** cuando la matriz § 2.1 / § 2.4 te baja a Hailuo / Seedance Lite / Wan-AI / cheap tier (motion narrativo, harto-movimiento budget-tight, establishing >2s sin budget Kling), el prompt **DEBE** ser premium 5-block para cerrar el gap de calidad vs tier HERO. Sin esto, cheap model produce slop y la decisión de bajar de tier no se sostiene.

> 📐 Premium 5-block prompt body (subject+camera+lighting+atmosphere+style, HR#20) canónico → `<format>-format/INGENIERO-PAUTA-MASTER § 5.7`.

**Anti-pattern (rationale de la conexión)**: prompt de 1 línea "Maikol uncanny en faro horror atmosphere" → cheap model produce slop. Mismo prompt expandido 5-clause + camera + lighting + literal physical mood → cheap model competitivo con tier HERO.

**Dependencia crítica del SPEC**: si SPEC v6 tiene gap en `scene_context.who_does_what` para algún shot → ENGINEER ESCALA al arquitecto antes de generar prompt. Sin scene description completa, premium prompt es imposible. Ver hard rule #20 + #21 docs/OPERATING-MANUAL.md.

---

## 3. SPEC SHEETS POR MODELO

> Formato: cada modelo en bloque autocontenido. Datos a fecha 2026-05-12. Donde dice "desconocido" = no se encontró fuente confiable.

### 3.1 PREMIUM WESTERN (5 modelos)

#### Veo 3.1 (Google DeepMind)

**Identidad**
- Vendor: Google DeepMind
- Acceso: Gemini API, Vertex AI, fal, Replicate, OpenRouter, Google Flow (web)
- Última versión + fecha: Veo 3.1 (oct 2025) + Ingredients-to-Video (nov 2025) + 4K + native vertical (ene 2026); Veo 3.1 Lite early 2026

**Specs base**
- Modalidad: t2v, i2v, multi-image-ref (Ingredients), first+last frame, scene extension
- Duración max: 8s base; extendable hasta ~140s vía chained extension (20 clips)
- Resolución / AR: 1080p nativo, 4K vía upscale; 16:9 + 9:16 nativo (no crop)

**Cost-intelligence**
- Standard 1080p w/audio: $0.40/s ($3.20 por 8s)
- Fast 1080p w/audio: $0.15/s ($1.20 por 8s)
- Standard 4K w/audio: $0.60/s
- Retry rate típico: ~1.3-1.5x (mejor que Pika/Luma; main driver = censorship trips)

**Quality forensics**
- Fortalezas: ad-grade visuals, product reveals, multi-image character lock vía Ingredients, audio nativo sincronizado + lipsync (<120ms latency), vertical sin crop loss
- Debilidades: hands/fingers/fine text glitches; geometry drift en physics complejas; filter estricto rechaza horror/violence/anatomy
- Prompt adherence: 9/10 — #2 detrás de Sora 2 en physics fidelity

**Pipeline-fit**
- Character consistency: Ingredients-to-Video — hasta 3-4 reference images
- First/last frame: yes
- Camera control: prompt-only (responde a lenguaje cinematográfico)
- Audio nativo: YES — dialogue, ambient, SFX, music sincronizados

**Real-world constraints**
- NSFW/horror: restrictive (zero NSFW; dual-layer filter input + output; over-flags horror y violencia cinematográfica)
- 9:16 nativo: yes (full-res)
- Watermark: SynthID invisible (sin watermark visible en API pagada)
- Licencia comercial: yes

**Evidence**
- Video Arena t2v: #2 Elo 1100 (May 2026, detrás de Grok + Seedance)
- Video Arena i2v: #4-5 Elo 1081-1087
- Refs: [Veo 3.1 pricing](https://www.aifreeapi.com/en/posts/veo-3-1-pricing-per-second-gemini-api) · [Ingredients-to-Video](https://blog.google/innovation-and-ai/technology/ai/veo-3-1-ingredients-to-video/) · [Artificial Analysis](https://artificialanalysis.ai/video/leaderboard/text-to-video)

---

#### Sora 2 Pro (OpenAI) — ⛔ DEPRECATING

**Identidad**
- Vendor: OpenAI
- Acceso: API en sunset (sep 24 2026); web/app cerrado abril 26 2026
- Última versión: sora-2-pro-2025-10-06 (NO Sora 3; modelo siendo sunset)

**Specs base**
- Modalidad: t2v, i2v (i2v bloquea real human faces en consumer app)
- Duración max: 10s / 15s / 25s (Pro tier)
- Resolución / AR: 1024p vía API (1080p vía ChatGPT Pro); 16:9 + 9:16

**Cost-intelligence**
- Pro 720p: $0.30/s
- Pro 1024p: $0.50/s ($5.00 por 10s)
- Standard 720p: $0.10/s
- Retry rate: ~1.8-2.5x (alto por content moderation)

**Quality forensics**
- Fortalezas: cinematic moody lighting, film-grain texture, physics simulation (best-in-class objects), spatial audio
- Debilidades: heavy content filter, watermark obligatorio, prompt drift en prompts detallados
- Prompt adherence: 9/10 short prompts, 7/10 detallados

**Pipeline-fit**
- Character consistency: world-state persistence intra-generation; no multi-image
- First/last frame: no
- Camera: prompt-only
- Audio nativo: YES (spatial best-in-class)

**Real-world constraints**
- NSFW/horror: restrictive (real people, trademarked chars, celebrity, política, military blocked)
- 9:16 nativo: yes
- Watermark: SÍ obligatorio dynamic + C2PA en TODOS los tiers
- Licencia comercial: yes (mientras dure)

**Evidence**
- Video Arena: Elo 975 i2v #63 (mayo 2026) — muy debajo del marketing
- Refs: [OpenAI Help — discontinuation](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation) · [the-decoder shutdown](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/)

**⛔ Acción:** NO incorporar a pipelines nuevos. Si algo depende de Sora API, migrar antes 2026-09-24.

---

#### Runway Gen-4.5 / Gen-4 (Runway)

**Identidad**
- Vendor: Runway
- Acceso: Runway API oficial, Runway web, Adobe Firefly partner; NOT en Replicate/fal first-party
- Última versión: Gen-4.5 flagship (mid-2025 → updates 2026); Gen-4 Foundation (mar 2025); Gen-3 Alpha Turbo legacy

**Specs base**
- Modalidad: t2v, i2v, references (character lock), v2v motion transfer
- Duración max: 2-10s (4.5); 60s continuous (Gen-4 Foundation); 5-10s (Gen-3 Turbo)
- Resolución / AR: 720p nativo 24fps + upscale; Gen-4 hasta 4K; AR completo

**Cost-intelligence**
- Gen-4 Turbo: 5 credits/s (~$0.05-0.096/s)
- Gen-4 full: 12 credits/s (~$0.12-0.23/s)
- Retry rate: ~1.2-1.5x — entre los más bajos del campo (72% usable rate first pass)

**Quality forensics**
- Fortalezas: **character consistency from single ref (95%+)**, cinematic camera moves, environment coherence, controlled motion, large camera moves nativos
- Debilidades: face consistency drifts on long clips, quality degrada en últimos segundos de 10s, no lipsync nativo, choreography compleja menos confiable
- Prompt adherence: 9/10 (Gen-4.5 = #1 Video Arena per Runway/AITA)

**Pipeline-fit**
- Character consistency: Gen-4 References — single-image lock, multi-character via separate refs
- First/last frame: yes (keyframe + end-frame en 4.5)
- Camera control: YES — dolly zoom, pan, tilt, truck en UI + node-based
- Audio nativo: partial — shot-reverse-shot handling; native audio rolling out pero behind Veo/Sora; lipsync vía Act-One separado

**Real-world constraints**
- NSFW/horror: moderate (más permisivo que Sora/Veo, menos que Kling)
- 9:16 nativo: yes
- Watermark: no en paid plans
- Licencia comercial: yes (Basic $12/mo+)

**Evidence**
- Video Arena: Gen-4.5 #1 overall T2V per Runway/AITA citation
- Refs: [Runway Gen-4.5 help](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5) · [pricing](https://fairstack.ai/blog/runway-pricing) · [character consistency guide](https://selfielab.me/blog/runway-gen-4-character-consistency-guide-20260215)

---

#### Pika 2.5 (Pika Labs)

**Identidad**
- Vendor: Pika Labs
- Acceso: Pika web (primario), fal.ai (Pika 2.2; 2.5 limited third-party); NO Replicate oficial
- Última versión: Pika 2.5 (late 2025/2026); 2.2 en Standard plan

**Specs base**
- Modalidad: t2v, i2v (Pikaframes start+end), v2v Pikaffects, lipsync
- Duración max: 5/10/15/20/25s
- Resolución / AR: 480p (Free) / 720p (Standard) / 1080p (Pro); 7 ARs nativos

**Cost-intelligence**
- Subscription-only: Standard $8-10/mo (700 credits)
- ~3 credits/s synced audio; 10s @ 1080p ≈ 80 credits ≈ $0.88-$1.10
- $/s efectivo: ~$0.03-0.05/s Pro tier
- Retry rate: ~2-3x — el más alto del comparison (alta variance, prompt adherence débil)

**Quality forensics**
- Fortalezas: Pikaffects creativos (melt/explode/swap), micro-movimientos, scene composition, lipsync, fast turnaround (<90s)
- Debilidades: detrás de Runway/Sora/Veo en photoreal, lucha con multi-character, "skips elements" en prompts complejos, alta variance
- Prompt adherence: 5-6/10 en 2.5 (mejora vs 2.2 pero todavía detrás de leaders)

**Pipeline-fit**
- Character consistency: i2v single image (modo más fuerte)
- First/last frame: YES (Pikaframes)
- Camera control: prompt-only + Pikaffects motion library
- Audio nativo: YES — SFX auto-matched + lipsync

**Real-world constraints**
- NSFW/horror: moderate-restrictive
- 9:16 nativo: yes
- Watermark: free-tier obligatorio; paid clean
- Licencia comercial: yes Standard+ ($8/mo)

**Evidence**
- Video Arena: NO en top 5 mayo 2026 (Pika perdió frontrunner status)
- Refs: [Pika 2.5 guide](https://pikaslabs.com/pika-2-5/) · [review Genra](https://genra.ai/blog/pika-2-5-complete-guide-review)

---

#### Luma Ray3.14 / Ray 3 (Luma Labs)

**Identidad**
- Vendor: Luma Labs
- Acceso: Dream Machine web, Luma API, fal.ai, Replicate
- Última versión: **Ray3.14 (ene 26 2026)** — native 1080p, 4x faster, 3x cheaper

**Specs base**
- Modalidad: t2v, i2v, v2v (Ray3 Modify), keyframe start+end, character ref, scene extension
- Duración max: 5s base, extend hasta 30s vía Smart Extensions
- Resolución / AR: **1080p nativo solo en 16:9; 9:16 portrait CAPADO a 720p** (limitación crítica para Reels); 4K upscale; HDR + EXR

**Cost-intelligence**
- Ray3.14 540p: 50 credits / 5s, 100 credits / 10s
- Ray 2 ~$0.71 por 5s @ 720p ($0.32/Mpx)
- fal ~$0.10/s para Ray 2
- Ray3.14 estimado ~$0.05-0.08/s @ 720p
- Retry rate: ~1.4x (72% usable rate reportado)

**Quality forensics**
- Fortalezas: cinematic HDR (único HDR-nativo), reasoning sobre scene logic, smooth motion, scene extension a 30s con identity/physics persistence, hybrid v2v
- Debilidades: **portrait/9:16 capped at 720p** (vs 1080p horizontal — costly para Reels); voice quality robótico inconsistente; multi-shot character consistency requiere first-frame workaround
- Prompt adherence: 8/10

**Pipeline-fit**
- Character consistency: Character Reference (single-image) + keyframe anchoring
- First/last frame: yes
- Camera control: vía keyframe start+end + prompt
- Audio nativo: yes (Ray 2/3) — pero voice quality inconsistente

**Real-world constraints**
- NSFW/horror: moderate (más permisivo que Veo/Sora)
- 9:16 nativo: yes pero capado a 720p (regression crítica)
- Watermark: free tier sí; paid no
- Licencia comercial: yes Plus $30/mo+

**Evidence**
- Video Arena: NO top 5 mayo 2026
- Refs: [Ray3 eval](https://lumalabs.ai/blog/engineering/ray3-eval) · [Ray3.14 BusinessWire](https://www.businesswire.com/news/home/20260126744711/en/Luma-AI-Launches-Ray3.14-Eliminating-Quality-Speed-Cost-Tradeoff-in-Generative-Video)

---

### 3.2 PREMIUM CHINESE (10+ modelos)

#### Kling 2.5 Turbo Pro (Kuaishou) — DEFAULT ACTUAL DEL PROYECTO

**Identidad**
- Vendor: Kuaishou
- Acceso: Replicate (`kwaivgi/kling-v2.5-turbo-pro`), fal, WaveSpeed, KlingAI API, web
- Última versión: Kling 2.5 Turbo Pro (sept 2025) — superseded por 2.6 Pro (audio) y 3.0 (feb 2026) pero **sigue siendo el cost/quality sweet spot**

**Specs base**
- Modalidad: t2v + i2v (i2v dominante; soporta first-frame + last-frame keyframe)
- Duración max: 5s o 10s nativo
- Resolución / AR: 1080p; 16:9, 9:16, 1:1 nativos

**Cost-intelligence**
- $0.35 por 5s; $0.70 por 10s en fal/Replicate
- $/s: **$0.07/s**
- Retry rate: ~1.3-1.6x para horror/dark (filter trips); 1.0-1.2x para safe content

**Quality forensics**
- Fortalezas: cinematic lighting con specular highlights + subsurface scattering; physics-grounded motion (no float); subject permanence ~60s; camera moves intentional; close-up faces sólidos
- Debilidades: **safety filter agresivo en horror/gore/violence** (#1 production blocker); generic "Ken Burns-ish" en prompts débiles; crowds y fast hand-object falla
- Prompt adherence: 8/10

**Pipeline-fit**
- Character consistency: image-ref vía first-frame i2v (single image; Kling 3.0 agregó multi-image, 2.5 NO)
- First/last frame: YES (`image` start + `last_image` end)
- Camera control: prompt-only + CFG/guidance_scale (sin discrete dolly/pan/zoom params como 1.6)
- Audio nativo: NO (Kling 2.6+ sí; 2.5 silent)

**Real-world constraints**
- NSFW/horror: **restrictive** (no NSFW toggle; trips on blood, weapons-at-people, demon close-ups, females in distress). Permitido: implied horror, environmental dread, monsters in shadow. Bloqueado: explicit gore, on-screen wounds.
- 9:16 nativo: yes (true)
- Watermark: no en API pagada
- Licencia comercial: yes

**Evidence**
- Video Arena i2v: **Elo 1283** (top-10) — supera ligeramente a Kling 3.0
- Refs: [Kling 2.5 Turbo "way more censored"](https://www.gstory.ai/blog/kling-2-5-turbo/) · [Curious Refuge review](https://curiousrefuge.com/blog/kling-25-turbo-ai-video-generator-review) · [getimg comparison](https://getimg.ai/blog/kling-2-5-vs-2-vs-1-6-comparison) · [Artificial Analysis i2v](https://artificialanalysis.ai/video/leaderboard/image-to-video)

#### Tactical notes (migrated from kling_rules.md memoria 2026-05-15)

**Default model in this project**: `kwaivgi/kling-v2.5-turbo-pro` (Replicate).

**Schema diffs vs v2.0** (impacts `ai-video video` → `build_input()`):
- `cfg_scale` REMOVIDO (deprecated, ignored if sent)
- `guidance_scale` deprecated / ignored
- Accepts: `start_image`, `prompt`, `duration` (5 or 10), `negative_prompt`
- New: `end_image` optional, `aspect_ratio` (ignored if start_image present)

**Pricing**: $0.07/s → tier 5s = $0.35, tier 10s = $0.70.

**Duration matching guidelines**:
- scene_duration ≤ 3s: Ken Burns o accept tier 5s subutilizado
- 3-4s: tier 5s
- 5-9s: tier 10s
- >10s: 2 clips + crossfade o hold last frame

Tier 5s puede usarse para data-duration <3s si se quiere consistencia visual (override regla "≤3s NO Kling" en primeros 30s — ver `animation_30s_rule.md` memoria). Pero <2s aún no compensa el costo.

**Close-up cara con v2.5 turbo pro + prompt restrictivo** (validated h6-santi-face mina-abandonada v10):
> "subtle head tilt, NO lip movement, eyes blink, mouth stays completely still and closed, slight breathing of shoulders, [emotional tone] atmosphere"

Validate frame-by-frame en t=0.3, 1.0, 1.5, 2.0, 2.3, 2.5: identidad y forma preservadas, blink limpio sin morphing.

**Iteration efficiency — no quemar plata en Kling**:

Antes de prompt-engineer Kling, leer el skill del FORMATO específico (`horror-choice-format`, `documental-format`, etc.) para entender qué motion preserva la narrativa vs qué la rompe.

Lessons from bosque-abandonado intro v6 ($1.40 perdidos):
1. **v2 spoiler**: animar Berni inclinándose hacia Yonaiker. Sin leer formato primero, no se sabía que los ROLES APARENTES son load-bearing — motion que los refuerza = ✅, interacción entre personajes = ❌ (spoilea twist).
2. **v3 over-correction**: tras spoiler de v2, quitar TODO character motion (solo atmospheric). Problema real era INTERACCIÓN, no char motion en sí.

Rules para iteración Kling:
- **Motion que refuerza roles aparentes** (no spoiler) = ✅
- **Interacción entre personajes** que revela algo del twist = ❌
- Si una iteración falla por X razón específica, corregir SOLO X. Conservar lo bueno.
- Verificar premise del usuario antes de iterar — ej. "aburrida" → preguntar "¿quieres char motion en caras o solo más motion ambient?" antes de gastar otro Kling.

Cada job descartado = $0.35-0.70 perdido. Re-Klingear tras rewrite = 2x costo.

---

#### Kling 2.1 Master (Kuaishou)

**Identidad**
- Vendor: Kuaishou
- Acceso: Replicate (`kwaivgi/kling-v2.1-master`), fal, WaveSpeed, Kling API
- Última versión: Kling 2.1 Master (mayo 2025) — usado como "premium-quality slow path" mientras 2.5 Turbo es "fast cheap"

**Specs base**
- Modalidad: t2v + i2v
- Duración max: 5s o 10s
- Resolución / AR: 1080p; 16:9, 9:16, 1:1

**Cost-intelligence**
- $1.40 por 5s; $0.28 por second adicional (~$2.80 por 10s)
- $/s: **$0.28/s** (4x más caro que 2.5 Turbo Pro)
- Retry rate: ~1.2-1.4x (filter más blando que 2.5 pero renders 3-5x más lentos)

**Quality forensics**
- Fortalezas: "art-film director" feel — best Kling para mood/atmósfera/cinematic slow-burn; richest texture detail; cleaner first-try para prompts ambiciosos
- Debilidades: 4-5x cost vs 2.5 Turbo para marginal gain en fast-cut social; floatier en fast motion; menos crisp en full body shots
- Prompt adherence: 8/10 (slightly más interpretivo que literal — reescribe weak prompts)

**Pipeline-fit**
- Character consistency: image-ref vía i2v start frame
- First/last frame: yes
- Camera: prompt-only + CFG
- Audio nativo: no

**Real-world constraints**
- NSFW/horror: moderate-restrictive (menos agresivo que 2.5; acepta atmospheric horror, masked figures, implied threat)
- 9:16 nativo: yes
- Watermark: no API
- Licencia comercial: yes

**Evidence**
- Video Arena: no top 15 (eclipsed by 2.5/2.6/3.0)
- Refs: [agiyes 2.1 vs 2.1 Standard](https://www.agiyes.com/aireviews/kling-2-1-standard-vs-kling-2-1-master/) · [302.AI Kling 2.1 vs 2.0/1.6](https://medium.com/@302.AI/302ai-benchmarks-kling-2-1-vs-2-0-1-6-does-2-1-version-truly-win-42c47c43d61f)

---

#### Kling 1.6 Pro (Kuaishou) — LEGACY w/ CAMERA PARAMS

**Identidad**
- Vendor: Kuaishou
- Acceso: Replicate, fal, Kling API, Novita, WaveSpeed
- Última versión: Kling 1.6 (dic 2024) — kept for cheapest 1080p tier + explicit camera control params

**Specs base**
- Modalidad: t2v + i2v (i2v fue primer Kling con stable first+last frame)
- Duración max: 5s o 10s
- Resolución / AR: 1080p (Pro); 720p (Standard); 16:9, 9:16, 1:1

**Cost-intelligence**
- ~$0.49 por 5s 1080p i2v (Replicate); $0.098/s en fal
- ~$0.46 en Novita
- Standard: ~$0.20-0.25 por 5s
- Retry rate: ~1.5-1.8x (quality menor → más re-rolls; pero filter muy permisivo)

**Quality forensics**
- Fortalezas: **cheapest 1080p Kling**; **explicit camera parameter control** (`camera_type`: simple, down_back, forward_up, right_turn_forward, left_turn_forward + magnitude); permissive content policy (pre-2.5 filter)
- Debilidades: textures "plastic" vs 2.x; physics débil; faces poco detail at distance; outdated motion realism
- Prompt adherence: 6/10

**Pipeline-fit**
- Character consistency: i2v image-ref
- First/last frame: YES (killer feature 1.6 — primer Kling con last-frame lock estable)
- Camera control: **YES nativo** — most parameter-controllable de toda la familia Kling
- Audio nativo: no

**Real-world constraints**
- NSFW/horror: **permissive (relativo a 2.5)** — acepta moodier horror prompts que 2.5 rechaza
- 9:16 nativo: yes
- Watermark: no API
- Licencia comercial: yes

**Evidence**
- Refs: [Replicate kling-1.6-pro](https://replicate.com/kwaivgi/kling-v1.6-pro) · [getimg 1.6 vs 2.0](https://getimg.ai/blog/what-is-kling-ai-comparing-kling-1-6-standard-pro-and-2-0-master) · [Novita i2v](https://blogs.novita.ai/kling-1-6-i2v/)

**Cuándo usar:** B-roll cheap 1080p + camera moves específicos via params + horror content que 2.5 bloquea.

---

#### Kling 3.0 / 3.0 Omni (Kuaishou) — NEWER

**Identidad**
- Vendor: Kuaishou
- Acceso: fal (`fal-ai/kling-3`), Kling API (Ultra early access), Replicate rollout
- Última versión: **Kling 3.0 + Omni + Image 3.0 (2026-02-05)**

**Specs base**
- Modalidad: t2v + i2v + multi-shot storyboard (Omni); audio nativo
- Duración max: hasta 15s por shot; multi-shot chains
- Resolución / AR: 1080p Pro / 720p Standard; Image stills 2K/4K; 16:9 + 9:16

**Cost-intelligence**
- ~$0.10-0.17/s con audio (similar a 2.6 Pro pricing)
- Retry rate: desconocido (too new)

**Quality forensics**
- Fortalezas: **audio lipsync nativo en 5+ idiomas**; multi-shot storyboard con per-shot direction (Omni); 95% character coherence cross-shots; Motion Brush; competitive con Veo 3.1
- Debilidades: censorship filters heredados 2.5/2.6 (posiblemente tighter); early-access bottleneck
- Prompt adherence: 8.5/10

**Pipeline-fit**
- Character consistency: multi-shot lock mejorado (Omni)
- First/last frame: yes
- Camera control: per-shot spec en Omni
- Audio nativo: **YES** sincronizado multi-lingual

**Real-world constraints**
- NSFW/horror: restrictive (filter family Kling)
- 9:16 nativo: yes
- Watermark: no API pagada
- Licencia comercial: yes

**Evidence**
- Video Arena t2v: #3 Elo 1249; Omni #4 Elo 1233
- Video Arena i2v: #7 Elo 1280 (LIGERAMENTE debajo de Kling 2.5 Turbo Pro 1283)
- Refs: [Kuaishou announcement](https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be/) · [Atlas Cloud review](https://www.atlascloud.ai/blog/guides/kling-3.0-review-features-pricing-ai-alternatives) · [Curious Refuge review](https://curiousrefuge.com/blog/kling-30-review)

**Cuándo migrar de 2.5 → 3.0:** SOLO si necesitás multilingual lipsync nativo o multi-shot Omni. Para i2v puro 2.5 Turbo Pro sigue siendo igual o mejor + más barato.

---

#### Hailuo 02 + 2.3 (MiniMax)

**Identidad**
- Vendor: MiniMax
- Acceso: Replicate (`minimax/hailuo-02`), fal (`fal-ai/minimax/hailuo-02/...`, `hailuo-2.3`), MiniMax API, Hailuo web
- Última versión: **Hailuo 2.3 (2025-10-28)**, en fal desde Q4 2025

**Specs base**
- Modalidad: t2v + i2v (subject-reference / character lock)
- Duración max: 6s (1080p Pro) o 6/10s (768p Standard)
- Resolución / AR: 1080p Pro; 768p Standard; 16:9 + 9:16 nativo 1080×1920

**Cost-intelligence**
- Pro 6s 1080p: $0.48 fal ($0.08/s)
- Standard 6s 768p: $0.27 ($0.045/s)
- Replicate Standard: $0.28
- Retry rate: ~1.2-1.4x (mejor que Kling en action/physics; peor en abstract/stylized)

**Quality forensics**
- Fortalezas: **best-in-class physics realism** (cloth, momentum); state-of-the-art prompt adherence en multi-subject; facial expression + body tracking sólido; bate a Kling stiff en action
- Debilidades: solo 6s nativo at 1080p; menos "cinematic painterly" que Kling 2.1 Master; **"resists disorder"** (Curious Refuge) — daña horror caótico; struggles con stylized non-realistic
- Prompt adherence: 9/10

**Pipeline-fit**
- Character consistency: subject-reference mode — explicit character ref image input + facial recognition + body tracking
- First/last frame: i2v start frame; last-frame partial en 2.3
- Camera control: prompt-only (2.3 refined adherence)
- Audio nativo: no (02); partial SFX en 2.3

**Real-world constraints**
- NSFW/horror: **moderate — más permisivo que Kling 2.5** para dark content. Genera creature reveals, environmental gore, masked figures con weapons. Bloqueado: sexual + graphic on-person wounds. ⚠️ **CLAIM "go-to cuando Kling rechaza" = WEAK evidence — ver § 4.2**
- 9:16 nativo: yes (1080×1920 true)
- Watermark: no API; web free sí
- Licencia comercial: yes

**Evidence**
- Video Arena: no top 15 actual (Hailuo 2.3 listed pero abajo de Seedance/Kling 3.0); previo top-5 mid-2025
- Refs: [MiniMax 2.3 announcement](https://www.minimax.io/news/minimax-hailuo-23) · [fal 2.3](https://blog.fal.ai/minimax-hailuo-2-3-is-now-available-on-fal/) · [Curious Refuge review](https://curiousrefuge.com/blog/minimax23-ai-video-generator-review) · [Levelsio Kling fallback tweet (Oct 2024)](https://x.com/levelsio/status/1847252618457780464)

---

#### Seedance 2.0 (ByteDance / Seed) — TOP-2 I2V CURRENT

**Identidad**
- Vendor: ByteDance (Dreamina / Seed)
- Acceso: Replicate, fal, Atlas Cloud, WaveSpeed, BytePlus API, Dreamina web
- Última versión: **Seedance 2.0 (2026-02-12)** — flagship actual

**Specs base**
- Modalidad: t2v + i2v + multi-shot + reference-to-video (hasta 9 ref images, 3 video clips, 3 audio files single pass)
- Duración max: hasta 15s por shot, chainable
- Resolución / AR: 1080p+; 16:9, 9:16, 1:1

**Cost-intelligence**
- 2.0 Pro: ~$0.247/s Atlas Cloud
- 1.0 Pro 1080p 5s: ~$0.62 fal (~$0.12/s)
- 1.0 Pro Fast: ~$0.05/s
- Retry rate: ~1.2x (nails prompt first try más que Kling)

**Quality forensics**
- Fortalezas: **best multi-shot narrative cohesion** del campo — thinks like editor, mantiene subject + style + atmosphere cross-shots; expressive content (comedy, viral); fluid camera work; **audio nativo + multi-shot single pass en 2.0**
- Debilidades: menos "stiff cinematic" para static product; puede over-stylize cuando se quiere literal realism; text in-video falla 9/10 veces (usar captions HyperFrames)
- Prompt adherence: 9/10 — top-3 del campo

**Pipeline-fit**
- Character consistency: 2.0 — hasta 9 reference images multi-character lock + multi-shot consistency
- First/last frame: yes (1.0 Pro start frame; 2.0 expanded)
- Camera control: prompt-only strong adherence; 2.0 shot-level direction
- Audio nativo: **YES en 2.0** + multi-shot

**Real-world constraints**
- NSFW/horror: moderate (más permisivo que Kling, comparable a Hailuo); ByteDance modera pero acepta horror atmospherics
- 9:16 nativo: yes
- Watermark: no API
- Licencia comercial: yes

**Evidence**
- Video Arena t2v: **#2 Elo 1273** (Dreamina Seedance 2.0 720p)
- Video Arena i2v: **#2 Elo 1347** (overtaken solo por HappyHorse-1.0)
- Refs: [Wikipedia Seedance 2.0](https://en.wikipedia.org/wiki/Seedance_2.0) · [fal Seedance 2.0](https://fal.ai/seedance-2.0) · [aimlapi 2.0 vs 1.5](https://aimlapi.com/blog/seedance-2-0-vs-seedance-1-5-pro---bytedances-breakthrough-multimodal-ai-video-models-2026) · [MattVidPro review](https://www.classcentral.com/course/youtube-seedance-2-0-feels-like-old-sora-but-better-fight-scenes-are-finally-good-528488)

---

#### HappyHorse-1.0 (Alibaba ATH) — NEW #1 I2V

**Identidad**
- Vendor: Alibaba ATH
- Acceso: desconocido (rollout muy reciente, abril 2026)
- Última versión: HappyHorse-1.0 (abril 2026)

**Specs base**
- Modalidad: i2v (al menos)
- Duración max: desconocido
- Resolución / AR: desconocido

**Cost-intelligence**
- Pricing: desconocido
- Retry rate: desconocido (too new)

**Quality forensics**
- Fortalezas: **#1 i2v Elo 1395 en Artificial Analysis** (mayo 2026), por encima de Seedance 2.0
- Debilidades: sin reviews independientes; falta data en YouTube; sin test side-by-side público
- Prompt adherence: desconocido

**Pipeline-fit**
- Todos los campos: desconocido (rollout muy reciente)

**Real-world constraints**
- Todos los campos: desconocido

**Evidence**
- Video Arena i2v: **#1 Elo 1395** (https://artificialanalysis.ai/video/leaderboard/image-to-video)
- Refs: [WaveSpeed HappyHorse vs Seedance comparison](https://wavespeed.ai/blog/posts/happyhorse-vs-seedance-2-0-comparison-2026/) · [Atlas Cloud HappyHorse vs Seedance](https://www.atlascloud.ai/blog/guides/happy-horse-1-vs-seedance-2)

**⚠️ ACCIÓN:** Hacer A/B test propio (1-2 prompts horror-choice) antes de defaultear o ignorar. Modelo nuevo, leaderboard fuerte, falta validación real-world.

---

#### Wan 2.2 / 2.5 / 2.7 (Alibaba)

**Identidad**
- Vendor: Alibaba (Wan team / Tongyi)
- Acceso: **Wan 2.2** open-weight Apache 2.0 (HF, GitHub, ComfyUI nativo), Replicate, fal, WaveSpeed. **Wan 2.5** API-only (Alibaba Cloud, fal, WaveSpeed, Kie.ai) — NOT open-weights. **Wan 2.7** Apache 2.0 open-weight again (abril 2026)
- Última versión: **Wan 2.7 suite (2026-04)** — full open-weight multi-model

**Specs base**
- Modalidad: t2v + i2v + ref2v multi-ref + s2v (speech-to-video lip-sync) + v2v editing
- Duración max: 5s (2.2/2.5); hasta 15s (2.6/2.7)
- Resolución / AR: hasta 1080p (2.5 4K nativo); 16:9, 9:16, 1:1, 4:3, 3:4 (2.6+)

**Cost-intelligence**
- Wan 2.5 fal: $0.05/s (480p), $0.10/s (720p), $0.15/s (1080p)
- Wan 2.1 i2v: $0.20 (480p) / $0.40 (720p)
- Wan 2.7 API: desde $0.10/s
- **Self-host 2.2/2.7: free + GPU time** (RTX 4090+ para iteración rápida)
- Retry rate: ~1.3-1.5x managed; mayor en self-host vanilla

**Quality forensics**
- Fortalezas: **ÚNICO premium family con TRUE open weights** (2.2 + 2.7) → unlimited use, fine-tuning, NSFW capability, local privacy; 4K nativo (2.5); audio sync (2.5+); 2.7 con first-last-frame + multi-ref (5 clips) + instruction-based editing
- Debilidades: open-weight 2.2/2.7 requieren GPU strong; raw quality debajo de Kling 2.5 Turbo sin LoRA fine-tuning; 2.5 closed API rompe tradición open-weight
- Prompt adherence: 7.5/10 managed; 6.5-7/10 self-host vanilla

**Pipeline-fit**
- Character consistency: multi-reference (2.7 hasta 5 video refs); LoRA training para identity lock total
- First/last frame: yes en 2.7 (FLF2V)
- Camera control: prompt-based strong; ComfyUI workflows exponen más knobs
- Audio nativo: yes 2.5+; voice clone en 2.7

**Real-world constraints**
- NSFW/horror: **most permissive de las 6 familias** — open weights = no API filter self-host; LoRAs community cubren horror/gore directly. **#1 razón horror creators usan Wan sobre Kling.**
- 9:16 nativo: yes (2.6+)
- Watermark: no
- Licencia comercial: yes (Apache 2.0 — unrestricted commercial)

**Evidence**
- Video Arena: Wan 2.5 debutó #5 t2v / #8 i2v (oct 2025); Wan 2.2 lidera VBench 84.7% open-source category
- Refs: [Wan 2.7 release](https://www.cliprise.app/news/wan-2-7-video-release) · [Wan 2.5 NSFW article](https://www.creativepadmedia.com/does-kling-ai-allow-nsfw-no-but-wan-2-5-does/) · [Wan-Video GitHub](https://github.com/Wan-Video/Wan2.2) · [SeaArt Wan 2.7 review](https://www.seaart.ai/blog/wan-2-7-review)

**Honest caveat (v2):** Wan 2.6 ranks 6.7/10 en Curious Refuge — debajo de TODOS los modelos pagos. Para 9.7 bar = experimentation tier, NO production tier todavía.

---

#### Hunyuan Video 1.5 (Tencent)

**Identidad**
- Vendor: Tencent
- Acceso: Open-weight (HF `tencent/HunyuanVideo-1.5`, GitHub), self-host RTX 4090 (75s/clip), fal, Replicate, WaveSpeed
- Última versión: **HunyuanVideo-1.5 (2026-05-04)** — 8.3B params

**Specs base**
- Modalidad: t2v + i2v (separate `HunyuanVideo-I2V` checkpoint)
- Duración max: 6s nativo (longer con extension workflows)
- Resolución / AR: 720p nativo 1.5 (lighter model); 1080p en fal managed; 16:9, 9:16, 1:1

**Cost-intelligence**
- fal: $0.075/s (1.5 t2v) → ~$0.45 por 6s
- WaveSpeed: $0.02/s (480p) / $0.04/s (720p)
- Self-host: ~$0.04/clip en 4090 (GPU cost only)
- Retry rate: ~1.5-2x vanilla

**Quality forensics**
- Fortalezas: **fully open + uncensored** con "cozy" community builds; lightweight (24GB consumer GPU); fast local iteration; large LoRA ecosystem; **de-facto base para AI video deepfake/horror/NSFW**
- Debilidades: raw quality menor vs Kling 2.5+/Seedance 2.0; weaker physics; no production cinematic bar out-of-box
- Prompt adherence: 6.5/10 vanilla; 7.5/10 con LoRA + workflow

**Pipeline-fit**
- Character consistency: LoRA-based (train custom char LoRA → rock-solid identity)
- First/last frame: partial (community ComfyUI workflows agregan)
- Camera control: prompt-only; ComfyUI custom nodes
- Audio nativo: no

**Real-world constraints**
- NSFW/horror: **most permissive de TODO el universo** self-hosted con cozy builds — no filter, no rejection. **⚠️ CAVEAT (v2):** community "cozy" builds remueven filtros pero el modelo NO está entrenado en explicit content — es "uncensored by filter removal", no "explicit-capable". Para horror (blood, gore, fear): SÍ funciona. Para true NSFW sexual: no es lo que la gente piensa.
- 9:16 nativo: yes
- Watermark: no
- Licencia comercial: yes (Tencent permissive license)

**Evidence**
- Video Arena: HunyuanVideo-1.5 listed AA con own page
- Refs: [HF Tencent](https://huggingface.co/tencent/HunyuanVideo-1.5) · [Promptus "#1 Open-Source Uncensored"](https://www.promptus.ai/blog/hunyuan-video-1-5) · [Unite.ai deepfakes article](https://www.unite.ai/the-rise-of-hunyuan-video-deepfakes/) · [Civitai uncensored workflows](https://civitai.com/articles/9920/no-limits-no-filters-start-from-scratch-to-fully-unlock-hunyuan-videos)

---

#### Vidu Q3 (Shengshu Technology)

**Identidad**
- Vendor: Shengshu Technology (Tsinghua spinoff; Baidu + Ant Group backed)
- Acceso: fal, WaveSpeed, Vidu API (`platform.vidu.com`), Vidu web
- Última versión: **Vidu Q3 (2026-01)** — industry-first long-form native audio+video single pass

**Specs base**
- Modalidad: t2v + i2v + **reference-to-video (hasta 7 reference images)** — signature mode; start-end-to-video
- Duración max: 5s (Q1), 8s (Q2), **16s nativo (Q3)** single pass
- Resolución / AR: 1080p; 24fps; 16:9, 9:16, 4:3, 3:4, 1:1

**Cost-intelligence**
- Q1 R2V: $0.10; Q2 Pro 720p: $0.10 base + $0.05/s; Q2 Pro 1080p: $0.30 + $0.10/s
- Q3 desconocido exacto (premium tier per fal)
- $/s: ~$0.05-0.10/s (Q2 Pro); ~$0.10-0.15/s (Q3 estimado)
- Retry rate: ~1.4x

**Quality forensics**
- Fortalezas: **reference-to-video industry-best** (hasta 7 refs blended: caras + props + escenas); Q3 = first long-form (16s) con audio nativo single pass; strong para anime/stylized; #1 VBench at Q1 launch; AI SFX 48kHz
- Debilidades: menos photoreal que Kling/Hailuo/Seedance en live-action; physics weaker; audience-specific (best anime/stylized/narrative VFX vs realistic horror)
- Prompt adherence: 7.5/10 (strong en references; weaker freeform t2v)

**Pipeline-fit**
- Character consistency: **multi-image reference (hasta 7)** — best-in-class via R2V mode
- First/last frame: yes (start-end-to-video Q1+)
- Camera: prompt-only; per-shot direction Q3
- Audio nativo: **YES Q3** (audio+video single pass 16s 48kHz)

**Real-world constraints**
- NSFW/horror: moderate (permissive en stylized/anime horror; stricter en photoreal violence; Chinese platform filtering)
- 9:16 nativo: yes
- Watermark: no API
- Licencia comercial: yes

**Evidence**
- Video Arena t2v: **#6 Vidu Q3 Pro Elo 1225**
- Video Arena i2v: **#5 Vidu Q3 Pro Elo 1287**
- Refs: [PRNewswire Q2 launch](https://www.prnewswire.com/news-releases/vidu-launches-q2-reference-to-video-pioneering-a-new-era-of-high-consistency-and-creative-control-302590002.html) · [Vidu Q3](https://www.vidu.com/vidu-q3) · [deevid.ai review](https://deevid.ai/blog/vidu-q3-review)

---

### 3.3 OPEN-SOURCE + NICHE SPECIALISTS (8 modelos)

#### LTX-Video 2.3 (Lightricks) — open-source general

**Identidad**
- Vendor: Lightricks
- Acceso: HF weights, GitHub, ComfyUI, fal, WaveSpeed, LTX Desktop local, Replicate
- Última versión: **LTX-2.3 (22B, marzo 2026)** — adds desktop local runtime; LTX-2 fully open-sourced ene 2026

**Specs base**
- Modalidad: t2v, i2v, v2v + audio sync nativo en 2.3
- Duración max: ~60s
- Resolución / AR: hasta 1088×1920 (1080p 9:16) en RTX 5090; 736×1280 / 768×1280 práctico; 9:16 nativo

**Cost-intelligence**
- Self-host: GPU cost only (RTX 5090: ~22s gen para 5s i2v — 5.7x más rápido que Wan 2.2)
- fal: ~$0.10-0.30/clip 5s
- $/s: ~$0.02-0.06/s API; $0 marginal self-host
- Retry rate: desconocido

**Quality forensics**
- Fortalezas: **SPEED + 9:16 vertical native + 60s long-form + built-in audio sync 2.3**; best open-source para draft volume
- Debilidades: hands + fine detail debajo Wan 2.2; camera stability menor; "AI float" en slow scenes
- Prompt adherence: 7/10

**Pipeline-fit**
- Character consistency: i2v from ref image; community LoRAs disponibles
- First/last frame: yes (keyframe conditioning)
- Camera: prompt-driven (no parametric)
- Audio nativo: YES en 2.3 (raro en open-source)

**Real-world constraints**
- NSFW/horror: open weights = no filter self-host
- 9:16 nativo: YES first-class
- Watermark: none self-host
- Licencia comercial: Apache 2.0 — free para orgs <$10M annual revenue, custom license arriba

**Evidence**
- Refs: [LTX GitHub](https://github.com/Lightricks/LTX-Video) · [LTX-2.3 vs Wan 2.2 benchmark](https://zenn.dev/toki_mwc/articles/ltx23-vs-wan22-i2v-benchmark-rtx5090) · [LTX 9:16 portrait guide](https://wavespeed.ai/blog/posts/ltx-2-3-portrait-video-9-16-workflow-2026/)

**¿Vale la pena vs Kling/Veo?** SÍ para BULK generation cuando budget importa y shot no es hero — 10-20 draft variants a ~$0.20 c/u vs $5 Kling. Para hero shots: stick Kling.

---

#### Mochi 1 (Genmo) — SKIP

**Identidad**
- Vendor: Genmo
- Acceso: HF, GitHub, Replicate, genmo.ai/play
- Última versión: Mochi 1 preview (oct 2024, 10B params); HD 720p announced pero open weights siguen siendo 480p preview en mayo 2026

**Specs base**
- Modalidad: **t2v only** (NO i2v público)
- Duración max: 5.4s @ 30fps
- Resolución / AR: 480p (open weights); **AR NO nativamente flexible** — 848×480 landscape típico; 9:16 requiere crop

**Cost-intelligence**
- ~$0.42/run Replicate; self-host requiere 4x H100 (reducido a 1x H100 80GB con optimizaciones)
- ~$0.08/s Replicate
- Retry rate: alto (strict auto NSFW filter)

**Quality forensics**
- Fortalezas: **motion quality #1 open-source** (fluid human motion, physics, hair/fur sim); top-tier prompt adherence (~80%)
- Debilidades: 480p ceiling KILLS production; NO I2V (text only); poor animated/stylized; landscape-only
- Prompt adherence: 8/10

**Pipeline-fit**
- Character consistency: NONE (no I2V, no ref image)
- First/last frame: no
- Camera: prompt-only
- Audio nativo: no

**Real-world constraints**
- NSFW/horror: managed strict; self-host bypass (TripleX fine-tunes)
- 9:16 nativo: **NO** — crop from landscape
- Watermark: none
- Licencia comercial: Apache 2.0

**Evidence**
- Refs: [Genmo Mochi blog](https://www.genmo.ai/blog/mochi-1-a-new-sota-in-open-text-to-video) · [GitHub](https://github.com/genmoai/mochi) · [the-decoder review](https://the-decoder.com/genmo-mochi-1-a-new-benchmark-for-open-ai-video-models/)

**¿Vale la pena?** NO para este pipeline. 480p + no I2V + landscape-only = unfit para IG Reels horror. **SKIP.**

---

#### CogVideoX-1.5 5B (Tsinghua / Zhipu AI) — SKIP

**Identidad**
- Vendor: Tsinghua KEG / Zhipu AI
- Acceso: HF (zai-org/CogVideoX1.5-5B + I2V), Replicate, ComfyUI
- Última versión: CogVideoX-1.5 (nov 2024); ICLR 2025 paper; **sin major 2026 update** — community migrated a Wan 2.2 / LTX-2

**Specs base**
- Modalidad: t2v + i2v (separate weights)
- Duración max: 10s
- Resolución / AR: 768P / 1360×768; I2V soporta **arbitrary AR incluyendo 9:16**

**Cost-intelligence**
- ~$0.32/run Replicate v1.0; self-host viable 24GB GPU con quantization
- $/s: ~$0.05-0.10/s
- Retry rate: moderado

**Quality forensics**
- Fortalezas: prompt adherence sólido open-source family; flexible AR I2V; 10s competitive
- Debilidades: motion debajo LTX-2 + Wan 2.2 en 2026; I2V conditioning drifts; community migrated
- Prompt adherence: 7/10

**Pipeline-fit**
- Char consistency: I2V ref image; no native identity LoRA
- First/last frame: limited
- Camera: prompt-driven
- Audio nativo: no (CogSound separate en Qingying)

**Real-world constraints**
- NSFW/horror: open self-host no filter
- 9:16 nativo: YES vía I2V
- Watermark: none
- Licencia comercial: CogVideoX License (NOT Apache) — free commercial hasta 1M MAU

**Evidence**
- Refs: [HF CogVideoX1.5-5B](https://huggingface.co/zai-org/CogVideoX1.5-5B) · [GitHub](https://github.com/zai-org/CogVideo)

**¿Vale la pena?** Marginal — LTX-2 y Wan 2.2 lo eclipsaron. **SKIP salvo legacy LoRA pipelines.**

---

#### Stable Video Diffusion 1.1 (Stability) — SKIP

**Identidad**
- Vendor: Stability AI
- Acceso: HF (stabilityai/stable-video-diffusion-img2vid-xt), ComfyUI, NVIDIA NIM
- Última versión: SVD-XT 1.1 (feb 2024); **legacy en 2026**

**Specs base**
- Modalidad: i2v only (NO t2v)
- Duración max: ~4s (14-25 frames)
- Resolución / AR: 1024×576 landscape; **9:16 NO nativo**

**Cost-intelligence**
- Self-host GPU only (8-16GB VRAM); ~$0.01/s
- Retry rate: alto

**Quality forensics**
- Fortalezas: low VRAM accessibility, ComfyUI tutorials standard
- Debilidades: quality bajo LTX-2/Wan 2.2/Mochi; no text conditioning; 4s clips; legacy
- Prompt adherence: 4/10 (no text — motion only)

**Pipeline-fit:** todos limited
**NSFW/horror:** open no filter
**9:16:** NO — crop
**Watermark:** none
**Licencia:** Stability Community License non-commercial; commercial require membership

**Refs:** [HF SVD-XT](https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt)

**¿Vale la pena?** NO. Legacy en 2026. **SKIP completely.**

---

#### Hedra Character-3 (Hedra Labs) — TALKING-HEAD / LIPSYNC SPECIALIST

**Identidad**
- Vendor: Hedra Labs
- Acceso: Hedra Studio web, official Platform API api.hedra.com (feb 2026 launch), atlabs.ai third-party
- Última versión: Character-3 (mar 2025); updates 2026

**Specs base**
- Modalidad: **image + audio → talking video** (omnimodal: text+image+audio joint reasoning)
- Duración max: ~60s+ driven by audio
- Resolución / AR: 720p (1080p limited tier); portrait input — 9:16 viable

**Cost-intelligence**
- Credit-based: Character-3 720p = 6 credits/sec → 360 credits/min
- Creator plan $30/mo = 5,400 credits ≈ 15 min de 720p video
- **$/s: ~$0.03-0.06/s output**
- Retry rate: low en portrait; alto en non-frontal

**Quality forensics**
- Fortalezas: **BEST-IN-CLASS lipsync** — phoneme-aligned mouth, blinks, gaze shifts, brow micro-expression; funciona con illustrations + cartoons + non-human faces (raro); ahead de D-ID y HeyGen para portrait avatars
- Debilidades: full-body inconsistent; non-frontal degrada; 720p cap mayoría tiers; face debe ser detectable
- Prompt adherence: 8/10 (audio is primary driver)

**Pipeline-fit**
- Character consistency: identity preserved from input image (no training)
- First/last frame: input image acts as first frame
- Camera: minimal (head/face focus)
- Audio nativo: YES (audio IS primary driver — omnimodal arch)
- **Lipsync quality: 9.5/10** — current state of the art

**Real-world constraints**
- NSFW/horror: ToS-bounded, permite horror creature characters; explicit NSFW filtered
- 9:16 nativo: yes vía portrait
- Watermark: free tier sí; paid clean
- Licencia comercial: yes paid tiers

**Evidence**
- Refs: [Hedra pricing](https://www.hedra.com/pricing) · [Hedra vs sync.so](https://lipsync.com/compare/sync-so-vs-hedra) · [Hedra review 2026](https://www.weshop.ai/blog/hedra-ai-review-2026-the-new-king-of-talking-heads-and-ai-avatars/)

**¿Vale la pena vs Kling/Veo?** **SÍ decisivo** — Kling lipsync mediocre, Veo closed/caro. Cuando horror video necesita creature/character/narrator hablando on-screen (bruja, fantasma, doll talking-head insert) → Hedra a ~$0.05/s. Drop-in layered insert sobre Kling environment shots.

---

#### Higgsfield DoP / Cinema Studio (Higgsfield AI) — CAMERA CONTROL SPECIALIST

**Identidad**
- Vendor: Higgsfield AI
- Acceso: higgsfield.ai web, no API pública oficial — third-party API vía WaveSpeed, Segmind, Pixazo
- Última versión: DoP I2V-01-preview primary; Cinema Studio 2.0 (2026)

**Specs base**
- Modalidad: i2v con parametric camera control
- Duración max: 5s DoP; 10s con Veo/Sora backbones
- Resolución / AR: 1080p; 9:16

**Cost-intelligence**
- Third-party APIs ~$0.86/video (Segmind)
- Platform Starter $15/mo = 200 credits; Plus $39/mo = 1000 credits
- Kling 3.0 ~6 credits, Sora 2/Veo 3.1 = 40-70 credits/video
- $/s: ~$0.15-0.40/s depending on backbone

**Quality forensics**
- Fortalezas: **DETERMINISTIC parametric camera control** — dolly zoom, crash zoom, Snorricam, crane, FPV drone, bullet-time. **STACK hasta 3 simultaneous camera moves.** Genre presets (Action, Horror, Comedy, Suspense). Simula real optical physics — virtual camera bodies, anamorphic lenses, focal length, DoF
- Debilidades: 5s clip cap DoP nativo; subject motion no mejor que backbone; moderation agresiva en Soul model
- Prompt adherence: 8/10 (camera params exact; subject = backbone-dependent)

**Pipeline-fit**
- Character consistency: input image only (i2v)
- First/last frame: input image
- **Camera control nativo: YES — el producto ENTERO.** 50+ camera motion presets stackable parametric
- Audio nativo: no

**Real-world constraints**
- NSFW/horror: horror genre preset oficialmente soportado; explicit NSFW blocked; jumpscares/atmospheric fine
- 9:16 nativo: yes
- Watermark: paid clean
- Licencia comercial: yes

**Evidence**
- Refs: [Higgsfield camera controls](https://higgsfield.ai/camera-controls) · [DoP on WaveSpeed](https://wavespeed.ai/models/higgsfield/dop/image-to-video) · [Cinema Studio 2.0 AIbase](https://www.aibase.com/news/16761)

**¿Vale la pena vs Kling/Veo?** **SÍ para shots donde el camera move ES el shot** — dolly zoom on horror reveal, crash zoom on jumpscare, FPV chase through forest. Kling no hace parametric stacked camera moves; Higgsfield sí. **Usar para 1-3 hero camera-driven shots por Reel**, no como workhorse.

---

#### Sync.so (sync labs) — POST-LIPSYNC ESPECIALISTA

**Identidad**
- Vendor: sync labs (YC-backed)
- Acceso: sync.so studio + API oficial, Replicate (sync/sync-1.7), fal
- Última versión: lipsync-2-pro (studio-grade actual 2026)

**Specs base**
- Modalidad: **video + audio → lipsynced video** (NOT image — needs source video clip)
- Duración max: bounded by input video; multi-minute soportado
- Resolución / AR: matches input (hasta 1080p); any AR

**Cost-intelligence**
- Replicate ~$0.05-0.10/run short clips
- API tiers desde free; per-second en sync.so/pricing
- $/s: ~$0.02-0.05/s output
- Retry rate: low clean human; alto en extreme angles

**Quality forensics**
- Fortalezas: **lipsync ONTO existing video** — reemplaza mouth movement en footage Kling ya generado para match diferente audio. Language-agnostic. Best para dubbing o fixing Kling lipsync drift
- Debilidades: NO genera motion from still (needs source video); menos expressive que Hedra para character animation
- Prompt adherence: N/A (audio-driven)

**Pipeline-fit**
- Character consistency: 100% — solo reemplaza mouth region
- First/last frame: full video conditioning
- Camera: N/A (input video drives)
- Audio: YES (audio is driver)
- **Lipsync quality: 9/10** live-action / video-driven; pierde a Hedra en still-image-to-talking

**Real-world constraints**
- NSFW/horror: developer-focused tool, fewer restrictions
- 9:16 nativo: yes (matches input)
- Watermark: paid clean
- Licencia comercial: yes

**Refs:** [sync.so](https://sync.so/) · [lipsync-2-pro](https://sync.so/lipsync-2-pro) · [Hedra vs sync](https://lipsync.com/compare/sync-so-vs-hedra)

**¿Vale la pena?** **SÍ como POST-processing layer** — cuando Kling genera character "speaking" pero lipsync queda off → correr sync.so sobre Kling clip con ElevenLabs narration para arreglarlo. **Complementary, NOT replacement.** Pair: Hedra para still-image-to-talking-head, sync.so para fixing-existing-video-lipsync.

---

#### Wan 2.2 Animate / Animate-X (Alibaba Tongyi + Ant Group) — POSE-DRIVEN CHARACTER ANIMATION

**Identidad**
- Vendor: Alibaba Tongyi Lab + Ant Group (same family, Wan2.2-Animate = production successor de Animate Anyone 2 / Animate-X)
- Acceso: HF (Wan-AI/Wan2.2-Animate-14B), GitHub, ComfyUI nativo, WaveSpeed API, Alibaba Cloud API; Animate-X github.com/antgroup/animate-x
- Última versión: Wan2.2-Animate-14B (2025-09-19)

**Specs base**
- Modalidad: **reference image + driving video → pose-transferred character video**; character-replacement mode (swap character en existing video)
- Duración max: bounded by driving video; Animate-X demoed hasta 16s
- Resolución / AR: 1080p; flexible AR (matches driving video)

**Cost-intelligence**
- Self-host GPU only en 24GB+ VRAM vía ComfyUI; WaveSpeed/Alibaba ~$0.20-0.50/clip
- $/s: ~$0.04-0.10/s API; marginal self-host
- Retry rate: low (pose conditioning is deterministic)

**Quality forensics**
- Fortalezas: **transfer exact body motion + facial expression from driving video onto ref character image**. Animate-X uniquely handles anthropomorphic / cartoon / non-human characters. Wan2.2-Animate agrega Relighting LoRA + character REPLACEMENT in existing footage
- Debilidades: requires good driving video; identity drift on fast motion; NOT for free-form generation (always pose-driven)
- Prompt adherence: N/A (pose-driven)

**Pipeline-fit**
- Character consistency: **BEST IN CLASS** — single ref image preserves identity across full clip via skeleton + implicit facial signals
- First/last frame: yes (reference image)
- Camera: inherited from driving video
- Audio: no
- Lipsync: facial expression replication good; explicit lipsync inferior a Hedra

**Real-world constraints**
- NSFW/horror: open self-host no filter; managed APIs filtered
- 9:16 nativo: yes (matches driving)
- Watermark: none self-host
- Licencia comercial: Wan 2.2 Animate Apache-style (Tongyi Wanxiang Community License); Animate-X academic license — verificar

**Refs:** [HF Wan2.2-Animate](https://huggingface.co/Wan-AI/Wan2.2-Animate-14B) · [Animate-X GitHub](https://github.com/antgroup/animate-x) · [ComfyUI tutorial](https://docs.comfy.org/tutorials/video/wan/wan2-2-animate)

**¿Vale la pena vs Kling/Veo?** **SÍ para character-driven shots requiring consistency across multiple clips con choreographed motion.** Kling no transfer pose from driving video; Wan-Animate sí. Use cases: animar horror character (witch, ghost) con motion capturada from ref performance, o reemplazar actores en footage con monster preserving real motion. **High leverage para H1-H6 hito structure con recurring character identity.**

---

### 3.4 IMAGE-GEN CHARACTER CONSISTENCY (9 modelos)

#### Gemini 2.5 Flash Image / Nano Banana (Google DeepMind) — DEFAULT ACTUAL DEL PROYECTO

**Identidad**
- Vendor: Google DeepMind
- Acceso: Gemini API, Vertex AI, AI Studio, web (Gemini app), Replicate, fal, OpenRouter, Leonardo
- Última versión: Gemini 2.5 Flash Image GA (agosto 2025). **Sucesor "Nano Banana Pro" (Gemini 3 Pro Image)** lanzado noviembre 2025 / GA enterprise 2026

**Specs base**
- Resolución max: 1024px lado largo nativo en 2.5 Flash Image; Pro extiende a 2K/4K explícito
- AR: 1:1, 3:4, 4:3, 9:16, 16:9 (9:16 nativo confirmado)
- Precio: $0.039/imagen 2.5 Flash Image (1290 output tokens); Pro ~$0.134/imagen 2K

**Quality forensics**
- Fortalezas: identity preservation cross-edit, conversational multi-turn editing, multimodal fusion, photoreal + stylized, semantic reasoning
- Debilidades: tipografía compleja débil vs Ideogram; ocasional hand drift; hard-cap implícito en cantidad de identidades simultáneas
- Prompt adherence: 9/10 — lider LMArena Image Edit + Text-to-Image desde agosto 2025

**Character consistency (LEVER PRIMARIO)**
- **Modo nativo:** multi-image-conversation (multi-image-ref en mismo prompt) + conversational turns que heredan identidad
- **Cómo se usa:** pasas 1-6 imágenes referencia en mismo prompt junto al texto. Modelo trata cada imagen como contexto y mantiene rasgos faciales cross-generation SIN fine-tuning. También "turn-based" editing donde cada nueva escena hereda identidad de previa
- **Fidelidad cross-prompt: 9/10** — community reports ~94% facial landmark consistency en storyboards 15 imgs (Nano Banana 2). 2.5 Flash practical cap: 6 referencias high-quality antes de degradar. Pro tier: 5 personajes simultáneos / 14 imagenes ref
- Limitaciones: drift en perfiles laterales extremos; cambios perspectiva son mixed; >6 referencias degrada precision

**Style consistency**
- Modo: implícito vía multi-image-ref (no flag separado tipo --sref); pasar imagenes con misma paleta/iluminación fuerza style match

**Real-world constraints**
- NSFW/horror: moderate-restrictive (horror suggestive pasa, gore explícito frecuente filter; mejor que MJ peor que Flux Dev self-host)
- Watermark: SynthID invisible
- Licencia comercial: yes

**Evidence**
- Refs: [Google Developers Blog](https://developers.googleblog.com/introducing-gemini-2-5-flash-image/) · [Flux Kontext vs Nano Banana](https://blog.runc.ai/authoritative-comparison-flux-kontext-vs-google-nano-banana/) · [Nano Banana limitations](https://milvus.io/ai-quick-reference/what-are-the-known-limitations-or-challenges-of-nano-banana)

**¿Vale la pena vs default?** Es el default. NO cambiar salvo: (a) NSFW/horror explícito → Flux Dev self-host; (b) >5 personajes simultáneos → Seedream 4.5 con 14 refs.

---

#### Imagen 4 / Imagen 4 Ultra (Google) — ⛔ DEPRECATING 2026-06-30

**Identidad**
- Vendor: Google
- Acceso: API Vertex AI, Gemini API, AI Studio, Firebase AI Logic
- Última versión: Imagen 4 Ultra (`imagen-4.0-ultra-generate-001`) GA mid-2025. **⛔ AVISO: shutdown 2026-06-30. Migrar a Nano Banana (Gemini Image)**

**Specs base**
- Resolución max: 2048×2048 nativo, hasta 4096×4096 vía upscale endpoint (Pro)
- AR: 1:1, 9:16, 16:9, 3:4, 4:3
- Precio: Standard $0.04, Imagen 4 $0.06, Ultra $0.08

**Quality forensics**
- Fortalezas: photoreal high-end, fidelity comparable foto real, prompt adherence Ultra alta, tipografía decente
- Debilidades: **NO editing nativo**, weaker en stylized/illustration vs MJ, sin conversational refinement
- Prompt adherence: 9/10 Ultra, 8/10 Standard

**Character consistency**
- Modo nativo: single-image-ref vía Imagen 3 Customization API (`subjectType="SUBJECT_TYPE_PERSON"`). **CRITICO: Customization API atada a `imagen-3.0-capability-001`, NO a Imagen 4. Imagen 4 base NO acepta referencias.**
- Fidelidad: 6/10 con Imagen 3 Customization (drift visible >4 escenas)
- Limitaciones: feature legacy Imagen 3, no portada a Imagen 4, stack se apaga junio 2026

**Real-world constraints**
- NSFW/horror: restrictive (lo más conservador Google; más estricto que Nano Banana)
- Watermark: SynthID invisible
- Licencia comercial: yes (mientras dure)

**Evidence**
- Refs: [Vertex Imagen 4 docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate) · [Subject customization (Imagen 3)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/image/subject-customization)

**⛔ ACCIÓN:** Auditar `ai-video image` para llamadas a `imagen-4.0-*`. Migrar a `gemini-2.5-flash-image-preview` o forward a Nano Banana Pro. Plazo: 2026-05-30 (new access blocking) / 2026-06-30 (full shutdown).

---

#### FLUX.1 Kontext + FLUX.2 + Dev + PuLID/IP-Adapter (Black Forest Labs)

**Identidad**
- Vendor: Black Forest Labs
- Acceso: BFL Playground API directo, fal, Replicate, Together AI, Adobe Firefly; Dev self-host (HF weights)
- Última versión: FLUX.1 Kontext [pro]/[max] mid-2025; Kontext [dev] open; **FLUX.2 multi-reference (hasta 10 refs) Q1 2026**

**Specs base**
- Resolución max: hasta 4MP en Kontext [max]; Flux 1.1 Pro Ultra hasta 4MP
- AR: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21 (9:16 ✓)
- Precio: Kontext [pro] $0.04, [max] $0.08, Flux 1.1 Pro Ultra ~$0.06; Dev self-host free + GPU

**Quality forensics**
- Fortalezas: photoreal, cinematic, anatomía correcta, prompt adherence sólido, multi-step editing preserva detail, **weights abiertos Dev (full control)**
- Debilidades: tipografía in-image inferior Ideogram; hands mejorado pero imperfecto
- Prompt adherence: 9/10

**Character consistency (LEVER PRIMARIO)**
- **Modo nativo:** Kontext = single-image-ref iterativo identity-lock; **FLUX.2 = multi-image-ref (hasta 10 refs)**; Dev = training-based LoRA / PuLID / IP-Adapter
- **Cómo se usa:**
  - Kontext: pasás ref image + prompt, denoising 0.6-0.7 + fixed seed
  - FLUX.2: `reference_images: [url1, url2, ...]` hasta 10
  - Dev: train LoRA offline (10-20 imgs) o PuLID node ComfyUI con 1 imagen ref para identity preservation
- **Fidelidad cross-prompt:** 8/10 Kontext (BFL claims cosine similarity >0.92 sobre 6 ediciones vs ~0.80 competidores). 9/10 con PuLID + LoRA bien entrenado en Dev. 8.5/10 FLUX.2 multi-ref
- Limitaciones: Kontext drifts en multi-step complejo; PuLID requiere ComfyUI/GPU; LoRA training = setup time

**Real-world constraints**
- NSFW/horror: API hosted moderate (safety_tolerance 1-6, default 2). **Dev self-host: PERMISSIVE total — único path 100% libre para horror gore/sangre realista**
- Watermark: no hosted; Dev none
- Licencia comercial: yes BFL API; Dev open + commercial OK

**Evidence**
- Refs: [BFL Kontext](https://bfl.ai/announcements/flux-1-kontext) · [FLUX.2 multi-ref](https://www.together.ai/blog/flux-2-multi-reference-image-generation-now-available-on-together-ai) · [PuLID vs ecomid vs InstantID](https://myaiforce.com/flux-pulid-vs-ecomid-vs-instantid/)

**¿Vale la pena vs Nano Banana?** SÍ en 2 escenarios: (1) horror gore explícito → Dev self-host único path 100% permisivo; (2) si presupuesto/tiempo para entrenar LoRA por protagonista → maximum identity lock + offline (ideal si 2 protagonistas se usan en 50+ videos).

---

#### Midjourney v7 (Midjourney) — NO API → NO SCRIPTABLE

**Identidad**
- Vendor: Midjourney
- Acceso: **Discord + midjourney.com web; NO API pública oficial**
- Última versión: v7 (abril 2025), Omni Reference shipped 2025

**Specs base**
- Resolución max: ~2048×2048 con upscale
- AR: cualquiera vía `--ar` (1:1, 9:16, 16:9, 2:3, 3:2, etc.)
- Precio: subscription. Basic $10/mo ~200 imgs (~$0.05/img Fast); Standard $30/mo ~900 imgs (~$0.033/img Fast)

**Quality forensics**
- Fortalezas: **aesthetic/stylized king** (anime, painterly, cinematic moods), composition, lighting drama, art-direction
- Debilidades: photoreal mejorando pero detrás Flux/Nano Banana; **sin API publica = NO automatizable en script**; tipografía mala
- Prompt adherence: 8/10

**Character consistency**
- Modo nativo: **`--oref` (Omni Reference) en v7. `--cref` es legacy v6 — NO funciona v7**
- Cómo se usa: `--oref <URL> --ow <peso 0-1000, default 100>`. Range óptimo 300-500 para character work. También `--sref` para style
- Fidelidad: 7/10 — sólido 3-4 escenas, degrada notable >5
- Limitaciones: subscription required ($10+), sin API = no scriptable, Discord workflow lento para 6+ scenes

**Real-world constraints**
- NSFW/horror: **RESTRICTIVE (PG-13 strict)**. Banned words: gore, blood, dismemberment, deformed, mutilated. Multi-layer filtros. Bypass = ban
- Watermark: no
- Licencia comercial: yes Standard+ ($30+/mo)

**Refs:** [Omni Reference docs](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference) · [v7 character masterclass](https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/)

**¿Vale la pena?** **NO para horror-choice automation.** Bloqueador #1 = restrictive horror policy. Bloqueador #2 = sin API → no scriptable.

---

#### Ideogram 3.0 / Ideogram Character (Ideogram)

**Identidad**
- Vendor: Ideogram AI
- Acceso: API, ideogram.ai web, Segmind, Kie.ai
- Última versión: Ideogram 3.0 (2025); Ideogram Character (single-image consistency) mid-2025

**Specs base**
- Resolución max: 1024×1024 base; upscaler endpoint dedicado 2K+
- AR: 16:9, 9:16, 1:1, 3:4, 4:3, 3:2, 2:3, 10:16, 16:10 (69 presets total)
- Precio: TURBO $0.0375, DEFAULT $0.075, QUALITY $0.1125. Free 10 prompts/día

**Quality forensics**
- Fortalezas: **TIPOGRAFÍA in-image #1 del mercado**, design/poster, vector-style ilustración, consistent styles
- Debilidades: photoreal flat vs Flux/Nano Banana, anatomía OK pero no top, complex scenes flaquean
- Prompt adherence: 8/10

**Character consistency**
- Modo nativo: single-image-ref (Ideogram Character — "first model with just one ref image")
- Cómo se usa: upload vía Character tab o API. Combinable con Style Reference (hasta 3)
- Fidelidad: 7/10 — Ideogram aclara "consistency isn't perfect, expect variation"
- Limitaciones: óptimo solo front/3/4 view inputs; drift en pose-heavy; sin multi-image-ref nativo (solo 1 vs NB 6, Seedream 14)

**Real-world constraints**
- NSFW/horror: RESTRICTIVE (zero NSFW; guardrails over-trigger en anatomía + fantasy fight)
- Watermark: no paid
- Licencia comercial: yes paid

**Refs:** [Ideogram Character](https://ideogram.ai/features/character/) · [X announcement](https://x.com/ideogram_ai/status/1950255115753095307)

**¿Vale la pena?** NO para character horror-choice (1-shot + NSFW filter). **SÍ como segundo modelo complementario para posters/signage in-scene con texto legible.**

---

#### Recraft V3 / V4 (Recraft)

**Identidad**
- Vendor: Recraft AI
- Acceso: API (recraft.ai, Replicate, Vercel AI Gateway, Segmind), web
- Última versión: Recraft V3 (oct 2024); **V4 / V4 Pro (feb 2026)** — 4MP output Pro

**Specs base**
- Resolución max: ~1024px V3 (1MP), V4 Pro 4MP
- AR: 2:1, 16:9, 5:3, 3:2, 7:5, 4:3, 5:4, 1:1, 4:5, 3:4, 5:7, 2:3, 3:5, 9:16, 1:2 (hasta 1024×2048)
- Precio: ~$0.04 API; Pro $25/mo incluye API

**Quality forensics**
- Fortalezas: **brand identity / design / vector / typography / poster**, style presets (20+), Style Lock, native SVG export, illustration sets coherentes
- Debilidades: photoreal y cinematic horror NO es su zona; character consistency NOT flagship
- Prompt adherence: 7/10

**Character consistency**
- Modo nativo: **NO feature dedicada character tracking.** Workaround: ref image en canvas + Style Lock + prompt engineering
- Fidelidad: 5/10 (community: útil "visual continuity" no "identity lock")
- Limitaciones: drift moderado-alto en 4+ escenas

**Style consistency**
- Modo: Style Lock (line weight, color, detail, proportions, rendering) + Style Sharing teams
- **Útil para: brand assets, illustration sets, logo systems — DONDE recraft brilla**

**Real-world constraints**
- NSFW/horror: moderate (design-focused; filters less aggressive que Ideogram/MJ)
- Watermark: no Pro
- Licencia comercial: yes Pro $25/mo (full incluso SVG export)

**Refs:** [Recraft character consistency](https://www.recraft.ai/docs/best-practices/character-consistency)

**¿Vale la pena para horror?** NO. Recraft = brand/design specialist, no character-lock. **SKIP para este use case.**

---

#### Runway Gen-4 References (Runway)

**Identidad**
- Vendor: Runway ML
- Acceso: web, API, Replicate (`runwayml/gen4-image`)
- Última versión: Gen-4 References (abril 2025); Image References mejorado 2025-2026

**Specs base**
- Resolución max: 1920×1080 / 1080×1920 nativo
- AR: 16:9, 9:16, 1:1, 4:3, 3:4 (9:16 nativo)
- Precio: credit system, Standard $28/mo; API Gen-4 image ~$0.08/imagen

**Quality forensics**
- Fortalezas: integración video-first (mismo asset → directo Gen-4 Video), reference workflow probado producción
- Debilidades: photoreal sólido pero no top-tier vs Flux/Nano Banana; prompt adherence intermedio
- Prompt adherence: 7.5/10

**Character consistency**
- Modo: multi-image-ref (hasta 3)
- Fidelidad: 8/10 (Runway claims 95%+ cross-shots; community 80-85% práctico)
- Limitaciones: max 3 refs (vs NB 6+, Seedream 14); tuning manual; requires front-facing input

**Real-world constraints**
- NSFW/horror: **RESTRICTIVE** (filters estrictos; NSFW + public figure names blocked; gore filtrado)
- Watermark: no paid
- Licencia comercial: yes Standard+ plan

**Refs:** [Gen-4 Image References docs](https://help.runwayml.com/hc/en-us/articles/40042718905875-Creating-with-Gen-4-Image-References) · [Runway announcement](https://runwayml.com/research/introducing-runway-gen-4)

**¿Vale la pena vs Nano Banana?** Caso único: si pipeline va a saltar image-to-video con Gen-4 Video (no Kling), mantener todo Runway. Como pipeline actual usa Kling → no hay razón cambiar.

---

#### Seedream 4.5 (ByteDance / Seed)

**Identidad**
- Vendor: ByteDance Seed
- Acceso: API vía fal.ai, Replicate, WaveSpeed, OpenRouter, Kie.ai
- Última versión: Seedream 4.5 (Q1 2026, sucesor 4.0)

**Specs base**
- Resolución max: **4K nativo** (t2i 4K, edit hasta 2K)
- AR: 1:1, 9:16, 16:9, 3:4, 4:3, 2:3, 3:2 (9:16 ✓)
- Precio: fal $0.04, Replicate ~$0.027-0.045, Kie.ai desde $0.0175, OpenRouter $0.035-0.045

**Quality forensics**
- Fortalezas: 4K nativo, cinematic lighting (vs flat 4.0), spatial logic, multi-image consistency, **MEJOR ratio precio/calidad del set**
- Debilidades: facial features con distortion vs Nano Banana Pro algunos reports; text rendering peor que Ideogram
- Prompt adherence: 8.5/10

**Character consistency (LEVER PRIMARIO)**
- **Modo nativo: multi-image-ref (hasta 14 reference images)** + **Sequence Mode** dedicado para character series
- Cómo se usa: `image_input: [url1, ..., url14]`. Sequence Mode genera N images compartiendo character/style en single call. Endpoint `edit-sequential` en WaveSpeed/fal
- **Fidelidad: 8.5/10** — líder en cantidad bruta refs (14 vs NB 6). Comparison reports: holds character details "more reliably than most alternatives" en sequences. Vs NB Pro 1-a-1: NB Pro gana en facial naturalness + multi-character
- Limitaciones: face distortion ocasional multi-character con expresiones complejas; content filter agresivo hosted (sensitive_info_detection errors en horror)

**Real-world constraints**
- NSFW/horror: **variable por plataforma**. Filtros built-in 3-layer en hosted. **Higgsfield AI ofrece version SIN filtros (uncensored)**. Para horror temático: pasa en fal.ai con prompts cuidadosos; gore explícito → Higgsfield route
- Watermark: no API
- Licencia comercial: yes (personal + commercial)

**Refs:** [Seedream 4.5 ByteDance](https://seed.bytedance.com/en/seedream4_5) · [WaveSpeed 4.5 guide](https://wavespeed.ai/blog/posts/seedream-4-5-complete-guide-2026/) · [Seedream vs Nano Banana Pro](https://medium.com/@302.AI/seedream-4-5-vs-nano-banana-pro-can-the-sota-be-replaced-99056bee667d) · [Sequence Mode use cases](https://www.scenario.com/blog/seedream-sequence-mode-use-cases)

**¿Vale la pena vs Nano Banana?** SÍ para tests A/B. Mismo precio (~$0.04), 14 refs vs 6 (más asset reuse), **Sequence Mode = ventaja real para producir 6+ scenes single call**. Caveat: NB Pro gana en multi-character consistency según community. **Recomendación: test 1 día con 2 protagonistas del video actual → comparar facial fidelity escena por escena.**

---

#### Krea Image / Krea 1 (Krea.ai)

**Identidad**
- Vendor: Krea AI
- Acceso: krea.ai web, API (Compute Units), hosts other models (Flux, Runway, Hailuo, Veo3)
- Última versión: Krea 1 (proprietary 2025); trainer feature actualizado 2026

**Specs base**
- Resolución max: hasta 22K vía upscale Max plan; base ~1MP-2MP
- AR: 16:9, 9:16, 1:1, 4:3, 3:4, custom
- Precio: API Compute Units (CU). Flux ~5 CU/imagen; 20,000 CU Pro plan ~4000 Flux images. **Efectivo ~$0.009/img Flux en Pro.** Subs: Free 100 CU/día, Basic $9, Pro $35, Max $70

**Quality forensics**
- Fortalezas: skin texture accuracy, extreme camera angles, **artistic rendering (grain/bloom/DOF blur)**, color science — "engineered photorealism con artistic edge"
- Debilidades: ecosystem más que model único; Krea-1 menos battle-tested vs Flux/Nano Banana en benchmarks puros
- Prompt adherence: 8/10

**Character consistency**
- Modo: 2 paths
  - (a) **Character Reference tool:** 1 photo por character, hasta 3 chars con `@nombre` tagging
  - (b) **Training-based:** custom model con 10-20 imgs (like LoRA)
- Fidelidad: 7/10 single-photo; 9/10 trained model
- Limitaciones: 1-shot drifts en lighting extremo; training requires setup time (~horas); max 3 chars en Reference mode

**Real-world constraints**
- NSFW/horror: desconocido oficial; community indica moderate (más permisivo que MJ/Runway, menos que Flux Dev self-host)
- Watermark: no paid
- Licencia comercial: yes paid

**Refs:** [Krea docs](https://www.krea.ai/docs/features/krea-image) · [Krea training](https://docs.krea.ai/user-guide/features/training)

**¿Vale la pena vs Nano Banana?** Caso único: si valorás aesthetic "filmic grain + DOF + bloom" estilísticamente. Para char lock puro: no le gana NB 1-shot; custom-trained iguala (pero entonces compará con Flux Dev + LoRA estándar y portable). **Skip default; considerar si buscás look filmic específico para narrativo concreto.**

---

## 4. CLAIM VALIDATION LOG

> Cada claim crítico que cambia decisión del director, con verdict + sources. Si un futuro agent ve un claim aquí marcado WEAK o REFUTED → necesita re-validar antes de actuar.

### 4.1 Seedance 2.0 supera a Kling 2.5 Turbo Pro y Veo 3.1 en image-to-video
- **Verdict:** MIXED
- **Detalle:** Seedance 2.0 Elo 1347 vs Kling 2.5 Turbo 1283 (i2v leaderboard) — solo 64 puntos Elo (no abrumador). Kling 3.0 Elo 1281, casi igual a 2.5 Turbo. **Para i2v puro, las 3 son comparables.** Seedance gana decisivo solo en multi-shot + native audio + physics complejas.
- **Fuentes:**
  - [Artificial Analysis i2v](https://artificialanalysis.ai/video/leaderboard/image-to-video)
  - [MattVidPro Seedance review](https://www.classcentral.com/course/youtube-seedance-2-0-feels-like-old-sora-but-better-fight-scenes-are-finally-good-528488) (validated)
  - [WaveSpeed comparison](https://wavespeed.ai/blog/posts/seedance-2-0-vs-kling-3-0-sora-2-veo-3-1-video-generation-comparison-2026/)
- **Acción director:** Probar Seedance 2.0 en 1-2 shots horror-choice antes de migrar. No abandonar Kling 2.5 Turbo Pro como default sin A/B.

### 4.2 Hailuo es el "go-to cuando Kling rechaza" para horror
- **Verdict:** **SUPPORTED — A/B test propio N=2** ✅ (upgrade from WEAK)
- **Update 2026-05-13:** A/B test propio en `ab-testing/` con source bosque-abandonado h1, 2 prompts (vague + polished). **Hailuo ganó en motion narrativo en AMBOS prompts.** Detalle:
  - vague prompt: Hailuo caminó hacia el fondo (único modelo que lo hizo); Kling + Seedance estáticos
  - polished prompt: Hailuo caminó hacia cámara con bastón activo + vapor de aliento visible; Kling giró+alejó (mejor que v1); Seedance rotó (sutil)
- **Detalle anterior (sigue válido para shutdown):** Tweet Pieter Levels octubre 2024 corrobora "Kling fallback when filter rejects". Curious Refuge nota Hailuo "resists disorder" — válido para horror visceral/caótico (no para motion narrativo).
- **Fuentes:**
  - `ab-testing/RESULTS.md` + `_scores.json` + `_scores-polished.json` (N=2 own test)
  - [Levelsio tweet 2024](https://x.com/levelsio/status/1847252618457780464)
  - [Curious Refuge Hailuo review](https://curiousrefuge.com/blog/minimax23-ai-video-generator-review)
  - [GoEnhance Kling censorship](https://www.goenhance.ai/blog/kling-ai-censorship)
- **Acción director:** Hailuo es default para shots con motion narrativo (caminar/correr/agarrar). Mantener Kling como default para shots atmosféricos estáticos.

### 4.3 Sora 2 API shutdown September 24, 2026
- **Verdict:** **VALIDATED** ✅
- **Fuentes:**
  - [OpenAI Help](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation)
  - [the-decoder shutdown](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/)
  - [OpenAI Dev forum](https://community.openai.com/t/is-the-sora2-api-still-working/1379946)
- **Detalle:** Web/app cerrado abril 26 2026; API ends sep 24 2026. OpenAI: redirect compute a enterprise/coding; Sora continues as "research initiative on world models". NO official replacement.
- **Acción director:** NO incorporar Sora a workflows nuevos. Si algo depende: migrar antes sep 24.

### 4.4 Kling 3.0 native audio + multi-shot competitive con Veo 3.1
- **Verdict:** **VALIDATED** (split por uso) ✅
- **Detalle:** Kling 3.0 gana en Dialogue (EN), Multilingual Speech, Lip Sync. Veo 3.1 gana Ambient/Environmental, SFX, Overall A/V Sync. **Complementary, NO redundant.**
- **Fuentes:**
  - [Atlas Cloud audio head-to-head](https://www.atlascloud.ai/blog/guides/ai-video-models-native-audio-compared)
  - [Veo3ai.io comparison](https://www.veo3ai.io/blog/kling-3-0-vs-veo-3-1-2026)
  - [MagicHour comparison](https://magichour.ai/blog/kling-30-vs-veo-31)
- **Acción director:** Para Spanish horror narration con character-speaking-on-screen → Kling 3.0. Para atmospheric SFX + ambient → Veo 3.1. Mayoría horror Reel = voiceover-only → ventaja Kling multilingual = MENOS relevante.

### 4.5 Hunyuan 1.5 + Wan 2.7 quality vs paid models para production
- **Verdict:** **WEAK / NEEDS MORE DATA** ⚠️
- **Detalle:** Hunyuan 1.5 = 8.4/10 instruction following vs Wan 2.2 7.6 (open-source benchmark). Wan 2.7 mejoró textures/fabric/lighting a commercial 1080p standards. **PERO:** Curious Refuge ranks Wan 2.6 = 6.7/10 — debajo de TODOS los paid models. Hunyuan 1.5 + Wan 2.7 NOT en Curious Refuge professional ranking.
- **Fuentes:**
  - [Hunyuan 1.5 paper](https://arxiv.org/html/2511.18870v1)
  - [Wan 2.6 vs 2.7](https://wavespeed.ai/blog/posts/wan-2-7-vs-wan-2-6/)
  - [Curious Refuge ranking](https://curiousrefuge.com/blog/best-ai-video-generators-for-2026)
- **Acción director:** **Experimentation tier, NO production tier** para 9.7 bar. Usar para cost-saving non-hero shots o testbed para horror NSFW. NO migrar default desde Kling.

### 4.6 Imagen 4 deprecation June 30, 2026
- **Verdict:** **VALIDATED** ✅
- **Detalle:** Retirement 2026-06-30 confirmado en Vertex AI docs. New access blocked 1 mes antes (2026-05-30). Google docs contradicen path: Vertex dice "downgrade Imagen 3", Gemini API dice "forward Nano Banana". **Seguir Gemini API guidance (Nano Banana) — estrategia futura.**
- **Fuentes:**
  - [Vertex model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
  - [Gemini API deprecations](https://ai.google.dev/gemini-api/docs/deprecations)
  - [Google Dev forum](https://discuss.google.dev/t/imagen-4-0-deprecation-and-canada-hosted-alternatives/342923)
- **Acción director:** Auditar `ai-video image` antes 2026-05-30. Migrar a `gemini-2.5-flash-image` (Nano Banana) o forward a Nano Banana Pro.

### 4.9 LTX legacy NO viable como draft tier
- **Verdict:** **REFUTED** ❌
- **Update 2026-05-13:** A/B test propio confirmó. LTX Video legacy (model `lightricks/ltx-video` en Replicate) scored 4.0/10 en v1 con motion coherence 2/10. Los 3 frames key son prácticamente idénticos — modelo NO animó.
- **Fuente:** `ab-testing/RESULTS.md` (own test)
- **Acción director:** ⛔ NO USAR LTX legacy ni como draft tier. **LTX-2.3 (la versión 2026)** no está en Replicate todavía — solo fal.ai. Validación de LTX-2.3 pending hasta tener FAL_KEY configurado.
- **Workaround:** usar Hailuo Std 768p como draft tier — barato ($0.27 / 6s) Y se mueve.

### 4.10 Prompt quality es el factor #1 — más que elección de modelo
- **Verdict:** **VALIDATED — A/B propio N=2** ✅ (descubrimiento del A/B test)
- **Update 2026-05-13:** El mismo modelo, misma imagen source, produce resultados RADICALMENTE distintos según calidad del prompt:
  - Kling 2.5 con vague prompt: totalmente estático (motion 3/10)
  - Kling 2.5 con polished prompt: gira de perfil + se aleja de espaldas (motion observable)
  - Hailuo con vague: caminó al fondo
  - Hailuo con polished: caminó hacia cámara con bastón activo + vapor exhalado
  - Seedance con vague: estático
  - Seedance con polished: rotó de perfil con orientation change
- **Implicación:** decision de modelo es SECUNDARIA a decision de prompt. Validar primero que prompt cumple regla `prompt_quality_no_vague.md`.
- **Acción director:** antes de elegir modelo, escribir el prompt completo. Si el prompt es vago, ningún modelo va a performar bien — el problema es el prompt, no el modelo.

### 4.7 HappyHorse-1.0 es #1 i2v en Artificial Analysis
- **Verdict:** **VALIDATED (leaderboard)** + **WEAK (real-world testing)** ⚠️
- **Detalle:** AA i2v Elo 1395 confirmado top. Ningún YouTube reviewer ha testado side-by-side. Sin reviews comunitarias independientes.
- **Fuentes:**
  - [AA i2v leaderboard](https://artificialanalysis.ai/video/leaderboard/image-to-video)
  - [WaveSpeed HappyHorse vs Seedance](https://wavespeed.ai/blog/posts/happyhorse-vs-seedance-2-0-comparison-2026/)
  - [Atlas Cloud comparison](https://www.atlascloud.ai/blog/guides/happy-horse-1-vs-seedance-2)
- **Acción director:** A/B test propio (1-2 shots horror-choice) antes de defaultear o ignorar.

### 4.8 Workflow community dominante 2026 = multi-model orchestration
- **Verdict:** **VALIDATED** ✅
- **Detalle:** Quote viral citada cross-aggregators: "Seedance for action, Kling for characters, Veo for products". Pieter Levels confirma multi-model en producción (Photo AI). Plataformas unificadoras (Pixo, Higgsfield, fal.ai) ganando market.
- **Fuentes:**
  - [Pixo migration guide](https://pixo.video/blog/sora-migration-to-pixo)
  - [Higgsfield 2026 review](https://higgsfield.ai/blog/best-ai-video-generators-2026)
  - [Levelsio tweet](https://x.com/levelsio/status/1847252618457780464)
- **Acción director:** Adoptar mindset multi-model en MODEL-BENCHMARK.md (este doc). NO defaultear single-model para video completo.

---

## 5. METHODOLOGY + BLINDSPOTS

### 5.1 Sources usadas (en orden de confianza)

**Tier 1 — Alta confianza (datos hard, independientes):**
- **Artificial Analysis** (artificialanalysis.ai/video/leaderboard) — Elo rankings t2v + i2v independientes
- **Video Arena** (lmarena.ai, videoarena.com) — community votes blind A/B
- **Vendor docs oficiales** (Google, OpenAI, BFL, Runway, Kuaishou, etc.) — solo para specs hard (precio, duración, AR, licencia)
- **Replicate / fal / WaveSpeed / Atlas Cloud** — precios reales API + disponibilidad confirmada
- **HuggingFace + GitHub** — open-source weights + licenses + technical reports
- **OpenAI Help Center** — shutdown timelines oficial

**Tier 2 — Media confianza (community-reported, múltiples fuentes):**
- **YouTube reviewers** (MattVidPro, Theoretically Media, Curious Refuge, Bilawal Sidhu) — comparison videos con side-by-side
- **Comparison Mediums** (@302.AI, @team_36250, runc.ai, milvus.io) — A/B benchmarks community
- **Review blogs** (weshop.ai, curiousrefuge, gstory.ai, getimg, atlascloud, lumeflow, lumalabs blog, magichour, scenario, selfielab, flowith) — synthesized community consensus
- **X/Twitter** — posts de practitioners verificables (Pieter Levels, ArtificialAnalysis account)

**Tier 3 — Baja confianza (vendor marketing, paráfrasis):**
- Vendor announcements + blog posts — solo después de corroborar con Tier 1-2
- Aggregator paraphrase de Reddit (cuando Reddit directo no accesible)

### 5.2 Blindspots conocidos

⚠️ **Reddit directo bloqueado en v2 pass** — los agents no pudieron WebFetch reddit.com URLs (timeouts/errors). Toda evidencia "Reddit" en este doc es paraphrase de aggregators. **Riesgo:** algunas claims viralizadas en Reddit pueden estar mal-citadas en aggregators. **Mitigación:** marcado explícitamente en § 4 cuando aplica.

⚠️ **YouTube comments completos no leídos** — los agents leyeron descripciones + comments parciales, no análisis full de comments donde practitioners postean side-by-side findings detallados.

⚠️ **Discord servers no accesibles** — Midjourney, Pika, Runway, Kling oficiales tienen channels con leaks + early access data. Fuera de scope tooling.

⚠️ **Tests propios NO ejecutados** — este benchmark es secondary-source synthesis. Para production decisions, ejecutar A/B test interno (1-2 shots) antes de cambiar default.

⚠️ **Claims marketing-only sin corroboración fuerte:**
- Runway Gen-4 References "95%+ character consistency" (vendor)
- Hailuo "best-in-class prompt adherence" en multi-subject (mostly community)
- Marcados como vendor-only o community-reported en spec sheets respectivos.

⚠️ **Modelos no cubiertos (gaps):**
- **Grok Imagine Video** (xAI) — aparece en leaderboards top mayo 2026 pero no fue scope de research v1
- **Bedrock Nova Reel** (Amazon) — emerging, no en scope
- **Lumen5 / Synthesia / D-ID** — corporate video, no horror-relevant
- **CapCut AI** — TikTok-native, no scope

### 5.3 Cómo refrescar este doc

**Trigger para revisar:**
1. Vendor anuncia nueva versión major (Kling 3.5, Seedance 3.0, Veo 4, etc.)
2. Vendor anuncia shutdown / deprecation
3. Leaderboard rank cambia top-5 significativo
4. Encontrás un modelo nuevo no listado con tracción real-world

**Proceso (mismo que v1+v2):**
1. Lanzar 1-2 agents WebSearch para target modelo/topic
2. Source priority: Tier 1 leaderboards + vendor docs primero, Tier 2 reviews después
3. Cross-validar claims críticos con 2+ fuentes independientes
4. Actualizar § 1.2 (Cambios críticos) + § 4 (Claim validation log) + spec sheet correspondiente
5. Bump "Última actualización" en header

**Frecuencia recomendada:** cada 60 días o cuando trigger above.

---

## Anexo — Inventario rápido (35 modelos cubiertos)

**Premium Western (5):** Veo 3.1 · Sora 2 Pro ⛔ · Runway Gen-4.5 · Pika 2.5 · Luma Ray3.14
**Premium Chinese (10):** Kling 2.5 Turbo Pro · Kling 2.1 Master · Kling 1.6 Pro · Kling 3.0 Omni · Hailuo 02 + 2.3 · Seedance 2.0 · HappyHorse-1.0 (nuevo) · Wan 2.7 · Hunyuan 1.5 · Vidu Q3
**Open-source general (4):** LTX-2.3 · Mochi 1 (skip) · CogVideoX-1.5 (skip) · SVD 1.1 (skip)
**Specialists (4):** Hedra Character-3 (lipsync still) · Higgsfield DoP (camera) · Sync.so (post-lipsync) · Wan 2.2 Animate (pose-driven)
**Image-gen char consistency (9):** Gemini Nano Banana · Imagen 4 ⛔ · Flux Kontext + PuLID · Midjourney v7 · Ideogram 3.0 · Recraft V4 · Runway Gen-4 References · Seedream 4.5 · Krea Image

**Defaults validados (ranking):**
1. **Animación reel:** Kling 2.5 Turbo Pro (Elo 1283, $0.07/s) — current default OK
2. **Animación cinematic:** Veo 3.1 Standard ($0.40/s)
3. **Animación multi-shot:** Seedance 2.0 ($0.247/s)
4. **Imagen storyboard:** Gemini Nano Banana ($0.039/img) — current default OK
5. **Lipsync still-to-talking:** Hedra Character-3 ($0.05/s)
6. **Camera hero:** Higgsfield DoP + Kling backbone ($0.15-0.40/s)
7. **Horror gore:** Wan 2.7 self-host (GPU cost only)

**Modelos a IGNORAR / SKIP:**
- Sora 2 Pro (deprecating sep 2026)
- Imagen 4 (deprecating jun 2026)
- Midjourney v7 (no API)
- Mochi 1 (480p ceiling)
- CogVideoX-1.5 (eclipsed)
- SVD 1.1 (legacy)
- Recraft V3 para character (no es su feature)
- Pika 2.5 (alta variance, behind leaders)

**Modelos a TESTAR en próximo ciclo:**
- HappyHorse-1.0 (#1 i2v leaderboard, sin reviews)
- Hailuo 2.3 vs Kling 2.5 para horror (validar/refutar claim WEAK)
- Seedream 4.5 Sequence Mode vs Nano Banana para character consistency
- Wan 2.7 self-host para gore explícito
