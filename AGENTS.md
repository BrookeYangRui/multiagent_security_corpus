# Corpus Maintenance Protocol

## Single authoritative corpus

There is one active manuscript corpus: **189 works**.

* `corpus/set1_core.csv`: 92 mature in-scope works
* `corpus/set2_emerging.csv`: 97 emerging in-scope works
* `papers/index.csv`: one-to-one materialized view of the same 189 works

Do not restore superseded denominators or removed screening artifacts to the active tree.

## Scope and maturity

Apply `CORPUS_SET_POLICY.md`. MAS must be the security object or the security consequence must materially depend on inter-agent interaction. Using multiple agents merely as a generic detector, red-team method, alignment method, workflow, or application architecture is insufficient by itself. The frozen literature cutoff is `2026-07-01`.

Set 1 uses `peer_reviewed == yes OR frozen_citation_count >= 10`; Set 2 contains the remaining in-scope works.

## Paper notes

Every active work appears exactly once under `papers/` and in `papers/index.csv`. Current dominant-contribution totals are **46 attacks, 80 defenses, 44 evaluations, 12 general works, and 7 surveys**.

A work outside the active 189 must not have a paper note under `papers/`. `sok_related/` is a supporting comparator view and is never added to the corpus denominator.

## Validation

Run `scripts/validate_all.sh`. Validation must enforce Set 1 = 92, Set 2 = 97, total = 187, the 44/80/44/12/7 contribution partition, exact paper-index membership, and exactly 187 non-README paper notes.
