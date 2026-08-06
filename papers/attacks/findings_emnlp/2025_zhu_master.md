# MASTER: Multi-Agent Security Through Exploration of Roles and Topological Structures - A Comprehensive Framework

## Citation

Title: MASTER: Multi-Agent Security Through Exploration of Roles and Topological Structures - A Comprehensive Framework

Authors: Yifan Zhu; Chao Zhang; Xin Shi; Xueqiao Zhang; Yi Yang; Yawei Luo

Year: 2025

Venue: Findings of EMNLP

DOI: 10.18653/v1/2025.findings-emnlp.917

Primary URL: https://aclanthology.org/2025.findings-emnlp.917/

Open access URL: https://aclanthology.org/2025.findings-emnlp.917.pdf

BibTeX key: zhu2025master

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Automatically constructed LLM multi-agent systems with heterogeneous roles, directed information flow, memory, and selectable graph topologies across seven application domains.

### Multi-Agent Dependency

The attacker first recovers role and neighborhood information, then uses the inferred role/topology structure to implant and activate adversarial traits that coordinate harmful behavior across agents.

### Application Domain

Software, finance, data management, education, research, healthcare, and security investigation.

## Security Model

### Protected Assets

Role integrity, collaboration integrity, and safe system task execution.

### Threat Actor

An external user able to converse with the MAS.

### Trusted Components

The evaluation judge, system constructor, and model interfaces are trusted.

### Attacker Capabilities

The attacker can submit multi-round prompts, elicit self-introductions, infer roles and topology, inject adversarial traits, and later activate them.

### Security Assumptions

The MAS exposes enough conversational behavior for probing; the prompt channel can reach selected starting agents.

## Main Contribution

MASTER combines automatic MAS construction, a three-stage role/topology-adaptive attack, three defenses, and a multi-domain evaluation framework. It measures attack success together with adversarial role consistency and harmful cooperation.

## Attack or Failure

### Attack Surface

Role prompts, inter-agent information flow, memory updates, and communication topology.

### Attack Mechanism

Probe the system structure, inject scenario-adaptive adversarial traits into selected roles, then activate those traits with prompts encoding role and topology information.

### System-Level Failure

Multiple specialized agents preserve adversarial roles and cooperate on harmful tasks.

### Security Consequence

Collective objective and action-integrity failure.

## Defense

### Defense Mechanism

Prompt-leakage detection, hierarchical monitoring based on agent criticality, and scenario-aware preemptive defense.

### Intervention Point

Input inspection, topology-aware monitoring, and pre-deployment role prompting.

### Required Observability

The hierarchical defense requires role importance and topology position; preemptive defense requires scenario and system descriptions.

### Assumptions

The defender knows or can compute role and topology metadata.

### Limitations

The evaluation uses constructed scenarios and prompt-level trait attacks rather than deployed production systems.

## Evaluation

### Evaluated Systems

Five model families, including GPT-4o and Gemini-2.5-Pro, in automatically generated MAS configurations.

### Agent Configuration

Five graph families, heterogeneous roles, and varying propagation levels.

### Dataset or Environment

A generated seven-domain collection of role- and topology-diverse MAS scenarios.

### Baselines

Dark-trait injection without role/topology adaptation and ablations without role or topology information.

### Metrics

Attack Success Rate, blackened-role consistency, harmful-cooperation score, and defense efficiency.

### Main Results

The authors report that role and topology adaptation increase attack effectiveness, hierarchical topology has the highest average ASR, and chain topology the lowest. The three defenses reduce ASR substantially in the reported settings.

## Relation to Existing Work

### Papers Compared by the Authors

Agent Smith, MultiAgent Collaboration Attack, NetSafe, G-Safeguard, and dark-trait injection methods.

### Claimed Research Gap

Existing attacks generally omit heterogeneous roles and topology context or require direct system access.

### Closest Related Work

Topology-aware adversarial analysis in NetSafe and G-Safeguard.

### Difference From Prior Work

MASTER jointly operationalizes role discovery, topology discovery, adaptive attack, defenses, and automatic scenario construction.

## Relevance to Our SoK

### Included Concepts

Topology reconnaissance, role composition, multi-round trait injection, coordinated harmful execution, topology-aware monitoring, and generated evaluation scenarios.

### Taxonomy Implications

The paper demonstrates a causal chain from system design through adversary capability and attack mechanism to collective action-integrity loss.

### Supported Research Questions

How do roles and topology alter attack reach, and what metadata must a topology-aware defense observe?

### Important Limitations

The scenarios are automatically constructed, the attack assumes a conversational probing channel, and real deployment validity is not established.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| MASTER models role-labeled agents and directed information flow. | Explicit author claim | Paper | 3.1 | 3-4 | Figure 2 | Framework definition. |
| The attack has probing, adaptive trait injection, and activation stages. | Explicit author claim | Paper | 3.2.4 | 5 | - | Attack strategy. |
| The defenses use leakage detection, hierarchical inspection, and scenario-aware preemption. | Explicit author claim | Paper | 3.2.5 | 5-6 | Figure 2 | Defense strategy. |
| The evaluation spans seven domains and five topology families. | Explicit author claim | Paper | 4.1 | 6-7 | - | Experimental setup. |
| Hierarchical topology has the highest mean ASR and chain the lowest. | Explicit author claim | Paper | 4.5 | 9 | Figure 5 | Topology analysis. |
| Role/topology ablations reduce the attack's reported effectiveness. | Explicit author claim | Paper | 4.2 | 6-8 | Table 2 | Ablation results. |

## Provenance

### Discovery Source

ACL Anthology; prior corpus.

### Discovery Query

Not applicable.

### Accessed Version

Published conference version.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
