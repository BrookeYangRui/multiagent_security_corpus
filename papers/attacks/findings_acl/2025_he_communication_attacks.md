# Red-Teaming LLM Multi-Agent Systems via Communication Attacks

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `Findings of ACL` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Pengfei He, Yuping Lin, Shen Dong, Han Xu, Yue Xing, Hui Liu
- Year: 2025
- Venue: Findings of ACL 2025
- DOI: 10.18653/v1/2025.findings-acl.349
- Primary URL: https://aclanthology.org/2025.findings-acl.349/
- Open access URL: https://aclanthology.org/2025.findings-acl.349.pdf
- BibTeX key: `he2025communicationattacks`

## Paper Type

Attack; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Message-based LLM multi-agent systems across multiple frameworks, communication
structures, and application tasks.

### Multi-Agent Dependency

The adversary compromises system behavior by intercepting and rewriting messages
between agents while leaving individual agent models uncompromised.

### Application Domain

General-purpose collaboration and real-world multi-agent applications.

## Security Model

- Protected assets: message integrity and collective task integrity.
- Threat actor: agent-in-the-middle adversary on communication links.
- Trusted components: endpoint agents and their local models.
- Attacker capabilities: intercept and manipulate inter-agent messages under
  limited control and role-restricted formats.
- Security assumptions: the attacker can access selected communication paths.

## Main Contribution

The paper introduces Agent-in-the-Middle, an LLM-powered adversarial agent with
reflection that generates context-aware malicious message modifications against
multi-agent systems.

## Attack or Failure

- Attack surface: inter-agent communication links.
- Attack mechanism: interception and adaptive rewriting of protocol-valid
  messages.
- System-level failure: message and collective decision integrity failure.
- Security consequence: system-wide task compromise without endpoint-agent
  compromise.

## Defense

- Defense mechanism: Not reported as the primary contribution.
- Intervention point: Not reported.
- Required observability: Not reported.
- Assumptions: Not reported.
- Limitations: attack feasibility depends on access to communication paths and
  allowed message formats.

## Evaluation

- Evaluated systems: multiple LLM-MAS frameworks.
- Agent configuration: varied communication structures and role formats.
- Dataset or environment: multiple real-world application tasks.
- Baselines: communication-attack variants described in the paper.
- Metrics: task compromise and attack success.
- Main results: the authors report vulnerability across evaluated frameworks,
  communication structures, and applications.

## Relation to Existing Work

- Claimed research gap: prior attacks compromise agents or inputs but do not
  isolate communication as the attack surface.
- Closest related work: man-in-the-middle attacks, indirect prompt injection, and
  malicious-member attacks.
- Difference from prior work: manipulates only messages in transit.

## Relevance to Our SoK

- Included concepts: communication integrity, message interception, protocol
  validity, adaptive attacker.
- Taxonomy implications: separates attacker position from attack mechanism and
  violated property.
- Supported research questions: whether endpoint-local defenses protect message
  paths.
- Important limitations: no universal claim follows for systems with authenticated
  or integrity-protected channels.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| AiTM attacks a system by manipulating messages rather than compromising agents. | Explicit author claim | Paper | Abstract; threat model | PDF 1-3 | Fig. 1 | Stated in the official abstract. |
| The adversarial agent uses reflection to generate context-aware malicious instructions. | Explicit author claim | Paper | Abstract; method | PDF 1; method section | Not applicable | Stated in the official abstract. |
| The evaluation covers multiple frameworks, structures, and applications. | Explicit author claim | Paper | Abstract; experiments | PDF 1; evaluation section | Not applicable | Stated in the official abstract. |
| Authenticated/integrity-protected channels may change feasibility. | Corpus interpretation | Paper | Threat model | PDF 2 onward | Not applicable | Scope caveat; not an evaluated guarantee. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: `site:aclanthology.org multi-agent LLM attack security`
- Accessed version: published Findings of ACL 2025 version
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

- Identity: Canonical Findings of ACL 2025 version confirmed. Metadata is correct.
- Recommended scope: `core_security`
- Multi-agent dependency: The attack changes only messages between agents while leaving endpoint models uncompromised.
- Recommended roles: attack; evaluation
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: Agent-in-the-middle adversary on selected communication links.
- Capabilities: Intercepts and adaptively rewrites protocol-valid messages under role and format constraints.
- Preconditions: Access to selected message paths; endpoints trust messages without authenticated integrity protection.
- Surfaces: Inter-agent communication links; protocol-valid message content.
- Mechanism: Context-aware message interception and adaptive rewriting using reflection.
- Primary system-level failure: F3 communication integrity failure.
- Impact: F4 collective task or decision integrity failure as a downstream consequence.

### Evaluation Contract

- Configuration: Multiple MAS frameworks, communication structures, roles, and application tasks.
- Topology: Chain, tree, complete, random, and framework-specific structures in evaluation.
- Baseline or ablation: Communication-attack variants and direct or prior adversarial strategies.
- Metric: Whole-dataset ASR for targeted behavior or denial-of-service outcomes.
- Unit: Task instance.
- Denominator: All evaluated dataset instances for a setting.
- Result boundary: The paper demonstrates cross-framework and cross-structure vulnerability in its evaluated tasks. Feasibility does not automatically transfer to authenticated or integrity-protected channels.

### Evidence and Boundaries

- Evidence locations: Abstract and threat model, PDF pp. 1 to 3 and Fig. 1; metric definition in Sec. 4.1, approximately PDF p. 5; evaluation tables for framework, structure, and application results; limitations section.
- Author claim versus corpus interpretation: AiTM construction, ASR, and evaluated results are author claims. The authenticated-channel caveat and F3/F4 mapping are corpus interpretations.
- Limitations: Black-box model access; selected frameworks and tasks; public subset of SoftwareDev; assumed message-path access; no universal claim for integrity-protected protocols.

### Required Corrections

- **HIGH - Metric denominator:** Record ASR as whole-dataset task-level success with separate targeted and denial-of-service predicates.
- **MEDIUM - Failure versus impact:** Use message integrity as primary and collective task corruption as downstream impact.
- **MEDIUM - Assumption:** Explicitly record lack of authenticated or integrity-protected channels.
<!-- SOURCE_REVIEW_END -->
