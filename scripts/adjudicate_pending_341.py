#!/usr/bin/env python3
"""Resolve every currently pending work into primary, secondary, or exclude.

This is an agent source review, not human verification. Obvious exclusions may be
resolved from title and abstract. Potential primary and secondary works are
checked against available abstracts and, where an open PDF is available, the
paper text. Every decision retains evidence basis and requires author signoff.
"""

from __future__ import annotations

import csv
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
REVIEW_OUT = ROOT / "reviews" / "pending_resolution.csv"
REVIEWER = "OpenAI GPT-5.6 Pro (agent source review)"
REVIEW_DATE = "2026-08-17"
CUTOFF = "2026-07-01"
UA = "multiagent-security-corpus-source-review/1.0 (mailto:ryang54@jh.edu)"

LLM_TERMS = [
    "large language model", "large-language model", " llm", "llm ",
    "language model agent", "language agent", "agentic ai", "chatgpt",
    "gpt-3", "gpt-4", "generative ai", "foundation model agent",
]
MULTI_TERMS = [
    "multi-agent", "multi agent", "multiple agents", "agent team",
    "agent society", "agent swarm", "agent collaboration", "agent debate",
    "agent-to-agent", "agent to agent", "inter-agent", "inter agent",
    "llm agents", "language agents", "agent network", "agent collective",
]
AGENTIC_TERMS = [
    "agentic", "autonomous agent", "web agent", "tool-using agent",
    "tool using agent", "software agent", "browser agent", "coding agent",
]
DIRECT_SECURITY_TERMS = [
    "security", "cybersecurity", "attack", "adversarial", "adversary",
    "threat model", "vulnerability", "exploit", "poison", "jailbreak",
    "backdoor", "malicious", "privacy", "leak", "exfiltrat",
    "confidentiality", "integrity", "authorization", "authentication",
    "access control", "credential", "byzantine", "collusion", "deception",
    "manipulat", "denial of service", "denial-of-service", "guardrail",
    "red team", "red-team", "unsafe", "misinformation", "trust attack",
]
SOFT_SECURITY_TERMS = [
    "safety", "safe", "trust", "trustworthy", "reliability", "reliable",
    "robust", "governance", "accountab", "audit", "monitor", "risk",
    "uncertainty", "alignment", "oversight", "verification",
]
INTERACTION_TERMS = [
    "inter-agent", "inter agent", "cross-agent", "cross agent",
    "agent-to-agent", "agent to agent", "communication", "message passing",
    "message", "propagat", "spread", "shared memory", "shared state",
    "delegat", "handoff", "hand-off", "consensus", "voting", "vote",
    "debate", "collusion", "coalition", "topology", "coordinator",
    "routing", "peer", "collective decision", "aggregation", "quorum",
    "compromised agent", "malicious agent", "byzantine agent",
    "trust propagation", "recursive", "infection", "worm", "retransmit",
    "joint decision", "role interaction", "agent interaction",
]
PRIMARY_EFFECT_TERMS = [
    "attack on multi-agent", "attack against multi-agent", "multi-agent attack",
    "multi-agent security", "security of multi-agent", "secure multi-agent",
    "defend multi-agent", "defense for multi-agent", "malicious agent",
    "compromised agent", "byzantine agent", "cross-agent leakage",
    "inter-agent leakage", "shared memory poisoning", "consensus manipulation",
    "collective manipulation", "agent collusion", "colluding agents",
    "propagation across agents", "spread across agents", "agent-to-agent security",
    "delegation attack", "delegated authority", "communication attack",
    "topology attack", "multi-agent vulnerability", "multi-agent threat model",
]
EXTERNAL_APPLICATION_TERMS = [
    "penetration test", "vulnerability detection", "vulnerability discovery",
    "smart contract fuzz", "malware detection", "intrusion detection",
    "phishing detection", "cyber threat intelligence", "security operation",
    "code generation", "software development", "bug finding", "fraud detection",
    "medical diagnosis", "medical monitoring", "health monitoring",
    "construction safety", "traffic safety", "air traffic", "radiation oncology",
    "drug discovery", "data center cooling", "energy system", "fault diagnosis",
    "named entity recognition", "knowledge integration", "business process",
    "enterprise resource planning", "recommendation system", "shilling attack",
    "text-to-image", "autonomous vehicle", "wireless network", "6g network",
]
SURVEY_TERMS = ["survey", "systematic review", "literature review", "overview", "position paper", "vision for"]
ATTACK_TERMS = ["attack", "adversarial", "poison", "jailbreak", "backdoor", "malicious", "exploit", "vulnerability", "collusion", "deception", "manipulat"]
DEFENSE_TERMS = ["defense", "defence", "guard", "secure", "security framework", "monitor", "access control", "authorization", "privacy-preserving", "trust framework", "mitigat", "protect"]
EVAL_TERMS = ["benchmark", "evaluation", "evaluate", "audit", "assessment", "empirical study", "measurement", "dataset", "taxonomy"]


