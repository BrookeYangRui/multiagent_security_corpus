# Load-Bearing Review Queue

`load_bearing_review_queue.csv` contains 20 papers that support the attack
landscape's central categories and quantitative claims. The queue covers
propagation, availability, collusion, confidentiality, communication, collective
decision integrity, Byzantine faults, control flow, compositional authority,
and protocol identity.

The initial automated precheck confirmed only that a primary source was
recorded, an Evidence table was populated, and a preliminary scope label was
present. A subsequent source-level review examined all 20 papers and recorded
55 corrections under `reviews/load_bearing/`.

Eighteen rows are now `source_reviewed_pending_author_signoff`. Two remain
blocked: Flooding awaits final-journal author and locator verification, while
A2ASecBench awaits exact final-PDF page, figure, and table locators. No paper was
upgraded from `agent_unverified`.

Author or designated-reviewer signoff must check:

1. canonical title, authors, venue, DOI, and version;
2. multi-agent dependency and attacker capability;
3. each evidence locator against the cited source;
4. evaluation unit, denominator, baseline, and reported result;
5. final `primary_category` and `scope_relation`.

After signoff, record the reviewer and adjudication note, then update the paper's
verification state in `papers.csv` only to the level actually checked. Do not
bulk-upgrade records from this queue.
