#!/usr/bin/env python3
"""Apply the later secondary review after the complete 228-row classification.

The ten rechecked membership decisions already agree with the complete human
classification. This reconciliation therefore preserves all Set 1/2/3 and
contribution decisions and applies only the later canonical-identity merge plus
explicit precedence/provenance metadata.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
DUP = "doi:10.2139/ssrn.6884338"
CANON = "doi:10.2139/ssrn.6996678"
CONFIRMED = CORPUS / "adjudication" / "confirmed_membership_revision_2026-08-21.csv"


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or ()), [dict(r) for r in reader]


def write_csv(path: Path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def append_once(value: str, text: str) -> str:
    value = (value or "").strip()
    return value if text in value else f"{value} {text}".strip()


def update_docs():
    root = ROOT / "README.md"
    text = root.read_text(encoding="utf-8")
    text = text.replace("**screened out = 1,550**", "**screened out = 1,549**", 1)
    text = text.replace("2,214 deduplicated works", "2,213 deduplicated works", 1)
    text = text.replace("| `corpus/screened_out.csv` | 1,550 |", "| `corpus/screened_out.csv` | 1,549 |", 1)
    text = text.replace("all 2,214 frozen-review works", "all 2,213 frozen-review works", 1)
    section = """

## 2026-08-21 secondary-review precedence correction

The complete 228-row human classification is applied first. The later named
secondary review is authoritative for its ten rechecked membership decisions;
those decisions agree with the complete classification. The later identity
review also merges DOI `10.2139/ssrn.6884338` into canonical DOI
`10.2139/ssrn.6996678`. The active corpus therefore remains **Set 1 = 96** and
**Set 2 = 105** (201 works), with **Set 3 = 463**. Removing the duplicate from
the canonical denominator leaves **1,549 screened-out works** and a **2,213-work
frozen review universe**. Source/evidence verification remains separate.
"""
    if "## 2026-08-21 secondary-review precedence correction" not in text:
        text += section
    root.write_text(text, encoding="utf-8")

    frozen = ROOT / "FROZEN_SNAPSHOT.md"
    text = frozen.read_text(encoding="utf-8")
    text = text.replace("| Screened out | 1,550 |", "| Screened out | 1,549 |", 1)
    text = text.replace("| Frozen review universe | 2,214 |", "| Frozen review universe | 2,213 |", 1)
    section = """

## 2026-08-21 secondary-review precedence correction

The complete 228-row human classification is applied first. The later named
secondary review is authoritative for its ten rechecked membership decisions,
which agree with the complete classification. Its identity review additionally
merges DOI `10.2139/ssrn.6884338` into canonical DOI
`10.2139/ssrn.6996678`. The final canonical partition is **Set 1 = 96, Set 2 =
105, Set 3 = 463, screened out = 1,549**, for a **2,213-work frozen review
universe** and a **201-work MAS-security corpus**.
"""
    if "## 2026-08-21 secondary-review precedence correction" not in text:
        text += section
    frozen.write_text(text, encoding="utf-8")

    c = CORPUS / "README.md"
    text = c.read_text(encoding="utf-8")
    text = text.replace("| `screened_out.csv` | 1,550 |", "| `screened_out.csv` | 1,549 |", 1)
    old = """Reviewer `expiol` completed named scope and dominant-contribution classification
for the 228-row manual cohort on 2026-08-21. The resulting active corpus contains
201 works. Source/evidence verification remains separate, and these decisions
must not be described as full evidence verification."""
    new = """Reviewer `expiol` completed named scope and dominant-contribution classification
