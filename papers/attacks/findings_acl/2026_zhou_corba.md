# CORBA: Contagious Recursive Blocking Attacks on Multi-Agent Systems Based on Large Language Models

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Zhenhong Zhou, Zherui Li, Jie Zhang, Yuanhe Zhang, Kun Wang, Yang Liu, Qing Guo
- Year: 2026
- Venue: Findings of ACL 2026
- DOI: 10.18653/v1/2026.findings-acl.342
- Primary URL: https://aclanthology.org/2026.findings-acl.342/
- Open access URL: https://aclanthology.org/2026.findings-acl.342.pdf
- BibTeX key: `zhou2026corba`

## Paper Type

Attack; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

LLM multi-agent systems with open-ended collaboration over varied communication
topologies.

### Multi-Agent Dependency

Recursive instructions force agents to trigger further messages, transforming
the collaboration graph into a resource-consuming cycle.

### Application Domain

General-purpose collaborative LLM systems.

## Security Model

- Protected assets: availability, bounded cost, and useful collaboration.
- Threat actor: source of a semantically benign recursive instruction.
- Trusted components: conventional model safety alignment.
- Attacker capabilities: introduce content that agents accept and recursively
  propagate.
- Security assumptions: agents can initiate messages or tasks for peers.

## Main Contribution

The paper formalizes Denial-of-Collaboration and introduces CORBA, a contagious
recursive blocking attack that induces meaningless communication cycles and
system paralysis.

## Attack or Failure

- Attack surface: open-ended inter-agent communication.
- Attack mechanism: benign-looking recursively contagious instructions.
- System-level failure: availability and resource-isolation failure.
- Security consequence: excessive resource use and system paralysis.

## Defense

- Defense mechanism: conventional safety alignment is evaluated, not introduced.
- Intervention point: content-level agent guardrails.
- Required observability: local semantic content in tested safeguards.
- Assumptions: semantically benign content is allowed.
- Limitations: baseline safeguards are not collaboration-aware.

## Evaluation

- Evaluated systems: multiple LLMs and communication topologies.
- Agent configuration: interacting agents capable of recursive communication.
- Dataset or environment: DoC attack tasks defined in the paper.
- Baselines: existing attacks and conventional safety alignment.
- Metrics: resource use, blocking, and paralysis outcomes.
- Main results: CORBA produces system paralysis in settings where baselines fail.

## Relation to Existing Work

- Claimed research gap: DoS targets nodes/services, while collaboration itself can
  be corrupted into self-sabotage.
- Closest related work: denial of service, prompt infection, and recursive agents.
- Difference from prior work: the attack payload can remain semantically benign.

## Relevance to Our SoK

- Included concepts: denial of collaboration, recursive delegation, contagious
  instructions, resource exhaustion.
- Taxonomy implications: availability is the violated property; recursion and
  contagion are mechanisms.
- Supported research questions: why content guardrails fail on systemic behavior.
- Important limitations: resource denominators differ from harmful-output ASR.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| DoC corrupts collaboration into self-sabotage and system paralysis. | Explicit author claim | Paper | Abstract; threat model | PDF 1 onward | Not applicable | Official abstract defines DoC. |
| CORBA uses benign recursively contagious instructions. | Explicit author claim | Paper | Abstract; method | PDF 1 onward | Not applicable | Official abstract describes the mechanism. |
| Conventional safety alignment is bypassed because content is semantically benign. | Explicit author claim | Paper | Abstract; experiments | PDF 1; evaluation | Not applicable | Reported in official abstract. |

## Provenance

- Discovery source: ACL Anthology; prior systematic search
- Discovery query: exact-title search
- Accessed version: published Findings of ACL 2026 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical Findings of ACL 2026 version confirmed. Metadata is correct.
- Recommended scope: `core_security`
- Multi-agent dependency: Recursive communication among agents is the mechanism that turns semantically benign instructions into system-level blocking and paralysis.
- Recommended roles: attack; evaluation
- Maturity: Archival peer-reviewed primary attack evidence.

### Threat and Failure Coding

- Attacker or fault actor: Source of a semantically benign recursive instruction.
- Capabilities: Introduces content that agents accept and recursively pass or act upon.
- Preconditions: Agents can initiate further messages or tasks for peers and lack a global collaboration budget.
- Surfaces: Inter-agent communication; delegation or invocation; topology; resource plane.
- Mechanism: Recursive contagious instructions create cycles of meaningless collaboration.
- Primary system-level failure: F7 availability and resource boundedness failure.
- Impact: System paralysis and loss of useful collaboration. Contagion is a mechanism, not the primary failure label.

### Evaluation Contract

- Configuration: Multiple LLMs and communication topologies with interacting agents.
- Topology: Multiple static topologies, including random entry and repeated runs.
- Baseline or ablation: Existing attacks and conventional content-level safety alignment.
- Metric: P-ASR and peak-blocking-turn style measures.
- Unit: Agent and interaction turn.
- Denominator: P-ASR equals blocked agents divided by total agents in the network.
- Result boundary: CORBA produces denial of collaboration in evaluated settings and bypasses content guardrails because the recursive text can be semantically benign.

### Evidence and Boundaries

- Evidence locations: Abstract and threat model, PDF p. 1 onward; metric definition and experiment tables, including topology results and repeated-run description; defense comparison section.
- Author claim versus corpus interpretation: DoC, CORBA, and P-ASR are author claims. Coding recursion as a mechanism and F7 as the primary property is a corpus interpretation.
- Limitations: Small or static topologies; blocked-agent fraction and turns are proxies rather than monetary or token cost; no full recovery or post-incident cleanup evaluation.

### Required Corrections

- **HIGH - Primary failure:** Use availability/resource boundedness, not behavioral infection, as the primary failure.
- **HIGH - Metric denominator:** Record P-ASR explicitly as blocked agents over network population.
- **MEDIUM - Cross-paper comparison:** Do not compare P-ASR directly with harmful-output ASR.
<!-- SOURCE_REVIEW_END -->
