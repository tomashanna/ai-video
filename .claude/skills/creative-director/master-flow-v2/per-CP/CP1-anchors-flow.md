# CP1 — Reference Anchors Flow (DRAFT — basado en matadero-banquete)

> **Status**: v1 draft 2026-05-18. Documentado retroactivamente post-cierre CP1 matadero-banquete.
> **Authority**: auditor-led documentation. Architect+engineer validan + amend.
> **Próxima validation**: 2do video del formato horror-choice end-to-end.

---

## 0. Overview

**Scope**: generar 8 reference anchors (4-6 characters + settings + props críticos) que regirán character/setting/prop consistency en los 22 shots downstream.

| Métrica | Valor matadero-banquete |
|---------|--------------------------|
| Anchors target | 8 (5 STRICT + 3 MEDIUM) |
| Entry criteria | SPEC `approved_by_user` + `reference_anchors` section completa |
| Exit criteria | 8/8 anchors PASS visual audit + cross-anchor consistency + as_built annotations in-SPEC |
| Cost típico | **$0.99-1.16** real ($0.12 Pro 2K STRICT + $0.04 Flash 3.1 MEDIUM + regens 30-50% común) |
| Time típico | ~2-4 horas (incluyendo regens + audit gates) |
| Budget % | ~8-10% del total proyecto |

---

## 1. Pre-handoff structure (engineer)

**File**: `<proyecto>/CP1-handoff.md` (or `-vN.md` si re-handoff cycle)

**Required sections** (per HANDOFF-PROTOCOL L91-138):
1. Lectura obligatoria completada (SPEC sections, MODEL-BENCHMARK, INGENIERO-PAUTA-MASTER, docs/OPERATING-MANUAL.md hard rules)
2. SPEC slots involucrados (reference_anchors.characters/settings/props)
3. Cross-shot coverage audit (count shots per anchor — gaps detection)
4. Estado actual de anchors generados (paths + descriptions)
5. Prompts engineer-expanded con diff vs SPEC visual_anchor_prompt (5-block premium)
6. Fixes autónomos aplicados (engineer-domain decisions per AUTONOMY MATRIX)
7. Plan de ejecución (batches, model selection per severity, cost estimate)
8. Self-audit criteria (qué se verificará POST-gen)
9. Preguntas explícitas Q1-QN (architect) + A1-AN (auditor)
10. Bloqueo explícito (qué destranca el next step)

**Authority cited (must)**:
- SPEC line numbers para cada visual_anchor_prompt
- MODEL-BENCHMARK § character anchor para model selection
- INGENIERO-PAUTA-MASTER § 5.7 premium prompt rule
- Hard rules #18 (template ships 2 pautas paired), #19 (NO autoridad propia), #20 (cheap model = premium prompt)

---

## 2. Pre-gate auditor checklist

Per `AUDITOR-PROTOCOL.md` § 3 CP1:

| # | Item | Verifico |
|---|------|----------|
| A1 | Model selection Pro/Flash 3.1 per severity | MODEL-BENCHMARK § 2.2 character anchor row |
| A2 | Resolution 2K/1K adequate downstream | MODEL-BENCHMARK L1220 + use case |
| A3 | `--no-mono-suffix` flag (dual palette) | `ai-video image:109` flag exists |
| A4 | Aspect 9:16 for reel format | `formats/reel.md` |
| A5 | Cost estimate vs pricing actual | MODEL-BENCHMARK L1222 |
| A6 | Contact-sheet format planeado | engineer self-decision OK |
| A7 | Pre-batch smoke test exists | sugerir si falta (lesson learned matadero) |
| A8 | Self-audit visual measurability | high-risk features (e.g. teeth count, glow) requiere Gemini Vision verification |

**Plus structural CP1 audit**:
- 8 anchors planeados cubren todo character/setting/prop recurrentes (≥2 shots)
- Dual palette intent ejecutable (cool vs warm per anchor)
- Plantillas PAUTA-MASTER § 8/§ 9 cited correctly per character
- Cross-anchor signatures planificadas (glove color cross-PPE, clock cross-setting)

---

## 3. Pre-gate architect checklist

**TODO architect**. Auditor stub:
- Cumple PAUTA-MASTER § 8/§ 9 plantillas per character
- Slot D regla del malo conecta con dilemas downstream
- Slot G cliffhanger archetype rotation per video-log.md
- Setup→payoff props seeded en hook + cliffhanger

---

## 4. Execution sub-patterns observados (matadero-banquete CP1)

### 4.1 Regen iter cycle (4/8 anchors necesitaron regen)

