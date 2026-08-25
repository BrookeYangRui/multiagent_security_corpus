# To Trust or Not to Trust: Attention-based Trust Management for LLM Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `defense` · venue `ACL` · signoff `2026-08-25`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: To Trust or Not to Trust: Attention-based Trust Management for LLM Multi-Agent Systems
Authors: Pengfei He; Zhenwei Dai; Xianfeng Tang; Yue Xing; Hui Liu; Jingying Zeng; Qiankun Peng; Shrivats Agrawal; Samarth Varshney; Suhang Wang; Jiliang Tang; Qi He
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2506.02546
Primary URL: https://arxiv.org/abs/2506.02546
Open access URL: https://arxiv.org/pdf/2506.02546
BibTeX key: he2025atrust

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
LLM agents that receive heterogeneous peer messages during collaboration.
### Multi-Agent Dependency
Trust scores estimate the reliability of peer communications and modulate their influence on the receiver.
### Application Domain
Collaborative question answering.

## Security Model
### Protected Assets
Collective answer integrity.
### Threat Actor
Unreliable, biased, deceptive, toxic, irrelevant, or low-quality member agents.
### Trusted Components
Multi-head attention analysis and the trust-management controller.
### Attacker Capabilities
Send protocol-valid but untrustworthy messages.
### Security Assumptions
The six trust dimensions are detectable from message and attention signals.

## Main Contribution
A-Trust defines six communication trust dimensions, derives an attention-based trust score, and uses it to filter or down-weight peer messages.

## Attack or Failure
### Attack Surface
Incoming inter-agent messages.
### Attack Mechanism
Unreliable contributions receive equal influence under ordinary aggregation.
### System-Level Failure
Low-quality or malicious messages distort collective reasoning.
### Security Consequence
Collective decision-integrity loss.

## Defense
### Defense Mechanism
Attention-derived multi-dimensional trust scoring and message filtering.
### Intervention Point
Message aggregation.
### Required Observability
Message content, sender identity, and model attention or derived trust features.
### Assumptions
Trust features remain stable across models and attacks.
### Limitations
The paper notes threshold trade-offs and incomplete coverage of unseen harmfulness; no official ACL record was verified at access time.

## Evaluation
### Evaluated Systems
Several LLM-agent configurations.
### Agent Configuration
Collaborating agents with injected untrustworthy peers.
### Dataset or Environment
Question-answering and trust-dimension datasets.
### Baselines
Unweighted communication and trust-filtering variants.
### Metrics
Trust classification, task accuracy, and attack resistance.
### Main Results
The authors report improved robustness across the evaluated harmful-message categories.

## Relation to Existing Work
### Papers Compared by the Authors
MAS trust, harmful-message detection, and attention analysis.
### Claimed Research Gap
Prior trust methods cover one harmfulness type rather than a unified message contract.
### Closest Related Work
Credibility scoring and message anomaly detection.
### Difference From Prior Work
A-Trust uses six interpretable trust dimensions and model attention.

## Relevance to Our SoK
### Included Concepts
Trust, message observability, identity, and aggregation.
### Taxonomy Implications
Defense locus is message/coordination; functions are detection and prevention.
### Supported Research Questions
Which internal model signals do defense contracts require?
### Important Limitations
Preprint status; an arXiv comment about acceptance is not treated as a formal publication.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| A-Trust defines six trust dimensions and an attention-based score. | Explicit author claim | Paper | 2-3 | 3-6 | Framework figure | Method. |
| Threshold selection trades sensitivity against false alarms. | Explicit author claim | Paper | Limitations | 9 | None | Boundary condition. |

## Provenance
### Discovery Source
arXiv API; defense completeness scan; ACL event-title verification.
### Discovery Query
A-Trust LLM multi-agent trust official publication
### Accessed Version
arXiv v2; no matching official ACL Anthology entry verified.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
