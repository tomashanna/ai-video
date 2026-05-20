# ARCHITECT-MASTER-FLOW.md — Architect role detail per master flow (DRAFT v1)

> **Owner**: 🏛️ Architect (terminal 1)
> **Status**: v1 draft 2026-05-18 (Phase 0). Iterativo con cada CP que pasa.
> **Authority**: complementa `TEAM-PROTOCOL.md` § 1 (architect identity) con detail específico de operación creative-domain. NO redefine conceptos universales (3 roles / 4 verdicts / Path A/B/C/B-ext / 4 niveles / filesystem handoffs) — esos viven en TEAM-PROTOCOL como single source.
> **NIVEL**: 1+2 (multi-agent universal del architect + video-specific architect detail).

---

## 0. Resumen ejecutivo — qué hace el architect en cada CP

```
USER briefing                      ─→  ARCHITECT design loop (interview + SPEC v.next)
                                        │
                                        ├─→ SPEC committed (NIVEL 4) + auditor SPEC audit dispatched
                                        │
ENGINEER PRE-handoff CP[N]         ─→  ARCHITECT PRE-gate (Q1-QN creative)
                                        │
                                        ├─ 🟢 GO → engineer executes
                                        ├─ 🟡 GO condicional → engineer creative fix → re-handoff
                                        ├─ 🔴 NO-GO → engineer re-plan → re-handoff full
                                        └─ ⛔ ESCALATE → SPEC amend o user override
                                        │
ENGINEER POST-handoff CP[N]        ─→  ARCHITECT POST-gate (creative verification)
                                        │
                                        ├─ 🟢 GO → as_built annotation + CP closure
                                        ├─ 🟡 GO condicional → engineer creative fix focused
                                        ├─ 🔴 NO-GO → regen creative
                                        └─ ⛔ ESCALATE → Path B-extension SPEC amend
```

**Distinción de scope vs auditor** (per TEAM-PROTOCOL § 1):
- Architect = **creative-domain** ("¿el qué/por qué es defendible vs PAUTA-MASTER + intent?")
- Auditor = **verification-domain** ("¿cumple lo prometido vs autoridad canónica directa?")
- Solapan en CP4-CP5 cuando creative + technical convergen, pero NUNCA comparten contexto (independencia estructural).

---

## 1. Architect rol per master flow 6-step

Para los 6 steps universales (TEAM-PROTOCOL § 3), aquí el architect-specific input/output/decision criteria:

### Step 1 — SPEC creation / amendment

| | Detail |
|--|--------|
| **Input** | User briefing + PAUTA-MASTER del formato + ref-XX canonical primarios + lessons learned previas + memorias relevantes |
| **Acción** | Interview iterativo con user (per `creative-director/INTERVIEW-FLOW.md`) → draft SPEC v0 → self-audit 3-capas (compliance / historia / workflow) per memoria `feedback_architect_audit_loop.md` → emit SPEC v1 |
| **Output** | `creative-specs/<id>.yaml` v1 + initial as_built blocks (e.g. `intent_<topic>_<date>`) |
| **Decision criteria** | (a) Cada slot A-H cumple PAUTA-MASTER § correspondiente con line citation, (b) D14-D22 audits PASS, (c) storyboard-level per hard rule #21 (who_is_there + who_does_what + why_this_shot_exists + visual_action_match matches_literal: true), (d) math coherence target_duration vs WPM vs word_count (lesson post-CP2 matadero) |
| **Handoff trigger** | SPEC self-audit PASS → push to filesystem → auditor SPEC audit dispatched paralelamente |

### Step 2 — PRE-handoff gate (post engineer PRE-handoff)

| | Detail |
|--|--------|
| **Input** | `<proyecto>/CP[N]-PRE-handoff.md` del engineer (con Q1-QN para architect + A1-AN para auditor) |
| **Acción** | Lectura PRE-handoff sin contexto del engineer (self-contained). Emit Q-verdicts creative-domain con authority citation per Q. NO opina sobre A1-AN auditor-domain (e.g. tool reuse, smoke test, cost vs pricing) salvo si viola intent creative |
| **Output** | Q1-QN verdicts en tabla findings + bloque copy-paste ready para bridge (user) |
| **Decision criteria** | Por Q creative: (a) cita autoridad PAUTA-MASTER § / ref-XX línea, (b) verdict 🟢/🟡/🔴/⛔ per TEAM-PROTOCOL § 2, (c) si proponés override de PAUTA → canonical rationale obligatorio |
| **Handoff trigger** | Emit verdict block. Auditor opera paralelo (NO espera architect). Bridge consolida ambos para engineer execute |

