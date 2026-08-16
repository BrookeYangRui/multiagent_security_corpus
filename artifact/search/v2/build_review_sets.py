#!/usr/bin/env python3
"""Build the persistent three-set review view for the MAS security corpus.

The builder reconciles search, broad-screen, peer-first, venue, targeted-gap,
canonical, and exclusion routes at work level. Route membership is evidence,
not a final classification. Explicit review decisions live in a separate ledger
and survive every rebuild.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import hashlib
import json
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "artifact" / "search" / "v2"
CUTOFF = "2026-07-01"

SEARCH = ROOT / "corpus" / "sets" / "01_search_catalog" / "search_catalog.csv"
BROAD = ROOT / "corpus" / "sets" / "02_broad_included" / "broad_included.csv"
TAXONOMY = ROOT / "corpus" / "sets" / "03_taxonomy_eligible" / "taxonomy_candidates.csv"
PAPERS = ROOT / "corpus" / "papers.csv"
CANONICAL = ROOT / "corpus" / "final" / "all_relevant_papers.csv"
REVIEWS = ROOT / "reviews" / "universal" / "active_source_review.csv"
STRUCTURED_EXCLUSIONS = ROOT / "corpus" / "sets" / "01_search_catalog" / "structured_exclusions.csv"
TARGETED_GAP = ROOT / "corpus" / "sets" / "01_search_catalog" / "targeted_gap_search.csv"
IDENTIFIER_OVERRIDES = HERE / "identifier_alias_overrides.csv"

QUEUE = HERE / "review_candidate_queue.csv"
ROUTE_QUEUE = HERE / "review_candidate_routes.csv"
LEDGER = HERE / "review_decision_ledger.csv"
PRIMARY = HERE / "review_primary.csv"
SECONDARY = HERE / "review_secondary.csv"
EXCLUDE = HERE / "review_exclude.csv"
PENDING = HERE / "review_pending.csv"
ALIASES = HERE / "review_identifier_aliases.csv"
SUMMARY = HERE / "review_set_summary.csv"
MANIFEST = HERE / "review_set_manifest.json"

FINAL_DECISIONS = {"primary", "secondary", "exclude"}
ALL_DECISIONS = FINAL_DECISIONS | {"pending"}

DOI_RE = re.compile(r"(?:https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/[^\s\"<>]+)", re.I)
ARXIV_RE = re.compile(r"(?:arxiv:|arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?", re.I)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text(value: object) -> str:
    return "" if value is None else str(value).strip()


def norm_title(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text(value).casefold()).split())


def compact_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text(value).casefold())


def norm_doi(value: str) -> str:
    match = DOI_RE.search(text(value))
    if not match:
        return ""
    value = match.group(1).rstrip(".,;)]}").casefold()
    if value.startswith("10.48550/arxiv."):
        return ""
    return value


def norm_arxiv(value: str) -> str:
    match = ARXIV_RE.search(text(value))
    return match.group(1).casefold() if match else ""


def first(*values: str) -> str:
    for value in values:
        if text(value):
            return text(value)
    return ""


def year_from(*values: str) -> str:
    for value in values:
        match = re.search(r"(?:19|20)\d{2}", text(value))
        if match:
            return match.group(0)
    return ""


def slug(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", text(value).casefold()).strip("_")
    return result or "unknown"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


@dataclasses.dataclass
class RouteRow:
    route_id: str
    route_type: str
    title: str
    canonical_paper_id: str = ""
    publication_date: str = ""
    year: str = ""
    venue: str = ""
    doi: str = ""
    arxiv_id: str = ""
    primary_url: str = ""
    source_decision: str = ""
    source_scope: str = ""
    source_status: str = ""
    source_reason: str = ""
    source_path: str = ""
    route_strength: int = 0

    def normalized(self) -> "RouteRow":
        self.title = text(self.title)
        self.canonical_paper_id = text(self.canonical_paper_id)
        self.publication_date = text(self.publication_date)
        self.year = year_from(self.year, self.publication_date)
        self.venue = text(self.venue)
        self.doi = norm_doi(self.doi)
        self.arxiv_id = norm_arxiv(first(self.arxiv_id, self.primary_url))
        self.primary_url = text(self.primary_url)
        return self


@dataclasses.dataclass(frozen=True)
class Proposal:
    decision: str
    strength: int
    source: str
    reason: str
    requires_signoff: str = "yes"


def load_overrides() -> tuple[dict[tuple[str, str], dict[str, str]], list[dict[str, str]]]:
    mapping: dict[tuple[str, str], dict[str, str]] = {}
    rows = read_csv(IDENTIFIER_OVERRIDES)
    for row in rows:
        alias_type = text(row.get("alias_type")).casefold()
        alias_value = text(row.get("alias_value"))
        if alias_type == "doi":
            alias_value = norm_doi(alias_value)
        elif alias_type == "arxiv":
            alias_value = norm_arxiv(alias_value)
        elif alias_type == "title":
            alias_value = norm_title(alias_value)
        else:
            raise ValueError(f"unknown alias type {alias_type!r}")
        if not alias_value:
            raise ValueError(f"empty normalized alias in {IDENTIFIER_OVERRIDES}: {row}")
        key = (alias_type, alias_value)
        if key in mapping:
            raise ValueError(f"duplicate identifier override {key}")
        mapping[key] = row
    return mapping, rows


def apply_override(route: RouteRow, overrides: dict[tuple[str, str], dict[str, str]]) -> RouteRow:
    keys = []
    if route.doi:
        keys.append(("doi", route.doi))
    if route.arxiv_id:
        keys.append(("arxiv", route.arxiv_id))
    if route.title:
        keys.append(("title", norm_title(route.title)))
    matches = [overrides[key] for key in keys if key in overrides]
    if not matches:
        return route
    canonical_ids = {
        (
            norm_doi(row.get("canonical_doi", "")),
            norm_arxiv(row.get("canonical_arxiv_id", "")),
            norm_title(row.get("canonical_title", "")),
        )
        for row in matches
    }
    if len(canonical_ids) != 1:
        raise ValueError(f"conflicting identifier overrides for route {route.route_id}: {matches}")
    row = matches[0]
    route.doi = first(norm_doi(row.get("canonical_doi", "")), route.doi)
    route.arxiv_id = first(norm_arxiv(row.get("canonical_arxiv_id", "")), route.arxiv_id)
    route.title = first(row.get("canonical_title", ""), route.title)
    route.primary_url = first(row.get("authoritative_url", ""), route.primary_url)
    return route


def build_routes() -> tuple[list[RouteRow], dict[str, int]]:
    routes: list[RouteRow] = []
    counts: Counter[str] = Counter()

    def add(route: RouteRow) -> None:
        route.normalized()
        if not route.title:
            return
        routes.append(route)
        counts[route.route_type] += 1

    search_rows = read_csv(SEARCH)
    for row in search_rows:
        add(
            RouteRow(
                route_id=f"search:{row['record_id']}",
                route_type="search",
                title=row["title"],
                canonical_paper_id=row.get("canonical_paper_id", ""),
                publication_date=row.get("publication_date", ""),
                venue=row.get("venue", ""),
                doi=row.get("doi", ""),
                arxiv_id=row.get("arxiv_id", ""),
                source_decision=row.get("final_decision", ""),
                source_scope=row.get("scope_relation", ""),
                source_status=row.get("attack_decision", ""),
                source_reason=row.get("screening_note", ""),
                source_path=str(SEARCH.relative_to(ROOT)),
                route_strength=50,
            )
        )

    broad_rows = read_csv(BROAD)
    # The frozen targeted route contains every cutoff-eligible broad-screen
    # work except the seven records explicitly reviewed as adjacent. Two
    # security-relevant failure/defense studies also carry the historical
    # gate label ``adjacent_not_core``; excluding by that label would drop
    # them incorrectly and produce 316 rather than the recorded 318.
    adjacent_record_ids = {
        row["record_id"]
        for row in read_csv(TAXONOMY)
        if text(row.get("recommended_scope")).casefold() == "adjacent"
    }
    targeted_rows = [row for row in broad_rows if row["record_id"] not in adjacent_record_ids]
    if len(targeted_rows) != 318:
        raise ValueError(
            f"targeted route reconstruction expected 318 cutoff candidates, got {len(targeted_rows)}; "
            f"broad={len(broad_rows)} adjacent={len(adjacent_record_ids)}"
        )

    for row in broad_rows:
        common = dict(
            title=row["title"],
            publication_date=row.get("publication_date", ""),
            venue=first(row.get("canonical_venue", ""), row.get("screened_venue", "")),
            doi=first(row.get("canonical_doi", ""), row.get("doi", "")),
            arxiv_id=row.get("arxiv_id", ""),
            primary_url=row.get("publication_evidence_url", ""),
            source_decision=row.get("scope_decision", ""),
            source_scope="broad_scope_included",
            source_status=row.get("peer_first_stratum", ""),
            source_reason="Frozen broad-screen inclusion.",
            source_path=str(BROAD.relative_to(ROOT)),
        )
        add(RouteRow(route_id=f"broad:{row['record_id']}", route_type="broad", route_strength=60, **common))
        if row["record_id"] not in adjacent_record_ids:
            add(RouteRow(route_id=f"targeted:{row['record_id']}", route_type="targeted", route_strength=60, **common))
        if row.get("publication_status") == "peer_reviewed":
            venue_id = first(row.get("canonical_doi", ""), row.get("doi", ""), row.get("record_id", ""))
            # The ACL Anthology route is authoritative for this known metadata alias.
            if row.get("arxiv_id") == "2508.15809":
                venue_id = "2025.ijcnlp-long.53"
                common = dict(common)
                common["doi"] = "10.18653/v1/2025.ijcnlp-long.53"
                common["primary_url"] = "https://aclanthology.org/2025.ijcnlp-long.53/"
            add(
                RouteRow(
                    route_id=f"venue:{slug(common['venue'])}:{slug(venue_id)}",
                    route_type="venue",
                    route_strength=55,
                    **common,
                )
            )

    for row in read_csv(TAXONOMY):
        add(
            RouteRow(
                route_id=f"peerfirst:{row['record_id']}",
                route_type="peerfirst",
                title=row["title"],
                canonical_paper_id=row.get("canonical_paper_id", ""),
                publication_date=row.get("publication_date", ""),
                venue=row.get("venue", ""),
                doi=row.get("doi", ""),
                arxiv_id=row.get("arxiv_id", ""),
                source_decision=row.get("gate_decision", ""),
                source_scope=row.get("recommended_scope", ""),
                source_status=row.get("source_review_status", ""),
                source_reason=row.get("decision_reason", ""),
                source_path=str(TAXONOMY.relative_to(ROOT)),
                route_strength=75,
            )
        )

    papers_by_id = {row["paper_id"]: row for row in read_csv(PAPERS)}
    reviews_by_id = {row["paper_id"]: row for row in read_csv(REVIEWS)}
    for row in read_csv(CANONICAL):
        review = reviews_by_id.get(row["paper_id"], {})
        paper = papers_by_id.get(row["paper_id"], {})
        add(
            RouteRow(
                route_id=f"canonical:{row['paper_id']}",
                route_type="canonical",
                title=row["title"],
                canonical_paper_id=row["paper_id"],
                publication_date=first(row.get("year", ""), paper.get("year", "")),
                year=row.get("year", ""),
                venue=row.get("venue", ""),
                doi=row.get("doi", ""),
                primary_url=first(row.get("primary_url", ""), row.get("open_access_url", ""), review.get("source_url", "")),
                source_decision=review.get("review_outcome", ""),
                source_scope=first(review.get("recommended_scope", ""), row.get("scope_relation", "")),
                source_status=review.get("review_status", ""),
                source_reason=first(review.get("scope_rationale", ""), row.get("security_relevance", "")),
                source_path=str(CANONICAL.relative_to(ROOT)),
                route_strength=100,
            )
        )

    for row in read_csv(STRUCTURED_EXCLUSIONS):
        add(
            RouteRow(
                route_id=f"structured-exclude:{row['paper_id']}",
                route_type="structured_exclude",
                title=row["title"],
                canonical_paper_id=row.get("canonical_paper_id", ""),
                year=row.get("year", ""),
                primary_url=row.get("primary_url", ""),
                source_decision="exclude" if not row.get("canonical_paper_id") else "version_merge",
                source_scope="exclude" if not row.get("canonical_paper_id") else "alias_only",
                source_status=row.get("screening_stage", ""),
                source_reason=row.get("exclusion_reason", ""),
                source_path=str(STRUCTURED_EXCLUSIONS.relative_to(ROOT)),
                route_strength=95,
            )
        )

    for index, row in enumerate(read_csv(TARGETED_GAP), start=1):
        if not text(row.get("candidate_title")):
            continue
        route_suffix = first(row.get("canonical_paper_id", ""), compact_title(row["candidate_title"]), str(index))
        add(
            RouteRow(
                route_id=f"targeted-gap:{slug(row.get('search_family', ''))}:{route_suffix}",
                route_type="targeted_gap",
                title=row["candidate_title"],
                canonical_paper_id=row.get("canonical_paper_id", ""),
                venue=row.get("publication_status", ""),
                primary_url=row.get("primary_url", ""),
                source_decision=row.get("decision", ""),
                source_scope="",
                source_status=row.get("publication_status", ""),
                source_reason=row.get("reason", ""),
                source_path=str(TARGETED_GAP.relative_to(ROOT)),
                route_strength=70,
            )
        )

    return routes, dict(counts)


def deduplicate(routes: list[RouteRow], overrides: dict[tuple[str, str], dict[str, str]]) -> tuple[list[list[RouteRow]], list[dict[str, str]]]:
    for route in routes:
        apply_override(route, overrides)
        route.normalized()

    uf = UnionFind(len(routes))
    indices: dict[tuple[str, str], int] = {}
    alias_rows: list[dict[str, str]] = []

    for index, route in enumerate(routes):
        keys: list[tuple[str, str]] = []
        if route.canonical_paper_id:
            keys.append(("paper_id", route.canonical_paper_id.casefold()))
        if route.arxiv_id:
            keys.append(("arxiv", route.arxiv_id))
        if route.doi:
            keys.append(("doi", route.doi))
        if route.title:
            keys.append(("title", norm_title(route.title)))
        for key in keys:
            previous = indices.get(key)
            if previous is None:
                indices[key] = index
            else:
                uf.union(index, previous)

    groups_map: dict[int, list[RouteRow]] = defaultdict(list)
    for index, route in enumerate(routes):
        groups_map[uf.find(index)].append(route)

    groups = list(groups_map.values())
    # Fail loudly if a public identifier still binds visibly different titles.
    for group in groups:
        titles = {norm_title(route.title) for route in group if route.title}
        arxiv_ids = {route.arxiv_id for route in group if route.arxiv_id}
        dois = {route.doi for route in group if route.doi}
        if (arxiv_ids or dois) and len(titles) > 1:
            compact = {compact_title(title) for title in titles}
            contained = all(any(a in b or b in a for b in compact if b != a) for a in compact) if len(compact) > 1 else True
            if not contained:
                # Multiple route titles may be legitimate version-title changes only when a canonical paper ID binds them.
                canonical_ids = {route.canonical_paper_id for route in group if route.canonical_paper_id}
                if not canonical_ids:
                    raise ValueError(
                        "public identifier spans multiple review rows: "
                        f"arxiv={sorted(arxiv_ids)} doi={sorted(dois)} routes={[r.route_id for r in group]} "
                        f"titles={sorted(titles)}"
                    )

        for route in group:
            if route.doi:
                alias_rows.append({"identifier_type": "doi", "identifier": route.doi, "route_id": route.route_id})
            if route.arxiv_id:
                alias_rows.append({"identifier_type": "arxiv", "identifier": route.arxiv_id, "route_id": route.route_id})

    return groups, alias_rows


def scope_class(value: str) -> str:
    value = text(value).casefold()
    if value.startswith("core_security"):
        return "primary"
    if value.startswith("security_relevant") or value.startswith("adjacent"):
        return "secondary"
    return ""


def proposals_for(group: list[RouteRow]) -> list[Proposal]:
    proposals: list[Proposal] = []
    for route in group:
        scope_decision = scope_class(route.source_scope)
        if route.route_type == "canonical" and scope_decision:
            proposals.append(
                Proposal(scope_decision, 100, route.route_id, route.source_reason or f"Canonical scope is {route.source_scope}.", "yes")
            )
            continue

        if route.route_type == "peerfirst":
            if route.source_decision == "provisional_pass_author_signoff_required" and scope_decision == "primary":
                proposals.append(Proposal("primary", 90, route.route_id, route.source_reason, "yes"))
            elif route.source_decision in {"contextual_not_strict_core", "adjacent_not_core"}:
                proposals.append(Proposal("secondary", 90, route.route_id, route.source_reason, "yes"))
            continue

        if route.route_type == "structured_exclude" and route.source_decision == "exclude":
            proposals.append(Proposal("exclude", 95, route.route_id, route.source_reason, "yes"))
            continue

        if route.route_type == "search":
            decision = route.source_decision
            if decision == "include-primary-interaction-security":
                proposals.append(Proposal("primary", 60, route.route_id, "Full-text interaction-security screen included the work.", "yes"))
            elif decision == "exclude-secondary":
                proposals.append(Proposal("secondary", 55, route.route_id, route.source_reason or decision, "yes"))
            elif decision.startswith("exclude-"):
                proposals.append(Proposal("exclude", 55, route.route_id, route.source_reason or decision, "yes"))
            continue

        if route.route_type == "targeted_gap":
            decision = route.source_decision
            if decision.startswith("excluded_"):
                proposals.append(Proposal("exclude", 70, route.route_id, route.source_reason, "yes"))
            elif decision == "included_security_relevant":
                proposals.append(Proposal("secondary", 70, route.route_id, route.source_reason, "yes"))
            # included/existing/evaluation/defense rows are route evidence only; the canonical or search review decides.
    return proposals


def choose_seed(proposals: list[Proposal]) -> tuple[str, str, str, str, str]:
    if not proposals:
        return "pending", "no_explicit_decision", "No explicit source-level classification is available.", "0", "yes"
    max_strength = max(p.strength for p in proposals)
    strongest = [p for p in proposals if p.strength == max_strength]
    decisions = {p.decision for p in strongest}
    if len(decisions) > 1:
        sources = ";".join(sorted(p.source for p in strongest))
        reason = "Conflicting equally strong decisions: " + " | ".join(f"{p.decision}: {p.reason}" for p in strongest)
        return "pending", f"conflict:{sources}", reason, str(max_strength), "yes"
    decision = strongest[0].decision
    same = [p for p in strongest if p.decision == decision]
    source = ";".join(sorted({p.source for p in same}))
    reason = " | ".join(dict.fromkeys(p.reason for p in same if p.reason))
    return decision, source, reason, str(max_strength), "yes" if any(p.requires_signoff == "yes" for p in same) else "no"


def canonical_group_row(group: list[RouteRow]) -> dict[str, str]:
    ranked = sorted(group, key=lambda r: (r.route_strength, bool(r.canonical_paper_id), bool(r.doi), bool(r.arxiv_id)), reverse=True)
    best = ranked[0]
    paper_ids = sorted({r.canonical_paper_id for r in group if r.canonical_paper_id})
    if len(paper_ids) > 1:
        raise ValueError(f"group contains multiple canonical paper IDs: {paper_ids} routes={[r.route_id for r in group]}")
    paper_id = paper_ids[0] if paper_ids else ""
    dois = [r.doi for r in ranked if r.doi]
    arxivs = [r.arxiv_id for r in ranked if r.arxiv_id]
    titles = [r.title for r in ranked if r.title]
    urls = [r.primary_url for r in ranked if r.primary_url]
    dates = [r.publication_date for r in ranked if r.publication_date]
    years = [r.year for r in ranked if r.year]
    venues = [r.venue for r in ranked if r.venue]

    # Prefer publisher DOI over repository or miscellaneous DOI aliases.
    doi = next((d for d in dois if d.startswith("10.18653/v1/")), "") or next((d for d in dois if not d.startswith("10.48448/")), "") or (dois[0] if dois else "")
    arxiv_id = arxivs[0] if arxivs else ""
    title = titles[0]
    canonical_key = paper_id or (f"arxiv:{arxiv_id}" if arxiv_id else "") or (f"doi:{doi}" if doi else "") or f"title:{hashlib.sha1(norm_title(title).encode()).hexdigest()[:16]}"

    seed_decision, seed_source, seed_reason, seed_strength, signoff = choose_seed(proposals_for(group))
    return {
        "work_key": canonical_key,
        "canonical_paper_id": paper_id,
        "title": title,
        "normalized_title": norm_title(title),
        "publication_date": dates[0] if dates else "",
        "year": years[0] if years else year_from(dates[0] if dates else ""),
        "venue": venues[0] if venues else "",
        "doi": doi,
        "arxiv_id": arxiv_id,
        "primary_url": urls[0] if urls else "",
        "route_types": ";".join(sorted({r.route_type for r in group})),
        "route_ids": ";".join(sorted(r.route_id for r in group)),
        "route_count": str(len(group)),
        "source_decisions": ";".join(sorted({r.source_decision for r in group if r.source_decision})),
        "source_scopes": ";".join(sorted({r.source_scope for r in group if r.source_scope})),
        "source_statuses": ";".join(sorted({r.source_status for r in group if r.source_status})),
        "source_paths": ";".join(sorted({r.source_path for r in group if r.source_path})),
        "seed_decision": seed_decision,
        "seed_decision_source": seed_source,
        "seed_decision_reason": seed_reason,
        "seed_decision_strength": seed_strength,
        "human_signoff_required": signoff,
    }


LEDGER_FIELDS = [
    "work_key", "canonical_paper_id", "title", "doi", "arxiv_id", "decision",
    "decision_source", "decision_strength", "rationale", "reviewer", "reviewed_at",
    "locked", "human_signoff_required", "previous_work_keys", "notes",
]

ROUTE_QUEUE_FIELDS = [
    "route_id", "route_type", "work_key", "canonical_paper_id", "route_title",
    "canonical_title", "publication_date", "year", "venue", "doi", "arxiv_id",
    "primary_url", "current_primary_category", "recommended_primary_category",
    "secondary_roles", "category_review_status", "source_decision", "source_scope", "source_status",
    "source_reason", "source_path", "route_strength", "ledger_decision",
    "ledger_decision_source", "human_signoff_required",
]

QUEUE_FIELDS = [
    "work_key", "canonical_paper_id", "title", "publication_date", "year", "venue", "doi", "arxiv_id",
    "primary_url", "current_primary_category", "recommended_primary_category",
    "secondary_roles", "category_review_status", "route_types", "route_ids", "route_count", "source_decisions", "source_scopes",
    "source_statuses", "source_paths", "seed_decision", "seed_decision_source", "seed_decision_reason",
    "seed_decision_strength", "ledger_decision", "ledger_decision_source", "ledger_rationale", "reviewer",
    "reviewed_at", "locked", "human_signoff_required", "needs_review",
]

FINAL_FIELDS = [
    "work_key", "canonical_paper_id", "title", "publication_date", "year", "venue", "doi", "arxiv_id",
    "primary_url", "current_primary_category", "recommended_primary_category",
    "secondary_roles", "category_review_status", "decision", "decision_source", "rationale", "reviewer", "reviewed_at",
    "human_signoff_required", "route_types", "route_ids", "source_paths",
]

SUMMARY_FIELDS = ["population", "dimension", "value", "count", "note"]


def merge_ledger(queue_seed: list[dict[str, str]], existing_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_key = {row.get("work_key", ""): row for row in existing_rows if row.get("work_key")}
    by_paper = {row.get("canonical_paper_id", ""): row for row in existing_rows if row.get("canonical_paper_id")}
    by_arxiv = {norm_arxiv(row.get("arxiv_id", "")): row for row in existing_rows if norm_arxiv(row.get("arxiv_id", ""))}
    by_doi = {norm_doi(row.get("doi", "")): row for row in existing_rows if norm_doi(row.get("doi", ""))}
    by_title = {norm_title(row.get("title", "")): row for row in existing_rows if norm_title(row.get("title", ""))}

    used_ids: set[int] = set()
    merged: list[dict[str, str]] = []
    for seed in queue_seed:
        old = by_key.get(seed["work_key"])
        if old is None and seed["canonical_paper_id"]:
            old = by_paper.get(seed["canonical_paper_id"])
        if old is None and seed["arxiv_id"]:
            old = by_arxiv.get(seed["arxiv_id"])
        if old is None and seed["doi"]:
            old = by_doi.get(seed["doi"])
        if old is None:
            old = by_title.get(seed["normalized_title"])

        if old is not None:
            used_ids.add(id(old))
            previous_keys = {x for x in text(old.get("previous_work_keys")).split(";") if x}
            if old.get("work_key") and old.get("work_key") != seed["work_key"]:
                previous_keys.add(old["work_key"])

            # Only an explicit human decision is immutable. Generated seeds are
            # refreshed when source ledgers change, otherwise the first build
            # would freeze stale automatic classifications forever. A reviewer,
            # review timestamp, or locked=yes marks an intentional adjudication.
            preserve_old = (
                text(old.get("locked")).casefold() == "yes"
                or bool(text(old.get("reviewer")))
                or bool(text(old.get("reviewed_at")))
                or text(old.get("decision_source")).casefold().startswith("manual:")
            )
            decision = text(old.get("decision")) if preserve_old else seed["seed_decision"]
            if not decision:
                decision = seed["seed_decision"]
            if decision not in ALL_DECISIONS:
                raise ValueError(f"invalid ledger decision {decision!r} for {seed['work_key']}")
            row = {
                "work_key": seed["work_key"],
                "canonical_paper_id": seed["canonical_paper_id"],
                "title": seed["title"],
                "doi": seed["doi"],
                "arxiv_id": seed["arxiv_id"],
                "decision": decision,
                "decision_source": text(old.get("decision_source")) if preserve_old else seed["seed_decision_source"],
                "decision_strength": text(old.get("decision_strength")) if preserve_old else seed["seed_decision_strength"],
                "rationale": text(old.get("rationale")) if preserve_old else seed["seed_decision_reason"],
                "reviewer": text(old.get("reviewer")) if preserve_old else "",
                "reviewed_at": text(old.get("reviewed_at")) if preserve_old else "",
                "locked": text(old.get("locked")) if preserve_old else "no",
                "human_signoff_required": text(old.get("human_signoff_required")) if preserve_old else seed["human_signoff_required"],
                "previous_work_keys": ";".join(sorted(previous_keys)),
                "notes": text(old.get("notes")),
            }
        else:
            row = {
                "work_key": seed["work_key"],
                "canonical_paper_id": seed["canonical_paper_id"],
                "title": seed["title"],
                "doi": seed["doi"],
                "arxiv_id": seed["arxiv_id"],
                "decision": seed["seed_decision"],
                "decision_source": seed["seed_decision_source"],
                "decision_strength": seed["seed_decision_strength"],
                "rationale": seed["seed_decision_reason"],
                "reviewer": "",
                "reviewed_at": "",
                "locked": "no",
                "human_signoff_required": seed["human_signoff_required"],
                "previous_work_keys": "",
                "notes": "",
            }
        merged.append(row)

    # Preserve unmatched historical rows rather than silently deleting human work.
    for old in existing_rows:
        if id(old) in used_ids:
            continue
        row = {field: text(old.get(field)) for field in LEDGER_FIELDS}
        row["notes"] = (row["notes"] + "; " if row["notes"] else "") + "orphaned_from_current_candidate_queue"
        merged.append(row)

    return sorted(merged, key=lambda r: (r["decision"], r["title"].casefold(), r["work_key"]))


def render(output_dir: Path, existing_ledger_path: Path | None) -> dict[str, object]:
    overrides, override_rows = load_overrides()
    routes, route_counts = build_routes()
    groups, _raw_alias_rows = deduplicate(routes, overrides)
    group_seed_pairs = [(group, canonical_group_row(group)) for group in groups]
    group_seed_pairs.sort(key=lambda pair: (pair[1]["title"].casefold(), pair[1]["work_key"]))
    seed_rows = [seed for _, seed in group_seed_pairs]

    paper_metadata = {row["paper_id"]: row for row in read_csv(PAPERS)}
    review_metadata = {row["paper_id"]: row for row in read_csv(REVIEWS)}
    for seed in seed_rows:
        paper = paper_metadata.get(seed["canonical_paper_id"], {})
        review = review_metadata.get(seed["canonical_paper_id"], {})
        seed["current_primary_category"] = text(paper.get("primary_category"))
        seed["recommended_primary_category"] = text(review.get("recommended_category"))
        seed["secondary_roles"] = text(review.get("secondary_roles"))
        seed["category_review_status"] = text(review.get("review_status"))

    existing_ledger = read_csv(existing_ledger_path) if existing_ledger_path and existing_ledger_path.exists() else []
    ledger_rows = merge_ledger(seed_rows, existing_ledger)
    ledger_by_key = {row["work_key"]: row for row in ledger_rows}

    queue_rows: list[dict[str, str]] = []
    route_queue_rows: list[dict[str, str]] = []
    final_rows: dict[str, list[dict[str, str]]] = {name: [] for name in ("primary", "secondary", "exclude")}
    pending_rows: list[dict[str, str]] = []

    for group, seed in group_seed_pairs:
        ledger = ledger_by_key[seed["work_key"]]
        for route in sorted(group, key=lambda item: (item.route_type, item.route_id)):
            route_queue_rows.append(
                {
                    "route_id": route.route_id,
                    "route_type": route.route_type,
                    "work_key": seed["work_key"],
                    "canonical_paper_id": seed["canonical_paper_id"],
                    "route_title": route.title,
                    "canonical_title": seed["title"],
                    "publication_date": route.publication_date,
                    "year": route.year,
                    "venue": route.venue,
                    "doi": route.doi,
                    "arxiv_id": route.arxiv_id,
                    "primary_url": route.primary_url,
                    "current_primary_category": seed["current_primary_category"],
                    "recommended_primary_category": seed["recommended_primary_category"],
                    "secondary_roles": seed["secondary_roles"],
                    "category_review_status": seed["category_review_status"],
                    "source_decision": route.source_decision,
                    "source_scope": route.source_scope,
                    "source_status": route.source_status,
                    "source_reason": route.source_reason,
                    "source_path": route.source_path,
                    "route_strength": str(route.route_strength),
                    "ledger_decision": ledger["decision"],
                    "ledger_decision_source": ledger["decision_source"],
                    "human_signoff_required": ledger["human_signoff_required"],
                }
            )

    for seed in seed_rows:
        ledger = ledger_by_key[seed["work_key"]]
        decision = ledger["decision"]
        queue = dict(seed)
        queue.update(
            {
                "ledger_decision": decision,
                "ledger_decision_source": ledger["decision_source"],
                "ledger_rationale": ledger["rationale"],
                "reviewer": ledger["reviewer"],
                "reviewed_at": ledger["reviewed_at"],
                "locked": ledger["locked"],
                "human_signoff_required": ledger["human_signoff_required"],
                "needs_review": "yes" if decision == "pending" or ledger["human_signoff_required"] == "yes" else "no",
            }
        )
        queue_rows.append(queue)
        final = {
            "work_key": seed["work_key"],
            "canonical_paper_id": seed["canonical_paper_id"],
            "title": seed["title"],
            "publication_date": seed["publication_date"],
            "year": seed["year"],
            "venue": seed["venue"],
            "doi": seed["doi"],
            "arxiv_id": seed["arxiv_id"],
            "primary_url": seed["primary_url"],
            "current_primary_category": seed["current_primary_category"],
            "recommended_primary_category": seed["recommended_primary_category"],
            "secondary_roles": seed["secondary_roles"],
            "category_review_status": seed["category_review_status"],
            "decision": decision,
            "decision_source": ledger["decision_source"],
            "rationale": ledger["rationale"],
            "reviewer": ledger["reviewer"],
            "reviewed_at": ledger["reviewed_at"],
            "human_signoff_required": ledger["human_signoff_required"],
            "route_types": seed["route_types"],
            "route_ids": seed["route_ids"],
            "source_paths": seed["source_paths"],
        }
        if decision in FINAL_DECISIONS:
            final_rows[decision].append(final)
        else:
            pending_rows.append(final)

    # Identifier aliases retain every public identifier observed on every route.
    # This makes version merges inspectable instead of silently discarding old IDs.
    alias_aggregate: dict[tuple[str, str, str], dict[str, object]] = {}
    for group, seed in group_seed_pairs:
        for route in group:
            for kind, value in (("doi", route.doi), ("arxiv", route.arxiv_id)):
                if not value:
                    continue
                key = (seed["work_key"], kind, value)
                entry = alias_aggregate.setdefault(
                    key,
                    {
                        "work_key": seed["work_key"],
                        "canonical_paper_id": seed["canonical_paper_id"],
                        "title": seed["title"],
                        "identifier_type": kind,
                        "identifier": value,
                        "identifier_status": "canonical" if value == seed[kind if kind == "doi" else "arxiv_id"] else "route_alias",
                        "observed_in_routes": set(),
                    },
                )
                entry["observed_in_routes"].add(route.route_id)
        for override in override_rows:
            canonical_doi = norm_doi(override.get("canonical_doi", ""))
            canonical_arxiv = norm_arxiv(override.get("canonical_arxiv_id", ""))
            if not ((canonical_doi and seed["doi"] == canonical_doi) or (canonical_arxiv and seed["arxiv_id"] == canonical_arxiv)):
                continue
            alias_type = text(override.get("alias_type")).casefold()
            alias_value = text(override.get("alias_value"))
            if alias_type == "doi":
                alias_value = norm_doi(alias_value)
            elif alias_type == "arxiv":
                alias_value = norm_arxiv(alias_value)
            else:
                alias_value = norm_title(alias_value)
            if not alias_value:
                continue
            key = (seed["work_key"], alias_type, alias_value)
            entry = alias_aggregate.setdefault(
                key,
                {
                    "work_key": seed["work_key"],
                    "canonical_paper_id": seed["canonical_paper_id"],
                    "title": seed["title"],
                    "identifier_type": alias_type,
                    "identifier": alias_value,
                    "identifier_status": "override_alias",
                    "observed_in_routes": set(),
                },
            )
            if entry["identifier_status"] != "canonical":
                entry["identifier_status"] = "override_alias"

    alias_rows: list[dict[str, str]] = []
    for entry in alias_aggregate.values():
        alias_rows.append(
            {
                **{key: text(value) for key, value in entry.items() if key != "observed_in_routes"},
                "observed_in_routes": ";".join(sorted(entry["observed_in_routes"])),
            }
        )

    for rows in final_rows.values():
        rows.sort(key=lambda r: (r["year"], r["title"].casefold(), r["work_key"]))
    pending_rows.sort(key=lambda r: (r["title"].casefold(), r["work_key"]))
    queue_rows.sort(key=lambda r: (r["ledger_decision"], r["title"].casefold(), r["work_key"]))
    route_queue_rows.sort(key=lambda r: (r["route_type"], r["route_id"]))
    alias_rows.sort(key=lambda r: (r["identifier_type"], r["identifier"], r["work_key"]))

    summary_rows: list[dict[str, str]] = []

    def add_summary(population: str, dimension: str, values: Iterable[str], note: str = "") -> None:
        for value, count in sorted(Counter(text(item) or "unclassified" for item in values).items()):
            summary_rows.append(
                {
                    "population": population,
                    "dimension": dimension,
                    "value": value,
                    "count": str(count),
                    "note": note,
                }
            )

    add_summary("all_work_queue", "decision", (row["ledger_decision"] for row in queue_rows))
    canonical_rows = [row for row in queue_rows if "canonical" in row["route_types"].split(";")]
    add_summary("canonical_142", "decision", (row["ledger_decision"] for row in canonical_rows))
    add_summary("canonical_142", "current_primary_category", (row["current_primary_category"] for row in canonical_rows))
    add_summary("canonical_142", "recommended_primary_category", (row["recommended_primary_category"] for row in canonical_rows))
    add_summary("targeted_318_records", "decision", (row["ledger_decision"] for row in route_queue_rows if row["route_type"] == "targeted"), "Route-record count; version records remain separate.")
    targeted_work_rows = [row for row in queue_rows if "targeted" in row["route_types"].split(";")]
    add_summary("targeted_317_works", "decision", (row["ledger_decision"] for row in targeted_work_rows), "Work-level count after version merging.")
    for decision in ("primary", "secondary", "exclude", "pending"):
        rows = pending_rows if decision == "pending" else final_rows[decision]
        add_summary(f"final_{decision}", "current_primary_category", (row["current_primary_category"] for row in rows))
    add_summary("route_ledger", "route_type", (row["route_type"] for row in route_queue_rows))

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / LEDGER.name, LEDGER_FIELDS, ledger_rows)
    write_csv(output_dir / QUEUE.name, QUEUE_FIELDS, queue_rows)
    write_csv(output_dir / ROUTE_QUEUE.name, ROUTE_QUEUE_FIELDS, route_queue_rows)
    write_csv(output_dir / PRIMARY.name, FINAL_FIELDS, final_rows["primary"])
    write_csv(output_dir / SECONDARY.name, FINAL_FIELDS, final_rows["secondary"])
    write_csv(output_dir / EXCLUDE.name, FINAL_FIELDS, final_rows["exclude"])
    write_csv(output_dir / PENDING.name, FINAL_FIELDS, pending_rows)
    write_csv(output_dir / ALIASES.name, ["work_key", "canonical_paper_id", "title", "identifier_type", "identifier", "identifier_status", "observed_in_routes"], alias_rows)
    write_csv(output_dir / SUMMARY.name, SUMMARY_FIELDS, summary_rows)

    counts = Counter(row["ledger_decision"] for row in queue_rows)
    targeted_ids = {route.route_id for route in routes if route.route_type == "targeted"}
    targeted_route_rows = [row for row in route_queue_rows if row["route_type"] == "targeted"]
    targeted_visible_ids = {row["route_id"] for row in targeted_route_rows}
    targeted_work_keys = {row["work_key"] for row in targeted_route_rows}
    canonical_queue = sum("canonical" in row["route_types"].split(";") for row in queue_rows)

    # Pairwise disjointness and identifier uniqueness are hard invariants.
    key_sets = {name: {row["work_key"] for row in rows} for name, rows in final_rows.items()}
    for left, right in (("primary", "secondary"), ("primary", "exclude"), ("secondary", "exclude")):
        overlap = key_sets[left] & key_sets[right]
        if overlap:
            raise ValueError(f"final sets overlap: {left}/{right}: {sorted(overlap)[:10]}")
    identifier_owner: dict[tuple[str, str], str] = {}
    for row in alias_rows:
        key = (row["identifier_type"], row["identifier"])
        owner = identifier_owner.setdefault(key, row["work_key"])
        if owner != row["work_key"]:
            raise ValueError(f"public identifier maps to multiple work keys: {key} -> {owner}, {row['work_key']}")
    if len(targeted_ids) != 318 or targeted_visible_ids != targeted_ids:
        missing = sorted(targeted_ids - targeted_visible_ids)
        extra = sorted(targeted_visible_ids - targeted_ids)
        raise ValueError(
            f"targeted route visibility failed: source={len(targeted_ids)} visible={len(targeted_visible_ids)} "
            f"missing={missing[:5]} extra={extra[:5]}"
        )

    chain_rows = [row for row in queue_rows if row["arxiv_id"] == "2508.15809"]
    if len(chain_rows) != 1:
        raise ValueError(f"arXiv 2508.15809 must resolve to one queue row, found {len(chain_rows)}")
    if chain_rows[0]["doi"] != "10.18653/v1/2025.ijcnlp-long.53":
        raise ValueError(f"Chain-of-Query canonical DOI is wrong: {chain_rows[0]['doi']}")

    manifest = {
        "schema_version": 2,
        "cutoff": CUTOFF,
        "candidate_unit": "canonical work",
        "decision_sets": ["primary", "secondary", "exclude"],
        "pending_policy": "pending rows remain in the queue and never enter a final set",
        "deduplication_priority": ["canonical_paper_id", "arxiv_id", "doi", "exact_normalized_title"],
        "decision_priority": "persistent ledger, canonical/source review, peer-first reviewed gate, structured exclusion, full-text search screen, weaker routes",
        "queue_count": len(queue_rows),
        "ledger_count": len(ledger_rows),
        "primary_count": counts["primary"],
        "secondary_count": counts["secondary"],
        "exclude_count": counts["exclude"],
        "pending_count": counts["pending"],
        "canonical_route_works_visible": canonical_queue,
        "targeted_cutoff_candidate_records": len(targeted_ids),
        "targeted_candidate_records_visible_in_route_queue": len(targeted_visible_ids),
        "targeted_canonical_works": len(targeted_work_keys),
        "targeted_version_merges": len(targeted_ids) - len(targeted_work_keys),
        "targeted_derivation": "325 broad-screen works minus seven records explicitly reviewed with recommended_scope=adjacent",
        "route_row_counts": route_counts,
        "route_rows_total": len(routes),
        "deduplicated_route_groups": len(groups),
        "identifier_override_count": len(override_rows),
        "human_signoff_required_count": sum(row["human_signoff_required"] == "yes" for row in queue_rows),
        "summary_row_count": len(summary_rows),
        "canonical_current_category_counts": dict(sorted(Counter(row["current_primary_category"] for row in canonical_rows).items())),
        "source_files": {
            str(path.relative_to(ROOT)): {"rows": len(read_csv(path)), "sha256": sha256(path)}
            for path in [SEARCH, BROAD, TAXONOMY, PAPERS, CANONICAL, REVIEWS, STRUCTURED_EXCLUSIONS, TARGETED_GAP, IDENTIFIER_OVERRIDES]
        },
    }
    (output_dir / MANIFEST.name).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def compare_files(expected_dir: Path, actual_dir: Path) -> list[str]:
    names = [QUEUE.name, ROUTE_QUEUE.name, LEDGER.name, PRIMARY.name, SECONDARY.name, EXCLUDE.name, PENDING.name, ALIASES.name, SUMMARY.name, MANIFEST.name]
    mismatches = []
    for name in names:
        expected = expected_dir / name
        actual = actual_dir / name
        if not actual.exists():
            mismatches.append(f"missing {actual}")
        elif expected.read_bytes() != actual.read_bytes():
            mismatches.append(f"stale {actual}")
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    HERE.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="review-sets-v2-") as temp:
        temp_dir = Path(temp)
        manifest = render(temp_dir, LEDGER if LEDGER.exists() else None)
        if args.check:
            mismatches = compare_files(temp_dir, HERE)
            if mismatches:
                print("\n".join(mismatches), file=sys.stderr)
                return 1
        else:
            for name in [QUEUE.name, ROUTE_QUEUE.name, LEDGER.name, PRIMARY.name, SECONDARY.name, EXCLUDE.name, PENDING.name, ALIASES.name, SUMMARY.name, MANIFEST.name]:
                shutil.copyfile(temp_dir / name, HERE / name)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
