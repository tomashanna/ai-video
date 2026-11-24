# FORMAT-DETECTION.md — Identifica el formato antes de aplicar reglas

> **Por qué este doc existe:** la v1 de mis reglas codificadas mezclaba universal vs format-specific. Un agente futuro produciendo un video B2B podría aplicar "warm/eerie color grade" + "monospaced character names" sin darse cuenta que esas reglas son horror-choice específicas. Este doc le dice al agente cómo identificar el formato ANTES de elegir reglas.

> Generado 2026-05-13 desde análisis de 7 referentes (4 H-choice + 1 AI mystery + 1 meme essay + 1 POV synthwave). Refinará a medida que cubramos más formatos.

---

## ⛔ Regla cero — SIEMPRE identificar formato antes de aplicar reglas

Antes de aplicar cualquier regla codificada en `CAPTIONS.md` / `COLOR-GRADING.md` / `PACING-MARKERS.md`, **identificar el formato del video objetivo**. Sin esto, las reglas se aplican mal.

```bash
# Pseudo-flow antes de cualquier producción de video
1. ¿Cuál es el genre del video?
2. ¿Cuál es el delivery format?
3. → Determinar combo (genre × delivery)
4. → Aplicar reglas universales (siempre)
5. → Aplicar reglas format-specific (solo las que corresponden)
```

---

## Las 4 reglas UNIVERSALES (siempre, sin importar formato)

Estas 4 SIEMPRE aplican. Sin excepciones:

| # | Regla | Doc | Script |
|---|-------|-----|--------|
| U1 | **LUFS -14 ±0.5 dB integrated** | `AUDIO-MASTERING.md` | `scripts/master-audio.sh` |
| U2 | **Drop shadow > thick stroke** en todo texto | `CAPTIONS.md` | n/a |
| U3 | **Vignette aplicado** (sutil a pronunciado según formato) | `COLOR-GRADING.md` | n/a |
| U4 | **Crushed blacks + high contrast** | `COLOR-GRADING.md` | n/a |

**Validación:** 7/7 referentes analizados las cumplen.

---

## Decision tree — identificar formato

```
START
│
├── ¿El video tiene VOICEOVER continuo con script estructurado?
│   │
│   ├── SÍ
│   │   │
│   │   ├── ¿La narrativa es CHOICE-BASED (elige A o B, decision points)?
│   │   │   │
│   │   │   ├── SÍ → ¿Hay archetype dyad con nombres (Bruno/Pablo)?
│   │   │   │       │
│   │   │   │       ├── SÍ → F1.a HORROR CHOICE NARRATIVO
│   │   │   │       └── NO → ¿Es binary visual (puertas, casas, lugares)?
│   │   │   │                ├── SÍ → F1.b HORROR CHOICE PUERTAS / LIMINAL
│   │   │   │                └── NO → F1.c CHOICE GENÉRICO (otro nicho)
│   │   │   │
│   │   │   └── NO → ¿Es exploration/mystery descriptivo?
│   │   │           │
│   │   │           ├── SÍ con AI imagery → F2 AI MYSTERY / SPECULATIVE HORROR
│   │   │           ├── SÍ con tutorial/how-to → F5 TUTORIAL (n=0 referentes, codificar)
│   │   │           ├── SÍ con product demo → F6 PRODUCT DEMO (n=0)
│   │   │           ├── SÍ con brand story → F7 BRAND STORY (n=0)
│   │   │           └── SÍ con documentary → F8 DOCUMENTARY (n=0)
│   │   │
│   │   └── NO → reformular: ¿hay voz pero sin script narrativo?
│   │           │
│   │           ├── Talking head testimonial → F9 TESTIMONIAL (n=0)
│   │           ├── Reaction commentary → F10 REACTION (n=0)
│   │           └── Comedy sketch → F11 SKETCH (n=0)
│   │
│   └── NO (sin voiceover continuo)
│       │
│       ├── ¿Hay ÚNICA caption persistente top (essay-style)?
│       │   │
│       │   ├── SÍ con footage existente → F3 MOVIE-CLIP MEME ESSAY
│       │   └── SÍ con AI imagery → F12 AI ESSAY (n=0)
│       │
│       ├── ¿Audio es PRIMARILY música + ambient (sin habla)?
│       │   │
│       │   ├── POV first-person + neon → F4 NIGHT POV SYNTHWAVE
│       │   ├── Music video con lyrics → F13 LYRIC VIDEO (n=0)
│       │   ├── Aesthetic/mood video → F14 AESTHETIC (n=0)
│       │   └── Sports highlight → F15 SPORTS HIGHLIGHT (n=0)
│       │
│       └── ¿Footage de archivo/película + sin captions narrativos?
│           └── F16 ARCHIVE/FOUND FOOTAGE (n=0)
END
```

