# Safe Systems with Unsafe Agents

## Citation
Title: Safe Systems with Unsafe Agents
Authors: Jeremy Bellay; J. Timothy Balint; Stephen A. Boxwell; Jeffrey Geppert
Year: 2025
Venue: AAMAS Blue Sky
DOI: Not reported
Primary URL: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2849.pdf
Open access URL: https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p2849.pdf
BibTeX key: bellay2025safesystems

## Paper Type
Position paper; Theoretical analysis

## Scope
### System Studied
Multi-agent systems whose individual components may be unsafe or unreliable while system architecture enforces acceptable outcomes.
### Multi-Agent Dependency
The central question is whether collective structure can yield safety without assuming every member is aligned.
### Application Domain
General autonomous multi-agent systems.

## Security Model
### Protected Assets
System-level safety and mission integrity.
### Threat Actor
Unsafe, faulty, or adversarial member agents.
### Trusted Components
System architecture, constraints, and verification mechanisms.
### Attacker Capabilities
Members may produce unsafe local actions or messages.
### Security Assumptions
System controls can restrict the effects of untrusted components.

## Main Contribution
The paper argues for engineering system-level safety properties that do not require every participating agent to be individually safe.

## Attack or Failure
### Attack Surface
Composition of unreliable agents.
### Attack Mechanism
Unsafe local behavior enters collective execution.
### System-Level Failure
Local assumptions fail to compose into global safety.
### Security Consequence
Mission or safety invariant violation.

## Defense
### Defense Mechanism
Architectural constraints, redundancy, monitoring, and system-level verification directions.
### Intervention Point
System design and coordination.
### Required Observability
Depends on the proposed system invariant.
### Assumptions
The architecture can mediate consequential actions.
### Limitations
Blue-sky position paper; it does not provide a complete implementation or benchmark.

## Evaluation
### Evaluated Systems
Not applicable.
### Agent Configuration
Conceptual heterogeneous systems.
### Dataset or Environment
Not applicable.
### Baselines
Agent-local alignment framing.
### Metrics
Not reported.
### Main Results
Conceptual architecture agenda.

## Relation to Existing Work
### Papers Compared by the Authors
Safe systems engineering and agent alignment.
### Claimed Research Gap
Requiring every component to be safe is brittle and unrealistic.
### Closest Related Work
Fault-tolerant distributed systems.
### Difference From Prior Work
Applies system-safety reasoning to autonomous agent composition.

## Relevance to Our SoK
### Included Concepts
Composition boundary, system invariant, untrusted members, and defense placement.
### Taxonomy Implications
Supports defining failures by violated global properties.
### Supported Research Questions
When can architecture contain locally unsafe behavior?
### Important Limitations
Conceptual claims should not be treated as empirical defense coverage.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper argues that safe systems need not assume safe agents. | Explicit author claim | Paper | Main text | 1-4 | None | Core thesis. |
| It is system-model evidence rather than evaluated defense evidence. | Corpus interpretation | Paper | Main text | 1-4 | None | Evidence maturity. |

## Provenance
### Discovery Source
AAMAS official proceedings.
### Discovery Query
site:ifaamas.org "Safe Systems with Unsafe Agents"
### Accessed Version
Published AAMAS 2025 Blue Sky paper.
### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction
Model and version, if automatically generated: Not recorded
### Verification Status
agent_unverified
### Last Updated
2026-08-06
