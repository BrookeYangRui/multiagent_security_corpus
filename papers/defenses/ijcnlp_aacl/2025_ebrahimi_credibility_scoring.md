# An Adversary-Resistant Multi-Agent LLM System via Credibility Scoring

## Citation
Title: An Adversary-Resistant Multi-Agent LLM System via Credibility Scoring
Authors: Sana Ebrahimi; Mohsen Dehghankar; Abolfazl Asudeh
Year: 2025
Venue: IJCNLP-AACL
DOI: 10.18653/v1/2025.ijcnlp-long.90
Primary URL: https://aclanthology.org/2025.ijcnlp-long.90/
Open access URL: https://aclanthology.org/2025.ijcnlp-long.90.pdf
BibTeX key: ebrahimi2025credibility

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Iterative multi-agent question answering with an aggregation stage.
### Multi-Agent Dependency
Credibility is learned from each agent's past contribution to group outcomes and then weights collective aggregation.
### Application Domain
Collaborative question answering.

## Security Model
### Protected Assets
Collective answer integrity.
### Threat Actor
Adversarial or persistently low-performing member agents.
### Trusted Components
Contribution evaluator and credibility-aware aggregator.
### Attacker Capabilities
Submit misleading answers during iterative collaboration.
### Security Assumptions
Past contribution quality can be estimated and agent identities persist across tasks.

## Main Contribution
The paper models collaboration as an iterative game, updates per-agent credibility from prior contribution quality, and uses credibility-weighted aggregation to resist adversarial influence.

## Attack or Failure
### Attack Surface
Agent contributions and final aggregation.
### Attack Mechanism
Malicious members submit incorrect answers to steer the group.
### System-Level Failure
Unweighted aggregation accepts adversarial contributions.
### Security Consequence
Collective decision-integrity loss.

## Defense
### Defense Mechanism
Historical credibility scoring and credibility-aware aggregation.
### Intervention Point
Coordination and aggregation protocol.
### Required Observability
Agent identity, contribution history, and estimated contribution quality.
### Assumptions
Stable identities and a trustworthy scoring signal.
### Limitations
Identity churn, Sybils, and coordinated manipulation of the evaluator are not the central evaluated setting.

## Evaluation
### Evaluated Systems
Multi-agent LLM question-answering teams.
### Agent Configuration
Iterative agents with benign and adversarial population ratios.
### Dataset or Environment
Multiple knowledge and reasoning tasks.
### Baselines
Standard aggregation and contribution-scoring variants.
### Metrics
Final answer accuracy and robustness by adversarial fraction.
### Main Results
The authors report resilience gains, including adversary-majority settings under their scoring assumptions.

## Relation to Existing Work
### Papers Compared by the Authors
Voting, debate, and contribution-based aggregation methods.
### Claimed Research Gap
Conventional aggregation treats unreliable and reliable contributors too similarly.
### Closest Related Work
Trust- and contribution-weighted aggregation.
### Difference From Prior Work
Credibility is accumulated across queries rather than inferred from one response alone.

## Relevance to Our SoK
### Included Concepts
Identity persistence, trust, aggregation, adversary fraction, and decision integrity.
### Taxonomy Implications
Defense locus is coordination; function is prevention through influence attenuation.
### Supported Research Questions
Which assumptions support claims beyond simple majority voting?
### Important Limitations
The result is not equivalent to classical Byzantine agreement under an asynchronous network.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Credibility is learned from past contributions and used in aggregation. | Explicit author claim | Paper | 2-4 | 3-6 | System overview | Scoring and aggregation design. |
| Experiments include adversary-majority settings. | Explicit author claim | Paper | 5 | 7-10 | Results tables | Population-ratio evaluation. |
| Stable identity is a prerequisite for longitudinal credibility. | Corpus interpretation | Paper | 3 | 4-5 | Scoring equations | Required state linkage. |

## Provenance
### Discovery Source
ACL Anthology; prior corpus defense scan.
### Discovery Query
adversary resistant multi-agent credibility official
### Accessed Version
Published IJCNLP-AACL 2025 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
