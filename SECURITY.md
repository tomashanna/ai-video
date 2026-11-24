# Seguridad

## Reportar una vulnerabilidad

No abras un issue público. Usá **GitHub → Security → Report a vulnerability** (private vulnerability
reporting) en este repositorio. Incluí pasos para reproducir, impacto y versión/commit afectado.
Respuesta inicial esperada: dentro de 7 días.

## Política de secretos

- Las API keys (`GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `REPLICATE_API_TOKEN`) se leen **solo** de variables
  de entorno o de un `.env` local (git-ignored). `.env.example` contiene únicamente nombres, nunca valores.
- En código, las keys viven como `SecretStr`; los logs pasan por un filtro que enmascara valores
  configurados y formatos de key conocidos. `ai-video doctor` informa si una key está configurada sin
  mostrarla.
- `gitleaks` corre en pre-commit y en CI (`gitleaks git` + `gitleaks dir`). Un hallazgo bloquea el merge.
- Si una key se expuso (commit, log, captura): **rotala primero** en el proveedor y después limpiá el
  historial. Borrar el archivo no alcanza.

## Gasto y abuso de APIs

Toda llamada paga pasa por `BudgetGuard` (tope `AIVIDEO_BUDGET_USD`, ledger append-only), con timeouts,
reintentos acotados y esperas con deadline. Usá `--dry-run` / `AIVIDEO_DRY_RUN=1` para validar sin gastar.

## Superficie de entrada

Los specs YAML se cargan con `yaml.safe_load` y un límite de tamaño; los subprocess usan listas de
argumentos (nunca `shell=True`) con timeout; las descargas de outputs de modelos exigen `https`.
