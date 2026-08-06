# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Search
cutoff: `2026-07-01 00:00 UTC`.

## Canonical corpus

| File | Count |
| --- | ---: |
| `corpus/papers.csv` | 114 papers |
| `corpus/final/all_relevant_papers.csv` | 114 papers |
| `corpus/final/peer_reviewed.csv` | 75 conference or journal papers |
| `corpus/final/non_peer_citations_gt_10.csv` | 3 canonical papers |
| `corpus/evidence/cves.csv` | 18 CVEs |
| `corpus/evidence/industry_reports.csv` | 8 reports |

Start with `reports/FINAL_SEARCH_CLOSURE.md` for the search sources, screening
rules, cutoff handling, and evidence limitations. The 2,182-row search catalog
and the 325-work broad screen under `corpus/sets/` are audit and candidate
ledgers, not included-paper denominators. `corpus/papers.csv` is the sole
canonical included-paper list; every final export must be a subset of its 114
paper IDs.

Paper notes and source reviews remain unverified until named human signoff.
CVEs and industry material never enter an academic-paper denominator.

## Validate

```bash
python3 scripts/build_final_exports.py
python3 scripts/validate_corpus.py
python3 scripts/validate_corpus_sets.py
```
