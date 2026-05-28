# lip-sync-workflow.md — Hailuo Std + Sync.so canonical workflow (Capa B horror-choice)

> **PRE-4.J BUILD 8 (2026-05-27)** post research + decisión Tomás: Sync.so PRIMARY only. Hedra deferred V6+.
>
> Razón arquitectural: Hailuo Std produce el VISUAL/motion completo (cuerpo en acción, atmósfera). Sync.so reemplaza SOLO región boca en el clip existente → **preserva la motion de Hailuo**. Hedra Character-3 generaría el clip from-scratch desde still+audio → perdería el body motion. Para horror-choice donde personajes tienen body action significativa (matarife con cuchillo, cocinera entre carcasas, etc.), Sync.so es el fit.

---

## Workflow canonical V5+

```
1. CP3 anchors  →  V5 character anchors (Gemini Nano Banana STRICT, still images)
2. CP4 Hailuo Std i2v   →  shot_NN.mp4 with character + motion (FACE VISIBLE, BOCA NEUTRA/CERRADA)
3. CP4.5 Sync.so post-process  →  shot_NN_lipsync.mp4 (mouth region replaced, body motion preserved)
4. CP4.6 atomic mux  →  shot_NN_atomic.mp4 (audio + captions baked) — via build_clip_atomic.py
```

Aplica SOLO a shots con `lip_sync_required: true` en SPEC. Otros shots saltan el step 3.

---

## SPEC field: `lip_sync_required` per shot (D17 architect audit)

Cada shot en `shot_list[]` DEBE declarar:
```yaml
shot_list:
  - shot_id: shot_05
    beat_role: consequence_A
    lip_sync_required: true   # character con cara visible hablando (dialog_text o character narration on-screen)
    ...
  - shot_id: shot_06
    beat_role: hook
    lip_sync_required: false  # POV first-person (sin cara) o character face-less (matarife casco)
    ...
```

**Regla de declaración:**
- **`true`** si: character con cara visible Y boca articulando (diálogo on-screen, narrator visible).
- **`false`** si: POV first-person (manos visibles pero no rostro del protagonista), character face-less (cleaver helmet, mask), narrator off-screen voiceover, escena ambiente sin character speech.

D17 architect auto-audit valida que **todos** los shots tengan el field declarado (no missing). El validador `audit-spec-lip-sync-marks.py` (BUILD 8) chequea consistencia: si shot tiene `dialog_text` o `speaker: character_*` Y `lip_sync_required: false` → FAIL inconsistencia.

---

## Hailuo prompt template para shots `lip_sync_required: true`

Per research community (Akool / Hedra / Curious Refuge 2026), el shot Hailuo base debe producir cara VISIBLE con boca en estado neutro (cerrada o ligeramente partida) para que Sync.so reemplace clean. **NUNCA escribir "talking" / "speaking" / "mouthing words" / "lips moving" / "shouting"** — Hailuo 2.3 inventa motion que pelea contra el overlay Sync.

**Template (extrapolated, community-sparse en stack exacto):**
```
Medium close-up of [character], [emotion via eyes/brow],
lips closed in [tense/soft] line, [subtle body motion: shallow
breathing / slight head tilt / blink], static camera with slow
push-in, [lighting], [atmosphere].
```

**Ejemplo concreto:**
```
Medium close-up of bearded man in flannel shirt, eyes wide with
fear, brow furrowed, lips closed tight, subtle shallow breathing,
slight tremor in shoulders, static camera with very slow push-in,
low-key tungsten light from below, dim cabin interior.
```

**Anti-patterns prompt (HALT):**
- ❌ "talking", "speaking", "moving lips", "shouting", "laughing", "screaming"
- ❌ Head turns / sudden angle changes (Hailuo pierde face shape)
- ❌ >3 camera moves; >3 prop elements

---

## Sync.so invocación canonical

**Vía Replicate** (recomendado — bypassa subscription gating sync.so):
- Model: `sync/lipsync-2-pro` (current 2026)
- Input: video mp4 (Hailuo shot output) + audio mp3 (TTS narrator/character)
- Output: mp4 con mouth region reemplazada
- Cost: ~$0.068/s estimado (Replicate pay-as-you-go, no subscription)
- Auth: REPLICATE_API_TOKEN

**Workflow CP4.5** (script forward, no built yet — flagged Phase 1 prioritization post-V5):
```python
# scripts/apply-sync-lipsync.py (TO BUILD — Phase 1 forward)
# Per shot with lip_sync_required: true:
#   1. Read shot_NN.mp4 (Hailuo output) + shot_NN_<character>_dialog.mp3 (TTS character voice)
#   2. Submit to Replicate sync/lipsync-2-pro
#   3. Download shot_NN_lipsync.mp4 → replace shot_NN.mp4
#   4. Log cost + duration
```

---

## Cuándo usar Sync.so vs minimizar shots-cara-hablando (design recommendation)

Horror-choice canonical favors **POV first-person + face-less / mask characters** (matarife casco-cuchillo, viewer POV sin rostro). Esto reduce shots con cara visible hablando → menos uso Sync.so → menos $. **Default V5: minimizar shots `lip_sync_required: true`**. Solo cuando el character ROSTRO ES central a la beat (e.g., dialog dramatic close-up).

Forward consideración: Hedra (deferred V6+) para shots talking-head puros donde queremos generar avatar from-scratch (sin Hailuo base). Útil para creature/doll talking-head inserts donde Hailuo struggle con cara stylized.

---

## Validación pre-CP4 (BUILD 8 audit-spec-lip-sync-marks.py)

`audit-spec-lip-sync-marks.py` valida:
1. **Cobertura**: TODOS los shots tienen `lip_sync_required` declarado (no missing).
2. **Consistencia**: si shot tiene `dialog_text` o `narration_in_this_shot.speaker` matching `character_*`, entonces `lip_sync_required: true`. Si `false` → FAIL inconsistencia.

Capability-gated: solo aplica si `format_type: interactive_choice` AND `has_layer_2_effects: true`. Otros formatos NO necesitan lip sync gate.

---

## References

- Research findings: 2026-05-27 WebSearch (Hedra/Sync.so pricing + Hailuo prompt community).
- [Sync.so lipsync-2-pro](https://sync.so/lipsync-2-pro) · [Replicate sync model](https://replicate.com/sync/lipsync-2-pro)
- [Hedra Lip Sync Guide](https://www.hedra.com/blog/ai-lip-sync-video-guide) (referencia neutral pre-shoot)
- [Akool Hailuo Prompt Guide](https://akool.com/blog-posts/minimax-hailuo-video-prompt-guide)
