# PEAR: Planner-Executor Agent Robustness Benchmark

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `Findings of EACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: PEAR: Planner-Executor Agent Robustness Benchmark

Authors: Shen Dong; Mingxuan Zhang; Pengfei He; Li Ma; Bhavani Thuraisingham; Hui Liu; Yue Xing

Year: 2026

Venue: Findings of EACL

DOI: 10.18653/v1/2026.findings-eacl.237

Primary URL: https://aclanthology.org/2026.findings-eacl.237/

Open access URL: https://aclanthology.org/2026.findings-eacl.237.pdf

BibTeX key: dong2026pear

## Paper Type

Benchmark; Evaluation; Attack; Empirical study

## Scope

### System Studied

Planner-executor agent systems in which one component produces plans and another executes them using memory and tools.

### Multi-Agent Dependency

Robustness depends on role-separated communication and whether an attack targets the planner, executor, or shared context.

### Application Domain

Tool-using planner-executor workflows.

## Security Model

### Protected Assets

Task utility and execution integrity.

### Threat Actor

Adversary injecting instructions into planner- or executor-facing context.

### Trusted Components

Benchmark environment, outcome evaluator, and non-targeted components.

### Attacker Capabilities

Role-specific prompt injection and memory influence.

### Security Assumptions

Planner and executor roles are separately instrumentable.

## Main Contribution

PEAR evaluates utility and adversarial robustness in planner-executor systems under role-specific attacks and memory ablations. It shows that robustness depends on where the attack enters and how role state is shared.

## Attack or Failure

### Attack Surface

Planner input, executor input, and memory.

### Attack Mechanism

Injected instructions corrupt plan formation or action execution.

### System-Level Failure

The delegated workflow fails or executes an adversarial objective.

### Security Consequence

Loss of plan or action integrity.

## Defense

### Defense Mechanism

No universal defense; memory and role design are analyzed as robustness factors.

### Intervention Point

Planner-executor boundary and memory.

### Required Observability

Role-specific prompts, plans, actions, and final outcomes.

### Assumptions

The benchmark can separately manipulate role inputs.

### Limitations

The two-role architecture does not represent every MAS topology.

## Evaluation

### Evaluated Systems

Planner-executor configurations using multiple LLM backbones.

### Agent Configuration

One planner and one executor with controlled memory conditions.

### Dataset or Environment

Tool-use tasks with benign and adversarial variants.

### Baselines

Planner-targeted versus executor-targeted attacks and memory ablations.

### Metrics

Task utility and attack/robustness outcomes.

### Main Results

The paper reports materially different vulnerabilities by attacked role and memory configuration.

## Relation to Existing Work

### Papers Compared by the Authors

Single-agent prompt-injection benchmarks and planner-executor frameworks.

### Claimed Research Gap

Existing evaluation does not isolate security effects across planner and executor roles.

### Closest Related Work

AgentDojo, InjecAgent, and role-structured MAS attacks.

### Difference From Prior Work

PEAR makes role position and memory explicit evaluation variables.

## Relevance to Our SoK

### Included Concepts

Role composition, delegation, memory, attack position, and interaction evidence.

### Taxonomy Implications

Demonstrates why a generic “malicious agent” label loses important attacker position.

### Supported Research Questions

How do role position and memory change planner-executor attack outcomes?

### Important Limitations

The benchmark focuses on a fixed two-role pattern.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| PEAR separates planner- and executor-targeted attacks. | Explicit author claim | Paper | Abstract; 3 | 1; 4-6 | Figure 1 | Threat model. |
| The evaluation includes memory ablation. | Explicit author claim | Paper | 4 | 6-9 | Main tables | Design variable. |
| Utility and robustness are evaluated jointly. | Explicit author claim | Paper | Abstract; 4 | 1; 6-9 | Main tables | Evaluation contract. |

## Provenance

### Discovery Source

ACL Anthology; local corpus; version reconciliation.

### Discovery Query

PEAR planner executor agent robustness benchmark

### Accessed Version

Published Findings of EACL 2026 version; withdrawn arXiv record not used.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
