#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
FILES = {
    "set1_core": "set1_core.csv",
    "set2_emerging": "set2_emerging.csv",
    "set3_context": "set3_context.csv",
    "screened_out": "screened_out.csv",
}

def rows(name):
    with (C / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

sets = {name: rows(filename) for name, filename in FILES.items()}
keys = {name: {row["work_key"] for row in data} for name, data in sets.items()}
for left in keys:
    for right in keys:
        if left < right and keys[left] & keys[right]:
            raise SystemExit(f"sets overlap: {left} and {right}")
ledger = rows("review_ledger.csv")
if set().union(*keys.values()) != {row["work_key"] for row in ledger}:
    raise SystemExit("sets do not partition review_ledger.csv")
if any(row["strict_scope_pass"] != "yes" for row in sets["set1_core"] + sets["set2_emerging"]):
    raise SystemExit("Set 1 or Set 2 contains a scope failure")
if any(row["maturity_rule_pass"] != "yes" for row in sets["set1_core"]):
    raise SystemExit("Set 1 contains an immature work")
if any(row["maturity_rule_pass"] == "yes" for row in sets["set2_emerging"]):
    raise SystemExit("Set 2 contains a work that meets the Set 1 maturity rule")
if any(not row["citation_role"] for row in sets["set3_context"]):
    raise SystemExit("Set 3 row lacks a citation role")
for old in ("primary.csv", "secondary.csv", "pending.csv", "exclude.csv", "review_queue.csv", "decision_ledger.csv"):
    if (C / old).exists():
        raise SystemExit(f"legacy active file remains: {old}")
manifest = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
actual = {name: len(data) for name, data in sets.items()}
if manifest["counts"] != actual:
    raise SystemExit("manifest counts do not match the CSV files")
print(f"Three-set corpus valid: Set 1={actual['set1_core']}, Set 2={actual['set2_emerging']}, Set 3={actual['set3_context']}, screened out={actual['screened_out']}")
