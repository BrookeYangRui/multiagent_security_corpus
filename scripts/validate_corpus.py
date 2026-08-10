#!/usr/bin/env python3
"""Validate structural invariants of the literature corpus."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_CSV = ROOT / "corpus" / "papers.csv"
CANONICAL_FIELD_OVERRIDES_CSV = (
    ROOT / "corpus" / "canonical_field_overrides.csv"
)
SETS = ROOT / "corpus" / "sets"
SEARCH_SET = SETS / "01_search_catalog"
BROAD_SET = SETS / "02_broad_included"
ANALYSIS_SET = SETS / "05_analysis_specific"
EXCLUDED_CSV = SEARCH_SET / "structured_exclusions.csv"
REFERENCES = ROOT / "corpus" / "references.bib"
EVALUATION_ARTIFACTS = ANALYSIS_SET / "evaluation_artifacts.csv"
EVALUATION_MEASUREMENT_CODING = (
    ANALYSIS_SET / "evaluation_measurement_coding.csv"
)
EVALUATION_MEASUREMENT_SUMMARY = (
    ANALYSIS_SET / "evaluation_measurement_summary.json"
)
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
    ROOT / "reviews" / "universal" / "active_source_review.csv"
)
UNIVERSAL_SOURCE_CORRECTIONS_CSV = (
    ROOT / "reviews" / "universal" / "active_source_review_corrections.csv"
)
SOK_DIR = ROOT / "sok_related"
SOK_PAPERS_CSV = SOK_DIR / "papers.csv"
SOK_EXCLUSIONS_CSV = SOK_DIR / "exclusions.csv"
SOK_REFERENCES = SOK_DIR / "references.bib"
FINAL_DIR = ROOT / "corpus" / "final"
FINAL_ALL_CSV = FINAL_DIR / "all_relevant_papers.csv"
FINAL_PEER_CSV = FINAL_DIR / "peer_reviewed.csv"
FINAL_NONPEER_CSV = FINAL_DIR / "non_peer_citations_gt_10.csv"
FINAL_INCLUDED_NONPEER_CSV = FINAL_DIR / "non_peer_included_citations_gt_10.csv"

PAPER_FIELDS = [
    "paper_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "paper_type", "primary_category", "topic",
    "scope_relation",
    "application_domain", "multiagent_dependency", "attack", "defense",
    "system_failure", "evaluation", "discovery_source", "discovery_query",
    "accessed_version", "access_date", "note_path", "prepared_by",
    "verification_status", "inclusion_status", "exclusion_reason",
]
CANONICAL_FIELD_OVERRIDE_FIELDS = [
    "paper_id", "field", "previous_value", "active_value", "reason",
    "evidence_source",
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
    "publication_status", "notes", "display_venue", "venue_type",
    "source_version",
]
EVALUATION_MEASUREMENT_FIELDS = [
    "artifact_id", "primary_eval_category", "secondary_eval_categories",
    "impact_stage_max", "interaction_counterfactual", "availability_kind",
    "coding_basis", "coding_status", "evidence_locator",
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
FINAL_INCLUDED_NONPEER_FIELDS = [
    "paper_id", "title", "year", "venue", "arxiv_id", "doi",
    "primary_url", "citations", "citation_source", "citation_snapshot_date",
    "scope_relation", "screening_status", "threshold_rule", "cutoff",
    "semantic_scholar_id",
]
SOK_FIELDS = [
    "sok_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "work_type", "relation_level",
    "multiagent_security_centrality", "publication_status",
    "first_public_date", "cutoff_status", "note_path", "accessed_version",
    "access_date", "prepared_by", "verification_status",
]
SOK_EXCLUSION_FIELDS = [
    "record_id", "title", "primary_url", "decision", "reason",
    "screened_date",
]
VERIFICATION_STATES = {
    "agent_unverified", "metadata_verified", "evidence_verified",
    "fully_reviewed",
}
INCLUSION_STATES = {"included", "excluded", "pending"}
PRIMARY_CATEGORIES = {"attack", "defense", "evaluation", "survey", "general"}
SCOPE_RELATIONS = {"core_security", "security_relevant", "adjacent"}
EVALUATION_PRIMARY_CATEGORIES = {
    "propagation_topology",
    "collective_decision_deception",
    "privacy_information_flow",
    "delegation_protocol_action",
    "trace_procedural_compliance",
    "adaptive_defense_detection",
}
EVALUATION_IMPACT_STAGES = {
    "S1_observable",
    "S2_trace",
    "S3_executed_or_persistent",
    "S4_deployment",
    "pending",
}
EVALUATION_COUNTERFACTUALS = {
    "matched_single_agent",
    "matched_architecture",
    "edge_state_authority_ablation",
    "component_or_attack_controls",
    "none_reported",
    "pending",
}
EVALUATION_AVAILABILITY_KINDS = {
    "code_and_data",
    "code_or_harness",
    "data_only",
    "project_page",
    "paper_only",
    "unverified",
}
EVALUATION_CODING_STATUSES = {
    "assistant_derived_pending_author_signoff",
}
EXPECTED_EVALUATION_PRIMARY_COUNTS = {
    "adaptive_defense_detection": 9,
    "collective_decision_deception": 8,
    "delegation_protocol_action": 6,
    "privacy_information_flow": 6,
    "propagation_topology": 11,
    "trace_procedural_compliance": 3,
}
EXPECTED_EVALUATION_PEER_PRIMARY_COUNTS = {
    "adaptive_defense_detection": 2,
    "collective_decision_deception": 7,
    "delegation_protocol_action": 6,
    "privacy_information_flow": 4,
    "propagation_topology": 6,
    "trace_procedural_compliance": 1,
}
EXPECTED_EVALUATION_OTHER_PRIMARY_COUNTS = {
    "adaptive_defense_detection": 7,
    "collective_decision_deception": 1,
    "delegation_protocol_action": 0,
    "privacy_information_flow": 2,
    "propagation_topology": 5,
    "trace_procedural_compliance": 2,
}
EXPECTED_EVALUATION_ARTIFACT_IDS = {
    "artifact_tamas",
    "artifact_aciarena",
    "artifact_risklab",
    "artifact_liecraft",
    "artifact_agentleak",
    "artifact_pear",
    "artifact_amongus_aamas",
    "artifact_magpie",
    "artifact_gambit",
    "artifact_gammaf",
    "artifact_harp",
    "artifact_calbench",
    "artifact_colosseum",
    "artifact_macbench",
    "artifact_netsafe",
    "artifact_mama",
    "artifact_psysafe",
    "artifact_masleak",
    "artifact_amongus_attack",
    "artifact_controlvalve",
    "artifact_architecture_matters",
    "artifact_a2asecbench",
    "artifact_safeagents",
    "artifact_troublemaker",
    "artifact_master",
    "artifact_shadows_code",
    "artifact_lying_truths",
    "artifact_hierarchical_attacks",
    "artifact_faulty_agents",
    "artifact_financial_fraud",
    "artifact_trust_paradox",
    "artifact_prompt_infection",
    "artifact_whos_mole",
    "artifact_collaborative_shadows",
    "artifact_dont_trust_upstream",
    "artifact_blindguard",
    "artifact_medsentry",
    "artifact_badacts",
    "artifact_sgoatmas",
    "artifact_misinfotask",
    "artifact_alteda_traces",
    "artifact_colludebench_v0",
    "artifact_valueflow",
}
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
        canonical_field_overrides = read_csv(
            CANONICAL_FIELD_OVERRIDES_CSV,
            CANONICAL_FIELD_OVERRIDE_FIELDS,
        )
        excluded = read_csv(EXCLUDED_CSV, EXCLUDED_FIELDS)
        evaluation_artifacts = read_csv(
            EVALUATION_ARTIFACTS, EVALUATION_ARTIFACT_FIELDS
        )
        evaluation_measurement = read_csv(
            EVALUATION_MEASUREMENT_CODING,
            EVALUATION_MEASUREMENT_FIELDS,
        )
        evaluation_summary_text = EVALUATION_MEASUREMENT_SUMMARY.read_text(
            encoding="utf-8"
        )
        evaluation_summary = json.loads(evaluation_summary_text)
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
        final_included_nonpeer = read_csv(
            FINAL_INCLUDED_NONPEER_CSV, FINAL_INCLUDED_NONPEER_FIELDS
        )
        sok_papers = read_csv(SOK_PAPERS_CSV, SOK_FIELDS)
        sok_exclusions = read_csv(SOK_EXCLUSIONS_CSV, SOK_EXCLUSION_FIELDS)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    bib_keys = BIB_KEY.findall(REFERENCES.read_text(encoding="utf-8"))
    bib_key_set = set(bib_keys)
    post_cutoff_bib_keys = BIB_KEY.findall(
        POST_CUTOFF_REFERENCES.read_text(encoding="utf-8")
    )
    sok_bib_keys = BIB_KEY.findall(SOK_REFERENCES.read_text(encoding="utf-8"))
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
    override_keys: list[tuple[str, str]] = []
    for line, row in enumerate(canonical_field_overrides, start=2):
        paper_id = row["paper_id"].strip()
        field = row["field"].strip()
        override_keys.append((paper_id, field))
        if paper_id not in papers_by_id:
            errors.append(
                f"canonical_field_overrides.csv:{line}: unknown paper_id"
            )
            continue
        if field not in PAPER_FIELDS or field == "paper_id":
            errors.append(
                f"canonical_field_overrides.csv:{line}: invalid field"
            )
            continue
        if papers_by_id[paper_id][field] != row["active_value"]:
            errors.append(
                f"canonical_field_overrides.csv:{line}: active value was not applied"
            )
    for paper_id, field in sorted(duplicates(override_keys)):
        errors.append(
            "canonical_field_overrides.csv contains duplicate override: "
            f"{paper_id}/{field}"
        )
    sok_ids = [row["sok_id"].strip() for row in sok_papers]
    if duplicates(sok_ids):
        errors.append("sok_related/papers.csv contains duplicate sok_id values")
    expected_sok_bib_keys = {
        row["bibtex_key"].strip() for row in sok_papers
    }
    if set(sok_bib_keys) != expected_sok_bib_keys:
        errors.append("sok-related BibTeX keys must exactly match its records")
    if duplicates(sok_bib_keys):
        errors.append("sok_related/references.bib contains duplicate keys")
    for line, row in enumerate(sok_papers, start=2):
        note = ROOT / row["note_path"]
        if (
            not note.is_file()
            or not note.is_relative_to(ROOT / "papers" / "surveys")
        ):
            errors.append(
                f"sok_related/papers.csv:{line}: invalid survey note path"
            )
        if row["relation_level"] not in {"direct", "strongly_related"}:
            errors.append(
                f"sok_related/papers.csv:{line}: invalid relation level"
            )
        if row["verification_status"] != "agent_unverified":
            errors.append(
                f"sok_related/papers.csv:{line}: invalid verification status"
            )
        if row["cutoff_status"] not in {"pre_cutoff", "post_cutoff"}:
            errors.append(
                f"sok_related/papers.csv:{line}: invalid cutoff status"
            )
        first_public_date = row["first_public_date"]
        expected_cutoff = None
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", first_public_date):
            expected_cutoff = (
                "pre_cutoff"
                if first_public_date < "2026-07-01"
                else "post_cutoff"
            )
        elif first_public_date != "Not reported":
            errors.append(
                f"sok_related/papers.csv:{line}: invalid first public date"
            )
        if expected_cutoff and row["cutoff_status"] != expected_cutoff:
            errors.append(
                f"sok_related/papers.csv:{line}: cutoff status/date mismatch"
            )
    excluded_sok_ids = [row["record_id"].strip() for row in sok_exclusions]
    if duplicates(excluded_sok_ids):
        errors.append("sok_related/exclusions.csv contains duplicate record IDs")
    if set(sok_ids).intersection(excluded_sok_ids):
        errors.append("a work cannot be both SoK-related included and excluded")
    final_ids = [row["paper_id"].strip() for row in final_all]
    final_by_id = {row["paper_id"].strip(): row for row in final_all}
    if len(final_ids) != len(corpus_ids) or set(final_ids) != corpus_ids:
        errors.append(
            "all_relevant_papers.csv must exactly equal the canonical papers.csv ID set"
        )
    final_subsets = (
        ("peer_reviewed.csv", final_peer),
        ("non_peer_included_citations_gt_10.csv", final_included_nonpeer),
    )
    for label, rows in final_subsets:
        ids = [row["paper_id"].strip() for row in rows]
        if duplicates(ids):
            errors.append(f"{label} contains duplicate paper IDs")
        if not set(ids).issubset(corpus_ids):
            errors.append(f"{label} contains papers outside the canonical corpus")
    if len(final_peer) != 90:
        errors.append(
            f"peer_reviewed.csv must contain the frozen 90-work publication view, "
            f"found {len(final_peer)}"
        )
    expected_peer_by_id = {
        row["paper_id"].strip(): row
        for row in final_all
        if row["publication_status"].strip() == "peer_reviewed"
    }
    actual_peer_by_id = {
        row["paper_id"].strip(): row
        for row in final_peer
    }
    if set(actual_peer_by_id) != set(expected_peer_by_id):
        errors.append(
            "peer_reviewed.csv must exactly project the peer-reviewed IDs from "
            "all_relevant_papers.csv"
        )
    for paper_id in sorted(set(actual_peer_by_id) & set(expected_peer_by_id)):
        if actual_peer_by_id[paper_id] != expected_peer_by_id[paper_id]:
            errors.append(
                f"peer_reviewed.csv row differs from all_relevant_papers.csv: "
                f"{paper_id}"
            )
    for line, row in enumerate(final_peer, start=2):
        if row["publication_status"].strip() != "peer_reviewed":
            errors.append(
                f"peer_reviewed.csv:{line}: publication_status is not peer_reviewed"
            )
        if row["venue_type"].strip() not in {"conference", "journal"}:
            errors.append(
                f"peer_reviewed.csv:{line}: non-archival venue_type: "
                f"{row['venue_type']}"
            )
    exported_candidate_ids = [row["paper_id"] for row in final_nonpeer]
    included_nonpeer_ids = [
        row["paper_id"] for row in final_included_nonpeer
    ]
    if set(exported_candidate_ids) != set(included_nonpeer_ids):
        errors.append(
            "the two authoritative non-peer exports must contain the same IDs"
        )
    if not set(exported_candidate_ids).issubset(corpus_ids):
        errors.append("non-peer export contains papers outside the canonical corpus")
    if duplicates(exported_candidate_ids):
        errors.append("non_peer_citations_gt_10.csv contains duplicate record IDs")
    for line, row in enumerate(final_all, start=2):
        paper = papers_by_id.get(row["paper_id"].strip())
        if paper and row["note_path"].strip() != paper["note_path"].strip():
            errors.append(
                f"all_relevant_papers.csv:{line}: note_path does not match papers.csv"
            )
        if (
            paper
            and row["interaction_dependency"].strip()
            != paper["multiagent_dependency"].strip()
        ):
            errors.append(
                f"all_relevant_papers.csv:{line}: interaction dependency does not "
                "match papers.csv"
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
    source_by_id = {
        row["paper_id"].strip(): row for row in universal_source_review
    }
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
    for line, row in enumerate(final_all, start=2):
        review = source_by_id.get(row["paper_id"].strip())
        if review and row["evidence_level"].strip() != review["review_status"].strip():
            errors.append(
                f"all_relevant_papers.csv:{line}: evidence level does not match "
                "active source review"
            )
        if review and row["evidence_locator"].strip() != review["evidence_locators"].strip():
            errors.append(
                f"all_relevant_papers.csv:{line}: evidence locator does not match "
                "active source review"
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
        "official_metadata_and_abstract_screened",
        "official_arxiv_metadata_and_abstract_screened",
        "official_workshop_metadata_and_full_text_screened",
        "boundary_full_text_screened",
        "full_text_scope_screened",
        "claim_level_review_required",
    }
    for line, row in enumerate(universal_source_review, start=2):
        paper_id = row["paper_id"].strip()
        if row["review_status"].strip() not in allowed_source_statuses:
            errors.append(
                f"active_source_review.csv:{line}: invalid review "
                f"status for {paper_id}: {row['review_status']}"
            )
        if not row["evidence_locators"].strip():
            errors.append(
                f"active_source_review.csv:{line}: missing evidence "
                f"locators for {paper_id}"
            )
        if papers_by_id[paper_id]["verification_status"].strip() != "agent_unverified":
            errors.append(
                f"universal source review improperly upgraded verification: "
                f"{paper_id}"
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
    artifact_id_set = set(artifact_ids)
    if (
        len(evaluation_artifacts) != len(EXPECTED_EVALUATION_ARTIFACT_IDS)
        or artifact_id_set != EXPECTED_EVALUATION_ARTIFACT_IDS
    ):
        errors.append(
            "evaluation_artifacts.csv must exactly equal the frozen "
            f"{len(EXPECTED_EVALUATION_ARTIFACT_IDS)}-artifact ID set"
        )
    artifact_canonical_ids = [
        row["canonical_paper_id"].strip() for row in evaluation_artifacts
    ]
    for value in sorted(duplicates(artifact_canonical_ids)):
        errors.append(f"duplicate evaluation canonical_paper_id: {value}")
    for field in ("unit", "denominator", "metrics"):
        descriptions = [row[field].strip() for row in evaluation_artifacts]
        if any(not value for value in descriptions):
            errors.append(f"evaluation_artifacts.csv: blank {field} description")
        if len(set(descriptions)) != len(descriptions):
            errors.append(
                f"evaluation_artifacts.csv: {field} descriptions are not "
                "lexically unique in the frozen 43-artifact view"
            )

    measurement_ids = [
        row["artifact_id"].strip() for row in evaluation_measurement
    ]
    for value in sorted(duplicates(measurement_ids)):
        errors.append(f"duplicate evaluation measurement artifact_id: {value}")
    if (
        len(evaluation_measurement) != len(EXPECTED_EVALUATION_ARTIFACT_IDS)
        or set(measurement_ids) != EXPECTED_EVALUATION_ARTIFACT_IDS
        or set(measurement_ids) != artifact_id_set
    ):
        errors.append(
            "evaluation_measurement_coding.csv must exactly equal the frozen "
            "evaluation artifact ID set"
        )

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

    artifact_by_id = {
        row["artifact_id"].strip(): row for row in evaluation_artifacts
    }
    canonical_category_to_artifact_category = {
        "attack": "attacks",
        "defense": "defenses",
        "evaluation": "evaluations",
        "general": "general",
    }
    for line, row in enumerate(evaluation_artifacts, start=2):
        artifact_id = row["artifact_id"].strip()
        canonical_id = row["canonical_paper_id"].strip()
        category = row["primary_category"].strip()
        note = row["note_path"].strip()

        if not artifact_id:
            errors.append(
                f"evaluation_artifacts.csv:{line}: missing artifact_id"
            )
        canonical_paper = papers_by_id.get(canonical_id)
        if canonical_paper is None:
            errors.append(
                f"evaluation_artifacts.csv:{line}: unknown canonical_paper_id: "
                f"{canonical_id}"
            )
        else:
            if note != canonical_paper["note_path"].strip():
                errors.append(
                    f"evaluation_artifacts.csv:{line}: note_path does not match "
                    f"canonical paper: {note}"
                )
            if row["paper_title"].strip() != canonical_paper["title"].strip():
                errors.append(
                    f"evaluation_artifacts.csv:{line}: paper_title does not "
                    f"match canonical paper: {artifact_id}"
                )
            expected_category = canonical_category_to_artifact_category.get(
                canonical_paper["primary_category"].strip()
            )
            if category != expected_category:
                errors.append(
                    f"evaluation_artifacts.csv:{line}: primary_category does "
                    f"not match canonical paper: {artifact_id}"
                )
        if category not in {"attacks", "defenses", "evaluations", "general"}:
            errors.append(
                f"evaluation_artifacts.csv:{line}: invalid primary_category: "
                f"{category}"
            )
        canonical_export = final_by_id.get(canonical_id)
        if canonical_export is None:
            errors.append(
                f"evaluation_artifacts.csv:{line}: canonical paper absent from "
                f"all_relevant_papers.csv: {canonical_id}"
            )
        else:
            export_fields = {
                "paper_title": "title",
                "note_path": "note_path",
                "publication_status": "publication_status",
                "display_venue": "venue",
                "venue_type": "venue_type",
            }
            for artifact_field, export_field in export_fields.items():
                if row[artifact_field].strip() != canonical_export[
                    export_field
                ].strip():
                    errors.append(
                        f"evaluation_artifacts.csv:{line}: {artifact_field} "
                        f"does not match final export for {artifact_id}"
                    )
        if not row["source_version"].strip():
            errors.append(
                f"evaluation_artifacts.csv:{line}: blank source_version"
            )
        if not row["availability_url"].strip().startswith(
            ("https://", "http://")
        ):
            errors.append(
                f"evaluation_artifacts.csv:{line}: invalid availability_url"
            )
        note_path = ROOT / note
        if not note or not note_path.is_file():
            errors.append(
                f"evaluation_artifacts.csv:{line}: note does not exist: {note}"
            )

    measurement_by_id = {
        row["artifact_id"].strip(): row for row in evaluation_measurement
    }
    for line, row in enumerate(evaluation_measurement, start=2):
        artifact_id = row["artifact_id"].strip()
        primary = row["primary_eval_category"].strip()
        secondary = [
            value.strip()
            for value in row["secondary_eval_categories"].split(";")
            if value.strip()
        ]
        impact = row["impact_stage_max"].strip()
        counterfactual = row["interaction_counterfactual"].strip()
        availability = row["availability_kind"].strip()
        coding_status = row["coding_status"].strip()
        if primary not in EVALUATION_PRIMARY_CATEGORIES:
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: invalid primary "
                f"category: {primary}"
            )
        if len(secondary) != len(set(secondary)):
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: duplicate secondary "
                f"category: {artifact_id}"
            )
        for value in secondary:
            if value not in EVALUATION_PRIMARY_CATEGORIES:
                errors.append(
                    f"evaluation_measurement_coding.csv:{line}: invalid "
                    f"secondary category: {value}"
                )
            if value == primary:
                errors.append(
                    f"evaluation_measurement_coding.csv:{line}: primary category "
                    f"repeated as secondary: {artifact_id}"
                )
        if impact not in EVALUATION_IMPACT_STAGES:
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: invalid impact "
                f"stage: {impact}"
            )
        if counterfactual not in EVALUATION_COUNTERFACTUALS:
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: invalid "
                f"counterfactual: {counterfactual}"
            )
        if availability not in EVALUATION_AVAILABILITY_KINDS:
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: invalid "
                f"availability kind: {availability}"
            )
        if coding_status not in EVALUATION_CODING_STATUSES:
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: invalid coding "
                f"status: {coding_status}"
            )
        for field in ("coding_basis", "coding_status", "evidence_locator"):
            if not row[field].strip():
                errors.append(
                    f"evaluation_measurement_coding.csv:{line}: blank {field}"
                )
        artifact = artifact_by_id.get(artifact_id)
        if artifact and not row["evidence_locator"].strip().startswith(
            artifact["note_path"].strip() + "#"
        ):
            errors.append(
                f"evaluation_measurement_coding.csv:{line}: evidence locator "
                f"does not start with the canonical note path: {artifact_id}"
            )

    if any(
        row["impact_stage_max"].strip() == "S4_deployment"
        for row in evaluation_measurement
    ):
        errors.append(
            "the frozen 43-artifact view has no S4 deployment evidence; "
            "platform or sandbox cases cannot substitute for an exposure, "
            "control, incident, and recovery denominator"
        )

    a2a_measurement = measurement_by_id.get("artifact_a2asecbench")
    if a2a_measurement is not None:
        if (
            a2a_measurement["impact_stage_max"].strip()
            != "S3_executed_or_persistent"
        ):
            errors.append(
                "A2ASecBench impact_stage_max must preserve the S3 coding "
                "supported by executed protocol effects and persistent task state"
            )
        if a2a_measurement["availability_kind"].strip() != "code_and_data":
            errors.append(
                "A2ASecBench availability must preserve the evidenced "
                "code-and-data release"
            )
        if (
            a2a_measurement["interaction_counterfactual"].strip()
            != "component_or_attack_controls"
        ):
            errors.append(
                "A2ASecBench interaction counterfactual must preserve the "
                "attack-and-component-control coding; no interaction "
                "ablation is reported"
            )

    calbench_measurement = measurement_by_id.get("artifact_calbench")
    if calbench_measurement is not None:
        if (
            calbench_measurement["impact_stage_max"].strip()
            != "S3_executed_or_persistent"
        ):
            errors.append(
                "CalBench impact_stage_max must preserve the S3 coding "
                "supported by validated writes to mutable calendars"
            )
        if calbench_measurement["availability_kind"].strip() != "code_and_data":
            errors.append(
                "CalBench availability must preserve the reviewed "
                "code-and-data release"
            )
        if (
            calbench_measurement["interaction_counterfactual"].strip()
            != "component_or_attack_controls"
        ):
            errors.append(
                "CalBench interaction counterfactual must preserve the "
                "component-and-policy-control coding; no matched interaction "
                "or architecture ablation is reported"
            )

    joined_measurements = []
    for artifact in evaluation_artifacts:
        artifact_id = artifact["artifact_id"].strip()
        measurement = measurement_by_id.get(artifact_id)
        canonical_export = final_by_id.get(
            artifact["canonical_paper_id"].strip()
        )
        if measurement is not None and canonical_export is not None:
            joined_measurements.append((measurement, canonical_export))

    def complete_counts(
        values: list[str], domain: set[str] | None = None
    ) -> dict[str, int]:
        counts = Counter(values)
        keys = domain if domain is not None else set(counts)
        return {key: counts[key] for key in sorted(keys)}

    def count_joined(
        field: str, domain: set[str] | None = None
    ) -> dict[str, int]:
        return complete_counts(
            [
                measurement[field].strip()
                for measurement, _ in joined_measurements
            ],
            domain,
        )

    def count_export(
        field: str, domain: set[str] | None = None
    ) -> dict[str, int]:
        return complete_counts(
            [
                export[field].strip()
                for _, export in joined_measurements
            ],
            domain,
        )

    def sensitivity_summary(peer_reviewed: bool) -> dict[str, object]:
        selected = [
            (measurement, export)
            for measurement, export in joined_measurements
            if (export["publication_status"].strip() == "peer_reviewed")
            is peer_reviewed
        ]

        def count_selected(
            field: str, domain: set[str], from_export: bool = False
        ) -> dict[str, int]:
            return complete_counts(
                [
                    (export if from_export else measurement)[field].strip()
                    for measurement, export in selected
                ],
                domain,
            )

        return {
            "artifact_count": len(selected),
            "venue_type": count_selected(
                "venue_type",
                {"conference", "journal", "preprint", "workshop"},
                from_export=True,
            ),
            "primary_eval_category": count_selected(
                "primary_eval_category", EVALUATION_PRIMARY_CATEGORIES
            ),
            "impact_stage_max": count_selected(
                "impact_stage_max", EVALUATION_IMPACT_STAGES
            ),
            "interaction_counterfactual": count_selected(
                "interaction_counterfactual", EVALUATION_COUNTERFACTUALS
            ),
            "availability_kind": count_selected(
                "availability_kind", EVALUATION_AVAILABILITY_KINDS
            ),
        }

    expected_evaluation_summary = {
        "schema_version": 1,
        "artifact_count": len(joined_measurements),
        "source_files": [
            "corpus/sets/05_analysis_specific/evaluation_artifacts.csv",
            "corpus/sets/05_analysis_specific/evaluation_measurement_coding.csv",
            "corpus/final/all_relevant_papers.csv",
        ],
        "publication_status": count_export("publication_status"),
        "venue_type": count_export("venue_type"),
        "primary_eval_category": count_joined(
            "primary_eval_category", EVALUATION_PRIMARY_CATEGORIES
        ),
        "impact_stage_max": count_joined(
            "impact_stage_max", EVALUATION_IMPACT_STAGES
        ),
        "interaction_counterfactual": count_joined(
            "interaction_counterfactual", EVALUATION_COUNTERFACTUALS
        ),
        "availability_kind": count_joined(
            "availability_kind", EVALUATION_AVAILABILITY_KINDS
        ),
        "coding_status": count_joined(
            "coding_status", EVALUATION_CODING_STATUSES
        ),
        "peer_sensitivity": {
            "peer_reviewed": sensitivity_summary(True),
            "other": sensitivity_summary(False),
        },
    }
    peer_summary = expected_evaluation_summary["peer_sensitivity"][
        "peer_reviewed"
    ]
    other_summary = expected_evaluation_summary["peer_sensitivity"]["other"]
    if (
        expected_evaluation_summary["primary_eval_category"]
        != EXPECTED_EVALUATION_PRIMARY_COUNTS
        or peer_summary["artifact_count"] != 26
        or other_summary["artifact_count"] != 17
        or peer_summary["primary_eval_category"]
        != EXPECTED_EVALUATION_PEER_PRIMARY_COUNTS
        or other_summary["primary_eval_category"]
        != EXPECTED_EVALUATION_OTHER_PRIMARY_COUNTS
    ):
        errors.append(
            "evaluation measurement coding drifted from the frozen overall "
            "or peer-sensitivity category distribution"
        )
    canonical_evaluation_summary = (
        json.dumps(expected_evaluation_summary, indent=2, ensure_ascii=True)
        + "\n"
    )
    if evaluation_summary != expected_evaluation_summary:
        errors.append(
            "evaluation_measurement_summary.json does not exactly regenerate "
            "from the artifact coding and final export"
        )
    if evaluation_summary_text != canonical_evaluation_summary:
        errors.append(
            "evaluation_measurement_summary.json is not in deterministic "
            "canonical JSON form"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Corpus valid: {len(papers)} paper rows, {len(excluded)} exclusions, "
        f"{len(bib_keys)} BibTeX entries, "
        f"{len(evaluation_artifacts)} evaluation artifacts and "
        f"{len(evaluation_measurement)} measurement codings, "
        f"{len(post_cutoff)} post-cutoff watchlist records, and "
        f"{len(attack_screening)} search-screening entities; "
        f"{len(peer_first)} canonical broad-inclusion decisions, "
        f"{len(attack_canonical_bridge)} canonical attack bridges, "
        f"{len(targeted_attack_gap_search)} targeted gap decisions, and "
        f"{len(load_bearing_review)} load-bearing plus "
        f"{len(attack_review)} standard attack and "
        f"{len(cross_category_review)} cross-category reviews; "
        f"{len(universal_review)} papers in the universal checklist; "
        f"{len(final_all)} papers in the canonical final export; "
        f"{len(sok_papers)} works in the supporting SoK-related view; "
        f"{len(universal_source_corrections)} universal source-review "
        "corrections."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
