# SentinelNet: Safeguarding Multi-Agent Collaboration Through Credit-Based Dynamic Threat Detection

## Citation
Title: SentinelNet: Safeguarding Multi-Agent Collaboration Through Credit-Based Dynamic Threat Detection
Authors: Yang Feng; Xudong Pan
Year: 2026
Venue: The Web Conference
DOI: 10.1145/3774904.3792462
Primary URL: https://doi.org/10.1145/3774904.3792462
Open access URL: https://arxiv.org/pdf/2510.16219
BibTeX key: feng2026sentinelnet

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Decentralized debating LLM agents with locally maintained neighbor credit.
### Multi-Agent Dependency
Each agent ranks peer messages and removes low-credit neighbors, changing distributed communication paths.
### Application Domain
Multi-agent debate and collaborative reasoning.

## Security Model
### Protected Assets
Collective answer integrity and decentralized availability.
### Threat Actor
Malicious member agents.
### Trusted Components
Local credit detectors trained on augmented adversarial trajectories.
### Attacker Capabilities
Send manipulative messages through legitimate debate channels.
### Security Assumptions
Local histories contain a learnable malicious signal and enough honest neighbors remain.

## Main Contribution
SentinelNet trains credit-based local detectors with contrastive adversarial trajectories and applies bottom-k neighbor elimination to suppress malicious influence without a central monitor.

## Attack or Failure
### Attack Surface
Peer debate messages.
### Attack Mechanism
Malicious participants repeatedly influence neighboring agents.
### System-Level Failure
Distributed debate converges on corrupted answers.
### Security Consequence
Collective decision-integrity loss.

## Defense
### Defense Mechanism
Local credibility estimation and dynamic neighbor elimination.
### Intervention Point
Peer messages and local topology.
### Required Observability
Each agent's received-message history and neighbor identities.
### Assumptions
Training attacks represent deployment behavior and local pruning does not fragment honest collaboration.
### Limitations
The authors identify adaptation to more diverse attacks and topologies as future work.

## Evaluation
### Evaluated Systems
LLM-agent debate systems.
### Agent Configuration
Distributed peers across topology and adversarial-ratio variations.
### Dataset or Environment
Reasoning and knowledge tasks including MMLU subsets.
### Baselines
Unprotected debate and centralized or static defense variants.
### Metrics
Detection rate, task accuracy, and rounds to detection.
### Main Results
The authors report near-100% detection within two rounds and recovery of 95% of clean-system accuracy in highlighted experiments.

## Relation to Existing Work
### Papers Compared by the Authors
Centralized safeguards and malicious-agent detection methods.
### Claimed Research Gap
Central monitors are reactive and create single points of failure.
### Closest Related Work
Trust-aware graph defense.
### Difference From Prior Work
SentinelNet places learned detectors at every participant.

## Relevance to Our SoK
### Included Concepts
Distributed observation, credit, topology adaptation, and containment.
### Taxonomy Implications
Defense locus is local message/topology; functions are detection and containment.
### Supported Research Questions
What coverage is possible without global trace access?
### Important Limitations
Local visibility may miss coalition-level behavior with individually plausible messages.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| SentinelNet uses contrastive credit detectors and bottom-k elimination. | Explicit author claim | Paper | 4 | 4-7 | Framework figure | Method. |
| Authors report near-perfect two-round detection and 95% accuracy recovery. | Explicit author claim | Paper | Abstract; 5 | 1; 7-10 | Results tables | Highlighted result. |
| Observer scope is decentralized and local. | Corpus interpretation | Paper | 4 | 4-7 | Framework figure | Detector placement. |

## Provenance
### Discovery Source
ACM DOI registry; WWW publication metadata; arXiv full text.
### Discovery Query
SentinelNet WWW 2026 DOI
### Accessed Version
Published WWW 2026 record; author preprint used for full text.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
