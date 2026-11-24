# SCORING-RUBRIC.md — Rúbrica de scoring aplicada por el agente

> **Nota de publicación:** versión sanitizada de la rúbrica interna — sin handles reales (anonimizados como `@referent-x`) ni citas de guiones de terceros. Las mediciones numéricas que la respaldan viven en `data/referent-analysis/`. El juez automatizado actual es el prompt calibrado v4 (`ai-video audit-gemini-calibrated`); esta rúbrica es la guía humana/descriptiva.


## ⚠️ Scope: horror-choice paradigm canonical only

> Codified PRE-4.H R2 2026-05-26 per Pattern 7 Capability Matrix methodology (`.claude/skills/ai-video-production/PIPELINE.md` §13.10).

Esta rúbrica de scoring deriva de **horror-choice paradigm** reference videos únicamente (13 refs: 8 viral horror-choice (videos de referencia locales, no versionados) + 5 backrooms variations).

**Forward:** otros paradigmas (tutorial, B2B commercial, compilation, mixed AI/pre-existing) requieren rúbrica + analysis SEPARADOS. F1 NO es universal — describe características de AI-generated viral horror video específicamente. Leerlo para un paradigma no-horror-choice = paradigm mismatch.

> Generado 2026-05-13 PM tras detectar que Gemini Flash Preview da scores demasiado generosos (todos los referentes + nuestros videos 8.5-9.5 sin discriminar).
>
> **Método nuevo:** Gemini describe hechos observables → agente aplica esta rúbrica con criterios estrictos → score con discriminación real.

---

## Las 15 dimensiones del scoring (F1 H-choice)

Cada dimensión 0-10. Score total = promedio ponderado.

### IMAGEN (peso 25%)

#### D1 — Image AI generation quality (0-10)
- **10:** Midjourney v6 / Flux con character LoRA, texturas piel realistas, iluminación volumétrica, character consistency entre tomas
- **8:** Midjourney v6 sin LoRA, detalle alto pero leve drift entre tomas
- **6:** DALL-E 3 / Nano Banana, look "plástico" sutil, character drift visible
- **4:** Nano Banana sin negative prompts, look genérico, character cambia notablemente
- **2:** Generación AI básica con artefactos obvios (dedos extraños, ojos mal)

**Criterio de evaluación:** examinar texturas piel, character consistency entre tomas, artefactos AI visibles.

#### D2 — Character design memorability (0-10)
- **10:** Personajes inolvidables (Bruno-cíclope, Axel-hongo, Pablo-hombre-patata) — híbridos surrealistas que se quedan en la cabeza
- **8:** Diseño memorable con un toque uncanny pero no extremo
- **6:** Personajes humanos estilizados con buen detail
- **4:** Personajes humanos estándar sin nada distintivo
- **2:** Sin character design propio (solo paisajes o objetos)

**Criterio:** ¿podrías describir el personaje a alguien 24h después? ¿le saca conversación?

#### D3 — Variedad de planos (0-10)
- **10:** 5+ tipos de plano distintos (wide + medium + close-up + extreme close-up + POV + detail + overhead)
- **8:** 4 tipos de plano
- **6:** 3 tipos
- **4:** 2 tipos
- **2:** Solo 1 tipo (todo medium o todo POV)

**Criterio:** contar tipos de plano observables en el video.

#### D4 — Color grading dual + accent isolation (0-10)
- **10:** Paleta dual psicológica opuesta entre opciones (verde podrido vs dorado miel) + accent isolation (rojo neón sobre cool)
- **8:** Paleta dual sí, sin accent isolation
- **6:** Una sola paleta cinematic con vignette + crushed blacks
- **4:** Una paleta sin variación entre escenas
- **2:** Sin grading consciente, look "default capcut"

**Criterio:** comparar paleta entre escenas peligrosas vs seguras + buscar elementos en color contrastante.

### SONIDO (peso 25%)

#### D5 — Music quality (0-10)
- **10:** Música layered (drone + pad + melody) que evoluciona con tensión, BPM matching beats narrativos
- **8:** Música layered sin evolución dinámica
- **6:** Música atmosférica simple (drone solo)
- **4:** Música AI genérica de stock
- **2:** Sin música o música totalmente off-tone

**Criterio:** ¿tiene capas? ¿evoluciona? ¿tiene hooks? ¿BPM apropiado?

#### D6 — Voice processing (0-10)
- **10:** ElevenLabs deep voice + compresión alta + bass boost +3dB + presence EQ + de-ess
- **8:** ElevenLabs + compresión + EQ básica
- **6:** ElevenLabs raw con atempo 2x
- **4:** TTS de menor calidad o sin atempo
- **2:** Sin voiceover o voiceover claramente robótico/amateur

**Criterio:** ¿la voz suena "en tu cara"? ¿corta en altavoz móvil?

#### D7 — SFX density (0-10)
- **10:** 30+ SFX eventos por minuto (5+ ambient layers + 10+ foley + 5+ impacts + caption pops)
- **8:** 20-30 SFX/min
- **6:** 15-20 SFX/min
- **4:** 8-15 SFX/min
- **2:** <8 SFX/min (música + voz solas)

