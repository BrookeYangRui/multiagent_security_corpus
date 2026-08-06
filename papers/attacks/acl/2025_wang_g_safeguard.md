# G-Safeguard: A Topology-Guided Security Lens and Treatment on LLM-based Multi-agent Systems

## Citation

- Authors: Shilong Wang, Guibin Zhang, Miao Yu, Guancheng Wan, Fanci Meng, Chongye Guo, Kun Wang, Yang Wang
- Year: 2025
- Venue: ACL 2025
- DOI: 10.18653/v1/2025.acl-long.359
- Primary URL: https://aclanthology.org/2025.acl-long.359/
- Open access URL: https://aclanthology.org/2025.acl-long.359.pdf
- BibTeX key: `wang2025gsafeguard`

## Paper Type

Attack; Defense; Evaluation; Empirical study

## Scope

### System Studied

LLM-based multi-agent systems represented as dynamic utterance graphs across
different backbones, sizes, and workflows.

### Multi-Agent Dependency

Attacks and defenses are modeled on the graph formed by agent utterances;
propagation and topological intervention require multiple communicating agents.

### Application Domain

General-purpose collaborative agent workflows.

## Security Model

- Protected assets: collective task integrity and safety.
- Threat actor: adversary introducing prompt injection or malicious information.
- Trusted components: graph construction, anomaly detector, and intervention
  mechanism.
- Attacker capabilities: influence utterances that propagate through the agent
  graph.
- Security assumptions: communication can be represented and monitored as an
  utterance graph.

## Main Contribution

G-Safeguard combines a topology-guided security analysis with graph-neural
anomaly detection and topological intervention for attack remediation.

## Attack or Failure

- Attack surface: agent utterances and communication topology.
- Attack mechanism: prompt injection and adversarial information propagation.
- System-level failure: collective task-integrity degradation.
- Security consequence: corrupted multi-agent reasoning and output.

## Defense

- Defense mechanism: graph neural anomaly detection plus topological
  intervention.
- Intervention point: utterance graph and communication links.
- Required observability: multi-agent utterances and their graph relationships.
- Assumptions: the monitor can construct the relevant utterance graph.
- Limitations: graph access and attack distribution may differ in deployed
  systems.

## Evaluation

- Evaluated systems: diverse LLM backbones and multi-agent system scales.
- Agent configuration: multiple workflows represented by utterance graphs.
- Dataset or environment: tasks and attacks specified by the paper.
- Baselines: mainstream MAS safeguards and attack conditions.
- Metrics: recovered task performance and security outcomes.
- Main results: the authors report recovery of more than 40% performance under
  prompt injection and adaptability across backbones and scales.

## Relation to Existing Work

- Claimed research gap: single-agent safeguards do not model multi-agent topology.
- Closest related work: graph anomaly detection, prompt-injection defense, and
  topology-aware MAS analysis.
- Difference from prior work: makes the utterance graph both the analysis object
  and intervention locus.

## Relevance to Our SoK

- Included concepts: utterance graph, graph monitor, prompt injection,
  topological intervention.
- Taxonomy implications: this attack-and-defense paper belongs in the attack
  corpus and must also be indexed later as a defense/evaluation artifact without
  duplicating its canonical record.
- Supported research questions: which graph visibility a defense requires.
- Important limitations: claimed security guarantees must be read under the
  paper's graph and observability assumptions.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| G-Safeguard uses a graph neural network on the agent utterance graph. | Explicit author claim | Paper | Abstract; method | PDF 1; method section | Not applicable | Stated in the official abstract. |
| The defense applies topological intervention for remediation. | Explicit author claim | Paper | Abstract; method | PDF 1; method section | Not applicable | Stated in the official abstract. |
| The authors report over 40% performance recovery for prompt injection. | Explicit author claim | Paper | Abstract; experiments | PDF 1; result tables | Not applicable | Stated in the official abstract. |
| Defense applicability depends on access to the utterance graph. | Corpus interpretation | Paper | System model | PDF 2 onward | Not applicable | Derived from required defense inputs. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: exact-title search
- Accessed version: published ACL 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

