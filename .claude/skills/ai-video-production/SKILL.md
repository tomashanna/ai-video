---
name: ai-video-production
description: TOOLKIT TÉCNICO base para CUALQUIER video con IA (HyperFrames + ElevenLabs + Gemini + GSAP). Cubre TTS, imágenes, SFX, motion (Ken Burns/parallax/flicker/glow), captions Whisper, variantes -a/-b/-c, mix volumes, bootstrap, QA Gemini, character consistency, HyperFrames gotchas. Activar SIEMPRE para ejecución técnica concreta — y SIEMPRE en combo con `video-director` (orquestador/INGENIERO) + skill del formato si aplica (`horror-choice-format`, etc.). NUNCA activar sola. En sistema three-agent (arquitecto + ingeniero + auditor): este skill es parte del lado INGENIERO que ejecuta CREATIVE-SPEC.yaml del arquitecto (`creative-director`).
---

# AI Video Production — Toolkit técnico del lado INGENIERO

> **Sistema three-agent (post-2026-05-17, AUDITOR formalizado):** este skill es parte del lado INGENIERO. El INGENIERO recibe CREATIVE-SPEC.yaml del ARQUITECTO (`creative-director` skill) y ejecuta técnicamente sin tocar decisiones creativas.
>
> - **Arquitecto** diseña: story, characters, script, intent visual/audio
> - **Ingeniero (vos)** ejecuta: TTS, image gen, SFX, animation, render
> - **Auditor** verifica: handoffs del ingeniero vs autoridad canónica, independiente (ver `creative-director/AUDITOR-PROTOCOL.md`)
>
> Si user activa solo este skill sin haber pasado por el arquitecto + sin CREATIVE-SPEC.yaml, **flag al user**: "Necesito un CREATIVE-SPEC. ¿Querés que active `creative-director` skill primero?"

## ⛔ LECTURA OBLIGATORIA al activar esta skill

Si activaste esta skill, leé estos archivos ANTES de planear o ejecutar:

1. **`docs/OPERATING-MANUAL.md`** — hard rules globales + arquitectura three-agent
2. **`.claude/skills/video-director/SKILL.md`** — rol del INGENIERO + workflow 5 checkpoints + SPEC ingestion
3. **`.claude/skills/creative-director/HANDOFF-PROTOCOL.md`** — protocolo de los 5 checkpoints con architect approval gates
4. Este archivo (`SKILL.md`) entero — toolkit + hard rules técnicas
5. Si existe `creative-specs/<project>.yaml` para ejecutar → leelo COMPLETO antes de generar assets
3. **El sub-doc específico de tu tarea** (lista abajo en "Documentos en este skill"):
   - **⭐ Tarea = video NUEVO desde cero / bootstrap → `DELIVERY-FORMATS.md` PRIMERO** (identificar combo genre × format) + `formats/<delivery>.md` + `BOOTSTRAP.md` + skill del genre. Si short-form: también `RETENTION-RULES.md`.
   - Tarea = generar TTS / imágenes / SFX → `PIPELINE.md`
   - Tarea = motion CSS → `MOTION-LAYER.md`
   - Tarea = captions → `CAPTIONS.md`
   - Tarea = SFX → `SFX-PIPELINE.md`
   - Tarea = variantes de imagen → `IMAGE-VARIETY.md`
   - Tarea = personajes consistentes → `CHARACTER-CONSISTENCY.md`
   - Tarea = QA Gemini → `QA.md` (adaptar prompt al delivery format — ver `formats/<delivery>.md` § QA específico)
   - Tarea = bootstrap proyecto → `BOOTSTRAP.md` + `formats/<delivery>.md`
   - Tarea = cortes narrativos → `NARRATIVE-LED-EDITING.md`
   - Tarea = render + lint + audit → `PIPELINE.md` § 5+11 + `AUDIT.md`
   - Tarea = bugs HyperFrames → `HYPERFRAMES-GOTCHAS.md`
   - Tarea = retención short-form → `RETENTION-RULES.md` (📱 Reels/TikTok/Shorts solo)
