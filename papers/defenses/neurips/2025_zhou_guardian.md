# GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `NeurIPS` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling
Authors: Jialong Zhou; Lichao Wang; Xiao Yang
Year: 2025
Venue: NeurIPS
DOI: Not reported
Primary URL: https://proceedings.neurips.cc/paper_files/paper/2025/hash/0bc795afae289ed465a65a3b4b1f4eb7-Abstract-Conference.html
Open access URL: https://proceedings.neurips.cc/paper_files/paper/2025/file/0bc795afae289ed465a65a3b4b1f4eb7-Paper-Conference.pdf
BibTeX key: zhou2025guardian

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Multi-turn LLM-agent collaborations represented as temporal attributed graphs.
### Multi-Agent Dependency
The method detects anomalous nodes and edges from changing cross-agent interactions and prunes suspicious communication.
### Application Domain
Collaborative reasoning and debate.

## Security Model
### Protected Assets
Collective answer integrity and trusted communication.
### Threat Actor
Compromised communicating agents.
### Trusted Components
The temporal graph encoder-decoder and pruning controller.
### Attacker Capabilities
Inject adversarial messages into collaboration.
### Security Assumptions
The monitor observes temporally ordered messages and graph identities.

## Main Contribution
GUARDIAN constructs a temporal attributed graph of MAS communication, detects anomalous nodes and edges with an unsupervised encoder-decoder, and removes high-risk edges.

## Attack or Failure
### Attack Surface
Multi-round messages and influence paths.
### Attack Mechanism
Adversarial contributions alter later agents' reasoning.
### System-Level Failure
Malicious influence propagates through the temporal graph.
### Security Consequence
Collective accuracy and integrity degrade.

## Defense
### Defense Mechanism
Temporal graph reconstruction, anomaly scoring, and edge pruning.
### Intervention Point
Messages and topology.
### Required Observability
Global timestamped interaction graph and message attributes.
### Assumptions
The monitor can suppress communication edges.
### Limitations
The evaluation focuses on small populations and simulated attack settings.

## Evaluation
### Evaluated Systems
LLM collaborations with several backbone models.
### Agent Configuration
Main experiments use four agents; scalability experiments use three to seven.
### Dataset or Environment
Reasoning and question-answering benchmarks under adversarial communication.
### Baselines
No-defense, graph anomaly, and MAS safeguard baselines.
### Metrics
Accuracy, anomaly detection rate, false discovery rate, and runtime.
### Main Results
The authors report improved detection and restored collaboration accuracy across tested attacks.

## Relation to Existing Work
### Papers Compared by the Authors
Graph anomaly detection and LLM-MAS safeguards.
### Claimed Research Gap
Static graph models miss time-dependent malicious influence.
### Closest Related Work
G-Safeguard and temporal graph anomaly detection.
### Difference From Prior Work
GUARDIAN explicitly models interaction order and edge anomalies.

## Relevance to Our SoK
### Included Concepts
Temporal graph monitoring, detection, containment, and observer scope.
### Taxonomy Implications
The defense contract assumes global trace visibility and topology control.
### Supported Research Questions
How often do defenses rely on privileged global observers?
### Important Limitations
Small-agent evaluation limits evidence for internet-scale systems.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| GUARDIAN uses temporal attributed graphs and unsupervised anomaly detection. | Explicit author claim | Paper | 3-4 | 3-6 | Method figures | Framework definition. |
| Experiments include three-to-seven-agent scalability tests. | Explicit author claim | Paper | 5 | 7 | Experimental setup | Agent-count range. |
| Edge pruning makes the defense a containment mechanism. | Corpus interpretation | Paper | 4 | 5-6 | Algorithm | Intervention action. |

## Provenance
### Discovery Source
NeurIPS proceedings; prior corpus defense scan.
### Discovery Query
GUARDIAN safeguarding LLM multi-agent NeurIPS
### Accessed Version
Published NeurIPS 2025 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
