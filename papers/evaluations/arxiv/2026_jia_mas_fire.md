# MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems

## Citation

Title: MAS-FIRE: Fault Injection and Reliability Evaluation for LLM-Based Multi-Agent Systems

Authors: Jin Jia; Zhiling Deng; Zhuangbin Chen; Yingqi Wang; Zibin Zheng

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2602.19843

Primary URL: https://arxiv.org/abs/2602.19843

Open access URL: https://arxiv.org/pdf/2602.19843

BibTeX key: jia2026masfire

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied
LLM-based MAS coordinating through unstructured natural-language messages.

### Multi-Agent Dependency
Injected semantic faults are reused, propagated, masked, or recovered from by downstream agents.

### Application Domain
Collaborative software and reasoning workflows.

## Security Model

### Protected Assets
Reliability, task integrity, and recovery.

### Threat Actor
Fault-injection harness; faults need not be malicious.

### Trusted Components
Harness, injection controller, trace recorder, and task oracle.

### Attacker Capabilities
Inject semantic deviations at selected agents and interaction points.

### Security Assumptions
The framework can identify injected fault position and downstream outcomes.

## Main Contribution

MAS-FIRE provides systematic semantic fault injection and trace-based reliability evaluation for LLM MAS. It measures propagation and recovery rather than only end-to-end task success.

## Attack or Failure

### Attack Surface
Agent outputs and inter-agent messages.

### Attack Mechanism
Hallucination, instruction misinterpretation, and reasoning drift are injected at controlled points.

### System-Level Failure
Fault propagation, masking, or unsuccessful recovery.

### Security Consequence
Loss of workflow reliability and diagnosability.

## Defense

### Defense Mechanism
No universal defense; recovery behavior is evaluated.

### Intervention Point
Agent and message stages.

### Required Observability
Full execution trace plus fault ground truth.

### Assumptions
Semantic fault labels are meaningful proxies for deployment failures.

### Limitations
Synthetic injections may not reproduce all naturally occurring or adversarial faults.

## Evaluation

### Evaluated Systems
Multiple LLM MAS frameworks and tasks described by the paper.

### Agent Configuration
Role-structured workflows with controlled injection sites.

### Dataset or Environment
Task suites paired with a semantic fault library.

### Baselines
Clean runs and end-to-end outcome evaluation.

### Metrics
Task outcome, propagation, masking, and recovery measures.

### Main Results
Trace-level analysis reveals failure and recovery behavior hidden by final success alone.

## Relation to Existing Work

### Papers Compared by the Authors
MAS capability benchmarks and software fault-injection research.

### Claimed Research Gap
End-to-end success does not explain where semantic failures spread or recover.

### Closest Related Work
MAS reliability and cascading-failure evaluations.

### Difference From Prior Work
MAS-FIRE injects faults at interaction points and follows their lifecycle.

## Relevance to Our SoK

### Included Concepts
Fault propagation, recovery, trace observability, and interaction evidence.

### Taxonomy Implications
Separates injected mechanism from propagation outcome.

### Supported Research Questions
Where do semantic failures propagate, and which agents recover from them?

### Important Limitations
Reliability faults are adjacent to security unless an adversary controls the injection.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| MAS-FIRE injects semantic rather than only crash faults. | Explicit author claim | Paper | Abstract; 3 | 1; 4-7 | Framework figure | Fault model. |
| It measures propagation and recovery beyond final task success. | Explicit author claim | Paper | Abstract; 4 | 1; 7-11 | Main tables | Evaluation contract. |

## Provenance

### Discovery Source
arXiv security/reliability query; local corpus screening.

### Discovery Query
multi-agent LLM fault injection reliability benchmark

### Accessed Version
arXiv v1.

### Access Date
2026-08-05
### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-05