Pattern recurrente: Pro genera con discrepancia minor del SPEC literal → architect/auditor flag → engineer regen v2 con prompt reinforced.

| Anchor | v1 fail | Fix v2 |
|--------|---------|--------|
| Matarife | Gloves mid-forearm vs SPEC "up to elbows" | Prompt + "NOT mid-forearm, NOT short, full forearm coverage required" (negative reinforcement triple) |
| Cocinera | Teeth ~14 visible vs SPEC 28-32 | Prompt "iris area appears to emit light from within" + 3000K (FIX 2) — but Pro ceiling hit at ~20-22 |
| Matadero | "EXIT" sign vs SPEC "5:40 AM red LED" | Prompt + "Digital wall clock showing '5:40 AM' in red LED visible at top-right" |
| Exterior | Brown leather gloves vs blue plastic (cross-anchor matarife/cuchillo) | Prompt + "industrial blue plastic gloves matches matarife" |

**Lesson learned**: Pro Gemini frequently hits "training data common" defaults (mid-forearm gloves, EXIT signs, normal teeth count). **Triple negative reinforcement + specific instruction language** rompe defaults ~50% of times. Si Pro ceiling persistent (e.g. teeth count) → Path B/C territory.

### 4.2 Path B deferral (cocinera teeth)

Pattern: cuando un detail target falla Pro ceiling, defer specific verification a downstream shot dedicated.

**Cocinera anchor**: 28-32 teeth target → Pro delivered ~20-22 → Path B accepted (per SPEC L391 "only noticeable on close inspection") → escalation trigger para shot_20 CP3 close-up.

**Defendibilidad canónica**:
- ✅ DEFENDIBLE si SPEC mismo admite "close inspection only" (L391)
- ✅ DEFENDIBLE si feature affecting downstream tiene gate explicit trigger
- ❌ NO defendible si SPEC target era literal (e.g. clock 5:40 AM cross-anchor signature)

### 4.3 As_built annotation in-SPEC (no version bump)

Pattern: cuando CP cierra con decisiones operacionales (deferral, model selection, regen iter counts), documentar in-SPEC como annotation bloque, **NO bump version** (SPEC creative content intact).

**Matadero ejemplos**:
- `as_built_annotations_2026_05_17` block (cierre CP1)
- `pace_decision_path_A_2026_05_17` (cierre CP2)
- `cp3_variants_strategy_2026_05_17` (mid CP3)

**Schema common**:
```yaml
<topic>_<date>:
  decision: "<one-line decision>"
  architect_concurrence: true|false
  auditor_concurrence: true|false
  rationale: "<authority citation + reasoning>"
  open_items: [list]
  decision_at: YYYY-MM-DD
```

### 4.4 Pre-batch smoke test (engineer lesson learned)

Antes de cascade $1+ en API calls, ejecutar 1 smoke test cheap ($0.04 Flash) que valide `.env` + venv + API quota.

**Caso matadero**: Auditor flageó en PRE-handoff. Engineer aplicó como Step 0 en `gen-anchors.sh`. Si .env mal seteado → falla por $0.04 vs $0.27 cascade desperdiciado.

### 4.5 Cross-anchor signature verification

Algunos anchors comparten signature visual que DEBE matchear cross-asset (no es decoración):
- **Clock 5:40 AM red LED**: matadero ↔ comedor (signature trap P6 — el cliffhanger depende de tiempo congelado)
- **Blue plastic industrial gloves**: matarife + cuchillo + exterior (PPE signature)
- **Olla #D4A847 broth**: cocinera anchor + olla anchor (setup→payoff)

**Audit visual cross-anchor obligatorio en POST-gate** sobre contact-sheet (no anchor-por-anchor isolated).

---

## 5. Post-handoff structure (engineer)

**File**: `<proyecto>/CP1-POST-AUDIT-handoff.md`

**Required deliverables**:
- 8/8 anchor PNG files paths
- Contact-sheet 4×2 grid con labels (per build-contact-sheet.py)
- Self-audit table (per anchor: visual checklist + verdicts)
- POST-CHECKPOINT 1 SELF-AUDIT (HANDOFF-PROTOCOL L142-214 template)
- Flags + open issues forward

**Required measurements**:
- N/A en CP1 (visual quality only — measurements son CP2+)

---

## 6. Post-gate auditor checklist

Visual audit del contact-sheet 8/8 + cross-anchor signatures:

