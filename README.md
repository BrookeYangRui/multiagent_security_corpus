# Multi Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Authoritative manuscript corpus

There is one active manuscript corpus: **201 works**.

| Set | Count | Meaning |
| --- | ---: | --- |
| Set 1 | 96 | In scope mature MAS security work |
| Set 2 | 105 | In scope emerging MAS security work |
| **Total** | **201** | **Authoritative MAS security corpus** |

No older corpus denominator is active in this repository. Superseded Set 3, screened out, review universe, migration, and adjudication tables are removed from the active tree so collaborators cannot mistake them for manuscript evidence.

The authoritative row level files are:

* `corpus/set1_core.csv`
* `corpus/set2_emerging.csv`

Together they contain exactly 201 unique works.

## Paper organization

`papers/` stores canonical paper notes and uses the existing organization by dominant contribution and publication venue:

```text
papers/
  attacks/<venue>/
  defenses/<venue>/
  evaluations/<venue>/
  general/<venue>/
  surveys/<venue>/
```

The signed dominant contribution totals are **42 attacks**, **94 defenses**, **44 evaluations**, **11 general works**, and **10 surveys**.

Only notes corresponding to the final 201 corpus should remain under `papers/`.

## Validation

Run:

```bash
scripts/validate_all.sh
```

The validator requires the exact 96 plus 105 partition and the signed contribution counts.
