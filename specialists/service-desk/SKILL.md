---
name: it-team-service-desk
description: "Use when assessing service desk: ITIL, SLA, ticketing."
category: service-desk
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [service-desk, ITIL, ticketing, SLA, knowledge-base, training, onboarding-offboarding, IT-asset-management, self-service-portal, incident-problem-change]
    related_skills: [it-team-endpoints, it-team-applications]
---

# Service Desk & Support — IT Specialist (it-team-service-desk)

This skill provides a structured protocol for assessing, improving, and operating an IT service desk aligned with ITIL standards, with ticketing integration (ServiceNow, Jira, Zendesk, Freshservice), SLA/SLO management, knowledge base, training, onboarding/offboarding, IT asset management, and self-service.

## Skill Objectives

- Assess the maturity of the service desk and ITIL processes.
- Measure critical KPIs: ticket volume, SLA adherence, First Response Time (FRT), Time to Resolution (TTR), CSAT, knowledge base coverage.
- Define and track improvements across ticketing, knowledge base, SLA, automations, and training.
- Support integration with ticketing and asset management tools.

## Assessment Protocol

Perform a complete assessment using the following checkpoints. Use tools of your choice (ticketing API, reports, interviews, surveys).

### 1. Ticket Volume & Trends
- Extract daily/weekly/monthly volume and trends.
- Analysis by category, priority, channel (email, web, phone, chat).
- Seasonal peaks, anomalous growth or declines.

### 2. SLA / SLO Adherence
- Percentage of tickets meeting SLA by category/priority.
- SLA breach rate and root cause of delays.
- Alignment with SLO targets (e.g., resolution within 24/48/72 hours).

### 3. First Response Time (FRT)
- Average and distribution of time before first response.
- Comparison against targets (e.g., <2 hours for critical/high, <24 hours for medium/low).

### 4. Time to Resolution (TTR)
- Average and distribution of closure time.
- TTR by category/known problem.

### 5. CSAT (Customer Satisfaction)
- Average post-interaction survey scores.
- Distribution across very satisfied, satisfied, neutral, dissatisfied, very dissatisfied.
- Free text comments for recurring themes.

### 6. Knowledge Base Coverage
- Percentage of tickets with linked/inserted KB articles.
- Total article count, usage frequency (search hits), self-service rate.
- Quality: accuracy, currency, coverage of frequent topics.

### 7. ITIL Process Maturity
- Maturity assessment (0–3 or 0–5) for: Incident, Problem, Change, Service Request, Release.
- Documentation, roles, responsibilities, workflows, registers (RFC, Problem, Known Error).

### 8. Onboarding / Offboarding Workflow
- Average time to provision/revoke access, accounts, licenses.
- Checklist completeness (hardware, software, email, SSO, permissions).
- User experience and employee feedback.

### 9. IT Asset Management
- Inventory accuracy (hardware/software/licenses).
- Lifecycle, maintenance, disposal.
- Alignment with licensing and compliance policies.

## Improvement Catalog

Prioritize based on Assessment results. Possible interventions:

### 1. ITIL Process Implementation
- Clearly define processes: intake, classification, assignment, SLA, escalation, closure.
- Implement registers and RACI.
- Establish cadences (daily triage, weekly SLA review).

### 2. Knowledge Base Creation & Optimization
- Categorical structure, article templates, content ownership.
- Ticketing integration: KB suggestion at creation time.
- Governance: periodic review, versioning, KPIs (usage rate, self-service).

### 3. Self-Service Portal
- Self-service catalog, request forms, ticket status.
- Integrated access to knowledge, FAQs, forms.
- Measure adoption rate and agent workload reduction.

### 4. SLA / SLO Tuning
- Define realistic targets for each category/priority.
- Automated escalation on SLA breach.
- Real-time SLA adherence dashboard.

