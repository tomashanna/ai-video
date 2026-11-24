# NARRATIVE.md — [TÍTULO DEL VIDEO]

> Fuente narrativa de verdad para el agente de producción. No tomar decisiones creativas — todo está aquí. Ejecutar en orden: imágenes + variantes → TTS → SFX → medir duraciones → escribir index.html → lint → render → Gemini QA.

**Caption del post:** [pregunta gancho para Instagram]
**Duración objetivo:** 80–95 segundos
**Idioma TTS:** español (`language_code: "es"`)
**Voz ElevenLabs:** `Tj9l48J9AJbry5yCP5eW` (voz canónica — lenta por naturaleza, usar 2x atempo)
**Atempo:** todas las narraciones se procesan a 2x con ffmpeg tras generarlas

---

## Decisiones creativas tomadas (FASE 0 INPUTS)

**Quién es quién:**
- **[NOMBRE_MALO]** = compañero peligroso. Camino del horror. [1 línea descriptiva]
- **[NOMBRE_BUENO]** = compañero seguro. No aparece en el horror. Solo en el cliffhanger final.

**Los 2 dilemas internos:**
- Hito 3 — [categoría del dilema según PATTERNS § 6]. Impulso: [X]. Opción ganadora: [Y]. [Razón breve].
- Hito 4 — [categoría]. Impulso: [X]. Opción ganadora: [Y].

**Cliffhanger:** [NOMBRE_BUENO] te lleva a [escena cálida]. Termina con "Una noche en paz."

**Color grade:**
- Hitos 1–5: `filter: contrast(1.18) saturate(0.45) brightness(0.82)` — frío
- Hito 6 (cliffhanger): `filter: none` en los 3 `<img>` — colores cálidos naturales

---

## Índice de hitos y timing estimado

| Hito | Rango estimado | Estado | Función |
|------|---------------|--------|---------|
| 1 | 0–10s | 🔄 PRODUCIR | Presentación [NOMBRE_MALO] y [NOMBRE_BUENO] |
| 2 | 10–22.5s | 🔄 PRODUCIR | Countdown 3-2-1 + loading bar (elección inicial) |
| 3 | 22.5–46s | 🔄 PRODUCIR | Regla cripta + 1er dilema |
| 4 | 46–64s | 🔄 PRODUCIR | 2do dilema |
| 5 | 64–72s | 🔄 PRODUCIR | Resolución rama [NOMBRE_MALO] — salida |
| 6 | 72–82s | 🔄 PRODUCIR | Cliffhanger [NOMBRE_BUENO] |

> Los tiempos son estimados. Después de generar todos los MP3 y aplicar atempo 2x, medir cada archivo con ffprobe y reconstruir la tabla.

---

## CHECKLIST V8 DE ASSETS A GENERAR

> Esta sección sustituye al "Checklist de assets a generar" simple — incluye variantes obligatorias (V8-1) y SFX dedicado (V8-2).

### Imágenes — con variantes obligatorias (V8-1)

Para cualquier escena que se muestra >4s en el video, generar 2–3 variantes con sufijos `-a`/`-b`/`-c`. Cambiar ángulo / distancia / framing — NO escenario.

- [ ] `h1-characters.png` — [NOMBRE_MALO] (izq) y [NOMBRE_BUENO] (der)
- [ ] `h3-wide-a.png` / `h3-wide-b.png` / `h3-wide-c.png` — POV escenario H3 (3 variantes — escena >8s)
- [ ] `h3-char.png` — close-up [NOMBRE_MALO] dando advertencia
- [ ] `h3-tension-a.png` / `h3-tension-b.png` — elemento de tensión H3 (2 variantes — escena 5-7s)
- [ ] `h3-twist-bad.png` — consecuencia mala H3
- [ ] `h3-twist-good.png` — salida buena H3
- [ ] `h4-wide-a.png` / `h4-wide-b.png` / `h4-wide-c.png` — POV escenario H4
- [ ] `h4-tension-a.png` / `h4-tension-b.png` — elemento de tensión H4
- [ ] `h4-twist-bad.png` — consecuencia mala H4
- [ ] `h4-twist-good.png` — salida buena H4
- [ ] `h5-exit.png` — salida del bosque/escenario
- [ ] `h6-cliff-1.png` *(--no-mono-suffix)* — cliffhanger 1
- [ ] `h6-cliff-2.png` *(--no-mono-suffix)* — cliffhanger 2
- [ ] `h6-cliff-3.png` *(--no-mono-suffix)* — cliffhanger 3

### Narración TTS (vía `ai-video tts`, luego atempo 2x)

- [ ] `h1-narr-2x.mp3`
- [ ] `h3-narr1-2x.mp3`, `h3-narr2-2x.mp3`, `h3-narr3-2x.mp3`, `h3-narr4-2x.mp3`
- [ ] `h4-narr1-2x.mp3`, `h4-narr2-2x.mp3`, `h4-narr3-2x.mp3`, `h4-narr4-2x.mp3`
- [ ] `h5-narr1-2x.mp3`, `h5-narr2-2x.mp3`
- [ ] `h6-narr1-2x.mp3`

### SFX dedicado V8-2 — vía `ai-video sfx` + `sfx-spec.json`

