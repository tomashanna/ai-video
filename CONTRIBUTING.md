# Contribuir

## Setup

```bash
uv sync --all-extras          # o --extra providers si no necesitás Whisper/OpenCV
pre-commit install            # ruff, gitleaks, guard >5 MB, EOF/whitespace
cp .env.example .env          # solo si vas a llamar APIs reales
```

`ffmpeg`/`ffprobe` son necesarios para los tests marcados `ffmpeg` y la suite `render` de evals
(se saltean automáticamente si no están).

## Antes de abrir un PR

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy
uv run pytest
uv run python -m evals.run
bash scripts/health-check.sh
```

## Convenciones

- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `refactor:`,
  `docs:`, `test:`, `ci:`, `chore:`), uno por cambio coherente. Nunca `--amend` / `push --force` sobre
  commits ya publicados.
- **Idioma:** docs en español; código, identificadores y mensajes de commit en inglés.
- **Sin rutas absolutas:** todo path se resuelve con `ai_video.paths` (repo-relativo o por env).
- **Sin secretos:** nada de keys en código, fixtures ni docs. Las keys se leen solo vía `ai_video.config`.
- **Sin media pesada:** el repo trackea el sistema, no producciones. `.mp4/.wav/.mp3` están ignorados
  salvo en `assets/` (whitelist) y el pre-commit rechaza archivos > 5 MB. Proyectos en `projects/`
  y specs de trabajo en `creative-specs/` son locales.

## Agregar un tool / gate

1. Módulo en `src/ai_video/<grupo>/<nombre>.py` con `main() -> int` (argparse) y lógica pura testeable
   separada del I/O. Exit codes de gates: `0` pass · `1` fail · `2` no se pudo medir.
2. Registrarlo en `TOOLS` de `src/ai_video/cli.py` (nombre con guiones).
3. Test en `tests/unit/test_<nombre>.py` (HR#26): casos adversariales; APIs siempre mockeadas.
4. Si es un gate de SPEC, sumar un caso en `evals/cases.yaml` que inyecte el defecto que detecta.
5. Llamadas pagas: usar `ai_video.providers.clients` + `budget.BudgetGuard.charge(...)` + `retry_call`,
   y soportar `--dry-run`.
6. Documentarlo en el skill que corresponda (y en `docs/OPERATING-MANUAL.md` si es un gate obligatorio).

## Skills vendorizadas

`.agents/skills/` viene de heygen-com/hyperframes (Apache-2.0). No editar en el lugar: actualizar desde
upstream y refrescar `skills-lock.json`.
