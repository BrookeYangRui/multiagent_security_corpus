#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
OUT = CORPUS / "section4_audit_view.csv"

fields = [
    "work_key", "title", "evidence_set", "year", "venue", "primary_url",
    "interaction_interfaces", "risk_or_property", "interaction_dependence",
    "scope_reason", "evidence_basis", "paper_section", "decision_reason",
]

rows = []
for name in ("set1_core.csv", "set2_emerging.csv"):
    with (CORPUS / name).open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append({k: row.get(k, "") for k in fields})

assert len(rows) == 201, len(rows)
with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {OUT}")
