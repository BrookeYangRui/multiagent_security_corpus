#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
PAPERS = ROOT / "papers"

# Human-reviewed 2026-08-25 partition update. These 15 works move from Set 2 to
# Set 1; all other corpus membership and paper-level taxonomy fields are kept.
PROMOTIONS = [
    ("IBGP: Imperfect Byzantine Generals Problem for Zero-Shot Robustness in Communicative Multi-Agent Systems", "AAMAS", "2025"),
    ("1-2-3 Check: Enhancing Contextual Privacy in LLM via Multi-Agent Reasoning", "IASEAI", "2026"),
    ("AdvEvo-MARL: Shaping Internalized Safety through Adversarial Co-Evolution in Multi-Agent Reinforcement Learning", "ICML", "2026"),
    ("Exposing Weak Links in Multi-Agent Systems under Adversarial Prompting", "AAMAS", "2026"),
    ("Goal-Aware Identification and Rectification of Misinformation in Multi-Agent Systems", "ICLR", "2026"),
    ("Securing Multi-Agent Systems Against Corruptions via Node Contribution Backpropagation", "ICML", "2026"),
    ("The Dark Side of LLMs: Agent-based Attack Vectors for System-level Compromise", "ARES Workshop (AI4TCI)", "2026"),
    ("To Trust or Not to Trust: Attention-based Trust Management for LLM Multi-Agent Systems", "ACL", "2026"),
    ("Robust Multi-Agent LLMs under Byzantine Faults", "EMNLP", "2026"),
    ("SAIGuard: Communication-State Simulation for Proactive Defense of LLM Multi-Agent Systems", "EMNLP Findings", "2026"),
    ("Achilles Heel of Distributed Multi-Agent Systems", "ICCV MMRAgI Workshop", "2025"),
    ("Prompt Optimization Enables Stable Algorithmic Collusion in LLM Agents", "ICLR Workshop", "2026"),
    ("Smarter Saboteurs, Better Fixers: Scaling&Security in Linear Multi-Agent Workflows", "AIWILD Workshop at ICML", "2026"),
    ("Toward Trustworthy Agentic AI: A Multimodal Framework for Preventing Prompt Injection Attacks", "ICCA", "2025"),
    ("INFA-Guard: Mitigating Malicious Propagation via Infection-Aware Safeguarding in LLM-Based Multi-Agent Systems", "EMNLP", "2026"),
]
PROMOTION_META = {title: (venue, year) for title, venue, year in PROMOTIONS}
PROMOTION_TITLES = [title for title, _, _ in PROMOTIONS]


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def promote_row(row: dict[str, str]) -> None:
    title = row["title"]
    venue, year = PROMOTION_META[title]
    row["evidence_set"] = "set1_core"
    row["maturity_rule_pass"] = "yes"
    row["peer_reviewed"] = "yes"
    row["peer_review_basis"] = "2026-08-25 human-reviewed publication metadata"
    row["venue"] = venue
    row["year"] = year
    reason = row.get("decision_reason", "").strip()
    note = (
        "2026-08-25 human-reviewed partition update: moved to set1_core after "
        "updated publication metadata established the Set 1 maturity criterion."
    )
    if note not in reason:
        row["decision_reason"] = (reason + " " + note).strip()
    row["membership_reason"] = (
        "Passed MAS-security scope. Maturity: peer_reviewed=yes under the "
        "2026-08-25 human-reviewed publication update. Meets the Set 1 union "
        "rule (peer reviewed OR frozen_citation_count>=10)."
    )


def update_note(path: Path, venue: str, year: str) -> None:
    text = path.read_text(encoding="utf-8")
    before = text
    # Only change the authoritative final-status banner's set membership.
    banner_start = text.find("<!-- FINAL_CORPUS_STATUS_START -->")
    banner_end = text.find("<!-- FINAL_CORPUS_STATUS_END -->")
    if banner_start < 0 or banner_end < banner_start:
        raise SystemExit(f"missing final-status banner: {path}")
    banner = text[banner_start:banner_end]
    banner = banner.replace("`set2_emerging`", "`set1_core`", 1)
    banner = re.sub(r"venue `[^`]*`", f"venue `{venue}`", banner, count=1)
    banner = re.sub(r"signoff `[^`]*`", "signoff `2026-08-25`", banner, count=1)
    text = text[:banner_start] + banner + text[banner_end:]

    # Refresh citation metadata only where an explicit Year/Venue field exists.
    text = re.sub(r"(?m)^(\* Year:\s*).*$", rf"\g<1>{year}", text, count=1)
    text = re.sub(r"(?m)^(\* Venue:\s*).*$", rf"\g<1>{venue}", text, count=1)
    text = re.sub(r"(?m)^(- Year:\s*).*$", rf"\g<1>{year}", text, count=1)
    text = re.sub(r"(?m)^(- Venue:\s*).*$", rf"\g<1>{venue}", text, count=1)
    if text == before:
        raise SystemExit(f"paper note did not change: {path}")
    path.write_text(text, encoding="utf-8")


