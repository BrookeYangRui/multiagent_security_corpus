#!/usr/bin/env python3
"""Import the authoritative 142-work package into the canonical corpus."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "corpus/source_packages/2026-07-01"
    / "multiagent_security_all_relevant_to_2026-07-01.csv"
)
SOK_SOURCE = (
    ROOT
    / "corpus/source_packages/2026-07-01"
    / "multiagent_security_strongly_related_soks_to_2026-07-01.csv"
)
PAPERS = ROOT / "corpus/papers.csv"
REFERENCES = ROOT / "corpus/references.bib"
SOK_PAPERS = ROOT / "sok_related/papers.csv"
SOK_REFERENCES = ROOT / "sok_related/references.bib"
ACCESS_DATE = "2026-08-07"

MANUAL_CATEGORIES = {
    "Chasing Moving Targets with Online Self-Play Reinforcement Learning for Safer Language Models": "defense",
    "Revisiting Multi-Agent Debate as Test-Time Scaling: A Systematic Study of Conditional Effectiveness": "evaluation",
    "SAFEFLOW: A Principled Protocol for Trustworthy and Transactional Autonomous Agent Systems": "defense",
    "SentinelAgent: Graph-based Anomaly Detection in Multi-Agent Systems": "defense",
    "The Sum Leaks More Than Its Parts: Compositional Privacy Risks and Mitigations in Multi-Agent Collaboration": "attack",
    "When Persuasion Overrides Truth in Multi-Agent LLM Debates: Introducing a Confidence-Weighted Persuasion Override Rate (CW-POR)": "attack",
    "WOLF: Werewolf-based Observations for LLM Deception and Falsehoods": "evaluation",
    "Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions": "evaluation",
    "Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs": "defense",
    "Taming Various Privilege Escalation in LLM-Based Agent Systems: A Mandatory Access Control Framework": "defense",
}

SURVEY_ROLES = {"survey", "survey_position", "perspective", "sok", "review"}
PAPER_FIELDS = [
    "paper_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "paper_type", "primary_category",
    "topic", "scope_relation", "application_domain", "multiagent_dependency",
    "attack", "defense", "system_failure", "evaluation", "discovery_source",
    "discovery_query", "accessed_version", "access_date", "note_path",
    "prepared_by", "verification_status", "inclusion_status",
    "exclusion_reason",
]
SOK_FIELDS = [
    "sok_id", "title", "authors", "year", "venue", "doi", "primary_url",
    "open_access_url", "bibtex_key", "work_type", "relation_level",
    "multiagent_security_centrality", "publication_status",
    "first_public_date", "cutoff_status", "note_path", "accessed_version",
    "access_date", "prepared_by", "verification_status",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def slug(value: str, limit: int = 64) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    return result[:limit].rstrip("_") or "paper"


def category_for(source: dict[str, str], old: dict[str, str] | None) -> str:
    if old:
        return old["primary_category"]
    if source["title"] in MANUAL_CATEGORIES:
        return MANUAL_CATEGORIES[source["title"]]
    role = source["primary_role"].casefold()
    if role.startswith("attack"):
        return "attack"
    if role.startswith("defense"):
        return "defense"
    if role in SURVEY_ROLES:
        return "survey"
    if role.startswith(
        ("evaluation", "benchmark", "assurance", "threat modeling", "security evaluation", "protocol; evaluation")
    ):
        return "evaluation"
    return "general"


def venue_folder(source: dict[str, str]) -> str:
    if source["publication_status"] == "non_peer_or_unverified":
        return "arxiv"
    venue = source["venue"].casefold()
    if "acm computing surveys" in venue:
        return "journals_acm_csur"
    if "ai open" in venue:
        return "journals_ai_open"
    if "npj" in venue:
        return "journals_npj_ai"
    if source["venue_type"] == "journal":
        return "journals_" + slug(source["venue"], 36)
    return slug(source["venue"], 36)


def note_path_for(
    source: dict[str, str], old: dict[str, str] | None, category: str
) -> str:
    if source.get("note_path"):
        return source["note_path"]
    if old:
        return old["note_path"]
    section = {
        "attack": "attacks",
        "defense": "defenses",
        "evaluation": "evaluations",
        "survey": "surveys",
        "general": "general",
    }[category]
    first_author = source["authors"].split(";")[0].strip().split()[-1]
    short_title = slug(source["title"], 48)
    return str(
        Path("papers")
        / section
        / venue_folder(source)
        / f"{source['year']}_{slug(first_author, 20)}_{short_title}.md"
    )


def normalized_scope(value: str) -> str:
    if value.startswith("core_security"):
        return "core_security"
    if value.startswith("security_relevant"):
        return "security_relevant"
    return "adjacent"


def split_bibtex(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    cursor = 0
    while True:
        match = re.search(r"(?m)^@\w+\s*\{\s*([^,\s]+)\s*,", text[cursor:])
        if not match:
            break
        start = cursor + match.start()
        key = match.group(1)
        brace = text.find("{", start)
        depth = 0
        end = brace
        while end < len(text):
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
                if depth == 0:
                    end += 1
                    break
            end += 1
        entries[key] = text[start:end].strip()
        cursor = end
    return entries


def generated_bibtex(source: dict[str, str], key: str) -> str:
    kind = {
        "conference": "inproceedings",
        "workshop": "inproceedings",
        "journal": "article",
        "preprint": "misc",
    }.get(source["venue_type"], "misc")
    venue_field = "journal" if kind == "article" else "booktitle"
    if kind == "misc":
        venue_field = "howpublished"
    fields = [
        ("title", source["title"]),
        ("author", source["authors"].replace(";", " and")),
        ("year", source["year"]),
        (venue_field, source["venue"] or "Preprint"),
    ]
    if source["doi"]:
        fields.append(("doi", source["doi"]))
    fields.append(("url", source["primary_url"]))
    body = ",\n".join(f"  {name} = {{{value}}}" for name, value in fields)
    return f"@{kind}{{{key},\n{body}\n}}"


def doi_from_url(value: str) -> str:
    match = re.search(r"doi\.org/(.+)$", value)
    return match.group(1) if match else ""


def note_text(source: dict[str, str], key: str, category: str) -> str:
    roles = "\n".join(
        f"- {part.strip()}" for part in source["primary_role"].split(";") if part.strip()
    )
    return f"""# {source['title']}

