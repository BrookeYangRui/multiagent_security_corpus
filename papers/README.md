# Final 201 paper corpus

This directory contains exactly the **201 works** in the manuscript corpus: **96 Set 1** and **105 Set 2**.

Papers are organized first by dominant contribution and then by publication venue. The tree is materialized only from `corpus/set1_core.csv` and `corpus/set2_emerging.csv`.

| Contribution | Count | Directory |
| --- | ---: | --- |
| attack | 44 | [`attacks/`](attacks/) |
| defense | 85 | [`defenses/`](defenses/) |
| evaluation | 46 | [`evaluations/`](evaluations/) |
| general | 16 | [`general/`](general/) |
| survey | 10 | [`surveys/`](surveys/) |

The defense dominant-contribution labels were re-audited on `2026-08-23` under a stricter rule: a paper is defense-primary only when its main contribution is a mechanism, protocol, or system that prevents, detects, contains, or recovers from a concrete security threat or system-level security failure. Security-adjacent reliability, application architecture, and measurement work are not defense-primary merely because they include privacy, robustness, safety, or governance features.

[`index.csv`](index.csv) is the exact one-to-one mapping from all 201 corpus work keys to their current paper paths.
