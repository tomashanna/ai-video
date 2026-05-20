> ⛔ **DEPRECATED 2026-05-15**: POST-MORTEM standalone was a write-only artifact — learnings never propagated to consumed docs (PATTERNS-LIBRARY.md last modified May 10, no recent project referenced).
>
> **New flow**: append 2-3 learning bullets directly to `<format>-format/video-log.md` (the doc that IS consulted before each new video for pattern rotation).
>
> **Template retained** to avoid breaking references in older projects (mina-abandonada, bosque-abandonado, etc.). NEW projects do NOT need to copy this template anymore.
>
> See `pre-render-gate/SKILL.md` Q15 (new flow) and `.claude/commands/video-new.md` PASO 6 (new flow).
>
> **Removal scheduled**: este archivo se borra cuando NINGÚN proyecto activo referencie POST-MORTEM.md (typically 2-3 sprints después de la deprecación). Hasta entonces se conserva como compat shim.

---

# Post-mortem `<proyecto>` `<version>`

> Generado automáticamente por el agente productor al alcanzar el stop point pre-Kling o post-Kling. Llenar TODOS los campos — son la base del meta-review cross-video.

**Fecha:** `<YYYY-MM-DD>`
**Stage:** `pre-kling | post-kling`
**Agent:** `<claude-model-id>`

---

## 1. Score Gemini final

| Métrica | Valor | Vara | Status |
|---|---|---|---|
| Score Gemini | `<X.X>` / 10 | ≥ 9.7 | ✅ / ⚠️ / ❌ |
| Iteraciones corridas | `<N>` / 3 | ≤ 3 | ✅ / ❌ |
| vs video previo (baseline) | `<+X.X / -X.X>` | mejora esperada | ✅ / ⚠️ |

---

## 2. Pattern usado (matriz expandida § 3.5)

**Pattern #:** `<1-10>` — `<nombre>`

| Eje | Valor |
|---|---|
| Apariencia visual | `Asimétrica / Doble monstruosa / Doble amable` |
| Verdad personaje A | `Malo / Bueno` |
| Verdad personaje B | `Malo / Bueno` |
| Plot twist incluido | `Sí (tipo: ...) / No` |
| Meta-cliffhanger | `Sí / No` |
| Slot H0 personal stakes | `Sí (objeto: ...) / No` |

---

## 3. Decisiones creativas (1 párrafo conciso)

`<Setting específico. Nombres malo + bueno aparente. Verbo H1. Dilemas H3 y H4 concretos. Twist específico si aplica. Cliffhanger setting H6. CTA elegido.>`

---

## 4. Library reuse

| Categoría | Reuse | Nuevos | % Reuse |
|---|---|---|---|
| SFX | `<N>` | `<N>` | `<X%>` |
| Voces | `<N>` | `<N>` | `<X%>` |
| Música | `<N>` | `<N>` | `<X%>` |
| **TOTAL** | `<N>` | `<N>` | `<X%>` |

**Assets nuevos promovidos a library:** `<lista de paths>`

---

## 5. Dimensiones Gemini QA — score por dimensión

| # | Dimensión | Score | Status | Notas |
|---|---|---|---|---|
| 1 | Variedad visual | `<X.X>` | ✅⚠️❌ | |
| 2 | Capa SFX completa | `<X.X>` | ✅⚠️❌ | |
| 3 | Cortes narrativos | `<X.X>` | ✅⚠️❌ | |
| 4 | Captions sync + legibilidad | `<X.X>` | ✅⚠️❌ | |
| 5 | Motion (Ken Burns + extras) | `<X.X>` | ✅⚠️❌ | |
| 6 | POV continuity | `<X.X>` | ✅⚠️❌ | |
| 7 | Mix volumes canónicos | `<X.X>` | ✅⚠️❌ | |
| 8 | Specs IG | `<X.X>` | ✅⚠️❌ | |
| 9 | Duración animaciones | `<X.X>` | ✅⚠️❌ | |
| 10 | Continuidad cap↔narrador | `<X.X>` | ✅⚠️❌ | |
| 11 | Inventario UI verificado | `<X.X>` | ✅⚠️❌ | |
| 12 | Plot twist coherence | `<X.X>` | ✅⚠️❌ | si aplica |

---

## 6. Verificación reglas críticas

| Regla | ¿Cumplió? | Detalle |
|---|---|---|
| Vara Gemini ≥9.7 | ✅ ❌ | |
| Primeros 30s = 100% Kling (hard rule #7) | ✅ ❌ | si post-kling |
| Plot twist 3 condiciones (si aplica) | ✅ ❌ | lógica / imágenes / narración |
| Setup elements timing 2.5-3.5s (si aplica) | ✅ ❌ | duraciones reales |
| Show 70/30 (0.7-0.9 palabras/seg) | ✅ ❌ | palabras totales / duración |
| Rotación archetype (≠ último video) | ✅ ❌ | comparar con video-log.md |
| Frame audit (audit-frames.py) | ✅ ❌ | issues encontrados |
| Audit narrativo (audit-narrative.py) | ✅ ❌ | issues encontrados |

---

## 7. Issues conocidos NO resueltos

`<Lista de issues que el agente detectó pero decidió no fixear, con razón>`

Ejemplo:
- Foto del padre en H3 duró 2.6s (target 2.5-3.5s — justo por encima del piso, podía ser 3.0)
- Mix música un toque alta en H4

---

## 8. Costos por fase

| Fase | API | Costo |
|---|---|---|
| TTS narrador | ElevenLabs | $ |
| SFX (nuevos) | ElevenLabs | $ |
| Imágenes | Gemini Nano Banana | $ |
| Captions Whisper | Local | $0 |
| Gemini QA (N rounds) | Gemini 3 Flash | $ |
| Frame audit | Gemini Vision | $ |
| Kling (si post) | Replicate | $ |
| **TOTAL** | | $ |

vs cap budget: `<X / cap Y>` ✅⚠️❌

---

## 9. Aprendizajes para próximos videos

`<2-5 bullets concretos sobre qué funcionó / qué falló / qué aplicar en próximo video>`

Ejemplos:
- Pattern 10 funciona muy bien con setup retroactivo + personal stakes (slot H0)
- Library reuse 75% es alcanzable cuando setting comparte ambient con video previo
- Voice ID canónico de Hugo se aplicó bien sin issues de pronunciación

---

## 10. Path al render + assets

| Recurso | Path |
|---|---|
| Render | `<proyecto>/renders/<version>.mp4` |
| NARRATIVE | `<proyecto>/NARRATIVE.md` |
| index.html | `<proyecto>/index.html` |
| Frame audit report | `<proyecto>/renders/<version>-frame-audit.json` |
| Gemini QA report | `<proyecto>/renders/<version>-qa-report.txt` |

---

## Cross-references

- `horror-choice-format/video-log.md` — actualizar con archetype + pattern + score + path
- `video-director/PERFORMANCE.md` — alimentar meta-review cada 10 videos
- `video-director/PATTERNS-LIBRARY.md` — promover patterns validados cross-video
