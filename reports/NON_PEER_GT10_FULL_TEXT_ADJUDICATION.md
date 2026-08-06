# Non-Peer Citation-Gate Full-Text Adjudication

Cutoff: `2026-07-01`  
Citation snapshot: `2026-08-06`  
Citation admission rule: Semantic Scholar `citationCount > 10`

## What Changed

The 19 candidates previously labeled `pending_full_text_adjudication` were
reviewed from primary full text. Citation count was used only to trigger review.
Each decision applied the five frozen gates: multi-agent boundary, explicit
interaction, direct security relevance, interaction dependence, and locatable
full-text evidence.

One candidate, *Cohesive Conversations*, has an official COLM 2024 conference
record and was moved to the peer-reviewed backbone. The current peer-first frame
therefore contains 94 peer-reviewed works and 21 non-peer works with more than
10 citations. The total taxonomy-candidate queue remains 115 works.

## Decisions for the 19-Work Batch

| Decision | Works |
| --- | ---: |
| Provisional strict-core pass, author signoff required | 7 |
| Security-relevant contextual evidence | 3 |
| Adjacent, not strict security core | 9 |
| Still pending full-text adjudication | 0 |

### Provisional Strict-Core Pass

- *When Persuasion Overrides Truth in Multi-Agent LLM Debates*
- *SentinelAgent*
- *SAFEFLOW*
- *1-2-3 Check*
- *The Sum Leaks More Than Its Parts*
- *Institutional AI*
- *Taming Various Privilege Escalation in LLM-Based Agent Systems*

These works passed all five gates. They remain provisional because the source
review has not received named human signoff and the required canonical paper
note, BibTeX, and `papers.csv` records have not all been created.

### Contextual, Not Strict Core

- *Multi-Agent Large Language Models for Conversational Task-Solving*
- *Revisiting Multi-Agent Debate as Test-Time Scaling*
- *WOLF*

These contain safety, deception, or interaction-relevant evidence, but security
is not a sufficiently explicit paper-level contract for automatic strict-core
admission. Security claims can still be extracted at claim level.

### Adjacent, Not Strict Core

- *Cohesive Conversations*
- *Towards Collaborative Intelligence*
- *CoopetitiveV*
- *CodeCoR*
- *Debate Only When Necessary*
- *Chasing Moving Targets with Online Self-Play Reinforcement Learning*
- *VeriMoA*
- *Maestro*
- *Agent Drift*

Most of these study accuracy, efficiency, code correctness, dialogue quality,
or non-adversarial reliability. *Chasing Moving Targets* is direct safety work,
but its attacker and defender are self-play roles used to train one protected
model rather than separately addressable deployed agent cores.

## Publication-Status Checks

- *Cohesive Conversations*: official COLM 2024 conference paper; promoted to
  peer-reviewed.
- *CoopetitiveV*, *Revisiting Multi-Agent Debate*, *Chasing Moving Targets*, and
  *WOLF*: official workshop listings were found; these were not promoted to the
  archival peer-reviewed backbone.
- *1-2-3 Check* and *VeriMoA*: their PDFs name 2026 conferences, but no indexed
  archival proceedings record was located during this check. Their status stays
  `non_peer_or_unverified` conservatively.

## Cutoff-Safe Versions

The review used the latest version available no later than the cutoff. In
particular, it used `CodeCoR` arXiv v1 and *Chasing Moving Targets* arXiv v1;
their latest revisions were posted after `2026-07-01` and were not used to make
the frozen corpus decision.

## Files

- Candidate universe: `corpus/final/non_peer_citations_gt_10.csv`
- At-or-above sensitivity list: `corpus/final/non_peer_candidates_citations_gte_10.csv`
- Canonical intersection: `corpus/final/non_peer_included_citations_gt_10.csv`
- Per-paper evidence: `reviews/citation_gate/non_peer_gt10_full_text_adjudication.csv`

This closes the 19-work non-peer full-text queue. It does not close the separate
53-work peer-reviewed source-review queue shown in
`corpus/sets/03_taxonomy_eligible/taxonomy_candidates.csv`.
