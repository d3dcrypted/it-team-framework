---
name: it-team-observability
description: 'Use when assessing or improving monitoring, logging, alerting, and SLOs. Metrics/logs/traces coverage + alert quality + dashboards + on-call + capacity trends.'
category: operations
version: 0.3.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [observability, monitoring, logging, alerting, slo, prometheus, grafana, zabbix, siem-adjacent, capacity]
    related_skills: [it-team-os-infra, it-team-network, it-team-security, it-team-service-desk, it-team-devops-platform]
---

# Observability Specialist — Monitoring / SRE-adjacent Engineer

Domain: `Observability` (canonical name). Covers infrastructure and application monitoring, log management, alerting, dashboards, SLOs, and capacity trends. Security-specific detection (SIEM content, threat rules) stays with `it-team-security`; this domain provides the telemetry plumbing both rely on.

## Assessment Protocol

### 1. Coverage Inventory
- What is monitored today? Servers, VMs, network devices, storage, applications, certificates, backup jobs, cloud resources.
- Blind spots: anything business-critical with NO monitoring (common: certificate expiry, backup success, disk trends on app servers, SaaS status).
- Agent vs agentless mix; monitoring of the monitoring (who watches the NMS?).

### 2. Metrics Stack
- Tooling: Prometheus/Grafana, Zabbix, PRTG, CheckMK, SolarWinds, cloud-native (Azure Monitor/CloudWatch)?
- Retention and resolution: enough history for capacity planning (≥13 months ideal)?
- Standardization: one stack or tool sprawl per team?

### 3. Log Management
- Central log platform: ELK/OpenSearch, Loki, Graylog, Splunk, Sentinel? Or logs live only on hosts?
- Coverage: OS logs, application logs, network/firewall, authentication events.
- Retention policy: defined per source? Compliance-driven minimums (auth logs often 6-12 months)?
- Cost control: noisy sources filtered at ingestion?

### 4. Alerting Quality
- Alert inventory: how many rules, how many fire per week, how many are acted on?
- Noise ratio: alerts acknowledged-without-action / total (target <30%).
- Actionability: every alert has severity, owner, and a linked runbook?
- Delivery: email-only (weak) vs on-call rotation with escalation (Telegram/Teams/PagerDuty-class)?
- Quiet hours / maintenance windows honored?

### 5. Dashboards & Reporting
- Per-audience dashboards: NOC/ops (real-time), management (KPI/SLA), capacity (trends).
- Are dashboards actually used? Stale dashboards = findings.
- Monthly service report generated from data (not hand-made)?

### 6. SLOs & Service Levels
- Are availability/latency targets defined per service? Measured or aspirational?
- Error budgets or at least uptime tracking with agreed measurement points.
- SLA reporting to business/customers backed by real measurements.

### 7. Synthetic & End-User Monitoring
- Synthetic checks for key user journeys (login, ERP transaction, website checkout).
- External vantage point (is the site up FROM OUTSIDE?).

### 8. Incident Feedback Loop
- MTTD/MTTR measured from data? Post-incident: are missing alerts added?
- Integration with Service Desk: alerts open tickets automatically where sensible.

## Improvement Catalog

- **Single metrics stack**: consolidate to one platform (e.g., Prometheus+Grafana or Zabbix); decommission overlap.
- **Log centralization with retention tiers**: hot (30d) / warm (6-12m) / archive; filter noise at source.
- **Alert hygiene sprint**: delete dead rules, add severity+owner+runbook link to the rest; route by severity.
- **Certificate/backup/job watchdogs**: cheap checks that prevent the most embarrassing outages. Quick win.
- **SLO definition for top 5 services**: measured availability with agreed measurement method.
- **Synthetic checks** for the 3 most business-critical user journeys.
- **Capacity trend reviews**: monthly review of disk/CPU/RAM growth; forecast before procurement panics.

## KPIs

| KPI | Target |
|---|---|
| Coverage of critical assets | 100% |
| MTTD for P1 incidents | < 5 min (alert-driven, not user-reported) |
| % incidents detected by monitoring vs users | ≥70% monitoring |
| Alert noise ratio | < 30% |
| Alerts with runbook link | 100% |
| Log sources centralized (critical systems) | 100% |

## Common Pitfalls

1. Monitoring everything except what pages someone at 3am — coverage ≠ alerting.
2. Alert rules copied from defaults, never tuned: 500 alerts/day trains everyone to ignore them.
3. Logs centralized without retention policy: storage bill grows until someone deletes evidence.
4. Dashboards as decoration: if no decision is made from it, delete it.
5. SLA promised to business without a measurement method — unprovable and undisprovable.

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), assessment report JSON schema, canonical domain names, execution states, and evidence rules. Do not redefine those here; if any local text conflicts with the orchestrator contract, the orchestrator contract wins.
