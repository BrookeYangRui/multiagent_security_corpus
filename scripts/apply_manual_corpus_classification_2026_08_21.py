#!/usr/bin/env python3
"""Apply the 228-row named human classification signoff from review drafts."""

from __future__ import annotations

import csv
import difflib
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
QUEUE = CORPUS / "manual_review_queue_2026-08-18.csv"
LEDGER = CORPUS / "review_ledger.csv"
ROUTES = CORPUS / "routes.csv"
STATE_DB = ROOT / ".review-state" / "review.sqlite3"
TRANSACTION = ROOT / ".review-state" / "manual_corpus_classification_2026-08-21"
AUDIT = CORPUS / "adjudication" / "manual_corpus_classification_2026-08-21.csv"
STRUCTURED_EXCLUSIONS = CORPUS / "sets" / "01_search_catalog" / "structured_exclusions.csv"
DATE = "2026-08-21"
REVIEWER = "expiol"

SET_FILES = {
    "set1_core": CORPUS / "set1_core.csv",
    "set2_emerging": CORPUS / "set2_emerging.csv",
    "set3_context": CORPUS / "set3_context.csv",
    "screened_out": CORPUS / "screened_out.csv",
}
SCOPE_DECISIONS = {"accept", "move_set3", "exclude"}
CONTRIBUTIONS = {"attack", "defense", "evaluation", "general", "survey"}
EXPECTED_SCOPE = Counter({"accept": 201, "move_set3": 18, "exclude": 9})
EXPECTED_COUNTS = {
    "set1_core": 96,
    "set2_emerging": 105,
    "set3_context": 463,
    "screened_out": 1550,
}
EXPECTED_SET1 = {"attack": 24, "defense": 40, "evaluation": 22, "general": 5, "survey": 5}
EXPECTED_SET2 = {"attack": 18, "defense": 54, "evaluation": 22, "general": 6, "survey": 5}

TOUCHED = [
    Path("README.md"),
    Path("FROZEN_SNAPSHOT.md"),
    Path("corpus/README.md"),
    Path("corpus/author_priority_review.csv"),
    Path("corpus/manifest.json"),
    Path("corpus/manual_review_queue_2026-08-18.csv"),
    Path("corpus/review_ledger.csv"),
    Path("corpus/routes.csv"),
    Path("corpus/set1_core.csv"),
    Path("corpus/set2_emerging.csv"),
    Path("corpus/set3_context.csv"),
    Path("corpus/screened_out.csv"),
    Path("corpus/summary.csv"),
    Path("scripts/validate_three_set_corpus.py"),
    Path("corpus/adjudication/manual_corpus_classification_2026-08-21.csv"),
    Path("corpus/sets/01_search_catalog/structured_exclusions.csv"),
]


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


def append_once(value: str, sentence: str) -> str:
    value = value.strip()
    if sentence in value:
        return value
    return f"{value} {sentence}".strip()


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected text missing from {path}: {old}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def backup_originals() -> dict[str, str]:
    if TRANSACTION.exists():
        raise SystemExit(f"transaction already exists: {TRANSACTION}")
    originals = TRANSACTION / "originals"
    originals.mkdir(parents=True)
    hashes: dict[str, str] = {}
    for relative in TOUCHED:
        source = ROOT / relative
        if not source.exists():
            continue
        target = originals / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        hashes[relative.as_posix()] = sha256(source)
    shutil.copy2(LEDGER, TRANSACTION / "ORIGINAL_FILE.csv")
    return hashes


def load_drafts() -> dict[str, dict[str, object]]:
    connection = sqlite3.connect(STATE_DB)
    try:
        rows = connection.execute(
            "SELECT work_key, payload FROM drafts WHERE queue = 'corpus'"
        ).fetchall()
    finally:
        connection.close()
    drafts = {str(key): json.loads(str(payload)) for key, payload in rows}
    if len(drafts) != 228:
        raise SystemExit(f"expected 228 corpus drafts, found {len(drafts)}")
    scopes = Counter(str(draft.get("human_scope_decision", "")) for draft in drafts.values())
    if scopes != EXPECTED_SCOPE:
        raise SystemExit(f"unexpected scope decisions: {scopes}")
    for key, draft in drafts.items():
        scope = str(draft.get("human_scope_decision", ""))
        contribution = str(draft.get("human_contribution_decision", ""))
        if scope not in SCOPE_DECISIONS:
            raise SystemExit(f"invalid scope decision for {key}: {scope}")
        if contribution and contribution not in CONTRIBUTIONS:
            raise SystemExit(f"invalid contribution decision for {key}: {contribution}")
    return drafts


