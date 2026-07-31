---
name: it-team-applications
description: 'Use when assessing or improving enterprise applications portfolio. App rationalization + integration patterns + lifecycle management.'
category: applications
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [applications, saas, api-integration, rationalization, vendor-health, code-quality, microservices]
    related_skills: [it-team-cloud, it-team-service-desk, it-team-budget]
---

# Specialista Applicativi — Application Manager (it-team-applications)

# Assessment Protocol

## 1. Inventario Applicativo
- **Nome e descrizione**: identificativo univoco, business owner, contesto ( produzione / pre-produzione / sviluppo ).
- **Tipologia**: CRM, ERP, SaaS, custom application, integration layer, tooling interno.
- **Stato**: in produzione, in manutenzione, deprecato, candidato alla rimozione.
- **Mappa dei flussi**: principali use-case e processi di business supportati.
- **Documentazione**: dove sono archiviati manuali, runbook, API docs, diagrammi di architettura.

## 2. Versioni
- **Versione corrente**: numero di versione o tag (es. 2024.1.0).
- **Storia delle versioni**: cronologia degli upgrade, release note per ogni major/minor.
- **Ecosystem di componenti**: librerie, framework, container, database driver versions.
- **Patti di versionamento**: semantic versioning, date based, internal numbering.
- **Allineamento**: versioni critiche allineate su ambienti (dev / test / prod).

## 3. Licenze
- **Modello di licensing**: perpetual, subscription, consumptive, core-based, user-based.
- **Entità licenziate**: numero di core, socket, utenti, dispositivi.
- **Scadenze e rinnovi**: date di scadenza, reminder, processo di rinnovo / acquisto.
- **Conformità**: controllo quote, audit periodici, report vendor.
- **Gestione emergenze**: procedure per upgrade urgente o variazione di carico.

## 4. Integrazioni
- **Endpoint e contatti**: API URLs, webhook, SFTP, messaggistica ( Kafka / RabbitMQ ), service bus.
- **Protocolli e formati**: REST / GraphQL / SOAP, JSON / XML / gRPC, payload size limits.
- **Autenticazione e autorizzazione**: API keys, OAuth2 / OIDC, mTLS, certificati, segreti gestiti.
- **SLA e QoS**: tempi di risposta, rate limits, retry policy, timeout, backoff.
- **Error handling**: codici di errore, pattern di fallback, dead-letter queue, logging delle eccezioni.
- **Monitoraggio integrato**: metriche di traffico, errori, latenze, dimensioni code.

## 5. Vendor Health
- **Stato del vendor**: financial health, roadmap, fusioni/acquisizioni, annunci strategici.
- **Supporto e servizi**: disponibilità di TAM, tempi di risposta, SLA contrattuali.
- **Comunità e ecosistema**: forums, eventi, partner network, certificazioni.
- **Rischi**: dipendenza singola fonte, lock-in, interruzioni del servizio, policy di privacy.
- **Piani di contingenza**: exit strategy, migrazione off vendor, dati escrow.

## 6. Custom Code Quality
- **Architettura**: clean architecture, separazione preoccupazioni, layers chiari (domain / application / infrastructure).
- **Code quality**: linting, formattazione, analisi statica, cyclomatic complexity, code smells.
- **Test**: coverage unit test, test di integrazione, test end-to-end, test di carico, strategy di test data.
- **Build & CI/CD**: pipeline di release, automazione, gating, approvazioni, rollback.
- **Security**: SAST / DAST, secret management, dependency scanning, threat modeling.
- **Performance**: benchmark, profiling, carichi previsti, piano di scalabilità.

---

# Improvement Catalog

## 1. Application Rationalization
- **Elimina ridondanze**: applicazioni sovrapposte con funzionalità simili.
- **Consolidamento**: migrazione di carichi di lavoro verso un'unica piattaforma.
- **Decommissioning sicuro**: archiviazione dati, comunicazione agli utenti, procedura di cutover.
- **KPI**: numero di applicazioni ridotto, percentuale di carico spostato, risparmio annuo.

## 2. API-First Integration
- **Design delle API**: contratto chiaro, versioning, documentazione OpenAPI/Swagger.
- **Gateway API**: gestione rate limiting, autenticazione, monitoraggio, caching.
- **Pattern di integrazione**: façade, anti-corruption layer, async messaging, event sourcing.
- **Strumenti**: schema validation, contract testing, mock server per sviluppo.

## 3. SaaS Consolidation
- **Valutazione totale costo di proprietà**: license, custom development, supporto, training.
- **User experience unification**: accesso SSO, esperienza utente coerente.
- **Data residency and compliance**: verifica regioni, certificazioni (SOC 2, ISO 27001).
- **Piano di migrazione**: dati, configurazioni, training, comunicazione.

## 4. Upgrade Planning
- **Roadmap**: versioni target, milestone, rischi e dipendenze.
- **Backwards compatibility**: valutare impatti su custom code e integrazioni.
- **Esecuzione pilot**: gruppo pilota, rollback plan, checklist di go/no-go.
- **Comunicazione**: agenda stakeholder, training, documentazione aggiornata.

## 5. Microservices Assessment
- **Dominio del modello**: bounded context, DDD, decomposizione per business capability.
- **Granularità**: servizi piccoli e autonomi vs monolite frazionato.
- **Data management**: database per servizio, eventuali pattern CQRS / Event Sourcing.
- **OSS e tool**: orchestrator (Kubernetes), service mesh, gestione osservabilità.

---

# Implementation Guide

## Fase 0 — Preparazione
- **Stakeholder**: business owner, IT, security, compliance, finance.
- **Obiettivi**: definire scope, success criteria, KPI, timeline.
- **Strumenti**: inventario condiviso ( foglio / CMDB ), issue tracker, wiki documentazione.

## Fase 1 — Discovery e Inventario
- Eseguire interview con i principali utenti e owners.
- Estrarre liste da CMDB, contratti di licenza, configurazioni CI/CD.
- Validare lo stato attuale con i responsabili delle applicazioni.

## Fase 2 — Valutazione e Prioritizzazione
- Applicare un modello di scoring (ad es. costo + rischio + valore di business).
- Classificare in: mantenere, ottimizzare, consolidare, sostituire, decommissionare.
- Definire backlog delle migliorie con priorità chiare.

## Fase 3 — Progettazione del Miglioramento
- Scegliere pattern di integrazione e target architecture.
- Definire success metrics e criteri di accettazione.
- Creare piani di dettaglio per ogni iniziativa (timeline, risorse, budget).

## Fase 4 — Esecuzione e Migrazione
- Pilot su ambiente limitato, monitoraggio continuo.
- Esecuzione del cutover con rollback ben definito.
- Aggiornamento documentazione e formazione utenti.

## Fase 5 — Operazioni e Ottimizzazione Continua
- Monitoring post-migrazione: SLA, errori, performance.
- Revisione periodica del portfolio (ogni 6-12 mesi).
- Iterare con miglioramenti incremental e technical debt riduzione.

---

# Note e Best Practices
- Mantenere un singolo punto di verità per l'inventario (CMDB / cloud asset inventory).
- Usare contratti API versionati e test di compatibilità.
- Valutare sempre il rischio vendor e avere un piano di contingenza.
- Promuovere cultura della qualità: code review, automated testing, CI/CD.
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

- Coinvolgere gli utenti finali in ogni fase di cambio e validazione del successo.