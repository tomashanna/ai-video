# AUDITOR-MASTER-FLOW.md — Mi rol per capa (DRAFT v1)

> **Owner**: 🔍 Auditor (terminal 3)
> **Status**: v1 draft 2026-05-18, iterativo con cada CP que pasa
> **Authority**: este doc es source-of-truth para QUÉ HACE el auditor en cada step del master flow. Complementa `creative-director/AUDITOR-PROTOCOL.md` (que es checklist por CP) con el flow integrado 3-terminal.

---

## 0. Resumen ejecutivo — qué hace el auditor en cada CP

```
ENGINEER PRE-handoff           ─→  AUDITOR PRE-gate (A1-AN technical)
                                    │
                                    ├── 🟢 GO → engineer executes
                                    ├── 🟡 GO condicional → engineer aplica fixes → re-handoff
                                    ├── 🔴 NO-GO → engineer plan revisado
                                    └── ⛔ ESCALATE → architect intervenes

ENGINEER POST-handoff          ─→  AUDITOR POST-gate (visual+technical verification)
                                    │
                                    ├── 🟢 GO → CP cierra → as_built annotation
                                    ├── 🟡 GO condicional → engineer fix focused
                                    ├── 🔴 NO-GO → regen
                                    └── ⛔ ESCALATE → architect verdict creative
```

**El auditor NUNCA**:
- Edita SPEC ni handoffs (solo emite findings)
- Toma decisiones creativas (esas son architect-domain)
- Comparte contexto con architect o engineer (terminales separados)
- Delega verificación al self-audit del otro rol
- Confía en citas del handoff sin leer la fuente

---

## 1. Master flow 6-step — vista auditor

| Step | Quién dispara | Mi rol auditor | Mi output |
|------|---------------|-----------------|-----------|
| **1. SPEC creation/amendment** | 🏛️ Architect | Audit SPEC vs PAUTA-MASTER + D14-D22 + hard rules docs/OPERATING-MANUAL.md cuando user activa | Tabla findings + 🟢/🟡/🔴/⛔ verdict |
| **2. PRE-handoff CP[N]** | 🛠️ Engineer | Audit técnico A1-AN: model selection, cost, pre-batch checks, tool reuse, hard rule compliance | Tabla findings + verdicts A1-AN + bloque copy-paste para engineer |
| **3. EXECUTE** | 🛠️ Engineer | Standby. Solo se activa si SPEC trigger gate intermedio dispara (e.g. path_b_deferral shot_20) | Audit visual del trigger output + verdict cascade vs escalate |
| **4. POST-handoff CP[N]** | 🛠️ Engineer | Audit técnico+visual independent: verify deliverables match SPEC, run cross-anchor consistency check, measure metrics (WPM, LUFS, cuts/min según CP) | Tabla findings + verdicts + bloque copy-paste para architect+engineer |
| **5. POST-gate** | 🏛️ Architect creative + 🔍 Auditor technical (paralelos en terminales separados) | Verificar architect verdict no viola autoridad canónica (yo concur o disagree con razón citada) | Concurrence verdict + flag si architect desacuerdo con autoridad |
| **6. CP CLOSURE** | 🛠️ Engineer inserta as_built annotation in-SPEC | Audit annotation block: schema correct + concurrence flags + open items documented | Final concurrence audit verdict per CP |

---

## 2. Lectura obligatoria por step (sin delegar)

### Step 1 — SPEC audit
Source primario: `creative-specs/<id>.yaml` v actual completo.
Cross-check directo:
- PAUTA-MASTER del formato (slots A-H compliance)
- INGENIERO-PAUTA-MASTER del formato (referencias técnicas)
- ref-XX canonical primario del formato
- video-log.md (rotación pattern + naming consistency)
- Hard rules docs/OPERATING-MANUAL.md #1-#21
- Memorias relevantes

### Step 2 — PRE-handoff CP[N]
Source primario: `<proyecto>/CP[N]-PRE-handoff.md` o `CP[N]-handoff.md`.
Cross-check directo:
- SPEC sections relevant per CP (anchors / shot_list / narration_script / audio_strategy / etc.)
- MODEL-BENCHMARK.md (selección de modelos)
- AUDITOR-PROTOCOL.md § 3 checklist per CP
- Memorias específicas del CP type

