# Authoritative corpus views

The repository uses three evidence sets and one screened search ledger.

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | 97 | Mature evidence used to build the systematization, counts, and headline findings. |
| `set2_emerging.csv` | 249 | In-scope early work used only for emerging directions and open problems. |
| `set3_context.csv` | 0 | Contextual citations. This set is not part of the MAS-security corpus. |
| `screened_out.csv` | 1,871 | Search records outside the direct corpus and without an active citation role. |

Set 1 and Set 2 pass the same strict MAS-security scope gate. Set 1 then
satisfies the maturity rule: peer reviewed, or more than 10 citations in the
frozen citation snapshot. Set 3 supports background and comparison only.

`review_ledger.csv` records every decision and preserves the previous label.
`author_priority_review.csv` identifies promotions, downgrades, missing
full-text locators, and unclear interaction tags. The review is model-assisted;
all retained rows require named-author signoff before they can be described as
human verified.

The literature cutoff is 2026-07-01. Citation counts are frozen on 2026-08-17.
OpenAlex is preferred, with Semantic Scholar used when OpenAlex has no count.
