# The Wolf Within: Covert Injection of Malice into MLLM Societies via an MLLM Operative

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `arXiv` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Zhen Tan, Chengshuai Zhao, Raha Moraffah, Yifan Li, Yu Kong, Tianlong Chen, Huan Liu
- Year: 2024
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2402.14859
- Primary URL: https://arxiv.org/abs/2402.14859
- Open access URL: https://arxiv.org/pdf/2402.14859
- BibTeX key: `tan2024wolfwithin`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Two-stage multimodal agent interaction in which a manipulated "wolf" MLLM
produces a prompt and media item consumed by a clean "sheep" MLLM.

### Multi-Agent Dependency

The attack objective is jointly optimized through the wolf and sheep models so
that the first agent's output becomes an indirect jailbreak prompt for the second.

### Application Domain

General-purpose multimodal agent societies.

## Security Model

- Protected assets: downstream agent refusal and output safety.
- Threat actor: an external white-box attacker.
- Trusted components: the sheep agent begins uncompromised.
- Attacker capabilities: access gradients and sampling behavior, perturb an image
  or audio input, and pass the wolf output plus perturbed media downstream.
- Security assumptions: the workflow forwards both generated text and media from
  one agent to another.

## Main Contribution

The paper formulates a cross-agent multimodal jailbreak in which an optimized
input makes one MLLM generate a prompt that induces another MLLM to emit a
targeted harmful response.

## Attack or Failure

- Attack surface: forwarded multimodal content and inter-agent prompts.
- Attack mechanism: projected-gradient perturbation through a composed
  wolf-to-sheep model path.
- System-level failure: one-hop cross-agent safety compromise.
- Security consequence: a previously clean recipient emits prohibited content.

## Defense

- Defense mechanism: Not proposed.
- Intervention point: Not applicable.
- Required observability: Not reported.
- Assumptions: Not applicable.
- Limitations: the study evaluates one-hop induced compromise, not autonomous
  retransmission or a reproducing population cascade.

## Evaluation

- Evaluated systems: LLaVA and PandaGPT as image-text and audio-text MLLMs.
- Agent configuration: one optimized wolf followed by a clean sheep, with
  transfer to other recipient models.
- Dataset or environment: 14 prohibited-content scenarios.
- Baselines: direct MLLM jailbreak literature is discussed; no directly matching
  cross-agent baseline is available.
- Metrics: manually judged attack success rate and transferability.
- Main results: Table 1 reports high image-based ASR across the 14 scenarios,
  with lower and more variable results for PandaGPT.

## Relation to Existing Work

- Claimed research gap: prior work directly attacked a target MLLM rather than
  using one MLLM's output to attack another.
- Closest related work: multimodal jailbreaks and Agent Smith.
- Difference from prior work: the adversarial objective is composed through two
  separately invoked MLLMs.

## Relevance to Our SoK

- Included concepts: compromised member, forwarded media, indirect prompt,
  multimodal composition, and cross-agent transfer.
- Taxonomy implications: the mechanism is cross-agent multimodal injection; the
  demonstrated failure is recipient compromise rather than epidemic contagion.
- Supported research questions: whether benign-looking inter-agent outputs can
  transport optimized malicious intent.
- Important limitations: white-box gradients, manual evaluation, two-agent flow,
  and an unresolved printed trial denominator constrain generalization.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The attacker optimizes through a wolf and sheep MLLM jointly. | Explicit author claim | Paper | 3 | PDF 3 | Equation 2; Figure 2 | The objective applies the sheep to the wolf-generated prompt under a perturbation bound. |
| The attack assumes white-box model access. | Explicit author claim | Paper | 3 | PDF 3 | Not applicable | The threat setting explicitly assumes gradients and sampling access. |
| Evaluation uses LLaVA, PandaGPT, and 14 prohibited scenarios. | Explicit author claim | Paper | 4 | PDF 4-5 | Table 1 | The setup and table list both models and scenario categories. |
| The experiment demonstrates one-hop compromise, not onward infectiousness. | Interpretation | Paper | 3-4 | PDF 3-5 | Figures 2-4 | The sheep emits the target response; it is not shown infecting another clean agent. |

## Provenance

- Discovery source: arXiv; prior propagation audit
- Discovery query: `The Wolf Within MLLM societies attack publication`
- Accessed version: arXiv v2
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
