# Universal Source Review Packet

This directory preserves the imported source-review results for the 114 works
in the canonical structured corpus.

## Files

```text
universal_114_source_review.csv              one consolidated row per work
universal_source_review_corrections.csv      231 field-level corrections
UNIVERSAL_114_SOURCE_REVIEW.xlsx             original workbook representation
```

The removed per-track exports duplicated the consolidated CSV. The three source
tracks remain visible in its `review_track` field: 20 load-bearing, 42 standard
attack-primary, and 52 cross-category works.

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
