#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
FILES = {
    "set1_core": "set1_core.csv",
    "set2_emerging": "set2_emerging.csv",
    "set3_context": "set3_context.csv",
    "screened_out": "screened_out.csv",
}
FROZEN_COUNTS = {
    "set1_core": 108,
    "set2_emerging": 132,
    "set3_context": 434,
    "screened_out": 1543,
}
FROZEN_SET1_CONTRIBUTIONS = {"attack": 33, "defense": 39, "evaluation": 22, "general": 5, "survey": 9}
FROZEN_SET2_CONTRIBUTIONS = {"attack": 38, "defense": 61, "evaluation": 22, "general": 4, "survey": 7}


def rows(name):
    with (C/name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def citations(row):
    try:
        return int(float((row.get("frozen_citation_count") or "0").replace(",", "")))
    except ValueError:
        return 0


sets = {name: rows(filename) for name, filename in FILES.items()}
actual = {name: len(data) for name, data in sets.items()}
if actual != FROZEN_COUNTS:
    raise SystemExit(f"frozen corpus partition changed: {actual} != {FROZEN_COUNTS}")

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

set1_contrib = Counter(row.get("dominant_contribution", "") for row in sets["set1_core"])
set2_contrib = Counter(row.get("dominant_contribution", "") for row in sets["set2_emerging"])
if {k: set1_contrib[k] for k in FROZEN_SET1_CONTRIBUTIONS} != FROZEN_SET1_CONTRIBUTIONS:
    raise SystemExit(f"Set 1 contribution distribution changed: {dict(set1_contrib)}")
if {k: set2_contrib[k] for k in FROZEN_SET2_CONTRIBUTIONS} != FROZEN_SET2_CONTRIBUTIONS:
    raise SystemExit(f"Set 2 contribution distribution changed: {dict(set2_contrib)}")
if set1_contrib["general"] + set2_contrib["general"] != 9:
    raise SystemExit("frozen residual general category must contain exactly 9 works")

adj1 = rows("adjudication/general_set1_2026-08-18.csv")
adj2 = rows("adjudication/general_set2_2026-08-18.csv")
if len(adj1) != 36 or len(adj2) != 73:
    raise SystemExit("frozen general adjudication ledgers are incomplete")

manifest = json.loads((C/"manifest.json").read_text(encoding="utf-8"))
if manifest["counts"] != actual:
    raise SystemExit("manifest counts do not match")
if manifest.get("corpus_counts", {}).get("total_corpus") != 240:
    raise SystemExit("manifest corpus total must be frozen at 240")
if manifest.get("set1_contributions") != FROZEN_SET1_CONTRIBUTIONS:
    raise SystemExit("manifest Set 1 contribution counts do not match the frozen revision")
if manifest.get("set2_contributions") != FROZEN_SET2_CONTRIBUTIONS:
    raise SystemExit("manifest Set 2 contribution counts do not match the frozen revision")
revision = manifest.get("adjudication_revision") or {}
if revision.get("date") != "2026-08-18" or revision.get("reviewed") != 109:
    raise SystemExit("manifest lacks the frozen 2026-08-18 adjudication revision")
if manifest.get("set1_maturity_rule") != "peer_reviewed == yes OR frozen_citation_count >= 10":
    raise SystemExit("manifest has the wrong Set 1 maturity rule")
if manifest.get("citation_threshold") != "at least 10":
    raise SystemExit("manifest has the wrong citation threshold")

inventory = manifest.get("source_file_inventory") or []
if sum(int(item.get("rows", 0)) for item in inventory) < 1000:
    raise SystemExit("source-review inventory is incomplete")

print(
    "Frozen three-set corpus valid: "
    f"Set 1={actual['set1_core']}, Set 2={actual['set2_emerging']}, "
    f"Set 3={actual['set3_context']}, screened out={actual['screened_out']}; "
    "MAS-security corpus=240; residual general=9"
)
