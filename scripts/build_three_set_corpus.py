#!/usr/bin/env python3
"""Build the three evidence sets used by the MAS security SoK.

Set 1 is the mature core synthesis corpus. Set 2 contains in-scope emerging
work. Set 3 contains contextual citations and is not part of the corpus.
Everything else remains in the screened search ledger.

The builder is conservative. It combines the repository review ledger with
source-review artifacts, requires source evidence for Set 1 and Set 2, freezes
citation counts, and records every promotion or downgrade for author signoff.
It does not claim human verification.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EVIDENCE_ROOT = ROOT / "review-evidence"
REVIEW_DATE = "2026-08-17"
CUTOFF = "2026-07-01"
REVIEWER = "OpenAI GPT-5.6 Pro, model-assisted source review"

FINAL_FILES = {
    "set1_core": "set1_core.csv",
    "set2_emerging": "set2_emerging.csv",
    "set3_context": "set3_context.csv",
    "screened_out": "screened_out.csv",
}

LLM_TERMS = [
    "large language model", "large-language model", " llm", "llm ",
    "gpt-", "language model agent", "language agents", "agentic ai",
]
MULTI_TERMS = [
    "multi-agent", "multi agent", "multiple agent", "agent society",
    "agent swarm", "agent team", "agent network", "agent collective",
    "llm agents", "language agents", "agent-to-agent", "inter-agent",
    "cross-agent",
]
DIRECT_SECURITY_TERMS = [
    "security", "attack", "adversarial", "adversary", "threat model",
    "vulnerab", "exploit", "poison", "jailbreak", "backdoor",
    "malicious", "privacy", "leak", "exfiltrat", "confidentiality",
    "integrity", "authoriz", "authenticat", "access control",
    "credential", "byzantine", "collusion", "deception", "manipulat",
    "denial of service", "denial-of-service", "guardrail", "red team",
    "unsafe", "misinformation", "prompt injection",
]
SOFT_SECURITY_TERMS = [
    "safety", "trust", "trustworthy", "reliability", "robust",
    "governance", "accountab", "audit", "monitor", "risk", "alignment",
    "oversight", "verification", "fault tolerance", "fault-tolerance",
]
INTERACTION_TERMS = [
    "inter-agent", "cross-agent", "agent-to-agent", "communication",
    "message passing", "messages", "shared memory", "shared state",
    "delegat", "handoff", "hand-off", "consensus", "voting", "debate",
    "collusion", "coalition", "topology", "coordinator", "routing",
    "peer agent", "collective decision", "aggregation", "quorum",
    "compromised agent", "malicious agent", "byzantine agent",
    "propagat", "spread across agents", "recursive", "infection",
    "retransmit", "joint decision", "agent interaction", "role interaction",
]
SYSTEM_TARGET_TERMS = [
    "multi-agent security", "security of multi-agent", "secure multi-agent",
    "multi-agent attack", "attack on multi-agent", "attack against multi-agent",
    "multi-agent vulnerab", "multi-agent threat", "malicious agent",
    "compromised agent", "byzantine agent", "cross-agent leakage",
    "inter-agent leakage", "shared memory poisoning",
    "consensus manipulation", "collective manipulation", "agent collusion",
    "colluding agents", "propagation across agents", "delegation attack",
    "delegated authority", "communication attack", "topology attack",
    "agent-to-agent security", "failure propagation", "cascade",
]
EXTERNAL_APPLICATION_TERMS = [
    "penetration test", "vulnerability detection", "vulnerability discovery",
    "smart contract", "malware detection", "intrusion detection",
    "phishing detection", "cyber threat intelligence", "security operation",
    "secure code generation", "code generation", "software development",
    "bug finding", "fraud detection", "medical diagnosis",
    "health monitoring", "construction safety", "traffic safety",
    "drug discovery", "fault diagnosis", "recommendation system",
    "autonomous driving", "wireless network", "power grid",
    "energy management",
]
SURVEY_TERMS = [
    "survey", "systematic review", "literature review", "position paper",
    "research agenda", "open challenges", "overview of", "landscape of",
]
PREPRINT_VENUE_TERMS = [
    "arxiv", "ssrn", "zenodo", "research square", "techrxiv", "osf",
    "preprints", "biorxiv", "medrxiv", "openreview", "cornell university",
    "authorea",
]
PEER_TYPES = [
    "journal-article", "proceedings-article", "book-chapter",
    "journal article", "conference paper", "proceedings article",
]
NON_PEER_TYPES = ["posted-content", "preprint", "report", "dataset", "thesis"]
ATTACK_TERMS = [
    "attack", "adversarial", "poison", "jailbreak", "backdoor",
    "malicious", "exploit", "vulnerab", "collusion", "deception",
    "manipulat", "hijack", "infection", "worm",
]
DEFENSE_TERMS = [
    "defense", "defence", "guard", "secure", "monitor", "access control",
    "authorization", "privacy-preserving", "trust framework", "mitigat",
    "protect", "isolation", "provenance", "taint", "authentication",
]
EVALUATION_TERMS = [
    "benchmark", "evaluation", "evaluate", "audit", "assessment",
    "empirical", "measurement", "dataset", "taxonomy", "study of",
    "analysis of",
]


def clean(value: object) -> str:
    text = html.unescape("" if value is None else str(value))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[A-Za-z]+\{([^{}]*)\}", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_title(value: object) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", clean(value).lower())
    return " ".join(text.split())


def normalize_doi(value: object) -> str:
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", clean(value).lower())
    match = re.search(r"(10\.\d{4,9}/[^\s\"<>]+)", text)
    return match.group(1).rstrip(".,;)]}") if match else ""


def normalize_arxiv(value: object) -> str:
    match = re.search(r"(\d{4}\.\d{4,5})(?:v\d+)?", clean(value).lower())
    return match.group(1) if match else ""


def has_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def count_terms(text: str, terms: Iterable[str]) -> int:
    return sum(text.count(term) for term in terms)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def numeric_citation_values(row: dict[str, str]) -> list[tuple[str, int]]:
    values: list[tuple[str, int]] = []
    for key, value in row.items():
        lowered = key.lower()
        if not any(token in lowered for token in (
            "citation", "cited_by", "citedby", "is_referenced_by",
            "referenced-by",
        )):
            continue
        if "reference_count" in lowered or "referenced_works" in lowered:
            continue
        text = clean(value).replace(",", "")
        if re.fullmatch(r"\d+(?:\.\d+)?", text):
            number = int(float(text))
            if 0 <= number < 10_000_000:
                values.append((key, number))
    return values


def valid_dates(row: dict[str, str]) -> list[str]:
    dates: list[str] = []
    for key, value in row.items():
        lowered = key.lower()
        if not (any(token in lowered for token in (
            "date", "published", "created", "issued",
        )) or lowered == "year"):
            continue
        match = re.search(r"(20\d{2})(?:-(\d{2})-(\d{2}))?", clean(value))
        if not match:
            continue
        year = int(match.group(1))
        month = int(match.group(2) or 1)
        day = int(match.group(3) or 1)
        if 2000 <= year <= 2030 and 1 <= month <= 12 and 1 <= day <= 31:
            dates.append(f"{year:04d}-{month:02d}-{day:02d}")
    return sorted(set(dates))


def load_source_index() -> tuple[
    dict[tuple[str, str], list[dict[str, object]]],
    dict[str, list[dict[str, object]]],
    list[dict[str, object]],
]:
    by_identifier: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    by_title: dict[str, list[dict[str, object]]] = defaultdict(list)
    inventory: list[dict[str, object]] = []

    for path in sorted(EVIDENCE_ROOT.rglob("*.csv")):
        try:
            rows = read_csv(path)
        except Exception:
            continue
        if not rows:
            continue
        relative = str(path.relative_to(EVIDENCE_ROOT))
        inventory.append({"path": relative, "rows": len(rows)})
        for row in rows:
            work_key = ""
            doi = ""
            arxiv_id = ""
            title = ""
            for key, value in row.items():
                lowered = key.lower()
                if not work_key and lowered in {
                    "work_key", "dedup_key", "record_id", "paper_id",
                    "canonical_paper_id",
                }:
                    work_key = clean(value)
                if not doi and "doi" in lowered:
                    doi = normalize_doi(value)
                if not arxiv_id and ("arxiv" in lowered or lowered == "eprint"):
                    arxiv_id = normalize_arxiv(value)
                if not title and lowered in {
                    "title", "paper_title", "display_name", "work_title",
                    "openalex_title", "s2_title", "crossref_title",
                    "arxiv_title",
                }:
                    title = clean(value)
            if not doi:
                for value in row.values():
                    doi = normalize_doi(value)
                    if doi:
                        break
            if not arxiv_id:
                for value in row.values():
                    arxiv_id = normalize_arxiv(value)
                    if arxiv_id:
                        break

            record: dict[str, object] = {"source_file": relative, "row": row}
            if work_key:
                by_identifier[("work", work_key)].append(record)
            if doi:
                by_identifier[("doi", doi)].append(record)
            if arxiv_id:
                by_identifier[("arxiv", arxiv_id)].append(record)
            normalized_title = normalize_title(title)
            if normalized_title:
                by_title[normalized_title].append(record)
    return by_identifier, by_title, inventory


def matched_records(
    row: dict[str, str],
    by_identifier: dict[tuple[str, str], list[dict[str, object]]],
    by_title: dict[str, list[dict[str, object]]],
) -> list[dict[str, object]]:
    keys = [
        ("work", clean(row.get("work_key", ""))),
        ("doi", normalize_doi(row.get("doi", ""))),
        ("arxiv", normalize_arxiv(row.get("arxiv_id", ""))),
    ]
    records: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for key in keys:
        if not key[1]:
            continue
        for record in by_identifier.get(key, []):
            signature = (
                str(record["source_file"]),
                json.dumps(record["row"], ensure_ascii=False, sort_keys=True),
            )
            if signature not in seen:
                seen.add(signature)
                records.append(record)
    title = normalize_title(row.get("title", ""))
    if title:
        for record in by_title.get(title, []):
            signature = (
                str(record["source_file"]),
                json.dumps(record["row"], ensure_ascii=False, sort_keys=True),
            )
            if signature not in seen:
                seen.add(signature)
                records.append(record)
    records.append({"source_file": "corpus/review_queue.csv", "row": row})
    return records


def collect_source_text(
    queue_row: dict[str, str], records: list[dict[str, object]]
) -> tuple[str, str, str, str]:
    abstracts: list[str] = []
    full_text: list[str] = []
    evidence: list[str] = []
    parts = [
        clean(queue_row.get("title", "")),
        clean(queue_row.get("rationale", "")),
        clean(queue_row.get("screening_note", "")),
    ]
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        for key, value in row.items():
            lowered = key.lower()
            text = clean(value)
            if not text:
                continue
            if "abstract" in lowered or lowered in {"summary", "description"}:
                abstracts.append(text)
            elif any(token in lowered for token in (
                "full_text", "fulltext", "pdf_text", "paper_text",
            )) and len(text) > 200:
                full_text.append(text)
            elif any(token in lowered for token in (
                "evidence", "rationale", "screening_note", "reason",
                "scope_relation", "final_decision", "decision", "gate",
            )):
                evidence.append(text)

    abstract_text = " ".join(dict.fromkeys(abstracts))[:24_000]
    paper_text = " ".join(dict.fromkeys(full_text))[:80_000]
    evidence_text = " ".join(dict.fromkeys(evidence))[:16_000]
    all_text = clean(" ".join(parts + [abstract_text, evidence_text, paper_text]))
    return all_text, abstract_text, paper_text, evidence_text


def prior_signals(
    records: list[dict[str, object]], queue_row: dict[str, str]
) -> tuple[list[str], list[str], list[str], list[str]]:
    include: list[str] = []
    context: list[str] = []
    exclude: list[str] = []
    canonical: list[str] = []
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        source = str(record["source_file"])
        joined = " ".join(clean(value) for value in row.values()).lower()
        if any(token in joined for token in (
            "include-primary-interaction-security", "core_security",
            "strict-pass", "strict pass", "eligible_not_in_corpus",
            "included_attack_canonical",
        )):
            include.append(source)
        if any(token in joined for token in (
            "security_relevant", "include-secondary", "contextual", "adjacent",
        )):
            context.append(source)
        if any(token in joined for token in (
            "exclude-no-interaction-security", "exclude-no-multi-core",
            "exclude-no-separate-llm-cores", "exclude-secondary-or-nonstudy",
            "exclude-no-reported-endpoint", "no_direct_security_property",
            "no_multiagent_boundary", "external_application_only",
        )):
            exclude.append(source)
        if "canonical:" in joined or clean(row.get("canonical_paper_id", "")):
            canonical.append(source)

    if queue_row.get("scope_relation") == "core_security":
        include.append("queue_scope")
    elif queue_row.get("scope_relation") == "security_relevant":
        context.append("queue_scope")
    return include, context, exclude, canonical


def citation_information(
    records: list[dict[str, object]], queue_row: dict[str, str]
) -> tuple[int, str, str]:
    candidates: list[tuple[int, int, str, str]] = []
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        for field, value in numeric_citation_values(row):
            joined = (str(record["source_file"]) + " " + field).lower()
            priority = 3 if "openalex" in joined or "cited_by" in joined else 2
            candidates.append((priority, value, str(record["source_file"]), field))
    for field, value in numeric_citation_values(queue_row):
        candidates.append((1, value, "corpus/review_queue.csv", field))
    if not candidates:
        return 0, "none", ""
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    _, count, source_file, field = candidates[0]
    joined = (source_file + " " + field).lower()
    source = "OpenAlex" if "openalex" in joined or "cited_by" in joined else (
        "Semantic Scholar" if "semantic" in joined or "s2" in joined else source_file
    )
    return count, source, field


def peer_review_information(
    records: list[dict[str, object]], queue_row: dict[str, str]
) -> tuple[str, str]:
    explicit: list[str] = []
    types: list[str] = []
    venues: list[str] = [clean(queue_row.get("venue", ""))]
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        for key, value in row.items():
            lowered = key.lower()
            text = clean(value)
            if not text:
                continue
            if "peer" in lowered and "review" in lowered:
                explicit.append(text.lower())
            if lowered.endswith("type") or "publication_type" in lowered:
                types.append(text.lower())
            if any(token in lowered for token in (
                "venue", "container", "primary_source", "source_name",
            )):
                venues.append(text)

    if any(value in {"yes", "true", "peer-reviewed", "peer reviewed", "archival"}
           or "peer-reviewed" in value for value in explicit):
        return "yes", "explicit metadata"
    if any(value in {"no", "false", "preprint", "not peer reviewed",
                     "non-peer-reviewed"} for value in explicit):
        return "no", "explicit metadata"

    venue = " ; ".join(dict.fromkeys(venues)).lower()
    publication_type = " ; ".join(dict.fromkeys(types)).lower()
    if has_any(venue, PREPRINT_VENUE_TERMS) or has_any(publication_type, NON_PEER_TYPES):
        return "no", "preprint or non-archival source"
    if has_any(publication_type, PEER_TYPES) and venue:
        return "yes", "archival publication metadata"

    archival_tokens = [
        "proceedings", "conference on", "transactions on", "journal of",
        "acm ", "ieee ", "usenix", "neurips", "icml", "acl", "emnlp",
        "naacl", "aaai", "ijcai", "springer", "elsevier", "mdpi", "wiley",
        "nature", "science", "pmlr",
    ]
    if venue and has_any(venue, archival_tokens):
        return "yes", "archival venue heuristic"
    return "unclear", "insufficient publication metadata"


def evidence_basis(abstract: str, paper_text: str, records: list[dict[str, object]]) -> str:
    if len(paper_text) >= 500:
        return "full_text"
    if len(abstract) >= 80:
        return "abstract"
    if any("fulltext" in str(record["source_file"]).lower()
           or "full_text" in str(record["source_file"]).lower()
           for record in records):
        return "full_text_screen_record"
    return "title_metadata"


def earliest_publication_date(
    queue_row: dict[str, str], records: list[dict[str, object]]
) -> str:
    dates = valid_dates(queue_row)
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        dates.extend(valid_dates(row))
    return sorted(set(dates))[0] if dates else ""


def evidence_locator(records: list[dict[str, object]]) -> str:
    locators: list[str] = []
    for record in records:
        row = record["row"]
        assert isinstance(row, dict)
        for key, value in row.items():
            lowered = key.lower()
            text = clean(value)
            if text and any(token in lowered for token in (
                "locator", "page", "section", "evidence_sentence",
                "evidence_phrase", "full_text_url", "pdf_url",
            )):
                locators.append(
                    f"{record['source_file']}:{key}={text[:500]}"
                )
    return " | ".join(dict.fromkeys(locators))[:4000]


def contribution(text: str, existing: str) -> str:
    normalized = clean(existing).lower()
    if normalized in {"attack", "defense", "evaluation", "survey", "general"}:
        return normalized
    if normalized == "other":
        return "general"
    if has_any(text, SURVEY_TERMS):
        return "survey"
    attack = count_terms(text, ATTACK_TERMS)
    defense = count_terms(text, DEFENSE_TERMS)
    evaluation = count_terms(text, EVALUATION_TERMS)
    if evaluation >= max(attack, defense) and evaluation > 0:
        return "evaluation"
    if attack > defense and attack > 0:
        return "attack"
    if defense > 0:
        return "defense"
    return "general"


def interaction_interfaces(text: str) -> str:
    groups = {
        "I1_boundary_admission": [
            "admission", "membership", "discovery", "registry",
            "external content", "retrieval", "webpage", "input",
        ],
        "I2_communication_routing": [
            "message", "communication", "routing", "topology", "peer",
            "broadcast", "channel", "retransmit",
        ],
        "I3_state_memory": [
            "memory", "shared state", "shared memory", "cache", "artifact",
            "persistent", "state poisoning",
        ],
        "I4_delegation_action": [
            "delegat", "handoff", "tool", "authority", "permission",
            "credential", "capability", "action",
        ],
        "I5_aggregation_outcome": [
            "vote", "voting", "consensus", "debate", "aggregation",
            "collective decision", "quorum", "majority",
        ],
        "I6_observation_defense": [
            "monitor", "guardrail", "detector", "audit", "oversight",
            "logging", "defense service", "sanitizer",
        ],
    }
    tags = [name for name, terms in groups.items() if has_any(text, terms)]
    return ";".join(tags or ["unspecified"])


def risk_tags(text: str) -> str:
    groups = {
        "R1_propagation_persistence": [
            "propagat", "spread", "infection", "worm", "persistent",
            "cascade", "contag",
        ],
        "R2_collusion_coordination": [
            "collusion", "colluding", "covert channel", "coalition",
            "coordination attack", "stegan",
        ],
        "R3_collective_integrity": [
            "consensus", "vote", "debate", "collective decision",
            "misinformation", "false belief", "majority",
        ],
        "R4_trajectory_goal_drift": [
            "goal drift", "trajectory", "alignment drift", "behavioral drift",
            "value drift", "policy drift",
        ],
        "R5_private_data_leakage": [
            "privacy", "leak", "exfiltrat", "confidential", "secret",
            "private data", "intellectual property",
        ],
        "R6_authority_misuse": [
            "delegat", "authority", "authorization", "credential",
            "confused deputy", "tool misuse", "unauthorized action",
            "privilege",
        ],
        "R7_availability_cost": [
            "denial of service", "denial-of-service", "availability",
            "resource exhaustion", "latency", "blocking", "token cost",
            "overload",
        ],
    }
    tags = [name for name, terms in groups.items() if has_any(text, terms)]
    return ";".join(tags or ["unspecified"])


def dependence_class(text: str, prior_include: list[str]) -> str:
    if has_any(text, [
        "only exists", "defined only", "population spread", "collusion",
        "colluding", "coalition", "quorum",
    ]):
        return "structurally_multi_agent"
    if has_any(text, [
        "compose", "composition", "conjunctive", "benign fragments",
        "handoff chain", "delegation chain", "locally valid",
        "individually benign",
    ]):
        return "composition_induced"
    if has_any(text, [
        "amplif", "increase", "greater vulnerability", "propagat", "spread",
        "persistence", "cascade", "peer impact",
    ]):
        return "interaction_amplified"
    if prior_include:
        return "interaction_dependent_mechanism"
    return "unclear"


def contextual_role(text: str) -> str:
    if has_any(text, [
        "byzantine", "confused deputy", "capability system",
        "distributed consensus", "access control model",
    ]):
        return "classical_foundation"
    if has_any(text, SURVEY_TERMS):
        return "related_work"
    if has_any(text, [
        "mcp", "agent2agent", "a2a protocol", "oauth", "nist",
        "mitre atlas", "owasp", "standard", "protocol specification",
    ]):
        return "protocol_or_standard"
    if has_any(text, [
        "benchmark", "measurement", "metric", "evaluation methodology",
        "reproducib",
    ]):
        return "measurement_context"
    if has_any(text, ["incident", "cve-", "deployment", "real-world exploit", "breach"]):
        return "deployment_evidence"
    if has_any(text, LLM_TERMS) and has_any(text, DIRECT_SECURITY_TERMS) \
            and not has_any(text, MULTI_TERMS):
        return "single_agent_baseline"
    if has_any(text, [
        "agentic ai", "llm agent", "web agent", "tool-using agent",
    ]) and has_any(text, DIRECT_SECURITY_TERMS):
        return "agentic_security_context"
    if has_any(text, DEFENSE_TERMS):
        return "defense_analogy"
    return "related_work"


def section_for_role(role: str) -> str:
    return {
        "related_work": "Overview and Related Work",
        "classical_foundation": "System Model and Discussion",
        "single_agent_baseline": "Scope, Attacks, and Defenses",
        "agentic_security_context": "Introduction and Related Work",
        "protocol_or_standard": "System Model and Defenses",
        "measurement_context": "Evaluation",
        "deployment_evidence": "Introduction and Threat Model",
        "defense_analogy": "Defenses",
    }.get(role, "Related Work")


def review_work(
    queue_row: dict[str, str], records: list[dict[str, object]]
) -> dict[str, str]:
    source_text, abstract, paper_text, _ = collect_source_text(queue_row, records)
    text = source_text.lower()
    prior_include, prior_context, prior_exclude, canonical = prior_signals(
        records, queue_row
    )
    basis = evidence_basis(abstract, paper_text, records)
    publication_date = earliest_publication_date(queue_row, records)
    post_cutoff = bool(publication_date and publication_date > CUTOFF)
    citations, citation_source, citation_field = citation_information(
        records, queue_row
    )
    peer_reviewed, peer_basis = peer_review_information(records, queue_row)

    has_llm = has_any(text, LLM_TERMS)
    has_multi = has_any(text, MULTI_TERMS)
    direct_security = has_any(text, DIRECT_SECURITY_TERMS)
    soft_security = has_any(text, SOFT_SECURITY_TERMS)
    interaction = has_any(text, INTERACTION_TERMS)
    system_target = has_any(text, SYSTEM_TARGET_TERMS)
    external_application = has_any(text, EXTERNAL_APPLICATION_TERMS)
    survey = has_any(text, SURVEY_TERMS)

    scope_pass = False
    scope_reason = ""
    if post_cutoff:
        scope_reason = "No source version before the literature cutoff."
    elif prior_include and not (prior_exclude and not canonical):
        scope_pass = True
        scope_reason = (
            "Prior source review explicitly included the work as "
            "interaction-security evidence."
        )
    elif has_llm and has_multi and direct_security and interaction \
            and (system_target or count_terms(text, INTERACTION_TERMS) >= 2):
        if external_application and not system_target:
            scope_reason = (
                "Agents are used for an external security or application task; "
                "the protected property is not the multi-agent system itself."
            )
        elif basis == "title_metadata":
            scope_reason = (
                "The title suggests relevance, but no abstract or full-text "
                "evidence establishes the strict MAS-security scope."
            )
        else:
            scope_pass = True
            scope_reason = (
                "Source evidence identifies multiple LLM-backed agents, an "
                "inter-agent relation, and a security effect tied to that relation."
            )
    else:
        missing: list[str] = []
        if not has_llm:
            missing.append("LLM-backed agents")
        if not has_multi:
            missing.append("multiple agents")
        if not direct_security:
            missing.append("direct security property")
        if not interaction:
            missing.append("interaction-dependent mechanism")
        scope_reason = "Strict scope not established: missing " + ", ".join(
            missing or ["sufficient source evidence"]
        ) + "."

    mature = peer_reviewed == "yes" or citations > 10
    existing_category = clean(
        queue_row.get("current_primary_category", "")
        or queue_row.get("broad_role", "")
    )
    dominant = contribution(text, existing_category)
    role = ""

    if scope_pass:
        evidence_set = "set1_core" if mature else "set2_emerging"
        decision_reason = (
            f"Passed strict MAS-security scope. Maturity: "
            f"peer_reviewed={peer_reviewed}; frozen_citations={citations}. "
            + (
                "Meets the Set 1 union rule."
                if mature
                else "Retained as an emerging direction because it has not yet "
                     "met the Set 1 maturity rule."
            )
        )
    else:
        citation_worthy = (
            direct_security or soft_security or survey or bool(prior_context)
        ) and basis != "title_metadata"
        if citation_worthy and not post_cutoff:
            evidence_set = "set3_context"
            role = contextual_role(text)
            decision_reason = (
                scope_reason
                + " Retained only for background, comparison, or methodological "
                  "context."
            )
        else:
            evidence_set = "screened_out"
            decision_reason = scope_reason

    return {
        "work_key": clean(queue_row.get("work_key", "")),
        "canonical_paper_id": clean(queue_row.get("canonical_paper_id", "")),
        "title": clean(queue_row.get("title", "")),
        "publication_date": publication_date or clean(
            queue_row.get("publication_date", "")
        ),
        "year": publication_date[:4] if publication_date else clean(
            queue_row.get("year", "")
        ),
        "venue": clean(queue_row.get("venue", "")),
        "doi": normalize_doi(queue_row.get("doi", "")),
        "arxiv_id": normalize_arxiv(queue_row.get("arxiv_id", "")),
        "primary_url": clean(queue_row.get("primary_url", "")),
        "evidence_set": evidence_set,
        "strict_scope_pass": "yes" if scope_pass else "no",
        "scope_reason": scope_reason,
        "peer_reviewed": peer_reviewed,
        "peer_review_basis": peer_basis,
        "frozen_citation_count": str(citations),
        "citation_count_source": citation_source,
        "citation_count_field": citation_field,
        "citation_snapshot_date": REVIEW_DATE,
        "maturity_rule_pass": "yes" if mature else "no",
        "dominant_contribution": dominant,
        "interaction_interfaces": interaction_interfaces(text) if scope_pass else "",
        "risk_or_property": risk_tags(text) if scope_pass else "",
        "interaction_dependence": dependence_class(text, prior_include)
        if scope_pass else "",
        "emerging_direction": dominant if evidence_set == "set2_emerging" else "",
        "citation_role": role,
        "paper_section": section_for_role(role) if role else "",
        "evidence_basis": basis,
        "evidence_locator": evidence_locator(records),
        "source_files": " ; ".join(sorted({
            str(record["source_file"]) for record in records
        }))[:6000],
        "decision_reason": decision_reason,
        "previous_decision": clean(queue_row.get("decision", "")),
        "previous_category": existing_category,
        "reviewer": REVIEWER,
        "reviewed_at": REVIEW_DATE,
        "author_signoff_required": "yes",
    }


def update_readme(counts: dict[str, int]) -> None:
    text = f"""# Authoritative corpus views

