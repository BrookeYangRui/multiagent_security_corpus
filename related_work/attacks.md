# Attacks

Cross-paper synthesis of attacks that depend on multi-agent interaction. Counts
below are generated from `corpus/papers.csv` at the frozen 2026-07-01 cutoff.

## Corpus Boundary

The attack-primary corpus contains 55 canonical papers: 47 `core_security` and
8 `security_relevant`. Forty-two have a formal conference, journal, workshop,
or proceedings venue; 13 remain arXiv-only. A paper can describe attacks and
still have another primary category when its main contribution is a benchmark,
defense, survey, or system study.

The deterministic route from retrieval to these 55 papers is recorded in
`corpus/attack_screening.csv` and `corpus/attack_canonical_bridge.csv`. The
retrieved ledger has 2,182 deduplicated records, of which 1,085 enter the attack
candidate frame. Candidate decisions remain explicit: 40 exact canonical attack
bindings, 26 bindings to another primary category, 102 eligible backlog records,
767 screening exclusions, and 150 unresolved records. The remaining 1,097
retrieved records are outside the attack query frame.

## Targeted Gap Check

The four-family check is recorded row by row in
`corpus/targeted_attack_gap_search.csv`.

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
- No pre-cutoff attack-primary paper demonstrating an LLM-MAS Sybil or identity
  minting attack was verified. A2ASecBench and BlockA2A remain evaluation- and
  defense-primary evidence for the identity surface. This is a bounded negative
  search result, not an impossibility claim.

## Evidence Status

The 20 load-bearing papers selected for source review are listed in
`corpus/load_bearing_review_queue.csv`. All received a source-level review, but
none is human-verified: 18 await author signoff and two retain explicit source
blockers. The remaining 42 attack-primary papers are in
`corpus/attack_review_queue.csv`. The two queues jointly cover all 55
attack-primary papers because reclassification leaves 13 attack papers and
seven defense/evaluation papers in the load-bearing queue.

Attack-bearing evidence is not restricted to attack-primary papers. The master
checklist in `corpus/universal_review_queue.csv` also assigns 52 remaining
defense, evaluation, survey, and general papers to cross-category screening.
Together, the three mutually exclusive tracks cover all 114 included papers;
94 still await minimum review.
