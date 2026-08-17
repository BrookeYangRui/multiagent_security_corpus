#!/usr/bin/env python3
"""Hardened source-evidence rebuild for the three-set MAS security corpus."""

from __future__ import annotations

import csv
import gzip
import importlib.util
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EVIDENCE = ROOT / "review-evidence"
BUILDER = ROOT / "scripts" / "build_three_set_corpus.py"

IDENTITY = {
    "work_key", "dedup_key", "record_id", "paper_id", "canonical_paper_id",
    "title", "paper_title", "display_name", "work_title", "doi",
    "canonical_doi", "arxiv_id", "arxiv", "eprint",
}


def text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def flatten(value: object, prefix: str = "") -> dict[str, str]:
    result: dict[str, str] = {}
    if isinstance(value, dict):
        for raw_key, item in value.items():
            key = f"{prefix}.{raw_key}" if prefix else str(raw_key)
            if isinstance(item, dict):
                result.update(flatten(item, key))
            elif isinstance(item, list):
                if item and all(isinstance(entry, dict) for entry in item):
                    for index, entry in enumerate(item):
                        result.update(flatten(entry, f"{key}.{index}"))
                else:
                    result[key] = "; ".join(text(entry) for entry in item)
            else:
                result[key] = text(item)
    else:
        result[prefix or "value"] = text(value)
    return result


def has_identity(flat: dict[str, str]) -> bool:
    return any(key.lower().split(".")[-1] in IDENTITY and value for key, value in flat.items())


def objects(value: object) -> Iterator[dict[str, str]]:
    if isinstance(value, list):
        for item in value:
            yield from objects(item)
        return
    if not isinstance(value, dict):
        return
    flat = flatten(value)
    if has_identity(flat):
        yield flat
        return
    for item in value.values():
        if isinstance(item, (dict, list)):
            yield from objects(item)


def records(path: Path) -> Iterator[dict[str, str]]:
    lowered = path.name.lower()
    try:
        if lowered.endswith(".csv"):
            with path.open(encoding="utf-8-sig", newline="") as handle:
                for row in csv.DictReader(handle):
                    yield {str(key): text(value) for key, value in row.items()}
        elif lowered.endswith(".jsonl.gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if line.strip():
                        yield from objects(json.loads(line))
        elif lowered.endswith(".json.gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
                yield from objects(json.load(handle))
        elif lowered.endswith(".jsonl"):
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if line.strip():
                        yield from objects(json.loads(line))
        elif lowered.endswith(".json"):
            yield from objects(json.loads(path.read_text(encoding="utf-8", errors="replace")))
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError):
        return


def terminal(key: str) -> str:
    return key.lower().split(".")[-1]


def value_for(row: dict[str, str], aliases: set[str]) -> str:
    for key, value in row.items():
        if terminal(key) in aliases and value:
            return value
    return ""


def load_module():
    spec = importlib.util.spec_from_file_location("three_set_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import three-set builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_index(builder):
    by_id: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    by_title: dict[str, list[dict[str, object]]] = defaultdict(list)
    inventory: list[dict[str, object]] = []
    suffixes = (".csv", ".json", ".jsonl", ".json.gz", ".jsonl.gz")

    for path in sorted(EVIDENCE.rglob("*")):
        if not path.is_file() or not path.name.lower().endswith(suffixes):
            continue
        parsed = list(records(path))
        rel = str(path.relative_to(EVIDENCE))
        inventory.append({"path": rel, "rows": len(parsed)})
        for row in parsed:
            work = value_for(row, {"work_key", "dedup_key", "record_id", "paper_id", "canonical_paper_id"})
            title = value_for(row, {"title", "paper_title", "display_name", "work_title", "openalex_title", "s2_title", "crossref_title", "arxiv_title"})
            doi = builder.normalize_doi(value_for(row, {"doi", "canonical_doi", "publication_doi", "publisher_doi"}))
            arxiv = builder.normalize_arxiv(value_for(row, {"arxiv_id", "arxiv", "eprint", "arxiv_identifier"}))
            if not doi:
                for item in row.values():
                    doi = builder.normalize_doi(item)
                    if doi:
                        break
            if not arxiv:
                for item in row.values():
                    arxiv = builder.normalize_arxiv(item)
                    if arxiv:
                        break
            record = {"source_file": rel, "row": row}
            if work:
                by_id[("work", work)].append(record)
            if doi:
                by_id[("doi", doi)].append(record)
            if arxiv:
                by_id[("arxiv", arxiv)].append(record)
            normalized = builder.normalize_title(title)
            if normalized:
                by_title[normalized].append(record)

    parsed_count = sum(int(item["rows"]) for item in inventory)
    if parsed_count < 1000:
        raise SystemExit(f"too few source-review records parsed: {parsed_count}")
    return by_id, by_title, inventory


def reconstruct_queue() -> None:
    queue = CORPUS / "review_queue.csv"
    if queue.exists():
        return
    ledger = CORPUS / "review_ledger.csv"
    if not ledger.exists():
        raise SystemExit("review ledger is missing")
    with ledger.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 2217:
        raise SystemExit(f"unexpected review ledger size: {len(rows)}")

    rebuilt: list[dict[str, str]] = []
    for row in rows:
        item = dict(row)
        set_name = row.get("evidence_set", "")
        item["decision"] = {
            "set1_core": "primary",
            "set2_emerging": "secondary",
            "set3_context": "secondary",
            "screened_out": "exclude",
        }.get(set_name, row.get("previous_decision", ""))
        category = row.get("dominant_contribution", "") or row.get("previous_category", "")
        item["current_primary_category"] = category
        item["broad_role"] = category
        item["rationale"] = row.get("decision_reason", "") or row.get("scope_reason", "")
        item["scope_relation"] = "core_security" if set_name in {"set1_core", "set2_emerging"} else (
            "security_relevant" if set_name == "set3_context" else ""
        )
        rebuilt.append(item)

    fields: list[str] = []
    for row in rebuilt:
        for key in row:
            if key not in fields:
                fields.append(key)
    with queue.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rebuilt)


def read(name: str) -> list[dict[str, str]]:
    with (CORPUS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def audit_outputs() -> None:
    set1 = read("set1_core.csv")
    set2 = read("set2_emerging.csv")
    set3 = read("set3_context.csv")
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    inventory = manifest.get("source_file_inventory") or []
    if sum(int(row.get("rows", 0)) for row in inventory) < 1000:
        raise SystemExit("source-review inventory is incomplete")
    if len(set3) < 10:
        raise SystemExit(f"context set is implausibly small: {len(set3)}")
    for label, rows in (("Set 1", set1), ("Set 2", set2)):
        if any(row.get("evidence_basis") == "title_metadata" for row in rows):
            raise SystemExit(f"{label} contains title-only evidence")
        if any(not row.get("dominant_contribution") for row in rows):
            raise SystemExit(f"{label} contains an untagged contribution")
        if any(row.get("interaction_interfaces") in {"", "unspecified"} for row in rows):
            raise SystemExit(f"{label} contains an unspecified interaction interface")
        if any(row.get("risk_or_property") in {"", "unspecified"} for row in rows):
            raise SystemExit(f"{label} contains an unspecified risk or property")
        if any(row.get("interaction_dependence") in {"", "unclear"} for row in rows):
            raise SystemExit(f"{label} contains unclear interaction dependence")


def main() -> int:
    reconstruct_queue()
    builder = load_module()
    evidence_index = make_index(builder)
    builder.load_source_index = lambda: evidence_index
    status = int(builder.main())
    audit_outputs()
    shutil.rmtree(EVIDENCE, ignore_errors=True)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
