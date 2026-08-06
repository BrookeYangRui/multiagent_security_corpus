# Adversarial Attacks in Multi-Agent LLM Pipelines: Unveiling Structural Vulnerabilities in Agentic AI Architectures

## Citation

Title: Adversarial Attacks in Multi-Agent LLM Pipelines: Unveiling Structural Vulnerabilities in Agentic AI Architectures

Authors: Faisal Haque Bappy; Tahrim Hossain; Tarannum Shaila Zaman; Raiful Hasan; Kamrul Hasan; Tariqul Islam

Year: 2026

Venue: IEEE GLOBECOM

DOI: Not reported

Primary URL: https://arxiv.org/abs/2608.00718

Open access URL: https://arxiv.org/pdf/2608.00718

BibTeX key: bappy2026adversarialpipelines

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

A ten-agent, five-layer pipeline with orchestrator, planner, parallel execution agents, reviewers, summarizer, and validator.

### Multi-Agent Dependency

The attacks exploit missing checks when content, plans, results, and identities cross agent-to-agent boundaries and then propagate through the pipeline.

### Application Domain

General task solving, retrieval, analysis, code generation, and review.

## Security Model

### Protected Assets

Task integrity, plan compliance, agent identity, provenance, and final-answer correctness.

### Threat Actor

An adversary controlling retrieved content, one or more pipeline positions, or a process responding at an agent routing slot.

### Trusted Components

The controlled experiment harness, task labels, and trace instrumentation.

### Attacker Capabilities

Prompt injection, consensus poisoning, plan hijacking, and Sybil substitution at specified boundaries.

### Security Assumptions

Pipeline architecture is held constant across model backbones and attacks are evaluated with predeclared success conditions.

## Main Contribution

The paper derives four attack classes from 147 annotated TRAIL traces and operationalizes them in a controlled multi-agent pipeline. It frames boundary verification over content, delegation, and identity as the missing security primitive.

## Attack or Failure

### Attack Surface

Retrieved content, aggregation, planner delegation, retry identity, and inter-agent messages.

### Attack Mechanism

Payloads exploit absent content typing, quorum checks, plan-to-trace enforcement, or credential binding.

### System-Level Failure

The pipeline accepts poisoned results, skips planned work, substitutes Sybil processes, or propagates injected instructions to the final output.

### Security Consequence

Loss of collective decision integrity, identity integrity, provenance, and task correctness.

## Defense

### Defense Mechanism

No implemented defense; the paper recommends boundary sanitization, quorum-based commitment, credential attestation, and out-of-band auditing.

### Intervention Point

Inter-agent edges, orchestrator aggregation, and routing identity.

### Required Observability

Messages, declared plans, execution traces, agent credentials, and routing events.

### Assumptions

Suggested defenses require a trusted enforcement layer outside the agent's own context.

### Limitations

The controlled evaluation fixes one pipeline architecture, 20 tasks, and three models; trace-derived classes come from GAIA and SWE-Bench settings.

## Evaluation

### Evaluated Systems

The same ten-agent pipeline using GPT-5-mini, Claude Sonnet 4.5, or Kimi K2.5.

### Agent Configuration

Five layers: orchestrator, planner, four parallel executors, two reviewers, and two output agents.

### Dataset or Environment

147 TRAIL traces with 836 labeled errors, followed by 20 shared tasks and three escalating payload variants per attack class.

### Baselines

Ninety clean runs with reported baseline accuracy of 0.80.

### Metrics

Attack success rate, task accuracy under attack, recovery rate, and propagation hop count.

### Main Results

Across 1,080 attack runs, every attack class exceeds 0.60 success; recovery is low and model-to-model variation is smaller than attack-class variation under the fixed architecture.

## Relation to Existing Work

### Papers Compared by the Authors

AgentDojo, Agent Security Bench, Agent Smith, Secret Collusion, PsySafe, and multi-agent jailbreak defenses.

### Claimed Research Gap

Existing benchmarks synthesize attacks or score final outputs without identifying naturally occurring cross-boundary failure modes in traces.

### Closest Related Work

Conjunctive prompt attacks, Agent Cascading Injection, and topology-guided propagation attacks.

### Difference From Prior Work

Attack classes are first derived from annotated benign traces and then tested under a fixed cross-model pipeline.

## Relevance to Our SoK

### Included Concepts

Boundary verification, delegation, identity, quorum, propagation, trace visibility, and structural ablation.

### Taxonomy Implications

The mechanisms map to propagation, decision integrity, and compositional authority failures rather than one undifferentiated prompt-injection class.

### Supported Research Questions

Does an empirical design isolate interaction structure, and what metadata is required to enforce inter-agent boundaries?

### Important Limitations

Acceptance is stated in the arXiv metadata and manuscript; an IEEE proceedings page and DOI were not yet available on the access date.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Four attack classes are derived from 147 traces containing 836 labeled errors. | Explicit author claim | Paper | 1; 3 | 2-3 | - | Trace-screening corpus and contribution statement. |
| The controlled study contains 1,080 attack runs and 90 clean runs. | Explicit author claim | Paper | 4 | 5 | Figure 6 | Evaluation denominator. |
| Four metrics cover success, task accuracy, recovery, and hop count. | Explicit author claim | Paper | 4 | 5-6 | Figure 6 | Measurement contract. |
| GLOBECOM acceptance is not yet backed by a proceedings DOI. | Metadata verification | arXiv metadata; manuscript | Comment; first page | - | - | Accepted status checked separately from archival publication availability. |

## Provenance

### Discovery Source

arXiv current-cutoff scan; full-text screening; publication-status search.

### Discovery Query

2026 evaluation multi-agent LLM attack defense benchmark

### Accessed Version

arXiv v1 author manuscript accepted at IEEE GLOBECOM 2026; proceedings version not yet available.

### Access Date

2026-08-06
### Prepared By

Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status

agent_unverified

### Last Updated

2026-08-06
