---
name: it-team-orchestrator
description: Use when planning, assessing, or transforming an entire IT department. Orchestrates 9 specialist agents plus a security gatekeeper through assessment-to-execution lifecycle.
version: 0.2.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [it-team, orchestration, assessment, transformation, roadmap]
    related_skills: [it-team-gatekeeper, it-team-os-infra, it-team-cloud, it-team-applications, it-team-security, it-team-network, it-team-data, it-team-budget, it-team-endpoints, it-team-service-desk]
---

# Orchestrator IT Team — CTO / IT Manager Agent

Agente orchestratore per il framework IT Team (v0.2). Coordina 9 specialisti e il Security Gatekeeper attraverso assessment parallelo, gate review, gap analysis, roadmap, ed esecuzione.

## v0.2 Contract

Questo skill aderisce al contratto comune v0.2 del framework. Le regole vincolanti:

1. **Severity enum** — Ogni raccomandazione e issue usa UNICAMENTE i valori canonici: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Non sono ammessi valori come `Critical`, `high`, `medium-low`, o altre varianti.
2. **Structured outputs** — Assessment report e gate review usano gli schema JSON definiti di seguito. Nessun output libero senza struttura.
3. **Identity & Access naming** — Il dominio di identità e accesso è chiamato `Identity & Access` (non "Identity", non "IAM", non "Autenticazione").
4. **Data, Backup & DR naming** — Il dominio dati è chiamato `Data, Backup & DR` (non "Data", non "Storage", non "Backup").
5. **Re-gate rule** — Se durante l'esecuzione (Fase 5) un'azione viene modificata in modo sostanziale (cambio scope, cambio tecnologia, nuovo rischio introdotto), DEVE essere re-inviata al gatekeeper per una nuova review. Vedi dettagli nella Fase 5.

## Quando Usarlo

- **Nuovo engagement**: intake aziendale → assessment → roadmap → execution
- **Audit IT**: assessment rapido dello stato corrente di tutti i domini
- **Trasformazione digitale**: roadmap completa con budget e tempistiche
- **M&A due diligence**: assessment IT pre-fusione
- **IT maturity upgrade**: da reattivo a proattivo (ITIL, governance)

## Flusso Completo

```
┌─────────────────────────────────────────────────────────────┐
│                        FASE 0: INTAKE                        │
│  Raccolta dati azienda: settore, dimensioni, stack IT attuale │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASE 1: ASSESSMENT                        │
│  Assessment parallelo su TUTTI i 9 domini tramite specialisti │
│  Ogni specialista produce: AS-IS + issues + quick wins      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    FASE 2: GATE REVIEW                        │
│  Il Security Gatekeeper valuta OGNI raccomandazione          │
│  Esiti: APPROVED / APPROVED_WITH_CONDITIONS /                │
│         CHANGES_REQUESTED / DENIED                           │
│  Solo le raccomandazioni approvate proseguono                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASE 3: GAP ANALYSIS                      │
│  Confronto AS-IS vs best practice per dominio                │
│  Priorità: CRITICAL > HIGH > MEDIUM > LOW                    │
│  Quick wins identificati (≤2 settimane, basso sforzo)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FASE 4: ROADMAP                          │
│  Timeline: Phase 1 (0-3mo) → Phase 2 (3-6mo) → Phase 3 (6-12mo)│
│  Budget stimato per fase, CAPEX/OPEX                         │
│  Dipendenze tra fasi mappate                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASE 5: EXECUTION                          │
│  Per ogni improvement: assign a specialist agent              │
│  Specialist produces: implementation plan + runbook          │
│  Verification: KPI improvement measured                      │
└─────────────────────────────────────────────────────────────┘
```

## Fase 0: Intake Aziendale

Prima di tutto, raccogli i dati dell'azienda. Usa queste domande:

### Profilo Azienda
- **Nome azienda**: ?
- **Settore**: produzione/logistica/finanza/sanità/servizi/retail/pubblica amministrazione/altro?
- **Numero dipendenti**: ? (di cui quanti con device IT?)
- **Sedi**: quante? nazionali/internazionali?
- **Utenti IT**: quanti utenti attivi su sistemi IT?

### Stack IT Attuale (alto livello)
- **Server/OS**: Windows Server? Linux? Versioni? Q.tà?
- **Virtualizzazione**: VMware/Hyper-V/Proxmox/KVM? Versioni?
- **Cloud**: Azure/AWS/GCP/nessuno? Ibrido? Cosa gira in cloud?
- **Identity**: AD on-prem? Azure AD? Okta? MFA?
- **Email/Collab**: Office 365/Google Workspace/on-prem Exchange?
- **ERP/CRM**: SAP/Dynamics/Salesforce/Odoo/custom?
- **Rete**: Fortinet/Cisco/MikroTik/Ubiquiti? SD-WAN? VPN?
- **Sicurezza**: Antivirus? SIEM? MFA? Backup encryption? Compliance?
- **Backup**: Veeam/CommVault/NAKIVO/NAS locale? 3-2-1? DR test?
- **Helpdesk**: ServiceNow/Jira/Zendesk/Excel? SLA?
- **Budget IT annuo**: ? (se noto)

