# HANDOFF-PROTOCOL.md — Workflow arquitecto ↔ ingeniero con 5 checkpoints

> El arquitecto NO entrega un SPEC y desaparece. Hay 5 checkpoints donde valida lo que el ingeniero produce antes de seguir. Esto evita re-generación en cascada cuando algo no matchea intent.

---

## El flujo completo

```
USER ─[describe video]──> ARQUITECTO
                              │
                              ▼
                  ┌── Entrevista user (INTERVIEW-FLOW)
                  ▼
                  ┌── Diseña CREATIVE-SPEC.yaml v1
                  ▼
                  USER aprueba SPEC ────[NO]────> iterar arquitecto
                  │
                  [YES]
                  ▼
                  CREATIVE-SPEC.yaml → handoff a INGENIERO
                  │
                  ▼
        ╔══════════════════════════════════════════════════╗
        ║       LOOP DE PRODUCCIÓN CON 5 CHECKPOINTS       ║
        ╠══════════════════════════════════════════════════╣
        ║                                                  ║
        ║  CHECKPOINT 1: Reference Anchors                 ║
        ║      Ingeniero → genera bruno_anchor + pablo     ║
        ║      Arquitecto → valida visualmente             ║
        ║      [NO] → re-generar anchor / ajustar prompt   ║
        ║      [YES] ↓                                     ║
        ║                                                  ║
        ║  CHECKPOINT 2: Base Images                       ║
        ║      Ingeniero → genera todas las images shots   ║
        ║      Arquitecto → valida coherencia + character  ║
        ║      [NO] → re-generar shots específicos         ║
        ║      [YES] ↓                                     ║
        ║                                                  ║
        ║  CHECKPOINT 3: Audio Assets                      ║
        ║      Ingeniero → genera TTS + SFX + music + amb  ║
        ║      Arquitecto → escucha + valida intent        ║
        ║      [NO] → re-generar assets específicos        ║
        ║      [YES] ↓                                     ║
        ║                                                  ║
        ║  CHECKPOINT 4: Animation Clips                   ║
        ║      Ingeniero → genera Kling/Seedance/etc clips ║
        ║      Ingeniero → ITERA modelos lip sync          ║
        ║      Arquitecto → valida motion + lip sync       ║
        ║      [NO] → iterar tool o ajustar intent         ║
        ║      [YES] ↓                                     ║
        ║                                                  ║
        ║  CHECKPOINT 5: Draft Render                      ║
        ║      Ingeniero → compone en HyperFrames + render ║
        ║      Ingeniero → pre-render-gate (24 Q Y/N)      ║
        ║      Arquitecto → review creativo final         ║
        ║      User → HUMAN-CHECKLIST                      ║
        ║      [NO] → re-componer + iterar                 ║
        ║      [YES] ↓                                     ║
        ║                                                  ║
        ╚══════════════════════════════════════════════════╝
                  │
                  ▼
                ✅ VIDEO LISTO PARA PUBLICAR
```

---

## ⛔ Self-audit obligatorio antes de cada approval gate

**Antes de entregar el deliverable de CUALQUIER checkpoint al arquitecto, el ingeniero hace self-audit primero.** No es opcional. Detalle del formato en `video-director/SKILL.md` § SELF-AUDIT.

Flujo por checkpoint:
```
1. Pre-checkpoint checklist (5 puntos en chat) — ver video-director/SKILL.md
2. Producir deliverable
3. SELF-AUDIT: abrir output, verificar vs SPEC, assessment honesto
4. Si self-audit dice "flojo" → 1 regen propia antes de molestar al arquitecto
5. Reportar al arquitecto: deliverable + self-audit + assessment
6. Arquitecto valida y aprueba/rechaza
```

Sin self-audit, cada checkpoint desperdicia 1 iteración. El ingeniero conoce el SPEC tan bien como el arquitecto — debe filtrar antes de entregar.

---

## 📋 Template literal de reporte por checkpoint (OBLIGATORIO copy-paste)

**El ingeniero NO procede sin postear este template completado en chat.** No es resumen ni "ya lo pensé internamente" — es copy-paste literal con los campos llenos.

### A) PRE-FASE — antes de generar nada del checkpoint

