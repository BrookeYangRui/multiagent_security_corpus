#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / "corpus"
EXPECTED = {"primary":303, "secondary":177, "exclude":1396, "pending":341}
ROLE_VALUES = {"attack","defense","evaluation","other"}

def rows(name):
    with (C / name).open(encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

queue=rows("review_queue.csv")
if len(queue) != 2217:
    raise SystemExit(f"review_queue count {len(queue)} != 2217")
keys=[r["work_key"] for r in queue]
if len(set(keys)) != len(keys):
    raise SystemExit("duplicate work_key in review_queue")

seen=set()
for decision,count in EXPECTED.items():
    data=rows(f"{decision}.csv")
    if len(data) != count:
        raise SystemExit(f"{decision} count {len(data)} != {count}")
    part={r["work_key"] for r in data}
    if len(part) != len(data):
        raise SystemExit(f"duplicate work_key in {decision}")
    if seen & part:
        raise SystemExit(f"decision sets overlap at {decision}")
    seen |= part
if seen != set(keys):
    raise SystemExit("decision sets do not partition review_queue")

for name in ("primary","secondary"):
    data=rows(f"{name}.csv")
    bad={r["broad_role"] for r in data} - ROLE_VALUES
    if bad:
        raise SystemExit(f"invalid broad roles in {name}: {sorted(bad)}")

routes=rows("routes.csv")
targeted=[r for r in routes if r.get("route_type")=="targeted"]
if len(targeted) != 318:
    raise SystemExit(f"targeted route count {len(targeted)} != 318")
if len({r["work_key"] for r in targeted}) != 317:
    raise SystemExit("targeted route does not resolve to 317 works")

manifest=json.loads((C/"manifest.json").read_text(encoding="utf-8"))
expected_manifest={"exclude":1396,"pending":341,"primary":303,"secondary":177,"total":2217}
if manifest["authoritative_counts"] != expected_manifest:
    raise SystemExit("manifest authoritative counts changed")
for name,meta in manifest["files"].items():
    path=C/name
    if not path.exists():
        raise SystemExit(f"manifest file missing: {name}")
    if digest(path) != meta["sha256"]:
        raise SystemExit(f"manifest digest mismatch: {name}")

print("Authoritative corpus valid: 2,217 works = 303 primary + 177 secondary + 1,396 exclude + 341 pending; targeted route 318 records / 317 works.")
