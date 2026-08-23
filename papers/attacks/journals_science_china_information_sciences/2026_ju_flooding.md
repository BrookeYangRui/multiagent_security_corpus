# Flooding Spread of Manipulated Knowledge in LLM-Based Multi-Agent Communities

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `Science China Information Sciences` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Tianjie Ju, Yiting Wang, Xinbei Ma, Pengzhou Cheng, Haodong Zhao, Yulong Wang, Lifeng Liu, Jian Xie, Zhuosheng Zhang, Gongshen Liu
- Year: 2026
- Venue: Science China Information Sciences
- DOI: 10.1007/s11432-024-4663-2
- Primary URL: https://doi.org/10.1007/s11432-024-4663-2
- Open access URL: https://arxiv.org/abs/2407.07791
- BibTeX key: `ju2026flooding`

## Paper Type

Attack; Evaluation

- Primary category: `attack`
- Scope relation: `core_security`

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

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `blocked_pending_final_source`

**Outcome:** Pending final source verification

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: The journal DOI and title are confirmed, but the final journal author metadata appears to disagree with the current ten-author record, potentially adding Yi Hua. The final journal PDF must be treated as authoritative before signoff.
- Recommended scope: `core_security`
- Multi-agent dependency: Manipulated knowledge spreads through communication and stored chat histories among LLM agents and persists through RAG retrieval.
- Recommended roles: attack; evaluation
- Maturity: Peer-reviewed journal work, but canonical metadata and full-text locators are not yet frozen.

### Threat and Failure Coding

- Attacker or fault actor: Adversary manipulates an initial model or agent before deployment and introduces manipulated knowledge through persuasion and knowledge injection.
- Capabilities: Uses DPO or LoRA-style persuasion adaptation and ROME-style knowledge editing, then relies on interaction and stored histories for spread.
- Preconditions: Agents trust peer messages and may persist chat histories for later RAG retrieval.
- Surfaces: Agent model state; communication; chat history; RAG memory.
- Mechanism: Persuasiveness injection plus manipulated-knowledge injection followed by interaction-driven spread and persistence.
- Primary system-level failure: F3 communication and shared-knowledge integrity failure.
- Impact: F1 containment and persistence failure is secondary.

### Evaluation Contract

- Configuration: Simulated LLM-agent communities with communication and optional RAG persistence.
- Topology: Community interaction settings; exact final-paper topology details must be recoded from the journal PDF.
- Baseline or ablation: Attack variants and benign settings described in the final paper.
- Metric: Spread accuracy for counterfactual or toxic knowledge, interaction turns, agent-order or population effects, and RAG persistence.
- Unit: Agent response, knowledge item, or interaction turn depending on analysis.
- Denominator: Must be copied from the final journal metric definitions and tables; the current record is too generic.
- Result boundary: The paper reports that manipulated knowledge can spread while preserving general capabilities and persist in retrieved histories. Exact numeric claims should wait for final-journal table verification.

### Evidence and Boundaries

- Evidence locations: Abstract and Introduction, PDF pp. 1 to 2 of the accessible version; method in Sec. III; experiments in Sec. IV, especially the spread and RAG-persistence subsections. Recheck page and table numbers against the final journal PDF.
- Author claim versus corpus interpretation: The two-stage manipulation and persistence are author claims. The F3 primary label and F1 secondary label are corpus interpretations.
- Limitations: Simulated community; predeployment model manipulation confounds a purely runtime attacker; static roles; final metadata and exact metric table locations remain unresolved.

### Required Corrections

- **CRITICAL - Author list:** Resolve the final journal author list from the publisher PDF before updating papers.csv.
- **CRITICAL - Evidence locators:** Replace accessible-version locators with final journal page and table locations.
- **HIGH - Attacker model:** Do not describe this as only an external runtime message attacker; the attack includes predeployment model manipulation.
<!-- SOURCE_REVIEW_END -->
