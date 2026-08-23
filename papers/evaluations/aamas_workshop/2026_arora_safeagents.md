# Exposing Weak Links in Multi-Agent Systems under Adversarial Prompting

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `evaluation` · venue `AAMAS Strategic Engineering Workshop` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: Exposing Weak Links in Multi-Agent Systems under Adversarial Prompting

Authors: Nirmit Arora; Sathvik Joel; Ishan Kavathekar; Palak; Rohan Gandhi; Yash Pandya; Tanuja Ganu; Aditya Kanade; Akshay Nambi

Year: 2026

Venue: AAMAS Strategic Engineering Workshop

DOI: Not reported

Primary URL: https://openreview.net/forum?id=XC5vOg5UTf

Open access URL: https://arxiv.org/abs/2511.10949

BibTeX key: arora2026safeagents

## Paper Type

Benchmark; Evaluation; Attack; Empirical study

## Scope

### System Studied
Five centralized, decentralized, and hybrid MAS architectures for web, tool-use, and code tasks.

### Multi-Agent Dependency
SafeAgents diagnoses how planning, context delegation, and refusal/fallback behavior distribute safety decisions across agents.

### Application Domain
Web tasks, tool use, and code generation.

## Security Model

### Protected Assets
Safe task execution and correct refusal of harmful requests.

### Threat Actor
Adversarial user supplying harmful prompts.

### Trusted Components
Evaluation datasets, trajectory judge, framework adapters, and task outcome instrumentation.

### Attacker Capabilities
Issue direct harmful requests that are decomposed across the MAS.

### Security Assumptions
Architecture components and trajectories are observable to the evaluator.

## Main Contribution

SafeAgents is a unified framework for evaluating five MAS architectures on four datasets. It introduces DHARMA, a hierarchical diagnostic that attributes rejection and unsafe execution to planning, delegation, sub-agent, and fallback stages.

## Attack or Failure

### Attack Surface
User request, planner, delegated subtasks, context sharing, and fallbacks.

### Attack Mechanism
Task decomposition hides global harmful intent from locally scoped agents or converts refusal into later execution.

### System-Level Failure
The complete workflow executes a harmful request despite component-level safeguards.

### Security Consequence
Compositional action-integrity and monitoring failure.

## Defense

### Defense Mechanism
Architecture-aware diagnosis; the paper argues for design changes rather than a single post-hoc filter.

### Intervention Point
Planner, delegation, context, sub-agent, and fallback logic.

### Required Observability
Full trajectory and stage identities.

### Assumptions
An LLM judge can consistently classify DHARMA trajectory categories.

### Limitations
Judge error and framework-specific behavior affect diagnostic labels.

## Evaluation

### Evaluated Systems
Five widely used MAS architectures across multiple frameworks.

### Agent Configuration
Centralized, decentralized, and hybrid variants.

### Dataset or Environment
Four datasets spanning web, tool-use, and code-generation tasks.

### Baselines
Architectures and single-agent safety metrics under matched adversarial prompts.

### Metrics
Attack Success Rate, Refusal Rate, ARIA risk levels, and DHARMA categories.

### Main Results
The study identifies atomic delegation, missing planner fallbacks, and stratified plans without re-evaluation as recurring weak links.

## Relation to Existing Work

### Papers Compared by the Authors
AgentHarm, ASB, MAST, and aggregate agent safety metrics.

### Claimed Research Gap
Aggregate ASR and refusal rates do not locate the component that produced a system-level failure.

### Closest Related Work
TAMAS and Architecture Matters.

### Difference From Prior Work
DHARMA attributes outcomes to architecture stages rather than only scoring final behavior.

## Relevance to Our SoK

### Included Concepts
Architecture, observer scope, delegation, fallbacks, stagewise metrics, and interaction evidence.

### Taxonomy Implications
Supports separating system design from attack mechanism and violated property.

### Supported Research Questions
Which architecture stage turns an adversarial request into harmful execution?

### Important Limitations
Published as an AAMAS workshop paper rather than the main proceedings.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| SafeAgents evaluates five architectures on four datasets. | Explicit author claim | Paper | Abstract; 4 | 1; 8-13 | Main tables | Evaluation scope. |
| DHARMA attributes rejection and execution outcomes to MAS stages. | Explicit author claim | Paper | 3 | 5-8 | Figure 3 | Metric design. |
| Three recurring architecture weak links are reported. | Explicit author claim | Paper | Abstract; 5 | 1; 13-18 | Results figures | Main finding. |

## Provenance

### Discovery Source
AAMAS workshop OpenReview; arXiv; author publication page; completeness audit.

### Discovery Query
SafeAgents AAMAS 2026 adversarial prompting

### Accessed Version
AAMAS Strategic Engineering Workshop 2026 version with arXiv v1 full text.

### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-06
