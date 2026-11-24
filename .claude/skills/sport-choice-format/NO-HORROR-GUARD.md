# NO-HORROR-GUARD.md — Firewall de GÉNERO sport-choice (cero-horror / fútbol-real)

> **Qué es:** el checklist que el 🛠️ INGENIERO y el 🔍 AUDITOR corren para garantizar que un video sport-choice salga **fútbol REAL** y **NO horror disfrazado**. Cada ítem = un **pass/fail** verificable.
>
> **Por qué existe:** sport-choice y horror-choice son HERMANOS que heredan la misma MECÁNICA agnóstica de `../choice-format-core/`. Pero comparten tanto que es trivial que el sabor de horror **se filtre** (preset CSS lúgubre, SFX de drones/gritos, narrador grave omnisciente, LUT `cool_horror`, body-horror). Este guard es el firewall que detecta esa fuga.
>
> **Autoridad de la que deriva:**
> - `PAUTA-MASTER.md` **§0 BAN** — *"Cualquier elemento de horror (muerte, body horror, monstruos, drones de terror, gritos de horror) — sport-choice es drama deportivo, no terror."*
> - `INGENIERO-PAUTA-MASTER.md` **§2 (paleta SFX fútbol + regla absoluta)**, **§4 (LUTs sport / música deportiva)**, **§1 (REGLA DE AMBIENTE)**.
> - `choice-format-core/CHOICE-MECHANIC.md` (la mecánica es compartida; el SABOR manda el género, §0).
>
> **Cuándo se corre:** **per-CP** (cada handoff `CP[N]-handoff.md`) **+ pre-render** (antes del stop point). Es complementario a los 8 gates universales y al dual quality bar — no los reemplaza.

---

## ⛔ Regla del firewall-por-capa (la causa raíz #1 de fuga)

> El ingeniero de un video sport-choice **HEREDA SOLO de estas 3 capas**:
>
> 1. `choice-format-core/` (Capa A.5 — mecánica choice agnóstica)
> 2. `sport-choice-format/` (Capa B — sabor deportivo: SFX fútbol, LUTs sport, narrador deportivo, paleta cálida)
> 3. `ai-video-production/` (Capa A — técnica universal: CAPTIONS, MOTION-LAYER CSS, AUDIO-MASTERING, PIPELINE, SFX-PIPELINE mecánica)
>
> ⛔ **NUNCA hereda de `horror-choice-format/`.** Ahí viven el preset CSS lúgubre (`VISUAL-STYLE.md`), el voice_id del narrador grave de horror, los presets de voz de horror (`assets/voice-effects/`), la paleta SFX de terror (drones/susurros/gritos) y las LUTs `cool_horror`. Si el ingeniero leyó/copió cualquier cosa de `horror-choice-format/` para producir un sport-choice → **fuga de género garantizada**.

Si una decisión técnica no aparece ni en core, ni en sport, ni en universal → **FLAGGEAR + escalar al arquitecto**, NO ir a buscarla a horror.

---

## El checklist (8 ítems — cada uno PASS/FAIL)

> Marcá cada uno `✅ PASS` / `❌ FAIL`. **Cualquier ❌ = NO-GO** hasta corregir. El auditor cita la autoridad en la columna correspondiente.