**Criterio:** contar SFX distintos en el video, normalizar por minuto.

#### D8 — Sound design coherencia y density (0-10)
- **10:** Cada acción visual tiene reforzador sonoro + ambient continuo + reverb específico por entorno + ducking automático + sound fabric 100%
- **8:** Most de lo anterior, dead zones <1s
- **6:** Sound design decente pero algunos eventos sin SFX
- **4:** Solo música + algunos SFX puntuales
- **2:** Sound design pobre, dead zones obvias

**Criterio:** ¿hay dead zones? ¿hay foley específico? ¿hay reverb por entorno?

### CAPTIONS (peso 15%)

#### D9 — Tipografía y efecto (0-10)
- **10:** Monospaced (VT323) para names + Sans bold (Montserrat) para narration + drop shadow + 3-class system + inline keyword highlight rojo/amarillo
- **8:** Sans bold + drop shadow + keyword highlight
- **6:** Sans bold + drop shadow uniforme
- **4:** Sans con thick stroke (anti-pattern)
- **2:** Instagram native font o display fonts

**Criterio:** examinar font, efecto separation, presencia de highlight inline.

#### D10 — Sync precision (0-10)
- **10:** Whisper-sync palabra por palabra, frame-accurate
- **8:** Sync correcto pero ocasional desfase de 1 frame
- **6:** Sync por frases (no por palabras)
- **4:** Hand-timed con desfase visible
- **2:** Captions estáticos sin sync

**Criterio:** observar coincidencia entre voz audible y caption visible.

### NARRATIVA (peso 20%)

#### D11 — Hook 0-3s (0-10)
- **10:** Visual impossible/uncanny + countdown + stake escalation inmediata ("ELIGE A TU COMPAÑERO PARA ESTA NOCHE")
- **8:** Visual fuerte + caption hook claro
- **6:** Hook decente pero no escalates stakes
- **4:** Hook lento, primeros 3s setup descriptivo
- **2:** Sin hook claro, viewer scroll likely

**Criterio:** evaluar primeros 3s específicamente. ¿obliga a no scrollear?

#### D12 — Stakes (0-10)
- **10:** Vital — muerte vs supervivencia, decision points dramáticos
- **8:** Alto — pérdida significativa
- **6:** Medio — incomodidad
- **4:** Bajo — trivial
- **2:** Sin stakes claros

#### D13 — Counterfactual outro con punchline (0-10)
- **10:** Punchline con humor negro / surrealismo extremo / contraste tonal radical
- **8:** Counterfactual tonal contrast pero sin punchline memorable
- **6:** Counterfactual presente pero genérico
- **4:** Counterfactual mencionado brevemente
- **2:** Sin counterfactual / outro abrupto

### EDICIÓN (peso 15%)

#### D14 — Felt cadence + internal motion (0-10)
- **10:** 18-30 eventos perceptibles/min (hard cuts + push-ins + parallax + caption swaps + SFX) + cero frames estáticos
- **8:** 15-20 eventos/min, motion en cada frame
- **6:** 10-15 eventos/min, motion mayoritario
- **4:** 5-10 eventos/min, frames estáticos ocasionales
- **2:** <5 eventos/min, slideshow feel

**Criterio:** contar eventos visuales distintos por minuto.

#### D15 — Mastering quality (0-10)
- **10:** LUFS -14 ±0.3 + LRA 3-6 + true peak <-1 dBTP + heavy multiband compression + corta en altavoces móviles
- **8:** LUFS -14 ±0.5 + compresión decente
- **6:** LUFS -14 sin compresión adicional
- **4:** LUFS fuera de rango pero audio decente
- **2:** Audio sin master / amateur

**Criterio:** medir LUFS objetivamente + escuchar en altavoz móvil.

---

## Score total ponderado

```
Score = (D1 + D2 + D3 + D4) × 0.25/4
      + (D5 + D6 + D7 + D8) × 0.25/4
      + (D9 + D10)          × 0.15/2
      + (D11 + D12 + D13)   × 0.20/3
      + (D14 + D15)         × 0.15/2
```

## Anchors de calibración

Para que esta rúbrica sea consistente, anchored a casos conocidos:

| Score range | Significado | Ejemplo |
|-------------|-------------|---------|
| 9.5-10 | Estándar de oro, viral asegurado | @referent-a top |
| 9-9.5 | Pro completo, todas las dimensiones bien | @referent-a regular |
| 8-9 | Pro con 1-2 dimensiones flojas | nuestros mejores |
| 7-8 | Bueno pero notable gap | nuestros buenos |
| 6-7 | Decente pero amateur visible | nuestros antiguos |
| 5-6 | Promedio, no destaca | content de baja calidad |
| <5 | Amateur evidente | beginner content |

## Cómo aplicarla

1. Gemini analiza el video con prompt descriptivo (NO scoring)
2. Agente lee la descripción
3. Para cada dimensión D1-D15, aplica criterios y asigna score 0-10
4. Calcula total ponderado
5. Reporta breakdown por dimensión (no solo total)

Esto da scoring DISCRIMINATIVO entre videos en lugar del scoring compensatorio de Gemini.
