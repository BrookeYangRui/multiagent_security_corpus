# Frozen Corpus Snapshot

Freeze date: `2026-08-18`

Literature cutoff: `2026-07-01`

Citation snapshot date: `2026-08-17`

## Frozen partition

| Partition | Count | Role |
| --- | ---: | --- |
| Set 1 | 104 | Mature in-scope MAS-security corpus |
| Set 2 | 112 | Emerging in-scope MAS-security corpus |
| Set 3 | 452 | Contextual literature outside the MAS-security corpus |
| Screened out | 1,546 | Reviewed works outside the active evidence sets |
| Review universe | 2,214 | All deduplicated reviewed works |

Set 1 plus Set 2 is the 216-work MAS-security corpus.

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

Before the 2026-08-21 revision, the frozen partition was **Set 1 = 105, Set 2 = 122, Set 3 = 447, screened out = 1,541**, for a **2,215-work review universe** and a **227-work MAS-security corpus**. Those 227 active rows formed the original export in `corpus/manual_review_queue_2026-08-18.csv`.


## 2026-08-21 confirmed-membership revision

Named secondary confirmation moved five works to Set 3 and screened out five works. The duplicate `10.2139/ssrn.6884338` record was merged into canonical DOI `10.2139/ssrn.6996678`. The corrected partition is **Set 1 = 104, Set 2 = 112, Set 3 = 452, screened out = 1,546**, for a **2,214-work review universe** and a **216-work MAS-security corpus**. Source/evidence verification remains pending.
