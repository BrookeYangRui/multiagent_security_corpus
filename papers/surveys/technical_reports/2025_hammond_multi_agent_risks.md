# Multi-Agent Risks from Advanced AI

## Citation

Title: Multi-Agent Risks from Advanced AI

Authors: Lewis Hammond; Alan Chan; Jesse Clifton; Jason Hoelscher-Obermaier; Akbir Khan; Euan McLean; Chandler Smith; Wolfram Barfuss; Jakob Foerster; Tomáš Gavenčiak; The Anh Han; Edward Hughes; Vojtěch Kovařík; Jan Kulveit; Joel Z. Leibo; Caspar Oesterheld; Christian Schroeder de Witt; Nisarg Shah; Michael Wellman; Paolo Bova; Theodor Cimpeanu; Carson Ezell; Quentin Feuillade-Montixi; Matija Franklin; Esben Kran; Igor Krawczuk; Max Lamparth; Niklas Lauffer; Alexander Meinke; Sumeet Motwani; Anka Reuel; Vincent Conitzer; Michael Dennis; Iason Gabriel; Adam Gleave; Gillian Hadfield; Nika Haghtalab; Atoosa Kasirzadeh; Sébastien Krier; Kate Larson; Joel Lehman; David C. Parkes; Georgios Piliouras; Iyad Rahwan

Year: 2025

Venue: Cooperative AI Foundation Technical Report 1

DOI: 10.48550/arXiv.2502.14143

Primary URL: https://www.cooperativeai.com/post/new-report-multi-agent-risks-from-advanced-ai

Open access URL: https://arxiv.org/pdf/2502.14143

BibTeX key: `hammond2025multiagentrisks`

## Paper Type

- Technical report
- Risk taxonomy
- Research agenda

Primary category: Not applicable; separate `sok_related` set

Scope relation: strongly_related

## Scope

### System Studied

Populations of advanced AI agents that interact and adapt to one another across economic, military, infrastructure, and social settings.

### Multi-Agent Dependency

The report restricts its taxonomy to risks that emerge, become more difficult, or become qualitatively different when multiple advanced agents interact.

### Application Domain

General advanced-AI ecosystems, markets, critical infrastructure, governance, and safety systems.

## Security Model

### Protected Assets

Coordination, system stability, safety controls, privacy, fairness, accountability, and governance.

### Threat Actor

No single fixed adversary; the report covers aligned, conflicting, colluding, vulnerable, and emergent agent populations.

### Trusted Components

Not fixed. Trust and commitment failures are themselves part of the taxonomy.

### Attacker Capabilities

Where adversarial behavior is involved, agents may coordinate, collude, exploit vulnerabilities, share capabilities, or undermine multi-agent safety schemes.

### Security Assumptions

The report analyzes heterogeneous future systems and does not impose one universal technical threat model.

## Main Contribution

The report organizes multi-agent risk into three failure modes, miscoordination, conflict, and collusion, and seven cross-cutting risk factors. It connects these risks to evaluation, mitigation, AI safety, governance, and ethics research directions.

## Attack or Failure

### Attack Surface

Inter-agent communication, incentives, network structure, shared environments, safety protocols, and security boundaries.

### Attack Mechanism

Varies across the taxonomy; examples include collusion, network amplification, destabilizing feedback, emergent agency, and multi-agent-specific exploitation.

### System-Level Failure

Miscoordination, conflict, collusion, and failures induced by seven interacting risk factors.

### Security Consequence

Collective harms that cannot be understood or mitigated solely through isolated-agent analysis.

## Defense

### Defense Mechanism

The report proposes directions rather than one defense, including multi-agent evaluation, secure interaction protocols, peer incentives, information design, network stabilization, and adversary robustness.

### Intervention Point

Agent design, interaction protocols, network structure, evaluation, deployment governance, and institutional coordination.

### Required Observability

Varies by proposed direction and is not standardized into one monitoring contract.

### Assumptions

Varies across the technical, governance, and ethics recommendations.

### Limitations

The taxonomy is anticipatory and broad; most discussed risks had not yet appeared at deployment scale when the report was written.

## Evaluation

### Evaluated Systems

Not applicable as a unified experiment; the report uses prior studies, real-world examples, and illustrative case studies.

### Agent Configuration

Varies across the cited evidence.

### Dataset or Environment

Not applicable.

### Baselines

Single-agent-centered safety, governance, and ethics treatments.

### Metrics

Not reported as one common measurement contract.

### Main Results

Not applicable; the output is a taxonomy and research agenda, not a pooled empirical estimate.

## Relation to Existing Work

### Papers Compared by the Authors

The report draws from cooperative AI, multi-agent learning, game theory, complex systems, AI safety, governance, ethics, privacy, and security.

### Claimed Research Gap

The authors state that advanced multi-agent risks are distinct from single-agent risks and have been systematically underappreciated and understudied.

### Closest Related Work

Open Challenges in Multi-Agent Security and later cross-domain multi-agent security agendas.

### Difference From Prior Work

The report integrates incentive-based failure modes with structural risk factors and broader safety, governance, and ethics implications.

## Relevance to Our SoK

### Included Concepts

Miscoordination, conflict, collusion, information asymmetry, network effects, selection pressure, destabilizing dynamics, commitment, emergent agency, and multi-agent security.

### Taxonomy Implications

It is a high-level comparator for distinguishing security violations from broader multi-agent safety and governance risks.

### Supported Research Questions

Which failures require interacting-agent analysis, and where do security-specific mechanisms sit within the wider multi-agent risk landscape?

### Important Limitations

Its failure modes and risk factors must not be treated as empirical prevalence estimates or copied directly into a fixed security taxonomy.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The report is limited to risks that emerge, intensify, or qualitatively change in multi-agent settings. | Explicit author claim | Report | Executive Summary; Introduction | PDF 4-5 | Not applicable | The authors state this boundary when motivating the taxonomy. |
| The taxonomy contains three failure modes: miscoordination, conflict, and collusion. | Explicit author claim | Report | Executive Summary; Section 2 | PDF 4; 10-19 | Figure 1 | The three modes are defined by desired cooperation and agent objectives. |
| The report defines seven cross-cutting risk factors. | Explicit author claim | Report | Executive Summary; Section 3 | PDF 4; 20-42 | Not applicable | Information asymmetries, network effects, selection pressures, destabilizing dynamics, commitment and trust, emergent agency, and multi-agent security are enumerated. |
| Multi-agent security is one risk factor within a broader risk framework. | Explicit author claim | Report | Section 3.7 | PDF 39-42 | Not applicable | The report distinguishes security vulnerabilities from the other structural factors. |
| The report connects the taxonomy to safety, governance, and ethics. | Explicit author claim | Report | Section 4 | PDF 43-48 | Not applicable | Separate subsections discuss implications for each field. |
| The taxonomy is a conceptual comparator rather than an empirical paper denominator. | Corpus interpretation | Report | Executive Summary; organization | PDF 4-5 | Not applicable | The report synthesizes examples and directions without a systematic evidence-counting contract. |

## Provenance

### Discovery Source

Cooperative AI Foundation official report page; arXiv API; repository gap review.

### Discovery Query

`multi-agent security survey SoK AI agents`; `Multi-Agent Risks from Advanced AI`

### Accessed Version

Cooperative AI Foundation Technical Report 1; arXiv v1 dated 2025-02-19.

### Access Date

2026-08-06

### Prepared By

Human or automated process: automated extraction from the complete primary report

Model and version, if automatically generated: Not recorded

### Verification Status

`agent_unverified`

### Last Updated

2026-08-06
