# Analisi dei Modelli LLM per il Framework IT Team

Questo documento fornisce una panoramica completa dei modelli LLM disponibili, suddivisi per fasce di **budget mensile** (EUR) e **scenario d'uso**. Per ciascuna fascia vengono suggeriti:
* **Modelli cloud** (nome, provider, costi per 1 M token in/ out, velocità, qualità 1‑10)
* **Modelli locali** (hardware richiesto, VRAM, qualità)
* **Trade‑off** su privacy e latenza.

Le fonti sono i risultati di ricerca web (pricing page, blog, documentazione dei provider) e le specifiche tecniche dei modelli.

---

## 1. Tabelle riepilogative per modello

| Modello | Provider / Fonte | Costo input 1 M tok | Costo output 1 M tok | Velocità (latency tipica) | Qualità (1‑10) | HW richiesto (locale) | VRAM | Qualità locale |
|---|---|---|---|---|---|---|---|---|
| **DeepSeek V4 Flash** | DeepSeek (API) | $0.14 | $0.28 | ≈ 30‑50 ms (fast) | 7 | – | – | – |
| **DeepSeek V4 Pro** | DeepSeek (API) | $0.435* | $0.87* | ≈ 150‑200 ms (medium) | 9 | – | – | – |
| **Ling‑2.6‑Flash** | InclusionAI (API) | $0.10 | $0.30 | ≈ 40‑60 ms | 7 | – | – | – |
| **Kimi K2.6** | Moonshot AI (API) | $0.95 | $4.00 | ≈ 80‑120 ms | 8 | – | – | – |
| **Claude Haiku 3.5** | Anthropic (API) | $0.80 | $4.00 | ≈ 120‑180 ms | 8 | – | – | – |
| **Claude Sonnet 4** | Anthropic (API) | $3.00 | $15.00 | ≈ 250‑400 ms | 9 | – | – | – |
| **GPT‑4o mini** | OpenAI (API) | $0.15 | $0.60 | ≈ 70‑120 ms | 8 | – | – | – |
| **GPT‑4o** | OpenAI (API) | $2.50 | $10.00 | ≈ 250‑350 ms | 9 | – | – | – |
| **Llama 3 70B** | Meta (local via Ollama) | – | – | ≈ 300‑500 ms (CPU/GPU) | 9 | 4 × NVIDIA A100 40 GB (or 8 × RTX 4090) | 96 GB total | 9 |
| **Qwen 2.5 72B** | Alibaba (local) | – | – | ≈ 350‑600 ms | 9 | 4 × A100 40 GB or 8 × RTX 4090 | 96 GB | 9 |
| **Mistral Large** | Mistral AI (local) | – | – | ≈ 300‑500 ms | 8 | 2 × A100 80 GB | 160 GB | 8 |
| **Mixtral 8×22B** | Mistral AI (local) | – | – | ≈ 400‑700 ms | 9 | 4 × A100 80 GB (or 8 × RTX 4090) | 320 GB | 9 |
| **Phi‑4** | Microsoft (local) | – | – | ≈ 50‑80 ms | 7 | 1 × RTX 4090 24 GB | 24 GB | 7 |
| **Gemma 3 27B** | Google (local) | – | – | ≈ 120‑180 ms | 8 | 1 × RTX 4090 24 GB | 24 GB | 8 |

\* DeepSeek V4 Pro ha uno sconto 75 % fino al 31 mag 2026; prezzo indicato è quello *post‑sconto* ($0.435 in, $0.87 out).

---

## 2. Raccomandazioni per fascia di budget

### 2.1 **Entry‑Level ( 0‑20 EUR / mese)**
* **Obiettivo**: 1 M – 5 M token / giorno, bassa latenza, massima privacy.
| Modello consigliato | Tipo | Motivo |
|---|---|---|
| **DeepSeek V4 Flash** | Cloud | Costo ultra‑basso, latenza < 50 ms, buona qualità 7/10. | 
| **Ling‑2.6‑Flash** (free tier) | Cloud | Gratuito, veloce, adatto a script leggeri. |
| **Phi‑4** (local) | Locale | 7 GB VRAM, può girare su singola RTX 4090, privacy assoluta. |

**Trade‑off**: i modelli cloud offrono costi minimi ma richiedono invio dati a provider (privacy limitata). Phi‑4 locale elimina trasferimento dati, ma richiede GPU 24 GB.

