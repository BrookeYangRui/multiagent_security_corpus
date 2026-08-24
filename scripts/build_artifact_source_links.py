#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
OUT = ROOT / "artifact" / "README.md"

EXPECTED = {"set1_core": 92, "set2_emerging": 97}


def read_rows(name: str) -> list[dict[str, str]]:
    path = CORPUS / f"{name}.csv"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != EXPECTED[name]:
        raise SystemExit(f"{name}: expected {EXPECTED[name]} rows, found {len(rows)}")
    return rows


def source_locator(row: dict[str, str]) -> tuple[str, str]:
    doi = (row.get("doi") or "").strip()
    arxiv = (row.get("arxiv_id") or "").strip()
    primary = (row.get("primary_url") or "").strip()

    if doi and doi.upper() != "N/A":
        return f"https://doi.org/{doi}", f"DOI: {doi}"
    if arxiv and arxiv.upper() != "N/A":
        return f"https://arxiv.org/abs/{arxiv}", f"arXiv: {arxiv}"
    if primary and primary.upper() != "N/A":
        return primary, "Primary source"
    raise SystemExit(f"No stable source locator for {row.get('title')}")


def esc(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def render_section(label: str, rows: list[dict[str, str]], start: int) -> tuple[list[str], int]:
    lines = [f"## {label} ({len(rows)})", ""]
    n = start
    for row in rows:
        url, source = source_locator(row)
        title = esc((row.get("title") or "").strip())
        venue = (row.get("venue") or "").strip() or "Venue not recorded"
        year = (row.get("year") or "").strip() or (row.get("publication_date") or "")[:4] or "Year not recorded"
        lines.append(f"{n}. [{title}]({url}) — {venue} · {year} · {source}")
        n += 1
    lines.append("")
    return lines, n


def main() -> None:
    set1 = read_rows("set1_core")
    set2 = read_rows("set2_emerging")
    rows = set1 + set2
    if len(rows) != 189:
        raise SystemExit(f"expected 189 active works, found {len(rows)}")

    lines = [
        "# Source Links for the 189-Work MAS-Security Corpus",
        "",
        "This page provides a stable source link and basic publication metadata for each active corpus work.",
        "",
        "Active corpus: **92 Set 1 + 97 Set 2 = 189 works**.",
        "",
    ]

    section, next_n = render_section("Set 1: mature MAS-security works", set1, 1)
    lines.extend(section)
    section, next_n = render_section("Set 2: emerging MAS-security works", set2, next_n)
    lines.extend(section)

    if next_n != 190:
        raise SystemExit(f"numbering error: next index is {next_n}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(rows)} linked works")


if __name__ == "__main__":
    main()
