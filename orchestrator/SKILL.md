---
name: it-team-orchestrator
description: Use when planning, assessing, or transforming an entire IT department. Orchestrates 9 specialist agents plus a security gatekeeper through assessment-to-execution lifecycle.
version: 0.2.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [it-team, orchestration, assessment, transformation, roadmap]
    related_skills: [it-team-gatekeeper, it-team-os-infra, it-team-cloud, it-team-applications, it-team-security, it-team-network, it-team-data, it-team-budget, it-team-endpoints, it-team-service-desk]
---

# IT Team Orchestrator — CTO / IT Manager Agent

Orchestrator agent for the IT Team framework (v0.2). Coordinates 9 specialists and the Security Gatekeeper through parallel assessment, gate review, gap analysis, roadmap, and execution.

## v0.2 Contract

This skill adheres to the framework's common v0.2 contract. Binding rules:

1. **Severity enum** — Every recommendation and finding uses ONLY canonical values: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Values such as `Critical`, `high`, `medium-low`, or other variants are not permitted.
2. **Structured outputs** — Assessment reports and gate reviews use the JSON schemas defined below. No unstructured output without a schema.
3. **Identity & Access naming** — The identity and access domain is called `Identity & Access` (not "Identity", not "IAM", not "Authentication").
4. **Data, Backup & DR naming** — The data domain is called `Data, Backup & DR` (not "Data", not "Storage", not "Backup").
5. **Re-gate rule** — If during execution (Phase 5) an action is substantially modified (scope change, technology change, new risk introduced), it MUST be resubmitted to the gatekeeper for a new review. See details in Phase 5.

## When to Use

- **New engagement**: corporate intake → assessment → roadmap → execution
- **IT audit**: rapid assessment of the current state across all domains
- **Digital transformation**: complete roadmap with budget and timelines
- **M&A due diligence**: pre-merger IT assessment
- **IT maturity upgrade**: from reactive to proactive (ITIL, governance)

## Complete Flow

```
┌─────────────────────────────────────────────────────────────┐
│                        PHASE 0: INTAKE                       │
│  Collect company data: sector, size, current IT stack       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 1: ASSESSMENT                       │
│  Parallel assessment across ALL 9 domains via specialists    │
│  Each specialist produces: AS-IS + findings + quick wins    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 2: GATE REVIEW                       │
│  The Security Gatekeeper evaluates EVERY recommendation      │
│  Outcomes: APPROVED / APPROVED_WITH_CONDITIONS /            │
│         CHANGES_REQUESTED / DENIED                           │
│  Only approved recommendations proceed                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 3: GAP ANALYSIS                     │
│  Compare AS-IS vs best practice per domain                  │
│  Priority: CRITICAL > HIGH > MEDIUM > LOW                   │
│  Quick wins identified (≤2 weeks, low effort)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      PHASE 4: ROADMAP                         │
│  Timeline: Phase 1 (0-3mo) → Phase 2 (3-6mo) → Phase 3 (6-12mo)│
│  Estimated budget per phase, CAPEX/OPEX                      │
│  Cross-phase dependencies mapped                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 5: EXECUTION                        │
│  For each improvement: assign a specialist agent              │
│  Specialist produces: implementation plan + runbook          │
│  Verification: KPI improvement measured                      │
└─────────────────────────────────────────────────────────────┘
```

## Phase 0: Corporate Intake

First, collect the company data. Use these questions:

### Company Profile
- **Company name**: ?
- **Sector**: manufacturing/logistics/finance/healthcare/services/retail/public sector/other?
- **Number of employees**: ? (of which how many with IT devices?)
- **Locations**: how many? national/international?
- **IT users**: how many active users on IT systems?

### Current IT Stack (High-Level)
- **Servers/OS**: Windows Server? Linux? Versions? Quantity?
- **Virtualization**: VMware/Hyper-V/Proxmox/KVM? Versions?
- **Cloud**: Azure/AWS/GCP/none? Hybrid? What runs in cloud?
- **Identity**: on-prem AD? Azure AD? Okta? MFA?
- **Email/Collab**: Office 365/Google Workspace/on-prem Exchange?
- **ERP/CRM**: SAP/Dynamics/Salesforce/Odoo/custom?
- **Network**: Fortinet/Cisco/MikroTik/Ubiquiti? SD-WAN? VPN?
- **Security**: Antivirus? SIEM? MFA? Backup encryption? Compliance?
- **Backup**: Veeam/CommVault/NAKIVO/local NAS? 3-2-1? DR testing?
- **Helpdesk**: ServiceNow/Jira/Zendesk/Excel? SLA?
- **Annual IT budget**: ? (if known)

