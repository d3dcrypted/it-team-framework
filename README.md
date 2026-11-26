# IT Team Framework

Multi-agent framework for corporate IT departments: a full IT team as specialized AI agents, run by an artificial CTO/IT Manager. v0.3 has 13 domain specialists, a security gatekeeper that reviews risk before execution, and an independent validator that checks the result against evidence. Sized for medium-to-large organizations.

## Philosophy

IT work is assessment, planning, execution and follow-through, not technical skill alone. The framework turns each IT role into a Hermes agent that can:

1. **Assessing** the current state (assessment)
2. **Planning** improvements (gap analysis + roadmap)
3. **Executing** changes (implementation playbook)
4. **Monitoring** results (KPIs and reports)

## Architecture

```
┌─────────────────────────────────────────────────┐
│              ORCHESTRATOR (CTO/CISO)             │
│  - Company intake                                │
│  - Parallel assessment coordination              │
│  - Security Gate Review (approve/deny)           │
│  - Gap analysis synthesis                        │
│  - Prioritized roadmap                           │
│  - Execution assignment                          │
└──────┬──────────────┬──────────────┬─────────────┘
       │              │              │
  ┌────▼──┐     ┌─────▼─────┐    ┌──▼──────┐
  │OS/Infra│     │ Security  │    │  Cloud  │  ... 13 specialists
  │Agent   │     │Gatekeeper │    │  Agent  │
  └────────┘     │(approve/  │    └─────────┘
                 │ deny rec) │
                 └───────────┘
```

## Structure

```
it-team-framework/
├── README.md
├── orchestrator/
│   └── SKILL.md              # CTO/IT Manager agent
├── specialists/
│   ├── os-infra/SKILL.md     # Operating systems, servers, virtualization
│   ├── cloud/SKILL.md        # Cloud IaaS/PaaS/SaaS
│   ├── applications/SKILL.md # Enterprise applications, CRM, ERP
│   ├── security/SKILL.md     # Security, compliance, monitoring
│   ├── network/SKILL.md      # LAN/WAN/VPN/firewall network
│   ├── data/SKILL.md         # Storage, backup, DR, analytics
│   ├── budget/SKILL.md       # Budget, licensing, vendor, procurement
│   ├── endpoints/SKILL.md    # Workstations, mobile, MDM, printers
│   ├── service-desk/SKILL.md # Helpdesk, ticketing, user training
│   ├── identity-access/SKILL.md   # IAM, MFA, PAM, JML lifecycle (v0.3)
│   ├── observability/SKILL.md     # Monitoring, logging, alerting, SLOs (v0.3)
│   ├── ai-automation/SKILL.md     # AI adoption, RPA, AI governance (v0.3)
│   └── devops-platform/SKILL.md   # CI/CD, IaC, containers, DORA (v0.3)
├── validator/
│   └── SKILL.md              # Independent technical validator (v0.3)
├── gatekeeper/
│   └── SKILL.md              # Security Gatekeeper (review/approve/deny)
├── api/
│   ├── server.py             # FastAPI server for remote management
│   └── it-team-api.service   # Systemd unit for daemon
├── assessment/
│   └── interview-guide.md    # Interview guide for initial assessment
├── docs/
│   ├── configuration.md           # API, secrets, providers, and budget profiles
│   ├── deployment-architecture.md # Filesystem layout and operating model
│   └── model-budget-analysis.md   # Historical AI model budget analysis
└── scripts/
    ├── deploy-skills.sh      # Install all skills in Hermes
    └── new-engagement.sh     # Start a new engagement
```

## How to Use

### 1. Installation

```bash
cd ~/it-team-framework
chmod +x scripts/*.sh
./scripts/deploy-skills.sh
```

### 2. New Engagement

```bash
hermes chat
# Load the orchestrator skill: /skill it-team-orchestrator
# Or use the script:
./scripts/new-engagement.sh "Acme Corp" --size 50 --sector manufacturing
```

### 3. Workflow

The orchestrator follows these phases:

| Phase | Action | Agents Involved |
|-------|--------|-----------------|
| **Intake** | Collect company data (employees, sector, IT stack) | Orchestrator |
| **Assessment** | Analyze current state for each domain | All (parallel) |
| **Gate Review** | Security gatekeeper approves/denies each recommendation | Security Gatekeeper |
| **GAP Analysis** | Compare AS-IS vs BEST PRACTICES (only approved recommendations) | Orchestrator |
| **Roadmap** | Prioritized plan with timelines and costs | Orchestrator |
| **Execution** | Implement improvements | Assigned specialists |
| **Review** | Verify KPIs and final report | Orchestrator |

### 4. Privacy

