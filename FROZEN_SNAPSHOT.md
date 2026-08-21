# Frozen Corpus Snapshot

Freeze date: `2026-08-18`

Literature cutoff: `2026-07-01`

Citation snapshot date: `2026-08-17`

## Frozen partition

| Partition | Count | Role |
| --- | ---: | --- |
| Set 1 | 96 | Mature in-scope MAS-security corpus |
| Set 2 | 105 | Emerging in-scope MAS-security corpus |
| Set 3 | 463 | Contextual literature outside the MAS-security corpus |
| Screened out | 1,550 | Reviewed works outside the active evidence sets |
| Frozen review universe | 2,214 | All deduplicated reviewed works |

Set 1 plus Set 2 is the 201-work MAS-security corpus.

## Membership rule

Set 1 and Set 2 share the same scope gate. Membership requires:

1. At least two separately addressable LLM-backed agents or principals.
2. A material inter-agent relation or interaction path.
3. A concrete security property, attack, defense, guarantee, adversary, or security evaluation.
4. Source evidence sufficient to support the membership decision.

Interaction dependence is an evidence-strength judgment, not a corpus-membership requirement.

Set 1 applies the frozen maturity union:

```text
peer_reviewed == yes OR frozen_citation_count >= 10
```

Set 2 contains in-scope works that do not satisfy that maturity union.

Set 3 is contextual only and is not part of the MAS-security corpus.

Full-text taxonomy readiness is tracked separately and never changes Set 1 versus Set 2 membership.

## Freeze policy

This snapshot is the manuscript-facing corpus for the current USENIX 2027 SoK revision. The set membership and frozen citation counts must not be silently regenerated or changed. Corrections require an explicit new revision, a documented change log, and a new frozen snapshot. Validation may check the frozen files but must not rewrite them.

## 2026-08-18 general-category adjudication revision

All 109 works previously labeled `general` in Set 1 and Set 2 were individually adjudicated. The revision retained 62 works in the MAS-security corpus, moved 44 to Set 3, screened out 3, and reduced the residual `general` category to 9 works. The adjudication ledgers under `corpus/adjudication/` are part of this frozen snapshot.

## 2026-08-18 survey-scope adjudication revision

All 16 records labeled `survey` in Set 1 and Set 2 were reviewed against the same substantive MAS-security scope gate. Eight surveys remained in the MAS-security corpus, seven unique works moved to Set 3, and the Research Square / SSRN copies of `Agentic and Multi-Agent Systems: A Systematic Review of Tool Use, Benchmarks, and Governance` were merged as one work. At that intermediate revision the corpus contained 232 active works and the review universe contained 2,216 works.

## 2026-08-18 evaluation and benchmark reconciliation revision

All 44 evaluation-primary works were re-adjudicated: 27 remain active and 17 move to context. The separate 44-paper benchmark analysis set was then reconciled against canonical identities. Twelve works were added or promoted into the active corpus, two dominant-contribution labels were corrected, and one post-cutoff benchmark remained outside the frozen corpus. `Deliberation and drift` was already contextual in the frozen ledger, so it does not create an additional active-corpus removal.

Two identity corrections matter for the final denominator. A2ASecBench already existed in `review_ledger.csv` as a screened-out work and is promoted rather than added to the review universe. MASLeak existed as both an active arXiv preprint row and a separate screened-out published canonical row; these are merged into the published USENIX Security record, reducing the deduplicated review universe by one.

The resulting frozen partition is **Set 1 = 105, Set 2 = 122, Set 3 = 447, screened out = 1,541**, for a **2,215-work review universe** and a **227-work MAS-security corpus**. All 227 active rows are exported to `corpus/manual_review_queue_2026-08-18.csv` and remain pending named-author signoff.


## 2026-08-21 named decision-signoff correction

Named reviewer `expiol` confirmed the 32-row changed-decision ledger. Thirty proposals were approved. `Algorithmic Cowardice` was restored from Set 3 to Set 2 after full-text scope review, while `Containing the Cascade` was removed from the frozen partition because its DOI was first registered after the cutoff. The corrected partition is **Set 1 = 105, Set 2 = 123, Set 3 = 445, screened out = 1,541**, for a **2,214-work frozen review universe** and a **228-work MAS-security corpus**. This confirms membership and dominant contribution only; the complete source/evidence queue remains pending.


## 2026-08-21 complete classification-signoff correction

Named reviewer `expiol` adjudicated all 228 rows in the manual classification cohort. The decisions retain 201 works in the active MAS-security corpus, move 18 works to Set 3, and screen out 9 works. The corrected partition is **Set 1 = 96, Set 2 = 105, Set 3 = 463, screened out = 1,550**, for a **2,214-work frozen review universe**. Dominant contributions use the explicit human selection where supplied and retain the previous value for 17 blank, non-applicable, or unresolved contribution fields. This signoff does not assert source/evidence verification.
