---
name: horror-choice-format
description: GENRE skill — horror-choice estilo @referent-a. Dilemas binarios, "malo aparente" vs "bueno aparente", hitos H1-H6, cliffhanger "Una noche en paz". Activar siempre que la tarea mencione: hito, choice, dilema, twist, cliffhanger, loading bar, white flash, "elige a tu compañero", "malo aparente", "bueno aparente". Por default asume delivery format = reel (vertical 9:16, 60-90s) pero es combinable con otros formats. DEPENDE de `ai-video-production` (toolkit técnico) + `video-director` (workflow). NUNCA activar sola.
---

# Horror-Choice Format — GENRE skill

> Este es un GENRE skill (qué cuenta el video), NO un delivery format skill (cómo se entrega). El delivery por default es `reel` (vertical 9:16) — combinación validada en mina-abandonada v15.
>
> Para combinaciones distintas (horror-choice × instagram-story versión mini, horror-choice × youtube-short, etc.) ver `ai-video-production/DELIVERY-FORMATS.md` y combinar este skill con el `formats/<delivery>.md` correspondiente.

## ⛔ LECTURA OBLIGATORIA al activar esta skill

> **🔄 ARQUITECTURA ACTUALIZADA 2026-05-13 PM:** la pauta narrativa autoritativa ahora es **`PAUTA-MASTER.md`** (derivada empíricamente de los 8 videos canónicos en `/videosref_elige_tu_compa/`). `CREATIVE-BRIEF.md` está **DEPRECATED** (estaba mal-grounded en V1/V2/V3 antiguos + V7 nuestro). Leé el master nuevo, ignorá el brief viejo excepto como historial.

Si activaste esta skill, leé estos archivos ANTES de planear o ejecutar:

1. **`<repo-root>/CLAUDE.md`** — context global + arquitectura 3 capas
2. **⭐ `<repo-root>/.claude/skills/horror-choice-format/PAUTA-MASTER.md`** — **AUTORIDAD CREATIVA EMPÍRICA del ARQUITECTO** (derivada de 8 videos virales canónicos). Reemplaza CREATIVE-BRIEF.md. Tiene: filosofía, estructura temporal validada, Slots A-H con data de los 8, reglas inviolables con compliance N/8, hallazgos críticos vs pauta vieja.
2.5. **⭐ `<repo-root>/.claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md`** — **AUTORIDAD TÉCNICA EMPÍRICA del INGENIERO** (derivada de mediciones n=5+ referentes F1, escalando a n=10). Tiene: pace WPM 156-195, LUFS -13.88, cuts/min 5.25, music BPM 99-161, coverage 87%, vignette 1.43, **0 cuts en hook (universal)**, **outro RMS drop -12dB**. El ingeniero consulta acá ANTES de cualquier decisión técnica (pace, mix, cuts, motion, color, BPM, UI timing). NUNCA comparar contra nuestras producciones previas (mina/bosque/elige/pueblo) — están en `/referent-analysis/our-production-archive/` con prefijo "NO AUTORIDAD".
2.7. **⭐ `<repo-root>/.claude/skills/horror-choice-format/canonical-scenes/INDEX.md` + `ref-XX.md`** correspondiente al pattern elegido (añadido 2026-05-16 Bloque I) — **scene-by-scene EMPÍRICO de los 8 canónicos**. INDEX.md tiene 12 grids cross-ref por `pattern_category` (hook / setup / decision_setup / consequence_A/B / cliffhanger). Cada ref-XX.md tiene 10-14 beats narrativos con `who's there` + `what they do LITERAL` + narration Whisper + UI active + animation tier + pattern observation. **El arquitecto consulta ANTES de diseñar SPEC v6** — sin esto el arquitecto improvisa (caso cabina-14: 17 bugs narrativos). Complementa a PAUTA-MASTER (síntesis macro) con detalle shot-by-shot.
3. **`<repo-root>/.claude/skills/horror-choice-format/PAUTA.md`** — workflow de producción + criterios de calidad + reglas V7+V8
4. **`<repo-root>/.claude/skills/horror-choice-format/PATTERNS.md`** — reglas técnicas perennes (timing %, audio, visual, mecánica elección). Validar contra PAUTA-MASTER si hay discrepancia (gana PAUTA-MASTER).
5. **⭐ `<repo-root>/.claude/skills/horror-choice-format/video-log.md` (AUTORITATIVO PARA ROTACIÓN PATTERN)** — registro de videos producidos. OBLIGATORIO consultar antes de elegir pattern.
6. Este archivo (`SKILL.md`) entero — hard rules del formato