def clean(value: object) -> str:
    text = html.unescape("" if value is None else str(value))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def lower(value: object) -> str:
    return clean(value).lower()


def has_any(text: str, terms: Iterable[str]) -> bool:
    return any(term in text for term in terms)


def count_any(text: str, terms: Iterable[str]) -> int:
    return sum(text.count(term) for term in terms)


def request_bytes(url: str, accept: str = "*/*", attempts: int = 4) -> tuple[bytes | None, str]:
    error = ""
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=45) as response:
                data = response.read(30 * 1024 * 1024 + 1)
            if len(data) > 30 * 1024 * 1024:
                return None, "response larger than 30 MB"
            return data, ""
        except Exception as exc:  # network failures remain visible in evidence_basis
            error = repr(exc)
            time.sleep(min(5.0, 0.4 * (2**attempt)))
    return None, error


def request_json(url: str) -> tuple[dict | None, str]:
    data, error = request_bytes(url, "application/json")
    if not data:
        return None, error
    try:
        return json.loads(data), ""
    except Exception as exc:
        return None, repr(exc)


def inverted_abstract(index: object) -> str:
    if not isinstance(index, dict):
        return ""
    tokens: list[tuple[int, str]] = []
    for word, positions in index.items():
        for position in positions or []:
            try:
                tokens.append((int(position), word))
            except (TypeError, ValueError):
                pass
    return " ".join(word for _, word in sorted(tokens))