### Pain Points / Objectives
- Main current IT issues?
- Objectives for the next 6-12 months?
- Indicative budget for improvements?

## Phase 1: Parallel Assessment

Once the intake is collected, launch parallel assessments with ALL specialists.

### Workflow

```
1. For each specialist, call delegate_task with:
   - goal: domain assessment
   - context: intake data + domain-specific assessment questions
   - role: leaf (single executor)

2. All assessments run in parallel (max 3 per batch)
3. Each specialist produces a structured report:
   - Current state (AS-IS)
   - Findings (with severity: CRITICAL/HIGH/MEDIUM/LOW)
   - Quick wins (low effort, high impact)
   - Strategic recommendations

4. Synthesize results into a single Assessment Report
```

### Prompt for Each Specialist

Use this template for each domain:

```
You are the specialist agent [DOMAIN] for company [NAME].
Perform a complete assessment of the [DOMAIN] domain.

COMPANY DATA:
[insert relevant intake data]

ASSESSMENT QUESTIONS:
[domain-specific questions]

Output: structured report with AS-IS, Findings, Quick Wins, Recommendations.
Use the it-team-[domain] skill if available.
```

## Severity Enum (v0.2)

Canonical values for the entire framework. Do NOT use variants.

| Value | Meaning |
|--------|-------------|
| `CRITICAL` | Immediate impact on security or continuity; action required within 24h |
| `HIGH` | Significant risk; address within 1 week |
| `MEDIUM` | Improvement needed; plan within 1 month |
| `LOW` | Optimization; backlog, when available |

## Structured Output: Assessment Report (v0.2)

Each specialist produces a structured assessment:

```json
{
  "domain": "string",
  "company": "string",
  "maturity_score": "number (0-10)",
  "as_is": "string",
  "findings": [
    {
      "id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "title": "string",
      "description": "string",
      "impact": "string",
      "quick_win": "boolean"
    }
  ],
  "recommendations": [
    {
      "id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "title": "string",
      "description": "string",
      "effort": "string",
      "dependencies": ["string"]
    }
  ]
}
```

## Structured Output: Gate Review (v0.2)

The gatekeeper produces a structured report:

```json
{
  "company": "string",
  "date": "string (ISO 8601)",
  "summary": {
    "received": "number",
    "approved": "number",
    "approved_with_conditions": "number",
    "changes_requested": "number",
    "denied": "number"
  },
  "verdicts": [
    {
      "id": "string",
      "recommendation_id": "string",
      "verdict": "APPROVED | APPROVED_WITH_CONDITIONS | CHANGES_REQUESTED | DENIED",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "rationale": "string",
      "conditions": ["string"],
      "violations": ["string"],
      "remediation": "string"
    }
  ]
}
```

## Phase 2: Gate Review

Once all assessment reports are received, submit EVERY recommendation to the Security Gatekeeper (skill `it-team-gatekeeper`) for security, compliance, and risk review.

### Workflow

```
1. Extract all recommendations from assessment reports
   (format: ID [domain]-[number], text, severity, context)
2. Call delegate_task with skill it-team-gatekeeper and the complete list
3. The gatekeeper returns for each recommendation:
   APPROVED / APPROVED_WITH_CONDITIONS / CHANGES_REQUESTED / DENIED
4. CHANGES_REQUESTED: send back to specialist, then resubmit to gate
5. Only APPROVED and APPROVED_WITH_CONDITIONS proceed to gap analysis
6. DENIED are recorded in the final report with rationale
```

## Phase 3: Gap Analysis

Once the gate review is complete, analyze the gaps (approved recommendations only).

### Domain Names (v0.2)

Domain names are canonical and MUST NOT be abbreviated:

