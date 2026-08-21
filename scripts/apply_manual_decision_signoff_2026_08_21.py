#!/usr/bin/env python3
"""Apply the named 2026-08-21 signoff for the 32 changed decisions."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
ADJUDICATION = CORPUS / "adjudication"
TRANSACTION = ROOT / ".review-state" / "manual_decision_signoff_2026-08-21"
DATE = "2026-08-21"
REVIEWER = "expiol"

ALGORITHMIC = "doi:10.5281/zenodo.18902320"
CASCADE = "doi:10.5281/zenodo.21314249"
REJECT_NOTES = {
    ALGORITHMIC: (
        "Reject move to Set 3. Full text v1.0.0, Sections 2.4, 3.1, and 6.3 "
        "define an adversarial Influencer whose messages are passed directly to the "
        "Target. Retain set2_emerging/evaluation; evaluation remains the dominant "
        "contribution."
    ),
    CASCADE: (
        "Reject both previous and proposed placement. DataCite records the DOI as "
        "created and registered on 2026-07-11, after the 2026-07-01 00:00 UTC "
        "cutoff. Zenodo reports deletion on 2026-07-22 for copyright. Route to "
        "post-cutoff provenance and exclude from the frozen Set 1/2/3 denominator; "
        "canonical full text is unavailable."
    ),
}

SET_FILES = {
    "set1_core": CORPUS / "set1_core.csv",
    "set2_emerging": CORPUS / "set2_emerging.csv",
    "set3_context": CORPUS / "set3_context.csv",
    "screened_out": CORPUS / "screened_out.csv",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or ()), [dict(row) for row in reader]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
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


def append_sentence(value: str, sentence: str) -> str:
    value = value.strip()
    if sentence in value:
        return value
    return f"{value} {sentence}".strip()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text missing from {path}: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def sign_row(row: dict[str, str]) -> None:
    source_reviewer = row.get("reviewer", "").strip()
    signoff = f"{REVIEWER}, named decision signoff"
    if signoff not in source_reviewer:
        row["reviewer"] = f"{source_reviewer}; {signoff}".strip("; ")
    row["reviewed_at"] = DATE
    row["author_signoff_required"] = "no"
    row["decision_reason"] = append_sentence(
        row.get("decision_reason", ""),
        f"{DATE} named decision signoff by {REVIEWER} confirmed membership and dominant contribution.",
    )


def update_algorithmic(row: dict[str, str]) -> None:
    row.update({
        "publication_date": "2026-03-07",
        "venue": "Zenodo",
        "primary_url": "https://zenodo.org/records/18902321",
        "evidence_set": "set2_emerging",
        "strict_scope_pass": "yes",
        "scope_reason": (
            f"{DATE} named decision signoff retained the work after full-text review: "
            "the adversarial Influencer directly pressures the Target and the interaction "
            "is the tested safety path."
        ),
        "peer_reviewed": "no",
        "peer_review_basis": "Zenodo preprint metadata",
        "maturity_rule_pass": "no",
        "dominant_contribution": "evaluation",
        "interaction_interfaces": "I2_communication_routing;I5_aggregation_outcome",
        "risk_or_property": "R3_collective_integrity;R6_authority_misuse",
        "interaction_dependence": "interaction_dependent_mechanism",
        "emerging_direction": "evaluation",
        "citation_role": "",
        "paper_section": "Sections 2.4;3.1;6.3;7",
        "evidence_basis": "full_text",
        "evidence_locator": (
            "Zenodo v1.0.0 DOI 10.5281/zenodo.18902321, Sections 2.4, 3.1, "
            "6.3, and 7"
        ),
        "decision_reason": (
            f"{DATE} named decision signoff rejected the proposed Set 3 move and "
            "retained set2_emerging/evaluation. The work directly evaluates adversarial "
            "peer-agent pressure against target safety behavior."
        ),
        "taxonomy_ready": "no",
        "membership_reason": (
            "Passed MAS-security scope. Maturity: peer_reviewed=no; frozen_citations=0. "
            "Does not yet meet the Set 1 maturity rule."
        ),
    })
    source_file = "corpus/adjudication/manual_decision_signoff_2026-08-21.csv"
    sources = [value.strip() for value in row.get("source_files", "").split(";") if value.strip()]
    if source_file not in sources:
        sources.append(source_file)
    row["source_files"] = "; ".join(sources)
    sign_row(row)


def update_documents() -> None:
    replace_once(
        ROOT / "README.md",
        "frozen as of `2026-08-18`. The authoritative counts are **Set 1 = 105**, **Set 2 = 122**, **Set 3 = 447**, and **screened out = 1,541**. Set 1 and Set 2 together form the **227-work MAS-security corpus**.",
        "frozen on `2026-08-18` and corrected by named decision signoff on `2026-08-21`. The authoritative counts are **Set 1 = 105**, **Set 2 = 123**, **Set 3 = 445**, and **screened out = 1,541**. Set 1 and Set 2 together form the **228-work MAS-security corpus**.",
    )
    replace_once(ROOT / "README.md", "| `corpus/set2_emerging.csv` | 122 |", "| `corpus/set2_emerging.csv` | 123 |")
    replace_once(ROOT / "README.md", "| `corpus/set3_context.csv` | 447 |", "| `corpus/set3_context.csv` | 445 |")
    replace_once(ROOT / "README.md", "together form the 227-work MAS-security corpus", "together form the 228-work MAS-security corpus")
    replace_once(ROOT / "README.md", "partition all 2,215 works", "partition all 2,214 frozen-review works")
    replace_once(
        ROOT / "README.md",
        "`corpus/manual_review_queue_2026-08-18.csv` contains all 227 active works for named-author signoff.",
        "`corpus/manual_review_queue_2026-08-18.csv` contains all 228 active works for source/evidence review. The 32 changed membership/contribution decisions received named signoff on 2026-08-21.",
    )
    replace_once(ROOT / "README.md", "complete 227-work corpus second", "complete 228-work corpus second")
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    marker = "## 2026-08-21 named decision-signoff correction"
    if marker not in text:
        text += (
            "\n\n## 2026-08-21 named decision-signoff correction\n\n"
            "Reviewer `expiol` confirmed all 32 changed membership/contribution decisions: "
            "30 proposed decisions were approved, `Algorithmic Cowardice` was retained in "
            "Set 2, and `Containing the Cascade` was removed as post-cutoff. This is a "
            "decision signoff only; it does not mark the complete 228-work source/evidence "
            "queue as fully reviewed.\n"
        )
        readme.write_text(text, encoding="utf-8")

    replace_once(CORPUS / "README.md", "| `set2_emerging.csv` | 122 |", "| `set2_emerging.csv` | 123 |")
    replace_once(CORPUS / "README.md", "| `set3_context.csv` | 447 |", "| `set3_context.csv` | 445 |")
    replace_once(
        CORPUS / "README.md",
        "All classifications remain model-assisted source review records and require\nnamed-author signoff before being described as human verified.",
        "The 32 changed membership/contribution decisions received named signoff from `expiol` on 2026-08-21. Source/evidence verification remains separate, and records must not be described as fully reviewed until that review is completed.",
    )

    snapshot = ROOT / "FROZEN_SNAPSHOT.md"
    replace_once(snapshot, "| Set 2 | 122 |", "| Set 2 | 123 |")
    replace_once(snapshot, "| Set 3 | 447 |", "| Set 3 | 445 |")
    replace_once(snapshot, "| Review universe | 2,215 |", "| Frozen review universe | 2,214 |")
    replace_once(snapshot, "Set 1 plus Set 2 is the 227-work MAS-security corpus.", "Set 1 plus Set 2 is the 228-work MAS-security corpus.")
    text = snapshot.read_text(encoding="utf-8")
    marker = "## 2026-08-21 named decision-signoff correction"
    if marker not in text:
        text += (
            "\n\n## 2026-08-21 named decision-signoff correction\n\n"
            "Named reviewer `expiol` confirmed the 32-row changed-decision ledger. Thirty "
            "proposals were approved. `Algorithmic Cowardice` was restored from Set 3 to "
            "Set 2 after full-text scope review, while `Containing the Cascade` was removed "
            "from the frozen partition because its DOI was first registered after the cutoff. "
            "The corrected partition is **Set 1 = 105, Set 2 = 123, Set 3 = 445, screened "
            "out = 1,541**, for a **2,214-work frozen review universe** and a **228-work "
            "MAS-security corpus**. This confirms membership and dominant contribution only; "
            "the complete source/evidence queue remains pending.\n"
        )
        snapshot.write_text(text, encoding="utf-8")

    replace_once(ROOT / "review_app/static/index.html", "0 / 227", "0 / 228")
    replace_once(ROOT / "scripts/rebuild_membership_from_ledger.py", "len(ledger) != 2215", "len(ledger) != 2214")


def write_validator() -> None:
    path = ROOT / "scripts/validate_three_set_corpus.py"
    path.write_text(
        """#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}
