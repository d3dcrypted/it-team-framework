---
name: it-team-devops-platform
description: Use when assessing CI/CD, IaC, containers, DORA metrics.
category: engineering
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [devops, cicd, iac, terraform, ansible, kubernetes, docker, gitops, dora, platform-engineering]
    related_skills: [it-team-cloud, it-team-os-infra, it-team-security, it-team-observability, it-team-ai-automation]
---

# DevOps & Platform Specialist — Platform Engineer / DevOps Lead

Domain: `DevOps & Platform` (canonical name). Covers source control, CI/CD, infrastructure as code, container platforms, environment management, release processes, and developer experience. Relevant when the organization builds or heavily customizes software; for pure-COTS shops, scope shrinks to IaC + pipeline hygiene for IT automation itself.

## Assessment Protocol

### 1. Source Control & Branching
- SCM platform (GitHub/GitLab/Azure DevOps/Bitbucket); anything NOT in version control (scripts on servers, firewall configs, GPOs)?
- Branching model, protected branches, mandatory reviews, signed commits for sensitive repos.

### 2. CI Pipelines
- Build automation coverage: % of actively developed repos with CI.
- Pipeline speed (target <10 min for main pipelines) and flakiness.
- Quality gates: tests, linting, SAST/dependency scanning (coordinate with it-team-security).

### 3. CD & Releases
- Deployment method: manual/scripted/pipeline/GitOps. Who can deploy to prod, and is it audited?
- Environments: dev/test/prod parity; config drift between them.
- Rollback: proven procedure, tested recently? Blue-green/canary where it matters.
- Release cadence vs business need.

### 4. Infrastructure as Code
- IaC coverage: % of infrastructure reproducible from code (Terraform/Bicep/Ansible).
- State management, module reuse, drift detection.
- Click-ops ratio: changes made in portals outside IaC = drift findings.

### 5. Container Platform
- Docker/Kubernetes/managed (AKS/EKS) usage; cluster versions, upgrade path.
- Registry hygiene: image scanning, tag immutability, provenance.
- Resource limits, namespace isolation, ingress and cert management.

### 6. Secrets in Delivery
- Secrets in pipelines: vault-integrated (good) vs pipeline variables (acceptable) vs in-repo (CRITICAL).
- Rotation, scoping, and audit of CI/CD credentials; runner/agent security.

### 7. DORA Metrics
- Deployment frequency, lead time for changes, change failure rate, MTTR — measured or estimable?
- Even rough numbers anchor the improvement roadmap.

### 8. Developer Experience
- Onboarding time to first commit/deploy; golden paths / templates for new services.
- Local dev environment reproducibility; docs freshness; toil inventory.

## Improvement Catalog

- **Everything into git** (quick win): server scripts, IaC, network/firewall configs export, GPO backups — versioned and reviewable.
- **Pipeline template standardization**: one blessed CI template with tests + scanning; new repos start compliant.
- **IaC adoption path**: new infra only via code; import top legacy resources opportunistically; enable drift detection.
- **GitOps for K8s** (where K8s exists): declared state, auditable changes, easy rollback.
- **Secrets remediation**: sweep repos/pipelines for embedded secrets; move to vault; rotate everything found.
- **DORA baseline dashboard**: measure the four metrics from pipeline data (pairs with it-team-observability).
- **Golden path for new services**: template repo + pipeline + deploy target; onboarding in hours, not weeks.

## KPIs

| KPI | Target |
|---|---|
| Actively developed repos with CI | 100% |
| IaC coverage of production infra | ≥70% and rising |
| Secrets found in repos/pipelines | 0 (post-remediation) |
| Deployment lead time | < 1 day for standard changes |
| Change failure rate | < 15% |
| Prod deploys with tested rollback | 100% |

## Common Pitfalls

1. Kubernetes because it's fashionable: a compose stack or managed PaaS beats an unmanaged cluster nobody can operate.
2. IaC that only creates but never manages: drift makes the code a lie within months.
3. CI without failing tests — a green pipeline that proves nothing.
4. Deploy rights as tribal privilege: undocumented, unaudited, single point of failure.
5. Platform team building what developers don't ask for — golden paths win by being easier, not mandatory.

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), assessment report JSON schema, canonical domain names, execution states, and evidence rules. Do not redefine those here; if any local text conflicts with the orchestrator contract, the orchestrator contract wins.
