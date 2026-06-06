# INGENIERO-CHOICE-CORE.md — Técnica AGNÓSTICA choice-específica del INGENIERO

> **AUTORIDAD TÉCNICA agnóstica del formato CHOICE** (rol 🛠️ INGENIERO de cualquier género choice). Define el "cómo" técnico de la **mecánica choice** — lo que es técnica del formato pero NO es pipeline universal.
>
> ⛔ **ESTE DOC NO DUPLICA LA TÉCNICA UNIVERSAL.** Para CUALQUIER métrica/técnica universal (LUFS -14, mix de volúmenes, render, HYBRID per-clip atomic, MODEL-CAPABILITIES, cost cap, TDD, Whisper auto-sync, motion primitives, audio mastering, 8 gates) la autoridad es **`ai-video-production/`** (Capa A). Este doc **APUNTA** a esos docs (ver §0 tabla heredada-universal) y hospeda SOLO la técnica choice-UI-específica.
>
> **Heredan de este doc:** `horror-choice-format/INGENIERO-PAUTA-MASTER.md` (técnica con sabor horror) y `sport-choice-format/INGENIERO-PAUTA-MASTER.md` (técnica con sabor sport). Si un doc de género y este discrepan sobre la técnica choice-UI → gana este doc.
>
> **Lineaje empírico:** los valores acá derivan de **mediciones F1 de 10 referentes** del formato "Elige a tu compañero" (vía `horror-choice-format/INGENIERO-PAUTA-MASTER.md`). Cada valor preserva su atribución empírica.
>
> **Última actualización:** 2026-06-01 (creación — extracción agnóstica).

---

## §0 — METODOLOGÍA + TABLA DE TÉCNICA UNIVERSAL HEREDADA

> **Regla #1 del ingeniero (heredada):** NUNCA usar nuestras propias producciones como autoridad técnica. La autoridad de la mecánica son los referentes F1 (vía horror INGENIERO-PAUTA). NEVER ESTIMATE, ALWAYS MEASURE — todo valor lleva `canonical_validation_status`.

### Lo que este doc hospeda (técnica CHOICE-UI específica)