---

## Tabla de reglas por formato

### F1 — Horror choice (a + b + c)

| Doc | Regla | Aplica |
|-----|-------|--------|
| `CAPTIONS.md` § 3 clases (name/narration/warning) | ✓ |
| `CAPTIONS.md` Y 65% bottom-center narration | ✓ |
| `CHARACTER-NAMES-CATALOG.md` monospaced names | ✓ (a) — NO en (b)(c) |
| `COLOR-GRADING.md` LUT_NARRATIVE warm/eerie | ✓ (a) |
| `COLOR-GRADING.md` LUT_CHOICE cool/cinematic | ✓ (b) |
| `COLOR-GRADING.md` paleta dual psicológica (Puerta 1 vs Puerta 2) | ✓ (b) |
| `PACING-MARKERS.md` 2-7 cuts/min (hard cuts) + felt cadence ~30-40/min | ✓ |
| `MOTION-LAYER.md` parallax 3D obligatorio | ✓ |
| Whisper-sync captions | ✓ |
| Highlight INLINE rojo/amarillo en keywords (NUEVO 2026-05-13) | ✓ |
| 3 decision points + counterfactual outro | ✓ |
| Film grain ~10% | ✓ |
| ElevenLabs voice deep + compression alta | ✓ |

### F2 — AI Mystery / Speculative Horror (n=1, baja confianza)

| Regla | Aplica |
|-------|--------|
| Color grade cool/desaturated + color isolation accent | ✓ |
| NO captions narrativos (audio-led) | ✓ |
| Watermark sutil bottom-center | ✓ |
| Wide variety shot types (drone wide + medium AI + POV) | ✓ |
| 7+ cuts/min hard cuts | ✓ |
| Push-in + parallax | ✓ |
| Cosmic horror / megalofobia tone | ✓ |
| Found footage / GoPro POV touch | ✓ |

**NO aplica de F1:** 3 clases captions, monospaced names, warm/eerie, Whisper-sync, archetype dyad.

### F3 — Movie-clip Meme Essay (n=1, baja confianza — referente 6/10, no es benchmark)

⚠️ **CAVEAT importante:** ref-02 fue categorizado 6/10 por Gemini. Es un viral exitoso pero NO un benchmark profesional. Si codificamos esta categoría, hacerlo con referentes ≥8/10.

| Regla preliminar | Aplica |
|-------------------|--------|
| Footage existente (películas, archivo) | ✓ |
| Single caption persistente TOP Y 20-25% | ✓ |
| Emojis incorporados en caption | ✓ |
| 1-2 cuts/min (slow pacing) | ✓ |
| Música licenciada | ✓ |
| **REQUERIDO PARA PRO:** sound design completo (foley + ambient + impacts) | ❌ ref-02 lo falla |
| **REQUERIDO PARA PRO:** captions personalizados (no Instagram nativo) | ❌ ref-02 lo falla |
| **REQUERIDO PARA PRO:** AI clean-up de movimientos (no glitches) | ❌ ref-02 lo falla |

**NO aplica de F1:** prácticamente nada — es otro formato.

### F4 — Night POV Synthwave (n=1, baja confianza)

| Regla | Aplica |
|-------|--------|
| Oversaturated neon (cyan + magenta + crimson + ácido) | ✓ |
| POV first-person siempre | ✓ |
| Motion blur direccional + bloom | ✓ |
| Center composition (rompe rule of thirds) | ✓ |
| NO captions narrativos | ✓ |
| Audio electronic music synthwave | ✓ |
| Black crush + saturation peak | ✓ |
| NO film grain (bloom instead) | ✓ |
| 3-5 cuts/min con speed ramp | ✓ |
| Coherencia estética RADICAL en grid (brand identity) | ✓ |

