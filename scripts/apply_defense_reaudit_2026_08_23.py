#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
PAPERS = ROOT / "papers"
DATE = "2026-08-23"

CATEGORY_DIR = {
    "attack": "attacks",
    "defense": "defenses",
    "evaluation": "evaluations",
    "general": "general",
    "survey": "surveys",
}

OLD_COUNTS = {"attack": 42, "defense": 94, "evaluation": 44, "general": 11, "survey": 10}
NEW_COUNTS = {"attack": 44, "defense": 85, "evaluation": 46, "general": 16, "survey": 10}

RECLASS = {
    "arxiv:2604.13353": (
        "general",
        "The paper's primary contribution is a cross-domain network-troubleshooting architecture; privacy-preserving anonymization is one of several system features rather than the main security-defense contribution.",
        "https://arxiv.org/abs/2604.13353",
    ),
    "arxiv:2604.07911": (
        "general",
        "DACS primarily addresses context pollution and steering accuracy in multi-agent orchestration. Its core problem is reliability and context isolation rather than an adversarial security defense.",
        "https://arxiv.org/abs/2604.07911",
    ),
    "arxiv:2605.12240": (
        "general",
        "NOD is primarily a reliable service-agent architecture for policy compliance, tool hallucination, and long-horizon execution; it does not center an adversarial threat model.",
        "https://arxiv.org/abs/2605.12240",
    ),
    "doi:10.2139/ssrn.7181662": (
        "general",
        "MedAgentNet is primarily a federated clinical-intelligence architecture. Privacy-preserving disclosure is an architectural requirement, not a threat-driven defense contribution.",
        "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7181662",
    ),
    "doi:10.2139/ssrn.7067276": (
        "general",
        "REMA is primarily a proactive robotic-manipulation architecture for reliable execution and semantic validation, not a security defense against a concrete adversary.",
        "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7067276",
    ),
    "xu2026trust_paradox": (
        "evaluation",
        "The main contribution is formalization and empirical measurement of the Trust-Vulnerability Paradox with OER and Authorization Drift; mitigation mechanisms are secondary evaluations.",
        "https://arxiv.org/abs/2510.18563",
    ),
    "arxiv:2606.30602": (
        "evaluation",
        "MESA's primary artifact is a label-free framework for ranking and measuring security-critical communication edges. It prioritizes where defenses should be deployed rather than providing the defense itself.",
        "https://arxiv.org/abs/2606.30602",
    ),
    "arxiv:2605.02812": (
        "attack",
        "The paper's central contribution is the first systematic automated analysis and demonstration of persistent cross-platform LLM-agent worm propagation; RTW-A is a substantial but subsequent defense contribution.",
        "https://arxiv.org/abs/2605.02812",
    ),
    "arxiv_2509_14284": (
        "attack",
        "The paper introduces and systematically studies compositional privacy leakage as a new multi-agent vulnerability class; ToM and CoDef are mitigation follow-ons to the risk contribution.",
        "https://vaidehi99.github.io/MultiAgentPrivacy.pdf",
    ),
}

CUTOFF_FLAGS = {
    "doi:10.2139/ssrn.7181662": "Current SSRN record says posted 2026-07-31, after the repository cutoff. Membership is intentionally unchanged in this contribution-only audit and needs a separate identity/first-public-date check.",
    "doi:10.2139/ssrn.7067276": "Current SSRN record says posted 2026-07-06, after the repository cutoff. Membership is intentionally unchanged in this contribution-only audit and needs a separate identity/first-public-date check.",
}

