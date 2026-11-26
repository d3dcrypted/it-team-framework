---
name: it-team-applications
description: 'Use when assessing or improving enterprise applications portfolio. App rationalization + integration patterns + lifecycle management.'
category: applications
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [applications, saas, api-integration, rationalization, vendor-health, code-quality, microservices]
    related_skills: [it-team-cloud, it-team-service-desk, it-team-budget]
---

# Applications Specialist — Application Manager (it-team-applications)

# Assessment Protocol

## 1. Application Inventory
- **Name and description**: unique identifier, business owner, context ( production / pre-production / development ).
- **Type**: CRM, ERP, SaaS, custom application, integration layer, internal tooling.
- **Status**: in production, under maintenance, deprecated, candidate for removal.
- **Flow map**: primary use cases and business processes supported.
- **Documentation**: where manuals, runbooks, API docs, architecture diagrams are stored.

## 2. Versions
- **Current version**: version number or tag (e.g. 2024.1.0).
- **Version history**: upgrade timeline, release notes for each major/minor.
- **Component ecosystem**: libraries, frameworks, containers, database driver versions.
- **Versioning policies**: semantic versioning, date-based, internal numbering.
- **Alignment**: critical versions aligned across environments (dev / test / prod).

## 3. Licenses
- **Licensing model**: perpetual, subscription, consumptive, core-based, user-based.
- **Licensed entities**: number of cores, sockets, users, devices.
- **Expirations and renewals**: expiration dates, reminders, renewal / purchase process.
- **Compliance**: quota checks, periodic audits, vendor reporting.
- **Emergency handling**: procedures for urgent upgrades or load changes.

## 4. Integrations
- **Endpoints and contacts**: API URLs, webhooks, SFTP, messaging ( Kafka / RabbitMQ ), service bus.
- **Protocols and formats**: REST / GraphQL / SOAP, JSON / XML / gRPC, payload size limits.
- **Authentication and authorization**: API keys, OAuth2 / OIDC, mTLS, certificates, managed secrets.
- **SLA and QoS**: response times, rate limits, retry policy, timeout, backoff.
- **Error handling**: error codes, fallback patterns, dead-letter queue, exception logging.
- **Integrated monitoring**: traffic metrics, errors, latencies, queue sizes.

## 5. Vendor Health
- **Vendor status**: financial health, roadmap, mergers/acquisitions, strategic announcements.
- **Support and services**: TAM availability, response times, contractual SLAs.
- **Community and ecosystem**: forums, events, partner network, certifications.
- **Risks**: single-source dependency, lock-in, service outages, privacy policies.
- **Contingency plans**: exit strategy, off-vendor migration, data escrow.

## 6. Custom Code Quality
- **Architecture**: clean architecture, separation of concerns, clear layers (domain / application / infrastructure).
- **Code quality**: linting, formatting, static analysis, cyclomatic complexity, code smells.
- **Tests**: unit test coverage, integration tests, end-to-end tests, load tests, test data strategy.
- **Build & CI/CD**: release pipelines, automation, gating, approvals, rollback.
- **Security**: SAST / DAST, secret management, dependency scanning, threat modeling.
- **Performance**: benchmarking, profiling, expected loads, scalability plan.

---

# Improvement Catalog

## 1. Application Rationalization
- **Eliminate redundancies**: overlapping applications with similar functionality.
- **Consolidation**: migrate workloads to a single platform.
- **Safe decommissioning**: data archival, user communication, cutover procedure.
- **KPIs**: number of applications reduced, percentage of workload migrated, annual savings.

## 2. API-First Integration
- **API design**: clear contract, versioning, OpenAPI/Swagger documentation.
- **API gateway**: rate limiting, authentication, monitoring, caching management.
- **Integration patterns**: façade, anti-corruption layer, async messaging, event sourcing.
- **Tools**: schema validation, contract testing, mock server for development.

## 3. SaaS Consolidation
- **Total cost of ownership evaluation**: license, custom development, support, training.
- **User experience unification**: SSO access, consistent user experience.
- **Data residency and compliance**: region verification, certifications (SOC 2, ISO 27001).
- **Migration plan**: data, configurations, training, communication.

## 4. Upgrade Planning
- **Roadmap**: target versions, milestones, risks and dependencies.
- **Backwards compatibility**: evaluate impacts on custom code and integrations.
- **Pilot execution**: pilot group, rollback plan, go/no-go checklist.
- **Communication**: stakeholder agenda, training, updated documentation.

## 5. Microservices Assessment
- **Domain model**: bounded context, DDD, decomposition by business capability.
- **Granularity**: small, autonomous services vs. fractured monolith.
- **Data management**: database per service, potential CQRS / Event Sourcing patterns.
- **OSS and tooling**: orchestrator (Kubernetes), service mesh, observability management.

---

# Implementation Guide

## Phase 0 — Preparation
- **Stakeholders**: business owner, IT, security, compliance, finance.
- **Objectives**: define scope, success criteria, KPIs, timeline.
- **Tools**: shared inventory (spreadsheet / CMDB), issue tracker, documentation wiki.

## Phase 1 — Discovery and Inventory
- Conduct interviews with primary users and owners.
- Extract lists from CMDB, license agreements, CI/CD configurations.
- Validate current state with application owners.

## Phase 2 — Evaluation and Prioritization
- Apply a scoring model (e.g., cost + risk + business value).
- Classify as: keep, optimize, consolidate, replace, decommission.
- Define improvement backlog with clear priorities.

## Phase 3 — Improvement Design
- Choose integration patterns and target architecture.
- Define success metrics and acceptance criteria.
- Create detailed plans for each initiative (timeline, resources, budget).

## Phase 4 — Execution and Migration
- Pilot on a limited environment, continuous monitoring.
- Execute cutover with well-defined rollback.
- Update documentation and train users.

## Phase 5 — Operations and Continuous Optimization
- Post-migration monitoring: SLA, errors, performance.
- Periodic portfolio review (every 6-12 months).
- Iterate with incremental improvements and technical debt reduction.

---

# Notes and Best Practices
- Maintain a single source of truth for the inventory (CMDB / cloud asset inventory).
- Use versioned API contracts and compatibility tests.
- Always evaluate vendor risk and have a contingency plan.
- Promote a quality culture: code review, automated testing, CI/CD.
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

- Involve end users in every phase of change and success validation.