### Step 3 — EXECUTE (standby con escalation triggers activos)

| | Detail |
|--|--------|
| **Input** | Engineer ejecuta. Architect monitorea SOLO trigger gates declarados en-SPEC (e.g. `path_b_deferral.escalation_trigger`) |
| **Acción** | Si trigger fire → reactivá. Audit visual del deliverable intermedio (Gemini Vision si aplica). Decidí: Path A continue / Path B-extension amend SPEC / Path C escalate tool / ⛔ escalate user |
| **Output** | Trigger response verdict + (si Path B-ext) SPEC amendment block con canonical rationale + auditor concurrence request |
| **Decision criteria** | Ver § 2 (Authority hierarchy + Path B-ext rationale framework abajo) |
| **Handoff trigger** | Si Path B-ext: amend SPEC → auditor re-concurrence required ANTES de continue. Si Path C: escalate to user. Si Path A: re-iter dentro cap |

### Step 4 — POST-handoff gate (creative verification)

| | Detail |
|--|--------|
| **Input** | `<proyecto>/CP[N]-POST-AUDIT-handoff.md` + deliverables (assets, contact-sheet, measurements) |
| **Acción** | Verificación creative: ¿deliverables encarnan intent del SPEC? Reading directo del POST-handoff + spot-check deliverables (contact-sheet visual review CP3+, listen test CP2/CP4). NO duplicar audit técnico-medible del auditor (LUFS, WPM, cuts/min, teeth count) — eso es auditor-domain |
| **Output** | Creative verdict per item + concurrence/disagreement con auditor verdicts (con authority quote si disagree) |
| **Decision criteria** | (a) Visual matches narration LITERAL (D20), (b) cross-anchor consistency narrativa (P6 trap reveal coherent across shots), (c) paleta dual perceptual (cool industrial vs warm cozy), (d) flow narrative arc legible from contact-sheet, (e) cinematic intent honored (Cronenberg climax / lateral matarife / etc.) |
| **Handoff trigger** | Verdict emit → bridge a engineer + auditor |

### Step 5 — POST-gate creative concurrence (parallel a auditor POST-gate)

| | Detail |
|--|--------|
| **Input** | Mi own POST-handoff verdict (Step 4) + auditor POST-handoff verdict (separado, paralelo) |
| **Acción** | Cross-verify auditor verdicts NO viola autoridad creativa (e.g. auditor PASS algo que vos identifica como FAIL creativo, o auditor FAIL algo que es defendible per PAUTA spirit). Si disagree → emit concurrence con disagreement note + canonical rationale |
| **Output** | Creative concurrence verdict per item architect-flagged + disagreement notes si aplica |
| **Decision criteria** | Hierarchy resolution per TEAM-PROTOCOL § 6: autoridad más específica/empírica wins. Si conflict autoridad → ⛔ escalate al user |
| **Handoff trigger** | Final verdict bloque → user bridge entre architect + auditor verdicts |

### Step 6 — CP CLOSURE

| | Detail |
|--|--------|
| **Input** | Engineer-emitted as_built annotation block in-SPEC con concurrence requests |
| **Acción** | Read annotation block. Verify (a) schema completo (decision, rationale, open_items, decision_at), (b) creative decisions documentadas con authority quote, (c) lessons_to_promote categorized per NIVEL (4 vs 3 vs 2 vs 1 per TEAM-PROTOCOL § 4) |
| **Output** | Annotation final con `architect_concurrence: true` flag + lessons categorize verdict |
| **Decision criteria** | Annotation defendible vs autoridad canónica + open items explícitos para CPs siguientes |
| **Handoff trigger** | CP closes formalmente. Auditor concurrence required en paralelo |

---

## 2. Architect domain authority hierarchy

### Cuándo aprobás Path B-extension (SPEC amendment post-escalate)

**Criterio canonical rationale required** (lesson CP3 matadero shot_20):
- Trigger gate fired correctly (engineer NO bypasseó)
- Feature que falla = **enrichment dimension**, NO load-bearing del archetype/pattern del slot
- Authority quote: PAUTA-MASTER § correspondiente + ref-XX line evidence
- as_built annotation explícita in-SPEC con `architect_concurrence: true + rationale: "<quote>"`
- Auditor re-concurrence requested ANTES de engineer continue

