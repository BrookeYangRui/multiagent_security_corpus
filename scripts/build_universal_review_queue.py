#!/usr/bin/env python3
"""Build the all-paper review checklist and cross-category queue."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

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
    load_bearing = read_csv(queue_dir / "load_bearing.csv")
    standard_attack = read_csv(queue_dir / "standard_attack.csv")
    load_by_id = {row["paper_id"]: row for row in load_bearing}
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
    for priority, paper in enumerate(remaining_nonattack, start=63):
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
            role = LOAD_BEARING_ROLES[paper_id]
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


if __name__ == "__main__":
    main()