**NO aplica de F1:** todo color grading (es opposite), todas las reglas de captions, monospaced names.

### F5-F16 — Formatos NO cubiertos aún

Estos requieren referentes profesionales antes de codificar reglas. **Hasta tener n≥3 por formato:**
- Aplicar solo las 4 reglas universales
- Documentar suposiciones razonadas, marcarlas como "needs validation"
- NO aplicar reglas de otros formatos por analogía sin evidencia

---

## Flujo de uso del agente

```python
# Pseudo-código del flujo
def produce_video(genre, delivery_format, content_spec):
    # Paso 1: identificar formato
    format_id = detect_format(genre, delivery_format, content_spec)

    # Paso 2: aplicar SIEMPRE reglas universales
    apply_rule("LUFS_-14")
    apply_rule("DROP_SHADOW_NOT_STROKE")
    apply_rule("VIGNETTE")
    apply_rule("CRUSHED_BLACKS")

    # Paso 3: aplicar reglas del formato detectado
    format_rules = FORMAT_RULES[format_id]
    for rule in format_rules:
        apply_rule(rule)

    # Paso 4: SI el formato es F5-F16 (no cubierto):
    if format_id.startswith("F5") or "n_zero" in format_id:
        warn("Formato sin referentes profesionales. Solo aplico universales + "
             "extrapolación razonada. Necesita validation humana extra.")

    # Paso 5: pre-render-gate gates
    run_gate_audit_audio()         # universal
    run_gate_check_pacing()        # depende del formato (target distinto F1 vs F4 vs F3)
    run_gate_vignette_check()      # universal
    run_gate_monospaced_check()    # solo si format=F1.a
    # ...
```

---

## Cuándo agregar un nuevo formato

Para agregar F5+ con reglas confiables:

1. **Conseguir ≥3 referentes profesionales del formato** (≥500k views idealmente)
2. **Correr el mismo pipeline:** scene detection + LUFS + Whisper + Gemini Vision frames + **Gemini full-video con audio**
3. **Identificar patrones presentes en TODOS los 3** (no en 1-2)
4. **Crear sección en este doc** con regla y evidencia
5. **Crear sección en CAPTIONS/COLOR-GRADING/PACING** si las reglas difieren
6. **Pre-render-gate:** agregar checks específicos del formato

Sin n≥3 → NO codificar reglas, solo documentar "extrapolación pendiente de validación".

---

## Anti-patterns de format detection

❌ **Aplicar reglas F1 (horror-choice) a cualquier video con AI imagery.** No todo AI es horror-choice. F2 también es AI pero tiene reglas opuestas (cool vs warm).

❌ **Asumir "es horror" = usar warm/eerie.** F2 horror también pero usa cool. Depende del SUB-formato.

❌ **Reusar caption-name monospaced en formatos sin character archetype.** Si no hay Bruno/Pablo, no hay anchor. Es estética horror-choice, no estética genérica.

❌ **Aplicar 2-7 cuts/min como universal.** F1 tiene felt cadence ~30-40/min (push-in + parallax + caption swap dentro de hard-cut shots). F3 tiene 1-2 cuts/min. F4 tiene 3-5 cuts/min. NO hay un target universal.

❌ **Codificar reglas con n=1.** ref-02 era n=1 y resultó ser amateur. n=3 mínimo antes de tratar como pattern.

---

## Limitaciones actuales

- **n=1 en F2/F3/F4:** las reglas son tentativas. Necesitan validación con 3-5 referentes adicionales por formato.
- **F3 invalidado parcialmente:** ref-02 puntuó 6/10. Las reglas codificadas pueden ser de un video amateur-avanzado, no profesional.
- **F5-F16 sin cobertura:** "editor capaz de TODO" es aspiracional sin estos formatos.
- **Sesgo de creator en F1:** 4/4 referentes son @referent-a. Las reglas pueden ser de este creator específicamente, no del genre.

Estas limitaciones se cierran consiguiendo más referentes (3-5 por formato, ≥500k views, mix de creators).
