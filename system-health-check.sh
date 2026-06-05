#!/usr/bin/env bash
# system-health-check.sh — Verifica los invariantes de higiene del repo (READ-ONLY).
#
# Codifica el cleanup manual (2026-06) para que se sostenga solo: el repo trackea SOLO
# el sistema agnóstico (skills, library, creative-specs, componentes, referent-analysis),
# nunca proyectos de video, secretos, bytecode, ni handoffs efímeros per-CP.
#
# Uso:   bash system-health-check.sh
# Exit:  0 = todo verde · 1 = hay invariantes violados
# NO escribe ni borra NADA. Seguro de ejecutar siempre (incl. mientras corre un video).

set -uo pipefail
cd "$(dirname "$0")" || exit 2

PASS=0; FAIL=0
ok()   { printf "  \033[32m✅ %s\033[0m\n" "$1"; PASS=$((PASS+1)); }
bad()  { printf "  \033[31m❌ %s\033[0m\n" "$1"; FAIL=$((FAIL+1)); }
info() { printf "  \033[33mℹ️  %s\033[0m\n" "$1"; }
list() { printf '       %s\n' "$@"; }

echo "════════════════════════════════════════════════════"
echo "  SYSTEM HEALTH CHECK — repo hygiene (read-only)"
echo "════════════════════════════════════════════════════"

# ── [1] Solo el sistema agnóstico tracked (allowlist top-level) ──
# Cualquier entrada top-level tracked fuera del allowlist = sospecha de proyecto leakeado
# (la clase del bug cerro-aislado-v4) o adición inesperada. Escala a proyectos NUEVOS solos.
echo "[1] Solo el sistema agnóstico en el repo (no proyectos de video)"
STRAY=$(git ls-files | sed 's#/.*##' | sort -u | grep -vxF \
  -e ".agents" -e ".claude" -e ".gitignore" \
  -e "AUTONOMOUS-FACTORY-ROADMAP.md" -e "CLAUDE.md" -e "EXCALIDRAW-SYSTEM-OVERVIEW.md" \
  -e "FEEDBACK-LOOP.md" -e "HARD-RULES.md" -e "README.md" -e "V4-LAUNCH-CHECKLIST.md" \
  -e "_archive-deprecated-docs" -e "_freeze-manifests" \
  -e "countdown-glitch" -e "countdown-pulse" -e "countdown-slam" \
  -e "creative-specs" -e "elements.json" -e "library" \
  -e "loader-bar" -e "loader-radial" -e "loader-segments" \
  -e "lower-blackletter" -e "lower-distressed" -e "lower-handwritten" \
  -e "lower-stamp" -e "lower-typewriter" \
  -e "referent-analysis" -e "skills-lock.json" -e "system-health-check.sh" || true)
if [ -z "$STRAY" ]; then ok "0 entradas top-level inesperadas (solo sistema)"
else bad "entradas top-level NO esperadas (¿proyecto leakeado? agregalas al .gitignore o al allowlist si son sistema):"; list $STRAY; fi

# ── [2] Sin secretos tracked ──
echo "[2] Secretos (.env / keys)"
SEC=$(git ls-files | grep -iE '(^|/)\.env($|\.)|(^|/)secret|credential' | grep -v -- '-TEMPLATE' || true)
if [ -z "$SEC" ]; then ok "0 secretos tracked"; else bad "SECRETOS tracked (ROTAR la key + git rm --cached):"; list $SEC; fi

# ── [3] Sin bytecode Python tracked ──
echo "[3] Bytecode Python (.pyc / __pycache__)"
PYC=$(git ls-files | grep -E '\.pyc$|(^|/)__pycache__/' || true)
if [ -z "$PYC" ]; then ok "0 .pyc/__pycache__ tracked"; else bad ".pyc tracked (git rm --cached):"; list $PYC; fi

# ── [4] Sin handoffs/verdicts efímeros tracked (git history ES el log) ──
echo "[4] Handoffs/verdicts efímeros per-CP"
HO=$(git ls-files | grep -iE 'CP[0-9].*(handoff|verdict)|(^|/)(FINAL-)?AUDIT.*-handoff' | grep -vi 'HANDOFF-PROTOCOL' || true)
if [ -z "$HO" ]; then ok "0 handoffs efímeros tracked"; else bad "handoffs tracked (deberían ser local-only):"; list $HO; fi

# ── [5] Arquitectura declarada = three-agent (no 'two-agent' stale) ──
echo "[5] Arquitectura en skills (three-agent, no 'two-agent' stale)"
TA=$(grep -rlnE 'two-agent|two agent|sistema de dos agentes|2 agentes' .claude/skills --include='*.md' 2>/dev/null || true)
if [ -z "$TA" ]; then ok "sin 'two-agent' stale"; else bad "'two-agent' stale en:"; list $TA; fi

