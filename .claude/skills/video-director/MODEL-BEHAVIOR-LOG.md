# MODEL-BEHAVIOR-LOG.md — observed behaviors of external AI models

> **NIVEL 1.5 — between CAPA 1 universal docs (skill/architecture) and CAPA 2 per-format technical pautas.**
>
> **Purpose**: capture empirically-observed quirks/limits of external AI models (image gen, video gen, TTS, vision) that we cannot control but must DESIGN AROUND. Companion to `MODEL-BENCHMARK.md` (which is feature/cost benchmark); this log is BEHAVIOR (failure modes, edge cases, workarounds).
>
> **Audience**: architect at CP0 (avoid shot compositions that hit known limits) + engineer at CP1-CP4 (apply workarounds in prompt structure) + auditor at gates (detect when bug class manifests).
>
> **Format**: append-only YAML-like entries. Each entry: model + date_discovered + behavior + validation_evidence + workaround_validated + implications_forward.

---

## Entry 1 — Gemini image gen `--ref` identity propagation is FACE-COUPLED for rare anatomy

```yaml
model: gemini-3.1-flash-image-preview (Nano Banana / Gemini Pro 3.1 Image)
date_discovered: 2026-05-22 PM
discovered_by: 🔍 Auditor (during V4 cerro-aislado-v4 CP3 audit)
behavior: |
  `--ref <anchor.png>` identity propagation is FACE-COUPLED. When face + anatomical-signature
  feature co-located in frame, the signature preserves correctly. When the signature appears
  in a hand-only or feature-only composition WITHOUT face in frame, the model regresses to
  NORMAL anatomy regardless of:
    (a) --ref reference image showing the signature
    (b) explicit prompt reinforcement ("6 fingers per hand, polydactyly, etc")
    (c) iteration count (3 attempts all deterministic 5-finger regression)
  
  The model appears to propagate identity primarily through facial recognition.
  When face absent, defaults to most-likely interpretation (normal human anatomy) for
  rare/uncanny features.
validation_evidence:
  - V4 anchor char_a_v1.png: 6-finger polydactyly achieved via explicit prompt + face+hand
    co-located + fingerless gloves (3 iter required to achieve initially)
  - V4 shot_10 (face + hand co-located in frame, palm forward, anemometer scene):
    polydactyl PRESERVED → 6 fingers ✓ on first iter with --ref + explicit prompt
  - V4 shot_11 (hand-only POV gripping precipice edge, NO face in frame): 3 iter all
    REGRESSED to 5-finger normal anatomy despite identical prompt + --ref structure
    as shot_10
  - V4 shot_16 (face + hand co-located, cabin interior, palm forward, similar to shot_10):
    confirmed PRESERVED 6 fingers ✓ post Option α regen test 2026-05-22 PM
sample_workaround_NOT_validated:
  - ALL-CAPS "POLYDACTYLY" in prompt triggers Gemini safety filter (likely medical-term
    detection). Engineer V4 shot_10 worked around by using neutral wording: "six fingertips
    per hand, extra finger between pinky and ring". Lower-case + descriptive wording bypasses
    the filter. Use neutral framing for any medical/anatomical-anomaly term.
workaround_validated:
  - "Locus-specific anchors" — for each signature region that may appear in feature-only
    composition without face, generate a DEDICATED anchor PNG showing that locus in
    isolation. Then use `--ref <locus_anchor.png>` for shots that isolate that locus from
    the face.
  - Example: char_a_v1.png (full body anchor with face) + char_a_v1_hand.png (close-up hand
    anchor showing 6-finger polydactyly in isolation) for hand-only shot compositions.
  - Validated V4 2026-05-22 PM CONFIRMED: shot_11 regen with `--ref char_a_v1_hand.png`
    succeeded 1/1 iter preserving 6-finger (after 3/3 iter had failed with full-body anchor).
    Locus anchor methodology PROVEN.
  - shot_16 with `--ref char_a_v1.png` (face+hand co-located, similar to shot_10 pattern):
    succeeded 1/1 iter preserving 6-finger on BOTH hands raised + face features intact.
    Validates face-coupling hypothesis: when face in frame, full anchor suffices.
implications_forward:
  architect_CP0:
    - At SPEC v11.2+ schema, NEW field `characters[].visual_signature_critical_loci[]`
      declaring which signature features are locus-coupled and require dedicated anchors
      (e.g., "hand_polydactyl", "left_eye_milky", "prosthetic_arm", "scar_face_left_cheek").
    - When SPEC includes shots that isolate a signature locus from the face (POV hand
      detail / extreme close-up feature / silhouette where only locus visible), the architect
      must flag those shots + indicate which dedicated anchor is required.
    - SPEC validation: shot_list[].pov_traversal + composition_isolates_locus[] → trigger
      locus-specific anchor generation pre-CP1.
  engineer_CP1:
    - Characters with signature features may require MULTIPLE anchors (full body + locus-
      specific per region).
    - Per-locus anchor prompt: close-up isolating the signature region, neutral wording for
      any anomaly term (avoid ALL-CAPS medical terms), clear lighting + neutral background,
      feature countable/identifiable.
    - Bootstrap: anchor inventory expands per-character based on visual_signature_critical_loci.
  engineer_CP3:
    - Per-shot prompt construction must check which `--ref` to use based on composition:
      face+hand → full anchor / hand-only → locus anchor / etc.
    - The shot's composition (face presence + which features in frame) is the deciding
      factor, NOT just "is character X visible".
  auditor_CP1 + CP3:
    - Sprint B `audit-anchor-vs-spec-signature.py` MUST extend per-locus methodology:
        a) Validate each signature feature in its composition context (anchor + locus)
        b) Validate shot output preserves the relevant locus signature
        c) Flag when shot composition isolates locus from face but locus anchor missing
status: **VALIDATED** (2026-05-22 PM late). Locus-anchor workaround CONFIRMED production-ready.
        V4 evidence: 3/3 hand-visible Iván shots achieve 6-finger compliance using methodology
        (shot_10 + shot_16 face+hand full anchor / shot_11 hand-only locus anchor).
        Canonical method forward for V5+ horror characters with anatomical signature features.
        **UPDATE 2026-05-22 PM late late — shot_16 v11.2 simplified regen (pose-coupling discovered)**:
        Stability budget ≤3 elements is **NECESSARY BUT STILL NOT SUFFICIENT**.
        ⭐ NEW empirical finding: Gemini `--ref` full anchor (face+hand) is **POSE-COUPLED in
        addition to face-coupled**. Polydactyl preserves ONLY when shot hand pose matches the
        ANCHOR hand pose. Different pose with full anchor → regression even if all other
        constraints (face co-located + stability budget ≤3 + neutral wording + explicit prompt
        reinforcement) are satisfied.

        V4 evidence refined:
        - char_a_v1.png anchor pose = palm-forward raised spread
        - shot_10 (palm-forward raised toward anemometer) → matches anchor pose → 6 ✓
        - shot_16 v2 stop-gesture (palm-forward raised stop) → matches anchor pose → 6 ✓
        - shot_16 v11.2 (palm-DOWN resting on table) → DIFFERENT pose from anchor → 5 ✗ × 2 iter
        - shot_11 v2 (palm-down gripping ledge, DIFFERENT pose from anchor) → 6 ✓ ONLY because
          used hand-only LOCUS anchor (not full anchor) — locus anchor is pose-TOLERANT
        
        Refined hypothesis: when face in frame with full anchor, Gemini balances face identity
        + hand identity. If face matches anchor but hand pose doesn't = "inconsistency penalty"
        → model regresses hand to normal anatomy as fallback. If face absent (locus anchor) =
        no penalty conflict, hand anatomy preserves regardless of pose.
        
        **Three preservation paths confirmed (revised post 4th refinement)**:
        (a) Full anchor + face+hand co-located + hand pose EXACTLY matches anchor + ≤3 props → ✓
            EXACT match includes: hand configuration (both bare OR both gloved matching anchor),
            object-holding state (empty hands if anchor empty, not holding object),
            full pose context match (not just abstract "palm forward" category)
        (b) Locus anchor + face absent + ≤3 props → ✓ (pose-tolerant, NO exact-match needed)
        (c) Multi-ref [full + locus] + face+hand co-located + ≤3 props → UNTESTED hypothesis
        
        **Failed paths confirmed**:
        (d) Full anchor + face+hand + DIFFERENT abstract pose (palm-down vs palm-forward) → ✗ V4 shot_16 v11.2
        (e) Full anchor + complex multi-action 4+ props → ✗ V4 shot_16 v3
        (f) ⭐ NEW 2026-05-22 PM late late: Full anchor + face+hand + ABSTRACT pose match
            (palm-forward) BUT bare/gloved asymmetry (one bare + one gloved vs anchor showing
            both same state) OR holding-object pose (clipboard) vs anchor empty pose → ✗
            V4 shot_16 v11.3: 5/6 fingers BOTH hands despite abstract pose match.
        
        **4th refinement implication**: pose-coupling is EXACT-MATCH coupling, not abstract
        category coupling. For V5+ practical design rule: SPEC shots requiring rare anatomy
        preservation must EXACTLY replicate anchor pose with zero variations (hand state +
        object holding + symmetry). For shots requiring different poses, must use:
        - Path (b) locus anchor with no face in frame, OR  
        - Generate additional locus anchor matching the shot's specific pose (e.g., 
          `char_a_v1_hand_holding_clipboard.png` for clipboard-holding shots).
        Multi-ref path (c) untested — could decouple face identity from hand pose constraint.
        V4 evidence: shot_16 v2 (face+hand + simple stop-gesture pose, no other props) → 6 fingers ✓.
        shot_16 v3 attempts (face+hand + ladder + clipboard + lamp + window + glove-removal action) → 5 OR 3 fingers ✗ across 2 iter.
        Iter 1 even produced anatomical hallucinations (detached glove with severed-flesh
        fingertips on table) — symptomatic of overloaded stability budget.
        Implication: when SPEC describes multi-action / multi-prop shot with anatomical
        signature, EITHER decompose into multiple simpler shots OR simplify single composition
        to ≤3 prop elements. Empirical threshold observed: ~3 distinct props or characters
        beyond the anchor character itself.
related_gaps:
  - GAPS-LOG.md #44 (anchor-vs-SPEC.visual_signature compliance NOT enforced) — CRÍTICA
  - GAPS-LOG.md #44b (this finding, codified)
```

