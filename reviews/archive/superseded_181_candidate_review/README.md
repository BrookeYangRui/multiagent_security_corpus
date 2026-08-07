# Superseded 181-Candidate Review Packet

This packet is retained only as adjudication history. It was superseded on
2026-08-07 when the user designated the packaged 142-work export as the sole
canonical academic corpus. Nothing in this directory contributes to current
paper counts, category counts, review queues, or final exports.

This packet is the human-review denominator for works first available before
`2026-07-01 00:00 UTC`.

## Candidate Count

- Current structured corpus: 107
- Peer-reviewed broad inclusions: 94
- Non-peer or unverified broad inclusions with Semantic Scholar citations
  greater than or equal to 10 at the `2026-08-06` snapshot: 25
- Broad/citation-gate candidates: 119
- Overlap between the current corpus and broad/citation-gate candidates: 45
- Additional broad/citation-gate candidates not in the current corpus: 74
- Total unique candidates for human review: 181

The number 181 is a candidate count, not a claim that all 181 works are
multi-agent security papers. The final paper count is the number of rows that
named human reviewers mark `include` after reading the canonical full text.

The four separately maintained SoK-related works are not part of this packet.

## Files

- `mas_security_human_review.csv`: portable master review table
- `mas_security_human_review.xlsx`: workbook with instructions, filters,
  frozen headers, dropdowns, and a live decision summary

## Human Decision Rule

Read the canonical full text and answer all five gates:

1. Does the work study a multi-agent system boundary?
2. Is there explicit interaction among separately addressable agents?
3. Is security a direct property, violation, defense, or evaluation?
4. Does the security claim materially depend on multi-agent interaction?
5. Is the decision supported by locatable canonical full-text evidence?

Use `include` only when the paper belongs in the structured multi-agent
security corpus. Use `exclude` when it does not. Use `unclear` when escalation
or a second reviewer is required.

Every completed decision requires the reviewer name, review date, canonical
version reviewed, evidence locations, and an adjudication note. Existing corpus
and prior-review columns are context only; they are not human decisions in this
packet.

## Counting the Result

After review, filter `human_final_decision` to `include`. That row count is the
human-adjudicated answer to how many pre-cutoff multi-agent security papers are
in this candidate frame. Deduplicate publication and preprint versions as one
canonical work before finalizing the count.