4. **`assets/library/LIBRARY.md`** — chequear si ya hay assets reutilizables ANTES de generar

**Esta skill nunca se activa sola.** Para tareas de video activá también:
- `video-director` SIEMPRE (orquestador + workflow + quality bar)
- Skill del formato si aplica (`horror-choice-format`, etc.)
- `video-animation` si la tarea es Kling/Replicate

**NO planees ni ejecutes hasta haber leído este SKILL.md + el sub-doc de tu tarea + LIBRARY.md.**

---

> Skill agnóstico al formato. Encodea las técnicas, herramientas y patrones que sirven para cualquier video con IA en HyperFrames.

## Cuándo activar este skill

- Generar TTS / imágenes / SFX en cualquier proyecto de video con IA
- Aplicar motion layer (Ken Burns, parallax, flicker, vignette, etc.)
- Configurar captions auto vía Whisper
- Bootstrappear un proyecto nuevo de video (cualquier formato)
- Calcular mix volumes
- Generar variantes de imagen para escenas largas
- Hacer QA con Gemini Video Analyzer
- Decidir naming conventions de assets

## Cuándo NO activarlo solo

Si trabajás en un formato específico (horror-choice, documental, etc.), activá AMBOS skills:
1. **Este** (`ai-video-production`) — para las técnicas base
2. **El skill del formato** (`horror-choice-format`, etc.) — para las reglas específicas

El skill del formato es responsable de la estructura narrativa, plantillas de guion, reglas viral-format, y otros patterns específicos.

## Documentos en este skill

| Doc | Cuándo leerlo |
|---|---|
| `PIPELINE.md` | Cualquier tarea técnica: TTS, imágenes, render, música, asset naming, HyperFrames gotchas |
| `MOTION-LAYER.md` | Animar planos estáticos con CSS/GSAP — Ken Burns + parallax + flicker + vignette + glitch + glow + niebla |
| `NARRATIVE-LED-EDITING.md` ⭐ | **El narrador dicta los cortes** — taxonomía de 7 tipos (WHITE FLASH, BLACK + LOW THUD, BLACK + DRONE BAJO, BLACK + RISE DRONE, BLACK + EXHALE, BLACK + PUNCT SILENCE, WARM WHITE). Aplicar a cualquier formato con narrador + cambios narrativos. |
| `ANIMATION-LAYER.md` | **REDIRECT** — el doc se movió a `video-animation/ANIMATION-LAYER.md` (skill propia para auto-trigger correcto en "animar/Kling/Replicate"). |
| `SFX-PIPELINE.md` | Generar SFX vía `ai-video sfx`, loop expansion >22s, mix volumes |
| `IMAGE-VARIETY.md` | Diseñar variantes -a/-b/-c para escenas >4s (evita slideshow feel) |
| **`CHARACTER-CONSISTENCY.md`** ⭐ | **Anchor + reference workflow para mantener personajes idénticos entre tomas.** Obligatorio en TODO video con personajes. |
| **`ELEMENTS-LIBRARY.md`** | Sistema híbrido de componentes UI (countdown/loader/lower-third) — selección + compatibility check intra-video |
| `CAPTIONS.md` | Auto-generar captions sincronizados con Whisper |
| `BOOTSTRAP.md` | Iniciar un proyecto de video desde cero (genérico, no asume formato). Incluye § 5.5 **shot list + character anchors gate + caption↔narrador continuity gate** (proyectos nuevos). |
| `QA.md` | Validar el render final con Gemini Video Analyzer + checklist universal (11 dimensiones, umbral 9.7, anti-alucinación) |
| **`HYPERFRAMES-GOTCHAS.md`** ⭐ | **Bugs sutiles HyperFrames** — timeline namespace `window.__timelines.main`, video data-duration > clip → NEGRO, lint warnings semantics |
| **`MICRO-COMPOSITION-WORKFLOW.md`** ⭐ | **Workflow para cambios estructurales** — validar en HTML standalone de 5-15s antes de tocar `index.html` completo. Incluye join-point QA. |
| **`DELIVERY-FORMATS.md`** ⭐ | **Catálogo de formats de entrega** (reel, youtube-short, youtube-long, b2b-commercial, instagram-story, libre). Sub-docs en `formats/`. Cada genre skill se combina con un format. |
| **`formats/<format>.md`** | Specs técnicas + reglas de cada delivery format (aspect, duration, UI safe zones, retention rules) |
| **`RETENTION-RULES.md`** ⭐ | **Reglas de retención para vertical short-form** (Scope: 📱 Reels/TikTok/Shorts ≤2min). NO aplica a long-form ni horizontal. Heredado por `formats/reel.md`, `formats/youtube-short.md`, `formats/instagram-story.md`. |
| `templates/` | Templates copyables: scripts (`ai-video tts`, `ai-video image` **con `--ref`**, `ai-video sfx`, `ai-video captions`), `.env.example`, `templates/project/hyperframes.json` |