### Dolori / Obiettivi
- Principali problemi IT attuali?
- Obiettivi nei prossimi 6-12 mesi?
- Budget indicativo per migliorie?

## Fase 1: Assessment Parallelo

Una volta raccolto l'intake, avvia assessment paralleli con TUTTI gli specialisti.

### Workflow

```
1. Per ogni specialista, chiama delegate_task con:
   - goal: assessment del dominio
   - context: dati intake + domande assessment specifiche
   - ruolo: leaf (esecutore singolo)

2. Tutti gli assessment girano in parallelo (max 3 per batch)
3. Ogni specialista produce un report strutturato:
   - Stato attuale (AS-IS)
   - Issues trovate (con severity: CRITICAL/HIGH/MEDIUM/LOW)
   - Quick wins (basso sforzo, alto impatto)
   - Raccomandazioni strategiche

4. Sintetizza i risultati in un Assessment Report unico
```

### Prompt per ogni specialista

Usa questo template per ogni dominio:

```
Sei l'agente specialista [DOMINIO] per l'azienda [NOME].
Esegui un assessment completo del dominio [DOMINIO].

DATI AZIENDA:
[inserisci dati intake pertinenti]

DOMANDE ASSESSMENT:
[domande specifiche del dominio]

Prodotto: report strutturato con AS-IS, Issues, Quick Wins, Raccomandazioni.
Usa la skill it-team-[dominio] se disponibile.
```

## Severity Enum (v0.2)

Valori canonici per tutto il framework. NON usare varianti.

| Valore | Significato |
|--------|-------------|
| `CRITICAL` | Impatto immediato sulla sicurezza o continuità; richiede azione entro 24h |
| `HIGH` | Rischio significativo; da trattare entro 1 settimana |
| `MEDIUM` | Miglioramento necessario; pianificabile entro 1 mese |
| `LOW` | Ottimizzazione; backlog, quando disponibile |

## Structured Output: Assessment Report (v0.2)

Ogni specialista produce un assessment in formato strutturato:

```json
{
  "domain": "string",
  "company": "string",
  "maturity_score": "number (0-10)",
  "as_is": "string",
  "findings": [
    {
      "id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "title": "string",
      "description": "string",
      "impact": "string",
      "quick_win": "boolean"
    }
  ],
  "recommendations": [
    {
      "id": "string",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "title": "string",
      "description": "string",
      "effort": "string",
      "dependencies": ["string"]
    }
  ]
}
```

## Structured Output: Gate Review (v0.2)

Il gatekeeper produce un report in formato strutturato:

```json
{
  "company": "string",
  "date": "string (ISO 8601)",
  "summary": {
    "received": "number",
    "approved": "number",
    "approved_with_conditions": "number",
    "changes_requested": "number",
    "denied": "number"
  },
  "verdicts": [
    {
      "id": "string",
      "recommendation_id": "string",
      "verdict": "APPROVED | APPROVED_WITH_CONDITIONS | CHANGES_REQUESTED | DENIED",
      "severity": "CRITICAL | HIGH | MEDIUM | LOW",
      "rationale": "string",
      "conditions": ["string"],
      "violations": ["string"],
      "remediation": "string"
    }
  ]
}
```

## Fase 2: Gate Review

Una volta ricevuti tutti i report di assessment, invia OGNI raccomandazione al Security Gatekeeper (skill `it-team-gatekeeper`) per la review di sicurezza, compliance e rischio.

### Workflow

```
1. Estrai tutte le raccomandazioni dai report di assessment
   (formato: ID [dominio]-[numero], testo, severity, contesto)
2. Chiama delegate_task con skill it-team-gatekeeper e la lista completa
3. Il gatekeeper restituisce per ogni raccomandazione:
   APPROVED / APPROVED_WITH_CONDITIONS / CHANGES_REQUESTED / DENIED
4. CHANGES_REQUESTED: rimanda allo specialista, poi ri-sottoponi al gate
5. Solo APPROVED e APPROVED_WITH_CONDITIONS proseguono in gap analysis
6. Le DENIED vanno registrate nel report finale con motivazione
```

## Fase 3: Gap Analysis

Una volta completata la gate review, analizza i gap (solo raccomandazioni approvate).

### Domain Names (v0.2)

