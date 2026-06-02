# TEAM-PROTOCOL.md — Multi-agent collaboration protocol (NIVEL 1 universal)

> **Scope**: Meta-protocol genérico para cualquier proyecto multi-capa con 3 roles independientes (architect / engineer / auditor). NO video-specific — aplica a cualquier dominio donde la separación de juicio + filesystem handoffs + layered architecture sean apropiados.
>
> **Status**: v1 draft 2026-05-18 (Phase 0). Validation pendiente con 2do video horror-choice + 1er formato distinto.
>
> **Distinción importante**: este doc es **NIVEL 1** (universal multi-agent). Para domain-specific:
> - NIVEL 2 (video production universal): `ai-video-production/` + templates PAUTA/INGENIERO-PAUTA
> - NIVEL 3 (format-specific): `<formato>-format/PAUTA-MASTER.md` + `INGENIERO-PAUTA.md`
> - NIVEL 4 (per-instance): `creative-specs/<id>.yaml`

---

## 1. Las 3 identidades + responsabilidades

### 🏛️ ARCHITECT

**Owns**: diseño creative + intent + decisiones de qué construir + amend SPEC.

**Authority**: creative-domain. La autoridad canónica del **qué** y **por qué**.

**Inputs**: user briefing + canonical references (NIVEL 3 PAUTA-MASTER) + lessons learned previas.

**Outputs**: SPEC (NIVEL 4) + as_built annotations + creative verdicts Q1-QN.

**Reads directly**: NIVEL 1 + NIVEL 2 + NIVEL 3 PAUTA-MASTER (creative authority). NO necesita leer NIVEL 3 INGENIERO-PAUTA (technical bands).

**NEVER does**:
- Especifica tooling/scripts/commands (eso es engineer)
- Audita deliverables del engineer (eso es auditor)
- Override autoridad canónica sin documentar rationale
- Acepta engineer Path B bypass sin escalation formal

### 🛠️ ENGINEER

**Owns**: ejecución técnica + transformar SPEC en artifacts + self-audit + emit handoffs.

**Authority**: technical-domain (within bounds of NIVEL 2 + NIVEL 3 INGENIERO-PAUTA). La autoridad del **cómo** construir.

**Inputs**: SPEC (NIVEL 4) + NIVEL 1 + NIVEL 2 + NIVEL 3 INGENIERO-PAUTA.

**Outputs**: artifacts (assets, code, files) + PRE/POST handoff packages + measurements.

**Reads directly**: NIVEL 1 + NIVEL 2 + NIVEL 3 INGENIERO-PAUTA (technical authority). May reference NIVEL 3 PAUTA-MASTER for context but NOT as authoritative source for technical decisions.

**NEVER does**:
- Edita SPEC (eso es architect)
- Decide creative-domain (e.g. amend target threshold post-failure — eso requiere architect Path B-extension)
- Skip SPEC trigger gates en parallel processing
- Authora architect-domain content en handoff (cita pero no inventa)

### 🔍 AUDITOR

**Owns**: verificación independiente contra autoridad canónica directa + emit verdicts + flag canonical-violations.

**Authority**: verification-domain. La autoridad de **¿cumple lo prometido?**

**Inputs**: handoff package del engineer + autoridad canónica directa (NIVEL 1 + NIVEL 2 + NIVEL 3 ambas pautas + NIVEL 4 SPEC).

**Outputs**: tabla findings + verdict states (🟢/🟡/🔴/⛔) + concurrence con architect verdicts.

**Reads directly TODAS las autoridades — sin delegar**: NIVEL 1 + NIVEL 2 + NIVEL 3 PAUTA-MASTER + NIVEL 3 INGENIERO-PAUTA + NIVEL 4 SPEC. Esto es no-negociable (anti-pattern: delegar verificación al self-audit del architect/engineer).

**NEVER does**:
- Edita SPEC ni handoffs (solo emite findings)
- Decide creative (eso es architect)
- Decide engineering (eso es engineer)
- Comparte contexto con architect o engineer (independencia de juicio = structural)
- Maquilla findings para acelerar GO

---

## 2. Comunicación entre roles — filesystem-based

### Principios

1. **Toda comunicación inter-rol** pasa por **filesystem** (handoff packages .md o .yaml), **NO** chat directo entre roles.
2. **Cada rol** tiene **terminal/contexto separado** (3-terminal model físico actual, 1-terminal-3-contexts model en Phase 5 automation).
3. **El usuario** es el **bridge entre terminales** en model manual. En Phase 5 automation, el bridge es el **orchestrator**.
4. **Cada handoff** es **self-contained**: el receiver lo lee SIN tener el contexto del sender.

