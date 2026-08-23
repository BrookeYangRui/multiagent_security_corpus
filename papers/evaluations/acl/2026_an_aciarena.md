# ACIARena: Toward Unified Evaluation for Agent Cascading Injection

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: ACIARena: Toward Unified Evaluation for Agent Cascading Injection

Authors: Hengyu An; Minxi Li; Jinghuai Zhang; Naen Xu; Chunyi Zhou; Changjiang Li; Xiaogang Xu; Tianyu Du; Shouling Ji

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.457

Primary URL: https://aclanthology.org/2026.acl-long.457/

Open access URL: https://aclanthology.org/2026.acl-long.457.pdf

BibTeX key: an2026aciarena

## Paper Type

Benchmark; Evaluation; Attack; Defense; Empirical study

## Scope

### System Studied

Six MAS implementations with different role, topology, memory, and tool arrangements.

### Multi-Agent Dependency

Agent Cascading Injection relies on a compromised agent transmitting malicious instructions through trusted inter-agent edges.

### Application Domain

General-purpose collaboration and tool-using workflows.

## Security Model

### Protected Assets

Instruction integrity, task availability, and confidential information.

### Threat Actor

An adversary able to influence external inputs, an agent profile, or inter-agent messages.

### Trusted Components

Evaluation harness, task data, and outcome judges.

### Attacker Capabilities

Inject through three surfaces to pursue hijacking, disruption, or exfiltration.

### Security Assumptions

The attacker uses the benchmark-defined access for each threat scenario.

## Main Contribution

ACIARena provides a modular specification for MAS, attacks, defenses, and evaluation across 1,356 test cases. It evaluates three attack surfaces, three objectives, and six implementations, finding that role design and controlled interaction matter beyond topology alone.

## Attack or Failure

### Attack Surface

External inputs, agent profiles, and inter-agent messages.

### Attack Mechanism

Injected instructions propagate through communication and trust relationships.

### System-Level Failure

Final-response hijacking, task disruption, or information exfiltration.

### Security Consequence

Cascading compromise of the collaborative workflow.

## Defense

### Defense Mechanism

The framework evaluates input/output defense modules; it does not claim a universal defense.

### Intervention Point

Attack surface and agent communication boundaries.

### Required Observability

Final responses and propagation outcomes.

### Assumptions

Defense transfer is evaluated under the supported implementations.

### Limitations

Real deployments may expose additional frameworks, roles, and channels.

## Evaluation

### Evaluated Systems

Six representative MAS implementations and multiple LLM backbones.

### Agent Configuration

Centralized, decentralized, sequential, and role-specialized structures represented by the included systems.

### Dataset or Environment

1,356 cases crossing three surfaces and three objectives.

### Baselines

Benign utility and undefended or defended attack conditions.

### Metrics

Benign Utility, Attack Success Rate, Defense Success Rate, and Propagation Success Rate.

### Main Results

Robustness cannot be inferred from topology alone, and defenses developed in simplified settings may fail to transfer.

## Relation to Existing Work

### Papers Compared by the Authors

NetSafe, G-Safeguard, communication-attack studies, and MASLab.

### Claimed Research Gap

Prior work uses incomplete threat scenarios, inconsistent settings, and non-extensible codebases.

### Closest Related Work

MAS cascading-injection attacks and unified MAS evaluation frameworks.

### Difference From Prior Work

It unifies system construction and attack-defense modules under one benchmark contract.

## Relevance to Our SoK

### Included Concepts

Propagation, role design, attack surfaces, defense transfer, and evaluation contracts.

### Taxonomy Implications

Separates attack surface from objective and system-level outcome.

### Supported Research Questions

Which interaction and role choices change cascading-injection robustness?

### Important Limitations

Outcome metrics remain specific to the benchmark's tasks and judges.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| ACIARena contains 1,356 cases over three surfaces and three objectives. | Explicit author claim | Paper | Abstract; 4 | 1; 5 | - | Benchmark scope. |
| Six MAS implementations are supported. | Explicit author claim | Paper | Abstract; 4 | 1; 5 | - | System coverage. |
| The benchmark reports benign utility, attack success, defense success, and propagation metrics. | Explicit author claim | Paper | 5.1 | 5 | - | Evaluation metric definitions. |

## Provenance

### Discovery Source

ACL Anthology; local corpus; citation snowballing.

### Discovery Query

ACL 2026 multi-agent security benchmark cascading injection

### Accessed Version

Published ACL 2026 version.

### Access Date

2026-08-05
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
