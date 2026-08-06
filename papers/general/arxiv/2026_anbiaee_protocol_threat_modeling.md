# Security Threat Modeling for Emerging AI-Agent Protocols: A Comparative Analysis of MCP, A2A, Agora, and ANP

## Citation
Title: Security Threat Modeling for Emerging AI-Agent Protocols: A Comparative Analysis of MCP, A2A, Agora, and ANP
Authors: Zeynab Anbiaee; Mahdi Rabbani; Mansur Mirani; Gunjan Piya; Igor Opushnyev; Ali Ghorbani; Sajjad Dadkhah
Year: 2026
Venue: arXiv
DOI: 10.48550/arXiv.2602.11327
Primary URL: https://arxiv.org/abs/2602.11327
Open access URL: https://arxiv.org/pdf/2602.11327
BibTeX key: anbiaee2026protocols

## Paper Type
Survey; Theoretical analysis

## Scope
### System Studied
MCP, A2A, Agora, and ANP protocol architectures and lifecycles.
### Multi-Agent Dependency
A2A, Agora, and ANP establish cross-agent identity, discovery, negotiation, and communication boundaries; MCP provides the tool-side comparator.
### Application Domain
Interoperable agent ecosystems.

## Security Model
### Protected Assets
Identity, authorization, message integrity, confidentiality, and protocol availability.
### Threat Actor
Malicious agents, servers, tools, intermediaries, and external attackers.
### Trusted Components
Protocol-specific identity and transport roots.
### Attacker Capabilities
Spoof, tamper, replay, escalate privilege, abuse discovery, or deny service.
### Security Assumptions
Compared protocols have distinct trust and lifecycle models.

## Main Contribution
The paper applies a structured threat-modeling framework to four emerging agent protocols and compares protocol-specific and cross-protocol risks.

## Attack or Failure
### Attack Surface
Discovery, authentication, session establishment, messages, delegation, and tools.
### Attack Mechanism
STRIDE-like spoofing, tampering, repudiation, disclosure, denial, and elevation threats.
### System-Level Failure
Protocol composition fails to preserve identity or authority.
### Security Consequence
Cross-domain security and interoperability loss.

## Defense
### Defense Mechanism
Maps threats to authentication, authorization, integrity, isolation, and audit controls.
### Intervention Point
Protocol lifecycle.
### Required Observability
Protocol messages, identities, state transitions, and delegated capabilities.
### Assumptions
Implementations expose and enforce the modeled controls.
### Limitations
Protocol specifications and implementations are evolving; analysis is not an exploit benchmark.

## Evaluation
### Evaluated Systems
Protocol specifications and representative implementations.
### Agent Configuration
Cross-agent and agent-tool interactions.
### Dataset or Environment
Not applicable.
### Baselines
Comparative protocol analysis.
### Metrics
Threat and control coverage.
### Main Results
Cross-protocol risk matrix and recommendations.

## Relation to Existing Work
### Papers Compared by the Authors
MCP security studies and agent-protocol documentation.
### Claimed Research Gap
No common protocol-centric risk framework spans these ecosystems.
### Closest Related Work
Protocol threat modeling.
### Difference From Prior Work
Directly compares four emerging standards under one method.

## Relevance to Our SoK
### Included Concepts
Protocol, identity, membership, delegation, authorization, and provenance.
### Taxonomy Implications
Profiles the interaction surface; protocol threats must still map to system-level failures.
### Supported Research Questions
Which security metadata survives cross-protocol translation?
### Important Limitations
Preprint analysis may age quickly as specifications change.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper compares MCP, A2A, Agora, and ANP under one threat model. | Explicit author claim | Paper | Method; Protocol sections | 3-18 | Comparison tables | Scope and method. |
| MCP is partly a tool-protocol comparator rather than a pure MAS protocol. | Corpus interpretation | Paper | MCP section | 5-8 | Architecture table | Scope coding. |

## Provenance
### Discovery Source
arXiv API; protocol keyword search.
### Discovery Query
security threat modeling MCP A2A Agora ANP
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
