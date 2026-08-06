# Attack Corpus

This directory contains canonical notes for papers whose primary contribution is
an attack, adversarial failure, or attack-centered evaluation against an
LLM-based multi-agent system.

## Inclusion Boundary

A paper belongs here when the attack mechanism, violated property, or measured
impact materially depends on interaction among separately addressable agents.
Qualifying structures include communication, delegation, shared state,
collective decisions, distributed authority, membership, and orchestration.

Using several agents only to generate attacks against one isolated target model
does not qualify. General collaboration failures without a security, privacy,
robustness, misuse, or trust consequence are routed to another corpus category.

## Canonical Record Rules

- Keep one canonical record for each intellectual work.
- Prefer a published conference version, then a journal version, then the latest
  accessible preprint when no formal version is available.
- Merge workshops and preprints into a later formal version when the contribution
  is substantially the same.
- Record superseded and screened-out versions in
  `corpus/excluded_papers.csv` instead of counting them twice.
- Place the note under the canonical publication venue. Journal directories use
  a `journals_` prefix; arXiv-only work is under `arxiv/`.

## Evidence and Status

Every note records the accessed version, discovery path, and source locations for
important claims. Publication status is checked against an official venue or
publisher source and a second metadata source when available. Records prepared
through automated extraction remain `agent_unverified` until a human verifies
them.

Some attack papers also introduce benchmarks, datasets, or evaluation harnesses.
Their canonical notes remain here; the evaluation corpus links to those records
rather than duplicating them.

Last publication-status audit: 2026-08-05.