````markdown
# 📋 PRE-CHECKPOINT [N] REPORT

## Lectura obligatoria completada
- [ ] `PAUTA-MASTER.md` § X (cita sección relevante)
- [ ] `LIBRARY.md` — reuso encontrado: [path absoluto / "nada reusable, justificar"]
- [ ] `SKILL.md` del formato — sub-doc específico del checkpoint
- [ ] Otros docs: [lista]

## SPEC slots involucrados en este checkpoint
- Slot X: [resumen breve de qué uso]
- Slot Y: [...]

## Cross-shot coverage audit (CP1 obligatorio, otros si aplica)
| Tipo | Item | Count shots | ¿Anchor en SPEC? |
|------|------|-------------|------------------|
| character | MAIKOL | 4 | ✓ STRICT |
| character | CHELO | 2 | ✓ STRICT |
| setting | salon | N | ✓ / ✗ FLAG |
| setting | cubierta | N | ✓ / ✗ FLAG |
| prop | mate | N | ✓ / ✗ FLAG (si setup→payoff) |
| prop | termo | N | ✓ / ✗ FLAG |

**Gaps detectados**: [lista de FLAG ✗ → aplicá AUTONOMY MATRIX: si fix obvio + within budget → FIX, si 3+ opciones → ESCALAR]

## Fixes autónomos aplicados (engineer domain — NO requieren approval)
> Solo declarativo. Cubre auto-correcciones técnicas, swaps de target del anchor, ajustes de prompt language, model choice, cost ajustado dentro de budget_target. Detalle en `video-director/SKILL.md` § AUTONOMY MATRIX.

- [Fix 1: ej. "signal of trap" → "warm steady light contrasting" en salon prompt — interpretación propia retirada]
- [Fix 2: ej. 5to anchor: mate → copa-champagne — cross-shot audit reveló copa con 5 shots setup→payoff y mate ya doble-anclado]
- [Fix 3: ej. cost ajustado $0.50→$0.65 — 6.5% del budget_target $10, dentro de mandato]
- [...] o "ninguno aplicado en este checkpoint"

## Self-audit criteria (qué voy a verificar POST-generación)
1. [criterio 1: ej. wardrobe MAIKOL matchea visual_anchor_prompt]
2. [criterio 2: ej. paleta cubierta = warm/golden/Ghibli style]
3. [criterio 3: ej. NO personas en frame de anchors de setting]

## Plan de ejecución
- Comando 1: [...]
- Costo estimado (post-fixes autónomos): $X.XX
- Tiempo estimado: ~X min

⏸ Procediendo — sin esperar confirmación si todos los ítems son engineer domain.
⏸ ESPERANDO confirmación arquitecto SOLO si alguna decisión cae en "ESCALAR siempre" del AUTONOMY MATRIX.
````

### B) POST-FASE — después de producir el deliverable, ANTES del approval gate

````markdown
# 🔍 POST-CHECKPOINT [N] SELF-AUDIT

## Deliverables producidos
- `path/file1.png` — [descripción]
- `path/file2.png` — [descripción]

## Verificación cara-a-cara vs SPEC
| Item | SPEC requirement | ¿Matchea? | Notas |
|------|------------------|-----------|-------|
| MAIKOL.cabello | "negro grasoso pegado por agua salada" | ✓ / ✗ | [...] |
| MAIKOL.piel | "plástica pálida con cristales de sal" | ✓ / ✗ | [...] |
| salon.iluminacion | "focos amarillos parpadeantes + disco" | ✓ / ✗ | [...] |
| ...todos los items críticos del SPEC | | | |

## Fixes autónomos aplicados durante la generación
> Cualquier auto-corrección técnica que hiciste mientras producías (ej. cambiar negative prompt, ajustar resolution, swap de model). Si caen en AUTONOMY MATRIX § FIX autónomo → solo declarativo, no requieren approval.

- [...] o "ninguno"

## Checks técnicos críticos añadidos post-maikol-crucero (2026-05-15)
> Aplicar SIEMPRE en CHECKPOINT 4 (Animations) y CHECKPOINT 5 (Render). Aplicar selectivamente antes según relevancia.

