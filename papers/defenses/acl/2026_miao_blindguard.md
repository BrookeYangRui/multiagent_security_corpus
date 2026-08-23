# BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks

Authors: Rui Miao; Yixin Liu; Yili Wang; Xu Shen; Yue Tan; Yiwei Dai; Shirui Pan; Xin Wang

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.1819

Primary URL: https://aclanthology.org/2026.acl-long.1819/

Open access URL: https://aclanthology.org/2026.acl-long.1819.pdf

BibTeX key: miao2026blindguard

## Paper Type

Defense; Evaluation; Empirical study

## Scope

### System Studied

LLM-backed agents communicate for three rounds over chain, tree, star, and random graph topologies.

### Multi-Agent Dependency

The defense identifies anomalous members from individual, neighborhood, and global interaction patterns, then removes their graph edges to contain cross-agent propagation.

### Application Domain

Question answering and tool- or memory-augmented collaboration.

## Security Model

### Protected Assets

Collective answer integrity and availability of honest communication paths.

### Threat Actor

Three compromised member agents in the evaluated MAS.

### Trusted Components

The monitoring and remediation pipeline, normal-behavior training traces, and graph representation.

### Attacker Capabilities

Direct prompt attack, injected tool output, or poisoned memory that changes compromised-agent messages.

### Security Assumptions

The monitor observes agent outputs and the communication graph, and its remediation can prune bidirectional edges.

## Main Contribution

BlindGuard is an unsupervised graph-anomaly defense trained without attack labels. It combines a hierarchical agent encoder, synthetic feature corruption, anomaly scoring, and topology pruning to detect and isolate compromised members.

## Attack or Failure

### Attack Surface

Agent prompts, tool-return content, memory, and inter-agent messages.

### Attack Mechanism

Compromised agents inject misleading outputs that propagate over the communication graph.

### System-Level Failure

Adversarial messages distort the collective answer after multiple communication rounds.

### Security Consequence

Loss of collective decision integrity and propagation containment.

## Defense

### Defense Mechanism

The monitor encodes multi-scale interaction context, detects representation outliers, and prunes edges incident to predicted malicious agents.

### Intervention Point

Global communication graph and message-monitoring layer.

### Required Observability

Agent responses, neighborhood structure, and population-level interaction context.

### Assumptions

Normal MAS traces are available for training and the defender can isolate detected agents.

### Limitations

Evaluation uses simulated environments; detection acts after infiltration; adaptive attackers may evade the anomaly signal; and performance depends on interaction structure and observable responses.

## Evaluation

### Evaluated Systems

MAS instances using Qwen3-30B-A3B, DeepSeek-V3, and GPT-4o-mini backbones.

### Agent Configuration

Chain, tree, star, and random graphs with exactly three compromised agents in the main setup.

### Dataset or Environment

Direct prompt attacks use CSQA, MMLU, and GSM8K; tool attacks use InjecAgent; memory attacks follow PoisonRAG and CSQA.

### Baselines

No defense, supervised G-Safeguard, and unsupervised graph anomaly detectors DOMINANT, PREM, and TAM.

### Metrics

Attack Success Rate after three rounds (ASR@3) and malicious-agent detection AUC.

### Main Results

BlindGuard improves attack detection and lowers post-defense ASR across the evaluated attack types and topologies, while the supervised G-Safeguard baseline generally remains an upper bound for detection.

## Relation to Existing Work

### Papers Compared by the Authors

G-Safeguard, DOMINANT, PREM, and TAM.

### Claimed Research Gap

Existing graph defenses require labeled malicious-agent data and may not generalize to unknown attacks.

### Closest Related Work

G-Safeguard and graph anomaly detection methods.

### Difference From Prior Work

BlindGuard learns from normal behavior plus synthetic representation corruption rather than labeled attack traces.

## Relevance to Our SoK

### Included Concepts

Global observation, topology-aware detection, containment, unknown-attack evaluation, and trust assumptions.

### Taxonomy Implications

The defense locus is the communication graph; its functions are detection and containment, not pre-infiltration prevention.

### Supported Research Questions

What observation and intervention rights do topology-aware defenses require, and how broadly are they evaluated?

### Important Limitations

The evaluation protocol reuses several task and attack datasets; the paper does not present them as one new named benchmark.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| BlindGuard trains without attack-specific labels and detects anomalies from hierarchical interaction representations. | Explicit author claim | Paper | Abstract; 3 | 1; 4-6 | Figure 2 | Defense design and training contract. |
| The evaluation spans three attack families, four graph topologies, and three LLM backbones. | Explicit author claim | Paper | 4.1 | 6 | Table 1 | Evaluation matrix. |
| Main metrics are ASR@3 and malicious-agent detection AUC. | Explicit author claim | Paper | 4.1 | 6 | Table 1 | Metric definitions. |
| The evaluation protocol is indexed as an artifact but is not relabeled as a new benchmark. | Corpus interpretation | Paper | 4.1 | 6 | Table 1 | Classification based on the reusable cross-attack evaluation design. |

## Provenance

### Discovery Source

ACL Anthology; defense-artifact audit; prior corpus references.

### Discovery Query

BlindGuard multi-agent systems official publication

### Accessed Version

Published ACL 2026 version.

### Access Date

2026-08-06
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
