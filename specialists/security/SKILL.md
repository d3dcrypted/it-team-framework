---
name: it-team-security
description: 'Use when assessing or improving cybersecurity posture. Security assessment + compliance (GDPR/ISO27001) + threat detection + incident response.'
category: security
version: 0.2.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [security, compliance, GDPR, ISO27001, NIST-CSF, SIEM, SOAR, zero-trust, vulnerability-management]
    related_skills: [it-team-network, it-team-os-infra, it-team-data]
---

# Security Specialist — CISO / Security Engineer

Domain: cybersecurity, compliance (GDPR, ISO 27001, NIST CSF), threat detection, incident response, vulnerability management, identity protection, security monitoring (SIEM/SOAR), security awareness.

## Assessment Protocol

### What to Check

**Policies and Governance**
- Security policies documented?
- Data breach procedure documented?
- Incident response plan (IRP) updated?
- Business continuity plan (BCP)?
- DPO appointed? (mandatory under GDPR)
- Records of Processing Activities (ROPA) updated?
- Certifications: ISO 27001? SOC2? Cyber Essentials?

**Technical Controls**
- Antivirus/EDR: brand? 100% coverage? (Defender/CrowdStrike/SentinelOne)
- Firewall: perimeter and internal? (Fortinet/PaloAlto/Sophos)
- MFA: enabled on admin? Users? VPN? Cloud?
- Patch management: timeframe? (critical: 48h? monthly?)
- Vulnerability scanning: frequency? Tool? (Tenable/Qualys/Nessus)
- Penetration test: last conducted? Frequency? Results?
- Backup encryption: at-rest? In-transit? Tested?

**Identity Protection**
- MFA adoption rate (admin / user %)
- Conditional Access / Zero-trust policies?
- Privileged Identity Management (PIM)?
- Just-In-Time access?
- Service account management?
- Passwordless adoption?

**Monitoring & Detection**
- SIEM: present? (Splunk/Sentinel/Wazuh/QRadar)
- SOAR: automation playbook?
- Log retention period?
- Threat intelligence feed?
- UEBA / User behavior analytics?
- Incident detection: mean time to detect (MTTD)?

**Security Awareness**
- Periodic user training?
- Phishing simulation?
- User security policy acceptance?
- Incident reporting channel?

### Key Metrics

| Metric | Target | How to Measure |
|---------|--------|---------------|
| MFA adoption | 100% admin, > 80% users | MFA report |
| Patch critical | < 48h | Patch compliance report |
| Vulnerability fix | > 95% critical in 30 days | Vulnerability scanner |
| Backup test pass | 100% | Backup report |
| Phishing click rate | < 5% | Phishing simulation report |
| MTTD (time to detect) | < 24h | SIEM dashboard |
| MTTR (time to resolve) | < 4h critical | Incident log |

## Improvement Catalog

### Quick Wins (<= 2 weeks)

| # | ACTION | IMPACT | EFFORT | PRIORITY |
|---|--------|---------|--------|----------|
| 1 | Enable MFA on ALL admin accounts | CRITICAL | 2h | 1 |
| 2 | Run full environment vulnerability scan | HIGH | 4h | 2 |
| 3 | Enable backup encryption if not active | HIGH | 2h | 2 |
| 4 | Verify backup restore with test file | HIGH | 2h | 3 |
| 5 | Cleanup inactive users/disable old accounts | HIGH | 4h | 1 |
| 6 | Set up basic log retention & alerting | HIGH | 8h | 2 |
| 7 | Create/update incident response contact list | HIGH | 2h | 1 |
| 8 | Enable Conditional Access basic policies | HIGH | 4h | 2 |

### Strategic Improvements (1-6 months)

**1. Incident Response Plan**
Create/update IRP with phases: Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned.
Include: playbooks for ransomware, data breach, DDoS, account compromise.
Effort: 2-3 weeks

