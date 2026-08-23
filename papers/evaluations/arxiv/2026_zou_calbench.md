# CalBench: Evaluating Coordination-Privacy Trade-offs in Multi-Agent LLMs

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `evaluation` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

Title: CalBench: Evaluating Coordination-Privacy Trade-offs in Multi-Agent LLMs

Authors: Chelsea Zou; Yiheng Yao; Selena She; Noah D. Goodman; Robert D. Hawkins

Year: 2026

Venue: arXiv

Version: arXiv v3, last revised 5 June 2026

DOI: 10.48550/arXiv.2605.09823

Primary URL: https://arxiv.org/pdf/2605.09823

Open access URL: https://arxiv.org/pdf/2605.09823

BibTeX key: zou2026calbench

## Paper Type

Benchmark; Evaluation; Empirical study

## Scope

### System Studied
Five assistants with private calendars coordinate five sequential incoming meetings. The canonical main suite contains 90 tasks (45 uniform-cost and 45 varied-cost), 16 calendar slots, and three rotating participants per meeting.

### Multi-Agent Dependency
No assistant can inspect another participant's full calendar or impose a global solution. Participants must selectively disclose local state and independently commit compatible scheduling actions.

### Application Domain
Calendar scheduling and delegated personal assistance.

## Security Model

### Protected Assets
Private availability and preferences, meeting feasibility, cost, and fair burden allocation.

### Threat Actor
No malicious actor is required; privacy and coordination failures are measured under ordinary delegation.

### Trusted Components
CP-SAT oracle, task generator, scaffolding-enforced private-state visibility, transactional action validator, and trace/measurement pipelines.

### Attacker Capabilities
Not applicable; information disclosure is evaluated as a system property.

### Security Assumptions
Private calendars remain inaccessible except through communication; the full-information CP-SAT evaluator, private labels, and truth-direction calibration are correct. Reflection-calibrated VPS also assumes that measurement-only self-reports are meaningful lower-bound evidence of belief movement.

## Main Contribution

CalBench generates solvable scheduling scenarios with CP-SAT oracle solutions and four decentralized non-LLM reference protocols. It evaluates task success, excess cost, communication efficiency, burden fairness, and privacy leakage across seven model families. The reference protocols operate under the task's private-information constraints; the global CP-SAT oracle instead uses full information to define optimal cost.

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
Reference protocols and policy-level privacy/coordination operating points; no universal defense. The reported main experiment is not a matched communication-architecture comparison.

### Intervention Point
Communication channel and commitment protocol.

### Required Observability
Private state for oracle evaluation; messages for leakage and efficiency.

### Assumptions
Oracle schedules and privacy labels correctly characterize the task.

### Limitations
Calendar scheduling is a controlled proxy for broader delegated agency. The main results cover one topology, and the privacy estimators used for LLM agents and typed protocols are not directly interchangeable.

## Evaluation

### Evaluated Systems
Seven model families plus IMAP, SD-MAP, DSM-welfare, and DSM-private reference protocols.

### Agent Configuration
The harness supports private DMs, meeting-participant groupchat, and all-agent groupchat. Appendix B states that the cooperative runs reported in the main table use private agent-to-agent DMs; the other channels are harness-supported rather than reported matched architecture conditions.

### Dataset or Environment
The canonical main suite has `N=5` agents, `M=5` sequential meetings, 16 slots, and three rotating participants per meeting across 90 tasks: 45 uniform-cost and 45 varied-cost tasks. Table 1 evaluates model seats over calibration slices; it does not redefine `N` as the task's agent population.

### Baselines
The full-information global CP-SAT oracle defines feasible and minimum-cost schedules. Four decentralized non-LLM protocols provide policy reference points under the same private-information task constraints. Table 2 reports each protocol over 45 tasks per cost setting and explicitly warns that its protocol-semantic VPS is not directly comparable with the reflection-calibrated VPS used for LLM agents.

### Metrics
Task success is the per-agent-game fraction of participant meetings scheduled consistently, averaged across games. Scheduled excess cost is positive realized displacement cost above the oracle for the successfully scheduled subset. Communication is messages per successful participant-meeting. Fairness is the absolute deviation of an agent's signed excess burden from the within-game mean. Privacy is reported in calibrated slot-equivalent VPS, with semantic-context leakage audited separately.

### Units, Denominators, and Aggregation
Table 1's `N=135` for Claude Sonnet 4.6, Gemini 3.1 Pro, Gemini 3 Flash, and GPT-5.4 Mini, and `N=45` for Llama 4 Maverick, Qwen 3.6 Plus, and DeepSeek V4 Pro, are evaluated agent-game seats per cost setting. They are not numbers of agents or tasks. `Meetings` is the mean number of successfully scheduled meetings per agent-game, with a maximum of three because each agent participates in three of the five meetings. Metrics are grouped by model and cost setting and aggregated over the games in which that model appears. Table 2 uses 45 tasks per cost setting, not Table 1's seat denominator.

### Main Results
Completion alone misses avoidable cost, and raw communication volume is a weak proxy for lower regret. The authors also report that low VPS can coincide with unfair burden allocation when agents omit cost-relevant context. This privacy-fairness interpretation combines model-level results with a targeted message audit and should not be presented as a universal causal effect.

## Provisional Measurement Coding

This coding is a SoK interpretation of arXiv v3 and remains pending named human signoff.

