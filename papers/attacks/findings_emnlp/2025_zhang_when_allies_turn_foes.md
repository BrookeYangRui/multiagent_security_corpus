# When Allies Turn Foes: Exploring Group Characteristics of LLM-Based Multi-Agent Collaborative Systems Under Adversarial Attacks

## Citation

Title: When Allies Turn Foes: Exploring Group Characteristics of LLM-Based Multi-Agent Collaborative Systems Under Adversarial Attacks

Authors: Jiahao Zhang; Baoshuo Kan; Tao Gong; Fu Lee Wang; Tianyong Hao

Year: 2025

Venue: Findings of EMNLP

DOI: 10.18653/v1/2025.findings-emnlp.333

Primary URL: https://aclanthology.org/2025.findings-emnlp.333/

Open access URL: https://aclanthology.org/2025.findings-emnlp.333.pdf

BibTeX key: zhang2025alliesfoes

## Paper Type

- Attack
- Defense
- Evaluation
- Empirical study

## Scope

### System Studied

LLM collaborative groups that repeatedly exchange answers and seek consensus under self-consistency, simultaneous-talk, or one-by-one communication.

### Multi-Agent Dependency

One or two adversarial members inject counterfactual answers into a group. Their influence propagates through communication rounds, and system robustness changes with group size and communication strategy.

### Application Domain

Collaborative reasoning and collective decision-making.

## Security Model

### Protected Assets

Correct collective answers and resistance of honest collaborators to adversarial influence.

### Threat Actor

One or two adversarial group members.

### Trusted Components

Dataset labels and the experimental controller are trusted.

### Attacker Capabilities

The adversarial agent produces a counterfactual answer, observes other agents' responses, retains interaction history, and generates further misleading responses.

### Security Assumptions

Tasks have predetermined answers; groups contain at most five collaborative agents; adversarial answers are synthetically constructed.

## Main Contribution

The paper studies adversarial influence as a group-dynamics problem across three collaboration scenarios, three communication strategies, and varying group compositions. It introduces System Defense Index (SDI), an agent- and round-sensitive robustness metric, and evaluates scaling and self-reflection mitigations.

## Attack or Failure

### Attack Surface

Inter-agent deliberation and consensus formation.

### Attack Mechanism

Adversarial members repeatedly introduce counterfactual answers and adapt subsequent misleading messages to the collaboration history.

### System-Level Failure

Adversarial answers spread through the group and alter honest-agent or collective decisions.

### Security Consequence

Collective decision-integrity loss and reduced robustness.

## Defense

### Defense Mechanism

Increase the number of collaborative agents or add self-reflection before subsequent responses.

### Intervention Point

Group composition and per-agent reasoning.

### Required Observability

Self-reflection uses an agent's own response and interaction history; group scaling requires control of membership.

### Assumptions

Additional honest agents and reflection prompts are available.

### Limitations

The paper notes that self-reflection can entrench an already incorrect response and does not study role-diverse groups.

## Evaluation

### Evaluated Systems

GPT-3.5-Turbo-0125, GPT-4.1-mini, LLaMA-3.3-70B, and Qwen/QwQ-32B.

### Agent Configuration

One to five collaborative agents, one or two adversarial agents, three communication strategies, and multiple rounds.

### Dataset or Environment

BlendQA sampled from MMLU, MedMCQA, and CommonsenseQA; MuSR; and CEB.

### Baselines

Configurations vary adversarial-agent count, honest group size, communication strategy, and self-reflection.

### Metrics

System Defense Index, First Attacked Time, consensus measures, and answer accuracy.

### Main Results

The authors report that additional adversarial agents reduce SDI and influence the group earlier, while simultaneous talk is more resistant than one-by-one communication. Self-reflection improves average robustness but can reinforce an incorrect prior answer.

## Relation to Existing Work

### Papers Compared by the Authors

MultiAgent Collaboration Attack and prior studies of adversarial debate and collaborative reasoning.

### Claimed Research Gap

Prior work does not systematically characterize how adversarial members affect group-level dynamics across communication and composition choices.

### Closest Related Work

MultiAgent Collaboration Attack.

### Difference From Prior Work

The paper emphasizes group composition, communication strategy, and a time-sensitive group robustness metric rather than only final attack success.

## Relevance to Our SoK

### Included Concepts

Malicious member, persuasion propagation, communication strategy, group size, collective decision integrity, and system-level metrics.

### Taxonomy Implications

The study supports separating attack mechanism from the violated collective decision property and shows that topology/protocol choices condition propagation.

### Supported Research Questions

How do adversarial fraction, communication schedule, and group size affect collective robustness, and how should population-level success be measured?

### Important Limitations

The maximum honest group size is five, tasks have fixed answers, and agents do not have heterogeneous roles.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The framework studies three scenarios and multiple communication/group configurations. | Explicit author claim | Paper | 2.1 | 2 | - | Experimental overview. |
| Adversarial agents generate counterfactual answers and adapt using stored interaction history. | Explicit author claim | Paper | 2.2 | 2 | - | Component definition. |
| SDI incorporates affected agents and the time of first influence. | Explicit author claim | Paper | 2.3 | 2-3 | Equations 1-3 | Metric definition. |
| More adversarial agents reduce robustness and produce earlier influence. | Explicit author claim | Paper | 3.1 | 3-4 | Figures 1-3 | Group-dynamics analysis. |
| Reflection can improve average robustness but can also entrench an incorrect response. | Explicit author claim | Paper | 3.2 | 4-6 | Figure 4 | Mitigation analysis. |
| Scale, fixed-answer tasks, and homogeneous roles limit generalization. | Explicit author claim | Paper | Limitations | 9 | - | Limitations statement. |

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
