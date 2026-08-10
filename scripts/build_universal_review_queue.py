#!/usr/bin/env python3
"""Build the all-paper review checklist and cross-category queue."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = (
    ROOT / "corpus/source_packages/2026-07-01"
    / "multiagent_security_all_relevant_to_2026-07-01.csv"
)

MASTER_FIELDS = [
    "review_track", "track_priority", "paper_id", "title", "year", "venue",
    "primary_category", "paper_type", "scope_relation", "primary_url",
    "note_path", "minimum_review_status", "attack_evidence_status",
    "attack_role", "attack_instance_coding_required", "reviewer",
    "review_date", "adjudication_note",
]

CROSS_CATEGORY_FIELDS = [
    "priority", "paper_id", "title", "year", "venue", "primary_category",
    "paper_type", "scope_relation", "primary_url", "note_path",
    "review_focus", "minimum_review_status", "attack_evidence_status",
    "attack_role", "attack_instance_coding_required", "reviewer",
    "review_date", "adjudication_note",
]

LOAD_BEARING_ROLES = {
    "gu2024agent_smith": "introduces_attack",
    "motwani2024secret_collusion": "introduces_attack; evaluates_defense",
    "men2025troublemaker": "introduces_attack",
    "cohen2025ai_worm": "introduces_attack; evaluates_defense",
    "ju2026flooding": "introduces_attack",
    "wang2025gsafeguard": "evaluates_attack; attack_analysis_only",
    "yu2025netsafe": "evaluates_attack; attack_analysis_only",
    "zhou2026corba": "introduces_attack",
    "mathew2025hidden": "attack_elicitation; evaluates_defense",
    "hu2026lying_truths": "introduces_attack",
    "huang2026whispering_agents": "dual_use_protocol",
    "wang2026masleak": "introduces_attack; benchmark_attack_suite",
    "liu2026topology_memory": "benchmark_attack_suite; evaluates_attack",
    "he2025communication_attacks": "introduces_attack",
    "liu2025collective_manipulation": "introduces_attack; evaluates_defense",
    "zheng2026byzantine_reliability": "fault_evaluation; evaluates_defense",
    "triedman2025malicious_code": "introduces_attack",
    "arif2026conjunctive": "introduces_attack",
    "zhao2026parasites": "introduces_attack; ecosystem_measurement",
    "li2026a2asecbench": "benchmark_attack_suite",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def apply_source_row_overrides(
    rows: list[dict[str, str]], override_path: Path
) -> None:
    """Apply audited active-view refinements without rewriting review history."""
    rows_by_id = {row["paper_id"]: row for row in rows}
    overrides = read_csv(override_path)
    seen: set[tuple[str, str]] = set()
    for override in overrides:
        key = (override["paper_id"], override["field"])
        if key in seen:
            raise ValueError(f"duplicate active source-review row override: {key}")
        seen.add(key)
        paper_id, field = key
        if paper_id not in rows_by_id:
            raise ValueError(
                f"active source-review row override has no active paper: {paper_id}"
            )
        row = rows_by_id[paper_id]
        if field not in row:
            raise ValueError(
                f"active source-review row override has unknown field: {key}"
            )
        if row[field] != override["previous_value"]:
            raise ValueError(
                "active source-review row override no longer matches historical "
                f"source: {key}"
            )
        row[field] = override["active_value"]


def pending_evidence_status(paper: dict[str, str]) -> str:
    roles = {part.strip().casefold() for part in paper["paper_type"].split(";")}
    if paper["primary_category"] == "attack":
        return "candidate_from_primary_category"
    if "attack" in roles or "attack analysis" in roles or "attack suite" in roles:
        return "candidate_from_secondary_role"
    return "not_screened"


def main() -> None:
    papers = read_csv(ROOT / "corpus" / "papers.csv")
    papers_by_id = {row["paper_id"]: row for row in papers}
    queue_dir = ROOT / "reviews" / "queues"
    load_bearing = [
        row for row in read_csv(queue_dir / "load_bearing.csv")
        if row["paper_id"] in papers_by_id
    ]
    existing_attack = {
        row["paper_id"]: row
        for row in read_csv(queue_dir / "standard_attack.csv")
    }
    load_by_id = {row["paper_id"]: row for row in load_bearing}
    standard_attack = []
    attack_papers = [
        paper for paper in papers
        if paper["primary_category"] == "attack"
        and paper["paper_id"] not in load_by_id
    ]
    attack_papers.sort(key=lambda row: (int(row["year"]), row["title"].casefold()))
    for priority, paper in enumerate(attack_papers, start=len(load_bearing) + 1):
        old = existing_attack.get(paper["paper_id"], {})
        standard_attack.append({
            "priority": str(priority),
            "paper_id": paper["paper_id"],
            "review_focus": old.get(
                "review_focus", "metadata; scope; category; evidence locators"
            ),
            "review_level": old.get("review_level", "standard_attack_review"),
            "human_review_status": old.get(
                "human_review_status", "pending_human_review"
            ),
            "reviewer": old.get("reviewer", ""),
            "adjudication_note": old.get("adjudication_note", ""),
        })
    write_csv(
        queue_dir / "standard_attack.csv",
        standard_attack,
        [
            "priority", "paper_id", "review_focus", "review_level",
            "human_review_status", "reviewer", "adjudication_note",
        ],
    )
    attack_by_id = {row["paper_id"]: row for row in standard_attack}

    remaining_nonattack = [
        paper for paper in papers
        if paper["paper_id"] not in load_by_id
        and paper["paper_id"] not in attack_by_id
    ]
    remaining_nonattack.sort(
        key=lambda row: (
            row["primary_category"], int(row["year"]), row["title"].casefold()
        )
    )

    cross_rows: list[dict[str, str]] = []
    for priority, paper in enumerate(
        remaining_nonattack, start=len(load_bearing) + len(standard_attack) + 1
    ):
        cross_rows.append({
            "priority": str(priority),
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "year": paper["year"],
            "venue": paper["venue"],
            "primary_category": paper["primary_category"],
            "paper_type": paper["paper_type"],
            "scope_relation": paper["scope_relation"],
            "primary_url": paper["primary_url"],
            "note_path": paper["note_path"],
            "review_focus": (
                "metadata; scope; primary and secondary roles; attack-bearing "
                "claims; evidence locators"
            ),
            "minimum_review_status": "pending_minimum_review",
            "attack_evidence_status": pending_evidence_status(paper),
            "attack_role": "",
            "attack_instance_coding_required": "pending",
            "reviewer": "",
            "review_date": "",
            "adjudication_note": "",
        })
    write_csv(
        queue_dir / "cross_category.csv",
        cross_rows,
        CROSS_CATEGORY_FIELDS,
    )

    cross_by_id = {row["paper_id"]: row for row in cross_rows}
    master_rows: list[dict[str, str]] = []
    for paper in papers:
        paper_id = paper["paper_id"]
        if paper_id in load_by_id:
            queue = load_by_id[paper_id]
            track = "load_bearing"
            priority = queue["priority"]
            status = queue["human_review_status"]
            role = LOAD_BEARING_ROLES.get(paper_id, "attack_bearing_review")
            evidence_status = (
                "dual_use_no_malicious_claim_confirmed"
                if role == "dual_use_protocol"
                else "confirmed_attack_bearing"
            )
            coding_required = "conditional" if role == "dual_use_protocol" else "yes"
            adjudication = queue["adjudication_note"]
        elif paper_id in attack_by_id:
            queue = attack_by_id[paper_id]
            track = "standard_attack"
            priority = queue["priority"]
            status = queue["human_review_status"]
            role = ""
            evidence_status = "candidate_from_primary_category"
            coding_required = "pending"
            adjudication = queue["adjudication_note"]
        else:
            queue = cross_by_id[paper_id]
            track = "cross_category"
            priority = queue["priority"]
            status = queue["minimum_review_status"]
            role = queue["attack_role"]
            evidence_status = queue["attack_evidence_status"]
            coding_required = queue["attack_instance_coding_required"]
            adjudication = queue["adjudication_note"]

        master_rows.append({
            "review_track": track,
            "track_priority": priority,
            "paper_id": paper_id,
            "title": paper["title"],
            "year": paper["year"],
            "venue": paper["venue"],
            "primary_category": paper["primary_category"],
            "paper_type": paper["paper_type"],
            "scope_relation": paper["scope_relation"],
            "primary_url": paper["primary_url"],
            "note_path": paper["note_path"],
            "minimum_review_status": status,
            "attack_evidence_status": evidence_status,
            "attack_role": role,
            "attack_instance_coding_required": coding_required,
            "reviewer": queue.get("reviewer", ""),
            "review_date": queue.get("review_date", ""),
            "adjudication_note": adjudication,
        })

    master_rows.sort(key=lambda row: int(row["track_priority"]))
    write_csv(
        queue_dir / "universal.csv",
        master_rows,
        MASTER_FIELDS,
    )

    # Preserve the imported 114-work packet as history while exposing an active
    # source-review view that follows the authoritative 142-work denominator.
    review_dir = ROOT / "reviews" / "universal"
    active_ids = set(papers_by_id)
    source_rows = read_csv(review_dir / "universal_114_source_review.csv")
    source_by_id = {row["paper_id"]: row for row in source_rows}
    authoritative_by_id = {
        row["paper_id"]: row for row in read_csv(AUTHORITATIVE)
    }
    master_by_id = {row["paper_id"]: row for row in master_rows}
    active_source_rows = []
    for paper in papers:
        paper_id = paper["paper_id"]
        authoritative = authoritative_by_id[paper_id]
        old = source_by_id.get(paper_id)
        if old:
            master = master_by_id[paper_id]
            row = dict(old)
            row.update({
                "global_priority": master["track_priority"],
                "review_track": master["review_track"],
                "paper_id": paper_id,
                "canonical_title": paper["title"],
                "canonical_authors": paper["authors"],
                "canonical_year": paper["year"],
                "canonical_venue": paper["venue"],
                "doi": paper["doi"],
                "source_url": paper["primary_url"],
                "current_scope": paper["scope_relation"],
                "current_category": paper["primary_category"],
                "secondary_roles": paper["paper_type"],
            })
        else:
            master = master_by_id[paper_id]
            row = {field: "" for field in source_rows[0]}
            row.update({
                "global_priority": master["track_priority"],
                "review_track": master["review_track"],
                "paper_id": paper_id,
                "canonical_title": paper["title"],
                "canonical_authors": paper["authors"],
                "canonical_year": paper["year"],
                "canonical_venue": paper["venue"],
                "doi": paper["doi"] or "Not reported",
                "source_url": paper["primary_url"],
                "version_status": authoritative["cutoff_basis"],
                "identity_verdict": "imported_authoritative_142",
                "current_scope": paper["scope_relation"],
                "recommended_scope": paper["scope_relation"],
                "scope_rationale": authoritative["security_relevance"],
                "current_category": paper["primary_category"],
                "recommended_category": paper["primary_category"],
                "secondary_roles": paper["paper_type"],
                "multiagent_verdict": authoritative["interaction_dependency"],
                "attack_evidence_status": pending_evidence_status(paper),
                "attack_instance_coding_required": "pending",
                "evidence_locators": authoritative["evidence_locator"],
                "author_claim_vs_corpus_interpretation": "Imported corpus interpretation pending named human signoff.",
                "limitations_maturity": "Claim-level extraction pending.",
                "review_outcome": "imported_authoritative_142_pending_claim_review",
                "promote_to_load_bearing": "pending",
                "review_status": authoritative["evidence_level"],
            })
        active_source_rows.append(row)
    apply_source_row_overrides(
        active_source_rows,
        review_dir / "active_source_review_row_overrides.csv",
    )
    write_csv(
        review_dir / "active_source_review.csv",
        active_source_rows,
        list(source_rows[0]),
    )
    correction_rows = read_csv(
        review_dir / "universal_source_review_corrections.csv"
    )
    override_rows = read_csv(
        review_dir / "active_source_review_correction_overrides.csv"
    )
    overrides = {
        (
            row["paper_id"],
            row["field_or_category"],
            row["previous_correction"],
        ): row
        for row in override_rows
    }
    if len(overrides) != len(override_rows):
        raise ValueError("duplicate active source-review correction override")
    matched_overrides = set()
    active_corrections = [
        dict(row) for row in correction_rows if row["paper_id"] in active_ids
    ]
    for row in active_corrections:
        key = (
            row["paper_id"],
            row["field_or_category"],
            row["recommended_correction"],
        )
        override = overrides.get(key)
        if not override:
            continue
        row["recommended_correction"] = override["active_correction"]
        row["rationale"] = override["change_reason"]
        row["evidence_source"] = override["evidence_source"]
        matched_overrides.add(key)
    missing_overrides = set(overrides) - matched_overrides
    if missing_overrides:
        raise ValueError(
            "active correction overrides did not match active records: "
            f"{sorted(missing_overrides)}"
        )
    write_csv(
        review_dir / "active_source_review_corrections.csv",
        active_corrections,
        list(correction_rows[0]),
    )


if __name__ == "__main__":
    main()
