# creative-direction/ — Docs operacionales del formato sport-choice

> ⛔ **ARQUITECTURA.** La AUTORIDAD CREATIVA del formato sport-choice vive en **`sport-choice-format/PAUTA-MASTER.md`**. La AUTORIDAD TÉCNICA en **`sport-choice-format/INGENIERO-PAUTA-MASTER.md`**. Los docs en ESTE folder son **operacionales secundarios** — el "cómo IMPLEMENTAR" lo que las pautas dictan. NO son autoridad.
>
> Si encontrás conflicto entre estos docs y las pautas (sport o las heredadas de horror) → **gana la pauta siempre**.

---

## ⚠️ QUÉ SE HEREDA (NO duplicado acá)

> ⛔ **Firewall de capas (`NO-HORROR-GUARD.md`):** sport-choice hereda SOLO de 3 capas — `choice-format-core` (Capa A.5, mecánica choice) + `sport-choice-format` (Capa B, sabor sport) + `ai-video-production` (Capa A, técnica universal). **NUNCA hereda operacionales de `horror-choice-format/`** (ahí viven el preset CSS lúgubre, el voice_id grave de horror, los SFX de terror, las LUTs `cool_horror`). Si algo no aparece en esas 3 capas → flaggear + escalar al arquitecto, NO ir a buscarlo a horror.

sport-choice **hereda el pipeline universal de `ai-video-production` + la mecánica agnóstica de `choice-format-core`**, salvo lo aquí especificado. En concreto:

- **MECÁNICA del formato choice** (estructura temporal, hook dyad, countdown, decisiones binarias, framing condicional, counterfactual, POV, lenguaje) → `../../choice-format-core/CHOICE-MECHANIC.md` (Capa A.5 agnóstica, derivada de los 8 virales vía horror) + su técnica choice-UI → `../../choice-format-core/INGENIERO-CHOICE-CORE.md`.
- **Pipeline técnico** (TTS, image, SFX, motion, captions, render, QA, HYBRID per-clip atomic, MODEL-CAPABILITIES, 8 gates) → `ai-video-production/`.
- **`canonical-scenes/`** → sport-choice AÚN no tiene canonical-scenes propios. La autoridad ESTRUCTURAL agnóstica (esqueleto, invariante, placement del counterfactual, framing acción-condicional, dyad, escalada de decisiones, outro) vive en `../../choice-format-core/CHOICE-MECHANIC.md` (ya extraída género-neutro de los 8 virales). Los canonical-scenes propios de sport se derivarán empíricamente de nuestros primeros videos. ⚠️ NO leer assets/contenido de `horror-choice-format/` para producir sport (firewall arriba) — la estructura ya está en core.
- **`templates/scripts/`** + **`effects-library/`** → se heredan de `ai-video-production/templates/` (los presets de VOZ de horror NO se usan — narrador deportivo limpio).
- **CREATIVE-SPEC schema (v11)** → `creative-director/templates/`.

Los docs de ESTE folder cubren SOLO la capa sport-específica.

---

## ⛔ LEER PRIMERO (orden estricto)

Antes de tocar nada de este folder, leer EN ORDEN:

1. **`../PAUTA-MASTER.md`** (sport) — la LÓGICA deportiva (elección=equipo, ramas asimétricas, decisiones=jugadas, consecuencias=gol/burla, cadena de lógica, anti-patterns)
2. **`../INGENIERO-PAUTA-MASTER.md`** (sport) — REGLA DE AMBIENTE + paleta SFX fútbol + consistencia de kits
3. **`../../choice-format-core/CHOICE-MECHANIC.md`** — la MECÁNICA AGNÓSTICA del formato choice (esqueleto + invariante + decisión→consecuencia + framing + counterfactual — heredada, común a horror y sport)
4. **`../../choice-format-core/INGENIERO-CHOICE-CORE.md`** — la técnica choice-UI heredada (decision-UI pacing, UI safe zones, captions chunking, lip sync, 0 cuts en hook). ⤴ Para la técnica UNIVERSAL (pace, LUFS, mix, HYBRID, MODEL-CAPABILITIES) apunta a `ai-video-production/`.
5. **`../SCRIPT-WRITING-GUIDE.md`** (sport)
6. **`../video-log.md`** (rotación obligatoria)
7. **`../../creative-director/templates/`** (schema CREATIVE-SPEC v11 para el SPEC output)

---

## Docs operacionales en este folder

