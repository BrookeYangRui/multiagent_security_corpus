#!/usr/bin/env python3
"""One shot cleanup that makes the signed 201 work corpus the only active corpus.

The script preserves existing full paper notes whenever possible, prunes notes that
are not in the final 201, and places every retained work under
papers/<contribution>/<venue>/ using the existing venue folder when available.
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
PAPERS = ROOT / "papers"

EXPECTED_SET1 = 96
EXPECTED_SET2 = 105
EXPECTED_TOTAL = 201
EXPECTED_CONTRIBUTIONS = {
    "attack": 42,
    "defense": 94,
    "evaluation": 44,
    "general": 11,
    "survey": 10,
}

CATEGORY_DIR = {
    "attack": "attacks",
    "defense": "defenses",
    "evaluation": "evaluations",
    "general": "general",
    "survey": "surveys",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def slug(text: str, limit: int = 90) -> str:
    out = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return (out[:limit].rstrip("_") or "paper")


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value


def normalize_arxiv(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^arxiv:", "", value)
    value = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", value)
    value = value.removesuffix(".pdf")
    return value


def note_metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = ""
    doi = ""
    arxiv = ""
    year = ""
    for line in text.splitlines():
        if not title and line.startswith("# "):
            title = line[2:].strip()
        m = re.match(r"^-\s*DOI:\s*(.*)$", line, re.I)
        if m and not doi:
            doi = normalize_doi(m.group(1))
        m = re.match(r"^-\s*arXiv(?: ID)?:\s*(.*)$", line, re.I)
        if m and not arxiv:
            arxiv = normalize_arxiv(m.group(1))
        m = re.match(r"^-\s*Year:\s*(\d{4})", line, re.I)
        if m and not year:
            year = m.group(1)
    if not arxiv:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)", text, re.I)
        if m:
            arxiv = normalize_arxiv(m.group(1))
    rel = path.relative_to(PAPERS)
    parts = rel.parts
    venue_dir = parts[1] if len(parts) >= 3 else ""
    return {
        "path": str(path),
        "title": title,
        "title_norm": norm(title),
        "doi": doi,
        "arxiv": arxiv,
        "year": year,
        "venue_dir": venue_dir,
        "filename": path.name,
        "content": text,
    }


def venue_slug(venue: str, peer_reviewed: str) -> str:
    v = (venue or "").strip()
    low = v.lower()
    rules = [
        ("usenix", "usenix_security"),
        ("symposium on security and privacy", "ieee_sp"),
        ("ieee s&p", "ieee_sp"),
        ("oakland", "ieee_sp"),
        ("computer and communications security", "ccs"),
        ("acm ccs", "ccs"),
        ("network and distributed system security", "ndss"),
        ("ndss", "ndss"),
        ("findings of acl", "acl"),
        ("annual meeting of the association for computational linguistics", "acl"),
        ("acl", "acl"),
        ("empirical methods in natural language processing", "emnlp"),
        ("emnlp", "emnlp"),
        ("north american chapter", "naacl"),
        ("naacl", "naacl"),
        ("international conference on learning representations", "iclr"),
        ("iclr", "iclr"),
        ("international conference on machine learning", "icml"),
        ("icml", "icml"),
        ("neural information processing systems", "neurips"),
        ("neurips", "neurips"),
        ("aaai", "aaai"),
        ("ijcai", "ijcai"),
        ("international joint conference on artificial intelligence", "ijcai"),
        ("international joint conference on neural", "ijcnn"),
        ("acm turing celebration", "acm_turing_celebration"),
        ("science china information sciences", "science_china_information_sciences"),
        ("transactions on", "journal"),
    ]
    for needle, folder in rules:
        if needle in low:
            return folder
    if not v or peer_reviewed != "yes" or low == "arxiv":
        return "arxiv"
    return slug(v, 60)


def generated_note(row: dict[str, str]) -> str:
    title = row["title"].strip()
    lines = [
        f"# {title}",
        "",
        "> **Corpus status:** Final signed 201 work MAS security corpus.",
        "",
        "## Citation metadata",
        "",
        f"- Year: {row.get('year','')}",
        f"- Venue: {row.get('venue','') or 'arXiv / preprint'}",
        f"- DOI: {row.get('doi','') or 'N/A'}",
        f"- arXiv: {row.get('arxiv_id','') or 'N/A'}",
        f"- Primary URL: {row.get('primary_url','') or 'N/A'}",
        "",
        "## Corpus classification",
        "",
        f"- Evidence set: `{row.get('evidence_set','')}`",
        f"- Dominant contribution: `{row.get('dominant_contribution','')}`",
        f"- Interaction interfaces: `{row.get('interaction_interfaces','') or 'unspecified'}`",
        f"- Risk or property: `{row.get('risk_or_property','') or 'unspecified'}`",
        f"- Interaction dependence: `{row.get('interaction_dependence','') or 'unspecified'}`",
        "",
        "This note was generated from the final signed corpus row because no prior full paper note matched the canonical record. It should be expanded only from the paper source.",
        "",
    ]
    return "\n".join(lines)


def build_active_rows() -> list[dict[str, str]]:
    set1 = read_csv(CORPUS / "set1_core.csv")
    set2 = read_csv(CORPUS / "set2_emerging.csv")
    if len(set1) != EXPECTED_SET1 or len(set2) != EXPECTED_SET2:
        raise SystemExit(f"Refusing cleanup: expected 96/105, got {len(set1)}/{len(set2)}")
    rows = set1 + set2
    if len(rows) != EXPECTED_TOTAL:
        raise SystemExit("Refusing cleanup: active corpus is not 201")
    keys = [r["work_key"] for r in rows]
    if len(keys) != len(set(keys)):
        raise SystemExit("Refusing cleanup: duplicate work_key in active corpus")
    if any(r.get("strict_scope_pass") != "yes" for r in rows):
        raise SystemExit("Refusing cleanup: non scope passing row in active corpus")
    counts = Counter(r.get("dominant_contribution", "") for r in rows)
    if dict(counts) != EXPECTED_CONTRIBUTIONS:
        raise SystemExit(f"Refusing cleanup: contribution counts changed: {dict(counts)}")
    return rows


def preserve_existing_notes() -> list[dict[str, str]]:
    notes = []
    if not PAPERS.exists():
        return notes
    for p in PAPERS.rglob("*.md"):
        if p.name.lower() == "readme.md":
            continue
        notes.append(note_metadata(p))
    return notes


def choose_note(row: dict[str, str], notes: list[dict[str, str]], used: set[str]) -> dict[str, str] | None:
    doi = normalize_doi(row.get("doi", ""))
    arxiv = normalize_arxiv(row.get("arxiv_id", ""))
    title_n = norm(row.get("title", ""))
    year = row.get("year", "")

    def available(n: dict[str, str]) -> bool:
        return n["path"] not in used

    if doi:
        for n in notes:
            if available(n) and n["doi"] and n["doi"] == doi:
                return n
    if arxiv:
        for n in notes:
            if available(n) and n["arxiv"] and n["arxiv"].split("v")[0] == arxiv.split("v")[0]:
                return n
    for n in notes:
        if available(n) and n["title_norm"] and n["title_norm"] == title_n:
            return n

    best = None
    best_score = 0.0
    for n in notes:
        if not available(n) or not n["title_norm"]:
            continue
        if year and n["year"] and year != n["year"]:
            continue
        score = SequenceMatcher(None, title_n, n["title_norm"]).ratio()
        if score > best_score:
            best = n
            best_score = score
    return best if best_score >= 0.94 else None


def write_all_201(rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0].keys())
    with (CORPUS / "all_201.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def rebuild_papers(rows: list[dict[str, str]], old_notes: list[dict[str, str]]) -> tuple[int, int, Counter]:
    used: set[str] = set()
    selected = []
    if PAPERS.exists():
        shutil.rmtree(PAPERS)
    PAPERS.mkdir(parents=True)

    venue_counts: Counter[str] = Counter()
    matched = 0
    generated = 0
    occupied: set[str] = set()

    for row in sorted(rows, key=lambda r: (r.get("dominant_contribution", ""), r.get("venue", ""), r.get("year", ""), r.get("title", ""))):
        contribution = row["dominant_contribution"]
        category = CATEGORY_DIR[contribution]
        prior = choose_note(row, old_notes, used)
        if prior:
            used.add(prior["path"])
            venue = prior["venue_dir"] or venue_slug(row.get("venue", ""), row.get("peer_reviewed", ""))
            filename = prior["filename"]
            content = prior["content"]
            matched += 1
        else:
            venue = venue_slug(row.get("venue", ""), row.get("peer_reviewed", ""))
            filename = f"{row.get('year','unknown')}_{slug(row.get('title',''))}.md"
            content = generated_note(row)
            generated += 1

        venue_counts[venue] += 1
        target_dir = PAPERS / category / venue
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / filename
        key = str(target.relative_to(PAPERS))
        if key in occupied or target.exists():
            stem = target.stem
            suffix = slug(row.get("work_key", "paper"), 32)
            target = target.with_name(f"{stem}_{suffix}.md")
            key = str(target.relative_to(PAPERS))
        occupied.add(key)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
        selected.append((row, target))

    by_category: dict[str, list[tuple[dict[str, str], Path]]] = defaultdict(list)
    for row, path in selected:
        by_category[row["dominant_contribution"]].append((row, path))

    for contribution, dirname in CATEGORY_DIR.items():
        items = by_category[contribution]
        lines = [
            f"# {contribution.title()} papers",
            "",
            f"Final corpus count: **{len(items)}**.",
            "",
            "Papers are grouped by publication venue. `arxiv/` contains works whose frozen corpus record is a preprint or has no peer reviewed venue in the snapshot.",
            "",
        ]
        grouped: dict[str, list[tuple[dict[str, str], Path]]] = defaultdict(list)
        for item in items:
            grouped[item[1].parent.name].append(item)
        for venue in sorted(grouped):
            lines += [f"## {venue}", ""]
            for row, path in sorted(grouped[venue], key=lambda x: (x[0].get("year", ""), x[0]["title"])):
                rel = path.relative_to(PAPERS / dirname)
                lines.append(f"* [{row['title']}]({rel.as_posix()})  `{row['evidence_set']}`")
            lines.append("")
        (PAPERS / dirname).mkdir(parents=True, exist_ok=True)
        (PAPERS / dirname / "README.md").write_text("\n".join(lines), encoding="utf-8")

    top = [
        "# Final 201 paper corpus",
        "",
        "This directory contains exactly the **201 works** in the signed manuscript corpus: **96 Set 1** and **105 Set 2**.",
        "",
        "Each paper appears exactly once and is organized first by dominant contribution, then by publication venue, preserving the prior venue folder classification whenever an existing reviewed note was available.",
        "",
        "| Contribution | Count | Directory |",
        "| --- | ---: | --- |",
    ]
    for contribution in ["attack", "defense", "evaluation", "general", "survey"]:
        top.append(f"| {contribution} | {EXPECTED_CONTRIBUTIONS[contribution]} | [`{CATEGORY_DIR[contribution]}/`]({CATEGORY_DIR[contribution]}/) |")
    top += [
        "",
        f"Existing detailed notes preserved: **{matched}**.",
        f"Rows without a matching prior note received a metadata note: **{generated}**.",
        "",
        "The authoritative row level data are `corpus/set1_core.csv`, `corpus/set2_emerging.csv`, and their union `corpus/all_201.csv`.",
        "",
    ]
    (PAPERS / "README.md").write_text("\n".join(top), encoding="utf-8")
    return matched, generated, venue_counts


def clean_stale_artifacts() -> None:
    stale_paths = [
        CORPUS / "set3_context.csv",
        CORPUS / "screened_out.csv",
        CORPUS / "review_ledger.csv",
        CORPUS / "routes.csv",
        CORPUS / "manual_review_queue_2026-08-18.csv",
        CORPUS / "author_priority_review.csv",
        CORPUS / "identifier_aliases.csv",
        CORPUS / "identifier_alias_overrides.csv",
        CORPUS / "adjudication",
        CORPUS / "sets",
        ROOT / "GENERAL_CONTRIBUTION_ADJUDICATION.md",
        ROOT / "SURVEY_SCOPE_ADJUDICATION.md",
        ROOT / "EXPERT_REVIEW.md",
    ]
    for path in stale_paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()

    stale_scripts = [
        "apply_general_adjudication.py",
        "apply_manual_corpus_classification_2026_08_21.py",
        "apply_manual_decision_signoff_2026_08_21.py",
        "build_three_set_corpus.py",
        "finalize_three_set_source_review.py",
        "patch_source_scope_policy.py",
        "rebuild_membership_from_ledger.py",
        "rebuild_three_set_from_evidence.py",
        "rebuild_three_set_from_evidence_v2.py",
        "reconcile_secondary_review_2026_08_21.py",
        "validate_authoritative_corpus.py",
        "validate_three_set_corpus.py",
    ]
    for name in stale_scripts:
        p = ROOT / "scripts" / name
        if p.exists():
            p.unlink()


def write_docs(rows: list[dict[str, str]], matched: int, generated: int, venue_counts: Counter) -> None:
    root_readme = """# Multi Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Authoritative manuscript corpus

