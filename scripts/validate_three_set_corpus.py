#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}
EXPECTED={'set1_core':96,'set2_emerging':105,'set3_context':463,'screened_out':1550}
E1={'attack':24,'defense':40,'evaluation':22,'general':5,'survey':5}
E2={'attack':18,'defense':54,'evaluation':22,'general':6,'survey':5}
def rows(p):
    with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={k:rows(v) for k,v in FILES.items()}; actual={k:len(v) for k,v in S.items()}
if actual!=EXPECTED: raise SystemExit(f"signed counts changed: {actual} != {EXPECTED}")
K={k:{r["work_key"] for r in v} for k,v in S.items()}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {a} {b}")
L=rows("review_ledger.csv"); LB={r["work_key"]:r for r in L}
if len(L)!=2214 or set().union(*K.values())!=set(LB): raise SystemExit("ledger partition mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
Q=rows("manual_review_queue_2026-08-18.csv")
if len(Q)!=228 or Counter(r["human_scope_decision"] for r in Q)!={"accept":201,"move_set3":18,"exclude":9}: raise SystemExit("manual classification queue mismatch")
A=rows("adjudication/manual_corpus_classification_2026-08-21.csv")
if len(A)!=228 or any(r["reviewer"]!="expiol" or r["source_evidence_verified"]!="no" for r in A): raise SystemExit("classification audit mismatch")
X=rows("sets/01_search_catalog/structured_exclusions.csv")
if len(X)!=9 or any(r["decision"]!="exclude" or r["reviewer"]!="expiol" for r in X): raise SystemExit("structured exclusions mismatch")
for r in A:
  expected={"accept":r["previous_membership"],"move_set3":"set3_context","exclude":"screened_out"}[r["human_scope_decision"]]
  if r["adjudicated_membership"]!=expected or LB[r["work_key"]]["evidence_set"]!=expected: raise SystemExit(f"classification application mismatch: {r['work_key']}")
  if r["human_contribution_decision"] and LB[r["work_key"]]["dominant_contribution"]!=r["human_contribution_decision"]: raise SystemExit(f"contribution application mismatch: {r['work_key']}")
signoff=rows("adjudication/manual_signoff_changes_2026-08-18.csv")
if len(signoff)!=32 or Counter(r["human_decision"] for r in signoff)!={"approve":30,"reject":2}: raise SystemExit("changed-decision signoff mismatch")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=201 or m["search_universe"]!=2214: raise SystemExit("manifest mismatch")
print("Human-classified corpus valid: Set1=96 Set2=105 Set3=463 screened=1550 active=201 universe=2214 scope=201/18/9 source_evidence_verified=no")