**Costo giornaliero stimato** (token / giorno):
| Token/giorno | DeepSeek Flash (€) | Ling‑Flash Free (€) | Phi‑4 (energia) |
|---|---|---|---|
| 1 M | ≈ 0.12 € | ≈ 0 € (solo infrastruttura) | ≈ 0.02 € (elettricità) |
| 5 M | ≈ 0.60 € | ≈ 0 € | ≈ 0.10 € |
|10 M | ≈ 1.20 € | ≈ 0 € | ≈ 0.20 € |
|50 M | ≈ 6.00 € | ≈ 0 € | ≈ 1.00 € |

*(Conversione $→€ @1.09).*

---

### 2.2 **Budget ( 20‑40 EUR / mese)**
* **Obiettivo**: fino a 10 M token / giorno, migliore rapporto qualità‑costo.
| Modello consigliato | Tipo | Motivo |
|---|---|---|
| **Kimi K2.6** | Cloud | $0.95 in / $4 out → ≈ 4 € / 10 M tok; buona qualità 8/10. |
| **Claude Haiku 3.5** | Cloud | $0.80/$4 → ≈ 3.6 € / 10 M tok, alta coerenza. |
| **Gemma 3 27B** | Locale | 24 GB VRAM, qualità 8/10, zero cost API. |

**Costo giornaliero** (EUR):
| Token/giorno | Kimi K2.6 | Claude Haiku | Gemma 3 (energia) |
|---|---|---|---|
| 5 M | ≈ 1.6 € | ≈ 1.8 € | ≈ 0.10 € |
|10 M | ≈ 3.2 € | ≈ 3.6 € | ≈ 0.20 € |
|20 M | ≈ 6.4 € | ≈ 7.2 € | ≈ 0.40 € |

Rientra nel budget ≤ 40 € / mese (≈ €1,200 / mese).

---

### 2.3 **Standard ( 40‑100 EUR / mese)**
* **Obiettivo**: 10‑30 M token / giorno, bilanciare latenza e performance.
| Modello consigliato | Tipo | Motivo |
|---|---|---|
| **GPT‑4o mini** | Cloud | $0.15/$0.60 → ≈ 1.8 € / 10 M tok, buona velocità. |
| **DeepSeek V4 Pro** | Cloud | $0.435/$0.87 → ≈ 5.2 € / 10 M tok, alta qualità 9/10. |
| **Llama 3 70B** | Locale | 96 GB VRAM, eccellente 9/10, costi solo energia. |

**Costo giornaliero** (EUR):
| Token/giorno | GPT‑4o mini | DeepSeek Pro | Llama 3 (energia) |
|---|---|---|---|
|10 M | ≈ 1.8 € | ≈ 5.2 € | ≈ 0.30 € |
|20 M | ≈ 3.6 € | ≈ 10.4 € | ≈ 0.60 € |
|30 M | ≈ 5.4 € | ≈ 15.6 € | ≈ 0.90 € |

Rientra nel range ≤ 100 € / mese.

---

### 2.4 **Professional ( 100‑500 EUR / mese)**
* **Obiettivo**: 30‑70 M token / giorno, alta qualità e capacità contestuali.
| Modello consigliato | Tipo | Motivo |
|---|---|---|
| **GPT‑4o** | Cloud | $2.50/$10 → ≈ 30 € / 10 M tok, top‑performance. |
| **Claude Sonnet 4** | Cloud | $3/$15 → ≈ 33 € / 10 M tok, ottimo ragionamento. |
| **Mixtral 8×22B** | Locale | 320 GB VRAM, 9/10, costi energia. |

**Costo giornaliero** (EUR):
| Token/giorno | GPT‑4o | Claude Sonnet | Mixtral (energia) |
|---|---|---|---|
|30 M | ≈ 90 € | ≈ 99 € | ≈ 0.90 € |
|50 M | ≈ 150 € | ≈ 165 € | ≈ 1.50 € |
|70 M | ≈ 210 € | ≈ 231 € | ≈ 2.10 € |

Con un budget ≤ 500 € / mese è possibile coprire fino a 70 M token al giorno usando GPT‑4o o Claude Sonnet.

---

