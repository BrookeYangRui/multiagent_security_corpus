# CIA: Inferring the Communication Topology from LLM-based Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: CIA: Inferring the Communication Topology from LLM-based Multi-Agent Systems

Authors: Yongxuan Wu; Xixun Lin; He Zhang; Nan Sun; Kun Wang; Chuan Zhou; Shirui Pan; Yanan Cao

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.815

Primary URL: https://aclanthology.org/2026.acl-long.815/

Open access URL: https://aclanthology.org/2026.acl-long.815.pdf

BibTeX key: wu2026cia

## Paper Type

- Attack
- Evaluation
- Empirical study

## Scope

### System Studied

Black-box LLM multi-agent systems whose hidden communication graphs were optimized for collaborative task solving.

### Multi-Agent Dependency

The protected asset is the graph of inter-agent edges. CIA induces and correlates intermediate agent outputs to infer those edges from black-box queries, a target that is undefined for one agent.

### Application Domain

General-purpose collaborative reasoning.

## Security Model

### Protected Assets

Proprietary communication topology and structural system information.

### Threat Actor

An external black-box querier.

### Trusted Components

Agents, model weights, system prompts, and internal communication logs are not compromised.

### Attacker Capabilities

The attacker submits crafted queries and observes exposed system outputs but has no direct access to model parameters, roles, prompts, messages, or graph edges.

### Security Assumptions

Semantic dependence induced by information flow is reflected in observable intermediate or returned outputs sufficiently to support weak supervision.

## Main Contribution

CIA generates adversarial queries that stimulate intermediate reasoning and infers graph edges from semantic correlations. It adds global-bias disentanglement and LLM-guided weak supervision for restrictive black-box topology reconstruction.

## Attack or Failure

### Attack Surface

Black-box query interface and interaction-dependent output correlations.

### Attack Mechanism

Construct queries that elicit diverse reasoning signals, remove global semantic bias, create weak edge labels with an LLM, and train an edge classifier.

### System-Level Failure

The hidden communication topology is reconstructed with useful accuracy.

### Security Consequence

Structural confidentiality and intellectual-property leakage; inferred topology may also support later targeted attacks.

## Defense

### Defense Mechanism

No implemented defense; the paper motivates protecting intermediate outputs and reducing topology-revealing correlations.

### Intervention Point

External response interface and communication observability.

### Required Observability

Potential defenses would need to detect topology-probing query patterns or control exposed intermediate information.

### Assumptions

Not reported.

### Limitations

The study targets a set of optimized graph constructions and treats topology inference as reconnaissance rather than demonstrating a downstream exploit.

## Evaluation

### Evaluated Systems

Multiple LLM backbones and optimized MAS communication topologies.

### Agent Configuration

Black-box systems with varying hidden directed graph structures.

### Dataset or Environment

Collaborative reasoning datasets and topology generators described in the experimental setup.

### Baselines

Correlation-based and graph-inference baselines plus component ablations.

### Metrics

Edge-inference AUC and related classification metrics.

### Main Results

The authors report mean AUC 0.87 and peak AUC 0.99, with both bias disentanglement and LLM weak supervision contributing in ablations.

## Relation to Existing Work

### Papers Compared by the Authors

Model extraction, graph reconstruction, topology optimization, and privacy leakage attacks.

### Claimed Research Gap

Prior MAS security work attacks messages or agents but does not infer a proprietary communication graph under restrictive black-box access.

### Closest Related Work

Black-box extraction of multi-agent internals and topology-aware safety analysis.

### Difference From Prior Work

CIA makes graph structure itself the protected asset and recovers it from semantic information-flow traces.

## Relevance to Our SoK

### Included Concepts

Topology, black-box external adversary, reconnaissance, structural confidentiality, partial observability, and weak supervision.

### Taxonomy Implications

Topology inference is an attack mechanism or enabling step, while the direct failure is structural confidentiality loss; it should not be conflated with topology corruption.

### Supported Research Questions

Which hidden MAS design choices can be inferred from public behavior, and what observer exposure enables reconstruction?

### Important Limitations

The evaluation establishes topology leakage but not the operational impact of a follow-on attack.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| CIA assumes restrictive black-box access without internal graph or message visibility. | Explicit author claim | Paper | 3 | 3-4 | Threat model figure | Attack setting. |
| Queries induce intermediate reasoning signals used for edge inference. | Explicit author claim | Paper | 4 | 4-6 | Method figure | Attack pipeline. |
| Global-bias disentanglement and LLM-guided weak supervision support classification. | Explicit author claim | Paper | 4 | 5-7 | - | Method components. |
| CIA reports average AUC 0.87 and peak AUC 0.99. | Explicit author claim | Paper | 5 | 8-10 | Main result tables | Evaluation result. |
| The result is reconnaissance/structure leakage rather than demonstrated topology modification. | Interpretation | Paper | 3-5 | 3-10 | - | Attack output is an inferred edge set. |

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
