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

The 2,182-row search catalog remains the retrieval and screening log. It is not
a paper denominator. The final export repairs the old broad ledger by merging
the 114 source-reviewed records with a proceedings-level gap pass, removing
false positives and adding verified omissions.

## Final counts

| Export | Works |
| --- | ---: |
| Relevant and security-relevant papers | 139 |
| Formal peer-reviewed conference or journal papers | 90 |
| Non-peer, non-archival workshop, or publication-unverified papers | 49 |
| Non-peer papers with citations strictly greater than 10 | 19 |
| CVE records | 18 |
| Industry and community reports | 8 |
| Strongly related SoKs, surveys, and direct comparators | 8 |

Within the 139-paper export, 89 are coded `core_security`, 49 are
`security_relevant`, and one mixed NetSafe record is security-relevant at paper
level with core adversarial claims. The formal peer-reviewed subset contains 78
conference records and 12 journal records. Four non-archival workshop records
remain in the broad export rather than being counted as formal publications.

## Evidence status

The 109 records already represented in the universal source review preserve
their source-review status and evidence locators. Nineteen proceedings-gap
records are labeled `official_metadata_and_abstract_screened`; they are real,
publication-verified works but still require the same claim-level full-text
coding before use in quantitative analysis. Eleven additional high-citation
preprints come from the recorded full-text citation-threshold screen. No record
is labeled human-verified without named human signoff.

## Completeness claim

No open-web literature review can prove that it contains every work on the
internet. The defensible claim is search closure: all specified databases,
venue families, keyword families, and snowballing paths were searched through
the cutoff, duplicates were merged, unresolved sources were not converted into
evidence, and all final rows have a primary or official publication link.
