# Search Catalog

`search_catalog.csv` contains 2,182 retrieval and screening records from the
frozen systematic search. It preserves query provenance, staged decisions, and
reasons for exclusion or non-resolution.

Final screening outcomes include 326 inclusion records and 343 unresolved
records. Inclusion records are canonicalized at work level in
`../02_broad_included/broad_included.csv`; the search catalog itself preserves
record-level history and is not a taxonomy denominator.

`canonical_bridges.csv` binds repository notes that did not match the search
ledger mechanically. `targeted_gap_search.csv` records the directed attack-gap
check. `post_cutoff_papers.csv` is an isolated watchlist.
