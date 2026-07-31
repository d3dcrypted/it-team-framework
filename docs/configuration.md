# Configuration

## API modes

The API supports two modes:

- `demo`: local development and tests. Authentication is not required. Do not expose this mode outside a trusted local environment.
- `production`: requires `IT_TEAM_API_KEY`. Every endpoint except `/health` requires an HTTP Bearer token matching that key.

The API binds to `127.0.0.1` in the supplied systemd template. Keep it on a private interface or place it behind a properly configured TLS reverse proxy. Do not expose the API directly to the public Internet.

## Environment variables

Copy `.env.example` to an untracked local file, or export the variables through your process manager. Never commit real values.

| Variable | Required | Default | Purpose |
|---|---:|---|---|
| `IT_TEAM_MODE` | No | `demo` | Selects `demo` or `production`. Production is required for authenticated deployments. |
| `IT_TEAM_API_KEY` | Only in production | None | Secret used as the HTTP Bearer token. Generate and store it locally. |
| `IT_TEAM_DB_PATH` | No | `api/it_team.db` | SQLite database path. Use a persistent path outside the repository for deployments. |
| `IT_TEAM_CORS_ORIGINS` | No | Empty | Comma-separated trusted frontend origins. Leave empty unless browser-based cross-origin access is needed. |
| `IT_TEAM_LOG_LEVEL` | No | `INFO` | Python logging level. |

Example local startup:

```bash
cd api
export IT_TEAM_MODE=demo
uvicorn server:app --host 127.0.0.1 --port 8080
```

Example production startup:

```bash
export IT_TEAM_MODE=production
export IT_TEAM_API_KEY='set-this-locally-and-never-commit-it'
export IT_TEAM_DB_PATH='/var/lib/it-team-framework/it_team.db'
cd api
uvicorn server:app --host 127.0.0.1 --port 8080
```

Use a secret manager or a root-readable environment file in production. Do not put secrets in shell history, source code, README examples, GitHub Actions logs, or issue reports.

## AI providers and models

The framework does not require the model IDs used in the original examples. They are demonstration seeds only. Replace them according to your provider, data-residency requirements, quality target, latency, availability and budget.

The framework can be used with:

- cloud APIs through a provider-compatible adapter;
- self-hosted or local models through a local adapter;
- different models for planning/reasoning and execution/delegation;
- a mixed strategy where sensitive data stays local and general reasoning uses a cloud provider.

API keys for AI providers belong in the provider's local secret store or environment variables. They must not be committed to this repository. The exact adapter and model configuration is intentionally deployment-specific because the framework's v0.2 API currently provides deterministic demo behavior; live Hermes/provider integration is a separate adapter.

There are two separate credential locations:

1. `IT_TEAM_API_KEY` protects this framework API in `production` mode. Set it in the local environment file or secret manager used by the API process.
2. The AI provider key is consumed by Hermes/the selected adapter. Configure it in the local Hermes/provider configuration or the provider-specific environment variable required by that adapter (for example, an `OPENROUTER_API_KEY`-style variable). Do not add provider keys to this repository, `.env.example`, issue reports, or documentation.

The exact provider variable name is not standardized by this framework. Follow the selected provider or Hermes adapter documentation and verify that the process can read the secret without printing it to logs.

## Budget profiles

The following profiles are planning patterns, not price guarantees. Provider pricing, model availability, context limits and quality change over time. Re-evaluate current prices before deployment.

| Profile | Typical strategy | Cost tendency | Trade-offs |
|---|---|---:|---|
| Local-only | Local open-weight model for planning and execution | Infrastructure cost only | Maximum data control; requires hardware and may reduce quality or speed. |
| Local-first hybrid | Local model for sensitive/large context; cloud model only for selected reasoning | Low to medium | Better privacy/cost balance; requires routing and clear data classification. |
| Economy cloud | Small/fast model for both planning and execution | Low | Good for routine assessments; weaker on complex architecture and long synthesis. |
| Balanced | Strong reasoning model for planning plus cheaper execution model | Medium | Usually the best cost/quality trade-off for multi-agent workflows. |
| Quality-first | High-quality reasoning model plus reliable execution model | High | Better consistency and complex decision quality; higher cost and possible latency. |
| Enterprise-controlled | Approved provider, private networking/region controls, logging and retention policies | Variable/high | Stronger governance and compliance; procurement and integration overhead. |

Practical controls to reduce cost without weakening the workflow:

1. Use a cheaper model for deterministic formatting, extraction and routine specialist tasks.
2. Reserve the strongest model for architecture, synthesis and gatekeeper decisions.
3. Limit context to the data required for the current domain.
4. Cache stable reference material and avoid resending it unnecessarily.
5. Set provider spending limits and monitor usage.
6. Keep a fallback model available, but validate its output quality before relying on it.

There is no mandatory default combination. Choose and document the combination that matches the engagement's risk, privacy, latency and budget requirements.

## Deployment notes

- Run production with a dedicated operating-system user and a persistent database path.
- Keep the API on a private network and use TLS at the reverse proxy.
- Restrict CORS to known frontend origins.
- Rotate API keys using the local secret-management process.
- Back up the SQLite database and test restoration before treating it as authoritative data.
- Do not store personal vault content, Honcho data, private notes, credentials or infrastructure secrets in this standalone project.

See `api/it-team-api.service` for a portable systemd template, [`deployment-architecture.md`](deployment-architecture.md) for the complete placement and operating model, and `README.md` for the quick-start workflow.

## Configuration checklist

Before deployment:

- [ ] Choose `demo` only for local development; use `production` for a protected deployment.
- [ ] Generate and store `IT_TEAM_API_KEY` outside Git.
- [ ] Choose a persistent database path outside the repository.
- [ ] Configure TLS, authentication and private networking at the reverse proxy.
- [ ] Set CORS only if required, and list trusted origins explicitly.
- [ ] Select models and providers based on data classification, quality, latency and budget.
- [ ] Verify provider terms, data retention and regional-transfer requirements.
- [ ] Test the deployment and its rollback procedure.

This project is a framework and a demo API, not a complete production security boundary. The operator remains responsible for deployment hardening and compliance.
