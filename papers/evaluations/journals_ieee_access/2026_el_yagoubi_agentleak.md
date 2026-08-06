# AgentLeak: A Benchmark for Internal-Channel Privacy Leakage in Multi-Agent LLM Systems

## Citation

Title: AgentLeak: A Benchmark for Internal-Channel Privacy Leakage in Multi-Agent LLM Systems

Authors: Faouzi El Yagoubi; Godwin Badu-Marfo; Ranwa Al Mallah

Year: 2026

Venue: IEEE Access

DOI: 10.1109/ACCESS.2026.3704541

Primary URL: https://doi.org/10.1109/ACCESS.2026.3704541

Open access URL: https://arxiv.org/abs/2602.11510

BibTeX key: elyagoubi2026agentleak

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Coordinator-worker multi-agent LLM systems with internal messages, shared memory, tool calls, and final outputs.

### Multi-Agent Dependency

The benchmark audits privacy violations in channels created specifically by delegation and inter-agent coordination.

### Application Domain

Healthcare, finance, legal, and corporate workflows.

## Security Model

### Protected Assets

Contextually sensitive personal and organizational information.

### Threat Actor

No single strategic attacker is required; tasks and prompts elicit over-disclosure through normal coordination channels.

### Trusted Components

Benchmark instrumentation, privacy labels, and channel-level trace collection.

### Attacker Capabilities

Benchmark scenarios exercise a 32-class attack taxonomy across internal and external channels.

### Security Assumptions

Contextual-integrity labels and channel instrumentation correctly identify exposure.

## Main Contribution

AgentLeak introduces 1,000 scenarios, seven leakage channels, and a 32-class attack taxonomy for internal-channel privacy. It evaluates five production LLMs and shows that output-only audits materially undercount exposure in inter-agent messages and shared state.

## Attack or Failure

### Attack Surface

Final output, inter-agent messages, reasoning/context, tool arguments, and shared memory.

### Attack Mechanism

Sensitive context is unnecessarily transmitted or retained during coordination.

### System-Level Failure

Information crosses its authorized contextual boundary inside the workflow.

### Security Consequence

Confidentiality and data-minimization failure hidden from final-output monitoring.

## Defense

### Defense Mechanism

The benchmark motivates channel-aware auditing; it does not establish a universal privacy defense.

### Intervention Point

Inter-agent message, memory, and tool boundaries.

### Required Observability

Full internal traces across seven channels.

### Assumptions

The auditor can instrument the evaluated framework.

### Limitations

Results depend on benchmark domains, privacy labels, frameworks, and five selected models.

## Evaluation

### Evaluated Systems

Five production LLMs in coordinator-worker configurations.

### Agent Configuration

Multi-agent versus single-agent comparisons with instrumented internal channels.

### Dataset or Environment

1,000 scenarios across four high-stakes domains and 4,979 execution traces.

### Baselines

Single-agent mode and final-output-only auditing.

### Metrics

External Leakage Rate, Whole-system Leakage Score, Channel Leakage Rate, and Attack Success Rate.

### Main Results

Inter-agent messages leak at 68.8% versus 27.2% for final outputs; auditing only final output misses 41.7 percentage points of violations in that comparison.

## Relation to Existing Work

### Papers Compared by the Authors

Privacy benchmarks that inspect final outputs and single-agent traces.

### Claimed Research Gap

Existing evaluations miss privacy exposure inside MAS coordination channels.

### Closest Related Work

MAGPIE and agent privacy-leakage benchmarks.

### Difference From Prior Work

AgentLeak explicitly instruments seven channels and measures whole-trace exposure.

## Relevance to Our SoK

### Included Concepts

Cross-agent confidentiality, observer scope, channel-level denominator, and contextual integrity.

### Taxonomy Implications

Demonstrates that final-output safety and whole-system confidentiality are different properties.

### Supported Research Questions

Which internal MAS channels dominate leakage, and what does an output-only observer miss?

### Important Limitations

The benchmark's aggregate leakage event is an any-channel union and should not be compared directly with per-channel rates.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| AgentLeak has 1,000 scenarios, seven channels, four domains, and five models. | Explicit author claim | Paper | Abstract; IV | 1; 6-9 | Benchmark tables | Benchmark scope. |
| Inter-agent messages leak at 68.8% and final outputs at 27.2%. | Explicit author claim | Paper | Abstract; VI | 1; 12-14 | Results tables | Channel comparison. |
| Whole-system exposure aggregates leakage across multiple channels. | Explicit author claim | Paper | IV; VI | 7; 12 | Metric definitions | Denominator and aggregation. |

## Provenance

### Discovery Source

IEEE DOI metadata; arXiv; local corpus.

### Discovery Query

AgentLeak IEEE Access multi-agent privacy benchmark

### Accessed Version

Published IEEE Access metadata with arXiv full text.

### Access Date

2026-08-05

### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-05
