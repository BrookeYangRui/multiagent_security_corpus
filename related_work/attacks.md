# Attacks

Cross-paper synthesis of attacks that depend on multi-agent interaction. Counts
below are generated from `corpus/papers.csv` at the frozen 2026-07-01 cutoff.

## Corpus Boundary

The frozen imported primary-role field contains 58 attack papers: 44
`core_security` and 14 `security_relevant`. Forty are in the canonical archival
publication view and 18 are nonarchival or unresolved. These are paper-placement
fields pending source signoff, not accepted attack-claim counts. A paper can describe attacks and
still have another primary category when its main contribution is a benchmark,
defense, evaluation, or system study.

The search ledger has 2,182 deduplicated entities, while the 142-work canonical
package is a separate curated mapping set. The released crosswalk links 105
canonical works to broad inclusions, ten to excluded or unresolved search hits,
and 27 to no mechanical search match. Accordingly, neither search screening nor
the imported paper role is treated as a deterministic attack-claim decision.

## Targeted Gap Check

The four-family check is recorded row by row in
`corpus/sets/01_search_catalog/targeted_gap_search.csv`.

- Denial of service has one interaction-native formal anchor, CORBA
  (`zhou2026corba`), plus an interaction-amplified arXiv result on shared
  guardrail contention (`zhou2026shieldtarget`).
- Goal drift remains preprint-heavy. Alignment Tipping contributes an
  interaction-dependent diffusion experiment (`han2025alignmenttipping`), while
  ValueFlow is evaluation-primary (`liu2026valueflow`). Synthetic projections in
  Agent Drift are excluded from empirical claims.
- Shared-state and shared-tool attacks gained two full-text-supported records:
  FuncPoison (`long2025funcpoison`) and OMNI-LEAK (`naik2026omnileak`). XAMT is
  excluded because its LLM-MAS component supplies a formulation and proposed
  protocol rather than demonstrated interacting-agent evidence.
- No retained row is currently coded as an attack-primary LLM-MAS Sybil or
  identity-minting demonstration. A2ASecBench and BlockA2A remain evaluation- and
  defense-primary evidence for the identity surface. This is a bounded negative
  coding result that may change after unresolved screening and source signoff,
  not an impossibility claim.

## Evidence Status

The 20 load-bearing papers selected for source review are listed in
`reviews/queues/load_bearing.csv`. All received a source-level review, but
none is human-verified: 18 await author signoff and two retain explicit source
blockers. The 45 records in `reviews/queues/standard_attack.csv` are
attack-review candidates, not a final attack-primary denominator.
Reclassification can move a paper between attack, defense, and evaluation
roles without moving it between the mutually exclusive review queues.

Attack-bearing evidence is not restricted to attack-primary papers. The master
checklist in `reviews/queues/universal.csv` also assigns 77 remaining defense,
evaluation, survey, and general papers to cross-category screening. Together,
the three mutually exclusive tracks cover all 142 canonical works; all 142 have active
source-review proposals, but none is human-verified without named signoff.
