# Evidence Policy and Source Review Report

## Status

This report is a decision document. It does not change the active corpus rule,
paper classifications, or verification states.

Fixed reference points:

- Literature cutoff: `2026-07-01 00:00 UTC`
- Citation source: Semantic Scholar Graph API
- Citation snapshot: `2026-08-06`
- Retrieved records: 2,182
- Scope-included records before canonical version merging: 326
- Canonical broad-included works: 325
- Screening records still unresolved: 343
- Peer-reviewed backbone within the 325: 93

The retrieval, included, peer-first, and reviewed denominators are different
sets and must not be reported as interchangeable paper counts.

| Denominator | Count | Meaning |
| --- | ---: | --- |
| Retrieved records | 2,182 | Search-screening records from OpenAlex and Semantic Scholar |
| Broad full-text inclusion records | 326 | Records passing the frozen primary interaction-security screen |
| Canonical broad-included works | 325 | Inclusion records after merging preprint and published versions |
| Unresolved screening records | 343 | 196 unresolved at full text plus 147 unresolved at title/abstract |
| Canonical research corpus | 107 | Primary research works represented in `papers.csv`, BibTeX, and paper notes |
| Strongly related SoK set | 4 | Separately counted multi-agent security reviews, perspectives, agendas, and risk taxonomies |
| Peer-reviewed backbone | 93 | Peer-reviewed works among the 325 canonical broad inclusions |
| Active source-reviewed research | 107 | Research works in the active view of the imported review packet |

The equality between the 107 research works and 107 active source-review rows
means the current research corpus has review coverage. It does not mean that all
325 broad inclusions have structured notes or source review. The original
114-work packet is retained as review history; seven survey rows were separated
from the research denominator.

The work-level count is one lower than the screening-inclusion count because
NetSafe appeared once under its arXiv identifier and once under its Findings of
ACL DOI. `corpus/sets/02_broad_included/deduplication_map.csv` records the merge
and retains the published DOI record as canonical.

## Recommended Evidence Architecture

Use four independently counted evidence layers:

| Layer | Contents | Role in the SoK | Citation threshold |
| --- | --- | --- | --- |
| Research corpus | Conference, journal, and selected preprint research | Taxonomy and cross-paper analysis | Applies only to non-peer research |
| Incident corpus | CVEs, NVD records, vendor advisories, and incident postmortems | Demonstrated implementation and deployment failures | Not applicable |
| Practice-evidence corpus | Technical industry reports and reproducible red-team reports | Deployment practice and emerging evidence | Not applicable |
| Standards corpus | OWASP, MITRE, NIST, and protocol specifications | Terminology, control mapping, and system assumptions | Not applicable |

CVEs, reports, and standards should never inflate the paper denominator. Their
counts and inclusion rules must be reported separately.

## Research Corpus Thresholds

The 325 canonical scope-included works contain 93 conservatively identified
peer-reviewed works: 84 conference or proceedings papers and 9 journal papers.
All scope-eligible peer-reviewed works enter the peer backbone regardless of
citation count.

For non-peer work, the citation threshold is a retrieval or evidence-maturity
gate, not a substitute for full-text security-scope screening.

| Non-peer rule | Eligible non-peer works | Raw peer-first total |
| --- | ---: | ---: |
| Citations `>50` | 0 | 93 |
| Citations `>20` | 8 | 101 |
| Citations `>10` | 21 | 115 |
| Citations `>5` | 52 | 145 |

The repository now uses strict `>10` as a non-peer full-text review gate. See
`reports/CITATION_THRESHOLD_DECISION.md` for the title-level comparison and the
recommended alternative of using `>10` for retrieval followed by a full-text
security-scope gate.

### What a `>50` rule removes

No non-peer work in the frozen 325-work frame has more than 50 citations at the
snapshot date. A `>50` non-peer rule therefore reduces the evidence set to the
93-work peer-reviewed backbone and excludes all 232 non-peer or unresolved
records.

Among the excluded non-peer records are directly relevant, recent works such
as AgentSafe (42 citations), Taming Various Privilege Escalation (37), SAFEFLOW
(25), MAGPIE (21), SentinelAgent (19), Agent Drift (18), 1-2-3 Check (16), The
Sum Leaks More Than Its Parts (15), MedSentry (12), WOLF (12), and
Institutional AI (12). These examples show the age bias of a high citation
threshold in a fast-moving field.

Across all publication statuses, eight works exceed 50 citations, but all eight
are already in the peer-reviewed backbone: Agent Smith, Cut the Crap,
Cooperation, Competition, and Maliciousness, Secret Collusion, PsySafe,
Flooding Spread of Manipulated Knowledge, G-Safeguard, and Multi-Agent Systems
Execute Arbitrary Malicious Code.

### Recommended non-peer rule

Use strict `>10` as a discovery gate, then require a direct interaction-security
property, adversary, violation, defense, or security evaluation in the full
text before taxonomy eligibility. Keep adjacent performance, reliability, and
social-behavior work visible without counting it in security denominators.

This rule creates 21 current non-peer review candidates. It does not make them
taxonomy-eligible until they pass the same full-text scope gate as peer-reviewed
work.

## CVE Inclusion Policy

Include CVEs because they supply evidence that research papers cannot: concrete
implementation faults, affected versions, exploit preconditions, and vendor
remediation. Keep them in a separate incident corpus.

A CVE is eligible only when all of the following hold:

1. It was public before the literature cutoff.
2. It affects an agent framework, inter-agent protocol, shared state, tool or
   delegation boundary, identity or membership system, orchestrator, or a
   clearly interaction-dependent application.
3. It has a direct security consequence, not merely a quality or performance
   defect.
