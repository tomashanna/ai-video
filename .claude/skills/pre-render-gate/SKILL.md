---
name: pre-render-gate
description: ⛔ INVOCAR OBLIGATORIO antes de cualquier render o reporte al usuario en proyectos de video. Skill bloqueante que ejecuta checklist Y/N de 24 puntos críticos (16 base + 4 referent-validated post 2026-05-13 + Q21 referent-profile + Q22 editorial-UI + Q24/Q25 AVU post-2026-05-19; numeración llega a Q25, Q23 ausente). Si CUALQUIER respuesta es No → PARAR, completar, re-invocar. Sin esto los videos fallan reproduciblemente (casos cabana-tormenta + isla-faro + pueblo-fantasma-desierto). Cubre: scripts QA copiados (8 gates), video-log.md consultado, pattern rotado, NARRATIVE.md cumple Show 70/30, plot twist coherente, primeros 30s = animation AI planeada, TTS sin "..." antes proper nouns, narración coverage >40%, sin gaps narrativos >2s, música coverage >85%, 8 gates obligatorios ejecutados, video-log.md learnings appended, human-checklist ejecutado, Q17 cuts/min 2-7, Q18 LUFS -14 ±0.5, Q19 vignette aplicado, Q20 monospaced fonts para character names, Q21 audit-against-referent ≥85% métricas críticas en p25-p75 bands.
---

# pre-render-gate — Checklist bloqueante pre-render

## Cuándo invocar

**OBLIGATORIO antes de:**
- `npx hyperframes render` (cualquier render)
- Declarar stop point pre-animation al usuario
- Llamar a Replicate (animation AI image-to-video — Kling/Hailuo/Seedance según MODEL-BENCHMARK)
- Reportar al usuario "el video está listo"

NO es opcional. NO se saltea por urgencia. Sin esto, los videos fallan reproduciblemente (cabana-tormenta v3+ paró en 9.3, isla-faro v1 paró en 9.3, ambos con bugs detectables por este gate).

## Cómo funciona

Responder Y/N a CADA pregunta del checklist abajo. Si cualquier respuesta es N → STOP, completar la pieza faltante, re-invocar el gate desde el inicio.

NO marcar Y a algo que no se hizo. NO marcar Y por aproximación. Solo Y si está demostradamente completo.

---

## ⛔ CHECKLIST — 24 preguntas Y/N

> **Q-count nota** (corregido post long-doc-audit): el checklist tiene **24 preguntas reales** numeradas **Q1–Q25** — la numeración **salta Q23** (slot vacío, nunca asignado). Breakdown: 16 base (Q1-Q16) + 4 referent-validated (Q17-Q20) + Q21 referent-profile + Q22 editorial-UI + Q24/Q25 AVU. El body manda sobre cualquier conteo legacy.
>
> **Gates = 8** (canónico `docs/OPERATING-MANUAL.md` § Pre-render gate): Gate 0 `ai-video audit-spec-completeness` (BLOQUEANTE, corre 1º) + Lint + audit-narrative + render-lock + audit-frames + audit-audio + continuity-check + qa-gate. Q11 abajo los lista los 8 (Gate 0 incluido).

### Setup técnico (verificar primero)

1. **¿El toolkit está instalado y los gates disponibles?**
   ```bash
   uv run ai-video doctor && uv run ai-video list | grep -E 'audit-narrative|render-lock|audit-frames|audit-audio|continuity-check|qa-gate'
   ```
   Si falta algo: `uv sync --all-extras` en la raíz del repo.

2. **¿`<genre>-format/video-log.md` leído antes de elegir pattern?**
   ```bash
   [ -f ../../.claude/skills/<genre>-format/video-log.md ] && echo "✓ exists" || echo "✗ MISSING — bootstrap del formato incompleto"
   ```
   El video-log.md es autoritativo para rotación pattern + alimenta learnings post-render (reemplaza POST-MORTEM standalone, deprecated 2026-05-15 por write-only — learnings nunca se propagaban).

### Narrativa (verificar antes de generar assets)

