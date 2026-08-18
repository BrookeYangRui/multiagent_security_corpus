#!/usr/bin/env python3
from pathlib import Path

p = Path('scripts/apply_evaluation_benchmark_reconciliation_v2.py')
s = p.read_text(encoding='utf-8')
start = s.index('        if action == "alias_merge_upgrade":')
end = s.index('\n        r = find(', start)
block = '''        if action == "alias_merge_upgrade":
            pre = [r for r in ledger if r.get("arxiv_id") == "2505.12442"]
            canon = [r for r in ledger if r.get("work_key") == "wang2026masleak"]
            if len(pre) != 1 or len(canon) != 1:
                raise SystemExit(f"MASLeak identity merge expected one preprint and one canonical row, got {len(pre)} and {len(canon)}")
            r = pre[0]
            duplicate = canon[0]
            old = dict(r)
            ledger.remove(duplicate)
            r.update({
                "work_key": "wang2026masleak", "canonical_paper_id": "wang2026masleak",
                "title": "MASLeak: Investigating and Exposing Intellectual Property Leakage Vulnerabilities in Multi-Agent Systems",
                "venue": "USENIX Security 2026", "year": "2026", "arxiv_id": "2505.12442",
                "primary_url": "https://www.usenix.org/conference/usenixsecurity26/presentation/wang-liwen",
                "strict_scope_pass": "yes", "evidence_set": "set1_core",
                "peer_reviewed": "yes", "peer_review_basis": "published USENIX Security 2026 paper",
                "maturity_rule_pass": "yes", "dominant_contribution": "attack",
                "citation_role": "", "paper_section": "", "emerging_direction": "",
                "decision_reason": "2026-08-18 identity correction: merged duplicate arXiv and canonical USENIX records into published MASLeak and upgraded to Set 1.",
                "reviewer": REVIEWER, "reviewed_at": DATE, "author_signoff_required": "yes",
            })
            original["wang2026masleak"] = old
            record(r, "identity_merge_and_maturity_upgrade", d["reason_code"], d["confidence"])
            continue
'''
s = s[:start] + block + s[end:]

# Identity facts established from the frozen ledger.
s = s.replace(
    'if len(ledger) != 2216: raise SystemExit("reconciliation must preserve 2,216-work universe")',
    'if len(ledger) != 2215: raise SystemExit("reconciliation must produce the deduplicated 2,215-work universe")',
)
s = s.replace(
    'text = text.replace("if len(ledger) != 2217:", "if len(ledger) != 2216:")',
    'text = text.replace("if len(ledger) != 2217:", "if len(ledger) != 2215:")',
)
s = s.replace(
    'if sum(counts.values()) != 2216 or counts["set1_core"] + counts["set2_emerging"] != 226:',
    'if sum(counts.values()) != 2215 or counts["set1_core"] + counts["set2_emerging"] != 227:',
)
s = s.replace('m["search_universe"] = 2216;', 'm["search_universe"] = 2215;')
s = s.replace('The frozen ledger contains 2,216 deduplicated works', 'The frozen ledger contains 2,215 deduplicated works')
s = s.replace(
    'A2ASecBench already existed in the deduplicated review ledger and is promoted rather than added, so the review universe remains 2,216 works.',
    'A2ASecBench already existed in the deduplicated review ledger and is promoted rather than added. The duplicate MASLeak preprint/published identities are merged, reducing the review universe to 2,215 works.',
)
s = s.replace('if len(L)!=2216 or set().union(*K.values())', 'if len(L)!=2215 or set().union(*K.values())')
s = s.replace('m["search_universe"]!=2216', 'm["search_universe"]!=2215')
s = s.replace('"universe":2216', '"universe":2215')

# The actual frozen benchmark reconciliation shows that Deliberation and drift was
# already contextual in the current ledger, so it is not an additional active removal.
s = s.replace('counts["set2_emerging"] != 121', 'counts["set2_emerging"] != 122')
s = s.replace('exp2 = {"attack":38,"defense":61,"evaluation":15,"general":4,"survey":3}', 'exp2 = {"attack":38,"defense":61,"evaluation":16,"general":4,"survey":3}')
s = s.replace('if len(manual) != 226:', 'if len(manual) != 227:')
s = s.replace('{"set1_core":105,"set2_emerging":121,"total_corpus":226}', '{"set1_core":105,"set2_emerging":122,"total_corpus":227}')
s = s.replace('"additional_unique_active_to_context_move":1,', '"additional_unique_active_to_context_move":0,')
s = s.replace('"final_active_corpus":226', '"final_active_corpus":227')
s = s.replace('"rows":226,"status":"pending_named_author_signoff"', '"rows":227,"status":"pending_named_author_signoff"')
s = s.replace('All 226 active works are queued', 'All 227 active works are queued')
s = s.replace('**Set 2 = 121**', '**Set 2 = 122**')
s = s.replace('**226-work MAS-security corpus**', '**227-work MAS-security corpus**')
s = s.replace('| `corpus/set2_emerging.csv` | 121 |', '| `corpus/set2_emerging.csv` | 122 |')
s = s.replace('together form the 226-work MAS-security corpus', 'together form the 227-work MAS-security corpus')
s = s.replace('freezes the active corpus at 226 works', 'freezes the active corpus at 227 works')
s = s.replace('contains all active works for named-author signoff.', 'contains all 227 active works for named-author signoff.')
s = s.replace('| Set 2 | 121 |', '| Set 2 | 122 |')
s = s.replace('Set 1 plus Set 2 is the 226-work MAS-security corpus.', 'Set 1 plus Set 2 is the 227-work MAS-security corpus.')
s = s.replace('moving one additional unique active work (`Deliberation and drift`) to context, ', 'confirming that `Deliberation and drift` was already contextual in the frozen ledger, ')
s = s.replace('for a 226-work MAS-security corpus. All 226 active rows', 'for a 227-work MAS-security corpus. All 227 active rows')
s = s.replace('if len(rows("manual_review_queue_2026-08-18.csv"))!=226:', 'if len(rows("manual_review_queue_2026-08-18.csv"))!=227:')
s = s.replace('m["corpus_counts"]["total_corpus"]!=226', 'm["corpus_counts"]["total_corpus"]!=227')
s = s.replace('active=226', 'active=227')
s = s.replace('"active":226', '"active":227')

p.write_text(s, encoding='utf-8')
