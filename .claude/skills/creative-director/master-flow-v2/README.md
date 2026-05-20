# Master Flow v2 — DRAFT (work in progress)

> ⚠️ **STATUS: DRAFT iterativo**. NO es autoridad canónica todavía.
> Vive aislado en `master-flow-v2/` para NO interrumpir el flujo actual (HANDOFF-PROTOCOL.md + AUDITOR-PROTOCOL.md siguen siendo working docs).
>
> **Propósito**: codificar el patrón 3-terminal (architect ↔ engineer ↔ auditor) que descubrimos experimentalmente con matadero-banquete. Replicable + automation-ready.
>
> **Approach**: cada rol owns su parte authoritative. Se mergea cuando los 3 estén completos + validados con 2+ proyectos.

---

## Estructura por nivel de abstracción (post-Phase 0 refinement)

```
master-flow-v2/
├── README.md                       ← este archivo (entry + status + niveles)
│
├── TEAM-PROTOCOL.md                ← ✅ NIVEL 1 universal multi-agent (any project, not just video)
│
├── AUDITOR-MASTER-FLOW.md          ← ✅ NIVEL 1+2 auditor role detail
├── ARCHITECT-MASTER-FLOW.md        ← TODO architect role detail
├── ENGINEER-MASTER-FLOW.md         ← TODO engineer role detail
│
├── per-CP/                          ← NIVEL 2+3 video production specifics (will refactor to NIVEL 2 templates + NIVEL 3 specifics in Phase 1)
│   ├── CP1-anchors-flow.md         ← ✅ v1
│   ├── CP2-script-flow.md          ← ✅ v1
│   ├── CP3-shots-flow.md           ← ✅ v2 (post Path B-extension)
│   ├── CP4-animation-flow.md       ← TODO post-CP4 matadero
│   └── CP5-render-flow.md          ← TODO post-CP5 matadero
│
└── shared/                          ← TODO Phase 1
    ├── HANDOFF-TEMPLATES.md
    ├── VERDICT-FORMAT.md
    ├── SPEC-ANNOTATION-PATTERNS.md
    ├── SUB-PATTERNS.md
    └── COST-TIME-TRACKING.md
```

## Los 4 niveles del sistema (mental model)

```
NIVEL 1 — MULTI-AGENT UNIVERSAL (no domain-specific)
└── TEAM-PROTOCOL.md ✅

NIVEL 2 — DOMAIN-UNIVERSAL (video production universal)
├── pipeline 5-CP genérico
├── tools reusable (image.py, tts.py, sfx.py, etc.)
├── canonical Q-gates (LUFS, Gemini ≥9.7, audit-against-referent ≥85%)
└── TEMPLATES vacíos (Phase 1): PAUTA-MASTER-TEMPLATE + INGENIERO-PAUTA-TEMPLATE

NIVEL 3 — FORMAT-SPECIFIC (horror-choice, tutorial, B2B, etc.)
├── PAUTA-MASTER (creative)
├── INGENIERO-PAUTA (technical)
└── canonical-scenes (N referentes virales)

NIVEL 4 — PER-INSTANCE
└── creative-specs/<id>.yaml + <proyecto>/
```

---

## Estado actual (2026-05-18 post Phase 0)

| File | Nivel | Status | Owner | Notas |
|------|-------|--------|-------|-------|
| `TEAM-PROTOCOL.md` | 1 | ✅ **v1** | 🔍 Auditor (provisional) | Multi-agent universal — Phase 0 closure |
| `AUDITOR-MASTER-FLOW.md` | 1+2 | ✅ v2 | 🔍 Auditor | Post-CP3 con Path B-extension |
| `ARCHITECT-MASTER-FLOW.md` | 1+2 | ⏸ pending | 🏛️ Architect | Handoff package ready |
| `ENGINEER-MASTER-FLOW.md` | 1+2 | ⏸ pending | 🛠️ Engineer | Partir de HANDOFF-PROTOCOL.md existing |
| `per-CP/CP1-anchors-flow.md` | 2+3 video | ✅ v1 | 🔍 Auditor | Refactor Phase 1 a NIVEL 2 template + NIVEL 3 specifics |
| `per-CP/CP2-script-flow.md` | 2+3 video | ✅ v1 | 🔍 Auditor | Idem |
| `per-CP/CP3-shots-flow.md` | 2+3 video | ✅ v2 | 🔍 Auditor | Idem — incluye Path B-extension |
| `per-CP/CP4-animation-flow.md` | 2+3 video | ✅ **v1 in-flight** | 🔍 Auditor | matadero CP4 active. Captures baseline test + dry-run gate + CP5 trim mandate + setpts ±20% workaround patterns. Update post-closure |
| `per-CP/CP5-render-flow.md` | 2+3 video | ⏸ pending | co-write | Post-CP5 matadero |
| `shared/*` | 2 templates | ⏸ Phase 1 | co-write | Después de CP4-CP5 matadero |
| `00-OVERVIEW.md` | meta | ⏸ Phase 4 | architect+auditor merge | Promover a canónico Phase 4 |

