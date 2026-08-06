# The Trust Paradox in LLM-Based Multi-Agent Systems: When Collaboration Becomes a Security Vulnerability

## Citation

Title: The Trust Paradox in LLM-Based Multi-Agent Systems: When Collaboration Becomes a Security Vulnerability

Authors: Zijie Xu; Minfeng Qi; Shiqing Wu; Lefeng Zhang; Qiwen Wei; Han He; Ningran Li

Year: 2026

Venue: IEEE Transactions on Computational Social Systems

DOI: 10.1109/TCSS.2026.3695070

Primary URL: https://doi.org/10.1109/TCSS.2026.3695070

Open access URL: https://arxiv.org/abs/2510.18563

BibTeX key: xu2026trustparadox

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Closed-loop LLM-MAS workflows in which a parameterized trust level changes how readily agents share information and accept peer requests.

### Multi-Agent Dependency

The tested risk is an authorization differential between agents: increasing inter-agent trust improves coordination but also permits more cross-role disclosure and action. Exposure is measured over complete interaction chains rather than one model response.

### Application Domain

Scenario-game collaboration across personal, organizational, and emergency contexts.

## Security Model

### Protected Assets

Sensitive information boundaries and least-authority constraints between agent roles.

### Threat Actor

Peer agents making requests that range from ordinary or emergent to overtly malicious; the study also measures non-adversarial over-sharing.

### Trusted Components

The scenario labels, Minimum Necessary Information policy, experiment controller, and optional guardian component.

### Attacker Capabilities

A requester interacts through normal channels and benefits from elevated trust; it does not modify model weights or orchestration code.

### Security Assumptions

Trust can be explicitly parameterized and MNI labels provide a valid reference for necessary disclosure.

## Main Contribution

The paper formalizes the Trust-Vulnerability Paradox and introduces Over-Exposure Rate and Authorization Drift to measure disclosure and sensitivity to trust. It evaluates 1,488 interaction chains across models, orchestration frameworks, and trust settings, then tests two defenses.

## Attack or Failure

### Attack Surface

Inter-agent requests, trust-conditioned information sharing, and cross-role authorization.

### Attack Mechanism

High trust weakens information gates and lets plausible peer requests elicit data beyond the MNI baseline.

### System-Level Failure

An agent discloses information or authorizes behavior beyond what the receiving role needs.

### Security Consequence

Cross-principal confidentiality and authorization-boundary failure.

## Defense

### Defense Mechanism

Sensitive Information Repartitioning separates information more finely; Guardian-Agent enablement adds a policy-checking role.

### Intervention Point

Shared information structure and inter-agent authorization.

### Required Observability

Defenses require the requested information, requester context, trust state, and MNI policy.

### Assumptions

Sensitive fields can be labeled or repartitioned and a guardian remains trustworthy.

### Limitations

The study uses synthetic scenario games and short closed-loop chains without full tool use, long-horizon operation, or stacked-defense evaluation.

## Evaluation

### Evaluated Systems

Multiple LLM backends under AutoGen, LangGraph, and AgentScope orchestration.

### Agent Configuration

Role-based requester and holder interactions with trust set at low, medium, and high values; optional guardian intervention.

### Dataset or Environment

A scenario-game dataset with three macro scenes and 19 sub-scenes.

### Baselines

Minimum Necessary Information, no defense, Sensitive Information Repartitioning, and Guardian-Agent enablement.

### Metrics

Task success, Over-Exposure Rate, and Authorization Drift across trust levels.

### Main Results

The paper reports that higher trust generally raises both coordination success and exposure, with heterogeneous slopes across models and frameworks; both defenses reduce OER and AD in tested settings.

## Relation to Existing Work

### Papers Compared by the Authors

Zero-trust agent access, human-agent trust, LLM agent trust surveys, and MAS orchestration studies.

### Claimed Research Gap

Trust had not been isolated as a quantitative control variable connecting collaboration utility to inter-agent exposure risk.

### Closest Related Work

Contextual privacy and least-privilege work for LLM agents.

### Difference From Prior Work

The paper sweeps trust across closed-loop MAS interactions and defines a slope metric rather than evaluating only overt malicious prompts.

## Relevance to Our SoK

### Included Concepts

Trust level, MNI, role differential, over-exposure, authorization drift, orchestration framework, guardian, and confidentiality.

### Taxonomy Implications

Trust is a system-design and precondition variable; the failure is cross-principal confidentiality or authorization, not trust itself.

### Supported Research Questions

How do authorization metrics define their denominator, and which trusted context must a guardian observe to enforce MNI across agents?

### Important Limitations

Synthetic labels and short text interactions may not transfer to dynamic identities, tools, shared memory, or real organizational policies.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The dataset spans three macro scenes and 19 sub-scenes. | Explicit author claim | Paper | 4 | 4-5 | Tables II-III | Scenario construction. |
| The study evaluates 1,488 closed-loop interaction chains. | Explicit author claim | Paper | 4 | 4 | Table I | Evaluation scale. |
| OER measures MNI boundary violations and AD measures trust sensitivity. | Explicit author claim | Paper | 3 | 3-4 | Equations 2-4 | Metric definitions. |
| Trust effects vary across models and orchestration frameworks. | Explicit author claim | Paper | 5 | 6-9 | Figures 4-8 | Main analysis. |
| Repartitioning and guardian enablement reduce OER and AD. | Explicit author claim | Paper | 5.5 | 9-10 | Figure 9 | Defense results. |

## Provenance

### Discovery Source

IEEE DOI metadata; Crossref; arXiv; prior corpus completeness scan.

### Discovery Query

`The Trust Paradox LLM multi-agent IEEE TCSS`

### Accessed Version

Published IEEE metadata; full text accessed as arXiv v1.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

