# PRISM: Generation-Time Detection and Mitigation of Secret Leakage in Multi-Agent LLM Pipelines

## Citation
Title: PRISM: Generation-Time Detection and Mitigation of Secret Leakage in Multi-Agent LLM Pipelines
Authors: Riya Tapwal; Abhishek Kumar; Carsten Maple
Year: 2026
Venue: arXiv
DOI: 10.48550/arXiv.2605.10614
Primary URL: https://arxiv.org/abs/2605.10614
Open access URL: https://arxiv.org/pdf/2605.10614
BibTeX key: tapwal2026prism

## Paper Type
Defense; Evaluation; Empirical study

## Scope
### System Studied
Multi-stage LLM-agent pipelines in which one agent can expose sensitive content to downstream generators.
### Multi-Agent Dependency
Leakage risk accumulates as content crosses repeated agent-generation boundaries.
### Application Domain
Credential-bearing agent workflows.

## Security Model
### Protected Assets
Secrets and credentials.
### Threat Actor
Leakage may be accidental or induced; no malicious member is required.
### Trusted Components
Generation-time risk monitor and masking or stopping policy.
### Attacker Capabilities
Elicit or propagate sensitive tokens through downstream context.
### Security Assumptions
Risk features can be estimated from black-box generation signals.

## Main Contribution
PRISM formalizes propagation amplification and accumulates token-level risk during generation to stop or redact leakage before a complete secret is emitted.

## Attack or Failure
### Attack Surface
Shared context and downstream generation.
### Attack Mechanism
Sensitive fragments are repeatedly exposed and regenerated across stages.
### System-Level Failure
Pipeline composition amplifies secret disclosure probability.
### Security Consequence
Cross-principal confidentiality loss.

## Defense
### Defense Mechanism
Sequential risk accumulation with generation-time stopping or masking.
### Intervention Point
Token generation and message boundary.
### Required Observability
Generated tokens, risk features, and pipeline position.
### Assumptions
Secret-like generations produce detectable signals before completion.
### Limitations
The paper notes black-box approximation error and difficulty with structured multi-step encodings.

## Evaluation
### Evaluated Systems
Multi-agent LLM pipelines under credential leakage scenarios.
### Agent Configuration
Sequential downstream generators.
### Dataset or Environment
Two-thousand-example evaluation split with multiple leakage transformations.
### Baselines
Regex, prompt safeguards, and LLM-as-judge filtering.
### Metrics
Leakage detection, mitigation, false positives, utility, and latency.
### Main Results
The authors report improved leakage mitigation with lower latency than post-generation judges.

## Relation to Existing Work
### Papers Compared by the Authors
Pattern matching, prompt defenses, and LLM judges.
### Claimed Research Gap
Existing methods act after generation or ignore accumulation across agents.
### Closest Related Work
Secret scanners and runtime output controls.
### Difference From Prior Work
PRISM intervenes during token generation and models cross-stage accumulation.

## Relevance to Our SoK
### Included Concepts
Cross-agent leakage, population scope, generation-time prevention, and observer variables.
### Taxonomy Implications
Defense locus is message/generation; functions are detection and prevention.
### Supported Research Questions
How should leakage denominators account for stage and component?
### Important Limitations
The preprint evaluates a bounded credential domain rather than arbitrary contextual privacy.

## Evidence
| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| PRISM models propagation amplification and sequential risk. | Explicit author claim | Paper | 3-4 | 4-8 | Framework figure | Formalization and method. |
| Evaluation uses 2,000 examples. | Explicit author claim | Paper | 5 | 8-10 | Evaluation setup | Denominator. |
| Black-box approximation and structured encodings are limitations. | Explicit author claim | Paper | Limitations | Appendix | Limitations text | Boundary conditions. |

## Provenance
### Discovery Source
arXiv API; privacy-defense scan.
### Discovery Query
PRISM secret leakage multi-agent pipeline
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
