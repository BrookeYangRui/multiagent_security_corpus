# Multi-Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Search cutoff: `2026-07-01 00:00 UTC`.

## One authoritative review universe

| File | Count |
| --- | ---: |
| `corpus/review_queue.csv` | 2,217 works |
| `corpus/primary.csv` | 303 primary |
| `corpus/secondary.csv` | 177 secondary |
| `corpus/exclude.csv` | 1,396 exclude |
| `corpus/pending.csv` | 341 pending |
| targeted route | 318 records / 317 works |

Older broad-screen, canonical-142, taxonomy-115, and source-package denominators were removed rather than archived so that counts cannot be mixed across versions. `primary` is the direct interaction-security evidence pool; `secondary` is security-relevant context; `exclude` is outside the evidence boundary; `pending` remains unresolved and is never counted as final evidence.

`corpus/routes.csv` preserves route-level provenance and `corpus/decision_ledger.csv` preserves review decisions. Discovery-route membership alone cannot promote a work. Stronger source or human review overrides weaker discovery evidence, and equal-strength conflicts remain pending.

`papers/` contains source notes where available, not a denominator. `related_work/` contains synthesis notes. `corpus/evidence/` contains non-paper evidence such as CVEs and industry reports and never enters the academic-work counts above.

## Validate

```bash
scripts/validate_all.sh
```
