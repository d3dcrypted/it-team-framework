---
name: it-team-assessment-guide
description: Use when conducting the initial IT department assessment interview. Structured questions for all 9 domains to build a complete AS-IS picture.
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [it-team, assessment, interview, intake]
    related_skills: [it-team-orchestrator]
---

# Assessment Interview Guide

Guida completa per l'intervista iniziale di assessment IT. Da usare nella Fase 0 (Intake) con il referente aziendale (CTO, IT Manager, o imprenditore).

## Come Usare

1. Parti dal profilo azienda (domande generali)
2. Scendi dominio per dominio
3. Segna cosa è presente, mancante, e cosa preoccupa
4. Alla fine, chiedi i "dolori" — spesso svelano priorità non dette

---

## 1. Profilo Azienda

```markdown
Domande obbligatorie:
- [ ] Ragione sociale / nome azienda
- [ ] Settore merceologico
- [ ] Numero dipendenti totali
- [ ] Numero utenti IT (chi usa un PC/work device)
- [ ] Numero sedi (e dove: Italia/estero?)
- [ ] Fatturato annuo (opzionale, per contesto budget)
- [ ] Anno di fondazione
- [ ] Crescita prevista nei prossimi 12 mesi (organico, sedi)
- [ ] Ci sono figure IT interne? Quante? Quali ruoli?
- [ ] Ci sono consulenti/fornitori IT esterni?
```

## 2. OS & Infrastruttura Server

```markdown
Server fisici e virtuali:
- [ ] Quanti server totali (fisici + virtuali)?
- [ ] Che hypervisor? (VMware/Hyper-V/Proxmox/KVM/Nutanix)
- [ ] Versioni hypervisor?
- [ ] Windows Server: versioni in uso? (2008/2012/2016/2019/2022/2025)
- [ ] Linux: distribuzioni? (Ubuntu/RHEL/Rocky/Debian)
- [ ] Container? (Docker/K8s/Nomad)
- [ ] Quanto uptime medio? Ci sono crash frequenti?
- [ ] Patch management: automatizzato o manuale? (WSUS/SCCM/Automation)
- [ ] Monitoring server? (Nagios/Zabbix/PRTG/Datadog/nessuno)
- [ ] Disaster recovery per i server? (HA? Cluster? Replication?)
- [ ] Storage: SAN/NAS/DAS? Marca? Capacità? Età?
```

## 3. Identità e Accessi

```markdown
Directory Services e Identity:
- [ ] Active Directory on-prem? Versione? (2008/2012/2016/2019/2022)
- [ ] Azure AD / Entra ID? Sync in corso? (Azure AD Connect?)
- [ ] Altri IdP? (Okta/Keycloak/LDAP)
- [ ] MFA attivo? Su quali servizi? (admin? utenti? VPN?)
- [ ] SSO implementato? Su cosa?
- [ ] Policy password: complessità? Rotation? Lockout?
- [ ] Account amministratori: separati dagli user day-to-day?
- [ ] Onboarding/offboarding: processo documentato?
- [ ] Audit log degli accessi? Retention?
```

## 4. Cloud

```markdown
Cloud pubblico e ibrido:
- [ ] Provider cloud? (Azure/AWS/GCP/nessuno)
- [ ] Cosa gira in cloud? (VM? DB? App? Storage?)
- [ ] Architettura: IaaS/PaaS/SaaS?
- [ ] Hybrid cloud? Connessione on-prem-cloud?
- [ ] Costo cloud mensile? Trend in crescita?
- [ ] Reserved instances / savings plans?
- [ ] Tagging strategy?
- [ ] Governance: policy, RBAC, blueprints?
- [ ] Backup in cloud? Region replication?
- [ ] Security posture: NSG, WAF, Sentinel?
- [ ] Landing zone: strutturata o resource group a caso?
```

## 5. Applicativi

```markdown
Enterprise applications:
- [ ] ERP? (SAP/Oracle/Dynamics/Zucchetti/Odoo)
- [ ] CRM? (Salesforce/Dynamics/HubSpot)
- [ ] Email/Collab: (Office 365/Google Workspace/on-prem)
- [ ] HR/Payroll: (Zucchetti/TeamSystem/ADP)
- [ ] Altri applicativi business-critical?
- [ ] Custom applications? Tecnologia? (.NET/PHP/Python/Java)
- [ ] Integrazioni tra applicativi? (API/ETL/middleware)
- [ ] Application lifecycle: chi mantiene? CI/CD?
- [ ] Licenze applicative: perpetue/subscription? Renewal date?
- [ ] Vendor health: support still active? End of life?
- [ ] Test environment? Dev/staging/prod separati?
```

## 6. Sicurezza

```markdown
Cybersecurity posture:
- [ ] Antivirus/EDR? (Kaspersky/Sophos/Defender/CrowdStrike/SentinelOne)
- [ ] Firewall: marca? Modello? (Fortinet/PaloAlto/Sophos/CheckPoint)
- [ ] VPN solution? (WireGuard/OpenVPN/FortiClient/AnyConnect)
- [ ] SIEM? (Splunk/QRadar/Sentinel/Wazuh/nessuno)
- [ ] Vulnerability management? (Tenable/Qualys/Nessus/nessuno)
- [ ] Incident response plan documentato?
- [ ] Backup: encrypted? Offline? 3-2-1?
- [ ] MFA: dove è attivo?
- [ ] GDPR compliance: DPO? ROPA? Data breach procedure?
- [ ] ISO 27001 / SOC2 / altra certificazione?
- [ ] Security awareness training per utenti?
- [ ] Phishing simulation?
- [ ] Penetration test: ultimo? Frequenza?
- [ ] Cyber insurance? Requisiti?
```

