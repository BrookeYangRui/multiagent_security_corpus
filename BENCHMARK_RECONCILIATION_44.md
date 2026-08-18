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
| promote_set1 | 7 | Current Set 3 record should move to Set 1 |
| promote_set2 | 4 | Current Set 3 record should move to Set 2 |
| add_set1 | 1 | A2ASecBench is absent from the frozen generated sets/ledger and should enter Set 1 |
| move_set3 | 3 | Current active evaluation paper is measurement/context rather than MAS-security |
| keep_set3 | 5 | Benchmark-relevant context, but not active MAS-security evidence |
| relabel | 2 | Keep active membership but change dominant contribution |
| alias_merge_upgrade | 1 | Merge an older arXiv identity into the published canonical record and upgrade maturity |
| post_cutoff | 1 | Retain outside the frozen active corpus |

No benchmark-report row remains unresolved in this audit.

### Add or promote to active corpus

**Set 1**

- A2ASecBench -> evaluation.
- ACIARena -> evaluation.
- PEAR -> evaluation.
- Hidden in Plain Text -> evaluation.
- RiskLab -> evaluation; named-author signoff is still required for manuscript use.
- LieCraft -> evaluation.
- The Subtle Art of Defection -> evaluation.
- ATAG -> general, with `security_characterization` / threat-assessment methodology as the natural subtype.

**Set 2**

- GAMBIT -> evaluation.
- MAC-Bench -> evaluation.
- SafeAgents -> evaluation.
- Collaborative Shadows -> attack.

The strongest frozen-ledger contradictions are cases where the Set 3 row uses a
generic scope-rejection reason while the canonical source note or primary source
explicitly describes a material inter-agent security path.

### Primary-source resolutions for the former boundary cases

**The Subtle Art of Defection -> Set 1 / evaluation.** The experiment uses four
agents with one explicitly uncooperative member. Its uncooperative behaviors include
strategic deception, threats, punishment, and greedy exploitation; the paper measures
collective collapse/resource overuse and evaluates detection/mitigation. The security
failure is therefore tied to one member's behavior through communication and shared
resource dynamics, rather than being merely generic cooperation measurement.

**ATAG -> Set 1 / general.** ATAG extends attack-graph reasoning to agentic
applications by modeling facts, interaction rules, and multi-step paths across
interconnected agents. Its case studies include a three-agent trip planner and a
hierarchical multi-agent email responder in which compromise propagates across agent
boundaries. The dominant contribution is threat assessment/security
characterization, not an empirical benchmark.

**From Tasks to Teams / M-SAEA -> keep Set 3 / evaluation context.** The framework
introduces multi-agent risk concepts and a cross-agent divergence metric, but the
reported experiment audits prerecorded R-Judge trajectories and the formal setup
allows `M >= 1`. The headline evaluated result therefore does not establish that an
inter-agent relation is materially required for the measured security property.

### Move from active corpus to context

- Deliberation and drift -> Set 3 / measurement context.
- Reproducibility Study of Cooperation, Competition, and Maliciousness -> Set 3 /
  measurement context.
- Revisiting Multi-Agent Debate as Test-Time Scaling -> Set 3 / measurement context.

These three are also present in the separate 44-row evaluation-scope adjudication and
must be applied only once during integration.

### Keep active, but fix primary contribution

- Who's the Mole? / AgentXposed: keep Set 1, change `attack` -> `evaluation`. The
  benchmark-and-detection contribution is dominant; the attack primitive remains a
  secondary role.
- A Trace-Based Assurance Framework for Agentic AI Orchestration: keep Set 1, change
  `evaluation` -> `general`. The work contributes security-assurance methodology and
  estimators rather than a reported empirical evaluation.

### Identity correction

- `arxiv:2505.12442` ("IP Leakage Attacks Targeting LLM-Based Multi-Agent Systems")
  is the earlier version of the published USENIX Security paper MASLeak. Merge it
  into canonical `wang2026masleak`, keep `attack` primary, and upgrade Set 2 -> Set
  1 under the peer-reviewed maturity rule. This is an identity/maturity correction,
  not an additional paper.

### Keep contextual

- EIB-Learner / Understanding the Information Propagation Effects of Communication
  Topologies -> generic propagation measurement.
- PsySafe -> broad safety/trait-manipulation context under the current narrow
  security gate.
- ValueFlow -> behavioral/value propagation measurement.
- Agent Drift / ASI -> behavioral degradation measurement.
- From Tasks to Teams / M-SAEA -> risk-evaluation methodology whose headline
  experiment does not establish a material multi-agent dependency.

### Post-cutoff

- WeClawArena stays outside the frozen active corpus because its reported version is
  after the 2026-07-01 cutoff.

## Count implications

Do **not** replace the current 232 count with a new manuscript number yet.

If the non-pending recommendations in this 44-paper reconciliation were applied by
themselves, the active-corpus change would be:

- 12 add/promote into Set 1/2
- 3 move from Set 1/2 to Set 3
- net +9, or **241 active works** relative to the current main snapshot

That is not the final corpus because the separate evaluation-scope audit proposes 17
active evaluation rows moving to Set 3. The three moves above are already included in
those 17 and must not be subtracted twice. Combining the two audits mechanically gives
a **provisional 227** active works: `232 - 17 + 12`.

This is only a reconciliation checkpoint. General/survey adjudications, identity
merges, builder integration, rebuild validation, and named-author signoff must be
completed before manuscript counts change.

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
