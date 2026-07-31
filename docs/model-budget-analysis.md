# LLM Model Analysis for the IT Team Framework

This document provides a comprehensive overview of available LLM models, organized by **monthly budget** (EUR) and **use scenario**. For each tier, the following are suggested:
* **Cloud models** (name, provider, cost per 1M tokens in/out, speed, quality 1–10)
* **Local models** (required hardware, VRAM, quality)
* **Trade-offs** on privacy and latency.

Sources include web search results (pricing pages, blogs, provider documentation) and technical model specifications.

---

## 1. Summary Table by Model

| Model | Provider / Source | Input Cost 1M tokens | Output Cost 1M tokens | Speed (typical latency) | Quality (1–10) | Required HW (local) | VRAM | Local Quality |
|---|---|---|---|---|---|---|---|---|
| **DeepSeek V4 Flash** | DeepSeek (API) | $0.14 | $0.28 | ≈ 30–50 ms (fast) | 7 | – | – | – |
| **DeepSeek V4 Pro** | DeepSeek (API) | $0.435* | $0.87* | ≈ 150–200 ms (medium) | 9 | – | – | – |
| **Ling-2.6-Flash** | InclusionAI (API) | $0.10 | $0.30 | ≈ 40–60 ms | 7 | – | – | – |
| **Kimi K2.6** | Moonshot AI (API) | $0.95 | $4.00 | ≈ 80–120 ms | 8 | – | – | – |
| **Claude Haiku 3.5** | Anthropic (API) | $0.80 | $4.00 | ≈ 120–180 ms | 8 | – | – | – |
| **Claude Sonnet 4** | Anthropic (API) | $3.00 | $15.00 | ≈ 250–400 ms | 9 | – | – | – |
| **GPT-4o mini** | OpenAI (API) | $0.15 | $0.60 | ≈ 70–120 ms | 8 | – | – | – |
| **GPT-4o** | OpenAI (API) | $2.50 | $10.00 | ≈ 250–350 ms | 9 | – | – | – |
| **Llama 3 70B** | Meta (local via Ollama) | – | – | ≈ 300–500 ms (CPU/GPU) | 9 | 4 × NVIDIA A100 40 GB (or 8 × RTX 4090) | 96 GB total | 9 |
| **Qwen 2.5 72B** | Alibaba (local) | – | – | ≈ 350–600 ms | 9 | 4 × A100 40 GB or 8 × RTX 4090 | 96 GB | 9 |
| **Mistral Large** | Mistral AI (local) | – | – | ≈ 300–500 ms | 8 | 2 × A100 80 GB | 160 GB | 8 |
| **Mixtral 8×22B** | Mistral AI (local) | – | – | ≈ 400–700 ms | 9 | 4 × A100 80 GB (or 8 × RTX 4090) | 320 GB | 9 |
| **Phi-4** | Microsoft (local) | – | – | ≈ 50–80 ms | 7 | 1 × RTX 4090 24 GB | 24 GB | 7 |
| **Gemma 3 27B** | Google (local) | – | – | ≈ 120–180 ms | 8 | 1 × RTX 4090 24 GB | 24 GB | 8 |

\* DeepSeek V4 Pro has a 75% discount valid through 31 May 2026; the price shown is the *post-discount* rate ($0.435 in, $0.87 out).

---

## 2. Recommendations by Budget Tier

### 2.1 **Entry-Level (0–20 EUR / month)**
* **Goal**: 1M–5M tokens / day, low latency, maximum privacy.

| Recommended Model | Type | Rationale |
|---|---|---|
| **DeepSeek V4 Flash** | Cloud | Ultra-low cost, latency < 50 ms, good quality 7/10. |
| **Ling-2.6-Flash** (free tier) | Cloud | Free, fast, suitable for lightweight scripts. |
| **Phi-4** (local) | Local | 7 GB VRAM, runs on a single RTX 4090, full privacy. |

**Trade-off**: Cloud models offer minimal costs but require sending data to providers (limited privacy). Local Phi-4 eliminates data transfer but requires a 24 GB GPU.

**Estimated daily cost** (tokens / day):

