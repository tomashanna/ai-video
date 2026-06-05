# architect-final-review.md — Checklist creativa post-draft

> Después de que el ingeniero rinde el draft.mp4 + pasa pre-render-gate (24 Q, Q1-Q25 salta Q23), el arquitecto valida las dimensiones CREATIVAS. Esto complementa el gate técnico — no lo reemplaza.

---

## Cuándo se ejecuta

**Después de:**
- ✅ CHECKPOINT 5 completed (draft.mp4 generated)
- ✅ Pre-render-gate (24 Q, Q1-Q25 salta Q23) PASSED (engineer validation técnica)

**Antes de:**
- ❌ User HUMAN-CHECKLIST
- ❌ Publishing

---

## Las 12 dimensiones creativas a validar

El arquitecto MIRA EL VIDEO COMPLETO y responde Y/N a estas 12 preguntas:

### 1. Hook 0-3s funciona?
- [ ] Visual uncanny extreme en frame 0 (no setup descriptivo)
- [ ] Caption warning o dilema explícito presente en primeros 2s
- [ ] Countdown UI visible antes de 3s
- [ ] Si lo viera scrolling, NO haría scroll
- [ ] Match con `hooks.md` fórmula elegida

**Si NO funciona:** identificar cuál sub-elemento falla → fix solo eso.

### 2. Character design uncanny llega?
- [ ] Personaje peligroso comunica menace visual SIN narración
- [ ] Personaje seguro comunica cozy/safe visual
- [ ] Character consistency cross-shots (mismo Bruno en todos sus shots)
- [ ] Detalles signature (cuello largo, ojo único, etc.) visibles claramente
- [ ] Pareciera @referent-a level (no AI generic)

**Si NO:** anchor image puede haber drift — re-generate específicos.

### 3. Stakes son vitales y se sienten?
- [ ] Stakes mencionados son muerte/supervivencia (no triviales)
- [ ] Consecuencias visualizadas concretamente (no abstractas)
- [ ] Curva ascendente H3 → H4 → H5
- [ ] Clímax (post-H5) es la imagen MÁS impactante del video

**Si NO:** stakes deben re-escalarse en script o re-visualizarse.

### 4. Decisiones encadenadas narrativamente?
- [ ] Decisión 1 lleva lógicamente a setup de Decisión 2
- [ ] Decisión 2 lleva lógicamente a setup de Decisión 3
- [ ] Pattern elegido (de matriz) coherente todo el video

**Si NO:** revisar story_arc.md narrative beats.

### 5. Twist (si hay) funciona?
- [ ] Lógica clara — viewer puede explicar en 1 frase
- [ ] Imágenes acompañan (visual evidence)
- [ ] Narración explica el link explícitamente
- [ ] Setup retroactivo plantado 2.5-3.5s on-screen

**Si NO:** twist se siente "deus ex machina" — fix setup + narración explícita.

### 6. Counterfactual outro carga catharsis?
- [ ] Cambio tonal RADICAL vs horror previo (warm vs cool, soft vs hard)
- [ ] Punchline tiene detalles específicos (no genérico)
- [ ] Música cambia a folk/cozy/diferente
- [ ] El viewer SUSPIRA después del outro

**Si NO:** outro NO está cargando catharsis — re-iterar.

### 7. Lip sync se ve natural?
- [ ] Si hay dialogue, lip movement matchea articulación natural del español
- [ ] No se ve robótico/stiff
- [ ] Character visual matchea anchor cuando habla
- [ ] Si lip sync queda mal → engineer debe iterar tool

**Si NO:** flag al ingeniero para iterar Hedra → Sync.so → Veo / Kling Omni.

### 8. Felt cadence ~18-30 events/min?
- [ ] Cero frames estáticos > 2s
- [ ] Cuts + push-ins + parallax + caption swaps suman ~50-70 events/min
- [ ] Video se siente "vivo" no slideshow

**Si NO:** agregar internal motion o cuts perceptibles.

### 9. Keyword highlights visibles e impactan?
- [ ] 5-10 keywords destacadas inline en captions
- [ ] Color matching categoría (rojo peligro, amarillo nombres, cyan seguros)
- [ ] Scale pop sutil al aparecer
- [ ] No se ve "demasiado highlight" (overload)

**Si NO:** ajustar captions strategy.

### 10. Audio quality
- [ ] Voiceover se entiende clara en altavoz móvil
- [ ] Music NO compite con voz (ducking activo)
- [ ] SFX impacts pegan (white flash, sub-bass, taladro)
- [ ] Cero dead zones (silencio prolongado mid-video)
- [ ] Ambient continuo presente

