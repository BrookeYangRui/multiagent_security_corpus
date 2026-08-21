#!/usr/bin/env python3
"""Rebuild the authoritative evidence sets from the frozen review ledger.

Membership and evidence readiness are deliberately separate:

* Set 1: in MAS-security scope and (peer reviewed OR frozen citations >= 10).
* Set 2: in MAS-security scope and not yet meeting the Set 1 maturity rule.
* Set 3: contextual literature outside the MAS-security corpus.
* screened_out: reviewed search records outside the corpus with no active context role.

Full-text taxonomy readiness is recorded in ``taxonomy_ready`` and never changes
Set 1 / Set 2 membership.  Interaction-dependence labels likewise describe the
strength/type of an interaction claim; they are not an inclusion gate.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"

SET_FILES = {
    "set1_core": "set1_core.csv",
    "set2_emerging": "set2_emerging.csv",
    "set3_context": "set3_context.csv",
    "screened_out": "screened_out.csv",
}
FULL_TEXT_BASES = {"full_text", "full_text_screen_record"}


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


def citation_count(row: dict[str, str]) -> int:
    raw = (row.get("frozen_citation_count") or "0").strip().replace(",", "")
    try:
        return int(float(raw))
    except ValueError:
        return 0


def taxonomy_ready(row: dict[str, str]) -> bool:
    basis = (row.get("evidence_basis") or "").strip()
    interface = (row.get("interaction_interfaces") or "").strip()
    risk = (row.get("risk_or_property") or "").strip()
    return (
        basis in FULL_TEXT_BASES
        and interface not in {"", "unspecified"}
        and risk not in {"", "unspecified"}
        and not interface.startswith("I0")
        and not risk.startswith("R0")
    )


def context_role(row: dict[str, str]) -> str:
    role = (row.get("citation_role") or "").strip()
    if role and role != "source_readiness_context":
        return role
    previous = (row.get("previous_category") or row.get("dominant_contribution") or "").strip()
    if previous == "survey":
        return "related_work"
    return "related_work"


def membership_reason(row: dict[str, str], set_name: str) -> str:
    peer = (row.get("peer_reviewed") or "unclear").strip()
    cites = citation_count(row)
    if set_name == "set1_core":
        return (
            f"Passed MAS-security scope. Maturity: peer_reviewed={peer}; "
            f"frozen_citations={cites}. Set 1 uses peer_reviewed=yes OR "
            "frozen_citation_count>=10; taxonomy readiness is tracked separately."
        )
    if set_name == "set2_emerging":
        return (
            f"Passed MAS-security scope. Maturity: peer_reviewed={peer}; "
            f"frozen_citations={cites}. Does not yet meet the Set 1 maturity rule."
        )
    if set_name == "set3_context":
        return "Outside the MAS-security corpus; retained for contextual citation use."
    return "Outside the MAS-security corpus and not retained as an active contextual citation."


def main() -> int:
    ledger_path = CORPUS / "review_ledger.csv"
    ledger = read_csv(ledger_path)
    if len(ledger) != 2214:
        raise SystemExit(f"unexpected review ledger size: {len(ledger)}")

    fields = list(ledger[0].keys())
    for field in ("taxonomy_ready", "membership_reason"):
        if field not in fields:
            fields.append(field)

    grouped: dict[str, list[dict[str, str]]] = {name: [] for name in SET_FILES}

    for original in ledger:
        row = dict(original)
        scope = (row.get("strict_scope_pass") or "no").strip().lower() == "yes"
        peer = (row.get("peer_reviewed") or "").strip().lower() == "yes"
        cites = citation_count(row)
        mature = peer or cites >= 10
        row["maturity_rule_pass"] = "yes" if mature else "no"
        row["taxonomy_ready"] = "yes" if taxonomy_ready(row) else "no"

        if scope:
            set_name = "set1_core" if mature else "set2_emerging"
            row["evidence_set"] = set_name
            # A prior source-readiness downgrade was not a context judgment.
            if (row.get("citation_role") or "") == "source_readiness_context":
                row["citation_role"] = ""
            if set_name in {"set1_core", "set2_emerging"} and (
                row.get("paper_section") == "Methodology and Limitations"
                and original.get("citation_role") == "source_readiness_context"
            ):
                row["paper_section"] = ""
        else:
            current = (row.get("evidence_set") or "").strip()
            role = (row.get("citation_role") or "").strip()
            if current == "set3_context" or role:
                set_name = "set3_context"
                row["evidence_set"] = set_name
                row["citation_role"] = context_role(row)
                if not (row.get("paper_section") or "").strip():
                    row["paper_section"] = "Overview and Related Work"
            else:
                set_name = "screened_out"
                row["evidence_set"] = set_name
                row["citation_role"] = ""

        row["membership_reason"] = membership_reason(row, set_name)
        grouped[set_name].append(row)

    # Deterministic row order in every public view.
    for set_name, filename in SET_FILES.items():
        rows = sorted(
            grouped[set_name],
            key=lambda row: (row.get("year", ""), row.get("title", "").lower(), row.get("work_key", "")),
        )
        write_csv(CORPUS / filename, rows, fields)

    ledger_out = sorted(
        [row for set_name in SET_FILES for row in grouped[set_name]],
        key=lambda row: row.get("work_key", ""),
    )
    write_csv(ledger_path, ledger_out, fields)

    # Keep the author-review queue focused on judgments that can affect paper claims.
    priority: list[dict[str, str]] = []
    for row in ledger_out:
        issues: list[str] = []
        if row["evidence_set"] == "set1_core" and row["taxonomy_ready"] != "yes":
            issues.append("mature corpus work needs taxonomy/source mapping")
        if row["evidence_set"] in {"set1_core", "set2_emerging"} and (
            (row.get("interaction_dependence") or "").strip() in {"", "unclear"}
        ):
            issues.append("interaction evidence strength needs review")
        if row["evidence_set"] in {"set1_core", "set2_emerging"} and (
            (row.get("interaction_interfaces") or "").startswith("I0")
            or (row.get("risk_or_property") or "").startswith("R0")
        ):
            issues.append("taxonomy tag needs review")
        if issues:
            priority.append({**row, "review_issues": "; ".join(issues)})

    priority_fields = fields + (["review_issues"] if "review_issues" not in fields else [])
    write_csv(CORPUS / "author_priority_review.csv", priority, priority_fields)

    summary: list[dict[str, str]] = [
        {"metric": "evidence_set", "label": name, "count": str(len(grouped[name]))}
        for name in SET_FILES
    ]
    for set_name in ("set1_core", "set2_emerging"):
        contributions = Counter((row.get("dominant_contribution") or "unclassified") for row in grouped[set_name])
        for label, count in sorted(contributions.items()):
            summary.append({"metric": f"{set_name}_contribution", "label": label, "count": str(count)})
    for label, count in sorted(Counter((row.get("citation_role") or "related_work") for row in grouped["set3_context"]).items()):
        summary.append({"metric": "set3_citation_role", "label": label, "count": str(count)})
    summary.append({
        "metric": "quality_control",
        "label": "taxonomy_ready_set1",
        "count": str(sum(row["taxonomy_ready"] == "yes" for row in grouped["set1_core"])),
    })
    summary.append({"metric": "quality_control", "label": "author_priority_review", "count": str(len(priority))})
    write_csv(CORPUS / "summary.csv", summary, ["metric", "label", "count"])

    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    counts = {name: len(rows) for name, rows in grouped.items()}
    manifest["schema_version"] = max(int(manifest.get("schema_version", 1)), 2)
    manifest["counts"] = counts
    manifest["corpus_counts"] = {
        "set1_core": counts["set1_core"],
        "set2_emerging": counts["set2_emerging"],
        "total_corpus": counts["set1_core"] + counts["set2_emerging"],
    }
    manifest["citation_threshold"] = "at least 10"
    manifest["set1_maturity_rule"] = "peer_reviewed == yes OR frozen_citation_count >= 10"
    manifest["scope_rule"] = (
        "LLM multi-agent system + concrete security property + material inter-agent interaction path; "
        "interaction-dependence strength is coded separately"
    )
    manifest["taxonomy_ready_count"] = sum(row["taxonomy_ready"] == "yes" for row in ledger_out)
    manifest["taxonomy_ready_set1_count"] = sum(row["taxonomy_ready"] == "yes" for row in grouped["set1_core"])
    manifest["set1_contributions"] = dict(Counter((row.get("dominant_contribution") or "unclassified") for row in grouped["set1_core"]))
    manifest["set2_contributions"] = dict(Counter((row.get("dominant_contribution") or "unclassified") for row in grouped["set2_emerging"]))
    manifest["set3_roles"] = dict(Counter((row.get("citation_role") or "related_work") for row in grouped["set3_context"]))
    manifest["author_priority_review_count"] = len(priority)
    manifest["files"] = {}
    for path in sorted(CORPUS.glob("*.csv")):
        manifest["files"][path.name] = {"sha256": sha256(path), "rows": len(read_csv(path))}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    (CORPUS / "README.md").write_text(
        f"""# Authoritative corpus views

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | {counts['set1_core']:,} | In-scope mature corpus: peer reviewed or at least 10 frozen citations. |
| `set2_emerging.csv` | {counts['set2_emerging']:,} | In-scope emerging corpus that has not yet met the Set 1 maturity rule. |
| `set3_context.csv` | {counts['set3_context']:,} | Contextual citations; not part of the MAS-security corpus. |
| `screened_out.csv` | {counts['screened_out']:,} | Reviewed search records outside the active evidence sets. |

Set 1 and Set 2 use the same MAS-security scope gate. Membership requires an
LLM multi-agent system, a concrete security property, and a material inter-agent
interaction path. Whether the paper isolates a causal interaction effect is an
evidence-strength question, not a corpus inclusion rule.

Set 1 then applies the maturity union rule: peer reviewed **or** frozen citation
count >= 10. Full-text taxonomy readiness is tracked separately by the
`taxonomy_ready` field and never removes an otherwise eligible paper from Set 1.
Set 2 contains the remaining in-scope early work. Set 3 is contextual only.

All classifications remain model-assisted source review records and require
named-author signoff before being described as human verified.
""",
        encoding="utf-8",
    )

    print(json.dumps({
        "counts": counts,
        "total_corpus": counts["set1_core"] + counts["set2_emerging"],
        "taxonomy_ready_set1": manifest["taxonomy_ready_set1_count"],
        "author_priority_review": len(priority),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
