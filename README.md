# IT Team Framework

Framework multi-agente per reparti IT aziendali. Un team IT completo come set di agenti AI specializzati, orchestrati da un CTO/IT Manager artificiale.

## Filosofia

Un reparto IT non è solo competenze tecniche — è assessment, pianificazione, esecuzione e miglioramento continuo. Questo framework traduce ogni ruolo IT in un agente Hermes skillato, capace di:

1. **Valutare** lo stato corrente (assessment)
2. **Pianificare** miglioramenti (gap analysis + roadmap)
3. **Eseguire** le modifiche (implementation playbook)
4. **Monitorare** i risultati (KPI e report)

## Architettura

```
┌─────────────────────────────────────────────────┐
│              ORCHESTRATOR (CTO/CISO)             │
│  - Intake aziendale                              │
│  - Coordinamento assessment parallelo            │
│  - Security Gate Review (approva/nega)           │
│  - Sintesi gap analysis                          │
│  - Roadmap prioritaria                           │
│  - Assegnazione esecuzione                       │
└──────┬──────────────┬──────────────┬─────────────┘
       │              │              │
  ┌────▼──┐     ┌─────▼─────┐    ┌──▼──────┐
  │OS/Infra│     │ Security  │    │  Cloud  │  ... 9 specialisti
  │Agent   │     │Gatekeeper │    │  Agent  │
  └────────┘     │(approva/  │    └─────────┘
                 │ nega rec) │
                 └───────────┘
```

## Struttura

```
it-team-framework/
├── README.md
├── orchestrator/
│   └── SKILL.md              # Agente CTO/IT Manager
├── specialists/
│   ├── os-infra/SKILL.md     # Sistemi operativi, server, virtualizzazione
│   ├── cloud/SKILL.md        # Cloud IaaS/PaaS/SaaS
│   ├── applications/SKILL.md # Applicativi enterprise, CRM, ERP
│   ├── security/SKILL.md     # Sicurezza, compliance, monitoring
│   ├── network/SKILL.md      # Rete LAN/WAN/VPN/firewall
│   ├── data/SKILL.md         # Storage, backup, DR, analytics
│   ├── budget/SKILL.md       # Budget, licensing, vendor, procurement
│   ├── endpoints/SKILL.md    # Workstation, mobile, MDM, stampanti
│   └── service-desk/SKILL.md # Helpdesk, ticketing, training utenti
├── gatekeeper/
│   └── SKILL.md              # Security Gatekeeper (review/approva/nega)
├── api/
│   ├── server.py             # FastAPI server per gestione remota
│   └── it-team-api.service   # Systemd unit per demone
├── assessment/
│   └── interview-guide.md    # Guida intervista per assessment iniziale
├── docs/
│   └── model-budget-analysis.md # Analisi modelli AI per budget
└── scripts/
    ├── deploy-skills.sh      # Installa tutti gli skill in Hermes
    └── new-engagement.sh     # Avvia un nuovo engagement
```

## Come si usa

### 1. Installazione

```bash
cd ~/it-team-framework
chmod +x scripts/*.sh
./scripts/deploy-skills.sh
```

### 2. Nuovo Engagement

```bash
hermes chat
# Carica lo skill orchestrator: /skill it-team-orchestrator
# Oppure usa lo script:
./scripts/new-engagement.sh "Azienda Srl" --size 50 --sector manufacturing
```

### 3. Flusso di Lavoro

L'orchestrator segue queste fasi:

| Fase | Azione | Agenti Coinvolti |
|------|--------|------------------|
| **Intake** | Raccolta dati aziendali (dipendenti, settore, stack IT) | Orchestrator |
| **Assessment** | Analisi stato corrente per ogni dominio | Tutti (parallelo) |
| **Gate Review** | Security gatekeeper approva/nega ogni raccomandazione | Security Gatekeeper |
| **GAP Analysis** | Confronto AS-IS vs BEST PRACTICES (solo rec approvate) | Orchestrator |
| **Roadmap** | Piano priorizzato con tempi e costi | Orchestrator |
| **Execution** | Implementazione miglioramenti | Specialisti assegnati |
| **Review** | Verifica KPI e report finale | Orchestrator |

