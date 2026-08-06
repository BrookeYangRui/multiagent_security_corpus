# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Search
cutoff: `2026-07-01 00:00 UTC`.

## Final exports

| File | Count |
| --- | ---: |
| `corpus/final/all_relevant_papers.csv` | 139 papers |
| `corpus/final/peer_reviewed.csv` | 90 conference or journal papers |
| `corpus/final/non_peer_citations_gt_10.csv` | 19 papers |
| `corpus/evidence/cves.csv` | 18 CVEs |
| `corpus/evidence/industry_reports.csv` | 8 reports |
| `corpus/final/strongly_related_soks.csv` | 8 reviews and comparators |

Start with `reports/FINAL_SEARCH_CLOSURE.md` for the search sources, screening
rules, cutoff handling, and evidence limitations. The 2,182-row search catalog
under `corpus/sets/01_search_catalog/` is an audit log, not a paper denominator.

Paper notes and source reviews remain unverified until named human signoff.
CVEs and industry material never enter an academic-paper denominator.

## Validate

```bash
python3 scripts/build_final_exports.py
python3 scripts/validate_corpus.py
python3 scripts/validate_corpus_sets.py
```
