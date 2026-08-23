# Multi Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Authoritative manuscript corpus

There is one active manuscript corpus: **187 works**.

| Set | Count | Meaning |
| --- | ---: | --- |
| Set 1 | 91 | In-scope mature MAS security work |
| Set 2 | 96 | In-scope emerging MAS security work |
| **Total** | **187** | **Authoritative MAS security corpus** |

The authoritative row-level files are `corpus/set1_core.csv` and `corpus/set2_emerging.csv`.

The 2026-08-23 scope correction removed 14 records from the previous 201-work view. Three were first public after the cutoff, two broad agent-security surveys remain only as related-work comparators, one source could not be independently recovered, and eight additional works were removed because MAS was primarily a tool or application architecture rather than the paper-level security object. CoMet, DACS, and NOD remain in scope.

## Paper organization

`papers/` contains exactly the active corpus notes, organized by dominant contribution and venue. Current totals are **44 attacks**, **80 defenses**, **44 evaluations**, **12 general works**, and **7 surveys**.

## Validation

Run `scripts/validate_all.sh`.
