# Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast

> **Source-review correction:** The Source Review section at the end supersedes inconsistent automated coding in this note. It still requires author signoff.

## Citation

- Authors: Xiangming Gu, Xiaosen Zheng, Tianyu Pang, Chao Du, Qian Liu, Ye Wang, Jing Jiang, Min Lin
- Year: 2024
- Venue: ICML 2024
- DOI: Not reported
- Primary URL: https://proceedings.mlr.press/v235/gu24e.html
- Open access URL: https://raw.githubusercontent.com/mlresearch/v235/main/assets/gu24e/gu24e.pdf
- BibTeX key: `gu2024agentsmith`

## Paper Type

Attack; Empirical study; Theoretical analysis

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

A population of independently instantiated LLaVA-1.5 agents with memory banks
that communicate through randomized pairwise chats.

### Multi-Agent Dependency

The attack becomes an infectious jailbreak only when the seeded agent transmits
adversarial content to peers; population spread and its growth rate are undefined
for a single isolated agent.

### Application Domain

General-purpose multimodal agent societies.

## Security Model

- Protected assets: behavioral alignment of agents and population-level safety.
- Threat actor: an external adversary able to place one adversarial image in one
  agent's memory.
- Trusted components: other agents initially behave honestly.
- Attacker capabilities: seed one selected agent; no continued intervention is
  required after seeding.
- Security assumptions: agents retrieve memory and exchange content through
  pairwise interaction.

## Main Contribution

The paper introduces infectious jailbreak, demonstrates propagation from one
seeded multimodal agent across populations up to one million simulated agents,
and analyzes conditions under which a defense can restrain spread.

## Attack or Failure

- Attack surface: agent memory and pairwise communication.
- Attack mechanism: an infectious adversarial image causes recipients to retain
  and retransmit jailbreak behavior.
- System-level failure: propagation and containment failure.
- Security consequence: population-wide harmful or unaligned behavior.

## Defense

- Defense mechanism: a theoretical restraint principle; no complete practical
  defense is introduced.
- Intervention point: inter-agent propagation process.
- Required observability: infection/spread behavior across the population.
- Assumptions: depends on the modeled interaction process.
- Limitations: the authors leave practical defense construction open.

## Evaluation

- Evaluated systems: LLaVA-1.5 agents.
- Agent configuration: randomized pairwise chat; populations scale to one
  million in simulation.
- Dataset or environment: simulated multimodal multi-agent environment.
- Baselines: non-infectious adversarial inputs and alternative settings described
  in the paper.
- Metrics: infected population and propagation behavior.
- Main results: one seeded adversarial image is reported to produce exponentially
  fast infectious jailbreak under the evaluated interaction model.

## Relation to Existing Work

- Claimed research gap: prior red teaming attacks individual MLLM agents rather
  than modeling autonomous spread through an agent population.
- Closest related work: single-agent multimodal jailbreak and adversarial-image
  attacks.
- Difference from prior work: the interaction graph is part of the attack rather
  than only the deployment context.

## Relevance to Our SoK

- Included concepts: infection seed, agent memory, behavioral contagion,
  population spread, containment.
- Taxonomy implications: supports a propagation-and-containment failure class.
- Supported research questions: how topology and agent interaction amplify a
  local compromise.
- Important limitations: proof-of-concept pairwise simulation does not establish
  prevalence in deployed systems.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The system contains up to one million LLaVA-1.5 agents with memory banks. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Not applicable | Official paper states the model, memory, and scale. |
| One seeded adversarial image can trigger infectious jailbreak without further attacker intervention. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | Stated in the official abstract. |
| The paper derives a condition for restraining spread but leaves practical defense open. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | Stated in the final abstract sentences. |
| This is a propagation-and-containment failure. | Corpus interpretation | Paper | Abstract; threat formulation | PDF 1-3 | Not applicable | Classification based on cross-agent spread. |

## Provenance

- Discovery source: prior corpus; PMLR proceedings
- Discovery query: Not applicable
- Accessed version: published ICML version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `source_reviewed_pending_author_signoff`

**Outcome:** Ready after minor patch

**Review source:** `reviews/universal/universal_114_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: Canonical published ICML version confirmed. Current title, author list, and year are consistent with PMLR. Use the PMLR record as canonical and retain any arXiv copy only as a linked version.
- Recommended scope: `core_security`
- Multi-agent dependency: The system contains independently instantiated multimodal agents with memory banks and randomized pairwise communication. Population spread and its growth are undefined for a single isolated agent.
- Recommended roles: attack; empirical study; theoretical analysis
- Maturity: Archival peer-reviewed primary evidence.

### Threat and Failure Coding

- Attacker or fault actor: External adversary seeds one selected agent with one adversarial image.
- Capabilities: Seeds the initial memory item; no continued intervention is required under the modeled propagation process.
- Preconditions: Agents retrieve memory content and exchange it through randomized pairwise chats.
- Surfaces: Agent memory; pairwise inter-agent communication.
- Mechanism: Memory seeding followed by retention and retransmission of the adversarial behavior.
- Primary system-level failure: F1 compromise propagation and containment failure.
- Impact: Population-level harmful or unaligned behavior. The one-million figure is simulated scale, not deployed prevalence.

### Evaluation Contract

- Configuration: LLaVA-1.5 agent population; randomized pairwise chats; simulated populations up to one million.
- Topology: Randomized pairwise interaction rather than a broad sweep of deployed topologies.
- Baseline or ablation: Noninfectious adversarial inputs and modeled alternative settings; exact baseline details should be cited from the experiment section when used.
- Metric: Infected population and propagation behavior over interaction rounds.
- Unit: Agent and population.
- Denominator: Population size, with infection status defined by the paper.
- Result boundary: The paper demonstrates rapid population spread from a single seeded agent under its simulated interaction model. Do not turn the title claim into a statement about real deployed systems.

### Evidence and Boundaries

- Evidence locations: Official PMLR abstract and paper record; paper Abstract and Introduction, PDF pp. 1 to 2; threat formulation and propagation analysis, PDF pp. 1 to 3.
- Author claim versus corpus interpretation: The seeded-image attack and simulated spread are author claims. Labeling the outcome F1 and interpreting it as a containment failure are corpus interpretations.
- Limitations: Proof-of-concept simulation; one principal model family; randomized pairwise interaction; no evidence of real-world prevalence; practical defense construction remains open.

### Required Corrections

- **MEDIUM - Result wording:** Do not equate one million simulated agents with a real deployment or prevalence claim.
- **MEDIUM - Evidence locator:** Replace broad abstract-only locator with exact propagation-analysis pages before citing a specific round or growth constant.
<!-- SOURCE_REVIEW_END -->
