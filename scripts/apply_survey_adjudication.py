#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
DATE = "2026-08-18"

MOVE = {
    "arxiv:2502.14321": "protocol_or_standard",
    "doi:10.1117/12.3076579": "related_work",
    "arxiv:2506.05364": "protocol_or_standard",
    "doi:10.3389/fcomp.2026.1802727": "agentic_security_context",
    "doi:10.21203/rs.3.rs-9839978/v1": "related_work",
    "arxiv:2606.26627": "agentic_security_context",
    "doi:10.20944/preprints202604.2147.v1": "protocol_or_standard",
}
KEEP = {
    "ko2026sevenchallenges",
    "raza2026trism",
    "doi:10.56726/irjmets98584",
    "doi:10.59324/ejaset.2026.4(2).16",
    "doi:10.38124/ijisrt/26feb1090",
    "doi:10.20944/preprints202602.1655.v1",
    "arxiv:2604.23338",
    "doi:10.2139/ssrn.7218206",
}
DUPLICATE = "doi:10.2139/ssrn.6839946"
CANONICAL = "doi:10.21203/rs.3.rs-9839978/v1"
CANONICAL_DOI = "10.21203/rs.3.rs-9839978/v1"
DUPLICATE_DOI = "10.2139/ssrn.6839946"
CANONICAL_TITLE = "Agentic and Multi-Agent Systems: A Systematic Review of Tool Use, Benchmarks, and Governance"
CANONICAL_URL = "https://www.researchsquare.com/article/rs-9839978/v1"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = []
        for row in rows:
            for key in row:
                if key not in fields:
                    fields.append(key)
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


def contextualize(row: dict[str, str], role: str) -> dict[str, str]:
    out = dict(row)
    out["evidence_set"] = "set3_context"
    out["strict_scope_pass"] = "no"
    out["scope_reason"] = (
        "2026-08-18 survey-scope adjudication: useful contextual literature, but MAS-specific "
        "security is not a substantive primary contribution of the survey."
    )
    out["citation_role"] = role
    out["emerging_direction"] = ""
    out["decision_reason"] = (
        "Moved to Set 3 by explicit survey-scope adjudication. Security may be discussed, but the "
        "survey primarily systematizes broader agentic or MAS architecture, communication, orchestration, "
        "privacy, or governance rather than MAS-specific security."
    )
    out["reviewer"] = "OpenAI GPT-5.6 Pro, model-assisted source review"
    out["reviewed_at"] = DATE
    out["author_signoff_required"] = "yes"
    out["membership_reason"] = "Outside the MAS-security corpus after explicit 2026-08-18 survey-scope adjudication; retained for contextual citation use."
    return out


