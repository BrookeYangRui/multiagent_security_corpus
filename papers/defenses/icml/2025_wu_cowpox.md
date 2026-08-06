# Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems

## Citation
Title: Cowpox: Towards the Immunity of VLM-based Multi-Agent Systems
Authors: Yutong Wu; Jie Zhang; Yiming Li; Chao Zhang; Qing Guo; Han Qiu; Nils Lukas; Tianwei Zhang
Year: 2025
Venue: ICML
DOI: Not reported
Primary URL: https://proceedings.mlr.press/v267/wu25aq.html
Open access URL: https://raw.githubusercontent.com/mlresearch/v267/main/assets/wu25aq/wu25aq.pdf
BibTeX key: wu2025cowpox

## Paper Type
Defense; Evaluation; Theoretical analysis; Empirical study

## Scope
### System Studied
Stateful VLM agents that exchange multimodal content and memory.
### Multi-Agent Dependency
Protective samples are distributed through the same population channels used by infectious jailbreaks.
### Application Domain
Multimodal agent societies.

## Security Model
### Protected Assets
Population-wide behavioral integrity.
### Threat Actor
An adversary seeding contagious multimodal jailbreak content.
### Trusted Components
The cure-generation and distribution process.
### Attacker Capabilities
Introduce infectious inputs that spread through agent memory and communication.
### Security Assumptions
Defenders can seed and disseminate cure samples before or during propagation.

## Main Contribution
Cowpox introduces distributed cure samples intended to immunize or recover VLM agents and analyzes conditions under which defensive propagation can dominate infection.

## Attack or Failure
### Attack Surface
Multimodal inputs, memory, and agent-to-agent transmission.
### Attack Mechanism
An infectious jailbreak propagates across agents.
### System-Level Failure
Population compromise grows through communication.
### Security Consequence
Loss of containment and behavioral integrity.

## Defense
### Defense Mechanism
Generate, seed, and propagate immunity-inducing samples.
### Intervention Point
Agent state and population communication.
### Required Observability
Population infection state for evaluation; deployment relies on access to distribution channels.
### Assumptions
Cure samples transfer across the target VLM population.
### Limitations
The paper notes model, task, and propagation assumptions; real open networks may not permit controlled cure distribution.

## Evaluation
### Evaluated Systems
VLM-based multi-agent systems.
### Agent Configuration
Networked populations under varying seed and propagation settings.
### Dataset or Environment
Multimodal harmful-query and propagation evaluations.
### Baselines
No defense and non-propagating safety interventions.
### Metrics
Infection, recovery, and benign-utility measures.
### Main Results
The authors report substantial population protection and recovery under evaluated assumptions.

## Relation to Existing Work
### Papers Compared by the Authors
Agent Smith and multimodal jailbreak defenses.
### Claimed Research Gap
Local defenses do not exploit population dynamics for recovery.
### Closest Related Work
Contagious attacks on VLM-agent networks.
### Difference From Prior Work
Cowpox turns propagation into a defensive distribution mechanism.

## Relevance to Our SoK
### Included Concepts
Contagion, containment, recovery, topology, and population metrics.
### Taxonomy Implications
Defense functions include prevention and recovery at agent and graph loci.
### Supported Research Questions
How should defensive and malicious reproduction dynamics be compared?
### Important Limitations
The evaluation contract is specialized to multimodal infection.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Cowpox distributes cure samples to immunize or recover agents. | Explicit author claim | Paper | 3-4 | 4-8 | Framework figure | Defense mechanism. |
| The paper includes theoretical robustness analysis. | Explicit author claim | Paper | 4 | 6-8 | Theorems | Formal conditions. |
| This is one of the corpus's few recovery-oriented defenses. | Corpus interpretation | Paper | 3-4 | 4-8 | Framework figure | Defense-function coding. |

## Provenance
### Discovery Source
PMLR; ICML proceedings; prior corpus defense scan.
### Discovery Query
Cowpox VLM multi-agent ICML
### Accessed Version
Published ICML 2025 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
