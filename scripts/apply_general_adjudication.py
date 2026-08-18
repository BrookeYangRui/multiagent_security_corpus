#!/usr/bin/env python3
"""Apply the 2026-08-18 adjudication of all 109 rows formerly labeled general.

This is an explicit frozen-corpus revision. It rewrites the four manuscript-facing
sets and review_ledger.csv from the adjudication ledgers, then regenerates
summary.csv, manifest.json, README counts, and FROZEN_SNAPSHOT.md.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
ADJ = C / "adjudication"
DATE = "2026-08-18"
EXPECTED = {"set1_core": 108, "set2_emerging": 132, "set3_context": 434, "screened_out": 1543}
FILES = {
    "set1_core": C / "set1_core.csv",
    "set2_emerging": C / "set2_emerging.csv",
    "set3_context": C / "set3_context.csv",
    "screened_out": C / "screened_out.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(rows[0]) if rows else []
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


def csv_rows(path: Path) -> int:
    return len(read_csv(path))


def reason_text(code: str) -> str:
    mapping = {
        "reliability_alignment_or_behavior_not_security": "the primary protected property is reliability, alignment, or behavior rather than a concrete MAS security property",
        "generic_mas_method_not_security_central": "the work is primarily a general MAS method and security is not the central protected property",
        "external_application_or_deployment_context": "the work is primarily an application or deployment study rather than MAS security research",
        "adjacent_safety_governance_not_concrete_security": "the work addresses adjacent safety or governance without a concrete MAS security property",
        "post_cutoff_no_pre_cutoff_version": "no public version before the frozen 2026-07-01 literature cutoff was established",
        "withdrawn_source": "the source is withdrawn and should not support the frozen corpus",
    }
    return mapping.get(code, code.replace("_", " "))


def load_adjudication() -> list[dict[str, str]]:
    set1 = read_csv(ADJ / "general_set1_2026-08-18.csv")
    set2 = read_csv(ADJ / "general_set2_2026-08-18.csv")
    if len(set1) != 36 or len(set2) != 73:
        raise SystemExit(f"unexpected adjudication sizes: Set1={len(set1)}, Set2={len(set2)}")
    rows = set1 + set2
    keys = [row["work_key"] for row in rows]
    if len(keys) != 109 or len(set(keys)) != 109:
        raise SystemExit("adjudication must contain 109 unique work keys")
    return rows


def transform() -> tuple[dict[str, list[dict[str, str]]], dict[str, dict[str, str]]]:
    adjudication = load_adjudication()
    decisions = {row["work_key"]: row for row in adjudication}
    sets = {name: read_csv(path) for name, path in FILES.items()}
    fields = list(sets["set1_core"][0])

    source_rows: dict[str, tuple[str, dict[str, str]]] = {}
    for set_name in ("set1_core", "set2_emerging"):
        for row in sets[set_name]:
            key = row["work_key"]
            if key in decisions:
                if key in source_rows:
                    raise SystemExit(f"duplicate adjudicated key in source sets: {key}")
                source_rows[key] = (set_name, dict(row))
    missing = set(decisions) - set(source_rows)
    if missing:
        raise SystemExit(f"adjudicated keys missing from Set 1/2: {sorted(missing)[:5]}")

    result = {
        "set1_core": [dict(r) for r in sets["set1_core"] if r["work_key"] not in decisions],
        "set2_emerging": [dict(r) for r in sets["set2_emerging"] if r["work_key"] not in decisions],
        "set3_context": [dict(r) for r in sets["set3_context"]],
        "screened_out": [dict(r) for r in sets["screened_out"]],
    }
    transformed: dict[str, dict[str, str]] = {}

    for key, decision in decisions.items():
        source_set, row = source_rows[key]
        if row.get("dominant_contribution") != "general":
            raise SystemExit(f"adjudication target was not general: {key}={row.get('dominant_contribution')}")
        membership = decision["recommended_membership"]
        contribution = decision["recommended_contribution"]
        code = decision["reason_code"]
        row["reviewed_at"] = DATE
        row["previous_category"] = row.get("previous_category") or "general"

        if membership == "keep_current":
            row["dominant_contribution"] = contribution
            if source_set == "set2_emerging":
                row["emerging_direction"] = contribution
            row["decision_reason"] = (
                f"2026-08-18 general-category adjudication retained this work in {source_set} "
                f"and assigned dominant_contribution={contribution}."
            )
            row["membership_reason"] = (
                "Passed the frozen MAS-security scope after explicit 2026-08-18 general-category adjudication. "
                + row.get("membership_reason", "")
            ).strip()
            result[source_set].append(row)

        elif membership == "move_set3":
            role = decision["set3_role_if_moved"]
            if not role:
                raise SystemExit(f"Set 3 move lacks citation role: {key}")
            row["evidence_set"] = "set3_context"
            row["strict_scope_pass"] = "no"
            row["scope_reason"] = f"2026-08-18 adjudication: {reason_text(code)}."
            row["citation_role"] = role
            row["emerging_direction"] = ""
            row["decision_reason"] = (
                f"2026-08-18 general-category adjudication moved this work from {source_set} to Set 3: "
                f"{reason_text(code)}."
            )
            row["membership_reason"] = "Outside the MAS-security corpus; retained for contextual citation use."
            result["set3_context"].append(row)

        elif membership == "screened_out":
            row["evidence_set"] = "screened_out"
            row["strict_scope_pass"] = "no"
            row["scope_reason"] = f"2026-08-18 adjudication: {reason_text(code)}."
            row["citation_role"] = ""
            row["emerging_direction"] = ""
            row["interaction_interfaces"] = ""
            row["risk_or_property"] = ""
            row["interaction_dependence"] = ""
            row["decision_reason"] = f"2026-08-18 adjudication excluded this work: {reason_text(code)}."
            row["membership_reason"] = "Outside the MAS-security corpus and not retained as an active contextual citation."
            result["screened_out"].append(row)
        else:
            raise SystemExit(f"unknown membership decision for {key}: {membership}")
        transformed[key] = row

    # Stable deterministic ordering without imposing a new scientific ordering.
    for name in result:
        if len(result[name]) != EXPECTED[name]:
            raise SystemExit(f"wrong {name} count after adjudication: {len(result[name])} != {EXPECTED[name]}")
        write_csv(FILES[name], result[name], fields)
    return result, transformed


def update_review_ledger(transformed: dict[str, dict[str, str]]) -> None:
    path = C / "review_ledger.csv"
    rows = read_csv(path)
    fields = list(rows[0])
    by_key = {row["work_key"]: row for row in rows}
    sync_fields = {
        "evidence_set", "strict_scope_pass", "scope_reason", "maturity_rule_pass",
        "dominant_contribution", "interaction_interfaces", "risk_or_property",
        "interaction_dependence", "emerging_direction", "citation_role", "paper_section",
        "decision_reason", "reviewer", "reviewed_at", "author_signoff_required",
        "taxonomy_ready", "membership_reason",
    }
    for key, source in transformed.items():
        target = by_key.get(key)
        if target is None:
            raise SystemExit(f"review ledger missing adjudicated key: {key}")
        for field in sync_fields:
            if field in target and field in source:
                target[field] = source[field]
    write_csv(path, rows, fields)


def update_summary(sets: dict[str, list[dict[str, str]]]) -> None:
    rows: list[dict[str, str]] = []
    for key in ("set1_core", "set2_emerging", "set3_context", "screened_out"):
        rows.append({"dimension": "evidence_set", "value": key, "count": str(len(sets[key]))})
    for set_name in ("set1_core", "set2_emerging"):
        counts = Counter(row.get("dominant_contribution", "") for row in sets[set_name])
        dim = f"{set_name}_contribution"
        for contribution in ("attack", "defense", "evaluation", "general", "survey"):
            rows.append({"dimension": dim, "value": contribution, "count": str(counts[contribution])})
    role_counts = Counter(row.get("citation_role", "") for row in sets["set3_context"])
    for role in sorted(k for k in role_counts if k):
        rows.append({"dimension": "set3_citation_role", "value": role, "count": str(role_counts[role])})
    rows.append({"dimension": "quality_control", "value": "taxonomy_ready_set1", "count": str(sum(r.get("taxonomy_ready") == "yes" for r in sets["set1_core"]))})
    apr = C / "author_priority_review.csv"
    rows.append({"dimension": "quality_control", "value": "author_priority_review", "count": str(csv_rows(apr))})
    write_csv(C / "summary.csv", rows, ["dimension", "value", "count"])


def update_manifest(sets: dict[str, list[dict[str, str]]]) -> None:
    path = C / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    counts = {name: len(rows) for name, rows in sets.items()}
    manifest["counts"] = counts
    manifest["corpus_counts"] = {
        "set1_core": counts["set1_core"],
        "set2_emerging": counts["set2_emerging"],
        "total_corpus": counts["set1_core"] + counts["set2_emerging"],
    }
    manifest["set1_contributions"] = dict(sorted(Counter(r.get("dominant_contribution", "") for r in sets["set1_core"]).items()))
    manifest["set2_contributions"] = dict(sorted(Counter(r.get("dominant_contribution", "") for r in sets["set2_emerging"]).items()))
    manifest["set3_roles"] = dict(sorted((k, v) for k, v in Counter(r.get("citation_role", "") for r in sets["set3_context"]).items() if k))
    manifest["taxonomy_ready_set1_count"] = sum(r.get("taxonomy_ready") == "yes" for r in sets["set1_core"])
    manifest["taxonomy_ready_count"] = sum(r.get("taxonomy_ready") == "yes" for name in ("set1_core", "set2_emerging") for r in sets[name])
    manifest["adjudication_revision"] = {
        "date": DATE,
        "scope": "all 109 rows previously labeled general in Set 1 and Set 2",
        "reviewed": 109,
        "retained_in_corpus": 62,
        "moved_to_set3": 44,
        "screened_out": 3,
        "remaining_general": 9,
        "frozen_corpus_total": 240,
    }

    tracked = list(manifest.get("files", {}))
    for rel in (
        "set1_core.csv", "set2_emerging.csv", "set3_context.csv", "screened_out.csv",
        "review_ledger.csv", "summary.csv",
        "adjudication/general_set1_2026-08-18.csv",
        "adjudication/general_set2_2026-08-18.csv",
    ):
        if rel not in tracked:
            tracked.append(rel)
    manifest["files"] = {}
    for rel in tracked:
        file_path = C / rel
        if file_path.exists():
            manifest["files"][rel] = {"rows": csv_rows(file_path), "sha256": sha256(file_path)}
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_docs() -> None:
    snapshot = ROOT / "FROZEN_SNAPSHOT.md"
    text = snapshot.read_text(encoding="utf-8")
    replacements = {
        "Freeze date: `2026-08-17`": "Freeze date: `2026-08-18`",
        "| Set 1 | 121 |": "| Set 1 | 108 |",
        "| Set 2 | 166 |": "| Set 2 | 132 |",
        "| Set 3 | 390 |": "| Set 3 | 434 |",
        "| Screened out | 1,540 |": "| Screened out | 1,543 |",
        "Set 1 plus Set 2 is the 287-work MAS-security corpus.": "Set 1 plus Set 2 is the 240-work MAS-security corpus.",
    }
    for old, new in replacements.items():
        if old not in text:
            raise SystemExit(f"snapshot replacement anchor missing: {old}")
        text = text.replace(old, new)
    note = (
        "\n## 2026-08-18 adjudication revision\n\n"
        "All 109 works previously labeled `general` in Set 1 and Set 2 were individually adjudicated. "
        "The revision retained 62 works in the MAS-security corpus, moved 44 to Set 3, screened out 3, "
        "and reduced the residual `general` category to 9 works. The adjudication ledgers under "
        "`corpus/adjudication/` are part of this frozen snapshot.\n"
    )
    if "## 2026-08-18 adjudication revision" not in text:
        text += note
    snapshot.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    replacements = {
        "frozen as of `2026-08-17`": "frozen as of `2026-08-18`",
        "**Set 1 = 121**, **Set 2 = 166**, **Set 3 = 390**, and **screened out = 1,540**": "**Set 1 = 108**, **Set 2 = 132**, **Set 3 = 434**, and **screened out = 1,543**",
        "**287-work MAS-security corpus**": "**240-work MAS-security corpus**",
        "`corpus/set1_core.csv` | 121": "`corpus/set1_core.csv` | 108",
        "`corpus/set2_emerging.csv` | 166": "`corpus/set2_emerging.csv` | 132",
        "`corpus/set3_context.csv` | 390": "`corpus/set3_context.csv` | 434",
        "`corpus/screened_out.csv` | 1,540": "`corpus/screened_out.csv` | 1,543",
        "together form the 287-work MAS-security corpus": "together form the 240-work MAS-security corpus",
    }
    for old, new in replacements.items():
        if old not in text:
            raise SystemExit(f"README replacement anchor missing: {old}")
        text = text.replace(old, new)
    readme.write_text(text, encoding="utf-8")

    audit = ROOT / "GENERAL_CONTRIBUTION_ADJUDICATION.md"
    if audit.exists():
        text = audit.read_text(encoding="utf-8")
        text = text.replace("## Proposed corpus impact", "## Frozen corpus impact")
        text = text.replace("If every adjudication in the ledger is applied:", "These adjudications are applied in the 2026-08-18 frozen corpus revision:")
        if "Status: applied" not in text:
            text = text.replace("Review date: 2026-08-18", "Review date: 2026-08-18\n\nStatus: applied to the frozen corpus on 2026-08-18")
        audit.write_text(text, encoding="utf-8")


def main() -> int:
    sets, transformed = transform()
    update_review_ledger(transformed)
    update_summary(sets)
    update_manifest(sets)
    update_docs()
    print("Applied frozen general adjudication: Set1=108 Set2=132 Set3=434 screened=1543 corpus=240")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
