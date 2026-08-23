#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
PAPERS = ROOT / "papers"
TODAY = "2026-08-23"


def read_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows):
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def make_row(fields, **values):
    row = {k: "" for k in fields}
    row.update(values)
    return row


def replace_text(path: Path, replacements: list[tuple[str, str]]):
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8")


s1_path = CORPUS / "set1_core.csv"
s2_path = CORPUS / "set2_emerging.csv"
s1 = read_rows(s1_path)
s2 = read_rows(s2_path)
fields = list(s1[0].keys())

whispering_key = "doi:10.1609/aaai.v40i37.40380"
tool_key = "arxiv:2606.28425"

if whispering_key not in {r["work_key"] for r in s1 + s2}:
    s1.append(make_row(
        fields,
        work_key=whispering_key,
        canonical_paper_id="huang2026whispering_agents",
        title="Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents",
        publication_date="2026-03-14",
        year="2026",
        venue="AAAI",
        doi="10.1609/aaai.v40i37.40380",
        arxiv_id="",
        primary_url="https://ojs.aaai.org/index.php/AAAI/article/view/40380",
        evidence_set="set1_core",
        strict_scope_pass="yes",
        scope_reason="The paper studies separately addressable LLM agents communicating through a covert event channel, with communication privacy and monitor evasion defined over the inter-agent relation.",
        peer_reviewed="yes",
        peer_review_basis="AAAI 2026 proceedings metadata and DOI",
        frozen_citation_count="0",
        citation_count_source="source re-audit",
        citation_count_field="frozen_citation_count",
        citation_snapshot_date=TODAY,
        maturity_rule_pass="yes",
        dominant_contribution="evaluation",
        interaction_interfaces="I2_communication_routing;I6_observation_defense",
        risk_or_property="R5_private_data_leakage",
        interaction_dependence="structurally_multi_agent",
        emerging_direction="",
        citation_role="primary",
        paper_section="full_text",
        evidence_basis="The work formalizes the Covert Event Channel and Pi-CCAP for agent-to-agent covert communication, then evaluates capacity, robustness, and imperceptibility to LLM-based wardens.",
        evidence_locator="AAAI 2026 paper, Abstract and evaluation; DOI 10.1609/aaai.v40i37.40380",
        source_files="AAAI official article and PDF; 2026-08-23 source re-audit",
        decision_reason="Restored on 2026-08-23 after source re-audit confirmed that covert communication privacy and monitor evasion are relational MAS security properties, not merely a generic multi-agent application.",
        previous_decision="omitted_from_active_corpus",
        previous_category="evaluation",
        reviewer="OpenAI GPT-5.6 Sol, source verification; Rui Yang, explicit corpus restoration",
        reviewed_at=TODAY,
        author_signoff_required="no",
        taxonomy_ready="yes",
        membership_reason="Passed strict MAS-security scope. The security object is covert communication between LLM agents and its detectability by an observer. Peer-reviewed AAAI 2026 publication satisfies the Set 1 maturity rule.",
    ))

if tool_key not in {r["work_key"] for r in s1 + s2}:
    s2.append(make_row(
        fields,
        work_key=tool_key,
        canonical_paper_id="arxiv_2606_28425",
        title="Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems",
        publication_date="2026-06-25",
        year="2026",
        venue="arXiv",
        doi="10.48550/arXiv.2606.28425",
        arxiv_id="2606.28425",
        primary_url="https://arxiv.org/abs/2606.28425",
        evidence_set="set2_emerging",
        strict_scope_pass="yes",
        scope_reason="Two LLM agents independently construct and select covert-channel schemes; the studied collusion and steganographic communication property is inherently inter-agent.",
        peer_reviewed="no",
        peer_review_basis="arXiv preprint",
        frozen_citation_count="0",
        citation_count_source="source re-audit",
        citation_count_field="frozen_citation_count",
        citation_snapshot_date=TODAY,
        maturity_rule_pass="no",
        dominant_contribution="attack",
        interaction_interfaces="I2_communication_routing;I4_delegation_action;I6_observation_defense",
        risk_or_property="R3_collective_integrity;R5_private_data_leakage",
        interaction_dependence="structurally_multi_agent",
        emerging_direction="attack",
        citation_role="primary",
        paper_section="full_text",
        evidence_basis="The study shows that tool-using LLM agents can implement covert stegosystems and formalizes tacit coordination as a Schelling-point problem with empirical coordination metrics.",
        evidence_locator="arXiv:2606.28425, Abstract and Sections 3.2.1 and 4.2; historical systematic full-text screen marked include-primary-interaction-security",
        source_files="arXiv primary paper; historical systematic full-text screening; 2026-08-23 source re-audit",
        decision_reason="Restored on 2026-08-23 because the prior full-text screen already established primary interaction-security evidence and the work was public before the 2026-07-01 cutoff.",
        previous_decision="omitted_from_active_corpus",
        previous_category="attack",
        reviewer="OpenAI GPT-5.6 Sol, source verification; Rui Yang, explicit corpus restoration",
        reviewed_at=TODAY,
        author_signoff_required="no",
        taxonomy_ready="yes",
        membership_reason="Passed strict MAS-security scope. The attack object is covert inter-agent communication and collusive coordination under monitoring. Preprint status places the work in Set 2.",
    ))

