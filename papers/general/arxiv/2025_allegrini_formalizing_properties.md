# Formalizing the Safety, Security, and Functional Properties of Agentic AI Systems

## Citation
Title: Formalizing the Safety, Security, and Functional Properties of Agentic AI Systems
Authors: Edoardo Allegrini; Ananth Shreekumar; Z. Berkay Celik
Year: 2025
Venue: arXiv
DOI: 10.48550/arXiv.2510.14133
Primary URL: https://arxiv.org/abs/2510.14133
Open access URL: https://arxiv.org/pdf/2510.14133
BibTeX key: allegrini2025formalizing

## Paper Type
Theoretical analysis; Position paper

## Scope
### System Studied
Agentic systems composed of host agents, MCP tool interactions, and A2A coordination.
### Multi-Agent Dependency
The formal model connects properties across host, tool, and inter-agent protocol boundaries.
### Application Domain
Protocol-based agentic systems.

## Security Model
### Protected Assets
Safety, security, and functional correctness.
### Threat Actor
Malicious or misconfigured protocol participants and tools.
### Trusted Components
Formal semantics and property monitors under the chosen model.
### Attacker Capabilities
Exploit mismatched assumptions across MCP and A2A composition.
### Security Assumptions
System behavior is represented by the proposed formal models.

## Main Contribution
The paper introduces host-agent and interaction models intended to express safety, security, and functional properties across MCP and A2A compositions.

## Attack or Failure
### Attack Surface
Host, tool, and agent protocol composition.
### Attack Mechanism
Semantic mismatch and exploitable coordination assumptions.
### System-Level Failure
Properties verified in isolation fail after protocol composition.
### Security Consequence
Safety and security invariant violation.

## Defense
### Defense Mechanism
Formal specification and property checking.
### Intervention Point
Design and verification layer.
### Required Observability
Modeled states, messages, capabilities, and transitions.
### Assumptions
The model faithfully captures implementation behavior.
### Limitations
Unmodeled semantics, opaque LLM behavior, and protocol evolution constrain guarantees.

## Evaluation
### Evaluated Systems
Formal examples and protocol compositions.
### Agent Configuration
Host, tool, and peer-agent interactions.
### Dataset or Environment
Not a benchmark.
### Baselines
Isolated protocol analyses.
### Metrics
Property expressiveness and formal checking outcomes.
### Main Results
The authors demonstrate how the model specifies cross-protocol properties.

## Relation to Existing Work
### Papers Compared by the Authors
MCP and A2A analyses, formal methods, and agent security models.
### Claimed Research Gap
Protocols are analyzed separately, leaving a semantic composition gap.
### Closest Related Work
Formal protocol and agent models.
### Difference From Prior Work
The model explicitly joins host and inter-agent semantics.

## Relevance to Our SoK
### Included Concepts
System model, capability, protocol, composition, and invariant.
### Taxonomy Implications
Supports adding shared state, capability distribution, and system properties to M.
### Supported Research Questions
Which variables are necessary to state collective security properties?
### Important Limitations
Preprint status and model abstraction limit implementation evidence.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The framework connects host-agent and interaction models. | Explicit author claim | Paper | Model | 3-8 | Formal definitions | System model. |
| It addresses MCP/A2A semantic composition. | Explicit author claim | Paper | Introduction; Model | 1-8 | Architecture figure | Research gap. |

## Provenance
### Discovery Source
arXiv API; protocol-model scan.
### Discovery Query
formalizing safety security functional agentic AI MCP A2A
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