### Tipos de handoff

| Tipo | Sender → Receiver | Trigger | Format |
|------|---------------------|---------|--------|
| **SPEC** | Architect → Engineer + Auditor | Architect completes design | `creative-specs/<id>.yaml` |
| **SPEC annotation** | Architect → all (via filesystem) | Post-CP decision | YAML block in-SPEC (`as_built_<topic>_<date>`) |
| **PRE-handoff** | Engineer → Architect + Auditor | Pre-execution CP[N] | `<proyecto>/CP[N]-PRE-handoff.md` (or `-vN.md` re-handoff cycle) |
| **POST-handoff** | Engineer → Architect + Auditor | Post-execution CP[N] | `<proyecto>/CP[N]-POST-AUDIT-handoff.md` |
| **Verdict** | Architect/Auditor → other roles | Post-gate evaluation | Markdown tabla findings (current format) — JSON schema (Phase 4) |

### Verdict states universales

Todos los roles emit verdicts usando los mismos 4 estados:

| Verdict | Significado | Acción siguiente |
|---------|--------------|-------------------|
| 🟢 **GO incondicional** | Todos los items PASS, 0 FAILs | Ejecutar plan exactamente |
| 🟡 **GO condicional** | 0 FAILs creativos, ≥1 fix técnico bloqueante accionable | Aplicar fixes → re-handoff vN+1 → re-audit focused (solo el diff) |
| 🔴 **NO-GO** | ≥1 FAIL bloqueante (canonical violation o deliverable miss) | Regen / re-plan → re-handoff completo → re-audit completo |
| ⛔ **ESCALATE** | Conflict autoridad o 3+ iter sub-target o decisión beyond role scope | User decide override / re-spec / pivot |

### Reglas de output format

1. **Tabla findings**: `| # | Item | Verdict | Razón | Authority | Fix |` — no prosa libre
2. **Authority quote**: `<doc> § <X> L###` o `SPEC L###` — NUNCA "según la pauta" sin línea
3. **Fix sugerido**: accionable, NO "considerar revisar"
4. **Copy-paste ready bloque**: cada verdict incluye un bloque listo para que el bridge (user/orchestrator) pase al receiver sin re-formatear

---

## 3. Coordinación per proyecto (CP flow)

Pointer a NIVEL 2 + NIVEL 3 docs para detail per CP.

**Universal patterns per CP** (que aplican cualquier dominio):
1. **PRE-handoff** (engineer → arch+audit)
2. **Parallel gate** (arch + audit en terminales separados, paralelos)
3. **Execute** (engineer)
4. **POST-handoff** (engineer → arch+audit)
5. **Parallel POST-gate** (arch + audit)
6. **CP closure** (as_built annotation in-SPEC con concurrence flags)

**Domain-specific detail** (qué hace cada CP) vive en:
- NIVEL 2 `ai-video-production/` (universal video CPs)
- NIVEL 3 `<formato>-format/per-CP/` (format-specific CPs)
- Mi `master-flow-v2/per-CP/` (per-CP video horror-choice — Phase 1 refactor lo moverá a NIVEL 2/3)

---

## 4. Coordinación per capa del sistema

### Las 4 capas

```
NIVEL 1: MULTI-AGENT UNIVERSAL (este doc TEAM-PROTOCOL)
        Owner: system architect (user + designated person)
        Cambia: rare (cuando descubrimos pattern multi-agent nuevo)

NIVEL 2: DOMAIN-UNIVERSAL (e.g. video production universal)
        Owner: domain architect (puede ser mismo que NIVEL 1)
        Cambia: ocasional (cuando descubrimos pattern domain pero NO format-specific)

NIVEL 3: FORMAT-SPECIFIC (e.g. horror-choice, tutorial, B2B)
        Owner: format curator (architect del formato)
        Cambia: cada N videos cuando measurements validan changes

NIVEL 4: PER-INSTANCE (SPEC + per-video assets)
        Owner: video architect (architect rol del per-video)
        Cambia: per video
```

### Quién owns cada capa

| Capa | Architect role | Engineer role | Auditor role |
|------|----------------|----------------|---------------|
| NIVEL 1 | Owns: meta-rules multi-agent + comunicación | Uses: comunicación rules para handoffs | Uses: AUDITOR-PROTOCOL para verify |
| NIVEL 2 | Owns: pipeline universal + templates | Uses: tools + scripts + canonical Q-gates | Uses: AUDITOR-PROTOCOL checklist per CP universal |
| NIVEL 3 | Owns: PAUTA-MASTER (creative) | Uses: INGENIERO-PAUTA (technical bands) | Uses: AMBAS pautas (lectura directa) |
| NIVEL 4 | Owns: SPEC creation/amendment | Uses: SPEC para execute | Uses: SPEC + autoridades upstream para audit |

