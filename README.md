# Multi-Agent Security Corpus

Auditable literature corpus for security, privacy, robustness, misuse, and
trust in systems with interacting autonomous or semi-autonomous agents.

This repository stores metadata, structured notes, BibTeX, related-work
syntheses, and provenance. It does not store paper PDFs, manuscript drafts,
experiments, or benchmark implementations.

## Start Here

```text
corpus/papers.csv                 included-paper index
corpus/references.bib             BibTeX for included papers
corpus/excluded_papers.csv        screened exclusions and duplicates
corpus/evaluation_artifacts.csv   datasets, benchmarks, and protocols
corpus/post_cutoff_papers.csv     post-cutoff watchlist
corpus/post_cutoff_references.bib isolated watchlist citations
papers/                           one note per included paper
papers/post_cutoff/               optional watchlist notes
related_work/                     cross-paper syntheses
templates/paper_note.md           required note template
AGENTS.md                         full maintenance protocol
```

## Scope

Include a work only when multi-agent interaction changes the threat model,
attack, security consequence, defense, or evaluation. Communication, shared
memory, delegation, topology, coordination, coalition formation, and collective
decisions are in scope. Multiple model calls or roles alone are insufficient.

Exclude single-agent failures, implementation-only multi-agent scaffolding,
non-security performance studies, duplicates, and superseded versions. Keep
every exclusion with a reason in `corpus/excluded_papers.csv`.

## Frozen Cutoff

The search cutoff is `2026-07-01 00:00 UTC`. Work first retrievable on or after
the cutoff is excluded from the main corpus and all analysis denominators. Keep
it in `corpus/post_cutoff_papers.csv`; optional notes and citations belong only
under `papers/post_cutoff/` and `corpus/post_cutoff_references.bib`.

If a pre-cutoff work later receives a formal publication, update its canonical
record instead of adding a second paper.

## Adding A Paper

For each included paper, update all three records in one change:

1. `corpus/papers.csv`
2. `corpus/references.bib`
3. A note copied from `templates/paper_note.md`

Prefer the published venue, then an official manuscript, then arXiv. Record the
exact URL, version, discovery source, access date, and evidence section/page for
important claims. Use `Not reported` or `Unclear`; never guess metadata or
evidence. Automated notes remain `agent_unverified` until human review.

## Validate

```bash
python3 scripts/validate_corpus.py
```

Before pushing, fetch `origin/main`, check for collaborator changes, run the
validator, and use a short English commit message.