## Citation

Title: {source['title']}

Authors: {source['authors']}

Year: {source['year']}

Venue: {source['venue']}

DOI: {source['doi'] or 'Not reported'}

Primary URL: {source['primary_url']}

Open access URL: {source['open_access_url']}

BibTeX key: {key}

## Paper Type

{roles}

Primary category: {category}

Scope relation: {normalized_scope(source['scope_relation'])}

## Scope

### System Studied

Not yet extracted at claim level from the canonical full text.

### Multi-Agent Dependency

Imported corpus characterization, pending author signoff: {source['interaction_dependency']}

### Application Domain

Not reported in the imported record.

## Security Model

### Protected Assets

Not yet extracted.

### Threat Actor

Not yet extracted.

### Trusted Components

Not yet extracted.

### Attacker Capabilities

Not yet extracted.

### Security Assumptions

Not yet extracted.

## Main Contribution

Imported corpus interpretation: {source['security_relevance']}

## Attack or Failure

### Attack Surface

Not yet extracted.

### Attack Mechanism

Not yet extracted.

### System-Level Failure

Not yet extracted.

### Security Consequence

Not yet extracted.

## Defense

### Defense Mechanism

Not yet extracted.

### Intervention Point

Not yet extracted.

### Required Observability

Not yet extracted.

### Assumptions

Not yet extracted.

### Limitations

The imported record has not received repository claim-level verification.

## Evaluation

### Evaluated Systems

Not yet extracted.

### Agent Configuration

Not yet extracted.

### Dataset or Environment

