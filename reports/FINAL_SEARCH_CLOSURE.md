# Final Search Closure

## Frozen boundary

- Cutoff: `2026-07-01 00:00 UTC`
- Unit of counting: canonical work
- Version rule: merge preprint and published versions; retain the published
  metadata and the earliest retrievable pre-cutoff version
- Citation rule for non-peer work: Semantic Scholar `citationCount > 10`
- Citation snapshot: `2026-08-06`

## Search sources

The search ledger combines arXiv, DBLP, Crossref, Semantic Scholar, ACL
Anthology, PMLR, OpenReview, official conference proceedings, journal publisher
pages, backward snowballing, and forward snowballing. Security-venue checks
cover USENIX Security, IEEE S&P, ACM CCS, NDSS, and AsiaCCS. ML/NLP/MAS checks
cover NeurIPS, ICML, ICLR, ACL and Findings, EMNLP and Findings, NAACL, EACL,
AAAI, AAMAS, COLM, KDD, and The Web Conference. Publisher searches cover ACM,
IEEE, Springer Nature, Elsevier, and relevant society journals.

The keyword families are:

1. System: `multi-agent LLM`, `LLM-MAS`, `agent society`, `agent collaboration`.
2. Interaction: `topology`, `communication`, `shared memory`, `delegation`,
   `debate`, `consensus`, `MCP`, `A2A`.
3. Security phenomena: `infection`, `collusion`, `Byzantine`, `goal drift`,
   `leakage`, `Sybil`, `denial of service`.
4. Defense: `provenance`, `monitor`, `quorum`, `topology defense`,
   `information flow`, `sandbox`, `guardrail`.

## Screening contract

A strict record requires separately addressable LLM-backed agents, an explicit
interaction relation, direct security relevance, an interaction-dependent
claim, and primary-source evidence. `security_relevant` records are retained as
a visible boundary set when the interaction evidence is direct but the paper's
main endpoint is safety, trust, or reliability. Pure performance, efficiency,
social simulation, and multi-call implementation papers are excluded from the
final export.

The 2,182-row search catalog remains the retrieval and screening log, and the
325-work broad ledger remains a candidate set. Neither is an included-paper
denominator. The sole canonical corpus is the 114-paper record set shared by
`corpus/papers.csv`, `corpus/references.bib`, paper notes, and the universal
review queue. Candidate or gap-search records enter this corpus only after all
three required paper records are created.

## Final counts

| Export | Works |
| --- | ---: |
| Canonical included papers | 114 |
| Formal peer-reviewed conference or journal papers | 75 |
| Non-peer or publication-unverified papers | 35 |
| Non-archival workshop papers | 4 |
| Canonical non-peer papers directly matched to the `>10` candidate ledger | 3 |
| CVE records | 18 |
| Industry and community reports | 8 |

Within the 114-paper corpus, 79 are coded `core_security`, 32 are
`security_relevant`, and 3 are `adjacent`. These scope labels remain visible;
they do not create a second paper corpus. The final exports contain no paper ID
that is absent from `corpus/papers.csv`.

## Evidence status

All 114 canonical records are represented in the universal source-review
packet and preserve their source-review status and evidence locators. All 114
remain `agent_unverified` in `corpus/papers.csv`; no record is labeled
human-verified without named human signoff. Proceedings-gap, citation-threshold,
and unresolved records remain candidates outside the canonical corpus until
the required full-text note, BibTeX entry, and `papers.csv` row are completed.

## Completeness claim

No open-web literature review can prove that it contains every work on the
internet. The defensible claim is search closure: all specified databases,
venue families, keyword families, and snowballing paths were searched through
the cutoff, duplicates were merged, unresolved sources were not converted into
evidence, and all final rows have a primary or official publication link.