## 7. Rete

```markdown
Network infrastructure:
- [ ] LAN: switch marca/modello? (Cisco/HPE/Aruba/MikroTik/Ubiquiti)
- [ ] WiFi: (Aruba/Ubiquiti/Meraki/Ruckus)
- [ ] VLAN segmentazione?
- [ ] Firewall: perimetrale? Internal segmentation?
- [ ] VPN: site-to-site? Remote access?
- [ ] SD-WAN? Provider?
- [ ] ISP: principale + backup? Banda?
- [ ] DNS: internal resolver? External?
- [ ] DHCP: da AD? Da firewall?
- [ ] Network monitoring? (PRTG/LibreNMS/Zabbix/SolarWinds)
- [ ] QoS gestito?
- [ ] Load balancer? (HAProxy/F5/NGINX)
- [ ] Cablaggio: categoria? Età? Documentato?
```

## 8. Backup e Disaster Recovery

```markdown
Data protection:
- [ ] Backup software? (Veeam/CommVault/NAKIVO/UrBackup)
- [ ] Storage backup: NAS? Tape? Cloud? (Wasabi/Backblaze/Azure)
- [ ] 3-2-1 rule rispettata? (3 copie, 2 media, 1 off-site)
- [ ] RTO obiettivo? RPO obiettivo?
- [ ] Backup crittografati? Testati?
- [ ] Ultimo test di restore con successo?
- [ ] Disaster recovery plan documentato?
- [ ] Sito DR? (caldo/freddo/cloud)
- [ ] DR test: frequenza? Ultimo test?
- [ ] Backup dei backup? (replication to second site)
- [ ] Retention policy documentata?
- [ ] Backup delle VM? Database? Fileshare? 365/Google Workspace?
```

## 9. Endpoint

```markdown
Workstation e dispositivi:
- [ ] Quanti PC/workstation? (Windows/macOS/Linux)
- [ ] SOE standard? Immagine unificata?
- [ ] Intune / MDM? (Intune/JAMF/Workspace ONE/MobileIron)
- [ ] Patch client: automatico o manuale?
- [ ] Antivirus su endpoint?
- [ ] Mobile devices: quanti? iOS/Android? MDM?
- [ ] BYOD policy?
- [ ] Printer fleet: quante? Marca? Gestite?
- [ ] Hardware lifecycle: refresh ogni quanti anni?
- [ ] Procurement PC: standardizzato? Fornitore?
- [ ] Virtual Desktop? (AVD/Citrix/VMware Horizon)
- [ ] BitLocker/FileVault? Disk encryption?
- [ ] Policy di utilizzo accettabile?
```

## 10. Service Desk & IT Service Management

```markdown
IT service delivery:
- [ ] Ticketing system? (ServiceNow/Jira/Zendesk/Freshservice/nessuno)
- [ ] SLA? (tempo primo response? resolution?)
- [ ] Quanti ticket/mese?
- [ ] Incident / Problem / Change management separati?
- [ ] Knowledge base? Quanti articoli?
- [ ] Self-service portal?
- [ ] Asset management integrato?
- [ ] Onboarding/offboarding: ticket + automation?
- [ ] CSAT (customer satisfaction) misurato?
- [ ] ITIL processes: Incident/Problem/Change/Release/Asset?
- [ ] Change Advisory Board (CAB)?
- [ ] CMDB? (Configuration Management DB)
```

## 11. Budget e Procurement

```markdown
IT financial management:
- [ ] Budget IT annuo? (totale e per categoria)
- [ ] CAPEX vs OPEX ratio?
- [ ] Licensing: Microsoft (EA/CSP/Open)? Adobe? Oracle? VMware?
- [ ] Software Asset Management (SAM)?
- [ ] Vendor principali? (Microsoft/Fastweb/TIM/Vodafone/Aruba)
- [ ] Contract renewal calendar?
- [ ] Procurement process: approvazioni? PO?
- [ ] Shadow IT: SaaS acquistati senza IT?
- [ ] IT chargeback/showback ai dipartimenti?
```

## 12. Domande Finali

```markdown
Sempre chiudere con:
- [ ] Quali sono i 3 problemi IT più urgenti?
- [ ] Se potessi cambiare una cosa sola, quale sarebbe?
- [ ] C'è un progetto IT bloccato da mesi/anni?
- [ ] Quanto tempo impiega in media un nuovo assunto ad avere tutto funzionante?
- [ ] L'ultimo incidente grave: cosa è successo? Quanto ha impattato?
- [ ] C'è qualcosa che NON ti ho chiesto che dovrei sapere?
```

## Scoring per Dominio

Dopo l'intervista, assegna un punteggio di maturità per ogni dominio:

| Punteggio | Descrizione |
|-----------|-------------|
| **0-3** | Reattivo — assente o funziona per caso. Nessun processo, nessuna documentazione |
| **4-5** | Base — processi informali, documentazione minima, backup non testati |
| **6-7** | Definito — processi documentati, monitoring base, backup testati periodicamente |
| **8-9** | Gestito — KPI misurati, automazione, miglioramento continuo, metriche |
| **10** | Ottimizzato — AI/automation, self-healing, predictive, continuous improvement |

Template punteggio:

```markdown
| Dominio | Punteggio | Note |
|---------|-----------|------|
| OS & Infra | /10 | |
| Cloud | /10 | |
| App | /10 | |
| Security | /10 | |
| Network | /10 | |
| Data/Backup | /10 | |
| Endpoint | /10 | |
| Service Desk | /10 | |
| Budget | /10 | |
| **Media** | **/10** | |
```