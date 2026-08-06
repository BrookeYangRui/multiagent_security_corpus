# HARP: Measuring Harm Amplification in Multi-Agent LLM Systems

## Citation

Title: HARP: Measuring Harm Amplification in Multi-Agent LLM Systems

Authors: Md Hafizur Rahman; Zafaryab Haider; Tanzim Mahfuz; Prabuddha Chakraborty

Year: 2026

Venue: arXiv

DOI: 10.48550/arXiv.2605.27489

Primary URL: https://arxiv.org/abs/2605.27489

Open access URL: https://arxiv.org/pdf/2605.27489

BibTeX key: rahman2026harp

## Paper Type

Benchmark; Evaluation; Attack; Defense; Empirical study

## Scope

### System Studied
Finance-oriented seven-agent workflows with specialist agents, tools, shared context, memory, and a deterministic decision gate.

### Multi-Agent Dependency
HARP compares local perturbation with harm measured over the complete multi-agent trace, explicitly modeling propagation beyond the initially compromised component.

### Application Domain
Finance and tool-using delegated workflows.

## Security Model

### Protected Assets
Decision integrity, benign utility, and bounded malicious impact.

### Threat Actor
Compromised specialist, colluding agents, or a shared-context attacker.

### Trusted Components
Trace oracle, decision gate, tool environment, and attack labels.

### Attacker Capabilities
Specialist compromise, collusion, shared-context corruption, temporal persistence, and memory persistence.

### Security Assumptions
Paired clean and perturbed executions are comparable and traceable.

## Main Contribution

HARP is a trace-first methodology that defines local harm, global harm, and harm amplification as their ratio. It evaluates twelve scenarios and five defense settings using specialist outputs, tool calls, memory operations, guard events, latency, token cost, and decisions.

## Attack or Failure

### Attack Surface
Agent outputs, tools, shared context, memory, and decision gates.

### Attack Mechanism
A local perturbation is reused or amplified by downstream agents.

### System-Level Failure
Global harm exceeds the local attack effect.

### Security Consequence
Propagation and containment failure that binary ASR does not expose.

## Defense

### Defense Mechanism
Prompt-only guards, pre-tool and step-level guards, and IntegrityGuard trace consistency.

### Intervention Point
Prompt, tool boundary, execution step, and global trace.

### Required Observability
Full paired traces including memory and tool events.

### Assumptions
Trace consistency can be checked against the clean/perturbed oracle.

### Limitations
The finance workflow, seven-agent architecture, and attack harness are controlled abstractions.

## Evaluation

### Evaluated Systems
Seven-agent finance MAS.

### Agent Configuration
Specialist roles with deterministic decision gate.

### Dataset or Environment
Twelve scenarios and five defense settings.

### Baselines
No defense, prompt sandwiching, LlamaFirewall, ToolSafe, and IntegrityGuard.

### Metrics
Local/global harm, harm amplification, ASR, safe and malicious impact, stealth, utility, latency, and token cost.

### Main Results
Shared-context corruption gives the highest ASR, temporal persistence the largest malicious impact, and IntegrityGuard the lowest reported ASR and global harm with utility/cost trade-offs.

## Relation to Existing Work

### Papers Compared by the Authors
TAMAS, Who's the Mole, AgentDojo, and single-agent safety guards.

### Claimed Research Gap
Existing benchmarks emphasize attack success, blocking, task completion, or final harmfulness rather than propagation.

### Closest Related Work
MAS contagion and benchmark papers.

### Difference From Prior Work
HARP introduces paired trace scoring for local-to-global amplification.

## Relevance to Our SoK

### Included Concepts
Propagation, global trace, harm denominator, defense placement, and containment.

### Taxonomy Implications
Requires recording both local and system-level units for attack severity.

### Supported Research Questions
How much harm does interaction add beyond the initial compromise?

### Important Limitations
Preprint-only evidence and one principal application domain.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| HARP defines harm amplification as global harm divided by local harm. | Explicit author claim | Paper | Abstract; 3 | 1; 4-6 | - | Metric definition. |
| The study covers twelve scenarios and five defenses. | Explicit author claim | Paper | Abstract; 5 | 1; 8-13 | Main tables | Evaluation scope. |
| Trace-level defenses change ASR, harm, utility, and cost differently. | Explicit author claim | Paper | Abstract; 5 | 1; 8-13 | Tables 3-5 | Main result. |

## Provenance

### Discovery Source
arXiv; MAS metric audit search.

### Discovery Query
multi-agent LLM harm amplification benchmark trace

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
