# Red-Teaming LLM Multi-Agent Systems via Communication Attacks

## Citation

- Authors: Pengfei He, Yuping Lin, Shen Dong, Han Xu, Yue Xing, Hui Liu
- Year: 2025
- Venue: Findings of ACL 2025
- DOI: 10.18653/v1/2025.findings-acl.349
- Primary URL: https://aclanthology.org/2025.findings-acl.349/
- Open access URL: https://aclanthology.org/2025.findings-acl.349.pdf
- BibTeX key: `he2025communicationattacks`

## Paper Type

Attack; Evaluation; Empirical study

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

