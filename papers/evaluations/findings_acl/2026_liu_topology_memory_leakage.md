# Topology Matters: Measuring Memory Leakage in Multi-Agent LLMs

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

Title: Topology Matters: Measuring Memory Leakage in Multi-Agent LLMs

Authors: Jinbo Liu; Defu Cao; Yifei Wei; Tianyao Su; Yuan Liang; Yushun Dong; Yan Liu; Yue Zhao; Xiyang Hu

Year: 2026

Venue: Findings of ACL

DOI: 10.18653/v1/2026.findings-acl.1980

Primary URL: https://aclanthology.org/2026.findings-acl.1980/

Open access URL: https://aclanthology.org/2026.findings-acl.1980.pdf

BibTeX key: liu2026topologymemory

## Paper Type

Benchmark; Evaluation; Attack study

- Primary category: `evaluation`
- Scope relation: `core_security`

## Scope

### System Studied

Text-only LLM multi-agent networks in which one target has private synthetic PII, one attacker seeks it, and normal agents relay task-relevant messages over fixed graph topologies.

### Multi-Agent Dependency

Private memory begins at one node and can reach an unauthorized node only through topology-conditioned communication and memory updates. Leakage is measured across attacker-target placements, graph families, rounds, and population sizes.

### Application Domain

General-purpose collaborative task solving with private memory.

## Security Model

### Protected Assets

Synthetic personally identifiable information stored exclusively in a target agent's private memory.

### Threat Actor

One malicious member agent.

### Trusted Components

The synthetic-data generator, exact-match evaluator, and LLM judge are trusted.

### Attacker Capabilities

The attacker participates in normal communication, frames PII requests as task assistance, observes only topology-permitted messages, and accumulates information over rounds.

### Security Assumptions

One attacker and one target are assigned in a static known graph; private data is synthetic; communication is text-only and synchronous.

## Main Contribution

The paper introduces MAMA, a controlled evaluation framework for memory leakage over six multi-agent topologies. Its Engram phase seeds exclusive private memory and its Resonance phase measures extraction and diffusion over repeated communication.

## Attack or Failure

### Attack Surface

Private memory, inter-agent messages, and topology-mediated observation.

### Attack Mechanism

The attacker repeatedly solicits private information under a cooperative task framing while intermediate agents relay partial cues and outputs through the graph.

### System-Level Failure

Information assigned to one principal becomes recoverable by an unauthorized participant.

### Security Consequence

Cross-principal confidentiality and contextual-integrity failure.

## Defense

### Defense Mechanism

No implemented defense; the authors derive design guidance involving sparse graphs, lower hub privilege, smaller radius exposure, and pre-deployment topology testing.

### Intervention Point

Topology and authority design.

### Required Observability

Graph structure, role placement, and leakage traces.

### Assumptions

The system designer can choose topology or constrain central-node privileges.

### Limitations

The paper fixes ten Resonance rounds, uses one attacker, text-only communication, synthetic PII, an LLM judge, and six canonical static topologies.

## Evaluation

### Evaluated Systems

GPT-4o-mini and Llama-3.1-70B-based agent networks.

### Agent Configuration

Four, five, or six agents; target, attacker, and normal roles; complete, circle, chain, tree, star, and star-ring topologies; varying placements.

### Dataset or Environment

Synthetic documents derived from FABRIC tasks with labeled PII and sanitized shared instructions.

### Baselines

Cross-topology, attacker-target placement, agent-count, round-count, PII category, and model comparisons.

### Metrics

Exact-match-plus-LLM-inference leakage rate, topology-conditioned leakage, diffusion over rounds, and ever-leaked entities.

### Main Results

The authors report that complete and star-ring graphs tend to leak most, chain/tree graphs tend to leak less, central placement increases risk, and most new leakage occurs early before plateauing. Absolute levels and some topology rankings vary by model.

## Relation to Existing Work

### Papers Compared by the Authors

NetSafe, G-Safeguard, memory-injection attacks, and black-box multi-agent leakage studies.

### Claimed Research Gap

Existing work does not isolate topology, placement, scale, and rounds for private-memory leakage under a controlled threat model.

### Closest Related Work

NetSafe for topology-conditioned safety and MASLeak for multi-agent information extraction.

### Difference From Prior Work

MAMA controls exclusive access to labeled synthetic PII and systematically enumerates graph and placement variables.

