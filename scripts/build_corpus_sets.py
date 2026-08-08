#!/usr/bin/env python3
"""Build auditable corpus sets from the canonical screening and review data."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETS = ROOT / "corpus" / "sets"
SEARCH = SETS / "01_search_catalog" / "search_catalog.csv"
BROAD = SETS / "02_broad_included" / "broad_included.csv"
BROAD_YEARLY = SETS / "02_broad_included" / "yearly_distribution.csv"
PAPERS = ROOT / "corpus" / "papers.csv"
REVIEWS = ROOT / "reviews" / "universal" / "active_source_review.csv"
CITATION_GATE_REVIEWS = (
    ROOT / "reviews" / "citation_gate" / "non_peer_gt10_full_text_adjudication.csv"
)
TAXONOMY = SETS / "03_taxonomy_eligible" / "taxonomy_candidates.csv"
CONTEXTUAL = SETS / "04_adjacent_contextual" / "adjacent_contextual.csv"
CLAIMS = SETS / "05_analysis_specific" / "claim_extraction_queue.csv"
CONTRACTS = SETS / "05_analysis_specific" / "analysis_contracts.csv"
ELIGIBILITY = SETS / "05_analysis_specific" / "analysis_eligibility.csv"
MANIFEST = SETS / "SET_MANIFEST.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def citation_count(row: dict[str, str]) -> int | None:
    value = row["citations_semantic_scholar"].strip()
    return int(value) if value.isdigit() else None


def normalized_scope(value: str) -> str:
    if value.startswith("core_security"):
        return "core_security"
    if value.startswith("security_relevant"):
        return "security_relevant"
    if value.startswith("adjacent"):
        return "adjacent"
    return "unresolved"


def candidate_signal(review: dict[str, str], analysis_id: str) -> str:
    combined = " ".join(review.values()).casefold()
    attack_required = review["attack_instance_coding_required"].strip()
    category_roles = " ".join(
        [
            review["current_category"],
            review["recommended_category"],
            review["secondary_roles"],
            review["attack_role"],
        ]
    ).casefold()

    if analysis_id == "attack_landscape":
        return "candidate" if attack_required.startswith("yes") else "no_signal"
    if analysis_id == "defense_landscape":
        return "candidate" if "defense" in category_roles else "no_signal"
    if analysis_id == "benchmark_audit":
        return (
            "candidate"
            if "benchmark" in category_roles or "evaluation" in category_roles
            else "no_signal"
        )
    if analysis_id == "metric_comparability":
        fields = review["metric_definition"] + review["unit_denominator"]
        return "candidate" if fields.strip() else "no_signal"
    if analysis_id == "observer_scope_audit":
        terms = ("observer", "monitor", "visibility", "trace", "white-box")
        return "candidate" if any(term in combined for term in terms) else "no_signal"
    if analysis_id == "assumption_audit":
        terms = ("formal", "guarantee", "byzantine", "bound", "theoretical")
        return "candidate" if any(term in combined for term in terms) else "no_signal"
    if analysis_id == "coverage_audit":
        required = [
            review["multiagent_verdict"],
            review["adversary_position"],
            review["mechanism"],
            review["primary_system_failure"],
            review["evidence_locators"],
        ]
        return "candidate" if all(value.strip() for value in required) else "no_signal"
    raise ValueError(f"unknown analysis: {analysis_id}")


ANALYSIS_CONTRACTS = [
    {
        "analysis_id": "attack_landscape",
        "unit": "claim",
        "eligibility_rule": "Primary paper reports an explicit attack or adversarial claim with interaction-dependent mechanism and security endpoint.",
        "exclusion_rule": "Survey mentions, inherited attacks, non-adversarial faults, and claims without full-text evidence.",
        "required_fields": "claim_id; mechanism; interaction surface; system failure; evidence locator",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "defense_landscape",
        "unit": "defense instance",
        "eligibility_rule": "Primary paper proposes or systematically evaluates a defense acting on a multi-agent security property.",
        "exclusion_rule": "Generic guardrails without multi-agent evaluation and post-hoc discussion without a defense instance.",
        "required_fields": "defense locus; defense function; observer scope; trusted components; evidence locator",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "benchmark_audit",
        "unit": "benchmark or evaluation artifact",
        "eligibility_rule": "Paper defines a reusable benchmark, dataset, harness, protocol, or attack suite with a security endpoint.",
        "exclusion_rule": "One-off evaluation without a reusable or fully specified evaluation object.",
        "required_fields": "artifact; task; metric; unit; denominator; availability; evidence locator",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "metric_comparability",
        "unit": "empirical metric claim",
        "eligibility_rule": "Full text reports the metric definition, unit, denominator, system configuration, and result.",
        "exclusion_rule": "Abstract-only numbers, missing denominator, or results that combine incompatible endpoints without disaggregation.",
        "required_fields": "metric definition; unit; denominator; population scope; budget; aggregation; verification",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "observer_scope_audit",
        "unit": "defense instance",
        "eligibility_rule": "Paper states what messages, state, topology, provenance, execution trace, or internals the defense observes.",
        "exclusion_rule": "Observer access cannot be located in the full text or is inferred only from the implementation name.",
        "required_fields": "protected property; required variables; observed variables; trusted components; guarantee; evidence locator",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "assumption_audit",
        "unit": "formal or explicit robustness claim",
        "eligibility_rule": "Paper gives a formal guarantee, numerical fault threshold, or explicit robustness claim with identifiable assumptions.",
        "exclusion_rule": "Qualitative robustness language without a bound, contract, or operational definition.",
        "required_fields": "claim; adversary; synchrony; authentication; validity; termination; trusted components; evidence locator",
        "peer_reviewed_sensitivity": "yes",
    },
    {
        "analysis_id": "coverage_audit",
        "unit": "paper or claim record",
        "eligibility_rule": "Architecture, threat, failure, and defense fields can all be coded from canonical full text.",
        "exclusion_rule": "Any required field is unavailable, unresolved, or supported only by a secondary source.",
        "required_fields": "architecture; threat actor; capability; precondition; mechanism; failure; impact; defense contract",
        "peer_reviewed_sensitivity": "yes",
    },
]


def main() -> None:
    search = read_csv(SEARCH)
    broad = read_csv(BROAD)
    papers = read_csv(PAPERS)
    reviews = read_csv(REVIEWS)
    citation_gate_reviews = read_csv(CITATION_GATE_REVIEWS)

    papers_by_title = {normalized_title(row["title"]): row for row in papers}
    reviews_by_title = {
        normalized_title(row["canonical_title"]): row for row in reviews
    }
    citation_reviews_by_record = {
        row["record_id"]: row for row in citation_gate_reviews
    }

    broad_year_counts: dict[str, Counter[str]] = {}
    for row in broad:
        year = row["publication_date"][:4]
        counts = broad_year_counts.setdefault(year, Counter())
        counts["total"] += 1
        counts[row["publication_status"]] += 1
        if row["publication_status"] == "peer_reviewed":
            counts[f"peer_reviewed_{row['venue_type']}"] += 1

    broad_yearly_rows: list[dict[str, str]] = []
    cumulative_total = 0
    for year in sorted(broad_year_counts):
        counts = broad_year_counts[year]
        cumulative_total += counts["total"]
        broad_yearly_rows.append(
            {
                "year": year,
                "total": str(counts["total"]),
                "peer_reviewed": str(counts["peer_reviewed"]),
                "non_peer_or_unverified": str(counts["non_peer_or_unverified"]),
                "peer_reviewed_conference": str(counts["peer_reviewed_conference"]),
                "peer_reviewed_journal": str(counts["peer_reviewed_journal"]),
                "cumulative_total": str(cumulative_total),
                "cutoff": "2026-07-01" if year == "2026" else "",
            }
        )
    write_csv(BROAD_YEARLY, list(broad_yearly_rows[0]), broad_yearly_rows)

    taxonomy_rows: list[dict[str, str]] = []
    for row in broad:
        citations = citation_count(row)
        if row["publication_status"] == "peer_reviewed":
            basis = "peer_reviewed_backbone"
        elif citations is not None and citations > 10:
            basis = "non_peer_citations_gt_10"
        else:
            continue

        key = normalized_title(row["title"])
        paper = papers_by_title.get(key)
        review = reviews_by_title.get(key)
        citation_review = citation_reviews_by_record.get(row["record_id"])
        if review:
            recommended_scope = normalized_scope(review["recommended_scope"])
            review_status = review["review_status"]
        elif citation_review:
            recommended_scope = normalized_scope(citation_review["recommended_scope"])
            review_status = "full_text_reviewed_pending_author_signoff"
        else:
            recommended_scope = "pending"
            review_status = "not_source_reviewed"

        if citation_review:
            gate_decision = citation_review["gate_decision"]
            reason = citation_review["decision_reason"]
        elif not review:
            gate_decision = "pending_full_text_adjudication"
            reason = "Candidate rule passed; uniform full-text security gate not yet applied."
        elif review["review_outcome"].startswith(("pending_", "blocked_")):
            gate_decision = "blocked_source_verification"
            reason = review["review_outcome"]
        elif recommended_scope == "core_security":
            gate_decision = "provisional_pass_author_signoff_required"
            reason = "Source review recommends core security; named human signoff remains required."
        elif recommended_scope == "security_relevant":
            gate_decision = "contextual_not_strict_core"
            reason = "Source review recommends paper-level security-relevant scope."
        elif recommended_scope == "adjacent":
            gate_decision = "adjacent_not_core"
            reason = "Source review recommends adjacent scope."
        else:
            gate_decision = "pending_scope_adjudication"
            reason = "Source review does not yield a normalized paper-level scope."

        taxonomy_rows.append(
            {
                "record_id": row["record_id"],
                "canonical_paper_id": paper["paper_id"] if paper else "",
                "title": row["title"],
                "publication_date": row["publication_date"],
                "venue": row["canonical_venue"] or row["screened_venue"],
                "doi": row["canonical_doi"] or row["doi"],
                "arxiv_id": row["arxiv_id"],
                "publication_status": row["publication_status"],
                "venue_type": row["venue_type"],
                "citations": "" if citations is None else str(citations),
                "citation_snapshot_date": row["citation_snapshot_date"],
                "candidate_basis": basis,
                "source_review_status": review_status,
                "recommended_scope": recommended_scope,
                "gate_decision": gate_decision,
                "decision_reason": reason,
            }
        )

    taxonomy_fields = list(taxonomy_rows[0])
    write_csv(TAXONOMY, taxonomy_fields, taxonomy_rows)

    contextual_rows: list[dict[str, str]] = []
    for review in reviews:
        scope = normalized_scope(review["recommended_scope"])
        if scope == "core_security":
            continue
        paper = papers_by_title.get(normalized_title(review["canonical_title"]))
        contextual_rows.append(
            {
                "paper_id": review["paper_id"],
                "title": review["canonical_title"],
                "year": review["canonical_year"],
                "venue": review["canonical_venue"],
                "recommended_scope": scope,
                "contextual_role": review["recommended_category"],
                "scope_rationale": review["scope_rationale"],
                "attack_instance_coding_required": review["attack_instance_coding_required"],
                "note_path": paper["note_path"] if paper else "",
                "source_review_status": review["review_status"],
            }
        )
    contextual_fields = list(contextual_rows[0])
    write_csv(CONTEXTUAL, contextual_fields, contextual_rows)

    claim_rows: list[dict[str, str]] = []
    for review in reviews:
        if not review["attack_instance_coding_required"].startswith("yes"):
            continue
        claim_rows.append(
            {
                "paper_id": review["paper_id"],
                "claim_id": "",
                "claim_type": "attack_candidate",
                "claim_split_status": "pending_claim_level_extraction",
                "adversary_position": review["adversary_position"],
                "adversary_capabilities": review["adversary_capabilities"],
                "preconditions": review["preconditions"],
                "mechanism": review["mechanism"],
                "interaction_surface": review["attack_surfaces"],
                "primary_system_failure": review["primary_system_failure"],
                "reported_impact": review["reported_impact"],
                "metric_definition": review["metric_definition"],
                "unit_denominator": review["unit_denominator"],
                "evidence_locators": review["evidence_locators"],
                "source_review_status": review["review_status"],
                "expert_decision": "pending",
            }
        )
    claim_fields = list(claim_rows[0])
    write_csv(CLAIMS, claim_fields, claim_rows)

    contract_fields = list(ANALYSIS_CONTRACTS[0])
    write_csv(CONTRACTS, contract_fields, ANALYSIS_CONTRACTS)

    eligibility_rows: list[dict[str, str]] = []
    for review in reviews:
        for contract in ANALYSIS_CONTRACTS:
            eligibility_rows.append(
                {
                    "analysis_id": contract["analysis_id"],
                    "paper_id": review["paper_id"],
                    "candidate_signal": candidate_signal(review, contract["analysis_id"]),
                    "eligibility_decision": "pending_expert_adjudication",
                    "exclusion_reason": "",
                    "peer_review_status": review["canonical_venue"],
                    "evidence_locator": review["evidence_locators"],
                    "adjudicator": "",
                    "adjudication_date": "",
                    "adjudication_note": "",
                }
            )
    eligibility_fields = list(eligibility_rows[0])
    write_csv(ELIGIBILITY, eligibility_fields, eligibility_rows)

    gate_counts = Counter(row["gate_decision"] for row in taxonomy_rows)
    manifest_rows = [
        {"set_id": "search_catalog", "count": str(len(search)), "status": "frozen", "unit": "transitively deduplicated search entity", "source": str(SEARCH.relative_to(ROOT))},
        {"set_id": "broad_included", "count": str(len(broad)), "status": "frozen", "unit": "work", "source": str(BROAD.relative_to(ROOT))},
        {"set_id": "structured_corpus", "count": str(len(papers)), "status": "source_reviewed_pending_author_signoff", "unit": "work", "source": str(PAPERS.relative_to(ROOT))},
        {"set_id": "taxonomy_candidates", "count": str(len(taxonomy_rows)), "status": "adjudication_in_progress", "unit": "work", "source": str(TAXONOMY.relative_to(ROOT))},
        {"set_id": "taxonomy_provisional_pass", "count": str(gate_counts["provisional_pass_author_signoff_required"]), "status": "not_final", "unit": "work", "source": str(TAXONOMY.relative_to(ROOT))},
        {"set_id": "taxonomy_pending_full_text", "count": str(gate_counts["pending_full_text_adjudication"]), "status": "pending", "unit": "work", "source": str(TAXONOMY.relative_to(ROOT))},
        {"set_id": "adjacent_contextual_reviewed", "count": str(len(contextual_rows)), "status": "provisional", "unit": "work", "source": str(CONTEXTUAL.relative_to(ROOT))},
        {"set_id": "attack_claim_extraction_queue", "count": str(len(claim_rows)), "status": "pending_claim_split", "unit": "paper-level candidate", "source": str(CLAIMS.relative_to(ROOT))},
        {"set_id": "analysis_eligibility_decisions", "count": str(len(eligibility_rows)), "status": "pending_expert_adjudication", "unit": "paper-analysis pair", "source": str(ELIGIBILITY.relative_to(ROOT))},
    ]
    manifest_fields = list(manifest_rows[0])
    write_csv(MANIFEST, manifest_fields, manifest_rows)

    print(
        f"Built {len(taxonomy_rows)} taxonomy candidates, "
        f"{len(contextual_rows)} contextual works, {len(claim_rows)} attack "
        f"claim candidates, and {len(eligibility_rows)} analysis decisions."
    )


if __name__ == "__main__":
    main()
