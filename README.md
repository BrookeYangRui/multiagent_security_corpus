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
| `corpus/sets/02_broad_included/yearly_distribution.csv` | 4 annual rows for all 325 broad-screen works |
| `reports/figures/broad_corpus_growth_by_year.svg` | Broad-screen annual and cumulative growth figure |
| `sok_related/papers.csv` | 14-work supporting synthesis view; overlaps the corpus |
| `corpus/evidence/cves.csv` | 52 CVEs and advisories |
| `corpus/evidence/industry_reports.csv` | 16 reports |

Start with `reports/FINAL_SEARCH_CLOSURE.md` for the search sources, screening
rules, cutoff handling, and evidence limitations. The 2,182-entity search catalog
and the 325-work broad screen under `corpus/sets/` are audit and candidate
ledgers, not included-paper denominators. `corpus/papers.csv` is the sole
canonical included-paper list; it is imported from the authoritative 142-work
package under `corpus/source_packages/2026-07-01/`. Survey and SoK works retained
by that package remain in the 142-work denominator and are filed under
`papers/surveys/`. The 14-work `sok_related/` view is supporting synthesis
metadata and must not be added to 142 because seven records overlap.
The source package remains immutable; source-backed canonical corrections are
recorded in `corpus/canonical_field_overrides.csv` and applied fail-loud during
import.

Paper notes and source reviews remain unverified until named human signoff.
CVEs and industry material never enter an academic-paper denominator.
Original annotations/data and scripts are released under the CC BY 4.0/MIT
terms in `LICENSE`; cited papers and bibliographic facts are not relicensed.

The cross-paper conclusions and manuscript-ready candidate statements are in
`reports/INSIGHTS.md`. They remain synthesis proposals pending the named human
signoff described by the evidence policy.

## Validate

```bash
scripts/validate_all.sh
```

Enable the tracked pre-push guard once per clone so a commit that fails the
same deterministic rebuild cannot reach GitHub:

```bash
git config core.hooksPath .githooks
```
