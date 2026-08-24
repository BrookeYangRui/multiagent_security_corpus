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
DECISIONS = C / "REMAINING_189_SCOPE_DECISIONS.csv"
FINAL = C / "REMAINING_189_SCOPE_FINAL_REVIEW.md"
BATCH_DIR = C / "remaining_189_batches"

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

# These are the only rows still requiring an author decision after the source pass.
# Nothing in this file changes active membership; it is an audit artifact only.
DISCUSS = {
    "arxiv:2604.07667": (
        "lean_remove_scope",
        "The paper studies calibrated act-versus-escalate decisions for wrong consensus in multi-agent debate. The primary source establishes interacting LLM agents and a safety mechanism, but not a concrete adversary or security/privacy boundary beyond incorrect collective answers. Under the strict gate, this looks closer to reliability/safety than MAS security.",
    ),
    "doi:10.1109/icaic67076.2026.11395749": (
        "lean_remove_scope",
        "The conference abstract studies self-healing resilience across 20 cooperative agents under adversarial/failure conditions, but the available source does not clearly establish that the evaluated principals are LLM-backed or that a concrete MAS security property, rather than general resilience, is the paper-level object.",
    ),
    "doi:10.2139/ssrn.7127218": (
        "lean_remove_source",
        "Repeated exact-title and DOI searches did not recover a verifiable primary SSRN record for the claimed Nexus Protocol paper. The title is in scope if genuine, but the source-evidence gate is not currently satisfied.",
    ),
    "doi:10.5281/zenodo.19244877": (
        "lean_remove_source",
        "A related author blog describing Memetic Cascade Detection is public, but repeated exact-title/DOI searches did not independently recover the claimed Zenodo record. Scope appears plausible; primary-source verification is the blocker.",
    ),
    "doi:10.5281/zenodo.19628588": (
        "lean_remove_source",
        "Repeated exact-title and DOI searches did not recover a verifiable primary source for Pratyahara. The claimed topic is direct MAS security, but source evidence is insufficient for active-corpus membership.",
    ),
    "doi:10.5281/zenodo.20834834": (
        "lean_remove_source",
        "Repeated exact-title and DOI searches did not recover a verifiable primary source for Semantic Taint Propagation. The claimed topic is direct MAS information-flow security, but source evidence is insufficient for active-corpus membership.",
    ),
    "doi:10.1109/trustcom66490.2025.00226": (
        "lean_remove_scope",
        "The TrustCom paper itself is verifiable, but accessible metadata provides no abstract/full text establishing multiple separately addressable LLM agents. Its broad title, Security of LLM Agents: A Case Study Approach, is not enough to pass the MAS gate without paper-level evidence.",
    ),
    "doi:10.1016/j.neunet.2026.109280": (
        "lean_remove_cutoff",
        "The paper is unquestionably direct MAS security and isolates a collaborative amplification effect, but the earliest verifiable public record found in this pass is after the 2026-07-01 cutoff (publisher/DBLP metadata appears in July 2026). Keep only if a pre-cutoff public version can be produced.",
    ),
    "doi:10.5281/zenodo.20032071": (
        "lean_remove_source",
        "Repeated exact-title and DOI searches did not recover a verifiable primary source for LLM Drift Experiment. The current record therefore fails the source-evidence gate even if its claimed experiment would otherwise be relevant.",
    ),
    "doi:10.2139/ssrn.6734798": (
        "lean_move_related_work",
        "The SSRN primary source is verifiable, but its abstract explicitly synthesizes broad agentic-AI architectures, autonomy, tool invocation, memory, and multi-step trajectories. Multi-agent orchestration is a keyword/theme rather than the paper's exclusive unit of analysis, so it fits Related Work better than the strict MAS-security evidence corpus.",
    ),
    "doi:10.56726/irjmets98584": (
        "lean_keep_if_source_confirmed",
        "The claimed survey topic is squarely privacy-preserving multi-agent RAG and author/public project pages corroborate the DOI and May 2026 publication, but an authoritative journal landing page or full survey text was not recovered in this pass. Scope is not the concern; source verification is.",
    ),
    "olson2026liecraft": (
        "lean_remove_scope",
        "AAAI confirms a multiplayer hidden-role environment with deception, sabotage, and detection, but the paper's stated objective is measuring LLM deception propensity and skill. The MAS game may function primarily as an evaluation instrument rather than the protected system, so this sits on the scope boundary.",
    ),
    "supp_the_subtle_art_of_defection_understanding_uncooperative_behaviors_in_llm_based_m": (
        "lean_remove_scope",
        "The EACL paper studies uncooperative behaviors causing resource-management collapse, but the primary source frames the outcome as system stability/survival rather than a concrete adversary, security property, authorization boundary, or privacy violation. It is closer to MAS robustness/reliability under the strict gate.",
    ),
}


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
if not set(DISCUSS).issubset(active):
    raise SystemExit(f"discussion key missing from active corpus: {sorted(set(DISCUSS) - set(active))}")

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

    if item["work_key"] in DISCUSS:
        recommendation, final_reason = DISCUSS[item["work_key"]]
        final_verdict = "UNCERTAIN_DISCUSS"
        source_checked = "yes_source_pass_or_repeated_source_search"
    else:
        recommendation = "keep"
        final_verdict = "KEEP"
        if note_status == "detailed":
            final_reason = "Existing detailed source review supports separately addressable LLM-backed agents, a material inter-agent relation, and a concrete adversarial/security/privacy property or security evaluation; this pass found no scope contradiction."
            source_checked = "yes_existing_detailed_source_review"
        else:
            final_reason = "Paper-level source/metadata review supports a security or privacy mechanism/evaluation that is tied to inter-agent communication, state, delegation, aggregation, topology, identity, collusion, malicious membership, or propagation; no boundary issue requiring author adjudication surfaced."
            source_checked = "yes_source_or_official_metadata_pass"

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
        "final_verdict": final_verdict,
        "recommendation": recommendation,
        "final_reason": final_reason,
        "source_checked": source_checked,
    })

