# CalBench: Evaluating Coordination-Privacy Trade-offs in Multi-Agent LLMs

## Citation

Title: CalBench: Evaluating Coordination-Privacy Trade-offs in Multi-Agent LLMs

Authors: Chelsea Zou; Yiheng Yao; Selena She; Noah D. Goodman; Robert D. Hawkins

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2605.09823

Primary URL: https://arxiv.org/abs/2605.09823

Open access URL: https://arxiv.org/pdf/2605.09823

BibTeX key: zou2026calbench

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied
N assistants with private calendars coordinate M incoming meetings through configurable communication channels.

### Multi-Agent Dependency
No assistant has another participant's full calendar; coordination requires selective disclosure and distributed commitments.

### Application Domain
Calendar scheduling and delegated personal assistance.

## Security Model

### Protected Assets
Private availability and preferences, meeting feasibility, cost, and fair burden allocation.

### Threat Actor
No malicious actor is required; privacy and coordination failures are measured under ordinary delegation.

### Trusted Components
CP-SAT oracle, task generator, private-information constraints, and trace logger.

### Attacker Capabilities
Not applicable; information disclosure is evaluated as a system property.

### Security Assumptions
Private calendars remain inaccessible except through communication.

## Main Contribution

CalBench generates solvable scheduling scenarios with CP-SAT oracle solutions and non-LLM reference protocols. It evaluates task success, excess cost, communication efficiency, burden fairness, and privacy leakage under matched information constraints across seven model families.

## Attack or Failure

### Attack Surface
Agent-to-agent messages and scheduling commitments.

### Attack Mechanism
Over-disclosure, under-disclosure, or poor coordination with private state.

### System-Level Failure
Feasible schedules are missed, costs are unnecessarily high, or private information leaks.

### Security Consequence
Coordination-privacy trade-off and cross-principal confidentiality failure.

## Defense

### Defense Mechanism
Reference protocols and communication-condition comparisons; no universal defense.

### Intervention Point
Communication channel and commitment protocol.

### Required Observability
Private state for oracle evaluation; messages for leakage and efficiency.

### Assumptions
Oracle schedules and privacy labels correctly characterize the task.

### Limitations
Calendar scheduling is a controlled proxy for broader delegated agency.

## Evaluation

### Evaluated Systems
Seven model families and non-LLM reference protocols.

### Agent Configuration
Private DMs, participant group chat, and all-agent group chat.

### Dataset or Environment
Generated calendar scenarios with N agents, M meetings, and CP-SAT solutions.

### Baselines
Centralized/oracle and reference protocols under matched information.

### Metrics
Completion, excess disruption cost, communication volume, burden fairness, and privacy leakage.

### Main Results
Completion alone misses avoidable cost, communication volume does not predict lower regret, and privacy-preserving silence can harm fair burden allocation.

## Relation to Existing Work

### Papers Compared by the Authors
Agentic benchmarks, negotiation, and distributed constraint-optimization benchmarks.

### Claimed Research Gap
Existing benchmarks often centralize private state or omit privacy-utility trade-offs.

### Closest Related Work
Multi-agent scheduling and negotiation evaluations.

### Difference From Prior Work
CalBench matches private-information constraints to an oracle optimum.

## Relevance to Our SoK

### Included Concepts
Private memory, delegation, information flow, fairness, and denominator contracts.

### Taxonomy Implications
Privacy and utility must be measured jointly at group level.

### Supported Research Questions
How much information must agents reveal to coordinate efficiently and fairly?

### Important Limitations
Preprint-only and non-adversarial benchmark conditions.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| CalBench uses private calendars and CP-SAT oracle solutions. | Explicit author claim | Paper | Abstract; 3 | 1; 3-6 | Figure 1 | Task construction. |
| Three communication conditions are evaluated. | Explicit author claim | Paper | 3 | 4-7 | Figure 1 | Configuration. |
| Metrics include success, excess cost, efficiency, fairness, and privacy. | Explicit author claim | Paper | Abstract; 3 | 1; 5-8 | - | Metric contract. |

## Provenance

### Discovery Source
arXiv; multi-agent privacy and coordination benchmark search.

### Discovery Query
multi-agent LLM coordination privacy benchmark calendar

### Accessed Version
arXiv v3.

### Access Date
2026-08-05
### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-05