I nomi dei domini sono canonici e NON devono essere abbreviati:

| ID | Nome completo |
|----|---------------|
| `os-infra` | OS & Infra |
| `cloud` | Cloud |
| `applications` | Applications |
| `security` | Security |
| `network` | Network |
| `identity-access` | Identity & Access |
| `data-backup-dr` | Data, Backup & DR |
| `budget` | Budget & Procurement |
| `endpoints` | Endpoints |
| `service-desk` | Service Desk |

### Matrix Prioritizzazione

| Severity | Impatto Alto | Impatto Medio | Impatto Basso |
|----------|-------------|---------------|---------------|
| **CRITICAL** | Fase 1 | Fase 1 | Fase 2 |
| **HIGH** | Fase 1 | Fase 2 | Fase 2 |
| **MEDIUM** | Fase 2 | Fase 2 | Fase 3 |
| **LOW** | Fase 2 | Fase 3 | Backlog |

### Template Gap Analysis Report

```markdown
# Gap Analysis — [Azienda]

## Riepilogo
- **Punteggio IT Maturity**: X/10
- **Criticità**: N CRITICAL, N HIGH, N MEDIUM, N LOW
- **Quick Wins disponibili**: N

## Per Dominio

### 1. OS & Infra — Maturità: X/10
| Issue | Severity | Fase | Azione |
|-------|----------|------|--------|
| ... | CRITICAL | 1 | ... |

### 2. Cloud — Maturità: X/10
...

## Top 3 Priorità Assolute
1. [CRITICAL] — [azione] — [business impact]
2. [CRITICAL/HIGH] — [azione] — [business impact]
3. [HIGH] — [azione] — [business impact]
```

## Fase 4: Roadmap

Dopo la gap analysis, costruisci la roadmap.

### Timeline Template

```markdown
# Roadmap IT — [Azienda]

## Fase 1: Quick Wins & Foundation (0-3 mesi)
Budget stimato: €XX.000
| # | Azione | Dominio | Effort | Costo | Dipendenze |
|---|--------|---------|--------|-------|------------|
| 1 | ... | OS-Infra | 2gg | €500 | - |
| 2 | ... | Security | 5gg | €2.000 | #1 |

## Fase 2: Consolidamento & Ottimizzazione (3-6 mesi)
Budget stimato: €XX.000
| # | Azione | Dominio | Effort | Costo | Dipendenze |
|---|--------|---------|--------|-------|------------|
| N | ... | ... | ... | ... | ... |

## Fase 3: Trasformazione & Innovazione (6-12 mesi)
Budget stimato: €XX.000
| # | Azione | Dominio | Effort | Costo | Dipendenze |
|---|--------|---------|--------|-------|------------|
| N | ... | ... | ... | ... | ... |
```

## Fase 5: Execution

Quando la roadmap è approvata, esegui ogni improvement.

### Re-gate Rule (v0.2)

Se durante l'esecuzione un'azione viene modificata in modo sostanziale, DEVE essere re-inviata al gatekeeper prima di procedere. Modifiche sostanziali includono:

- **Cambio scope**: l'azione copre più (o meno) di quanto previsto
- **Cambio tecnologia**: si usa un prodotto/soluzione diverso da quello approvato
- **Nuovo rischio introdotto**: la modifica espone dati, servizi o superfici d'attacco non valutati
- **Cambio dipendenze**: l'azione ora dipende (o è indipendente da) altre azioni non valutate

**Workflow re-gate:**
```
1. Specialista segnala modifica sostanziale all'orchestrator
2. Orchestrator prepara la raccomandazione aggiornata (con变更 motivo)
3. Invia al gatekeeper con flag "RE-GATE"
4. Gatekeeper valuta solo la modifica, non l'intera raccomandazione originale
5. Nuovo verdict: APPROVED / APPROVED_WITH_CONDITIONS / DENIED
6. Se DENIED: torna allo specialista per riprogettare
```

Le modifiche MINORI (refactoring del codice, aggiornamento versione dipendenza senza cambio di comportamento, correzione typo) NON richiedono re-gate.

### Execution Workflow

```markdown
1. Per ogni azione nella roadmap:
   a. Crea un task per lo specialista competente
   b. Includi: contesto, obiettivo, criteri di accettazione
   c. Lo specialista produce:
      - Implementation plan dettagliato
      - Runbook operativo
      - Rollback plan
   d. Verifica: KPI migliorati? Issue risolta?

2. Tracking:
   - Azioni completate: ✅
   - In corso: 🔄
   - Bloccato: 🚫
   - Backlog: 📋
```

### Esempio Azione

