# Authoritative corpus views

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | 96 | In-scope mature corpus: peer reviewed or at least 10 frozen citations. |
| `set2_emerging.csv` | 105 | In-scope emerging corpus that has not yet met the Set 1 maturity rule. |
| `set3_context.csv` | 463 | Contextual citations; not part of the MAS-security corpus. |
| `screened_out.csv` | 1,550 | Reviewed search records outside the active evidence sets. |

Set 1 and Set 2 use the same MAS-security scope gate. Membership requires an
LLM multi-agent system, a concrete security property, and a material inter-agent
interaction path. Whether the paper isolates a causal interaction effect is an
evidence-strength question, not a corpus inclusion rule.

Set 1 then applies the maturity union rule: peer reviewed **or** frozen citation
count >= 10. Full-text taxonomy readiness is tracked separately by the
`taxonomy_ready` field and never removes an otherwise eligible paper from Set 1.
Set 2 contains the remaining in-scope early work. Set 3 is contextual only.

Reviewer `expiol` completed named scope and dominant-contribution classification
for the 228-row manual cohort on 2026-08-21. The resulting active corpus contains
201 works. Source/evidence verification remains separate, and these decisions
must not be described as full evidence verification.
