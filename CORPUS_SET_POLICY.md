# Corpus policy

## Scope gate

A work enters the active corpus only if all of the following hold:

1. It studies at least two separately addressable LLM-backed agents or principals.
2. A material inter-agent relation or interaction path is present.
3. It studies a concrete security property, attack, defense, guarantee, adversary, or security evaluation.
4. The security claim is about the interacting system or materially depends on an inter-agent relation; merely using multiple agents as a generic security or safety instrument is not enough.
5. Source evidence is sufficient to support the membership decision.
6. The work was publicly available by the frozen literature cutoff `2026-07-01`.

Interaction-dependence strength remains an evidence characterization, not a separate membership tier. Covert coordination, cross-agent context control, and cross-agent action control can satisfy the scope gate when the protected or adversarial property is relational.

Broad agent-security surveys may remain in `sok_related/` without entering the active evidence corpus.

## Set 1 and Set 2

Set 1 uses `peer_reviewed == yes OR frozen_citation_count >= 10`. Set 2 contains the remaining in-scope emerging work. The current corpus is **107 Set 1 + 82 Set 2 = 189 works**.
