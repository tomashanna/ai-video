# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/); versionado [SemVer](https://semver.org/lang/es/).

## [0.2.0] — 2026-11-24

Reestructuración para publicación open-source.

### Added
- Paquete `ai_video` (`src/`) con un único CLI `ai-video` que expone los ~57 tools (providers, build,
  audits, research, editor, spec) más `list`, `doctor` y `budget`.
- Configuración centralizada (`pydantic-settings`), `.env.example`, logging estructurado con redacción de
  secretos, reintentos con backoff, `BudgetGuard` con ledger de gasto y `--dry-run` en todos los providers.
- `validate-spec`: schema pydantic para creative specs v11 (tipos, rangos, referencias cruzadas, warnings
  de voces superpuestas y desvío de duración).
- Harness de evals offline (`evals/`): spec, captions, safe zones, rúbrica calibrada y render sintético.
- ~110 tests nuevos (infra, providers mockeados, spec, render-lock, captions, CLI); CI con lint,
  typecheck, tests, evals y gitleaks; pre-commit; Dependabot.
- README, CONTRIBUTING, SECURITY, AGENTS/CLAUDE, THIRD_PARTY_NOTICES; rúbrica de scoring sanitizada.

### Changed
- Layout: `assets/`, `templates/`, `docs/`, `examples/`, `data/`, `scripts/`, `tests/`; los gates ya no
  se copian a cada proyecto. Todas las referencias de skills/docs apuntan a la nueva estructura.

### Fixed
- Rutas `<repo-root>` literales que rompían `qa-gate`, `hard_rules_parser`, builders AVU y tools de research.
- `audit-gemini-calibrated` nunca calculaba el score ponderado (esperaba 8 dimensiones; v4 tiene 10).
- `render-lock` nunca bloqueaba (guardaba el pid del proceso efímero) y `release <proyecto>` fallaba.
- Veo: upload no usado, polling sin deadline, mime fijo; Kling: esperas sin límite, descargas sin https.
- Gate de unicidad narrativa fallaba abierto sin `sentence-transformers`.
- Sintaxis exclusiva de Python 3.12 en `audit-videolog-appended`; `/tmp` fijos compartidos entre corridas;
  67 llamadas a subprocess sin timeout; captions con texto sin escapar en JS; `make-ass` con redondeo de
  centésimas incorrecto y ejecución al importar; `audit-narrative --help`.

### Removed
- Media de auditions/A-B de voces (2.7 MB), thumbnails regenerables, docs archivados, freeze manifests,
  specs legacy/inválidos y con personas reales, docs de estrategia de marca personal, referencias a
  clientes y notas de configuración de máquina.
