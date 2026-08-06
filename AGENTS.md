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

## Version and Duplicate Handling

- Use one canonical record for a preprint and its published version.
- Prefer the published metadata and retain the preprint URL as an open-access
  URL when useful.
- Record superseded or duplicate versions in `corpus/excluded_papers.csv` and
  point to the canonical `paper_id`.
- Do not count workshop, preprint, and conference versions of the same work as
  separate included papers.

## CSV Rules

- Preserve the existing header and column order.
- Use UTF-8 and RFC 4180-compatible CSV quoting.
- Use semicolon-separated values inside multi-value fields.
- Use ISO dates in `YYYY-MM-DD` format.
- Use stable lowercase `paper_id` and `bibtex_key` values.
- Leave a field empty only when it is not applicable; use `Not reported` or
  `Unclear` for source-level missingness.

## Related-Work Synthesis

- Cite paper-note paths or BibTeX keys for every substantive synthesis claim.
- Label statements as `Established finding`, `Author-claimed gap`,
  `Cross-paper observation`, `Our interpretation`, or `Open question`.
- Do not present a cross-paper inference as an individual paper's claim.
- Keep uncertainty and publication status visible.

## Before Committing

- Confirm every referenced note path exists.
- Confirm every included `bibtex_key` exists exactly once in
  `corpus/references.bib`.
- Confirm every important note claim has an evidence location.
- Confirm automatically prepared or modified records remain
  `agent_unverified` unless human review is documented.
- Keep commit messages short, imperative, and in English.

