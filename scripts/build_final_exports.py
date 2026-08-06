#!/usr/bin/env python3
"""Build cutoff-frozen, auditable corpus exports from reviewed source records."""

from __future__ import annotations

import csv
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CUTOFF = "2026-07-01"
SNAPSHOT = "2026-08-06"


SUPPLEMENTAL_PEER = {
    "Teaching Models to Balance Resisting and Accepting Persuasion": {
        "authors": "Elias Stengel-Eskin; Peter Hase; Mohit Bansal",
        "year": "2025",
        "venue": "NAACL 2025",
        "doi": "10.18653/v1/2025.naacl-long.412",
        "url": "https://aclanthology.org/2025.naacl-long.412/",
        "role": "defense; evaluation",
        "scope": "security_relevant",
        "dependency": "Adversarial persuasion and resistance are evaluated in recursive dialogues and multi-agent debate.",
    },
    "Reproducibility Study of Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation": {
        "authors": "Jose L. Garcia; Karolina Hajkova; Maria Marchenko; Carlos Miguel Patino",
        "year": "2025",
        "venue": "Transactions on Machine Learning Research",
        "doi": "",
        "url": "https://openreview.net/forum?id=MTrhFmkC45",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "The study reproduces maliciousness, information leakage, and fairness effects in interacting LLM stakeholders.",
    },
    "Deliberation and drift: Evaluating alignment fragility in multi-agent medical artificial intelligence": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "AI and Ethics",
        "doi": "10.1007/s43681-026-01048-9",
        "url": "https://doi.org/10.1007/s43681-026-01048-9",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "Alignment fragility is evaluated as an effect of multi-agent deliberation.",
    },
    "Enhancing Robustness of LLM-Driven Multi-Agent Systems through Randomized Smoothing": {
        "authors": "Jinwei Hu; Yi Dong; Zhengtao Ding; Xiaowei Huang",
        "year": "2026",
        "venue": "Chinese Journal of Aeronautics",
        "doi": "10.1016/j.cja.2025.103779",
        "url": "https://doi.org/10.1016/j.cja.2025.103779",
        "role": "defense; evaluation",
        "scope": "core_security",
        "dependency": "The threat and defense act on malicious messages and consensus propagation in a ring of LLM agents.",
    },
    "Evaluating Multi-Agent Defences Against Jailbreaking Attacks on Large Language Models": {
        "authors": "Not reported in current export",
        "year": "2025",
        "venue": "FLLM 2025",
        "doi": "10.1109/FLLM67465.2025.11391246",
        "url": "https://doi.org/10.1109/FLLM67465.2025.11391246",
        "role": "defense; evaluation",
        "scope": "core_security",
        "dependency": "The paper evaluates a multi-agent defense configuration against jailbreak attacks.",
    },
    "PeerGuard: Defending Multi-Agent Systems Against Backdoor Attacks Through Mutual Reasoning": {
        "authors": "Falong Fan; Xi Li",
        "year": "2025",
        "venue": "IEEE IRI 2025",
        "doi": "10.1109/IRI66576.2025.00051",
        "url": "https://doi.org/10.1109/IRI66576.2025.00051",
        "role": "defense; evaluation",
        "scope": "core_security",
        "dependency": "Agents mutually inspect peer reasoning to detect a backdoored member.",
    },
    "Decentralized Multi-Agent System with Trust-Aware Communication": {
        "authors": "Not reported in current export",
        "year": "2025",
        "venue": "IEEE ISPA 2025",
        "doi": "10.1109/ISPA67752.2025.00198",
        "url": "https://doi.org/10.1109/ISPA67752.2025.00198",
        "role": "defense",
        "scope": "security_relevant",
        "dependency": "Trust scores govern communication among decentralized agents.",
    },
    "ATAG: AI-Agent Application Threat Assessment with Attack Graphs": {
        "authors": "Parth Atulbhai Gandhi; David Tayouri; Akansha Shukla; Beni Ifland; Yuval Elovici; Rami Puzis; Asaf Shabtai",
        "year": "2026",
        "venue": "ACM AsiaCCS 2026",
        "doi": "10.1145/3779208.3785380",
        "url": "https://doi.org/10.1145/3779208.3785380",
        "role": "threat modeling; evaluation",
        "scope": "security_relevant",
        "dependency": "Attack graphs model compromise paths across agentic application components and interactions.",
    },
    "SafeSieve: From Heuristics to Experience in Progressive Pruning for LLM-based Multi-Agent Communication": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "AAAI 2026",
        "doi": "10.1609/aaai.v40i35.40236",
        "url": "https://doi.org/10.1609/aaai.v40i35.40236",
        "role": "defense; evaluation",
        "scope": "core_security",
        "dependency": "The defense prunes unsafe or unreliable inter-agent communication.",
    },
    "CoMet: Metaphor-Driven Covert Communication for Multi-Agent Language Games": {
        "authors": "Shuxiang Xu; Fangwei Zhong",
        "year": "2025",
        "venue": "ACL 2025",
        "doi": "10.18653/v1/2025.acl-long.389",
        "url": "https://aclanthology.org/2025.acl-long.389/",
        "role": "attack; evaluation",
        "scope": "core_security",
        "dependency": "Multiple agents establish covert communication through metaphor in language games.",
    },
    "Understanding the Information Propagation Effects of Communication Topologies in LLM-based Multi-Agent Systems": {
        "authors": "Xu Shen; Yixin Liu; Yiwei Dai; Yili Wang; Rui Miao; Yue Tan; Shirui Pan; Xin Wang",
        "year": "2025",
        "venue": "EMNLP 2025",
        "doi": "10.18653/v1/2025.emnlp-main.623",
        "url": "https://aclanthology.org/2025.emnlp-main.623/",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "The measured effect is information propagation under different communication graphs.",
    },
    "Safe in Isolation, Dangerous Together: Agent-Driven Multi-Turn Decomposition Jailbreaks on LLMs": {
        "authors": "Devansh Srivastav; Xiao Yu Zhang",
        "year": "2025",
        "venue": "REALM Workshop at ACL 2025",
        "doi": "10.18653/v1/2025.realm-1.13",
        "url": "https://aclanthology.org/2025.realm-1.13/",
        "role": "attack; evaluation",
        "scope": "core_security",
        "dependency": "A team of agents decomposes a harmful request into individually benign-looking turns.",
    },
    "The Adaptive Interrogator: Detecting Trojan LLMs in Multi-Agent Systems via Evolved Conversational Strategies": {
        "authors": "Rana Muhammad Shahroz Khan; Ruichen Zhang; Zhen Tan; Charles Fleming; Tianlong Chen",
        "year": "2026",
        "venue": "Findings of ACL 2026",
        "doi": "10.18653/v1/2026.findings-acl.1348",
        "url": "https://aclanthology.org/2026.findings-acl.1348/",
        "role": "defense; evaluation",
        "scope": "core_security",
        "dependency": "An interrogator agent uses interaction strategies to identify Trojan members.",
    },
    "From Tasks to Teams: A Risk-First Evaluation Framework for Multi-Agent LLM Systems in Finance": {
        "authors": "Zichen Chen; Jianda Chen; Jiaao Chen; Misha Sra",
        "year": "2026",
        "venue": "Findings of ACL 2026",
        "doi": "10.18653/v1/2026.findings-acl.1934",
        "url": "https://aclanthology.org/2026.findings-acl.1934/",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "The evaluation targets risks that emerge at team and workflow level in a financial MAS.",
    },
    "The Subtle Art of Defection: Understanding Uncooperative Behaviors in LLM based Multi-Agent Systems": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "ACL 2026",
        "doi": "10.48448/bp60-8m40",
        "url": "https://doi.org/10.48448/bp60-8m40",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "Defection is defined through strategic behavior among interacting agents.",
    },
    "Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation": {
        "authors": "Not reported in current export",
        "year": "2024",
        "venue": "NeurIPS 2024",
        "doi": "10.52202/079017-2658",
        "url": "https://doi.org/10.52202/079017-2658",
        "role": "evaluation",
        "scope": "security_relevant",
        "dependency": "Maliciousness and information sharing are measured in multi-party negotiation.",
    },
    "AI Agents with Decentralized Identifiers and Verifiable Credentials": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "ICAART 2026",
        "doi": "10.5220/0014234400004052",
        "url": "https://doi.org/10.5220/0014234400004052",
        "role": "defense; protocol",
        "scope": "security_relevant",
        "dependency": "DIDs and verifiable credentials bind identities in agent-to-agent interactions.",
    },
    "A Trace-Based Assurance Framework for Agentic AI Orchestration: Contracts, Testing, and Governance": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "ENASE 2026",
        "doi": "10.5220/0014840300004015",
        "url": "https://doi.org/10.5220/0014840300004015",
        "role": "assurance; evaluation",
        "scope": "security_relevant",
        "dependency": "Assurance contracts and traces cover orchestrated agent workflows.",
    },
    "MIN-Trust: A Minimum Necessary Information Trust Orchestration Framework for Multi-Agent Collaboration": {
        "authors": "Not reported in current export",
        "year": "2026",
        "venue": "GAIE 2026",
        "doi": "10.1145/3813808.3813811",
        "url": "https://doi.org/10.1145/3813808.3813811",
        "role": "defense",
        "scope": "core_security",
        "dependency": "The framework restricts information disclosure across collaborating agents.",
    },
}


