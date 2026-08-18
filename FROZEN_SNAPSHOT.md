# Frozen Corpus Snapshot

Freeze date: `2026-08-18`

Literature cutoff: `2026-07-01`

Citation snapshot date: `2026-08-17`

## Frozen partition

| Partition | Count | Role |
| --- | ---: | --- |
| Set 1 | 108 | Mature in-scope MAS-security corpus |
| Set 2 | 132 | Emerging in-scope MAS-security corpus |
| Set 3 | 434 | Contextual literature outside the MAS-security corpus |
| Screened out | 1,543 | Reviewed works outside the active evidence sets |
| Review universe | 2,217 | All deduplicated reviewed works |

Set 1 plus Set 2 is the 240-work MAS-security corpus.

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

## 2026-08-18 adjudication revision

All 109 works previously labeled `general` in Set 1 and Set 2 were individually adjudicated. The revision retained 62 works in the MAS-security corpus, moved 44 to Set 3, screened out 3, and reduced the residual `general` category to 9 works. The adjudication ledgers under `corpus/adjudication/` are part of this frozen snapshot.
