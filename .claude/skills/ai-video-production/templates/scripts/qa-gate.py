#!/usr/bin/env python3
"""
qa-gate.py — Pre-Kling QA gate. Bloquea stop point si score < 9.7.

Codifica como CÓDIGO (no solo regla en docs) la regla:
"Pre-Kling stop point requiere ≥9.7. Iterar con fixes NO-KLING hasta llegar."

Razón: el agente productor PUEDE saltarse reglas en docs si su lógica
interna lo lleva a stoppear. Este gate bloquea el camino literalmente.

Usage:
  python qa-gate.py --score 9.3 --stage pre-kling
    → exit 1, blocks stop point
  python qa-gate.py --score 9.7 --stage pre-kling
    → exit 0, OK to proceed to Kling

Integration con el flow del agente productor:
  En lugar de:
    score = run_gemini_qa()
    print(f"Score: {score}")
    if user_wants_kling:
        go_to_kling_stage()

  Hacer:
    score = run_gemini_qa()
    subprocess.run([
        "python", "scripts/qa-gate.py",
        "--score", str(score),
        "--stage", "pre-kling"
    ], check=True)  # raises if score < 9.7
    # Solo llega acá si score ≥ 9.7
    go_to_kling_stage()
"""

import argparse
import sys


# Umbrales canónicos del proyecto (2026-05-13)
PRE_KLING_THRESHOLD = 9.7
POST_KLING_THRESHOLD = 9.7
STRUCTURAL_ROT_THRESHOLD = 7.0


def gate(score: float, stage: str, iteration: int = 1) -> int:
    """
    Returns exit code: 0 = pass, 1 = block.
    """
    if score < STRUCTURAL_ROT_THRESHOLD:
        print(f"🚨 STRUCTURAL ROT — score {score} < {STRUCTURAL_ROT_THRESHOLD}")
        print(f"   Algo estructural está roto. NO iterar — escalar al usuario YA.")
        print(f"   Revisar diseño desde la raíz del NARRATIVE.md.")
        return 1

    if stage == "pre-kling":
        if score < PRE_KLING_THRESHOLD:
            print(f"❌ PRE-KLING QA GATE BLOCKED")
            print(f"   Score actual: {score} < umbral {PRE_KLING_THRESHOLD}")
            print(f"   Iteración: {iteration}/3")
            print()
            print(f"   ⚠️ NO autorizado reportar al usuario ni proceder a Kling.")
            print()
            print(f"   Iterar con fixes NO-KLING en orden A→B→C:")
            print(f"     A. Guion/captions — rewrite frases vagas, eliminar '...' antes")
            print(f"        de proper nouns, comprimir intro si >10% del total")
            print(f"     B. Assets — regenerar imágenes confusas, agregar detail shots,")
            print(f"        setup elements del twist con timing 2.5-3.5s")
            print(f"     C. Wiring/mix — ambient missing, volumes canónicos,")
            print(f"        captions safe zone, opacity gaps")
            print()
            print(f"   Kling NO rescata score bajo — agrega +0.1-0.2 sobre baseline.")
            print(f"   Si tras 3 iteraciones sigue <{PRE_KLING_THRESHOLD} → ESCALAR.")
            return 1

        print(f"✅ PRE-KLING QA GATE PASSED")
        print(f"   Score: {score} ≥ {PRE_KLING_THRESHOLD}")
        print(f"   OK to proceed to Kling stage (cumple hard rule primeros 30s)")
        return 0

    elif stage == "post-kling":
        if score < POST_KLING_THRESHOLD:
            print(f"❌ POST-KLING QA GATE BLOCKED")
            print(f"   Score actual: {score} < umbral {POST_KLING_THRESHOLD}")
            print(f"   Final post-Kling requires ≥{POST_KLING_THRESHOLD}")
            print(f"   Iterar Kling clips problemáticos o regresar a fixes no-Kling.")
            return 1

        print(f"✅ POST-KLING QA GATE PASSED")
        print(f"   Score: {score} ≥ {POST_KLING_THRESHOLD}")
        print(f"   Ready to ship — reportar al usuario con score honesto.")
        return 0

    else:
        print(f"❌ INVALID STAGE: {stage}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="QA gate to block sub-9.7 stop points (Pre-Kling regla 2026-05-13)."
    )
    parser.add_argument(
        "--score", type=float, required=True,
        help="Gemini QA score (0.0-10.0)"
    )
    parser.add_argument(
        "--stage", choices=["pre-kling", "post-kling"], required=True,
        help="Pipeline stage: pre-kling (antes de Replicate) o post-kling (final)"
    )
    parser.add_argument(
        "--iteration", type=int, default=1,
        help="Iteration number (1-3). After 3 sub-9.7 iter → ESCALATE."
    )

    args = parser.parse_args()

    if args.score < 0 or args.score > 10:
        print(f"❌ Invalid score: {args.score}. Must be 0.0-10.0")
        return 1

    if args.iteration > 3:
        print(f"🚨 ESCALATION REQUIRED — {args.iteration} iterations sin llegar a 9.7")
        print(f"   Reportar al usuario con análisis dimensión-por-dimensión.")
        return 2  # Distinct exit code for escalation

    return gate(args.score, args.stage, args.iteration)


if __name__ == "__main__":
    sys.exit(main())
