# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Search
cutoff: `2026-07-01 00:00 UTC`.

## Canonical corpus

| File | Count |
| --- | ---: |
| `corpus/papers.csv` | 142 canonical academic works |
| `corpus/final/all_relevant_papers.csv` | 142 canonical academic works |
| `corpus/final/peer_reviewed.csv` | 90 archival conference or journal works |
| `corpus/final/non_peer_citations_gt_10.csv` | 19 retained non-peer works with citations > 10 |
| `corpus/final/yearly_distribution.csv` | 4 annual rows for trend plotting |
| `reports/figures/corpus_growth_by_year.svg` | Annual and cumulative growth figure |
| `sok_related/papers.csv` | 14-work supporting synthesis view; overlaps the corpus |
| `corpus/evidence/cves.csv` | 52 CVEs and advisories |
| `corpus/evidence/industry_reports.csv` | 16 reports |

Start with `reports/FINAL_SEARCH_CLOSURE.md` for the search sources, screening
rules, cutoff handling, and evidence limitations. The 2,182-row search catalog
and the 325-work broad screen under `corpus/sets/` are audit and candidate
ledgers, not included-paper denominators. `corpus/papers.csv` is the sole
canonical included-paper list; it is imported from the authoritative 142-work
package under `corpus/source_packages/2026-07-01/`. Survey and SoK works retained
by that package remain in the 142-work denominator and are filed under
`papers/surveys/`. The 14-work `sok_related/` view is supporting synthesis
metadata and must not be added to 142 because seven records overlap.

Paper notes and source reviews remain unverified until named human signoff.
CVEs and industry material never enter an academic-paper denominator.

## Validate

```bash
python3 scripts/import_authoritative_142.py
python3 scripts/build_universal_review_queue.py
python3 scripts/build_corpus_sets.py
python3 scripts/build_final_exports.py
python3 scripts/validate_corpus.py
python3 scripts/validate_corpus_sets.py
```
