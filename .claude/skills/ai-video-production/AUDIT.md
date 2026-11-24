# AUDIT.md — Pre-render narrative audit

> Validación automática que corre ANTES de `npx hyperframes render`. Captura issues estructurales y narrativos que `hyperframes lint` no detecta. Origen: post-mortem mina-abandonada v7 (sesión 2026-05-10).

---

## Qué cubre

| Check | Severidad | Origen del aprendizaje |
|---|---|---|
| `visibility_under_1s` | ERROR si <0.5s, WARN si <1.0s | mina-abandonada v7c: h4-pull flasheaba 0.15s |
| `data_duration_too_short` | WARN | mina-abandonada v7b: h4-hand data-duration=2.5 cortaba la imagen antes que GSAP la ocultara a 68.65 |
| `z_index_covers_captions` | ERROR | mina-abandonada v7 first: black-overlay z-index 94 tapaba caption-wrap z-index 70 |
| `orphan_asset` | WARN | Limpieza — assets generados con $$$ que nunca se referencian |

Cada check **falla con razón concreta** + sugerencia de fix.

---

## Setup en un proyecto nuevo

```bash
uv run ai-video audit-narrative --help   # disponible en cualquier proyecto; nada que copiar
```

No requiere dependencias extra — usa solo la stdlib de Python.

---

## Uso

### Manual

```bash
uv run ai-video audit-narrative          # default: ./index.html
uv run ai-video audit-narrative compositions/main.html
```

Exit code 0 si todos los checks pasan, 1 si hay errores. Las WARN no fallan el exit.

### Como pre-render gate obligatorio

Wrappear el comando de render:

```bash
uv run ai-video audit-narrative && \
  npx hyperframes render --output renders/v8.mp4
```

Si audit falla, el render no arranca. Te ahorraste 12 minutos de render basura.

### Como parte del workflow del agente

Workflow extendido — ver `video-director/WORKFLOW.md` § "Paso 3.5 — Pre-render audit gate".

---

## Output típico

### Caso clean

```
audit-narrative: 24 <img> tags, 18 GSAP-controlled elements
✓ All checks pass
```

### Caso con issues (mina v7c reproducido)

```
[WARN] visibility_under_1s: #h4-pull effective visibility = 0.15s
       (data-start=67.5, data-end=69.7, eff window=[68.5,68.65])
       — image covered by black-overlay almost immediately

[WARN] data_duration_too_short: #h4-hand GSAP keeps opacity:1 until 68.65s
       but data-duration ends at 67.50s (diff = 1.15s).
       Fix: data-duration=3.65

audit-narrative: 0 error(s), 2 warning(s)
```

---

## Cómo agregar un check nuevo

El tool vive en `src/ai_video/audits/audit_narrative.py` (`uv run ai-video audit-narrative`). Cada check es una función `check_<nombre>(...)` que devuelve `list[(severity, check_name, message)]`. Se agregan al pipeline en `main()`.

Plantilla:

```python
def check_my_new_thing(imgs, gsap_events):
    findings = []
    for img in imgs:
        if some_condition_is_bad(img):
            findings.append(
                ("ERROR", "my_new_check_name",
                 f"#{img['id']} explanation + fix suggestion")
            )
    return findings
```

Después en `main()`:

```python
findings += check_my_new_thing(imgs, gsap_events)
```

---

## Qué NO cubre (y debería en el futuro)

| Check | Por qué falta | Cuándo agregarlo |
|---|---|---|
| `caption_text_mismatch_with_active_image` | Requiere parsear el GSAP innerHTML changes y cruzarlo con la imagen activa en ese instante. Complejo. | Cuando aparezca el primer bug "caption A sobre imagen B" en producción |
| `audio_caption_sync_drift` | Necesita parsear `caption-spec.json` (Whisper output) + cruzar con GSAP cap timing. | Cuando los captions Whisper queden desfasados >0.3s |
| `loading_bar_safe_zone_check` | Actualmente solo está en doc, no en script. | Cuando aparezca el primer render con loading bar en `bottom: <540px` |
| `mix_volume_balance` | Requiere ffprobe sobre cada audio + tabla de volúmenes esperados. | Cuando un render tenga música tapando narración |

Cada uno se agrega solo cuando un bug en producción justifica el costo de implementación. **No agregar checks especulativos** — cada check falso-positivo erosiona la confianza en el audit.

---

## Validado en

- mina-abandonada v7c → reproduce `visibility_under_1s` correctamente
- mina-abandonada v7b → reproduce `data_duration_too_short` correctamente

---

## Costo operativo

- Tiempo de ejecución: <1s para HTML de ~500 líneas
- Cero llamadas a API
- Cero credit cost

**Siempre vale la pena correrlo.** No hay razón para skippearlo.
