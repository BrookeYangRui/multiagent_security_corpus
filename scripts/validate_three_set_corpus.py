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


def citations(row):
    try:
        return int(float((row.get("frozen_citation_count") or "0").replace(",", "")))
    except ValueError:
        return 0


sets = {name: rows(filename) for name, filename in FILES.items()}
keys = {name: {row["work_key"] for row in data} for name, data in sets.items()}
for left in keys:
    for right in keys:
        if left < right and keys[left] & keys[right]:
            raise SystemExit(f"sets overlap: {left} and {right}")

ledger = rows("review_ledger.csv")
if len(ledger) != 2217:
    raise SystemExit(f"review ledger changed size: {len(ledger)}")
if set().union(*keys.values()) != {row["work_key"] for row in ledger}:
    raise SystemExit("sets do not partition review_ledger.csv")

for row in sets["set1_core"]:
    mature = row.get("peer_reviewed") == "yes" or citations(row) >= 10
    if row.get("strict_scope_pass") != "yes" or not mature or row.get("maturity_rule_pass") != "yes":
        raise SystemExit(f"Set 1 contains an ineligible row: {row.get('work_key')}")
    if row.get("taxonomy_ready") not in {"yes", "no"}:
        raise SystemExit("Set 1 lacks an explicit taxonomy_ready flag")

for row in sets["set2_emerging"]:
    mature = row.get("peer_reviewed") == "yes" or citations(row) >= 10
    if row.get("strict_scope_pass") != "yes" or mature or row.get("maturity_rule_pass") != "no":
        raise SystemExit(f"Set 2 violates scope or maturity: {row.get('work_key')}")
    if row.get("taxonomy_ready") not in {"yes", "no"}:
        raise SystemExit("Set 2 lacks an explicit taxonomy_ready flag")

for row in sets["set3_context"]:
    if row.get("strict_scope_pass") == "yes":
        raise SystemExit(f"Set 3 contains an in-scope corpus work: {row.get('work_key')}")
    if not row.get("citation_role"):
        raise SystemExit(f"Set 3 row lacks a citation role: {row.get('work_key')}")

for row in sets["screened_out"]:
    if row.get("strict_scope_pass") == "yes":
        raise SystemExit(f"screened_out contains an in-scope corpus work: {row.get('work_key')}")

for old in ("primary.csv", "secondary.csv", "pending.csv", "exclude.csv", "review_queue.csv", "decision_ledger.csv"):
    if (C/old).exists():
        raise SystemExit(f"legacy active file remains: {old}")

manifest = json.loads((C/"manifest.json").read_text(encoding="utf-8"))
actual = {name: len(data) for name, data in sets.items()}
if manifest["counts"] != actual:
    raise SystemExit("manifest counts do not match")
if manifest.get("set1_maturity_rule") != "peer_reviewed == yes OR frozen_citation_count >= 10":
    raise SystemExit("manifest has the wrong Set 1 maturity rule")
if manifest.get("citation_threshold") != "at least 10":
    raise SystemExit("manifest has the wrong citation threshold")

inventory = manifest.get("source_file_inventory") or []
if sum(int(item.get("rows", 0)) for item in inventory) < 1000:
    raise SystemExit("source-review inventory is incomplete")

print(
    "Three-set corpus valid: "
    f"Set 1={actual['set1_core']}, Set 2={actual['set2_emerging']}, "
    f"Set 3={actual['set3_context']}, screened out={actual['screened_out']}; "
    f"taxonomy-ready Set 1={manifest.get('taxonomy_ready_set1_count', 0)}"
)
