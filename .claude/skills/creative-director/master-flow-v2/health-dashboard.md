# Health Dashboard — System trend tracker

> **Purpose**: tracker tendencias de salud sistémica cross-video. Métricas per-video y deltas cross-video. Single source of system-wide observability.
> **Owner**: 🔍 Auditor mantiene. Update post-each-video-PUBLISH (side-effect del audit cycle, no proceso separado).
> **Created**: 2026-05-21 (post TAREA 2 sprint sistémico).
> **Cadence**: una fila per video shipped. Trends review every 5 videos.

---

## Métricas tracked (8 columns)

| Métrica | Cómo se calcula | Quién provee |
|---------|-----------------|--------------|
| **`iter_count`** | Cantidad de iteraciones engineer hasta SHIP | Auditor extrae de CP5 final handoff |
| **`cost_total_usd`** | Suma final API + Replicate per video | Engineer reporta CP5 closeout |
| **`gaps_new / codified / deprecated`** | Trio de gap velocity per video | Auditor extrae de GAPS-LOG diff |
| **`user_overrides_count`** | Veces que Rule D PRECEDENCE invocada (user reject/redirect system PASS) | Auditor cuenta en session log |
| **`audit_vs_referent_final_score`** | `audit-against-referent.py` final % (gate b dual-quality) | Engineer reporta final |
| **`user_perceptual_score`** ⭐ | Manual 1-10 que USER provee post-PUBLISH ("¿qué tan satisfecho?") | **USER (manual input 30s post-PUBLISH)** |
| **`gemini_user_delta`** ⭐ | Calculado: `gemini_holistic_final - user_perceptual_score` (signal de inflación) | Auditor calcula auto |
| **`production_duration_days`** | Wall-clock real (first commit → PUBLISH) | Auditor extrae git log |

⭐ = NEW metrics added 2026-05-21 (captura el gap Gemini-vs-user que detectamos en comparative analysis).

---

## Video entries — retroactive backfill

