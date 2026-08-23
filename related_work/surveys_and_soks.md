# Multi Agent Security Surveys and SoKs

This synthesis uses the final signed **201 work** manuscript corpus as the only active corpus denominator.

The active corpus contains **10 survey primary works**, all indexed in `papers/index.csv` and materialized under `papers/surveys/`. These survey primary papers are part of the 201 and must not be counted again when reporting the corpus size.

## Direct and adjacent survey views

The survey papers vary in scope. Some are centered on multi agent security, while others cover broader multi agent trust, safety, governance, or agentic security questions that remain substantively relevant to the manuscript scope.

Use `papers/surveys/README.md` for the complete final survey primary list and the individual paper notes for source grounded comparisons.

## Supporting SoK comparator view

`sok_related/` is a separate supporting view used to organize especially close SoKs and survey comparators. It may overlap with the 201 corpus and may also contain broader contextual comparators. It is **not** an additional corpus and its row count must never be added to 201.

This supporting view is useful for explaining how the manuscript differs from neighboring agent security, MCP security, trustworthy agent, governance, and multi agent survey work. It should not be used as primary empirical evidence for an attack, defense, or prevalence claim.

## Use in synthesis

1. Treat 201 as the only manuscript corpus denominator.
2. Treat the 10 survey primary works as members of that 201, not an extra set.
3. Treat `sok_related/` as supporting comparison material only.
4. Use primary attack, defense, and evaluation papers for substantive empirical claims whenever possible.
5. Do not revive counts or overlap arithmetic from older corpus packages.
