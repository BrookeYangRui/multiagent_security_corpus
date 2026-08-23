#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
C = R / "corpus"
P = R / "papers"

REMOVE = {
    # post-cutoff
    "doi:10.2139/ssrn.7067276": "post-cutoff first public availability",
    "doi:10.2139/ssrn.7181662": "post-cutoff first public availability",
    "doi:10.2139/ssrn.7218206": "post-cutoff first public availability",
    # broad agent-security surveys kept only as related-work comparators
    "arxiv:2604.23338": "broad agent-security survey; related-work comparator only",
    "doi:10.20944/preprints202602.1655.v1": "broad autonomous/collaborative agent-security survey; related-work comparator only",
    # unverifiable source
    "doi:10.5281/zenodo.19477187": "primary source could not be independently recovered",
    # user-approved strict-scope removals
    "doi:10.1609/aaai.v40i31.39812": "workflow synthesis rather than MAS-security paper-level boundary",
    "doi:10.1109/icassp49660.2025.10890479": "multi-agent alignment method rather than MAS-security paper-level boundary",
    "arxiv:2509.14285": "multi-agent pipeline used as generic prompt-injection defense instrument",
    "doi:10.1109/apsec66846.2025.00086": "multi-agent jailbreak-defense instrument rather than security of MAS interaction",
    "arxiv:2512.22496": "pedagogical reliability/oversight rather than MAS-security paper-level boundary",
    "arxiv:2506.11083": "multi-agent red-team debate used for generic response safety",
    "arxiv:2503.23138": "multi-agent encryption workflow rather than security of MAS interaction",
    "arxiv:2604.13353": "network-troubleshooting architecture with privacy as a feature rather than MAS-security boundary",
}

KEEP_EXPLICIT = {
    "supp_comet_metaphor_driven_covert_communication_for_multi_agent_language_games",
    "arxiv:2604.07911",  # DACS
    "arxiv:2605.12240",  # NOD
}

EXPECTED_COUNTS = {"set1_core": 91, "set2_emerging": 96, "total_corpus": 187}
EXPECTED_CONTRIB = {"attack": 44, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}
CATEGORY_DIR = {"attack": "attacks", "defense": "defenses", "evaluation": "evaluations", "general": "general", "survey": "surveys"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows):
    if not rows:
        raise SystemExit(f"refusing to write empty CSV: {path}")
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


s1 = read_csv(C / "set1_core.csv")
s2 = read_csv(C / "set2_emerging.csv")
all_before = s1 + s2
before_keys = {r["work_key"] for r in all_before}
missing = set(REMOVE) - before_keys
if missing:
    raise SystemExit(f"removal keys not found: {sorted(missing)}")
if not KEEP_EXPLICIT.issubset(before_keys):
    raise SystemExit(f"explicit keep keys missing: {sorted(KEEP_EXPLICIT - before_keys)}")

s1 = [r for r in s1 if r["work_key"] not in REMOVE]
s2 = [r for r in s2 if r["work_key"] not in REMOVE]
write_csv(C / "set1_core.csv", s1)
write_csv(C / "set2_emerging.csv", s2)

idx = read_csv(P / "index.csv")
removed_idx = [r for r in idx if r["work_key"] in REMOVE]
if len(removed_idx) != 14:
    raise SystemExit(f"expected 14 paper-index removals, got {len(removed_idx)}")
for r in removed_idx:
    path = R / r["paper_path"]
    if path.exists():
        path.unlink()
idx = [r for r in idx if r["work_key"] not in REMOVE]
write_csv(P / "index.csv", idx)

# Chu and Sun remain in the related-work comparator view, but are not corpus members.
sp = R / "sok_related" / "papers.csv"
comparators = read_csv(sp)
for r in comparators:
    if r["sok_id"] in {"chu2026layered", "sun2026unique_security"}:
        r["in_final_201"] = "no"
        r["final_paper_path"] = ""
write_csv(sp, comparators)

all_rows = s1 + s2
counts = Counter(r["dominant_contribution"] for r in all_rows)
if len(s1) != 91 or len(s2) != 96 or len(all_rows) != 187:
    raise SystemExit(f"membership mismatch: {len(s1)}/{len(s2)}/{len(all_rows)}")
if dict(counts) != EXPECTED_CONTRIB:
    raise SystemExit(f"contribution mismatch: {dict(counts)}")
if not KEEP_EXPLICIT.issubset({r["work_key"] for r in all_rows}):
    raise SystemExit("CoMet, DACS, or NOD was accidentally removed")

