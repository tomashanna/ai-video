# ANIMATION-LAYER.md — REDIRECT

> Este doc se **MOVIÓ** a su propia skill: `video-animation`.

## Por qué se movió

Aprendizaje 2026-05-11: `ANIMATION-LAYER.md` dentro de `ai-video-production/` no se auto-activaba cuando el usuario decía "animar" o "Kling". El agente tenía que descubrirlo manualmente. Ahora vive como skill independiente con auto-trigger en su description.

## Nueva ubicación

`.claude/skills/video-animation/`

| Archivo | Path |
|---|---|
| Entry point | `video-animation/SKILL.md` |
| Doc maestro completo (12 secciones) | `video-animation/ANIMATION-LAYER.md` |

## Cuándo se auto-activa la nueva skill

El skill `video-animation` se carga automáticamente cuando el usuario menciona:
- "animar", "animación", "Kling", "Replicate"
- "image-to-video", "video-AI", "video animado", "clip animado"
- "vamos a animar el video", "darle vida al video"
- "convertir las imágenes en clips"

## Cross-references actualizadas

Cualquier referencia previa a `ai-video-production/ANIMATION-LAYER.md` debe leerse como `video-animation/ANIMATION-LAYER.md`.

Docs ya actualizadas:
- `docs/OPERATING-MANUAL.md` § Mapa de docs autoritativos (ref canónica)
- `video-director/SKILL.md`
- `ai-video-production/SKILL.md` (eliminada referencia a ANIMATION-LAYER local)

## Última actualización

2026-05-11. Stub de redirección.