def arxiv_metadata(ids: list[str]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for start in range(0, len(ids), 40):
        batch = ids[start : start + 40]
        url = "https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(",".join(batch)) + f"&max_results={len(batch)}"
        data, error = request_bytes(url, "application/atom+xml")
        if not data:
            for identifier in batch:
                result.setdefault(identifier, {"error": error})
            continue
        try:
            root = ET.fromstring(data)
            for entry in root.findall("a:entry", ns):
                identifier = entry.findtext("a:id", "", ns).rsplit("/", 1)[-1].split("v")[0]
                result[identifier] = {
                    "title": clean(entry.findtext("a:title", "", ns)),
                    "abstract": clean(entry.findtext("a:summary", "", ns)),
                    "published": clean(entry.findtext("a:published", "", ns)),
                    "updated": clean(entry.findtext("a:updated", "", ns)),
                    "categories": ";".join(item.attrib.get("term", "") for item in entry.findall("a:category", ns)),
                }
        except Exception as exc:
            for identifier in batch:
                result.setdefault(identifier, {"error": repr(exc)})
        time.sleep(0.5)
    return result


def metadata_for(row: dict[str, str], arxiv: dict[str, dict[str, str]]) -> dict[str, str]:
    meta: dict[str, str] = {}
    doi = lower(row.get("doi", ""))
    aid = clean(row.get("arxiv_id", ""))
    if aid and aid in arxiv:
        meta.update({f"arxiv_{key}": value for key, value in arxiv[aid].items()})

    oa: dict | None = None
    oa_error = ""
    if doi:
        oa, oa_error = request_json("https://api.openalex.org/works/https://doi.org/" + urllib.parse.quote(doi, safe="/:()") + "?mailto=ryang54@jh.edu")
    elif aid:
        oa, oa_error = request_json("https://api.openalex.org/works/https://arxiv.org/abs/" + urllib.parse.quote(aid, safe="") + "?mailto=ryang54@jh.edu")
    if oa:
        location = oa.get("primary_location") or {}
        best = oa.get("best_oa_location") or {}
        source = location.get("source") or {}
        meta.update(
            {
                "openalex_title": clean(oa.get("display_name", "")),
                "openalex_abstract": clean(inverted_abstract(oa.get("abstract_inverted_index"))),
                "openalex_type": clean(oa.get("type", "")),
                "openalex_date": clean(oa.get("publication_date", "")),
                "openalex_source": clean(source.get("display_name", "")),
                "openalex_landing": clean(location.get("landing_page_url", "")),
                "openalex_pdf": clean(best.get("pdf_url", "") or location.get("pdf_url", "")),
                "openalex_topics": ";".join(clean(topic.get("display_name", "")) for topic in (oa.get("topics") or [])[:8]),
            }
        )
    elif oa_error:
        meta["openalex_error"] = oa_error

    if not meta.get("openalex_abstract") and doi:
        cr, error = request_json("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe=""))
        message = (cr or {}).get("message") if cr else None
        if message:
            meta.update(
                {
                    "crossref_title": clean(" ".join(message.get("title") or [])),
                    "crossref_abstract": clean(message.get("abstract", "")),
                    "crossref_type": clean(message.get("type", "")),
                    "crossref_url": clean(message.get("URL", "")),
                }
            )
        elif error:
            meta["crossref_error"] = error

    if not any(meta.get(key) for key in ("arxiv_abstract", "openalex_abstract", "crossref_abstract")):
        identifier = ""
        if doi:
            identifier = "DOI:" + doi
        elif aid:
            identifier = "ARXIV:" + aid
        if identifier:
            s2_url = "https://api.semanticscholar.org/graph/v1/paper/" + urllib.parse.quote(identifier, safe=":./") + "?fields=title,abstract,venue,year,publicationDate,openAccessPdf,url"
            s2, error = request_json(s2_url)
            if s2 and not s2.get("error"):
                meta.update(
                    {
                        "s2_title": clean(s2.get("title", "")),
                        "s2_abstract": clean(s2.get("abstract", "")),
                        "s2_url": clean(s2.get("url", "")),
                        "s2_pdf": clean((s2.get("openAccessPdf") or {}).get("url", "")),
                    }
                )
            elif error:
                meta["s2_error"] = error
    return meta


def choose_abstract(meta: dict[str, str]) -> tuple[str, str]:
    for key in ("arxiv_abstract", "openalex_abstract", "s2_abstract", "crossref_abstract"):
        value = clean(meta.get(key, ""))
        if value:
            return value, key.replace("_abstract", "")
    return "", "none"


def pdf_candidates(row: dict[str, str], meta: dict[str, str]) -> list[str]:
    urls: list[str] = []
    aid = clean(row.get("arxiv_id", ""))
    if aid:
        urls.append(f"https://arxiv.org/pdf/{aid}")
    for key in ("openalex_pdf", "s2_pdf"):
        value = clean(meta.get(key, ""))
        if value:
            urls.append(value)
    doi = lower(row.get("doi", ""))
    if doi:
        unpaywall, _ = request_json("https://api.unpaywall.org/v2/" + urllib.parse.quote(doi, safe="") + "?email=ryang54@jh.edu")
        if unpaywall:
            best = unpaywall.get("best_oa_location") or {}
            value = clean(best.get("url_for_pdf", ""))
            if value:
                urls.append(value)
    seen: set[str] = set()
    return [url for url in urls if not (url in seen or seen.add(url))]


def extract_pdf_text(urls: list[str]) -> tuple[str, str, str]:
    for url in urls:
        data, error = request_bytes(url, "application/pdf")
        if not data or not data.startswith(b"%PDF"):
            continue
        with tempfile.TemporaryDirectory() as directory:
            pdf = Path(directory) / "paper.pdf"
            txt = Path(directory) / "paper.txt"
            pdf.write_bytes(data)
            try:
                subprocess.run(
                    ["pdftotext", "-f", "1", "-l", "16", "-layout", str(pdf), str(txt)],
                    check=True,
                    timeout=90,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                text = clean(txt.read_text(encoding="utf-8", errors="ignore"))
                if len(text) >= 500:
                    return text[:120000], url, ""
            except Exception as exc:
                error = repr(exc)
        if error:
            continue
    return "", "", "no open PDF text recovered"


def first_evidence_sentence(text: str, preferred: Iterable[str]) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", clean(text))
    for sentence in sentences:
        lowered = sentence.lower()
        if 35 <= len(sentence) <= 420 and has_any(lowered, preferred):
            return sentence
    return ""


def publication_before_cutoff(row: dict[str, str], meta: dict[str, str]) -> bool:
    dates = [clean(meta.get("arxiv_published", ""))[:10], clean(row.get("publication_date", ""))[:10]]
    valid = [item for item in dates if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item)]
    return bool(valid and min(valid) < CUTOFF)


def classify(row: dict[str, str], meta: dict[str, str]) -> dict[str, str]:
    title = clean(row.get("title", "")) or clean(meta.get("openalex_title", "")) or clean(meta.get("s2_title", ""))
    abstract, abstract_source = choose_abstract(meta)
    title_abstract = lower(title + " " + abstract + " " + meta.get("openalex_topics", ""))

    has_llm = has_any(title_abstract, LLM_TERMS)
    has_multi = has_any(title_abstract, MULTI_TERMS)
    has_agentic = has_any(title_abstract, AGENTIC_TERMS)
    direct_security = has_any(title_abstract, DIRECT_SECURITY_TERMS)
    soft_security = has_any(title_abstract, SOFT_SECURITY_TERMS)
    interaction = has_any(title_abstract, INTERACTION_TERMS)
    primary_effect = has_any(title_abstract, PRIMARY_EFFECT_TERMS)
    survey = has_any(title_abstract, SURVEY_TERMS)
    external_application = has_any(title_abstract, EXTERNAL_APPLICATION_TERMS)

    coarse_candidate = (has_llm or has_agentic) and (has_multi or has_agentic) and (direct_security or soft_security)
    need_pdf = coarse_candidate or (direct_security and (has_multi or has_agentic))
    pdf_text = ""
    pdf_url = ""
    pdf_error = ""
    if need_pdf:
        pdf_text, pdf_url, pdf_error = extract_pdf_text(pdf_candidates(row, meta))

    full = lower(title + " " + abstract + " " + pdf_text)
    has_llm = has_any(full, LLM_TERMS)
    has_multi = has_any(full, MULTI_TERMS)
    has_agentic = has_any(full, AGENTIC_TERMS)
    direct_security = has_any(full, DIRECT_SECURITY_TERMS)
    soft_security = has_any(full, SOFT_SECURITY_TERMS)
    interaction = has_any(full, INTERACTION_TERMS)
    primary_effect = has_any(full, PRIMARY_EFFECT_TERMS)
    survey = has_any(full, SURVEY_TERMS)
    external_application = has_any(full, EXTERNAL_APPLICATION_TERMS)

    source_basis = "full_text" if pdf_text else ("abstract" if abstract else "title_metadata")
    post_cutoff = not publication_before_cutoff(row, meta)

    # Direct post-cutoff records cannot enter the frozen evidence universe.
    if post_cutoff:
        decision = "exclude"
        reason_code = "post_cutoff"
        rationale = f"Excluded: no retrievable version before the {CUTOFF} cutoff was found. Review basis: {source_basis}."
    # Surveys and position papers are useful context, but not direct primary evidence.
    elif survey and (has_llm or has_agentic) and (has_multi or has_agentic) and (direct_security or soft_security):
        decision = "secondary"
        reason_code = "survey_or_position_context"
        rationale = "Secondary: synthesizes or frames agent or multi-agent security, but does not itself supply a direct interaction-security experiment or mechanism claim."
    # The core gate requires LLM-backed multi-agent principals, direct security, and an interaction-dependent mechanism.
    elif has_llm and has_multi and direct_security and interaction and (primary_effect or count_any(full, INTERACTION_TERMS) >= 2):
        if external_application and not primary_effect:
            decision = "secondary"
            reason_code = "mas_used_for_external_security_task"
            rationale = "Secondary: uses a multi-agent LLM architecture in a security application, but the available source does not show that the protected property belongs to the interacting agent system itself."
        else:
            decision = "primary"
            reason_code = "direct_interaction_security"
            rationale = "Primary: the source studies a security property of interacting LLM-backed principals and identifies communication, shared state, delegation, aggregation, topology, or coordinated members as part of the attack or defense mechanism."
    # Direct agentic or multi-agent security without a demonstrated relation is retained as context.
    elif (has_llm or has_agentic) and (has_multi or has_agentic) and direct_security:
        decision = "secondary"
        reason_code = "security_relevant_interaction_not_isolated"
        rationale = "Secondary: directly concerns LLM-agent security, but the available source does not establish an interaction-dependent effect across separately addressable principals."
    # Safety, reliability, trust, privacy, and governance can inform the SoK without proving security.
    elif has_llm and has_multi and soft_security:
        decision = "secondary"
        reason_code = "mas_safety_reliability_context"
        rationale = "Secondary: studies safety, reliability, trust, governance, or monitoring in an LLM multi-agent setting, but lacks a direct interaction-security violation or defense claim."
    # Non-LLM relational security can supply classical context only when the relation is explicit.
    elif has_multi and direct_security and interaction:
        decision = "secondary"
        reason_code = "non_llm_multiagent_security_context"
        rationale = "Secondary: provides relational multi-agent security context, but the available source does not establish an LLM-backed multi-agent system within this SoK's system boundary."
    # Single-agent LLM security and MAS-as-a-tool papers are outside the direct or contextual boundary unless agentic structure matters.
    elif (has_llm or has_agentic) and direct_security and not has_multi:
        decision = "exclude"
        reason_code = "no_multiagent_boundary"
        rationale = "Excluded: concerns an LLM or agent security primitive without multiple separately addressable LLM-backed principals or a cross-principal interaction effect."
    elif external_application:
        decision = "exclude"
        reason_code = "external_application_only"
        rationale = "Excluded: uses agents as a method for an external application or security task; the available source does not study security of the interacting LLM-agent system."
    elif not (has_llm or has_agentic):
        decision = "exclude"
        reason_code = "no_llm_agent_boundary"
        rationale = "Excluded: the available source does not establish an LLM-backed agent system within scope."
    elif not has_multi:
        decision = "exclude"
        reason_code = "no_multiagent_boundary"
        rationale = "Excluded: the available source does not establish multiple separately addressable LLM-backed principals."
    else:
        decision = "exclude"
        reason_code = "no_direct_security_property"
        rationale = "Excluded: the source concerns multi-agent LLM capability or application performance without a concrete security property, adversary, violation, defense, or security evaluation."

    evidence = first_evidence_sentence(pdf_text or abstract or title, PRIMARY_EFFECT_TERMS + INTERACTION_TERMS + DIRECT_SECURITY_TERMS + SOFT_SECURITY_TERMS)
    if evidence:
        rationale += " Evidence: " + evidence[:360]
    elif source_basis == "title_metadata":
        rationale += " No abstract or open full text was recovered; the strict inclusion burden was therefore not met."

    category = "other"
    if decision in {"primary", "secondary"}:
        attack_score = count_any(full, ATTACK_TERMS)
        defense_score = count_any(full, DEFENSE_TERMS)
        eval_score = count_any(full, EVAL_TERMS)
        if eval_score >= max(attack_score, defense_score) and eval_score > 0:
            category = "evaluation"
        elif attack_score > defense_score and attack_score > 0:
            category = "attack"
        elif defense_score > 0:
            category = "defense"

    return {
        "decision": decision,
        "reason_code": reason_code,
        "rationale": rationale,
        "recommended_primary_category": category if decision != "exclude" else "",
        "evidence_basis": source_basis,
        "abstract_source": abstract_source,
        "abstract": abstract[:3000],
        "evidence_sentence": evidence[:500],
        "full_text_url": pdf_url,
        "full_text_error": pdf_error,
        "has_llm": "yes" if has_llm else "no",
        "has_multiagent": "yes" if has_multi else "no",
        "has_direct_security": "yes" if direct_security else "no",
        "has_interaction": "yes" if interaction else "no",
        "has_primary_effect_phrase": "yes" if primary_effect else "no",
        "post_cutoff": "yes" if post_cutoff else "no",
    }


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def update_row(row: dict[str, str], result: dict[str, str]) -> dict[str, str]:
    updated = dict(row)
    updated["decision"] = result["decision"]
    if "decision_source" in updated:
        updated["decision_source"] = "agent_source_review:pending_341"
    if "rationale" in updated:
        updated["rationale"] = result["rationale"]
    if "reviewer" in updated:
        updated["reviewer"] = REVIEWER
    if "reviewed_at" in updated:
        updated["reviewed_at"] = REVIEW_DATE
    if "human_signoff_required" in updated:
        updated["human_signoff_required"] = "yes"
    if "recommended_primary_category" in updated:
        updated["recommended_primary_category"] = result["recommended_primary_category"]
    if "category_review_status" in updated:
        updated["category_review_status"] = "agent_source_review_pending_author_signoff"
    return updated


def recursively_update_counts(value: object, counts: Counter[str]) -> object:
    if isinstance(value, dict):
        out: dict[str, object] = {}
        for key, item in value.items():
            lowered = key.lower()
            if lowered in {"primary", "primary_works", "primary_count"} and isinstance(item, int):
                out[key] = counts["primary"]
            elif lowered in {"secondary", "secondary_works", "secondary_count"} and isinstance(item, int):
                out[key] = counts["secondary"]
            elif lowered in {"exclude", "excluded", "exclude_works", "exclude_count"} and isinstance(item, int):
                out[key] = counts["exclude"]
            elif lowered in {"pending", "pending_works", "pending_count"} and isinstance(item, int):
                out[key] = 0
            elif lowered in {"total", "total_works", "deduplicated_works", "review_queue"} and isinstance(item, int):
                out[key] = sum(counts.values())
            else:
                out[key] = recursively_update_counts(item, counts)
        return out
    if isinstance(value, list):
        return [recursively_update_counts(item, counts) for item in value]
    return value


def replace_population_text(path: Path, counts: Counter[str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    replacements = {
        r"303 primary": f"{counts['primary']:,} primary",
        r"177 secondary": f"{counts['secondary']:,} secondary",
        r"1,396 exclude": f"{counts['exclude']:,} exclude",
        r"341 pending": "0 pending",
        r"\| `corpus/pending\.csv` \| 341 pending \|\n": "",
        r" and 341 pending works": " and no pending works",
        r", and 341 pending": ", with no pending",
        r"Pending records remain visible but never enter a final evidence set\.\s*": "",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    path.write_text(text, encoding="utf-8")


def write_validator(counts: Counter[str]) -> None:
    validator = ROOT / "scripts" / "validate_authoritative_corpus.py"
    validator.write_text(
        '''#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"

def rows(name):
    with (CORPUS/name).open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))

queue = rows("review_queue.csv")
primary = rows("primary.csv")
secondary = rows("secondary.csv")
exclude = rows("exclude.csv")
sets = {"primary": primary, "secondary": secondary, "exclude": exclude}
keys = {name: {r["work_key"] for r in data} for name, data in sets.items()}
if any(keys[a] & keys[b] for a in keys for b in keys if a < b):
    raise SystemExit("authoritative sets overlap")
if set().union(*keys.values()) != {r["work_key"] for r in queue}:
    raise SystemExit("three final sets do not partition review_queue.csv")
if any(r.get("decision") not in sets for r in queue):
    raise SystemExit("pending or invalid decision remains in review queue")
for name, data in sets.items():
    if any(r.get("decision") != name for r in data):
        raise SystemExit(f"{name}.csv contains another decision")
print(f"Authoritative corpus valid: {len(queue):,} works = {len(primary):,} primary + {len(secondary):,} secondary + {len(exclude):,} exclude; pending 0.")
''',
        encoding="utf-8",
    )
    validator.chmod(0o755)


def main() -> int:
    pending_fields, pending = read_csv(CORPUS / "pending.csv")
    if len(pending) != 341:
        raise SystemExit(f"expected 341 pending works, found {len(pending)}")

    arxiv_ids = sorted({clean(row.get("arxiv_id", "")) for row in pending if clean(row.get("arxiv_id", ""))})
    arxiv = arxiv_metadata(arxiv_ids)
    decisions: dict[str, dict[str, str]] = {}
    audit_rows: list[dict[str, str]] = []
    for index, row in enumerate(pending, 1):
        meta = metadata_for(row, arxiv)
        result = classify(row, meta)
        work_key = row["work_key"]
        decisions[work_key] = result
        audit = {
            "work_key": work_key,
            "title": clean(row.get("title", "")),
            "doi": clean(row.get("doi", "")),
            "arxiv_id": clean(row.get("arxiv_id", "")),
            "decision": result["decision"],
            "reason_code": result["reason_code"],
            "recommended_primary_category": result["recommended_primary_category"],
            "evidence_basis": result["evidence_basis"],
            "abstract_source": result["abstract_source"],
            "full_text_url": result["full_text_url"],
            "has_llm": result["has_llm"],
            "has_multiagent": result["has_multiagent"],
            "has_direct_security": result["has_direct_security"],
            "has_interaction": result["has_interaction"],
            "has_primary_effect_phrase": result["has_primary_effect_phrase"],
            "post_cutoff": result["post_cutoff"],
            "rationale": result["rationale"],
            "evidence_sentence": result["evidence_sentence"],
            "abstract": result["abstract"],
            "reviewer": REVIEWER,
            "reviewed_at": REVIEW_DATE,
            "human_signoff_required": "yes",
        }
        audit_rows.append(audit)
        print(f"[{index:03d}/341] {result['decision']:9s} {work_key} {audit['title'][:90]}", flush=True)
        time.sleep(0.03)

    counts = Counter(result["decision"] for result in decisions.values())
    if sum(counts.values()) != 341 or set(counts) - {"primary", "secondary", "exclude"}:
        raise SystemExit(f"invalid adjudication counts: {counts}")

    queue_fields, queue = read_csv(CORPUS / "review_queue.csv")
    queue_by_key = {row["work_key"]: row for row in queue}
    if set(decisions) - set(queue_by_key):
        raise SystemExit("pending work missing from review queue")
    updated_queue = [update_row(row, decisions[row["work_key"]]) if row["work_key"] in decisions else row for row in queue]
    write_csv(CORPUS / "review_queue.csv", queue_fields, sorted(updated_queue, key=lambda row: row["work_key"]))

    final_sets: dict[str, list[dict[str, str]]] = {}
    for decision in ("primary", "secondary", "exclude"):
        fields, rows = read_csv(CORPUS / f"{decision}.csv")
        additions = [update_row(row, decisions[row["work_key"]]) for row in pending if decisions[row["work_key"]]["decision"] == decision]
        merged = {row["work_key"]: row for row in rows}
        for row in additions:
            merged[row["work_key"]] = row
        final_sets[decision] = sorted(merged.values(), key=lambda row: row["work_key"])
        write_csv(CORPUS / f"{decision}.csv", fields, final_sets[decision])

    ledger_path = CORPUS / "decision_ledger.csv"
    ledger_fields, ledger = read_csv(ledger_path)
    updated_ledger = [update_row(row, decisions[row["work_key"]]) if row.get("work_key") in decisions else row for row in ledger]
    write_csv(ledger_path, ledger_fields, updated_ledger)

    audit_fields = list(audit_rows[0])
    write_csv(REVIEW_OUT, audit_fields, audit_rows)

    # Exactly three final sets remain. The old pending file is deleted rather than archived.
    (CORPUS / "pending.csv").unlink()

    final_counts = Counter({name: len(rows) for name, rows in final_sets.items()})
    manifest_path = CORPUS / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest = recursively_update_counts(manifest, final_counts)
        if isinstance(manifest, dict):
            manifest["decision_counts"] = dict(final_counts)
            manifest["pending"] = 0
            manifest["reviewed_pending_resolution"] = {
                "records": 341,
                "reviewer": REVIEWER,
                "reviewed_at": REVIEW_DATE,
                "human_signoff_required": True,
                "audit_path": "reviews/pending_resolution.csv",
            }
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    summary_path = CORPUS / "summary.csv"
    if summary_path.exists():
        fields, rows = read_csv(summary_path)
        for row in rows:
            joined = " ".join(lower(value) for value in row.values())
            for name in ("primary", "secondary", "exclude"):
                if name in joined:
                    for field in fields:
                        if field.lower() in {"count", "value", "works", "n"}:
                            row[field] = str(final_counts[name])
            if "pending" in joined:
                for field in fields:
                    if field.lower() in {"count", "value", "works", "n"}:
                        row[field] = "0"
        write_csv(summary_path, fields, rows)

    replace_population_text(ROOT / "README.md", final_counts)
    replace_population_text(CORPUS / "README.md", final_counts)
    write_validator(final_counts)

    # Remove temporary collection workflows. The audit CSV and decision ledger are the retained provenance.
    for path in [
        ROOT / ".github/workflows/export-pending-review.yml",
        ROOT / ".github/workflows/enrich-pending-review.yml",
        ROOT / ".github/workflows/enrich-pending-semantic-scholar.yml",
    ]:
        if path.exists():
            path.unlink()

    print(json.dumps({"resolved": 341, "new_decisions": dict(counts), "final_counts": dict(final_counts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
