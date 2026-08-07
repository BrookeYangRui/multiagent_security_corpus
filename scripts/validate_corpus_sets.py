#!/usr/bin/env python3
"""Validate relationships among the five corpus sets."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETS = ROOT / "corpus" / "sets"


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_doi(value: str) -> str:
    value = re.sub(
        r"^https?://(?:dx\.)?doi\.org/", "", value.casefold().strip()
    )
    return value if value and not value.startswith("arxiv:") else ""


def duplicate_values(values: list[str]) -> set[str]:
    counts = Counter(value for value in values if value)
    return {value for value, count in counts.items() if count > 1}


def main() -> int:
    errors: list[str] = []
    search = read(SETS / "01_search_catalog" / "search_catalog.csv")
    broad = read(SETS / "02_broad_included" / "broad_included.csv")
    broad_yearly = read(SETS / "02_broad_included" / "yearly_distribution.csv")
    dedup = read(SETS / "02_broad_included" / "deduplication_map.csv")
    taxonomy = read(SETS / "03_taxonomy_eligible" / "taxonomy_candidates.csv")
    contextual = read(SETS / "04_adjacent_contextual" / "adjacent_contextual.csv")
    claims = read(SETS / "05_analysis_specific" / "claim_extraction_queue.csv")
    contracts = read(SETS / "05_analysis_specific" / "analysis_contracts.csv")
    eligibility = read(SETS / "05_analysis_specific" / "analysis_eligibility.csv")
    manifest = read(SETS / "SET_MANIFEST.csv")
    papers = read(ROOT / "corpus" / "papers.csv")
    reviews = read(
        ROOT / "reviews" / "universal" / "active_source_review.csv"
    )

    if len(search) != 2182:
        errors.append(f"search catalog must retain 2182 records, found {len(search)}")
    final_counts = Counter(row["final_decision"] for row in search)
    if final_counts["include-primary-interaction-security"] != 326:
        errors.append("search catalog must retain 326 broad inclusion records")
    if (
        final_counts["unresolved-full-text"]
        + final_counts["unresolved-title-abstract"]
        != 343
    ):
        errors.append("search catalog must retain 343 unresolved records")

    if len(broad) != 325:
        errors.append(f"broad corpus must contain 325 canonical works, found {len(broad)}")
    if len(dedup) != 1:
        errors.append("broad corpus must retain the one-record version merge")
    broad_ids = [row["record_id"] for row in broad]
    for value in sorted(duplicate_values(broad_ids)):
        errors.append(f"duplicate broad record_id: {value}")
    dois = [
        normalized_doi(row["canonical_doi"] or row["doi"])
        for row in broad
    ]
    for value in sorted(duplicate_values(dois)):
        errors.append(f"duplicate canonical DOI in broad corpus: {value}")

    expected_by_year: dict[str, Counter[str]] = {}
    for row in broad:
        year = row["publication_date"][:4]
        counts = expected_by_year.setdefault(year, Counter())
        counts["total"] += 1
        counts[row["publication_status"]] += 1
        if row["publication_status"] == "peer_reviewed":
            counts[f"peer_reviewed_{row['venue_type']}"] += 1
    cumulative_total = 0
    if [row["year"] for row in broad_yearly] != sorted(expected_by_year):
        errors.append("broad yearly export does not cover each publication year once")
    for row in broad_yearly:
        year = row["year"]
        counts = expected_by_year.get(year, Counter())
        cumulative_total += counts["total"]
        expected_values = {
            "total": counts["total"],
            "peer_reviewed": counts["peer_reviewed"],
            "non_peer_or_unverified": counts["non_peer_or_unverified"],
            "peer_reviewed_conference": counts["peer_reviewed_conference"],
            "peer_reviewed_journal": counts["peer_reviewed_journal"],
            "cumulative_total": cumulative_total,
        }
        for field, expected in expected_values.items():
            if row[field] != str(expected):
                errors.append(
                    f"yearly_distribution.csv:{year}: {field} must be {expected}"
                )
        expected_cutoff = "2026-07-01" if year == "2026" else ""
        if row["cutoff"] != expected_cutoff:
            errors.append(f"yearly_distribution.csv:{year}: incorrect cutoff marker")

    candidate_basis = Counter(row["candidate_basis"] for row in taxonomy)
    if candidate_basis != {
        "peer_reviewed_backbone": 94,
        "non_peer_citations_gt_10": 21,
    }:
        errors.append(f"unexpected taxonomy candidate basis: {candidate_basis}")
    if len(taxonomy) != 115:
        errors.append(f"taxonomy candidate set must contain 115 works, found {len(taxonomy)}")
    broad_id_set = set(broad_ids)
    for line, row in enumerate(taxonomy, start=2):
        if row["record_id"] not in broad_id_set:
            errors.append(f"taxonomy_candidates.csv:{line}: work is outside broad corpus")
        if row["candidate_basis"] == "peer_reviewed_backbone":
            if row["publication_status"] != "peer_reviewed":
                errors.append(f"taxonomy_candidates.csv:{line}: invalid peer candidate")
        else:
            if not row["citations"].isdigit() or int(row["citations"]) <= 10:
                errors.append(f"taxonomy_candidates.csv:{line}: non-peer threshold failure")

    reviewed_ids = {row["paper_id"] for row in reviews}
    paper_ids = {row["paper_id"] for row in papers}
    if reviewed_ids != paper_ids or len(reviews) != len(papers):
        errors.append("active source review must match all structured research papers")
    expected_contextual_ids = {
        row["paper_id"]
        for row in reviews
        if row["recommended_scope"] != "core_security"
    }
    if {row["paper_id"] for row in contextual} != expected_contextual_ids:
        errors.append("contextual set must match non-core active source reviews")
    for line, row in enumerate(contextual, start=2):
        if row["paper_id"] not in reviewed_ids:
            errors.append(f"adjacent_contextual.csv:{line}: unknown paper")
        if row["recommended_scope"] not in {"security_relevant", "adjacent"}:
            errors.append(f"adjacent_contextual.csv:{line}: invalid scope")

    expected_claim_ids = {
        row["paper_id"]
        for row in reviews
        if row["attack_instance_coding_required"].startswith("yes")
    }
    claim_ids = {row["paper_id"] for row in claims}
    if claim_ids != expected_claim_ids or len(claims) != 91:
        errors.append("claim extraction queue does not match 91 attack candidates")
    for line, row in enumerate(claims, start=2):
        if row["claim_id"]:
            errors.append(f"claim_extraction_queue.csv:{line}: provisional claim_id must be empty")
        if row["expert_decision"] != "pending":
            errors.append(f"claim_extraction_queue.csv:{line}: unexpected expert decision")

    analysis_ids = [row["analysis_id"] for row in contracts]
    if len(analysis_ids) != 7 or duplicate_values(analysis_ids):
        errors.append("analysis contracts must define seven unique audits")
    expected_pairs = {
        (analysis_id, paper_id)
        for analysis_id in analysis_ids
        for paper_id in reviewed_ids
    }
    observed_pairs = {
        (row["analysis_id"], row["paper_id"])
        for row in eligibility
    }
    if observed_pairs != expected_pairs or len(eligibility) != len(expected_pairs):
        errors.append("analysis eligibility must contain the complete paper x analysis grid")
    if any(
        row["eligibility_decision"] != "pending_expert_adjudication"
        for row in eligibility
    ):
        errors.append("analysis decisions cannot be finalized automatically")

    manifest_counts = {row["set_id"]: int(row["count"]) for row in manifest}
    expected_manifest = {
        "search_catalog": len(search),
        "broad_included": len(broad),
        "structured_corpus": len(papers),
        "taxonomy_candidates": len(taxonomy),
        "adjacent_contextual_reviewed": len(contextual),
        "attack_claim_extraction_queue": len(claims),
        "analysis_eligibility_decisions": len(eligibility),
    }
    for set_id, count in expected_manifest.items():
        if manifest_counts.get(set_id) != count:
            errors.append(f"SET_MANIFEST.csv: stale count for {set_id}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Corpus sets valid: 2182 search records, 325 broad works, 115 taxonomy "
        f"candidates, {len(contextual)} contextual works, {len(claims)} claim "
        f"candidates, and {len(eligibility)} audit decisions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