write_rows(s1_path, s1)
write_rows(s2_path, s2)

# Update manifest.
manifest_path = CORPUS / "manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["final_signoff_date"] = TODAY
manifest["counts"] = {"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}
manifest["contributions"] = {"attack": 45, "defense": 80, "evaluation": 45, "general": 12, "survey": 7}
manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

# Add exact materialized paper index rows.
index_path = PAPERS / "index.csv"
index = read_rows(index_path)
index_fields = list(index[0].keys())
index_keys = {r["work_key"] for r in index}
if whispering_key not in index_keys:
    index.append(make_row(
        index_fields,
        work_key=whispering_key,
        title="Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents",
        evidence_set="set1_core",
        dominant_contribution="evaluation",
        venue="AAAI",
        venue_folder="aaai",
        paper_path="papers/evaluations/aaai/2026_huang_whispering_agents.md",
    ))
if tool_key not in index_keys:
    index.append(make_row(
        index_fields,
        work_key=tool_key,
        title="Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems",
        evidence_set="set2_emerging",
        dominant_contribution="attack",
        venue="arXiv",
        venue_folder="arxiv",
        paper_path="papers/attacks/arxiv/2026_tool_use_enables_undetectable_steganography.md",
    ))
write_rows(index_path, index)

# Add paper notes required by the exact materialized view.
whispering_note = PAPERS / "evaluations" / "aaai" / "2026_huang_whispering_agents.md"
whispering_note.parent.mkdir(parents=True, exist_ok=True)
whispering_note.write_text("""# Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `evaluation` · venue `AAAI` · signoff `2026-08-23`.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation metadata

* Authors: Kaibo Huang, Yukun Wei, Wansheng Wu, Tianhua Zhang, Zhongliang Yang, Linna Zhou
* Year: 2026
* Venue: AAAI 2026
* DOI: 10.1609/aaai.v40i37.40380
* Published: 2026-03-14
* Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40380

## Final corpus classification

* Work key: `doi:10.1609/aaai.v40i37.40380`
* Evidence set: `set1_core`
* Dominant contribution: `evaluation`
* Interaction interfaces: `I2_communication_routing;I6_observation_defense`
* Risk or property: `R5_private_data_leakage`
* Interaction dependence: `structurally_multi_agent`

## Evidence summary

The paper formalizes a Covert Event Channel for agent-to-agent communication and implements Pi-CCAP across storage, timing, and behavioral channels. Its evaluation measures capacity, robustness, and imperceptibility to LLM-based wardens. The protected and adversarial object is relational: the existence and detectability of communication between agents.

## Restoration note

Restored to the active corpus on 2026-08-23 after source re-audit confirmed that this is a peer-reviewed MAS security study rather than a generic multi-agent application. The PDF uses “An Event-Driven” in the title while the AAAI metadata page renders “A Event-Driven.”
""", encoding="utf-8")

tool_note = PAPERS / "attacks" / "arxiv" / "2026_tool_use_enables_undetectable_steganography.md"
tool_note.parent.mkdir(parents=True, exist_ok=True)
tool_note.write_text("""# Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · signoff `2026-08-23`.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation metadata

* Authors: Jimmy Laurence Rippin, Simon C. Marshall, David Demitri Africa, Christian Schroeder de Witt
* Year: 2026
* Venue: arXiv
* DOI: 10.48550/arXiv.2606.28425
* arXiv: 2606.28425
* First public: 2026-06-25
* Primary URL: https://arxiv.org/abs/2606.28425

## Final corpus classification

* Work key: `arxiv:2606.28425`
* Evidence set: `set2_emerging`
* Dominant contribution: `attack`
* Interaction interfaces: `I2_communication_routing;I4_delegation_action;I6_observation_defense`
* Risk or property: `R3_collective_integrity;R5_private_data_leakage`
* Interaction dependence: `structurally_multi_agent`

## Evidence summary

The paper demonstrates that tool-using agentic models can construct sophisticated covert stegosystems and studies whether independently acting agents converge on compatible schemes. It formalizes tacit steganographic coordination as a Schelling-point problem and evaluates coordination across schemes, keys, and parameters. The historical systematic full-text screen already classified the work as `include-primary-interaction-security`.

## Restoration note

Restored to the active corpus on 2026-08-23. It was publicly available before the frozen 2026-07-01 cutoff and directly studies covert inter-agent communication, collusion, and monitor evasion.
""", encoding="utf-8")

# Update corpus counts in maintenance and synthesis documentation.
common_replacements = [
    ("**187 works**", "**189 works**"),
    ("187 works", "189 works"),
    ("187-work", "189-work"),
    ("187 work", "189 work"),
    ("active 187", "active 189"),
    ("same 187", "same 189"),
    ("Set 1 | 91 |", "Set 1 | 92 |"),
    ("Set 2 | 96 |", "Set 2 | 97 |"),
    ("`set1_core.csv` | 91 |", "`set1_core.csv` | 92 |"),
    ("`set2_emerging.csv` | 96 |", "`set2_emerging.csv` | 97 |"),
    ("Set 1 = 91", "Set 1 = 92"),
    ("Set 2 = 96", "Set 2 = 97"),
    ("total = 187", "total = 189"),
    ("91 mature in-scope works", "92 mature in-scope works"),
    ("96 emerging in-scope works", "97 emerging in-scope works"),
    ("**91 Set 1** and **96 Set 2**", "**92 Set 1** and **97 Set 2**"),
    ("**44 attacks**, **80 defenses**, **44 evaluations**, **12 general works**, and **7 surveys**", "**45 attacks**, **80 defenses**, **45 evaluations**, **12 general works**, and **7 surveys**"),
    ("**44 attacks, 80 defenses, 44 evaluations, 12 general works, and 7 surveys**", "**45 attacks, 80 defenses, 45 evaluations, 12 general works, and 7 surveys**"),
    ("44/80/44/12/7", "45/80/45/12/7"),
    ("| attack | 44 |", "| attack | 45 |"),
    ("| evaluation | 44 |", "| evaluation | 45 |"),
]
for rel in [
    "README.md", "AGENTS.md", "CORPUS_SET_POLICY.md", "FROZEN_SNAPSHOT.md",
    "corpus/README.md", "papers/README.md", "sok_related/README.md",
    "related_work/attacks.md", "related_work/benchmarks.md", "related_work/surveys_and_soks.md",
]:
    path = ROOT / rel
    if path.exists():
        replace_text(path, common_replacements)

# Make the same-day restoration explicit in the top-level README.
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
marker = "CoMet, DACS, and NOD remain in scope."
addition = " CoMet, DACS, and NOD remain in scope. A same-day source re-audit also restored Whispering Agents and Tool Use Enables Undetectable Steganography because both directly study relational MAS security properties."
if marker in text and "same-day source re-audit also restored" not in text:
    text = text.replace(marker, addition)
    readme.write_text(text, encoding="utf-8")

# Update contribution README counts and insert the two paper links.
attack_readme = PAPERS / "attacks" / "README.md"
replace_text(attack_readme, [("Final 187-corpus dominant-contribution count: **44**.", "Final 189-corpus dominant-contribution count: **45**.")])
a_text = attack_readme.read_text(encoding="utf-8")
a_bullet = "* [Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems](arxiv/2026_tool_use_enables_undetectable_steganography.md)  `set2_emerging`\n"
if a_bullet not in a_text:
    a_text = a_text.replace("## arxiv\n\n", "## arxiv\n\n" + a_bullet)
    attack_readme.write_text(a_text, encoding="utf-8")

eval_readme = PAPERS / "evaluations" / "README.md"
replace_text(eval_readme, [("Final 187-corpus dominant-contribution count: **44**.", "Final 189-corpus dominant-contribution count: **45**.")])
e_text = eval_readme.read_text(encoding="utf-8")
e_bullet = "* [Whispering Agents: An Event-Driven Covert Communication Protocol for the Internet of Agents](aaai/2026_huang_whispering_agents.md)  `set1_core`\n"
if e_bullet not in e_text:
    e_text = e_text.replace("## aaai\n\n", "## aaai\n\n" + e_bullet)
    eval_readme.write_text(e_text, encoding="utf-8")

# Update validator invariants to the restored 189-work corpus.
validator = ROOT / "scripts" / "validate_corpus.py"
vtext = validator.read_text(encoding="utf-8")n