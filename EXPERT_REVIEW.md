# Expert Review Guide

## Review Objective

Determine whether the corpus supports a defensible multi-agent security SoK
without denominator drift, version duplication, scope inflation, or
paper-level collapse of claim-level evidence.

## Current State

| Item | Count | Review status |
| --- | ---: | --- |
| Deduplicated search entities | 2,182 | Frozen |
| Broad inclusion records | 326 | Frozen screening decisions |
| Canonical broad works | 325 | One preprint/publication merge recorded |
| Taxonomy candidates | 115 | 93 peer + 22 non-peer with citations `>10` |
| Provisional strict-gate passes | 45 | Author signoff required |
| Contextual candidate decisions | 26 | Not strict core |
| Adjacent candidate decisions | 9 | Not core |
| Source-blocked taxonomy candidates | 1 | Canonical source required |
| Pending taxonomy candidates | 34 | Full-text adjudication required |
| Structured paper notes | 142 | Mixed review depth; not human-verified |
| Active field-level corrections | 220 | 20 critical, 100 high, 100 medium |
| Attack claim extraction candidates | 91 | Claim splitting pending |
| Analysis decisions | 994 | Complete 142 by 7 grid; all pending |

These counts are not interchangeable. No final taxonomy or audit denominator
has been declared.

## Suggested Review Order

1. Check `corpus/sets/SET_MANIFEST.csv` and the NetSafe merge in
   `corpus/sets/02_broad_included/deduplication_map.csv`.
2. Review the selection rule and every `gate_decision` in
   `corpus/sets/03_taxonomy_eligible/taxonomy_candidates.csv`.
3. Adjudicate the 20 critical corrections, then the high and medium rows in
   `reviews/universal/active_source_review_corrections.csv`.
4. Resolve the explicit source blockers in
   `reviews/universal/active_source_review.csv`.
5. Keep imported `core_security`/`security_relevant` scope labels distinct from
   the five-gate taxonomy decisions; reconcile them only after adjudication.
6. Split each eligible paper in
   `corpus/sets/05_analysis_specific/claim_extraction_queue.csv` into atomic
   claims before counting attacks or failures.
7. Apply each contract in `analysis_contracts.csv` to
   `analysis_eligibility.csv`; record reviewer, date, exclusion reason, and
   adjudication note.
8. Re-run all headline findings on the peer-reviewed-only subset.

## Five Taxonomy Gates

A strict-core work must satisfy all five:

1. At least two separately addressable LLM-backed agent cores.
2. Explicit interaction through messages, shared state, delegation, tools,
   aggregation, membership, or environment modification.
3. A direct adversary, security property, defense, guarantee, or security
   evaluation endpoint.
4. The interaction relation changes the failure's existence, severity, scope,
   observability, attribution, containment, or enforceability.
5. Canonical full text supplies the threat setting, interaction setting,
   endpoint, metric or claim definition, and evidence locator.

## Required Signoff Outputs

The expert should return:

- accepted, rejected, boundary, or blocked status for every taxonomy candidate;
- corrected paper-level scope and primary category for the 142 structured works;
- resolved or retained disposition for every critical correction;
- atomic claim rows for papers used in quantitative synthesis;
- final `n`, peer-reviewed `n`, and non-peer `n` for each analysis contract;
- a list of claims that change direction in peer-reviewed-only sensitivity.

Do not upgrade any verification state without a named reviewer and an
adjudication note tied to canonical full-text evidence.