def apply_ledger(
    drafts: dict[str, dict[str, object]],
    queue_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    fields, rows = read_csv(LEDGER)
    by_key = {row["work_key"]: row for row in rows}
    queue_by_key = {row["work_key"]: row for row in queue_rows}
    if set(drafts) != set(queue_by_key):
        raise SystemExit("drafts and manual queue do not identify the same 228 works")
    missing = set(drafts) - set(by_key)
    if missing:
        raise SystemExit(f"draft works missing from ledger: {sorted(missing)}")

    for key, draft in drafts.items():
        row = by_key[key]
        scope = str(draft["human_scope_decision"])
        contribution = str(draft.get("human_contribution_decision", ""))
        notes = str(draft.get("human_notes", "")).strip()
        old_set = row["evidence_set"]
        old_contribution = row["dominant_contribution"]

        if contribution:
            row["dominant_contribution"] = contribution

        if scope == "accept":
            row["strict_scope_pass"] = "yes"
            row["evidence_set"] = old_set
            if row.get("citation_role") == "source_readiness_context":
                row["citation_role"] = ""
            scope_result = f"retained in {old_set}"
        elif scope == "move_set3":
            row["strict_scope_pass"] = "no"
            row["evidence_set"] = "set3_context"
            row["citation_role"] = row.get("citation_role", "") or "related_work"
            row["paper_section"] = row.get("paper_section", "") or "Overview and Related Work"
            scope_result = "moved to set3_context"
        else:
            row["strict_scope_pass"] = "no"
            row["evidence_set"] = "screened_out"
            row["citation_role"] = ""
            scope_result = "moved to screened_out"

        if scope != "accept":
            explanation = notes or "Named human classification found that the work does not meet the active MAS-security scope decision."
            row["scope_reason"] = f"{DATE} named human classification: {scope_result}. {explanation}"

        contribution_result = row["dominant_contribution"]
        sentence = (
            f"{DATE} named corpus classification signoff by {REVIEWER}: "
            f"{scope_result}; dominant_contribution={contribution_result}."
        )
        row["decision_reason"] = append_once(row.get("decision_reason", ""), sentence)
        reviewer = row.get("reviewer", "").strip()
        signoff = f"{REVIEWER}, named corpus classification signoff"
        if signoff not in reviewer:
            row["reviewer"] = f"{reviewer}; {signoff}".strip("; ")
        row["reviewed_at"] = DATE
        row["author_signoff_required"] = "no"

        queue = queue_by_key[key]
        queue["human_scope_decision"] = scope
        queue["human_contribution_decision"] = contribution
        queue["human_notes"] = notes
        queue["evidence_set"] = row["evidence_set"]
        queue["dominant_contribution"] = row["dominant_contribution"]
        queue["scope_reason"] = row["scope_reason"]
        queue["decision_reason"] = row["decision_reason"]
        queue["author_signoff_required"] = "no"

    write_csv(LEDGER, fields, sorted(rows, key=lambda row: row["work_key"]))
    return rows


def write_audit(
    drafts: dict[str, dict[str, object]],
    original_queue: list[dict[str, str]],
    final_ledger: list[dict[str, str]],
) -> None:
    original = {row["work_key"]: row for row in original_queue}
    final = {row["work_key"]: row for row in final_ledger}
    fields = [
        "work_key",
        "title",
        "previous_membership",
        "human_scope_decision",
        "adjudicated_membership",
        "previous_contribution",
        "human_contribution_decision",
        "adjudicated_contribution",
        "reviewer",
        "reviewed_at",
        "decision_scope",
        "source_evidence_verified",
        "human_notes",
        "adjudication_note",
    ]
    rows: list[dict[str, str]] = []
    for key in original:
        draft = drafts[key]
        before = original[key]
        after = final[key]
        scope = str(draft["human_scope_decision"])
        selected = str(draft.get("human_contribution_decision", ""))
        notes = str(draft.get("human_notes", "")).strip()
        contribution_note = selected or f"retained previous value ({before['dominant_contribution']})"
        rows.append({
            "work_key": key,
            "title": before["title"],
            "previous_membership": before["evidence_set"],
            "human_scope_decision": scope,
            "adjudicated_membership": after["evidence_set"],
            "previous_contribution": before["dominant_contribution"],
            "human_contribution_decision": selected,
            "adjudicated_contribution": after["dominant_contribution"],
            "reviewer": REVIEWER,
            "reviewed_at": DATE,
            "decision_scope": "membership_and_dominant_contribution_only",
            "source_evidence_verified": "no",
            "human_notes": notes,
            "adjudication_note": (
                f"Human scope decision={scope}; contribution decision={contribution_note}. "
                "This classification signoff does not assert source/evidence verification."
            ),
        })
    write_csv(AUDIT, fields, rows)


def stable_paper_id(row: dict[str, str]) -> str:
    if row.get("canonical_paper_id"):
        return row["canonical_paper_id"].lower()
    value = row["work_key"].lower()
    for character in ":/.":
        value = value.replace(character, "_")
    return value


def write_structured_exclusions(
    final_ledger: list[dict[str, str]],
    drafts: dict[str, dict[str, object]],
) -> None:
    fields = [
        "paper_id",
        "title",
        "decision",
        "reason_code",
        "reason",
        "canonical_paper_id",
        "reviewer",
        "reviewed_at",
        "source",
    ]
    rows = []
    for row in final_ledger:
        if row["work_key"] not in drafts:
            continue
        draft = drafts[row["work_key"]]
        if draft["human_scope_decision"] != "exclude":
            continue
        paper_id = stable_paper_id(row)
        rows.append({
            "paper_id": paper_id,
            "title": row["title"],
            "decision": "exclude",
            "reason_code": "named_human_scope_exclusion",
            "reason": row["scope_reason"],
            "canonical_paper_id": row.get("canonical_paper_id") or paper_id,
            "reviewer": REVIEWER,
            "reviewed_at": DATE,
            "source": "corpus/adjudication/manual_corpus_classification_2026-08-21.csv",
        })
    if len(rows) != 9:
        raise SystemExit(f"expected 9 structured exclusions, found {len(rows)}")
    write_csv(STRUCTURED_EXCLUSIONS, fields, sorted(rows, key=lambda row: row["paper_id"]))


def rebuild_sets() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/rebuild_membership_from_ledger.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise SystemExit((result.stderr or result.stdout).strip())


def update_queue_from_ledger(
    queue_fields: list[str],
    queue_rows: list[dict[str, str]],
    drafts: dict[str, dict[str, object]],
) -> None:
    _, ledger_rows = read_csv(LEDGER)
    ledger = {row["work_key"]: row for row in ledger_rows}
    source_fields = [field for field in queue_fields if not field.startswith("human_")]
    output: list[dict[str, str]] = []
    for old in queue_rows:
        current = ledger[old["work_key"]]
        draft = drafts[old["work_key"]]
        row = {field: current.get(field, "") for field in source_fields}
        row.update({
            "human_scope_decision": str(draft["human_scope_decision"]),
            "human_contribution_decision": str(draft.get("human_contribution_decision", "")),
            "human_notes": str(draft.get("human_notes", "")).strip(),
        })
        output.append(row)
    write_csv(QUEUE, queue_fields, output)


def update_routes(
    final_ledger: list[dict[str, str]],
    reviewed_keys: set[str],
) -> None:
    fields, rows = read_csv(ROUTES)
    final = {row["work_key"]: row for row in final_ledger}
    for route in rows:
        record = final.get(route["work_key"])
        if record is None or route["work_key"] not in reviewed_keys:
            continue
        route["current_primary_category"] = record["dominant_contribution"]
        route["human_signoff_required"] = "no"
        evidence_set = record["evidence_set"]
        route["ledger_decision"] = (
            "primary" if evidence_set in {"set1_core", "set2_emerging"}
            else "secondary" if evidence_set == "set3_context"
            else "exclude"
        )
        route["ledger_decision_source"] = "manual-corpus-classification:2026-08-21"
    write_csv(ROUTES, fields, rows)


def write_summary() -> None:
    sets = {name: read_csv(path)[1] for name, path in SET_FILES.items()}
    rows = [
        {"metric": "evidence_set", "label": name, "count": str(len(sets[name]))}
        for name in SET_FILES
    ]
    for name in ("set1_core", "set2_emerging"):
        counts = Counter(row["dominant_contribution"] for row in sets[name])
        for label, count in sorted(counts.items()):
            rows.append({"metric": f"{name}_contribution", "label": label, "count": str(count)})
    roles = Counter(row["citation_role"] or "related_work" for row in sets["set3_context"])
    for label, count in sorted(roles.items()):
        rows.append({"metric": "set3_citation_role", "label": label, "count": str(count)})
    _, priority = read_csv(CORPUS / "author_priority_review.csv")
    rows.extend([
        {
            "metric": "quality_control",
            "label": "taxonomy_ready_set1",
            "count": str(sum(row["taxonomy_ready"] == "yes" for row in sets["set1_core"])),
        },
        {"metric": "quality_control", "label": "author_priority_review", "count": str(len(priority))},
        {"metric": "decision_signoff", "label": "changed_queue_approve", "count": "30"},
        {"metric": "decision_signoff", "label": "changed_queue_reject", "count": "2"},
        {"metric": "classification_signoff", "label": "accept", "count": "201"},
        {"metric": "classification_signoff", "label": "move_set3", "count": "18"},
        {"metric": "classification_signoff", "label": "exclude", "count": "9"},
    ])
    write_csv(CORPUS / "summary.csv", ["metric", "label", "count"], rows)


def update_documents() -> None:
    readme = ROOT / "README.md"
    replace_once(
        readme,
        "The USENIX 2027 SoK manuscript-facing corpus is frozen on `2026-08-18` and corrected by named decision signoff on `2026-08-21`. The authoritative counts are **Set 1 = 105**, **Set 2 = 123**, **Set 3 = 445**, and **screened out = 1,541**. Set 1 and Set 2 together form the **228-work MAS-security corpus**.",
        "The USENIX 2027 SoK manuscript-facing corpus is frozen on `2026-08-18` and corrected by named classification signoff on `2026-08-21`. The authoritative counts are **Set 1 = 96**, **Set 2 = 105**, **Set 3 = 463**, and **screened out = 1,550**. Set 1 and Set 2 together form the **201-work MAS-security corpus**.",
    )
    replace_once(readme, "The frozen ledger contains 2,215 deduplicated works", "The frozen ledger contains 2,214 deduplicated works")
    replace_once(readme, "| `corpus/set1_core.csv` | 105 |", "| `corpus/set1_core.csv` | 96 |")
    replace_once(readme, "| `corpus/set2_emerging.csv` | 123 |", "| `corpus/set2_emerging.csv` | 105 |")
    replace_once(readme, "| `corpus/set3_context.csv` | 445 |", "| `corpus/set3_context.csv` | 463 |")
    replace_once(readme, "| `corpus/screened_out.csv` | 1,541 |", "| `corpus/screened_out.csv` | 1,550 |")
    replace_once(
        readme,
        "Set 1 and Set 2 use the same MAS-security scope gate and together form the 228-work MAS-security corpus.",
        "Set 1 and Set 2 use the same MAS-security scope gate and together form the 201-work MAS-security corpus.",
    )
    replace_once(
        readme,
        "`corpus/manual_review_queue_2026-08-18.csv` contains all 228 active works for source/evidence review. The 32 changed membership/contribution decisions received named signoff on 2026-08-21.",
        "`corpus/manual_review_queue_2026-08-18.csv` preserves the 228-work human-classification cohort. Named classification signoff retained 201 active works, moved 18 to Set 3, and screened out 9; source/evidence verification remains separate.",
    )
    with readme.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n\n## 2026-08-21 complete classification signoff\n\n"
            "Reviewer `expiol` adjudicated the complete 228-work classification cohort: "
            "201 accepted, 18 moved to Set 3, and 9 screened out. The resulting active "
            "corpus contains 96 Set 1 works and 105 Set 2 works. This is a scope and "
            "dominant-contribution signoff only; it does not upgrade source/evidence "
            "verification status.\n"
        )

    frozen = ROOT / "FROZEN_SNAPSHOT.md"
    replace_once(frozen, "| Set 1 | 105 |", "| Set 1 | 96 |")
    replace_once(frozen, "| Set 2 | 123 |", "| Set 2 | 105 |")
    replace_once(frozen, "| Set 3 | 445 |", "| Set 3 | 463 |")
    replace_once(frozen, "| Screened out | 1,541 |", "| Screened out | 1,550 |")
    replace_once(frozen, "Set 1 plus Set 2 is the 228-work MAS-security corpus.", "Set 1 plus Set 2 is the 201-work MAS-security corpus.")
    with frozen.open("a", encoding="utf-8") as handle:
        handle.write(
            "\n\n## 2026-08-21 complete classification-signoff correction\n\n"
            "Named reviewer `expiol` adjudicated all 228 rows in the manual classification "
            "cohort. The decisions retain 201 works in the active MAS-security corpus, move "
            "18 works to Set 3, and screen out 9 works. The corrected partition is "
            "**Set 1 = 96, Set 2 = 105, Set 3 = 463, screened out = 1,550**, for a "
            "**2,214-work frozen review universe**. Dominant contributions use the explicit "
            "human selection where supplied and retain the previous value for 17 blank, "
            "non-applicable, or unresolved contribution fields. This signoff does not assert "
            "source/evidence verification.\n"
        )

    (CORPUS / "README.md").write_text(
        """# Authoritative corpus views

| File | Count | Role in the SoK |
| --- | ---: | --- |
| `set1_core.csv` | 96 | In-scope mature corpus: peer reviewed or at least 10 frozen citations. |
| `set2_emerging.csv` | 105 | In-scope emerging corpus that has not yet met the Set 1 maturity rule. |
| `set3_context.csv` | 463 | Contextual citations; not part of the MAS-security corpus. |
| `screened_out.csv` | 1,550 | Reviewed search records outside the active evidence sets. |

Set 1 and Set 2 use the same MAS-security scope gate. Membership requires an
LLM multi-agent system, a concrete security property, and a material inter-agent
interaction path. Whether the paper isolates a causal interaction effect is an
evidence-strength question, not a corpus inclusion rule.

Set 1 then applies the maturity union rule: peer reviewed **or** frozen citation
count >= 10. Full-text taxonomy readiness is tracked separately by the
`taxonomy_ready` field and never removes an otherwise eligible paper from Set 1.
Set 2 contains the remaining in-scope early work. Set 3 is contextual only.

Reviewer `expiol` completed named scope and dominant-contribution classification
for the 228-row manual cohort on 2026-08-21. The resulting active corpus contains
201 works. Source/evidence verification remains separate, and these decisions
must not be described as full evidence verification.
""",
        encoding="utf-8",
    )


