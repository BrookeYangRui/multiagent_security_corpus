#!/usr/bin/env python3
"""Correct OMNI-LEAK from survey-primary to attack-primary.

The paper note already identifies the work as an attack/benchmark/evaluation and
states ``Primary category: attack``.  This migration changes only dominant
contribution and derived materialized views; corpus membership and Set 2 status
remain unchanged.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEY = "naik2026omni_leak"
OLD_NOTE = ROOT / "papers/surveys/arxiv/2026_naik_omni_leak.md"
NEW_NOTE = ROOT / "papers/attacks/arxiv/2026_naik_omni_leak.md"


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


# 1. Authoritative Set 2 row.
set2_path = ROOT / "corpus/set2_emerging.csv"
fields, rows = read_csv(set2_path)
matches = [r for r in rows if r["work_key"] == KEY]
assert len(matches) == 1, f"expected one {KEY} row in Set 2, found {len(matches)}"
row = matches[0]
assert row["dominant_contribution"] == "survey", row["dominant_contribution"]
row["dominant_contribution"] = "attack"
if "emerging_direction" in row:
    row["emerging_direction"] = "attack"
correction = (
    "2026-08-24 author-directed contribution correction: the retained paper note "
    "and source-level summary identify the work as an attack/benchmark/evaluation "
    "with primary category attack; dominant_contribution corrected survey -> attack. "
    "Membership and Set 2 maturity are unchanged."
)
prior_reason = row.get("decision_reason", "").strip()
row["decision_reason"] = (prior_reason + " " + correction).strip()
write_csv(set2_path, fields, rows)

# 2. Materialized index row and note path.
index_path = ROOT / "papers/index.csv"
fields, rows = read_csv(index_path)
matches = [r for r in rows if r["work_key"] == KEY]
assert len(matches) == 1, f"expected one {KEY} row in papers/index.csv"
item = matches[0]
assert item["dominant_contribution"] == "survey", item["dominant_contribution"]
assert item["paper_path"] == "papers/surveys/arxiv/2026_naik_omni_leak.md", item["paper_path"]
item["dominant_contribution"] = "attack"
item["paper_path"] = "papers/attacks/arxiv/2026_naik_omni_leak.md"
write_csv(index_path, fields, rows)

# 3. Move the paper note and make the corrected status explicit.
assert OLD_NOTE.is_file(), f"missing old OMNI-LEAK note: {OLD_NOTE}"
assert not NEW_NOTE.exists(), f"new OMNI-LEAK note already exists: {NEW_NOTE}"
text = OLD_NOTE.read_text(encoding="utf-8")
old_banner = (
    "> **Final signed corpus status:** `set2_emerging` · `survey` · venue `arXiv` · signoff `2026-08-21`.\n"
    "> This banner is authoritative if older review prose below records an earlier classification."
)
new_banner = (
    "> **Final corpus status:** `set2_emerging` · `attack` · venue `arXiv` · contribution correction `2026-08-24`.\n"
    "> This banner is authoritative if older review prose below records an earlier classification."
)
assert old_banner in text, "unexpected OMNI-LEAK status banner"
text = text.replace(old_banner, new_banner, 1)
marker = "\n## Provenance\n"
if marker in text:
    correction_note = (
        "\n## Contribution correction\n\n"
        "The active corpus records this work as attack-primary. Its central contribution "
        "is the demonstrated cross-agent data-exfiltration attack and accompanying benchmark; "
        "it is not a survey. The correction does not change corpus membership or maturity.\n"
    )
    text = text.replace(marker, correction_note + marker, 1)
NEW_NOTE.parent.mkdir(parents=True, exist_ok=True)
NEW_NOTE.write_text(text, encoding="utf-8")
OLD_NOTE.unlink()

# 4. Update the two category indexes.
attack_readme = ROOT / "papers/attacks/README.md"
text = attack_readme.read_text(encoding="utf-8")
assert "Final 189-corpus dominant-contribution count: **46**." in text
text = text.replace(
    "Final 189-corpus dominant-contribution count: **46**.",
    "Final 189-corpus dominant-contribution count: **47**.",
    1,
)
anchor = (
    "* [Many-to-One Adversarial Consensus: Exposing Multi-Agent Collusion Risks in AI-Based Healthcare]"
    "(arxiv/2025_many_to_one_adversarial_consensus_exposing_multi_agent_collusion_risks_i.md)  `set2_emerging`\n"
)
assert anchor in text, "attack README insertion anchor not found"
omni_line = (
    "* [OMNI-LEAK: Orchestrator Multi-Agent Network Induced Data Leakage]"
    "(arxiv/2026_naik_omni_leak.md)  `set2_emerging`\n"
)
text = text.replace(anchor, anchor + omni_line, 1)
attack_readme.write_text(text, encoding="utf-8")

survey_readme = ROOT / "papers/surveys/README.md"
text = survey_readme.read_text(encoding="utf-8")
assert "Final 189-corpus dominant-contribution count: **7**." in text
text = text.replace(
    "Final 189-corpus dominant-contribution count: **7**.",
    "Final 189-corpus dominant-contribution count: **6**.",
    1,
)
omni_block = (
    "## arxiv\n\n"
    "* [OMNI-LEAK: Orchestrator Multi-Agent Network Induced Data Leakage]"
    "(arxiv/2026_naik_omni_leak.md)  `set2_emerging`\n\n"
)
assert omni_block in text, "survey README OMNI-LEAK block not found"
text = text.replace(omni_block, "", 1)
survey_readme.write_text(text, encoding="utf-8")

# 5. Update current corpus summaries and validator invariants.
replacements = {
    ROOT / "README.md": [
        ("**46 attacks**", "**47 attacks**"),
        ("**7 surveys**", "**6 surveys**"),
    ],
    ROOT / "AGENTS.md": [
        ("46 attacks", "47 attacks"),
        ("7 surveys", "6 surveys"),
    ],
    ROOT / "CORPUS_SET_POLICY.md": [
        ("46 attacks", "47 attacks"),
        ("7 surveys", "6 surveys"),
    ],
    ROOT / "papers/README.md": [
        ("| attack | 46 |", "| attack | 47 |"),
        ("| survey | 7 |", "| survey | 6 |"),
    ],
    ROOT / "related_work/attacks.md": [
        ("**46 attack-primary works**", "**47 attack-primary works**"),
        ("so 46 is not", "so 47 is not"),
    ],
    ROOT / "related_work/surveys_and_soks.md": [
        ("**7 survey-primary works**", "**6 survey-primary works**"),
    ],
    ROOT / "scripts/validate_corpus.py": [
        ('"attack": 46', '"attack": 47'),
        ('"survey": 7', '"survey": 6'),
    ],
}
for path, pairs in replacements.items():
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in text, f"expected text not found in {path.relative_to(ROOT)}: {old}"
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

print("OMNI-LEAK corrected: Set 2 attack-primary; corpus remains 92 + 97 = 189; contributions 47/80/44/12/6")
