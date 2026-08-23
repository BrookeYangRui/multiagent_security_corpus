#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "corpus"

def rows(name):
    with (C / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

s1 = rows("set1_core.csv")
s2 = rows("set2_emerging.csv")
if (len(s1), len(s2)) != (96, 105):
    raise SystemExit(f"authoritative counts changed: {len(s1)}/{len(s2)}")
all_rows = s1 + s2
if len(all_rows) != 201:
    raise SystemExit("active corpus is not 201")
keys = [r["work_key"] for r in all_rows]
if len(keys) != len(set(keys)):
    raise SystemExit("duplicate work_key in active corpus")
if any(r.get("strict_scope_pass") != "yes" for r in all_rows):
    raise SystemExit("out of scope row in active corpus")
if any(r.get("maturity_rule_pass") != "yes" for r in s1):
    raise SystemExit("invalid Set 1 maturity")
if any(r.get("maturity_rule_pass") != "no" for r in s2):
    raise SystemExit("invalid Set 2 maturity")
expected = {"attack": 42, "defense": 94, "evaluation": 44, "general": 11, "survey": 10}
if dict(Counter(r["dominant_contribution"] for r in all_rows)) != expected:
    raise SystemExit("signed contribution counts changed")
stale = [
    "set3_context.csv", "screened_out.csv", "review_ledger.csv", "routes.csv",
    "manual_review_queue_2026-08-18.csv", "author_priority_review.csv",
    "identifier_aliases.csv", "identifier_alias_overrides.csv", "adjudication", "sets"
]
if any((C / p).exists() for p in stale):
    raise SystemExit("superseded corpus artifact is still present")
m = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
if m["counts"] != {"set1_core": 96, "set2_emerging": 105, "total_corpus": 201}:
    raise SystemExit("manifest mismatch")
print("Final corpus valid: Set1=96 Set2=105 total=201")