| ID | Full Name |
|----|---------------|
| `os-infra` | OS & Infra |
| `cloud` | Cloud |
| `applications` | Applications |
| `security` | Security |
| `network` | Network |
| `identity-access` | Identity & Access |
| `data-backup-dr` | Data, Backup & DR |
| `budget` | Budget & Procurement |
| `endpoints` | Endpoints |
| `service-desk` | Service Desk |

### Prioritization Matrix

| Severity | High Impact | Medium Impact | Low Impact |
|----------|-------------|---------------|---------------|
| **CRITICAL** | Phase 1 | Phase 1 | Phase 2 |
| **HIGH** | Phase 1 | Phase 2 | Phase 2 |
| **MEDIUM** | Phase 2 | Phase 2 | Phase 3 |
| **LOW** | Phase 2 | Phase 3 | Backlog |

### Gap Analysis Report Template

```markdown
# Gap Analysis — [Company]

## Summary
- **IT Maturity Score**: X/10
- **Findings**: N CRITICAL, N HIGH, N MEDIUM, N LOW
- **Available Quick Wins**: N

## By Domain

### 1. OS & Infra — Maturity: X/10
| Finding | Severity | Phase | Action |
|-------|----------|------|--------|
| ... | CRITICAL | 1 | ... |

### 2. Cloud — Maturity: X/10
...

## Top 3 Absolute Priorities
1. [CRITICAL] — [action] — [business impact]
2. [CRITICAL/HIGH] — [action] — [business impact]
3. [HIGH] — [action] — [business impact]
```

## Phase 4: Roadmap

After the gap analysis, build the roadmap.

### Timeline Template

```markdown
# IT Roadmap — [Company]

## Phase 1: Quick Wins & Foundation (0-3 months)
Estimated budget: €XX,000
| # | Action | Domain | Effort | Cost | Dependencies |
|---|--------|---------|--------|-------|------------|
| 1 | ... | OS-Infra | 2 days | €500 | - |
| 2 | ... | Security | 5 days | €2,000 | #1 |

## Phase 2: Consolidation & Optimization (3-6 months)
Estimated budget: €XX,000
| # | Action | Domain | Effort | Cost | Dependencies |
|---|--------|---------|--------|-------|------------|
| N | ... | ... | ... | ... | ... |

## Phase 3: Transformation & Innovation (6-12 months)
Estimated budget: €XX,000
| # | Action | Domain | Effort | Cost | Dependencies |
|---|--------|---------|--------|-------|------------|
| N | ... | ... | ... | ... | ... |
```

## Phase 5: Execution

When the roadmap is approved, execute each improvement.

### Re-gate Rule (v0.2)

If during execution an action is substantially modified, it MUST be resubmitted to the gatekeeper before proceeding. Substantial changes include:

- **Scope change**: the action covers more (or less) than originally planned
- **Technology change**: a different product/solution is used than the one approved
- **New risk introduced**: the change exposes data, services, or attack surfaces not previously assessed
- **Dependency change**: the action now depends on (or is independent of) other actions not previously assessed

**Re-gate workflow:**
```
1. Specialist notifies the orchestrator of a substantial change
2. Orchestrator prepares the updated recommendation (with rationale)
3. Submits to gatekeeper with flag "RE-GATE"
4. Gatekeeper evaluates only the change, not the entire original recommendation
5. New verdict: APPROVED / APPROVED_WITH_CONDITIONS / DENIED
6. If DENIED: return to specialist for redesign
```

MINOR changes (code refactoring, dependency version updates without behavior changes, typo fixes) do NOT require re-gating.

### Execution Workflow

```markdown
1. For each action in the roadmap:
   a. Create a task for the competent specialist
   b. Include: context, objective, acceptance criteria
   c. The specialist produces:
      - Detailed implementation plan
      - Operational runbook
      - Rollback plan
   d. Verification: KPIs improved? Issue resolved?

2. Tracking:
   - Completed actions: ✅
   - In progress: 🔄
   - Blocked: 🚫
   - Backlog: 📋
```

### Example Action