## Hard rules generales (cualquier video con IA)

1. **Narración nunca es raw TTS.** Aplicar `atempo=2.0` con ffmpeg si la voz canónica es lenta (verificar voice ID del proyecto).
2. **Captions nunca son manuales.** Siempre auto-generadas desde el audio con Whisper. Los timings manuales se desincronizan.
3. **Escenas >4s requieren ≥2 variantes de imagen.** Reusar el mismo PNG produce slideshow feel, especialmente con motion aplicado.
4. **Ningún plano estático >2s sin motion.** Ken Burns es el piso, no el techo.
5. **Capa SFX dedicada obligatoria.** Música + narración + ticks NO es sound design.
6. **Mix volumes estandarizados:** Narración 1.0, música 0.05-0.18, SFX eventos 0.20-0.35, flash impacts 0.55-0.65, ambient continuo 0.10-0.18.
7. **Reservar `data-track-index` 60-110 para SFX.** Otros rangos: 0-19 imágenes, 20-39 texto, 40-59 audio principal.
8. **No publicar nada sin Gemini QA score ≥ 9.0** (ver `QA.md` para prompt extendido).

## Stack técnico de referencia

- **HyperFrames** — composición + render (1080×1920, 30fps, H.264/AAC)
- **GSAP 3.14+** — animaciones
- **ElevenLabs** — TTS (`text_to_speech.convert`) + SFX (`text_to_sound_effects.convert`)
- **Gemini Nano Banana** (`gemini-3.1-flash-image-preview`) — generación de imágenes
- **Gemini 3 Flash** — video analyzer / QA
- **OpenAI Whisper** — captions auto
- **ffmpeg** — atempo, stream_loop, fades, format conversion
- **Replicate Kling** — animación de imágenes estáticas (opcional)

## Cómo usar este toolkit en un formato nuevo

Cuando crees un skill para un formato nuevo (ej: `documental-format/`, `educacional-format/`), tu skill debe:

1. **Referenciar este skill** en su `SKILL.md` ("uso ai-video-production como base técnica")
2. **Definir sus propias reglas de formato** (estructura narrativa, patterns de timing, paleta visual, dilemas si aplican)
3. **Reusar los scripts del toolkit** (`ai-video tts`, `ai-video image`, `ai-video sfx`, `ai-video captions`) sin modificar
4. **Parametrizar lo específico** — por ejemplo en `ai-video image` reemplazar `HORROR_SUFFIX` por un `STYLE_SUFFIX` configurable
5. **Heredar el motion layer** (`MOTION-LAYER.md`) — solo elegir qué técnicas aplican a tu formato
6. **Heredar el SFX pipeline** — solo redefinir los prompts contextuales al tema

Ejemplo de referencia: `horror-choice-format/` aplica este toolkit al formato `@referent-a`.

## Estado / referencias

- **Última actualización:** 2026-05-10
- **Validado en:** elige-companero (V7, 9.5/10) + bosque-abandonado (v3)
- **Skills relacionados:** `horror-choice-format` (formato específico), `hyperframes` (CLI), `gsap` (animaciones), `video-analyzer` (QA)