def write_validator() -> None:
    validator = ROOT / "scripts" / "validate_three_set_corpus.py"
    validator.write_text(
        '''#!/usr/bin/env python3
import csv,json
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; C=R/"corpus"
FILES={"set1_core":"set1_core.csv","set2_emerging":"set2_emerging.csv","set3_context":"set3_context.csv","screened_out":"screened_out.csv"}
EXPECTED={'set1_core':96,'set2_emerging':105,'set3_context':463,'screened_out':1550}
E1={'attack':24,'defense':40,'evaluation':22,'general':5,'survey':5}
E2={'attack':18,'defense':54,'evaluation':22,'general':6,'survey':5}
def rows(p):
    with (C/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
S={k:rows(v) for k,v in FILES.items()}; actual={k:len(v) for k,v in S.items()}
if actual!=EXPECTED: raise SystemExit(f"signed counts changed: {actual} != {EXPECTED}")
K={k:{r["work_key"] for r in v} for k,v in S.items()}
for a in K:
  for b in K:
    if a<b and K[a]&K[b]: raise SystemExit(f"overlap {a} {b}")
L=rows("review_ledger.csv"); LB={r["work_key"]:r for r in L}
if len(L)!=2214 or set().union(*K.values())!=set(LB): raise SystemExit("ledger partition mismatch")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="yes" for r in S["set1_core"]): raise SystemExit("invalid Set 1 row")
if any(r["strict_scope_pass"]!="yes" or r["maturity_rule_pass"]!="no" for r in S["set2_emerging"]): raise SystemExit("invalid Set 2 row")
if any(r["strict_scope_pass"]=="yes" or not r["citation_role"] for r in S["set3_context"]): raise SystemExit("invalid Set 3 row")
if dict(Counter(r["dominant_contribution"] for r in S["set1_core"]))!=E1: raise SystemExit("Set 1 contribution mismatch")
if dict(Counter(r["dominant_contribution"] for r in S["set2_emerging"]))!=E2: raise SystemExit("Set 2 contribution mismatch")
Q=rows("manual_review_queue_2026-08-18.csv")
if len(Q)!=228 or Counter(r["human_scope_decision"] for r in Q)!={"accept":201,"move_set3":18,"exclude":9}: raise SystemExit("manual classification queue mismatch")
A=rows("adjudication/manual_corpus_classification_2026-08-21.csv")
if len(A)!=228 or any(r["reviewer"]!="expiol" or r["source_evidence_verified"]!="no" for r in A): raise SystemExit("classification audit mismatch")
X=rows("sets/01_search_catalog/structured_exclusions.csv")
if len(X)!=9 or any(r["decision"]!="exclude" or r["reviewer"]!="expiol" for r in X): raise SystemExit("structured exclusions mismatch")
for r in A:
  expected={"accept":r["previous_membership"],"move_set3":"set3_context","exclude":"screened_out"}[r["human_scope_decision"]]
  if r["adjudicated_membership"]!=expected or LB[r["work_key"]]["evidence_set"]!=expected: raise SystemExit(f"classification application mismatch: {r['work_key']}")
  if r["human_contribution_decision"] and LB[r["work_key"]]["dominant_contribution"]!=r["human_contribution_decision"]: raise SystemExit(f"contribution application mismatch: {r['work_key']}")
signoff=rows("adjudication/manual_signoff_changes_2026-08-18.csv")
if len(signoff)!=32 or Counter(r["human_decision"] for r in signoff)!={"approve":30,"reject":2}: raise SystemExit("changed-decision signoff mismatch")
m=json.loads((C/"manifest.json").read_text())
if m["counts"]!=actual or m["corpus_counts"]["total_corpus"]!=201 or m["search_universe"]!=2214: raise SystemExit("manifest mismatch")
print("Human-classified corpus valid: Set1=96 Set2=105 Set3=463 screened=1550 active=201 universe=2214 scope=201/18/9 source_evidence_verified=no")
''',
        encoding="utf-8",
    )
    validator.chmod(0o755)