There is one active manuscript corpus: **201 works**.

| Set | Count | Meaning |
| --- | ---: | --- |
| Set 1 | 96 | In scope mature MAS security work |
| Set 2 | 105 | In scope emerging MAS security work |
| **Total** | **201** | **Authoritative MAS security corpus** |

No older corpus denominator is active in this repository. Context only, screened out, migration, and superseded adjudication tables have been removed from the active tree so collaborators cannot mistake them for manuscript evidence.

The authoritative files are:

* `corpus/set1_core.csv`
* `corpus/set2_emerging.csv`
* `corpus/all_201.csv`
* `papers/`, containing exactly the same 201 works organized by contribution and publication venue

## Paper organization

`papers/` is organized as:

```text
papers/
  attacks/<venue>/
  defenses/<venue>/
  evaluations/<venue>/
  general/<venue>/
  surveys/<venue>/
```

The signed dominant contribution totals are 42 attacks, 94 defenses, 44 evaluations, 11 general works, and 10 surveys.

## Validation

Run:

```bash
scripts/validate_all.sh
```

The validator requires the exact 96 plus 105 partition, the exact 201 union, the signed contribution counts, and exactly 201 paper notes.
"""
    (ROOT / "README.md").write_text(root_readme, encoding="utf-8")

    corpus_readme = """# Authoritative 201 work corpus