# ── [6] Scripts core del bootstrap presentes en templates ──
echo "[6] Scripts core del bootstrap (copy-list canónica)"
TPL=".claude/skills/ai-video-production/templates/scripts"
MISS=""
for f in tts.py image.py sfx.py captions.py video.py audit-narrative.py render-lock.py \
         audit-frames.py audit-audio.py continuity-check.py qa-gate.py build_clip_atomic.py; do
  [ -f "$TPL/$f" ] || MISS="$MISS $f"
done
if [ -z "$MISS" ]; then ok "scripts core presentes en templates/scripts"
else bad "FALTAN en $TPL:$MISS"; fi

# ── [7] Pointer-targets de la consolidación resuelven (homes canónicos existen) ──
echo "[7] Homes canónicos de los punteros (consolidate-to-pointer)"
PT_MISS=""
for tgt in \
  ".claude/skills/ai-video-production/SFX-PIPELINE.md" \
  ".claude/skills/ai-video-production/CAPTIONS.md" \
  ".claude/skills/ai-video-production/BOOTSTRAP.md" \
  ".claude/skills/horror-choice-format/INGENIERO-PAUTA-MASTER.md" \
  ".claude/skills/choice-format-core/INGENIERO-CHOICE-CORE.md" \
  ".claude/skills/creative-director/master-flow-v2/TEAM-PROTOCOL.md"; do
  [ -f "$tgt" ] || PT_MISS="$PT_MISS $tgt"
done
if [ -z "$PT_MISS" ]; then ok "homes canónicos presentes"; else bad "pointer-targets AUSENTES (punteros rotos):"; list $PT_MISS; fi

# ── [8] Consistencia de gate-count (canónico = 8 pre-render gates) ──
# Caza el cascade 5/6/7→8: cualquier doc que diga "N gates" (N≠8) sin contextualizar como
# subset. El canónico es CLAUDE.md § Pre-render gate = 8 (Gate 0 + 7). Reconciliado 2026-06.
echo "[8] Consistencia gate-count (canónico = 8, sin counts contradictorios)"
GC=$(grep -rniE '\b[567] gates\b' .claude/skills --include='*.md' 2>/dev/null \
  | grep -viE 'canónico de 8|subset|núcleo|de calidad|binarios|V4-LAUNCH|los 3 gates' || true)
if [ -z "$GC" ]; then ok "sin counts de gates contradictorios (todo = 8 o subset marcado)"
else bad "gate-count ≠8 sin contextualizar (cascade — reconciliar al canónico de 8):"; printf '       %s\n' "$GC"; fi

# ── [9] (INFO) ephemera local en proyectos activos — no afecta el repo ──
echo "[9] (info) ephemera local en proyectos activos"
LOCAL_HO=$(find . -path ./.git -prune -o \( -name 'CP*-handoff.md' -o -name 'CP*-AUDIT-verdict.md' \) -print 2>/dev/null \
  | grep -vE '_archive|/.venv/' | wc -l | tr -d ' ')
info "$LOCAL_HO handoffs/verdicts locales en proyectos activos (gitignored — limpialos cuando el proyecto shippee)"

