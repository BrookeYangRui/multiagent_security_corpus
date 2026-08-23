# A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `ICLR` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

Title: A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems

Authors: Tianhao Li; Chuangxin Chu; Yujia Zheng; Bohan Zhang; Neil Zhenqiang Gong; Chaowei Xiao

Year: 2026

Venue: ICLR

Version: Published conference paper at ICLR 2026

DOI: Not reported

Primary URL: https://openreview.net/pdf?id=LfdFnakqGJ

Open access URL: https://proceedings.iclr.cc/paper_files/paper/2026/file/c6a4c60e4c12b4157d33f34b29d22067-Paper-Conference.pdf

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
The actor depends on the attack. AgentCard Spoofing uses a spoofed publisher; Capability Cloaking and Artifact-Triggered Script Injection use a malicious registered remote agent; Cycle Overflow, Half-Open Task Flooding, and Agent-Side Request Forgery can be induced by an adversarial client or user. In ASRF and ATSI, the Host becomes a confused deputy that relays the attack across a trust boundary.

### Trusted Components
Official A2A samples, benchmark adapter, scenario prompts, canary instrumentation, and benign task labels.

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
Supply-chain manipulation corrupts discovery and admission, while protocol-logic abuse exploits task state, privileged dereferencing, or artifact relay after a protocol-valid request reaches the system.

### System-Level Failure
Identity confusion, task-loop exhaustion, unauthorized requests, or unsafe artifact delivery whose formal threat target is downstream execution.

### Security Consequence
Confidentiality, integrity, and availability failure across agent boundaries. For ATSI, the evaluation verifies artifact delivery rather than the full formal execution-and-harm consequence.

## Defense

### Defense Mechanism
The paper evaluates NVIDIA NeMo Guardrails as an input gateway for four protocol-level attacks and proposes, but does not implement as a complete defense, prompt hardening, progress-aware orchestration, peer authentication, quotas, DAG validation, artifact sanitization, verifiable AgentCards, and capability attestation.

### Intervention Point
Discovery, admission, task state, request, and artifact boundaries.

### Required Observability
AgentCard metadata, protocol messages, task state, artifacts, and environment outcomes.

### Assumptions
The benchmark adapter preserves semantics across agent stacks.

### Limitations
The official demo set and three domains do not cover all A2A implementations or deployment policies. The NeMo experiment is a gateway stress test rather than a complete hardened protocol, and its table does not state a trial denominator.

## Evaluation

### Evaluated Systems
An official-sample-based system with one Host coordinating three client wrappers connected to three remote A2A servers. The Host and remote servers S1--S3 use Gemini 2.5 Flash; the adapter instantiates travel, healthcare, and finance scenarios. Transfer experiments additionally cover LangGraph and ANP.

### Agent Configuration
The front end invokes one Host, which coordinates three A2A clients C1--C3 connected to three remote servers S1--S3. The topology is fixed in the main study; attack cases exercise discovery, request, task-state, and response paths within it.

### Dataset or Environment
Table 5 reports 100 benign tasks and 100 cases for each of AgentCard Spoofing, Cycle Overflow, Half-Open Task Flooding, Agent-Side Request Forgery, and Artifact-Triggered Script Injection in each of three domains. This yields 600 cases per domain and 1,800 total. Capability Cloaking is evaluated through benign-task utility degradation and is not a separate Table 5 task family.

### Baselines
Default safeguards and matched benign tasks; NVIDIA NeMo Guardrails as an evaluated input gateway; LangGraph and ANP as transfer targets. These are component or attack controls, not an interaction-removal or matched single-agent counterfactual.

### Metrics
Per-condition attack success rate with attack-specific criteria. AgentCard Spoofing measures failure to select the benign card; Cycle Overflow and Half-Open Task Flooding use timeout, repeated routing, or service disruption; Agent-Side Request Forgery uses a returned canary after malicious dereferencing; Artifact-Triggered Script Injection operationally uses return of a canary-bearing artifact. Capability Cloaking is reported through utility degradation as well as an ASR row.

### Main Results
Table 2 reports AgentCard Spoofing ASR of 0.820, 0.816, and 0.828 in travel, healthcare, and finance. The other five rows are 1.00 in all three domains. Capability Cloaking reduces benign utility from 0.853 to 0.682, 0.872 to 0.595, and 0.962 to 0.749, respectively. The paper does not report a separate Capability Cloaking trial denominator, and its Artifact-Triggered Script Injection operational label does not independently establish browser execution or downstream harm.

