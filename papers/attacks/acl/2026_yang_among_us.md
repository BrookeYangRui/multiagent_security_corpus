# Among Us: Measuring and Mitigating Malicious Contributions in Model Collaboration Systems

## Citation

- Authors: Ziyuan Yang, Wenxuan Ding, Shangbin Feng, Yulia Tsvetkov
- Year: 2026
- Venue: ACL 2026
- DOI: 10.18653/v1/2026.acl-long.725
- Primary URL: https://aclanthology.org/2026.acl-long.725/
- Open access URL: https://aclanthology.org/2026.acl-long.725.pdf
- BibTeX key: `yang2026amongus`

## Paper Type

Attack; Defense; Benchmark; Evaluation; Empirical study

## Scope

### System Studied

Multi-model collaboration at four interaction levels: API routing, text exchange,
logit aggregation, and weight merging.

### Multi-Agent Dependency

The failure arises when one or more malicious contributor models participate in
a collaboration pool and influence routing, debate, aggregation, or merging; the
measured outcome is degradation of the composed system relative to a benign-only
pool.

### Application Domain

General-purpose model collaboration across safety, reasoning, factuality, code,
and instruction-following tasks.

## Security Model

- Protected assets: system-level safety, reasoning quality, factuality, code
  correctness, and instruction following.
- Threat actor: a contributor supplying one or more malicious models.
- Trusted components: the collaboration method and external supervisor are
  treated as benign in their respective evaluations.
- Attacker capabilities: introduce maliciousness through prompting, activation
  steering, supervised fine-tuning, or inverted-reward reinforcement learning.
- Security assumptions: the collaboration system accepts models from multiple
  parties and does not perfectly identify malicious contributors before use.

## Main Contribution

The paper engineers four classes of malicious language models and measures their
effect in eight collaboration methods spanning four interaction levels. It also
evaluates external-supervisor mitigations that disable or mask suspected models.

## Attack or Failure

- Attack surface: contributor admission, routing, exchanged text, aggregated
  logits, and merged parameters.
- Attack mechanism: insert models whose outputs or internal behavior have been
  made malicious through one of four engineering methods.
- System-level failure: collective output integrity and safety degradation.
- Security consequence: compromised contributors lower performance in reasoning
  and safety domains and can influence multiple collaboration mechanisms.

## Defense

- Defense mechanism: external supervisors score contributor outputs and disable
  or mask models judged malicious.
- Intervention point: collaboration supervisor and contributor aggregation.
- Required observability: access to candidate model outputs or contributions.
- Assumptions: an external supervisor is sufficiently trustworthy and capable of
  distinguishing malicious from benign contributions.
- Limitations: the authors report substantial recovery rather than complete
  resistance, and evaluate a bounded set of models, tasks, and collaboration
  methods.

## Evaluation

- Evaluated systems: eight methods at API, text, logit, and weight levels.
- Agent configuration: pools combining benign and malicious language models,
  with malicious count and diversity varied in ablations.
- Dataset or environment: ten datasets covering safety, reasoning, knowledge,
  code, and instruction following.
- Baselines: corresponding benign-only collaboration systems and unmitigated
  malicious settings.
- Metrics: task performance, degradation relative to the benign system, and
  performance recovery after mitigation.
- Main results: the paper reports average degradation of 7.12% in reasoning and
  7.94% in safety and average recovery of 95.31% of initial performance under its
  supervisor strategies.

## Relation to Existing Work

- Claimed research gap: prior model-collaboration work largely assumes benign
  contributors.
- Closest related work: faulty-agent robustness, malicious-agent attacks, and
  multi-agent debate attacks.
- Difference from prior work: the study spans four collaboration levels and four
  mechanisms for engineering malicious contributors in one evaluation.

## Relevance to Our SoK

- Included concepts: malicious membership, contributor diversity, collaboration
  level, aggregation, external supervision, and collective integrity.
- Taxonomy implications: contributor compromise is an adversary capability;
  routing, debate, logit aggregation, and weight merging are distinct exposed
  surfaces rather than separate failure categories.
- Supported research questions: how malicious fractions and collaboration
  mechanisms affect system-level robustness, and what observer scope mitigation
  requires.
- Important limitations: only text-level debate directly matches persistent
  message-passing LLM-MAS; API, logit, and weight collaboration remain adjacent
  multi-model composition settings and should be coded separately.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Four malicious-model engineering methods are evaluated. | Explicit author claim | Paper | 2.1 | PDF 2-3 | Not applicable | The methods are prompting, activation steering, SFT, and RL with inverted preference signals. |
| Eight collaboration methods span API, text, logit, and weight levels. | Explicit author claim | Paper | 2.2 | PDF 3-4 | Not applicable | The paper defines two representative methods at each of four collaboration levels. |
| Evaluation covers ten datasets and five task domains. | Explicit author claim | Paper | Abstract; A.1 | PDF 1; 14 | Table 4 | The dataset table lists safety, reasoning, knowledge, code, and instruction-following sources. |
| Reported average reasoning and safety degradation is 7.12% and 7.94%. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | The published abstract reports both aggregate decreases. |
| Supervisor strategies recover 95.31% of initial performance on average. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | The published abstract reports recovery while noting full resistance remains open. |
| Text-level debate is the clearest LLM-MAS subset of the broader model-collaboration study. | Interpretation | Paper | 2.2 | PDF 3 | Not applicable | Only this level is defined through generated-text exchange between independently responding models. |

## Provenance

- Discovery source: ACL Anthology; prior systematic screening corpus
- Discovery query: `site:aclanthology.org 2026 malicious multi-agent collaboration`
- Accessed version: published ACL 2026 version
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05

