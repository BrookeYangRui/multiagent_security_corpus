# Flooding Spread of Manipulated Knowledge in LLM-Based Multi-Agent Communities

## Citation

- Authors: Tianjie Ju, Yiting Wang, Xinbei Ma, Pengzhou Cheng, Haodong Zhao, Yulong Wang, Lifeng Liu, Jian Xie, Zhuosheng Zhang, Gongshen Liu
- Year: 2026
- Venue: Science China Information Sciences
- DOI: 10.1007/s11432-024-4663-2
- Primary URL: https://doi.org/10.1007/s11432-024-4663-2
- Open access URL: https://arxiv.org/abs/2407.07791
- BibTeX key: `ju2026flooding`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

LLM-based agent communities with chat histories, communication, and optional RAG
storage/retrieval.

### Multi-Agent Dependency

Manipulated knowledge spreads when affected agents persuade peers and persist
the resulting chat histories for later retrieval.

### Application Domain

General-purpose social and collaborative agent communities.

## Security Model

- Protected assets: shared knowledge integrity and long-term memory integrity.
- Threat actor: attacker introducing manipulated knowledge through one agent.
- Trusted components: benign agents and the trusted deployment platform.
- Attacker capabilities: persuasiveness and manipulated-knowledge injection.
- Security assumptions: agents rely on peer messages and stored chat histories.

## Main Contribution

The paper presents a two-stage attack using Persuasiveness Injection and
Manipulated Knowledge Injection, then studies spread of counterfactual/toxic
knowledge and persistence through RAG.

## Attack or Failure

- Attack surface: messages, chat history, and RAG memory.
- Attack mechanism: persuasive fabricated evidence induces unconscious forwarding.
- System-level failure: knowledge-integrity and containment failure.
- Security consequence: persistent manipulated beliefs among benign agents.

## Defense

- Defense mechanism: guardian agents and fact checking are discussed.
- Intervention point: messages and shared/retrieved knowledge.
- Required observability: claims, provenance, and stored histories.
- Assumptions: verification tools can assess manipulated claims.
- Limitations: discussed defenses are not the primary evaluated contribution.

## Evaluation

- Evaluated systems: simulated LLM agent communities and RAG persistence setting.
- Agent configuration: attacker/affected agents and benign peers.
- Dataset or environment: counterfactual and toxic knowledge scenarios.
- Baselines: attack variants described in the paper.
- Metrics: spread and persistence of manipulated knowledge.
- Main results: manipulated knowledge spreads without degrading foundational
  capabilities and can persist in retrieved histories.

## Relation to Existing Work

- Claimed research gap: security implications of manipulated knowledge spread in
  LLM-based MAS were underexplored.
- Closest related work: misinformation propagation, RAG poisoning, and persuasion.
- Difference from prior work: combines interaction spread with post-interaction
  memory persistence.

## Relevance to Our SoK

- Included concepts: persuasion, knowledge integrity, persistence, RAG memory.
- Taxonomy implications: separates persuasive mechanism from integrity failure.
- Supported research questions: how communication and memory jointly sustain an
  attack.
- Important limitations: simulation results do not establish prevalence.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attack has Persuasiveness and Manipulated Knowledge Injection stages. | Explicit author claim | Paper | Abstract; method | PDF 1 onward | Not applicable | Stated in the abstract. |
| Counterfactual and toxic knowledge spread without explicit prompt manipulation. | Explicit author claim | Paper | Abstract; experiments | PDF 1; results | Not applicable | Reported by authors. |
| Manipulated chat histories persist through RAG retrieval. | Explicit author claim | Paper | Abstract; RAG analysis | PDF 1; RAG section | Not applicable | Reported persistence result. |

## Provenance

- Discovery source: prior corpus; journal DOI; arXiv
- Discovery query: exact-title and DOI verification
- Accessed version: published journal metadata; arXiv 2407.07791 open copy
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

