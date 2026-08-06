# A Survey on Trustworthy LLM Agents: Threats and Countermeasures

## Citation
Title: A Survey on Trustworthy LLM Agents: Threats and Countermeasures
Authors: Miao Yu; Fanci Meng; Xinyun Zhou; Shilong Wang; Junyuan Mao; Linsey Pan; Tianlong Chen; Kun Wang; Xinfeng Li; Yongfeng Zhang; Bo An; Qingsong Wen
Year: 2025
Venue: KDD
DOI: 10.1145/3711896.3736561
Primary URL: https://doi.org/10.1145/3711896.3736561
Open access URL: https://arxiv.org/pdf/2503.09648
BibTeX key: yu2025trustworthyagents

## Paper Type
Survey

## Scope
### System Studied
LLM agents and MAS decomposed into brain, memory, tools, users, agents, and environment.
### Multi-Agent Dependency
Other agents form an extrinsic trust surface, but MAS is one part of a larger modular taxonomy.
### Application Domain
General-purpose agentic systems.

## Security Model
### Protected Assets
Safety, robustness, privacy, fairness, and trustworthiness.
### Threat Actor
Users, peer agents, environment, and compromised components.
### Trusted Components
Varies across cited work.
### Attacker Capabilities
Intrinsic and extrinsic manipulation.
### Security Assumptions
Heterogeneous across literature.

## Main Contribution
TrustAgent organizes trustworthy-agent work into intrinsic and extrinsic components and surveys attacks, defenses, and evaluations.

## Attack or Failure
### Attack Surface
Brain, memory, tools, users, agents, and environment.
### Attack Mechanism
Varies.
### System-Level Failure
Broad trustworthiness failures, some interaction-dependent.
### Security Consequence
Security, privacy, robustness, and safety loss.

## Defense
### Defense Mechanism
Catalogs countermeasures by component and trust dimension.
### Intervention Point
Intrinsic and extrinsic modules.
### Required Observability
Varies.
### Assumptions
Varies.
### Limitations
The broad trustworthiness scope mixes security with adjacent safety and quality concerns.

## Evaluation
### Evaluated Systems
Not applicable; survey.
### Agent Configuration
Varies.
### Dataset or Environment
Not applicable.
### Baselines
Prior trustworthy-LLM surveys.
### Metrics
Literature coverage.
### Main Results
Modular taxonomy and research agenda.

## Relation to Existing Work
### Papers Compared by the Authors
Trustworthy LLM and agent surveys.
### Claimed Research Gap
LLM taxonomies omit agent modules and external relationships.
### Closest Related Work
Agent security and trustworthy-AI surveys.
### Difference From Prior Work
Explicit intrinsic/extrinsic agent decomposition.

## Relevance to Our SoK
### Included Concepts
Agent-as-peer attack surface, modular design, and trust dimensions.
### Taxonomy Implications
Useful design vocabulary but not a system-level failure taxonomy.
### Supported Research Questions
Where does interaction sit relative to component-centric taxonomies?
### Important Limitations
Not all trustworthiness entries meet the SoK's security inclusion criteria.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| TrustAgent separates intrinsic and extrinsic components. | Explicit author claim | Paper | Framework | 2-5 | Taxonomy figure | Organizing model. |
| Peer-agent interaction is one extrinsic module rather than the sole axis. | Corpus interpretation | Paper | Framework | 2-5 | Taxonomy figure | Comparative scope. |

## Provenance
### Discovery Source
ACM KDD proceedings; Crossref; arXiv full text.
### Discovery Query
trustworthy LLM agents threats countermeasures KDD
### Accessed Version
Published KDD 2025 record; author preprint used for full text.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