**Si NO:** mix issues, engineer ajusta levels.

### 11. Color grading dual psicológica funciona?
- [ ] Escenas peligrosas tienen paleta opuesta a escenas seguras
- [ ] Color isolation accent (e.g., rojo medidor) visible donde corresponde
- [ ] Vignette pronunciada
- [ ] Crushed blacks + high contrast
- [ ] Outro contrasta tonalmente vs horror

**Si NO:** color grading necesita refinement por sección.

### 12. Brand identity presente?
- [ ] Watermark del creator visible toda la duración
- [ ] Tagline signature en hook
- [ ] Cliffhanger/loop CTA al final (si pattern lo requiere)
- [ ] Easter eggs visibles si fueron planeados
- [ ] Reel caption para Instagram listo

**Si NO:** completar brand elements faltantes.

---

## Veredicto final

| Resultado | Acción |
|-----------|--------|
| **12/12 Yes** | ✅ APROBADO. Pass al user para HUMAN-CHECKLIST. |
| **1-3 No** | ⚠️ Iterar SOLO esas dimensiones. Re-render. Re-validate. |
| **4-6 No** | 🟡 Revisar SPEC con engineer — issues estructurales. Posible volver a Checkpoint 3 o 4. |
| **7+ No** | 🔴 Algo fundamental falla. Re-design del SPEC desde fase 2 con engineer feedback. |

---

## Cómo el arquitecto reporta al engineer

```
🏛️ ARCHITECT REVIEW — Draft v1

✅ Approved dimensions: [list]
⚠️ Requires iteration: [list with specific instructions]
❌ Blocking issues: [list with escalation if any]

Proceed to user HUMAN-CHECKLIST: yes / no
```

---

## Ejemplo de review

```
🏛️ ARCHITECT REVIEW — mina-kraven-v1 Draft v1

✅ Approved:
- D1 Hook funciona (visual + warning + countdown)
- D2 Character design (Kraven cíclope cuello largo coherente)
- D3 Stakes vitales claros
- D5 Twist cumple 3 condiciones
- D8 Felt cadence ~22 events/min
- D9 Keyword highlights buenos
- D11 Color grading dual funciona
- D12 Brand identity completa

⚠️ Requires iteration:
- D6 Counterfactual outro: la música no cambia suficientemente
  → Engineer: iterar music outro a folk acústico más marcado vs drone horror
- D7 Lip sync de Kraven en shot 5 se ve robótico
  → Engineer: probar Sync.so post-process sobre clip Kling

❌ No blocking issues.

Once D6 + D7 fixed → proceder a user HUMAN-CHECKLIST.
```

---

## Anti-patterns en el review del arquitecto

❌ **Aprobar sin mirar el video completo** → fail.
❌ **Rechazar todo sin specificar qué fixear** → engineer paralizado.
❌ **Pedir cambios fuera del scope creative** ("subí el LUFS a -13") → es del ingeniero.
❌ **No documentar issues** → engineer no sabe qué iterar.
❌ **Iterar infinitamente** → escalate a user después de 3 drafts.

---

## Diferencia vs pre-render-gate (engineer's checklist)

| Pre-render-gate (engineer) | Architect final review (este doc) |
|----------------------------|-----------------------------------|
| 24 Q técnicas Y/N (Q1-Q25 salta Q23) | 12 dimensiones creativas Y/N |
| Verifica scripts QA copiados | Verifica intent creativo se logró |
| Verifica LUFS -14 ±0.5 | Verifica AUDIO se entiende en móvil |
| Verifica cuts/min 2-7 | Verifica felt cadence 18-30 events/min |
| Verifica vignette aplicado | Verifica color grading dual psicológica |
| Verifica captions no overlap | Verifica keyword highlights impactan |
| Verifica narration coverage ≥70% | Verifica counterfactual outro carga catharsis |
| Verifica learnings appended to video-log.md | Verifica twist funciona (3 condiciones) |

**Los dos son obligatorios. Engineer's gate primero (técnico). Architect's review después (creativo).**

---

## Cuándo declarar "listo para publicar"

```
✅ Pre-render-gate engineer: 20/20 passed
✅ Architect final review: 12/12 passed
✅ User HUMAN-CHECKLIST: 7/7 passed

→ PUBLICAR
```

Si alguno NO está al 100% → NO publicar. Iterar.
