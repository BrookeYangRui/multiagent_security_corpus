#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}
EXPECTED={'set1_core': 105, 'set2_emerging': 122, 'set3_context': 447, 'screened_out': 1541}; E1={'attack': 33, 'defense': 39, 'evaluation': 21, 'general': 7, 'survey': 5}; E2={'attack': 38, 'defense': 61, 'evaluation': 16, 'general': 4, 'survey': 3}
def rows(p):
    with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={k:rows(v) for k,v in FILES.items()}; actual={k:len(v) for k,v in S.items()}
if actual!=EXPECTED: raise SystemExit(f"frozen counts changed: {actual} != {EXPECTED}")
K={k:{r["work_key"] for r in v} for k,v in S.items()}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {a} {b}")
L=rows("review_ledger.csv")
if len(L)!=2215 or set().union(*K.values())!={r["work_key"] for r in L}: raise SystemExit("ledger partition mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
if len(rows("manual_review_queue_2026-08-18.csv"))!=227: raise SystemExit("manual queue incomplete")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=227 or m["search_universe"]!=2215: raise SystemExit("manifest mismatch")
print(f"Frozen corpus valid: Set1=105 Set2=121 Set3={actual['set3_context']} screened={actual['screened_out']} active=227 universe=2216")
