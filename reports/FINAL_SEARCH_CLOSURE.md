# Final Search Closure

Literature cutoff: `2026-07-01 00:00 UTC`

The user-designated source of truth is the package preserved under
`corpus/source_packages/2026-07-01/`. Its 142-work academic export is the sole
canonical paper denominator. Earlier 107-, 114-, 129-, 139-, and 181-work views
are superseded and remain only in explicitly named archive directories or audit
ledgers.

## Current Counts

| Set | Works |
| --- | ---: |
| Canonical academic corpus | 142 |
| Archival peer-reviewed subset | 90 |
| Non-peer citation `>10` retained subset | 19 |
| Core security | 92 |
| Security relevant | 50 |
| Attack primary | 58 |
| Defense primary | 40 |
| Evaluation primary | 34 |
| Survey primary | 7 |
| General primary | 3 |

The 142 works each have a `corpus/papers.csv` row, one BibTeX entry, and one
paper note. Newly generated metadata-level notes remain `agent_unverified` and
must not be treated as claim-level human review.

## Supporting Evidence

| Set | Records | Denominator status |
| --- | ---: | --- |
| SoK-related synthesis view | 14 | Supporting view; seven overlap the 142 |
| CVEs and advisories | 52 | Never part of the paper denominator |
| Industry and institutional reports | 16 | Never part of the paper denominator |

The SoK-related count must not be added to 142. Search catalogs, broad screens,
exclusions, historical adjudication, and archived review packets remain audit
records rather than current included-paper lists.

## Version and Evidence Policy

The canonical unit is a work, not a version. Published and preprint versions
are merged under one `paper_id`. The final export preserves the package's
cutoff basis, official URLs, and publication status; evidence level and locator
are projected from the fail-loud active source-review view so later source
resolution does not rewrite the frozen package. Metadata-only, abstract-only,
blocked, and pending-signoff states remain visible and are never promoted to
human-verified status by import.
