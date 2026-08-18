# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Frozen manuscript corpus

The USENIX 2027 SoK manuscript-facing corpus is frozen as of `2026-08-18`. The authoritative counts are **Set 1 = 105**, **Set 2 = 122**, **Set 3 = 447**, and **screened out = 1,541**. Set 1 and Set 2 together form the **227-work MAS-security corpus**.

Corpus membership and the frozen citation snapshot should not be regenerated silently. Any later correction must be treated as an explicit new corpus revision with documented changes. The repository keeps validation automation, but the one-shot reconstruction and migration workflows have been retired after the freeze.

See [`FROZEN_SNAPSHOT.md`](FROZEN_SNAPSHOT.md) for the frozen definitions and counts.

## Authoritative review universe

The frozen ledger contains 2,216 deduplicated works and 3,217 discovery-route records. The manuscript-facing partition is:

| File | Count | Meaning |
| --- | ---: | --- |
| `corpus/set1_core.csv` | 105 | in-scope mature MAS-security work |
| `corpus/set2_emerging.csv` | 122 | in-scope emerging MAS-security work |
| `corpus/set3_context.csv` | 447 | contextual literature outside the MAS-security corpus |
| `corpus/screened_out.csv` | 1,541 | reviewed works outside the active evidence sets |

Set 1 and Set 2 use the same MAS-security scope gate and together form the 227-work MAS-security corpus. Membership requires an LLM multi-agent system, a concrete protected property, and a material inter-agent interaction path. A paper does not need a matched single-agent or rewired-system comparison merely to enter the corpus.

Set 1 then applies the frozen maturity union:

```text
peer_reviewed == yes OR frozen_citation_count >= 10
```

Interaction-dependence strength and full-text taxonomy readiness are recorded separately. In particular, `taxonomy_ready` does not change Set 1 versus Set 2 membership. The current manifest flags 115 rows for priority named-author review, and model-assisted decisions must not be described as human verified before signoff.

`corpus/routes.csv` preserves route-level provenance. `corpus/review_ledger.csv` preserves current and previous review decisions, source locators, publication/citation metadata, evidence fields, and readiness flags. Historical canonical, broad-screen, and earlier primary/secondary denominators may still appear in reconstruction material, but they are not the current evidence-set definitions.

The 2026-08-18 survey-scope adjudication reviewed all 16 survey records, retained 8 in the MAS-security corpus, moved 7 unique works to Set 3, and merged one cross-platform duplicate.

## Policy

See [`CORPUS_SET_POLICY.md`](CORPUS_SET_POLICY.md) for the exact scope, maturity, contextual-citation, and evidence-strength boundaries.

## Validate

Run either entry point from the repository root:

```bash
scripts/validate_all.sh
# or
python3 scripts/validate_three_set_corpus.py
```

The validator checks that the four sets partition all 2,216 works, that Set 1 and Set 2 satisfy the scope/maturity invariants, that Set 3 is contextual only, and that the manifest matches the frozen views.

The 2026-08-18 evaluation and benchmark reconciliation freezes the active corpus at 227 works. `corpus/manual_review_queue_2026-08-18.csv` contains all 227 active works for named-author signoff.
