# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Frozen manuscript corpus

The USENIX 2027 SoK manuscript-facing corpus is frozen on `2026-08-18` and corrected by named classification signoff on `2026-08-21`. The authoritative counts are **Set 1 = 96**, **Set 2 = 105**, **Set 3 = 463**, and **screened out = 1,550**. Set 1 and Set 2 together form the **201-work MAS-security corpus**.

Corpus membership and the frozen citation snapshot should not be regenerated silently. Any later correction must be treated as an explicit new corpus revision with documented changes. The repository keeps validation automation, but the one-shot reconstruction and migration workflows have been retired after the freeze.

See [`FROZEN_SNAPSHOT.md`](FROZEN_SNAPSHOT.md) for the frozen definitions and counts.

## Authoritative review universe

The frozen ledger contains 2,214 deduplicated works and 3,217 discovery-route records. The manuscript-facing partition is:

| File | Count | Meaning |
| --- | ---: | --- |
| `corpus/set1_core.csv` | 96 | in-scope mature MAS-security work |
| `corpus/set2_emerging.csv` | 105 | in-scope emerging MAS-security work |
| `corpus/set3_context.csv` | 463 | contextual literature outside the MAS-security corpus |
| `corpus/screened_out.csv` | 1,550 | reviewed works outside the active evidence sets |

Set 1 and Set 2 use the same MAS-security scope gate and together form the 201-work MAS-security corpus. Membership requires an LLM multi-agent system, a concrete protected property, and a material inter-agent interaction path. A paper does not need a matched single-agent or rewired-system comparison merely to enter the corpus.

Set 1 then applies the frozen maturity union:

```text
peer_reviewed == yes OR frozen_citation_count >= 10
```

Interaction-dependence strength and full-text taxonomy readiness are recorded separately. In particular, `taxonomy_ready` does not change Set 1 versus Set 2 membership. The current manifest flags 103 rows for priority named-author review, and model-assisted decisions must not be described as human verified before signoff.

`corpus/routes.csv` preserves route-level provenance. `corpus/review_ledger.csv` preserves current and previous review decisions, source locators, publication/citation metadata, evidence fields, and readiness flags. Historical canonical, broad-screen, and earlier primary/secondary denominators may still appear in reconstruction material, but they are not the current evidence-set definitions.

The 2026-08-18 survey-scope adjudication reviewed all 16 survey records, retained 8 in the MAS-security corpus, moved 7 unique works to Set 3, and merged one cross-platform duplicate.

The 2026-08-18 evaluation and benchmark reconciliation re-adjudicated all 44 evaluation-primary works and reconciled the separate 44-paper benchmark analysis set. It also merged the duplicate MASLeak arXiv/published identities and promoted the existing screened-out A2ASecBench record into Set 1.

## Policy

See [`CORPUS_SET_POLICY.md`](CORPUS_SET_POLICY.md) for the exact scope, maturity, contextual-citation, and evidence-strength boundaries.

## Validate

Run either entry point from the repository root:

```bash
scripts/validate_all.sh
# or
python3 scripts/validate_three_set_corpus.py
```

The validator checks that the four sets partition all 2,214 frozen-review works, that Set 1 and Set 2 satisfy the scope/maturity invariants, that Set 3 is contextual only, and that the manifest matches the frozen views.

`corpus/manual_review_queue_2026-08-18.csv` preserves the 228-work human-classification cohort. Named classification signoff retained 201 active works, moved 18 to Set 3, and screened out 9; source/evidence verification remains separate.

## 2026-08-21 named decision-signoff correction

Reviewer `expiol` confirmed all 32 changed membership/contribution decisions: 30 proposed decisions were approved, `Algorithmic Cowardice` was retained in Set 2, and `Containing the Cascade` was removed as post-cutoff. This is a decision signoff only; it does not mark the complete 228-work source/evidence queue as fully reviewed.


## 2026-08-21 complete classification signoff

Reviewer `expiol` adjudicated the complete 228-work classification cohort: 201 accepted, 18 moved to Set 3, and 9 screened out. The resulting active corpus contains 96 Set 1 works and 105 Set 2 works. This is a scope and dominant-contribution signoff only; it does not upgrade source/evidence verification status.
