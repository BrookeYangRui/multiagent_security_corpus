# Seven Security Challenges in Cross-Domain Multi-Agent LLM Systems

## Citation
Title: Seven Security Challenges in Cross-Domain Multi-Agent LLM Systems
Authors: Ronny Ko; Jiseong Chung; Shuyuan Zheng; Chuan Xiao; Tae-Wan Kim; Makoto Onizuka; Won-Yong Shin
Year: 2026
Venue: npj Artificial Intelligence
DOI: 10.1038/s44387-026-00128-9
Primary URL: https://doi.org/10.1038/s44387-026-00128-9
Open access URL: https://www.nature.com/articles/s44387-026-00128-9.pdf
BibTeX key: ko2026sevenchallenges

## Paper Type
Survey; Position paper

## Scope
### System Studied
Cross-domain LLM agents interacting across organizational and technical boundaries.
### Multi-Agent Dependency
The challenges arise from cross-agent trust, interoperability, shared context, and cascading behavior.
### Application Domain
Cross-domain agent ecosystems.

## Security Model
### Protected Assets
Identity, trust, privacy, integrity, accountability, and availability.
### Threat Actor
Malicious agents, external attackers, and compromised infrastructure.
### Trusted Components
Depends on the challenge and proposed research direction.
### Attacker Capabilities
Cross-domain impersonation, manipulation, leakage, and coordination abuse.
### Security Assumptions
The paper frames open challenges rather than one fixed model.

## Main Contribution
The paper identifies seven security challenges that emerge when heterogeneous LLM agents interact across domains and proposes research directions for secure interoperability.

## Attack or Failure
### Attack Surface
Identity, communication, memory, delegation, and governance boundaries.
### Attack Mechanism
Varies across the seven challenges.
### System-Level Failure
Trust and policy fail to compose across domains.
### Security Consequence
Integrity, privacy, and accountability loss.

## Defense
### Defense Mechanism
Discusses authentication, policy, monitoring, privacy, and governance directions.
### Intervention Point
Protocol and cross-domain control planes.
### Required Observability
Varies by proposed direction.
### Assumptions
Interoperable identity and policy metadata can be established.
### Limitations
This is a challenge paper rather than a systematic corpus audit.

## Evaluation
### Evaluated Systems
Not applicable.
### Agent Configuration
Conceptual cross-domain systems.
### Dataset or Environment
Not applicable.
### Baselines
Not applicable.
### Metrics
Not reported.
### Main Results
Seven research challenges and mitigation directions.

## Relation to Existing Work
### Papers Compared by the Authors
Agent security, distributed systems, and cross-domain trust work.
### Claimed Research Gap
Single-domain agent controls do not compose across heterogeneous domains.
### Closest Related Work
Multi-agent security position papers.
### Difference From Prior Work
The focus is explicitly cross-domain interoperability.

## Relevance to Our SoK
### Included Concepts
Membership, identity, delegation, contextual integrity, and distributed authority.
### Taxonomy Implications
Supports system-model dimensions but does not provide an empirical failure denominator.
### Supported Research Questions
Which assumptions break at organizational boundaries?
### Important Limitations
Challenge enumeration should not be coded as prevalence evidence.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper frames seven cross-domain MAS security challenges. | Explicit author claim | Paper | Main text | 1-8 | Challenge headings | Organizing contribution. |
| The work is a position/challenge synthesis rather than an empirical audit. | Corpus interpretation | Paper | Methods and main text | 1-8 | None | Evidence maturity coding. |

## Provenance
### Discovery Source
Nature official article; Crossref DOI.
### Discovery Query
cross-domain multi-agent LLM seven security challenges
### Accessed Version
Published npj Artificial Intelligence 2026 version.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