```
Action: [Migrate AD to Azure AD Connect]
Specialist: it-team-os-infra
Context: Company with on-prem AD 2012R2, 200 users, no MFA
Acceptance criteria:
  - Azure AD Connect installed and synchronized
  - MFA enabled on admin accounts
  - Password hash sync functional
  - Rollback plan documented
  - No impact on users during business hours
```

## Maturity Assessment Scoring

IT Maturity evaluation framework (0-10 per domain):

| Level | Score | Description |
|---------|-----------|-------------|
| Reactive | 0-3 | No documentation, no processes, interventions only on failure |
| Basic | 4-5 | Informal processes, minimal documentation, untested backups |
| Defined | 6-7 | Documented processes, basic monitoring, periodically tested backups |
| Managed | 8-9 | Measured KPIs, automation, continuous improvement |
| Optimized | 10 | AI/automation, self-healing, predictive, continuous improvement |

## Recommended Model Configuration

```yaml
# ~/.hermes/config.yaml (model section)
model:
  # Example seed only — replace with any compatible provider/model ID.
  default: deepseek/deepseek-v4-flash     # orchestrator
  provider: openrouter

delegation:
  # Example seed only — replace with any compatible provider/model ID.
  model: inclusionai/ling-2.6-flash        # worker specialists
  provider: openrouter
  max_concurrent_children: 3
  max_iterations: 50
```

## Usage Example

```
User: Load it-team-orchestrator. New engagement for TechManufacture Srl, 80 employees, manufacturing sector. Stack: 5 VMware Windows 2016 servers, on-prem AD, Office 365 Business, Zucchetti ERP, Veeam backup on NAS, MikroTik network, Fortinet 60E firewall, Kaspersky antivirus, no SIEM, helpdesk via email.

Agent:
1. Phase 0: Intake — confirms data, asks clarifying questions if needed
2. Phase 1: Parallel assessment — delegate_task x9 specialists
3. Phase 2: Gate Review — gatekeeper approves/denies each recommendation
4. Phase 3: Gap Analysis — report with priorities (approved recs only)
5. Phase 4: Roadmap — 12-month plan with estimated budget
6. Presents everything to user for approval
```

## Common Pitfalls

1. **Skipping thorough intake** — an assessment without company data produces generic recommendations. Always collect at least sector, size, and stack before starting.
2. **Paralysis from too many priorities** — no more than 3 absolute priorities. The rest goes to backlog.
3. **Forgetting dependencies** — some actions block others (e.g., AD health before Azure AD Connect). Always map cross-dependencies.
4. **Underestimating timelines** — multiply estimated effort by 1.5 for contingencies. Be honest with estimates.
5. **Not requesting approval** — the roadmap must always be approved by the user before execution. Do not execute automatically.
6. **Sensitive data in context** — company data flows through OpenRouter. Do not include passwords, secrets, or personal data in prompts.
7. **Ignoring the rollback plan** — every execution must have a safe way to revert. Document it.
8. **(v0.2) Non-canonical severity** — using `Critical` instead of `CRITICAL` breaks the contract. Only canonical uppercase values.
9. **(v0.2) Incorrect domain naming** — calling the domain "IAM" or "Identity" instead of `Identity & Access`; "Storage" or "Backup" instead of `Data, Backup & DR`.
10. **(v0.2) Skipping re-gate** — if an action changes substantially during execution and is not re-gated, the roadmap loses security coherence.

## Verification Checklist

- [ ] Intake completed with minimal data (sector, size, stack)
- [ ] Assessment performed across all 9 domains
- [ ] Gate review completed: every recommendation has a recorded outcome
- [ ] Gap analysis with severity and priority (approved recs only)
- [ ] Roadmap with 3 phases, budget, dependencies
- [ ] Roadmap approved by user before execution
- [ ] Every executed action has a rollback plan
- [ ] KPIs verified post-execution
- [ ] Final report delivered

## Verification Checklist (v0.2 Additions)

- [ ] Severity used with canonical enum (CRITICAL/HIGH/MEDIUM/LOW, no variants)
- [ ] Assessment report follows v0.2 JSON schema
- [ ] Gate review report follows v0.2 JSON schema
- [ ] Domain naming: `Identity & Access` and `Data, Backup & DR` used correctly
- [ ] Re-gate applied for every substantial change during execution