NONPEER_DECISIONS = {
    "AgentSafe: Safeguarding Large Language Model-based Multi-agent Systems via Hierarchical Data Management": ("core_security", "full_text_source_reviewed"),
    "Taming Various Privilege Escalation in LLM-Based Agent Systems: A Mandatory Access Control Framework": ("core_security", "full_text_scope_screened"),
    "SAFEFLOW: A Principled Protocol for Trustworthy and Transactional Autonomous Agent Systems": ("core_security", "full_text_scope_screened"),
    "MAGPIE: A benchmark for Multi-AGent contextual PrIvacy Evaluation": ("core_security", "full_text_source_reviewed"),
    "When Persuasion Overrides Truth in Multi-Agent LLM Debates: Introducing a Confidence-Weighted Persuasion Override Rate (CW-POR)": ("core_security", "full_text_scope_screened"),
    "MedSentry: Understanding and Mitigating Safety Risks in Medical LLM Multi-Agent Systems": ("core_security", "full_text_source_reviewed"),
    "Revisiting Multi-Agent Debate as Test-Time Scaling: A Systematic Study of Conditional Effectiveness": ("security_relevant", "claim_level_review_required"),
    "SentinelAgent: Graph-based Anomaly Detection in Multi-Agent Systems": ("core_security", "full_text_scope_screened"),
    "1-2-3 Check: Enhancing Contextual Privacy in LLM via Multi-Agent Reasoning": ("core_security", "full_text_scope_screened"),
    "The Sum Leaks More Than Its Parts: Compositional Privacy Risks and Mitigations in Multi-Agent Collaboration": ("core_security", "full_text_scope_screened"),
    "WOLF: Werewolf-based Observations for LLM Deception and Falsehoods": ("core_security", "full_text_scope_screened"),
    "Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs": ("core_security", "full_text_scope_screened"),
    "Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions": ("security_relevant", "boundary_full_text_screened"),
    "Chasing Moving Targets with Online Self-Play Reinforcement Learning for Safer Language Models": ("security_relevant", "boundary_full_text_screened"),
}