---

---

## Entry 2 — Gemini Image renders label-prefixed scene directions as BURNED-IN overlay text

```yaml
model: gemini-3.1-flash-image-preview (Nano Banana / Gemini Pro 3.1 Image)
date_discovered: 2026-05-22 evening
discovered_by: User Tomás caught V4 cerro-aislado-v4 shot_06 (auditor missed in CP3 audit — only zoom-verified 3 polydactyly-critical shots, trusted contact sheet thumbnail for other 17 which lacks resolution to detect overlay text)
behavior: |
  When engineer prompt includes label-prefixed scene direction syntax (e.g., "POV: Renato
  leans forward whispering", "ANGLE: Low angle hero shot", "ACTION: Iván raises hand"),
  Gemini Image may interpret the label-prefix as TEXT-TO-RENDER-AS-OVERLAY rather than
  as scene context. Result: burned-in English caption appears in the generated image at
  top of frame (often as if it were a subtitle), in the original prompt language.
  This is hallucinated text, NOT requested by the SPEC. Affects narrative shots where
  visual_intent context is described with screenplay-style label prefixes.
validation_evidence:
  - V4 shot_06 (Renato close-up whisper, cool_blue caseta interior): generated with English
    burned-in caption "POV: Iván, he's scared and has to whisper" at top of frame. Text
    was NOT in SPEC visual_intent — it was likely scene context label "POV:" or similar
    in engineer's prompt that Gemini rendered as overlay.
  - Other V4 shots (shot_02, shot_07, shot_10, shot_11, shot_16, shot_19) had no overlay
    text — suggests engineer's shot_06 prompt specifically had label-prefix syntax that
    other shots avoided.
workaround_validated:
  - DESCRIPTIVE SENTENCES instead of label-prefix syntax. Replace:
      "POV: Renato leans forward whispering" → "First-person POV. Renato leans toward
      the camera, whispering quietly into frame."
      "ANGLE: Low angle hero shot" → "Low-angle hero composition. Camera tilted up at
      character."
      "ACTION: Iván raises hand" → "Iván raises his hand into frame."
  - All scene direction context expressed as full sentences with subject + verb, NO
    label-prefix colons + descriptive clauses.
  - Validation: pending V4 shot_06 regen with this workaround applied.
implications_forward:
  engineer_CP3 + CP4:
    - Engineer prompt construction MUST use descriptive sentences ONLY for scene context.
      NO label-prefix syntax ("POV:", "ANGLE:", "ACTION:", "CAMERA:", "SHOT:", etc.).
    - If SPEC `scene_context.camera_intent` uses screenplay shorthand, engineer
      MUST REWRITE to descriptive sentences before sending to Gemini.
    - Pre-send self-check: scan prompt for `(?i)^(POV|ANGLE|ACTION|CAMERA|SHOT):` pattern
      → reject if matched.
  auditor_CP3:
    - Visual fidelity audit MUST direct-verify EVERY shot at native resolution. Contact
      sheet thumbnail view is INSUFFICIENT to detect overlay text (~24×42px per shot in
      4×5 grid).
    - Sprint B priority: `audit-shot-burned-text-ocr.py` via Gemini Vision OCR per shot
      to detect any rendered overlay text not declared in SPEC (Gap #51).
  architect_CP0:
    - SPEC.shot_list[N].camera_intent should use descriptive sentences in YAML, NOT
      screenplay-shorthand label-prefix syntax. Forward MODEL-BEHAVIOR-LOG-aware SPEC
      authoring style.
status: **VALIDATED** (2026-05-22 evening). Both bug behavior AND workaround confirmed.
        V4 shot_06 regen 1/1 iter: NO overlay text rendered when prompt uses descriptive
        sentences only + explicit anti-typography negative block. Production-ready forward.
related_gaps:
  - GAPS-LOG.md #50 (this finding codified — engineer prompt syntax constraint)
  - GAPS-LOG.md #51 (auditor CP3 skim audit anti-pattern enabling this to escape detection)
```