7. **El sub-doc específico de tu tarea**:
   - Diseñar concepto + slots → **`PAUTA-MASTER.md` (todo)** + video-log para rotación
   - Escribir guion → `SCRIPT-WRITING-GUIDE.md` + **PAUTA-MASTER §§ 3, 10, 11**
   - Construir HTML por hito → `VIDEO-PLAYBOOK.md`
   - Bootstrap proyecto nuevo → `BOOTSTRAP-NEW-PROJECT.md`
   - Producción técnica → `PRODUCTION-PIPELINE.md`
   - ⚠️ `CREATIVE-BRIEF.md` (deprecated) — solo consultar para contexto histórico, NO como autoridad

**ACTIVÁ EN PARALELO obligatoriamente:**
- **`video-director`** — workflow + quality bar + decisiones estratégicas
- **`ai-video-production`** — toolkit técnico (PIPELINE, MOTION, CAPTIONS, SFX, QA, etc.)

Si la tarea es animar con Kling, **también `video-animation`**.

**NO planees ni ejecutes hasta haber leído**: CLAUDE.md + **PAUTA-MASTER.md (COMPLETO)** + PAUTA.md + PATTERNS.md + video-log.md + este SKILL.md + el sub-doc de tu tarea.

(⚠️ NO USES `CREATIVE-BRIEF.md` como guía — está DEPRECATED. Toda la autoridad creativa vive en `PAUTA-MASTER.md`.)

---


## Qué es este skill

Este skill encodea las **reglas, patterns, schema y plan de producción del formato horror-choice** ("Elige a tu compañero" estilo `@referent-a`).

Es **format-specific**. El toolkit técnico general (TTS, image gen, SFX gen, motion, captions, render, QA) vive en `ai-video-production/`. Este skill construye encima de ese toolkit.

## Validado en

- **Video #1 — elige-companero** (Cristóbal beetle-head vs Gerald uncanny smile, casa rural). V7 aprobado por Gemini con 9.5/10.
- **Video #2 — bosque-abandonado** (Berni gaunt 60s vs Yonaiker joven, bosque oscuro). V3 con sound design completo, pendiente animación.

## Cuándo activar este skill

Activar cuando el usuario:

- Pide generar un nuevo script o narración del formato (`SCRIPT-WRITING-GUIDE.md` + `PATTERNS.md` § 5-6)
- Menciona algún hito (H1-H6) o pide renderear
- Pide prompts de imagen para personajes del formato (`PATTERNS.md` § 4 arquetipos + `REFERENCE-ANALYSIS.md`)
- Quiere configurar timing, loading bars, transiciones (`PATTERNS.md` § 1, 8)
- Presenta opciones A/B y pide decidir (resolver contra `PATTERNS.md`, no preferencia personal)
- Valida un render contra el formato (`PATTERNS.md` § 1 + Gemini QA con prompt extendido en `PAUTA.md` § 2)
- Pregunta por qué un video viral de referencia hace X (`REFERENCE-ANALYSIS.md`)

**Para cualquier tarea técnica concreta** (generar audio, imágenes, SFX, motion, captions, render, QA), activar también `ai-video-production`.

## Filosofía Phase 2 (simplicidad primero)

Hasta validar el formato en producción (1 video con >70% retención + 3 variantes manuales) seguimos en Phase 2: simple, local, rápido. No construir generadores parametrizados (esos van en Phase 4, ver `TEMPLATE-SPEC.md` deferido).

- Edit HTML directo en lugar de template engines
- Hardcoded en lugar de configs
- Manual en lugar de automated
- Reusar antes que generar
- Una sola fuente de verdad por asset

## Documentos en este skill