### Primary and Secondary Categories
Primary: `privacy_information_flow`. Secondary: `collective_decision_deception`, using that label for collective scheduling decisions rather than for a demonstrated deception attack.

### Impact Stage
`S3_executed_or_persistent`. Agents submit atomic `SCHEDULE` and `RESCHEDULE` batches that are validated and applied to mutable calendars; resulting commitments and consistency failures carry into later rounds. The paper therefore supports an executed, persistent environment effect in addition to message and trace measurements.

### Interaction Counterfactual
`component_or_attack_controls`. The study compares models, cost settings, and protocol policies, including matched DSM privacy/welfare parameterizations, but it does not remove an interaction edge or report a matched single-agent, topology, or communication-architecture ablation. Section 5 explicitly limits the reported results to one topology.

### Artifact Availability
`code_and_data`. The paper links a runnable harness and trace/leaderboard resources; the linked release contains task fixtures, tests, analysis scripts, and aggregate result data. The release repository notes that raw model traces are not committed there, so this code records availability rather than independent reproduction.

## Relation to Existing Work

### Papers Compared by the Authors
Agentic benchmarks, negotiation, and distributed constraint-optimization benchmarks.

### Claimed Research Gap
Existing benchmarks often centralize private state or omit privacy-utility trade-offs.

### Closest Related Work
Multi-agent scheduling and negotiation evaluations.

### Difference From Prior Work
CalBench evaluates decentralized coordination under private-information constraints while using a separate full-information oracle to define feasibility and optimal cost.

## Relevance to Our SoK

### Included Concepts
Private memory, delegation, information flow, fairness, and denominator contracts.

### Taxonomy Implications
Privacy and utility must be measured jointly at group level.

### Supported Research Questions
How much information must agents reveal to coordinate efficiently and fairly?

### Important Limitations
The work is a preprint and a controlled calendar proxy. Headline results use one five-agent topology and rely on reflection-calibrated VPS, which the authors interpret as a lower bound; the post-hoc judge audit finds only weak-to-moderate agreement with self-reflection. The main cohort is cooperative, while a separate earlier homogeneous-team trace audit includes a probe condition and must not be merged with the headline denominators.

The source is internally inconsistent about main-table team composition. Section 4.1, Table 1, Table 7, and Appendix G describe a mixed-agent cohort and calibration/entrant slices, whereas Appendix B says the cooperative main-table runs use homogeneous same-model teams. Table-level seat denominators are explicit and usable, but team homogeneity should remain unresolved unless the authors clarify it.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The title block lists five authors and the PDF is arXiv v3. | Explicit source metadata | Paper | Title page | 1 | - | Five-author canonical identity; v3 dated 5 June 2026. |
| The main suite uses five agents, five sequential meetings, 16 slots, three participants per meeting, and 45 uniform plus 45 varied tasks. | Explicit author claim | Paper | 4.1 | 5 | - | Canonical task configuration and task denominator. |
| Table 1's `N=135/45` counts evaluated agent-game seats per cost setting, and `Meetings` has maximum three per agent-game. | Explicit author claim | Paper | 4.1; 4.2 | 5-6 | Table 1 | Seat and meeting denominators. |
| The harness supports three message types, but Appendix B says the cooperative main-table runs use private DMs. | Explicit author claim | Paper | 3; Appendix A.4; Appendix B | 4; 13-14 | Figure 1 | Supported channels are not a reported matched architecture comparison. |
| Valid atomic schedule/reschedule actions are applied to calendar state and consistency is checked across rounds. | Explicit author claim | Paper | 3; Appendix A.5-A.6 | 4; 13-14 | Table 5 | Supports provisional `S3_executed_or_persistent` coding. |
| The study compares policy/reference controls but reports only one topology. | Explicit author claim plus corpus coding | Paper | 3.1; 5; Appendix D | 4-5; 8; 14-18 | Table 2; Tables 8-9 | Supports `component_or_attack_controls`, not `matched_architecture`. |
| Metrics include success, scheduled and adjusted excess cost, messages per successful participant-meeting, fairness, and calibrated VPS. | Explicit author claim | Paper | 3.2; 4.2; Appendix F | 5-7; 19-20 | Table 1; Table 10 | Metric definitions, units, aggregation, and estimator distinction. |
| Code, task/result data, and trace/leaderboard resources are linked. | Explicit author claim and linked artifact | Paper; artifact | Abstract; Conclusion | 1; 8 | - | Supports availability coding, not a reproduction claim. |
| Main-cohort mixed-team wording conflicts with Appendix B's homogeneous-team wording. | Source inconsistency | Paper | 4.1; Appendix B; Appendix G | 5; 14; 21-22 | Tables 1 and 7 | Team composition requires author clarification; explicit seat denominators remain usable. |

## Provenance

### Discovery Source
arXiv; multi-agent privacy and coordination benchmark search.

### Discovery Query
multi-agent LLM coordination privacy benchmark calendar

### Accessed Version
arXiv v3, last revised 5 June 2026.

### Source SHA-256
`98153bb0268d56140b2c942fb56a9649b0c5dc35a839a328c9ff24d2c9f9f6eb`

### Access Date
2026-08-10

### Prepared By
Human or automated process: automated primary-source audit

Model and version, if automatically generated: OpenAI Codex; exact serving version not recorded in the repository

### Verification Status
assistant_source_reviewed_pending_named_human_signoff

### Last Updated
2026-08-10
