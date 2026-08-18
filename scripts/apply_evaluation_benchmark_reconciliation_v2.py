#!/usr/bin/env python3
"""Apply the final 2026-08-18 evaluation + benchmark reconciliation.

The frozen 232-work snapshot already contains A2ASecBench in the 2,216-work
review ledger, but not in the active corpus. This integrator promotes that
existing row rather than adding a new identity, applies the two adjudication
ledgers, canonicalizes MASLeak, rebuilds all public views, and emits a complete
manual-review queue for named-author signoff.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
A = C / "adjudication"
DATE = "2026-08-18"
REVIEWER = "OpenAI GPT-5.6 Pro, model-assisted source review"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def norm(s: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split())


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def section(role: str) -> str:
    return {
        "measurement_context": "Evaluation",
        "deployment_evidence": "Introduction and Threat Model",
        "related_work": "Overview and Related Work",
        "protocol_or_standard": "System Model and Defenses",
        "agentic_security_context": "Introduction and Related Work",
        "defense_analogy": "Defenses",
    }.get(role, "Overview and Related Work")


def main() -> int:
    ledger_path = C / "review_ledger.csv"
    ledger = read_csv(ledger_path)
    if len(ledger) != 2216:
        raise SystemExit(f"expected 2,216-work frozen ledger, got {len(ledger)}")
    fields = list(ledger[0])
    original = {r["work_key"]: dict(r) for r in ledger}
    original_title = {norm(r["title"]): dict(r) for r in ledger}

    def maps():
        return ({r["work_key"]: r for r in ledger}, {norm(r["title"]): r for r in ledger})

    def find(*, key: str = "", title: str = "") -> dict[str, str]:
        by_key, by_title = maps()
        if key and key in by_key: return by_key[key]
        if title and norm(title) in by_title: return by_title[norm(title)]
        raise KeyError(f"unresolved row: {key=} {title=}")

    changes: dict[str, dict[str, str]] = {}
    def record(row: dict[str, str], action: str, reason: str, confidence: str) -> None:
        old = original.get(row["work_key"]) or original_title.get(norm(row["title"])) or {}
        changes[row["work_key"]] = {
            "change_type": action,
            "work_key": row["work_key"],
            "title": row["title"],
            "previous_membership": old.get("evidence_set", ""),
            "proposed_membership": row.get("evidence_set", ""),
            "previous_contribution": old.get("dominant_contribution", ""),
            "proposed_contribution": row.get("dominant_contribution", ""),
            "reason_code": reason,
            "confidence": confidence,
            "human_decision": "",
            "human_notes": "",
        }

    def to_context(row: dict[str, str], role: str, reason: str, confidence: str, action: str) -> None:
        row["strict_scope_pass"] = "no"
        row["evidence_set"] = "set3_context"
        row["citation_role"] = role or "measurement_context"
        row["paper_section"] = section(row["citation_role"])
        row["scope_reason"] = "2026-08-18 adjudication: the headline protected property/evaluation is contextual rather than substantively MAS-security under the frozen scope gate."
        row["decision_reason"] = f"2026-08-18 adjudication: {reason}. Moved to Set 3 context."
        row["reviewer"] = REVIEWER; row["reviewed_at"] = DATE; row["author_signoff_required"] = "yes"
        record(row, action, reason, confidence)

    # Evaluation-primary audit: exactly 17 unique active -> context decisions.
    eval_rows = read_csv(A / "evaluation_scope_2026-08-18.csv")
    if len(eval_rows) != 44: raise SystemExit("evaluation adjudication must have 44 rows")
    moves = [d for d in eval_rows if d["decision"] == "move"]
    if len(moves) != 17: raise SystemExit(f"expected 17 evaluation moves, got {len(moves)}")
    moved = set()
    for d in moves:
        r = find(title=d["title"])
        if r["evidence_set"] not in {"set1_core", "set2_emerging"}:
            raise SystemExit(f"evaluation move is not active: {d['title']} ({r['evidence_set']})")
        moved.add(norm(r["title"]))
        to_context(r, d.get("target_role") or "measurement_context", d["reason_code"], d["confidence"], "evaluation_scope_move")

    bench = read_csv(A / "benchmark_reconciliation_2026-08-18.csv")
    if len(bench) != 44: raise SystemExit("benchmark reconciliation must have 44 rows")

    emerging = {
        "lemercier2026gambit": ("no", "arXiv preprint"),
        "zhu2025_collaborative_shadows": ("no", "arXiv preprint"),
        "zhao2026macbench": ("no", "arXiv preprint"),
        "arora2026safeagents": ("unclear", "workshop peer-review status not established in this adjudication"),
    }

    for d in bench:
        action = d["action"]
        if action in {"keep", "keep_set3", "post_cutoff"}: continue

        if action == "add_set1":
            # The old generated-set audit missed that this work already existed in
            # review_ledger.csv. Promote that canonical row; do not change universe size.
            r = find(key="li2026a2asecbench", title=d["title"])
            old_set = r["evidence_set"]
            if old_set in {"set1_core", "set2_emerging"}:
                raise SystemExit(f"A2ASecBench unexpectedly already active in {old_set}")
            r.update({
                "strict_scope_pass": "yes", "evidence_set": "set1_core",
                "peer_reviewed": "yes", "peer_review_basis": "published ICLR 2026 conference paper",
                "maturity_rule_pass": "yes", "dominant_contribution": "evaluation",
                "citation_role": "", "paper_section": "", "emerging_direction": "",
                "scope_reason": "Published A2A protocol benchmark with attacks across discovery, task state, remote requests, and returned artifacts between separately addressable agents.",
                "decision_reason": "2026-08-18 benchmark reconciliation: promoted existing A2ASecBench ledger row into Set 1 based on the published ICLR source review.",
                "reviewer": REVIEWER, "reviewed_at": DATE, "author_signoff_required": "yes",
            })
            record(r, f"promote_{old_set}_to_set1", d["reason_code"], d["confidence"])
            continue

        if action == "alias_merge_upgrade":
            cands = [r for r in ledger if r.get("arxiv_id") == "2505.12442" or r.get("work_key") == "wang2026masleak"]
            # Deduplicate the candidate list by object identity.
            uniq = []
            for r in cands:
                if all(r is not x for x in uniq): uniq.append(r)
            if len(uniq) != 1: raise SystemExit(f"MASLeak expected one ledger row, got {len(uniq)}")
            r = uniq[0]; old_key = r["work_key"]
            if old_key != "wang2026masleak" and any(x["work_key"] == "wang2026masleak" for x in ledger):
                raise SystemExit("MASLeak canonical key collision")
            old = original.get(old_key, dict(r))
            r.update({
                "work_key": "wang2026masleak", "canonical_paper_id": "wang2026masleak",
                "title": "MASLeak: Investigating and Exposing Intellectual Property Leakage Vulnerabilities in Multi-Agent Systems",
                "venue": "USENIX Security 2026", "year": "2026", "arxiv_id": "2505.12442",
                "primary_url": "https://www.usenix.org/conference/usenixsecurity26/presentation/wang-liwen",
                "strict_scope_pass": "yes", "evidence_set": "set1_core",
                "peer_reviewed": "yes", "peer_review_basis": "published USENIX Security 2026 paper",
                "maturity_rule_pass": "yes", "dominant_contribution": "attack",
                "citation_role": "", "paper_section": "", "emerging_direction": "",
                "decision_reason": "2026-08-18 identity correction: earlier arXiv version canonicalized to published MASLeak and upgraded to Set 1.",
                "reviewer": REVIEWER, "reviewed_at": DATE, "author_signoff_required": "yes",
            })
            original["wang2026masleak"] = old
            record(r, "identity_merge_and_maturity_upgrade", d["reason_code"], d["confidence"])
            continue

        r = find(key=d.get("canonical_work_key", ""), title=d["title"])

        if action == "move_set3":
            if norm(r["title"]) in moved: continue
            if r["evidence_set"] in {"set1_core", "set2_emerging"}:
                to_context(r, "measurement_context", d["reason_code"], d["confidence"], "benchmark_scope_move")
            continue

        if action == "relabel":
            old = r["dominant_contribution"]
            r["dominant_contribution"] = d["recommended_contribution"]
            if r["evidence_set"] == "set2_emerging": r["emerging_direction"] = r["dominant_contribution"]
            r["decision_reason"] = f"2026-08-18 contribution correction: {d['reason_code']}."
            r["reviewer"] = REVIEWER; r["reviewed_at"] = DATE; r["author_signoff_required"] = "yes"
            record(r, f"relabel_{old}_to_{r['dominant_contribution']}", d["reason_code"], d["confidence"])
            continue

        if action in {"promote_set1", "promote_set2"}:
            target = d["recommended_membership"]
            r["strict_scope_pass"] = "yes"; r["evidence_set"] = target
            r["citation_role"] = ""; r["paper_section"] = ""
            r["dominant_contribution"] = d["recommended_contribution"]
            r["scope_reason"] = f"2026-08-18 source reconciliation established a material inter-agent security path: {d['reason_code']}."
            r["decision_reason"] = f"2026-08-18 benchmark reconciliation promoted this work into {target}: {d['reason_code']}."
            r["reviewer"] = REVIEWER; r["reviewed_at"] = DATE; r["author_signoff_required"] = "yes"
            if target == "set1_core":
                r["peer_reviewed"] = "yes"; r["peer_review_basis"] = r.get("peer_review_basis") or "published archival venue/source review"
                r["maturity_rule_pass"] = "yes"; r["emerging_direction"] = ""
            else:
                peer, basis = emerging[d["canonical_work_key"]]
                r["peer_reviewed"] = peer; r["peer_review_basis"] = basis; r["maturity_rule_pass"] = "no"
                r["emerging_direction"] = r["dominant_contribution"]
                try: cites = int(float((r.get("frozen_citation_count") or "0").replace(",", "")))
                except ValueError: cites = 0
                if peer == "yes" or cites >= 10: raise SystemExit(f"Set 2 promotion meets maturity: {r['title']}")
            record(r, action, d["reason_code"], d["confidence"])
            continue

        raise SystemExit(f"unhandled benchmark action {action}")

    keys = [r["work_key"] for r in ledger]
    dup = [k for k, n in Counter(keys).items() if k and n > 1]
    if dup: raise SystemExit(f"duplicate work keys after reconciliation: {dup[:5]}")
    if len(ledger) != 2216: raise SystemExit("reconciliation must preserve 2,216-work universe")
    write_csv(ledger_path, sorted(ledger, key=lambda r: r["work_key"]), fields)

    # Correct the stale one-shot rebuild invariant to the already-deduplicated universe.
    rebuild = ROOT / "scripts" / "rebuild_membership_from_ledger.py"
    text = rebuild.read_text(encoding="utf-8")
    text = text.replace("if len(ledger) != 2217:", "if len(ledger) != 2216:")
    rebuild.write_text(text, encoding="utf-8")
    subprocess.run(["python3", str(rebuild)], check=True)

    sets = {name: read_csv(C / filename) for name, filename in {
        "set1_core":"set1_core.csv", "set2_emerging":"set2_emerging.csv",
        "set3_context":"set3_context.csv", "screened_out":"screened_out.csv"}.items()}
    counts = {k: len(v) for k, v in sets.items()}
    if counts["set1_core"] != 105 or counts["set2_emerging"] != 121:
        raise SystemExit(f"unexpected active-set split: {counts}")
    if sum(counts.values()) != 2216 or counts["set1_core"] + counts["set2_emerging"] != 226:
        raise SystemExit(f"unexpected integrated arithmetic: {counts}")

    s1 = dict(Counter(r["dominant_contribution"] for r in sets["set1_core"]))
    s2 = dict(Counter(r["dominant_contribution"] for r in sets["set2_emerging"]))
    exp1 = {"attack":33,"defense":39,"evaluation":21,"general":7,"survey":5}
    exp2 = {"attack":38,"defense":61,"evaluation":15,"general":4,"survey":3}
    if s1 != exp1 or s2 != exp2: raise SystemExit(f"unexpected contributions: {s1=} {s2=}")

    # Full manual queue over every active work.
    manual_fields = [
        "work_key","title","evidence_set","dominant_contribution","year","venue",
        "peer_reviewed","frozen_citation_count","interaction_interfaces","risk_or_property",
        "interaction_dependence","scope_reason","decision_reason","evidence_basis","evidence_locator",
        "author_signoff_required","human_scope_decision","human_contribution_decision","human_notes"
    ]
    manual = []
    for r in sets["set1_core"] + sets["set2_emerging"]:
        manual.append({**r,"human_scope_decision":"","human_contribution_decision":"","human_notes":""})
    manual.sort(key=lambda r:(0 if r["evidence_set"]=="set1_core" else 1,r["dominant_contribution"],r["title"].lower()))
    write_csv(C / "manual_review_queue_2026-08-18.csv", manual, manual_fields)
    if len(manual) != 226: raise SystemExit("manual queue is not complete")

    change_fields = ["change_type","work_key","title","previous_membership","proposed_membership","previous_contribution","proposed_contribution","reason_code","confidence","human_decision","human_notes"]
    write_csv(A / "manual_signoff_changes_2026-08-18.csv", sorted(changes.values(), key=lambda r:(r["change_type"],r["title"].lower())), change_fields)

    # Explicit arXiv -> published MASLeak alias.
    alias_path = C / "identifier_alias_overrides.csv"
    aliases = read_csv(alias_path); alias_fields = list(aliases[0])
    if not any(r.get("alias_type")=="arxiv" and r.get("alias_value")=="2505.12442" for r in aliases):
        aliases.append({
            "alias_type":"arxiv","alias_value":"2505.12442","canonical_doi":"","canonical_arxiv_id":"2505.12442",
            "canonical_title":"MASLeak: Investigating and Exposing Intellectual Property Leakage Vulnerabilities in Multi-Agent Systems",
            "authoritative_url":"https://www.usenix.org/conference/usenixsecurity26/presentation/wang-liwen",
            "note":"Earlier arXiv title is the prepublication version of the USENIX Security 2026 MASLeak paper."
        })
        write_csv(alias_path, aliases, alias_fields)

    manifest_path = C / "manifest.json"
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    m["search_universe"] = 2216; m["counts"] = counts
    m["corpus_counts"] = {"set1_core":105,"set2_emerging":121,"total_corpus":226}
    m["set1_contributions"] = exp1; m["set2_contributions"] = exp2
    m["evaluation_adjudication_revision"] = {"date":DATE,"reviewed":44,"retained_in_corpus":27,"moved_to_set3":17,"ledger":"adjudication/evaluation_scope_2026-08-18.csv"}
    m["benchmark_reconciliation_revision"] = {"date":DATE,"reviewed_report_papers":44,"active_additions_or_promotions":12,"additional_unique_active_to_context_move":1,"contribution_relabels":2,"identity_merge_and_maturity_upgrade":1,"post_cutoff":1,"final_active_corpus":226,"ledger":"adjudication/benchmark_reconciliation_2026-08-18.csv"}
    m["manual_review_queue"] = {"path":"manual_review_queue_2026-08-18.csv","rows":226,"status":"pending_named_author_signoff"}
    m["verification_note"] = "Model-assisted source review. All 226 active works are queued for named-author manual signoff; do not claim human verification before signoff."
    m["files"] = {}
    for p in sorted(C.glob("*.csv")):
        m["files"][p.name] = {"sha256":file_hash(p),"rows":len(read_csv(p))}
    for p in sorted(A.glob("*.csv")):
        m["files"][f"adjudication/{p.name}"] = {"sha256":file_hash(p),"rows":len(read_csv(p))}
    manifest_path.write_text(json.dumps(m,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    # Manuscript-facing docs use actual non-active split, which depends on where the
    # preexisting A2ASecBench row lived in the old frozen partition.
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    root_readme = re.sub(r"\*\*Set 1 = 104\*\*, \*\*Set 2 = 128\*\*, \*\*Set 3 = 441\*\*, and \*\*screened out = 1,543\*\*\. Set 1 and Set 2 together form the \*\*232-work MAS-security corpus\*\*\.", f"**Set 1 = 105**, **Set 2 = 121**, **Set 3 = {counts['set3_context']}**, and **screened out = {counts['screened_out']:,}**. Set 1 and Set 2 together form the **226-work MAS-security corpus**.", root_readme)
    root_readme = root_readme.replace("The frozen ledger contains 2,216 deduplicated works", "The frozen ledger contains 2,216 deduplicated works")
    root_readme = re.sub(r"\| `corpus/set1_core.csv` \| \d+ \|", "| `corpus/set1_core.csv` | 105 |", root_readme)
    root_readme = re.sub(r"\| `corpus/set2_emerging.csv` \| \d+ \|", "| `corpus/set2_emerging.csv` | 121 |", root_readme)
    root_readme = re.sub(r"\| `corpus/set3_context.csv` \| \d+ \|", f"| `corpus/set3_context.csv` | {counts['set3_context']} |", root_readme)
    root_readme = re.sub(r"\| `corpus/screened_out.csv` \| [\d,]+ \|", f"| `corpus/screened_out.csv` | {counts['screened_out']:,} |", root_readme)
    root_readme = root_readme.replace("together form the 232-work MAS-security corpus", "together form the 226-work MAS-security corpus")
    root_readme += "\nThe 2026-08-18 evaluation and benchmark reconciliation freezes the active corpus at 226 works. `corpus/manual_review_queue_2026-08-18.csv` contains all active works for named-author signoff.\n"
    (ROOT / "README.md").write_text(root_readme,encoding="utf-8")

    snap_path = ROOT / "FROZEN_SNAPSHOT.md"; snap = snap_path.read_text(encoding="utf-8")
    snap = re.sub(r"\| Set 1 \| \d+ \|", "| Set 1 | 105 |", snap)
    snap = re.sub(r"\| Set 2 \| \d+ \|", "| Set 2 | 121 |", snap)
    snap = re.sub(r"\| Set 3 \| \d+ \|", f"| Set 3 | {counts['set3_context']} |", snap)
    snap = re.sub(r"\| Screened out \| [\d,]+ \|", f"| Screened out | {counts['screened_out']:,} |", snap)
    snap = snap.replace("Set 1 plus Set 2 is the 232-work MAS-security corpus.", "Set 1 plus Set 2 is the 226-work MAS-security corpus.")
    snap += f"""

