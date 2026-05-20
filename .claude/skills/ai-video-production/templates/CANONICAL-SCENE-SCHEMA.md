# CANONICAL-SCENE-SCHEMA.md — Template per-scene markdown

> Schema canónico que cada `canonical-scenes/ref-XX.md` sigue per scene.
> Copy-paste el bloque "Scene N" abajo y llenar campos.
> Si dato no se puede determinar del raw data → `[NEEDS VALIDATION]` (NUNCA inventar).

---

## File header obligatorio (al inicio de cada ref-XX.md)

```markdown
# Canonical scene-by-scene — ref-XX

**Source video**: /videosref_elige_tu_compa/ScreenRecording_XXX.MP4
**Pattern**: P[1-10] (per PAUTA-MASTER § 15)
**Score Gemini empirical**: X.XX/10 (per PAUTA-MASTER § 0 table)
**Duration total**: XX.Xs
**Total scenes (de-clustered)**: N
**Last validated**: YYYY-MM-DD by [agent draft / user manual]

> ⚠️ **DISCLAIMER**: Este doc es **ejemplo empírico canónico**, NO template rígido.
> Adaptá STRUCTURE (timing, transiciones, pattern flow) con TU historia/characters.
> NO copies línea por línea — un video que clona ref-XX con nombres cambiados es plagio, no creatividad.
> El formato es el generador, no el límite.
> Ver PAUTA-MASTER.md § 1 para filosofía.

---
```

---

## Per-scene block (copy-paste y llenar)

```markdown
## Scene N — [MM:SS_start - MM:SS_end] ([duration]s)

**Pattern category**: hook | setup_post_hook | decision_setup | decision_countdown | consequence_A | rama_B_transition | consequence_B | cliffhanger
<!-- valid categories per PAUTA-MASTER § slots E/G + sprint combinado v6 narrative_function enum -->

**Who's physically in scene**: [character_id, character_id, ...]
<!-- LITERAL list. POV viewer NOT included aquí (implícito si camera POV). -->

**Camera / shot type**: POV | wide | medium | close-up | over-shoulder + [movement]
<!-- movement: static | push-in | dolly | pan | handheld | whip-pan -->

**Setting**: [setting_name] + [key elementos diegéticos]
<!-- diegetic = visible in frame, not abstract -->

**Action LITERAL**:
- character_X: "verbo + objeto + cómo"
  <!-- LITERAL action. NO "appears uncanny". SÍ "gira 90° hacia cámara, sonrisa contenida" -->
- character_Y: "..."
- viewer (POV): "qué ve / siente" — solo si POV shot

**Narration text** (literal from transcription.json):
"..."
<!-- Texto exacto del Whisper segment overlapping este timestamp. Si span múltiples segments, listarlos: -->
<!-- - [start-end]s: "..." -->
<!-- - [start-end]s: "..." -->

**Character dialogue** (if any):
- character_X: "..."
<!-- VACÍO si solo narrator. -->

**Visual-narration coherence**:
"how visual matches narration LITERAL"
<!-- 1 sentence. Si NO matchea (canónico tiene visual decorativo no-literal) → flag. -->

**UI elements active**:
- countdown | choice_buttons | loading_bar | name_label | caption_narration | caption_warning | watermark
<!-- Cross-ref con ui-elements.json keyframes en este rango. -->

**Animation tier observed**:
Kling_full | Hailuo | Seedance | static_KenBurns | unknown
<!-- Heurística: frame-to-frame diff alto = animation full. Diff bajo + Ken Burns visible = static. -->
<!-- Si no se puede determinar visualmente → [NEEDS VALIDATION] -->

**Pattern observation**:
- [por qué esta scene funciona canónicamente — pattern recognition vs PAUTA-MASTER]
- [qué otras refs hacen en este timestamp/pattern_category similar]
- [outlier observations si aplica]
```

---

## Pattern_category — definiciones (alineadas con SPEC v6 narrative_function enum)

| Category | Rango típico (% video) | Qué pasa |
|---|---|---|
| `hook` | 0-15% | Hook visual + caption + narrator intro. Dyad presentation si aplica. |
| `setup_post_hook` | 15-25% | Establishing setting + stakes + Slot B/C/D context. |
| `decision_setup` | varía | Approach al dilema (Slot E setup). |
| `decision_countdown` | ~2-3s antes de cada decision | Countdown 3-2-1 + A/B buttons + loading bar. |
| `consequence_A` | post-countdown | Consecuencia rama A elegida (Slot E action + body horror). |
| `rama_B_transition` | post-consequence_A | Bridge narrativo "Si elegiste B..." + caption transition. |
| `consequence_B` | post-bridge | Consecuencia rama B (counterfactual mid-video). |
| `cliffhanger` | 88-100% | Slot G archetype (Paz perdida domina 7/8). Counterfactual cozy. |

---

## Validación de output (script self-check)

Antes de declarar un ref-XX.md draft "listo para STOP point", el script verifica:

```
☐ Header con source_video + pattern + duration_total + total_scenes ✓
☐ Cada scene tiene los 9 campos obligatorios ✓
☐ Sum de duration per scene ≈ duration_total (±5%) ✓
☐ Narration text LITERAL de transcription.json (no parafrasis) ✓
☐ Pattern category usa enum válido ✓
☐ Items que script no pudo determinar → marcados [NEEDS VALIDATION] ✓
```

Si CUALQUIER check falla → script aborta con error específico, NO genera output incompleto silenciosamente.

---

## Última actualización

2026-05-16. Creado en Bloque I. Schema fijado post sprint combinado v6 — alineado con SPEC v6 `narrative_function` enum + `scene_context` structure.