EXTRA_NONPEER = {
    "tian2023evil_geniuses": (123, "263a58f4fd32caca1dad2351af4d711aec451fe6"),
    "tan2024wolf_within": (25, "d42c94924fb0117e4fdb746c21071a950c2eb83a"),
    "schroederdewitt2025openchallenges": (76, "bfbc4873584f1daec31589d58a53607db6e2e170"),
    "zou2025blocka2a": (16, "ff8870115312b9c2c970e9490a91e309e661b157"),
    "anbiaee2026protocols": (14, "c3175b64ca2b9b6ea6432c493ce6bac402c8e73f"),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80]


def venue_family(value: str) -> str:
    lower = value.lower()
    mappings = (
        (("findings of acl", "findings of eacl", "findings of emnlp"), "ACL Findings"),
        (("acl system demonstrations",), "ACL System Demonstrations"),
        (("realm workshop",), "ACL Workshop"),
        (("ijcnlp",), "IJCNLP-AACL"),
        (("naacl",), "NAACL"),
        (("emnlp",), "EMNLP"),
        (("acl",), "ACL"),
        (("aaai symposium",), "AAAI Symposium Series"),
        (("aaai",), "AAAI"),
        (("neurips responsible",), "NeurIPS Workshop"),
        (("neurips",), "NeurIPS"),
        (("icml",), "ICML"),
        (("iclr",), "ICLR"),
        (("usenix",), "USENIX Security"),
        (("ieee symposium on security",), "IEEE S&P"),
        (("acm ccs",), "ACM CCS"),
        (("asiaccs",), "ACM AsiaCCS"),
        (("aamas strategic",), "AAMAS Workshop"),
        (("aamas",), "AAMAS"),
        (("web conference",), "The Web Conference"),
        (("colm",), "COLM"),
    )
    for needles, family in mappings:
        if any(needle in lower for needle in needles):
            return family
    return value


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def reviewed_rows() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    with (ROOT / "corpus/papers.csv").open(newline="", encoding="utf-8-sig") as handle:
        papers = {row["paper_id"]: row for row in csv.DictReader(handle)}
    with (ROOT / "reviews/universal/universal_114_source_review.csv").open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        reviews = list(csv.DictReader(handle))

    rows = []
    for review in reviews:
        if review["recommended_scope"] == "adjacent":
            continue
        paper = papers[review["paper_id"]]
        is_arxiv_only = "/arxiv/" in paper["note_path"]
        is_nonarchival_workshop = any(
            marker in paper["note_path"]
            for marker in ("/neurips_workshop/", "/aamas_workshop/", "/fedkdd_workshop/")
        ) or paper["paper_id"] == "hagag2026architecture_matters"
        if is_arxiv_only:
            status, venue_type = "non_peer_or_unverified", "preprint"
        elif is_nonarchival_workshop:
            status, venue_type = "workshop_or_nonarchival", "workshop"
        else:
            status = "peer_reviewed"
            venue_type = "journal" if "/journals_" in paper["note_path"] else "conference"
        rows.append(
            {
                "paper_id": paper["paper_id"],
                "title": paper["title"],
                "authors": paper["authors"],
                "year": paper["year"],
                "venue": paper["venue"],
                "venue_family": venue_family(paper["venue"]),
                "venue_type": venue_type,
                "doi": paper["doi"],
                "primary_url": paper["primary_url"],
                "open_access_url": paper["open_access_url"],
                "publication_status": status,
                "scope_relation": review["recommended_scope"],
                "primary_role": review["recommended_category"],
                "interaction_dependency": paper["multiagent_dependency"],
                "security_relevance": review["scope_rationale"],
                "evidence_level": review["review_status"],
                "evidence_locator": review["evidence_locators"],
                "discovery_source": paper["discovery_source"],
                "cutoff": CUTOFF,
                "cutoff_basis": "first version available before cutoff",
                "note_path": paper["note_path"],
            }
        )
    return rows, papers


