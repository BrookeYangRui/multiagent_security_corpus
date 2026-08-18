#!/usr/bin/env python3
"""Apply the 2026-08-18 evaluation + benchmark reconciliation to the frozen corpus.

This script is intentionally one-shot and explicit.  It consumes the two row-level
adjudication ledgers under ``corpus/adjudication/``, updates the frozen review ledger,
adds the missing A2ASecBench canonical record, fixes the MASLeak version identity,
and then delegates deterministic set regeneration to
``rebuild_membership_from_ledger.py``.

It also creates a manuscript-facing human review queue.  All rows remain
model-assisted and require named-author signoff before being described as human
verified.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
ADJ = CORPUS / "adjudication"
DATE = "2026-08-18"
REVIEWER = "OpenAI GPT-5.6 Pro, model-assisted source review"

EXPECTED_FINAL = {
    "set1_core": 105,
    "set2_emerging": 121,
    "set3_context": 448,
    "screened_out": 1543,
}
EXPECTED_SET1_CONTRIB = {
    "attack": 33,
    "defense": 39,
    "evaluation": 21,
    "general": 7,
    "survey": 5,
}
EXPECTED_SET2_CONTRIB = {
    "attack": 38,
    "defense": 61,
    "evaluation": 15,
    "general": 4,
    "survey": 3,
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def norm_title(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).split())


def paper_section_for_role(role: str) -> str:
    return {
        "measurement_context": "Evaluation",
        "deployment_evidence": "Introduction and Threat Model",
        "related_work": "Overview and Related Work",
        "protocol_or_standard": "System Model and Defenses",
        "agentic_security_context": "Introduction and Related Work",
        "defense_analogy": "Defenses",
    }.get(role, "Overview and Related Work")


def main() -> int:
    ledger_path = CORPUS / "review_ledger.csv"
    ledger = read_csv(ledger_path)
    if len(ledger) != 2216:
        raise SystemExit(f"expected frozen 2216-row ledger before reconciliation, got {len(ledger)}")

    fields = list(ledger[0].keys())
    before_by_key = {row.get("work_key", ""): dict(row) for row in ledger}
    before_by_title = {norm_title(row.get("title", "")): dict(row) for row in ledger}

    def indexes() -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
        return (
            {row.get("work_key", ""): row for row in ledger},
            {norm_title(row.get("title", "")): row for row in ledger},
        )

    def find_row(*, work_key: str = "", title: str = "") -> dict[str, str]:
        by_key, by_title = indexes()
        if work_key and work_key in by_key:
            return by_key[work_key]
        nt = norm_title(title)
        if nt and nt in by_title:
            return by_title[nt]
        raise KeyError(f"unable to resolve corpus row: work_key={work_key!r} title={title!r}")

    changed: dict[str, dict[str, str]] = {}

    def remember(row: dict[str, str], *, action: str, reason: str, confidence: str) -> None:
        key = row.get("work_key", "") or norm_title(row.get("title", ""))
        old = before_by_key.get(row.get("work_key", "")) or before_by_title.get(norm_title(row.get("title", ""))) or {}
        changed[key] = {
            "change_type": action,
            "work_key": row.get("work_key", ""),
            "title": row.get("title", ""),
            "previous_membership": old.get("evidence_set", "not_in_frozen_ledger"),
            "proposed_membership": row.get("evidence_set", ""),
            "previous_contribution": old.get("dominant_contribution", ""),
            "proposed_contribution": row.get("dominant_contribution", ""),
            "reason_code": reason,
            "confidence": confidence,
            "human_decision": "",
            "human_notes": "",
        }

    def move_to_context(row: dict[str, str], role: str, reason: str, confidence: str, action: str) -> None:
        row["strict_scope_pass"] = "no"
        row["evidence_set"] = "set3_context"
        row["citation_role"] = role or "measurement_context"
        row["paper_section"] = paper_section_for_role(row["citation_role"])
        row["scope_reason"] = (
            "2026-08-18 adjudication: the work is useful context but the protected property or "
            "headline evaluation is not substantively MAS security under the frozen scope gate."
        )
        row["decision_reason"] = f"2026-08-18 adjudication: {reason}. Moved to Set 3 context."
        row["reviewer"] = REVIEWER
        row["reviewed_at"] = DATE
        row["author_signoff_required"] = "yes"
        remember(row, action=action, reason=reason, confidence=confidence)

    # 1) Apply the complete 44-row evaluation-primary audit.
    evaluation = read_csv(ADJ / "evaluation_scope_2026-08-18.csv")
    if len(evaluation) != 44:
        raise SystemExit(f"evaluation adjudication must have 44 rows, got {len(evaluation)}")
    eval_moves = [row for row in evaluation if row.get("decision") == "move"]
    if len(eval_moves) != 17:
        raise SystemExit(f"evaluation adjudication must contain 17 moves, got {len(eval_moves)}")
    moved_titles: set[str] = set()
    for decision in eval_moves:
        row = find_row(title=decision["title"])
        if row.get("evidence_set") not in {"set1_core", "set2_emerging"}:
            raise SystemExit(f"evaluation move is not active before application: {decision['title']}")
        moved_titles.add(norm_title(decision["title"]))
        move_to_context(
            row,
            decision.get("target_role") or "measurement_context",
            decision["reason_code"],
            decision.get("confidence", ""),
            "evaluation_scope_move",
        )

    # 2) Reconcile the broader 44-paper benchmark/report population.
    benchmark = read_csv(ADJ / "benchmark_reconciliation_2026-08-18.csv")
    if len(benchmark) != 44:
        raise SystemExit(f"benchmark reconciliation must have 44 rows, got {len(benchmark)}")

    # Known emerging records must remain Set 2 even when the venue label could be ambiguous.
    force_emerging_peer = {
        "lemercier2026gambit": ("no", "arXiv preprint"),
        "zhu2025_collaborative_shadows": ("no", "arXiv preprint"),
        "zhao2026macbench": ("no", "arXiv preprint"),
        "arora2026safeagents": ("unclear", "workshop peer-review status not established in this adjudication"),
    }

    for decision in benchmark:
        action = decision.get("action", "")
        if action in {"keep", "keep_set3", "post_cutoff"}:
            continue

        if action == "add_set1":
            # A2ASecBench has a canonical full source note but was absent from the generated ledger.
            if any(row.get("work_key") == "li2026a2asecbench" for row in ledger):
                raise SystemExit("A2ASecBench unexpectedly already exists in review_ledger.csv")
            row = {field: "" for field in fields}
            row.update({
                "work_key": "li2026a2asecbench",
                "canonical_paper_id": "li2026a2asecbench",
                "title": "A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems",
                "publication_date": "2026-01-01",
                "year": "2026",
                "venue": "ICLR 2026",
                "doi": "",
                "arxiv_id": "",
                "primary_url": "https://openreview.net/forum?id=LfdFnakqGJ",
                "evidence_set": "set1_core",
                "strict_scope_pass": "yes",
                "scope_reason": "Published protocol-aware benchmark whose attacks target A2A discovery, task state, remote requests, and returned artifacts across separately addressable agents.",
                "peer_reviewed": "yes",
                "peer_review_basis": "published ICLR 2026 conference paper",
                "frozen_citation_count": "0",
                "citation_count_source": "frozen corpus correction",
                "citation_count_field": "not re-snapshotted",
                "citation_snapshot_date": "2026-08-17",
                "maturity_rule_pass": "yes",
                "dominant_contribution": "evaluation",
                "interaction_interfaces": "I1_boundary_admission;I2_communication_routing;I4_delegation_action",
                "risk_or_property": "R5_private_data_leakage;R6_authority_misuse;R7_availability_cost",
                "interaction_dependence": "interaction_dependent_mechanism",
                "emerging_direction": "",
                "citation_role": "",
                "paper_section": "",
                "evidence_basis": "full_text",
                "evidence_locator": "papers/evaluations/iclr/2026_li_a2asecbench.md; published ICLR proceedings and OpenReview source review",
                "source_files": "papers/evaluations/iclr/2026_li_a2asecbench.md",
                "decision_reason": "2026-08-18 benchmark reconciliation: canonical ICLR source note establishes direct A2A protocol security evaluation; the work had been omitted from generated sets.",
                "previous_decision": "omitted_from_generated_ledger",
                "previous_category": "evaluation",
                "reviewer": REVIEWER,
                "reviewed_at": DATE,
                "author_signoff_required": "yes",
                "taxonomy_ready": "yes",
                "membership_reason": "Passed MAS-security scope and published at ICLR 2026; added as a frozen corpus correction.",
            })
            ledger.append(row)
            remember(row, action="benchmark_add_set1", reason=decision["reason_code"], confidence=decision.get("confidence", ""))
            continue

        if action == "alias_merge_upgrade":
            # Canonicalize the pre-cutoff arXiv identity to the published USENIX paper.
            candidates = [row for row in ledger if row.get("arxiv_id") == "2505.12442" or norm_title(row.get("title", "")) == norm_title("IP Leakage Attacks Targeting LLM-Based Multi-Agent Systems")]
            if not candidates:
                # Fallback if the frozen row has already adopted the canonical title.
                candidates = [row for row in ledger if row.get("work_key") == "wang2026masleak" or norm_title(row.get("title", "")) == norm_title(decision["title"])]
            if len(candidates) != 1:
                raise SystemExit(f"MASLeak identity resolution expected exactly one row, got {len(candidates)}")
            row = candidates[0]
            old_key = row.get("work_key", "")
            row.update({
                "work_key": "wang2026masleak",
                "canonical_paper_id": "wang2026masleak",
                "title": "MASLeak: Investigating and Exposing Intellectual Property Leakage Vulnerabilities in Multi-Agent Systems",
                "year": "2026",
                "venue": "USENIX Security 2026",
                "arxiv_id": "2505.12442",
                "primary_url": "https://www.usenix.org/conference/usenixsecurity26/presentation/wang-liwen",
                "evidence_set": "set1_core",
                "strict_scope_pass": "yes",
                "scope_reason": "USENIX source review establishes a black-box multi-agent IP leakage attack whose disclosures propagate through internal cross-agent communication.",
                "peer_reviewed": "yes",
                "peer_review_basis": "published USENIX Security 2026 paper",
                "maturity_rule_pass": "yes",
                "dominant_contribution": "attack",
                "citation_role": "",
                "paper_section": "",
                "decision_reason": "2026-08-18 identity correction: the arXiv work is the earlier version of the published MASLeak paper; canonicalized and upgraded under the Set 1 maturity rule.",
                "reviewer": REVIEWER,
                "reviewed_at": DATE,
                "author_signoff_required": "yes",
            })
            if old_key and old_key in before_by_key:
                before_by_key["wang2026masleak"] = before_by_key[old_key]
            remember(row, action="identity_merge_and_maturity_upgrade", reason=decision["reason_code"], confidence=decision.get("confidence", ""))
            continue

        row = find_row(work_key=decision.get("canonical_work_key", ""), title=decision.get("title", ""))

        if action == "move_set3":
            # Two of these are already moved by the evaluation-primary audit.  Deliberation
            # and Drift is an additional benchmark-reconciliation removal and must be counted once.
            if norm_title(row.get("title", "")) in moved_titles:
                continue
            if row.get("evidence_set") not in {"set1_core", "set2_emerging"}:
                # If it is already context in the frozen view, there is nothing more to apply.
                continue
            move_to_context(
                row,
                "measurement_context",
                decision["reason_code"],
                decision.get("confidence", ""),
                "benchmark_scope_move",
            )
            continue

        if action == "relabel":
            old = row.get("dominant_contribution", "")
            row["dominant_contribution"] = decision["recommended_contribution"]
            if row.get("evidence_set") == "set2_emerging":
                row["emerging_direction"] = row["dominant_contribution"]
            row["decision_reason"] = f"2026-08-18 benchmark reconciliation contribution correction: {decision['reason_code']}."
            row["reviewer"] = REVIEWER
            row["reviewed_at"] = DATE
            row["author_signoff_required"] = "yes"
            remember(row, action=f"contribution_relabel_{old}_to_{row['dominant_contribution']}", reason=decision["reason_code"], confidence=decision.get("confidence", ""))
            continue

        if action in {"promote_set1", "promote_set2"}:
            target = decision["recommended_membership"]
            row["strict_scope_pass"] = "yes"
            row["evidence_set"] = target
            row["citation_role"] = ""
            row["paper_section"] = ""
            row["dominant_contribution"] = decision["recommended_contribution"]
            row["scope_reason"] = f"2026-08-18 source-level reconciliation established a material inter-agent security path: {decision['reason_code']}."
            row["decision_reason"] = f"2026-08-18 benchmark reconciliation promoted this work into {target}: {decision['reason_code']}."
            row["reviewer"] = REVIEWER
            row["reviewed_at"] = DATE
            row["author_signoff_required"] = "yes"
            if target == "set1_core":
                row["peer_reviewed"] = "yes"
                if not (row.get("peer_review_basis") or "").strip() or row.get("peer_reviewed") != "yes":
                    row["peer_review_basis"] = "published archival venue/source review"
                row["maturity_rule_pass"] = "yes"
                row["emerging_direction"] = ""
            else:
                peer, basis = force_emerging_peer.get(decision.get("canonical_work_key", ""), (row.get("peer_reviewed", "no") or "no", row.get("peer_review_basis", "") or "emerging source"))
                row["peer_reviewed"] = peer
                row["peer_review_basis"] = basis
                # Keep the frozen citation count; these decisions are Set 2 only if they do not meet maturity.
                try:
                    cites = int(float((row.get("frozen_citation_count") or "0").replace(",", "")))
                except ValueError:
                    cites = 0
                if peer == "yes" or cites >= 10:
                    raise SystemExit(f"benchmark row recommended Set 2 but meets Set 1 maturity: {row['title']}")
                row["maturity_rule_pass"] = "no"
                row["emerging_direction"] = row["dominant_contribution"]
            remember(row, action=action, reason=decision["reason_code"], confidence=decision.get("confidence", ""))
            continue

        raise SystemExit(f"unhandled benchmark action: {action}")

    # Ensure canonical work keys remain unique after version correction and A2A insertion.
    keys = [row.get("work_key", "") for row in ledger]
    duplicate_keys = sorted(key for key, n in Counter(keys).items() if key and n > 1)
    if duplicate_keys:
        raise SystemExit(f"duplicate work keys after reconciliation: {duplicate_keys[:10]}")
    if len(ledger) != 2217:
        raise SystemExit(f"expected 2217 rows after adding the missing A2ASecBench work, got {len(ledger)}")

    write_csv(ledger_path, sorted(ledger, key=lambda row: row.get("work_key", "")), fields)

    # Record the MASLeak version alias explicitly.
    alias_path = CORPUS / "identifier_alias_overrides.csv"
    aliases = read_csv(alias_path)
    alias_fields = list(aliases[0].keys())
    if not any(row.get("alias_type") == "arxiv" and row.get("alias_value") == "2505.12442" for row in aliases):
        aliases.append({
            "alias_type": "arxiv",
            "alias_value": "2505.12442",
            "canonical_doi": "",
            "canonical_arxiv_id": "2505.12442",
            "canonical_title": "MASLeak: Investigating and Exposing Intellectual Property Leakage Vulnerabilities in Multi-Agent Systems",
            "authoritative_url": "https://www.usenix.org/conference/usenixsecurity26/presentation/wang-liwen",
            "note": "The arXiv title IP Leakage Attacks Targeting LLM-Based Multi-Agent Systems is the earlier version of the published USENIX Security 2026 MASLeak paper.",
        })
        write_csv(alias_path, aliases, alias_fields)

    # Deterministically regenerate the four authoritative sets, summary, manifest basics,
    # corpus README, and author-priority queue from the corrected ledger.
    subprocess.run(["python3", str(ROOT / "scripts" / "rebuild_membership_from_ledger.py")], check=True)

    sets = {
        "set1_core": read_csv(CORPUS / "set1_core.csv"),
        "set2_emerging": read_csv(CORPUS / "set2_emerging.csv"),
        "set3_context": read_csv(CORPUS / "set3_context.csv"),
        "screened_out": read_csv(CORPUS / "screened_out.csv"),
    }
    actual = {name: len(rows) for name, rows in sets.items()}
    if actual != EXPECTED_FINAL:
        raise SystemExit(f"unexpected integrated partition: {actual} != {EXPECTED_FINAL}")

    set1_contrib = dict(Counter(row.get("dominant_contribution", "") for row in sets["set1_core"]))
    set2_contrib = dict(Counter(row.get("dominant_contribution", "") for row in sets["set2_emerging"]))
    if set1_contrib != EXPECTED_SET1_CONTRIB:
        raise SystemExit(f"unexpected Set 1 contribution distribution: {set1_contrib}")
    if set2_contrib != EXPECTED_SET2_CONTRIB:
        raise SystemExit(f"unexpected Set 2 contribution distribution: {set2_contrib}")

    # Build a 226-row manual signoff queue over the complete active corpus.
    manual_fields = [
        "work_key", "title", "evidence_set", "dominant_contribution", "year", "venue",
        "peer_reviewed", "frozen_citation_count", "interaction_interfaces", "risk_or_property",
        "interaction_dependence", "scope_reason", "decision_reason", "evidence_basis",
        "evidence_locator", "author_signoff_required", "human_scope_decision",
        "human_contribution_decision", "human_notes",
    ]
    manual_rows: list[dict[str, str]] = []
    for row in sets["set1_core"] + sets["set2_emerging"]:
        manual_rows.append({
            **row,
            "human_scope_decision": "",
            "human_contribution_decision": "",
            "human_notes": "",
        })
    manual_rows.sort(key=lambda row: (0 if row["evidence_set"] == "set1_core" else 1, row.get("dominant_contribution", ""), row.get("title", "").lower()))
    write_csv(CORPUS / "manual_review_queue_2026-08-18.csv", manual_rows, manual_fields)
    if len(manual_rows) != 226:
        raise SystemExit(f"manual review queue must contain all 226 active works, got {len(manual_rows)}")

    # Build a smaller queue containing only rows changed by these two adjudications.
    changed_fields = [
        "change_type", "work_key", "title", "previous_membership", "proposed_membership",
        "previous_contribution", "proposed_contribution", "reason_code", "confidence",
        "human_decision", "human_notes",
    ]
    changed_rows = sorted(changed.values(), key=lambda row: (row["change_type"], row["title"].lower()))
    write_csv(ADJ / "manual_signoff_changes_2026-08-18.csv", changed_rows, changed_fields)

    # Patch the frozen manifest with this explicit revision and include adjudication files.
    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["search_universe"] = 2217
    manifest["counts"] = actual
    manifest["corpus_counts"] = {
        "set1_core": actual["set1_core"],
        "set2_emerging": actual["set2_emerging"],
        "total_corpus": actual["set1_core"] + actual["set2_emerging"],
    }
    manifest["set1_contributions"] = EXPECTED_SET1_CONTRIB
    manifest["set2_contributions"] = EXPECTED_SET2_CONTRIB
    manifest["evaluation_adjudication_revision"] = {
        "date": DATE,
        "reviewed": 44,
        "retained_in_corpus": 27,
        "moved_to_set3": 17,
        "ledger": "adjudication/evaluation_scope_2026-08-18.csv",
    }
    manifest["benchmark_reconciliation_revision"] = {
        "date": DATE,
        "reviewed_report_papers": 44,
        "new_or_promoted_into_active_corpus": 12,
        "additional_unique_move_to_set3_beyond_evaluation_audit": 1,
        "contribution_relabels": 2,
        "identity_merge_and_maturity_upgrade": 1,
        "post_cutoff": 1,
        "final_active_corpus": 226,
        "ledger": "adjudication/benchmark_reconciliation_2026-08-18.csv",
    }
    manifest["manual_review_queue"] = {
        "path": "manual_review_queue_2026-08-18.csv",
        "rows": 226,
        "status": "pending_named_author_signoff",
    }
    manifest["verification_note"] = "Model-assisted source review. The 226-work active corpus is queued for named-author manual signoff; do not claim human verification before signoff."

    # Refresh file hashes for root corpus CSVs and adjudication ledgers.
    manifest["files"] = {}
    for path in sorted(CORPUS.glob("*.csv")):
        manifest["files"][path.name] = {"sha256": sha256(path), "rows": len(read_csv(path))}
    for path in sorted(ADJ.glob("*.csv")):
        key = f"adjudication/{path.name}"
        manifest["files"][key] = {"sha256": sha256(path), "rows": len(read_csv(path))}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Update root manuscript-facing documentation.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme = readme.replace("**Set 1 = 104**, **Set 2 = 128**, **Set 3 = 441**, and **screened out = 1,543**. Set 1 and Set 2 together form the **232-work MAS-security corpus**.", "**Set 1 = 105**, **Set 2 = 121**, **Set 3 = 448**, and **screened out = 1,543**. Set 1 and Set 2 together form the **226-work MAS-security corpus**.")
    readme = readme.replace("The frozen ledger contains 2,216 deduplicated works", "The frozen ledger contains 2,217 deduplicated works")
    readme = readme.replace("| `corpus/set1_core.csv` | 104 |", "| `corpus/set1_core.csv` | 105 |")
    readme = readme.replace("| `corpus/set2_emerging.csv` | 128 |", "| `corpus/set2_emerging.csv` | 121 |")
    readme = readme.replace("| `corpus/set3_context.csv` | 441 |", "| `corpus/set3_context.csv` | 448 |")
    readme = readme.replace("together form the 232-work MAS-security corpus", "together form the 226-work MAS-security corpus")
    readme = readme.replace("The validator checks that the four sets partition all 2,216 works", "The validator checks that the four sets partition all 2,217 works")
    readme += "\nThe 2026-08-18 evaluation and benchmark reconciliation reviewed all 44 evaluation-primary rows and the 44-paper benchmark analysis set. The integrated correction moves 18 unique active works to context, adds or promotes 12 previously missing/contextual works into the active corpus, canonicalizes MASLeak, and freezes a 226-work corpus. See `corpus/manual_review_queue_2026-08-18.csv` for named-author signoff.\n"
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    snapshot = (ROOT / "FROZEN_SNAPSHOT.md").read_text(encoding="utf-8")
    snapshot = snapshot.replace("| Set 1 | 104 |", "| Set 1 | 105 |")
    snapshot = snapshot.replace("| Set 2 | 128 |", "| Set 2 | 121 |")
    snapshot = snapshot.replace("| Set 3 | 441 |", "| Set 3 | 448 |")
    snapshot = snapshot.replace("| Review universe | 2,216 |", "| Review universe | 2,217 |")
    snapshot = snapshot.replace("Set 1 plus Set 2 is the 232-work MAS-security corpus.", "Set 1 plus Set 2 is the 226-work MAS-security corpus.")
    snapshot = snapshot.replace("The deduplicated review universe is therefore 2,216 works and the MAS-security corpus is 232 works.", "That survey revision produced a 2,216-work review universe and 232-work MAS-security corpus before the evaluation/benchmark reconciliation below.")
    snapshot += """