3. **¿Leíste `<genre>-format/video-log.md` y elegiste pattern NO repetido?**
   - Patterns sobre-usados (>2 veces consecutivas) ≠ elegidos
   - Pattern justificado por rotación en el NARRATIVE.md o reporte

4. **¿El pattern elegido pertenece a la matriz expandida § 3.5 (10 patterns + meta)?**
   - NO inventaste un archetype nuevo
   - Si tiene plot twist: pattern 3, 8, 9, 10 o meta-cliffhanger

5. **Si el pattern tiene plot twist: ¿cumple las 3 condiciones?**
   - **Lógica clara**: viewer puede explicar twist en 1 frase post-video
   - **Imágenes acompañan**: visual evidence del twist (no solo narrado)
   - **Narración explica el link**: 1 frase explícita (no metáfora vaga)
   - Test: leer twist en voz alta — ¿un viewer sin contexto previo puede explicarlo?

6. **Si hay setup retroactivo del twist: ¿el elemento de setup dura 2.5-3.5s en pantalla?**
   - NO 1s (= viewer no procesa)
   - Verificar con `grep data-duration index.html` para el elemento crítico

### Producción (verificar antes de render)

7. **¿NARRATIVE.md cumple Show 70/30 (0.7-0.9 palabras/seg)?**
   ```bash
   # Contar palabras de líneas que empiezan con "Narrador" o "narr"
   grep -E "^(Narrador|narr|h[0-9]-narr)" NARRATIVE.md | wc -w
   # Dividir por duración total en segundos
   ```
   Target: 63-81 palabras para 90s. >100 = sobre-narrado. <50 = atmosférico.

8. **¿NARRATIVE.md NO tiene "..." antes de proper nouns?**
   ```bash
   grep -nE "\.\.\.\s*(KRAVEN|MARCO|HUGO|SANTI|<otros proper nouns>)" NARRATIVE.md
   ```
   Causa mispronunciación TTS → cascada de regens. Reemplazar "..." por "." o ",".

9. **¿Primeros 30s del Reel = animation AI planeada?** (model-agnostic per `animation_30s_rule.md` memoria)
   - Revisar shot list: toda imagen con data-start < 30s tiene flag "animation AI obligatoria"
   - Modelo según `video-director/MODEL-BENCHMARK.md` § 1.1 / § 2.0 (HOOK VIRAL OVERRIDE: Kling 2.5 Turbo Pro default para hook)
   - NO Ken Burns ni estática en esa ventana

10. **¿Character anchors generados antes de escenas con `--ref`?**
    - Anchor por personaje recurrente (uno por outfit canónico)
    - Spot-check anchors antes de generar escenas

### Render + QA (verificar antes de reportar al usuario)

11. **¿Los 8 gates pasaron exit 0 después del render draft?**
    - **⛔ `ai-video audit-spec-completeness --spec ../../creative-specs/<id>.yaml --cp 5` → exit 0 (Gate 0 BLOQUEANTE — inventario SPEC asset_list/ui vs filesystem, corre ANTES de todo)**
    - `npx hyperframes lint` → 0 errors reales
    - `ai-video audit-narrative` → 0 issues críticos
    - `ai-video render-lock acquire <proyecto>` → lock obtenido
    - `ai-video audit-frames --max-issues 2` → ≤2 frames con issues
    - **⭐ `ai-video audit-audio --video renders/draft.mp4 --html index.html` → ≤2 issues** (NUEVO 2026-05-13 — detecta gaps narrativos + música ausente)
    - **⭐ `ai-video continuity-check --narrative NARRATIVE.md --html index.html` → ≤2 issues** (NUEVO 2026-05-13 — detecta caminos rotos + cobertura <40%)
    - `ai-video qa-gate --score <X.X> --stage pre-kling --iteration <N>` → exit 0 (score ≥9.7)

12. **¿Cobertura de narración ≥70%?** (`ai-video audit-audio` v2 lo reporta como `narration_pct`)
    Vara basada en 3 videos exitosos: mina v15 77%, bosque v10 70%, elige V7 73%. Pueblo fallido tuvo 30.9%. Si <70% → el viewer percibe trama fragmentada aunque Gemini lo apruebe holísticamente.