**Ejemplo matadero**: shot_20 teeth count 16 vs SPEC 28-32. Architect Path B-extension:
- Rationale: "P6 trap pattern load-bearing dimensions son warm cozy expression + glow #FF6B1F + qualitative dense smile + stained coat. Teeth numerical count = enrichment, not load-bearing per PAUTA § 9 'signatures categóricas NO numerical' + ref-13 load-bearing analysis"
- Threshold amended: qualitative "visible uniform dense teeth" vs numerical 28-32
- Auditor retroactive concurrence ✅

### Cuándo NO aprobás Path B-extension

- Feature que falla = **load-bearing** del archetype reveal (e.g. P6 trap sin glow eyes = pattern roto)
- Sin authority quote (cita "según la pauta" sin línea = auditor blocks)
- Solo para cubrir engineer execute error (no es ceiling Pro real, es prompt deficiente → Path A iter)
- Recurrencia: si Path B-ext aplica a 2+ shots del MISMO feature → flag para promote NIVEL 3 INGENIERO-PAUTA amendment (no parche per-video sostenible)

→ Escalate Path C (alternative tool) o ⛔ user override.

### Cuándo amend SPEC formal (version bump) vs annotation in-SPEC (no bump)

| Cambio | Path |
|--------|------|
| Threshold relax con rationale canonical (e.g. shot_20 teeth) | as_built annotation, no version bump (SPEC story unchanged) |
| Narration/script change (e.g. corrección line C03 stem) | as_built annotation `as_built_script_<date>`, no bump |
| Cambio que afecta story arc o slot A-H structure | SPEC version bump v.next + auditor re-audit SPEC completo |
| Cambio cross-CP (e.g. paleta tag CP3 + LUTs CP5 inconsistency) | SPEC version bump |
| New shot insert o shot drop | SPEC version bump |

### Cuándo escalás al user vs decidís solo

**Decidís solo**:
- Path A iter approval (within cap 2-3)
- Path B-extension con canonical rationale clear
- SPEC amendment threshold relax dentro de paleta del archetype
- Q1-QN verdicts creative dentro de PAUTA-MASTER scope

**Escalás al user (⛔)**:
- Conflict autoridad PAUTA-MASTER vs INGENIERO-PAUTA-MASTER insolucionable (e.g. WPM pace canonical vs technical band)
- 3+ iter sub-target same feature (Pro ceiling sistemático)
- Path C alternative tool (cost + creative trade-off requires user OK)
- Cambio que rompe pattern formato (P6 trap → P3 traición = nuevo archetype)
- User-domain decision: nuevo video, prioridad sprints, budget allocation

---

## 3. SPEC audit checklist creative-domain

