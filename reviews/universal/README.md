# Universal Source Review Packet

This directory preserves the original imported 114-work packet and the active
142-work canonical view derived from the authoritative source package.

## Files

```text
universal_114_source_review.csv              one consolidated row per work
universal_source_review_corrections.csv      231 field-level corrections
UNIVERSAL_114_SOURCE_REVIEW.xlsx             original workbook representation
active_source_review.csv                     active 142-work canonical view
active_source_review_corrections.csv         active historical corrections
active_source_review_correction_overrides.csv audited active-view refinements
```

The original packet is immutable review history. The active view includes the
seven survey-primary records retained by the authoritative package. Its tracks
contain 20 load-bearing, 45 standard attack-primary, and 77 cross-category
works. The 14-work SoK-related file is a supporting view with intentional
overlap, not an additional denominator.

The override ledger records refinements made after the historical packet. The
builder verifies each previous value before applying its active replacement, so
upstream history remains intact and unexpected source changes fail loudly.

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
