#!/usr/bin/env python3
"""Rebuild papers/ from the signed 201-work manuscript corpus.

The authoritative membership is corpus/set1_core.csv plus corpus/set2_emerging.csv.
Existing detailed paper notes are preserved when they match a retained work, but
all placement and the status banner are regenerated from the signed corpus row.
Anything outside the final 201 is removed because papers/ is rebuilt from scratch.
"""

from __future__ import annotations

import csv
import re
import shutil
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
PAPERS = ROOT / "papers"

EXPECTED = {"set1_core": 96, "set2_emerging": 105}
EXPECTED_CONTRIB = {
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


def compact(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (text or "").lower())


def slug(text: str, limit: int = 90) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_")
    return (value[:limit].rstrip("_") or "paper")


def norm_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return value


def norm_arxiv(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^arxiv:\s*", "", value)
    value = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", value)
    value = value.removesuffix(".pdf")
    value = re.sub(r"v\d+$", "", value)
    return value


def note_info(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    title = ""
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    doi = ""
    arxiv = ""
    patterns = [
        r"(?:^|\n)[-*]?\s*DOI\s*:\s*([^\s|]+)",
        r"https?://doi\.org/([^\s)>]+)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            doi = norm_doi(m.group(1).rstrip(".,"))
            break
    patterns = [
        r"(?:^|\n)[-*]?\s*arXiv(?:\s+ID)?\s*:\s*([^\s|]+)",
        r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            arxiv = norm_arxiv(m.group(1).rstrip(".,"))
            break

    return {
        "path": str(path),
        "title": title,
        "title_norm": compact(title),
        "doi": doi,
        "arxiv": arxiv,
        "content": text,
        "filename": path.name,
    }


def venue_dir(row: dict[str, str]) -> str:
    venue = (row.get("venue") or "").strip()
    low = venue.lower()

    if not venue or "arxiv" in low or low in {"preprint", "preprints"}:
        return "arxiv"
    if "ssrn" in low:
        return "ssrn"
    if "zenodo" in low:
        return "zenodo"

    # NLP venues. Check Findings and industry tracks before the main venue.
    if "findings" in low and "emnlp" in low:
        return "findings_emnlp"
    if "findings" in low and "eacl" in low:
        return "findings_eacl"
    if "findings" in low and "acl" in low:
        return "findings_acl"
    if "industry" in low and "eacl" in low:
        return "eacl_industry"
    if "industry" in low and "acl" in low:
        return "acl_industry"
    if "naacl" in low or "north american chapter" in low:
        return "naacl"
    if "ijcnlp" in low or "aacl" in low:
        return "ijcnlp_aacl"
    if "emnlp" in low or "empirical methods in natural language processing" in low:
        return "emnlp"
    if "eacl" in low or "european chapter of the association for computational linguistics" in low:
        return "eacl"
    if low == "acl" or "annual meeting of the association for computational linguistics" in low:
        return "acl"

    # Major ML and agent venues.
    if "international conference on machine learning" in low or re.search(r"\bicml\b", low):
        return "icml"
    if "international conference on learning representations" in low or re.search(r"\biclr\b", low):
        return "iclr"
    if "neurips" in low or "neural information processing systems" in low:
        return "neurips_workshop" if "workshop" in low else "neurips"
    if "aaai" in low:
        return "aaai_symposium" if "symposium" in low else "aaai"
    if "aamas" in low or "autonomous agents and multiagent systems" in low:
        return "aamas_workshop" if "workshop" in low else "aamas"
    if re.search(r"\bcolm\b", low) or "conference on language modeling" in low:
        return "colm"
    if re.search(r"\bkdd\b", low) or "knowledge discovery and data mining" in low:
        return "kdd"
    if "web conference" in low or re.search(r"\bwww\b", low):
        return "www"
    if "cvpr" in low or "computer vision and pattern recognition" in low:
        return "cvpr"

    # Security venues.
    if "usenix" in low and "security" in low:
        return "usenix_security"
    if "symposium on security and privacy" in low or "ieee s&p" in low:
        return "ieee_security_privacy"
    if "asia" in low and "ccs" in low:
        return "acm_asiaccs"
    if "computer and communications security" in low or re.search(r"\bccs\b", low):
        return "ccs"
    if "network and distributed system security" in low or re.search(r"\bndss\b", low):
        return "ndss"
    if "esorics" in low:
        return "esorics_workshops" if "workshop" in low else "esorics"
    if "llmsec" in low:
        return "llmsec_workshop"

    # Other recurring conference folders already used by the corpus.
    known = [
        ("international joint conference on neural network", "ijcnn"),
        ("international joint conference on neural networks", "ijcnn"),
        ("international conference on agents and artificial intelligence", "icaart"),
        ("international conference on computational intelligence and applications", "iccia"),
        ("international conference on acoustics, speech", "icassp"),
        ("international conference on machine learning and applications", "icmla"),
        ("international conference on information reuse and integration", "ieee_iri"),
        ("international symposium on parallel and distributed processing", "ieee_ispa"),
        ("trustcom", "trustcom"),
        ("bigdata congress", "bigdata_congress"),
        ("software engineering conference", "apsec"),
        ("turing celebration conference", "acm_turing_celebration"),
        ("international conference on computer and applications", "icca"),
        ("international conference on enterprise information systems", "iceis"),
        ("international conference on evaluation of novel approaches to software engineering", "enase"),
    ]
    for needle, folder in known:
        if needle in low:
            return folder

    # Journal and proceedings names retain a readable prefix.
    journal_markers = (
        "journal", "transactions", "scientific reports", "science china",
        "information processing", "ieee access", "npj", "ai open",
    )
    if any(marker in low for marker in journal_markers):
        return "journals_" + slug(venue, 60)

    return slug(venue, 70)


def load_existing_notes() -> list[dict[str, str]]:
    if not PAPERS.exists():
        return []
    notes = []
    for path in PAPERS.rglob("*.md"):
        if path.name.lower() == "readme.md":
            continue
        notes.append(note_info(path))
    return notes


def choose_existing(row: dict[str, str], notes: list[dict[str, str]], used: set[str]) -> dict[str, str] | None:
    title_norm = compact(row.get("title", ""))
    doi = norm_doi(row.get("doi", ""))
    arxiv = norm_arxiv(row.get("arxiv_id", ""))

    available = [n for n in notes if n["path"] not in used]

    exact_title = [n for n in available if n["title_norm"] and n["title_norm"] == title_norm]
    if len(exact_title) == 1:
        return exact_title[0]

    if doi:
        exact_doi = [n for n in available if n["doi"] and n["doi"] == doi]
        if len(exact_doi) == 1:
            return exact_doi[0]

    if arxiv:
        exact_arxiv = [n for n in available if n["arxiv"] and n["arxiv"] == arxiv]
        if len(exact_arxiv) == 1:
            return exact_arxiv[0]

    best = None
    best_score = 0.0
    runner_up = 0.0
    for n in available:
        if not n["title_norm"]:
            continue
        score = SequenceMatcher(None, title_norm, n["title_norm"]).ratio()
        if score > best_score:
            runner_up = best_score
            best_score = score
            best = n
        elif score > runner_up:
            runner_up = score
    if best is not None and best_score >= 0.965 and best_score - runner_up >= 0.03:
        return best
    return None


def status_banner(row: dict[str, str]) -> str:
    return (
        "<!-- FINAL_CORPUS_STATUS_START -->\n"
        "> **Final signed corpus status:** "
        f"`{row['evidence_set']}` · `{row['dominant_contribution']}` · "
        f"venue `{row.get('venue') or 'arXiv / preprint'}` · signoff `2026-08-21`.\n"
        "> This banner is authoritative if older review prose below records an earlier classification.\n"
        "<!-- FINAL_CORPUS_STATUS_END -->"
    )


def stamp_existing(text: str, row: dict[str, str]) -> str:
    banner = status_banner(row)
    text = re.sub(
        r"\n?<!-- FINAL_CORPUS_STATUS_START -->.*?<!-- FINAL_CORPUS_STATUS_END -->\n?",
        "\n",
        text,
        flags=re.S,
    ).strip()
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0].rstrip() + "\n\n" + banner + "\n\n" + "\n".join(lines[1:]).lstrip() + "\n"
    return f"# {row['title']}\n\n{banner}\n\n{text}\n"


def generated_note(row: dict[str, str]) -> str:
    fields = [
        f"# {row['title']}",
        "",
        status_banner(row),
        "",
        "## Citation metadata",
        "",
        f"* Year: {row.get('year') or 'N/A'}",
        f"* Venue: {row.get('venue') or 'arXiv / preprint'}",
        f"* DOI: {row.get('doi') or 'N/A'}",
        f"* arXiv: {row.get('arxiv_id') or 'N/A'}",
        f"* Primary URL: {row.get('primary_url') or 'N/A'}",
        "",
        "## Final corpus classification",
        "",
        f"* Work key: `{row['work_key']}`",
        f"* Evidence set: `{row['evidence_set']}`",
        f"* Dominant contribution: `{row['dominant_contribution']}`",
        f"* Interaction interfaces: `{row.get('interaction_interfaces') or 'unspecified'}`",
        f"* Risk or property: `{row.get('risk_or_property') or 'unspecified'}`",
        f"* Interaction dependence: `{row.get('interaction_dependence') or 'unspecified'}`",
        "",
        "This metadata note was generated from the final signed corpus row because no unambiguous prior paper note matched the retained work.",
        "",
    ]
    return "\n".join(fields)


def safe_filename(row: dict[str, str], existing: dict[str, str] | None) -> str:
    if existing is not None:
        name = existing["filename"]
        if name.lower().endswith(".md"):
            return name
    year = row.get("year") or "unknown"
    return f"{year}_{slug(row['title'], 72)}.md"


def main() -> None:
    set1 = read_csv(CORPUS / "set1_core.csv")
    set2 = read_csv(CORPUS / "set2_emerging.csv")
    if len(set1) != EXPECTED["set1_core"] or len(set2) != EXPECTED["set2_emerging"]:
        raise SystemExit(f"Refusing rebuild: expected 96/105, got {len(set1)}/{len(set2)}")

    rows = set1 + set2
    if len(rows) != 201 or len({r["work_key"] for r in rows}) != 201:
        raise SystemExit("Refusing rebuild: active corpus is not 201 unique works")
    if any(r.get("strict_scope_pass") != "yes" for r in rows):
        raise SystemExit("Refusing rebuild: active corpus contains a scope failure")
    contrib = Counter(r.get("dominant_contribution", "") for r in rows)
    if dict(contrib) != EXPECTED_CONTRIB:
        raise SystemExit(f"Refusing rebuild: contribution totals changed: {dict(contrib)}")

    old_notes = load_existing_notes()
    used: set[str] = set()
    prepared: list[tuple[dict[str, str], str, str, str]] = []
    matched = 0
    generated = 0

    occupied: set[str] = set()
    for row in sorted(rows, key=lambda r: (r["dominant_contribution"], venue_dir(r), r.get("year", ""), r["title"])):
        existing = choose_existing(row, old_notes, used)
        if existing is not None:
            used.add(existing["path"])
            content = stamp_existing(existing["content"], row)
            matched += 1
        else:
            content = generated_note(row)
            generated += 1

        category = CATEGORY_DIR[row["dominant_contribution"]]
        venue = venue_dir(row)
        filename = safe_filename(row, existing)
        rel = f"{category}/{venue}/{filename}"
        if rel in occupied:
            stem = Path(filename).stem
            filename = f"{stem}_{slug(row['work_key'], 28)}.md"
            rel = f"{category}/{venue}/{filename}"
        if rel in occupied:
            raise SystemExit(f"Unresolved paper path collision: {rel}")
        occupied.add(rel)
        prepared.append((row, rel, content, venue))

    # Rebuild from scratch so no stale, post-cutoff, Set 3, or screened-out note survives.
    if PAPERS.exists():
        shutil.rmtree(PAPERS)
    PAPERS.mkdir(parents=True)

    index_rows: list[dict[str, str]] = []
    by_category: dict[str, list[tuple[dict[str, str], str, str]]] = defaultdict(list)
    for row, rel, content, venue in prepared:
        target = PAPERS / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
        index_rows.append({
            "work_key": row["work_key"],
            "title": row["title"],
            "evidence_set": row["evidence_set"],
            "dominant_contribution": row["dominant_contribution"],
            "venue": row.get("venue", ""),
            "venue_folder": venue,
            "paper_path": f"papers/{rel}",
        })
        by_category[row["dominant_contribution"]].append((row, rel, venue))

    with (PAPERS / "index.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "work_key", "title", "evidence_set", "dominant_contribution",
            "venue", "venue_folder", "paper_path",
        ])
        writer.writeheader()
        writer.writerows(sorted(index_rows, key=lambda r: (r["dominant_contribution"], r["venue_folder"], r["title"])))

    for contribution, dirname in CATEGORY_DIR.items():
        items = by_category[contribution]
        grouped: dict[str, list[tuple[dict[str, str], str]]] = defaultdict(list)
        for row, rel, venue in items:
            grouped[venue].append((row, rel))
        lines = [
            f"# {contribution.title()} papers",
            "",
            f"Final signed corpus count: **{len(items)}**.",
            "",
            "Each retained work is placed under its publication venue folder. The status banner inside every note records the final signed set and contribution.",
            "",
        ]
        for venue in sorted(grouped):
            lines.extend([f"## {venue}", ""])
            for row, rel in sorted(grouped[venue], key=lambda x: (x[0].get("year", ""), x[0]["title"])):
                local = Path(rel).relative_to(dirname).as_posix()
                lines.append(f"* [{row['title']}]({local})  `{row['evidence_set']}`")
            lines.append("")
        (PAPERS / dirname / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    root_lines = [
        "# Final 201 paper corpus",
        "",
        "This directory contains exactly the **201 works** in the signed manuscript corpus: **96 Set 1** and **105 Set 2**.",
        "",
        "Papers are organized first by dominant contribution and then by publication venue. The tree is generated only from `corpus/set1_core.csv` and `corpus/set2_emerging.csv`; older corpus states do not populate this directory.",
        "",
        "| Contribution | Count | Directory |",
        "| --- | ---: | --- |",
    ]
    for contribution in ("attack", "defense", "evaluation", "general", "survey"):
        dirname = CATEGORY_DIR[contribution]
        root_lines.append(f"| {contribution} | {EXPECTED_CONTRIB[contribution]} | [`{dirname}/`]({dirname}/) |")
    root_lines.extend([
        "",
        f"Existing detailed notes preserved and re-stamped: **{matched}**.",
        f"Metadata notes generated for unmatched retained works: **{generated}**.",
        "",
        "[`index.csv`](index.csv) is the exact one-to-one mapping from all 201 signed corpus work keys to their paper paths.",
        "",
    ])
    (PAPERS / "README.md").write_text("\n".join(root_lines), encoding="utf-8")

    print(
        f"Rebuilt papers/: total=201 matched_existing={matched} generated={generated} "
        f"categories={dict(contrib)}"
    )


if __name__ == "__main__":
    main()
