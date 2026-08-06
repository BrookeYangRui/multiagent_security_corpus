# A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

Title: A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems

Authors: Tianhao Li; Chuangxin Chu; Yujia Zheng; Bohan Zhang; Neil Zhenqiang Gong; Chaowei Xiao

Year: 2026

Venue: ICLR

DOI: Not reported

Primary URL: https://iclr.cc/virtual/2026/poster/10010017

Open access URL: https://openreview.net/forum?id=LfdFnakqGJ

BibTeX key: li2026a2asecbench

## Paper Type

Benchmark; Evaluation; Attack suite

- Primary category: `evaluation`
- Scope relation: `core_security`

## Scope

### System Studied
Heterogeneous client and remote agents communicating through the Agent-to-Agent protocol for discovery, task orchestration, and artifact exchange.

### Multi-Agent Dependency
The six attacks target AgentCards, discovery, asynchronous task state, remote endpoints, and returned artifacts created by the A2A relationship.

### Application Domain
Travel, healthcare, and finance.

## Security Model

### Protected Assets
Agent identity, capability integrity, availability, confidential resources, and safe artifact handling.

### Threat Actor
Malicious registered remote agent, spoofed AgentCard publisher, or protocol peer.

### Trusted Components
Official A2A demos, benchmark adapter, workload oracle, and benign task labels.

### Attacker Capabilities
AgentCard spoofing, capability cloaking, cycle overflow, half-open task flooding, agent-side request forgery, and artifact-triggered script injection.

### Security Assumptions
The adversary operates through protocol-valid discovery and task interfaces represented by the benchmark.

## Main Contribution

A2ASecBench provides a protocol-specific threat model, six attacks, and a dynamic adapter for heterogeneous A2A stacks. It pairs adversarial trials with benign tasks to measure safety and utility jointly on official A2A demos in three high-stakes domains.

## Attack or Failure

### Attack Surface
Agent registry, AgentCard, task lifecycle, remote requests, and artifacts.

### Attack Mechanism
Supply-chain manipulation or protocol-logic abuse admits and activates a malicious peer.

### System-Level Failure
Identity confusion, task-loop exhaustion, unauthorized requests, or unsafe artifact execution.

### Security Consequence
Confidentiality, integrity, and availability failure across agent boundaries.

## Defense

### Defense Mechanism
The paper evaluates default safeguards but does not establish a complete protocol defense.

### Intervention Point
Discovery, admission, task state, request, and artifact boundaries.

### Required Observability
AgentCard metadata, protocol messages, task state, artifacts, and environment outcomes.

### Assumptions
The benchmark adapter preserves semantics across agent stacks.

### Limitations
The official demo set and three domains do not cover all A2A implementations or deployment policies.

## Evaluation

### Evaluated Systems
Official A2A Project demos deployed through a dynamic adapter.

### Agent Configuration
Client agents interact with heterogeneous remote service agents.

### Dataset or Environment
Benign and adversarial tasks in travel, healthcare, and finance.

### Baselines
Default safeguards and benign paired trials.

### Metrics
Safety/attack outcomes and benign utility/helpfulness.

### Main Results
The six attacks consistently bypass default safeguards in the evaluated demos.

## Relation to Existing Work

### Papers Compared by the Authors
MCP security work and general agent-security benchmarks.

### Claimed Research Gap
Existing benchmarks do not cover the A2A protocol lifecycle and heterogeneous peer stacks.

### Closest Related Work
MCP-SafetyBench and MCP Security Bench.

### Difference From Prior Work
The benchmark centers A2A discovery, remote task state, and artifact exchange rather than host-tool calls.

## Relevance to Our SoK

### Included Concepts
Protocol, membership, identity, remote authority, availability, and joint safety-utility evaluation.

### Taxonomy Implications
Maps adversary position and protocol stage separately from CIA impact.

### Supported Research Questions
Which A2A lifecycle stages create security failures absent in one-agent tool use?