### Cómo se promueve cambio inter-capa (learning propagation)

**Pattern**: descubrimiento en NIVEL bajo → evaluation si aplica higher NIVEL → promoción.

**Ejemplo concreto**: `Pro ceiling sistemático para numerical anatomical counts` descubierto en NIVEL 4 (matadero-banquete CP3 shot_20 + cocinera anchor 4 iterations).

Decisión de promoción:
- ¿Aplica solo a este video? → stay NIVEL 4 as as_built annotation
- ¿Aplica a horror-choice format (cualquier video del formato)? → promote a NIVEL 3 INGENIERO-PAUTA-MASTER amendment
- ¿Aplica a cualquier video con Pro generation? → promote a NIVEL 2 (`ai-video-production/` o `MODEL-BENCHMARK`)
- ¿Aplica a cualquier multi-agent system? → promote a NIVEL 1 (esto solo si aprende algo del sistema mismo, no domain)

**Pro ceiling** es claramente NIVEL 2 (universal video con Pro models). Promoción path: as_built annotation NIVEL 4 → INGENIERO-PAUTA amendment NIVEL 3 → MODEL-BENCHMARK update NIVEL 2.

### Workflow de promoción

| Step | Quién | Output |
|------|-------|--------|
| 1. Discovery | Engineer durante execute o auditor durante audit | Documentar in handoff package |
| 2. Categorize layer | Architect (con auditor concurrence) | Decisión: ¿NIVEL 4, 3, 2, o 1? |
| 3. Draft amendment | Architect (NIVEL 3+) o auditor (NIVEL 2 technical) | Propose change to canonical doc |
| 4. Cross-role concurrence | Architect + Auditor + Engineer (si applicable) | Concur or amend |
| 5. Commit amendment | Owner of target layer | Update canonical doc + version bump si applies |
| 6. Propagate downstream | Architect + Engineer | Update derived docs/code that reference |

**Critical**: Step 2 (categorize layer) es decisión deliberativa. **Default conservative**: stay NIVEL 4 hasta validation con 2do video. Promote NIVEL 3 cuando aparece en 2+ videos del formato. Promote NIVEL 2 cuando aparece en 2+ formatos.

---

## 5. Learning capture + propagation

### Bug arquitectural reconocido

Los lessons learned aparecen frecuentemente (5-9 per CP). Pero las **autoridades canónicas (PAUTA-MASTER, INGENIERO-PAUTA, hard rules CLAUDE.md) NO se actualizan automatically**. Hay gap de "captura → propagation" — lo escribimos en chat/handoffs pero no se propaga.

### Workflow de learning capture

**Per CP closure**:
1. Engineer + Auditor identify lessons en POST-handoff
2. Architect categoriza per layer (NIVEL 4 vs 3 vs 2 vs 1)
3. Architect drafts amendment (si NIVEL 3+) o flag para review batch (acumular)

**Per video closure**:
1. Retro multi-role: review all lessons del video
2. Decide qué se promote inmediato vs qué espera 2do video validation
3. Commit amendments

**Per N videos del formato** (N = 2-3):
1. Validation: ¿lessons recurrentes son pattern real o accident del 1er video?
2. Promote validated patterns a NIVEL 3 INGENIERO-PAUTA / PAUTA-MASTER
3. Update video-log + canonical refs

**Per dominio cross-format** (after 1er video de FORMATO NUEVO):
1. ¿Patterns NIVEL 3 son specific al formato o universal video?
2. Promote universal patterns to NIVEL 2

---

## 6. Conflict resolution — autoridad hierarchy

### Cuando 2 autoridades chocan

**Caso real matadero CP2**:
- CLAUDE.md hard rule #10: "Atempo 2x sobre TTS lento"
- INGENIERO-PAUTA-MASTER § 1.7 measured: 2.3x para hit median 165 WPM canónico
- Conflict: ¿2.0x o 2.3x?

**Resolution per hard rule #19**: "INGENIERO-PAUTA-MASTER es autoridad técnica empírica". Wins sobre default genérico.

### Hierarchy genérica

```
[Más específica/empírica] > [Más genérica/default]

NIVEL 4 SPEC explicit > NIVEL 3 INGENIERO-PAUTA empirical > NIVEL 3 PAUTA-MASTER creative > NIVEL 2 universal templates > NIVEL 1 multi-agent rules > NIVEL 2 default hard rules CLAUDE.md
```

