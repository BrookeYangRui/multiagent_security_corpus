# Peer-First Corpus

This ledger canonicalizes the 326 inclusion records produced by the frozen
interaction-security screen into 325 unique works. It does not alter the
2,182-record retrieval denominator or resolve the 343 screening records that
remain undecidable.

## Rule

- Publication cutoff: `2026-07-01`
- Citation snapshot: `2026-08-06`
- Citation source: Semantic Scholar Graph API
- Influential non-peer threshold: strictly more than `10` citations
- Peer evidence: non-CoRR DBLP record, or indexed archival venue evidence
- Preprint and published versions are one canonical work

## Current Counts

| Stratum | Works |
| --- | ---: |
| Peer-reviewed conference/proceedings | 84 |
| Peer-reviewed journal | 9 |
| Non-peer-reviewed, citations > 10 | 22 |
| Non-peer-reviewed, citations <= 10 | 202 |
| Unresolved citation/publication status | 8 |
| **Total scope-included works** | **325** |

Only the two peer-reviewed strata and `influential_non_peer` form the
peer-first core. Emerging preprints remain visible for trend analysis but
must not enter corpus-level denominators. Unresolved records are not exclusions.

## Peer-Reviewed Venues

| Indexed venue | Works |
| --- | ---: |
| ACL | 11 |
| Findings of ACL | 5 |
| AAAI | 5 |
| AAAI proceedings | 4 |
| FINDINGS ACL | 4 |
| NeurIPS | 3 |
| EMNLP MAIN | 3 |
| Formal proceedings (10.48448 DOI) | 3 |
| Findings of EMNLP | 2 |
| Conference on Empirical Methods in Natural Language Processing | 2 |
| The Web Conference | 2 |
| ACL LONG | 2 |
| EMNLP | 2 |
| IJCNLP-AACL | 2 |
| Proceedings of the 25th International Conference on Autonomous Agents and Multiagent Systems | 2 |
| ICML | 1 |
| International Conference on Learning Representations | 1 |
| North American Chapter of the Association for Computational Linguistics | 1 |
| Trans. Mach. Learn. Res. | 1 |
| COLM | 1 |
| Findings of EACL | 1 |
| ESORICS 2025 International Workshops | 1 |
| Asian Conference on Intelligent Information and Database Systems | 1 |
| Science China Information Sciences | 1 |
| Complex & Intelligent Systems | 1 |
| AI and Ethics | 1 |
| Chinese Journal of Aeronautics | 1 |
| IEEE Access | 1 |
| 2026 Joint European Conference on Networks and Communications & 6G Summit (EuCNC/6G Summit) | 1 |
| 2025 3rd International Conference on Foundation and Large Language Models (FLLM) | 1 |
| International Conference on Agents | 1 |
| ICMLA | 1 |
| IEEE International Conference on Information Reuse and Integration | 1 |
| IEEE/RJS International Conference on Intelligent RObots and Systems | 1 |
| International Symposium on Image and Signal Processing and Analysis | 1 |
| 2024 IEEE Intelligent Vehicles Symposium (IV) | 1 |
| IEEE Transactions on Computational Social Systems | 1 |
| IEEE Transactions on Pattern Analysis and Machine Intelligence | 1 |
| IEEE International WIE Conference on Electrical and Computer Engineering | 1 |
| ACM Asia Conference on Computer and Communications Security | 1 |
| ACM CAIS 2026 | 1 |
| Proceedings of the 2025 6th International Conference on Computer Science and Management Technology | 1 |
| Proceedings of the 3rd ACM International Conference on AI-Powered Software | 1 |
| Proceedings of the 2026 International Conference on Generative Artificial Intelligence and Education | 1 |
| International Journal of Advanced Computer Science and Applications | 1 |
| AAAI Symposium Series | 1 |
| REALM 1 | 1 |
| EACL DEMO | 1 |
| EACL LONG | 1 |
| FINDINGS EACL | 1 |
| Proceedings of the ... Annual Hawaii International Conference on System Sciences/Proceedings of the Annual Hawaii International Conference on System Sciences | 1 |
| Annual Meeting of the Association for Computational Linguistics | 1 |
| International Conference on Agents and Artificial Intelligence | 1 |
| International Conference on Evaluation of Novel Approaches to Software Engineering | 1 |
| Neural Information Processing Systems | 1 |
| AAMAS | 1 |

## Rebuild

```bash
python3 scripts/build_peer_first_eligibility.py --refresh
python3 scripts/build_peer_first_eligibility.py --check
```

Citation counts are mutable. Any manuscript number must name the snapshot
date. Publication evidence is deliberately conservative and requires manual
resolution before an unresolved record can enter the peer-reviewed strata.
