# Attack Review Queue

`reviews/queues/standard_attack.csv` contains 45 standard attack-track review
records. Together with 20 load-bearing and 77 cross-category records, the three
mutually exclusive queues cover all 142 canonical works. These are review
routes, not accepted attack-paper denominators: the frozen imported placement
field currently labels 58 works attack-primary, and source signoff may move a
work between attack, defense, and evaluation roles.

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
promote its review depth to the load-bearing protocol without duplicating its
row across queues.

## Status

Use `pending_human_review`, `in_review`, or `completed`. A completed row requires
a reviewer and an adjudication note. Updating the queue alone does not change
the paper's `verification_status`; set that status only to the level actually
verified.
