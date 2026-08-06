# Breaking Agents: Compromising Autonomous LLM Agents Through Malfunction Amplification

## Citation

Title: Breaking Agents: Compromising Autonomous LLM Agents Through Malfunction Amplification

Authors: Boyang Zhang; Yicong Tan; Yun Shen; Ahmed Salem; Michael Backes; Savvas Zannettou; Yang Zhang

Year: 2025

Venue: EMNLP

DOI: 10.18653/v1/2025.emnlp-main.1771

Primary URL: https://aclanthology.org/2025.emnlp-main.1771/

Open access URL: https://aclanthology.org/2025.emnlp-main.1771.pdf

BibTeX key: zhang2025breakingagents

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

Autonomous LLM agents and multi-agent orchestration frameworks that iteratively plan and invoke tools.

### Multi-Agent Dependency

The basic malfunction-amplification primitive also applies to a single autonomous agent. Its MAS relevance comes from evaluation on multi-agent frameworks where one manipulated component can consume shared execution budget or derail an orchestrated workflow; it is therefore interaction-amplified rather than MAS-native.

### Application Domain

Autonomous task execution, software workflows, web tasks, and multi-agent orchestration.

## Security Model

### Protected Assets

Task completion, execution budget, and availability of agent workflows.

### Threat Actor

An external adversary who controls content encountered by an agent.

### Trusted Components

The base model, framework controller, and task evaluator are not directly compromised.

### Attacker Capabilities

The attacker places adversarial instructions in observations or content that induce repetitive, irrelevant, or malformed agent actions.

### Security Assumptions

Agents autonomously process untrusted content and can make repeated tool calls or actions before termination.

## Main Contribution

The paper introduces malfunction amplification, which converts small behavioral deviations into prolonged task failure without requiring an overt harmful action. It evaluates the attack across autonomous-agent settings, including multi-agent frameworks, and studies self-examination defenses.

## Attack or Failure

### Attack Surface

Untrusted observations entering iterative planning and action loops.

### Attack Mechanism

Adversarial content induces repetitive or irrelevant actions whose effects compound over subsequent planning steps.

### System-Level Failure

The workflow exhausts its action budget, loops, or fails to complete the assigned task.

### Security Consequence

Availability and task-integrity failure.

## Defense

### Defense Mechanism

Agent self-examination and framework-level checks for malfunctioning behavior.

### Intervention Point

The planning loop before or after action selection.

### Required Observability

The defense requires access to recent actions, observations, and the task objective.

### Assumptions

The checking model remains trustworthy and can identify behavioral inconsistency.

### Limitations

The core vulnerability is not uniquely multi-agent, and the paper's MAS evidence demonstrates amplification in orchestrated systems rather than a failure requiring multiple independent agents.

## Evaluation

### Evaluated Systems

Multiple autonomous-agent implementations and multi-agent frameworks described in the experimental section.

### Agent Configuration

Single-agent and orchestrated multi-agent task configurations with iterative action budgets.

### Dataset or Environment

Task environments covering web, tool-use, and software-oriented agent workflows.

### Baselines

Unattacked executions, direct prompt attacks, and defense variants.

### Metrics

Task failure or attack success rate, action usage, and defense effectiveness.

### Main Results

The authors report failure rates above 80% in multiple tested settings and show that subtle malfunction amplification can evade defenses focused on explicitly harmful output. Self-examination reduces but does not eliminate the attack.

## Relation to Existing Work

### Papers Compared by the Authors

Indirect prompt injection, denial-of-service, and agent red-teaming methods.

### Claimed Research Gap

Prior attacks focus on explicit harmful outputs rather than amplifying small operational malfunctions over long agent trajectories.

### Closest Related Work

Indirect prompt injection against tool-using autonomous agents.

### Difference From Prior Work

The attack objective is ordinary task malfunction and budget exhaustion rather than a visibly malicious terminal action.

## Relevance to Our SoK

### Included Concepts

Long-horizon failure amplification, shared execution budget, availability, task integrity, and trajectory-aware monitoring.

### Taxonomy Implications

This is an interaction-amplified boundary case: the mechanism is inherited from single-agent autonomy, while orchestration broadens the impact.

### Supported Research Questions

Which attacks become materially worse in multi-agent workflows even when their primitive exists at n=1?

### Important Limitations

It should not be counted as evidence for a MAS-native failure without separating the multi-agent subset of the evaluation.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Malfunction amplification targets iterative action selection rather than only harmful terminal output. | Explicit author claim | Paper | 1, 3 | 1-4 | Figure 1 | Motivation and method. |
| The attack is evaluated in both autonomous-agent and multi-agent scenarios. | Explicit author claim | Paper | 4 | 5-8 | Experimental tables | Evaluation scope. |
| Multiple settings show attack success above 80%. | Explicit author claim | Paper | 4 | 6-8 | Main result tables | Reported results. |
| Self-examination is evaluated as a defense. | Explicit author claim | Paper | 5 | 8-9 | Defense table | Defense analysis. |
| The primitive can be represented in a single-agent loop. | Interpretation | Paper | 3 | 3-5 | - | The method does not require an inter-agent edge; MAS relevance arises in evaluation and amplification. |

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
