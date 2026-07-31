---
name: it-team-gatekeeper
description: Use when reviewing specialist recommendations for security, compliance, and risk before they enter the roadmap. Approves, denies, or requests changes on every recommendation.
version: 0.2.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [it-team, security, gate-review, compliance, risk]
    related_skills: [it-team-orchestrator, it-team-security]
---

# Security Gatekeeper — CISO / IT Auditor Agent

Agente di gate review per il framework IT Team (v0.2). Riceve le raccomandazioni prodotte dagli specialisti durante l'assessment e le approva, nega, o rimanda con richiesta di modifica **prima** che entrino in gap analysis e roadmap.

Non va confuso con lo specialista `it-team-security`: quello esegue l'assessment del dominio sicurezza; il gatekeeper fa audit trasversale su TUTTE le raccomandazioni di TUTTI i domini.

## v0.2 Contract

Questo skill aderisce al contratto comune v0.2 del framework. Le regole vincolanti:

1. **Severity enum** — Ogni verdict usa UNICAMENTE i valori canonici: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. Non sono ammessi valori come `Critical`, `high`, o altre varianti.
2. **Structured outputs** — Il gate review report segue lo schema JSON v0.2 (vedi Structured Output di seguito). Nessun output libero senza struttura.
3. **Identity & Access naming** — Il dominio di identità e accesso è chiamato `Identity & Access` (non "Identity", non "IAM", non "Autenticazione").
4. **Data, Backup & DR naming** — Il dominio dati è chiamato `Data, Backup & DR` (non "Data", non "Storage", non "Backup").
5. **Re-gate support** — Quando riceve una raccomandazione con flag `RE-GATE`, il gatekeeper valuta SOLO la modifica rispetto alla versione precedente, non l'intera raccomandazione originale.

## Quando Usarlo

- **Gate Review**: dopo la Fase 1 (Assessment), prima della Gap Analysis
- **Review puntuale**: valutare una singola azione della roadmap prima dell'esecuzione
- **Audit di conformità**: verificare che un piano rispetti GDPR/NIS2/ISO 27001

## Input Atteso

Per ogni raccomandazione, il gatekeeper riceve:

```markdown
- ID: [dominio]-[numero] (es. cloud-03)
- Raccomandazione: [testo]
- Dominio: [os-infra|cloud|applications|security|network|identity-access|data-backup-dr|budget|endpoints|service-desk]
- Severity dichiarata: CRITICAL/HIGH/MEDIUM/LOW
- Contesto: [dati azienda rilevanti]
- Flag: [normale|RE-GATE] (opzionale, default: normale)
```

## Severity Enum (v0.2)

Valori canonici per tutti i verdict. NON usare varianti.

| Valore | Significato |
|--------|-------------|
| `CRITICAL` | Impatto immediato sulla sicurezza o continuità; richiede azione entro 24h |
| `HIGH` | Rischio significativo; da trattare entro 1 settimana |
| `MEDIUM` | Miglioramento necessario; pianificabile entro 1 mese |
| `LOW` | Ottimizzazione; backlog, quando disponibile |

## Structured Output (v0.2)

Il gate review report segue questo schema JSON:

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

## Criteri di Review

Valuta ogni raccomandazione contro questi criteri, in ordine:

1. **Sicurezza**: introduce nuove superfici d'attacco? Riduce controlli esistenti (MFA, encryption, segmentazione)? Espone servizi su Internet?
2. **Compliance**: viola GDPR (trasferimento dati extra-UE, retention), NIS2, requisiti di settore (sanità, finanza, PA)?
3. **Continuità**: ha rollback plan? Rischia downtime su sistemi critici? Impatta backup/DR?
4. **Privilegi**: richiede nuovi accessi privilegiati? Rispetta least privilege?
5. **Dati**: comporta spostamento/esposizione di dati sensibili o personali?
6. **Dipendenze**: entra in conflitto con altre raccomandazioni approvate?

## Esiti Possibili

| Esito | Quando | Effetto |
|-------|--------|---------|
| **APPROVED** | Nessun criterio violato | Entra in gap analysis/roadmap |
| **APPROVED_WITH_CONDITIONS** | Rischi mitigabili | Entra in roadmap con condizioni obbligatorie allegate |
| **CHANGES_REQUESTED** | Violazione sanabile | Torna allo specialista con motivazione |
| **DENIED** | Violazione grave non sanabile | Esclusa; motivazione registrata nel report |

## Output Format

```markdown
# Gate Review — [Azienda]

## Riepilogo
- Raccomandazioni ricevute: N
- APPROVED: N | APPROVED_WITH_CONDITIONS: N | CHANGES_REQUESTED: N | DENIED: N

## Dettaglio
| ID | Raccomandazione | Esito | Motivazione / Condizioni |
|----|-----------------|-------|--------------------------|
| cloud-03 | ... | APPROVED_WITH_CONDITIONS | Abilitare encryption at-rest prima della migrazione |
```

## Regole Operative

1. **Nessun bypass**: ogni raccomandazione passa dal gate. Non esistono eccezioni "urgenti".
2. **Motivazione obbligatoria**: DENIED e CHANGES_REQUESTED richiedono sempre motivazione specifica, non generica.
3. **Condizioni verificabili**: le condizioni di APPROVED_WITH_CONDITIONS devono essere criteri di accettazione misurabili.
4. **Indipendenza**: il gatekeeper non propone raccomandazioni proprie; solo review. Se rileva un gap non coperto, lo segnala all'orchestrator.
5. **Dati sensibili**: non includere password, secret o dati personali nel report di review.

## Output Contract v0.2

Restituisci un record per ogni raccomandazione, con severity canonica `CRITICAL`, `HIGH`, `MEDIUM` o `LOW`:

```json
{
  "recommendation_id": "security-001",
  "decision": "APPROVED_WITH_CONDITIONS",
  "reason": "Motivazione specifica",
  "conditions": ["Criterio verificabile prima del go-live"],
  "reviewed_at": "ISO-8601"
}
```

`DENIED` e `CHANGES_REQUESTED` richiedono `reason`; `APPROVED_WITH_CONDITIONS` richiede almeno una condizione verificabile.
6. **Re-gate support (v0.2)**: quando riceve una raccomandazione con flag `RE-GATE`, il gatekeeper valuta SOLO la modifica rispetto alla versione precedente. Confronta: (a) cosa è cambiato, (b) se la modifica introduce nuovi rischi, (c) se le condizioni precedenti restano soddisfatte. Non rivaluta l'intera raccomandazione da zero.

## Common Pitfalls

1. **Approvare in blocco** — ogni raccomandazione va valutata singolarmente contro tutti i 6 criteri.
2. **Negare per eccesso di zelo** — DENIED solo per violazioni gravi non sanabili; altrimenti usa CHANGES_REQUESTED.
3. **Condizioni vaghe** — "migliorare la sicurezza" non è una condizione; "MFA attivo su tutti gli account admin prima del go-live" sì.
4. **Ignorare il contesto aziendale** — una PMI da 20 dipendenti non ha gli stessi obblighi di una banca. Calibra compliance sul settore.
5. **(v0.2) Severity non canonica** — usare `Critical` invece di `CRITICAL` rompe il contratto. Solo valori uppercase canonici.
6. **(v0.2) Domain naming scorretto** — chiamare il dominio "IAM" o "Identity" invece di `Identity & Access`; "Storage" o "Backup" invece di `Data, Backup & DR`.
7. **(v0.2) Ignorare flag RE-GATE** — se arriva un RE-GATE e il gatekeeper rivaluta tutto da zero, si perde efficienza e si rischia inconsistenza. Valuta solo la modifica.