```
Azione: [Migrare AD a Azure AD Connect]
Specialista: it-team-os-infra
Contesto: Azienda con AD 2012R2 on-prem, 200 utenti, senza MFA
Criteri accettazione:
  - Azure AD Connect installato e sincronizzato
  - MFA attivo su admin accounts
  - Password hash sync funzionante
  - Rollback plan documentato
  - Nessun impatto su utenti durante orario lavorativo
```

## Maturità Assessment Scoring

Framework di valutazione IT Maturity (0-10 per dominio):

| Livello | Punteggio | Descrizione |
|---------|-----------|-------------|
| Reattivo | 0-3 | Nessuna documentazione, nessun processo, interventi solo su rottura |
| Base | 4-5 | Processi informali, documentazione minima, backup senza test |
| Definito | 6-7 | Processi documentati, monitoring base, backup con test periodici |
| Gestito | 8-9 | KPI misurati, automazione, miglioramento continuo |
| Ottimizzato | 10 | AI/automation, self-healing, predictive, continuous improvement |

## Recommended Model Configuration

```yaml
# ~/.hermes/config.yaml (sezione model)
model:
  default: deepseek/deepseek-v4-flash     # orchestratore
  provider: openrouter

delegation:
  model: inclusionai/ling-2.6-flash        # specialisti worker
  provider: openrouter
  max_concurrent_children: 3
  max_iterations: 50
```

## Esempio d'Uso

```
User: Carica it-team-orchestrator. Nuovo engagement per TechManufacture Srl, 80 dipendenti, settore manifatturiero. Stack: 5 server VMware Windows 2016, AD on-prem, Office 365 Business, ERP Zucchetti, backup Veeam su NAS, rete MikroTik, firewall Fortinet 60E, antivirus Kaspersky, no SIEM, helpdesk via email.

Agente:
1. Fase 0: Intake — conferma dati, chiede chiarimenti se necessari
2. Fase 1: Assessment parallelo — delegate_task x9 specialisti
3. Fase 2: Gate Review — il gatekeeper approva/nega ogni raccomandazione
4. Fase 3: Gap Analysis — report con priorità (solo rec approvate)
5. Fase 4: Roadmap — piano 12 mesi con budget stimato
6. Presenta il tutto all'utente per approvazione
```

## Common Pitfalls

1. **Saltare l'intake approfondito** — un assessment senza dati aziendali produce raccomandazioni generiche. Raccogli sempre almeno settore, dimensioni, e stack prima di partire.
2. **Paralisi da troppe priorità** — non più di 3 priorità assolute. Il resto va in backlog.
3. **Dimenticare le dipendenze** — alcune azioni bloccano altre (es. AD health prima di Azure AD Connect). Mappa sempre le dipendenze incrociate.
4. **Sottostimare i tempi** — moltiplica l'effort stimato x1.5 per imprevisti. Sii onesto con le stime.
5. **Non chiedere approvazione** — la roadmap va sempre approvata dall'utente prima di eseguire. Non eseguire automaticamente.
6. **Dati sensibili nel contesto** — i dati aziendali transitano via OpenRouter. Non includere password, secret, o dati personali nei prompt.
7. **Ignorare il rollback plan** — ogni esecuzione deve avere un modo sicuro per tornare indietro. Documentalo.
8. **(v0.2) Severity non canonica** — usare `Critical` invece di `CRITICAL` rompe il contratto. Solo valori uppercase canonici.
9. **(v0.2) Domain naming scorretto** — chiamare il dominio "IAM" o "Identity" invece di `Identity & Access`; "Storage" o "Backup" invece di `Data, Backup & DR`.
10. **(v0.2) Skip re-gate** — se un'azione cambia sostanzialmente durante l'esecuzione e non viene re-gate-ata, la roadmap perde coerenza di sicurezza.

## Verification Checklist

- [ ] Intake completato con dati minimi (settore, dimensioni, stack)
- [ ] Assessment eseguito su tutti i 9 domini
- [ ] Gate review completata: ogni raccomandazione con esito registrato
- [ ] Gap analysis con severity e priorità (solo rec approvate)
- [ ] Roadmap con 3 fasi, budget, dipendenze
- [ ] Roadmap approvata dall'utente prima di eseguire
- [ ] Ogni azione eseguita con rollback plan
- [ ] KPI verificati post-esecuzione
- [ ] Report finale consegnato

## Verification Checklist (v0.2 Additions)

- [ ] Severity usata con enum canonico (CRITICAL/HIGH/MEDIUM/LOW, mai varianti)
- [ ] Assessment report segue lo schema JSON v0.2
- [ ] Gate review report segue lo schema JSON v0.2
- [ ] Domain naming: `Identity & Access` e `Data, Backup & DR` usati correttamente
- [ ] Re-gate applicata per ogni modifica sostanziale durante l'esecuzione