#!/usr/bin/env python3
"""Patch the frozen 2026-08-17 source-review builder to the revised corpus policy.

The base builder is restored from commit f5c205e during the one-shot source
rerun. These replacements change only scope and maturity semantics. Scope
signals are taken from the title and abstract so incidental mentions in Related
Work do not promote a paper. The frozen pre-policy ledger remains a negative
anchor, except where the old exclusion was specifically caused by the former
interaction-dependence requirement or a newly available title is explicitly
about MAS security. Interaction presence is a scope condition while interaction
dependence is not. The maturity threshold is >=10.
"""

from __future__ import annotations

import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one {label} block, found {count}")
    return text.replace(old, new, 1)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: patch_source_scope_policy.py BUILDER.py")
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    text = replace_once(
        text,
        '    "agent-to-agent security", "failure propagation", "cascade",\n]\n',
        '    "agent-to-agent security", "failure propagation", "cascade",\n'
        '    "multi-agent safety", "safety of multi-agent", "safe multi-agent",\n'
        '    "multi-agent trust", "trust in multi-agent", "multi-agent reliability",\n'
        '    "reliability of multi-agent", "multi-agent robustness",\n'
        '    "robustness of multi-agent", "faulty agents", "fault tolerance",\n'
        '    "fault-tolerance", "collective integrity", "collective safety",\n'
        ']\n',
        "system-target terms",
    )

    text = replace_once(
        text,
        '    parts = [\n'
        '        clean(queue_row.get("title", "")),\n'
        '        clean(queue_row.get("rationale", "")),\n'
        '        clean(queue_row.get("screening_note", "")),\n'
        '    ]\n',
        '    # Scope signals must come from the paper/source, not prior review labels.\n'
        '    parts = [clean(queue_row.get("title", ""))]\n',
        "source-text parts",
    )

    text = replace_once(
        text,
        '    all_text = clean(" ".join(parts + [abstract_text, evidence_text, paper_text]))\n',
        '    # Corpus membership is based on the paper\'s stated contribution.\n'
        '    # Full text is retained for later taxonomy/evidence extraction, but\n'
        '    # it cannot make a paper in-scope merely because Related Work mentions\n'
        '    # attacks, privacy, or other MAS-security terms.\n'
        '    all_text = clean(" ".join(parts + [abstract_text]))\n',
        "source-text composition",
    )

    text = replace_once(
        text,
        '    survey = has_any(text, SURVEY_TERMS)\n\n'
        '    scope_pass = False\n',
        '    survey = has_any(text, SURVEY_TERMS)\n'
        '    # Direct security always qualifies as a protected property. Softer\n'
        '    # safety/trust/reliability language qualifies only when the source\n'
        '    # explicitly targets the multi-agent system rather than an external task.\n'
        '    security_property = direct_security or (soft_security and system_target)\n'
        '    frozen_scope = clean(queue_row.get("strict_scope_pass", "")).lower()\n'
        '    frozen_reason = clean(queue_row.get("scope_reason", "")).lower()\n'
        '    title_text = clean(queue_row.get("title", "")).lower()\n'
        '    explicit_security_title = (\n'
        '        has_any(title_text, MULTI_TERMS)\n'
        '        and (has_any(title_text, DIRECT_SECURITY_TERMS) or has_any(title_text, SOFT_SECURITY_TERMS))\n'
        '    )\n'
        '    # A frozen negative decision is reconsidered only when the old reason\n'
        '    # was the interaction-dependence requirement we are intentionally\n'
        '    # removing, or when the title itself clearly identifies MAS security.\n'
        '    reconsider_old_negative = (\n'
        '        "interaction-dependent mechanism" in frozen_reason\n'
        '        or explicit_security_title\n'
        '    )\n'
        '    hard_prior_exclude = frozen_scope == "no" and not reconsider_old_negative\n\n'
        '    scope_pass = False\n',
        "security-property definition",
    )

    text = replace_once(
        text,
        '    elif prior_include and not (prior_exclude and not canonical):\n'
        '        scope_pass = True\n'
        '        scope_reason = (\n'
        '            "Prior source review explicitly included the work as "\n'
        '            "interaction-security evidence."\n'
        '        )\n'
        '    elif has_llm and has_multi and direct_security and interaction \\\n'
        '            and (system_target or count_terms(text, INTERACTION_TERMS) >= 2):\n',
        '    elif hard_prior_exclude:\n'
        '        scope_reason = (\n'
        '            "Frozen source review kept the work outside the MAS-security "\n'
        '            "corpus for a reason other than the former interaction-dependence gate."\n'
        '        )\n'
        '    elif has_llm and has_multi and security_property and interaction:\n',
        "scope gate",
    )

    text = replace_once(
        text,
        '        if not direct_security:\n'
        '            missing.append("direct security property")\n'
        '        if not interaction:\n'
        '            missing.append("interaction-dependent mechanism")\n'
        '        scope_reason = "Strict scope not established: missing " + ", ".join(\n',
        '        if not security_property:\n'
        '            missing.append("security/safety/trust property")\n'
        '        if not interaction:\n'
        '            missing.append("material inter-agent interaction path")\n'
        '        scope_reason = "MAS-security scope not established: missing " + ", ".join(\n',
        "missing-signal wording",
    )

    text = replace_once(
        text,
        '    mature = peer_reviewed == "yes" or citations > 10\n',
        '    mature = peer_reviewed == "yes" or citations >= 10\n',
        "maturity threshold",
    )

    text = text.replace(
        'Passed strict MAS-security scope. Maturity:',
        'Passed MAS-security scope. Maturity:',
    )
    text = text.replace(
        '"Meets the Set 1 union rule."',
        '"Meets the Set 1 union rule (peer reviewed OR citations >= 10)."',
    )

    path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
