# Semantic Intent Fragmentation: A Single-Shot Compositional Attack on Multi-Agent AI Pipelines

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `AAAI Symposium Series` · signoff `2026-08-21`.
> This banner is authoritative if older review prose below records an earlier classification.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Tanzim Ahad, Ismail Hossain, Md Jahangir Alam, Sai Puppala, Yoonpyo Lee, Syed Bahauddin Alam, Sajedul Talukder
- Year: 2026
- Venue: AAAI Symposium Series
- DOI: 10.1609/aaaiss.v9i1.42936
- Primary URL: https://ojs.aaai.org/index.php/AAAI-SS/article/view/42936
- Open access URL: https://arxiv.org/abs/2604.08608
- BibTeX key: `ahad2026sif`

## Paper Type

Attack; Defense; Evaluation; Theoretical analysis; Empirical study

## Scope

### System Studied

LLM orchestration pipelines that decompose an enterprise request into subtasks
executed or assessed separately by multiple components or agents.

### Multi-Agent Dependency

Each subtask appears benign in isolation, while their composed plan violates a
security policy. The attack therefore depends on distributed task decomposition
and on guards that observe only local pieces of the execution.

### Application Domain

Financial reporting, information security, and human-resources analytics.

## Security Model

- Protected assets: plan integrity, information-flow policy, and authorization.
- Threat actor: a user submitting one legitimately phrased enterprise request.
- Trusted components: individual subtask classifiers and the orchestrator are
  treated as non-malicious but locally scoped.
- Attacker capabilities: choose the initial request; no later interaction or
  system modification is required.
- Security assumptions: the orchestrator autonomously decomposes work and local
  controls assess subtasks without reconstructing their joint intent.

## Main Contribution

The paper introduces Semantic Intent Fragmentation (SIF), formalizes a
plan-generation gap, and defines a Fragmentation Score. It evaluates four SIF
mechanisms and proposes plan-level compliance checking plus information-flow
taint analysis.

## Attack or Failure

- Attack surface: orchestrator task decomposition and per-subtask safety checks.
- Attack mechanism: harmful intent is fragmented into individually benign
  subtasks whose composition performs an unauthorized operation.
- System-level failure: compositional authorization and information-flow failure.
- Security consequence: policy-violating plans pass all local classifiers.

## Defense

- Defense mechanism: a Compositional Intent Verifier combined with
  information-flow-control taint analysis.
- Intervention point: before subtask dispatch, at the complete-plan boundary.
- Required observability: all subtasks, their data dependencies, and the original
  request.
- Assumptions: the plan is available before execution and can be checked as a
  whole.
- Limitations: the reported study uses 14 generated enterprise scenarios and a
  particular orchestrator rather than deployed production traces.

## Evaluation

- Evaluated systems: an LLM orchestrator plus six subtask-level classifier
  families and three independent validation signals.
- Agent configuration: one orchestrator decomposes each request into a
  multi-step plan assessed locally and globally.
- Dataset or environment: 14 scenarios across finance, security, and HR.
- Baselines: local subtask classifiers without compositional plan checking.
- Metrics: attack success, classifier pass rate, and defense false-positive rate.
- Main results: 10 of 14 requests yield policy-violating plans while every
  individual subtask passes local checks; the reported combined defense detects
  all confirmed cases with no false positives in this study.

## Relation to Existing Work

- Papers compared by the authors: prompt injection, task-decomposition attacks,
  and LLM-agent safety evaluation.
- Claimed research gap: local classifier improvements cannot identify a violation
  visible only in the full plan.
- Closest related work: conjunctive prompt attacks and multi-agent arbitrary-code
  composition attacks.
- Difference from prior work: SIF uses one benign-looking request and requires no
  injected artifact or follow-up interaction.

## Relevance to Our SoK

- Included concepts: task decomposition, partial observability, compositional
  intent, provenance gaps, and pre-dispatch enforcement.
- Taxonomy implications: the attack mechanism differs from the violated property,
  which is system-level action and authorization integrity.
- Supported research questions: what global context a defense needs to validate a
  distributed plan.
- Important limitations: reported sufficiency applies to the paper's scenarios
  and checker configuration, not arbitrary multi-agent workflows.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| SIF fragments one harmful intent across locally benign subtasks. | Explicit author claim | Paper | Abstract; threat model | PDF 1 onward | Not applicable | The violation becomes visible only when the generated plan is considered jointly. |
| The attack requires only the initial request. | Explicit author claim | Paper | Abstract | PDF 1 | Not applicable | The authors call this property single-shot autonomy. |
| Ten of fourteen scenarios produce violating plans while local checks pass. | Explicit author claim | Paper | Evaluation | Reported results | Not applicable | The paper reports a 71% attack rate and local pass status for all component tasks. |
| The paper appears in the AAAI Symposium Series. | Verified metadata | Publisher | Article metadata | Not applicable | Not applicable | The AAAI article page and DOI identify volume 9, issue 1, pages 229-237. |

## Provenance

- Discovery source: AAAI publisher page; DOI metadata; arXiv; prior systematic corpus
- Discovery query: `Semantic Intent Fragmentation DOI AAAI Symposium`
- Accessed version: published AAAI Symposium Series metadata with arXiv full text
- Access date: 2026-08-05
- Prepared by: automated extraction; model/version not recorded
- Verification status: `agent_unverified`
- Last updated: 2026-08-05