---

## Reglas de iteración

1. **Cada CP que pasamos en producción real → update incremental** del per-CP doc relevant
2. **Lo que aprendemos** (lessons learned, antipatterns, fixes sistémicos) → captura en el doc del rol que lo identificó
3. **NO se promueve a canónico** hasta validar con ≥2 proyectos completos end-to-end
4. **Cross-link entre docs**: usar `[[name]]` style + path relativos para links internos
5. **Si conflicto entre draft y working doc actual** → working doc gana hasta que draft promueva a canónico

---

## Roadmap

| Phase | Cuándo | Qué |
|-------|--------|-----|
| **Phase 0** ✅ CLOSED 2026-05-18 | Pre-CP4 matadero | TEAM-PROTOCOL NIVEL 1 + AUDITOR-MASTER-FLOW v2 + per-CP CP1-CP3 retroactive |
| **Phase 1** | Post-CP5 matadero closure | Refactor NIVEL 2 templates (PAUTA + INGENIERO-PAUTA) + `measure-canonical-referents.py` + per-CP CP4/CP5 closure docs + refactor CLAUDE.md (separar NIVEL 1 vs NIVEL 2). ⭐ **PRIORITY BUMP 2026-05-18**: `measure-canonical-per-speaker.py` (diarization pyannote-audio + per-speaker WPM + pitch + energy bands) DEBE arrancar ANTES de 2do video (no post-CP5). Per CLAUDE.md hard rule #19 expansion "MEASURE → MATCH → VALIDATE → USE" workflow. Sin per-speaker measurement no podemos validate voice IDs canonical. Plus audit cross-library defaults (sfx-catalog, scripts defaults, elements.json). |
| **Phase 2** | 2do video horror-choice end-to-end | Validation NIVEL 1+2+3 con segundo video horror-choice + architect crea ARCHITECT-MASTER-FLOW + engineer ENGINEER-MASTER-FLOW |
| **Phase 3** | 1er video FORMATO DISTINTO | Test speed-up con templates Phase 1: ¿2-3 hrs arrancar formato nuevo? |
| **Phase 4** | Post formato distinto | Promote a canónico, deprecate working docs viejos, JSON schemas formal |
| **Phase 5** | Phase 4 closed + criteria explícitos | 1-terminal orchestrator pilot — automation end-to-end |

---

## Quick links

- Working canon actual: `creative-director/HANDOFF-PROTOCOL.md` + `creative-director/AUDITOR-PROTOCOL.md`
- Pauta empírica del formato: `horror-choice-format/PAUTA-MASTER.md` + `INGENIERO-PAUTA-MASTER.md`
- Sistema architecture (3-terminal): `CLAUDE.md` § 0.0

---

**Generado**: 2026-05-18 (mid-CP3 matadero-banquete)
**Próximo update esperado**: tras CP3 closure (variants strategy + shot_20 path B/C resolution)

---

## Quick-read order para validar

Si vos / architect / engineer quieren validar lo escrito hasta acá, leer en este orden:

1. `README.md` (este) — 5 min
2. `AUDITOR-MASTER-FLOW.md` — 15 min (mi parte authoritative)
3. `per-CP/CP1-anchors-flow.md` — 10 min (retroactive matadero)
4. `per-CP/CP2-script-flow.md` — 10 min (retroactive matadero)
5. `per-CP/CP3-shots-flow.md` — 10 min (in-flight matadero, parcial)

Total: ~50 min validar todo el draft Phase 0.

**Items que pido validar específicamente al architect**:
- ¿Sub-patterns observados son correctos? (test-first, Path A/B/C, spirit-not-literal, procedural violations)
- ¿Lessons learned codified son derivables del experience matadero?
- ¿Architect domain decisions están bien atribuidas vs auditor/engineer domain?
- ¿Algún anti-pattern mío en mi propio doc auditor que no detecté?

**Items que pido validar específicamente al engineer**:
- ¿Engineer-domain decisions están bien atribuidas?
- ¿Self-audit criteria que documenté están alineadas con HANDOFF-PROTOCOL.md template?
- ¿Hay sub-patterns engineer que faltan en mi audit?
