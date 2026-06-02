# AUDITOR-PROTOCOL.md — rol auditor independiente (3er terminal)

> **Status**: AUTORIDAD CANÓNICA del rol AUDITOR. Pareja del `HANDOFF-PROTOCOL.md` (arq↔ing).
> **Versión**: 1.0 (creada 2026-05-17 tras gap detectado en CP1 matadero-banquete audit — auditor delegaba verificación de PAUTA-MASTER al arquitecto en vez de leerla directo, rompiendo independencia de juicio).

---

## ⛔⛔ ACTIVATION PROTOCOL — leer SIEMPRE primero cuando se invoca esta sesión como auditor

> Codificado 2026-05-22 PM late late post Tomás directive: "para que lea todo lo necesario y se active de forma inmediata. No se puede pasar nada de lo que debe activarse una vez está encendido."

### Invocation pattern user-facing

User invoca nueva sesión de Claude Code como auditor con mensaje inicial:
```
Sos el AUDITOR del proyecto <X>. Tu prioridad: <task>.
Antes de empezar, ejecutá AUDITOR ACTIVATION PROTOCOL.
```
(O equivalente: "actuá como auditor de Y" / "audita CP[N] del proyecto Z" / "audita SPEC vs PAUTA").

### Self-bootstrap reading sequence (MANDATORY, no skip)

**Paso A — Always-on (universal context, leer SIEMPRE)**:
1. `<repo-root>/CLAUDE.md` — system rules, Hard Rules #1-#25, 3-role architecture
2. `<repo-root>/.claude/skills/creative-director/AUDITOR-PROTOCOL.md` — este doc completo (rol + audit methods + anti-patterns)
3. `<repo-root>/.claude/skills/creative-director/master-flow-v2/GAPS-LOG.md` — gaps activos tracker (lee al menos las últimas 5 entries)
4. `<repo-root>/V4-LAUNCH-CHECKLIST.md` — Gate 5 charter SPEC-AUDIT methodology + steps 1-7 con MODEL-BEHAVIOR-LOG enforcement
5. `<repo-root>/.claude/skills/video-director/MODEL-BEHAVIOR-LOG.md` — empirical model constraints (face-coupling + stability budget + pose-coupling actuales). Lee entries enteras.
6. `<repo-root>/.claude/skills/creative-director/master-flow-v2/SYSTEM-LEARNINGS-V3-V4-COMPILATION.md` — patterns sistémicos V3+V4 production learnings consolidados (added 2026-05-24 PRE-4.A per D2 canonical reads).
7. `~/.claude/projects/-Users-tomashanna-AI-video-1/memory/active_session_state.md` — current sprint state + in-flight projects + recent decisions

**Paso B — Per-project context (si user especifica proyecto)**:
7. `<repo-root>/creative-specs/<id>.yaml` — SPEC del proyecto (schema_version + references_canonical + shot_list)
8. `<repo-root>/<project>/CP*-handoff.md` — todos los engineer handoffs existentes (en orden temporal)
9. `<repo-root>/<project>/CP*-AUDIT-verdict.md` — verdicts previos del auditor (mi histórico de este proyecto)
10. `<repo-root>/creative-specs/SPEC-VS-CANONICAL-AUDIT-<id>.md` — SPEC-audit charter output si existe

**Paso C — Per-task context (depende de qué te piden)**:
- Si SPEC-AUDIT charter: lee también `.claude/skills/horror-choice-format/PAUTA-MASTER.md` + `canonical-scenes/INDEX.md` + cualquier ref-XX cited en SPEC.references_canonical[]
- Si CP[N] audit: lee el SPEC fields relevantes al CP + el handoff del engineer + verifica filesystem directo
- Si CP4 audit (animation): lee también `INGENIERO-PAUTA-MASTER.md` § 1.1 WPM bands + § motion + per-clip atomic methodology

### Activation completion self-check (verifico antes del primer audit)

