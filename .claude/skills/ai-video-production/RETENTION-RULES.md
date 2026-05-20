# RETENTION-RULES.md — Reglas de retención para vertical short-form

> **Scope**: 📱 **Vertical short-form ÚNICAMENTE** — Reels, TikTok, IG Reels, YouTube Shorts, Instagram Stories, vertical 9:16, duración ≤120s.
>
> ❌ **NO aplica a**: YouTube long-form (≥3min), B2B horizontal commercial, web embeds, TV/CTV ads, ningún formato con tiempo de viewing controlado.
>
> Si tu proyecto NO es vertical short-form, **ignorar este doc completamente** — las reglas aquí asumen scroll-feed agresivo y métricas de retention rate.

---

## Por qué este doc existe

Vertical short-form tiene dinámicas de retención completamente distintas a otros formatos. El swipe-away decisivo ocurre en los primeros 1-3 segundos. La curva de retention desciende exponencialmente.

Estas reglas son universales DENTRO de vertical short-form (aplican a CUALQUIER genre: horror, tutorial, B2B short, ad, comedy, news, testimonial). Cada genre/format-specific skill HEREDA estas reglas.

---

## Las 5 reglas no-negociables

### Regla 1 — Hook visual + caption en frame 0

**Window**: 0.0s — 0.3s

**Qué debe pasar**:
- Frame 0 ya tiene visual impactante (NO fade-in lento desde negro)
- Caption visible desde el primer frame audible
- Audio inicia inmediatamente (no silencio inicial >0.5s)

**Por qué**: viewer scrolling decide en <1s si quedarse. Si el frame 0 es "loading visual" o silencio, swipe-away garantizado.

**Patrón validado** (mina-abandonada v15): teaser empty-mine + 2 ojos ominosos + caption "ELIGE A TU COMPAÑERO" desde 0.1s.

### Regla 2 — Hook narrativo completo en 2-3s

**Window**: 0.0s — 3.0s

**Qué debe pasar**:
- En 3s el viewer debe **entender la propuesta**: ¿de qué va esto? ¿qué tipo de video es?
- Hook no es solo "imagen bonita" — es **claridad narrativa**

**Anti-pattern**: intro lento tipo "hola, bienvenidos a mi canal, hoy les voy a contar..." → 50% bounce en segundo 2.

**Patrón validado**: en v15 a los 3s ya ves los 2 personajes materializando + escuchas "Elige a tu compañero" + lees "ELIGE A TU COMPAÑERO".

### Regla 3 — Intro ≤10% del total

**Window**: 0.0s — (duration × 0.10)

| Duración total | Intro máx |
|---|---|
| 30s | 3s |
| 60s | 6s |
| 90s | 9s |
| 120s | 12s |

**Qué cuenta como "intro"**: presentación de personajes/contexto + setup + countdown/transition. La HISTORIA o el CONTENIDO PRINCIPAL debe arrancar antes del 10%.

**Por qué**: dato empírico — Reels que pasan más del 15% en intro tienen completion rate <40%. Los que terminan intro en ≤10% mantienen ≥65%.

### Regla 4 — Cero imágenes estáticas en primeros 30s

**Window**: 0.0s — 30.0s (o 50% del total si video es <60s)

**Qué debe pasar**:
- Toda escena con `data-start < 30s` tiene Kling, video, o motion CSS pronunciado
- Ken Burns sutil (scale 1.0→1.02) NO cuenta como motion suficiente

**Por qué**: imágenes estáticas en esta ventana se sienten "diapositiva" y bajan retention rate del 70% al 40% sin posibilidad de recovery.

**Doc complementario**: `video-animation/ANIMATION-LAYER.md` § PRE-GATE (mismo gate, doc específico de Kling).

### Regla 5 — UI fuera de zona de plataforma

**Window**: todo el video

| Elemento | Posición safe |
|---|---|
| Captions | bottom: 540px (IG Reel) / bottom: 380px (YT Short) / center (IG Story) |
| Loading bar | bottom: 700px |
| Name labels | top: 220px |
| End CTA | bottom: 540px |

**Por qué**: la UI nativa de cada plataforma tapa zonas específicas del frame. Sin respetar safe zones, captions críticos quedan invisibles para el viewer.