## 2026-08-18 evaluation and benchmark reconciliation revision

All 44 evaluation-primary works were re-adjudicated: 27 remain active and 17 move to context. The 44-paper benchmark analysis set was then reconciled against canonical identities, adding/promoting 12 security-relevant works into the active corpus, moving one additional unique active work (`Deliberation and drift`) to context, correcting two dominant-contribution labels, and canonicalizing the MASLeak arXiv/USENIX version chain. A2ASecBench already existed in the deduplicated review ledger and is promoted rather than added, so the review universe remains 2,216 works.

The resulting frozen partition is Set 1 = 105, Set 2 = 121, Set 3 = {counts['set3_context']}, screened out = {counts['screened_out']:,}, for a 226-work MAS-security corpus. All 226 active rows are exported to `corpus/manual_review_queue_2026-08-18.csv` and remain pending named-author signoff.
"""
    snap_path.write_text(snap,encoding="utf-8")

    # Freeze validator to actual reconciled counts.
    validator = f'''#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={{"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}}
EXPECTED={counts!r}; E1={exp1!r}; E2={exp2!r}
def rows(p):
    with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={{k:rows(v) for k,v in FILES.items()}}; actual={{k:len(v) for k,v in S.items()}}
if actual!=EXPECTED: raise SystemExit(f"frozen counts changed: {{actual}} != {{EXPECTED}}")
K={{k:{{r["work_key"] for r in v}} for k,v in S.items()}}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {{a}} {{b}}")
L=rows("review_ledger.csv")
if len(L)!=2216 or set().union(*K.values())!={{r["work_key"] for r in L}}: raise SystemExit("ledger partition mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
if len(rows("manual_review_queue_2026-08-18.csv"))!=226: raise SystemExit("manual queue incomplete")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=226 or m["search_universe"]!=2216: raise SystemExit("manifest mismatch")
print(f"Frozen corpus valid: Set1=105 Set2=121 Set3={{actual['set3_context']}} screened={{actual['screened_out']}} active=226 universe=2216")
'''
    (ROOT/"scripts"/"validate_three_set_corpus.py").write_text(validator,encoding="utf-8")

    print(json.dumps({"counts":counts,"active":226,"universe":2216,"A2A_previous_set":changes.get("li2026a2asecbench",{}).get("previous_membership"),"set1_contributions":s1,"set2_contributions":s2,"changed_rows":len(changes)},indent=2,sort_keys=True))
    return 0

if __name__ == "__main__": raise SystemExit(main())
