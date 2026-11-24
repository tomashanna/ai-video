# CP2 — Script + Captions Flow (DRAFT — basado en matadero-banquete)

> **Status**: v1 draft 2026-05-18. Documentado retroactivamente post-cierre CP2 matadero-banquete.
> **Authority**: auditor-led documentation. Architect+engineer validan + amend.

---

## 0. Overview

**Scope**: generar TTS unificado (N segments per narration_script) + captions Whisper post-procesados con SPEC override + voice processing chains (matarife effects + cocinera reverb).

| Métrica | Valor matadero-banquete |
|---------|--------------------------|
| Segments | 19 (narrator 14 + matarife 3 + cocinera 2) |
| Entry criteria | CP1 cerrado + SPEC `narration_script` + `audio_strategy` + `captions_strategy` completos |
| Exit criteria | TTS files generated + Whisper captions + measurements PASS + 3-class system applied |
| Cost típico | **$0.45** real (ElevenLabs $0.40 + sample search $0.05 + Whisper local $0) |
| Time típico | ~15-25 min (Whisper transcribe es bottleneck) |
| Budget % | ~4-5% del total proyecto |

---

## 1. Pre-handoff structure (engineer)

**File**: `<proyecto>/CP2-PRE-handoff.md`

**Required sections**:
1. Lectura obligatoria (SPEC narration_script + audio_strategy + captions_strategy + INGENIERO-PAUTA § 1 pace + assets/library/voices-catalog)
2. SPEC slots involucrados
3. Audits POV + lip_sync_required (D14 + D17 from architect SPEC audits)
4. Voice ID selection (narrator + matarife + cocinera — engineer-domain per SPEC L1364)
5. atempo decision (uniform vs per-segment per INGENIERO-PAUTA § 1.7)
6. Voice processing pipeline plan (ffmpeg chains)
7. Whisper captions pipeline plan
8. Fixes autónomos applied
9. Self-audit criteria
10. Plan ejecución (steps + cost + time)
11. Preguntas explícitas Q1-QN (architect) + A1-AN (auditor)

**Authority cited (must)**:
- SPEC line numbers narration_script segments + voice_processing chains
- INGENIERO-PAUTA-MASTER § 1.1 (WPM bands) + § 1.7 (atempo measured)
- Library voices-catalog (voice IDs validated)
- docs/OPERATING-MANUAL.md hard rule #3 (Whisper exclusive) + #10 (atempo)

---

## 2. Pre-gate auditor checklist

Per `AUDITOR-PROTOCOL.md` § 3 CP2:

| # | Item | Verifico |
|---|------|----------|
| A1 | Hierarchy hard rules conflict resolution | #19 (INGENIERO-PAUTA autoritativa) > #10 (atempo 2x default) cuando measure conflicts |
| A2 | Voice processing approach (ffmpeg vs dedicated tool) | First-attempt ffmpeg + fallback path documented |
| A3 | Cost estimate vs ElevenLabs pricing actual | ~$0.30/1K chars × estimated total chars |
| A4 | Whisper transcribe approach (full vs per-segment) | Full preserves natural timing markers |
| A5 | Matarife audio listen test pre-CP4 obligatorio | SPEC engineer_test_criteria L1385 per-segment validation |
| A6 | Per-segment WPM band compliance | INGENIERO-PAUTA § 1.1 [153-180] p25-p75 |

