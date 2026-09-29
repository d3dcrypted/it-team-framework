# Model Strategy for Workers, Agents & Sub‑agents

## 1. Overview
- **Goal**: maximise throughput of the Hermès orchestration while keeping monthly LLM cost < €30.
- **Assumptions**: 1 CPU VM, OpenRouter as provider, ability to switch models per‑task via Hermès delegation.

## 2. Model Roles
| Role | Primary Model | Backup Model | Typical Use‑case | Cost / 1 k tokens |
||------|---------------|--------------|------------------|-------------------|
|| **Orchestrator / Default** | `deepseek/deepseek‑v4‑flash` (OpenRouter) | `openai/gpt‑oss‑120b` (OpenRouter) | General agent, coding, complex reasoning. | ~ $0.019–0.021 / 1k tok |
|| **Decision / Delegation** | `typesafe/jev‑router` (JevRouter, OpenRouter) | – | Task classification, routing decisions, fast cheap inference. | ~ $0.042 / 1k tok (input), $0 output |
|| **Local fallback** | `qwen3` (Ollama, local) | – | Offline/private short prompts, retrieval. | $0 (local) |

## 3. Routing Rules (Hermès config)
1. **Default** – All agent tasks use `deepseek/deepseek‑v4‑flash`.
2. **Delegation / Classification** – Sub‑agents and task routing use `typesafe/jev‑router`.
3. **Local / offline** – `qwen3` (Ollama) for private short prompts, fallback if OpenRouter unreachable.
4. **Cost‑threshold** – If estimated token count > 10 k for a single request, split into sub‑tasks.
5. **Fallback** – On model error, retry with `openai/gpt‑oss‑120b`.

## 4. Cost Monitoring & Alerts
- **Cron `budget-watchdog`** already watches daily spend.
- Add a **model‑usage log** (`~/.hermes/cache/model_usage.log`) updated by each worker via a lightweight wrapper (`hermes-model-wrapper.sh`).
- Alert via Telegram when daily spend > $5 or projected monthly > €30.

## 5. Model Update Cycle
1. Quarterly review of OpenRouter pricing (via `web_search`).
2. Pull new LLM releases; run a cheap benchmark (prompt‑to‑output latency, token cost) on a sandbox repo.
3. Promote the best‑performing model to the **Reasoning** role; demote if cost > 15 % of budget.

## 6. Governance
- Document any deviation in this file – timestamp and rationale.
- Use `ponytail` style – keep changes to a one‑line diff when possible.
- All workers must call `hermes-model-wrapper.sh` to ensure logging.

*Generated on $(date) for user d3d.*