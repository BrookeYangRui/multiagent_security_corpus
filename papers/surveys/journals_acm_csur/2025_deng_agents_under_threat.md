# AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways

## Citation
Title: AI Agents Under Threat: A Survey of Key Security Challenges and Future Pathways
Authors: Zehang Deng; Yongjian Guo; Changzhou Han; Wanlun Ma; Junwu Xiong; Sheng Wen; Yang Xiang
Year: 2025
Venue: ACM Computing Surveys
DOI: 10.1145/3716628
Primary URL: https://doi.org/10.1145/3716628
Open access URL: https://dl.acm.org/doi/pdf/10.1145/3716628
BibTeX key: deng2025agentsunderthreat

## Paper Type
Survey

## Scope
### System Studied
LLM-based agents and their component attack surfaces.
### Multi-Agent Dependency
MAS risks are included but are not the primary organizing boundary.
### Application Domain
General agentic AI.

## Security Model
### Protected Assets
Agent confidentiality, integrity, availability, privacy, and safe action.
### Threat Actor
Users, external inputs, compromised tools, and malicious components.
### Trusted Components
Varies by surveyed work.
### Attacker Capabilities
Prompt, memory, tool, environment, and communication manipulation.
### Security Assumptions
Heterogeneous across the literature.

## Main Contribution
The survey organizes agent security threats, defenses, and future research pathways across the agent stack.

## Attack or Failure
### Attack Surface
Model, prompt, memory, tools, environment, and communication.
### Attack Mechanism
Varies across surveyed studies.
### System-Level Failure
Broad agent compromise; interaction-native properties receive partial coverage.
### Security Consequence
Security, privacy, and safety harms.

## Defense
### Defense Mechanism
Catalogs input filtering, monitoring, access control, isolation, and robustness methods.
### Intervention Point
Multiple agent layers.
### Required Observability
Varies.
### Assumptions
Varies.
### Limitations
The broad scope limits claim-level MAS coding.

## Evaluation
### Evaluated Systems
Not applicable; survey.
### Agent Configuration
Varies.
### Dataset or Environment
Not applicable.
### Baselines
Prior LLM-security surveys.
### Metrics
Literature coverage.
### Main Results
Taxonomy and open research directions.

## Relation to Existing Work
### Papers Compared by the Authors
LLM and agent-security surveys.
### Claimed Research Gap
Prior LLM surveys underrepresent autonomous agent behavior.
### Closest Related Work
He et al. and other agent-security surveys.
### Difference From Prior Work
Emphasizes a unified agent threat landscape.

## Relevance to Our SoK
### Included Concepts
Single-agent boundary, component attacks, and imported defenses.
### Taxonomy Implications
Comparator for deciding which risks are inherited versus interaction-native.
### Supported Research Questions
Which single-agent defenses are evaluated after multi-agent composition?
### Important Limitations
Do not count every cited agent paper as MAS-primary.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The survey organizes threats and defenses across agent components. | Explicit author claim | Paper | Taxonomy | 4-20 | Taxonomy figures | Organizing structure. |
| MAS is partial rather than the sole system boundary. | Corpus interpretation | Paper | Scope and taxonomy | 2-20 | Taxonomy figures | Scope coding. |

## Provenance
### Discovery Source
ACM Digital Library; Crossref DOI.
### Discovery Query
AI Agents Under Threat ACM Computing Surveys
### Accessed Version
Published ACM Computing Surveys 2025 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
