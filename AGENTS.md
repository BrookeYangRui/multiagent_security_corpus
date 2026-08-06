# Corpus Maintenance Protocol

These rules apply to every contribution in this repository.

## Repository Boundary

- Maintain a literature corpus only.
- Do not add manuscript drafts, experiments, benchmark implementations, or
  downloaded paper PDFs.
- Do not turn provisional corpus labels into a fixed security taxonomy.

## Source Use

- Read the primary paper before creating a paper note.
- Do not rely on search snippets, blogs, citation metadata, or abstracts for
  technical extraction when the full text is available.
- Prefer the published version. If only a preprint is available, record its
  exact version.
- Do not fabricate missing metadata, page numbers, evidence locations, results,
  limitations, or relationships to prior work.
- Use `Not reported` when the source omits information and `Unclear` when the
  source is ambiguous.

## Required Record Set

For every included paper, update all three records in the same commit:

1. `corpus/papers.csv`
2. `corpus/references.bib`
3. One note under the appropriate `papers/` category

For every excluded paper, add a row to `corpus/excluded_papers.csv`. Do not add
an included-paper note or BibTeX entry unless the source is also retained for a
documented supporting purpose.

## Paper Notes

- Copy `templates/paper_note.md` without deleting required sections.
- Name notes `YEAR_author_short_title.md`.
- Preserve the source's title, author list, year, venue, DOI, and URLs.
- Keep the main-contribution summary to no more than three sentences.
- Attach a section, page, figure, table, or appendix location to every important
  factual claim.
- Mark whether each statement is an explicit author claim or an interpretation.
- Never infer an evaluation from an abstract.
- Never claim an attack, defense, guarantee, or limitation without direct
  evidence from the paper.

## Provenance and Verification

- Record the exact discovery source and query when applicable.
- Record the exact accessed version and access date.
- Record how the note was prepared. Automated extraction must be marked
  `agent_unverified` until a human checks it.
- Do not upgrade a verification state without the corresponding human review.
- Preserve adjudication history when a classification or claim changes.
- Use `load_bearing_review_queue.csv` for full evidence review of headline
  papers and `attack_review_queue.csv` for the remaining standard attack review.
- Use `cross_category_review_queue.csv` to screen every remaining defense,
  evaluation, survey, and general paper for attack-bearing claims. The three
  queues must remain disjoint and must jointly equal `papers.csv` through
  `universal_review_queue.csv`.
- Treat `primary_category` as canonical placement, not as evidence that a paper
  does or does not contain attacks. Record attack evidence at claim level using
  the roles and rules in `corpus/UNIVERSAL_REVIEW.md`.
- Do not count a survey mention, related-work summary, or inherited attack as
  primary attack evidence. Preserve the cited primary source instead.
- A completed review row requires a named reviewer and adjudication note. Update
  `papers.csv` verification status only to the level actually checked.
- `source_reviewed_pending_author_signoff` records a non-human source review; it
  must not be translated into `metadata_verified`, `evidence_verified`, or
  `fully_reviewed` without named human signoff.
- Preserve `blocked_pending_final_source` and
  `blocked_pending_exact_full_text` until the missing canonical source evidence
  is actually available. Never fill a blocker by inference.

## Version and Duplicate Handling

- Use one canonical record for a preprint and its published version.
- Prefer the published metadata and retain the preprint URL as an open-access
  URL when useful.
- Record superseded or duplicate versions in `corpus/excluded_papers.csv` and
  point to the canonical `paper_id`.
- Do not count workshop, preprint, and conference versions of the same work as
  separate included papers.

## Frozen Cutoff

- The search cutoff is `2026-07-01 00:00 UTC`.
- Do not add a work first retrievable on or after the cutoff to `papers.csv`,
  `references.bib`, or `evaluation_artifacts.csv`.
- Record such work in `post_cutoff_papers.csv`; place any retained citation in
  `post_cutoff_references.bib` and any retained note under `papers/post_cutoff/`.
- A post-cutoff publication of a work already available before the cutoff is a
  canonical version update, not a new post-cutoff work.

## CSV Rules

- Preserve the existing header and column order.
- Use UTF-8 and RFC 4180-compatible CSV quoting.
- Use semicolon-separated values inside multi-value fields.
- Use ISO dates in `YYYY-MM-DD` format.
- Use stable lowercase `paper_id` and `bibtex_key` values.
- Leave a field empty only when it is not applicable; use `Not reported` or
  `Unclear` for source-level missingness.
- Set exactly one `primary_category` from `attack`, `defense`, `evaluation`,
  `survey`, or `general`; secondary roles remain in `paper_type`.
- Set `scope_relation` to `core_security` only for a direct security model,
  violation, defense, or evaluation. Use `security_relevant` when the work is
  directly informative but lacks a complete security framing, and `adjacent`
  for background safety, reliability, or social-behavior evidence.

## Related-Work Synthesis

- Cite paper-note paths or BibTeX keys for every substantive synthesis claim.
- Label statements as `Established finding`, `Author-claimed gap`,
  `Cross-paper observation`, `Our interpretation`, or `Open question`.
- Do not present a cross-paper inference as an individual paper's claim.
- Keep uncertainty and publication status visible.
- Preserve all rows and decision states in `corpus/attack_screening.csv`; never
  convert `unresolved` or `eligible_not_in_corpus` into an exclusion merely to
  improve completion counts.

## Before Committing

- Confirm every referenced note path exists.
- Confirm every included `bibtex_key` exists exactly once in
  `corpus/references.bib`.
- Confirm every important note claim has an evidence location.
- Confirm automatically prepared or modified records remain
  `agent_unverified` unless human review is documented.
- Keep commit messages short, imperative, and in English.