## Provisional Measurement Coding

This coding is a SoK interpretation of the published ICLR paper and remains pending named human signoff.

### Impact Stage
`S3_executed_or_persistent`. The evaluated failures include dereferencing internal resources, persistent half-open tasks, repeated routing until timeout, and returned artifacts that reach the client. This label does not upgrade the ATSI result to independently verified browser harm.

### Interaction Counterfactual
`component_or_attack_controls`. Benign trials, default behavior, NeMo, and transfer targets are useful controls, but the paper does not remove an interaction edge or report a matched topology or single-agent ablation.

### Artifact Availability
`code_and_data`. The authors link the benchmark repository and project materials; availability is recorded without claiming independent reproduction.

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
No DOI is reported. The published paper leaves the Capability Cloaking ASR denominator and the trial denominators for Tables 3--4 unstated. AgentCard Spoofing describes `k=10` adversarial variants plus one benign card, while its prompts ask the model to choose among ten cards. The ATSI formal definition requires execution and a harmful outcome, but its operational success rule only checks whether the canary-bearing artifact is returned to the client.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| A2ASecBench defines six attacks across A2A lifecycle stages and protocol components. | Explicit author claim | Paper | Abstract; 3 | 1; 3-4 | Figure 1; Table 1 | Threat classes and stage/component/CIA mapping. |
| Each attack has a formal and operational success criterion. | Explicit author claim | Paper | 4.2 | 5-6 | - | AS, CC, CO, HOTF, ASRF, and ATSI definitions. |
| The main system has one Host, three client wrappers, and three remote servers across three domains. | Explicit author claim | Paper | 5.1 | 7 | Figure 2 | Main configuration and models. |
| Table 2 reports AS at 0.820/0.816/0.828 and the other five rows at 1.00 across the three domains. | Explicit author claim | Paper | 5.3 | 7-8 | Table 2 | Main result; CC also reports utility deltas. |
| NeMo leaves nonzero residual ASR for all four evaluated protocol-level attacks. | Explicit author claim | Paper | 5.5 | 9 | Table 4 | Gateway defense stress test; trial denominator unstated. |
| The benchmark contains 1,800 enumerated tasks, while CC has no separate task family in the count. | Explicit author claim | Paper | Appendix A | 14 | Figure 5; Table 5 | 100 benign plus 100 each for five attack types per domain. |
| ATSI's operational success rule is weaker than its formal harm definition. | Source-boundary observation | Paper | 4.2; 5.2 | 6-7 | - | Returned canary-bearing artifact is not independently verified browser execution. |

## Provenance

### Discovery Source
ICLR official program; OpenReview; author project page; completeness audit.

### Discovery Query
multi-agent security benchmark A2A protocol ICLR 2026

### Accessed Version
Published ICLR 2026 conference paper from the official proceedings; corresponding OpenReview record `LfdFnakqGJ`.

### Source SHA-256
`bc5a74aa624232346b2fd649ae0baa6d331a2d4a5336a03d26fff310bd10084a`

### Access Date
2026-08-10
### Prepared By
Human or automated process: automated primary-source audit

Model and version, if automatically generated: OpenAI Codex; exact serving version not recorded in the repository

### Verification Status
assistant_source_reviewed_pending_named_human_signoff

### Last Updated
2026-08-10

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `assistant_source_reviewed_pending_author_signoff`

**Outcome:** Published primary source recovered and claim extraction completed; pending named human signoff

**Review source:** `reviews/universal/active_source_review.csv`, applied through `active_source_review_row_overrides.csv` while preserving `universal_114_source_review.csv` as history

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: The official ICLR proceedings paper matches the title, six-author list, and OpenReview identifier `LfdFnakqGJ`, and is labeled as a published ICLR 2026 conference paper. No DOI is reported.
- Recommended scope: `core_security`
- Multi-agent dependency: The benchmark targets heterogeneous client and remote agents communicating through the A2A protocol across discovery, task state, requests, and artifacts.
- Recommended roles: benchmark; evaluation; attack suite
- Maturity: Archival peer-reviewed benchmark with exact full-text evidence locators; interpretation remains pending named human signoff.

