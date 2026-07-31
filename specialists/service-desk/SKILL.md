---
name: it-team-service-desk
description: 'Use when assessing or improving IT service desk operations. ITIL processes + ticketing + SLA management + knowledge base + user training.'
category: service-desk
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [service-desk, ITIL, ticketing, SLA, knowledge-base, training, onboarding-offboarding, IT-asset-management, self-service-portal, incident-problem-change]
    related_skills: [it-team-endpoints, it-team-applications]
---

# Service Desk & Support — Specialista IT (it-team-service-desk)

Questa skill fornisce un protocollo strutturato per valutare, migliorare e operare un service desk IT allineato agli standard ITIL, con integrazione ticketing (ServiceNow, Jira, Zendesk, Freshservice), gestione SLA/SLO, knowledge base, formazione, onboarding/offboarding, IT asset management e self-service.

## 🎯 Obiettivi della skill

- Valutare lo stato maturo del service desk e dei processi ITIL.
- Misurare KPI critici: volume ticket, SLA adherence, First Response Time (FRT), Time to Resolution (TTR), CSAT, knowledge base coverage.
- Definire e tracciare miglioramenti su ticketing, knowledge base, SLA, automazioni e formazione.
- Supportare l’integrazione con tool di ticketing e asset management.

## 📋 Assessment Protocol

Esegui una valutazione completa con i seguenti checkpoint. Usa strumenti a tua scelta (API ticketing, report, interviste, sondaggi).

### 1. Ticket Volume & Trends
- Estrai volume giornaliero/settimanale/mensile e trend.
- Analisi per categoria, priorità, canale (email, web, telefono, chat).
- Picchi stagionali, crescita o cali anomali.

### 2. SLA / SLO Adherence
- Percentuale di ticket rispettati SLA per categoria/priorità.
- SLA breach rate e root cause dei ritardi.
- Allineamento con obiettivi SLO (es. risoluzione entro 24/48/72 ore).

### 3. First Response Time (FRT)
- Media e distribuzione del tempo prima della prima risposta.
- Confronto con target (es. <2 ore per critiche/alte, <24 ore per medie/basse).

### 4. Time to Resolution (TTR)
- Media e distribuzione del tempo di chiusura.
- TTR per categoria/problema noto.

### 5. CSAT (Customer Satisfaction)
- Media sondaggi post-intervento.
- Distribuzione tra very satisfied, satisfied, neutral, dissatisfied, very dissatisfied.
- Commenti free text per temi ricorrenti.

### 6. Knowledge Base Coverage
- Percentuale di ticket con articoli KB collegati/inseriti.
- Numero totale articoli, frequenza d’uso (search hits), tasso di auto-servizio.
- Qualità: accuratezza, aggiornamento, copertura temi frequenti.

### 7. ITIL Process Maturity
- Valutazione a maturità (0–3 o 0–5) per: Incidente, Problema, Cambiamento, Richiesta di Servizio, Release.
- Documentazione, ruoli, responsabilità, workflow, registri (RFC, Problem, Known Error).

### 8. Onboarding / Offboarding Workflow
- Tempo medio per attivare/revocare accessi, account, licenze.
- Completezza checklist (hardware, software, email, SSO, autorizzazioni).
- Esperienza utente e feedback dipendenti.

### 9. IT Asset Management
- Accuratezza inventario (hardware/software/licenze).
- Lifecycle, manutenzione, smaltimento.
- Allineamento a policy licenze e compliance.

## 🚀 Improvement Catalog

Priorizza in base ai risultati dell’Assessment. Ecco possibili interventi:

### 1. ITIL Process Implementation
- Definire chiaramente processi: ricezione, classificazione, assegnazione, SLA, escalation, chiusura.
- Implementare registri e RACI.
- Stabilire cadenze (daily triage, weekly review SLA).

### 2. Knowledge Base Creation & Optimization
- Struttura categorica, template articoli, proprietario contenuto.
- Integrazione con ticketing: suggerimento KB al momento della creazione.
- Governance: review periodica, versionamento, KPIs (tasso uso, auto-servizio).

### 3. Self-Service Portal
- Catalogo servizi self-service, modulo richiesta, stato ticket.
- Accesso integrato a conoscenze, FAQ, form.
- Misurare tasso di adozione e riduzione carico su agenti.

### 4. SLA / SLO Tuning
- Definire target realistici per ciascuna categoria/priorità.
- Automazione escalation in base a SLA breach.
- Dashboard in tempo reale SLA adherence.

### 5. Chatbot Integration
- Bot per FAQ, triage iniziale, ricerca KB, creazione ticket.
- Fallback chiaro a agente umano.
- Misurare FRT ridotto, tasso di risoluzione bot, soddisfazione.

### 6. Automated Onboarding / Offboarding
- Moduli di compilazione, integrazione con HRIS/Active Directory/SSO.
- Workflow approvazioni, checklist, notifiche.
- Misurare time-to-produttività e completezza.

### 7. Training Program
- Percorsi formativi: ITIL basics, tool ticketing, KB authoring, soft skills.
- Formazione new hire, refresh periodico, certificazioni.
- Valutazione competenze pre/post training.

### 8. IT Asset Management Enhancements
- Automazione discovery, integrazione CMDB, licenze monitoraggio.
- Policy di riordino, smaltimento sicuro, report compliance.

