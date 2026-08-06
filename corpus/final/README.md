# Canonical Corpus Exports

These files freeze the literature boundary at `2026-07-01 00:00 UTC`.

- `all_relevant_papers.csv` is a generated view of all 107 research records in
  `../papers.csv`. It must have exactly the same `paper_id` set.
- `peer_reviewed.csv` contains formal conference and journal publications.
  Non-archival workshop papers remain visible in the broad export and are not
  silently promoted to this subset.
- `venue_coverage.csv` reports the normalized conference and journal coverage
  of that subset.
- `non_peer_citations_gt_10.csv` contains all 21 current non-peer candidates
  with a Semantic Scholar citation count strictly greater than 10.
- `non_peer_candidates_citations_gte_10.csv` contains the 25 current non-peer
  candidates at or above 10 citations, including four records that do not pass
  the repository's strict `>10` admission threshold.
- `non_peer_included_citations_gt_10.csv` is the three-paper intersection of
  the `>10` candidate set and the canonical structured corpus.
- `../../reviews/citation_gate/non_peer_gt10_full_text_adjudication.csv` records
  the full-text decisions for the 19 candidates that were previously pending.

No paper may be introduced into the canonical corpus directly from this
directory. A paper first needs the
required `papers.csv`, BibTeX, and paper-note records; these exports are then
rebuilt from that canonical record set.

The citation threshold is a retrieval gate, not a claim of scientific quality.
Paper counts use canonical works; preprint and published versions are merged.
The repository does not claim that an open-web search can prove mathematical
completeness. Search completeness instead means that the documented databases,
venue proceedings, keyword families, and snowballing passes reached closure at
the cutoff. Records lacking a primary source are not silently included.