for the 228-row manual cohort on 2026-08-21. A later secondary review rechecked
ten membership decisions; those decisions agree with the complete classification
and are authoritative for the rechecked records. The later review also merged one
obsolete SSRN DOI into its canonical record. The active corpus remains 201 works.
Source/evidence verification remains separate."""
    if old not in text:
        raise SystemExit("corpus README signoff paragraph not found")
    c.write_text(text.replace(old, new, 1), encoding="utf-8")


def main():
    # Confirm that the later ten membership decisions agree with the complete classification.
    _, confirmed = read_csv(CONFIRMED)
    if len(confirmed) != 11:
        raise SystemExit(f"expected 11 later-review rows, found {len(confirmed)}")

    ledger_path = CORPUS / "review_ledger.csv"
    lf, ledger = read_csv(ledger_path)
    if len(ledger) != 2214:
        raise SystemExit(f"expected 2214 pre-reconciliation ledger rows, found {len(ledger)}")
    by_key = {r["work_key"]: r for r in ledger}
    if DUP not in by_key or CANON not in by_key:
        raise SystemExit("duplicate/canonical SSRN rows not both present")

    for d in confirmed:
        if d["action"] == "merge_duplicate":
            continue
        key = d["work_key"]
        if key not in by_key:
            raise SystemExit(f"later-review record missing: {key}")
        if by_key[key]["evidence_set"] != d["adjudicated_membership"]:
            raise SystemExit(
                f"precedence conflict for {key}: complete={by_key[key]['evidence_set']} "
                f"later={d['adjudicated_membership']}"
            )
        note = (
            "2026-08-21 later secondary membership review by expiol confirmed "
            f"evidence_set={d['adjudicated_membership']}; later review is authoritative for this record."
        )
        by_key[key]["decision_reason"] = append_once(by_key[key].get("decision_reason", ""), note)
        reviewer = by_key[key].get("reviewer", "")
        tag = "expiol, later secondary membership review"
        if tag not in reviewer:
            by_key[key]["reviewer"] = f"{reviewer}; {tag}".strip("; ")
        by_key[key]["reviewed_at"] = "2026-08-21"
        by_key[key]["author_signoff_required"] = "no"

    by_key[CANON]["decision_reason"] = append_once(
        by_key[CANON].get("decision_reason", ""),
        f"2026-08-21 later identity review retained {CANON} and merged alias {DUP}.",
    )
    ledger = [r for r in ledger if r["work_key"] != DUP]
    write_csv(ledger_path, lf, sorted(ledger, key=lambda r: r["work_key"]))

    # The duplicate lived in screened_out, so the active corpus and Set 3 stay unchanged.
    screened_path = CORPUS / "screened_out.csv"
    sf, screened = read_csv(screened_path)
    matches = [r for r in screened if r["work_key"] == DUP]
    if len(matches) != 1:
        raise SystemExit(f"expected duplicate once in screened_out, found {len(matches)}")
    screened = [r for r in screened if r["work_key"] != DUP]
    if len(screened) != 1549:
        raise SystemExit(f"unexpected screened_out size {len(screened)}")
    write_csv(screened_path, sf, screened)

    # Discovery provenance points the old DOI at the retained canonical record.
    routes_path = CORPUS / "routes.csv"
    rf, routes = read_csv(routes_path)
    changed = 0
    for r in routes:
        if r.get("work_key") == DUP:
            r["work_key"] = CANON
            r["canonical_paper_id"] = CANON
            r["ledger_decision"] = "exclude"
            r["ledger_decision_source"] = "confirmed-membership-revision:2026-08-21"
            r["human_signoff_required"] = "no"
            changed += 1
    if changed != 1:
        raise SystemExit(f"expected one duplicate route, changed {changed}")
    write_csv(routes_path, rf, routes)

    # The alias tables from the later direct commit must remain present.
    _, aliases = read_csv(CORPUS / "identifier_aliases.csv")
    alias = [r for r in aliases if r.get("identifier") == "10.2139/ssrn.6884338"]
    if len(alias) != 1 or alias[0].get("work_key") != CANON or alias[0].get("identifier_status") != "alias":
        raise SystemExit("identifier_aliases does not preserve the later canonical mapping")

    # Retain the human exclusion row as provenance, but mark it as a duplicate identity.
    structured_path = CORPUS / "sets" / "01_search_catalog" / "structured_exclusions.csv"
    xf, rows = read_csv(structured_path)
    item = [r for r in rows if r.get("paper_id") == "doi_10_2139_ssrn_6884338"]
    if len(item) != 1:
        raise SystemExit("duplicate structured-exclusion row missing")
    item = item[0]
    item["reason_code"] = "duplicate_identifier_record"
    item["reason"] = "Duplicate DOI record removed from the canonical denominator and merged into the retained SSRN record."
    item["canonical_paper_id"] = CANON
    item["source"] = "corpus/adjudication/confirmed_membership_revision_2026-08-21.csv"
    write_csv(structured_path, xf, rows)

    # Preserve every human classification and contribution count; only the screened denominator changes.
    summary_path = CORPUS / "summary.csv"
    mf, summary = read_csv(summary_path)
    found = False
    for r in summary:
        if r["metric"] == "evidence_set" and r["label"] == "screened_out":
            r["count"] = "1549"
            found = True
    if not found:
        raise SystemExit("screened_out summary row missing")
    write_csv(summary_path, mf, summary)

    update_docs()

    # Update validator without weakening any human-classification invariant.
    vp = ROOT / "scripts" / "validate_three_set_corpus.py"
    v = vp.read_text(encoding="utf-8")
    v = v.replace("'screened_out':1550", "'screened_out':1549")
    v = v.replace("len(L)!=2214", "len(L)!=2213")
    v = v.replace("m[\"search_universe\"]!=2214", "m[\"search_universe\"]!=2213")
    old = """for r in A:\n  expected={\"accept\":r[\"previous_membership\"],\"move_set3\":\"set3_context\",\"exclude\":\"screened_out\"}[r[\"human_scope_decision\"]]\n  if r[\"adjudicated_membership\"]!=expected or LB[r[\"work_key\"]][\"evidence_set\"]!=expected: raise SystemExit(f\"classification application mismatch: {r['work_key']}\")\n  if r[\"human_contribution_decision\"] and LB[r[\"work_key\"]][\"dominant_contribution\"]!=r[\"human_contribution_decision\"]: raise SystemExit(f\"contribution application mismatch: {r['work_key']}\")\n"""
    new = """for r in A:\n  expected={\"accept\":r[\"previous_membership\"],\"move_set3\":\"set3_context\",\"exclude\":\"screened_out\"}[r[\"human_scope_decision\"]]\n  if r[\"work_key\"]==\"doi:10.2139/ssrn.6884338\":\n    if r[\"adjudicated_membership\"]!=\"screened_out\" or \"doi:10.2139/ssrn.6884338\" in LB or \"doi:10.2139/ssrn.6996678\" not in LB: raise SystemExit(\"duplicate identity reconciliation mismatch\")\n    continue\n  if r[\"adjudicated_membership\"]!=expected or LB[r[\"work_key\"]][\"evidence_set\"]!=expected: raise SystemExit(f\"classification application mismatch: {r['work_key']}\")\n  if r[\"human_contribution_decision\"] and LB[r[\"work_key\"]][\"dominant_contribution\"]!=r[\"human_contribution_decision\"]: raise SystemExit(f\"contribution application mismatch: {r['work_key']}\")\n"""
    if old not in v:
        raise SystemExit("classification-validation loop not found")
    v = v.replace(old, new)
    v = v.replace("screened=1550 active=201 universe=2214", "screened=1549 active=201 universe=2213")
    vp.write_text(v, encoding="utf-8")

    # The ledger builder should also know the combined canonical denominator.
    rp = ROOT / "scripts" / "rebuild_membership_from_ledger.py"
    rtext = rp.read_text(encoding="utf-8")
    if "if len(ledger) != 2214:" in rtext:
        rp.write_text(rtext.replace("if len(ledger) != 2214:", "if len(ledger) != 2213:"), encoding="utf-8")

    # Preserve the existing manifest history/inventory and update only affected current-state fields.
    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["counts"]["screened_out"] = 1549
    manifest["search_universe"] = 2213
    manifest["secondary_membership_review_revision"] = {
        "date": "2026-08-21",
        "ledger": "adjudication/confirmed_membership_revision_2026-08-21.csv",
        "reviewer": "expiol",
        "precedence": "applied after manual_corpus_classification_signoff_revision",
        "membership_rechecks": 10,
        "duplicate_identity_merges": 1,
        "canonical_duplicate_removed": DUP,
        "canonical_record_retained": CANON,
        "source_evidence_verified": False,
    }

    changed_files = {
        "review_ledger.csv": ledger_path,
        "routes.csv": routes_path,
        "screened_out.csv": screened_path,
        "summary.csv": summary_path,
        "sets/01_search_catalog/structured_exclusions.csv": structured_path,
        "adjudication/confirmed_membership_revision_2026-08-21.csv": CONFIRMED,
    }
    files = manifest.setdefault("files", {})
    for name, path in changed_files.items():
        _, data = read_csv(path)
        files[name] = {"sha256": sha256(path), "rows": len(data)}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "set1": 96,
        "set2": 105,
        "active": 201,
        "set3": 463,
        "screened_out": 1549,
        "review_universe": 2213,
        "attack_primary_set1": 24,
        "attack_primary_set2": 18,
    }, indent=2))


if __name__ == "__main__":
    main()