Not yet extracted.

### Baselines

Not yet extracted.

### Metrics

Not yet extracted.

### Main Results

Not yet extracted.

## Relation to Existing Work

### Papers Compared by the Authors

Not yet extracted.

### Claimed Research Gap

Not yet extracted.

### Closest Related Work

Not yet extracted.

### Difference From Prior Work

Not yet extracted.

## Relevance to Our SoK

### Included Concepts

Pending claim-level extraction.

### Taxonomy Implications

Do not infer a fixed taxonomy from this imported placement.

### Supported Research Questions

Pending claim-level extraction.

### Important Limitations

This note preserves imported metadata and scope coding only.

## Evidence

| Claim | Claim status | Source type | Section | Page | Figure or table | Evidence |
| ----- | ------------ | ----------- | ------- | ---: | --------------- | -------- |
| Imported scope and placement | Corpus interpretation | Paper | Unclear | | | {source['evidence_locator']} |

## Provenance

### Discovery Source

{source['discovery_source']}

### Discovery Query

Not reported in the imported record.

### Accessed Version

Canonical source linked by the authoritative 142-work package; exact version requires claim-level verification.

### Access Date

{ACCESS_DATE}

### Prepared By

Automated organization from the authoritative 142-work package.

### Verification Status

agent_unverified

### Last Updated

