# Attack Review Queue

`attack_review_queue.csv` contains the 42 attack-primary papers not selected for
the initial load-bearing review. Together with
`load_bearing_review_queue.csv`, it covers all 55 attack-primary papers. After
source-review reclassification, the load-bearing queue includes 13 attack papers
plus seven defense/evaluation papers;
`attack_review_queue.csv` contains the remaining attack papers as priorities
21-62.

## Standard Review

For each paper, verify:

1. title, authors, venue, year, DOI, URL, and accessed version;
2. that separately addressable LLM-backed agents interact;
3. whether `core_security` or `security_relevant` is justified;
4. whether the primary category is attack rather than defense or evaluation;
5. adversary position, capability, preconditions, and mechanism;
6. the violated system-level property and reported impact;
7. agent count, topology, baselines, metric definition, and denominator;
8. source locations for every load-bearing claim in the paper note.

If a paper supports a headline finding or exposes a disputed classification,
promote it to the load-bearing protocol and perform a full evidence review.

## Status

Use `pending_human_review`, `in_review`, or `completed`. A completed row requires
a reviewer and an adjudication note. Updating the queue alone does not change
the paper's `verification_status`; set that status only to the level actually
verified.
