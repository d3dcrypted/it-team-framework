---
name: it-team-cloud
description: 'Use when assessing or improving cloud infrastructure. Assessment protocol + FinOps + migration planning for Azure/AWS/GCP.'
category: cloud
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [cloud, azure, aws, gcp, finops, migration, landing-zone, infrastructure-as-code]
    related_skills: [it-team-budget, it-team-network, it-team-security]
---

# Specialista Cloud — Cloud Architect

Dominio: cloud IaaS/PaaS/SaaS (Azure, AWS, GCP), landing zone, migration, cost optimization (FinOps), hybrid cloud, cloud governance.

## Assessment Protocol

### Cosa Controllare

**Architettura Cloud**
- Provider cloud attuali (Azure/AWS/GCP/multi-cloud)
- Modello di deployment (IaaS/PaaS/SaaS/serverless)
- Landing zone: strutturata o ad-hoc? Resource group organizzati?
- Hybrid cloud: connessione on-prem al cloud? (ExpressRoute/Direct Connect/VPN)
- Region deployment: singola regione o multi-regione?
- Container orchestration: AKS/EKS/GKE? Self-managed?

**Costi e FinOps**
- Costo cloud mensile medio e trend (stabile/crescente)
- Reserved instances / Savings Plans utilizzate?
- Resource right-sizing: compute/storage ottimizzati?
- Tagging strategy per chargeback/showback?
- Budget alerts configurati?
- Cost anomalies detection attiva?

**Security Posture**
- RBAC: least privilege applicato?
- Network Security Groups / Security Groups: regole granulari?
- WAF/Web Application Firewall?
- DDoS protection?
- Encryption: at-rest + in-transit?
- Key management: managed HSM? BYOK?
- Audit logging: retention centralizzata?

**Governance**
- Policy / Blueprints / Landing Zone?
- Subscription/Account structure gerarchica?
- Management groups organizzati?
- Compliance monitoring? (Azure Policy/AWS Config)
- Backup & DR: region replication? Snapshot policy?
- Cost governance: spending limits? Quotas?

### Metriche Chiave

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| Cloud spend/utilization ratio | < 70% | Dashboard cost management |
| Instance coverage RI/SP | > 60% | RI/SP recommendations |
| Tag compliance | > 95% | Policy compliance report |
| Unused resources | < 5% | Advisor/Trusted Advisor |
| Backup coverage | 100% | Backup reports |
| RBAC compliance | 100% | Access review |

## Improvement Catalog

### Quick Wins (<= 2 settimane)

| # | AZIONE | IMPATTO | SFORZO |
|---|--------|---------|--------|
| 1 | Enable budget alerts | HIGH | 1h |
| 2 | Delete unattached disks/unused IPs | MEDIUM | 2h |
| 3 | Enable backup on unprotected resources | HIGH | 4h |
| 4 | Implement resource tagging policy | HIGH | 4h |
| 5 | Right-size overprovisioned VMs | HIGH | 8h |
| 6 | Enable Azure Security Center / AWS Security Hub | HIGH | 4h |
| 7 | Set up cost anomalies detection | MEDIUM | 2h |
| 8 | Review and cleanup RBAC assignments | HIGH | 4h |

### Migliorie Strategiche (1-3 mesi)

**1. Landing Zone Setup**
Struttura gerarchica con management groups, policy, networking hub-spoke.
Azure: Enterprise Scale / ALZ | AWS: Control Tower | GCP: Resource Hierarchy
Effort: 2-4 settimane | Costo: solo effort

**2. Cost Optimization Program**
Ridurre cloud spend del 20-40% con RI/SP coverage, right-sizing automation, dev/test scheduling, storage tiering.
Effort: 2 settimane iniziali + continuo | Risparmio: 20-40%

**3. Cloud Security Hardening**
Zero-trust: network segmentation hub-spoke, policy compliance, Key Vault per secret, private endpoints, DDoS protection.
Effort: 3-4 settimane

**4. Disaster Recovery in Cloud**
DR automation: Site Recovery, region replication, runbook automation, DR test trimestrale.
Effort: 2-3 settimane

**5. Container Migration Assessment**
Containerization assessment, AKS/EKS/GKE setup, CI/CD pipeline, monitoring.
Effort: 4-6 settimane

## Implementation Guide

### Cloud Migration - Fasi

- **FASE 1 - Assessment (2 settimane)**: Inventario risorse, dependency mapping, TCO comparison, workload prioritization
- **FASE 2 - Foundation (3-4 settimane)**: Landing zone, connectivity VPN/ExpressRoute, SSO identity, backup baseline
- **FASE 3 - Migration (variabile)**: Lift & shift, re-architect per PaaS, cutover con rollback, testing
- **FASE 4 - Optimization (continuo)**: FinOps review, security posture, IaC automation (Terraform/Bicep)

### Tool Consigliati

- **Terraform** - IaC multi-cloud (gratuito)
- **Infracost** - Cost estimation IaC
- **Azure Cost Mgmt / AWS Cost Explorer** - Cost analysis (incluso)
- **Prometheus/Grafana** - Monitoring FOSS
- **CloudHealth** - Multi-cloud FinOps (a pagamento)

### Errori Comuni

1. Landing zone saltata -> caos. Sempre landing zone prima.
2. Tag non applicati -> chargeback impossibile. Obbliga via policy.
3. Overprovisioning -> VM grandi per sicurezza. Right-sizing automation.
4. Nessun RI/SP -> on-demand 30-50% piu caro.
5. Backup dimenticato -> backup su TUTTE le risorse.
6. Accessi troppo ampi -> RBAC strict (contributor su RG, non subscription).
7. Secret in chiaro -> Key Vault/Secrets Manager sempre.
---

## Output Contract

All specialist assessments produce structured deliverables:

| Deliverable | Format | Audience |
|---|---|---|
| Executive Summary | 1-page markdown or PDF | Leadership, C-suite |
| Findings Register | Table with severity and effort | IT Manager, Technical Leads |
| Recommendations Backlog | Prioritized list (impact × effort) | Project team |
| Metrics Dashboard | KPI values vs. targets | Ongoing governance |

## Severity Levels

| Level | Definition | SLA |
|---|---|---|
| **CRITICAL** | Immediate risk to operations, data, or compliance | Action within 48 h |
| **HIGH** | Significant impact; degrades service or increases risk | Action within 30 days |
| **MEDIUM** | Moderate impact; optimization or compliance gap | Plan within 90 days |
| **LOW** | Minor improvement opportunity | Backlog |
| **Info** | Observation, best practice, or FYI | Documented |

## Privacy & Data Handling

- Assessment data classified per organization policy (public / internal / confidential / restricted).
- PII in findings must be redacted or anonymized in all deliverables.
- Reports stored only in approved repositories or encrypted shares.
- Credentials, secrets, and API keys must never appear in deliverables.
- Comply with GDPR, HIPAA, SOX, and local regulations where applicable.
- Data retention follows organization retention schedule; dispose per policy.

