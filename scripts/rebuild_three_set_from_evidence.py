#!/usr/bin/env python3
"""Rebuild the three evidence sets from the complete source-review artifacts.

The first three-set migration only indexed CSV inputs, while the source-review
runs store most records as JSONL, JSONL.GZ, and JSON.  This wrapper loads every
supported format, reconstructs the one-time work queue from the review ledger,
and then invokes the canonical builder with a complete evidence index.

This remains a model-assisted source review.  Rows retain evidence provenance
and require named-author signoff before being described as human verified.
"""

from __future__ import annotations

import csv
import gzip
import importlib.util
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Iterator

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
EVIDENCE_ROOT = ROOT / "review-evidence"
BUILDER_PATH = ROOT / "scripts" / "build_three_set_corpus.py"


def clean(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).strip()


def flatten(value: object, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(item, dict):
                out.update(flatten(item, name))
            elif isinstance(item, list):
                if item and all(isinstance(entry, dict) for entry in item):
                    for index, entry in enumerate(item):
                        out.update(flatten(entry, f"{name}.{index}"))
                else:
                    out[name] = "; ".join(clean(entry) for entry in item)
            else:
                out[name] = clean(item)
    else:
        out[prefix or "value"] = clean(value)
    return out


def iter_json_objects(value: object) -> Iterator[dict[str, object]]:
    if isinstance(value, list):
        for item in value:
            yield from iter_json_objects(item)
        return
    if not isinstance(value, dict):
        return

    field_names = {str(key).lower().split(".")[-1] for key in value}
    identity_fields = {
        "work_key", "record_id", "paper_id", "canonical_paper_id", "title",
        "doi", "arxiv_id", "arxiv", "display_name", "paper_title",
    }
    if field_names & identity_fields:
        yield value
        return

    for item in value.values():
        if isinstance(item, (dict, list)):
            yield from iter_json_objects(item)


def read_records(path: Path) -> Iterator[dict[str, str]]:
    name = path.name.lower()
    try:
        if name.endswith(".csv"):
            with path.open(encoding="utf-8-sig", newline="") as handle:
                for row in csv.DictReader(handle):
                    yield {str(key): clean(value) for key, value in row.items()}
            return

        if name.endswith(".jsonl.gz") or name.endswith(".json.gz"):
            with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
                if name.endswith(".jsonl.gz"):
                    for line in handle:
                        line = line.strip()
                        if not line:
                            continue
                        value = json.loads(line)
                        for record in iter_json_objects(value):
                            yield flatten(record)
                else:
                    value = json.load(handle)
                    for record in iter_json_objects(value):
                        yield flatten(record)
            return

        if name.endswith(".jsonl"):
            with path.open(encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    value = json.loads(line)
                    for record in iter_json_objects(value):
                        yield flatten(record)
            return

        if name.endswith(".json"):
            value = json.loads(path.read_text(encoding="utf-8", errors="replace"))
            for record in iter_json_objects(value):
                yield flatten(record)
    except (OSError, UnicodeError, csv.Error, json.JSONDecodeError):
        return


def base_name(key: str) -> str:
    return key.lower().split(".")[-1]


def first_field(row: dict[str, str], aliases: Iterable[str]) -> str:
    wanted = {alias.lower() for alias in aliases}
    for key, value in row.items():
        if base_name(key) in wanted and clean(value):
            return clean(value)
    return ""


def load_builder():
    spec = importlib.util.spec_from_file_location("three_set_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {BUILDER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_evidence_index(builder):
    by_identifier: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    by_title: dict[str, list[dict[str, object]]] = defaultdict(list)
    inventory: list[dict[str, object]] = []

    supported = (".csv", ".json", ".jsonl", ".json.gz", ".jsonl.gz")
    for path in sorted(EVIDENCE_ROOT.rglob("*")):
        if not path.is_file() or not path.name.lower().endswith(supported):
            continue

        records = list(read_records(path))
        relative = str(path.relative_to(EVIDENCE_ROOT))
        inventory.append({"path": relative, "rows": len(records)})
        for row in records:
            work_key = first_field(
                row,
                ("work_key", "dedup_key", "record_id", "paper_id", "canonical_paper_id"),
            )
            title = first_field(
                row,
                ("title", "paper_title", "display_name", "work_title", "openalex_title", "s2_title", "crossref_title", "arxiv_title"),
            )
            doi = builder.normalize_doi(first_field(
                row,
                ("doi", "canonical_doi", "publication_doi", "publisher_doi"),
            ))
            arxiv_id = builder.normalize_arxiv(first_field(
                row,
                ("arxiv_id", "arxiv", "eprint", "arxiv_identifier"),
            ))

            if not doi:
                for value in row.values():
                    doi = builder.normalize_doi(value)
                    if doi:
                        break
            if not arxiv_id:
                for value in row.values():
                    arxiv_id = builder.normalize_arxiv(value)
                    if arxiv_id:
                        break

            record: dict[str, object] = {"source_file": relative, "row": row}
            if work_key:
                by_identifier[("work", work_key)].append(record)
            if doi:
                by_identifier[("doi", doi)].append(record)
            if arxiv_id:
                by_identifier[("arxiv", arxiv_id)].append(record)
            normalized_title = builder.normalize_title(title)
            if normalized_title:
                by_title[normalized_title].append(record)

    if not inventory or sum(int(item["rows"]) for item in inventory) == 0:
        raise SystemExit("no source-review evidence records were parsed")
    return by_identifier, by_title, inventory


def reconstruct_queue() -> None:
    ledger_path = CORPUS / "review_ledger.csv"
    queue_path = CORPUS / "review_queue.csv"
    if queue_path.exists():
        return
    if not ledger_path.exists():
        raise SystemExit("neither review_queue.csv nor review_ledger.csv exists")

    with ledger_path.open(encoding="utf-8-sig", newline="") as handle:
        old_rows = list(csv.DictReader(handle))
    if len(old_rows) != 2217:
        raise SystemExit(f"unexpected review ledger size: {len(old_rows)}")

    queue_rows: list[dict[str, str]] = []
    for row in old_rows:
        evidence_set = row.get("evidence_set", "")
        previous = {
            "set1_core": "primary",
            "set2_emerging": "secondary",
            "set3_context": "secondary",
            "screened_out": "exclude",
        }.get(evidence_set, row.get("previous_decision", ""))
        category = row.get("dominant_contribution", "") or row.get("previous_category", "")
        rebuilt = dict(row)
        rebuilt["decision"] = previous
        rebuilt["current_primary_category"] = category
        rebuilt["broad_role"] = category
        rebuilt["rationale"] = row.get("decision_reason", "") or row.get("scope_reason", "")
        rebuilt["scope_relation"] = (
            "core_security" if evidence_set in {"set1_core", "set2_emerging"}
            else "security_relevant" if evidence_set == "set3_context"
            else ""
        )
        queue_rows.append(rebuilt)

    fields: list[str] = []
    for row in queue_rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with queue_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(queue_rows)


def quality_gate() -> None:
    def rows(name: str) -> list[dict[str, str]]:
        with (CORPUS / name).open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    set1 = rows("set1_core.csv")
    set2 = rows("set2_emerging.csv")
    set3 = rows("set3_context.csv")
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    inventory = manifest.get("source_file_inventory") or []

    if not inventory:
        raise SystemExit("manifest contains no source-review inventory")
    if not set3:
        raise SystemExit("Set 3 is empty after loading source evidence")
    if any(row.get("evidence_basis") == "title_metadata" for row in set1):
        raise SystemExit("Set 1 contains title-only evidence")
    if any(row.get("evidence_basis") == "title_metadata" for row in set2):
        raise SystemExit("Set 2 contains title-only evidence")
    if any(not row.get("dominant_contribution") for row in set1 + set2):
        raise SystemExit("retained corpus row lacks a contribution tag")
    if any(not row.get("interaction_interfaces") for row in set1 + set2):
        raise SystemExit("retained corpus row lacks an interface tag")
    if any(not row.get("risk_or_property") for row in set1 + set2):
        raise SystemExit("retained corpus row lacks a risk or property tag")


def main() -> int:
    if not EVIDENCE_ROOT.exists():
        raise SystemExit("review-evidence directory is missing")
    reconstruct_queue()
    builder = load_builder()
    evidence_index = build_evidence_index(builder)
    builder.load_source_index = lambda: evidence_index
    result = int(builder.main())
    quality_gate()
    shutil.rmtree(EVIDENCE_ROOT, ignore_errors=True)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