**Excepción**: hard rules safety/security NIVEL 1 NUNCA son overridden by domain (e.g. "no auto-publish without user approval" — eso es structural).

### Workflow conflict resolution

1. Auditor detecta conflict during audit
2. Cita ambas autoridades con line numbers
3. Aplica hierarchy → emite verdict siguiendo autoridad ganadora
4. Flag forward: ¿la autoridad perdedora debe actualizarse para no causar conflict futuro?
5. Si sí → flag amendment NIVEL apropiado

**Ejemplo matadero atempo**:
- Auditor concur con INGENIERO-PAUTA 2.3x
- Flag forward: "Hard rule #10 CLAUDE.md should be updated post-CP5 si 2.3x funciona en render final"
- Pending: architect-domain edit CLAUDE.md hard rule #10 → "Atempo per INGENIERO-PAUTA-MASTER § 1.7 measured per formato"

---

## 7. Sub-loops common (pointer a master-flow-v2 detail)

Patterns que recurren entre CPs y proyectos:

| Pattern | Cuándo aparece | Detail |
|---------|----------------|--------|
| **Path A/B/C/B-extension** | Deliverable falla SPEC target | `master-flow-v2/AUDITOR-MASTER-FLOW.md` § 5.1 |
| **Test-first** | High-risk single antes cascade | `master-flow-v2/per-CP/CP3-shots-flow.md` § 4.1 |
| **Re-handoff cycle** | v1 → v2 → v3 con fixes applied | `master-flow-v2/AUDITOR-MASTER-FLOW.md` § 5.3 |
| **SPEC trigger gates** | Gate bloqueante en SPEC | `master-flow-v2/per-CP/CP3-shots-flow.md` § 4.3 |
| **Procedural violations NB** | Engineer salta gate inadvertidamente | `master-flow-v2/AUDITOR-MASTER-FLOW.md` § 5.5 |

**Principio**: sub-loops viven en el doc del CP donde más aparecen, pero son **patterns genéricos** que aplicarán a cualquier proyecto.

---

## 8. Automation path — 3-terminal manual → 1-terminal orchestrator

### Phase actual (discovery mode)

- 3 terminales físicos separados (architect / engineer / auditor)
- User = bridge entre terminales
- Filesystem = state machine (handoffs + SPEC annotations)
- Manual judgment en cada decision point

### Phase 5 target (production mode)

- 1 terminal con orchestrator agent
- 3 LLM sub-contexts (architect/engineer/auditor), cada uno con **fresh context per role per CP** (preserves judgment independence sin separación física)
- Filesystem = state machine (sin cambio)
- **Automated decision points** based on canonical criteria + measurements
- **Escalate to user** solo cuando: conflict autoridad insolucionable + 3+ iter sub-target + cost guardrail breach + ambiguity beyond role scope

### Transformación operacional

| Manual (Phase 0-3) | Automated (Phase 5) |
|---------------------|---------------------|
| User reads architect handoff + pastes to engineer terminal | Orchestrator reads filesystem + dispatches engineer agent con SPEC context loaded |
| User pickea sample voice option de 3 | Architect agent picks per criteria + scoring (LLM judgment within bounded scoring) |
| User decides Path A iter 2 vs Path C escalate | Decision tree explícito: iter count + cost vs Path C cost vs feature load-bearing classification |
| User concur with verdict en chat | Auditor agent emits structured verdict en filesystem + orchestrator state update |

### Pre-requisitos para Phase 5

1. Decision criteria 100% explícitos (NO judgment calls vagos)
2. Quality gates 100% measurable (no human "feels right")
3. Sub-pattern decision trees completos
4. Escalation criteria explícitos (cuándo user override)
5. Cost guardrails per CP (budget allocations)
6. JSON schemas para handoffs + verdicts + annotations
7. Tooling APIs definidos (engineer scripts con clear input/output contracts)

---

## 9. Anti-patterns team-level

### 9.1 Contamination contextual entre roles

**Anti-pattern**: architect lee engineer's reasoning previo to emit verdict → loses creative independence.

**Fix**: cada handoff es self-contained. Receiver lee SIN context del sender.

### 9.2 Override unilateral sin canonical rationale

**Anti-pattern**: architect approves Path B engineer-bypass sin documentar canonical authority.

**Fix**: cada amendment requiere `architect_concurrence: true + rationale: "<authority citation>"`.

### 9.3 Learning loss (lessons NO promoted)