| Check | Pregunta | Aplica en |
|-------|----------|-----------|
| **Clip duplication** | ¿Algún clip animado (data-source de Kling) aparece >1 vez en el timeline? | CP4, CP5 |
| **Character continuity** | ¿Cada personaje recurrente está presente consistentemente entre shots ligados narrativamente? (ej. bueno aparente NO debe desaparecer entre cliffhanger y wrap) | CP4, CP5 |
| **UI overlap with subject** | ¿Algún UI element (countdown, choice button, CTA) se superpone al subject focus o a texto dentro de la imagen? Cross-check vs INGENIERO-PAUTA-MASTER § 7 safe zones | CP5 |
| **Motion per shot** | ¿Hay ≥3 shots consecutivos sin Kling motion fuera del hook? (ver INGENIERO-PAUTA-MASTER § 5.6) | CP4, CP5 |
| **Lip sync coherence** | Para cada Kling clip animado: ¿el audio en ese timestamp es character dialogue (lip_sync OK) o narrator (lip_sync prohibido)? Ver INGENIERO-PAUTA-MASTER § 8.5 | CP4, CP5 |
| **Narrative flow** | ¿Cada transición entre shots tiene conexión lógica clara? ¿Hay saltos sin shot intermedio (ej. mirrors→agua sin transition)? Reportar al arquitecto si falta. | CP5 |
| **Pace WPM** | Después de TTS: medir speaking WPM. ¿Está en p25-p75 (153-180)? Ver INGENIERO-PAUTA-MASTER § 1.1 | CP3, CP5 |
| **Visual-narration coherence per shot** (añadida 2026-05-16) | ¿Cada shot tiene visual LITERAL que matchea narration en ese timestamp? Cross-check SPEC v6 `visual_action_match.matches_literal: true` con render real | CP4, CP5 |
| **Contact sheet post-CP2** (añadida 2026-05-16) | ¿Generé grid temporal 5×5 de shots y validé flow narrativo HOLÍSTICO (no shot-by-shot)? Caso cabina-14: optimizar shots aislados → render reveló 10 issues | CP2, CP5 |
| **TTS duration measured** (añadida 2026-05-16) | ¿Medí TTS reales pre-wire HTML y ajusté layout sobre DURACIONES REALES (no SPEC target abstracto)? Mismatch entre estimate y real = bugs de timing | CP3, CP4 |
| **Camera spec compliance** (añadida 2026-05-17 schema v7) | ¿Cada shot del render tiene `camera` block respetado (shot_type + movement + lens_hint exactos del SPEC)? Sin esto prompts Kling/Hailuo divergen del intent arquitecto. Cross-check SPEC v7 `shot_list[].camera` con prompts realmente usados. | CP2-CP5 |
| **Mini-cuts implementation** (añadida 2026-05-17 schema v7) | Shots de `narrative_function: cuts_flooding` ¿tienen mini-cuts implementados (5-7 cuts por shot)? Cross-check SPEC v7 `mini_cuts_internal` con render real. Sin esto perdés pattern ref-13 signature. | CP4-CP5 |
| **Voice processing applied** (añadida 2026-05-17 schema v7) | Characters con `audio_strategy.character_voice_processing` block ¿tienen voice generated con specs exactas (effects chain order respetada)? Pass side-by-side test con `reference_canónico` definido en SPEC. | CP3-CP5 |
| **Color LUT applied** (añadida 2026-05-17 schema v7) | LUT/CSS filter aplicado en render matchea `aesthetic_strategy.color_grading_luts.<palette_id>` del SPEC? Cross-check CSS filter values + reference cinematográfica. | CP5 |

---

## ⛔ GATES INCREMENTALES DE RENDER (añadidos 2026-05-16)

Render incremental por checkpoint — captura bugs temprano vs descubrirlos al final. OBLIGATORIO.

```
Post-CP1: render anchor draft (1 frame contact sheet con todos los anchors)
          → valida character consistency + setting + props
Post-CP2: render shots draft (grid temporal 5×5 — VALIDAR FLOW HOLÍSTICO)
          → valida narrativa, NO solo unidades aisladas
Post-CP3: measure TTS durations reales, si total > sweet spot ESCALAR antes de wire
          → previene timing bugs estructurales
Post-CP4: render incremental sin captions (validar animation AI + audio sync narrativo)
          → valida match visual-audio antes de overlays
```