The repository uses three evidence sets and one screened search ledger.

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | {counts['set1_core']:,} | Mature evidence used to build the systematization, counts, and headline findings. |
| `set2_emerging.csv` | {counts['set2_emerging']:,} | In-scope early work used only for emerging directions and open problems. |
| `set3_context.csv` | {counts['set3_context']:,} | Contextual citations. This set is not part of the MAS-security corpus. |
| `screened_out.csv` | {counts['screened_out']:,} | Search records outside the direct corpus and without an active citation role. |

Set 1 and Set 2 pass the same strict MAS-security scope gate. Set 1 then
satisfies the maturity rule: peer reviewed, or more than 10 citations in the
frozen citation snapshot. Set 3 supports background and comparison only.

`review_ledger.csv` records every decision and preserves the previous label.
`author_priority_review.csv` identifies promotions, downgrades, missing
full-text locators, and unclear interaction tags. The review is model-assisted;
all retained rows require named-author signoff before they can be described as
human verified.

The literature cutoff is {CUTOFF}. Citation counts are frozen on {REVIEW_DATE}.
OpenAlex is preferred, with Semantic Scholar used when OpenAlex has no count.
"""
    (CORPUS / "README.md").write_text(text, encoding="utf-8")


def write_validator() -> None:
    content = '''#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
FILES = {
    "set1_core": "set1_core.csv",
    "set2_emerging": "set2_emerging.csv",
    "set3_context": "set3_context.csv",
    "screened_out": "screened_out.csv",
}

def rows(name):
    with (C / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))

sets = {name: rows(filename) for name, filename in FILES.items()}
keys = {name: {row["work_key"] for row in data} for name, data in sets.items()}
for left in keys:
    for right in keys:
        if left < right and keys[left] & keys[right]:
            raise SystemExit(f"sets overlap: {left} and {right}")
ledger = rows("review_ledger.csv")
if set().union(*keys.values()) != {row["work_key"] for row in ledger}:
    raise SystemExit("sets do not partition review_ledger.csv")
if any(row["strict_scope_pass"] != "yes" for row in sets["set1_core"] + sets["set2_emerging"]):
    raise SystemExit("Set 1 or Set 2 contains a scope failure")
if any(row["maturity_rule_pass"] != "yes" for row in sets["set1_core"]):
    raise SystemExit("Set 1 contains an immature work")
if any(row["maturity_rule_pass"] == "yes" for row in sets["set2_emerging"]):
    raise SystemExit("Set 2 contains a work that meets the Set 1 maturity rule")
if any(not row["citation_role"] for row in sets["set3_context"]):
    raise SystemExit("Set 3 row lacks a citation role")
for old in ("primary.csv", "secondary.csv", "pending.csv", "exclude.csv", "review_queue.csv", "decision_ledger.csv"):
    if (C / old).exists():
        raise SystemExit(f"legacy active file remains: {old}")
manifest = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
actual = {name: len(data) for name, data in sets.items()}
if manifest["counts"] != actual:
    raise SystemExit("manifest counts do not match the CSV files")
print(f"Three-set corpus valid: Set 1={actual['set1_core']}, Set 2={actual['set2_emerging']}, Set 3={actual['set3_context']}, screened out={actual['screened_out']}")
'''
    path = ROOT / "scripts" / "validate_three_set_corpus.py"
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def main() -> int:
    queue_path = CORPUS / "review_queue.csv"
    if not queue_path.exists():
        raise SystemExit("corpus/review_queue.csv is required for the one-time migration")
    queue = read_csv(queue_path)
    if len(queue) != 2217:
        raise SystemExit(f"unexpected search-universe size: {len(queue)}")

    by_identifier, by_title, source_inventory = load_source_index()
    reviewed: list[dict[str, str]] = []
    for queue_row in queue:
        reviewed.append(review_work(
            queue_row,
            matched_records(queue_row, by_identifier, by_title),
        ))

    fields = list(reviewed[0].keys())
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in reviewed:
        grouped[row["evidence_set"]].append(row)

    if sum(len(grouped[name]) for name in FINAL_FILES) != len(reviewed):
        raise SystemExit("not every work received exactly one evidence-set decision")
    if any(row["strict_scope_pass"] != "yes"
           for row in grouped["set1_core"] + grouped["set2_emerging"]):
        raise SystemExit("scope failure entered Set 1 or Set 2")
    if any(row["maturity_rule_pass"] != "yes" for row in grouped["set1_core"]):
        raise SystemExit("immature work entered Set 1")
    if any(row["maturity_rule_pass"] == "yes" for row in grouped["set2_emerging"]):
        raise SystemExit("mature work remained in Set 2")

    for set_name, filename in FINAL_FILES.items():
        rows = sorted(
            grouped[set_name],
            key=lambda row: (row["year"], row["title"].lower(), row["work_key"]),
        )
        write_csv(CORPUS / filename, rows, fields)

    write_csv(
        CORPUS / "review_ledger.csv",
        sorted(reviewed, key=lambda row: row["work_key"]),
        fields,
    )

    priority: list[dict[str, str]] = []
    for row in reviewed:
        issues: list[str] = []
        if row["evidence_set"] == "set1_core" and row["evidence_basis"] not in {
            "full_text", "full_text_screen_record",
        }:
            issues.append("Set 1 lacks a direct full-text locator")
        if row["evidence_set"] in {"set1_core", "set2_emerging"} \
                and row["interaction_dependence"] == "unclear":
            issues.append("interaction-dependence tag is unclear")
        if row["previous_decision"] == "primary" \
                and row["evidence_set"] not in {"set1_core", "set2_emerging"}:
            issues.append("previous primary was downgraded")
        if row["previous_decision"] in {"secondary", "pending", "exclude"} \
                and row["evidence_set"] == "set1_core":
            issues.append("work was promoted to Set 1")
        if issues:
            priority.append({**row, "review_issues": "; ".join(issues)})

    priority_fields = fields + ["review_issues"]
    write_csv(CORPUS / "author_priority_review.csv", priority, priority_fields)

    counts = {name: len(grouped[name]) for name in FINAL_FILES}
    summary_rows: list[dict[str, object]] = [
        {"metric": "evidence_set", "label": name, "count": count}
        for name, count in counts.items()
    ]
    for set_name in ("set1_core", "set2_emerging"):
        for label, count in sorted(Counter(
            row["dominant_contribution"] for row in grouped[set_name]
        ).items()):
            summary_rows.append({
                "metric": f"{set_name}_contribution",
                "label": label,
                "count": count,
            })
    for label, count in sorted(Counter(
        row["citation_role"] for row in grouped["set3_context"]
    ).items()):
        summary_rows.append({
            "metric": "set3_citation_role", "label": label, "count": count,
        })
    summary_rows.append({
        "metric": "quality_control",
        "label": "author_priority_review",
        "count": len(priority),
    })
    write_csv(
        CORPUS / "summary.csv",
        [{key: str(value) for key, value in row.items()} for row in summary_rows],
        ["metric", "label", "count"],
    )

    for legacy in (
        "primary.csv", "secondary.csv", "pending.csv", "exclude.csv",
        "review_queue.csv", "decision_ledger.csv",
    ):
        path = CORPUS / legacy
        if path.exists():
            path.unlink()

    manifest = {
        "schema_version": 1,
        "literature_cutoff": CUTOFF,
        "citation_snapshot_date": REVIEW_DATE,
        "citation_threshold": "strictly greater than 10",
        "set1_maturity_rule": (
            "peer_reviewed == yes OR frozen_citation_count > 10"
        ),
        "search_universe": len(reviewed),
        "corpus_counts": {
            "set1_core": counts["set1_core"],
            "set2_emerging": counts["set2_emerging"],
            "total_corpus": counts["set1_core"] + counts["set2_emerging"],
        },
        "counts": counts,
        "set1_contributions": dict(Counter(
            row["dominant_contribution"] for row in grouped["set1_core"]
        )),
        "set2_contributions": dict(Counter(
            row["dominant_contribution"] for row in grouped["set2_emerging"]
        )),
        "set3_roles": dict(Counter(
            row["citation_role"] for row in grouped["set3_context"]
        )),
        "author_priority_review_count": len(priority),
        "reviewer": REVIEWER,
        "verification_note": (
            "Model-assisted source review. Named author signoff is required "
            "before claiming human verification."
        ),
        "source_file_inventory": source_inventory,
        "files": {},
    }
    for path in sorted(CORPUS.glob("*.csv")):
        manifest["files"][path.name] = {
            "sha256": file_hash(path),
            "rows": len(read_csv(path)),
        }
    (CORPUS / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    update_readme(counts)
    write_validator()
    shutil.rmtree(ROOT / ".bootstrap", ignore_errors=True)
    print(json.dumps(manifest["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
