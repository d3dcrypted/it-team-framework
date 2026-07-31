---
name: it-team-security
description: 'Use when assessing or improving cybersecurity posture. Security assessment + compliance (GDPR/ISO27001) + threat detection + incident response.'
category: security
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [security, compliance, GDPR, ISO27001, NIST-CSF, SIEM, SOAR, zero-trust, vulnerability-management]
    related_skills: [it-team-network, it-team-os-infra, it-team-data]
---

# Specialista Sicurezza — CISO / Security Engineer

Dominio: cybersecurity, compliance (GDPR, ISO 27001, NIST CSF), threat detection, incident response, vulnerability management, identity protection, security monitoring (SIEM/SOAR), security awareness.

## Assessment Protocol

### Cosa Controllare

**Policies e Governance**
- Policy di sicurezza documentate?
- Data breach procedure documentata?
- Incident response plan (IRP) aggiornato?
- Business continuity plan (BCP)?
- DPO nominato? (obbligatorio GDPR)
- Registro trattamenti dati (ROPA) aggiornato?
- Certificazioni: ISO 27001? SOC2? Cyber Essentials?

**Technical Controls**
- Antivirus/EDR: marca? Copertura 100%? (Defender/CrowdStrike/SentinelOne)
- Firewall: perimetrale e interno? (Fortinet/PaloAlto/Sophos)
- MFA: attivo su admin? Utenti? VPN? Cloud?
- Patch management: timeframe? (critical: 48h? monthly?)
- Vulnerability scanning: frequenza? Strumento? (Tenable/Qualys/Nessus)
- Penetration test: ultimo? Frequenza? Risultati?
- Backup encryption: at-rest? In-transit? Testati?

**Identity Protection**
- MFA adoption rate (admin: utenti %)
- Conditional Access / Zero-trust policies?
- Privileged Identity Management (PIM)?
- Just-In-Time access?
- Service account management?
- Passwordless adoption?

**Monitoring & Detection**
- SIEM: presente? (Splunk/Sentinel/Wazuh/QRadar)
- SOAR: automation playbook?
- Log retention period?
- Threat intelligence feed?
- UEBA / User behavior analytics?
- Incident detection: tempo medio (MTTD)?

**Security Awareness**
- Training periodico per utenti?
- Phishing simulation?
- Policy di sicurezza accettazione utente?
- Reporting channel per incidenti?

### Metriche Chiave

| Metrica | Target | Come Misurare |
|---------|--------|---------------|
| MFA adoption | 100% admin, > 80% users | MFA report |
| Patch critical | < 48h | Patch compliance report |
| Vulnerability fix | > 95% critical in 30gg | Vulnerability scanner |
| Backup test pass | 100% | Backup report |
| Phishing click rate | < 5% | Phishing simulation report |
| MTTD (time to detect) | < 24h | SIEM dashboard |
| MTTR (time to resolve) | < 4h critical | Incident log |

## Improvement Catalog

### Quick Wins (<= 2 settimane)

| # | AZIONE | IMPATTO | SFORZO | PRIORITA |
|---|--------|---------|--------|----------|
| 1 | Enable MFA on ALL admin accounts | CRITICAL | 2h | 1 |
| 2 | Run vulnerability scan full environment | HIGH | 4h | 2 |
| 3 | Enable backup encryption if not active | HIGH | 2h | 2 |
| 4 | Verify backup restore with test file | HIGH | 2h | 3 |
| 5 | Cleanup inactive users/disabling old accounts | HIGH | 4h | 1 |
| 6 | Set up basic log retention & alerting | HIGH | 8h | 2 |
| 7 | Create/update incident response contact list | HIGH | 2h | 1 |
| 8 | Enable Conditional Access basic policies | HIGH | 4h | 2 |

### Migliorie Strategiche (1-6 mesi)

**1. Incident Response Plan**
Crea/aggiorna IRP con fasi: Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned.
Include: playbook per ransomware, data breach, DDoS, account compromise.
Effort: 2-3 settimane

**2. SIEM Deployment (Wazuh/FOSS)**
Wazuh gratuito (FOSS). Copre: log collection, file integrity, vulnerability detection, alerts.
Architettura: Wazuh server + agents su tutti i server.
Costo: €0 software, solo infrastruttura server.
Effort: 3-4 settimane

**3. Vulnerability Management Program**
Processo continuo: scan settimanale, remediation entro SLA, reporting mensile.
Fase 1: scan con Nessus/OpenVAS (gratuito).
Fase 2: remediation workflow.
Fase 3: reporting al management.
Effort: 2-3 settimane iniziali, continuo poi

**4. Zero-Trust Architecture**
Principi: verify explicitly, least privilege, assume breach.
Azioni:
- Network segmentation (micro-segmentation)
- MFA everywhere
- Conditional Access policies
- Just-In-Time access per admin
- Device compliance check (Intune)
Effort: 4-8 settimane

**5. Security Awareness Program**
Training base per tutti gli utenti + phishing simulation trimestrale.
Strumenti gratuiti: GoPhish (phishing simulation) + LMS open source (es. Moodle).
Effort: 2 settimane setup, continuo

**6. GDPR Compliance Project**
Se azienda tratta dati di cittadini UE:
- DPO nomination (se > 250 dipendenti o dati sensibili)
- ROPA (Registro Trattamenti)
- Data breach procedure
- Data retention & deletion policy
- DPIA (Data Protection Impact Assessment) per nuovi trattamenti
Effort: 4-6 settimane (dipende da compliance attuale)

## Implementation Guide

### Zero-Trust Implementation

```
1. Identity pillar
   - MFA su tutti gli account
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

### Tool Gratuiti Raccomandati

| Strumento | Uso | Licenza |
|-----------|-----|---------|
| Wazuh | SIEM/XDR | Open source (AGPL) |
| OpenVAS / Greenbone | Vulnerability scanner | Open source (GPL) |
| GoPhish | Phishing simulation | Open source (MIT) |
| Velociraptor | DFIR / endpoint visibility | Open source (AGPL) |
| Shuffle | SOAR / automation | Open source (GPL) |
| Security Onion | SOC platform | Open source (GPL) |
| CrowdSec | IPS/CTI community-based | Open source (MIT) |

### Errori Comuni

1. **MFA solo parziale** - attivarlo solo sugli admin e dimenticare servizi critici (VPN, cloud, email). MFA su tutto.
2. **Patch solo quando esplode** - vulnerability window lasciata aperta. Patch critical entro 48h.
3. **Backup non testati** - il backup esiste ma il restore non funziona. Test mensile obbligatorio.
4. **Security awareness ignorata** - l'anello piu debole resta l'utente. Training + phishing simulation.
5. **Log senza retention** - log accesi ma retention 7gg. Minimo 90gg, 1 anno per compliance.
6. **IR plan inesistente** - quando succede, si improvvisa. Playbook da scrivere prima.
7. **Password manager non usato** - password copiate sticky note. Bitwarden/KeePass obbligatorio.
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