## 2026-08-18 evaluation and benchmark reconciliation revision

All 44 evaluation-primary works were individually rechecked under the same substantive MAS-security scope rule. Twenty-seven remain active and seventeen move to Set 3. A separate reconciliation of the 44-paper benchmark analysis set then identified twelve active-corpus omissions/promotions, one additional unique active-to-context move (`Deliberation and drift`) not present in the evaluation-primary ledger, two dominant-contribution corrections, the MASLeak arXiv/USENIX identity merge and maturity upgrade, and one post-cutoff benchmark. A2ASecBench was present as a canonical source note but missing from the generated review ledger and is added as an explicit corpus correction.

The resulting frozen partition is Set 1 = 105, Set 2 = 121, Set 3 = 448, screened out = 1,543, for a 2,217-work review universe and a 226-work MAS-security corpus. The complete active corpus is exported to `corpus/manual_review_queue_2026-08-18.csv` for named-author signoff. Until those fields are completed, the corpus remains model-assisted rather than human verified.
"""
    (ROOT / "FROZEN_SNAPSHOT.md").write_text(snapshot, encoding="utf-8")

    # Freeze the validator to the integrated counts and adjudication invariants.
    validator = f'''#!/usr/bin/env python3
from __future__ import annotations
import csv, json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
FILES = {{"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}}
FROZEN_COUNTS = {EXPECTED_FINAL!r}
FROZEN_SET1_CONTRIBUTIONS = {EXPECTED_SET1_CONTRIB!r}
FROZEN_SET2_CONTRIBUTIONS = {EXPECTED_SET2_CONTRIB!r}

def rows(name):
    with (C/name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))
def citations(row):
    try: return int(float((row.get("frozen_citation_count") or "0").replace(",", "")))
    except ValueError: return 0
sets = {{name: rows(filename) for name, filename in FILES.items()}}
actual = {{name: len(data) for name, data in sets.items()}}
if actual != FROZEN_COUNTS: raise SystemExit(f"frozen corpus partition changed: {{actual}} != {{FROZEN_COUNTS}}")
keys = {{name: {{row["work_key"] for row in data}} for name, data in sets.items()}}
for left in keys:
    for right in keys:
        if left < right and keys[left] & keys[right]: raise SystemExit(f"sets overlap: {{left}} and {{right}}")
ledger = rows("review_ledger.csv")
if len(ledger) != 2217: raise SystemExit(f"review ledger changed size: {{len(ledger)}}")
if set().union(*keys.values()) != {{row["work_key"] for row in ledger}}: raise SystemExit("sets do not partition review_ledger.csv")
for row in sets["set1_core"]:
    mature = row.get("peer_reviewed") == "yes" or citations(row) >= 10
    if row.get("strict_scope_pass") != "yes" or not mature or row.get("maturity_rule_pass") != "yes": raise SystemExit(f"Set 1 contains an ineligible row: {{row.get('work_key')}}")
for row in sets["set2_emerging"]:
    mature = row.get("peer_reviewed") == "yes" or citations(row) >= 10
    if row.get("strict_scope_pass") != "yes" or mature or row.get("maturity_rule_pass") != "no": raise SystemExit(f"Set 2 violates scope or maturity: {{row.get('work_key')}}")
for row in sets["set3_context"]:
    if row.get("strict_scope_pass") == "yes" or not row.get("citation_role"): raise SystemExit(f"invalid Set 3 row: {{row.get('work_key')}}")
for row in sets["screened_out"]:
    if row.get("strict_scope_pass") == "yes": raise SystemExit(f"screened_out contains in-scope work: {{row.get('work_key')}}")
set1 = dict(Counter(row.get("dominant_contribution", "") for row in sets["set1_core"]))
set2 = dict(Counter(row.get("dominant_contribution", "") for row in sets["set2_emerging"]))
if set1 != FROZEN_SET1_CONTRIBUTIONS: raise SystemExit(f"Set 1 contributions changed: {{set1}}")
if set2 != FROZEN_SET2_CONTRIBUTIONS: raise SystemExit(f"Set 2 contributions changed: {{set2}}")
if len(rows("adjudication/evaluation_scope_2026-08-18.csv")) != 44: raise SystemExit("evaluation adjudication ledger incomplete")
if len(rows("adjudication/benchmark_reconciliation_2026-08-18.csv")) != 44: raise SystemExit("benchmark reconciliation ledger incomplete")
if len(rows("manual_review_queue_2026-08-18.csv")) != 226: raise SystemExit("manual review queue must cover all active works")
manifest = json.loads((C/"manifest.json").read_text(encoding="utf-8"))
if manifest.get("counts") != actual: raise SystemExit("manifest counts do not match")
if manifest.get("search_universe") != 2217: raise SystemExit("manifest review universe must be 2217")
if manifest.get("corpus_counts", {{}}).get("total_corpus") != 226: raise SystemExit("manifest corpus total must be frozen at 226")
if manifest.get("set1_contributions") != FROZEN_SET1_CONTRIBUTIONS: raise SystemExit("manifest Set 1 contributions mismatch")
if manifest.get("set2_contributions") != FROZEN_SET2_CONTRIBUTIONS: raise SystemExit("manifest Set 2 contributions mismatch")
if (manifest.get("evaluation_adjudication_revision") or {{}}).get("moved_to_set3") != 17: raise SystemExit("manifest evaluation revision missing")
if (manifest.get("benchmark_reconciliation_revision") or {{}}).get("new_or_promoted_into_active_corpus") != 12: raise SystemExit("manifest benchmark revision missing")
print("Frozen three-set corpus valid: Set 1=105, Set 2=121, Set 3=448, screened out=1543; MAS-security corpus=226; manual review pending")
'''
    (ROOT / "scripts" / "validate_three_set_corpus.py").write_text(validator, encoding="utf-8")

    print(json.dumps({
        "counts": actual,
        "corpus_total": 226,
        "review_universe": 2217,
        "set1_contributions": set1_contrib,
        "set2_contributions": set2_contrib,
        "changed_rows_for_signoff": len(changed_rows),
        "manual_review_queue": len(manual_rows),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
