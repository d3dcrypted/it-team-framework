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

Complete guide for the initial IT assessment interview. To be used in Phase 0 (Intake) with the company stakeholder (CTO, IT Manager, or business owner).

## How to Use

1. Start with the company profile (general questions)
2. Go through each domain in order
3. Note what is present, what is missing, and what is concerning
4. At the end, ask about "pain points" — they often reveal unstated priorities

---

## 1. Company Profile

```markdown
Required questions:
- [ ] Legal name / company name
- [ ] Industry / sector
- [ ] Total number of employees
- [ ] Number of IT users (anyone who uses a PC/work device)
- [ ] Number of locations (and where: domestic/abroad?)
- [ ] Annual revenue (optional, for budget context)
- [ ] Year founded
- [ ] Expected growth in the next 12 months (headcount, locations)
- [ ] Are there in-house IT staff? How many? What roles?
- [ ] Are there external IT consultants/vendors?
```

## 2. OS & Server Infrastructure

```markdown
Physical and virtual servers:
- [ ] Total number of servers (physical + virtual)?
- [ ] What hypervisor? (VMware/Hyper-V/Proxmox/KVM/Nutanix)
- [ ] Hypervisor versions?
- [ ] Windows Server: versions in use? (2008/2012/2016/2019/2022/2025)
- [ ] Linux: distributions? (Ubuntu/RHEL/Rocky/Debian)
- [ ] Containers? (Docker/K8s/Nomad)
- [ ] Average uptime? Frequent crashes?
- [ ] Patch management: automated or manual? (WSUS/SCCM/Automation)
- [ ] Server monitoring? (Nagios/Zabbix/PRTG/Datadog/none)
- [ ] Disaster recovery for servers? (HA? Clusters? Replication?)
- [ ] Storage: SAN/NAS/DAS? Brand? Capacity? Age?
```

## 3. Identity & Access

```markdown
Directory Services and Identity:
- [ ] On-prem Active Directory? Version? (2008/2012/2016/2019/2022)
- [ ] Azure AD / Entra ID? Sync in progress? (Azure AD Connect?)
- [ ] Other IdPs? (Okta/Keycloak/LDAP)
- [ ] MFA active? On which services? (admin? users? VPN?)
- [ ] SSO implemented? On what?
- [ ] Password policy: complexity? Rotation? Lockout?
- [ ] Admin accounts: separated from day-to-day user accounts?
- [ ] Onboarding/offboarding: documented process?
- [ ] Access audit logs? Retention?
```

## 4. Cloud

```markdown
Public and hybrid cloud:
- [ ] Cloud provider? (Azure/AWS/GCP/none)
- [ ] What runs in the cloud? (VMs? DBs? Apps? Storage?)
- [ ] Architecture: IaaS/PaaS/SaaS?
- [ ] Hybrid cloud? On-prem to cloud connection?
- [ ] Monthly cloud cost? Growing trend?
- [ ] Reserved instances / savings plans?
- [ ] Tagging strategy?
- [ ] Governance: policies, RBAC, blueprints?
- [ ] Cloud backup? Region replication?
- [ ] Security posture: NSG, WAF, Sentinel?
- [ ] Landing zone: structured or random resource groups?
```

## 5. Applications

```markdown
Enterprise applications:
- [ ] ERP? (SAP/Oracle/Dynamics/Zucchetti/Odoo)
- [ ] CRM? (Salesforce/Dynamics/HubSpot)
- [ ] Email/Collaboration: (Office 365/Google Workspace/on-prem)
- [ ] HR/Payroll: (Zucchetti/TeamSystem/ADP)
- [ ] Other business-critical applications?
- [ ] Custom applications? Technology? (.NET/PHP/Python/Java)
- [ ] Application integrations? (API/ETL/middleware)
- [ ] Application lifecycle: who maintains it? CI/CD?
- [ ] Software licenses: perpetual/subscription? Renewal date?
- [ ] Vendor health: support still active? End of life?
- [ ] Test environment? Separate dev/staging/prod?
```

## 6. Security

```markdown
Cybersecurity posture:
- [ ] Antivirus/EDR? (Kaspersky/Sophos/Defender/CrowdStrike/SentinelOne)
- [ ] Firewall: brand? Model? (Fortinet/PaloAlto/Sophos/CheckPoint)
- [ ] VPN solution? (WireGuard/OpenVPN/FortiClient/AnyConnect)
- [ ] SIEM? (Splunk/QRadar/Sentinel/Wazuh/none)
- [ ] Vulnerability management? (Tenable/Qualys/Nessus/none)
- [ ] Documented incident response plan?
- [ ] Backups: encrypted? Offline? 3-2-1?
- [ ] MFA: where is it active?
- [ ] GDPR compliance: DPO? ROPA? Data breach procedures?
- [ ] ISO 27001 / SOC2 / other certification?
- [ ] Security awareness training for users?
- [ ] Phishing simulation?
- [ ] Penetration test: last one? Frequency?
- [ ] Cyber insurance? Requirements?
```

## 7. Network

