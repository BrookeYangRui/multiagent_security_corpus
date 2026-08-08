# Search Catalog

`search_catalog.csv` contains 2,182 transitively deduplicated search entities
from 6,105 OpenAlex and Semantic Scholar source-query memberships. It preserves
query-family provenance, staged decisions, and reasons for exclusion or
non-resolution. The paper artifact separately releases the prospective literal
queries, request URLs/order, retrieval-time response-body digests, an
abstract-hash membership ledger, and a machine-checked provenance manifest.
Parsed API payloads and third-party abstract text are withheld pending
source-license review; original HTTP bytes and headers were not preserved.

Final screening outcomes include 326 inclusion records and 343 unresolved
records. Inclusion records are canonicalized at work level in
`../02_broad_included/broad_included.csv`; the search catalog itself preserves
entity-level screening history and is not a taxonomy denominator.

`canonical_bridges.csv` binds repository notes that did not match the search
ledger mechanically. `targeted_gap_search.csv` records the directed attack-gap
check. `post_cutoff_papers.csv` is an isolated watchlist.
