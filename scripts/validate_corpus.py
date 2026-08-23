#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "corpus"
P = R / "papers"

EXPECTED_COUNTS = {"set1_core": 96, "set2_emerging": 105, "total_corpus": 201}
EXPECTED_CONTRIB = {"attack": 42, "defense": 94, "evaluation": 44, "general": 11, "survey": 10}
CATEGORY_DIR = {"attack": "attacks", "defense": "defenses", "evaluation": "evaluations", "general": "general", "survey": "surveys"}


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


s1 = rows(C / "set1_core.csv")
s2 = rows(C / "set2_emerging.csv")
if (len(s1), len(s2)) != (96, 105):
    raise SystemExit(f"authoritative counts changed: {len(s1)}/{len(s2)}")
all_rows = s1 + s2
if len(all_rows) != 201:
    raise SystemExit("active corpus is not 201")
keys = [r["work_key"] for r in all_rows]
if len(keys) != len(set(keys)):
    raise SystemExit("duplicate work_key in active corpus")
if any(r.get("strict_scope_pass") != "yes" for r in all_rows):
    raise SystemExit("out of scope row in active corpus")
if any(r.get("maturity_rule_pass") != "yes" for r in s1):
    raise SystemExit("invalid Set 1 maturity")
if any(r.get("maturity_rule_pass") != "no" for r in s2):
    raise SystemExit("invalid Set 2 maturity")
if dict(Counter(r["dominant_contribution"] for r in all_rows)) != EXPECTED_CONTRIB:
    raise SystemExit("signed contribution counts changed")

stale = [
    "set3_context.csv", "screened_out.csv", "review_ledger.csv", "routes.csv",
    "manual_review_queue_2026-08-18.csv", "author_priority_review.csv",
    "identifier_aliases.csv", "identifier_alias_overrides.csv", "adjudication", "sets"
]
if any((C / name).exists() for name in stale):
    raise SystemExit("superseded corpus artifact is still present")

manifest = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
if manifest["counts"] != EXPECTED_COUNTS:
    raise SystemExit("manifest mismatch")

# papers/ must be an exact materialized view of the signed 201 corpus.
if (P / "post_cutoff").exists():
    raise SystemExit("post_cutoff must not exist under papers/")
if not (P / "index.csv").exists():
    raise SystemExit("papers/index.csv is missing")
index = rows(P / "index.csv")
if len(index) != 201:
    raise SystemExit(f"papers/index.csv must have 201 rows, found {len(index)}")
if len({r["work_key"] for r in index}) != 201:
    raise SystemExit("duplicate work_key in papers/index.csv")
if {r["work_key"] for r in index} != set(keys):
    missing = set(keys) - {r["work_key"] for r in index}
    extra = {r["work_key"] for r in index} - set(keys)
    raise SystemExit(f"papers/index.csv membership mismatch: missing={sorted(missing)} extra={sorted(extra)}")

active_by_key = {r["work_key"]: r for r in all_rows}
seen_paths = set()
for item in index:
    key = item["work_key"]
    source = active_by_key[key]
    if item["evidence_set"] != source["evidence_set"]:
        raise SystemExit(f"paper set mismatch: {key}")
    if item["dominant_contribution"] != source["dominant_contribution"]:
        raise SystemExit(f"paper contribution mismatch: {key}")
    expected_prefix = f"papers/{CATEGORY_DIR[source['dominant_contribution']]}/"
    if not item["paper_path"].startswith(expected_prefix):
        raise SystemExit(f"paper category path mismatch: {key} -> {item['paper_path']}")
    if item["paper_path"] in seen_paths:
        raise SystemExit(f"duplicate paper path: {item['paper_path']}")
    seen_paths.add(item["paper_path"])
    path = R / item["paper_path"]
    if not path.is_file():
        raise SystemExit(f"indexed paper note missing: {item['paper_path']}")
    rel = path.relative_to(P)
    if len(rel.parts) < 3:
        raise SystemExit(f"paper not grouped by contribution and venue: {rel}")
    text = path.read_text(encoding="utf-8", errors="replace")
    if "<!-- FINAL_CORPUS_STATUS_START -->" not in text:
        raise SystemExit(f"paper note lacks final status banner: {rel}")

notes = [path for path in P.rglob("*.md") if path.name.lower() != "readme.md"]
if len(notes) != 201:
    raise SystemExit(f"expected exactly 201 paper notes, found {len(notes)}")
if {str(path.relative_to(R)) for path in notes} != seen_paths:
    unindexed = {str(path.relative_to(R)) for path in notes} - seen_paths
    raise SystemExit(f"unindexed paper notes remain: {sorted(unindexed)}")

for contribution, dirname in CATEGORY_DIR.items():
    count = len([path for path in (P / dirname).rglob("*.md") if path.name.lower() != "readme.md"])
    if count != EXPECTED_CONTRIB[contribution]:
        raise SystemExit(f"paper directory count mismatch for {contribution}: {count}")

print("Final corpus valid: Set1=96 Set2=105 total=201; papers=201; category and venue placement indexed")