manifest = json.loads((C / "manifest.json").read_text(encoding="utf-8"))
manifest["counts"] = EXPECTED_COUNTS
manifest["contributions"] = EXPECTED_CONTRIB
(C / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

(R / "README.md").write_text("""# Multi Agent Security Corpus

Auditable literature corpus for security of interacting LLM agents. Literature cutoff: `2026-07-01`.

## Authoritative manuscript corpus

There is one active manuscript corpus: **187 works**.

| Set | Count | Meaning |
| --- | ---: | --- |
| Set 1 | 91 | In-scope mature MAS security work |
| Set 2 | 96 | In-scope emerging MAS security work |
| **Total** | **187** | **Authoritative MAS security corpus** |

The authoritative row-level files are `corpus/set1_core.csv` and `corpus/set2_emerging.csv`.

The 2026-08-23 scope correction removed 14 records from the previous 201-work view. Three were first public after the cutoff, two broad agent-security surveys remain only as related-work comparators, one source could not be independently recovered, and eight additional works were removed because MAS was primarily a tool or application architecture rather than the paper-level security object. CoMet, DACS, and NOD remain in scope.

## Paper organization

`papers/` contains exactly the active corpus notes, organized by dominant contribution and venue. Current totals are **44 attacks**, **80 defenses**, **44 evaluations**, **12 general works**, and **7 surveys**.

## Validation

Run `scripts/validate_all.sh`.
""", encoding="utf-8")

(C / "README.md").write_text("""# Authoritative 187 work corpus

Only Set 1 and Set 2 are active manuscript evidence sets.

| File | Count | Meaning |
| --- | ---: | --- |
| `set1_core.csv` | 91 | Mature in-scope MAS security work |
| `set2_emerging.csv` | 96 | Emerging in-scope MAS security work |
| **Union** | **187** | **Exact manuscript corpus** |

Both sets use the same MAS-security scope gate. Set 1 additionally satisfies the frozen maturity rule: peer reviewed or at least 10 frozen citations.
""", encoding="utf-8")

(R / "FROZEN_SNAPSHOT.md").write_text("""# Frozen corpus snapshot

Literature cutoff: `2026-07-01`

Final scope correction: `2026-08-23`

| Partition | Count |
| --- | ---: |
| Set 1 | 91 |
| Set 2 | 96 |
| **Authoritative corpus** | **187** |

The 187-work union is the sole manuscript-facing corpus.
""", encoding="utf-8")

(R / "CORPUS_SET_POLICY.md").write_text("""# Corpus policy

## Scope gate

A work enters the active corpus only if all of the following hold:

1. It studies at least two separately addressable LLM-backed agents or principals.
2. A material inter-agent relation or interaction path is present.
3. It studies a concrete security property, attack, defense, guarantee, adversary, or security evaluation.
4. The security claim is about the interacting system or materially depends on an inter-agent relation; merely using multiple agents as a generic security or safety instrument is not enough.
5. Source evidence is sufficient to support the membership decision.
6. The work was publicly available by the frozen literature cutoff `2026-07-01`.

Interaction-dependence strength remains an evidence characterization, not a separate membership tier. Covert coordination, cross-agent context control, and cross-agent action control can satisfy the scope gate when the protected or adversarial property is relational.

Broad agent-security surveys may remain in `sok_related/` without entering the active evidence corpus.

## Set 1 and Set 2

Set 1 uses `peer_reviewed == yes OR frozen_citation_count >= 10`. Set 2 contains the remaining in-scope emerging work. The current corpus is **91 Set 1 + 96 Set 2 = 187 works**.
""", encoding="utf-8")

(R / "AGENTS.md").write_text("""# Corpus Maintenance Protocol

## Single authoritative corpus

There is one active manuscript corpus: **187 works**.

* `corpus/set1_core.csv`: 91 mature in-scope works
* `corpus/set2_emerging.csv`: 96 emerging in-scope works
* `papers/index.csv`: one-to-one materialized view of the same 187 works

Do not restore superseded denominators or removed screening artifacts to the active tree.

## Scope and maturity

Apply `CORPUS_SET_POLICY.md`. MAS must be the security object or the security consequence must materially depend on inter-agent interaction. Using multiple agents merely as a generic detector, red-team method, alignment method, workflow, or application architecture is insufficient by itself. The frozen literature cutoff is `2026-07-01`.

Set 1 uses `peer_reviewed == yes OR frozen_citation_count >= 10`; Set 2 contains the remaining in-scope works.

## Paper notes

Every active work appears exactly once under `papers/` and in `papers/index.csv`. Current dominant-contribution totals are **44 attacks, 80 defenses, 44 evaluations, 12 general works, and 7 surveys**.

A work outside the active 187 must not have a paper note under `papers/`. `sok_related/` is a supporting comparator view and is never added to the corpus denominator.

## Validation

Run `scripts/validate_all.sh`. Validation must enforce Set 1 = 91, Set 2 = 96, total = 187, the 44/80/44/12/7 contribution partition, exact paper-index membership, and exactly 187 non-README paper notes.
""", encoding="utf-8")

(P / "README.md").write_text("""# Final 187 paper corpus

This directory contains exactly **187 works**: **91 Set 1** and **96 Set 2**.

| Contribution | Count | Directory |
| --- | ---: | --- |
| attack | 44 | [`attacks/`](attacks/) |
| defense | 80 | [`defenses/`](defenses/) |
| evaluation | 44 | [`evaluations/`](evaluations/) |
| general | 12 | [`general/`](general/) |
| survey | 7 | [`surveys/`](surveys/) |

[`index.csv`](index.csv) is the exact one-to-one mapping from the 187 work keys to paper-note paths.
""", encoding="utf-8")

# Regenerate category README files from the final index.
for category, dirname in CATEGORY_DIR.items():
    rows_cat = [r for r in idx if r["dominant_contribution"] == category]
    by_venue = {}
    for r in rows_cat:
        by_venue.setdefault(r["venue_folder"], []).append(r)
    lines = [f"# {category.title()} papers", "", f"Final 187-corpus dominant-contribution count: **{len(rows_cat)}**.", ""]
    for venue in sorted(by_venue):
        lines += [f"## {venue}", ""]
        for r in sorted(by_venue[venue], key=lambda x: x["title"].lower()):
            rel = Path(r["paper_path"]).relative_to(P / dirname)
            lines.append(f"* [{r['title']}]({rel.as_posix()})  `{r['evidence_set']}`")
        lines.append("")
    (P / dirname / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

(R / "related_work" / "attacks.md").write_text("""# Attacks

This synthesis is anchored to the final **187-work** manuscript corpus. It contains **44 attack-primary works**. A paper in another dominant-contribution category may still provide attack evidence, so 44 is not the total number of works containing attack results.

Use `papers/attacks/README.md` for the complete attack-primary list and individual notes for technical claims and evidence locations.
""", encoding="utf-8")

(R / "related_work" / "benchmarks.md").write_text("""# Benchmarks and Evaluations

This synthesis is anchored to the final **187-work** manuscript corpus. It contains **44 evaluation-primary works**. The evaluation set spans attack benchmarks, security auditing frameworks, privacy measurements, topology studies, collusion and deception evaluations, and system-level robustness studies.

Use `papers/evaluations/README.md` for the complete list and individual notes for units, baselines, metrics, and evidence locations.
""", encoding="utf-8")

(R / "related_work" / "surveys_and_soks.md").write_text("""# Multi Agent Security Surveys and SoKs

The active evidence denominator is the final **187-work** corpus, including **7 survey-primary works**.

Two broader agent-security surveys, `chu2026layered` and `sun2026unique_security`, are intentionally outside the strict MAS-security corpus and remain in `sok_related/` as strongly related comparators. Their unit of analysis extends beyond interaction-dependent MAS security.

`sok_related/` is a supporting comparator view and is never added to the 187-work denominator. Use primary attack, defense, and evaluation papers for empirical claims whenever possible.
""", encoding="utf-8")

(R / "sok_related" / "README.md").write_text("""# Strongly Related Multi Agent Security SoKs

This directory is a supporting comparator view, not an active corpus partition. The manuscript evidence corpus contains **187 works**.

Comparator records may overlap the corpus or may be contextual only. Broad agent-security surveys such as Chu et al. and Sun et al. remain here even though they are outside the strict MAS-security evidence corpus. Never add this directory's row count to 187.
""", encoding="utf-8")

# The defense re-audit files were intermediate 201-work artifacts and are no longer active.
for stale in [C / "DEFENSE_REAUDIT_2026-08-23.md", C / "defense_reaudit_2026-08-23.csv"]:
    if stale.exists():
        stale.unlink()

# Update validator invariants.
vpath = R / "scripts" / "validate_corpus.py"
v = vpath.read_text(encoding="utf-8")
v = v.replace('EXPECTED_COUNTS = {"set1_core": 96, "set2_emerging": 105, "total_corpus": 201}', 'EXPECTED_COUNTS = {"set1_core": 91, "set2_emerging": 96, "total_corpus": 187}')
v = v.replace('EXPECTED_CONTRIB = {"attack": 44, "defense": 85, "evaluation": 46, "general": 16, "survey": 10}', 'EXPECTED_CONTRIB = {"attack": 44, "defense": 80, "evaluation": 44, "general": 12, "survey": 7}')
v = v.replace('(len(s1), len(s2)) != (96, 105)', '(len(s1), len(s2)) != (91, 96)')
v = v.replace('if len(all_rows) != 201:', 'if len(all_rows) != 187:')
v = v.replace('active corpus is not 201', 'active corpus is not 187')
v = v.replace('signed 201 corpus', 'active 187 corpus')
v = v.replace('if len(index) != 201:', 'if len(index) != 187:')
v = v.replace('must have 201 rows', 'must have 187 rows')
v = v.replace('if len({r["work_key"] for r in index}) != 201:', 'if len({r["work_key"] for r in index}) != 187:')
v = v.replace('if len(notes) != 201:', 'if len(notes) != 187:')
v = v.replace('expected exactly 201 paper notes', 'expected exactly 187 paper notes')
v = v.replace('final 201 corpus', 'active 187 corpus')
v = v.replace('Final corpus valid: Set1=96 Set2=105 total=201; papers=201;', 'Final corpus valid: Set1=91 Set2=96 total=187; papers=187;')
vpath.write_text(v, encoding="utf-8")

print("Final corpus cleanup complete: Set1=91 Set2=96 total=187; contributions=44/80/44/12/7")