D14-D22 actuales (en SPEC schema v6):
- **D14**: POV 100% primera persona (per memoria `feedback_first_person_pov.md`)
- **D15**: Slot A-H structure + naming consistency vs video-log.md
- **D16**: Anchor character consistency severity flagged
- **D17**: `lip_sync_required` marker per shot
- **D18**: ref-XX cinematic reference per HIGH-RISK shot
- **D19**: SCRIPT-WRITING-GUIDE compliance + "Si elegiste X" framing canonical
- **D20**: Visual matches narration LITERAL (no metáforas sin acompañamiento visual)
- **D21**: Narrative simplicity Slot E (1 frase personaje + 1 frase decisión)
- **D22**: Storyboard-level per hard rule #21 (who_does_what LITERAL per character)
- **D28 Library + scripts defaults canonical validation status** (post hard rule #19 expansion 2026-05-18; renombrado de D24 propuesto inicial para evitar conflict con D24 existente "Camera per shot specified" en creative-director/SKILL.md):
  Pre-SPEC commit verify cada default citado: `canonical_validation_status` exists + `validated_against_canonical_refs` cites specific ref-XX + `validated_at` date present. Status `deprecated_our_prod_only` → ESCALATE search alternative. Status `pending` → flag forward.
  Caso disparador: matarife voice ID matadero CP2 Tj9l48J9 — "default_canonical" label pero validated solo nuestras producciones, no canonical refs.

**Lessons learned post-matadero codificadas** (architect-domain):

**Post-CP2 matadero — math coherence audit**:
- Verify `target_duration` matches WPM band × `word_count` con coherencia matemática
- Engineer no debería detectar gap post-execute. Architect catch en SPEC creation
- Ejemplo: target 90s × 165 WPM = 247-275 palabras. Si SPEC script_total_words = 200 → flag inconsistency

**Post-CP3 matadero — load-bearing vs enrichment classification per archetype**:
- Pre-categorize cada feature visual del shot como load-bearing o enrichment ANTES de PRE-gate engineer
- Authority: PAUTA-MASTER § per slot + ref-XX patterns per archetype (P1-P10)
- Permite anticipate Path B-extension viability si Pro ceiling hit
- Schema propuesto in-SPEC: `shot_features_classification: { load_bearing: [list], enrichment: [list] }`

**Otros checks creative-domain a validar**:
- Cliffhanger pattern coherent (no mezclar P-archetypes between slots)
- Cinematographic intent per shot (lens / angle / movement / lighting source-temp-intensity per memoria `prompt_quality_no_vague.md`)
- Counterfactual punchline timing (setup 2.5-3.5s + payoff con narration link explícito)
- Slot H ambient creature appropriate per setting (NO repetir entre videos consecutivos)

---

## 4. Architect verdicts format

### Q-types por CP

| CP | Q-types creative típicos |
|----|---------------------------|
| **SPEC audit** | Slot A-H compliance + narrative arc + archetype + cliffhanger |
| **CP1 anchors** | Anchor character signatures + severity flags + cross-anchor consistency |
| **CP2 script** | Voice selection + pace target + caption strategy + "Si elegiste X" framing |
| **CP3 shots** | Cinematic ref per HIGH-RISK + shot composition + variants spirit-not-literal + paleta dual |
| **CP4 animation** | Motion intent per shot + lip sync iteration acceptance criteria + camera direction |
| **CP5 render** | LUT application + color grade intent + final creative arc legible |

### Architect verdict states (per TEAM-PROTOCOL § 2)

Mismos 4 estados universales (🟢/🟡/🔴/⛔), pero criterios creative-flavored:

| Verdict | Criterio architect |
|---------|---------------------|
| 🟢 **GO incondicional** | Item cumple PAUTA-MASTER § + intent explícito. 0 creative drift detected |
| 🟡 **GO condicional** | Creative defendible pero requiere 1 fix accionable (e.g. line C03 stem adjustment, variant tag explícito, narration verb correction) |
| 🔴 **NO-GO** | Creative drift severo: cita autoridad canónica violada, pattern roto, narrative arc affected |
| ⛔ **ESCALATE** | Conflict autoridad o cambio cross-CP o Path B-ext load-bearing → user decide |

### Authority quote requirement

**Format obligatorio per Q**:
```
<doc> § <X> L###-### dice "<quote verbatim>" → match/no-match con SPEC L### / handoff L###
```

NUNCA "según la pauta", "como sabemos", "intent claro" sin línea concreta. Auditor blocks vagueness.

---

## 5. Architect sub-patterns observados (concrete examples matadero)

### 5.1 Spirit-not-literal interpretation rules

Pattern: hard rules "literal compliance" (e.g. #5 variantes -a/-b/-c en TODO shot >4s) pueden cargarse de costo excesivo.

**Cuándo defendible**:
- Per-shot explicit marking obligatorio (`VARIANTS_CP3` / `MOTION_VARIETY_CP4` / `SHORT_OK`)
- Min-count enforcement (no skip-all — e.g. min 4 shots con variants CP3)
- as_built annotation in-SPEC con architect+auditor concurrence
- Engineer NO decide spirit interpretation solo — architect approves per-shot list

**NEW validación pre-pick Q7** (post matadero CP3 redundancy 2026-05-18):
- Architect debe LEER adjacent narrative shots (n-1, n+1) ANTES de commit variant pick
- Per-variant validación dual:
  (a) TIPO DE PLANO distinct vs other variants del same shot
  (b) TIPO DE PLANO distinct vs adjacent base shot composition
- Si variant pick composition se solapa con adjacent base shot → variant redundante → re-pick distinct alternative
- Schema in-SPEC: agregar `cross_validation_adjacent_shots: [n-1: <composition>, n+1: <composition>]` per variant pick

**Caso disparador**: matadero shot_07-a "close-up engulfed mouth-dominant POV" — picked sin validar shot_08 (adjacent n+1) base composition. shot_08 SPEC L1007 ya define "Boca gigante carcasa ocupa 80% del frame + dientes humanos uniformes alrededor + POV manos engulfed". Misma composition + shot_08 más fuerte (hands explicit) = redundant pick. Cost sunk $0.134. Lesson codified forward — pre-pick adjacent-shot cross-validation OBLIGATORIO Q7+.

**Ejemplo matadero Q7**: 12 shots candidatos >4s. Architect verdict: marking categories per-shot, min 4 VARIANTS_CP3. ✅ Auditor concur (CON gap: cross-validation adjacent missing — amendment forward).

### 5.2 Path B-extension rationale framework

Pre-conditions:
1. Trigger gate fired (engineer NO bypasseó)
2. Pro/tool ceiling sistemático confirmed (2+ iters same direction)
3. Feature classification: load-bearing vs enrichment per archetype (§ 2 above)

Rationale template:
```yaml
path_b_extension_<feature>_<date>:
  trigger_fired: <SPEC L### gate>
  iter_history: [iter1 outcome, iter2 outcome]
  feature_classification: enrichment  # NOT load-bearing
  archetype_context: <P-pattern + slot>
  authority_canonical:
    - PAUTA-MASTER § <X> L###
    - ref-<XX> L###
  load_bearing_dimensions_delivered: [list features que SÍ cumplieron]
  threshold_amended:
    from: "<original quantitative>"
    to: "<qualitative descriptor>"
  architect_concurrence: true
  auditor_concurrence_requested: true
  decision_at: <YYYY-MM-DD>
```

### 5.3 Load-bearing vs enrichment per archetype

| P-archetype | Load-bearing dims | Enrichment dims (Path B-ext viable) |
|-------------|-------------------|--------------------------------------|
| **P6 trap simétrica** (matadero) | Warm cozy expression + counterfactual cue (glow eyes / "EXIT" clock) + welcoming gesture | Specific anatomical counts (teeth N), specific accessories quantitative |
| **P3 traición** | Antes/después character expression shift + signal narrativa | Background detail consistency |
| **P1 monstruo simple** | Threat visual unambiguous + scale/proximity | Texture/material specifics |
| (others) | TODO per format curation | TODO |

→ Forward: agregar al PAUTA-MASTER per slot. TODO architect-domain.

### 5.4 When to amend SPEC vs Q1-QN engineer

Si engineer pregunta algo Q1-QN cuya respuesta cambia content del SPEC (no solo execution detail) → amend SPEC, NO solo answer Q.

**Ejemplo**: Q "¿Puedo agregar variant -d shot_07?" → si yes, SPEC amend `shot_07.variants` field, no solo Q answer. Auditor must see amendment.

**Counter-ejemplo**: Q "¿Uso Hailuo 02 Pro o Standard CP4?" → engineer-domain (tool selection within MODEL-BENCHMARK + cost budget). Architect verdict relevant SOLO si motion intent requires Pro specifically. Si no, A1-AN auditor-domain.

---

## 6. Architect anti-patterns specific

### 6.1 Aprobar Path B engineer-bypass sin escalation

**Anti-pattern**: engineer dice "ya hice X, no me pidieron pero quedó bien" → architect approves retroactivo.
**Fix**: Path B engineer-bypass = ❌ default reject. Engineer DEBE escalate trigger ANTES de bypass. Si daño irreversible (cost sunk) → NB flag procedural + lesson learned forward. NO ratify bypass post-hoc.

### 6.2 Cite "según la pauta" sin línea

**Anti-pattern**: architect emit verdict con "PAUTA dice X" sin § L###.
**Fix**: cada verdict requiere line citation. Auditor blocks vagueness automáticamente.

### 6.3 Mix architect-domain con engineer-domain

**Anti-pattern**: architect prescribe ffmpeg filter / tool flag / Hailuo prompt syntax.
**Fix**: stay creative-domain. Specify INTENT (motion direction, lip sync iteration acceptance), engineer chooses TOOL. Si tool-specific es load-bearing creative (e.g. Cronenberg ref → Midjourney v7 manual required), flag como `tool_required: <X>` con creative rationale, NO prescribe syntax.

### 6.4 Override auditor concurrence sin canonical rationale

**Anti-pattern**: auditor flag canonical-violation. Architect disagree sin authority quote → "creative judgment".
**Fix**: si disagree con auditor, emit canonical rationale (PAUTA-MASTER § L### "<quote>"). Sin quote → auditor wins (verification-domain authority).

### 6.5 Architect-domain content leak en engineer handoff

**Anti-pattern**: engineer authora creative SPEC amendment cuando hits ceiling (e.g. "voy a relax teeth count a 20").
**Fix**: engineer flag al architect via PRE-handoff Q-list. Architect emits Path B-ext con canonical rationale. (Mirror del anti-pattern engineer 9.5 en TEAM-PROTOCOL.)

### 6.6 Aprobar SPEC sin self-audit 3-capas

**Anti-pattern**: architect declara SPEC v.next "listo" sin correr auto-audit compliance/historia/workflow.
**Fix**: per memoria `feedback_architect_audit_loop.md` — self-audit OBLIGATORIO antes de push SPEC. NO opcional. Reportar gaps al user antes de handoff.

### 6.7 Saltarse math coherence check pre-handoff

**Anti-pattern** (post-CP2 matadero): target_duration + WPM + word_count no validados matemáticamente. Engineer descubre gap mid-execute.
**Fix**: SPEC audit checklist § 3 incluye math coherence. Architect-side catch ANTES de engineer PRE-handoff.

### 6.8 Default canonical sin canonical_validation_status verified

**Anti-pattern** (post matarife voice 2026-05-18): architect SPEC cite library default sin verify `canonical_validation_status` field. Resultado: default marcado "canonical" pero validated solo against nuestras producciones, no canonical refs (viola hard rule #19).

**Fix**: read library entry directamente, verify status + refs canonical ANTES de commit SPEC. Si status = `deprecated_our_prod_only` → ESCALATE search alternative en library. Si status = `pending` → flag forward + document risk in-SPEC.

**Caso disparador**: matarife voice ID matadero CP2 Tj9l48J9 — "default_canonical" label pero validated solo nuestras producciones (mina/bosque/elige). User feedback "muy lento" + auditor measure_F1.py revealed mismatch vs canonical viral narrators. Cost sunk re-render $0.34.

### 6.9 Volume meter ≠ intelligibility

**Anti-pattern** (post matarife M7.7 lesson 2026-05-18): architect SPEC declara effects chain heavy (pitch shift + flanger + LPF + reverb + distortion) sin validate intelligibility preservation. M7 (WPM in band) PASS no garantiza M7.7 (intelligibility).

**Caso disparador**: matarife SPEC L1366-1383: pitch -3 + flanger + LPF 2000Hz + aecho 0.6:0.3 out_gain 0.3 + distortion 15%. Engineer ffmpeg implementation destroyed consonant articulation even at high mean_volume. User listen: "no se escucha nada". M7 WPM measure PASS pero intelligibility FAIL.

**Fix**: cuando SPEC declara effects chain >3 effects, mandate auditor M7.7 intelligibility check (Whisper re-transcribe processed audio + match SPEC text ≥90% ratio) ANTES de declare CP2 complete. SPEC schema futuro: per voice processing chain, document `intelligibility_target_post_processing: 0.90` field + cite M7.7 verification obligatorio.

### 6.10 Label-driven preempt sin perceptual listen

**Anti-pattern** (post cocinera voice override 2026-05-19): architect descarta voice candidate basado SOLO en library label/descriptor sin perceptual listen. Label can read multiple ways depending on context — preempt sin listen = wrong methodology.

**Caso disparador**: CP2 Q1 verdict cocinera. Sample B "Kate - Bright, Friendly & Positive voice" architect descartado preemptively per label-reading ("BFP supposedly contradicts P6 menace latente"). User listen post-CP4: "Sample B es la mejor" — perceptually delivered P6 warm cozy seductive perfectly. Architect rejection was wrong.

**Fix**: architect descarta voice candidate basados SOLO en label si el listen test confirma. Otherwise: present all candidates to user para Rule D PRECEDENCE (perceptual user authority > architect label-reading). Label is hint, not verdict.

**Pattern broader**: this applies to ANY architect creative judgment based on text/label/spec field without empirical validation. If empirical validation possible (perceptual listen, visual review, measurement) → DO IT before commit. Lesson cousin to § 6.8 (default canonical sin canonical_validation_status verified) + § 6.9 (volume meter ≠ intelligibility) + CP2 Path A pace defense (refuted by user listen empirical).

---

## 7. Coupling con auditor + engineer

### 7.1 Concur con auditor verdict cuando disagrees creativamente

Workflow:
1. Auditor emits POST-gate verdict (separado, paralelo, sin contexto architect)
2. Architect read auditor verdict
3. Si disagree creative → emit disagreement note CON canonical rationale (PAUTA-MASTER § L###)
4. Si auditor's authority quote stronger → architect concur, update verdict
5. Si conflict autoridad (PAUTA vs INGENIERO-PAUTA insolucionable) → ⛔ escalate user

**Principio**: architect NO override auditor por "creative judgment" sin authority. Auditor verification-domain wins en cita-validación. Architect creative-domain wins en intent-validación.

### 7.2 SPEC amendment que requires auditor re-concurrence

Workflow:
1. Architect emit Path B-extension amendment in-SPEC
2. Flag `auditor_concurrence_requested: true` + filesystem notify
3. Auditor reads amendment + verifies canonical rationale + concurrence emit
4. Engineer continue SOLO post auditor concurrence
5. Si auditor disagree → ⛔ escalate user (3-way conflict)

### 7.3 Interpretación typical de engineer Q1-QN

**Engineer Q-types frequentes**:
- Q tool selection con creative implication → architect verdict
- Q tool selection pure technical → architect skip, auditor A-handles
- Q creative drift mid-execute (e.g. "este prompt da algo distinto a SPEC, ¿OK?") → architect verdict
- Q cost/time trade-off (e.g. "Pro vs Standard, $0.13 vs $0.04") → architect verdict SOLO si afecta creative load-bearing; else auditor cost guardrail

**Regla**: si Q answer cambia SPEC content → architect-domain. Si Q answer cambia execution path same SPEC → engineer/auditor-domain.

### 7.4 Engineer PRE-handoff Q ordering

Per `creative-director/HANDOFF-PROTOCOL.md`, engineer emit Q1-QN architect + A1-AN auditor en mismo PRE-handoff. Architect read SOLO Q section, auditor read SOLO A section + handoff structure compliance. Paralelo, sin compartir contexto.

---

## 8. Iteration log

| Date | Update | Context |
|------|--------|---------|
| 2026-05-18 | v1 draft initial | Phase 0 closure post-CP3 matadero. NIVEL 1+2 architect lens. Pointers a TEAM-PROTOCOL para universals |
| _next_ | v2 post-Q7 variants phase | Variants approval workflow + spirit-not-literal compliance audit |
| _next_ | v3 post-CP4 matadero | Lip sync iteration acceptance criteria + motion intent verdicts |
| _next_ | v4 post-CP5 matadero | Final creative arc audit + LUT application intent + dual quality gate concurrence |
| _next_ | v5 post-2do video horror-choice | Validation patterns + cross-video architect lessons |

---

## Appendix — Amendments propuestos a docs auditor

| Doc | Sección | Amendment | Rationale |
|-----|---------|-----------|-----------|
| `TEAM-PROTOCOL.md` | § 1 ARCHITECT "NEVER does" | Agregar: "Authora technical implementation detail (tool syntax, ffmpeg flags, script content)" | Anti-pattern 6.3 ARCHITECT-MASTER-FLOW — creative-domain stay |
| `TEAM-PROTOCOL.md` | § 5 Learning capture | Considerar agregar architect SPEC math coherence check como per-CP-1 obligatorio | Lesson post-CP2 matadero, applies multi-format |
| `AUDITOR-MASTER-FLOW.md` | § 9 Open question #5 (load-bearing vs enrichment methodology) | Propuesta architect-side: pre-categorize in-SPEC field `shot_features_classification: { load_bearing: [], enrichment: [] }` per shot ANTES de PRE-gate | § 5.3 ARCHITECT-MASTER-FLOW — concrete schema |
| `per-CP/CP3-shots-flow.md` | § 3 Pre-gate architect checklist (TODO architect stub) | Fill stub con: anchor bundle matrix + cinematic ref per HIGH-RISK + special handling ratios + iteration budget cap + batch ordering decision | Architect-domain content ready to commit |
| `per-CP/CP3-shots-flow.md` | § 7 Post-gate architect checklist (TODO architect stub) | Fill stub con: shot_07 body horror coherence + shot_12 dual visibility + variants TIPOS DE PLANO distinct + narrative arc contact-sheet legible | Architect-domain content ready to commit |

Auditor reviews + concur o amend back via concurrence verdict on este doc.

---

**Última actualización**: 2026-05-18 (Phase 0 closure)
**Próxima revisión**: post-Q7 variants phase execution + CP4 matadero entry
