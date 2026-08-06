# Targeted Attack Gap Search

`targeted_attack_gap_search.csv` records the 2026-08-06 gap check for denial of
service, collective goal drift, identity or Sybil attacks, and shared-memory or
shared-tool poisoning. Searches combined the frozen systematic ledger with
title, abstract, and full-text checks against arXiv, DBLP, and official venue
pages. The publication cutoff remains 2026-07-01.

An entry is included only when the security effect depends on interaction among
separate LLM-backed agent cores. Papers that merely deploy multiple defensive
agents, attack one ordinary agent, report projected simulations, or only propose
an unevaluated protocol remain excluded or are assigned another primary
category.

The identity/Sybil row is a negative result, not proof that no such work exists.
It means that this bounded pre-cutoff search found no verified attack-primary
paper demonstrating identity minting or a Sybil attack against an LLM-MAS.
