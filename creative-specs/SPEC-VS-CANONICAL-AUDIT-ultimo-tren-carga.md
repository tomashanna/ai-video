# SPEC-VS-CANONICAL-AUDIT — ultimo-tren-carga (V7)

**Audited**: 2026-06-03
**SPEC**: creative-specs/ultimo-tren-carga.yaml v11.1 (1786 líneas, 22 shots)
**Auditor**: terminal independiente. Leído DIRECTO: PAUTA-MASTER § 2 (esqueleto + INVARIANTE + 8 perspectivas) + § 3 (reglas inviolables) + § 5/§ 6/§ 7 (hallazgos críticos + Slot A) + canonical-scenes/ref-03 COMPLETO (referente maestro, 579 L) + INDEX grids. Refs secundarios (ref-06/08/09/10) verificados contra las tablas empíricas de PAUTA § 5/§ 6 (no deep-read — claims coincidentes; scope declarado honesto).
**Validators**: re-corridos por el auditor independientemente (NO confiado el self-audit del arquitecto — anti-pattern #17 corolario).

## Validators re-corridos (auditor, independiente)

| Validator | Exit | Resultado auditor |
|---|---|---|
| `audit-spec-structure-vs-canonical` | 0 | PASS — invariante + skeleton + secuencial ✓ |
| `audit-spec-narration-fits-duration` | 0 | PASS 14/14 (MATRIX leída; shots 19/21 freeze_extend declarado) |
| `audit-spec-lip-sync-marks` | 0 | PASS 22/22 (3 dialog Dario consistentes) |
| `audit-spec-narrative-coherence` (+ video-log) | 0 | 0 FAIL · 1 FLAG advisory (shots 08/13/18 — RESUELTO manualmente, ver V6) |
| `audit-spec-genre-fidelity` | 0 | not_applicable (horror) |

Coincide con el self-validation del arquitecto (HR#27 cumplido — corrió los validators de verdad).

## Coverage tally

- references_canonical[] declarados: **5/8** — floor ≥5/8: **PASS**
- Refs no usados con razón declarada (ref-11 outlier @referent-c / ref-12 / ref-13): ✓ aceptable

## Per-ref linkage table

| ref_id | informs[] | ¿Sustantivo? | Verificación del auditor |
|--------|-----------|--------------|--------------------------|
| ref-03 | pattern, counterfactual_placement, cliffhanger_archetype, char_a, shots 06/07, pacing | ✅ SÍ | **Deep-read completo.** Claims EXACTOS vs doc real: Bruno scary-savior P2 (beat 11 reveal "Vámonos, fin del turno") · 3 decisiones anidadas escaladas (linterna/seguir/alarma) con categorías distintas · counterfactual FINAL Paz-perdida (beat 12 Pablo cartas+pan+amanecer ↔ Tobias caseta+termo+gato+tango) · dinámica procedural frases cortas ("Sostenla") · body horror al setting (pozo/dinamita/taladro ↔ descarga/agua negra/barra al rojo). Linkage 1:1 real, no decorativo |
| ref-10 | shots 05/15, drone_base | ✅ SÍ | Rurik enmascarado órdenes procedurales + categoría sumisión/resistencia válvula ↔ D3 barra — coincide con PAUTA § 6 tabla (ref-10 fila) + § 5 |
| ref-06 | shots 11/12, consequence_framing_style | ✅ SÍ | Axel "quedate inmóvil" / impulso mata, pasividad salva ↔ D2 — coincide PAUTA § 6 tabla (ref-06 claxon/silencio) |
| ref-09 | emotional_framing, shots 19/21 | ✅ SÍ | Registro somber de resolución scary-savior; placement NO copiado (declarado explícito — counterfactual va al FINAL per ref-03). Honesto |
| ref-08 | char_b, shot_01 | ✅ SÍ | Hugo/Pablo bueno-aparente que OFRECE + postura acogedora + visualmente extreme permitido (PAUTA § 5 tabla 7/8) ↔ Tobias sonrisa demasiados dientes |

Field paths de informs[] verificados existentes en el SPEC ✓.

## PAUTA-MASTER § 2.4 — las 8 perspectivas (beat-por-beat)

| # | Perspectiva | Verdict | Evidencia |
|---|-------------|---------|-----------|
| 1 | Estructura § 2.1 | ✅ PASS | hook+labels+countdown(LAST) → recorrido jugado (setup→D1/D2/D3 c/u con consequence A muerte + B continúa) → resolución (19/20) → counterfactual FINAL (21) → cliffhanger (22). Calco del esqueleto 5/5 |
| 2 | ⛔ INVARIANTE § 2.2 | ✅ PASS | Tobias (bueno_aparente) en who_is_there SOLO de shot_01/21/22 — verificado en los 22 shots. Tentaciones del played path = entorno/instinto (riel seco / chapoteo / barra que cae) + Dario (ELEGIDO, permitido). Lección V6 F2 aplicada desde diseño |
| 3 | Recorridos secuenciales § 2.3 | ✅ PASS | Jugado completo → counterfactual UNA vez al final. Sin intercalado |
| 4 | Pattern + rotación HR#14 | ✅ PASS | P2 ∈ canónicos; rotación real P6→P3→P2→P1→P9→**P2** (≠P9 ≠P1; P2 descansado desde cerro). Apariencia asimétrica clásica descansada (video-log § Rotación V7 lo recomienda textual) |
| 5 | Name labels § 2.5 | ✅ PASS | DARIO/TOBIAS monospaced large Y11.5, `timestamp_visible_s [0.0, 9.0]` = persistentes through-countdown (bug V6 evitado explícito) |
| 6 | Glitch cambios de historia | ✅ PASS (1 NB) | `old_screen_glitch_error` en muerte→bridge + bridge→rama B (07→08, 08→09, 12→13, 13→14, 17→18, 18→19) ✓. NB-2: inconsistencia textual interna (ver abajo) |
| 7 | Sonido (SFX densos + death-screams + sutil) | ✅ PASS | 33 SFX (banda 30-40) matcheados a la acción per shot · death-scream en CADA consequence-A fatal (07/12/17) · **regla V7+ "sonido de muerte sutil bajo el scream" cumplida en los 3 prompts** ("subtle choked gasp / gurgling drowning gasp / pained gasp underneath") · mix ducked Layer 3 -6dB |
| 8 | Checks pre-existentes | ✅ PASS | WPM/narration-fits 14/14 (verifiqué la aritmética: 16 palabras=5.82s@165 ≤5.9 ✓; 17=6.18s y 18=6.55s → freeze_extend shots 19/21 ✓) · framing acción-condicional 6/6 ("Si pisas/Si corres/Si la atrapas…" — forma DOMINANTE 6/8 primary source; 0 bare-label) · visual-matches-narración literal per shot ✓ · POV 22/22 ✓ · español neutral ✓ · anti-cliché ✓ · nombres reales ✓ · camera_intent descriptivo sin label-prefix (MODEL-BEHAVIOR-LOG E2) ✓ · locus anchor char_a_v1_mask para close-ups de máscara (E1 análogo correcto; sin anatomía contable) ✓ |

## Reglas § 3 adicionales verificadas

- ✅ Rama B explícita post-cada-decisión: bridges 08/13/18 con `bridge_caption` "SI PISAS EL CEMENTO" / "SI TE QUEDAS INMÓVIL" / "SI ESPERAS LA SIGUIENTE" (marcador-puente válido per § 3 corregido 2026-05-29) + consequence B narrada re-marca la rama. **El FLAG del validator queda RESUELTO manualmente** — branch-marking presente vía caption (el validator no ve ui_active)
- ✅ Bueno aparente ≥2 shots pre-cliffhanger: Tobias shot_01 + shot_21 antes de shot_22 — patrón idéntico a ref-03 (Pablo beat 1 + beat 12)
- ✅ Lip-sync intent marcado 22/22; Dario habla bajo máscara → engineer_notes manda patrón sin-boca-visible (anti-pattern #9 cubierto: NO mouth movement sin audio) + D27 voice processing con criterio de inteligibilidad M7.7 (anti-caso matarife)
- ✅ Narración CLARA no tenebrosa (verbo+sujeto+objeto literal en todos los segmentos)
- ✅ Slot A 5 reglas: atrapamiento (reja shot_02) + aislamiento (3 AM sin señal implícito) + función específica (mantenimiento de metro) + diegéticos (riel/charco/escalera/barra/cableado) + iluminación dramática (ámbar emergencia single-source)

## NBs (no bloqueantes — para atención de Tomás y del ingeniero)

1. **🟡 NB-1 (creativo, decisión de Tomás si quiere tocarla): heurística ganadora uniforme en las 3 decisiones.** En V7 la ganadora SIEMPRE es "obedecé la regla que Dario acaba de dar" (D1 cemento, D2 quieto, D3 esperar). En el canon AMBAS variantes existen: ref-09 (8.99) es uniforme "obedecé a Victor" las 3 veces; ref-03 (9.04) la rompe en D2 (seguir la orden de Bruno = dinamita; quedarte contra la orden = vivir). Per Pattern 8 esto es 🟩 variabilidad creativa (NO enforce) — la DUDA real (PAUTA § 6) persiste vía instinto-vs-confianza (huir de lo que respira en el agua es pull visceral aunque sepas la heurística). Lo reporto explícito en vez de racionalizarlo en silencio (anti-pattern #20, lección V6). Si se quiere imprevisibilidad tipo ref-03, el fix mínimo es invertir UNA decisión (la propuesta C original lo hacía en su D3). **Default si no se toca: PASS.**
2. **🟡 NB-2 (textual): inconsistencia interna Layer 2.** `hybrid_layers.layer_2.description` dice glitch también en "played↔counterfactual", pero la transitions table usa `cross_fade_warm` para 20→21 (correcto canónicamente — ref-03 beat 11→12 corta directo a warm; el glitch codificado 2026-06-01 es para cambios-A/B+muerte). Fix: alinear la description con la table. El ingeniero debe seguir la **transitions table**.
3. **🟡 NB-3 (timeline): narration_script llega a ~96s con `total_duration_s_intent: 90`.** Declarado por el arquitecto (engineer ajusta el corte final; banda 80-100s lo absorbe). El ingeniero reconcilia en CP2 y los timestamps de decision UI (`hyperframes_ui_overlay`) se re-derivan del corte real.
4. **🟡 NB-4 (bootstrap CP — HERENCIA HR#30): el TEMPLATE `build_clip_atomic.py` (Capa A) NO contiene `chunk_caption_cues`** (verificado: grep = 0 hits). El fix HR#30 vive solo en los project-local `cp5b_build_atomic.py` de sala-limpia + invernadero. **Condición de bootstrap V7: el ingeniero copia/porta el caption-burn desde `invernadero-turno-riego/scripts/cp5b_build_atomic.py`** (la copia más reciente con fix), NO desde el template. Red de seguridad: Gate 6.5 `audit-caption-temporal-coverage.py` (existe en templates ✓).
5. **🟡 NB-5 (cosmético): dialog Dario "Pisa el cemento. Nunca el riel." = 6 palabras** vs patrón observado "máx 5" (ref-03 "Vámonos, fin del turno" = 4). Son 2 oraciones staccato de ≤3 — espíritu cumplido. Sin acción.
6. **🟡 NB-6 (publicación): caption del Reel + hashtags** (PAUTA § 3 "pregunta directa ¿A quién elegirías?") no viven en el SPEC — entregable de CP5/publicación, recordar al cierre.
7. **🟡 NB-7 (operativo): `enforcement_integration.script_c` declara cap $8/alert $6 (default), pero Tomás autorizó hoy cap $10/alert $8 para V7.** La autorización del user supersede el default — queda registrada acá. Estimación del arquitecto ~$7.8 cabe incluso bajo el default.

## MODEL-BEHAVIOR-LOG constraints check (Gate 5 step 7)

- Entry 1 (face/pose-coupling + stability budget): Dario SIN anatomía contable rara (signature = máscara/wardrobe — diseño deliberado de bajo riesgo). Locus anchor `char_a_v1_mask` declarado para shots 05/15 que aíslan la máscara ✓. Props per shot ≤3 verificado en shots con Dario (peor caso shot_15: escalera+barra+cableado = 3) ✓
- Entry 2 (label-prefix burned text): camera_intent 22/22 en frases descriptivas ✓ + engineer_notes prompt_style_note ✓

## Verdict

**🟡 NB — PROCEED a aprobación de Tomás para CP1.** 0 findings 🔴. Estructura, invariante, rotación, refs, framing, narración-fits, SFX y model-constraints: todos PASS contra fuente primaria directa. Los 7 NBs no requieren rework del SPEC (NB-1 es decisión creativa opcional de Tomás; NB-2/3 los reconcilia el ingeniero; NB-4 es condición de bootstrap que el auditor enforcea en CP-setup).

**Próximo paso**: Tomás aprueba SPEC (con o sin ajuste NB-1) → CP1 anchors (engineer narrow spawn, 1 CP por invocación, gate del auditor entre CPs — HR#24). Cap $10 / alert $8 (autorizado 2026-06-03).
