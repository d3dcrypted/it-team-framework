---
name: it-team-network
description: 'Use when assessing or improving network infrastructure. LAN/WAN/VPN assessment + firewall rules + SD-WAN + network segmentation + monitoring.'
category: network
version: 0.2.0
author: d3d
license: MIT
metadata:
  hermes:
    tags: [network, firewall, sd-wan, segmentation, vpn, wifi, dns-dhcp, monitoring]
    related_skills: [it-team-security, it-team-cloud, it-team-os-infra]
---

# Network Specialist — Network Engineer (it-team-network)

## Assessment Protocol

Perform a complete assessment following this sequence. For each item, verify and document results, current configurations, and recommendations.

### 1. Network Topology
- Physical and logical maps (Visio/Draw.io diagrams).
- Identify core, distribution, access layers.
- Verify fiber/copper links and redundancies.
- Document ISP, BGP/edge routers, upstream switches.

### 2. Firewall Rules
- Export rules from firewalls (ASA, Palo, Forti, Cisco FTD, OPNsense).
- Classify rules: inbound, outbound, intra-VLAN, DMZ, toward Internet.
- Verify explicit vs. implicit rules (deny any any).
- Check NAT/PAT and logging.
- Remove obsolete/duplicate/rules open to 0.0.0.0/0.

### 3. VLAN Segmentation
- VLAN list (ID, name, purpose, subnet, VLAN gateway).
- Verify trunk/access tagging on switches.
- Ensure servers/DBs are on VLANs separate from users.
- Verify inter-VLAN ACLs (inter-VLAN routing on L3 switch/firewall).

### 4. Bandwidth Utilization
- Connect NetFlow/sFlow (router, switch, firewall) to collector (ntop, SolarWinds, Plixer).
- Daily/weekly reports by volume, applications, top talker.
- Identify peaks, congestions, ISP/upstream link saturation.
- Verify QoS enforcement and DSCP marking.

### 5. WiFi Coverage
- Site survey (Heatmap, RSSI, SNR, throughput). A/B testing 2.4 vs 5 GHz.
- Verify channel utilization, overlap, TX power.
- Check radio bands 11a/b/g/n/ac/ax, same channels on nearby APs.
- Verify load balancing, band steering, RRM aggressiveness.
- Test roaming between AP vendors.

### 6. VPN Concentrator Health
- Test site-to-site (IPSec/SSL) and remote client (SSL/DTLS) tunnels.
- Verify SA lifetime, rekey, traffic stats/errors.
- Log CPU/memory congestion, tunnel drops.
- Test failover across multiple instances (if present).

### 7. DNS / DHCP Config
- Authoritative servers (AD, BIND, Unbound) and forwarding/conditional.
- Split-horizon DNS (internal/external), DNSSEC.
- DHCP scopes, reservations, option 43/66 for APs/VoIP.
- Verify TTL, cache, forwarding performance.
- Check spoofing (DHCP snooping, IP Source Guard).

### 8. Device Inventory
- HW/SW assets: models, serials, firmware, installation dates.
- Current configurations (daily backup).
- Licenses and maintenance/contract expirations.
- MAC/port mapping for switches/access points.

---

## Improvement Catalog

Prioritize these improvements based on risk, cost, and business impact.

### SD-WAN Migration
- Evaluate critical applications (VoIP, ERP, branch apps).
- Choose between Internet+LTE/5G with bonding or supplementary MPLS.
- Pilot on one branch, then rollout with rollback plan.
- QoS configuration, appliance/Cloud onramp (optional SASE).

### Zero-Trust Network Segmentation
- Micro-segmentation with identity-based policies (802.1X, certificates).
- Create VLANs/VSRs for sensitive workloads.
- L7 threshold firewall and TLS inspection.
- Extend to cloud (Security Groups, NSX/Azure NSG micro-segmentation).

### Firewall Rule Cleanup
- Remove open/permissive rules, reorder to minimize.
- Apply principle of least privilege.
- Use tag/group objects for dynamic objects.
- Enable logging on critical rules and quarterly review.

### WiFi 6 Upgrade
- Migrate to 6E/6 APs for higher density and low latency.
- Optimal channel/HE40/80MHz configuration, TDLS/MU-MIMO.
- Update controller/AP firmware.
- Validate with user experience tests (speedtest, video conferencing).

### Redundant ISP Setup
- Secondary ISP with BGP/edge or simple default route.
- Automatic failover (BFD/stateful, floating static).
- Critical/OTT traffic separation on primary ISP.
- Verify split routing to separate locations.

### Network Monitoring Deployment
- Deploy NMS/PaaS (Grafana+Prometheus, Zabbix, PRTG, NetBox).
- Proactive alerts: congestion, downtime, config drift, VPN flaps.
- Integrate NetFlow/sFlow for application visibility.
- SLA/top talkers dashboards and capacity trend reporting.

---

## Implementation Guide

Estimated intervention timelines. Adapt based on size and vendor.

### Phase 0 – Preparation
- Document baseline (topology, config, performance).
- Engage change management and stakeholders.
- Plan maintenance windows and safe rollbacks.
- Back up critical configurations.

### Phase 1 – Monitoring and Visibility
- Install NetFlow/sFlow on collector.
- Configure basic NMS (discovery, charts, elementary alerting).
- Set KPIs: throughput, error rate, latency, jitter, utilization >70% trigger.

### Phase 2 – Security and Segmentation
- Firewall cleanup: duplicate rules, implicit deny, logging.
- Enable DHCP snooping, Dynamic ARP Inspection, IP Source Guard.
- Create VLANs for servers/DMZ/Guest; apply inter-VLAN ACLs.
- Enable 802.1X on access ports (if switches support it).

### Phase 3 – WiFi Optimization
- Update controller/AP firmware.
- Re-survey critical areas; adjust positioning/APs.
- Configure band steering, airtime fairness, minimize noise.
- Enable WMM and optimize voice/video profiles.

### Phase 4 – VPN/Edge
- Verify SA and tunnel performance; increase resources if needed.
- Configure route-map/policy-based routing for privileged traffic.
- If migrating to SD-WAN, pilot on non-critical branches; fast rollback.

### Phase 5 – Structural Improvements (on timeline)
- SD-WAN: provisioning, bonding, QoS, appliance/Cloud onramp.
- Zero Trust: identity integration, micro-segmentation, L7 policy.
- ISP redundancy: BGP and floating static, failover testing.
- Cabling/switch upgrades to support 10G where needed.

### Phase 6 – Testing and Validation
- Verify reachability, performance (iperf, pathping, MTR).
- Test failover (firewall, ISP, VPN).
- Verify QoS under load and fault simulation.
- Document changes and available rollbacks.

### Phase 7 – Operations and Governance
- Periodic configuration review (monthly/quarterly).
- Update asset/capacity planning reports.
- Team training on new processes and tools.
- SLA/KPI monitoring and cyclic reviews.

---

## Operational Notes
- Always maintain a tested rollback for every critical change.
- Use config via test-bed before production.
- Keep documentation updated (topology, VLAN, firewall objects).
- For cloud extensions, integrate security groups/NSG and private link where applicable.
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


## Privacy & Data Handling

- Assessment data classified per organization policy (public / internal / confidential / restricted).
- PII in findings must be redacted or anonymized in all deliverables.
- Reports stored only in approved repositories or encrypted shares.
- Credentials, secrets, and API keys must never appear in deliverables.
- Comply with GDPR, HIPAA, SOX, and local regulations where applicable.
- Data retention follows organization retention schedule; dispose per policy.

- Evaluate SASE/SD-WAN with integrated zero trust for distributed/multi-cloud environments.
