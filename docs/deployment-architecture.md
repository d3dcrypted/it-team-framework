# Deployment Architecture and Operating Model

This document defines the recommended filesystem layout, runtime components, configuration boundaries, and execution workflow for the IT Team Framework.

The repository is a standalone project. It must not read from or persist data in a personal knowledge vault, Honcho, personal notes, or unrelated infrastructure directories.

## 1. Logical components

```text
+---------------------------+
| Operator / IT Lead        |
| approves scope and work   |
+-------------+-------------+
              |
              v
+---------------------------+
| Hermes Agent               |
| orchestrator model        |
| delegation/worker model   |
+-------------+-------------+
              |
              v
+---------------------------+
| IT Team Framework skills  |
| orchestrator              |
| 9 specialist skills       |
| security gatekeeper       |
+-------------+-------------+
              |
              v
+---------------------------+
| Optional FastAPI API       |
| state, recommendations,    |
| gate decisions, roadmap    |
+-------------+-------------+
              |
              v
+---------------------------+
| Local SQLite database      |
| deployment-specific data   |
+---------------------------+
```

The API is optional. The skills and the Hermes workflow can be used without running the API.

## 2. Recommended filesystem layout

Use separate paths for source code, Hermes runtime skills, secrets, and operational data.

```text
/srv/it-team-framework/                         # repository checkout
├── README.md
├── .env.example                                # safe template only
├── api/
│   ├── server.py
│   └── it-team-api.service                     # service template
├── orchestrator/SKILL.md
├── gatekeeper/SKILL.md
├── specialists/*/SKILL.md
├── assessment/interview-guide.md
├── docs/
└── scripts/

/home/<operator>/.hermes/                       # Hermes runtime, operator-owned
├── config.yaml                                 # model/provider configuration
├── skills/
│   ├── it-team-orchestrator/SKILL.md
│   ├── it-team-gatekeeper/SKILL.md
│   ├── it-team-assessment-guide/SKILL.md
│   └── it-team-*/SKILL.md                      # specialist skills
└── .env                                        # provider secrets, mode 0600

/etc/it-team-framework/
└── api.env                                     # optional production API secrets, mode 0600

/var/lib/it-team-framework/
└── it_team.db                                  # persistent API state, service-owned

/var/log/it-team-framework/                     # optional service logs
└── api.log
```

The exact root paths may be changed, but the separation of responsibilities should remain.

### Required placement rules

1. Keep the Git repository in a dedicated source directory such as `/srv/it-team-framework`, `/opt/it-team-framework`, or an operator home directory.
2. Install the skills into the Hermes skill directory used by the same OS user that runs Hermes. The deployment script is the supported installation path.
3. Keep `config.yaml` in the active Hermes home, not inside the Git repository.
4. Keep provider API keys in the active Hermes secret store or environment, never in Git.
5. Keep `IT_TEAM_API_KEY` outside Git and outside `.env.example`.
6. Keep the SQLite database outside the source tree for production deployments.
7. Keep generated reports and engagement data in a deployment-specific, access-controlled data directory.
8. Do not place the repository inside a personal vault or use a personal vault as the framework database.

## 3. Ownership and permissions

Recommended Linux ownership:

```text
/srv/it-team-framework              root:it-team-framework   0750
/etc/it-team-framework/api.env      it-team:it-team-framework 0600
/var/lib/it-team-framework          it-team:it-team-framework 0750
/var/lib/it-team-framework/it_team.db  it-team:it-team-framework 0600
/home/<operator>/.hermes/config.yaml <operator>:<operator> 0600
/home/<operator>/.hermes/.env       <operator>:<operator> 0600
```

Use a dedicated non-root service account for the API. Do not run the API as root.

The exact group ownership depends on the operating system. The requirement is that only the Hermes operator and the API service account can read operational data and secrets.

## 4. Hermes installation sequence

From the repository root:

```bash
cd /srv/it-team-framework
chmod +x scripts/*.sh
./scripts/deploy-skills.sh
```

The script copies or registers the repository skills in the active Hermes installation. Verify that the target skill files exist under the Hermes skill directory before starting an engagement.

Then configure the models and providers in the active Hermes configuration. The model IDs in examples are replaceable seeds:

```yaml
# /home/<operator>/.hermes/config.yaml
model:
  default: <provider>/<orchestrator-model>
  provider: <provider>

delegation:
  model: <provider>/<worker-model>
  provider: <provider>
  max_concurrent_children: 3
```

A worker/delegation model is optional. If used, select it independently from the orchestrator model.

## 5. API installation sequence

The API requires Python and the dependencies in `requirements.txt`.

For a local demo:

```bash
cd /srv/it-team-framework
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt pytest
cd api
export IT_TEAM_MODE=demo
uvicorn server:app --host 127.0.0.1 --port 8080
```

For production:

