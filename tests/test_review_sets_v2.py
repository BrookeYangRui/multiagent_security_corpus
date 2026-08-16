#!/usr/bin/env python3
"""Regression checks for the persistent three-set review view."""

from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "artifact" / "search" / "v2" / "build_review_sets.py"


def load_module():
    spec = importlib.util.spec_from_file_location("review_sets_v2", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def by_key(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["work_key"]: row for row in rows}


def test_current_outputs(module) -> None:
    here = MODULE_PATH.parent
    queue = read_csv(here / "review_candidate_queue.csv")
    routes = read_csv(here / "review_candidate_routes.csv")
    ledger = read_csv(here / "review_decision_ledger.csv")
    primary = read_csv(here / "review_primary.csv")
    secondary = read_csv(here / "review_secondary.csv")
    excluded = read_csv(here / "review_exclude.csv")
    pending = read_csv(here / "review_pending.csv")
    aliases = read_csv(here / "review_identifier_aliases.csv")
    summary = read_csv(here / "review_set_summary.csv")

    assert len(queue) == len(ledger) == 2217
    assert summary
    assert (len(primary), len(secondary), len(excluded), len(pending)) == (303, 177, 1396, 341)

    sets = [set(by_key(rows)) for rows in (primary, secondary, excluded, pending)]
    for index, left in enumerate(sets):
        for right in sets[index + 1 :]:
            assert not (left & right)
    assert set(by_key(queue)) == set().union(*sets)

    targeted = [row for row in routes if row["route_type"] == "targeted"]
    assert len(targeted) == 318
    assert len({row["route_id"] for row in targeted}) == 318
    assert len({row["work_key"] for row in targeted}) == 317

    magpie = [row for row in targeted if row["arxiv_id"] in {"2506.20737", "2510.15186"}]
    assert len(magpie) == 2
    assert len({row["work_key"] for row in magpie}) == 1

    chain = [row for row in queue if row["arxiv_id"] == "2508.15809"]
    assert len(chain) == 1
    assert chain[0]["doi"] == "10.18653/v1/2025.ijcnlp-long.53"

    identifier_owner: dict[tuple[str, str], str] = {}
    for row in aliases:
        key = (row["identifier_type"], row["identifier"])
        owner = identifier_owner.setdefault(key, row["work_key"])
        assert owner == row["work_key"], (key, owner, row["work_key"])

    canonical = [row for row in queue if "canonical" in row["route_types"].split(";")]
    assert len(canonical) == 142
    assert sum(row["ledger_decision"] == "primary" for row in canonical) == 92
    assert sum(row["ledger_decision"] == "secondary" for row in canonical) == 50
    assert all(row["current_primary_category"] for row in canonical)


def test_ledger_precedence(module) -> None:
    here = MODULE_PATH.parent
    current = read_csv(here / "review_decision_ledger.csv")
    target = next(row for row in current if row["decision"] == "primary")

    with tempfile.TemporaryDirectory(prefix="v2-ledger-test-") as temp_name:
        temp = Path(temp_name)

        manual_rows = [dict(row) for row in current]
        manual = next(row for row in manual_rows if row["work_key"] == target["work_key"])
        manual.update(
            {
                "decision": "secondary",
                "decision_source": "manual:test",
                "decision_strength": "1000",
                "rationale": "Regression test for persistent human adjudication.",
                "reviewer": "Rui Yang",
                "reviewed_at": "2026-08-16",
                "locked": "yes",
                "human_signoff_required": "no",
            }
        )
        manual_ledger = temp / "manual.csv"
        write_csv(manual_ledger, module.LEDGER_FIELDS, manual_rows)
        manual_out = temp / "manual-out"
        module.render(manual_out, manual_ledger)
        rebuilt = by_key(read_csv(manual_out / module.LEDGER.name))[target["work_key"]]
        assert rebuilt["decision"] == "secondary"
        assert rebuilt["decision_source"] == "manual:test"
        assert rebuilt["reviewer"] == "Rui Yang"
        assert rebuilt["locked"] == "yes"

        automatic_rows = [dict(row) for row in current]
        automatic = next(row for row in automatic_rows if row["work_key"] == target["work_key"])
        automatic.update(
            {
                "decision": "secondary",
                "decision_source": "obsolete_automatic_seed",
                "decision_strength": "1",
                "rationale": "This automatic value must be refreshed.",
                "reviewer": "",
                "reviewed_at": "",
                "locked": "no",
            }
        )
        automatic_ledger = temp / "automatic.csv"
        write_csv(automatic_ledger, module.LEDGER_FIELDS, automatic_rows)
        automatic_out = temp / "automatic-out"
        module.render(automatic_out, automatic_ledger)
        refreshed = by_key(read_csv(automatic_out / module.LEDGER.name))[target["work_key"]]
        assert refreshed["decision"] == "primary"
        assert refreshed["decision_source"] != "obsolete_automatic_seed"


def test_strong_source_wins(module) -> None:
    here = MODULE_PATH.parent
    queue = read_csv(here / "review_candidate_queue.csv")
    reviews = {row["paper_id"]: row for row in read_csv(ROOT / "reviews" / "universal" / "active_source_review.csv")}
    for row in queue:
        paper_id = row["canonical_paper_id"]
        if not paper_id or paper_id not in reviews:
            continue
        expected = module.scope_class(reviews[paper_id]["recommended_scope"])
        if expected:
            assert row["ledger_decision"] == expected, (paper_id, expected, row["ledger_decision"])


def main() -> int:
    module = load_module()
    test_current_outputs(module)
    test_ledger_precedence(module)
    test_strong_source_wins(module)
    print("review sets v2 regression checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
