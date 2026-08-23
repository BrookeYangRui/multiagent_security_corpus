# GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `evaluation` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems

Authors: Pablo Mateo-Torrejón; Alfonso Sánchez-Macián

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2604.24477

Primary URL: https://arxiv.org/abs/2604.24477

Open access URL: https://arxiv.org/pdf/2604.24477

BibTeX key: mateotorrejon2026gammaf

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied
Debating LLM agents represented as attributed communication graphs.

### Multi-Agent Dependency
Detection and remediation use message content together with network neighborhood and dynamic topology.

### Application Domain
Knowledge and mathematical reasoning tasks.

## Security Model

### Protected Assets
Collective answer integrity and operational cost.

### Threat Actor
Prompt-infected or compromised communicating agent.

### Trusted Components
Data-generation pipeline, benchmark runner, labels, and isolation mechanism.

### Attacker Capabilities
Generate adversarial messages intended to steer peer answers.

### Security Assumptions
The framework has access to the attributed communication graph.

## Main Contribution

GAMMAF standardizes synthetic interaction-data generation and live benchmarking for graph-based MAS anomaly detectors. It evaluates XG-Guard and BlindGuard across several topologies and tasks while measuring both detection and post-isolation system behavior.

## Attack or Failure

### Attack Surface
Inter-agent debate messages and graph neighborhoods.

### Attack Mechanism
Malicious nodes steer deliberation through adversarial outputs.

### System-Level Failure
Wrong collective answer or excessive debate cost.

### Security Consequence
Decision-integrity and resource-efficiency loss.

## Defense

### Defense Mechanism
Graph anomaly detection followed by dynamic isolation.

### Intervention Point
Topology and communication layer.

### Required Observability
Messages, graph structure, node labels during training, and live rounds.

### Assumptions
Flagged agents can be removed from the interaction graph.

### Limitations
Synthetic attacks and benchmark tasks may not cover open-ended tool workflows.

## Evaluation

### Evaluated Systems
XG-Guard and BlindGuard within the common runner.

### Agent Configuration
Chain, tree, and random debate topologies.

### Dataset or Environment
MMLU-Pro, GSM8K, and related knowledge tasks.

### Baselines
Two graph-based defense baselines and undefended configurations.

### Metrics
Agent accuracy, Attack Success Rate, malicious-agent detection, token cost, and execution efficiency.

### Main Results
Effective isolation recovers integrity and reduces token use by shortening adversarial deliberation.

## Relation to Existing Work

### Papers Compared by the Authors
G-Safeguard, NetSafe, XG-Guard, and BlindGuard.

### Claimed Research Gap
Defense implementations use incompatible data and execution environments.

### Closest Related Work
Graph-based MAS defense studies.

### Difference From Prior Work
GAMMAF is an evaluation architecture, not a new defense.

## Relevance to Our SoK

### Included Concepts
Topology defense, observer scope, detection, containment, and cost.

### Taxonomy Implications
Separates detection performance from restored system utility.

### Supported Research Questions
Can graph defenses be compared under one attack, task, and topology contract?

### Important Limitations
Current evidence is preprint-only and reproduces a limited defense set.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| GAMMAF has data-generation and defense-benchmarking pipelines. | Explicit author claim | Paper | Abstract; 3 | 1; 5-8 | Figure 2 | Architecture. |
| It compares XG-Guard and BlindGuard across multiple topologies and tasks. | Explicit author claim | Paper | Abstract; 4 | 1; 8-13 | Main tables | Evaluation scope. |

## Provenance

### Discovery Source
arXiv; local bibliography screening.

### Discovery Query
graph anomaly monitoring benchmark LLM multi-agent

### Accessed Version
arXiv v1.

### Access Date
2026-08-05

### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-05