| # | Item | Method |
|---|------|--------|
| V1 | Character consistency cross-shots planeada en anchors | Visual review face/wardrobe/pose per character anchor |
| V2 | Setting coherence cross-shots | Visual review matadero/comedor/exterior/pasillo anchors |
| V3 | Cross-anchor signatures (clock, gloves, olla) | Spot-check cross-pairs |
| V4 | Paleta dual ejecutada | Cool vs warm split per anchor visible |
| V5 | Hard rule #20 premium prompts compliance | Re-check prompts → assets match prompt intent |
| V6 | Hard rule #19 NO autoridad propia | Engineer NO cita producciones propias |

**Gemini Vision audit programmatic** sobre items uncountable visualmente (e.g. cocinera teeth count → `validate-cocinera.py`).

---

## 7. Post-gate architect checklist

**TODO architect**. Auditor stub:
- Anchors honran archetype P6 / Slot B+C plantilla canónica
- Visual signature uncanny memorable (scroll-stop test per PAUTA § 8)
- Cumple contraste extremo malo vs bueno

---

## 8. CP closure

**as_built annotation schema** (validated matadero):

```yaml
as_built_annotations_<date>:
  cp1_closure_date: <YYYY-MM-DD>
  total_iterations:
    <anchor_id>: <iter_count>
  cost_total_cp1_usd: <X.XX>
  cross_anchor_signatures_verified: [list]
  path_b_deferrals_active:
    - shot_id: <shot referenced>
      target: <SPEC target>
      actual_anchor_delivers: <observed>
      escalation_trigger: <criterio para escalate downstream>
  architect_concurrence: true
  auditor_concurrence: true
```

---

## 9. Sub-patterns matadero-banquete (concrete examples)

### Casos Path A/B/C

| Path | Caso | Outcome |
|------|------|---------|
| A (iter regen) | matarife gloves, matadero clock, exterior gloves | Aplicado 3 veces, todos PASS post-regen |
| B (accept deferred) | cocinera teeth 20-22 vs 28-32 | Accepted con explicit shot_20 CP3 escalation trigger |
| C (escalate alternative tool) | NO usado en CP1 | (reservado si Path A falla 3 iter) |

### Test-first

**NO usado en CP1 matadero** — todos los 8 anchors generados en batches paralelos.

**Lesson**: futuros CP1 con HIGH-RISK feature (uncanny extreme, complex composition) podrían beneficiar test-first del anchor más arriesgado antes de cascade.

### Procedural violations

Ninguna detectada en CP1 matadero.

### Re-handoff cycles

| Handoff | Razón |
|---------|-------|
| v1 → v2 | Architect rejected matarife gloves + flag 4 fixes prompts |
| v2 → v3 (NO emitido) | Smoke test fix engineer aplicó directo sin re-handoff (engineer-domain decision OK) |

---

## 10. Open issues forward

| # | Issue | Forward CP |
|---|-------|-----------|
| 1 | Cocinera 28-32 teeth Path B → must verify CP3 shot_20 close-up | CP3 (active — shot_20 generated 16, iter 2 en flight) |
| 2 | Matarife cleaver-head sin face/eyes — lip sync workaround needed | CP4 (vibration handle + caption-as-mouth + voice flanger) |
| 3 | Cocinera voice ID elegida CP2 (Valeria) cross-affects shot_20 voice continuity | CP4 |

---

## 11. Métricas observadas matadero-banquete CP1

| Métrica | Valor |
|---------|-------|
| Anchors planned | 8 |
| Anchors v1 PASS first try | 4/8 (50%) |
| Anchors required regen | 4/8 (50%) — matarife, cocinera, matadero, exterior |
| Cost real (incluyendo regens) | $1.16 |
| Time real | ~3 horas (con audits + regen cycles) |
| Cross-anchor signatures issues | 0 (signatures planificados PASS post-regens) |
| Path B deferrals active | 1 (cocinera teeth → shot_20) |
| Procedural violations | 0 |
| Re-handoff cycles | 1 (v1 → v2 post architect feedback) |

---

## 12. Lessons learned codified

1. **Triple negative reinforcement** rompe Pro training data defaults ~50% del tiempo
2. **Pre-batch smoke test** $0.04 evita $0.27+ cascade desperdiciado si .env mal
3. **Visual audit cross-anchor sobre contact-sheet** > audit anchor-por-anchor isolated
4. **Path B deferral defendible solo con explicit escalation trigger** in-SPEC + auditor concurrence
5. **As_built annotations NO require version bump** — annotation operational vs creative change
6. **Engineer NUNCA autora architect-domain content** — re-handoff cycle para change verbatim del SPEC

---

**Última actualización**: 2026-05-18 (post-CP1 matadero closure)
**Próximo update**: 2do video del formato horror-choice end-to-end → validation patterns
