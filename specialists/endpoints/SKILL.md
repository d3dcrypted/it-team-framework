---
name: it-team-endpoints
description: 'Use when assessing or improving endpoint and device management. Workstation/mobile MDM + SOE + hardware lifecycle + VDI.'
category: endpoints
version: 0.3.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [endpoints, MDM, SOE, hardware-lifecycle, VDI, BYOD, patch-management, printers]
    related_skills: [it-team-os-infra, it-team-service-desk, it-team-security]
---

# Endpoint & Devices Specialist — it-team-endpoints

Use this skill when you need to assess, design, or improve endpoint and device management for workstations, mobile devices, printers, and virtual desktops. Covers MDM strategy, SOE standardization, hardware lifecycle, BYOD policy, and VDI assessment.

## When to use
- Assessing current endpoint posture and compliance
- Designing or refining SOE and patch management
- Planning MDM rollout (Intune / JAMF / Workspace ONE)
- Optimizing printer fleet and imaging/OSD processes
- Evaluating hardware refresh needs and lifecycle
- Assessing VDI (AVD / Citrix) feasibility and pilot planning
- Defining BYOD and mobile device policies

## Assessment protocol
Perform a structured assessment across the following domains. For each item, record current state, gaps, risk level, and recommended actions.

### 1) SOE standardization
- Verify existence and version of SOE documentation for Windows, macOS, and Linux.
- Compare installed software list against approved application catalog.
- Check image build process (manual vs automated) and reproducibility.
- Validate adherence to naming, domain-join, and local-admin standards.
- Gap examples: inconsistent apps, manual builds, missing drivers.

### 2) Patch compliance
- Collect patch status across endpoints (OS, runtime, drivers, firmware).
- Measure time-to-patch for critical/security updates across OS families.
- Review patch exceptions and rework rate.
- Check update bandwidth optimization (WSUS/Intune/ccmcache).

### 3) MDM coverage
- Inventory endpoints per platform (Windows: Intune; macOS: Intune/JAMF; iOS/Android: Intune/Workspace ONE).
- Calculate coverage ratio (managed devices / total eligible devices).
- Verify compliance policies, conditional access, and app protection policies.
- Check enrollment experience and user adoption friction.

MDM feature checklist (HIGH priority):
- Device and app compliance policies
- Conditional access / compliance state for VPN/EOE
- App protection / containerization
- Remote wipe/lock and retire
- Role-based admin and alerts

### 4) Device inventory
- Central CMDB/asset DB with owner, location, serial, model, SOE version.
- Warranty and support expiration tracking.
- Hardware lifecycle stage (in-warranty, EOL-proximate, deprecated).
- Integration with ITSM for change and incident context.

### 5) Printer fleet
- Inventory make/model/firmware and location.
- Driver consolidation and universal driver strategy.
- Print server/osd health and redundancy.
- Security: secure printing, TLS, network segmentation.
- Cost per print and duplex defaults.

### 6) Hardware age / replacement cycle
- Average device age by role and department.
- Failure rates and RMA trends.
- Establish replacement cadence (e.g., 3–5 years) and exceptions.
- Budget forecast and end-of-life vendor planning.

### 7) OS version fragmentation
- Distribution of OS versions and build numbers.
- CRITICAL/end-of-life versions flagged.
- Compatibility matrix for line-of-business apps.
- Target state: limited, documented set of supported builds.

### 8) Antivirus / endpoint protection
- Coverage ratio and real-time protection status.
- EDR/XDR presence and alerting integration (SIEM).
- Tampering protection and scheduled scan results.
- Ensure definitions and engine versions are current.

### 9) BYOD policy adoption
- Enrolled devices ratio and policy exceptions.
- Containerization / app protection effectiveness.
- Personal vs corporate data segregation and wipe boundaries.
- User onboarding/offboarding experience.

### 10) Virtual Desktop (AVD / Citrix)
- Broker health, host utilization, licensing.
- Personal vs pooled assignments and profile management.
- FSLogix/ADMX optimization and performance baseline.
- Network, gateway, and client compatibility checks.

### 11) Physical & environmental
- UPS coverage for critical workstations/print devices.
- Dust/fan/noise indicators and cleaning cadence.
- Secure disposal and decommission workflow.

### 12) Security & identity
- Device posture checks (disk encryption, EDR, OS updates).
- MFA for admin consoles and remote management.
- Least-privilege local admin model (LAPS/ Azure AD/Intune).

## Improvement catalog
Proposed improvements (ordered by impact and effort):

1) SOE standardisation with Intune / Microsoft Deployment Toolkit
   - Create and validate Windows images in a shared pipeline.
   - Standardize applications, drivers, and settings via OMA-URI/PowerShell.
   - Automate image versioning and release notes.

2) Autopilot for Windows & Apple Business/School Manager
   - Reduce touch for new devices and consistent initial setup.
   - Integrate with HRIS/asset workflow for owner pre-staging.

3) Printer consolidation and universal drivers
   - Migrate to modern print servers and secure pull-print.
   - Reduce driver sprawl and simplify firmware management.

4) Mobile Device Policy (MDM + MAM)
   - Enroll all corporate and BYOD devices into Intune/Workspace ONE.
   - Apply app protection, compliance, and conditional access.

