# CLAUDE.md

@AGENTS.md

## Notas para Claude Code

- Las skills del proyecto están en `.claude/skills/` (las de HyperFrames son symlinks a `.agents/skills/`).
  Activá las que indique la tabla de roles de `AGENTS.md`; el detalle de triggers y lecturas obligatorias
  por rol está en `docs/OPERATING-MANUAL.md` § Step 0.
- `/video-new` (`.claude/commands/video-new.md`) arranca un video nuevo siguiendo el bootstrap canónico.
- Los handoffs entre roles van por filesystem (`projects/<id>/CP[N]-handoff.md`, git-ignored), no por
  memoria conversacional.