Ver template completo en `SFX-LIST-TEMPLATE.md`. Mínimo por video:
- [ ] ~3 SFX para H1 (howl distante, name stab, etc.)
- [ ] ~3 SFX para H2 (loading drone, flash impact, glass)
- [ ] ~8 SFX para H3 (footsteps loop, whisper, breath, flash, body fall, exhale)
- [ ] ~8 SFX para H4 (similar a H3)
- [ ] ~3 SFX para H5 (gravel footsteps, disappear, first bird)
- [ ] ~5 SFX para H6 (fire crackle, cup toast, warm pad)

### Freesound auxiliar — ver `FREESOUND-QUERIES.md` del proyecto

- [ ] `ambient-forest-wind.mp3` (75s, loop, capa bajo H1-H5)
- [ ] `ambient-dawn-warmth.mp3` (12s, capa bajo H6)
- [ ] `h5-first-bird.mp3` (1.5s, canto distante)
- [ ] `h6-laughter-warm.mp3` (3s, voces humanas reales)
- [ ] `h6-acoustic-strum.mp3` (2s, guitarra acústica real)
- [ ] `h6-dawn-birds.mp3` (4s, coro real)

### Música (Pixabay)

| Segmento | Archivo | Timing | Volumen |
|----------|---------|--------|---------|
| Horror | `music-horror.mp3` | 0–64s | 0.05–0.18 |
| Cliffhanger | `music-dawn.mp3` | 64–82s | 0.13–0.18 |

---

## Prompts de imagen detallados

> Todos los prompts se usan con `ai-video image` aplicando el horror style vía `STYLE_SUFFIX = HORROR_SUFFIX` (en tu copia) o `--style-suffix` — el template es AGNÓSTICO por default (ya NO automático; ver `PRODUCTION-PIPELINE.md` § ai-video image). Los marcados `--no-mono-suffix` van sin suffix (estilo cálido inline en el prompt).

### h1-characters.png
```
[Prompt completo descriptivo de la presentación, ver REFERENCE-ANALYSIS.md sección 3 para patterns validados]
```

### h3-wide-a.png / h3-wide-b.png / h3-wide-c.png (3 variantes — V8-1)
Variante A — POV principal:
```
[Prompt principal]
```
Variante B — distinto ángulo:
```
[Mismo escenario, distinta distancia/framing. Ej: si A es a 3 pasos del personaje, B es a 5 pasos]
```
Variante C — distinto enfoque:
```
[Mismo escenario, low angle o detalle distinto]
```

[... repetir patrón para cada imagen con variantes ...]

---

## Texto TTS exacto por narración

> Copiar el texto exactamente como aparece. No modificar puntuación — afecta la prosodia de ElevenLabs.

### h1-narr (Hito 1):
```
[Texto literal — "Elige a tu compañero. Para esta noche, [NOMBRE_MALO]... o [NOMBRE_BUENO]."]
```

### h3-narr1 (Hito 3 — setup):
```
[Texto literal]
```

[... continuar para todas las narraciones ...]

---

## Plan de motion por escena (V8-3)

> Define qué motion lleva cada plano más allá del Ken Burns base. Esto se implementa en la Fase 5.5 (Motion Pass) del VIDEO-PLAYBOOK.

| Plano | Duración | Ken Burns | Parallax | Flicker | Shake | Vignette pulse | Glitch | Glow | Niebla |
|---|---|---|---|---|---|---|---|---|---|
| h1-characters | 7s | ✅ push-in 1.0→1.05 | – | – | – | – | – | – | – |
| h3-wide (a/b/c) | 9s | ✅ | ✅ 3 capas | – | – | – | – | – | ✅ |
| h3-char (whisper) | 2.3s | ✅ | – | ✅ ojos | ✅ sutil | – | – | – | – |
| h3-tension (a/b) | 5.3s | ✅ | – | – | – | ✅ cierre | – | – | – |
| h3-twist-bad | 3.3s | – | – | – | – | – | ✅ frame | – | – |
| h4-light | 5.5s | ✅ | – | – | – | – | – | ✅ pulse | – |
| h6-cliff-1 (fogata) | 3s | ✅ | – | ✅ fuego | – | – | – | – | partículas |
| ... | | | | | | | | | |

---

## Validación de formato (V7 + V8)

- [ ] **Total palabras TTS:** ~180–220 (rango válido para 90s)
- [ ] **Promedio por oración:** ~5 palabras ✓
- [ ] **Oraciones nominales (mín. 3):** [enumerar] ✓
- [ ] **Oraciones de 1-3 palabras (mín. 2):** [enumerar] ✓
- [ ] **Verbos en presente:** revisado ✓
- [ ] **Opción ganadora va contra impulso primario:** [Hito 3] ✓ [Hito 4] ✓
- [ ] **Cliffhanger termina con "Una noche en paz."** ✓
- [ ] **Compañero peligroso ([NOMBRE_MALO]) tiene 1-2 líneas crípticas** ✓
- [ ] **Compañero seguro ([NOMBRE_BUENO]) NO tiene diálogo** ✓
- [ ] **3+ elementos sensoriales en cliffhanger** ✓
- [ ] **Loading bars: 2.5s exactos × 2** ✓
- [ ] **White flash en cada twist** ✓
- [ ] **V8-1: cada escena >4s tiene ≥2 variantes** ✓
- [ ] **V8-2: SFX list completa por hito** ✓
- [ ] **V8-3: motion plan por escena** ✓

---

# HITO 1 — Presentación

[Estructura completa por hito siguiendo VIDEO-PLAYBOOK.md fase correspondiente]

---

**Última actualización:** [FECHA]
**Estado:** [Narrativa completa / Listo para producción / En producción / Aprobado]
