# On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents

## Citation

Title: On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents

Authors: Jen-Tse Huang; Jiaxu Zhou; Tailin Jin; Xuhui Zhou; Zixi Chen; Wenxuan Wang; Youliang Yuan; Michael R. Lyu; Maarten Sap

Year: 2025

Venue: ICML

DOI: Not reported

Primary URL: https://proceedings.mlr.press/v267/huang25ay.html

Open access URL: https://raw.githubusercontent.com/mlresearch/v267/main/assets/huang25ay/huang25ay.pdf

BibTeX key: huang2025faultyagents

## Paper Type

- Attack
- Defense
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Six LLM multi-agent collaboration systems arranged as linear, flat, or hierarchical structures across code generation, mathematics, translation, and text evaluation.

### Multi-Agent Dependency

AutoTransform and AutoInject corrupt messages produced by selected agents, after which errors traverse downstream dependencies or peer exchanges. The tested failure and recovery behavior is determined by the system's communication structure and task allocation.

### Application Domain

Collaborative reasoning, code generation, translation, and evaluation.

## Security Model

### Protected Assets

Accuracy and reliability of the collective task output.

### Threat Actor

Clumsy or malicious member agents whose outputs contain syntactic, semantic, or task-specific errors.

### Trusted Components

The fault injector, evaluator, non-faulty agents, and optional Challenger or Inspector defense components.

### Attacker Capabilities

AutoTransform changes an agent's role prompt to induce erroneous behavior; AutoInject directly inserts generated errors into selected inter-agent messages.

### Security Assumptions

Faults can be represented as message-level errors and ground-truth or evaluator-based task scoring is available.

## Main Contribution

The paper introduces AutoTransform and AutoInject to evaluate faulty-agent resilience across six collaboration systems and four tasks. It also proposes Challenger peer checking and a separate Inspector agent to correct faulty messages.

## Attack or Failure

### Attack Surface

Role instructions and inter-agent messages from a faulty member.

### Attack Mechanism

The framework either transforms an agent into an error-producing role or injects generated errors directly into its output messages.

### System-Level Failure

Other agents accept or build on the faulty content, degrading final task performance.

### Security Consequence

Collective output-integrity and reliability failure.

## Defense

### Defense Mechanism

Challenger lets agents question peer outputs; Inspector adds a dedicated reviewing agent that identifies and corrects suspect messages.

### Intervention Point

Peer communication and centralized review.

### Required Observability

Challenger sees peer messages; Inspector sees messages selected for review and task context.

### Assumptions

At least one reviewer remains capable and honest, and the task permits errors to be recognized from context.

### Limitations

Fault behavior is synthetically induced, tested systems and tasks use fixed templates, and recovery depends strongly on evaluator quality and error type.

## Evaluation

### Evaluated Systems

Self-collaboration, Camel, MetaGPT, MAD, ChatEval, and AgentVerse configurations.

### Agent Configuration

Linear, all-to-all flat, and hierarchical structures with task-specific expert roles.

### Dataset or Environment

HumanEval, MATH, WMT19 translation, and FairEval text evaluation.

### Baselines

Single-agent and unmodified multi-agent systems, plus systems under AutoTransform or AutoInject without the proposed defenses.

### Metrics

Task-specific accuracy or quality scores, performance drop, and fraction of injected errors recovered.

### Main Results

The paper reports a 5.5% average performance drop for hierarchical systems versus 10.5% and 23.7% for the other structures, and recovery of up to 96.4% of faulty-agent errors with the proposed defenses.

## Relation to Existing Work

### Papers Compared by the Authors

Multi-agent debate, contagious jailbreak, adversarial collaboration, and fault-tolerant multi-agent systems.

### Claimed Research Gap

Prior security work emphasized toxic or malicious outcomes rather than systematically comparing structural resilience across ordinary downstream tasks.

### Closest Related Work

MultiAgent Collaboration Attack and topology-aware MAS safety evaluations.

### Difference From Prior Work

The framework varies error type, error rate, task, and architecture, and includes both role-level and message-level fault generation.

## Relevance to Our SoK

### Included Concepts

Faulty member, role corruption, message injection, error propagation, topology, peer challenge, inspector, and recovery.

### Taxonomy Implications

This paper is best coded as collective task-integrity degradation under member faults, with architecture as a precondition and defense placement as a separate dimension.

### Supported Research Questions

How do topology and task decomposition alter fault propagation, and where can review recover from a compromised member?

### Important Limitations

Synthetic faults are not equivalent to an adaptive adversary, and task metrics and system sizes differ enough that resilience numbers should not be treated as a universal MAS bound.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| AutoTransform changes role behavior and AutoInject inserts generated errors. | Explicit author claim | Paper | 3 | 3-4 | Figure 2 | Fault-generation methods. |
| Six systems and four downstream tasks are evaluated. | Explicit author claim | Paper | 4 | 4-6 | Tables 1-2 | Experimental settings. |
| Hierarchical systems have the lowest reported average performance drop. | Explicit author claim | Paper | 5 | 6-8 | Figures 3-5; Tables 4-5 | Structural comparison. |
| Challenger and Inspector are communication-level recovery mechanisms. | Explicit author claim | Paper | 6 | 8-9 | Figure 6 | Defense definitions. |
| The defenses recover up to 96.4% of faulty-agent errors. | Explicit author claim | Paper | 6 | 9 | Figure 6 | Defense results. |

## Provenance

### Discovery Source

PMLR proceedings; prior corpus completeness scan.

### Discovery Query

`site:proceedings.mlr.press multi-agent faulty agents security`

### Accessed Version

Published ICML version, PMLR volume 267.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