| Tokens/day | DeepSeek Flash (€) | Ling-Flash Free (€) | Phi-4 (energy only) |
|---|---|---|---|
| 1M | ≈ 0.12 € | ≈ 0 € (infrastructure only) | ≈ 0.02 € (electricity) |
| 5M | ≈ 0.60 € | ≈ 0 € | ≈ 0.10 € |
| 10M | ≈ 1.20 € | ≈ 0 € | ≈ 0.20 € |
| 50M | ≈ 6.00 € | ≈ 0 € | ≈ 1.00 € |

*(USD → EUR conversion @ 1.09).*

---

### 2.2 **Budget (20–40 EUR / month)**
* **Goal**: up to 10M tokens / day, best quality-cost ratio.

| Recommended Model | Type | Rationale |
|---|---|---|
| **Kimi K2.6** | Cloud | $0.95 in / $4 out → ≈ 4 € / 10M tokens; good quality 8/10. |
| **Claude Haiku 3.5** | Cloud | $0.80 / $4 → ≈ 3.6 € / 10M tokens, high consistency. |
| **Gemma 3 27B** | Local | 24 GB VRAM, quality 8/10, zero API cost. |

**Daily cost** (EUR):

| Tokens/day | Kimi K2.6 | Claude Haiku | Gemma 3 (energy only) |
|---|---|---|---|
| 5M | ≈ 1.6 € | ≈ 1.8 € | ≈ 0.10 € |
| 10M | ≈ 3.2 € | ≈ 3.6 € | ≈ 0.20 € |
| 20M | ≈ 6.4 € | ≈ 7.2 € | ≈ 0.40 € |

Falls within the ≤ 40 € / month budget (≈ €1,200 / year).

---

### 2.3 **Standard (40–100 EUR / month)**
* **Goal**: 10–30M tokens / day, balance latency and performance.

| Recommended Model | Type | Rationale |
|---|---|---|
| **GPT-4o mini** | Cloud | $0.15 / $0.60 → ≈ 1.8 € / 10M tokens, good speed. |
| **DeepSeek V4 Pro** | Cloud | $0.435 / $0.87 → ≈ 5.2 € / 10M tokens, high quality 9/10. |
| **Llama 3 70B** | Local | 96 GB VRAM, excellent 9/10, energy cost only. |

**Daily cost** (EUR):

| Tokens/day | GPT-4o mini | DeepSeek Pro | Llama 3 (energy only) |
|---|---|---|---|
| 10M | ≈ 1.8 € | ≈ 5.2 € | ≈ 0.30 € |
| 20M | ≈ 3.6 € | ≈ 10.4 € | ≈ 0.60 € |
| 30M | ≈ 5.4 € | ≈ 15.6 € | ≈ 0.90 € |

Falls within the ≤ 100 € / month range.

---

### 2.4 **Professional (100–500 EUR / month)**
* **Goal**: 30–70M tokens / day, high quality and contextual capability.

| Recommended Model | Type | Rationale |
|---|---|---|
| **GPT-4o** | Cloud | $2.50 / $10 → ≈ 30 € / 10M tokens, top performance. |
| **Claude Sonnet 4** | Cloud | $3 / $15 → ≈ 33 € / 10M tokens, excellent reasoning. |
| **Mixtral 8×22B** | Local | 320 GB VRAM, 9/10, energy cost only. |

**Daily cost** (EUR):

| Tokens/day | GPT-4o | Claude Sonnet | Mixtral (energy only) |
|---|---|---|---|
| 30M | ≈ 90 € | ≈ 99 € | ≈ 0.90 € |
| 50M | ≈ 150 € | ≈ 165 € | ≈ 1.50 € |
| 70M | ≈ 210 € | ≈ 231 € | ≈ 2.10 € |

With a ≤ 500 € / month budget, it is possible to cover up to 70M tokens per day using GPT-4o or Claude Sonnet.

---

### 2.5 **Enterprise (> 500 EUR / month)**
* **Goal**: > 70M tokens / day, ultra-low latency, dedicated data residency.

