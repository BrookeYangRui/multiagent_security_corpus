# Persistent Review Sets

This directory reconciles the frozen search and review routes into one
work-level queue. It does not replace `corpus/papers.csv`, and it does not turn
a provisional screen into verified evidence.

## Outputs

| File | Unit | Purpose |
| --- | --- | --- |
| `review_candidate_routes.csv` | route record | Preserves every search, targeted, venue, peer-first, canonical, and exclusion occurrence after identifier resolution. |
| `review_candidate_queue.csv` | canonical work | Gives one review row per deduplicated work, with every contributing route and the current ledger decision. |
| `review_decision_ledger.csv` | canonical work | Persistent decision source. A named reviewer, review date, `manual:` source, or `locked=yes` protects an adjudication from automatic replacement. |
| `review_primary.csv` | canonical work | Direct interaction-security works selected by the strongest available decision. |
| `review_secondary.csv` | canonical work | Security-relevant or contextual works that should not be counted as strict primary evidence. |
| `review_exclude.csv` | canonical work | Works explicitly outside the review boundary. |
| `review_pending.csv` | canonical work | Unresolved works. Pending rows never enter a final set. |
| `review_identifier_aliases.csv` | public identifier | DOI and arXiv aliases retained for each resolved work. |
| `review_set_summary.csv` | aggregate | Decision and contribution-category counts for the full queue, targeted route, and canonical corpus. |
| `review_set_manifest.json` | build | Counts, source hashes, precedence rules, and route coverage. |

The queue also carries the current and recommended paper categories from the
canonical review records. These category fields remain separate from the
primary, secondary, and exclude decision because a paper's contribution type
is not its evidence status.

## Targeted route

The targeted route contains 318 cutoff-eligible candidate records. It is the
325-work broad screen with the seven records explicitly reviewed as
`recommended_scope=adjacent` removed. Two additional rows have the older gate
label `adjacent_not_core` but are retained because their reviewed scope is
`security_relevant`. The 318 route records resolve to 317 works because two
MAGPIE preprints are versions of the same canonical work. Both route records
remain visible in `review_candidate_routes.csv`.

## Decision precedence

A route is evidence about how a work was found. It is not automatically a final
classification. The builder applies the following order:

1. a persistent human adjudication in `review_decision_ledger.csv`;
2. canonical source-review scope;
3. the reviewed peer-first gate;
4. a structured exclusion;
5. the full-text search screen;
6. weaker discovery routes.

Broad, targeted, and venue membership alone cannot promote a work to primary.
A weaker primary suggestion also cannot override a stronger secondary or
exclude decision. Equal-strength conflicts are returned to pending rather than
resolved by guesswork.

To record a human decision, set `decision`, `rationale`, `reviewer`, and
`reviewed_at`, then set `locked=yes`. Generated rows without those markers are
refreshed when the source ledgers change. Historical rows that no longer match a
candidate are retained and marked as orphaned instead of being silently
removed.

## Identifier resolution

Matching prefers a canonical paper ID, then arXiv and DOI identifiers, then an
exact normalized title. `identifier_alias_overrides.csv` records the small
number of source-specific metadata corrections needed to resolve a known work.
It currently preserves the official ACL Anthology DOI for Chain-of-Query and
the current arXiv titles for two targeted-gap records with obsolete working
titles. An unresolved public-identifier collision stops the build.

## Rebuild and validate

```bash
python3 artifact/search/v2/build_review_sets.py --write
python3 artifact/search/v2/build_review_sets.py --check
python3 tests/test_review_sets_v2.py
```

`--check` performs a deterministic rebuild and fails when a generated file is
stale. The regression test checks set disjointness, targeted-route visibility,
version merging, identifier ownership, source precedence, and persistence of
explicit human adjudication.