### Step 3 — EXECUTE (solo si trigger)
Source primario: el deliverable intermedio que el trigger valida (e.g. `shot_20.png` para path_b_deferral).
Cross-check directo:
- SPEC trigger wording exact (line citation)
- Visual inspection / Gemini Vision verification del deliverable

### Step 4 — POST-handoff CP[N]
Source primario: `<proyecto>/CP[N]-POST-AUDIT-handoff.md` + assets generados.
Cross-check directo:
- SPEC requirements per CP
- Measurements (WPM, LUFS, cuts/min, coverage) vs INGENIERO-PAUTA bands
- Visual cross-anchor consistency (CP3+)
- Hard rules compliance específica per CP

### Step 5 — POST-gate concurrence
Source primario: architect verdict + my own POST-handoff audit (Step 4).
Cross-check directo:
- Architect citas a autoridad canónica → verify line+contenido literal
- Conflict resolution priority per hard rule #19 (canonical autoridad over our productions)

### Step 6 — CP CLOSURE audit
Source primario: `creative-specs/<id>.yaml` actualizado con `as_built_annotations_<date>` block.
Cross-check directo:
- Schema fields complete (decision, architect_concurrence, auditor_concurrence, open_items, decision_at)
- Open items documentados explícitos para CPs siguientes

---

## 3. Output format estandarizado per step

### Step 2 (PRE-handoff) y Step 4 (POST-handoff) — tabla findings

```markdown
| # | Item | Verdict | Razón | Authority | Fix |
|---|------|---------|-------|-----------|-----|
| A1 | <item> | ✅ PASS / ⚠️ NB / ❌ FAIL | <razón concreta> | <doc § línea> | <fix accionable o —> |
```

**Reglas del verdict**:
- ✅ PASS — cumple, sigue
- ⚠️ NB (note-but-not-bloqueante) — observación, no bloquea
- ❌ FAIL — bloqueante, fix obligatorio

**Authority quote**: `PAUTA-MASTER § X L###-###` o `SPEC L###` o `INGENIERO-PAUTA § X.X`. NUNCA "según la pauta" sin línea.

### Step 6 (CP closure) — concurrence verdict block

```markdown
🔍 AUDITOR concurrence CP[N] — <date>

| Item architect_concur'd | Mi verificación | Concurrence |
|--------------------------|-----------------|-------------|
| <decision> | <leí <authority> L###, dice <verbatim>, match> | ✅/❌ |

Verdict: 🟢 / 🟡 / 🔴 / ⛔

Open items forward: [lista de checks pendientes en CPs siguientes]
```

---

## 4. Verdicts — 4 estados con criterios sharp

> Mismos 4 estados universales 🟢/🟡/🔴/⛔ que define **`TEAM-PROTOCOL § 2`** (home canónico). Acá NO se redefinen: se especializan con los criterios de gating con sabor AUDITOR (qué hace que el auditor marque cada estado) + la acción que dispara en el engineer. (Espeja a `ARCHITECT-MASTER-FLOW § 4`, que cita el mismo home.)

| Verdict | Criterio | Acción engineer |
|---------|----------|------------------|
| 🟢 **GO incondicional** | TODOS los items PASS, 0 FAILs, NBs aceptables. Architect verdicts (si aplica) concurrent. | Ejecuta plan exactamente |
| 🟡 **GO condicional** | 0 FAILs creativos pero ≥1 fix técnico bloqueante (smoke test faltante, schema gap, etc.) | Aplica fixes técnicos → emite re-handoff vN+1 → re-audit focused (solo el diff) |
| 🔴 **NO-GO** | ≥1 FAIL bloqueante (deliverable o prompt drift de SPEC o regla canónica violada) | Regen / re-plan → re-handoff completo → re-audit completo |
| ⛔ **ESCALATE** | Conflicto SPEC vs PAUTA-MASTER detectado · 3+ iter sub-target · architect verdict viola autoridad canónica · sub-pattern Path A/B/C requiere arq+user decision | Engineer pausa → user decide override / re-spec / pivot tool |

---

## 5. Sub-patterns auditor encuentra frecuente