### 5. Chatbot Integration
- Bot for FAQ, initial triage, KB search, ticket creation.
- Clear fallback to human agent.
- Measure reduced FRT, bot resolution rate, satisfaction.

### 6. Automated Onboarding / Offboarding
- Forms, HRIS/Active Directory/SSO integration.
- Approval workflows, checklists, notifications.
- Measure time-to-productivity and completeness.

### 7. Training Program
- Training paths: ITIL basics, ticketing tools, KB authoring, soft skills.
- New hire training, periodic refresh, certifications.
- Pre/post-training competency assessment.

### 8. IT Asset Management Enhancements
- Discovery automation, CMDB integration, license monitoring.
- Reorder policy, secure disposal, compliance reporting.

## Implementation Guide

### Phase 1: Discovery and Baseline (2–4 weeks)
- Run the Assessment Protocol on all checkpoints.
- Define baseline KPIs and targets.
- Engage stakeholders: Helpdesk, IT, HR, Security, Vendors.

### Phase 2: Design and Planning (2–3 weeks)
- Prioritize improvements with RICE/WSJF.
- Define roadmap, MVP, milestones, and owners.
- Estimate resources, budget, timelines.

### Phase 3: Implementation (4–12 weeks depending on scope)
- Configure/optimize ticketing (fields, SLA, workflows, automations).
- Create/modify KB and implement ticket integration.
- Launch self-service portal and/or chatbot in limited scope.
- Enable automated onboarding/offboarding with HRIS/AD.
- Launch training programs.

### Phase 4: Testing, Pilot, Measurement
- Pilot with a small group, collect feedback.
- Monitor KPIs: SLA adherence, FRT, TTR, CSAT, KB usage, time-to-prod.
- Learn and iterate.

### Phase 5: Roll-out and Governance
- Gradual or full roll-out based on results.
- Define Governance: KB owners, SLA review, ticket management, change control.
- Dashboards and periodic reports.

### Phase 6: Maintenance and Maturity
- Quarterly ITIL audits and process reviews.
- KB and self-service evolution.
- Continuous SLO/SLA optimization based on load and needs.

## Recommended Tools & Integrations

- Ticketing: ServiceNow, Jira Service Management, Zendesk, Freshservice.
- Knowledge Base: integrated ticketing solution or dedicated KB (e.g., Confluence).
- SSO & Access: Azure AD, Okta, Google Workspace.
- Asset Management: ServiceNow CMDB, Lansweeper, Snipe-IT.
- Self-service/Portal: integrated or custom solution.
- Chatbot: Native solutions (Zendesk Answer Bot, Freshservice Freddy) or LLM-built bot with guardrails.
- Analytics/BI: Power BI, Tableau, Looker or native ticketing reports.

## Reference KPIs (indicative targets)

- SLA adherence ≥95% (critical SLAs), ≥98% (high/low SLAs).
- FRT <2 hours (critical), <24 hours (high), <48 hours (medium/low).
- TTR <48 hours (critical), <72 hours (high), <120 hours (medium/low) — adjust per category.
- CSAT ≥85% satisfied/very satisfied.
- KB coverage ≥70% tickets with linked KB; self-service usage rate ≥30%.
- Onboarding provisioned ≤3 days; offboarding revocations within 24 hours of request.

## Notes & Best Practices

- Align SLA with business needs; avoid unrealistic targets that cause dissatisfaction.
- Keep KB simple, searchable, up-to-date; assign ownership.
- Continuously monitor volume and breach trends for proactive intervention.
- Involve end users in testing and feedback.
- Document processes and responsibilities (RACI) and communicate them clearly.

## Example Roadmap (M3)

- Week 1–2: Assessment and KPI baseline.
- Week 3–4: KB design and SLA tuning.
- Week 5–8: Advanced ticketing implementation, KB management, first chatbot pilot.
- Week 9–12: Self-service portal roll-out, onboarding automation, training program.
- Week 13+: Governance, continuous monitoring, iterative improvements.

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