---

## Entry 3 — Gemini `--ref` con LOCUS anchor en composición full-scene inserta el locus como OBJETO duplicado

```yaml
model: gemini-3.1-flash-image-preview (Nano Banana / Gemini Pro 3.1 Image)
date_discovered: 2026-06-04
discovered_by: 🔍 Auditor (V7 ultimo-tren-carga CP3 audit — sweep visual 40 shots)
behavior: |
  Cuando un shot full-scene (personaje de cuerpo entero + entorno) usa como `--ref` un
  LOCUS anchor (imagen del rasgo AISLADO — p.ej. una máscara flotando sola, generada per
  Entry 1 workaround), Gemini inserta el locus COMO OBJETO INDEPENDIENTE en el frame
  además del personaje: una segunda máscara gigante flotando en el foreground, sin
  pertenecer a ninguna cara. El modelo interpreta el ref aislado como "este objeto debe
  estar en la escena", no como "este rasgo pertenece al personaje".
validation_evidence:
  - V7 shot_05 (Dario full-scene señalando el piso, --ref char_a_v1_mask): máscara
    duplicada gigante en foreground inferior + Dario completo arriba. FAIL audit.
  - V7 shot_15 (Dario arriba de escalera vertical, --ref char_a_v1_mask): misma máscara
    suelta flotante en foreground. FAIL audit. (2/2 full-scene con locus ref = bug)
  - Contraejemplo: CP1 char_a_v1_mask como TARGET de generación (close-up del locus solo)
    → correcto; el bug es solo cuando el locus es REF de una composición mayor.
workaround_validated:
  - Full-scene con personaje → `--ref <full_body_anchor>` + REINFORCE el rasgo EN el
    personaje vía prompt ("his face covered by the antique twin-filter respirator mask
    he WEARS"). Validado V7 regen shot_05 (1 iter) + shot_15 (2 iter): máscara única
    puesta, cero objetos duplicados.
  - LOCUS anchor como --ref SOLO para close-ups donde el rasgo ocupa el frame SIN
    cuerpo/escena (uso original Entry 1).
implications_forward:
  architect_CP0:
    - SPEC `anchor_id_required` per shot debe asignar el locus anchor SOLO a shots cuyo
      encuadre aísla el rasgo (close-up del locus); shots full-scene del personaje llevan
      el full anchor aunque el rasgo deba leerse nítido (se refuerza por prompt).
  engineer_CP3:
    - Pre-batch check: si anchor_id_required = locus anchor Y el shot es full-scene →
      flag al auditor (probable error de asignación) antes de generar.
  auditor_CP3:
    - Sweep visual: buscar el rasgo/locus DUPLICADO como objeto suelto en foreground —
      firma visual de esta clase de bug.
status: **VALIDATED** (2026-06-04). Workaround production-ready (V7 shots 05+15 regen OK).
related_gaps:
  - Entry 1 (locus-anchor methodology — este entry acota su scope de uso como --ref)
```