| § | Técnica choice-específica | Por qué vive acá (no en Capa A) |
|---|----------------------------|----------------------------------|
| §1 | **Decision-UI editorial pacing** (countdown 1s/dígito + pause beat + freeze/filter OPCIONAL + loading bar L→R + audio cue) | Es la firma editorial del momento de decisión del formato choice — no existe en videos AI genéricos |
| §2 | **UI safe zones** (caption Y62 / loading Y52 / countdown Y46 / name labels Y11.5 monospaced + no-overlap matrix + per-speaker Y-band) | Layout específico de la UI choice (countdown, loading bar, botones A/B, name labels) |
| §3 | **Caption chunking word-timed para choice** (≤2 líneas progresivas) | El requisito de chunkear toda la narración del clip (HR#30) aplicado a la UI choice |
| §4 | **Lip-sync rule** (`lip_sync_required:false` → no boca visible) | Regla de la mecánica choice (personaje del dyad habla o no on-screen) |
| §5 | **0 cuts en hook + hook-continuity-no-zoom-cut** | Pattern de pacing específico del hook choice |

### ⤴ Lo que este doc NO hospeda — APUNTA a `ai-video-production/` (Capa A universal)

> **Tabla heredada-universal.** Para CUALQUIER cosa de esta tabla, la autoridad es el doc de Capa A indicado. Este doc NO la re-hospeda (evita una tercera copia que se desincronice). El skill de género tampoco la re-mide — la hereda igual.

| Métrica / técnica universal | Valor heredado | ⤴ Autoridad canónica (Capa A) |
|-----------------------------|----------------|-------------------------------|
| **Speaking rate / pace WPM** | ~165 WPM target (bandas F1 medidas) | `ai-video-production/` (NARRATION) + `MODEL-CAPABILITIES-MATRIX.md` (pace per modelo TTS) |
| **Narration coverage** | ≥80% del timeline | `ai-video-production/` (audit-audio / coverage) |
| **LUFS integrated** | **-14 ±0.5** (Instagram) | `ai-video-production/AUDIO-MASTERING.md` + CLAUDE.md HR#1/#9 |
| **Mix de volúmenes** | narración 1.0 / música 0.05-0.18 / SFX 0.20-0.35 / flash 0.55-0.65 | `ai-video-production/SFX-PIPELINE.md` + CLAUDE.md HR#9 |
| **Ducking / sidechain** | -3 a -6 dB sobre música+ambient cuando el narrador habla | `ai-video-production/SFX-PIPELINE.md` + SPEC `layer_3.sidechain_target_db` |
| **Música 3 capas** (drone + ambient + accent) | bed continuo sin gaps; accent event-driven | `ai-video-production/SFX-PIPELINE.md` + MUSIC layers |
| **Cuts/min** | banda de-clustered 1-9 (sweet spot 2.75-5) · Gemini-perceived 14-22 | `ai-video-production/PACING-MARKERS.md` (+ § cuts del INGENIERO de género para la banda choice) |
| **Captions Whisper word-timed** | progresivos, ≤2 líneas, chunkear TODA la narración (NUNCA bloque estático que se trunca) | `ai-video-production/CAPTIONS.md` + CLAUDE.md HR#3/#25/#30 |
| **HYBRID per-clip atomic assembly** | audio+visual+captions burned per clip + Layer 3 narrador continuo | `ai-video-production/PIPELINE.md § 13` + `build_clip_atomic.py` + CLAUDE.md HR#23/#25 |
| **MODEL-CAPABILITIES** (clip_max, constraints i2v/TTS/Gemini) | leer la MATRIX ANTES de producir | `ai-video-production/MODEL-CAPABILITIES-MATRIX.md` + CLAUDE.md HR#28/#29 |
| **Motion primitives** (Ken Burns / parallax / flicker / glow) | animation AI preferida (Ken Burns fallback ≤20%) | `ai-video-production/MOTION-LAYER.md` + CLAUDE.md HR#6/#7 |
| **Audio mastering** | normalize -14 LUFS + limiter | `ai-video-production/AUDIO-MASTERING.md` + `scripts/master-audio.sh` |
| **Regla 30s** (primeros 30s = animation AI) | obligatoria short-form | `ai-video-production/` (animation_30s_rule) + CLAUDE.md HR#6 |
| **Atempo 2x sobre TTS lento** | sí | `ai-video-production/PIPELINE.md § 1` + CLAUDE.md HR#10 |
| **Cost cap** | ≤ 25% sobre el último video exitoso | SYSTEM-LEARNINGS-V3-V4 (vía género) |
| **TDD** (`test_*.py` companion por script nuevo) | obligatorio | `ai-video-production/BOOTSTRAP.md` + CLAUDE.md HR#26 |
| **8 gates pre-render** | Gate 0 spec-completeness + lint + narrative + render-lock + frames + audio + continuity + qa-gate | CLAUDE.md § Pre-render gate |

> **Sabor de género** (densidad/tipo de SFX, voces, color grading, BPM por mood, motion con sabor de género, background creatures/atmospheric motions) → el INGENIERO-PAUTA del género. NO acá.

---

## §1 — DECISION-UI EDITORIAL PACING (técnica choice-UI)

> **Authority:** `CHOICE-MECHANIC.md §9` (creative intent) + canonical-scenes decision-setup grids (empírico 8/8 vía horror). El momento de decisión es un **micro-evento editorial estructurado**, NO "UI suelto sobre clip animado".

### 1.1 Pattern canonical

```
[narration_end] → [pause beat ~0.9s median] → [countdown 3-2-1 (1.0s por dígito)] → [loading bar fills L→R]
                                                [freeze frame OPCIONAL] [filter overlay OPCIONAL]
                                                [audio cue per digit OPCIONAL]
```

### 1.2 Defaults canónicos (medidos — Phase 1, 8/8 refs vía horror)

| Parámetro | Valor canónico | Status | n |
|-----------|----------------|--------|---|
| `countdown_digit_duration_s` | **1.0** ("1, 2, 3 = segundos literales" — user Rule D PRECEDENCE) | validated_via_user_perceptual | user |
| `countdown_pause_beat_s` (gap narration_end → countdown_start) | **0.9** median (p25=0.33, p75=2.1) | validated_via_video_measurement | 14 |
| `ambient_duck_db_during_countdown` | **0** (NO duck obligatorio — refuta -6dB inferido) | validated_via_video_measurement | 20 |
| `freeze_frame_applied` | **false default** (OPCIONAL — 14% refs) | validated_via_video_measurement | 22 |
| `filter_overlay_applied` | **false default** (OPCIONAL — minority pattern) | validated_via_video_measurement | 22 |
| `loading_bar_y_pct` | **52** (≥6% sep de countdown Y46) | validated_via_video_measurement | 8 |
| `countdown_y_pct` | **46** | validated_via_video_measurement | 8 |
| `countdown_visual_style` | **film_leader_academy** (crosshair circle + dígito central grande ~40-50% frame width, serif/condensed bold) | validated_via_direct_frame_verification | 4 |

### 1.3 Timing técnico del countdown (hook + decisiones)

- **Countdown total** = 3 dígitos × 1.0s = **~3.0s** (cada dígito on-screen ~1s). (El rango histórico medido de hook countdown fue 2.2-2.5s a ~0.8s/dígito; el default actual es 1.0s/dígito por user Rule D PRECEDENCE.)
- **Loading bar** = inicia cuando aparecen los botones A/B, termina justo antes del cut de consecuencia. Sync ~1:1 con los botones. Duración target **2.0-2.5s** (variante dramática hasta ~4.2s con % counter explícito).
- **Botones A/B visibles** = ~2.0-2.5s, simultáneo con la loading bar.
- **CTA outro** = corto (~1s), no tapa el cierre.

### 1.4 Freeze frame + filter overlay (OPCIONALES)

- **Freeze frame** (GSAP `paused: true` en narration_end O ffmpeg last-frame extract): separa el decision moment del flow continuo. OPCIONAL (14% refs). Si se usa, runtime control vía GSAP es preferido.
- **Filter overlay** ("looking back at footage": vintage/grano que implica al viewer retroactivamente). OPCIONAL (minority pattern). El TIPO concreto de filtro (sepia horror vs. broadcast-replay sport) es **de género**.

### 1.5 Audio cue per countdown digit

- Si el countdown viene de un AVU (`.mp4` con ticks bundled): **muxear la pista de audio del AVU** (NO componerlo video-only — eso deja el countdown mudo). El AVU trae los ticks sincronizados al dígito = sync bullet-proof.
- Si el countdown se compone con dígitos sueltos: colocar `countdown_tick` / `decision-tick` en CADA beat 3-2-1.
- **Volumen del tick:** audible **sobre el bed** (no ducked debajo), da urgencia a la decisión.
- El SFX concreto (glitch horror vs. silbato/pitido sport) es **de género**.

### 1.6 Anti-pattern

🟥 Countdown con timing flotante (no anclado a narration_end) + clip en movimiento durante el countdown + loading bar pegada al countdown (<6% sep) + sin sync de audio → "elementos UI puestos sueltos sobre video". La estructura editorial colapsa.

✅ Canonical: pause beat → countdown anclado a narration_end (+ ~0.9s) → loading bar Y52 (≥6% sep de countdown Y46) → tick audible per dígito.

> **Implementación detallada (GSAP snippets, CSS filter, freeze frame techniques, AVU mux):** ver el INGENIERO-PAUTA del género (`horror-choice-format/INGENIERO-PAUTA-MASTER § 7.10`) — los snippets concretos son técnicos pero pueden tener referencias de género; el pattern y los defaults agnósticos viven acá.

---

## §2 — UI SAFE ZONES (técnica choice-UI)

> **Authority:** medido 2026-05-15 vía Gemini Vision sobre 50 frames de 10 referentes (vía horror INGENIERO-PAUTA § 7). Fuente raw: `referent-analysis/F1-UI-SAFE-ZONES.json`.

### 2.1 ⚠️ REGLA OPERACIONAL #1 — un UI element por banda Y a la vez

**UN UI element por banda Y por vez.** Si el countdown está activo en Y 35-56%, NO pongas captions en esa banda. Si captions en Y 58-72% activos, NO pongas otro UI en Y 58-72%. Las bandas son **temporalmente exclusivas**. El video se compone en zonas temporales.

🟦 **Corolario — durante un countdown ACTIVO el caption de narración se OCULTA.** La banda Y35-56 es **exclusiva del UI de decisión** (countdown + loading bar + botones) mientras la decisión está en curso. La pregunta narrada del dilema se muestra ANTES del countdown y su caption **termina al arrancar el countdown** (los cues que empezarían dentro del countdown se descartan; el que lo cruza se recorta a `countdown_start`). El audio de narración puede seguir; lo que se oculta es el **caption** sobre esa banda. (Empírico: 8/8 refs auditados no muestran caption de narración encima de un countdown activo — la atención del viewer es del UI de decisión.) Impl de referencia: el burn recorta/descarta el cue narrador al inicio del countdown en build-time.

### 2.2 Position safe zones (n=10 referentes)

| UI element | Y % center | Y band | X % center | Font | Notas |
|-----------|------------|--------|------------|------|-------|
| **Caption narración** | **62%** | 58-72% | 50% | sans-serif | white (red para warning) |
| **Caption warning** | 53% | 21-66% | 50% | sans-serif bold | **red** |
| **Countdown 3-2-1** | **46%** | 35-56% | 50% (center) | sans-serif large | film_leader_academy |
| **Loading bar** | **52%** (revised, era 48%) | 44-51% baseline / 52% en decision shots | 50% | — | ≥6% sep de countdown |
| **Character name labels** | **11.5%** (anchor) / banda 12-40% | top third | sobre cada opción del dyad | **monospaced** (canónico) | white, GRANDES (~64px) |
| **Choice buttons A/B** | stacked top | 7-20% | left-aligned | monospaced | 🟦 SIEMPRE prefijo **"A) …" / "B) …"** (ver 2.2.1) |
| Watermark | 79% | 75-85% | 30% (bottom-left) | sans-serif | always-on |

### 2.2.1 Botones A/B — prefijo de agencia SIEMPRE presente

🟦 **Todo botón de decisión lleva su prefijo literal "A) …" / "B) …"** (la letra + paréntesis antes del texto de la opción). No es cosmético: es la **señal de agencia** que le dice al viewer "esto se elige, vos decidís" y mapea la opción al orden hablado (regla "orden hablado = orden de botones"). Un botón sin prefijo se lee como texto descriptivo, no como una opción accionable. 🟩 El estilo del separador/caja varía (mayúsculas, color, box), pero el prefijo `A)` / `B)` es invariante.

### 2.3 No-overlap matrix (REGLA CRÍTICA)

Cuando un UI element está visible en su banda, NO pongas otro en la misma banda:

| Banda Y | Owner cuando activa | Prohibido en esa banda |
|---------|----------------------|-------------------------|
| **Y 7-20%** | Choice buttons A/B (poll style) | character labels, captions |
| **Y 12-40%** | Character name labels | choice buttons, captions, subject focus |
| **Y 35-56%** | Countdown (cuando activo) | captions, choice buttons, narration text |
| **Y 44-52%** | Loading bar (cuando activa) | captions, countdown (mutuamente exclusivo) |
| **Y 58-72%** | Captions narración (zona canónica) | countdown, loading bar, choice buttons, subject text |
| **Y 75-85%** | Watermark (always-on) | otros UI overlays |

### 2.4 Name labels GRANDES + through-countdown

- **Tamaño:** GRANDE. `fontsize_intent: large` → ~64px (frame 1080px wide, ≈6% de la altura). Legible de un vistazo en el scroll.
- **Posición:** una label **arriba de cada opción** del dyad (no centradas), banda Y 12-40% (anchor Y11.5).
- **Timing:** visibles desde el inicio de la intro Y **DURANTE todo el countdown** — `timestamp_visible_s: [0.0, fin-del-countdown]`. ⛔ NO desaparecen al arrancar el countdown.
- **Font:** monospaced + drop-shadow (canónico, 52% de observaciones monospaced).

### 2.5 Per-speaker Y-band (CAPTION-OVERLAP fix)

- **Narrador (Layer 3) = Y62.** **Diálogo de personaje (Layer 1) = Y52 + tag del nombre** ("[NOMBRE]:").
- NUNCA 2 cues de caption que se solapen en TIEMPO al MISMO Y — **cross-layer narrador-L3 + diálogo-L1 incluido** (no solo char-vs-char). El burn de-conflicta en build-time: cue tardío solapado → offset Y ↑ con ≥6% de separación. (Impl: `deconflict_cue_ys` en `cp5b_build_atomic.py` / `build_clip_atomic.py` — Capa A.)

### 2.6 Loading bar Y52 vs Y48

Y48 era el baseline empírico, pero **causa overlap con countdown Y46% en decision shots densos** (countdown + botones + loading + caption simultáneos). **Revised para decision UI shots: Y52** (`bottom: 940px` en frame 1920) — ≥6% sep de countdown Y46. Para shots NON-decision, Y48 baseline OK.

---

## §3 — CAPTION CHUNKING WORD-TIMED (técnica choice-UI)

> Captions vía Whisper, NUNCA hand-timed (autoridad universal: `ai-video-production/CAPTIONS.md` + CLAUDE.md HR#3). Acá: la regla choice-específica de **cobertura temporal**.

- 🟦 El caption burn DEBE **chunkear TODA la narración del clip** en cues word-timed progresivos (≤2 líneas cada uno), NO un bloque estático (que se trunca a la 1ª frase).
- 🟦 **Caption coverage = 3 niveles:** (A) existence + (B) semantic-match del texto + (C) **TEMPORAL span** (caption presente durante TODA la narración hablada del clip).
- 🟥 Verificar coverage en 1 solo frame = existence only (insuficiente). Chequear coverage temporal.
- (Caso disparador vía horror V6: solo la 1ª frase se mostraba — el resto de la narración del clip iba sin caption.)

---

## §4 — LIP-SYNC RULE (técnica choice-UI)

> Regla de la mecánica choice: un personaje del dyad habla on-screen o no.

| Estado del SPEC | Acción del ingeniero |
|------------------|----------------------|
| `lip_sync_required: true` (shot incluye diálogo del personaje on-screen) | Aplicar lip sync con tool (Hedra / Sync.so / Veo / Kling Omni — ver MODEL-BENCHMARK) ANTES de wire al timeline |
| `lip_sync_required: false` (solo narración voiceover) | **NUNCA usar clip animado con movimiento de boca visible.** Opciones: (1) shot NO animado (estático + Ken Burns) · (2) clip generado con prompt explícito "mouth closed, neutral expression, NO mouth movement" · (3) cover lower face con UI overlay · (4) frame del clip ANTES de cualquier mouth movement |

**Auto-detección del bug:** si vas a usar un clip donde el personaje habla naturalmente, inspeccioná antes de wire — ¿mouth movement visible >0.5s + audio del shot es narrador (no character)? → violación → re-generar o substituir.

🟥 Anti-pattern: clip con boca moviéndose + audio narrador → "está hablando pero no se le entiende". (Caso disparador vía horror: maikol-crucero.)

---

## §5 — 0 CUTS EN HOOK + HOOK-CONTINUITY (técnica choice-pacing)

> **Authority:** vía horror INGENIERO-PAUTA § 3.2 (8/10 refs) + feedback_hook_continuity_no_zoom_cut.

- 🟦 **0 cuts en el hook** (universal, 8/10 refs): el hook es **un plano largo continuo** con motion interno (animation AI / push-in / parallax) durante los primeros ~13-14s. Se sostiene por **motion + narrative tension**, NO por cortes.
- Implicancia operacional: hook con >2 cuts = estás rompiendo el pattern típico.
- 🟦 **Hook-continuity-no-zoom-cut:** el hook = UN solo shot O un push-in continuo. NUNCA cortar entre framings (p. ej. wide-dyad → medium-dyad) dentro del hook — uncanny + señal de AI-detect. Los 8/8 canónicos usan single shot. (Caso disparador vía horror: cinema-abandonado iter 1.)

> La banda de cuts/min global (de-clustered 1-9 / Gemini-perceived 14-22) es técnica de pacing universal → `ai-video-production/PACING-MARKERS.md` + la sección de cuts del INGENIERO del género.

---

## §6 — RELACIÓN CON OTROS DOCS

- **Técnica universal** (todo lo de la tabla §0 heredada-universal) → `ai-video-production/` (Capa A). Este doc apunta, no duplica.
- **Creative intent de la mecánica** (esqueleto, invariante, decisión→consecuencia, framing, counterfactual) → `CHOICE-MECHANIC.md` (Capa A.5).
- **Rotación entre videos** → `ROTATION-RULES.md` (Capa A.5).
- **Técnica con sabor de género** (SFX concretos, voces, color grading, BPM por mood, background creatures/atmospheric motions, GSAP snippets con referencias de género) → el INGENIERO-PAUTA del género (Capa B).
