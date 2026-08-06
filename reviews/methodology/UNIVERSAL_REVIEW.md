# Universal Corpus Review Checklist

Every included paper receives a minimum review regardless of its primary
directory. `primary_category` controls canonical placement and paper-level
counting; it does not determine whether the paper contains attack evidence.

## Files

- `reviews/queues/universal.csv`: master checklist for all 114 included papers.
- `reviews/queues/load_bearing.csv`: 20 load-bearing papers, including source
  blockers.
- `reviews/queues/standard_attack.csv`: 42 attack-primary papers.
- `reviews/queues/cross_category.csv`: 52 defense, evaluation, survey,
  and general papers requiring attack-bearing screening.

The three review tracks are mutually exclusive and jointly cover all 114
structured papers. All 114 now have a source-review proposal in
`reviews/universal/universal_114_source_review.csv`; every row still requires
named human signoff or resolution of its explicit blocker.

## Minimum Review

For every paper, check:

1. canonical title, authors, year, venue, DOI, URLs, and accessed version;
2. whether separately addressable LLM-backed agents actually interact;
3. `primary_category`, all secondary `paper_type` roles, and `scope_relation`;
4. whether the paper introduces, evaluates, reuses, analyzes, or merely mentions
   an attack;
5. whether attack evidence is empirical, theoretical, inherited from another
   paper, or only discussed as background;
6. attacker position, capabilities, preconditions, mechanism, system-level
   failure, and impact for each eligible claim;
7. metric, unit, denominator, baseline, and exact evidence location;
8. which analysis-specific eligible sets may use each attack instance.

## Attack Evidence Roles

Use one or more of:

```text
introduces_attack
attack_elicitation
evaluates_attack
benchmark_attack_suite
reuses_existing_attack
fault_evaluation
ecosystem_measurement
attack_analysis_only
mentions_attack
dual_use_protocol
```

`mentions_attack` and survey summaries are not primary attack evidence. A
defense or evaluation paper can be attack-bearing when it actually executes or
measures an attack, but its paper-level primary category remains unchanged.

## Completion

After minimum review, set `attack_evidence_status` to an adjudicated value,
record `attack_role`, and decide whether claim-level attack-instance coding is
required. Human verification still requires a named reviewer, date, and
adjudication note.