| Doc | Función operacional | Pauta relacionada |
|-----|---------------------|-------------------|
| `script-writing.md` | La lógica narrativa sport (cómo se estructura el guion deportivo, slot a slot) | PAUTA-MASTER (sport) §§ 1-8 + SCRIPT-WRITING-GUIDE |
| `image-direction.md` | ⭐ La **REGLA DE AMBIENTE** (orden visual del partido) + per-shot framework + anchors de kit/likeness | INGENIERO-PAUTA (sport) § 1 REGLA DE AMBIENTE + § 3 consistencia |
| `audio-direction.md` | Paleta SFX fútbol + ambient de estadio + música de tensión deportiva + ducking | INGENIERO-PAUTA (sport) § 2 SFX + § 4 música |
| `ui-elements.md` | Name labels de EQUIPOS, countdown, botones A/B de jugadas, watermark | UI heredado (`choice-format-core/INGENIERO-CHOICE-CORE.md § 2` UI safe zones) reskineado a deporte |

(Para `camera-and-shots`, `captions`, `aesthetic`, `animation-direction`, `shared-universe`: la MECÁNICA agnóstica vive en `../../choice-format-core/` (CHOICE-MECHANIC + INGENIERO-CHOICE-CORE) + la técnica universal en `ai-video-production/`. Solo cambia el CONTENIDO, que está cubierto por los 4 docs de arriba + las pautas sport. No se duplican — y NO se leen de `horror-choice-format/` (firewall de capas arriba).)

---

## Workflow del arquitecto sport-choice

```
1. Leer pautas (sport + mecánica heredada de `choice-format-core`) en orden estricto
2. Consultar video-log.md → rotación (liga/equipos + jugada-clave + posición POV + pattern)
3. ENTREVISTAR user (partido/equipos/jugadores objetivo, topical o ficticio)
4. Diseñar (timeline beat-a-beat → PAUTA-MASTER § 10.A):
   - La elección = equipo (con contexto explícito) + los DOS recorridos completos asimétricos por favorito (jugado + foil tagueado `counterfactual_*`, orden libre, secuenciales, foil fuera del played path)
   - Las compuertas (2-3 por recorrido según favorito; tipos distintos, escalada de zona, duda real — catálogo por posición POV § 10.B) + sus consecuencias (gol/burla, catálogo § 6)
   - El pivote marcado entre recorridos + el cliffhanger/CTA
5. Correr la PLANTILLA DE CADENA CAUSAL (PAUTA-MASTER § 10.C) eslabón por eslabón sobre AMBOS recorridos + los anti-patterns (§ 10)
6. Aplicar la REGLA DE AMBIENTE a cada shot (image-direction.md)
7. Llenar audio-direction (paleta SFX fútbol) + ui-elements (name labels equipos)
8. Self-validation pre-emit (HR#27): correr los validators estructurales (`audit-spec-structure-vs-canonical.py` + `audit-spec-narrative-coherence.py`) + `NO-HORROR-GUARD.md` contra el propio SPEC; iterar hasta 0 findings 🔴
9. Codificar en CREATIVE-SPEC v11.yaml (schema heredado) + references_canonical[] (citadas por valor ESTRUCTURAL)
10. HANDOFF al ingeniero
```

---

## Anti-patterns del arquitecto sport-choice

❌ **Olvidar el contexto explícito de equipo en el hook** → incoherencia rival/compañero (el bug que el formato existe para resolver).

❌ **Recorridos interleaved, un recorrido que spoilea el otro, o el foil dentro del played path** (los rivales del played path = `rival_npc` genérico, NO el anchor del foil) → el bug del topical champions.

❌ **Tratar la estructura como un "counterfactual opening fijo / rama corta"** — son DOS recorridos completos, orden libre (§ PAUTA-MASTER § 4 + § 10.A).

❌ **Tratar la lógica deportiva como empíricamente validada** — es diseño pre-empírico en validación. No inventar "compliance N/8" que no existe.

❌ **Meter cualquier elemento de horror** (muerte, monstruos, body horror, drones de terror, gritos).

❌ **Violar un anti-pattern de PAUTA-MASTER § 10** (balón al rival, orden desalineado, consecuencia no causal, contradicción física, B siempre correcta, decisión sin duda).

❌ **Prompts de imagen que no ubican la geografía del partido** (saltar la REGLA DE AMBIENTE → frames confusos).

❌ **Poner el nombre de la celebridad literal en el prompt** → describir por rasgos foto-reales + kit (descriptor-based).
