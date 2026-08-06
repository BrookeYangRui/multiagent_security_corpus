# Multi-Agent Security Corpus

This repository maintains a structured and auditable literature corpus for
research on the security of multi-agent systems.

It contains paper metadata, structured paper notes, related-work syntheses, and
source provenance. It does not contain experimental code, benchmark
implementations, manuscript drafts, or copyrighted paper PDFs.

## Repository Structure

```text
corpus/
    papers.csv
    references.bib
    excluded_papers.csv
    post_cutoff_papers.csv
    post_cutoff_references.bib

papers/
    surveys/
    attacks/
    defenses/
    evaluations/
    general/
    post_cutoff/

related_work/
    surveys_and_soks.md
    system_models.md
    attacks.md
    system_failures.md
    defenses.md
    benchmarks.md

templates/
    paper_note.md
```

`corpus/papers.csv` is the canonical index of included papers. Each included
paper also has one BibTeX entry and one structured note. Files under
`related_work/` synthesize evidence across paper notes; they are not substitutes
for source-level extraction.

## Search Cutoff

The corpus cutoff is frozen at `2026-07-01`. The search closed at the start of
that date (00:00 UTC); work first retrievable on or after the boundary is not
part of the included corpus or any analysis denominator.

Post-cutoff discoveries are retained in `corpus/post_cutoff_papers.csv` so that
the search history remains auditable. Their optional notes live under
`papers/post_cutoff/`, and their citations are isolated in
`corpus/post_cutoff_references.bib`. These records are a watchlist only. A
pre-cutoff work that later receives a formal publication is instead merged into
its existing canonical record without changing corpus eligibility. When a
source-reported date conflicts with a post-cutoff identifier or discovery
record, the conservative watchlist decision and the conflict are both retained.

## Scope

A paper is relevant when its security problem, attack, defense, failure, or
evaluation meaningfully depends on interactions among multiple autonomous or
semi-autonomous agents.

A paper is not included solely because it uses multiple model calls, multiple
roles, or an agent workflow. The multi-agent structure must affect the threat
model, attack mechanism, security consequence, defense, or evaluation.

## Inclusion Criteria

A paper may be included when it satisfies at least one of these conditions:

1. It studies attacks that propagate through agent interactions.
2. It studies malicious, compromised, colluding, or strategically interacting
   agents.
3. It studies security failures involving communication, shared memory,
   delegation, topology, coordination, coalition formation, or collective
   decision-making.
4. It proposes defenses that operate across agents or at the system level.
5. It introduces an evaluation, benchmark, taxonomy, survey, or SoK directly
   relevant to multi-agent security.

## Exclusion Criteria

A paper should normally be excluded when:

1. Its security problem can be completely represented as a single-agent
   component failure.
2. Multiple agents are only an implementation detail.
3. It discusses general multi-agent performance without a security, privacy,
   robustness, misuse, or trust dimension.
4. It is a duplicate, superseded version, non-archival summary, or inaccessible
   secondary description of another paper.

Excluded papers remain recorded in `corpus/excluded_papers.csv` with an explicit
reason. A preprint superseded by a published version should be merged into one
canonical record rather than counted as a separate paper.

## Paper Organization Protocol

Every included paper must have:

1. One entry in `corpus/papers.csv`.
2. One BibTeX entry in `corpus/references.bib`.
3. One structured note based on `templates/paper_note.md`.
4. A recorded discovery source, discovery query when applicable, and accessed
   paper version.
5. Page-level or section-level evidence for important claims.

Paper-note filenames use `YEAR_author_short_title.md`, for example
`2025_kim_agentic_ai_security.md`. Notes must distinguish explicit author claims
from corpus-level interpretation.

## Source Priority

When multiple sources exist, use this order:

1. Published conference or journal paper
2. Official author manuscript
3. Latest arXiv version
4. Official project repository
5. Trusted bibliographic database
6. Secondary source

Secondary sources may support discovery but should not be the primary basis for
technical claims.

## Verification Levels

Records use one of four verification states:

```text
agent_unverified
metadata_verified
evidence_verified
fully_reviewed
```

- `agent_unverified`: generated or substantially modified automatically and not
  checked by a human.
- `metadata_verified`: bibliographic metadata and links checked by a human.
- `evidence_verified`: cited source locations and extracted claims checked by a
  human.
- `fully_reviewed`: the complete note and classification checked by a human.

## Related-Work Protocol

Files under `related_work/` must reference corresponding paper notes or BibTeX
keys. Each synthesis statement should be labeled as one of:

```text
Established finding
Author-claimed gap
Cross-paper observation
Our interpretation
Open question
```

## Copyright

This repository does not redistribute copyrighted paper PDFs unless
redistribution is explicitly permitted. It stores bibliographic metadata,
links, structured notes, and limited evidence excerpts for scholarly analysis.