| # | Ítem | PASS si… | FAIL (= horror-leak) si… | Autoridad |
|---|------|----------|--------------------------|-----------|
| **G1** | **Preset CSS** | El preset de `.scene-image` (en `index.html` / `VISUAL-STYLE.md` deportes) es **cálido/saturado/brillante/broadcast** (saturate ≥1.0, brightness ≥0.95). | Usa el preset lúgubre de horror `filter: contrast(1.28) saturate(0.35) brightness(0.74)` (o cualquier `saturate(<0.6)` / `brightness(<0.85)`). | horror `BRAND.md §4` (preset lúgubre = OPUESTO) + sport PAUTA §14 deliverable `VISUAL-STYLE.md` deportes |
| **G2** | **SFX = paleta fútbol** | Todos los SFX son deportivos: **rugido de hinchada, silbato, golpe al balón, red, atajada, abucheos, confeti, cánticos de ultras, tick de countdown**. | Aparece **CUALQUIER** SFX de terror: **drone de terror, susurro, grito (scream), sub-bass de jumpscare, death-scream, whisper uncanny, heartbeat de tensión-horror, drone uncanny**. | `INGENIERO-PAUTA §2` (catálogo SFX + "Regla absoluta": ⛔ NUNCA gritos de horror, drones de terror, sub-bass de jumpscare, susurros uncanny) |
| **G3** | **Narrador = relator play-by-play** | El narrador es **relator deportivo play-by-play vivo** (mete al viewer en la jugada, neutral de juicio, español neutral). Canónico sport: **El Faraón** `QpDQJR3frbDwOhTIo8nW` (voices-catalog). El `voice_id` NO es el del narrador grave de horror. | El `narrator_voice` / `voice_id` = `Tj9l48J9AJbry5yCP5eW` (voice de horror whisper-grave, DEPRECATED) **o** el tono declarado es "grave omnisciente / susurro / frío de cripta / tenebroso". | sport PAUTA §8 (relator play-by-play, narra-no-juzga) + horror (voz grave omnisciente = horror) |
| **G4** | **Música = sports-thriller / celebración** | Layers de música = **drone subharmónico de tensión DEPORTIVA (sports-thriller bed) → celebración triunfal cálida → rising strings en clímax**. Los prompts de ElevenLabs cierran con "no horror" o equivalente. | Algún layer de música = **dark ambient drone (de terror), horror drone, eerie pad, dread ambience**. | `INGENIERO-PAUTA §4` (mood reskineado: tensión deportiva → triunfo; tabla música) |
| **G5** | **CERO body-horror / muerte / monstruos / uncanny** | La consecuencia de un error = **humillación deportiva** (papelón, abucheos, memes, gol rival, error injusto). Ningún personaje muere, se mutila, se transforma, ni aparece criatura. | Aparece en `visual_intent` / `narration` / `description`: **muerte, sangre, cadáver, body-horror, mutilación, monstruo, criatura, demonio, ente, jumpscare, posesión, lo uncanny/perturbador, daño físico al protagonista**. | sport PAUTA §0 BAN + §6 (catálogo de fracaso = deportivo, NO daño físico) |
| **G6** | **LUTs sport** | `visual_style_lut` ∈ {`warm_glory`, `cool_cinematic_stadium`, `cool_defeat`} (con sufijos de versión `_v1` / `_freeze_filter` permitidos). | Algún `visual_style_lut` contiene `horror` (`cool_horror`, `horror_deep`, etc.) o es un grade de terror. | `INGENIERO-PAUTA §4` (LUTs sport — "Sin `cool_horror` ni ninguna LUT de terror") |
| **G7** | **Geografía de estadio clara (REGLA DE AMBIENTE)** | Cada `visual_intent` ubica POV → zona → geografía (arco/red, kit propio, kit rival, arquero, balón, líneas) → estadio (lleno/reflectores/césped) → acción. La acción va AL FINAL. | El shot no establece estadio/cancha (geografía ambigua, sin arco/kits/balón), o la escena no transcurre en un estadio de fútbol. | `INGENIERO-PAUTA §1` (REGLA DE AMBIENTE — la regla técnica central) |
| **G8** | **Herencia de capas correcta** | El handoff del ingeniero declara herencia SOLO de `choice-format-core` + `sport-choice-format` + `ai-video-production`. | El handoff (o cualquier asset/prompt/voz/preset) fue tomado de `horror-choice-format/`. | Esta doc § "Regla del firewall-por-capa" + sport PAUTA §13 (lo que se hereda) |

---

## Cómo lo usa cada rol

### 🛠️ INGENIERO (per-CP, antes de declarar el handoff)
- En **CP1** (anchors): verificar G5 (kits/jugadores, NO criaturas) + G7 (geografía estadio) + G8 (no copió anchors de horror).
- En **CP2** (script): verificar G3 (narrador deportivo) + G5 (narración sin muerte/body-horror) + G7 (visual_intent con REGLA DE AMBIENTE).
- En **CP3** (shot images): G1 (preset CSS) + G6 (LUTs) + G7.
- En **CP4** (audio): G2 (SFX fútbol) + G4 (música deportiva) + G3 (voz).
- En **CP5** (render): re-correr **TODOS** los ítems pre-render.
- Registrar el resultado del checklist en `CP[N]-handoff.md`.

