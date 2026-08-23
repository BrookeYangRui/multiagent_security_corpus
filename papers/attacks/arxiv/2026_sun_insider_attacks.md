# Insider Attacks in Multi-Agent LLM Consensus Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Xiaolin Sun, Zixuan Liu, Yibin Hu, Zizhan Zheng
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2605.08268
- Primary URL: https://arxiv.org/abs/2605.08268
- Open access URL: https://arxiv.org/pdf/2605.08268
- BibTeX key: `sun2026insider`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Communicating LLM agents that iteratively exchange arguments and update their
answers until the benign participants reach consensus.

### Multi-Agent Dependency

One legitimate group member pursues a hidden objective to delay or prevent
agreement among the remaining agents. Consensus rate and time to agreement do
not exist for an isolated agent.

### Application Domain

General-purpose multi-agent deliberation and consensus formation.

## Security Model

- Protected assets: agreement, termination, and collective decision integrity.
- Threat actor: one malicious insider participating through the normal protocol.
- Trusted components: benign agents follow the deliberation process.
- Attacker capabilities: observe interaction state and send protocol-valid
  natural-language messages.
- Security assumptions: the attacker can train against a learned surrogate of
  benign response dynamics.

## Main Contribution

The paper formulates insider consensus manipulation as sequential decision
making. It learns a latent world model of benign-agent dynamics and trains an RL
attacker against that surrogate to prolong or prevent agreement.

## Attack or Failure

- Attack surface: protocol-valid deliberation messages from a group member.
- Attack mechanism: a learned policy adaptively chooses messages based on latent
  behavioral state.
- System-level failure: consensus termination and collective decision-integrity
  failure.
- Security consequence: benign agents agree less often and remain in disagreement
  longer.

## Defense

- Defense mechanism: Not proposed.
- Intervention point: Not reported.
- Required observability: a candidate defense would need interaction history and
  member-level influence signals.
- Assumptions: Not reported.
- Limitations: the paper labels its results preliminary and evaluates a small
  controlled consensus setting.

## Evaluation

- Evaluated systems: groups of GPT-4o agents in a language-based consensus task.
- Agent configuration: benign participants plus one malicious insider.
- Dataset or environment: controlled consensus episodes described by the paper.
- Baselines: a direct malicious-prompt attacker.
- Metrics: benign consensus rate and episode duration.
- Main results: the world-model RL attacker reduces consensus and prolongs
  disagreement more than the direct-prompt baseline.

## Relation to Existing Work

- Papers compared by the authors: multi-agent debate, Byzantine behavior, and
  model-based reinforcement learning.
- Claimed research gap: prior LLM-MAS work commonly assumes all participating
  members share the collective objective.
- Closest related work: malicious-agent debate attacks and Byzantine consensus
  studies.
- Difference from prior work: the insider adapts using a learned surrogate of
  benign interaction dynamics rather than a fixed malicious prompt.

## Relevance to Our SoK

- Included concepts: malicious member, protocol-valid influence, adaptive attack,
  and consensus termination.
- Taxonomy implications: the mechanism is world-model RL manipulation; the
  violated properties are agreement and liveness.
- Supported research questions: how adaptive insiders exploit collective dynamics
  without modifying the protocol.
- Important limitations: preliminary preprint evidence should not be weighted like
  a peer-reviewed Byzantine robustness result.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| A malicious insider seeks to delay or prevent benign consensus. | Explicit author claim | Paper | Abstract; problem formulation | PDF 1-3 | Not applicable | The objective is defined over agreement among benign members. |
| The attack uses a learned latent world model and reinforcement learning. | Explicit author claim | Paper | Method | PDF 2-4 | Not applicable | The surrogate predicts benign dynamics used during attacker training. |
| The evaluation reports consensus rate and episode duration. | Explicit author claim | Paper | Experiment | PDF 3-4 | Not applicable | These measure agreement success and prolonged disagreement. |
| The paper presents its evidence as preliminary. | Explicit author claim | Paper | Abstract; results | PDF 1; 4 | Not applicable | The abstract explicitly calls the results preliminary. |

## Provenance

- Discovery source: arXiv; prior systematic full-text screening
- Discovery query: `Insider Attacks Multi-Agent LLM Consensus Systems`
- Accessed version: arXiv v1
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
