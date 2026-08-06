#!/usr/bin/env python3
"""Validate structural invariants of the literature corpus."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS_CSV = ROOT / "corpus" / "papers.csv"
EXCLUDED_CSV = ROOT / "corpus" / "excluded_papers.csv"
REFERENCES = ROOT / "corpus" / "references.bib"
EVALUATION_ARTIFACTS = ROOT / "corpus" / "evaluation_artifacts.csv"
POST_CUTOFF_CSV = ROOT / "corpus" / "post_cutoff_papers.csv"
POST_CUTOFF_REFERENCES = ROOT / "corpus" / "post_cutoff_references.bib"
ATTACK_SCREENING_CSV = ROOT / "corpus" / "attack_screening.csv"
ATTACK_CANONICAL_BRIDGE_CSV = ROOT / "corpus" / "attack_canonical_bridge.csv"
TARGETED_ATTACK_GAP_SEARCH_CSV = (
    ROOT / "corpus" / "targeted_attack_gap_search.csv"
)
LOAD_BEARING_REVIEW_CSV = ROOT / "corpus" / "load_bearing_review_queue.csv"

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
VERIFICATION_STATES = {
    "agent_unverified", "metadata_verified", "evidence_verified",
    "fully_reviewed",
}
INCLUSION_STATES = {"included", "excluded", "pending"}
PRIMARY_CATEGORIES = {"attack", "defense", "evaluation", "survey", "general"}
SCOPE_RELATIONS = {"core_security", "security_relevant", "adjacent"}
BIB_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)


def read_csv(path: Path, expected_fields: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
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
            "pending_human_review", "in_review", "completed"
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
        f"{len(attack_canonical_bridge)} canonical attack bridges, "
        f"{len(targeted_attack_gap_search)} targeted gap decisions, and "
        f"{len(load_bearing_review)} load-bearing reviews."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