## Relevance to Our SoK

### Included Concepts

Private/shared memory, graph topology, attacker placement, cross-principal authorization, population denominator, and temporal leakage.

### Taxonomy Implications

The paper directly links system design and attacker position to a cross-principal confidentiality violation without treating privacy leakage as a generic prompt-injection outcome.

### Supported Research Questions

Which topology and placement variables govern cross-agent memory leakage, and what measurement contract supports comparison?

### Important Limitations

This attack-and-benchmark paper remains canonically in `papers/attacks`; the evaluations area should reference this note rather than duplicate its corpus record.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Only the target receives the private PII at initialization. | Explicit author claim | Paper | 3.1-3.2 | 3-4 | Figure 1, Table 1 | Role and state construction. |
| Engram seeds memory and Resonance propagates requests and responses over the graph. | Explicit author claim | Paper | 3.2 | 4-5 | Figure 1 | Two-phase protocol. |
| Six topologies and populations of four to six agents are evaluated. | Explicit author claim | Paper | 3.3, 4.1 | 5-6 | Figure 1 | Experimental design. |
| Dense topologies generally leak more and most leakage appears in early rounds. | Explicit author claim | Paper | 4 | 7-9 | Tables 2-3, Figures 2-3 | Main analysis. |
| The study is limited to fixed rounds, text, one attacker, synthetic data, and an LLM judge. | Explicit author claim | Paper | Limitations | 9 | - | Limitations statement. |

## Provenance

### Discovery Source

ACL Anthology; prior corpus.

### Discovery Query

Not applicable.

### Accessed Version

Published conference version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after major patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical Findings of ACL 2026 version confirmed. Metadata is correct.
- Recommended scope: `core_security`
- Multi-agent dependency: Private memory originates at one agent and reaches an unauthorized member only through topology-conditioned communication and memory updates.
- Recommended roles: benchmark; evaluation; attack study
- Maturity: Archival peer-reviewed benchmark and evaluation evidence.

### Threat and Failure Coding

- Attacker or fault actor: One malicious member agent targeting one private-memory holder.
- Capabilities: Participates in normal communication, solicits private data, observes topology-permitted messages, and accumulates information across rounds.
- Preconditions: Static known graph, one attacker and one target, synchronous text communication, synthetic PII.
- Surfaces: Private memory; inter-agent messages; topology; role placement.
- Mechanism: Repeated cooperative-looking solicitation and topology-mediated relay of private cues.
- Primary system-level failure: F2 cross-principal confidentiality violation.
- Impact: Recovery and diffusion of private PII by an unauthorized participant.

### Evaluation Contract

- Configuration: GPT-4o-mini and Llama-3.1-70B networks; 4, 5, or 6 agents; one target and one attacker; ten communication rounds.
- Topology: Complete, circle, chain, tree, star, and star-ring; varied attacker-target placement.
- Baseline or ablation: Cross-topology, placement, agent-count, round-count, PII-category, and model comparisons.
- Metric: Exact-match-plus-LLM-inference leakage rate, ever-leaked entities, and temporal diffusion.
- Unit: PII entity and trace or configuration.
- Denominator: Seeded protected PII entities or evaluated traces, as defined by each result.
- Result boundary: Dense graphs and central placements often leak more, while much leakage appears early. Absolute levels and some topology rankings vary by model and should not be universalized.

### Evidence and Boundaries

- Evidence locations: Secs. 3.1 to 3.3, PDF pp. 3 to 6 and Fig. 1/Table 1 for state, roles, and six topologies; Sec. 4, PDF pp. 7 to 9, Tables 2 to 3 and Figs. 2 to 3 for leakage and temporal results; limitations, PDF p. 9.
- Author claim versus corpus interpretation: Topology setup, metrics, and reported trends are author claims. Assigning F2 as the primary property and indexing it as benchmark/evaluation are corpus decisions.
- Limitations: Synthetic PII; fixed ten rounds; one attacker; text-only synchronous communication; six static topologies; LLM judge in metric pipeline.

### Required Corrections

- **CRITICAL - Primary category:** Change from attack to benchmark/evaluation with an attack study role.
- **HIGH - Metric denominator:** Store exact-match and LLM-inference leakage definitions and seeded-entity denominator.
- **MEDIUM - Generalization:** Do not state a universal topology ranking across models.
<!-- SOURCE_REVIEW_END -->