def replace_duplicate_refs(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    result = []
    for row in rows:
        out = {}
        for key, value in row.items():
            text = value or ""
            text = text.replace(DUPLICATE, CANONICAL)
            out[key] = text
        result.append(out)
    return result


def main() -> int:
    paths = {name: C / name for name in (
        "set1_core.csv", "set2_emerging.csv", "set3_context.csv", "screened_out.csv",
        "review_ledger.csv", "routes.csv", "identifier_aliases.csv", "author_priority_review.csv",
        "identifier_alias_overrides.csv",
    )}
    set1 = read_csv(paths["set1_core.csv"])
    set2 = read_csv(paths["set2_emerging.csv"])
    set3 = read_csv(paths["set3_context.csv"])
    screened = read_csv(paths["screened_out.csv"])
    ledger = read_csv(paths["review_ledger.csv"])

    all_active = {row["work_key"] for row in set1 + set2}
    missing = (set(MOVE) | KEEP | {DUPLICATE}) - all_active
    if missing:
        raise SystemExit(f"survey adjudication keys missing from active corpus: {sorted(missing)}")

    moved: list[dict[str, str]] = []
    new_set1 = []
    for row in set1:
        key = row["work_key"]
        if key in MOVE:
            moved.append(contextualize(row, MOVE[key]))
        else:
            new_set1.append(row)

    new_set2 = []
    for row in set2:
        key = row["work_key"]
        if key == DUPLICATE:
            continue
        if key in MOVE:
            moved.append(contextualize(row, MOVE[key]))
        else:
            new_set2.append(row)

    if len(new_set1) != 104 or len(new_set2) != 128 or len(moved) != 7:
        raise SystemExit(f"unexpected survey migration sizes: set1={len(new_set1)}, set2={len(new_set2)}, moved={len(moved)}")

    new_set3 = set3 + moved
    if len(new_set3) != 441:
        raise SystemExit(f"unexpected Set 3 size: {len(new_set3)}")

    moved_by_key = {row["work_key"]: row for row in moved}
    new_ledger = []
    for row in ledger:
        key = row["work_key"]
        if key == DUPLICATE:
            continue
        if key in moved_by_key:
            new_ledger.append(dict(moved_by_key[key]))
        else:
            new_ledger.append(row)
    if len(new_ledger) != 2216:
        raise SystemExit(f"unexpected deduplicated review universe: {len(new_ledger)}")

    write_csv(paths["set1_core.csv"], new_set1, list(set1[0]))
    write_csv(paths["set2_emerging.csv"], new_set2, list(set2[0]))
    write_csv(paths["set3_context.csv"], new_set3, list(set3[0]))
    write_csv(paths["screened_out.csv"], screened, list(screened[0]))
    write_csv(paths["review_ledger.csv"], new_ledger, list(ledger[0]))

    routes = replace_duplicate_refs(read_csv(paths["routes.csv"]))
    write_csv(paths["routes.csv"], routes)

    aliases = replace_duplicate_refs(read_csv(paths["identifier_aliases.csv"]))
    for row in aliases:
        if (row.get("identifier") or "").lower() == DUPLICATE_DOI:
            row["identifier_status"] = "alias"
            row["work_key"] = CANONICAL
            row["canonical_paper_id"] = CANONICAL
            row["title"] = CANONICAL_TITLE
    seen_alias = set()
    dedup_aliases = []
    for row in aliases:
        sig = (row.get("work_key", ""), row.get("identifier_type", ""), row.get("identifier", ""))
        if sig in seen_alias:
            continue
        seen_alias.add(sig)
        dedup_aliases.append(row)
    write_csv(paths["identifier_aliases.csv"], dedup_aliases)

    priority = replace_duplicate_refs(read_csv(paths["author_priority_review.csv"]))
    seen_priority = set()
    dedup_priority = []
    for row in priority:
        key = row.get("work_key", "")
        if key and key in seen_priority:
            continue
        if key:
            seen_priority.add(key)
        dedup_priority.append(row)
    write_csv(paths["author_priority_review.csv"], dedup_priority)

    overrides = read_csv(paths["identifier_alias_overrides.csv"])
    if not any((row.get("alias_type") == "doi" and row.get("alias_value", "").lower() == DUPLICATE_DOI) for row in overrides):
        overrides.append({
            "alias_type": "doi",
            "alias_value": DUPLICATE_DOI,
            "canonical_doi": CANONICAL_DOI,
            "canonical_arxiv_id": "",
            "canonical_title": CANONICAL_TITLE,
            "authoritative_url": CANONICAL_URL,
            "reason": "Research Square and SSRN records are cross-platform versions of the same systematic review; the Research Square record is retained as the canonical work.",
        })
    write_csv(paths["identifier_alias_overrides.csv"], overrides)

    set1_contrib = Counter(row.get("dominant_contribution", "") for row in new_set1)
    set2_contrib = Counter(row.get("dominant_contribution", "") for row in new_set2)
    set3_roles = Counter(row.get("citation_role", "") for row in new_set3)

    summary = []
    for label, count in (("set1_core", len(new_set1)), ("set2_emerging", len(new_set2)), ("set3_context", len(new_set3)), ("screened_out", len(screened))):
        summary.append({"dimension": "evidence_set", "value": label, "count": count})
    for label in ("attack", "defense", "evaluation", "general", "survey"):
        summary.append({"dimension": "set1_core_contribution", "value": label, "count": set1_contrib[label]})
    for label in ("attack", "defense", "evaluation", "general", "survey"):
        summary.append({"dimension": "set2_emerging_contribution", "value": label, "count": set2_contrib[label]})
    for label in sorted(k for k in set3_roles if k):
        summary.append({"dimension": "set3_citation_role", "value": label, "count": set3_roles[label]})
    taxonomy_ready_set1 = sum(row.get("taxonomy_ready") == "yes" for row in new_set1)
    taxonomy_ready_corpus = sum(row.get("taxonomy_ready") == "yes" for row in new_set1 + new_set2)
    summary.append({"dimension": "quality_control", "value": "taxonomy_ready_set1", "count": taxonomy_ready_set1})
    summary.append({"dimension": "quality_control", "value": "author_priority_review", "count": len(dedup_priority)})
    write_csv(C / "summary.csv", summary, ["dimension", "value", "count"])

    manifest_path = C / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["author_priority_review_count"] = len(dedup_priority)
    manifest["search_universe"] = len(new_ledger)
    manifest["counts"] = {
        "set1_core": len(new_set1), "set2_emerging": len(new_set2),
        "set3_context": len(new_set3), "screened_out": len(screened),
    }
    manifest["corpus_counts"] = {"set1_core": len(new_set1), "set2_emerging": len(new_set2), "total_corpus": len(new_set1) + len(new_set2)}
    manifest["set1_contributions"] = {k: set1_contrib[k] for k in ("attack", "defense", "evaluation", "general", "survey")}
    manifest["set2_contributions"] = {k: set2_contrib[k] for k in ("attack", "defense", "evaluation", "general", "survey")}
    manifest["set3_roles"] = {k: set3_roles[k] for k in sorted(k for k in set3_roles if k)}
    manifest["taxonomy_ready_set1_count"] = taxonomy_ready_set1
    manifest["taxonomy_ready_count"] = taxonomy_ready_corpus
    manifest["survey_adjudication_revision"] = {
        "date": DATE,
        "reviewed_records": 16,
        "retained_in_corpus": 8,
        "moved_unique_works_to_set3": 7,
        "identity_duplicates_merged": 1,
        "frozen_corpus_total": len(new_set1) + len(new_set2),
        "review_universe": len(new_ledger),
    }

    tracked = set(manifest.get("files", {})) | {
        "set1_core.csv", "set2_emerging.csv", "set3_context.csv", "screened_out.csv",
        "review_ledger.csv", "routes.csv", "summary.csv", "identifier_aliases.csv",
        "identifier_alias_overrides.csv", "author_priority_review.csv",
        "adjudication/survey_scope_2026-08-18.csv",
    }
    files = {}
    for name in sorted(tracked):
        path = C / name
        if not path.exists():
            continue
        if path.suffix == ".csv":
            rows_count = len(read_csv(path))
        else:
            rows_count = manifest.get("files", {}).get(name, {}).get("rows", 0)
        files[name] = {"rows": rows_count, "sha256": sha256(path)}
    manifest["files"] = files
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    replacements = {
        "Set 1 = 108": "Set 1 = 104",
        "Set 2 = 132": "Set 2 = 128",
        "Set 3 = 434": "Set 3 = 441",
        "240-work MAS-security corpus": "232-work MAS-security corpus",
        "`corpus/set1_core.csv` | 108": "`corpus/set1_core.csv` | 104",
        "`corpus/set2_emerging.csv` | 132": "`corpus/set2_emerging.csv` | 128",
        "`corpus/set3_context.csv` | 434": "`corpus/set3_context.csv` | 441",
        "2,217 deduplicated works": "2,216 deduplicated works",
        "2217": "2216",
        "287-work MAS-security corpus": "232-work MAS-security corpus",
    }
    for old, new in replacements.items():
        readme = readme.replace(old, new)
    marker = "\n## Policy\n"
    note = "\nThe 2026-08-18 survey-scope adjudication reviewed all 16 survey records, retained 8 in the MAS-security corpus, moved 7 unique works to Set 3, and merged one cross-platform duplicate.\n"
    if note.strip() not in readme:
        readme = readme.replace(marker, note + marker)
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    snapshot_path = ROOT / "FROZEN_SNAPSHOT.md"
    snapshot = snapshot_path.read_text(encoding="utf-8")
    for old, new in {
        "| Set 1 | 108 |": "| Set 1 | 104 |",
        "| Set 2 | 132 |": "| Set 2 | 128 |",
        "| Set 3 | 434 |": "| Set 3 | 441 |",
        "| Review universe | 2,217 |": "| Review universe | 2,216 |",
        "Set 1 plus Set 2 is the 240-work MAS-security corpus.": "Set 1 plus Set 2 is the 232-work MAS-security corpus.",
    }.items():
        snapshot = snapshot.replace(old, new)
    section = "\n## 2026-08-18 survey-scope adjudication revision\n\nAll 16 records labeled `survey` in Set 1 and Set 2 were reviewed against the same substantive MAS-security scope gate. Eight surveys remain in the MAS-security corpus, seven unique works move to Set 3 because MAS-specific security is contextual rather than a substantive primary contribution, and the Research Square / SSRN copies of `Agentic and Multi-Agent Systems: A Systematic Review of Tool Use, Benchmarks, and Governance` are merged as one work. The deduplicated review universe is therefore 2,216 works and the MAS-security corpus is 232 works.\n"
    if "survey-scope adjudication revision" not in snapshot:
        snapshot += section
    snapshot_path.write_text(snapshot, encoding="utf-8")

    survey_md = ROOT / "SURVEY_SCOPE_ADJUDICATION.md"
    survey_md.write_text(
        "# Survey Scope Adjudication\n\n"
        "Review date: `2026-08-18`\n\n"
        "All 16 records labeled `survey` in Set 1 and Set 2 were reviewed under one rule: MAS-specific security must be a substantive contribution, not merely a challenge or consideration section.\n\n"
        "## Result\n\n"
        "- 8 surveys remain in the MAS-security corpus: 5 in Set 1 and 3 in Set 2.\n"
        "- 7 unique works move to Set 3.\n"
        "- 1 cross-platform Research Square / SSRN duplicate is merged.\n"
        "- Frozen MAS-security corpus: 232 works.\n"
        "- Frozen review universe after identity correction: 2,216 works.\n\n"
        "See `corpus/adjudication/survey_scope_2026-08-18.csv` for all row-level decisions.\n",
        encoding="utf-8",
    )

    validator_path = ROOT / "scripts" / "validate_three_set_corpus.py"
    validator = validator_path.read_text(encoding="utf-8")
    validator = validator.replace('"set1_core": 108,', '"set1_core": 104,')
    validator = validator.replace('"set2_emerging": 132,', '"set2_emerging": 128,')
    validator = validator.replace('"set3_context": 434,', '"set3_context": 441,')
    validator = validator.replace('"survey": 9}', '"survey": 5}')
    validator = validator.replace('"survey": 7}', '"survey": 3}')
    validator = validator.replace('if len(ledger) != 2217:', 'if len(ledger) != 2216:')
    validator = validator.replace('!= 240:', '!= 232:')
    validator = validator.replace('"manifest corpus total must be frozen at 240"', '"manifest corpus total must be frozen at 232"')
    validator = validator.replace('"MAS-security corpus=240; residual general=9"', '"MAS-security corpus=232; surveys=8; residual general=9"')
    anchor = 'if len(adj1) != 36 or len(adj2) != 73:\n    raise SystemExit("frozen general adjudication ledgers are incomplete")\n'
    survey_check = anchor + '\nsurvey_adj = rows("adjudication/survey_scope_2026-08-18.csv")\nif len(survey_adj) != 16 or sum(row.get("decision") == "keep" for row in survey_adj) != 8 or sum(row.get("decision") == "merge" for row in survey_adj) != 1:\n    raise SystemExit("frozen survey adjudication ledger is incomplete")\n'
    if 'survey_adj = rows(' not in validator:
        validator = validator.replace(anchor, survey_check)
    validator_path.write_text(validator, encoding="utf-8")

    print(
        f"Applied survey adjudication: Set1={len(new_set1)}, Set2={len(new_set2)}, "
        f"Set3={len(new_set3)}, screened={len(screened)}, universe={len(new_ledger)}, corpus={len(new_set1)+len(new_set2)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