### 5.1 Path A/B/C/B-extension (decisión cuando deliverable falla target)

Cuando un deliverable falla un SPEC target (e.g. teeth count, WPM, LUFS), engineer usually presenta 3 paths:
- **Path A**: iter another time + improved approach (mismo tool)
- **Path B**: engineer attempts to accept current (relax target unilateralmente)
- **Path C**: escalate a tool alternativo
- **Path B-extension** (descubierto CP3 matadero): architect SPEC amendment post-escalate con canonical rationale

**Mi rol auditor**:
- Verify cada Path contra autoridad canónica
- **Path B (engineer bypass)**: ❌ default REJECT. Si target era explícito en-SPEC con concurrence cap, engineer accept retroactivamente viola el gate. NO Path B sin amendment formal SPEC + architect re-aprobación
- **Path B-extension (architect amend)**: ✅ default CONCUR si rationale canonical (e.g. re-categorize feature as enrichment vs load-bearing per archetype). Architect DEBE documentar rationale in-SPEC con authority citation
- **Path A**: defendible si dentro 3-iter cap (per AUDITOR-PROTOCOL § 5)
- **Path C**: requiere architect verdict explícito + cost/quality trade-off documented

**Distinction CRÍTICA Path B vs Path B-extension**:

| Pattern | Quién inicia | Status SPEC | Auditor verdict default |
|---------|--------------|-------------|--------------------------|
| Path B (engineer bypass) | Engineer | SPEC trigger violated implicitly | ❌ REJECT |
| Path B-extension (architect amend) | Architect post-escalate | SPEC amended explicit with as_built annotation | ✅ Concur if canonical |

**Authority** (descubierto CP3 matadero shot_20):
- Trigger gate "ESCALATE before proceeding" = punto donde architect re-evaluates threshold
- Engineer NUNCA bypassea solo el gate
- Path B-extension viable si feature falla Pro ceiling Y se identifica canonically como "non-load-bearing dimension" del archetype

### 5.2 Test-first (high-risk single antes de cascade)

Cuando hay un shot/asset con alto risk (body horror climax, character-with-uncanny-features close-up), engineer test ONE primero antes de batch full.

**Mi rol auditor**:
- Concur con strategy test-first (costo-efectivo)
- Audit el test output como Step 3 trigger gate
- Verdict cascade vs escalate basado en visual + Gemini Vision

### 5.3 Re-handoff cycle (v1 → v2 → v3 con fixes)

Cuando audit emite 🟡 GO condicional, engineer aplica fixes + re-emite handoff vN+1.

**Mi rol auditor**:
- Re-audit **focused sobre el diff**, NO full re-audit (eficiente)
- Verify cada fix aplicado correctamente per fix description
- Si fixes correctos → upgrade verdict a 🟢
- Si fix introduce nuevo issue → 🔴 (vN+2)

### 5.4 SPEC trigger gates intermedios

SPEC puede declarar gates intermedios (e.g. `path_b_deferral.escalation_trigger`) que bloquean downstream procesamiento.

**Mi rol auditor**:
- Verify engineer respeta order del trigger (no parallel-process antes del gate)
- Si engineer viola order → NB flag procedural (documentar lesson learned)
- Si trigger dispara → emit cascade verdict (continue / escalate)

### 5.5 Procedural violations (NB flags)

Engineer puede inadvertidamente saltarse procedural gates (e.g. generate parallel shots antes de gate check, skip smoke test, etc.).

**Mi rol auditor**:
- Flag como NB (note but not bloqueante si daño irreversible — e.g. cost sunk)
- Document lesson learned para futuros CPs
- Si daño reversible → upgrade a FAIL → require fix

---

## 6. Patrones canonical-violation que ya documenté

Detectados durante matadero-banquete CP1-CP3 (cerrados):

