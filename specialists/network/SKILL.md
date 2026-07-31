---
name: it-team-network
description: 'Use when assessing or improving network infrastructure. LAN/WAN/VPN assessment + firewall rules + SD-WAN + network segmentation + monitoring.'
category: network
version: 1.0.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [network, firewall, sd-wan, segmentation, vpn, wifi, dns-dhcp, monitoring]
    related_skills: [it-team-security, it-team-cloud, it-team-os-infra]
---

# Specialista Rete — Network Engineer (it-team-network)

## Assessment Protocol

Esegui una valutazione completa seguendo questa sequenza. Per ogni punto, verifica e documenta risultati, configurazioni attuali e raccomandazioni.

### 1. Topologia Rete
- Mappa fisica e logica (disegni Visio/Draw.io).
- Identifica core, distribution, access layer.
- Verifica collegamenti fibra/rame e ridondanze.
- Documenta ISP, router BGP/edge, switch upstream.

### 2. Firewall Rules
- Esporta regole da firewall (ASA, Palo, Forti, Cisco FTD, OPNsense).
- Classifica regole: inbound, outbound, intra-VLAN, DMZ, verso Internet.
- Verifica regole esplicite vs implicite (deny any any).
- Controllo NAT/PAT e logging.
- Rimuovi regole obsolete/duplicate/aperte a 0.0.0.0/0.

### 3. VLAN Segmentation
- Lista VLAN (ID, name, scopo, subnet, VLAN Gateway).
- Verifica tagging trunk/access su switch.
- Controllo che server/DB siano su VLAN separate da utente.
- Verifica ACL tra VLAN (inter-VLAN routing su L3 switch/firewall).

### 4. Bandwidth Utilization
- Collega NetFlow/sFlow (router, switch, firewall) a collector (ntop, SolarWinds, Plixer).
- Report giornalieri/settimanali per volume, applicazioni, top talker.
- Identifica picchi, congestioni, saturazione link ISP/upstream.
- Verifica QoS in applicazione e marking DSCP.

### 5. WiFi Coverage
- Site survey (Heatmap, RSSI, SNR, throughput). A/B testing 2.4 vs 5 GHz.
- Verifica channel utilization, overlap, potenze TX.
- Controllo bande Radio 11a/b/g/n/ac/ax, stesse channel su APs vicine.
- Verifica Load Balancing, Band Steering, RRM aggressiveness.
- Test roaming tra AP vendor.

### 6. VPN Concentrator Health
- Collaudo tunnel site-to-site (IPSec/SSL) e remote client (SSL/DTLS).
- Verifica SA lifetime, rekey, traffic stats/errors.
- Log congestione CPU/memoria, tunnel drops.
- Test failover tra istanze multiple (se presenti).

### 7. DNS / DHCP Config
- Server autoritativi (AD, BIND, Unbound) e forwarding/conditional.
- Split-horizon DNS (interno/esterno), DNSSEC.
- DHCP scope, reservation, option 43/66 per APs/VoIP.
- Verifica TTL, cache, forwarding performance.
- Controllo spoofing (DHCP snooping, IP Source Guard).

### 8. Device Inventory
- Asset HW/SW: modelli, seriali, firmware, data di installazione.
- Configurazioni correnti (backup giornaliero).
- Licenze e maintenance/contract in scadenza.
- Mappa MAC/porta per switch/access point.

---

## Improvement Catalog

Prioritizza queste migliorie in base a rischio, costo e business impact.

### SD-WAN Migration
- Valuta applicazioni critiche (VoIP, ERP, branch apps).
- Scegli tra Internet+LTE/5G con bonding o MPLS supplementare.
- Pilota su un branch, poi rollout con rollback plan.
- Configurazione QoS, applicance/Cloud onramp (SASE opzionale).

### Network Segmentation Zero-Trust
- Micro-segmentation con policy basate su identità (802.1X, certificati).
- Crea VLAN/VSVR per workload sensibili.
- Firewall a soglia L7 e ispezione TLS.
- Estendi a cloud (Security Groups, micro-segmentation NSX/Azure NSG).

