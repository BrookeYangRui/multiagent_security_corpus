# MultiAgent Collaboration Attack: Investigating Adversarial Attacks in Large Language Model Collaborations via Debate

## Citation

- Authors: Alfonso Amayuelas, Xianjun Yang, Antonis Antoniades, Wenyue Hua, Liangming Pan, William Yang Wang
- Year: 2024
- Venue: Findings of EMNLP 2024
- DOI: 10.18653/v1/2024.findings-emnlp.407
- Primary URL: https://aclanthology.org/2024.findings-emnlp.407/
- Open access URL: https://aclanthology.org/2024.findings-emnlp.407.pdf
- BibTeX key: `amayuelas2024collaborationattack`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Multi-agent LLM collaborations that deliberate through multi-round debate and
aggregate a collective answer.

### Multi-Agent Dependency

The adversarial participant influences peers through debate messages; the target
is the collective decision rather than only the malicious agent's output.

### Application Domain

Collaborative reasoning and multi-agent debate.

## Security Model

- Protected assets: integrity of the collective answer.
- Threat actor: one malicious or adversarial debate participant.
- Trusted components: honest participants and the collaboration protocol.
- Attacker capabilities: contribute persuasive or adversarial messages within its
  assigned debate role.
- Security assumptions: participants consume and react to peer messages.

## Main Contribution

The paper studies how one adversarial agent can exploit model, knowledge, and
persuasion asymmetries to manipulate LLM collaborations conducted through
debate.

## Attack or Failure

- Attack surface: debate messages and collective aggregation.
- Attack mechanism: an adversarial participant supplies misleading arguments and
  exploits influence asymmetry.
- System-level failure: collective decision integrity failure.
- Security consequence: the collaboration converges to an incorrect answer.

## Defense

- Defense mechanism: Not reported as a primary contribution.
- Intervention point: Unclear.
- Required observability: Unclear.
- Assumptions: Not reported.
- Limitations: the evaluated debate protocols do not cover every coordination
  architecture.

## Evaluation

- Evaluated systems: multiple LLMs collaborating through debate.
- Agent configuration: honest agents plus an adversarial participant.
- Dataset or environment: reasoning/knowledge tasks defined in the paper.
- Baselines: benign collaboration and attack variants.
- Metrics: collective task accuracy and attack influence.
- Main results: the paper reports that collaboration can be manipulated by an
  adversarial participant across evaluated settings.

## Relation to Existing Work

- Claimed research gap: collaboration benefits had been studied more than
  adversarial participants within collaboration.
- Closest related work: multi-agent debate and adversarial persuasion.
- Difference from prior work: treats one collaborating member as the attacker.

## Relevance to Our SoK

- Included concepts: compromised member, persuasion, debate protocol, collective
  answer integrity.
- Taxonomy implications: persuasion is an attack mechanism; incorrect group
  output is the system-level property failure.
- Supported research questions: when collaboration amplifies a malicious
  minority.
- Important limitations: task-level incorrectness must not automatically be
  generalized to real-world security impact.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The paper evaluates adversarial agents in collaborative debate. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Fig. 1 | The official paper frames malicious participants in debate. |
| Agents may exploit model size, knowledge, or persuasion advantages. | Explicit author claim | Paper | Introduction; attack setup | PDF 1-3 | Fig. 1 | The paper enumerates collaboration asymmetries. |
| The protected property is collective answer integrity. | Corpus interpretation | Paper | Task and metrics | PDF 3 onward | Not applicable | Derived from manipulation of the final collaborative answer. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: exact-title search on ACL Anthology
- Accessed version: published Findings of EMNLP 2024 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