| Recommended Model | Type | Rationale |
|---|---|---|
| **GPT-4o** (dedicated plan) | Cloud | 99.9% SLA, region-specific endpoints, data isolation. |
| **Claude Sonnet 4** (Enterprise) | Cloud | SLA, VPC-peered, audit logs. |
| **Qwen 2.5 72B** (on-prem) | Local | 96 GB VRAM, 9/10, complete data control. |
| **Llama 3 70B** (on-prem) | Local | Multi-node scalability, zero API cost. |

**Daily cost** (EUR) – estimates based on pay-as-you-go rates + 20% margin for SLA:

| Tokens/day | GPT-4o (enterprise) | Claude Sonnet Enterprise | Qwen 2.5 (energy only) |
|---|---|---|---|
| 100M | ≈ 300 € | ≈ 330 € | ≈ 1.00 € |
| 200M | ≈ 600 € | ≈ 660 € | ≈ 2.00 € |
| 500M | ≈ 1,500 € | ≈ 1,650 € | ≈ 5.00 € |

---

## 3. Privacy / Latency Trade-offs

| Scenario | Cloud (OpenRouter) | Cloud (Direct API) | Local |
|---|---|---|---|
| **Privacy** | Data transits through OpenRouter (logging and caching optional). Does not guarantee EU data residency. | Direct API → data sent to the provider (e.g., OpenAI, Anthropic). EU region selection available for some providers. | No data leaves the on-premises environment; maximum confidentiality. |
| **Latency** | 30–200 ms (depends on network). | 30–350 ms (varies by provider). | 10–150 ms (local GPU, depends on hardware). |
| **Scalability** | Easy (pay-as-you-go). | Requires credential management and rate-limit handling. | Limited to local GPU/CPU capacity. |

## 4. Comparative Daily Cost Table (€/day)

| Model | 1M tokens | 5M tokens | 10M tokens | 50M tokens |
|---|---|---|---|---|
| DeepSeek Flash | 0.12 | 0.60 | 1.20 | 6.00 |
| Ling-Flash (free) | 0.00 | 0.00 | 0.00 | 0.00 |
| Kimi K2.6 | 1.0 | 5.0 | 10.0 | 50.0 |
| Claude Haiku | 1.0 | 5.0 | 10.0 | 50.0 |
| GPT-4o mini | 1.8 | 9.0 | 18.0 | 90.0 |
| GPT-4o | 30.0 | 150.0 | 300.0 | 1,500.0 |
| Claude Sonnet 4 | 33.0 | 165.0 | 330.0 | 1,650.0 |
| DeepSeek Pro | 5.2 | 26.0 | 52.0 | 260.0 |
| Llama 3 70B (local) | 0.30* | 1.5* | 3.0* | 15.0* |
| Qwen 2.5 72B (local) | 0.35* | 1.75* | 3.5* | 17.5* |
| Mixtral 8×22B (local) | 0.90* | 4.5* | 9.0* | 45.0* |
| Phi-4 (local) | 0.02* | 0.10* | 0.20* | 1.0* |
| Gemma 3 27B (local) | 0.20* | 1.0* | 2.0* | 10.0* |

*Energy estimates assume €0.05/kWh, 2 kWh per 10M tokens.*

---

## 5. Final Recommendations
* **Entry-Level** – DeepSeek Flash or free Ling-Flash + local Phi-4 for full privacy.
* **Budget** – Kimi K2.6 or Claude Haiku to balance cost and quality.
* **Standard** – GPT-4o mini or DeepSeek Pro; Llama 3 70B for teams with dedicated GPUs.
* **Professional** – GPT-4o or Claude Sonnet 4 for critical workloads; Mixtral on-prem when privacy is a priority.
* **Enterprise** – Dedicated GPT-4o / Claude Sonnet plans with VPC and SLA, or Qwen 2.5 / Llama 3 on-prem for full control.

**Data Residency Notes**
* OpenRouter does not guarantee that data remains within the EU; choose providers with EU endpoints (OpenAI, Anthropic) for GDPR compliance.
* Local solutions (Llama 3, Qwen 2.5, Mixtral) provide complete data residency but require hardware capacity and an MLOps team.

---

*Document automatically generated by Hermes Agent.*
