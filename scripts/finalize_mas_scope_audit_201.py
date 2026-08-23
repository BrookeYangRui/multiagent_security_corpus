#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = ROOT / 'corpus'
SRC = C / 'MAS_SCOPE_AUDIT_2026-08-23.csv'
OUT = C / 'MAS_SCOPE_FINAL_AUDIT_2026-08-23.csv'
SUMMARY = C / 'MAS_SCOPE_AUDIT_SUMMARY_2026-08-23.md'

# Strict boundary: the work must substantively study security/privacy of an
# interacting LLM-agent system, or a security mechanism/evaluation whose result
# materially depends on inter-agent communication, shared state, delegation,
# aggregation, topology, identity, or another relation among agents. Merely
# using several agents as a generic safety/security tool is not sufficient.
MOVE_CONTEXT = {
    'doi:10.1609/aaai.v40i31.39812': ('DAWN is a distributed workflow-synthesis paper. Privacy is a deployment constraint for federated workflow learning, not a security property or adversarial MAS evaluation.', 'AAAI primary abstract/full text'),
    'supp_comet_metaphor_driven_covert_communication_for_multi_agent_language_games': ('CoMet improves metaphor use, covert communication, and semantic evasion in language games, but does not formulate or evaluate a MAS security property, adversary, attack, or defense.', 'ACL/arXiv primary abstract/full text'),
    'doi:10.1109/icassp49660.2025.10890479': ('The supervisor framework uses multi-agent interaction to improve generic LLM alignment against adversarial prompts; the protected object is the target LLM, not a security failure created by MAS interaction.', 'ICASSP publication metadata and source description'),
    'arxiv:2509.14285': ('This work uses a chain/coordinator of agents as a prompt-injection detector for ordinary LLM deployments. MAS is the defense instrument rather than the security object.', 'arXiv primary abstract/full text'),
    'doi:10.1109/apsec66846.2025.00086': ('MAJD is a multi-agent framework for generic jailbreak defense. Available source evidence supports MAS-as-defense-tool, not an interaction-native MAS security failure.', 'IEEE/APSEC publication and paper source'),
    'arxiv:2512.22496': ('HPO is a pedagogical reliability framework addressing tutoring sycophancy and answer quality through adversarial debate, not MAS security.', 'arXiv primary abstract'),
    'arxiv:2506.11083': ('RedDebate uses multi-agent red-team debate to make model responses safer on HarmBench; it evaluates generic output safety rather than security of the multi-agent interaction itself.', 'arXiv/OpenReview primary abstract'),
    'arxiv:2604.07911': ('Dynamic Attentional Context Scoping is an orchestration/reliability method for context pollution and steering accuracy without a concrete adversarial MAS security model.', 'primary paper abstract/current source record'),
    'arxiv:2605.12240': ('NOD is a reliability architecture for service agents, targeting policy violations, hallucinated tools, and long-horizon execution errors without an adversarial MAS threat model.', 'arXiv primary abstract'),
    'arxiv:2503.23138': ('EncGPT uses multiple agents to construct and operate dynamic encryption workflows; the research target is encryption generation/application, not security of the MAS.', 'primary paper abstract/current source record'),
    'arxiv:2604.23338': ('This is a broad LLM-agent security survey. Multi-Agent Coordination is one layer of a seven-layer agentic attack-surface model, so MAS security is a substantial subsection but not the paper-level analysis boundary.', 'arXiv primary abstract'),
    'arxiv:2604.13353': ('The primary contribution is a telecommunications query-translation architecture. PII anonymization/privacy preservation is one system feature, but the work does not study a MAS security threat or interaction-induced security failure.', 'arXiv primary abstract'),
    'doi:10.20944/preprints202602.1655.v1': ('This survey covers autonomous and collaborative LLM-agent security across external, cognitive, and multi-agent paradigms. MAS security is one branch of a broader agent-security survey rather than the paper-level scope.', 'Preprints.org v1 and companion repository'),
}

POST_CUTOFF = {
    'doi:10.2139/ssrn.7067276': ('First public SSRN posting is 2026-07-06, after the frozen 2026-07-01 literature cutoff.', 'SSRN posting record'),
    'doi:10.2139/ssrn.7181662': ('First public SSRN posting is 2026-07-31, after the frozen 2026-07-01 literature cutoff.', 'SSRN posting record'),
    'doi:10.2139/ssrn.7218206': ('First public SSRN posting is 2026-08-01, after the frozen 2026-07-01 literature cutoff.', 'SSRN posting record'),
}

HOLD_SOURCE = {
    'doi:10.5281/zenodo.19477187': ('The repository currently has only a metadata-only note and the primary source could not be reliably recovered during this audit. Under the corpus policy, it cannot be certified as in-scope without source evidence.', 'current metadata-only note; primary source unresolved'),
}

with SRC.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 201

fields = ['work_key','title','current_set','dominant_contribution','verdict','reason','evidence_basis','note_depth','paper_path']
out = []
for r in rows:
    key = r['work_key']
    if key in POST_CUTOFF:
        verdict = 'remove_post_cutoff'
        reason, basis = POST_CUTOFF[key]
    elif key in MOVE_CONTEXT:
        verdict = 'move_context_not_strict_mas_security'
        reason, basis = MOVE_CONTEXT[key]
    elif key in HOLD_SOURCE:
        verdict = 'hold_out_pending_primary_source'
        reason, basis = HOLD_SOURCE[key]
    else:
        verdict = 'keep_strict_mas_security'
        if r['note_depth'] == 'detailed':
            reason = 'Existing source note supports an interacting LLM-agent boundary plus a concrete security/privacy property, adversarial/fault condition, security mechanism, or interaction-specific security evaluation.'
            basis = 'existing detailed paper/source-review note'
        else:
            reason = 'Title/metadata and corpus evidence identify an interacting LLM-agent system with an explicit security/privacy threat, defense, guarantee, or evaluation; no contrary scope evidence was found in the strict re-screen.'
            basis = 'current paper record plus targeted source/abstract re-screen where needed'
    out.append({
        'work_key': key,
        'title': r['title'],
        'current_set': r['evidence_set'],
        'dominant_contribution': r['dominant_contribution'],
        'verdict': verdict,
        'reason': reason,
        'evidence_basis': basis,
        'note_depth': r['note_depth'],
        'paper_path': r['paper_path'],
    })

with OUT.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(out)

from collections import Counter
counts = Counter(r['verdict'] for r in out)
strict = counts['keep_strict_mas_security']
md = f'''# Strict MAS Security Scope Audit\n\nDate: `2026-08-23`\n\nThis audit re-checks all 201 manuscript-corpus works against a strict paper-level boundary: a retained work must substantively study security or privacy of interacting LLM-backed agents, or a security mechanism/evaluation whose claim materially depends on inter-agent communication, shared state, delegation, aggregation, topology, identity, or another agent relation. Merely using multiple agents as a generic safety/security tool is not enough.\n\n## Result\n\n* Re-screened: **201** works\n* Keep as strict MAS security: **{strict}**\n* Move to context because MAS security is not the paper-level boundary: **{counts['move_context_not_strict_mas_security']}**\n* Remove for post-cutoff first public availability: **{counts['remove_post_cutoff']}**\n* Hold out pending recoverable primary-source evidence: **{counts['hold_out_pending_primary_source']}**\n\nThe full row-level decisions are in `MAS_SCOPE_FINAL_AUDIT_2026-08-23.csv`. This audit does not itself mutate Set 1/Set 2 membership; it records the proposed strict correction first.\n'''
SUMMARY.write_text(md, encoding='utf-8')
print(counts)
