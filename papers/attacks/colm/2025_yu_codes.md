# LLM-based Multi-Agents System Attack via Continuous Optimization with Discrete Efficient Search

## Citation

- Authors: Weichen Yu, Kai Hu, Tianyu Pang, Chao Du, Min Lin, Matt Fredrikson
- Year: 2025
- Venue: COLM
- DOI: Not reported
- Primary URL: https://openreview.net/forum?id=ED5diyzc1C
- Open access URL: https://openreview.net/pdf?id=ED5diyzc1C
- BibTeX key: `yu2025codes`

## Paper Type

Attack; Evaluation; Empirical study

## Scope

### System Studied

Multi-agent LLM systems in which agents repeatedly exchange natural-language
messages and retain earlier interaction context.

### Multi-Agent Dependency

The adversary intervenes once against one agent. A successful self-repeating
suffix is then emitted by recipients and propagated through subsequent
inter-agent messages, so compromise is defined over the collective execution.

### Application Domain

General-purpose multi-agent LLM workflows and multi-level safeguard pipelines.

## Security Model

- Protected assets: collective instruction integrity and system-wide safety.
- Threat actor: an external adversary able to affect one initial agent.
- Trusted components: downstream agents and safeguards begin uncompromised.
- Attacker capabilities: optimize and inject a token-level adversarial suffix in
  one interaction.
- Security assumptions: agents transmit text and retain enough received content
  for self-repetition to continue.

## Main Contribution

The paper defines three single-intervention attack scenarios and proposes
Continuous Optimization with Discrete Efficient Search (CODES). CODES combines
continuous-space token optimization with discrete search to produce
self-replicating prompts that propagate beyond the initially targeted agent.

## Attack or Failure

- Attack surface: inter-agent messages and retained conversation context.
- Attack mechanism: a token-level suffix induces recipients to reproduce the
  adversarial string while generating harmful content.
- System-level failure: behavioral contagion and failure to contain a one-agent
  compromise.
- Security consequence: one intervention can affect an agent cohort or traverse
  multiple safeguard modules.

## Defense

- Defense mechanism: the paper evaluates attacks against multi-level safeguard
  configurations; it does not establish a general defense.
- Intervention point: safeguards operate before or between model invocations.
- Required observability: the message presented at each guarded stage.
- Assumptions: local safeguards can identify or rewrite adversarial content.
- Limitations: adaptive optimization can target the composed pipeline, and the
  evaluated settings do not establish coverage for arbitrary topologies.

## Evaluation

- Evaluated systems: multi-agent message chains and multi-level safeguard
  pipelines.
- Agent configuration: one initially targeted agent followed by interacting
  recipients; configurations vary across the three threat scenarios.
- Dataset or environment: harmful request and conversational attack settings
  defined by the paper.
- Baselines: prior token-level jailbreak optimization methods, including GCG and
  ADC.
- Metrics: attack success, self-repetition or propagation success, optimization
  loss, and efficiency.
- Main results: CODES succeeds across all three stated scenarios and improves
  optimization stability relative to the evaluated token-level baselines.

## Relation to Existing Work

- Papers compared by the authors: token-level jailbreak optimization and early
  infectious attacks on LLM agents.
- Claimed research gap: existing attacks are unstable when the optimized text is
  both input and changing output across repeated agents.
- Closest related work: the authors' earlier GIGA workshop paper and Agent Smith.
- Difference from prior work: CODES evaluates three practical, single-intervention
  scenarios and introduces a continuous-plus-discrete optimization procedure.

## Relevance to Our SoK

- Included concepts: single-seed infection, multi-round propagation, adaptive
  safeguard bypass, and containment failure.
- Taxonomy implications: the mechanism is suffix optimization; the system-level
  property lost is propagation containment.
- Supported research questions: how one local compromise becomes a population
  failure and why local safeguards do not necessarily compose.
- Important limitations: publication reports selected topologies and model
  configurations rather than a standardized population-level infection contract.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| The threat model permits one intervention on one MAS agent. | Explicit author claim | Paper | Abstract; Introduction | PDF 1-2 | Not applicable | The authors define three attack scenarios under a single-intervention constraint. |
| CODES combines continuous optimization with discrete search. | Explicit author claim | Paper | 3.2 | PDF 5 | Algorithms 1-2 | The method maintains dense adversarial tokens and uses coordinate search during optimization. |
| The optimized prompt self-repeats and propagates across agents. | Explicit author claim | Paper | Abstract; threat scenarios | PDF 1 onward | Not applicable | Repetition in agent outputs carries the harmful content to later recipients. |
| The work is a published COLM 2025 conference paper. | Verified metadata | Official venue | Paper header; accepted-paper list | PDF 1 | Not applicable | OpenReview labels the paper as published at COLM 2025, and the COLM accepted-paper list includes it. |

## Provenance

- Discovery source: COLM accepted-paper list; OpenReview; prior systematic corpus
- Discovery query: `COLM 2025 LLM-based Multi-Agents System Attack CODES`
- Accessed version: published COLM 2025 conference version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

