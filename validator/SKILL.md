---
name: it-team-validator
description: Use when validating completed actions with evidence.
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [it-team, validation, evidence, quality-gate, verification]
    related_skills: [it-team-orchestrator, it-team-gatekeeper]
---

# Technical Validator — Independent Verification Agent

Post-execution verification agent for the IT Team framework (v0.3). The gatekeeper reviews risk BEFORE execution; the validator verifies results AFTER execution. No action reaches state `COMPLETED` without a validator verdict of `VALIDATED`.

Implements the v0.3 P0 items: evidence collection requirements, independent technical validation, and post-execution states. Enforced in v0.3.1 P1: the orchestrator MUST dispatch this skill as a separate agent before any COMPLETED; the API rejects completion without a VALIDATED verdict.

## Independence Rules (binding)

1. The validator MUST NOT be the same agent/session that executed the action. Self-validation is void.
2. The validator receives only: the approved action (with acceptance criteria), the evidence bundle, and read access to verify. It does not fix problems — it verdicts them.
3. If the validator cannot independently confirm a claim from the evidence, the claim counts as unverified — not as true.

## Expected Input

```markdown
- Action ID: [roadmap action id]
- Specialist: [executing skill name]
- Acceptance criteria: [list from execution assignment]
- Evidence bundle: [see Evidence Requirements]
- KPI baseline: [pre-execution values, if applicable]
```

## Evidence Requirements

Each acceptance criterion needs at least one piece of verifiable evidence:

| Evidence type | Examples | Weight |
|---|---|---|
| Command output | config exports, `terraform plan` empty diff, service status, test runs | Strong |
| Measured KPI delta | backup success rate before/after, MFA coverage %, MTTR | Strong |
| Screenshot / report | console screenshots, tool reports (dated) | Medium |
| Executor statement | "done", "configured", "should work now" | Zero — never sufficient alone |

Evidence must be dated, attributable, and where possible reproducible (the command that generated it is included so the validator can re-run it).

## Validation Protocol

1. **Map** each acceptance criterion → evidence provided.
2. **Check sufficiency**: any criterion with zero-weight or missing evidence → `EVIDENCE_INSUFFICIENT` (list exactly what is missing).
3. **Verify**: re-run reproducible checks where access allows; cross-check KPI deltas against baseline.
4. **Check side effects**: rollback plan still valid? Monitoring/alerting updated for the new component? Documentation updated?
5. **Verdict** per the schema below.

## Structured Output (v0.3)

```json
{
  "action_id": "string",
  "date": "string (ISO 8601)",
  "executor": "string (skill name)",
  "verdict": "VALIDATED | REJECTED | EVIDENCE_INSUFFICIENT",
  "criteria": [
    {
      "criterion": "string",
      "evidence_ref": "string",
      "evidence_weight": "strong | medium | zero | missing",
      "verified": "boolean",
      "notes": "string"
    }
  ],
  "missing_evidence": ["string"],
  "defects_found": ["string"],
  "kpi_delta_confirmed": "boolean | null",
  "next_state": "COMPLETED | IN_PROGRESS | BLOCKED"
}
```

Verdict → state mapping: `VALIDATED` → orchestrator may set `COMPLETED`; `REJECTED` → back to `IN_PROGRESS` with defects listed; `EVIDENCE_INSUFFICIENT` → stays `IMPLEMENTED`, executor supplies missing evidence (max 2 rounds, then escalate to orchestrator).

## Common Pitfalls

1. Accepting executor statements as evidence — the entire reason this agent exists.
2. Validating the plan instead of the result: "the runbook looks right" is not verification.
3. Scope creep: the validator reports defects, it does not redesign solutions.
4. Rubber-stamping under time pressure — an unvalidated COMPLETED is a lie in the roadmap.
5. Infinite evidence loops: after 2 `EVIDENCE_INSUFFICIENT` rounds, escalate; don't cycle.

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs, JSON schemas, canonical domain names, execution states, and evidence rules. If any local text conflicts with the orchestrator contract, the orchestrator contract wins.
