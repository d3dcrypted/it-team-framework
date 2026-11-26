---
name: it-team-data
description: 'Use when assessing or improving data infrastructure. Storage + backup/DR (3-2-1) + data governance + analytics.'
category: data-infrastructure
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [storage, backup, disaster-recovery, data-governance, analytics, ransomware, 3-2-1]
    related_skills: [it-team-cloud, it-team-security, it-team-os-infra]
---

# Data & Backup Specialist (it-team-data)

## Overview
Specialist agent for data infrastructure assessment and improvement, covering storage systems (SAN/NAS/Object), backup strategies, disaster recovery, business continuity, data governance, and analytics/data warehouse pipelines.

## Assessment Protocol

### 1. Storage Capacity & Tiering
- **Current capacity**: Total storage, used/free space across all systems
- **Growth trends**: Monthly/quarterly growth rates
- **Tiering analysis**: Hot/warm/cold data distribution
- **Performance tiers**: Match storage to workload requirements
- **Thin provisioning**: Evaluate allocation efficiency

### 2. Backup Success Rate
- **Success metrics**: Backup completion rates, failure patterns
- **Duration trends**: Backup window adherence
- **Data coverage**: Percentage of critical systems backed up
- **Integrity checks**: Backup validation and checksum verification
- **Monitoring**: Alerting on backup failures

### 3. RTO/RPO Current State
- **Recovery Time Objectives**: Actual vs. target RTO per system
- **Recovery Point Objectives**: Actual vs. target RPO per system
- **Measurement methodology**: Test-based verification
- **Gap analysis**: Identify systems needing improvement

### 4. DR Test History
- **Test frequency**: Regular vs. ad-hoc testing
- **Test types**: Full failover, partial, tabletop exercises
- **Results documentation**: Lessons learned and improvements
- **Recovery verification**: Data consistency and application functionality
- **Stakeholder participation**: IT, business, management involvement

### 5. Data Retention Policies
- **Policy compliance**: Adherence to legal, regulatory, business requirements
- **Retention periods**: Match to business value and regulations
- **Exception handling**: Special cases and overrides
- **Automated enforcement**: Policy-driven lifecycle management
- **Audit trail**: Track retention-related activities

### 6. Archival Strategy
- **Archive tiers**: Cost-optimized long-term storage
- **Retrievability**: RTO/RPO for archived data
- **Compliance**: Legal hold and regulatory requirements
- **Migration strategy**: Move to/from archive
- **Cost management**: Archive storage spend optimization

### 7. Data Classification
- **Sensitivity levels**: Public, internal, confidential, restricted
- **Business value**: CRITICAL, important, peripheral
- **Retention mapping**: Different retention by classification
- **Access controls**: RBAC based on classification
- **Lifecycle stages**: Creation → active → archive → delete

## Improvement Catalog

### 1. 3-2-1 Backup Hardening
- **3 copies**: Production + 2 backup copies
- **2 different media**: Disk and tape/cloud
- **1 offsite**: Geographic separation
- **Immutable backups**: WORM storage for ransomware protection
- **Air-gapped copies**: Offline/immutable backup vaults

### 2. DR Automation
- **Automated failover**: Scripted recovery procedures
- **Infrastructure as Code**: DR environment provisioning
- **Playbook automation**: Runbook execution automation
- **Monitoring integration**: Automated health checks
- **Testing automation**: Regular, scheduled DR tests

### 3. Storage Tiering Optimization
- **Data placement strategy**: Automated based on access patterns
- **Cost optimization**: Balance performance vs. cost
- **Migration policies**: Automated tier movement
- **Performance monitoring**: Track IOPS, latency, throughput
- **Capacity planning**: Predictive growth analysis

### 4. Ransomware-Proof Backup
- **Immutable storage**: Prevent deletion/modification
- **Multi-factor authentication**: Backup system access
- **Zero-trust architecture**: Least privilege access
- **Air-gapped copies**: Offline backup vaults
- **Rapid detection**: Anomaly detection in backup systems

### 5. Data Lifecycle Automation
- **Automated classification**: ML-based sensitivity analysis
- **Policy-driven movement**: Automated tiering and archiving
- **Retention enforcement**: Automatic deletion at policy expiry
- **Orchestration tools**: Workflow automation platforms
- **Integration with applications**: Native lifecycle management

### 6. Analytics/Data Warehouse Pipeline
- **Data ingestion**: Real-time vs. batch processing
- **ETL/ELT processes**: Data transformation and loading
- **Data quality**: Validation and cleansing procedures
- **Metadata management**: Data catalog and lineage
- **Performance optimization**: Query acceleration strategies

## Implementation Guide

### Phase 1: Assessment (Weeks 1-2)
1. Inventory all storage systems and capacities
2. Document current backup configurations and success rates
3. Measure current RTO/RPO through testing
4. Review DR test history and effectiveness
5. Audit data retention policy compliance
6. Classify data according to business value and sensitivity

### Phase 2: Gap Analysis (Week 3)
1. Compare current state vs. 3-2-1 requirements
2. Identify DR automation opportunities
3. Analyze storage tiering optimization potential
4. Assess ransomware protection gaps
5. Review data lifecycle automation needs

### Phase 3: Quick Wins (Weeks 4-6)
1. Implement backup monitoring and alerting
2. Optimize storage tiering for high-value data
3. Enhance data classification processes
4. Automate retention policy enforcement
5. Improve backup validation procedures

### Phase 4: Strategic Improvements (Weeks 7-12)
1. Implement DR automation and playbooks
2. Deploy immutable/air-gapped backups
3. Build analytics/data warehouse pipelines
4. Implement data lifecycle automation
5. Create comprehensive DR testing program

### Phase 5: Optimization (Ongoing)
1. Continuous monitoring and optimization
2. Cost optimization initiatives
3. Performance tuning
4. Regular DR testing and validation
5. Policy review and updates

## Key Metrics & KPIs
- **Backup success rate**: Target >99%
- **RTO compliance**: Percentage of systems meeting RTO targets
- **RPO compliance**: Percentage of systems meeting RPO targets
- **Storage cost per GB**: Overall and by tier
- **Data classification accuracy**: Percentage correctly classified
- **DR test frequency**: Number of tests per period
- **Policy compliance rate**: Adherence to retention and archival policies

## Tools & Technologies
- **Backup solutions**: Veeam, Commvault, Rubrik, Cohesity
- **Storage platforms**: Pure Storage, Dell PowerStore, NetApp, object storage
- **DR orchestration**: VMware SRM, Azure Site Recovery, custom scripts
- **Data classification**: Microsoft Purview, IBM Guardium, BigID
- **Analytics platforms**: Snowflake, Redshift, BigQuery, Databricks
- **Monitoring**: Prometheus, Grafana, CloudWatch, Splunk

## Best Practices
- Regular DR testing (at least quarterly)
- Immutable backups for critical systems
- Automated monitoring and alerting
- Data classification as foundation for all policies
- Cost optimization through right-tiering
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

- Documentation of all procedures and runbooks