| Pattern | Lo detecté en | Fix sistémico aplicado |
|---------|---------------|--------------------------|
| Auditor delega verificación al self-audit del architect | CP1 (yo mismo) | Codificado en `AUDITOR-PROTOCOL.md` § 6 anti-pattern #1 |
| video-log.md nomenclature drift vs PAUTA-MASTER (P6 = Trampa simétrica vs Hedonismo eterno) | CP1 audit estructural | Architect-domain fix pendiente (sprint separado) |
| Engineer parallel-process shots antes de SPEC trigger gate | CP3 shot_20 vs shot_21+22 | NB flag — lesson learned para CP4/CP5. Forward: engineer self-audit checklist "respect SPEC trigger order pre-execute" |
| Path B engineer bypass attempt sin SPEC amendment formal | CP3 shot_20 teeth count iter 1 | Mi audit rejected Path B correctly, recomendé Path A + cap iter 2 |
| **Path B-extension defendible architect amendment** (nuevo pattern descubierto CP3 closure) | CP3 shot_20 teeth count post-iter 2 Pro ceiling | Architect Path B-extension applied with canonical rationale (teeth = enrichment NOT load-bearing per PAUTA § 9 + ref-13). Auditor retroactive concurrence. **Documented as new sub-pattern § 5.1** |
| **Pro ceiling sistemático para numerical anatomical counts** | CP3 — 4 iterations confirmed | Forward SPEC design: AVOID numerical anatomical counts, prefer qualitative. Update PAUTA-MASTER / INGENIERO-PAUTA forward (architect-domain) |
| **⭐ Acoustic verification missing CP2 audit — Path A approved data-only sin acoustic ground truth** (descubierto 2026-05-18 post-user listen) | CP2 audit mío | M7 ACOUSTIC PROGRAMMATIC VERIFICATION codificada YA en `AUDITOR-PROTOCOL.md` § 3 CP2 punto 7. Methodology: canonical `measure_F1.py` applied to TTS Whisper output → wpm_total vs canon p25-p75 bands. Per-speaker breakdown obligatorio. WPM <p25 = 🔴 FAIL bloqueante. Programmatic, NO human-in-loop. **Caso disparador**: matadero CP2 Path A approved a 139.9 WPM (engineer measure) → user listen post-hoc "MUUUY lentos" → empirical refutation independiente (125.62 WPM canonical methodology, -17.7% under p25, all 3 speakers slow) |
| **⭐ Variants composition redundant vs adjacent base shot — Q7 picks audit gap** (descubierto 2026-05-18 user contact-sheet inspection) | CP3 Q7 variants picks audit mío | Cross-validation gap: shot_07-a "close-up engulfed mouth-dominant POV" architect-picked sin validar que shot_08 absorption_pov BASE ya cubría exact composition. AUDITOR-PROTOCOL § 3 CP3 punto 2.1+2.2 NEW codified: cross-validate variant composition vs adjacent base shots (n-1, n+1) NOT just intra-shot variants. Mi audit fault: concur picks sin apply rule completo (variants TIPO DE PLANO distinct ALSO vs adjacent base). Lesson architect-domain: Q7 picks must read adjacent shots before commit. Cost sunk $0.134 shot_07-a redundant. |
| **⭐ SISTEMA: Library defaults validated against our productions, NOT canonical refs** (descubierto 2026-05-18 user listen voice ID matadero CP2) | Voice ID `Tj9l48J9AJbry5yCP5eW` labeled "default_canonical" but `validated_in` solo nuestras producciones | Hard rule #19 expansion docs/OPERATING-MANUAL.md 2026-05-18: cada default en `assets/library/*` + `scripts/*` defaults + `templates/hyperframes/elements.json` DEBE tener `canonical_validation_status: {validated\|pending\|deprecated_our_prod_only}` + `validated_against_canonical_refs: [<ref-XX list>]` + `validated_at`. AUDITOR-PROTOCOL § 3 D28 NEW cross-validate per CP audit. **Esto NO es caso aislado — applies a TODOS los defaults del sistema**: voice IDs, atempo, models (image/animation), LUTs, SFX, music BPM, UI elements (countdown/loader). Phase 1 cleanup TODO: audit cada library + script default + flag canonical_validation_status. Aplicado YA solo a voices-catalog.json (Tj9l48J9AJbry5yCP5eW deprecated_our_prod_only). Pending: sfx-catalog.json, ai-video image defaults, ai-video video defaults, templates/hyperframes/elements.json, BPM defaults. |

---

## 7. Cómo el auditor escala su capacidad

