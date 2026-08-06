# A Troublemaker with Contagious Jailbreak Makes Chaos in Honest Towns

## Citation

- Authors: Tianyi Men, Pengfei Cao, Zhuoran Jin, Yubo Chen, Kang Liu, Jun Zhao
- Year: 2025
- Venue: ACL 2025
- DOI: 10.18653/v1/2025.acl-long.859
- Primary URL: https://aclanthology.org/2025.acl-long.859/
- Open access URL: https://aclanthology.org/2025.acl-long.859.pdf
- BibTeX key: `men2025troublemaker`

## Paper Type

Attack; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Large text-based multi-agent societies whose agents maintain independent memories
and communicate over line, star, and other graph structures.

### Multi-Agent Dependency

One attacker attempts to spread jailbreak content across honest agents; retrieval,
replication, topology, and population size determine propagation.

### Application Domain

General-purpose agent societies.

## Security Model

- Protected assets: integrity of each agent's memory and population safety.
- Threat actor: one attacker/troublemaker agent.
- Trusted components: honest agents and their initially clean memories.
- Attacker capabilities: inject crafted content that recipients may retrieve and
  replicate.
- Security assumptions: agents store interaction content and later retrieve it.

## Main Contribution

The paper introduces the TMCHT multi-topology evaluation task and Adversarial
Replication Contagious Jailbreak, which optimizes retrieval and replication
suffixes to sustain attacks across sparse and large agent networks.

## Attack or Failure

- Attack surface: independent memories and inter-agent messages.
- Attack mechanism: optimized retrieval and replication suffixes make poison
  retrievable and contagious.
- System-level failure: propagation and containment failure.
- Security consequence: jailbreak spreads from one malicious member to honest
  agents.

## Defense

- Defense mechanism: Not reported as the primary contribution.
- Intervention point: Not reported.
- Required observability: Not reported.
- Assumptions: Not reported.
- Limitations: the reported topology and population settings do not cover all
  deployed communication and memory designs.

## Evaluation

- Evaluated systems: text-based LLM agents with independent memory.
- Agent configuration: one attacker and honest agents under multiple topologies;
  includes a 100-agent setting.
- Dataset or environment: TMCHT.
- Baselines: non-optimized and prior jailbreak approaches described in the paper.
- Metrics: attack success and propagation effectiveness.
- Main results: ARCJ improves reported attack outcomes by 23.51% in line, 18.95%
  in star, and 52.93% in the 100-agent setting.

## Relation to Existing Work

- Claimed research gap: prior work focuses on single agents or shared memory and
  does not handle sparse topology and scale.
- Closest related work: Agent Smith, prompt infection, memory poisoning, and
  jailbreak attacks.
- Difference from prior work: targets independent memories with explicit
  retrieval and replication optimization.

## Relevance to Our SoK

- Included concepts: contagious jailbreak, retrieval, replication, independent
  memory, topology, scale.
- Taxonomy implications: supports behavioral contagion and memory-integrity
  analysis.
- Supported research questions: how sparse graphs and large populations affect
  attack attenuation.
- Important limitations: benchmark improvements are not directly comparable to
  other infection metrics without denominator normalization.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| TMCHT evaluates one attacker against multi-topology and large-scale agent societies. | Explicit author claim | Paper | Abstract; task definition | PDF 1-3 | Not applicable | Stated in the official abstract and setup. |
| ARCJ optimizes retrieval and replication suffixes. | Explicit author claim | Paper | Abstract; method | PDF 1; method section | Not applicable | The abstract names both optimization targets. |
| Reported improvements are 23.51%, 18.95%, and 52.93% in specified settings. | Explicit author claim | Paper | Abstract; results | PDF 1; result tables | Not applicable | Values are stated in the official abstract. |
| Cross-paper infection severity requires denominator normalization. | Corpus interpretation | Paper | Evaluation | results section | Not applicable | Methodological caution; not an author claim. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: exact-title search
- Accessed version: published ACL 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

