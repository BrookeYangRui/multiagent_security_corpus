# Attack Screening Ledger

`attack_screening.csv` imports the deduplicated parent search ledger and binds
its records to this repository. It is the audit trail between retrieval and the
canonical attack corpus; it is not a second paper index.

## Frame

The ledger contains 2,182 deduplicated search records. An attack candidate is a
record retrieved by an attack-family query (`*-AT`) or matched to an existing
attack-primary canonical record. Every record has exactly one `attack_decision`.
Attack-primary papers that predate this import but did not bind by DOI, arXiv ID,
or normalized title are listed separately in `attack_canonical_bridge.csv`.
They are not inserted as synthetic retrieval records and do not change the
2,182-record denominator.

| Decision | Meaning |
| --- | --- |
| `included_attack_canonical` | Bound to an attack-primary paper in `papers.csv` |
| `included_other_primary` | Bound to a defense-, evaluation-, survey-, or general-primary paper |
| `eligible_not_in_corpus` | Parent full-text screen included it, but no canonical record was matched |
| `excluded_at_screening` | Parent screening assigned an explicit exclusion |
| `unresolved` | Required source text or title/abstract evidence was unavailable or insufficient |
| `not_in_attack_query_frame` | Not retrieved by an attack-family query and not a canonical attack paper |

The denominator is closed as an accounting identity because every retrieved
record has a decision. `unresolved` remains visible and must not be silently
treated as included or excluded. Likewise, `eligible_not_in_corpus` is a review
backlog, not evidence that the work is attack-primary.

## Provenance

The imported fields retain the parent ledger's source databases, query IDs,
lexical decision, semantic decision, full-text decision, and final decision.
Canonical bindings use DOI, arXiv ID, or normalized title. Records not matched
by those identifiers remain unbound rather than being joined approximately.
The validator requires every attack-primary canonical paper to be represented
either by an exact ledger binding or by the explicit bridge.