5) Hardware refresh plan & lifecycle governance
   - Define role-based replacement windows (e.g., 3-year laptops, 4-year desktops).
   - Stage buy/lease options and disposal partners.

6) VDI assessment (pilot for knowledge workers)
   - Profile performance, licensing, and user experience.
   - Optimize FSLogix/UEFS and app layering.

7) Patch automation and bandwidth optimization
   - WSUS/Intune ring strategies, maintenance windows, feature updates.
   - Driver update cadence and vendor engagement.

8) Antivirus/EDR consolidation
   - Move to platform-native or single EDR to reduce conflicts.
   - Tune alerts and integrate with SIEM.

9) BYOD enablement with containerization
   - Implement app protection and selective wipe.
   - Streamline enrollment and user self-service.

10) Print cost governance and sustainability
   - Set duplex default, pull-print, and disposal/recycling program.

11) CMDB + ITSM integration
   - Enforce unique identifiers, ownership, and lifecycle states.
   - Link incidents, changes, and deployments to devices.

12) Continuous compliance & reporting
   - Dashboards for MDM coverage, patch SLA, OS fragmentation, AV health.
   - Monthly exception reviews and remediation plans.

## Implementation guide

### Step 0: Prepare
- Define scope (platforms, locations, user groups).
- Assign owners for data collection and remediation.
- Establish OKRs and success metrics (e.g., 95% MDM coverage, <7-day patch SLA).

### Step 1: Baseline
- Run inventory and collect data per Assessment protocol.
- Produce a gap register with risk ratings.
- Agree on target state and timeline.

### Step 2: Quick wins (0–4 weeks)
- Enroll corporate devices into MDM; apply basic compliance & app protection.
- Harden printers (firmware, secure print, network zones).
- Disable legacy protocols and enforce encryption where needed.
- Standardize AV/EDR and patch critical vulnerabilities.

### Step 3: SOE & imaging (4–12 weeks)
- Build and validate a reference image per platform.
- Automate image capture/deployment and driver catalog.
- Migrate pilot departments; capture feedback and iterate.
- Promote standardized apps and settings via Intune/configuration profiles.

autopilot note: If supported by hardware/HP/DEP/Apple DEP, enable Autopilot for zero-touch enrollment and consistent initial experience.

### Step 4: Patch & update management (ongoing)
- Define ring strategy for Intune/WSUS; pilot → steady state.
- Set maintenance windows and rollback plans.
- Automate driver updates and monitor compatibility.

### Step 5: Printer consolidation & security (2–6 weeks)
- Catalog printers; retire or relocate low-volume devices.
- Standardize on universal drivers and pull-print.
- Segment print VLAN and enforce TLS/Hardening.

### Step 6: MDM coverage & mobile policy (4–12 weeks)
- Onboard corporate and BYOD into Intune/Workspace ONE.
- Apply device/jailbreak detection, app protection, conditional access.
- Configure self-service portals and clear user communication.

### Step 7: VDI pilot (6–12 weeks, optional)
- Select pilot user group and baseline performance.
- Configure broker, hosts, licensing, profile/FSLogix.
- Validate apps, peripherals, and user experience; adjust at scale.

### Step 8: Hardware refresh & lifecycle (rolling)
- Create role-based device profiles and replacement plan.
- Engage vendors for buy/lease and EOL disposal.
- Track age/failure and budget quarterly.

### Step 9: Governance & continuous improvement
- Publish runbooks, ownership, and escalation paths.
- Build dashboards for MDM coverage, patch SLA, OS versions, AV health.
- Review exceptions monthly; iterate on SOE and policies.

### Step 10: Skills & change management
- Train IT staff on image pipelines, MDM, and printer workflows.
- Communicate changes to users; provide self-service guides.

## Key metrics / SLAs (examples)
- MDM coverage: ≥95% corporate-managed devices
- Patch SLA: CRITICAL ≤7 days, HIGH ≤30 days
- OS fragmentation: ≤3 actively supported builds
- Printer cost per print: target reduction X%
- VDI pilot success: ≥90% user satisfaction in pilot

## Troubleshooting tips
- Image deployment failures: validate drivers, network boot (PXE/UEFI), and image integrity.
- MDM enrollment errors: check DNS, APNs/Intune enrollment limits, and compliance policies.
- Printer discovery issues: confirm mDNS/LLTD, driver compatibility, and print server health.
- Patch conflicts: stage updates in rings; hold problematic updates and create remediations.
- VDI performance: baseline CPU/memory/disk; tune FSLogix/container settings and profile size.

## References & templates
- Intune compliance policies and configuration profiles
- Autopilot deployment guides (Microsoft/Apple DEP)
- Printer universal driver strategy and secure print best practices
- VDI architecture checklist (AVD / Citrix)
- CMDB schema and ITSM integration patterns
- Patch management runbook and exception process

## Notes
- Keep SOE documentation under version control (Git/repository) and link images to CI/CD.
- Align hardware lifecycle with finance and security for EOL handling and cost control.
- Regularly review OS fragmentation and retire unsupported versions to reduce risk.
- Balance user experience with security; use conditional access to protect corporate data on personal devices.

---
*Created for the it-team-endpoints skill. Tailor steps, OKRs, and SLAs to your organization's size, tooling, and risk appetite.*

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
