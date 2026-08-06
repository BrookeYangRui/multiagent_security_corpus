# Load-Bearing Review Queue

`reviews/queues/load_bearing.csv` contains 20 papers that support the attack
landscape's central categories and quantitative claims. The queue covers
propagation, availability, collusion, confidentiality, communication, collective
decision integrity, Byzantine faults, control flow, compositional authority,
and protocol identity.

The initial automated precheck confirmed only that a primary source was
recorded, an Evidence table was populated, and a preliminary scope label was
present. The universal source review later examined all 20 papers. Their 55
corrections are retained as a subset of the 231-row ledger in
`reviews/universal/universal_source_review_corrections.csv`.

Eighteen rows are source-reviewed pending author signoff. Flooding remains
blocked on final-journal metadata. A2ASecBench remains blocked in the broader
review packet until exact final-PDF locators are confirmed. No paper was
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
