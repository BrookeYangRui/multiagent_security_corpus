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


def source_url(row: dict[str, str]) -> str:
    doi = (row.get("doi") or "").strip()
    arxiv = (row.get("arxiv_id") or "").strip()
    primary = (row.get("primary_url") or "").strip()

    if doi and doi.upper() != "N/A":
        return f"https://doi.org/{doi}"
    if arxiv and arxiv.upper() != "N/A":
        return f"https://arxiv.org/abs/{arxiv}"
    if primary and primary.upper() != "N/A":
        return primary
    raise SystemExit(f"No stable source locator for {row.get('title')}")


def esc(text: str) -> str:
    return text.replace("[", "\\[").replace("]", "\\]")


def main() -> None:
    rows = read_rows("set1_core") + read_rows("set2_emerging")
    if len(rows) != 189:
        raise SystemExit(f"expected 189 active works, found {len(rows)}")

    lines = [
        "# Source Links for the 189-Work MAS-Security Corpus",
        "",
        "This page provides a stable source link for each of the 189 works in the corpus.",
        "",
    ]

    for i, row in enumerate(rows, start=1):
        title = esc((row.get("title") or "").strip())
        lines.append(f"{i}. [{title}]({source_url(row)})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(rows)} linked works")


if __name__ == "__main__":
    main()