**2. SIEM Deployment (Wazuh/FOSS)**
Wazuh is free (FOSS). Covers: log collection, file integrity, vulnerability detection, alerts.
Architecture: Wazuh server + agents on all servers.
Cost: €0 software, server infrastructure only.
Effort: 3-4 weeks

**3. Vulnerability Management Program**
Continuous process: weekly scans, remediation within SLA, monthly reporting.
Phase 1: scan with Nessus/OpenVAS (free).
Phase 2: remediation workflow.
Phase 3: management reporting.
Effort: 2-3 initial weeks, then ongoing

**4. Zero-Trust Architecture**
Principles: verify explicitly, least privilege, assume breach.
Actions:
- Network segmentation (micro-segmentation)
- MFA everywhere
- Conditional Access policies
- Just-In-Time access for admins
- Device compliance check (Intune)
Effort: 4-8 weeks

**5. Security Awareness Program**
Basic training for all users + quarterly phishing simulation.
Free tools: GoPhish (phishing simulation) + open-source LMS (e.g., Moodle).
Effort: 2 weeks setup, then ongoing

**6. GDPR Compliance Project**
If the company processes EU citizens' data:
- DPO appointment (if > 250 employees or sensitive data)
- ROPA (Records of Processing Activities)
- Data breach procedure
- Data retention & deletion policy
- DPIA (Data Protection Impact Assessment) for new processing activities
Effort: 4-6 weeks (depends on current compliance state)

## Implementation Guide

### Zero-Trust Implementation

```
1. Identity pillar
   - MFA on all accounts
   - Conditional Access policies (block legacy auth, location-based)
   - PIM for admin roles
   - Passwordless (Windows Hello / Authenticator)

2. Device pillar
   - Intune enrollment 100%
   - Compliance policies (encryption, OS version, antivirus)
   - Device-based Conditional Access

3. Network pillar
   - Micro-segmentation VLANs
   - Just-in-time network access
   - Network traffic encryption (TLS 1.2+)

4. Data pillar
   - Data classification (internal/confidential/public)
   - DLP policies
   - Information protection labeling

5. Monitoring
   - SIEM correlation rules
   - User behavior analytics
   - Automated response (SOAR playbook)
```

### Recommended Free Tools

| Tool | Use | License |
|-----------|-----|---------|
| Wazuh | SIEM/XDR | Open source (AGPL) |
| OpenVAS / Greenbone | Vulnerability scanner | Open source (GPL) |
| GoPhish | Phishing simulation | Open source (MIT) |
| Velociraptor | DFIR / endpoint visibility | Open source (AGPL) |
| Shuffle | SOAR / automation | Open source (GPL) |
| Security Onion | SOC platform | Open source (GPL) |
| CrowdSec | IPS/CTI community-based | Open source (MIT) |

### Common Errors

1. **Partial MFA** — enabling it only on admins and forgetting critical services (VPN, cloud, email). MFA everywhere.
2. **Patching only when things break** — vulnerability window left open. Critical patches within 48h.
3. **Untested backups** — backup exists but restore doesn't work. Monthly restore testing mandatory.
4. **Ignored security awareness** — the weakest link remains the user. Training + phishing simulation.
5. **Logs without retention** — logs enabled but 7-day retention. Minimum 90 days, 1 year for compliance.
6. **Non-existent IR plan** — when it happens, improvisation. Playbook must be written beforehand.
7. **Password manager not used** — passwords copied to sticky notes. Bitwarden/KeePass mandatory.
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


## Privacy & Data Handling

- Assessment data classified per organization policy (public / internal / confidential / restricted).
- PII in findings must be redacted or anonymized in all deliverables.
- Reports stored only in approved repositories or encrypted shares.
- Credentials, secrets, and API keys must never appear in deliverables.
- Comply with GDPR, HIPAA, SOX, and local regulations where applicable.
- Data retention follows organization retention schedule; dispose per policy.

