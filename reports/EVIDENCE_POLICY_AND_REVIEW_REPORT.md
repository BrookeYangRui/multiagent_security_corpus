# Evidence Policy and Review Status

The active corpus contains 142 canonical academic works from the authoritative
pre-`2026-07-01` source package.

## Evidence Strata

| Evidence level | Works |
| --- | ---: |
| Assistant source reviewed, pending author signoff | 90 |
| Source reviewed, pending author signoff | 18 |
| Official metadata and abstract screened | 19 |
| Full-text scope screened | 7 |
| Official arXiv metadata and abstract screened | 3 |
| Boundary full-text screened | 2 |
| Blocked pending exact source | 1 |
| Official workshop metadata and full text screened | 1 |
| Claim-level review required | 1 |

These labels come from the frozen source package plus fail-loud active-view
overrides for later source resolution. None implies named human signoff unless
that signoff is separately recorded.

## Active Review Coverage

The three disjoint queues jointly cover all 142 works:

| Queue | Works |
| --- | ---: |
| Load bearing | 20 |
| Standard attack | 45 |
| Cross category | 77 |

`reviews/universal/active_source_review.csv` has one row per canonical paper.
The historical 114-work packet and superseded 181-candidate AI review are not
part of the current export. Their review state is represented by the active
rows and is recoverable from repository history; neither is a current evidence
denominator.

## Claim Use

Paper placement and `primary_category` do not prove a claim. Attack, defense,
metric, guarantee, and limitation statements still require locatable canonical
full-text evidence. Abstract-only records cannot carry technical extraction,
and imported metadata-level notes remain `agent_unverified`.