Only Set 1 and Set 2 are active manuscript evidence sets.

| File | Count | Meaning |
| --- | ---: | --- |
| `set1_core.csv` | 96 | Mature in scope MAS security work |
| `set2_emerging.csv` | 105 | Emerging in scope MAS security work |
| `all_201.csv` | 201 | Exact union used by the manuscript |

Set 1 and Set 2 share the same scope gate. Membership requires an LLM multi agent system, a concrete security property, and a material inter agent interaction path. Set 1 additionally satisfies the frozen maturity rule: peer reviewed or at least 10 frozen citations. Set 2 contains the remaining in scope emerging work.

Superseded corpus partitions and review migration tables are intentionally absent from the active repository.
"""
    (CORPUS / "README.md").write_text(corpus_readme, encoding="utf-8")

    policy = """# Corpus policy

## Scope gate

A work enters the active corpus only if all of the following hold:

1. It studies at least two separately addressable LLM backed agents or principals.
2. A material inter agent relation or interaction path is present.
3. It studies a concrete security property, attack, defense, guarantee, adversary, or security evaluation.
4. Source evidence is sufficient to support the membership decision.

Interaction dependence strength is recorded as evidence characterization and is not itself a membership gate.

## Set 1 and Set 2

Both sets are in scope. Set 1 is the mature subset and uses the frozen rule `peer_reviewed == yes OR frozen_citation_count >= 10`. Set 2 contains the remaining in scope emerging work.