# ── [10] Membresía del gate-set (canónico = los 8 nombres exactos) ──
# El invariante #8 caza la literal '5/6/7 gates' pero NO la MEMBRESÍA: un doc puede decir
# "8 gates" y listar un set divergente (incluir audit-frames-granular como gate, u omitir
# audit-audio/continuity-check) — así sobrevivió el BOOTSTRAP.md (findings M3/M4). Para los
# docs CLAVE, dentro de cada ventana ±15 líneas de un "8 gates" con LISTA nombrada (≥4 nombres
# canónicos, sin marca subset/pointer) chequeamos las DOS señales concretas de divergencia:
#   A) audit-frames-granular presentado COMO gate numerado ("gate N") → es red adicional, no gate.
#   B) la enumeración OMITE audit-audio o continuity-check (los dos que M3/M4 dejaron caer).
# Matching case-insensitive y con alias (spec-completeness ≡ audit-spec-completeness, Lint ≡ lint)
# para no false-positivear las variantes legítimas de nombre.
echo "[10] Membresía del gate-set (8 nombres canónicos, no listas divergentes)"
# pares "nombre-canónico|regex-de-detección" (alias incluidos)
GATE_PROBES="audit-spec-completeness|spec-completeness lint|lint audit-narrative|audit-narrative render-lock|render-lock audit-frames|audit-frames(\.py)?[^-] audit-audio|audit-audio continuity-check|continuity-check qa-gate|qa-gate"
GATESET_BAD=""
for doc in \
  CLAUDE.md \
  .claude/skills/ai-video-production/BOOTSTRAP.md \
  .claude/skills/video-director/WORKFLOW.md \
  .claude/skills/pre-render-gate/SKILL.md \
  .claude/skills/creative-director/AUDITOR-PROTOCOL.md; do
  [ -f "$doc" ] || continue
  # líneas que mencionan "8 gates"/"8 gate"/"ocho gates"
  for ln in $(grep -niE '\b(8 gates?|ocho gates)\b' "$doc" 2>/dev/null | cut -d: -f1); do
    lo=$((ln-15)); [ "$lo" -lt 1 ] && lo=1; hi=$((ln+15))
    WIN=$(sed -n "${lo},${hi}p" "$doc")
    # excluir mentions pointer/subset (legítimas: "subset del canónico", "núcleo", "Autoridad canónica")
    echo "$WIN" | grep -qiE 'subset|núcleo|nucleo|Autoridad canónica|autoridad canonica' && continue
    # ¿es contexto de LISTA enumerada? (≥4 nombres canónicos presentes, case-insensitive + alias)
    NAMES_PRESENT=0; MISSING_AC=""
    for probe in $GATE_PROBES; do
      canon="${probe%%|*}"; rx="${probe#*|}"
      if echo "$WIN" | grep -qiE "$rx"; then NAMES_PRESENT=$((NAMES_PRESENT+1))
      elif [ "$canon" = "audit-audio" ] || [ "$canon" = "continuity-check" ]; then MISSING_AC="$MISSING_AC $canon"; fi
    done
    [ "$NAMES_PRESENT" -lt 4 ] && continue   # mención suelta, no lista → no exigir membresía
    # Señal A — audit-frames-granular presentado como gate NUMERADO ("gate N")
    EXTRA=""
    echo "$WIN" | grep -iE 'audit-frames-granular' | grep -qiE 'gate [0-9]' && EXTRA="audit-frames-granular(como gate numerado)"
    if [ -n "$MISSING_AC" ] || [ -n "$EXTRA" ]; then
      MSG="$doc:$ln — lista de 8 gates divergente:"
      [ -n "$MISSING_AC" ] && MSG="$MSG omite:$MISSING_AC"
      [ -n "$EXTRA" ]      && MSG="$MSG extra-no-canónico: $EXTRA"
      GATESET_BAD="${GATESET_BAD}${MSG}"$'\n'
    fi
  done
done
if [ -z "$GATESET_BAD" ]; then ok "gate-set canónico {audit-spec-completeness,lint,audit-narrative,render-lock,audit-frames,audit-audio,continuity-check,qa-gate} en docs clave"
else bad "gate-set divergente en docs clave (reconciliar a los 8 nombres canónicos):"; printf '%s' "$GATESET_BAD" | while IFS= read -r l; do [ -n "$l" ] && list "$l"; done; fi

# ── [11] Q-count del pre-render-gate (canónico = 24 Q, Q1-Q25 salta Q23) ──
# Ningún doc activo puede decir "20 Q"/"21 Q"/"20 preguntas"/"21 preguntas" del pre-render-gate.
# Scope: .claude/skills/ + root .md (CLAUDE.md INCLUIDO — reconciliado completo 2026-06-04), sin _archive*.
echo "[11] Q-count del pre-render-gate (canónico = 24 Q, no '20/21 Q' stale)"
QC=$(grep -rniE '\b(20|21)[ -]?(Q|preguntas)\b' .claude/skills *.md --include='*.md' 2>/dev/null \
  | grep -vE '/_archive|(^|/)_archive' \
  | grep -iE 'pre-render|pregunta|gate|técnic|[^A-Za-z]Q[^A-Za-z]' || true)
if [ -z "$QC" ]; then ok "sin Q-counts '20/21 Q' stale del pre-render-gate (todo = 24, Q1-Q25 salta Q23)"
else bad "Q-count stale del pre-render-gate (reconciliar a '24 Q, Q1-Q25 salta Q23'):"; printf '       %s\n' "$QC"; fi

echo "════════════════════════════════════════════════════"
if [ "$FAIL" -eq 0 ]; then
  printf "  \033[32m✅ SISTEMA LIMPIO — %d/%d invariantes OK\033[0m\n" "$PASS" "$PASS"
  echo "════════════════════════════════════════════════════"
  exit 0
else
  printf "  \033[31m❌ %d invariante(s) violado(s) — %d OK\033[0m\n" "$FAIL" "$PASS"
  echo "════════════════════════════════════════════════════"
  exit 1
fi
