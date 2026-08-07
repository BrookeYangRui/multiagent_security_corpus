# Canonical Corpus Exports

These files freeze the literature boundary at `2026-07-01 00:00 UTC`.

- `all_relevant_papers.csv` is a generated view of all 142 canonical records in
  `../papers.csv`. It must have exactly the same `paper_id` set.
- `peer_reviewed.csv` contains 90 formal conference and journal publications.
  Non-archival workshop papers remain visible in the broad export and are not
  silently promoted to this subset.
- `venue_coverage.csv` reports the normalized conference and journal coverage
  of that subset.
- `yearly_distribution.csv` is the chart-ready annual trend table. It contains
  raw counts by primary category, scope, publication status, and cumulative
  corpus size; category and publication columns are mutually exclusive within
  each year.
- `non_peer_citations_gt_10.csv` and
  `non_peer_included_citations_gt_10.csv` contain the same 19 retained
  non-peer works with a Semantic Scholar citation count strictly greater than
  10 at the package snapshot.

The source snapshot is preserved under `../source_packages/2026-07-01/`.
Canonical records still require `papers.csv`, BibTeX, and paper-note records;
these exports are rebuilt from that record set and the authoritative snapshot.

The citation threshold is a retrieval gate, not a claim of scientific quality.
Paper counts use canonical works; preprint and published versions are merged.
The repository does not claim that an open-web search can prove mathematical
completeness. Search completeness instead means that the documented databases,
venue proceedings, keyword families, and snowballing passes reached closure at
the cutoff. Records lacking a primary source are not silently included.
