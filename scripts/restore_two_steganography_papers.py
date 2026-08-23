#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
P = ROOT / "papers"

WHISPER_KEY = "doi:10.1609/aaai.v40i37.40380"
TOOL_KEY = "arxiv:2606.28425"


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows):
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)


def blank_like(row):
    return {k: "" for k in row.keys()}

s1 = read_csv(C / "set1_core.csv")
s2 = read_csv(C / "set2_emerging.csv")
existing = {r["work_key"] for r in s1 + s2}
if WHISPER_KEY in existing or TOOL_KEY in existing:
    raise SystemExit("one of the restoration records already exists")

w = blank_like(s1[0])
w.update({
    "work_key": WHISPER_KEY,
    "canonical_paper_id": "huang2026whispering",
    "title": "Whispering Agents: A Event-Driven Covert Communication Protocol for the Internet of Agents",
    "publication_date": "2026-03-14",
    "year": "2026",
    "venue": "AAAI",
    "doi": "10.1609/aaai.v40i37.40380",
    "arxiv_id": "2508.02188",
    "primary_url": "https://ojs.aaai.org/index.php/AAAI/article/view/40380",
    "evidence_set": "set1_core",
    "strict_scope_pass": "yes",
    "scope_reason": "The paper studies covert communication between separately addressable LLM agents over event-driven A2A interaction and evaluates imperceptibility against LLM wardens; the security property is relational communication privacy and monitor evasion.",
    "peer_reviewed": "yes",
    "peer_review_basis": "AAAI 2026 proceedings",
    "frozen_citation_count": "0",
    "citation_count_source": "not needed for Set 1; peer reviewed",
    "citation_count_field": "restoration_review",
    "citation_snapshot_date": "2026-08-17",
    "maturity_rule_pass": "yes",
    "dominant_contribution": "attack",
    "interaction_interfaces": "I2_communication_routing;I6_observation_defense",
    "risk_or_property": "R5_private_data_leakage",
    "interaction_dependence": "structurally_multi_agent",
    "emerging_direction": "covert communication;monitor evasion",
    "citation_role": "primary",
    "paper_section": "full_text",
    "evidence_basis": "AAAI 2026 official article and extended arXiv version 2508.02188",
    "evidence_locator": "https://ojs.aaai.org/index.php/AAAI/article/view/40380 ; https://arxiv.org/abs/2508.02188",
    "source_files": "AAAI official article ; arXiv:2508.02188",
    "decision_reason": "Restored on 2026-08-23 after explicit scope re-check: the Covert Event Channel and Pi-CCAP are interaction-native MAS security mechanisms and the paper evaluates evasion of LLM-based wardens.",
    "previous_decision": "excluded_or_missing_from_active_view",
    "previous_category": "attack",
    "reviewer": "OpenAI GPT-5.6 Sol source review; author restoration decision",
    "reviewed_at": "2026-08-23",
    "author_signoff_required": "no",
    "taxonomy_ready": "yes",
    "membership_reason": "Peer-reviewed AAAI work within the 2026-07-01 cutoff; direct MAS covert-channel security evidence.",
})

t = blank_like(s2[0])
t.update({
    "work_key": TOOL_KEY,
    "canonical_paper_id": "rippin2026toolstego",
    "title": "Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems",
    "publication_date": "2026-06-25",
    "year": "2026",
    "venue": "arXiv",
    "doi": "10.48550/arXiv.2606.28425",
    "arxiv_id": "2606.28425",
    "primary_url": "https://arxiv.org/abs/2606.28425",
    "evidence_set": "set2_emerging",
    "strict_scope_pass": "yes",
    "scope_reason": "The threat model explicitly contains a sender and receiver connected by a monitored natural-language channel, with covert information transfer and monitor evasion depending on inter-agent communication and tacit coordination.",
    "peer_reviewed": "no",
    "peer_review_basis": "arXiv preprint",
    "frozen_citation_count": "0",
    "citation_count_source": "restoration review",
    "citation_count_field": "restoration_review",
    "citation_snapshot_date": "2026-08-17",
    "maturity_rule_pass": "no",
    "dominant_contribution": "attack",
    "interaction_interfaces": "I2_communication_routing;I6_observation_defense",
    "risk_or_property": "R5_private_data_leakage",
    "interaction_dependence": "structurally_multi_agent",
    "emerging_direction": "tool-enabled steganography;tacit coordination;monitor evasion",
    "citation_role": "primary",
    "paper_section": "full_text",
    "evidence_basis": "arXiv full text 2606.28425",
    "evidence_locator": "https://arxiv.org/abs/2606.28425",
    "source_files": "arXiv:2606.28425",
    "decision_reason": "Restored on 2026-08-23 after explicit scope re-check: the paper directly studies covert channels, information-flow violations, monitored inter-agent communication, and tacit coordination in MAS.",
    "previous_decision": "excluded_or_missing_from_active_view",
    "previous_category": "attack",
    "reviewer": "OpenAI GPT-5.6 Sol source review; author restoration decision",
    "reviewed_at": "2026-08-23",
    "author_signoff_required": "no",
    "taxonomy_ready": "yes",
    "membership_reason": "Public before the 2026-07-01 cutoff and directly within strict MAS-security scope; emerging because it is an unreviewed preprint.",
})

