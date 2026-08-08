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
Its `publication_status`, `display_venue`, and `venue_type` fields are exact
projections of `corpus/final/all_relevant_papers.csv`; `source_version` records
the particular source used for extraction and must not be interpreted as a
publication-status label.

`evaluation_measurement_coding.csv` adds a provisional measurement lens to the
frozen 43-artifact view.  It is keyed one-to-one by `artifact_id`, and every row
is explicitly assistant-derived pending author signoff.  The categories are
analysis aids rather than a fixed security taxonomy.  See
`EVALUATION_MEASUREMENT_CODEBOOK.md` for the controlled fields and evidence
thresholds.

`evaluation_measurement_summary.json` is a deterministic projection of the two
evaluation ledgers joined to `corpus/final/all_relevant_papers.csv`.  It reports
all measurement counts both overall and under the peer-reviewed sensitivity;
`scripts/validate_corpus.py` regenerates and compares the complete JSON object
and canonical serialization.  Availability counts describe indexed release
evidence, not independent execution or human verification.