**Razón**: caso cabina-14 (2026-05-15) — engineer optimizó 16 shots aisladamente, render final reveló 10 issues que se hubieran detectado en 5 min con render parcial. 4h gastadas en optimización ciega.

**Anti-pattern**: "voy a perfeccionar cada shot antes de renderizar" = trampa clásica del ingeniero. Units OK pero sistema falla. Ver memoria `feedback_render_incremental_early.md`.

---

## Self-assessment honesto
- TOP TOP / aceptable / flojo: [veredicto]
- Si flojo → ¿regen propia o flag arquitecto? [decisión per AUTONOMY MATRIX]
- Cost real vs estimado: $X.XX / $X.XX

## Listo para architect approval gate?
- [ ] Sí, todo matchea + checks técnicos críticos pasados → mando al arquitecto
- [ ] No, regen propia primero (1 iteración interna — engineer domain)
- [ ] No, flag al arquitecto (limitación técnica o slot contradiction — architect domain)
````

**Si el ingeniero omite cualquier campo del template → arquitecto rechaza y exige completarlo antes de aprobar.**

---

## CHECKPOINT 1 — Reference Anchors

### Qué entrega el ingeniero
- 1 imagen anchor por cada personaje recurrente del SPEC (`reference_anchors.characters[]`)
- 1 imagen anchor por cada setting que aparece >2 shots (`reference_anchors.settings[]`)
- 1 imagen anchor por cada prop recurrente con función setup→payoff (`reference_anchors.props[]`)
- Generadas con tool premium (Nano Banana Pro / Seedream 4.5 Sequence Mode / Flux Kontext)
- Posa neutral, plain background, photorealistic
- **Self-audit completo antes de entregar** (matchea visual_anchor_prompt? wardrobe? proportions? signature elements?)

### Qué valida el arquitecto
- ✅ Character matchea el intent del visual_anchor_prompt
- ✅ Proportions correctas (cíclope tiene cuello largo, tubérculo es ovoide, etc.)
- ✅ Wardrobe correcto
- ✅ Visual signature elements presentes (e.g., red tape en helmet de Bruno)
- ✅ Photorealistic quality (no plastic AI look)

### Failure modes y acciones

| Fail | Acción |
|------|--------|
| Anatomía incorrecta (cuello no 3x, ojo único mal posicionado) | Ajustar anchor prompt + regenerar |
| Look plastic/cartoon AI | Cambiar tool (probar Flux Pro o Seedream 4.5) |
| Wardrobe incorrecto | Especificar SETTING-APPROPRIATE más detallado en prompt |
| Character drift entre 2 anchors generados | Usar SAME seed o Sequence Mode estricto |

### Max iteraciones recomendadas
3 por anchor. Si tras 3 iter no matchea → ingeniero flaguea via feedback_protocol con limitación técnica.

### Tiempo estimado
~30 min por anchor (incluyendo 1-2 iteraciones).

---

## CHECKPOINT 2 — Base Images

### Qué entrega el ingeniero
- 1 imagen por cada shot del SPEC (~22-28 imágenes)
- Generadas usando anchors approved como reference (IP-Adapter / multi-image conversation)
- Coherencia entre shots verificada
- Composition + lighting + atmosphere matching intent per shot

### Qué valida el arquitecto
- ✅ Character consistency cross-shots (mismo Bruno en TODOS sus shots)
- ✅ Lighting matchea intent
- ✅ Composition matchea intent (POV, medium, close-up, etc.)
- ✅ Color emphasis correcto (paleta dual + accent isolation)
- ✅ Atmosphere visible (polvo, niebla, vapor)
- ✅ Mood comunica intent

### Failure modes y acciones

| Fail | Acción |
|------|--------|
| Character drift entre shots | Re-generar con anchor más estricto |
| Lighting incoherente con setting | Re-prompt con lighting más específico |
| Composition wrong (medium en lugar de close-up) | Re-prompt con composition explícita |
| Atmosphere ausente (sin polvo/niebla) | Re-prompt con atmosphere más enfático |