The signed manuscript corpus is frozen at 96 Set 1 works plus 105 Set 2 works, for 201 total. Older denominators are not active corpus views.
"""
    (ROOT / "CORPUS_SET_POLICY.md").write_text(policy, encoding="utf-8")

    snapshot = """# Frozen corpus snapshot

Literature cutoff: `2026-07-01`

Final named classification signoff: `2026-08-21`

| Partition | Count |
| --- | ---: |
| Set 1 | 96 |
| Set 2 | 105 |
| **Authoritative corpus** | **201** |

This 201 work union is the sole manuscript facing corpus. Superseded Set 3, screened out, review universe, and intermediate 226, 227, or 228 work states are not active corpus definitions and are intentionally not retained as current repository artifacts.
"""
    (ROOT / "FROZEN_SNAPSHOT.md").write_text(snapshot, encoding="utf-8")

    manifest = {
        "literature_cutoff": "2026-07-01",
        "final_signoff_date": "2026-08-21",
        "counts": {"set1_core": EXPECTED_SET1, "set2_emerging": EXPECTED_SET2, "total_corpus": EXPECTED_TOTAL},
        "contributions": EXPECTED_CONTRIBUTIONS,
        "paper_notes": EXPECTED_TOTAL,
        "preserved_existing_notes": matched,
        "generated_metadata_notes": generated,
        "venue_counts": dict(sorted(venue_counts.items())),
        "authoritative_files": ["set1_core.csv", "set2_emerging.csv", "all_201.csv"],
    }
    (CORPUS / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_validator() -> None:
    validator = r'''#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "corpus"
P = R / "papers"

EXPECTED = {"set1_core": 96, "set2_emerging": 105, "total": 201}
CONTRIB = {"attack": 42, "defense": 94, "evaluation": 44, "general": 11, "survey": 10}
CAT = {"attack": "attacks", "defense": "defenses", "evaluation": "evaluations", "general": "general", "survey": "surveys"}

def rows(name):
    with (C / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

s1 = rows("set1_core.csv")
s2 = rows("set2_emerging.csv")
all_rows = rows("all_201.csv")
if (len(s1), len(s2), len(all_rows)) != (96, 105, 201):
    raise SystemExit("authoritative 201 counts changed")
keys = [r["work_key"] for r in all_rows]
if len(keys) != len(set(keys)) or set(keys) != {r["work_key"] for r in s1 + s2}:
    raise SystemExit("all_201 is not the exact Set 1 plus Set 2 union")
if any(r.get("strict_scope_pass") != "yes" for r in all_rows):
    raise SystemExit("out of scope row in active corpus")
if any(r.get("maturity_rule_pass") != "yes" for r in s1):
    raise SystemExit("invalid Set 1 maturity")
if any(r.get("maturity_rule_pass") != "no" for r in s2):
    raise SystemExit("invalid Set 2 maturity")
if dict(Counter(r["dominant_contribution"] for r in all_rows)) != CONTRIB:
    raise SystemExit("signed contribution counts changed")

stale = [
    C / "set3_context.csv", C / "screened_out.csv", C / "review_ledger.csv", C / "routes.csv",
    C / "manual_review_queue_2026-08-18.csv", C / "adjudication", C / "sets", P / "post_cutoff"
]
if any(p.exists() for p in stale):
    raise SystemExit("superseded corpus artifact is present")

notes = [p for p in P.rglob("*.md") if p.name.lower() != "readme.md"]
if len(notes) != 201:
    raise SystemExit(f"expected 201 paper notes, found {len(notes)}")
for p in notes:
    rel = p.relative_to(P)
    if len(rel.parts) < 3:
        raise SystemExit(f"paper is not classified by contribution and venue: {rel}")

for contribution, dirname in CAT.items():
    n = len([p for p in (P / dirname).rglob("*.md") if p.name.lower() != "readme.md"])
    if n != CONTRIB[contribution]:
        raise SystemExit(f"paper directory count mismatch for {contribution}: {n}")

m = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
if m["counts"] != EXPECTED or m["paper_notes"] != 201:
    raise SystemExit("manifest mismatch")
print("Final corpus valid: Set1=96 Set2=105 total=201; paper notes=201; superseded corpus artifacts absent")
'''
    p = ROOT / "scripts" / "validate_corpus.py"
    p.write_text(validator, encoding="utf-8")
    p.chmod(0o755)
    (ROOT / "scripts" / "validate_all.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\npython3 scripts/validate_corpus.py\n", encoding="utf-8")
    (ROOT / "scripts" / "validate_all.sh").chmod(0o755)


def main() -> None:
    rows = build_active_rows()
    old_notes = preserve_existing_notes()
    write_all_201(rows)
    matched, generated, venue_counts = rebuild_papers(rows, old_notes)
    clean_stale_artifacts()
    write_docs(rows, matched, generated, venue_counts)
    write_validator()

    # Remove the one shot machinery from the final tree.
    workflow = ROOT / ".github" / "workflows" / "sync-final-201.yml"
    if workflow.exists():
        workflow.unlink()
    this_file = Path(__file__)
    if this_file.exists():
        this_file.unlink()

    print(f"Prepared final 201 corpus. Preserved notes={matched}, generated notes={generated}")


if __name__ == "__main__":
    main()
