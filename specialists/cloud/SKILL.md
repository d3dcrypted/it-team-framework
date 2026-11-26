---
name: it-team-cloud
description: 'Use when assessing or improving cloud infrastructure. Assessment protocol + FinOps + migration planning for Azure/AWS/GCP.'
category: cloud
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [cloud, azure, aws, gcp, finops, migration, landing-zone, infrastructure-as-code]
    related_skills: [it-team-budget, it-team-network, it-team-security]
---

# Cloud Specialist — Cloud Architect

Domain: IaaS/PaaS/SaaS cloud (Azure, AWS, GCP), landing zone, migration, cost optimization (FinOps), hybrid cloud, cloud governance.

## Assessment Protocol

### What to Check

**Cloud Architecture**
- Current cloud providers (Azure/AWS/GCP/multi-cloud)
- Deployment model (IaaS/PaaS/SaaS/serverless)
- Landing zone: structured or ad-hoc? Resource groups organized?
- Hybrid cloud: on-prem to cloud connectivity? (ExpressRoute/Direct Connect/VPN)
- Region deployment: single region or multi-region?
- Container orchestration: AKS/EKS/GKE? Self-managed?

**Costs and FinOps**
- Average monthly cloud spend and trend (stable/increasing)
- Reserved instances / Savings Plans in use?
- Resource right-sizing: compute/storage optimized?
- Tagging strategy for chargeback/showback?
- Budget alerts configured?
- Cost anomalies detection active?

**Security Posture**
- RBAC: least privilege applied?
- Network Security Groups / Security Groups: granular rules?
- WAF / Web Application Firewall?
- DDoS protection?
- Encryption: at-rest + in-transit?
- Key management: managed HSM? BYOK?
- Audit logging: centralized retention?

**Governance**
- Policy / Blueprints / Landing Zone?
- Hierarchical subscription/account structure?
- Management groups organized?
- Compliance monitoring? (Azure Policy/AWS Config)
- Backup & DR: region replication? Snapshot policy?
- Cost governance: spending limits? Quotas?

### Key Metrics

| Metric | Target | How to Measure |
|---------|--------|---------------|
| Cloud spend/utilization ratio | < 70% | Cost management dashboard |
| Instance coverage RI/SP | > 60% | RI/SP recommendations |
| Tag compliance | > 95% | Policy compliance report |
| Unused resources | < 5% | Advisor/Trusted Advisor |
| Backup coverage | 100% | Backup reports |
| RBAC compliance | 100% | Access review |

## Improvement Catalog

### Quick Wins (<= 2 weeks)

| # | ACTION | IMPACT | EFFORT |
|---|--------|---------|--------|
| 1 | Enable budget alerts | HIGH | 1h |
| 2 | Delete unattached disks/unused IPs | MEDIUM | 2h |
| 3 | Enable backup on unprotected resources | HIGH | 4h |
| 4 | Implement resource tagging policy | HIGH | 4h |
| 5 | Right-size overprovisioned VMs | HIGH | 8h |
| 6 | Enable Azure Security Center / AWS Security Hub | HIGH | 4h |
| 7 | Set up cost anomalies detection | MEDIUM | 2h |
| 8 | Review and cleanup RBAC assignments | HIGH | 4h |

### Strategic Improvements (1-3 months)

**1. Landing Zone Setup**
Hierarchical structure with management groups, policy, networking hub-spoke.
Azure: Enterprise Scale / ALZ | AWS: Control Tower | GCP: Resource Hierarchy
Effort: 2-4 weeks | Cost: effort only

**2. Cost Optimization Program**
Reduce cloud spend by 20-40% with RI/SP coverage, right-sizing automation, dev/test scheduling, storage tiering.
Effort: 2 initial weeks + ongoing | Savings: 20-40%

**3. Cloud Security Hardening**
Zero-trust: network segmentation hub-spoke, policy compliance, Key Vault for secrets, private endpoints, DDoS protection.
Effort: 3-4 weeks

**4. Disaster Recovery in Cloud**
DR automation: Site Recovery, region replication, runbook automation, quarterly DR testing.
Effort: 2-3 weeks

**5. Container Migration Assessment**
Containerization assessment, AKS/EKS/GKE setup, CI/CD pipeline, monitoring.
Effort: 4-6 weeks

## Implementation Guide

### Cloud Migration - Phases

- **PHASE 1 - Assessment (2 weeks)**: Resource inventory, dependency mapping, TCO comparison, workload prioritization
- **PHASE 2 - Foundation (3-4 weeks)**: Landing zone, VPN/ExpressRoute connectivity, SSO identity, backup baseline
- **PHASE 3 - Migration (variable)**: Lift & shift, re-architect to PaaS, cutover with rollback, testing
- **PHASE 4 - Optimization (ongoing)**: FinOps review, security posture, IaC automation (Terraform/Bicep)

### Recommended Tools

- **Terraform** - Multi-cloud IaC (free)
- **Infracost** - IaC cost estimation
- **Azure Cost Mgmt / AWS Cost Explorer** - Cost analysis (included)
- **Prometheus/Grafana** - FOSS monitoring
- **CloudHealth** - Multi-cloud FinOps (paid)

### Common Errors

1. Skipping landing zone → chaos. Always landing zone first.
2. Tags not applied → chargeback impossible. Enforce via policy.
3. Overprovisioning → large VMs for safety. Right-sizing automation.
4. No RI/SP → on-demand 30-50% more expensive.
5. Forgotten backup → backup ALL resources.
6. Overly broad access → strict RBAC (contributor on RG, not subscription).
7. Secrets in plaintext → Key Vault/Secrets Manager always.
---

## Output Contract

All specialist assessments produce structured deliverables:

| Deliverable | Format | Audience |
|---|---|---|
| Executive Summary | 1-page markdown or PDF | Leadership, C-suite |
| Findings Register | Table with severity and effort | IT Manager, Technical Leads |
| Recommendations Backlog | Prioritized list (impact × effort) | Project team |
| Metrics Dashboard | KPI values vs. targets | Ongoing governance |

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), assessment report JSON schema, canonical domain names, execution states, and evidence rules. Do not redefine those here; if any local text conflicts with the orchestrator contract, the orchestrator contract wins.


## Privacy & Data Handling

- Assessment data classified per organization policy (public / internal / confidential / restricted).
- PII in findings must be redacted or anonymized in all deliverables.
- Reports stored only in approved repositories or encrypted shares.
- Credentials, secrets, and API keys must never appear in deliverables.
- Comply with GDPR, HIPAA, SOX, and local regulations where applicable.
- Data retention follows organization retention schedule; dispose per policy.

