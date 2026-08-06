# NetSafe: Exploring the Topological Safety of Multi-agent System

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Miao Yu, Shilong Wang, Guibin Zhang, Junyuan Mao, Chenlong Yin, Qijiong Liu, Kun Wang, Qingsong Wen, Yang Wang
- Year: 2025
- Venue: Findings of ACL 2025
- DOI: 10.18653/v1/2025.findings-acl.150
- Primary URL: https://aclanthology.org/2025.findings-acl.150/
- Open access URL: https://aclanthology.org/2025.findings-acl.150.pdf
- BibTeX key: `yu2025netsafe`

## Paper Type

Benchmark; Evaluation; Topology analysis

- Primary category: `evaluation`
- Scope relation: `security_relevant`

## Scope

### System Studied

LLM-based multi-agent workflows unified through iterative relation and
communication interactions under multiple communication topologies.

### Multi-Agent Dependency

The paper measures how graph connectivity, network size, and aggregation change
the propagation and impact of malicious content.

### Application Domain

General-purpose multi-agent reasoning.

## Security Model

- Protected assets: agent and aggregate answer safety and task integrity.
- Threat actor: a malicious-query source or compromised interaction input.
- Trusted components: topology configuration and evaluation harness.
- Attacker capabilities: introduce misinformation, bias, or harmful content.
- Security assumptions: agents iteratively exchange information according to the
  configured graph.

## Main Contribution

NetSafe introduces a topology-centered framework for studying multi-agent safety
and reports Agent Hallucination, Aggregation Safety, and Security Bottleneck
phenomena under attack.

## Attack or Failure

- Attack surface: graph edges and iterative communication.
- Attack mechanism: malicious content propagates and is aggregated by peers.
- System-level failure: propagation, aggregation, and collective-decision
  integrity failures.
- Security consequence: degraded task performance and unsafe collective output.

## Defense

- Defense mechanism: topology analysis rather than a single standalone defense.
- Intervention point: communication graph.
- Required observability: topology, per-round messages, and per-agent outcomes.
- Assumptions: workflows can be represented by the RelCom abstraction.
- Limitations: topology effects may interact with model, prompt, and compute
  changes.

## Evaluation

- Evaluated systems: multiple LLM-based MAS workflows.
- Agent configuration: varying graph connectivity and population size.
- Dataset or environment: the NetSafe/RelCom evaluation framework.
- Baselines: alternative topologies and benign/attacked conditions.
- Metrics: per-agent and aggregate accuracy/safety outcomes.
- Main results: highly connected and larger systems are reported as more
  vulnerable; star-topology task performance decreases by 29.7% in one reported
  setting.

## Relation to Existing Work

- Claimed research gap: single-agent safeguards and evaluations do not capture
  communication topology.
- Closest related work: multi-agent debate, topology design, and malicious-query
  evaluation.
- Difference from prior work: systematically varies graph structure as a safety
  factor.

## Relevance to Our SoK

- Included concepts: topology, graph connectivity, propagation, aggregation,
  security bottleneck.
- Taxonomy implications: contains both attack evidence and a reusable evaluation
  framework; later evaluation indexing should point here rather than duplicate it.
- Supported research questions: whether topology isolates or amplifies attacks.
- Important limitations: reported task drops are setting-specific and not a
  universal severity scale.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| NetSafe unifies workflows through iterative RelCom interactions. | Explicit author claim | Paper | Abstract; framework | PDF 1-3 | Not applicable | Stated in the official abstract. |
| The paper identifies Agent Hallucination, Aggregation Safety, and Security Bottleneck. | Explicit author claim | Paper | Abstract; analysis | PDF 1; result sections | Not applicable | Phenomena are named in the abstract. |
| A star topology shows a 29.7% task-performance decrease in a reported setting. | Explicit author claim | Paper | Abstract; experiments | PDF 1; result tables | Not applicable | Value appears in the official abstract. |
| The framework is a benchmark/evaluation artifact as well as attack evidence. | Corpus interpretation | Paper | Framework and experiments | PDF 2 onward | Not applicable | Corpus classification based on reusable evaluation design. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: exact-title search
- Accessed version: published Findings of ACL 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after major patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical Findings of ACL 2025 version confirmed. Metadata is correct.
- Recommended scope: `security_relevant at paper level; core_security for adversarial claims`
- Multi-agent dependency: The paper mixes adversarial misinformation or harmful content with broader hallucination, bias, fairness, and reliability phenomena. Only the adversarial security claims should enter core-security statistics.
- Recommended roles: benchmark; evaluation; topology analysis
- Maturity: Archival peer-reviewed mixed safety and security evidence.

### Threat and Failure Coding

- Attacker or fault actor: Malicious-query source or compromised interaction input in adversarial subsets.
- Capabilities: Introduces misinformation, bias, or harmful content that propagates and is aggregated.
- Preconditions: Agents iteratively exchange information according to a configured RelCom graph.
- Surfaces: Communication topology; iterative messages; aggregation.
- Mechanism: Topology-conditioned propagation and aggregation. Topology itself is an evaluation variable, not an attack mechanism.
- Primary system-level failure: Claim-level F1 or F4 for adversarial subsets; adjacent reliability and fairness for other phenomena.
- Impact: Task-performance and safety degradation in evaluated settings.

### Evaluation Contract

- Configuration: Multiple workflows, graph connectivity levels, system sizes, and per-round interactions.
- Topology: RelCom abstraction with multiple graph structures and scales.
- Baseline or ablation: Alternative topologies and benign versus attacked conditions.
- Metric: Per-agent and aggregate joint accuracy or safety outcomes by round and topology.
- Unit: Agent, round, and task.
- Denominator: Per-agent or aggregate task cases as defined in each experiment.
- Result boundary: The reported 29.7% star-topology decrease is a relative task-performance decrease in a specific setting. It is not a universal severity figure or necessarily a percentage-point change.

### Evidence and Boundaries

- Evidence locations: Abstract and framework, PDF pp. 1 to 3; result sections naming Agent Hallucination, Aggregation Safety, and Security Bottleneck; exact result table for the 29.7% setting; limitations section.
- Author claim versus corpus interpretation: RelCom, phenomena, and setting-specific numbers are author claims. Treating the artifact as benchmark/evaluation and splitting security from adjacent claims are corpus decisions.
- Limitations: Authors note that RelCom may not capture system-specific designs and that privacy and security are not comprehensively covered; topology effects can interact with prompt, model, and compute changes.

### Required Corrections

- **CRITICAL - Primary category:** Change from attack to benchmark/evaluation.
- **CRITICAL - Scope relation:** Use claim-level screening; paper-level core_security overstates broad safety and reliability content.
- **HIGH - Result wording:** Label 29.7% as a setting-specific relative performance decrease.
<!-- SOURCE_REVIEW_END -->