### 🔍 AUDITOR (independiente, per-CP + final)
- Correr este checklist **sin compartir terminal** con arq/ing (AUDITOR-PROTOCOL).
- Para cada ítem: leer la **fuente primaria** (la celda "Autoridad") + el handoff + el SPEC/render, y emitir `✅/❌` con evidencia (cita textual del SPEC o del frame).
- **1 frame = existence only NO alcanza** para G7 (igual que HR#30 para captions): verificar la geografía a lo largo de TODO el video, no un único frame.
- Verdict: **GO** (8/8 ✅) / **NO-GO** (cualquier ❌) / **ESCALAR** (ambigüedad arquitectural real).

### Acelerador (BONUS) — scanner de SPEC
Para los ítems que viven en el SPEC (G2 SFX, G3 voz, G4 música, G5 narración/visual, G6 LUT), correr:

```bash
uv run ai-video audit-spec-genre-fidelity \
  --format sport-choice --spec ../../creative-specs/<id>.yaml
# Exit 0 → sin horror-leak en el SPEC (G2-G6 limpios) → seguir con la verificación humana de G1/G7/G8
# Exit 1 → horror-leak detectado → el reporte JSON lista los hits (campo + término + ítem) → corregir
# Exit 2 → error (SPEC no encontrado / sin video_capabilities)
```

> ⚠️ El scanner es un **detector de fuga textual** (términos de horror, LUT de horror, SFX de horror, voice_id de horror). **NO sustituye** la verificación humana de:
> - **G1 (preset CSS)** → vive en `index.html` / `VISUAL-STYLE.md` deportes, no en el SPEC.
> - **G7 (geografía de estadio)** → requiere mirar los frames (Gemini Vision en Gate 4).
> - **G8 (herencia de capas)** → requiere leer el handoff/proceso del ingeniero.
>
> El scanner v0 cubre a nivel SPEC: **G2** (SFX), **G4** (música), **G5** (narración/visual), **G6** (LUT) + el **voice_id deprecado** de G3.
> ⚠️ **Gaps conocidos del scanner v0 (el HUMANO los cubre vía checklist):**
> - **G3 tono-de-texto** — un campo tipo `narrator_tone: "grave omnisciente, tenebroso, susurro"` NO lo caza el v0 (solo caza el voice_id deprecado). El auditor lee la declaración de tono a mano.
> - **G1 (preset CSS)** vive en `index.html`/BRAND, **G7 (geografía)** requiere mirar frames (Gemini Gate 4), **G8 (herencia)** requiere leer el handoff.
> - Términos del catálogo aún fuera del léxico: `transforma`, `retorcido`, `ominous`, `sinister`, `shriek`.
> **Forward v0.1** (machine-enforcement upgrade): sumar al scanner el scan de campos de tono-de-narrador + esos términos + colectar TODOS los hits por campo (hoy corta al primero). Hasta entonces: **el scanner acelera, el checklist humano es el firewall completo.**

---

## Catálogo de términos de horror-leak (referencia para el scanner + el ojo humano)

> Si alguno aparece en `narration` / `visual_intent` / `description` / SFX / música / LUT / voz de un sport-choice → **horror-leak**.

- **Muerte / daño físico:** muerte, mueres, morir, cadáver, cuerpo (en sentido macabro), sangre, herida, mutilación, descuartiza, agoniza.
- **Monstruos / sobrenatural:** monstruo, criatura, demonio, ente, fantasma, espectro, posesión, ritual, sacrificio.
- **Body-horror / uncanny:** body horror, deforme, retorcido, perturbador, uncanny, grotesco, antinatural, se transforma (en algo no-humano).
- **Atmósfera de terror:** terror, horror, pesadilla, pavor, escalofrío de miedo, jumpscare, susto, tinieblas malignas.
- **Audio de horror:** drone (de terror), drone uncanny, dark ambient drone, susurro/whisper (uncanny), grito/scream (de terror), death-scream, sub-bass de jumpscare, heartbeat de pavor, eerie pad, dread ambience.
- **LUT de horror:** `cool_horror`, `horror_deep`, `horror-deep`, cualquier grade etiquetado horror.
- **Voz de horror:** voice_id `Tj9l48J9AJbry5yCP5eW`; tono "grave omnisciente", "frío de cripta", "tenebroso", "whisper".

**NO son horror-leak (deportivos legítimos, aunque suenen tensos):** tensión (deportiva), rugido (de hinchada), abucheos, silbidos, drone subharmónico **de tensión deportiva** (sports-thriller bed), `cool_defeat` (frío del fracaso deportivo gris-azul, NO horror), gol rival, papelón, humillación deportiva, derrota, presión, clímax. El frío del fracaso (`cool_defeat`) es deportivo; el frío de terror (`cool_horror`) es leak.
- ⚠️ **"grave" — desambiguación (trap para G3):** narrador **grave DEPORTIVO** = relator play-by-play vivo = ✅ OK (lo dicen BRAND §3 + INGENIERO-PAUTA). narrador **grave OMNISCIENTE / tenebroso / frío de cripta / susurro** = ❌ leak (horror). Lo que distingue NO es la palabra "grave" — es **"deportivo / play-by-play / relata la jugada"** vs **"omnisciente / cripta / susurra"**.
- ⚠️ **G1 vs `cool_defeat` (scope):** G1 mide el **preset BASE** de `.scene-image` (cálido/saturado). El LUT `cool_defeat` (saturate 0.78 / brightness 0.92) es un **override scoped al beat de derrota**, gobernado por **G6** (LUTs sport), NO por G1 — no aplicar el umbral de G1 a un frame con `cool_defeat`.

---

## Estado

- **Versión:** v0 (pre-empírico). Pareado con `PAUTA-MASTER.md` v0 + `INGENIERO-PAUTA-MASTER.md` v0.1.
- **Forward:** cuando sport-choice tenga ≥3 videos shipped, sumar al scanner una verificación de **% de shots con geografía-de-estadio clara** (G7 medible) derivada empíricamente, y consolidar el catálogo de términos con los falsos positivos reales observados (loguear en `video-log.md`).