## 📐 Implementation Guide

### Fase 1: Scoperta e Baseline (2–4 settimane)
- Esegui Assessment Protocol su tutti i punti.
- Definisci baseline KPI e target.
- Coinvolgi stakeholder: Helpdesk, IT, HR, Security, Fornitori.

### Fase 2: Progettazione e Pianificazione (2–3 settimane)
- Prioritizza miglioramenti con RICE/WSJF.
- Definisci roadmap, MVP, milestone e owner.
- Stima risorse, budget, tempi.

### Fase 3: Implementazione (4–12 settimane a seconda dell’ambito)
- Configura/ottimizza ticketing (campi, SLA, workflow, automazioni).
- Crea/modifica KB e implementa integrazione ticket.
- Lancia self-service portal e/o chatbot su ambiti contenuti.
- Attiva automated onboarding/offboarding con HRIS/AD.
- Lancia programmi di training.

### Fase 4: Test, Pilota, Misura
- Pilota su piccolo gruppo, raccogli feedback.
- Monitora KPI: SLA adherence, FRT, TTR, CSAT, KB usage, time-to-prod.
- Apprendi e itera.

### Fase 5: Roll-out e Governance
- Roll-out graduale o completo a seconda dei risultati.
- Definisci Governance: proprietari KB, review SLA, gestione ticket, change control.
- Dashboard e report periodici.

### Fase 6: Mantenimento e Maturità
- Audit trimestrali ITIL e processi.
- Evoluzione KB e self-service.
- Ottimizzazione continuo SLO/SLA in base al carico e necessità.

## 🛠 Strumenti & Integrazioni Consigliati

- Ticketing: ServiceNow, Jira Service Management, Zendesk, Freshservice.
- Knowledge Base: soluzione integrata al ticketing o KB dedicato (es. Confluence).
- SSO & Access: Azure AD, Okta, Google Workspace.
- Asset Management: ServiceNow CMDB, Lansweeper, Snipe-IT.
- Self-service/Portal: soluzione integrata o custom.
- Chatbot: Soluzioni native (Zendesk Answer Bot, Freshservice Freddy) o Bot costruito su LLM con guardrails.
- Analytics/BI: Power BI, Tableau, Looker o report nativi ticketing.

## 📊 KPI di Riferimento (target indicativi)

- SLA adherence ≥95% (SLA critiche), ≥98% (SLA alte/basse).
- FRT <2 ore (critico), <24 ore (alto), <48 ore (medio/basso).
- TTR <48 ore (critico), <72 ore (alto), <120 ore (medio/basso) — da aggiustare per categoria.
- CSAT ≥85% satisfied/very satisfied.
- KB coverage ≥70% ticket con KB collegato; tasso uso auto-servizio ≥30%.
- Onboarding attivato ≤3 giorni; offboarding revoche entro 24 ore da richiesta.

## ⚠️ Note & Best Practices

- Allineare SLA con business needs; evitare target non raggiungibili che generano insoddisfazione.
- Mantenere KB semplice, cercabile, aggiornato; assegnare proprietario.
- Monitorare in continuazione i trend di volume e breaching per interventi proattivi.
- Coinvolgere gli utenti finali in test e feedback.
- Documentare processi e responsabilità (RACI) e comunicarli chiaramente.

## 📅 Esempio di Roadmap (M3)

- Settimana 1–2: Assessment e baseline KPI.
- Settimana 3–4: Progettazione KB e SLA tuning.
- Settimana 5–8: Implementazione ticketing avanzato, KB management, primo pilota chatbot.
- Settimana 9–12: Roll-out self-service portal, onboarding automation, training program.
- Settimana 13+: Governance, monitoraggio continuo, miglioramenti iterativi.

---
*Skills correlate: [it-team-service-desk] può essere integrata con skills di [autonomous-ai-agents] per chatbot/agenti virtuali e [hermes-ops] per operazioni e cost monitoring.*

---

## Output Contract

All specialist assessments produce structured deliverables:

| Deliverable | Format | Audience |
|---|---|---|
| Executive Summary | 1-page markdown or PDF | Leadership, C-suite |
| Findings Register | Table with severity and effort | IT Manager, Technical Leads |
| Recommendations Backlog | Prioritized list (impact × effort) | Project team |
| Metrics Dashboard | KPI values vs. targets | Ongoing governance |

## Severity Levels

| Level | Definition | SLA |
|---|---|---|
| **CRITICAL** | Immediate risk to operations, data, or compliance | Action within 48 h |
| **HIGH** | Significant impact; degrades service or increases risk | Action within 30 days |
| **MEDIUM** | Moderate impact; optimization or compliance gap | Plan within 90 days |
| **LOW** | Minor improvement opportunity | Backlog |
| **Info** | Observation, best practice, or FYI | Documented |

## Privacy & Data Handling

- Assessment data classified per organization policy (public / internal / confidential / restricted).
- PII in findings must be redacted or anonymized in all deliverables.
- Reports stored only in approved repositories or encrypted shares.
- Credentials, secrets, and API keys must never appear in deliverables.
- Comply with GDPR, HIPAA, SOX, and local regulations where applicable.
- Data retention follows organization retention schedule; dispose per policy.
