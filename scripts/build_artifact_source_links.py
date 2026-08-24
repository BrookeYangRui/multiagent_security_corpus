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


def source_url(row: dict[str, str]) -> tuple[str, str]:
    doi = (row.get("doi") or "").strip()
    arxiv = (row.get("arxiv_id") or "").strip()
    primary = (row.get("primary_url") or "").strip()

    # Prefer durable scholarly identifiers over aggregator URLs.
    if doi and doi.upper() != "N/A":
        return f"https://doi.org/{doi}", "DOI"
    if arxiv and arxiv.upper() != "N/A":
        return f"https://arxiv.org/abs/{arxiv}", "arXiv"
    if primary and primary.upper() != "N/A":
        return primary, "Primary source"
    raise SystemExit(f"No stable source locator for {row.get('work_key')}: {row.get('title')}")


def esc(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def render_section(label: str, rows: list[dict[str, str]], start: int) -> tuple[list[str], int]:
    lines = [f"## {label} ({len(rows)})", ""]
    n = start
    for row in rows:
        url, kind = source_url(row)
        title = esc((row.get("title") or "").strip())
        venue = (row.get("venue") or "").strip() or "venue not recorded"
        year = (row.get("year") or "").strip() or (row.get("publication_date") or "")[:4]
        contribution = (row.get("dominant_contribution") or "").strip() or "unspecified"
        work_key = (row.get("work_key") or "").strip()
        lines.append(
            f"{n}. [{title}]({url}) — **{contribution}** · {venue} · {year} · {kind} · `{work_key}`"
        )
        n += 1
    lines.append("")
    return lines, n


def main() -> None:
    set1 = read_rows("set1_core")
    set2 = read_rows("set2_emerging")
    all_rows = set1 + set2
    if len(all_rows) != 189:
        raise SystemExit(f"expected 189 active works, found {len(all_rows)}")
    keys = [r.get("work_key", "") for r in all_rows]
    if len(keys) != len(set(keys)):
        raise SystemExit("duplicate work_key in active corpus")

    lines = [
        "# Source Links for the 189-Work MAS-Security Corpus",
        "",
        "This directory is the source-access layer for the USENIX artifact. It lists every active corpus work with at least one stable, clickable locator. Third-party PDFs are not redistributed here; the links point to DOI, arXiv, or the recorded primary source.",
        "",
        "Active corpus: **92 Set 1 + 97 Set 2 = 189 works**.",
        "",
        "Source-link priority is **DOI → arXiv → recorded primary URL** so that durable scholarly identifiers are preferred over aggregator pages. Corpus membership and taxonomy remain authoritative in `../corpus/set1_core.csv` and `../corpus/set2_emerging.csv`.",
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
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(all_rows)} linked works")


if __name__ == "__main__":
    main()
