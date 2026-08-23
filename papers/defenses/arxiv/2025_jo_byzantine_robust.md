# Byzantine-Robust Decentralized Coordination of LLM Agents

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `defense` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: Byzantine-Robust Decentralized Coordination of LLM Agents
Authors: Yongrae Jo; Chanik Park
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2507.14928
Primary URL: https://arxiv.org/abs/2507.14928
Open access URL: https://arxiv.org/pdf/2507.14928
BibTeX key: jo2025byzantinerobust

## Paper Type
Defense; Theoretical analysis; Evaluation

## Scope
### System Studied
Decentralized LLM agents coordinating without a permanent leader.
### Multi-Agent Dependency
Correctness and efficiency depend on the fraction of Byzantine participants and distributed aggregation.
### Application Domain
Open decentralized agent platforms.

## Security Model
### Protected Assets
Agreement quality, liveness, and resistance to malicious members.
### Threat Actor
Byzantine member agents.
### Trusted Components
Authenticated synchronous communication and protocol implementation.
### Attacker Capabilities
Submit arbitrary proposals or votes.
### Security Assumptions
Synchronous authenticated network and fewer than half Byzantine participants.

## Main Contribution
The paper proposes leaderless decentralized coordination designed to tolerate f<n/2 Byzantine agents under synchronous authenticated communication.

## Attack or Failure
### Attack Surface
Proposals, votes, and coordination rounds.
### Attack Mechanism
Malicious members delay or bias leader-based consensus.
### System-Level Failure
Coordination fails or accepts a poor proposal.
### Security Consequence
Agreement, validity, and availability degradation.

## Defense
### Defense Mechanism
Leaderless decentralized proposal and aggregation protocol.
### Intervention Point
Coordination protocol.
### Required Observability
Authenticated proposals and votes from the participant set.
### Assumptions
Synchrony, authentication, and bounded Byzantine fraction.
### Limitations
The f<n/2 claim is not a result under classical asynchronous unauthenticated Byzantine agreement.

## Evaluation
### Evaluated Systems
LLM-agent coordination tasks.
### Agent Configuration
Decentralized participants with varied Byzantine fractions.
### Dataset or Environment
Reasoning tasks and protocol simulations.
### Baselines
Leader-based and voting coordination.
### Metrics
Accuracy, latency, rounds, and robustness by f/n.
### Main Results
The authors report higher robustness and lower leader-failure cost under the stated assumptions.

## Relation to Existing Work
### Papers Compared by the Authors
Leader-based BFT and LLM-agent voting.
### Claimed Research Gap
Leader compromise causes repeated costly LLM consensus rounds.
### Closest Related Work
Byzantine coordination protocols.
### Difference From Prior Work
Removes a permanent leader and explicitly optimizes LLM invocation cost.

## Relevance to Our SoK
### Included Concepts
Byzantine fraction, synchrony, authentication, agreement, and termination.
### Taxonomy Implications
Defense locus is coordination; function is prevention under a normalized assumption set.
### Supported Research Questions
Which relaxed assumptions enable f<n/2 claims?
### Important Limitations
Preprint status and non-classical network assumptions must accompany every bound.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The protocol claims f<n/2 under synchronous authenticated communication. | Explicit author claim | Paper | Threat model; Theory | 3-7 | Theorems | Bound and assumptions. |
| The claim is not directly comparable to asynchronous f<n/3. | Corpus interpretation | Paper | Threat model | 3-4 | Assumption table | Assumption normalization. |

## Provenance
### Discovery Source
arXiv API; Byzantine audit corpus.
### Discovery Query
Byzantine robust decentralized coordination LLM agents
### Accessed Version
arXiv v1.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