### Max iteraciones recomendadas
2 por image. Si shot crítico no funciona en 2 iter → escalate al arquitecto con alternativas.

### Tiempo estimado
~45-60 min por video completo (22-28 imágenes).

---

## CHECKPOINT 3 — Audio Assets

### Qué entrega el ingeniero
- TTS por cada script segment (~25-30 TTS clips)
- SFX por cada evento en asset_list (~25-35 SFX prompts generados)
- Music tracks (main + outro)
- Ambient loops (mina + outro cozy)
- Todos con duration medida real

### Qué valida el arquitecto
- ✅ Voice character matchea intent (deep voice + intimate)
- ✅ Multi-narrator processing distinto per character
- ✅ Dialogue lines tienen delivery correcto (whisper, urgency, etc.)
- ✅ Pausas dramáticas respetadas (pause_after_strict_seconds)
- ✅ SFX matching prompt intent
- ✅ Music genre + BPM correcto
- ✅ Ambient layers presentes y continuos

### Failure modes y acciones

| Fail | Acción |
|------|--------|
| TTS voice no matchea intent (no es intimate enough) | Iterar voice ID / processing |
| Pace incorrect | Re-generate con `<break>` markers ajustados |
| SFX genérico/no match | Re-prompt ElevenLabs SFX con más detalle |
| Music BPM wrong | Re-generate con BPM specific |
| Ambient corto | Loop expansion con ffmpeg |

### Max iteraciones recomendadas
2 por asset.

### Tiempo estimado
~1h para video completo (todos los TTS + SFX + music + ambient).

---

## CHECKPOINT 4 — Animation Clips

### Qué entrega el ingeniero
- 1 clip animation por cada shot que requiere motion real (HERO + STANDARD tier)
- Tier-appropriate model (Kling 2.5 Turbo Pro / Seedance / Hailuo / LTX)
- Lip sync clips para shots con dialogue (Hedra Character-3 primary, iterar fallbacks)
- Motion intent respetado (lo que se anima Y lo que NO se anima)

### Qué valida el arquitecto
- ✅ Motion intent matchea (Bruno parpadea ojo único correcto)
- ✅ Lip sync se ve natural (boca matchea articulación español)
- ✅ Character consistency mantiene entre frame de anchor y frames de animation
- ✅ Audio-reactive events sincronizados (SFX impact + visual punch)
- ✅ Transitions entre shots feel intentional
- ✅ NO motion de elementos que arquitecto dijo "NOT to animate"

### Failure modes y acciones — incluyendo lip sync iteration

| Fail | Acción |
|------|--------|
| Lip sync stiff / robotic (Hedra falla) | Probar Sync.so post-process encima del clip |
| Lip sync falla character match | Veo 3.1 native audio (premium fallback) |
| Lip sync sigue fallando | Kling 3.0 Omni multilingual |
| Character drift severo | Re-generate con tier HERO (más caro pero coherente) |
| Motion extras no intencional | Re-prompt con "DO NOT animate X" más explícito |
| Audio sync off | Ajustar timing en HyperFrames timeline, no re-generate |

### Max iteraciones por lip sync shot
3 (probando Hedra → Sync.so → Veo / Kling Omni). Si todos fallan → flag a arquitecto, considerar eliminar dialogue o cambiar a non-lip-sync shot.

### Tiempo estimado
~1-2h para video completo (dependiendo cuántos lip sync shots).

---

## CHECKPOINT 5 — Draft Render

### Qué entrega el ingeniero
- Video MP4 1080x1920 30fps H.264/AAC -14 LUFS
- Composed en HyperFrames con:
  - Images + animations en track de video
  - TTS + music + SFX + ambient en tracks de audio
  - Captions sync con Whisper
  - UI elements overlays (countdown, loaders, buttons, watermark)
  - Color grading aplicado (CSS filters + LUTs)
  - Vignette + film grain overlays
- Pre-render-gate (24 Q, Q1-Q25 salta Q23) PASADO

