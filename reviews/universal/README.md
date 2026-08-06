# Universal Source Review Packet

This directory preserves the imported source-review results for the 114 works
in the canonical structured corpus.

## Files

```text
universal_114_source_review.csv              one consolidated row per work
universal_source_review_corrections.csv      231 field-level corrections
standard_and_cross_category_source_review.csv combined 42 + 52 review tracks
universal_review_queue_reviewed.csv          reviewed 114-work master queue
attack_review_queue_reviewed.csv             reviewed 42-work attack queue
cross_category_review_queue_reviewed.csv     reviewed 52-work cross-category queue
UNIVERSAL_114_SOURCE_REVIEW.xlsx             original workbook representation
```

The 20 load-bearing rows are included in the consolidated review and are not a
fourth independent queue. The three tracks are 20 load-bearing, 42 standard
attack-primary, and 52 cross-category works.

## Verification Status

These records are source-reviewed proposals awaiting named author signoff.
They are not `metadata_verified`, `evidence_verified`, or `fully_reviewed`.
Blocked source and metadata states must remain blocked until the canonical
source resolves them.

Do not bulk-copy `recommended_category` into `primary_category`: the review
field is multi-valued and contains secondary roles. Apply corrections
individually and preserve the adjudication history.

See `corpus/EVIDENCE_POLICY_AND_REVIEW_REPORT.md` for counts, interpretation,
and the remaining review gap.
