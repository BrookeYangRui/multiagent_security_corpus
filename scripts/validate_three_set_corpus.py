#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}
EXPECTED={"set1_core":104,"set2_emerging":112,"set3_context":452,"screened_out":1546}
E1={"attack":33,"defense":38,"evaluation":21,"general":7,"survey":5}
E2={"attack":35,"defense":55,"evaluation":15,"general":4,"survey":3}
DUP="doi:10.2139/ssrn.6884338"; CAN="doi:10.2139/ssrn.6996678"
def rows(p):
  with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={k:rows(v) for k,v in FILES.items()}; actual={k:len(v) for k,v in S.items()}
if actual!=EXPECTED: raise SystemExit(f"confirmed counts changed: {actual} != {EXPECTED}")
K={k:{r["work_key"] for r in v} for k,v in S.items()}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {a} {b}")
L=rows("review_ledger.csv"); LB={r["work_key"]:r for r in L}
if len(L)!=2214 or set().union(*K.values())!=set(LB): raise SystemExit("ledger partition mismatch")
if DUP in LB or CAN not in LB: raise SystemExit("duplicate identity merge mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
Q=rows("manual_review_queue_2026-08-18.csv"); scopes=Counter(r["human_scope_decision"] for r in Q)
if len(Q)!=226 or scopes!={"":216,"move_set3":5,"exclude":5}: raise SystemExit(f"manual queue mismatch: {len(Q)} {scopes}")
if any(r["human_contribution_decision"] or r["human_notes"] for r in Q): raise SystemExit("membership revision changed contribution or notes")
A=rows("adjudication/confirmed_membership_revision_2026-08-21.csv")
if len(A)!=11 or Counter(r["action"] for r in A)!={"membership_signoff":10,"merge_duplicate":1}: raise SystemExit("revision audit mismatch")
if any(r["reviewer"]!="expiol" or r["source_evidence_verified"]!="no" for r in A): raise SystemExit("revision attribution mismatch")
X=rows("sets/01_search_catalog/structured_exclusions.csv")
if len(X)!=6 or any(r["decision"]!="exclude" or r["reviewer"]!="expiol" for r in X): raise SystemExit("structured exclusions mismatch")
if not any(r["reason_code"]=="duplicate_identifier_record" and r["canonical_paper_id"]==CAN for r in X): raise SystemExit("structured duplicate exclusion mismatch")
for r in A:
  if r["action"]!="membership_signoff": continue
  expected="set3_context" if r["human_scope_decision"]=="move_set3" else "screened_out"
  if r["adjudicated_membership"]!=expected or LB[r["work_key"]]["evidence_set"]!=expected: raise SystemExit(f"membership application mismatch: {r['work_key']}")
  if r["human_contribution_decision"] or r["previous_contribution"]!=r["adjudicated_contribution"] or LB[r["work_key"]]["dominant_contribution"]!=r["previous_contribution"]: raise SystemExit(f"contribution changed: {r['work_key']}")
O=rows("identifier_alias_overrides.csv")
if not any(r["alias_value"]=="10.2139/ssrn.6884338" and r["canonical_doi"]=="10.2139/ssrn.6996678" for r in O): raise SystemExit("alias override missing")
I=rows("identifier_aliases.csv")
if not any(r["identifier"]=="10.2139/ssrn.6884338" and r["work_key"]==CAN and r["identifier_status"]=="alias" for r in I): raise SystemExit("identifier alias mismatch")
T=rows("routes.csv")
if not any(r["route_id"]=="search:doi:10.2139/ssrn.6884338" and r["work_key"]==CAN for r in T): raise SystemExit("route alias mismatch")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=216 or m["search_universe"]!=2214: raise SystemExit("manifest mismatch")
print("Confirmed membership revision valid: Set1=104 Set2=112 Set3=452 screened=1546 active=216 universe=2214 signoff=5/5 duplicate_merges=1 source_evidence_verified=no")
