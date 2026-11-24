# AGENTS.md — guía para asistentes de IA

Sistema para producir videos cortos verticales con IA, guiado por un **creative spec** (YAML v11).
Código en `src/ai_video/` (CLI `ai-video`), prompts/roles en `.claude/skills/`, manual completo en
`docs/OPERATING-MANUAL.md` (hard rules, gates por checkpoint, triggers). Leelo antes de producir un video.

## Comandos

```bash
uv sync --extra providers              # deps (+ --extra media para Whisper/OpenCV)
uv run ai-video list | doctor | budget # tools · entorno · gasto
uv run ai-video validate-spec <spec>   # schema v11
uv run ai-video <tool> --help          # cualquier gate/builder/provider
uv run pytest -q                       # tests (APIs mockeadas)
uv run python -m evals.run             # evals offline
uv run ruff check . && uv run ruff format --check . && uv run mypy
bash scripts/health-check.sh           # higiene del repo
```

## Roles (nunca mezclar en una misma sesión)

| Pedido | Rol / skill |
|---|---|
| Diseñar historia, concepto, guion | 🏛️ arquitecto — `creative-director` → `creative-specs/<id>.yaml` |
| Producir / renderizar un spec | 🛠️ ingeniero — `video-director` + `ai-video-production` (+ skill del formato) |
| Auditar un checkpoint / handoff | 🔍 auditor — `creative-director/AUDITOR-PROTOCOL.md` (fuentes primarias, sin contexto del arquitecto) |
| Editar footage ya grabado | 🎬 editor — `video-editor` |
| Formato choice (dilema A/B, countdown) | + `choice-format-core` + `horror-choice-format` o `sport-choice-format` |
| HyperFrames (lint/render/preview) | + `hyperframes` / `hyperframes-cli` (vendorizadas) |

## Reglas no negociables

- **Plan primero:** antes de llamar APIs pagas (ElevenLabs, Gemini, Replicate), modificar assets o
  renderizar: presentar plan y esperar confirmación. Probar con `--dry-run`; respetar `AIVIDEO_BUDGET_USD`.
- **Gates antes de declarar listo:** los 8 gates pre-render de `docs/OPERATING-MANUAL.md` deben salir con
  exit 0; después, checklist humano. Hard rules completas: `docs/OPERATING-MANUAL.md` § Hard rules
  (resumen parseado por `qa-gate`) y `docs/HARD-RULES.md` (detalle).
- **Medir, no estimar:** los umbrales empíricos salen de `data/referent-analysis/` vía
  `ai_video.core.empirical_bands`; nunca hardcodear números que ya tienen banda medida.
- **Nada local al repo:** proyectos en `projects/<id>/` y specs de trabajo en `creative-specs/` están
  git-ignored; no commitear media, `.env`, handoffs por checkpoint ni renders.
- **Privacidad:** no agregar handles reales de creadores (usar `@referent-x`), nombres de clientes,
  rutas absolutas ni material de terceros (audio, frames, transcripciones).

## Al tocar código

- Tool nuevo = módulo con `main() -> int` + entrada en `ai_video/cli.py:TOOLS` + test en `tests/unit/`
  (HR#26). Gates: exit `0` pass · `1` fail · `2` no medible.
- Rutas con `ai_video.paths`; config con `ai_video.config.get_settings()`; subprocess con lista de
  argumentos y `timeout`; llamadas pagas con `providers/clients.py` + `BudgetGuard.charge` + `retry_call`.
- Commits pequeños con Conventional Commits; no reescribir historia publicada.