### Important Limitations
No DOI is reported; canonical status is verified through the official ICLR program and OpenReview record.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| A2ASecBench defines six attacks over all A2A stages and components. | Explicit author claim | Paper | Abstract; threat model | 1; 4-8 | Threat-model figure | Benchmark scope. |
| Evaluation uses official A2A demos in travel, healthcare, and finance. | Explicit author claim | Paper | Abstract; evaluation | 1; 8-11 | Main tables | Evaluation scope. |
| Benign tasks are paired with attacks for safety-utility evaluation. | Explicit author claim | Paper | Abstract; methodology | 1; 7-9 | - | Measurement contract. |

## Provenance

### Discovery Source
ICLR official program; OpenReview; author project page; completeness audit.

### Discovery Query
multi-agent security benchmark A2A protocol ICLR 2026

### Accessed Version
Published ICLR 2026 paper and official project materials.

### Access Date
2026-08-06
### Prepared By
Human or automated process: automated extraction

Model and version, if automatically generated: Not recorded

### Verification Status
agent_unverified

### Last Updated
2026-08-06

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `blocked_pending_exact_full_text`

**Outcome:** Pending exact full-text verification

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Official ICLR program and project repository confirm title, authors, and ICLR 2026 status. No DOI is reported. The full OpenReview PDF was not reliably retrievable during this audit, so exact page and table locators remain pending.
- Recommended scope: `core_security`
- Multi-agent dependency: The benchmark targets heterogeneous client and remote agents communicating through the A2A protocol across discovery, task state, requests, and artifacts.
- Recommended roles: benchmark; evaluation; attack suite
- Maturity: Archival peer-reviewed benchmark, but exact full-text evidence locators still require manual author access.

### Threat and Failure Coding

- Attacker or fault actor: Malicious registered remote agent, spoofed AgentCard publisher, or adversarial A2A protocol peer.
- Capabilities: AgentCard spoofing, capability cloaking, cyclic delegation, half-open task flooding, agent-side request forgery, and artifact-triggered script injection.
- Preconditions: Protocol-valid discovery, task, request, and artifact interfaces and an adapter that preserves semantics across implementations.
- Surfaces: Registry and AgentCard; discovery; asynchronous task state; remote requests; returned artifacts.
- Mechanism: Protocol-logic abuse or supply-chain manipulation introduces and activates a malicious peer.
- Primary system-level failure: Claim-level identity, confidentiality, integrity, or availability failures.
- Impact: Unsafe request handling, resource exhaustion, or artifact execution.

### Evaluation Contract

- Configuration: Official A2A demos in travel, healthcare, and finance through a dynamic adapter; deterministic offline and optional LLM-backed SUTs in the released repository.
- Topology: Client-to-remote-agent A2A interactions and task lifecycle rather than a generic graph benchmark.
- Baseline or ablation: Matched benign controls and default safeguard behavior; release includes deterministic offline baselines.
- Metric: Attack or safety outcome plus benign utility or helpfulness; Capability Cloaking also reports label accuracy and evidence quality.
- Unit: Benchmark case and SUT trial.
- Denominator: Repository release includes 100 AgentCard Spoofing cases and 100 cases for each Capability Cloaking split; other executable families have attack cases and matched controls.
- Result boundary: Official materials state that the six attack families bypass default safeguards in evaluated demos. Exact paper table values and full denominators must be copied from the final PDF before any quantitative manuscript claim.

### Evidence and Boundaries

- Evidence locations: Official ICLR 2026 poster record; project README for the seven listed benchmark rows, release-case counts, matched controls, deterministic baselines, and output schema. Exact paper page and table references remain unresolved.
- Author claim versus corpus interpretation: Benchmark attacks, release structure, and official program status are author or official-project claims. Taxonomic mapping is a corpus interpretation.
- Limitations: Official demo set and three domains; adapter semantics; full paper locators unavailable in this audit; no DOI; not all A2A stacks or deployment policies are covered.

### Required Corrections

- **CRITICAL - Primary category:** Change from attack to benchmark/evaluation with an attack-suite role.
- **CRITICAL - Evidence locators:** Obtain the final PDF and record exact page, figure, and table locations before manuscript use.
- **HIGH - Metric denominator:** Use release-case counts and matched-control denominators, then reconcile them with the paper tables.
<!-- SOURCE_REVIEW_END -->