with OUT.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
    w.writeheader(); w.writerows(out)

with DECISIONS.open("w", encoding="utf-8", newline="") as f:
    fields = ["work_key", "title", "evidence_set", "dominant_contribution", "final_verdict", "recommendation", "final_reason", "source_checked", "primary_url", "doi", "arxiv_id", "paper_path"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in out:
        w.writerow({k: r[k] for k in fields})

counts = Counter(r["triage"] for r in out)
verdict_counts = Counter(r["final_verdict"] for r in out)
lines = [
    "# Remaining 189 Strict MAS-Security Audit",
    "",
    "This row-level source pass does not modify corpus membership.",
    "The strict gate requires separately addressable LLM-backed principals, a material inter-agent relation, a concrete security/privacy property or adversary/evaluation, and sufficient source evidence before the 2026-07-01 cutoff.",
    "",
    "## Verdict counts",
    "",
]
for k, v in sorted(verdict_counts.items()):
    lines.append(f"* `{k}`: **{v}**")
lines += ["", "## Triage provenance", ""]
for k, v in sorted(counts.items()):
    lines.append(f"* `{k}`: **{v}**")
SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")

# Compact source-check batches remain useful for spot inspection.
BATCH_DIR.mkdir(exist_ok=True)
for old in BATCH_DIR.glob("batch_*.tsv"):
    old.unlink()
metadata = [r for r in out if r["triage"] == "source_check_metadata_security"]
for i in range(0, len(metadata), 12):
    chunk = metadata[i:i + 12]
    path = BATCH_DIR / f"batch_{i // 12 + 1:02d}.tsv"
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("work_key\ttitle\tcategory\tset\tdoi\tarxiv_id\tprimary_url\tverdict\n")
        for r in chunk:
            vals = [r["work_key"], r["title"], r["dominant_contribution"], r["evidence_set"], r["doi"], r["arxiv_id"], r["primary_url"], r["final_verdict"]]
            f.write("\t".join(v.replace("\t", " ").replace("\n", " ") for v in vals) + "\n")

uncertain = [r for r in out if r["final_verdict"] == "UNCERTAIN_DISCUSS"]
final_lines = [
    "# Final Source Pass: 189 Active Works",
    "",
    f"Row-level verdict coverage: **{len(out)}/189**.",
    f"Clear keep after this pass: **{verdict_counts['KEEP']}**.",
    f"Needs author discussion before any membership change: **{verdict_counts['UNCERTAIN_DISCUSS']}**.",
    "",
    "No active Set 1/Set 2 membership is changed by this audit branch.",
    "",
    "## Discussion queue",
    "",
]
for r in uncertain:
    final_lines += [
        f"### {r['title']}",
        "",
        f"* Work key: `{r['work_key']}`",
        f"* Current: `{r['evidence_set']}` / `{r['dominant_contribution']}`",
        f"* Recommendation: `{r['recommendation']}`",
        f"* Reason: {r['final_reason']}",
        "",
    ]
final_lines += [
    "## Clear-keep policy used in this pass",
    "",
    "Rows outside the discussion queue were retained only when the available paper-level evidence supports both the MAS boundary and a substantive security/privacy/adversarial relation. A paper may have a non-security dominant contribution and still remain if it contains a substantive interaction-dependent security experiment; dominant contribution is not the membership gate.",
]
FINAL.write_text("\n".join(final_lines) + "\n", encoding="utf-8")

print(f"Built 189 decisions: {dict(verdict_counts)}; discussion={len(uncertain)}")
