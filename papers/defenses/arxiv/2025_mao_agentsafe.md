# AgentSafe: Safeguarding Large Language Model-based Multi-agent Systems via Hierarchical Data Management

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `defense` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation
Title: AgentSafe: Safeguarding Large Language Model-based Multi-agent Systems via Hierarchical Data Management
Authors: Junyuan Mao; Fanci Meng; Yifan Duan; Miao Yu; Xiaojun Jia; Junfeng Fang; Yuxuan Liang; Kun Wang; Qingsong Wen
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2503.04392
Primary URL: https://arxiv.org/abs/2503.04392
Open access URL: https://arxiv.org/pdf/2503.04392
BibTeX key: mao2025agentsafe

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
LLM agents exchanging messages and using persistent memories with different sensitivity levels.
### Multi-Agent Dependency
Authorization depends on sender, receiver, information level, and cross-agent memory access.
### Application Domain
General collaborative agents.

## Security Model
### Protected Assets
Sensitive messages and memory integrity.
### Threat Actor
Unauthorized or impersonating member agents.
### Trusted Components
ThreatSieve, HierarCache, identity metadata, and policy labels.
### Attacker Capabilities
Request unauthorized information, impersonate authority, or poison shared memory.
### Security Assumptions
Agents and data can be assigned reliable security levels.

## Main Contribution
AgentSafe combines ThreatSieve for authority-aware communication checks with HierarCache for hierarchical memory access and poisoning defense.

## Attack or Failure
### Attack Surface
Messages and shared memory.
### Attack Mechanism
Unauthorized access, impersonation, or malicious memory writes.
### System-Level Failure
Information crosses role boundaries or poisoned state influences peers.
### Security Consequence
Confidentiality and integrity loss.

## Defense
### Defense Mechanism
Hierarchical data labels, authority verification, and protected memory management.
### Intervention Point
Message and memory layers.
### Required Observability
Identity, authority, message provenance, and memory labels.
### Assumptions
Policy labels are correct and enforcement components are trusted.
### Limitations
The paper notes reliance on predefined hierarchies and evaluated LLM/task settings.

## Evaluation
### Evaluated Systems
Llama, GPT-3.5, GPT-4o, and other LLM-agent configurations.
### Agent Configuration
Role- and authority-stratified collaborating agents.
### Dataset or Environment
Communication and memory attack scenarios.
### Baselines
Unprotected and component-ablated systems.
### Metrics
Attack prevention, task utility, and scalability.
### Main Results
The authors report reduced unauthorized access and poisoning with limited utility loss.

## Relation to Existing Work
### Papers Compared by the Authors
Prompt guardrails and memory defenses.
### Claimed Research Gap
Existing safeguards lack cross-agent authority and memory hierarchy.
### Closest Related Work
Access control and agent-memory protection.
### Difference From Prior Work
AgentSafe couples communication authorization with memory policy.

## Relevance to Our SoK
### Included Concepts
Authority distribution, identity, contextual integrity, and memory defense.
### Taxonomy Implications
Defense loci are message and shared state; function is prevention.
### Supported Research Questions
Which metadata must survive delegation for access control?
### Important Limitations
Preprint evidence and administratively assigned labels limit maturity.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| AgentSafe combines ThreatSieve and HierarCache. | Explicit author claim | Paper | 3 | 3-6 | Framework figure | Core architecture. |
| Evaluation spans several commercial and open LLMs. | Explicit author claim | Paper | 4 | 6-9 | Setup table | Evaluated models. |
| Policy correctness is part of the trusted computing base. | Corpus interpretation | Paper | 3 | 3-6 | Policy definitions | Trust assumption. |

## Provenance
### Discovery Source
arXiv API; prior corpus defense scan.
### Discovery Query
multi-agent hierarchical data security AgentSafe
### Accessed Version
arXiv v2.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
