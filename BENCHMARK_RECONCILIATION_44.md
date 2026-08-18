# Benchmark Reconciliation Audit: 44-Paper Evaluation Report

Date: 2026-08-18  
Base: `main@7cf51bfd39231f6123fbd0dc74b8f17fd8ab1969`  
Status: audit only; no generated corpus membership has been changed.

## Purpose

This audit reconciles the 44 papers in the benchmark report with the current frozen
three-set corpus and the repository's benchmark sidecar notes. The report population
is an **analysis set**, not the same thing as papers whose
`dominant_contribution=evaluation`.

The reconciliation therefore keeps two independent labels:

1. `dominant_contribution`: attack, defense, evaluation, general, or survey.
2. `evaluation_artifact_role`: whether a paper supplies a benchmark, harness,
   dataset, reusable metric, or comparable evaluation artifact.

Attack-primary papers do not become evaluation-primary merely because they contain a
benchmark.

## Current frozen snapshot

The base manifest has 2,216 frozen works:

- Set 1: 99
- Set 2: 133
- Set 3: 444
- Screened out: 1,540
- Active MAS-security corpus: 232 = 99 + 133

These counts remain canonical until adjudications are integrated through the review
ledger and builder.

## Reconciliation result

All 44 report papers are mapped in
`corpus/adjudication/benchmark_reconciliation_2026-08-18.csv`.

| Action | Count | Meaning |
| --- | ---: | --- |
| keep | 20 | Current active membership and dominant contribution remain appropriate |
| promote_set1 | 5 | Current Set 3 record should move to Set 1 |
| promote_set2 | 4 | Current Set 3 record should move to Set 2 |
| add_set1 | 1 | A2ASecBench is absent from the frozen generated sets/ledger and should enter Set 1 |
| move_set3 | 3 | Current active evaluation paper is measurement/context rather than MAS-security |
| keep_set3 | 4 | Benchmark-relevant context, but not active MAS-security evidence |
| relabel | 2 | Keep active membership but change dominant contribution |
| alias_merge_upgrade | 1 | Merge an older arXiv identity into the published canonical record and upgrade maturity |
| needs_source_review | 3 | Do not change membership until claim-level source review resolves the boundary |
| post_cutoff | 1 | Retain outside the frozen active corpus |

### High-value corrections

**Promote or add to active corpus**

- A2ASecBench -> Set 1 / evaluation.
- ACIARena -> Set 1 / evaluation.
- PEAR -> Set 1 / evaluation.
- Hidden in Plain Text -> Set 1 / evaluation.
- RiskLab -> Set 1 / evaluation, with named-author signoff still required.
- LieCraft -> Set 1 / evaluation, medium confidence.
- GAMBIT -> Set 2 / evaluation.
- MAC-Bench -> Set 2 / evaluation.
- SafeAgents -> Set 2 / evaluation.
- Collaborative Shadows -> Set 2 / attack.

The strongest contradictions are ACIARena, PEAR, SafeAgents, Hidden in Plain Text,
GAMBIT, and MAC-Bench: their canonical notes describe a material inter-agent
security path, while the frozen Set 3 rows use generic scope-rejection language.

**Move from active corpus to context**

- Deliberation and drift -> Set 3 / measurement context.
- Reproducibility Study of Cooperation, Competition, and Maliciousness -> Set 3 /
  measurement context.
- Revisiting Multi-Agent Debate as Test-Time Scaling -> Set 3 / measurement context.

These are also present in the separate 44-row evaluation-scope adjudication. They
must be applied only once during integration.

**Keep active, but fix primary contribution**

- Who's the Mole? / AgentXposed: Set 1 remains, but the benchmark-and-detection
  contribution is better represented as `evaluation` than `attack`.
- A Trace-Based Assurance Framework for Agentic AI Orchestration: Set 1 remains,
  but the report shows no empirical evaluation; its primary contribution is better
  represented as `general` / security-assurance methodology. Its evaluation
  estimators remain analysis artifacts.

**Identity correction**

- `arxiv:2505.12442` ("IP Leakage Attacks Targeting LLM-Based Multi-Agent Systems")
  is the earlier version of the published USENIX Security paper MASLeak. Merge it
  into canonical `wang2026masleak`, keep `attack` primary, and upgrade Set 2 -> Set
  1 under the peer-reviewed maturity rule. This is an identity/maturity correction,
  not an additional paper.

**Do not promote yet**

- The Subtle Art of Defection: current note is not claim-level extracted.
- ATAG: the benchmark report gives multi-agent attack-graph evidence, but the
  canonical note is still imported and the paper has no runtime empirical
  evaluation. Source review should decide whether it becomes Set 1 `general`
  threat-modeling/security characterization.
- From Tasks to Teams / M-SAEA: the reported auditor operates over prerecorded
  trajectories and the framework admits M>=1; source review must establish that a
  material inter-agent security relation is part of the evaluated property.

**Keep contextual**

- EIB-Learner / information-propagation study.
- PsySafe under the current narrow security gate.
- ValueFlow.
- Agent Drift / ASI.

**Post-cutoff**

- WeClawArena stays outside the frozen active corpus because its reported version is
  after the 2026-07-01 cutoff.

## Count implications

Do **not** replace the current 232 count with a new paper number yet.

If the non-pending recommendations in this 44-paper reconciliation were applied by
themselves, the net active-corpus change would be:

- 10 add/promote into Set 1/2
- 3 move from Set 1/2 to Set 3
- net +7, or 239 active works relative to the current main snapshot

That is not the final corpus because the separate evaluation-scope audit proposes
17 active evaluation rows moving to Set 3. Since the three moves above are already
among those 17, combining the two audits mechanically gives a **provisional 225**
active works: `232 - 17 + 10`.

This number is only a reconciliation checkpoint. General and survey adjudications,
identity merges, source-review decisions, and rebuild validation must be applied
before any manuscript count is changed.

## Benchmark-report corrections required before manuscript use

The report is useful as an analysis artifact, but its current numbers should not be
copied into the paper yet.

1. Its scope paragraph still uses the old `287 = 121 + 166` snapshot.
2. The report states both `14/44` and `9/44` for full-execution-trace headline
   evaluation. The measurement contract needs one operational definition and a
   regenerated count.
3. It states both `7/44` and `6/44` for matched single-agent controls. The
   `partial`-control rule must be fixed before recounting.
4. `related_work/benchmarks.md` says there are 21 canonical evaluation notes, while
   its table currently lists 20 keys.
5. The report's 44-paper benchmark population should be regenerated from a dedicated
   evaluation-artifact index after membership reconciliation, rather than inferred
   from primary paper category.

## Integration rule

Do not hand-edit `corpus/set1_core.csv`, `corpus/set2_emerging.csv`, or
`corpus/set3_context.csv`.

Integration should:

1. apply membership/contribution overrides at the review-ledger or builder input;
2. merge aliases before counting;
3. rebuild all generated sets and the manifest;
4. regenerate the evaluation-artifact index from canonical identities;
5. regenerate benchmark-report counts from that index;
6. validate Set1 + Set2 + Set3 + screened-out arithmetic;
7. require named-author signoff for manuscript-facing counts and claims.

Until that integration is complete, current `main` counts remain authoritative.
