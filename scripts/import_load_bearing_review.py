#!/usr/bin/env python3
"""Apply the structured load-bearing source review to canonical records."""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "reviews" / "load_bearing"

CATEGORY_OVERRIDES = {
    "wang2025gsafeguard": "defense",
    "yu2025netsafe": "evaluation",
    "mathew2025hidden": "evaluation",
    "huang2026whispering_agents": "evaluation",
    "liu2026topology_memory": "evaluation",
    "zheng2026byzantine_reliability": "defense",
}

NOTE_PATH_OVERRIDES = {
    "wang2025gsafeguard": "papers/defenses/acl/2025_wang_g_safeguard.md",
    "yu2025netsafe": "papers/evaluations/findings_acl/2025_yu_netsafe.md",
    "mathew2025hidden": "papers/evaluations/ijcnlp_aacl/2025_mathew_hidden_plain_text.md",
    "huang2026whispering_agents": "papers/evaluations/aaai/2026_huang_whispering_agents.md",
    "liu2026topology_memory": "papers/evaluations/findings_acl/2026_liu_topology_memory_leakage.md",
    "zheng2026byzantine_reliability": "papers/defenses/aaai/2026_zheng_byzantine_reliability.md",
}

METADATA_OVERRIDES = {
    "wang2026masleak": {
        "open_access_url": "https://arxiv.org/pdf/2505.12442",
    },
    "zheng2026byzantine_reliability": {
        "title": "Rethinking the Reliability of Multi-agent System: A Perspective from Byzantine Fault Tolerance",
    },
    "huang2026whispering_agents": {
        "authors": "Kaibo Huang; Yukun Wei; Wansheng Wu; Tianhua Zhang; Zhongliang Yang; Linna Zhou",
    },
    "zhao2026parasites": {
        "doi": "10.1109/SP63933.2026.00154",
        "primary_url": "https://doi.org/10.1109/SP63933.2026.00154",
        "open_access_url": "https://arxiv.org/pdf/2509.06572",
        "accessed_version": (
            "published IEEE S&P 2026 metadata; arXiv v5 full text"
        ),
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def paper_type(value: str) -> str:
    return "; ".join(part.strip().capitalize() for part in value.split(";"))


def review_status(outcome: str) -> str:
    if outcome == "Pending final source verification":
        return "blocked_pending_final_source"
    if outcome == "Pending exact full-text verification":
        return "blocked_pending_exact_full_text"
    return "source_reviewed_pending_author_signoff"


def source_review_block(
    review: dict[str, str], corrections: list[dict[str, str]]
) -> str:
    correction_lines = "\n".join(
        f"- **{item['severity'].upper()} - {item['field']}:** "
        f"{item['required_correction']}"
        for item in corrections
    )
    return f"""<!-- SOURCE_REVIEW_START -->
## Source Review

**Status:** `{review_status(review['outcome'])}`

**Outcome:** {review['outcome']}

**Review source:** `reviews/load_bearing/load_bearing_source_review.csv`

This section supersedes inconsistent automated coding elsewhere in this note.
It is a source-level review, not human verification. Manuscript-facing claims
still require author or designated-reviewer signoff.

### Identity and Scope

- Identity: {review['identity']}
- Recommended scope: `{review['recommended_scope']}`
- Multi-agent dependency: {review['scope_reason']}
- Recommended roles: {review['recommended_category']}
- Maturity: {review['maturity']}

### Threat and Failure Coding

- Attacker or fault actor: {review['attacker']}
- Capabilities: {review['capabilities']}
- Preconditions: {review['preconditions']}
- Surfaces: {review['surfaces']}
- Mechanism: {review['mechanism']}
- Primary system-level failure: {review['primary_failure']}
- Impact: {review['impact']}

### Evaluation Contract

- Configuration: {review['configuration']}
- Topology: {review['topology']}
- Baseline or ablation: {review['baseline']}
- Metric: {review['metric']}
- Unit: {review['unit']}
- Denominator: {review['denominator']}
- Result boundary: {review['result']}

### Evidence and Boundaries

- Evidence locations: {review['evidence']}
- Author claim versus corpus interpretation: {review['claim_boundary']}
- Limitations: {review['limitations']}

### Required Corrections

{correction_lines}
<!-- SOURCE_REVIEW_END -->"""


def update_note(path: Path, block: str, paper: dict[str, str]) -> None:
    text = path.read_text(encoding="utf-8")
    paper_type_block = (
        "## Paper Type\n\n"
        f"{paper['paper_type']}\n\n"
        f"- Primary category: `{paper['primary_category']}`\n"
        f"- Scope relation: `{paper['scope_relation']}`\n"
    )
    text = re.sub(
        r"## Paper Type\n\n.*?(?=\n## )",
        paper_type_block.rstrip() + "\n",
        text,
        count=1,
        flags=re.DOTALL,
    )
    start = "<!-- SOURCE_REVIEW_START -->"
    end = "<!-- SOURCE_REVIEW_END -->"
    if start in text and end in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        text = before.rstrip() + "\n\n" + block + after
    else:
        lines = text.splitlines()
        notice = (
            "> **Source-review correction:** The Source Review section at the "
            "end supersedes inconsistent automated coding in this note. It "
            "still requires author signoff."
        )
        lines.insert(1, "")
        lines.insert(2, notice)
        text = "\n".join(lines).rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    reviews = read_csv(REVIEW_DIR / "load_bearing_source_review.csv")
    review_by_id = {row["paper_id"]: row for row in reviews}
    corrections_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(REVIEW_DIR / "load_bearing_corrections.csv"):
        corrections_by_id[row["paper_id"]].append(row)

    papers_path = ROOT / "corpus" / "papers.csv"
    papers = read_csv(papers_path)
    paper_fields = list(papers[0])
    papers_by_id = {row["paper_id"]: row for row in papers}

    for paper_id, review in review_by_id.items():
        paper = papers_by_id[paper_id]
        paper["paper_type"] = paper_type(review["recommended_category"])
        paper["primary_category"] = CATEGORY_OVERRIDES.get(
            paper_id, paper["primary_category"]
        )
        paper["scope_relation"] = (
            "security_relevant"
            if review["recommended_scope"].startswith("security_relevant")
            else "core_security"
        )
        paper["multiagent_dependency"] = review["scope_reason"]
        paper["attack"] = review["mechanism"]
        paper["system_failure"] = review["primary_failure"]
        paper["evaluation"] = review["metric"]
        if paper_id in NOTE_PATH_OVERRIDES:
            paper["note_path"] = NOTE_PATH_OVERRIDES[paper_id]
        paper.update(METADATA_OVERRIDES.get(paper_id, {}))

    write_csv(papers_path, papers, paper_fields)

    queue_path = ROOT / "corpus" / "load_bearing_review_queue.csv"
    queue = read_csv(queue_path)
    queue_fields = list(queue[0])
    for row in queue:
        review = review_by_id[row["paper_id"]]
        paper = papers_by_id[row["paper_id"]]
        row["primary_url"] = paper["primary_url"]
        row["note_path"] = paper["note_path"]
        row["scope_precheck"] = paper["scope_relation"]
        if row["paper_id"] == "zhao2026parasites":
            row["metadata_precheck"] = "official_source_recorded"
        row["human_review_status"] = review_status(review["outcome"])
        row["adjudication_note"] = (
            f"Source review recorded {len(corrections_by_id[row['paper_id']])} "
            f"corrections; {review['outcome'].lower()}; author signoff required."
        )
    write_csv(queue_path, queue, queue_fields)

    artifacts_path = ROOT / "corpus" / "evaluation_artifacts.csv"
    artifacts = read_csv(artifacts_path)
    artifact_fields = list(artifacts[0])
    for row in artifacts:
        paper_id = row["canonical_paper_id"]
        if paper_id in papers_by_id:
            paper = papers_by_id[paper_id]
            row["note_path"] = paper["note_path"]
            row["primary_category"] = {
                "attack": "attacks",
                "defense": "defenses",
                "evaluation": "evaluations",
                "general": "general",
            }.get(paper["primary_category"], row["primary_category"])
    write_csv(artifacts_path, artifacts, artifact_fields)

    for paper_id, review in review_by_id.items():
        note_path = ROOT / papers_by_id[paper_id]["note_path"]
        update_note(
            note_path,
            source_review_block(review, corrections_by_id[paper_id]),
            papers_by_id[paper_id],
        )


if __name__ == "__main__":
    main()