def supplemental_rows() -> list[dict[str, str]]:
    rows = []
    for title, item in SUPPLEMENTAL_PEER.items():
        rows.append(
            {
                "paper_id": "supp_" + slug(title),
                "title": title,
                "authors": item["authors"],
                "year": item["year"],
                "venue": item["venue"],
                "venue_family": venue_family(item["venue"]),
                "venue_type": "journal" if any(x in item["venue"] for x in ("Journal", "Ethics", "Research")) else "conference",
                "doi": item["doi"],
                "primary_url": item["url"],
                "open_access_url": item["url"],
                "publication_status": "peer_reviewed",
                "scope_relation": item["scope"],
                "primary_role": item["role"],
                "interaction_dependency": item["dependency"],
                "security_relevance": item["dependency"],
                "evidence_level": "official_metadata_and_abstract_screened",
                "evidence_locator": item["url"],
                "discovery_source": "venue proceedings and backward/forward snowballing",
                "cutoff": CUTOFF,
                "cutoff_basis": "preprint or official record available before cutoff",
                "note_path": "",
            }
        )
    return rows


def nonpeer_rows(papers: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    with (ROOT / "corpus/sets/03_taxonomy_eligible/taxonomy_candidates.csv").open(
        newline="", encoding="utf-8-sig"
    ) as handle:
        candidates = list(csv.DictReader(handle))

    rows = []
    for candidate in candidates:
        decision = NONPEER_DECISIONS.get(candidate["title"])
        if candidate["candidate_basis"] != "non_peer_citations_gt_10" or not decision:
            continue
        rows.append(
            {
                "paper_id": candidate["canonical_paper_id"] or "arxiv_" + candidate["arxiv_id"].replace(".", "_"),
                "title": candidate["title"],
                "year": candidate["publication_date"][:4],
                "venue": candidate["venue"] or "arXiv",
                "arxiv_id": candidate["arxiv_id"],
                "doi": candidate["doi"],
                "primary_url": "https://arxiv.org/abs/" + candidate["arxiv_id"],
                "citations": candidate["citations"],
                "citation_source": "Semantic Scholar Graph API",
                "citation_snapshot_date": candidate["citation_snapshot_date"],
                "scope_relation": decision[0],
                "screening_status": decision[1],
                "threshold_rule": "citationCount > 10; citation count is a retrieval gate, not automatic inclusion",
                "cutoff": CUTOFF,
            }
        )

    for paper_id, (citations, semantic_id) in EXTRA_NONPEER.items():
        paper = papers[paper_id]
        arxiv = ""
        for value in (paper["doi"], paper["primary_url"], paper["open_access_url"]):
            match = re.search(r"(\d{4}\.\d{4,5})", value or "")
            if match:
                arxiv = match.group(1)
                break
        rows.append(
            {
                "paper_id": paper_id,
                "title": paper["title"],
                "year": paper["year"],
                "venue": "arXiv",
                "arxiv_id": arxiv,
                "doi": paper["doi"],
                "primary_url": "https://arxiv.org/abs/" + arxiv,
                "citations": str(citations),
                "citation_source": "Semantic Scholar Graph API",
                "citation_snapshot_date": SNAPSHOT,
                "scope_relation": paper["scope_relation"],
                "screening_status": "full_text_source_reviewed",
                "threshold_rule": "citationCount > 10; citation count is a retrieval gate, not automatic inclusion",
                "cutoff": CUTOFF,
                "semantic_scholar_id": semantic_id,
            }
        )
    return sorted(rows, key=lambda row: (-int(row["citations"]), row["title"].lower()))


def main() -> None:
    fields = [
        "paper_id", "title", "authors", "year", "venue", "venue_family", "venue_type", "doi",
        "primary_url", "open_access_url", "publication_status", "scope_relation",
        "primary_role", "interaction_dependency", "security_relevance", "evidence_level",
        "evidence_locator", "discovery_source", "cutoff", "cutoff_basis", "note_path",
    ]
    reviewed, papers = reviewed_rows()
    high_citation_nonpeer = nonpeer_rows(papers)
    all_rows = reviewed + supplemental_rows()
    existing_titles = {slug(row["title"]) for row in all_rows}
    for candidate in high_citation_nonpeer:
        if slug(candidate["title"]) in existing_titles:
            continue
        all_rows.append(
            {
                "paper_id": candidate["paper_id"],
                "title": candidate["title"],
                "authors": "Not reported in current export",
                "year": candidate["year"],
                "venue": "arXiv",
                "venue_family": "arXiv",
                "venue_type": "preprint",
                "doi": candidate["doi"],
                "primary_url": candidate["primary_url"],
                "open_access_url": candidate["primary_url"],
                "publication_status": "non_peer_or_unverified",
                "scope_relation": candidate["scope_relation"],
                "primary_role": "high-citation non-peer security candidate",
                "interaction_dependency": "Confirmed by the recorded full-text interaction-security scope screen.",
                "security_relevance": "Retained after the citation retrieval gate and security scope screen.",
                "evidence_level": candidate["screening_status"],
                "evidence_locator": candidate["primary_url"],
                "discovery_source": "systematic search catalog and citation-threshold review",
                "cutoff": CUTOFF,
                "cutoff_basis": "primary preprint available before cutoff",
                "note_path": "",
            }
        )
    all_rows = sorted(all_rows, key=lambda row: (int(row["year"]), row["title"].lower()))
    peer = [row for row in all_rows if row["publication_status"] == "peer_reviewed"]
    write_csv(ROOT / "corpus/final/all_relevant_papers.csv", fields, all_rows)
    write_csv(ROOT / "corpus/final/peer_reviewed.csv", fields, peer)

    coverage = []
    for family in sorted({row["venue_family"] for row in peer}):
        selected = [row for row in peer if row["venue_family"] == family]
        coverage.append(
            {
                "venue_family": family,
                "venue_type": ";".join(sorted({row["venue_type"] for row in selected})),
                "paper_count": str(len(selected)),
                "core_security": str(sum(row["scope_relation"].startswith("core_security") for row in selected)),
                "security_relevant": str(sum(not row["scope_relation"].startswith("core_security") for row in selected)),
                "cutoff": CUTOFF,
            }
        )
    write_csv(
        ROOT / "corpus/final/venue_coverage.csv",
        ["venue_family", "venue_type", "paper_count", "core_security", "security_relevant", "cutoff"],
        coverage,
    )

    nonpeer_fields = [
        "paper_id", "title", "year", "venue", "arxiv_id", "doi", "primary_url",
        "citations", "citation_source", "citation_snapshot_date", "scope_relation",
        "screening_status", "threshold_rule", "cutoff", "semantic_scholar_id",
    ]
    write_csv(ROOT / "corpus/final/non_peer_citations_gt_10.csv", nonpeer_fields, high_citation_nonpeer)


if __name__ == "__main__":
    main()
