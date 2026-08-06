# Here Comes the AI Worm: Preventing the Propagation of Adversarial Self-Replicating Prompts Within GenAI Ecosystems

## Citation

- Authors: Stav Cohen, Ron Bitton, Ben Nassi
- Year: 2025
- Venue: ACM CCS 2025
- DOI: 10.1145/3719027.3765196
- Primary URL: https://doi.org/10.1145/3719027.3765196
- Open access URL: https://arxiv.org/abs/2403.02817
- BibTeX key: `cohen2025aiworm`

## Paper Type

Attack; Defense; Evaluation; Empirical study

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

