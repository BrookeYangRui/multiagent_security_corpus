# A Troublemaker with Contagious Jailbreak Makes Chaos in Honest Towns

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Tianyi Men, Pengfei Cao, Zhuoran Jin, Yubo Chen, Kang Liu, Jun Zhao
- Year: 2025
- Venue: ACL 2025
- DOI: 10.18653/v1/2025.acl-long.859
- Primary URL: https://aclanthology.org/2025.acl-long.859/
- Open access URL: https://aclanthology.org/2025.acl-long.859.pdf
- BibTeX key: `men2025troublemaker`

## Paper Type

Attack; Benchmark; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

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

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical ACL 2025 version confirmed. Current title, author list, DOI, venue, and year are correct.
- Recommended scope: `core_security`
- Multi-agent dependency: One malicious member spreads jailbreak content through communication and independent memories; retrieval, replication, topology, and population size determine system-level propagation.
- Recommended roles: attack; benchmark; evaluation
- Maturity: Archival peer-reviewed primary evidence.

### Threat and Failure Coding

- Attacker or fault actor: One malicious member or troublemaker agent.
- Capabilities: Injects optimized retrieval and replication suffixes into messages or memory content that honest agents later retrieve and retransmit.
- Preconditions: Agents maintain independent memories and store and retrieve interaction content.
- Surfaces: Inter-agent messages; independent agent memories; communication topology.
- Mechanism: Adversarial retrieval and replication optimization creates a contagious jailbreak.
- Primary system-level failure: F1 compromise propagation and containment failure.
- Impact: Population-wide jailbreak among previously honest agents.

### Evaluation Contract

- Configuration: One attacker plus honest agents; line, star, and larger population settings, including a 100-agent experiment.
- Topology: Line, star, and other benchmarked structures; static experiment graphs.
- Baseline or ablation: Prior jailbreak or nonoptimized variants described in the paper.
- Metric: ASR by round, maximum ASR over rounds, and rounds to reach a target ASR.
- Unit: Agent-question pair and interaction round.
- Denominator: The paper defines the round metric over agent by question cases, then reports the maximum over rounds for its summary ASR.
- Result boundary: Reported improvements of 23.51%, 18.95%, and 52.93% are setting-specific values. Do not silently relabel them as percentage-point improvements.

### Evidence and Boundaries

- Evidence locations: Abstract, PDF p. 1; metric definition in Sec. 2.2, approximately PDF p. 3; experiment tables for topology and large-scale settings; abstract and result tables for the reported improvements.
- Author claim versus corpus interpretation: Attack construction and results are author claims. Cross-paper denominator incompatibility is a corpus interpretation.
- Limitations: Maximum reported population is 100 in the empirical benchmark; fixed topologies; multiple-choice style memory tasks; limited model and deployment diversity.

### Required Corrections

- **HIGH - Metric denominator:** Replace generic attack success with the paper's agent-question and round-specific definition.
- **MEDIUM - Result wording:** Report the three improvements exactly as authors report them; do not call them percentage points without table support.
<!-- SOURCE_REVIEW_END -->