### 4. Privacy

**Attenzione**: i dati inseriti nei prompt (intake, assessment) transitano via OpenRouter verso i provider dei modelli. Il framework mitiga così:
- Non inserire mai password, secret o dati personali nei prompt (vedi Common Pitfalls dell'orchestrator)
- Assessment template locali (nessun upload di file esterni)
- Report generati e salvati localmente
- Per data-residency UE o privacy totale, usa modelli locali (vedi `docs/model-budget-analysis.md`)

## Ruoli del Team IT

| Ruolo | Agente | Competenze Chiave |
|-------|--------|-------------------|
| **CTO/IT Manager** | Orchestrator | Strategia, coordinamento, prioritizzazione |
| **CISO/IT Auditor** | Security Gatekeeper | Gate review trasversale: approva/nega ogni raccomandazione |
| **Sysadmin Senior** | OS & Infra | Server, AD, patch, virtualization |
| **Cloud Architect** | Cloud | IaaS/PaaS, migration, FinOps |
| **Application Manager** | Applications | CRM, ERP, integrations, lifecycle |
| **Security Engineer** | Security | Assessment sicurezza, SIEM, incident response, GDPR |
| **Network Engineer** | Network | LAN/WAN, firewall, VPN, SD-WAN |
| **Storage & DR Admin** | Data | Backup, disaster recovery, analytics |
| **IT Procurement** | Budget & Procurement | Vendor management, licensing, CAPEX/OPEX |
| **Endpoint Engineer** | Endpoints | MDM, SOE, mobile, patch client |
| **IT Support Lead** | Service Desk | Ticketing, SLA, knowledge base, training |

## Esempio di Engagement

```bash
# 1. Carica orchestrator
hermes chat -q "Carica skill it-team-orchestrator. Nuovo engagement per azienda di 100 dipendenti, settore logistica, stack IT: AD on-prem, Office 365, 3 server VMware, backup NAS, firewall Fortinet."

# 2. L'orchestrator farà:
#    - Assessment parallelo di tutti i domini
#    - Report gap analysis
#    - Roadmap 6-12 mesi
#    - Budget stimato per migliorie

# 3. Approvata la roadmap, esegue:
hermes chat -q "Esegui fase 1 della roadmap: aggiornamento AD a Azure AD Connect e backup automation"
```

## API di Gestione (opzionale)

`api/server.py` espone una API FastAPI per tracciare engagement, raccomandazioni, gate review e roadmap (SQLite locale).

```bash
pip install fastapi uvicorn
uvicorn server:app --host 127.0.0.1 --port 8080   # da api/
# oppure come demone: cp api/it-team-api.service /etc/systemd/system/ && systemctl enable --now it-team-api
```

Endpoint principali: `POST /engagements`, `POST /engagements/{id}/assess`, `GET /engagements/{id}/recommendations`, `POST /engagements/{id}/gate-review`, `POST /engagements/{id}/gate-review/{rec_id}/decision`, `GET /engagements/{id}/roadmap`, `POST /engagements/{id}/execute`, `GET /health`.

L'API non ha autenticazione di default: impostare `IT_TEAM_API_KEY` per richiedere un Bearer token, e non esporla su interfacce pubbliche.

## Versioning

Il progetto segue Semantic Versioning (`MAJOR.MINOR.PATCH`). La versione corrente è in `VERSION`.

```bash
# Verifica versione
cat VERSION

# Crea un tag di release dopo le verifiche
git add .
git commit -m "release: v$(tr -d "\n" < VERSION)"
git tag -a "v$(tr -d "\n" < VERSION)" -m "IT Team Framework v$(tr -d "\n" < VERSION)"
```

Le modifiche devono essere registrate in `CHANGELOG.md`. Non committare database, secret, ambienti virtuali o report temporanei.

## Requisiti

- Hermes Agent v0.19+
- Modello orchestratore: deepseek/deepseek-v4-flash o superiore
- Modello worker: inclusionai/ling-2.6-flash ($0.10/M input, $0.30/M output — vedi `docs/model-budget-analysis.md`)
- Budget: ~$0.50-2.00/engagement completo (dipende dalla complessità)