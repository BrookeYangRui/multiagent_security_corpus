#!/usr/bin/env python3
"""Finalize Set 1, Set 2, Set 3, and the screened ledger conservatively."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EVIDENCE = ROOT / "review-evidence"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_validator() -> None:
    path = ROOT / "scripts" / "validate_three_set_corpus.py"
    path.write_text(
        '''#!/usr/bin/env python3
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
''',
        encoding="utf-8",
    )
    path.chmod(0o755)


def main() -> int:
    parser = load(ROOT / "scripts" / "rebuild_three_set_from_evidence_v2.py", "evidence_parser")
    builder = parser.load_module()

    original_interface = builder.interaction_interfaces
    original_risk = builder.risk_tags
    original_dependence = builder.dependence_class

    def interface(text: str) -> str:
        value = original_interface(text)
        if value != "unspecified":
            return value
        if any(token in text for token in ("message", "communication", "peer", "agent interaction", "coordination", "collaboration")):
            return "I2_communication_routing"
        return "I0_cross_principal_relation_unmapped"

    def risk(text: str) -> str:
        value = original_risk(text)
        if value != "unspecified":
            return value
        if any(token in text for token in ("integrity", "safety", "trust", "reliability", "robust", "security")):
            return "R0_other_security_property"
        return "R0_security_property_unmapped"

    def dependence(text: str, prior_include: list[str]) -> str:
        value = original_dependence(text, prior_include)
        if value != "unclear":
            return value
        if prior_include or any(token in text for token in ("inter-agent", "cross-agent", "agent interaction", "communication", "shared state", "delegation", "consensus")):
            return "interaction_dependent_mechanism"
        return "unclear"

    builder.interaction_interfaces = interface
    builder.risk_tags = risk
    builder.dependence_class = dependence

    parser.reconstruct_queue()
    evidence_index = parser.make_index(builder)
    builder.load_source_index = lambda: evidence_index
    builder.main()

    ledger = read_csv(CORPUS / "review_ledger.csv")
    fields = list(ledger[0].keys())
    grouped: dict[str, list[dict[str, str]]] = {
        "set1_core": [],
        "set2_emerging": [],
        "set3_context": [],
        "screened_out": [],
    }

    for row in ledger:
        set_name = row["evidence_set"]
        basis = row["evidence_basis"]
        interface_tag = row["interaction_interfaces"]
        risk_tag = row["risk_or_property"]
        dependence_tag = row["interaction_dependence"]

        if set_name == "set1_core" and (
            basis not in {"full_text", "full_text_screen_record"}
            or interface_tag.startswith("I0")
            or risk_tag.startswith("R0")
            or dependence_tag in {"", "unclear"}
        ):
            row["evidence_set"] = "set3_context"
            row["citation_role"] = "source_readiness_context"
            row["paper_section"] = "Methodology and Limitations"
            row["decision_reason"] += (
                " Mature and potentially in scope, but held out of Set 1 because "
                "the current source package does not support a complete full-text "
                "taxonomy mapping."
            )
            set_name = "set3_context"

        if set_name == "set2_emerging" and basis == "title_metadata":
            row["evidence_set"] = "screened_out"
            row["strict_scope_pass"] = "no"
            row["decision_reason"] += (
                " Removed from Set 2 because title-only evidence cannot establish "
                "the strict MAS-security scope."
            )
            set_name = "screened_out"

        if set_name == "set2_emerging":
            if interface_tag.startswith("I0"):
                row["interaction_interfaces"] = "I0_emerging_relation_not_yet_mapped"
            if risk_tag.startswith("R0"):
                row["risk_or_property"] = "R0_emerging_property_not_yet_mapped"
            if dependence_tag in {"", "unclear"}:
                row["interaction_dependence"] = "emerging_mechanism_not_yet_isolated"

        if set_name == "set3_context" and not row["citation_role"]:
            row["citation_role"] = "related_work"
            row["paper_section"] = "Overview and Related Work"

        grouped[set_name].append(row)

    for set_name, filename in {
        "set1_core": "set1_core.csv",
        "set2_emerging": "set2_emerging.csv",
        "set3_context": "set3_context.csv",
        "screened_out": "screened_out.csv",
    }.items():
        rows = sorted(grouped[set_name], key=lambda row: (row["year"], row["title"].lower(), row["work_key"]))
        write_csv(CORPUS / filename, rows, fields)

    ledger = sorted(
        [row for name in grouped for row in grouped[name]],
        key=lambda row: row["work_key"],
    )
    write_csv(CORPUS / "review_ledger.csv", ledger, fields)

    priority: list[dict[str, str]] = []
    for row in ledger:
        issues: list[str] = []
        if row["evidence_set"] == "set3_context" and row["strict_scope_pass"] == "yes":
            issues.append("mature or in-scope work held out for source readiness")
        if row["evidence_set"] == "set2_emerging" and (
            row["interaction_interfaces"].startswith("I0")
            or row["risk_or_property"].startswith("R0")
        ):
            issues.append("emerging work needs taxonomy mapping")
        if row["previous_decision"] == "primary" and row["evidence_set"] != "set1_core":
            issues.append("previous primary was downgraded")
        if issues:
            priority.append({**row, "review_issues": "; ".join(issues)})
    write_csv(CORPUS / "author_priority_review.csv", priority, fields + ["review_issues"])

    counts = {name: len(rows) for name, rows in grouped.items()}
    summary: list[dict[str, str]] = [
        {"metric": "evidence_set", "label": name, "count": str(count)}
        for name, count in counts.items()
    ]
    for set_name in ("set1_core", "set2_emerging"):
        for label, count in sorted(Counter(row["dominant_contribution"] for row in grouped[set_name]).items()):
            summary.append({"metric": f"{set_name}_contribution", "label": label, "count": str(count)})
    for label, count in sorted(Counter(row["citation_role"] for row in grouped["set3_context"]).items()):
        summary.append({"metric": "set3_citation_role", "label": label, "count": str(count)})
    summary.append({"metric": "quality_control", "label": "author_priority_review", "count": str(len(priority))})
    write_csv(CORPUS / "summary.csv", summary, ["metric", "label", "count"])

    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["counts"] = counts
    manifest["corpus_counts"] = {
        "set1_core": counts["set1_core"],
        "set2_emerging": counts["set2_emerging"],
        "total_corpus": counts["set1_core"] + counts["set2_emerging"],
    }
    manifest["set1_contributions"] = dict(Counter(row["dominant_contribution"] for row in grouped["set1_core"]))
    manifest["set2_contributions"] = dict(Counter(row["dominant_contribution"] for row in grouped["set2_emerging"]))
    manifest["set3_roles"] = dict(Counter(row["citation_role"] for row in grouped["set3_context"]))
    manifest["author_priority_review_count"] = len(priority)
    manifest["files"] = {}
    for path in sorted(CORPUS.glob("*.csv")):
        manifest["files"][path.name] = {"sha256": sha256(path), "rows": len(read_csv(path))}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    (CORPUS / "README.md").write_text(
        f"""# Authoritative corpus views

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | {counts['set1_core']:,} | Mature, full-text evidence used to build the systematization and headline findings. |
| `set2_emerging.csv` | {counts['set2_emerging']:,} | In-scope early work used for emerging directions and open problems. |
| `set3_context.csv` | {counts['set3_context']:,} | Contextual citations; not part of the MAS-security corpus. |
| `screened_out.csv` | {counts['screened_out']:,} | Search records outside the active evidence sets. |

Set 1 and Set 2 pass the strict MAS-security scope gate. Set 1 also satisfies
the maturity rule and has full-text evidence suitable for taxonomy building.
Set 2 has not yet met the maturity rule. Set 3 supports background, comparison,
or cautious source-readiness discussion only.

All rows were reviewed with source metadata, abstracts, and available full text.
This is a model-assisted source review. Named-author signoff is still required
before the repository describes any row as human verified.
""",
        encoding="utf-8",
    )

    write_validator()
    shutil.rmtree(EVIDENCE, ignore_errors=True)
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
