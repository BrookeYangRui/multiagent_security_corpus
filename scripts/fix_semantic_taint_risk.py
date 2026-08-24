#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "corpus" / "set2_emerging.csv"
rows = []
with path.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        if row["work_key"] == "doi:10.5281/zenodo.20834834":
            row["risk_or_property"] = "R5_private_data_leakage"
            row["primary_url"] = "https://zenodo.org/records/20834835"
            reason = row.get("decision_reason", "")
            correction = " 2026-08-24 source-review correction: primary violated property is confidentiality/private-data leakage (R5); propagation is the mechanism, not the terminal risk. Zenodo version DOI 10.5281/zenodo.20834835 published 2026-06-24."
            if correction.strip() not in reason:
                row["decision_reason"] = (reason + correction).strip()
            membership = row.get("membership_reason", "")
            if "R5_private_data_leakage" not in membership:
                row["membership_reason"] = (membership + " Source-confirmed indirect-injection and inter-agent semantic-flow defense protects sensitive records from unauthorized disclosure.").strip()
        rows.append(row)

matches = [r for r in rows if r["work_key"] == "doi:10.5281/zenodo.20834834"]
if len(matches) != 1:
    raise SystemExit(f"expected one Semantic Taint row, found {len(matches)}")
if matches[0]["risk_or_property"] != "R5_private_data_leakage":
    raise SystemExit("risk correction failed")

with path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
print("Corrected Semantic Taint Propagation to R5_private_data_leakage")