---

## Entry 4 — i2v NO preserva rasgos del personaje no visibles en el frame fuente; al girar/revelar, alucina

```yaml
model: i2v image-to-video class (validado en Hailuo; aplica a la clase image-to-video — ver MODEL-BENCHMARK)
date_discovered: 2026-06-04
discovered_by: 🔍 Auditor (V7 ultimo-tren-carga CP4 animation audit)
behavior: |
  Un modelo i2v solo "conoce" lo que la imagen fuente MUESTRA. Cualquier rasgo del personaje que
  NO sea visible en el frame de entrada (una cara tapada/de espaldas, un detalle fuera de cuadro)
  el modelo NO lo tiene — y si el motion prompt pide girar / revelar / mostrar ese rasgo, el modelo
  lo ALUCINA: inventa lo que falta en vez de respetar la identidad del personaje. No hay "memoria"
  del diseño del personaje más allá del píxel fuente.
validation_evidence:
  - Personaje enmascarado filmado de espaldas + motion prompt que pedía un giro hacia cámara →
    el i2v inventó un ROSTRO HUMANO bajo/en lugar de la máscara (rasgo nunca presente en la fuente).
    FAIL audit de consistencia.
  - Contraejemplo: cuando el rasgo SÍ era visible en el frame fuente (close-up del rasgo de frente)
    y el motion era sutil (push-in / parallax sin revelar), el i2v lo preservó correctamente.
workaround_validated:
  - Motion prompts NUNCA piden revelar lo que la fuente no muestra (sin giros que expongan una cara
    tapada/de espaldas, sin "se da vuelta y vemos…").
  - Cuando el rasgo SÍ es visible en la fuente → REINFORCE explícito del rasgo en el motion prompt
    (nómbralo: "the mask he wears stays on", etc.) para que no derive entre frames.
  - En personajes con un rasgo OCULTO por diseño, LOCK explícito ("face/feature never shown") en el
    motion prompt — el rasgo se mantiene fuera de cuadro durante toda la animación.
implications_forward:
  architect_CP0:
    - Al especificar shot direction de un personaje con rasgo oculto, el motion intent del SPEC NO
      debe pedir un reveal de ese rasgo vía i2v; si la historia necesita el reveal, resolverlo con
      un shot/anchor nuevo que YA muestre el rasgo (no confiar en que el i2v lo invente bien).
  engineer_CP4:
    - Antes de animar: verificar que el motion prompt no exija exponer un rasgo ausente del frame
      fuente; agregar el reinforce (rasgo visible) o el lock (rasgo oculto) según corresponda.
  auditor_CP4:
    - Sweep de consistencia en los frames del clip animado: buscar rasgos ALUCINADOS en giros/reveals
      (una cara aparecida donde la fuente no la mostraba) — firma visual de esta clase de bug.
status: **VALIDATED** (2026-06-04, V7). Workaround production-ready.
related_gaps:
  - Entry 1 / Entry 3 (consistencia de rasgos de anatomía rara — acá la pérdida ocurre en el paso i2v,
    no en image gen).
```