13. **¿Avg block duration ≥4.5s?** (`ai-video audit-audio` v2 lo reporta como `avg_block`)
    Vara basada en exitosos: mina 6.07s, bosque 5.24s, elige 4.73s. Pueblo fallido tuvo 2.34s = tartamudeo. **MÁS IMPORTANTE que cobertura** — narrador con frases cortas suena entrecortado aunque sume mucho tiempo total.

14. **¿Sound fabric ≥99%?** (`ai-video audit-audio` v2 lo reporta como `sound_fabric_pct`)
    Narración + ambient + música cubren prácticamente todo. Dead zones ≥1s sin nada sonoro = bug.
    Los exitosos: 99.9-100%. Pueblo también 100% (su problema NO era dead zones, era narración corta).

15. **¿Learnings de este proyecto agregados a `<genre>-format/video-log.md`?** (NUEVO 2026-05-15 — POST-MORTEM standalone deprecated)
    Append 2-3 bullets al video-log incluyendo:
    - Pattern usado (matriz § 3.5) + score Gemini final + audit-against-referent match % (cuando ai-video audit-against-referent disponible, Bloque C)
    - 1 bullet "qué funcionó" (replicar en futuros videos)
    - 1 bullet "qué no funcionó" (anti-pattern descubierto, si aplica)
    - Costo total del proyecto

    Razón: el video-log.md se consulta antes de cada nuevo video (rotación pattern + cross-video lessons). POST-MORTEM standalone era write-only — nunca propagaba.

16. **¿HUMAN-CHECKLIST ejecutado (gate humano del usuario)?**
    El gate humano detecta lo que ningún script ve. Antes de declarar "listo": el usuario abre el render y responde las 7 preguntas de `video-director/HUMAN-CHECKLIST.md`. **NO publicar sin esto.** En autopilot autonomous mode, esto se traduce a: agente reporta al usuario "esperando HUMAN-CHECKLIST" — NO declara "listo" por su cuenta.

### Referent-validated (post 2026-05-13 — análisis 7 referentes)

17. **¿Cuts/min en rango 2-7?** (validado contra 7 referentes — pacing target empírico)
    ```bash
    DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/draft.mp4)
    CUTS=$(ffmpeg -i renders/draft.mp4 -filter:v "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -c "pts_time")
    CUTS_PER_MIN=$(echo "scale=2; $CUTS * 60 / $DURATION" | bc)
    echo "Cuts/min: $CUTS_PER_MIN"
    ```
    Target: 2-7 cuts/min para horror narrativo. <2 = demás static (riesgo bounce). >7 = MTV/overcut (rompe inmersión). Ver `ai-video-production/PACING-MARKERS.md`.

18. **¿LUFS integrado en -14 ±0.5 dB?** (Instagram Reels mastering standard)
    ```bash
    MEASURED=$(ffmpeg -i renders/draft.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 \
      | grep '"input_i"' | grep -oE '"-?[0-9.]+"' | tail -1 | tr -d '"')
    echo "LUFS: $MEASURED (target -14 ±0.5)"
    ```
    7/7 referentes entre -13.76 y -14.45. Si fuera → ejecutar `scripts/master-audio.sh renders/draft.mp4`. Ver `ai-video-production/AUDIO-MASTERING.md`.

19. **¿Vignette aplicado en composición?** (universal 7/7 referentes)
    ```bash
    # ⭐ Fase 0 (2026-06-04): gate determinístico reemplaza el grep manual — cubre Q19 Y Q20 en una corrida
    uv run ai-video audit-style-markup --format <format> \
      --spec ../../creative-specs/<id>.yaml --html index.html
    # Exit 0 → ✓ ambas · Exit 1 → falta vignette markup (Q19) o mono font en names (Q20) · Exit 2 → can't-measure
    ```
    Si no hay vignette → agregar `<div id="vignette-overlay">` con CSS según `ai-video-production/COLOR-GRADING.md`.

20. **¿Font monospaced presente para character names (si archetype usa nombres)?**
    ⭐ Cubierto por la MISMA corrida de `ai-video audit-style-markup` de Q19 (lee `characters[]` del SPEC — ya no hace falta el grep manual con lista hardcodeada de nombres; detecta labels por selector canónico O por texto matching los nombres del SPEC; sin name labels → not_applicable automático).
    Ver `horror-choice-format/CHARACTER-NAMES-CATALOG.md` y `ai-video-production/CAPTIONS.md` sistema 3 clases.