**Anti-pattern**: lessons identificadas en POST-handoff quedan en chat sin propagación a canonical layers.

**Fix**: per-CP closure obligatorio incluye `lessons_to_promote: [list]` con categorize layer.

### 9.4 Delegate verification al self-audit

**Anti-pattern**: auditor confía en "engineer reports X" sin lectura directa.

**Fix**: AUDITOR-PROTOCOL § 1 — lectura obligatoria fuentes primarias directas.

### 9.5 Engineer authoring architect-domain content

**Anti-pattern**: engineer inventa SPEC amendment cuando hits ceiling.

**Fix**: engineer flag al architect via handoff. Architect emits Path B-extension con canonical rationale.

### 9.6 Bridge bottleneck (user attention dependency)

**Anti-pattern**: cada decision point requiere user attention → sistema NO escala.

**Fix Phase 5**: automated decisions based on criteria. User escalation reserved for criteria-undefined edge cases.

### 9.7 Mixing capas en autoridad

**Anti-pattern**: hard rule NIVEL 1 contradicts NIVEL 3 INGENIERO-PAUTA empirical (e.g. atempo 2x vs 2.3x).

**Fix**: hierarchy resolution explícita + flag amendment downstream para evitar recurrencia.

### 9.8 Library defaults validated against our productions (NOT canonical refs)

**Anti-pattern**: library entries (voice IDs, atempo defaults, model presets, SFX, LUTs) etiquetados "default_canonical" pero `validated_in` field cite nuestras producciones (V7, bosque, mina, etc.). Silently drift de canonical compliance. Engineer reads "default_canonical" tag y assumes canonical-validated, pero realmente es our-prod-validated.

**Caso disparador 2026-05-18**: matadero CP2 voice ID `Tj9l48J9AJbry5yCP5eW` labeled "default_canonical" pero validated_in solo elige-companero V7 + bosque-abandonado v1. User listen test refutó canonical perception. WPM measurement in band PERO voice character (susurro grave) NO matches canonical viral narrators.

