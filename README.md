# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Authoritative review universe

The frozen ledger contains 2,217 deduplicated works and 3,217 discovery-route records. The current manuscript-facing partition is:

| File | Count | Meaning |
| --- | ---: | --- |
| `corpus/set1_core.csv` | 121 | in-scope mature MAS-security work |
| `corpus/set2_emerging.csv` | 166 | in-scope emerging MAS-security work |
| `corpus/set3_context.csv` | 390 | contextual literature outside the MAS-security corpus |
| `corpus/screened_out.csv` | 1,540 | reviewed works outside the active evidence sets |

Set 1 and Set 2 use the same MAS-security scope gate and together form the 287-work MAS-security corpus. Membership requires an LLM multi-agent system, a concrete protected property, and a material inter-agent interaction path. A paper does not need a matched single-agent or rewired-system comparison merely to enter the corpus.

Set 1 then applies the frozen maturity union:

```text
peer_reviewed == yes OR frozen_citation_count >= 10
```

Interaction-dependence strength and full-text taxonomy readiness are recorded separately. In particular, `taxonomy_ready` does not change Set 1 versus Set 2 membership. The current manifest flags 115 rows for priority named-author review, and model-assisted decisions must not be described as human verified before signoff.

`corpus/routes.csv` preserves route-level provenance. `corpus/review_ledger.csv` preserves current and previous review decisions, source locators, publication/citation metadata, evidence fields, and readiness flags. Historical canonical, broad-screen, and earlier primary/secondary denominators may still appear in reconstruction material, but they are not the current evidence-set definitions.

## Policy

See [`CORPUS_SET_POLICY.md`](CORPUS_SET_POLICY.md) for the exact scope, maturity, contextual-citation, and evidence-strength boundaries.

## Validate

Run either entry point from the repository root:

```bash
scripts/validate_all.sh
# or
python3 scripts/validate_three_set_corpus.py
```

The validator checks that the four sets partition all 2,217 works, that Set 1 and Set 2 satisfy the scope/maturity invariants, that Set 3 is contextual only, and that the manifest matches the generated views.
