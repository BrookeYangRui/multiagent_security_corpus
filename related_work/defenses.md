# Defenses

Cross-paper synthesis of defense mechanisms, intervention points, observability,
trusted components, and limitations.

## Entries

Use BibTeX keys or paper-note paths and label every statement by evidence type.

### Topology and Trace Defenses

- **Established finding:** `pan2026xgguard`, `huang2026toposhield`,
  `zhou2025guardian`, and the attack-primary `wang2025gsafeguard` all use the
  communication graph as an observed or controlled object. Their interventions
  span anomaly detection, edge pruning, community isolation, and topology
  repair.
- **Cross-paper observation:** These methods require message and graph access
  that an ordinary member agent does not possess; their trusted observer and
  topology controller must therefore be coded separately from their detection
  model.
- **Established finding:** `rabieinejad2026alteda` uses synchronized
  application, network, and system logs instead of prompt content, illustrating
  that global scope and content visibility are distinct observer dimensions.

### Distributed Trust and Coordination

- **Established finding:** `feng2026sentinelnet` distributes learned credit
  detectors among peers, while `darabi2026bioautonomic` distributes local
  anomaly signals through gossip and trust updates.
- **Established finding:** `ebrahimi2025credibility` attenuates unreliable
  contributors through longitudinal credibility; `he2025atrust` scores six
  message-trust dimensions; `mao2025ibgp` changes the agreement contract to
  local coordination; and `jo2025byzantinerobust` assumes authenticated
  synchrony for leaderless f<n/2 coordination.
- **Our interpretation:** Robustness numbers from these papers are not directly
  comparable until identity persistence, honest-neighbor, synchrony, and
  agreement assumptions are normalized.

### Prevention, Containment, and Recovery

- **Established finding:** `zhou2026resmas` and `rosser2025agentbreeder` act at
  design time; `shi2026saiguard` acts before message delivery; XG-Guard,
  TopoSHIELD, GUARDIAN, and SentinelNet contain detected influence at runtime.
- **Established finding:** `wu2025cowpox` explicitly studies population
  immunization and recovery, a function rarely represented by graph anomaly
  detectors.
- **Cross-paper observation:** Detection and containment remain much more common
  than recovery, and most methods assume either a trusted graph controller or
  persistent identities.

### Confidentiality, Authority, and Protocol Controls

- **Established finding:** `mao2025agentsafe` enforces hierarchical message and
  memory access; `cui2025maris` applies reference monitors and verified flow
  policies; `tapwal2026prism` intervenes during generation; `zou2025blocka2a`
  proposes protocol-native identity, provenance, authorization, and revocation.
- **Cross-paper observation:** These controls protect different confidentiality
  contracts: credential-string leakage, administratively labeled access, and
  principal-specific information flow should not share one undifferentiated
  defense count.
- **Open question:** How can principal and provenance metadata survive semantic
  rewriting, delegation, shared memory, and cross-protocol translation?

### Covert-Coordination Detection

- **Established finding:** `tailor2025auditwhisper` combines channel-capacity
  analysis, paired-run interventions, calibrated detectors, and
  ColludeBench-v0.
- **Cross-paper observation:** Detectability depends on added auditor powers:
  channel perturbation, paired executions, outcome access, or subgroup labels.
  These assumptions must accompany any detection claim.