**Fix** (CLAUDE.md hard rule #19 expansion 2026-05-18):
- Cada default en library/scripts/elements.json DEBE tener field `canonical_validation_status: {validated|pending|deprecated_our_prod_only}`
- Cada validated entry DEBE cite `validated_against_canonical_refs: [<ref-XX list>]` + `validated_at: <date>`
- Auditor D28 cross-validate canonical compliance per CP audit (renombrado de D24 2026-05-18 post conflict con D24 architect "Camera per shot specified" en creative-director/SKILL.md)
- Status `deprecated_our_prod_only` = NO use, search canonical-validated alternative
- Status `pending` = audit obligatorio antes de production canonical use

### 9.9 ⭐ Estimating instead of measuring (principle: NEVER ESTIMATE, ALWAYS MEASURE)

**Anti-pattern**: cualquier rol (architect / engineer / auditor) ESTIMA un canonical parameter en lugar de MEDIRLO. Ejemplos observados:
- Engineer estimates "voice character probably canonical" sin sample test
- Architect estimates "Pro ceiling defendible" basado en intuition
- Auditor estimates "spec compliance" sin measure_F1.py methodology run
- Anyone uses "median canonical WPM" assumed from documentation when measurement could verify directly

**Caso disparador 2026-05-18 user feedback explícito**: "Esto de la voz nunca más puede pasar. Se debe calcular velocidad voz de todos los personajes y narrador de las pautas → buscar las voces que hacen match con eso, luego si se validan se usan esas voces. NUNCA estimar, SIEMPRE calcular."

**Fix — workflow MEASURE → MATCH → VALIDATE → USE** (CLAUDE.md hard rule #19 expansion 2026-05-18):

```
PASO 1 — MEASURE (canonical ground truth)
  Run extractor script over N canonical refs → output bands per dimension
  Example: measure-canonical-per-speaker.py → per_speaker_canonical_bands.json
  
PASO 2 — MATCH (candidate search)
  Search candidates (voice IDs, models, presets) vs measured bands
  Quantitative comparison, NO qualitative guess
  
PASO 3 — VALIDATE (dual gate)
  Programmatic: candidate output measured fits canonical bands
  Perceptual: user listen test / visual review acoustic ground truth
  BOTH must pass
  
PASO 4 — USE (commit)
  library entry: canonical_validation_status: validated
  validated_against_canonical_refs: [refs measured]
  measured_canonical_bands_match: {dimension: value}
```

**Aplicabilidad universal** — applies a:
- Voice IDs (workflow measure-canonical-per-speaker.py Phase 1 priority)
- Atempo defaults (measured per voice character vs canonical WPM band)
- Image models (canonical character fidelity measured per model)
- Animation models (canonical motion smoothness measured)
- LUTs (color analysis canonical frames)
- SFX library (canonical SFX type extraction)
- Music BPM (extracted per ref, band derived)
- UI elements (canonical UI safe zones measured F1)

**Forward implication**: NO new format / video / asset should be authored without measure-then-match-then-validate cycle complete. Phase 1 priority script bump.

### 9.9.1 Responsibility matrix — canonical compliance ownership

Para que el principle "NEVER ESTIMATE, ALWAYS MEASURE" NUNCA falle (caso disparador matadero voice ID 2026-05-18), ownership codified así:

| Trigger | Owner | Acción |
|---------|-------|--------|
| **New format / video starts** | 🏛️ Architect | D28 check during SPEC creation: cada default citado en SPEC verify `canonical_validation_status: validated`. Si deprecated o pending → escalate engineer para search canonical alternative ANTES de commit SPEC |
| **Per-CP audit** | 🔍 Auditor | D28 cross-validate canonical compliance (BLOCKING per AUDITOR-PROTOCOL § 3 D28). Si engineer cite default sin canonical_validation_status → 🔴 FAIL |
| **New library entry needed** (engineer detects gap during execute) | 🛠️ Engineer | Execute MEASURE → MATCH → VALIDATE → USE workflow. Commit library entry con canonical_validation_status: validated + bands match documented. NO commit con status pending sin auditor concurrence |
| **⭐ Recurring canonical refresh audit** (cada 5 videos producidos OR cada 60 days, lo que ocurra primero) | 🔍 Auditor (BLOCKING audit) | Run measure-canonical-* scripts vs current library entries. Flag drift (e.g. nuevos canonical refs added al catalog cambiaron bands). Emit refresh batch update list to engineer. Engineer batch update library entries |
| **Phase 1 initial library audit** (one-time, post-CP5 matadero closure) | 🛠️ Engineer + 🔍 Auditor co-led | Audit cada library entry + script default + elements.json para canonical_validation_status field. Mark TODOS los defaults explícitamente. Engineer implements field updates, auditor verify. |

**Accountability final**: 🔍 **AUDITOR** is the BLOCKING enforcement per CP. Architect owns prevention at SPEC creation. Engineer owns implementation. Es accountability shared, pero el AUDITOR es el **final gate** que bloquea producción si compliance fails.

**Recurring refresh trigger automation** (Phase 5 target): cron-style task triggered cada 60 days OR post-5-videos-produced → auditor agent dispatched para measurement refresh batch. Hoy es manual auditor action (TODO Phase 1 calendar).

---

## 10. Engineer STOP point template — inventory table OBLIGATORIA (added 2026-05-19 post gap #13)

> **Trigger**: cada vez que engineer declara CP[N] complete + emite handoff hacia auditor/architect/user.
>
> **Razón**: caso disparador matadero CP5 STOP point 2026-05-19. Engineer declared CP4/CP5 complete con assets parcialmente generados (29 Hailuo clips ✅ + master.mp3 narration-only ✅) PERO SFX/music/ambient/UI elements ZERO generated (vs SPEC 10/3/2/3+2+2 required). Engineer's `coverage_pct 69.93% structural` label was pattern-matched by auditor as "1 LU off LUFS tweak" — real scope was missing entire sound design + interactive UI layer.

### 10.1 Template OBLIGATORIA en CP[N]-handoff.md (section "STOP point inventory check")

Engineer NO PUEDE declarar STOP point ni emitir handoff sin completar esta tabla 100% PASS:

```markdown
## SPEC asset_list + ui_active inventory check (BLOQUEANTE)

Verified: $(date +%Y-%m-%d)
SPEC source: creative-specs/<id>.yaml v<X>

### Audio assets (assets/ folder count vs SPEC asset_list)

| Asset class           | SPEC required | Generated      | Status   |
|-----------------------|---------------|----------------|----------|
| SFX prompts           | <N> per L<X>  | <M>            | ✅/🔴    |
| Music tracks          | <N> per L<X>  | <M>            | ✅/🔴    |
| Ambient continuous    | <N> per L<X>  | <M>            | ✅/🔴    |
| TTS segments          | <N> per L<X>  | <M>            | ✅/🔴    |
| Anchors (CP1)         | <N> per L<X>  | <M>            | ✅/🔴    |

### Video assets (assets/clips/ folder count vs SPEC shot_list_total)

| Asset class           | SPEC required | Generated      | Status   |
|-----------------------|---------------|----------------|----------|
| Shot clips base       | <N>           | <M>            | ✅/🔴    |
| Variants (-a/-b/-c)   | <N>           | <M>            | ✅/🔴    |

### UI elements (index.html grep vs SPEC ui_active per shot)

| Element type          | SPEC shots ui_active | HTML wired count | Status   |
|-----------------------|----------------------|------------------|----------|
| countdown_*           | <N> per countdown_appearances | <M>     | ✅/🔴    |
| choice_buttons_*      | <N> shots            | <M>              | ✅/🔴    |
| loading_bar_*         | <N> shots            | <M>              | ✅/🔴    |
| name_labels           | <N> shots            | <M>              | ✅/🔴    |

### Audio tracks wired in index.html

| Track type            | Expected minimum | HTML wired | Status   |
|-----------------------|------------------|------------|----------|
| Narration (master.mp3 or per-segment) | 1 | <M>          | ✅/🔴    |
| Music                 | 1 (or per-section) | <M>      | ✅/🔴    |
| Ambient continuous    | 1+ (per section) | <M>        | ✅/🔴    |
| SFX events            | 5+ (per SPEC sfx_categories) | <M> | ✅/🔴 |

### Verdict

[ ] ALL ROWS PASS → ✅ STOP point VALID → handoff emitted
[ ] ANY ROW FAIL → 🔴 STOP point INVALID → engineer continues execute (CP4-audio / CP5-UI / etc.) hasta ALL PASS antes de declarar STOP
```

### 10.2 Verification command (engineer auto-fills before STOP point declaration)

```bash
cd <project>
SPEC="creative-specs/<id>.yaml"

# Audio inventory
echo "=== AUDIO ASSETS ==="
echo "SFX:     SPEC=$(yq '.asset_list.sfx_prompts_to_generate | length' $SPEC) / Actual=$(ls assets/sfx/*.mp3 2>/dev/null | wc -l)"
echo "Music:   SPEC=$(yq '.asset_list.music_to_generate | length' $SPEC) / Actual=$(ls assets/music/*.mp3 2>/dev/null | wc -l)"
echo "Ambient: SPEC=$(yq '.asset_list.ambient_continuous_to_generate | length' $SPEC) / Actual=$(ls assets/ambient/*.mp3 2>/dev/null | wc -l)"
echo "TTS:     SPEC=$(yq '.asset_list.tts_segments_to_generate' $SPEC) / Actual=$(ls assets/tts/*.mp3 2>/dev/null | wc -l)"

# UI wired in index.html
echo "=== UI ELEMENTS WIRED ==="
echo "countdown:    HTML count=$(grep -c -i countdown index.html)"
echo "choice button: HTML count=$(grep -c -i choice-button index.html)"
echo "loading bar:   HTML count=$(grep -c -i loading-bar index.html)"

# Audio tracks
echo "=== AUDIO TRACKS WIRED ==="
echo "audio tags:    HTML count=$(grep -c '<audio' index.html)"
```

Si CUALQUIERA `Actual < SPEC` o `HTML count = 0` cuando SPEC requires → engineer NO emite STOP. Continúa execute.

### 10.3 Forward — automation Phase 1

`scripts/audit-spec-completeness.py` (Phase 1 priority) automates esta tabla:
- Parse SPEC.yaml asset_list + ui_active per shot
- Diff actual filesystem + index.html grep
- Emit table + 🔴/✅ verdict per row
- Exit 1 if ANY 🔴 (blocks engineer STOP declaration)
- Auditor runs as gate antes de cualquier otro CP5 audit (per AUDITOR-PROTOCOL § 3 CP5 step 9)

### 10.4 Responsibility

- **Engineer owns**: complete the inventory table 100% PASS BEFORE emit STOP point handoff. Si CUALQUIERA 🔴 → continue execute, do NOT emit STOP.
- **Auditor owns**: re-run inventory diff independently (NO trust engineer's table), block CP5 gates si any 🔴.
- **Architect owns**: SPEC asset_list + ui_active per shot must be complete + measurable (current state OK per matadero SPEC L1933-1955).

### 10.5 Caso disparador (codified for reference)

**Matadero CP5 STOP point 2026-05-19**:
- Engineer self-report: `renders/draft.mp4` ✅ + `assets/clips/` 29 clips ✅ + `assets/tts/` 19 segments ✅ + `master.mp3` narration mix ✅
- Engineer label: "coverage_pct 69.93% structural" — interpreted "1 LU off LUFS"
- User flag: "faltan SFX + countdowns 3-2-1 + cut effects"
- Auditor direct measure: `assets/sfx/` 0/10, `assets/music/` 0/3, `assets/ambient/` 0/2, `index.html` 0 countdown / 0 button / 0 loading wired
- Lesson: engineer can't declare STOP based on partial sub-CPs (only video done) — STOP requires SPEC asset_list 100% inventory. Auditor can't pattern-match labels — must measure directo. Both gaps closed by § 10 inventory table + AUDITOR-PROTOCOL § 3 CP5 step 9.

---

## 11. Open evolution questions

| # | Question | Status |
|---|----------|--------|
| 1 | Cuándo promote NIVEL 4 → 3 → 2: ¿N=2 videos suficiente o requiere N=3 con format diferente? | TODO empirical |
| 2 | Hierarchy resolution edge case: si NIVEL 3 INGENIERO-PAUTA empirical contradice SPEC NIVEL 4, ¿cuál wins? | TBD — probably SPEC wins porque architect-creative-intent explicit |
| 3 | Auditor LLM judgment independence: ¿basta con "fresh context per role" o necesita different model entirely? | TBD Phase 4 |
| 4 | Multi-agent NIVEL 1 generalization: ¿este protocolo aplica a non-video projects (e.g. software development, marketing campaigns)? | TBD — test cuando exista non-video proyecto |
| 5 | Escalation budget: cuántos $ permitir auto-decide antes de user override? | TODO formalize |
| 6 | Re-handoff cycle cap: ¿cuántas vN versions permitir antes de NO-GO completo? | TBD empirical |
| 7 | Cuando hay 2+ architects (e.g. one creative + one technical), ¿cómo se coordinan? | TBD si caso aparece |

---

## 12. Quick reference card

### Para architect

```
Antes de cada CP:
1. Read SPEC + NIVEL 3 PAUTA-MASTER + relevant NIVEL 1+2
2. Anticipate engineer questions Q1-QN
3. Pre-categorize features load-bearing vs enrichment (per archetype)

Durante PRE-gate:
1. Emit Q-verdicts creative
2. Cite authority con line numbers
3. Concur con auditor verdicts o flag disagreement con canonical rationale

Durante POST-gate:
1. Audit creative deliverables
2. Approve as_built annotations
3. Promote lessons a higher layer si applicable
```

### Para engineer

```
Antes de execute:
1. Self-audit pre-execute (smoke test, SPEC trigger compliance, NIVEL 2 tools available)
2. PRE-handoff package self-contained con Q1-QN architect + A1-AN auditor

Durante execute:
1. Apply verdicts + fixes
2. Respect SPEC trigger gates (NO parallel-process pre-gate)
3. Self-audit incremental (no esperar a POST)

POST-execute (CRITICAL pre-STOP):
1. ⛔ § 10 inventory table OBLIGATORIA — 100% PASS antes de emit STOP point
   (SFX/music/ambient generated? UI countdown/buttons/loading wired? Audio tracks ≥4?)
2. Measurements + visual review
3. POST-handoff package con deliverables + measurements + flags + § 10 inventory table
4. NEVER author architect-domain content (cita pero no invent)
5. NEVER declare STOP con CUALQUIERA inventory 🔴 — continue execute hasta ALL PASS
```

### Para auditor

```
Antes de cada audit:
1. READ FUENTES DIRECTAS — NO delegar (NIVEL 1 + 2 + 3 ambas pautas + 4 SPEC)
2. Identify autoridad hierarchy si hay conflict
3. Coverage matrix: ¿qué items debo verificar este CP?

Durante audit (CP4/CP5 BLOQUEANTE pre-cualquier-otro-gate):
1. ⛔ C-INVENTORY first — `ls assets/sfx/`, `grep countdown index.html`, etc.
   (NO trust engineer's labels — measure directo. Anti-pattern #8 AUDITOR-PROTOCOL § 6)
2. Tabla findings con line numbers
3. 4 verdict states (🟢/🟡/🔴/⛔)
4. Copy-paste ready bloque para bridge (user/orchestrator)

Post-audit:
1. Concurrence con architect verdicts (verify cita autoridad correctly)
2. Flag canonical-violations forward (lessons learned)
3. NEVER edita SPEC ni handoffs — solo emit findings
4. NUNCA pattern-match label engineer ("coverage_pct structural" ≠ "1 LU off")
   — Hard rule #19 NUNCA estimar SIEMPRE medir aplica al auditor también
```

---

**Última actualización**: 2026-05-19 (Phase 0 — § 10 inventory table OBLIGATORIA added post gap #13)
**Próxima revisión**: post-CP5 matadero-banquete closure + audit-spec-completeness.py implementation