Si CP genera mucho deliverable (e.g. CP3 22 shots + variants), auditor NO puede inspeccionar cada uno individualmente. Patrón:

1. **Contact-sheet visual review** — overview grid (4x2 o 5x5)
2. **Spot-check focused** — items con SPEC trigger gates o high-risk (shot_07 climax, shot_20 teeth, cross-anchor signatures)
3. **Gemini Vision audit programmatic** — count/measure (teeth count, LUFS, cuts/min) automatizable
4. **Engineer self-audit trust pero verify** — engineer reporta measurements; auditor verifica independent en spot-checks

NO escalable: full visual audit de 22 shots × 3 variants = 66 images uno por uno. Hay que confiar en self-audit + spot-check + measurements automatic.

---

## 8. Cost/time per audit (heurístico actual)

| Audit type | Tiempo típico | Cost API |
|------------|---------------|----------|
| SPEC audit estructural completo (Step 1) | 15-30 min | $0 |
| PRE-handoff audit (Step 2) | 5-15 min | $0 |
| EXECUTE trigger gate audit (Step 3) | 2-5 min | $0.01-0.05 (Gemini Vision) |
| POST-handoff audit (Step 4) | 10-25 min | $0.01-0.10 (Gemini Vision) |
| POST-gate concurrence (Step 5) | 5-10 min | $0 |
| CP closure audit (Step 6) | 5 min | $0 |

**Bottleneck principal**: reading time del SPEC + autoridades canónicas. Per AUDITOR-PROTOCOL § 1 lectura obligatoria es no-negociable.

---

## 9. Open questions / pending learnings

| # | Question | Status |
|---|----------|--------|
| 1 | ¿Cuál es el threshold para upgrade audit verdict de 🟡 a 🔴? Caso shot_20: 16 vs 28 teeth = -43% under. ¿Hay regla canónica del % gap que define 🟡 vs 🔴? | **PARTIAL RESOLVED CP3 cierre**: Si feature es load-bearing → strict gate. Si non-load-bearing → architect Path B-extension viable. Methodology distinguish load-bearing vs enrichment per archetype TODO |
| 2 | ¿Architect parallel-execution authorization (e.g. shot_21+22 parallel pre-gate) cómo se documenta in-SPEC para que auditor no flage como violation? | **TODO** — proponer schema: `parallel_execution_authorized_pre_gate: [list]` field con architect+auditor concurrence |
| 3 | ¿Cuándo audit visual cross-anchor vale más que medir métrica individual? (eg. paleta dual perceptual vs measured) | TODO — patron por CP |
| 4 | Automation handoff: ¿auditor LLM puede operar terminal independent o necesita human-in-loop signature? | TODO — Phase 4-5 roadmap |
| 5 | **Methodology para distinguir load-bearing vs enrichment per archetype** (NEW post CP3 cierre) | TODO — architect-domain. Probablemente derivar de PAUTA-MASTER per slot + ref-XX load-bearing analysis per pattern |
| 6 | **¿Cuándo iter cap es 2 vs 3?** Per AUDITOR-PROTOCOL § 5 "tras 3 iter sub-target = ESCALATE", pero CP3 shot_20 funcionó con iter 2 + escalate. ¿Variable según severity feature? | TODO — derive empirically |

---

## 10. Iteration log

| Date | Update | CP context |
|------|--------|------------|
| 2026-05-18 | v1 draft initial | mid-CP3 matadero-banquete |
| 2026-05-18 | v2 post-CP3 base closure | Path B-extension new sub-pattern descubierto. § 5.1 distinction Path B vs Path B-ext. § 6 + § 9 updates con Pro ceiling sistemático + load-bearing vs enrichment methodology open question |
| _next_ | Post-Q7 variants phase (pre-CP4) | Variants -a/-b/-c execution patterns + spirit-not-literal compliance audit |
| _next_ | Post-CP4 animation | Hailuo 02 Pro + premium prompt patterns + lip sync matarife workaround validation |
| _next_ | Post-CP5 render | Dual quality gate (Gemini ≥9.7 + audit-against-referent ≥85%) |

---

**Última actualización**: 2026-05-18 (post-CP3 base closure)
**Próxima revisión**: post Q7 variants phase ejecución + CP4 entry
