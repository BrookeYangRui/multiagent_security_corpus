# Taxonomy Eligibility

`taxonomy_candidates.csv` applies the agreed discovery rule:

```text
all peer-reviewed broad inclusions
plus
non-peer broad inclusions with citations >10
```

Passing that rule creates a full-text review candidate, not automatic security
evidence. `gate_decision` distinguishes provisional core recommendations,
contextual decisions, blockers, and pending adjudication. No row becomes final
until a named human signs off on all five security gates.

The five gates are multi-agent boundary, explicit interaction, direct security
relevance, interaction dependence, and canonical full-text evidence.
