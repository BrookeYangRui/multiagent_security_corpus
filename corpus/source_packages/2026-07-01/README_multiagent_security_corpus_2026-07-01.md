# Multiagent Security Corpus Through 2026-07-01

## What this package is

This is a search-closed, source-linked corpus of research and practitioner evidence relevant to security in LLM-backed multiagent systems. The literature cutoff is **2026-07-01 00:00 UTC**. It is not a logically provable list of every paper on the public internet. The defensible claim is that the search protocol was closed under the documented databases, venue checks, citation searches, and snowballing procedure.

## Files and counts

| File | Records | Meaning |
| --- | ---: | --- |
| `multiagent_security_all_relevant_to_2026-07-01.csv` | 142 | All works retained by the broad relevance screen, including core security, security-relevant, adjacent, formal, survey, and evaluation work |
| `multiagent_security_peer_reviewed_to_2026-07-01.csv` | 90 | Archival peer-reviewed conference and journal backbone under the corpus policy |
| `multiagent_security_non_peer_citations_gt_10.csv` | 19 | Non-archival, workshop, preprint, or otherwise non-backbone works with Semantic Scholar `citationCount > 10` at the 2026-08-06 snapshot |
| `multiagent_security_cves_verified_expanded_to_2026-07-01.csv` | 52 | CVEs and advisories relevant to agent, MCP, orchestration, or interoperable-agent infrastructure |
| `multiagent_security_industry_reports_to_2026-07-01.csv` | 16 | Official industry, nonprofit, and government reports and guidance |
| `multiagent_security_strongly_related_soks_to_2026-07-01.csv` | 14 | Closest SoKs, surveys, reviews, and challenge papers |

## Search and inclusion protocol

1. Search sources included arXiv, DBLP, Crossref, Semantic Scholar, ACL Anthology, PMLR, OpenReview, official proceedings, publisher pages, and backward and forward citation snowballing.
2. Targeted venue checks covered major security, machine learning, natural language processing, multiagent, and web venues.
3. The canonical unit is a work, not a version. Preprints and formal versions are merged when they describe the same work.
4. A work is security-core only when it has separately addressable LLM-backed agents, explicit interaction, direct security relevance, an interaction-dependent claim, and primary-source evidence.
5. The all-relevant file intentionally retains broader `security_relevant` and `adjacent` works so that scope decisions remain auditable.
6. Citation count is used only as a retrieval gate. It does not prove quality, security relevance, or evidence strength.
7. Peer-reviewed-only sensitivity analysis should be used for load-bearing quantitative findings. Preprints can support emerging-direction discussion but should not independently carry a headline conclusion.

## Frozen base and supplemental closure

The base export contained 139 canonical works. A supplemental post-export verification pass added three official arXiv records that met the same pre-cutoff scope rule: AgentShield, DynaTrust, and the STAR cooperative-attack/rectification paper. This produces 142 all-relevant works in the delivered file.

Metadata reconciliation also filled previously missing author fields and corrected canonical formal versions where official proceedings were found. Examples include 1-2-3 Check at LLMSEC 2025 and The Subtle Art of Defection at EACL 2026 Industry Track.

## Evidence strata

`peer_reviewed` means archival conference or journal evidence under this corpus policy. Workshops and non-archival proceedings are retained separately even when they used peer review. This conservative convention prevents a workshop or preprint from silently entering the archival backbone.

The CVE and industry-report files are supporting ecosystem evidence, not academic-paper denominators. CVE presence demonstrates implementation vulnerabilities, not necessarily interaction-native multiagent failure. Industry guidance demonstrates practitioner concern and proposed controls, not independent defense efficacy.

## Known limitations

No open-web search can prove absolute exhaustiveness. Citation databases change, venues can publish late metadata, and terminology remains unstable. The corpus therefore preserves source URLs, evidence status, scope labels, and cutoff basis so additions and corrections can be audited rather than hidden.