```bash
sudo install -d -o it-team -g it-team-framework -m 0750 /var/lib/it-team-framework
sudo install -d -o root -g it-team-framework -m 0750 /etc/it-team-framework
sudo install -m 0600 -o it-team -g it-team-framework /path/to/api.env /etc/it-team-framework/api.env
```

The production environment file must contain locally generated values, for example:

```text
IT_TEAM_MODE=production
IT_TEAM_API_KEY=<long-random-local-secret>
IT_TEAM_DB_PATH=/var/lib/it-team-framework/it_team.db
```

Do not copy this file into the repository.

## 6. Systemd placement and service configuration

The supplied `api/it-team-api.service` is a template. Review and adapt `User`, `WorkingDirectory`, the virtual-environment Python path, and `EnvironmentFile` before enabling it.

Important: the supplied unit uses `%i`, which is meaningful for an instantiated unit such as `it-team-api@it-team.service`. If you install it as the non-instantiated `it-team-api.service`, replace `%i` with the dedicated service user and configure the environment file explicitly. Do not enable the unmodified template in production.

A concrete deployment should use a normal service unit, for example:

```ini
[Unit]
Description=IT Team Framework API
After=network.target

[Service]
Type=simple
User=it-team
Group=it-team-framework
WorkingDirectory=/srv/it-team-framework/api
EnvironmentFile=/etc/it-team-framework/api.env
ExecStart=/srv/it-team-framework/.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Install and validate it with:

```bash
sudo install -m 0644 api/it-team-api.service /etc/systemd/system/it-team-api.service
sudo systemctl daemon-reload
sudo systemctl enable --now it-team-api.service
sudo systemctl status it-team-api.service
curl --fail http://127.0.0.1:8080/health
```

Place TLS termination, external authentication, rate limiting, and network policy in a reverse proxy or private gateway. Do not bind this API directly to a public interface.

## 7. Correct engagement workflow

Every engagement should follow this sequence:

```text
0. Define scope and data classification
        |
        v
1. Intake: collect business context and identify missing data
        |
        v
2. Parallel assessment: run the nine specialist domains
        |
        v
3. Normalize findings: separate facts, assumptions, unknowns, and evidence
        |
        v
4. Security gate review: review every recommendation
        |
        +--> DENIED: return to the specialist with remediation
        |
        +--> CONDITIONAL: record mandatory pre-deployment conditions
        |
        +--> APPROVED: allow into the roadmap
        |
        v
5. Gap analysis: compare the current state with the target state
        |
        v
6. Roadmap: sequence work by risk, dependency, effort, cost, and rollback
        |
        v
7. Human approval: approve the scope and execution window
        |
        v
8. Execution: implement only approved work
        |
        v
9. Validation: test acceptance criteria, security controls, and rollback
        |
        v
10. Review: record KPIs, residual risk, lessons learned, and next actions
```

No production change should be executed solely because an AI agent proposed it. The operator remains the final authority for scope, risk acceptance, credentials, maintenance windows, and execution approval.

## 8. Data flow and boundaries

```text
Company input
    |
    +--> sanitized engagement context --> Hermes prompt/model provider
    |
    +--> local operational state --> API SQLite database
    |
    +--> approved reports --> access-controlled report directory
```

Do not place credentials, private keys, personal data, customer secrets, production configuration dumps, or unrestricted infrastructure exports in prompts or reports.

If a cloud model is used, classify the data before transmission and verify the provider's retention, training, region, and subprocessors policies. Use a local model or a redacted dataset when the data cannot leave the controlled environment.

## 9. Pre-flight checklist

- [ ] Repository is in a dedicated source directory.
- [ ] Hermes is installed for the intended OS user.
- [ ] All skills are present in the active Hermes skill directory.
- [ ] `config.yaml` points to valid, tested providers/models.
- [ ] Provider keys are stored outside Git with restrictive permissions.
- [ ] `IT_TEAM_MODE=production` is used for a protected deployment.
- [ ] `IT_TEAM_API_KEY` is generated and stored outside Git.
- [ ] SQLite is stored outside the source tree and backed up.
- [ ] API binds to localhost or a private interface.
- [ ] TLS, authentication, rate limiting, and network controls are configured upstream.
- [ ] Data classification and cloud-provider transfer rules are documented.
- [ ] The security gatekeeper has reviewed the recommendations.
- [ ] A human has approved the roadmap and execution window.
- [ ] Rollback and acceptance tests are defined.

## 10. Operational principle

The repository contains reusable code, prompts, schemas, and skills. It is not the authoritative store for customer engagement data, credentials, personal knowledge, or production infrastructure state. Keep those concerns outside the repository and apply explicit access controls, retention rules, backups, and deletion procedures.

See [`configuration.md`](configuration.md), [`api/it-team-api.service`](../api/it-team-api.service), and [`README.md`](../README.md) for the related configuration and quick-start material.
