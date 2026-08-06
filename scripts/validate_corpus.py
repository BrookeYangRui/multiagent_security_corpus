#!/usr/bin/env python3
"""Validate structural invariants of the literature corpus."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_CSV = ROOT / "corpus" / "papers.csv"
SETS = ROOT / "corpus" / "sets"
SEARCH_SET = SETS / "01_search_catalog"
BROAD_SET = SETS / "02_broad_included"
ANALYSIS_SET = SETS / "05_analysis_specific"
EXCLUDED_CSV = SEARCH_SET / "structured_exclusions.csv"
REFERENCES = ROOT / "corpus" / "references.bib"
EVALUATION_ARTIFACTS = ANALYSIS_SET / "evaluation_artifacts.csv"
POST_CUTOFF_CSV = SEARCH_SET / "post_cutoff_papers.csv"
POST_CUTOFF_REFERENCES = SEARCH_SET / "post_cutoff_references.bib"
ATTACK_SCREENING_CSV = SEARCH_SET / "search_catalog.csv"
ATTACK_CANONICAL_BRIDGE_CSV = SEARCH_SET / "canonical_bridges.csv"
TARGETED_ATTACK_GAP_SEARCH_CSV = (
    SEARCH_SET / "targeted_gap_search.csv"
)
REVIEW_QUEUES = ROOT / "reviews" / "queues"
LOAD_BEARING_REVIEW_CSV = REVIEW_QUEUES / "load_bearing.csv"
ATTACK_REVIEW_CSV = REVIEW_QUEUES / "standard_attack.csv"
CROSS_CATEGORY_REVIEW_CSV = (
    REVIEW_QUEUES / "cross_category.csv"
)
UNIVERSAL_REVIEW_CSV = REVIEW_QUEUES / "universal.csv"
PEER_FIRST_CSV = BROAD_SET / "broad_included.csv"
DEDUPLICATION_MAP_CSV = BROAD_SET / "deduplication_map.csv"
PUBLICATION_OVERRIDES_CSV = (
    BROAD_SET / "publication_status_overrides.csv"
)
UNIVERSAL_SOURCE_REVIEW_CSV = (
    ROOT / "reviews" / "universal" / "universal_114_source_review.csv"
)
UNIVERSAL_SOURCE_CORRECTIONS_CSV = (
    ROOT / "reviews" / "universal" / "universal_source_review_corrections.csv"
)
FINAL_DIR = ROOT / "corpus" / "final"
FINAL_ALL_CSV = FINAL_DIR / "all_relevant_papers.csv"
FINAL_PEER_CSV = FINAL_DIR / "peer_reviewed.csv"
FINAL_NONPEER_CSV = FINAL_DIR / "non_peer_citations_gt_10.csv"

PAPER_FIELDS = [
    "paper_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "paper_type", "primary_category", "topic",
    "scope_relation",
    "application_domain", "multiagent_dependency", "attack", "defense",
    "system_failure", "evaluation", "discovery_source", "discovery_query",
    "accessed_version", "access_date", "note_path", "prepared_by",
    "verification_status", "inclusion_status", "exclusion_reason",
]
EXCLUDED_FIELDS = [
    "paper_id", "title", "authors", "year", "primary_url",
    "discovery_source", "discovery_query", "screening_stage",
    "exclusion_reason", "canonical_paper_id", "screened_by",
    "screening_date", "notes",
]
EVALUATION_ARTIFACT_FIELDS = [
    "artifact_id", "artifact_name", "artifact_type", "canonical_paper_id",
    "paper_title", "primary_category", "note_path", "evaluation_focus",
    "unit", "denominator", "metrics", "availability_url",
    "publication_status", "notes",
]
POST_CUTOFF_FIELDS = [
    "paper_id", "title", "authors", "source_date", "primary_url",
    "publication_status", "scope_status", "note_path", "last_checked",
    "cutoff_reason",
]
ATTACK_SCREENING_FIELDS = [
    "record_id", "title", "publication_date", "venue", "doi", "arxiv_id",
    "sources", "query_ids", "lexical_decision", "semantic_decision",
    "full_text_decision", "final_decision", "attack_candidate",
    "attack_decision", "canonical_paper_id", "canonical_primary_category",
    "scope_relation", "screening_note",
]
ATTACK_CANONICAL_BRIDGE_FIELDS = [
    "paper_id", "title", "primary_url", "bridge_source", "bridge_reason",
]
TARGETED_ATTACK_GAP_SEARCH_FIELDS = [
    "search_family", "query", "source", "candidate_title", "primary_url",
    "publication_status", "decision", "reason", "canonical_paper_id",
    "checked_date",
]
LOAD_BEARING_REVIEW_FIELDS = [
    "priority", "paper_id", "risk_family", "review_focus", "primary_url",
    "note_path", "metadata_precheck", "evidence_locator_precheck",
    "scope_precheck", "human_review_status", "reviewer",
    "adjudication_note",
]
ATTACK_REVIEW_FIELDS = [
    "priority", "paper_id", "review_focus", "review_level",
    "human_review_status", "reviewer", "adjudication_note",
]
CROSS_CATEGORY_REVIEW_FIELDS = [
    "priority", "paper_id", "title", "year", "venue", "primary_category",
    "paper_type", "scope_relation", "primary_url", "note_path",
    "review_focus", "minimum_review_status", "attack_evidence_status",
    "attack_role", "attack_instance_coding_required", "reviewer",
    "review_date", "adjudication_note",
]
UNIVERSAL_REVIEW_FIELDS = [
    "review_track", "track_priority", "paper_id", "title", "year", "venue",
    "primary_category", "paper_type", "scope_relation", "primary_url",
    "note_path", "minimum_review_status", "attack_evidence_status",
    "attack_role", "attack_instance_coding_required", "reviewer",
    "review_date", "adjudication_note",
]
PEER_FIRST_FIELDS = [
    "record_id", "title", "publication_date", "screened_venue",
    "canonical_venue", "doi", "canonical_doi", "arxiv_id",
    "scope_decision", "publication_status", "venue_type",
    "publication_evidence_type", "publication_evidence_url",
    "publication_override", "semantic_scholar_id",
    "semantic_scholar_title_match", "citations_semantic_scholar",
    "citation_snapshot_date", "peer_first_stratum",
]
PUBLICATION_OVERRIDE_FIELDS = [
    "record_id", "publication_status", "venue_type", "canonical_venue",
    "canonical_doi", "evidence_type", "evidence_url", "checked_date", "note",
]
DEDUPLICATION_MAP_FIELDS = [
    "duplicate_record_id", "canonical_record_id", "canonical_doi", "reason",
]
UNIVERSAL_SOURCE_REVIEW_FIELDS = [
    "global_priority", "review_track", "paper_id", "canonical_title",
    "canonical_authors", "canonical_year", "canonical_venue", "doi",
    "source_url", "version_status", "identity_verdict", "current_scope",
    "recommended_scope", "scope_rationale", "current_category",
    "recommended_category", "secondary_roles", "multiagent_verdict",
    "attack_evidence_status", "attack_role",
    "attack_instance_coding_required", "adversary_position",
    "adversary_capabilities", "preconditions", "mechanism",
    "attack_surfaces", "primary_system_failure", "reported_impact",
    "agent_count_or_configuration", "topology", "communication",
    "baselines", "metric_definition", "unit_denominator",
    "system_level_impact_verified", "evidence_locators",
    "author_claim_vs_corpus_interpretation", "limitations_maturity",
    "key_corrections", "review_outcome", "promote_to_load_bearing",
    "review_status",
]
UNIVERSAL_SOURCE_CORRECTION_FIELDS = [
    "severity", "global_priority", "paper_id", "title", "review_track",
    "field_or_category", "current_coding", "recommended_correction",
    "rationale", "evidence_source", "author_signoff_required",
]
FINAL_PAPER_FIELDS = [
    "paper_id", "title", "authors", "year", "venue", "venue_family",
    "venue_type", "doi", "primary_url", "open_access_url",
    "publication_status", "scope_relation", "primary_role",
    "interaction_dependency", "security_relevance", "evidence_level",
    "evidence_locator", "discovery_source", "cutoff", "cutoff_basis",
    "note_path",
]
FINAL_NONPEER_FIELDS = [
    "paper_id", "title", "year", "venue", "arxiv_id", "doi",
    "primary_url", "citations", "citation_source", "citation_snapshot_date",
    "scope_relation", "screening_status", "threshold_rule", "cutoff",
    "semantic_scholar_id",
]
VERIFICATION_STATES = {
    "agent_unverified", "metadata_verified", "evidence_verified",
    "fully_reviewed",
}
INCLUSION_STATES = {"included", "excluded", "pending"}
PRIMARY_CATEGORIES = {"attack", "defense", "evaluation", "survey", "general"}
SCOPE_RELATIONS = {"core_security", "security_relevant", "adjacent"}
ATTACK_EVIDENCE_STATES = {
    "confirmed_attack_bearing", "confirmed_attack_bearing_secondary",
    "confirmed_attack_mention_only", "confirmed_not_attack_bearing",
    "dual_use_no_malicious_claim_confirmed", "candidate_from_primary_category",
    "candidate_from_secondary_role", "not_screened",
}
ATTACK_CODING_DECISIONS = {"yes", "no", "pending", "conditional"}
BIB_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)


def read_csv(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != expected_fields:
            raise ValueError(
                f"{path.relative_to(ROOT)} has an unexpected header\n"
                f"expected: {expected_fields}\nactual:   {reader.fieldnames}"
            )
        return list(reader)


def duplicates(values: list[str]) -> set[str]:
    return {value for value in values if value and values.count(value) > 1}


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def normalized_doi(value: str) -> str:
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.casefold()).strip()


def normalized_url(value: str) -> str:
    return value.casefold().strip().rstrip("/")


def main() -> int:
    errors: list[str] = []
    try:
        papers = read_csv(PAPERS_CSV, PAPER_FIELDS)
        excluded = read_csv(EXCLUDED_CSV, EXCLUDED_FIELDS)
        evaluation_artifacts = read_csv(
            EVALUATION_ARTIFACTS, EVALUATION_ARTIFACT_FIELDS
        )
        post_cutoff = read_csv(POST_CUTOFF_CSV, POST_CUTOFF_FIELDS)
        attack_screening = read_csv(ATTACK_SCREENING_CSV, ATTACK_SCREENING_FIELDS)
        attack_canonical_bridge = read_csv(
            ATTACK_CANONICAL_BRIDGE_CSV, ATTACK_CANONICAL_BRIDGE_FIELDS
        )
        targeted_attack_gap_search = read_csv(
            TARGETED_ATTACK_GAP_SEARCH_CSV,
            TARGETED_ATTACK_GAP_SEARCH_FIELDS,
        )
        load_bearing_review = read_csv(
            LOAD_BEARING_REVIEW_CSV, LOAD_BEARING_REVIEW_FIELDS
        )
        attack_review = read_csv(ATTACK_REVIEW_CSV, ATTACK_REVIEW_FIELDS)
        cross_category_review = read_csv(
            CROSS_CATEGORY_REVIEW_CSV, CROSS_CATEGORY_REVIEW_FIELDS
        )
        universal_review = read_csv(
            UNIVERSAL_REVIEW_CSV, UNIVERSAL_REVIEW_FIELDS
        )
        peer_first = read_csv(PEER_FIRST_CSV, PEER_FIRST_FIELDS)
        publication_overrides = read_csv(
            PUBLICATION_OVERRIDES_CSV, PUBLICATION_OVERRIDE_FIELDS
        )
        deduplication_map = read_csv(
            DEDUPLICATION_MAP_CSV, DEDUPLICATION_MAP_FIELDS
        )
        universal_source_review = read_csv(
            UNIVERSAL_SOURCE_REVIEW_CSV,
            UNIVERSAL_SOURCE_REVIEW_FIELDS,
        )
        universal_source_corrections = read_csv(
            UNIVERSAL_SOURCE_CORRECTIONS_CSV,
            UNIVERSAL_SOURCE_CORRECTION_FIELDS,
        )
        final_all = read_csv(FINAL_ALL_CSV, FINAL_PAPER_FIELDS)
        final_peer = read_csv(FINAL_PEER_CSV, FINAL_PAPER_FIELDS)
        final_nonpeer = read_csv(FINAL_NONPEER_CSV, FINAL_NONPEER_FIELDS)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    bib_keys = BIB_KEY.findall(REFERENCES.read_text(encoding="utf-8"))
    bib_key_set = set(bib_keys)
    post_cutoff_bib_keys = BIB_KEY.findall(
        POST_CUTOFF_REFERENCES.read_text(encoding="utf-8")
    )
    for key in sorted(duplicates(bib_keys)):
        errors.append(f"duplicate BibTeX key: {key}")

    for field in ("paper_id", "bibtex_key", "note_path"):
        for value in sorted(duplicates([row[field].strip() for row in papers])):
            errors.append(f"duplicate {field}: {value}")

    canonical_keys = {
        "normalized title": [normalized_title(row["title"]) for row in papers],
        "DOI": [normalized_doi(row["doi"]) for row in papers],
        "primary URL": [normalized_url(row["primary_url"]) for row in papers],
    }
    for label, values in canonical_keys.items():
        for value in sorted(duplicates(values)):
            errors.append(f"duplicate canonical {label}: {value}")

    excluded_ids = [row["paper_id"].strip() for row in excluded]
    for value in sorted(duplicates(excluded_ids)):
        errors.append(f"duplicate excluded paper_id: {value}")

    post_cutoff_ids = [row["paper_id"].strip() for row in post_cutoff]
    for value in sorted(duplicates(post_cutoff_ids)):
        errors.append(f"duplicate post-cutoff paper_id: {value}")
    corpus_ids = {row["paper_id"].strip() for row in papers}
    papers_by_id = {row["paper_id"].strip(): row for row in papers}
    final_ids = [row["paper_id"].strip() for row in final_all]
    if len(final_ids) != len(corpus_ids) or set(final_ids) != corpus_ids:
        errors.append(
            "all_relevant_papers.csv must exactly equal the canonical papers.csv ID set"
        )
    final_subsets = (
        ("peer_reviewed.csv", final_peer),
        ("non_peer_citations_gt_10.csv", final_nonpeer),
    )
    for label, rows in final_subsets:
        ids = [row["paper_id"].strip() for row in rows]
        if duplicates(ids):
            errors.append(f"{label} contains duplicate paper IDs")
        if not set(ids).issubset(corpus_ids):
            errors.append(f"{label} contains papers outside the canonical corpus")
    for line, row in enumerate(final_all, start=2):
        paper = papers_by_id.get(row["paper_id"].strip())
        if paper and row["note_path"].strip() != paper["note_path"].strip():
            errors.append(
                f"all_relevant_papers.csv:{line}: note_path does not match papers.csv"
            )
    for value in sorted(corpus_ids.intersection(post_cutoff_ids)):
        errors.append(f"post-cutoff paper appears in papers.csv: {value}")
    for value in sorted(set(excluded_ids).intersection(post_cutoff_ids)):
        errors.append(f"post-cutoff paper appears in excluded_papers.csv: {value}")
    for value in sorted(duplicates(post_cutoff_bib_keys)):
        errors.append(f"duplicate post-cutoff BibTeX key: {value}")
    for value in sorted(set(bib_keys).intersection(post_cutoff_bib_keys)):
        errors.append(f"post-cutoff BibTeX key appears in references.bib: {value}")

    screening_ids = [row["record_id"].strip() for row in attack_screening]
    for value in sorted(duplicates(screening_ids)):
        errors.append(f"duplicate attack screening record_id: {value}")
    allowed_attack_decisions = {
        "not_in_attack_query_frame", "included_attack_canonical",
        "included_other_primary", "eligible_not_in_corpus",
        "excluded_at_screening", "unresolved",
    }
    for line, row in enumerate(attack_screening, start=2):
        candidate = row["attack_candidate"].strip()
        decision = row["attack_decision"].strip()
        canonical_id = row["canonical_paper_id"].strip()
        if candidate not in {"yes", "no"}:
            errors.append(
                f"attack_screening.csv:{line}: invalid attack_candidate: "
                f"{candidate}"
            )
        if decision not in allowed_attack_decisions:
            errors.append(
                f"attack_screening.csv:{line}: invalid attack_decision: "
                f"{decision}"
            )
        if canonical_id and canonical_id not in papers_by_id:
            errors.append(
                f"attack_screening.csv:{line}: unknown canonical_paper_id: "
                f"{canonical_id}"
            )
        if candidate == "no" and decision != "not_in_attack_query_frame":
            errors.append(
                f"attack_screening.csv:{line}: non-candidate has a candidate "
                f"decision: {decision}"
            )

    included_screen_ids = {
        row["record_id"] for row in attack_screening
        if row["final_decision"] == "include-primary-interaction-security"
    }
    duplicate_inclusion_ids = {
        row["duplicate_record_id"].strip() for row in deduplication_map
    }
    canonical_inclusion_ids = {
        row["canonical_record_id"].strip() for row in deduplication_map
    }
    for line, row in enumerate(deduplication_map, start=2):
        if row["duplicate_record_id"].strip() not in included_screen_ids:
            errors.append(
                f"deduplication_map.csv:{line}: duplicate is outside included "
                "screen"
            )
        if row["canonical_record_id"].strip() not in included_screen_ids:
            errors.append(
                f"deduplication_map.csv:{line}: canonical record is outside "
                "included screen"
            )
    expected_peer_first_ids = included_screen_ids - duplicate_inclusion_ids
    peer_first_ids = [row["record_id"] for row in peer_first]
    if (
        set(peer_first_ids) != expected_peer_first_ids
        or len(peer_first_ids) != len(expected_peer_first_ids)
    ):
        errors.append(
            "broad_included.csv must contain every canonical scope-included "
            "work exactly once"
        )
    if not canonical_inclusion_ids.issubset(set(peer_first_ids)):
        errors.append("deduplication map canonical records are absent from broad corpus")
    allowed_strata = {
        "peer_reviewed_conference", "peer_reviewed_journal",
        "influential_non_peer", "emerging_non_peer",
        "unresolved_citation_or_publication_status",
    }
    for line, row in enumerate(peer_first, start=2):
        stratum = row["peer_first_stratum"]
        if stratum not in allowed_strata:
            errors.append(
                f"peer_first_eligibility.csv:{line}: invalid stratum: {stratum}"
            )
        citation = row["citations_semantic_scholar"]
        if stratum == "influential_non_peer" and (
            not citation.isdigit() or int(citation) <= 10
        ):
            errors.append(
                f"peer_first_eligibility.csv:{line}: influential non-peer "
                "does not satisfy citations > 10"
            )
    override_ids = [row["record_id"] for row in publication_overrides]
    for record_id in duplicates(override_ids):
        errors.append(f"duplicate publication override: {record_id}")
    for record_id in set(override_ids) - included_screen_ids:
        errors.append(f"publication override is outside included screen: {record_id}")

    bridge_ids = [row["paper_id"].strip() for row in attack_canonical_bridge]
    for value in sorted(duplicates(bridge_ids)):
        errors.append(f"duplicate attack canonical bridge paper_id: {value}")
    exact_attack_bindings = {
        row["canonical_paper_id"].strip()
        for row in attack_screening
        if row["attack_decision"].strip() == "included_attack_canonical"
    }
    for line, row in enumerate(attack_canonical_bridge, start=2):
        paper_id = row["paper_id"].strip()
        if paper_id not in papers_by_id:
            errors.append(
                f"attack_canonical_bridge.csv:{line}: unknown paper_id: "
                f"{paper_id}"
            )
            continue
        paper = papers_by_id[paper_id]
        if paper["primary_category"].strip() != "attack":
            errors.append(
                f"attack_canonical_bridge.csv:{line}: non-attack paper: "
                f"{paper_id}"
            )
        if row["title"].strip() != paper["title"].strip():
            errors.append(
                f"attack_canonical_bridge.csv:{line}: title mismatch: "
                f"{paper_id}"
            )
        if row["primary_url"].strip() != paper["primary_url"].strip():
            errors.append(
                f"attack_canonical_bridge.csv:{line}: URL mismatch: "
                f"{paper_id}"
            )
        if not row["bridge_reason"].strip():
            errors.append(
                f"attack_canonical_bridge.csv:{line}: missing bridge reason"
            )
        if paper_id in exact_attack_bindings:
            errors.append(
                f"attack canonical paper has both exact and bridge bindings: "
                f"{paper_id}"
            )

    attack_paper_ids = {
        row["paper_id"].strip()
        for row in papers
        if row["primary_category"].strip() == "attack"
    }
    represented_attack_ids = exact_attack_bindings | set(bridge_ids)
    for paper_id in sorted(attack_paper_ids - represented_attack_ids):
        errors.append(f"attack paper has no screening bridge: {paper_id}")
    for paper_id in sorted(represented_attack_ids - attack_paper_ids):
        errors.append(f"attack screening bridge targets non-attack: {paper_id}")

    allowed_gap_families = {
        "denial_of_service", "goal_drift", "identity_sybil",
        "shared_memory_poisoning",
    }
    for line, row in enumerate(targeted_attack_gap_search, start=2):
        family = row["search_family"].strip()
        canonical_id = row["canonical_paper_id"].strip()
        primary_url = row["primary_url"].strip()
        if family not in allowed_gap_families:
            errors.append(
                f"targeted_attack_gap_search.csv:{line}: invalid family: "
                f"{family}"
            )
        if not row["query"].strip() or not row["decision"].strip() or not row[
            "reason"
        ].strip():
            errors.append(
                f"targeted_attack_gap_search.csv:{line}: incomplete decision"
            )
        if primary_url and not primary_url.startswith(("https://", "http://")):
            errors.append(
                f"targeted_attack_gap_search.csv:{line}: invalid URL: "
                f"{primary_url}"
            )
        if canonical_id and canonical_id not in papers_by_id:
            errors.append(
                f"targeted_attack_gap_search.csv:{line}: unknown canonical "
                f"paper: {canonical_id}"
            )
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["checked_date"].strip()):
            errors.append(
                f"targeted_attack_gap_search.csv:{line}: invalid checked date"
            )

    review_ids = [row["paper_id"].strip() for row in load_bearing_review]
    for value in sorted(duplicates(review_ids)):
        errors.append(f"duplicate load-bearing review paper_id: {value}")
    for line, row in enumerate(load_bearing_review, start=2):
        paper_id = row["paper_id"].strip()
        note = row["note_path"].strip()
        if paper_id not in papers_by_id:
            errors.append(
                f"load_bearing_review_queue.csv:{line}: unknown paper_id: "
                f"{paper_id}"
            )
            continue
        if note != papers_by_id[paper_id]["note_path"].strip():
            errors.append(
                f"load_bearing_review_queue.csv:{line}: note_path does not "
                f"match canonical paper: {note}"
            )
        if row["human_review_status"].strip() not in {
            "pending_human_review", "in_review", "completed",
            "source_reviewed_pending_author_signoff",
            "blocked_pending_final_source",
            "blocked_pending_exact_full_text",
        }:
            errors.append(
                f"load_bearing_review_queue.csv:{line}: invalid human review "
                f"status: {row['human_review_status']}"
            )
        if row["human_review_status"].strip() == "completed" and not row[
            "reviewer"
        ].strip():
            errors.append(
                f"load_bearing_review_queue.csv:{line}: completed review has "
                "no reviewer"
            )

    attack_review_ids = [row["paper_id"].strip() for row in attack_review]
    for value in sorted(duplicates(attack_review_ids)):
        errors.append(f"duplicate attack review paper_id: {value}")
    for value in sorted(set(review_ids).intersection(attack_review_ids)):
        errors.append(f"paper appears in both review queues: {value}")
    for line, row in enumerate(attack_review, start=2):
        paper_id = row["paper_id"].strip()
        if paper_id not in papers_by_id:
            errors.append(
                f"attack_review_queue.csv:{line}: unknown paper_id: {paper_id}"
            )
            continue
        if papers_by_id[paper_id]["primary_category"].strip() != "attack":
            errors.append(
                f"attack_review_queue.csv:{line}: non-attack paper: {paper_id}"
            )
        if row["review_level"].strip() != "standard_attack_review":
            errors.append(
                f"attack_review_queue.csv:{line}: invalid review level"
            )
        status = row["human_review_status"].strip()
        if status not in {"pending_human_review", "in_review", "completed"}:
            errors.append(
                f"attack_review_queue.csv:{line}: invalid review status: "
                f"{status}"
            )
        if status == "completed" and (
            not row["reviewer"].strip() or not row["adjudication_note"].strip()
        ):
            errors.append(
                f"attack_review_queue.csv:{line}: completed review requires "
                "reviewer and adjudication note"
            )

    load_bearing_attack_ids = {
        paper_id for paper_id in review_ids
        if paper_id in papers_by_id
        and papers_by_id[paper_id]["primary_category"].strip() == "attack"
    }
    reviewed_attack_frame = load_bearing_attack_ids | set(attack_review_ids)
    if reviewed_attack_frame != attack_paper_ids:
        for paper_id in sorted(attack_paper_ids - reviewed_attack_frame):
            errors.append(f"attack paper is absent from review queues: {paper_id}")
        for paper_id in sorted(reviewed_attack_frame - attack_paper_ids):
            errors.append(f"review queue contains non-attack paper: {paper_id}")

    cross_review_ids = [
        row["paper_id"].strip() for row in cross_category_review
    ]
    for value in sorted(duplicates(cross_review_ids)):
        errors.append(f"duplicate cross-category review paper_id: {value}")
    expected_cross_ids = corpus_ids - set(review_ids) - set(attack_review_ids)
    if set(cross_review_ids) != expected_cross_ids:
        for paper_id in sorted(expected_cross_ids - set(cross_review_ids)):
            errors.append(f"paper is absent from cross-category review: {paper_id}")
        for paper_id in sorted(set(cross_review_ids) - expected_cross_ids):
            errors.append(f"unexpected cross-category review paper: {paper_id}")
    for line, row in enumerate(cross_category_review, start=2):
        paper_id = row["paper_id"].strip()
        if paper_id not in papers_by_id:
            errors.append(
                f"cross_category_review_queue.csv:{line}: unknown paper_id: "
                f"{paper_id}"
            )
            continue
        paper = papers_by_id[paper_id]
        for field in (
            "title", "year", "venue", "primary_category", "paper_type",
            "scope_relation", "primary_url", "note_path",
        ):
            if row[field].strip() != paper[field].strip():
                errors.append(
                    f"cross_category_review_queue.csv:{line}: {field} does "
                    f"not match papers.csv: {paper_id}"
                )
        if paper["primary_category"].strip() == "attack":
            errors.append(
                f"cross_category_review_queue.csv:{line}: attack-primary "
                f"paper: {paper_id}"
            )
        status = row["minimum_review_status"].strip()
        if status not in {
            "pending_minimum_review", "in_review", "completed",
            "blocked_pending_source",
        }:
            errors.append(
                f"cross_category_review_queue.csv:{line}: invalid review "
                f"status: {status}"
            )
        evidence_status = row["attack_evidence_status"].strip()
        if evidence_status not in ATTACK_EVIDENCE_STATES:
            errors.append(
                f"cross_category_review_queue.csv:{line}: invalid attack "
                f"evidence status: {evidence_status}"
            )
        coding = row["attack_instance_coding_required"].strip()
        if coding not in ATTACK_CODING_DECISIONS:
            errors.append(
                f"cross_category_review_queue.csv:{line}: invalid coding "
                f"decision: {coding}"
            )
        if status == "completed" and (
            not row["reviewer"].strip()
            or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["review_date"].strip())
            or not row["adjudication_note"].strip()
        ):
            errors.append(
                f"cross_category_review_queue.csv:{line}: completed review "
                "requires reviewer, date, and adjudication note"
            )

    universal_ids = [row["paper_id"].strip() for row in universal_review]
    universal_priorities = [
        row["track_priority"].strip() for row in universal_review
    ]
    for value in sorted(duplicates(universal_ids)):
        errors.append(f"duplicate universal review paper_id: {value}")
    for value in sorted(duplicates(universal_priorities)):
        errors.append(f"duplicate universal review priority: {value}")
    if set(universal_ids) != corpus_ids:
        for paper_id in sorted(corpus_ids - set(universal_ids)):
            errors.append(f"paper is absent from universal review: {paper_id}")
        for paper_id in sorted(set(universal_ids) - corpus_ids):
            errors.append(f"unknown paper in universal review: {paper_id}")
    expected_priorities = {str(value) for value in range(1, len(papers) + 1)}
    if set(universal_priorities) != expected_priorities:
        errors.append("universal review priorities are not contiguous")
    expected_tracks = {
        **{paper_id: "load_bearing" for paper_id in review_ids},
        **{paper_id: "standard_attack" for paper_id in attack_review_ids},
        **{paper_id: "cross_category" for paper_id in cross_review_ids},
    }
    for line, row in enumerate(universal_review, start=2):
        paper_id = row["paper_id"].strip()
        if paper_id not in papers_by_id:
            continue
        paper = papers_by_id[paper_id]
        if row["review_track"].strip() != expected_tracks.get(paper_id):
            errors.append(
                f"universal_review_queue.csv:{line}: wrong review track: "
                f"{paper_id}"
            )
        for field in (
            "title", "year", "venue", "primary_category", "paper_type",
            "scope_relation", "primary_url", "note_path",
        ):
            if row[field].strip() != paper[field].strip():
                errors.append(
                    f"universal_review_queue.csv:{line}: {field} does not "
                    f"match papers.csv: {paper_id}"
                )
        if row["attack_evidence_status"].strip() not in ATTACK_EVIDENCE_STATES:
            errors.append(
                f"universal_review_queue.csv:{line}: invalid attack evidence "
                f"status: {row['attack_evidence_status']}"
            )
        if row["attack_instance_coding_required"].strip() not in (
            ATTACK_CODING_DECISIONS
        ):
            errors.append(
                f"universal_review_queue.csv:{line}: invalid attack coding "
                f"decision: {row['attack_instance_coding_required']}"
            )

    source_ids = [row["paper_id"].strip() for row in universal_source_review]
    for value in sorted(duplicates(source_ids)):
        errors.append(f"duplicate universal source-review paper_id: {value}")
    if set(source_ids) != corpus_ids:
        for paper_id in sorted(corpus_ids - set(source_ids)):
            errors.append(
                f"paper is absent from universal source review: {paper_id}"
            )
        for paper_id in sorted(set(source_ids) - corpus_ids):
            errors.append(
                f"unknown paper in universal source review: {paper_id}"
            )

    source_track_counts = {
        track: sum(
            row["review_track"].strip() == track
            for row in universal_source_review
        )
        for track in ("load_bearing", "standard_attack", "cross_category")
    }
    expected_source_track_counts = {
        "load_bearing": len(load_bearing_review),
        "standard_attack": len(attack_review),
        "cross_category": len(cross_category_review),
    }
    if source_track_counts != expected_source_track_counts:
        errors.append(
            "universal source-review track counts do not match review queues"
        )

    allowed_source_statuses = {
        "assistant_source_reviewed_pending_author_signoff",
        "source_reviewed_pending_author_signoff",
        "blocked_pending_exact_source",
        "blocked_metadata_signoff",
    }
    for line, row in enumerate(universal_source_review, start=2):
        paper_id = row["paper_id"].strip()
        if row["review_status"].strip() not in allowed_source_statuses:
            errors.append(
                f"universal_114_source_review.csv:{line}: invalid review "
                f"status for {paper_id}: {row['review_status']}"
            )
        if not row["evidence_locators"].strip():
            errors.append(
                f"universal_114_source_review.csv:{line}: missing evidence "
                f"locators for {paper_id}"
            )
        if papers_by_id[paper_id]["verification_status"].strip() != "agent_unverified":
            errors.append(
                f"universal source review improperly upgraded verification: "
                f"{paper_id}"
            )

    if len(universal_source_corrections) != 231:
        errors.append(
            "universal_source_review_corrections.csv: expected 231 rows"
        )
    correction_source_ids = set(source_ids)
    for line, row in enumerate(universal_source_corrections, start=2):
        paper_id = row["paper_id"].strip()
        if paper_id not in correction_source_ids:
            errors.append(
                f"universal_source_review_corrections.csv:{line}: unknown "
                f"reviewed paper: {paper_id}"
            )
        if row["severity"].strip() not in {"critical", "high", "medium"}:
            errors.append(
                f"universal_source_review_corrections.csv:{line}: invalid "
                "severity"
            )
        if row["author_signoff_required"].strip() != "yes":
            errors.append(
                f"universal_source_review_corrections.csv:{line}: correction "
                "must require author signoff"
            )
        if not row["recommended_correction"].strip():
            errors.append(
                f"universal_source_review_corrections.csv:{line}: empty "
                "recommended correction"
            )

    for line, row in enumerate(post_cutoff, start=2):
        paper_id = row["paper_id"].strip()
        source_date = row["source_date"].strip()
        primary_url = row["primary_url"].strip()
        note = row["note_path"].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", source_date):
            errors.append(
                f"post_cutoff_papers.csv:{line}: invalid source_date for "
                f"{paper_id}: {source_date}"
            )
        if not primary_url.startswith(("https://", "http://")):
            errors.append(
                f"post_cutoff_papers.csv:{line}: invalid primary_url for "
                f"{paper_id}: {primary_url}"
            )
        if note:
            note_path = ROOT / note
            if not note_path.is_file():
                errors.append(
                    f"post_cutoff_papers.csv:{line}: note does not exist: {note}"
                )
            elif not note_path.is_relative_to(ROOT / "papers" / "post_cutoff"):
                errors.append(
                    f"post_cutoff_papers.csv:{line}: note is outside "
                    f"papers/post_cutoff/: {note}"
                )
            if paper_id not in post_cutoff_bib_keys:
                errors.append(
                    f"post_cutoff_papers.csv:{line}: retained note has no "
                    f"post-cutoff BibTeX entry: {paper_id}"
                )

    for line, row in enumerate(excluded, start=2):
        paper_id = row["paper_id"].strip()
        year = row["year"].strip()
        primary_url = row["primary_url"].strip()
        if not re.fullmatch(r"\d{4}", year):
            errors.append(
                f"excluded_papers.csv:{line}: invalid year for {paper_id}: {year}"
            )
        if not primary_url.startswith(("https://", "http://")):
            errors.append(
                f"excluded_papers.csv:{line}: invalid primary_url for "
                f"{paper_id}: {primary_url}"
            )

    artifact_ids = [row["artifact_id"].strip() for row in evaluation_artifacts]
    for value in sorted(duplicates(artifact_ids)):
        errors.append(f"duplicate evaluation artifact_id: {value}")

    for line, row in enumerate(papers, start=2):
        paper_id = row["paper_id"].strip()
        status = row["inclusion_status"].strip()
        verification = row["verification_status"].strip()
        primary_category = row["primary_category"].strip()
        scope_relation = row["scope_relation"].strip()
        key = row["bibtex_key"].strip()
        note = row["note_path"].strip()

        if not paper_id:
            errors.append(f"papers.csv:{line}: missing paper_id")
        if status not in INCLUSION_STATES:
            errors.append(f"papers.csv:{line}: invalid inclusion_status: {status}")
        if verification not in VERIFICATION_STATES:
            errors.append(
                f"papers.csv:{line}: invalid verification_status: {verification}"
            )
        if primary_category not in PRIMARY_CATEGORIES:
            errors.append(
                f"papers.csv:{line}: invalid primary_category: "
                f"{primary_category}"
            )
        if scope_relation not in SCOPE_RELATIONS:
            errors.append(
                f"papers.csv:{line}: invalid scope_relation: {scope_relation}"
            )
        if status == "included":
            if not key or key not in bib_key_set:
                errors.append(f"papers.csv:{line}: missing BibTeX entry: {key}")
            note_path = ROOT / note
            if not note or not note_path.is_file():
                errors.append(f"papers.csv:{line}: note does not exist: {note}")
            elif not note_path.is_relative_to(ROOT / "papers"):
                errors.append(f"papers.csv:{line}: note is outside papers/: {note}")

    for line, row in enumerate(evaluation_artifacts, start=2):
        artifact_id = row["artifact_id"].strip()
        canonical_id = row["canonical_paper_id"].strip()
        category = row["primary_category"].strip()
        note = row["note_path"].strip()

        if not artifact_id:
            errors.append(
                f"evaluation_artifacts.csv:{line}: missing artifact_id"
            )
        if canonical_id not in papers_by_id:
            errors.append(
                f"evaluation_artifacts.csv:{line}: unknown canonical_paper_id: "
                f"{canonical_id}"
            )
        elif note != papers_by_id[canonical_id]["note_path"].strip():
            errors.append(
                f"evaluation_artifacts.csv:{line}: note_path does not match "
                f"canonical paper: {note}"
            )
        if category not in {"attacks", "defenses", "evaluations", "general"}:
            errors.append(
                f"evaluation_artifacts.csv:{line}: invalid primary_category: "
                f"{category}"
            )
        note_path = ROOT / note
        if not note or not note_path.is_file():
            errors.append(
                f"evaluation_artifacts.csv:{line}: note does not exist: {note}"
            )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Corpus valid: {len(papers)} paper rows, {len(excluded)} exclusions, "
        f"{len(bib_keys)} BibTeX entries, "
        f"{len(evaluation_artifacts)} evaluation artifacts, "
        f"{len(post_cutoff)} post-cutoff watchlist records, and "
        f"{len(attack_screening)} attack-screening records; "
        f"{len(peer_first)} canonical broad-inclusion decisions, "
        f"{len(attack_canonical_bridge)} canonical attack bridges, "
        f"{len(targeted_attack_gap_search)} targeted gap decisions, and "
        f"{len(load_bearing_review)} load-bearing plus "
        f"{len(attack_review)} standard attack and "
        f"{len(cross_category_review)} cross-category reviews; "
        f"{len(universal_review)} papers in the universal checklist; "
        f"{len(final_all)} papers in the canonical final export; "
        f"{len(universal_source_corrections)} universal source-review "
        "corrections."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
