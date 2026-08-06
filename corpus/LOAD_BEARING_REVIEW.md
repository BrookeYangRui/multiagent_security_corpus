# Load-Bearing Review Queue

`load_bearing_review_queue.csv` contains 20 papers that support the attack
landscape's central categories and quantitative claims. The queue covers
propagation, availability, collusion, confidentiality, communication, collective
decision integrity, Byzantine faults, control flow, compositional authority,
and protocol identity.

The automated precheck confirms only that a primary source is recorded, an
Evidence table is populated, and the paper currently satisfies the
`core_security` scope rule. It does not verify that a source location supports a
claim. Every row therefore remains `pending_human_review` until a human checks:

1. canonical title, authors, venue, DOI, and version;
2. multi-agent dependency and attacker capability;
3. each evidence locator against the cited source;
4. evaluation unit, denominator, baseline, and reported result;
5. final `primary_category` and `scope_relation`.

After review, record the reviewer and adjudication note, then update the paper's
verification state in `papers.csv`. Do not bulk-upgrade records from this queue.