### Threat and Failure Coding

- Attacker or fault actor: Spoofed publisher for AS; malicious registered remote agent for CC and ATSI; adversarial client or user for CO, HOTF, and ASRF. The Host is a confused deputy for ASRF and ATSI.
- Capabilities: AgentCard spoofing, capability cloaking, cyclic delegation, half-open task flooding, agent-side request forgery, and artifact-triggered script injection.
- Preconditions: Protocol-valid discovery, task, request, and artifact interfaces and an adapter that preserves semantics across implementations.
- Surfaces: Registry and AgentCard; discovery; asynchronous task state; remote requests; returned artifacts.
- Mechanism: Discovery attacks manipulate AgentCards or capability claims; lifecycle attacks create cycles or half-open tasks; relay attacks exploit privileged FilePart dereferencing or untrusted artifact forwarding.
- Primary system-level failure: Agent-selection/capability integrity, workflow availability, privileged-resource confidentiality, or artifact integrity failure.
- Impact: Unsafe request handling, resource exhaustion, or artifact delivery targeting downstream execution; the ATSI experiment stops at delivery.
- Stage/component/CIA map: AS--Discovery/AgentCard/Integrity; CC--Discovery/AgentCard/Integrity; CO--Initiation and Processing/Message, Task, Stream/Availability; HOTF--Initiation and Interaction/Task, Session, Stream/Availability; ASRF--Processing/Part/Confidentiality; ATSI--Completion/Artifact/Integrity (Table 1).

### Evaluation Contract

- Configuration: One Host coordinates three A2A clients connected to three remote servers; Host and S1--S3 use Gemini 2.5 Flash. The adapter covers travel, healthcare, and finance (p. 7, Figure 2).
- Topology: Front end to Host to three client/server A2A links, with the Host relaying requests and responses across trust boundaries.
- Baseline or ablation: Default safeguards, matched benign tasks, a NeMo gateway condition, and LangGraph/ANP transfer studies. These are component or attack controls, not interaction-removal ablations.
- Metric: Per-condition ASR with attack-specific criteria, plus benign utility degradation for Capability Cloaking (pp. 7--8, Table 2).
- Unit: Benchmark case and SUT trial.
- Denominator: Appendix A, Table 5 reports 100 benign plus 100 each for AS, CO, HOTF, ASRF, and ATSI per domain, or 600 per domain and 1,800 total. CC is evaluated through benign-task degradation and has no separately reported task denominator.
- Result boundary: AS is 0.820/0.816/0.828 across domains and the other five Table 2 rows are 1.00. CC's ASR denominator is unstated; Tables 3--4 also omit trial denominators. ATSI's operational criterion establishes return of a canary-bearing artifact, not independently verified browser harm.

### Evidence and Boundaries

- Evidence locations: Abstract p. 1; threat model and Table 1 pp. 3--4; attack definitions pp. 5--6; adapter p. 6; system and metric p. 7; main results and Table 2 pp. 7--8; transfer and defense Tables 3--4 p. 9; task counts in Appendix A, Figure 5 and Table 5 p. 14.
- Author claim versus corpus interpretation: Attack taxonomy, system configuration, task counts, and reported results are author claims. SoK category, impact-stage, and counterfactual labels are corpus interpretations. The difference between ATSI's formal and operational criteria is a source-boundary observation.
- Limitations: Official demos and three domains; no CC trial denominator; no stated trial denominator for Tables 3--4; AgentCard candidate-count inconsistency between the formal text and prompts; ATSI operational labeling stops at artifact return; no DOI; not all A2A stacks or deployment policies are covered.

### Required Corrections

- **RESOLVED - Primary category:** Retain evaluation as primary, with benchmark and attack-suite roles.
- **RESOLVED - Evidence locators:** Use the published ICLR proceedings PDF and the exact page/table locations recorded above.
- **HIGH - Metric denominator:** Use Table 5's 1,800 enumerated cases; leave the Capability Cloaking and Tables 3--4 trial denominators explicitly unstated.
- **HIGH - ATSI result boundary:** Describe the operational result as return of a canary-bearing artifact, not verified browser execution or harm.
<!-- SOURCE_REVIEW_END -->