> ⛔ **FLOW pre-emit (Hard Rule #27, 2026-05-29):** el arquitecto corre los 3 validators (narrative-coherence + narration-fits-duration + lip-sync-marks) contra su PROPIO SPEC ANTES de entregar, e itera hasta 0 FAIL. NUEVO flow = `Architect → self-validate (3 validators) → iterate hasta 🟢 → entrega`. NO el viejo `Architect → entrega con gap → Auditor corre validators → Tomás triangula`. Si el auditor recibe SPEC con 🔴 → RETORNA al arquitecto (no escala a Tomás salvo ambigüedad arquitectural real). Pattern_class 5/5 `architect_self_flags_gaps_instead_of_iterating_pre_emit`.

**Plus structural CP2 audit**:
- Consequence framing marca rama en TODAS las consequence narrations — 🟩 variabilidad ("Si la enciendes"/"Si decides"/"Si elegiste a <Nombre>"), 🟥 NO bare label "Si elegiste A" (validation D19, corregido 2026-05-29)
- Visual matches narration LITERAL (D20 forward CP3)
- Narration simplicity (D21 — 1 frase personaje + 1 frase decisión)
- Pace WPM target alineado con SPEC vs INGENIERO-PAUTA

---

## 3. Pre-gate architect checklist

**TODO architect**. Auditor stub:
- Voice ID selection candidate samples (cocinera Q1 path B) — architect picks de 3
- Voice processing chain intent (matarife "NO humana convencional" SPEC L1383)
- Pace target SPEC vs INGENIERO-PAUTA — architect domain (creative pacing)

---

## 4. Execution sub-patterns observados (matadero-banquete CP2)

### 4.1 Voice ID selection con sample test (Path B Q1)

Pattern: cuando library no tiene voice ID matching SPEC criteria (e.g. "warm_female_spanish_middle_age"), engineer search ElevenLabs library + 3-sample test → architect picks.

**Workflow matadero**:
1. Engineer search con criteria filter (LatAm Spanish, female 35-55, warm cozy, NO breathy)
2. Top 3 candidates → 1s sample c/u del texto canónico ("Probá el caldo. Solo una cucharada.")
3. Architect listens 3 samples → picks → engineer commits

**Cost**: ~$0.05 sample test
**Lesson**: criteria filter del architect (Q1 verdict) es CRÍTICO — engineer NO debe arrancar search sin architect criteria explícito

### 4.2 SPEC math tension (Path A/B/C decision)

Pattern: SPEC puede tener targets matemáticamente inconsistentes entre fields.

**Caso matadero**:
- SPEC L212 `target_total_duration`: 87s
- SPEC L213 `target_speaking_wpm`: 165
- SPEC L214 `target_total_words_estimated`: 193
- Math: 193 / 165 × 60 = 70.2s + pauses ≈ 78.8s. Vs sum per-segment 89.30s. Vs top-level 87s. **3 targets conflicting**.

**Engineer choice**: fit a sum-based per-segment target_duration_s (89.30s real) → WPM drops to 139.9.

**3 paths**:
- A. Accept current ("slow contemplative tone" per INGENIERO-PAUTA § 1.6)
- B. Reduce target_s per segment (rompe architect rhythm)
- C. Add words to script (architect creative change)

**Architect verdict**: Path A. **Auditor concurrence**: ✅ (per hard rule #19 INGENIERO-PAUTA priority + SPEC-level explicit target preserva over generic default).

**Lesson**: SPEC math tensions deben detectarse en architect Q audit DURING design, no descubrirse en CP2 ejecución. Forward → architect SPEC audit checklist debería incluir "math coherence target_duration vs WPM vs word_count".

### 4.3 Per-segment atempo (engineer fix autónomo vs uniform)

Pattern: uniform atempo (e.g. 2.3x for all segments) puede romper per-segment SPEC target_duration_s. Engineer fix autónomo: per-segment atempo = raw_duration / target_duration, clamped [0.7, 2.5].

**Authority**: hard rule #19 (INGENIERO-PAUTA § 1.7 autoritativa) + SPEC per-segment target_s explicit.

**Auditor verdict**: ✅ CONCUR — per-segment respeta architect rhythm intent + maintains visual sync downstream CP4.

### 4.4 Caption text override (Whisper vs SPEC ground truth)

Pattern: Whisper-small ES mispronounces specific words (voseo argentino, proper nouns, accent words). Engineer override visible caption text con SPEC narration_script ground truth WHILE preserving Whisper timestamps for sync.

**Caso matadero**:
- Whisper transcribed: "matarífe" / "vacillo" / "vita" / "6"
- SPEC ground truth: "matarife" / "pasillo" / "vida" / "seis"
- Override: `captions.json` retains both `whisper_text` (raw) + `spec_segment_id` (SPEC text link). CP5 visual layer uses SPEC text via spec_segment_id.

**Authority**: memoria `feedback_qa_gates_and_audits.md` canonical pattern.

**Lesson**: Whisper para TIMING, SPEC para VISUAL TEXT. Re-Whisper con `medium` model NO resuelve raíz (Whisper allá nunca matchea SPEC voseo exact).

### 4.5 Matarife voice processing chain (ffmpeg approximation)

Pattern: SPEC prescribe heavy effects chain (pitch shift + flanger + LPF + reverb + distortion). ffmpeg approximates vía `rubberband + flanger + lowpass + aecho`.

**Risk**: ffmpeg `aecho` NO es industrial_metallic reverb proper. Fallback documented: SoX → Audacity manual → Logic DAW → RVC voice cloning local.

**Authority architect (Q3 CP2)**: CAVEAT — test SPEC L1385 ("voz aislada NO-humana pero entendible") en TODAS las 3 matarife segments per-segment, NO average pass.

**Lesson**: complex effects chains via ffmpeg viable como first-attempt + fallback documentado. Per-segment validation OBLIGATORIA (no average).

---

## 5. Post-handoff structure (engineer)

**File**: `<proyecto>/CP2-POST-AUDIT-handoff.md`

**Required deliverables**:
- N TTS files per segment in `assets/tts/`
- `full-narration.mp3` concatenated con SPEC pauses
- `manifest.json` per-segment timing + WPM + speaker + paths
- `captions.json` Whisper post-processed + 3-class system + keyword_highlights + staccato_climax

**Required measurements**:
- WPM per segment + overall (vs INGENIERO-PAUTA p25-p75)
- Coverage % narration / total (≥85% p25 canónico)
- Total duration vs SPEC target (delta)
- Voice processing per-segment status (SPEC L1385 criteria check)

---

## 6. Post-gate auditor checklist

| # | Item | Method |
|---|------|--------|
| M1 | WPM measurement methodology consistent | Re-derive WPM independent vs engineer's |
| M2 | Coverage ≥85% | Sum speaking / total duration |
| M3 | 3-class caption system applied | Spot-check captions.json |
| M4 | 15 keyword_highlights tagged | Count vs SPEC L1413-1428 |
| M5 | 3 staccato_climax detected | SPEC L1429 verbatim |
| M6 | Consequence framing marks branch (acción/choice/nombre, NOT bare label "Si elegiste A") | Grep narration_script audio (via captions text) |
| M7 | Caption text override pattern correct | Schema check `whisper_text` + `spec_segment_id` |

---

## 7. Post-gate architect checklist

**TODO architect**. Auditor stub:
- Cocinera voice picked sounds adequate vs SPEC L1395 ("warm humana cálida")
- Matarife voice processed sounds NO-humana per SPEC L1385
- Per-segment narrative pace feel match architect rhythm intent

---

## 8. CP closure

**as_built annotation schema** (validated matadero `pace_decision_path_A_2026_05_17`):

```yaml
pace_decision_path_<A|B|C>_<date>:
  decision: "<one-line>"
  architect_concurrence: true
  auditor_concurrence: true
  auditor_questions_resolved: [A1, A2, A3, ...]
  cp2_metrics_actualized:
    duration_s: <X.XX>
    coverage_pct: <X.X>
    overall_speaking_wpm: <X.X>
    target_wpm_p25_floor: 153
    target_wpm_median: 165
  rationale: "<reasoning + authority>"
  engineer_fix_autonomo_accepted: "<description>"
  open_items: [list forward to next CPs]
  cost_cp2_usd: <X.XX>
  cumulative_project_usd: <X.XX>
  decision_at: <YYYY-MM-DD>
```

---

## 9. Sub-patterns matadero-banquete CP2 (concrete examples)

### Path A/B/C aplicado

**WPM math tension** → Path A accepted (slow contemplative tone). Architect concurrence + auditor concurrence in-SPEC L579-603.

### Test-first

**NO usado en CP2** — TTS commit fue post-architect-pick-from-3-samples (que es similar to test-first en spirit).

### Procedural violations

Ninguna detectada en CP2 matadero.

### Re-handoff cycles

| Handoff | Razón |
|---------|-------|
| PRE → execute | Architect Q1-Q5 verdicts + Auditor A1-A6 verdicts entregados → no re-handoff |
| Execute → POST | TTS pipeline executed end-to-end |
| POST → closure | Architect Path A verdict + auditor concurrence → as_built block in-SPEC |

---

## 10. Open issues forward

| # | Issue | Forward CP |
|---|-------|-----------|
| 1 | Matarife per-segment listen test SPEC L1385 — engineer TODO pre-CP4 | CP4 lip sync |
| 2 | Cocinera voice Valeria → shot_20 CP4 voice continuity (Path B deferral active) | CP4 |
| 3 | Hard rule #10 docs/OPERATING-MANUAL.md "atempo 2x" debería actualizarse → 2.3x measured | Sprint separado architect-domain |

---

## 11. Métricas observadas matadero-banquete CP2

| Métrica | Valor |
|---------|-------|
| Segments target | 19 |
| Segments generated | 19/19 (one reused from sample A) |
| Cost real | $0.45 |
| Time real | ~20 min (Whisper transcribe el slowest) |
| Voice IDs activos | 3 (narrator default + matarife=narrator+effects + cocinera Valeria) |
| WPM overall | 139.9 (under p25 153, accepted Path A) |
| Coverage | 90.2% (≥85% ✓) |
| Duration | 89.44s (vs SPEC sum-based 89.30s, Δ +0.14s) |
| Caption entries | 33 (Whisper segments) |
| Keyword highlights | 33 hits across 30 captions |
| Staccato climax | 3/3 detected |
| Path B/C aplicados | 1 Path A (WPM tension) |
| Procedural violations | 0 |
| Re-handoff cycles | 0 (PRE → execute → POST direct) |

---

## 12. Lessons learned codified (updated post-CP2 acoustic refutation 2026-05-18)

1. **SPEC math tensions** entre 3 fields (duration / wpm / word_count) deben detectarse en architect Q audit DURING design, NO descubrirse en CP2 execute. Forward: agregar "math coherence check" a architect SPEC audit checklist.
2. **Per-segment atempo > uniform atempo** cuando SPEC tiene per-segment target_s explicit. Engineer fix autónomo defendible per hard rule #19. **PERO** debe respetar target WPM canónico — per-segment atempo dropped WPM unintentionally en matadero. **Per-speaker atempo** puede ser mejor approach (narrator vs character voices con effects chain compounding).
3. **Whisper para TIMING, SPEC para TEXT** — engineer override approach canonical.
4. **Voice ID search con architect criteria filter** es Q1 architect verdict CRÍTICO — engineer no arranca sin criteria explícito.
5. **Per-segment validation matarife voice** NO average pass — caveat architect Q3.
6. **WPM measurement methodology RESOLVED 2026-05-18**: canonical `measure_F1.py` methodology = `words / sum(Whisper segment durations)`. Engineer manifest methodology = `words / out_duration_s` (similar). **AMBOS incluyen intra-segment pauses**. Apples-to-apples vs canon p25-p75 [152.71, 179.84]. Matadero hit 125.62 (Whisper) / 139.9 (manifest) — both well below p25. Pace IS slow, NO artifact methodology.
7. ⭐ **ACOUSTIC PROGRAMMATIC VERIFICATION OBLIGATORIO CP2 audit** (caso disparador matadero 2026-05-18): auditor debe correr `measure_F1.py` methodology sobre TTS Whisper output ANTES de emit verdict CP2. Comparison vs canonical bands automated. NO human-in-loop. Codificado en `AUDITOR-PROTOCOL.md` § 3 CP2 punto 7 (M7).
8. ⭐ **Effects chain compounds atempo lag** — matarife (pitch shift + flanger + LPF + aecho + atempo) ended 119.5 WPM vs narrator (same voice + atempo only) 143 WPM. Forward: cuando voice tiene effects chain, atempo target debe compensar lag adicional (~10-15% más agresivo).
9. ⭐ **Path A "slow contemplative" defense NO viable si pace <p25 floor 152.71** — PAUTA § 1.6 admite 153-165 "slow horror" pero NO sub-p25. Matadero 125-143 está debajo de slow tier. Path A en este caso era engineering rationalization de un problema técnico real.
10. ⭐ **Volume meter ≠ intelligibility — M7.7 codified post matarife inaudible (2026-05-18)** — Caso disparador: matarife post-Oxley voice swap volume mean -21 dB (HIGH measured) pero user listen "no se escucha nada" porque LPF 2000Hz cortó consonant articulation (frequency range 2-8kHz) + aecho out_gain 0.3 drown dry signal. M7 PACE PASS aunque intelligibility destroyed. Lesson: speech intelligibility canonical compliance NO reducible a volume meter — requiere **Whisper re-transcribe processed audio + match SPEC text ≥0.90 ratio**. Codified AUDITOR-PROTOCOL § 3 CP2 M7.7. **Plus pattern observado**: short segments (<2s) + heavy effects chain compound destroy articulation (matarife_count "Veinte minutos" 1.5s went to 0.00 intelligibility, while matarife_exit 2s 1.00). Forward: per-segment effects chain calibration (lighter for shorter segments) o re-render con slower delivery + lighter chain.
11. ⭐ **Voice ID library validation against canonical refs OBLIGATORIO (not our productions)** — Caso disparador matadero CP2 Tj9l48J9 voice ID. Validated_in solo nuestras producciones V7 + bosque v1 = our-prod-validated. Real canonical = LatAm energetic conversational narrators (8 viral refs horror-choice). Replaced con Oxley Evil Character `2gPFXx8pN3Avh27Dw5Ma` post user listen pick. Lesson codified docs/OPERATING-MANUAL.md hard rule #19 expansion + canonical_validation_status field obligatorio library entries. Forward: measure-canonical-per-speaker.py Phase 1 priority — diarization per-speaker bands derived from canonical refs, voice IDs must match measured bands programmatically.

---

**Última actualización**: 2026-05-18 (post-CP2 matadero closure)
**Próximo update**: 2do video del formato → validation methodology WPM + voice processing patterns
