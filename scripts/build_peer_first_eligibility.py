#!/usr/bin/env python3
"""Build the peer-first evidence strata from the frozen systematic screen."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "corpus" / "attack_screening.csv"
PAPERS = ROOT / "corpus" / "papers.csv"
SNAPSHOT = ROOT / "corpus" / "peer_first_snapshot.json"
OUTPUT = ROOT / "corpus" / "peer_first_eligibility.csv"
SUMMARY = ROOT / "corpus" / "PEER_FIRST_CORPUS.md"
OVERRIDES = ROOT / "corpus" / "publication_status_overrides.csv"
CUTOFF = "2026-07-01"
THRESHOLD = 20
S2_FIELDS = (
    "title,citationCount,publicationDate,venue,publicationTypes,externalIds,url"
)

PREPRINT_VENUES = {
    "", "arxiv", "arxiv.org", "arxiv (cornell university)", "preprints.org",
    "zenodo (cern european organization for nuclear research)", "open mind",
    "underline science inc.", "volume 1",
}

CONFERENCE_PATTERNS = re.compile(
    r"conference|symposium|workshop|proceedings|annual meeting|acl|emnlp|"
    r"naacl|eacl|ijcnlp|neurips|nips|icml|iclr|aaai|aamas|the web conference|"
    r"usenix|ndss|asia.?ccs|computer vision and pattern recognition",
    re.I,
)
JOURNAL_PATTERNS = re.compile(
    r"transactions|journal|science china|complex & intelligent systems|"
    r"ai and ethics|frontiers in|ieee access|computing surveys|machine intelligence",
    re.I,
)
JOURNAL_DOI_PREFIXES = (
    "10.1007/s", "10.1016/", "10.1109/", "10.14569/",
)
CONFERENCE_DOI_PREFIXES = (
    "10.1145/", "10.1609/", "10.18653/", "10.24251/", "10.48448/",
    "10.5220/", "10.65109/",
)


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def included_rows() -> list[dict[str, str]]:
    with SCREENING.open(encoding="utf-8") as handle:
        return [
            row for row in csv.DictReader(handle)
            if row["final_decision"] == "include-primary-interaction-security"
        ]


def publication_overrides() -> dict[str, dict[str, str]]:
    with OVERRIDES.open(encoding="utf-8") as handle:
        return {row["record_id"]: row for row in csv.DictReader(handle)}


def canonical_papers() -> dict[str, dict[str, str]]:
    with PAPERS.open(encoding="utf-8") as handle:
        return {normalize_title(row["title"]): row for row in csv.DictReader(handle)}


def cleaned_venue(venue: str, doi: str, canonical: dict[str, str] | None) -> str:
    if canonical and canonical["venue"].lower() not in PREPRINT_VENUES:
        return canonical["venue"]
    if doi.lower().startswith("10.18653/v1/"):
        identifier = doi.lower().split("10.18653/v1/", 1)[1]
        series = identifier.split(".", 2)[1].replace("-", " ").upper()
        return series
    if doi.lower().startswith("10.1609/"):
        return "AAAI proceedings"
    if doi.lower().startswith("10.48448/") and venue.lower() in PREPRINT_VENUES:
        return "Formal proceedings (10.48448 DOI)"
    return venue


def query_id(row: dict[str, str]) -> str:
    record_id = row["record_id"]
    if record_id.startswith("doi:"):
        return "DOI:" + record_id.removeprefix("doi:")
    if row["arxiv_id"]:
        return "ARXIV:" + row["arxiv_id"]
    doi = row["doi"]
    if doi:
        return "DOI:" + doi
    return ""


def fetch_semantic_scholar(rows: list[dict[str, str]], snapshot_date: str) -> dict:
    identifiers = [query_id(row) for row in rows]
    requested = [identifier for identifier in identifiers if identifier]
    url = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=" + S2_FIELDS
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "multiagent-security-corpus/1.0",
    }
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    records: dict[str, dict | None] = {}
    for offset in range(0, len(requested), 50):
        batch = requested[offset:offset + 50]
        request = urllib.request.Request(
            url, data=json.dumps({"ids": batch}).encode(), headers=headers
        )
        for attempt in range(7):
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    results = json.load(response)
                break
            except urllib.error.HTTPError as error:
                if error.code != 429 or attempt == 6:
                    raise
                time.sleep(2 ** attempt)
        records.update(zip(batch, results))
        if offset + len(batch) < len(requested):
            time.sleep(1.1)
    return {
        "_meta": {
            "schema_version": 1,
            "publication_cutoff": CUTOFF,
            "citation_snapshot_date": snapshot_date,
            "citation_source": "Semantic Scholar Graph API",
            "citation_rule": f"citationCount > {THRESHOLD}",
            "requested_records": len(requested),
            "resolved_records": sum(result is not None for result in results),
        },
        "records": records,
    }


def archival_doi(row: dict[str, str], s2: dict | None) -> str:
    candidates = [row["record_id"].removeprefix("doi:"), row["doi"]]
    if s2:
        candidates.append((s2.get("externalIds") or {}).get("DOI", ""))
    for value in candidates:
        value = value.strip()
        if value and not value.lower().startswith("10.48550/arxiv."):
            return value
    return ""


def publication_status(row: dict[str, str], s2: dict | None) -> tuple[str, str, str, str]:
    """Return peer status, venue type, evidence kind, and evidence URL."""
    external = (s2 or {}).get("externalIds") or {}
    dblp = external.get("DBLP", "")
    venue = ((s2 or {}).get("venue") or row["venue"] or "").strip()
    doi = archival_doi(row, s2)

    if dblp and not dblp.lower().startswith("journals/corr/"):
        venue_type = "journal" if dblp.lower().startswith("journals/") else "conference"
        return "peer_reviewed", venue_type, "dblp_non_corr_record", f"https://dblp.org/rec/{dblp}"

    lower_venue = venue.lower()
    if doi.lower().startswith(CONFERENCE_DOI_PREFIXES):
        return "peer_reviewed", "conference", "archival_proceedings_doi", f"https://doi.org/{doi}"
    if doi.lower().startswith("10.1007/978-"):
        return "peer_reviewed", "conference", "archival_proceedings_doi", f"https://doi.org/{doi}"
    if lower_venue not in PREPRINT_VENUES:
        if JOURNAL_PATTERNS.search(venue) and doi.lower().startswith(JOURNAL_DOI_PREFIXES):
            return "peer_reviewed", "journal", "archival_doi_and_journal_venue", f"https://doi.org/{doi}"
        if CONFERENCE_PATTERNS.search(venue):
            evidence = f"https://doi.org/{doi}" if doi else (s2 or {}).get("url", "")
            return "peer_reviewed", "conference", "indexed_archival_venue", evidence

    return "non_peer_or_unverified", "", "no_archival_peer_evidence", (s2 or {}).get("url", "")


def build(rows: list[dict[str, str]], snapshot: dict) -> list[dict[str, str]]:
    output = []
    records = snapshot["records"]
    overrides = publication_overrides()
    canonical_records = canonical_papers()
    for row in rows:
        identifier = query_id(row)
        s2 = records.get(identifier) if identifier else None
        title_match = bool(
            s2 and normalize_title(s2.get("title", "")) == normalize_title(row["title"])
        )
        citations = s2.get("citationCount") if s2 and title_match else None
        status, venue_type, evidence_type, evidence_url = publication_status(
            row, s2 if title_match else None
        )
        override = overrides.get(row["record_id"])
        canonical = canonical_records.get(normalize_title(row["title"]))
        if override:
            status = override["publication_status"]
            venue_type = override["venue_type"]
            evidence_type = override["evidence_type"]
            evidence_url = override["evidence_url"]
        canonical_venue = cleaned_venue((
            override["canonical_venue"] if override
            else ((s2 or {}).get("venue") or row["venue"])
        ), override["canonical_doi"] if override else archival_doi(row, s2 if title_match else None), canonical)
        canonical_doi = (
            override["canonical_doi"] if override
            else ((canonical or {}).get("doi") or archival_doi(row, s2 if title_match else None))
        )
        if status == "peer_reviewed":
            stratum = f"peer_reviewed_{venue_type}"
        elif citations is None:
            stratum = "unresolved_citation_or_publication_status"
        elif citations > THRESHOLD:
            stratum = "influential_non_peer"
        else:
            stratum = "emerging_non_peer"
        output.append({
            "record_id": row["record_id"],
            "title": row["title"],
            "publication_date": row["publication_date"],
            "screened_venue": row["venue"],
            "canonical_venue": canonical_venue,
            "doi": row["doi"],
            "canonical_doi": canonical_doi,
            "arxiv_id": row["arxiv_id"],
            "scope_decision": row["final_decision"],
            "publication_status": status,
            "venue_type": venue_type,
            "publication_evidence_type": evidence_type,
            "publication_evidence_url": evidence_url,
            "publication_override": "yes" if override else "no",
            "semantic_scholar_id": (s2 or {}).get("paperId", "") if title_match else "",
            "semantic_scholar_title_match": "yes" if title_match else "no",
            "citations_semantic_scholar": "" if citations is None else str(citations),
            "citation_snapshot_date": snapshot["_meta"]["citation_snapshot_date"],
            "peer_first_stratum": stratum,
        })
    return output


def summary_text(rows: list[dict[str, str]], snapshot: dict) -> str:
    counts = Counter(row["peer_first_stratum"] for row in rows)
    venue_counts = Counter(
        row["canonical_venue"] or "Not reported"
        for row in rows if row["publication_status"] == "peer_reviewed"
    )
    lines = [
        "# Peer-First Corpus",
        "",
        "This ledger applies a publication-status layer to the 326 primary studies",
        "included by the frozen interaction-security screen. It does not alter the",
        "2,182-record retrieval denominator or resolve the 343 screening records that",
        "remain undecidable.",
        "",
        "## Rule",
        "",
        f"- Publication cutoff: `{CUTOFF}`",
        f"- Citation snapshot: `{snapshot['_meta']['citation_snapshot_date']}`",
        "- Citation source: Semantic Scholar Graph API",
        f"- Influential non-peer threshold: strictly more than `{THRESHOLD}` citations",
        "- Peer evidence: non-CoRR DBLP record, or indexed archival venue evidence",
        "- Preprint and published versions are one canonical work",
        "",
        "## Current Counts",
        "",
        "| Stratum | Works |",
        "| --- | ---: |",
    ]
    labels = (
        ("peer_reviewed_conference", "Peer-reviewed conference/proceedings"),
        ("peer_reviewed_journal", "Peer-reviewed journal"),
        ("influential_non_peer", "Non-peer-reviewed, citations > 20"),
        ("emerging_non_peer", "Non-peer-reviewed, citations <= 20"),
        ("unresolved_citation_or_publication_status", "Unresolved citation/publication status"),
    )
    lines.extend(f"| {label} | {counts[key]} |" for key, label in labels)
    lines.extend([
        f"| **Total scope-included works** | **{len(rows)}** |",
        "",
        "Only the two peer-reviewed strata and `influential_non_peer` form the",
        "peer-first core. Emerging preprints remain visible for trend analysis but",
        "must not enter corpus-level denominators. Unresolved records are not exclusions.",
        "",
        "## Peer-Reviewed Venues",
        "",
        "| Indexed venue | Works |",
        "| --- | ---: |",
    ])
    lines.extend(f"| {venue} | {count} |" for venue, count in venue_counts.most_common())
    lines.extend([
        "",
        "## Rebuild",
        "",
        "```bash",
        "python3 scripts/build_peer_first_eligibility.py --refresh",
        "python3 scripts/build_peer_first_eligibility.py --check",
        "```",
        "",
        "Citation counts are mutable. Any manuscript number must name the snapshot",
        "date. Publication evidence is deliberately conservative and requires manual",
        "resolution before an unresolved record can enter the peer-reviewed strata.",
        "",
    ])
    return "\n".join(lines)


def write(snapshot_date: str, refresh: bool) -> None:
    rows = included_rows()
    if refresh:
        snapshot = fetch_semantic_scholar(rows, snapshot_date)
        SNAPSHOT.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    output = build(rows, snapshot)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    SUMMARY.write_text(summary_text(output, snapshot), encoding="utf-8")
    print(Counter(row["peer_first_stratum"] for row in output))


def check() -> int:
    if not all(path.exists() for path in (SNAPSHOT, OUTPUT, SUMMARY)):
        print("FAIL: peer-first outputs are missing")
        return 1
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    expected = build(included_rows(), snapshot)
    with OUTPUT.open(encoding="utf-8") as handle:
        observed = list(csv.DictReader(handle))
    if observed != expected:
        print("FAIL: peer-first eligibility ledger is stale")
        return 1
    if SUMMARY.read_text(encoding="utf-8") != summary_text(expected, snapshot):
        print("FAIL: peer-first summary is stale")
        return 1
    if len(observed) != 326:
        print(f"FAIL: expected 326 included works, found {len(observed)}")
        return 1
    print("Peer-first corpus OK: 326 complete dispositions")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--snapshot-date", default=date.today().isoformat())
    args = parser.parse_args()
    if sum((args.refresh, args.write, args.check)) != 1:
        parser.error("choose exactly one of --refresh, --write, or --check")
    if args.check:
        return check()
    write(args.snapshot_date, args.refresh)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