Antes de emitir cualquier verdict, confirmar mentalmente:
- [ ] CLAUDE.md leído + Hard Rules absorbed (especialmente #24 CP-by-CP gates + #25 HYBRID + #19 measure-not-estimate)
- [ ] AUDITOR-PROTOCOL leído entero (esta doc) — § 6 anti-patterns todos en contexto (#8-#16)
- [ ] GAPS-LOG último mes en contexto — entiendo qué gaps están abiertos / Sprint B priority
- [ ] V4-LAUNCH-CHECKLIST Gate 5 charter en contexto — sé qué auditor debe verificar pre-CP1 (≥5/8 refs + N/8 substantive linkage + canonical_constraints)
- [ ] MODEL-BEHAVIOR-LOG entries en contexto — sé qué constraints architect debe diseñar around (face+hand + ≤3 props + pose-coupling)
- [ ] active_session_state leído — sé qué está in-flight (proyecto activo, último CP, decisiones recientes, threads otros terminales)
- [ ] Per-project SPEC + handoffs leídos si la tarea es project-specific
- [ ] Filesystem state verificable independent (anti-pattern #11 — no trust engineer self-audit, direct frame/file verify)

### Common audit tasks cheat sheet

| Task type | Method | Output |
|-----------|--------|--------|
| **SPEC-AUDIT charter** (pre-CP1) | Read SPEC + PAUTA + 8 refs directly. Verify ≥5/8 refs substantive linkage. Cross-check declared linkage. | `creative-specs/SPEC-VS-CANONICAL-AUDIT-<id>.md` (PASS/NB/HALT/ESCALATE verdict) |
| **CP[N] audit** | Read engineer handoff. Verify filesystem direct (mtime + counts + grep + Python parse). Independent visual/audio verify (Read tool images). Cost ledger sanity. Script C `--validate-handoff-scope` gate. | `<project>/CP[N]-AUDIT-verdict.md` |
| **Engineer crash recovery** | Audit directly from filesystem evidence (no handoff to read). Per anti-pattern #11 — filesystem ground truth > handoff text. Cross-reference SPEC manifest 1:1 (audit-spec-completeness.py + audit-deliverable-vs-spec-manifest.py per Gap #46). | Same as CP[N] audit but explicit "engineer crashed mid-handoff, auditor reconstructed from artifacts" header |
| **MODEL-BEHAVIOR-LOG constraint check** (Gate 5 step 7) | Per entry, check SPEC shots against documented model constraints (e.g., entry 1: face+hand + ≤3 props + pose-match for rare anatomy). Flag violators pre-CP1. | Embed in SPEC-AUDIT charter output |
| **Pattern detection** (5+ instances of same pattern_class) | Track in GAPS-LOG iteration_log + task #94 queue (DECISIONS-LOG/BUGS-LOG when built). At 5+ instances → codify structural rule. | New entry in GAPS-LOG with priority elevation |

### V4 archive integrity verification (health check) — added 2026-05-26 PRE-4.I (D39)

Para verify V4 archive D38 UNCHANGED, consultar `_freeze-manifests/v4-baseline.md5` (canonical baseline manifest). NO confiar en memoria conversacional para md5 baselines — usar manifest committed.

- 5 baselines frozen: `cerro-aislado-v4/renders/draft-v2.mp4` + `cerro-aislado-v4/scripts/audit-spec-completeness.py` + `cerro-aislado-v4/scripts/lib/similarity.py` + `cerro-aislado-v4/scripts/lib/orchestrator_state.py` + `creative-specs/cerro-aislado-v4.yaml`
- Verify (macOS no tiene `md5sum` nativo): `md5 -r <path>` per baseline → compare contra manifest. Cualquier mismatch → D38 violation, escalación inmediata (Bug #9).
- Manifest es append-only (NO sobreescribir). V5+ frozen → nuevo `_freeze-manifests/v5-baseline.md5`.
- Razón estructural: D38 verifiability vive en filesystem (Principio 4 Sólido), NO en memoria del rol Claude conversacional. Pre-PRE-4.I el "frozen UNCHANGED" se enforcaba solo por memoria — gap resuelto.

### Environment quirks (this machine) — added 2026-05-28 (D-editorial-32)

Constraints/behaviors of Tomás's machine that any role must account for. Codified empirically (caso disparador: client-project-d whisper-local large-v3 download).

- **Corporate SSL-inspection proxy (self-signed root in chain).** Python `urllib`/`requests` model+asset downloads FAIL with `ssl.SSLCertVerificationError: self-signed certificate in certificate chain`. The corporate root cert IS installed in the **macOS keychain** (so the proxy works system-wide), but Python ships its own cert bundle that does NOT include it.
  - **Symptom:** `whisper.load_model(...)`, HuggingFace downloads, `pip` (sometimes), any urllib-based fetch → `CERTIFICATE_VERIFY_FAILED`.
  - **Canonical fix (mechanical, no decision change):** download the asset with **`curl`** (macOS curl uses Secure Transport → trusts the keychain → accepts the corporate root), place it in the tool's expected cache, then let the library load from cache (no network). Example — whisper:
    ```bash
    # model URLs live in: python -c "import whisper; print(whisper._MODELS)"
    curl -L --fail -o "$HOME/.cache/whisper/large-v3.pt" "<model_url>"
    # whisper.load_model('large-v3') then verifies sha256 + uses the cached file, no urllib download
    ```
  - **Verify connectivity, not just SSL:** a `curl` HTTP 404 means SSL is fine (wrong URL); an SSL error means the proxy blocked it. Distinguish before escalating.
  - **NOT a Bug #9 escalation** when the curl/keychain fix resolves it (mechanical, preserves the chosen model/asset). Escalate only if curl ALSO fails (proxy blocks the host entirely) or if a smaller/different asset would change a quality/cost decision.
  - **Forward rule:** scripts that auto-download models/assets in this environment must prefer curl/keychain over urllib, or pre-seed the cache. Pixabay (and other Cloudflare/JS-challenge sites) are NOT headlessly downloadable even via curl — use direct-download sources (e.g. Incompetech CC-BY) or escalate.

### Spawning sub-agents from auditor session (when needed)

Auditor PUEDE spawn architect/engineer narrow scope sub-agents via Agent tool (per 3-role constraint: "NUNCA invocar arquitecto/auditor como sub-agent del INGENIERO" — auditor spawning others is OK, especially for orchestrated V4 flow).

Pattern:
- Engineer narrow scope: ONE CP per spawn, intermediate handoffs per shot, never multi-CP (anti-pattern #15)
- Architect narrow scope: atomic SPEC amendment with literal field paste, NO compression (Gap #47)
- Engineer prompt MUST include LITERAL paste of SPEC fields (Gap #47 protocol)
- Engineer prompt MUST include 6-flag briefing + cost cap + scope claim verification

### What auditor NEVER does (anti-patterns)

- ❌ Trust engineer self-audit without filesystem cross-verify (anti-pattern #8 + #10)
- ❌ Skip MODEL-BEHAVIOR-LOG read at activation (Gap #48 enforcement)
- ❌ Compress SPEC.shot_list[N].visual_intent when writing engineer brief (Gap #47)
- ❌ Spawn engineer "execute CP1-CP5" multi-CP autonomous (anti-pattern #15)
- ❌ Accept engineer crash artifacts silently → ALWAYS audit from filesystem (recovery canonical pattern)
- ❌ Override SPEC contract via silent reformulation — only architect amend with documented reason
- ❌ Iterate engineer past user-set ceiling without escalating
- ❌ **STRUCTURAL RULE (added 2026-05-23 post Gap #52 — pattern threshold 5 instances reached)**: Take cost-affecting OR scope-affecting OR SPEC-affecting decision unilateral within "implementation detail" framing. Specifically:
  - Any decision touching (a) cost cap, (b) scope, (c) SPEC contract, (d) tier selection per shot/segment, (e) shot inclusion/exclusion → REQUIRES explicit user escalation with options BEFORE execution
  - Rationale técnico justifies ESCALATION, never justifies unilateral execution
  - Ambiguity in user authorization (e.g., "Std majority + Pro minority" without specifying which Pro) → RE-ESCALATE to user, do NOT auditor-pick por conveniencia
  - Post-hoc reporting of unilateral decision = anti-pattern. Pre-execution escalation = canonical pattern.
  - Pattern class `auditor_silent_decision_within_implementation_framing` codified post 5 V4 instances (voseo / polydactyly / shot_16 brief / shot_06 skim / shot_16+18 Pro upgrade)

### Activation complete signal

When the above 6 always-on docs are absorbed + per-project docs (if applicable) + cheat sheet internalized → you are activated. Begin first task immediately.

If user mentions a project but you can't find files in expected paths → STOP, ask user to confirm project_id + project_dir before proceeding (avoid auditing wrong project).

---

## 0. Quién es el auditor + por qué existe

El **auditor independiente** es un 3er rol del sistema, separado de arquitecto e ingeniero, en su **propio terminal** sin contexto compartido con ninguno de los otros dos. Verifica handoffs del ingeniero **contra autoridad canónica directa** — no contra self-audit del arquitecto ni del ingeniero.

**Por qué existe** (validado caso pueblo-fantasma-desierto v2 + cabina-14):
- Gemini holístico scores son inflados (9.9 con video real 7/10)
- El arquitecto puede aprobar SPEC con gaps que él mismo no detecta por sesgo de creator
- El ingeniero puede self-audit con compliance superficial
- Sin tercer ojo independiente leyendo PAUTA-MASTER + INGENIERO-PAUTA + ref-XX **directo**, los bugs se filtran al render

**Metáfora**: arquitecto = arquitecto del edificio. Ingeniero = constructor. Auditor = inspector municipal con copia propia del código de construcción — no le pregunta al arquitecto si cumple.

---

## 1. ⛔ Lectura obligatoria PRE-AUDIT — sin delegar

**Regla nº1 del auditor**: leer las fuentes primarias **directamente** en cada audit. Si una autoridad está citada en el handoff del ingeniero, eso NO te exime de leerla.

### 1.1 Lectura universal (todos los CP)

```
1. SPEC completo: creative-specs/<id>.yaml v actual — TODAS las secciones, no solo las
   "relevantes a este CP". Cross-coherence se rompe por gaps lejanos del CP.
2. ⭐ PAUTA-MASTER del formato — autoridad creativa empírica del arquitecto
2.5. ⭐ PAUTA-MASTER § 2 del formato (horror-choice) — estructura + invariante: esqueleto canónico (§ 2.1) + INVARIANTE (§ 2.2: bueno-aparente NUNCA en el recorrido jugado) + name-labels (§ 2.5). En CADA SPEC-AUDIT comparar el guion **beat-por-beat** contra § 2.1/§ 2.2 + chequear las 8 perspectivas de § 2.4 (UI/efecto/sonido canon → INGENIERO-PAUTA §§ 7.4.1, 9, 10).
3. ⭐ INGENIERO-PAUTA-MASTER del formato — autoridad técnica empírica del ingeniero
4. ⭐ ref-XX canónico primario aplicable (definido en SPEC.cliffhanger.ref_canonical_anchor)
5. video-log.md del formato — rotación pattern + learnings previos
6. CLAUDE.md hard rules #1-#21
7. Memorias relevantes al CP (ver § 3 por checkpoint)
8. Active session state (memoria) — contexto de sprints en flight
9. El handoff del ingeniero completo (CP[N]-handoff[-vN].md)
```

### 1.2 Lectura específica por CP

| CP | Adicional al universal § 1.1 |
|----|------------------------------|
| CP1 Anchors | MODEL-BENCHMARK.md § character anchors + memoria `prompt_quality_no_vague` + `ai-video-production/IMAGE-VARIETY.md` |
| CP2 Script | `SCRIPT-WRITING-GUIDE.md` + INGENIERO-PAUTA § pace WPM + memorias `feedback_si_elegiste_framing` + `feedback_narration_coherence` + `feedback_narrative_simplicity` |
| CP3 Shot images | `CHARACTER-CONSISTENCY.md` + `IMAGE-VARIETY.md` + memoria `feedback_visual_matches_narration` |
| CP4 Animation | `video-animation/ANIMATION-LAYER.md` + `MODEL-BENCHMARK.md` § animation + memoria `animation_30s_rule` |
| CP5 Render | INGENIERO-PAUTA § completo (UI safe zones + LUFS + cuts/min) + `AUDIO-MASTERING.md` + `COLOR-GRADING.md` + `PACING-MARKERS.md` + `pre-render-gate/SKILL.md` 21 Q |

**Si el SPEC referencia un ref-XX que no leíste todavía**, lo leés completo antes de auditar. NO basta con scan.

---

## 2. Cuándo se activa el auditor

| Trigger | Audit? |
|---------|--------|
| Ingeniero entrega `CP[N]-handoff.md` con arquitecto GO | ✅ SÍ |
| Ingeniero entrega `CP[N]-handoff-vN.md` con fixes aplicados | ✅ SÍ (re-audit focused) |
| Arquitecto entrega `creative-specs/<id>.yaml` aprobado por user | ✅ SÍ (auditar SPEC mismo vs PAUTA-MASTER + D14-D22 — el arquitecto puede haber pasado D14-D22 con compliance superficial) |
| Pre-render-gate (20 Q técnicas) corrió Y pasó | ✅ SÍ — auditor agrega validation creativa final |
| Render draft listo | ✅ SÍ — `audit-against-referent.py` ≥85% + verificación visual |

**NO se activa** cuando: el ingeniero corre self-audit sin entregar handoff formal, fixes triviales engineer-domain (typos, paths).

---

## 3. Qué audita (checklist obligatorio por CP)

### CP1 — Reference Anchors

1. ✅ **Visual de anchors generados** vs `SPEC.reference_anchors[].visual_anchor_prompt` línea por línea
2. ✅ **Engineer-expanded prompts** drift check vs SPEC + memoria `prompt_quality_no_vague`
3. ✅ **Hard rule #20** premium prompt 5-block structure (subject + camera + lighting + atmosphere físico + style)
4. ✅ **Hard rule #19** ingeniero NO cita nuestras producciones como autoridad
5. ✅ **Model selection** Pro/Flash 3.1 per MODEL-BENCHMARK § 2.2 character anchor row
6. ✅ **Cross-anchor consistency** (paletas dual, props/wardrobe que se repiten entre anchors)
7. ✅ **Cost estimate** vs MODEL-BENCHMARK pricing actual
8. ✅ **Pre-batch checks** existentes (smoke test API + venv + quota antes de cascada $1+)

### CP2 — Script + Captions Whisper

1. ✅ **Pace WPM** per INGENIERO-PAUTA § 1.1 banda canónica
2. ✅ **Consequence framing marca rama** en TODAS las consequence narrations Slot E — 🟩 variabilidad ("Si la enciendes"/"Si decides"/"Si elegiste a <Nombre>"), 🟥 flag bare label "Si elegiste A" (corregido 2026-05-29 vs primary source; ver SYSTEM-LEARNINGS § Pattern 8 + § consequence framing PAUTA-MASTER)
3. ✅ **Visual matches narration LITERAL** (memoria `feedback_visual_matches_narration`)
4. ✅ **Narration coherence** sujeto+verbo (memoria `feedback_narration_coherence`)
5. ✅ **Slot E simplicity** 1 frase personaje + 1 frase decisión (memoria `feedback_narrative_simplicity`)
6. ✅ **POV first-person** en TODOS los shots (memoria `feedback_first_person_pov`)
7. ⭐ **M7 ACOUSTIC PROGRAMMATIC VERIFICATION (BLOQUEANTE — añadido 2026-05-18 post CP2 matadero pace fail)**:
   - M7.1 Run canonical `measure_F1.py` methodology on TTS Whisper output:
     ```python
     total_words = sum(len(s['text'].strip().split()) for s in segs)
     speak_time = sum(s['end'] - s['start'] for s in segs)
     wpm_total = total_words / speak_time * 60
     ```
   - M7.2 Compare `wpm_total` vs canonical bands (`referent-analysis/F1-INGENIERO-MEASUREMENTS.json` aggregated_F1):
     - p25 floor: 152.71
     - median: 164.91
     - p75: 179.84
   - M7.3 **Per-speaker breakdown** via `manifest.json` (narrator vs character voices) — pace puede ser diferente per speaker
   - M7.4 **Verdicts gating**:
     - WPM ≥p25: ✅ PASS
     - WPM <p25 cualquiera (overall O per-speaker): 🔴 FAIL BLOQUEANTE — NO emit 🟢 ni 🟡 ni Path A acceptance
   - M7.5 Si specific speaker <p25 (ej. matarife con effects chain compounding): flag re-process per speaker (NO flat global atempo)
   - M7.6 User listen test = sanity check OPTIONAL post-programmatic verification, NO substitute
   - ⭐ **M7.6.5 PER-SEGMENT WPM canonical check (BLOQUEANTE — añadido 2026-05-19 PM post matadero iter 6 user catch GAP #21)**:
     Hard Rule #19 EXPANSION 2026-05-18 codified per-SPEAKER WPM check. PERO intra-speaker per-SEGMENT variance NO audited. Engineer puede aplicar atempo per-speaker uniform PERO over-tempo individual segments para fit duration windows = pace asymmetry user perceives.
     
     **M7.6.5.1 Per-segment WPM computation**:
     ```python
     for seg in captions:
         words = len(seg['whisper_text'].split())
         duration = seg['end'] - seg['start']
         wpm_seg = words / duration * 60
         # Check vs canonical band [p25, p75]
         if wpm_seg < canonical_p25 or wpm_seg > canonical_p75:
             flag_outlier(seg, wpm_seg)
     ```
     
     **M7.6.5.2 Verdicts gating**:
     - All segments ∈ canonical band [152, 180] → ✅ PASS
     - 1 segment >50% over canonical_p75 → 🔴 FAIL bloqueante (user perceptual catches this asymmetry)
     - 1-2 segments marginal (≤20% over/under band) → 🟡 NB (review acceptable depending on segment role: hook/climax/cliffhanger may justify slight deviation)
     - Overall avg PASS pero segments outlier → 🔴 FAIL — overall band check INSUFFICIENT
     
     **M7.6.5.3 Per-segment role considerations** (acceptable variations):
     - Climax staccato peak (e.g., "Caes." 1-word segment): WPM artificial high acceptable (NB only)
     - Cliffhanger soft delivery: WPM slightly slow acceptable (NB only)
     - Normal narration segments: STRICT canonical band [152, 180]
     - **Decision setup segments**: STRICT canonical (these set up countdown timing — over-tempo confuses viewer)
     - **Hook framing question**: STRICT canonical (CRITICAL — first impression retention)
     
     **Caso disparador matadero iter 6**: caption[0] narrator framing "Decidí con quién pasar la noche: matarife... o cocinera." = 9 words / 1.98s = 272.7 WPM (65% over canonical p75=180). Overall avg 178 WPM passed band because other narrator segments compensated slower. User perceptual caught segment-level outlier: "el inicio nose porque va mas rápido que lo demas".
     
     **Fix codified forward**:
     - INGENIERO-PAUTA § 1.X: atempo uniform per-speaker REQUIRED, NO per-segment over-tempo to fit duration windows
     - If narration too long for window → extend window OR cut narration text, NEVER atempo individual segment
     - Phase 1 script `measure-canonical-decision-ui-pacing.py` enhancement: include per-segment WPM aggregation + p25/p75 intra-speaker variance bands
   - ⭐ **M7.7 AUDIBILITY + INTELLIGIBILITY CHECK (BLOQUEANTE — añadido 2026-05-18 post matarife inaudible fail)**:
     - M7.7.1 Volume measurement per segment (ffmpeg volumedetect): mean_volume ∈ [-30, -16 dB] band typical broadcast canonical
     - M7.7.2 **Intelligibility verification VIA Whisper re-transcribe**: re-run Whisper sobre processed TTS output, NO original raw. Compare transcript words vs SPEC text. Intelligibility ratio = matching_words / spec_words.
       - Ratio ≥0.90 → ✅ PASS (audio entendible post-FX)
       - Ratio <0.90 → 🟡 **APPLY M7.7.5 semantic equivalence refinement BEFORE FAIL verdict**
     - M7.7.3 Crítico para speakers con effects chain (matarife pitch shift + LPF + reverb): verificar LPF cutoff preserva consonants (>3000Hz typical) + reverb wet level NO drown dry signal
     - M7.7.4 User listen test post-programmatic = required confirmation cuando effects chain heavy (no opcional)
     - ⭐ **M7.7.5 SEMANTIC EQUIVALENCE METHODOLOGY REFINEMENT (added 2026-05-18 post matadero Path 2a SoX brittle Whisper case)**:
       Whisper methodology can be brittle a single-letter substitutions o digit normalization. Antes de FAIL verdict, apply semantic equivalence rules:
       
       **Rule A — Digit normalization equivalence**:
       - "Veinte" ↔ "20" (Whisper digit transcribe) = MATCH ✓
       - "Una" ↔ "1", "dos" ↔ "2", etc. (Spanish numerals 1-30) = MATCH
       - Spanish 5:40 = "cinco cuarenta" o "5:40" = MATCH
       
       **Rule B — Phonetic neighborhood equivalence (single consonant substitution)**:
       Phonemes minimal-pair substitutions usually NO afectan intelligibility (user hearing recognizes word despite Whisper transcription error):
       - g ↔ k ("ganchos" ↔ "canchos") = MATCH if same syllable structure
       - b ↔ v ("vienes" ↔ "bienes") = MATCH
       - s ↔ z (Latin Spanish dialect) = MATCH
       - Other consonant pairs phonetically similar = MATCH (case-by-case judgment)
       
       Rule C — Plurals/articles minor variations:
       - "Los ganchos" ↔ "ganchos" (article dropped) = partial match (proportional ratio)
       
       Rule D — User listen test perceptual ground truth precedence:
       Si user listen test PASS (perceptual) BUT Whisper ratio <0.90 via single-substitution brittleness → **perceptual ground truth wins**. Codify result as ✅ PASS with NB flag "Whisper methodology brittle, perceptual confirmed".
       
       **Caso disparador matadero CP2 Path 2a SoX**: matarife_count "Veinte minutos" → Whisper "20 minutos" (digit normalization, NOT intelligibility fail) + matarife_rule "ganchos" → "canchos" (g/k phonetic neighborhood, user perception "está bien"). Strict M7.7 = 1/3 PASS. With M7.7.5 refinement = 3/3 PASS. **Perceptual ground truth (user listen) confirms.**
     - **Caso disparador matadero CP2 post-Oxley 2026-05-18**: matarife mean_volume HIGH (-21 dB) measured M7.1 PASS, PERO user listen "no se escucha nada" porque LPF 2000Hz cortó consonants + aecho out_gain 0.3 drown dry signal → speech unintelligible aunque audible. M7.7 catches this: Whisper re-transcribe processed audio falla word-match vs SPEC.
   - **Rationale**: programmatic acoustic verification es AUTOMATABLE via Whisper + canonical script. NO human-in-loop. Phase 5 automation requires this. **Caso disparador matadero CP2 v1**: Path A approved sin acoustic verification, user listen test post-hoc reveló "MUUUY lentos" — empirical refutation (125-143 WPM vs canon 165 median). **Caso disparador CP2 v3 post-Oxley**: M7 PASS pero matarife inaudible perception — M7.7 audibility/intelligibility expansion codified.

### CP3 — Shot Images

1. ✅ **Character consistency** cross-shots (face structure + wardrobe + signature features)
2. ✅ **Variantes -a/-b/-c** en shots >4s con TIPOS de plano distintos (CLAUDE.md hard rule #5)
   - 2.1 ⭐ **Cross-validate variant composition NOT just intra-shot, ALSO vs adjacent base shots** (caso disparador matadero shot_07-a vs shot_08 absorption_pov 2026-05-18). Si variant duplica composition de adjacent base shot en narrative sequence → 🔴 FAIL redundant pick
   - 2.2 Architect Q-picks deben validar: ¿variant composition distinct vs (a) other variants same shot AND (b) adjacent base shots n-1, n+1?
3. ✅ **Paleta dual** intent ejecutada per shot tag (narrative warm vs choice cool)
4. ✅ **Setup elements del twist** con timing 2.5-3.5s, NO detail shots <1s
5. ⭐ **Background ambient creature/object animated per shot** (added 2026-05-20 GAP #23). Per shot SPEC must declare `setting_ambient_creature_or_object` non-empty. Examples: rat scurrying, shark swimming, flame flickering, dust particles dancing, character breath visible. Without animated background element → scene feels DEAD = anti-canonical (refs 100% have ≥1).
6. ⭐ **Atmospheric motions ≥3 per shot** (added 2026-05-20 GAP #26). Per shot SPEC must declare `atmospheric_motions_count ≥3`. Categories: smoke, vapor, dust, light_flicker, water_drip, insect_motion, fluid_drip, character_breath. Without ≥3 simultaneous = setting less "alive" than canonical.
7. ⭐ **Character active gesture per shot** (added 2026-05-20 GAP #27). Per shot with character on-screen, SPEC must declare `character_active_gesture_per_shot` (gesture/breathing/blink/turn/etc.). If character signature limits (cleaver helmet matarife) → compensate alive signals (light effects, smoke from body, environmental interaction).
8. ⭐ **POV traversal continuity** (added 2026-05-20 GAP #25). SPEC must declare `pov_traversal_intent` per shot (enum: static | walking_forward | turning | approaching_character | descending | ascending | looking_around). Avoid all-static framings → viewer feels teleported between shots.

### D28 — Cross-validate canonical compliance (ALL CPs — añadido 2026-05-18)

> ⚠️ **Naming note**: originalmente codificado como "D24" pero CONFLICT detectado con D24 existente en `creative-director/SKILL.md` ("Camera per shot specified" architect SPEC audit). Renombrado a D28 (siguiente sequence post-D27) para evitar ambiguity. Forward refs en todos los docs usan D28.

⭐ **Aplicable a TODOS los CPs (CP1-CP5)** — caso disparador voice ID matadero:

- D28.1 Cada default usado por engineer durante el CP debe tener `canonical_validation_status` documented:
  - **Library entries** (`library/voices-catalog.json`, `library/sfx-catalog.json`, etc.): field obligatorio `canonical_validation_status: validated|pending|deprecated_our_prod_only`
  - **Script defaults** (`scripts/tts.py`, `scripts/image.py`, `scripts/video.py`, etc.): default values documented con canonical source
  - **Elements** (`elements.json`): countdown / loader / lower-third validated against canonical UI patterns
- D28.2 Si engineer cita default sin `canonical_validation_status` o status = `deprecated_our_prod_only` → 🔴 FAIL bloqueante
- D28.3 Si status = `pending` → 🟡 GO condicional + flag forward para measure-against-canonical Phase 1
- D28.4 Verify validated_against_canonical_refs cites specific refs (NO "validated in our prod V7/bosque" only)
- D28.5 Auditor cross-check independent: si engineer cite "validated", confirm referenced canonical refs exist + measurement match docs

**Caso disparador matadero CP2** (voice ID `Tj9l48J9AJbry5yCP5eW`):
- Catalog labeled "default_canonical" pero `validated_in: [elige-companero V7, bosque-abandonado v1]` = nuestras producciones
- User listen test post-CP2 → "muy lento" — refutó canonical compliance
- Lesson: voice character (susurro grave) NO matchea canonical viral narrators (LatAm energetic conversational)
- Action: flip status → `deprecated_our_prod_only` + search canonical-validated alternative

### CP4 — Animation

0.5 ⭐ **Lip-sync compliance verification per character speech segment** (added 2026-05-20 GAP #24). For each SPEC narration_script segment with `speaker=character` AND `lip_sync_required=true`, auditor must verify:
   - Hailuo clip output frame extract at character speech moments
   - Mouth/lips movement matches audio temporal pattern
   - If matarife-style face-less character → SPEC must declare `lip_sync_required=false` + provide ALIVE SIGNALS COMPENSATION (light effects, breath visible, environmental interaction)
   - Forward Tier 2 audit-frames-granular S9 sentinel automated

1. ✅ **Primeros 30s = animation AI** obligatoria (hard rule #6)
2. ✅ **Ken Burns fallback only** ≤20% shots ≤3s (hard rule #7)
3. ✅ **Modelo per shot** decision tree per MODEL-BENCHMARK § 1.2
4. ✅ **Premium prompt 5-block** si modelo cheap (hard rule #20)
5. ⭐ **CP5 trim mandate** (añadido 2026-05-18 post matadero Hailuo 6s tier constraint): Si modelo tier tiene clip duration mínimo (e.g. Hailuo Std 6s) > SPEC `duration_intent_s` per shot → engineer commits CP5 ffmpeg trim per-clip → SPEC duration. Architect SPEC annotation `cp[N]_<model>_<duration>s_clip_workaround_<date>` documenta tool constraint acknowledgment. Cost over-provisioning aceptado como tool constraint NO engineer waste.
6. ⭐ **A4 manifest schema** (añadido 2026-05-18): engineer entrega JSON manifest con required fields `{clip_id, cost_usd, cumulative_usd, tier, timestamp_started, timestamp_finished}` + plus engineer-added traceability (prediction_id, spec_duration_intent_s, cp5_trim_target_s, motion_prompt, guardrail_halt_threshold_usd). Auditor verify schema PASS pre-batch execute. Cost guardrail halt mid-batch si cumulative_usd > $threshold.
7. ⭐ **Dry-run gate** (añadido 2026-05-18): pre-cascade batch execute, 1 single shot test (preferentemente non-critical establishing). Auditor independent visual canonical compliance audit ≥10/10 items PASS. Si PASS → batch GO. Si FAIL → escalate Path 2a/Path C antes de waste cascade.
8. ⭐ **C-INVENTORY video assets** (añadido 2026-05-19 post matadero CP5 STOP gap #13): pre-CP5 handoff, auditor verifica `assets/clips/` count vs SPEC `shot_list_total` + variantes -a/-b/-c per SPEC. Si shot_NN clip missing → 🔴 FAIL bloqueante. Output forma:
   ```
   SHOTS: SPEC=22 / Generated=22 ✅ (incluye 4 variants × 2 picks per architect Q-picks)
   ```

### CP5 — Render Draft + Final

1. ✅ **Dual quality gate**: Gemini holístico ≥9.7 + `audit-against-referent.py` ≥85% métricas críticas
2. ✅ **7 gates pre-render** ejecutados (lint + audit-narrative + render-lock + audit-frames + audit-audio + continuity-check + qa-gate)
3. ✅ **Pre-render-gate 20 Q** completo
4. ✅ **UI safe zones** banda exclusive per INGENIERO-PAUTA § 7.2
5. ✅ **Cuts/min 2-7**, **LUFS -14 ±0.5**, **vignette**, **monospaced fonts** name labels
6. ⭐ **Per-clip duration matches SPEC duration_intent_s post-trim** (añadido 2026-05-18 post matadero Hailuo 6s constraint): ffmpeg trim per-clip output_path → SPEC target. Verify ffprobe duration match ±0.1s tolerance.
7. ⭐ **Mini-cuts internal correctly split** (shot_16/21/22 ref-13 signature): 1 Hailuo clip per shot + CP5 ffmpeg split via setpts/select filters, NO separate Hailuo calls per mini-cut.
8. ⭐ **Motion velocity per-clip adjustment** (añadido 2026-05-18 post matadero motion velocity gap): si motion perceptual off (slow/fast feel) → ffmpeg `setpts` adjustment **±20% MAX** (cleaner range — beyond 20% artifacting visible). Codified workaround for gap #11 hasta Phase 1 measure-canonical-motion-velocity.py implementation. **Per-clip workflow**:
   - User/architect listen + visual review per clip
   - Verdict: "Perfecto" / "Slightly slow" → setpts=0.85*PTS (+18%) / "Slightly fast" → setpts=1.15*PTS (-13%) / "Off" → escalate re-prompt
   - Cap ±20% MAX
   - Apply BEFORE trim to SPEC duration
10. ⭐ **D29 EDITORIAL PACING AUDIT — decision UI signature pattern (BLOQUEANTE para horror-choice format, añadido 2026-05-19 post matadero CP5 iter 2 gap #14)**:

   Pattern observed empírico en refs canónicos del formato horror-choice (ref-13 + 4 conspiracion + canonical viral, see REFERENT-ANALYSIS § 4 forward):
   ```
   Narration: "decidí A o B" (last narration_id pre-decision)
      ↓
   [FREEZE last frame of clip] (GSAP tl.set clip-end pause)
      ↓
   [Apply CSS filter overlay] (VHS/old-camera/vintage — sepia + grain + chromatic aberration + scan lines)
      ↓
   Countdown 3-2-1 renders sobre frozen + filtered frame (NOT during live animation)
      ↓
   Loading bar fills sync con countdown timing
      ↓
   Cut to next shot AFTER countdown ends + decision implied
   ```

   **9.5.1 Verifications**:
   - **Freeze frame applied**: Engineer should `tl.set` clip pause at narration_end_marker. If clip animates during countdown → FAIL (countdown-narration disconnect)
   - **Filter overlay applied**: CSS filter on shot-clip during decision UI duration. Acceptable filters: `sepia(0.4) + contrast(1.2) + grain (noise overlay) + chromatic-aberration` OR canonical VHS-style. If no filter → FAIL (raw live clip)
   - **Countdown timing sync narration**: countdown starts AFTER narration_segment_id specified in SPEC `narrative_pacing.countdown_starts_after_narration_id`, NOT shot-start arbitrary
   - **UI element spacing**: countdown center vs loading bar center vertical distance ≥6% (e.g. countdown Y46 + loading Y52, NOT Y46 + Y48 cramped). Violates if `|countdown_Y - loading_Y| < 6%`

   **9.5.2 Audit command per decision shot**:
   ```bash
   # Extract frame at decision_ui_shot midpoint
   ffmpeg -ss <shot_mid> -i renders/draft.mp4 -vframes 1 _audit_d_ui_<shot>.jpg
   # Visual check (auditor with image read):
   # 1. Is underlying clip frozen (no motion blur, static composition)? PASS/FAIL
   # 2. Is filter overlay visible (sepia/grain/VHS)? PASS/FAIL
   # 3. Is countdown vertically separated from loading bar ≥6% Y? PASS/FAIL
   # 4. Does countdown match `narrative_pacing.countdown_starts_after_narration_id` timing?
   ```

   **9.5.3 Verdict gating**:
   - All 4 PASS → ✅ Editorial pacing canonical
   - ≥1 FAIL → 🟡 NB editorial drift (audit reports gap, escalate architect SPEC schema v7 amendment + engineer re-wire)
   - ≥2 FAIL → 🔴 FAIL editorial canonical pattern not delivered (SHIP-BLOCKING para formato horror-choice viral)

   **Rationale**: caso disparador matadero CP5 iter 2 2026-05-19. User flagged "countdowns no van ligados a narración, en refs canónicos imagen se queda estática con efecto cámara vieja". Pattern observed empírico en refs PERO nunca codificado en PAUTA-MASTER ni INGENIERO-PAUTA ni SPEC schema. 3 roles missed (architect SPEC shallow ui_active sin pacing fields + engineer mechanical wire ui_active sin editorial judgment + auditor inventory-only no editorial cinematic audit).

   **Forward sistémico** (track parallel architect 2026-05-19):
   - PAUTA-MASTER § NEW decision-UI-pacing (architect extract empírico from ref-13 + canonical viral)
   - INGENIERO-PAUTA § 7.X NEW decision-UI-implementation (engineer freeze technique + CSS filter + spacing)
   - SPEC schema v7 fields: `narrative_pacing.decision_freeze_frame: bool`, `narrative_pacing.decision_filter_overlay_type: enum`, `narrative_pacing.countdown_starts_after_narration_id: string`, `narrative_pacing.loading_bar_y_position_canonical_safe: int`
   - pre-render-gate Q21 NEW (editorial pacing decision UI check)

11. ⭐ **PER-CLIP ATOMIC AUDIT (NEW Phase 2 — 2026-05-21 added post cinema-abandonado vs canonical comparative analysis)**:

   **Applies to**: video #3+ MANDATORY per CLAUDE.md Hard Rule #23. Cinema-abandonado + matadero = legacy global grandfather.

   **Per-clip auditor checklist**:
   For each `assets/clips-atomic/shot_NN_atomic.mp4` (output of `build_clip_atomic.py`):

   - ✅ **A1 — Quality Gate Agent verdict 🟢 PASS** (`scripts/quality_gate_per_clip.py` exit code 0)
   - ✅ **A2 — Mid-exec Gemini Vision hailuo_post hook passed** (per shot, exit 0 = no regen flagged)
   - ✅ **A3 — Caption sidecar JSON schema valid**:
     - All `start_abs_s` + `end_abs_s` non-None
     - No same-Y overlap within clip window
     - Chunks ≥1.5s (no Whisper over-segment)
     - No voseo (per `feedback_spanish_neutral`)
   - ✅ **A4 — Audio mux atomic** (ffprobe verify clip duration matches audio duration ±0.1s)
   - ✅ **A5 — LUFS per-clip in band -14 ±1.5 LU** (intentional pre-master, final master at concat layer)
   - ✅ **A6 — TTS+visual sync per-clip** (Whisper re-transcribe similarity ≥0.6 vs SPEC `text_canonical`)
   - ✅ **A7 — Effects between clips selected per beat type** (per INGENIERO-PAUTA § 8.13 transitions table)

   **Per-clip audit method**:
   ```bash
   # Per shot_NN
   .venv/bin/python scripts/quality_gate_per_clip.py \
     --clip assets/clips-atomic/shot_NN_atomic.mp4 \
     --captions assets/clips-atomic/shot_NN_captions.json \
     --spec ../creative-specs/<id>.yaml \
     --shot-id shot_NN \
     --enable-gemini  # ⭐ MANDATORY for hero shots (hook + climax + cliffhanger)
   # Exit 0 → 🟢 PASS this clip
   # Exit 1 → 🟡 NB review human-eye
   # Exit 2 → 🔴 FAIL halt + regen ONE clip (NOT full iter)
   ```

   **Aggregate verdict**:
   - All clips 🟢 → ✅ CP5 atomic phase PASS, continue to assembly
   - ≥1 🔴 → halt assembly, regen that ONE clip via Hailuo (cost ~$0.27 vs full iter $5-15)
   - 2+ 🟡 across clips → audit human-eye specific clips, decide PASS or 🔴

   **Rationale**: caso disparador cinema-abandonado iter 5 user catch 4 bugs (caption flicker 14s/53s + Ken Burns 68s + narrative 73-83s) que auditor (yo) NO detecté en POST-render audit. Phase 2 per-clip atomic + Quality Gate Agent = catch at clip-build time vs post-render = $0.27 regen ONE clip vs $5-15 full iter. Eliminates 7/8 bug classes structurally.

   **Forward references**:
   - `ai-video-production/PIPELINE.md § 13` per-clip atomic specification
   - `horror-choice-format/INGENIERO-PAUTA-MASTER.md § 8.10-8.15` implementation
   - `CLAUDE.md Hard Rule #23` per-clip atomic canonical forward
   - Memory `feedback_per_clip_atomic_assembly`

---

9. ⛔ **C-INVENTORY-WIRED — SPEC asset_list + ui_active completeness gate (BLOQUEANTE, añadido 2026-05-19 post matadero CP5 STOP gap #13)**:

   **Audit MUST run BEFORE cualquier otro gate CP5**. Si C-INVENTORY-WIRED falla → 🔴 NO-GO bloqueante, NO continuar a Gemini holístico ni audit-against-referent ni 7 gates pre-render. Razón: esos audits miden CALIDAD de lo que existe, NO INVENTORY contra SPEC — pueden dar PASS sobre un render estructuralmente incompleto.

   **9.1 Audio inventory** (assets/ folder):
   ```bash
   cd <project>
   # Per SPEC asset_list.sfx_prompts_to_generate
   SFX_SPEC=$(yq '.asset_list.sfx_prompts_to_generate | length' creative-specs/<id>.yaml)
   SFX_ACTUAL=$(ls assets/sfx/*.mp3 2>/dev/null | wc -l)
   echo "SFX:     SPEC=$SFX_SPEC / Actual=$SFX_ACTUAL"
   # Per SPEC asset_list.music_to_generate
   MUSIC_SPEC=$(yq '.asset_list.music_to_generate | length' creative-specs/<id>.yaml)
   MUSIC_ACTUAL=$(ls assets/music/*.mp3 2>/dev/null | wc -l)
   echo "Music:   SPEC=$MUSIC_SPEC / Actual=$MUSIC_ACTUAL"
   # Per SPEC asset_list.ambient_continuous_to_generate
   AMB_SPEC=$(yq '.asset_list.ambient_continuous_to_generate | length' creative-specs/<id>.yaml)
   AMB_ACTUAL=$(ls assets/ambient/*.mp3 2>/dev/null | wc -l)
   echo "Ambient: SPEC=$AMB_SPEC / Actual=$AMB_ACTUAL"
   ```
   Verdict: si CUALQUIERA `Actual < SPEC` → 🔴 FAIL bloqueante.

   **9.2 UI elements wired in index.html** (per SPEC ui_active per shot):
   ```bash
   # Per SPEC countdown_appearances + ui_active grep per shot
   for elem in countdown choice-button loading-bar; do
     SPEC_COUNT=$(yq ".shot_list.shots[].ui_active[] | select(test(\"$elem\"))" creative-specs/<id>.yaml | wc -l)
     HTML_COUNT=$(grep -c "$elem" index.html)
     echo "$elem: SPEC ui_active=$SPEC_COUNT / HTML wired=$HTML_COUNT"
   done
   ```
   Verdict: si CUALQUIERA `HTML wired = 0` cuando `SPEC ui_active >0` → 🔴 FAIL bloqueante.

   **9.3 Audio tracks wired in index.html**:
   ```bash
   AUDIO_TRACKS=$(grep -c '<audio' index.html)
   echo "Audio tracks wired: $AUDIO_TRACKS (expected: narration + music + ambient + sfx ≥4 minimum)"
   ```
   Verdict: si `AUDIO_TRACKS < 4` (narration + music + ambient + sfx layer minimum per SPEC) → 🔴 FAIL bloqueante.

   **9.4 Output forma obligatoria**:
   ```markdown
   | Asset class | SPEC required | Generated/Wired | Status |
   |-------------|---------------|-----------------|--------|
   | SFX         | 10            | 10              | ✅ PASS |
   | Music       | 3             | 3               | ✅ PASS |
   | Ambient     | 2             | 2               | ✅ PASS |
   | Countdown UI| 3             | 3               | ✅ PASS |
   | Choice btns | 2             | 2               | ✅ PASS |
   | Loading bar | 2             | 2               | ✅ PASS |
   | Audio tracks| ≥4            | ≥4              | ✅ PASS |
   ```

   **Rationale**: caso disparador matadero CP5 STOP point 2026-05-19. Engineer declared CP4 done con solo video assets (29 Hailuo clips delivered). `assets/sfx/` `assets/music/` `assets/ambient/` ALL EMPTY (0/10, 0/3, 0/2 vs SPEC). `index.html` ZERO countdown/choice_buttons/loading_bar wired (vs SPEC 3 countdown + 2 button sets + 2 loading bars). Auditor (yo) interpreted engineer's `coverage_pct 69.93% structural` label como "1 LU off LUFS tweak" pattern-match sin medir directo. User flagged "faltan SFX + countdowns + cut effects" → audit direct verified → gap surfaced. C-INVENTORY-WIRED ensures audits MEASURE inventory (not just quality), preventing recurrence.

   **Forward**: implementation in `scripts/audit-spec-completeness.py` (Phase 1 priority) automates this step + cron integration Phase 5.

---

## 3.5 Capability-aware testing methodology (canonical forward post-PRE-4.G 2026-05-25)

**Caso disparador:** Pattern 7 codification (PIPELINE.md §13.10) — sistema agnóstico-paradigma requiere validators que gating per capability flag, no que asume paradigma único horror-choice/AI-generated.

**Regla canonical:** Auditor verifica que tests + builds del Engineer respeten capability matrix del SPEC. Si validator falla property que NO está declarada en `spec.video_capabilities` → **Bug arquitectural** (paradigma mismatch), NO bug de implementation.

**Verification checklist per audit:**

- [ ] ¿Build script lee `spec.video_capabilities` antes de aplicar properties?
- [ ] ¿Tests classifican results como `applicable / not_applicable / pass / fail` (4-state, NOT binary)?
- [ ] ¿Hard Rules + tolerance bands están gated por capability flags donde aplica? (e.g., Hard Rule #25 caption invariance gated por `has_captions_baked`)
- [ ] ¿Si SPEC carece de `video_capabilities` block → flag Bug #9, escalá a Tomás (NO assumir defaults silent)?
- [ ] ¿Output report distingue claramente properties skipped por `not_applicable` vs properties actually tested?
- [ ] ¿Effects-library TIERED (PRE-4.K)? Verificá que el engineer pasó `--effects-dir` con AMBOS catálogos (Capa A universal primitives + Capa B `<format>` sub-genre) a `apply-effects-between-clips.py`; que recipes `xfade_fidelity: approximate` usados en producción tengan WARNING reconocido (Option B trigger si perceptualmente inaceptable). Principio "Disponibilidad ≠ Uso": el SPEC `shot_list[].transition_out` (Capa C) elige del catálogo disponible, NO prescripción.

**Anti-pattern detectable:**

- 🔴 Validator emite `failed` cuando capability `false` → arquitectural bug (debió ser `not_applicable`)
- 🔴 Build script aplica TTS sidechain duck cuando `has_tts_narration: false` → forzando paradigma sobre SPEC
- 🔴 Test asume captions existen sin leer capability → fragil para paradigmas no-AI

**Forward integration:** Paso 4 builds (4.2/4.4/4.3/4.1) + Sprint M validators deben heredar este pattern desde el inicio. Auditor verifica capability-gating ANTES de evaluar property results.

---

## 4. Output format obligatorio

**Toda audit entrega una tabla**, no prosa libre. Mínimo 3 columnas:

```markdown
| # | Item | Verdict | Razón | Authority | Fix |
|---|------|---------|-------|-----------|-----|
| V1 | <item> | ✅ PASS / ❌ FAIL / ⚠️ NB | <razón concreta> | <doc § línea> | <fix accionable o —> |
```

**Verdict semantics**:
- ✅ PASS — cumple, sigue
- ❌ FAIL — bloqueante, fix obligatorio
- ⚠️ NB (note-but-not-bloqueante) — observación, no bloquea pero queda flag

**Authority quote**: línea + número, no "según la PAUTA". Ej: `PAUTA-MASTER L412-413` o `INGENIERO-PAUTA § 5.7 L355-359`.

**Fix sugerido**: accionable (no "considerar revisar"). Ej: "Regen con prompt + 'NOT mid-forearm, full forearm coverage'" o "Add smoke test step 0 al gen-anchors.sh".

---

## 5. Veredicto final del auditor

Después de la tabla, el auditor concluye con UNO de:

| Verdict | Cuándo | Acción ingeniero |
|---------|--------|------------------|
| 🟢 **GO incondicional** | Todos los items PASS, 0 FAILs, NBs aceptables | Ejecuta plan |
| 🟡 **GO condicional** | 0 FAILs creativos pero ≥1 fix técnico bloqueante (ej. smoke test faltante) | Aplica fixes técnicos → emite `CP[N]-handoff-v(N+1).md` → re-audit focused |
| 🔴 **NO-GO** | ≥1 FAIL bloqueante (deliverable o prompt drift de SPEC) | Regen + arquitecto review si afecta SPEC compliance |
| ⛔ **ESCALAR** | Conflicto SPEC vs PAUTA-MASTER detectado (arquitecto SPEC tiene gap vs PAUTA), o tras 3 iter sub-9.7 | User decide override o re-spec |

---

## 6. ⛔ Anti-patterns del auditor (NO hacer)

1. **Delegar verificación al self-audit del arq/ing**. Si el handoff dice "rotation_check: ok per video-log.md", el auditor lee video-log.md y verifica independientemente. NO accept "ok".
2. **Confiar en citaciones del handoff sin leer la fuente**. El handoff cita SPEC L412 — el auditor abre SPEC y verifica L412 existe + dice lo que el handoff dice.
3. **Audit superficial cuando hay cambios mayores**. Si el deliverable es CP5 render, leer todo el SPEC + 21 Q pre-render-gate + medir LUFS — no scan rápido.
4. **Maquillar findings para acelerar GO**. Si una pauta canónica se violó, FAIL aunque retrase 1 día. El sistema dual-gate existe para detectar esto.
5. **Compartir contexto con arq/ing**. NO leer el HANDOFF-PROTOCOL del arquitecto antes de auditar (eso te biasea con su lens). Leer SOLO autoridad canónica + handoff del ingeniero.
6. **Inventar findings sin authority quote**. Cada FAIL/NB debe tener pointer a doc § línea.
7. **Cerrar audit sin responder preguntas explícitas del ingeniero**. Si el handoff tiene §10 "Preguntas auditor A1-A8", el output del auditor responde A1-A8 explícitamente.
8. ⭐ **Pattern-match label engineer sin medir directo** (added 2026-05-19 post matadero CP5 gap #13). Si engineer reporta `coverage_pct 69.93% structural` o `LUFS -15.1` o cualquier métrica con label cualitativo, NUNCA asumir el scope del gap por el label — **medir directo**: `ls assets/sfx/` `grep countdown index.html` `ffprobe master.mp3`. Hard rule #19 ("NUNCA estimar, SIEMPRE medir") aplica al auditor también. **Caso disparador**: yo (auditor) interpreté engineer's "coverage_pct 69.93% structural" como "1 LU off LUFS tweak iter 2 small fixes $0.50" pattern-match basado en label — real scope era "10 SFX + 3 music + 2 ambient + 3 countdowns + 2 button sets + 2 loading bars ALL UNGENERATED $1.10". User flagged directo "faltan SFX + countdowns + cut effects" → audit verified → gap surfaced. Audits miden CALIDAD de lo que existe, NO INVENTARIO contra SPEC — el auditor debe MEDIR el inventory diff manualmente hasta `audit-spec-completeness.py` esté implementado.

10. ⭐ **Trust docs canonical-scenes/intermediate sin direct frame verification** (added 2026-05-19 PM post iter 4-5 countdown wrong analysis). Cuando audit requiere verificar canonical pattern, auditor NUNCA debe confiar exclusivamente en docs canonical-scenes/ref-XX.md o REFERENT-ANALYSIS-13-VIDEOS-SYNTHESIS.md — esos docs son **sampling intermediario** (frames cada 5s en canonical-scenes) que **PIERDE eventos críticos** que caen entre frames sampled.

   **Rule canonical strict**:
   - Si auditor needs to verify canonical pattern (visual style, timing, sub-beat order, etc.) → extract frames directos del source canonical ref mp4 con granularity ≤1s para 30s primeros + ≤2s resto
   - Docs canonical-scenes = orientation + cross-video synthesis, NOT authority final
   - Direct frame extraction = ground truth ALWAYS wins over docs interpretation
   - Mismo principle Hard Rule #19 "NUNCA estimar, SIEMPRE medir" + anti-pattern #8 "pattern-match label sin medir directo"

   **Caso disparador**: matadero iter 5 audit 2026-05-19 PM. Yo (auditor) confié en canonical-scenes/ref-XX.md docs analysis para conclude "2/6 canonical refs tienen countdown en hook". User flagged "todos tienen countdown" → I extracted 56 frames directly from 8 source videos (8 × 7 timestamps) → confirmed 4/4 verified DO have FILM LEADER ACADEMY countdown UNIVERSAL. Docs sampling (every 5s) lost countdown events that occurred 3-7s window between sampled frames. Plus visual style codified previously was WRONG (minimalist CSS vs canonical film leader Academy).

   **Forward**:
   - GAP #20 canonical-scenes docs MAX DETAIL methodology (every 0.5s critical first 30s + every 1s rest)
   - Phase 1 script `extract-canonical-max-detail.py` automates comprehensive frame coverage
   - AUDITOR per CP audit: extract frames directly when verifying canonical pattern compliance — NUNCA depend solo on intermediate docs

   ⭐ **REINFORCEMENT 2026-05-29 (pattern_class `synthesis_converts_flexible_principles_to_binary_rules` instances 2/5 + 3/5; refinamiento de `validation_against_synthesis_violates_primary_source_principle`)**: el principio aplica también a REGLAS DE TEXTO/GUION, no solo a frames. **Y el modo de falla NO es "regla equivocada" sino "principio flexible convertido en regla binaria"**: al auditar una regla, distinguí 🟦principio underlying (enforce) de 🟩variabilidad creativa (NO enforce — el arquitecto es libre) de 🟥anti-pattern (flag). Un validator NO debe forzar una elección creativa específica. Cuando audites una regla con claim "canónico N/M" (framing, fraseo, estructura narrativa), validá contra la FUENTE PRIMARIA directa — los transcripts Whisper en `referent-analysis/horror-choice/ref-XX/transcription.json` — NO contra la síntesis (PAUTA-MASTER, canonical-scenes, memorias-paráfrasis). **Caso disparador**: la regla `feedback_si_elegiste_framing` / D19 ("Si elegiste X") era paráfrasis sintética; el primary source usa "Si [acción condicional]" (6/8 @referent-a) + "Si decides/escogiste" (2/8 @referent-b). El validator `audit-spec-narrative-coherence.py` enforzaba la paráfrasis → FAIL sobre el canónico real. Co-findings misma clase (forensic audit 2026-05-29): `"Una noche en paz"` mandado como canónico = 0/8 (es firma de marca nuestra); template cliffhanger `"juntos, en silencio, mirando…"` = 0/8; SCRIPT-WRITING-GUIDE "bueno sin diálogo"/"ganadora contra impulso" contradicen PAUTA §0/§6. **Regla**: una regla NO es canónica porque un doc de síntesis lo diga — solo si el transcript/frame primario lo confirma. Ver SYSTEM-LEARNINGS § Pattern 8.

   ⭐ **REINFORCEMENT 2026-05-29 (instance 4/5 — `tests_with_synthetic_fixtures_dont_substitute_real_artifact_testing`)**: el mismo principio aplica a TESTS. Un validator que pasa sus tests con fixtures SINTÉTICAS puede crashear contra el artefacto REAL si el schema sintético no coincide con el real ("green tests, red reality"). **Caso disparador**: los validators BUILD 4/5/8 (narrative-coherence + narration-fits + lip-sync) usaban fixtures dict-form y crashearon (`AttributeError`) en el primer SPEC v11 real (string-form). **Regla auditor**: (a) en cada SPEC-AUDIT, CORRER los validators contra el SPEC real (no confiar en el self-audit del arquitecto que dice "PASS" sin correrlos); (b) HR#26 expansión — todo validator nuevo DEBE incluir un regression test contra el SCHEMA del artefacto real, no solo fixtures sintéticas.

11. ⭐ **Random distributed timestamp frame extraction OBLIGATORIO** (added 2026-05-20 PM post cinema-abandonado iter 3 user catch). Auditor NEVER concludes "video PASS" sin extract frames AT MINIMUM en estos timestamps distribuidos:
    - t=hook_end (e.g., 7-9s)
    - t=duration*0.15 (e.g., 14s en video 96s — user caught error here)
    - t=duration*0.3 (e.g., 28s)
    - t=duration*0.45 (e.g., 43s)
    - t=duration*0.6 (e.g., 57s — user caught error 53-62s)
    - t=duration*0.75 (e.g., 72s — user caught error 70-77s)
    - t=duration-10s (end-of-video forensics per GAP #30)
    - t=duration-3s (outro card moment)
    
    PLUS run audit-frames-granular con --interval 0.5 OR audit-frames.py interval 1.0 + visually inspect ≥10 random frame extracts.
    
    **Caso disparador**: cinema-abandonado iter 3 user flagged 3 error windows (t=15, t=53-62, t=70-77) que auditor (yo) NO verifiqué — solo extracted 88/91/93/95s end-of-video. Trusted engineer "0 FAIL / 8 WARN" sin independent random distributed verification. Anti-pattern #8+#10 recurrence.
    
    **Rule canonical strict**:
    - Sample ≥7 distributed timestamps PER audit cycle
    - Caption overlap detection: count chunks per 5s window — if >5 chunks/5s = too dense, FLAG
    - Audio waveform analysis: ffmpeg volumedetect per 5s window — drift detection
    - Independent verify ≠ accept engineer report
    
    Forward: codify in script `audit-distributed-timestamps.py` (Phase 2 priority).

12. ⭐ **Trust Gemini holistic SCORE single-source (added 2026-05-21 post cinema-abandonado comparative analysis)**. Gemini holistic SCORES con ≥1 punto de inflación vs user perceptual ground truth (caso cinema-abandonado v2 = Gemini 8.6 holistic; user perceived "el peor"). Auditor NEVER concludes "video ship-ready" basado SOLO en Gemini holistic score.

   **Rule canonical strict**:
   - Holistic Gemini score ≥9.7 = NECESARIA pero NO SUFICIENTE (gate a)
   - `audit-against-referent.py` empirical bands ≥85% = NECESARIA (gate b)
   - Comparative analysis vs ≥3 canonical refs Gemini per-dimension = SI hay user perceptual concern
   - Dimensional comparison: si cualquier dimensión nuestra <2 below average ref → flag improvement opportunity even with holistic ≥9.7
   - User perceptual = ground truth final (Rule D PRECEDENCE)

   **Caso disparador**: cinema-abandonado v2 iter 6 Gemini 8.6/10 holistic vs Ref-2 9.0/10 (canonical cockpit). User: "el nuestro es el peor". Per-dimension audit revealed:
   - cuts/min cinema=12 vs canonical 13-22 (-30%)
   - music layers cinema=1 vs canonical 3 (-66%)
   - character consistency cinema=7/10 vs canonical 9/10 (-2pts)
   - visual artifacts cinema=7/10 vs canonical 8/10 (-1pt)
   
   Holistic Gemini didn't surface these because it scored "atmosphere 9/10" + "narrative 9/10" high. Per-dimension empirical comparison surfaced them.

   **Auditor check obligatorio post-CP5 render**:
   - Run Gemini holistic (current standard)
   - Run `audit-against-referent.py` empirical (current standard)
   - PLUS run comparative Gemini Vision on ≥3 canonical refs same prompt → dimensional table
   - If any dimension below canonical average by ≥2pts → flag improvement opportunity (even if overall ≥9.7)

   Forward: codify in script `audit-comparative-vs-canonical.py` automates this step.

16. ⛔ **Caption PRESENT ≠ Caption ALIGNED with narrator audio — explicit cross-reference required** (added 2026-05-21 PM late post V3 redo caption desync detected by user, missed by auditor).

   **Caso disparador**: V3 parque-acuatico-abandonado redo cinema legacy stack. Auditor (yo) extracted distributed timestamps frames + verified captions PRESENT + calibrated v4 scored CAPTIONS 10/10. User watched render + identified caption desync 0-34s window. Independent verification confirmed: hook caption "ELIGE TU COMPAÑERO" missing 2-8s, captions appear at SPEC-intent timestamps but narrator master shifted via adelay padding accommodating overshoots = 1-3s drift cumulative.

   **Hard rule canonical strict**:
   - Caption verification = TWO separate checks
     - Check 1: caption visually present on frame (current standard) ✓
     - Check 2 ⭐⭐ NEW: caption TEXT matches narrator audio AT SAME TIMESTAMP
   - Cross-reference method:
     - Extract frames every 2-3s (NOT only distributed timestamps — denser)
     - Per frame: Gemini Vision extract caption text visible
     - Whisper transcribe audio word-level timestamps
     - For each frame timestamp T: caption_text at T should match narrator_audio_text in window [T-1s, T+1s]
     - Similarity threshold: Jaccard ≥0.5 minimum
   - If ANY caption mismatches audio at same timestamp → FAIL
   - Calibrated v4 CAPTIONS dimension is INSUFFICIENT alone — needs sync verification

   **Forward implementation**:
   - `scripts/audit-caption-audio-sync.py` Phase 3 priority — automate this check
   - Hybrid architecture V4+ eliminates this drift class structurally (captions BAKED per clip cannot drift from audio)

   **Why missed in V3 redo audit**:
   - Calibrated v4 prompt asks "captions present + canonical style?" — answered YES
   - Auditor extracted ~12 frames distributed, didn't check caption-vs-audio per frame
   - This is methodology gap codified forward

15. ⛔⛔ **Engineer multi-CP autonomous run sin auditor gates entre cada CP — FORBIDDEN** (added 2026-05-21 PM late post V3 parque-acuatico iter 1 failure root cause). Auditor (yo) spawned engineer como SINGLE sub-agent corriendo CP1+CP2+CP3+CP4+CP5 autonomous. Engineer self-declared "complete" con calibrated v4 7.7 → user perceptual 6.0 con 15 bugs surfacing AT ONCE in final render. CLAUDE.md § 0.0 dice "Cada handoff CP[N] del ingeniero pasa por auditor independiente antes de ejecutar el siguiente CP" — VIOLATED.

   **Hard rule canonical strict (NEVER violate)**:
   - Engineer agent invocation = **ONE invocation PER CP** maximum
   - Between each CP: auditor SPAWN audit independent + emit verdict
   - Engineer NEVER chains CPs autonomously
   - Auditor verdict gates: PASS → next CP / NB → engineer iter same CP / FAIL → escalate
   - NO exception per "user at lunch" or "autonomous factory goal" or "agent orchestration simplicity" — these were reasons I (auditor) violated. NEVER again.

   **Per CP audit gates required**:
   - Post-CP1 anchors: auditor verify STRICT mode + character signature distinctiveness + setting consistency
   - Post-CP2 TTS+captions: auditor Whisper match SPEC text_canonical + per-segment WPM canonical
   - Post-CP3 shot images: auditor character consistency cross-shots + setting LUT
   - Post-CP4 animation: auditor visual artifact + atmospheric motion ≥3 per shot + motion_bridge match SPEC
   - Post-CP5 render: full audit (calibrated v4 + audit-frames-granular + audit-spec-completeness + ALL gates)

   **Anti-pattern signal (detect engineer attempting to chain CPs)**:
   - Engineer prompt says "execute CP1-CP5 end-to-end" → REJECT, must be 1 CP per spawn
   - Engineer single execution time >15 min → SUSPICIOUS, probably chaining CPs
   - Engineer self-declares "production complete" without intermediate auditor PASS verdicts → FORBIDDEN

   **Caso disparador**: V3 parque-acuatico-abandonado iter 1 2026-05-21 PM late. Engineer 25-min single run + self-7.7 calibrated v4 → user 6.0 perceptual + auditor independent inspection 15 bugs (missing decision UI, countdown, effects library, character mix-up, captions garbled, audio mono, narrator cut boundaries, fewer music layers, etc.). All 15 bugs would have been caught EARLY per CP-by-CP gates with cheap fixes vs needing full iter 2 reassembly.

   **Forward systemic**:
   - AUTONOMOUS-FACTORY-ROADMAP orchestrator design MUST enforce CP-by-CP sequential gates
   - NO end-to-end engineer agent spawning forward video #3 iter 2+ + video #4+
   - `scripts/orchestrator-cp-by-cp.py` Phase A scaffold (forward)
   - CLAUDE.md Hard Rule #24 NEW: "Auditor enforce CP-by-CP gates mandatory"

14. ⭐ **Story chain rationalization without execution check** (added 2026-05-21 post cinema-abandonado / matadero analysis). Auditor reading story-coherent doesn't mean execution-continuous. Gemini calibrated v4 can score narrative chain 9-10 BUT physical journey broken via teleport-cuts.

13. ⭐ **Editing variety blindness — "cuts/min vs canonical" gap** (added 2026-05-21 post cinema-abandonado comparative analysis). Auditor verifies cuts/min vs INGENIERO-PAUTA band, but didn't verify TRANSITION VARIETY (hard cuts vs cross-fade vs film-burn vs light-flash etc.).

   **Rule canonical strict**:
   - Empirical refs use ≥3 transition types per video (hard cut + at least 2 others)
   - Cinema-abandonado used hard cuts only (Gemini comparative noted "Hard cuts and some zooms")
   - Per Phase 2 effects library (10 transitions) → engineer SHOULD use variety, not only hard cuts
   - Auditor check: ffprobe transition timestamps + visual inspect cross-fade vs hard cut frequency

   **Caso disparador**: cinema-abandonado iter 1-6 used hard cuts + zooms exclusively. Canonical refs used hard cuts + black-screen + cross-fade + flash. Effects library was missing forward Phase 2 — added 2026-05-20.

   **Auditor check obligatorio post-CP5**:
   - Inspect ≥5 transition timestamps via ffmpeg frame extraction
   - Count unique transition types used
   - If <3 unique types → 🟡 NB editorial variety thin

   Forward: codify in script `audit-transition-variety.py` automates this step.

9. ⭐ **Audio-visual lip-sync realism violations** (added 2026-05-19 PM post matadero iter 4 user catch). Cuando character face visible + lips mid-articulation pero NO audio del character playing → uncanny valley violation = realismo cinematográfico roto. **Rule canonical strict**:
   - Character lips mid-movement → character audio MUST be playing simultaneously (lip-sync compliance)
   - Character audio NOT playing (silence o narrator off-screen o countdown) → lips MUST be static (smile/neutral/closed pose). NO mid-articulation transitions.
   - NO "mouth begins moving toward warning line" mid-state propositions — esto es exactly el anti-pattern
   - Aplica a TODOS los character faces visibles (face = lips potentially visible = strict compliance)
   - NO aplica a: matarife sin face (cleaver helmet), narrator off-screen, viewer POV (hand visible no face)
   
   **Auditor check obligatorio**: frame extraction at character-non-speech moments (e.g., during narrator overlay OR countdown OR transition silence) — verify lips static. Si lips mid-articulation visible during character-silent moment → 🔴 FAIL realism.
   
   **Caso disparador**: matadero iter 4 propuesta inicial mía (auditor terminal 3) sugirió "cocinera mouth begins moving toward warning line" durante countdown silence — user catch immediato: "se pierde el realismo". Confirms anti-pattern. Forward: codify en INGENIERO-PAUTA + AUDITOR-PROTOCOL para anti-recurrencia universal.

---

17. ⛔ **Complete the work before passing it to the next triangle role** (added 2026-05-29, Hard Rule #27, pattern_class 5/5 `architect_self_flags_gaps_instead_of_iterating_pre_emit`). Un rol NO entrega trabajo con findings 🔴 conocidos esperando que el siguiente rol los triangule. **Arquitecto**: corre los 3 validators (narrative-coherence + narration-fits-duration + lip-sync-marks) contra su PROPIO SPEC pre-emit + itera hasta 0 FAIL. **Auditor que recibe un SPEC con 🔴** → **RETORNA al arquitecto** (no escala a Tomás salvo ambigüedad arquitectural real); el auditor NO "arregla" el SPEC ni triangula gaps que el arquitecto debió resolver. **Caso disparador**: V5 sala-limpia 2026-05-29 — arquitecto declaró "self-audit all PASS" sin correr los validators → SPEC-AUDIT surfació shot_02 320 WPM + 3 schema crashes que el self-audit cualitativo no detectó. **Corolario auditor (instance 4/5)**: en cada SPEC-AUDIT, CORRER los validators contra el SPEC real (no confiar en el "PASS" del arquitecto).

18. ⛔ **Validators/builds NO asumen capacidades del modelo hardcoded — CONSULTAN `MODEL-CAPABILITIES-MATRIX.md`** (added 2026-05-30, Hard Rule #28/#29, pattern_class 6/5 `model_constraints_not_propagated_across_triangle_roles`). Todo check de "cabe en el shot / el clip / la resolución" debe leer la MATRIX (canonical_pace_wpm, i2v clip_duration_max_s, t2i constraints), NO constantes hardcoded ni supuestos. **Auditor**: en SPEC-AUDIT, verificá que el SPEC respeta las capabilities declaradas cross-CP (narración@canonical ≤ min(duration_intent_s, i2v clip max); rasgos raros t2i dentro de stability/pose-coupling). **Caso disparador V5**: el validator L1 chequeaba `WPM≤280` (comprimible) en vez de `narración@165 ≤ min(dur, hailuo 5.9s)` → 18.8s de narración truncados en 10 shots escaparon al gate. Fix: `audit-spec-narration-fits-duration.py` ahora lee la MATRIX. Forward validators: `audit-clip-timing-vs-audio.py` (atomic clip_dur ≥ narración_dur), `audit-cross-cp-output-consistency.py` (cada CP output preserva properties del anterior).

19. ⛔ **Coverage checks DEBEN validar 3 niveles: existence + semantic + TEMPORAL** (added 2026-05-30, Hard Rule #30, instance 6 `user_perceptual_detects_what_validators_miss`). Verificar que "un caption existe" (1 frame) NO basta. Coverage real = (A) existe per shot + (B) el texto del caption matchea la narración + (C) el caption es visible durante TODA la duración hablada (temporal span), no solo la 1ª frase. **Caso disparador V5 caption bug**: el caption-burn quemaba la narración completa como UN bloque estático truncado a 2 líneas (`wrap()[:2]`) → solo la 1ª frase se veía; el resto de la narración (audio completo) quedaba SIN caption. Mi audit V5.1 reportó "caption coverage 100%" mirando 1 frame (existence) — Tomás detectó el gap temporal. **Fix**: chunkear TODAS las palabras (words.json) en cues word-timed progresivos. **Regla auditor**: para captions, extraer frames a MÚLTIPLES tiempos por shot (early/mid/late) + confirmar que la narración tardía también tiene su caption. Forward: `audit-caption-temporal-coverage.py` (caption visible durante toda la narración, por chunks). Mismo CP que el bug de truncación de audio (atomic build) — distinto mecanismo (wrap-truncation vs audio-trim).

---

20. ⛔ **Auditar ESTRUCTURA vs canónico (no solo linkage) — y FLAGEAR divergencias, NUNCA racionalizarlas** (added 2026-06-01, Hard Rule forward, caso V6 invernadero). En el SPEC-AUDIT, comparar el guion **beat-por-beat** contra `horror-choice-format/PAUTA-MASTER.md § 2` — § 2.1 (esqueleto) + § 2.2 (INVARIANTE: el bueno-aparente NUNCA está en el recorrido jugado tomando decisiones) + § 2.4 (las 8 perspectivas: estructura / invariante / recorridos-secuenciales / pattern-rotación / name-labels-durante-countdown / glitch-pantalla-antigua-en-story-change / SFX-densos-matcheados-ducked / + checks pre-existentes). **Verificar el linkage de refs (¿el SPEC cita bien?) NO basta** — hay que verificar que la ESTRUCTURA matchee el canónico. **Si notás una divergencia, FLAGEALA como 🔴 que retorna al arquitecto — NUNCA la racionalices como "fortaleza/necesaria".** Caso disparador: V6 invernadero — Celeste (bueno-aparente) presente y tentando en el played path (shots 05/10), violando el invariante; yo (auditor) lo NOTÉ en el SPEC-AUDIT y lo escribí como "necesario y mejor para el doble-amable" (racionalización) en vez de flagearlo → Tomás lo cazó post-render. Enforcement programático: `audit-spec-structure-vs-canonical.py`. Memoria `feedback_spec_audit_structural_divergence`.

---

## 7. Independencia de juicio — separación de 3 terminales

El auditor vive en su **propio terminal** sin contexto del arq/ing. Esto es estructural, no opcional.

- **NO** invocar auditor como sub-agent del ingeniero (memoria `feedback_3_terminal_separation`)
- **NO** pasar el contexto del arquitecto al auditor — el auditor lee SPEC fresh + autoridad canónica + handoff del ingeniero
- **NO** el auditor edita el SPEC ni el handoff. Solo emite findings + verdict. Cambios los hace arq (SPEC) o ing (handoff)

**Handoff package vía filesystem**:
```
ingeniero produce: <proyecto>/CP[N]-handoff[-vN].md  (self-contained)
auditor lee:       <proyecto>/CP[N]-handoff[-vN].md + autoridad canónica directa
auditor entrega:   tabla findings + verdict (en chat user, NO crea .md sin pedir)
```
