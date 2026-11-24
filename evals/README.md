# Evals

Evaluaciones offline y deterministas del pipeline. No llaman a APIs pagas: los specs y los
timings de captions son fixtures sintéticos, los videos se generan con `ffmpeg -f lavfi`, y el
juez subjetivo (Gemini calibrado v4) se reemplaza por puntajes grabados.

```bash
uv run python -m evals.run                    # todas las suites
uv run python -m evals.run --suite spec       # spec | captions | safe_zone | rubric | render
uv run python -m evals.run --json evals/out/report.json
```

| Suite | Qué mide | Fuente de verdad |
|---|---|---|
| `spec` | Cada caso inyecta **un** defecto en `fixtures/base_spec.yaml` (voseo, cliché, nombre-oficio, handle ajeno, voces superpuestas, narración que no entra en el shot, schema inválido) y verifica que el gate real lo detecta — y que el baseline limpio pasa (sin falsos positivos). | Gates de `ai_video.audits` + `validate-spec` |
| `captions` | Timings tipo Whisper → agrupación real de `ai_video.providers.captions` → orden, solapamiento, duración mínima, legibilidad (chars/s) y **cobertura temporal** (HR#30-C). | `evals/checks.py` |
| `safe_zone` | Posición vertical de un caption ASS vs. la banda empírica medida en referentes. | `data/referent-analysis` |
| `rubric` | Puntaje ponderado calibrado v4 + lógica OR de HR#1 (calibrado ≥ umbral **o** perceptual humano ≥ umbral) sobre salidas de juez grabadas. | `audit_gemini_calibrated.WEIGHTS` + `docs/OPERATING-MANUAL.md` |
| `render` | Clips 9:16 sintéticos: duración, resolución, fps, loudness integrado (−14 LUFS ±1) y true peak; incluye variantes rotas que **deben** fallar. Se omite si no hay ffmpeg. | `evals/media.py` |

Agregar un caso: sumá una entrada a `cases.yaml` (`set`/`append` con rutas punteadas sobre el
spec base) con su `expect: pass|fail`. Para evaluar renders reales con el juez en vivo, usá
`evals.rubric.GeminiJudge` (requiere `GEMINI_API_KEY`; respeta el presupuesto configurado).

Exit code: `0` si todos los casos coinciden con lo esperado, `1` si alguno no.
