#!/usr/bin/env python3
"""Build final exports strictly from the canonical structured corpus."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUTOFF = "2026-07-01"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def venue_family(value: str) -> str:
    lower = value.lower()
    mappings = (
        (("findings of acl", "findings of eacl", "findings of emnlp"), "ACL Findings"),
        (("acl system demonstrations",), "ACL System Demonstrations"),
        (("ijcnlp",), "IJCNLP-AACL"),
        (("naacl",), "NAACL"),
        (("emnlp",), "EMNLP"),
        (("acl",), "ACL"),
        (("aaai symposium",), "AAAI Symposium Series"),
        (("aaai",), "AAAI"),
        (("neurips responsible",), "NeurIPS Workshop"),
        (("neurips",), "NeurIPS"),
        (("icml",), "ICML"),
        (("iclr",), "ICLR"),
        (("usenix",), "USENIX Security"),
        (("ieee symposium on security",), "IEEE S&P"),
        (("acm ccs",), "ACM CCS"),
        (("aamas strategic",), "AAMAS Workshop"),
        (("aamas",), "AAMAS"),
        (("web conference",), "The Web Conference"),
        (("colm",), "COLM"),
    )
    for needles, family in mappings:
        if any(needle in lower for needle in needles):
            return family
    return value


def publication_status(paper: dict[str, str]) -> tuple[str, str]:
    note_path = paper["note_path"]
    if "/arxiv/" in note_path:
        return "non_peer_or_unverified", "preprint"
    if any(
        marker in note_path
        for marker in ("/neurips_workshop/", "/aamas_workshop/", "/fedkdd_workshop/")
    ) or paper["paper_id"] == "hagag2026architecture_matters":
        return "workshop_or_nonarchival", "workshop"
    if "/journals_" in note_path:
        return "peer_reviewed", "journal"
    return "peer_reviewed", "conference"


def canonical_rows() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    papers = read_csv(ROOT / "corpus/papers.csv")
    reviews = {
        row["paper_id"]: row
        for row in read_csv(ROOT / "reviews/universal/active_source_review.csv")
    }
    rows = []
    for paper in papers:
        review = reviews[paper["paper_id"]]
        status, venue_type = publication_status(paper)
        rows.append(
            {
                "paper_id": paper["paper_id"],
                "title": paper["title"],
                "authors": paper["authors"],
                "year": paper["year"],
                "venue": paper["venue"],
                "venue_family": venue_family(paper["venue"]),
                "venue_type": venue_type,
                "doi": paper["doi"],
                "primary_url": paper["primary_url"],
                "open_access_url": paper["open_access_url"],
                "publication_status": status,
                "scope_relation": paper["scope_relation"],
                "primary_role": paper["primary_category"],
                "interaction_dependency": paper["multiagent_dependency"],
                "security_relevance": review["scope_rationale"],
                "evidence_level": review["review_status"],
                "evidence_locator": review["evidence_locators"],
                "discovery_source": paper["discovery_source"],
                "cutoff": CUTOFF,
                "cutoff_basis": "first version available before cutoff",
                "note_path": paper["note_path"],
            }
        )
    rows.sort(key=lambda row: (int(row["year"]), row["title"].lower()))
    return rows, {row["paper_id"]: row for row in papers}


def canonical_nonpeer_rows(papers: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    by_title = {paper["title"].casefold(): paper for paper in papers.values()}
    broad_by_record = {
        row["record_id"]: row
        for row in read_csv(ROOT / "corpus/sets/02_broad_included/broad_included.csv")
    }
    candidates = read_csv(
        ROOT / "corpus/sets/03_taxonomy_eligible/taxonomy_candidates.csv"
    )
    rows = []
    for candidate in candidates:
        if candidate["candidate_basis"] != "non_peer_citations_gt_10":
            continue
        paper = by_title.get(candidate["title"].casefold())
        if not paper:
            continue
        broad = broad_by_record.get(candidate["record_id"], {})
        rows.append(
            {
                "paper_id": paper["paper_id"],
                "title": paper["title"],
                "year": paper["year"],
                "venue": paper["venue"],
                "arxiv_id": candidate["arxiv_id"],
                "doi": paper["doi"],
                "primary_url": paper["primary_url"],
                "citations": candidate["citations"],
                "citation_source": "Semantic Scholar Graph API",
                "citation_snapshot_date": candidate["citation_snapshot_date"],
                "scope_relation": paper["scope_relation"],
                "screening_status": "canonical_structured_corpus",
                "threshold_rule": "citationCount > 10; canonical corpus members only",
                "cutoff": CUTOFF,
                "semantic_scholar_id": broad.get("semantic_scholar_id", "Not reported"),
            }
        )
    return sorted(rows, key=lambda row: (-int(row["citations"]), row["title"].lower()))


def nonpeer_candidate_rows(minimum: int, strict: bool) -> list[dict[str, str]]:
    broad = read_csv(ROOT / "corpus/sets/02_broad_included/broad_included.csv")
    taxonomy = {
        row["record_id"]: row
        for row in read_csv(
            ROOT / "corpus/sets/03_taxonomy_eligible/taxonomy_candidates.csv"
        )
    }
    rows = []
    for row in broad:
        if row["publication_status"] == "peer_reviewed":
            continue
        value = row["citations_semantic_scholar"].strip()
        if not value.isdigit():
            continue
        citations = int(value)
        admitted = citations > minimum if strict else citations >= minimum
        if not admitted:
            continue
        decision = taxonomy.get(row["record_id"], {})
        rows.append(
            {
                "record_id": row["record_id"],
                "title": row["title"],
                "publication_date": row["publication_date"],
                "venue": row["canonical_venue"] or row["screened_venue"],
                "arxiv_id": row["arxiv_id"],
                "doi": row["canonical_doi"] or row["doi"],
                "primary_url": (
                    f"https://arxiv.org/abs/{row['arxiv_id']}"
                    if row["arxiv_id"]
                    else row["publication_evidence_url"]
                ),
                "citations": str(citations),
                "citation_source": "Semantic Scholar Graph API",
                "citation_snapshot_date": row["citation_snapshot_date"],
                "recommended_scope": decision.get("recommended_scope", "not_admitted"),
                "gate_decision": decision.get(
                    "gate_decision", "not_admitted_strict_threshold"
                ),
                "source_review_status": decision.get(
                    "source_review_status", "not_source_reviewed"
                ),
                "threshold_rule": (
                    f"citationCount > {minimum}"
                    if strict
                    else f"citationCount >= {minimum}"
                ),
                "cutoff": CUTOFF,
                "semantic_scholar_id": row["semantic_scholar_id"],
            }
        )
    return sorted(rows, key=lambda item: (-int(item["citations"]), item["title"].lower()))


def main() -> None:
    fields = [
        "paper_id", "title", "authors", "year", "venue", "venue_family",
        "venue_type", "doi", "primary_url", "open_access_url",
        "publication_status", "scope_relation", "primary_role",
        "interaction_dependency", "security_relevance", "evidence_level",
        "evidence_locator", "discovery_source", "cutoff", "cutoff_basis",
        "note_path",
    ]
    all_rows, papers = canonical_rows()
    peer = [row for row in all_rows if row["publication_status"] == "peer_reviewed"]
    write_csv(ROOT / "corpus/final/all_relevant_papers.csv", fields, all_rows)
    write_csv(ROOT / "corpus/final/peer_reviewed.csv", fields, peer)

    coverage = []
    for family in sorted({row["venue_family"] for row in peer}):
        selected = [row for row in peer if row["venue_family"] == family]
        coverage.append(
            {
                "venue_family": family,
                "venue_type": ";".join(sorted({row["venue_type"] for row in selected})),
                "paper_count": str(len(selected)),
                "core_security": str(sum(row["scope_relation"] == "core_security" for row in selected)),
                "security_relevant": str(sum(row["scope_relation"] == "security_relevant" for row in selected)),
                "adjacent": str(sum(row["scope_relation"] == "adjacent" for row in selected)),
                "cutoff": CUTOFF,
            }
        )
    write_csv(
        ROOT / "corpus/final/venue_coverage.csv",
        ["venue_family", "venue_type", "paper_count", "core_security", "security_relevant", "adjacent", "cutoff"],
        coverage,
    )

    included_nonpeer_fields = [
        "paper_id", "title", "year", "venue", "arxiv_id", "doi",
        "primary_url", "citations", "citation_source", "citation_snapshot_date",
        "scope_relation", "screening_status", "threshold_rule", "cutoff",
        "semantic_scholar_id",
    ]
    write_csv(
        ROOT / "corpus/final/non_peer_included_citations_gt_10.csv",
        included_nonpeer_fields,
        canonical_nonpeer_rows(papers),
    )

    candidate_fields = [
        "record_id", "title", "publication_date", "venue", "arxiv_id",
        "doi", "primary_url", "citations", "citation_source",
        "citation_snapshot_date", "recommended_scope", "gate_decision",
        "source_review_status", "threshold_rule", "cutoff",
        "semantic_scholar_id",
    ]
    write_csv(
        ROOT / "corpus/final/non_peer_citations_gt_10.csv",
        candidate_fields,
        nonpeer_candidate_rows(10, strict=True),
    )
    write_csv(
        ROOT / "corpus/final/non_peer_candidates_citations_gte_10.csv",
        candidate_fields,
        nonpeer_candidate_rows(10, strict=False),
    )


if __name__ == "__main__":
    main()
