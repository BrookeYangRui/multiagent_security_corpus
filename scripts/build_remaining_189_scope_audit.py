#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
P = ROOT / "papers"
OUT = C / "REMAINING_189_SCOPE_AUDIT.csv"
SUMMARY = C / "REMAINING_189_SCOPE_AUDIT_SUMMARY.md"

SECURITY_TERMS = (
    "attack", "adversar", "malicious", "security", "secure", "privacy", "leak",
    "confidential", "integrity", "authorization", "authentication", "byzantine",
    "collusion", "deception", "jailbreak", "injection", "poison", "compromis",
    "tamper", "exploit", "backdoor", "worm", "threat", "denial", "taint",
    "stegan", "covert", "zero-trust", "fault-toler", "fault toler",
)
WEAK_TERMS = (
    "safety", "robust", "reliab", "alignment", "hallucination", "ethical",
    "governance", "compliance", "misinformation", "drift", "trustworthy",
)
INTERACTION_TERMS = (
    "multi-agent", "multi agent", "agent-to-agent", "agent to agent", "cross-agent",
    "inter-agent", "inter agent", "communication", "message", "topology", "shared",
    "delegat", "aggregat", "consensus", "collab", "orchestrat", "sender", "receiver",
    "principal", "coalition", "collective", "coordination",
)


def rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def section(text: str, headings: tuple[str, ...]) -> str:
    for heading in headings:
        m = re.search(rf"^##+\s+{re.escape(heading)}\s*$", text, re.I | re.M)
        if not m:
            continue
        start = m.end()
        nxt = re.search(r"^##+\s+", text[start:], re.M)
        end = start + nxt.start() if nxt else len(text)
        return " ".join(text[start:end].strip().split())
    return ""

s1 = rows(C / "set1_core.csv")
s2 = rows(C / "set2_emerging.csv")
if (len(s1), len(s2)) != (92, 97):
    raise SystemExit(f"expected 92/97, got {len(s1)}/{len(s2)}")
active = {r["work_key"]: r for r in s1 + s2}
index = rows(P / "index.csv")
if len(index) != 189 or {r["work_key"] for r in index} != set(active):
    raise SystemExit("papers/index.csv is not the exact 189 corpus")

out = []
for item in index:
    source = active[item["work_key"]]
    path = ROOT / item["paper_path"]
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    system = section(text, ("System Studied", "System studied"))
    dependency = section(text, ("Multi-Agent Dependency", "Multi agent dependency", "Multi-Agent dependency"))
    threat = section(text, ("Threat Actor", "Attacker or fault actor", "Security Model"))
    failure = section(text, ("Attack or Failure", "Attack Mechanism", "Failure"))
    defense = section(text, ("Defense", "Defense Mechanism"))
    evaluation = section(text, ("Evaluation", "Evaluation Contract"))
    relevance = section(text, ("Relevance to Our SoK", "Taxonomy Implications", "Included Concepts"))
    title = item["title"]
    combined = " ".join((title, source.get("scope_reason", ""), source.get("risk_or_property", ""), system, dependency, threat, failure, defense, evaluation, relevance)).lower()

    note_status = "metadata_only" if "this metadata note was generated" in lower else "detailed"
    security_hits = sorted({t for t in SECURITY_TERMS if t in combined})
    weak_hits = sorted({t for t in WEAK_TERMS if t in combined})
    interaction_hits = sorted({t for t in INTERACTION_TERMS if t in combined})
    direct_security = bool(security_hits)
    direct_interaction = bool(interaction_hits) or bool(dependency)

    if note_status == "detailed" and direct_security and direct_interaction:
        triage = "likely_keep_detailed"
    elif note_status == "metadata_only" and direct_security and direct_interaction:
        triage = "source_check_metadata_security"
    elif direct_interaction and weak_hits:
        triage = "scope_boundary_check_safety_reliability"
    else:
        triage = "scope_boundary_check_other"

    out.append({
        "work_key": item["work_key"],
        "title": title,
        "evidence_set": item["evidence_set"],
        "dominant_contribution": item["dominant_contribution"],
        "venue": item["venue"],
        "primary_url": source.get("primary_url", ""),
        "doi": source.get("doi", ""),
        "arxiv_id": source.get("arxiv_id", ""),
        "paper_path": item["paper_path"],
        "note_status": note_status,
        "scope_reason_current": source.get("scope_reason", ""),
        "interaction_dependence_current": source.get("interaction_dependence", ""),
        "risk_or_property_current": source.get("risk_or_property", ""),
        "system_studied": system,
        "multi_agent_dependency": dependency,
        "threat_or_security_model": threat,
        "attack_or_failure": failure,
        "defense": defense,
        "evaluation": evaluation,
        "sok_relevance": relevance,
        "security_hits": ";".join(security_hits),
        "interaction_hits": ";".join(interaction_hits),
        "weak_hits": ";".join(weak_hits),
        "triage": triage,
        "final_verdict": "PENDING_MANUAL_REVIEW",
        "final_reason": "",
        "source_checked": "no",
    })

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

counts = Counter(r["triage"] for r in out)
lines = [
    "# Remaining 189 Strict MAS-Security Audit",
    "",
    "This is a row-level audit queue. Triage is not a final membership decision.",
    "Final review must answer two questions for every work: (1) does the studied system contain separately addressable LLM-backed principals with a material inter-agent relation, and (2) is a concrete security/privacy property, adversary, attack, defense, guarantee, or security evaluation substantively about that relation rather than merely using MAS as a tool?",
    "",
    "## Triage counts",
    "",
]
for k, v in sorted(counts.items()):
    lines.append(f"* `{k}`: **{v}**")
for tier in ("scope_boundary_check_other", "scope_boundary_check_safety_reliability", "source_check_metadata_security", "likely_keep_detailed"):
    subset = [r for r in out if r["triage"] == tier]
    lines += ["", f"## {tier} ({len(subset)})", ""]
    for r in subset:
        lines.append(f"* `{r['work_key']}` | {r['title']} | {r['evidence_set']} | {r['dominant_contribution']} | {r['venue']}")
SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Built {len(out)}-row scope audit queue: {dict(counts)}")
