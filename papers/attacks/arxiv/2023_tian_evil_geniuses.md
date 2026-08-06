# Evil Geniuses: Delving into the Safety of LLM-based Agents

## Citation

- Authors: Yu Tian, Xiao Yang, Jingyuan Zhang, Yinpeng Dong, Hang Su
- Year: 2023
- Venue: arXiv preprint
- DOI: 10.48550/arXiv.2311.11855
- Primary URL: https://arxiv.org/abs/2311.11855
- Open access URL: https://arxiv.org/pdf/2311.11855
- BibTeX key: `tian2023evilgeniuses`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Role-based LLM agent systems instantiated with CAMEL, MetaGPT, and ChatDev.

### Multi-Agent Dependency

The study varies agent count, role definitions, and attack placement across
system-level and agent-level prompts; its ablations report that removing
inter-agent conversation materially reduces attack effectiveness.

### Application Domain

Role-play, software development, and general collaborative tasks.

## Security Model

- Protected assets: refusal behavior and safe system output.
- Threat actor: a user or system designer able to supply adversarial role prompts.
- Trusted components: model weights and framework code are unchanged.
- Attacker capabilities: modify prompts at agent or system level and use a
  Red-Blue multi-agent process to generate role-specific attacks.
- Security assumptions: deployed agents follow configurable role prompts and
  exchange outputs during task execution.

## Main Contribution

The paper studies how agent quantity, role definition, and attack level affect
harmful behavior, and introduces Evil Geniuses, a Red-Blue prompt-generation
method for role-specific attacks.

## Attack or Failure

- Attack surface: role prompts, system prompts, and inter-agent dialogue.
- Attack mechanism: template attacks or adversarial roles generated through
  iterative Red-Blue interaction.
- System-level failure: collaborative generation bypasses refusal safeguards.
- Security consequence: agent systems generate harmful or stealthy content at
  higher rates than isolated models in evaluated settings.

## Defense

- Defense mechanism: reviewer/tester roles and GPT-4 filtering are evaluated
  incidentally; no general defense is proposed.
- Intervention point: downstream review and model output filtering.
- Required observability: generated content and role outputs.
- Assumptions: reviewing agents or provider filters recognize unsafe content.
- Limitations: review components do not consistently prevent harmful generation.

## Evaluation

- Evaluated systems: CAMEL, MetaGPT, and ChatDev using GPT-3.5 and GPT-4.
- Agent configuration: one-model baseline, two-agent CAMEL, and seven-agent
  ChatDev, plus agent-role and system-component ablations.
- Dataset or environment: AdvBench and a role/attack-level dataset introduced by
  the authors.
- Baselines: direct/template attacks and isolated LLM evaluation.
- Metrics: harmful and non-refusal attack success rates.
- Main results: Table 3 reports higher attack success as the evaluated system
  moves from one model to two-agent CAMEL and seven-agent ChatDev.

## Relation to Existing Work

- Claimed research gap: prior jailbreak work did not study the combined effects
  of agent quantity, roles, and interaction environment.
- Closest related work: LLM jailbreak prompts and role-play attacks.
- Difference from prior work: the attack-generation and target settings are
  structured around role-based agent systems.

## Relevance to Our SoK

- Included concepts: role composition, attack placement, agent count, review
  roles, and interaction-amplified jailbreak.
- Taxonomy implications: role prompts are a precondition and adversarial prompt
  generation is a mechanism; the failure is collective safety integrity.
- Supported research questions: whether interaction and role composition amplify
  single-model jailbreak risk.
- Important limitations: the study predates a precise LLM-MAS threat model and
  mixes attack generation by agents with attacks on collaborative systems.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The study evaluates CAMEL, MetaGPT, and ChatDev with GPT-3.5 and GPT-4. | Explicit author claim | Paper | 4 | PDF 5 | Not applicable | The experimental setup names all frameworks and model families. |
| Removing collaborative dialogue reduces attack performance. | Explicit author claim | Paper | 4, Ablations | PDF 6 | Table 2 | The no-reviewer/tester and isolated-agent ablations test interaction components. |
| Agent quantity is compared from one model to two and seven agents. | Explicit author claim | Paper | 4 | PDF 6 | Table 3 | The table reports Num values of 1, 2, and 7. |
| The paper mixes MAS-targeted risk with a multi-agent attack generator. | Interpretation | Paper | 3-4 | PDF 3-7 | Figures 2-4 | Evil Geniuses itself is a Red-Blue generation workflow, while the evaluated targets include agent systems. |

## Provenance

- Discovery source: arXiv; prior systematic corpus
- Discovery query: `Evil Geniuses LLM multi-agent safety attack`
- Accessed version: arXiv v2
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

