---
name: it-team-ai-automation
description: 'Use when assessing or introducing AI adoption and process automation. Automation inventory + AI/LLM use cases + shadow AI + data readiness + AI governance (EU AI Act) + ROI-ranked automation backlog.'
category: innovation
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ai, llm, automation, rpa, n8n, power-automate, copilot, ai-act, governance, llmops, rag]
    related_skills: [it-team-applications, it-team-data, it-team-security, it-team-budget, it-team-devops-platform]
---

# AI & Automation Specialist — AI Adoption / Automation Engineer

Domain: `AI & Automation` (canonical name). Covers process automation (RPA, workflow engines), AI/LLM adoption (copilots, chatbots, RAG), AI governance and compliance (EU AI Act, GDPR overlap), and data readiness for AI. Model serving infrastructure detail belongs to `it-team-devops-platform`; data quality foundations to `it-team-data`.

## Assessment Protocol

### 1. Automation Inventory
- What is automated today? Scripts, scheduled tasks, RPA bots, workflow tools (n8n, Power Automate, Zapier, Logic Apps).
- Ownership and documentation: who maintains each automation? Bus factor.
- Failure handling: do automations fail silently?

### 2. Automation Candidates
- Identify high-volume, rule-based, low-exception processes (invoice entry, onboarding steps, report generation, ticket routing).
- Score each: frequency × time per run × error rate × people involved = ROI rank.
- Distinguish: eliminate (process is waste) > automate > assist (AI copilot).

### 3. AI Usage & Shadow AI
- Sanctioned AI tools in use (Copilot, ChatGPT Enterprise, internal chatbots)?
- Shadow AI: employees pasting company data into free consumer AI tools — assume yes until proven otherwise. Check DNS/proxy logs if available.
- Existing AI spend and license utilization (paid seats actually used?).

### 4. AI Use Cases
- Rank candidate use cases: internal knowledge Q&A (RAG over docs/wiki), support ticket drafting, meeting summaries, document extraction (invoices, contracts), code assistance, customer-facing chatbots (higher risk).
- For each: data sensitivity, human-in-the-loop requirement, measurable success criteria.

### 5. Data Readiness
- Is the knowledge needed by AI accessible, current, and permission-aware (SharePoint/wiki/file shares)?
- Document quality: duplicated/stale content poisons RAG. Coordinate with it-team-data.
- Access control mapping: AI must not answer from documents the asking user cannot read.

### 6. AI Governance & Compliance
- AI usage policy: exists, communicated, enforced? (What data may go to which tool.)
- EU AI Act exposure: classify use cases (prohibited / high-risk / limited / minimal). HR screening and biometric use cases = high-risk, need extra controls.
- GDPR: DPIA for AI processing personal data; data residency of AI providers; retention of prompts/outputs.
- Vendor terms: is customer data used for training? Zero-data-retention options.
- Output accountability: human review requirements for consequential decisions.

### 7. Skills & Change Management
- Team AI literacy; champions per department; training plan.
- Fear/resistance mapping — automation lands better framed as toil removal.

## Improvement Catalog

- **AI usage policy + sanctioned tool** (quick win): a short published policy plus one approved tool kills most shadow AI.
- **ROI-ranked automation backlog**: top 10 processes with effort/saving estimates; execute top 3.
- **Internal RAG assistant** over policies/runbooks/wiki — highest-value low-risk LLM use case for most orgs.
- **Document extraction pipeline** for invoices/orders (structured output, human validation queue).
- **Copilot pilot with DLP guardrails**: measure before/after on a defined team, then decide rollout.
- **LLM gateway** for API usage: one entry point with logging, cost attribution, rate limits, model routing (cost/observability leverage; pairs with it-team-devops-platform).
- **Automation runbook standard**: every bot/flow gets owner, alerting, and failure procedure.

## KPIs

| KPI | Target |
|---|---|
| Hours saved / month by automation | measured, growing; report quarterly |
| Top-10 backlog processes automated | ≥3 in first 6 months |
| Shadow AI incidents after policy | trending to 0 |
| AI use cases with completed risk classification | 100% |
| Automations with owner + failure alerting | 100% |
| AI license seat utilization | ≥70% or reduce seats |

## Common Pitfalls

1. Starting with a customer-facing chatbot — highest risk, hardest use case. Start internal.
2. Automating a broken process: automate AFTER simplification, or you get faster garbage.
3. RAG over a stale, duplicated document base — answers confidently wrong. Fix sources first.
4. AI policy that only forbids: without a sanctioned alternative, shadow AI grows.
5. Counting "time saved" nobody can verify — define the measurement before building.
6. Ignoring per-query cost at scale: pilot economics ≠ production economics; cap and monitor.

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), assessment report JSON schema, canonical domain names, execution states, and evidence rules. Do not redefine those here; if any local text conflicts with the orchestrator contract, the orchestrator contract wins.
