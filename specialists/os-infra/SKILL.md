---
name: it-team-os-infra
description: 'Use when assessing or improving OS, server, virtualization, and identity infrastructure. Assessment protocol + improvement catalog for OS/AD/hypervisor.'
category: infrastructure
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [os, server, virtualization, active-directory, identity, patch-management]
    related_skills: [it-team-network, it-team-security, it-team-endpoints]
---

# OS & Infrastructure Specialist Skill (it-team-os-infra)

## Purpose
Use this skill to systematically assess, harden, and improve operating system, server, virtualization, and identity infrastructure across Windows Server, Linux, macOS, VMware/Hyper-V/Proxmox, and Active Directory environments.

## Assessment Protocol

### 1. Inventory & Baseline
- Collect asset inventory: hostnames, IPs, owners, criticality, data classification.
- Document OS type, version, architecture, and installed updates.
- Record uptime, last reboot time, and change windows.

## 2. Version & Patch Assessment
- Windows: Verify OS build and installed patches; check for missing CRITICAL/Security updates.
- Linux: Confirm distribution version and kernel; audit installed security patches.
- macOS: Confirm macOS version and updates; check for missing security patches.
- Virtualization: Document hypervisor version and build; review patch status and compatibility.

## 3. Uptime & Reliability
- Review uptime, event logs, and planned maintenance.
- Identify frequent reboots or instability indicators.

## 4. AD Health (Windows Active Directory)
- Domain and forest functional levels.
- Replication health and KCC connections; USN rollback checks.
- PDC/RID and FSMO role holders; SYSVOL and DFSR status.
- Domain controller time sync, certificate validity, LDAP over SSL/TLS.
- Deleted objects and tombstone considerations.

## 5. Virtualization Assessment
- VM counts, resource utilization, and sprawl review.
- VM templates, snapshots, and configuration baselines.
- Clustering, HA, DRS/motion, and backup integration status.
- Integration services / VM tools versions.

## 6. Identity & Access Hygiene
- On-premises and cloud identities sync status (Azure AD Connect).
- Conditional Access, MFA coverage, privileged admin roles.
- Service account review and password policies.
- Stale/non-compliant devices and orphaned permissions.

## 7. Security & Hardening Indicators
- Antivirus/EDR status and signatures.
- Firewall configuration and exposed management ports.
- SMB and legacy protocol usage; NTLM and NTLMv2 posture.
- TLS versions, weak ciphers, and certificate issues.

## 8. Reporting & Prioritization
- Produce an executive summary with health scores per domain.
- List findings by severity (CRITICAL/HIGH/MEDIUM/LOW) and effort.
- Define quick wins vs. longer initiatives.

## Improvement Catalog (Standard Improvements)

### A. OS Hardening
- Apply security baselines (CIS Benchmarks, STIGs) via GPO or configuration management.
- Remove/disable unnecessary services, protocols, and default accounts.
- Enforce SMBv3, disable SMBv1/SMBv2; restrict NTLM usage.
- Enable secure boot and, where applicable, virtualization-based security (VBS).
- Harden Remote Desktop: NLA, Gateway, session timeouts, allow only via Admin or bastion.
- Standardize anti-malware agents and tamper-protection; enable tamper-resistant logging.

### B. Patch Automation
- Windows: WSUS/WSUS offline or Microsoft Update for Business; patch SLAs and testing windows.
- Linux: Use native update management (apt/yum/dnf) or Ansible/SCCM; schedule security-only vs full updates.
- macOS: Use DEP/AME/Apple Business/School Manager; test updates with staged rollout.
- Hypervisor: Firmware/BIOS updates; hypervisor patches in maintenance windows; test compatibility with VM tools.

### C. Virtualization Consolidation & Optimization
- Right-size VMs: CPU, memory, disk, and network; remove unused snapshots.
- Enable deduplication/compression where workload-appropriate; plan for performance impact.
- Implement VM tagging, naming standards, and role-based access control.
- Migrate to clusters with HA/DRS; enable vMotion, DPM, and storage DRS.
- Evaluate licensing and cost optimization (reserved instances, hybrid benefits).

### D. Active Directory Modernization (Azure AD Integration)
- Extend on-prem AD to Azure AD via Azure AD Connect; enable password hash sync or passthrough.
- Implement Conditional Access, device compliance, and MFA for hybrid joined devices.
- Move identities toward cloud-managed models (Azure AD joined + hybrid Azure AD joined).
- Enable Azure AD Privileged Identity Management (PIM) and role-based access.
- Modernize group-based management: use Azure AD groups, dynamic membership, and entitlement management.

### E. Identity & Access Governance
- Implement tiered admin model and Just-In-Time (JIT) access.
- Remove excessive local admin rights; deploy LAPS or alternative password rotation.
- Enforce MFA for all admins and privileged service accounts.
- Regular access reviews for groups, applications, and impersonation rights.

### F. Backup, DR, & Operations
- Validate VM and AD backups with restore testing; define RPO/RTO.
- Implement VM/host monitoring and alerting (CPU, memory, storage latency).
- Define maintenance windows and change control for infrastructure updates.

## Implementation Guide (Safe Execution)

### 1. Planning & Change Management
- Document expected changes, scope, owners, and rollback plan.
- Define maintenance windows and communication to stakeholders.
- Use a pilot group or non-critical system to validate changes.

### 2. Pre-Change Validation
- Capture baseline performance, configurations, and AD health states.
- Ensure backups, snapshots, and VM configurations are current.
- Verify update management connectivity and patch test results.

### 3. Execution Pattern
- Start with low-risk hosts; progress to critical after validation.
- Apply one change category at a time (e.g., patches, then hardening, then AD changes).
- Use configuration management (e.g., Ansible, DSC, Group Policy) for consistency.
- Log and capture outputs; treat idempotency and rollbacks as first-class concerns.

### 4. AD-Specific Safeguards
- Ensure FSMO role holders are known and operations master is healthy before schema changes.
- Test AD replication and DNS resolution before and after changes.
- Stage schema/forest/domain prep only when required; validate prerequisites thoroughly.

### 5. Virtualization Safeguards
- Apply hypervisor patches in clustered environments with rolling maintenance.
- Ensure VM tools/integration services are updated in a controlled manner.
- Verify VM compatibility and shared storage paths before migrations.

### 6. Identity Safeguards
- Run Azure AD Connect health checks; monitor sync errors.
- Stage Conditional Access policies with report-only mode before enforcement.
- Keep break-glass/admin accounts accessible and protected during transitions.

### 7. Post-Change Verification
- Run the assessment protocol again; compare against baseline.
- Verify patch levels, uptime stability, AD replication, and VM health.
- Update documentation and CMDB entries accordingly.

## Quick Commands & Checks (Examples)
- Windows patch inventory: `Get-HotFix | Sort-Object InstalledOn`
- AD domain/forest level: `Get-ADDomain | Select-Object DomainMode,ForestMode`
- AD replication: `repadmin /replsummary`
- Hypervisor version (ESXi): `esxcli system version get`
- VM tools status (VMware): `vmware-toolbox-cmd version status`
- Azure AD Connect health: `Get-ADSyncHealth` (module) or portal overview
- CPU/memory summary (Linux): `lscpu && free -h`

## Notes
- Keep this skill updated with your environment’s specific baselines, tooling, and regulatory requirements.
- Use configuration management and IaC to codify improvements and ensure repeatability.
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