```markdown
Network infrastructure:
- [ ] LAN: switch brand/model? (Cisco/HPE/Aruba/MikroTik/Ubiquiti)
- [ ] WiFi: (Aruba/Ubiquiti/Meraki/Ruckus)
- [ ] VLAN segmentation?
- [ ] Firewall: perimeter? Internal segmentation?
- [ ] VPN: site-to-site? Remote access?
- [ ] SD-WAN? Provider?
- [ ] ISP: primary + backup? Bandwidth?
- [ ] DNS: internal resolver? External?
- [ ] DHCP: from AD? From firewall?
- [ ] Network monitoring? (PRTG/LibreNMS/Zabbix/SolarWinds)
- [ ] QoS managed?
- [ ] Load balancer? (HAProxy/F5/NGINX)
- [ ] Cabling: category? Age? Documented?
```

## 8. Backup & Disaster Recovery

```markdown
Data protection:
- [ ] Backup software? (Veeam/CommVault/NAKIVO/UrBackup)
- [ ] Backup storage: NAS? Tape? Cloud? (Wasabi/Backblaze/Azure)
- [ ] 3-2-1 rule followed? (3 copies, 2 media types, 1 off-site)
- [ ] Target RTO? Target RPO?
- [ ] Encrypted backups? Tested?
- [ ] Last successful restore test?
- [ ] Documented disaster recovery plan?
- [ ] DR site? (hot/warm/cold/cloud)
- [ ] DR testing: frequency? Last test?
- [ ] Backup of backups? (replication to secondary site)
- [ ] Documented retention policy?
- [ ] VM backups? Database backups? Fileshare? Microsoft 365/Google Workspace?
```

## 9. Endpoints

```markdown
Workstations and devices:
- [ ] Number of PCs/workstations? (Windows/macOS/Linux)
- [ ] Standard SOE? Unified image?
- [ ] Intune / MDM? (Intune/JAMF/Workspace ONE/MobileIron)
- [ ] Client patching: automatic or manual?
- [ ] Antivirus on endpoints?
- [ ] Mobile devices: how many? iOS/Android? MDM?
- [ ] BYOD policy?
- [ ] Printer fleet: how many? Brand? Managed?
- [ ] Hardware lifecycle: refresh every how many years?
- [ ] PC procurement: standardized? Vendor?
- [ ] Virtual Desktop? (AVD/Citrix/VMware Horizon)
- [ ] BitLocker/FileVault? Disk encryption?
- [ ] Acceptable use policy?
```

## 10. Service Desk & IT Service Management

```markdown
IT service delivery:
- [ ] Ticketing system? (ServiceNow/Jira/Zendesk/Freshservice/none)
- [ ] SLAs? (first response time? resolution time?)
- [ ] Number of tickets per month?
- [ ] Separate Incident / Problem / Change management?
- [ ] Knowledge base? How many articles?
- [ ] Self-service portal?
- [ ] Integrated asset management?
- [ ] Onboarding/offboarding: ticket + automation?
- [ ] CSAT (customer satisfaction) measured?
- [ ] ITIL processes: Incident/Problem/Change/Release/Asset?
- [ ] Change Advisory Board (CAB)?
- [ ] CMDB? (Configuration Management DB)
```

## 11. Budget & Procurement

```markdown
IT financial management:
- [ ] Annual IT budget? (total and by category)
- [ ] CAPEX vs OPEX ratio?
- [ ] Licensing: Microsoft (EA/CSP/Open)? Adobe? Oracle? VMware?
- [ ] Software Asset Management (SAM)?
- [ ] Main vendors? (Microsoft/Fastweb/TIM/Vodafone/Aruba)
- [ ] Contract renewal calendar?
- [ ] Procurement process: approvals? POs?
- [ ] Shadow IT: SaaS purchased without IT involvement?
- [ ] IT chargeback/showback to departments?
```

## 12. Closing Questions

```markdown
Always close with:
- [ ] What are the 3 most urgent IT problems?
- [ ] If you could change one thing, what would it be?
- [ ] Is there an IT project stuck for months/years?
- [ ] On average, how long does it take for a new hire to get everything working?
- [ ] The last major incident: what happened? How much did it impact the business?
- [ ] Is there something I did NOT ask that I should know?
```

## Scoring per Domain

After the interview, assign a maturity score for each domain:

| Score | Description |
|-------|-------------|
| **0–3** | Reactive — absent or working by chance. No processes, no documentation |
| **4–5** | Basic — informal processes, minimal documentation, untested backups |
| **6–7** | Defined — documented processes, basic monitoring, periodically tested backups |
| **8–9** | Managed — measured KPIs, automation, continuous improvement, metrics |
| **10** | Optimized — AI/automation, self-healing, predictive, continuous improvement |

Scoring template:

```markdown
| Domain        | Score | Notes |
|---------------|-------|-------|
| OS & Infra    | /10   |       |
| Cloud         | /10   |       |
| Applications  | /10   |       |
| Security      | /10   |       |
| Network       | /10   |       |
| Data/Backup   | /10   |       |
| Endpoints     | /10   |       |
| Service Desk  | /10   |       |
| Budget        | /10   |       |
| **Average**   | **/10** |     |
```