def update_manifest() -> None:
    path = CORPUS / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    sets = {name: read_csv(file)[1] for name, file in SET_FILES.items()}
    counts = {name: len(rows) for name, rows in sets.items()}
    manifest["counts"] = counts
    manifest["corpus_counts"] = {"set1_core": 96, "set2_emerging": 105, "total_corpus": 201}
    manifest["search_universe"] = 2214
    manifest["set1_contributions"] = dict(Counter(row["dominant_contribution"] for row in sets["set1_core"]))
    manifest["set2_contributions"] = dict(Counter(row["dominant_contribution"] for row in sets["set2_emerging"]))
    manifest["set3_roles"] = dict(Counter(row["citation_role"] or "related_work" for row in sets["set3_context"]))
    manifest["reviewer"] = (
        "OpenAI GPT-5.6 Pro, model-assisted source review; expiol, named decision signoff; "
        "expiol, named corpus classification signoff"
    )
    manifest["manual_review_queue"] = {
        "path": "manual_review_queue_2026-08-18.csv",
        "rows": 228,
        "status": "classification_signoff_complete_source_evidence_pending",
    }
    manifest["manual_corpus_classification_signoff_revision"] = {
        "date": DATE,
        "reviewer": REVIEWER,
        "ledger": "adjudication/manual_corpus_classification_2026-08-21.csv",
        "reviewed": 228,
        "accepted": 201,
        "moved_to_set3": 18,
        "excluded": 9,
        "explicit_contribution_decisions": 211,
        "retained_previous_contributions": 17,
        "resulting_active_corpus": 201,
        "decision_scope": "membership_and_dominant_contribution_only",
        "source_evidence_verified": False,
    }
    manifest["verification_note"] = (
        "Named reviewer expiol classified all 228 reviewed works on 2026-08-21. "
        "The signoff covers scope and dominant contribution only; source/evidence "
        "verification remains pending and must not be inferred from classification signoff."
    )
    manifest["files"] = {}
    for csv_path in sorted(CORPUS.rglob("*.csv")):
        relative = csv_path.relative_to(CORPUS).as_posix()
        manifest["files"][relative] = {"sha256": sha256(csv_path), "rows": len(read_csv(csv_path)[1])}
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def create_artifacts(original_hashes: dict[str, str], modified_test: subprocess.CompletedProcess[str]) -> None:
    shutil.copy2(LEDGER, TRANSACTION / "MODIFIED_FILE.csv")
    before = (TRANSACTION / "ORIGINAL_FILE.csv").read_text(encoding="utf-8").splitlines(keepends=True)
    after = (TRANSACTION / "MODIFIED_FILE.csv").read_text(encoding="utf-8").splitlines(keepends=True)
    diff = difflib.unified_diff(before, after, fromfile="ORIGINAL_FILE.csv", tofile="MODIFIED_FILE.csv")
    (TRANSACTION / "DIFF_FILE.patch").write_text("".join(diff), encoding="utf-8")

    backup = (TRANSACTION / "originals").as_posix()
    restore_lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        'TARGET="${1:-' + ROOT.as_posix() + '}"',
        f'BACKUP="{backup}"',
    ]
    for relative in TOUCHED:
        rel = relative.as_posix()
        if rel in original_hashes:
            restore_lines.extend([
                f'mkdir -p "$TARGET/{relative.parent.as_posix()}"',
                f'cp -p "$BACKUP/{rel}" "$TARGET/{rel}"',
            ])
        else:
            restore_lines.append(f'rm -f "$TARGET/{rel}"')
    restore_lines.append('printf "%s\\n" "ROLLBACK_OK target=$TARGET restored=pre-classification state"')
    rollback = TRANSACTION / "ROLLBACK.sh"
    rollback.write_text("\n".join(restore_lines) + "\n", encoding="utf-8")
    rollback.chmod(0o755)

    test_root = TRANSACTION / "ROLLBACK_TEST"
    for relative in TOUCHED:
        source = ROOT / relative
        if source.exists():
            target = test_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    rollback_test = subprocess.run([str(rollback), str(test_root)], text=True, capture_output=True, check=False)
    if rollback_test.returncode:
        raise SystemExit(rollback_test.stderr or rollback_test.stdout)
    for relative, expected_hash in original_hashes.items():
        restored = test_root / relative
        if not restored.exists() or sha256(restored) != expected_hash:
            raise SystemExit(f"rollback test mismatch: {relative}")

    verification = f"""Classification branch/field: human_scope_decision and human_contribution_decision
Result: accept=201; move_set3=18; exclude=9; active corpus=201; source_evidence_verified=no
Original review ledger SHA256: {original_hashes['corpus/review_ledger.csv']}
Modified review ledger SHA256: {sha256(LEDGER)}
MODIFIED_FILE: {TRANSACTION / 'MODIFIED_FILE.csv'}
DIFF_FILE: {TRANSACTION / 'DIFF_FILE.patch'}
VERIFICATION: {TRANSACTION / 'VERIFICATION.txt'}
ROLLBACK: {rollback}

BASELINE command: scripts/validate_all.sh
BASELINE input: repository state before applying the 228-row classification
BASELINE literal output: Corrected corpus valid: Set1=105 Set2=123 Set3=445 screened=1541 active=228 universe=2214 signoff=30/2
BASELINE exit status: 0

MODIFIED command: scripts/validate_all.sh
MODIFIED input: 228 SQLite corpus drafts; blank contribution decisions retain the previous value
MODIFIED literal output: {modified_test.stdout.strip()}
MODIFIED exit status: {modified_test.returncode}

ROLLBACK command: {rollback} {test_root}
ROLLBACK input: copy of the modified files under ROLLBACK_TEST
ROLLBACK literal output: {rollback_test.stdout.strip()}
ROLLBACK exit status: {rollback_test.returncode}
ROLLBACK restored behavior/status: pre-classification hashes restored for all {len(original_hashes)} pre-existing touched files; MODIFIED_FILE remains changed.
"""
    (TRANSACTION / "VERIFICATION.txt").write_text(verification, encoding="utf-8")


def main() -> int:
    original_hashes = backup_originals()
    queue_fields, queue_rows = read_csv(QUEUE)
    original_queue = [dict(row) for row in queue_rows]
    drafts = load_drafts()
    apply_ledger(drafts, queue_rows)
    rebuild_sets()
    _, rebuilt_ledger = read_csv(LEDGER)
    write_audit(drafts, original_queue, rebuilt_ledger)
    write_structured_exclusions(rebuilt_ledger, drafts)
    update_queue_from_ledger(queue_fields, queue_rows, drafts)
    _, final_ledger = read_csv(LEDGER)
    update_routes(final_ledger, set(drafts))
    write_summary()
    update_documents()
    write_validator()
    update_manifest()

    modified_test = subprocess.run(
        ["scripts/validate_all.sh"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if modified_test.returncode:
        raise SystemExit((modified_test.stderr or modified_test.stdout).strip())
    create_artifacts(original_hashes, modified_test)
    print(modified_test.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
