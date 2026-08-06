# Analysis-Specific Sets

`analysis_contracts.csv` freezes seven audit contracts. Each contract defines
its unit, inclusion rule, exclusion rule, required fields, and peer-reviewed
sensitivity requirement.

`analysis_eligibility.csv` is an expert-adjudication ledger. Its automatic
`candidate_signal` is only a routing aid; every eligibility decision remains
pending until reviewed.

`claim_extraction_queue.csv` contains 91 paper-level attack candidates. Empty
`claim_id` values are intentional: papers with multiple attacks, defenses, or
failures must be split into separate claim records before quantitative use.

`evaluation_artifacts.csv` indexes reusable benchmarks, datasets, attack
suites, and evaluation protocols without duplicating their canonical notes.
