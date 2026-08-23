# MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `NeurIPS Responsible Foundation Models Workshop` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: MAGPIE: A Benchmark for Multi-Agent Contextual Privacy Evaluation

Authors: Gurusha Juneja; Jayanth Naga Sai Pasupulati; Alon Albalak; Wenyue Hua; William Yang Wang

Year: 2025

Venue: NeurIPS Workshop on Responsible Foundation Models

DOI: Not reported

Primary URL: https://nips.cc/virtual/2025/workshop/127834

Open access URL: https://arxiv.org/abs/2510.15186

BibTeX key: juneja2025magpie

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Multiple role-specialized LLM agents collaborating on tasks containing information with context-dependent sharing constraints.

### Multi-Agent Dependency

Privacy is violated when one role transmits information to another role lacking the appropriate contextual authorization.

### Application Domain

Multi-domain collaborative workflows.

## Security Model

### Protected Assets

Sensitive items governed by contextual privacy norms.

### Threat Actor

The benchmark includes manipulation conditions but also measures unprompted over-sharing.

### Trusted Components

Task construction, sensitive-item labels, recipient roles, and leakage evaluator.

### Attacker Capabilities

Adversarial manipulation can pressure agents to disclose protected information.

### Security Assumptions

The benchmark's contextual rules correctly identify permitted and prohibited disclosures.

## Main Contribution

MAGPIE provides 200 tasks for measuring contextual privacy leakage in collaborating LLM agents. It evaluates model and manipulation effects using sensitive-item-level leakage rather than only inspecting final workflow output.

## Attack or Failure

### Attack Surface

Role prompts, inter-agent messages, and task context.

### Attack Mechanism

Agents over-share protected items or comply with manipulation during collaboration.

### System-Level Failure

Sensitive information reaches a role outside its contextual boundary.

### Security Consequence

Cross-principal confidentiality and contextual-integrity failure.

## Defense

### Defense Mechanism

Not a primary defense contribution.

### Intervention Point

Inter-agent communication.

### Required Observability

Messages, sensitive-item labels, sender and recipient roles, and task context.

### Assumptions

Leakage is evaluated against benchmark-specified norms.

### Limitations

Synthetic tasks and judge-based classification may not capture all real privacy expectations.

## Evaluation

### Evaluated Systems

Role-specialized MAS using frontier language models.

### Agent Configuration

Multiple agents exchange information to complete a shared task.

### Dataset or Environment

200 contextual-privacy tasks in the canonical workshop version.

### Baselines

Models and benign versus manipulation conditions.

### Metrics

Percentage of sensitive items leaked and task-level privacy outcomes.

### Main Results

The paper reports model-dependent leakage, including 35.1% for GPT-5 and 50.7% for Gemini 2.5 Pro, with manipulation increasing leakage.

## Relation to Existing Work

### Papers Compared by the Authors

Contextual-integrity datasets and single-agent privacy benchmarks.

### Claimed Research Gap

Prior privacy evaluation does not model role-relative sharing during multi-agent collaboration.

### Closest Related Work

AgentLeak.

### Difference From Prior Work

MAGPIE centers privacy norms and recipient roles at the task level.

## Relevance to Our SoK

### Included Concepts

Cross-agent leakage, role authorization, contextual integrity, and sensitive-item denominator.

### Taxonomy Implications

Provides a per-item metric contract distinct from per-message or per-run leakage.

### Supported Research Questions

How frequently do collaborating agents violate role-relative privacy constraints?

### Important Limitations

The canonical workshop version supersedes an earlier 158-scenario preprint with a different title and author list.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The canonical benchmark contains 200 tasks. | Explicit author claim | Paper | Abstract; Dataset | 1; 3-5 | - | Dataset scale. |
| Leakage is measured per sensitive item under contextual rules. | Explicit author claim | Paper | Method | 3-5 | - | Metric denominator. |
| Reported leakage differs substantially by model and manipulation condition. | Explicit author claim | Paper | Results | 6-9 | Main tables | Evaluation results. |

## Provenance

### Discovery Source

NeurIPS workshop program; OpenReview; arXiv; version reconciliation.

### Discovery Query

NeurIPS 2025 MAGPIE multi-agent contextual privacy benchmark

### Accessed Version

NeurIPS 2025 workshop version; arXiv 2510.15186 full text.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
