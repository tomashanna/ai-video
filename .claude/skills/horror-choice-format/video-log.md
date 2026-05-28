# video-log.md — Registro de producción del formato horror-choice

> Una fila por video producido. Antes de empezar un nuevo brief: leer las últimas 3 filas. **La combinación apariencia × verdad del próximo video DEBE ser diferente a los 3 últimos (matriz expandida § 3.5 desde 2026-05-13).**

**Última actualización**: 2026-05-27 (GAP #10 nomenclature reconciliation)

---

## ⚠️ NOMENCLATURA CANONICAL — reconciliación GAP #10 (2026-05-27)

**Source of truth de pattern numbering = `PAUTA-MASTER.md` (P1/P2/P3/P6/P9 empíricos, derivados de 8 refs canónicos).** El P-numbering histórico de este log (P4 Paz perdida / P6 Trampa simétrica / P10 Inversión total / Meta-cliffhanger) viene del **ex-CREATIVE-BRIEF DEPRECATED** y usa una taxonomía DISTINTA (matriz apariencia×verdad) donde los **mismos números significan otra cosa** (ej: P6 = "Trampa simétrica" acá vs "Hedonismo eterno" en PAUTA-MASTER). NO es mero renaming — son dos taxonomías incompatibles con números colisionando. PAUTA-MASTER ya adjudicó: estos son los únicos observados.

**Taxonomía CANONICAL forward (PAUTA-MASTER — usar SOLO esta para rotación HR#14):**

| Pattern | Significado (empírico, 8 refs) | Refs |
|---------|--------------------------------|------|
| **P1 — Verdad visible** | El obvio peligroso ES peligroso | ref-03/06/08/10/12 |
| **P2 — Supervivencia si manejás bien** | Peligroso sobrevivible con decisiones correctas | ref-03 |
| **P3 — Seguro era trampa** | Bueno aparente era el peligro real | ref-08 |
| **P6 — Hedonismo eterno** | "Bueno" lleva a placer pero perdés el objetivo | ref-13 |
| **P9 — Peligroso te ayuda** | El amenazante es el que te salva | ref-09 |

**P4 / P5 / P10 / Meta-cliffhanger (taxonomía vieja) = NO observados en los 8 refs → DEPRECATED, NO usar forward.**

**Mapeo histórico:** la tabla maestra abajo (#1-#6) usa taxonomía DEPRECATED — se deja **as-is como registro histórico** (esos videos se produjeron bajo la taxonomía vieja; re-taggear sería revisionista). Solo #7 matadero "P6 Hedonismo Eterno" ya está en taxonomía canonical PAUTA-MASTER.

**Rotación V5 (HR#14), sin ambigüedad:** matadero (#7) = **P6 Hedonismo** (canonical) → **V5 NOT P6**. Patterns canonical NO usados por nosotros = **P1, P2, P3, P9** → V5 elige cualquiera de esos. (Las "Reglas de rotación" más abajo con nombres Paz perdida/Trampa/Inversión son DEPRECATED — usar esta tabla.)

---

## Tabla maestra

> Tres rotaciones tracked independientemente: **pattern matriz expandida** (apariencia × verdad), **countdown style** (3 opciones), **loader style** (3 opciones), **lower-third style** (5 opciones — solo si el video usa lower-third). Cada uno debe rotar entre videos para evitar feed predecible.

| # | Fecha | Proyecto | Pattern (matriz § 3.5) | Countdown | Loader | Lower-third | Score | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-05-08 | `elige-companero` V7 | **P10 — Inversión total** (asimétrica + B/M) | (hardcoded) | (hardcoded) | — | 9.5/10 | Final aprobado |
| 2 | 2026-05-09 | `bosque-abandonado` v3 | **P6 — Trampa simétrica** (asimétrica + M/M) | (hardcoded) | (hardcoded) | — | 9.1/10 | Pendiente fixes |
| 3 | 2026-05-09 | `mina-abandonada` v6 | **P4 — Paz perdida** (asimétrica + B/B) | (hardcoded) | (hardcoded) | — | 8.5/10 | Pendiente iteración |
| 4 | 2026-05-11 | `mina-abandonada` v15-final | **P4 — Paz perdida** (asimétrica + B/B) | (hardcoded) | (hardcoded) | — | 9.9/10 | ⭐ Star video — referencia |
| 5 | 2026-05-13 | `cabana-tormenta` v5 | **P6 — Trampa simétrica** (asimétrica + M/M — KRAVEN/MARCO) | (hardcoded) | (hardcoded) | — | "Decente / muy bueno" | Pre-Kling — setup retroactivo H3→H6 |
| 6 | 2026-05-13 | `isla-faro` v1 | **P6 — Trampa simétrica** ⚠️ (repetido vs #5) | (hardcoded) | (hardcoded) | — | 9.3/10 | Paró pre-Kling en 9.3 (anti-pattern) |
| 7 | 2026-05-20 | `matadero-banquete` v1 SHIP | **P6 Hedonismo Eterno** (Cocinera trap eterno cliffhanger — DIFFERENT from #5/#6 P6 Trampa simétrica) | FILM LEADER ACADEMY AVU (canonical correction) | horizontal Y52 | — | **10.0/10** | ✅ SHIPPED 2026-05-20 + 18 gaps codified |

---

## Cross-video uniqueness fields — schema + backfill (BUILD 3 PRE-4.J 2026-05-27)

> Schema enriquecido para soportar `audit-spec-narrative-coherence.py` (cross-video tracking). V5+ SPEC declara `location` + `signature_staging` pre-emit; el validator compara V5 contra estas filas:
> - **location**: exact-match → FAIL (no repetir lugar específico cross-video)
> - **signature_staging**: semantic similarity (paraphrase-multilingual-MiniLM-L12-v2) → ≥0.85 hard-block / 0.75-0.84 flag architect review
> - Verbs de acción + characters: NO check (catálogo válido + repetibles per refinement Tomás 2026-05-27)
>
> Backfill #1-#7 = **estimaciones honest** desde titles + descriptions del log (videos previos no tienen content full re-accesible). Confidence per row indicado. Forward rows (#8+) declaran fields al producirse (HIGH confidence).

| # | Proyecto | location | signature_staging | Confidence |
|---|----------|----------|-------------------|------------|
| 1 | `elige-companero` V7 | legacy uncertain — origin de la serie | legacy uncertain — descripción no captura staging completo | LOW (legacy log, pre-schema) |
| 2 | `bosque-abandonado` v3 | bosque abandonado nocturno | figura amenazante emerge entre árboles muertos del bosque oscuro | LOW-MED (estimate from title) |
| 3 | `mina-abandonada` v6 | mina subterránea abandonada | descenso POV con casco LED encuentra figura al fondo del túnel | LOW-MED (estimate) |
| 4 | `mina-abandonada` v15-final | mina subterránea abandonada (mismo proyecto que #3 — iter, NO cross-video repeat) | descenso POV iterado del túnel con choice H1-H6 | LOW-MED (estimate, iter de #3) |
| 5 | `cabana-tormenta` v5 | cabaña montaña en tormenta nocturna | dos figuras KRAVEN/MARCO buscan refugio en cabaña aislada durante tormenta nocturna | LOW-MED (estimate from title) |
| 6 | `isla-faro` v1 | isla con faro abandonado | aislamiento en isla con faro como punto de elección entre dos figuras presentes | LOW-MED (estimate) |
| 7 | `matadero-banquete` v1 SHIP | matadero refrigerado -30°C turno noche 2-6 AM | matarife casco-cuchillo en patio matadero + cocinera Kate BFP entre carcasas hanging — banquete eterno trampa P6 Hedonismo | HIGH (descripción rica en log) |

**Validator parsing**: el script lee esta tabla (parser regex sobre filas que matchean `| <N> | ...`) y extrae `(num, project, location, signature_staging, confidence)`. LOW-confidence rows participan en comparación pero el validator anota explícitamente low-confidence en el output (false-positive risk + tunear thresholds empíricamente post 5-10 videos forward-declared HIGH).

**Forward rows (#8+):** producir con location + signature_staging declarados al ship, confidence HIGH (escritos al momento, no backfill).

---

## ⚠️ Alertas de rotación (actualizadas 2026-05-20)

### Pattern (matriz expandida § 3.5)

**Patterns usados hasta ahora:**
- P4 (Paz perdida): 2 veces (#3, #4)
- P6 (Trampa simétrica): 3 veces consecutivas (#2, #5, #6) → 🚨 **SOBRE-USADO**
- P10 (Inversión total): 1 vez (#1)
- **NO usados todavía:** P1, P2, P3, P5, P7, P8, P9, Meta-cliffhanger (3.4)

**Próximo video DEBE NO ser P6** (3 veces consecutivas viola la regla "no repetir mismo pattern 2 videos seguidos").

**Recomendaciones por prioridad de variedad:**
1. **Meta-cliffhanger (3.4)** — nunca usado, rompe la 4ª pared, máxima disrupción
2. **P1 — Verdad visible asimétrica** (monstruoso malo + amable bueno, sin twist sorpresa)
3. **P10 — Inversión total** (monstruoso bueno + amable malo, plot twist máximo)
4. **P2 — Paz neutral** (doble amable, ambos buenos) — descansa el feed

**NO recomendado para próximo video:**
- P4 (Paz perdida) — usado hace 2 videos, demasiado pronto
- P6 (Trampa simétrica) — usado 3 veces consecutivas, fatigado

### Patterns con apariencia visual NO probada

Las 3 combinaciones de apariencia (asimétrica / doble monstruosa / doble amable) en la matriz expandida:
- **Asimétrica**: 6/6 videos producidos
- **Doble monstruosa**: 0 videos
- **Doble amable**: 0 videos

Para máxima ruptura de fatiga visual, próximo video podría ser primero con **doble monstruosa** o **doble amable**.

### Element components (countdown, loader, lower-third)

Los 3 videos NO usaron el sistema de element components — fueron hardcoded directamente en el index.html. **A partir del video #4 hay que usar `elements.json`**.

#### 🚨 CHECKLIST ANTES DE PICKEAR COMPONENTES (no se saltea)

##### 1. Consistencia INTRA-video (regla dura)
- [ ] El countdown elegido se usa en TODOS los countdowns del video (H2 + H3 + H4 mismo countdown)
- [ ] El loader elegido se usa en TODOS los loaders del video (H2 + H3 + H4 mismo loader)
- [ ] NUNCA mezclar countdown-X en H2 con countdown-Y en H3

##### 2. Timing — son SECUENCIALES, no simultáneos
```
H2: countdown 3-3.5s → flash → loader 2.5-3s → flash → resultado
H3: countdown 3-3.5s → flash → loader 3.0s → flash → resultado
H4: countdown 3-3.5s → flash → loader 3.0s → flash → resultado
```
- [ ] Loader `data-start` = countdown `data-start` + countdown duración (sin overlap)

##### 3. Compatibility matrix estética

| Countdown × Loader | bar | radial | segments |
|---|---|---|---|
| pulse | ✅ | ✅ | ⚠️ |
| glitch | ⚠️ | ✅ | ✅ |
| slam | ✅ | ⚠️ | ✅ |

- [ ] El combo elegido NO es uno de los ⚠️ a evitar
- [ ] El combo es distinto al del video anterior (ver tabla maestra arriba)

##### 4. Lower-third (opcional)
- [ ] Si el video lo necesita: distinto al del video anterior
- [ ] Estilo coherente con countdown+loader elegidos

#### Combos top-tier validados

| # | Countdown | Loader | Mood |
|---|---|---|---|
| 1 | `countdown-pulse` | `loader-bar` | Cine clásico, suspenso elegante |
| 2 | `countdown-glitch` | `loader-segments` | VHS industrial, paranoia |
| 3 | `countdown-slam` | `loader-segments` | Impact + tracking urgente |
| 4 | `countdown-pulse` | `loader-radial` | Film + circular, atmosférico |
| 5 | `countdown-glitch` | `loader-radial` | VHS + modern, glitch elegante |
| 6 | `countdown-slam` | `loader-bar` | Impact + linear, físico directo |

**Combos a evitar**: pulse+segments, glitch+bar, slam+radial.

#### Variedad ENTRE videos

Ningún componente puede repetirse en 2 videos consecutivos del mismo formato. Pero el COMBO puede repetirse si pasaron 3+ videos en el medio.

Catálogo completo + reglas: `ai-video-production/ELEMENTS-LIBRARY.md`.

---

## Cómo agregar entrada

Después de aprobar Gemini QA (≥9.7) y antes de publicar:

```markdown
| 4 | 2026-MM-DD | <slug> | <escenario corto> | <Malo> / <Bueno> | **<Archetype>** | X.X/10 | <status> | <fecha pub> | `<proyecto>/performance/...` |
```

---

## Reglas de rotación (del PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated])

| Video # | Archetype recomendado |
|---|---|
| 1 (debut serie) | Paz perdida ✅ (hicimos) |
| 2 | Paz perdida o Trampa simétrica (hicimos Paz perdida ✅, debió ser Trampa) |
| 3 | Trampa simétrica (si #2 fue Paz) o Inversión total (hicimos Paz ❌) |
| 4 | Inversión total |
| 5 | Paz perdida (reset al clásico) |
| 6 | Meta-cliffhanger (disrupción) |
| 7+ | Rotar entre los 4, nunca repetir el mismo dos veces seguidas |

**Aprendizaje 2026-05-10**: los 3 primeros videos repitieron Paz perdida — error histórico que debe corregirse desde el video #4.

---

## Anotación de patterns descubiertos por video

Cuando un video sale, anotar acá patterns notables (positivos o negativos) que descubrimos en producción. Diferente de `video-director/PATTERNS-LIBRARY.md` (que es cross-formato y solo agrega validados con N≥3).

### elige-companero V7 (9.5/10)
- ✅ **Patrón validado**: B&W vintage para "el otro camino" (cliffhanger Paz perdida)
- ✅ **Patrón validado**: CTA narrado por la misma voz del narrador (pide "y por qué" — comments más largos)
- ✅ **Patrón validado**: White flash 2-3 frames + hard cut en cada twist

### bosque-abandonado v2 (9.1/10)
- ✅ **Patrón validado**: Captions vía Whisper (0% hand-timing)
- ✅ **Patrón validado**: SFX layer dedicada (34 SFX) — bumped Gemini sound design 9→10
- ✅ **Patrón validado**: Captions safe zone IG bottom:540
- ❌ **Anti-pattern detectado**: H1 con 1 sola imagen para 10s — Gemini lo detectó como "estatismo"
- ❌ **Anti-pattern detectado**: caption-warm class custom inventado (no estaba en docs canonicales)

### mina-abandonada v6 (8.5/10)
- ❌ **Anti-pattern detectado**: usar solo white flash para todos los cortes (no la taxonomía NARRATIVE-LED de 7 cortes)
- ✅ **Patrón validado**: gaps eliminados entre frases del mismo caton (solo último opacity:0)
- ✅ **Patrón validado**: CSS canonical posición bottom:540

### matadero-banquete v1 SHIP — iter 6 Gemini 10.0/10 — 2026-05-20
- **Pattern**: P6 Hedonismo Eterno (Cocinera path TRAP eterno cliffhanger)
- **Score Gemini iter 5 → iter 6**: 9.2 → **10.0/10** (post engineer iter 6 D1+D2 fix lip-sync cocinera + subtítulos duplicados)
- **Setting**: matadero refrigerado -30°C turno noche 2-6 AM
- **Architect domain residuals accepted** (cp5_architect_domain_residuals_accepted_2026_05_19):
  - F13 cuts/min 17.43 ACCEPTED (ref-13 mini-cuts flooding signature SPEC L820)
  - F14 coverage 75.74% ACCEPTED (P6 archetype structural pauses load-bearing)
  - F15 Gemini Dim12 Y58 REJECTED (false-positive — Hard Rule #4 Y62 empirical wins)
- ✅ **Patrón validado**: AVU principle universal (audio+visual atomic units pre-rendered .mp4) — resuelve compose-time GSAP+CSS+audio race conditions (iter 3-4 demonstrated)
- ✅ **Patrón validado**: Countdown FILM LEADER ACADEMY (crosshair + big central digit) — direct frame verification 4/4 canonical refs (GAP #19 correction)
- ✅ **Patrón validado**: Hook sub-beat ordering canonical (name labels → caption setting → narrator framing → push-in → countdown LAST → character dialogue SEPARATE shot_02 NOT in hook)
- ✅ **Patrón validado**: Per-speaker atempo multipliers (narrator ×1.15, cocinera ×1.21-1.24, matarife ×1.28 ceiling) — Path E pace correction post user "muy lento" feedback
- ✅ **Patrón validado**: Voice ID Kate BFP cocinera (qWWAqFomnJ99VwQLREfT) — user Rule D PRECEDENCE override architect-pick Valeria
- ❌ **Anti-pattern detectado**: dialogue cocinera ON-screen mid-hook + countdown overlap (matadero iter 1) → editorial collapse, hook should end with countdown FILM LEADER LAST
- ❌ **Anti-pattern detectado**: matarife voice effects chain heavy sin M7.7 intelligibility check (LPF 2000Hz + aecho out_gain 0.3 = unintelligible despite high mean_volume) — codified ARCHITECT-MASTER-FLOW § 6.9
- ❌ **Anti-pattern detectado**: architect label-driven preempt sin perceptual listen (Kate BFP rejected based on label "Bright Friendly Positive") — codified ARCHITECT-MASTER-FLOW § 6.10
- ❌ **Anti-pattern detectado**: docs trust without direct verification (architect/auditor sampled canonical-scenes every 5s → wrong countdown analysis) — codified GAP #20 canonical-scenes MAX DETAIL methodology

#### Post-SHIP analysis 2026-05-20 — 6 NEW gaps identified (#23-#28)

User concern post v1 SHIP: "los videos canonical se ven y escuchen tan bien" → auditor deep frame analysis 8 canonical refs identified 6 systemic gaps matadero vs canonical:

- ❌ **Anti-pattern detectado GAP #23**: settings static sin background creature/object animated — matadero refrigerator carcasas hanging static + no rats moving + no flame flickering vs canonical 100% have ≥1 background animated element (ref-08 shark + ref-13 light beam + ref-10 flame). Codified PAUTA § 20.
- ❌ **Anti-pattern detectado GAP #24**: lip-sync coverage incomplete — cocinera speech ON-screen iter 1 had audio without lip-sync motion sync (user D1 catch iter 5 forced fix). Universal canonical 8/8: lip-sync OBLIGATORIO per character speech ON-screen. Codified PAUTA § 21.2.
- ❌ **Anti-pattern detectado GAP #25**: POV traversal teleports — multiple consecutive shots viewer position changes dramatically with no implied physical traversal vs canonical refs SHOW viewer walking/turning/descending. Codified PAUTA § 22.
- ❌ **Anti-pattern detectado GAP #26**: atmospheric secondary motions <3 per shot — matadero shots had minimal smoke/vapor/dust/flicker vs canonical 100% have ≥3 atmospheric motions per shot. Codified PAUTA § 20.1 + § 20.3 catalog.
- ❌ **Anti-pattern detectado GAP #27**: character active gesture missing per shot — matarife shots static (cleaver-head no expression + apron static + boots static = stage prop feel) vs canonical 8/8 include ONE active gesture per character per shot. Codified PAUTA § 21.3 + alive signals compensation for signature-limited characters.
- ❌ **Anti-pattern detectado GAP #28**: ambient sound design canonical fingerprint missing per setting — matadero ambient layer not matching canonical refs setting-specific fingerprint depth. Codified Track C forward.

#### Gaps codified during full production (#11-#28 = 18 gaps total)
- Track C Phase 1 (#11-#17): decision UI editorial pacing + canonical_validation_status compliance + label preempt + volume meter intelligibility
- Track E Phase 2 (#18-#20): hook sub-beat ordering + countdown FILM LEADER correction + canonical-scenes MAX DETAIL methodology
- Track A SPEC v9 (#23-#28): setting/character/POV alive canonical patterns

#### Final ship status: ✅ SHIPPED 2026-05-20

- iter 6 Gemini 10.0/10 final score
- 18 gaps codified across 5 NIVEL cascade (matadero-specific → project-template → format-canonical → universal QA → referent-empirical)
- AVU library founded (countdown-3-2-1-film-leader-with-ticks.mp4 first template)
- SPEC schema v6→v7→v8→v9 evolution post-matadero

#### Forward rotation post-matadero
- **NEXT video should NOT use P6 again**. Per PAUTA-MASTER § 17 rotación rules:
  - Suggested patterns: **P3 Trampa simétrica** (no usado nuestro), **P5 Empleo trampa** (no usado nuestro), **P9 Engaño identidad** (no usado nuestro)
- **Setting suggestion forward**: cinema abandonado (post matadero refrigerated, contrast cool→warm light dynamic + POV traversal canonical opportunities)
- **Quality fingerprint forward**: heredando 18 gaps codified across PAUTA + INGENIERO-PAUTA + SPEC TEMPLATE + pre-render-gate + canonical-scenes + ARCHITECT-MASTER-FLOW + AUDITOR-PROTOCOL
- **Phase 1 priority remaining**:
  - Build full AVU library 3 templates remaining (decision-freeze + hook-transition + outro-card)
  - Run extract-canonical-max-detail.py 8 source videos regenerate canonical-scenes MAX DETAIL
  - Build measure-canonical-decision-ui-pacing.py + audio cue levels script
  - Build audit-frames-granular.py S10 sentinel (background motion + traversal + atmospheric + character gesture detection)

---

## Próximas iteraciones planeadas

| Acción | Cuándo | Status |
|---|---|---|
| Publicar elige-companero V7 a IG (cuenta nueva) | Tras decidir handle | ⏸️ Pending handle |
| Bosque-abandonado v2 → fixes para 9.5 (variantes H1 + heartbeat + viñeta H6) | Próxima sesión | ⏸️ Pending |
| Mina-abandonada v6 → aplicar NARRATIVE-LED-EDITING completo | Próxima sesión | ⏸️ Pending |
| **Video #4 con archetype Trampa simétrica** | Cuando los 3 anteriores estén publicados | ⏸️ Pending |

---

## Cross-references

- Sistema de archetypes: `PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated]` § 3
- Sistema de patterns universales: `video-director/PATTERNS-LIBRARY.md`
- Métricas de cada video: `<proyecto>/performance/YYYY-MM-DD-<slug>.md`
- Reglas perennes: `PATTERNS.md`
- Script writing: `SCRIPT-WRITING-GUIDE.md`

---

## Última actualización

**2026-05-20 (PM late) — Track A v3 R1 countdown_digit_duration_s RESOLUTION**: 3 sources of truth conflict resolved per user Rule D PRECEDENCE. User verdict iter 7-8: "Me gusta que los segundos en vd sean segundos, 1, 2, 3" → `countdown_digit_duration_s = 1.0s` canonical. Engineer empirical 0.5 (n=1 LOW confidence) REFUTED. Architect Track A v2 compromise 0.7 REFUTED. Status: `validated_via_user_perceptual_2026_05_20`. Forward revisit trigger: Phase 1 forward measure-canonical-decision-ui-pacing.py n≥5 sample increase — if median significantly differs from 1.0s, escalate to user perceptual re-confirm. Updated PAUTA § 18 + INGENIERO § 7.10 + SPEC TEMPLATE v9.1 + matadero in-SPEC. countdown_digit_duration_s user-validated 1.0s (NOT engineer 0.5 n=1).

**2026-05-20 (PM)** — Track A v2 EMPIRICAL CORRECTIONS post engineer Track B Phase 1: `measure-canonical-decision-ui-pacing.py` COMPLETE 8/8 refs measured. Source `referent-analysis/empirical-decision-ui-pacing/aggregate-canonical-bands.json`. **3 REFUTATIONS Phase 0 inferred values**: (1) countdown_pause_beat_s 0.3 → 0.9 median canonical (n=14), (2) ambient_duck_db -6 → +0.22 (NO duck canonical, n=20), (3) freeze_frame_applied default true → 14% MINORITY OPTIONAL (n=22 windows). Confirmations: digit_duration_s 0.7 ✅ [SUPERSEDED by Track A v3 R1 user-validated 1.0s], loading_bar_y 52 ✅, countdown_y 46 ✅, countdown_visual_style film_leader_academy ✅. All canonical_validation_status flags flipped pending_video_measurement → validated_via_video_measurement across PAUTA § 18.9 + INGENIERO § 7.10.8 + REFERENT-ANALYSIS § 4.6 + matadero cp5_iter3 SPEC + CREATIVE-SPEC-TEMPLATE v9.1 defaults. **Matadero v1 SHIPPED leave-as-is** (architect-domain creative-residual per user Rule D PRECEDENCE) — corrections apply FORWARD next videos.

**2026-05-20 (AM)** — matadero-banquete v1 SHIPPED 10.0/10 + 18 gaps codified (#11-#28). Forward rotation: NEXT video NOT P6 (used matadero) — suggest P3/P5/P9 not yet used. Phase 1 priority remaining: AVU library 3 templates + extract-canonical-max-detail.py + audit-frames-granular.py S10 sentinel.

2026-05-10 (prior). Backfill de los 3 videos existentes (elige V7, bosque v2, mina v6). Alerta de rotación: necesitás romper Paz perdida en el próximo video.