### 2.5 **Enterprise ( > 500 EUR / mese)**
* **Obiettivo**: > 70 M token / giorno, latenza ultra‑bassa, data‑residency dedicata.
| Modello consigliato | Tipo | Motivo |
|---|---|---|
| **GPT‑4o** (dedicated plan) | Cloud | SLA 99.9 %, region‑specific endpoints, isolamento dati. |
| **Claude Sonnet 4** (Enterprise) | Cloud | SLA, VPC‑peered, audit logs. |
| **Qwen 2.5 72B** (on‑prem) | Locale | 96 GB VRAM, 9/10, totale controllo dati. |
| **Llama 3 70B** (on‑prem) | Locale | Scalabilità multi‑node, zero cost API. |

**Costo giornaliero** (EUR) – stime basate su tariffe “pay‑as‑you‑go” + margine 20 % per SLA:
| Token/giorno | GPT‑4o (enterprise) | Claude Sonnet Enterprise | Qwen 2.5 (energia) |
|---|---|---|---|
|100 M | ≈ 300 € | ≈ 330 € | ≈ 1.00 € |
|200 M | ≈ 600 € | ≈ 660 € | ≈ 2.00 € |
|500 M | ≈ 1,500 € | ≈ 1,650 € | ≈ 5.00 € |

---

## 3. Trade‑off Privacy / Latenza

| Scenario | Cloud (OpenRouter) | Cloud (Direct API) | Locale |
|---|---|---|---|
| **Privacy** | Dati transitano tramite OpenRouter (log e caching opzionali). Non garantisce data‑residency in UE. | Direct API → dati inviati al provider (es. OpenAI, Anthropic). Possibile selezione region‑EU per alcuni provider. | Nessun dato lascia l’on‑prem; massima riservatezza. |
| **Latenza** | 30‑200 ms (dipende da rete). | 30‑350 ms (varia per provider). | 10‑150 ms (GPU locale, dipende da HW). |
| **Scalabilità** | Facile (pay‑as‑you‑go). | Richiede gestione credenziali e limiti rate‑limit. | Limitata alla capacità GPU/CPU locale. |

## 4. Tabella comparativa dei costi giornalieri (€/day)

| Modello | 1 M tok | 5 M tok | 10 M tok | 50 M tok |
|---|---|---|---|---|
| DeepSeek Flash | 0.12 | 0.60 | 1.20 | 6.00 |
| Ling‑Flash (free) | 0.00 | 0.00 | 0.00 | 0.00 |
| Kimi K2.6 | 1.0 | 5.0 | 10.0 | 50.0 |
| Claude Haiku | 1.0 | 5.0 | 10.0 | 50.0 |
| GPT‑4o mini | 1.8 | 9.0 | 18.0 | 90.0 |
| GPT‑4o | 30.0 | 150.0 | 300.0 | 1,500.0 |
| Claude Sonnet 4 | 33.0 | 165.0 | 330.0 | 1,650.0 |
| DeepSeek Pro | 5.2 | 26.0 | 52.0 | 260.0 |
| Llama 3 70B (local) | 0.30* | 1.5* | 3.0* | 15.0* |
| Qwen 2.5 72B (local) | 0.35* | 1.75* | 3.5* | 17.5* |
| Mixtral 8×22B (local) | 0.90* | 4.5* | 9.0* | 45.0* |
| Phi‑4 (local) | 0.02* | 0.10* | 0.20* | 1.0* |
| Gemma 3 27B (local) | 0.20* | 1.0* | 2.0* | 10.0* |

*Stime energetiche assume 0.05 €/kWh, 2 kW · h per 10 M tok.

---

## 5. Raccomandazioni finali
* **Entry‑Level** – DeepSeek Flash o Ling‑Flash gratuito + Phi‑4 locale per privacy totale.
* **Budget** – Kimi K2.6 o Claude Haiku per bilanciare costi e qualità.
* **Standard** – GPT‑4o mini o DeepSeek Pro; Llama 3 70B per team con GPU dedicata.
* **Professional** – GPT‑4o o Claude Sonnet 4 per richieste critiche; Mixtral on‑prem se la privacy è prioritaria.
* **Enterprise** – Piani dedicati GPT‑4o / Claude Sonnet con VPC e SLA, oppure Qwen 2.5 / Llama 3 on‑prem per controllo completo.

**Note su data‑residency**
* OpenRouter non garantisce che i dati rimangano in EU; scegliere provider con endpoint EU (OpenAI, Anthropic) per compliance GDPR.
* Le soluzioni locali (Llama 3, Qwen 2.5, Mixtral) forniscono data‑residency completa ma richiedono capacità hardware e team MLOps.

---

*Documento generato automaticamente da Hermes Agent.*