# SPEC-VS-CANONICAL-AUDIT — invernadero-turno-riego (V6)

**Audited**: 2026-05-31
**SPEC**: `creative-specs/invernadero-turno-riego.yaml` v11.1 (post-F1 amendment)
**Auditor**: terminal independiente. Corrí los 3 validators yo mismo + leí PAUTA-MASTER / refs / MODEL-BEHAVIOR-LOG directo + medí la narración palabra-por-palabra (no delegué al self-validation del arquitecto — anti-pattern #1/#8/#17).
**Pattern**: P9 (Peligroso te ayuda) · **Apariencia**: doble-amable (territorio virgen) · **Delivery**: reel 9:16 ~90s

---

## Coverage tally
- `references_canonical[]` declarados: **5/8**
- Coverage floor (≥5/8): **PASS**

## Per-ref linkage table (verificada substantiva, no boilerplate)
| ref_id | Citado | informs[] | Linkage substantivo | Nota |
|--------|:---:|---|:---:|---|
| ref-09 | SÍ | pattern, counterfactual_placement, emotional_framing, cliffhanger, shot_02, char_a | ✅ MAESTRO — P9 calco 1:1 (Victor amenazante=salvador → Bruno musgo=salvador); counterfactual OPENING | core del video |
| ref-03 | SÍ | shot_06, shot_07, pacing | ✅ D1 objeto-tentación ("enciendes" → "comes la fruta") + framing acción-condicional | — |
| ref-08 | SÍ | char_b, shot_05 lip-sync, shot_09 | ✅ refuta "bueno calla" (Celeste habla) + feeding-creature (planta ↔ tiburones) | — |
| ref-10 | SÍ | shot_15, shot_18, drone_base | ✅ válvula procedural (CO2 ↔ vapor a presión) + outro laboral-cozy | — |
| ref-06 | SÍ | shot_16, consequence_framing_style | ✅ P1 contra-impulso (el impulso cómodo mata) | — |
| ref-11/12/13 | NO | — | — | razones declaradas en SPEC (outlier / melodrama / P6 hedonista) — aceptable |

## PAUTA-MASTER section compliance
- §19.5 hook sub-beats (countdown LAST): **PASS** (name_labels → setting → push-in → countdown)
- §24 counterfactual (before_choice_resolves + stakes_lift, NO retrospective): **PASS**
- §23 cuts/min (banda declarada 18-22): **PASS**
- HR#14 rotación (P9 ≠ #8 P1): **PASS**
- anti-cliché (0 frases prohibidas): **PASS**

## MODEL-BEHAVIOR-LOG verification
- Entry 1 (Bruno musgo = rasgo aislable de la cara): locus-anchors `char_a_v1_neck` + `char_a_v1_knuckles` + `visual_signature_critical_loci` + `locus_anchor_required: true` → **PASS** (consistencia cross-shot a verificar en CP3)
- Entry 2 (no label-prefix en camera_intent): **PASS** (frases descriptivas)

## Validators (corridos por el auditor, post-F1)
| Validator | overall_status | FAIL | Nota |
|---|---|:---:|---|
| `audit-spec-narration-fits-duration.py` | pass | 0 | 15 shots; todos caben |
| `audit-spec-lip-sync-marks.py` | pass | 0 | 22/22; dialog shots 05/10/15 marcados true |
| `audit-spec-narrative-coherence.py` (--skip-semantic) | flag | 0 | 2 advisory no-bloqueantes (abajo) |

⚠️ Semantic `signature_staging` check NO corrió (sentence-transformers ausente del venv). Verificación MANUAL del auditor: invernadero húmedo-orgánico es semánticamente lejano de toda la lista previa (lab/matadero/cinema/cerro/parque/cabina/mina/bosque/isla) → uniqueness PASS con alta confianza.

## Findings
| # | Finding | Verdict | Estado |
|---|---|:---:|---|
| **F1** | Modelo de capa del narrador ambiguo (Layer1+Layer3) + §9 ⟂ nis divergen → riesgo desync (anti-pattern #16) / cobertura (HR#30) | 🟡→✅ | **RESUELTO**. Verificado: narrador Layer3-only; §9==nis verbatim 15/15; 0 huérfanos |
| **F2** | `structure_wpm` flag shots 16/20 (banda estilística) | 🔵 NB | Aceptado (roles decisión/resolución; fit físico OK) |
| **F3** | Lip-sync on-screen shots 05/10/15 (Celeste/Bruno hablan) | 🔵 NB | Aceptado (Phase 3 Hedra diferido; líneas 4-6 palabras; igual que V5 Hugo) — flag forward CP4 |
| **F4** | `audit-spec-narration-fits-duration.py` NO implementa el check de la MATRIX (usa MAX_WPM=280 hardcoded, no lee clip cap 5.9s) — enforcement de HR#28/29 ausente en código | 🟠 sistémico-forward | NO bloquea V6 (chunking manual verificado sano). Forward: buildear el check real + verificar/portar template antes de V7 |

## Verdict
🟢 **PASS** — SPEC canónicamente compliant. F1 resuelto + verificado independiente. Proceder al gate de aprobación CP0 del usuario (Tomás) → CP1 anchors.

## Forward (carry al engineer/próximos CPs)
- CP1: generar 4 anchors (char_a_v1 full + char_a_v1_neck + char_a_v1_knuckles locus + char_b_v1). Verificar consistencia del musgo de Bruno cross-shot (Script B dim 6).
- CP4: lip-sync aproximado shots 05/10/15 (F3) — líneas cortas mitigan.
- Sistémico: F4 — enforcement real de HR#28/29 antes de V7.