### Firewall Rule Cleanup
- Rimuovi regole aperte/permesse, inverte ordine per minimizzazione.
- Applica principle of least privilege.
- Usa tag/group objects per oggetti dinamici.
- Abilita logging sulle regole critiche e quarterly review.

### WiFi 6 Upgrade
- Migrazione AP 6E/6 per maggiore densità e bassa latenza.
- Configurazione ottimale channel/HE40/80MHz, TDLS/MU-MIMO.
- Aggiorna firmware controller/AP.
- Valida con user experience test (speedtest, video conferencing).

### Redundant ISP Setup
- Secondo ISP con BGP/edge o semplice default route.
- Failover automatico (BFD/stateful, floating static).
- Separazione traffico critico/OTT su ISP primario.
- Verifica split routing verso sedi distinte.

### Network Monitoring Deployment
- Deploy NMS/PaaS (Grafana+Prometheus, Zabbix, PRTG, NetBox).
- Alert proattivi: congestione, downtime, config drift, VPN flaps.
- Integra NetFlow/sFlow per visibilità applicativa.
- Dashboard SLA/top talkers e trend capacity.

---

## Implementation Guide

Tempi di intervento indicativi. Adatta in base alle dimensioni e al vendor.

### Fase 0 – Preparazione
- Documenta baseline (topologia, config, performance).
- Coinvolgi change management e stakeholders.
- Pianifica finestre di manutenzione e rollback safe.
- Esegui backup di configurazioni critiche.

### Fase 1 – Monitoraggio e Visibilità
- Installa NetFlow/sFlow su collector.
- Configura NMS di base (discovery, grafici, allerta elementari).
- Fissa KPI: throughput, error rate, latency, jitter, utilization >70% trigger.

### Fase 2 – Sicurezza e Segmentazione
- Pulizia firewall: regole duplicate, implicit deny, logging.
- Abilita DHCP snooping, Dynamic ARP Inspection, IP Source Guard.
- Crea VLAN per server/DMZ/Guest; applica ACL inter-VLAN.
- Abilita 802.1X su porte di accesso (se switch lo supportano).

### Fase 3 – Ottimizzazione WiFi
- Aggiorna firmware controller/AP.
- Ri-survey aree critiche; aggiusta posizionamento/AP.
- Configura band steering, airtime fairness, minimizza rumore.
- Abilita WMM e ottimizza voice/video profiles.

### Fase 4 – VPN/Edge
- Verifica SA e performance tunnel; aumenta risorse se necessarie.
- Configura route-map/policy based routing per traffico privilegiato.
- Se migrazione SD-WAN, pilotare su branch non critici; rollback rapido.

### Fase 5 – Migliorie Strutturali (su timeline)
- SD-WAN: provisioning, bonding, QoS, applicance/Cloud onramp.
- Zero Trust: integrazione identità, micro-segmentation, L7 policy.
- Ridondanza ISP: BGP e floating static, test failover.
- Upgrade cablaggio/switch per supportare 10 G dove necessario.

### Fase 6 – Testing e Validation
- Verifica reachability, performance (iperf, pathping, MTR).
- Test failover (firewall, ISP, VPN).
- Verifica QoS in condizioni di carico e simulazione falli.
- Report delle modifiche e rollback disponibile.

### Fase 7 – Operazioni e Governance
- Configurazioni in revisione periodica (mensile/trimestrale).
- Aggiorna asset/report di capacity planning.
- Formazione team operations su nuovi processi e strumenti.
- SLA/KPI monitorati e review cicliche.

---

## Note Operative
- Mantieni sempre un rollback testato per ogni cambiamento critico.
- Usa config via test-bed prima del production.
- Mantieni documentazione aggiornata (topologia, VLAN, oggetti firewall).
- Per le estensioni cloud, integra security groups/NSG e private link dove applicabile.
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

- Valuta SASE/SD-WAN con zero trust integrato per ambienti distribuiti/multi-cloud.