{ACCESS_DATE}
"""


def main() -> None:
    source_rows = read_csv(SOURCE)
    old_rows = read_csv(PAPERS)
    old_by_title = {normalized_title(row["title"]): row for row in old_rows}
    old_bib = split_bibtex(REFERENCES.read_text(encoding="utf-8"))

    output_rows: list[dict[str, str]] = []
    bib_entries: list[str] = []
    created_notes = 0
    for source in source_rows:
        old = old_by_title.get(normalized_title(source["title"]))
        category = category_for(source, old)
        note_path = note_path_for(source, old, category)
        key = old["bibtex_key"] if old else source["paper_id"]
        scope = normalized_scope(source["scope_relation"])

        if old:
            row = dict(old)
            row.update(
                {
                    "title": source["title"],
                    "authors": source["authors"],
                    "year": source["year"],
                    "venue": source["venue"],
                    "doi": source["doi"],
                    "primary_url": source["primary_url"],
                    "open_access_url": source["open_access_url"],
                    "paper_type": source["primary_role"].replace("_", " "),
                    "primary_category": category,
                    "scope_relation": scope,
                    "multiagent_dependency": source["interaction_dependency"],
                    "discovery_source": source["discovery_source"],
                    "note_path": note_path,
                    "verification_status": "agent_unverified",
                    "inclusion_status": "included",
                    "exclusion_reason": "",
                }
            )
        else:
            row = {
                "paper_id": source["paper_id"],
                "title": source["title"],
                "authors": source["authors"],
                "year": source["year"],
                "venue": source["venue"],
                "doi": source["doi"],
                "primary_url": source["primary_url"],
                "open_access_url": source["open_access_url"],
                "bibtex_key": key,
                "paper_type": source["primary_role"].replace("_", " "),
                "primary_category": category,
                "topic": source["primary_role"].replace("_", " "),
                "scope_relation": scope,
                "application_domain": "Not reported",
                "multiagent_dependency": source["interaction_dependency"],
                "attack": "Not reported",
                "defense": "Not reported",
                "system_failure": source["security_relevance"],
                "evaluation": "Not reported",
                "discovery_source": source["discovery_source"],
                "discovery_query": "Not reported",
                "accessed_version": (
                    "published version linked in authoritative package"
                    if source["publication_status"] == "peer_reviewed"
                    else "pre-cutoff version linked in authoritative package"
                ),
                "access_date": ACCESS_DATE,
                "note_path": note_path,
                "prepared_by": "automated organization from authoritative 142-work package",
                "verification_status": "agent_unverified",
                "inclusion_status": "included",
                "exclusion_reason": "",
            }
        output_rows.append(row)

        if key in old_bib:
            bib_entries.append(old_bib[key])
        else:
            bib_entries.append(generated_bibtex(source, key))

        note = ROOT / note_path
        if not note.exists():
            note.parent.mkdir(parents=True, exist_ok=True)
            note.write_text(note_text(source, key, category), encoding="utf-8")
            created_notes += 1

    with PAPERS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAPER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)
    REFERENCES.write_text("\n\n".join(bib_entries) + "\n", encoding="utf-8")

    papers_by_title = {normalized_title(row["title"]): row for row in output_rows}
    sok_rows = []
    sok_bib = []
    for source in read_csv(SOK_SOURCE):
        paper = papers_by_title.get(normalized_title(source["title"]))
        key = paper["bibtex_key"] if paper else source["record_id"]
        if paper:
            note_path = paper["note_path"]
            doi = paper["doi"]
            open_url = paper["open_access_url"]
        else:
            doi = doi_from_url(source["primary_url"])
            fake = {
                "authors": source["authors"],
                "year": source["year"],
                "title": source["title"],
                "publication_status": (
                    "peer_reviewed" if source["peer_reviewed"] == "yes"
                    else "non_peer_or_unverified"
                ),
                "venue": source["venue_or_status"],
                "venue_type": "preprint",
            }
            note_path = note_path_for(fake, None, "survey")
            open_url = source["primary_url"]
            note = ROOT / note_path
            if not note.exists():
                note.parent.mkdir(parents=True, exist_ok=True)
                note_source = {
                    "title": source["title"],
                    "authors": source["authors"],
                    "year": source["year"],
                    "venue": source["venue_or_status"],
                    "doi": doi,
                    "primary_url": source["primary_url"],
                    "open_access_url": open_url,
                    "primary_role": "survey; SoK-related comparator",
                    "scope_relation": "security_relevant",
                    "interaction_dependency": source["mas_security_scope"],
                    "security_relevance": source["why_strongly_related"],
                    "evidence_locator": source["evidence_basis"],
                    "discovery_source": "authoritative 142-work source package",
                }
                note.write_text(note_text(note_source, key, "survey"), encoding="utf-8")
                created_notes += 1

        sok_rows.append({
            "sok_id": source["record_id"],
            "title": source["title"],
            "authors": source["authors"],
            "year": source["year"],
            "venue": source["venue_or_status"],
            "doi": doi,
            "primary_url": source["primary_url"],
            "open_access_url": open_url,
            "bibtex_key": key,
            "work_type": "SoK-related survey, review, perspective, or comparator",
            "relation_level": (
                "direct" if source["relation_level"].startswith("direct")
                else "strongly_related"
            ),
            "multiagent_security_centrality": source["why_strongly_related"],
            "publication_status": (
                "peer_reviewed" if source["peer_reviewed"] == "yes"
                else "non_peer_or_unverified"
            ),
            "first_public_date": "Not reported",
            "cutoff_status": "pre_cutoff",
            "note_path": note_path,
            "accessed_version": source["venue_or_status"],
            "access_date": ACCESS_DATE,
            "prepared_by": "imported authoritative 142-work source package",
            "verification_status": "agent_unverified",
        })
        if key in old_bib:
            sok_bib.append(old_bib[key])
        else:
            bib_source = {
                "title": source["title"],
                "authors": source["authors"],
                "year": source["year"],
                "venue": source["venue_or_status"],
                "venue_type": "article" if source["peer_reviewed"] == "yes" else "preprint",
                "doi": doi,
                "primary_url": source["primary_url"],
            }
            sok_bib.append(generated_bibtex(bib_source, key))

    with SOK_PAPERS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOK_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(sok_rows)
    SOK_REFERENCES.write_text("\n\n".join(sok_bib) + "\n", encoding="utf-8")
    print(
        f"Imported {len(output_rows)} canonical works and {len(sok_rows)} "
        f"SoK-related records; created {created_notes} notes."
    )


if __name__ == "__main__":
    main()
