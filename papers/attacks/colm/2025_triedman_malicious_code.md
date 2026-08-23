# Multi-Agent Systems Execute Arbitrary Malicious Code

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `COLM` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Harold Triedman, Rishi Dev Jha, Vitaly Shmatikov
- Year: 2025
- Venue: COLM 2025
- DOI: Not reported
- Primary URL: https://openreview.net/forum?id=DAozI4etUp
- Open access URL: https://openreview.net/pdf?id=DAozI4etUp
- BibTeX key: `triedman2025maliciouscode`

## Paper Type

Attack; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Deployed and research multi-agent frameworks that route tasks and messages among
specialized LLM agents.

### Multi-Agent Dependency

The attack hijacks control flow and inter-agent communication to invoke an
otherwise unreachable unsafe agent or functionality.

### Application Domain

General-purpose orchestration, web interaction, and code-capable agent workflows.

## Security Model

- Protected assets: control-flow integrity, tool authorization, and host-system
  integrity.
- Threat actor: an external party controlling untrusted web or document content.
- Trusted components: framework orchestration and nominally safe routing logic.
- Attacker capabilities: place indirect prompt injection in content processed by
  one agent.
- Security assumptions: agents and orchestrators use LLM-generated text to make
  routing or invocation decisions.

## Main Contribution

The paper formalizes and demonstrates control-flow hijacking attacks that use
untrusted content to redirect multi-agent execution toward unsafe agents and
functions, including arbitrary malicious code execution.

## Attack or Failure

- Attack surface: untrusted content, inter-agent messages, and orchestrator
  routing.
- Attack mechanism: indirect prompt injection changes control and communication
  flow.
- System-level failure: compositional authority and action-integrity failure.
- Security consequence: unauthorized invocation and arbitrary code execution.

## Defense

- Defense mechanism: framework-level mitigations are analyzed in the paper.
- Intervention point: routing, communication, and tool invocation boundaries.
- Required observability: system control flow and invoked functionality.
- Assumptions: defenses must mediate LLM-decided routing and execution.
- Limitations: protection is framework-dependent and does not follow from
  content filtering alone.

## Evaluation

- Evaluated systems: several deployed or proposed LLM multi-agent frameworks.
- Agent configuration: orchestrated specialist agents, including code-capable
  functions.
- Dataset or environment: malicious web and other untrusted-content scenarios.
- Baselines: direct and indirect prompt-injection attacks.
- Metrics: attack success and successful unsafe/code invocation.
- Main results: the authors report arbitrary-code attack success across evaluated
  systems, with rates depending on framework and model.

## Relation to Existing Work

- Claimed research gap: indirect prompt-injection work did not capture
  multi-agent control-flow and communication hijacking.
- Closest related work: indirect prompt injection and tool-using agent attacks.
- Difference from prior work: system routing composes local agent capabilities
  into an unauthorized global action.

## Relevance to Our SoK

- Included concepts: orchestration, control-flow hijacking, distributed
  authority, unsafe tool invocation.
- Taxonomy implications: separates initial prompt injection from the resulting
  compositional authorization failure.
- Supported research questions: how local content compromise crosses agent and
  tool trust boundaries.
- Important limitations: exact exploitability depends on framework architecture
  and enabled functions.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Adversarial content can hijack control and communication to invoke unsafe agents and functions. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Not applicable | Stated in the official COLM record and paper. |
| The paper compares against direct and indirect prompt injection. | Explicit author claim | Paper | Abstract; evaluation | PDF 1; experiments | Not applicable | The official record describes the comparison. |
| Arbitrary code execution is a compositional authority failure. | Corpus interpretation | Paper | Attack design | PDF 2 onward | Not applicable | Classification follows cross-agent routing to unsafe functionality. |

## Provenance

- Discovery source: prior corpus; COLM OpenReview record
- Discovery query: exact-title search
- Accessed version: published COLM 2025 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Published COLM 2025 record and arXiv version lineage confirmed. Use the conference record as canonical.
- Recommended scope: `core_security`
- Multi-agent dependency: Untrusted content hijacks multi-agent control flow and routing to invoke otherwise unreachable unsafe agents or functions.
- Recommended roles: attack; evaluation
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: External adversary controlling web, file, email, audio, or other untrusted content.
- Capabilities: Places indirect prompt injection that changes LLM-mediated routing or invocation decisions.
- Preconditions: Framework orchestrators use generated text or metadata to route among specialist agents and code-capable functions.
- Surfaces: Untrusted content; inter-agent messages; orchestration metadata; routing; tool invocation.
- Mechanism: Indirect prompt injection plus confused-deputy or control-flow laundering.
- Primary system-level failure: F6 delegation, authority, and control-flow integrity failure.
- Impact: Unauthorized invocation, data exfiltration, or arbitrary code execution.

### Evaluation Contract

- Configuration: AutoGen, CrewAI, MetaGPT, and selected models and orchestrators in lab or container settings.
- Topology: Framework-specific orchestrated specialist-agent workflows.
- Baseline or ablation: Direct and indirect prompt-injection baselines and framework-level mitigations.
- Metric: Trial-level attack success and successful unsafe or code invocation.
- Unit: Attack trial and framework/model configuration.
- Denominator: Trials for each framework, model, and attack scenario.
- Result boundary: Setting-specific successes include high rates across several orchestrators and models. Every numeric claim must be copied from its exact table rather than summarized as universal arbitrary-code reliability.

### Evidence and Boundaries

- Evidence locations: Abstract and Introduction, PDF pp. 1 to 2; attack design and system diagrams, PDF p. 2 onward; framework/model result tables; mitigation analysis.
- Author claim versus corpus interpretation: Control-flow hijacking and measured unsafe invocations are author claims. Classifying the system consequence as F6 authority integrity is a corpus interpretation.
- Limitations: Three principal frameworks; selected models and orchestrators; enabled unsafe functions; laboratory or container deployment; exploitability depends strongly on routing architecture.

### Required Corrections

- **HIGH - Result evidence:** Attach each success rate to the exact framework/model table; avoid a single generalized rate.
- **MEDIUM - Failure versus impact:** Use authority/control-flow integrity as the failure and RCE or exfiltration as impact.
<!-- SOURCE_REVIEW_END -->
