# OMNI-LEAK: Orchestrator Multi-Agent Network Induced Data Leakage

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `survey` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Akshat Naik, Jay Culligan, Yarin Gal, Philip Torr, Rahaf Aljundi, Alasdair Paren, Adel Bibi
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2602.13477
- Primary URL: https://arxiv.org/abs/2602.13477
- Open access URL: https://arxiv.org/pdf/2602.13477
- BibTeX key: `naik2026omnileak`

## Paper Type

Attack; Benchmark; Evaluation; Empirical study

Primary category: attack

Scope relation: core_security

## Scope

### System Studied

An orchestrator delegates work to a data-processing agent and a notification
agent with different tools and access rights.

### Multi-Agent Dependency

One indirect injection must compromise a data agent, influence the orchestrator,
and cause a separate notification agent to exfiltrate the retrieved data. No
single downstream agent holds the complete authority chain.

### Application Domain

Enterprise data processing and notification workflows.

## Security Model

- Protected assets: private database records and authorization boundaries.
- Threat actor: external party able to place content in public data.
- Trusted components: access control and uncompromised system prompts.
- Attacker capabilities: indirect prompt injection without insider knowledge.
- Security assumptions: a privileged user's later query retrieves poisoned data.

## Main Contribution

OMNI-LEAK demonstrates cross-agent data exfiltration despite per-agent access
control in an orchestrator architecture. The paper also supplies a benchmark
covering attacks, models, database sizes, and agent configurations.

## Attack or Failure

- Attack surface: public data consumed by a privileged downstream agent.
- Attack mechanism: indirect injection followed by delegated exfiltration.
- System-level failure: cross-principal confidentiality failure.
- Security consequence: sensitive records reach an attacker-controlled email.

## Defense

Access control is present as an engineering safeguard but is bypassed by the
composed authority chain; no complete defense is introduced.

## Evaluation

- Evaluated systems: orchestrator systems using five frontier model families.
- Agent configuration: orchestrator, SQL agent, and notification agent, with
  additional configurations in the appendices.
- Dataset or environment: synthetic employee databases and email API.
- Baselines: direct and indirect attack variants.
- Metrics: exact-match end-to-end attack success and benign task correctness.
- Main results: most evaluated model families are vulnerable to at least one
  tested attack category.

## Relevance to Our SoK

- Included concepts: authority composition, indirect injection, confidentiality.
- Taxonomy implications: per-agent access control does not imply end-to-end
  noninterference when delegation composes privileges.
- Important limitations: preprint, synthetic environment, and strict exact-match
  success criterion.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack compromises several agents from one indirect injection. | Explicit author claim | Paper | Abstract; Sec. 4.1 | 1, 3-4 | Fig. 2-3 | The described chain crosses SQL agent, orchestrator, and notification agent. |
| The setup enforces access separation between downstream agents. | Explicit author claim | Paper | Sec. 4 | 3 | Fig. 2 | Each downstream agent has distinct prompts and tools. |
| Success requires sensitive data to reach the specified attacker email. | Explicit author claim | Paper | Sec. 4.2 | 4 | Fig. 4 | Partial exfiltration or wrong-recipient delivery is marked unsuccessful. |
| Five frontier models are evaluated. | Explicit author claim | Paper | Sec. 5 | 4-7 | Tables 1-5 | Experiments vary models, attacks, queries, and databases. |

## Provenance

- Discovery source: systematic screening ledger; arXiv API
- Discovery query: cross-agent leakage orchestrator multi-agent
- Accessed version: arXiv v2
- Access date: 2026-08-06
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-06
