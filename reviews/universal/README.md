# Universal Source Review Packet

This directory preserves the original imported 114-work packet and the active
107-work research-corpus view derived from it.

## Files

```text
universal_114_source_review.csv              one consolidated row per work
universal_source_review_corrections.csv      231 field-level corrections
UNIVERSAL_114_SOURCE_REVIEW.xlsx             original workbook representation
active_source_review.csv                     active 107-paper research view
active_source_review_corrections.csv         210 active corrections
```

The original packet is immutable review history. The active view excludes seven
survey records that are now handled by the separate SoK-related screening
boundary. Its tracks contain 20 load-bearing, 42 standard attack-primary, and
45 cross-category research papers.

## Verification Status

These records are source-reviewed proposals awaiting named author signoff.
They are not `metadata_verified`, `evidence_verified`, or `fully_reviewed`.
Blocked source and metadata states must remain blocked until the canonical
source resolves them.

Do not bulk-copy `recommended_category` into `primary_category`: the review
field is multi-valued and contains secondary roles. Apply corrections
individually and preserve the adjudication history.

See `reports/EVIDENCE_POLICY_AND_REVIEW_REPORT.md` for counts, interpretation,
and the remaining review gap.