| Doc | Cuándo leerlo |
|---|---|
| **`PAUTA.md`** | **Punto de entrada al formato.** Primero, siempre. Define orden de lectura, criterios de calidad, las 6 V7 + 3 V8 rules, errores conocidos. |
| `PATTERNS.md` | Reglas perennes del formato (timing %, personajes, dilema moral, cliffhanger, choice mechanics, prohibiciones) |
| `SCRIPT-WRITING-GUIDE.md` | Plantilla maestra para escribir guion del formato + plan de assets V8 |
| `VIDEO-PLAYBOOK.md` | Playbook secuencial fases 0→7 con templates HTML/GSAP por tipo de hito |
| `PRODUCTION-PIPELINE.md` | Detalles técnicos APLICADOS al formato (V7 rules CSS, Kling prompts horror). Para pipeline general ver `ai-video-production/PIPELINE.md`. |
| `BOOTSTRAP-NEW-PROJECT.md` | Bootstrap APLICADO al formato (FASE 0 inputs horror-specific). Para bootstrap general ver `ai-video-production/BOOTSTRAP.md`. |
| `REFERENCE-ANALYSIS.md` | Análisis crudo de Gemini de los 3 videos virales `@referent-a` |
| `TEMPLATE-SPEC.md` | Schema del generador parametrizado del formato (Phase 4, deferido) |
| `templates/` | Templates específicos del formato: NARRATIVE, SFX-LIST, sfx-spec, FREESOUND-QUERIES (opcional) |

## Hard rules del formato (nunca romper)

> Para hard rules del toolkit general (V8-1 variantes, V8-2 SFX, V8-3 motion), ver `ai-video-production/SKILL.md`. Estas son **específicas del formato horror-choice**:

1. **La opción ganadora va contra el impulso primario.** Nunca un dilema donde la opción moral obvia gana (ver `PATTERNS.md` § 6).
2. **Loading bars exactamente 2.5 segundos absolutos.** No proporcional.
3. **Hard cuts en twists con white flash 2-3 frames.** Nunca fade ni dissolve.
4. **Texto on-screen nunca anima** (no fade, no slide). Hard cut only.
5. **Verbos siempre en presente.** Nunca futuro. "Te quema" no "te quemará".
6. **Cliffhanger cierra con frase canónica del pattern** (no es siempre "Una noche en paz"). La frase de cierre varía por pattern (P1/P9 → "Una noche en paz" canon; otros → variante cálida/nihilista según archetype). Ver `PAUTA-MASTER.md` §§ 13, 15.
7. **Diálogo según apariencia (variabilidad, NO regla absoluta):** en doble-amable AMBOS pueden hablar/aparecer **SOLO en el HOOK (H1 dyad de presentación)**. **INVARIANTE (5/5 refs): el bueno-aparente NUNCA aparece en el recorrido jugado tomando decisiones — solo en hook + counterfactual + cliffhanger.** Las tentaciones del recorrido jugado vienen del compañero ELEGIDO (scary) + el instinto/entorno. Ver `PAUTA-MASTER.md` § 2.
8. **Color grading frío todo el video excepto cliffhanger** (warm amber/gold).
9. **Narración requiere post-procesado** (atempo 2x, EQ, compresión, reverb dark room <0.6s) — raw TTS nunca aceptable.
10. **Duración sweet spot 80-100 segundos.** Fuera de ese rango cae la retención.
11. **Las 6 reglas V7 del formato** — text stroke captions, choice labels 64px, separador A→B, puente narrativo, CTA engagement, Gemini QA gate. Ver `PAUTA.md` § 3.
12. **Instagram safe zones (V7-7)** — captions en zona y=300-1380. Ver `PAUTA.md` § 3 V7-7.
13. **Las 3 reglas V8 aplicadas al formato** — variantes -a/-b/-c, capa SFX dedicada con prompts horror, motion mínimo Ken Burns + parallax/flicker. Ver `PAUTA.md` § 3.7.

## Estado del formato

- **Última actualización:** 2026-05-10
- **V7 render aprobado**: elige-companero `renders/hito-completo-v7.mp4` (Gemini 9.5/10)
- **V8 rules added** post-mortem bosque-abandonado v2
- **Pending**: re-render V8 de elige-companero con motion + SFX dedicado; producir nuevos videos del formato en V8