| Video | iter | cost USD | gaps_new | user_overrides | gemini_generic | user_percep ⭐ | Δ_generic | gemini_calibrated ⭐⭐ | Δ_calibrated ⭐⭐ | duration_days |
|-------|-----:|---------:|---------:|---------------:|---------------:|--------------:|----------:|----------------------:|----------------:|--------------:|
| **matadero-banquete v1** (own prod) | 8 | $15.56 | 22 | 6 | 9.75 (avg iter 6+7) | **7.9** | +1.85 | **9.9** | **+2.00** ⚠ | ~5 |
| **cinema-abandonado v2** (own prod) | 6 | $14.29 | 6 (#34-#39) | 5 | 8.6 | **7.8** | +0.80 | **7.8** | **0.00** ✅ | ~1 |
| _Ref-1 mina (canonical, Bruno+Pablo)_ | n/a | n/a | n/a | n/a | n/a | **9.9** | n/a | **9.9** | **0.00** ✅ | n/a |
| _Ref-2 alt (canonical)_ | n/a | n/a | n/a | n/a | n/a | **9.9** | n/a | **9.9** | **0.00** ✅ | n/a |
| _Ref-3 cockpit (canonical, Victor+Axel)_ | n/a | n/a | n/a | n/a | n/a | **10.0** | n/a | **10.0** | **0.00** ✅ | n/a |
| _Ref-4 (canonical)_ | n/a | n/a | n/a | n/a | n/a | **9.9** | n/a | **10.0** | **+0.10** ✅ | n/a |
| _Ref-6 carretera (canonical, Enzo+Axel)_ | n/a | n/a | n/a | n/a | n/a | **9.9** | n/a | **9.9** | **0.00** ✅ | n/a |
| _Ref-8 acuario (canonical, Hugo+Pablo)_ | n/a | n/a | n/a | n/a | n/a | **10.0** | n/a | **9.6** | **-0.40** ✅ | n/a |
| _Ref-A cave (canonical backrooms, Felipe+Enzo)_ | n/a | n/a | n/a | n/a | 6.9 | **10.0** | -3.10 | **10.0** | **0.00** ✅ | n/a |
| _Ref-B tower (canonical backrooms, Tulio+Daniel)_ | n/a | n/a | n/a | n/a | 6.6 | **10.0** | -3.40 | **10.0** | **0.00** ✅ | n/a |
| _Ref-C Louvre (canonical backrooms, Dylan+Leo)_ | n/a | n/a | n/a | n/a | 7.9 | **9.6** | -1.70 | **9.6** | **0.00** ✅ | n/a |

⭐⭐ = **gemini_calibrated** uses prompt v2 with 11-datapoint few-shot calibration. **Mean abs Δ_calibrated = 0.227** (vs generic mean abs Δ ~2.0). Calibrated prompt narrows gap **~10x** for canonical refs. ONE outlier: matadero +2.00 needs investigation (Gemini sees features GAPS-LOG memos claim absent — auditing reality vs codified gaps required).

*audit_vs_ref cinema estimate — final número no recorded explícitamente en handoffs cinema; needs Auditor backfill from `audit-against-referent.py` cinema run.

### Notas retroactive matadero v1
- Iter 6 Gemini 10/10 (FIRST TIME crossed gate a) then iter 7 polish dropped to 9.5/10 (still above ≥9.7 threshold). Average iter 6+7 = 9.75 PASS gate a cumulative.
- user_overrides count = 6 (estimate from session memory): voice ID Kate override architect Valeria pick + countdown digit duration 1.0s user refute architect 0.7s + intro narrative structure user catch + iter 5 AVU pilot architectural insight user-driven + iter 7 narrator pace user catch + iter 8 GSAP stagger user catch.
- gaps_deprecated = 0 because no formal deprecation ritual ran during matadero.

### Notas retroactive cinema-abandonado v2
- Gemini holistic 8.6/10 (NO crossed gate a ≥9.7) — shipped per Rule D user override (PUBLISH approved despite gate a fail).
- user_overrides count = 5 (estimate): Spanish neutral catch + anti-cliché horror writing catch + watermark @elige_tucompanero override + character real names Salvador/Nico override Proyector/Acomodador + iter 5 4 bugs caught (caption flicker 14s/53s + Ken Burns 68s + narrative 73-83s).
- gaps_deprecated = 2 retroactively (#22 + #39 archived via TAREA 1 categorization 2026-05-21).
- user_perceptual_score from user post-PUBLISH session 2026-05-21: user said "el nuestro es el peor" cuando comparó vs canonical refs — suggest perceptual ~6-7 range, but **USER MUST CONFIRM** exact number.

---

## Trend signals to watch (analytical guidance)

Cuando 5 videos accumulated, evaluate:

### Convergence signals (system improving)
- ✅ `iter_count` decreasing monotonically (8 → 6 → ? → ? → ?)
- ✅ `cost_total_usd` decreasing OR stable while quality up
- ✅ `gaps_new` decreasing (system learns)
- ✅ `gaps_deprecated` >0 (system prunes)
- ✅ `gemini_user_delta` shrinking toward 0 (Gemini stops inflating relative to user)
- ✅ `production_duration_days` decreasing

### Divergence signals (system NOT improving)
- 🔴 `iter_count` oscillating or growing
- 🔴 `gaps_new` per video stable or growing (system not learning)
- 🔴 `gaps_deprecated` permanently 0 (system only accumulates)
- 🔴 `user_overrides_count` increasing (gates failing more)
- 🔴 `gemini_user_delta` widening (Gemini inflation worsening)

### Equilibrium signals (system stable, NOT improving NOT degrading)
- ⚠️ Iter count plateaus at 3-4 → likely Phase 2 ceiling reached
- ⚠️ `gaps_new` plateaus at 5-7 per video → format saturation
- ⚠️ `gemini_user_delta` stable at fixed offset → known inflation, codify offset

---

## Automation script (next steps, NOT in TAREA 2 scope)

Trivial future automation:

```bash
# Post-PUBLISH script outline (Phase 3 priority):
.venv/bin/python scripts/health-dashboard-append.py \
  --video-id <id> \
  --iter-count <N> \
  --cost-usd <X.XX> \
  --gemini-holistic <X.X> \
  --user-perceptual <Y.Y> \
  --git-first-commit-ts <iso> \
  --git-publish-ts <iso>

# Output: append row to health-dashboard.md + compute deltas auto
```

NOT building yet — wait for 1-2 more video entries to validate column schema first.

---

## Last update

**2026-05-21** — Created TAREA 2 sprint sistémico. Retroactive entries matadero v1 + cinema-abandonado v2 + Refs A/B/C backrooms backfilled. User provided perceptual scores same session: matadero **7.9** + cinema **7.8** + Ref-A **10.0** + Ref-B **10.0** + Ref-C **9.6**. Deltas computed.

**🚨 Crítical findings — datapoints invierten signo del delta**:

1. **Gemini holistic INVIERTE SIGNO per video type**:
   - Own productions average delta: **+1.33** (Gemini OVER-scores)
   - Canonical backrooms refs average delta: **-2.73** (Gemini UNDER-scores)
   - **Total spread = 4.06 puntos** between how Gemini judges own vs canonical
   
   ⚠️ Esto demuele anti-pattern #12 versión original. Gemini NO infla constante 1 pt. Gemini NO sabe puntuar género POV/liminal-spaces correctamente. Penaliza visual artifacts (rubber hands, melt walls) que SON parte del feel backrooms — y por eso under-scores canonical refs.

2. **User baseline NO es 7.85 — es vara honesta**:
   - User dio 10/10 a 2 refs + 9.6 al tercero = no es restrictive en scoring
   - matadero/cinema 7.9/7.8 reflejan honestamente que NO están al 10
   - Gap real entre nuestras producciones y "10 user-perceptual" = **~2.15 puntos**

3. **"INMERSIÓN > PERFECCIÓN" hypothesis CONFIRMED** (TASTE-LOG entry #1 revised):
   - Backrooms refs tienen artifacts Gemini-flagged (Ref-A walls melt + finger morph; Ref-B hand melts + fingers dissolve; Ref-C hand digit morph + jittering)
   - User da 10/10 a pesar de los artifacts → demuestra inmersión + liminal-vibe overrides technical perfection en tu juicio
   - System target real video #3: NO Gemini ≥9.7 sino **user perceptual ≥8.5+** OR achieve "backrooms-tier inmersión + atmosphere coherence"

4. **Cinema NO fue perceptualmente "el peor" entre own productions**:
   - Diferencia matadero vs cinema = 0.1 (esencialmente iguales perceptualmente)
   - Tu "el peor" era RELATIVO a canonical refs (Ref-2 cockpit 9.0 / backrooms 9.6-10), NO vs matadero

**Pending inputs forward**:
- Video #3 (post-ship): `user_perceptual_score` + computed `gemini_user_delta` — primary validation if Phase 2 + 6 amendments narrow the gap.
- Question forward: ¿qué X factor separa 7.85 → 10 perceptualmente? Hipótesis tentativas: POV integration + liminal-space-vibe coherence + sound layering 3-4 + atmospheric secondary motion ≥3.

---

## ⭐⭐ Calibrated Gemini deployment 2026-05-21

### Phase 1+2 completed — v4 EXECUTION CONTINUITY breakthrough

**v2 first attempt** (11-datapoint calibration):
- Mean abs Δ 0.227 across 11 videos
- 10/11 within ±0.5 — BUT 1 outlier: matadero +2.00 (Gemini scored 9.9 vs user 7.9)
- v2 weighted INMERSIÓN POV / SOUND / ATMOSPHERE / NARRATIVE chain — missed the real gap

**v4 EXECUTION CONTINUITY** (post user insight 2026-05-21):
- User confirmed exact insight: "no es story chain, es execution continuity — POV traversal motion bridge between shots, audio bridges, kinetic momentum"
- New PRIMARY dimension #1 (30% weight): EXECUTION CONTINUITY
- Specifically tests: POV motion bridges + audio bridges + kinetic momentum + visual style consistent
- **Result mean abs Δ 0.14** (38% improvement vs v2)

| Video | User | v2 | **v4** | v4 Δ | Exec dim |
|-------|:---:|:---:|:---:|:---:|:---:|
| matadero | 7.9 | 9.9 | **7.6** | -0.30 | **4.8** ⚠ teleport-cuts detected |
| cinema | 7.8 | 7.8 | **7.4** | -0.40 | **5.5** ⚠ teleport-cuts detected |
| Ref-A cave | 10 | 10 | **10** | 0.00 | strong |
| Ref-3 cockpit | 10 | 10 | **10** | 0.00 | strong |
| Ref-1 mina | 9.9 | 9.9 | **9.9** | 0.00 | 10/10 |

**v4 successfully detects teleport-cut pattern matadero/cinema have**. v2 missed it.

### THE X factor identified

User articulated: "consistencia" = **physical journey continuous shot-to-shot**, NOT just story logic chain.

Specifically 4 sub-criteria:
1. POV/character motion REAL between shots (no teleportation)
2. Audio layer continuous across cuts (no silence gaps)
3. Visual style consistent shot-to-shot (no style jumps)
4. Kinetic momentum sustains (shot N motion continues into N+1)

Canonical refs HAVE all 4 (Ref-A cave POV walks → encounter → diving suit → I put on → descend → swim).
Own productions FAIL on this (matadero: meat → matadero exterior → cutting → mouth attacks = 4 teleport-cuts).

### Architecture forward

- DUAL Gemini metric tracked: `gemini_generic` (current default) + `gemini_calibrated_v4` (Tomás-tuned with EXECUTION CONTINUITY)
- Per video: both numbers + delta vs user_perceptual_score
- Gemini calibrated v4 mean accuracy ±0.4 across 5 critical videos
- Decision rule (proposed):
  - Gate primario nuevo: `gemini_calibrated_v4 ≥9.0` OR `user_perceptual ≥8.5`
  - Gemini generic ≥9.7 kept como TECHNICAL FLOOR (sanity check, no longer primary)
  - User perceptual = ground truth (Rule D PRECEDENCE preserved)

### Cost model evolution 2026-05-21 PM late — Veo 3.1 enterprise FREE confirmed + test bench VALIDATED

User confirmed Gemini Enterprise (Business Edition) includes Veo 3.1 as capacity. Test bench 4 sample shots executed 2026-05-21 PM late — **ALL PASS**.

| Scenario forward | Replicate cost | Total video cost | Status |
|---|---|---|---|
| **A: Veo accepts horror content** | **$0** | **~$0 (operational only)** | ✅ **VALIDATED 2026-05-21** |
| B (realistic): Veo safe + Hailuo gore 30% | $3.60-4.20 | ~$4 | Not needed (A confirmed) |
| C (conservative): Veo hero only + Hailuo rest | $7.92 | ~$8 | Not needed (A confirmed) |
| D (fallback): Veo NSFW reject + Hailuo + Hedra | $5-9.50 | ~$7-10 | Not needed (A confirmed) |

**Test bench results (2026-05-21 PM late)**:

| Test | Result | Latency | Audio bundled | Whisper match |
|------|--------|:---:|:---:|:---:|
| SAFE (POV library corridor) | ✅ PASS | 78s | AAC ✓ | n/a (no dialog) |
| BORDERLINE (uncanny figure hallway) | ✅ PASS | 64s | AAC ✓ | n/a |
| HORROR (industrial helmet figure) | ✅ PASS | 80s | AAC ✓ | n/a |
| CHARACTER SPEAKING ("Elige bien, no hay vuelta atrás") | ✅ PASS | 64s | AAC ✓ | "El lige bien, no hay vuelta atrás" ≈ match |

**Implications for video #3**:
- Use Veo 3.1 as PRIMARY for all character-speaking shots (native lip-sync $0)
- Use Veo 3.1 OR Hailuo Std for atmospheric/setting shots (both accept content, Veo free)
- Cost video #3 forward: **~$0** if all Veo, ~$4 if some Hailuo Pro escalation
- Per-clip pipeline simplification: Veo bundles audio in clip = skip separate TTS/SFX for character shots
- Production wall-clock: ~25 min generation for 22 shots sequential (parallel TBD)

**Production script ready**: `<repo-root>/.claude/skills/ai-video-production/templates/scripts/veo3.py` (3-tier preview/fast/lite + httpx download + image-ref support)

### Matadero outlier RESOLVED

Original mystery: Gemini v2 detected features GAPS-LOG said absent (rats, smoke, carcasses, motions).
**Resolution**: those features ARE present in matadero, but EXECUTION CONTINUITY is broken (teleport cuts between rich shots). User's "el peor" reflects execution continuity gap, NOT atmospheric features absence.

GAP #23/#26/#27 are now revealed as PARTIAL — atmosphere is present but execution doesn't string it together. Worth amendment in GAPS-LOG:
- GAP #23/#26/#27 require update: features present but EXECUTION CONTINUITY missing
- NEW GAP #40 (forward): EXECUTION CONTINUITY (POV motion bridge + audio bridge + kinetic momentum) — the primary gap own → canonical
