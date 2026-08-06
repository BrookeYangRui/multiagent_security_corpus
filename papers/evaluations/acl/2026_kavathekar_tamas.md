# TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems

## Citation

Title: TAMAS: Benchmarking Adversarial Risks in Multi-Agent LLM Systems

Authors: Ishan Kavathekar; Hemang Jain; Ameya Rathod; Ponnurangam Kumaraguru; Tanuja Ganu

Year: 2026

Venue: ACL

DOI: 10.18653/v1/2026.acl-long.1442

Primary URL: https://aclanthology.org/2026.acl-long.1442/

Open access URL: https://aclanthology.org/2026.acl-long.1442.pdf

BibTeX key: kavathekar2026tamas

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied

AutoGen and CrewAI systems using centralized, decentralized, and sequential interaction configurations.

### Multi-Agent Dependency

The benchmark varies the communication and orchestration structure through which compromised inputs, identities, and tools affect collaborating agents.

### Application Domain

Education, legal, finance, healthcare, and e-commerce.

## Security Model

### Protected Assets

Task integrity, safe tool use, confidentiality, and service availability.

### Threat Actor

Malicious user or external source able to inject adversarial content or impersonate an authority.

### Trusted Components

Benchmark harness, task labels, and evaluators.

### Attacker Capabilities

Direct and indirect prompt injection, impersonation, information theft, malicious code execution, and denial of service.

### Security Assumptions

Attacks are instantiated through the benchmark's specified interfaces and tool environment.

## Main Contribution

TAMAS provides five scenarios with 300 adversarial instances across six attack types and 211 tools, plus 100 harmless tasks. It evaluates ten LLMs in three interaction configurations and introduces Effective Robustness Score (ERS) to combine safety with task effectiveness.

## Attack or Failure

### Attack Surface

User prompts, external content, identities, and tool interfaces.

### Attack Mechanism

Scenario-specific adversarial instructions exploit the routing and trust relations in a MAS.

### System-Level Failure

Unsafe task execution, information disclosure, or failure to complete the benign task.

### Security Consequence

Loss of integrity, confidentiality, or availability at workflow level.

## Defense

### Defense Mechanism

Not proposed; the paper evaluates robustness.

### Intervention Point

Not applicable.

### Required Observability

The evaluation observes final task and attack outcomes.

### Assumptions

ERS assumes both attack resistance and benign effectiveness are measurable.

### Limitations

The selected frameworks, models, scenarios, and attack implementations do not cover every deployed MAS.

## Evaluation

### Evaluated Systems

AutoGen Magentic-One and CrewAI configurations across ten backbone LLMs.

### Agent Configuration

Centralized orchestrator, decentralized collaboration, and sequential collaboration.

### Dataset or Environment

300 adversarial instances, 100 harmless tasks, five domains, and 211 tools.

### Baselines

Single-agent and multiple MAS configurations are compared where specified by the benchmark.

### Metrics

Attack Success Rate, Task Success Rate, and Effective Robustness Score.

### Main Results

The benchmark reports substantial vulnerability and a safety-utility trade-off that varies by model and interaction configuration.

## Relation to Existing Work

### Papers Compared by the Authors

AgentDojo, InjecAgent, RedCode, and Agent Security Bench.

### Claimed Research Gap

Existing security benchmarks primarily evaluate isolated agents or narrow attacks.

### Closest Related Work

Agent Security Bench and MAS attack studies.

### Difference From Prior Work

TAMAS jointly varies attack type, domain, framework, and multi-agent interaction configuration.

## Relevance to Our SoK

### Included Concepts

Attack surfaces, topology, tool use, system-level success, and metric contracts.

### Taxonomy Implications

Shows why benchmark denominators must distinguish harmful success from benign task effectiveness.

### Supported Research Questions

How robust are common MAS configurations, and how does interaction structure affect that robustness?

### Important Limitations

ERS is benchmark-specific and does not by itself normalize population-level spread.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| TAMAS contains 300 adversarial instances, six attack types, 211 tools, and 100 harmless tasks. | Explicit author claim | Paper | Abstract; 5.1 | 1; 6 | Table 3 | Benchmark composition. |
| Ten LLMs and three interaction configurations are evaluated. | Explicit author claim | Paper | Abstract; 5 | 1; 6-7 | - | Evaluation scope. |
| ERS combines safety and task effectiveness. | Explicit author claim | Paper | Abstract; 5 | 1; 7 | - | Metric definition. |

## Provenance

### Discovery Source

ACL Anthology; local corpus; benchmark keyword search.

### Discovery Query

multi-agent LLM security benchmark TAMAS

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
