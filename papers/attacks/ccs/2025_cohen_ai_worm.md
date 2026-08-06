# Here Comes the AI Worm: Preventing the Propagation of Adversarial Self-Replicating Prompts Within GenAI Ecosystems

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Stav Cohen, Ron Bitton, Ben Nassi
- Year: 2025
- Venue: ACM CCS 2025
- DOI: 10.1145/3719027.3765196
- Primary URL: https://doi.org/10.1145/3719027.3765196
- Open access URL: https://arxiv.org/abs/2403.02817
- BibTeX key: `cohen2025aiworm`

## Paper Type

Attack; Defense; Ecosystem evaluation

- Primary category: `attack`
- Scope relation: `security_relevant`

## Scope

### System Studied

GenAI-powered email assistants and retrieval-augmented applications that ingest
messages, generate content, and send outputs to other users or applications.

### Multi-Agent Dependency

The adversarial prompt self-replicates through application-to-application and
user-to-user communication, creating a zero-click propagation chain.

### Application Domain

Email assistants and RAG-enabled GenAI ecosystems.

## Security Model

- Protected assets: confidential data, application integrity, and ecosystem
  availability/containment.
- Threat actor: external sender of a malicious message or document.
- Trusted components: application workflow and downstream recipients before
  infection.
- Attacker capabilities: place a self-replicating adversarial prompt in ingested
  content.
- Security assumptions: applications automatically process and forward generated
  content.

## Main Contribution

The paper demonstrates a zero-click GenAI worm built from adversarial
self-replicating prompts and evaluates propagation, payload behavior, and
preventive measures in realistic application workflows.

## Attack or Failure

- Attack surface: inbound email/RAG content and automated outbound messages.
- Attack mechanism: self-replicating prompt injection.
- System-level failure: propagation, containment, and confidentiality failure.
- Security consequence: infection and data exfiltration across applications.

## Defense

- Defense mechanism: propagation-prevention measures evaluated in the paper.
- Intervention point: content processing and forwarding boundaries.
- Required observability: inbound/outbound generated content and workflow state.
- Assumptions: mitigations can inspect or constrain replication paths.
- Limitations: effectiveness is tied to evaluated application designs.

## Evaluation

- Evaluated systems: GenAI email assistants and RAG applications.
- Agent configuration: communicating applications/users connected through email.
- Dataset or environment: end-to-end proof-of-concept ecosystem.
- Baselines: benign and attack/defense configurations.
- Metrics: propagation and payload success.
- Main results: the paper reports zero-click propagation and end-to-end malicious
  effects.

## Relation to Existing Work

- Claimed research gap: conventional computer worms and isolated prompt injection
  do not capture self-replication through generative content.
- Closest related work: indirect prompt injection and worms.
- Difference from prior work: prompt output carries the next infection.

## Relevance to Our SoK

- Included concepts: zero-click spread, self-replication, RAG, email graph,
  exfiltration.
- Taxonomy implications: one attack instance can violate both containment and
  confidentiality.
- Supported research questions: cross-application propagation and defense
  placement.
- Important limitations: the system boundary includes interacting applications
  and users rather than only a conventional agent society.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack uses adversarial self-replicating prompts. | Explicit author claim | Paper | Abstract; threat model | PDF 1 onward | Not applicable | Canonical CCS title and paper describe self-replication. |
| The work demonstrates zero-click propagation in email/RAG applications. | Explicit author claim | Paper | Introduction; evaluation | PDF 1 onward | Not applicable | End-to-end scenarios in the paper. |
| The preprint and CCS paper are one canonical work. | Corpus interpretation | Publication records | Metadata | Not applicable | Not applicable | Title/authors and DOI version lineage match. |

## Provenance

- Discovery source: prior corpus; ACM DOI record
- Discovery query: exact-title and DOI verification
- Accessed version: published CCS 2025 metadata; arXiv 2403.02817 open copy
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after major patch

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: The CCS paper is the canonical version. The earlier arXiv version used the title 'Here Comes The AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications' and used earlier system names. Merge them as one work but preserve version-specific terminology and results.
- Recommended scope: `security_relevant`
- Multi-agent dependency: The work studies a network of GenAI email and RAG applications and users. It is highly relevant to propagation, but the system boundary is broader than a population of independently stateful LLM agent cores.
- Recommended roles: attack; defense; ecosystem evaluation
- Maturity: Archival peer-reviewed evidence, with a materially different earlier preprint.

### Threat and Failure Coding

- Attacker or fault actor: External sender who inserts a self-replicating prompt into an email or retrieved document.
- Capabilities: Places malicious content that automated applications ingest, reproduce, and forward.
- Preconditions: Applications automatically process inbound content and can emit generated content to downstream users or applications.
- Surfaces: Inbound email or RAG content; automated outbound messages; application-to-application workflow.
- Mechanism: Indirect prompt injection with self-replication through generated content.
- Primary system-level failure: F1 propagation and containment failure.
- Impact: Confidentiality loss and availability effects can be secondary payloads.

### Evaluation Contract

- Configuration: End-to-end GenAI email assistant and RAG application ecosystem.
- Topology: Application and user communication chains rather than a canonical LLM-agent society topology.
- Baseline or ablation: Benign, attack, and defense configurations in the final paper.
- Metric: Propagation behavior, payload success, and defense true-positive, false-positive, and latency measures.
- Unit: Application or client, propagation event, and detector decision.
- Denominator: Final-paper evaluation trials and clients. Do not import denominators from the preprint without checking the final paper.
- Result boundary: Use the final CCS values and names. The final paper reports super-linear propagation, a 20-new-client behavior within 1 to 3 days in its modeled scenario, and DonkeyRail TPR 1.0, FPR 0.017, and latency 7.6 to 38.3 ms. Do not mix these with preprint values or the earlier Morris-II and Virtual Donkey names.

### Evidence and Boundaries

- Evidence locations: Final ACM record and CCS paper; preprint retained only for lineage. Cite final tables for propagation and DonkeyRail values. The current note's abstract-only locators are insufficient for quantitative use.
- Author claim versus corpus interpretation: Zero-click self-replication and measured defense results are author claims. Classifying the ecosystem as security_relevant rather than strict core MAS is a corpus decision.
- Limitations: Laboratory ecosystem; broader GenAI applications rather than strict agent cores; result and terminology changed across versions; no evidence of prevalence in deployed ecosystems.

### Required Corrections

- **CRITICAL - Canonical version:** Replace preprint title and Morris-II terminology with the final CCS title and final names; retain the preprint only as a linked version.
- **CRITICAL - Metrics:** Use final-paper FPR 0.017 and final latency/result tables. Do not mix preprint FPR 0.015.
- **HIGH - Scope relation:** Downgrade from core_security to security_relevant under the independent LLM-agent-core boundary.
<!-- SOURCE_REVIEW_END -->
