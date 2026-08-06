# ValueFlow: Measuring the Propagation of Value Perturbations in Multi-Agent LLM Systems

## Citation

- Authors: Jinnuo Liu, Chuke Liu, Hua Shen
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2602.08567
- Primary URL: https://arxiv.org/abs/2602.08567
- Open access URL: https://arxiv.org/pdf/2602.08567
- BibTeX key: `liu2026valueflow`

## Paper Type

Benchmark; Evaluation; Empirical study

Primary category: evaluation

Scope relation: security_relevant

## Scope

### System Studied

Multi-agent pipelines in which agents observe prior agents' value-expressive
outputs under different roles, backbones, and communication topologies.

### Multi-Agent Dependency

The measured outcome is propagation from a perturbed node to downstream agents
and the final system output; topology and node position are experimental factors.

### Application Domain

General-purpose value-alignment auditing.

## Security Model

- Protected assets: stability of collective value orientation.
- Threat actor: the framework injects controlled value perturbations; it does not
  specify a deployment adversary.
- Trusted components: the evaluation questions and judge protocol.
- Attacker capabilities: perturb a selected agent's value signal.
- Security assumptions: downstream agents observe upstream outputs.

## Main Contribution

ValueFlow introduces a 56-value dataset and metrics for agent susceptibility and
system susceptibility. It evaluates how controlled value perturbations propagate
across models, personas, and topologies.

## Attack or Failure

- Attack surface: inter-agent messages.
- Attack mechanism: controlled node-level value perturbation.
- System-level failure: possible collective value or objective drift.
- Security consequence: final output changes despite a localized perturbation.

## Defense

No deployed defense is established; the framework is intended for auditing and
future mitigation design.

## Evaluation

- Evaluated systems: multiple LLM backbones and agent pipelines.
- Agent configuration: varied node roles and pipeline or branching topologies.
- Dataset or environment: 56 values derived from the Schwartz Value Survey.
- Baselines: unperturbed systems and alternative node placements.
- Metrics: beta-susceptibility and system susceptibility.
- Main results: propagation varies materially by value, model, role, and topology.

## Relevance to Our SoK

- Included concepts: measurement contract, value propagation, topology effects.
- Taxonomy implications: this is evaluation-primary rather than proof of a
  naturally occurring attack.
- Important limitations: preprint, LLM-as-a-judge measurement, and controlled
  perturbations rather than deployment incidents.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| ValueFlow uses a 56-value evaluation dataset. | Explicit author claim | Paper | Abstract; Sec. 3 | 1, 5-6 | Table 1 | Dataset is derived from the Schwartz Value Survey. |
| It separates agent sensitivity from final-system effects. | Explicit author claim | Paper | Sec. 2-3 | 3-5 | Fig. 2 | Beta-susceptibility and system susceptibility are separately defined. |
| Topology and node position are varied. | Explicit author claim | Paper | Sec. 4-5 | 7-12 | Fig. 4-7 | Experiments compare structural settings. |
| The study is evaluation-primary, not an observed incident. | Corpus interpretation | Paper | Throughout | Not applicable | Not applicable | Perturbations are deliberately constructed for measurement. |

## Provenance

- Discovery source: systematic screening ledger; arXiv API
- Discovery query: goal drift propagation multi-agent LLM
- Accessed version: arXiv v2
- Access date: 2026-08-06
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-06