4. The record is supported by an official CVE, NVD, CNA, or vendor advisory.
5. Duplicate CVE, NVD, GHSA, and vendor records are merged into one incident.

Recommended incident fields:

```text
incident_id
cve_id
title
affected_product
affected_versions
publication_date
interaction_dependency
attack_preconditions
vulnerability_or_mechanism
security_property_violated
impact
cvss
official_advisory
vendor_advisory
patch_or_mitigation
evidence_locations
verification_status
```

Do not include a CVE merely because the affected product uses an LLM, RAG, or
tools. The interaction dependency must be explicit. Do not apply academic
citation thresholds to CVEs.

The current repository does not yet contain a closed, reproducible CVE search
frame. It therefore cannot claim a complete CVE count.

## Industry Report Inclusion Policy

Industry reports can document deployed architecture, incidents, threat models,
and operational controls that are absent from academic literature. They should
form a separate practice-evidence corpus.

Include only first-party technical material with enough detail to audit the
claim, such as:

- official security advisories or postmortems;
- technical red-team reports with a reproducible setup;
- protocol or platform security analyses with explicit assumptions;
- measured deployment reports with named methods and denominators.

Exclude marketing pages, opinion pieces, secondary summaries, unverifiable
demos, generic risk lists, and reports that merely repeat academic results.

Recommended report fields:

```text
report_id
organization
title
publication_date
report_type
primary_url
system_and_deployment_scope
interaction_dependency
threat_model
method
metric_and_denominator
finding
limitations
conflict_of_interest
evidence_locations
verification_status
```

Industry reports should support operational observations, not replace primary
research for formal claims. The current repository does not yet have a closed
industry-report search frame and must not claim completeness or a total count.

## Active 107-Work Source Review

The imported 114-work packet remains under `reviews/universal/` as history. Its
active research view covers 107 works drawn from three disjoint queues:

| Review track | Works |
| --- | ---: |
| Load-bearing | 20 |
| Standard attack-primary | 42 |
| Cross-category attack screening | 45 |
| **Total** | **107** |

This packet does not represent all 325 included works. It is a deep source
review of the existing universal review queue and must not be presented as the
full-corpus review denominator.

### Review outcomes

| Outcome | Works |
| --- | ---: |
| Ready after major patch | 56 |
| Ready after minor patch | 48 |
| Pending final source verification | 1 |
| Pending exact full-text verification | 1 |
| Blocked metadata signoff | 1 |

The three unresolved works are:

- `ju2026flooding`: final journal author metadata and exact locators require the
  canonical journal PDF.
- `li2026a2asecbench`: formal identity is supported, but exact final-paper page,
  figure, and table locators remain to be verified.
- `zou2026calbench`: author metadata conflicts between available sources and
  requires explicit signoff.

### Correction load

The active correction ledger contains 210 field-level changes. The original
231-row ledger remains unchanged as adjudication history.

| Severity | Corrections |
| --- | ---: |
| Critical | 20 |
| High | 96 |
| Medium | 94 |

These corrections have not been bulk-applied to `papers.csv` or paper notes.
Many require author judgment, claim-level splitting, or a canonical PDF check.

### Scope results

Current paper-level scope labels in the research corpus are 79 `core_security`,
25 `security_relevant`, and 3 `adjacent`. After normalizing NetSafe's mixed
recommendation to its paper-level label, the active review recommends:

| Recommended paper-level scope | Works |
| --- | ---: |
| Core security | 71 |
| Security relevant | 31 |
| Adjacent | 5 |

NetSafe remains core evidence only for its adversarial claims; its paper-level
scope is security-relevant because it mixes security with safety, fairness, and
reliability phenomena.

### Attack-bearing evidence

The review requires attack-instance coding for 91 of the 107 research works and
records no qualifying attack instance for 16. This confirms why attack review cannot be
limited to the `papers/attacks/` directory: defense, benchmark, evaluation, and
general papers can contain original attack evidence.

The recommended-category field is multi-valued and includes primary category
and secondary roles. It must not be copied directly into the single-valued
`primary_category` column. Category changes need paper-by-paper adjudication.

### Coverage against the peer-first frame

Only 40 of the 94 peer-reviewed backbone works appear in the active research
packet: 28 currently core, 11 security-relevant, and one mixed-scope NetSafe
record. The citation-gate review separately covers the newly confirmed COLM
paper *Cohesive Conversations*. Therefore 53 peer-reviewed works still need the
same source-review treatment.

All 21 current non-peer works above the `>10` discovery threshold now have a
full-text decision: three through the active research packet and 18 through
`reviews/citation_gate/non_peer_gt10_full_text_adjudication.csv`. The original
19-work pending batch also contained *Cohesive Conversations*, which was moved
to the peer-reviewed backbone after its official COLM 2024 record was located.

## Verification Semantics

Every imported row is `source_reviewed_pending_author_signoff` or blocked. This
means a non-human source review has proposed corrections. It does not mean that
a named human verified metadata, evidence locations, or the complete note.

The packet must not trigger automatic upgrades to `metadata_verified`,
`evidence_verified`, or `fully_reviewed`. Apply corrections individually,
preserve adjudication notes, and record named human signoff.

## Decision

1. Use `>10` as the non-peer discovery threshold plus a full-text
   security-scope gate.
2. Keep every pending candidate outside the final taxonomy denominator.
3. Include CVEs and technical industry reports as separately searched and
   separately counted evidence corpora.
4. Apply the 231 corrections by severity, starting with the 20 critical items.
5. Review the remaining 53 peer-reviewed backbone works before reporting a
   final taxonomy-eligible denominator. The non-peer `>10` full-text queue is
   closed, subject to named author signoff.
6. Do not claim complete CVE or industry-report coverage until their search
   sources, queries, deduplication rules, and screening decisions are released.
