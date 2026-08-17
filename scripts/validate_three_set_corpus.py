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
    with (C/name).open(encoding="utf-8-sig", newline="") as handle:
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
if len(ledger) != 2217:
    raise SystemExit(f"review ledger changed size: {len(ledger)}")
for row in sets["set1_core"]:
    if row["strict_scope_pass"] != "yes" or row["maturity_rule_pass"] != "yes":
        raise SystemExit("Set 1 contains an ineligible row")
    if row["evidence_basis"] not in {"full_text", "full_text_screen_record"}:
        raise SystemExit("Set 1 lacks full-text evidence")
    if row["interaction_interfaces"].startswith("I0") or row["risk_or_property"].startswith("R0"):
        raise SystemExit("Set 1 contains an unmapped tag")
    if row["interaction_dependence"] in {"", "unclear"}:
        raise SystemExit("Set 1 contains unclear interaction dependence")
for row in sets["set2_emerging"]:
    if row["strict_scope_pass"] != "yes" or row["maturity_rule_pass"] != "no":
        raise SystemExit("Set 2 violates the scope or maturity rule")
    if row["evidence_basis"] == "title_metadata":
        raise SystemExit("Set 2 contains title-only evidence")
for row in sets["set3_context"]:
    if not row["citation_role"]:
        raise SystemExit("Set 3 row lacks a citation role")
for old in ("primary.csv", "secondary.csv", "pending.csv", "exclude.csv", "review_queue.csv", "decision_ledger.csv"):
    if (C/old).exists():
        raise SystemExit(f"legacy active file remains: {old}")
manifest = json.loads((C/"manifest.json").read_text(encoding="utf-8"))
actual = {name: len(data) for name, data in sets.items()}
if manifest["counts"] != actual:
    raise SystemExit("manifest counts do not match")
inventory = manifest.get("source_file_inventory") or []
if sum(int(item.get("rows", 0)) for item in inventory) < 1000:
    raise SystemExit("source-review inventory is incomplete")
print(f"Three-set corpus valid: Set 1={actual['set1_core']}, Set 2={actual['set2_emerging']}, Set 3={actual['set3_context']}, screened out={actual['screened_out']}")