### Qué valida el arquitecto (creative review)
Ver `architect-final-review.md` checklist creativa. Resumen:
- ✅ Hook agarra atención en 3s
- ✅ Stakes vitales se sienten
- ✅ Twist (si hay) cumple 3 condiciones
- ✅ Counterfactual outro carga catharsis
- ✅ Keyword highlights visibles + impacto
- ✅ Lip sync natural (no robótico)
- ✅ Coherencia visual cross-shots
- ✅ Audio se entiende en altavoz móvil
- ✅ Felt cadence 18-30 events/min

### Qué valida el user (HUMAN-CHECKLIST)
Las 7 preguntas del `video-director/HUMAN-CHECKLIST.md`.

### Failure modes y acciones

| Fail | Acción |
|------|--------|
| Hook no agarra | Re-iterar primer shot (animation + caption) |
| Lip sync se nota robótico | Volver a CHECKPOINT 4 con tool iteration |
| Audio compitiendo (no entiende voiceover) | Ajustar mix levels + ducking |
| Caption off-sync | Re-Whisper + sync |
| Color grading uniforme | Aplicar paleta dual explícita por sección |

### Max iteraciones totales
3 drafts. Si tras 3 no convergemos → escalate al user con opciones de scope (acortar duración, simplificar dyad, etc.).

### Tiempo estimado
~1-2h para compose + render + QA gates.

---

## Tiempo total estimado de producción

| Checkpoint | Tiempo |
|------------|--------|
| 1 — Anchors | 30-60 min |
| 2 — Images | 45-90 min |
| 3 — Audio | 60-90 min |
| 4 — Animations | 60-120 min |
| 5 — Render + QA | 60-120 min |
| **TOTAL** | **~5-8h** por video |

Costos típicos por video:
- Image gen: ~$1-3
- TTS: ~$2-3
- SFX: ~$5-10
- Animation (mix tiers): ~$5-15
- **Total assets: $13-30**
- Plus engineer time + iteration

---

## Cuando los checkpoints fallan repetidamente

Si CHECKPOINT N falla 3+ veces sin convergencia:

1. **Engineer flagea** via `feedback_protocol` (ver SKILL.md)
2. **Arquitecto recibe** flag con:
   - Lo que se pidió
   - Lo intentado
   - Por qué falla técnicamente
   - 2-3 alternativas propuestas
3. **Arquitecto decide:**
   - Accept alternative
   - Adjust spec
   - Escalate to user

---

## Comunicación durante producción

### Format de status del ingeniero

Cada checkpoint, el ingeniero reporta brevemente:

```
[Checkpoint N status]
✅ Completed: X items
⚠️ Iterating: Y items (current iteration / max)
❌ Failed: Z items (flagged for architect review)

Next: Awaiting architect approval for [list of items]
```

### Format de respuesta del arquitecto

```
Checkpoint N review:
✅ Approved: [list]
⚠️ Re-do with adjustment: [list with new instructions]
❌ Cannot proceed: [list with escalation]

Proceed to checkpoint N+1: yes/no
```

---

## Iteraciones eficientes vs ineficientes

### ✅ Iteración eficiente
- Engineer flagea PROBLEMA específico
- Arquitecto da instrucción CLARA de ajuste
- Engineer re-genera SOLO lo problemático
- Re-validar en mismo checkpoint

### ❌ Iteración ineficiente
- Engineer entrega todo final, arquitecto revisa todo, encuentra issues en checkpoint 1 → re-do everything
- Por eso los CHECKPOINTS INTERMEDIOS existen.

---

## Excepción: producción fast-track

Si el arquitecto y el ingeniero ya tienen experiencia juntos en el formato (ej. video #5+ de la serie), pueden:
- Saltar CHECKPOINT 2 (validar solo problemáticos)
- Saltar CHECKPOINT 4 (validar solo lip sync)
- Mantener CHECKPOINTS 1 (anchors) y 5 (final) siempre

Para video #1 de nuevo formato → TODOS los checkpoints obligatorios.

---

## Cómo este protocolo se enchufa con el SPEC

El SPEC tiene una sección `checkpoints:` que enumera explícitamente los 5 checkpoints con `approval_required: true`. El ingeniero NO procede al siguiente checkpoint hasta que el anterior tenga approval.

Esto convierte el workflow en gates determinísticos, no flow opcional.
