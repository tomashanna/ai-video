# ARCHITECTURAL-DECISIONS.md — Override + Decision Log

> **Purpose**: append-only log of architectural overrides + bypass decisions for orchestrator (Script C) + any deviation from canonical workflow. Required by docs/OPERATING-MANUAL.md Hard Rule #24 + Script C gates.
>
> **Status**: ACTIVE log. Append entries chronological. NEVER truncate or rewrite history.
>
> **Schema**: YAML structured per entry. Validation script: `scripts/validate-architectural-decisions.py`

---

## Schema definition (binding)

Per entry MUST contain:

```yaml
- timestamp: <ISO8601 UTC>          # e.g., 2026-05-21T22:30:00Z
  override_flag: <string>           # e.g., "skip-cp3-audit" | "force-pass-cp2-fail" | "cost-cap-bypass"
  cp_affected: <CP1|CP2|CP3|CP4|CP5|GLOBAL>
  reason: <string>                  # MANDATORY explicit reason (≥10 chars, NOT empty)
  agent: <user|auditor|engineer|architect|orchestrator>
  verdict_bypassed: <string|null>   # which verdict bypassed (PASS/NB/FAIL) or null if not applicable
  related_files:                     # optional, files touched
    - path: <string>
      action: <created|modified|deleted>
  notes: <string|null>              # optional extended context
```

**Validation rules**:
- `timestamp` must be valid ISO8601
- `reason` must be ≥10 characters AND non-whitespace
- `cp_affected` enum: CP1 | CP2 | CP3 | CP4 | CP5 | GLOBAL
- `agent` enum: user | auditor | engineer | architect | orchestrator
- `override_flag` must reference real Script C flag (e.g., `--override-cp3-skip` → `override_flag: skip-cp3-audit`)

---

## Append-only entries

```yaml
# Entries appended below as architectural decisions occur.
# Script C MUST append entry for every --override invocation.
# User MUST be notified when override applied (visible in orchestrator output).

# Example skeleton (do not delete — keep as reference):
# - timestamp: 2026-05-21T22:00:00Z
#   override_flag: skip-cp3-audit
#   cp_affected: CP3
#   reason: "V4 iter 3 — only regenerating CP4 animation, CP1-CP3 unchanged from iter 2"
#   agent: user
#   verdict_bypassed: null
#   related_files: []
#   notes: "User initiated targeted iter — full pipeline re-run not needed"

entries: []
```

---

## How Script C uses this file

```python
# Pseudocode:
def apply_override(override_flag, reason, cp_affected, agent, verdict_bypassed=None):
    if not reason or len(reason) < 10:
        raise ValueError("Override requires explicit reason ≥10 chars")
    
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'override_flag': override_flag,
        'cp_affected': cp_affected,
        'reason': reason,
        'agent': agent,
        'verdict_bypassed': verdict_bypassed,
    }
    
    # Append to YAML file (NEVER overwrite)
    append_to_architectural_decisions(entry)
    
    # Log visible to user
    print(f"⚠️ ARCHITECTURAL OVERRIDE: {override_flag} | CP: {cp_affected} | Reason: {reason}")
    print(f"   Logged to ARCHITECTURAL-DECISIONS.md")
```

---

## Forensics use

This log is the FORENSIC RECORD when V4+ fails. Reviewing entries reveals:
- Which gates were bypassed
- Why bypasses authorized
- Patterns of override abuse (if any agent over-uses overrides)
- Cost impact of bypasses (if related to cost-cap-bypass)

**Recurring overrides on same flag** = signal that workflow needs amendment (not more overrides).
