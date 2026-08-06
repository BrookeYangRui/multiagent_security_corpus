# Architecture Matters for Multi-Agent Security

## Citation

Title: Architecture Matters for Multi-Agent Security

Authors: Ben Hagag; William L. Anderson; Christian Schroeder de Witt; Sarah Scheffler

Year: 2026

Venue: ICML

DOI: Not reported

Primary URL: https://icml.cc/virtual/2026/poster/64792

Open access URL: https://arxiv.org/abs/2604.23459

BibTeX key: hagag2026architecturematters

## Paper Type

- Attack
- Benchmark
- Evaluation
- Empirical study

## Scope

### System Studied

Standalone and multi-agent systems in browser, desktop, and code environments, instantiated in 13 role, topology, and memory configurations.

### Multi-Agent Dependency

The paper holds tasks and base models comparable while changing how intent, tool authority, communication, and state are distributed across agents. The measured security effect is therefore attributed to architectural composition rather than a new single-agent jailbreak.

### Application Domain

Browser automation, computer use, and code generation.

## Security Model

### Protected Assets

Prevention of harmful task execution while retaining benign task performance.

### Threat Actor

A malicious user directly requests a harmful task.

### Trusted Components

The evaluation harness and environment outcome checks; no compromised member agent is modeled.

### Attacker Capabilities

The user supplies a direct harmful request to the system but does not inject memory, compromise agents, or tamper with messages.

### Security Assumptions

Architecture may fragment harmful intent or execution context across otherwise safety-trained agents; benchmark checkers can classify execution outcomes by stage.

## Main Contribution

The paper presents a controlled empirical study of how role decomposition, communication topology, and memory visibility change both attack resistance and benign performance. It adapts three harmful-agent benchmarks to 13 multi-agent configurations and uses stagewise outcomes rather than a single binary ASR.

## Attack or Failure

### Attack Surface

Task decomposition, distributed tool authority, inter-agent routing, and memory visibility.

### Attack Mechanism

A harmful request is split or transformed across agents so that individual planners or executors may see only part of its intent or context.

### System-Level Failure

The composed system partially or fully executes a harmful task that a standalone agent may refuse.

### Security Consequence

Compositional action-integrity failure caused by distributed authority and partial observability.

## Defense

### Defense Mechanism

No dedicated defense is proposed; architecture choices are treated as security-relevant design variables.

### Intervention Point

Roles, communication topology, tool allocation, and memory design.

### Required Observability

The evaluation observes planner refusals, executor refusals, partial action traces, completed harm, and benign outcomes.

### Assumptions

Security-relevant differences can be isolated by holding the benchmark, model, and reference configuration fixed within each axis.

### Limitations

Only direct misuse is studied; indirect prompt injection, malicious members, memory poisoning, dedicated guardrails, and interactions among design axes are excluded.

## Evaluation

### Evaluated Systems

Multiple frontier and open models in standalone, orchestrator-executor, specialist, star, chain, mesh, private-memory, reasoning-visible, and shared-memory configurations.

### Agent Configuration

Thirteen configurations varying roles, topology, or memory around common reference architectures.

### Dataset or Environment

BrowserART, OS-Harm with OS-World benign tasks, and RedCode-Gen.

### Baselines

Standalone agents and matched multi-agent configurations without the tested architecture change.

### Metrics

Planning Refusal, Execution Refusal, Harmful Action, Harmful Task completion, and benign task accuracy.

### Main Results

Multi-agent configurations are more vulnerable than standalone agents in most tested comparisons, with up to a reported 3.8-fold difference at comparable or higher benign accuracy; topology and memory effects vary by model and environment.

## Relation to Existing Work

### Papers Compared by the Authors

AgentHarm, BrowserART, OS-Harm, RedCode, MAS attacks, and recent agentic security evaluations.

### Claimed Research Gap

Prior work largely evaluated model or defense components rather than isolating security effects of MAS architecture.

### Closest Related Work

Security Tax of LLM-MAS and topology-aware attack and defense studies.

### Difference From Prior Work

The study jointly reports benign capability and stagewise harm while systematically varying three architecture axes.

## Relevance to Our SoK

### Included Concepts

Role decomposition, authority distribution, topology, memory visibility, direct misuse, staged impact verification, and single-agent baseline.

### Taxonomy Implications

Architecture is a system-design field, not a failure category; the observed failure is unauthorized global action enabled by compositional context and authority.

### Supported Research Questions

Does a claimed multi-agent security effect isolate interaction structure, and which outcome stages define successful harm?

### Important Limitations

The study does not model adversarial members or inter-agent injection, and no architecture is universally safer across the tested domains and models.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Thirteen configurations vary roles, topology, and memory across three environments. | Explicit author claim | Paper | 4 | 4-5 | Tables 8-10 | Experimental design. |
| Outcomes separate planning refusal, execution refusal, harmful action, and completed harm. | Explicit author claim | Paper | 4.4 | 5 | - | Metric definitions. |
| Role decomposition can increase vulnerability while benign performance remains high. | Explicit author claim | Paper | 5.1 | 5-6 | Table 1 | Role results. |
| Topology and memory rankings depend on environment and model. | Explicit author claim | Paper | 5.2-5.3 | 6-8 | Tables 2-3; 6-7 | Cross-configuration results. |
| The study excludes indirect injection, malicious members, and dedicated safety layers. | Explicit author claim | Paper | 8 | 9 | - | Limitations. |

## Provenance

### Discovery Source

ICML official program; arXiv; prior corpus completeness scan.

### Discovery Query

`site:icml.cc/Downloads/2026 multi-agent security`

### Accessed Version

Published ICML paper; full text accessed as arXiv v1 because the PMLR page was not yet indexed.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05