SOURCE_GAP = {
    "doi:10.5281/zenodo.19477187": "Primary source could not be recovered during this re-audit. The defense label is retained provisionally rather than changed from title-level inference alone.",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


s1_path = CORPUS / "set1_core.csv"
s2_path = CORPUS / "set2_emerging.csv"
index_path = PAPERS / "index.csv"
s1 = read_csv(s1_path)
s2 = read_csv(s2_path)
index = read_csv(index_path)

active = s1 + s2
old = Counter(r["dominant_contribution"] for r in active)
if dict(old) != OLD_COUNTS:
    raise SystemExit(f"unexpected starting contribution counts: {dict(old)}")
if len(active) != 201 or len(index) != 201:
    raise SystemExit("expected the frozen 201-work corpus")

by_key = {r["work_key"]: r for r in active}
idx_by_key = {r["work_key"]: r for r in index}
missing = set(RECLASS) - set(by_key)
if missing:
    raise SystemExit(f"reaudit keys missing from active corpus: {sorted(missing)}")

# Apply row-level contribution corrections and move the corresponding note.
for key, (new_cat, reason, source) in RECLASS.items():
    row = by_key[key]
    if row["dominant_contribution"] != "defense":
        raise SystemExit(f"expected defense before reaudit: {key} -> {row['dominant_contribution']}")
    row["dominant_contribution"] = new_cat

    item = idx_by_key[key]
    old_path = ROOT / item["paper_path"]
    if not old_path.is_file():
        raise SystemExit(f"missing paper note for {key}: {old_path}")
    venue_folder = item["venue_folder"]
    new_rel = Path("papers") / CATEGORY_DIR[new_cat] / venue_folder / old_path.name
    new_path = ROOT / new_rel
    new_path.parent.mkdir(parents=True, exist_ok=True)
    if new_path.exists() and new_path != old_path:
        raise SystemExit(f"destination already exists: {new_path}")

    text = old_path.read_text(encoding="utf-8", errors="replace")
    set_name = row["evidence_set"]
    venue = item["venue"] or "Not reported"
    status = f"> **Final signed corpus status:** `{set_name}` · `{new_cat}` · venue `{venue}` · defense re-audit `{DATE}`."
    text = re.sub(
        r"> \*\*Final signed corpus status:\*\* .*?\n",
        status + "\n",
        text,
        count=1,
    )
    text = text.replace("* Dominant contribution: `defense`", f"* Dominant contribution: `{new_cat}`")
    text = text.replace("- Primary category: `defense`", f"- Primary category: `{new_cat}`")
    text += (
        f"\n\n## Defense dominant-contribution re-audit ({DATE})\n\n"
        f"**Decision:** reclassify `defense` → `{new_cat}`.\n\n"
        f"**Reason:** {reason}\n\n"
        f"**Evidence used for this re-audit:** {source}\n"
    )
    new_path.write_text(text, encoding="utf-8")
    if new_path != old_path:
        old_path.unlink()

    item["dominant_contribution"] = new_cat
    item["paper_path"] = str(new_rel).replace("\\", "/")

# Remove empty venue/category directories left by moved notes.
for p in sorted(PAPERS.rglob("*"), reverse=True):
    if p.is_dir():
        try:
            p.rmdir()
        except OSError:
            pass

new = Counter(r["dominant_contribution"] for r in active)
if dict(new) != NEW_COUNTS:
    raise SystemExit(f"unexpected final contribution counts: {dict(new)}")

write_csv(s1_path, s1, list(s1[0].keys()))
write_csv(s2_path, s2, list(s2[0].keys()))
write_csv(index_path, index, list(index[0].keys()))

# Build a transparent 94-row re-audit ledger. This is contribution screening, not a claim that all 94 papers were newly full-text verified.
old_defense_items = [r for r in index if r["work_key"] in RECLASS or r["dominant_contribution"] == "defense"]
if len(old_defense_items) != 94:
    raise SystemExit(f"defense reaudit universe changed: {len(old_defense_items)}")
ledger_fields = [
    "work_key", "title", "evidence_set", "previous_contribution", "reaudited_contribution",
    "changed", "decision_basis", "source_gap", "cutoff_flag"
]
ledger = []
for item in old_defense_items:
    key = item["work_key"]
    if key in RECLASS:
        new_cat, reason, source = RECLASS[key]
        basis = f"Targeted source verification: {reason} Source: {source}"
        changed = "yes"
    else:
        new_cat = "defense"
        basis = "Retained after strict dominant-contribution screening of the existing paper note/title; no evidence found that a non-defense contribution clearly dominates. This does not upgrade source-verification status."
        changed = "no"
    ledger.append({
        "work_key": key,
        "title": item["title"],
        "evidence_set": item["evidence_set"],
        "previous_contribution": "defense",
        "reaudited_contribution": new_cat,
        "changed": changed,
        "decision_basis": basis,
        "source_gap": SOURCE_GAP.get(key, ""),
        "cutoff_flag": CUTOFF_FLAGS.get(key, ""),
    })
write_csv(CORPUS / f"defense_reaudit_{DATE}.csv", ledger, ledger_fields)

# Regenerate category READMEs from the final index.
labels = {
    "attack": "Attack papers",
    "defense": "Defense papers",
    "evaluation": "Evaluation papers",
    "general": "General papers",
    "survey": "Survey papers",
}
for cat, dirname in CATEGORY_DIR.items():
    rows = [r for r in index if r["dominant_contribution"] == cat]
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        groups[r["venue_folder"]].append(r)
    out = [
        f"# {labels[cat]}",
        "",
        f"Final 201-corpus dominant-contribution count after the {DATE} defense re-audit: **{len(rows)}**.",
        "",
        "Each retained work is placed under its publication venue folder. The status banner inside every note records the current corpus set and dominant contribution.",
        "",
    ]
    for venue in sorted(groups):
        out += [f"## {venue}", ""]
        for r in sorted(groups[venue], key=lambda x: x["title"].lower()):
            rel = Path(r["paper_path"]).relative_to(Path("papers") / dirname)
            out.append(f"* [{r['title']}]({str(rel).replace('\\\\', '/')})  `{r['evidence_set']}`")
        out.append("")
    (PAPERS / dirname / "README.md").write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")

papers_readme = f"""# Final 201 paper corpus

This directory contains exactly the **201 works** in the manuscript corpus: **96 Set 1** and **105 Set 2**.

Papers are organized first by dominant contribution and then by publication venue. The tree is materialized only from `corpus/set1_core.csv` and `corpus/set2_emerging.csv`.

| Contribution | Count | Directory |
| --- | ---: | --- |
| attack | {NEW_COUNTS['attack']} | [`attacks/`](attacks/) |
| defense | {NEW_COUNTS['defense']} | [`defenses/`](defenses/) |
| evaluation | {NEW_COUNTS['evaluation']} | [`evaluations/`](evaluations/) |
| general | {NEW_COUNTS['general']} | [`general/`](general/) |
| survey | {NEW_COUNTS['survey']} | [`surveys/`](surveys/) |

The defense dominant-contribution labels were re-audited on `{DATE}` under a stricter rule: a paper is defense-primary only when its main contribution is a mechanism, protocol, or system that prevents, detects, contains, or recovers from a concrete security threat or system-level security failure. Security-adjacent reliability, application architecture, and measurement work are not defense-primary merely because they include privacy, robustness, safety, or governance features.

[`index.csv`](index.csv) is the exact one-to-one mapping from all 201 corpus work keys to their current paper paths.
"""
(PAPERS / "README.md").write_text(papers_readme, encoding="utf-8")

# Update concise repository-facing counts.
root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
root_readme = root_readme.replace(
    "The signed dominant contribution totals are **42 attacks**, **94 defenses**, **44 evaluations**, **11 general works**, and **10 surveys**.",
    "After the 2026-08-23 defense dominant-contribution re-audit, the totals are **44 attacks**, **85 defenses**, **46 evaluations**, **16 general works**, and **10 surveys**.",
)
(ROOT / "README.md").write_text(root_readme, encoding="utf-8")

attacks = (ROOT / "related_work" / "attacks.md").read_text(encoding="utf-8")
attacks = attacks.replace("**42 attack primary works**", "**44 attack primary works**")
attacks = attacks.replace("the count of 42", "the count of 44")
attacks = attacks.replace("complete 42 work attack primary list", "complete 44 work attack primary list")
(ROOT / "related_work" / "attacks.md").write_text(attacks, encoding="utf-8")

bench = (ROOT / "related_work" / "benchmarks.md").read_text(encoding="utf-8")
bench = bench.replace("**44 evaluation primary works**", "**46 evaluation primary works**")
bench = bench.replace("complete 44 work evaluation primary list", "complete 46 work evaluation primary list")
(ROOT / "related_work" / "benchmarks.md").write_text(bench, encoding="utf-8")

defense_doc = (ROOT / "related_work" / "defenses.md").read_text(encoding="utf-8")
intro = "# Defenses\n\nThe final 201-work corpus contains **85 defense-primary works** after the 2026-08-23 dominant-contribution re-audit. Defense-primary now requires the security mechanism itself to be a main contribution; reliability or application papers with incidental security features are filed elsewhere.\n\n"
defense_doc = re.sub(r"^# Defenses\n\n", intro, defense_doc, count=1)
(ROOT / "related_work" / "defenses.md").write_text(defense_doc, encoding="utf-8")

validator = (ROOT / "scripts" / "validate_corpus.py").read_text(encoding="utf-8")
validator = validator.replace(
    'EXPECTED_CONTRIB = {"attack": 42, "defense": 94, "evaluation": 44, "general": 11, "survey": 10}',
    'EXPECTED_CONTRIB = {"attack": 44, "defense": 85, "evaluation": 46, "general": 16, "survey": 10}',
)
(ROOT / "scripts" / "validate_corpus.py").write_text(validator, encoding="utf-8")

summary = f"""# Defense Dominant-Contribution Re-Audit

Date: `{DATE}`

## Rule

The previous `defense` bucket was re-screened under a stricter dominant-contribution rule. A work is defense-primary only when its main contribution is a mechanism, protocol, or system intended to prevent, detect, contain, or recover from a concrete MAS security threat or system-level security failure. A paper is not defense-primary merely because it contains privacy-preserving, robust, safe, trustworthy, or governance-oriented features.

This pass reviews the full **94-work previous defense bucket** as a contribution-classification audit. It does **not** upgrade the source-verification state of papers whose notes remain metadata-only.

## Result

* Previous defense-primary count: **94**
* Retained as defense-primary: **85**
* Reclassified: **9**
* Final 201-work contribution counts: **44 attack, 85 defense, 46 evaluation, 16 general, 10 survey**

## Reclassified works

| Work | New category | Reason |
| --- | --- | --- |
"""
for key, (new_cat, reason, source) in RECLASS.items():
    title = idx_by_key[key]["title"]
    summary += f"| {title} | `{new_cat}` | {reason} |\n"
summary += """

## Important source-status notes

`Governance Effectiveness in Distributed Multi-Agent LLM Systems: Confound Isolation, Diversity Erosion, and the Accidental Governance Effect` remains provisionally defense-primary because the primary source could not be recovered during this pass. Its current metadata-only note is not enough to justify a category change in either direction.

Two reclassified application/reliability papers also expose a separate cutoff question. The currently discoverable SSRN records for `MedAgentNet` and `REMA` report posting dates after the repository's 2026-07-01 literature cutoff. This audit intentionally leaves the 201-work membership frozen and records the anomaly for a separate identity and first-public-date review rather than silently changing the denominator here.
"""
(CORPUS / f"DEFENSE_REAUDIT_{DATE}.md").write_text(summary, encoding="utf-8")

print("Defense re-audit applied: attack=44 defense=85 evaluation=46 general=16 survey=10 total=201")