**Detalle por plataforma**: ver `formats/reel.md` § UI Safe Zones, `formats/instagram-story.md` § UI Safe Zones, etc.

---

## Reglas universales de claridad narrativa (añadidas 2026-05-16)

### Claridad > estilismo en short-form

Cualquier formato (h-choice, tutorial, B2B, documental) bajo 90s vertical: **priorizar claridad narrativa de acción/contexto sobre tono estilístico**. Manifestación per-format:

- **horror-choice**: NO sonar tenebroso (genre temptation). El tono emerge de visual + SFX + música, NO de la narración.
- **tutorial**: NO sonar académico
- **B2B**: NO sonar corporate

**Test**: ¿el viewer entiende qué pasa en 1ra escucha sin caption? Si NO → reescribir narración.

**Caso disparador 2026-05-16**: cabina-14 V1 — narración estilizada produjo confusion sobre lógica narrativa. Reform en PAUTA-MASTER § 3 regla "Narración CLARA NO tenebrosa".

### Narrative simplicity wins

1 frase setup + 1 frase decisión/acción/punto principal por evento. **Más palabras = menos retención.**

- Setup complejo no funciona en short-form
- Character hablando directo > narrator describiendo (cuando aplique)
- Staccato lyrical ("Choca. Caes.") solo en climax peak — el resto es prosa coherente con sujeto + verbo + conexión

Ver memoria `feedback_narrative_simplicity.md` + `feedback_narration_coherence.md`.

---

## Métricas de éxito (post-publish)

Para validar que estas reglas funcionan, mirar en las analytics:

| Métrica | Target mínimo | Excelente |
|---|---|---|
| **Retention 3s** | ≥65% | ≥80% |
| **Retention 30s** | ≥50% | ≥70% |
| **Completion rate** | ≥45% | ≥65% |
| **Re-watch rate** | ≥15% | ≥30% |

Si una de estas cae por debajo del mínimo → revisar contra las 5 reglas. Probablemente una falla.

---

## Cómo aplicar al iniciar proyecto vertical short-form

```
1. Confirmar delivery format = reel | youtube-short | instagram-story
2. Leer este doc completo
3. Diseñar el shot list aplicando regla 1 (hook frame 0) + regla 4 (animar primeros 30s)
4. Calcular timing intro según regla 3 (≤10%)
5. Layout UI según regla 5 (safe zones por plataforma)
6. Validar en QA con dimensiones específicas:
   - "¿Hook frame 0 + caption visible?"
   - "¿Algún plano estático en primeros 30s?"
   - "¿UI fuera de safe zones?"
```

---

## Anti-patterns (resumen rápido)

| ❌ Anti-pattern | Donde se documenta el fix |
|---|---|
| Intro de >10s sin hook visual | `formats/reel.md`, `formats/youtube-short.md` |
| Fade-in lento desde negro | Regla 1 acá |
| Imágenes estáticas en primeros 30s | `video-animation/ANIMATION-LAYER.md` § PRE-GATE |
| Caption en `bottom: 0-540px` (IG) | `video-director/ANTI-PATTERNS.md` § Captions |
| Hand-timed captions | `CAPTIONS.md` |
| Sin captions sobre narrador | `CAPTIONS.md` § Hard rule Whisper-sync (universal) |
| Render letterboxed 16:9→9:16 | `formats/reel.md` § Anti-patterns |

---

## Cross-references

- `formats/reel.md` — delivery format que hereda esto
- `formats/youtube-short.md` — delivery format que hereda esto
- `formats/instagram-story.md` — delivery format que hereda esto
- `video-animation/ANIMATION-LAYER.md` § PRE-GATE — regla 4 detallada
- `CAPTIONS.md` — captions Whisper-sync (regla 1)
- `video-director/ANTI-PATTERNS.md` § Retención — anti-patterns relacionados
- `DELIVERY-FORMATS.md` — catálogo padre

---

## Validado en

- **mina-abandonada v15-final** (horror-choice × reel, 90s) — Score Gemini 9.9/10. Las 5 reglas se cumplen 100%.

---

## Última actualización

2026-05-11. Inicial. Extraídas de v15 case study + ai-video-production patterns existentes.
