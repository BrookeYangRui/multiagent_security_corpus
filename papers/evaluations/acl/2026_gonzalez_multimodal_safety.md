# Multimodal Safety Evaluation in Generative Agent Social Simulations

## Citation

Title: Multimodal Safety Evaluation in Generative Agent Social Simulations

Authors: Alhim Adonai Vera Gonzalez; Carlos Hinojosa; Karen Sanchez; Haidar Bin Hamid; Donghoon Kim; Bernard Ghanem

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.1915

Primary URL: https://aclanthology.org/2026.acl-long.1915/

Open access URL: https://aclanthology.org/2026.acl-long.1915.pdf

BibTeX key: gonzalez2026multimodalsafety

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Generative-agent social simulations in which agents plan, perceive multimodal scenes, converse, reflect, and act.

### Multi-Agent Dependency

Unsafe plans and visual cues propagate into social actions through conversations and shared simulation state.

### Application Domain

Social activity simulations with text and images.

## Security Model

### Protected Assets

Safe plans, safe social actions, and reliable multimodal risk recognition.

### Threat Actor

No strategic attacker is required; the evaluation introduces unsafe scenarios and misleading visual cues.

### Trusted Components

Scenario construction, human verification, simulator, and safety annotators.

### Attacker Capabilities

Not applicable; the benchmark evaluates situational safety failures.

### Security Assumptions

The scenario and action labels represent the intended safety judgment.

## Main Contribution

The paper introduces a reproducible multimodal social-simulation framework and SocialMetrics. Its dataset contains 1,000 plans and produces more than 600,000 simulation steps for evaluating how unsafe inputs are revised or amplified through agent interaction.

## Attack or Failure

### Attack Surface

Initial plans, images, conversations, memory, and reflection.

### Attack Mechanism

Unsafe or misleading multimodal context affects downstream collective behavior.

### System-Level Failure

Agents accept, retain, or execute unsafe social actions.

### Security Consequence

Interaction-amplified situational safety failure.

## Defense

### Defense Mechanism

Planning and reflection can revise unsafe activities; no formal defense guarantee is proposed.

### Intervention Point

Plan revision and reflection stages.

### Required Observability

Plans, conversations, actions, and multimodal context.

### Assumptions

SocialMetrics relies on labeled unsafe plans and actions.

### Limitations

Simulated social behavior and model-based generation do not establish real-world prevalence.

## Evaluation

### Evaluated Systems

Generative agents using language and multimodal language models.

### Agent Configuration

Multiple agents share a social environment and interact over repeated simulation steps.

### Dataset or Environment

1,000 multimodal plans and over 600,000 action-level steps.

### Baselines

Safe versus unsafe plans and text-only versus multimodal conditions.

### Metrics

SocialMetrics for revision, acceptance, and execution of unsafe plans and actions.

### Main Results

The paper reports correction of 55% of unsafe plans but acceptance of unsafe actions in 45% of cases with misleading visual cues.

## Relation to Existing Work

### Papers Compared by the Authors

Multimodal safety benchmarks and generative-agent social simulations.

### Claimed Research Gap

Existing benchmarks do not connect multimodal situational risk to multi-agent social dynamics.

### Closest Related Work

Multimodal situational-safety and agent-society evaluation.

### Difference From Prior Work

The evaluation follows risk across planning, interaction, reflection, and execution.

## Relevance to Our SoK

### Included Concepts

Emergent safety, shared environment, multimodal context, and trace-level measurement.

### Taxonomy Implications

Distinguishes unsafe input recognition from unsafe system action.

### Supported Research Questions

How do multimodal cues and agent interactions change safety over time?

### Important Limitations

The work is safety-oriented and does not model a capability-bearing adversary.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The dataset contains 1,000 multimodal plans and yields more than 600,000 steps. | Explicit author claim | Paper | Abstract; 3 | 1; 3-4 | Figure 1 | Scale and pipeline. |
| The framework defines SocialMetrics over plans and actions. | Explicit author claim | Paper | 4 | 5 | - | Metric definitions. |
| Misleading visual cues leave substantial unsafe behavior uncorrected. | Explicit author claim | Paper | Abstract; 4 | 1; 6-8 | Main results | Reported safety outcome. |

## Provenance

### Discovery Source

ACL Anthology; formal venue scan.

### Discovery Query

ACL 2026 multi-agent safety evaluation benchmark

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