### Referent profile matching (post 2026-05-15 — dual gate hard rule #1)

21. **¿`ai-video audit-against-referent` retorna exit 0 (≥85% métricas críticas en rango canónico)?** (NUEVO 2026-05-15 — referent profile matching, complemento de Gemini ≥9.7)
    ```bash
    uv run ai-video audit-against-referent --video renders/draft.mp4 --html index.html
    ```
    Compara nuestro video vs F1 canonical n=10 (`data/referent-analysis/F1-INGENIERO-MEASUREMENTS.json`). Tolerance per métrica = **p25-p75 bands** (interquartile range).

    **Critical metrics** (failure relevant):
    - `pace.wpm_total` (sweet spot ~153-180 wpm)
    - `audio.lufs_integrated` (-14 ±0.5)
    - `pacing.cuts_per_min` (2-7 horror-narrativo)
    - `pace.coverage_pct` (≥70% narration coverage)

    Razón: Gemini holístico ha mostrado scores históricamente inflados (caso pueblo v2: 9.9 con video 7/10 real). Match contra perfil viral measured es independiente y data-driven. **Gate complementario a Gemini ≥9.7 (hard rule #1 — AMBOS requeridos).**

### Editorial UI pacing (post 2026-05-19 — GAP #14 matadero codification)

22. **¿Cada decision UI shot (06/13 equivalents) tiene freeze frame + filter overlay + countdown sync to narration_end + loading bar ≥6% Y separated from countdown?** (NUEVO 2026-05-19 — decision UI editorial canonical pattern)

    Per `horror-choice-format/PAUTA-MASTER.md § decision-UI-pacing` + `INGENIERO-PAUTA-MASTER § 7.X decision-UI-implementation`:

    Pre-render verify per decision shot:
    - [ ] **Freeze frame**: clip animation paused at narration_end timestamp (GSAP `tl.set(..., animationPlayState: paused)` o ffmpeg static last-frame extracted). Motion canónico = MÍNIMO during decision (refs hand poised + filter, NOT full motion).
    - [ ] **Filter overlay**: CSS `filter: sepia(0.4) contrast(1.2) hue-rotate(15deg)` + grain canvas 8% opacity applied to decision-UI clip layer. Empírico ref-03 "filter cinematic/gritty con grain", ref-09 "typewriter UI".
    - [ ] **Countdown sync narration**: `data-start` de countdown digit 1 = `narration_end_marker + 0.3s` (pause beat structural cue). NOT countdown floating loose.
    - [ ] **Loading bar Y position**: `bottom: <Y52-Y54>` para ≥6% Y separation desde countdown Y46. NO Y48 (cramped 2% — causes visual overlap).
    - [ ] **Audio cue durante countdown**: SFX `time_loop_glitch` per digit + ambient duck -6dB.

    Razón: pattern observed empíricamente en 8/8 canonical refs (canonical-scenes/INDEX.md decision setup grid). Sin esto el horror-choice format colapsa decision UI a "elementos puestos sueltos" en lugar de "moment cognitivo estructurado". User flagged matadero iter 2 — codified post-CP5.

    **Y → PASS, N → FAIL** (editorial canonical signature missing for horror-choice format).

    ⚠️ **Hard Rule #19 EXPANSION compliance** — verify SPEC narrative_pacing block tiene:
    - `canonical_validation_status` field present (NO ausente)
    - Status NO es `deprecated_our_prod_only` (debe ser `pending_video_measurement` OR `validated_via_perceptual_test` OR `validated_via_video_measurement`)
    - Si status = `deprecated_our_prod_only` → ESCALATE search canonical alternative ANTES de render.

### AVU principle + sync_contract validation (post 2026-05-19 — GAP #19 + AVU principle Track E Phase 2)

24. **¿Audio-visual coupled elements implemented as AVU (pre-rendered .mp4 with audio bundled) OR declared in explicit sync_contract validated?** (NUEVO 2026-05-19)

    Per `horror-choice-format/PAUTA-MASTER § 19 AVU principle` + `INGENIERO-PAUTA § 7.11 AVU library`:

    Pre-render verify per shot con audio+visual coupled:
    - [ ] Countdown 3-2-1 → AVU pre-rendered .mp4 (NO CSS minimalist ring + separated SFX)
    - [ ] Decision UI moments → AVU pre-rendered .mp4 freeze+filter+countdown+ticks bundled
    - [ ] Hook transitions → AVU pre-rendered .mp4 flash+whoosh bundled
    - [ ] Outro cards → AVU pre-rendered .mp4 card+drone bundled
    - [ ] Per-video variable text/audio (narrator framing, character dialogue) → explicit `sync_contract` declared en SPEC con visual_start_s + audio_start_s + tolerance_s

    Razón: compose-time GSAP timing + CSS race conditions + audio mix wiring = múltiple failure points (matadero iter 3-4 demonstrated). AVU pre-rendered .mp4 = 1 failure point = bullet-proof sync.

    Detection: grep SPEC.yaml `audio_visual_atomic_units` field present per shot con audio+visual coupled. Asset paths exist en `assets/avu/`. Sync contracts validated pre-render via script.

    **Y → PASS, N → 🔴 FAIL ship-blocking** (compose-time fragility risk demonstrated).

25. **¿Countdown visual style = FILM LEADER ACADEMY (crosshair + big central digit ~40-50% frame width)?** (NUEVO 2026-05-19 — GAP #19 correction)

    Per `PAUTA-MASTER § 19.6` direct frame verification 4/4 canonical refs:

    Pre-render verify countdown visual:
    - [ ] Crosshair circle visible (light gray ring + horizontal/vertical center lines)
    - [ ] BIG central digit ~40-50% frame width
    - [ ] Black serif/condensed bold font
    - [ ] NOT CSS minimalist thin ring + small digit (deprecated per GAP #19)
    - [ ] Optional: subtle motion blur + vintage film grain/scratches

    Source canonical: 4/4 refs direct frame verified. Previous codification PAUTA § 18 (CSS minimalist ring) was **INCORRECT** — replaced by FILM LEADER ACADEMY pattern.

    **Y → PASS, N → 🟡 NB style drift from canonical** (acceptable si justified per video tone, e.g. project explicitly opt-out canonical horror-choice style).

---

## Acción según resultado

| Resultado | Acción |
|---|---|
| **24/24 Yes** | ✅ STOP POINT autorizado. Reportar al usuario. Esperar autorización animation AI. |
| **1-3 No** | ⚠️ Completar pieza faltante. Re-invocar gate desde inicio. NO reportar al usuario aún. |
| **4+ No** | ❌ Bootstrap incompleto o flow saltado. Volver al inicio del flow (PASO 1 del `/video-new`). |
| **Score qa-gate < 9.7** | ❌ Iterar fixes NO-ANIMATION-AI (A→B→C — guion/captions/imágenes/wiring/mix). Re-invocar gate. Máx 3 iter → ESCALAR usuario. |
| **Q17-Q20 No (referent-validated)** | ⚠️ Completar el fix correspondiente. Estos son non-blocking si justificación documentada en video-log.md, pero recomendado fixear. |
| **Q21 No (referent-profile matching)** | ⛔ BLOQUEA — falla de hard rule #1 dual gate. Iterar fixes NO-ANIMATION-AI hasta que `ai-video audit-against-referent` retorne exit 0. |
| **Q22 No (decision UI editorial pacing)** | ⛔ BLOQUEA en formato horror-choice — falla canonical signature decision moment. Fix per `PAUTA-MASTER § decision-UI-pacing` + `INGENIERO-PAUTA § 7.X`. NB en otros formatos. |
| **Q24 No (AVU + sync_contract)** | ⛔ BLOQUEA ship — compose-time fragility risk demonstrated (matadero iter 3-4). Build AVU pre-rendered .mp4 OR declare sync_contract explicit en SPEC. |
| **Q25 No (countdown FILM LEADER ACADEMY)** | 🟡 NB style drift — acceptable si justified per video tone, sino fix con AVU template canonical. |
| **Q26 No (background ambient creature/object animated per shot — GAP #23)** | ⛔ BLOQUEA — setting feels DEAD. Each shot SPEC must declare `setting_ambient_creature_or_object` non-empty + engineer Hailuo prompt must request animation. Canonical refs 100% have ≥1 animated background element. ⭐ Fase 0: scripted — `ai-video audit-spec-declarations --checks q26`. |
| **Q27 No (atmospheric motions ≥3 per shot — GAP #26)** | ⛔ BLOQUEA — setting less "alive" than canonical. Each shot SPEC must declare `atmospheric_motions_count ≥3` with list (smoke/vapor/dust/light_flicker/water_drip/insect/etc.). Engineer prompt request 3+ atmospheric elements. ⭐ Fase 0: scripted — `ai-video audit-spec-declarations --checks q27`. |
| **Q28 No (POV traversal continuity — GAP #25)** | 🟡 NB — acceptable some shots `static` PERO must NOT have ALL shots static framing throughout video (viewer teleports between cuts = anti-canonical). Each shot SPEC `pov_traversal_intent` enum. ⭐ Fase 0: el sentinel automated ya existe — `ai-video audit-spec-declarations --checks q28` (all-static check). |

> ⭐ **Fase 0 (2026-06-04) — corrida consolidada de los 4 checks de declaración del SPEC** (Q26+Q27+Q28+status de validación canónica HR#19):
> ```bash
> uv run ai-video audit-spec-declarations --format <format> --spec ../../creative-specs/<id>.yaml
> # Exit 0 → los 4 ✓ · Exit 1 → FAIL con offenders por shot · Exit 2 → can't-measure (Bug #9)
> ```
| **Q29 No (character active gesture per shot — GAP #27)** | 🟡 NB — character on-screen MUST have ONE active gesture per shot (hand reach/breath/blink/turn). If character signature limits (e.g. cleaver helmet), compensate alive signals (light, breath visible, environmental interaction). |
| **Q30 No (lip-sync verification per character speech — GAP #24)** | ⛔ BLOQUEA si `lip_sync_required: true` declared in SPEC. Engineer must verify Hailuo output frame extract OR use Hedra/Sync.so retarget. Auditor S9 sentinel flags character speech segments needing verification. |

---

## Anti-patterns que este gate previene

1. **Parar pre-animation con sub-9.7 esperando que animation AI lo arregle** (caso isla-faro v1)
2. **Repetir mismo pattern en videos consecutivos** (caso cabana → isla-faro)
3. **Setup elements del twist <1s** (caso cabana-tormenta v4 — foto del padre)
4. **Sobre-narrar plot twist** (caso isla-faro — narración explicativa, aburre)
5. **TTS con "..." antes de proper nouns** (causa 11 regens en cabana-tormenta v1)
6. **UI overlap con imagen principal** (caso isla-faro — countdown tapa H1)
7. **Frames negros sin razón narrativa**
8. **Texto sobre rostros de personajes**
9. **Captions overlap entre sí**
10. **Reportar al usuario sin agregar learnings a `<format>-format/video-log.md`** (pierde rotación pattern + lessons cross-video — el doc que SÍ se consulta antes de cada nuevo video)

---

## Cuándo NO invocar este gate

- Tareas que NO son producción de video (analítica, planning, refactor docs)
- Edits triviales pedidos por el usuario ("arreglá ese typo")
- Comandos read-only (ls, cat, grep)

Si dudás → invocar el gate igual. El costo es bajo, el beneficio es alto.

---

## Casos disparadores (por qué existe este gate)

- **cabana-tormenta v3+**: paró en 9.3 antes de Kling con plot twist confuso. El gate detectaría 7+ violaciones.
- **isla-faro v1**: paró en 9.3 antes de Kling. Audit-frames retroactivo detectó 15 issues (countdown tapa imagen, texto sobre rostros, frames negros). El gate los habría detectado antes del stop point.

Sin este gate como skill invocable, las reglas codificadas en sub-docs no penetran al agente productor — caen por debajo del threshold de atención cuando hay muchos docs compitiendo. Este gate es la última defensa.
