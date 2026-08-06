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

PAPER_FIELDS = [
    "paper_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "paper_type", "topic",
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
VERIFICATION_STATES = {
    "agent_unverified", "metadata_verified", "evidence_verified",
    "fully_reviewed",
}
INCLUSION_STATES = {"included", "excluded", "pending"}
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


def main() -> int:
    errors: list[str] = []
    try:
        papers = read_csv(PAPERS_CSV, PAPER_FIELDS)
        excluded = read_csv(EXCLUDED_CSV, EXCLUDED_FIELDS)
        evaluation_artifacts = read_csv(
            EVALUATION_ARTIFACTS, EVALUATION_ARTIFACT_FIELDS
        )
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    bib_keys = BIB_KEY.findall(REFERENCES.read_text(encoding="utf-8"))
    bib_key_set = set(bib_keys)
    for key in sorted(duplicates(bib_keys)):
        errors.append(f"duplicate BibTeX key: {key}")

    for field in ("paper_id", "bibtex_key", "note_path"):
        for value in sorted(duplicates([row[field].strip() for row in papers])):
            errors.append(f"duplicate {field}: {value}")

    excluded_ids = [row["paper_id"].strip() for row in excluded]
    for value in sorted(duplicates(excluded_ids)):
        errors.append(f"duplicate excluded paper_id: {value}")

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
        if status == "included":
            if not key or key not in bib_key_set:
                errors.append(f"papers.csv:{line}: missing BibTeX entry: {key}")
            note_path = ROOT / note
            if not note or not note_path.is_file():
                errors.append(f"papers.csv:{line}: note does not exist: {note}")
            elif not note_path.is_relative_to(ROOT / "papers"):
                errors.append(f"papers.csv:{line}: note is outside papers/: {note}")

    papers_by_id = {row["paper_id"].strip(): row for row in papers}
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
        f"{len(bib_keys)} BibTeX entries, and "
        f"{len(evaluation_artifacts)} evaluation artifacts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