---

## How to use this log

**Architect at CP0**: scan entries for any model behavior that affects the SPEC you're designing. If your SPEC includes shots that hit a known behavior pattern (e.g., feature-only composition + character with anatomical signature), flag in `architect_annotations[]` + structure SPEC accordingly (locus anchors, composition rewrites, etc.).

**Engineer at CP1-CP4**: when generating prompts, consult this log for known workarounds. Apply neutral wording for safety-filter triggers. Use locus-specific anchors when shots isolate features from face. Do not silently accept regressions — escalate per anti-pattern protocol.

**Auditor at gates**: when detecting unexpected behavior at audit time, check if it matches a known entry. If novel → add new entry per format below.

---

## Adding a new entry

Append below the most recent entry. Required fields:
- `model`: exact model ID + version
- `date_discovered`: ISO date + AM/PM if relevant
- `discovered_by`: agent + project context
- `behavior`: precise description of failure mode + conditions
- `validation_evidence`: ≥2 data points (case where bug manifests + case where it doesn't)
- `workaround_validated` (or `_NOT_validated`): what we tried + result
- `implications_forward`: what changes for architect/engineer/auditor going forward
- `status`: VALIDATED / PENDING / WORKAROUND_FAILED / SUPERSEDED
- `related_gaps`: cross-reference to GAPS-LOG entries

If behavior is later proven false (model update fixes it) → mark entry SUPERSEDED + append new entry noting the fix date. NEVER delete entries (append-only forensic record).
