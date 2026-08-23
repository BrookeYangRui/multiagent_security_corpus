#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "corpus"
P = R / "papers"

EXPECTED_COUNTS = {"set1_core": 92, "set2_emerging": 97, "total_corpus": 189}
EXPECTED_CONTRIB = {"attack": 45, "defense": 80, "evaluation": 45, "general": 12, "survey": 7}
CATEGORY_DIR = {"attack": "attacks", "defense": "defenses", "evaluation": "evaluations", "general": "general", "survey": "surveys"}


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


s1 = rows(C / "set1_core.csv")
s2 = rows(C / "set2_emerging.csv")
if (len(s1), len(s2)) != (92, 97):
    raise SystemExit(f"authoritative counts changed: {len(s1)}/{len(s2)}")
all_rows = s1 + s2
if len(all_rows) != 189:
    raise SystemExit("active corpus is not 189")
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

# papers/ must be an exact materialized view of the active 189 corpus.
if (P / "post_cutoff").exists():
    raise SystemExit("post_cutoff must not exist under papers/")
if not (P / "index.csv").exists():
    raise SystemExit("papers/index.csv is missing")
index = rows(P / "index.csv")
if len(index) != 189:
    raise SystemExit(f"papers/index.csv must have 189 rows, found {len(index)}")
if len({r["work_key"] for r in index}) != 189:
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
if len(notes) != 189:
    raise SystemExit(f"expected exactly 189 paper notes, found {len(notes)}")
if {str(path.relative_to(R)) for path in notes} != seen_paths:
    unindexed = {str(path.relative_to(R)) for path in notes} - seen_paths
    raise SystemExit(f"unindexed paper notes remain: {sorted(unindexed)}")

for contribution, dirname in CATEGORY_DIR.items():
    count = len([path for path in (P / dirname).rglob("*.md") if path.name.lower() != "readme.md"])
    if count != EXPECTED_CONTRIB[contribution]:
        raise SystemExit(f"paper directory count mismatch for {contribution}: {count}")

# Supporting SoK comparators may overlap the active corpus, but they are never an
# additional denominator. A comparator marked as part of the final corpus must
# point to a real final paper note; contextual comparators must not carry stale
# paper paths from older corpus layouts.
comparator_path = R / "sok_related" / "papers.csv"
if comparator_path.exists():
    comparators = rows(comparator_path)
    if len({r["sok_id"] for r in comparators}) != len(comparators):
        raise SystemExit("duplicate sok comparator id")
    for r in comparators:
        flag = r.get("in_final_201", "").strip().lower()
        paper_path = r.get("final_paper_path", "").strip()
        if flag == "yes":
            if not paper_path or not (R / paper_path).is_file():
                raise SystemExit(f"final SoK comparator path missing: {r['sok_id']} -> {paper_path}")
        elif flag == "no":
            if paper_path:
                raise SystemExit(f"context comparator carries final paper path: {r['sok_id']} -> {paper_path}")
        else:
            raise SystemExit(f"invalid in_final_201 flag for comparator: {r['sok_id']}")

# Maintenance and synthesis docs must not point collaborators back to removed
# corpus layouts or superseded manuscript denominators.
docs = [
    R / "README.md",
    R / "AGENTS.md",
    R / "CORPUS_SET_POLICY.md",
    R / "FROZEN_SNAPSHOT.md",
    R / "sok_related" / "README.md",
]
docs.extend((R / "related_work").glob("*.md"))
legacy_tokens = [
    "corpus/papers.csv",
    "corpus/sets/",
    "reviews/queues/",
    "142-work corpus",
    "142-work package",
    "227-work",
    "228-work",
    "232-work",
    "287-work",
]
for path in docs:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for token in legacy_tokens:
        if token in text:
            raise SystemExit(f"legacy corpus reference remains in {path.relative_to(R)}: {token}")

print("Final corpus valid: Set1=92 Set2=97 total=189; papers=189; category and venue placement indexed; legacy active views absent")
