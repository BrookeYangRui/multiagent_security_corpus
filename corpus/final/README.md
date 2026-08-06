# Final exports

These files freeze the literature boundary at `2026-07-01 00:00 UTC`.

- `all_relevant_papers.csv` is the broad paper-level export. It includes direct
  security papers and explicitly marked security-relevant boundary work.
- `peer_reviewed.csv` contains formal conference and journal publications.
  Non-archival workshop papers remain visible in the broad export and are not
  silently promoted to this subset.
- `venue_coverage.csv` reports the normalized conference and journal coverage
  of that subset.
- `non_peer_citations_gt_10.csv` contains non-peer work with a Semantic Scholar
  citation count strictly greater than 10 at the recorded snapshot.
- `strongly_related_soks.csv` separates direct MAS reviews from broader agentic
  comparators.

The citation threshold is a retrieval gate, not a claim of scientific quality.
Paper counts use canonical works; preprint and published versions are merged.
The repository does not claim that an open-web search can prove mathematical
completeness. Search completeness instead means that the documented databases,
venue proceedings, keyword families, and snowballing passes reached closure at
the cutoff. Records lacking a primary source are not silently included.
