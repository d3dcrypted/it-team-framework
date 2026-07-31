# Use case v0.2 — Alfa Logistica Srl

## Obiettivo

Validare il workflow `Intake → Assessment → Gate Review → Roadmap` su una PMI logistica senza eseguire modifiche produttive.

## Contesto sintetico

- 80 dipendenti, 65 utenti IT, 2 sedi
- Operatività 24/7; downtime massimo: 2 ore
- Budget iniziale massimo: 35.000 EUR
- Active Directory on-premise e Microsoft 365
- 4 VM VMware con Windows Server 2016/2019
- ERP business-critical
- Veeam su NAS; restore test completo non eseguito negli ultimi 12 mesi
- Firewall Fortinet e VPN utenti remoti
- Endpoint Windows e helpdesk via email
- MFA non uniforme; nessun SIEM

## Criteri di accettazione

Il test è superato se il report contiene:

1. 9 domini specialistici;
2. fatti confermati, assunzioni e dati mancanti separati;
3. raccomandazioni con ID univoco;
4. severity tra `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`;
5. decisione individuale del gatekeeper;
6. condizioni e rollback verificabili;
7. roadmap entro 35.000 EUR;
8. nessuna esecuzione senza approvazione esplicita.

## Prompt di test

```text
Carica skill it-team-orchestrator.

Avvia un assessment per Alfa Logistica Srl usando il contesto documentato in questo file.
Esegui intake, assessment dei 9 domini, gate review e roadmap a 90 giorni.
Non eseguire modifiche. Se mancano dati, separa chiaramente fatti, assunzioni e unknowns.
Restituisci output strutturati secondo il contratto v0.2.
```