s1.append(w); s2.append(t)
write_csv(C / "set1_core.csv", s1)
write_csv(C / "set2_emerging.csv", s2)

notes = {
    "papers/attacks/aaai/2026_huang_whispering_agents.md": """# Whispering Agents: A Event-Driven Covert Communication Protocol for the Internet of Agents

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set1_core` · `attack` · venue `AAAI` · restoration `2026-08-23`.
> This banner is authoritative for current corpus membership.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Kaibo Huang, Yukun Wei, Wansheng Wu, Tianhua Zhang, Zhongliang Yang, Linna Zhou
- Year: 2026
- Venue: AAAI 2026
- DOI: 10.1609/aaai.v40i37.40380
- arXiv: 2508.02188
- Primary URL: https://ojs.aaai.org/index.php/AAAI/article/view/40380

## Paper Type

Attack; covert-channel protocol; empirical security evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

Internet-of-Agents settings where LLM-backed agents communicate through event-driven A2A interactions while a warden observes their overt behavior.

### Multi-Agent Dependency

The covert channel exists across interacting agents and encodes a hidden dialogue through storage, timing, and behavioral event patterns. The protected and violated property is therefore relational: whether communication between agents can be observed and controlled.

## Security Model

- Protected property: communication privacy, traffic-analysis resistance, and monitoring integrity.
- Threat capability: agents coordinate a covert event channel within otherwise benign-looking interactions.
- Defender: an LLM-based warden monitoring the observable agent interaction.

## Main Contribution

The paper formalizes the Covert Event Channel and engineers Pi-CCAP, an event-driven covert communication protocol spanning storage, timing, and behavioral channels.

## Attack or Failure

The protocol hides the existence and content of inter-agent communication inside normal-looking agent events, creating a covert channel that can evade traffic analysis and LLM-based monitoring.

## Evaluation

The official AAAI paper reports that Pi-CCAP provides high capacity and robustness while remaining imperceptible to strong LLM-based wardens in the evaluated settings.

## Relevance to Our SoK

This is direct MAS-security evidence for covert communication and monitoring-evasion attacks at the communication and observation interfaces. It is not merely a multi-agent application used to solve a separate security task.

## Source Review

Primary sources checked for restoration: AAAI 2026 proceedings article and extended arXiv version 2508.02188. The paper is peer reviewed and predates the 2026-07-01 literature cutoff through its published AAAI version.
""",
    "papers/attacks/arxiv/2026_rippin_tool_use_steganography.md": """# Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems

<!-- FINAL_CORPUS_STATUS_START -->
> **Final signed corpus status:** `set2_emerging` · `attack` · venue `arXiv` · restoration `2026-08-23`.
> This banner is authoritative for current corpus membership.
<!-- FINAL_CORPUS_STATUS_END -->

## Citation

- Authors: Jimmy Laurence Rippin, Simon C. Marshall, David Demitri Africa, Christian Schroeder de Witt
- Year: 2026
- Venue: arXiv
- DOI: 10.48550/arXiv.2606.28425
- arXiv: 2606.28425
- Primary URL: https://arxiv.org/abs/2606.28425

## Paper Type

Attack capability study; covert communication; security evaluation

- Primary category: `attack`
- Scope relation: `core_security`

## Scope

### System Studied

A multi-agent system with at least a sender and receiver connected by a monitored natural-language channel, plus realistic agentic tool access such as code execution, files, model sampling, and web search.

### Multi-Agent Dependency

The security failure is covert information transfer from one principal to another despite complete observation of the overt message channel. The paper separately studies whether agents can tacitly converge on compatible steganographic schemes without explicit agreement.

## Security Model

- Protected property: information-flow confidentiality and effectiveness of content-level monitoring.
- Threat actor: an agent attempting to transmit restricted information covertly to a cooperating receiver.
- Defender: a monitor that sees agent outputs but lacks the secret key and may lack visibility into tools and intermediate artifacts.

## Main Contribution

The paper introduces an agentic covert-channel construction benchmark, shows that tool-using agents can operationalize sophisticated stegosystems, and frames tacit steganographic agreement as a Schelling-point coordination problem.

## Attack or Failure

Agents use tools to construct hidden natural-language channels that can carry prohibited information through apparently benign text, defeating the assumption that readable inter-agent messages are sufficient for information-flow enforcement.

## Evaluation

The paper evaluates implementation success under progressively restricted tool environments and measures algorithmic, hyperparameter, and complete coordination between independently acting agents.

## Relevance to Our SoK

This is direct interaction-dependent MAS-security evidence for covert communication, collusion, information-flow violations, and monitor evasion. The sender-receiver relation and monitored channel are part of the threat model rather than incidental experimental machinery.

## Source Review

Primary source checked for restoration: arXiv 2606.28425, first posted 2026-06-25, before the 2026-07-01 literature cutoff. It remains Set 2 because it is a non-peer-reviewed preprint under the frozen maturity rule.
""",
}
for rel, text in notes.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