def update_docs() -> None:
    replacements = {
        "| Set 1 | 92 |": "| Set 1 | 107 |",
        "| Set 2 | 97 |": "| Set 2 | 82 |",
        "**92** Set 1": "**107** Set 1",
        "**97** Set 2": "**82** Set 2",
        "92 Set 1": "107 Set 1",
        "97 Set 2": "82 Set 2",
        "Set 1 = 92": "Set 1 = 107",
        "Set 2 = 97": "Set 2 = 82",
        "Set~1 = 92": "Set~1 = 107",
        "Set~2 = 97": "Set~2 = 82",
        "Set1=92": "Set1=107",
        "Set2=97": "Set2=82",
        "Set~1: 92": "Set~1: 107",
        "Set~2: 97": "Set~2: 82",
        "Set 1: 92": "Set 1: 107",
        "Set 2: 97": "Set 2: 82",
    }
    docs = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CORPUS_SET_POLICY.md",
        ROOT / "FROZEN_SNAPSHOT.md",
        CORPUS / "README.md",
    ]
    for path in docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


def update_support_scripts() -> None:
    validator = ROOT / "scripts" / "validate_corpus.py"
    text = validator.read_text(encoding="utf-8")
    text = text.replace(
        'EXPECTED_COUNTS = {"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}',
        'EXPECTED_COUNTS = {"set1_core": 107, "set2_emerging": 82, "total_corpus": 189}',
    )
    text = text.replace("if (len(s1), len(s2)) != (92, 97):", "if (len(s1), len(s2)) != (107, 82):")
    text = text.replace(
        'print("Final corpus valid: Set1=92 Set2=97 total=189; papers=189; category and venue placement indexed; legacy active views absent")',
        'print("Final corpus valid: Set1=107 Set2=82 total=189; papers=189; category and venue placement indexed; legacy active views absent")',
    )
    validator.write_text(text, encoding="utf-8")

    builder = ROOT / "scripts" / "build_artifact_source_links.py"
    text = builder.read_text(encoding="utf-8")
    text = text.replace(
        'EXPECTED = {"set1_core": 92, "set2_emerging": 97}',
        'EXPECTED = {"set1_core": 107, "set2_emerging": 82}',
    )
    text = text.replace(
        '"Active corpus: **92 Set 1 + 97 Set 2 = 189 works**.",',
        '"Active corpus: **107 Set 1 + 82 Set 2 = 189 works**.",',
    )
    builder.write_text(text, encoding="utf-8")


def main() -> None:
    s1_fields, s1 = read_csv(CORPUS / "set1_core.csv")
    s2_fields, s2 = read_csv(CORPUS / "set2_emerging.csv")
    if s1_fields != s2_fields:
        raise SystemExit("Set 1 and Set 2 schemas differ")

    if (len(s1), len(s2)) == (107, 82):
        print("107/82 partition already applied")
        return
    if (len(s1), len(s2)) != (92, 97):
        raise SystemExit(f"unexpected starting partition: {len(s1)}/{len(s2)}")

    s1_titles = {r["title"] for r in s1}
    s2_by_title = {r["title"]: r for r in s2}
    missing = [t for t in PROMOTION_TITLES if t not in s2_by_title]
    already = [t for t in PROMOTION_TITLES if t in s1_titles]
    if missing or already:
        raise SystemExit(f"promotion precondition failed: missing={missing}, already_set1={already}")

    promoted = []
    for title in PROMOTION_TITLES:
        row = s2_by_title[title]
        promote_row(row)
        promoted.append(row)
    remaining = [r for r in s2 if r["title"] not in PROMOTION_META]
    new_s1 = s1 + promoted
    if (len(new_s1), len(remaining)) != (107, 82):
        raise SystemExit("promotion count did not produce 107/82")

    write_csv(CORPUS / "set1_core.csv", s1_fields, new_s1)
    write_csv(CORPUS / "set2_emerging.csv", s2_fields, remaining)

    index_fields, index = read_csv(PAPERS / "index.csv")
    by_title = {r["title"]: r for r in index}
    for title, venue, year in PROMOTIONS:
        item = by_title.get(title)
        if item is None:
            raise SystemExit(f"promotion missing from papers/index.csv: {title}")
        item["evidence_set"] = "set1_core"
        item["venue"] = venue
        update_note(ROOT / item["paper_path"], venue, year)
    write_csv(PAPERS / "index.csv", index_fields, index)

    # Keep the human-facing paper lists aligned with the authoritative partition.
    papers_readme = PAPERS / "README.md"
    if papers_readme.exists():
        lines = papers_readme.read_text(encoding="utf-8").splitlines()
        changed = 0
        out = []
        for line in lines:
            if any(title in line for title in PROMOTION_TITLES) and "`set2_emerging`" in line:
                line = line.replace("`set2_emerging`", "`set1_core`")
                changed += 1
            out.append(line)
        if changed != 15:
            raise SystemExit(f"expected 15 papers/README status changes, got {changed}")
        papers_readme.write_text("\n".join(out) + "\n", encoding="utf-8")

    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["counts"] = {"set1_core": 107, "set2_emerging": 82, "total_corpus": 189}
    manifest["final_signoff_date"] = "2026-08-25"
    manifest["contributions"] = dict(Counter(r["dominant_contribution"] for r in new_s1 + remaining))
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    update_docs()
    update_support_scripts()

    # Regenerate the public source-link view from the updated authoritative CSVs.
    subprocess.run(["python3", str(ROOT / "scripts" / "build_artifact_source_links.py")], check=True)
    subprocess.run(["python3", str(ROOT / "scripts" / "validate_corpus.py")], check=True)

    print("Applied human-reviewed 107/82 partition and validated the 189-work corpus")


if __name__ == "__main__":
    main()
