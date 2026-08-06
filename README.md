# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. The frozen
search cutoff is `2026-07-01`; citation counts use the `2026-08-06` Semantic
Scholar snapshot.

## Corpus Sets

| Set | Current count | Purpose |
| --- | ---: | --- |
| Search catalog | 2,182 records | Retrieval, screening, exclusions, and PRISMA flow |
| Broad included | 325 works | Broad interaction-security landscape after version deduplication |
| Taxonomy candidates | 115 works | 93 peer-reviewed works plus 22 non-peer works with citations `>10` |
| Adjacent/contextual | 41 reviewed works | Boundary, reliability, safety, governance, and background evidence |
| Analysis eligibility | 798 pending decisions | Seven audit contracts applied to 114 structured works |

`taxonomy_candidates` is not a final denominator. Current source review yields
30 provisional core passes awaiting author signoff, 12 contextual decisions,
one source blocker, and 72 pending full-text adjudications.

## Start Here

```text
corpus/sets/SET_MANIFEST.csv                    authoritative counts
corpus/sets/01_search_catalog/                  retrieval and screening
corpus/sets/02_broad_included/                  325 canonical broad inclusions
corpus/sets/03_taxonomy_eligible/               strict-core adjudication queue
corpus/sets/04_adjacent_contextual/             reviewed contextual works
corpus/sets/05_analysis_specific/               claims, contracts, and audit sets
corpus/papers.csv                               114 structured paper records
corpus/references.bib                           canonical references
papers/                                         structured paper notes
reviews/universal/                              114-work source review and corrections
reviews/queues/                                 expert signoff queues
reports/                                        evidence and threshold decisions
```

Corpus counts are by work. Taxonomy and synthesis are claim-level. Every audit
must report its own eligibility rule, final `n`, peer-reviewed `n`, and
non-peer `n`.

## Validate

```bash
python3 scripts/build_peer_first_eligibility.py --check
python3 scripts/build_corpus_sets.py
python3 scripts/validate_corpus.py
```

Paper notes and imported source reviews remain unverified until named human
signoff. CVEs, industry reports, and standards use separate evidence datasets
and never enter the paper denominator.