idx = read_csv(P / "index.csv")
idx.extend([
    {"work_key": WHISPER_KEY, "title": w["title"], "evidence_set": "set1_core", "dominant_contribution": "attack", "venue": "AAAI", "venue_folder": "aaai", "paper_path": "papers/attacks/aaai/2026_huang_whispering_agents.md"},
    {"work_key": TOOL_KEY, "title": t["title"], "evidence_set": "set2_emerging", "dominant_contribution": "attack", "venue": "arXiv", "venue_folder": "arxiv", "paper_path": "papers/attacks/arxiv/2026_rippin_tool_use_steganography.md"},
])
write_csv(P / "index.csv", idx)

manifest = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
manifest["counts"] = {"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}
manifest["contributions"] = {"attack": 46, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}
(C / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

# Update maintenance and synthesis prose without changing historical audit files.
text_files = [
    ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "CORPUS_SET_POLICY.md", ROOT / "FROZEN_SNAPSHOT.md",
    C / "README.md", P / "README.md", ROOT / "sok_related" / "README.md",
]
text_files.extend((ROOT / "related_work").glob("*.md"))
for path in text_files:
    text = path.read_text(encoding="utf-8")
    text = text.replace("187-work", "189-work").replace("187 works", "189 works").replace("active 187", "active 189")
    text = text.replace("91 mature", "92 mature").replace("96 emerging", "97 emerging")
    text = text.replace("Set 1 = 91", "Set 1 = 92").replace("Set 2 = 96", "Set 2 = 97")
    text = text.replace("91 Set 1", "92 Set 1").replace("96 Set 2", "97 Set 2")
    text = text.replace("44 attacks", "46 attacks").replace("44 attack-primary works", "46 attack-primary works")
    path.write_text(text, encoding="utf-8")

# Regenerate category README files from the exact index.
category_dirs = {"attack":"attacks","defense":"defenses","evaluation":"evaluations","general":"general","survey":"surveys"}
for cat, dirname in category_dirs.items():
    rows_cat = [r for r in idx if r["dominant_contribution"] == cat]
    by = {}
    for r in rows_cat:
        by.setdefault(r["venue_folder"], []).append(r)
    lines = [f"# {cat.title()} papers", "", f"Final 189-corpus dominant-contribution count: **{len(rows_cat)}**.", ""]
    for venue in sorted(by):
        lines.extend([f"## {venue}", ""])
        for r in sorted(by[venue], key=lambda x: x["title"].lower()):
            rel = Path(r["paper_path"]).relative_to(Path("papers") / dirname)
            lines.append(f"* [{r['title']}]({rel.as_posix()})  `{r['evidence_set']}`")
        lines.append("")
    (P / dirname / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

# Pin validation to the restored corpus.
vpath = ROOT / "scripts" / "validate_corpus.py"
v = vpath.read_text(encoding="utf-8")
v = v.replace('{"set1_core": 91, "set2_emerging": 96, "total_corpus": 187}', '{"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}')
v = v.replace('{"attack": 44, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}', '{"attack": 46, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}')
v = v.replace('(91, 96)', '(92, 97)').replace('!= 187', '!= 189').replace('not 187', 'not 189')
v = v.replace('active 187 corpus', 'active 189 corpus').replace('must have 187 rows', 'must have 189 rows')
v = v.replace('!= 187:\n    raise SystemExit("duplicate work_key in papers/index.csv")', '!= 189:\n    raise SystemExit("duplicate work_key in papers/index.csv")')
v = v.replace('expected exactly 187 paper notes', 'expected exactly 189 paper notes')
v = v.replace('Set1=91 Set2=96 total=187; papers=187;', 'Set1=92 Set2=97 total=189; papers=189;')
vpath.write_text(v, encoding="utf-8")

# Assert the result before CI.
all_rows = s1 + s2
counts = Counter(r["dominant_contribution"] for r in all_rows)
expected = {"attack":46,"defense":80,"evaluation":44,"general":12,"survey":7}
if len(s1) != 92 or len(s2) != 97 or len(all_rows) != 189 or dict(counts) != expected:
    raise SystemExit(f"restoration count mismatch: {len(s1)}/{len(s2)} {dict(counts)}")
print("Restored Whispering Agents and Tool Use steganography: Set1=92 Set2=97 total=189")
