# Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast

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

