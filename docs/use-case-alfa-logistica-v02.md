# Use Case v0.2 — Acme Logistics Ltd

## Objective

Validate the `Intake → Assessment → Gate Review → Roadmap` workflow on a logistics SME without making any production changes.

## Summary Context

- 80 employees, 65 IT users, 2 locations
- 24/7 operations; maximum downtime: 2 hours
- Initial budget cap: EUR 35,000
- On-premise Active Directory and Microsoft 365
- 4 VMware VMs running Windows Server 2016/2019
- Business-critical ERP
- Veeam on NAS; no complete restore test performed in the last 12 months
- Fortinet firewall and remote user VPN
- Windows endpoints and helpdesk via email
- Non-uniform MFA; no SIEM

## Acceptance Criteria

The test is passed if the report contains:

1. 9 specialist domains;
2. confirmed facts, assumptions, and missing data clearly separated;
3. recommendations with unique IDs;
4. severity between `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`;
5. individual gatekeeper decision;
6. verifiable conditions and rollback steps;
7. roadmap within EUR 35,000;
8. no execution without explicit approval.

## Test Prompt

```text
Load skill it-team-orchestrator.

Start an assessment for Acme Logistics Ltd using the documented context in this file.
Run intake, assessment of the 9 domains, gate review, and a 90-day roadmap.
Do not make any changes. If data is missing, clearly separate facts, assumptions, and unknowns.
Return structured output according to the v0.2 contract.
```
