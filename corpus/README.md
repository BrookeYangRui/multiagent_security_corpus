# Authoritative review corpus

These files are the only paper-population tables used by the SoK. The fixed 1 July 2026 review universe contains 2,217 deduplicated works: 303 primary, 177 secondary, 1,396 exclude, and 341 pending. The four decision files partition the queue exactly. Pending rows remain visible but never enter a final evidence set.

The targeted route contains 318 cutoff-eligible records resolving to 317 works. `primary.csv` and `secondary.csv` add a descriptive `broad_role` (`attack`, `defense`, `evaluation`, `other`). Existing source-reviewed/imported roles are preserved; rows without a prior role use a title-level rule and are marked `assistant_derived_pending_author_signoff`. Role coding never changes inclusion.

`papers/` contains partial source notes and is not a corpus-membership list. Historical source paths retained in provenance fields explain how a row entered review; the superseded broad-screen, canonical-142, taxonomy-115, and source-package tables themselves have been removed.
