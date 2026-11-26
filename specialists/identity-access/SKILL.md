---
name: it-team-identity-access
description: "Use when assessing IAM: MFA, PAM, JML, SSO, governance."
category: security
version: 0.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [identity, iam, mfa, pam, sso, entra, active-directory, zero-trust, jml, access-reviews]
    related_skills: [it-team-security, it-team-os-infra, it-team-cloud, it-team-endpoints]
---

# Identity & Access Specialist — IAM Engineer / Identity Architect

Domain: `Identity & Access` (canonical name — never "IAM", "Identity", or "Authentication" in reports). Covers directory services, authentication, authorization, privileged access, identity lifecycle, federation, and identity governance.

Fills the v0.2 contract gap: the domain existed in the orchestrator contract but had no specialist. From v0.3 this skill owns it.

## Assessment Protocol

### 1. Directory Services
- Inventory: on-prem AD (forest/domain level, FSMO, replication health), Entra ID / Azure AD (sync method, connect health), Okta/other IdP.
- AD hygiene: stale objects, tombstone lifetime, SYSVOL replication (FRS vs DFSR), unsupported schema extensions.
- Hybrid: Entra Connect vs Cloud Sync, password hash sync vs PTA vs federation, sync errors, staging server.

### 2. Identity Lifecycle (Joiner / Mover / Leaver)
- How are accounts created, changed, disabled? Manual, HR-driven, automated (SCIM)?
- Time-to-provision (joiner) and time-to-deprovision (leaver) — measure both.
- Orphaned accounts: enabled accounts with no owner or no login >90 days.
- Contractor/external identity handling and expiry dates.

### 3. Authentication
- MFA coverage: % admins, % users, % VPN, % cloud apps. Methods (SMS = weak, authenticator, FIDO2).
- Conditional Access / risk-based policies: baseline present? Legacy auth blocked?
- Passwordless adoption; password policy vs NIST 800-63 (length over rotation).
- Break-glass accounts: exist, excluded from CA, monitored, tested?

### 4. Privileged Access
- Count of privileged accounts (Domain Admins, Global Admins, subscription Owners). Target: minimal, known, justified.
- PAM/PIM: just-in-time elevation? Approval workflow? Session recording?
- Admin workstation separation (PAW), tiering model (Tier 0/1/2).
- Shared admin accounts and service accounts with interactive login = findings.

### 5. Authorization & Governance
- RBAC model: role definitions documented? Group sprawl and nesting depth.
- Access reviews (recertification): frequency, coverage, completion rate.
- Segregation of duties for critical systems (finance, HR, production).
- Entitlement management for app access requests.

### 6. Federation & SSO
- SSO coverage: % of business apps behind the IdP vs local logins.
- Protocols in use: SAML/OIDC (good), legacy LDAP binds, NTLM (flag).
- B2B/guest access policy and cleanup process.

### 7. Service Accounts & Secrets
- Inventory of service accounts, owners, password age, SPN/Kerberoastable accounts.
- gMSA/managed identities adoption vs static credentials.
- Secrets in scripts/config: refer findings to it-team-security and it-team-devops-platform.

### 8. Identity Threat Detection
- Identity protection signals (risky sign-ins, impossible travel) monitored? Routed where?
- AD attack-path exposure (BloodHound-style review), tier-0 protection.
- Alerting on privileged group changes.

## Improvement Catalog

- **MFA completion**: close gaps to 100% admins, >95% users; kill legacy auth. Quick win, highest risk reduction per euro.
- **Conditional Access baseline**: block legacy auth, require MFA off-network, require compliant device for sensitive apps.
- **Tiering + PAW for admins**: separate Tier 0 credentials from daily-driver accounts.
- **PIM/JIT elevation**: no standing Global/Domain Admin; time-boxed, approved elevation.
- **JML automation**: HR-driven provisioning (SCIM), automatic leaver disable within 24h.
- **Access reviews**: quarterly for privileged roles, semi-annual for app entitlements.
- **Passwordless rollout**: FIDO2/Windows Hello for admins first, then users.
- **Service account cleanup**: migrate to gMSA/managed identities, vault the rest.

## KPIs

| KPI | Target |
|---|---|
| MFA coverage (admin / user) | 100% / ≥95% |
| Time-to-deprovision (leaver) | ≤24h |
| Orphaned enabled accounts | 0 |
| Standing privileged accounts | ≤5 per environment, all justified |
| SSO coverage of business apps | ≥80% |
| Access review completion | 100% privileged, ≥90% overall |

## Common Pitfalls

1. MFA rollout without CA policies — users register but legacy auth still bypasses it.
2. Deprovisioning that disables AD but forgets SaaS apps outside SSO.
3. PAM tool bought, tiering never implemented — tool ≠ model.
4. Access reviews that auto-approve everything: completion 100%, value 0.
5. Break-glass accounts excluded from MFA but also excluded from monitoring.

## Framework Contract (v0.3)

This skill follows the shared it-team contract defined in `orchestrator/SKILL.md` — the single source of truth for: severity enum and SLAs (`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), assessment report JSON schema, canonical domain names, execution states, and evidence rules. Do not redefine those here; if any local text conflicts with the orchestrator contract, the orchestrator contract wins.