EXPECTED={'set1_core':105,'set2_emerging':123,'set3_context':445,'screened_out':1541}
E1={'attack':33,'defense':39,'evaluation':21,'general':7,'survey':5}
E2={'attack':38,'defense':61,'evaluation':17,'general':4,'survey':3}
def rows(p):
    with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={k:rows(v) for k,v in FILES.items()}; actual={k:len(v) for k,v in S.items()}
if actual!=EXPECTED: raise SystemExit(f"corrected counts changed: {actual} != {EXPECTED}")
K={k:{r["work_key"] for r in v} for k,v in S.items()}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {a} {b}")
L=rows("review_ledger.csv")
if len(L)!=2214 or set().union(*K.values())!={r["work_key"] for r in L}: raise SystemExit("ledger partition mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
if len(rows("manual_review_queue_2026-08-18.csv"))!=228: raise SystemExit("manual queue incomplete")
signoff=rows("adjudication/manual_signoff_changes_2026-08-18.csv")
if len(signoff)!=32 or Counter(r["human_decision"] for r in signoff)!={"approve":30,"reject":2}: raise SystemExit("decision signoff mismatch")
post=rows("sets/01_search_catalog/post_cutoff_papers.csv")
if not any(r["paper_id"]=="zenodo21314249_containing_cascade" for r in post): raise SystemExit("post-cutoff record missing")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=228 or m["search_universe"]!=2214: raise SystemExit("manifest mismatch")
print(f"Corrected corpus valid: Set1=105 Set2=123 Set3={actual['set3_context']} screened={actual['screened_out']} active=228 universe=2214 signoff=30/2")
""",
        encoding="utf-8",
    )
    path.chmod(0o755)


def main() -> int:
    signoff_path = ADJUDICATION / "manual_signoff_changes_2026-08-18.csv"
    fields, decisions = read_csv(signoff_path)
    if len(decisions) != 32 or len({row["work_key"] for row in decisions}) != 32:
        raise SystemExit("changed-decision ledger must contain 32 unique rows")
    for row in decisions:
        key = row["work_key"]
        row["human_decision"] = "reject" if key in REJECT_NOTES else "approve"
        row["human_notes"] = REJECT_NOTES.get(key, "")
    write_csv(signoff_path, fields, decisions)
    write_csv(TRANSACTION / "MODIFIED_FILE.csv", fields, decisions)

    sets: dict[str, list[dict[str, str]]] = {}
    set_fields: list[str] = []
    for name, path in SET_FILES.items():
        current_fields, rows = read_csv(path)
        if not set_fields:
            set_fields = current_fields
        elif current_fields != set_fields:
            raise SystemExit(f"set header mismatch: {path}")
        sets[name] = rows

    locations: dict[str, tuple[str, dict[str, str]]] = {}
    for name, rows in sets.items():
        for row in rows:
            key = row["work_key"]
            if key in locations:
                raise SystemExit(f"duplicate set row: {key}")
            locations[key] = (name, row)

    decision_keys = {row["work_key"] for row in decisions}
    if not decision_keys <= locations.keys():
        raise SystemExit(f"decision rows absent from sets: {sorted(decision_keys-locations.keys())}")

    algorithmic_name, algorithmic = locations[ALGORITHMIC]
    sets[algorithmic_name].remove(algorithmic)
    update_algorithmic(algorithmic)
    sets["set2_emerging"].append(algorithmic)

    cascade_name, cascade = locations[CASCADE]
    sets[cascade_name].remove(cascade)

    for decision in decisions:
        key = decision["work_key"]
        if key in {ALGORITHMIC, CASCADE}:
            continue
        _, row = locations[key]
        sign_row(row)

    for name, rows in sets.items():
        write_csv(SET_FILES[name], set_fields, rows)

    ledger_fields, ledger = read_csv(CORPUS / "review_ledger.csv")
    ledger_by_key = {row["work_key"]: row for row in ledger}
    ledger_by_key.pop(CASCADE)
    for name, rows in sets.items():
        for row in rows:
            if row["work_key"] in decision_keys:
                ledger_by_key[row["work_key"]] = dict(row)
    write_csv(CORPUS / "review_ledger.csv", ledger_fields, sorted(ledger_by_key.values(), key=lambda row: row["work_key"]))

    priority_fields, priority = read_csv(CORPUS / "author_priority_review.csv")
    signed_rows = {row["work_key"]: row for name in sets for row in sets[name] if row["work_key"] in decision_keys}
    for index, row in enumerate(priority):
        if row["work_key"] in signed_rows:
            review_issues = row.get("review_issues", "")
            priority[index] = {**signed_rows[row["work_key"]], "review_issues": review_issues}
    write_csv(CORPUS / "author_priority_review.csv", priority_fields, priority)

    queue_fields, old_queue = read_csv(CORPUS / "manual_review_queue_2026-08-18.csv")
    human = {
        row["work_key"]: {
            "human_scope_decision": row["human_scope_decision"],
            "human_contribution_decision": row["human_contribution_decision"],
            "human_notes": row["human_notes"],
        }
        for row in old_queue
    }
    queue_rows: list[dict[str, str]] = []
    queue_source_fields = [field for field in queue_fields if not field.startswith("human_")]
    for name in ("set1_core", "set2_emerging"):
        for row in sets[name]:
            queued = {field: row.get(field, "") for field in queue_source_fields}
            queued.update(human.get(row["work_key"], {
                "human_scope_decision": "",
                "human_contribution_decision": "",
                "human_notes": "",
            }))
            queue_rows.append(queued)
    write_csv(CORPUS / "manual_review_queue_2026-08-18.csv", queue_fields, queue_rows)

    route_fields, routes = read_csv(CORPUS / "routes.csv")
    for row in routes:
        if row["work_key"] in decision_keys:
            row["human_signoff_required"] = "no"
        if row["work_key"] == CASCADE:
            row["source_decision"] = "exclude-after-cutoff"
            row["source_scope"] = "post_cutoff"
            row["source_status"] = "post_cutoff"
            row["source_reason"] = "DOI first registered 2026-07-11, after the frozen cutoff."
            row["ledger_decision"] = "post_cutoff"
            row["ledger_decision_source"] = "manual-decision-signoff:2026-08-21"
    write_csv(CORPUS / "routes.csv", route_fields, routes)

    post_fields = [
        "paper_id", "title", "authors", "source_date", "primary_url",
        "publication_status", "scope_status", "note_path", "last_checked", "cutoff_reason",
    ]
    post_rows = [{
        "paper_id": "zenodo21314249_containing_cascade",
        "title": cascade["title"],
        "authors": "Not reported",
        "source_date": "2026-07-11",
        "primary_url": "https://doi.org/10.5281/zenodo.21314249",
        "publication_status": "Zenodo record deleted 2026-07-22 for copyright",
        "scope_status": "post_cutoff_not_assessed",
        "note_path": "",
        "last_checked": DATE,
        "cutoff_reason": "DOI created and registered after 2026-07-01 00:00 UTC cutoff",
    }]
    write_csv(CORPUS / "sets/01_search_catalog/post_cutoff_papers.csv", post_fields, post_rows)

    audit_fields = [
        "work_key", "title", "human_decision", "adjudicated_membership",
        "adjudicated_contribution", "reviewer", "reviewed_at", "decision_scope",
        "source_evidence_verified", "human_notes", "adjudication_note",
    ]
    audit_rows = []
    for row in decisions:
        key = row["work_key"]
        membership = row["proposed_membership"]
        contribution = row["proposed_contribution"]
        if key == ALGORITHMIC:
            membership = "set2_emerging"
        elif key == CASCADE:
            membership = "post_cutoff"
        note = row["human_notes"]
        audit_rows.append({
            "work_key": key,
            "title": row["title"],
            "human_decision": row["human_decision"],
            "adjudicated_membership": membership,
            "adjudicated_contribution": contribution,
            "reviewer": REVIEWER,
            "reviewed_at": DATE,
            "decision_scope": "membership_and_dominant_contribution_only",
            "source_evidence_verified": "no",
            "human_notes": note,
            "adjudication_note": note or "Approved the proposed membership and dominant contribution.",
        })
    audit_path = ADJUDICATION / "manual_decision_signoff_2026-08-21.csv"
    write_csv(audit_path, audit_fields, audit_rows)

    counts = {name: len(rows) for name, rows in sets.items()}
    summary_rows = [
        {"metric": "evidence_set", "label": name, "count": str(counts[name])}
        for name in ("set1_core", "set2_emerging", "set3_context", "screened_out")
    ]
    for name in ("set1_core", "set2_emerging"):
        for label, count in sorted(Counter(row["dominant_contribution"] for row in sets[name]).items()):
            summary_rows.append({"metric": f"{name}_contribution", "label": label, "count": str(count)})
    for label, count in sorted(Counter(row["citation_role"] for row in sets["set3_context"]).items()):
        summary_rows.append({"metric": "set3_citation_role", "label": label, "count": str(count)})
    summary_rows.extend([
        {"metric": "quality_control", "label": "taxonomy_ready_set1", "count": str(sum(row["taxonomy_ready"] == "yes" for row in sets["set1_core"]))},
        {"metric": "quality_control", "label": "author_priority_review", "count": str(len(priority))},
        {"metric": "decision_signoff", "label": "approve", "count": "30"},
        {"metric": "decision_signoff", "label": "reject", "count": "2"},
    ])
    write_csv(CORPUS / "summary.csv", ["metric", "label", "count"], summary_rows)

    update_documents()
    write_validator()

    manifest_path = CORPUS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["counts"] = counts
    manifest["corpus_counts"] = {"set1_core": 105, "set2_emerging": 123, "total_corpus": 228}
    manifest["search_universe"] = 2214
    manifest["set1_contributions"] = dict(Counter(row["dominant_contribution"] for row in sets["set1_core"]))
    manifest["set2_contributions"] = dict(Counter(row["dominant_contribution"] for row in sets["set2_emerging"]))
    manifest["set3_roles"] = dict(Counter(row["citation_role"] for row in sets["set3_context"]))
    manifest["reviewer"] = "OpenAI GPT-5.6 Pro, model-assisted source review; expiol, named decision signoff"
    manifest["manual_review_queue"] = {
        "path": "manual_review_queue_2026-08-18.csv",
        "rows": 228,
        "status": "pending_named_source_and_evidence_signoff",
    }
    manifest["manual_decision_signoff_revision"] = {
        "date": DATE,
        "reviewer": REVIEWER,
        "ledger": "adjudication/manual_decision_signoff_2026-08-21.csv",
        "reviewed": 32,
        "approved": 30,
        "rejected": 2,
        "resulting_active_corpus": 228,
        "decision_scope": "membership_and_dominant_contribution_only",
        "source_evidence_verified": False,
    }
    manifest["verification_note"] = (
        "Named reviewer expiol confirmed all 32 changed membership/contribution decisions "
        "on 2026-08-21. The 228-work source/evidence queue remains pending and must not be "
        "described as fully reviewed."
    )
    tracked = {
        "adjudication/manual_signoff_changes_2026-08-18.csv": signoff_path,
        "adjudication/manual_decision_signoff_2026-08-21.csv": audit_path,
        "author_priority_review.csv": CORPUS / "author_priority_review.csv",
        "identifier_alias_overrides.csv": CORPUS / "identifier_alias_overrides.csv",
        "identifier_aliases.csv": CORPUS / "identifier_aliases.csv",
        "manual_review_queue_2026-08-18.csv": CORPUS / "manual_review_queue_2026-08-18.csv",
        "review_ledger.csv": CORPUS / "review_ledger.csv",
        "routes.csv": CORPUS / "routes.csv",
        "screened_out.csv": CORPUS / "screened_out.csv",
        "set1_core.csv": CORPUS / "set1_core.csv",
        "set2_emerging.csv": CORPUS / "set2_emerging.csv",
        "set3_context.csv": CORPUS / "set3_context.csv",
        "sets/01_search_catalog/post_cutoff_papers.csv": CORPUS / "sets/01_search_catalog/post_cutoff_papers.csv",
        "summary.csv": CORPUS / "summary.csv",
    }
    for relative, path in tracked.items():
        manifest["files"][relative] = {"sha256": sha256(path), "rows": len(read_csv(path)[1])}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "approve": 30,
        "reject": 2,
        "set1_core": counts["set1_core"],
        "set2_emerging": counts["set2_emerging"],
        "set3_context": counts["set3_context"],
        "screened_out": counts["screened_out"],
        "active": counts["set1_core"] + counts["set2_emerging"],
        "universe": sum(counts.values()),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
