# Corpus Maintenance Protocol

These rules apply to every contribution in this repository.

## Single authoritative corpus

There is one active manuscript corpus: **201 works**.

* `corpus/set1_core.csv`: 96 mature in scope works
* `corpus/set2_emerging.csv`: 105 emerging in scope works
* `papers/index.csv`: one to one materialized view of the same 201 works

Do not restore older corpus denominators, generated membership ledgers, Set 3 tables, screened out tables, review universes, migration outputs, or historical reconstruction scripts to the active tree. Git history already preserves those states.

## Scope and maturity

A work belongs to the active corpus only when it satisfies the scope gate in `CORPUS_SET_POLICY.md`: at least two separately addressable LLM backed agents or principals, a material inter agent relation, a concrete security property or evaluation, and source evidence sufficient for the membership decision.

Set 1 uses the frozen maturity rule `peer_reviewed == yes OR frozen_citation_count >= 10`. Set 2 contains the remaining in scope emerging work. Interaction dependence is an evidence characterization, not a membership gate.

The signed 96 plus 105 partition is frozen for the current manuscript. Any future membership correction must be an explicit corpus revision. Never silently regenerate membership from superseded search or review artifacts.

## Paper notes

Every active work must appear exactly once under `papers/` and exactly once in `papers/index.csv`.

Paper notes are organized by dominant contribution and publication venue:

```text
papers/
  attacks/<venue>/
  defenses/<venue>/
  evaluations/<venue>/
  general/<venue>/
  surveys/<venue>/
```

The signed contribution totals are 42 attacks, 94 defenses, 44 evaluations, 11 general works, and 10 surveys.

When editing a note:

1. Read the primary paper when technical claims are changed.
2. Preserve the canonical title, authors, publication status, DOI, arXiv identifier, and source URLs.
3. Do not invent missing metadata, evidence locations, results, limitations, or relationships.
4. Keep source claims distinct from cross paper interpretation.
5. Preserve the final corpus status banner and the note path recorded in `papers/index.csv`.

A work outside the final 201 must not have a paper note under `papers/`.

## Version and identity handling

Use one canonical record for a preprint and its published version. Prefer the published identity when one exists and retain the preprint URL only as supporting access information when useful.

Do not create separate active corpus rows for workshop, preprint, conference, journal, SSRN, or repository copies of the same work.

## Supporting material

`corpus/evidence/` contains non paper evidence such as CVEs, industry reports, and standards. These files never contribute to the 201 paper denominator.

`sok_related/` is a supporting comparator view for related SoKs and surveys. It is not an additional corpus and its count must never be added to 201.

`related_work/` contains synthesis notes. Any numerical statement about the manuscript corpus must be derived from the final 201 view, not from historical corpus states.

## Validation

Before committing, run:

```bash
scripts/validate_all.sh
```

Validation must enforce all of the following:

1. Set 1 contains exactly 96 rows.
2. Set 2 contains exactly 105 rows.
3. The combined active corpus contains exactly 201 unique work keys.
4. Contribution totals are exactly 42, 94, 44, 11, and 10.
5. `papers/index.csv` contains exactly the same 201 work keys.
6. `papers/` contains exactly 201 non README paper notes, grouped by contribution and venue.
7. Superseded corpus artifacts are absent from the active `corpus/` tree.

If a proposed change violates these invariants, stop and treat it as a deliberate corpus revision rather than a routine edit.
