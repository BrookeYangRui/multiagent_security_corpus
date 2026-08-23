#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
INDEX = PAPERS / "index.csv"
OUT = ROOT / "corpus" / "REMAINING_187_SCOPE_AUDIT.csv"
SUMMARY = ROOT / "corpus" / "REMAINING_187_SCOPE_AUDIT_SUMMARY.md"

SECURITY_TERMS = (
    "attack", "adversar", "malicious", "security", "secure", "privacy", "leak",
    "confidential", "integrity", "authorization", "authentication", "byzantine",
    "collusion", "deception", "jailbreak", "injection", "poison", "compromis",
    "tamper", "exploit", "backdoor", "worm", "threat", "denial", "taint",
)
WEAK_TERMS = ("safety", "robust", "reliab", "alignment", "hallucination", "ethical", "governance", "compliance", "misinformation", "drift")


def read_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##+\s+{re.escape(heading)}\s*$", re.I | re.M)
    m = pattern.search(text)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^##+\s+", text[start:], re.M)
    end = start + nxt.start() if nxt else len(text)
    return " ".join(text[start:end].strip().split())


def pick(text: str, headings: tuple[str, ...]) -> str:
    for h in headings:
        value = section(text, h)
        if value:
            return value
    return ""

rows = read_rows(INDEX)
if len(rows) != 187:
    raise SystemExit(f"expected 187 index rows, found {len(rows)}")

out = []
for r in rows:
    path = ROOT / r["paper_path"]
    text = path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    system = pick(text, ("System Studied", "System studied"))
    dependency = pick(text, ("Multi-Agent Dependency", "Multi agent dependency", "Multi-Agent dependency"))
    threat = pick(text, ("Threat Actor", "Attacker or fault actor"))
    attack = pick(text, ("Attack or Failure", "Attack Mechanism", "Failure"))
    defense = pick(text, ("Defense", "Defense Mechanism"))
    evaluation = pick(text, ("Evaluation", "Evaluation Contract"))
    relevance = pick(text, ("Relevance to Our SoK", "Taxonomy Implications", "Included Concepts"))
    source_review = "source_reviewed" if "<!-- source_review_start -->" in lower else ("metadata_only" if "this metadata note was generated" in lower else "detailed_unreviewed")
    sec_hits = sorted({t for t in SECURITY_TERMS if t in lower})
    weak_hits = sorted({t for t in WEAK_TERMS if t in lower})
    evidence_text = " ".join((system, dependency, threat, attack, defense, evaluation, relevance)).lower()
    has_multi = bool(dependency) or any(t in evidence_text for t in ("agent", "principal", "message", "topology", "shared", "delegat", "aggregat", "collab", "communicat"))
    has_security = bool(sec_hits) or any(t in evidence_text for t in SECURITY_TERMS)
    if source_review == "source_reviewed" and has_multi and has_security:
        tier = "strong_existing_source_evidence"
    elif source_review == "metadata_only":
        tier = "metadata_only_requires_primary_source_check"
    elif has_multi and has_security:
        tier = "plausible_requires_manual_confirmation"
    else:
        tier = "weak_or_ambiguous_requires_manual_confirmation"
    out.append({
        "work_key": r["work_key"],
        "title": r["title"],
        "evidence_set": r["evidence_set"],
        "dominant_contribution": r["dominant_contribution"],
        "venue": r["venue"],
        "paper_path": r["paper_path"],
        "note_status": source_review,
        "system_studied": system,
        "multi_agent_dependency": dependency,
        "threat_actor": threat,
        "attack_or_failure": attack,
        "defense": defense,
        "evaluation": evaluation,
        "sok_relevance": relevance,
        "security_terms": ";".join(sec_hits),
        "weak_terms": ";".join(weak_hits),
        "preliminary_tier": tier,
        "final_verdict": "PENDING_MANUAL_REVIEW",
        "final_reason": "",
    })

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

counts = Counter(r["preliminary_tier"] for r in out)
lines = [
    "# Remaining 187 Scope Audit Triage",
    "",
    "This is a triage view only. Every row still requires a final manual verdict.",
    "",
    "## Tier counts",
    "",
]
for tier, count in sorted(counts.items()):
    lines.append(f"* `{tier}`: **{count}**")
for tier in (
    "weak_or_ambiguous_requires_manual_confirmation",
    "metadata_only_requires_primary_source_check",
    "plausible_requires_manual_confirmation",
):
    subset = [r for r in out if r["preliminary_tier"] == tier]
    lines += ["", f"## {tier} ({len(subset)})", ""]
    for r in subset:
        lines.append(f"* `{r['work_key']}` | {r['title']} | {r['evidence_set']} | {r['dominant_contribution']} | {r['venue']}")
SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {len(out)} rows and summary")
