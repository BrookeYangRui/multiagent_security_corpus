# Maris: A Formally Verifiable Privacy Policy Enforcement Paradigm for Multi-Agent Collaboration Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `defense` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: Maris: A Formally Verifiable Privacy Policy Enforcement Paradigm for Multi-Agent Collaboration Systems
Authors: Jian Cui; Zichuan Li; Chi Wang; Luyi Xing; Xiaojing Liao
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2505.04799
Primary URL: https://arxiv.org/abs/2505.04799
Open access URL: https://arxiv.org/pdf/2505.04799
BibTeX key: cui2025maris

## Paper Type
Defense; Theoretical analysis; Evaluation

## Scope
### System Studied
Multi-agent collaboration with messages, LLM calls, tools, users, and sensitive data flows.
### Multi-Agent Dependency
Policies constrain which principals and endpoints may receive data across agent boundaries.
### Application Domain
Privacy-sensitive collaborative workflows.

## Security Model
### Protected Assets
Sensitive data and contextual confidentiality.
### Threat Actor
Eavesdroppers, injected instructions, or over-privileged agents.
### Trusted Components
Reference monitors, policy compiler, labels, and verification runtime.
### Attacker Capabilities
Cause data to flow along unauthorized message or tool paths.
### Security Assumptions
All relevant flows pass through Maris enforcement and policies are correct.

## Main Contribution
Maris embeds reference monitors into agent communication and offers a policy language and formal verification for fine-grained information-flow enforcement.

## Attack or Failure
### Attack Surface
Messages, tools, LLM endpoints, and external users.
### Attack Mechanism
Sensitive content is forwarded or elicited outside its permitted context.
### System-Level Failure
Distributed data flows violate principal-specific policy.
### Security Consequence
Confidentiality and contextual-integrity loss.

## Defense
### Defense Mechanism
Runtime reference monitors plus formally checked flow policies.
### Intervention Point
Every message and tool boundary.
### Required Observability
Data labels, principal identity, sender/receiver, and tool endpoints.
### Assumptions
Complete mediation and correct policy specification.
### Limitations
Policy authoring, label accuracy, covert channels, and unmediated side effects remain difficult.

## Evaluation
### Evaluated Systems
Prototype multi-agent applications.
### Agent Configuration
Agents with mediated messaging and tool registration.
### Dataset or Environment
Privacy policies and attack scenarios in representative workflows.
### Baselines
Unprotected frameworks and prompt-only privacy controls.
### Metrics
Policy enforcement, overhead, and application utility.
### Main Results
The authors report effective flow blocking with practical prototype overhead.

## Relation to Existing Work
### Papers Compared by the Authors
Information-flow control, reference monitors, and prompt defenses.
### Claimed Research Gap
Agent frameworks lack enforceable cross-principal privacy policy.
### Closest Related Work
Language-based information-flow control.
### Difference From Prior Work
Maris adapts complete mediation and verification to agent communication and tools.

## Relevance to Our SoK
### Included Concepts
Principal identity, provenance, complete mediation, and formal confidentiality policy.
### Taxonomy Implications
Defense loci are message, tool, and shared state; function is prevention.
### Supported Research Questions
Can graph-aware information flow preserve principal context through delegation?
### Important Limitations
Formal guarantees cover the modeled enforcement path, not semantic covert channels.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Maris uses embedded reference monitors and a verifiable policy model. | Explicit author claim | Paper | 3-4 | 4-9 | Architecture figure | Enforcement design. |
| The implementation mediates registered messages and tools. | Explicit author claim | Paper | 4 | 8-10 | API description | Prototype boundary. |
| Guarantee strength depends on complete mediation. | Corpus interpretation | Paper | 3 | 4-8 | Threat model | Trusted-path assumption. |

## Provenance
### Discovery Source
arXiv API; privacy-defense scan.
### Discovery Query
multi-agent privacy policy enforcement Maris
### Accessed Version
arXiv v5.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
