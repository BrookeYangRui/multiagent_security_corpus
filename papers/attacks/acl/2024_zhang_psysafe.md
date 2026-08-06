# PsySafe: A Comprehensive Framework for Psychological-based Attack, Defense, and Evaluation of Multi-agent System Safety

## Citation

- Authors: Zaibin Zhang, Yongting Zhang, Lijun Li, Hongzhi Gao, Lijun Wang, Huchuan Lu, Feng Zhao, Yu Qiao, Jing Shao
- Year: 2024
- Venue: ACL 2024
- DOI: 10.18653/v1/2024.acl-long.812
- Primary URL: https://aclanthology.org/2024.acl-long.812/
- Open access URL: https://aclanthology.org/2024.acl-long.812.pdf
- BibTeX key: `zhang2024psysafe`

## Paper Type

Attack; Defense; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

LLM-based multi-agent systems in which agents interact under assigned
psychological traits and produce collective behavior.

### Multi-Agent Dependency

The evaluated harm includes collective dangerous behavior caused during agent
interaction, not only an unsafe response from one isolated model.

### Application Domain

General-purpose agent societies and social interaction.

## Security Model

- Protected assets: behavioral safety of individual agents and the collective.
- Threat actor: an evaluator or adversary that instills dark psychological traits.
- Trusted components: the evaluation framework and defense components.
- Attacker capabilities: manipulate agent traits or psychological state in the
  evaluated scenarios.
- Security assumptions: agents' prompted psychological characteristics affect
  their interactive behavior.

## Main Contribution

PsySafe provides a psychology-grounded framework spanning attacks, behavioral
and psychological evaluation, and mitigation of safety risks in multi-agent
systems.

## Attack or Failure

- Attack surface: agent role/personality prompts and social interaction.
- Attack mechanism: traits attacks induce dark psychological states.
- System-level failure: collective dangerous behavior.
- Security consequence: unsafe group decisions or actions.

## Defense

- Defense mechanism: psychological and behavioral safety strategies described
  in the paper.
- Intervention point: agent behavior and system evaluation.
- Required observability: conversations and assessed psychological/behavioral
  state.
- Assumptions: psychology-inspired measurements serve as useful proxies.
- Limitations: transfer from simulated psychological traits to deployed systems
  is not established by the corpus record.

## Evaluation

- Evaluated systems: multiple LLM-based multi-agent configurations.
- Agent configuration: interacting agents with controlled psychological traits.
- Dataset or environment: PsySafe attack-defense-evaluation framework.
- Baselines: configurations and mitigation variants defined in the paper.
- Metrics: psychological assessments and collective danger rates.
- Main results: the authors report collective dangerous behavior, self-reflection
  during dangerous behavior, and correlation between psychological assessments
  and dangerous behavior.

## Relation to Existing Work

- Claimed research gap: limited comprehensive treatment of multi-agent safety
  attacks, evaluation, and defense.
- Closest related work: LLM safety evaluation and psychology-inspired model
  assessment.
- Difference from prior work: makes interacting agent psychology the attack and
  evaluation surface.

## Relevance to Our SoK

- Included concepts: malicious role composition, social influence, collective
  unsafe behavior, group-level metrics.
- Taxonomy implications: behavior is an impact unless tied to a stated protected
  property; the attack mechanism and system failure should be coded separately.
- Supported research questions: how local trait manipulation changes collective
  outcomes.
- Important limitations: broad safety phenomena may not all meet a narrow
  security inclusion rule.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| PsySafe covers attack, defense, psychological evaluation, and behavioral evaluation. | Explicit author claim | Paper | Abstract; framework overview | PDF 1-3 | Not applicable | The official abstract enumerates the framework components. |
| Traits attacks can cause collective dangerous behavior during interaction. | Explicit author claim | Paper | Sec. 2.2 | PDF 3 | Not applicable | The paper describes contamination of multi-agent systems through traits attack. |
| The work reports correlation between psychological assessment and dangerous behavior. | Explicit author claim | Paper | Abstract; experiments | PDF 1; results sections | Not applicable | Stated in the abstract. |
| Some reported outcomes may be safety rather than security failures. | Corpus interpretation | Paper | Scope and experiments | PDF 1 onward | Not applicable | Inclusion boundary applied by this corpus. |

## Provenance

- Discovery source: prior corpus; ACL Anthology
- Discovery query: `site:aclanthology.org/2024 multi-agent attack LLM safety`
- Accessed version: published ACL 2024 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