**Warning**: data entered in prompts (intake, assessment) is transmitted via OpenRouter to model providers. The framework mitigates this as follows:
- Never enter passwords, secrets, or personal data in prompts (see the orchestrator's Common Pitfalls)
- Local assessment templates (no external file uploads)
- Reports generated and saved locally
- For EU data residency or full privacy, use local models (see `docs/model-budget-analysis.md`)

## IT Team Roles

| Role | Agent | Key Competencies |
|------|-------|------------------|
| **CTO/IT Manager** | Orchestrator | Strategy, coordination, prioritization |
| **CISO/IT Auditor** | Security Gatekeeper | Cross-cutting gate review: approves/denies each recommendation |
| **Senior Sysadmin** | OS & Infra | Servers, AD, patching, virtualization |
| **Cloud Architect** | Cloud | IaaS/PaaS, migration, FinOps |
| **Application Manager** | Applications | CRM, ERP, integrations, lifecycle |
| **Security Engineer** | Security | Security assessment, SIEM, incident response, GDPR |
| **Network Engineer** | Network | LAN/WAN, firewall, VPN, SD-WAN |
| **Storage & DR Admin** | Data | Backup, disaster recovery, analytics |
| **IT Procurement** | Budget & Procurement | Vendor management, licensing, CAPEX/OPEX |
| **Endpoint Engineer** | Endpoints | MDM, SOE, mobile, client patching |
| **IT Support Lead** | Service Desk | Ticketing, SLA, knowledge base, training |

## Engagement Example

```bash
# 1. Load orchestrator
hermes chat -q "Load skill it-team-orchestrator. New engagement for a 100-employee company in logistics, IT stack: on-prem AD, Office 365, 3 VMware servers, NAS backup, Fortinet firewall."

# 2. The orchestrator will:
#    - Parallel assessment of all domains
#    - Gap analysis report
#    - 6-12 month roadmap
#    - Estimated budget for improvements

# 3. Once the roadmap is approved, execute:
hermes chat -q "Execute phase 1 of the roadmap: upgrade AD to Azure AD Connect and backup automation"
```

## Configuration and deployment

The API configuration, required and optional environment variables, local secret handling, production deployment guidance, and budget profiles are documented in [`docs/configuration.md`](docs/configuration.md).

For the complete filesystem layout, component placement, permissions, systemd deployment, data boundaries, and end-to-end operating workflow, read [`docs/deployment-architecture.md`](docs/deployment-architecture.md).

The model IDs shown in examples are replaceable seeds, not mandatory dependencies. Select cloud or local providers according to privacy, data residency, quality, latency, availability, and budget requirements.

## Management API (Optional)

`api/server.py` exposes a FastAPI API for tracking engagements, recommendations, gate reviews, and roadmaps (local SQLite).

```bash
pip install fastapi uvicorn
uvicorn server:app --host 127.0.0.1 --port 8080   # from api/
# or as a daemon: cp api/it-team-api.service /etc/systemd/system/ && systemctl enable --now it-team-api
```

Main endpoints: `POST /engagements`, `POST /engagements/{id}/assess`, `GET /engagements/{id}/recommendations`, `POST /engagements/{id}/gate-review`, `POST /engagements/{id}/gate-review/{rec_id}/decision`, `GET /engagements/{id}/roadmap`, `POST /engagements/{id}/execute`, `GET /health`.

The API requires `IT_TEAM_API_KEY` when `IT_TEAM_MODE=production`; in `demo` mode it is intended for local use only. Do not expose the API directly to the Internet: use a TLS reverse proxy, authentication, and a private network. The models in the initial database are demonstration seeds and should be replaced or updated based on the chosen provider.

## Authorship

Human thought, machine hand. The author set the direction, took the decisions and reviewed the result; an AI assistant produced the drafting, the code and the prose in this file. Mistakes are the author's.

## Contributing

Repository workflow, branch naming, pull requests, validation, commit messages, and release rules are documented in [`CONTRIBUTING.md`](CONTRIBUTING.md).

`main` is the protected, releasable branch. Changes must be developed on a short-lived branch and merged through a pull request after CI passes.

## Versioning

The project follows Semantic Versioning (`MAJOR.MINOR.PATCH`). The current version is in `VERSION`.

```bash
# Check version
cat VERSION

# Create a release tag after verification
git add .
git commit -m "release: v$(tr -d "\n" < VERSION)"
git tag -a "v$(tr -d "\n" < VERSION)" -m "IT Team Framework v$(tr -d "\n" < VERSION)"
```

Changes must be recorded in `CHANGELOG.md`. Do not commit databases, secrets, virtual environments, or temporary reports.

## Requirements

- Hermes Agent v0.19+
- Orchestrator model: any Hermes-compatible provider/model; the IDs shown in examples are replaceable seeds
- Worker model: optional and replaceable; choose according to task complexity, privacy, latency, and cost
- Budget: deployment-dependent; see the documented local, hybrid, economy, balanced, quality-first, and enterprise-controlled profiles
